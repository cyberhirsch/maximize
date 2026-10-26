# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's cameras: the Point-of-View menu (V over a viewport, Max's "[Camera001]" label menu), Select
Camera, Lock Camera to View, Lock Camera, the Target Camera (drag from the camera to the target),
Field of View dragging, Roll, and vertical tilt correction (2-point perspective through lens
shift).

Everything is Blender data: cameras, an empty with a Track To constraint as the target, the
camera's lens shift, the viewport's own Lock Camera to View.
"""

import math

import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import GizmoGroup, Menu, Operator
from bpy_extras import view3d_utils
from mathutils import Vector
from mathutils.geometry import intersect_line_plane

# Max's default viewport field of view, 45 degrees, as a Blender viewport lens.
VIEWPORT_LENS = 43.5
VIEWPORT_CLIP_END = 100000.0


def _view_camera(context):
    space = context.space_data
    if space is None or space.type != 'VIEW_3D':
        return None
    rv3d = space.region_3d
    if rv3d is None or rv3d.view_perspective != 'CAMERA':
        return None
    return space.camera or context.scene.camera


class MAXIMIZE_OT_look_through(Operator):
    """Look through this camera"""
    bl_idname = "maximize.look_through"
    bl_label = "Look Through"

    camera: StringProperty(name="Camera")

    @classmethod
    def poll(cls, context):
        return context.space_data is not None and context.space_data.type == 'VIEW_3D'

    def execute(self, context):
        cam = bpy.data.objects.get(self.camera)
        if cam is None or cam.type != 'CAMERA':
            return {'CANCELLED'}
        space = context.space_data
        if space.use_local_camera:
            space.camera = cam
        else:
            context.scene.camera = cam
        if space.region_3d.view_perspective != 'CAMERA':
            bpy.ops.view3d.view_camera()
        return {'FINISHED'}


class MAXIMIZE_OT_select_camera(Operator):
    """Select the camera you are looking through"""
    bl_idname = "maximize.select_camera"
    bl_label = "Select Camera"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and _view_camera(context) is not None

    def execute(self, context):
        cam = _view_camera(context)
        for obj in context.selected_objects:
            obj.select_set(False)
        if cam.hide_select:
            self.report({'WARNING'}, "The camera is frozen")
            return {'CANCELLED'}
        cam.select_set(True)
        context.view_layer.objects.active = cam
        return {'FINISHED'}


def camera_locked(cam):
    return all(cam.lock_location) and all(cam.lock_rotation) and all(cam.lock_scale)


class MAXIMIZE_OT_lock_camera(Operator):
    """Lock Camera: the camera can't be moved, rotated or scaled by accident"""
    bl_idname = "maximize.lock_camera"
    bl_label = "Lock Camera"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (_view_camera(context) or context.scene.camera) is not None

    def execute(self, context):
        cam = _view_camera(context) or context.scene.camera
        state = not camera_locked(cam)
        cam.lock_location = cam.lock_rotation = cam.lock_scale = (state, state, state)
        return {'FINISHED'}


def tilt_correct(cam):
    """Level the camera (no pitch, no roll) and keep the framing through vertical lens shift: Max's
    Camera Correction, 2-point perspective."""
    data = cam.data
    forward = cam.matrix_world.to_3x3() @ Vector((0.0, 0.0, -1.0))
    pitch = math.asin(max(-1.0, min(1.0, forward.z)))
    heading = math.atan2(forward.y, forward.x)
    # Level camera: looking along the heading, up is world Z.
    cam.rotation_mode = 'XYZ'
    cam.rotation_euler = (math.radians(90.0), 0.0, heading - math.radians(90.0))
    if data.type != 'PERSP':
        return 0.0
    sensor = data.sensor_height if data.sensor_fit == 'VERTICAL' else data.sensor_width
    data.shift_y = data.lens * math.tan(pitch) / sensor
    return pitch


class MAXIMIZE_OT_camera_tilt_correction(Operator):
    """Vertical tilt correction: level the camera and keep the framing with lens shift, so vertical
    lines stay vertical (2-point perspective)"""
    bl_idname = "maximize.camera_tilt_correction"
    bl_label = "Camera Correction"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.type == 'CAMERA') or _view_camera(context) is not None

    def execute(self, context):
        obj = context.active_object
        cam = obj if obj is not None and obj.type == 'CAMERA' else _view_camera(context)
        # A tracking constraint would undo the levelling.
        for con in cam.constraints:
            if con.type in {'TRACK_TO', 'DAMPED_TRACK', 'LOCKED_TRACK'} and con.enabled:
                self.report({'WARNING'}, "The camera follows a target; turn its Track To off first")
                return {'CANCELLED'}
        pitch = tilt_correct(cam)
        self.report({'INFO'}, "Levelled a {:.1f}° tilt".format(math.degrees(pitch)))
        return {'FINISHED'}


def make_target_camera(context, position, target):
    """A camera at `position` looking at an empty at `target` (Max's Target camera)."""
    data = bpy.data.cameras.new("Camera")
    data.lens = VIEWPORT_LENS
    cam = bpy.data.objects.new("Camera", data)
    goal = bpy.data.objects.new(cam.name + ".Target", None)
    goal.empty_display_type = 'CUBE'
    goal.empty_display_size = 0.1
    collection = context.collection
    collection.objects.link(cam)
    collection.objects.link(goal)
    cam.location = position
    goal.location = target
    con = cam.constraints.new('TRACK_TO')
    con.target = goal
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    for obj in context.selected_objects:
        obj.select_set(False)
    cam.select_set(True)
    context.view_layer.objects.active = cam
    if context.scene.camera is None:
        context.scene.camera = cam
    return cam, goal


class MAXIMIZE_OT_target_camera(Operator):
    """Target Camera, as in Max: press where the camera goes, drag to the target, release"""
    bl_idname = "maximize.target_camera"
    bl_label = "Target Camera"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.area is not None and context.area.type == 'VIEW_3D'

    def _ground(self, context, event):
        region, rv3d = context.region, context.region_data
        co = (event.mouse_region_x, event.mouse_region_y)
        origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, co)
        direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, co)
        hit = intersect_line_plane(origin, origin + direction, Vector(), Vector((0, 0, 1)))
        return hit if hit is not None else view3d_utils.region_2d_to_location_3d(region, rv3d, co, Vector())

    def invoke(self, context, _event):
        self._start = None
        self._cam = None
        context.window_manager.modal_handler_add(self)
        context.workspace.status_text_set("Target Camera: press at the camera, drag to the target")
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            context.workspace.status_text_set(None)
            return {'CANCELLED'} if self._cam is None else {'FINISHED'}
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self._start is None:
            self._start = self._ground(context, event)
            self._cam, self._goal = make_target_camera(context, self._start, self._start + Vector((0, 1, 0)))
            return {'RUNNING_MODAL'}
        if event.type == 'MOUSEMOVE' and self._cam is not None:
            target = self._ground(context, event)
            if (target - self._start).length > 1e-4:
                self._goal.location = target
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE' and self._cam is not None:
            context.workspace.status_text_set(None)
            return {'FINISHED'}
        return {'PASS_THROUGH'} if self._start is None else {'RUNNING_MODAL'}


class MAXIMIZE_OT_camera_fov(Operator):
    """Field of View: drag left and right to widen or narrow the camera's (or the viewport's) view"""
    bl_idname = "maximize.camera_fov"
    bl_label = "Field of View"
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR', 'BLOCKING'}

    @classmethod
    def poll(cls, context):
        return context.space_data is not None and context.space_data.type == 'VIEW_3D'

    def _target(self, context):
        cam = _view_camera(context)
        return (cam.data, "lens") if cam is not None and cam.data.type == 'PERSP' else (context.space_data, "lens")

    def invoke(self, context, event):
        self._data, self._prop = self._target(context)
        self._start = getattr(self._data, self._prop)
        self._x = event.mouse_x
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            lens = self._start * math.pow(1.01, (event.mouse_x - self._x) * 0.5)
            setattr(self._data, self._prop, max(1.0, min(5000.0, lens)))
            context.area.tag_redraw()
        elif event.type in {'LEFTMOUSE', 'RET'} and event.value == 'RELEASE':
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            setattr(self._data, self._prop, self._start)
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}


def camera_target(cam):
    con = next((c for c in cam.constraints if c.type in {'TRACK_TO', 'DAMPED_TRACK', 'LOCKED_TRACK'} and
                c.target is not None), None) if cam is not None else None
    return con.target if con is not None else None


class MAXIMIZE_OT_camera_dolly(Operator):
    """Max's Dolly Camera / Target / Both: drag up and down to move along the view direction"""
    bl_idname = "maximize.camera_dolly"
    bl_label = "Dolly"
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR', 'BLOCKING'}

    mode: EnumProperty(name="Dolly", items=(('CAMERA', "Camera", ""), ('TARGET', "Target", ""),
                                            ('BOTH', "Camera and Target", "")))

    @classmethod
    def poll(cls, context):
        return _view_camera(context) is not None

    def invoke(self, context, event):
        cam = _view_camera(context)
        self._moving = []
        target = camera_target(cam)
        if self.mode in {'CAMERA', 'BOTH'}:
            self._moving.append(cam)
        if self.mode in {'TARGET', 'BOTH'} and target is not None:
            self._moving.append(target)
        if not self._moving:
            self.report({'WARNING'}, "The camera has no target")
            return {'CANCELLED'}
        self._start = [o.location.copy() for o in self._moving]
        self._dir = (cam.matrix_world.to_3x3() @ Vector((0.0, 0.0, -1.0))).normalized()
        self._y = event.mouse_y
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            step = (event.mouse_y - self._y) * 0.01 * max(1.0, context.scene.unit_settings.scale_length ** -1)
            for obj, start in zip(self._moving, self._start):
                obj.location = start + self._dir * step
            return {'RUNNING_MODAL'}
        if event.type in {'LEFTMOUSE', 'RET'} and event.value == 'RELEASE':
            return {'FINISHED'}
        if event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            for obj, start in zip(self._moving, self._start):
                obj.location = start
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}


# Max's camera navigation buttons, bottom right of a camera view: (operator, props, icon).
_CAMERA_BUTTONS = (
    ("maximize.camera_dolly", {"mode": 'CAMERA'}, 'VIEW_ZOOM'),
    ("maximize.camera_fov", {}, 'VIEW_PERSPECTIVE'),
    ("view3d.move", {}, 'VIEW_PAN'),
    ("view3d.rotate", {}, 'ORIENTATION_GIMBAL'),
    ("view3d.view_roll", {"type": 'ANGLE'}, 'FILE_REFRESH'),
)


class MAXIMIZE_GGT_camera_navigation(GizmoGroup):
    bl_idname = "MAXIMIZE_GGT_camera_navigation"
    bl_label = "Camera Navigation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    @classmethod
    def poll(cls, context):
        return _view_camera(context) is not None and context.space_data.lock_camera

    def setup(self, _context):
        self.buttons = []
        for idname, props, icon in _CAMERA_BUTTONS:
            gz = self.gizmos.new("GIZMO_GT_button_2d")
            gz.icon = icon
            gz.draw_options = {'BACKDROP', 'OUTLINE'}
            gz.color = (0.0, 0.0, 0.0)
            gz.alpha = 0.4
            gz.color_highlight = (0.8, 0.8, 0.8)
            gz.alpha_highlight = 0.2
            gz.scale_basis = 14.0
            op = gz.target_set_operator(idname)
            for key, value in props.items():
                setattr(op, key, value)
            self.buttons.append(gz)

    def draw_prepare(self, context):
        region = context.region
        ui_scale = context.preferences.system.ui_scale
        size = 32.0 * ui_scale
        x = region.width - size * 0.75
        y = size * 0.75
        for gz in reversed(self.buttons):
            gz.matrix_basis[0][3] = x
            gz.matrix_basis[1][3] = y
            x -= size


class MAXIMIZE_MT_point_of_view(Menu):
    """Max's Point-of-View menu"""
    bl_idname = "MAXIMIZE_MT_point_of_view"
    bl_label = "Point of View"

    def draw(self, context):
        layout = self.layout
        space = context.space_data
        cameras = sorted((o for o in context.scene.objects if o.type == 'CAMERA'), key=lambda o: o.name)
        if cameras:
            layout.label(text="Cameras")
            for cam in cameras:
                layout.operator("maximize.look_through", text=cam.name, icon='CAMERA_DATA').camera = cam.name
            layout.separator()
        layout.operator("maximize.view_projection", text="Perspective").projection = 'PERSP'
        layout.operator("maximize.view_projection", text="Orthographic").projection = 'ORTHO'
        layout.separator()
        for view, text in (('TOP', "Top"), ('BOTTOM', "Bottom"), ('FRONT', "Front"), ('BACK', "Back"),
                           ('LEFT', "Left"), ('RIGHT', "Right")):
            layout.operator("view3d.view_axis", text=text).type = view
        layout.separator()
        layout.operator("maximize.select_camera")
        if space is not None and space.type == 'VIEW_3D':
            layout.prop(space, "lock_camera", text="Lock Camera to View")
        cam = _view_camera(context) or context.scene.camera
        if cam is not None:
            layout.operator("maximize.lock_camera", text="Lock Camera",
                            icon='LOCKED' if camera_locked(cam) else 'UNLOCKED')
        layout.separator()
        layout.operator("maximize.target_camera", icon='CAMERA_DATA')
        layout.operator("maximize.camera_fov", icon='VIEW_PERSPECTIVE')
        layout.operator_menu_enum("maximize.camera_dolly", "mode", text="Dolly", icon='VIEW_ZOOM')
        layout.operator("view3d.view_roll", text="Roll", icon='FILE_REFRESH').type = 'ANGLE'
        layout.operator("maximize.camera_tilt_correction")


def apply_viewport_defaults(space):
    """Max's viewport camera defaults for new files: 45 degree field of view, a far clip for
    centimeter scenes, Lock Camera to View on."""
    space.lens = VIEWPORT_LENS
    space.clip_end = max(space.clip_end, VIEWPORT_CLIP_END)
    space.lock_camera = True


def _draw_view_menu(self, _context):
    self.layout.menu("MAXIMIZE_MT_point_of_view")


classes = (
    MAXIMIZE_OT_look_through,
    MAXIMIZE_OT_select_camera,
    MAXIMIZE_OT_lock_camera,
    MAXIMIZE_OT_camera_tilt_correction,
    MAXIMIZE_OT_target_camera,
    MAXIMIZE_OT_camera_fov,
    MAXIMIZE_OT_camera_dolly,
    MAXIMIZE_GGT_camera_navigation,
    MAXIMIZE_MT_point_of_view,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_view_cameras.append(_draw_view_menu)


def unregister():
    bpy.types.VIEW3D_MT_view_cameras.remove(_draw_view_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

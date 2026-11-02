# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Viewport commands with Max behavior, and the Max layout for new files."""

import bpy
from bpy.app.handlers import persistent
from bpy.props import BoolProperty, EnumProperty
from bpy.types import Operator


class MAXIMIZE_OT_view_projection(Operator):
    """Switch the viewport to a perspective (P) or orthographic user view (U)"""
    bl_idname = "maximize.view_projection"
    bl_label = "Perspective / User View"

    projection: EnumProperty(
        items=(('PERSP', "Perspective", ""), ('ORTHO', "Orthographic User", "")),
    )

    @classmethod
    def poll(cls, context):
        return context.region_data is not None

    def execute(self, context):
        context.region_data.view_perspective = self.projection
        return {'FINISHED'}


# The main view's state while another quad view is maximized, per 3D View space.
_saved_main_view = {}

_VIEW_PROPS = ("view_location", "view_rotation", "view_distance", "view_perspective", "view_camera_zoom",
               "view_camera_offset", "is_orthographic_side_view")


def _copy_view(src, dst):
    for prop in _VIEW_PROPS:
        value = getattr(src, prop) if not isinstance(src, dict) else src[prop]
        if hasattr(value, "copy"):
            value = value.copy()
        setattr(dst, prop, value)


class MAXIMIZE_OT_space_key(Operator):
    """Maximize the viewport under the mouse (as Alt+W); elsewhere, or while the animation plays,
    play / stop the animation"""
    bl_idname = "maximize.space_key"
    bl_label = "Maximize Viewport or Play"

    def invoke(self, context, event):
        if context.area is not None and context.area.type == 'VIEW_3D' and not context.screen.is_animation_playing:
            return bpy.ops.maximize.viewport_maximize('INVOKE_DEFAULT')
        return bpy.ops.screen.animation_play()


class MAXIMIZE_OT_viewport_maximize(Operator):
    """Maximize the viewport under the mouse; again to return to the four views (Alt+W)"""
    bl_idname = "maximize.viewport_maximize"
    bl_label = "Maximize Viewport Toggle"

    @classmethod
    def poll(cls, context):
        return context.area is not None and context.area.type == 'VIEW_3D'

    def invoke(self, context, event):
        area = context.area
        space = area.spaces.active
        main = space.region_3d
        key = space.as_pointer()
        main_region = next(r for r in reversed(area.regions) if r.type == 'WINDOW')

        if space.region_quadviews:
            # Which of the four views is under the mouse?
            under = None
            for region in area.regions:
                if region.type == 'WINDOW' and region.x <= event.mouse_x < region.x + region.width and \
                        region.y <= event.mouse_y < region.y + region.height:
                    under = region.data
            if under is None:
                under = context.region_data or main
            picked = None if under == main else {p: _snapshot(getattr(under, p)) for p in _VIEW_PROPS}
            with context.temp_override(region=main_region):
                bpy.ops.screen.region_quadview()
            if picked is not None:
                # The single view keeps the main view's data: show the picked view in it, and
                # remember the main view to restore it when going back to four views.
                _saved_main_view[key] = {p: _snapshot(getattr(main, p)) for p in _VIEW_PROPS}
                _copy_view(picked, space.region_3d)
            return {'FINISHED'}

        with context.temp_override(region=main_region):
            bpy.ops.screen.region_quadview()
        saved = _saved_main_view.pop(key, None)
        if saved is not None:
            _copy_view(saved, space.region_3d)
        return {'FINISHED'}

    def execute(self, _context):
        # Without a mouse position there is no view to pick: plain quad view toggle.
        return bpy.ops.screen.region_quadview()


def _snapshot(value):
    return value.copy() if hasattr(value, "copy") else value


# Fly keys (as in Unreal): along the view, and Q / E down and up along the world's Z.
_FLY_KEYS = {
    'W': (0.0, 0.0, -1.0), 'S': (0.0, 0.0, 1.0), 'A': (-1.0, 0.0, 0.0), 'D': (1.0, 0.0, 0.0),
    'Q': None, 'E': None,
}
_FLY_LOOK = 0.0035  # Radians per pixel at Walk Navigation's mouse sensitivity 1.


class MAXIMIZE_OT_view_fly(Operator):
    """Pan the view; with W A S D (Q E down and up) pressed while the button is held, fly through
    the scene, looking with the mouse. The wheel sets the speed (Walk Navigation's)"""
    bl_idname = "maximize.view_fly"
    bl_label = "Pan / Fly"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.region_data is not None and context.area is not None and context.area.type == 'VIEW_3D'

    def invoke(self, context, event):
        # The pan runs as before (Blender's, with its camera and lock handling) until a fly key is
        # pressed. This operator's handler is added after it, so it sees the keys first.
        bpy.ops.view3d.move('INVOKE_DEFAULT')
        self._button = event.type
        self._held = set()
        self._flying = False
        self._camera = None
        self._timer = None
        self._time = None
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _start(self, context, event):
        import time
        rv3d = context.region_data
        if rv3d.lock_rotation:
            return False
        self._flying = True
        if rv3d.view_perspective == 'CAMERA' and context.scene.camera is not None:
            # As Walk Navigation: through a camera, the camera flies.
            self._camera = context.scene.camera
            self._camera_start = self._camera.matrix_world.copy()
        elif rv3d.view_perspective == 'ORTHO':
            rv3d.view_perspective = 'PERSP'
        self._origin = (event.mouse_x, event.mouse_y)
        self._last = self._origin
        self._time = time.perf_counter()
        self._timer = context.window_manager.event_timer_add(1.0 / 60.0, window=context.window)
        context.window.cursor_modal_set('NONE')
        self._show_speed(context)
        return True

    def _eye(self, context):
        """The viewer's rotation (a 3x3 matrix) and position."""
        from mathutils import Vector
        if self._camera is not None:
            m = self._camera.matrix_world
            return m.to_quaternion().to_matrix(), m.translation.copy()
        rv3d = context.region_data
        rot = rv3d.view_rotation.to_matrix()
        return rot, rv3d.view_location + rot @ Vector((0.0, 0.0, rv3d.view_distance))

    def _set_eye(self, context, rot, eye):
        from mathutils import Matrix, Vector
        if self._camera is not None:
            scale = self._camera.matrix_world.to_scale()
            m = Matrix.Translation(eye) @ rot.to_4x4() @ Matrix.Diagonal(scale.to_4d())
            if self._camera.parent is not None:
                m = self._camera.parent.matrix_world.inverted() @ m
                self._camera.matrix_basis = self._camera.matrix_parent_inverse.inverted() @ m
            else:
                self._camera.matrix_world = m
            return
        rv3d = context.region_data
        rv3d.view_rotation = rot.to_quaternion()
        rv3d.view_location = eye - rot @ Vector((0.0, 0.0, rv3d.view_distance))

    def _look(self, context, dx, dy):
        from mathutils import Matrix, Vector
        walk = context.preferences.inputs.walk_navigation
        k = _FLY_LOOK * walk.mouse_speed
        if walk.use_mouse_reverse:
            dy = -dy
        rot, eye = self._eye(context)
        turned = Matrix.Rotation(-dx * k, 3, 'Z') @ rot
        pitched = turned @ Matrix.Rotation(dy * k, 3, 'X')
        # Not over the top: the view's up stays above the horizon.
        if (pitched @ Vector((0.0, 1.0, 0.0))).z > 0.01:
            turned = pitched
        self._set_eye(context, turned, eye)

    def _move(self, context, event):
        import time
        from mathutils import Vector
        now = time.perf_counter()
        dt, self._time = min(now - self._time, 0.1), now
        rot, eye = self._eye(context)
        step = Vector()
        for key in self._held:
            if key == 'Q':
                step.z -= 1.0
            elif key == 'E':
                step.z += 1.0
            else:
                step += rot @ Vector(_FLY_KEYS[key])
        if step.length == 0.0:
            return
        walk = context.preferences.inputs.walk_navigation
        speed = walk.walk_speed / max(context.scene.unit_settings.scale_length, 1e-6)
        if event.shift:
            speed *= walk.walk_speed_factor
        self._set_eye(context, rot, eye + step.normalized() * speed * dt)

    def _show_speed(self, context):
        if self._flying:
            context.area.header_text_set(
                "Fly: W A S D, Q E down / up, Shift faster, wheel speed {:.2f} m/s".format(
                    context.preferences.inputs.walk_navigation.walk_speed))

    def _finish(self, context, cancel=False):
        if self._timer is not None:
            context.window_manager.event_timer_remove(self._timer)
        if self._flying:
            context.window.cursor_modal_restore()
            context.window.cursor_warp(*self._origin)
            context.area.header_text_set(None)
        if self._camera is not None:
            if cancel:
                self._camera.matrix_world = self._camera_start
            elif not (context.space_data.lock_camera and context.mode in {'OBJECT', 'POSE'}):
                # One undo step for the camera's new place (with Camera to View on, the pan
                # underneath makes it).
                return {'FINISHED', 'PASS_THROUGH'}
        return {'CANCELLED', 'PASS_THROUGH'}

    def modal(self, context, event):
        if event.type == self._button and event.value == 'RELEASE':
            # The pan underneath ends on the same release.
            return self._finish(context)
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            # The pan cancels too, putting the view back as it was.
            return self._finish(context, cancel=True)
        if event.type in _FLY_KEYS:
            if event.value == 'PRESS':
                if not self._flying and not self._start(context, event):
                    return {'RUNNING_MODAL'}
                self._held.add(event.type)
            elif event.value == 'RELEASE':
                self._held.discard(event.type)
            return {'RUNNING_MODAL'}
        if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            walk = context.preferences.inputs.walk_navigation
            walk.walk_speed = min(max(walk.walk_speed * (1.25 if event.type == 'WHEELUPMOUSE' else 0.8), 0.01), 100.0)
            context.preferences.is_dirty = True
            self._show_speed(context)
            return {'RUNNING_MODAL'}
        if not self._flying:
            return {'PASS_THROUGH'}
        if event.type == 'MOUSEMOVE':
            dx, dy = event.mouse_x - self._last[0], event.mouse_y - self._last[1]
            self._last = (event.mouse_x, event.mouse_y)
            if dx or dy:
                self._look(context, dx, dy)
                # Keep the hidden cursor near where it started, so the look never runs out of screen.
                if abs(event.mouse_x - self._origin[0]) + abs(event.mouse_y - self._origin[1]) > 100:
                    context.window.cursor_warp(*self._origin)
                    self._last = self._origin
            return {'RUNNING_MODAL'}
        if event.type == 'TIMER':
            self._move(context, event)
            return {'RUNNING_MODAL'}
        return {'RUNNING_MODAL'}


class MAXIMIZE_OT_camera_from_view(Operator):
    """Create a camera that matches the current view and look through it (Ctrl+C)"""
    bl_idname = "maximize.camera_from_view"
    bl_label = "Create Camera From View"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.region_data is not None and context.mode == 'OBJECT'

    def execute(self, context):
        rv3d = context.region_data
        if rv3d.view_perspective == 'CAMERA':
            rv3d.view_perspective = 'PERSP'
        bpy.ops.object.camera_add()
        camera = context.active_object
        context.scene.camera = camera
        bpy.ops.view3d.camera_to_view()
        return {'FINISHED'}


def _open_editor_window(context, ui_type, setup=None):
    """Open a new window showing one editor, like Max's floating dialogs."""
    windows = set(context.window_manager.windows)
    bpy.ops.wm.window_new()
    new = [w for w in context.window_manager.windows if w not in windows]
    if not new:
        return False
    area = new[0].screen.areas[0]
    area.ui_type = ui_type
    if setup:
        setup(area.spaces.active)
    return True


class MAXIMIZE_OT_open_editor(Operator):
    """Open an editor in its own window"""
    bl_idname = "maximize.open_editor"
    bl_label = "Open Editor"

    ui_type: bpy.props.StringProperty(name="Editor", default='PROPERTIES')

    def execute(self, context):
        try:
            opened = _open_editor_window(context, self.ui_type)
        except TypeError:
            self.report({'ERROR'}, "Unknown editor: " + self.ui_type)
            return {'CANCELLED'}
        return {'FINISHED'} if opened else {'CANCELLED'}


class MAXIMIZE_OT_material_editor(Operator):
    """Open the material editor in its own window (M)"""
    bl_idname = "maximize.material_editor"
    bl_label = "Material Editor"

    def execute(self, context):
        return {'FINISHED'} if _open_editor_window(context, 'ShaderNodeTree') else {'CANCELLED'}


class MAXIMIZE_OT_render_setup(Operator):
    """Open the render settings in their own window (F10)"""
    bl_idname = "maximize.render_setup"
    bl_label = "Render Setup"

    def execute(self, context):
        def setup(space):
            space.context = 'RENDER'
        return {'FINISHED'} if _open_editor_window(context, 'PROPERTIES', setup) else {'CANCELLED'}


class MAXIMIZE_OT_angle_snap(Operator):
    """Toggle angle snap: rotations snap to the angle increment, moves stay free (A)"""
    bl_idname = "maximize.angle_snap"
    bl_label = "Angle Snap Toggle"

    def execute(self, context):
        ts = context.scene.tool_settings
        scene = context.scene
        if scene.get("maximize_angle_snap"):
            saved = scene["maximize_angle_snap"]
            ts.use_snap = bool(saved.get("use_snap", False))
            ts.use_snap_translate = bool(saved.get("translate", True))
            ts.use_snap_scale = bool(saved.get("scale", True))
            ts.use_snap_rotate = bool(saved.get("rotate", True))
            del scene["maximize_angle_snap"]
            self.report({'INFO'}, "Angle Snap: Off")
        else:
            scene["maximize_angle_snap"] = {
                "use_snap": ts.use_snap,
                "translate": ts.use_snap_translate,
                "scale": ts.use_snap_scale,
                "rotate": ts.use_snap_rotate,
            }
            if not ts.use_snap:
                # Snap only rotations, like Max's separate angle snap.
                ts.use_snap_translate = False
                ts.use_snap_scale = False
            ts.use_snap = True
            ts.use_snap_rotate = True
            self.report({'INFO'}, "Angle Snap: On ({:.0f}°)".format(
                ts.snap_angle_increment_3d * 57.29578))
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Max layout for new files

def _apply_layout():
    from .preferences import get_prefs
    prefs = get_prefs()
    if prefs is None or not prefs.use_startup_layout:
        return None
    scene = bpy.context.scene
    if scene is None or scene.get("maximize_layout"):
        return None

    units = scene.unit_settings
    units.system = 'METRIC'
    units.length_unit = 'CENTIMETERS'
    # Moritz has the Command Panel and no Max sidebar tab.
    moritz = hasattr(bpy.types, "PROPERTIES_PT_create")

    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            space = area.spaces.active
            if not moritz:
                space.show_region_ui = True
            from .cameras import apply_viewport_defaults
            apply_viewport_defaults(space)
            region = next((r for r in area.regions if r.type == 'WINDOW'), None)
            if region is None:
                continue
            # Only the main viewport of the Layout workspace becomes a quad view.
            if area.width > 500 and not space.region_quadviews:
                with bpy.context.temp_override(window=window, area=area, region=region):
                    bpy.ops.screen.region_quadview()
    scene["maximize_layout"] = True
    # The sidebar tabs only exist once the sidebar has been drawn.
    if not moritz:
        bpy.app.timers.register(_select_max_tab, first_interval=0.5)
    return None


def _select_max_tab():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            for region in area.regions:
                if region.type == 'UI':
                    try:
                        region.active_panel_category = "Max"
                    except (AttributeError, TypeError, ValueError):
                        pass
                    area.tag_redraw()
    return None


# ------------------------------------------------------------------------------
# Viewport undo / redo (Shift+Z, Shift+Y): a short history of view changes per viewport.

_HISTORY_SIZE = 50
_view_history = {}  # region_3d pointer -> {"states": [...], "index": int, "restoring": bool}
# Max's active viewport, as far as Python can tell: the one whose view changed last.
_active_view = None  # region_3d pointer


def active_view_region(window):
    """(area, region) of the active viewport in `window`: the one changed last, else None."""
    if _active_view is None or window is None:
        return None
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW' and region.data is not None and                         region.data.as_pointer() == _active_view:
                    return area, region
    return None


def _view_state(rv3d):
    return (tuple(rv3d.view_location), tuple(rv3d.view_rotation), rv3d.view_distance,
            rv3d.view_perspective, rv3d.is_perspective)


def _set_view_state(rv3d, state):
    location, rotation, distance, perspective, is_perspective = state
    rv3d.view_location = location
    rv3d.view_rotation = rotation
    rv3d.view_distance = distance
    rv3d.view_perspective = perspective
    rv3d.is_perspective = is_perspective


def _track_views():
    global _active_view
    try:
        windows = bpy.context.window_manager.windows
    except AttributeError:
        return 0.3
    for window in windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            for region in area.regions:
                rv3d = region.data if region.type == 'WINDOW' else None
                if rv3d is None:
                    continue
                state = _view_state(rv3d)
                entry = _view_history.setdefault(rv3d.as_pointer(), {"states": [state], "index": 0})
                if entry["states"][entry["index"]] != state:
                    _active_view = rv3d.as_pointer()
                    del entry["states"][entry["index"] + 1:]
                    entry["states"].append(state)
                    del entry["states"][:-_HISTORY_SIZE]
                    entry["index"] = len(entry["states"]) - 1
    return 0.3


class MAXIMIZE_OT_view_history(Operator):
    """Undo or redo a view change in this viewport (Shift+Z, Shift+Y)"""
    bl_idname = "maximize.view_history"
    bl_label = "Undo View Change"

    redo: BoolProperty(name="Redo")

    @classmethod
    def poll(cls, context):
        return context.region_data is not None

    def execute(self, context):
        rv3d = context.region_data
        _track_views()
        entry = _view_history.get(rv3d.as_pointer())
        if entry is None:
            return {'CANCELLED'}
        index = entry["index"] + (1 if self.redo else -1)
        if not 0 <= index < len(entry["states"]):
            return {'CANCELLED'}
        entry["index"] = index
        _set_view_state(rv3d, entry["states"][index])
        context.area.tag_redraw()
        return {'FINISHED'}


@persistent
def _load_post(_filepath):
    if not bpy.data.filepath:
        # Wait until the window and its areas exist.
        bpy.app.timers.register(_apply_layout, first_interval=0.05)


classes = (
    MAXIMIZE_OT_view_projection,
    MAXIMIZE_OT_space_key,
    MAXIMIZE_OT_viewport_maximize,
    MAXIMIZE_OT_view_fly,
    MAXIMIZE_OT_camera_from_view,
    MAXIMIZE_OT_open_editor,
    MAXIMIZE_OT_material_editor,
    MAXIMIZE_OT_render_setup,
    MAXIMIZE_OT_angle_snap,
    MAXIMIZE_OT_view_history,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.handlers.load_post.append(_load_post)
    bpy.app.timers.register(_track_views, first_interval=1.0, persistent=True)


def unregister():
    if bpy.app.timers.is_registered(_track_views):
        bpy.app.timers.unregister(_track_views)
    _view_history.clear()
    if _load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_load_post)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

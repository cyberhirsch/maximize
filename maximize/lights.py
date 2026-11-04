# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Area lights created like V-Ray's Plane, Disc and Sphere lights: drag them out in a viewport.

They are Blender's own lights (Plane and Disc: area lights; Sphere: a point light with a radius),
so files stay readable in any Blender. The drag works like Max's primitives: on the construction
grid, or with AutoGrid on the surface under the mouse, shining away from it. Drawn in a top or
perspective view they shine down, as V-Ray's Plane light does.
"""

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator
from bpy_extras import view3d_utils
from mathutils import Matrix, Vector
from mathutils.geometry import intersect_line_plane

from . import primitives, tool_state

# (identifier, label, description, icon)
SHAPES = (
    ('PLANE', "Plane Light", "A rectangle: drag its width and length", 'LIGHT_AREA'),
    ('DISC', "Disc Light", "A disc: drag its radius", 'MESH_CIRCLE'),
    ('SPHERE', "Sphere Light", "A sphere: drag its radius", 'LIGHT_POINT'),
)
_LABELS = {s[0]: s[1] for s in SHAPES}
POWER = 100.0  # Watts: brighter than Blender's 10 W, which hardly lights a room.
_TARGET = "Target"  # Name of the Track To constraint of a targeted light.


def create_light(context, shape, matrix):
    name = primitives._max_name(_LABELS[shape].replace(" ", ""))
    if shape == 'SPHERE':
        data = bpy.data.lights.new(name, 'POINT')
        data.shadow_soft_size = 0.0
    else:
        data = bpy.data.lights.new(name, 'AREA')
        data.shape = 'RECTANGLE' if shape == 'PLANE' else 'DISK'
        data.size = data.size_y = 0.0
    data.energy = POWER
    obj = bpy.data.objects.new(name, data)
    context.collection.objects.link(obj)
    obj.matrix_world = matrix
    for other in context.selected_objects:
        other.select_set(False)
    obj.select_set(True)
    context.view_layer.objects.active = obj
    # The Create tab shows its Parameters.
    context.window_manager.maximize_created = obj.name
    return obj


def light_shape(obj):
    """'PLANE', 'DISC' or 'SPHERE' for a light these tools work with, else None."""
    if obj is None or obj.type != 'LIGHT':
        return None
    data = obj.data
    if data.type == 'POINT':
        return 'SPHERE'
    if data.type == 'AREA':
        return 'PLANE' if data.shape in {'RECTANGLE', 'SQUARE'} else 'DISC'
    return None


def target(obj):
    con = obj.constraints.get(_TARGET)
    return con.target if con is not None and con.type == 'TRACK_TO' else None


class MAXIMIZE_OT_add_light(Operator):
    """Create a light by dragging in a viewport, as V-Ray's Plane, Disc and Sphere lights. A Plane or
    Disc drawn on the ground shines down; with AutoGrid it shines away from the surface"""
    bl_idname = "maximize.add_light"
    bl_label = "Add Light"
    bl_options = {'REGISTER', 'UNDO'}

    shape: EnumProperty(name="Shape", items=[s[:3] for s in SHAPES])

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        """Without a mouse (scripts, redo): a 1 m light at the 3D cursor."""
        obj = create_light(context, self.shape, context.scene.cursor.matrix)
        if self.shape == 'SPHERE':
            obj.data.shadow_soft_size = 0.5
        else:
            obj.data.size = obj.data.size_y = 1.0
        return {'FINISHED'}

    def invoke(self, context, _event):
        if context.area is None or context.area.type != 'VIEW_3D':
            return self.execute(context)
        self._obj = None
        self._region = None
        self._created = 0
        context.window_manager.modal_handler_add(self)
        tool_state.begin(context)
        self._status(context)
        return {'RUNNING_MODAL'}

    def _status(self, context):
        what = "drag the rectangle" if self.shape == 'PLANE' else "drag the radius"
        context.workspace.status_text_set("Create {:s}: {:s} in a viewport (right-click or Esc to stop)".format(
            _LABELS[self.shape], what))

    def _mouse(self, event):
        return (event.mouse_x - self._region.x, event.mouse_y - self._region.y)

    def _hit(self, event):
        rv3d = self._region.data
        co = self._mouse(event)
        origin = view3d_utils.region_2d_to_origin_3d(self._region, rv3d, co)
        direction = view3d_utils.region_2d_to_vector_3d(self._region, rv3d, co)
        return intersect_line_plane(origin, origin + direction, self._origin, self._n)

    def _begin(self, context, event):
        self._region = primitives.MAXIMIZE_OT_add_primitive._region_at(self, context, event)
        if self._region is None:
            return False
        u, v, n = primitives._grid_plane(self._region.data)
        self._origin = Vector()
        surface = primitives.autogrid_hit(context, self._region, self._mouse(event))
        if surface is not None:
            self._origin, u, v, n = surface
        self._u, self._v, self._n = u, v, n
        hit = self._hit(event)
        if hit is None:
            return False
        self._p0 = hit
        if surface is not None:
            # Area lights shine along their -Z: away from the surface. (v, u, -n) stays right-handed.
            basis = Matrix((v, u, -n)).transposed().to_4x4()
        else:
            # On the grid they shine into it: down from a top or perspective view, as V-Ray's lights.
            basis = Matrix((u, v, n)).transposed().to_4x4()
        self._obj = create_light(context, self.shape, Matrix.Translation(hit) @ basis)
        return True

    def _apply(self, event):
        hit = self._hit(event)
        if hit is None:
            return
        d = hit - self._p0
        data = self._obj.data
        if self.shape == 'PLANE':
            du, dv = d.dot(self._u), d.dot(self._v)
            data.size, data.size_y = abs(du), abs(dv)
            self._obj.matrix_world.translation = self._p0 + self._u * (du / 2) + self._v * (dv / 2)
        elif self.shape == 'DISC':
            data.size = data.size_y = 2.0 * d.length
        else:
            data.shadow_soft_size = d.length
        for area in bpy.context.window.screen.areas:
            if area.type == 'PROPERTIES':
                area.tag_redraw()

    def _size(self):
        data = self._obj.data
        return data.shadow_soft_size if self.shape == 'SPHERE' else min(data.size, data.size_y)

    def _end(self, context):
        context.workspace.status_text_set(None)
        tool_state.end(context)
        return {'FINISHED'} if self._created else {'CANCELLED'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            if self._obj is not None:
                bpy.data.objects.remove(self._obj)
                self._obj = None
            return self._end(context)
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'WHEELINMOUSE', 'WHEELOUTMOUSE',
                          'TRACKPADPAN', 'TRACKPADZOOM'}:
            return {'PASS_THROUGH'}
        if event.type == 'MOUSEMOVE' and self._obj is not None:
            self._apply(event)
        elif event.type == 'LEFTMOUSE':
            if event.value == 'PRESS' and self._obj is None:
                if primitives.MAXIMIZE_OT_add_primitive._region_at(self, context, event) is None:
                    # Clicking outside the viewport ends create mode.
                    return self._end(context)
                self._begin(context, event)
            elif event.value == 'RELEASE' and self._obj is not None:
                self._apply(event)
                if self._size() < 1e-6:
                    # A click without a drag creates nothing.
                    bpy.data.objects.remove(self._obj)
                else:
                    self._created += 1
                self._obj = None
        return {'RUNNING_MODAL'}


class MAXIMIZE_OT_light_target(Operator):
    """Targeted: the light aims at a target you can move (a Track To constraint on a target empty).
    Again to remove the target"""
    bl_idname = "maximize.light_target"
    bl_label = "Targeted"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return light_shape(context.active_object) is not None

    def execute(self, context):
        obj = context.active_object
        con = obj.constraints.get(_TARGET)
        if con is not None:
            empty = con.target
            obj.constraints.remove(con)
            if empty is not None and empty.users_collection and not empty.children:
                bpy.data.objects.remove(empty)
            return {'FINISHED'}
        empty = bpy.data.objects.new(obj.name + ".Target", None)
        empty.empty_display_type = 'CUBE'
        empty.empty_display_size = 0.1
        for coll in obj.users_collection:
            coll.objects.link(empty)
        # In front of the light, where it shines (its -Z), one meter away.
        empty.location = obj.matrix_world @ Vector((0.0, 0.0, -1.0 / obj.matrix_world.to_scale().z))
        con = obj.constraints.new('TRACK_TO')
        con.name = _TARGET
        con.target = empty
        con.track_axis = 'TRACK_NEGATIVE_Z'
        con.up_axis = 'UP_Y'
        return {'FINISHED'}


def draw_parameters(layout, obj):
    """The light's parameters, as V-Ray's light rollout: shape and size, intensity, color, options."""
    data = obj.data
    shape = light_shape(obj)
    col = layout.column()
    col.use_property_split = True
    col.use_property_decorate = False
    if shape == 'PLANE':
        col.prop(data, "size", text="Width")
        col.prop(data, "size_y", text="Length")
    elif shape == 'DISC':
        col.prop(data, "size", text="Diameter")
    else:
        col.prop(data, "shadow_soft_size", text="Radius")
    col.separator()
    col.prop(data, "energy", text="Power")
    col.prop(data, "exposure", text="Exposure")
    if shape != 'SPHERE':
        col.prop(data, "normalize", text="Normalize")
    col.separator()
    col.prop(data, "use_temperature", text="Temperature")
    if data.use_temperature:
        col.prop(data, "temperature", text="Kelvin")
    else:
        col.prop(data, "color", text="Color")
    col.separator()
    col.prop(obj, "visible_camera", text="Visible to Camera")
    if shape != 'SPHERE':
        col.prop(data, "spread", text="Spread (Directional)")
    col.prop(data, "diffuse_factor", text="Affect Diffuse")
    col.prop(data, "specular_factor", text="Affect Specular")
    col.prop(data, "use_shadow", text="Cast Shadows")
    row = col.row()
    row.operator("maximize.light_target", text="Targeted", icon='CON_TRACKTO', depress=target(obj) is not None)


classes = (
    MAXIMIZE_OT_add_light,
    MAXIMIZE_OT_light_target,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

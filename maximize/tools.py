# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max object tools: Array and Spacing Tool."""

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty
from bpy.types import Operator
from mathutils import Euler, Matrix, Vector

from .transform import CLONE_TYPES


def _new_clone(obj, clone_type, matrix):
    new = obj.copy()
    if obj.data is not None and clone_type == 'COPY':
        new.data = obj.data.copy()
    for coll in obj.users_collection:
        coll.objects.link(new)
    new.matrix_world = matrix
    return new


# ------------------------------------------------------------------------------
# Array

class MAXIMIZE_OT_array(Operator):
    """Array: clone the selection in 1D, 2D or 3D with incremental move, rotate and scale"""
    bl_idname = "maximize.array"
    bl_label = "Array"
    bl_options = {'REGISTER', 'UNDO'}

    move: FloatVectorProperty(name="Move", subtype='TRANSLATION', default=(1.0, 0.0, 0.0))
    rotate: FloatVectorProperty(name="Rotate", subtype='EULER')
    scale: FloatVectorProperty(name="Scale", default=(100.0, 100.0, 100.0), subtype='XYZ',
                               description="Scale in percent")
    use_totals: BoolProperty(
        name="Totals",
        description="The values above are totals over the whole array, not per copy",
    )
    dimension: EnumProperty(
        name="Array Dimensions",
        items=(('1D', "1D", ""), ('2D', "2D", ""), ('3D', "3D", "")),
    )
    count_1d: IntProperty(name="Count", default=10, min=1, max=10000)
    count_2d: IntProperty(name="Count", default=1, min=1, max=10000)
    offset_2d: FloatVectorProperty(name="Incremental Row Offset", subtype='TRANSLATION', default=(0.0, 1.0, 0.0))
    count_3d: IntProperty(name="Count", default=1, min=1, max=10000)
    offset_3d: FloatVectorProperty(name="Incremental Row Offset", subtype='TRANSLATION', default=(0.0, 0.0, 1.0))
    clone_type: EnumProperty(name="Type of Object", items=CLONE_TYPES)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects)

    def invoke(self, context, _event):
        return context.window_manager.invoke_props_dialog(self, width=520)

    def draw(self, _context):
        layout = self.layout
        box = layout.box()
        box.label(text="Array Transformation: World Coordinates")
        grid = box.grid_flow(columns=3, even_columns=True, align=True)
        for prop in ("move", "rotate", "scale"):
            col = grid.column(align=True)
            col.label(text=self.bl_rna.properties[prop].name + (" (%)" if prop == "scale" else ""))
            col.prop(self, prop, text="")
        box.prop(self, "use_totals")
        box = layout.box()
        box.label(text="Array Dimensions")
        box.row().prop(self, "dimension", expand=True)
        box.prop(self, "count_1d", text="1D Count")
        if self.dimension in {'2D', '3D'}:
            row = box.row()
            row.prop(self, "count_2d", text="2D Count")
            row.prop(self, "offset_2d", text="")
        if self.dimension == '3D':
            row = box.row()
            row.prop(self, "count_3d", text="3D Count")
            row.prop(self, "offset_3d", text="")
        total = self.count_1d * (self.count_2d if self.dimension != '1D' else 1) * (
            self.count_3d if self.dimension == '3D' else 1)
        box.label(text="Total in Array: {:d}".format(total))
        layout.row().prop(self, "clone_type", expand=True)

    def _per_copy(self):
        steps = max(self.count_1d - 1, 1) if self.use_totals else 1
        move = Vector(self.move) / steps
        rotate = Vector(self.rotate) / steps
        scale = Vector((s / 100.0) ** (1.0 / steps) if s > 0 else 1.0 for s in self.scale)
        return move, rotate, scale

    def execute(self, context):
        move, rotate, scale = self._per_copy()
        n2 = self.count_2d if self.dimension in {'2D', '3D'} else 1
        n3 = self.count_3d if self.dimension == '3D' else 1
        created = []
        for obj in list(context.selected_objects):
            base = obj.matrix_world.copy()
            pivot = base.translation.copy()
            for k in range(n3):
                for j in range(n2):
                    for i in range(self.count_1d):
                        if i == j == k == 0:
                            continue
                        rot = Euler(rotate * i).to_matrix().to_4x4()
                        scl = Matrix.Diagonal([s ** i for s in scale] + [1.0])
                        offset = move * i + Vector(self.offset_2d) * j + Vector(self.offset_3d) * k
                        matrix = (Matrix.Translation(pivot + offset) @ rot @ scl @
                                  Matrix.Translation(-pivot) @ base)
                        created.append(_new_clone(obj, self.clone_type, matrix))
        self.report({'INFO'}, "Array: {:d} new objects".format(len(created)))
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Spacing Tool

def _curve_polyline(curve_obj, depsgraph):
    """World-space points along the curve, in order, and whether it is closed."""
    eval_obj = curve_obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    try:
        points = [curve_obj.matrix_world @ v.co for v in mesh.vertices]
        neighbors = {i: [] for i in range(len(points))}
        for edge in mesh.edges:
            a, b = edge.vertices
            neighbors[a].append(b)
            neighbors[b].append(a)
    finally:
        eval_obj.to_mesh_clear()
    if len(points) < 2:
        return [], False
    start = next((i for i, n in neighbors.items() if len(n) == 1), 0)
    closed = all(len(n) == 2 for n in neighbors.values())
    order, prev, cur = [start], None, start
    while True:
        nxt = next((n for n in neighbors[cur] if n != prev), None)
        if nxt is None or nxt == start:
            break
        order.append(nxt)
        prev, cur = cur, nxt
        if len(order) > len(points):
            break
    path = [points[i] for i in order]
    if closed:
        path.append(path[0])
    return path, closed


def _sample(path, distance):
    """Point and tangent at a distance along the polyline."""
    walked = 0.0
    for a, b in zip(path, path[1:]):
        seg = (b - a).length
        if seg > 0.0 and walked + seg >= distance:
            t = (distance - walked) / seg
            return a.lerp(b, t), (b - a).normalized()
        walked += seg
    a, b = path[-2], path[-1]
    return b.copy(), (b - a).normalized() if (b - a).length > 0 else Vector((1, 0, 0))


class MAXIMIZE_OT_spacing(Operator):
    """Spacing Tool: distribute clones of the selected object along the active curve"""
    bl_idname = "maximize.spacing"
    bl_label = "Spacing Tool"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(
        name="Parameters",
        items=(('COUNT', "Count", "Fixed number of objects, evenly spaced"),
               ('SPACING', "Spacing", "Fixed distance between objects")),
    )
    count: IntProperty(name="Count", default=10, min=1, max=10000)
    spacing: FloatProperty(name="Spacing", default=1.0, min=0.0001, subtype='DISTANCE')
    follow: BoolProperty(name="Follow", description="Align the clones' X axis to the path", default=False)
    clone_type: EnumProperty(name="Type of Object", items=CLONE_TYPES, default='INSTANCE')

    @classmethod
    def poll(cls, context):
        active = context.active_object
        return (context.mode == 'OBJECT' and active is not None and active.type == 'CURVE' and
                any(o != active for o in context.selected_objects))

    def invoke(self, context, _event):
        return context.window_manager.invoke_props_dialog(self, width=320)

    def draw(self, _context):
        layout = self.layout
        layout.row().prop(self, "mode", expand=True)
        layout.prop(self, "count" if self.mode == 'COUNT' else "spacing")
        layout.prop(self, "follow")
        layout.row().prop(self, "clone_type", expand=True)

    def execute(self, context):
        curve = context.active_object
        sources = [o for o in context.selected_objects if o != curve]
        path, closed = _curve_polyline(curve, context.evaluated_depsgraph_get())
        if len(path) < 2:
            self.report({'ERROR'}, "The path has no length")
            return {'CANCELLED'}
        length = sum((b - a).length for a, b in zip(path, path[1:]))
        if self.mode == 'COUNT':
            count = self.count
            step = length / (count if closed else max(count - 1, 1))
        else:
            step = self.spacing
            count = int(length / step) + (0 if closed else 1)
        source = sources[0]
        base = source.matrix_world
        loc0, rot0, scale0 = base.decompose()
        for i in range(count):
            point, tangent = _sample(path, min(i * step, length))
            rot = tangent.to_track_quat('X', 'Z') @ rot0 if self.follow else rot0
            _new_clone(source, self.clone_type, Matrix.LocRotScale(point, rot, scale0))
        self.report({'INFO'}, "Spacing Tool: {:d} objects along {:s}".format(count, curve.name))
        return {'FINISHED'}


class MAXIMIZE_OT_show_end_result(Operator):
    """Show End Result (Alt+`): toggle whether the modifier stack shows while editing sub-objects"""
    bl_idname = "maximize.show_end_result"
    bl_label = "Show End Result"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and len(obj.modifiers) > 0

    def execute(self, context):
        mods = context.active_object.modifiers
        on = not all(m.show_in_editmode for m in mods)
        for m in mods:
            m.show_in_editmode = on
            if not on:
                m.show_on_cage = False
        self.report({'INFO'}, "Show End Result: " + ("On" if on else "Off"))
        return {'FINISHED'}


classes = (
    MAXIMIZE_OT_show_end_result,
    MAXIMIZE_OT_array,
    MAXIMIZE_OT_spacing,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

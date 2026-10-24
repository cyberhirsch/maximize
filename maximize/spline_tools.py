# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Editable Spline tools Max has and Blender lacks: Fillet, Chamfer and Outline in curve Edit Mode,
Loft and 2D shape booleans on objects. Blender's own curve tools (handle types, extrude and bevel,
Screw for Lathe, the Pen tool for Refine) stay as they are.

Shapes are treated as lying in their object's local XY plane, as Max's shapes do.
"""

import math

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.types import Operator
from mathutils import Vector

from .nodes import GroupBuilder, find_group, modifier_input


# ------------------------------------------------------------------------------
# Reading and rebuilding splines


class _Point:
    __slots__ = ("co", "left", "right", "left_type", "right_type", "radius", "tilt", "select")

    def __init__(self, co, left=None, right=None, left_type='VECTOR', right_type='VECTOR',
                 radius=1.0, tilt=0.0, select=False):
        self.co = Vector(co)
        self.left = Vector(left) if left is not None else self.co.copy()
        self.right = Vector(right) if right is not None else self.co.copy()
        self.left_type, self.right_type = left_type, right_type
        self.radius, self.tilt, self.select = radius, tilt, select


def _read(spline):
    if spline.type == 'BEZIER':
        return [_Point(p.co, p.handle_left, p.handle_right, p.handle_left_type, p.handle_right_type,
                       p.radius, p.tilt, p.select_control_point) for p in spline.bezier_points]
    return [_Point(p.co.xyz, radius=p.radius, tilt=p.tilt, select=p.select) for p in spline.points]


def _write(curve, spline, points, cyclic=None):
    """A Bezier spline through `points`, replacing `spline` (when given); returns the new spline."""
    new = curve.splines.new('BEZIER')
    new.bezier_points.add(len(points) - 1)
    for bp, p in zip(new.bezier_points, points):
        bp.co = p.co
        bp.handle_left_type = 'FREE'
        bp.handle_right_type = 'FREE'
        bp.handle_left = p.left
        bp.handle_right = p.right
        bp.handle_left_type = p.left_type
        bp.handle_right_type = p.right_type
        bp.radius, bp.tilt = p.radius, p.tilt
        bp.select_control_point = p.select
        bp.select_left_handle = bp.select_right_handle = p.select
    new.use_cyclic_u = spline.use_cyclic_u if cyclic is None else cyclic
    if spline is not None:
        new.resolution_u = spline.resolution_u
        new.material_index = spline.material_index
        new.use_smooth = spline.use_smooth
        curve.splines.remove(spline)
    return new


def _edit_curves(context):
    for obj in context.objects_in_mode_unique_data:
        if obj.type == 'CURVE':
            yield obj


def _with_object_mode(context, fn):
    """Spline edits through the data API need Object Mode; come back to Edit Mode after.
    `fn(objects)` gets the curve objects that were in Edit Mode."""
    objects = list(_edit_curves(context))
    bpy.ops.object.mode_set(mode='OBJECT')
    try:
        return fn(objects)
    finally:
        bpy.ops.object.mode_set(mode='EDIT')


# ------------------------------------------------------------------------------
# Fillet and Chamfer


def _round_corner(points, i, amount, chamfer):
    n = len(points)
    p = points[i]
    a = points[i - 1].co
    b = points[(i + 1) % n].co
    u, v = a - p.co, b - p.co
    if u.length < 1e-9 or v.length < 1e-9:
        return [p]
    angle = u.angle(v)
    if angle < 1e-4 or angle > math.pi - 1e-4:
        return [p]
    if chamfer:
        d = amount
    else:
        d = amount / math.tan(angle / 2.0)
    d = min(d, u.length * 0.5, v.length * 0.5)
    u, v = u.normalized(), v.normalized()
    p1, p2 = p.co + u * d, p.co + v * d
    if chamfer:
        return [_Point(p1, select=True, radius=p.radius, tilt=p.tilt),
                _Point(p2, select=True, radius=p.radius, tilt=p.tilt)]
    # A circular arc as one Bezier segment: handle length 4/3 * tan(sweep / 4) * radius.
    radius = d * math.tan(angle / 2.0)
    sweep = math.pi - angle
    k = 4.0 / 3.0 * math.tan(sweep / 4.0) * radius
    first = _Point(p1, p1 + u * k, p1 - u * k, 'ALIGNED', 'ALIGNED', p.radius, p.tilt, True)
    second = _Point(p2, p2 - v * k, p2 + v * k, 'ALIGNED', 'ALIGNED', p.radius, p.tilt, True)
    return [first, second]


def _fillet_spline(points, cyclic, amount, chamfer):
    out = []
    n = len(points)
    for i, p in enumerate(points):
        inner = cyclic or 0 < i < n - 1
        if p.select and inner and n >= 3:
            out += _round_corner(points, i, amount, chamfer)
        else:
            out.append(p)
    return out


class _CornerOperator:
    bl_options = {'REGISTER', 'UNDO'}
    chamfer = False

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        amount = self.radius if not self.chamfer else self.distance

        def run(objects):
            changed = 0
            for obj in objects:
                curve = obj.data
                for spline in list(curve.splines):
                    points = _read(spline)
                    if not any(p.select for p in points):
                        continue
                    _write(curve, spline, _fillet_spline(points, spline.use_cyclic_u, amount, self.chamfer))
                    changed += 1
            return changed

        if not _with_object_mode(context, run):
            self.report({'WARNING'}, "Select corner vertices first")
            return {'CANCELLED'}
        return {'FINISHED'}


class MAXIMIZE_OT_spline_fillet(_CornerOperator, Operator):
    """Fillet: round the selected spline vertices with an arc of the given radius"""
    bl_idname = "maximize.spline_fillet"
    bl_label = "Fillet"

    radius: FloatProperty(name="Radius", default=0.1, min=0.0, subtype='DISTANCE')


class MAXIMIZE_OT_spline_chamfer(_CornerOperator, Operator):
    """Chamfer: cut the selected spline vertices off with a straight segment"""
    bl_idname = "maximize.spline_chamfer"
    bl_label = "Chamfer (Spline)"
    chamfer = True

    distance: FloatProperty(name="Distance", default=0.1, min=0.0, subtype='DISTANCE')


# ------------------------------------------------------------------------------
# Outline


def _offsets(points, cyclic, distance):
    """Per-point offset vectors in the XY plane (mitered, limited at sharp corners)."""
    n = len(points)
    z = Vector((0, 0, 1))
    result = []
    for i, p in enumerate(points):
        prev_ = points[i - 1].co if (cyclic or i > 0) else None
        next_ = points[(i + 1) % n].co if (cyclic or i < n - 1) else None
        dirs = []
        if prev_ is not None:
            dirs.append((p.co - prev_).to_2d().to_3d())
        if next_ is not None:
            dirs.append((next_ - p.co).to_2d().to_3d())
        normals = [d.cross(z).normalized() for d in dirs if d.length > 1e-9]
        if not normals:
            result.append(Vector())
            continue
        avg = sum(normals, Vector())
        if avg.length < 1e-6:
            avg = normals[0]
        avg.normalize()
        cos = max(0.25, avg.dot(normals[0]))
        result.append(avg * (distance / cos))
    return result


def _shift(p, offset):
    return _Point(p.co + offset, p.left + offset, p.right + offset, p.left_type, p.right_type,
                  p.radius, p.tilt, False)


def _reverse(points):
    out = []
    for p in reversed(points):
        out.append(_Point(p.co, p.right, p.left, p.right_type, p.left_type, p.radius, p.tilt, p.select))
    return out


class MAXIMIZE_OT_spline_outline(Operator):
    """Outline: an offset copy of the selected splines; open splines become one closed outline"""
    bl_idname = "maximize.spline_outline"
    bl_label = "Outline"
    bl_options = {'REGISTER', 'UNDO'}

    distance: FloatProperty(name="Distance", default=0.1, subtype='DISTANCE')

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        def run(objects):
            changed = 0
            for obj in objects:
                curve = obj.data
                for spline in list(curve.splines):
                    points = _read(spline)
                    if not any(p.select for p in points) or len(points) < 2:
                        continue
                    offsets = _offsets(points, spline.use_cyclic_u, self.distance)
                    shifted = [_shift(p, o) for p, o in zip(points, offsets)]
                    if spline.use_cyclic_u:
                        _write(curve, None, shifted, cyclic=True)
                    else:
                        # Original, then the offset copy backwards: one closed shape.
                        _write(curve, spline, points + _reverse(shifted), cyclic=True)
                    changed += 1
            return changed

        if not _with_object_mode(context, run):
            self.report({'WARNING'}, "Select a spline first")
            return {'CANCELLED'}
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Loft


LOFT_GROUP = "MX Loft"


def _loft_group():
    group = find_group(LOFT_GROUP)
    if group is not None:
        return group
    g = GroupBuilder(LOFT_GROUP, "loft")
    path_ob = g.input("Path", 'NodeSocketObject')
    shape_ob = g.input("Shape", 'NodeSocketObject')
    scale = g.input("Scale", 'NodeSocketFloat', 1.0, 0.0)
    caps = g.input("Cap", 'NodeSocketBool', True)
    smooth = g.input("Smooth", 'NodeSocketBool', True)
    out = g.output()
    path = g.node('GeometryNodeObjectInfo', {"Object": path_ob}, transform_space='RELATIVE').outputs["Geometry"]
    shape = g.node('GeometryNodeObjectInfo', {"Object": shape_ob}, transform_space='ORIGINAL').outputs["Geometry"]
    path = g.node('GeometryNodeSetCurveRadius', {"Curve": path, "Radius": scale}).outputs[0]
    mesh = g.node('GeometryNodeCurveToMesh', {"Curve": path, "Profile Curve": shape, "Fill Caps": caps}).outputs[0]
    mesh = g.node('GeometryNodeSetShadeSmooth', {"Mesh": mesh, "Shade Smooth": smooth}).outputs[0]
    g.set(out, mesh)
    return g.tree


class MAXIMIZE_OT_loft(Operator):
    """Loft: sweep the selected shape along the active path; both stay editable"""
    bl_idname = "maximize.loft"
    bl_label = "Loft"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        path = context.active_object
        return (context.mode == 'OBJECT' and path is not None and
                any(o is not path for o in context.selected_objects))

    def execute(self, context):
        path = context.active_object
        shape = next(o for o in context.selected_objects if o is not path)
        name = "Loft001"
        i = 1
        while name in bpy.data.objects:
            i += 1
            name = "Loft{:03d}".format(i)
        obj = bpy.data.objects.new(name, bpy.data.meshes.new(name))
        context.collection.objects.link(obj)
        obj.matrix_world = path.matrix_world
        mod = obj.modifiers.new("Loft", 'NODES')
        mod.node_group = _loft_group()
        modifier_input(mod, "Path").value = path
        modifier_input(mod, "Shape").value = shape
        for o in context.selected_objects:
            o.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# 2D shape booleans


BOOLEAN_GROUP = "MX Shape Boolean"
OPERATIONS = (
    ('UNION', "Union", "Both shapes merged"),
    ('DIFFERENCE', "Subtraction", "The other shape cut out of the active one"),
    ('INTERSECT', "Intersection", "Only where the shapes overlap"),
)


def _boolean_group():
    group = find_group(BOOLEAN_GROUP)
    if group is not None:
        return group
    g = GroupBuilder(BOOLEAN_GROUP, "shape_boolean")
    geometry = g.input("Geometry", 'NodeSocketGeometry')
    other_ob = g.input("Other", 'NodeSocketObject')
    op = g.input("Operation", 'NodeSocketInt', 0, 0, 2)
    out = g.output()
    other = g.node('GeometryNodeObjectInfo', {"Object": other_ob}, transform_space='RELATIVE').outputs["Geometry"]

    def solid(curve):
        """A closed slab around the filled shape, so the exact mesh boolean has volumes to work on."""
        fill = g.node('GeometryNodeFillCurve', {"Curve": curve})
        fill.inputs["Mode"].default_value = 'N-gons'
        filled = fill.outputs[0]
        # Face the fill up whichever way the shape winds, so the slab is not inside out.
        _fx, _fy, fz = g.separate(g.node('GeometryNodeInputNormal').outputs["Normal"])
        down = g.node('FunctionNodeCompare', {"A": fz, "B": 0.0}, data_type='FLOAT', operation='LESS_THAN').outputs[0]
        filled = g.node('GeometryNodeFlipFaces', {"Mesh": filled, "Selection": down}).outputs[0]
        bottom = g.node('GeometryNodeTransform', {"Geometry": filled, "Translation": g.combine(z=-0.5)}).outputs[0]
        flipped = g.node('GeometryNodeFlipFaces', {"Mesh": bottom}).outputs[0]
        top = g.node('GeometryNodeExtrudeMesh', {"Mesh": bottom, "Offset Scale": 1.0, "Offset": g.combine(z=1.0)},
                     mode='FACES').outputs[0]
        join = g.node('GeometryNodeJoinGeometry')
        g.set(join.inputs[0], top)
        g.set(join.inputs[0], flipped)
        return g.node('GeometryNodeMergeByDistance', {"Geometry": join.outputs[0]}).outputs[0]

    a, b = solid(geometry), solid(other)
    results = []
    for operation in ('UNION', 'DIFFERENCE', 'INTERSECT'):
        node = g.node('GeometryNodeMeshBoolean', operation=operation, solver='EXACT')
        if operation == 'DIFFERENCE':
            g.set(node.inputs[0], a)
            g.set(node.inputs[1], b)
        else:
            g.set(node.inputs[1], a)
            g.set(node.inputs[1], b)
        results.append(node.outputs[0])
    pick = g.node('GeometryNodeIndexSwitch', data_type='GEOMETRY')
    while len(pick.index_switch_items) < 3:
        pick.index_switch_items.new()
    g.set(pick.inputs["Index"], op)
    for i, result in enumerate(results):
        g.set(pick.inputs[i + 1], result)
    mesh = pick.outputs[0]
    # Keep the top faces, then their outline.
    normal = g.node('GeometryNodeInputNormal').outputs["Normal"]
    _nx, _ny, nz = g.separate(normal)
    _px, _py, pz = g.separate(g.node('GeometryNodeInputPosition').outputs[0])
    top_face = g.node('FunctionNodeBooleanMath', {
        0: g.node('FunctionNodeCompare', {"A": nz, "B": 0.9}, data_type='FLOAT', operation='GREATER_THAN').outputs[0],
        1: g.node('FunctionNodeCompare', {"A": g.on_faces(pz), "B": 0.25}, data_type='FLOAT',
                  operation='GREATER_THAN').outputs[0]}, operation='AND').outputs[0]
    not_top = g.node('FunctionNodeBooleanMath', {0: top_face}, operation='NOT').outputs[0]
    top = g.node('GeometryNodeDeleteGeometry', {"Geometry": mesh, "Selection": not_top}, domain='FACE').outputs[0]
    faces = g.node('GeometryNodeInputMeshEdgeNeighbors').outputs["Face Count"]
    boundary_sel = g.node('FunctionNodeCompare', {"A": faces, "B": 1.5}, data_type='FLOAT',
                          operation='LESS_THAN').outputs[0]
    curve = g.node('GeometryNodeMeshToCurve', {"Mesh": top, "Selection": boundary_sel}).outputs[0]
    curve = g.node('GeometryNodeTransform', {"Geometry": curve, "Translation": g.combine(z=-0.5)}).outputs[0]
    g.set(out, curve)
    return g.tree


class MAXIMIZE_OT_shape_boolean(Operator):
    """Boolean of two shapes in their plane (Max's Editable Spline Boolean): union, subtraction or
    intersection of the active shape with the other selected one"""
    bl_idname = "maximize.shape_boolean"
    bl_label = "Shape Boolean"
    bl_options = {'REGISTER', 'UNDO'}

    operation: EnumProperty(name="Operation", items=OPERATIONS, default='UNION')

    @classmethod
    def poll(cls, context):
        active = context.active_object
        return (context.mode == 'OBJECT' and active is not None and active.type in {'CURVE', 'MESH'} and
                any(o is not active for o in context.selected_objects))

    def execute(self, context):
        active = context.active_object
        other = next(o for o in context.selected_objects if o is not active)
        from .primitives import is_shape
        from .shapes import to_editable_spline
        if is_shape(active):
            # Shapes (Geometry Nodes) first become editable splines.
            active = to_editable_spline(context, active)
        mod = active.modifiers.new("Shape Boolean", 'NODES')
        mod.node_group = _boolean_group()
        modifier_input(mod, "Other").value = other
        modifier_input(mod, "Operation").value = [o[0] for o in OPERATIONS].index(self.operation)
        # Bake the result into an editable spline.
        active = to_editable_spline(context, active)
        for o in context.selected_objects:
            o.select_set(o is active)
        context.view_layer.objects.active = active
        other.hide_set(True)
        return {'FINISHED'}


class MAXIMIZE_MT_spline_tools(bpy.types.Menu):
    bl_label = "Max Spline Tools"
    bl_idname = "MAXIMIZE_MT_spline_tools"

    def draw(self, context):
        layout = self.layout
        if context.mode == 'EDIT_CURVE':
            layout.operator("maximize.spline_fillet")
            layout.operator("maximize.spline_chamfer")
            layout.operator("maximize.spline_outline")
            layout.operator("wm.tool_set_by_id", text="Refine (Pen)").name = "builtin.pen"
        else:
            layout.operator("maximize.loft")
            for ident, name, _desc in OPERATIONS:
                layout.operator("maximize.shape_boolean", text="Boolean: " + name).operation = ident


def _menu_curve(self, _context):
    self.layout.separator()
    self.layout.menu("MAXIMIZE_MT_spline_tools")


classes = (
    MAXIMIZE_OT_spline_fillet,
    MAXIMIZE_OT_spline_chamfer,
    MAXIMIZE_OT_spline_outline,
    MAXIMIZE_OT_loft,
    MAXIMIZE_OT_shape_boolean,
    MAXIMIZE_MT_spline_tools,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_edit_curve.append(_menu_curve)
    bpy.types.VIEW3D_MT_object.append(_menu_curve)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(_menu_curve)
    bpy.types.VIEW3D_MT_edit_curve.remove(_menu_curve)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

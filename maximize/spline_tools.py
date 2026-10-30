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
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import Operator
from bpy_extras import view3d_utils
from mathutils import Vector
from mathutils.geometry import intersect_line_plane

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


# ------------------------------------------------------------------------------
# Line tool


LINE_TYPES = (
    ('CORNER', "Corner", "Sharp vertex"),
    ('SMOOTH', "Smooth", "Smooth vertex, handles set automatically"),
    ('BEZIER', "Bezier", "Smooth vertex whose handles follow the drag"),
)


class MAXIMIZE_OT_line(Operator):
    """Line, as in Max: click for Initial Type vertices, drag for Drag Type vertices; Shift keeps
    90 degree angles, Backspace removes the last vertex, clicking the first vertex closes the
    spline; right-click or Esc to finish. Snaps to the grid while snapping is on"""
    bl_idname = "maximize.line"
    bl_label = "Line"
    bl_options = {'REGISTER', 'UNDO'}

    initial_type: EnumProperty(name="Initial Type", items=LINE_TYPES[:2], default='CORNER',
                               description="Type of a vertex made by a click")
    drag_type: EnumProperty(name="Drag Type", items=LINE_TYPES, default='BEZIER',
                            description="Type of a vertex made by a drag")
    start_new_shape: BoolProperty(name="Start New Shape", default=True,
                                  description="Off: the line is added as a new spline to the selected shape")

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.area is not None and context.area.type == 'VIEW_3D'

    def invoke(self, context, _event):
        self._obj = None
        self._target = None    # Start New Shape off: the shape that gets the new spline
        if not self.properties.is_property_set("start_new_shape"):
            self.start_new_shape = getattr(context.window_manager, "maximize_start_new_shape", True)
        active = context.active_object
        if not self.start_new_shape and active is not None and active.type == 'CURVE' and active.select_get():
            self._target = active
            self._keep = len(active.data.splines)
        self._points = []      # fixed points: (co, handle or None, vertex type)
        self._plane = None     # AutoGrid: (origin, normal) of the surface under the first click
        self._press = None     # (co, mouse) where the button went down
        self._drag = None
        self._region = None
        context.window_manager.modal_handler_add(self)
        context.workspace.status_text_set("Line: click for corners, drag for curves, click the first point "
                                          "to close; right-click or Esc to finish")
        return {'RUNNING_MODAL'}

    def _region_at(self, context, event):
        for region in context.area.regions:
            if (region.type == 'WINDOW' and region.x <= event.mouse_x < region.x + region.width and
                    region.y <= event.mouse_y < region.y + region.height):
                return region
        return None

    def _hit(self, context, mouse):
        """The point under the mouse on the construction plane, as for the primitives; with AutoGrid
        the plane is the surface under the first click."""
        from .primitives import _grid_plane
        region = self._region
        rv3d = region.data
        plane_origin, normal = self._plane if self._plane is not None else (Vector(), _grid_plane(rv3d)[2])
        origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse)
        direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse)
        hit = intersect_line_plane(origin, origin + direction, plane_origin, normal)
        if hit is not None and context.tool_settings.use_snap:
            step = context.space_data.overlay.grid_scale_unit or 1.0
            hit = Vector([round(c / step) * step for c in hit])
        return hit

    def _orthogonal(self, last, hit):
        from .primitives import _grid_plane
        u, v, _n = _grid_plane(self._region.data)
        d = hit - last
        du, dv = d.dot(u), d.dot(v)
        return last + (u * du if abs(du) >= abs(dv) else v * dv)

    def _screen(self, co):
        p = view3d_utils.location_3d_to_region_2d(self._region, self._region.data, co)
        return p if p is not None else Vector((1e9, 1e9))

    def _vertex(self, co, handle, kind):
        if kind == 'BEZIER' and handle is not None:
            return _Point(co, co - (handle - co), handle, 'ALIGNED', 'ALIGNED')
        if kind == 'SMOOTH':
            return _Point(co, co, co, 'AUTO', 'AUTO')
        return _Point(co)

    def _rebuild(self, context, points):
        """Write `points` [(co, handle or None, type)] into the line's spline."""
        if self._target is not None:
            curve = self._target.data
            for spline in list(curve.splines)[self._keep:]:
                curve.splines.remove(spline)
            local = self._target.matrix_world.inverted()
            return _write(curve, None, [self._vertex(local @ co, None if h is None else local @ h, k)
                                        for co, h, k in points], cyclic=False)
        if self._obj is None:
            data = bpy.data.curves.new("Line", 'CURVE')
            data.dimensions = '3D'
            i = 1
            while "Line{:03d}".format(i) in bpy.data.objects:
                i += 1
            self._obj = bpy.data.objects.new("Line{:03d}".format(i), data)
            context.collection.objects.link(self._obj)
            for o in context.selected_objects:
                o.select_set(False)
            self._obj.select_set(True)
            context.view_layer.objects.active = self._obj
        curve = self._obj.data
        curve.splines.clear()
        _write(curve, None, [self._vertex(co, h, k) for co, h, k in points], cyclic=False)
        return curve.splines[0]

    def _finish(self, context, close=False):
        context.workspace.status_text_set(None)
        if len(self._points) < 2:
            if self._target is not None:
                for spline in list(self._target.data.splines)[self._keep:]:
                    self._target.data.splines.remove(spline)
            elif self._obj is not None:
                data = self._obj.data
                bpy.data.objects.remove(self._obj)
                bpy.data.curves.remove(data)
            return {'CANCELLED'}
        self._rebuild(context, self._points).use_cyclic_u = close
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        if event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            return self._finish(context)
        region = self._region_at(context, event)
        if region is None:
            return {'PASS_THROUGH'} if self._press is None else {'RUNNING_MODAL'}
        self._region = region
        mouse = Vector((event.mouse_x - region.x, event.mouse_y - region.y))
        if event.type == 'BACK_SPACE' and event.value == 'PRESS':
            # Max: Backspace removes the last vertex.
            if self._points:
                self._points.pop()
                if self._points:
                    self._rebuild(context, self._points)
            return {'RUNNING_MODAL'}
        hit = self._hit(context, mouse)
        if hit is None:
            return {'RUNNING_MODAL'}
        if event.shift and self._points and self._press is None:
            # Max: Shift keeps the new segment at 90 degrees, along the construction plane's axes.
            hit = self._orthogonal(self._points[-1][0], hit)
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and not self._points and self._plane is None:
            from .primitives import autogrid_hit
            surface = autogrid_hit(context, region, mouse)
            if surface is not None:
                self._plane = (surface[0], surface[3])
                hit = self._hit(context, mouse)
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if len(self._points) >= 2 and (self._screen(self._points[0][0]) - mouse).length < 10:
                # Max asks "Close spline?" when the first vertex is clicked.
                result = self._finish(context)
                obj = self._target or self._obj
                if result == {'FINISHED'} and obj is not None:
                    bpy.ops.maximize.line_close_confirm('INVOKE_DEFAULT', object_name=obj.name)
                return result
            self._press = (hit, mouse)
            self._drag = None
        elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE' and self._press is not None:
            kind = self.initial_type if self._drag is None else self.drag_type
            self._points.append((self._press[0], self._drag, kind))
            self._press = self._drag = None
            self._rebuild(context, self._points + [(hit, None, 'CORNER')])
        elif event.type == 'MOUSEMOVE':
            if self._press is not None:
                if (mouse - self._press[1]).length > 4:
                    self._drag = hit
                kind = self.initial_type if self._drag is None else self.drag_type
                self._rebuild(context, self._points + [(self._press[0], self._drag, kind)])
            elif self._points:
                self._rebuild(context, self._points + [(hit, None, 'CORNER')])
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}


class MAXIMIZE_OT_line_close_confirm(Operator):
    """Close the spline just drawn"""
    bl_idname = "maximize.line_close_confirm"
    bl_label = "Close spline?"
    bl_options = {'REGISTER', 'UNDO'}

    object_name: StringProperty(options={'HIDDEN', 'SKIP_SAVE'})

    def invoke(self, context, _event):
        return context.window_manager.invoke_confirm(self, None, title="Close spline?", confirm_text="Yes")

    def execute(self, _context):
        obj = bpy.data.objects.get(self.object_name)
        if obj is None or obj.type != 'CURVE' or not obj.data.splines:
            return {'CANCELLED'}
        obj.data.splines[-1].use_cyclic_u = True
        return {'FINISHED'}


class MAXIMIZE_OT_freehand(Operator):
    """Freehand, as in Max: draw a new spline with the mouse (Blender's Draw tool on a new shape)"""
    bl_idname = "maximize.freehand"
    bl_label = "Freehand"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        from .primitives import _max_name
        name = _max_name("Freehand")
        data = bpy.data.curves.new(name, 'CURVE')
        data.dimensions = '3D'
        obj = bpy.data.objects.new(name, data)
        context.collection.objects.link(obj)
        for o in context.selected_objects:
            o.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        context.scene["maximize_level"] = 'VERTEX'
        if context.area is not None and context.area.type == 'VIEW_3D':
            bpy.ops.wm.tool_set_by_id(name="builtin.draw")
        return {'FINISHED'}


def section_curve(context, objects, origin, normal, name="Section"):
    """Max's Section > Create Shape: where the plane (origin, normal) cuts the meshes, as a shape
    of corner vertices. Returns the new object, or None if nothing is cut."""
    loops = section_loops(context, objects, origin, normal)
    if not loops:
        return None
    from .primitives import _max_name
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    for points, closed in loops:
        _write(data, None, [_Point(co) for co in points], cyclic=closed)
    obj = bpy.data.objects.new(_max_name(name), data)
    context.collection.objects.link(obj)
    return obj


def section_loops(context, objects, origin, normal):
    """[(world points, closed)] where the plane cuts the meshes."""
    import bmesh
    depsgraph = context.evaluated_depsgraph_get()
    loops = []
    for obj in objects:
        if obj.type != 'MESH':
            continue
        bm = bmesh.new()
        bm.from_object(obj, depsgraph)
        bm.transform(obj.matrix_world)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        cut = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=origin, plane_no=normal, dist=1e-6)
        edges = {e for e in cut["geom_cut"] if isinstance(e, bmesh.types.BMEdge)}
        # Chain the cut edges into polylines.
        while edges:
            edge = edges.pop()
            chain = [edge.verts[0], edge.verts[1]]
            for at_end in (True, False):
                while True:
                    v = chain[-1] if at_end else chain[0]
                    nxt = next((e for e in v.link_edges if e in edges), None)
                    if nxt is None:
                        break
                    edges.discard(nxt)
                    other = nxt.other_vert(v)
                    if at_end:
                        chain.append(other)
                    else:
                        chain.insert(0, other)
            closed = len(chain) > 2 and chain[0] == chain[-1]
            loops.append(([v.co.copy() for v in (chain[:-1] if closed else chain)], closed))
        bm.free()
    return loops


class MAXIMIZE_OT_section(Operator):
    """Section, as in Max: a shape where a plane through the 3D cursor (its Z axis as the normal)
    cuts the selected meshes"""
    bl_idname = "maximize.section"
    bl_label = "Section"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and any(o.type == 'MESH' for o in context.selected_objects)

    def execute(self, context):
        cursor = context.scene.cursor
        normal = cursor.matrix.to_3x3() @ Vector((0, 0, 1))
        obj = section_curve(context, context.selected_objects, cursor.location.copy(), normal)
        if obj is None:
            self.report({'WARNING'}, "The section plane cuts none of the selected meshes")
            return {'CANCELLED'}
        for o in context.selected_objects:
            o.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Break


def break_spline(curve, spline):
    """Split `spline` at its selected points; each becomes two ends. Returns True if it split."""
    points = _read(spline)
    cuts = [i for i, p in enumerate(points) if p.select]
    if spline.use_cyclic_u:
        if not cuts:
            return False
        first = cuts[0]
        points = points[first:] + points[:first + 1]
        cuts = [0] + [c - first for c in cuts[1:]] + [len(points) - 1]
    else:
        cuts = [c for c in cuts if 0 < c < len(points) - 1]
        if not cuts:
            return False
        cuts = [0] + cuts + [len(points) - 1]
    for a, b in zip(cuts, cuts[1:]):
        piece = [_Point(p.co, p.left, p.right, p.left_type, p.right_type, p.radius, p.tilt, p.select)
                 for p in points[a:b + 1]]
        new = _write(curve, None, piece, cyclic=False)
        new.resolution_u = spline.resolution_u
        new.material_index = spline.material_index
    curve.splines.remove(spline)
    return True


class MAXIMIZE_OT_spline_break(Operator):
    """Break: split the splines at the selected vertices"""
    bl_idname = "maximize.spline_break"
    bl_label = "Break"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        def run(objects):
            return sum(break_spline(obj.data, spline) for obj in objects for spline in list(obj.data.splines))

        if not _with_object_mode(context, run):
            self.report({'WARNING'}, "Select inner vertices to break at")
            return {'CANCELLED'}
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Trim and Extend
#
# A spline is parametrized by u = segment index + t. Intersections are found in the object's XY
# plane on sampled segments, then cut exactly with de Casteljau, so curved segments stay curves.


def _segment(points, i):
    a, b = points[i], points[(i + 1) % len(points)]
    return a.co, a.right, b.left, b.co


def _segment_count(points, cyclic):
    return len(points) if cyclic else len(points) - 1


def _split(c, t):
    """Split the cubic `c` at t into two cubics."""
    p0, p1, p2, p3 = c
    a, b, d = p0.lerp(p1, t), p1.lerp(p2, t), p2.lerp(p3, t)
    e, f = a.lerp(b, t), b.lerp(d, t)
    g = e.lerp(f, t)
    return (p0, a, e, g), (g, f, d, p3)


def _straight(c):
    p0, p1, p2, p3 = c
    line = p3 - p0
    if line.length < 1e-9:
        return True
    return all((p - p0).cross(line).length / line.length < 1e-6 for p in (p1, p2))


def _polyline(points, cyclic):
    """[(u, co)] samples along the spline."""
    out = []
    for i in range(_segment_count(points, cyclic)):
        c = _segment(points, i)
        steps = 1 if _straight(c) else 16
        for k in range(steps):
            t = k / steps
            out.append((i + t, _split(c, t)[1][0] if 0 < t else c[0]))
    end = len(points) if cyclic else len(points) - 1
    out.append((end, points[0].co if cyclic else points[-1].co))
    return out


def _cross2(a, b):
    return a.x * b.y - a.y * b.x


def _edge_hits(p, q, r, s):
    """Intersection of segments p-q and r-s in XY: (fraction on pq, fraction on rs) or None."""
    d1, d2 = (q - p).xy, (s - r).xy
    den = _cross2(d1, d2)
    if abs(den) < 1e-12:
        return None
    w = (r - p).xy
    a, b = _cross2(w, d2) / den, _cross2(w, d1) / den
    if -1e-9 <= a <= 1 + 1e-9 and -1e-9 <= b <= 1 + 1e-9:
        return a, b
    return None


def _intersections(curve, index):
    """Parameters u on spline `index` where it crosses any spline of `curve` (itself included)."""
    splines = [(_read(s), s.use_cyclic_u) for s in curve.splines]
    points, cyclic = splines[index]
    mine = _polyline(points, cyclic)
    found = []
    for j, (other, other_cyclic) in enumerate(splines):
        theirs = mine if j == index else _polyline(other, other_cyclic)
        for k in range(len(mine) - 1):
            (u0, p), (u1, q) = mine[k], mine[k + 1]
            for m in range(len(theirs) - 1):
                if j == index and abs(m - k) <= 1:
                    continue
                (_v0, r), (_v1, s) = theirs[m], theirs[m + 1]
                hit = _edge_hits(p, q, r, s)
                if hit is not None:
                    found.append(u0 + (u1 - u0) * hit[0])
    found.sort()
    return [u for i, u in enumerate(found) if i == 0 or u - found[i - 1] > 1e-6]


def _cut(points, cyclic, u0, u1):
    """The piece of a spline from u0 to u1 (u1 may wrap past the end of a closed spline)."""
    n = _segment_count(points, cyclic)
    if u1 < u0:
        u1 += n
    out = []
    u = u0
    while u < u1 - 1e-9:
        i = int(math.floor(u + 1e-9))
        seg = _segment(points, i % n)
        end = min(u1, i + 1)
        t0, t1 = u - i, end - i
        c = _split(seg, t1)[0] if t1 < 1 - 1e-9 else seg
        if t0 > 1e-9:
            c = _split(c, t0 / t1)[1]
        if not out:
            out.append(_Point(c[0], c[0], c[1], 'FREE', 'FREE'))
        else:
            out[-1].right = c[1]
        out.append(_Point(c[3], c[2], c[3], 'FREE', 'FREE'))
        u = end
    for p, src in ((out[0], u0), (out[-1], u1)):
        k = round(src) % len(points) if abs(src - round(src)) < 1e-9 else None
        if k is not None:
            p.radius, p.tilt = points[k].radius, points[k].tilt
    return out


def trim(curve, index, u):
    """Max's Trim: remove the piece of spline `index` around u, up to the nearest crossings."""
    spline = curve.splines[index]
    points, cyclic = _read(spline), spline.use_cyclic_u
    n = _segment_count(points, cyclic)
    cuts = [c for c in _intersections(curve, index) if 1e-6 < c < n - 1e-6 or cyclic]
    before = [c for c in cuts if c < u]
    after = [c for c in cuts if c > u]
    if cyclic:
        if len(cuts) < 2:
            return False
        a = before[-1] if before else cuts[-1]
        b = after[0] if after else cuts[0]
        pieces = [(b, a)]
    else:
        if not cuts:
            return False
        pieces = []
        if before:
            pieces.append((0.0, before[-1]))
        if after:
            pieces.append((after[0], float(n)))
    for u0, u1 in pieces:
        new = _write(curve, None, _cut(points, cyclic, u0, u1), cyclic=False)
        new.resolution_u = spline.resolution_u
        new.material_index = spline.material_index
    curve.splines.remove(spline)
    return True


def extend(curve, index, at_end):
    """Max's Extend: lengthen the open end of spline `index` straight on to the nearest spline it meets."""
    spline = curve.splines[index]
    if spline.use_cyclic_u:
        return False
    points = _read(spline)
    end = points[-1] if at_end else points[0]
    handle = end.left if at_end else end.right
    neighbor = points[-2] if at_end else points[1]
    direction = end.co - (handle if (end.co - handle).length > 1e-9 else neighbor.co)
    if direction.xy.length < 1e-9:
        return False
    # A ray just long enough to cross everything (mathutils works in single precision).
    polys = [_polyline(_read(s), s.use_cyclic_u) for s in curve.splines]
    reach = 2.0 * max((co - end.co).length for poly in polys for _u, co in poly) + 1.0
    far = end.co + direction.normalized() * reach
    best = None
    for poly in polys:
        for m in range(len(poly) - 1):
            hit = _edge_hits(end.co, far, poly[m][1], poly[m + 1][1])
            if hit is not None and hit[0] * reach > 1e-5 and (best is None or hit[0] < best):
                best = hit[0]
    if best is None:
        return False
    target = end.co.lerp(far, best)
    new = _Point(target)
    if at_end:
        end.right = end.co.copy()
        end.right_type = 'VECTOR'
        points.append(new)
    else:
        end.left = end.co.copy()
        end.left_type = 'VECTOR'
        points.insert(0, new)
    _write(curve, spline, points, cyclic=False)
    return True


class _PickSpline:
    """Modal base: click near a spline in Editable Spline to act on it; right-click or Esc ends."""
    bl_options = {'REGISTER', 'UNDO'}
    status = ""

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE' and context.area is not None and context.area.type == 'VIEW_3D'

    def invoke(self, context, _event):
        context.window_manager.modal_handler_add(self)
        context.workspace.status_text_set(self.status)
        return {'RUNNING_MODAL'}

    def _pick(self, context, event):
        """(object, spline index, u) of the spline point nearest the mouse, within 15 pixels."""
        region = next((r for r in context.area.regions if r.type == 'WINDOW' and
                       r.x <= event.mouse_x < r.x + r.width and r.y <= event.mouse_y < r.y + r.height), None)
        if region is None:
            return None
        mouse = Vector((event.mouse_x - region.x, event.mouse_y - region.y))
        best = None
        for obj in _edit_curves(context):
            for index, s in enumerate(obj.data.splines):
                poly = _polyline(_read(s), s.use_cyclic_u)
                for (u0, a), (u1, b) in zip(poly, poly[1:]):
                    pa = view3d_utils.location_3d_to_region_2d(region, region.data, obj.matrix_world @ a)
                    pb = view3d_utils.location_3d_to_region_2d(region, region.data, obj.matrix_world @ b)
                    if pa is None or pb is None:
                        continue
                    d = pb - pa
                    t = 0.0 if d.length < 1e-6 else max(0.0, min(1.0, (mouse - pa).dot(d) / d.length_squared))
                    dist = (pa + d * t - mouse).length
                    if dist < 15 and (best is None or dist < best[0]):
                        best = (dist, obj, index, u0 + (u1 - u0) * t)
        return best[1:] if best else None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            context.workspace.status_text_set(None)
            return {'FINISHED'}
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = self._pick(context, event)
            if hit is not None:
                obj, index, u = hit
                _with_object_mode(context, lambda _objects: self.act(obj.data, index, u))
                context.area.tag_redraw()
            return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}


class MAXIMIZE_OT_spline_trim(_PickSpline, Operator):
    """Trim: click a piece of spline to remove it up to the nearest crossings"""
    bl_idname = "maximize.spline_trim"
    bl_label = "Trim"
    status = "Trim: click a spline piece to remove it; right-click or Esc to finish"

    def act(self, curve, index, u):
        return trim(curve, index, u)


class MAXIMIZE_OT_spline_extend(_PickSpline, Operator):
    """Extend: click near an open end to lengthen it to the next spline it meets"""
    bl_idname = "maximize.spline_extend"
    bl_label = "Extend"
    status = "Extend: click near an open end; right-click or Esc to finish"

    def act(self, curve, index, u):
        n = _segment_count(_read(curve.splines[index]), curve.splines[index].use_cyclic_u)
        return extend(curve, index, at_end=u > n / 2)


# ------------------------------------------------------------------------------
# Max vertex types, Reset Tangents, Make First


# Max's vertex types as Blender handle types.
VERTEX_TYPES = (
    ('CORNER', "Corner", "Sharp vertex, straight handles towards the neighbours (Vector)"),
    ('SMOOTH', "Smooth", "Smooth curve through the vertex, handles set automatically (Auto)"),
    ('BEZIER', "Bezier", "Smooth vertex with editable, locked-together handles (Aligned)"),
    ('BEZIER_CORNER', "Bezier Corner", "Vertex with two independent handles (Free)"),
)
_BLENDER_TYPE = {'CORNER': 'VECTOR', 'SMOOTH': 'AUTO', 'BEZIER': 'ALIGNED', 'BEZIER_CORNER': 'FREE'}


def _selected_points(curve):
    for spline in curve.splines:
        if spline.type == 'BEZIER':
            for bp in spline.bezier_points:
                if bp.select_control_point:
                    yield bp


def set_vertex_type(curve, vertex_type, only_selected=True):
    """Give the (selected) vertices a Max vertex type. As in Max, a Corner vertex that becomes
    Bezier or Bezier Corner first gets smooth handles."""
    target = _BLENDER_TYPE[vertex_type]
    points = _selected_points(curve) if only_selected else (
        bp for s in curve.splines if s.type == 'BEZIER' for bp in s.bezier_points)
    count = 0
    for bp in points:
        if target in {'ALIGNED', 'FREE'} and 'VECTOR' in {bp.handle_left_type, bp.handle_right_type}:
            bp.handle_left_type = bp.handle_right_type = 'AUTO'
        bp.handle_left_type = bp.handle_right_type = target
        count += 1
    return count


def reset_tangents(curve):
    """Max's Reset Tangents: smooth handles again, keeping each vertex's type."""
    count = 0
    for bp in _selected_points(curve):
        left, right = bp.handle_left_type, bp.handle_right_type
        bp.handle_left_type = bp.handle_right_type = 'AUTO'
        bp.handle_left_type, bp.handle_right_type = left, right
        count += 1
    return count


_POINT_ATTRS = ("co", "handle_left", "handle_right", "handle_left_type", "handle_right_type",
                "radius", "tilt", "weight_softbody", "select_control_point", "select_left_handle",
                "select_right_handle", "hide")


def make_first(curve):
    """Max's Make First: the selected vertex of each closed spline becomes its first vertex."""
    count = 0
    for spline in curve.splines:
        if spline.type != 'BEZIER' or not spline.use_cyclic_u:
            continue
        points = spline.bezier_points
        first = next((i for i, bp in enumerate(points) if bp.select_control_point), 0)
        if first == 0:
            continue
        data = [{a: (getattr(bp, a).copy() if hasattr(getattr(bp, a), "copy") else getattr(bp, a))
                 for a in _POINT_ATTRS} for bp in points]
        data = data[first:] + data[:first]
        for bp, values in zip(points, data):
            # Free handles first, so setting positions doesn't recompute them.
            bp.handle_left_type = bp.handle_right_type = 'FREE'
            for attr in _POINT_ATTRS:
                if attr not in {"handle_left_type", "handle_right_type"}:
                    setattr(bp, attr, values[attr])
        for bp, values in zip(points, data):
            bp.handle_left_type = values["handle_left_type"]
            bp.handle_right_type = values["handle_right_type"]
        count += 1
    return count


class _CurveDataOperator:
    """Edits the curve data of the active curve; in Edit Mode it round-trips through Object Mode
    so the edit-mode selection is used and the result shows."""
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'CURVE' and context.mode in {'EDIT_CURVE', 'OBJECT'}

    def execute(self, context):
        edit = context.mode == 'EDIT_CURVE'
        if edit:
            bpy.ops.object.mode_set(mode='OBJECT')
        count = self.apply(context.active_object.data, only_selected=edit)
        if edit:
            bpy.ops.object.mode_set(mode='EDIT')
        if not count:
            self.report({'WARNING'}, "Nothing to change: select Bezier vertices")
            return {'CANCELLED'}
        return {'FINISHED'}


class MAXIMIZE_OT_spline_vertex_type(_CurveDataOperator, Operator):
    """Set the Max vertex type of the selected vertices (all vertices in Object Mode)"""
    bl_idname = "maximize.spline_vertex_type"
    bl_label = "Vertex Type"

    type: EnumProperty(name="Type", items=VERTEX_TYPES, default='BEZIER')

    def apply(self, curve, only_selected):
        return set_vertex_type(curve, self.type, only_selected)


class MAXIMIZE_OT_spline_reset_tangents(_CurveDataOperator, Operator):
    """Reset the handles of the selected vertices to smooth, keeping their vertex type"""
    bl_idname = "maximize.spline_reset_tangents"
    bl_label = "Reset Tangents"

    @classmethod
    def poll(cls, context):
        return super().poll(context) and context.mode == 'EDIT_CURVE'

    def apply(self, curve, only_selected):
        return reset_tangents(curve)


class MAXIMIZE_OT_spline_make_first(_CurveDataOperator, Operator):
    """Make the selected vertex the first vertex of its closed spline"""
    bl_idname = "maximize.spline_make_first"
    bl_label = "Make First"

    @classmethod
    def poll(cls, context):
        return super().poll(context) and context.mode == 'EDIT_CURVE'

    def apply(self, curve, only_selected):
        return make_first(curve)


# ------------------------------------------------------------------------------
# Editable Spline levels: 1 Vertex, 2 Segment, 3 Spline
#
# Blender's curve Edit Mode selects control points only. At the Segment and Spline levels a click
# selects the control points at both ends of a segment, or all of a spline, and the level tools
# below act on segments (both ends selected) or whole splines.

SPLINE_LEVELS = {'VERTEX': 'VERTEX', 'EDGE': 'SEGMENT', 'BORDER': 'SPLINE'}


def spline_level(context):
    """'VERTEX', 'SEGMENT' or 'SPLINE' (keys 1, 2, 3); stored like the poly levels."""
    return SPLINE_LEVELS.get(context.scene.get("maximize_level"), 'VERTEX')


def _select_point(bp, state):
    bp.select_control_point = bp.select_left_handle = bp.select_right_handle = state


def select_segment(curve, index, segment, state=True):
    points = curve.splines[index].bezier_points
    for i in (segment, (segment + 1) % len(points)):
        _select_point(points[i], state)


def select_spline(curve, index, state=True):
    for bp in curve.splines[index].bezier_points:
        _select_point(bp, state)


def _deselect_all(curve):
    for spline in curve.splines:
        for bp in spline.bezier_points:
            _select_point(bp, False)


def selected_splines(curve):
    """Indices of the splines with every vertex selected."""
    return [i for i, s in enumerate(curve.splines)
            if s.type == 'BEZIER' and all(bp.select_control_point for bp in s.bezier_points)]


class MAXIMIZE_OT_spline_pick(_PickSpline, Operator):
    """Click selection at the Segment and Spline levels: a whole segment or a whole spline (the
    click passes through at the Vertex level)"""
    bl_idname = "maximize.spline_pick"
    bl_label = "Pick Segment / Spline"

    extend: BoolProperty(name="Extend", description="Add to the selection")
    deselect: BoolProperty(name="Deselect", description="Remove from the selection")

    def invoke(self, context, event):
        level = spline_level(context)
        if level == 'VERTEX':
            # Max's Segment End: a click on a segment selects its nearer end.
            if not any(o.data.maximize_shape.segment_end for o in _edit_curves(context)):
                return {'PASS_THROUGH'}
            hit = self._pick(context, event)
            if hit is None:
                return {'PASS_THROUGH'}
            obj, index, u = hit

            def pick_end(_objects):
                if not (self.extend or self.deselect):
                    for other in _objects:
                        _deselect_all(other.data)
                points = obj.data.splines[index].bezier_points
                _select_point(points[int(round(u)) % len(points)], not self.deselect)

            _with_object_mode(context, pick_end)
            context.area.tag_redraw()
            return {'FINISHED'}
        hit = self._pick(context, event)
        if hit is None:
            if not (self.extend or self.deselect):
                bpy.ops.curve.select_all(action='DESELECT')
            return {'FINISHED'}
        obj, index, u = hit

        def pick(_objects):
            curve = obj.data
            if not (self.extend or self.deselect):
                for other in _objects:
                    _deselect_all(other.data)
            if level == 'SPLINE':
                select_spline(curve, index, not self.deselect)
            else:
                count = _segment_count(_read(curve.splines[index]), curve.splines[index].use_cyclic_u)
                select_segment(curve, index, min(int(u), count - 1), not self.deselect)

        _with_object_mode(context, pick)
        context.area.tag_redraw()
        return {'FINISHED'}


def _segment_selected(points, i):
    return points[i].select and points[(i + 1) % len(points)].select


def delete_segments(curve):
    """Delete the selected segments (both ends selected); the splines open or split there."""
    count = 0
    for spline in list(curve.splines):
        if spline.type != 'BEZIER':
            continue
        points = _read(spline)
        cyclic = spline.use_cyclic_u
        n = _segment_count(points, cyclic)
        cut = [i for i in range(n) if _segment_selected(points, i)]
        if not cut:
            continue
        count += len(cut)
        # Walk the spline from just after a cut, collecting runs of points joined by kept segments.
        if cyclic:
            start = (cut[0] + 1) % len(points)
            order = [(start + k) % len(points) for k in range(len(points))]
        else:
            order = list(range(len(points)))
        runs, run = [], [order[0]]
        for a, b in zip(order, order[1:]):
            if a in cut and (b == (a + 1) % len(points)):
                runs.append(run)
                run = [b]
            else:
                run.append(b)
        runs.append(run)
        for run in runs:
            if len(run) > 1:
                piece = [points[i] for i in run]
                for p in piece:
                    p.select = False
                _write(curve, None, piece, cyclic=False).resolution_u = spline.resolution_u
        curve.splines.remove(spline)
    return count


def delete_splines(curve):
    doomed = selected_splines(curve)
    for i in reversed(doomed):
        curve.splines.remove(curve.splines[i])
    return len(doomed)


def close_splines(curve):
    """Max's Close: the selected open splines become closed."""
    count = 0
    for i in selected_splines(curve) or [i for i, s in enumerate(curve.splines)
                                         if any(bp.select_control_point for bp in s.bezier_points)]:
        spline = curve.splines[i]
        if not spline.use_cyclic_u and len(spline.bezier_points) > 1:
            spline.use_cyclic_u = True
            count += 1
    return count


def fuse_vertices(curve):
    """Max's Fuse: move the selected vertices (handles along) to their average position."""
    points = list(_selected_points(curve))
    if len(points) < 2:
        return 0
    centre = sum((bp.co for bp in points), Vector()) / len(points)
    for bp in points:
        offset = centre - bp.co
        left, right = bp.handle_left_type, bp.handle_right_type
        bp.handle_left_type = bp.handle_right_type = 'FREE'
        bp.handle_left = bp.handle_left + offset
        bp.handle_right = bp.handle_right + offset
        bp.co = centre
        bp.handle_left_type, bp.handle_right_type = left, right
    return len(points)


def weld_vertices(curve, threshold):
    """Max's Weld: selected end vertices closer than `threshold` become one vertex. Two ends of
    one spline close it; ends of two splines join them into one spline."""
    welded = 0
    while True:
        ends = []
        for index, spline in enumerate(curve.splines):
            pts = spline.bezier_points
            if spline.type != 'BEZIER' or spline.use_cyclic_u or len(pts) < 1:
                continue
            for at_end in (False, True):
                bp = pts[-1] if at_end else pts[0]
                if bp.select_control_point:
                    ends.append((index, at_end, bp.co.copy()))
        pair = None
        for a in range(len(ends)):
            for b in range(a + 1, len(ends)):
                if (ends[a][2] - ends[b][2]).length <= threshold and \
                        (ends[a][0] != ends[b][0] or len(curve.splines[ends[a][0]].bezier_points) > 2):
                    pair = (ends[a], ends[b])
                    break
            if pair:
                break
        if pair is None:
            return welded
        (ia, end_a, _), (ib, end_b, _) = pair
        if ia == ib:
            spline = curve.splines[ia]
            points = _read(spline)
            first, last = points[0], points[-1]
            first.co = (first.co + last.co) / 2
            first.left = last.left + (first.co - last.co)
            first.left_type = 'FREE' if first.left_type == 'VECTOR' else first.left_type
            _write(curve, spline, points[:-1], cyclic=True)
        else:
            sa, sb = curve.splines[ia], curve.splines[ib]
            a, b = _read(sa), _read(sb)
            if not end_a:
                a = _reverse(a)
            if end_b:
                b = _reverse(b)
            # a ends and b starts at the welded vertex.
            joint = _Point((a[-1].co + b[0].co) / 2, a[-1].left, b[0].right, a[-1].left_type, b[0].right_type,
                           a[-1].radius, a[-1].tilt, True)
            joint.left += joint.co - a[-1].co
            joint.right += joint.co - b[0].co
            merged = a[:-1] + [joint] + b[1:]
            resolution = sa.resolution_u
            for spline in sorted((sa, sb), key=lambda s: -list(curve.splines).index(s)):
                curve.splines.remove(spline)
            _write(curve, None, merged, cyclic=False).resolution_u = resolution
        welded += 1


def _ends(curve):
    """(spline index, at_end, point) of every open Bezier spline end."""
    for index, spline in enumerate(curve.splines):
        pts = spline.bezier_points
        if spline.type == 'BEZIER' and not spline.use_cyclic_u and len(pts):
            yield index, False, pts[0]
            if len(pts) > 1:
                yield index, True, pts[-1]


def auto_weld(curve, threshold):
    """Max's End Point Auto-Welding: a selected (just moved) spline end that lands within
    `threshold` of another end snaps onto it and the two become one vertex."""
    ends = list(_ends(curve))
    moved = [e for e in ends if e[2].select_control_point]
    targets = [e for e in ends if not e[2].select_control_point]
    snapped = 0
    for index, at_end, bp in moved:
        best = None
        for t_index, t_end, t_bp in targets:
            if t_index == index and len(curve.splines[index].bezier_points) < 3:
                continue
            distance = (t_bp.co - bp.co).length
            if distance <= threshold and (best is None or distance < best[0]):
                best = (distance, t_bp)
        if best is None:
            continue
        target = best[1]
        offset = target.co - bp.co
        left, right = bp.handle_left_type, bp.handle_right_type
        bp.handle_left_type = bp.handle_right_type = 'FREE'
        bp.handle_left = bp.handle_left + offset
        bp.handle_right = bp.handle_right + offset
        bp.co = target.co
        bp.handle_left_type, bp.handle_right_type = left, right
        target.select_control_point = True
        targets = [e for e in targets if e[2] != target]
        snapped += 1
    if not snapped:
        return 0
    return weld_vertices(curve, 1e-6)


def _insert(points, cyclic, us):
    """`points` with new knots at the spline parameters `us` (curved segments stay the same curve)."""
    n = _segment_count(points, cyclic)
    by_segment = {}
    for u in sorted(us):
        i = min(int(math.floor(u)), n - 1)
        t = u - i
        if 1e-6 < t < 1 - 1e-6:
            by_segment.setdefault(i, []).append(t)
    out = []
    for i, p in enumerate(points):
        out.append(p)
        if i not in by_segment:
            continue
        c = _segment(points, i)
        straight = _straight(c)
        done = 0.0
        for t in by_segment[i]:
            head, c = _split(c, (t - done) / (1 - done))
            out[-1].right = head[1]
            kind = 'VECTOR' if straight else 'ALIGNED'
            out.append(_Point(head[3], head[2], c[1], kind, kind, p.radius, p.tilt, True))
            done = t
        points[(i + 1) % len(points)].left = c[2]
    return out


def cross_insert(curve, threshold):
    """Max's CrossInsert: a vertex on both splines wherever two splines cross within `threshold`
    (seen from the shape's local Z); the splines stay separate."""
    splines = [(_read(sp), sp.use_cyclic_u) for sp in curve.splines]
    lines = [_polyline(pts, cyc) for pts, cyc in splines]
    cuts = [[] for _ in splines]
    for i in range(len(splines)):
        for j in range(i + 1, len(splines)):
            if curve.splines[i].type != 'BEZIER' or curve.splines[j].type != 'BEZIER':
                continue
            for k in range(len(lines[i]) - 1):
                (u0, p), (u1, q) = lines[i][k], lines[i][k + 1]
                for m in range(len(lines[j]) - 1):
                    (v0, r), (v1, w) = lines[j][m], lines[j][m + 1]
                    hit = _edge_hits(p, q, r, w)
                    if hit is None or (p.lerp(q, hit[0]) - r.lerp(w, hit[1])).length > threshold:
                        continue
                    cuts[i].append(u0 + (u1 - u0) * hit[0])
                    cuts[j].append(v0 + (v1 - v0) * hit[1])
    old = list(curve.splines)
    inserted = 0
    for spline, (pts, cyc), us in zip(old, splines, cuts):
        if not us:
            continue
        new = _insert(pts, cyc, us)
        inserted += len(new) - len(pts)
        if len(new) > len(pts):
            _write(curve, spline, new)
    return inserted


def mirror_splines(context, axis):
    """Max's Mirror (spline level): flip each selected spline about its own centre."""
    settings = context.scene.tool_settings
    pivot = settings.transform_pivot_point
    settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
    try:
        constraint = (axis == 'X', axis == 'Y', False)
        bpy.ops.transform.mirror(orient_type='LOCAL', constraint_axis=constraint)
    finally:
        settings.transform_pivot_point = pivot


def explode_splines(context):
    """Max's Explode: every spline of the edited curve becomes its own object."""
    obj = context.edit_object
    count = len(obj.data.splines)
    bpy.ops.object.mode_set(mode='OBJECT')
    base_name = obj.name
    for i in range(count - 1, 0, -1):
        data = obj.data.copy()
        for j in range(len(data.splines) - 1, -1, -1):
            if j != i:
                data.splines.remove(data.splines[j])
        new = obj.copy()
        new.data = data
        for coll in obj.users_collection:
            coll.objects.link(new)
        new.name = "{:s}.{:03d}".format(base_name, i)
    for j in range(len(obj.data.splines) - 1, 0, -1):
        obj.data.splines.remove(obj.data.splines[j])
    return count


class MAXIMIZE_OT_spline_level_delete(Operator):
    """Delete at the current Editable Spline level: vertices, segments or whole splines (Delete)"""
    bl_idname = "maximize.spline_level_delete"
    bl_label = "Delete"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        level = spline_level(context)
        if level == 'VERTEX':
            return bpy.ops.curve.delete(type='VERT')
        fn = delete_segments if level == 'SEGMENT' else delete_splines
        count = _with_object_mode(context, lambda objects: sum(fn(o.data) for o in objects))
        if not count:
            self.report({'WARNING'}, "Nothing selected at the {:s} level".format(level.title()))
            return {'CANCELLED'}
        return {'FINISHED'}


class MAXIMIZE_OT_spline_divide(Operator):
    """Max's Divide: add vertices evenly in the selected segments"""
    bl_idname = "maximize.spline_divide"
    bl_label = "Divide"
    bl_options = {'REGISTER', 'UNDO'}

    cuts: IntProperty(name="Divisions", default=1, min=1, max=100)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        return bpy.ops.curve.subdivide(number_cuts=self.cuts)


class MAXIMIZE_OT_spline_close(_CurveDataOperator, Operator):
    """Max's Close: close the selected open splines"""
    bl_idname = "maximize.spline_close"
    bl_label = "Close"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def apply(self, curve, only_selected):
        return close_splines(curve)


class MAXIMIZE_OT_spline_fuse(_CurveDataOperator, Operator):
    """Max's Fuse: move the selected vertices to their average position (they stay separate)"""
    bl_idname = "maximize.spline_fuse"
    bl_label = "Fuse"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def apply(self, curve, only_selected):
        return fuse_vertices(curve)


class MAXIMIZE_OT_spline_weld(_CurveDataOperator, Operator):
    """Max's Weld: selected end vertices within the threshold become one vertex, joining or closing
    their splines"""
    bl_idname = "maximize.spline_weld"
    bl_label = "Weld"

    threshold: FloatProperty(name="Threshold", default=0.01, min=0.0, unit='LENGTH')

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def apply(self, curve, only_selected):
        return weld_vertices(curve, self.threshold)


class MAXIMIZE_OT_spline_cross_insert(_CurveDataOperator, Operator):
    """Max's CrossInsert: add a vertex to both splines wherever two splines of the shape cross"""
    bl_idname = "maximize.spline_cross_insert"
    bl_label = "CrossInsert"

    threshold: FloatProperty(name="Threshold", default=0.1, min=0.0, unit='LENGTH',
                             description="How far apart the two splines may pass and still count as crossing")

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def apply(self, curve, only_selected):
        return cross_insert(curve, self.threshold)


# End Point Auto-Welding runs after each finished Move (key, gizmo or tool) in spline Edit Mode.
_last_move = None


def _auto_weld_watch():
    global _last_move
    wm = bpy.context.window_manager
    ops = wm.operators if wm else ()
    if not ops or ops[-1].bl_idname != "TRANSFORM_OT_translate":
        return 0.2
    op = ops[-1]
    key = (op.as_pointer(), tuple(op.properties.value))
    if key == _last_move:
        return 0.2
    _last_move = key
    obj = bpy.context.view_layer.objects.active if bpy.context.view_layer else None
    if obj is None or obj.type != 'CURVE' or obj.mode != 'EDIT' or not obj.data.maximize_shape.auto_weld:
        return 0.2
    window = wm.windows[0] if wm.windows else None
    if window is None:
        return 0.2
    with bpy.context.temp_override(window=window):
        count = _with_object_mode(bpy.context, lambda objects: sum(
            auto_weld(o.data, o.data.maximize_shape.weld_threshold)
            for o in objects if o.data.maximize_shape.auto_weld))
        if count:
            bpy.ops.ed.undo_push(message="Auto Weld")
    return 0.2


class MAXIMIZE_OT_spline_mirror(Operator):
    """Max's Mirror (spline level): flip each selected spline about its own centre"""
    bl_idname = "maximize.spline_mirror"
    bl_label = "Mirror"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(name="Axis", items=(('X', "Horizontal", ""), ('Y', "Vertical", "")))

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        mirror_splines(context, self.axis)
        return {'FINISHED'}


class MAXIMIZE_OT_spline_detach(Operator):
    """Max's Detach: the selected segments or splines become a new shape object"""
    bl_idname = "maximize.spline_detach"
    bl_label = "Detach"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        return bpy.ops.curve.separate()


class MAXIMIZE_OT_spline_explode(Operator):
    """Max's Explode: every spline of the shape becomes its own object"""
    bl_idname = "maximize.spline_explode"
    bl_label = "Explode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE' and context.edit_object is not None and \
            len(context.edit_object.data.splines) > 1

    def execute(self, context):
        count = explode_splines(context)
        self.report({'INFO'}, "Exploded into {:d} objects".format(count))
        return {'FINISHED'}


class MAXIMIZE_MT_spline_vertex_type(bpy.types.Menu):
    bl_label = "Vertex Type"
    bl_idname = "MAXIMIZE_MT_spline_vertex_type"

    def draw(self, _context):
        for ident, name, _desc in VERTEX_TYPES:
            self.layout.operator("maximize.spline_vertex_type", text=name).type = ident


class MAXIMIZE_MT_spline_tools(bpy.types.Menu):
    # "Max" tells it apart in stock Blender; Moritz has no add-on names (it is built in there).
    bl_label = "Spline Tools" if hasattr(bpy.types, "PROPERTIES_PT_create") else "Max Spline Tools"
    bl_idname = "MAXIMIZE_MT_spline_tools"

    def draw(self, context):
        layout = self.layout
        if context.mode == 'EDIT_CURVE':
            layout.menu("MAXIMIZE_MT_spline_vertex_type")
            layout.operator("maximize.spline_reset_tangents")
            layout.operator("maximize.spline_make_first")
            layout.operator("curve.switch_direction", text="Reverse")
            layout.separator()
            layout.operator("maximize.spline_weld")
            layout.operator("maximize.spline_fuse")
            layout.operator("maximize.spline_cross_insert")
            layout.operator("maximize.spline_divide")
            layout.operator("maximize.spline_detach")
            layout.operator("maximize.spline_close")
            layout.operator("maximize.spline_mirror")
            layout.operator("maximize.spline_explode")
            layout.operator("maximize.spline_level_delete")
            layout.separator()
            layout.operator("maximize.spline_fillet")
            layout.operator("maximize.spline_chamfer")
            layout.operator("maximize.spline_outline")
            layout.operator("maximize.spline_break")
            layout.operator("maximize.spline_trim")
            layout.operator("maximize.spline_extend")
            layout.operator("curve.make_segment", text="Connect")
            layout.operator("wm.tool_set_by_id", text="Refine (Pen)").name = "builtin.pen"
        else:
            layout.operator("maximize.line")
            layout.operator("maximize.loft")
            for ident, name, _desc in OPERATIONS:
                layout.operator("maximize.shape_boolean", text="Boolean: " + name).operation = ident


def _menu_curve(self, _context):
    self.layout.separator()
    self.layout.menu("MAXIMIZE_MT_spline_tools")


classes = (
    MAXIMIZE_OT_line,
    MAXIMIZE_OT_line_close_confirm,
    MAXIMIZE_OT_freehand,
    MAXIMIZE_OT_section,
    MAXIMIZE_OT_spline_break,
    MAXIMIZE_OT_spline_trim,
    MAXIMIZE_OT_spline_extend,
    MAXIMIZE_OT_spline_fillet,
    MAXIMIZE_OT_spline_chamfer,
    MAXIMIZE_OT_spline_outline,
    MAXIMIZE_OT_loft,
    MAXIMIZE_OT_shape_boolean,
    MAXIMIZE_OT_spline_vertex_type,
    MAXIMIZE_OT_spline_reset_tangents,
    MAXIMIZE_OT_spline_make_first,
    MAXIMIZE_MT_spline_vertex_type,
    MAXIMIZE_OT_spline_pick,
    MAXIMIZE_OT_spline_level_delete,
    MAXIMIZE_OT_spline_divide,
    MAXIMIZE_OT_spline_close,
    MAXIMIZE_OT_spline_fuse,
    MAXIMIZE_OT_spline_weld,
    MAXIMIZE_OT_spline_cross_insert,
    MAXIMIZE_OT_spline_mirror,
    MAXIMIZE_OT_spline_detach,
    MAXIMIZE_OT_spline_explode,
    MAXIMIZE_MT_spline_tools,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_edit_curve.append(_menu_curve)
    bpy.types.VIEW3D_MT_object.append(_menu_curve)
    if not bpy.app.background:
        bpy.app.timers.register(_auto_weld_watch, first_interval=1.0, persistent=True)


def unregister():
    if bpy.app.timers.is_registered(_auto_weld_watch):
        bpy.app.timers.unregister(_auto_weld_watch)
    bpy.types.VIEW3D_MT_object.remove(_menu_curve)
    bpy.types.VIEW3D_MT_edit_curve.remove(_menu_curve)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

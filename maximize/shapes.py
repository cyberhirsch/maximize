# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Editable (parametric) shapes, as Max's Shapes panel: Rectangle with corner radius, Circle,
Ellipse, Arc, NGon, Star, Helix and Donut.

They are built like the editable primitives (`primitives.py`): a "Parameters" Geometry Nodes
modifier makes the curve, created by dragging in the viewport. "Thickness" renders the shape as a
round tube (Max's "Enable in Viewport / Renderer"). Pressing 1 converts it to an editable spline.
"""

import math

DIST = 'NodeSocketFloat'
INT = 'NodeSocketInt'
FLOAT = 'NodeSocketFloat'

SHAPE_KINDS = (
    ('RECTANGLE', "Rectangle", "", 'MESH_PLANE', 20),
    ('CIRCLE', "Circle", "", 'MESH_CIRCLE', 21),
    ('ELLIPSE', "Ellipse", "", 'MESH_CIRCLE', 22),
    ('ARC', "Arc", "", 'SPHERECURVE', 23),
    ('NGON', "NGon", "", 'SEQ_CHROMA_SCOPE', 24),
    ('STAR', "Star", "", 'SOLO_OFF', 25),
    ('HELIX', "Helix", "", 'FORCE_VORTEX', 26),
    ('DONUT', "Donut", "", 'MESH_TORUS', 27),
)
SHAPES = {kind[0] for kind in SHAPE_KINDS}


def _fillet(b, curve, radius):
    """Round the corners of a poly curve (Rectangle and NGon corner radius)."""
    node = b.node('GeometryNodeFilletCurve', {"Curve": curve, "Radius": radius})
    if hasattr(node, "mode"):
        node.mode = 'BEZIER'
    elif "Mode" in node.inputs:
        node.inputs["Mode"].default_value = 'Bézier'
    return node.outputs[0]


def _finish(b, curve):
    """Optional thickness: the shape as a round tube."""
    thickness = b.input("Thickness", DIST, 0.0, 0.0, subtype='DISTANCE')
    sides = b.input("Thickness Sides", INT, 12, 3, 100)
    profile = b.node('GeometryNodeCurvePrimitiveCircle', {
        "Resolution": sides, "Radius": b.math('MULTIPLY', thickness, 0.5)}).outputs[0]
    mesh = b.node('GeometryNodeCurveToMesh', {"Curve": curve, "Profile Curve": profile, "Fill Caps": True}).outputs[0]
    mesh = b.node('GeometryNodeSetShadeSmooth', {"Mesh": mesh, "Shade Smooth": True}).outputs[0]
    use = b.node('FunctionNodeCompare', {"A": thickness, "B": 0.0},
                 data_type='FLOAT', operation='GREATER_THAN').outputs[0]
    return b.node('GeometryNodeSwitch', {"Switch": use, "False": curve, "True": mesh},
                  input_type='GEOMETRY').outputs[0]


def _build_rectangle(b):
    length = b.input("Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    width = b.input("Width", DIST, 1.0, 0.0, subtype='DISTANCE')
    corner = b.input("Corner Radius", DIST, 0.0, 0.0, subtype='DISTANCE')
    quad = b.node('GeometryNodeCurvePrimitiveQuadrilateral', {"Width": width, "Height": length}).outputs[0]
    return _finish(b, _fillet(b, quad, corner))


def _build_circle(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    steps = b.input("Steps", INT, 32, 3, 512)
    return _finish(b, b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": steps, "Radius": radius}).outputs[0])


def _build_ellipse(b):
    length = b.input("Length", DIST, 1.0, 0.0, subtype='DISTANCE')
    width = b.input("Width", DIST, 0.6, 0.0, subtype='DISTANCE')
    steps = b.input("Steps", INT, 32, 3, 512)
    circle = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": steps, "Radius": 1.0}).outputs[0]
    ellipse = b.node('GeometryNodeTransform', {
        "Geometry": circle,
        "Scale": b.combine(b.math('MULTIPLY', width, 0.5), b.math('MULTIPLY', length, 0.5), 1.0)}).outputs[0]
    return _finish(b, ellipse)


def _build_arc(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    start = b.input("From", FLOAT, 0.0, subtype='ANGLE')
    sweep = b.input("Angle", FLOAT, math.radians(180.0), subtype='ANGLE')
    steps = b.input("Steps", INT, 16, 2, 512)
    arc = b.node('GeometryNodeCurveArc', {
        "Resolution": steps, "Radius": radius, "Start Angle": start, "Sweep Angle": sweep}).outputs[0]
    return _finish(b, arc)


def _build_ngon(b):
    radius = b.input("Radius", DIST, 0.5, 0.0, subtype='DISTANCE')
    sides = b.input("Sides", INT, 6, 3, 100)
    corner = b.input("Corner Radius", DIST, 0.0, 0.0, subtype='DISTANCE')
    ngon = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": sides, "Radius": radius}).outputs[0]
    return _finish(b, _fillet(b, ngon, corner))


def _build_star(b):
    radius1 = b.input("Radius 1", DIST, 0.5, 0.0, subtype='DISTANCE')
    radius2 = b.input("Radius 2", DIST, 0.25, 0.0, subtype='DISTANCE')
    points = b.input("Points", INT, 6, 3, 100)
    twist = b.input("Distortion", FLOAT, 0.0, subtype='ANGLE')
    star = b.node('GeometryNodeCurveStar', {
        "Points": points, "Inner Radius": radius2, "Outer Radius": radius1, "Twist": twist}).outputs[0]
    return _finish(b, star)


def _build_helix(b):
    radius1 = b.input("Radius 1", DIST, 0.5, 0.0, subtype='DISTANCE')
    radius2 = b.input("Radius 2", DIST, 0.5, 0.0, subtype='DISTANCE')
    height = b.input("Height", DIST, 1.0, subtype='DISTANCE')
    turns = b.input("Turns", FLOAT, 3.0, 0.0)
    spiral = b.node('GeometryNodeCurveSpiral', {
        "Resolution": 32, "Rotations": turns, "Start Radius": radius1, "End Radius": radius2,
        "Height": height}).outputs[0]
    return _finish(b, spiral)


def _build_donut(b):
    radius1 = b.input("Radius 1", DIST, 0.5, 0.0, subtype='DISTANCE')
    radius2 = b.input("Radius 2", DIST, 0.35, 0.0, subtype='DISTANCE')
    steps = b.input("Steps", INT, 32, 3, 512)
    outer = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": steps, "Radius": radius1}).outputs[0]
    inner = b.node('GeometryNodeCurvePrimitiveCircle', {"Resolution": steps, "Radius": radius2}).outputs[0]
    join = b.node('GeometryNodeJoinGeometry')
    b.set(join.inputs[0], outer)
    b.set(join.inputs[0], inner)
    return _finish(b, join.outputs[0])


SHAPE_BUILDERS = {
    'RECTANGLE': _build_rectangle,
    'CIRCLE': _build_circle,
    'ELLIPSE': _build_ellipse,
    'ARC': _build_arc,
    'NGON': _build_ngon,
    'STAR': _build_star,
    'HELIX': _build_helix,
    'DONUT': _build_donut,
}

SHAPE_STEPS = {
    'RECTANGLE': ('RECT',),
    'ELLIPSE': ('RECT',),
    'CIRCLE': ('RADIUS',),
    'ARC': ('RADIUS',),
    'NGON': ('RADIUS',),
    'STAR': ('RADIUS', 'RADIUS2'),
    'HELIX': ('RADIUS', 'HEIGHT', 'RADIUS2'),
    'DONUT': ('RADIUS', 'RADIUS2'),
}


# ------------------------------------------------------------------------------
# Convert to Editable Spline


_HANDLE_TYPES = ('FREE', 'AUTO', 'VECTOR', 'ALIGNED')


def _attr(curves, name, default):
    attr = curves.attributes.get(name)
    if attr is None:
        return lambda i: default
    data = attr.data
    key = "vector" if attr.data_type == 'FLOAT_VECTOR' else "value"
    return lambda i: getattr(data[i], key)


def to_editable_spline(context, obj):
    """Replace a shape object by a legacy curve object (Blender's editable spline) with the same
    name, transform and materials. Returns the new object."""
    import bpy
    obj.update_tag()
    depsgraph = context.evaluated_depsgraph_get()
    depsgraph.update()
    # Keep the geometry set alive while its curves are read.
    geometry = obj.evaluated_get(depsgraph).evaluated_geometry()
    curves = geometry.curves
    name = obj.name
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    if curves is not None:
        position = _attr(curves, "position", (0.0, 0.0, 0.0))
        left = _attr(curves, "handle_left", None)
        right = _attr(curves, "handle_right", None)
        left_type = _attr(curves, "handle_type_left", 0)
        right_type = _attr(curves, "handle_type_right", 0)
        curve_type = _attr(curves, "curve_type", 0)
        cyclic = _attr(curves, "cyclic", False)
        for ci, c in enumerate(curves.curves):
            first, count = c.first_point_index, c.points_length
            if curve_type(ci) == 2 and left(first) is not None:
                spline = data.splines.new('BEZIER')
                spline.bezier_points.add(count - 1)
                for k, bp in enumerate(spline.bezier_points):
                    i = first + k
                    bp.co = position(i)
                    bp.handle_left_type = bp.handle_right_type = 'FREE'
                    bp.handle_left = left(i)
                    bp.handle_right = right(i)
                    bp.handle_left_type = _HANDLE_TYPES[left_type(i) % 4]
                    bp.handle_right_type = _HANDLE_TYPES[right_type(i) % 4]
            else:
                # Poly curves (polygons, arcs, stars) become Bezier splines with vector handles,
                # so Fillet and the handle tools work on them.
                spline = data.splines.new('BEZIER')
                spline.bezier_points.add(count - 1)
                for k, bp in enumerate(spline.bezier_points):
                    bp.co = position(first + k)
                    bp.handle_left_type = bp.handle_right_type = 'VECTOR'
            spline.use_cyclic_u = bool(cyclic(ci))
    new = bpy.data.objects.new(name + ".spline", data)
    for coll in obj.users_collection:
        coll.objects.link(new)
    new.matrix_world = obj.matrix_world
    for mat in obj.data.materials:
        data.materials.append(mat)
    old_data = obj.data
    bpy.data.objects.remove(obj)
    if old_data is not None and old_data.users == 0:
        (bpy.data.meshes if isinstance(old_data, bpy.types.Mesh) else bpy.data.curves).remove(old_data)
    new.name = name
    data.name = name
    new.select_set(True)
    context.view_layer.objects.active = new
    return new

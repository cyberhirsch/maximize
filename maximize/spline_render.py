# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's spline Rendering rollout for shapes and editable splines: Enable In Renderer / In Viewport,
a Radial (Thickness, Sides, Angle) or Rectangular (Length, Width, Angle) cross section, Auto
Smooth with a threshold, Generate Mapping Coords, Twist Correction and the caps (Cap, Quad Cap,
Segments, Sphere).

The settings live on the curve data (`Curve.maximize_shape`, next to the shape parameters, so
they stay after Convert to Editable Spline). They drive a "Rendering" Geometry Nodes modifier;
"In Viewport" and "In Renderer" are its viewport and render switches. Stock Blender evaluates the
modifier as it is, it only can't change the settings from this rollout.
"""

import math

import bpy

from .nodes import GroupBuilder, find_group, modifier_input

MODIFIER_NAME = "Rendering"
GROUP_NAME = "MX Renderable Spline"
REVISION = 3
DIST = 'NodeSocketFloat'


def _build(b):
    curve = b.input("Geometry", 'NodeSocketGeometry')
    radial = b.input("Radial", 'NodeSocketBool', True)
    thickness = b.input("Thickness", DIST, 0.01, 0.0, subtype='DISTANCE')
    sides = b.input("Sides", 'NodeSocketInt', 12, 3, 100)
    angle = b.input("Angle", DIST, 0.0, subtype='ANGLE')
    length = b.input("Length", DIST, 0.06, 0.0, subtype='DISTANCE')
    width = b.input("Width", DIST, 0.02, 0.0, subtype='DISTANCE')
    rect_angle = b.input("Rectangular Angle", DIST, 0.0, subtype='ANGLE')
    smooth = b.input("Auto Smooth", 'NodeSocketBool', True)
    threshold = b.input("Threshold", DIST, math.radians(40.0), 0.0, subtype='ANGLE')
    mapping = b.input("Generate Mapping Coords", 'NodeSocketBool', False)
    twist = b.input("Twist Correction", 'NodeSocketBool', True)
    cap = b.input("Cap", 'NodeSocketBool', True)
    quad_cap = b.input("Quad Cap", 'NodeSocketBool', False)
    cap_segments = b.input("Cap Segments", 'NodeSocketInt', 4, 1, 100)
    sphere = b.input("Sphere", 'NodeSocketBool', False)
    # Use Viewport Settings: in the viewport, its own thickness, sides, length and width.
    use_vp = b.input("Use Viewport Settings", 'NodeSocketBool', False)
    vp_thickness = b.input("Viewport Thickness", DIST, 0.01, 0.0, subtype='DISTANCE')
    vp_sides = b.input("Viewport Sides", 'NodeSocketInt', 12, 3, 100)
    vp_length = b.input("Viewport Length", DIST, 0.06, 0.0, subtype='DISTANCE')
    vp_width = b.input("Viewport Width", DIST, 0.02, 0.0, subtype='DISTANCE')
    in_viewport = b.node('FunctionNodeBooleanMath', {
        0: use_vp, 1: b.node('GeometryNodeIsViewport').outputs[0]}, operation='AND').outputs[0]

    def pick(render_value, viewport_value, kind='FLOAT'):
        return b.node('GeometryNodeSwitch', {"Switch": in_viewport, "False": render_value,
                                             "True": viewport_value}, input_type=kind).outputs[0]

    thickness = pick(thickness, vp_thickness)
    sides = pick(sides, vp_sides, 'INT')
    length = pick(length, vp_length)
    width = pick(width, vp_width)

    def boolean(operation, a, c=None):
        inputs = {0: a} if c is None else {0: a, 1: c}
        return b.node('FunctionNodeBooleanMath', inputs, operation=operation).outputs[0]

    # Twist Correction: the cross section follows the spline with the least twist; off, it keeps
    # its up direction (Z).
    least = b.node('GeometryNodeSetCurveNormal', {"Curve": curve}, mode='MINIMUM_TWIST').outputs[0]
    upright = b.node('GeometryNodeSetCurveNormal', {"Curve": curve}, mode='Z_UP').outputs[0]
    curve = b.node('GeometryNodeSwitch', {"Switch": twist, "False": upright, "True": least},
                   input_type='GEOMETRY').outputs[0]

    def rotated(geometry, a):
        return b.node('GeometryNodeTransform', {"Geometry": geometry, "Rotation": b.combine(z=a)}).outputs[0]

    circle = b.node('GeometryNodeCurvePrimitiveCircle', {
        "Resolution": sides, "Radius": b.math('MULTIPLY', thickness, 0.5)}).outputs[0]
    rectangle = b.node('GeometryNodeCurvePrimitiveQuadrilateral', {"Width": width, "Height": length}).outputs[0]
    profile = b.node('GeometryNodeSwitch', {"Switch": radial, "False": rotated(rectangle, rect_angle),
                                            "True": rotated(circle, angle)}, input_type='GEOMETRY').outputs[0]

    # Mapping: U is the length along the spline, V goes once around the cross section.
    def store(geometry, name, value):
        return b.node('GeometryNodeStoreNamedAttribute', {"Geometry": geometry, "Name": name, "Value": value},
                      data_type='FLOAT', domain='POINT').outputs[0]

    along = b.node('GeometryNodeSplineParameter').outputs["Length"]
    around = b.node('GeometryNodeSplineParameter').outputs["Factor"]
    curve = store(curve, "mx_u", along)
    profile = store(profile, "mx_v", around)
    # Caps: flat n-gons, or on the round section a dome of Segments rings (Sphere) or the same
    # rings flattened into quads (Quad Cap), one on each end of every open spline.
    dome = boolean('AND', boolean('AND', cap, radial), boolean('OR', sphere, quad_cap))
    flat = boolean('AND', cap, boolean('NOT', dome))
    mesh = b.node('GeometryNodeCurveToMesh', {"Curve": curve, "Profile Curve": profile, "Fill Caps": flat}).outputs[0]
    ball = b.node('GeometryNodeMeshUVSphere', {"Segments": sides, "Rings": b.math('MULTIPLY', cap_segments, 2.0),
                                              "Radius": b.math('MULTIPLY', thickness, 0.5)}).outputs["Mesh"]
    below = b.node('FunctionNodeCompare', {"A": b.separate(b.node('GeometryNodeInputPosition').outputs[0])[2],
                                           "B": -1e-6}, data_type='FLOAT', operation='LESS_THAN').outputs[0]
    half = b.node('GeometryNodeDeleteGeometry', {"Geometry": ball, "Selection": below}, domain='POINT').outputs[0]
    height = b.node('GeometryNodeSwitch', {"Switch": sphere, "False": 0.0, "True": 1.0}, input_type='FLOAT').outputs[0]
    half = b.node('GeometryNodeTransform', {"Geometry": half, "Scale": b.combine(1.0, 1.0, height)}).outputs[0]
    start = b.node('GeometryNodeCurveEndpointSelection', {"Start Size": 1, "End Size": 0}).outputs[0]
    end = b.node('GeometryNodeCurveEndpointSelection', {"Start Size": 0, "End Size": 1}).outputs[0]
    is_open = boolean('NOT', b.node('GeometryNodeInputSplineCyclic').outputs[0])
    tangent = b.node('GeometryNodeInputTangent').outputs[0]
    backward = b.node('ShaderNodeVectorMath', {0: tangent, "Scale": -1.0}, operation='SCALE').outputs["Vector"]
    outward = b.node('GeometryNodeSwitch', {"Switch": start, "False": tangent, "True": backward},
                     input_type='VECTOR').outputs[0]
    facing = b.node('FunctionNodeAlignRotationToVector', {"Vector": outward}, axis='Z').outputs[0]
    ends = boolean('AND', boolean('AND', boolean('OR', start, end), is_open), dome)
    domes = b.node('GeometryNodeInstanceOnPoints', {"Points": curve, "Selection": ends, "Instance": half,
                                                     "Rotation": facing}).outputs[0]
    domes = b.node('GeometryNodeRealizeInstances', {"Geometry": domes}).outputs[0]
    joined = b.node('GeometryNodeJoinGeometry')
    b.set(joined.inputs[0], domes)
    b.set(joined.inputs[0], mesh)
    mesh = joined.outputs[0]
    u = b.node('GeometryNodeInputNamedAttribute', {"Name": "mx_u"}, data_type='FLOAT').outputs[0]
    v = b.node('GeometryNodeInputNamedAttribute', {"Name": "mx_v"}, data_type='FLOAT').outputs[0]
    mapped = b.store_uv(mesh, b.combine(u, v))
    mesh = b.node('GeometryNodeSwitch', {"Switch": mapping, "False": mesh, "True": mapped},
                  input_type='GEOMETRY').outputs[0]

    # Auto Smooth: smooth faces, sharp edges above the threshold.
    mesh = b.node('GeometryNodeSetShadeSmooth', {"Mesh": mesh, "Shade Smooth": smooth}, domain='FACE').outputs[0]
    edge_angle = b.node('GeometryNodeInputMeshEdgeAngle').outputs["Unsigned Angle"]
    soft = b.node('FunctionNodeCompare', {"A": edge_angle, "B": threshold},
                  data_type='FLOAT', operation='LESS_EQUAL').outputs[0]
    return b.node('GeometryNodeSetShadeSmooth', {"Mesh": mesh, "Shade Smooth": soft}, domain='EDGE').outputs[0]


def ensure_group():
    group = find_group(GROUP_NAME)
    if group is not None and group.get("maximize_revision", 1) != REVISION:
        # An older version of the group: sync() moves the modifiers to the new one.
        group.name = GROUP_NAME + " (old)"
        group = None
    if group is None:
        b = GroupBuilder(GROUP_NAME, "spline_render")
        out = b.output()
        b.set(out, _build(b))
        group = b.tree
        group["maximize_revision"] = REVISION
    return group


def rendering_modifier(obj):
    mod = obj.modifiers.get(MODIFIER_NAME)
    if mod is not None and mod.type == 'NODES' and mod.node_group is not None and \
            mod.node_group.get("maximize_kind") == "spline_render":
        return mod
    return None


# (modifier input, MaximizeShape property)
_INPUTS = (
    ("Thickness", "thickness"), ("Sides", "thickness_sides"), ("Angle", "render_angle"),
    ("Length", "rect_length"), ("Width", "rect_width"), ("Rectangular Angle", "rect_angle"),
    ("Auto Smooth", "auto_smooth"), ("Threshold", "smooth_threshold"),
    ("Generate Mapping Coords", "mapping"), ("Twist Correction", "twist_correction"), ("Cap", "cap"),
    ("Quad Cap", "quad_cap"), ("Cap Segments", "cap_segments"), ("Sphere", "cap_sphere"),
    ("Use Viewport Settings", "use_viewport_settings"), ("Viewport Thickness", "viewport_thickness"),
    ("Viewport Sides", "viewport_sides"), ("Viewport Length", "viewport_rect_length"),
    ("Viewport Width", "viewport_rect_width"),
)


def sync(curve):
    """Bring the Rendering modifier of every object using `curve` in line with its settings."""
    p = curve.maximize_shape
    enabled = p.render_viewport or p.render_renderer
    for obj in bpy.data.objects:
        if obj.data != curve:
            continue
        mod = rendering_modifier(obj)
        if mod is None:
            if not enabled:
                continue
            mod = obj.modifiers.new(MODIFIER_NAME, 'NODES')
            mod.show_in_editmode = False
        group = ensure_group()
        if mod.node_group != group:
            mod.node_group = group
        modifier_input(mod, "Radial").value = p.render_mode == 'RADIAL'
        for name, prop in _INPUTS:
            modifier_input(mod, name).value = getattr(p, prop)
        mod.show_viewport = p.render_viewport
        mod.show_render = p.render_renderer
        obj.update_tag()


def draw(layout, obj):
    """Max's Rendering rollout."""
    p = obj.data.maximize_shape
    col = layout.column(align=True)
    col.prop(p, "render_renderer")
    col.prop(p, "render_viewport")
    layout.prop(p, "use_viewport_settings")
    viewport = p.use_viewport_settings and p.render_settings_target == 'VIEWPORT'
    if p.use_viewport_settings:
        layout.row().prop(p, "render_settings_target", expand=True)
    layout.row().prop(p, "render_mode", expand=True)
    col = layout.column(align=True)
    if p.render_mode == 'RADIAL':
        col.prop(p, "viewport_thickness" if viewport else "thickness")
        col.prop(p, "viewport_sides" if viewport else "thickness_sides")
        col.prop(p, "render_angle")
    else:
        col.prop(p, "viewport_rect_length" if viewport else "rect_length")
        col.prop(p, "viewport_rect_width" if viewport else "rect_width")
        col.prop(p, "rect_angle")
        if not viewport:
            row = col.row(align=True)
            row.prop(p, "rect_aspect")
            row.prop(p, "rect_aspect_lock", text="", icon='LOCKED' if p.rect_aspect_lock else 'UNLOCKED')
    row = layout.row(align=True)
    row.prop(p, "auto_smooth")
    sub = row.row(align=True)
    sub.active = p.auto_smooth
    sub.prop(p, "smooth_threshold", text="Threshold")
    layout.prop(p, "mapping")
    layout.prop(p, "twist_correction")
    row = layout.row(align=True)
    row.prop(p, "cap")
    if p.render_mode == 'RADIAL':
        sub = row.row(align=True)
        sub.active = p.cap
        sub.prop(p, "quad_cap")
        sub.prop(p, "cap_sphere")
        sub = layout.row()
        sub.active = p.cap and (p.quad_cap or p.cap_sphere)
        sub.prop(p, "cap_segments")

# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's spline Rendering rollout for shapes and editable splines: Enable In Renderer / In Viewport,
a Radial (Thickness, Sides, Angle) or Rectangular (Length, Width, Angle) cross section, Auto
Smooth with a threshold, and Generate Mapping Coords.

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
    mesh = b.node('GeometryNodeCurveToMesh', {"Curve": curve, "Profile Curve": profile, "Fill Caps": True}).outputs[0]
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
    if group is None:
        b = GroupBuilder(GROUP_NAME, "spline_render")
        out = b.output()
        b.set(out, _build(b))
        group = b.tree
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
    ("Generate Mapping Coords", "mapping"),
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
            mod.node_group = ensure_group()
            mod.show_in_editmode = False
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
    layout.row().prop(p, "render_mode", expand=True)
    col = layout.column(align=True)
    if p.render_mode == 'RADIAL':
        col.prop(p, "thickness")
        col.prop(p, "thickness_sides")
        col.prop(p, "render_angle")
    else:
        col.prop(p, "rect_length")
        col.prop(p, "rect_width")
        col.prop(p, "rect_angle")
    row = layout.row(align=True)
    row.prop(p, "auto_smooth")
    sub = row.row(align=True)
    sub.active = p.auto_smooth
    sub.prop(p, "smooth_threshold", text="Threshold")
    layout.prop(p, "mapping")

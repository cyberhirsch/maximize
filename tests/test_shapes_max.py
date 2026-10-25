# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_shapes_max.py
# The parametric shapes give the same Bezier vertices and handles as 3ds Max 2026. The reference
# (data/max2026_shapes.json) was dumped from Max: each shape created with these parameters and
# converted to an Editable Spline; per spline the knots as [position, in vector, out vector].
import json
import math
import os
import sys

import addon_utils

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Matrix

from maximize import primitives, shapes


def say(*a): print("MXSM", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


rad = math.radians
# Max's MaxScript parameters, per reference shape.
CASES = {
    'circle_r10': ('CIRCLE', {"radius": 10}),
    'ellipse_20x10': ('ELLIPSE', {"length": 10, "width": 20}),
    'rectangle_20x10': ('RECTANGLE', {"length": 10, "width": 20}),
    'rectangle_20x10_r2': ('RECTANGLE', {"length": 10, "width": 20, "corner_radius": 2}),
    'ngon_r10_6': ('NGON', {"radius": 10, "sides": 6, "scribe": 'INSCRIBED'}),
    'ngon_r10_6_inscribed': ('NGON', {"radius": 10, "sides": 6, "scribe": 'CIRCUMSCRIBED'}),  # scribe:1
    'ngon_r10_6_fillet2': ('NGON', {"radius": 10, "sides": 6, "corner_radius": 2}),
    'ngon_r10_6_circular': ('NGON', {"radius": 10, "sides": 6, "circular": True}),
    'star_10_5_6': ('STAR', {"radius1": 10, "radius2": 5, "points": 6}),
    'star_10_5_6_f': ('STAR', {"radius1": 10, "radius2": 5, "points": 6, "distortion": rad(15),
                               "fillet1": 1, "fillet2": 0.5}),
    'arc_r10_0_90': ('ARC', {"radius": 10, "angle_from": 0, "angle_to": rad(90)}),
    'arc_r10_0_270_pie': ('ARC', {"radius": 10, "angle_from": 0, "angle_to": rad(270), "pie": True}),
    'donut_10_5': ('DONUT', {"radius1": 10, "radius2": 5}),
    'egg_w15': ('EGG', {"width": 15, "outline": False}),
    'egg_w15_outline5': ('EGG', {"width": 15, "outline": True, "egg_thickness": 5}),
    'helix_10_5_20_3': ('HELIX', {"radius1": 10, "radius2": 5, "height": 20, "turns": 3, "direction": 'CW'}),
    'helix_bias': ('HELIX', {"radius1": 10, "radius2": 10, "height": 20, "turns": 2, "bias": 0.5,
                             "direction": 'CCW'}),
}

reference = json.load(open(os.path.join(HERE, "data", "max2026_shapes.json")))
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
ctx = bpy.context

TOL = 2e-4
for name, (kind, params) in CASES.items():
    obj = primitives._create_object(ctx, kind, Matrix())
    shape = obj.data.maximize_shape
    for prop, value in params.items():
        setattr(shape, prop, value)
    ours = obj.data.splines
    theirs = reference[name]
    worst = 0.0
    same = len(ours) == len(theirs)
    for spline, ref in zip(ours, theirs):
        same &= spline.use_cyclic_u == ref["closed"] and len(spline.bezier_points) == len(ref["knots"])
        for bp, (p, left, right) in zip(spline.bezier_points, ref["knots"]):
            for a, b in ((bp.co, p), (bp.handle_left, left), (bp.handle_right, right)):
                worst = max(worst, max(abs(x - y) for x, y in zip(a, b)))
    check("max " + name, same and worst < TOL, kind, "splines", len(ours), "worst", "{:.2e}".format(worst))

# The handle rule reproduces Max's arcs at any angle (measured: 4 knots, these handles at r = 10).
ARCS = {10: 0.193977, 45: 0.873899, 120: 2.35095, 180: 3.57204, 359: 7.64937}
for angle, handle in ARCS.items():
    got = 10 * shapes.arc_handle(rad(angle) / 3)
    check("arc handle {:d}".format(angle), abs(got - handle) < 1e-4, round(got, 6), handle)

# Parameters rebuild the splines; Steps and Thickness drive the curve's own settings.
circle = primitives._create_object(ctx, 'CIRCLE', Matrix())
primitives.parameter(circle, "Radius").value = 2.0
check("rebuild", abs(circle.data.splines[0].bezier_points[0].co.x - 2.0) < 1e-6)
primitives.parameter(circle, "Steps").value = 3
primitives.parameter(circle, "Thickness").value = 0.2
primitives.parameter(circle, "Enable In Viewport").value = True
check("interpolation", circle.data.resolution_u == 4, circle.data.resolution_u)
dg = ctx.evaluated_depsgraph_get()
mesh = circle.evaluated_get(dg).to_mesh()
xs = [v.co.x for v in mesh.vertices]
check("rendering radial", len(mesh.polygons) > 0 and abs(max(xs) - 2.1) < 1e-3, len(mesh.polygons), round(max(xs), 4))
circle.evaluated_get(dg).to_mesh_clear()
shape = circle.data.maximize_shape
shape.render_mode = 'RECTANGULAR'
shape.rect_length, shape.rect_width = 0.6, 0.2
shape.mapping = True
dg = ctx.evaluated_depsgraph_get()
mesh = circle.evaluated_get(dg).to_mesh()
zs = [v.co.z for v in mesh.vertices]
check("rendering rectangular", abs(max(zs) - 0.3) < 1e-4 and "UVMap" in mesh.uv_layers,
      round(max(zs), 4), list(mesh.uv_layers.keys()))
circle.evaluated_get(dg).to_mesh_clear()
shape.render_viewport = False
dg = ctx.evaluated_depsgraph_get()
check("rendering off", circle.evaluated_get(dg).type == 'CURVE' and
      not circle.modifiers["Rendering"].show_viewport)

# Optimize (Moritz core): a rectangle's straight sides evaluate to their corners only.
rect = primitives._create_object(ctx, 'RECTANGLE', Matrix())
if hasattr(rect.data, "use_optimize"):
    def evaluated_points(obj):
        ev = obj.evaluated_get(ctx.evaluated_depsgraph_get())
        mesh = ev.to_mesh()
        n = len(mesh.vertices)
        ev.to_mesh_clear()
        return n
    optimized = evaluated_points(rect)
    primitives.parameter(rect, "Optimize").value = False
    plain = evaluated_points(rect)
    check("optimize", optimized == 4 and plain == 4 * 7, optimized, plain)
else:
    say("SKIP optimize (needs a Moritz build with Curve.use_optimize)")

# Convert to Editable Spline keeps the object and its splines, and drops the parameters.
before = [tuple(bp.co) for bp in circle.data.splines[0].bezier_points]
for o in ctx.selected_objects:
    o.select_set(False)
circle.select_set(True)
ctx.view_layer.objects.active = circle
bpy.ops.maximize.convert_spline()
check("convert", shapes.shape_kind(circle) is None and not primitives.is_shape(circle) and
      [tuple(bp.co) for bp in circle.data.splines[0].bezier_points] == before)

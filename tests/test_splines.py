# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_splines.py
# Editable shapes, conversion to an editable spline, Fillet / Chamfer / Outline, Loft and 2D booleans.
import math
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Matrix

from maximize import primitives, shapes
from maximize.nodes import modifier_input


def say(*a): print("MXSP", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


def evaluated(obj):
    obj.update_tag()
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    return obj.evaluated_get(dg)


for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
ctx = bpy.context

# Every shape evaluates to a curve; with Thickness it becomes a mesh.
for kind in sorted(shapes.SHAPES):
    obj = primitives._create_object(ctx, kind, Matrix())
    ev = evaluated(obj)
    curves = ev.evaluated_geometry().curves if hasattr(ev, "evaluated_geometry") else None
    mod = obj.modifiers[primitives.MODIFIER_NAME]
    modifier_input(mod, "Thickness").value = 0.05
    polys = len(evaluated(obj).data.polygons)
    check("shape " + kind, polys > 0, obj.name, "faces with thickness", polys)
    modifier_input(mod, "Thickness").value = 0.0

rect = bpy.data.objects["Rectangle001"]
modifier_input(rect.modifiers[primitives.MODIFIER_NAME], "Length").value = 2.0
modifier_input(rect.modifiers[primitives.MODIFIER_NAME], "Width").value = 2.0
for o in ctx.selected_objects:
    o.select_set(False)
rect.select_set(True)
ctx.view_layer.objects.active = rect

# Level 1 makes it an editable spline.
bpy.ops.maximize.subobject(level='VERTEX')
rect = ctx.active_object
check("editable spline", rect.type == 'CURVE' and ctx.mode == 'EDIT_CURVE', rect.type, ctx.mode)
spline = rect.data.splines[0]
count = len(spline.bezier_points) or len(spline.points)
say("spline", spline.type, count, spline.use_cyclic_u)

bpy.ops.curve.select_all(action='SELECT')
bpy.ops.maximize.spline_fillet(radius=0.3)
spline = rect.data.splines[0]
check("fillet", len(spline.bezier_points) == 2 * count, len(spline.bezier_points))
bpy.ops.object.mode_set(mode='OBJECT')
spline = rect.data.splines[0]
xs = [p.co.x for p in spline.bezier_points]
check("fillet geometry", abs(max(xs) - 1.0) < 1e-4 and abs(spline.bezier_points[0].co.length - 1.0) > 1e-4,
      round(max(xs), 3))
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.select_all(action='SELECT')
bpy.ops.maximize.spline_outline(distance=0.2)
check("outline", len(rect.data.splines) == 2, len(rect.data.splines))
bpy.ops.object.mode_set(mode='OBJECT')

# Chamfer on a new rectangle.
r2 = primitives._create_object(ctx, 'RECTANGLE', Matrix())
bpy.ops.maximize.subobject(level='VERTEX')
r2 = ctx.active_object
n = len(r2.data.splines[0].bezier_points) or len(r2.data.splines[0].points)
bpy.ops.curve.select_all(action='SELECT')
bpy.ops.maximize.spline_chamfer(distance=0.1)
check("chamfer", len(r2.data.splines[0].bezier_points) == 2 * n, len(r2.data.splines[0].bezier_points))
bpy.ops.object.mode_set(mode='OBJECT')

# Loft: a circle along a helix.
helix = primitives._create_object(ctx, 'HELIX', Matrix())
circle = primitives._create_object(ctx, 'CIRCLE', Matrix())
modifier_input(circle.modifiers[primitives.MODIFIER_NAME], "Radius").value = 0.1
for o in ctx.selected_objects:
    o.select_set(False)
circle.select_set(True)
helix.select_set(True)
ctx.view_layer.objects.active = helix
bpy.ops.maximize.loft()
loft = ctx.active_object
check("loft", loft.name.startswith("Loft") and len(evaluated(loft).data.polygons) > 100,
      loft.name, len(evaluated(loft).data.polygons))

# Boolean: two overlapping squares.
a = primitives._create_object(ctx, 'RECTANGLE', Matrix())
b = primitives._create_object(ctx, 'RECTANGLE', Matrix.Translation((0.5, 0.5, 0)))
for o in ctx.selected_objects:
    o.select_set(False)
a.select_set(True)
b.select_set(True)
ctx.view_layer.objects.active = a
bpy.ops.maximize.shape_boolean(operation='UNION')
a = ctx.active_object
pts = [p.co for s in a.data.splines for p in (s.points if s.type == 'POLY' else s.bezier_points)]
xs = [p.x for p in pts]
check("boolean union", a.type == 'CURVE' and len(a.data.splines) >= 1 and abs(max(xs) - 1.0) < 1e-3 and
      abs(min(xs) + 0.5) < 1e-3, a.type, len(a.data.splines), len(pts),
      round(min(xs), 3) if xs else None, round(max(xs), 3) if xs else None)

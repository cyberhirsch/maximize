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

# Break: a closed rectangle split at two corners gives two open splines.
r3 = primitives._create_object(ctx, 'RECTANGLE', Matrix())
bpy.ops.maximize.subobject(level='VERTEX')
r3 = ctx.active_object
bpy.ops.curve.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
sp = r3.data.splines[0]
pts = sp.bezier_points if sp.type == 'BEZIER' else sp.points
n3 = len(pts)
for i in (0, 2):
    if sp.type == 'BEZIER':
        pts[i].select_control_point = True
    else:
        pts[i].select = True
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.maximize.spline_break()
bpy.ops.object.mode_set(mode='OBJECT')
splines = r3.data.splines
check("break", len(splines) == 2 and not any(s.use_cyclic_u for s in splines) and
      sum(len(s.bezier_points) for s in splines) == n3 + 2, len(splines), [len(s.bezier_points) for s in splines])

# Connect: Blender's Make Segment joins the two ends again.
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
s0, s1 = r3.data.splines
s0.bezier_points[-1].select_control_point = True
s1.bezier_points[0].select_control_point = True
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.make_segment()
bpy.ops.object.mode_set(mode='OBJECT')
check("connect", len(r3.data.splines) == 1, len(r3.data.splines))

# Line: the spline builder behind the modal tool.
from maximize.spline_tools import MAXIMIZE_OT_line
from mathutils import Vector


class _FakeLine:
    _obj = None
    _points = [(Vector((0, 0, 0)), None), (Vector((1, 0, 0)), Vector((1.5, 0.5, 0))), (Vector((1, 1, 0)), None)]


fake = _FakeLine()
MAXIMIZE_OT_line._rebuild(fake, ctx, fake._points)
line = fake._obj
bp = line.data.splines[0].bezier_points
check("line", line.name.startswith("Line") and len(bp) == 3 and bp[0].handle_left_type == 'VECTOR' and
      bp[1].handle_left_type == 'ALIGNED' and (bp[1].handle_left - Vector((0.5, -0.5, 0))).length < 1e-5,
      line.name, len(bp))

# Trim and Extend on straight and curved splines.
from maximize import spline_tools


def poly_curve(name, polylines, cyclic=()):
    data = bpy.data.curves.new(name, 'CURVE')
    for k, pts in enumerate(polylines):
        s = data.splines.new('BEZIER')
        s.bezier_points.add(len(pts) - 1)
        for bp, co in zip(s.bezier_points, pts):
            bp.co = co
            bp.handle_left_type = bp.handle_right_type = 'VECTOR'
        s.use_cyclic_u = k in cyclic
    obj = bpy.data.objects.new(name, data)
    ctx.collection.objects.link(obj)
    return obj


plus = poly_curve("Plus", [[(-1, 0, 0), (1, 0, 0)], [(0, -1, 0), (0, 1, 0)]])
ok = spline_tools.trim(plus.data, 0, 0.8)
xs = sorted(round(p.co.x, 4) for p in plus.data.splines[-1].bezier_points)
check("trim open", ok and len(plus.data.splines) == 2 and xs == [-1.0, 0.0], xs)

box = poly_curve("Box", [[(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)], [(0, -2, 0), (0, 2, 0)]], cyclic=(0,))
ok = spline_tools.trim(box.data, 0, 0.75)   # bottom edge, right of the line
s = box.data.splines[-1]
xs = [round(p.co.x, 4) for p in s.bezier_points]
check("trim closed", ok and not s.use_cyclic_u and len(s.bezier_points) == 4 and xs[0] == 0 and xs[-1] == 0, xs)

ext = poly_curve("Ext", [[(-1, 2, 0), (-0.5, 2, 0)], [(0, -3, 0), (0, 3, 0)]])
ok = spline_tools.extend(ext.data, 0, at_end=True)
end = ext.data.splines[-1].bezier_points[-1].co
check("extend", ok and (end - Vector((0, 2, 0))).length < 1e-5, tuple(round(c, 4) for c in end))

# A curved spline: trimming a circle keeps its curvature.
circ = primitives._create_object(ctx, 'CIRCLE', Matrix())
for o in ctx.selected_objects:
    o.select_set(False)
circ.select_set(True)
ctx.view_layer.objects.active = circ
bpy.ops.maximize.subobject(level='VERTEX')
circ = ctx.active_object
bpy.ops.object.mode_set(mode='OBJECT')
s = circ.data.splines.new('BEZIER')
s.bezier_points.add(1)
for bp, co in zip(s.bezier_points, ((0, -5, 0), (0, 5, 0))):
    bp.co = co
    bp.handle_left_type = bp.handle_right_type = 'VECTOR'
r = max(p.co.length for p in circ.data.splines[0].bezier_points)
ok = spline_tools.trim(circ.data, 0, 0.5)
arc = circ.data.splines[-1]
ev = arc.bezier_points
check("trim curved", ok and len(circ.data.splines) == 2 and
      all(abs(p.co.length - r) < 1e-3 for p in ev), [round(p.co.length, 4) for p in ev], round(r, 4))

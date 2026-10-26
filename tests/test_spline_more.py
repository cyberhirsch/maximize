# Run: moritz.exe --factory-startup -b --python tests/test_spline_more.py
# The rest of Max's Editable Spline rollouts: Refine, Cycle, Area Selection, Select By, Named
# Selections, Tangent Copy / Paste, Cross Section, Attach Mult. (Reorient), Detach options, Explode
# To Splines, Mirror Both, Adaptive, Rendering Aspect lock and Use Viewport Settings.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Matrix, Vector

from maximize import primitives, spline_more, spline_tools


def say(*a): print("MXSM", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


ctx = bpy.context
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)


def shape(kind, at=(0, 0, 0)):
    obj = primitives._create_object(ctx, kind, Matrix.Translation(at))
    for o in ctx.view_layer.objects:
        o.select_set(False)
    ctx.view_layer.objects.active = obj
    obj.select_set(True)
    return obj


def edit(obj):
    bpy.ops.object.mode_set(mode='OBJECT')
    ctx.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='CURVE') if obj.modifiers else None
    bpy.ops.object.mode_set(mode='EDIT')


def pts(obj):
    return obj.data.splines[0].bezier_points


rect = shape('RECTANGLE')
# Refine keeps the shape: one knot more, same outline.
curve = rect.data
n = len(pts(rect))
first = Vector(pts(rect)[0].co)
op = spline_more.MAXIMIZE_OT_spline_refine
dummy = type("R", (), {"_added": []})()
op.act(dummy, curve, 0, 0.5)
check("refine adds a knot", len(curve.splines[0].bezier_points) == n + 1, len(curve.splines[0].bezier_points))
check("refine keeps the shape", (Vector(curve.splines[0].bezier_points[0].co) - first).length < 1e-6)
added = dummy._added[0][1]
check("refine vertex on the edge", abs(added.y - first.y) < 1e-6 or abs(added.x - first.x) < 1e-6, tuple(added))

edit(rect)
bpy.ops.curve.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
pts(rect)[0].select_control_point = True
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.maximize.spline_cycle()
bpy.ops.object.mode_set(mode='OBJECT')
check("cycle", not pts(rect)[0].select_control_point and pts(rect)[1].select_control_point)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.maximize.spline_select_by(by='SPLINE')
bpy.ops.object.mode_set(mode='OBJECT')
check("select by spline", all(bp.select_control_point for bp in pts(rect)))
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.maximize.spline_named_copy()
bpy.ops.curve.select_all(action='DESELECT')
bpy.ops.maximize.spline_named_paste()
bpy.ops.object.mode_set(mode='OBJECT')
check("named selections", all(bp.select_control_point for bp in pts(rect)))

for bp in pts(rect):
    bp.select_control_point = False
pts(rect)[0].select_control_point = True
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.maximize.spline_area_select(distance=100.0)
bpy.ops.object.mode_set(mode='OBJECT')
check("area selection", all(bp.select_control_point for bp in pts(rect)))

# Tangent copy / paste.
bp0 = pts(rect)[0]
bp0.handle_left_type = bp0.handle_right_type = 'FREE'
bp0.handle_right = bp0.co + Vector((0.3, 0.1, 0.0))
for i, bp in enumerate(pts(rect)):
    bp.select_control_point = i == 0
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.maximize.spline_tangent(action='COPY')
bpy.ops.object.mode_set(mode='OBJECT')
for i, bp in enumerate(pts(rect)):
    bp.select_control_point = i == 2
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.maximize.spline_tangent(action='PASTE')
bpy.ops.object.mode_set(mode='OBJECT')
bp2 = pts(rect)[2]
check("tangent paste", ((bp2.handle_right - bp2.co) - Vector((0.3, 0.1, 0))).length < 1e-5)

# Explode to splines: 4 segments of a closed rectangle (5 knots after refine) give 5 splines.
segs = len(pts(rect))
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.maximize.spline_explode_max(to='SPLINES')
bpy.ops.object.mode_set(mode='OBJECT')
check("explode to splines", len(rect.data.splines) == segs and all(len(s.bezier_points) == 2 for s in rect.data.splines),
      len(rect.data.splines))

# Cross Section: three circles stacked, vertices joined by 4 new splines.
circles = [shape('CIRCLE', (0, 0, z)) for z in (0, 1, 2)]
for c in circles:
    bpy.ops.object.mode_set(mode='OBJECT')
    ctx.view_layer.objects.active = c
    bpy.ops.object.convert(target='CURVE') if c.modifiers else None
target = circles[0]
ctx.view_layer.objects.active = target
target.select_set(True)
bpy.ops.maximize.spline_attach_multiple(shapes={circles[1].name, circles[2].name})
check("attach mult.", len(target.data.splines) == 3, len(target.data.splines))
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.select_all(action='SELECT')
bpy.ops.maximize.spline_cross_section()
bpy.ops.object.mode_set(mode='OBJECT')
check("cross section", len(target.data.splines) == 3 + 4, len(target.data.splines))

# Adaptive: a circle's splines get about 6 degrees per step (90 degree arcs: 15 steps).
circle = shape('CIRCLE', (5, 0, 0))
circle.data.maximize_shape.adaptive = True
res = [s.resolution_u for s in circle.data.splines]
check("adaptive", res and 12 <= res[0] <= 20, res)
circle.data.maximize_shape.adaptive = False
check("adaptive off", all(s.resolution_u == circle.data.resolution_u for s in circle.data.splines))

# Show Selected Segs: a circle with two neighbouring knots selected has one red segment.
for i, bp in enumerate(circle.data.splines[0].bezier_points):
    bp.select_control_point = i in (0, 1)
lines = spline_more.selected_segment_lines(circle)
check("selected segment lines", len(lines) >= 2 and len(lines) % 2 == 0, len(lines))

# Rendering: Aspect lock, Use Viewport Settings.
p = circle.data.maximize_shape
p.rect_length, p.rect_width = 0.06, 0.02
check("aspect", abs(p.rect_aspect - 3.0) < 1e-5, p.rect_aspect)
p.rect_aspect_lock = True
p.rect_length = 0.12
check("aspect lock", abs(p.rect_width - 0.04) < 1e-6, p.rect_width)
p.render_viewport = True
p.use_viewport_settings = True
p.viewport_thickness = 0.5
from maximize import spline_render
mod = spline_render.rendering_modifier(circle)
from maximize.nodes import modifier_input
check("viewport settings reach the modifier", mod is not None and
      abs(modifier_input(mod, "Viewport Thickness").value - 0.5) < 1e-6)
dg = ctx.evaluated_depsgraph_get()
dg.update()
ev = circle.evaluated_get(dg)
mesh = ev.to_mesh()
xs = [v.co.z for v in mesh.vertices]
check("viewport thickness used", xs and max(xs) - min(xs) > 0.4, xs and max(xs) - min(xs))
ev.to_mesh_clear()

# Live Section: a plane through a cube cuts a square; Create Shape makes it.
bpy.ops.object.mode_set(mode='OBJECT') if ctx.mode != 'OBJECT' else None
bpy.ops.mesh.primitive_cube_add(location=(20, 0, 0))
ctx.scene.cursor.location = (20, 0, 0)
bpy.ops.maximize.section_plane()
plane = ctx.active_object
loops = spline_tools.section_loops(ctx, spline_more._section_targets(ctx, plane), *spline_more._section_frame(plane))
check("section loops", len(loops) == 1 and loops[0][1] and len(loops[0][0]) >= 4, [len(l[0]) for l in loops])
before = len(bpy.data.curves)
bpy.ops.maximize.section_create_shape()
check("section create shape", len(bpy.data.curves) == before + 1)

# Connect Copy: copies moved by (0, 0, 1) get joined to their originals.
data = bpy.data.curves.new("CC", 'CURVE')
sp = data.splines.new('BEZIER')
sp.bezier_points.add(1)
sp.bezier_points[0].co = (0, 0, 0)
sp.bezier_points[1].co = (1, 0, 0)
sp2 = data.splines.new('BEZIER')
sp2.bezier_points.add(1)
sp2.bezier_points[0].co = (0, 0, 1)
sp2.bezier_points[1].co = (1, 0, 1)
for bp in sp2.bezier_points:
    bp.select_control_point = True
for bp in sp.bezier_points:
    bp.select_control_point = False
made = spline_more.connect_copies(data, Vector((0, 0, 1)))
check("connect copy", made == 2 and len(data.splines) == 4, made)

# Bind: the end of one spline stays on the middle of the other's segment.
data = bpy.data.curves.new("Bind", 'CURVE')
a = data.splines.new('BEZIER')
a.bezier_points.add(1)
a.bezier_points[0].co = (0, 0, 0)
a.bezier_points[1].co = (2, 0, 0)
for bp in a.bezier_points:
    bp.handle_left_type = bp.handle_right_type = 'VECTOR'
b = data.splines.new('BEZIER')
b.bezier_points.add(1)
b.bezier_points[0].co = (5, 5, 0)
b.bezier_points[1].co = (1, 3, 0)
spline_more.bind(data, 1, 1, 0, 0)
check("bind snaps", (Vector(data.splines[1].bezier_points[1].co) - Vector((1, 0, 0))).length < 1e-5,
      tuple(data.splines[1].bezier_points[1].co))
data.splines[0].bezier_points[1].co = (4, 0, 0)
data.splines[0].bezier_points[1].handle_left_type = 'VECTOR'
spline_more.apply_binds(data)
check("bind follows", abs(data.splines[1].bezier_points[1].co.x - 2.0) < 1e-4, tuple(data.splines[1].bezier_points[1].co))
data.splines[1].bezier_points[1].select_control_point = True
check("unbind", spline_more.unbind(data) == 1 and "mx_bind" not in data)
say("DONE")

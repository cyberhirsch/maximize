# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_spline_required.py
# The rare-tier spline controls Seb requires: End Point Auto-Welding, CrossInsert, Twist Correction
# and the rendering caps.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Matrix, Vector

from maximize import primitives, spline_render, spline_tools


def say(*a): print("MXSR", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


def polyline(curve, coords, cyclic=False):
    sp = curve.splines.new('BEZIER')
    sp.bezier_points.add(len(coords) - 1)
    for bp, co in zip(sp.bezier_points, coords):
        bp.co = co
        bp.handle_left_type = bp.handle_right_type = 'VECTOR'
        bp.select_control_point = False
    sp.use_cyclic_u = cyclic
    return sp


for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)

# Auto-weld: the moved (selected) end within the threshold snaps onto the other spline's end.
curve = bpy.data.curves.new("weld", 'CURVE')
polyline(curve, [(0, 0, 0), (1, 0, 0)])
polyline(curve, [(1.1, 0.05, 0), (2, 1, 0)])
curve.splines[1].bezier_points[0].select_control_point = True
n = spline_tools.auto_weld(curve, 0.15)
pts = curve.splines[0].bezier_points if len(curve.splines) == 1 else []
check("auto weld joins", n == 1 and len(curve.splines) == 1 and len(pts) == 3, n, len(curve.splines))
check("auto weld snaps to the target", pts and (pts[1].co - Vector((1, 0, 0))).length < 1e-6,
      pts and tuple(pts[1].co))

curve = bpy.data.curves.new("far", 'CURVE')
polyline(curve, [(0, 0, 0), (1, 0, 0)])
polyline(curve, [(1.5, 0, 0), (2, 1, 0)])
curve.splines[1].bezier_points[0].select_control_point = True
check("auto weld respects threshold", spline_tools.auto_weld(curve, 0.15) == 0 and len(curve.splines) == 2)

curve = bpy.data.curves.new("close", 'CURVE')
polyline(curve, [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0.05, 0.02, 0)])
curve.splines[0].bezier_points[3].select_control_point = True
spline_tools.auto_weld(curve, 0.15)
check("auto weld closes its own spline", curve.splines[0].use_cyclic_u and len(curve.splines[0].bezier_points) == 3)

# CrossInsert: a plus sign gets a vertex on both lines; a near miss within the threshold too.
curve = bpy.data.curves.new("cross", 'CURVE')
polyline(curve, [(-1, 0, 0), (1, 0, 0)])
polyline(curve, [(0, -1, 0.05), (0, 1, 0.05)])
n = spline_tools.cross_insert(curve, 0.1)
counts = [len(s.bezier_points) for s in curve.splines]
mid = [s.bezier_points[1].co.copy() for s in curve.splines]
check("cross insert", n == 2 and counts == [3, 3], n, counts)
check("cross insert positions", (mid[0] - Vector((0, 0, 0))).length < 1e-6 and
      (mid[1] - Vector((0, 0, 0.05))).length < 1e-6, [tuple(m) for m in mid])
curve = bpy.data.curves.new("apart", 'CURVE')
polyline(curve, [(-1, 0, 0), (1, 0, 0)])
polyline(curve, [(0, -1, 0.5), (0, 1, 0.5)])
check("cross insert threshold", spline_tools.cross_insert(curve, 0.1) == 0)

# A curved crossing keeps its shape: the circle's samples do not move.
obj = primitives._create_object(bpy.context, 'CIRCLE', Matrix())
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
from maximize import shapes
obj = shapes.to_editable_spline(bpy.context, obj)
c = obj.data
before = [tuple(round(x, 5) for x in p.co) for p in c.splines[0].bezier_points]
polyline(c, [(-2, 0.3, 0), (2, 0.3, 0)])
n = spline_tools.cross_insert(c, 0.1)
check("cross insert on a circle", n == 4 and len(c.splines[0].bezier_points) == 6, n)


# Rendering: caps and twist correction.
def render_mesh(obj):
    obj.update_tag()
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    me = obj.evaluated_get(dg).to_mesh()
    return len(me.vertices), len(me.polygons), max((len(p.vertices) for p in me.polygons), default=0)


line = primitives._create_object(bpy.context, 'CIRCLE', Matrix())
p = line.data.maximize_shape
p.render_viewport = True
mod = spline_render.rendering_modifier(line)
check("rendering group revision", mod and mod.node_group.get("maximize_revision") == spline_render.REVISION)
# An open spline to cap.
data = bpy.data.curves.new("open", 'CURVE')
polyline(data, [(0, 0, 0), (1, 0, 0), (1, 1, 1)])
ob = bpy.data.objects.new("open", data)
bpy.context.collection.objects.link(ob)
q = data.maximize_shape
q.render_viewport = True
q.thickness_sides = 8
spline_render.sync(data)
flat = render_mesh(ob)
check("flat caps are n-gons", flat[2] == 8, flat)
q.cap = False
spline_render.sync(data)
none = render_mesh(ob)
check("no caps", none[1] == flat[1] - 2 and none[2] == 4, none)
q.cap = True
q.cap_sphere = True
q.cap_segments = 3
spline_render.sync(data)
dome = render_mesh(ob)
check("sphere caps add rings", dome[1] > none[1] and dome[2] <= 4, dome)
dg = bpy.context.evaluated_depsgraph_get()
xs = [v.co.x for v in ob.evaluated_get(dg).to_mesh().vertices]
check("sphere cap points outward", min(xs) < -0.0045, min(xs))
q.cap_sphere = False
q.quad_cap = True
spline_render.sync(data)
quad = render_mesh(ob)
check("quad caps", quad[1] == dome[1] and quad[2] <= 4, quad)
q.twist_correction = False
spline_render.sync(data)
check("twist correction off evaluates", render_mesh(ob)[0] == quad[0])
say("DONE")

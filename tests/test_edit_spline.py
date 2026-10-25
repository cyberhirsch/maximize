# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_edit_spline.py
# Edit Spline modifier (add-on stage): edits on a parametric shape follow its parameters while the
# knot count below stays the same; a knot count change keeps the edits and warns.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Matrix, Vector

from maximize import edit_spline, primitives


def say(*a): print("MXES", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


def knots(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    geometry = obj.evaluated_get(dg).evaluated_geometry()   # keep alive while reading
    pos = geometry.curves.attributes["position"].data
    return [Vector(pos[i].vector) for i in range(len(pos))]


for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
ctx = bpy.context
rect = primitives._create_object(ctx, 'RECTANGLE', Matrix())
primitives.parameter(rect, "Width").value = 2.0
primitives.parameter(rect, "Length").value = 2.0
mod = edit_spline.add_edit_spline(ctx, rect)
before = knots(rect)
check("passthrough", len(before) == 4 and abs(before[0].x - 1.0) < 1e-6, [tuple(round(c, 3) for c in v) for v in before])

# Edit: level 1 swaps in the Edited stand-in; move the first knot up by 0.5.
bpy.ops.maximize.subobject(level='VERTEX')
edited = ctx.active_object
check("session", edited.get(edit_spline.TAG) and ctx.mode == 'EDIT_CURVE' and rect.hide_get(), edited.name, ctx.mode)
bpy.ops.object.mode_set(mode='OBJECT')
bp = edited.data.splines[0].bezier_points[0]
bp.handle_left_type = bp.handle_right_type = 'FREE'
bp.co.z += 0.5
bp.handle_left.z += 0.5
bp.handle_right.z += 0.5
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.maximize.subobject(level='OBJECT')
check("session end", ctx.active_object == rect and ctx.mode == 'OBJECT' and not rect.hide_get(), ctx.active_object.name)
after = knots(rect)
check("edit shows", abs(after[0].z - 0.5) < 1e-6 and abs(after[1].z) < 1e-6, round(after[0].z, 4))

# The shape below changes: the edit follows (index-based).
primitives.parameter(rect, "Width").value = 4.0
moved = knots(rect)
check("edit follows parameters", abs(moved[0].x - 2.0) < 1e-6 and abs(moved[0].z - 0.5) < 1e-6 and
      not edit_spline.topology_changed(ctx, rect), tuple(round(c, 3) for c in moved[0]))

# A knot count change below (corner radius: 8 knots) keeps the edit as it was and warns.
primitives.parameter(rect, "Corner Radius").value = 0.2
frozen = knots(rect)
check("topology change", len(frozen) == 4 and edit_spline.topology_changed(ctx, rect), len(frozen))

# Editing again re-bases onto the new input: the edited knots stay, each following the nearest
# new input knot from now on (the frozen knot at x = 1 moves with its neighbour by +1), and the
# warning goes.
bpy.ops.maximize.subobject(level='EDGE')
bpy.ops.maximize.subobject(level='OBJECT')
check("rebase", not edit_spline.topology_changed(ctx, rect) and len(knots(rect)) == 4, len(knots(rect)))
primitives.parameter(rect, "Width").value = 6.0
check("follows after rebase", abs(knots(rect)[0].x - 2.0) < 1e-6, round(knots(rect)[0].x, 3))

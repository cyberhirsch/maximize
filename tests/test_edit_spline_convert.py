# Run: moritz.exe --factory-startup -b --python tests/test_edit_spline_convert.py
# Converting a stage-0 (Geometry Nodes) Edit Spline to the native modifier keeps the edit.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Matrix, Vector

from maximize import edit_spline, primitives


def say(*a): print("MXESC", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


def output(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    geo = obj.evaluated_get(dg).evaluated_geometry()
    return [Vector(d.vector) for d in geo.curves.attributes["position"].data]


if not edit_spline.native():
    say("SKIP no native Edit Spline")
else:
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)
    ctx = bpy.context
    obj = primitives._create_object(ctx, 'RECTANGLE', Matrix())
    ctx.view_layer.objects.active = obj
    obj.select_set(True)
    # A stage-0 setup, as older files have it.
    real = edit_spline.native
    edit_spline.native = lambda: False
    mod = edit_spline.add_edit_spline(ctx, obj)
    edit_spline.native = real
    check("stage-0 setup", mod.type == 'NODES')
    _base, edited = edit_spline._helpers(mod)
    bp = edited.data.splines[0].bezier_points[0]
    bp.handle_left_type = bp.handle_right_type = 'FREE'
    for name in ("co", "handle_left", "handle_right"):
        setattr(bp, name, getattr(bp, name) + Vector((0, 0, 0.5)))
    obj.update_tag()
    before = output(obj)
    check("edit shows", abs(before[0].z - 0.5) < 1e-6)

    new = edit_spline.convert_to_native(ctx, obj, mod)
    check("native now", new.type == 'EDIT_SPLINE' and obj.modifiers[0] == new and all(m.type != 'NODES' or m.node_group.get("maximize_kind") != "edit_spline" for m in obj.modifiers),
          [m.type for m in obj.modifiers])
    check("helpers removed", not any(o.get(edit_spline.TAG) for o in bpy.data.objects))
    after = output(obj)
    check("same output", len(after) == len(before) and all((a - b).length < 1e-6 for a, b in zip(after, before)))
    primitives.parameter(obj, "Width").value = 4.0
    moved = output(obj)
    check("follows the parameters", abs(moved[0].x - 2.0) < 1e-6 and abs(moved[0].z - 0.5) < 1e-6,
          tuple(moved[0]))
say("DONE")

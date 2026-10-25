# Run: moritz.exe --factory-startup -b --python tests/test_edit_spline_native.py
# Maximize's Edit Spline on the native EDIT_SPLINE modifier (Moritz builds): add, edit through the
# stand-in, store, follow the shape's parameters below, the Interpolation settings.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Matrix, Vector

from maximize import edit_spline, primitives


def say(*a): print("MXESN", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


def output(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    geo = obj.evaluated_get(dg).evaluated_geometry()
    c = geo.curves
    return [Vector(d.vector) for d in c.attributes["position"].data] if c else []


if not edit_spline.native():
    say("SKIP no native Edit Spline in this build")
    say("DONE")
else:
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)
    ctx = bpy.context
    obj = primitives._create_object(ctx, 'CIRCLE', Matrix())
    ctx.view_layer.objects.active = obj
    obj.select_set(True)
    mod = edit_spline.add_edit_spline(ctx, obj)
    check("native modifier", mod.type == 'EDIT_SPLINE', mod.type)
    check("no helpers", not any(o.get(edit_spline.TAG) for o in bpy.data.objects))
    before = output(obj)

    edit_spline.begin_edit(ctx, obj, mod, 'VERTEX')
    stand_in = ctx.view_layer.objects.active
    check("stand-in", stand_in is not obj and stand_in.mode == 'EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bp = stand_in.data.splines[0].bezier_points[0]
    for name in ("co", "handle_left", "handle_right"):
        setattr(bp, name, getattr(bp, name) + Vector((0, 0, 0.5)))
    edit_spline.end_edit(ctx)
    check("stored", mod.edit_mode == 'TOPOLOGY', mod.edit_mode)
    check("stand-in removed", not any(o.name.endswith("Edit Spline") for o in bpy.data.objects))
    after = output(obj)
    check("knot moved", len(after) == len(before) and abs(after[0].z - before[0].z - 0.5) < 1e-5,
          after and tuple(after[0]))

    # The shape's radius changes below: the edit rides along.
    obj.data.maximize_shape.radius = 2.0
    obj.update_tag()
    grown = output(obj)
    check("follows the parameters", abs(grown[1].length - 2.0) < 1e-4 and abs(grown[0].z - 0.5) < 1e-5,
          tuple(grown[1]), tuple(grown[0]))

    # Topology: a knot added on the stand-in.
    edit_spline.begin_edit(ctx, obj, mod, 'VERTEX')
    stand_in = ctx.view_layer.objects.active
    bpy.ops.object.mode_set(mode='OBJECT')
    sp = stand_in.data.splines[0]
    sp.bezier_points.add(1)
    sp.bezier_points[-1].co = (3, 3, 0)
    sp.bezier_points[-1].tilt = -1.0
    edit_spline.end_edit(ctx)
    check("stored topology", mod.edit_mode == 'TOPOLOGY', mod.edit_mode)
    check("topology output", len(output(obj)) == len(grown) + 1, len(output(obj)))
    obj.data.maximize_shape.radius = 1.0
    obj.update_tag()
    back = output(obj)
    check("topology follows", abs(back[1].length - 1.0) < 1e-4 and (back[-1] - Vector((3, 3, 0))).length < 1e-5,
          tuple(back[1]), tuple(back[-1]))

    mod.steps = 2
    check("steps prop", mod.steps == 2)
    say("DONE")

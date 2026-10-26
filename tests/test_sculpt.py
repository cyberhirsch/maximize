# Run: moritz.exe --factory-startup -b --python tests/test_sculpt.py
# The Sculpt modifier: Multires at the bottom of the stack, mid-stack on a native Edit Poly (Moritz),
# sculpt offsets stored on leaving, Dyntopo bakes the levels.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Vector

from maximize import edit_poly, sculpt


def say(*a): print("MXSC", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


def output(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    ev = obj.evaluated_get(dg)
    mesh = ev.to_mesh()
    cos = [v.co.copy() for v in mesh.vertices]
    ev.to_mesh_clear()
    return cos


ctx = bpy.context
cube = bpy.data.objects["Cube"]
ctx.view_layer.objects.active = cube
cube.select_set(True)
mod = sculpt.add_sculpt(ctx, cube)
check("bottom is multires", mod.type == 'MULTIRES' and sculpt.is_sculpt(cube, mod))
bpy.ops.object.multires_subdivide(modifier=mod.name, mode='CATMULL_CLARK')
check("subdivided", mod.total_levels == 1)
sculpt.begin_sculpt(ctx, cube, mod)
check("sculpt mode", cube.mode == 'SCULPT')
sculpt.end_sculpt(ctx)
check("back", cube.mode == 'OBJECT')
bpy.ops.maximize.sculpt_dyntopo('EXEC_DEFAULT')
check("dyntopo bakes", not any(m.type == 'MULTIRES' for m in cube.modifiers) and len(cube.data.vertices) > 8 and
      cube.use_dynamic_topology_sculpting, len(cube.data.vertices))
bpy.ops.object.mode_set(mode='OBJECT')

if edit_poly.native():
    bpy.ops.mesh.primitive_cube_add(location=(5, 0, 0))
    box = ctx.active_object
    box.modifiers.new("Bevel", 'BEVEL')
    mid = sculpt.add_sculpt(ctx, box)
    check("mid-stack is edit poly", mid.type == 'EDIT_POLY' and sculpt.is_midstack(box, mid))
    before = output(box)
    stand_in = sculpt.begin_sculpt(ctx, box, mid)
    stand_in_name = stand_in.name
    check("stand-in sculpt", stand_in is not box and stand_in.mode == 'SCULPT' and box.hide_get())
    bpy.ops.object.mode_set(mode='OBJECT')
    # A "stroke": move one vertex up.
    stand_in.data.vertices[0].co.z += 0.5
    bpy.ops.object.mode_set(mode='SCULPT')
    sculpt.end_sculpt(ctx)
    after = output(box)
    moved = [i for i, (a, b) in enumerate(zip(before, after)) if (a - b).length > 1e-4]
    check("offset stored", len(after) == len(before) and len(moved) == 1 and
          abs(after[moved[0]].z - before[moved[0]].z - 0.5) < 1e-4, moved)
    check("stand-in gone", stand_in_name not in bpy.data.objects and not box.hide_get())
else:
    say("SKIP no native Edit Poly")
say("DONE")

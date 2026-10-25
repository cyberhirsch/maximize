# Run: moritz.exe --factory-startup -b --python tests/bench_edit_poly.py
# Time entering and leaving an Edit Poly level on a heavy mesh (about 400k vertices, a Displace
# below), against one evaluation of the stack, the unit the begin cost is made of.
import os
import sys
import time

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy

from maximize import edit_poly


def say(*a): print("MXBENCH", " ".join(str(x) for x in a), flush=True)


obj = bpy.data.objects["Cube"]
bpy.context.view_layer.objects.active = obj
sub = obj.modifiers.new("Sub", 'SUBSURF')
sub.levels = 8
with bpy.context.temp_override(object=obj, active_object=obj):
    bpy.ops.object.modifier_apply(modifier=sub.name)
disp = obj.modifiers.new("Displace", 'DISPLACE')
disp.strength = 0.1
bpy.ops.maximize.edit_poly_add()
mod = obj.modifiers.active
say("vertices", len(obj.data.vertices), "core session" if hasattr(mod, "session_begin") else "stand-in")

t = time.perf_counter()
me = edit_poly._evaluated_mesh(bpy.context, obj, mod, include=False)
one_eval = time.perf_counter() - t
bpy.data.meshes.remove(me)

for run in range(3):
    t = time.perf_counter()
    bpy.ops.maximize.subobject(level='VERTEX')
    enter = time.perf_counter() - t
    t = time.perf_counter()
    bpy.ops.maximize.subobject(level='OBJECT')
    leave = time.perf_counter() - t
    say("run", run, "enter %.0f ms" % (enter * 1000), "leave %.0f ms" % (leave * 1000),
        "one stack evaluation %.0f ms" % (one_eval * 1000))

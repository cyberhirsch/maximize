# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_phase4.py
# Smoothing groups, instances that share the modifier stack, Make Unique, Freeze.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bmesh
import bpy
from mathutils import Vector

from maximize import transform


def say(*a): print("MXP4", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


def evaluated(obj):
    obj.update_tag()
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    return obj.evaluated_get(dg).data


ctx = bpy.context
cube = bpy.data.objects["Cube"]
ctx.view_layer.objects.active = cube
cube.select_set(True)

# Smoothing groups.
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type='FACE')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.maximize.smoothing_group(group=1)


def sharp_count():
    bm = bmesh.from_edit_mesh(cube.data)
    return sum(not e.smooth for e in bm.edges), sum(f.smooth for f in bm.faces)


check("all in group 1", sharp_count() == (0, 6), sharp_count())
bm = bmesh.from_edit_mesh(cube.data)
for f in bm.faces:
    f.select_set(f.calc_center_median().z > 0.9)
bmesh.update_edit_mesh(cube.data)
bpy.ops.maximize.smoothing_group('EXEC_DEFAULT', group=2)
bpy.ops.maximize.smoothing_group('EXEC_DEFAULT', group=1)
check("top in group 2 only", sharp_count()[0] == 4, sharp_count())
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.maximize.smoothing_auto(angle=0.5)
check("auto smooth 30 deg", sharp_count() == (12, 6), sharp_count())
bpy.ops.maximize.smoothing_group(group=32)
check("group 32 (sign bit)", sharp_count()[0] == 0, sharp_count())
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.maximize.smoothing_select(group=32)
bm = bmesh.from_edit_mesh(cube.data)
check("select by SG", sum(f.select for f in bm.faces) == 6)
bpy.ops.object.mode_set(mode='OBJECT')
check("sharp edges in the mesh", "sharp_edge" not in cube.data.attributes or
      not any(a.value for a in cube.data.attributes["sharp_edge"].data))

# Instances share the stack, including modifiers added later.
sub = cube.modifiers.new("TurboSmooth", 'SUBSURF')
sub.levels = 1
bpy.ops.maximize.clone(clone_type='INSTANCE', copies=1)
inst = next(o for o in ctx.selected_objects if o is not cube)
check("instance shares", transform.shared_stack(inst) is not None and inst.data == cube.data,
      [m.name for m in inst.modifiers])
cube.modifiers.new("Shell", 'SOLIDIFY')
n_orig, n_inst = len(evaluated(cube).vertices), len(evaluated(inst).vertices)
check("modifier added later reaches the instance", n_orig == n_inst and n_orig > 26, n_orig, n_inst)
own = inst.modifiers.new("Bend", 'SIMPLE_DEFORM')
check("instance's own modifier stays on it", len(cube.modifiers) == 2)

for o in ctx.selected_objects:
    o.select_set(False)
inst.select_set(True)
ctx.view_layer.objects.active = inst
bpy.ops.maximize.make_unique()
names = [m.name for m in inst.modifiers]
check("make unique", transform.shared_stack(inst) is None and inst.data != cube.data and
      names == ["TurboSmooth", "Shell", "Bend"], names, len(evaluated(inst).vertices))

# Freeze.
inst.select_set(True)
bpy.ops.maximize.freeze(freeze=True)
check("freeze", inst.hide_select and not inst.select_get())
bpy.ops.maximize.freeze(freeze=False)
check("unfreeze", not inst.hide_select)

# Deform gizmo poll.
from maximize import modifier_gizmos
ctx.view_layer.objects.active = inst
inst.modifiers.active = inst.modifiers["Bend"]
check("deform gizmo", modifier_gizmos._deform_modifier(inst) is not None)

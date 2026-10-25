# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_edit_poly.py
# Edit Poly in the middle of the stack: edits follow the stack below, survive a topology change
# below with a warning flag, and collapse.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bmesh
import bpy
from mathutils import Vector

from maximize import edit_poly


def say(*a): print("MXEP", " ".join(str(x) for x in a), flush=True)


def evaluated(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    return obj.evaluated_get(dg).data


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


obj = bpy.data.objects["Cube"]
bpy.context.view_layer.objects.active = obj
disp = obj.modifiers.new("Displace", 'DISPLACE')
disp.strength = 0.0
disp.direction = 'Z'
disp.mid_level = 0.0

bpy.ops.maximize.edit_poly_add()
mod = obj.modifiers.active
NATIVE = edit_poly.is_native(mod)
say("native modifier" if NATIVE else "geometry nodes prototype")
check("added", edit_poly.is_edit_poly(mod), [m.name for m in obj.modifiers])


def changed_flag(me):
    """The prototype's topology warning; the native modifier warns in its panel instead."""
    flag = me.attributes.get(edit_poly.CHANGED)
    return None if flag is None else bool(flag.data[0].value)

# Level 1 edits the modifier's mesh in place of the object.
bpy.ops.maximize.subobject(level='VERTEX')
stand_in = bpy.context.active_object
check("stand-in", stand_in is not obj and bpy.context.mode == 'EDIT_MESH', stand_in.name)
bm = bmesh.from_edit_mesh(stand_in.data)
bm.verts.ensure_lookup_table()
v0 = bm.verts[0].co.copy()
bm.verts[0].co.z += 1.0
# Extrude a face: the new vertices follow the vertices they came from.
face = max(bm.faces, key=lambda f: f.calc_center_median().z)
ret = bmesh.ops.extrude_face_region(bm, geom=[face])
new_verts = [e for e in ret["geom"] if isinstance(e, bmesh.types.BMVert)]
bmesh.ops.translate(bm, verts=new_verts, vec=(0, 0, 0.5))
bmesh.update_edit_mesh(stand_in.data)
bpy.ops.maximize.subobject(level='OBJECT')
check("back", bpy.context.active_object == obj and bpy.context.mode == 'OBJECT', bpy.context.active_object.name)

me = evaluated(obj)
check("edit kept", abs(me.vertices[0].co.z - (v0.z + 1.0)) < 1e-4 and len(me.vertices) == 12,
      round(me.vertices[0].co.z, 3), len(me.vertices))

# Change the stack below: everything moves up 2; the edit rides along.
disp.strength = 2.0
me = evaluated(obj)
check("follows below", abs(me.vertices[0].co.z - (v0.z + 3.0)) < 1e-4, round(me.vertices[0].co.z, 3))
top = max(me.vertices, key=lambda v: v.co.z).co.z
# The extruded copy of vertex 0 (moved up 1, then extruded 0.5) rides along too.
check("extruded follows", abs(top - (v0.z + 1.0 + 0.5 + 2.0)) < 1e-4, round(top, 3))
check("no warning", NATIVE or changed_flag(me) is False)

# Topology change below: the edits stay as they were and the flag warns.
sub = obj.modifiers.new("Subdivision", 'SUBSURF')
sub.levels = 1
with bpy.context.temp_override(object=obj):
    bpy.ops.object.modifier_move_to_index(modifier=sub.name, index=1)
me = evaluated(obj)
check("topology warning", (NATIVE or changed_flag(me)) and len(me.vertices) == 12, len(me.vertices))

# Editing again re-bases onto the new input.
obj.modifiers.active = obj.modifiers["Edit Poly"]
bpy.ops.maximize.subobject(level='POLYGON')
bpy.ops.maximize.subobject(level='OBJECT')
me = evaluated(obj)
check("re-based", (changed_flag(me) is False) if not NATIVE else
      (mod.edit_mode == 'TOPOLOGY' and len(me.vertices) == 12), len(me.vertices))

helpers = [o.name for o in bpy.data.objects if o.get(edit_poly.TAG)]
obj.modifiers.active = obj.modifiers["Edit Poly"]
bpy.ops.maximize.collapse_all()
left = [o.name for o in bpy.data.objects if o.get(edit_poly.TAG)]
check("collapse all", len(obj.modifiers) == 0 and not left and edit_poly.ORIG not in obj.data.attributes,
      helpers, left, len(obj.data.vertices))

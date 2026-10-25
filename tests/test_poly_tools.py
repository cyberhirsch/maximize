# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_poly_tools.py
# Edit Poly buttons for Blender tools: aliases, Material IDs, Make Planar X / Y / Z, Create Shape.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bmesh
import bpy


def say(*a): print("MXPT", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
bpy.ops.mesh.primitive_cube_add()
obj = bpy.context.active_object
for name in ("A", "B", "C"):
    obj.data.materials.append(bpy.data.materials.new(name))
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type='FACE')
bpy.ops.mesh.select_all(action='DESELECT')
bm = bmesh.from_edit_mesh(obj.data)
bm.faces.ensure_lookup_table()
bm.faces[0].select = True
bm.faces[1].select = True
bmesh.update_edit_mesh(obj.data)
check("set id", bpy.ops.maximize.set_material_id(material_id=3) == {'FINISHED'})
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.maximize.select_material_id(material_id=3, clear=True)
bm = bmesh.from_edit_mesh(obj.data)
sel = [f.index for f in bm.faces if f.select]
check("select id clears", sel == [0, 1], sel)
bm.faces.ensure_lookup_table()
for f in bm.faces:
    f.select = f.index == 5
bm.select_flush_mode()
bmesh.update_edit_mesh(obj.data)
bpy.ops.maximize.select_material_id(material_id=3, clear=False)
bm = bmesh.from_edit_mesh(obj.data)
check("select id adds", sorted(f.index for f in bm.faces if f.select) == [0, 1, 5])

bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.maximize.make_planar_axis(axis='Z')
bm = bmesh.from_edit_mesh(obj.data)
zs = {round(v.co.z, 5) for v in bm.verts}
check("make planar z", zs == {0.0}, zs)

for ident in ("split", "break_vertex", "turn", "remove_isolated", "create_poly", "hard", "smooth_edges",
              "select_by_angle"):
    check("alias " + ident, hasattr(bpy.ops.maximize, ident) and
          bpy.ops.maximize.__getattr__(ident).idname() == "MAXIMIZE_OT_" + ident)

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_plane_add()
plane = bpy.context.active_object
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type='EDGE')
bpy.ops.mesh.select_all(action='SELECT')
before = set(bpy.data.objects)
check("create shape", bpy.ops.maximize.create_shape() == {'FINISHED'})
new = [o for o in bpy.data.objects if o not in before]
check("create shape is a closed spline", len(new) == 1 and new[0].type == 'CURVE' and
      len(new[0].data.splines) == 1 and new[0].data.splines[0].use_cyclic_u and
      len(new[0].data.splines[0].bezier_points) == 4,
      new and new[0].type, new and [len(s.bezier_points) for s in new[0].data.splines])
check("still editing the mesh", bpy.context.mode == 'EDIT_MESH' and bpy.context.edit_object == plane)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_cube_add()
for ident, mode in (("turn", 'EDGE'), ("split", 'EDGE'), ("break_vertex", 'VERT'), ("remove_isolated", 'VERT'),
                    ("hard", 'EDGE'), ("smooth_edges", 'EDGE'), ("select_by_angle", 'FACE')):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type=mode)
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
    seq = {'VERT': bm.verts, 'EDGE': bm.edges, 'FACE': bm.faces}[mode]
    seq.ensure_lookup_table()
    seq[0].select = True
    bm.select_flush_mode()
    bmesh.update_edit_mesh(bpy.context.edit_object.data)
    try:
        r = getattr(bpy.ops.maximize, ident)()
        check("run " + ident, r == {'FINISHED'}, r)
    except Exception as ex:
        check("run " + ident, False, ex)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_plane_add()
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='ONLY_FACE')
bpy.ops.mesh.select_all(action='SELECT')
r = bpy.ops.maximize.create_poly()
bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
check("run create_poly", r == {'FINISHED'} and len(bm.faces) == 1, r, len(bm.faces))
say("DONE")

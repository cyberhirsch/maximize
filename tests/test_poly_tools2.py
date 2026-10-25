# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_poly_tools2.py
# Extrude Along Spline, Hinge From Edge, Insert Vertex, Slice Plane, Named Selections Copy / Paste,
# Crease / Weight, Show Cage, material select by name.
import math
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bmesh
import bpy
from mathutils import Vector

from maximize import poly_tools


def say(*a): print("MXP2", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)


def edit(obj):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    return bmesh.from_edit_mesh(obj.data)


def plane():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_plane_add(size=1)
    return bpy.context.active_object


# Extrude Along Spline: a straight 2 m spline along X; aligned, the plane's face goes 2 m up (+Z).
curve = bpy.data.curves.new("path", 'CURVE')
sp = curve.splines.new('BEZIER')
sp.bezier_points.add(1)
for bp, co in zip(sp.bezier_points, ((0, 0, 0), (2, 0, 0))):
    bp.co = co
    bp.handle_left_type = bp.handle_right_type = 'VECTOR'
path = bpy.data.objects.new("path", curve)
bpy.context.collection.objects.link(path)
obj = plane()
bm = edit(obj)
bpy.ops.mesh.select_mode(type='FACE')
bpy.ops.mesh.select_all(action='SELECT')
r = bpy.ops.maximize.extrude_along_spline(spline="path", segments=4, align=True)
bm = bmesh.from_edit_mesh(obj.data)
zs = sorted({round(v.co.z, 4) for v in bm.verts})
check("extrude along spline", r == {'FINISHED'} and zs == [0.0, 0.5, 1.0, 1.5, 2.0] and len(bm.verts) == 20,
      zs, len(bm.verts), len(bm.faces))
check("extrude along spline is closed", all(e.is_manifold for e in bm.edges if not e.is_boundary) and
      sum(1 for e in bm.edges if e.is_boundary) == 4, sum(1 for e in bm.edges if e.is_boundary))
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_plane_add(size=1)
obj = bpy.context.active_object
bm = edit(obj)
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.maximize.extrude_along_spline(spline="path", segments=2, align=True, taper=-0.5)
bm = bmesh.from_edit_mesh(obj.data)
top = [v for v in bm.verts if abs(v.co.z - 2.0) < 1e-4]
check("taper", len(top) == 4 and all(abs(abs(v.co.x) - 0.25) < 1e-4 for v in top), [tuple(v.co) for v in top])

# Hinge From Edge: the plane's face swings 90° about its -X edge.
obj = plane()
bm = edit(obj)
bpy.ops.mesh.select_all(action='SELECT')
bm.edges.ensure_lookup_table()
hinge_edge = [e for e in bm.edges if all(abs(v.co.x + 0.5) < 1e-6 for v in e.verts)][0]
faces = [f for f in bm.faces if f.select]
poly_tools.hinge(bm, faces, hinge_edge, math.radians(90), 2)
bmesh.update_edit_mesh(obj.data)
top = max(v.co.z for v in bm.verts)
check("hinge from edge", abs(top - 1.0) < 1e-4 and len(bm.verts) == 8, top, len(bm.verts))
bpy.context.view_layer.objects.active = obj

# Insert Vertex.
obj = plane()
bm = edit(obj)
bm.edges.ensure_lookup_table()
v = poly_tools.insert_vertex(bm, bm.edges[0], 0.25)
bmesh.update_edit_mesh(obj.data)
bm.faces.ensure_lookup_table()
check("insert vertex", len(bm.verts) == 5 and len(bm.faces[0].verts) == 5, len(bm.verts))

# Slice Plane, then Split.
obj = plane()
bm = edit(obj)
bpy.ops.mesh.select_all(action='DESELECT')
r = bpy.ops.maximize.slice_plane(plane_co=(0.1, 0, 0), plane_no=(1, 0, 0), split=False)
bm = bmesh.from_edit_mesh(obj.data)
check("slice", r == {'FINISHED'} and len(bm.faces) == 2 and len(bm.verts) == 6, len(bm.faces), len(bm.verts))
obj = plane()
bm = edit(obj)
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.maximize.slice_plane(plane_co=(0.1, 0, 0), plane_no=(1, 0, 0), split=True)
bm = bmesh.from_edit_mesh(obj.data)
check("slice split", len(bm.faces) == 2 and len(bm.verts) == 8, len(bm.verts))

# Named selections: copy a set from one cube, paste into another.
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_cube_add()
a = bpy.context.active_object
bm = edit(a)
bpy.ops.mesh.select_mode(type='FACE')
bpy.ops.mesh.select_all(action='DESELECT')
bm.faces.ensure_lookup_table()
bm.faces[2].select = True
bmesh.update_edit_mesh(a.data)
bpy.ops.maximize.selset_create(name="Lid")
check("copy", bpy.ops.maximize.named_selection_copy(name="Lid") == {'FINISHED'})
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_cube_add(location=(3, 0, 0))
b = bpy.context.active_object
edit(b)
check("paste", bpy.ops.maximize.named_selection_paste() == {'FINISHED'})
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.maximize.selset_select(name="Lid")
bm = bmesh.from_edit_mesh(b.data)
check("pasted set selects", [f.index for f in bm.faces if f.select] == [2])

# Crease / Weight.
bpy.ops.mesh.select_mode(type='EDGE')
bpy.ops.mesh.select_all(action='DESELECT')
bm.edges.ensure_lookup_table()
bm.edges[0].select = True
bmesh.update_edit_mesh(b.data)
bpy.ops.maximize.set_crease_weight(target='EDGE_CREASE', value=0.75)
bpy.ops.maximize.set_crease_weight(target='EDGE_WEIGHT', value=0.5)
bpy.ops.object.mode_set(mode='OBJECT')
crease = b.data.attributes.get("crease_edge")
weight = b.data.attributes.get("bevel_weight_edge")
check("edge crease", crease and abs(crease.data[0].value - 0.75) < 1e-6 and crease.data[1].value == 0.0)
check("edge weight", weight and abs(weight.data[0].value - 0.5) < 1e-6)

# Show Cage.
mod = b.modifiers.new("TurboSmooth", 'SUBSURF')
mod.show_on_cage = True
b.maximize_show_cage = True
check("show cage", b.maximize_show_cage and not mod.show_on_cage)
b.maximize_show_cage = False
check("hide cage", not b.maximize_show_cage and mod.show_on_cage)

# Select by material name.
b.data.materials.append(bpy.data.materials.new("Red"))
b.data.materials.append(bpy.data.materials.new("Blue"))
bm = edit(b)
bpy.ops.mesh.select_mode(type='FACE')
bm.faces.ensure_lookup_table()
bm.faces[4].material_index = 1
bmesh.update_edit_mesh(b.data)
r = bpy.ops.maximize.select_material_name(material='2', clear=True)
bm = bmesh.from_edit_mesh(b.data)
check("select by name", r == {'FINISHED'} and [f.index for f in bm.faces if f.select] == [4])
# Cap: quad grid (default), one n-gon (Ctrl), inset ring + grid (Shift); odd border: one triangle.
def capped(mode, sides=8):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_cylinder_add(vertices=sides, end_fill_type='NOTHING')
    cyl = bpy.context.active_object
    bm = edit(cyl)
    bpy.ops.mesh.select_mode(type='EDGE')
    for e in bm.edges:
        e.select = e.is_boundary and all(v.co.z > 0 for v in e.verts)
    bm.select_flush_mode()
    bmesh.update_edit_mesh(cyl.data)
    before = len(bm.faces)
    r = bpy.ops.maximize.cap(mode=mode)
    bm = bmesh.from_edit_mesh(cyl.data)
    cap = [f for f in bm.faces if all(v.co.z > 0.99 for v in f.verts)]
    open_edges = sum(1 for e in bm.edges if e.is_boundary and all(v.co.z > 0 for v in e.verts))
    return r, len(bm.faces) - before, sorted(len(f.verts) for f in cap), open_edges, len(cyl.data.polygons)


r, new, sizes, open_edges, _ = capped('NGON')
check("cap n-gon", r == {'FINISHED'} and sizes == [8] and open_edges == 0, sizes)
r, new, sizes, open_edges, _ = capped('QUAD')
check("quad cap", r == {'FINISHED'} and new > 1 and set(sizes) == {4} and open_edges == 0, sizes)
r, new, sizes, open_edges, _ = capped('QUAD', sides=9)
check("quad cap odd border", r == {'FINISHED'} and sizes.count(3) == 1 and set(sizes) <= {3, 4} and open_edges == 0, sizes)
r, new, sizes, open_edges, _ = capped('INSET')
check("inset quad cap", r == {'FINISHED'} and set(sizes) == {4} and new >= 8 + 2 and open_edges == 0, new, sizes)
say("DONE")

# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Cap Relax (Seb, 2026-10-31: "can we relax the quad cap a little?"): the quad caps' inner vertices
even out, the rim stays, the cap stays flat, its UVs stay unfolded, an odd Sides keeps its one
triangle, the domes keep their height; Edit Poly's Cap the same, in quad and inset mode.

moritz --factory-startup -b --python tests/test_cap_relax.py
    MX_SHOT=<folder>: top views of the Cylinder cap at Sides 32/48, Cap Segments 1/3, Relax 0/0.5/1
"""

import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import primitives  # noqa: E402

failures = []


def check(name, ok, *info):
    print("MXCR", "OK" if ok else "FAIL", name, *info, flush=True)
    if not ok:
        failures.append(name)


def make(kind, **params):
    obj = primitives._create_object(bpy.context, kind, Matrix())
    for name, value in params.items():
        primitives.parameter(obj, name).value = value
    obj.update_tag()
    bpy.context.view_layer.update()
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    bm = bmesh.new()
    bm.from_mesh(ev.to_mesh())
    ev.to_mesh_clear()
    bpy.data.objects.remove(obj)
    return bm


def top_cap(bm):
    """The top cap's faces (all at the top height) and its rim vertices."""
    top = max(v.co.z for v in bm.verts)
    faces = [f for f in bm.faces if all(abs(v.co.z - top) < 1e-4 for v in f.verts)]
    face_set = set(faces)
    rim = {v for f in faces for e in f.edges for v in e.verts
           if sum(1 for g in e.link_faces if g in face_set) == 1}
    return faces, rim


def evenness(faces, rim):
    """(rim quad depth / inner edge, largest / smallest face area, spread of the inner edges'
    lengths: their standard deviation over their mean)."""
    edges = {e for f in faces for e in f.edges}
    spokes = [e.calc_length() for e in edges if (e.verts[0] in rim) != (e.verts[1] in rim)]
    inner = np.array([e.calc_length() for e in edges if e.verts[0] not in rim and e.verts[1] not in rim])
    areas = [f.calc_area() for f in faces]
    if not len(inner):
        return None, max(areas) / min(areas), 0.0
    return sum(spokes) / len(spokes) / inner.mean(), max(areas) / min(areas), inner.std() / inner.mean()


def uv_folds(bm, faces):
    """Faces whose UVs wind the other way from the rest (a fold), and UVs outside the cap's circle."""
    uv = bm.loops.layers.uv["UVMap"]
    signs = []
    for f in faces:
        pts = [l[uv].uv for l in f.loops]
        signs.append(sum(a.x * b.y - b.x * a.y for a, b in zip(pts, pts[1:] + pts[:1])))
    major = 1 if sum(s > 0 for s in signs) >= len(signs) / 2 else -1
    return sum(1 for s in signs if s * major <= 0)


def draw(faces, path, size=700):
    img = np.ones((size, size, 4), np.float32)
    verts = {v for f in faces for v in f.verts}
    r = max(max(abs(v.co.x), abs(v.co.y)) for v in verts) * 1.04

    def px(co):
        return ((co.x / r) * 0.5 + 0.5) * (size - 1), ((co.y / r) * 0.5 + 0.5) * (size - 1)
    for e in {e for f in faces for e in f.edges}:
        (x0, y0), (x1, y1) = px(e.verts[0].co), px(e.verts[1].co)
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        img[np.linspace(y0, y1, n).round().astype(int), np.linspace(x0, x1, n).round().astype(int), :3] = 0.0
    im = bpy.data.images.new("cap", size, size)
    im.pixels.foreach_set(img.ravel())
    im.filepath_raw = path
    im.file_format = 'PNG'
    im.save()
    bpy.data.images.remove(im)


SHOT = os.environ.get("MX_SHOT")

# The primitives' Quad Cap.
for sides, segs in ((32, 1), (32, 3), (48, 1), (48, 3), (7, 1), (10, 2), (5, 1)):
    caps = {}
    for relax in (0.0, 0.5, 1.0):
        bm = make('CYLINDER', **{"Sides": sides, "Cap Segments": segs, "Cap Relax": relax})
        faces, rim = top_cap(bm)
        caps[relax] = (bm, faces, rim)
        if SHOT:
            draw(faces, os.path.join(SHOT, "cap_s{}_c{}_relax{}.png".format(sides, segs, int(relax * 100))))
    label = "Cylinder Sides {} Cap Segs {}".format(sides, segs)
    (bm0, f0, rim0), (bm5, f5, rim5), (bm1, f1, rim1) = caps[0.0], caps[0.5], caps[1.0]
    check(label + ": same faces", [len(f.verts) for f in f0] == [len(f.verts) for f in f1],
          len(f0), len(f1))
    check(label + ": one triangle per cap when Sides is odd",
          sum(len(f.verts) == 3 for f in f1) == sides % 2, sum(len(f.verts) == 3 for f in f1))
    rim_moved = max(min((v.co - w.co).length for w in rim0) for v in rim1)
    check(label + ": the rim stays", len(rim0) == len(rim1) == sides and rim_moved < 1e-5, rim_moved)
    zs = [v.co.z for f in f1 for v in f.verts]
    check(label + ": the cap stays flat", max(zs) - min(zs) < 1e-5)
    check(label + ": faces still point up", all(f.normal.z > 0.99 for f in f1))
    check(label + ": no folded UVs", uv_folds(bm1, f1) == 0 and uv_folds(bm5, f5) == 0)
    inner0 = sorted(tuple(round(c, 5) for c in v.co) for f in f0 for v in f.verts if v not in rim0)
    inner5 = sorted(tuple(round(c, 5) for c in v.co) for f in f5 for v in f.verts if v not in rim5)
    if sides >= 16:
        e0, e5, e1 = (evenness(c[1], c[2]) for c in (caps[0.0], caps[0.5], caps[1.0]))
        check(label + ": the inside moves at 0.5", inner0 != inner5)
        check(label + ": cell areas are more even at the default 0.5", e5[1] < e0[1],
              "{:.2f} -> {:.2f}".format(e0[1], e5[1]))
        check(label + ": the outer ring is about one cell deep", 0.8 < e5[0] < 1.4 and 0.8 < e1[0] < 1.4,
              "{:.2f} {:.2f}".format(e5[0], e1[0]))
    for c in caps.values():
        c[0].free()

# The quad poles and cones keep their height, relaxed too.
for kind, params, height in (('SPHERE', {"Segments": 32}, 1.0), ('SPHERE', {"Segments": 27}, 1.0),
                             ('CAPSULE', {"Sides": 24}, 2.0), ('OILTANK', {"Sides": 30}, 2.0),
                             ('SPINDLE', {"Sides": 24, "Cap Segs": 3}, 2.0),
                             ('CHAMFERCYL', {"Sides": 32, "Cap Segs": 2}, 1.0),
                             ('GENGON', {"Sides": 9, "Cap Segs": 2}, 1.0)):
    for relax in (0.0, 1.0):
        bm = make(kind, **params, **{"Cap Relax": relax})
        zs = [v.co.z for v in bm.verts]
        sizes = [len(f.verts) for f in bm.faces]
        open_edges = sum(1 for e in bm.edges if not e.is_manifold)
        check("{} {} relax {}: height, closed, no n-gons".format(kind, params, relax),
              abs(max(zs) - min(zs) - height) < 1e-3 and open_edges == 0 and max(sizes) == 4 and
              bm.calc_volume(signed=True) > 0, round(max(zs) - min(zs), 4), open_edges, max(sizes))
        bm.free()

# Edit Poly's Cap.
def cap(mode, sides, relax):
    bpy.ops.object.mode_set(mode='OBJECT') if bpy.context.object and bpy.context.object.mode != 'OBJECT' else None
    bpy.ops.mesh.primitive_cylinder_add(vertices=sides, end_fill_type='NOTHING')
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='EDGE')
    bm = bmesh.from_edit_mesh(obj.data)
    border = []
    for e in bm.edges:
        e.select = e.is_boundary and all(v.co.z > 0 for v in e.verts)
        if e.select:
            border += [v.co.copy() for v in e.verts]
    bm.select_flush_mode()
    bmesh.update_edit_mesh(obj.data)
    r = bpy.ops.maximize.cap(mode=mode, relax=relax)
    bm = bmesh.from_edit_mesh(obj.data)
    faces = [f for f in bm.faces if all(abs(v.co.z - 1.0) < 1e-4 for v in f.verts)]
    rim = {v for v in bm.verts if any((v.co - b).length < 1e-6 for b in border)}
    out = (r, faces and [len(f.verts) for f in faces], max(abs(v.co.z - 1.0) for f in faces for v in f.verts) if faces else 1,
           sum(1 for e in bm.edges if e.is_boundary and all(v.co.z > 0 for v in e.verts)),
           evenness(faces, rim) if faces else None, sorted(tuple(round(c, 4) for c in v.co) for v in rim))
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects.remove(obj)
    return out


for mode, sides in (('QUAD', 32), ('QUAD', 9), ('INSET', 32), ('INSET', 24)):
    r0, s0, flat0, open0, even0, rim0 = cap(mode, sides, 0.0)
    r1, s1, flat1, open1, even1, rim1 = cap(mode, sides, 1.0)
    label = "Edit Poly Cap {} {}".format(mode, sides)
    check(label + ": capped, same faces", r1 == {'FINISHED'} and sorted(s0) == sorted(s1) and open1 == 0, len(s1), open1)
    check(label + ": the border stays, the cap stays flat", rim0 == rim1 and len(rim1) == sides and flat1 < 1e-5,
          flat1, len(rim0), len(rim1))
    check(label + ": the grid evens out", even1[2] <= even0[2] + 1e-9,
          "{:.3f} -> {:.3f}".format(even0[2], even1[2]))

print("MXCR FAILURES", len(failures), failures, flush=True)

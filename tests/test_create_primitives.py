# Run: moritz.exe --factory-startup -b --python tests/test_create_primitives.py
# Every Standard and Extended Primitive builds, evaluates to sane, outward-facing geometry, and
# has the inputs its drag steps and Keyboard Entry set.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bmesh
import bpy
from mathutils import Matrix, Vector

from maximize import primitives


def say(*a): print("MXCREATE", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


ctx = bpy.context
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob)

kinds = primitives.STANDARD_PRIMITIVES + primitives.EXTENDED_PRIMITIVES
for kind in kinds:
    try:
        ob = primitives._create_object(ctx, kind, Matrix())
    except Exception as ex:
        check(kind, False, "create", repr(ex))
        continue
    ctx.view_layer.update()
    ev = ob.evaluated_get(ctx.evaluated_depsgraph_get())
    me = ev.to_mesh()
    verts = len(me.vertices)
    co = [v.co.copy() for v in me.vertices]
    finite = all(c.x == c.x and abs(c.x) < 1e6 and abs(c.y) < 1e6 and abs(c.z) < 1e6 for c in co)
    size = Vector((max(c[i] for c in co) - min(c[i] for c in co) for i in range(3))) if co else Vector()
    bm = bmesh.new()
    bm.from_mesh(me)
    open_edges = sum(1 for e in bm.edges if not e.is_manifold)
    # Outward: faces point away from the center of the bounding box on average.
    center = sum(co, Vector()) / max(len(co), 1)
    outward = sum((f.calc_center_median() - center).dot(f.normal) * f.calc_area() for f in bm.faces)
    bm.free()
    ev.to_mesh_clear()
    missing = [n for n in primitives.first_step_inputs(kind) if not primitives._has_input(ob, n)]
    flat = kind in {'PLANE', 'RINGWAVE'}
    grounded = kind in {'SPHERE', 'GEOSPHERE', 'TORUS', 'HEDRA', 'TORUS_KNOT'} or abs(min(c.z for c in co)) < 1e-4
    ok = grounded and verts > 0 and finite and not missing and (flat or min(size) > 1e-4) and (flat or outward > 0)
    check(kind, ok, "verts", verts, "size", tuple(round(s, 3) for s in size), "zmin", round(min(c.z for c in co), 3) if co else None, "open", open_edges,
          "outward", round(outward, 4), "missing", missing)
    say("INPUTS", kind, [s.name for s in primitives.primitive_modifier(ob).node_group.interface.items_tree
                         if s.item_type == 'SOCKET' and s.in_out == 'INPUT'])

# The teapot's parts switch off one by one.
pot = primitives._create_object(ctx, 'TEAPOT', Matrix())
counts = {}
for part in ("", "Lid", "Spout", "Handle"):
    if part:
        primitives.modifier_input(primitives.primitive_modifier(pot), part).value = False
    pot.update_tag()
    ctx.view_layer.update()
    counts[part or "all"] = len(pot.evaluated_get(ctx.evaluated_depsgraph_get()).data.vertices)
check("teapot parts", list(counts.values()) == sorted(counts.values(), reverse=True)
      and len(set(counts.values())) == 4, counts)
# Extended Splines: closed outlines of the right size, centered, with the walls' thickness.
from maximize import shapes
expected = {'WRECTANGLE': (2, 8), 'CHANNEL': (1, 8), 'ANGLE': (1, 6), 'TEE': (1, 8), 'WIDE_FLANGE': (1, 12)}
for kind in shapes.EXTENDED_SPLINES:
    ob = primitives._create_object(ctx, kind, Matrix())
    primitives.parameter(ob, "Width").value = 2.0
    primitives.parameter(ob, "Thickness").value = 0.2
    splines = ob.data.splines
    knots = [p.co for sp in splines for p in sp.bezier_points]
    xs, ys = [c.x for c in knots], [c.y for c in knots]
    ok = ((len(splines), sum(len(sp.bezier_points) for sp in splines)) == expected[kind]
          and all(sp.use_cyclic_u for sp in splines)
          and abs(min(xs) + 1) < 1e-6 and abs(max(xs) - 1) < 1e-6 and abs(min(ys) + 0.5) < 1e-6
          and abs(max(ys) - 0.5) < 1e-6)
    check(kind, ok, ob.name, len(splines), len(knots))
    # Rounded corners add knots.
    for name in ("Corner Radius 1", "Corner Radius"):
        if primitives._has_input(ob, name):
            primitives.parameter(ob, name).value = 0.1
    check(kind + " fillets", sum(len(sp.bezier_points) for sp in ob.data.splines) > len(knots))

# Text and TextPlus.
bpy.ops.maximize.add_text()
bpy.ops.maximize.add_text(plus=True)
t, tp = bpy.data.objects.get("Text001"), bpy.data.objects.get("TextPlus001")
check("text", t is not None and t.data.fill_mode == 'NONE' and tp is not None and tp.data.fill_mode == 'BOTH')
say("DONE")

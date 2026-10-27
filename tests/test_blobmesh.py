# Run: moritz.exe --factory-startup -b --python tests/test_blobmesh.py
# Max's BlobMesh (Compound Objects): blobs on the Blob Objects' vertices, blending by Tension,
# Mesh Volume, Off in Viewport, Add / Remove.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy

from maximize import compound, primitives


def say(*a): print("MXBLOB", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


ctx = bpy.context
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(3, 0, 0))
cube = ctx.object
bpy.ops.maximize.add_blobmesh()
blob = ctx.object
check("created", blob.name == "BlobMesh001" and compound.is_blobmesh(blob), blob.name)
check("selected became blob objects", cube.name in compound.blob_collection(blob).objects)
check("base label", primitives.base_entry(blob)[1] == "BlobMesh")


def evaluate():
    blob.update_tag()
    ctx.view_layer.update()
    me = blob.evaluated_get(ctx.evaluated_depsgraph_get()).data
    co = [v.co.copy() for v in me.vertices]
    if not co:
        return 0, None, None
    lo = [min(c[i] for c in co) for i in range(3)]
    hi = [max(c[i] for c in co) for i in range(3)]
    return len(co), lo, hi


def param(name, value):
    primitives.parameter(blob, name).value = value


# Background mode counts as render: Render Coarseness.
n, lo, hi = evaluate()
# Eight blobs of Size 0.2 on the cube corners at 3 +- 0.5: from 2.4 to 3.6 in X.
check("blobs on vertices", n > 0 and abs(lo[0] - 2.4) < 0.05 and abs(hi[0] - 3.6) < 0.05, n, lo, hi)
param("Size", 1.2)
n_apart, _lo, _hi = evaluate()
param("Tension", 0.0)
n_blend, lo, hi = evaluate()
check("tension blends", n_blend != n_apart, n_apart, n_blend)
param("Tension", 1.0)
param("Size", 0.2)
param("Mesh Volume", True)
n, lo, hi = evaluate()
check("mesh volume", n > 0 and abs(lo[0] - 2.5) < 0.05 and abs(hi[0] - 3.5) < 0.05, n, lo, hi)
param("Mesh Volume", False)
param("Resample Faces", 50.0)
n2, _lo, _hi = evaluate()
check("resample adds blobs", n2 > n, n, n2)
param("Smoothing", 2)
param("Adaptive", 0.5)
n3, _lo, _hi = evaluate()
check("adaptive", 0 < n3 < n2, n2, n3)

with ctx.temp_override(object=blob, active_object=blob):
    bpy.ops.maximize.blob_objects_remove(name=cube.name)
check("remove", evaluate()[0] == 0)
blob.select_set(True)
cube.select_set(True)
ctx.view_layer.objects.active = blob
bpy.ops.maximize.blob_objects_add()
check("add", cube.name in compound.blob_collection(blob).objects and evaluate()[0] > 0)
say("DONE")

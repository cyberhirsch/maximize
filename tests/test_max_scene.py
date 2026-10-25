# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_max_scene.py
# Import a .mxscene as written by max_side/moritz_export.ms: units, hierarchy, pivots, polygons,
# UVs, Multi/Sub material IDs, smoothing groups, layers, frozen/hidden, camera, lights, and the
# V-Ray / Corona / Physical / Standard material conversion.
import json
import math
import os
import sys
import tempfile

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy

from maximize import max_scene


def say(*a): print("MXMS", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


def tm(x=0, y=0, z=0, rot_z=0.0):
    c, s = math.cos(rot_z), math.sin(rot_z)
    return [[c, s, 0], [-s, c, 0], [0, 0, 1], [x, y, z]]


bitmap = {"class": "Bitmaptexture", "name": "Map #1", "file": "C:/maps/wood.jpg",
          "params": {"filename": "C:/maps/wood.jpg"}}
scene = {
    "format": "mxscene", "version": 1, "max_version": 26000,
    "units_per_cm": 1.0,  # system unit: centimeters
    "nodes": [
        {"name": "Box001", "class": "Box", "kind": "MESH", "parent": None,
         "transform": tm(100, 0, 0, math.radians(90)), "layer": "Furniture",
         "hidden": False, "frozen": True, "wirecolor": [0.5, 0.2, 0.1], "renderable": True,
         "material": 0,
         "mesh": {
             # A 100 cm quad box, pivot at the bottom center (in node space).
             "verts": [[-50, -50, 0], [50, -50, 0], [50, 50, 0], [-50, 50, 0],
                       [-50, -50, 100], [50, -50, 100], [50, 50, 100], [-50, 50, 100]],
             "faces": [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]],
             "mat_ids": [1, 2, 3, 3, 3, 3],
             "smoothing": [1, 2, 4, 8, 16, 2147483648],
             "uv_verts": [[0, 0], [1, 0], [1, 1], [0, 1]],
             "uv_faces": [[0, 1, 2, 3]] * 6}},
        {"name": "Child", "class": "Dummy", "kind": "EMPTY", "parent": "Box001",
         "transform": tm(100, 0, 200), "layer": "Furniture", "hidden": True, "frozen": False,
         "wirecolor": [1, 1, 1], "renderable": True},
        {"name": "Camera001", "class": "Targetcamera", "kind": "CAMERA", "parent": None,
         "transform": tm(0, -500, 150), "layer": "0", "hidden": False, "frozen": False,
         "wirecolor": [0, 0, 1], "renderable": True, "fov": 60.0, "target": "Box001"},
        {"name": "VRayLight001", "class": "VRayLight", "kind": "LIGHT", "parent": None,
         "transform": tm(0, 0, 300), "layer": "0", "hidden": False, "frozen": False,
         "wirecolor": [1, 1, 0], "renderable": True,
         "light": {"type": 0, "size0": 50.0, "size1": 25.0, "color": [1.0, 0.9, 0.8]}},
    ],
    "materials": [
        {"class": "Multimaterial", "name": "Multi", "sub": [
            {"id": 1, "material": 1}, {"id": 2, "material": 2}, {"id": 3, "material": 3}],
         "params": {}},
        {"class": "VRayMtl", "name": "Wood", "params": {
            "diffuse": [0.6, 0.4, 0.2], "texmap_diffuse": bitmap, "reflection": [0.5, 0.5, 0.5],
            "reflection_glossiness": 0.7, "reflection_fresnel": True, "reflection_ior": 1.6,
            "brdf_useRoughness": False, "refraction": [0, 0, 0],
            "texmap_bump": {"class": "VRayNormalMap", "name": "N", "params": {
                "normal_map": {"class": "Bitmaptexture", "name": "n", "file": "C:/maps/wood_n.png", "params": {}}}},
            "texmap_bump_multiplier": 30.0}},
        {"class": "CoronaPhysicalMtl", "name": "Chrome", "params": {
            "baseColor": [0.9, 0.9, 0.9], "baseLevel": 1.0, "baseRoughness": 0.1,
            "roughnessMode": 0, "metalnessMode": 1, "baseIor": 1.5}},
        {"class": "PhysicalMaterial", "name": "Glass", "params": {
            "base_color": [1, 1, 1], "roughness": 0.0, "roughness_inv": False,
            "metalness": 0.0, "transparency": 1.0, "trans_ior": 1.52}},
    ],
}

path = os.path.join(tempfile.gettempdir(), "moritz_test.mxscene")
with open(path, "w", encoding="utf-8") as f:
    json.dump(scene, f)

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
result = bpy.ops.maximize.import_mxscene(filepath=path)
check("operator", result == {'FINISHED'}, result)

box = bpy.data.objects["Box001"]
me = box.data
check("polygons", len(me.polygons) == 6 and all(p.loop_total == 4 for p in me.polygons))
# 100 cm box, 1 unit = 1 cm: 1 m wide, pivot at the bottom, 1 m along X, turned 90 degrees.
dims = tuple(round(d, 4) for d in box.dimensions)
check("units", dims == (1.0, 1.0, 1.0), dims)
check("pivot and transform", abs(box.matrix_world.translation.x - 1.0) < 1e-6 and abs(box.rotation_euler.z - math.radians(90)) < 1e-5,
      tuple(round(c, 3) for c in box.matrix_world.translation), round(math.degrees(box.rotation_euler.z), 2))
check("uv", "UVMap" in me.uv_layers and tuple(round(c, 3) for c in me.uv_layers["UVMap"].data[2].uv) == (1.0, 1.0))
check("material slots", [m.name for m in me.materials] == ["Wood", "Chrome", "Glass"],
      [m.name if m else None for m in me.materials])
check("material ids", [p.material_index for p in me.polygons] == [0, 1, 2, 2, 2, 2],
      [p.material_index for p in me.polygons])
sharp = me.attributes.get("sharp_edge")
nsharp = sum(1 for v in sharp.data if v.value) if sharp else 0
check("smoothing groups", nsharp == 12 and "smoothing_groups" in me.attributes, nsharp)
check("frozen", box.hide_select)
child = bpy.data.objects["Child"]
check("hierarchy", child.parent == box and abs(child.matrix_world.translation.z - 2.0) < 1e-6 and child.hide_get(),
      tuple(round(c, 3) for c in child.matrix_world.translation))
check("layer collection", box.users_collection[0].name == "Furniture")
cam = bpy.data.objects["Camera001"]
check("camera", abs(math.degrees(cam.data.angle) - 60) < 1e-4 and cam.constraints and cam.constraints[0].target == box)
light = bpy.data.objects["VRayLight001"].data
check("area light", light.type == 'AREA' and abs(light.size - 1.0) < 1e-6 and abs(light.size_y - 0.5) < 1e-6,
      light.type, light.size, light.size_y)


def bsdf(mat):
    return next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')


wood = bpy.data.materials["Wood"]
b = bsdf(wood)
check("vray glossiness to roughness", abs(b.inputs["Roughness"].default_value - 0.3) < 1e-5,
      round(b.inputs["Roughness"].default_value, 3))
check("vray diffuse map", b.inputs["Base Color"].is_linked and
      b.inputs["Base Color"].links[0].from_node.image.filepath == "C:/maps/wood.jpg")
check("vray normal map", b.inputs["Normal"].is_linked and
      b.inputs["Normal"].links[0].from_node.type == 'NORMAL_MAP')
check("vray ior", abs(b.inputs["IOR"].default_value - 1.6) < 1e-5)
chrome = bsdf(bpy.data.materials["Chrome"])
check("corona metal", chrome.inputs["Metallic"].default_value == 1.0 and
      abs(chrome.inputs["Roughness"].default_value - 0.1) < 1e-5)
glass = bsdf(bpy.data.materials["Glass"])
check("physical glass", glass.inputs["Transmission Weight"].default_value == 1.0 and
      abs(glass.inputs["IOR"].default_value - 1.52) < 1e-5)
check("exporter shipped", os.path.isfile(max_scene.EXPORTER))
os.remove(path)

# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Camera Map Per Pixel: an image projected from the camera renders back as the same image.

moritz --factory-startup -b --python tests/test_camera_map.py
"""

import os
import sys
import tempfile

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import camera_map  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


W, H = 32, 18
scene = bpy.context.scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)

# An image whose red is u and green is v.
image = bpy.data.images.new("ramp", W, H, float_buffer=True)
image.colorspace_settings.name = 'Non-Color'
pixels = []
for y in range(H):
    for x in range(W):
        pixels += [(x + 0.5) / W, (y + 0.5) / H, 0.0, 1.0]
image.pixels = pixels

cam_data = bpy.data.cameras.new("Cam")
cam_data.lens = 35.0
cam_data.shift_x = 0.1
cam_data.shift_y = -0.05
camera = bpy.data.objects.new("Cam", cam_data)
scene.collection.objects.link(camera)
camera.location = (0.3, -6.0, 1.0)
camera.rotation_euler = (1.45, 0.0, 0.1)
scene.camera = camera

# A wall far behind, larger than the view.
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 20, 0), rotation=(1.5708, 0, 0))
wall = bpy.context.active_object
mat = bpy.data.materials.new("Wall")
wall.data.materials.append(mat)
camera_map.add_camera_map(mat, camera, scene, image)
tree = mat.node_tree
tex = next(n for n in tree.nodes if n.type == 'TEX_IMAGE')
tex.interpolation = 'Closest'
out = next(n for n in tree.nodes if n.type == 'OUTPUT_MATERIAL')
emit = tree.nodes.new('ShaderNodeEmission')
tree.links.new(tex.outputs["Color"], emit.inputs["Color"])
tree.links.new(emit.outputs[0], out.inputs["Surface"])
check(tree.animation_data is not None and len(tree.animation_data.drivers) == 5, "Drivers for lens, sensor, shift, aspect")

scene.render.engine = 'CYCLES'
scene.cycles.samples = 1
scene.cycles.use_denoising = False
scene.cycles.pixel_filter_type = 'BOX'
scene.cycles.filter_width = 0.01
scene.render.resolution_x, scene.render.resolution_y = W, H
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Standard'
scene.render.image_settings.file_format = 'OPEN_EXR'
path = os.path.join(tempfile.gettempdir(), "mx_camera_map.exr")
scene.render.filepath = path
bpy.ops.render.render(write_still=True)
result = bpy.data.images.load(path)
rendered = list(result.pixels)
worst = 0.0
for i in range(W * H):
    worst = max(worst, abs(rendered[4 * i] - pixels[4 * i]), abs(rendered[4 * i + 1] - pixels[4 * i + 1]))
print("worst difference", worst)
check(worst < 0.5 / W, "Rendered from the camera, the projection matches the image pixel for pixel")

print("FAILURES", len(failures))
if failures:
    sys.exit(1)

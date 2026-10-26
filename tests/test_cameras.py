# Run: moritz.exe --factory-startup -b --python tests/test_cameras.py
# Max's cameras: target camera, Lock Camera, tilt correction, the Point-of-View menu and its V key.
import math
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Vector

from maximize import cameras


def say(*a): print("MXCAM", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


ctx = bpy.context
cam, goal = cameras.make_target_camera(ctx, Vector((0, -10, 2)), Vector((0, 0, 5)))
check("target camera", cam.constraints[0].target == goal and goal.location.z == 5)
ctx.view_layer.update()
forward = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
check("looks at the target", forward.angle((goal.location - cam.location)) < 1e-3)

cameras.MAXIMIZE_OT_lock_camera.execute(type("Op", (), {})(), type("C", (), {
    "space_data": None, "scene": ctx.scene})())
check("lock camera", cameras.camera_locked(ctx.scene.camera))

cam.constraints[0].enabled = False
cam.lock_rotation = (False, False, False)
pitch = cameras.tilt_correct(cam)
ctx.view_layer.update()
forward = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
check("levelled", abs(forward.z) < 1e-6, tuple(forward))
want = cam.data.lens * math.tan(pitch) / cam.data.sensor_width
check("shift keeps framing", pitch > 0 and abs(cam.data.shift_y - want) < 1e-6, cam.data.shift_y)

check("menu", hasattr(bpy.types, "MAXIMIZE_MT_point_of_view"))
check("target found", cameras.camera_target(cam) == goal)
check("navigation buttons", "bl_rna" in cameras.MAXIMIZE_GGT_camera_navigation.__dict__ and
      hasattr(bpy.types, "MAXIMIZE_OT_camera_dolly"))
bpy.ops.preferences.keyconfig_activate(filepath=bpy.utils.preset_find("Moritz", "keyconfig"))
kc = ctx.window_manager.keyconfigs.active
has_v = any(k.idname == "wm.call_menu" and k.type == 'V' and not k.ctrl and
            k.properties.name == "MAXIMIZE_MT_point_of_view" for k in kc.keymaps["3D View"].keymap_items)
has_dbl = any(k.idname == "maximize.outliner_select_children" and k.value == 'DOUBLE_CLICK'
              for k in kc.keymaps["Outliner"].keymap_items)
check("outliner double-click", has_dbl)
check("V opens Point of View", has_v)
say("DONE")

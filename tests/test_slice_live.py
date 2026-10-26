# Run: moritz.exe --factory-startup -b --python tests/test_slice_live.py
# Live Slice Plane (gizmo props, Slice), Show Cage colors in the preferences.
import os, sys, addon_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)
import bpy, math
def check(n, ok, *i): print("MXSL", "OK" if ok else "FAIL", n, *i, flush=True)
ctx = bpy.context
cube = bpy.data.objects["Cube"]
cube.location = (0, 0, 1)
ctx.view_layer.objects.active = cube
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
wm = ctx.window_manager
bpy.ops.maximize.slice_plane_mode(action='TOGGLE')
check("active", wm.maximize_slice_active and abs(wm.maximize_slice_location[2] - 1.0) < 1e-5, tuple(wm.maximize_slice_location))
wm.maximize_slice_rotation = (math.radians(90), 0, 0)
n = len(cube.data.vertices)
r = bpy.ops.maximize.slice_plane_mode(action='SLICE')
bpy.ops.object.mode_set(mode='OBJECT')
check("sliced", r == {'FINISHED'} and len(cube.data.vertices) == n + 4, len(cube.data.vertices))
check("cut is vertical", sum(1 for v in cube.data.vertices if abs(v.co.y) < 1e-5) == 4)
prefs = ctx.preferences.addons["maximize"].preferences
check("cage colors", len(prefs.cage_color) == 3 and len(prefs.cage_selected_color) == 3)
print("MXSL DONE")

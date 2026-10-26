# Run: moritz.exe --factory-startup -b --python tests/test_caddy.py
# Max's caddy: the preference, the settings buttons, running a tool with its last values, the
# values snapshot the live redo watches. (The popup and Undo and Redo need a window: GUI only.)
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bmesh
import bpy

from maximize import caddy
from maximize.preferences import get_prefs


def say(*a): print("MXCADDY", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


ctx = bpy.context
prefs = get_prefs()
check("default is Blender's panel", prefs.tool_settings_style == 'PANEL' and not caddy.use_caddy(ctx))
prefs.tool_settings_style = 'CADDY'
check("caddy selectable", caddy.use_caddy(ctx))
check("settings: Connect", caddy.has_settings("maximize.connect"))
check("settings: Chamfer through Bevel", caddy.has_settings("maximize.chamfer"))
check("no settings: Flip", not caddy.has_settings("maximize.flip"))

for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob)
bpy.ops.mesh.primitive_cube_add()
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type='FACE')
bpy.ops.mesh.select_all(action='SELECT')
before = caddy.vertex_count(ctx)
check("vertex count", before == 8, before)
bpy.ops.mesh.select_mode(type='EDGE')
ctx.window_manager.operator_properties_last("mesh.bevel").offset = 0.1
result = caddy.run_tool(ctx, "maximize.chamfer")
after = caddy.vertex_count(ctx)
check("last values", caddy.last_values("mesh.bevel").get("offset") is not None)
check("chamfer runs as bevel", 'FINISHED' in result and after > before, result, after)
# Background mode registers no operations; the snapshot reads any operator's properties.
op = type("Op", (), {"properties": ctx.window_manager.operator_properties_last("mesh.bevel")})()
snap = caddy.snapshot(op)
check("values snapshot", abs(snap["offset"] - 0.1) < 1e-6, snap.get("offset"))

# The rollout draws a settings button per tool in caddy mode.
class Layout:
    def __init__(self):
        self.ops = []

    def row(self, **_k):
        return self

    def operator(self, idname, **_k):
        self.ops.append(idname)
        return type("P", (), {})()


lay = Layout()
caddy.tool_button(lay, ctx, "maximize.connect")
check("settings button", lay.ops == ["maximize.connect", "maximize.caddy_run"], lay.ops)
prefs.tool_settings_style = 'PANEL'
lay = Layout()
caddy.tool_button(lay, ctx, "maximize.connect")
check("panel mode: tool only", lay.ops == ["maximize.connect"], lay.ops)
say("DONE")

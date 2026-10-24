# Run: moritz.exe (or blender.exe) --factory-startup -b --python tests/test_keymaps.py
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

import bpy
for name in ("Max", "Moritz"):
    bpy.ops.preferences.keyconfig_activate(filepath=bpy.utils.preset_find(name, "keyconfig"))
    kc = bpy.context.window_manager.keyconfigs.active
    def find(km, idname, value, **mods):
        for it in kc.keymaps[km].keymap_items:
            if it.idname == idname and it.type == 'LEFTMOUSE' and it.value == value and \
                    all(getattr(it, m) == v for m, v in mods.items()):
                return it
    ctrl = find("3D View", "view3d.select", 'CLICK', ctrl=True, shift=False, alt=False)
    print("MXKM", name, kc.name,
          "ctrl-click toggle", ctrl.properties.toggle, "extend", ctrl.properties.extend,
          "| dbl loop", bool(find("Mesh", "mesh.loop_select", 'DOUBLE_CLICK', ctrl=False)),
          "| ring", bool(find("Mesh", "mesh.edgering_select", 'DOUBLE_CLICK', ctrl=True, alt=True)),
          "| path", bool(find("Mesh", "mesh.shortest_path_pick", 'CLICK', ctrl=True, shift=True)),
          "| children", bool(find("Object Mode", "object.select_grouped", 'DOUBLE_CLICK')))
import maximize.preferences as p
print("MXKM enum", [k[0] for k in p.KEYMAPS])

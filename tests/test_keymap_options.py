# Run: moritz.exe --factory-startup -b --python tests/test_keymap_options.py
# Keymap preferences (Maya navigation, F frames selection, Blender modal keys), numpad views,
# editor keys and Moritz's region select binding.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)
import bpy


def say(*a): print("MXOPT", " ".join(str(x) for x in a), flush=True)


def find(kc, km, idname, type, value='PRESS', **mods):
    for it in kc.keymaps[km].keymap_items:
        if it.idname == idname and it.type == type and it.value == value and \
                all(getattr(it, m) == v for m, v in mods.items()):
            return it


bpy.ops.preferences.keyconfig_activate(filepath=bpy.utils.preset_find("Moritz", "keyconfig"))
kc = bpy.context.window_manager.keyconfigs.active
say("numpad 1", bool(find(kc, "3D View", "view3d.view_axis", 'NUMPAD_1', ctrl=False)),
    "numpad 5", bool(find(kc, "3D View", "view3d.view_persportho", 'NUMPAD_5')))
say("region select", bool(find(kc, "3D View Tool: Select Box", "maximize.select_region", 'LEFTMOUSE', 'CLICK_DRAG')))
say("outliner F2", bool(find(kc, "Outliner", "outliner.item_rename", 'F2')),
    "graph K", bool(find(kc, "Graph Editor", "graph.keyframe_insert", 'K')),
    "node ctrl+D none", find(kc, "Node Editor", "node.select_all", 'D', ctrl=True).properties.action)
say("F before", find(kc, "3D View", "view3d.view_axis", 'F', ctrl=False) is not None)
kc.preferences.use_f_frames_selection = True
kc.preferences.use_maya_navigation = True
kc.preferences.use_blender_modal_keys = True
kc = bpy.context.window_manager.keyconfigs.active
say("F frames", bool(find(kc, "3D View", "view3d.view_selected", 'F', ctrl=False)),
    "ctrl F front", bool(find(kc, "3D View", "view3d.view_axis", 'F', ctrl=True)))
say("alt LMB orbit", bool(find(kc, "3D View", "view3d.rotate", 'LEFTMOUSE', alt=True)),
    "shift click toggle", find(kc, "3D View", "view3d.select", 'LEFTMOUSE', 'CLICK', shift=True, ctrl=False).properties.toggle)
say("ctrl+shift+G", bool(find(kc, "Object Mode", "transform.translate", 'G', ctrl=True, shift=True)))

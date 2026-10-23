# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The Max and Moritz keymaps as keyconfig presets.

Blender lists keymaps from preset files, so the add-on writes two small loaders into the user's
`presets/keyconfig` folder while it is enabled and removes them when it is disabled. The key data
lives in `keymap_max.py`.
"""

import importlib
import os

import bpy

NAMES = ("Moritz", "Max")

_LOADER = '''\
# Written by the Maximize add-on: the {name} keymap. Removed when the add-on is disabled.
import importlib
importlib.import_module("{package}.keymaps").load("{name}")
'''


def _preset_dir(create=False):
    return bpy.utils.user_resource('SCRIPTS', path=os.path.join("presets", "keyconfig"), create=create)


def load(name):
    """Create and activate-ready keyconfig `name` ("Max" or "Moritz"); called by the preset files."""
    from sys import platform
    from bl_keymap_utils.io import keyconfig_init_from_data
    from . import keymap_max

    industry_compatible = bpy.utils.execfile(os.path.join(
        bpy.utils.system_resource('SCRIPTS'), "presets", "keyconfig", "keymap_data", "industry_compatible_data.py"))
    importlib.reload(keymap_max)

    prefs = bpy.context.preferences
    kc = bpy.context.window_manager.keyconfigs.new(name)
    params = industry_compatible.Params(use_mouse_emulate_3_button=prefs.inputs.use_mouse_emulate_3_button)
    keyconfig_data = keymap_max.generate_keymaps(industry_compatible, params, moritz=(name == "Moritz"))

    if platform == "darwin":
        from bl_keymap_utils.platform_helpers import keyconfig_data_oskey_from_ctrl_for_macos
        keyconfig_data = keyconfig_data_oskey_from_ctrl_for_macos(keyconfig_data)

    keyconfig_init_from_data(kc, keyconfig_data)


def write_presets():
    folder = _preset_dir(create=True)
    for name in NAMES:
        with open(os.path.join(folder, name + ".py"), "w", encoding="utf-8") as fh:
            fh.write(_LOADER.format(name=name, package=__package__))


def remove_presets():
    folder = _preset_dir()
    for name in NAMES:
        path = os.path.join(folder, name + ".py")
        if os.path.exists(path):
            os.remove(path)


def activate(name):
    filepath = bpy.utils.preset_find(name, "keyconfig")
    if filepath:
        bpy.utils.keyconfig_set(filepath)
    return filepath


def _reload_active():
    if bpy.context.preferences.keymap.active_keyconfig in NAMES:
        activate(bpy.context.preferences.keymap.active_keyconfig)
    return None


def reload_active():
    """Reload the Moritz or Max keymap once the add-on's operators exist.

    At startup the keymap loads before add-ons register, so its key items for `maximize.*`
    operators lose their settings (a 1 key without its sub-object level does nothing).
    """
    bpy.app.timers.register(_reload_active, first_interval=0.0)


def register():
    write_presets()


def unregister():
    # Without the add-on its keymaps would call missing operators: fall back to Blender's.
    if bpy.context.preferences.keymap.active_keyconfig in NAMES:
        activate("Blender")
    remove_presets()

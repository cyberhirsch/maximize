# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Name schemes: Blender, Max and Moritz names, and Follow Keymap.

moritz --factory-startup -b --python tests/test_name_schemes.py
"""

import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import vocabulary  # noqa: E402
from maximize.preferences import get_prefs  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


tr = bpy.app.translations
prefs = get_prefs()
weld_tip = bpy.ops.mesh.remove_doubles.get_rna_type().description


def label():
    return tr.pgettext_iface("Merge by Distance", "Operator")


def tip():
    return tr.pgettext_tip(weld_tip)


def keymap(name):
    bpy.ops.preferences.keyconfig_activate(filepath=bpy.utils.preset_find(name, "keyconfig"))
    vocabulary.apply_scheme()


check(prefs.name_scheme == 'AUTO', "Follow Keymap by default")
keymap("Moritz")
check(vocabulary.name_scheme() == 'MORITZ' and label() == "Weld", "Moritz keymap: Moritz names ({})".format(label()))
check(tip().endswith("\nBlender: Merge by Distance"), "Moritz: the Blender name in the tooltip")
keymap("Max")
check(vocabulary.name_scheme() == 'MAX' and label() == "Weld" and tip() == weld_tip,
      "Max keymap: Max names, tooltips as they are")
keymap("Blender")
check(vocabulary.name_scheme() == 'BLENDER' and label() == "Merge by Distance", "Blender keymap: Blender names")
prefs.name_scheme = 'MORITZ'
check(label() == "Weld" and tip().endswith("Blender: Merge by Distance"), "Moritz names chosen with any keymap")
prefs.name_scheme = 'BLENDER'
check(label() == "Merge by Distance" and tip() == weld_tip, "Blender names chosen")
prefs.name_scheme = 'AUTO'

print("FAILURES", len(failures))
if failures:
    sys.exit(1)

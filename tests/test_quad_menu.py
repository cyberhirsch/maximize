# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""The quad menu's contents in Max 2026's style: no icons, groups split by lines, quadrant pairs
padded to the same rows and lines (so they meet at the cursor), Convert To as a submenu.

moritz --factory-startup -b --python tests/test_quad_menu.py
"""

import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import quad_menu as qm  # noqa: E402

failures = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


class Ctx:
    """The parts of the context the quadrant builders read."""
    def __init__(self, mode):
        self.mode = mode
        self.active_object = bpy.context.active_object
        self.scene = bpy.context.scene
        self.space_data = next(a.spaces.active for a in bpy.context.screen.areas if a.type == 'VIEW_3D')


bpy.ops.mesh.primitive_cube_add()
for mode, tools in (('OBJECT', qm._tools_object), ('EDIT_MESH', qm._tools_poly)):
    ctx = Ctx(mode)
    quads = {"display": qm._display(ctx), "viewport": qm._viewport(ctx), "tools": tools(ctx),
             "transform": qm._transform(ctx)}
    icons = [e for q in quads.values() for e in q if e[0] == "op" and "icon" in e[4]
             and e[4]["icon"] not in {'CHECKBOX_HLT', 'CHECKBOX_DEHLT'}]
    check(not icons, mode + ": no icons besides checkboxes " + str([e[2] for e in icons]))
    check(all(any(e[0] == "sep" for e in q) for q in quads.values()), mode + ": every quadrant has groups")
    for q in quads.values():
        check(q[0][0] != "sep" and q[-1][0] != "sep", mode + ": no line at a quadrant's edge")
    size = qm._size(quads["display"], quads["viewport"])
    check(size == tuple(max(a, b) for a, b in zip(qm._counts(quads["display"]),
                                                   qm._counts(quads["viewport"]))), mode + ": padding size")

check(hasattr(bpy.types, "MAXIMIZE_MT_quad_convert"), "Convert To submenu")
check(any(e[0] == "menu" and e[1] == "MAXIMIZE_MT_quad_convert" for e in qm._tools_object(Ctx('OBJECT'))),
      "Convert To in the tools quadrant")
settings = [e[2] for e in qm._tools_poly(Ctx('EDIT_MESH')) if e[0] == "op" and e[4].get("settings")]
check({"Extrude", "Chamfer", "Inset", "Bridge"} <= set(settings), "settings squares " + str(settings))

print("FAILURES", len(failures), failures)

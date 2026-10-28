# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's Hold / Fetch: Hold (Ctrl+H) keeps a copy of the scene in the temp folder; Fetch
(Ctrl+Alt+F) brings it back after asking, still working on the same file, so Save still saves to
it. The copy remembers the open file the way autosave does (Moritz's Save As `recovery` option)
and comes back through Recover Auto Save.
"""

import os
import tempfile

import bpy
from bpy.types import Operator

HOLD_NAME = "moritz_hold.blend"


def hold_path(context):
    folder = bpy.path.abspath(context.preferences.filepaths.temporary_directory) or tempfile.gettempdir()
    return os.path.join(folder, HOLD_NAME)


class MAXIMIZE_OT_hold(Operator):
    """Hold: keep a copy of the scene to come back to with Fetch"""
    bl_idname = "maximize.hold"
    bl_label = "Hold"

    def execute(self, context):
        params = {"filepath": hold_path(context), "copy": True, "check_existing": False}
        if "recovery" in bpy.ops.wm.save_as_mainfile.get_rna_type().properties:
            params["recovery"] = True
        else:
            # Without Moritz's option Fetch opens the copy itself (Save would save the copy).
            self.report({'WARNING'}, "This build can't keep the file path: after Fetch, use Save As")
        bpy.ops.wm.save_as_mainfile(**params)
        self.report({'INFO'}, "Hold: scene kept")
        return {'FINISHED'}


class MAXIMIZE_OT_fetch(Operator):
    """Fetch: go back to the scene kept with Hold"""
    bl_idname = "maximize.fetch"
    bl_label = "Fetch"

    @classmethod
    def poll(cls, context):
        return os.path.isfile(hold_path(context))

    def invoke(self, context, _event):
        return context.window_manager.invoke_confirm(
            self, None, title="Fetch", message="Go back to the scene kept with Hold?", confirm_text="Fetch")

    def execute(self, context):
        bpy.ops.wm.recover_auto_save(filepath=hold_path(context))
        return {'FINISHED'}


def _menu_edit(self, _context):
    layout = self.layout
    layout.separator()
    layout.operator("maximize.hold")
    layout.operator("maximize.fetch")


classes = (
    MAXIMIZE_OT_hold,
    MAXIMIZE_OT_fetch,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_edit.append(_menu_edit)


def unregister():
    bpy.types.TOPBAR_MT_edit.remove(_menu_edit)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

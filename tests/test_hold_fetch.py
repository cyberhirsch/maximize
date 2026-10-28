# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Hold / Fetch: Fetch brings back the held scene and keeps working on the open file.

moritz --factory-startup -b --python tests/test_hold_fetch.py
"""

import os
import sys
import tempfile

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import addon_utils  # noqa: E402

addon_utils.enable("maximize", default_set=True)
from maximize import hold  # noqa: E402

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print("FAIL", msg)


folder = tempfile.mkdtemp()
bpy.context.preferences.filepaths.temporary_directory = folder
user = os.path.join(folder, "user.blend")
bpy.ops.wm.save_as_mainfile(filepath=user)
bpy.ops.mesh.primitive_monkey_add()
bpy.ops.maximize.hold()
check(os.path.isfile(hold.hold_path(bpy.context)), "Hold: no copy in the temp folder")
check(os.path.normcase(bpy.data.filepath) == os.path.normcase(user), "Hold changed the open file")
bpy.data.objects.remove(bpy.data.objects["Suzanne"])
bpy.ops.maximize.fetch('EXEC_DEFAULT')
check("Suzanne" in bpy.data.objects, "Fetch: the held scene did not come back")
check(os.path.normcase(bpy.data.filepath) == os.path.normcase(user),
      "Fetch: open file is {}, expected {}".format(bpy.data.filepath, user))

print("FAILURES", len(failures))
if failures:
    sys.exit(1)

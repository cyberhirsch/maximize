# Run: moritz.exe --factory-startup -b --python tests/test_outliner.py
# Max's Scene Explorer in the Outliner: select with children, Unhide / Unfreeze All, Color By Layer,
# and (Moritz builds) the Shapes filter and the Display as Box column.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy


def say(*a): print("MXOUT", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


ctx = bpy.context
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
coll = ctx.scene.collection
parent = bpy.data.objects.new("Parent", None)
child = bpy.data.objects.new("Child", None)
grand = bpy.data.objects.new("Grand", None)
for o in (parent, child, grand):
    coll.objects.link(o)
child.parent = parent
grand.parent = child
ctx.view_layer.objects.active = parent
parent.select_set(True)

# The poll needs an Outliner; run the selection part directly.
from maximize import outliner
check("descendants", set(outliner._descendants(parent)) == {child, grand})
outliner.MAXIMIZE_OT_outliner_select_children.execute(None, ctx)
check("children selected", child.select_get() and grand.select_get())

child.hide_set(True)
grand.hide_select = True
bpy.ops.maximize.unhide_all()
bpy.ops.maximize.unfreeze_all()
check("unhide all", not child.hide_get())
check("unfreeze all", not grand.hide_select)

red = bpy.data.collections.new("Red")
red.color_tag = 'COLOR_01'
coll.children.link(red)
box = bpy.data.objects.new("Box", bpy.data.meshes.new("Box"))
red.objects.link(box)
bpy.ops.maximize.color_by_layer()
want = ctx.preferences.themes[0].collection_color[0].color
check("color by layer", all(abs(a - b) < 1e-4 for a, b in zip(box.color[:3], want)), tuple(box.color))

space_props = bpy.types.SpaceOutliner.bl_rna.properties
if "use_filter_object_shapes" in space_props:
    check("shapes filter", space_props["use_filter_object_shapes"].type == 'BOOLEAN')
    check("box column", "show_restrict_column_display_box" in space_props)
    check("freeze label", space_props["show_restrict_column_select"].name == "Freeze")
else:
    say("SKIP no Moritz Outliner columns in this build")
say("DONE")

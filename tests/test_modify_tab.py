# Run: moritz.exe --factory-startup -b --python tests/test_modify_tab.py
# Moritz's Modify tab with Maximize: the base entry (a primitive's Parameters modifier is the base,
# hidden from the stack, named after the kind), selecting the base, the rollouts inside the Edit
# Poly modifier's panel, and Maximize's modifiers in Add Modifier.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from mathutils import Matrix

from maximize import primitives, ui


def say(*a): print("MXMOD", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)


if not hasattr(bpy.types.DATA_PT_modifiers, "moritz_base_entry"):
    say("SKIP not Moritz")
    raise SystemExit

panel = bpy.types.DATA_PT_modifiers
check("base hooks", panel.moritz_base_draw is ui.draw_base and panel.moritz_base_entry is primitives.base_entry)
check("no Max panel", not hasattr(bpy.types, "MAXIMIZE_PT_command_modify"))
check("Edit Poly rollouts", ui.MAXIMIZE_PT_edit_poly_rollouts.is_registered)
check("Add Modifier has Maximize's", ui._draw_add_menu in bpy.types.OBJECT_MT_modifier_add_flat._dyn_ui_initialize())

ctx = bpy.context
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob)
box = primitives._create_object(ctx, 'BOX', Matrix())
params, label = primitives.base_entry(box)
check("base entry", params == primitives.primitive_modifier(box) and label == "Box", label)
check("new primitive: base selected", box.modifiers.active is None)

edit = box.modifiers.new("Edit Poly", 'EDIT_POLY')
box.moritz_modifier_stack_index = box.modifiers.find(edit.name)
check("modifier selected", box.modifiers.active == edit and edit.show_expanded)

# The stack hides the Parameters modifier.
from bl_ui.properties_data_modifier import MODIFIER_UL_stack
flags, order = MODIFIER_UL_stack.filter_items(
    type("L", (), {"bitflag_filter_item": 1 << 30})(), ctx, box, "modifiers")
shown = [box.modifiers[i].name for i in order if flags[i]]
check("Parameters hidden from the stack", shown == ["Edit Poly"], shown)

with ctx.temp_override(object=box, active_object=box):
    bpy.ops.object.moritz_modifier_select_base()
    check("select base", box.modifiers.active is None and not edit.show_expanded)
    # The stack's operators leave the base's own modifier alone.
    box.modifiers.active = params
    check("stack operators skip the base modifier",
          not bpy.ops.object.moritz_modifier_toggle.poll())
say("DONE")

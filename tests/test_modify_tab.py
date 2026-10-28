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

# The stack: the Parameters modifier is the base row ("Box"), not a modifier row; plain meshes
# have an Editable Poly base with sub-object levels, a Box has none.
from bl_ui import properties_data_modifier as pdm
check("Box has no levels", pdm.entry_levels(box, None) == ())
check("Edit Poly levels", pdm.entry_levels(box, edit)[:2] == ('VERTEX', 'EDGE'))

with ctx.temp_override(object=box, active_object=box):
    bpy.ops.object.moritz_modifier_select_base()
    check("select base", box.modifiers.active is None and not edit.show_expanded)
    # The stack's operators leave the base's own modifier alone.
    box.modifiers.active = params
    check("stack operators skip the base modifier",
          not bpy.ops.object.moritz_modifier_toggle.poll())
# Selecting entries from the stack.
with ctx.temp_override(object=box, active_object=box):
    box.modifiers.active = None
    bpy.ops.object.moritz_modifier_select(modifier=edit.name)
    check("select entry", box.modifiers.active == edit and edit.show_expanded)
    bpy.ops.object.moritz_modifier_select(modifier="")
    check("select base entry", box.modifiers.active is None)
    from bl_operators.moritz_modifier_stack import is_entry_open
    bpy.ops.object.moritz_stack_expand(modifier=edit.name)
    check("expand entry", is_entry_open(box, edit) and not is_entry_open(box, None))

# Show Cage: the modifiers above an Edit Poly edit on their result when it is off.
from maximize import edit_poly
check("no cage without modifiers above", edit_poly.show_cage(box, edit) is None)
smooth = box.modifiers.new("TurboSmooth", 'SUBSURF')
before = edit_poly.show_cage(box, edit)
with ctx.temp_override(object=box, active_object=box):
    bpy.ops.maximize.show_cage(modifier=edit.name)
check("show cage toggles", before is not None and edit_poly.show_cage(box, edit) is (not before)
      and smooth.show_on_cage is before)
say("DONE")

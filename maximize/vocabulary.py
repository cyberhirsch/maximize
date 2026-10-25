# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max vocabulary: the "Max English" interface translation and Max-named alias operators.

The translation renames Blender labels in place (Merge by Distance -> Weld). The aliases are
operators with Max names that call the Blender operator; they live in the Max menu, so they also
show up in F3 menu search under both keymaps.
"""

import bpy
from bpy.types import Operator


# ------------------------------------------------------------------------------
# Max English

# Blender label -> Max label. Registered for the contexts Blender uses for operator names,
# menu entries and modifier types.
MAX_TERMS = {
    "Merge by Distance": "Weld",
    "Join": "Attach",
    "Separate": "Detach",
    "Bevel": "Chamfer",
    "Inset Faces": "Inset",
    "Loop Cut and Slide": "Swift Loop",
    "Loop Cut": "Swift Loop",
    "Knife": "Cut",
    "Knife Topology Tool": "Cut",
    "Bisect": "QuickSlice",
    "Bridge Edge Loops": "Bridge",
    "Dissolve Vertices": "Remove Vertices",
    "Dissolve Edges": "Remove Edges",
    "Dissolve Faces": "Remove Polygons",
    "Dissolve Selection": "Remove",
    "Local View": "Isolate Selection",
    "Toggle Local View": "Isolate Selection",
    "Toggle X-Ray": "See-Through",
    "Duplicate Objects": "Clone",
    "Duplicate Linked": "Clone as Instance",
    "Make Single User": "Make Unique",
    "Reveal Hidden": "Unhide All",
    "Subdivision Surface": "TurboSmooth",
    "Solidify": "Shell",
    "Outliner": "Scene Explorer",
    "Set Origin": "Set Pivot",
    "Origin to Geometry": "Center Pivot to Object",
    "Origin to 3D Cursor": "Pivot to 3D Cursor",
    "Geometry to Origin": "Center Object to Pivot",
    "Convert to Mesh": "Convert to Editable Poly",
    "Apply Modifier": "Collapse To",
    "Vertex Connect Path": "Connect",
    "Subdivide Edge-Ring": "Connect Edges",
    "Smooth Vertices": "Relax",
    "Flip Normals": "Flip",
    "Lattice": "FFD",
    "Shrinkwrap": "Conform",
    "UV Project": "UVW Map (Blender)",
    "Unwrap": "Unwrap UVW",
}

_CONTEXTS = ("*", "Operator", "ID", "Modifier")
_registered = False


def _translation_dict():
    terms = {(ctx, src): dst for src, dst in MAX_TERMS.items() for ctx in _CONTEXTS}
    return {"en_US": terms, "en_GB": terms}


def set_enabled(enabled):
    global _registered
    if enabled and not _registered:
        bpy.app.translations.register(__name__, _translation_dict())
        _registered = True
    elif not enabled and _registered:
        bpy.app.translations.unregister(__name__)
        _registered = False


# ------------------------------------------------------------------------------
# Alias operators

# (id, Max label, Blender operator, properties, menu, description)
ALIASES = (
    # Edit Poly.
    ("weld", "Weld", "mesh.remove_doubles", {}, 'POLY', "Weld selected vertices that are within the threshold"),
    ("target_weld", "Target Weld", "mesh.merge", {"type": 'LAST'}, 'POLY',
     "Weld the selected vertices onto the last selected one"),
    ("collapse_sub", "Collapse", "mesh.merge", {"type": 'COLLAPSE'}, 'POLY',
     "Collapse each selected group of elements to a single vertex"),
    ("swift_loop", "Swift Loop", "mesh.loopcut_slide", {}, 'POLY', "Insert an edge loop and slide it"),
    ("cut", "Cut", "mesh.knife_tool", {}, 'POLY', "Cut new edges across polygons"),
    ("quickslice", "QuickSlice", "mesh.bisect", {}, 'POLY', "Slice the selection with a plane"),
    ("cap", "Cap", "mesh.fill", {}, 'POLY', "Fill a border with a polygon"),
    ("bridge", "Bridge", "mesh.bridge_edge_loops", {}, 'POLY', "Connect two borders or edge loops with polygons"),
    ("detach", "Detach", "mesh.separate", {"type": 'SELECTED'}, 'POLY', "Detach the selection to a new object"),
    ("remove", "Remove", "mesh.dissolve_mode", {}, 'POLY', "Remove the selection without leaving a hole"),
    ("inset", "Inset", "mesh.inset", {}, 'POLY', "Inset the selected polygons"),
    ("bevel_poly", "Bevel", "mesh.inset", {"use_individual": False}, 'POLY',
     "Bevel the selected polygons: drag to inset, hold Ctrl to change the height"),
    ("relax", "Relax", "mesh.vertices_smooth", {}, 'POLY', "Relax the selected vertices"),
    ("flip", "Flip", "mesh.flip_normals", {}, 'POLY', "Flip the normals of the selected polygons"),
    ("tessellate", "Tessellate", "mesh.subdivide", {}, 'POLY', "Subdivide the selected polygons"),
    ("make_planar", "Make Planar", "mesh.face_make_planar", {}, 'POLY', "Flatten the selected polygons"),
    ("split", "Split", "mesh.edge_split", {"type": 'EDGE'}, 'POLY', "Split the mesh along the selected edges"),
    ("break_vertex", "Break", "mesh.edge_split", {"type": 'VERT'}, 'POLY',
     "Break each selected vertex into one vertex per polygon"),
    ("turn", "Turn", "mesh.edge_rotate", {"use_ccw": False}, 'POLY', "Turn the selected edges inside their polygons"),
    ("remove_isolated", "Remove Isolated Vertices", "mesh.delete_loose",
     {"use_verts": True, "use_edges": False, "use_faces": False}, 'POLY', "Delete vertices that belong to no polygon"),
    ("create_poly", "Create", "mesh.edge_face_add", {}, 'POLY', "Create a polygon (or edge) from the selected vertices"),
    ("hard", "Hard", "mesh.mark_sharp", {}, 'POLY', "Make the selected edges hard (sharp)"),
    ("smooth_edges", "Smooth", "mesh.mark_sharp", {"clear": True}, 'POLY', "Make the selected edges smooth"),
    ("select_by_angle", "Select By Angle", "mesh.faces_select_linked_flat", {}, 'POLY',
     "Grow the polygon selection to neighbors within the angle"),
    ("grow", "Grow", "mesh.select_more", {}, 'POLY', "Grow the sub-object selection"),
    ("shrink", "Shrink", "mesh.select_less", {}, 'POLY', "Shrink the sub-object selection"),
    ("loop", "Loop", "mesh.select_edge_loop_multi", {}, 'POLY', "Select the loops of the selected edges"),
    ("ring", "Ring", "mesh.select_edge_ring_multi", {}, 'POLY', "Select the rings of the selected edges"),
    # Objects and the stack.
    ("attach", "Attach", "object.join", {}, 'OBJECT', "Attach the selected objects to the active one"),
    ("convert_poly", "Convert to Editable Poly", "object.convert", {"target": 'MESH'}, 'OBJECT',
     "Collapse the stack and convert to an editable mesh"),
    ("instance", "Clone as Instance", "object.duplicate_move_linked", {}, 'OBJECT',
     "Clone the selection as instances that share their mesh"),
    ("turbosmooth", "TurboSmooth", "object.modifier_add", {"type": 'SUBSURF'}, 'MODIFY',
     "Add a TurboSmooth (Subdivision Surface) modifier"),
    ("shell", "Shell", "object.modifier_add", {"type": 'SOLIDIFY'}, 'MODIFY', "Add a Shell (Solidify) modifier"),
    ("symmetry", "Symmetry", "object.modifier_add", {"type": 'MIRROR'}, 'MODIFY', "Add a Symmetry (Mirror) modifier"),
    ("bend", "Bend", "object.modifier_add", {"type": 'SIMPLE_DEFORM'}, 'MODIFY',
     "Add a Bend (Simple Deform) modifier"),
    ("ffd", "FFD", "object.modifier_add", {"type": 'LATTICE'}, 'MODIFY', "Add an FFD (Lattice) modifier"),
    ("optimize", "ProOptimizer", "object.modifier_add", {"type": 'DECIMATE'}, 'MODIFY',
     "Add a ProOptimizer (Decimate) modifier"),
    ("conform", "Conform", "object.modifier_add", {"type": 'SHRINKWRAP'}, 'MODIFY',
     "Add a Conform (Shrinkwrap) modifier"),
    ("unwrap_uvw", "Unwrap UVW", "uv.unwrap", {}, 'POLY', "Unwrap the selected polygons"),
    # Display.
    ("isolate", "Isolate Selection", "view3d.localview", {}, 'DISPLAY', "Show only the selection (Alt+Q)"),
    ("see_through", "See-Through", "view3d.toggle_xray", {}, 'DISPLAY', "Toggle see-through display (Alt+X)"),
)


def _alias_class(ident, label, target, props, description):
    module, name = target.split(".")

    def target_op():
        return getattr(getattr(bpy.ops, module), name)

    def finished(result):
        return {'FINISHED'} if result & {'FINISHED', 'RUNNING_MODAL'} else {'CANCELLED'}

    def poll(cls, _context):
        return target_op().poll()

    def invoke(self, _context, _event):
        return finished(target_op()('INVOKE_DEFAULT', **props))

    def execute(self, _context):
        return finished(target_op()('EXEC_DEFAULT', **props))

    return type("MAXIMIZE_OT_" + ident, (Operator,), {
        "bl_idname": "maximize." + ident,
        "bl_label": label,
        "bl_description": description,
        "poll": classmethod(poll),
        "invoke": invoke,
        "execute": execute,
    })


classes = tuple(_alias_class(ident, label, target, props, desc)
                for ident, label, target, props, _menu, desc in ALIASES)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    from .preferences import get_prefs
    prefs = get_prefs()
    set_enabled(prefs.use_max_english if prefs else True)


def unregister():
    set_enabled(False)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

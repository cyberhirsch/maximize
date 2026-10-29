# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max vocabulary: the name schemes and Max-named alias operators.

The name schemes, parallel to the keymaps: Blender (Blender's names), Max (Max's names wherever Max
has one) and Moritz (Max's names, with Blender's name in the tooltip so tutorials and F3 search
keep working). By default the scheme follows the keymap. They are interface translations
(Merge by Distance -> Weld), so files and the Python API are unchanged. The aliases are
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
    # Modifiers whose Blender name is used nowhere else (Skin, Smooth, Armature and Wireframe need
    # their own translation context first: the modifier list names them meanwhile).
    "Screw": "Lathe",
    "Decimate": "ProOptimizer",
    "Cast": "Spherify",
    "UV Warp": "UVW Xform",
    "Normal Edit": "Edit Normals",
    "Weighted Normal": "Weighted Normals",
    "Surface Deform": "Skin Wrap",
    "Mesh Cache": "Point Cache",
    "Smooth Laplacian": "Relax",
    "Data Transfer": "Attribute Transfer",
    # Edit Poly and the viewport.
    "Extrude Region": "Extrude",
    "Extrude Individual Faces": "Extrude by Polygon",
    "Subdivide": "Tessellate",
    "Delete Loose": "Remove Isolated Vertices",
    "Proportional Editing": "Soft Selection",
    "Frame Selected": "Zoom Extents Selected",
    "Frame All": "Zoom Extents",
    "Hide Selected": "Hide Selection",
    "Select Linked": "Select Element",
    "Select Linked All": "Select Element",
}

_CONTEXTS = ("*", "Operator", "ID", "Modifier")

NAME_SCHEMES = (
    ('AUTO', "Follow Keymap", "Max's names with the Max keymap, Moritz's with the Moritz keymap, "
     "Blender's otherwise"),
    ('BLENDER', "Blender", "Blender's names"),
    ('MAX', "Max", "3ds Max's names wherever Max has one (Weld, Chamfer, Attach, Swift Loop and more)"),
    ('MORITZ', "Moritz", "Max's names, with Blender's name in the tooltip"),
)
_KEYMAP_SCHEMES = {"Max": 'MAX', "Moritz": 'MORITZ'}
_current = 'BLENDER'


def _blender_tooltips():
    """Moritz: each renamed operator's and modifier's tooltip ends with its Blender name."""
    tips = {}

    def add(name, description):
        if name in MAX_TERMS and description:
            tips[("*", description)] = "{:s}\nBlender: {:s}".format(description, name)
    for module in dir(bpy.ops):
        ops = getattr(bpy.ops, module)
        for name in dir(ops):
            try:
                rna = getattr(ops, name).get_rna_type()
            except (AttributeError, KeyError, RuntimeError):
                continue
            add(rna.name, rna.description)
    for item in bpy.types.Modifier.bl_rna.properties["type"].enum_items:
        add(item.name, item.description)
    return tips


def _translation_dict(scheme):
    terms = {(ctx, src): dst for src, dst in MAX_TERMS.items() for ctx in _CONTEXTS}
    if scheme == 'MORITZ':
        terms.update(_blender_tooltips())
    return {"en_US": terms, "en_GB": terms}


def name_scheme(context=None):
    """The scheme in use: the preference, or for Follow Keymap the one that goes with the keymap."""
    from .preferences import get_prefs
    context = context or bpy.context
    prefs = get_prefs(context)
    scheme = prefs.name_scheme if prefs else 'AUTO'
    if scheme == 'AUTO':
        keyconfig = context.window_manager.keyconfigs.active if context.window_manager else None
        scheme = _KEYMAP_SCHEMES.get(keyconfig.name if keyconfig else "", 'BLENDER')
    return scheme


def set_scheme(scheme):
    """Register the names for `scheme` ('BLENDER' / 'MAX' / 'MORITZ') in place of the current ones."""
    global _current
    if scheme == _current:
        return
    if _current != 'BLENDER':
        bpy.app.translations.unregister(__name__)
    _current = scheme
    if scheme != 'BLENDER':
        bpy.app.translations.register(__name__, _translation_dict(scheme))
        # The names are an interface translation: it has to be on.
        view = bpy.context.preferences.view
        view.use_translate_interface = True
        if scheme == 'MORITZ':
            view.use_translate_tooltips = True
    for window in getattr(bpy.context.window_manager, "windows", ()):
        for area in window.screen.areas:
            area.tag_redraw()


def apply_scheme(context=None):
    set_scheme(name_scheme(context))


def _watch_keymap():
    """Follow Keymap: the keymap can change in Preferences or the Quick Setup."""
    try:
        apply_scheme()
    except (AttributeError, ReferenceError):
        pass
    return 1.0


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
    ("paint_connect", "Paint Connect", "mesh.knife_tool", {"use_occlude_geometry": True}, 'POLY',
     "Draw across polygons to connect their edges (Blender's Knife: Ctrl snaps to edge middles, Enter ends)"),
    ("build_corner", "Build Corner", "mesh.edge_rotate", {"use_ccw": False}, 'POLY',
     "Turn the selected edges inside their two polygons, so the edge loop turns a corner"),
    ("quickslice", "QuickSlice", "mesh.bisect", {}, 'POLY', "Slice the selection with a plane"),
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
    ("similar", "Similar", "mesh.select_similar", {}, 'POLY', "Select sub-objects similar to the selected ones"),
    ("select_outline", "Outline", "mesh.region_to_loop", {}, 'POLY', "Select the outline of the selected polygons"),
    ("select_fill", "Fill", "mesh.shortest_path_select", {"use_fill": True}, 'POLY',
     "Select everything between the last two selected sub-objects"),
    ("select_nonquads", "NonQuads", "mesh.select_face_by_sides", {"number": 4, "type": 'NOTEQUAL', "extend": False},
     'POLY', "Select the polygons that are not quads"),
    ("select_open", "Open", "mesh.select_non_manifold", {
        "extend": False, "use_wire": False, "use_boundary": True, "use_multi_face": False,
        "use_non_contiguous": False, "use_verts": False}, 'POLY', "Select the open edges (borders)"),
    ("select_random", "Random", "mesh.select_random", {}, 'POLY', "Select sub-objects at random"),
    ("select_mirror", "Symmetry", "mesh.select_mirror", {}, 'POLY',
     "Select the sub-objects mirrored across the symmetry axis"),
    ("symmetrize", "Symmetrize", "mesh.symmetrize", {}, 'POLY', "Make one side of the mesh a mirror of the other"),
    ("quadrify", "Quadrify Selection", "mesh.tris_convert_to_quads", {}, 'POLY',
     "Join the triangles of the selection into quads"),
    ("meshsmooth", "MeshSmooth", "mesh.subdivide", {"smoothness": 1.0}, 'POLY',
     "Subdivide and smooth the selected polygons"),
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
    ("see_through", "See-Through", "maximize.see_through_objects", {}, 'DISPLAY', "Toggle see-through display (Alt+X)"),
)


def view3d_override(context):
    """Context for the biggest 3D View of the window (for viewport tools run from a panel button),
    or None."""
    window = context.window
    screen = window.screen if window else None
    if screen is None:
        return None
    from .viewport import active_view_region
    active = active_view_region(window)
    if active is not None:
        return {"window": window, "area": active[0], "region": active[1]}
    areas = [a for a in screen.areas if a.type == 'VIEW_3D']
    if not areas:
        return None
    area = max(areas, key=lambda a: a.width * a.height)
    # In a four-view layout, the main (user) view.
    main = area.spaces.active.region_3d
    regions = [r for r in area.regions if r.type == 'WINDOW']
    region = next((r for r in regions if r.data is not None and main is not None and
                   r.data.as_pointer() == main.as_pointer()), regions[0] if regions else None)
    return {"window": window, "area": area, "region": region} if region else None


def _alias_class(ident, label, target, props, description):
    module, name = target.split(".")

    def target_op():
        return getattr(getattr(bpy.ops, module), name)

    def finished(result):
        return {'FINISHED'} if result & {'FINISHED', 'RUNNING_MODAL'} else {'CANCELLED'}

    def run(context, mode):
        op = target_op()
        if not op.poll():
            # From a panel button: a viewport tool (Cut, Paint Connect) runs in the 3D View.
            override = view3d_override(context)
            if override is not None:
                with context.temp_override(**override):
                    return finished(op(mode, **props))
        return finished(op(mode, **props))

    def poll(cls, context):
        if target_op().poll():
            return True
        override = view3d_override(context)
        if override is None:
            return False
        with context.temp_override(**override):
            return target_op().poll()

    def invoke(self, context, _event):
        return run(context, 'INVOKE_DEFAULT')

    def execute(self, context):
        return run(context, 'EXEC_DEFAULT')

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


def modifier_list():
    """Moritz's modifier list module (Max names and search keywords), or None in stock Blender."""
    try:
        from bl_operators import moritz_modifier_list
    except ImportError:
        return None
    return moritz_modifier_list


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    apply_scheme()
    mlist = modifier_list()
    if mlist is not None:
        mlist.name_scheme = lambda: _current
    bpy.app.timers.register(_watch_keymap, first_interval=1.0, persistent=True)


def unregister():
    if bpy.app.timers.is_registered(_watch_keymap):
        bpy.app.timers.unregister(_watch_keymap)
    set_scheme('BLENDER')
    mlist = modifier_list()
    if mlist is not None:
        mlist.name_scheme = lambda: 'BLENDER'
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

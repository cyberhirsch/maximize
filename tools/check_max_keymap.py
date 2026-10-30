"""Check Moritz's Max keymap against 3ds Max's documented default shortcuts.

Reads the Main UI, Edit Poly and Editable Poly tables from docs/shortcuts_max_maya_full.md, looks up
what the "Max" keyconfig binds to each key, and writes docs/shortcut_coverage.md.

Run: blender --factory-startup -b --python tools/check_max_keymap.py
"""
import fnmatch
import os
import re
import sys

import addon_utils
import bpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
addon_utils.enable("maximize", default_set=True)
DOCS = os.path.join(ROOT, "docs")
SOURCE = os.path.join(DOCS, "shortcuts_max_maya_full.md")
REPORT = os.path.join(DOCS, "shortcut_coverage.md")

TABLES = (
    ("Main UI (global)", "### Main UI (global)", 'OBJECT'),
    ("Edit Poly modifier", "### Edit Poly modifier", 'EDIT'),
    ("Editable Poly", "### Editable Poly", 'EDIT'),
)

# Keymaps that handle a key in the 3D Viewport, highest priority first.
LOOKUP = {
    'OBJECT': ("Object Mode", "Object Non-modal", "3D View Generic", "3D View", "Frames",
               "Screen Editing", "Screen", "Window"),
    'EDIT': ("Mesh", "3D View Generic", "3D View", "Frames", "Screen Editing", "Screen", "Window"),
}
# Main UI rows that belong to Edit Poly.
EDIT_CATEGORIES = ("Editable Polygon Object", "PolyTools")

# Max action -> patterns for the binding's signature ("idname prop=value ..."), "|"-separated.
# None: Moritz has no matching feature yet.
EXPECTED = {
    # Main UI: edit, file, selection.
    "Align": "maximize.align*",
    "Clone": "maximize.clone*",
    "Delete Objects": "object.delete*",
    "Fetch": "maximize.fetch*",
    "Hold": "maximize.hold*",
    "Normal Align": None,
    "Redo Scene Operation": "ed.redo*",
    "Transform Type-In Dialog Toggle": "maximize.transform_typein*",
    "Undo Scene Operation": "ed.undo*",
    "New Scene": "wm.read_homefile*",
    "Open File": "wm.open_mainfile*",
    "Save File": "wm.save_mainfile*",
    "Save File As": "wm.save_as_mainfile*",
    "Save Incremental (+)": "wm.save_mainfile*incremental=True*",
    "Select All": "*select_all*action=SELECT*",
    "Select Ancestor": "object.select_hierarchy*PARENT*",
    "Select By Name": "maximize.select_by_name*",
    "Select Child": "object.select_hierarchy*CHILD*",
    "Select Children": "object.select_grouped*CHILDREN*",
    "Select Invert": "*select_all*action=INVERT*",
    "Select None": "*select_all*action=DESELECT*",
    "Select Similar": "object.select_grouped*|mesh.select_similar*",
    "Selection Lock Toggle": None,
    "Smart Select": "wm.tool_set_by_id*select*",
    # Edit Poly in the Main UI table.
    "Extrude Face (Poly)": "mesh.extrude*",
    "Grow Selection (Poly)": "mesh.select_more*",
    "Ignore Backfacing Toggle (Poly)": "view3d.toggle_xray*",
    "Select Sub-object Loop": "mesh.select_edge_loop_multi*",
    "Select Sub-object Ring": "mesh.select_edge_ring_multi*",
    "Shrink Selection (Poly)": "mesh.select_less*",
    "Soft Selection Toggle (Poly)": "wm.context_toggle*use_proportional_edit*",
    "Swift Loop": "mesh.loopcut_slide*|maximize.swift_loop*",
    "Circle Loops": None, "Geo Poly": None, "Insert Loop": "mesh.loopcut_slide*", "PolyShift Move": None,
    "Set Flow": None, "Spin Edge": "mesh.edge_rotate*", "Straighten Loops": None,
    "Refine (Spline)": None,
    # Objects, cameras, stack.
    "Group Attach": None,
    "Create Camera (Physical) From View": "maximize.camera_from_view*",
    "Create Camera (Standard) From View": "maximize.camera_from_view*",
    "MAXScript Listener": None,
    "Show End Result": "maximize.show_end_result*",
    "Sub-Object Level 1": "maximize.subobject*VERTEX*",
    "Sub-Object Level 2": "maximize.subobject*EDGE*",
    "Sub-Object Level 3": "maximize.subobject*BORDER*",
    "Sub-Object Level 4": "maximize.subobject*POLYGON*",
    "Sub-object Level 5": "maximize.subobject*ELEMENT*",
    "Geometry Selection Visibility Toggle": None,
    "Asset Tracking Toggle": None,
    "Lock User Interface Toggle": None,
    "Show Main Toolbar Toggle": None,
    # Quad menu sets.
    "Lock": None,
    "Viewports": "wm.call_menu*MAXIMIZE_MT_point_of_view*",
    "Windows": None,
    # Render.
    "Advanced Lighting Panel": None,
    "Create Animated Sequence File...": None,
    "Environment Dialog Toggle": None,
    "Render": "render.render*",
    "Render Last": "render.render*",
    "Render SetUp...": "maximize.render_setup*",
    # Animation and time.
    "Auto Key Mode Toggle": "wm.context_toggle*use_keyframe_insert_auto*",
    "Set Keys": "anim.keyframe_insert*",
    "Backup Time One Unit": "screen.frame_offset*delta=-1*",
    "Forward Time One Unit": "screen.frame_offset*delta=1*",
    "Go to End Frame": "screen.frame_jump*end=True*",
    "Go to Start Frame": "screen.frame_jump*end=False*",
    "Play Animation": "screen.animation_play*",
    # Snaps.
    "Angle Snap Toggle": "maximize.angle_snap*",
    "Cycle Active Snap Type": None,
    "Enable Axis Constraints in Snaps Toggle": None,
    "Snaps Toggle": "wm.context_toggle*tool_settings.use_snap*",
    # Tools.
    "Affect Pivot Only Mode Toggle": "maximize.affect_pivot_only*",
    "Center Point Cycle": "*pivot*",
    "Cycle Selection Method": None,
    "Display as See-Through Toggle": "maximize.see_through_objects*",
    "Hide Selection": "object.hide_view_set*unselected=False*",
    "Hide Unselected": "object.hide_view_set*unselected=True*|mesh.hide*unselected=True*",
    "Isolate Selection": "view3d.localview*",
    "Isolate Selection Toggle": "view3d.localview*",
    "Keyboard Shortcut Override Toggle": None,
    "Material Editor Toggle": "maximize.material_editor*",
    "Maximize Viewport Toggle": "maximize.viewport_maximize*|screen.region_quadview*|screen.screen_full_area*",
    "Pan Viewport": None,
    "Quick Align": None,
    "Scale Cycle": None,
    "Select and Move": "wm.tool_set_by_id*builtin.move*",
    "Select and Rotate": "wm.tool_set_by_id*builtin.rotate*",
    "Show Statistics Toggle": "wm.context_toggle*show_stats*",
    "Smart Place": None,
    "Smart Scale": "wm.tool_set_by_id*builtin.scale*",
    "Sound Toggle": None,
    "Spacing Tool": "maximize.spacing*",
    "Sub-object Selection Toggle": None,
    "Transform Gizmo Plane Constraint Cycle": None,
    "Transform Gizmo Size Down": None,
    "Transform Gizmo Size Up": None,
    "Transform Gizmo X Constraint": None,
    "Transform Gizmo Y Constraint": None,
    "Transform Gizmo Z Constraint": None,
    "Unhide All": "object.hide_view_clear*|mesh.reveal*",
    "Viewport Lighting Illuminate with Default / Scene Lights Toggle": None,
    "Viewport Safe Frames Toggle": "wm.context_toggle*show_safe_areas*",
    "Viewport Selection Shade Selected Faces Toggle": None,
    "Viewport Selection Show Selection Bracket Toggle": None,
    "Virtual Viewport Pan Down": None, "Virtual Viewport Pan Left": None,
    "Virtual Viewport Pan Right": None, "Virtual Viewport Pan Up": None,
    "Virtual Viewport Toggle": None, "Virtual Viewport Zoom In": None, "Virtual Viewport Zoom Out": None,
    "Window / Crossing Toggle": None,
    "Zoom Extents": "view3d.view_all*",
    "Zoom Extents All": "view3d.view_all*use_all_regions=True*",
    "Zoom Extents Selected": "view3d.view_selected*",
    "Zoom In 2X": None,
    "Zoom Mode": None,
    "Zoom Region Mode": "view3d.zoom_border*",
    "Zoom Viewport In": "view3d.zoom*delta=1*",
    "Zoom Viewport Out": "view3d.zoom*delta=-1*",
    "Add/Edit Parameters... (TV)": None,
    "Launch Global Search": "wm.search_menu*|wm.search_operator*",
    # Views.
    "High Quality": None,
    "Adaptive Degradation Toggle": None,
    "Camera View": "view3d.view_camera*",
    "Disable Viewport": None,
    "Expert Mode Toggle": None,
    "Front View": "view3d.view_axis*FRONT*",
    "Hide Cameras Toggle": "wm.context_toggle*viewport_camera*",
    "Hide Geometry Toggle": "wm.context_toggle*viewport_mesh*",
    "Hide Grids Toggle": "wm.context_toggle*show_floor*",
    "Hide Helpers Toggle": "wm.context_toggle*viewport_empty*",
    "Hide Lights Toggle": "wm.context_toggle*viewport_light*",
    "Hide Particle Systems Toggle": None,
    "Hide Shapes Toggle": "wm.context_toggle*viewport_curve*",
    "Hide Space Warps Toggle": None,
    "Home View": None,
    "Left View": "view3d.view_axis*LEFT*",
    "Orbit View Mode": None,
    "Orthographic User View": "maximize.view_projection*ORTHO*",
    "Pan View": None,
    "Perspective User View": "maximize.view_projection*PERSP*",
    "Redo Viewport Operation": "maximize.view_history*redo=True*",
    "Redraw All Views": None,
    "Selection/Preview Highlights Toggle": None,
    "Show Floating Dialogs": None,
    "Spot/Directional Light View": "view3d.object_as_camera*",
    "Top View": "view3d.view_axis*TOP*",
    "Undo Viewport Operation": "maximize.view_history*redo=False*",
    "Update Background Image": None,
    "View Edged Faces Toggle": "wm.context_toggle*show_wireframes*",
    "Viewport Background": None,
    "WalkThrough View Mode": "view3d.walk*|view3d.navigate*",
    "Wireframe / Smooth+Highlights Toggle": "wm.context_toggle_enum*shading.type*",
    # Edit Poly / Editable Poly.
    "Attach": "maximize.attach*|object.join*",
    "Attach Mode": "maximize.attach*|object.join*",
    "Bevel Mode": "maximize.bevel_poly*|mesh.inset*",
    "Break": "mesh.split*|mesh.edge_split*|mesh.rip*",
    "Break Vertices": "mesh.split*|mesh.edge_split*|mesh.rip*",
    "Cap": "maximize.cap*|mesh.fill*",
    "Chamfer Mode": "maximize.chamfer*|mesh.bevel*",
    "Collapse": "mesh.merge*COLLAPSE*|maximize.collapse_sub*",
    "Connect": "maximize.connect*",
    "Constrain to Edges": None,
    "Cut": "mesh.knife_tool*|maximize.cut*",
    "Cut Mode": "mesh.knife_tool*|maximize.cut*",
    "Detach": "mesh.separate*|maximize.detach*",
    "Edge Turn": "mesh.edge_rotate*",
    "Edit Soft Selection Mode": None,
    "Edit Soft Selection": None,
    "Extrude along Spline Mode": None,
    "Extrude Mode": "mesh.extrude*",
    "Grow Selection": "mesh.select_more*",
    "Hide": "mesh.hide*unselected=False*",
    "Hide Selected": "mesh.hide*unselected=False*",
    "Ignore Backfacing in Selections": "view3d.toggle_xray*",
    "Make Planar": "maximize.make_planar*|mesh.face_make_planar*",
    "MeshSmooth": "mesh.subdivide*|object.subdivision_set*",
    "Quickslice Mode": "mesh.bisect*|maximize.quickslice*",
    "Repeat Last Operation": "screen.repeat_last*",
    "Shrink Selection": "mesh.select_less*",
    "Target Weld Mode": "mesh.merge*LAST*|maximize.target_weld*",
    "Weld Target Mode": "mesh.merge*LAST*|maximize.target_weld*",
    "Weld Selected": "mesh.remove_doubles*|maximize.weld*",
    "Use Soft Selection": "wm.context_toggle*use_proportional_edit*",
    "Soft Selection": "wm.context_toggle*use_proportional_edit*",
    "Remove (vertices; combines polygons, no hole)": "mesh.dissolve*|maximize.remove*",
    "Remove edges and delete the extra vertices": "mesh.dissolve*",
}

KEY_NAMES = {
    "PgUp": 'PAGE_UP', "PgDown": 'PAGE_DOWN', "Up": 'UP_ARROW', "Down": 'DOWN_ARROW',
    "Left": 'LEFT_ARROW', "Right": 'RIGHT_ARROW', "Del": 'DEL', "Insert": 'INSERT', "Home": 'HOME',
    "End": 'END', "Space": 'SPACE', "Enter": 'RET', "Backspace": 'BACK_SPACE', "Tab": 'TAB',
    "Esc": 'ESC', "`": 'ACCENT_GRAVE', "[": 'LEFT_BRACKET', "]": 'RIGHT_BRACKET', ";": 'SEMI_COLON',
    ",": 'COMMA', ".": 'PERIOD', "/": 'SLASH', "-": 'MINUS', "=": 'EQUAL', "\\": 'BACK_SLASH',
    "Num/": 'NUMPAD_SLASH', "Num+": 'NUMPAD_PLUS', "Num-": 'NUMPAD_MINUS',
}
DIGITS = ("ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE")


def parse_combo(text):
    """'Ctrl+Shift+C' -> ('C', {'ctrl', 'shift'}); None for mouse gestures and descriptions."""
    text = text.replace("\\`", "`").strip()
    if not text or text == "—" or re.search(r"LMB|RMB|MMB|drag|Drag|click|\[hold\]|\(", text):
        return None
    mods = set()
    while True:
        m = re.match(r"(Ctrl|Shift|Alt)\+(.+)", text)
        if not m:
            break
        mods.add(m.group(1).lower())
        text = m.group(2)
    if text in KEY_NAMES:
        key = KEY_NAMES[text]
    elif re.fullmatch(r"[A-Za-z]", text):
        key = text.upper()
    elif re.fullmatch(r"[0-9]", text):
        key = DIGITS[int(text)]
    elif re.fullmatch(r"F\d{1,2}", text):
        key = text
    elif re.fullmatch(r"Num\d", text):
        key = "NUMPAD_" + text[3]
    else:
        return None
    return key, mods


def split_combos(cell):
    # "[, Ctrl+=" and "Ctrl+PgUp, Ctrl+Up": alternatives separated by ", ".
    return [c for c in re.split(r",\s+", cell.strip()) if c]


def read_tables():
    lines = open(SOURCE, encoding="utf-8").read().splitlines()
    tables = []
    for title, heading, context in TABLES:
        start = lines.index(heading)
        rows = []
        for line in lines[start + 1:]:
            if line.startswith("#"):
                break
            if not line.startswith("|") or line.startswith("|---") or line.startswith("| Shortcut"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            # A "|" inside a cell ("Lighting \| Render") splits it; glue the action back together.
            if len(cells) > 3:
                cells = [cells[0], " | ".join(cells[1:-1]), cells[-1]]
            rows.append(cells[:3])
        tables.append((title, context, rows))
    return tables


def signature(kmi):
    parts = [kmi.idname]
    props = kmi.properties
    if props is not None:
        for prop in props.bl_rna.properties:
            ident = prop.identifier
            if ident == "rna_type" or not props.is_property_set(ident) or prop.type == 'POINTER':
                # Pointers are the macro's sub-operators: their address changes every run.
                continue
            value = getattr(props, ident)
            if isinstance(value, (set, frozenset)):
                value = ",".join(sorted(value))
            parts.append("{:s}={!s}".format(ident, value))
    return " ".join(parts)


def lookup(kc, keymaps, key, mods, expected):
    """The first keymap that binds the key; within it, prefer an item that matches `expected`
    (several items can share a key when their operators poll for different contexts)."""
    for km_name in keymaps:
        km = kc.keymaps.get(km_name)
        if km is None:
            continue
        found = []
        for kmi in km.keymap_items:
            if not kmi.active or kmi.type != key or kmi.value not in {'PRESS', 'CLICK'}:
                continue
            if kmi.key_modifier != 'NONE':
                continue
            if kmi.any or (kmi.ctrl == ('ctrl' in mods) and kmi.shift == ('shift' in mods)
                           and kmi.alt == ('alt' in mods) and not kmi.oskey):
                found.append(signature(kmi))
        if found:
            best = next((sig for sig in found if expected and matches(sig, expected)), found[0])
            return km_name, best
    return None, None


def matches(sig, patterns):
    return any(fnmatch.fnmatchcase(sig, p) for p in patterns.split("|"))


def main():
    path = bpy.utils.preset_find("Max", "keyconfig")
    bpy.utils.keyconfig_set(path)
    kc = bpy.context.window_manager.keyconfigs["Max"]

    out = ["# Max keymap coverage", "",
           "Generated by `tools/check_max_keymap.py` from the Moritz build: every key in 3ds Max's Main UI, "
           "Edit Poly and Editable Poly tables ([shortcuts_max_maya_full.md](shortcuts_max_maya_full.md)), "
           "and what Moritz's Max keymap does with it in the 3D Viewport (Object Mode for the Main UI, "
           "Edit Mode for Edit Poly). Plan: [shortcut_plan.md](shortcut_plan.md).", "",
           "- **OK**: same key, same function.",
           "- **Conflict**: the key does something else in Moritz.",
           "- **Unbound**: Moritz has the function but not on this key.",
           "- **No feature**: Moritz has no matching function yet (the cell shows what the key does today).",
           "- **Mouse**: mouse gestures and descriptions; checked by hand, not here.", ""]
    totals = {}
    sections = []
    unknown = []
    for title, context, rows in read_tables():
        counts = {}
        body = ["## " + title, "", "| Max key | Max action | Moritz | Status |", "|---|---|---|---|"]
        for shortcut, action, notes in rows:
            ctx = 'EDIT' if context == 'EDIT' or any(c in notes for c in EDIT_CATEGORIES) else 'OBJECT'
            if action not in EXPECTED:
                unknown.append(action)
            expected = EXPECTED.get(action)
            combos = [(c, parse_combo(c)) for c in split_combos(shortcut)]
            for text, parsed in combos:
                if parsed is None:
                    status, found = "Mouse", ""
                else:
                    km_name, sig = lookup(kc, LOOKUP[ctx], *parsed, expected)
                    found = "`{:s}` ({:s})".format(sig, km_name) if sig else "—"
                    if expected is None:
                        status = "No feature"
                    elif sig is None:
                        status = "Unbound"
                    elif matches(sig, expected):
                        status = "OK"
                    else:
                        status = "Conflict"
                counts[status] = counts.get(status, 0) + 1
                totals[status] = totals.get(status, 0) + 1
                body.append("| {:s} | {:s} | {:s} | {:s} |".format(
                    text.replace("|", "\\|"), action.replace("|", "\\|"), found.replace("|", "\\|"),
                    "**{:s}**".format(status) if status in {"Conflict", "Unbound"} else status))
        body.append("")
        sections.append((title, counts, body))

    order = ("OK", "Conflict", "Unbound", "No feature", "Mouse")
    out += ["## Summary", "", "| Table | " + " | ".join(order) + " |", "|---" * (len(order) + 1) + "|"]
    for title, counts, _body in sections:
        out.append("| {:s} | ".format(title) + " | ".join(str(counts.get(s, 0)) for s in order) + " |")
    out.append("| **All** | " + " | ".join("**{:d}**".format(totals.get(s, 0)) for s in order) + " |")
    keyed = sum(totals.get(s, 0) for s in order[:4])
    out += ["", "{:d} of {:d} keyboard shortcuts are OK ({:.0f}%); of the ones Moritz has a feature for, {:d} of {:d}."
            .format(totals.get("OK", 0), keyed, 100.0 * totals.get("OK", 0) / max(keyed, 1),
                    totals.get("OK", 0), sum(totals.get(s, 0) for s in order[:3])), ""]
    for _title, _counts, body in sections:
        out += body
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("MAXCOV", totals, "unknown actions:", unknown)


main()

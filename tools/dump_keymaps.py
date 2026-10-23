"""Dump every binding of Blender's built-in keymaps (Blender default + Industry Compatible)
to Markdown. Run: blender --factory-startup -b --python tools/dump_keymaps.py"""
import os
import sys

import bpy

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
sys.path.insert(0, os.path.join(bpy.utils.system_resource('SCRIPTS'), "presets", "keyconfig"))

from keymap_data import blender_default as bd  # noqa: E402
from keymap_data import industry_compatible_data as ic  # noqa: E402

KMI = bpy.types.KeyMapItem.bl_rna.properties
TYPE_NAMES = {i.identifier: i.name for i in KMI["type"].enum_items}
VALUE_NAMES = {i.identifier: i.name for i in KMI["value"].enum_items}
DIR_NAMES = {i.identifier: i.name for i in KMI["direction"].enum_items}


def key_text(ev):
    parts = []
    if ev.get("any"):
        parts.append("Any modifier")
    for mod, label in (("ctrl", "Ctrl"), ("shift", "Shift"), ("alt", "Alt"),
                       ("oskey", "OS"), ("hyper", "Hyper")):
        v = ev.get(mod, False)
        if v == -1:
            parts.append(f"[{label}]")  # Either state.
        elif v:
            parts.append(label)
    if ev.get("key_modifier"):
        parts.append(TYPE_NAMES.get(ev["key_modifier"], ev["key_modifier"]) + " (held)")
    parts.append(TYPE_NAMES.get(ev["type"], ev["type"]) or ev["type"])
    text = "+".join(parts)
    value = ev.get("value", 'PRESS')
    if value not in ('PRESS', 'NOTHING'):
        text += " " + VALUE_NAMES.get(value, value).lower()
    if ev.get("direction") and ev["direction"] != 'ANY':
        text += " " + DIR_NAMES.get(ev["direction"], ev["direction"]).lower()
    if ev.get("repeat"):
        text += " (repeat)"
    return text.replace("|", "\\|")


def op_label(idname):
    if "." not in idname:
        return ""
    mod, fn = idname.split(".", 1)
    try:
        return getattr(getattr(bpy.ops, mod), fn).get_rna_type().name
    except Exception:
        return ""


def props_text(props):
    if not props:
        return ""
    out = []
    for p in props.get("properties", []) or []:
        name, value = p[0], p[1]
        if isinstance(value, list):  # Nested pointer properties.
            value = "{" + ", ".join(f"{n}={v!r}" for n, v, *_ in value) + "}"
        else:
            value = repr(value)
        out.append(f"{name}={value}")
    return ", ".join(out).replace("|", "\\|")


def write(path, title, intro, keyconfig_data):
    lines = [f"# {title}", "", *intro, ""]
    toc = []
    body = []
    total = 0
    for km_name, km_args, km_content in keyconfig_data:
        items = [it for it in km_content.get("items", [])
                 if not (it[2] and it[2].get("active") is False)]
        if not items:
            continue
        modal = km_args.get("modal", False)
        space = km_args.get("space_type", "EMPTY")
        region = km_args.get("region_type", "WINDOW")
        anchor = km_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "")
        toc.append(f"- [{km_name}](#{anchor}) — {len(items)}")
        body += [f"## {km_name}", "",
                 f"Space `{space}`, region `{region}`" + (", **modal** (keys while a tool runs)" if modal else ""),
                 "", "| Key | Action | Operator / modal item | Properties |", "|---|---|---|---|"]
        for idname, ev, props in items:
            label = idname if modal else op_label(idname)
            note = props_text(props)
            if idname == "screen.area_join" and props and any(
                    p[0] == "header_drag" for p in props.get("properties", [])):
                label += " (Moritz)"
            body.append(f"| {key_text(ev)} | {label} | `{idname}` | {note} |")
            total += 1
        body.append("")
    lines += [f"**{total} bindings in {len(toc)} keymaps.**", "", "### Keymaps", "", *toc, "", *body]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("MORITZ_DUMP", path, total, len(toc))


os.makedirs(DOCS, exist_ok=True)

# The defaults the "Blender" keymap preset (Blender.py) uses on a fresh install.
default_data = bd.generate_keymaps(bd.Params(
    select_mouse='LEFT',
    use_mouse_emulate_3_button=False,
    spacebar_action='PLAY',
    use_key_activate_tools=False,
    use_region_toggle_pie=False,
    v3d_tilde_action='VIEW',
    use_v3d_mmb_pan=False,
    v3d_alt_mmb_drag_action='RELATIVE',
    use_select_all_toggle=False,
    use_v3d_tab_menu=False,
    use_v3d_shade_ex_pie=False,
    use_gizmo_drag=True,
    use_fallback_tool=True,
    use_fallback_tool_select_handled=False,
    use_alt_tool_or_cursor=False,
    use_alt_click_leader=False,
    use_pie_click_drag=False,
    use_file_single_click=False,
    use_alt_navigation=True,
))
common_intro = [
    "Generated 2026-10-23 from the keymap source of the Moritz fork (Blender 5.3, branch "
    "`blender-v5.3-release`), so it lists every binding, not a selection.",
    "",
    "- **Key**: modifiers + key + event. No event word means *press*. `[Ctrl]` means either state.",
    "- **Action**: the operator's UI name; for modal keymaps, the modal item.",
    "- Windows/Linux keys; on macOS Blender maps Ctrl to Cmd for most items.",
    "- Bindings marked *(Moritz)* are Moritz additions.",
]
write(os.path.join(DOCS, "shortcuts_blender_full.md"),
      "Blender 5.3 — complete default keymap",
      common_intro + ["- Preset settings: left-click select, Spacebar = Play, Tool Keys = Immediate, "
                      "MMB = Orbit, Alt-MMB = Relative, gizmo on drag, Alt navigation on."],
      default_data)

ic_data = ic.generate_keymaps(ic.Params(use_mouse_emulate_3_button=False))
write(os.path.join(DOCS, "shortcuts_blender_industry_compatible_full.md"),
      "Blender 5.3 — complete Industry Compatible keymap",
      common_intro + ["- The Industry Compatible preset (Maya/Max-like); default settings."],
      ic_data)

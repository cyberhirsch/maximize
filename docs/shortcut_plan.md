# Moritz shortcut plan

Which keys follow 3ds Max, which stay Blender, and where Maya (or Unreal) is the better model.
Data: [shortcuts.md](shortcuts.md), [shortcuts_max_maya_full.md](shortcuts_max_maya_full.md), the complete Blender lists and the [comparison page](shortcut_comparison.html). Current Max keymap: `blender/scripts/addons_core/maximize/keymap_max.py`.

## Rules

Apply them in this order. The first rule that has an answer wins.

1. **Max, where Max has a default key for the same action in the same context.** Max users are the audience. Muscle memory in the viewport and in Edit Poly is what they notice in the first hour.
2. **The industry standard, where Max has no key or no such editor.** The keymap is built on Blender's Industry Compatible keymap, which already follows the keys that Maya, Unreal and other DCCs share (W/E/R, F to frame, Alt+mouse navigation in node and 2D editors). Animation and rigging lean on Maya, because the pipelines (Unreal, game studios) do.
3. **Blender, where neither Max nor Maya has the feature.** That covers sculpting, painting, Grease Pencil, Geometry Nodes, the sequencer and text editing. Industry Compatible already chose sensible keys for these.
4. **Never bury a Blender strength without a way back.** If a Max key replaces a Blender power key, the Blender function stays reachable through another key, the quad menu, F3/X search or a preference.
5. **Contested keys get a preference, not a fight.** Max has a "Maya interaction mode" option of its own; Moritz offers the same kind of switch. The Blender keymap stays one click away for following Blender tutorials.

## Decisions by area

Status: ✅ done in `keymap_max.py` · 🟡 partly done · ⬜ to do.

| Area | Follows | Why | Status |
|---|---|---|---|
| Viewport navigation (MMB pan, Alt+MMB orbit, Ctrl+Alt+MMB zoom, wheel) | **Max** | The top complaint in the research (15 of 27 sources) | ✅ |
| Views and zoom extents (T B F L P U C, Z, Ctrl+Alt+Z, Ctrl+Shift+Z, Alt+W, Alt+Q) | **Max** | Daily use | ✅ |
| Numpad views (Num 1/3/7/5/0/.) | **Blender**, as a bonus | Max doesn't use the numpad, so there's no conflict, and Blender tutorials keep working | ✅ |
| Display toggles (F3, F4, Alt+X, G, 7, Shift+C/L/G/H) | **Max** | Daily use | ✅ |
| Selection (click, Ctrl adds, Alt removes, Ctrl+A/D/I, H) | **Max** | Daily use; Shift selecting is the most common surprise for Max users | ✅ |
| Transform tools Q W E R | **Max = Maya = Unreal** | All three agree | ✅ |
| Transform dialogs (F12 Type-In, Alt+A Align, Insert Affect Pivot) | **Max** | Daily use | ✅ |
| Axis constraints while transforming | **Max and Blender** | Add Max's F5/F6/F7 (X/Y/Z) and F8 (plane cycle); keep Blender's X/Y/Z and typed numbers during a drag, which Max users like once they find them | ✅ F5–F8 during transforms |
| Snaps (S, A, Shift+S, Alt+S) | **Max** | Daily use | 🟡 S and A done |
| Clone (Ctrl+V, Shift+drag, Shift+drag on gizmo) | **Max** | Daily use | ✅ |
| Sub-object levels 1–5 and 6/Top | **Max** | Daily use; Blender puts collections here, which Max users never miss | ✅ |
| Edit Poly (Alt+L/R, Ctrl+PgUp/PgDn, Shift+E, Ctrl+Shift+C/B/E/W, Alt+C, Alt+1, Ctrl+Alt+C, Backspace, Del) | **Max** | Daily use | ✅ |
| Rest of Edit Poly / Editable Poly (61 rows: Shift+B soft selection, Alt+Shift+X ignore backfacing, Alt+Shift+E extrude face, Alt+N normal align…) | **Max** | Complete the table | ⬜ |
| Quad menu on right-click | **Max** | Signature Max UI | ✅ |
| Undo / redo, repeat last | **Max** (Ctrl+Z / Ctrl+Y, `;`) with Ctrl+Shift+Z still redoing outside the viewport | Ctrl+Y is the Windows standard too | ✅ |
| Hold / Fetch (Ctrl+H / Ctrl+Alt+F) | **Max** | Cheap to build: save and reload a temporary file | ⬜ |
| Undo / redo viewport change (Shift+Z / Shift+Y) | **Max** | Blender has view history only partly; needs a small operator | ✅ |
| Render (F9, F10, Shift+Q) | **Max** | Daily use | ✅ |
| Timeline and playback (`/` play, `,` `.` frames, Home/End, K set key, N auto key) | **Max**, plus Space = play | Max has no Space binding in the viewport except the quad-menu lock, so Space can keep Play like Maya, Unreal and Blender | ✅ |
| Graph Editor, Dope Sheet | **Maya**, plus Max where nothing clashes (K, Ctrl+A/D/I, Ctrl+Alt+Z) | Max's Track View keys are few and rarely used; animators coming from pipelines know Maya, and Industry Compatible is already Maya-like here | ⬜ |
| Pose mode, rigging | **Maya** (S set key, plus Max's K) | Rigify replaces Biped/CAT (out of scope); riggers moving to game engines know Maya | ⬜ |
| Splines (levels 1/2/3, Alt+Shift+1 Refine, Shift+drag extrude, Shift+click break tangent) | **Max** | Phase 3 Editable Spline tools | ⬜ (Phase 3) |
| UV editor | **Max Unwrap UVW** (Shift+X Relax, Shift+A Pack, Ctrl+B Break, Q Freeform, Ctrl+PgUp/PgDn, Alt+H…) | Max users unwrap in Max; the table is long (96 rows) and complete | ⬜ (with Phase 2 Unwrap UVW) |
| Shader / material node editor | **Max Slate** where it has a key (L lay out, H hide unused, P parameters, A assign, F2 rename, Q select, Ctrl+A/D/I), **Unreal / Industry Compatible** for wiring (Tab or right-click search, Alt+click to cut a link) | Slate has keys for layout, none for wiring | ⬜ |
| Geometry Nodes, compositor | **Blender / Industry Compatible** with Unreal-style node wiring | Max Creation Graph has no keys | — keep |
| Sculpt, weight / vertex / texture paint | **Blender** | Max has almost nothing comparable (Viewport Canvas has 8 keys) | — keep |
| Grease Pencil, sequencer, text editor, console, file browser | **Blender / OS standard** | No Max equivalent | — keep |
| Outliner (Scene Explorer) | **Industry Compatible** plus Max's F2 rename | Scene Explorer has few keys | ✅ |
| File and window (Ctrl+N/O/S, Ctrl+Shift+S, Ctrl+Alt+S) | **Max = OS standard** | Already identical | ✅ |

## Contested keys

| Key | Max | Maya / Unreal / Blender IC | Blender | Decision | Preference |
|---|---|---|---|---|---|
| F | Front view | Frame selected | — | **Max**; Z frames the selection | "F frames selection (Maya)" moves Front to Ctrl+F |
| Alt+LMB | Subtract from selection | Orbit | — | **Max** | "Maya navigation": Alt+LMB orbit, Alt+MMB pan, Alt+RMB zoom, Shift/Ctrl selection; the same switch Max has |
| Space | Quad-menu lock | Play | Play | **Play** | — |
| Tab | — | Search (IC) | Edit Mode | **Toggle Edit Poly** at the last sub-object level; search stays on X | — |
| X | Global Search | Snap toggle (IC) | Delete | **Max** | — |
| Ctrl+D | Select None | Duplicate | — | **Max**; cloning is Ctrl+V and Shift+drag | — |
| Ctrl+Shift+Z | Zoom Extents All | Redo | Redo | **Max in the viewport**, redo elsewhere; Ctrl+Y redoes everywhere | — |
| G / R / S | Grid / Scale tool / Snap | Repeat / Scale / Set key | Grab / Rotate / Scale (modal) | **Max** | "Blender modal keys": Ctrl+Shift+G/R/S start Blender's free modal transforms |
| H | Select by Name | Hide (IC Ctrl+H) | Hide | **Max**; hide is Alt+H, Alt+I, Alt+U | — |
| 1–5 | Sub-object levels | Component modes (IC 1–3) | Collections | **Max** | — |
| Del / Backspace | Delete / Remove (Edit Poly) | Delete | Delete menu / — | **Max** | — |
| F1–F12 | Help, F2 shade faces, F3 wire, F4 edges, F5–F8 constraints, F9/F10 render, F12 Type-In | IC: views on F1–F4 | F2 rename, F3 search | **Max**; F2 renames in the Outliner and node editors (Max does that there too) | — |
| Ctrl+C / Ctrl+V | Camera from view / Clone | Copy / Paste | Copy / Paste | **Max** in the 3D viewport only; copy and paste everywhere else | — |

## Selection presets

Three presets: **Max**, **Moritz** (default) and **Blender**. Moritz keeps Max's modifier keys (muscle memory) and adds Blender's ideas where Max has nothing comparable.

| Behavior | Max | Blender | Moritz |
|---|---|---|---|
| Add to selection | Ctrl+click | Shift+click | **Ctrl+click**; Ctrl+click on a selected item removes it |
| Remove from selection | Alt+click | Shift+click on a selected item | **Alt+click** |
| Shift | Clone (objects), extrude (edges) | Toggle selection | **Max**: clone and extrude, never selection |
| Click on empty space | Deselect all | Deselect all | Deselect all, unless a modifier is held |
| Window / crossing | Fixed setting (crossing), "by direction" is a preference | Always crossing | **By direction, on by default**: left to right = window, right to left = crossing |
| Region shape | Q repeated cycles rectangle, circle, fence, lasso, paint | B / C / lasso tools | **Max's Q cycle**; the last shape is remembered |
| Repeated click on one spot | Same object | Cycles through overlapping objects | **Blender's cycle** |
| Hover highlight | Yes | No | **Yes**, objects and sub-objects |
| Hidden sub-objects | Selects back faces unless Ignore Backfacing | Visible only, unless X-ray | **Visible only**; Alt+Shift+X selects through |
| Hidden objects | Everything in the region | Visible only in solid shading | **Everything in the region** (Max) |
| Loop | Double-click edge, Alt+L | Alt+click | **Double-click**, Alt+L; Alt+click stays "remove" |
| Ring | Alt+R | Ctrl+Alt+click | **Alt+R**, Ctrl+Alt+double-click |
| Shortest path | — | Ctrl+click | **Ctrl+Shift+click** |
| Double-click object | Selects it and its children | — | **Selects it and its children** |
| Active object | Not shown | Highlighted, used by Align, Parent, Join | **Kept**, shown in a lighter color |
| Change sub-object level | Ctrl+click converts the selection | Ctrl+click converts | Ctrl converts; Shift keeps only the border |

## Steps

1. **Coverage check script** (`tools/check_max_keymap.py`). Read the Main UI and Edit Poly tables from `shortcuts_max_maya_full.md`, map each Max action to a Blender operator (a small hand-kept mapping table), and report which keys the Max keymap covers, which clash and which have no Moritz feature yet. This turns the plan into a number we can track. ✅ Report: [shortcut_coverage.md](shortcut_coverage.md). First run: 99 of 216 keys OK, 4 conflicts (Ctrl+Shift+A, Shift+I, Shift+S, Up), 33 unbound but the feature exists, 80 with no Moritz feature yet.
2. **Finish the Max Main UI table** (163 + 25 rows): F5–F8, Shift+Z/Y, Ctrl+H/Ctrl+Alt+F, Alt+N, Shift+B, Alt+Shift+X, Ctrl+Shift+N selection lock, Alt+` show end result, and the rest the script lists. Skip rows for Max-only systems (Asset Tracking, MAXScript, State Sets).
3. **Restore free Blender keys**: numpad views and the other bindings Max leaves unused, so Blender tutorials work as far as possible. ✅ Numpad views; menus and tooltips also show Blender's key (Moritz core).
4. **Preferences**: "Maya navigation", "F frames selection" and "Blender modal keys", each a patch on top of `keymap_max.py`. ✅ In Preferences > Keymap under the Max and Moritz keymaps (Moritz's presets).
5. **Editors**: Graph Editor and Dope Sheet (Maya + Max), shader editor (Slate + Unreal wiring), Outliner (F2). ✅ F2, Ctrl+A/D/I, K, Ctrl+Alt+Z, Slate's H and P. Later, with their phases: UV editor (Unwrap UVW, Phase 2) and splines (Phase 3).
6. **Verify** ✅: add a "Moritz" column to the [comparison page](shortcut_comparison.html), so every common Max action shows the Moritz key next to Max's; extend the background test to assert the keys; then a hand test.

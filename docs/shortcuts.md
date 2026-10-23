# Default shortcuts: 3ds Max, Maya, Unreal Editor, Blender

Reference for designing Moritz's 3ds Max-style keymap. Compiled 2026-10-22.

This file is a selection. Complete lists:
- [Blender 5.3, complete default keymap](shortcuts_blender_full.md) (3,295 bindings, generated from the keymap source)
- [Blender 5.3, complete Industry Compatible keymap](shortcuts_blender_industry_compatible_full.md) (2,785 bindings)
- [3ds Max and Maya 2026, complete reference](shortcuts_max_maya_full.md) (Max 965 rows in 44 tables, Maya 661 rows in 51 tables, from Autodesk Help; checked against 2027)
- [Shortcut comparison page](shortcut_comparison.html) (colored table, by-key view, keyboard heatmaps)
## Versions and sources

| App | Version(s) | Source |
|---|---|---|
| 3ds Max | 2026, 2027 | Autodesk Help, "Keyboard Shortcut Tables" (raw CloudHelp HTML): [2026](https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-A73E1B09-7BFE-4A22-8153-1D3D2237B8E9.htm), [2027](https://help.autodesk.com/cloudhelp/2027/ENU/3DSMax-Basics/files/GUID-A73E1B09-7BFE-4A22-8153-1D3D2237B8E9.htm). The 2027 tables are identical to 2026. Mouse navigation is from the [Zoom](https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-CCD2C70B-52B4-4BF0-A5C0-74ECC591ACDD.htm), [Orbit](https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-6DA741AB-9941-4957-903A-4B998C1C65E7.htm), [Pan View](https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-802A4CCA-1695-4D91-BC30-9A4C0DAEEE5F.htm), [Select Object](https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-6CEB9419-A182-430C-9C6C-FEE5799324E0.htm), [Shift+Clone](https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-03F84C88-6EEC-42A4-BCB9-C487243E7B99.htm) and [Track Bar](https://help.autodesk.com/cloudhelp/2026/ENU/3DSMax-Basics/files/GUID-A55E4702-263E-4768-9964-5866698784DA.htm) pages. The keyboard-map images on "Default Hotkey Maps" were not used. |
| Maya | 2026, 2027 | Autodesk Help, Maya Keyboard Shortcuts book (raw CloudHelp HTML), mainly [All Maya Hotkeys 2026](https://help.autodesk.com/cloudhelp/2026/ENU/Maya-KeyboardShortcuts/files/GUID-30CACC9D-8FBE-4B85-8A8F-C5ADF32DDD4E.htm) and its per-category pages (Camera, Display, View, Selection, Tool, Snapping, Transformation, Edit, File, Interface, Modeling, Modeling Toolkit, Rendering, UV Editor, Animation, Marking Menus). Also used: Basics pages on [Node Editor/Hypershade hotkeys](https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-8E175070-AB7C-41A2-B0D7-85E842F83C4E.htm) and [camera tumble/track/dolly](https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Basics/files/GUID-941480C1-9BDA-4DB3-8EA8-113A0D6FAF1F.htm), plus the Modeling pages on [Multi-Cut](https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-21E402B5-1ABF-4DD3-A9CE-8B7957F6DF2B.htm) and [Extrude](https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Modeling/files/GUID-77FF95F8-13E8-48A6-BF82-84078E1F4FD3.htm). [2027 All Maya Hotkeys](https://help.autodesk.com/cloudhelp/2027/ENU/Maya-KeyboardShortcuts/files/GUID-30CACC9D-8FBE-4B85-8A8F-C5ADF32DDD4E.htm) was diffed against 2026: no hotkey changed, and a Walk Tool table was added. `www.autodesk.com/shortcuts/maya` returned HTTP 403 and could not be fetched. |
| Unreal Engine editor | 5.6, 5.7 | Epic has **no single editor-hotkey page** for 5.6 or 5.7. Entries come from individual pages at `https://dev.epicgames.com/documentation/en-us/unreal-engine/<slug>`, fetched with `?application_version=5.6` and `5.7`: `viewport-controls-in-unreal-engine`, `viewport-modes-in-unreal-engine`, `level-editor-modes-in-unreal-engine`, `transforming-actors-in-unreal-engine`, `actor-snapping-in-unreal-engine`, `grouping-actors-in-unreal-engine`, `ineditor-testing-play-and-simulate-in-unreal-engine`, `playing-and-simulating-in-unreal-engine`, `sequencer-hotkeys-in-unreal-engine`, `blueprint-editor-cheat-sheet-in-unreal-engine`, `unreal-engine-material-editor-ui`, `modeling-mode-in-unreal-engine`. Three pages were fetched for 5.6 only: `content-browser-in-unreal-engine`, `global-asset-picker-in-unreal-engine` and `using-live-coding-to-recompile-unreal-engine-applications-at-runtime`. No shortcut differs between 5.6 and 5.7. **Secondary:** the Epic [UEFN shortcut page](https://dev.epicgames.com/documentation/en-us/uefn/keyboard-shortcuts-in-unreal-editor-for-fortnite), which covers Unreal Editor for Fortnite rather than UE 5.6/5.7, and the UE 4.26 Viewport Options docs, seen in search results only. |
| Blender | 5.3 (Moritz fork) | Extracted from the keymap source by running `generate_keymaps()` from `blender/scripts/presets/keyconfig/keymap_data/blender_default.py` with the default preset preferences in `Blender.py`: Left select, Spacebar = Play, Tool Keys = Immediate, MMB = Orbit, Alt-MMB = Relative, gizmo drag, fallback tool, Alt navigation on. Industry Compatible comes from `generate_keymaps_impl()` in `industry_compatible_data.py`. Excluded: the Moritz addition (header LMB click-drag → `screen.area_join`), and the MMB-drag variants of transform tools that `keymap_transform_tool_mmb()` adds at runtime. |

### Legend

- **LMB / MMB / RMB** = left / middle / right mouse button. **Wheel** = scroll wheel. **drag** = press and move; **click** = press and release without moving.
- `A / B` = two related shortcuts in the same order as the action text (for example "Move / Rotate" → `W / E`).
- **[hold]** = the key must be held while doing something else.
- **—** = no default shortcut found in the source. For Blender this is certain, because the full keymap was read. For the other apps it means the official docs list none.
- **†** = from a secondary or non-version-specific source. Verify before relying on it.
- **(tool)** = in Blender Industry Compatible (IC), the key activates a toolbar tool rather than running a modal operator.
- Numpad keys are written `Num7`, `Num.` and so on. Blender `Ctrl` becomes `Cmd` on macOS.

---

## 1. Cross-reference by action

### Viewport navigation

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| Orbit / tumble | Alt+MMB drag | Alt+LMB drag | Alt+LMB drag (orbit pivot); RMB drag = look around | MMB drag | Alt+LMB drag |
| Pan / track | MMB drag | Alt+MMB drag | MMB drag; Alt+MMB drag (track) | Shift+MMB drag | Alt+MMB drag |
| Zoom / dolly (drag) | Ctrl+Alt+MMB drag | Alt+RMB drag | Alt+RMB drag | Ctrl+MMB drag (zoom); Ctrl+Shift+MMB drag (dolly) | Alt+RMB drag |
| Zoom (wheel) | Wheel | — (not in docs) | Wheel = step forward/back | Wheel | Wheel |
| Fly / walk | Up arrow (WalkThrough) | Walk Tool table (2027) lists keys, no entry key | RMB [hold] + W/A/S/D/Q/E | Shift+` (fly/walk navigation) | — |
| Frame selected | Z (Zoom Extents Selected) | F | F | Num. | F |
| Frame all | Ctrl+Alt+Z | A | — | Home | A |
| Frame in all views | Shift+Ctrl+Z (Zoom Extents All) | Shift+F (selected) / Shift+A (all) | — | Ctrl+Num. (selected) / Ctrl+Home (all) | Shift+A (all) |
| Zoom region / border | Ctrl+W | Alt+Ctrl+drag box | — | Shift+B | Z |
| Maximize viewport | Alt+W | Ctrl+Space (full screen); Space tap (single/multi pane) | F11 (immersive) | Ctrl+Space | — |
| Undo / redo view change | Shift+Z / Shift+Y | [ / ] | — | — | — |
| Center view on clicked point | I (pan to cursor) | — | — | Alt+MMB click | Shift+F |
| Toggle quad view | — (Alt+W maximize toggle) | Space tap | — | Ctrl+Alt+Q | — |

### Views and cameras

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| Top | T | — | Alt+J † | Num7 | F3 |
| Bottom | — | — | Alt+Shift+J † | Ctrl+Num7 | Ctrl+F3 |
| Front | F | — | Alt+H † | Num1 | F1 |
| Back | — | — | Alt+Shift+H † | Ctrl+Num1 | Ctrl+F1 |
| Left | L | — | Alt+K † | Ctrl+Num3 | Ctrl+F2 |
| Right | — | — | Alt+Shift+K † | Num3 | F2 |
| Perspective | P (perspective user view) | — | Alt+G † | Num5 (toggle persp/ortho) | — |
| Orthographic user view | U | — | — | Num5 | — |
| Camera view | C | — | — | Num0 | F4 |
| Camera from view / align camera to view | Ctrl+C (create Physical camera from view) | — | — | Ctrl+Alt+Num0 | — |
| View menu / pie | V (Viewports quad) | Space [hold] (hotbox) | — | ` (view pie) | V (view pie) |
| Game view (hide editor-only items) | — | — | G | — | — |

### Selection

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| Select tool | Q (Smart Select) | Q | Q | W (cycles select tools) | Q (tool) |
| Select all | Ctrl+A | — | — | A | Ctrl+A |
| Deselect all | Ctrl+D | — | — | Alt+A or A double-tap | Ctrl+Shift+A |
| Invert selection | Ctrl+I | — (Ctrl+Shift+I in UV Editor) | — | Ctrl+I | Ctrl+I |
| Add to selection | Ctrl+click | Ctrl+Shift+click (always add) | Ctrl+click or Shift+click | Shift+click (toggle) | Shift+click (toggle) |
| Remove from selection | Alt+click | Ctrl+click | Ctrl+RMB drag (ortho marquee) | Shift+click (toggle) or Ctrl+LMB drag box | Ctrl+LMB drag box (tool) |
| Toggle selection | — | Shift+click | Ctrl+click (Blueprint graph) | Shift+click | Shift+click |
| Box / lasso / circle | drag; Ctrl+F cycles region type | drag | LMB drag (ortho views) | B / Ctrl+RMB drag / C | LMB drag (tool) |
| Select by name | H | — | — | — (Outliner Ctrl+F filter) | — |
| Select similar / same | Ctrl+Shift+A | — | Shift+E (same static mesh) | Shift+G (grouped/similar) | — |
| Grow / shrink selection | Ctrl+PgUp / Ctrl+PgDn | > / < | — | Ctrl+Num+ / Ctrl+Num− | Up / Down arrow |
| Select parent / child | PgUp / PgDown | Up / Down arrow (pickwalk) | — | [ / ] | [ / ] |
| Lock selection | Space (as listed) / Ctrl+Shift+N | — | — | — | — |

### Transform tools and pivot

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| Move | W | W | W | G (modal) | W (tool) |
| Rotate | E | E | E | R (modal) | E (tool) |
| Scale | R (Smart Scale; Ctrl+E cycles) | R | R | S (modal) | R (tool) |
| Combined / universal manipulator | — | Ctrl+T (universal); T (show manipulator) | Space (cycle gizmo) | — | T (Transform tool) |
| Gizmo size up / down | = / − | = or + / − | — | — | — |
| Gizmo visibility toggle | — | — | — | Ctrl+` | — |
| Axis constraint X / Y / Z | F5 / F6 / F7 | — | — | X / Y / Z (during transform) | X / Y / Z (during transform) |
| Plane constraint | F8 (cycle) | — | — | Shift+X / Shift+Y / Shift+Z (during transform) | same |
| Numeric type-in | F12 (Transform Type-In) | — | — | type a number during transform; N sidebar | Ctrl+] sidebar |
| Edit pivot only | Insert (Affect Pivot Only) | D [hold] + drag; Insert | MMB drag on pivot (temporary) | Ctrl+. (affect only origins) | — |
| Pivot point menu | Alt+Shift+5 (Center Point Cycle) | — | — | . (pie) | . (pie) |
| Transform orientation | — | — | Ctrl+` (world/local) | , (pie) | , (pie) |
| Clone while transforming | Shift+drag | Shift+drag manipulator (object mode) | Alt+LMB drag on gizmo | Shift+D (duplicate, then move) | Ctrl+D |
| Duplicate / clone | Ctrl+V (Clone) | Ctrl+D; Shift+D (with transform) | Ctrl+W (duplicate in place); Ctrl+D † | Shift+D; Alt+D (linked) | Ctrl+D |
| Reset location / rotation / scale | — | — | — | Alt+G / Alt+R / Alt+S | Alt+W / Alt+E / Alt+R |
| Align | Alt+A (Align); Shift+A (Quick Align); Alt+N (Normal Align) | — | End (snap to floor) | — | — |
| Repeat last | ; (Editable Poly) | G; Shift+G (at mouse position) | — | Shift+R | G |

### Snapping

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| Snap toggle | S | — | — (toolbar only) | Shift+Tab | X |
| Snap to grid / curve / point | — | X / C / V [hold] | — | — | — |
| Vertex snap | — | V [hold] | V [hold] (Translate gizmo) | Ctrl [hold] during transform (inverts snap toggle) | same as Blender |
| Angle snap toggle | A | — | — | — | — |
| Snap menu / options | Shift+RMB (Snap quad); Alt+S cycles snap type | J [hold] (Move/Rotate/Scale snapping) | — | Shift+S (pie); Ctrl+Shift+Tab (panel) | Shift+X (pie) |

### Display and isolate

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| Wireframe / shaded toggle | F3 | 4 (wire) / 5 (shaded); Alt+5 toggle | Alt+2 (wire) / Alt+4 (lit) | Shift+Z (wireframe toggle); Z (shading pie) | — |
| Edged faces / wire on shaded | F4 | — | — | — (Overlays) | — |
| See-through / X-ray | Alt+X | — | — | Alt+Z | Alt+X |
| Toggle overlays / grid | G (grid) | — | — | Alt+Shift+Z (overlays) | — |
| Statistics | 7 | — | Ctrl+L † | — | — |
| Hide selected | Alt+H | Ctrl+H | H | H | Ctrl+H |
| Hide unselected | Alt+I | Alt+H | — | Shift+H | Shift+H |
| Unhide all | Alt+U | Shift+H (show selection); Ctrl+Shift+H (show last hidden) | Ctrl+H | Alt+H | Alt+H |
| Isolate selection | Alt+Q; Ctrl+Alt+Q (toggle) | Ctrl+1 | — | / or Num/ (local view) | Shift+I |
| Smooth / subdiv preview | — | 1 / 2 / 3 | — | Ctrl+0…5 (adds Subdivision modifier) | Ctrl+0…5; D / Shift+D (±1 level) |

### Modeling / edit mesh

| Action | 3ds Max (Editable/Edit Poly) | Maya | Unreal (Modeling mode) | Blender (Edit Mesh) | Blender IC |
|---|---|---|---|---|---|
| Enter edit / component mode | 1–5 (enter a sub-object level); Ctrl+B (toggle sub-object selection) | F8 (object/component toggle) | Shift+5 (Modeling mode) | Tab (Object/Edit); Ctrl+Tab (mode pie) | 1 / 2 / 3 (enter Edit Mode at vert/edge/face); 4 (Object Mode); 5 (mode pie) |
| Vertex / edge / face level | 1 / 2 / 4 (Editable Poly order: 1 vertex, 2 edge, 3 border, 4 polygon, 5 element) | F9 / F10 / F11 (F12 = UV) | — | 1 / 2 / 3 | 1 / 2 / 3 |
| Convert selection | — | Ctrl+F9 / F10 / F11 / F12; Ctrl+RMB menu | — | Ctrl+1 / 2 / 3 (expand) | Ctrl+1 / 2 / 3 |
| Extrude | Shift+E; Alt+Shift+E (Extrude Face, main UI); Shift+drag with Move (Edit Poly) | Ctrl+E; Shift+drag manipulator (component mode) | — | E; Alt+E (menu) | Ctrl+E (tool) |
| Bevel / chamfer | Ctrl+Shift+B (bevel); Ctrl+Shift+C (chamfer) | — | — | Ctrl+B (edges); Ctrl+Shift+B (vertices) | Ctrl+B (tool) |
| Inset | Shift+drag with Scale (Edit Poly) | — | — | I | I (tool) |
| Loop select | Alt+L | — | — | Alt+click | LMB double-click |
| Ring select | Alt+R | — | — | Ctrl+Alt+click | Alt+LMB double-click |
| Insert loop / loop cut | Alt+3 (Insert Loop); Alt+1 (Swift Loop) | Ctrl+click in Multi-Cut | — | Ctrl+R | Alt+C (tool) |
| Connect | Shift+Ctrl+E | — | — | J (vertex connect path) | — |
| Weld / merge / collapse | Shift+Ctrl+W (Target Weld); Ctrl+Alt+C (Collapse); Alt+Shift+W (Weld, Edit Mesh) | — | — | M (merge menu) | — |
| Cut / knife | Alt+C | Ctrl+Shift+X (Multi-Cut) | — | K; Shift+K (selected only) | K (tool) |
| Attach / join | Alt+Shift+D (Attach) | — | — | Ctrl+J (object mode) | — |
| Detach / separate | Ctrl+Alt+D (Detach) | — | — | P (separate); Y (split) | — |
| Break / rip | Shift+R (Break) | — | — | V (rip); Alt+D (rip edge) | — |
| Cap / fill | Alt+P (Cap) | — | — | F (make edge/face); Alt+F (fill) | — |
| Delete / dissolve | Del (objects) | — | — | X or Del (menu); Ctrl+X or Ctrl+Del (dissolve) | Backspace or Del (menu); Ctrl+Backspace or Ctrl+Del (dissolve) |
| Slice / bisect | Shift+Ctrl+Q (Quickslice) | — | — | — | — |
| Soft selection / proportional editing | Shift+B (toggle); B (edit mode) | B (Modeling Toolkit) | — | O; Shift+O (falloff pie) | B |
| Smooth / subdivide | Ctrl+M (MeshSmooth) | — | — | — | — |
| Hide / unhide in sub-object mode | Alt+H / Alt+I / Alt+U | Ctrl+H / Shift+H | — | H / Shift+H / Alt+H | Ctrl+H / Shift+H / Alt+H |

### Hierarchy and grouping

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| Parent | — | P | — | Ctrl+P | P |
| Unparent | — | Shift+P | — | Alt+P | Shift+P |
| Group | Ctrl+U (Group Attach) | Ctrl+G | Ctrl+G | Ctrl+G (new collection) | — |
| Ungroup | — | — | Shift+G | Ctrl+Alt+G (remove from collection) | — |
| Move to collection / layer | — | — | — | M; Shift+M (link) | Ctrl+G; Ctrl+Shift+G (link) |

### Animation and timeline

| Action | 3ds Max | Maya | Unreal (Sequencer) | Blender | Blender IC |
|---|---|---|---|---|---|
| Set key | K | S | S (key location + rotation + scale); Enter (key selected tracks) | I (insert); K (keyframe menu) | S |
| Key translate / rotate / scale | — | Shift+W / Shift+E / Shift+R | Shift+W / Shift+E / Shift+R | — | Shift+W / Shift+E / Shift+R |
| Delete key | — | — | — | Alt+I | Alt+S |
| Auto key toggle | N | — | — | — | — |
| Play / stop | / (play) | Alt+V (play); Esc (stop) | Space (play/pause); K (pause) | Space; Esc (cancel); Ctrl+Shift+Space (reverse) | Space; Esc |
| Next / previous frame | . / , | Alt+. / Alt+, | Right / Left | Right / Left | Right / Left |
| Next / previous key | — | . / , | . / , (key or section bound) | Up / Down | — |
| Go to start / end | Home / End | Alt+Shift+V (min frame) | Up / Ctrl+Up | Shift+Left / Shift+Right | Ctrl+Left / Ctrl+Right |
| Scrub | Ctrl+Alt+drag on track bar (sets range) | K [hold] + MMB drag | — | Alt+Wheel (step frames) | — |
| Preview / play range | Ctrl+Alt+LMB / RMB drag on track bar | — | I / O (custom range); [ / ] (sequence start/end) | P / Alt+P (in timeline); Ctrl+Alt+P (Graph Editor, Dope Sheet) | — |
| Play in Editor | — | — | Alt+P (PIE); Alt+S (Simulate); Esc (stop); F10 (eject/possess) | — | — |

### Rendering

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| Render | Shift+Q or Shift+F9 | — | — | F12 | Ctrl+Enter |
| Render last | F9 | — | — | — | — |
| Render animation | — | — | — | Ctrl+F12 | Ctrl+Alt+Enter |
| Render setup | F10 | — | — | — | — |
| Show render window | — | — | — | F11 | — |
| Render region | — | — | — | Ctrl+B (set); Ctrl+Alt+B (clear) | — |
| Environment | 8 | — | — | — | — |

### File and scene

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| New | Ctrl+N | Ctrl+N | Ctrl+N † (new level) | Ctrl+N (menu) | Ctrl+N |
| Open | Ctrl+O | Ctrl+O | Ctrl+O † (open level); Ctrl+P (open asset) | Ctrl+O; Ctrl+Shift+O (recent) | Ctrl+O |
| Save | Ctrl+S | Ctrl+S | Ctrl+S | Ctrl+S | Ctrl+S |
| Save as | Ctrl+Shift+S | Ctrl+Shift+S | Ctrl+Alt+S † (save level as) | Ctrl+Shift+S | Ctrl+Shift+S |
| Save all / incremental | Ctrl+Alt+S (Save Incremental) | — | Ctrl+Shift+S † (Save All) | Ctrl+Alt+S (incremental) | Ctrl+Alt+S |
| Undo / redo | Ctrl+Z / Ctrl+Y | Ctrl+Z / Ctrl+Y (2026 docs; old 2014 list also gives Z and Shift+Z †) | Ctrl+Z / Ctrl+Y | Ctrl+Z / Ctrl+Shift+Z | Ctrl+Z / Ctrl+Shift+Z; Ctrl+Alt+Z (history) |
| Hold / fetch | Ctrl+H / Ctrl+Alt+F | — | — | — | — |
| Delete objects | Del | — | Delete † | X (confirm) / Del | Backspace / Del |
| Copy / paste objects | — | Ctrl+C / Ctrl+V | Ctrl+C / Ctrl+V † | Ctrl+C / Ctrl+V (3D View copybuffer) | Ctrl+C / Ctrl+V |
| Quit | — | Ctrl+Q | — | Ctrl+Q | Ctrl+Q |

### UI and windows

| Action | 3ds Max | Maya | Unreal | Blender | Blender IC |
|---|---|---|---|---|---|
| Command search | X (Global Search) | — | — | F3 | Tab |
| Context menu | RMB (quad menu) | RMB (marking menu) | RMB (Blueprint graph action menu) | RMB | RMB |
| Modifier quad / marking menus | Ctrl+RMB (modeling), Alt+RMB (animation), Shift+RMB (snap), Ctrl+Alt+RMB (lighting/render) | Shift+RMB (polygon tools), Ctrl+RMB (convert selection) | — | — | — |
| Popup / hotbox | — | Space [hold] (hotbox) | — | Shift+Space (toolbar popup) | Shift+Space (asset shelf) |
| Toolbar / properties panels | — | Ctrl+A (Attribute Editor ↔ Channel Box) | — | T (toolbar) / N (sidebar) | Ctrl+[ / Ctrl+] |
| Rename | — (F2 only in Schematic View / Slate) | — | F2 (Blueprint editor) | F2; Ctrl+F2 (batch rename) | Enter; Alt+Enter (batch rename) |
| Redo-last panel | — | — | — | F9 | — |
| Material / shader editor | M | — | — | Shift+F3 (node editor) | — |
| Scripting console | F11 (MAXScript Listener) | — | ~ (PIE console) | Shift+F4 (Python console) | — |
| Expert mode / hide UI | Ctrl+Alt+X | Ctrl+M / Shift+M / Ctrl+Shift+M (menu bars) | F11 (immersive) | Ctrl+Alt+Space | — |
| Preferences | — | — | — | Ctrl+, | Ctrl+, |
| Help / manual | — | F1 | F1 † | F1 (manual for the hovered item) | — |
| Content browser / asset picker | — | — | Ctrl+Space (Content Drawer); Ctrl+B (find in Content Browser) | — | — |
| Workspace / editor switching | — | F2 / F3 / F4 / F6 (menu sets) | Shift+1…8 (editor modes) | Ctrl+PgUp / Ctrl+PgDn (workspace); Shift+F1…F12 (editor type) | — |

---

## 2. 3ds Max 2026/2027 (full default list, Main UI and key contexts)

Source: "Keyboard Shortcut Tables" (2026/2027), unless noted. The **Keyboard Shortcut Override** toggle is on by default, so context keys (Editable Poly, Unwrap and others) take priority while that context is active.

### Viewport navigation (mouse, 3ds Max interaction mode)
| Action | Shortcut |
|---|---|
| Pan | MMB drag |
| Orbit | Alt+MMB drag |
| Zoom | Ctrl+Alt+MMB drag; Wheel |
| Zoom faster / slower | Ctrl / Alt [hold] while zooming |
| Pan constrained to one axis / faster | Shift / Ctrl [hold] while panning |
| Exit navigation mode | Esc or RMB |
| Maya interaction mode (option) | Alt+LMB orbit, Alt+MMB pan, Alt+RMB zoom, A = Zoom Extents All |

### Viewport navigation (keyboard)
| Action | Shortcut |
|---|---|
| Zoom Extents Selected / Zoom Extents / Zoom Extents All | Z / Ctrl+Alt+Z / Shift+Ctrl+Z |
| Zoom mode / Zoom Region mode / Zoom In 2X | Alt+Z / Ctrl+W / Ctrl+Alt+Shift+Z |
| Zoom viewport in / out | [ or Ctrl+= / ] or Ctrl+− |
| Pan View / Pan to cursor | Ctrl+P / I |
| Orbit mode / WalkThrough | Ctrl+R / Up arrow |
| Home view / ViewCube home / ViewCube visibility | Alt+Home / Alt+Ctrl+H / Alt+Ctrl+V |
| Maximize viewport toggle | Alt+W |
| Undo / redo viewport operation | Shift+Z / Shift+Y |
| Redraw all views | ` |
| Expert mode | Ctrl+Alt+X |
| Disable viewport | Ctrl+Shift+D |
| Virtual viewport toggle / pan / zoom | Num/ / Num8 Num2 Num4 Num6 / Num+ Num− |
| SteeringWheels toggle | Shift+W |

### Views
| Action | Shortcut |
|---|---|
| Top / Front / Left | T / F / L |
| Perspective / Orthographic user view | P / U |
| Camera view / Spot or directional light view | C / Shift+4 |
| Viewports quad menu | V |
| Create Physical camera from view | Ctrl+C or Alt+Shift+C |
| Create Standard camera from view | Ctrl+Alt+Shift+C |

### Selection and hierarchy
| Action | Shortcut |
|---|---|
| Smart Select / Select By Name | Q / H |
| Select all / none / invert / similar | Ctrl+A / Ctrl+D / Ctrl+I / Ctrl+Shift+A |
| Add to / remove from selection | Ctrl+click / Alt+click |
| Selection lock | Ctrl+Shift+N (Space listed in Quad Menu Sets) |
| Cycle selection region type / Window-Crossing toggle | Ctrl+F / Shift+O |
| Select ancestor / child / children | PgUp / PgDown / Shift+PgDown |
| Group Attach | Ctrl+U |

### Transform and snapping
| Action | Shortcut |
|---|---|
| Move / Rotate / Smart Scale / Scale cycle | W / E / R / Ctrl+E |
| Smart Place | Y |
| Gizmo size up / down | = / − |
| Constrain to X / Y / Z / cycle planes | F5 / F6 / F7 / F8 |
| Transform Type-In | F12 |
| Affect Pivot Only | Insert |
| Center Point Cycle | Alt+Shift+5 |
| Align / Quick Align / Normal Align / Spacing Tool | Alt+A / Shift+A / Alt+N / Shift+I |
| Clone / Shift+Clone | Ctrl+V / Shift+drag with Move, Rotate or Scale |
| Snaps toggle / Angle snap / Cycle snap type | S / A / Alt+S |
| Axis constraints in snaps | Alt+F3 |

### Display and visibility
| Action | Shortcut |
|---|---|
| Wireframe ↔ Smooth+Highlights / Edged faces / Shade selected faces | F3 / F4 / F2 |
| Selection brackets / selection-preview highlights | Shift+J / Alt+J |
| Grid / Adaptive degradation / Statistics | G / O / 7 |
| See-through / Safe frames | Alt+X / Shift+F |
| Hide cameras / geometry / helpers / lights | Shift+C / Shift+G / Shift+H / Shift+L |
| Hide particles / shapes / space warps | Shift+P / Shift+S / Shift+W |
| Hide selection / Hide unselected / Unhide all | Alt+H / Alt+I / Alt+U |
| Isolate selection / Isolate toggle | Alt+Q / Ctrl+Alt+Q |
| Default ↔ scene lights / High-quality lighting | Ctrl+L / Shift+F3 |
| Viewport background / update background image | Alt+B / Alt+Shift+Ctrl+B |

### Rendering, file, animation, UI
| Action | Shortcut |
|---|---|
| Render / Render last / Render setup | Shift+Q or Shift+F9 / F9 / F10 |
| Environment / Advanced lighting | 8 / 9 |
| Create animated sequence file | Shift+V |
| New / Open / Save / Save As / Save Incremental | Ctrl+N / Ctrl+O / Ctrl+S / Ctrl+Shift+S / Ctrl+Alt+S |
| Undo / Redo | Ctrl+Z / Ctrl+Y |
| Hold / Fetch | Ctrl+H / Ctrl+Alt+F |
| Delete objects / Asset tracking | Del / Shift+T |
| Auto Key / Set Key | N / K |
| Go to start / end / step back / forward / play / sound | Home / End / , / . / / / \ |
| Active time segment start / end / move both | Ctrl+Alt+LMB / RMB / MMB drag on track bar |
| Material Editor / MAXScript Listener / Global Search | M / F11 / X |
| Floating dialogs / Override toggle / Show end result | Ctrl+` / Ctrl+Alt+Shift+X / Alt+` |
| Quad menus | RMB (default); Ctrl+RMB (modeling); Alt+RMB (animation); Ctrl+Alt+RMB (lighting/render); Shift+RMB (snap); Ctrl+Shift+RMB, Ctrl+Alt+Shift+RMB (custom); J ("Windows" quad set) |
| Particle View | 6 |

### Editable Poly / Edit Poly (context) and PolyTools (Main UI)
| Action | Shortcut |
|---|---|
| Sub-object level 1–5 / sub-object selection toggle | 1–5 / Ctrl+B |
| Loop / Ring / Grow / Shrink | Alt+L / Alt+R / Ctrl+PgUp (Ctrl+Up) / Ctrl+PgDn (Ctrl+Down) |
| Extrude / Bevel / Chamfer | Shift+E / Ctrl+Shift+B / Ctrl+Shift+C |
| Connect / Cut / Collapse | Shift+Ctrl+E / Alt+C / Ctrl+Alt+C |
| Attach / Detach / Break / Cap | Alt+Shift+D / Ctrl+Alt+D / Shift+R / Alt+P |
| Target Weld / Quickslice / Extrude along spline | Shift+Ctrl+W / Shift+Ctrl+Q / Ctrl+Alt+Shift+E |
| MeshSmooth / Make Planar (Edit Poly) / Constrain to edges | Ctrl+M / Alt+M / Shift+X |
| Repeat last operation | ; |
| Ignore backfacing / Soft selection / Edit soft selection | Alt+Shift+X / Shift+B / B |
| Extrude / Clone / Inset polygons (Edit Poly) | Shift+drag with Move / Ctrl+Shift+drag with Move / Shift+drag with Scale |
| Extrude Face (Main UI) | Alt+Shift+E |
| Swift Loop / Set Flow / Insert Loop / PolyShift / Spin Edge | Alt+1 / Alt+2 / Alt+3 / Alt+4 / Alt+5 |
| Straighten / Circle loops / Geo Poly / Spline Refine | Alt+Shift+2 / Alt+Shift+3 / Alt+Shift+4 / Alt+Shift+1 |
| Edit Mesh: Edge Turn / Weld Selected | Ctrl+T / Alt+Shift+W |

### Other contexts (summary)
| Context | Keys |
|---|---|
| Track View | K add/remove keys, M move keys, Left / Right nudge, C assign controller, U make unique, L lock tangents, S snap frames, Ctrl+Alt+Z frame extents, Ctrl+A / Ctrl+D / Ctrl+I select all / none / invert |
| Schematic View | Q select, C connect, Z / Ctrl+Alt+Z zoom selected / extents, Alt+H hide, F2 rename, G grid, B bookmark |
| Slate Material Editor | A assign, O browser, P parameter editor, N navigator, L / C lay out all / children, H hide unused slots, U update previews, Z zoom selected, F2 rename, Del delete |
| Compact Material Editor | A assign, O get material, F9 preview, Up / Left / Right navigate |
| Unwrap UVW | W / E / R transform, Q freeform, Ctrl+E edit UVWs, Alt+L / Alt+R loop / ring, Shift+X relax, Shift+S stitch, Shift+A pack, Ctrl+Q peel, Shift+R break, Alt+Shift+W weld, Shift+Ctrl+W target weld, Alt+H / Alt+U hide / unhide |
| WalkThrough | W / A / S / D or arrows move, E / C up / down, Q / Z accelerate / decelerate, ] / [ step size, Space lock vertical |

The help page also covers Biped, Hair, Particle Flow, FFD, NURBS, Physique, Reaction Manager, Video Post and PaintWeight. Those are omitted here.

---

## 3. Maya 2026/2027 (default hotkeys)

Source: the 2026 Maya Keyboard Shortcuts book (CloudHelp), unless marked †. 2027 adds only the Walk Tool table.

### Camera / view
| Action | Shortcut |
|---|---|
| Tumble / Track / Dolly | Alt+LMB / Alt+MMB / Alt+RMB drag (dolly also Alt+LMB+MMB) |
| Box dolly in / out | Alt+Ctrl+drag box left→right / right→left |
| Frame all / selected (active panel) | A / F |
| Frame all / selected (all views) | Shift+A / Shift+F |
| Undo / redo view change | [ / ] |
| Restore default view | Home |
| 2D pan / zoom (toggle with \) | \ + MMB / \ + RMB |
| Hotbox / single↔multi pane | Space [hold] / Space tap |
| Zoom pane / full-screen pane | Shift+Space / Ctrl+Space |
| Previous / next panel layout | Shift+{ / Shift+} |
| Cycle background colour | Alt+B |

### Selection
| Action | Shortcut |
|---|---|
| Select tool | Q |
| Toggle / remove / add | Shift+click / Ctrl+click / Ctrl+Shift+click |
| Object↔component / Vertex / Edge / Face / UV / Vertex Face | F8 / F9 / F10 / F11 / F12 / Alt+F9 |
| Grow / shrink | > / < |
| Pickwalk | arrow keys |
| Select next intermediate object | Ctrl+I |

### Transform, pivot, snapping
| Action | Shortcut |
|---|---|
| Move / Rotate / Scale (hold + LMB for marking menu) | W / E / R |
| Show manipulator / Universal manipulator / Last tool | T / Ctrl+T / Y |
| Manipulator size | = or + / − |
| Move pivot | D [hold] + drag; Insert toggles pivot mode |
| Complete tool / In-View Editor cycle | Enter / Tab, Shift+Tab |
| Snap to grid / curve / point | X / C / V [hold] |
| Tool snapping / relative snapping | J / Shift+J [hold] |
| Nudge 1 pixel | Alt+arrow keys |
| Move along normals / local rotate / local scale (component mode) | Ctrl+MMB drag |

### Display
| Action | Shortcut |
|---|---|
| Smoothness: no smoothing / cage+smooth / smooth | 1 / 2 / 3 |
| Wireframe / Shaded / Textured / All lights | 4 / 5 / 6 / 7 |
| Default quality display | 0 |
| Hide selection / Show selection / Show last hidden / Hide unselected | Ctrl+H / Shift+H / Ctrl+Shift+H / Alt+H |
| Isolate selection (view selected) | Ctrl+1 |
| Toggle NURBS curves / polygon / image plane visibility | Alt+1 / Alt+2 / Alt+4 |
| Wireframe ↔ shaded | Alt+5 |
| Smooth-mesh division levels up / down | PgUp / PgDn |
| Paint Effects panel | 8 † (2014 list only) |

### Modeling
| Action | Shortcut |
|---|---|
| Convert selection to Vertices / Edges / Faces / UVs | Ctrl+F9 / Ctrl+F10 / Ctrl+F11 / Ctrl+F12 |
| Extrude | Ctrl+E |
| Extrude (component mode) / Duplicate (object mode) | Shift+drag manipulator |
| Slide component along edge | Ctrl+Shift+drag manipulator |
| Multi-Cut / Quad Draw | Ctrl+Shift+X / Ctrl+Shift+Q |
| Multi-Cut: edge loop / finish / cancel | Ctrl+click / RMB or Enter / Esc |
| Multi-component mode / tweak / soft selection / pivot edit (Modeling Toolkit) | Ctrl+Tab / ` / B / D |
| Subdiv Proxy / options / proxy↔smooth / show both | Ctrl+` / Ctrl+Shift+` / ` / ~ |
| Polygon marking menu / object marking menu / convert-selection menu | Shift+RMB / RMB / Ctrl+RMB |

Bevel, insert edge loop, merge, combine and separate have **no** default hotkeys in the 2026 docs.

### Edit / file / interface
| Action | Shortcut |
|---|---|
| Undo / Redo | Ctrl+Z / Ctrl+Y (2026 docs). The 2014 list also gives Z / Shift+Z † |
| Repeat last / repeat at mouse | G / Shift+G |
| Duplicate / Duplicate Special / Duplicate with Transform | Ctrl+D / Ctrl+Shift+D / Shift+D |
| Group / Parent / Unparent | Ctrl+G / P / Shift+P |
| Cut / Copy / Paste | Ctrl+X / Ctrl+C / Ctrl+V |
| New / Open / Save / Save As / Exit | Ctrl+N / Ctrl+O / Ctrl+S / Ctrl+Shift+S / Ctrl+Q |
| Create reference | Ctrl+R |
| Attribute Editor ↔ Channel Box | Ctrl+A |
| Main menu bar / panel menu / panel toolbar | Ctrl+M / Shift+M / Ctrl+Shift+M |
| Menu sets: Modeling / Rigging / Animation / Rendering | F2 / F3 / F4 / F6 |
| Menu set marking menu / Help | H + LMB / F1 |

### Animation
| Action | Shortcut |
|---|---|
| Set key / key translate / rotate / scale | S / Shift+W / Shift+E / Shift+R |
| Insert key on channel | Ctrl+Shift+W / E / R |
| Insert keys at current time / Insert key on curve (Graph Editor) | Alt+I / I + MMB |
| Next / previous frame | Alt+. / Alt+, |
| Next / previous key | . / , |
| Play / stop / go to min frame | Alt+V / Esc / Alt+Shift+V |
| Scrub (virtual slider) | K [hold] + MMB drag |
| Select time range | Shift+drag on Time Slider |
| Bookmarks | Alt+T (window), Alt+Shift+T (quick), \| frame, Alt+\ unframe |
| Graph Editor: absolute / stacked / normalized | 1 / 2 / 3 |
| Graph Editor: auto tangents / center current time / move keys | D / T / Shift+9, Shift+0 |

### UV Editor / Node Editor & Hypershade
| Context | Keys |
|---|---|
| UV Editor | 4–7 display modes, A / F frame, Q / W / E / R tools, Ctrl+L layout, Ctrl+U unfold, Shift+X cut, Shift+S sew, Ctrl+Shift+X create shell |
| Node Editor / Hypershade | Tab create node, 1–4 view modes, Del delete, , / . / / select upstream / downstream / both, < / > / ? regraph, L layout, P pin, S attribute search |
| Walk Tool (2027) | W / A / S / D or arrows, Q up, E down, Ctrl crouch, LMB / MMB / RMB click = normal / slow / fast speed |

---

## 4. Unreal Engine 5.6 / 5.7 editor

Source: the official per-feature pages listed in the header. † marks entries from the UEFN page or UE 4.x docs.

### Viewport (perspective)
| Action | Shortcut |
|---|---|
| Move forward/back + turn | LMB drag |
| Look around | RMB drag |
| Move up/down/left/right | MMB drag |
| Step forward/back | Wheel |
| Camera speed | RMB [hold] + Wheel |
| Fly forward / back / left / right | RMB [hold] + W / S / A / D (also Num8/2/4/6 or arrow keys) |
| Up / down (world) | RMB [hold] + E / Q (also Num9 / Num7, PgUp / PgDn) |
| Up / down (local) | RMB [hold] + R / F |
| Change FOV | RMB [hold] + Z / C (also Num1 / Num3) |
| Focus selection | F |
| Orbit / Dolly / Track | Alt+LMB / Alt+RMB / Alt+MMB drag |
| Orthographic views: marquee / pan / zoom | LMB drag / RMB drag / LMB+RMB drag or Wheel |

### Selection, transform, display
| Action | Shortcut |
|---|---|
| Select / add | LMB / Ctrl+LMB or Shift+LMB |
| Ortho marquee add / remove | Shift+LMB drag / Ctrl+RMB drag |
| Select all actors with same static mesh | Shift+E |
| Select / Translate / Rotate / Scale tool | Q / W / E / R |
| Cycle gizmo / world↔local | Space / Ctrl+` |
| Vertex snap | V [hold] |
| Temporary pivot move | MMB drag on pivot |
| Duplicate while dragging / duplicate in place | Alt+drag gizmo / Ctrl+W |
| Snap to floor | End |
| Group / ungroup / toggle group selection | Ctrl+G / Shift+G / Ctrl+Shift+G |
| Set group pivot | Alt+MMB click (5.6 page) |
| Game view / realtime / immersive | G / Ctrl+R / F11 |
| Hide selected / show all | H / Ctrl+H |
| View modes: Wireframe / Unlit / Lit / Detail lighting / Lighting only / Light complexity / Shader complexity / Lightmap density | Alt+2 / 3 / 4 / 5 / 6 / 7 / 8 / Alt+0 |
| Editor modes: Select / Landscape / Foliage / Mesh Paint / Modeling / Fracture / Brush / Animation | Shift+1 … Shift+8 |
| Viewport type: Perspective / Top / Front / Left | Alt+G / Alt+J / Alt+H / Alt+K † |
| Bottom / Back / Right | Alt+Shift+J / Alt+Shift+H / Alt+Shift+K † |
| Set / jump to bookmark | Ctrl+0…9 / 0…9 † |
| FPS / stats / viewport toolbar | Ctrl+Shift+H / Ctrl+L / Ctrl+Shift+T † |

### Play, file, assets, build
| Action | Shortcut |
|---|---|
| Play / Simulate | Alt+P / Alt+S |
| Eject / possess | F10 |
| Release mouse / stop / console | Shift+F1 / Esc / ~ |
| Keep simulation changes | K |
| Content Drawer / Open asset / Find in Content Browser | Ctrl+Space / Ctrl+P / Ctrl+B |
| Save / Undo / Redo | Ctrl+S / Ctrl+Z / Ctrl+Y |
| New level / Open level / Save as / Save all | Ctrl+N / Ctrl+O / Ctrl+Alt+S / Ctrl+Shift+S † |
| Cut / Copy / Paste / Duplicate / Delete | Ctrl+X / C / V / Ctrl+D / Delete † |
| Live Coding / Compile Blueprint | Ctrl+Alt+F11 / F7 |

### Sequencer (main items)
| Action | Shortcut |
|---|---|
| Play-pause / play / pause / shuttle | Space / Down / K / J, L |
| Jump to start / end | Up / Ctrl+Up |
| Step frame / step by jump increment | Left, Right / Shift+Left, Shift+Right |
| Next / previous key or section bound | . / , |
| Set sequence start / end; custom range in / out | [ / ]; I / O |
| Key Location+Rotation+Scale / key Location / Rotation / Scale only | S / Shift+W / Shift+E / Shift+R |
| Key selected tracks / key at cursor | Enter / MMB click |
| Interpolation: auto / user / break / linear / constant | 1 / 2 / 3 / 4 / 5 |
| Split / trim left / trim right | Ctrl+/ / Ctrl+, / Ctrl+. |
| Toggle mark / add selected actor / go to time | M / Ctrl+A / Ctrl+T |

### Blueprint & Material editors, Modeling mode
| Context | Keys |
|---|---|
| Blueprint | RMB action menu, RMB drag pan, Wheel zoom, Home zoom to fit, F7 compile, F2 rename, C comment, F9 breakpoint, Ctrl+F / Ctrl+Shift+F find, Ctrl+D duplicate, Alt+click pin to break links, B / D / S / G / F / M / N / O / P + LMB to place Branch / Delay / Sequence / Gate / ForEach / MultiGate / DoN / DoOnce / BeginPlay |
| Material | Space force preview update, Enter apply, hold a letter key and LMB to place a node (A Add, M Multiply, L Lerp, T TextureSample, S ScalarParameter, V VectorParameter, 1–4 Constants, U TexCoord, C Comment) |
| Modeling mode | Shift+5 enter, Ctrl [hold] align gizmo to scene, Ctrl+click move gizmo grid to hit normal, Q toggle orientation lock |

Searched for but **not confirmed** in official 5.x docs: Ctrl+A (select all in level), Esc to deselect, [ / ] for grid size, F8 eject (the docs say F10), Ctrl+E edit asset, F2 rename in the level editor, Alt+1 view mode.

---

## 5. Blender 5.3 (default "Blender" keymap, left-click select)

Extracted from `blender_default.py`. Modal keys are listed separately in their own tables.

### Window / Screen (global)
| Action | Shortcut |
|---|---|
| New file menu / Open / Open recent | Ctrl+N / Ctrl+O / Ctrl+Shift+O |
| Save / Save As / Save incremental | Ctrl+S / Ctrl+Shift+S / Ctrl+Alt+S |
| Quit | Ctrl+Q |
| Quick Favorites menu | Q |
| Help (manual for hovered item) | F1 |
| Rename active item / batch rename | F2 / Ctrl+F2 |
| Menu search | F3 |
| File context menu | F4 |
| Adjust last operation (redo panel) | F9 |
| Toolbar popup | Shift+Space |
| Editor type: File Browser / Clip / Node / Console / 3D View / Graph / Properties / Sequencer / Outliner / Image / Text / Dope Sheet | Shift+F1 / F2 / F3 / F4 / F5 / F6 / F7 / F8 / F9 / F10 / F11 / F12 |
| Undo / Redo / Repeat last | Ctrl+Z / Ctrl+Shift+Z / Shift+R |
| Render image / animation | F12 / Ctrl+F12 |
| Render with sequencer scene (image / animation) | Alt+F12 / Ctrl+Alt+F12 |
| Show render window / play rendered animation | F11 / Ctrl+F11 |
| Maximize area / full-screen area | Ctrl+Space / Ctrl+Alt+Space |
| Toggle quad view | Ctrl+Alt+Q |
| Cycle Properties tabs / workspaces | Ctrl+Tab, Ctrl+Shift+Tab / Ctrl+PgDn, Ctrl+PgUp |
| Preferences | Ctrl+, |
| Area corner: split/join · duplicate into window · swap | LMB drag · Shift+LMB drag · Ctrl+LMB drag on area corner |
| Area options / region context menu | RMB on area border / RMB on header |

### UI (buttons and fields under the cursor)
| Action | Shortcut |
|---|---|
| Insert / delete / clear keyframe | I / Alt+I / Alt+Shift+I |
| Add / remove driver | Ctrl+D / Ctrl+Alt+D |
| Add to / remove from keying set | K / Alt+K |
| Reset to default | Backspace |
| Eyedropper | E |
| Copy data path / full data path | Ctrl+Shift+C / Ctrl+Alt+Shift+C |
| Filter lists / clear filter | Ctrl+F / Alt+F |

### 3D View: navigation and view
| Action | Shortcut |
|---|---|
| Orbit / Pan / Zoom / Dolly | MMB / Shift+MMB / Ctrl+MMB / Ctrl+Shift+MMB drag |
| Zoom | Wheel; Num+ / Num−; Ctrl+= / Ctrl+− |
| Dolly | Shift+Num+ / Shift+Num−; Ctrl+Shift+= / Ctrl+Shift+− |
| Snap view to axis (relative) / center on clicked point | Alt+MMB drag / Alt+MMB click |
| Frame selected / in all regions | Num. / Ctrl+Num. (also Mouse button 4) |
| Frame all / in all regions / frame all and center cursor | Home / Ctrl+Home / Shift+C |
| Front / Right / Top | Num1 / Num3 / Num7 |
| Back / Left / Bottom | Ctrl+Num1 / Ctrl+Num3 / Ctrl+Num7 |
| Align view to active object (same axes) | Shift+Num1 / 3 / 7 (Ctrl+Shift for opposite side) |
| Camera view / active object as camera / camera to view | Num0 / Ctrl+Num0 / Ctrl+Alt+Num0 |
| Perspective ↔ orthographic | Num5 |
| Orbit in steps / pan in steps / roll | Num2 / 4 / 6 / 8; Ctrl+Num2 / 4 / 6 / 8; Shift+Num4 / Shift+Num6 |
| Orbit 180° | Num9 |
| View pie / fly-walk navigation | ` / Shift+` |
| Local view (isolate) / remove from local view | / or Num/ / Alt+/ |
| Zoom border / clipping border | Shift+B / Alt+B |
| Render border set / clear | Ctrl+B / Ctrl+Alt+B |
| Toolbar / Sidebar | T / N |

### 3D View: selection, tools, display
| Action | Shortcut |
|---|---|
| Select / toggle (extend) / deselect all on empty | LMB click / Shift+LMB click / LMB click on empty space |
| Select object (in Edit Mode) / pick from overlapping items | Ctrl+LMB click / Alt+LMB click |
| Box (tool) / lasso add / lasso subtract | LMB drag / Ctrl+RMB drag / Ctrl+Shift+RMB drag |
| Box select / circle select | B / C |
| Cycle select tools | W |
| Context menu | RMB |
| 3D cursor: place / drag | Shift+RMB click / Shift+RMB drag |
| Snap toggle / snapping panel / snap pie | Shift+Tab / Ctrl+Shift+Tab / Shift+S |
| Pivot pie / orientation pie | . / , |
| Shading pie / wireframe toggle / X-ray / overlays | Z / Shift+Z / Alt+Z / Alt+Shift+Z |
| Gizmo toggle | Ctrl+` |
| Copy / paste objects (between files) | Ctrl+C / Ctrl+V |

### Object Mode
| Action | Shortcut |
|---|---|
| Edit-mode toggle / mode pie / transfer mode | Tab / Ctrl+Tab / Alt+Q |
| Select all / none / invert | A / Alt+A or A double-tap / Ctrl+I |
| Select more / less | Ctrl+Num+ / Ctrl+Num− |
| Select linked / grouped | Shift+L / Shift+G |
| Select parent / child (Shift = extend) | [ / ] |
| Move / Rotate / Scale | G / R / S; LMB drag (Tweak tool) |
| Mirror / interactive axis target | Ctrl+M / Shift+T |
| Clear location / rotation / scale | Alt+G / Alt+R / Alt+S |
| Affect only origins toggle | Ctrl+. |
| Add menu / Apply menu / Link-Transfer menu | Shift+A / Ctrl+A / Ctrl+L |
| Duplicate / duplicate linked / Join | Shift+D / Alt+D / Ctrl+J |
| Delete (with confirm) / delete / delete globally | X / Del / Shift+X, Shift+Del |
| Parent / clear parent | Ctrl+P / Alt+P |
| New collection / remove from collection / remove from all / add to active / remove from active | Ctrl+G / Ctrl+Alt+G / Ctrl+Alt+Shift+G / Ctrl+Shift+G / Alt+Shift+G |
| Move / link to collection | M / Shift+M |
| Hide / hide unselected / reveal / hide collection | H / Shift+H / Alt+H / Ctrl+H |
| Subdivision level 0–5 | Ctrl+0 … Ctrl+5 |
| Proportional editing / falloff pie | O / Shift+O |
| Insert keyframe / keyframe menu / delete keyframes / active keying set | I / K / Alt+I / Shift+K |

### Edit Mesh
| Action | Shortcut |
|---|---|
| Vertex / Edge / Face select mode (Shift = add mode, Ctrl = expand/contract) | 1 / 2 / 3 |
| Move / Rotate / Scale | G / R / S |
| Loop / ring select (Shift = extend) | Alt+LMB click / Ctrl+Alt+LMB click |
| Shortest path / with fill | Ctrl+LMB click / Ctrl+Shift+LMB click |
| Extrude to cursor (Ctrl+Shift = no source rotation) | Ctrl+RMB click |
| Select all / none / invert | A / Alt+A / Ctrl+I |
| Grow / shrink / next / previous active | Ctrl+Num+ / Ctrl+Num− / Ctrl+Shift+Num+ / Ctrl+Shift+Num− |
| Select linked all / under cursor / deselect linked | Ctrl+L / L / Shift+L |
| Select mirror / similar | Ctrl+Shift+M / Shift+G |
| Hide / hide unselected / reveal | H / Shift+H / Alt+H |
| Extrude / extrude menu | E / Alt+E |
| Inset / Bevel edges / Bevel vertices | I / Ctrl+B / Ctrl+Shift+B |
| Loop cut / offset edge loops | Ctrl+R / Ctrl+Shift+R |
| Knife / knife (selected only, through) | K / Shift+K |
| Connect vertex path | J |
| Make edge/face / fill | F / Alt+F |
| Merge menu / split menu | M / Alt+M |
| Rip / rip fill / rip edge / vertex slide | V / Alt+V / Alt+D / Shift+V |
| Duplicate / Separate / Split | Shift+D / P / Y |
| Delete menu / dissolve | X or Del / Ctrl+X or Ctrl+Del |
| Faces / Edges / Vertices menus | Ctrl+F / Ctrl+E / Ctrl+V |
| Triangulate / triangulate (fixed) / tris to quads | Ctrl+T / Ctrl+Shift+T / Alt+J |
| Recalculate normals outside / inside / normals menu | Shift+N / Ctrl+Shift+N / Alt+N |
| Edge crease / shrink-fatten / to sphere / shear / bend | Shift+E / Alt+S / Alt+Shift+S / Ctrl+Alt+Shift+S / Shift+W |
| Mirror / skin resize / point normals to target | Ctrl+M / Ctrl+A / Alt+L |
| UV unwrap menu / vertex groups menu / hooks menu | U / Ctrl+G / Ctrl+H |
| Make vertex parent | Ctrl+P |
| Proportional editing / connected only / falloff pie | O / Alt+O / Shift+O |
| Add mesh menu / context menu | Shift+A / RMB |

### Transform modal keys (while G / R / S is running)
| Action | Shortcut |
|---|---|
| Confirm / cancel | LMB, Enter, Space / RMB, Esc |
| Constrain to axis / plane / clear constraint | X, Y, Z / Shift+X, Y, Z / C |
| Switch to Move / Rotate (press R again for trackball) / Scale | G / R / S |
| Rotate normals | N |
| Toggle snapping / invert snapping (hold) | Shift+Tab / Ctrl |
| Edit snap source / add / remove snap point | B / A or Ctrl+A / Alt+A |
| Precision | Shift [hold] |
| Auto-constrain to axis / plane | MMB / Shift+MMB |
| Proportional size | PgUp / PgDn or Wheel |
| Navigate while transforming | Alt [hold] |

### Knife and Bevel modal keys
| Context | Keys |
|---|---|
| Knife | LMB cut, LMB double-click close loop, RMB start new cut, Enter or Space confirm, Esc cancel, Ctrl+Z undo, Shift [hold] snap to midpoints, Ctrl [hold] ignore snapping, X / Y / Z axis lock, A angle snap, R cycle angle-snap reference, C cut through, S show distance/angle, V depth test |
| Bevel | Wheel or Num+ / Num− segments, A offset, P profile, S segments, M offset mode, C clamp overlap, V vertices/edges, H harden normals, U mark seam, K mark sharp, O / I outer / inner miter, Z profile type, N vertex mesh, Ctrl [hold] snap, Shift [hold] precision |

### Outliner
| Action | Shortcut |
|---|---|
| Select / extend / range | LMB / Ctrl+LMB / Shift+LMB |
| Select hierarchy (children) | LMB double-click |
| Rename | F2 or LMB double-click |
| Box select | B or LMB drag |
| Walk selection | arrow keys |
| Select all / none / invert | A / Alt+A / Ctrl+I |
| Expand toggle / one level open / close | Shift+A / Num+ / Num− |
| Show hierarchy / show active | Home / . or Num. |
| New collection / delete | C / X or Del |
| Move / link to collection | M / Shift+M |
| Exclude / include collection | E / Alt+E |
| Hide / hide unselected / unhide all | H / Shift+H / Alt+H |
| Filter / clear filter | Ctrl+F / Alt+F |
| Copy / paste data-blocks | Ctrl+C / Ctrl+V |
| Show only collection N (Shift = add, Alt = collections 11–20) | 1 … 0 |
| Keyframe insert / delete; driver add / delete | I / Alt+I; Ctrl+D / Ctrl+Alt+D |
| View pie | ` |

### Timeline / Dope Sheet / Graph Editor (shared and per-editor)
| Action | Shortcut |
|---|---|
| Play / reverse play / stop and restore | Space / Ctrl+Shift+Space / Esc |
| Previous / next frame | Left / Right |
| Start / end frame | Shift+Left / Shift+Right |
| Jump by time step | Ctrl+Left / Ctrl+Right |
| Previous / next keyframe | Up / Down |
| Step frames | Alt+Wheel |
| Scrub | LMB in the scrubbing region; Shift+RMB (Dope Sheet) |
| Set / clear preview range | P / Alt+P |
| Set start / end frame | Ctrl+Home / Ctrl+End |
| Toggle seconds/frames display | Ctrl+T |
| Add marker / rename marker / move marker | M / F2 / G |
| Select keys: click / column / channel | LMB / Alt+LMB / Ctrl+Alt+LMB |
| Box / circle / lasso select | B or LMB drag / C / Ctrl+RMB drag |
| Select left or right of the current frame | [ / ] or Ctrl+LMB click |
| Select columns: keys / current frame / markers / between markers | K / Ctrl+K / Shift+K / Alt+K |
| Select all / none / invert / more / less / linked | A / Alt+A / Ctrl+I / Ctrl+Num+ / Ctrl+Num− / L |
| Move / extend / scale (Dope Sheet: time; Graph: values too) / slide | G / E / S / Shift+T (Dope Sheet) |
| Rotate keys | R (Graph Editor) |
| Keyframe type | R (Dope Sheet) |
| Insert keyframe / duplicate / delete | I / Shift+D / X or Del |
| Copy / paste / paste flipped | Ctrl+C / Ctrl+V / Ctrl+Shift+V |
| Handle type / interpolation / easing / extrapolation | V / T / Ctrl+E / Shift+E |
| Snap pie / mirror / jump to keys | Shift+S / Ctrl+M / Ctrl+G |
| Frame all / selected / current frame | Home / Num. / Num0 |
| Preview range from selected keys | Ctrl+Alt+P |
| Graph: hide curves / hide unselected / reveal / show handles | H / Shift+H / Alt+H / Ctrl+H |
| Graph: smooth / bake keys / keys to samples / smoothing menu / blending menu | Alt+O / Alt+Shift+O / Alt+C / Alt+S / Alt+D |
| Graph: add F-Curve modifier / place 2D cursor / click-insert key | Ctrl+Shift+M / Shift+RMB / Ctrl+RMB click |
| Graph: switch to Dope Sheet / local view | Ctrl+Tab / / |
| Channels: toggle / enable / disable setting | Shift+W / Ctrl+Shift+W / Alt+W |
| Channels: group / ungroup / move / editable toggle | Ctrl+G / Ctrl+Alt+G / PgUp, PgDn / Tab |
| Proportional editing | O / Shift+O |
| Context menu | RMB |

### Node editors (Shader / Geometry / Compositor)
| Action | Shortcut |
|---|---|
| Select / toggle / box / lasso / circle | LMB / Shift+LMB / LMB drag / Ctrl+Alt+LMB drag / C |
| Cycle select tools / box select | W / B |
| Select all / none / invert | A / Alt+A / Ctrl+I |
| Select linked from / to | L / Shift+L |
| Select grouped / same type previous / next | Shift+G / Shift+[ / Shift+] |
| Add menu / swap menu / find | Shift+A / Shift+S / Ctrl+F |
| Move / rotate / scale | G or LMB drag / R / S |
| Detach links while moving | Alt+LMB drag |
| Duplicate / linked / keep inputs | Shift+D / Alt+D / Ctrl+Shift+D |
| Delete / delete with reconnect | X or Del / Shift+X or Ctrl+Del |
| Cut (delete, copy, reconnect) / copy / paste | Ctrl+X / Ctrl+C / Ctrl+V |
| Make link / replace links | J / Shift+J |
| Join in new frame / join named / parent to frame / remove from frame | Ctrl+J / F / Ctrl+P / Alt+P |
| Group: make / ungroup / separate / enter-exit | Ctrl+G / Ctrl+Alt+G / P / Tab, Ctrl+Tab |
| Collapse / mute / toggle preview / hide unused sockets | H / M / Shift+H / Ctrl+H |
| Cut links / mute links / add reroute | Ctrl+RMB drag / Ctrl+Alt+RMB drag / Shift+RMB drag |
| Link to Viewer (Geometry) / connect to output | Ctrl+Shift+LMB / Alt+Shift+LMB |
| Frame all / selected | Home / Num. |
| Backdrop: move / zoom / fit / sample | Alt+MMB / V, Alt+V / Alt+Home / Alt+RMB |
| Viewer slots (Compositor): recall / set | 1…9 / Ctrl+1…9 |
| Edit comment / label | F2 or Enter |
| Toggle snapping / overlays | Shift+Tab / Alt+Shift+Z |
| Toolbar / sidebar | T / N |

### Image / UV Editor
| Action | Shortcut |
|---|---|
| Pan / zoom | MMB drag / Wheel, Ctrl+MMB drag |
| Frame all / fit / selected / center on cursor | Home / Shift+Home / Num. / Shift+C |
| Sample colour / set black point / set white point | RMB / Ctrl+RMB / Shift+RMB (Image editor, View mode) |
| Render slot 1–9 | 1 … 9 (Image editor) |
| UV select mode: vertex / edge / face / island toggle | 1 / 2 / 3 / 4 |
| UV select / toggle / loop / ring / shortest path | LMB / Shift+LMB / Alt+LMB / Ctrl+Alt+LMB / Ctrl+LMB |
| UV box / pinned box / circle / lasso | B / Alt+B / C / Ctrl+RMB drag |
| UV linked / pick linked / similar / pinned / split selection | Ctrl+L / L / Shift+G / Shift+P / Y |
| UV grow / shrink | Ctrl+Num+ / Ctrl+Num− |
| UV move / rotate / scale / mirror / shear | G / R / S / Ctrl+M / Ctrl+Alt+Shift+S |
| UV merge / split / align menus | M / Alt+M / Shift+W |
| UV stitch / rip / pin / unpin | Alt+V / V / P / Alt+P |
| UV hide / hide unselected / reveal | H / Shift+H / Alt+H |
| Unwrap menu / mark seam | U / Ctrl+E |
| UV snapping toggle / element / snap pie | Shift+Tab / Ctrl+Shift+Tab / Shift+S |
| 2D cursor set / drag | Shift+RMB / Shift+RMB drag |
| Copy / paste UVs | Ctrl+C / Ctrl+V |
| Custom region set / toggle | Ctrl+B / Ctrl+Alt+B |
| Context menu | RMB |

### Sculpt Mode (basics)
| Action | Shortcut |
|---|---|
| Stroke / invert / smooth / mask | LMB / Ctrl+LMB / Shift+LMB / Alt+LMB |
| Brush size / strength / texture angle (radial) | F / Shift+F / Ctrl+F |
| Brush size smaller / bigger | [ / ] |
| Brushes: Draw / Smooth / Pinch / Inflate / Grab / Clay Strips / Snake Hook / Mask | V / S / P / I / G / C / K / M |
| Brushes: Scrape/Fill / Crease Polish | Shift+T / Shift+C |
| Brush asset shelf | Shift+Space |
| Mask pie / invert mask / clear mask / box mask | A / Ctrl+I / Alt+M / B |
| Lasso mask: add / clear | Ctrl+Shift+RMB drag / Ctrl+RMB drag |
| Expand mask (geodesic / normals) | Shift+A / Alt+Shift+A |
| Expand face set / face sets pie | Shift+W / Alt+W |
| Face set grow / shrink | Ctrl+W / Ctrl+Alt+W |
| Hide active face set / toggle / show all | H / Shift+H / Alt+H |
| Visibility grow / shrink | PgUp / PgDn |
| Voxel size / remesh (or Dyntopo detail size / flood, by context) | R / Ctrl+R |
| Subdivision level 0–5 / step down / step up | Ctrl+0…5 / Alt+1 / Alt+2 |
| Sample colour / flip colours / fill colour | Shift+X / X / Ctrl+X |
| Stroke method / smooth stroke toggle / auto-masking pie | Alt+E / Shift+S / Alt+A |
| Set pivot on surface | Shift+RMB |
| Context menu | RMB |

---

## 6. Blender Industry Compatible: what differs from the default keymap

Source: `industry_compatible_data.py`. IC is a Maya/Max hybrid. It is mostly Maya-flavoured: Alt+LMB/MMB/RMB navigation, F to frame, Q/W/E/R tools, S to key, Shift+W/E/R key-transform channels, P / Shift+P parent.

| Area | IC binding |
|---|---|
| Navigation | Alt+LMB orbit, Alt+MMB pan, Alt+RMB zoom (also Alt+Wheel); F frame selected; Shift+F center on clicked point; A / Shift+A frame all / in all views; Z zoom border |
| Views | F1 / F2 / F3 front / right / top; Ctrl+F1 / F2 / F3 opposite views; F4 camera; F5 orbit 180°; V view pie; Shift+I local view |
| Command search | Tab (in most editors) |
| Rename / batch rename | Enter (3D View, Outliner) / Alt+Enter |
| Quick Favorites | Shift+Tab |
| Repeat last / undo history | G / Ctrl+Alt+Z |
| Render image / animation | Ctrl+Enter / Ctrl+Alt+Enter |
| Toolbar / sidebar / asset shelf | Ctrl+[ / Ctrl+] / Shift+Space |
| Tools (Object and Edit) | Q select box, W move, E rotate, R scale, T transform, D annotate, M measure, C cursor (press again to cycle) |
| Edit-mesh tools | Ctrl+E extrude, Ctrl+B bevel, I inset, K knife, Alt+C loop cut |
| Modes | 1 / 2 / 3 enter Edit Mode at vertex / edge / face; 4 Object Mode; 5 mode pie; ` transfer mode |
| Selection | Ctrl+A all, Ctrl+Shift+A none, Ctrl+I invert, Up / Down grow / shrink, Ctrl+L linked; in Edit Mesh, LMB double-click loop, Alt+LMB double-click ring, Ctrl+Shift+LMB shortest path |
| Delete / dissolve | Backspace or Del / Ctrl+Backspace or Ctrl+Del |
| Duplicate | Ctrl+D |
| Clear location / rotation / scale | Alt+W / Alt+E / Alt+R |
| Hide / hide unselected / reveal | Ctrl+H / Shift+H / Alt+H |
| Parent / clear parent | P / Shift+P |
| Collections | Ctrl+G move to collection, Ctrl+Shift+G link |
| Snapping | X snap toggle, Shift+X snap pie, Alt+X X-ray |
| Proportional editing | B |
| Keyframes | S key LocRotScale, Shift+W / Shift+E / Shift+R key location / rotation / scale, Shift+S insert (keying set), Alt+S delete, Ctrl+Alt+Shift+S set active keying set |
| Timeline | Space play, Esc stop, Left / Right frame step, Ctrl+Left / Ctrl+Right start / end |
| Subdivision level | Ctrl+0…5; D / Shift+D up / down one level |
| Not bound in IC (bound in default) | Join (Ctrl+J), merge menu (M), separate (P), connect (J), area maximize (Ctrl+Space), shading pie (Z), wireframe toggle (Shift+Z), redo panel (F9), the F-key editor switchers, keyframe-jump (Up / Down) |

---

## 7. Conflicts and notes for Moritz

The biggest clashes between 3ds Max muscle memory and Blender's default keymap:

| Max key | Max meaning | Blender default meaning | IC meaning | Note for Moritz |
|---|---|---|---|---|
| W / E / R | Move / Rotate / Scale tool | W = cycle select tools; E = extrude (Edit); R = rotate (modal) | Move / Rotate / Scale **tools** | IC already matches Max. Decide between tool activation (Max-like, persistent gizmo) and modal operators (Blender G/R/S). |
| Q | Smart Select (cycles region type) | Quick Favorites menu | Select box tool (cycles) | IC is close. Max's repeated Q cycles region shape, and so does IC's `cycle=True`. |
| H | Select By Name dialog | Hide selected | — (Ctrl+H hides) | Max-style H needs a "select by name" popup, for example an outliner-filter search popup. Blender's hide moves to Alt+H, which clashes with Blender's unhide. |
| Alt+H / Alt+I / Alt+U | Hide selected / hide unselected / unhide all (Editable Poly) | Alt+H = unhide all | Alt+H = unhide | Opposite meaning for Alt+H. A Max keymap must remap the whole hide set. |
| Alt+Q | Isolate selection | Transfer mode | — (` = transfer mode) | Map to `view3d.localview` (Blender: /, IC: Shift+I). |
| Alt+W | Maximize viewport toggle | Fallback-tool pie (left select) | Clear location (Object Mode) | Map to `screen.screen_full_area` (Blender: Ctrl+Space). |
| Z | Zoom extents selected | Shading pie | Zoom border | Map to `view3d.view_selected`. The shading pie needs a new key. |
| Ctrl+Alt+Z / Shift+Ctrl+Z | Zoom extents / extents all | — / **Redo** | Undo history / redo | Hard clash: Max uses Ctrl+Y for redo, so Moritz could move redo to Ctrl+Y and free Shift+Ctrl+Z. |
| Shift+Z | Undo viewport change | Wireframe toggle | — | Blender has no view-undo operator. It would need a new feature or stay unbound. |
| F2 / F3 / F4 | Shade selected faces / wireframe toggle / edged faces | Rename / menu search / file context menu | F2 = right view, F3 = top view, F4 = camera | F3 search is Blender's most important key. In a Max layout it could move to X (Max Global Search), which collides with Blender delete and transform-axis keys. |
| F5–F8 | Axis constraints X / Y / Z / plane cycle | — (F5–F8 unbound globally) | F5 = orbit 180° | F5–F8 are free in the default keymap. They could set the transform constraint, a toggle Blender lacks outside modal transforms. |
| F9 / F10 / F12 | Render last / Render setup / Transform type-in | Redo panel / — / Render | — / — / — | Clash on F9 and F12. The Max type-in matches Blender's redo panel or N sidebar. |
| T / F / L / P / C / U | Top / Front / Left / Perspective / Camera / User views | T toolbar, F make face, L select linked, P separate, C circle select, U UV menu | T transform tool, F frame, C cursor tool | Large clash with Edit Mesh keys. Max view keys only make sense in Object Mode or with a modifier. |
| S / A | Snap toggle / Angle snap | Scale / Select all | Key LocRotScale / frame all | Moving Blender's modal S would lose Blender's fastest scale. Blender has no separate angle-snap toggle (only increment snapping per transform). |
| G | Grid toggle | Grab / move | Repeat last | — |
| 1–5 / 6 | Sub-object levels / Particle View | 1–3 vertex / edge / face (Edit Mode); Object Mode numbers unbound (the Outliner uses 1–0 for collections) | 1–3 enter Edit Mode at that level; 4 Object Mode; 5 mode pie | IC matches Max well. Max 4 = Polygon, 5 = Element; Blender has no border or element level. |
| Ctrl+B | Sub-object selection toggle | Bevel edges (Edit) / render border (Object) | Bevel tool | Max bevel is Ctrl+Shift+B, which Blender uses for vertex bevel. |
| Shift+E / Alt+C / Alt+L / Alt+R | Extrude / Cut / Loop / Ring | Edge crease / — / point normals / rotation clear (Object) | — / loop cut tool / — / scale clear | Max loop and ring use keyboard keys on the selection; Blender and IC use Alt+click or double-click. |
| Ctrl+Shift+E / Shift+Ctrl+W | Connect / Target weld | — / — | — | Free in Blender. Map to `mesh.vert_connect_path` / `mesh.merge(type='CURSOR')` or a target-weld modal. |
| Alt+Shift+D / Ctrl+Alt+D | Attach / Detach | — / driver remove (UI) | — | Blender equivalents are Ctrl+J and P. Mostly free. |
| Ctrl+D / Ctrl+I / Ctrl+A | Select none / invert / all | — (UI: add driver) / invert / Apply menu (Object) | Duplicate / invert / select all | Ctrl+D is Max deselect but IC duplicate. Max clones with Ctrl+V or Shift+drag. |
| Ctrl+V | Clone | Paste objects / vertices menu (Edit) | Paste | — |
| Space | Selection lock | Play animation | Play | Low priority. Max users rarely rely on Space lock. |
| N / K | Auto Key / Set Key | Sidebar / keyframe menu | — / — | N for Auto Key clashes with the sidebar. IC uses S for keying. |
| , / . / / | Prev / next frame / play | Orientation pie / pivot pie / local view | same as Blender | Max uses these for animation; Blender uses them for pies and local view. |
| Home / End | Go to start / end | Frame all / — | — | Clash on Home. |
| RMB | Quad menu (context sensitive; Ctrl / Alt / Shift variants) | Context menu (left select) | Context menu | Close equivalent. The quad variants (Ctrl/Alt/Shift+RMB) need pie or custom menus. Blender uses Ctrl+RMB for lasso and Shift+RMB for the 3D cursor. |
| MMB / Alt+MMB / Ctrl+Alt+MMB | Pan / Orbit / Zoom | Orbit / snap view to axis (Alt+MMB drag) / — | — / Pan / — | Core clash. Max-style navigation needs Pan on MMB, Orbit on Alt+MMB, and Zoom on Ctrl+Alt+MMB plus Wheel. Blender's Alt+MMB axis-snap and Shift+MMB pan get displaced. The preference `use_v3d_mmb_pan` already swaps MMB to pan. |
| Shift+drag (with transform) | Clone | precision (inside modal transform) | precision | Max Shift+drag clone has no direct Blender equivalent (Shift+D is duplicate then move). It would need a gizmo-drag hook. |

**What IC already provides for a Max user:** Q/W/E/R tools, 1/2/3 sub-object entry from Object Mode, Ctrl+A / Ctrl+I select all / invert, Ctrl+B bevel, Ctrl+E extrude, K knife, Alt+C loop cut, Del/Backspace delete, P/Shift+P parent, X snap toggle, Alt+X see-through (matches Max Alt+X exactly), and F frame (Maya, not Max).

**IC is Maya-like, not Max-like, for:** Alt+LMB/MMB/RMB navigation, F1–F4 views, Tab search, S key, Ctrl+D duplicate, Ctrl+H hide, Ctrl+Shift+A deselect.

A Moritz Max keymap is therefore best built as a **fork of IC**. Replace its navigation with Max mouse navigation and Max's T/F/L/P/C view keys (Object Mode), Max's Alt+Q isolate, Alt+W maximize, Z frame, Ctrl+D deselect, H select-by-name and Alt+H/I/U hide set, and the Editable Poly key set (Shift+E, Ctrl+Shift+B/C, Ctrl+Shift+E, Alt+C, Alt+L/R, Shift+Ctrl+W, Alt+Shift+D, Ctrl+Alt+D).

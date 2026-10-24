# Maximize

A 3ds Max workflow for Blender and Moritz, as one add-on.

- **Keymaps:** Max (3ds Max 2026 defaults on top of Blender's Industry Compatible keymap) and Moritz (Max keys plus Blender's selection ideas). Both appear in Preferences > Keymap while the add-on is enabled.
- **Quad menu** on right-click, **Alt+W** maximizes the viewport under the mouse.
- **Sub-object levels** 1–5 (Vertex, Edge, Border, Polygon, Element), Max-style Ctrl/Alt selection.
- **Max tools:** Transform Type-In, Align, Array, Spacing Tool, Clone (copy / instance / reference), pivot tools, Select by Name, named selection sets.
- **Editable primitives** (Box, Sphere, Cylinder, Cone, Tube, Torus, Plane) with live parameters, and a **UVW Map** modifier.
- **Max English:** interface names such as Weld, Chamfer, Attach and Swift Loop.
- A Max sidebar tab and a Max menu in the 3D Viewport header.

Requires Blender 5.3 or Moritz.

## Install

Copy or link the `maximize` folder into your add-ons folder, for example on Windows:

```
mklink /J "%APPDATA%\Blender Foundation\Blender\5.3\scripts\addons\maximize" "<repo>\maximize"
```

For Moritz the folder is `%APPDATA%\Moritz\5.3\scripts\addons`. Then enable **Maximize** in Preferences > Add-ons. On first enable it switches to the Moritz keymap; switch back in the Max sidebar tab (Keymap) or in Preferences > Keymap.

## Repository

- `maximize/` — the add-on
- `docs/` — shortcut references, the coverage report and the Max / Blender / Maya comparison page
- `tools/` — `check_max_keymap.py` (coverage report) and `dump_keymaps.py`
- `tests/` — background and simulated-input UI tests; run each with `moritz.exe` (or `blender`) `--factory-startup [-b | --enable-event-simulate] --python tests/<name>.py`

## License

GPL-2.0-or-later, see `LICENSE`.

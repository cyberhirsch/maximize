# Blender 5.3 — complete Industry Compatible keymap

Generated 2026-10-23 from the keymap source of the Moritz fork (Blender 5.3, branch `blender-v5.3-release`), so it lists every binding, not a selection.

- **Key**: modifiers + key + event. No event word means *press*. `[Ctrl]` means either state.
- **Action**: the operator's UI name; for modal keymaps, the modal item.
- Windows/Linux keys; on macOS Blender maps Ctrl to Cmd for most items.
- Bindings marked *(Moritz)* are Moritz additions.
- The Industry Compatible preset (Maya/Max-like); default settings.

**2785 bindings in 276 keymaps.**

### Keymaps

- [Window](#window) — 15
- [Screen](#screen) — 17
- [Screen Editing](#screen-editing) — 18
- [Region Context Menu](#region-context-menu) — 2
- [View2D](#view2d) — 25
- [View2D Buttons List](#view2d-buttons-list) — 16
- [User Interface](#user-interface) — 19
- [Property Editor](#property-editor) — 21
- [Outliner](#outliner) — 58
- [UV Editor](#uv-editor) — 46
- [3D View Generic](#3d-view-generic) — 3
- [3D View](#3d-view) — 69
- [Mask Editing](#mask-editing) — 38
- [Markers](#markers) — 21
- [Graph Editor Generic](#graph-editor-generic) — 5
- [Graph Editor](#graph-editor) — 53
- [Image Generic](#image-generic) — 10
- [Image](#image) — 41
- [Node Generic](#node-generic) — 4
- [Node Editor](#node-editor) — 66
- [Info](#info) — 15
- [File Browser](#file-browser) — 37
- [File Browser Main](#file-browser-main) — 32
- [File Browser Buttons](#file-browser-buttons) — 6
- [Dopesheet Generic](#dopesheet-generic) — 4
- [Dopesheet](#dopesheet) — 57
- [NLA Generic](#nla-generic) — 11
- [NLA Tracks](#nla-tracks) — 6
- [NLA Editor](#nla-editor) — 36
- [Text Generic](#text-generic) — 5
- [Text](#text) — 78
- [Video Sequence Editor](#video-sequence-editor) — 3
- [Sequencer](#sequencer) — 88
- [Preview](#preview) — 7
- [Sequencer Channels](#sequencer-channels) — 2
- [Console](#console) — 40
- [Clip](#clip) — 10
- [Clip Editor](#clip-editor) — 73
- [Clip Graph Editor](#clip-graph-editor) — 22
- [Clip Dopesheet Editor](#clip-dopesheet-editor) — 4
- [Spreadsheet Generic](#spreadsheet-generic) — 2
- [Frames](#frames) — 6
- [Animation](#animation) — 1
- [Animation Channels](#animation-channels) — 33
- [Paint Face Mask (Weight, Vertex, Texture)](#paint-face-mask-weight,-vertex,-texture) — 11
- [Paint Vertex Selection (Weight, Vertex)](#paint-vertex-selection-weight,-vertex) — 8
- [Pose](#pose) — 39
- [Object Mode](#object-mode) — 50
- [Paint Curve](#paint-curve) — 15
- [Curve](#curve) — 31
- [Image Paint](#image-paint) — 26
- [Vertex Paint](#vertex-paint) — 27
- [Weight Paint](#weight-paint) — 28
- [Sculpt](#sculpt) — 56
- [Mesh](#mesh) — 50
- [Armature](#armature) — 34
- [Metaball](#metaball) — 21
- [Lattice](#lattice) — 15
- [Particle](#particle) — 20
- [Font](#font) — 46
- [Curves](#curves) — 20
- [Sculpt Curves](#sculpt-curves) — 16
- [Point Cloud](#point-cloud) — 4
- [Object Non-modal](#object-non-modal) — 3
- [Knife Tool Modal Map](#knife-tool-modal-map) — 26
- [Eyedropper Modal Map](#eyedropper-modal-map) — 7
- [Eyedropper ColorRamp PointSampling Map](#eyedropper-colorramp-pointsampling-map) — 7
- [Transform Modal Map](#transform-modal-map) — 57
- [Generic Gizmo Drag](#generic-gizmo-drag) — 1
- [Generic Gizmo Maybe Drag](#generic-gizmo-maybe-drag) — 1
- [3D View Tool: Tweak](#3d-view-tool:-tweak) — 2
- [3D View Tool: Object, Add Primitive](#3d-view-tool:-object,-add-primitive) — 4
- [Image Editor Tool: Uv, Tweak](#image-editor-tool:-uv,-tweak) — 2
- [Preview Tool: Select Box](#preview-tool:-select-box) — 2
- [Sequencer Tool: Select Box](#sequencer-tool:-select-box) — 2
- [Preferences](#preferences) — 2
- [Preferences_nav](#preferences_nav) — 2
- [Time Scrub](#time-scrub) — 1
- [Clip Time Scrub](#clip-time-scrub) — 1
- [Grease Pencil](#grease-pencil) — 5
- [Grease Pencil Selection](#grease-pencil-selection) — 10
- [Grease Pencil Draw Mode](#grease-pencil-draw-mode) — 39
- [Grease Pencil Edit Mode](#grease-pencil-edit-mode) — 57
- [Grease Pencil Sculpt Mode](#grease-pencil-sculpt-mode) — 27
- [Grease Pencil Weight Paint](#grease-pencil-weight-paint) — 23
- [Grease Pencil Vertex Paint](#grease-pencil-vertex-paint) — 22
- [Grease Pencil Brush Stroke](#grease-pencil-brush-stroke) — 6
- [Grease Pencil Fill Tool](#grease-pencil-fill-tool) — 3
- [View3D Placement Modal](#view3d-placement-modal) — 12
- [View3D Gesture Circle](#view3d-gesture-circle) — 14
- [Gesture Box](#gesture-box) — 10
- [Gesture Zoom Border](#gesture-zoom-border) — 6
- [Gesture Straight Line](#gesture-straight-line) — 7
- [Gesture Lasso](#gesture-lasso) — 1
- [Gesture Polyline](#gesture-polyline) — 6
- [Standard Modal Map](#standard-modal-map) — 8
- [Custom Normals Modal Map](#custom-normals-modal-map) — 14
- [Bevel Modal Map](#bevel-modal-map) — 30
- [Transform Axis Target Modal Map](#transform-axis-target-modal-map) — 9
- [View3D Fly Modal](#view3d-fly-modal) — 39
- [View3D Walk Modal](#view3d-walk-modal) — 50
- [View3D Rotate Modal](#view3d-rotate-modal) — 5
- [View3D Move Modal](#view3d-move-modal) — 1
- [View3D Zoom Modal](#view3d-zoom-modal) — 1
- [View3D Dolly Modal](#view3d-dolly-modal) — 1
- [View3D VR Location Scouting Capture Review Modal](#view3d-vr-location-scouting-capture-review-modal) — 6
- [Paint Stroke Modal](#paint-stroke-modal) — 1
- [Sculpt Expand Modal](#sculpt-expand-modal) — 25
- [Mesh Filter Modal Map](#mesh-filter-modal-map) — 6
- [Curve Pen Modal Map](#curve-pen-modal-map) — 5
- [Pen Tool Modal Map](#pen-tool-modal-map) — 3
- [Node Link Modal Map](#node-link-modal-map) — 6
- [Node Resize Modal Map](#node-resize-modal-map) — 7
- [Primitive Tool Modal Map](#primitive-tool-modal-map) — 14
- [Fill Tool Modal Map](#fill-tool-modal-map) — 14
- [Interpolate Tool Modal Map](#interpolate-tool-modal-map) — 7
- [Slip Modal](#slip-modal) — 12
- [Generic Gizmo](#generic-gizmo) — 1
- [Generic Gizmo Click Drag](#generic-gizmo-click-drag) — 2
- [Generic Gizmo Select](#generic-gizmo-select) — 1
- [Generic Gizmo Tweak Modal Map](#generic-gizmo-tweak-modal-map) — 12
- [Toolbar Popup](#toolbar-popup) — 5
- [Generic Tool: Annotate](#generic-tool:-annotate) — 4
- [Generic Tool: Annotate Line](#generic-tool:-annotate-line) — 4
- [Generic Tool: Annotate Polygon](#generic-tool:-annotate-polygon) — 4
- [Generic Tool: Annotate Eraser](#generic-tool:-annotate-eraser) — 4
- [Image Editor Tool: Sample](#image-editor-tool:-sample) — 2
- [Image Editor Tool: Uv, Cursor](#image-editor-tool:-uv,-cursor) — 4
- [Image Editor Tool: Uv, Select Box](#image-editor-tool:-uv,-select-box) — 3
- [Image Editor Tool: Uv, Select Box (fallback)](#image-editor-tool:-uv,-select-box-fallback) — 3
- [Image Editor Tool: Uv, Select Circle](#image-editor-tool:-uv,-select-circle) — 3
- [Image Editor Tool: Uv, Select Circle (fallback)](#image-editor-tool:-uv,-select-circle-fallback) — 3
- [Image Editor Tool: Uv, Select Lasso](#image-editor-tool:-uv,-select-lasso) — 3
- [Image Editor Tool: Uv, Select Lasso (fallback)](#image-editor-tool:-uv,-select-lasso-fallback) — 3
- [Image Editor Tool: Uv, Rip Region](#image-editor-tool:-uv,-rip-region) — 2
- [Image Editor Tool: Uv, Grab](#image-editor-tool:-uv,-grab) — 8
- [Image Editor Tool: Uv, Relax](#image-editor-tool:-uv,-relax) — 8
- [Image Editor Tool: Uv, Pinch](#image-editor-tool:-uv,-pinch) — 8
- [Image Editor Tool: Uv, Move](#image-editor-tool:-uv,-move) — 2
- [Image Editor Tool: Uv, Rotate](#image-editor-tool:-uv,-rotate) — 2
- [Image Editor Tool: Uv, Scale](#image-editor-tool:-uv,-scale) — 2
- [Image Editor Tool: Mask, Cursor](#image-editor-tool:-mask,-cursor) — 4
- [Image Editor Tool: Mask, Tweak](#image-editor-tool:-mask,-tweak) — 3
- [Image Editor Tool: Mask, Select Box](#image-editor-tool:-mask,-select-box) — 3
- [Image Editor Tool: Mask, Select Box (fallback)](#image-editor-tool:-mask,-select-box-fallback) — 3
- [Image Editor Tool: Mask, Select Circle](#image-editor-tool:-mask,-select-circle) — 3
- [Image Editor Tool: Mask, Select Circle (fallback)](#image-editor-tool:-mask,-select-circle-fallback) — 3
- [Image Editor Tool: Mask, Select Lasso](#image-editor-tool:-mask,-select-lasso) — 3
- [Image Editor Tool: Mask, Select Lasso (fallback)](#image-editor-tool:-mask,-select-lasso-fallback) — 3
- [Image Editor Tool: Mask, Move](#image-editor-tool:-mask,-move) — 2
- [Image Editor Tool: Mask, Rotate](#image-editor-tool:-mask,-rotate) — 2
- [Image Editor Tool: Mask, Scale](#image-editor-tool:-mask,-scale) — 2
- [Image Editor Tool: Mask, Transform](#image-editor-tool:-mask,-transform) — 2
- [Image Editor Tool: Mask, Circle](#image-editor-tool:-mask,-circle) — 2
- [Image Editor Tool: Mask, Box](#image-editor-tool:-mask,-box) — 2
- [Node Tool: Select Box](#node-tool:-select-box) — 3
- [Node Tool: Select Box (fallback)](#node-tool:-select-box-fallback) — 3
- [Node Tool: Select Lasso](#node-tool:-select-lasso) — 3
- [Node Tool: Select Lasso (fallback)](#node-tool:-select-lasso-fallback) — 3
- [Node Tool: Select Circle](#node-tool:-select-circle) — 3
- [Node Tool: Select Circle (fallback)](#node-tool:-select-circle-fallback) — 3
- [Node Tool: Links Cut](#node-tool:-links-cut) — 2
- [Node Tool: Mute Links](#node-tool:-mute-links) — 2
- [Node Tool: Add Reroute](#node-tool:-add-reroute) — 2
- [3D View Tool: Cursor](#3d-view-tool:-cursor) — 4
- [3D View Tool: Edit Text, Select Text](#3d-view-tool:-edit-text,-select-text) — 4
- [3D View Tool: Select Box](#3d-view-tool:-select-box) — 4
- [3D View Tool: Select Box (fallback)](#3d-view-tool:-select-box-fallback) — 4
- [3D View Tool: Select Circle](#3d-view-tool:-select-circle) — 3
- [3D View Tool: Select Circle (fallback)](#3d-view-tool:-select-circle-fallback) — 3
- [3D View Tool: Select Lasso](#3d-view-tool:-select-lasso) — 4
- [3D View Tool: Select Lasso (fallback)](#3d-view-tool:-select-lasso-fallback) — 4
- [3D View Tool: Transform](#3d-view-tool:-transform) — 2
- [3D View Tool: Move](#3d-view-tool:-move) — 2
- [3D View Tool: Rotate](#3d-view-tool:-rotate) — 2
- [3D View Tool: Scale](#3d-view-tool:-scale) — 2
- [3D View Tool: Shear](#3d-view-tool:-shear) — 6
- [3D View Tool: Bend](#3d-view-tool:-bend) — 2
- [3D View Tool: Measure](#3d-view-tool:-measure) — 4
- [3D View Tool: Breakdowner](#3d-view-tool:-breakdowner) — 2
- [3D View Tool: Push](#3d-view-tool:-push) — 2
- [3D View Tool: Relax](#3d-view-tool:-relax) — 2
- [3D View Tool: Edit Armature, Roll](#3d-view-tool:-edit-armature,-roll) — 2
- [3D View Tool: Edit Armature, B-Bone Size](#3d-view-tool:-edit-armature,-b-bone-size) — 2
- [3D View Tool: Edit Armature, Bone Envelope](#3d-view-tool:-edit-armature,-bone-envelope) — 2
- [3D View Tool: Edit Armature, Extrude](#3d-view-tool:-edit-armature,-extrude) — 2
- [3D View Tool: Edit Armature, Extrude to Cursor](#3d-view-tool:-edit-armature,-extrude-to-cursor) — 4
- [3D View Tool: Edit Mesh, Extrude Region](#3d-view-tool:-edit-mesh,-extrude-region) — 2
- [3D View Tool: Edit Mesh, Extrude Manifold](#3d-view-tool:-edit-mesh,-extrude-manifold) — 2
- [3D View Tool: Edit Mesh, Extrude Along Normals](#3d-view-tool:-edit-mesh,-extrude-along-normals) — 2
- [3D View Tool: Edit Mesh, Extrude Individual](#3d-view-tool:-edit-mesh,-extrude-individual) — 2
- [3D View Tool: Edit Mesh, Extrude to Cursor](#3d-view-tool:-edit-mesh,-extrude-to-cursor) — 4
- [3D View Tool: Edit Mesh, Inset Faces](#3d-view-tool:-edit-mesh,-inset-faces) — 2
- [3D View Tool: Edit Mesh, Bevel](#3d-view-tool:-edit-mesh,-bevel) — 2
- [3D View Tool: Edit Mesh, Loop Cut](#3d-view-tool:-edit-mesh,-loop-cut) — 2
- [3D View Tool: Edit Mesh, Offset Edge Loop Cut](#3d-view-tool:-edit-mesh,-offset-edge-loop-cut) — 2
- [3D View Tool: Edit Mesh, Knife](#3d-view-tool:-edit-mesh,-knife) — 2
- [3D View Tool: Edit Mesh, Bisect](#3d-view-tool:-edit-mesh,-bisect) — 2
- [3D View Tool: Edit Mesh, Poly Build](#3d-view-tool:-edit-mesh,-poly-build) — 6
- [3D View Tool: Edit Mesh, Spin](#3d-view-tool:-edit-mesh,-spin) — 2
- [3D View Tool: Edit Mesh, Spin Duplicates](#3d-view-tool:-edit-mesh,-spin-duplicates) — 2
- [3D View Tool: Edit Mesh, Smooth](#3d-view-tool:-edit-mesh,-smooth) — 2
- [3D View Tool: Edit Mesh, Randomize](#3d-view-tool:-edit-mesh,-randomize) — 2
- [3D View Tool: Edit Mesh, Edge Slide](#3d-view-tool:-edit-mesh,-edge-slide) — 2
- [3D View Tool: Edit Mesh, Vertex Slide](#3d-view-tool:-edit-mesh,-vertex-slide) — 2
- [3D View Tool: Edit Mesh, Shrink/Fatten](#3d-view-tool:-edit-mesh,-shrinkfatten) — 2
- [3D View Tool: Edit Mesh, Push/Pull](#3d-view-tool:-edit-mesh,-pushpull) — 2
- [3D View Tool: Edit Mesh, To Sphere](#3d-view-tool:-edit-mesh,-to-sphere) — 2
- [3D View Tool: Edit Mesh, Rip Region](#3d-view-tool:-edit-mesh,-rip-region) — 2
- [3D View Tool: Edit Mesh, Rip Edge](#3d-view-tool:-edit-mesh,-rip-edge) — 2
- [3D View Tool: Edit Curve, Draw](#3d-view-tool:-edit-curve,-draw) — 2
- [3D View Tool: Edit Curve, Curve Pen](#3d-view-tool:-edit-curve,-curve-pen) — 6
- [3D View Tool: Edit Curve, Radius](#3d-view-tool:-edit-curve,-radius) — 2
- [3D View Tool: Edit Curve, Tilt](#3d-view-tool:-edit-curve,-tilt) — 2
- [3D View Tool: Edit Curve, Randomize](#3d-view-tool:-edit-curve,-randomize) — 2
- [3D View Tool: Edit Curve, Extrude](#3d-view-tool:-edit-curve,-extrude) — 2
- [3D View Tool: Edit Curve, Extrude to Cursor](#3d-view-tool:-edit-curve,-extrude-to-cursor) — 4
- [3D View Tool: Edit Curves, Draw](#3d-view-tool:-edit-curves,-draw) — 2
- [3D View Tool: Edit Curves, Pen](#3d-view-tool:-edit-curves,-pen) — 12
- [3D View Tool: Sculpt, Box Mask](#3d-view-tool:-sculpt,-box-mask) — 4
- [3D View Tool: Sculpt, Lasso Mask](#3d-view-tool:-sculpt,-lasso-mask) — 4
- [3D View Tool: Sculpt, Line Mask](#3d-view-tool:-sculpt,-line-mask) — 4
- [3D View Tool: Sculpt, Polyline Mask](#3d-view-tool:-sculpt,-polyline-mask) — 4
- [3D View Tool: Sculpt, Box Hide](#3d-view-tool:-sculpt,-box-hide) — 5
- [3D View Tool: Sculpt, Lasso Hide](#3d-view-tool:-sculpt,-lasso-hide) — 5
- [3D View Tool: Sculpt, Line Hide](#3d-view-tool:-sculpt,-line-hide) — 5
- [3D View Tool: Sculpt, Polyline Hide](#3d-view-tool:-sculpt,-polyline-hide) — 4
- [3D View Tool: Sculpt, Box Face Set](#3d-view-tool:-sculpt,-box-face-set) — 2
- [3D View Tool: Sculpt, Lasso Face Set](#3d-view-tool:-sculpt,-lasso-face-set) — 2
- [3D View Tool: Sculpt, Line Face Set](#3d-view-tool:-sculpt,-line-face-set) — 2
- [3D View Tool: Sculpt, Polyline Face Set](#3d-view-tool:-sculpt,-polyline-face-set) — 2
- [3D View Tool: Sculpt, Box Trim](#3d-view-tool:-sculpt,-box-trim) — 2
- [3D View Tool: Sculpt, Lasso Trim](#3d-view-tool:-sculpt,-lasso-trim) — 2
- [3D View Tool: Sculpt, Line Trim](#3d-view-tool:-sculpt,-line-trim) — 2
- [3D View Tool: Sculpt, Polyline Trim](#3d-view-tool:-sculpt,-polyline-trim) — 2
- [3D View Tool: Sculpt, Line Project](#3d-view-tool:-sculpt,-line-project) — 2
- [3D View Tool: Sculpt, Mesh Filter](#3d-view-tool:-sculpt,-mesh-filter) — 2
- [3D View Tool: Sculpt, Cloth Filter](#3d-view-tool:-sculpt,-cloth-filter) — 2
- [3D View Tool: Sculpt, Color Filter](#3d-view-tool:-sculpt,-color-filter) — 4
- [3D View Tool: Sculpt, Mask by Color](#3d-view-tool:-sculpt,-mask-by-color) — 2
- [3D View Tool: Sculpt, Face Set Edit](#3d-view-tool:-sculpt,-face-set-edit) — 2
- [3D View Tool: Paint Weight, Sample Weight](#3d-view-tool:-paint-weight,-sample-weight) — 4
- [3D View Tool: Paint Weight, Sample Vertex Group](#3d-view-tool:-paint-weight,-sample-vertex-group) — 2
- [3D View Tool: Paint Weight, Gradient](#3d-view-tool:-paint-weight,-gradient) — 2
- [3D View Tool: Paint Grease Pencil, Line](#3d-view-tool:-paint-grease-pencil,-line) — 6
- [3D View Tool: Paint Grease Pencil, Polyline](#3d-view-tool:-paint-grease-pencil,-polyline) — 4
- [3D View Tool: Paint Grease Pencil, Box](#3d-view-tool:-paint-grease-pencil,-box) — 6
- [3D View Tool: Paint Grease Pencil, Circle](#3d-view-tool:-paint-grease-pencil,-circle) — 6
- [3D View Tool: Paint Grease Pencil, Arc](#3d-view-tool:-paint-grease-pencil,-arc) — 6
- [3D View Tool: Paint Grease Pencil, Curve](#3d-view-tool:-paint-grease-pencil,-curve) — 2
- [3D View Tool: Paint Grease Pencil, Trim](#3d-view-tool:-paint-grease-pencil,-trim) — 2
- [3D View Tool: Paint Grease Pencil, Interpolate](#3d-view-tool:-paint-grease-pencil,-interpolate) — 2
- [3D View Tool: Paint Grease Pencil, Eyedropper](#3d-view-tool:-paint-grease-pencil,-eyedropper) — 8
- [3D View Tool: Edit Grease Pencil, Gradient](#3d-view-tool:-edit-grease-pencil,-gradient) — 2
- [3D View Tool: Edit Grease Pencil, Pen](#3d-view-tool:-edit-grease-pencil,-pen) — 12
- [3D View Tool: Edit Grease Pencil, Interpolate](#3d-view-tool:-edit-grease-pencil,-interpolate) — 2
- [3D View Tool: Paint Grease Pencil, Carver](#3d-view-tool:-paint-grease-pencil,-carver) — 2
- [Sequencer Tool: Select Box (fallback)](#sequencer-tool:-select-box-fallback) — 5
- [Preview Tool: Tweak](#preview-tool:-tweak) — 4
- [Preview Tool: Tweak (fallback)](#preview-tool:-tweak-fallback) — 2
- [Preview Tool: Select Box (fallback)](#preview-tool:-select-box-fallback) — 5
- [Sequencer Tool: Select Lasso](#sequencer-tool:-select-lasso) — 3
- [Sequencer Tool: Select Lasso (fallback)](#sequencer-tool:-select-lasso-fallback) — 3
- [Preview Tool: Select Lasso](#preview-tool:-select-lasso) — 3
- [Preview Tool: Select Lasso (fallback)](#preview-tool:-select-lasso-fallback) — 3
- [Preview Tool: Select Circle](#preview-tool:-select-circle) — 3
- [Preview Tool: Select Circle (fallback)](#preview-tool:-select-circle-fallback) — 3
- [Sequencer Tool: Select Circle](#sequencer-tool:-select-circle) — 3
- [Sequencer Tool: Select Circle (fallback)](#sequencer-tool:-select-circle-fallback) — 3
- [Sequencer Tool: Blade](#sequencer-tool:-blade) — 14
- [Sequencer Tool: Slip](#sequencer-tool:-slip) — 4
- [Preview Tool: Cursor](#preview-tool:-cursor) — 4
- [Preview Tool: Sample](#preview-tool:-sample) — 2
- [Preview Tool: Move](#preview-tool:-move) — 2
- [Preview Tool: Rotate](#preview-tool:-rotate) — 2
- [Preview Tool: Scale](#preview-tool:-scale) — 2

## Window

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Alt+Return | Batch Rename | `wm.batch_rename` |  |
| Ctrl+N | Reload Start-Up File | `wm.read_homefile` |  |
| Ctrl+Shift+O | Call Menu | `wm.call_menu` | name='TOPBAR_MT_file_open_recent' |
| Ctrl+O | Open | `wm.open_mainfile` |  |
| Ctrl+S | Save Blender File | `wm.save_mainfile` | show_save_modified_images_dialog=True |
| Ctrl+Shift+S | Save As | `wm.save_as_mainfile` | show_save_modified_images_dialog=True |
| Ctrl+Alt+S | Save Blender File | `wm.save_mainfile` | incremental=True, show_save_modified_images_dialog=True |
| Ctrl+Q | Quit Blender | `wm.quit_blender` |  |
| Shift+Tab | Call Menu | `wm.call_menu` | name='SCREEN_MT_user_menu' |
| NDOF Menu | Call Panel | `wm.call_panel` | name='USERPREF_PT_ndof_settings' |
| NDOF Plus | Context Scale Float | `wm.context_scale_float` | data_path='preferences.inputs.ndof_translation_sensitivity', value=1.1 |
| NDOF Minus | Context Scale Float | `wm.context_scale_float` | data_path='preferences.inputs.ndof_translation_sensitivity', value=0.9090909090909091 |
| Shift+NDOF Plus | Context Scale Float | `wm.context_scale_float` | data_path='preferences.inputs.ndof_translation_sensitivity', value=1.5 |
| Shift+NDOF Minus | Context Scale Float | `wm.context_scale_float` | data_path='preferences.inputs.ndof_translation_sensitivity', value=0.6666666666666666 |
| Any modifier+Timer Report any | Update Reports Display | `info.reports_display_update` |  |

## Screen

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| G (repeat) | Repeat Last | `screen.repeat_last` |  |
| Ctrl+, | Open Preferences... | `screen.userpref_show` |  |
| Any modifier+Timer 0 any | Animation Step | `screen.animation_step` |  |
| Any modifier+Timer Region any | Region Alpha | `screen.region_blend` |  |
| Ctrl+Tab | Cycle Space Context | `screen.space_context_cycle` | direction='NEXT' |
| Ctrl+Shift+Tab | Cycle Space Context | `screen.space_context_cycle` | direction='PREV' |
| Ctrl+Page Down | Cycle Workspace | `screen.workspace_cycle` | direction='NEXT' |
| Ctrl+Page Up | Cycle Workspace | `screen.workspace_cycle` | direction='PREV' |
| Return | Execute File Window | `file.execute` |  |
| Numpad Enter | Execute File Window | `file.execute` |  |
| Esc | Cancel File Operation | `file.cancel` |  |
| Ctrl+Z (repeat) | Undo Catalog Edits | `asset.catalog_undo` |  |
| Ctrl+Shift+Z (repeat) | Redo Catalog Edits | `asset.catalog_redo` |  |
| Ctrl+Z (repeat) | Undo | `ed.undo` |  |
| Ctrl+Shift+Z (repeat) | Redo | `ed.redo` |  |
| Ctrl+Alt+Z | Undo History | `ed.undo_history` |  |
| Esc | Cancel Render View | `render.view_cancel` |  |

## Screen Editing

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Handle Area Action Zones | `screen.actionzone` | modifier=0 |
| Shift+Left Mouse | Handle Area Action Zones | `screen.actionzone` | modifier=1 |
| Ctrl+Left Mouse | Handle Area Action Zones | `screen.actionzone` | modifier=2 |
| ActionZone Area any | Split Area | `screen.area_split` |  |
| ActionZone Area any | Join Area | `screen.area_join` |  |
| Shift+ActionZone Area any | Duplicate Area into New Window | `screen.area_dupli` |  |
| Ctrl+ActionZone Area any | Swap Areas | `screen.area_swap` |  |
| ActionZone Region any | Scale Region Size | `screen.region_scale` |  |
| ActionZone Quad any | Quad View Resize | `screen.quadview_size` |  |
| ActionZone Fullscreen any | Toggle Maximize Area | `screen.screen_full_area` | use_hide_panels=True |
| Left Mouse | Move Area Edges | `screen.area_move` |  |
| Ctrl+Left Mouse | Move Area Edges | `screen.area_move` | snap=True |
| Right Mouse | Area Edge Options | `screen.area_options` |  |
| Ctrl+Return | Render | `render.render` | use_viewport=True |
| Ctrl+Alt+Return | Render | `render.render` | animation=True, use_viewport=True |
| Alt+F12 | Render | `render.render` | use_sequencer_scene=True, use_viewport=True |
| Ctrl+Alt+F12 | Render | `render.render` | animation=True, use_sequencer_scene=True, use_viewport=True |
| Esc | Cancel Render View | `render.view_cancel` |  |

## Region Context Menu

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Right Mouse | Region | `screen.region_context_menu` |  |
| Left Mouse drag | Join Area (Moritz) | `screen.area_join` | header_drag=True |

## View2D

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Scroller Activate | `view2d.scroller_activate` |  |
| Middle Mouse | Scroller Activate | `view2d.scroller_activate` |  |
| Alt+Left Mouse | Pan View | `view2d.pan` |  |
| Alt+Middle Mouse | Pan View | `view2d.pan` |  |
| Alt+Right Mouse | Zoom 2D View | `view2d.zoom` |  |
| Mouse/Trackpad Pan any | Pan View | `view2d.pan` |  |
| Ctrl+Wheel Down | Scroll Right | `view2d.scroll_right` |  |
| Ctrl+Wheel Up | Scroll Left | `view2d.scroll_left` |  |
| Shift+Wheel Down | Scroll Down | `view2d.scroll_down` |  |
| Shift+Wheel Up | Scroll Up | `view2d.scroll_up` |  |
| NDOF Motion any | NDOF Pan/Zoom | `view2d.ndof` |  |
| Wheel Out | Zoom Out | `view2d.zoom_out` |  |
| Wheel In | Zoom In | `view2d.zoom_in` |  |
| Alt+Wheel Out | Zoom Out | `view2d.zoom_out` |  |
| Alt+Wheel In | Zoom In | `view2d.zoom_in` |  |
| Numpad - (repeat) | Zoom Out | `view2d.zoom_out` |  |
| Numpad + (repeat) | Zoom In | `view2d.zoom_in` |  |
| Ctrl+Mouse/Trackpad Pan any | Zoom 2D View | `view2d.zoom` |  |
| Any modifier+Timer 1 any | Smooth View 2D | `view2d.smoothview` |  |
| Wheel Down | Scroll Down | `view2d.scroll_down` |  |
| Wheel Up | Scroll Up | `view2d.scroll_up` |  |
| Wheel Down | Scroll Right | `view2d.scroll_right` |  |
| Wheel Up | Scroll Left | `view2d.scroll_left` |  |
| Mouse/Trackpad Zoom any | Zoom 2D View | `view2d.zoom` |  |
| Z | Zoom to Border | `view2d.zoom_border` |  |

## View2D Buttons List

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Scroller Activate | `view2d.scroller_activate` |  |
| Middle Mouse | Scroller Activate | `view2d.scroller_activate` |  |
| Alt+Left Mouse | Pan View | `view2d.pan` |  |
| Alt+Middle Mouse | Pan View | `view2d.pan` |  |
| Mouse/Trackpad Pan any | Pan View | `view2d.pan` |  |
| Middle Mouse | Pan View | `view2d.pan` |  |
| Wheel Down | Scroll Down | `view2d.scroll_down` |  |
| Wheel Up | Scroll Up | `view2d.scroll_up` |  |
| Page Down (repeat) | Scroll Down | `view2d.scroll_down` | page=True |
| Page Up (repeat) | Scroll Up | `view2d.scroll_up` | page=True |
| Alt+Right Mouse | Zoom 2D View | `view2d.zoom` |  |
| Mouse/Trackpad Zoom any | Zoom 2D View | `view2d.zoom` |  |
| Ctrl+Mouse/Trackpad Pan any | Zoom 2D View | `view2d.zoom` |  |
| Numpad - (repeat) | Zoom Out | `view2d.zoom_out` |  |
| Numpad + (repeat) | Zoom In | `view2d.zoom_in` |  |
| A | Reset View | `view2d.reset` |  |

## User Interface

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| I | Eyedropper | `ui.eyedropper_color` |  |
| I | Eyedropper Colorband | `ui.eyedropper_colorramp` |  |
| Alt+I | Eyedropper Colorband (Points) | `ui.eyedropper_colorramp_point` |  |
| I | Eyedropper Data-Block | `ui.eyedropper_id` |  |
| I | Eyedropper Depth | `ui.eyedropper_depth` |  |
| I | Eyedropper Bone | `ui.eyedropper_bone` |  |
| Ctrl+C | Copy Data Path | `ui.copy_data_path_button` |  |
| Ctrl+Alt+C | Copy Data Path | `ui.copy_data_path_button` | full_path=True |
| S | Insert Keyframe (Buttons) | `anim.keyframe_insert_button` |  |
| Alt+S | Delete Keyframe (Buttons) | `anim.keyframe_delete_button` |  |
| Shift+Alt+S | Clear Keyframe (Buttons) | `anim.keyframe_clear_button` |  |
| D | Add Driver | `anim.driver_button_add` |  |
| Alt+D | Remove Driver | `anim.driver_button_remove` |  |
| K | Add to Keying Set | `anim.keyingset_button_add` |  |
| Alt+K | Remove from Keying Set | `anim.keyingset_button_remove` |  |
| Left Mouse | Select View Item | `ui.view_item_select` |  |
| Wheel Up any | View Scroll | `ui.view_scroll` |  |
| Wheel Down any | View Scroll | `ui.view_scroll` |  |
| Mouse/Trackpad Pan any | View Scroll | `ui.view_scroll` |  |

## Property Editor

Space `PROPERTIES`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Tab | Search Menu | `wm.search_menu` |  |
| Right Mouse | Context Menu | `buttons.context_menu` |  |
| Ctrl+Wheel Up | Cycle Space Context | `screen.space_context_cycle` | direction='PREV' |
| Ctrl+Wheel Down | Cycle Space Context | `screen.space_context_cycle` | direction='NEXT' |
| Ctrl+F | Filter | `buttons.start_filter` |  |
| Esc | Clear Filter | `buttons.clear_filter` |  |
| Left Mouse | Set Active Modifier | `object.modifier_set_active` |  |
| Backspace | Remove Modifier | `object.modifier_remove` | report=True |
| Delete | Remove Modifier | `object.modifier_remove` | report=True |
| Ctrl+D | Copy Modifier | `object.modifier_copy` |  |
| Backspace | Remove Grease Pencil Effect | `object.shaderfx_remove` | report=True |
| Delete | Remove Grease Pencil Effect | `object.shaderfx_remove` | report=True |
| Ctrl+D |  | `objectshaderfx_copy` |  |
| Backspace | Delete Constraint | `constraint.delete` | report=True |
| Delete | Delete Constraint | `constraint.delete` | report=True |
| Ctrl+D | Duplicate Constraint | `constraint.copy` |  |
| Left Mouse | Set Active Strip Modifier | `sequencer.strip_modifier_set_active` |  |
| Left Mouse | Set Active Scene Effect | `scene.set_active_compositor_effect` |  |
| Backspace | Remove Scene Effect | `scene.remove_compositor_effect` |  |
| Delete | Remove Scene Effect | `scene.remove_compositor_effect` |  |
| Ctrl+D | Duplicate Scene Effect | `scene.duplicate_compositor_effect` |  |

## Outliner

Space `OUTLINER`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse double click | Rename | `outliner.item_rename` |  |
| Return | Rename | `outliner.item_rename` | use_active=True |
| Tab | Search Menu | `wm.search_menu` |  |
| Any modifier+Mouse Move any | Update Highlight | `outliner.highlight_update` |  |
| Left Mouse click | Select | `outliner.item_activate` | extend=False, deselect_all=True |
| Ctrl+Left Mouse click | Select | `outliner.item_activate` | extend=True, deselect_all=True |
| Shift+Left Mouse click | Select | `outliner.item_activate` | extend=False, extend_range=True, deselect_all=True |
| Ctrl+Shift+Left Mouse click | Select | `outliner.item_activate` | extend=True, extend_range=True, deselect_all=True |
| Left Mouse double click | Select | `outliner.item_activate` | recurse=True, deselect_all=True |
| Ctrl+Left Mouse double click | Select | `outliner.item_activate` | recurse=True, extend=True, deselect_all=True |
| Shift+Left Mouse double click | Select | `outliner.item_activate` | recurse=True, extend_range=True, deselect_all=True |
| Ctrl+Shift+Left Mouse double click | Select | `outliner.item_activate` | recurse=True, extend=True, extend_range=True, deselect_all=True |
| Left Mouse drag | Box Select | `outliner.select_box` | tweak=True |
| Shift+Left Mouse drag | Box Select | `outliner.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `outliner.select_box` | tweak=True, mode='SUB' |
| Up Arrow (repeat) | Walk Select | `outliner.select_walk` | direction='UP' |
| Shift+Up Arrow (repeat) | Walk Select | `outliner.select_walk` | direction='UP', extend=True |
| Down Arrow (repeat) | Walk Select | `outliner.select_walk` | direction='DOWN' |
| Shift+Down Arrow (repeat) | Walk Select | `outliner.select_walk` | direction='DOWN', extend=True |
| Left Arrow (repeat) | Walk Select | `outliner.select_walk` | direction='LEFT' |
| Shift+Left Arrow (repeat) | Walk Select | `outliner.select_walk` | direction='LEFT', toggle_all=True |
| Right Arrow (repeat) | Walk Select | `outliner.select_walk` | direction='RIGHT' |
| Shift+Right Arrow (repeat) | Walk Select | `outliner.select_walk` | direction='RIGHT', toggle_all=True |
| Left Mouse click | Open/Close | `outliner.item_openclose` | all=False |
| Shift+Left Mouse click | Open/Close | `outliner.item_openclose` | all=True |
| Left Mouse drag | Open/Close | `outliner.item_openclose` | all=False |
| Right Mouse | Context Menu | `outliner.operation` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='OUTLINER_MT_context_menu' |
| Left Mouse drag | Drag and Drop | `outliner.item_drag_drop` |  |
| Shift+Left Mouse drag | Drag and Drop | `outliner.item_drag_drop` |  |
| A | Show Hierarchy | `outliner.show_hierarchy` |  |
| . | Show Active | `outliner.show_active` |  |
| F | Show Active | `outliner.show_active` |  |
| Page Down (repeat) | Scroll Page | `outliner.scroll_page` | up=False |
| Page Up (repeat) | Scroll Page | `outliner.scroll_page` | up=True |
| Numpad + | Show/Hide One Level | `outliner.show_one_level` |  |
| Numpad - | Show/Hide One Level | `outliner.show_one_level` | open=False |
| Ctrl+A | Toggle Selected | `outliner.select_all` | action='SELECT' |
| Ctrl+Shift+A | Toggle Selected | `outliner.select_all` | action='DESELECT' |
| Ctrl+I | Toggle Selected | `outliner.select_all` | action='INVERT' |
| K | Keying Set Add Selected | `outliner.keyingset_add_selected` |  |
| Alt+K | Keying Set Remove Selected | `outliner.keyingset_remove_selected` |  |
| S | Insert Keyframe | `anim.keyframe_insert` |  |
| Alt+S | Delete Keying-Set Keyframe | `anim.keyframe_delete` |  |
| Ctrl+D | Add Drivers for Selected | `outliner.drivers_add_selected` |  |
| Ctrl+Alt+D | Delete Drivers for Selected | `outliner.drivers_delete_selected` |  |
| Backspace | Delete | `outliner.delete` |  |
| Delete | Delete | `outliner.delete` |  |
| Ctrl+G | Call Menu | `wm.call_menu` | name='OBJECT_MT_move_to_collection' |
| Ctrl+Shift+M | Call Menu | `wm.call_menu` | name='OBJECT_MT_link_to_collection' |
| E | Disable from View Layer | `outliner.collection_exclude_set` |  |
| Alt+E | Enable in View Layer | `outliner.collection_exclude_clear` |  |
| Ctrl+H | Hide | `outliner.hide` |  |
| Alt+H | Unhide All | `outliner.unhide_all` |  |
| Ctrl+F | Filter | `outliner.start_filter` |  |
| Alt+F | Clear Filter | `outliner.clear_filter` |  |
| Ctrl+C | Outliner ID Data Copy | `outliner.id_copy` |  |
| Ctrl+V | Outliner ID Data Paste | `outliner.id_paste` |  |

## UV Editor

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Tab | Search Menu | `wm.search_menu` |  |
| 1 | Select Mode | `mesh.select_mode` | type='VERT' |
| 2 | Select Mode | `mesh.select_mode` | type='EDGE' |
| 3 | Select Mode | `mesh.select_mode` | type='FACE' |
| Shift+1 | Select Mode | `mesh.select_mode` | use_extend=True, type='VERT' |
| Shift+2 | Select Mode | `mesh.select_mode` | use_extend=True, type='EDGE' |
| Shift+3 | Select Mode | `mesh.select_mode` | use_extend=True, type='FACE' |
| Ctrl+1 | Select Mode | `mesh.select_mode` | use_expand=True, type='VERT' |
| Ctrl+2 | Select Mode | `mesh.select_mode` | use_expand=True, type='EDGE' |
| Ctrl+3 | Select Mode | `mesh.select_mode` | use_expand=True, type='FACE' |
| Ctrl+Shift+1 | Select Mode | `mesh.select_mode` | use_extend=True, use_expand=True, type='VERT' |
| Ctrl+Shift+2 | Select Mode | `mesh.select_mode` | use_extend=True, use_expand=True, type='EDGE' |
| Ctrl+Shift+3 | Select Mode | `mesh.select_mode` | use_extend=True, use_expand=True, type='FACE' |
| 1 | UV Select Mode | `uv.select_mode` | type='VERTEX' |
| 2 | UV Select Mode | `uv.select_mode` | type='EDGE' |
| 3 | UV Select Mode | `uv.select_mode` | type='FACE' |
| 4 | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_uv_select_island' |
| Left Mouse click | Select | `uv.select` | deselect_all=True |
| Shift+Left Mouse click | Select | `uv.select` | toggle=True, deselect_all=False |
| Left Mouse drag | Move | `transform.translate` |  |
| Shift+Left Mouse double click | Loop Select | `uv.select_loop` | extend=True |
| Left Mouse double click | Loop Select | `uv.select_loop` | extend=False |
| Ctrl+L | Select Linked | `uv.select_linked` |  |
| Up Arrow (repeat) | Select More | `uv.select_more` |  |
| Down Arrow (repeat) | Select Less | `uv.select_less` |  |
| Ctrl+A | (De)select All | `uv.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `uv.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `uv.select_all` | action='INVERT' |
| Ctrl+H | Hide Selected | `uv.hide` | unselected=False |
| Shift+H | Hide Selected | `uv.hide` | unselected=True |
| Alt+H | Reveal Hidden | `uv.reveal` |  |
| Ctrl+C | Copy UVs | `uv.copy` |  |
| Ctrl+V | Paste UVs | `uv.paste` |  |
| Shift+X | Call Pie Menu | `wm.call_menu_pie` | name='IMAGE_MT_uvs_snap_pie' |
| Right Mouse | Call Menu | `wm.call_menu` | name='IMAGE_MT_uvs_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='IMAGE_MT_uvs_context_menu' |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| X | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_snap' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |

## 3D View Generic

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+[ | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Shift+Space Bar | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_asset_shelf' |

## 3D View

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Tab | Search Menu | `wm.search_menu` |  |
| Shift+Right Mouse | Set 3D Cursor | `view3d.cursor3d` |  |
| Shift+Right Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |
| Shift+I | Local View | `view3d.localview` |  |
| Mouse/Trackpad Smart Zoom any | Local View | `view3d.localview` |  |
| V | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_view_pie' |
| Alt+Left Mouse | Rotate View | `view3d.rotate` |  |
| Wheel Left | Pan View Direction | `view3d.view_pan` | type='PANLEFT' |
| Wheel Right | Pan View Direction | `view3d.view_pan` | type='PANRIGHT' |
| Alt+Middle Mouse | Pan View | `view3d.move` |  |
| Alt+Right Mouse | Zoom View | `view3d.zoom` |  |
| F | Frame Selected | `view3d.view_selected` | use_all_regions=False |
| Shift+F | Center View to Mouse | `view3d.view_center_pick` |  |
| Any modifier+Timer 1 any | Smooth View | `view3d.smoothview` |  |
| Mouse/Trackpad Pan any | Rotate View | `view3d.rotate` |  |
| Mouse/Trackpad Rotate any | Rotate View | `view3d.rotate` |  |
| Shift+Mouse/Trackpad Pan any | Pan View | `view3d.move` |  |
| Mouse/Trackpad Zoom any | Zoom View | `view3d.zoom` |  |
| Ctrl+Mouse/Trackpad Pan any | Zoom View | `view3d.zoom` |  |
| Numpad + (repeat) | Zoom View | `view3d.zoom` | delta=1 |
| Numpad - (repeat) | Zoom View | `view3d.zoom` | delta=-1 |
| Wheel In | Zoom View | `view3d.zoom` | delta=1 |
| Wheel Out | Zoom View | `view3d.zoom` | delta=-1 |
| Alt+Wheel In | Zoom View | `view3d.zoom` | delta=1 |
| Alt+Wheel Out | Zoom View | `view3d.zoom` | delta=-1 |
| Shift+Numpad + (repeat) | Dolly View | `view3d.dolly` | delta=1 |
| Shift+Numpad - (repeat) | Dolly View | `view3d.dolly` | delta=-1 |
| A | Frame All | `view3d.view_all` | center=False |
| Shift+A | Frame All | `view3d.view_all` | use_all_regions=True, center=False |
| F4 | View Camera | `view3d.view_camera` |  |
| F1 | View Axis | `view3d.view_axis` | type='FRONT' |
| F2 | View Axis | `view3d.view_axis` | type='RIGHT' |
| F3 | View Axis | `view3d.view_axis` | type='TOP' |
| Ctrl+F1 | View Axis | `view3d.view_axis` | type='BACK' |
| Ctrl+F2 | View Axis | `view3d.view_axis` | type='LEFT' |
| Ctrl+F3 | View Axis | `view3d.view_axis` | type='BOTTOM' |
| F5 | View Orbit | `view3d.view_orbit` | angle=3.1415927, type='ORBITRIGHT' |
| NDOF Motion any | NDOF Orbit View with Zoom | `view3d.ndof_orbit_zoom` |  |
| Ctrl+NDOF Motion any | NDOF Orbit View | `view3d.ndof_orbit` |  |
| Shift+NDOF Motion any | NDOF Pan View | `view3d.ndof_pan` |  |
| Ctrl+Shift+NDOF Motion any | NDOF Transform View | `view3d.ndof_all` |  |
| NDOF Fit | Frame Selected | `view3d.view_selected` | use_all_regions=False |
| NDOF Roll CCW | View Roll | `view3d.view_roll` | type='LEFT' |
| NDOF Roll CCW | View Roll | `view3d.view_roll` | type='RIGHT' |
| NDOF Front | View Axis | `view3d.view_axis` | type='FRONT' |
| NDOF Back | View Axis | `view3d.view_axis` | type='BACK' |
| NDOF Left | View Axis | `view3d.view_axis` | type='LEFT' |
| NDOF Right | View Axis | `view3d.view_axis` | type='RIGHT' |
| NDOF Top | View Axis | `view3d.view_axis` | type='TOP' |
| NDOF Bottom | View Axis | `view3d.view_axis` | type='BOTTOM' |
| Shift+NDOF Front | View Axis | `view3d.view_axis` | type='FRONT', align_active=True |
| Shift+NDOF Right | View Axis | `view3d.view_axis` | type='RIGHT', align_active=True |
| Shift+NDOF Top | View Axis | `view3d.view_axis` | type='TOP', align_active=True |
| Left Mouse click | Select | `view3d.select` | deselect_all=True |
| Shift+Left Mouse click | Select | `view3d.select` | toggle=True |
| Ctrl+Left Mouse click | Select | `view3d.select` | center=True, object=True |
| Ctrl+Shift+Left Mouse click | Select | `view3d.select` | extend=True, toggle=True, center=True |
| Shift+Alt+Left Mouse click | Select | `view3d.select` | toggle=True, enumerate=True |
| Ctrl+Shift+Alt+Left Mouse click | Select | `view3d.select` | toggle=True, center=True, enumerate=True |
| Z | Zoom to Border | `view3d.zoom_border` |  |
| Ctrl+C | Copy Objects | `view3d.copybuffer` |  |
| Ctrl+V | Paste Objects | `view3d.pastebuffer` |  |
| Shift+X | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_snap_pie' |
| Left Mouse drag | Move | `transform.translate` |  |
| . | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_pivot_pie' |
| , | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_orientations_pie' |
| Alt+X | Toggle X-Ray | `view3d.toggle_xray` |  |
| X | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_snap' |

## Mask Editing

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Tab | Search Menu | `wm.search_menu` |  |
| Alt+N | New Mask | `mask.new` |  |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit_mask' |
| Ctrl+Left Mouse | Add Vertex and Slide | `mask.add_vertex_slide` |  |
| Ctrl+Shift+Left Mouse | Add Feather Vertex and Slide | `mask.add_feather_vertex_slide` |  |
| Backspace | Delete | `mask.delete` |  |
| Delete | Delete | `mask.delete` |  |
| Shift+Left Mouse | Select | `mask.select` | extend=False, deselect=False, toggle=True |
| Ctrl+A | (De)select All | `mask.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `mask.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `mask.select_all` | action='INVERT' |
| Ctrl+L | Select Linked All | `mask.select_linked` |  |
| L | Select Linked | `mask.select_linked_pick` | deselect=False |
| Shift+L | Select Linked | `mask.select_linked_pick` | deselect=True |
| Q | Box Select | `mask.select_box` |  |
| C | Circle Select | `mask.select_circle` |  |
| Ctrl+Alt+Right Mouse drag | Lasso Select | `mask.select_lasso` | mode='ADD' |
| Ctrl+Shift+Alt+Right Mouse drag | Lasso Select | `mask.select_lasso` | mode='SUB' |
| Up Arrow (repeat) | Select More | `mask.select_more` |  |
| Down Arrow (repeat) | Select Less | `mask.select_less` |  |
| Alt+H | Clear Restrict View | `mask.hide_view_clear` |  |
| Ctrl+H | Set Restrict View | `mask.hide_view_set` | unselected=False |
| Shift+H | Set Restrict View | `mask.hide_view_set` | unselected=True |
| Ctrl+Left Mouse | Select | `clip.select` | extend=False |
| Alt+C | Toggle Cyclic | `mask.cyclic_toggle` |  |
| Left Mouse | Slide Point | `mask.slide_point` |  |
| Left Mouse | Slide Spline Curvature | `mask.slide_spline_curvature` |  |
| V | Set Handle Type | `mask.handle_type_set` |  |
| Ctrl+P | Make Parent | `mask.parent_set` |  |
| Shift+P | Clear Parent | `mask.parent_clear` |  |
| I | Insert Shape Key | `mask.shape_key_insert` |  |
| Alt+I | Clear Shape Key | `mask.shape_key_clear` |  |
| Ctrl+D | Add Duplicate | `mask.duplicate_move` |  |
| Ctrl+C | Copy Splines | `mask.copy_splines` |  |
| Ctrl+V | Paste Splines | `mask.paste_splines` |  |
| W | Move | `transform.translate` |  |
| R | Resize | `transform.resize` |  |
| E | Rotate | `transform.rotate` |  |

## Markers

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Tab | Search Menu | `wm.search_menu` |  |
| M | Add Time Marker | `marker.add` |  |
| Left Mouse drag | Move Time Marker | `marker.move` |  |
| Ctrl+D | Duplicate Time Marker | `marker.duplicate` |  |
| Left Mouse | Select Time Marker | `marker.select` |  |
| Shift+Left Mouse | Select Time Marker | `marker.select` | extend=True |
| Ctrl+Left Mouse | Select Time Marker | `marker.select` | extend=False, camera=True |
| Ctrl+Shift+Left Mouse | Select Time Marker | `marker.select` | extend=True, camera=True |
| Ctrl+Left Mouse click | Select Markers Before/After Current Frame | `marker.select_leftright` | mode='CLICK_SIDE', extend=False |
| Ctrl+Shift+Left Mouse click | Select Markers Before/After Current Frame | `marker.select_leftright` | mode='CLICK_SIDE', extend=True |
| [ | Select Markers Before/After Current Frame | `marker.select_leftright` | mode='LEFT', extend=False |
| ] | Select Markers Before/After Current Frame | `marker.select_leftright` | mode='RIGHT', extend=False |
| Q | Marker Box Select | `marker.select_box` |  |
| Ctrl+A | (De)select all Markers | `marker.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select all Markers | `marker.select_all` | action='DESELECT' |
| Ctrl+I | (De)select all Markers | `marker.select_all` | action='INVERT' |
| Backspace | Delete Markers | `marker.delete` |  |
| Delete | Delete Markers | `marker.delete` | confirm=False |
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name_marker', keep_open=False |
| Left Mouse double click | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name_marker', keep_open=False |
| W | Move Time Marker | `marker.move` |  |

## Graph Editor Generic

Space `GRAPH_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Ctrl+F | Filter Channels | `anim.channels_select_filter` |  |
| Ctrl+H | Hide Curves | `graph.hide` | unselected=False |
| Shift+H | Hide Curves | `graph.hide` | unselected=True |
| Alt+H | Reveal Curves | `graph.reveal` |  |

## Graph Editor

Space `GRAPH_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Tab | Search Menu | `wm.search_menu` |  |
| Ctrl+[ | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_channels' |
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Left Arrow | Frame Offset | `screen.frame_offset` | delta=-1 |
| Right Arrow | Frame Offset | `screen.frame_offset` | delta=1 |
| Ctrl+Right Arrow | Jump to Endpoint | `screen.frame_jump` | end=True |
| Ctrl+Left Arrow | Jump to Endpoint | `screen.frame_jump` | end=False |
| Ctrl+Right Mouse | Set Cursor | `graph.cursor_set` |  |
| Left Mouse | Select Keyframes | `graph.clickselect` | extend=False, deselect_all=True, column=False, curves=False |
| Alt+Left Mouse | Select Keyframes | `graph.clickselect` | extend=False, column=True, curves=False |
| Shift+Left Mouse | Select Keyframes | `graph.clickselect` | extend=True, column=False, curves=False |
| Shift+Alt+Left Mouse | Select Keyframes | `graph.clickselect` | extend=True, column=True, curves=False |
| Ctrl+Alt+Left Mouse | Select Keyframes | `graph.clickselect` | extend=False, column=False, curves=True |
| Ctrl+Shift+Alt+Left Mouse | Select Keyframes | `graph.clickselect` | extend=True, column=False, curves=True |
| Ctrl+Shift+Left Mouse | Select Left/Right | `graph.select_leftright` | mode='CHECK', extend=True |
| [ | Select Left/Right | `graph.select_leftright` | mode='LEFT', extend=False |
| ] | Select Left/Right | `graph.select_leftright` | mode='RIGHT', extend=False |
| Ctrl+A | Select All | `graph.select_all` | action='SELECT' |
| Ctrl+Shift+A | Select All | `graph.select_all` | action='DESELECT' |
| Ctrl+I | Select All | `graph.select_all` | action='INVERT' |
| Q | Box Select | `graph.select_box` | axis_range=False |
| Alt+Q | Box Select | `graph.select_box` | axis_range=True |
| Left Mouse drag | Box Select | `graph.select_box` | tweak=True, axis_range=False, mode='SET' |
| Shift+Left Mouse drag | Box Select | `graph.select_box` | tweak=True, axis_range=False, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `graph.select_box` | tweak=True, axis_range=False, mode='SUB' |
| Up Arrow (repeat) | Select More | `graph.select_more` |  |
| Down Arrow (repeat) | Select Less | `graph.select_less` |  |
| Ctrl+L | Select Linked | `graph.select_linked` |  |
| Backspace | Call Menu | `wm.call_menu` | name='GRAPH_MT_delete' |
| Delete | Delete Keyframes | `graph.delete` | confirm=False |
| Right Mouse | Call Menu | `wm.call_menu` | name='GRAPH_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='GRAPH_MT_context_menu' |
| Ctrl+D | Duplicate | `graph.duplicate_move` |  |
| S | Insert Keyframes | `graph.keyframe_insert` |  |
| Ctrl+C | Copy Keyframes | `graph.copy` |  |
| Ctrl+V | Paste Keyframes | `graph.paste` |  |
| Ctrl+Shift+V | Paste Keyframes | `graph.paste` | flipped=True |
| Ctrl+Alt+P | Set Preview Range to Selected | `graph.previewrange_set` |  |
| A | Frame All | `graph.view_all` |  |
| NDOF Fit | Frame All | `graph.view_all` |  |
| F | Frame Selected | `graph.view_selected` |  |
| Shift+A | Go to Current Frame | `graph.view_frame` |  |
| Left Mouse double click | Toggle Channel Editability | `anim.channels_editable_toggle` |  |
| W | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Middle Mouse drag | Move | `transform.translate` |  |
| Y | Transform | `transform.transform` | mode='TIME_EXTEND' |
| E | Rotate | `transform.rotate` |  |
| R | Resize | `transform.resize` |  |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_fcurve' |
| X | Context Enum Menu | `wm.context_menu_enum` | data_path='space_data.auto_snap' |
| M | Add Time Marker | `marker.add` |  |
| Shift+X | Call Pie Menu | `wm.call_menu_pie` | name='GRAPH_MT_snap_pie' |

## Image Generic

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Ctrl+[ | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Tab | Search Menu | `wm.search_menu` |  |
| Alt+N | New Image | `image.new` |  |
| Alt+O | Open Image | `image.open` |  |
| Alt+R | Reload Image | `image.reload` |  |
| Ctrl+R | Open Cached Render | `image.read_viewlayers` |  |
| Alt+S | Save Image | `image.save` |  |
| Shift+Alt+S | Save As Image | `image.save_as` |  |

## Image

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| A | Frame All | `image.view_all` |  |
| F | View Center | `image.view_selected` |  |
| Alt+Middle Mouse | Pan View | `image.view_pan` |  |
| Alt+Left Mouse | Pan View | `image.view_pan` |  |
| Mouse/Trackpad Pan any | Pan View | `image.view_pan` |  |
| NDOF Fit | Frame All | `image.view_all` |  |
| NDOF Motion any | NDOF Pan/Zoom | `image.view_ndof` |  |
| Wheel In | Zoom In | `image.view_zoom_in` |  |
| Wheel Out | Zoom Out | `image.view_zoom_out` |  |
| Alt+Wheel In | Zoom In | `image.view_zoom_in` |  |
| Alt+Wheel Out | Zoom Out | `image.view_zoom_out` |  |
| Numpad + (repeat) | Zoom In | `image.view_zoom_in` |  |
| Numpad - (repeat) | Zoom Out | `image.view_zoom_out` |  |
| Alt+Right Mouse | Zoom View | `image.view_zoom` |  |
| Mouse/Trackpad Zoom any | Zoom View | `image.view_zoom` |  |
| Ctrl+Mouse/Trackpad Pan any | Zoom View | `image.view_zoom` |  |
| Z | Zoom to Border | `image.view_zoom_border` |  |
| F1 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=1.0 |
| F2 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=0.5 |
| F3 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=0.25 |
| F4 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=0.125 |
| Ctrl+F4 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=8.0 |
| Ctrl+F3 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=4.0 |
| Ctrl+F2 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=2.0 |
| Ctrl+F1 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=1.0 |
| Shift+F4 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=8.0 |
| Shift+F3 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=4.0 |
| Shift+F2 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=2.0 |
| Shift+F1 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=1.0 |
| Left Mouse | Change Frame | `image.change_frame` |  |
| Left Mouse | Sample Color | `image.sample` |  |
| Ctrl+Left Mouse | Set Curves Point | `image.curves_point_set` | point='BLACK_POINT' |
| Shift+Left Mouse | Set Curves Point | `image.curves_point_set` | point='WHITE_POINT' |
| . | Call Pie Menu | `wm.call_menu_pie` | name='IMAGE_MT_pivot_pie' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| I | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.sample', cycle=True |

## Node Generic

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Tab | Search Single Menu | `wm.search_single_menu` | menu_idname='NODE_MT_add' |
| Ctrl+[ | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |

## Node Editor

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `node.select` | deselect_all=True, select_passthrough=True |
| Ctrl+Left Mouse | Select | `node.select` |  |
| Alt+Left Mouse | Select | `node.select` |  |
| Ctrl+Alt+Left Mouse | Select | `node.select` |  |
| Shift+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Left Mouse | Select | `node.select` | toggle=True |
| Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Left Mouse click | Select | `node.select` | deselect_all=True |
| Left Mouse drag | Box Select | `node.select_box` | tweak=True |
| Ctrl+Alt+Left Mouse drag | Lasso Select | `node.select_lasso` | mode='ADD' |
| Ctrl+Shift+Alt+Left Mouse drag | Lasso Select | `node.select_lasso` | mode='SUB' |
| Left Mouse drag | Link Nodes | `node.link` | detach=False |
| Ctrl+Left Mouse drag | Link Nodes | `node.link` | detach=True |
| Left Mouse drag | Resize Node | `node.resize` |  |
| Shift+Right Mouse drag | Add Reroute | `node.add_reroute` |  |
| Ctrl+Right Mouse drag | Cut Links | `node.links_cut` |  |
| Ctrl+Alt+Right Mouse drag | Mute Links | `node.links_mute` |  |
| Ctrl+Shift+Left Mouse | Link Viewer | `node.select_link_viewer` |  |
| Alt+A | Background Image Fit | `node.backimage_fit` |  |
| Alt+Left Mouse | Backimage Sample | `node.backimage_sample` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='NODE_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='NODE_MT_context_menu' |
| L | Make Links | `node.link_make` | replace=False |
| Shift+L | Make Links | `node.link_make` | replace=True |
| Ctrl+D | Duplicate | `node.duplicate_move` | NODE_OT_translate_attach={TRANSFORM_OT_translate=[('view2d_edge_pan', True)]} |
| P | Make Parent | `node.parent_set` |  |
| Ctrl+J | Join Nodes in Frame | `node.join` |  |
| Ctrl+H | Collapse | `node.hide_toggle` |  |
| M | Toggle Node Mute | `node.mute_toggle` |  |
| Shift+H | Toggle Node Preview | `node.preview_toggle` |  |
| Ctrl+H | Toggle Hidden Node Sockets | `node.hide_socket_toggle` |  |
| A | Frame All | `node.view_all` |  |
| NDOF Fit | Frame All | `node.view_all` |  |
| F | Frame Selected | `node.view_selected` |  |
| Q | Box Select | `node.select_box` | tweak=False |
| Backspace | Delete | `node.delete` |  |
| Delete | Delete | `node.delete` |  |
| Ctrl+Backspace | Delete with Reconnect | `node.delete_reconnect` |  |
| Ctrl+Delete | Delete with Reconnect | `node.delete_reconnect` |  |
| Ctrl+A | (De)select All | `node.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `node.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `node.select_all` | action='INVERT' |
| Shift+[ | Select Linked To | `node.select_linked_to` |  |
| ] | Select Linked From | `node.select_linked_from` |  |
| Shift+] | Activate Same Type Next/Prev | `node.select_same_type_step` | prev=False |
| Shift+[ | Activate Same Type Next/Prev | `node.select_same_type_step` | prev=True |
| Left Mouse double click | Edit Comment | `node.comment_edit` |  |
| Ctrl+F | Find Node | `node.find_node` |  |
| Ctrl+G | Make Group | `node.group_make` |  |
| Ctrl+Alt+G | Ungroup | `node.group_ungroup` |  |
| Left Mouse double click | Edit Group | `node.group_edit` | exit=False |
| Esc | Edit Group | `node.group_edit` | exit=True |
| Ctrl+C | Copy to Clipboard | `node.clipboard_copy` |  |
| Ctrl+V | Paste from Clipboard | `node.clipboard_paste` |  |
| Ctrl+X | Delete with Copy and Reconnect | `node.delete_copy_reconnect` |  |
| W | Move and Attach | `node.translate_attach` |  |
| Left Mouse drag | Move and Attach | `node.translate_attach` |  |
| Middle Mouse drag | Move and Attach | `node.translate_attach` |  |
| W | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |
| E | Rotate | `transform.rotate` |  |
| R | Resize | `transform.resize` |  |
| Alt+Right Mouse drag | Detach | `node.move_detach_links_release` |  |
| Alt+Left Mouse drag | Detach | `node.move_detach_links` |  |
| X | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_snap_node' |

## Info

Space `INFO`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Tab | Search Menu | `wm.search_menu` |  |
| Left Mouse | Select Report | `info.select_pick` |  |
| Shift+Left Mouse | Select Report | `info.select_pick` | extend=True |
| Left Mouse drag | Box Select | `info.select_box` | wait_for_input=False |
| Ctrl+A | (De)select All | `info.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `info.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `info.select_all` | action='INVERT' |
| Q | Box Select | `info.select_box` |  |
| R | Replay Operators | `info.report_replay` |  |
| Backspace | Delete Reports | `info.report_delete` |  |
| Delete | Delete Reports | `info.report_delete` |  |
| Ctrl+C | Copy Reports to Clipboard | `info.report_copy` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='INFO_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='INFO_MT_context_menu' |

## File Browser

Space `FILE_BROWSER`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_tool_props' |
| Alt+Up Arrow | Parent Directory | `file.parent` |  |
| Ctrl+Up Arrow | Parent Directory | `file.parent` |  |
| Alt+Left Arrow | Previous Folder | `file.previous` |  |
| Ctrl+Left Arrow | Previous Folder | `file.previous` |  |
| Button4 Mouse | Previous Folder | `file.previous` |  |
| Ctrl+[ | Previous Folder | `file.previous` |  |
| Alt+Right Arrow | Next Folder | `file.next` |  |
| Ctrl+Right Arrow | Next Folder | `file.next` |  |
| Button5 Mouse | Next Folder | `file.next` |  |
| Ctrl+] | Next Folder | `file.next` |  |
| Ctrl+1 | Context Set Enum | `wm.context_set_enum` | data_path='space_data.params.display_type', value='LIST_VERTICAL' |
| Ctrl+2 | Context Set Enum | `wm.context_set_enum` | data_path='space_data.params.display_type', value='LIST_HORIZONTAL' |
| Ctrl+3 | Context Set Enum | `wm.context_set_enum` | data_path='space_data.params.display_type', value='THUMBNAIL' |
| Ctrl+R | Refresh File List | `file.refresh` |  |
| Ctrl+R | Refresh Asset Library | `asset.library_refresh` |  |
| Shift+R | Reload Remote Asset Library Listing | `asset.library_reload_listing` |  |
| Backspace | Previous Folder | `file.previous` |  |
| Shift+Backspace | Next Folder | `file.next` |  |
| H | Context Toggle | `wm.context_toggle` | data_path='space_data.params.show_hidden' |
| Ctrl+H | Context Toggle | `wm.context_toggle` | data_path='space_data.params.show_hidden' |
| Ctrl+Shift+. | Context Toggle | `wm.context_toggle` | data_path='space_data.params.show_hidden' |
| Ctrl+Shift+N | Create New Directory | `file.directory_new` | confirm=False |
| F2 | Rename File or Directory | `file.rename` |  |
| Delete | Delete Selected Files | `file.delete` |  |
| Any modifier+Timer 1 any | Smooth Scroll | `file.smoothscroll` |  |
| T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| Ctrl+B | Add Bookmark | `file.bookmark_add` |  |
| Numpad + (repeat) | Increment Number in Filename | `file.filenum` | increment=1 |
| Shift+Numpad + (repeat) | Increment Number in Filename | `file.filenum` | increment=10 |
| Ctrl+Numpad + (repeat) | Increment Number in Filename | `file.filenum` | increment=100 |
| Numpad - (repeat) | Increment Number in Filename | `file.filenum` | increment=-1 |
| Shift+Numpad - (repeat) | Increment Number in Filename | `file.filenum` | increment=-10 |
| Ctrl+Numpad - (repeat) | Increment Number in Filename | `file.filenum` | increment=-100 |
| Right Mouse | Select | `file.select` | open=False, only_activate_if_selected=True, pass_through=True |
| Right Mouse | Call Menu | `wm.call_menu` | name='FILEBROWSER_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='FILEBROWSER_MT_context_menu' |

## File Browser Main

Space `FILE_BROWSER`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse double click | Execute File | `file.mouse_execute` |  |
| Ctrl+R | Refresh File List | `file.refresh` |  |
| Ctrl+R | Refresh Asset Library | `asset.library_refresh` |  |
| Shift+R | Reload Remote Asset Library Listing | `asset.library_reload_listing` |  |
| Left Mouse | Select | `file.select` | open=False, deselect_all=True |
| Ctrl+Left Mouse click | Select | `file.select` | extend=True, open=False |
| Shift+Left Mouse click | Select | `file.select` | extend=True, fill=True, open=False |
| Shift+Right Mouse click | Select | `file.select` | extend=True, open=False |
| Alt+Right Mouse click | Select | `file.select` | extend=True, fill=True, open=False |
| Up Arrow | Walk Select/Deselect File | `file.select_walk` | direction='UP' |
| Shift+Up Arrow | Walk Select/Deselect File | `file.select_walk` | direction='UP', extend=True |
| Ctrl+Shift+Up Arrow | Walk Select/Deselect File | `file.select_walk` | direction='UP', extend=True, fill=True |
| Down Arrow | Walk Select/Deselect File | `file.select_walk` | direction='DOWN' |
| Shift+Down Arrow | Walk Select/Deselect File | `file.select_walk` | direction='DOWN', extend=True |
| Ctrl+Shift+Down Arrow | Walk Select/Deselect File | `file.select_walk` | direction='DOWN', extend=True, fill=True |
| Left Arrow | Walk Select/Deselect File | `file.select_walk` | direction='LEFT' |
| Shift+Left Arrow | Walk Select/Deselect File | `file.select_walk` | direction='LEFT', extend=True |
| Ctrl+Shift+Left Arrow | Walk Select/Deselect File | `file.select_walk` | direction='LEFT', extend=True, fill=True |
| Right Arrow | Walk Select/Deselect File | `file.select_walk` | direction='RIGHT' |
| Shift+Right Arrow | Walk Select/Deselect File | `file.select_walk` | direction='RIGHT', extend=True |
| Ctrl+Shift+Right Arrow | Walk Select/Deselect File | `file.select_walk` | direction='RIGHT', extend=True, fill=True |
| Button4 Mouse click | Previous Folder | `file.previous` |  |
| Button5 Mouse click | Next Folder | `file.next` |  |
| Ctrl+A | (De)select All Files | `file.select_all` |  |
| Q | Box Select | `file.select_box` |  |
| Left Mouse drag | Box Select | `file.select_box` |  |
| Shift+Left Mouse drag | Box Select | `file.select_box` | mode='ADD' |
| Any modifier+Mouse Move any | Highlight File | `file.highlight` |  |
| Any modifier+Left Mouse | Sort from Column | `file.sort_column_ui_context` |  |
| F | Frame Selected | `file.view_selected` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='ASSETBROWSER_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='ASSETBROWSER_MT_context_menu' |

## File Browser Buttons

Space `FILE_BROWSER`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Numpad + (repeat) | Increment Number in Filename | `file.filenum` | increment=1 |
| Shift+Numpad + (repeat) | Increment Number in Filename | `file.filenum` | increment=10 |
| Ctrl+Numpad + (repeat) | Increment Number in Filename | `file.filenum` | increment=100 |
| Numpad - (repeat) | Increment Number in Filename | `file.filenum` | increment=-1 |
| Shift+Numpad - (repeat) | Increment Number in Filename | `file.filenum` | increment=-10 |
| Ctrl+Numpad - (repeat) | Increment Number in Filename | `file.filenum` | increment=-100 |

## Dopesheet Generic

Space `DOPESHEET_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Tab | Search Menu | `wm.search_menu` |  |
| Ctrl+[ | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_channels' |
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |

## Dopesheet

Space `DOPESHEET_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Arrow | Frame Offset | `screen.frame_offset` | delta=-1 |
| Right Arrow | Frame Offset | `screen.frame_offset` | delta=1 |
| Ctrl+Right Arrow | Jump to Endpoint | `screen.frame_jump` | end=True |
| Ctrl+Left Arrow | Jump to Endpoint | `screen.frame_jump` | end=False |
| Left Mouse | Select Keyframes | `action.clickselect` | extend=False, deselect_all=True, column=False, channel=False |
| Alt+Left Mouse | Select Keyframes | `action.clickselect` | extend=False, column=True, channel=False |
| Shift+Left Mouse | Select Keyframes | `action.clickselect` | extend=True, column=False, channel=False |
| Shift+Alt+Left Mouse | Select Keyframes | `action.clickselect` | extend=True, column=True, channel=False |
| Ctrl+Alt+Left Mouse | Select Keyframes | `action.clickselect` | extend=False, column=False, channel=True |
| Ctrl+Shift+Alt+Left Mouse | Select Keyframes | `action.clickselect` | extend=True, column=False, channel=True |
| Ctrl+Shift+Left Mouse | Select Left/Right | `action.select_leftright` | mode='CHECK', extend=True |
| [ | Select Left/Right | `action.select_leftright` | mode='LEFT', extend=False |
| ] | Select Left/Right | `action.select_leftright` | mode='RIGHT', extend=False |
| Ctrl+A | Select All | `action.select_all` | action='SELECT' |
| Ctrl+Shift+A | Select All | `action.select_all` | action='DESELECT' |
| Ctrl+I | Select All | `action.select_all` | action='INVERT' |
| Q | Box Select | `action.select_box` | axis_range=False |
| Alt+Q | Box Select | `action.select_box` | axis_range=True |
| Left Mouse drag | Box Select | `action.select_box` | tweak=True, axis_range=False, wait_for_input=False, mode='SET' |
| Shift+Left Mouse drag | Box Select | `action.select_box` | tweak=True, axis_range=False, wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `action.select_box` | tweak=True, axis_range=False, wait_for_input=False, mode='SUB' |
| K | Select All | `action.select_column` | mode='KEYS' |
| Ctrl+K | Select All | `action.select_column` | mode='CFRA' |
| Shift+K | Select All | `action.select_column` | mode='MARKERS_COLUMN' |
| Alt+K | Select All | `action.select_column` | mode='MARKERS_BETWEEN' |
| Ctrl+Up Arrow (repeat) | Select More | `action.select_more` |  |
| Ctrl+Down Arrow (repeat) | Select Less | `action.select_less` |  |
| Ctrl+L | Select Linked | `action.select_linked` |  |
| Ctrl+G | Jump to Keyframes | `action.frame_jump` |  |
| X | Context Enum Menu | `wm.context_menu_enum` | data_path='space_data.auto_snap' |
| Shift+X | Call Pie Menu | `wm.call_menu_pie` | name='DOPESHEET_MT_snap_pie' |
| Right Mouse | Call Menu | `wm.call_menu` | name='DOPESHEET_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='DOPESHEET_MT_context_menu' |
| Backspace | Call Menu | `wm.call_menu` | name='DOPESHEET_MT_delete' |
| Delete | Delete Keyframes | `action.delete` | confirm=False |
| Ctrl+D | Duplicate | `action.duplicate_move` |  |
| S | Insert Keyframes | `action.keyframe_insert` |  |
| Ctrl+C | Copy Keyframes | `action.copy` |  |
| Ctrl+V | Paste Keyframes | `action.paste` |  |
| Ctrl+Shift+V | Paste Keyframes | `action.paste` | flipped=True |
| Ctrl+Alt+P | Set Preview Range to Selected | `action.previewrange_set` |  |
| A | Frame All | `action.view_all` |  |
| NDOF Fit | Frame All | `action.view_all` |  |
| F | Frame Selected | `action.view_selected` |  |
| Numpad 0 | Go to Current Frame | `action.view_frame` |  |
| Left Mouse double click | Toggle Channel Editability | `anim.channels_editable_toggle` |  |
| Ctrl+F | Filter Channels | `anim.channels_select_filter` |  |
| W | Transform | `transform.transform` | mode='TIME_TRANSLATE' |
| Left Mouse drag | Transform | `transform.transform` | mode='TIME_TRANSLATE' |
| Middle Mouse drag | Transform | `transform.transform` | mode='TIME_TRANSLATE' |
| E | Transform | `transform.transform` | mode='TIME_EXTEND' |
| R | Transform | `transform.transform` | mode='TIME_SCALE' |
| Shift+T | Transform | `transform.transform` | mode='TIME_SLIDE' |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_action' |
| M | Add Time Marker | `marker.add` |  |
| Ctrl+Left Arrow | Set Start Frame | `anim.start_frame_set` |  |
| Ctrl+Right Arrow | Set End Frame | `anim.end_frame_set` |  |

## NLA Generic

Space `NLA_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Ctrl+[ | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_channels' |
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Tab | Search Menu | `wm.search_menu` |  |
| Left Arrow | Frame Offset | `screen.frame_offset` | delta=-1 |
| Right Arrow | Frame Offset | `screen.frame_offset` | delta=1 |
| Ctrl+Right Arrow | Jump to Endpoint | `screen.frame_jump` | end=True |
| Ctrl+Left Arrow | Jump to Endpoint | `screen.frame_jump` | end=False |
| Left Mouse double click | Enter Tweak Mode | `nla.tweakmode_enter` |  |
| Esc | Exit Tweak Mode | `nla.tweakmode_exit` |  |
| Ctrl+F | Filter Channels | `anim.channels_select_filter` |  |

## NLA Tracks

Space `NLA_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mouse Click on NLA Tracks | `nla.channels_click` | extend=False |
| Shift+Left Mouse | Mouse Click on NLA Tracks | `nla.channels_click` | extend=True |
| Backspace | Delete Tracks | `nla.tracks_delete` |  |
| Delete | Delete Tracks | `nla.tracks_delete` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='NLA_MT_channel_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='NLA_MT_channel_context_menu' |

## NLA Editor

Space `NLA_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `nla.click_select` | extend=False, deselect_all=True |
| Shift+Left Mouse | Select | `nla.click_select` | extend=True |
| Ctrl+Shift+Left Mouse | Select Left/Right | `nla.select_leftright` | mode='CHECK', extend=True |
| [ | Select Left/Right | `nla.select_leftright` | mode='LEFT', extend=False |
| ] | Select Left/Right | `nla.select_leftright` | mode='RIGHT', extend=False |
| Ctrl+A | (De)select All | `nla.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `nla.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `nla.select_all` | action='INVERT' |
| Q | Box Select | `nla.select_box` | axis_range=False |
| Alt+Q | Box Select | `nla.select_box` | axis_range=True |
| Left Mouse drag | Box Select | `nla.select_box` | tweak=True, mode='SET' |
| Shift+Left Mouse drag | Box Select | `nla.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `nla.select_box` | tweak=True, mode='SUB' |
| A | Frame All | `nla.view_all` |  |
| NDOF Fit | Frame All | `nla.view_all` |  |
| F | Frame Selected | `nla.view_selected` |  |
| Numpad 0 | Go to Current Frame | `nla.view_frame` |  |
| Ctrl+G | Add Meta-Strips | `nla.meta_add` |  |
| Ctrl+Alt+G | Remove Meta-Strips | `nla.meta_remove` |  |
| Ctrl+D | Duplicate Strips | `nla.duplicate` | linked=False |
| Ctrl+Alt+D | Duplicate Strips | `nla.duplicate` | linked=True |
| U | Make Single User | `nla.make_single_user` |  |
| Backspace | Delete Strips | `nla.delete` |  |
| Delete | Delete Strips | `nla.delete` |  |
| M | Toggle Muting | `nla.mute_toggle` |  |
| Page Up | Move Strips Up | `nla.move_up` |  |
| Page Down | Move Strips Down | `nla.move_down` |  |
| W | Transform | `transform.transform` | mode='TRANSLATION' |
| Left Mouse drag | Transform | `transform.transform` | mode='TRANSLATION' |
| Middle Mouse drag | Transform | `transform.transform` | mode='TRANSLATION' |
| E | Transform | `transform.transform` | mode='TIME_EXTEND' |
| R | Transform | `transform.transform` | mode='TIME_SCALE' |
| Right Mouse | Call Menu | `wm.call_menu` | name='NLA_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='NLA_MT_context_menu' |
| Shift+X | Call Pie Menu | `wm.call_menu_pie` | name='NLA_MT_snap_pie' |
| M | Add Time Marker | `marker.add` |  |

## Text Generic

Space `TEXT_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+F | Find | `text.start_find` |  |
| Ctrl+J | Jump | `text.jump` |  |
| Ctrl+G | Find Next | `text.find` |  |
| Ctrl+H | Replace | `text.replace` |  |
| Ctrl+I | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |

## Text

Space `TEXT_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+Left Arrow | Move Cursor | `text.move` | type='LINE_BEGIN' |
| Ctrl+Right Arrow | Move Cursor | `text.move` | type='LINE_END' |
| Ctrl+Up Arrow | Move Cursor | `text.move` | type='FILE_TOP' |
| Ctrl+Down Arrow | Move Cursor | `text.move` | type='FILE_BOTTOM' |
| Alt+Left Arrow | Move Cursor | `text.move` | type='PREVIOUS_WORD' |
| Alt+Right Arrow | Move Cursor | `text.move` | type='NEXT_WORD' |
| Ctrl+Wheel Up | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=False |
| Ctrl+Wheel Down | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=True |
| Ctrl+Numpad + (repeat) | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=False |
| Ctrl+Numpad - (repeat) | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=True |
| Ctrl+N | New Text | `text.new` |  |
| Alt+O | Open Text | `text.open` |  |
| Alt+R | Reload | `text.reload` |  |
| Alt+S | Save | `text.save` |  |
| Ctrl+Shift+Alt+S | Save As | `text.save_as` |  |
| Alt+P | Run Script | `text.run_script` |  |
| Ctrl+X | Cut | `text.cut` |  |
| Ctrl+C | Copy | `text.copy` |  |
| Ctrl+V (repeat) | Paste | `text.paste` |  |
| Shift+Delete | Cut | `text.cut` |  |
| Ctrl+Insert | Copy | `text.copy` |  |
| Shift+Insert (repeat) | Paste | `text.paste` |  |
| Ctrl+D (repeat) | Duplicate Line | `text.duplicate_line` |  |
| Ctrl+A | Select All | `text.select_all` |  |
| Ctrl+Shift+A | Select Line | `text.select_line` |  |
| Left Mouse double click | Select Word | `text.select_word` |  |
| Ctrl+Shift+Up Arrow (repeat) | Move Lines | `text.move_lines` | direction='UP' |
| Ctrl+Shift+Down Arrow (repeat) | Move Lines | `text.move_lines` | direction='DOWN' |
| Tab (repeat) | Indent or Autocomplete | `text.indent_or_autocomplete` |  |
| Shift+Tab (repeat) | Unindent | `text.unindent` |  |
| Ctrl+Shift+D |  | `text.uncomment` |  |
| Home | Move Cursor | `text.move` | type='LINE_BEGIN' |
| End | Move Cursor | `text.move` | type='LINE_END' |
| Ctrl+E | Move Cursor | `text.move` | type='LINE_END' |
| Ctrl+Shift+E | Move Cursor | `text.move` | type='LINE_END' |
| Left Arrow (repeat) | Move Cursor | `text.move` | type='PREVIOUS_CHARACTER' |
| Right Arrow (repeat) | Move Cursor | `text.move` | type='NEXT_CHARACTER' |
| Ctrl+Left Arrow (repeat) | Move Cursor | `text.move` | type='PREVIOUS_WORD' |
| Ctrl+Right Arrow (repeat) | Move Cursor | `text.move` | type='NEXT_WORD' |
| Up Arrow (repeat) | Move Cursor | `text.move` | type='PREVIOUS_LINE' |
| Down Arrow (repeat) | Move Cursor | `text.move` | type='NEXT_LINE' |
| Page Up (repeat) | Move Cursor | `text.move` | type='PREVIOUS_PAGE' |
| Page Down (repeat) | Move Cursor | `text.move` | type='NEXT_PAGE' |
| Ctrl+Home | Move Cursor | `text.move` | type='FILE_TOP' |
| Ctrl+End | Move Cursor | `text.move` | type='FILE_BOTTOM' |
| Shift+Home | Move Select | `text.move_select` | type='LINE_BEGIN' |
| Shift+End | Move Select | `text.move_select` | type='LINE_END' |
| Shift+Left Arrow (repeat) | Move Select | `text.move_select` | type='PREVIOUS_CHARACTER' |
| Shift+Right Arrow (repeat) | Move Select | `text.move_select` | type='NEXT_CHARACTER' |
| Ctrl+Shift+Left Arrow (repeat) | Move Select | `text.move_select` | type='PREVIOUS_WORD' |
| Ctrl+Shift+Right Arrow (repeat) | Move Select | `text.move_select` | type='NEXT_WORD' |
| Shift+Up Arrow (repeat) | Move Select | `text.move_select` | type='PREVIOUS_LINE' |
| Shift+Down Arrow (repeat) | Move Select | `text.move_select` | type='NEXT_LINE' |
| Shift+Page Up (repeat) | Move Select | `text.move_select` | type='PREVIOUS_PAGE' |
| Shift+Page Down (repeat) | Move Select | `text.move_select` | type='NEXT_PAGE' |
| Ctrl+Shift+Home | Move Select | `text.move_select` | type='FILE_TOP' |
| Ctrl+Shift+End | Move Select | `text.move_select` | type='FILE_BOTTOM' |
| Delete (repeat) | Delete | `text.delete` | type='NEXT_CHARACTER' |
| Backspace (repeat) | Delete | `text.delete` | type='PREVIOUS_CHARACTER' |
| Shift+Backspace (repeat) | Delete | `text.delete` | type='PREVIOUS_CHARACTER' |
| Ctrl+Delete (repeat) | Delete | `text.delete` | type='NEXT_WORD' |
| Ctrl+Backspace | Delete | `text.delete` | type='PREVIOUS_WORD' |
| Insert | Toggle Overwrite | `text.overwrite_toggle` |  |
| Left Mouse | Scrollbar | `text.scroll_bar` |  |
| Middle Mouse | Scrollbar | `text.scroll_bar` |  |
| Middle Mouse | Scroll | `text.scroll` |  |
| Mouse/Trackpad Pan any | Scroll | `text.scroll` |  |
| Left Mouse drag | Set Selection | `text.selection_set` |  |
| Left Mouse | Set Cursor | `text.cursor_set` |  |
| Shift+Left Mouse | Set Selection | `text.selection_set` |  |
| Wheel Up | Scroll | `text.scroll` | lines=-1 |
| Wheel Down | Scroll | `text.scroll` | lines=1 |
| Return (repeat) | Line Break | `text.line_break` |  |
| Numpad Enter (repeat) | Line Break | `text.line_break` |  |
| Any modifier+Right Mouse | Call Menu | `wm.call_menu` | name='TEXT_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='TEXT_MT_context_menu' |
| Any modifier+Text Input any | Line Number | `text.line_number` |  |
| Any modifier+Text Input any (repeat) | Insert | `text.insert` |  |

## Video Sequence Editor

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Ctrl+[ | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_channels' |
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |

## Sequencer

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Tab | Search Menu | `wm.search_menu` |  |
| Left Arrow | Frame Offset | `screen.frame_offset` | delta=-1 |
| Right Arrow | Frame Offset | `screen.frame_offset` | delta=1 |
| Ctrl+Right Arrow | Jump to Endpoint | `screen.frame_jump` | end=True |
| Ctrl+Left Arrow | Jump to Endpoint | `screen.frame_jump` | end=False |
| Left Mouse click | Select | `sequencer.select` |  |
| Shift+Left Mouse | Select | `sequencer.select` | extend=True |
| Alt+Left Mouse | Select | `sequencer.select` | linked_handle=True |
| Shift+Alt+Left Mouse | Select | `sequencer.select` | extend=True, linked_handle=True |
| Ctrl+Left Mouse | Select | `sequencer.select` | side_of_frame=True, linked_time=True |
| Ctrl+Shift+Left Mouse | Select | `sequencer.select` | extend=True, side_of_frame=True, linked_time=True |
| Up Arrow (repeat) | Select More | `sequencer.select_more` |  |
| Down Arrow (repeat) | Select Less | `sequencer.select_less` |  |
| Ctrl+L | Select Pick Linked | `sequencer.select_linked_pick` | extend=False |
| Shift+] | Select Pick Linked | `sequencer.select_linked_pick` | extend=True |
| Ctrl+L | Select Linked | `sequencer.select_linked` |  |
| Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='SET' |
| Shift+Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='SUB' |
| Shift+G | Select Grouped | `sequencer.select_grouped` |  |
| Ctrl+A | (De)select All | `sequencer.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `sequencer.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `sequencer.select_all` | action='INVERT' |
| Ctrl+B | Split Strips | `sequencer.split` | type='SOFT', only_selected=True |
| M | Mute Strips | `sequencer.mute` | unselected=False |
| Shift+M | Mute Strips | `sequencer.mute` | unselected=True |
| Alt+M | Unmute Strips | `sequencer.unmute` | unselected=False |
| Shift+Alt+M | Unmute Strips | `sequencer.unmute` | unselected=True |
| Shift+L | Lock Strips | `sequencer.lock` |  |
| Shift+Alt+L | Unlock Strips | `sequencer.unlock` |  |
| Ctrl+Alt+L | Connect Strips | `sequencer.connect` | toggle=True |
| R | Reassign Inputs | `sequencer.reassign_inputs` |  |
| Ctrl+R | Reload Strips | `sequencer.reload` |  |
| Shift+Alt+R | Reload Strips | `sequencer.reload` | adjust_length=True |
| Alt+O | Clear Strip Offset | `sequencer.offset_clear` |  |
| Ctrl+D | Duplicate Strips | `sequencer.duplicate_move` |  |
| Ctrl+Alt+D | Duplicate Strips | `sequencer.duplicate_move_linked` |  |
| Backspace | Delete Retiming Keys | `sequencer.retiming_key_delete` |  |
| Delete | Delete Retiming Keys | `sequencer.retiming_key_delete` |  |
| Backspace | Delete Strips | `sequencer.delete` |  |
| Delete | Delete Strips | `sequencer.delete` |  |
| Shift+Delete | Ripple Delete Strips | `sequencer.ripple_delete` |  |
| Ctrl+C | Copy | `sequencer.copy` |  |
| Ctrl+V | Paste | `sequencer.paste` |  |
| Y | Separate Images | `sequencer.images_separate` |  |
| Left Mouse double click | Toggle Meta Strip | `sequencer.meta_toggle` |  |
| Ctrl+G | Make Meta Strip | `sequencer.meta_make` |  |
| Ctrl+Alt+G | UnMeta Strip | `sequencer.meta_separate` |  |
| A | Frame All | `sequencer.view_all` |  |
| NDOF Fit | Frame All | `sequencer.view_all` |  |
| F | Frame Selected | `sequencer.view_selected` |  |
| Numpad 0 | Go to Current Frame | `sequencer.view_frame` |  |
| Page Up (repeat) | Jump to Strip | `sequencer.strip_jump` | next=False, center=False |
| Page Down (repeat) | Jump to Strip | `sequencer.strip_jump` | next=True, center=False |
| Alt+Page Up (repeat) | Jump to Strip | `sequencer.strip_jump` | next=False, center=True |
| Alt+Page Down (repeat) | Jump to Strip | `sequencer.strip_jump` | next=True, center=True |
| Alt+Left Arrow (repeat) | Swap Strip | `sequencer.swap` | side='LEFT' |
| Alt+Right Arrow (repeat) | Swap Strip | `sequencer.swap` | side='RIGHT' |
| Backspace | Remove Gaps | `sequencer.gap_remove` | all=False |
| Shift+Backspace | Remove Gaps | `sequencer.gap_remove` | all=True |
| Shift+= | Insert Gaps | `sequencer.gap_insert` |  |
| X | Snap Strips to the Current Frame | `sequencer.snap` | keep_offset=True |
| Alt+S | Swap Inputs | `sequencer.swap_inputs` |  |
| 1 | Split Multicam | `sequencer.split_multicam` | camera=1 |
| 2 | Split Multicam | `sequencer.split_multicam` | camera=2 |
| 3 | Split Multicam | `sequencer.split_multicam` | camera=3 |
| 4 | Split Multicam | `sequencer.split_multicam` | camera=4 |
| 5 | Split Multicam | `sequencer.split_multicam` | camera=5 |
| 6 | Split Multicam | `sequencer.split_multicam` | camera=6 |
| 7 | Split Multicam | `sequencer.split_multicam` | camera=7 |
| 8 | Split Multicam | `sequencer.split_multicam` | camera=8 |
| 9 | Split Multicam | `sequencer.split_multicam` | camera=9 |
| 0 | Split Multicam | `sequencer.split_multicam` | camera=10 |
| R | Slip Strips | `sequencer.slip` |  |
| O | Context Set | `wm.context_set_int` | data_path='sequencer_scene.sequence_editor.overlay_frame', value=0 |
| W | Sequence Slide | `transform.seq_slide` | view2d_edge_pan=True |
| Left Mouse drag | Sequence Slide | `transform.seq_slide` | view2d_edge_pan=True, use_restore_handle_selection=True |
| Middle Mouse drag | Sequence Slide | `transform.seq_slide` | view2d_edge_pan=True, use_restore_handle_selection=True |
| E | Transform | `transform.transform` | mode='TIME_EXTEND' |
| M | Add Time Marker | `marker.add` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_context_menu' |
| I | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_retiming' |
| Shift+R | Set Speed | `sequencer.retiming_segment_speed_set` |  |
| Ctrl+Shift+R | Retime Strips | `sequencer.retiming_show` |  |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| B | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.blade', cycle=True |
| S | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.slip', cycle=True |

## Preview

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Tab | Search Menu | `wm.search_menu` |  |
| A | Frame All | `sequencer.view_all_preview` |  |
| NDOF Fit | Frame All | `sequencer.view_all_preview` |  |
| F | Frame Selected | `sequencer.view_selected` |  |
| O | Border Offset View | `sequencer.view_ghost_border` |  |
| Numpad 1 | Sequencer View Zoom Ratio | `sequencer.view_zoom_ratio` | ratio=1.0 |
| Left Mouse | Sample Color | `sequencer.sample` |  |

## Sequencer Channels

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+Left Mouse | Rename Channel | `sequencer.rename_channel` |  |
| Left Mouse double click | Rename Channel | `sequencer.rename_channel` |  |

## Console

Space `CONSOLE`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+Left Arrow (repeat) | Move Cursor | `console.move` | type='PREVIOUS_WORD' |
| Ctrl+Shift+Left Arrow (repeat) | Move Cursor | `console.move` | type='PREVIOUS_WORD', select=True |
| Ctrl+Right Arrow (repeat) | Move Cursor | `console.move` | type='NEXT_WORD' |
| Ctrl+Shift+Right Arrow (repeat) | Move Cursor | `console.move` | type='NEXT_WORD', select=True |
| Home | Move Cursor | `console.move` | type='LINE_BEGIN' |
| Shift+Home | Move Cursor | `console.move` | type='LINE_BEGIN', select=True |
| End | Move Cursor | `console.move` | type='LINE_END' |
| Shift+End | Move Cursor | `console.move` | type='LINE_END', select=True |
| Ctrl+Wheel Up | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=False |
| Ctrl+Wheel Down | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=True |
| Ctrl+Numpad + (repeat) | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=False |
| Ctrl+Numpad - (repeat) | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=True |
| Left Arrow (repeat) | Move Cursor | `console.move` | type='PREVIOUS_CHARACTER' |
| Shift+Left Arrow (repeat) | Move Cursor | `console.move` | type='PREVIOUS_CHARACTER', select=True |
| Right Arrow (repeat) | Move Cursor | `console.move` | type='NEXT_CHARACTER' |
| Shift+Right Arrow (repeat) | Move Cursor | `console.move` | type='NEXT_CHARACTER', select=True |
| Up Arrow (repeat) | History Cycle | `console.history_cycle` | reverse=True |
| Down Arrow (repeat) | History Cycle | `console.history_cycle` | reverse=False |
| Delete (repeat) | Delete | `console.delete` | type='NEXT_CHARACTER' |
| Backspace (repeat) | Delete | `console.delete` | type='PREVIOUS_CHARACTER' |
| Shift+Backspace (repeat) | Delete | `console.delete` | type='PREVIOUS_CHARACTER' |
| Ctrl+Delete (repeat) | Delete | `console.delete` | type='NEXT_WORD' |
| Ctrl+Backspace (repeat) | Delete | `console.delete` | type='PREVIOUS_WORD' |
| Shift+Return | Clear Line | `console.clear_line` |  |
| Shift+Numpad Enter | Clear Line | `console.clear_line` |  |
| Return | Console Execute | `console.execute` | interactive=True |
| Numpad Enter | Console Execute | `console.execute` | interactive=True |
| Ctrl+Shift+C | Copy to Clipboard (as Script) | `console.copy_as_script` |  |
| Ctrl+C | Copy to Clipboard | `console.copy` |  |
| Ctrl+X | Copy to Clipboard | `console.copy` | delete=True |
| Ctrl+V (repeat) | Paste from Clipboard | `console.paste` |  |
| Left Mouse | Set Selection | `console.select_set` |  |
| Ctrl+A | Select All | `console.select_all` |  |
| Left Mouse double click | Select Word | `console.select_word` |  |
| Ctrl+Tab (repeat) | Insert | `console.insert` | text='\t' |
| Tab (repeat) | Indent or Autocomplete | `console.indent_or_autocomplete` |  |
| Shift+Tab (repeat) | Unindent | `console.unindent` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='CONSOLE_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='CONSOLE_MT_context_menu' |
| Any modifier+Text Input any (repeat) | Insert | `console.insert` |  |

## Clip

Space `CLIP_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Tab | Search Menu | `wm.search_menu` |  |
| Alt+O | Open Clip | `clip.open` |  |
| Alt+Left Arrow (repeat) | Track Markers | `clip.track_markers` | backwards=True, sequence=False |
| Alt+Right Arrow (repeat) | Track Markers | `clip.track_markers` | backwards=False, sequence=False |
| Ctrl+T | Track Markers | `clip.track_markers` | backwards=False, sequence=True |
| Ctrl+Shift+T | Track Markers | `clip.track_markers` | backwards=True, sequence=True |
| Tab | Context Toggle Values | `wm.context_toggle_enum` | data_path='space_data.mode', value_1='TRACKING', value_2='MASK' |
| Shift+S | Solve Camera | `clip.solve_camera` |  |
| P | Prefetch Frames | `clip.prefetch` |  |

## Clip Editor

Space `CLIP_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+[ | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Tab | Search Menu | `wm.search_menu` |  |
| Middle Mouse | Pan View | `clip.view_pan` |  |
| Shift+Middle Mouse | Pan View | `clip.view_pan` |  |
| Mouse/Trackpad Pan any | Pan View | `clip.view_pan` |  |
| Ctrl+Middle Mouse | View Zoom | `clip.view_zoom` |  |
| Mouse/Trackpad Zoom any | View Zoom | `clip.view_zoom` |  |
| Ctrl+Mouse/Trackpad Pan any | View Zoom | `clip.view_zoom` |  |
| Wheel In | Zoom In | `clip.view_zoom_in` |  |
| Wheel Out | Zoom Out | `clip.view_zoom_out` |  |
| Alt+Wheel In | Zoom In | `clip.view_zoom_in` |  |
| Alt+Wheel Out | Zoom Out | `clip.view_zoom_out` |  |
| Numpad + (repeat) | Zoom In | `clip.view_zoom_in` |  |
| Numpad - (repeat) | Zoom Out | `clip.view_zoom_out` |  |
| Ctrl+Numpad 8 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=8.0 |
| Ctrl+Numpad 4 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=4.0 |
| Ctrl+Numpad 2 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=2.0 |
| Shift+Numpad 8 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=8.0 |
| Shift+Numpad 4 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=4.0 |
| Shift+Numpad 2 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=2.0 |
| Numpad 1 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=1.0 |
| Numpad 2 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=0.5 |
| Numpad 4 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=0.25 |
| Numpad 8 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=0.125 |
| A | Frame All | `clip.view_all` |  |
| F | Frame Selected | `clip.view_selected` |  |
| NDOF Fit | Frame All | `clip.view_all` |  |
| NDOF Motion any | NDOF Pan/Zoom | `clip.view_ndof` |  |
| Ctrl+Shift+Left Arrow (repeat) | Jump to Frame | `clip.frame_jump` | position='PATHSTART' |
| Ctrl+Shift+Right Arrow (repeat) | Jump to Frame | `clip.frame_jump` | position='PATHEND' |
| Shift+Alt+Left Arrow (repeat) | Jump to Frame | `clip.frame_jump` | position='FAILEDPREV' |
| Shift+Alt+Right Arrow (repeat) | Jump to Frame | `clip.frame_jump` | position='PATHSTART' |
| Left Mouse | Change Frame | `clip.change_frame` |  |
| Left Mouse | Select | `clip.select` | extend=False, deselect_all=True |
| Shift+Left Mouse | Select | `clip.select` | extend=True |
| Q | Box Select | `clip.select_box` |  |
| Ctrl+A | (De)select All | `clip.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `clip.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `clip.select_all` | action='INVERT' |
| Shift+G | Call Menu | `wm.call_menu` | name='CLIP_MT_select_grouped' |
| Ctrl+Left Mouse | Add Marker and Slide | `clip.add_marker_slide` |  |
| Shift+Backspace | Delete Marker | `clip.delete_marker` |  |
| Shift+Delete | Delete Marker | `clip.delete_marker` |  |
| Left Mouse | Slide Marker | `clip.slide_marker` |  |
| Shift+D | Disable Markers | `clip.disable_markers` | action='TOGGLE' |
| Backspace | Delete Track | `clip.delete_track` |  |
| Delete | Delete Track | `clip.delete_track` |  |
| Ctrl+L | Lock Tracks | `clip.lock_tracks` | action='LOCK' |
| Alt+L | Lock Tracks | `clip.lock_tracks` | action='UNLOCK' |
| Ctrl+H | Hide Tracks | `clip.hide_tracks` | unselected=False |
| Shift+H | Hide Tracks | `clip.hide_tracks` | unselected=True |
| Alt+H | Hide Tracks Clear | `clip.hide_tracks_clear` |  |
| Left Mouse | Slide Plane Marker | `clip.slide_plane_marker` |  |
| S | Insert Keyframe | `clip.keyframe_insert` |  |
| Alt+S | Delete Keyframe | `clip.keyframe_delete` |  |
| Ctrl+J | Join Tracks | `clip.join_tracks` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='CLIP_MT_tracking_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='CLIP_MT_tracking_context_menu' |
| L | Context Toggle | `wm.context_toggle` | data_path='space_data.lock_selection' |
| Alt+D | Context Toggle | `wm.context_toggle` | data_path='space_data.show_disabled' |
| Alt+S | Context Toggle | `wm.context_toggle` | data_path='space_data.show_marker_search' |
| M | Context Toggle | `wm.context_toggle` | data_path='space_data.use_mute_footage' |
| W | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| R | Resize | `transform.resize` |  |
| E | Rotate | `transform.rotate` |  |
| Alt+T | Clear Track Path | `clip.clear_track_path` | action='REMAINED', clear_active=False |
| Shift+T | Clear Track Path | `clip.clear_track_path` | action='UPTO', clear_active=False |
| Shift+Alt+T | Clear Track Path | `clip.clear_track_path` | action='ALL', clear_active=False |
| . | Call Pie Menu | `wm.call_menu_pie` | name='CLIP_MT_pivot_pie' |
| Ctrl+C | Copy Tracks | `clip.copy_tracks` |  |
| Ctrl+V | Paste Tracks | `clip.paste_tracks` |  |

## Clip Graph Editor

Space `CLIP_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Return | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Tab | Search Menu | `wm.search_menu` |  |
| Left Mouse | Select | `clip.graph_select` | extend=False |
| Shift+Left Mouse | Select | `clip.graph_select` | extend=True |
| Q | Box Select | `clip.graph_select_box` |  |
| Ctrl+A |  | `clip.graph_select_all` |  |
| Backspace | Delete Curve | `clip.graph_delete_curve` |  |
| Delete | Delete Curve | `clip.graph_delete_curve` |  |
| Shift+Backspace | Delete Knot | `clip.graph_delete_knot` |  |
| Shift+Delete | Delete Knot | `clip.graph_delete_knot` |  |
| A | Frame All | `clip.graph_view_all` |  |
| NDOF Fit | Frame All | `clip.graph_view_all` |  |
| Numpad 0 | Center Current Frame | `clip.graph_center_current_frame` |  |
| L | Context Toggle | `wm.context_toggle` | data_path='space_data.lock_time_cursor' |
| Alt+T | Clear Track Path | `clip.clear_track_path` | action='REMAINED', clear_active=True |
| Shift+T | Clear Track Path | `clip.clear_track_path` | action='UPTO', clear_active=True |
| Shift+Alt+T | Clear Track Path | `clip.clear_track_path` | action='ALL', clear_active=True |
| Shift+D | Disable Markers | `clip.graph_disable_markers` | action='TOGGLE' |
| W | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| R | Resize | `transform.resize` |  |
| E | Rotate | `transform.rotate` |  |

## Clip Dopesheet Editor

Space `CLIP_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Tab | Search Menu | `wm.search_menu` |  |
| Left Mouse | Select Channel | `clip.dopesheet_select_channel` | extend=True |
| Home | Frame All | `clip.dopesheet_view_all` |  |
| NDOF Fit | Frame All | `clip.dopesheet_view_all` |  |

## Spreadsheet Generic

Space `SPREADSHEET`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+[ | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| Ctrl+] | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |

## Frames

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Media Last | Jump to Endpoint | `screen.frame_jump` | end=True |
| Media First | Jump to Endpoint | `screen.frame_jump` | end=False |
| Space Bar | Play Animation | `screen.animation_play` |  |
| Esc | Cancel Animation | `screen.animation_cancel` |  |
| Media Play/Pause | Play Animation | `screen.animation_play` |  |
| Media Stop | Cancel Animation | `screen.animation_cancel` |  |

## Animation

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_seconds' |

## Animation Channels

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mouse Click on Channels | `anim.channels_click` |  |
| Shift+Left Mouse click | Mouse Click on Channels | `anim.channels_click` | extend_range=True |
| Ctrl+Left Mouse click | Mouse Click on Channels | `anim.channels_click` | extend=True |
| Ctrl+Shift+Left Mouse | Mouse Click on Channels | `anim.channels_click` | children_only=True |
| Return | Rename Channel | `anim.channels_rename` |  |
| Left Mouse double click | Rename Channel | `anim.channels_rename` |  |
| Left Mouse double click | Select Channel Keyframes | `anim.channel_select_keys` |  |
| Shift+Left Mouse double click | Select Channel Keyframes | `anim.channel_select_keys` | extend=True |
| Ctrl+F | Filter Channels | `anim.channels_select_filter` |  |
| Ctrl+A | Select All | `anim.channels_select_all` | action='SELECT' |
| Ctrl+Shift+A | Select All | `anim.channels_select_all` | action='DESELECT' |
| Ctrl+I | Select All | `anim.channels_select_all` | action='INVERT' |
| Left Mouse drag | Box Select | `anim.channels_select_box` |  |
| Shift+Left Mouse drag | Box Select | `anim.channels_select_box` | extend=True |
| Ctrl+Left Mouse drag | Box Select | `anim.channels_select_box` | deselect=True |
| Backspace | Delete Channels | `anim.channels_delete` |  |
| Delete | Delete Channels | `anim.channels_delete` |  |
| Shift+W | Toggle Channel Setting | `anim.channels_setting_toggle` |  |
| Ctrl+Shift+W | Enable Channel Setting | `anim.channels_setting_enable` |  |
| Alt+W | Disable Channel Setting | `anim.channels_setting_disable` |  |
| Left Mouse double click | Toggle Channel Editability | `anim.channels_editable_toggle` |  |
| Right Arrow | Expand Channels | `anim.channels_expand` |  |
| Left Arrow | Collapse Channels | `anim.channels_collapse` |  |
| Ctrl+Numpad + | Expand Channels | `anim.channels_expand` | all=False |
| Ctrl+Numpad - | Collapse Channels | `anim.channels_collapse` | all=False |
| Page Up (repeat) | Move Channels | `anim.channels_move` | direction='UP' |
| Page Down (repeat) | Move Channels | `anim.channels_move` | direction='DOWN' |
| Shift+Page Up | Move Channels | `anim.channels_move` | direction='TOP' |
| Shift+Page Down | Move Channels | `anim.channels_move` | direction='BOTTOM' |
| Ctrl+G | Group Channels | `anim.channels_group` |  |
| Ctrl+Alt+G | Ungroup Channels | `anim.channels_ungroup` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='DOPESHEET_MT_channel_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='DOPESHEET_MT_channel_context_menu' |

## Paint Face Mask (Weight, Vertex, Texture)

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Shift+Alt+Left Mouse | Select | `view3d.select` | deselect_all=True |
| Ctrl+Shift+Alt+Left Mouse | Select | `view3d.select` | toggle=True |
| Ctrl+A | (De)select All | `paint.face_select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `paint.face_select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `paint.face_select_all` | action='INVERT' |
| Ctrl+H | Face Select Hide | `paint.face_select_hide` | unselected=False |
| Shift+H | Face Select Hide | `paint.face_select_hide` | unselected=True |
| Alt+H | Reveal Faces/Vertices | `paint.face_vert_reveal` |  |
| Ctrl+L | Select Linked | `paint.face_select_linked` |  |
| Alt+Left Mouse double click | Select Linked Pick | `paint.face_select_linked_pick` | deselect=False |
| Ctrl+Alt+Left Mouse double click | Select Linked Pick | `paint.face_select_linked_pick` | deselect=True |

## Paint Vertex Selection (Weight, Vertex)

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Shift+Alt+Left Mouse | Select | `view3d.select` | deselect_all=True |
| Ctrl+Shift+Alt+Left Mouse | Select | `view3d.select` | toggle=True |
| Ctrl+A | (De)select All | `paint.vert_select_all` |  |
| Shift+H | Vertex Select Hide | `paint.vert_select_hide` | unselected=True |
| Alt+H | Reveal Faces/Vertices | `paint.face_vert_reveal` |  |
| Ctrl+L | Select Linked Vertices | `paint.vert_select_linked` |  |
| Alt+Left Mouse double click | Select Linked Vertices Pick | `paint.vert_select_linked_pick` | select=True |
| Ctrl+Alt+Left Mouse double click | Select Linked Vertices Pick | `paint.vert_select_linked_pick` | select=False |

## Pose

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Arrow | Frame Offset | `screen.frame_offset` | delta=-1 |
| Right Arrow | Frame Offset | `screen.frame_offset` | delta=1 |
| Ctrl+Right Arrow | Jump to Endpoint | `screen.frame_jump` | end=True |
| Ctrl+Left Arrow | Jump to Endpoint | `screen.frame_jump` | end=False |
| P | Make Parent | `object.parent_set` |  |
| Ctrl+H | Hide Selected | `pose.hide` | unselected=False |
| Shift+H | Hide Selected | `pose.hide` | unselected=True |
| Alt+H | Reveal Selected | `pose.reveal` |  |
| Alt+E | Clear Pose Rotation | `pose.rot_clear` |  |
| Alt+W | Clear Pose Location | `pose.loc_clear` |  |
| Alt+R | Clear Pose Scale | `pose.scale_clear` |  |
| Ctrl+C | Copy Pose | `pose.copy` |  |
| Ctrl+V | Paste Pose | `pose.paste` | flipped=False |
| Ctrl+Shift+V | Paste Pose | `pose.paste` | flipped=True |
| Ctrl+A | (De)select All | `pose.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `pose.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `pose.select_all` | action='INVERT' |
| Ctrl+Up Arrow | Select Parent Bone | `pose.select_parent` |  |
| Up Arrow (repeat) | Select Hierarchy | `pose.select_hierarchy` | direction='PARENT', extend=False |
| Shift+Up Arrow (repeat) | Select Hierarchy | `pose.select_hierarchy` | direction='PARENT', extend=True |
| Down Arrow (repeat) | Select Hierarchy | `pose.select_hierarchy` | direction='CHILD', extend=False |
| Shift+Down Arrow (repeat) | Select Hierarchy | `pose.select_hierarchy` | direction='CHILD', extend=True |
| Ctrl+L | Select Connected | `pose.select_linked` |  |
| Shift+S | Insert Keyframe | `anim.keyframe_insert` |  |
| S | Insert Keyframe (by name) | `anim.keyframe_insert_by_name` | type='LocRotScale' |
| Shift+W | Insert Keyframe (by name) | `anim.keyframe_insert_by_name` | type='Location' |
| Shift+E | Insert Keyframe (by name) | `anim.keyframe_insert_by_name` | type='Rotation' |
| Shift+R | Insert Keyframe (by name) | `anim.keyframe_insert_by_name` | type='Scaling' |
| Alt+S | Delete Keyframe | `anim.keyframe_delete_v3d` |  |
| Ctrl+Shift+Alt+S | Set Active Keying Set | `anim.keying_set_active_set` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_pose_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_pose_context_menu' |
| Shift+Alt+W | Call Menu | `wm.call_menu` | name='POSE_MT_selection_sets_select' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| M | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.measure', cycle=True |

## Object Mode

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Arrow | Frame Offset | `screen.frame_offset` | delta=-1 |
| Right Arrow | Frame Offset | `screen.frame_offset` | delta=1 |
| Ctrl+Right Arrow | Jump to Endpoint | `screen.frame_jump` | end=True |
| Ctrl+Left Arrow | Jump to Endpoint | `screen.frame_jump` | end=False |
| Ctrl+A | (De)select All | `object.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `object.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `object.select_all` | action='INVERT' |
| Up Arrow (repeat) | Select More | `object.select_more` |  |
| Down Arrow (repeat) | Select Less | `object.select_less` |  |
| Ctrl+L | Select Linked | `object.select_linked` |  |
| [ (repeat) | Select Hierarchy | `object.select_hierarchy` | direction='PARENT', extend=False |
| Shift+[ (repeat) | Select Hierarchy | `object.select_hierarchy` | direction='PARENT', extend=True |
| ] (repeat) | Select Hierarchy | `object.select_hierarchy` | direction='CHILD', extend=False |
| Shift+] (repeat) | Select Hierarchy | `object.select_hierarchy` | direction='CHILD', extend=True |
| P | Make Parent | `object.parent_set` |  |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit_objects' |
| Shift+P | Clear Parent | `object.parent_clear` |  |
| Alt+W | Clear Location | `object.location_clear` | clear_delta=False |
| Alt+E | Clear Rotation | `object.rotation_clear` | clear_delta=False |
| Alt+R | Clear Scale | `object.scale_clear` | clear_delta=False |
| Backspace | Delete | `object.delete` | use_global=False, confirm=False |
| Shift+Backspace | Delete | `object.delete` | use_global=True, confirm=False |
| Delete | Delete | `object.delete` | use_global=False, confirm=False |
| Shift+Delete | Delete | `object.delete` | use_global=True, confirm=False |
| Ctrl+D | Duplicate Objects | `object.duplicate_move` |  |
| Shift+S | Insert Keyframe | `anim.keyframe_insert` |  |
| S | Insert Keyframe (by name) | `anim.keyframe_insert_by_name` | type='LocRotScale' |
| Shift+W | Insert Keyframe (by name) | `anim.keyframe_insert_by_name` | type='Location' |
| Shift+E | Insert Keyframe (by name) | `anim.keyframe_insert_by_name` | type='Rotation' |
| Shift+R | Insert Keyframe (by name) | `anim.keyframe_insert_by_name` | type='Scaling' |
| Alt+S | Delete Keyframe | `anim.keyframe_delete_v3d` |  |
| Ctrl+Shift+Alt+S | Set Active Keying Set | `anim.keying_set_active_set` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_object_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_object_context_menu' |
| Ctrl+G | Call Menu | `wm.call_menu` | name='OBJECT_MT_move_to_collection' |
| Ctrl+Shift+G | Call Menu | `wm.call_menu` | name='OBJECT_MT_link_to_collection' |
| Alt+H | Show Hidden Objects | `object.hide_view_clear` |  |
| Ctrl+H | Hide Objects | `object.hide_view_set` | unselected=False |
| Shift+H | Hide Objects | `object.hide_view_set` | unselected=True |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| M | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.measure', cycle=True |
| C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor', cycle=True |
| 1 | Set Object Mode with Sub-mode | `object.mode_set_with_submode` | mode='EDIT', mesh_select_mode={'VERT'} |
| 2 | Set Object Mode with Sub-mode | `object.mode_set_with_submode` | mode='EDIT', mesh_select_mode={'EDGE'} |
| 3 | Set Object Mode with Sub-mode | `object.mode_set_with_submode` | mode='EDIT', mesh_select_mode={'FACE'} |

## Paint Curve

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+Left Mouse | Add Curve Point and Slide | `paintcurve.add_point_slide` |  |
| Left Mouse | Select Paint Curve Point | `paintcurve.select` | extend=False |
| Shift+Left Mouse | Select Paint Curve Point | `paintcurve.select` | extend=True |
| Left Mouse | Slide Paint Curve Point | `paintcurve.slide` | align=False |
| Shift+Left Mouse | Slide Paint Curve Point | `paintcurve.slide` | align=True |
| A | Select Paint Curve Point | `paintcurve.select` | toggle=True |
| Left Mouse | Place Cursor | `paintcurve.cursor` |  |
| Backspace | Remove Paint Curve Point | `paintcurve.delete_point` |  |
| Delete | Remove Paint Curve Point | `paintcurve.delete_point` |  |
| Return | Draw Curve | `paintcurve.draw` |  |
| Numpad Enter | Draw Curve | `paintcurve.draw` |  |
| W | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| E | Rotate | `transform.rotate` |  |
| R | Resize | `transform.resize` |  |

## Curve

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+A | (De)select All | `curve.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `curve.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `curve.select_all` | action='INVERT' |
| Shift+R | Select Control Point Row | `curve.select_row` |  |
| Up Arrow (repeat) | Select More | `curve.select_more` |  |
| Down Arrow (repeat) | Select Less | `curve.select_less` |  |
| Ctrl+L | Select Linked All | `curve.select_linked` |  |
| Ctrl+Shift+Left Mouse | Pick Shortest Path | `curve.shortest_path_pick` |  |
| Ctrl+D | Add Duplicate | `curve.duplicate_move` |  |
| Backspace | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curve_delete' |
| Delete | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curve_delete' |
| Ctrl+Backspace | Dissolve Vertices | `curve.dissolve_verts` |  |
| Ctrl+Delete | Dissolve Vertices | `curve.dissolve_verts` |  |
| Alt+T | Clear Tilt | `curve.tilt_clear` |  |
| Alt+H | Reveal Hidden | `curve.reveal` |  |
| Ctrl+H | Hide Selected | `curve.hide` | unselected=False |
| Shift+H | Hide Selected | `curve.hide` | unselected=True |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curve_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curve_context_menu' |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| M | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.measure', cycle=True |
| C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor', cycle=True |
| Ctrl+E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.extrude', cycle=True |
| Y | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.tilt', cycle=True |
| U | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.radius', cycle=True |

## Image Paint

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Image Paint | `paint.image_paint` | mode='NORMAL' |
| Ctrl+Left Mouse | Image Paint | `paint.image_paint` | mode='INVERT' |
| I | Sample Color | `paint.sample_color` | merged=False |
| Shift+I | Sample Color | `paint.sample_color` | merged=True |
| X | Swap Colors | `paint.brush_colors_flip` |  |
| Middle Mouse | Grab Clone | `paint.grab_clone` |  |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| S | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.image_paint.brush.size', data_path_secondary='tool_settings.image_paint.unified_paint_settings.size', use_secondary='tool_settings.image_paint.brush.use_unified_size', rotation_path='tool_settings.image_paint.brush.mask_texture_slot.angle', color_path='tool_settings.image_paint.brush.cursor_color_add', fill_color_path='tool_settings.image_paint.brush.color', fill_color_override_path='tool_settings.image_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.image_paint.brush.use_unified_color', zoom_path='space_data.zoom', image_id='tool_settings.image_paint.brush', secondary_tex=True |
| U | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.image_paint.brush.strength', data_path_secondary='tool_settings.image_paint.unified_paint_settings.strength', use_secondary='tool_settings.image_paint.brush.use_unified_strength', rotation_path='tool_settings.image_paint.brush.mask_texture_slot.angle', color_path='tool_settings.image_paint.brush.cursor_color_add', fill_color_path='tool_settings.image_paint.brush.color', fill_color_override_path='tool_settings.image_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.image_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.image_paint.brush', secondary_tex=True |
| Ctrl+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.image_paint.brush.texture_slot.angle', data_path_secondary='', use_secondary='', rotation_path='tool_settings.image_paint.brush.texture_slot.angle', color_path='tool_settings.image_paint.brush.cursor_color_add', fill_color_path='tool_settings.image_paint.brush.color', fill_color_override_path='tool_settings.image_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.image_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.image_paint.brush', secondary_tex=False |
| Ctrl+Alt+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.image_paint.brush.mask_texture_slot.angle', data_path_secondary='', use_secondary='', rotation_path='tool_settings.image_paint.brush.mask_texture_slot.angle', color_path='tool_settings.image_paint.brush.cursor_color_add', fill_color_path='tool_settings.image_paint.brush.color', fill_color_override_path='tool_settings.image_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.image_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.image_paint.brush', secondary_tex=True |
| Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION' |
| Shift+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE' |
| Ctrl+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION' |
| Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION', texmode='SECONDARY' |
| Shift+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE', texmode='SECONDARY' |
| Ctrl+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION', texmode='SECONDARY' |
| 1 | Context Toggle | `wm.context_toggle` | data_path='image_paint_object.data.use_paint_mask' |
| L | Context Toggle | `wm.context_toggle` | data_path='tool_settings.image_paint.brush.use_smooth_stroke' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_texture_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_texture_context_menu' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| B | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_texture_paint' |
| B | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='IMAGE_AST_brush_paint' |

## Vertex Paint

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Vertex Paint | `paint.vertex_paint` | mode='NORMAL' |
| Ctrl+Left Mouse | Vertex Paint | `paint.vertex_paint` | mode='INVERT' |
| Shift+Left Mouse | Vertex Paint | `paint.vertex_paint` | brush_toggle='SMOOTH' |
| I | Sample Color | `paint.sample_color` | merged=False |
| Shift+I | Sample Color | `paint.sample_color` | merged=True |
| X | Swap Colors | `paint.brush_colors_flip` |  |
| Backspace | Set Vertex Colors | `paint.vertex_color_set` |  |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| S | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.vertex_paint.brush.size', data_path_secondary='tool_settings.vertex_paint.unified_paint_settings.size', use_secondary='tool_settings.vertex_paint.brush.use_unified_size', rotation_path='tool_settings.vertex_paint.brush.texture_slot.angle', color_path='tool_settings.vertex_paint.brush.cursor_color_add', fill_color_path='tool_settings.vertex_paint.brush.color', fill_color_override_path='tool_settings.vertex_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.vertex_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.vertex_paint.brush', secondary_tex=False |
| U | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.vertex_paint.brush.strength', data_path_secondary='tool_settings.vertex_paint.unified_paint_settings.strength', use_secondary='tool_settings.vertex_paint.brush.use_unified_strength', rotation_path='tool_settings.vertex_paint.brush.texture_slot.angle', color_path='tool_settings.vertex_paint.brush.cursor_color_add', fill_color_path='tool_settings.vertex_paint.brush.color', fill_color_override_path='tool_settings.vertex_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.vertex_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.vertex_paint.brush', secondary_tex=False |
| Ctrl+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.vertex_paint.brush.texture_slot.angle', data_path_secondary='', use_secondary='', rotation_path='tool_settings.vertex_paint.brush.texture_slot.angle', color_path='tool_settings.vertex_paint.brush.cursor_color_add', fill_color_path='tool_settings.vertex_paint.brush.color', fill_color_override_path='tool_settings.vertex_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.vertex_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.vertex_paint.brush', secondary_tex=False |
| Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION' |
| Shift+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE' |
| Ctrl+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION' |
| Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION', texmode='SECONDARY' |
| Shift+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE', texmode='SECONDARY' |
| Ctrl+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION', texmode='SECONDARY' |
| 1 | Context Toggle | `wm.context_toggle` | data_path='vertex_paint_object.data.use_paint_mask' |
| 2 | Context Toggle | `wm.context_toggle` | data_path='vertex_paint_object.data.use_paint_mask_vertex' |
| L | Context Toggle | `wm.context_toggle` | data_path='tool_settings.vertex_paint.brush.use_smooth_stroke' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_vertex_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_vertex_context_menu' |
| Alt+A | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_mesh_paint_automasking_pie' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| B | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_vertex_paint' |

## Weight Paint

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Weight Paint | `paint.weight_paint` | mode='NORMAL' |
| Ctrl+Left Mouse | Weight Paint | `paint.weight_paint` | mode='INVERT' |
| Shift+Left Mouse | Weight Paint | `paint.weight_paint` | brush_toggle='SMOOTH' |
| I | Weight Paint Sample Weight | `paint.weight_sample` |  |
| Alt+I | Weight Paint Sample Group | `paint.weight_sample_group` |  |
| Backspace | Set Weight | `paint.weight_set` |  |
| Ctrl+Alt+I | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_wpaint_vgroup_lock_pie' |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| S | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.weight_paint.brush.size', data_path_secondary='tool_settings.weight_paint.unified_paint_settings.size', use_secondary='tool_settings.weight_paint.brush.use_unified_size', rotation_path='tool_settings.weight_paint.brush.texture_slot.angle', color_path='tool_settings.weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.weight_paint.brush', secondary_tex=False |
| U | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.weight_paint.brush.strength', data_path_secondary='tool_settings.weight_paint.unified_paint_settings.strength', use_secondary='tool_settings.weight_paint.brush.use_unified_strength', rotation_path='tool_settings.weight_paint.brush.texture_slot.angle', color_path='tool_settings.weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.weight_paint.brush', secondary_tex=False |
| Ctrl+Alt+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.weight_paint.brush.mask_texture_slot.angle', data_path_secondary='', use_secondary='', rotation_path='tool_settings.weight_paint.brush.texture_slot.angle', color_path='tool_settings.weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.weight_paint.brush', secondary_tex=False |
| Ctrl+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.weight_paint.brush.weight', data_path_secondary='tool_settings.weight_paint.unified_paint_settings.weight', use_secondary='tool_settings.weight_paint.brush.use_unified_weight', rotation_path='tool_settings.weight_paint.brush.texture_slot.angle', color_path='tool_settings.weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.weight_paint.brush', secondary_tex=False |
| 1 | Context Toggle | `wm.context_toggle` | data_path='weight_paint_object.data.use_paint_mask' |
| 2 | Context Toggle | `wm.context_toggle` | data_path='weight_paint_object.data.use_paint_mask_vertex' |
| L | Context Toggle | `wm.context_toggle` | data_path='tool_settings.weight_paint.brush.use_smooth_stroke' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_weight_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_weight_context_menu' |
| Alt+A | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_mesh_paint_automasking_pie' |
| Shift+Alt+Left Mouse | Select | `view3d.select` |  |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor', cycle=True |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| B | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_weight_paint' |

## Sculpt

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Shift+Right Mouse | Set Pivot Position | `sculpt.set_pivot_position` | mode='SURFACE' |
| Left Mouse | Sculpt | `sculpt.brush_stroke` | mode='NORMAL' |
| Ctrl+Left Mouse | Sculpt | `sculpt.brush_stroke` | mode='INVERT' |
| Shift+Left Mouse | Sculpt | `sculpt.brush_stroke` | brush_toggle='SMOOTH' |
| Ctrl+Alt+Left Mouse | Sculpt | `sculpt.brush_stroke` | brush_toggle='MASK' |
| Ctrl+Shift+Alt+Left Mouse | Sculpt | `sculpt.brush_stroke` | mode='INVERT', brush_toggle='MASK' |
| Shift+A | Expand | `sculpt.expand` | target='MASK', falloff_type='GEODESIC', invert=False, use_auto_mask=False, use_mask_preserve=True |
| Shift+Alt+A | Expand | `sculpt.expand` | target='MASK', falloff_type='NORMALS', invert=False, use_mask_preserve=True |
| Shift+W | Expand | `sculpt.expand` | target='FACE_SETS', falloff_type='GEODESIC', invert=False, use_mask_preserve=False, use_modify_active=False |
| Shift+Alt+W | Expand | `sculpt.expand` | target='FACE_SETS', falloff_type='BOUNDARY_FACE_SET', invert=False, use_mask_preserve=False, use_modify_active=True |
| H | Face Sets Visibility | `sculpt.face_set_change_visibility` | mode='HIDE_ACTIVE' |
| Shift+H | Face Sets Visibility | `sculpt.face_set_change_visibility` | mode='TOGGLE' |
| Ctrl+H | Hide/Show Masked | `paint.hide_show_masked` | action='HIDE' |
| Alt+H | Hide/Show All | `paint.hide_show_all` | action='SHOW' |
| Ctrl+0 | Subdivision Set | `object.subdivision_set` | level=0, relative=False, ensure_modifier=True |
| Ctrl+1 | Subdivision Set | `object.subdivision_set` | level=1, relative=False, ensure_modifier=True |
| Ctrl+2 | Subdivision Set | `object.subdivision_set` | level=2, relative=False, ensure_modifier=True |
| Ctrl+3 | Subdivision Set | `object.subdivision_set` | level=3, relative=False, ensure_modifier=True |
| Ctrl+4 | Subdivision Set | `object.subdivision_set` | level=4, relative=False, ensure_modifier=True |
| Ctrl+5 | Subdivision Set | `object.subdivision_set` | level=5, relative=False, ensure_modifier=True |
| D (repeat) | Subdivision Set | `object.subdivision_set` | level=1, relative=True, ensure_modifier=False |
| Shift+D (repeat) | Subdivision Set | `object.subdivision_set` | level=-1, relative=True, ensure_modifier=False |
| Ctrl+Shift+A | Mask Flood Fill | `paint.mask_flood_fill` | mode='VALUE', value=1.0 |
| Ctrl+I | Mask Flood Fill | `paint.mask_flood_fill` | mode='INVERT' |
| Page Up | Edit Face Set | `sculpt.face_set_edit` | mode='GROW' |
| Page Down | Edit Face Set | `sculpt.face_set_edit` | mode='SHRINK' |
| Ctrl+D | Detail Flood Fill | `sculpt.detail_flood_fill` |  |
| Ctrl+Shift+D | Edit Dyntopo Detail Size | `sculpt.dyntopo_detail_size_edit` |  |
| Ctrl+D | Voxel Remesh | `object.voxel_remesh` |  |
| Ctrl+Shift+D | Edit Voxel Size | `object.voxel_size_edit` |  |
| I | Sample Color | `paint.sample_color` | merged=False |
| Shift+I | Sample Color | `paint.sample_color` | merged=True |
| X | Swap Colors | `paint.brush_colors_flip` |  |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| S | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.sculpt.brush.size', data_path_secondary='tool_settings.sculpt.unified_paint_settings.size', use_secondary='tool_settings.sculpt.brush.use_unified_size', rotation_path='tool_settings.sculpt.brush.texture_slot.angle', color_path='tool_settings.sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.sculpt.brush', secondary_tex=False |
| U | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.sculpt.brush.strength', data_path_secondary='tool_settings.sculpt.unified_paint_settings.strength', use_secondary='tool_settings.sculpt.brush.use_unified_strength', rotation_path='tool_settings.sculpt.brush.texture_slot.angle', color_path='tool_settings.sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.sculpt.brush', secondary_tex=False |
| Ctrl+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.sculpt.brush.texture_slot.angle', data_path_secondary='', use_secondary='', rotation_path='tool_settings.sculpt.brush.texture_slot.angle', color_path='tool_settings.sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.sculpt.brush', secondary_tex=False |
| Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION' |
| Shift+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE' |
| Ctrl+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION' |
| Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION', texmode='SECONDARY' |
| Shift+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE', texmode='SECONDARY' |
| Ctrl+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION', texmode='SECONDARY' |
| L | Context Toggle | `wm.context_toggle` | data_path='tool_settings.sculpt.brush.use_smooth_stroke' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.box_mask', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| Ctrl+A | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_sculpt_mask_edit_pie' |
| Alt+A | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_mesh_paint_automasking_pie' |
| Ctrl+W | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_sculpt_face_sets_edit_pie' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_sculpt_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_sculpt_context_menu' |
| B | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_sculpt' |

## Mesh

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse double click | Loop Select | `mesh.loop_select` | extend=False, deselect=False, toggle=False |
| Shift+Left Mouse double click | Loop Select | `mesh.loop_select` | extend=True, deselect=False, toggle=False |
| Ctrl+Left Mouse double click | Loop Select | `mesh.loop_select` | extend=False, deselect=True, toggle=False |
| Alt+Left Mouse double click | Edge Ring Select | `mesh.edgering_select` | extend=False, deselect=False, toggle=False |
| Shift+Alt+Left Mouse double click | Edge Ring Select | `mesh.edgering_select` | extend=True, deselect=False, toggle=False |
| Ctrl+Alt+Left Mouse double click | Edge Ring Select | `mesh.edgering_select` | extend=False, deselect=True, toggle=False |
| Ctrl+Shift+Left Mouse | Pick Shortest Path | `mesh.shortest_path_pick` | use_fill=False |
| Ctrl+Shift+Alt+Left Mouse | Pick Shortest Path | `mesh.shortest_path_pick` | use_fill=True |
| Ctrl+A | (De)select All | `mesh.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `mesh.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `mesh.select_all` | action='INVERT' |
| Up Arrow (repeat) | Select More | `mesh.select_more` |  |
| Down Arrow (repeat) | Select Less | `mesh.select_less` |  |
| Ctrl+L | Select Linked All | `mesh.select_linked` |  |
| 1 | Select Mode | `mesh.select_mode` | type='VERT' |
| 2 | Select Mode | `mesh.select_mode` | type='EDGE' |
| 3 | Select Mode | `mesh.select_mode` | type='FACE' |
| Shift+1 | Select Mode | `mesh.select_mode` | use_extend=True, type='VERT' |
| Shift+2 | Select Mode | `mesh.select_mode` | use_extend=True, type='EDGE' |
| Shift+3 | Select Mode | `mesh.select_mode` | use_extend=True, type='FACE' |
| Ctrl+1 | Select Mode | `mesh.select_mode` | use_expand=True, type='VERT' |
| Ctrl+2 | Select Mode | `mesh.select_mode` | use_expand=True, type='EDGE' |
| Ctrl+3 | Select Mode | `mesh.select_mode` | use_expand=True, type='FACE' |
| Ctrl+Shift+1 | Select Mode | `mesh.select_mode` | use_extend=True, use_expand=True, type='VERT' |
| Ctrl+Shift+2 | Select Mode | `mesh.select_mode` | use_extend=True, use_expand=True, type='EDGE' |
| Ctrl+Shift+3 | Select Mode | `mesh.select_mode` | use_extend=True, use_expand=True, type='FACE' |
| Ctrl+H | Hide Selected | `mesh.hide` | unselected=False |
| Shift+H | Hide Selected | `mesh.hide` | unselected=True |
| Alt+H | Reveal Hidden | `mesh.reveal` |  |
| Ctrl+D | Add Duplicate | `mesh.duplicate_move` |  |
| Backspace | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_delete' |
| Delete | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_delete' |
| Ctrl+Backspace | Dissolve Selection | `mesh.dissolve_mode` |  |
| Ctrl+Delete | Dissolve Selection | `mesh.dissolve_mode` |  |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_context_menu' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| M | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.measure', cycle=True |
| C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor', cycle=True |
| Ctrl+B | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.bevel', cycle=True |
| I | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.inset_faces', cycle=True |
| Ctrl+E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.extrude_region', cycle=True |
| K | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.knife', cycle=True |
| Alt+C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.loop_cut', cycle=True |

## Armature

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+H | Hide Selected | `armature.hide` | unselected=False |
| Shift+H | Hide Selected | `armature.hide` | unselected=True |
| Alt+H | Reveal Hidden | `armature.reveal` |  |
| P | Make Parent | `armature.parent_set` |  |
| Shift+P | Clear Parent | `armature.parent_clear` |  |
| Ctrl+A | (De)select All | `armature.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `armature.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `armature.select_all` | action='INVERT' |
| [ | Select Hierarchy | `armature.select_hierarchy` | direction='PARENT', extend=False |
| Shift+[ | Select Hierarchy | `armature.select_hierarchy` | direction='PARENT', extend=True |
| ] | Select Hierarchy | `armature.select_hierarchy` | direction='CHILD', extend=False |
| Shift+] | Select Hierarchy | `armature.select_hierarchy` | direction='CHILD', extend=True |
| Up Arrow (repeat) | Select More | `armature.select_more` |  |
| Down Arrow (repeat) | Select Less | `armature.select_less` |  |
| Shift+G | Select Similar | `armature.select_similar` |  |
| Ctrl+L | Select Linked | `armature.select_linked_pick` | deselect=False |
| Ctrl+Shift+Left Mouse | Pick Shortest Path | `armature.shortest_path_pick` |  |
| Delete | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_armature_delete' |
| Backspace | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_armature_delete' |
| Ctrl+D | Duplicate | `armature.duplicate_move` |  |
| Ctrl+Backspace | Dissolve Selected Bone(s) | `armature.dissolve` |  |
| Ctrl+Delete | Dissolve Selected Bone(s) | `armature.dissolve` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_armature_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_armature_context_menu' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| M | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.measure', cycle=True |
| C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor', cycle=True |
| Y | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.roll', cycle=True |
| Ctrl+E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.extrude', cycle=True |

## Metaball

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Alt+H | Reveal Hidden | `mball.reveal_metaelems` |  |
| Ctrl+H | Hide Selected | `mball.hide_metaelems` | unselected=False |
| Shift+H | Hide Selected | `mball.hide_metaelems` | unselected=True |
| Backspace | Delete | `mball.delete_metaelems` |  |
| Delete | Delete | `mball.delete_metaelems` |  |
| Ctrl+D | Duplicate | `mball.duplicate_move` |  |
| Ctrl+A | (De)select All | `mball.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `mball.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `mball.select_all` | action='INVERT' |
| Shift+G | Select Similar | `mball.select_similar` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_metaball_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_metaball_context_menu' |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| M | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.measure', cycle=True |
| C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor', cycle=True |

## Lattice

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+A | (De)select All | `lattice.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `lattice.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `lattice.select_all` | action='INVERT' |
| Up Arrow (repeat) | Select More | `lattice.select_more` |  |
| Down Arrow (repeat) | Select Less | `lattice.select_less` |  |
| Ctrl+P | Make Vertex Parent | `object.vertex_parent_set` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_lattice_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_lattice_context_menu' |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| M | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.measure', cycle=True |

## Particle

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+A | (De)select All | `particle.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `particle.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `particle.select_all` | action='INVERT' |
| Up Arrow (repeat) | Select More | `particle.select_more` |  |
| Down Arrow (repeat) | Select Less | `particle.select_less` |  |
| Ctrl+L | Select Linked | `particle.select_linked_pick` | deselect=False |
| Alt+Left Mouse double click | Select Linked | `particle.select_linked_pick` | deselect=True |
| Shift+Alt+Left Mouse double click | Select Linked All | `particle.select_linked` |  |
| Backspace | Delete | `particle.delete` |  |
| Delete | Delete | `particle.delete` |  |
| Alt+H | Reveal | `particle.reveal` |  |
| Ctrl+H | Hide Selected | `particle.hide` | unselected=False |
| Shift+H | Hide Selected | `particle.hide` | unselected=True |
| Left Mouse | Brush Edit | `particle.brush_edit` |  |
| Shift+Left Mouse | Brush Edit | `particle.brush_edit` |  |
| S | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.particle_edit.brush.size' |
| U | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.particle_edit.brush.strength' |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_particle_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_particle_context_menu' |

## Font

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+B | Toggle Style | `font.style_toggle` | style='BOLD' |
| Ctrl+I | Toggle Style | `font.style_toggle` | style='ITALIC' |
| Ctrl+U | Toggle Style | `font.style_toggle` | style='UNDERLINE' |
| Ctrl+P | Toggle Style | `font.style_toggle` | style='SMALL_CAPS' |
| Delete (repeat) | Delete | `font.delete` | type='NEXT_OR_SELECTION' |
| Ctrl+Delete (repeat) | Delete | `font.delete` | type='NEXT_WORD' |
| Backspace (repeat) | Delete | `font.delete` | type='PREVIOUS_OR_SELECTION' |
| Shift+Backspace (repeat) | Delete | `font.delete` | type='PREVIOUS_OR_SELECTION' |
| Ctrl+Backspace (repeat) | Delete | `font.delete` | type='PREVIOUS_WORD' |
| Home | Move Cursor | `font.move` | type='LINE_BEGIN' |
| End | Move Cursor | `font.move` | type='LINE_END' |
| Left Arrow (repeat) | Move Cursor | `font.move` | type='PREVIOUS_CHARACTER' |
| Right Arrow (repeat) | Move Cursor | `font.move` | type='NEXT_CHARACTER' |
| Ctrl+Left Arrow (repeat) | Move Cursor | `font.move` | type='PREVIOUS_WORD' |
| Ctrl+Right Arrow (repeat) | Move Cursor | `font.move` | type='NEXT_WORD' |
| Up Arrow (repeat) | Move Cursor | `font.move` | type='PREVIOUS_LINE' |
| Down Arrow (repeat) | Move Cursor | `font.move` | type='NEXT_LINE' |
| Page Up (repeat) | Move Cursor | `font.move` | type='PREVIOUS_PAGE' |
| Page Down (repeat) | Move Cursor | `font.move` | type='NEXT_PAGE' |
| Ctrl+Home (repeat) | Move Cursor | `font.move` | type='TEXT_BEGIN' |
| Ctrl+End (repeat) | Move Cursor | `font.move` | type='TEXT_END' |
| Shift+Home | Move Select | `font.move_select` | type='LINE_BEGIN' |
| Shift+End | Move Select | `font.move_select` | type='LINE_END' |
| Shift+Left Arrow (repeat) | Move Select | `font.move_select` | type='PREVIOUS_CHARACTER' |
| Shift+Right Arrow (repeat) | Move Select | `font.move_select` | type='NEXT_CHARACTER' |
| Ctrl+Shift+Left Arrow (repeat) | Move Select | `font.move_select` | type='PREVIOUS_WORD' |
| Ctrl+Shift+Right Arrow (repeat) | Move Select | `font.move_select` | type='NEXT_WORD' |
| Shift+Up Arrow (repeat) | Move Select | `font.move_select` | type='PREVIOUS_LINE' |
| Shift+Down Arrow (repeat) | Move Select | `font.move_select` | type='NEXT_LINE' |
| Shift+Page Up (repeat) | Move Select | `font.move_select` | type='PREVIOUS_PAGE' |
| Shift+Page Down (repeat) | Move Select | `font.move_select` | type='NEXT_PAGE' |
| Ctrl+Shift+Home (repeat) | Move Select | `font.move_select` | type='TEXT_BEGIN' |
| Ctrl+Shift+End (repeat) | Move Select | `font.move_select` | type='TEXT_END' |
| Alt+Left Arrow (repeat) | Change Spacing | `font.change_spacing` | delta=-1.0 |
| Alt+Right Arrow (repeat) | Change Spacing | `font.change_spacing` | delta=1.0 |
| Alt+Up Arrow (repeat) | Change Character | `font.change_character` | delta=1 |
| Alt+Down Arrow (repeat) | Change Character | `font.change_character` | delta=-1 |
| Ctrl+A | Select All | `font.select_all` |  |
| Ctrl+C | Copy Text | `font.text_copy` |  |
| Ctrl+X | Cut Text | `font.text_cut` |  |
| Ctrl+V (repeat) | Paste Text | `font.text_paste` |  |
| Return | Line Break | `font.line_break` |  |
| Any modifier+Text Input any | Insert Text | `font.text_insert` |  |
| Alt+Backspace | Insert Text | `font.text_insert` | accent=True |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_font_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_font_context_menu' |

## Curves

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| 1 | Set Select Mode | `curves.set_selection_domain` | domain='POINT' |
| 2 | Set Select Mode | `curves.set_selection_domain` | domain='CURVE' |
| Ctrl+D | Duplicate | `curves.duplicate_move` |  |
| Ctrl+A | (De)select All | `curves.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `curves.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `curves.select_all` | action='INVERT' |
| Ctrl+L | Select Linked | `curves.select_linked` |  |
| Page Up (repeat) | Select More | `curves.select_more` |  |
| Page Down (repeat) | Select Less | `curves.select_less` |  |
| Delete | Delete | `curves.delete` |  |
| B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Q | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.move', cycle=True |
| E | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.rotate', cycle=True |
| R | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.scale', cycle=True |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| M | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.measure', cycle=True |
| C | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor', cycle=True |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |

## Sculpt Curves

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Stroke Curves Sculpt | `sculpt_curves.brush_stroke` | mode='NORMAL' |
| Ctrl+Left Mouse | Stroke Curves Sculpt | `sculpt_curves.brush_stroke` | mode='INVERT' |
| Shift+Left Mouse | Stroke Curves Sculpt | `sculpt_curves.brush_stroke` | brush_toggle='SMOOTH' |
| 1 | Set Select Mode | `curves.set_selection_domain` | domain='POINT' |
| 2 | Set Select Mode | `curves.set_selection_domain` | domain='CURVE' |
| S | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.curves_sculpt.brush.size', data_path_secondary='tool_settings.curves_sculpt.unified_paint_settings.size', use_secondary='tool_settings.curves_sculpt.brush.use_unified_size', rotation_path='tool_settings.curves_sculpt.brush.texture_slot.angle', color_path='tool_settings.curves_sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.curves_sculpt.brush', secondary_tex=False |
| U | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.curves_sculpt.brush.strength', data_path_secondary='tool_settings.curves_sculpt.unified_paint_settings.strength', use_secondary='tool_settings.curves_sculpt.brush.use_unified_strength', rotation_path='tool_settings.curves_sculpt.brush.texture_slot.angle', color_path='tool_settings.curves_sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.curves_sculpt.brush', secondary_tex=False |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| Ctrl+A | (De)select All | `curves.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `curves.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `curves.select_all` | action='INVERT' |
| Shift+A | Select Grow | `sculpt_curves.select_grow` |  |
| Ctrl+D | Edit Minimum Distance | `sculpt_curves.min_distance_edit` |  |
| D | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.annotate', cycle=True |
| B | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_sculpt_curves' |

## Point Cloud

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+A | (De)select All | `pointcloud.select_all` | action='SELECT' |
| Ctrl+Shift+A | (De)select All | `pointcloud.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `pointcloud.select_all` | action='INVERT' |
| Delete | Delete | `pointcloud.delete` |  |

## Object Non-modal

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| ` | Transfer Mode | `object.transfer_mode` |  |
| 4 | Set Object Mode | `object.mode_set` | mode='OBJECT' |
| 5 | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_object_mode_pie' |

## Knife Tool Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Alt+Left Mouse | PANNING | `PANNING` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Any modifier+Left Mouse double click | ADD_CUT_CLOSED | `ADD_CUT_CLOSED` |  |
| Any modifier+Left Mouse any | ADD_CUT | `ADD_CUT` |  |
| Ctrl+Z | UNDO | `UNDO` |  |
| Right Mouse | NEW_CUT | `NEW_CUT` |  |
| Left Ctrl | SNAP_MIDPOINTS_ON | `SNAP_MIDPOINTS_ON` |  |
| Left Ctrl release | SNAP_MIDPOINTS_OFF | `SNAP_MIDPOINTS_OFF` |  |
| Right Ctrl | SNAP_MIDPOINTS_ON | `SNAP_MIDPOINTS_ON` |  |
| Right Ctrl release | SNAP_MIDPOINTS_OFF | `SNAP_MIDPOINTS_OFF` |  |
| Any modifier+Left Shift | IGNORE_SNAP_ON | `IGNORE_SNAP_ON` |  |
| Any modifier+Left Shift release | IGNORE_SNAP_OFF | `IGNORE_SNAP_OFF` |  |
| Any modifier+Right Shift | IGNORE_SNAP_ON | `IGNORE_SNAP_ON` |  |
| Any modifier+Right Shift release | IGNORE_SNAP_OFF | `IGNORE_SNAP_OFF` |  |
| X | X_AXIS | `X_AXIS` |  |
| Y | Y_AXIS | `Y_AXIS` |  |
| Z | Z_AXIS | `Z_AXIS` |  |
| A | ANGLE_SNAP_TOGGLE | `ANGLE_SNAP_TOGGLE` |  |
| R | CYCLE_ANGLE_SNAP_EDGE | `CYCLE_ANGLE_SNAP_EDGE` |  |
| C | CUT_THROUGH_TOGGLE | `CUT_THROUGH_TOGGLE` |  |
| Alt+Middle Mouse | PANNING | `PANNING` |  |
| Alt+Right Mouse | PANNING | `PANNING` |  |
| D | SHOW_DISTANCE_ANGLE_TOGGLE | `SHOW_DISTANCE_ANGLE_TOGGLE` |  |
| V | DEPTH_TEST_TOGGLE | `DEPTH_TEST_TOGGLE` |  |

## Eyedropper Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Return release | SAMPLE_CONFIRM | `SAMPLE_CONFIRM` |  |
| Any modifier+Numpad Enter release | SAMPLE_CONFIRM | `SAMPLE_CONFIRM` |  |
| Any modifier+Left Mouse release | SAMPLE_CONFIRM | `SAMPLE_CONFIRM` |  |
| Any modifier+Left Mouse | SAMPLE_BEGIN | `SAMPLE_BEGIN` |  |
| Any modifier+Space Bar release | SAMPLE_RESET | `SAMPLE_RESET` |  |

## Eyedropper ColorRamp PointSampling Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Backspace | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse | SAMPLE_CONFIRM | `SAMPLE_CONFIRM` |  |
| Any modifier+Return release | SAMPLE_CONFIRM | `SAMPLE_CONFIRM` |  |
| Any modifier+Numpad Enter release | SAMPLE_CONFIRM | `SAMPLE_CONFIRM` |  |
| Any modifier+Left Mouse | SAMPLE_SAMPLE | `SAMPLE_SAMPLE` |  |
| Any modifier+Space Bar release | SAMPLE_RESET | `SAMPLE_RESET` |  |

## Transform Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Left Mouse | CONFIRM | `CONFIRM` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Any modifier+Space Bar | CONFIRM | `CONFIRM` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| X | AXIS_X | `AXIS_X` |  |
| Y | AXIS_Y | `AXIS_Y` |  |
| Z | AXIS_Z | `AXIS_Z` |  |
| Shift+X | PLANE_X | `PLANE_X` |  |
| Shift+Y | PLANE_Y | `PLANE_Y` |  |
| Shift+Z | PLANE_Z | `PLANE_Z` |  |
| C | CONS_OFF | `CONS_OFF` |  |
| G | TRANSLATE | `TRANSLATE` |  |
| G | VERT_EDGE_SLIDE | `VERT_EDGE_SLIDE` |  |
| R | ROTATE | `ROTATE` |  |
| R | TRACKBALL | `TRACKBALL` |  |
| S | RESIZE | `RESIZE` |  |
| N | ROTATE_NORMALS | `ROTATE_NORMALS` |  |
| B | EDIT_SNAP_SOURCE_ON | `EDIT_SNAP_SOURCE_ON` |  |
| B | EDIT_SNAP_SOURCE_OFF | `EDIT_SNAP_SOURCE_OFF` |  |
| Shift+Tab | SNAP_TOGGLE | `SNAP_TOGGLE` |  |
| Any modifier+Left Ctrl | SNAP_INV_ON | `SNAP_INV_ON` |  |
| Any modifier+Left Ctrl release | SNAP_INV_OFF | `SNAP_INV_OFF` |  |
| Any modifier+Right Ctrl | SNAP_INV_ON | `SNAP_INV_ON` |  |
| Any modifier+Right Ctrl release | SNAP_INV_OFF | `SNAP_INV_OFF` |  |
| A | ADD_SNAP | `ADD_SNAP` |  |
| Ctrl+A | ADD_SNAP | `ADD_SNAP` |  |
| Alt+A | REMOVE_SNAP | `REMOVE_SNAP` |  |
| Page Up (repeat) | PROPORTIONAL_SIZE_UP | `PROPORTIONAL_SIZE_UP` |  |
| Page Down (repeat) | PROPORTIONAL_SIZE_DOWN | `PROPORTIONAL_SIZE_DOWN` |  |
| Shift+Page Up (repeat) | PROPORTIONAL_SIZE_UP | `PROPORTIONAL_SIZE_UP` |  |
| Shift+Page Down (repeat) | PROPORTIONAL_SIZE_DOWN | `PROPORTIONAL_SIZE_DOWN` |  |
| Wheel Down | PROPORTIONAL_SIZE_UP | `PROPORTIONAL_SIZE_UP` |  |
| Wheel Up | PROPORTIONAL_SIZE_DOWN | `PROPORTIONAL_SIZE_DOWN` |  |
| Shift+Wheel Down | PROPORTIONAL_SIZE_UP | `PROPORTIONAL_SIZE_UP` |  |
| Shift+Wheel Up | PROPORTIONAL_SIZE_DOWN | `PROPORTIONAL_SIZE_DOWN` |  |
| Mouse/Trackpad Pan any | PROPORTIONAL_SIZE | `PROPORTIONAL_SIZE` |  |
| Page Up (repeat) | AUTOIK_CHAIN_LEN_UP | `AUTOIK_CHAIN_LEN_UP` |  |
| Page Down (repeat) | AUTOIK_CHAIN_LEN_DOWN | `AUTOIK_CHAIN_LEN_DOWN` |  |
| Shift+Page Up (repeat) | AUTOIK_CHAIN_LEN_UP | `AUTOIK_CHAIN_LEN_UP` |  |
| Shift+Page Down (repeat) | AUTOIK_CHAIN_LEN_DOWN | `AUTOIK_CHAIN_LEN_DOWN` |  |
| Wheel Down | AUTOIK_CHAIN_LEN_UP | `AUTOIK_CHAIN_LEN_UP` |  |
| Wheel Up | AUTOIK_CHAIN_LEN_DOWN | `AUTOIK_CHAIN_LEN_DOWN` |  |
| Shift+Wheel Down | AUTOIK_CHAIN_LEN_UP | `AUTOIK_CHAIN_LEN_UP` |  |
| Shift+Wheel Up | AUTOIK_CHAIN_LEN_DOWN | `AUTOIK_CHAIN_LEN_DOWN` |  |
| T | INSERTOFS_TOGGLE_DIR | `INSERTOFS_TOGGLE_DIR` |  |
| Any modifier+Left Alt release | NODE_ATTACH_ON | `NODE_ATTACH_ON` |  |
| Any modifier+Left Alt | NODE_ATTACH_OFF | `NODE_ATTACH_OFF` |  |
| Middle Mouse any | AUTOCONSTRAIN | `AUTOCONSTRAIN` |  |
| Shift+Middle Mouse any | AUTOCONSTRAINPLANE | `AUTOCONSTRAINPLANE` |  |
| Any modifier+Left Shift any | PRECISION | `PRECISION` |  |
| Any modifier+Right Shift any | PRECISION | `PRECISION` |  |
| Any modifier+C | STRIP_CLAMP_TOGGLE | `STRIP_CLAMP_TOGGLE` |  |
| S | STRIP_OVERLAP_SHUFFLE | `STRIP_OVERLAP_SHUFFLE` |  |
| R | STRIP_OVERLAP_RIPPLE | `STRIP_OVERLAP_RIPPLE` |  |
| V | STRIP_OVERLAP_OVERWRITE | `STRIP_OVERLAP_OVERWRITE` |  |

## Generic Gizmo Drag

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Gizmo Tweak | `gizmogroup.gizmo_tweak` |  |

## Generic Gizmo Maybe Drag

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Gizmo Tweak | `gizmogroup.gizmo_tweak` |  |

## 3D View Tool: Tweak

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `view3d.select` | deselect_all=True |
| Shift+Left Mouse | Select | `view3d.select` | toggle=True |

## 3D View Tool: Object, Add Primitive

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Add Primitive Object | `view3d.interactive_add` | wait_for_input=False |
| Ctrl+Left Mouse drag | Add Primitive Object | `view3d.interactive_add` | wait_for_input=False |
| Middle Mouse | Add Primitive Object | `view3d.interactive_add` | wait_for_input=False |
| Ctrl+Middle Mouse | Add Primitive Object | `view3d.interactive_add` | wait_for_input=False |

## Image Editor Tool: Uv, Tweak

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `uv.select` | deselect_all=True |
| Shift+Left Mouse | Select | `uv.select` | extend=True |

## Preview Tool: Select Box

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `sequencer.select` | deselect_all=True |
| Shift+Left Mouse | Select | `sequencer.select` | toggle=True |

## Sequencer Tool: Select Box

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `sequencer.select` | deselect_all=True |
| Shift+Left Mouse | Select | `sequencer.select` | toggle=True |

## Preferences

Space `PREFERENCES`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+F | Filter | `preferences.start_filter` |  |
| Alt+F | Clear Filter | `preferences.clear_filter` |  |

## Preferences_nav

Space `PREFERENCES`, region `UI`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+F | Filter | `preferences.start_filter` |  |
| Alt+F | Clear Filter | `preferences.clear_filter` |  |

## Time Scrub

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Change Frame | `anim.change_frame` |  |

## Clip Time Scrub

Space `CLIP_EDITOR`, region `PREVIEW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Change Frame | `clip.change_frame` |  |

## Grease Pencil

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| D (held)+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW', wait_for_input=False |
| Shift+D (held)+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW', wait_for_input=False |
| Alt+D (held)+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW_STRAIGHT', wait_for_input=False |
| Shift+Alt+D (held)+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW_POLY', wait_for_input=False |
| D (held)+Right Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |

## Grease Pencil Selection

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| A | (De)select All Strokes | `grease_pencil.select_all` | action='SELECT' |
| Alt+A | (De)select All Strokes | `grease_pencil.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All Strokes | `grease_pencil.select_all` | action='INVERT' |
| A double click | (De)select All Strokes | `grease_pencil.select_all` | action='DESELECT' |
| Ctrl+L | Select Fill | `grease_pencil.select_fill` |  |
| L | Select Linked | `grease_pencil.select_linked` |  |
| Shift+L | Select Linked | `grease_pencil.select_linked` | deselect=True |
| Ctrl+Numpad + (repeat) | Select More | `grease_pencil.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `grease_pencil.select_less` |  |
| Shift+G | Select Similar | `grease_pencil.select_similar` |  |

## Grease Pencil Draw Mode

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| A | (De)select All Strokes | `grease_pencil.select_all` | action='SELECT' |
| Alt+A | (De)select All Strokes | `grease_pencil.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All Strokes | `grease_pencil.select_all` | action='INVERT' |
| A double click | (De)select All Strokes | `grease_pencil.select_all` | action='DESELECT' |
| U | Call Menu | `wm.call_menu` | name='VIEW3D_MT_greasepencil_material_active' |
| Y | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_layer_active' |
| Alt+H | Show All Layers | `grease_pencil.layer_reveal` |  |
| H | Hide Layer(s) | `grease_pencil.layer_hide` | unselected=False |
| Shift+H | Hide Layer(s) | `grease_pencil.layer_hide` | unselected=True |
| X | Swap Colors | `paint.brush_colors_flip` |  |
| Shift+X | Sample Color | `paint.sample_color` | merged=False |
| Numpad * | Isolate Layers | `grease_pencil.layer_isolate` |  |
| I | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_greasepencil_animation' |
| Shift+I | Insert Blank Frame | `grease_pencil.insert_blank_frame` |  |
| Shift+Delete | Delete Frame | `grease_pencil.delete_frame` | type='ALL_FRAMES' |
| Alt+I | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_draw_delete' |
| Ctrl+Shift+M | Merge | `grease_pencil.layer_merge` | mode='ACTIVE' |
| Ctrl+E | Grease Pencil Interpolation | `grease_pencil.interpolate` | use_selection=False |
| Ctrl+Shift+E | Interpolate Sequence | `grease_pencil.interpolate_sequence` | use_selection=False |
| Ctrl+Alt+Right Mouse | Grease Pencil Erase Lasso | `grease_pencil.erase_lasso` |  |
| B | Grease Pencil Box Erase | `grease_pencil.erase_box` | wait_for_input=True |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.gpencil_paint.brush.size', data_path_secondary='tool_settings.gpencil_paint.unified_paint_settings.size', use_secondary='tool_settings.gpencil_paint.brush.use_unified_size', rotation_path='tool_settings.gpencil_paint.brush.texture_slot.angle', color_path='tool_settings.gpencil_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.gpencil_paint.brush', secondary_tex=False |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.gpencil_paint.brush.strength', data_path_secondary='tool_settings.gpencil_paint.unified_paint_settings.strength', use_secondary='tool_settings.gpencil_paint.brush.use_unified_strength', rotation_path='tool_settings.gpencil_paint.brush.texture_slot.angle', color_path='tool_settings.gpencil_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.gpencil_paint.brush', secondary_tex=False |
| Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_gpencil_paint' |
| W | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_draw_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_draw_context_menu' |
| Delete | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_greasepencil_delete' |
| Ctrl+C | Copy Strokes | `grease_pencil.copy` |  |
| Ctrl+V | Paste Strokes | `grease_pencil.paste` |  |
| Ctrl+Shift+V | Paste Strokes | `grease_pencil.paste` | paste_back=True |
| Shift+D | Duplicate Strokes | `grease_pencil.duplicate_move` |  |
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Right Mouse drag | Move | `transform.translate` |  |
| Shift+W | Bend | `transform.bend` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Shift+Alt+S | To Sphere | `transform.tosphere` |  |
| Ctrl+Shift+Alt+S | Shear | `transform.shear` |  |

## Grease Pencil Edit Mode

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| X | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_greasepencil_delete' |
| Delete | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_greasepencil_delete' |
| Ctrl+X | Dissolve | `grease_pencil.dissolve` |  |
| Ctrl+Delete | Dissolve | `grease_pencil.dissolve` |  |
| Ctrl+C | Copy Strokes | `grease_pencil.copy` |  |
| Ctrl+V | Paste Strokes | `grease_pencil.paste` |  |
| Ctrl+Shift+V | Paste Strokes | `grease_pencil.paste` | paste_back=True |
| Shift+S | Call Pie Menu | `wm.call_menu_pie` | name='GREASE_PENCIL_MT_snap_pie' |
| P | Separate | `grease_pencil.separate` |  |
| Shift+Delete | Delete Frame | `grease_pencil.delete_frame` | type='ALL_FRAMES' |
| I | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_greasepencil_animation' |
| Shift+I | Insert Blank Frame | `grease_pencil.insert_blank_frame` |  |
| Alt+I | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_draw_delete' |
| Alt+H | Show All Layers | `grease_pencil.layer_reveal` |  |
| H | Hide Layer(s) | `grease_pencil.layer_hide` | unselected=False |
| Shift+H | Hide Layer(s) | `grease_pencil.layer_hide` | unselected=True |
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Right Mouse drag | Move | `transform.translate` |  |
| Shift+W | Bend | `transform.bend` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Shift+Alt+S | To Sphere | `transform.tosphere` |  |
| Ctrl+Shift+Alt+S | Shear | `transform.shear` |  |
| Alt+S | Transform | `transform.transform` | mode='CURVE_SHRINKFATTEN' |
| Shift+F | Transform | `transform.transform` | mode='GPENCIL_OPACITY' |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Alt+O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_connected' |
| F | Set Cyclical State | `grease_pencil.cyclical_set` | type='CLOSE', subdivide_cyclic_segment=True |
| Alt+C | Set Cyclical State | `grease_pencil.cyclical_set` | type='TOGGLE', subdivide_cyclic_segment=False |
| Ctrl+J | Join Selection | `grease_pencil.join_selection` | type='JOINSTROKES' |
| Ctrl+Shift+J | Join Selection | `grease_pencil.join_selection` | type='SPLITCOPY' |
| Shift+D | Duplicate Strokes | `grease_pencil.duplicate_move` |  |
| Shift+V | Split stroke | `grease_pencil.stroke_split` |  |
| E | Extrude Stroke Points | `grease_pencil.extrude_move` |  |
| Y | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_layer_active' |
| M | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_move_to_layer' |
| Ctrl+Shift+M | Merge | `grease_pencil.layer_merge` | mode='ACTIVE' |
| Shift+Q | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.use_gpencil_edit_lines' |
| Shift+Alt+Q | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.use_gpencil_multiedit_line_only' |
| W | Call Menu | `wm.call_menu` | name='VIEW3D_MT_greasepencil_edit_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_greasepencil_edit_context_menu' |
| Ctrl+G | Call Menu | `wm.call_menu` | name='VIEW3D_MT_greasepencil_vertex_group' |
| Ctrl+Shift+Up Arrow | Reorder | `grease_pencil.reorder` | direction='TOP' |
| Ctrl+Up Arrow (repeat) | Reorder | `grease_pencil.reorder` | direction='UP' |
| Ctrl+Down Arrow (repeat) | Reorder | `grease_pencil.reorder` | direction='DOWN' |
| Ctrl+Shift+Down Arrow | Reorder | `grease_pencil.reorder` | direction='BOTTOM' |
| Numpad * | Isolate Layers | `grease_pencil.layer_isolate` |  |
| 1 | Select Mode | `grease_pencil.set_selection_mode` | mode='POINT' |
| 2 | Select Mode | `grease_pencil.set_selection_mode` | mode='STROKE' |
| 3 | Select Mode | `grease_pencil.set_selection_mode` | mode='SEGMENT' |
| V | Set Handle Type | `grease_pencil.set_handle_type` |  |
| Shift+J | Join Fills | `grease_pencil.join_fills` |  |
| Alt+P | Separate Fills | `grease_pencil.separate_fills` |  |
| Ctrl+E | Grease Pencil Interpolation | `grease_pencil.interpolate` | use_selection=True |
| Ctrl+Shift+E | Interpolate Sequence | `grease_pencil.interpolate_sequence` | use_selection=True |

## Grease Pencil Sculpt Mode

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| Left Mouse | Grease Pencil Sculpt | `grease_pencil.sculpt_paint` |  |
| Ctrl+Left Mouse | Grease Pencil Sculpt | `grease_pencil.sculpt_paint` | mode='INVERT' |
| Shift+Left Mouse | Grease Pencil Sculpt | `grease_pencil.sculpt_paint` | brush_toggle='SMOOTH' |
| 1 | Context Toggle | `wm.context_toggle` | data_path='scene.tool_settings.use_gpencil_select_mask_point' |
| 2 | Context Toggle | `wm.context_toggle` | data_path='scene.tool_settings.use_gpencil_select_mask_stroke' |
| 3 | Context Toggle | `wm.context_toggle` | data_path='scene.tool_settings.use_gpencil_select_mask_segment' |
| Shift+Q | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.use_gpencil_edit_lines' |
| Shift+Alt+Q | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.use_gpencil_multiedit_line_only' |
| I | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_greasepencil_animation' |
| Shift+I | Insert Blank Frame | `grease_pencil.insert_blank_frame` |  |
| Alt+I | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_draw_delete' |
| Shift+Delete | Delete Frame | `grease_pencil.delete_frame` | type='ALL_FRAMES' |
| Ctrl+Shift+M | Merge | `grease_pencil.layer_merge` | mode='ACTIVE' |
| Ctrl+C | Copy Strokes | `grease_pencil.copy` |  |
| Ctrl+V | Paste Strokes | `grease_pencil.paste` |  |
| Ctrl+Shift+V | Paste Strokes | `grease_pencil.paste` | paste_back=True |
| U | Call Menu | `wm.call_menu` | name='VIEW3D_MT_greasepencil_material_active' |
| Y | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_layer_active' |
| Shift+Alt+A | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_grease_pencil_sculpt_automasking_pie' |
| Alt+E | Context Enum Menu | `wm.context_menu_enum` | data_path='tool_settings.gpencil_sculpt_paint.brush.stroke_method' |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.gpencil_sculpt_paint.brush.size', data_path_secondary='tool_settings.gpencil_sculpt_paint.unified_paint_settings.size', use_secondary='tool_settings.gpencil_sculpt_paint.brush.use_unified_size', rotation_path='tool_settings.gpencil_sculpt_paint.brush.texture_slot.angle', color_path='tool_settings.gpencil_sculpt_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.gpencil_sculpt_paint.brush', secondary_tex=False |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.gpencil_sculpt_paint.brush.strength', data_path_secondary='tool_settings.gpencil_sculpt_paint.unified_paint_settings.strength', use_secondary='tool_settings.gpencil_sculpt_paint.brush.use_unified_strength', rotation_path='tool_settings.gpencil_sculpt_paint.brush.texture_slot.angle', color_path='tool_settings.gpencil_sculpt_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.gpencil_sculpt_paint.brush', secondary_tex=False |
| Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_gpencil_sculpt' |
| W | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_sculpt_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_sculpt_context_menu' |

## Grease Pencil Weight Paint

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Paint Weight | `grease_pencil.weight_brush_stroke` |  |
| Ctrl+Left Mouse | Grease Pencil Paint Weight | `grease_pencil.weight_brush_stroke` | mode='INVERT' |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.gpencil_weight_paint.brush.size', data_path_secondary='tool_settings.gpencil_weight_paint.unified_paint_settings.size', use_secondary='tool_settings.gpencil_weight_paint.brush.use_unified_size', rotation_path='tool_settings.gpencil_weight_paint.brush.texture_slot.angle', color_path='tool_settings.gpencil_weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.gpencil_weight_paint.brush', secondary_tex=False |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.gpencil_weight_paint.brush.strength', data_path_secondary='tool_settings.gpencil_weight_paint.unified_paint_settings.strength', use_secondary='tool_settings.gpencil_weight_paint.brush.use_unified_strength', rotation_path='tool_settings.gpencil_weight_paint.brush.texture_slot.angle', color_path='tool_settings.gpencil_weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.gpencil_weight_paint.brush', secondary_tex=False |
| Ctrl+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.gpencil_weight_paint.brush.weight', data_path_secondary='tool_settings.gpencil_weight_paint.unified_paint_settings.weight', use_secondary='tool_settings.gpencil_weight_paint.brush.use_unified_weight', rotation_path='tool_settings.gpencil_weight_paint.brush.texture_slot.angle', color_path='tool_settings.gpencil_weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.gpencil_weight_paint.brush', secondary_tex=False |
| D | Weight Paint Toggle Direction | `grease_pencil.weight_toggle_direction` |  |
| Shift+Q | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.use_gpencil_edit_lines' |
| Shift+Alt+Q | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.use_gpencil_multiedit_line_only' |
| Y | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_layer_active' |
| Ctrl+Shift+M | Merge | `grease_pencil.layer_merge` | mode='ACTIVE' |
| I | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_greasepencil_animation' |
| Shift+I | Insert Blank Frame | `grease_pencil.insert_blank_frame` |  |
| Alt+I | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_draw_delete' |
| Shift+Delete | Delete Frame | `grease_pencil.delete_frame` | type='ALL_FRAMES' |
| Shift+X | Weight Paint Sample Weight | `grease_pencil.weight_sample` |  |
| W | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_weight_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_weight_context_menu' |
| Alt+H | Show All Layers | `grease_pencil.layer_reveal` |  |
| H | Hide Layer(s) | `grease_pencil.layer_hide` | unselected=False |
| Shift+H | Hide Layer(s) | `grease_pencil.layer_hide` | unselected=True |
| Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_gpencil_weight' |

## Grease Pencil Vertex Paint

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Paint Vertex | `grease_pencil.vertex_brush_stroke` |  |
| Ctrl+Left Mouse | Grease Pencil Paint Vertex | `grease_pencil.vertex_brush_stroke` | mode='INVERT' |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| 1 | Context Toggle | `wm.context_toggle` | data_path='scene.tool_settings.use_gpencil_vertex_select_mask_point' |
| 2 | Context Toggle | `wm.context_toggle` | data_path='scene.tool_settings.use_gpencil_vertex_select_mask_stroke' |
| 3 | Context Toggle | `wm.context_toggle` | data_path='scene.tool_settings.use_gpencil_vertex_select_mask_segment' |
| X | Swap Colors | `paint.brush_colors_flip` |  |
| Shift+X | Sample Color | `paint.sample_color` | merged=False |
| Shift+Q | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.use_gpencil_edit_lines' |
| Shift+Alt+Q | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.use_gpencil_multiedit_line_only' |
| Y | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_layer_active' |
| Ctrl+Shift+M | Merge | `grease_pencil.layer_merge` | mode='ACTIVE' |
| I | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_greasepencil_animation' |
| Shift+I | Insert Blank Frame | `grease_pencil.insert_blank_frame` |  |
| Alt+I | Call Menu | `wm.call_menu` | name='GREASE_PENCIL_MT_draw_delete' |
| Shift+Delete | Delete Frame | `grease_pencil.delete_frame` | type='ALL_FRAMES' |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.gpencil_vertex_paint.brush.size', data_path_secondary='tool_settings.gpencil_vertex_paint.unified_paint_settings.size', use_secondary='tool_settings.gpencil_vertex_paint.brush.use_unified_size', rotation_path='tool_settings.gpencil_vertex_paint.brush.texture_slot.angle', color_path='tool_settings.gpencil_vertex_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.gpencil_vertex_paint.brush', secondary_tex=False |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.gpencil_vertex_paint.brush.strength', data_path_secondary='tool_settings.gpencil_vertex_paint.unified_paint_settings.strength', use_secondary='tool_settings.gpencil_vertex_paint.brush.use_unified_strength', rotation_path='tool_settings.gpencil_vertex_paint.brush.texture_slot.angle', color_path='tool_settings.gpencil_vertex_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.gpencil_vertex_paint.brush', secondary_tex=False |
| W | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_vertex_paint_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_vertex_paint_context_menu' |
| Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_gpencil_vertex' |

## Grease Pencil Brush Stroke

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Draw | `grease_pencil.brush_stroke` |  |
| Ctrl+Left Mouse | Grease Pencil Draw | `grease_pencil.brush_stroke` | brush_toggle='ERASE' |
| Shift+Left Mouse | Grease Pencil Draw | `grease_pencil.brush_stroke` | brush_toggle='SMOOTH' |
| Eraser | Grease Pencil Draw | `grease_pencil.brush_stroke` | brush_toggle='ERASE' |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |

## Grease Pencil Fill Tool

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Fill | `grease_pencil.fill` |  |
| Ctrl+Left Mouse | Grease Pencil Fill | `grease_pencil.fill` | invert=True |
| Alt+Left Mouse | Grease Pencil Draw | `grease_pencil.brush_stroke` |  |

## View3D Placement Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Left Alt | PIVOT_CENTER_ON | `PIVOT_CENTER_ON` |  |
| Any modifier+Left Alt release | PIVOT_CENTER_OFF | `PIVOT_CENTER_OFF` |  |
| Any modifier+Right Alt | PIVOT_CENTER_ON | `PIVOT_CENTER_ON` |  |
| Any modifier+Right Alt release | PIVOT_CENTER_OFF | `PIVOT_CENTER_OFF` |  |
| Any modifier+Left Shift | FIXED_ASPECT_ON | `FIXED_ASPECT_ON` |  |
| Any modifier+Left Shift release | FIXED_ASPECT_OFF | `FIXED_ASPECT_OFF` |  |
| Any modifier+Right Shift | FIXED_ASPECT_ON | `FIXED_ASPECT_ON` |  |
| Any modifier+Right Shift release | FIXED_ASPECT_OFF | `FIXED_ASPECT_OFF` |  |
| Any modifier+Left Ctrl | SNAP_ON | `SNAP_ON` |  |
| Any modifier+Left Ctrl release | SNAP_OFF | `SNAP_OFF` |  |
| Any modifier+Right Ctrl | SNAP_ON | `SNAP_ON` |  |
| Any modifier+Right Ctrl release | SNAP_OFF | `SNAP_OFF` |  |

## View3D Gesture Circle

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse any | CANCEL | `CANCEL` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Numpad Enter | CONFIRM | `CONFIRM` |  |
| Left Mouse | SELECT | `SELECT` |  |
| Shift+Left Mouse | DESELECT | `DESELECT` |  |
| Any modifier+Left Mouse release | NOP | `NOP` |  |
| Middle Mouse | DESELECT | `DESELECT` |  |
| Any modifier+Middle Mouse release | NOP | `NOP` |  |
| Wheel Up | SUBTRACT | `SUBTRACT` |  |
| Numpad - (repeat) | SUBTRACT | `SUBTRACT` |  |
| Wheel Down | ADD | `ADD` |  |
| Numpad + (repeat) | ADD | `ADD` |  |
| Mouse/Trackpad Pan any | SIZE | `SIZE` |  |

## Gesture Box

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse release | SELECT | `SELECT` |  |
| Shift+Left Mouse | BEGIN | `BEGIN` |  |
| Shift+Left Mouse release | DESELECT | `DESELECT` |  |
| Left Mouse | BEGIN | `BEGIN` |  |
| Any modifier+Left Mouse release | SELECT | `SELECT` |  |
| Middle Mouse | BEGIN | `BEGIN` |  |
| Middle Mouse release | DESELECT | `DESELECT` |  |
| Any modifier+Space Bar any | MOVE | `MOVE` |  |

## Gesture Zoom Border

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse any | CANCEL | `CANCEL` |  |
| Left Mouse | BEGIN | `BEGIN` |  |
| Left Mouse release | IN | `IN` |  |
| Middle Mouse | BEGIN | `BEGIN` |  |
| Middle Mouse release | OUT | `OUT` |  |

## Gesture Straight Line

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse any | CANCEL | `CANCEL` |  |
| Left Mouse | BEGIN | `BEGIN` |  |
| Any modifier+Left Mouse release | SELECT | `SELECT` |  |
| Any modifier+Space Bar any | MOVE | `MOVE` |  |
| Any modifier+Left Ctrl any | SNAP | `SNAP` |  |
| Any modifier+F | FLIP | `FLIP` |  |

## Gesture Lasso

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Space Bar any | MOVE | `MOVE` |  |

## Gesture Polyline

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Left Mouse double click | CONFIRM | `CONFIRM` |  |
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse any | CANCEL | `CANCEL` |  |
| Any modifier+Left Mouse | SELECT | `SELECT` |  |
| Any modifier+Space Bar any | MOVE | `MOVE` |  |

## Standard Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Left Mouse any | APPLY | `APPLY` |  |
| Any modifier+Return | APPLY | `APPLY` |  |
| Any modifier+Numpad Enter | APPLY | `APPLY` |  |
| Any modifier+Left Ctrl | SNAP | `SNAP` |  |
| Any modifier+Left Ctrl release | SNAP_OFF | `SNAP_OFF` |  |
| Any modifier+Right Ctrl | SNAP | `SNAP` |  |
| Any modifier+Right Ctrl release | SNAP_OFF | `SNAP_OFF` |  |

## Custom Normals Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Left Mouse | CONFIRM | `CONFIRM` |  |
| R | RESET | `RESET` |  |
| I | INVERT | `INVERT` |  |
| S | SPHERIZE | `SPHERIZE` |  |
| A | ALIGN | `ALIGN` |  |
| M | USE_MOUSE | `USE_MOUSE` |  |
| L | USE_PIVOT | `USE_PIVOT` |  |
| O | USE_OBJECT | `USE_OBJECT` |  |
| Ctrl+Left Mouse click | SET_USE_3DCURSOR | `SET_USE_3DCURSOR` |  |
| Ctrl+Right Mouse click | SET_USE_SELECTED | `SET_USE_SELECTED` |  |

## Bevel Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Any modifier+Left Mouse | CONFIRM | `CONFIRM` |  |
| Any modifier+A | VALUE_OFFSET | `VALUE_OFFSET` |  |
| Any modifier+P | VALUE_PROFILE | `VALUE_PROFILE` |  |
| Any modifier+S | VALUE_SEGMENTS | `VALUE_SEGMENTS` |  |
| Any modifier+Wheel Up | SEGMENTS_UP | `SEGMENTS_UP` |  |
| Any modifier+Numpad + | SEGMENTS_UP | `SEGMENTS_UP` |  |
| Any modifier+Wheel Down | SEGMENTS_DOWN | `SEGMENTS_DOWN` |  |
| Any modifier+Numpad - | SEGMENTS_DOWN | `SEGMENTS_DOWN` |  |
| Any modifier+M | OFFSET_MODE_CHANGE | `OFFSET_MODE_CHANGE` |  |
| Any modifier+C | CLAMP_OVERLAP_TOGGLE | `CLAMP_OVERLAP_TOGGLE` |  |
| Any modifier+V | AFFECT_CHANGE | `AFFECT_CHANGE` |  |
| Any modifier+H | HARDEN_NORMALS_TOGGLE | `HARDEN_NORMALS_TOGGLE` |  |
| Any modifier+U | MARK_SEAM_TOGGLE | `MARK_SEAM_TOGGLE` |  |
| Any modifier+K | MARK_SHARP_TOGGLE | `MARK_SHARP_TOGGLE` |  |
| Any modifier+O | OUTER_MITER_CHANGE | `OUTER_MITER_CHANGE` |  |
| Any modifier+I | INNER_MITER_CHANGE | `INNER_MITER_CHANGE` |  |
| Any modifier+Z | PROFILE_TYPE_CHANGE | `PROFILE_TYPE_CHANGE` |  |
| Any modifier+N | VERTEX_MESH_CHANGE | `VERTEX_MESH_CHANGE` |  |
| Any modifier+Left Ctrl | SNAP_ON | `SNAP_ON` |  |
| Any modifier+Right Ctrl | SNAP_ON | `SNAP_ON` |  |
| Any modifier+Left Ctrl release | SNAP_OFF | `SNAP_OFF` |  |
| Any modifier+Right Ctrl release | SNAP_OFF | `SNAP_OFF` |  |
| Any modifier+Left Shift | PRECISION_ON | `PRECISION_ON` |  |
| Any modifier+Left Shift release | PRECISION_OFF | `PRECISION_OFF` |  |
| Any modifier+Right Shift | PRECISION_ON | `PRECISION_ON` |  |
| Any modifier+Right Shift release | PRECISION_OFF | `PRECISION_OFF` |  |

## Transform Axis Target Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Right Mouse any | CANCEL | `CANCEL` |  |
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Left Mouse any | CONFIRM | `CONFIRM` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Any modifier+Left Ctrl | TRANSLATE_ENABLE | `TRANSLATE_ENABLE` |  |
| Any modifier+Left Ctrl release | TRANSLATE_DISABLE | `TRANSLATE_DISABLE` |  |
| Any modifier+Right Ctrl | TRANSLATE_ENABLE | `TRANSLATE_ENABLE` |  |
| Any modifier+Right Ctrl release | TRANSLATE_DISABLE | `TRANSLATE_DISABLE` |  |

## View3D Fly Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Right Mouse any | CANCEL | `CANCEL` |  |
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Left Mouse any | CONFIRM | `CONFIRM` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Space Bar | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Mouse/Trackpad Pan any | CONFIRM | `CONFIRM` |  |
| W (repeat) | FORWARD | `FORWARD` |  |
| Up Arrow (repeat) | FORWARD | `FORWARD` |  |
| S (repeat) | BACKWARD | `BACKWARD` |  |
| Down Arrow (repeat) | BACKWARD | `BACKWARD` |  |
| A (repeat) | LEFT | `LEFT` |  |
| Left Arrow (repeat) | LEFT | `LEFT` |  |
| D (repeat) | RIGHT | `RIGHT` |  |
| Right Arrow (repeat) | RIGHT | `RIGHT` |  |
| E (repeat) | UP | `UP` |  |
| R (repeat) | UP | `UP` |  |
| Q (repeat) | DOWN | `DOWN` |  |
| F (repeat) | DOWN | `DOWN` |  |
| Any modifier+Numpad + (repeat) | ACCELERATE | `ACCELERATE` |  |
| Any modifier+Numpad - (repeat) | DECELERATE | `DECELERATE` |  |
| Any modifier+Wheel Up | ACCELERATE | `ACCELERATE` |  |
| Any modifier+Wheel Down | DECELERATE | `DECELERATE` |  |
| Any modifier+Middle Mouse | PAN_ENABLE | `PAN_ENABLE` |  |
| Any modifier+Middle Mouse release | PAN_DISABLE | `PAN_DISABLE` |  |
| X | AXIS_LOCK_X | `AXIS_LOCK_X` |  |
| Z | AXIS_LOCK_Z | `AXIS_LOCK_Z` |  |
| Any modifier+Left Alt | PRECISION_ENABLE | `PRECISION_ENABLE` |  |
| Any modifier+Left Alt release | PRECISION_DISABLE | `PRECISION_DISABLE` |  |
| Any modifier+Right Alt | PRECISION_ENABLE | `PRECISION_ENABLE` |  |
| Any modifier+Right Alt release | PRECISION_DISABLE | `PRECISION_DISABLE` |  |
| Any modifier+Left Shift | PRECISION_ENABLE | `PRECISION_ENABLE` |  |
| Any modifier+Left Shift release | PRECISION_DISABLE | `PRECISION_DISABLE` |  |
| Any modifier+Right Shift | PRECISION_ENABLE | `PRECISION_ENABLE` |  |
| Any modifier+Right Shift release | PRECISION_DISABLE | `PRECISION_DISABLE` |  |
| Any modifier+Left Ctrl | FREELOOK_ENABLE | `FREELOOK_ENABLE` |  |
| Any modifier+Left Ctrl release | FREELOOK_DISABLE | `FREELOOK_DISABLE` |  |
| Any modifier+Right Ctrl | FREELOOK_ENABLE | `FREELOOK_ENABLE` |  |
| Any modifier+Right Ctrl release | FREELOOK_DISABLE | `FREELOOK_DISABLE` |  |

## View3D Walk Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Right Mouse any | CANCEL | `CANCEL` |  |
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Left Mouse any | CONFIRM | `CONFIRM` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Any modifier+W | FORWARD | `FORWARD` |  |
| Any modifier+W release | FORWARD_STOP | `FORWARD_STOP` |  |
| Up Arrow | FORWARD | `FORWARD` |  |
| Any modifier+Up Arrow release | FORWARD_STOP | `FORWARD_STOP` |  |
| Any modifier+S | BACKWARD | `BACKWARD` |  |
| Any modifier+S release | BACKWARD_STOP | `BACKWARD_STOP` |  |
| Down Arrow | BACKWARD | `BACKWARD` |  |
| Any modifier+Down Arrow release | BACKWARD_STOP | `BACKWARD_STOP` |  |
| Any modifier+A | LEFT | `LEFT` |  |
| Any modifier+A release | LEFT_STOP | `LEFT_STOP` |  |
| Left Arrow | LEFT | `LEFT` |  |
| Any modifier+Left Arrow release | LEFT_STOP | `LEFT_STOP` |  |
| Any modifier+D | RIGHT | `RIGHT` |  |
| Any modifier+D release | RIGHT_STOP | `RIGHT_STOP` |  |
| Right Arrow | RIGHT | `RIGHT` |  |
| Any modifier+Right Arrow release | RIGHT_STOP | `RIGHT_STOP` |  |
| Any modifier+E | UP | `UP` |  |
| Any modifier+E release | UP_STOP | `UP_STOP` |  |
| Any modifier+Q | DOWN | `DOWN` |  |
| Any modifier+Q release | DOWN_STOP | `DOWN_STOP` |  |
| Any modifier+R | LOCAL_UP | `LOCAL_UP` |  |
| Any modifier+R release | LOCAL_UP_STOP | `LOCAL_UP_STOP` |  |
| Any modifier+F | LOCAL_DOWN | `LOCAL_DOWN` |  |
| Any modifier+F release | LOCAL_DOWN_STOP | `LOCAL_DOWN_STOP` |  |
| Any modifier+V | JUMP | `JUMP` |  |
| Any modifier+V release | JUMP_STOP | `JUMP_STOP` |  |
| Any modifier+. | INCREASE_JUMP | `INCREASE_JUMP` |  |
| Any modifier+, | DECREASE_JUMP | `DECREASE_JUMP` |  |
| Any modifier+Space Bar | TELEPORT | `TELEPORT` |  |
| Any modifier+Middle Mouse any | TELEPORT | `TELEPORT` |  |
| Any modifier+Left Shift | FAST_ENABLE | `FAST_ENABLE` |  |
| Any modifier+Left Shift release | FAST_DISABLE | `FAST_DISABLE` |  |
| Any modifier+Right Shift | FAST_ENABLE | `FAST_ENABLE` |  |
| Any modifier+Right Shift release | FAST_DISABLE | `FAST_DISABLE` |  |
| Any modifier+Left Alt | SLOW_ENABLE | `SLOW_ENABLE` |  |
| Any modifier+Left Alt release | SLOW_DISABLE | `SLOW_DISABLE` |  |
| Any modifier+Right Alt | SLOW_ENABLE | `SLOW_ENABLE` |  |
| Any modifier+Right Alt release | SLOW_DISABLE | `SLOW_DISABLE` |  |
| Tab | GRAVITY_TOGGLE | `GRAVITY_TOGGLE` |  |
| G | GRAVITY_TOGGLE | `GRAVITY_TOGGLE` |  |
| Any modifier+Numpad + (repeat) | ACCELERATE | `ACCELERATE` |  |
| Any modifier+Numpad - (repeat) | DECELERATE | `DECELERATE` |  |
| Any modifier+Wheel Up | ACCELERATE | `ACCELERATE` |  |
| Any modifier+Wheel Down | DECELERATE | `DECELERATE` |  |
| Z | AXIS_LOCK_Z | `AXIS_LOCK_Z` |  |

## View3D Rotate Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Left Alt | AXIS_SNAP_ENABLE | `AXIS_SNAP_ENABLE` |  |
| Any modifier+Left Alt release | AXIS_SNAP_DISABLE | `AXIS_SNAP_DISABLE` |  |
| Any modifier+Right Alt | AXIS_SNAP_ENABLE | `AXIS_SNAP_ENABLE` |  |
| Any modifier+Right Alt release | AXIS_SNAP_DISABLE | `AXIS_SNAP_DISABLE` |  |

## View3D Move Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |

## View3D Zoom Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |

## View3D Dolly Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |

## View3D VR Location Scouting Capture Review Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | EXIT | `EXIT` |  |
| Any modifier+Right Mouse | EXIT | `EXIT` |  |
| Up Arrow | PREVIOUS | `PREVIOUS` |  |
| Down Arrow | NEXT | `NEXT` |  |
| C | ADD_CAMERA | `ADD_CAMERA` |  |
| M | ADD_MARKER | `ADD_MARKER` |  |

## Paint Stroke Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |

## Sculpt Expand Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Left Mouse | CONFIRM | `CONFIRM` |  |
| Any modifier+Left Mouse release | CONFIRM | `CONFIRM` |  |
| Any modifier+F | INVERT | `INVERT` |  |
| Any modifier+E | PRESERVE | `PRESERVE` |  |
| Any modifier+G | GRADIENT | `GRADIENT` |  |
| R | RECURSION_STEP_GEODESIC | `RECURSION_STEP_GEODESIC` |  |
| Alt+R | RECURSION_STEP_TOPOLOGY | `RECURSION_STEP_TOPOLOGY` |  |
| Any modifier+Space Bar any | MOVE_TOGGLE | `MOVE_TOGGLE` |  |
| Any modifier+1 | FALLOFF_GEODESICS | `FALLOFF_GEODESICS` |  |
| Any modifier+2 | FALLOFF_TOPOLOGY | `FALLOFF_TOPOLOGY` |  |
| Any modifier+3 | FALLOFF_TOPOLOGY_DIAGONALS | `FALLOFF_TOPOLOGY_DIAGONALS` |  |
| Any modifier+4 | FALLOFF_SPHERICAL | `FALLOFF_SPHERICAL` |  |
| Any modifier+Numpad 1 | FALLOFF_GEODESICS | `FALLOFF_GEODESICS` |  |
| Any modifier+Numpad 2 | FALLOFF_TOPOLOGY | `FALLOFF_TOPOLOGY` |  |
| Any modifier+Numpad 3 | FALLOFF_TOPOLOGY_DIAGONALS | `FALLOFF_TOPOLOGY_DIAGONALS` |  |
| Any modifier+Numpad 4 | FALLOFF_SPHERICAL | `FALLOFF_SPHERICAL` |  |
| Left Ctrl any | SNAP_TOGGLE | `SNAP_TOGGLE` |  |
| Right Ctrl any | SNAP_TOGGLE | `SNAP_TOGGLE` |  |
| Any modifier+W (repeat) | LOOP_COUNT_INCREASE | `LOOP_COUNT_INCREASE` |  |
| Any modifier+Q (repeat) | LOOP_COUNT_DECREASE | `LOOP_COUNT_DECREASE` |  |
| Any modifier+B | BRUSH_GRADIENT_TOGGLE | `BRUSH_GRADIENT_TOGGLE` |  |
| Y | TEXTURE_DISTORTION_INCREASE | `TEXTURE_DISTORTION_INCREASE` |  |
| T | TEXTURE_DISTORTION_DECREASE | `TEXTURE_DISTORTION_DECREASE` |  |

## Mesh Filter Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Left Mouse | CONFIRM | `CONFIRM` |  |
| Any modifier+Left Mouse release | CONFIRM | `CONFIRM` |  |
| Any modifier+Return release | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter release | CONFIRM | `CONFIRM` |  |
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |

## Curve Pen Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Left Shift any | FREE_ALIGN_TOGGLE | `FREE_ALIGN_TOGGLE` |  |
| Any modifier+Left Ctrl any | MOVE_ADJACENT | `MOVE_ADJACENT` |  |
| Any modifier+Space Bar any | MOVE_ENTIRE | `MOVE_ENTIRE` |  |
| Any modifier+Left Alt any | LOCK_ANGLE | `LOCK_ANGLE` |  |
| Any modifier+Right Ctrl | LINK_HANDLES | `LINK_HANDLES` |  |

## Pen Tool Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Left Ctrl any | MOVE_HANDLE | `MOVE_HANDLE` |  |
| Any modifier+Left Alt any | MOVE_ENTIRE | `MOVE_ENTIRE` |  |
| Any modifier+Left Shift any | SNAP_ANGLE | `SNAP_ANGLE` |  |

## Node Link Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Left Mouse | BEGIN | `BEGIN` |  |
| Any modifier+Left Mouse release | CONFIRM | `CONFIRM` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Left Alt any | SWAP | `SWAP` |  |
| Any modifier+Right Alt any | SWAP | `SWAP` |  |

## Node Resize Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Left Mouse | BEGIN | `BEGIN` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Ctrl | SNAP_INVERT_ON | `SNAP_INVERT_ON` |  |
| Any modifier+Right Ctrl release | SNAP_INVERT_OFF | `SNAP_INVERT_OFF` |  |
| Any modifier+Left Ctrl | SNAP_INVERT_ON | `SNAP_INVERT_ON` |  |
| Any modifier+Left Ctrl release | SNAP_INVERT_OFF | `SNAP_INVERT_OFF` |  |

## Primitive Tool Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Q | CANCEL | `CANCEL` |  |
| Shift+Middle Mouse any | PANNING | `PANNING` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Middle Mouse | CONFIRM | `CONFIRM` |  |
| E | EXTRUDE | `EXTRUDE` |  |
| G | GRAB | `GRAB` |  |
| R | ROTATE | `ROTATE` |  |
| S | SCALE | `SCALE` |  |
| Up Arrow (repeat) | INCREASE_SUBDIVISION | `INCREASE_SUBDIVISION` |  |
| Down Arrow (repeat) | DECREASE_SUBDIVISION | `DECREASE_SUBDIVISION` |  |
| F | CHANGE_RADIUS | `CHANGE_RADIUS` |  |
| Shift+F | CHANGE_OPACITY | `CHANGE_OPACITY` |  |

## Fill Tool Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Left Mouse | CONFIRM | `CONFIRM` |  |
| S | EXTENSION_MODE_TOGGLE | `EXTENSION_MODE_TOGGLE` |  |
| Page Up (repeat) | EXTENSION_LENGTHEN | `EXTENSION_LENGTHEN` |  |
| Wheel Down | EXTENSION_LENGTHEN | `EXTENSION_LENGTHEN` |  |
| Page Down (repeat) | EXTENSION_SHORTEN | `EXTENSION_SHORTEN` |  |
| Wheel Up | EXTENSION_SHORTEN | `EXTENSION_SHORTEN` |  |
| Middle Mouse | EXTENSION_DRAG | `EXTENSION_DRAG` |  |
| D | EXTENSION_COLLIDE | `EXTENSION_COLLIDE` |  |
| Any modifier+Left Ctrl any | INVERT | `INVERT` |  |
| Any modifier+Right Ctrl any | INVERT | `INVERT` |  |
| Any modifier+Left Shift any | PRECISION | `PRECISION` |  |
| Any modifier+Right Shift any | PRECISION | `PRECISION` |  |

## Interpolate Tool Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Any modifier+Left Mouse release | CONFIRM | `CONFIRM` |  |
| Wheel Up | INCREASE | `INCREASE` |  |
| Wheel Down | DECREASE | `DECREASE` |  |

## Slip Modal

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Left Mouse | CONFIRM | `CONFIRM` |  |
| Any modifier+Left Mouse release | CONFIRM | `CONFIRM` |  |
| Any modifier+Return release | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter release | CONFIRM | `CONFIRM` |  |
| Any modifier+Space Bar release | CONFIRM | `CONFIRM` |  |
| Any modifier+Right Mouse any | CANCEL | `CANCEL` |  |
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Left Shift | PRECISION_ENABLE | `PRECISION_ENABLE` |  |
| Any modifier+Left Shift release | PRECISION_DISABLE | `PRECISION_DISABLE` |  |
| Any modifier+Right Shift | PRECISION_ENABLE | `PRECISION_ENABLE` |  |
| Any modifier+Right Shift release | PRECISION_DISABLE | `PRECISION_DISABLE` |  |
| Any modifier+C | CLAMP_TOGGLE | `CLAMP_TOGGLE` |  |

## Generic Gizmo

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| [Ctrl]+[Shift]+[OS]+[Hyper]+Left Mouse | Gizmo Tweak | `gizmogroup.gizmo_tweak` |  |

## Generic Gizmo Click Drag

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| [Ctrl]+[Shift]+[OS]+[Hyper]+Left Mouse click | Gizmo Tweak | `gizmogroup.gizmo_tweak` |  |
| [Ctrl]+[Shift]+[OS]+[Hyper]+Left Mouse drag | Gizmo Tweak | `gizmogroup.gizmo_tweak` |  |

## Generic Gizmo Select

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| [Ctrl]+[Shift]+[OS]+[Hyper]+Left Mouse | Gizmo Tweak | `gizmogroup.gizmo_tweak` |  |

## Generic Gizmo Tweak Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Right Mouse | CANCEL | `CANCEL` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Any modifier+Right Shift | PRECISION_ON | `PRECISION_ON` |  |
| Any modifier+Right Shift release | PRECISION_OFF | `PRECISION_OFF` |  |
| Any modifier+Left Shift | PRECISION_ON | `PRECISION_ON` |  |
| Any modifier+Left Shift release | PRECISION_OFF | `PRECISION_OFF` |  |
| Any modifier+Right Ctrl | SNAP_ON | `SNAP_ON` |  |
| Any modifier+Right Ctrl release | SNAP_OFF | `SNAP_OFF` |  |
| Any modifier+Left Ctrl | SNAP_ON | `SNAP_ON` |  |
| Any modifier+Left Ctrl release | SNAP_OFF | `SNAP_OFF` |  |

## Toolbar Popup

Space `EMPTY`, region `TEMPORARY`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Space Bar | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.cursor' |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select' |
| L | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_lasso' |
| T | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.transform' |
| M | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.measure' |

## Generic Tool: Annotate

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW', wait_for_input=False |
| Ctrl+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |
| Middle Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW', wait_for_input=False |
| Ctrl+Middle Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |

## Generic Tool: Annotate Line

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Annotation Draw | `gpencil.annotate` | mode='DRAW_STRAIGHT', wait_for_input=False |
| Ctrl+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |
| Middle Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW_STRAIGHT', wait_for_input=False |
| Ctrl+Middle Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |

## Generic Tool: Annotate Polygon

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW_POLY', wait_for_input=False |
| Ctrl+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |
| Middle Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW_POLY', wait_for_input=False |
| Ctrl+Middle Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |

## Generic Tool: Annotate Eraser

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |
| Ctrl+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |
| Middle Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |
| Ctrl+Middle Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |

## Image Editor Tool: Sample

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Sample Color | `image.sample` |  |
| Middle Mouse | Sample Color | `image.sample` |  |

## Image Editor Tool: Uv, Cursor

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set 2D Cursor | `uv.cursor_set` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |
| Middle Mouse | Set 2D Cursor | `uv.cursor_set` |  |
| Middle Mouse | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## Image Editor Tool: Uv, Select Box

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `uv.select_box` |  |
| Shift+Left Mouse drag | Box Select | `uv.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `uv.select_box` | mode='SUB' |

## Image Editor Tool: Uv, Select Box (fallback)

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `uv.select_box` |  |
| Shift+Left Mouse drag | Box Select | `uv.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `uv.select_box` | mode='SUB' |

## Image Editor Tool: Uv, Select Circle

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `uv.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `uv.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `uv.select_circle` | wait_for_input=False, mode='SUB' |

## Image Editor Tool: Uv, Select Circle (fallback)

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `uv.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `uv.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `uv.select_circle` | wait_for_input=False, mode='SUB' |

## Image Editor Tool: Uv, Select Lasso

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select UV | `uv.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select UV | `uv.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select UV | `uv.select_lasso` | mode='SUB' |

## Image Editor Tool: Uv, Select Lasso (fallback)

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select UV | `uv.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select UV | `uv.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select UV | `uv.select_lasso` | mode='SUB' |

## Image Editor Tool: Uv, Rip Region

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rip Move UVs | `uv.rip_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Middle Mouse | Rip Move UVs | `uv.rip_move` | TRANSFORM_OT_translate={release_confirm=True} |

## Image Editor Tool: Uv, Grab

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grab UVs | `sculpt.uv_sculpt_grab` |  |
| Ctrl+Left Mouse | Grab UVs | `sculpt.uv_sculpt_grab` | use_invert=True |
| Shift+Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.size' |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.strength' |
| Middle Mouse | Grab UVs | `sculpt.uv_sculpt_grab` |  |
| Ctrl+Middle Mouse | Grab UVs | `sculpt.uv_sculpt_grab` | use_invert=True |
| Shift+Middle Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |

## Image Editor Tool: Uv, Relax

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |
| Ctrl+Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` | use_invert=True |
| Shift+Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.size' |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.strength' |
| Middle Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |
| Ctrl+Middle Mouse | Relax UVs | `sculpt.uv_sculpt_relax` | use_invert=True |
| Shift+Middle Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |

## Image Editor Tool: Uv, Pinch

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Pinch UVs | `sculpt.uv_sculpt_pinch` |  |
| Ctrl+Left Mouse | Pinch UVs | `sculpt.uv_sculpt_pinch` | use_invert=True |
| Shift+Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.size' |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.strength' |
| Middle Mouse | Pinch UVs | `sculpt.uv_sculpt_pinch` |  |
| Ctrl+Middle Mouse | Pinch UVs | `sculpt.uv_sculpt_pinch` | use_invert=True |
| Shift+Middle Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |

## Image Editor Tool: Uv, Move

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |
| Middle Mouse | Move | `transform.translate` | release_confirm=True |

## Image Editor Tool: Uv, Rotate

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rotate | `transform.rotate` | release_confirm=True |
| Middle Mouse | Rotate | `transform.rotate` | release_confirm=True |

## Image Editor Tool: Uv, Scale

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |
| Middle Mouse | Resize | `transform.resize` | release_confirm=True |

## Image Editor Tool: Mask, Cursor

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set 2D Cursor | `uv.cursor_set` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |
| Middle Mouse | Set 2D Cursor | `uv.cursor_set` |  |
| Middle Mouse | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## Image Editor Tool: Mask, Tweak

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `mask.select` | deselect_all=True, select_passthrough=True |
| Left Mouse click | Select | `mask.select` | deselect_all=True |
| Shift+Left Mouse | Select | `mask.select` | deselect_all=False, toggle=True |

## Image Editor Tool: Mask, Select Box

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `mask.select_box` |  |
| Shift+Left Mouse drag | Box Select | `mask.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `mask.select_box` | mode='SUB' |

## Image Editor Tool: Mask, Select Box (fallback)

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `mask.select_box` |  |
| Shift+Left Mouse drag | Box Select | `mask.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `mask.select_box` | mode='SUB' |

## Image Editor Tool: Mask, Select Circle

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `mask.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `mask.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `mask.select_circle` | wait_for_input=False, mode='SUB' |

## Image Editor Tool: Mask, Select Circle (fallback)

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `mask.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `mask.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `mask.select_circle` | wait_for_input=False, mode='SUB' |

## Image Editor Tool: Mask, Select Lasso

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `mask.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `mask.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `mask.select_lasso` | mode='SUB' |

## Image Editor Tool: Mask, Select Lasso (fallback)

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `mask.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `mask.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `mask.select_lasso` | mode='SUB' |

## Image Editor Tool: Mask, Move

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |
| Middle Mouse | Move | `transform.translate` | release_confirm=True |

## Image Editor Tool: Mask, Rotate

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rotate | `transform.rotate` | release_confirm=True |
| Middle Mouse | Rotate | `transform.rotate` | release_confirm=True |

## Image Editor Tool: Mask, Scale

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |
| Middle Mouse | Resize | `transform.resize` | release_confirm=True |

## Image Editor Tool: Mask, Transform

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |
| Middle Mouse | Resize | `transform.resize` | release_confirm=True |

## Image Editor Tool: Mask, Circle

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Add Circle | `mask.primitive_circle_add` |  |
| Middle Mouse | Add Circle | `mask.primitive_circle_add` |  |

## Image Editor Tool: Mask, Box

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Add Square | `mask.primitive_square_add` |  |
| Middle Mouse | Add Square | `mask.primitive_square_add` |  |

## Node Tool: Select Box

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `node.select_box` | tweak=True |
| Shift+Left Mouse drag | Box Select | `node.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `node.select_box` | tweak=True, mode='SUB' |

## Node Tool: Select Box (fallback)

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `node.select_box` | tweak=True |
| Shift+Left Mouse drag | Box Select | `node.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `node.select_box` | tweak=True, mode='SUB' |

## Node Tool: Select Lasso

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `node.select_lasso` | tweak=True |
| Shift+Left Mouse drag | Lasso Select | `node.select_lasso` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `node.select_lasso` | tweak=True, mode='SUB' |

## Node Tool: Select Lasso (fallback)

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `node.select_lasso` | tweak=True |
| Shift+Left Mouse drag | Lasso Select | `node.select_lasso` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `node.select_lasso` | tweak=True, mode='SUB' |

## Node Tool: Select Circle

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `node.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `node.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `node.select_circle` | wait_for_input=False, mode='SUB' |

## Node Tool: Select Circle (fallback)

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `node.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `node.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `node.select_circle` | wait_for_input=False, mode='SUB' |

## Node Tool: Links Cut

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Cut Links | `node.links_cut` |  |
| Middle Mouse | Cut Links | `node.links_cut` |  |

## Node Tool: Mute Links

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mute Links | `node.links_mute` |  |
| Middle Mouse | Mute Links | `node.links_mute` |  |

## Node Tool: Add Reroute

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Add Reroute | `node.add_reroute` |  |
| Middle Mouse | Add Reroute | `node.add_reroute` |  |

## 3D View Tool: Cursor

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set 3D Cursor | `view3d.cursor3d` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |
| Middle Mouse | Set 3D Cursor | `view3d.cursor3d` |  |
| Middle Mouse | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## 3D View Tool: Edit Text, Select Text

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set Selection | `font.selection_set` |  |
| Left Mouse double click | Select Word | `font.select_word` |  |
| Middle Mouse | Set Selection | `font.selection_set` |  |
| Middle Mouse | Select Word | `font.select_word` |  |

## 3D View Tool: Select Box

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `view3d.select_box` |  |
| Shift+Left Mouse drag | Box Select | `view3d.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `view3d.select_box` | mode='SUB' |
| Ctrl+Shift+Left Mouse drag | Box Select | `view3d.select_box` | mode='AND' |

## 3D View Tool: Select Box (fallback)

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `view3d.select_box` |  |
| Shift+Left Mouse drag | Box Select | `view3d.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `view3d.select_box` | mode='SUB' |
| Ctrl+Shift+Left Mouse drag | Box Select | `view3d.select_box` | mode='AND' |

## 3D View Tool: Select Circle

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `view3d.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `view3d.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `view3d.select_circle` | wait_for_input=False, mode='SUB' |

## 3D View Tool: Select Circle (fallback)

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `view3d.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `view3d.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `view3d.select_circle` | wait_for_input=False, mode='SUB' |

## 3D View Tool: Select Lasso

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `view3d.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='SUB' |
| Ctrl+Shift+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='AND' |

## 3D View Tool: Select Lasso (fallback)

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `view3d.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='SUB' |
| Ctrl+Shift+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='AND' |

## 3D View Tool: Transform

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Transform from Gizmo | `transform.from_gizmo` |  |
| Middle Mouse | Transform from Gizmo | `transform.from_gizmo` |  |

## 3D View Tool: Move

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |
| Middle Mouse | Move | `transform.translate` | release_confirm=True |

## 3D View Tool: Rotate

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rotate | `transform.rotate` | release_confirm=True |
| Middle Mouse | Rotate | `transform.rotate` | release_confirm=True |

## 3D View Tool: Scale

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |
| Middle Mouse | Resize | `transform.resize` | release_confirm=True |

## 3D View Tool: Shear

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag north | Shear | `transform.shear` | release_confirm=True, orient_axis_ortho='Y' |
| Left Mouse drag south | Shear | `transform.shear` | release_confirm=True, orient_axis_ortho='Y' |
| Left Mouse drag | Shear | `transform.shear` | release_confirm=True, orient_axis_ortho='X' |
| Middle Mouse drag north | Shear | `transform.shear` | release_confirm=True, orient_axis_ortho='Y' |
| Middle Mouse drag south | Shear | `transform.shear` | release_confirm=True, orient_axis_ortho='Y' |
| Middle Mouse | Shear | `transform.shear` | release_confirm=True, orient_axis_ortho='X' |

## 3D View Tool: Bend

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Bend | `transform.bend` | release_confirm=True |
| Middle Mouse | Bend | `transform.bend` | release_confirm=True |

## 3D View Tool: Measure

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Ruler Add | `view3d.ruler_add` |  |
| X | Ruler Remove | `view3d.ruler_remove` |  |
| Delete | Ruler Remove | `view3d.ruler_remove` |  |
| Middle Mouse | Ruler Add | `view3d.ruler_add` |  |

## 3D View Tool: Breakdowner

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Pose Breakdowner | `pose.breakdown` |  |
| Middle Mouse | Pose Breakdowner | `pose.breakdown` |  |

## 3D View Tool: Push

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Push Pose from Breakdown | `pose.push` |  |
| Middle Mouse | Push Pose from Breakdown | `pose.push` |  |

## 3D View Tool: Relax

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Relax Pose to Breakdown | `pose.relax` |  |
| Middle Mouse | Relax Pose to Breakdown | `pose.relax` |  |

## 3D View Tool: Edit Armature, Roll

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Transform | `transform.transform` | release_confirm=True, mode='BONE_ROLL' |
| Middle Mouse | Transform | `transform.transform` | release_confirm=True, mode='BONE_ROLL' |

## 3D View Tool: Edit Armature, B-Bone Size

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Scale B-Bone | `transform.bbone_resize` | release_confirm=True |
| Middle Mouse | Scale B-Bone | `transform.bbone_resize` | release_confirm=True |

## 3D View Tool: Edit Armature, Bone Envelope

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Transform | `transform.transform` | release_confirm=True, mode='BONE_ENVELOPE_DIST' |
| Middle Mouse | Transform | `transform.transform` | release_confirm=True, mode='BONE_ENVELOPE_DIST' |

## 3D View Tool: Edit Armature, Extrude

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude | `armature.extrude_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Middle Mouse | Extrude | `armature.extrude_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Armature, Extrude to Cursor

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Extrude to Cursor | `armature.click_extrude` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |
| Middle Mouse | Extrude to Cursor | `armature.click_extrude` |  |
| Middle Mouse | Move | `transform.translate` | release_confirm=True |

## 3D View Tool: Edit Mesh, Extrude Region

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Region and Move | `mesh.extrude_context_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Middle Mouse | Extrude Region and Move | `mesh.extrude_context_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Mesh, Extrude Manifold

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Manifold | `mesh.extrude_manifold` | MESH_OT_extrude_region={use_dissolve_ortho_edges=True}, TRANSFORM_OT_translate={release_confirm=True, use_automerge_and_split=True, constraint_axis=(False, False, True), orient_type='NORMAL'} |
| Middle Mouse | Extrude Manifold | `mesh.extrude_manifold` | MESH_OT_extrude_region={use_dissolve_ortho_edges=True}, TRANSFORM_OT_translate={release_confirm=True, use_automerge_and_split=True, constraint_axis=(False, False, True), orient_type='NORMAL'} |

## 3D View Tool: Edit Mesh, Extrude Along Normals

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Region and Shrink/Fatten | `mesh.extrude_region_shrink_fatten` | TRANSFORM_OT_shrink_fatten={release_confirm=True} |
| Middle Mouse | Extrude Region and Shrink/Fatten | `mesh.extrude_region_shrink_fatten` | TRANSFORM_OT_shrink_fatten={release_confirm=True} |

## 3D View Tool: Edit Mesh, Extrude Individual

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Individual Faces and Move | `mesh.extrude_faces_move` | TRANSFORM_OT_shrink_fatten={release_confirm=True} |
| Middle Mouse | Extrude Individual Faces and Move | `mesh.extrude_faces_move` | TRANSFORM_OT_shrink_fatten={release_confirm=True} |

## 3D View Tool: Edit Mesh, Extrude to Cursor

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Extrude to Cursor or Add | `mesh.dupli_extrude_cursor` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |
| Middle Mouse | Extrude to Cursor or Add | `mesh.dupli_extrude_cursor` |  |
| Middle Mouse | Move | `transform.translate` | release_confirm=True |

## 3D View Tool: Edit Mesh, Inset Faces

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Inset Faces | `mesh.inset` | release_confirm=True |
| Middle Mouse | Inset Faces | `mesh.inset` | release_confirm=True |

## 3D View Tool: Edit Mesh, Bevel

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Bevel | `mesh.bevel` | release_confirm=True |
| Middle Mouse | Bevel | `mesh.bevel` | release_confirm=True |

## 3D View Tool: Edit Mesh, Loop Cut

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Loop Cut and Slide | `mesh.loopcut_slide` | TRANSFORM_OT_edge_slide={release_confirm=True} |
| Middle Mouse | Loop Cut and Slide | `mesh.loopcut_slide` | TRANSFORM_OT_edge_slide={release_confirm=True} |

## 3D View Tool: Edit Mesh, Offset Edge Loop Cut

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Offset Edge Slide | `mesh.offset_edge_loops_slide` |  |
| Middle Mouse | Offset Edge Slide | `mesh.offset_edge_loops_slide` |  |

## 3D View Tool: Edit Mesh, Knife

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Knife Topology Tool | `mesh.knife_tool` | wait_for_input=False |
| Middle Mouse | Knife Topology Tool | `mesh.knife_tool` | wait_for_input=False |

## 3D View Tool: Edit Mesh, Bisect

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Bisect | `mesh.bisect` |  |
| Middle Mouse | Bisect | `mesh.bisect` |  |

## 3D View Tool: Edit Mesh, Poly Build

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Extrude at Cursor Move | `mesh.polybuild_extrude_at_cursor_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Ctrl+Left Mouse | Face at Cursor Move | `mesh.polybuild_face_at_cursor_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Shift+Left Mouse click | Poly Build Delete at Cursor | `mesh.polybuild_delete_at_cursor` |  |
| Middle Mouse | Extrude at Cursor Move | `mesh.polybuild_extrude_at_cursor_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Ctrl+Middle Mouse | Face at Cursor Move | `mesh.polybuild_face_at_cursor_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Shift+Middle Mouse | Poly Build Delete at Cursor | `mesh.polybuild_delete_at_cursor` |  |

## 3D View Tool: Edit Mesh, Spin

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Spin | `mesh.spin` |  |
| Middle Mouse | Spin | `mesh.spin` |  |

## 3D View Tool: Edit Mesh, Spin Duplicates

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Spin | `mesh.spin` | dupli=True |
| Middle Mouse | Spin | `mesh.spin` | dupli=True |

## 3D View Tool: Edit Mesh, Smooth

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Smooth Vertices | `mesh.vertices_smooth` | wait_for_input=False |
| Middle Mouse | Smooth Vertices | `mesh.vertices_smooth` | wait_for_input=False |

## 3D View Tool: Edit Mesh, Randomize

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Randomize | `transform.vertex_random` | wait_for_input=False |
| Middle Mouse | Randomize | `transform.vertex_random` | wait_for_input=False |

## 3D View Tool: Edit Mesh, Edge Slide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Edge Slide | `transform.edge_slide` | release_confirm=True |
| Middle Mouse | Edge Slide | `transform.edge_slide` | release_confirm=True |

## 3D View Tool: Edit Mesh, Vertex Slide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Vertex Slide | `transform.vert_slide` | release_confirm=True |
| Middle Mouse | Vertex Slide | `transform.vert_slide` | release_confirm=True |

## 3D View Tool: Edit Mesh, Shrink/Fatten

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Shrink/Fatten | `transform.shrink_fatten` | release_confirm=True |
| Middle Mouse | Shrink/Fatten | `transform.shrink_fatten` | release_confirm=True |

## 3D View Tool: Edit Mesh, Push/Pull

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Push/Pull | `transform.push_pull` | release_confirm=True |
| Middle Mouse | Push/Pull | `transform.push_pull` | release_confirm=True |

## 3D View Tool: Edit Mesh, To Sphere

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | To Sphere | `transform.tosphere` | release_confirm=True |
| Middle Mouse | To Sphere | `transform.tosphere` | release_confirm=True |

## 3D View Tool: Edit Mesh, Rip Region

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rip | `mesh.rip_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Middle Mouse | Rip | `mesh.rip_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Mesh, Rip Edge

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extend Vertices | `mesh.rip_edge_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Middle Mouse | Extend Vertices | `mesh.rip_edge_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Curve, Draw

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Draw Curve | `curve.draw` | wait_for_input=False |
| Middle Mouse | Draw Curve | `curve.draw` | wait_for_input=False |

## 3D View Tool: Edit Curve, Curve Pen

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Curve Pen | `curve.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, close_spline_method='ON_CLICK' |
| Ctrl+Left Mouse | Curve Pen | `curve.pen` | insert_point=True, delete_point=True |
| Left Mouse double click | Curve Pen | `curve.pen` | toggle_vector=True, cycle_handle_type=True |
| Middle Mouse | Curve Pen | `curve.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, close_spline_method='ON_CLICK' |
| Ctrl+Middle Mouse | Curve Pen | `curve.pen` | insert_point=True, delete_point=True |
| Middle Mouse | Curve Pen | `curve.pen` | toggle_vector=True, cycle_handle_type=True |

## 3D View Tool: Edit Curve, Radius

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Transform | `transform.transform` | mode='CURVE_SHRINKFATTEN', release_confirm=True |
| Middle Mouse | Transform | `transform.transform` | mode='CURVE_SHRINKFATTEN', release_confirm=True |

## 3D View Tool: Edit Curve, Tilt

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Tilt | `transform.tilt` | release_confirm=True |
| Middle Mouse | Tilt | `transform.tilt` | release_confirm=True |

## 3D View Tool: Edit Curve, Randomize

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Randomize | `transform.vertex_random` | wait_for_input=False |
| Middle Mouse | Randomize | `transform.vertex_random` | wait_for_input=False |

## 3D View Tool: Edit Curve, Extrude

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Curve and Move | `curve.extrude_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Middle Mouse | Extrude Curve and Move | `curve.extrude_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Curve, Extrude to Cursor

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Extrude to Cursor or Add | `curve.vertex_add` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |
| Middle Mouse | Extrude to Cursor or Add | `curve.vertex_add` |  |
| Middle Mouse | Move | `transform.translate` | release_confirm=True |

## 3D View Tool: Edit Curves, Draw

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Draw Curves | `curves.draw` | wait_for_input=False |
| Middle Mouse | Draw Curves | `curves.draw` | wait_for_input=False |

## 3D View Tool: Edit Curves, Pen

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Curves Pen | `curves.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, extrude_handle='VECTOR' |
| Shift+Left Mouse | Curves Pen | `curves.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, extrude_handle='AUTO' |
| Alt+Left Mouse | Curves Pen | `curves.pen` | extrude_point=True, move_segment=False, select_point=False, move_point=False, extrude_handle='VECTOR' |
| Shift+Alt+Left Mouse | Curves Pen | `curves.pen` | extrude_point=True, move_segment=False, select_point=False, move_point=False, extrude_handle='AUTO' |
| Ctrl+Left Mouse | Curves Pen | `curves.pen` | insert_point=True, delete_point=True |
| Left Mouse double click | Curves Pen | `curves.pen` | cycle_handle_type=True |
| Middle Mouse | Curves Pen | `curves.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, extrude_handle='VECTOR' |
| Shift+Middle Mouse | Curves Pen | `curves.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, extrude_handle='AUTO' |
| Alt+Middle Mouse | Curves Pen | `curves.pen` | extrude_point=True, move_segment=False, select_point=False, move_point=False, extrude_handle='VECTOR' |
| Shift+Alt+Middle Mouse | Curves Pen | `curves.pen` | extrude_point=True, move_segment=False, select_point=False, move_point=False, extrude_handle='AUTO' |
| Ctrl+Middle Mouse | Curves Pen | `curves.pen` | insert_point=True, delete_point=True |
| Middle Mouse | Curves Pen | `curves.pen` | cycle_handle_type=True |

## 3D View Tool: Sculpt, Box Mask

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Mask Box Gesture | `paint.mask_box_gesture` | value=1.0 |
| Ctrl+Left Mouse drag | Mask Box Gesture | `paint.mask_box_gesture` | value=0.0 |
| Middle Mouse | Mask Box Gesture | `paint.mask_box_gesture` | value=1.0 |
| Ctrl+Middle Mouse | Mask Box Gesture | `paint.mask_box_gesture` | value=0.0 |

## 3D View Tool: Sculpt, Lasso Mask

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Mask Lasso Gesture | `paint.mask_lasso_gesture` | value=1.0 |
| Ctrl+Left Mouse drag | Mask Lasso Gesture | `paint.mask_lasso_gesture` | value=0.0 |
| Middle Mouse | Mask Lasso Gesture | `paint.mask_lasso_gesture` | value=1.0 |
| Ctrl+Middle Mouse | Mask Lasso Gesture | `paint.mask_lasso_gesture` | value=0.0 |

## 3D View Tool: Sculpt, Line Mask

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Mask Line Gesture | `paint.mask_line_gesture` | value=1.0 |
| Ctrl+Left Mouse drag | Mask Line Gesture | `paint.mask_line_gesture` | value=0.0 |
| Middle Mouse | Mask Line Gesture | `paint.mask_line_gesture` | value=1.0 |
| Ctrl+Middle Mouse | Mask Line Gesture | `paint.mask_line_gesture` | value=0.0 |

## 3D View Tool: Sculpt, Polyline Mask

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mask Polyline Gesture | `paint.mask_polyline_gesture` | value=1.0 |
| Ctrl+Left Mouse | Mask Polyline Gesture | `paint.mask_polyline_gesture` | value=0.0 |
| Middle Mouse | Mask Polyline Gesture | `paint.mask_polyline_gesture` | value=1.0 |
| Ctrl+Middle Mouse | Mask Polyline Gesture | `paint.mask_polyline_gesture` | value=0.0 |

## 3D View Tool: Sculpt, Box Hide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Hide/Show | `paint.hide_show` | action='HIDE' |
| Ctrl+Left Mouse drag | Hide/Show | `paint.hide_show` | action='SHOW' |
| Right Mouse | Hide/Show All | `paint.hide_show_all` | action='SHOW' |
| Middle Mouse | Hide/Show | `paint.hide_show` | action='HIDE' |
| Ctrl+Middle Mouse | Hide/Show | `paint.hide_show` | action='SHOW' |

## 3D View Tool: Sculpt, Lasso Hide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Hide/Show Lasso | `paint.hide_show_lasso_gesture` | action='HIDE' |
| Ctrl+Left Mouse drag | Hide/Show Lasso | `paint.hide_show_lasso_gesture` | action='SHOW' |
| Right Mouse | Hide/Show All | `paint.hide_show_all` | action='SHOW' |
| Middle Mouse | Hide/Show Lasso | `paint.hide_show_lasso_gesture` | action='HIDE' |
| Ctrl+Middle Mouse | Hide/Show Lasso | `paint.hide_show_lasso_gesture` | action='SHOW' |

## 3D View Tool: Sculpt, Line Hide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Hide/Show Line | `paint.hide_show_line_gesture` | action='HIDE' |
| Ctrl+Left Mouse drag | Hide/Show Line | `paint.hide_show_line_gesture` | action='SHOW' |
| Right Mouse | Hide/Show All | `paint.hide_show_all` | action='SHOW' |
| Middle Mouse | Hide/Show Line | `paint.hide_show_line_gesture` | action='HIDE' |
| Ctrl+Middle Mouse | Hide/Show Line | `paint.hide_show_line_gesture` | action='SHOW' |

## 3D View Tool: Sculpt, Polyline Hide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Hide/Show Polyline | `paint.hide_show_polyline_gesture` | action='HIDE' |
| Ctrl+Left Mouse | Hide/Show Polyline | `paint.hide_show_polyline_gesture` | action='SHOW' |
| Middle Mouse | Hide/Show Polyline | `paint.hide_show_polyline_gesture` | action='HIDE' |
| Ctrl+Middle Mouse | Hide/Show Polyline | `paint.hide_show_polyline_gesture` | action='SHOW' |

## 3D View Tool: Sculpt, Box Face Set

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Face Set Box Gesture | `sculpt.face_set_box_gesture` |  |
| Middle Mouse | Face Set Box Gesture | `sculpt.face_set_box_gesture` |  |

## 3D View Tool: Sculpt, Lasso Face Set

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Face Set Lasso Gesture | `sculpt.face_set_lasso_gesture` |  |
| Middle Mouse | Face Set Lasso Gesture | `sculpt.face_set_lasso_gesture` |  |

## 3D View Tool: Sculpt, Line Face Set

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Face Set Line Gesture | `sculpt.face_set_line_gesture` |  |
| Middle Mouse | Face Set Line Gesture | `sculpt.face_set_line_gesture` |  |

## 3D View Tool: Sculpt, Polyline Face Set

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Face Set Lasso Gesture | `sculpt.face_set_polyline_gesture` |  |
| Middle Mouse | Face Set Lasso Gesture | `sculpt.face_set_polyline_gesture` |  |

## 3D View Tool: Sculpt, Box Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Trim Box Gesture | `sculpt.trim_box_gesture` |  |
| Middle Mouse | Trim Box Gesture | `sculpt.trim_box_gesture` |  |

## 3D View Tool: Sculpt, Lasso Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Trim Lasso Gesture | `sculpt.trim_lasso_gesture` |  |
| Middle Mouse | Trim Lasso Gesture | `sculpt.trim_lasso_gesture` |  |

## 3D View Tool: Sculpt, Line Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Trim Line Gesture | `sculpt.trim_line_gesture` |  |
| Middle Mouse | Trim Line Gesture | `sculpt.trim_line_gesture` |  |

## 3D View Tool: Sculpt, Polyline Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Trim Polyline Gesture | `sculpt.trim_polyline_gesture` |  |
| Middle Mouse | Trim Polyline Gesture | `sculpt.trim_polyline_gesture` |  |

## 3D View Tool: Sculpt, Line Project

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Project Line Gesture | `sculpt.project_line_gesture` |  |
| Middle Mouse | Project Line Gesture | `sculpt.project_line_gesture` |  |

## 3D View Tool: Sculpt, Mesh Filter

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Filter Mesh | `sculpt.mesh_filter` |  |
| Middle Mouse | Filter Mesh | `sculpt.mesh_filter` |  |

## 3D View Tool: Sculpt, Cloth Filter

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Filter Cloth | `sculpt.cloth_filter` |  |
| Middle Mouse | Filter Cloth | `sculpt.cloth_filter` |  |

## 3D View Tool: Sculpt, Color Filter

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Filter Color | `sculpt.color_filter` |  |
| Ctrl+Left Mouse | Filter Color | `sculpt.color_filter` | use_secondary_color=True |
| Middle Mouse | Filter Color | `sculpt.color_filter` |  |
| Ctrl+Middle Mouse | Filter Color | `sculpt.color_filter` | use_secondary_color=True |

## 3D View Tool: Sculpt, Mask by Color

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mask by Color | `sculpt.mask_by_color` |  |
| Middle Mouse | Mask by Color | `sculpt.mask_by_color` |  |

## 3D View Tool: Sculpt, Face Set Edit

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Edit Face Set | `sculpt.face_set_edit` |  |
| Middle Mouse | Edit Face Set | `sculpt.face_set_edit` |  |

## 3D View Tool: Paint Weight, Sample Weight

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Weight Paint Sample Weight | `paint.weight_sample` |  |
| Left Mouse | Weight Paint Sample Weight | `grease_pencil.weight_sample` |  |
| Middle Mouse | Weight Paint Sample Weight | `paint.weight_sample` |  |
| Middle Mouse | Weight Paint Sample Weight | `grease_pencil.weight_sample` |  |

## 3D View Tool: Paint Weight, Sample Vertex Group

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Weight Paint Sample Group | `paint.weight_sample_group` |  |
| Middle Mouse | Weight Paint Sample Group | `paint.weight_sample_group` |  |

## 3D View Tool: Paint Weight, Gradient

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Weight Gradient | `paint.weight_gradient` |  |
| Middle Mouse | Weight Gradient | `paint.weight_gradient` |  |

## 3D View Tool: Paint Grease Pencil, Line

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Line Shape | `grease_pencil.primitive_line` |  |
| Shift+Left Mouse | Grease Pencil Line Shape | `grease_pencil.primitive_line` |  |
| Alt+Left Mouse | Grease Pencil Line Shape | `grease_pencil.primitive_line` |  |
| Middle Mouse | Grease Pencil Line Shape | `grease_pencil.primitive_line` |  |
| Shift+Middle Mouse | Grease Pencil Line Shape | `grease_pencil.primitive_line` |  |
| Alt+Middle Mouse | Grease Pencil Line Shape | `grease_pencil.primitive_line` |  |

## 3D View Tool: Paint Grease Pencil, Polyline

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Polyline Shape | `grease_pencil.primitive_polyline` |  |
| Shift+Left Mouse | Grease Pencil Polyline Shape | `grease_pencil.primitive_polyline` |  |
| Middle Mouse | Grease Pencil Polyline Shape | `grease_pencil.primitive_polyline` |  |
| Shift+Middle Mouse | Grease Pencil Polyline Shape | `grease_pencil.primitive_polyline` |  |

## 3D View Tool: Paint Grease Pencil, Box

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Box Shape | `grease_pencil.primitive_box` |  |
| Shift+Left Mouse | Grease Pencil Box Shape | `grease_pencil.primitive_box` |  |
| Alt+Left Mouse | Grease Pencil Box Shape | `grease_pencil.primitive_box` |  |
| Middle Mouse | Grease Pencil Box Shape | `grease_pencil.primitive_box` |  |
| Shift+Middle Mouse | Grease Pencil Box Shape | `grease_pencil.primitive_box` |  |
| Alt+Middle Mouse | Grease Pencil Box Shape | `grease_pencil.primitive_box` |  |

## 3D View Tool: Paint Grease Pencil, Circle

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Circle Shape | `grease_pencil.primitive_circle` |  |
| Shift+Left Mouse | Grease Pencil Circle Shape | `grease_pencil.primitive_circle` |  |
| Alt+Left Mouse | Grease Pencil Circle Shape | `grease_pencil.primitive_circle` |  |
| Middle Mouse | Grease Pencil Circle Shape | `grease_pencil.primitive_circle` |  |
| Shift+Middle Mouse | Grease Pencil Circle Shape | `grease_pencil.primitive_circle` |  |
| Alt+Middle Mouse | Grease Pencil Circle Shape | `grease_pencil.primitive_circle` |  |

## 3D View Tool: Paint Grease Pencil, Arc

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Arc Shape | `grease_pencil.primitive_arc` |  |
| Shift+Left Mouse | Grease Pencil Arc Shape | `grease_pencil.primitive_arc` |  |
| Alt+Left Mouse | Grease Pencil Arc Shape | `grease_pencil.primitive_arc` |  |
| Middle Mouse | Grease Pencil Arc Shape | `grease_pencil.primitive_arc` |  |
| Shift+Middle Mouse | Grease Pencil Arc Shape | `grease_pencil.primitive_arc` |  |
| Alt+Middle Mouse | Grease Pencil Arc Shape | `grease_pencil.primitive_arc` |  |

## 3D View Tool: Paint Grease Pencil, Curve

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Curve Shape | `grease_pencil.primitive_curve` |  |
| Middle Mouse | Grease Pencil Curve Shape | `grease_pencil.primitive_curve` |  |

## 3D View Tool: Paint Grease Pencil, Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Trim | `grease_pencil.stroke_trim` |  |
| Middle Mouse | Grease Pencil Trim | `grease_pencil.stroke_trim` |  |

## 3D View Tool: Paint Grease Pencil, Interpolate

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Grease Pencil Interpolation | `grease_pencil.interpolate` | use_selection=False |
| Middle Mouse | Grease Pencil Interpolation | `grease_pencil.interpolate` | use_selection=False |

## 3D View Tool: Paint Grease Pencil, Eyedropper

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Shift+Left Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Ctrl+Left Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Ctrl+Shift+Left Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Middle Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Shift+Middle Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Ctrl+Middle Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Ctrl+Shift+Middle Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |

## 3D View Tool: Edit Grease Pencil, Gradient

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Texture Gradient | `grease_pencil.texture_gradient` |  |
| Middle Mouse | Texture Gradient | `grease_pencil.texture_gradient` |  |

## 3D View Tool: Edit Grease Pencil, Pen

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Pen | `grease_pencil.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, extrude_handle='VECTOR' |
| Shift+Left Mouse | Grease Pencil Pen | `grease_pencil.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, extrude_handle='AUTO' |
| Alt+Left Mouse | Grease Pencil Pen | `grease_pencil.pen` | extrude_point=True, move_segment=False, select_point=False, move_point=False, extrude_handle='VECTOR' |
| Shift+Alt+Left Mouse | Grease Pencil Pen | `grease_pencil.pen` | extrude_point=True, move_segment=False, select_point=False, move_point=False, extrude_handle='AUTO' |
| Ctrl+Left Mouse | Grease Pencil Pen | `grease_pencil.pen` | insert_point=True, delete_point=True |
| Left Mouse double click | Grease Pencil Pen | `grease_pencil.pen` | cycle_handle_type=True |
| Middle Mouse | Grease Pencil Pen | `grease_pencil.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, extrude_handle='VECTOR' |
| Shift+Middle Mouse | Grease Pencil Pen | `grease_pencil.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, extrude_handle='AUTO' |
| Alt+Middle Mouse | Grease Pencil Pen | `grease_pencil.pen` | extrude_point=True, move_segment=False, select_point=False, move_point=False, extrude_handle='VECTOR' |
| Shift+Alt+Middle Mouse | Grease Pencil Pen | `grease_pencil.pen` | extrude_point=True, move_segment=False, select_point=False, move_point=False, extrude_handle='AUTO' |
| Ctrl+Middle Mouse | Grease Pencil Pen | `grease_pencil.pen` | insert_point=True, delete_point=True |
| Middle Mouse | Grease Pencil Pen | `grease_pencil.pen` | cycle_handle_type=True |

## 3D View Tool: Edit Grease Pencil, Interpolate

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Grease Pencil Interpolation | `grease_pencil.interpolate` | use_selection=True |
| Middle Mouse | Grease Pencil Interpolation | `grease_pencil.interpolate` | use_selection=True |

## 3D View Tool: Paint Grease Pencil, Carver

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Carver | `grease_pencil.stroke_carver` |  |
| Middle Mouse | Grease Pencil Carver | `grease_pencil.stroke_carver` |  |

## Sequencer Tool: Select Box (fallback)

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select Handle | `sequencer.select_handle` |  |
| Alt+Left Mouse | Select Handle | `sequencer.select_handle` | ignore_connections=True |
| Left Mouse | Change Frame | `anim.change_frame` | pass_through_on_strip_handles=True |
| Shift+Left Mouse | Change Frame | `anim.change_frame` | seq_solo_preview=True |
| Left Mouse drag | Sequence Slide | `transform.seq_slide` | view2d_edge_pan=True, use_restore_handle_selection=True |

## Preview Tool: Tweak

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse drag | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse | Set 2D Cursor | `sequencer.cursor_set` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## Preview Tool: Tweak (fallback)

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse drag | Set Cursor | `sequencer.text_cursor_set` |  |

## Preview Tool: Select Box (fallback)

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse drag | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse drag | Box Select | `sequencer.select_box` |  |
| Shift+Left Mouse drag | Box Select | `sequencer.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `sequencer.select_box` | mode='SUB' |

## Sequencer Tool: Select Lasso

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `sequencer.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='SUB' |

## Sequencer Tool: Select Lasso (fallback)

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `sequencer.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='SUB' |

## Preview Tool: Select Lasso

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `sequencer.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='SUB' |

## Preview Tool: Select Lasso (fallback)

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `sequencer.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='SUB' |

## Preview Tool: Select Circle

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='SUB' |

## Preview Tool: Select Circle (fallback)

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='SUB' |

## Sequencer Tool: Select Circle

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='SUB' |

## Sequencer Tool: Select Circle (fallback)

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='SUB' |

## Sequencer Tool: Blade

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse click | Split Strips | `sequencer.split` | side='NO_CHANGE', use_cursor_position=True |
| Alt+Left Mouse click | Split Strips | `sequencer.split` | side='NO_CHANGE', use_cursor_position=True, ignore_connections=True |
| Shift+Left Mouse click | Split Strips | `sequencer.split` | side='NO_CHANGE', use_cursor_position=True, all_channels=True |
| Left Mouse drag | Box Blade | `sequencer.box_blade` |  |
| Shift+Left Mouse drag | Box Blade | `sequencer.box_blade` | remove_gaps=False |
| Alt+Left Mouse drag | Box Blade | `sequencer.box_blade` | ignore_connections=True |
| Shift+Alt+Left Mouse drag | Box Blade | `sequencer.box_blade` | remove_gaps=False, ignore_connections=True |
| Middle Mouse | Split Strips | `sequencer.split` | side='NO_CHANGE', use_cursor_position=True |
| Alt+Middle Mouse | Split Strips | `sequencer.split` | side='NO_CHANGE', use_cursor_position=True, ignore_connections=True |
| Shift+Middle Mouse | Split Strips | `sequencer.split` | side='NO_CHANGE', use_cursor_position=True, all_channels=True |
| Middle Mouse | Box Blade | `sequencer.box_blade` |  |
| Shift+Middle Mouse | Box Blade | `sequencer.box_blade` | remove_gaps=False |
| Alt+Middle Mouse | Box Blade | `sequencer.box_blade` | ignore_connections=True |
| Shift+Alt+Middle Mouse | Box Blade | `sequencer.box_blade` | remove_gaps=False, ignore_connections=True |

## Sequencer Tool: Slip

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Slip Strips | `sequencer.slip` | slip_keyframes=True, use_cursor_position=True |
| Alt+Left Mouse | Slip Strips | `sequencer.slip` | slip_keyframes=True, use_cursor_position=True, ignore_connections=True |
| Middle Mouse | Slip Strips | `sequencer.slip` | slip_keyframes=True, use_cursor_position=True |
| Alt+Middle Mouse | Slip Strips | `sequencer.slip` | slip_keyframes=True, use_cursor_position=True, ignore_connections=True |

## Preview Tool: Cursor

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set 2D Cursor | `sequencer.cursor_set` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |
| Middle Mouse | Set 2D Cursor | `sequencer.cursor_set` |  |
| Middle Mouse | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## Preview Tool: Sample

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Sample Color | `sequencer.sample` |  |
| Middle Mouse | Sample Color | `sequencer.sample` |  |

## Preview Tool: Move

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |
| Middle Mouse | Move | `transform.translate` | release_confirm=True |

## Preview Tool: Rotate

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rotate | `transform.rotate` | release_confirm=True |
| Middle Mouse | Rotate | `transform.rotate` | release_confirm=True |

## Preview Tool: Scale

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |
| Middle Mouse | Resize | `transform.resize` | release_confirm=True |

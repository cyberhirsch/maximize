# Blender 5.3 — complete default keymap

Generated 2026-10-23 from the keymap source of the Moritz fork (Blender 5.3, branch `blender-v5.3-release`), so it lists every binding, not a selection.

- **Key**: modifiers + key + event. No event word means *press*. `[Ctrl]` means either state.
- **Action**: the operator's UI name; for modal keymaps, the modal item.
- Windows/Linux keys; on macOS Blender maps Ctrl to Cmd for most items.
- Bindings marked *(Moritz)* are Moritz additions.
- Preset settings: left-click select, Spacebar = Play, Tool Keys = Immediate, MMB = Orbit, Alt-MMB = Relative, gizmo on drag, Alt navigation on.

**3295 bindings in 281 keymaps.**

### Keymaps

- [Window](#window) — 33
- [Screen](#screen) — 26
- [Screen Editing](#screen-editing) — 14
- [Region Context Menu](#region-context-menu) — 2
- [View2D](#view2d) — 25
- [View2D Buttons List](#view2d-buttons-list) — 14
- [User Interface](#user-interface) — 39
- [Property Editor](#property-editor) — 26
- [Outliner](#outliner) — 104
- [Preferences](#preferences) — 2
- [Preferences_nav](#preferences_nav) — 2
- [UV Editor](#uv-editor) — 88
- [3D View Generic](#3d-view-generic) — 2
- [3D View](#3d-view) — 116
- [Mask Editing](#mask-editing) — 48
- [Markers](#markers) — 25
- [Time Scrub](#time-scrub) — 1
- [Clip Time Scrub](#clip-time-scrub) — 1
- [Graph Editor Generic](#graph-editor-generic) — 10
- [Graph Editor](#graph-editor) — 71
- [Image Generic](#image-generic) — 11
- [Image](#image) — 51
- [Node Generic](#node-generic) — 2
- [Node Editor](#node-editor) — 108
- [Spreadsheet Generic](#spreadsheet-generic) — 5
- [Info](#info) — 14
- [File Browser](#file-browser) — 41
- [File Browser Main](#file-browser-main) — 33
- [File Browser Buttons](#file-browser-buttons) — 6
- [Dopesheet Generic](#dopesheet-generic) — 3
- [Dopesheet](#dopesheet) — 68
- [NLA Generic](#nla-generic) — 6
- [NLA Tracks](#nla-tracks) — 8
- [NLA Editor](#nla-editor) — 49
- [Text Generic](#text-generic) — 5
- [Text](#text) — 71
- [Video Sequence Editor](#video-sequence-editor) — 7
- [Sequencer](#sequencer) — 99
- [Preview](#preview) — 89
- [Sequencer Channels](#sequencer-channels) — 2
- [Console](#console) — 40
- [Clip](#clip) — 14
- [Clip Editor](#clip-editor) — 76
- [Clip Graph Editor](#clip-graph-editor) — 24
- [Clip Dopesheet Editor](#clip-dopesheet-editor) — 4
- [Frames](#frames) — 17
- [Animation](#animation) — 5
- [Animation Channels](#animation-channels) — 37
- [Grease Pencil](#grease-pencil) — 5
- [Grease Pencil Selection](#grease-pencil-selection) — 10
- [Grease Pencil Draw Mode](#grease-pencil-draw-mode) — 40
- [Grease Pencil Edit Mode](#grease-pencil-edit-mode) — 57
- [Grease Pencil Sculpt Mode](#grease-pencil-sculpt-mode) — 27
- [Grease Pencil Weight Paint](#grease-pencil-weight-paint) — 26
- [Grease Pencil Vertex Paint](#grease-pencil-vertex-paint) — 22
- [Grease Pencil Brush Stroke](#grease-pencil-brush-stroke) — 6
- [Grease Pencil Fill Tool](#grease-pencil-fill-tool) — 3
- [Object Mode](#object-mode) — 59
- [Object Non-modal](#object-non-modal) — 3
- [Pose](#pose) — 53
- [Paint Curve](#paint-curve) — 15
- [Image Paint](#image-paint) — 26
- [Vertex Paint](#vertex-paint) — 27
- [Weight Paint](#weight-paint) — 26
- [Paint Face Mask (Weight, Vertex, Texture)](#paint-face-mask-weight,-vertex,-texture) — 14
- [Paint Vertex Selection (Weight, Vertex)](#paint-vertex-selection-weight,-vertex) — 16
- [Sculpt](#sculpt) — 67
- [Sculpt Curves](#sculpt-curves) — 16
- [Mesh](#mesh) — 93
- [Armature](#armature) — 52
- [Metaball](#metaball) — 22
- [Lattice](#lattice) — 21
- [Particle](#particle) — 30
- [Font](#font) — 49
- [Curve](#curve) — 45
- [Curves](#curves) — 34
- [Point Cloud](#point-cloud) — 18
- [Eyedropper Modal Map](#eyedropper-modal-map) — 7
- [Eyedropper ColorRamp PointSampling Map](#eyedropper-colorramp-pointsampling-map) — 7
- [Transform Modal Map](#transform-modal-map) — 60
- [View3D Placement Modal](#view3d-placement-modal) — 12
- [View3D Gesture Circle](#view3d-gesture-circle) — 14
- [Gesture Box](#gesture-box) — 10
- [Gesture Zoom Border](#gesture-zoom-border) — 6
- [Gesture Straight Line](#gesture-straight-line) — 7
- [Gesture Lasso](#gesture-lasso) — 1
- [Gesture Polyline](#gesture-polyline) — 6
- [Standard Modal Map](#standard-modal-map) — 8
- [Knife Tool Modal Map](#knife-tool-modal-map) — 25
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
- [Generic Gizmo Drag](#generic-gizmo-drag) — 1
- [Generic Gizmo Maybe Drag](#generic-gizmo-maybe-drag) — 1
- [Generic Gizmo Click Drag](#generic-gizmo-click-drag) — 2
- [Generic Gizmo Select](#generic-gizmo-select) — 1
- [Generic Gizmo Tweak Modal Map](#generic-gizmo-tweak-modal-map) — 12
- [Toolbar Popup](#toolbar-popup) — 5
- [Generic Tool: Annotate](#generic-tool:-annotate) — 2
- [Generic Tool: Annotate Line](#generic-tool:-annotate-line) — 2
- [Generic Tool: Annotate Polygon](#generic-tool:-annotate-polygon) — 2
- [Generic Tool: Annotate Eraser](#generic-tool:-annotate-eraser) — 2
- [Image Editor Tool: Sample](#image-editor-tool:-sample) — 1
- [Image Editor Tool: Uv, Cursor](#image-editor-tool:-uv,-cursor) — 2
- [Image Editor Tool: Uv, Tweak](#image-editor-tool:-uv,-tweak) — 3
- [Image Editor Tool: Uv, Tweak (fallback)](#image-editor-tool:-uv,-tweak-fallback) — 3
- [Image Editor Tool: Uv, Select Box](#image-editor-tool:-uv,-select-box) — 3
- [Image Editor Tool: Uv, Select Box (fallback)](#image-editor-tool:-uv,-select-box-fallback) — 3
- [Image Editor Tool: Uv, Select Circle](#image-editor-tool:-uv,-select-circle) — 3
- [Image Editor Tool: Uv, Select Circle (fallback)](#image-editor-tool:-uv,-select-circle-fallback) — 3
- [Image Editor Tool: Uv, Select Lasso](#image-editor-tool:-uv,-select-lasso) — 3
- [Image Editor Tool: Uv, Select Lasso (fallback)](#image-editor-tool:-uv,-select-lasso-fallback) — 3
- [Image Editor Tool: Uv, Rip Region](#image-editor-tool:-uv,-rip-region) — 1
- [Image Editor Tool: Uv, Grab](#image-editor-tool:-uv,-grab) — 5
- [Image Editor Tool: Uv, Relax](#image-editor-tool:-uv,-relax) — 5
- [Image Editor Tool: Uv, Pinch](#image-editor-tool:-uv,-pinch) — 5
- [Image Editor Tool: Uv, Move](#image-editor-tool:-uv,-move) — 1
- [Image Editor Tool: Uv, Rotate](#image-editor-tool:-uv,-rotate) — 1
- [Image Editor Tool: Uv, Scale](#image-editor-tool:-uv,-scale) — 1
- [Image Editor Tool: Mask, Cursor](#image-editor-tool:-mask,-cursor) — 2
- [Image Editor Tool: Mask, Tweak](#image-editor-tool:-mask,-tweak) — 3
- [Image Editor Tool: Mask, Tweak (fallback)](#image-editor-tool:-mask,-tweak-fallback) — 3
- [Image Editor Tool: Mask, Select Box](#image-editor-tool:-mask,-select-box) — 3
- [Image Editor Tool: Mask, Select Box (fallback)](#image-editor-tool:-mask,-select-box-fallback) — 3
- [Image Editor Tool: Mask, Select Circle](#image-editor-tool:-mask,-select-circle) — 3
- [Image Editor Tool: Mask, Select Circle (fallback)](#image-editor-tool:-mask,-select-circle-fallback) — 3
- [Image Editor Tool: Mask, Select Lasso](#image-editor-tool:-mask,-select-lasso) — 3
- [Image Editor Tool: Mask, Select Lasso (fallback)](#image-editor-tool:-mask,-select-lasso-fallback) — 3
- [Image Editor Tool: Mask, Move](#image-editor-tool:-mask,-move) — 1
- [Image Editor Tool: Mask, Rotate](#image-editor-tool:-mask,-rotate) — 1
- [Image Editor Tool: Mask, Scale](#image-editor-tool:-mask,-scale) — 1
- [Image Editor Tool: Mask, Transform](#image-editor-tool:-mask,-transform) — 1
- [Image Editor Tool: Mask, Circle](#image-editor-tool:-mask,-circle) — 1
- [Image Editor Tool: Mask, Box](#image-editor-tool:-mask,-box) — 1
- [Node Tool: Tweak](#node-tool:-tweak) — 9
- [Node Tool: Tweak (fallback)](#node-tool:-tweak-fallback) — 9
- [Node Tool: Select Box](#node-tool:-select-box) — 12
- [Node Tool: Select Box (fallback)](#node-tool:-select-box-fallback) — 12
- [Node Tool: Select Lasso](#node-tool:-select-lasso) — 3
- [Node Tool: Select Lasso (fallback)](#node-tool:-select-lasso-fallback) — 3
- [Node Tool: Select Circle](#node-tool:-select-circle) — 3
- [Node Tool: Select Circle (fallback)](#node-tool:-select-circle-fallback) — 3
- [Node Tool: Links Cut](#node-tool:-links-cut) — 1
- [Node Tool: Mute Links](#node-tool:-mute-links) — 1
- [Node Tool: Add Reroute](#node-tool:-add-reroute) — 1
- [3D View Tool: Cursor](#3d-view-tool:-cursor) — 2
- [3D View Tool: Edit Text, Select Text](#3d-view-tool:-edit-text,-select-text) — 2
- [3D View Tool: Tweak](#3d-view-tool:-tweak) — 9
- [3D View Tool: Tweak (fallback)](#3d-view-tool:-tweak-fallback) — 9
- [3D View Tool: Select Box](#3d-view-tool:-select-box) — 10
- [3D View Tool: Select Box (fallback)](#3d-view-tool:-select-box-fallback) — 10
- [3D View Tool: Select Circle](#3d-view-tool:-select-circle) — 9
- [3D View Tool: Select Circle (fallback)](#3d-view-tool:-select-circle-fallback) — 9
- [3D View Tool: Select Lasso](#3d-view-tool:-select-lasso) — 10
- [3D View Tool: Select Lasso (fallback)](#3d-view-tool:-select-lasso-fallback) — 10
- [3D View Tool: Transform](#3d-view-tool:-transform) — 1
- [3D View Tool: Move](#3d-view-tool:-move) — 1
- [3D View Tool: Rotate](#3d-view-tool:-rotate) — 1
- [3D View Tool: Scale](#3d-view-tool:-scale) — 1
- [3D View Tool: Shear](#3d-view-tool:-shear) — 3
- [3D View Tool: Bend](#3d-view-tool:-bend) — 1
- [3D View Tool: Measure](#3d-view-tool:-measure) — 3
- [3D View Tool: Object, Add Primitive](#3d-view-tool:-object,-add-primitive) — 1
- [3D View Tool: Breakdowner](#3d-view-tool:-breakdowner) — 1
- [3D View Tool: Push](#3d-view-tool:-push) — 1
- [3D View Tool: Relax](#3d-view-tool:-relax) — 1
- [3D View Tool: Edit Armature, Roll](#3d-view-tool:-edit-armature,-roll) — 1
- [3D View Tool: Edit Armature, B-Bone Size](#3d-view-tool:-edit-armature,-b-bone-size) — 1
- [3D View Tool: Edit Armature, Bone Envelope](#3d-view-tool:-edit-armature,-bone-envelope) — 1
- [3D View Tool: Edit Armature, Extrude](#3d-view-tool:-edit-armature,-extrude) — 1
- [3D View Tool: Edit Armature, Extrude to Cursor](#3d-view-tool:-edit-armature,-extrude-to-cursor) — 1
- [3D View Tool: Edit Mesh, Extrude Region](#3d-view-tool:-edit-mesh,-extrude-region) — 1
- [3D View Tool: Edit Mesh, Extrude Manifold](#3d-view-tool:-edit-mesh,-extrude-manifold) — 1
- [3D View Tool: Edit Mesh, Extrude Along Normals](#3d-view-tool:-edit-mesh,-extrude-along-normals) — 1
- [3D View Tool: Edit Mesh, Extrude Individual](#3d-view-tool:-edit-mesh,-extrude-individual) — 1
- [3D View Tool: Edit Mesh, Extrude to Cursor](#3d-view-tool:-edit-mesh,-extrude-to-cursor) — 1
- [3D View Tool: Edit Mesh, Inset Faces](#3d-view-tool:-edit-mesh,-inset-faces) — 1
- [3D View Tool: Edit Mesh, Bevel](#3d-view-tool:-edit-mesh,-bevel) — 1
- [3D View Tool: Edit Mesh, Loop Cut](#3d-view-tool:-edit-mesh,-loop-cut) — 1
- [3D View Tool: Edit Mesh, Offset Edge Loop Cut](#3d-view-tool:-edit-mesh,-offset-edge-loop-cut) — 1
- [3D View Tool: Edit Mesh, Knife](#3d-view-tool:-edit-mesh,-knife) — 1
- [3D View Tool: Edit Mesh, Bisect](#3d-view-tool:-edit-mesh,-bisect) — 1
- [3D View Tool: Edit Mesh, Poly Build](#3d-view-tool:-edit-mesh,-poly-build) — 3
- [3D View Tool: Edit Mesh, Spin](#3d-view-tool:-edit-mesh,-spin) — 1
- [3D View Tool: Edit Mesh, Spin Duplicates](#3d-view-tool:-edit-mesh,-spin-duplicates) — 1
- [3D View Tool: Edit Mesh, Smooth](#3d-view-tool:-edit-mesh,-smooth) — 1
- [3D View Tool: Edit Mesh, Randomize](#3d-view-tool:-edit-mesh,-randomize) — 1
- [3D View Tool: Edit Mesh, Edge Slide](#3d-view-tool:-edit-mesh,-edge-slide) — 1
- [3D View Tool: Edit Mesh, Vertex Slide](#3d-view-tool:-edit-mesh,-vertex-slide) — 1
- [3D View Tool: Edit Mesh, Shrink/Fatten](#3d-view-tool:-edit-mesh,-shrinkfatten) — 1
- [3D View Tool: Edit Mesh, Push/Pull](#3d-view-tool:-edit-mesh,-pushpull) — 1
- [3D View Tool: Edit Mesh, To Sphere](#3d-view-tool:-edit-mesh,-to-sphere) — 1
- [3D View Tool: Edit Mesh, Rip Region](#3d-view-tool:-edit-mesh,-rip-region) — 1
- [3D View Tool: Edit Mesh, Rip Edge](#3d-view-tool:-edit-mesh,-rip-edge) — 1
- [3D View Tool: Edit Curve, Draw](#3d-view-tool:-edit-curve,-draw) — 1
- [3D View Tool: Edit Curve, Curve Pen](#3d-view-tool:-edit-curve,-curve-pen) — 3
- [3D View Tool: Edit Curve, Radius](#3d-view-tool:-edit-curve,-radius) — 1
- [3D View Tool: Edit Curve, Tilt](#3d-view-tool:-edit-curve,-tilt) — 1
- [3D View Tool: Edit Curve, Randomize](#3d-view-tool:-edit-curve,-randomize) — 1
- [3D View Tool: Edit Curve, Extrude](#3d-view-tool:-edit-curve,-extrude) — 1
- [3D View Tool: Edit Curve, Extrude to Cursor](#3d-view-tool:-edit-curve,-extrude-to-cursor) — 1
- [3D View Tool: Edit Curves, Draw](#3d-view-tool:-edit-curves,-draw) — 1
- [3D View Tool: Edit Curves, Pen](#3d-view-tool:-edit-curves,-pen) — 6
- [3D View Tool: Sculpt, Box Mask](#3d-view-tool:-sculpt,-box-mask) — 2
- [3D View Tool: Sculpt, Lasso Mask](#3d-view-tool:-sculpt,-lasso-mask) — 2
- [3D View Tool: Sculpt, Line Mask](#3d-view-tool:-sculpt,-line-mask) — 2
- [3D View Tool: Sculpt, Polyline Mask](#3d-view-tool:-sculpt,-polyline-mask) — 2
- [3D View Tool: Sculpt, Box Hide](#3d-view-tool:-sculpt,-box-hide) — 3
- [3D View Tool: Sculpt, Lasso Hide](#3d-view-tool:-sculpt,-lasso-hide) — 3
- [3D View Tool: Sculpt, Line Hide](#3d-view-tool:-sculpt,-line-hide) — 3
- [3D View Tool: Sculpt, Polyline Hide](#3d-view-tool:-sculpt,-polyline-hide) — 2
- [3D View Tool: Sculpt, Box Face Set](#3d-view-tool:-sculpt,-box-face-set) — 1
- [3D View Tool: Sculpt, Lasso Face Set](#3d-view-tool:-sculpt,-lasso-face-set) — 1
- [3D View Tool: Sculpt, Line Face Set](#3d-view-tool:-sculpt,-line-face-set) — 1
- [3D View Tool: Sculpt, Polyline Face Set](#3d-view-tool:-sculpt,-polyline-face-set) — 1
- [3D View Tool: Sculpt, Box Trim](#3d-view-tool:-sculpt,-box-trim) — 1
- [3D View Tool: Sculpt, Lasso Trim](#3d-view-tool:-sculpt,-lasso-trim) — 1
- [3D View Tool: Sculpt, Line Trim](#3d-view-tool:-sculpt,-line-trim) — 1
- [3D View Tool: Sculpt, Polyline Trim](#3d-view-tool:-sculpt,-polyline-trim) — 1
- [3D View Tool: Sculpt, Line Project](#3d-view-tool:-sculpt,-line-project) — 1
- [3D View Tool: Sculpt, Mesh Filter](#3d-view-tool:-sculpt,-mesh-filter) — 1
- [3D View Tool: Sculpt, Cloth Filter](#3d-view-tool:-sculpt,-cloth-filter) — 1
- [3D View Tool: Sculpt, Color Filter](#3d-view-tool:-sculpt,-color-filter) — 2
- [3D View Tool: Sculpt, Mask by Color](#3d-view-tool:-sculpt,-mask-by-color) — 1
- [3D View Tool: Sculpt, Face Set Edit](#3d-view-tool:-sculpt,-face-set-edit) — 1
- [3D View Tool: Paint Weight, Sample Weight](#3d-view-tool:-paint-weight,-sample-weight) — 2
- [3D View Tool: Paint Weight, Sample Vertex Group](#3d-view-tool:-paint-weight,-sample-vertex-group) — 1
- [3D View Tool: Paint Weight, Gradient](#3d-view-tool:-paint-weight,-gradient) — 1
- [3D View Tool: Paint Grease Pencil, Line](#3d-view-tool:-paint-grease-pencil,-line) — 3
- [3D View Tool: Paint Grease Pencil, Polyline](#3d-view-tool:-paint-grease-pencil,-polyline) — 2
- [3D View Tool: Paint Grease Pencil, Box](#3d-view-tool:-paint-grease-pencil,-box) — 3
- [3D View Tool: Paint Grease Pencil, Circle](#3d-view-tool:-paint-grease-pencil,-circle) — 3
- [3D View Tool: Paint Grease Pencil, Arc](#3d-view-tool:-paint-grease-pencil,-arc) — 3
- [3D View Tool: Paint Grease Pencil, Curve](#3d-view-tool:-paint-grease-pencil,-curve) — 1
- [3D View Tool: Paint Grease Pencil, Trim](#3d-view-tool:-paint-grease-pencil,-trim) — 1
- [3D View Tool: Paint Grease Pencil, Interpolate](#3d-view-tool:-paint-grease-pencil,-interpolate) — 1
- [3D View Tool: Paint Grease Pencil, Eyedropper](#3d-view-tool:-paint-grease-pencil,-eyedropper) — 4
- [3D View Tool: Edit Grease Pencil, Gradient](#3d-view-tool:-edit-grease-pencil,-gradient) — 1
- [3D View Tool: Edit Grease Pencil, Pen](#3d-view-tool:-edit-grease-pencil,-pen) — 6
- [3D View Tool: Edit Grease Pencil, Interpolate](#3d-view-tool:-edit-grease-pencil,-interpolate) — 1
- [3D View Tool: Paint Grease Pencil, Carver](#3d-view-tool:-paint-grease-pencil,-carver) — 1
- [Sequencer Tool: Select Box](#sequencer-tool:-select-box) — 8
- [Sequencer Tool: Select Box (fallback)](#sequencer-tool:-select-box-fallback) — 8
- [Preview Tool: Tweak](#preview-tool:-tweak) — 5
- [Preview Tool: Tweak (fallback)](#preview-tool:-tweak-fallback) — 5
- [Preview Tool: Select Box](#preview-tool:-select-box) — 5
- [Preview Tool: Select Box (fallback)](#preview-tool:-select-box-fallback) — 5
- [Sequencer Tool: Select Lasso](#sequencer-tool:-select-lasso) — 3
- [Sequencer Tool: Select Lasso (fallback)](#sequencer-tool:-select-lasso-fallback) — 3
- [Preview Tool: Select Lasso](#preview-tool:-select-lasso) — 3
- [Preview Tool: Select Lasso (fallback)](#preview-tool:-select-lasso-fallback) — 3
- [Preview Tool: Select Circle](#preview-tool:-select-circle) — 3
- [Preview Tool: Select Circle (fallback)](#preview-tool:-select-circle-fallback) — 3
- [Sequencer Tool: Select Circle](#sequencer-tool:-select-circle) — 3
- [Sequencer Tool: Select Circle (fallback)](#sequencer-tool:-select-circle-fallback) — 3
- [Sequencer Tool: Blade](#sequencer-tool:-blade) — 7
- [Sequencer Tool: Slip](#sequencer-tool:-slip) — 2
- [Preview Tool: Cursor](#preview-tool:-cursor) — 2
- [Preview Tool: Sample](#preview-tool:-sample) — 1
- [Preview Tool: Move](#preview-tool:-move) — 1
- [Preview Tool: Rotate](#preview-tool:-rotate) — 1
- [Preview Tool: Scale](#preview-tool:-scale) — 1

## Window

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+N | Call Menu | `wm.call_menu` | name='TOPBAR_MT_file_new' |
| Ctrl+Shift+O | Call Menu | `wm.call_menu` | name='TOPBAR_MT_file_open_recent' |
| Ctrl+O | Open | `wm.open_mainfile` |  |
| Ctrl+S | Save Blender File | `wm.save_mainfile` | show_save_modified_images_dialog=True |
| Ctrl+Shift+S | Save As | `wm.save_as_mainfile` | show_save_modified_images_dialog=True |
| Ctrl+Alt+S | Save Blender File | `wm.save_mainfile` | incremental=True, show_save_modified_images_dialog=True |
| Ctrl+Q | Quit Blender | `wm.quit_blender` |  |
| Q | Call Menu | `wm.call_menu` | name='SCREEN_MT_user_menu' |
| Shift+F1 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='FILE_BROWSER' |
| Shift+F2 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='CLIP_EDITOR' |
| Shift+F3 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='NODE_EDITOR' |
| Shift+F4 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='CONSOLE' |
| Shift+F5 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='VIEW_3D' |
| Shift+F6 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='GRAPH_EDITOR' |
| Shift+F7 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='PROPERTIES' |
| Shift+F8 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='SEQUENCE_EDITOR' |
| Shift+F9 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='OUTLINER' |
| Shift+F10 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='IMAGE_EDITOR' |
| Shift+F11 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='TEXT_EDITOR' |
| Shift+F12 | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='DOPESHEET_EDITOR' |
| NDOF Menu | Call Panel | `wm.call_panel` | name='USERPREF_PT_ndof_settings' |
| NDOF Plus | Context Scale Float | `wm.context_scale_float` | data_path='preferences.inputs.ndof_translation_sensitivity', value=1.1 |
| NDOF Minus | Context Scale Float | `wm.context_scale_float` | data_path='preferences.inputs.ndof_translation_sensitivity', value=0.9090909090909091 |
| Shift+NDOF Plus | Context Scale Float | `wm.context_scale_float` | data_path='preferences.inputs.ndof_translation_sensitivity', value=1.5 |
| Shift+NDOF Minus | Context Scale Float | `wm.context_scale_float` | data_path='preferences.inputs.ndof_translation_sensitivity', value=0.6666666666666666 |
| Any modifier+Timer Report any | Update Reports Display | `info.reports_display_update` |  |
| F1 | View Online Manual | `wm.doc_view_manual_ui_context` |  |
| F2 | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name', keep_open=False |
| Ctrl+F2 | Batch Rename | `wm.batch_rename` |  |
| F3 | Search Menu | `wm.search_menu` |  |
| F4 | Call Menu | `wm.call_menu` | name='TOPBAR_MT_file_context_menu' |
| Alt+W | Fallback Tool Pie Menu | `wm.toolbar_fallback_pie` |  |
| Shift+Space Bar | Toolbar | `wm.toolbar` |  |

## Screen

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Timer 0 any | Animation Step | `screen.animation_step` |  |
| Any modifier+Timer Region any | Region Alpha | `screen.region_blend` |  |
| Ctrl+Tab | Cycle Space Context | `screen.space_context_cycle` | direction='NEXT' |
| Ctrl+Shift+Tab | Cycle Space Context | `screen.space_context_cycle` | direction='PREV' |
| Ctrl+Page Down | Cycle Workspace | `screen.workspace_cycle` | direction='NEXT' |
| Ctrl+Page Up | Cycle Workspace | `screen.workspace_cycle` | direction='PREV' |
| Ctrl+Alt+Q | Toggle Quad View | `screen.region_quadview` |  |
| Shift+R (repeat) | Repeat Last | `screen.repeat_last` |  |
| Return | Execute File Window | `file.execute` |  |
| Numpad Enter | Execute File Window | `file.execute` |  |
| Esc | Cancel File Operation | `file.cancel` |  |
| Ctrl+Z (repeat) | Undo Catalog Edits | `asset.catalog_undo` |  |
| Ctrl+Shift+Z (repeat) | Redo Catalog Edits | `asset.catalog_redo` |  |
| Ctrl+Z (repeat) | Undo | `ed.undo` |  |
| Ctrl+Shift+Z (repeat) | Redo | `ed.redo` |  |
| F12 | Render | `render.render` | use_viewport=True |
| Ctrl+F12 | Render | `render.render` | animation=True, use_viewport=True |
| Alt+F12 | Render | `render.render` | use_sequencer_scene=True, use_viewport=True |
| Ctrl+Alt+F12 | Render | `render.render` | animation=True, use_sequencer_scene=True, use_viewport=True |
| Esc | Cancel Render View | `render.view_cancel` |  |
| F11 | Show/Hide Render View | `render.view_show` |  |
| Ctrl+F11 | Play Rendered Animation | `render.play_rendered_anim` |  |
| Ctrl+Space Bar | Toggle Maximize Area | `screen.screen_full_area` |  |
| Ctrl+Alt+Space Bar | Toggle Maximize Area | `screen.screen_full_area` | use_hide_panels=True |
| F9 | Redo Last | `screen.redo_last` |  |
| Ctrl+, | Open Preferences... | `screen.userpref_show` |  |

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
| Shift+Left Mouse | Move Area Edges | `screen.area_move` |  |
| Right Mouse | Area Edge Options | `screen.area_options` |  |

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
| Middle Mouse | Pan View | `view2d.pan` |  |
| Shift+Middle Mouse | Pan View | `view2d.pan` |  |
| Mouse/Trackpad Pan any | Pan View | `view2d.pan` |  |
| Ctrl+Wheel Down | Scroll Right | `view2d.scroll_right` |  |
| Wheel Right | Scroll Right | `view2d.scroll_right` |  |
| Ctrl+Wheel Up | Scroll Left | `view2d.scroll_left` |  |
| Wheel Left | Scroll Left | `view2d.scroll_left` |  |
| Shift+Wheel Down | Scroll Down | `view2d.scroll_down` |  |
| Shift+Wheel Up | Scroll Up | `view2d.scroll_up` |  |
| NDOF Motion any | NDOF Pan/Zoom | `view2d.ndof` |  |
| Wheel Out | Zoom Out | `view2d.zoom_out` |  |
| Wheel In | Zoom In | `view2d.zoom_in` |  |
| Numpad - (repeat) | Zoom Out | `view2d.zoom_out` |  |
| Numpad + (repeat) | Zoom In | `view2d.zoom_in` |  |
| Ctrl+Mouse/Trackpad Pan any | Zoom 2D View | `view2d.zoom` |  |
| Any modifier+Timer 1 any | Smooth View 2D | `view2d.smoothview` |  |
| Wheel Down | Scroll Down | `view2d.scroll_down` |  |
| Wheel Up | Scroll Up | `view2d.scroll_up` |  |
| Wheel Down | Scroll Right | `view2d.scroll_right` |  |
| Wheel Up | Scroll Left | `view2d.scroll_left` |  |
| Ctrl+Middle Mouse | Zoom 2D View | `view2d.zoom` |  |
| Mouse/Trackpad Zoom any | Zoom 2D View | `view2d.zoom` |  |
| Shift+B | Zoom to Border | `view2d.zoom_border` |  |

## View2D Buttons List

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Scroller Activate | `view2d.scroller_activate` |  |
| Middle Mouse | Scroller Activate | `view2d.scroller_activate` |  |
| Middle Mouse | Pan View | `view2d.pan` |  |
| Mouse/Trackpad Pan any | Pan View | `view2d.pan` |  |
| Wheel Down | Scroll Down | `view2d.scroll_down` |  |
| Wheel Up | Scroll Up | `view2d.scroll_up` |  |
| Page Down (repeat) | Scroll Down | `view2d.scroll_down` | page=True |
| Page Up (repeat) | Scroll Up | `view2d.scroll_up` | page=True |
| Ctrl+Middle Mouse | Zoom 2D View | `view2d.zoom` |  |
| Mouse/Trackpad Zoom any | Zoom 2D View | `view2d.zoom` |  |
| Ctrl+Mouse/Trackpad Pan any | Zoom 2D View | `view2d.zoom` |  |
| Numpad - (repeat) | Zoom Out | `view2d.zoom_out` |  |
| Numpad + (repeat) | Zoom In | `view2d.zoom_in` |  |
| Home | Reset View | `view2d.reset` |  |

## User Interface

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| E | Eyedropper | `ui.eyedropper_color` |  |
| E | Eyedropper Colorband | `ui.eyedropper_colorramp` |  |
| Alt+E | Eyedropper Colorband (Points) | `ui.eyedropper_colorramp_point` |  |
| E | Eyedropper Data-Block | `ui.eyedropper_id` |  |
| E | Eyedropper Depth | `ui.eyedropper_depth` |  |
| E | Eyedropper Bone | `ui.eyedropper_bone` |  |
| Ctrl+Shift+C | Copy Data Path | `ui.copy_data_path_button` |  |
| Ctrl+Shift+Alt+C | Copy Data Path | `ui.copy_data_path_button` | full_path=True |
| I | Insert Keyframe (Buttons) | `anim.keyframe_insert_button` | all=True |
| Alt+I | Delete Keyframe (Buttons) | `anim.keyframe_delete_button` | all=True |
| Shift+Alt+I | Clear Keyframe (Buttons) | `anim.keyframe_clear_button` | all=True |
| Ctrl+D | Add Driver | `anim.driver_button_add` |  |
| Ctrl+Alt+D | Remove Driver | `anim.driver_button_remove` |  |
| K | Add to Keying Set | `anim.keyingset_button_add` |  |
| Alt+K | Remove from Keying Set | `anim.keyingset_button_remove` |  |
| Backspace | Reset to Default Value | `ui.reset_default_button` | all=True |
| Ctrl+F | List Filter | `ui.list_start_filter` |  |
| Ctrl+F | View Filter | `ui.view_start_filter` |  |
| Wheel Up any | View Scroll | `ui.view_scroll` |  |
| Wheel Down any | View Scroll | `ui.view_scroll` |  |
| Mouse/Trackpad Pan any | View Scroll | `ui.view_scroll` |  |
| Left Mouse | Select View Item | `ui.view_item_select` |  |
| Ctrl+Left Mouse | Select View Item | `ui.view_item_select` | extend=True |
| Shift+Left Mouse | Select View Item | `ui.view_item_select` | range_select=True |
| F2 | Rename View Item | `ui.view_item_rename` |  |
| X | Delete | `ui.view_item_delete` |  |
| Delete | Delete | `ui.view_item_delete` |  |
| Up Arrow (repeat) | View Navigate | `ui.view_item_navigate` | direction='UP' |
| Down Arrow (repeat) | View Navigate | `ui.view_item_navigate` | direction='DOWN' |
| Left Arrow (repeat) | View Navigate | `ui.view_item_navigate` | direction='LEFT' |
| Right Arrow (repeat) | View Navigate | `ui.view_item_navigate` | direction='RIGHT' |
| Numpad . | Focus Active Item | `ui.view_item_focus` |  |
| Button4 Mouse | Focus Active Item | `ui.view_item_focus` |  |
| Page Up (repeat) | Scroll page | `ui.view_item_page_scroll` | scroll_direction='UP' |
| Page Down (repeat) | Scroll page | `ui.view_item_page_scroll` | scroll_direction='DOWN' |
| Home | Scroll page | `ui.view_item_page_scroll` | scroll_direction='TOP' |
| End | Scroll page | `ui.view_item_page_scroll` | scroll_direction='BOTTOM' |
| Ctrl+F | Show Filter | `ui.region_start_filter` |  |
| Alt+F | Clear and Hide Filter | `ui.region_clear_filter` |  |

## Property Editor

Space `PROPERTIES`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Right Mouse | Context Menu | `buttons.context_menu` |  |
| Ctrl+Wheel Up | Cycle Space Context | `screen.space_context_cycle` | direction='PREV' |
| Ctrl+Wheel Down | Cycle Space Context | `screen.space_context_cycle` | direction='NEXT' |
| Ctrl+F | Filter | `buttons.start_filter` |  |
| Alt+F | Clear Filter | `buttons.clear_filter` |  |
| Left Mouse | Set Active Modifier | `object.modifier_set_active` |  |
| X | Remove Modifier | `object.modifier_remove` | report=True |
| Delete | Remove Modifier | `object.modifier_remove` | report=True |
| Shift+D | Copy Modifier | `object.modifier_copy` |  |
| Shift+A | Add Modifier | `object.add_modifier_menu` |  |
| Ctrl+A | Apply Modifier | `object.modifier_apply` | report=True |
| X | Remove Grease Pencil Effect | `object.shaderfx_remove` | report=True |
| Delete | Remove Grease Pencil Effect | `object.shaderfx_remove` | report=True |
| Shift+D | Copy Effect | `object.shaderfx_copy` |  |
| X | Delete Constraint | `constraint.delete` | report=True |
| Delete | Delete Constraint | `constraint.delete` | report=True |
| Shift+D | Duplicate Constraint | `constraint.copy` |  |
| Ctrl+A | Apply Constraint | `constraint.apply` | report=True |
| Shift+D | Duplicate Modifier | `sequencer.strip_modifier_duplicate` |  |
| Shift+A | Add Modifier | `sequencer.add_strip_modifier_menu` |  |
| Left Mouse | Set Active Strip Modifier | `sequencer.strip_modifier_set_active` |  |
| Left Mouse | Set Active Scene Effect | `scene.set_active_compositor_effect` |  |
| X | Remove Scene Effect | `scene.remove_compositor_effect` |  |
| Delete | Remove Scene Effect | `scene.remove_compositor_effect` |  |
| Shift+D | Duplicate Scene Effect | `scene.duplicate_compositor_effect` |  |
| Shift+A | Add Compositor Effect Menu | `scene.add_compositor_effect_menu` |  |

## Outliner

Space `OUTLINER`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Mouse Move any | Update Highlight | `outliner.highlight_update` |  |
| Left Mouse double click | Rename | `outliner.item_rename` |  |
| F2 | Rename | `outliner.item_rename` | use_active=True |
| Left Mouse click | Select | `outliner.item_activate` | deselect_all=True |
| Ctrl+Left Mouse click | Select | `outliner.item_activate` | extend=True, deselect_all=True |
| Shift+Left Mouse click | Select | `outliner.item_activate` | extend_range=True, deselect_all=True |
| Ctrl+Shift+Left Mouse click | Select | `outliner.item_activate` | extend=True, extend_range=True, deselect_all=True |
| Left Mouse double click | Select | `outliner.item_activate` | recurse=True, deselect_all=True |
| Ctrl+Left Mouse double click | Select | `outliner.item_activate` | recurse=True, extend=True, deselect_all=True |
| Shift+Left Mouse double click | Select | `outliner.item_activate` | recurse=True, extend_range=True, deselect_all=True |
| Ctrl+Shift+Left Mouse double click | Select | `outliner.item_activate` | recurse=True, extend=True, extend_range=True, deselect_all=True |
| B | Box Select | `outliner.select_box` |  |
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
| ` | Call Pie Menu | `wm.call_menu_pie` | name='OUTLINER_MT_view_pie' |
| Left Mouse drag | Drag and Drop | `outliner.item_drag_drop` |  |
| Shift+Left Mouse drag | Drag and Drop | `outliner.item_drag_drop` |  |
| Home | Show Hierarchy | `outliner.show_hierarchy` |  |
| . | Show Active | `outliner.show_active` |  |
| Numpad . | Show Active | `outliner.show_active` |  |
| Button4 Mouse | Show Active | `outliner.show_active` |  |
| Page Down (repeat) | Scroll Page | `outliner.scroll_page` | up=False |
| Page Up (repeat) | Scroll Page | `outliner.scroll_page` | up=True |
| Numpad + | Show/Hide One Level | `outliner.show_one_level` |  |
| Numpad - | Show/Hide One Level | `outliner.show_one_level` | open=False |
| A | Toggle Selected | `outliner.select_all` | action='SELECT' |
| Alt+A | Toggle Selected | `outliner.select_all` | action='DESELECT' |
| Ctrl+I | Toggle Selected | `outliner.select_all` | action='INVERT' |
| A double click | Toggle Selected | `outliner.select_all` | action='DESELECT' |
| Shift+A | Expand/Collapse All | `outliner.expanded_toggle` |  |
| K | Keying Set Add Selected | `outliner.keyingset_add_selected` |  |
| Alt+K | Keying Set Remove Selected | `outliner.keyingset_remove_selected` |  |
| I | Insert Keyframe | `anim.keyframe_insert` |  |
| Alt+I | Delete Keying-Set Keyframe | `anim.keyframe_delete` |  |
| Ctrl+D | Add Drivers for Selected | `outliner.drivers_add_selected` |  |
| Ctrl+Alt+D | Delete Drivers for Selected | `outliner.drivers_delete_selected` |  |
| C | New Collection | `outliner.collection_new` |  |
| X | Delete | `outliner.delete` |  |
| Delete | Delete | `outliner.delete` |  |
| M | Call Menu | `wm.call_menu` | name='OBJECT_MT_move_to_collection' |
| Shift+M | Call Menu | `wm.call_menu` | name='OBJECT_MT_link_to_collection' |
| E | Disable from View Layer | `outliner.collection_exclude_set` |  |
| Alt+E | Enable in View Layer | `outliner.collection_exclude_clear` |  |
| H | Hide | `outliner.hide` |  |
| Shift+H | Hide | `outliner.hide` | unselected=True |
| Alt+H | Unhide All | `outliner.unhide_all` |  |
| Ctrl+F | Filter | `outliner.start_filter` |  |
| Alt+F | Clear Filter | `outliner.clear_filter` |  |
| Ctrl+C | Outliner ID Data Copy | `outliner.id_copy` |  |
| Ctrl+V | Outliner ID Data Paste | `outliner.id_paste` |  |
| 1 | Hide Other Collections | `object.hide_collection` | collection_index=1, extend=False |
| 2 | Hide Other Collections | `object.hide_collection` | collection_index=2, extend=False |
| 3 | Hide Other Collections | `object.hide_collection` | collection_index=3, extend=False |
| 4 | Hide Other Collections | `object.hide_collection` | collection_index=4, extend=False |
| 5 | Hide Other Collections | `object.hide_collection` | collection_index=5, extend=False |
| 6 | Hide Other Collections | `object.hide_collection` | collection_index=6, extend=False |
| 7 | Hide Other Collections | `object.hide_collection` | collection_index=7, extend=False |
| 8 | Hide Other Collections | `object.hide_collection` | collection_index=8, extend=False |
| 9 | Hide Other Collections | `object.hide_collection` | collection_index=9, extend=False |
| 0 | Hide Other Collections | `object.hide_collection` | collection_index=10, extend=False |
| Alt+1 | Hide Other Collections | `object.hide_collection` | collection_index=11, extend=False |
| Alt+2 | Hide Other Collections | `object.hide_collection` | collection_index=12, extend=False |
| Alt+3 | Hide Other Collections | `object.hide_collection` | collection_index=13, extend=False |
| Alt+4 | Hide Other Collections | `object.hide_collection` | collection_index=14, extend=False |
| Alt+5 | Hide Other Collections | `object.hide_collection` | collection_index=15, extend=False |
| Alt+6 | Hide Other Collections | `object.hide_collection` | collection_index=16, extend=False |
| Alt+7 | Hide Other Collections | `object.hide_collection` | collection_index=17, extend=False |
| Alt+8 | Hide Other Collections | `object.hide_collection` | collection_index=18, extend=False |
| Alt+9 | Hide Other Collections | `object.hide_collection` | collection_index=19, extend=False |
| Alt+0 | Hide Other Collections | `object.hide_collection` | collection_index=20, extend=False |
| Shift+1 | Hide Other Collections | `object.hide_collection` | collection_index=1, extend=True |
| Shift+2 | Hide Other Collections | `object.hide_collection` | collection_index=2, extend=True |
| Shift+3 | Hide Other Collections | `object.hide_collection` | collection_index=3, extend=True |
| Shift+4 | Hide Other Collections | `object.hide_collection` | collection_index=4, extend=True |
| Shift+5 | Hide Other Collections | `object.hide_collection` | collection_index=5, extend=True |
| Shift+6 | Hide Other Collections | `object.hide_collection` | collection_index=6, extend=True |
| Shift+7 | Hide Other Collections | `object.hide_collection` | collection_index=7, extend=True |
| Shift+8 | Hide Other Collections | `object.hide_collection` | collection_index=8, extend=True |
| Shift+9 | Hide Other Collections | `object.hide_collection` | collection_index=9, extend=True |
| Shift+0 | Hide Other Collections | `object.hide_collection` | collection_index=10, extend=True |
| Shift+Alt+1 | Hide Other Collections | `object.hide_collection` | collection_index=11, extend=True |
| Shift+Alt+2 | Hide Other Collections | `object.hide_collection` | collection_index=12, extend=True |
| Shift+Alt+3 | Hide Other Collections | `object.hide_collection` | collection_index=13, extend=True |
| Shift+Alt+4 | Hide Other Collections | `object.hide_collection` | collection_index=14, extend=True |
| Shift+Alt+5 | Hide Other Collections | `object.hide_collection` | collection_index=15, extend=True |
| Shift+Alt+6 | Hide Other Collections | `object.hide_collection` | collection_index=16, extend=True |
| Shift+Alt+7 | Hide Other Collections | `object.hide_collection` | collection_index=17, extend=True |
| Shift+Alt+8 | Hide Other Collections | `object.hide_collection` | collection_index=18, extend=True |
| Shift+Alt+9 | Hide Other Collections | `object.hide_collection` | collection_index=19, extend=True |
| Shift+Alt+0 | Hide Other Collections | `object.hide_collection` | collection_index=20, extend=True |

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

## UV Editor

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+Tab | Call Menu | `wm.call_menu` | name='IMAGE_MT_uvs_select_mode' |
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
| Shift+Left Mouse click | Select | `uv.select` | toggle=True |
| Ctrl+E | Mark Seam | `uv.mark_seam` |  |
| Alt+Left Mouse click | Loop Select | `uv.select_loop` |  |
| Shift+Alt+Left Mouse click | Loop Select | `uv.select_loop` | extend=True |
| Ctrl+Alt+Left Mouse click | Edge Ring Select | `uv.select_edge_ring` |  |
| Ctrl+Shift+Alt+Left Mouse click | Edge Ring Select | `uv.select_edge_ring` | extend=True |
| Ctrl+Left Mouse click | Pick Shortest Path | `uv.shortest_path_pick` | use_fill=False |
| Ctrl+Shift+Left Mouse click | Pick Shortest Path | `uv.shortest_path_pick` | use_fill=True |
| Y | Select Split | `uv.select_split` |  |
| B | Box Select | `uv.select_box` | pinned=False |
| Alt+B | Box Select | `uv.select_box` | pinned=True |
| C | Circle Select | `uv.select_circle` |  |
| Ctrl+Right Mouse drag | Lasso Select UV | `uv.select_lasso` | mode='ADD' |
| Ctrl+Shift+Right Mouse drag | Lasso Select UV | `uv.select_lasso` | mode='SUB' |
| Ctrl+L | Select Linked | `uv.select_linked` |  |
| L | Select Linked Pick | `uv.select_linked_pick` | extend=True, deselect=False |
| Shift+L | Select Linked Pick | `uv.select_linked_pick` | deselect=True |
| Ctrl+Numpad + (repeat) | Select More | `uv.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `uv.select_less` |  |
| Shift+G | Select Similar | `uv.select_similar` |  |
| A | (De)select All | `uv.select_all` | action='SELECT' |
| Alt+A | (De)select All | `uv.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `uv.select_all` | action='INVERT' |
| A double click | (De)select All | `uv.select_all` | action='DESELECT' |
| Alt+H | Reveal Hidden | `uv.reveal` |  |
| H | Hide Selected | `uv.hide` | unselected=False |
| Shift+H | Hide Selected | `uv.hide` | unselected=True |
| Shift+P | Selected Pinned | `uv.select_pinned` |  |
| M | Call Menu | `wm.call_menu` | name='IMAGE_MT_uvs_merge' |
| Alt+M | Call Menu | `wm.call_menu` | name='IMAGE_MT_uvs_split' |
| Shift+W | Call Menu | `wm.call_menu` | name='IMAGE_MT_uvs_align' |
| Ctrl+Numpad 8 | Move on Axis | `uv.move_on_axis` | axis='Y', type='DYNAMIC', distance=1 |
| Ctrl+Numpad 2 | Move on Axis | `uv.move_on_axis` | axis='Y', type='DYNAMIC', distance=-1 |
| Ctrl+Numpad 6 | Move on Axis | `uv.move_on_axis` | axis='X', type='DYNAMIC', distance=1 |
| Ctrl+Numpad 4 | Move on Axis | `uv.move_on_axis` | axis='X', type='DYNAMIC', distance=-1 |
| Shift+Numpad 8 | Move on Axis | `uv.move_on_axis` | axis='Y', type='PIXEL', distance=1 |
| Shift+Numpad 2 | Move on Axis | `uv.move_on_axis` | axis='Y', type='PIXEL', distance=-1 |
| Shift+Numpad 6 | Move on Axis | `uv.move_on_axis` | axis='X', type='PIXEL', distance=1 |
| Shift+Numpad 4 | Move on Axis | `uv.move_on_axis` | axis='X', type='PIXEL', distance=-1 |
| Numpad 8 | Move on Axis | `uv.move_on_axis` | axis='Y', type='UDIM', distance=1 |
| Numpad 2 | Move on Axis | `uv.move_on_axis` | axis='Y', type='UDIM', distance=-1 |
| Numpad 6 | Move on Axis | `uv.move_on_axis` | axis='X', type='UDIM', distance=1 |
| Numpad 4 | Move on Axis | `uv.move_on_axis` | axis='X', type='UDIM', distance=-1 |
| Alt+V | Stitch | `uv.stitch` |  |
| V | Rip Move UVs | `uv.rip_move` |  |
| P | Pin | `uv.pin` | clear=False |
| Alt+P | Pin | `uv.pin` | clear=True |
| Ctrl+C | Copy UVs | `uv.copy` |  |
| Ctrl+V | Paste UVs | `uv.paste` |  |
| Ctrl+B | Set User Region | `uv.custom_region_set` |  |
| Ctrl+Alt+B | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_uv_custom_region' |
| U | Call Menu | `wm.call_menu` | name='IMAGE_MT_uvs_unwrap' |
| Shift+S | Call Pie Menu | `wm.call_menu_pie` | name='IMAGE_MT_uvs_snap_pie' |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Ctrl+Shift+Alt+S | Shear | `transform.shear` |  |
| Shift+Tab | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_snap_uv' |
| Ctrl+Shift+Tab | Context Enum Menu | `wm.context_menu_enum` | data_path='tool_settings.snap_uv_element' |
| Ctrl+` | Context Toggle | `wm.context_toggle` | data_path='space_data.show_gizmo' |
| Shift+Alt+Z | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.show_overlays' |
| Right Mouse | Call Menu | `wm.call_menu` | name='IMAGE_MT_uvs_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='IMAGE_MT_uvs_context_menu' |
| Shift+Right Mouse | Set 2D Cursor | `uv.cursor_set` |  |
| Shift+Right Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |

## 3D View Generic

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |

## 3D View

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Shift+Right Mouse | Set 3D Cursor | `view3d.cursor3d` |  |
| Shift+Right Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |
| Numpad / | Local View | `view3d.localview` |  |
| / | Local View | `view3d.localview` |  |
| Mouse/Trackpad Smart Zoom any | Local View | `view3d.localview` |  |
| Alt+Numpad / | Remove from Local View | `view3d.localview_remove_from` |  |
| Alt+/ | Remove from Local View | `view3d.localview_remove_from` |  |
| Mouse/Trackpad Rotate any | Rotate View | `view3d.rotate` |  |
| Middle Mouse | Rotate View | `view3d.rotate` |  |
| Shift+Middle Mouse | Pan View | `view3d.move` |  |
| Mouse/Trackpad Pan any | Rotate View | `view3d.rotate` |  |
| Shift+Mouse/Trackpad Pan any | Pan View | `view3d.move` |  |
| Wheel Left | Pan View Direction | `view3d.view_pan` | type='PANLEFT' |
| Wheel Right | Pan View Direction | `view3d.view_pan` | type='PANRIGHT' |
| Ctrl+Middle Mouse | Zoom View | `view3d.zoom` |  |
| Ctrl+Shift+Middle Mouse | Dolly View | `view3d.dolly` |  |
| Ctrl+Numpad . | Frame Selected | `view3d.view_selected` | use_all_regions=True |
| Numpad . | Frame Selected | `view3d.view_selected` |  |
| Button4 Mouse | Frame Selected | `view3d.view_selected` |  |
| Any modifier+Timer 1 any | Smooth View | `view3d.smoothview` |  |
| Mouse/Trackpad Zoom any | Zoom View | `view3d.zoom` |  |
| Ctrl+Mouse/Trackpad Pan any | Zoom View | `view3d.zoom` |  |
| Numpad + (repeat) | Zoom View | `view3d.zoom` | delta=1 |
| Numpad - (repeat) | Zoom View | `view3d.zoom` | delta=-1 |
| Ctrl+= (repeat) | Zoom View | `view3d.zoom` | delta=1 |
| Ctrl+- (repeat) | Zoom View | `view3d.zoom` | delta=-1 |
| Wheel In | Zoom View | `view3d.zoom` | delta=1 |
| Wheel Out | Zoom View | `view3d.zoom` | delta=-1 |
| Shift+Numpad + (repeat) | Dolly View | `view3d.dolly` | delta=1 |
| Shift+Numpad - (repeat) | Dolly View | `view3d.dolly` | delta=-1 |
| Ctrl+Shift+= (repeat) | Dolly View | `view3d.dolly` | delta=1 |
| Ctrl+Shift+- (repeat) | Dolly View | `view3d.dolly` | delta=-1 |
| Home | Frame Camera Bounds | `view3d.view_center_camera` |  |
| Home | View Lock Center | `view3d.view_center_lock` |  |
| Home | Frame All | `view3d.view_all` | center=False |
| Ctrl+Home | Frame All | `view3d.view_all` | use_all_regions=True, center=False |
| Shift+C | Frame All | `view3d.view_all` | center=True |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_view_pie' |
| Shift+` | View Navigation (Walk/Fly) | `view3d.navigate` |  |
| Numpad 0 | View Camera | `view3d.view_camera` |  |
| Numpad 1 | View Axis | `view3d.view_axis` | type='FRONT' |
| Numpad 3 | View Axis | `view3d.view_axis` | type='RIGHT' |
| Numpad 7 | View Axis | `view3d.view_axis` | type='TOP' |
| Ctrl+Numpad 1 | View Axis | `view3d.view_axis` | type='BACK' |
| Ctrl+Numpad 3 | View Axis | `view3d.view_axis` | type='LEFT' |
| Ctrl+Numpad 7 | View Axis | `view3d.view_axis` | type='BOTTOM' |
| Numpad 2 (repeat) | View Orbit | `view3d.view_orbit` | type='ORBITDOWN' |
| Numpad 4 (repeat) | View Orbit | `view3d.view_orbit` | type='ORBITLEFT' |
| Numpad 5 | View Perspective/Orthographic | `view3d.view_persportho` |  |
| Numpad 6 (repeat) | View Orbit | `view3d.view_orbit` | type='ORBITRIGHT' |
| Numpad 8 (repeat) | View Orbit | `view3d.view_orbit` | type='ORBITUP' |
| Ctrl+Numpad 2 (repeat) | Pan View Direction | `view3d.view_pan` | type='PANDOWN' |
| Ctrl+Numpad 4 (repeat) | Pan View Direction | `view3d.view_pan` | type='PANLEFT' |
| Ctrl+Numpad 6 (repeat) | Pan View Direction | `view3d.view_pan` | type='PANRIGHT' |
| Ctrl+Numpad 8 (repeat) | Pan View Direction | `view3d.view_pan` | type='PANUP' |
| Shift+Numpad 4 (repeat) | View Roll | `view3d.view_roll` | type='LEFT' |
| Shift+Numpad 6 (repeat) | View Roll | `view3d.view_roll` | type='RIGHT' |
| Numpad 9 | View Orbit | `view3d.view_orbit` | angle=3.141592653589793, type='ORBITRIGHT' |
| Shift+Numpad 1 | View Axis | `view3d.view_axis` | type='FRONT', align_active=True |
| Shift+Numpad 3 | View Axis | `view3d.view_axis` | type='RIGHT', align_active=True |
| Shift+Numpad 7 | View Axis | `view3d.view_axis` | type='TOP', align_active=True |
| Ctrl+Shift+Numpad 1 | View Axis | `view3d.view_axis` | type='BACK', align_active=True |
| Ctrl+Shift+Numpad 3 | View Axis | `view3d.view_axis` | type='LEFT', align_active=True |
| Ctrl+Shift+Numpad 7 | View Axis | `view3d.view_axis` | type='BOTTOM', align_active=True |
| Alt+Middle Mouse drag north | View Axis | `view3d.view_axis` | type='TOP', relative=True |
| Alt+Middle Mouse drag south | View Axis | `view3d.view_axis` | type='BOTTOM', relative=True |
| Alt+Middle Mouse drag east | View Axis | `view3d.view_axis` | type='RIGHT', relative=True |
| Alt+Middle Mouse drag west | View Axis | `view3d.view_axis` | type='LEFT', relative=True |
| Alt+Middle Mouse click | Center View to Mouse | `view3d.view_center_pick` |  |
| NDOF Motion any | NDOF Orbit View with Zoom | `view3d.ndof_orbit_zoom` |  |
| Ctrl+NDOF Motion any | NDOF Orbit View | `view3d.ndof_orbit` |  |
| Shift+NDOF Motion any | NDOF Pan View | `view3d.ndof_pan` |  |
| Ctrl+Shift+NDOF Motion any | NDOF Transform View | `view3d.ndof_all` |  |
| NDOF Fit | Frame Selected | `view3d.view_selected` |  |
| NDOF Roll CW | View Roll | `view3d.view_roll` | angle=1.5707963267948966 |
| NDOF Roll CCW | View Roll | `view3d.view_roll` | angle=-1.5707963267948966 |
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
| Alt+Left Mouse click | Select | `view3d.select` | enumerate=True |
| Ctrl+Shift+Left Mouse click | Select | `view3d.select` | toggle=True, center=True |
| Ctrl+Alt+Left Mouse click | Select | `view3d.select` | center=True, enumerate=True |
| Shift+Alt+Left Mouse click | Select | `view3d.select` | toggle=True, enumerate=True |
| Ctrl+Shift+Alt+Left Mouse click | Select | `view3d.select` | toggle=True, center=True, enumerate=True |
| B | Box Select | `view3d.select_box` |  |
| Ctrl+Right Mouse drag | Lasso Select | `view3d.select_lasso` | mode='ADD' |
| Ctrl+Shift+Right Mouse drag | Lasso Select | `view3d.select_lasso` | mode='SUB' |
| C | Circle Select | `view3d.select_circle` |  |
| Alt+B | Clipping Region | `view3d.clip_border` |  |
| Shift+B | Zoom to Border | `view3d.zoom_border` |  |
| Ctrl+B | Set Render Region | `view3d.render_border` |  |
| Ctrl+Alt+B | Clear Render Region | `view3d.clear_render_border` |  |
| Ctrl+Alt+Numpad 0 | Align Camera to View | `view3d.camera_to_view` |  |
| Ctrl+Numpad 0 | Set Active Object as Camera | `view3d.object_as_camera` |  |
| Ctrl+C | Copy Objects | `view3d.copybuffer` |  |
| Ctrl+V | Paste Objects | `view3d.pastebuffer` |  |
| Shift+Tab | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_snap' |
| Ctrl+Shift+Tab | Call Panel | `wm.call_panel` | name='VIEW3D_PT_snapping', keep_open=True |
| Shift+S | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_snap_pie' |
| Ctrl+` | Context Toggle | `wm.context_toggle` | data_path='space_data.show_gizmo' |
| . | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_pivot_pie' |
| , | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_orientations_pie' |
| Z | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_shading_pie' |
| Shift+Z | Toggle Shading Type | `view3d.toggle_shading` | type='WIREFRAME' |
| Alt+Z | Toggle X-Ray | `view3d.toggle_xray` |  |
| Shift+Alt+Z | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.show_overlays' |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |

## Mask Editing

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Alt+N | New Mask | `mask.new` |  |
| Shift+A | Call Menu | `wm.call_menu` | name='MASK_MT_add' |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit_mask' |
| Ctrl+Left Mouse | Add Vertex and Slide | `mask.add_vertex_slide` |  |
| Ctrl+Shift+Left Mouse | Add Feather Vertex and Slide | `mask.add_feather_vertex_slide` |  |
| X | Delete | `mask.delete` |  |
| Delete | Delete | `mask.delete` |  |
| Shift+Left Mouse | Select | `mask.select` | toggle=True |
| A | (De)select All | `mask.select_all` | action='SELECT' |
| Alt+A | (De)select All | `mask.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `mask.select_all` | action='INVERT' |
| A double click | (De)select All | `mask.select_all` | action='DESELECT' |
| Ctrl+L | Select Linked All | `mask.select_linked` |  |
| L | Select Linked | `mask.select_linked_pick` | deselect=False |
| Shift+L | Select Linked | `mask.select_linked_pick` | deselect=True |
| B | Box Select | `mask.select_box` |  |
| C | Circle Select | `mask.select_circle` |  |
| Ctrl+Alt+Right Mouse drag | Lasso Select | `mask.select_lasso` | mode='ADD' |
| Ctrl+Shift+Alt+Right Mouse drag | Lasso Select | `mask.select_lasso` | mode='SUB' |
| Ctrl+Numpad + (repeat) | Select More | `mask.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `mask.select_less` |  |
| Alt+H | Clear Restrict View | `mask.hide_view_clear` |  |
| H | Set Restrict View | `mask.hide_view_set` | unselected=False |
| Shift+H | Set Restrict View | `mask.hide_view_set` | unselected=True |
| Ctrl+Left Mouse | Select | `clip.select` |  |
| Alt+C | Toggle Cyclic | `mask.cyclic_toggle` |  |
| Left Mouse | Slide Point | `mask.slide_point` |  |
| Left Mouse | Slide Spline Curvature | `mask.slide_spline_curvature` |  |
| V | Set Handle Type | `mask.handle_type_set` |  |
| Shift+N | Recalculate Handles | `mask.normals_make_consistent` |  |
| Ctrl+P | Make Parent | `mask.parent_set` |  |
| Alt+P | Clear Parent | `mask.parent_clear` |  |
| I | Insert Shape Key | `mask.shape_key_insert` |  |
| Alt+I | Clear Shape Key | `mask.shape_key_clear` |  |
| Shift+D | Add Duplicate | `mask.duplicate_move` |  |
| Ctrl+C | Copy Splines | `mask.copy_splines` |  |
| Ctrl+V | Paste Splines | `mask.paste_splines` |  |
| M | Move to Layer | `mask.move_to_layer` |  |
| G | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Shift+Alt+S | To Sphere | `transform.tosphere` |  |
| Ctrl+Shift+Alt+S | Shear | `transform.shear` |  |
| Alt+S | Transform | `transform.transform` | mode='MASK_SHRINKFATTEN' |
| Shift+Right Mouse | Set 2D Cursor | `uv.cursor_set` |  |
| Shift+Right Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## Markers

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| M | Add Time Marker | `marker.add` |  |
| Left Mouse drag | Move Time Marker | `marker.move` | tweak=True |
| Shift+D | Duplicate Time Marker | `marker.duplicate` |  |
| Left Mouse | Select Time Marker | `marker.select` |  |
| Shift+Left Mouse | Select Time Marker | `marker.select` | extend=True |
| Ctrl+Left Mouse | Select Time Marker | `marker.select` | camera=True |
| Ctrl+Shift+Left Mouse | Select Time Marker | `marker.select` | extend=True, camera=True |
| Left Mouse drag | Marker Box Select | `marker.select_box` | tweak=True |
| Ctrl+Left Mouse click | Select Markers Before/After Current Frame | `marker.select_leftright` | mode='CLICK_SIDE', extend=False |
| Ctrl+Shift+Left Mouse click | Select Markers Before/After Current Frame | `marker.select_leftright` | mode='CLICK_SIDE', extend=True |
| [ | Select Markers Before/After Current Frame | `marker.select_leftright` | mode='LEFT', extend=False |
| ] | Select Markers Before/After Current Frame | `marker.select_leftright` | mode='RIGHT', extend=False |
| Shift+Left Mouse drag | Marker Box Select | `marker.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Marker Box Select | `marker.select_box` | tweak=True, mode='SUB' |
| B | Marker Box Select | `marker.select_box` |  |
| A | (De)select all Markers | `marker.select_all` | action='SELECT' |
| Alt+A | (De)select all Markers | `marker.select_all` | action='DESELECT' |
| Ctrl+I | (De)select all Markers | `marker.select_all` | action='INVERT' |
| A double click | (De)select all Markers | `marker.select_all` | action='DESELECT' |
| X | Delete Markers | `marker.delete` |  |
| Delete | Delete Markers | `marker.delete` | confirm=False |
| F2 | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name_marker', keep_open=False |
| Left Mouse double click | Call Panel | `wm.call_panel` | name='TOPBAR_PT_name_marker', keep_open=False |
| G | Move Time Marker | `marker.move` |  |
| Ctrl+B | Bind Camera to Markers | `marker.camera_bind` |  |

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

## Graph Editor Generic

Space `GRAPH_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Shift+E | Set F-Curve Extrapolation | `graph.extrapolation_type` |  |
| Ctrl+Shift+M | Add F-Curve Modifier | `graph.fmodifier_add` | only_active=False |
| Ctrl+F | Filter Channels | `anim.channels_select_filter` |  |
| Alt+H | Reveal Curves | `graph.reveal` |  |
| H | Hide Curves | `graph.hide` | unselected=False |
| Shift+H | Hide Curves | `graph.hide` | unselected=True |
| Ctrl+Tab | Cycle Space Type Set | `screen.space_type_set_or_cycle` | space_type='DOPESHEET_EDITOR' |
| / | Local View | `graph.local_view` |  |
| Numpad / | Local View | `graph.local_view` |  |

## Graph Editor

Space `GRAPH_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+H | Context Toggle | `wm.context_toggle` | data_path='space_data.show_handles' |
| Shift+Tab | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_snap_anim' |
| Left Mouse | Select Keyframes | `graph.clickselect` | deselect_all=True |
| Alt+Left Mouse | Select Keyframes | `graph.clickselect` | column=True |
| Shift+Left Mouse | Select Keyframes | `graph.clickselect` | extend=True |
| Shift+Alt+Left Mouse | Select Keyframes | `graph.clickselect` | extend=True, column=True |
| Ctrl+Alt+Left Mouse | Select Keyframes | `graph.clickselect` | curves=True |
| Ctrl+Shift+Alt+Left Mouse | Select Keyframes | `graph.clickselect` | extend=True, curves=True |
| Ctrl+Left Mouse click | Select Left/Right | `graph.select_leftright` | mode='CHECK' |
| Ctrl+Shift+Left Mouse click | Select Left/Right | `graph.select_leftright` | mode='CHECK', extend=True |
| [ | Select Left/Right | `graph.select_leftright` | mode='LEFT' |
| ] | Select Left/Right | `graph.select_leftright` | mode='RIGHT' |
| A | Select All | `graph.select_all` | action='SELECT' |
| Alt+A | Select All | `graph.select_all` | action='DESELECT' |
| Ctrl+I | Select All | `graph.select_all` | action='INVERT' |
| A double click | Select All | `graph.select_all` | action='DESELECT' |
| B | Box Select | `graph.select_box` |  |
| Alt+B | Box Select | `graph.select_box` | axis_range=True |
| Left Mouse drag | Box Select | `graph.select_box` | tweak=True, mode='SET' |
| Shift+Left Mouse drag | Box Select | `graph.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `graph.select_box` | tweak=True, mode='SUB' |
| Ctrl+Right Mouse drag | Lasso Select | `graph.select_lasso` | mode='ADD' |
| Ctrl+Shift+Right Mouse drag | Lasso Select | `graph.select_lasso` | mode='SUB' |
| C | Circle Select | `graph.select_circle` |  |
| K | Select All | `graph.select_column` | mode='KEYS' |
| Ctrl+K | Select All | `graph.select_column` | mode='CFRA' |
| Shift+K | Select All | `graph.select_column` | mode='MARKERS_COLUMN' |
| Alt+K | Select All | `graph.select_column` | mode='MARKERS_BETWEEN' |
| Ctrl+Numpad + (repeat) | Select More | `graph.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `graph.select_less` |  |
| L | Select Linked | `graph.select_linked` |  |
| Ctrl+G | Jump to Keyframes | `graph.frame_jump` |  |
| Shift+S | Call Pie Menu | `wm.call_menu_pie` | name='GRAPH_MT_snap_pie' |
| Ctrl+M | Mirror Keys | `graph.mirror` |  |
| V | Set Keyframe Handle Type | `graph.handle_type` |  |
| T | Set Keyframe Interpolation | `graph.interpolation_type` |  |
| Ctrl+E | Set Keyframe Easing Type | `graph.easing_type` |  |
| Alt+O | Smooth Keys | `graph.smooth` |  |
| Shift+Alt+O | Bake Keyframes | `graph.bake_keys` |  |
| Alt+C | Keys to Samples | `graph.keys_to_samples` |  |
| X | Call Menu | `wm.call_menu` | name='GRAPH_MT_delete' |
| Delete | Delete Keyframes | `graph.delete` | confirm=False |
| Shift+D | Duplicate | `graph.duplicate_move` |  |
| I | Insert Keyframes | `graph.keyframe_insert` |  |
| Ctrl+Right Mouse click | Click-Insert Keyframes | `graph.click_insert` |  |
| Ctrl+Shift+Right Mouse click | Click-Insert Keyframes | `graph.click_insert` | extend=True |
| Ctrl+C | Copy Keyframes | `graph.copy` |  |
| Ctrl+V | Paste Keyframes | `graph.paste` |  |
| Ctrl+Shift+V | Paste Keyframes | `graph.paste` | flipped=True |
| Alt+S | Call Menu | `wm.call_menu` | name='GRAPH_MT_key_smoothing' |
| Alt+D | Call Menu | `wm.call_menu` | name='GRAPH_MT_key_blending' |
| Ctrl+Alt+P | Set Preview Range to Selected | `graph.previewrange_set` |  |
| Home | Frame All | `graph.view_all` |  |
| NDOF Fit | Frame All | `graph.view_all` |  |
| Numpad . | Frame Selected | `graph.view_selected` |  |
| Button4 Mouse | Frame Selected | `graph.view_selected` |  |
| Numpad 0 | Go to Current Frame | `graph.view_frame` |  |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='GRAPH_MT_view_pie' |
| Tab | Toggle Channel Editability | `anim.channels_editable_toggle` |  |
| G | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| E | Transform | `transform.transform` | mode='TIME_EXTEND' |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_fcurve' |
| M | Add Time Marker | `marker.add` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='GRAPH_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='GRAPH_MT_context_menu' |
| . | Call Pie Menu | `wm.call_menu_pie` | name='GRAPH_MT_pivot_pie' |
| Shift+Right Mouse | Set Cursor | `graph.cursor_set` |  |

## Image Generic

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Alt+N | New Image | `image.new` |  |
| Alt+O | Open Image | `image.open` |  |
| Alt+R | Reload Image | `image.reload` |  |
| Ctrl+R | Open Cached Render | `image.read_viewlayers` |  |
| Alt+S | Save Image | `image.save` |  |
| J (repeat) | Cycle Render Slot | `image.cycle_render_slot` |  |
| Alt+J (repeat) | Cycle Render Slot | `image.cycle_render_slot` | reverse=True |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='IMAGE_MT_view_pie' |
| Shift+Alt+S | Save As Image | `image.save_as` |  |

## Image

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Home | Frame All | `image.view_all` |  |
| Shift+Home | Frame All | `image.view_all` | fit_view=True |
| Numpad . | View Center | `image.view_selected` |  |
| Button4 Mouse | View Center | `image.view_selected` |  |
| Shift+C | Cursor To Center View | `image.view_cursor_center` |  |
| Middle Mouse | Pan View | `image.view_pan` |  |
| Shift+Middle Mouse | Pan View | `image.view_pan` |  |
| Mouse/Trackpad Pan any | Pan View | `image.view_pan` |  |
| NDOF Fit | Frame All | `image.view_all` |  |
| NDOF Motion any | NDOF Pan/Zoom | `image.view_ndof` |  |
| Wheel In | Zoom In | `image.view_zoom_in` |  |
| Wheel Out | Zoom Out | `image.view_zoom_out` |  |
| Numpad + (repeat) | Zoom In | `image.view_zoom_in` |  |
| Numpad - (repeat) | Zoom Out | `image.view_zoom_out` |  |
| Ctrl+Middle Mouse | Zoom View | `image.view_zoom` |  |
| Mouse/Trackpad Zoom any | Zoom View | `image.view_zoom` |  |
| Ctrl+Mouse/Trackpad Pan any | Zoom View | `image.view_zoom` |  |
| Shift+B | Zoom to Border | `image.view_zoom_border` |  |
| Numpad 1 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=1.0 |
| Numpad 2 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=0.5 |
| Numpad 4 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=0.25 |
| Numpad 8 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=0.125 |
| Ctrl+Numpad 1 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=1.0 |
| Ctrl+Numpad 2 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=2.0 |
| Ctrl+Numpad 4 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=4.0 |
| Ctrl+Numpad 8 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=8.0 |
| Shift+Numpad 1 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=1.0 |
| Shift+Numpad 2 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=2.0 |
| Shift+Numpad 4 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=4.0 |
| Shift+Numpad 8 | View Zoom Ratio | `image.view_zoom_ratio` | ratio=8.0 |
| Left Mouse | Change Frame | `image.change_frame` |  |
| Right Mouse | Sample Color | `image.sample` |  |
| Ctrl+Right Mouse | Set Curves Point | `image.curves_point_set` | point='BLACK_POINT' |
| Shift+Right Mouse | Set Curves Point | `image.curves_point_set` | point='WHITE_POINT' |
| Tab | Set Object Mode | `object.mode_set` | mode='EDIT', toggle=True |
| 1 | Context Set | `wm.context_set_int` | data_path='space_data.image.render_slots.active_index', value=0 |
| 2 | Context Set | `wm.context_set_int` | data_path='space_data.image.render_slots.active_index', value=1 |
| 3 | Context Set | `wm.context_set_int` | data_path='space_data.image.render_slots.active_index', value=2 |
| 4 | Context Set | `wm.context_set_int` | data_path='space_data.image.render_slots.active_index', value=3 |
| 5 | Context Set | `wm.context_set_int` | data_path='space_data.image.render_slots.active_index', value=4 |
| 6 | Context Set | `wm.context_set_int` | data_path='space_data.image.render_slots.active_index', value=5 |
| 7 | Context Set | `wm.context_set_int` | data_path='space_data.image.render_slots.active_index', value=6 |
| 8 | Context Set | `wm.context_set_int` | data_path='space_data.image.render_slots.active_index', value=7 |
| 9 | Context Set | `wm.context_set_int` | data_path='space_data.image.render_slots.active_index', value=8 |
| Ctrl+B | Render Region | `image.render_border` |  |
| Ctrl+Alt+B | Clear Render Region | `image.clear_render_border` |  |
| Ctrl+` | Context Toggle | `wm.context_toggle` | data_path='space_data.show_gizmo' |
| Shift+Alt+Z | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.show_overlays' |
| Right Mouse | Call Menu | `wm.call_menu` | name='IMAGE_MT_mask_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='IMAGE_MT_mask_context_menu' |
| . | Call Pie Menu | `wm.call_menu_pie` | name='IMAGE_MT_pivot_pie' |

## Node Generic

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |

## Node Editor

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse click | Select | `node.select` | select_passthrough=True |
| Ctrl+Left Mouse click | Select | `node.select` |  |
| Alt+Left Mouse click | Select | `node.select` |  |
| Ctrl+Alt+Left Mouse click | Select | `node.select` |  |
| Shift+Left Mouse click | Select | `node.select` | toggle=True |
| Ctrl+Shift+Left Mouse click | Select | `node.select` | toggle=True |
| Shift+Alt+Left Mouse click | Select | `node.select` | toggle=True |
| Ctrl+Shift+Alt+Left Mouse click | Select | `node.select` | toggle=True |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |
| Left Mouse drag | Box Select | `node.select_box` | tweak=True |
| Ctrl+Alt+Left Mouse drag | Lasso Select | `node.select_lasso` | mode='ADD' |
| Ctrl+Shift+Alt+Left Mouse drag | Lasso Select | `node.select_lasso` | mode='SUB' |
| B | Box Select | `node.select_box` | tweak=False |
| C | Circle Select | `node.select_circle` |  |
| Left Mouse drag | Link Nodes | `node.link` | detach=False |
| Ctrl+Left Mouse drag | Link Nodes | `node.link` | detach=True |
| Left Mouse drag | Resize Node | `node.resize` |  |
| Shift+Right Mouse drag | Add Reroute | `node.add_reroute` |  |
| Ctrl+Right Mouse drag | Cut Links | `node.links_cut` |  |
| Ctrl+Alt+Right Mouse drag | Mute Links | `node.links_mute` |  |
| Ctrl+Shift+Left Mouse | Link Viewer | `node.select_link_viewer` |  |
| Shift+Alt+Left Mouse | Connect to Output | `node.connect_to_output` | run_in_geometry_nodes=True |
| Ctrl+Shift+Left Mouse | Connect to Output | `node.connect_to_output` | run_in_geometry_nodes=False |
| Shift+Alt+Left Mouse | Connect to Output | `node.connect_to_output` | run_in_geometry_nodes=False |
| Alt+Middle Mouse | Background Image Move | `node.backimage_move` |  |
| V (repeat) | Background Image Zoom | `node.backimage_zoom` | factor=0.8333333333333334 |
| Alt+V (repeat) | Background Image Zoom | `node.backimage_zoom` | factor=1.2 |
| Alt+Home | Background Image Fit | `node.backimage_fit` |  |
| Alt+Right Mouse | Backimage Sample | `node.backimage_sample` |  |
| J | Make Links | `node.link_make` | replace=False |
| Shift+J | Make Links | `node.link_make` | replace=True |
| Ctrl+J | Join Nodes | `node.join_nodes` |  |
| Shift+A | Call Menu | `wm.call_menu` | name='NODE_MT_add' |
| Shift+S | Call Menu | `wm.call_menu` | name='NODE_MT_swap' |
| Shift+D | Duplicate | `node.duplicate_move` | NODE_OT_translate_attach={TRANSFORM_OT_translate=[('view2d_edge_pan', True)]} |
| Alt+D | Duplicate Linked | `node.duplicate_move_linked` | NODE_OT_translate_attach={TRANSFORM_OT_translate=[('view2d_edge_pan', True)]} |
| Ctrl+Shift+D | Duplicate | `node.duplicate_move_keep_inputs` | NODE_OT_translate_attach={TRANSFORM_OT_translate=[('view2d_edge_pan', True)]} |
| Ctrl+P | Make Parent | `node.parent_set` |  |
| Alt+P | Detach Nodes | `node.detach` |  |
| F | Join in Named Frame | `node.join_named` |  |
| H | Collapse | `node.hide_toggle` |  |
| M | Toggle Node Mute | `node.mute_toggle` |  |
| Shift+H | Toggle Node Preview | `node.preview_toggle` |  |
| Ctrl+H | Toggle Hidden Node Sockets | `node.hide_socket_toggle` |  |
| Home | Frame All | `node.view_all` |  |
| NDOF Fit | Frame All | `node.view_all` |  |
| Numpad . | Frame Selected | `node.view_selected` |  |
| Button4 Mouse | Frame Selected | `node.view_selected` |  |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='NODE_MT_view_pie' |
| X | Delete | `node.delete` |  |
| Delete | Delete | `node.delete` |  |
| Shift+X | Delete with Reconnect | `node.delete_reconnect` |  |
| Ctrl+Delete | Delete with Reconnect | `node.delete_reconnect` |  |
| A | (De)select All | `node.select_all` | action='SELECT' |
| Alt+A | (De)select All | `node.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `node.select_all` | action='INVERT' |
| A double click | (De)select All | `node.select_all` | action='DESELECT' |
| Shift+L | Select Linked To | `node.select_linked_to` |  |
| L | Select Linked From | `node.select_linked_from` |  |
| Shift+G | Select Grouped | `node.select_grouped` |  |
| Ctrl+Shift+G | Select Grouped | `node.select_grouped` | extend=True |
| Shift+] | Activate Same Type Next/Prev | `node.select_same_type_step` | prev=False |
| Shift+[ | Activate Same Type Next/Prev | `node.select_same_type_step` | prev=True |
| Ctrl+F | Find Node | `node.find_node` |  |
| Ctrl+G | Make Group | `node.group_make` |  |
| Ctrl+Alt+G | Ungroup | `node.group_ungroup` |  |
| P | Separate | `node.group_separate` |  |
| Left Mouse double click | Edit Comment | `node.comment_edit` |  |
| Return | Edit Comment | `node.comment_edit` |  |
| F2 | Edit Comment | `node.comment_edit` | use_active=True |
| Left Mouse double click | Enter/Exit Group | `node.group_enter_exit` |  |
| Tab | Edit Group | `node.group_edit` | exit=False |
| Ctrl+Tab | Edit Group | `node.group_edit` | exit=True |
| Ctrl+R | Read View Layers | `node.read_viewlayers` |  |
| Z | Render Changed Layer | `node.render_changed` |  |
| Ctrl+C | Copy to Clipboard | `node.clipboard_copy` |  |
| Ctrl+V | Paste from Clipboard | `node.clipboard_paste` |  |
| Ctrl+X | Delete with Copy and Reconnect | `node.delete_copy_reconnect` |  |
| G | Move and Attach | `node.translate_attach` | TRANSFORM_OT_translate={view2d_edge_pan=True} |
| Left Mouse drag | Move and Attach | `node.translate_attach` | TRANSFORM_OT_translate={view2d_edge_pan=True} |
| G | Move | `transform.translate` | view2d_edge_pan=True |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, view2d_edge_pan=True |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Alt+Right Mouse drag | Detach | `node.move_detach_links_release` | NODE_OT_translate_attach={TRANSFORM_OT_translate=[('view2d_edge_pan', True)]} |
| Alt+Left Mouse drag | Detach | `node.move_detach_links` | TRANSFORM_OT_translate={view2d_edge_pan=True} |
| Shift+Tab | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_snap_node' |
| Shift+Alt+Z | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.show_overlays' |
| Right Mouse | Call Menu | `wm.call_menu` | name='NODE_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='NODE_MT_context_menu' |
| 1 | Fast Preview | `node.viewer_shortcut_get` | viewer_index=1 |
| 2 | Fast Preview | `node.viewer_shortcut_get` | viewer_index=2 |
| 3 | Fast Preview | `node.viewer_shortcut_get` | viewer_index=3 |
| 4 | Fast Preview | `node.viewer_shortcut_get` | viewer_index=4 |
| 5 | Fast Preview | `node.viewer_shortcut_get` | viewer_index=5 |
| 6 | Fast Preview | `node.viewer_shortcut_get` | viewer_index=6 |
| 7 | Fast Preview | `node.viewer_shortcut_get` | viewer_index=7 |
| 8 | Fast Preview | `node.viewer_shortcut_get` | viewer_index=8 |
| 9 | Fast Preview | `node.viewer_shortcut_get` | viewer_index=9 |
| Ctrl+1 | Fast Preview | `node.viewer_shortcut_set` | viewer_index=1 |
| Ctrl+2 | Fast Preview | `node.viewer_shortcut_set` | viewer_index=2 |
| Ctrl+3 | Fast Preview | `node.viewer_shortcut_set` | viewer_index=3 |
| Ctrl+4 | Fast Preview | `node.viewer_shortcut_set` | viewer_index=4 |
| Ctrl+5 | Fast Preview | `node.viewer_shortcut_set` | viewer_index=5 |
| Ctrl+6 | Fast Preview | `node.viewer_shortcut_set` | viewer_index=6 |
| Ctrl+7 | Fast Preview | `node.viewer_shortcut_set` | viewer_index=7 |
| Ctrl+8 | Fast Preview | `node.viewer_shortcut_set` | viewer_index=8 |
| Ctrl+9 | Fast Preview | `node.viewer_shortcut_set` | viewer_index=9 |

## Spreadsheet Generic

Space `SPREADSHEET`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_channels' |
| Left Mouse | Resize Column | `spreadsheet.resize_column` |  |
| Left Mouse double click | Fit Column | `spreadsheet.fit_column` |  |
| Left Mouse drag | Reorder Columns | `spreadsheet.reorder_columns` |  |

## Info

Space `INFO`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse click | Select Report | `info.select_pick` |  |
| Shift+Left Mouse click | Select Report | `info.select_pick` | extend=True |
| Left Mouse drag | Box Select | `info.select_box` | wait_for_input=False |
| A | (De)select All | `info.select_all` | action='SELECT' |
| Alt+A | (De)select All | `info.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `info.select_all` | action='INVERT' |
| A double click | (De)select All | `info.select_all` | action='DESELECT' |
| B | Box Select | `info.select_box` |  |
| R | Replay Operators | `info.report_replay` |  |
| X | Delete Reports | `info.report_delete` |  |
| Delete | Delete Reports | `info.report_delete` |  |
| Ctrl+C | Copy Reports to Clipboard | `info.report_copy` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='INFO_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='INFO_MT_context_menu' |

## File Browser

Space `FILE_BROWSER`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_tool_props' |
| Alt+Up Arrow | Parent Directory | `file.parent` |  |
| Ctrl+Up Arrow | Parent Directory | `file.parent` |  |
| Alt+Left Arrow | Previous Folder | `file.previous` |  |
| Button4 Mouse | Previous Folder | `file.previous` |  |
| Ctrl+[ | Previous Folder | `file.previous` |  |
| Alt+Right Arrow | Next Folder | `file.next` |  |
| Button5 Mouse | Next Folder | `file.next` |  |
| Ctrl+] | Next Folder | `file.next` |  |
| Ctrl+1 | Context Set Enum | `wm.context_set_enum` | data_path='space_data.params.display_type', value='LIST_VERTICAL' |
| Ctrl+2 | Context Set Enum | `wm.context_set_enum` | data_path='space_data.params.display_type', value='LIST_HORIZONTAL' |
| Ctrl+3 | Context Set Enum | `wm.context_set_enum` | data_path='space_data.params.display_type', value='THUMBNAIL' |
| R | Refresh File List | `file.refresh` |  |
| Ctrl+R | Refresh File List | `file.refresh` |  |
| R | Refresh Asset Library | `asset.library_refresh` |  |
| Shift+R | Reload Remote Asset Library Listing | `asset.library_reload_listing` |  |
| P | Parent Directory | `file.parent` |  |
| Backspace | Previous Folder | `file.previous` |  |
| Shift+Backspace | Next Folder | `file.next` |  |
| H | Context Toggle | `wm.context_toggle` | data_path='space_data.params.show_hidden' |
| Ctrl+H | Context Toggle | `wm.context_toggle` | data_path='space_data.params.show_hidden' |
| Ctrl+Shift+. | Context Toggle | `wm.context_toggle` | data_path='space_data.params.show_hidden' |
| Ctrl+Shift+N | Create New Directory | `file.directory_new` | confirm=False |
| F2 | Rename File or Directory | `file.rename` |  |
| X | Delete Selected Files | `file.delete` |  |
| Delete | Delete Selected Files | `file.delete` |  |
| Any modifier+Timer 1 any | Smooth Scroll | `file.smoothscroll` |  |
| Ctrl+B | Add Bookmark | `file.bookmark_add` |  |
| Ctrl+F | Filter | `file.start_filter` |  |
| Ctrl+L | Edit Directory Path | `file.edit_directory_path` |  |
| Numpad + (repeat) | Increment Number in Filename | `file.filenum` | increment=1 |
| Shift+Numpad + (repeat) | Increment Number in Filename | `file.filenum` | increment=10 |
| Ctrl+Numpad + (repeat) | Increment Number in Filename | `file.filenum` | increment=100 |
| Numpad - (repeat) | Increment Number in Filename | `file.filenum` | increment=-1 |
| Shift+Numpad - (repeat) | Increment Number in Filename | `file.filenum` | increment=-10 |
| Ctrl+Numpad - (repeat) | Increment Number in Filename | `file.filenum` | increment=-100 |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='FILEBROWSER_MT_view_pie' |
| Right Mouse | Select | `file.select` | open=False, only_activate_if_selected=True, pass_through=True |
| Right Mouse | Call Menu | `wm.call_menu` | name='FILEBROWSER_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='FILEBROWSER_MT_context_menu' |

## File Browser Main

Space `FILE_BROWSER`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse double click | Select | `file.select` | open=True, deselect_all=True |
| Left Mouse double click | Execute File | `file.mouse_execute` |  |
| Left Mouse | Select | `file.select` | open=False, deselect_all=True |
| Ctrl+Left Mouse click | Select | `file.select` | extend=True, open=False |
| Shift+Left Mouse click | Select | `file.select` | extend=True, fill=True, open=False |
| Up Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='UP' |
| Shift+Up Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='UP', extend=True |
| Ctrl+Shift+Up Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='UP', extend=True, fill=True |
| Down Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='DOWN' |
| Shift+Down Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='DOWN', extend=True |
| Ctrl+Shift+Down Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='DOWN', extend=True, fill=True |
| Left Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='LEFT' |
| Shift+Left Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='LEFT', extend=True |
| Ctrl+Shift+Left Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='LEFT', extend=True, fill=True |
| Right Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='RIGHT' |
| Shift+Right Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='RIGHT', extend=True |
| Ctrl+Shift+Right Arrow (repeat) | Walk Select/Deselect File | `file.select_walk` | direction='RIGHT', extend=True, fill=True |
| Button4 Mouse click | Previous Folder | `file.previous` |  |
| Button5 Mouse click | Next Folder | `file.next` |  |
| A | (De)select All Files | `file.select_all` | action='SELECT' |
| Alt+A | (De)select All Files | `file.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All Files | `file.select_all` | action='INVERT' |
| A double click | (De)select All Files | `file.select_all` | action='DESELECT' |
| Ctrl+A | (De)select All Files | `file.select_all` |  |
| B | Box Select | `file.select_box` |  |
| Left Mouse drag | Box Select | `file.select_box` |  |
| Shift+Left Mouse drag | Box Select | `file.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `file.select_box` | mode='SUB' |
| Any modifier+Mouse Move any | Highlight File | `file.highlight` |  |
| Any modifier+Left Mouse | Sort from Column | `file.sort_column_ui_context` |  |
| Numpad . | Frame Selected | `file.view_selected` |  |
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
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Ctrl+Tab | Context Set Enum | `wm.context_set_enum` | data_path='area.type', value='GRAPH_EDITOR' |
| Shift+E | Set F-Curve Extrapolation | `action.extrapolation_type` |  |

## Dopesheet

Space `DOPESHEET_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select Keyframes | `action.clickselect` | deselect_all=True |
| Alt+Left Mouse | Select Keyframes | `action.clickselect` | column=True |
| Shift+Left Mouse | Select Keyframes | `action.clickselect` | extend=True |
| Shift+Alt+Left Mouse | Select Keyframes | `action.clickselect` | extend=True, column=True |
| Ctrl+Alt+Left Mouse | Select Keyframes | `action.clickselect` | channel=True |
| Ctrl+Shift+Alt+Left Mouse | Select Keyframes | `action.clickselect` | extend=True, channel=True |
| Ctrl+Left Mouse click | Select Left/Right | `action.select_leftright` | mode='CHECK' |
| Ctrl+Shift+Left Mouse click | Select Left/Right | `action.select_leftright` | mode='CHECK', extend=True |
| [ | Select Left/Right | `action.select_leftright` | mode='LEFT' |
| ] | Select Left/Right | `action.select_leftright` | mode='RIGHT' |
| A | Select All | `action.select_all` | action='SELECT' |
| Alt+A | Select All | `action.select_all` | action='DESELECT' |
| Ctrl+I | Select All | `action.select_all` | action='INVERT' |
| A double click | Select All | `action.select_all` | action='DESELECT' |
| B | Box Select | `action.select_box` | axis_range=False |
| Alt+B | Box Select | `action.select_box` | axis_range=True |
| Left Mouse drag | Box Select | `action.select_box` | tweak=True, mode='SET' |
| Shift+Left Mouse drag | Box Select | `action.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `action.select_box` | tweak=True, mode='SUB' |
| Ctrl+Right Mouse drag | Lasso Select | `action.select_lasso` | mode='ADD' |
| Ctrl+Shift+Right Mouse drag | Lasso Select | `action.select_lasso` | mode='SUB' |
| C | Circle Select | `action.select_circle` |  |
| K | Select All | `action.select_column` | mode='KEYS' |
| Ctrl+K | Select All | `action.select_column` | mode='CFRA' |
| Shift+K | Select All | `action.select_column` | mode='MARKERS_COLUMN' |
| Alt+K | Select All | `action.select_column` | mode='MARKERS_BETWEEN' |
| Ctrl+Numpad + (repeat) | Select More | `action.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `action.select_less` |  |
| L | Select Linked | `action.select_linked` |  |
| Ctrl+G | Jump to Keyframes | `action.frame_jump` |  |
| Shift+S | Call Pie Menu | `wm.call_menu_pie` | name='DOPESHEET_MT_snap_pie' |
| Ctrl+M | Mirror Keys | `action.mirror` |  |
| V | Set Keyframe Handle Type | `action.handle_type` |  |
| T | Set Keyframe Interpolation | `action.interpolation_type` |  |
| Shift+E | Set F-Curve Extrapolation | `action.extrapolation_type` |  |
| Ctrl+E | Set Keyframe Easing Type | `action.easing_type` |  |
| R | Set Keyframe Type | `action.keyframe_type` |  |
| Shift+Alt+O | Bake Keyframes | `action.bake_keys` |  |
| Numpad * | Isolate Layers | `grease_pencil.layer_isolate` |  |
| X | Call Menu | `wm.call_menu` | name='DOPESHEET_MT_delete' |
| Delete | Delete Keyframes | `action.delete` | confirm=False |
| Shift+D | Duplicate | `action.duplicate_move` |  |
| I | Insert Keyframes | `action.keyframe_insert` |  |
| Ctrl+C | Copy Keyframes | `action.copy` |  |
| Ctrl+V | Paste Keyframes | `action.paste` |  |
| Ctrl+Shift+V | Paste Keyframes | `action.paste` | flipped=True |
| Ctrl+Alt+P | Set Preview Range to Selected | `action.previewrange_set` |  |
| Home | Frame All | `action.view_all` |  |
| NDOF Fit | Frame All | `action.view_all` |  |
| Numpad . | Frame Selected | `action.view_selected` |  |
| Button4 Mouse | Frame Selected | `action.view_selected` |  |
| Numpad 0 | Go to Current Frame | `action.view_frame` |  |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='DOPESHEET_MT_view_pie' |
| Tab | Toggle Channel Editability | `anim.channels_editable_toggle` |  |
| Ctrl+F | Filter Channels | `anim.channels_select_filter` |  |
| G | Transform | `transform.transform` | mode='TIME_TRANSLATE' |
| Left Mouse drag | Transform | `transform.transform` | mode='TIME_TRANSLATE' |
| E | Transform | `transform.transform` | mode='TIME_EXTEND' |
| S | Transform | `transform.transform` | mode='TIME_SCALE' |
| Shift+T | Transform | `transform.transform` | mode='TIME_SLIDE' |
| Shift+Tab | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_snap_anim' |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_action' |
| M | Add Time Marker | `marker.add` |  |
| Ctrl+B | Bind Camera to Markers | `marker.camera_bind` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='DOPESHEET_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='DOPESHEET_MT_context_menu' |
| Shift+Right Mouse | Change Frame | `anim.change_frame` |  |

## NLA Generic

Space `NLA_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Tab | Enter Tweak Mode | `nla.tweakmode_enter` | use_upper_stack_evaluation=True |
| Tab | Exit Tweak Mode | `nla.tweakmode_exit` |  |
| Shift+Tab | Enter Tweak Mode | `nla.tweakmode_enter` | isolate_action=True |
| Shift+Tab | Exit Tweak Mode | `nla.tweakmode_exit` | isolate_action=True |
| Ctrl+F | Filter Channels | `anim.channels_select_filter` |  |

## NLA Tracks

Space `NLA_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mouse Click on NLA Tracks | `nla.channels_click` |  |
| Shift+Left Mouse | Mouse Click on NLA Tracks | `nla.channels_click` | extend=True |
| Shift+A | Add Tracks | `nla.tracks_add` | above_selected=False |
| Ctrl+Shift+A | Add Tracks | `nla.tracks_add` | above_selected=True |
| X | Delete Tracks | `nla.tracks_delete` |  |
| Delete | Delete Tracks | `nla.tracks_delete` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='NLA_MT_channel_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='NLA_MT_channel_context_menu' |

## NLA Editor

Space `NLA_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `nla.click_select` | deselect_all=True |
| Shift+Left Mouse | Select | `nla.click_select` | extend=True |
| Ctrl+Left Mouse click | Select Left/Right | `nla.select_leftright` | mode='CHECK' |
| Ctrl+Shift+Left Mouse click | Select Left/Right | `nla.select_leftright` | mode='CHECK', extend=True |
| [ | Select Left/Right | `nla.select_leftright` | mode='LEFT' |
| ] | Select Left/Right | `nla.select_leftright` | mode='RIGHT' |
| A | (De)select All | `nla.select_all` | action='SELECT' |
| Alt+A | (De)select All | `nla.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `nla.select_all` | action='INVERT' |
| A double click | (De)select All | `nla.select_all` | action='DESELECT' |
| B | Box Select | `nla.select_box` | axis_range=False |
| Alt+B | Box Select | `nla.select_box` | axis_range=True |
| Left Mouse drag | Box Select | `nla.select_box` | tweak=True, mode='SET' |
| Shift+Left Mouse drag | Box Select | `nla.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `nla.select_box` | tweak=True, mode='SUB' |
| Ctrl+Alt+P | Set Preview Range to Selected | `nla.previewrange_set` |  |
| Home | Frame All | `nla.view_all` |  |
| NDOF Fit | Frame All | `nla.view_all` |  |
| Numpad . | Frame Selected | `nla.view_selected` |  |
| Button4 Mouse | Frame Selected | `nla.view_selected` |  |
| Numpad 0 | Go to Current Frame | `nla.view_frame` |  |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='NLA_MT_view_pie' |
| Shift+A | Add Action Strip | `nla.actionclip_add` |  |
| Shift+T | Add Transition | `nla.transition_add` |  |
| Shift+K | Add Sound Clip | `nla.soundclip_add` |  |
| Ctrl+G | Add Meta-Strips | `nla.meta_add` |  |
| Ctrl+Alt+G | Remove Meta-Strips | `nla.meta_remove` |  |
| Shift+D | Duplicate Linked | `nla.duplicate_linked_move` |  |
| Alt+D | Duplicate | `nla.duplicate_move` |  |
| U | Make Single User | `nla.make_single_user` |  |
| X | Delete Strips | `nla.delete` |  |
| Delete | Delete Strips | `nla.delete` |  |
| Y | Split Strips | `nla.split` |  |
| H | Toggle Muting | `nla.mute_toggle` |  |
| Alt+F | Swap Strips | `nla.swap` |  |
| Page Up (repeat) | Move Strips Up | `nla.move_up` |  |
| Page Down (repeat) | Move Strips Down | `nla.move_down` |  |
| Ctrl+A | Apply Scale | `nla.apply_scale` |  |
| Alt+S | Clear Scale | `nla.clear_scale` |  |
| Shift+S | Call Pie Menu | `wm.call_menu_pie` | name='NLA_MT_snap_pie' |
| Ctrl+Shift+M | Add F-Modifier | `nla.fmodifier_add` |  |
| G | Transform | `transform.transform` | mode='TRANSLATION' |
| Left Mouse drag | Transform | `transform.transform` | mode='TRANSLATION' |
| E | Transform | `transform.transform` | mode='TIME_EXTEND' |
| S | Transform | `transform.transform` | mode='TIME_SCALE' |
| M | Add Time Marker | `marker.add` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='NLA_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='NLA_MT_context_menu' |
| Shift+Right Mouse | Change Frame | `anim.change_frame` | seq_solo_preview=True |

## Text Generic

Space `TEXT_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Ctrl+F | Find | `text.start_find` |  |
| Ctrl+J | Jump | `text.jump` |  |
| Ctrl+G | Find & Set Selection | `text.find_set_selected` |  |
| Ctrl+H | Replace | `text.replace` |  |

## Text

Space `TEXT_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+Wheel Up | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=False |
| Ctrl+Wheel Down | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=True |
| Ctrl+Numpad + (repeat) | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=False |
| Ctrl+Numpad - (repeat) | Context Int Cycle | `wm.context_cycle_int` | data_path='space_data.font_size', reverse=True |
| Alt+N | New Text | `text.new` |  |
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
| Ctrl+/ | Toggle Comments | `text.comment_toggle` |  |
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
| Ctrl+Backspace (repeat) | Delete | `text.delete` | type='PREVIOUS_WORD' |
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
| Any modifier+Text Input any (repeat) | Line Number | `text.line_number` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='TEXT_MT_context_menu' |
| Any modifier+Text Input any (repeat) | Insert | `text.insert` |  |

## Video Sequence Editor

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Shift+O | Context Toggle | `wm.context_toggle` | data_path='sequencer_scene.sequence_editor.show_overlay_frame' |
| Ctrl+Tab | Context Toggle Values | `wm.context_toggle_enum` | data_path='space_data.view_type', value_1='SEQUENCER', value_2='PREVIEW' |
| Shift+Tab | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_snap_sequencer' |
| Ctrl+E | Refresh Sequencer | `sequencer.refresh_all` |  |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_box', cycle=True |

## Sequencer

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse click | Select | `sequencer.select` | deselect_all=True |
| Shift+Left Mouse click | Select | `sequencer.select` | toggle=True |
| Ctrl+Left Mouse | Select | `sequencer.select` | linked_time=True |
| Ctrl+Shift+Left Mouse | Select | `sequencer.select` | linked_time=True, extend=True |
| Ctrl+Left Mouse click | Select | `sequencer.select` | side_of_frame=True |
| Alt+Left Mouse click | Select | `sequencer.select` | deselect_all=True, ignore_connections=True |
| Shift+Alt+Left Mouse click | Select | `sequencer.select` | toggle=True, ignore_connections=True |
| Ctrl+Numpad + (repeat) | Select More | `sequencer.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `sequencer.select_less` |  |
| L | Select Pick Linked | `sequencer.select_linked_pick` |  |
| Shift+L | Select Pick Linked | `sequencer.select_linked_pick` | extend=True |
| Ctrl+L | Select Linked | `sequencer.select_linked` |  |
| Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='SET' |
| Shift+Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='SUB' |
| Alt+Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, ignore_connections=True, mode='SET' |
| B | Box Select | `sequencer.select_box` |  |
| Ctrl+B | Box Select | `sequencer.select_box` | include_handles=True |
| Shift+G | Select Grouped | `sequencer.select_grouped` |  |
| A | (De)select All | `sequencer.select_all` | action='SELECT' |
| Alt+A | (De)select All | `sequencer.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `sequencer.select_all` | action='INVERT' |
| A double click | (De)select All | `sequencer.select_all` | action='DESELECT' |
| [ | Select Side of Frame | `sequencer.select_side_of_frame` | side='LEFT' |
| ] | Select Side of Frame | `sequencer.select_side_of_frame` | side='RIGHT' |
| K | Split Strips | `sequencer.split` | type='SOFT', only_selected=True |
| Shift+K | Split Strips | `sequencer.split` | type='HARD', only_selected=True |
| H | Mute Strips | `sequencer.mute` | unselected=False |
| Shift+H | Mute Strips | `sequencer.mute` | unselected=True |
| Alt+H | Unmute Strips | `sequencer.unmute` | unselected=False |
| Shift+Alt+H | Unmute Strips | `sequencer.unmute` | unselected=True |
| Ctrl+H | Lock Strips | `sequencer.lock` |  |
| Ctrl+Alt+H | Unlock Strips | `sequencer.unlock` |  |
| Ctrl+Alt+C | Connect Strips | `sequencer.connect` | toggle=True |
| R | Reassign Inputs | `sequencer.reassign_inputs` |  |
| Alt+R | Reload Strips | `sequencer.reload` |  |
| Shift+Alt+R | Reload Strips | `sequencer.reload` | adjust_length=True |
| Alt+O | Clear Strip Offset | `sequencer.offset_clear` |  |
| Shift+D | Duplicate Strips | `sequencer.duplicate_move` |  |
| Alt+D | Duplicate Strips | `sequencer.duplicate_move_linked` |  |
| X | Delete Retiming Keys | `sequencer.retiming_key_delete` |  |
| Delete | Delete Retiming Keys | `sequencer.retiming_key_delete` |  |
| X | Delete Strips | `sequencer.delete` |  |
| Delete | Delete Strips | `sequencer.delete` |  |
| Shift+X | Ripple Delete Strips | `sequencer.ripple_delete` |  |
| Shift+Delete | Ripple Delete Strips | `sequencer.ripple_delete` |  |
| Shift+Q | Ripple Trim Strips | `sequencer.ripple_trim` | side='LEFT' |
| Shift+W | Ripple Trim Strips | `sequencer.ripple_trim` | side='RIGHT' |
| Ctrl+C | Copy | `sequencer.copy` |  |
| Ctrl+V | Paste | `sequencer.paste` |  |
| Ctrl+Shift+V | Paste | `sequencer.paste` | keep_offset=True |
| Y | Separate Images | `sequencer.images_separate` |  |
| Tab | Toggle Meta Strip | `sequencer.meta_toggle` |  |
| Ctrl+G | Make Meta Strip | `sequencer.meta_make` |  |
| Ctrl+Alt+G | UnMeta Strip | `sequencer.meta_separate` |  |
| Home | Frame All | `sequencer.view_all` |  |
| NDOF Fit | Frame All | `sequencer.view_all` |  |
| Numpad . | Frame Selected | `sequencer.view_selected` |  |
| Button4 Mouse | Frame Selected | `sequencer.view_selected` |  |
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
| Shift+S | Snap Strips to the Current Frame | `sequencer.snap` | keep_offset=True |
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
| Shift+A | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_add' |
| Ctrl+Shift+C | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_change' |
| C | Set Tool by Name (Hold) | `wm.tool_set_by_id_hold` | name='builtin.blade' |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='SEQUENCER_MT_view_pie' |
| S | Slip Strips | `sequencer.slip` | use_cursor_position=False |
| O | Context Set | `wm.context_set_int` | data_path='sequencer_scene.sequence_editor.overlay_frame', value=0 |
| G | Sequence Slide | `transform.seq_slide` | view2d_edge_pan=True |
| Left Mouse drag | Sequence Slide | `transform.seq_slide` | view2d_edge_pan=True, use_restore_handle_selection=True |
| Alt+Left Mouse drag | Sequence Slide | `transform.seq_slide` | view2d_edge_pan=True, use_restore_handle_selection=True |
| Ctrl+Left Mouse drag | Sequence Slide | `transform.seq_slide` | view2d_edge_pan=True, use_restore_handle_selection=True |
| E | Transform | `transform.transform` | mode='TIME_EXTEND' |
| M | Add Time Marker | `marker.add` |  |
| Shift+Alt+Z | Context Toggle | `wm.context_toggle` | data_path='space_data.show_overlays' |
| Right Mouse | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_context_menu' |
| I | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_retiming' |
| R | Set Speed | `sequencer.retiming_segment_speed_set` |  |
| Ctrl+R | Retime Strips | `sequencer.retiming_show` |  |

## Preview

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='PREVIOUS_CHARACTER' |
| Shift+Left Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='PREVIOUS_CHARACTER', select_text=True |
| Right Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='NEXT_CHARACTER' |
| Shift+Right Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='NEXT_CHARACTER', select_text=True |
| Up Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='PREVIOUS_LINE' |
| Shift+Up Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='PREVIOUS_LINE', select_text=True |
| Down Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='NEXT_LINE' |
| Shift+Down Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='NEXT_LINE', select_text=True |
| Home (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='LINE_BEGIN' |
| Shift+Home (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='LINE_BEGIN', select_text=True |
| End (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='LINE_END' |
| Shift+End (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='LINE_END', select_text=True |
| Ctrl+Left Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='PREVIOUS_WORD' |
| Ctrl+Shift+Left Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='PREVIOUS_WORD', select_text=True |
| Ctrl+Right Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='NEXT_WORD' |
| Ctrl+Shift+Right Arrow (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='NEXT_WORD', select_text=True |
| Page Up (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='TEXT_BEGIN' |
| Shift+Page Up (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='TEXT_BEGIN', select_text=True |
| Page Down (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='TEXT_END' |
| Shift+Page Down (repeat) | Move Cursor | `sequencer.text_cursor_move` | type='TEXT_END', select_text=True |
| Delete (repeat) | Delete Text | `sequencer.text_delete` | type='NEXT_OR_SELECTION' |
| Backspace (repeat) | Delete Text | `sequencer.text_delete` | type='PREVIOUS_OR_SELECTION' |
| Return (repeat) | Insert Line Break | `sequencer.text_line_break` |  |
| Numpad Enter (repeat) | Insert Line Break | `sequencer.text_line_break` |  |
| Ctrl+A | Select All | `sequencer.text_select_all` |  |
| Esc | Deselect All | `sequencer.text_deselect_all` |  |
| Tab | Edit Text | `sequencer.text_edit_mode_toggle` |  |
| Ctrl+C | Copy Text | `sequencer.text_edit_copy` |  |
| Ctrl+V | Paste Text | `sequencer.text_edit_paste` |  |
| Ctrl+X | Cut Text | `sequencer.text_edit_cut` |  |
| Any modifier+Text Input any (repeat) | Insert Text | `sequencer.text_insert` |  |
| Left Mouse click | Select | `sequencer.select` | deselect_all=True |
| Shift+Left Mouse click | Select | `sequencer.select` | toggle=True |
| Ctrl+Left Mouse click | Select | `sequencer.select` | center=True |
| Alt+Left Mouse click | Select | `sequencer.select` | ignore_connections=True |
| Ctrl+Shift+Left Mouse click | Select | `sequencer.select` | toggle=True, center=True |
| Shift+Alt+Left Mouse click | Select | `sequencer.select` | toggle=True, ignore_connections=True |
| A | (De)select All | `sequencer.select_all` | action='SELECT' |
| Alt+A | (De)select All | `sequencer.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `sequencer.select_all` | action='INVERT' |
| A double click | (De)select All | `sequencer.select_all` | action='DESELECT' |
| B | Box Select | `sequencer.select_box` |  |
| C | Circle Select | `sequencer.select_circle` |  |
| Shift+G | Select Grouped | `sequencer.select_grouped` |  |
| Numpad . | Frame Selected | `sequencer.view_selected` |  |
| Button4 Mouse | Frame Selected | `sequencer.view_selected` |  |
| Home | Frame All | `sequencer.view_all_preview` |  |
| NDOF Fit | Frame All | `sequencer.view_all_preview` |  |
| O | Border Offset View | `sequencer.view_ghost_border` |  |
| Numpad 1 | Sequencer View Zoom Ratio | `sequencer.view_zoom_ratio` | ratio=1.0 |
| Numpad 2 | Sequencer View Zoom Ratio | `sequencer.view_zoom_ratio` | ratio=0.5 |
| Numpad 4 | Sequencer View Zoom Ratio | `sequencer.view_zoom_ratio` | ratio=0.25 |
| Numpad 8 | Sequencer View Zoom Ratio | `sequencer.view_zoom_ratio` | ratio=0.125 |
| Ctrl+Numpad 2 | Sequencer View Zoom Ratio | `sequencer.view_zoom_ratio` | ratio=2.0 |
| Ctrl+Numpad 4 | Sequencer View Zoom Ratio | `sequencer.view_zoom_ratio` | ratio=4.0 |
| Ctrl+Numpad 8 | Sequencer View Zoom Ratio | `sequencer.view_zoom_ratio` | ratio=8.0 |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='SEQUENCER_MT_preview_view_pie' |
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Ctrl+. | Move | `transform.translate` | translate_origin=True |
| Alt+G | Clear Strip Transform | `sequencer.strip_transform_clear` | property='POSITION' |
| Alt+S | Clear Strip Transform | `sequencer.strip_transform_clear` | property='SCALE' |
| Alt+R | Clear Strip Transform | `sequencer.strip_transform_clear` | property='ROTATION' |
| Shift+D | Duplicate Strips | `sequencer.preview_duplicate_move` |  |
| Alt+D | Duplicate Strips | `sequencer.preview_duplicate_move_linked` |  |
| H | Mute Strips | `sequencer.mute` | unselected=False |
| Shift+H | Mute Strips | `sequencer.mute` | unselected=True |
| Alt+H | Unmute Strips | `sequencer.unmute` | unselected=False |
| X | Delete Strips | `sequencer.delete` |  |
| Delete | Delete Strips | `sequencer.delete` |  |
| Ctrl+Right Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='ADD' |
| Ctrl+Shift+Right Mouse drag | Lasso Select | `sequencer.select_lasso` | mode='SUB' |
| Ctrl+C | Copy | `sequencer.copy` |  |
| Ctrl+V | Paste | `sequencer.paste` |  |
| Ctrl+Shift+V | Paste | `sequencer.paste` | keep_offset=True |
| Shift+K | Set Active Keying Set | `anim.keying_set_active_set` |  |
| K | Insert Keyframe Menu | `anim.keyframe_insert_menu` | always_prompt=True |
| Alt+I | Delete Keyframe | `anim.keyframe_delete_vse` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_preview_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='SEQUENCER_MT_preview_context_menu' |
| I | Insert Keyframe | `anim.keyframe_insert` |  |
| Ctrl+` | Context Toggle | `wm.context_toggle` | data_path='space_data.show_gizmo' |
| . | Call Pie Menu | `wm.call_menu_pie` | name='SEQUENCER_MT_pivot_pie' |
| Shift+Alt+Z | Context Toggle | `wm.context_toggle` | data_path='space_data.show_overlays' |
| Shift+Right Mouse | Set 2D Cursor | `sequencer.cursor_set` |  |
| Shift+Right Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

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
| T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_toolbar' |
| N | Context Toggle | `wm.context_toggle` | data_path='space_data.show_region_ui' |
| Alt+O | Open Clip | `clip.open` |  |
| Alt+Left Arrow (repeat) | Track Markers | `clip.track_markers` | backwards=True, sequence=False |
| Alt+Right Arrow (repeat) | Track Markers | `clip.track_markers` | backwards=False, sequence=False |
| Ctrl+T | Track Markers | `clip.track_markers` | backwards=False, sequence=True |
| Ctrl+Shift+T | Track Markers | `clip.track_markers` | backwards=True, sequence=True |
| Tab | Context Toggle Values | `wm.context_toggle_enum` | data_path='space_data.mode', value_1='TRACKING', value_2='MASK' |
| P | Prefetch Frames | `clip.prefetch` |  |
| E | Call Pie Menu | `wm.call_menu_pie` | name='CLIP_MT_tracking_pie' |
| Shift+S | Call Pie Menu | `wm.call_menu_pie` | name='CLIP_MT_solving_pie' |
| Shift+E | Call Pie Menu | `wm.call_menu_pie` | name='CLIP_MT_marker_pie' |
| Shift+W | Call Pie Menu | `wm.call_menu_pie` | name='CLIP_MT_reconstruction_pie' |
| ` | Call Pie Menu | `wm.call_menu_pie` | name='CLIP_MT_view_pie' |

## Clip Editor

Space `CLIP_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Middle Mouse | Pan View | `clip.view_pan` |  |
| Shift+Middle Mouse | Pan View | `clip.view_pan` |  |
| Mouse/Trackpad Pan any | Pan View | `clip.view_pan` |  |
| Ctrl+Middle Mouse | View Zoom | `clip.view_zoom` |  |
| Mouse/Trackpad Zoom any | View Zoom | `clip.view_zoom` |  |
| Ctrl+Mouse/Trackpad Pan any | View Zoom | `clip.view_zoom` |  |
| Wheel In | Zoom In | `clip.view_zoom_in` |  |
| Wheel Out | Zoom Out | `clip.view_zoom_out` |  |
| Numpad + (repeat) | Zoom In | `clip.view_zoom_in` |  |
| Numpad - (repeat) | Zoom Out | `clip.view_zoom_out` |  |
| Numpad 1 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=1.0 |
| Numpad 2 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=0.5 |
| Numpad 4 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=0.25 |
| Numpad 8 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=0.125 |
| Ctrl+Numpad 2 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=2.0 |
| Ctrl+Numpad 4 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=4.0 |
| Ctrl+Numpad 8 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=8.0 |
| Shift+Numpad 2 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=2.0 |
| Shift+Numpad 4 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=4.0 |
| Shift+Numpad 8 | View Zoom Ratio | `clip.view_zoom_ratio` | ratio=8.0 |
| Home | Frame All | `clip.view_all` |  |
| F | Frame All | `clip.view_all` | fit_view=True |
| Numpad . | Frame Selected | `clip.view_selected` |  |
| Button4 Mouse | Frame Selected | `clip.view_selected` |  |
| NDOF Fit | Frame All | `clip.view_all` |  |
| NDOF Motion any | NDOF Pan/Zoom | `clip.view_ndof` |  |
| Ctrl+Shift+Left Arrow (repeat) | Jump to Frame | `clip.frame_jump` | position='PATHSTART' |
| Ctrl+Shift+Right Arrow (repeat) | Jump to Frame | `clip.frame_jump` | position='PATHEND' |
| Shift+Alt+Left Arrow (repeat) | Jump to Frame | `clip.frame_jump` | position='FAILEDPREV' |
| Shift+Alt+Right Arrow (repeat) | Jump to Frame | `clip.frame_jump` | position='PATHSTART' |
| Left Mouse | Change Frame | `clip.change_frame` |  |
| Left Mouse | Select | `clip.select` | deselect_all=True |
| Shift+Left Mouse | Select | `clip.select` | extend=True |
| A | (De)select All | `clip.select_all` | action='SELECT' |
| Alt+A | (De)select All | `clip.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `clip.select_all` | action='INVERT' |
| A double click | (De)select All | `clip.select_all` | action='DESELECT' |
| B | Box Select | `clip.select_box` |  |
| C | Circle Select | `clip.select_circle` |  |
| Shift+G | Call Menu | `wm.call_menu` | name='CLIP_MT_select_grouped' |
| Ctrl+Alt+Right Mouse drag | Lasso Select | `clip.select_lasso` | mode='ADD' |
| Ctrl+Shift+Alt+Right Mouse drag | Lasso Select | `clip.select_lasso` | mode='SUB' |
| Ctrl+Left Mouse | Add Marker and Slide | `clip.add_marker_slide` |  |
| Shift+X | Delete Marker | `clip.delete_marker` |  |
| Shift+Delete | Delete Marker | `clip.delete_marker` |  |
| Left Mouse | Slide Marker | `clip.slide_marker` |  |
| Shift+D | Disable Markers | `clip.disable_markers` | action='TOGGLE' |
| X | Delete Track | `clip.delete_track` |  |
| Delete | Delete Track | `clip.delete_track` |  |
| Ctrl+L | Lock Tracks | `clip.lock_tracks` | action='LOCK' |
| Alt+L | Lock Tracks | `clip.lock_tracks` | action='UNLOCK' |
| Alt+H | Hide Tracks Clear | `clip.hide_tracks_clear` |  |
| H | Hide Tracks | `clip.hide_tracks` | unselected=False |
| Shift+H | Hide Tracks | `clip.hide_tracks` | unselected=True |
| Left Mouse drag | Slide Plane Marker | `clip.slide_plane_marker` |  |
| I | Insert Keyframe | `clip.keyframe_insert` |  |
| Alt+I | Delete Keyframe | `clip.keyframe_delete` |  |
| Ctrl+J | Join Tracks | `clip.join_tracks` |  |
| L | Toggle Lock Selection | `clip.lock_selection_toggle` |  |
| Alt+D | Context Toggle | `wm.context_toggle` | data_path='space_data.show_disabled' |
| Alt+S | Context Toggle | `wm.context_toggle` | data_path='space_data.show_marker_search' |
| Ctrl+H | Context Toggle | `wm.context_toggle` | data_path='space_data.use_mute_footage' |
| G | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| S | Resize | `transform.resize` |  |
| R | Rotate | `transform.rotate` |  |
| Alt+T | Clear Track Path | `clip.clear_track_path` | action='REMAINED', clear_active=False |
| Shift+T | Clear Track Path | `clip.clear_track_path` | action='UPTO', clear_active=False |
| Shift+Alt+T | Clear Track Path | `clip.clear_track_path` | action='ALL', clear_active=False |
| Shift+Right Mouse | Set 2D Cursor | `clip.cursor_set` |  |
| Ctrl+C | Copy Tracks | `clip.copy_tracks` |  |
| Ctrl+V | Paste Tracks | `clip.paste_tracks` |  |
| Shift+Alt+Z | Context Toggle | `wm.context_toggle` | data_path='space_data.overlay.show_overlays' |
| Right Mouse | Call Menu | `wm.call_menu` | name='CLIP_MT_tracking_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='CLIP_MT_tracking_context_menu' |
| . | Call Pie Menu | `wm.call_menu_pie` | name='CLIP_MT_pivot_pie' |

## Clip Graph Editor

Space `CLIP_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `clip.graph_select` |  |
| Shift+Left Mouse | Select | `clip.graph_select` | extend=True |
| A | (De)select All Markers | `clip.graph_select_all_markers` | action='SELECT' |
| Alt+A | (De)select All Markers | `clip.graph_select_all_markers` | action='DESELECT' |
| Ctrl+I | (De)select All Markers | `clip.graph_select_all_markers` | action='INVERT' |
| A double click | (De)select All Markers | `clip.graph_select_all_markers` | action='DESELECT' |
| B | Box Select | `clip.graph_select_box` |  |
| X | Delete Curve | `clip.graph_delete_curve` |  |
| Delete | Delete Curve | `clip.graph_delete_curve` |  |
| Shift+X | Delete Knot | `clip.graph_delete_knot` |  |
| Shift+Delete | Delete Knot | `clip.graph_delete_knot` |  |
| Home | Frame All | `clip.graph_view_all` |  |
| NDOF Fit | Frame All | `clip.graph_view_all` |  |
| Numpad 0 | Center Current Frame | `clip.graph_center_current_frame` |  |
| L | Context Toggle | `wm.context_toggle` | data_path='space_data.lock_time_cursor' |
| Alt+T | Clear Track Path | `clip.clear_track_path` | action='REMAINED', clear_active=True |
| Shift+T | Clear Track Path | `clip.clear_track_path` | action='UPTO', clear_active=True |
| Shift+Alt+T | Clear Track Path | `clip.clear_track_path` | action='ALL', clear_active=True |
| Shift+D | Disable Markers | `clip.graph_disable_markers` | action='TOGGLE' |
| G | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| S | Resize | `transform.resize` |  |
| R | Rotate | `transform.rotate` |  |
| Shift+Right Mouse | Change Frame | `clip.change_frame` |  |

## Clip Dopesheet Editor

Space `CLIP_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select Channel | `clip.dopesheet_select_channel` | extend=True |
| Home | Frame All | `clip.dopesheet_view_all` |  |
| NDOF Fit | Frame All | `clip.dopesheet_view_all` |  |
| X | Delete Track | `clip.delete_track` |  |

## Frames

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Arrow (repeat) | Frame Offset | `screen.frame_offset` | delta=-1 |
| Right Arrow (repeat) | Frame Offset | `screen.frame_offset` | delta=1 |
| Shift+Right Arrow (repeat) | Jump to Endpoint | `screen.frame_jump` | end=True |
| Shift+Left Arrow (repeat) | Jump to Endpoint | `screen.frame_jump` | end=False |
| Ctrl+Right Arrow (repeat) | Jump Time by Delta | `screen.time_jump` | backward=False |
| Ctrl+Left Arrow (repeat) | Jump Time by Delta | `screen.time_jump` | backward=True |
| Up Arrow (repeat) | Jump to Keyframe | `screen.keyframe_jump` | next=False |
| Down Arrow (repeat) | Jump to Keyframe | `screen.keyframe_jump` | next=True |
| Media Last | Jump to Keyframe | `screen.keyframe_jump` | next=True |
| Media First | Jump to Keyframe | `screen.keyframe_jump` | next=False |
| Alt+Wheel Down | Frame Offset | `screen.frame_offset` | delta=1 |
| Alt+Wheel Up | Frame Offset | `screen.frame_offset` | delta=-1 |
| Space Bar | Play Animation | `screen.animation_play` |  |
| Ctrl+Shift+Space Bar | Play Animation | `screen.animation_play` | reverse=True |
| Esc | Cancel Animation | `screen.animation_cancel` |  |
| Media Play/Pause | Play Animation | `screen.animation_play` |  |
| Media Stop | Cancel Animation | `screen.animation_cancel` |  |

## Animation

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+T | Context Toggle | `wm.context_toggle` | data_path='space_data.show_seconds' |
| P | Set Preview Range | `anim.previewrange_set` |  |
| Alt+P | Clear Preview Range | `anim.previewrange_clear` |  |
| Ctrl+Home | Set Start Frame | `anim.start_frame_set` |  |
| Ctrl+End | Set End Frame | `anim.end_frame_set` |  |

## Animation Channels

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mouse Click on Channels | `anim.channels_click` |  |
| Shift+Left Mouse click | Mouse Click on Channels | `anim.channels_click` | extend_range=True |
| Ctrl+Left Mouse click | Mouse Click on Channels | `anim.channels_click` | extend=True |
| Ctrl+Shift+Left Mouse | Mouse Click on Channels | `anim.channels_click` | children_only=True |
| Left Mouse double click | Rename Channel | `anim.channels_rename` |  |
| Left Mouse double click | Select Channel Keyframes | `anim.channel_select_keys` |  |
| Shift+Left Mouse double click | Select Channel Keyframes | `anim.channel_select_keys` | extend=True |
| Ctrl+F | Filter Channels | `anim.channels_select_filter` |  |
| A | Select All | `anim.channels_select_all` | action='SELECT' |
| Alt+A | Select All | `anim.channels_select_all` | action='DESELECT' |
| Ctrl+I | Select All | `anim.channels_select_all` | action='INVERT' |
| A double click | Select All | `anim.channels_select_all` | action='DESELECT' |
| B | Box Select | `anim.channels_select_box` |  |
| Left Mouse drag | Box Select | `anim.channels_select_box` | extend=False |
| Shift+Left Mouse drag | Box Select | `anim.channels_select_box` | extend=True |
| Ctrl+Left Mouse drag | Box Select | `anim.channels_select_box` | deselect=True |
| X | Delete Channels | `anim.channels_delete` |  |
| Delete | Delete Channels | `anim.channels_delete` |  |
| Shift+W | Toggle Channel Setting | `anim.channels_setting_toggle` |  |
| Ctrl+Shift+W | Enable Channel Setting | `anim.channels_setting_enable` |  |
| Alt+W | Disable Channel Setting | `anim.channels_setting_disable` |  |
| Tab | Toggle Channel Editability | `anim.channels_editable_toggle` |  |
| Numpad + | Expand Channels | `anim.channels_expand` |  |
| Numpad - | Collapse Channels | `anim.channels_collapse` |  |
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
| Alt+Middle Mouse | Frame Channel Under Cursor | `anim.channel_view_pick` |  |
| Numpad . | Frame Selected Channels | `anim.channels_view_selected` |  |
| Button4 Mouse | Frame Selected Channels | `anim.channels_view_selected` |  |

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
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_gpencil_paint' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_draw_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_draw_context_menu' |
| Delete | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_greasepencil_delete' |
| Ctrl+C | Copy Strokes | `grease_pencil.copy` |  |
| Ctrl+V | Paste Strokes | `grease_pencil.paste` |  |
| Ctrl+Shift+V | Paste Strokes | `grease_pencil.paste` | paste_back=True |
| Shift+D | Duplicate Strokes | `grease_pencil.duplicate_move` |  |
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Shift+W | Bend | `transform.bend` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Shift+Alt+S | To Sphere | `transform.tosphere` |  |
| Ctrl+Shift+Alt+S | Shear | `transform.shear` |  |
| W | Set Tool by Name | `wm.tool_set_by_id` | name='builtin.select_lasso', cycle=True |

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
| Left Mouse drag | Move | `transform.translate` |  |
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
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_greasepencil_edit_context_menu' |
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
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_gpencil_sculpt' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_sculpt_context_menu' |
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
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_weight_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_weight_context_menu' |
| Alt+H | Show All Layers | `grease_pencil.layer_reveal` |  |
| H | Hide Layer(s) | `grease_pencil.layer_hide` | unselected=False |
| Shift+H | Hide Layer(s) | `grease_pencil.layer_hide` | unselected=True |
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_gpencil_weight' |
| Alt+Left Mouse | Select | `view3d.select` |  |
| Shift+Alt+Left Mouse | Select | `view3d.select` | toggle=True |
| Ctrl+Shift+Left Mouse | Select | `view3d.select` |  |

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
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_vertex_paint_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_greasepencil_vertex_paint_context_menu' |
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_gpencil_vertex' |

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

## Object Mode

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit_objects' |
| A | (De)select All | `object.select_all` | action='SELECT' |
| Alt+A | (De)select All | `object.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `object.select_all` | action='INVERT' |
| A double click | (De)select All | `object.select_all` | action='DESELECT' |
| Ctrl+Numpad + (repeat) | Select More | `object.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `object.select_less` |  |
| Shift+L | Select Linked | `object.select_linked` |  |
| Shift+G | Select Grouped | `object.select_grouped` |  |
| [ (repeat) | Select Hierarchy | `object.select_hierarchy` | direction='PARENT', extend=False |
| Shift+[ (repeat) | Select Hierarchy | `object.select_hierarchy` | direction='PARENT', extend=True |
| ] (repeat) | Select Hierarchy | `object.select_hierarchy` | direction='CHILD', extend=False |
| Shift+] (repeat) | Select Hierarchy | `object.select_hierarchy` | direction='CHILD', extend=True |
| Ctrl+P | Make Parent | `object.parent_set` |  |
| Alt+P | Clear Parent | `object.parent_clear` |  |
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Shift+T | Look at Surface | `object.transform_axis_target` |  |
| Alt+G | Clear Location | `object.location_clear` | clear_delta=False |
| Alt+R | Clear Rotation | `object.rotation_clear` | clear_delta=False |
| Alt+S | Clear Scale | `object.scale_clear` | clear_delta=False |
| X | Delete | `object.delete` | use_global=False |
| Shift+X | Delete | `object.delete` | use_global=True |
| Delete | Delete | `object.delete` | use_global=False, confirm=False |
| Shift+Delete | Delete | `object.delete` | use_global=True, confirm=False |
| Shift+A | Call Menu | `wm.call_menu` | name='VIEW3D_MT_add' |
| Ctrl+A | Call Menu | `wm.call_menu` | name='VIEW3D_MT_object_apply' |
| Ctrl+L | Call Menu | `wm.call_menu` | name='VIEW3D_MT_make_links' |
| Shift+D | Duplicate Objects | `object.duplicate_move` |  |
| Alt+D | Duplicate Linked | `object.duplicate_move_linked` |  |
| Ctrl+J | Join | `object.join` |  |
| Ctrl+. | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_transform_data_origin' |
| K | Insert Keyframe Menu | `anim.keyframe_insert_menu` | always_prompt=True |
| Alt+I | Delete Keyframe | `anim.keyframe_delete_v3d` |  |
| Shift+K | Set Active Keying Set | `anim.keying_set_active_set` |  |
| Ctrl+G | Create New Collection | `collection.create` |  |
| Ctrl+Alt+G | Remove from Collection | `collection.objects_remove` |  |
| Ctrl+Shift+Alt+G | Remove from All Collections | `collection.objects_remove_all` |  |
| Ctrl+Shift+G | Add Selected to Active Object's Collection | `collection.objects_add_active` |  |
| Shift+Alt+G | Remove Selected from Active Collection | `collection.objects_remove_active` |  |
| Ctrl+0 | Subdivision Set | `object.subdivision_set` | level=0, relative=False, ensure_modifier=True |
| Ctrl+1 | Subdivision Set | `object.subdivision_set` | level=1, relative=False, ensure_modifier=True |
| Ctrl+2 | Subdivision Set | `object.subdivision_set` | level=2, relative=False, ensure_modifier=True |
| Ctrl+3 | Subdivision Set | `object.subdivision_set` | level=3, relative=False, ensure_modifier=True |
| Ctrl+4 | Subdivision Set | `object.subdivision_set` | level=4, relative=False, ensure_modifier=True |
| Ctrl+5 | Subdivision Set | `object.subdivision_set` | level=5, relative=False, ensure_modifier=True |
| M | Call Menu | `wm.call_menu` | name='OBJECT_MT_move_to_collection' |
| Shift+M | Call Menu | `wm.call_menu` | name='OBJECT_MT_link_to_collection' |
| Alt+H | Show Hidden Objects | `object.hide_view_clear` |  |
| H | Hide Objects | `object.hide_view_set` | unselected=False |
| Shift+H | Hide Objects | `object.hide_view_set` | unselected=True |
| Ctrl+H | Hide Other Collections | `object.hide_collection` |  |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_object_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_object_context_menu' |
| I | Insert Keyframe | `anim.keyframe_insert` |  |

## Object Non-modal

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Alt+Q | Transfer Mode | `object.transfer_mode` |  |
| Tab | Set Object Mode | `object.mode_set` | mode='EDIT', toggle=True |
| Ctrl+Tab | Object Mode Menu | `view3d.object_mode_pie_or_toggle` |  |

## Pose

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Ctrl+P | Make Parent | `object.parent_set` |  |
| Alt+H | Reveal Selected | `pose.reveal` |  |
| H | Hide Selected | `pose.hide` | unselected=False |
| Shift+H | Hide Selected | `pose.hide` | unselected=True |
| Ctrl+A | Call Menu | `wm.call_menu` | name='VIEW3D_MT_pose_apply' |
| Alt+R | Clear Pose Rotation | `pose.rot_clear` |  |
| Alt+G | Clear Pose Location | `pose.loc_clear` |  |
| Alt+S | Clear Pose Scale | `pose.scale_clear` |  |
| Alt+F | Flip Quaternions | `pose.quaternions_flip` |  |
| Ctrl+R | Convert Rotation Mode | `anim.rotation_mode_convert` |  |
| Ctrl+C | Copy Pose | `pose.copy` |  |
| Ctrl+V | Paste Pose | `pose.paste` | flipped=False |
| Ctrl+Shift+V | Paste Pose | `pose.paste` | flipped=True |
| A | (De)select All | `pose.select_all` | action='SELECT' |
| Alt+A | (De)select All | `pose.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `pose.select_all` | action='INVERT' |
| A double click | (De)select All | `pose.select_all` | action='DESELECT' |
| Shift+P | Select Parent Bone | `pose.select_parent` |  |
| [ (repeat) | Select Hierarchy | `pose.select_hierarchy` | direction='PARENT', extend=False |
| Shift+[ (repeat) | Select Hierarchy | `pose.select_hierarchy` | direction='PARENT', extend=True |
| ] (repeat) | Select Hierarchy | `pose.select_hierarchy` | direction='CHILD', extend=False |
| Shift+] (repeat) | Select Hierarchy | `pose.select_hierarchy` | direction='CHILD', extend=True |
| Ctrl+L | Select Connected | `pose.select_linked` |  |
| L | Select Connected | `pose.select_linked_pick` |  |
| Shift+G | Select Grouped | `pose.select_grouped` |  |
| Ctrl+Shift+M | Select Mirror | `pose.select_mirror` |  |
| Ctrl+Shift+C | Add Constraint (with Targets) | `pose.constraint_add_with_targets` |  |
| Ctrl+Alt+C | Clear Pose Constraints | `pose.constraints_clear` |  |
| Shift+I | Add IK to Bone | `pose.ik_add` |  |
| Ctrl+Alt+I | Remove IK | `pose.ik_clear` |  |
| Shift+W | Call Menu | `wm.call_menu` | name='VIEW3D_MT_bone_options_toggle' |
| Ctrl+Shift+W | Call Menu | `wm.call_menu` | name='VIEW3D_MT_bone_options_enable' |
| Alt+W | Call Menu | `wm.call_menu` | name='VIEW3D_MT_bone_options_disable' |
| Shift+M | Assign to Collection | `armature.assign_to_collection` |  |
| M | Move to Collection | `armature.move_to_collection` |  |
| Ctrl+Shift+Alt+S | Scale B-Bone | `transform.bbone_resize` |  |
| K | Insert Keyframe Menu | `anim.keyframe_insert_menu` | always_prompt=True |
| Alt+I | Delete Keyframe | `anim.keyframe_delete_v3d` |  |
| Shift+K | Set Active Keying Set | `anim.keying_set_active_set` |  |
| Ctrl+E | Push Pose from Breakdown | `pose.push` |  |
| Alt+E | Relax Pose to Breakdown | `pose.relax` |  |
| Shift+E | Pose Breakdowner | `pose.breakdown` |  |
| Shift+Alt+E | Blend to Neighbor | `pose.blend_to_neighbor` |  |
| Alt+P | Call Menu | `wm.call_menu` | name='VIEW3D_MT_pose_propagate' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_pose_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_pose_context_menu' |
| Shift+Alt+W | Call Menu | `wm.call_menu` | name='POSE_MT_selection_sets_select' |
| I | Insert Keyframe | `anim.keyframe_insert` |  |

## Paint Curve

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Ctrl+Right Mouse | Add Curve Point and Slide | `paintcurve.add_point_slide` |  |
| Left Mouse | Select Paint Curve Point | `paintcurve.select` |  |
| Shift+Left Mouse | Select Paint Curve Point | `paintcurve.select` | extend=True |
| Right Mouse | Slide Paint Curve Point | `paintcurve.slide` | align=False |
| Shift+Right Mouse | Slide Paint Curve Point | `paintcurve.slide` | align=True |
| A | Select Paint Curve Point | `paintcurve.select` | toggle=True |
| Ctrl+Shift+Right Mouse | Place Cursor | `paintcurve.cursor` |  |
| X | Remove Paint Curve Point | `paintcurve.delete_point` |  |
| Delete | Remove Paint Curve Point | `paintcurve.delete_point` |  |
| Return | Draw Curve | `paintcurve.draw` |  |
| Numpad Enter | Draw Curve | `paintcurve.draw` |  |
| G | Move | `transform.translate` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |

## Image Paint

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Image Paint | `paint.image_paint` |  |
| Ctrl+Left Mouse | Image Paint | `paint.image_paint` | mode='INVERT' |
| Shift+Left Mouse | Image Paint | `paint.image_paint` | brush_toggle='SMOOTH' |
| X | Swap Colors | `paint.brush_colors_flip` |  |
| Right Mouse | Grab Clone | `paint.grab_clone` |  |
| Shift+X | Sample Color | `paint.sample_color` | merged=False |
| Ctrl+Shift+X | Sample Color | `paint.sample_color` | merged=True |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.image_paint.brush.size', data_path_secondary='tool_settings.image_paint.unified_paint_settings.size', use_secondary='tool_settings.image_paint.brush.use_unified_size', rotation_path='tool_settings.image_paint.brush.mask_texture_slot.angle', color_path='tool_settings.image_paint.brush.cursor_color_add', fill_color_path='tool_settings.image_paint.brush.color', fill_color_override_path='tool_settings.image_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.image_paint.brush.use_unified_color', zoom_path='space_data.zoom', image_id='tool_settings.image_paint.brush', secondary_tex=True |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.image_paint.brush.strength', data_path_secondary='tool_settings.image_paint.unified_paint_settings.strength', use_secondary='tool_settings.image_paint.brush.use_unified_strength', rotation_path='tool_settings.image_paint.brush.mask_texture_slot.angle', color_path='tool_settings.image_paint.brush.cursor_color_add', fill_color_path='tool_settings.image_paint.brush.color', fill_color_override_path='tool_settings.image_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.image_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.image_paint.brush', secondary_tex=True |
| Ctrl+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.image_paint.brush.texture_slot.angle', data_path_secondary='', use_secondary='', rotation_path='tool_settings.image_paint.brush.texture_slot.angle', color_path='tool_settings.image_paint.brush.cursor_color_add', fill_color_path='tool_settings.image_paint.brush.color', fill_color_override_path='tool_settings.image_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.image_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.image_paint.brush', secondary_tex=False |
| Ctrl+Alt+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.image_paint.brush.mask_texture_slot.angle', data_path_secondary='', use_secondary='', rotation_path='tool_settings.image_paint.brush.mask_texture_slot.angle', color_path='tool_settings.image_paint.brush.cursor_color_add', fill_color_path='tool_settings.image_paint.brush.color', fill_color_override_path='tool_settings.image_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.image_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.image_paint.brush', secondary_tex=True |
| Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION' |
| Shift+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE' |
| Ctrl+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION' |
| Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION', texmode='SECONDARY' |
| Shift+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE', texmode='SECONDARY' |
| Ctrl+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION', texmode='SECONDARY' |
| 1 | Context Toggle | `wm.context_toggle` | data_path='image_paint_object.data.use_paint_mask' |
| Shift+S | Context Toggle | `wm.context_toggle` | data_path='tool_settings.image_paint.brush.use_smooth_stroke' |
| Alt+E | Context Enum Menu | `wm.context_menu_enum` | data_path='tool_settings.image_paint.brush.stroke_method' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_texture_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_texture_context_menu' |
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_texture_paint' |
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='IMAGE_AST_brush_paint' |

## Vertex Paint

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Vertex Paint | `paint.vertex_paint` |  |
| Ctrl+Left Mouse | Vertex Paint | `paint.vertex_paint` | mode='INVERT' |
| Shift+Left Mouse | Vertex Paint | `paint.vertex_paint` | brush_toggle='SMOOTH' |
| X | Swap Colors | `paint.brush_colors_flip` |  |
| Shift+X | Sample Color | `paint.sample_color` | merged=False |
| Ctrl+Shift+X | Sample Color | `paint.sample_color` | merged=True |
| Ctrl+X | Set Vertex Colors | `paint.vertex_color_set` |  |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.vertex_paint.brush.size', data_path_secondary='tool_settings.vertex_paint.unified_paint_settings.size', use_secondary='tool_settings.vertex_paint.brush.use_unified_size', rotation_path='tool_settings.vertex_paint.brush.texture_slot.angle', color_path='tool_settings.vertex_paint.brush.cursor_color_add', fill_color_path='tool_settings.vertex_paint.brush.color', fill_color_override_path='tool_settings.vertex_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.vertex_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.vertex_paint.brush', secondary_tex=False |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.vertex_paint.brush.strength', data_path_secondary='tool_settings.vertex_paint.unified_paint_settings.strength', use_secondary='tool_settings.vertex_paint.brush.use_unified_strength', rotation_path='tool_settings.vertex_paint.brush.texture_slot.angle', color_path='tool_settings.vertex_paint.brush.cursor_color_add', fill_color_path='tool_settings.vertex_paint.brush.color', fill_color_override_path='tool_settings.vertex_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.vertex_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.vertex_paint.brush', secondary_tex=False |
| Ctrl+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.vertex_paint.brush.texture_slot.angle', data_path_secondary='', use_secondary='', rotation_path='tool_settings.vertex_paint.brush.texture_slot.angle', color_path='tool_settings.vertex_paint.brush.cursor_color_add', fill_color_path='tool_settings.vertex_paint.brush.color', fill_color_override_path='tool_settings.vertex_paint.unified_paint_settings.color', fill_color_override_test_path='tool_settings.vertex_paint.brush.use_unified_color', zoom_path='', image_id='tool_settings.vertex_paint.brush', secondary_tex=False |
| Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION' |
| Shift+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE' |
| Ctrl+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION' |
| Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION', texmode='SECONDARY' |
| Shift+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE', texmode='SECONDARY' |
| Ctrl+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION', texmode='SECONDARY' |
| 1 | Context Toggle | `wm.context_toggle` | data_path='vertex_paint_object.data.use_paint_mask' |
| Shift+S | Context Toggle | `wm.context_toggle` | data_path='tool_settings.vertex_paint.brush.use_smooth_stroke' |
| Alt+E | Context Enum Menu | `wm.context_menu_enum` | data_path='tool_settings.vertex_paint.brush.stroke_method' |
| Alt+H | Reveal Faces/Vertices | `paint.face_vert_reveal` |  |
| Alt+A | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_mesh_paint_automasking_pie' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_vertex_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_vertex_context_menu' |
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_vertex_paint' |
| 2 | Context Toggle | `wm.context_toggle` | data_path='vertex_paint_object.data.use_paint_mask_vertex' |

## Weight Paint

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Weight Paint | `paint.weight_paint` |  |
| Ctrl+Left Mouse | Weight Paint | `paint.weight_paint` | mode='INVERT' |
| Shift+Left Mouse | Weight Paint | `paint.weight_paint` | brush_toggle='SMOOTH' |
| Shift+X | Weight Paint Sample Weight | `paint.weight_sample` |  |
| Ctrl+Shift+X | Weight Paint Sample Group | `paint.weight_sample_group` |  |
| Shift+Alt+A | Weight Gradient | `paint.weight_gradient` | type='RADIAL' |
| Shift+A | Weight Gradient | `paint.weight_gradient` | type='LINEAR' |
| Ctrl+X | Set Weight | `paint.weight_set` |  |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.weight_paint.brush.size', data_path_secondary='tool_settings.weight_paint.unified_paint_settings.size', use_secondary='tool_settings.weight_paint.brush.use_unified_size', rotation_path='tool_settings.weight_paint.brush.texture_slot.angle', color_path='tool_settings.weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.weight_paint.brush', secondary_tex=False |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.weight_paint.brush.strength', data_path_secondary='tool_settings.weight_paint.unified_paint_settings.strength', use_secondary='tool_settings.weight_paint.brush.use_unified_strength', rotation_path='tool_settings.weight_paint.brush.texture_slot.angle', color_path='tool_settings.weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.weight_paint.brush', secondary_tex=False |
| Ctrl+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.weight_paint.brush.weight', data_path_secondary='tool_settings.weight_paint.unified_paint_settings.weight', use_secondary='tool_settings.weight_paint.brush.use_unified_weight', rotation_path='tool_settings.weight_paint.brush.texture_slot.angle', color_path='tool_settings.weight_paint.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.weight_paint.brush', secondary_tex=False |
| Alt+E | Context Enum Menu | `wm.context_menu_enum` | data_path='tool_settings.vertex_paint.brush.stroke_method' |
| 1 | Context Toggle | `wm.context_toggle` | data_path='weight_paint_object.data.use_paint_mask' |
| 2 | Context Toggle | `wm.context_toggle` | data_path='weight_paint_object.data.use_paint_mask_vertex' |
| 3 | Context Toggle | `wm.context_toggle` | data_path='weight_paint_object.data.use_paint_bone_selection' |
| Shift+S | Context Toggle | `wm.context_toggle` | data_path='tool_settings.weight_paint.brush.use_smooth_stroke' |
| Alt+A | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_mesh_paint_automasking_pie' |
| K | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_wpaint_vgroup_lock_pie' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_weight_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_paint_weight_context_menu' |
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_weight_paint' |
| Alt+Left Mouse | Select | `view3d.select` |  |
| Shift+Alt+Left Mouse | Select | `view3d.select` | toggle=True |
| Ctrl+Shift+Left Mouse | Select | `view3d.select` |  |

## Paint Face Mask (Weight, Vertex, Texture)

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| A | (De)select All | `paint.face_select_all` | action='SELECT' |
| Alt+A | (De)select All | `paint.face_select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `paint.face_select_all` | action='INVERT' |
| A double click | (De)select All | `paint.face_select_all` | action='DESELECT' |
| Ctrl+Shift+Right Mouse drag | Lasso Select | `view3d.select_lasso` | mode='SUB' |
| Ctrl+Right Mouse drag | Lasso Select | `view3d.select_lasso` | mode='ADD' |
| Alt+H | Reveal Faces/Vertices | `paint.face_vert_reveal` |  |
| H | Face Select Hide | `paint.face_select_hide` | unselected=False |
| Shift+H | Face Select Hide | `paint.face_select_hide` | unselected=True |
| Ctrl+L | Select Linked | `paint.face_select_linked` |  |
| L | Select Linked Pick | `paint.face_select_linked_pick` | deselect=False |
| Shift+L | Select Linked Pick | `paint.face_select_linked_pick` | deselect=True |
| Ctrl+Numpad + | Select More | `paint.face_select_more` |  |
| Ctrl+Numpad - | Select Less | `paint.face_select_less` |  |

## Paint Vertex Selection (Weight, Vertex)

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| A | (De)select All | `paint.vert_select_all` | action='SELECT' |
| Alt+A | (De)select All | `paint.vert_select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `paint.vert_select_all` | action='INVERT' |
| A double click | (De)select All | `paint.vert_select_all` | action='DESELECT' |
| Ctrl+Shift+Right Mouse drag | Lasso Select | `view3d.select_lasso` | mode='SUB' |
| Ctrl+Right Mouse drag | Lasso Select | `view3d.select_lasso` | mode='ADD' |
| Alt+H | Reveal Faces/Vertices | `paint.face_vert_reveal` |  |
| H | Vertex Select Hide | `paint.vert_select_hide` | unselected=False |
| Shift+H | Vertex Select Hide | `paint.vert_select_hide` | unselected=True |
| B | Box Select | `view3d.select_box` |  |
| C | Circle Select | `view3d.select_circle` |  |
| Ctrl+L | Select Linked Vertices | `paint.vert_select_linked` |  |
| L | Select Linked Vertices Pick | `paint.vert_select_linked_pick` | select=True |
| Shift+L | Select Linked Vertices Pick | `paint.vert_select_linked_pick` | select=False |
| Ctrl+Numpad + | Select More | `paint.vert_select_more` |  |
| Ctrl+Numpad - | Select Less | `paint.vert_select_less` |  |

## Sculpt

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Sculpt | `sculpt.brush_stroke` |  |
| Ctrl+Left Mouse | Sculpt | `sculpt.brush_stroke` | mode='INVERT' |
| Shift+Left Mouse | Sculpt | `sculpt.brush_stroke` | brush_toggle='SMOOTH' |
| Alt+Left Mouse | Sculpt | `sculpt.brush_stroke` | brush_toggle='MASK' |
| Ctrl+Alt+Left Mouse | Sculpt | `sculpt.brush_stroke` | mode='INVERT', brush_toggle='MASK' |
| Shift+A | Expand | `sculpt.expand` | target='MASK', falloff_type='GEODESIC', invert=False, use_auto_mask=False, use_mask_preserve=True |
| Shift+Alt+A | Expand | `sculpt.expand` | target='MASK', falloff_type='NORMALS', invert=False, use_mask_preserve=True |
| Shift+W | Expand | `sculpt.expand` | target='FACE_SETS', falloff_type='GEODESIC', invert=False, use_mask_preserve=False, use_modify_active=False |
| Shift+Alt+W | Expand | `sculpt.expand` | target='FACE_SETS', falloff_type='BOUNDARY_FACE_SET', invert=False, use_mask_preserve=False, use_modify_active=True |
| Shift+H | Face Sets Visibility | `sculpt.face_set_change_visibility` | mode='TOGGLE' |
| H | Face Sets Visibility | `sculpt.face_set_change_visibility` | mode='HIDE_ACTIVE' |
| Alt+H | Hide/Show All | `paint.hide_show_all` | action='SHOW' |
| Page Up (repeat) | Visibility Filter | `paint.visibility_filter` | action='GROW' |
| Page Down (repeat) | Visibility Filter | `paint.visibility_filter` | action='SHRINK' |
| Ctrl+W | Edit Face Set | `sculpt.face_set_edit` | mode='GROW' |
| Ctrl+Alt+W | Edit Face Set | `sculpt.face_set_edit` | mode='SHRINK' |
| Ctrl+0 | Subdivision Set | `object.subdivision_set` | level=0, relative=False, ensure_modifier=True |
| Ctrl+1 | Subdivision Set | `object.subdivision_set` | level=1, relative=False, ensure_modifier=True |
| Ctrl+2 | Subdivision Set | `object.subdivision_set` | level=2, relative=False, ensure_modifier=True |
| Ctrl+3 | Subdivision Set | `object.subdivision_set` | level=3, relative=False, ensure_modifier=True |
| Ctrl+4 | Subdivision Set | `object.subdivision_set` | level=4, relative=False, ensure_modifier=True |
| Ctrl+5 | Subdivision Set | `object.subdivision_set` | level=5, relative=False, ensure_modifier=True |
| Alt+1 (repeat) | Subdivision Set | `object.subdivision_set` | level=-1, relative=True, ensure_modifier=False |
| Alt+2 (repeat) | Subdivision Set | `object.subdivision_set` | level=1, relative=True, ensure_modifier=False |
| Alt+M | Mask Flood Fill | `paint.mask_flood_fill` | mode='VALUE', value=0.0 |
| Ctrl+I | Mask Flood Fill | `paint.mask_flood_fill` | mode='INVERT' |
| B | Mask Box Gesture | `paint.mask_box_gesture` | mode='VALUE', value=0.0 |
| R | Edit Dyntopo Detail Size | `sculpt.dyntopo_detail_size_edit` |  |
| Ctrl+R | Detail Flood Fill | `sculpt.detail_flood_fill` |  |
| Ctrl+R | Voxel Remesh | `object.voxel_remesh` |  |
| R | Edit Voxel Size | `object.voxel_size_edit` |  |
| Shift+X | Sample Color | `paint.sample_color` | merged=False |
| Ctrl+Shift+X | Sample Color | `paint.sample_color` | merged=True |
| X | Swap Colors | `paint.brush_colors_flip` |  |
| Ctrl+X | Filter Color | `sculpt.color_filter` | type='FILL', strength=1.0, use_immediate=True |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.sculpt.brush.size', data_path_secondary='tool_settings.sculpt.unified_paint_settings.size', use_secondary='tool_settings.sculpt.brush.use_unified_size', rotation_path='tool_settings.sculpt.brush.texture_slot.angle', color_path='tool_settings.sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.sculpt.brush', secondary_tex=False |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.sculpt.brush.strength', data_path_secondary='tool_settings.sculpt.unified_paint_settings.strength', use_secondary='tool_settings.sculpt.brush.use_unified_strength', rotation_path='tool_settings.sculpt.brush.texture_slot.angle', color_path='tool_settings.sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.sculpt.brush', secondary_tex=False |
| Ctrl+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.sculpt.brush.texture_slot.angle', data_path_secondary='', use_secondary='', rotation_path='tool_settings.sculpt.brush.texture_slot.angle', color_path='tool_settings.sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.sculpt.brush', secondary_tex=False |
| Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION' |
| Shift+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE' |
| Ctrl+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION' |
| Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='TRANSLATION', texmode='SECONDARY' |
| Shift+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='SCALE', texmode='SECONDARY' |
| Ctrl+Alt+Right Mouse | Stencil Brush Control | `brush.stencil_control` | mode='ROTATION', texmode='SECONDARY' |
| Shift+Right Mouse | Set Pivot Position | `sculpt.set_pivot_position` | mode='SURFACE' |
| Alt+E | Context Enum Menu | `wm.context_menu_enum` | data_path='tool_settings.sculpt.brush.stroke_method' |
| Shift+S | Context Toggle | `wm.context_toggle` | data_path='tool_settings.sculpt.brush.use_smooth_stroke' |
| A | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_sculpt_mask_edit_pie' |
| Alt+A | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_mesh_paint_automasking_pie' |
| Alt+W | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_sculpt_face_sets_edit_pie' |
| Right Mouse | Call Panel | `wm.call_panel` | name='VIEW3D_PT_sculpt_context_menu' |
| Application | Call Panel | `wm.call_panel` | name='VIEW3D_PT_sculpt_context_menu' |
| V | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Draw' |
| S | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Smooth' |
| P | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Pinch/Magnify' |
| I | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Inflate/Deflate' |
| G | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Grab' |
| Shift+T | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Scrape/Fill' |
| C | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Clay Strips' |
| Shift+C | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Crease Polish' |
| K | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Snake Hook' |
| M | Activate Brush Asset | `brush.asset_activate` | asset_library_type='ESSENTIALS', relative_asset_identifier='brushes/essentials_brushes-mesh_sculpt.blend/Brush/Mask', use_toggle=True |
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_sculpt' |
| Ctrl+Shift+Right Mouse | Mask Lasso Gesture | `paint.mask_lasso_gesture` | value=1.0 |
| Ctrl+Right Mouse | Mask Lasso Gesture | `paint.mask_lasso_gesture` | value=0.0 |

## Sculpt Curves

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Stroke Curves Sculpt | `sculpt_curves.brush_stroke` |  |
| Ctrl+Left Mouse | Stroke Curves Sculpt | `sculpt_curves.brush_stroke` | mode='INVERT' |
| Shift+Left Mouse | Stroke Curves Sculpt | `sculpt_curves.brush_stroke` | brush_toggle='SMOOTH' |
| 1 | Set Select Mode | `curves.set_selection_domain` | domain='POINT' |
| 2 | Set Select Mode | `curves.set_selection_domain` | domain='CURVE' |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.curves_sculpt.brush.size', data_path_secondary='tool_settings.curves_sculpt.unified_paint_settings.size', use_secondary='tool_settings.curves_sculpt.brush.use_unified_size', rotation_path='tool_settings.curves_sculpt.brush.texture_slot.angle', color_path='tool_settings.curves_sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.curves_sculpt.brush', secondary_tex=False |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.curves_sculpt.brush.strength', data_path_secondary='tool_settings.curves_sculpt.unified_paint_settings.strength', use_secondary='tool_settings.curves_sculpt.brush.use_unified_strength', rotation_path='tool_settings.curves_sculpt.brush.texture_slot.angle', color_path='tool_settings.curves_sculpt.brush.cursor_color_add', fill_color_path='', fill_color_override_path='', fill_color_override_test_path='', zoom_path='', image_id='tool_settings.curves_sculpt.brush', secondary_tex=False |
| [ (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=0.9 |
| ] (repeat) | Scale Sculpt/Paint Brush Size | `brush.scale_size` | scalar=1.1111111111111112 |
| A | (De)select All | `curves.select_all` | action='SELECT' |
| Alt+A | (De)select All | `curves.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `curves.select_all` | action='INVERT' |
| A double click | (De)select All | `curves.select_all` | action='DESELECT' |
| R | Edit Minimum Distance | `sculpt_curves.min_distance_edit` |  |
| Shift+A | Select Grow | `sculpt_curves.select_grow` |  |
| Shift+Space Bar | Call Asset Shelf Popover | `wm.call_asset_shelf_popover` | name='VIEW3D_AST_brush_sculpt_curves' |

## Mesh

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Shift+W | Bend | `transform.bend` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Shift+Alt+S | To Sphere | `transform.tosphere` |  |
| Ctrl+Shift+Alt+S | Shear | `transform.shear` |  |
| Ctrl+A | Skin Resize | `transform.skin_resize` |  |
| Ctrl+R | Loop Cut and Slide | `mesh.loopcut_slide` | TRANSFORM_OT_edge_slide={release_confirm=False} |
| Ctrl+Shift+R | Offset Edge Slide | `mesh.offset_edge_loops_slide` | TRANSFORM_OT_edge_slide={release_confirm=False} |
| I | Inset Faces | `mesh.inset` |  |
| Ctrl+B | Bevel | `mesh.bevel` | affect='EDGES' |
| Alt+S | Shrink/Fatten | `transform.shrink_fatten` |  |
| Ctrl+Shift+B | Bevel | `mesh.bevel` | affect='VERTICES' |
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
| Alt+Left Mouse click | Loop Select | `mesh.loop_select` |  |
| Shift+Alt+Left Mouse click | Loop Select | `mesh.loop_select` | toggle=True |
| Ctrl+Alt+Left Mouse click | Edge Ring Select | `mesh.edgering_select` |  |
| Ctrl+Shift+Alt+Left Mouse click | Edge Ring Select | `mesh.edgering_select` | toggle=True |
| Ctrl+Left Mouse click | Pick Shortest Path | `mesh.shortest_path_pick` | use_fill=False |
| Ctrl+Shift+Left Mouse click | Pick Shortest Path | `mesh.shortest_path_pick` | use_fill=True |
| A | (De)select All | `mesh.select_all` | action='SELECT' |
| Alt+A | (De)select All | `mesh.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `mesh.select_all` | action='INVERT' |
| A double click | (De)select All | `mesh.select_all` | action='DESELECT' |
| Ctrl+Numpad + (repeat) | Select More | `mesh.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `mesh.select_less` |  |
| Ctrl+Shift+Numpad + (repeat) | Select Next Element | `mesh.select_next_item` |  |
| Ctrl+Shift+Numpad - (repeat) | Select Previous Element | `mesh.select_prev_item` |  |
| Ctrl+L | Select Linked All | `mesh.select_linked` |  |
| L | Select Linked | `mesh.select_linked_pick` | deselect=False |
| Shift+L | Select Linked | `mesh.select_linked_pick` | deselect=True |
| Ctrl+Shift+M | Select Mirror | `mesh.select_mirror` |  |
| Shift+G | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_select_similar' |
| Alt+H | Reveal Hidden | `mesh.reveal` |  |
| H | Hide Selected | `mesh.hide` | unselected=False |
| Shift+H | Hide Selected | `mesh.hide` | unselected=True |
| Shift+N | Recalculate Normals | `mesh.normals_make_consistent` | inside=False |
| Ctrl+Shift+N | Recalculate Normals | `mesh.normals_make_consistent` | inside=True |
| E | Extrude and Move on Normals | `view3d.edit_mesh_extrude_move_normal` |  |
| Alt+E | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_extrude' |
| Shift+E | Edge Crease | `transform.edge_crease` |  |
| Alt+F | Fill | `mesh.fill` |  |
| Ctrl+T | Triangulate Faces | `mesh.quads_convert_to_tris` | quad_method='BEAUTY', ngon_method='BEAUTY' |
| Ctrl+Shift+T | Triangulate Faces | `mesh.quads_convert_to_tris` | quad_method='FIXED', ngon_method='CLIP' |
| Alt+J | Triangles to Quads | `mesh.tris_convert_to_quads` |  |
| V | Rip | `mesh.rip_move` | MESH_OT_rip={use_fill=False} |
| Alt+V | Rip | `mesh.rip_move` | MESH_OT_rip={use_fill=True} |
| Alt+D | Extend Vertices | `mesh.rip_edge_move` |  |
| M | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_merge' |
| Alt+M | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_split' |
| F (repeat) | Make Edge/Face | `mesh.edge_face_add` |  |
| Shift+D | Add Duplicate | `mesh.duplicate_move` |  |
| Shift+A | Call Menu | `wm.call_menu` | name='VIEW3D_MT_mesh_add' |
| P | Separate | `mesh.separate` |  |
| Y | Split | `mesh.split` |  |
| J | Vertex Connect Path | `mesh.vert_connect_path` |  |
| Alt+L | Point Normals to Target | `mesh.point_normals` |  |
| Shift+V | Vertex Slide | `transform.vert_slide` |  |
| Ctrl+Right Mouse click | Extrude to Cursor or Add | `mesh.dupli_extrude_cursor` | rotate_source=True |
| Ctrl+Shift+Right Mouse click | Extrude to Cursor or Add | `mesh.dupli_extrude_cursor` | rotate_source=False |
| X | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_delete' |
| Delete | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_delete' |
| Ctrl+X | Dissolve Selection | `mesh.dissolve_mode` |  |
| Ctrl+Delete | Dissolve Selection | `mesh.dissolve_mode` |  |
| K | Knife Topology Tool | `mesh.knife_tool` | use_occlude_geometry=True, only_selected=False |
| Shift+K | Knife Topology Tool | `mesh.knife_tool` | use_occlude_geometry=False, only_selected=True |
| Ctrl+P | Make Vertex Parent | `object.vertex_parent_set` |  |
| Ctrl+F | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_faces' |
| Ctrl+E | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_edges' |
| Ctrl+V | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_vertices' |
| Ctrl+H | Call Menu | `wm.call_menu` | name='VIEW3D_MT_hook' |
| U | Call Menu | `wm.call_menu` | name='VIEW3D_MT_uv_map' |
| Ctrl+G | Call Menu | `wm.call_menu` | name='VIEW3D_MT_vertex_group' |
| Alt+N | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_normals' |
| Ctrl+Alt+G | Remove from Vertex Group | `object.vertex_group_remove_from` |  |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Alt+O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_connected' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_mesh_context_menu' |

## Armature

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Alt+H | Reveal Hidden | `armature.reveal` |  |
| H | Hide Selected | `armature.hide` | unselected=False |
| Shift+H | Hide Selected | `armature.hide` | unselected=True |
| Ctrl+Alt+A | Align Bones | `armature.align` |  |
| Shift+N | Recalculate Roll | `armature.calculate_roll` |  |
| Alt+R | Clear Roll | `armature.roll_clear` |  |
| Alt+F | Switch Direction | `armature.switch_direction` |  |
| Shift+A | Add Bone | `armature.bone_primitive_add` |  |
| Ctrl+P | Make Parent | `armature.parent_set` |  |
| Alt+P | Clear Parent | `armature.parent_clear` |  |
| A | (De)select All | `armature.select_all` | action='SELECT' |
| Alt+A | (De)select All | `armature.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `armature.select_all` | action='INVERT' |
| A double click | (De)select All | `armature.select_all` | action='DESELECT' |
| Ctrl+Shift+M | Select Mirror | `armature.select_mirror` | extend=False |
| [ | Select Hierarchy | `armature.select_hierarchy` | direction='PARENT', extend=False |
| Shift+[ | Select Hierarchy | `armature.select_hierarchy` | direction='PARENT', extend=True |
| ] | Select Hierarchy | `armature.select_hierarchy` | direction='CHILD', extend=False |
| Shift+] | Select Hierarchy | `armature.select_hierarchy` | direction='CHILD', extend=True |
| Ctrl+Numpad + (repeat) | Select More | `armature.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `armature.select_less` |  |
| Shift+G | Select Similar | `armature.select_similar` |  |
| L | Select Linked | `armature.select_linked_pick` | deselect=False |
| Shift+L | Select Linked | `armature.select_linked_pick` | deselect=True |
| Ctrl+L | Select Linked All | `armature.select_linked` |  |
| Ctrl+Left Mouse click | Pick Shortest Path | `armature.shortest_path_pick` |  |
| X | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_armature_delete' |
| Delete | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_armature_delete' |
| Shift+D | Duplicate | `armature.duplicate_move` |  |
| Ctrl+X | Dissolve Selected Bone(s) | `armature.dissolve` |  |
| Ctrl+Delete | Dissolve Selected Bone(s) | `armature.dissolve` |  |
| E | Extrude | `armature.extrude_move` |  |
| Shift+E | Extrude Forked | `armature.extrude_forked` |  |
| Ctrl+Right Mouse click | Extrude to Cursor | `armature.click_extrude` |  |
| F | Fill Between Joints | `armature.fill` |  |
| Y | Split | `armature.split` |  |
| P | Separate Bones | `armature.separate` |  |
| Shift+W | Call Menu | `wm.call_menu` | name='VIEW3D_MT_bone_options_toggle' |
| Ctrl+Shift+W | Call Menu | `wm.call_menu` | name='VIEW3D_MT_bone_options_enable' |
| Alt+W | Call Menu | `wm.call_menu` | name='VIEW3D_MT_bone_options_disable' |
| Shift+M | Assign to Collection | `armature.assign_to_collection` |  |
| M | Move to Collection | `armature.move_to_collection` |  |
| Ctrl+Shift+Alt+S | Scale B-Bone | `transform.bbone_resize` |  |
| Alt+S | Transform | `transform.transform` | mode='BONE_ENVELOPE_DIST' |
| Ctrl+R | Transform | `transform.transform` | mode='BONE_ROLL' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_armature_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_armature_context_menu' |

## Metaball

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Shift+A | Add Metaball | `object.metaball_add` |  |
| Alt+H | Reveal Hidden | `mball.reveal_metaelems` |  |
| H | Hide Selected | `mball.hide_metaelems` | unselected=False |
| Shift+H | Hide Selected | `mball.hide_metaelems` | unselected=True |
| X | Delete | `mball.delete_metaelems` |  |
| Delete | Delete | `mball.delete_metaelems` |  |
| Shift+D | Duplicate | `mball.duplicate_move` |  |
| A | (De)select All | `mball.select_all` | action='SELECT' |
| Alt+A | (De)select All | `mball.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `mball.select_all` | action='INVERT' |
| A double click | (De)select All | `mball.select_all` | action='DESELECT' |
| Shift+G | Select Similar | `mball.select_similar` |  |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Alt+O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_connected' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_metaball_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_metaball_context_menu' |

## Lattice

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Shift+W | Bend | `transform.bend` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Shift+Alt+S | To Sphere | `transform.tosphere` |  |
| Ctrl+Shift+Alt+S | Shear | `transform.shear` |  |
| A | (De)select All | `lattice.select_all` | action='SELECT' |
| Alt+A | (De)select All | `lattice.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `lattice.select_all` | action='INVERT' |
| A double click | (De)select All | `lattice.select_all` | action='DESELECT' |
| Ctrl+Numpad + (repeat) | Select More | `lattice.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `lattice.select_less` |  |
| Ctrl+P | Make Vertex Parent | `object.vertex_parent_set` |  |
| Alt+F | Flip (Distortion Free) | `lattice.flip` |  |
| Ctrl+H | Call Menu | `wm.call_menu` | name='VIEW3D_MT_hook' |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_lattice_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_lattice_context_menu' |

## Particle

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| A | (De)select All | `particle.select_all` | action='SELECT' |
| Alt+A | (De)select All | `particle.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `particle.select_all` | action='INVERT' |
| A double click | (De)select All | `particle.select_all` | action='DESELECT' |
| Ctrl+Numpad + (repeat) | Select More | `particle.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `particle.select_less` |  |
| L | Select Linked | `particle.select_linked_pick` | deselect=False |
| Shift+L | Select Linked | `particle.select_linked_pick` | deselect=True |
| Ctrl+L | Select Linked All | `particle.select_linked` |  |
| X | Delete | `particle.delete` |  |
| Delete | Delete | `particle.delete` |  |
| Alt+H | Reveal | `particle.reveal` |  |
| H | Hide Selected | `particle.hide` | unselected=False |
| Shift+H | Hide Selected | `particle.hide` | unselected=True |
| Left Mouse | Brush Edit | `particle.brush_edit` |  |
| Shift+Left Mouse | Brush Edit | `particle.brush_edit` |  |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.particle_edit.brush.size' |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.particle_edit.brush.strength' |
| Shift+K | Weight Set | `particle.weight_set` |  |
| 1 | Context Set Enum | `wm.context_set_enum` | data_path='tool_settings.particle_edit.select_mode', value='PATH' |
| 2 | Context Set Enum | `wm.context_set_enum` | data_path='tool_settings.particle_edit.select_mode', value='POINT' |
| 3 | Context Set Enum | `wm.context_set_enum` | data_path='tool_settings.particle_edit.select_mode', value='TIP' |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_particle_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_particle_context_menu' |
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |

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
| Shift+Alt+Left Arrow (repeat) | Change Spacing | `font.change_spacing` | delta=-0.1 |
| Shift+Alt+Right Arrow (repeat) | Change Spacing | `font.change_spacing` | delta=0.1 |
| Alt+Up Arrow (repeat) | Change Character | `font.change_character` | delta=1 |
| Alt+Down Arrow (repeat) | Change Character | `font.change_character` | delta=-1 |
| Ctrl+A | Select All | `font.select_all` |  |
| Ctrl+C | Copy Text | `font.text_copy` |  |
| Ctrl+X | Cut Text | `font.text_cut` |  |
| Ctrl+V (repeat) | Paste Text | `font.text_paste` |  |
| Return (repeat) | Line Break | `font.line_break` |  |
| Numpad Enter (repeat) | Line Break | `font.line_break` |  |
| Any modifier+Text Input any (repeat) | Insert Text | `font.text_insert` |  |
| Alt+Backspace (repeat) | Insert Text | `font.text_insert` | accent=True |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_font_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_font_context_menu' |

## Curve

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Shift+W | Bend | `transform.bend` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Shift+A | Call Menu | `wm.call_menu` | name='TOPBAR_MT_edit_curve_add' |
| V | Set Handle Type | `curve.handle_type_set` |  |
| Ctrl+Right Mouse click | Extrude to Cursor or Add | `curve.vertex_add` |  |
| A | (De)select All | `curve.select_all` | action='SELECT' |
| Alt+A | (De)select All | `curve.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `curve.select_all` | action='INVERT' |
| A double click | (De)select All | `curve.select_all` | action='DESELECT' |
| Ctrl+Shift+R | Select Control Point Row | `curve.select_row` |  |
| Ctrl+Numpad + (repeat) | Select More | `curve.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `curve.select_less` |  |
| Ctrl+L | Select Linked All | `curve.select_linked` |  |
| Shift+G | Select Similar | `curve.select_similar` |  |
| L | Select Linked | `curve.select_linked_pick` | deselect=False |
| Shift+L | Select Linked | `curve.select_linked_pick` | deselect=True |
| Ctrl+Left Mouse click | Pick Shortest Path | `curve.shortest_path_pick` |  |
| P | Separate | `curve.separate` |  |
| Y | Split | `curve.split` |  |
| E | Extrude Curve and Move | `curve.extrude_move` |  |
| Shift+D | Add Duplicate | `curve.duplicate_move` |  |
| F | Make Segment | `curve.make_segment` |  |
| Alt+C | Toggle Cyclic | `curve.cyclic_toggle` |  |
| X | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curve_delete' |
| Delete | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curve_delete' |
| Ctrl+X | Dissolve Vertices | `curve.dissolve_verts` |  |
| Ctrl+Delete | Dissolve Vertices | `curve.dissolve_verts` |  |
| Alt+T | Clear Tilt | `curve.tilt_clear` |  |
| Ctrl+T | Tilt | `transform.tilt` |  |
| Alt+S | Transform | `transform.transform` | mode='CURVE_SHRINKFATTEN' |
| Alt+H | Reveal Hidden | `curve.reveal` |  |
| H | Hide Selected | `curve.hide` | unselected=False |
| Shift+H | Hide Selected | `curve.hide` | unselected=True |
| Shift+N | Recalculate Handles | `curve.normals_make_consistent` |  |
| Ctrl+P | Make Vertex Parent | `object.vertex_parent_set` |  |
| Ctrl+H | Call Menu | `wm.call_menu` | name='VIEW3D_MT_hook' |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Alt+O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_connected' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curve_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curve_context_menu' |

## Curves

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Shift+W | Bend | `transform.bend` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| 1 | Set Select Mode | `curves.set_selection_domain` | domain='POINT' |
| 2 | Set Select Mode | `curves.set_selection_domain` | domain='CURVE' |
| Shift+D | Duplicate | `curves.duplicate_move` |  |
| A | (De)select All | `curves.select_all` | action='SELECT' |
| Alt+A | (De)select All | `curves.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `curves.select_all` | action='INVERT' |
| A double click | (De)select All | `curves.select_all` | action='DESELECT' |
| E | Extrude Curve and Move | `curves.extrude_move` |  |
| Ctrl+L | Select Linked | `curves.select_linked` |  |
| L | Select Linked | `curves.select_linked_pick` | deselect=False |
| Shift+L | Select Linked | `curves.select_linked_pick` | deselect=True |
| X | Delete | `curves.delete` |  |
| Delete | Delete | `curves.delete` |  |
| P | Separate | `curves.separate` |  |
| Ctrl+Numpad + (repeat) | Select More | `curves.select_more` |  |
| Ctrl+Numpad - (repeat) | Select Less | `curves.select_less` |  |
| Y | Split | `curves.split` |  |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Alt+O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_connected' |
| Alt+T | Clear Tilt | `curves.tilt_clear` |  |
| Ctrl+T | Tilt | `transform.tilt` |  |
| Alt+S | Transform | `transform.transform` | mode='CURVE_SHRINKFATTEN' |
| Alt+C | Toggle Cyclic | `curves.cyclic_toggle` |  |
| V | Set Handle Type | `curves.handle_type_set` |  |
| Shift+A | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curves_add' |
| Right Mouse | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curves_context_menu' |
| Application | Call Menu | `wm.call_menu` | name='VIEW3D_MT_edit_curves_context_menu' |

## Point Cloud

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| G | Move | `transform.translate` |  |
| R | Rotate | `transform.rotate` |  |
| S | Resize | `transform.resize` |  |
| Left Mouse drag | Move | `transform.translate` |  |
| Shift+W | Bend | `transform.bend` |  |
| Ctrl+M | Mirror | `transform.mirror` |  |
| Shift+D | Duplicate | `pointcloud.duplicate_move` |  |
| A | (De)select All | `pointcloud.select_all` | action='SELECT' |
| Alt+A | (De)select All | `pointcloud.select_all` | action='DESELECT' |
| Ctrl+I | (De)select All | `pointcloud.select_all` | action='INVERT' |
| A double click | (De)select All | `pointcloud.select_all` | action='DESELECT' |
| X | Delete | `pointcloud.delete` |  |
| Delete | Delete | `pointcloud.delete` |  |
| P | Separate | `pointcloud.separate` |  |
| Alt+S | Transform | `transform.transform` | mode='CURVE_SHRINKFATTEN' |
| Shift+O | Call Pie Menu | `wm.call_menu_pie` | name='VIEW3D_MT_proportional_editing_falloff_pie' |
| O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_edit' |
| Alt+O | Context Toggle | `wm.context_toggle` | data_path='tool_settings.use_proportional_connected' |

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
| F | NODE_FRAME | `NODE_FRAME` |  |
| Middle Mouse any | AUTOCONSTRAIN | `AUTOCONSTRAIN` |  |
| Shift+Middle Mouse any | AUTOCONSTRAINPLANE | `AUTOCONSTRAINPLANE` |  |
| Any modifier+Left Shift any | PRECISION | `PRECISION` |  |
| Any modifier+Right Shift any | PRECISION | `PRECISION` |  |
| Any modifier+C | STRIP_CLAMP_TOGGLE | `STRIP_CLAMP_TOGGLE` |  |
| S | STRIP_OVERLAP_SHUFFLE | `STRIP_OVERLAP_SHUFFLE` |  |
| R | STRIP_OVERLAP_RIPPLE | `STRIP_OVERLAP_RIPPLE` |  |
| V | STRIP_OVERLAP_OVERWRITE | `STRIP_OVERLAP_OVERWRITE` |  |
| I | STRIP_RIPPLE_INSERT | `STRIP_RIPPLE_INSERT` |  |
| Any modifier+Left Alt any | PASSTHROUGH_NAVIGATE | `PASSTHROUGH_NAVIGATE` |  |

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

## Knife Tool Modal Map

Space `EMPTY`, region `WINDOW`, **modal** (keys while a tool runs)

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Any modifier+Esc | CANCEL | `CANCEL` |  |
| Any modifier+Middle Mouse any | PANNING | `PANNING` |  |
| Any modifier+Left Mouse double click | ADD_CUT_CLOSED | `ADD_CUT_CLOSED` |  |
| Any modifier+Left Mouse any | ADD_CUT | `ADD_CUT` |  |
| Ctrl+Z | UNDO | `UNDO` |  |
| Any modifier+Return | CONFIRM | `CONFIRM` |  |
| Any modifier+Numpad Enter | CONFIRM | `CONFIRM` |  |
| Any modifier+Space Bar | CONFIRM | `CONFIRM` |  |
| Right Mouse | NEW_CUT | `NEW_CUT` |  |
| Any modifier+Left Shift | SNAP_MIDPOINTS_ON | `SNAP_MIDPOINTS_ON` |  |
| Any modifier+Left Shift release | SNAP_MIDPOINTS_OFF | `SNAP_MIDPOINTS_OFF` |  |
| Any modifier+Right Shift | SNAP_MIDPOINTS_ON | `SNAP_MIDPOINTS_ON` |  |
| Any modifier+Right Shift release | SNAP_MIDPOINTS_OFF | `SNAP_MIDPOINTS_OFF` |  |
| Any modifier+Left Ctrl | IGNORE_SNAP_ON | `IGNORE_SNAP_ON` |  |
| Any modifier+Left Ctrl release | IGNORE_SNAP_OFF | `IGNORE_SNAP_OFF` |  |
| Any modifier+Right Ctrl | IGNORE_SNAP_ON | `IGNORE_SNAP_ON` |  |
| Any modifier+Right Ctrl release | IGNORE_SNAP_OFF | `IGNORE_SNAP_OFF` |  |
| X | X_AXIS | `X_AXIS` |  |
| Y | Y_AXIS | `Y_AXIS` |  |
| Z | Z_AXIS | `Z_AXIS` |  |
| A | ANGLE_SNAP_TOGGLE | `ANGLE_SNAP_TOGGLE` |  |
| R | CYCLE_ANGLE_SNAP_EDGE | `CYCLE_ANGLE_SNAP_EDGE` |  |
| C | CUT_THROUGH_TOGGLE | `CUT_THROUGH_TOGGLE` |  |
| S | SHOW_DISTANCE_ANGLE_TOGGLE | `SHOW_DISTANCE_ANGLE_TOGGLE` |  |
| V | DEPTH_TEST_TOGGLE | `DEPTH_TEST_TOGGLE` |  |

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

## Generic Gizmo Drag

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| [Ctrl]+[Shift]+[OS]+[Hyper]+Left Mouse drag | Gizmo Tweak | `gizmogroup.gizmo_tweak` |  |

## Generic Gizmo Maybe Drag

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| [Ctrl]+[Shift]+[OS]+[Hyper]+Left Mouse drag | Gizmo Tweak | `gizmogroup.gizmo_tweak` |  |

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

## Generic Tool: Annotate Line

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Annotation Draw | `gpencil.annotate` | mode='DRAW_STRAIGHT', wait_for_input=False |
| Ctrl+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |

## Generic Tool: Annotate Polygon

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Annotation Draw | `gpencil.annotate` | mode='DRAW_POLY', wait_for_input=False |
| Ctrl+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |

## Generic Tool: Annotate Eraser

Space `EMPTY`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |
| Ctrl+Left Mouse | Annotation Draw | `gpencil.annotate` | mode='ERASER', wait_for_input=False |

## Image Editor Tool: Sample

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Sample Color | `image.sample` |  |

## Image Editor Tool: Uv, Cursor

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set 2D Cursor | `uv.cursor_set` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## Image Editor Tool: Uv, Tweak

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `uv.select` | deselect_all=True, select_passthrough=True |
| Left Mouse click | Select | `uv.select` | deselect_all=True |
| Shift+Left Mouse | Select | `uv.select` | deselect_all=False, toggle=True |

## Image Editor Tool: Uv, Tweak (fallback)

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `uv.select` | deselect_all=True, select_passthrough=True |
| Shift+Left Mouse | Select | `uv.select` | toggle=True |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |

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
| Left Mouse drag | Circle Select | `uv.select_circle` | wait_for_input=False |
| Shift+Left Mouse drag | Circle Select | `uv.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse drag | Circle Select | `uv.select_circle` | wait_for_input=False, mode='SUB' |

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

## Image Editor Tool: Uv, Grab

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grab UVs | `sculpt.uv_sculpt_grab` |  |
| Ctrl+Left Mouse | Grab UVs | `sculpt.uv_sculpt_grab` | use_invert=True |
| Shift+Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.size' |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.strength' |

## Image Editor Tool: Uv, Relax

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |
| Ctrl+Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` | use_invert=True |
| Shift+Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.size' |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.strength' |

## Image Editor Tool: Uv, Pinch

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Pinch UVs | `sculpt.uv_sculpt_pinch` |  |
| Ctrl+Left Mouse | Pinch UVs | `sculpt.uv_sculpt_pinch` | use_invert=True |
| Shift+Left Mouse | Relax UVs | `sculpt.uv_sculpt_relax` |  |
| F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.size' |
| Shift+F | Radial Control | `wm.radial_control` | data_path_primary='tool_settings.uv_sculpt.strength' |

## Image Editor Tool: Uv, Move

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |

## Image Editor Tool: Uv, Rotate

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rotate | `transform.rotate` | release_confirm=True |

## Image Editor Tool: Uv, Scale

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |

## Image Editor Tool: Mask, Cursor

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set 2D Cursor | `uv.cursor_set` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## Image Editor Tool: Mask, Tweak

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `mask.select` | deselect_all=True, select_passthrough=True |
| Left Mouse click | Select | `mask.select` | deselect_all=True |
| Shift+Left Mouse | Select | `mask.select` | deselect_all=False, toggle=True |

## Image Editor Tool: Mask, Tweak (fallback)

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `mask.select` | deselect_all=True, select_passthrough=True |
| Shift+Left Mouse | Select | `mask.select` | toggle=True |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |

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
| Left Mouse drag | Circle Select | `mask.select_circle` | wait_for_input=False |
| Shift+Left Mouse drag | Circle Select | `mask.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse drag | Circle Select | `mask.select_circle` | wait_for_input=False, mode='SUB' |

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

## Image Editor Tool: Mask, Rotate

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rotate | `transform.rotate` | release_confirm=True |

## Image Editor Tool: Mask, Scale

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |

## Image Editor Tool: Mask, Transform

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |

## Image Editor Tool: Mask, Circle

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Add Circle | `mask.primitive_circle_add` |  |

## Image Editor Tool: Mask, Box

Space `IMAGE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Add Square | `mask.primitive_square_add` |  |

## Node Tool: Tweak

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `node.select` | select_passthrough=True |
| Ctrl+Left Mouse | Select | `node.select` |  |
| Alt+Left Mouse | Select | `node.select` |  |
| Ctrl+Alt+Left Mouse | Select | `node.select` |  |
| Shift+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Left Mouse | Select | `node.select` | toggle=True |
| Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Left Mouse click | Select | `node.select` | deselect_all=True |

## Node Tool: Tweak (fallback)

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `node.select` | select_passthrough=True |
| Ctrl+Left Mouse | Select | `node.select` |  |
| Alt+Left Mouse | Select | `node.select` |  |
| Ctrl+Alt+Left Mouse | Select | `node.select` |  |
| Shift+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Left Mouse | Select | `node.select` | toggle=True |
| Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Left Mouse click | Select | `node.select` | deselect_all=True |

## Node Tool: Select Box

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `node.select_box` | tweak=True |
| Shift+Left Mouse drag | Box Select | `node.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `node.select_box` | tweak=True, mode='SUB' |
| Left Mouse | Select | `node.select` | select_passthrough=True |
| Ctrl+Left Mouse | Select | `node.select` |  |
| Alt+Left Mouse | Select | `node.select` |  |
| Ctrl+Alt+Left Mouse | Select | `node.select` |  |
| Shift+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Left Mouse | Select | `node.select` | toggle=True |
| Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Left Mouse click | Select | `node.select` | deselect_all=True |

## Node Tool: Select Box (fallback)

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `node.select_box` | tweak=True |
| Shift+Left Mouse drag | Box Select | `node.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `node.select_box` | tweak=True, mode='SUB' |
| Left Mouse | Select | `node.select` | select_passthrough=True |
| Ctrl+Left Mouse | Select | `node.select` |  |
| Alt+Left Mouse | Select | `node.select` |  |
| Ctrl+Alt+Left Mouse | Select | `node.select` |  |
| Shift+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Left Mouse | Select | `node.select` | toggle=True |
| Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Ctrl+Shift+Alt+Left Mouse | Select | `node.select` | toggle=True |
| Left Mouse click | Select | `node.select` | deselect_all=True |

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
| Left Mouse drag | Circle Select | `node.select_circle` | wait_for_input=False |
| Shift+Left Mouse drag | Circle Select | `node.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse drag | Circle Select | `node.select_circle` | wait_for_input=False, mode='SUB' |

## Node Tool: Links Cut

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Cut Links | `node.links_cut` |  |

## Node Tool: Mute Links

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mute Links | `node.links_mute` |  |

## Node Tool: Add Reroute

Space `NODE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Add Reroute | `node.add_reroute` |  |

## 3D View Tool: Cursor

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set 3D Cursor | `view3d.cursor3d` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## 3D View Tool: Edit Text, Select Text

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set Selection | `font.selection_set` |  |
| Left Mouse double click | Select Word | `font.select_word` |  |

## 3D View Tool: Tweak

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `view3d.select` | deselect_all=True, select_passthrough=True |
| Left Mouse click | Select | `view3d.select` | deselect_all=True |
| Shift+Left Mouse | Select | `view3d.select` | deselect_all=False, toggle=True |
| Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=False |
| Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=False |

## 3D View Tool: Tweak (fallback)

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `view3d.select` | deselect_all=True, select_passthrough=True |
| Shift+Left Mouse | Select | `view3d.select` | toggle=True |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |
| Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=False |
| Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=False |

## 3D View Tool: Select Box

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `view3d.select_box` |  |
| Shift+Left Mouse drag | Box Select | `view3d.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `view3d.select_box` | mode='SUB' |
| Ctrl+Shift+Left Mouse drag | Box Select | `view3d.select_box` | mode='AND' |
| Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=False |
| Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=False |

## 3D View Tool: Select Box (fallback)

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Box Select | `view3d.select_box` |  |
| Shift+Left Mouse drag | Box Select | `view3d.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `view3d.select_box` | mode='SUB' |
| Ctrl+Shift+Left Mouse drag | Box Select | `view3d.select_box` | mode='AND' |
| Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=False |
| Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=False |

## 3D View Tool: Select Circle

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Circle Select | `view3d.select_circle` | wait_for_input=False |
| Shift+Left Mouse | Circle Select | `view3d.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse | Circle Select | `view3d.select_circle` | wait_for_input=False, mode='SUB' |
| Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=False |
| Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=False |

## 3D View Tool: Select Circle (fallback)

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Circle Select | `view3d.select_circle` | wait_for_input=False |
| Shift+Left Mouse drag | Circle Select | `view3d.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse drag | Circle Select | `view3d.select_circle` | wait_for_input=False, mode='SUB' |
| Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=False |
| Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=False |

## 3D View Tool: Select Lasso

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `view3d.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='SUB' |
| Ctrl+Shift+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='AND' |
| Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=False |
| Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=False |

## 3D View Tool: Select Lasso (fallback)

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Lasso Select | `view3d.select_lasso` |  |
| Shift+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='ADD' |
| Ctrl+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='SUB' |
| Ctrl+Shift+Left Mouse drag | Lasso Select | `view3d.select_lasso` | mode='AND' |
| Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.face_select_loop` | extend=True, select=False |
| Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=False, select=True |
| Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=True |
| Ctrl+Shift+Alt+Left Mouse | Select Loop | `paint.vert_select_loop` | extend=True, select=False |

## 3D View Tool: Transform

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Transform from Gizmo | `transform.from_gizmo` |  |

## 3D View Tool: Move

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |

## 3D View Tool: Rotate

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rotate | `transform.rotate` | release_confirm=True |

## 3D View Tool: Scale

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |

## 3D View Tool: Shear

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag north | Shear | `transform.shear` | release_confirm=True, orient_axis_ortho='Y' |
| Left Mouse drag south | Shear | `transform.shear` | release_confirm=True, orient_axis_ortho='Y' |
| Left Mouse drag | Shear | `transform.shear` | release_confirm=True, orient_axis_ortho='X' |

## 3D View Tool: Bend

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Bend | `transform.bend` | release_confirm=True |

## 3D View Tool: Measure

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Ruler Add | `view3d.ruler_add` |  |
| X | Ruler Remove | `view3d.ruler_remove` |  |
| Delete | Ruler Remove | `view3d.ruler_remove` |  |

## 3D View Tool: Object, Add Primitive

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| [Ctrl]+[Shift]+[OS]+[Hyper]+Left Mouse drag | Add Primitive Object | `view3d.interactive_add` | wait_for_input=False |

## 3D View Tool: Breakdowner

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Pose Breakdowner | `pose.breakdown` |  |

## 3D View Tool: Push

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Push Pose from Breakdown | `pose.push` |  |

## 3D View Tool: Relax

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Relax Pose to Breakdown | `pose.relax` |  |

## 3D View Tool: Edit Armature, Roll

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Transform | `transform.transform` | release_confirm=True, mode='BONE_ROLL' |

## 3D View Tool: Edit Armature, B-Bone Size

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Scale B-Bone | `transform.bbone_resize` | release_confirm=True |

## 3D View Tool: Edit Armature, Bone Envelope

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Transform | `transform.transform` | release_confirm=True, mode='BONE_ENVELOPE_DIST' |

## 3D View Tool: Edit Armature, Extrude

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude | `armature.extrude_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Armature, Extrude to Cursor

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Extrude to Cursor | `armature.click_extrude` |  |

## 3D View Tool: Edit Mesh, Extrude Region

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Region and Move | `mesh.extrude_context_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Mesh, Extrude Manifold

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Manifold | `mesh.extrude_manifold` | MESH_OT_extrude_region={use_dissolve_ortho_edges=True}, TRANSFORM_OT_translate={release_confirm=True, use_automerge_and_split=True, constraint_axis=(False, False, True), orient_type='NORMAL'} |

## 3D View Tool: Edit Mesh, Extrude Along Normals

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Region and Shrink/Fatten | `mesh.extrude_region_shrink_fatten` | TRANSFORM_OT_shrink_fatten={release_confirm=True} |

## 3D View Tool: Edit Mesh, Extrude Individual

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Individual Faces and Move | `mesh.extrude_faces_move` | TRANSFORM_OT_shrink_fatten={release_confirm=True} |

## 3D View Tool: Edit Mesh, Extrude to Cursor

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Extrude to Cursor or Add | `mesh.dupli_extrude_cursor` |  |

## 3D View Tool: Edit Mesh, Inset Faces

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Inset Faces | `mesh.inset` | release_confirm=True |

## 3D View Tool: Edit Mesh, Bevel

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Bevel | `mesh.bevel` | release_confirm=True |

## 3D View Tool: Edit Mesh, Loop Cut

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Loop Cut and Slide | `mesh.loopcut_slide` | TRANSFORM_OT_edge_slide={release_confirm=True} |

## 3D View Tool: Edit Mesh, Offset Edge Loop Cut

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Offset Edge Slide | `mesh.offset_edge_loops_slide` |  |

## 3D View Tool: Edit Mesh, Knife

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Knife Topology Tool | `mesh.knife_tool` | wait_for_input=False |

## 3D View Tool: Edit Mesh, Bisect

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Bisect | `mesh.bisect` |  |

## 3D View Tool: Edit Mesh, Poly Build

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Extrude at Cursor Move | `mesh.polybuild_extrude_at_cursor_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Ctrl+Left Mouse | Face at Cursor Move | `mesh.polybuild_face_at_cursor_move` | TRANSFORM_OT_translate={release_confirm=True} |
| Shift+Left Mouse click | Poly Build Delete at Cursor | `mesh.polybuild_delete_at_cursor` |  |

## 3D View Tool: Edit Mesh, Spin

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Spin | `mesh.spin` |  |

## 3D View Tool: Edit Mesh, Spin Duplicates

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Spin | `mesh.spin` | dupli=True |

## 3D View Tool: Edit Mesh, Smooth

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Smooth Vertices | `mesh.vertices_smooth` | wait_for_input=False |

## 3D View Tool: Edit Mesh, Randomize

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Randomize | `transform.vertex_random` | wait_for_input=False |

## 3D View Tool: Edit Mesh, Edge Slide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Edge Slide | `transform.edge_slide` | release_confirm=True |

## 3D View Tool: Edit Mesh, Vertex Slide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Vertex Slide | `transform.vert_slide` | release_confirm=True |

## 3D View Tool: Edit Mesh, Shrink/Fatten

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Shrink/Fatten | `transform.shrink_fatten` | release_confirm=True |

## 3D View Tool: Edit Mesh, Push/Pull

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Push/Pull | `transform.push_pull` | release_confirm=True |

## 3D View Tool: Edit Mesh, To Sphere

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | To Sphere | `transform.tosphere` | release_confirm=True |

## 3D View Tool: Edit Mesh, Rip Region

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rip | `mesh.rip_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Mesh, Rip Edge

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extend Vertices | `mesh.rip_edge_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Curve, Draw

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Draw Curve | `curve.draw` | wait_for_input=False |

## 3D View Tool: Edit Curve, Curve Pen

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Curve Pen | `curve.pen` | extrude_point=True, move_segment=True, select_point=True, move_point=True, close_spline_method='ON_CLICK' |
| Ctrl+Left Mouse | Curve Pen | `curve.pen` | insert_point=True, delete_point=True |
| Left Mouse double click | Curve Pen | `curve.pen` | toggle_vector=True, cycle_handle_type=True |

## 3D View Tool: Edit Curve, Radius

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Transform | `transform.transform` | mode='CURVE_SHRINKFATTEN', release_confirm=True |

## 3D View Tool: Edit Curve, Tilt

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Tilt | `transform.tilt` | release_confirm=True |

## 3D View Tool: Edit Curve, Randomize

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Randomize | `transform.vertex_random` | wait_for_input=False |

## 3D View Tool: Edit Curve, Extrude

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Extrude Curve and Move | `curve.extrude_move` | TRANSFORM_OT_translate={release_confirm=True} |

## 3D View Tool: Edit Curve, Extrude to Cursor

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Extrude to Cursor or Add | `curve.vertex_add` |  |

## 3D View Tool: Edit Curves, Draw

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Draw Curves | `curves.draw` | wait_for_input=False |

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

## 3D View Tool: Sculpt, Box Mask

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Mask Box Gesture | `paint.mask_box_gesture` | value=1.0 |
| Ctrl+Left Mouse drag | Mask Box Gesture | `paint.mask_box_gesture` | value=0.0 |

## 3D View Tool: Sculpt, Lasso Mask

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Mask Lasso Gesture | `paint.mask_lasso_gesture` | value=1.0 |
| Ctrl+Left Mouse drag | Mask Lasso Gesture | `paint.mask_lasso_gesture` | value=0.0 |

## 3D View Tool: Sculpt, Line Mask

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Mask Line Gesture | `paint.mask_line_gesture` | value=1.0 |
| Ctrl+Left Mouse drag | Mask Line Gesture | `paint.mask_line_gesture` | value=0.0 |

## 3D View Tool: Sculpt, Polyline Mask

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mask Polyline Gesture | `paint.mask_polyline_gesture` | value=1.0 |
| Ctrl+Left Mouse | Mask Polyline Gesture | `paint.mask_polyline_gesture` | value=0.0 |

## 3D View Tool: Sculpt, Box Hide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Hide/Show | `paint.hide_show` | action='HIDE' |
| Ctrl+Left Mouse drag | Hide/Show | `paint.hide_show` | action='SHOW' |
| Left Mouse click | Hide/Show All | `paint.hide_show_all` | action='SHOW' |

## 3D View Tool: Sculpt, Lasso Hide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Hide/Show Lasso | `paint.hide_show_lasso_gesture` | action='HIDE' |
| Ctrl+Left Mouse drag | Hide/Show Lasso | `paint.hide_show_lasso_gesture` | action='SHOW' |
| Left Mouse click | Hide/Show All | `paint.hide_show_all` | action='SHOW' |

## 3D View Tool: Sculpt, Line Hide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Hide/Show Line | `paint.hide_show_line_gesture` | action='HIDE' |
| Ctrl+Left Mouse drag | Hide/Show Line | `paint.hide_show_line_gesture` | action='SHOW' |
| Left Mouse click | Hide/Show All | `paint.hide_show_all` | action='SHOW' |

## 3D View Tool: Sculpt, Polyline Hide

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Hide/Show Polyline | `paint.hide_show_polyline_gesture` | action='HIDE' |
| Ctrl+Left Mouse | Hide/Show Polyline | `paint.hide_show_polyline_gesture` | action='SHOW' |

## 3D View Tool: Sculpt, Box Face Set

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Face Set Box Gesture | `sculpt.face_set_box_gesture` |  |

## 3D View Tool: Sculpt, Lasso Face Set

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Face Set Lasso Gesture | `sculpt.face_set_lasso_gesture` |  |

## 3D View Tool: Sculpt, Line Face Set

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Face Set Line Gesture | `sculpt.face_set_line_gesture` |  |

## 3D View Tool: Sculpt, Polyline Face Set

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Face Set Lasso Gesture | `sculpt.face_set_polyline_gesture` |  |

## 3D View Tool: Sculpt, Box Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Trim Box Gesture | `sculpt.trim_box_gesture` |  |

## 3D View Tool: Sculpt, Lasso Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Trim Lasso Gesture | `sculpt.trim_lasso_gesture` |  |

## 3D View Tool: Sculpt, Line Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Trim Line Gesture | `sculpt.trim_line_gesture` |  |

## 3D View Tool: Sculpt, Polyline Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Trim Polyline Gesture | `sculpt.trim_polyline_gesture` |  |

## 3D View Tool: Sculpt, Line Project

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Project Line Gesture | `sculpt.project_line_gesture` |  |

## 3D View Tool: Sculpt, Mesh Filter

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Filter Mesh | `sculpt.mesh_filter` |  |

## 3D View Tool: Sculpt, Cloth Filter

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Filter Cloth | `sculpt.cloth_filter` |  |

## 3D View Tool: Sculpt, Color Filter

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Filter Color | `sculpt.color_filter` |  |
| Ctrl+Left Mouse | Filter Color | `sculpt.color_filter` | use_secondary_color=True |

## 3D View Tool: Sculpt, Mask by Color

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Mask by Color | `sculpt.mask_by_color` |  |

## 3D View Tool: Sculpt, Face Set Edit

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Edit Face Set | `sculpt.face_set_edit` |  |

## 3D View Tool: Paint Weight, Sample Weight

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Weight Paint Sample Weight | `paint.weight_sample` |  |
| Left Mouse | Weight Paint Sample Weight | `grease_pencil.weight_sample` |  |

## 3D View Tool: Paint Weight, Sample Vertex Group

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Weight Paint Sample Group | `paint.weight_sample_group` |  |

## 3D View Tool: Paint Weight, Gradient

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Weight Gradient | `paint.weight_gradient` |  |

## 3D View Tool: Paint Grease Pencil, Line

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Line Shape | `grease_pencil.primitive_line` |  |
| Shift+Left Mouse | Grease Pencil Line Shape | `grease_pencil.primitive_line` |  |
| Alt+Left Mouse | Grease Pencil Line Shape | `grease_pencil.primitive_line` |  |

## 3D View Tool: Paint Grease Pencil, Polyline

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Polyline Shape | `grease_pencil.primitive_polyline` |  |
| Shift+Left Mouse | Grease Pencil Polyline Shape | `grease_pencil.primitive_polyline` |  |

## 3D View Tool: Paint Grease Pencil, Box

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Box Shape | `grease_pencil.primitive_box` |  |
| Shift+Left Mouse | Grease Pencil Box Shape | `grease_pencil.primitive_box` |  |
| Alt+Left Mouse | Grease Pencil Box Shape | `grease_pencil.primitive_box` |  |

## 3D View Tool: Paint Grease Pencil, Circle

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Circle Shape | `grease_pencil.primitive_circle` |  |
| Shift+Left Mouse | Grease Pencil Circle Shape | `grease_pencil.primitive_circle` |  |
| Alt+Left Mouse | Grease Pencil Circle Shape | `grease_pencil.primitive_circle` |  |

## 3D View Tool: Paint Grease Pencil, Arc

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Arc Shape | `grease_pencil.primitive_arc` |  |
| Shift+Left Mouse | Grease Pencil Arc Shape | `grease_pencil.primitive_arc` |  |
| Alt+Left Mouse | Grease Pencil Arc Shape | `grease_pencil.primitive_arc` |  |

## 3D View Tool: Paint Grease Pencil, Curve

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Curve Shape | `grease_pencil.primitive_curve` |  |

## 3D View Tool: Paint Grease Pencil, Trim

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Trim | `grease_pencil.stroke_trim` |  |

## 3D View Tool: Paint Grease Pencil, Interpolate

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Grease Pencil Interpolation | `grease_pencil.interpolate` | use_selection=False |

## 3D View Tool: Paint Grease Pencil, Eyedropper

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Shift+Left Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Ctrl+Left Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |
| Ctrl+Shift+Left Mouse | Grease Pencil Eyedropper | `ui.eyedropper_grease_pencil_color` |  |

## 3D View Tool: Edit Grease Pencil, Gradient

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Texture Gradient | `grease_pencil.texture_gradient` |  |

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

## 3D View Tool: Edit Grease Pencil, Interpolate

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Grease Pencil Interpolation | `grease_pencil.interpolate` | use_selection=True |

## 3D View Tool: Paint Grease Pencil, Carver

Space `VIEW_3D`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Grease Pencil Carver | `grease_pencil.stroke_carver` |  |

## Sequencer Tool: Select Box

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `sequencer.select` | deselect_all=True |
| Shift+Left Mouse | Select | `sequencer.select` | toggle=True |
| Alt+Left Mouse | Select | `sequencer.select` | deselect_all=True, ignore_connections=True |
| Shift+Alt+Left Mouse | Select | `sequencer.select` | toggle=True, ignore_connections=True |
| Shift+Right Mouse | Change Frame | `anim.change_frame` | seq_solo_preview=True, pass_through_on_strip_handles=False |
| Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True |
| Shift+Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='SUB' |

## Sequencer Tool: Select Box (fallback)

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Select | `sequencer.select` | deselect_all=True |
| Shift+Left Mouse | Select | `sequencer.select` | toggle=True |
| Alt+Left Mouse | Select | `sequencer.select` | deselect_all=True, ignore_connections=True |
| Shift+Alt+Left Mouse | Select | `sequencer.select` | toggle=True, ignore_connections=True |
| Shift+Right Mouse | Change Frame | `anim.change_frame` | seq_solo_preview=True, pass_through_on_strip_handles=False |
| Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True |
| Shift+Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `sequencer.select_box` | tweak=True, mode='SUB' |

## Preview Tool: Tweak

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse drag | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse | Select | `sequencer.select` | deselect_all=True, select_passthrough=True |
| Left Mouse click | Select | `sequencer.select` | deselect_all=True |
| Shift+Left Mouse | Select | `sequencer.select` | deselect_all=False, toggle=True |

## Preview Tool: Tweak (fallback)

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse drag | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse | Select | `sequencer.select` | deselect_all=True, select_passthrough=True |
| Shift+Left Mouse | Select | `sequencer.select` | toggle=True |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |

## Preview Tool: Select Box

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse drag | Set Cursor | `sequencer.text_cursor_set` |  |
| Left Mouse drag | Box Select | `sequencer.select_box` |  |
| Shift+Left Mouse drag | Box Select | `sequencer.select_box` | mode='ADD' |
| Ctrl+Left Mouse drag | Box Select | `sequencer.select_box` | mode='SUB' |

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
| Left Mouse drag | Circle Select | `sequencer.select_circle` | wait_for_input=False |
| Shift+Left Mouse drag | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse drag | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='SUB' |

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
| Left Mouse drag | Circle Select | `sequencer.select_circle` | wait_for_input=False |
| Shift+Left Mouse drag | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='ADD' |
| Ctrl+Left Mouse drag | Circle Select | `sequencer.select_circle` | wait_for_input=False, mode='SUB' |

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

## Sequencer Tool: Slip

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Slip Strips | `sequencer.slip` | slip_keyframes=True, use_cursor_position=True |
| Alt+Left Mouse | Slip Strips | `sequencer.slip` | slip_keyframes=True, use_cursor_position=True, ignore_connections=True |

## Preview Tool: Cursor

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Set 2D Cursor | `sequencer.cursor_set` |  |
| Left Mouse drag | Move | `transform.translate` | release_confirm=True, cursor_transform=True |

## Preview Tool: Sample

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse | Sample Color | `sequencer.sample` |  |

## Preview Tool: Move

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Move | `transform.translate` | release_confirm=True |

## Preview Tool: Rotate

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Rotate | `transform.rotate` | release_confirm=True |

## Preview Tool: Scale

Space `SEQUENCE_EDITOR`, region `WINDOW`

| Key | Action | Operator / modal item | Properties |
|---|---|---|---|
| Left Mouse drag | Resize | `transform.resize` | release_confirm=True |

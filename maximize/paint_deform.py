# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Paint Deform: Max's Freeform brushes that reshape the mesh itself, on Edit Poly.

They work on the low-poly mesh in Edit Mode, like the Conform brushes, not in Sculpt Mode:
Shift, Shift Rotate and Shift Scale (drag), Push/Pull, Relax/Soften, Flatten, Pinch/Spread,
Smudge, Noise, Exaggerate and Revert (paint). Ctrl turns Push into Pull, Pinch into Spread and
Relax into Soften's opposite. While a brush is on, right-click or Enter commits, Esc cancels the
whole session (Max's Commit / Cancel), and Revert paints the mesh back to how it was when the
brush started.

Pick locks the brushes to one object, Mirror repeats every change on the other side of the
object's own X, Y or Z, and Defaults are presets of the brush settings (Blender's preset menu).
"""

import math
import os

import bmesh
import bpy
import gpu
from bl_operators.presets import AddPresetBase
from bpy.props import BoolVectorProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty
from bpy.types import Menu, Operator, PropertyGroup
from bpy_extras import view3d_utils
from gpu_extras.batch import batch_for_shader
from mathutils import Matrix, Vector, kdtree
from mathutils.noise import noise

from .freeform import brush_weights, outside, pixel_size, ui_state

PAINT_BRUSHES = (
    ('SHIFT', "Shift", "Drag: move the mesh under the brush"),
    ('SHIFT_ROTATE', "Shift Rotate", "Drag around the brush: turn the mesh under it about its middle"),
    ('SHIFT_SCALE', "Shift Scale", "Drag right to grow, left to shrink the mesh under the brush"),
    ('PUSH_PULL', "Push/Pull", "Paint: push the surface out along its normals (Ctrl: pull it in)"),
    ('RELAX', "Relax/Soften", "Paint: even out the mesh under the brush"),
    ('FLATTEN', "Flatten", "Paint: flatten the mesh under the brush onto its average plane"),
    ('PINCH', "Pinch/Spread", "Paint: draw the vertices towards the middle of the brush (Ctrl: spread them)"),
    ('SMUDGE', "Smudge", "Paint: drag the mesh along with the stroke"),
    ('NOISE', "Noise", "Paint: roughen the surface with bumps"),
    ('EXAGGERATE', "Exaggerate", "Paint: make the shapes under the brush stronger"),
    ('REVERT', "Revert", "Paint: bring the mesh back to how it was when the brush started"),
)
_DRAGS = {'SHIFT', 'SHIFT_ROTATE', 'SHIFT_SCALE'}


class MaximizePaintDeformSettings(PropertyGroup):
    size: IntProperty(name="Size", default=60, min=2, max=1000, subtype='PIXEL',
                      description="Brush radius ([ and ] while painting)")
    strength: FloatProperty(name="Strength", default=0.3, min=0.0, max=1.0, subtype='FACTOR',
                            description="How much each step of the brush changes the mesh")
    push_value: FloatProperty(name="Push/Pull Value", default=0.1, min=0.0, soft_max=1.0, subtype='FACTOR',
                              description="Push/Pull and Noise per step, as a part of the brush's size")
    picked: PointerProperty(name="Pick", type=bpy.types.Object, poll=lambda _self, obj: obj.type == 'MESH',
                            description="Lock the brushes to this object (empty: the active object)")
    mirror: BoolVectorProperty(name="Mirror", size=3, subtype='XYZ',
                               description="Repeat every change on the other side of the object's own axis")


def settings(context):
    return context.scene.maximize_paint_deform


def _neighbour_middle(world, v):
    return sum((world @ e.other_vert(v).co for e in v.link_edges), Vector()) / len(v.link_edges)


def paint_step(obj, bm, under, mode, strength, invert=False, world_radius=1.0, push=0.1, stroke=None,
               originals=None):
    """One dab of a painting brush on `under` ([(vert, world point, world normal, weight)] from
    brush_weights). `stroke` is the world move of the brush since the last dab (Smudge);
    `originals` the local positions when the brush started (Revert). Returns how many moved."""
    world = obj.matrix_world
    inverse = world.inverted_safe()
    if not under:
        return 0
    middle = sum((p * w for _v, p, _n, w in under), Vector()) / max(sum(w for *_x, w in under), 1e-9)
    if mode == 'FLATTEN':
        # The average plane: through the weighted middle, facing the average normal.
        normal = sum((n * w for _v, _p, n, w in under), Vector())
        if normal.length_squared < 1e-12:
            return 0
        normal.normalize()
    sign = -1.0 if invert else 1.0
    moves = []
    for v, point, vnormal, w in under:
        f = strength * w
        if mode == 'PUSH_PULL':
            new = point + vnormal * (sign * push * world_radius * w)
        elif mode == 'NOISE':
            # Off the whole-number lattice, where Perlin noise is 0.
            bump = noise(point * (4.0 / max(world_radius, 1e-6)) + Vector((0.37, 0.71, 0.13)))
            new = point + vnormal * (bump * push * world_radius * w)
        elif mode in {'RELAX', 'EXAGGERATE'}:
            if not v.link_edges or v.is_boundary:
                continue
            towards = _neighbour_middle(world, v)
            if (mode == 'EXAGGERATE') != invert:
                new = point + (point - towards) * f
            else:
                new = point.lerp(towards, f)
        elif mode == 'FLATTEN':
            new = point - normal * ((point - middle).dot(normal) * f)
        elif mode == 'PINCH':
            new = point + (middle - point) * (sign * f * 0.5)
        elif mode == 'SMUDGE':
            if stroke is None:
                continue
            new = point + stroke * f
        elif mode == 'REVERT':
            if originals is None or v.index >= len(originals):
                continue
            new = point.lerp(world @ originals[v.index], f)
        else:
            continue
        moves.append((v, new))
    # All from the shape as it was, so the order doesn't matter.
    for v, new in moves:
        v.co = inverse @ new
    if moves:
        bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)
    return len(moves)


def mirror_pairs(bm, axes, tolerance=1e-4):
    """{vertex index: [(axis, index of its mirror image)]} across the local `axes` (X, Y, Z
    booleans); a vertex on the mirror plane is its own image."""
    tree = kdtree.KDTree(len(bm.verts))
    for v in bm.verts:
        tree.insert(v.co, v.index)
    tree.balance()
    pairs = {}
    for i, on in enumerate(axes):
        if not on:
            continue
        for v in bm.verts:
            image = v.co.copy()
            image[i] = -image[i]
            _co, j, dist = tree.find(image)
            if j is not None and dist <= tolerance:
                pairs.setdefault(v.index, []).append((i, j))
    return pairs


def apply_mirror(bm, pairs, moved):
    """After the brush moved the vertices `moved`, their mirror images follow. Where both sides
    were under the brush they meet halfway; a vertex on the mirror plane stays on it."""
    bm.verts.ensure_lookup_table()
    done = set()
    for v in moved:
        for axis, j in pairs.get(v.index, ()):
            if (axis, v.index) in done:
                continue
            other = bm.verts[j]
            image = v.co.copy()
            image[axis] = -image[axis]
            if j == v.index:
                v.co[axis] = 0.0
            elif other in moved:
                middle = (image + other.co) * 0.5
                other.co = middle
                middle = middle.copy()
                middle[axis] = -middle[axis]
                v.co = middle
            else:
                other.co = image
            done.add((axis, v.index))
            done.add((axis, j))


def shift(obj, grabbed, transform):
    """Shift / Shift Rotate / Shift Scale: each grabbed vertex goes to `transform(point, weight)`."""
    inverse = obj.matrix_world.inverted_safe()
    for v, point, _normal, weight in grabbed:
        v.co = inverse @ transform(point, weight)
    if grabbed:
        bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)
    return len(grabbed)


class MAXIMIZE_OT_paint_deform(Operator):
    """Paint Deform brushes (right-click or Enter commits, Esc cancels, [ and ] size the brush).
    Started in Object Mode, they edit the mesh and go back to Object Mode at the end"""
    bl_idname = "maximize.paint_deform"
    bl_label = "Paint Deform"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(name="Brush", items=PAINT_BRUSHES)

    @classmethod
    def description(cls, _context, properties):
        return next(d for k, _n, d in PAINT_BRUSHES if k == properties.mode) + \
            " (right-click or Enter commits, Esc cancels; [ and ] size the brush)"

    @classmethod
    def poll(cls, context):
        obj = context.edit_object or context.active_object
        return obj is not None and obj.type == 'MESH' and obj.mode in {'EDIT', 'OBJECT'}

    def invoke(self, context, event):
        if context.region_data is None:
            from .vocabulary import view3d_override
            override = view3d_override(context)
            if override is None:
                return {'CANCELLED'}
            with context.temp_override(**override):
                bpy.ops.maximize.paint_deform('INVOKE_DEFAULT', mode=self.mode)
            return {'FINISHED'}
        obj = context.edit_object or context.active_object
        picked = settings(context).picked
        if picked is not None and picked != obj and picked.name in context.view_layer.objects:
            # Pick: the brushes work on the picked object only.
            if obj.mode == 'EDIT':
                bpy.ops.object.mode_set(mode='OBJECT')
            context.view_layer.objects.active = picked
            picked.select_set(True)
            obj = picked
        self._back_to_object = obj.mode == 'OBJECT'
        if self._back_to_object:
            bpy.ops.object.mode_set(mode='EDIT')
        self._obj = obj
        self._bm = bmesh.from_edit_mesh(obj.data)
        self._bm.verts.ensure_lookup_table()
        self._originals = [v.co.copy() for v in self._bm.verts]
        mirror = tuple(settings(context).mirror)
        self._mirror = mirror_pairs(self._bm, mirror) if any(mirror) else None
        self._region = context.region
        self._rv3d = context.region_data
        self._settings = settings(context)
        self._painting = False
        self._mouse = None
        self._last = None
        self._grab = None
        self._moved = 0
        self._area = context.area
        self._state = ui_state(context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(self._draw, (), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        name = next(n for k, n, _d in PAINT_BRUSHES if k == self.mode)
        action = "drag" if self.mode in _DRAGS else "paint over the mesh"
        context.area.header_text_set("{}: {}; right-click or Enter commits, Esc cancels; [ ] brush size".format(
            name, action))
        return {'RUNNING_MODAL'}

    def _project(self, point):
        return view3d_utils.location_3d_to_region_2d(self._region, self._rv3d, point)

    def _view(self):
        return view3d_utils.region_2d_to_vector_3d(self._region, self._rv3d, self._mouse)

    def _under(self):
        return brush_weights(self._obj, self._bm, self._project, self._mouse, self._settings.size, self._view())

    def _world_radius(self, under):
        middle = sum((p for _v, p, _n, _w in under), Vector()) / len(under)
        return pixel_size(self._region, self._rv3d, self._mouse, middle) * self._settings.size

    def _dab(self, event):
        under = self._under()
        if not under:
            return
        s = self._settings
        stroke = None
        if self.mode == 'SMUDGE':
            if self._last is None:
                self._last = self._mouse.copy()
                return
            middle = sum((p for _v, p, _n, _w in under), Vector()) / len(under)
            a = view3d_utils.region_2d_to_location_3d(self._region, self._rv3d, self._last, middle)
            b = view3d_utils.region_2d_to_location_3d(self._region, self._rv3d, self._mouse, middle)
            stroke = b - a
            self._last = self._mouse.copy()
        self._moved += paint_step(self._obj, self._bm, under, self.mode, s.strength, event.ctrl,
                                  self._world_radius(under), s.push_value, stroke, self._originals)
        self._mirrored(under)

    def _mirrored(self, under):
        if self._mirror:
            apply_mirror(self._bm, self._mirror, {v for v, *_x in under})
            bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=False)

    def _start_drag(self):
        grabbed = self._under()
        if not grabbed:
            return
        total = sum(w for *_x, w in grabbed)
        pivot = sum((p * w for _v, p, _n, w in grabbed), Vector()) / total
        self._grab = (grabbed, self._mouse.copy(), pivot)

    def _drag(self):
        grabbed, start, pivot = self._grab
        region, rv3d = self._region, self._rv3d
        if self.mode == 'SHIFT':
            delta = view3d_utils.region_2d_to_location_3d(region, rv3d, self._mouse, pivot) - \
                view3d_utils.region_2d_to_location_3d(region, rv3d, start, pivot)

            def transform(p, w):
                return p + delta * w
        elif self.mode == 'SHIFT_ROTATE':
            centre = self._project(pivot) or start
            a, b = start - centre, self._mouse - centre
            if a.length < 1.0 or b.length < 1.0:
                return
            axis = -self._view()
            angle = -a.angle_signed(b)

            def transform(p, w):
                return pivot + Matrix.Rotation(angle * w, 3, axis) @ (p - pivot)
        else:
            factor = math.exp((self._mouse.x - start.x) / 200.0)

            def transform(p, w):
                return pivot + (p - pivot) * (1.0 + (factor - 1.0) * w)
        self._moved = shift(self._obj, grabbed, transform)
        self._mirrored(grabbed)

    def _end(self, cancel=False):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self._area.header_text_set(None)
        self._area.tag_redraw()
        if cancel and self._obj.mode == 'EDIT':
            for v in self._bm.verts:
                if v.index < len(self._originals):
                    v.co = self._originals[v.index]
            bmesh.update_edit_mesh(self._obj.data)
            self._moved = 0
        if self._back_to_object and self._obj.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'} if self._moved else {'CANCELLED'}

    def modal(self, context, event):
        self._area.tag_redraw()
        if ui_state(context) != self._state:
            # A button elsewhere changed the tool, mode or object: the brush is done.
            self._back_to_object = False
            return self._end()
        if outside(self._region, event) and not self._painting:
            # Buttons, panels, the Outliner and menus work while the brush is on.
            self._mouse = None
            return {'PASS_THROUGH'}
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'TRACKPADPAN', 'TRACKPADZOOM'} or \
                event.type.startswith('NDOF'):
            return {'PASS_THROUGH'}
        if event.type in {'MOUSEMOVE', 'LEFTMOUSE', 'INBETWEEN_MOUSEMOVE'}:
            self._mouse = Vector((event.mouse_x - self._region.x, event.mouse_y - self._region.y))
        dragging = self.mode in _DRAGS
        if event.type == 'LEFTMOUSE':
            self._painting = event.value == 'PRESS'
            self._last = None
            if self._painting:
                if dragging:
                    self._start_drag()
                else:
                    self._dab(event)
            else:
                self._grab = None
            return {'RUNNING_MODAL'}
        if event.type == 'MOUSEMOVE' and self._painting:
            if not dragging:
                self._dab(event)
            elif self._grab is not None:
                self._drag()
            return {'RUNNING_MODAL'}
        if event.value == 'PRESS' and event.type in {'LEFT_BRACKET', 'RIGHT_BRACKET'}:
            s = self._settings
            s.size = int(s.size * (0.9 if event.type == 'LEFT_BRACKET' else 1.0 / 0.9) + 0.5)
            return {'RUNNING_MODAL'}
        if event.value == 'PRESS' and event.type == 'ESC':
            return self._end(cancel=True)
        if event.value == 'PRESS' and event.type in {'RIGHTMOUSE', 'RET', 'NUMPAD_ENTER', 'SPACE'}:
            return self._end()
        return {'RUNNING_MODAL'}

    def _draw(self):
        try:
            centre = self._grab[1] if self._grab is not None else self._mouse
            radius = self._settings.size
        except ReferenceError:
            return
        if centre is None:
            return
        points = [(centre.x + radius * math.cos(a * math.tau / 48), centre.y + radius * math.sin(a * math.tau / 48))
                  for a in range(49)]
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        gpu.state.blend_set('ALPHA')
        shader.uniform_float("color", (0.3, 0.75, 1.0, 0.9))
        batch_for_shader(shader, 'LINE_STRIP', {"pos": points}).draw(shader)
        gpu.state.blend_set('NONE')


def draw(layout, context):
    """The Paint Deform rollout's contents (Edit Poly)."""
    from .ui import ToolGrid
    s = settings(context)
    grid = ToolGrid(layout)
    for mode, text, _d in PAINT_BRUSHES:
        grid.operator("maximize.paint_deform", text=text).mode = mode
    grid.pad()
    row = layout.row(align=True)
    row.menu("MAXIMIZE_MT_paint_deform_presets", text=MAXIMIZE_MT_paint_deform_presets.bl_label)
    row.operator("maximize.paint_deform_preset_add", text="", icon='ADD')
    row.operator("maximize.paint_deform_preset_add", text="", icon='REMOVE').remove_active = True
    layout.prop(s, "picked", icon='LOCKED' if s.picked else 'UNLOCKED')
    row = layout.row(align=True)
    row.label(text="Mirror")
    row.prop(s, "mirror", text="", toggle=True)
    col = layout.column(align=True)
    col.prop(s, "size")
    col.prop(s, "strength")
    col.prop(s, "push_value")
    layout.label(text="Right-click commits, Esc cancels, Ctrl inverts", icon='INFO')


PRESET_SUBDIR = "maximize/paint_deform"

# Starter presets (Max's Defaults): name -> (size, strength, push/pull value).
_STARTERS = {
    "Fine": (25, 0.15, 0.05),
    "Medium": (60, 0.3, 0.1),
    "Broad": (150, 0.5, 0.2),
}


class MAXIMIZE_MT_paint_deform_presets(Menu):
    bl_label = "Defaults"
    preset_subdir = PRESET_SUBDIR
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


class MAXIMIZE_OT_paint_deform_preset_add(AddPresetBase, Operator):
    """Save the brush settings as a preset, or remove the chosen one"""
    bl_idname = "maximize.paint_deform_preset_add"
    bl_label = "Add Paint Deform Preset"
    preset_menu = "MAXIMIZE_MT_paint_deform_presets"
    preset_defines = ["s = bpy.context.scene.maximize_paint_deform"]
    preset_values = ["s.size", "s.strength", "s.push_value"]
    preset_subdir = PRESET_SUBDIR


def write_starters():
    """The starter presets, once, into the user's preset folder."""
    folder = bpy.utils.user_resource('SCRIPTS', path=os.path.join("presets", PRESET_SUBDIR), create=True)
    if not folder or any(name.endswith(".py") for name in os.listdir(folder)):
        return
    for name, (size, strength, push) in _STARTERS.items():
        with open(os.path.join(folder, name + ".py"), "w", encoding="utf-8") as f:
            f.write("import bpy\ns = bpy.context.scene.maximize_paint_deform\n"
                    "s.size = {:d}\ns.strength = {!r}\ns.push_value = {!r}\n".format(size, strength, push))


classes = (
    MaximizePaintDeformSettings,
    MAXIMIZE_OT_paint_deform,
    MAXIMIZE_MT_paint_deform_presets,
    MAXIMIZE_OT_paint_deform_preset_add,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.maximize_paint_deform = PointerProperty(type=MaximizePaintDeformSettings)
    try:
        write_starters()
    except OSError:
        pass


def unregister():
    del bpy.types.Scene.maximize_paint_deform
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

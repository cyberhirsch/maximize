# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Transform tools: Transform Type-In, pivot tools, Align and Clone."""

import math

import bmesh
import bpy
from bpy.props import BoolVectorProperty, EnumProperty, FloatVectorProperty, IntProperty, StringProperty
from bpy.types import Operator
from bpy_extras import view3d_utils
from mathutils import Euler, Matrix, Vector


# ------------------------------------------------------------------------------
# Transform Type-In (F12)

_TOOL_MODES = {
    'builtin.rotate': 'ROTATE',
    'builtin.scale': 'SCALE',
    'builtin.scale_cage': 'SCALE',
}


def _active_tool_mode(context):
    tool = context.workspace.tools.from_space_view3d_mode(context.mode, create=False)
    return _TOOL_MODES.get(tool.idname if tool else "", 'MOVE')


def _selected_verts(context):
    obj = context.edit_object
    bm = bmesh.from_edit_mesh(obj.data)
    return obj, bm, [v for v in bm.verts if v.select]


class MAXIMIZE_OT_transform_typein(Operator):
    """Type exact values for Move, Rotate or Scale, absolute or as an offset (F12)"""
    bl_idname = "maximize.transform_typein"
    bl_label = "Transform Type-In"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(
        name="Transform",
        items=(('MOVE', "Move", ""), ('ROTATE', "Rotate", ""), ('SCALE', "Scale", "")),
    )
    absolute: FloatVectorProperty(name="Absolute: World", size=3)
    offset: FloatVectorProperty(name="Offset: World", size=3)

    @classmethod
    def poll(cls, context):
        if context.mode == 'OBJECT':
            return context.active_object is not None
        return context.mode == 'EDIT_MESH'

    def _units(self):
        return {'MOVE': "", 'ROTATE': "°", 'SCALE': "%"}[self.mode]

    def _read_absolute(self, context):
        if context.mode == 'EDIT_MESH':
            obj, _bm, verts = _selected_verts(context)
            if self.mode == 'MOVE' and verts:
                center = sum((v.co for v in verts), Vector()) / len(verts)
                return tuple(obj.matrix_world @ center)
            return (0.0, 0.0, 0.0) if self.mode != 'SCALE' else (100.0, 100.0, 100.0)
        mat = context.active_object.matrix_world
        if self.mode == 'MOVE':
            return tuple(mat.translation)
        if self.mode == 'ROTATE':
            return tuple(math.degrees(a) for a in mat.to_euler())
        return tuple(s * 100.0 for s in mat.to_scale())

    def invoke(self, context, _event):
        self.mode = _active_tool_mode(context)
        self.absolute = self._read_absolute(context)
        self.offset = (100.0, 100.0, 100.0) if self.mode == 'SCALE' else (0.0, 0.0, 0.0)
        self._start = tuple(self.absolute)
        return context.window_manager.invoke_props_dialog(self, width=420, title="{:s} Transform Type-In".format(
            self.mode.title()))

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "mode", expand=True)
        row = layout.row()
        col = row.column(align=True)
        col.label(text="Absolute: World")
        enabled = not (context.mode == 'EDIT_MESH' and self.mode != 'MOVE')
        col.enabled = enabled
        for i, axis in enumerate("XYZ"):
            col.prop(self, "absolute", index=i, text=axis + self._units())
        col = row.column(align=True)
        col.label(text="Offset: World")
        for i, axis in enumerate("XYZ"):
            col.prop(self, "offset", index=i, text=axis + self._units())

    def check(self, context):
        # Changing the mode in the dialog re-reads the values of that transform.
        if getattr(self, "_shown_mode", self.mode) != self.mode:
            self.absolute = self._read_absolute(context)
            self.offset = (100.0, 100.0, 100.0) if self.mode == 'SCALE' else (0.0, 0.0, 0.0)
            self._start = tuple(self.absolute)
        self._shown_mode = self.mode
        return True

    def _offset_is_identity(self):
        identity = 100.0 if self.mode == 'SCALE' else 0.0
        return all(abs(v - identity) < 1e-9 for v in self.offset)

    def execute(self, context):
        start = getattr(self, "_start", None) or self._read_absolute(context)
        use_offset = not self._offset_is_identity()
        if context.mode == 'EDIT_MESH':
            return self._execute_edit(context, start, use_offset)
        return self._execute_object(context, start, use_offset)

    def _execute_object(self, context, start, use_offset):
        objects = context.selected_objects or [context.active_object]
        if self.mode == 'MOVE':
            delta = Vector(self.offset) if use_offset else Vector(self.absolute) - Vector(start)
            for obj in objects:
                obj.matrix_world.translation += delta
        elif self.mode == 'ROTATE':
            if use_offset:
                rot = Euler([math.radians(a) for a in self.offset]).to_matrix().to_4x4()
                for obj in objects:
                    loc = obj.matrix_world.translation.copy()
                    obj.matrix_world = Matrix.Translation(loc) @ rot @ Matrix.Translation(-loc) @ obj.matrix_world
            else:
                for obj in objects:
                    loc, _rot, scale = obj.matrix_world.decompose()
                    rot = Euler([math.radians(a) for a in self.absolute]).to_quaternion()
                    obj.matrix_world = Matrix.LocRotScale(loc, rot, scale)
        else:
            for obj in objects:
                loc, rot, scale = obj.matrix_world.decompose()
                if use_offset:
                    scale = Vector(s * f / 100.0 for s, f in zip(scale, self.offset))
                else:
                    scale = Vector(f / 100.0 for f in self.absolute)
                obj.matrix_world = Matrix.LocRotScale(loc, rot, scale)
        return {'FINISHED'}

    def _execute_edit(self, context, start, use_offset):
        obj, bm, verts = _selected_verts(context)
        if not verts:
            return {'CANCELLED'}
        world = obj.matrix_world
        to_local = world.inverted()
        center = world @ (sum((v.co for v in verts), Vector()) / len(verts))
        if self.mode == 'MOVE':
            delta = Vector(self.offset) if use_offset else Vector(self.absolute) - Vector(start)
            mat = Matrix.Translation(delta)
        elif self.mode == 'ROTATE':
            rot = Euler([math.radians(a) for a in self.offset]).to_matrix().to_4x4()
            mat = Matrix.Translation(center) @ rot @ Matrix.Translation(-center)
        else:
            scale = Matrix.Diagonal([f / 100.0 for f in self.offset] + [1.0])
            mat = Matrix.Translation(center) @ scale @ Matrix.Translation(-center)
        for v in verts:
            v.co = to_local @ (mat @ (world @ v.co))
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Pivot (Hierarchy panel)

class MAXIMIZE_OT_affect_pivot_only(Operator):
    """Transform only the pivot (origin), not the object (Insert)"""
    bl_idname = "maximize.affect_pivot_only"
    bl_label = "Affect Pivot Only"

    def execute(self, context):
        ts = context.scene.tool_settings
        ts.use_transform_data_origin = not ts.use_transform_data_origin
        self.report({'INFO'}, "Affect Pivot Only: " + ("On" if ts.use_transform_data_origin else "Off"))
        return {'FINISHED'}


class MAXIMIZE_OT_center_pivot(Operator):
    """Move the pivot to the center of the object's bounding box"""
    bl_idname = "maximize.center_pivot"
    bl_label = "Center to Object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects)

    def execute(self, _context):
        return bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')


class MAXIMIZE_OT_align_pivot_world(Operator):
    """Align the pivot to the world axes without moving the geometry"""
    bl_idname = "maximize.align_pivot_world"
    bl_label = "Align to World"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects)

    def execute(self, _context):
        return bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)


class MAXIMIZE_OT_reset_xform(Operator):
    """Reset XForm: bake rotation and scale into the mesh, so the object has a clean transform"""
    bl_idname = "maximize.reset_xform"
    bl_label = "Reset XForm"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects)

    def execute(self, context):
        # Instances share data, which transform_apply refuses; make them unique first, as Max does.
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=False, obdata=True)
        return bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


# ------------------------------------------------------------------------------
# Align (Alt+A)

POINTS = (
    ('MIN', "Minimum", "Lowest point of the bounding box on that axis"),
    ('CENTER', "Center", "Center of the bounding box"),
    ('PIVOT', "Pivot Point", "The object's pivot (origin)"),
    ('MAX', "Maximum", "Highest point of the bounding box on that axis"),
)


def _world_bounds(obj, depsgraph):
    eval_obj = obj.evaluated_get(depsgraph)
    corners = [eval_obj.matrix_world @ Vector(c) for c in eval_obj.bound_box]
    if not corners or obj.type == 'EMPTY':
        loc = obj.matrix_world.translation
        return loc.copy(), loc.copy()
    lo = Vector(min(c[i] for c in corners) for i in range(3))
    hi = Vector(max(c[i] for c in corners) for i in range(3))
    return lo, hi


def _point(obj, depsgraph, kind, axis):
    if kind == 'PIVOT':
        return obj.matrix_world.translation[axis]
    lo, hi = _world_bounds(obj, depsgraph)
    if kind == 'MIN':
        return lo[axis]
    if kind == 'MAX':
        return hi[axis]
    return (lo[axis] + hi[axis]) * 0.5


class MAXIMIZE_OT_align_apply(Operator):
    """Align the selection to the target object"""
    bl_idname = "maximize.align_apply"
    bl_label = "Align Selection"
    bl_options = {'REGISTER', 'UNDO'}

    target: StringProperty(name="Target Object")
    position: BoolVectorProperty(name="Position", size=3, default=(True, True, True))
    current_point: EnumProperty(name="Current Object", items=POINTS, default='CENTER')
    target_point: EnumProperty(name="Target Object", items=POINTS, default='CENTER')
    orientation: BoolVectorProperty(name="Align Orientation (Local)", size=3, default=(False, False, False))
    match_scale: BoolVectorProperty(name="Match Scale", size=3, default=(False, False, False))

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def invoke(self, context, _event):
        return context.window_manager.invoke_props_dialog(
            self, width=380, title="Align Selection ({:s})".format(self.target))

    def draw(self, _context):
        layout = self.layout
        layout.label(text="Align Position (World):")
        layout.row().prop(self, "position", text="", toggle=True)
        row = layout.row()
        row.column().prop(self, "current_point", expand=True)
        row.column().prop(self, "target_point", expand=True)
        layout.label(text="Align Orientation (Local):")
        layout.row().prop(self, "orientation", text="", toggle=True)
        layout.label(text="Match Scale:")
        layout.row().prop(self, "match_scale", text="", toggle=True)

    def execute(self, context):
        target = bpy.data.objects.get(self.target)
        if target is None:
            self.report({'ERROR'}, "No align target")
            return {'CANCELLED'}
        depsgraph = context.evaluated_depsgraph_get()
        objects = [o for o in context.selected_objects if o != target]
        if not objects:
            self.report({'ERROR'}, "Select the objects to align, other than the target")
            return {'CANCELLED'}
        t_loc, t_rot, t_scale = target.matrix_world.decompose()
        t_euler = t_rot.to_euler()
        for obj in objects:
            delta = Vector()
            for axis in range(3):
                if self.position[axis]:
                    delta[axis] = (_point(target, depsgraph, self.target_point, axis)
                                   - _point(obj, depsgraph, self.current_point, axis))
            loc, rot, scale = obj.matrix_world.decompose()
            euler = rot.to_euler()
            for axis in range(3):
                if self.orientation[axis]:
                    euler[axis] = t_euler[axis]
                if self.match_scale[axis]:
                    scale[axis] = t_scale[axis]
            obj.matrix_world = Matrix.LocRotScale(loc + delta, euler, scale)
        return {'FINISHED'}


class MAXIMIZE_OT_align(Operator):
    """Align the selection to a target: pick the target object in the viewport (Alt+A)"""
    bl_idname = "maximize.align"
    bl_label = "Align"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT' and bool(context.selected_objects) and
                context.area is not None and context.area.type == 'VIEW_3D')

    def invoke(self, context, _event):
        context.window_manager.modal_handler_add(self)
        context.workspace.status_text_set("Align: pick the target object (Esc / Right-click to cancel)")
        context.window.cursor_modal_set('EYEDROPPER')
        return {'RUNNING_MODAL'}

    def _finish(self, context):
        context.workspace.status_text_set(None)
        context.window.cursor_modal_restore()

    def modal(self, context, event):
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            self._finish(context)
            return {'CANCELLED'}
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            target = self._pick(context, event)
            if target is None:
                return {'RUNNING_MODAL'}
            self._finish(context)
            bpy.ops.maximize.align_apply('INVOKE_DEFAULT', target=target.name)
            return {'FINISHED'}
        return {'PASS_THROUGH'} if event.type in {
            'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'WHEELINMOUSE', 'WHEELOUTMOUSE'} else {'RUNNING_MODAL'}

    def _pick(self, context, event):
        for region in context.area.regions:
            if region.type != 'WINDOW':
                continue
            x, y = event.mouse_x - region.x, event.mouse_y - region.y
            if not (0 <= x < region.width and 0 <= y < region.height):
                continue
            rv3d = region.data
            origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, (x, y))
            direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, (x, y))
            hit, _loc, _normal, _index, obj, _matrix = context.scene.ray_cast(
                context.evaluated_depsgraph_get(), origin, direction)
            if hit and obj is not None:
                return obj.original
        return None


# ------------------------------------------------------------------------------
# Clone (Ctrl+V and Shift+drag)

CLONE_TYPES = (
    ('COPY', "Copy", "Independent copy"),
    ('INSTANCE', "Instance", "Shares the mesh and the modifier stack with the original: editing the mesh or "
     "the original's modifiers changes all. Modifiers added to an instance stay on it"),
    ('REFERENCE', "Reference", "Shares the original's mesh and modifier stack; modifiers you add to the "
     "reference stay on the reference"),
)

SHARED_GROUP = "MX Shared Stack"
SHARED_MODIFIER = "Shared Stack"


def _shared_group():
    from .nodes import GroupBuilder, find_group
    group = find_group(SHARED_GROUP)
    if group is not None:
        return group
    g = GroupBuilder(SHARED_GROUP, "shared_stack")
    g.input("Geometry", 'NodeSocketGeometry')
    source = g.input("Original", 'NodeSocketObject')
    out = g.output()
    info = g.node('GeometryNodeObjectInfo', {"Object": source}, transform_space='ORIGINAL')
    g.set(out, info.outputs["Geometry"])
    return g.tree


def shared_stack(obj):
    """The modifier through which an instance or reference gets its original's stack, or None."""
    mod = obj.modifiers.get(SHARED_MODIFIER) if obj is not None else None
    if mod is not None and mod.type == 'NODES' and mod.node_group is not None and             mod.node_group.get("maximize_kind") == "shared_stack":
        return mod
    return None


def _share_stack(new, original):
    """Give `new` the original's modifier stack: its own modifiers go, a Shared Stack modifier
    brings in the original's evaluated mesh (the mesh itself is shared too)."""
    from .nodes import modifier_input
    if shared_stack(original) is not None:
        # Cloning an instance: share the same original.
        return
    new.modifiers.clear()
    mod = new.modifiers.new(SHARED_MODIFIER, 'NODES')
    mod.node_group = _shared_group()
    modifier_input(mod, "Original").value = original


def _clone(context, objects, clone_type, offset):
    """Clone objects; each new copy is offset from the previous one."""
    linked = clone_type != 'COPY'
    clones = []
    for obj in objects:
        new = obj.copy()
        if obj.data is not None and not linked:
            new.data = obj.data.copy()
        for coll in obj.users_collection:
            coll.objects.link(new)
        new.matrix_world = Matrix.Translation(offset) @ obj.matrix_world
        if linked and obj.type == 'MESH':
            # Max instances share the modifier stack too, including modifiers added later.
            _share_stack(new, obj)
        clones.append(new)
    return clones


class MAXIMIZE_OT_make_unique(Operator):
    """Make Unique: turn instances and references into independent copies with their own mesh and
    their own copy of the modifier stack"""
    bl_idname = "maximize.make_unique"
    bl_label = "Make Unique"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects

    def execute(self, context):
        from .nodes import modifier_input
        targets = list(context.selected_objects)
        active = context.view_layer.objects.active
        for obj in targets:
            if obj.data is not None and obj.data.users > 1:
                obj.data = obj.data.copy()
            mod = shared_stack(obj)
            if mod is None:
                continue
            original = modifier_input(mod, "Original").value
            obj.modifiers.remove(mod)
            if original is None:
                continue
            # Copy the original's modifiers below the object's own ones.
            for o in context.selected_objects:
                o.select_set(False)
            obj.select_set(True)
            context.view_layer.objects.active = original
            for index, om in enumerate(original.modifiers):
                with context.temp_override(object=original, active_object=original, selected_objects=[obj],
                                           selected_editable_objects=[obj]):
                    bpy.ops.object.modifier_copy_to_selected(modifier=om.name)
                copied = obj.modifiers[-1]
                with context.temp_override(object=obj, active_object=obj):
                    bpy.ops.object.modifier_move_to_index(modifier=copied.name, index=index)
        for o in targets:
            o.select_set(True)
        context.view_layer.objects.active = active
        return {'FINISHED'}


class MAXIMIZE_OT_clone(Operator):
    """Clone the selection in place as copies, instances or references (Ctrl+V)"""
    bl_idname = "maximize.clone"
    bl_label = "Clone Options"
    bl_options = {'REGISTER', 'UNDO'}

    clone_type: EnumProperty(name="Object", items=CLONE_TYPES)
    copies: IntProperty(name="Number of Copies", default=1, min=1, max=10000)
    offset: FloatVectorProperty(name="Offset", subtype='TRANSLATION', options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects)

    def invoke(self, context, _event):
        self.offset = (0.0, 0.0, 0.0)
        return context.window_manager.invoke_props_dialog(self, width=260)

    def draw(self, _context):
        layout = self.layout
        layout.prop(self, "clone_type", expand=True)
        layout.prop(self, "copies")

    def execute(self, context):
        sources = list(context.selected_objects)
        active = context.view_layer.objects.active
        current = sources
        for _ in range(self.copies):
            current = _clone(context, current, self.clone_type, Vector(self.offset))
        for obj in sources:
            obj.select_set(False)
        for obj in current:
            obj.select_set(True)
        if active in sources:
            context.view_layer.objects.active = current[sources.index(active)]
        return {'FINISHED'}


class MAXIMIZE_OT_clone_finish(Operator):
    """Choose how the clones made by Shift+drag relate to the original"""
    bl_idname = "maximize.clone_finish"
    bl_label = "Clone Options"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    clone_type: EnumProperty(name="Object", items=CLONE_TYPES)
    copies: IntProperty(name="Number of Copies", default=1, min=1, max=10000)
    pairs: StringProperty(options={'HIDDEN'})

    def invoke(self, context, _event):
        return context.window_manager.invoke_props_dialog(self, width=260)

    def draw(self, _context):
        layout = self.layout
        layout.prop(self, "clone_type", expand=True)
        layout.prop(self, "copies")

    def execute(self, context):
        pairs = [p.split("\t") for p in self.pairs.split("\n") if "\t" in p]
        pairs = [(bpy.data.objects.get(a), bpy.data.objects.get(b)) for a, b in pairs]
        pairs = [(a, b) for a, b in pairs if a is not None and b is not None]
        if not pairs:
            return {'CANCELLED'}
        if self.clone_type != 'COPY':
            for orig, dup in pairs:
                if orig.data is not None and dup.data is not orig.data:
                    old = dup.data
                    dup.data = orig.data
                    if old.users == 0:
                        bpy.data.batch_remove([old])
        # Each further copy repeats the move, rotation or scale of the drag, as Max does.
        orig, dup = pairs[0]
        step = dup.matrix_world @ orig.matrix_world.inverted()
        current = [dup for _orig, dup in pairs]
        for _ in range(self.copies - 1):
            previous = current
            current = _clone(context, previous, self.clone_type, Vector())
            for prev, obj in zip(previous, current):
                obj.matrix_world = step @ prev.matrix_world
                prev.select_set(False)
                obj.select_set(True)
        context.view_layer.objects.active = current[-1]
        return {'FINISHED'}


_pending_clone = None
_MODAL_PREFIXES = ("TRANSFORM_OT_", "GIZMOGROUP_OT_")


def _start_clone(context):
    """Duplicate the selection; the clones become the selection. Returns False on failure."""
    global _pending_clone
    sources = list(context.selected_objects)
    bpy.ops.object.duplicate(linked=False)
    clones = list(context.selected_objects)
    if len(clones) != len(sources):
        return False
    # object.duplicate keeps the selection order of the sources.
    _pending_clone = (context.window, context.area, list(zip(sources, clones)), 0)
    bpy.app.timers.register(_watch_clone_drag, first_interval=0.05)
    return True


def _watch_clone_drag():
    """Timer: once the drag that moves the clones is done, show the Clone Options dialog."""
    global _pending_clone
    if _pending_clone is None:
        return None
    window, area, pairs, ticks = _pending_clone
    try:
        running = any(op.bl_idname.startswith(_MODAL_PREFIXES) for op in window.modal_operators)
    except ReferenceError:
        _pending_clone = None
        return None
    if running or ticks < 2:
        # Give a gizmo drag a moment to start before deciding that nothing happens.
        _pending_clone = (window, area, pairs, ticks + 1)
        return 0.05
    _pending_clone = None
    pairs = [(a, b) for a, b in pairs if a.name in bpy.data.objects and b.name in bpy.data.objects]
    if not pairs:
        return None
    a, b = pairs[0][0].matrix_world, pairs[0][1].matrix_world
    moved = any(abs(a[i][j] - b[i][j]) > 1e-6 for i in range(4) for j in range(4))
    if not moved:
        # The drag was cancelled: drop the clones, as Max does.
        for _orig, dup in pairs:
            bpy.data.objects.remove(dup)
        for orig, _dup in pairs:
            orig.select_set(True)
        return None
    region = next((r for r in area.regions if r.type == 'WINDOW'), None)
    with bpy.context.temp_override(window=window, area=area, region=region):
        bpy.ops.maximize.clone_finish(
            'INVOKE_DEFAULT', pairs="\n".join("{:s}\t{:s}".format(a.name, b.name) for a, b in pairs))
    return None


class MAXIMIZE_OT_clone_drag(Operator):
    """Shift+drag: clone the selection and move the clones, then choose the clone options"""
    bl_idname = "maximize.clone_drag"
    bl_label = "Clone and Move"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects) and context.area is not None

    def invoke(self, context, _event):
        if not _start_clone(context):
            return {'CANCELLED'}
        bpy.ops.transform.translate('INVOKE_DEFAULT', release_confirm=True)
        return {'FINISHED'}


class MAXIMIZE_OT_clone_gizmo(Operator):
    """Shift+drag on a transform gizmo: clone the selection, then let the gizmo drag the clones"""
    bl_idname = "maximize.clone_gizmo"
    bl_label = "Clone with Gizmo"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects) and context.area is not None

    def invoke(self, context, _event):
        _start_clone(context)
        # Pass the event on: the next keymap item starts the gizmo drag on the clones.
        return {'PASS_THROUGH'}


classes = (
    MAXIMIZE_OT_make_unique,
    MAXIMIZE_OT_transform_typein,
    MAXIMIZE_OT_affect_pivot_only,
    MAXIMIZE_OT_center_pivot,
    MAXIMIZE_OT_align_pivot_world,
    MAXIMIZE_OT_reset_xform,
    MAXIMIZE_OT_align_apply,
    MAXIMIZE_OT_align,
    MAXIMIZE_OT_clone,
    MAXIMIZE_OT_clone_finish,
    MAXIMIZE_OT_clone_drag,
    MAXIMIZE_OT_clone_gizmo,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    global _pending_clone
    _pending_clone = None
    if bpy.app.timers.is_registered(_watch_clone_drag):
        bpy.app.timers.unregister(_watch_clone_drag)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Selection: sub-object levels, Select by Name, named selection sets and Edit Poly helpers."""

import bmesh
import bpy
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import Operator, PropertyGroup, UIList


# ------------------------------------------------------------------------------
# Sub-object levels

LEVELS = (
    ('OBJECT', "Object", "Top level"),
    ('VERTEX', "Vertex", "Vertex sub-object level (1)"),
    ('EDGE', "Edge", "Edge sub-object level (2)"),
    ('BORDER', "Border", "Border sub-object level: open edge loops (3)"),
    ('POLYGON', "Polygon", "Polygon sub-object level (4)"),
    ('ELEMENT', "Element", "Element sub-object level: connected polygons (5)"),
)
_SELECT_MODE = {'VERTEX': 'VERT', 'EDGE': 'EDGE', 'BORDER': 'EDGE', 'POLYGON': 'FACE', 'ELEMENT': 'FACE'}


def current_level(context):
    if context.mode != 'EDIT_MESH':
        return 'OBJECT'
    mode = context.tool_settings.mesh_select_mode
    level = 'VERTEX' if mode[0] else 'EDGE' if mode[1] else 'POLYGON'
    # Border and Element share a select mode with Edge and Polygon; remember which one was chosen.
    stored = context.scene.get("maximize_level")
    if stored in _SELECT_MODE and _SELECT_MODE[stored] == _SELECT_MODE[level]:
        return stored
    return level


class MAXIMIZE_OT_subobject(Operator):
    """Go to a sub-object level; pressing the key of the current level returns to the object"""
    bl_idname = "maximize.subobject"
    bl_label = "Sub-Object Level"
    bl_options = {'REGISTER', 'UNDO'}

    level: EnumProperty(name="Level", items=LEVELS)

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and context.mode in {'OBJECT', 'EDIT_MESH'}

    def execute(self, context):
        if self.level == 'OBJECT' or (context.mode == 'EDIT_MESH' and current_level(context) == self.level):
            bpy.ops.object.mode_set(mode='OBJECT')
            context.scene["maximize_level"] = 'OBJECT'
            return {'FINISHED'}
        if context.mode != 'EDIT_MESH':
            from .primitives import primitive_modifier
            if primitive_modifier(context.active_object) is not None:
                # Sub-object levels need an editable mesh, as in Max.
                bpy.ops.object.convert(target='MESH')
                self.report({'INFO'}, "Converted to Editable Poly")
            bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type=_SELECT_MODE[self.level])
        context.scene["maximize_level"] = self.level
        if self.level == 'BORDER' and _has_selected_faces(context):
            bpy.ops.mesh.region_to_loop()
        elif self.level == 'ELEMENT' and _has_selected_faces(context):
            bpy.ops.mesh.select_linked(delimit=set())
        _redraw_headers(context)
        return {'FINISHED'}


def _redraw_headers(context):
    # Edge -> Border keeps Blender's select mode, so nothing else redraws the level buttons.
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def _has_selected_faces(context):
    bm = bmesh.from_edit_mesh(context.edit_object.data)
    return any(f.select for f in bm.faces)


class MAXIMIZE_OT_subobject_pick(Operator):
    """Click selection at the Border and Element levels: a whole open border, or a whole element"""
    bl_idname = "maximize.subobject_pick"
    bl_label = "Pick Border / Element"
    bl_options = {'REGISTER', 'UNDO'}

    extend: BoolProperty(name="Extend", description="Add to the selection")
    deselect: BoolProperty(name="Deselect", description="Remove from the selection")

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def invoke(self, context, _event):
        level = current_level(context)
        if level == 'ELEMENT':
            if not (self.extend or self.deselect):
                bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_linked_pick('INVOKE_DEFAULT', deselect=self.deselect, delimit=set())
            return {'FINISHED'}
        if level == 'BORDER':
            self._pick_border(context)
            return {'FINISHED'}
        # Other levels: leave the click to the normal selection.
        return {'PASS_THROUGH'}

    def _pick_border(self, context):
        mesh = context.edit_object.data
        bm = bmesh.from_edit_mesh(mesh)
        before = {e.index for e in bm.edges if e.select}
        # On an open edge, a loop selection follows the border.
        bpy.ops.mesh.loop_select('INVOKE_DEFAULT', extend=self.extend, deselect=self.deselect)
        bm = bmesh.from_edit_mesh(mesh)
        bm.edges.ensure_lookup_table()
        if self.deselect:
            return
        # Max only picks borders: drop new edges that have faces on both sides.
        for edge in bm.edges:
            if edge.select and edge.index not in before and len(edge.link_faces) != 1:
                edge.select = False
        for vert in bm.verts:
            vert.select = any(e.select for e in vert.link_edges)
        bm.select_flush_mode()
        bmesh.update_edit_mesh(mesh, loop_triangles=False, destructive=False)


class MAXIMIZE_OT_attach_edit(Operator):
    """Attach the other selected objects to the object being edited (Alt+Shift+D)"""
    bl_idname = "maximize.attach_edit"
    bl_label = "Attach"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and len(context.selected_objects) > 1

    def execute(self, context):
        # Joining needs Object Mode; come back to the same sub-object level.
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


class MAXIMIZE_OT_delete_subobject(Operator):
    """Delete the selected sub-objects at the current level (Delete)"""
    bl_idname = "maximize.delete_subobject"
    bl_label = "Delete Sub-Objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        mode = context.tool_settings.mesh_select_mode
        bpy.ops.mesh.delete(type='VERT' if mode[0] else 'EDGE' if mode[1] else 'FACE')
        return {'FINISHED'}


class MAXIMIZE_OT_chamfer(Operator):
    """Chamfer the selected vertices or edges (Ctrl+Shift+C)"""
    bl_idname = "maximize.chamfer"
    bl_label = "Chamfer"

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def invoke(self, context, _event):
        affect = 'VERTICES' if context.tool_settings.mesh_select_mode[0] else 'EDGES'
        bpy.ops.mesh.bevel('INVOKE_DEFAULT', affect=affect)
        return {'FINISHED'}


class MAXIMIZE_OT_connect(Operator):
    """Connect: new edges between selected vertices, or across selected edges (Ctrl+Shift+E)"""
    bl_idname = "maximize.connect"
    bl_label = "Connect"
    bl_options = {'REGISTER', 'UNDO'}

    segments: IntProperty(name="Segments", default=1, min=1, max=100)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        if context.tool_settings.mesh_select_mode[0]:
            result = bpy.ops.mesh.vert_connect_path()
        else:
            bm = bmesh.from_edit_mesh(context.edit_object.data)
            if sum(1 for e in bm.edges if e.select) >= 2:
                result = bpy.ops.mesh.subdivide_edgering(number_cuts=self.segments)
            else:
                result = bpy.ops.mesh.subdivide(number_cuts=self.segments)
        return {'FINISHED'} if 'FINISHED' in result else {'CANCELLED'}


# ------------------------------------------------------------------------------
# Select by Name (H)

class MaximizeNameItem(PropertyGroup):
    name: StringProperty()
    select: BoolProperty(name="Select")
    icon: StringProperty()


class MAXIMIZE_UL_names(UIList):
    def draw_item(self, _context, layout, _data, item, _icon, _active_data, _active_propname, _index):
        row = layout.row(align=True)
        row.prop(item, "select", text="")
        row.label(text=item.name, icon=item.icon)


_OBJECT_ICONS = {
    'MESH': 'OUTLINER_OB_MESH', 'CURVE': 'OUTLINER_OB_CURVE', 'CAMERA': 'OUTLINER_OB_CAMERA',
    'LIGHT': 'OUTLINER_OB_LIGHT', 'EMPTY': 'OUTLINER_OB_EMPTY', 'ARMATURE': 'OUTLINER_OB_ARMATURE',
}


class MAXIMIZE_OT_select_by_name(Operator):
    """Select objects from a filterable list (H)"""
    bl_idname = "maximize.select_by_name"
    bl_label = "Select From Scene"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.view_layer is not None

    def invoke(self, context, _event):
        wm = context.window_manager
        wm.maximize_names.clear()
        for obj in sorted(context.view_layer.objects, key=lambda o: o.name.lower()):
            if not obj.visible_get():
                continue
            item = wm.maximize_names.add()
            item.name = obj.name
            item.select = obj.select_get()
            item.icon = _OBJECT_ICONS.get(obj.type, 'OBJECT_DATA')
        return wm.invoke_props_dialog(self, width=360, confirm_text="Select")

    def draw(self, context):
        wm = context.window_manager
        self.layout.template_list(
            "MAXIMIZE_UL_names", "", wm, "maximize_names", wm, "maximize_names_index", rows=14)

    def execute(self, context):
        names = {item.name for item in context.window_manager.maximize_names if item.select}
        active = None
        for obj in context.view_layer.objects:
            selected = obj.name in names
            obj.select_set(selected)
            if selected and active is None:
                active = obj
        if active is not None:
            context.view_layer.objects.active = active
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Named selection sets

SUB_PREFIX = "nss_"


class MaximizeSetObject(PropertyGroup):
    object: PointerProperty(type=bpy.types.Object)


class MaximizeSelectionSet(PropertyGroup):
    name: StringProperty(name="Name")
    objects: CollectionProperty(type=MaximizeSetObject)


def _sub_domain(context):
    mode = context.tool_settings.mesh_select_mode
    return 'VERT' if mode[0] else 'EDGE' if mode[1] else 'FACE'


def _bm_seq(bm, domain):
    return {'VERT': bm.verts, 'EDGE': bm.edges, 'FACE': bm.faces}[domain]


def sub_set_names(context):
    """Named sub-object sets of the edit mesh, as (attribute name, label, domain)."""
    obj = context.edit_object
    if obj is None or obj.type != 'MESH':
        return []
    domains = {'POINT': 'VERT', 'EDGE': 'EDGE', 'FACE': 'FACE'}
    return [(a.name, a.name[len(SUB_PREFIX):], domains[a.domain]) for a in obj.data.attributes
            if a.name.startswith(SUB_PREFIX) and a.domain in domains]


class MAXIMIZE_OT_selset_create(Operator):
    """Store the current selection as a named selection set"""
    bl_idname = "maximize.selset_create"
    bl_label = "Create Selection Set"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty(name="Name", default="Set")

    @classmethod
    def poll(cls, context):
        return context.mode in {'OBJECT', 'EDIT_MESH'}

    def invoke(self, context, _event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            obj = context.edit_object
            bm = bmesh.from_edit_mesh(obj.data)
            domain = _sub_domain(context)
            seq = _bm_seq(bm, domain)
            attr = SUB_PREFIX + self.name
            for other_seq in (bm.verts, bm.edges, bm.faces):
                old = other_seq.layers.int.get(attr)
                if old is not None:
                    other_seq.layers.int.remove(old)
            layer = seq.layers.int.new(attr)
            for elem in seq:
                elem[layer] = int(elem.select)
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
            return {'FINISHED'}
        sets = context.scene.maximize_sets
        sel_set = next((s for s in sets if s.name == self.name), None) or sets.add()
        sel_set.name = self.name
        sel_set.objects.clear()
        for obj in context.selected_objects:
            sel_set.objects.add().object = obj
        context.scene.maximize_sets_index = list(sets).index(sel_set)
        return {'FINISHED'}


class MAXIMIZE_OT_selset_select(Operator):
    """Select the contents of a named selection set"""
    bl_idname = "maximize.selset_select"
    bl_label = "Select Set"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty(name="Name")
    extend: BoolProperty(name="Extend", description="Add to the current selection")

    def invoke(self, context, event):
        self.extend = event.ctrl
        return self.execute(context)

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            obj = context.edit_object
            bm = bmesh.from_edit_mesh(obj.data)
            for attr, label, domain in sub_set_names(context):
                if label != self.name:
                    continue
                bpy.ops.mesh.select_mode(type=domain)
                seq = _bm_seq(bm, domain)
                layer = seq.layers.int.get(attr)
                for elem in seq:
                    if elem[layer]:
                        elem.select_set(True)
                    elif not self.extend:
                        elem.select_set(False)
                bm.select_flush_mode()
                bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
                return {'FINISHED'}
            return {'CANCELLED'}
        sel_set = context.scene.maximize_sets.get(self.name)
        if sel_set is None:
            return {'CANCELLED'}
        if not self.extend:
            for obj in context.view_layer.objects:
                obj.select_set(False)
        last = None
        for item in sel_set.objects:
            obj = item.object
            if obj is not None and obj.name in context.view_layer.objects:
                obj.select_set(True)
                last = obj
        if last is not None:
            context.view_layer.objects.active = last
        return {'FINISHED'}


class MAXIMIZE_OT_selset_remove(Operator):
    """Delete a named selection set (the objects stay)"""
    bl_idname = "maximize.selset_remove"
    bl_label = "Remove Selection Set"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty(name="Name")

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            obj = context.edit_object
            bm = bmesh.from_edit_mesh(obj.data)
            attr = SUB_PREFIX + self.name
            for seq in (bm.verts, bm.edges, bm.faces):
                layer = seq.layers.int.get(attr)
                if layer is not None:
                    seq.layers.int.remove(layer)
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
            return {'FINISHED'}
        sets = context.scene.maximize_sets
        index = sets.find(self.name)
        if index < 0:
            return {'CANCELLED'}
        sets.remove(index)
        context.scene.maximize_sets_index = min(index, len(sets) - 1)
        return {'FINISHED'}


class MAXIMIZE_MT_selection_sets(bpy.types.Menu):
    bl_label = "Named Selection Sets"

    def draw(self, context):
        layout = self.layout
        if context.mode == 'EDIT_MESH':
            names = [label for _attr, label, _domain in sub_set_names(context)]
        else:
            names = [s.name for s in context.scene.maximize_sets]
        for name in names:
            layout.operator("maximize.selset_select", text=name).name = name
        if names:
            layout.separator()
        layout.operator("maximize.selset_create", text="Create Selection Set...", icon='ADD')


classes = (
    MAXIMIZE_OT_subobject,
    MAXIMIZE_OT_subobject_pick,
    MAXIMIZE_OT_attach_edit,
    MAXIMIZE_OT_delete_subobject,
    MAXIMIZE_OT_chamfer,
    MAXIMIZE_OT_connect,
    MaximizeNameItem,
    MAXIMIZE_UL_names,
    MAXIMIZE_OT_select_by_name,
    MaximizeSetObject,
    MaximizeSelectionSet,
    MAXIMIZE_OT_selset_create,
    MAXIMIZE_OT_selset_select,
    MAXIMIZE_OT_selset_remove,
    MAXIMIZE_MT_selection_sets,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    wm = bpy.types.WindowManager
    wm.maximize_names = CollectionProperty(type=MaximizeNameItem)
    wm.maximize_names_index = IntProperty()
    bpy.types.Scene.maximize_sets = CollectionProperty(type=MaximizeSelectionSet)
    bpy.types.Scene.maximize_sets_index = IntProperty()


def unregister():
    del bpy.types.Scene.maximize_sets_index
    del bpy.types.Scene.maximize_sets
    del bpy.types.WindowManager.maximize_names_index
    del bpy.types.WindowManager.maximize_names
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Edit Poly as a modifier (prototype): edit a mesh in the middle of its modifier stack.

The modifier is a Geometry Nodes group with two hidden helper objects:

- **Base**: the mesh that came into the modifier when you last edited it.
- **Edited**: your edited version of it. Its integer point attribute `mx_orig` says which base
  vertex each vertex came from (new vertices copy it from the vertex they were made from).

While the topology below stays the same, the modifier outputs the edited mesh and moves each
vertex by how far its base vertex has moved since (index-based, as Max does). When the topology
below changes, the edits are kept as they were and the panel warns.

Editing (1–5 on an object whose active modifier is Edit Poly) re-bases first: Base becomes the
current input and Edited the current result, then you edit Edited in place of the object.
"""

import bmesh
import bpy
import numpy as np
from bpy.app.handlers import persistent
from bpy.types import Operator, Panel

from .nodes import GroupBuilder, find_group, modifier_input

GROUP = "MX Edit Poly"
ORIG = "mx_orig"
CHANGED = "mx_topology_changed"
TAG = "maximize_edit_poly"


def build_group():
    group = find_group(GROUP)
    if group is not None:
        return group
    old = bpy.data.node_groups.get(GROUP)
    if old is not None:
        old.name = GROUP + " (old)"
    g = GroupBuilder(GROUP, "edit_poly")
    geometry = g.input("Geometry", 'NodeSocketGeometry')
    base_ob = g.input("Base", 'NodeSocketObject')
    edited_ob = g.input("Edited", 'NodeSocketObject')
    out = g.output()

    base = g.node('GeometryNodeObjectInfo', {"Object": base_ob}, transform_space='ORIGINAL').outputs["Geometry"]
    edited = g.node('GeometryNodeObjectInfo', {"Object": edited_ob}, transform_space='ORIGINAL').outputs["Geometry"]

    def points(geo):
        return g.node('GeometryNodeAttributeDomainSize', {"Geometry": geo}, component='MESH').outputs["Point Count"]

    same_topology = g.node('FunctionNodeCompare', {"A": points(geometry), "B": points(base), "Epsilon": 0.5},
                           data_type='FLOAT', operation='EQUAL').outputs["Result"]
    orig = g.node('GeometryNodeInputNamedAttribute', {"Name": ORIG}, data_type='INT').outputs["Attribute"]
    mapped = g.node('FunctionNodeCompare', {"A": orig, "B": 0.0},
                    data_type='FLOAT', operation='GREATER_EQUAL').outputs["Result"]
    use = g.node('FunctionNodeBooleanMath', {0: same_topology, 1: mapped}, operation='AND').outputs[0]
    position = g.node('GeometryNodeInputPosition').outputs[0]

    def sample(geo):
        return g.node('GeometryNodeSampleIndex', {"Geometry": geo, "Value": position, "Index": orig},
                      data_type='FLOAT_VECTOR', domain='POINT').outputs[0]

    offset = g.vmath('SUBTRACT', sample(geometry), sample(base))
    offset = g.node('GeometryNodeSwitch', {"Switch": use, "True": offset}, input_type='VECTOR').outputs[0]
    moved = g.node('GeometryNodeSetPosition', {"Geometry": edited, "Offset": offset}).outputs[0]
    # For the panel's warning.
    changed = g.node('FunctionNodeBooleanMath', {0: same_topology}, operation='NOT').outputs[0]
    moved = g.node('GeometryNodeStoreNamedAttribute', {"Geometry": moved, "Name": CHANGED, "Value": changed},
                   data_type='BOOLEAN', domain='POINT').outputs[0]
    g.set(out, moved)
    return g.tree


def is_edit_poly(mod):
    return mod is not None and mod.type == 'NODES' and mod.node_group is not None and \
        mod.node_group.get("maximize_kind") == "edit_poly"


def active_edit_poly(obj):
    if obj is None or obj.type != 'MESH':
        return None
    mod = obj.modifiers.active
    return mod if is_edit_poly(mod) else None


def _helpers(mod):
    return modifier_input(mod, "Base").value, modifier_input(mod, "Edited").value


def _evaluated_mesh(context, obj, upto, include):
    """The object's mesh evaluated up to modifier `upto` (including it when `include`)."""
    index = list(obj.modifiers).index(upto)
    saved = [(m, m.show_viewport) for m in obj.modifiers]
    for i, m in enumerate(obj.modifiers):
        if i > index or (i == index and not include):
            m.show_viewport = False
    try:
        depsgraph = context.evaluated_depsgraph_get()
        depsgraph.update()
        ob_eval = obj.evaluated_get(depsgraph)
        mesh = bpy.data.meshes.new_from_object(ob_eval, preserve_all_data_layers=True, depsgraph=depsgraph)
    finally:
        for m, show in saved:
            m.show_viewport = show
    return mesh


def _point_count(mesh):
    return len(mesh.vertices)


def _set_orig(mesh, values=None):
    attr = mesh.attributes.get(ORIG)
    if attr is None:
        attr = mesh.attributes.new(ORIG, 'INT', 'POINT')
    if values is None:
        values = np.arange(len(mesh.vertices), dtype=np.int32)
    attr.data.foreach_set("value", values)


def _remap_nearest(edited, base):
    """After a topology change below: each edited vertex follows the nearest new base vertex."""
    from mathutils.kdtree import KDTree
    tree = KDTree(len(base.vertices))
    for v in base.vertices:
        tree.insert(v.co, v.index)
    tree.balance()
    _set_orig(edited, np.array([tree.find(v.co)[1] if len(base.vertices) else -1
                                for v in edited.vertices], dtype=np.int32))


def _helper_object(name, mesh):
    obj = bpy.data.objects.new(name, mesh)
    obj[TAG] = True
    obj.hide_render = True
    return obj


def _replace_mesh(obj, mesh):
    old = obj.data
    obj.data = mesh
    if old.users == 0:
        bpy.data.meshes.remove(old)


def rebase(context, obj, mod):
    """Base := the current input of the modifier, Edited := its current result."""
    base_ob, edited_ob = _helpers(mod)
    new_base = _evaluated_mesh(context, obj, mod, include=False)
    new_edited = _evaluated_mesh(context, obj, mod, include=True)
    if ORIG not in new_edited.attributes:
        _set_orig(new_edited)
    elif base_ob.data is not None and len(base_ob.data.vertices) != len(new_base.vertices):
        _remap_nearest(new_edited, new_base)
    _replace_mesh(base_ob, new_base)
    _replace_mesh(edited_ob, new_edited)
    base_ob.data.name = obj.name + " Edit Poly Base"
    edited_ob.data.name = obj.name + " Edit Poly"


class MAXIMIZE_OT_edit_poly_add(Operator):
    """Add an Edit Poly modifier on top of the stack: edit the mesh without collapsing the modifiers
    below"""
    bl_idname = "maximize.edit_poly_add"
    bl_label = "Edit Poly"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and context.mode == 'OBJECT'

    def execute(self, context):
        obj = context.active_object
        mod = obj.modifiers.new("Edit Poly", 'NODES')
        mod.node_group = build_group()
        base = bpy.data.meshes.new(obj.name + " Edit Poly Base")
        edited = bpy.data.meshes.new(obj.name + " Edit Poly")
        modifier_input(mod, "Base").value = _helper_object(obj.name + " Edit Poly Base", base)
        modifier_input(mod, "Edited").value = _helper_object(obj.name + " Edit Poly", edited)
        obj.modifiers.active = mod
        # Start with no edits: Edited is a copy of the input.
        base_ob, edited_ob = _helpers(mod)
        new_base = _evaluated_mesh(context, obj, mod, include=False)
        new_edited = new_base.copy()
        _set_orig(new_edited)
        _replace_mesh(base_ob, new_base)
        _replace_mesh(edited_ob, new_edited)
        base_ob.data.name = obj.name + " Edit Poly Base"
        edited_ob.data.name = obj.name + " Edit Poly"
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Editing: the Edited helper stands in for the object while you edit.


def _session(scene):
    """The running edit session as a plain dict (a copy: the ID property can go away)."""
    session = scene.get("maximize_edit_poly_session")
    return session.to_dict() if session is not None else None


def begin_edit(context, obj, mod, select_mode):
    rebase(context, obj, mod)
    _base_ob, edited_ob = _helpers(mod)
    for o in context.selected_objects:
        o.select_set(False)
    context.scene.collection.objects.link(edited_ob)
    edited_ob.matrix_world = obj.matrix_world
    # Show the modifiers above Edit Poly on the stand-in too? Max shows the result up to here.
    obj.hide_set(True)
    edited_ob.hide_set(False)
    edited_ob.select_set(True)
    context.view_layer.objects.active = edited_ob
    context.scene["maximize_edit_poly_session"] = {"object": obj.name, "modifier": mod.name,
                                                   "edited": edited_ob.name}
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type=select_mode)


def end_edit(context):
    """Back to the object; the modifier picks up the edited mesh."""
    scene = context.scene
    session = _session(scene)
    if not session:
        return False
    del scene["maximize_edit_poly_session"]
    edited_ob = bpy.data.objects.get(session["edited"])
    obj = bpy.data.objects.get(session["object"])
    if edited_ob is not None:
        if edited_ob.mode == 'EDIT' and context.view_layer.objects.active == edited_ob:
            bpy.ops.object.mode_set(mode='OBJECT')
        # Vertices made by tools without the attribute (or with garbage) don't follow the input.
        _sanitize_orig(edited_ob.data)
        for coll in list(edited_ob.users_collection):
            coll.objects.unlink(edited_ob)
    if obj is not None:
        obj.hide_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        obj.update_tag()
    return True


def _sanitize_orig(mesh):
    attr = mesh.attributes.get(ORIG)
    if attr is None:
        _set_orig(mesh, np.full(len(mesh.vertices), -1, dtype=np.int32))
        return
    values = np.empty(len(mesh.vertices), dtype=np.int32)
    attr.data.foreach_get("value", values)
    values[(values < 0)] = -1
    attr.data.foreach_set("value", values)


@persistent
def _depsgraph_post(scene, _depsgraph):
    # Leaving Edit Mode on the stand-in any other way (Tab, the mode menu) also ends the session.
    session = _session(scene)
    if not session:
        return
    edited_ob = bpy.data.objects.get(session["edited"])
    if edited_ob is None or edited_ob.mode != 'EDIT':
        bpy.app.timers.register(lambda: end_edit(bpy.context) and None, first_interval=0.0)


def editing_object(context):
    """The object being edited through its Edit Poly modifier, or None."""
    session = _session(context.scene)
    return bpy.data.objects.get(session["object"]) if session else None


class MAXIMIZE_OT_edit_poly_end(Operator):
    """Leave the Edit Poly modifier and return to the object"""
    bl_idname = "maximize.edit_poly_end"
    bl_label = "Exit Edit Poly"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return _session(context.scene) is not None

    def execute(self, context):
        end_edit(context)
        return {'FINISHED'}


def _apply_through(context, obj, mod):
    """Apply the stack from the bottom up to and including `mod`."""
    target = mod.name
    while obj.modifiers:
        first = obj.modifiers[0]
        name = first.name
        helpers = _helpers(first) if is_edit_poly(first) else ()
        with context.temp_override(object=obj, active_object=obj):
            bpy.ops.object.modifier_apply(modifier=name)
        for helper in helpers:
            # Helpers belong to one modifier; once it is applied they can go.
            if helper is not None and helper.get(TAG):
                mesh = helper.data
                bpy.data.objects.remove(helper, do_unlink=True)
                if mesh is not None and mesh.users == 0:
                    bpy.data.meshes.remove(mesh)
        if name == target:
            break
    if ORIG in obj.data.attributes:
        obj.data.attributes.remove(obj.data.attributes[ORIG])


class MAXIMIZE_OT_collapse_to(Operator):
    """Collapse To: apply the active modifier and everything below it"""
    bl_idname = "maximize.collapse_to"
    bl_label = "Collapse To"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and context.mode == 'OBJECT' and \
            obj.modifiers.active is not None

    def execute(self, context):
        obj = context.active_object
        _apply_through(context, obj, obj.modifiers.active)
        return {'FINISHED'}


class MAXIMIZE_OT_collapse_all(Operator):
    """Collapse the whole modifier stack into the mesh (Edit Poly helpers are removed)"""
    bl_idname = "maximize.collapse_all"
    bl_label = "Collapse All"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and context.mode == 'OBJECT'

    def execute(self, context):
        obj = context.active_object
        if obj.modifiers:
            _apply_through(context, obj, obj.modifiers[-1])
        return {'FINISHED'}


class MAXIMIZE_PT_edit_poly(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Max"
    bl_label = "Modifier Stack"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        if _session(context.scene):
            layout.label(text="Editing Edit Poly of " + _session(context.scene)["object"], icon='EDITMODE_HLT')
            layout.operator("maximize.edit_poly_end", icon='LOOP_BACK')
            return
        col = layout.column(align=True)
        col.operator("maximize.edit_poly_add", icon='MODIFIER')
        row = col.row(align=True)
        row.operator("maximize.collapse_to")
        row.operator("maximize.collapse_all")
        mod = active_edit_poly(obj)
        if mod is not None:
            layout.label(text="1–5 edit at this level", icon='INFO')
            ob_eval = obj.evaluated_get(context.evaluated_depsgraph_get())
            attr = ob_eval.data.attributes.get(CHANGED) if ob_eval.type == 'MESH' else None
            if attr is not None and len(attr.data) and attr.data[0].value:
                layout.label(text="Topology below changed: edits kept as they were", icon='ERROR')


classes = (
    MAXIMIZE_OT_edit_poly_add,
    MAXIMIZE_OT_edit_poly_end,
    MAXIMIZE_OT_collapse_to,
    MAXIMIZE_OT_collapse_all,
    MAXIMIZE_PT_edit_poly,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.handlers.depsgraph_update_post.append(_depsgraph_post)


def unregister():
    if _depsgraph_post in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_depsgraph_post)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

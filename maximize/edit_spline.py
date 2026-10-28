# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Edit Spline as a modifier (stage 0, add-on): edit a shape in the middle of its stack, as Max's
Edit Spline modifier does, without converting it.

The modifier is a Geometry Nodes group with two hidden helper curve objects, as the Edit Poly
prototype (`edit_poly.py`):

- **Base**: the splines that came into the modifier when you last edited it.
- **Edited**: your edited version of them.

Each edited knot knows which base knot it came from. Legacy curves have no custom point
attributes, so the knot index is kept in the knot's **tilt** (an integer value). Knots made
by subdividing get an in-between tilt and count as new; knots that are copied keep it. The
output's tilt is taken back from the input.

While the knot count below stays the same, the modifier outputs the edited splines and moves each
knot, and its handles, by how far its base knot has moved since (index-based, as Max does). So
changing the parameters of the shape below moves the edits along. When the knot count below
changes, the edits stay as they were and the panel warns.

Editing (1, 2, 3 on a shape whose active modifier is Edit Spline) re-bases first: Base becomes the
current input and Edited the current result. Then you edit Edited in place of the object, with
every Editable Spline tool. Leaving the level returns to the object.

*Files:* a Geometry Nodes modifier plus two helper objects; stock Blender evaluates them as they are.

**Native (Moritz builds with the `EDIT_SPLINE` modifier):** the edit lives in the modifier itself
(see the Moritz source `MOD_edit_spline.cc`), with no helper objects. Builds with
`session_begin` edit on the object itself: Edit Mode shows the modifier's result and writes back
into it. Older native builds use a stand-in object for the time of the edit and store with
`modifier.store()`, mapping knots through the tilt as above. Stock Blender keeps the modifier,
disabled.
"""

import bpy
from bpy.app.handlers import persistent
from bpy.types import Operator

from .nodes import GroupBuilder, find_group, modifier_input

GROUP = "MX Edit Spline"
CHANGED = "mx_topology_changed"
TAG = "maximize_edit_spline"
SESSION = "maximize_edit_spline_session"


def build_group():
    group = find_group(GROUP)
    if group is not None:
        return group
    old = bpy.data.node_groups.get(GROUP)
    if old is not None:
        old.name = GROUP + " (old)"
    g = GroupBuilder(GROUP, "edit_spline")
    geometry = g.input("Geometry", 'NodeSocketGeometry')
    base_ob = g.input("Base", 'NodeSocketObject')
    edited_ob = g.input("Edited", 'NodeSocketObject')
    out = g.output()

    def info(ob):
        return g.node('GeometryNodeObjectInfo', {"Object": ob}, transform_space='ORIGINAL').outputs["Geometry"]

    base, edited = info(base_ob), info(edited_ob)

    def points(geo):
        return g.node('GeometryNodeAttributeDomainSize', {"Geometry": geo}, component='CURVE').outputs["Point Count"]

    same_topology = g.node('FunctionNodeCompare', {"A": points(geometry), "B": points(base), "Epsilon": 0.5},
                           data_type='FLOAT', operation='EQUAL').outputs["Result"]
    # The base knot index, kept in the tilt of the edited knots.
    tilt = g.node('GeometryNodeInputCurveTilt').outputs[0]
    orig = g.math('ROUND', tilt)
    whole = g.node('FunctionNodeCompare', {"A": tilt, "B": orig, "Epsilon": 1e-3},
                   data_type='FLOAT', operation='EQUAL').outputs["Result"]
    known = g.node('FunctionNodeCompare', {"A": orig, "B": 0.0},
                   data_type='FLOAT', operation='GREATER_EQUAL').outputs["Result"]
    mapped = g.node('FunctionNodeBooleanMath', {0: whole, 1: known}, operation='AND').outputs[0]
    use = g.node('FunctionNodeBooleanMath', {0: same_topology, 1: mapped}, operation='AND').outputs[0]
    position = g.node('GeometryNodeInputPosition').outputs[0]

    def sample(geo, value, data_type='FLOAT_VECTOR'):
        return g.node('GeometryNodeSampleIndex', {"Geometry": geo, "Value": value, "Index": orig},
                      data_type=data_type, domain='POINT').outputs[0]

    offset = g.vmath('SUBTRACT', sample(geometry, position), sample(base, position))
    offset = g.node('GeometryNodeSwitch', {"Switch": use, "True": offset}, input_type='VECTOR').outputs[0]
    moved = g.node('GeometryNodeSetPosition', {"Geometry": edited, "Offset": offset}).outputs[0]
    for mode in ('LEFT', 'RIGHT'):
        moved = g.node('GeometryNodeSetCurveHandlePositions', {"Curve": moved, "Offset": offset},
                       mode=mode).outputs[0]
    # The tilt carried the knot index: give the knots the input's tilt back.
    input_tilt = sample(geometry, g.node('GeometryNodeInputCurveTilt').outputs[0], 'FLOAT')
    input_tilt = g.node('GeometryNodeSwitch', {"Switch": use, "True": input_tilt}, input_type='FLOAT').outputs[0]
    moved = g.node('GeometryNodeSetCurveTilt', {"Curve": moved, "Tilt": input_tilt}).outputs[0]
    # For the panel's warning.
    changed = g.node('FunctionNodeBooleanMath', {0: same_topology}, operation='NOT').outputs[0]
    moved = g.node('GeometryNodeStoreNamedAttribute', {"Geometry": moved, "Name": CHANGED, "Value": changed},
                   data_type='BOOLEAN', domain='POINT').outputs[0]
    g.set(out, moved)
    return g.tree


def native():
    """True in Moritz builds that have the native Edit Spline modifier."""
    return hasattr(bpy.types, "EditSplineModifier")


def is_native(mod):
    return mod is not None and mod.type == 'EDIT_SPLINE'


def is_edit_spline(mod):
    return is_native(mod) or (mod is not None and mod.type == 'NODES' and mod.node_group is not None and
                              mod.node_group.get("maximize_kind") == "edit_spline")


def active_edit_spline(obj):
    if obj is None or obj.type != 'CURVE':
        return None
    mod = obj.modifiers.active
    return mod if is_edit_spline(mod) else None


def _helpers(mod):
    return modifier_input(mod, "Base").value, modifier_input(mod, "Edited").value


def _evaluated_curve(context, obj, upto, include, name):
    """The object's splines evaluated up to modifier `upto` (including it when `include`), as
    legacy curve data."""
    from .shapes import curve_from_geometry
    index = list(obj.modifiers).index(upto)
    saved = [(m, m.show_viewport) for m in obj.modifiers]
    for i, m in enumerate(obj.modifiers):
        if i > index or (i == index and not include):
            m.show_viewport = False
    try:
        obj.update_tag()
        depsgraph = context.evaluated_depsgraph_get()
        depsgraph.update()
        geometry = obj.evaluated_get(depsgraph).evaluated_geometry()
        data = curve_from_geometry(geometry.curves, name)
    finally:
        for m, show in saved:
            m.show_viewport = show
        obj.update_tag()
    data.resolution_u = obj.data.resolution_u
    return data


def _knots(curve):
    return [bp for s in curve.splines if s.type == 'BEZIER' for bp in s.bezier_points]


def _set_ids(curve, ids=None):
    """Store each knot's base index in its tilt (identity when `ids` is None)."""
    for i, bp in enumerate(_knots(curve)):
        bp.tilt = float(i if ids is None else ids[i])


def _remap_nearest(edited, base):
    """After a topology change below: each edited knot follows the nearest new base knot."""
    from mathutils.kdtree import KDTree
    knots = _knots(base)
    tree = KDTree(len(knots))
    for i, bp in enumerate(knots):
        tree.insert(bp.co, i)
    tree.balance()
    for bp in _knots(edited):
        bp.tilt = float(tree.find(bp.co)[1]) if knots else -1.0


def _helper_object(name, curve):
    obj = bpy.data.objects.new(name, curve)
    obj[TAG] = True
    obj.hide_render = True
    return obj


def _replace_curve(obj, curve):
    old = obj.data
    obj.data = curve
    if old is not None and old.users == 0:
        bpy.data.curves.remove(old)


def rebase(context, obj, mod):
    """Base := the current input of the modifier, Edited := its current result (with its ids)."""
    base_ob, edited_ob = _helpers(mod)
    old_ids = [bp.tilt for bp in _knots(edited_ob.data)] if edited_ob.data is not None else []
    old_base_count = len(_knots(base_ob.data)) if base_ob.data is not None else -1
    new_base = _evaluated_curve(context, obj, mod, False, obj.name + " Edit Spline Base")
    new_edited = _evaluated_curve(context, obj, mod, True, obj.name + " Edit Spline")
    knots = _knots(new_edited)
    if len(old_ids) == len(knots) and old_base_count == len(_knots(new_base)):
        # The result is the edited helper moved: same knots, same ids.
        _set_ids(new_edited, old_ids)
    else:
        _remap_nearest(new_edited, new_base)
    _replace_curve(base_ob, new_base)
    _replace_curve(edited_ob, new_edited)


def add_edit_spline(context, obj):
    if native():
        mod = obj.modifiers.new("Edit Spline", 'EDIT_SPLINE')
    else:
        mod = obj.modifiers.new("Edit Spline", 'NODES')
        mod.node_group = build_group()
    # Below the Rendering modifier, which turns the splines into a mesh.
    from .spline_render import rendering_modifier
    render = rendering_modifier(obj)
    if render is not None:
        with context.temp_override(object=obj, active_object=obj):
            bpy.ops.object.modifier_move_to_index(modifier=mod.name, index=list(obj.modifiers).index(render))
    if is_native(mod):
        obj.modifiers.active = mod
        obj.update_tag()
        return mod
    base = _evaluated_curve(context, obj, mod, False, obj.name + " Edit Spline Base")
    edited = base.copy()
    edited.name = obj.name + " Edit Spline"
    _set_ids(edited)
    modifier_input(mod, "Base").value = _helper_object(obj.name + " Edit Spline Base", base)
    modifier_input(mod, "Edited").value = _helper_object(obj.name + " Edit Spline", edited)
    obj.modifiers.active = mod
    obj.update_tag()
    return mod


def convert_to_native(context, obj, mod):
    """Replace a stage-0 (Geometry Nodes) Edit Spline with the native modifier, keeping the edit.
    Returns the new modifier."""
    input_curves = _evaluated_curves(context, obj, mod, False)
    output = _evaluated_curves(context, obj, mod, True)
    base_ob, edited_ob = _helpers(mod)
    ids = [bp.tilt for bp in _knots(edited_ob.data)] if edited_ob and edited_ob.data else []
    same = base_ob is not None and base_ob.data is not None and \
        len(_knots(base_ob.data)) == len(input_curves.points) and len(ids) == len(output.points)
    if same:
        mapped = [int(round(t)) if abs(t - round(t)) < 1e-3 and t >= 0 else -1 for t in ids]
    else:
        # The knots below changed since the last edit: each knot follows the nearest input knot.
        from mathutils.kdtree import KDTree
        points = [d.vector for d in input_curves.attributes["position"].data]
        tree = KDTree(len(points))
        for i, co in enumerate(points):
            tree.insert(co, i)
        tree.balance()
        mapped = [tree.find(d.vector)[1] if points else -1 for d in output.attributes["position"].data]
    orig = output.attributes.get("mx_orig") or output.attributes.new("mx_orig", 'INT', 'POINT')
    orig.data.foreach_set("value", mapped)
    index = list(obj.modifiers).index(mod)
    name = mod.name
    native_mod = obj.modifiers.new(name + " (native)", 'EDIT_SPLINE')
    with context.temp_override(object=obj, active_object=obj):
        bpy.ops.object.modifier_move_to_index(modifier=native_mod.name, index=index)
    native_mod.store(input=input_curves, edited=output)
    bpy.data.hair_curves.remove(input_curves)
    bpy.data.hair_curves.remove(output)
    obj.modifiers.remove(mod)
    native_mod.name = name
    for helper in (base_ob, edited_ob):
        if helper is not None and helper.get(TAG):
            data = helper.data
            bpy.data.objects.remove(helper)
            if data is not None and data.users == 0:
                bpy.data.curves.remove(data)
    obj.modifiers.active = native_mod
    obj.update_tag()
    return native_mod


class MAXIMIZE_OT_edit_spline_convert(Operator):
    """Replace this Geometry Nodes Edit Spline with Moritz's native Edit Spline modifier, keeping
    the edit. Stock Blender then shows the shape without the edit (it keeps the modifier, disabled)"""
    bl_idname = "maximize.edit_spline_convert"
    bl_label = "Convert to Native"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        mod = active_edit_spline(obj)
        return native() and mod is not None and not is_native(mod) and context.mode == 'OBJECT'

    def execute(self, context):
        obj = context.active_object
        convert_to_native(context, obj, active_edit_spline(obj))
        return {'FINISHED'}


class MAXIMIZE_OT_edit_spline_add(Operator):
    """Add an Edit Spline modifier: edit the shape's splines without converting it, so its
    parameters stay editable below"""
    bl_idname = "maximize.edit_spline_add"
    bl_label = "Edit Spline"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'CURVE' and context.mode == 'OBJECT'

    def execute(self, context):
        add_edit_spline(context, context.active_object)
        return {'FINISHED'}


# ------------------------------------------------------------------------------
# Editing: the Edited helper stands in for the object while you edit.


def _session(scene):
    session = scene.get(SESSION)
    return session.to_dict() if session is not None else None


def _evaluated_curves(context, obj, upto, include):
    """A Curves data-block copy of the object's splines evaluated up to modifier `upto`."""
    index = list(obj.modifiers).index(upto)
    saved = [(m, m.show_viewport) for m in obj.modifiers]
    for i, m in enumerate(obj.modifiers):
        if i > index or (i == index and not include):
            m.show_viewport = False
    try:
        obj.update_tag()
        depsgraph = context.evaluated_depsgraph_get()
        depsgraph.update()
        geometry = obj.evaluated_get(depsgraph).evaluated_geometry()
        return copy_curves(geometry.curves, obj.name + " Edit Spline Input")
    finally:
        for m, show in saved:
            m.show_viewport = show
        obj.update_tag()


_ATTR_KEYS = {"FLOAT_VECTOR": ("vector", 3), "FLOAT": ("value", 1), "INT": ("value", 1),
              "INT8": ("value", 1), "BOOLEAN": ("value", 1), "FLOAT_COLOR": ("color", 4)}


def copy_curves(src, name):
    """A new Curves data-block with the points, curves and attributes of `src` (e.g. evaluated)."""
    dst = bpy.data.hair_curves.new(name)
    dst.add_curves([c.points_length for c in src.curves])
    # Types first, through the API (it keeps Blender's type counts right), then the values.
    types = src.attributes.get("curve_type")
    kinds = {d.value for d in types.data} if types is not None else {0}
    names = {0: 'CATMULL_ROM', 1: 'POLY', 2: 'BEZIER', 3: 'NURBS'}
    if len(kinds) == 1:
        dst.set_types(type=names.get(kinds.pop(), 'POLY'))
    for attr in src.attributes:
        if attr.name.startswith(".") or attr.data_type not in _ATTR_KEYS:
            continue
        if attr.name == "curve_type" and len(kinds) <= 1:
            continue
        key, width = _ATTR_KEYS[attr.data_type]
        target = dst.attributes.get(attr.name) or dst.attributes.new(attr.name, attr.data_type, attr.domain)
        values = [0] * (len(attr.data) * width)
        attr.data.foreach_get(key, values)
        target.data.foreach_set(key, values)
    return dst


def _begin_native(context, obj, mod):
    """The stand-in for a native modifier: its current result, knots tagged with their input index."""
    from .shapes import curve_from_geometry
    input_curves = _evaluated_curves(context, obj, mod, False)
    output = _evaluated_curves(context, obj, mod, True)
    data = curve_from_geometry(output, obj.name + " Edit Spline")
    data.resolution_u = obj.data.resolution_u
    changed = output.attributes.get(CHANGED)
    if changed is not None and len(changed.data) and changed.data[0].value:
        # The knots below changed since the last edit: each knot follows the nearest new one.
        base = curve_from_geometry(input_curves, obj.name + " Edit Spline Base")
        _remap_nearest(data, base)
        bpy.data.curves.remove(base)
    else:
        orig = output.attributes.get("mx_orig")
        _set_ids(data, [d.value for d in orig.data] if orig is not None else None)
    bpy.data.hair_curves.remove(output)
    return _helper_object(obj.name + " Edit Spline", data), input_curves.name


def _end_native(obj, mod, edited_ob, input_name):
    """Store the stand-in's splines in the native modifier."""
    input_curves = bpy.data.hair_curves.get(input_name)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    # Keep the geometry set alive while its curves are read.
    geometry = edited_ob.evaluated_get(depsgraph).evaluated_geometry()
    edited = copy_curves(geometry.curves, obj.name + " Edit Spline Edited")
    tilt = edited.attributes.get("tilt")
    ids = [d.value for d in tilt.data] if tilt is not None else []
    mapped = [int(round(t)) if abs(t - round(t)) < 1e-3 and t >= 0 else -1 for t in ids]
    edited.attributes.new("mx_orig", 'INT', 'POINT').data.foreach_set("value", mapped)
    # The tilt carried the knot index: give the knots the input's tilt back.
    in_tilt = input_curves.attributes.get("tilt") if input_curves else None
    if tilt is not None:
        tilt.data.foreach_set("value", [
            in_tilt.data[m].value if in_tilt is not None and 0 <= m < len(in_tilt.data) else 0.0
            for m in mapped])
    if input_curves is not None:
        mod.store(input=input_curves, edited=edited)
        bpy.data.hair_curves.remove(input_curves)
    bpy.data.hair_curves.remove(edited)


def _session_curves(context, obj, mod):
    """The modifier's input and its current result, the result's knots mapped to input knots
    (`mx_orig`; by nearest position after a knot count change below)."""
    input_curves = _evaluated_curves(context, obj, mod, False)
    output = _evaluated_curves(context, obj, mod, True)
    changed = output.attributes.get(CHANGED)
    if changed is not None and len(changed.data) and changed.data[0].value:
        from mathutils.kdtree import KDTree
        points = [d.vector for d in input_curves.attributes["position"].data]
        tree = KDTree(len(points))
        for i, co in enumerate(points):
            tree.insert(co, i)
        tree.balance()
        orig = output.attributes.get("mx_orig") or output.attributes.new("mx_orig", 'INT', 'POINT')
        orig.data.foreach_set("value", [tree.find(d.vector)[1] if points else -1
                                        for d in output.attributes["position"].data])
    return input_curves, output


def begin_edit(context, obj, mod, level):
    if is_native(mod) and hasattr(mod, "session_begin"):
        # Edit on the object itself: Edit Mode shows the modifier's result.
        input_curves, output = _session_curves(context, obj, mod)
        try:
            ok = mod.session_begin(input=input_curves, edited=output)
        finally:
            bpy.data.hair_curves.remove(input_curves)
            bpy.data.hair_curves.remove(output)
        if not ok:
            return False
        for o in context.selected_objects:
            o.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        context.scene[SESSION] = {"object": obj.name, "modifier": mod.name, "native": True}
        bpy.ops.object.mode_set(mode='EDIT')
        context.scene["maximize_level"] = level
        return True
    if is_native(mod):
        edited_ob, input_name = _begin_native(context, obj, mod)
    else:
        rebase(context, obj, mod)
        _base_ob, edited_ob = _helpers(mod)
        input_name = ""
    for o in context.selected_objects:
        o.select_set(False)
    context.scene.collection.objects.link(edited_ob)
    edited_ob.matrix_world = obj.matrix_world
    obj.hide_set(True)
    edited_ob.hide_set(False)
    edited_ob.select_set(True)
    context.view_layer.objects.active = edited_ob
    context.scene[SESSION] = {"object": obj.name, "modifier": mod.name, "edited": edited_ob.name,
                              "input": input_name}
    bpy.ops.object.mode_set(mode='EDIT')
    context.scene["maximize_level"] = level


def end_edit(context):
    """Back to the object; the modifier picks up the edited splines."""
    scene = context.scene
    session = _session(scene)
    if not session:
        return False
    del scene[SESSION]
    obj = bpy.data.objects.get(session["object"])
    if session.get("native"):
        # Leaving Edit Mode writes the edit into the modifier and ends the session.
        if obj is not None and obj.mode == 'EDIT':
            with context.temp_override(active_object=obj, object=obj):
                bpy.ops.object.mode_set(mode='OBJECT')
        scene["maximize_level"] = 'OBJECT'
        return True
    edited_ob = bpy.data.objects.get(session["edited"])
    if edited_ob is not None:
        if edited_ob.mode == 'EDIT' and context.view_layer.objects.active == edited_ob:
            bpy.ops.object.mode_set(mode='OBJECT')
    mod = obj.modifiers.get(session["modifier"]) if obj is not None else None
    if is_native(mod) and edited_ob is not None:
        # Store while the stand-in is still in the scene (it is evaluated for its splines).
        _end_native(obj, mod, edited_ob, session.get("input", ""))
    if edited_ob is not None:
        for coll in list(edited_ob.users_collection):
            coll.objects.unlink(edited_ob)
    if is_native(mod) and edited_ob is not None:
        data = edited_ob.data
        bpy.data.objects.remove(edited_ob)
        if data is not None and data.users == 0:
            bpy.data.curves.remove(data)
    if obj is not None:
        obj.hide_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        obj.update_tag()
    scene["maximize_level"] = 'OBJECT'
    return True


@persistent
def _depsgraph_post(scene, _depsgraph):
    # Leaving Edit Mode on the stand-in any other way (Tab, the mode menu) also ends the session.
    session = _session(scene)
    if not session:
        return
    if _left_edit_mode(session):
        # Checked again then: an update can come between starting the session and entering
        # Edit Mode.
        bpy.app.timers.register(_end_if_left, first_interval=0.0)


def _left_edit_mode(session):
    edited_ob = bpy.data.objects.get(session["object" if session.get("native") else "edited"])
    return edited_ob is None or edited_ob.mode != 'EDIT'


def _end_if_left():
    session = _session(bpy.context.scene)
    if session and _left_edit_mode(session):
        end_edit(bpy.context)


def editing_object(context):
    session = _session(context.scene)
    return bpy.data.objects.get(session["object"]) if session else None


class MAXIMIZE_OT_edit_spline_end(Operator):
    """Leave the Edit Spline modifier and return to the object"""
    bl_idname = "maximize.edit_spline_end"
    bl_label = "Exit Edit Spline"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return _session(context.scene) is not None

    def execute(self, context):
        end_edit(context)
        return {'FINISHED'}


def topology_changed(context, obj):
    ob_eval = obj.evaluated_get(context.evaluated_depsgraph_get())
    geometry = ob_eval.evaluated_geometry()
    curves = geometry.curves
    if curves is None:
        return False
    attr = curves.attributes.get(CHANGED)
    return attr is not None and len(attr.data) > 0 and attr.data[0].value


def draw(layout, context, obj):
    session = _session(context.scene)
    if session:
        layout.label(text="Editing the Edit Spline modifier of " + session["object"], icon='EDITMODE_HLT')
        layout.operator("maximize.edit_spline_end", icon='LOOP_BACK')
        return
    mod = active_edit_spline(obj)
    if mod is None:
        layout.operator("maximize.edit_spline_add", icon='MODIFIER')
        return
    layout.label(text="1, 2, 3 edit at this level", icon='INFO')
    if is_native(mod):
        col = layout.column(align=True)
        col.label(text="Interpolation")
        col.prop(mod, "steps")
        col.prop(mod, "use_optimize")
        col.prop(mod, "use_adaptive")
        return
    if topology_changed(context, obj):
        layout.label(text="Knot count below changed: edits kept as they were", icon='ERROR')
    if native():
        layout.operator("maximize.edit_spline_convert", icon='MODIFIER')


classes = (
    MAXIMIZE_OT_edit_spline_add,
    MAXIMIZE_OT_edit_spline_convert,
    MAXIMIZE_OT_edit_spline_end,
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

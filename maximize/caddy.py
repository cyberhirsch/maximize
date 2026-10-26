# SPDX-FileCopyrightText: 2026 Moritz Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Max's caddy: a tool's settings button opens a small panel at the mouse with the tool's values
(live: changing one redoes the tool), the vertex count before and after, and OK / Apply and
Continue / Cancel. Preferences > Tool Settings picks it or Blender's Adjust Last Operation panel."""

import time

import bmesh
import bpy
from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    IntVectorProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import Operator, PropertyGroup

# Tools whose caddy runs another operator: Chamfer's button is interactive, its caddy is Bevel's.
_CADDY_TOOL = {
    "maximize.chamfer": ("mesh.bevel", lambda context: {
        "affect": 'VERTICES' if context.tool_settings.mesh_select_mode[0] else 'EDGES'}),
}

_state = {"before": None, "after": None, "snapshot": None, "idname": "", "drawn": 0.0, "where": None,
          "mirror": None, "label": ""}
_settings_cache = {}


def use_caddy(context):
    from .preferences import get_prefs
    prefs = get_prefs(context)
    return prefs is not None and prefs.tool_settings_style == 'CADDY'


def _op(idname):
    mod, name = idname.split(".")
    return getattr(getattr(bpy.ops, mod), name)


def has_settings(idname):
    """True when the tool has values a caddy can show."""
    if idname in _CADDY_TOOL:
        return True
    if idname not in _settings_cache:
        try:
            rna = _op(idname).get_rna_type()
            _settings_cache[idname] = any(p.identifier != "rna_type" and not p.is_hidden
                                          for p in rna.properties)
        except (AttributeError, KeyError):
            _settings_cache[idname] = False
    return _settings_cache[idname]


def tool_button(layout, context, idname, **kwargs):
    """The tool's button; in caddy mode a settings button (Max's small square) follows it."""
    if not (use_caddy(context) and has_settings(idname)):
        layout.operator(idname, **kwargs)
        return
    row = layout.row(align=True)
    row.operator(idname, **kwargs)
    row.operator("maximize.caddy_run", text="", icon='OPTIONS').tool = idname


def vertex_count(context):
    total = 0
    for obj in context.objects_in_mode_unique_data:
        if obj.type == 'MESH' and obj.mode == 'EDIT':
            total += len(bmesh.from_edit_mesh(obj.data).verts)
    return total


def last_operator(context):
    ops = context.window_manager.operators
    return ops[-1] if len(ops) else None


def _value(value):
    if isinstance(value, (str, set)):
        return value
    try:
        return tuple(value)
    except TypeError:
        return value


def last_values(idname):
    """The tool's values from its last run (Blender applies them to clicks, not to Python calls)."""
    props = bpy.context.window_manager.operator_properties_last(idname)
    return {p.identifier: _value(getattr(props, p.identifier)) for p in props.bl_rna.properties
            if p.identifier != "rna_type" and p.type not in {'POINTER', 'COLLECTION'} and
            not p.is_readonly and not p.is_skip_save and props.is_property_set(p.identifier)}


def snapshot(op):
    return {p.identifier: _value(getattr(op.properties, p.identifier))
            for p in op.properties.bl_rna.properties if p.identifier != "rna_type"}


# The caddy's fields edit a copy of the tool's values on the window manager, never the operator's
# own properties: undo frees those while the popup can still draw them.
_mirrors = {}


def _spec(p):
    """A property definition like `p` (an operator property's RNA), or None."""
    common = {"name": p.name, "description": p.description}
    if p.type == 'ENUM':
        items = [(i.identifier, i.name, i.description, i.icon, i.value) for i in p.enum_items]
        if not items:
            return None
        if p.is_enum_flag:
            return EnumProperty(items=items, options={'ENUM_FLAG'}, **common)
        return EnumProperty(items=items, **common)
    if p.type == 'STRING':
        return StringProperty(**common)
    if p.type == 'BOOLEAN':
        if p.is_array:
            return BoolVectorProperty(size=p.array_length, **common)
        return BoolProperty(**common)
    limits = {"min": p.hard_min, "max": p.hard_max, "soft_min": p.soft_min, "soft_max": p.soft_max}
    if p.type == 'INT':
        if p.is_array:
            return IntVectorProperty(size=p.array_length, **limits, **common)
        return IntProperty(step=p.step, **limits, **common)
    if p.type == 'FLOAT':
        extra = {"step": p.step, "precision": p.precision, **limits, **common}
        for kwargs in ({"subtype": p.subtype, "unit": p.unit}, {"unit": p.unit}, {}):
            try:
                if p.is_array:
                    return FloatVectorProperty(size=p.array_length, **kwargs, **extra)
                return FloatProperty(**kwargs, **extra)
            except TypeError:
                continue
    return None


def mirror(context, op):
    """The window manager's copy of `op`'s values (made once per tool), filled from `op`."""
    idname = op.bl_idname
    if idname not in _mirrors:
        fields = {}
        for p in op.properties.bl_rna.properties:
            if p.identifier == "rna_type" or p.is_hidden or p.is_readonly or p.type in {'POINTER', 'COLLECTION'}:
                continue
            spec = _spec(p)
            if spec is not None:
                fields[p.identifier] = spec
        cls = type("MAXIMIZE_PG_caddy_" + idname.lower(), (PropertyGroup,), {"__annotations__": fields})
        bpy.utils.register_class(cls)
        attr = "maximize_caddy_" + idname.lower()
        setattr(bpy.types.WindowManager, attr, PointerProperty(type=cls))
        _mirrors[idname] = (cls, attr, list(fields))
    _cls, attr, fields = _mirrors[idname]
    values = getattr(context.window_manager, attr)
    for name in fields:
        try:
            setattr(values, name, getattr(op.properties, name))
        except (TypeError, ValueError):
            pass
    return values, fields


def mirror_values(values, fields):
    return {name: _value(getattr(values, name)) for name in fields}


def _override():
    window, area, region = _state["where"] or (None, None, None)
    if window is None or window not in bpy.context.window_manager.windows[:]:
        window = bpy.context.window_manager.windows[0]
        area = region = None
    if area is not None and area not in window.screen.areas[:]:
        area = region = None
    kwargs = {"window": window, "screen": window.screen}
    if area is not None:
        kwargs["area"] = area
        if region is not None and region in area.regions[:]:
            kwargs["region"] = region
    return bpy.context.temp_override(**kwargs)


def _watch():
    """While the caddy is open: a changed value redoes the tool (Blender's Undo and Redo)."""
    context = bpy.context
    op = last_operator(context)
    if op is None or op.bl_idname != _state["idname"] or time.monotonic() - _state["drawn"] > 1.0:
        return None
    values, fields = _state["mirror"]
    current = mirror_values(values, fields)
    if current != _state["snapshot"]:
        for name, value in current.items():
            try:
                setattr(op.properties, name, value)
            except (TypeError, ValueError):
                pass
        with _override():
            if bpy.ops.ed.undo_redo.poll():
                bpy.ops.ed.undo_redo('EXEC_DEFAULT', True)
            _state["after"] = vertex_count(bpy.context)
        op = last_operator(context)
        if op is not None:
            # The tool may adjust its own values (clamping); show what it used.
            _state["mirror"] = mirror(context, op)
        _state["snapshot"] = mirror_values(*_state["mirror"])
    return 0.1


def draw_caddy(self, context):
    layout = self.layout
    if _state["mirror"] is None:
        layout.label(text="Nothing to adjust")
        return
    _state["drawn"] = time.monotonic()
    if not bpy.app.timers.is_registered(_watch):
        bpy.app.timers.register(_watch, first_interval=0.1)
    layout.label(text=_state["label"])
    col = layout.column()
    col.use_property_split = True
    col.use_property_decorate = False
    values, fields = _state["mirror"]
    for name in fields:
        col.prop(values, name)
    if _state["before"] is not None:
        layout.label(text="Before: %d, After: %d" % (_state["before"], _state["after"]))
    row = layout.row(align=True)
    row.operator("maximize.caddy_ok", text="OK", icon='CHECKMARK')
    row.operator("maximize.caddy_continue", text="", icon='ADD')
    row.operator("maximize.caddy_cancel", text="", icon='X')


def open_caddy(context, before):
    op = last_operator(context)
    if op is None:
        return
    values = mirror(context, op)
    _state.update(before=before, after=vertex_count(context), mirror=values, snapshot=mirror_values(*values),
                  idname=op.bl_idname, label=op.name, drawn=time.monotonic())
    context.window_manager.popover(draw_caddy, ui_units_x=13)


def run_tool(context, idname):
    """Run `idname` with its last values (Max's caddy runs the tool, then shows its values)."""
    target, extra = _CADDY_TOOL.get(idname, (idname, None))
    values = last_values(target)
    if extra:
        values.update(extra(context))
    # undo=True: an undo step and a place in the redo list, so the caddy (and Undo and Redo) can redo it.
    return _op(target)('EXEC_DEFAULT', True, **values)


def _later(func):
    """Run `func` after the calling operator finished, so the tool registers as the last operation."""
    def step():
        with _override():
            func(bpy.context)
        return None
    bpy.app.timers.register(step, first_interval=0.0)


def _remember(context):
    _state["where"] = (context.window, context.area, context.region)


class MAXIMIZE_OT_caddy_run(Operator):
    """Run the tool and open its settings at the mouse (Max's caddy)"""
    bl_idname = "maximize.caddy_run"
    bl_label = "Settings"
    bl_options = {'INTERNAL'}

    tool: StringProperty(options={'HIDDEN'})

    def execute(self, context):
        _remember(context)
        tool = self.tool

        def go(ctx):
            before = vertex_count(ctx)
            if 'FINISHED' in run_tool(ctx, tool):
                open_caddy(ctx, before)
        _later(go)
        return {'FINISHED'}


class MAXIMIZE_OT_caddy_ok(Operator):
    """Keep the result"""
    bl_idname = "maximize.caddy_ok"
    bl_label = "OK"
    bl_options = {'INTERNAL'}

    def execute(self, _context):
        _state["drawn"] = 0.0
        return {'FINISHED'}


class MAXIMIZE_OT_caddy_continue(Operator):
    """Apply and Continue: keep the result and run the tool again on it, with the same values"""
    bl_idname = "maximize.caddy_continue"
    bl_label = "Apply and Continue"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        _remember(context)

        def go(ctx):
            op = last_operator(ctx)
            if op is None:
                return
            # Not Repeat Last: it adds no undo step of its own, so Cancel would take back both runs.
            values = mirror_values(*mirror(ctx, op))
            module, name = op.bl_idname.split("_OT_")
            before = vertex_count(ctx)
            if 'FINISHED' in _op(module.lower() + "." + name)('EXEC_DEFAULT', True, **values):
                open_caddy(ctx, before)
        _later(go)
        return {'FINISHED'}


class MAXIMIZE_OT_caddy_cancel(Operator):
    """Cancel: take the tool back"""
    bl_idname = "maximize.caddy_cancel"
    bl_label = "Cancel"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        _state["drawn"] = 0.0
        _remember(context)
        _later(lambda _ctx: bpy.ops.ed.undo())
        return {'FINISHED'}


classes = (
    MAXIMIZE_OT_caddy_run,
    MAXIMIZE_OT_caddy_ok,
    MAXIMIZE_OT_caddy_continue,
    MAXIMIZE_OT_caddy_cancel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    if bpy.app.timers.is_registered(_watch):
        bpy.app.timers.unregister(_watch)
    _state["mirror"] = None
    for cls, attr, _fields in _mirrors.values():
        delattr(bpy.types.WindowManager, attr)
        bpy.utils.unregister_class(cls)
    _mirrors.clear()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

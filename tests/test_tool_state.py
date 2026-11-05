# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_tool_state.py
# A running tool: its button is lit (`is_running`), the pointer is set on start and restored on the
# way out, and both end with Esc and with a right-click. The tools also start from the Command Panel
# (the operator invoked from the Properties editor), and the drawn buttons are checked there.
import os
import sys
import traceback

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bmesh
import bpy
from maximize import preferences, tool_state, ui

failures = []
calls = {"begin": 0, "end": 0}
redraws = {"count": 0}
real_begin, real_end, real_redraw = tool_state.begin, tool_state.end, tool_state.redraw


def counted_redraw():
    redraws["count"] += 1
    real_redraw()


tool_state.redraw = counted_redraw


def counted_begin(context, cursor='CROSSHAIR'):
    calls["begin"] += 1
    real_begin(context, cursor)


def counted_end(context):
    calls["end"] += 1
    real_end(context)


tool_state.begin, tool_state.end = counted_begin, counted_end


def say(*a): print("MXTS", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)
    if not ok:
        failures.append(name)


def view3d():
    window = bpy.context.window_manager.windows[0]
    area = max((a for a in window.screen.areas if a.type == 'VIEW_3D'), key=lambda a: a.width * a.height)
    region = next(r for r in area.regions if r.type == 'WINDOW')
    return window, area, region


def run(idname, **props):
    module, name = idname.split(".")
    window, area, region = view3d()
    with bpy.context.temp_override(window=window, area=area, region=region):
        return getattr(getattr(bpy.ops, module), name)('INVOKE_DEFAULT', **props)


def key(event_type):
    window, area, region = view3d()
    x, y = region.x + region.width // 2, region.y + region.height // 2
    window.event_simulate('MOUSEMOVE', 'NOTHING', x=x, y=y)
    window.event_simulate(event_type, 'PRESS', x=x, y=y)
    window.event_simulate(event_type, 'RELEASE', x=x, y=y)


def set_mode(kind):
    window, area, region = view3d()
    with bpy.context.temp_override(window=window, area=area, region=region):
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        if kind == 'MESH':
            bpy.ops.mesh.primitive_cube_add()
            bpy.ops.object.mode_set(mode='EDIT')
        elif kind == 'CURVE':
            bpy.ops.curve.primitive_bezier_curve_add()
            bpy.ops.object.mode_set(mode='EDIT')


# (operator, properties, mode, pointer, how it ends)
TOOLS = (
    ("maximize.line", {}, 'OBJECT', True, 'ESC'),
    ("maximize.line", {}, 'OBJECT', True, 'RIGHTMOUSE'),
    ("maximize.target_camera", {}, 'OBJECT', True, 'ESC'),
    ("maximize.target_camera", {}, 'OBJECT', True, 'RIGHTMOUSE'),
    ("maximize.add_primitive", {"kind": 'BOX'}, 'OBJECT', True, 'ESC'),
    ("maximize.add_light", {"shape": 'PLANE'}, 'OBJECT', True, 'ESC'),
    ("maximize.spline_insert", {}, 'CURVE', True, 'ESC'),
    ("maximize.spline_trim", {}, 'CURVE', True, 'RIGHTMOUSE'),
    ("maximize.spline_extend", {}, 'CURVE', True, 'ESC'),
    ("maximize.spline_refine", {}, 'CURVE', True, 'ESC'),
    ("maximize.insert_vertex", {}, 'MESH', True, 'ESC'),
    ("maximize.hinge_from_edge", {}, 'MESH', True, 'RIGHTMOUSE'),
)


class Layout:
    """Stands in for a UILayout and records every button a draw function makes."""

    def __init__(self):
        self.buttons = []

    def __getattr__(self, _name):
        return lambda *a, **k: self

    def panel(self, *_a, **_k):
        return self, self

    def operator(self, idname, **kwargs):
        button = Button(idname, kwargs.get("depress", False))
        self.buttons.append(button)
        return button


class Button:
    def __init__(self, idname, depress):
        self.idname, self.depress = idname, depress


def drawn(draw, *args):
    window, area, region = panel()
    layout = Layout()
    with bpy.context.temp_override(window=window, area=area, region=region):
        draw(layout, bpy.context, *args)
    return layout.buttons


def panel():
    window = bpy.context.window_manager.windows[0]
    area = next(a for a in window.screen.areas if a.type == 'PROPERTIES')
    return window, area, next(r for r in area.regions if r.type == 'WINDOW')


def press(idname, **props):
    """What a button in the Command Panel does: invokes the operator from the Properties editor."""
    window, area, region = panel()
    module, name = idname.split(".")
    op = getattr(getattr(bpy.ops, module), name)
    with bpy.context.temp_override(window=window, area=area, region=region):
        if not op.poll():
            return None
        return op('INVOKE_DEFAULT', **props)


def lit(buttons, idname):
    return [b.depress for b in buttons if b.idname == idname]


def spline_geometry(layout, context):
    ui.draw_spline_geometry(layout, context, context.active_object)


def poly_level(layout, context):
    ui._draw_poly_level_rollouts(layout, context, "test")


def poly_geometry(layout, context):
    ui.draw_poly_geometry(layout, context)


def set_level(index):
    mode = [False, False, False]
    mode[index] = True
    bpy.context.tool_settings.mesh_select_mode = mode


# (mode, polygon level, button, what runs, draw function, buttons that stay dark, properties)
PANEL_TOOLS = (
    ('CURVE', None, "maximize.spline_trim", "maximize.spline_trim", spline_geometry, ("maximize.spline_extend",), {}),
    ('CURVE', None, "maximize.spline_extend", "maximize.spline_extend", spline_geometry, ("maximize.spline_trim",), {}),
    ('CURVE', None, "maximize.spline_insert", "maximize.spline_insert", spline_geometry, (), {}),
    ('CURVE', None, "maximize.spline_bind", "maximize.spline_bind", spline_geometry, (), {}),
    ('MESH', 1, "maximize.insert_vertex", "maximize.insert_vertex", poly_level, (), {}),
    ('MESH', 2, "maximize.hinge_from_edge", "maximize.hinge_from_edge", poly_level, ("maximize.extrude_along_spline",), {}),
    ('MESH', 2, "maximize.cut", "mesh.knife_tool", poly_geometry, ("maximize.paint_connect",), {}),
    ('MESH', 2, "maximize.paint_connect", "mesh.knife_tool", poly_geometry, ("maximize.cut",), {}),
    ('MESH', 2, "maximize.quickslice", "mesh.bisect", poly_geometry, (), {}),
    ('MESH', 2, "maximize.inset", "mesh.inset", poly_level, ("maximize.bevel_poly",), {}),
    ('MESH', 2, "maximize.bevel_poly", "mesh.inset", poly_level, ("maximize.inset",), {}),
    ('MESH', 1, "maximize.chamfer", "mesh.bevel", poly_level, (), {}),
)


def click_view(fx, fy):
    window, area, region = view3d()
    x, y = region.x + int(region.width * fx), region.y + int(region.height * fy)
    window.event_simulate('MOUSEMOVE', 'NOTHING', x=x, y=y)
    return window, x, y


def panel_steps():
    for mode, level, idname, target, draw, dark, props in PANEL_TOOLS:
        name = idname + " from the panel"
        set_mode(mode)
        if level is not None:
            set_level(level)
            window, area, region = view3d()
            with bpy.context.temp_override(window=window, area=area, region=region):
                bpy.ops.mesh.select_all(action='SELECT')
        yield
        check(name + " dark before", lit(drawn(draw), idname)[:1] == [False], lit(drawn(draw), idname))
        redraws["count"] = 0
        result = press(idname, **props)
        yield
        check(name + " available", result is not None, result)
        running = tool_state.is_running(target)
        check(name + " runs", running, [op.bl_idname for op in view3d()[0].modal_operators])
        buttons = drawn(draw)
        check(name + " lit", lit(buttons, idname)[:1] == [True], lit(buttons, idname))
        for other in dark:
            check(name + ": " + other + " stays dark", not any(lit(buttons, other)), lit(buttons, other))
        check(name + " tells the panels", redraws["count"] > 0, redraws)
        key('ESC')
        yield
        yield
        check(name + " ended", not tool_state.is_running(target))
        check(name + " dark again", lit(drawn(draw), idname)[:1] == [False], lit(drawn(draw), idname))
        redraws["count"] = 0
        yield
        yield

    # Refine and Refine Connect: one operator, a setting apart, which the start from the panel keeps.
    for connect, expected in ((False, [True, False]), (True, [False, True])):
        set_mode('CURVE')
        yield
        check("Refine available from the panel", press("maximize.spline_refine", connect=connect) is not None)
        yield
        states = lit(drawn(spline_geometry), "maximize.spline_refine")
        check("Refine connect=" + str(connect) + " lights its own button", states == expected, states)
        key('ESC')
        yield

    # The Lights in the Create tab.
    set_mode('OBJECT')
    yield
    check("Light Plane dark before", not any(b.depress for b in drawn(ui.draw_object_types, 'LIGHTS')))
    press("maximize.create_in_viewport", operator="maximize.add_light", kind='PLANE')
    yield
    buttons = [b for b in drawn(ui.draw_object_types, 'LIGHTS') if b.idname == "maximize.create_in_viewport"]
    check("only the running Light is lit", [b.kind for b in buttons if b.depress] == ['PLANE'],
          [(b.kind, b.depress) for b in buttons])
    key('ESC')
    yield

    # Align from the Utilities tab.
    set_mode('OBJECT')
    window, area, region = view3d()
    with bpy.context.temp_override(window=window, area=area, region=region):
        bpy.ops.mesh.primitive_cube_add()
    yield
    check("Align available from the panel", press("maximize.align") is not None)
    yield
    check("Align lit", lit(drawn(ui.draw_utilities), "maximize.align")[:1] == [True])
    key('ESC')
    yield

    # Caddy style: the same buttons, with the settings square beside them.
    prefs = preferences.get_prefs(bpy.context)
    style = prefs.tool_settings_style
    prefs.tool_settings_style = 'CADDY'
    set_mode('MESH')
    set_level(2)
    yield
    press("maximize.hinge_from_edge")
    yield
    check("lit in Caddy style", lit(drawn(poly_level), "maximize.hinge_from_edge")[:1] == [True])
    key('ESC')
    yield
    prefs.tool_settings_style = style

    # The tools work in the 3D View after starting from the panel.
    set_mode('MESH')
    set_level(1)
    yield
    obj = bpy.context.active_object
    before = len(bmesh.from_edit_mesh(obj.data).verts)
    press("maximize.insert_vertex")
    yield
    # A cube fills little of the view: the edge nearest the middle is within the tool's reach.
    region = view3d()[2]
    for fx, fy in ((.5, .5), (.5, .55), (.55, .5), (.5, .45), (.45, .5)):
        window, x, y = click_view(fx, fy)
        yield
        window.event_simulate('LEFTMOUSE', 'PRESS', x=x, y=y)
        yield
        window.event_simulate('LEFTMOUSE', 'RELEASE', x=x, y=y)
        yield
    after = len(bmesh.from_edit_mesh(obj.data).verts)
    check("Insert Vertex from the panel clicks in the view", after > before, before, after)
    key('ESC')
    yield

    set_mode('CURVE')
    yield
    obj = bpy.context.active_object
    splines = len(obj.data.splines)
    # Create Line in Edit Mode, drawn from the panel, the button lit though the rollout is gone.
    check("Create Line available", press("maximize.spline_create_line") is not None)
    yield
    check("Create Line runs", tool_state.is_running("maximize.line", start_new_shape=False))
    with_panel = drawn(ui.draw_spline_rollouts, obj, "test", True)
    check("Create Line lit in Object Mode", lit(with_panel, "maximize.spline_create_line") == [True],
          lit(with_panel, "maximize.spline_create_line"))
    for fx, fy in ((.3, .3), (.7, .3)):
        window, x, y = click_view(fx, fy)
        yield
        window.event_simulate('LEFTMOUSE', 'PRESS', x=x, y=y)
        yield
        window.event_simulate('LEFTMOUSE', 'RELEASE', x=x, y=y)
        yield
    key('RIGHTMOUSE')
    yield
    yield
    check("Create Line added a spline to the shape", len(obj.data.splines) == splines + 1,
          splines, len(obj.data.splines))
    check("Create Line ended", not tool_state.is_running("maximize.line"))


def steps():
    yield from panel_steps()
    for idname, props, mode, pointer, ending in TOOLS:
        name = idname + " " + ending
        set_mode(mode)
        yield
        calls.update(begin=0, end=0)
        result = run(idname, **props)
        yield
        check(name + " started", 'RUNNING_MODAL' in result, result)
        check(name + " lit", tool_state.is_running(idname, **props))
        check(name + " pointer set", calls["begin"] == 1, calls)
        for key_prop, value in props.items():
            other = 'SPHERE' if value != 'SPHERE' else 'BOX'
            if key_prop == "kind":
                check(name + " another kind stays dark", not tool_state.is_running(idname, kind=other))
        key(ending)
        yield
        check(name + " dark again", not tool_state.is_running(idname, **props))
        check(name + " pointer restored", calls["end"] == 1, calls)
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


runner = None


def tick():
    try:
        next(runner)
    except StopIteration:
        return None
    except Exception:
        traceback.print_exc()
        say("FAILURES crashed")
        bpy.ops.wm.quit_blender()
        return None
    return 0.3


def start():
    global runner
    runner = steps()
    bpy.app.timers.register(tick, first_interval=0.0)
    return None


bpy.app.timers.register(start, first_interval=2.0)

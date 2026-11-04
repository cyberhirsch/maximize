# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_tool_state.py
# A running tool: its button is lit (`is_running`), the pointer is set on start and restored on the
# way out, and both end with Esc and with a right-click.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from maximize import tool_state

failures = []
calls = {"begin": 0, "end": 0}
real_begin, real_end = tool_state.begin, tool_state.end


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


def steps():
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
    return 0.3


def start():
    global runner
    runner = steps()
    bpy.app.timers.register(tick, first_interval=0.0)
    return None


bpy.app.timers.register(start, first_interval=2.0)

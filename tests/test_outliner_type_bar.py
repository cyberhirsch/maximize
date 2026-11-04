# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_outliner_type_bar.py
# The Outliner's show buttons in a vertical strip on its left edge, not in the header. A click
# toggles the filter, and the strip survives a save and reload.
import os
import sys
import tempfile

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from maximize import outliner

failures = []


def say(*a): print("MXOB", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)
    if not ok:
        failures.append(name)


def find():
    window = bpy.context.window_manager.windows[0]
    for area in window.screen.areas:
        if area.type == 'OUTLINER':
            bars = [r for r in area.regions if r.type == 'NAVIGATION_BAR']
            return window, area, bars
    return window, None, []


def click_mesh_button():
    window, area, bars = find()
    bar = bars[0]
    x = bar.x + bar.width // 2
    y = bar.y + bar.height - int(16 * bpy.context.preferences.system.ui_scale)
    window.event_simulate('MOUSEMOVE', 'NOTHING', x=x, y=y)
    return x, y


def mouse(kind, value):
    x, y = state["xy"]
    find()[0].event_simulate(kind, value, x=x, y=y)


state = {}


def steps():
    # Each yield hands control back so the events and redraws run.
    window, area, bars = find()
    check("the strip registered", outliner._has_type_bar)
    check("the Outliner has one strip", len(bars) == 1, len(bars))
    if not bars:
        return
    bar = bars[0]
    main = next(r for r in area.regions if r.type == 'WINDOW')
    check("the strip has a width", bar.width > 10, bar.width)
    check("it is on the left, beside the tree", bar.x == area.x and main.x >= bar.x + bar.width,
          bar.x, main.x, bar.width)
    check("it is narrow", bar.width < 80, bar.width)

    space = area.spaces.active
    before = space.use_filter_object_mesh
    state["xy"] = click_mesh_button()
    yield
    # The first simulated click after startup is dropped on any button, stock ones too.
    mouse('MOUSEMOVE', 'NOTHING')
    yield
    mouse('LEFTMOUSE', 'PRESS')
    yield
    mouse('LEFTMOUSE', 'RELEASE')
    yield
    check("the dropped click did nothing", space.use_filter_object_mesh == before)
    mouse('MOUSEMOVE', 'NOTHING')
    yield
    mouse('LEFTMOUSE', 'PRESS')
    yield
    mouse('LEFTMOUSE', 'RELEASE')
    yield
    check("a click on the top button toggles Geometry", space.use_filter_object_mesh != before,
          space.use_filter_object_mesh)
    space.use_filter_object_mesh = True

    path = os.path.join(tempfile.mkdtemp(prefix="moritz_type_bar"), "bar.blend")
    bpy.ops.wm.save_as_mainfile(filepath=path)
    state["path"] = path
    bpy.app.timers.register(reload_file, first_interval=0.0)


def reload_file():
    bpy.ops.wm.open_mainfile(filepath=state["path"])
    bpy.app.timers.register(after_reload, first_interval=1.0)
    return None


def after_reload():
    check("one strip after a reload", len(find()[2]) == 1)
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()
    return None


runner = None


def tick():
    try:
        next(runner)
    except StopIteration:
        return None
    return 0.5


def start():
    global runner
    runner = steps()
    bpy.app.timers.register(tick, first_interval=0.0)
    return None


bpy.app.timers.register(start, first_interval=2.0, persistent=True)

# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_line_handles.py
# Line: a dragged vertex shows both handles while the segment to the mouse stays straight; a plain
# click placed after it stays straight too; a second drag curves the segment between the two.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy
from maximize import spline_tools

failures = []
SHOT = os.environ.get("MX_SHOT")
drawn = []
shows_out = []
real_draw = spline_tools.MAXIMIZE_OT_line._draw


def counted_draw(self):
    drawn.append(len(self._shown))
    shows_out[:] = [self._shows_out(self._shown, index) for index in range(len(self._shown))]
    real_draw(self)


spline_tools.MAXIMIZE_OT_line._draw = counted_draw


def say(*a): print("MXLH", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)
    if not ok:
        failures.append(name)


def view3d():
    window = bpy.context.window_manager.windows[0]
    area = max((a for a in window.screen.areas if a.type == 'VIEW_3D'), key=lambda a: a.width * a.height)
    return window, area, next(r for r in area.regions if r.type == 'WINDOW')


def at(fx, fy):
    _window, _area, region = view3d()
    return region.x + int(region.width * fx), region.y + int(region.height * fy)


def mouse(kind, value, pos):
    view3d()[0].event_simulate(kind, value, x=pos[0], y=pos[1])


def points():
    obj = bpy.context.view_layer.objects.active
    return obj.data.splines[0].bezier_points


def steps():
    A, A2, B, C, C2 = at(.3, .4), at(.36, .55), at(.55, .4), at(.7, .55), at(.76, .7)
    window, area, region = view3d()
    with bpy.context.temp_override(window=window, area=area, region=region):
        bpy.ops.maximize.line('INVOKE_DEFAULT')
    yield
    # A drag: a Bezier vertex.
    mouse('MOUSEMOVE', 'NOTHING', A)
    yield
    mouse('LEFTMOUSE', 'PRESS', A)
    yield
    mouse('MOUSEMOVE', 'NOTHING', A2)
    yield
    mouse('LEFTMOUSE', 'RELEASE', A2)
    yield
    # Toward the next point: the preview runs straight, the handles stay visible.
    mouse('MOUSEMOVE', 'NOTHING', B)
    yield
    yield
    p = points()
    check("two points in the preview", len(p) == 2, len(p))
    check("the segment to the mouse stays straight", (p[0].handle_right - p[0].co).length < 1e-6,
          (p[0].handle_right - p[0].co).length)
    check("the curve keeps its incoming handle", (p[0].handle_left - p[0].co).length > 0.01,
          (p[0].handle_left - p[0].co).length)
    check("handles and points are drawn", bool(drawn) and drawn[-1] == 2, drawn[-3:])
    check("the last dragged vertex draws both handles", shows_out[:1] == [True], shows_out)
    if SHOT:
        with bpy.context.temp_override(window=window, area=area):
            bpy.ops.screen.screenshot_area(filepath=SHOT + "_preview.png")
    # A plain click, then a drag: the segment between them curves, with the first point's handle back.
    mouse('LEFTMOUSE', 'PRESS', B)
    yield
    mouse('LEFTMOUSE', 'RELEASE', B)
    yield
    p = points()
    check("a click stays a corner", p[1].handle_left_type == 'VECTOR', p[1].handle_left_type)
    check("a placed click makes the segment before it straight", (p[0].handle_right - p[0].co).length < 1e-6,
          (p[0].handle_right - p[0].co).length)
    mouse('MOUSEMOVE', 'NOTHING', C)
    yield
    mouse('LEFTMOUSE', 'PRESS', C)
    yield
    mouse('MOUSEMOVE', 'NOTHING', C2)
    yield
    yield
    p = points()
    check("dragging shows the new point's handle", (p[2].handle_right - p[2].co).length > 0.01,
          (p[2].handle_right - p[2].co).length)
    if SHOT:
        with bpy.context.temp_override(window=window, area=area):
            bpy.ops.screen.screenshot_area(filepath=SHOT + "_drag.png")
    mouse('LEFTMOUSE', 'RELEASE', C2)
    yield
    # A dragged vertex that follows a placed one: its incoming curve stays, the way on stays straight.
    mouse('MOUSEMOVE', 'NOTHING', B)
    yield
    yield
    p = points()
    check("the made curve keeps its incoming handle", (p[2].handle_left - p[2].co).length > 0.01,
          (p[2].handle_left - p[2].co).length)
    check("the way on stays straight", (p[2].handle_right - p[2].co).length < 1e-6,
          (p[2].handle_right - p[2].co).length)
    check("and draws both handles", shows_out[2:3] == [True], shows_out)
    mouse('RIGHTMOUSE', 'PRESS', C2)
    yield
    mouse('RIGHTMOUSE', 'RELEASE', C2)
    yield
    p = points()
    check("the finished line has 3 points", len(p) == 3, len(p))
    check("its first segment is still straight", (p[0].handle_right - p[0].co).length < 1e-6)
    check("the last vertex has both handles", (p[2].handle_right - p[2].co).length > 0.01 and
          (p[2].handle_left - p[2].co).length > 0.01)
    check("the handler is gone after the tool ends", not spline_tools.tool_state.is_running("maximize.line"))
    count = len(drawn)
    area.tag_redraw()
    yield
    yield
    check("nothing is drawn after the tool ends", len(drawn) == count, count, len(drawn))
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


runner = None


def tick():
    try:
        next(runner)
    except StopIteration:
        return None
    return 0.4


def start():
    global runner
    runner = steps()
    bpy.app.timers.register(tick, first_interval=0.0)
    return None


bpy.app.timers.register(start, first_interval=2.0)

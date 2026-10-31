# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_create_drag_grow.py
# (MX_KEYMAP=Max for the Max keymap; Moritz by default.)
# Seb: "when creating a teapot ... when you click and drag, you can make it bigger, and smaller, but
# not bigger again. it gets stuck." Every drag-created object grows, shrinks and grows again with
# its first drag.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy  # noqa: E402
from maximize import primitives  # noqa: E402
from maximize.keymaps import activate  # noqa: E402

KEYMAP = os.environ.get("MX_KEYMAP", "Moritz")
failures = []
P = {}


def say(*a): print("MXGROW", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", KEYMAP + ":", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def region(): return [r for r in area().regions if r.type == 'WINDOW'][int(os.environ.get("MX_REGION", "-1"))]
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)


KINDS = [k for k in primitives.STANDARD_PRIMITIVES + primitives.EXTENDED_PRIMITIVES
         if primitives.STEPS[k][0] in {'RECT', 'RADIUS'}]
if os.environ.get("MX_KINDS"):
    KINDS = os.environ["MX_KINDS"].split(",")
# How far in the shrink goes (pixels from the start) and how far out the second growth goes.
IN = [float(c) for c in os.environ.get("MX_IN", "30,18").split(",")]
OUT = [float(c) for c in os.environ.get("MX_OUT", "200,120").split(",")]


def size():
    obj = P.get('obj')
    if obj is None:
        new = [o for o in bpy.data.objects if o.name not in P['before']]
        if not new:
            return None
        obj = P['obj'] = new[0]
    if os.environ.get("MX_MEASURE") == "PARAM":
        return sum(primitives.parameter(obj, n).value for n in primitives.first_step_inputs(P['kind']))
    # What the viewport shows: the evaluated object's size.
    return max(obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).dimensions)


def move_to(dx, dy, steps=8):
    x0, y0 = P['at']
    for i in range(1, steps + 1):
        ev('MOUSEMOVE', 'NOTHING', x0 + (dx - x0) * i / steps, y0 + (dy - y0) * i / steps)
    P['at'] = (dx, dy)


def s_setup():
    activate(KEYMAP)
    ev('ESC', 'PRESS', 10, 10)
    ev('ESC', 'RELEASE', 10, 10)
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob)
    r = region()
    P['cx'], P['cy'] = r.x + r.width * 0.5, r.y + r.height * 0.5


def make_steps(kind):
    def start():
        P['kind'] = kind
        P['obj'] = None
        P['before'] = {o.name for o in bpy.data.objects}
        with bpy.context.temp_override(window=win(), area=area(), region=region()):
            bpy.ops.maximize.add_primitive('INVOKE_DEFAULT', kind=kind)
        cx, cy = P['cx'], P['cy']
        P['at'] = (cx, cy)
        ev('MOUSEMOVE', 'NOTHING', cx, cy)
        ev('LEFTMOUSE', 'PRESS', cx, cy)
        move_to(cx + 120, cy + 70)

    def grown():
        P['s1'] = size()
        move_to(P['cx'] + IN[0], P['cy'] + IN[1])

    def shrunk():
        P['s2'] = size()
        move_to(P['cx'] + OUT[0], P['cy'] + OUT[1])

    def regrown():
        P['s3'] = size()
        s1, s2, s3 = P['s1'], P['s2'], P['s3']
        ok = None not in (s1, s2, s3) and s2 < s1 < s3
        check(kind + " grows, shrinks and grows again", ok,
              *(round(s, 3) if s is not None else None for s in (s1, s2, s3)))
        ev('ESC', 'PRESS', *P['at'])
        ev('ESC', 'RELEASE', *P['at'])
        ev('LEFTMOUSE', 'RELEASE', *P['at'])
    return [start, grown, shrunk, regrown]


def s_end():
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_setup] + [s for k in KINDS for s in make_steps(k)] + [s_end]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say("ERR", repr(e))
    return 0.4 if steps else None


bpy.app.timers.register(run, first_interval=2.0)

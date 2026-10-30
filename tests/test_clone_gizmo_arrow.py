# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_clone_gizmo_arrow.py
# (MX_KEYMAP=Max for the Max keymap; Moritz by default.)
# Shift+drag on a Move gizmo arrow in Object Mode clones, and the clone moves along that arrow, as in
# Max (Blender's gizmo would turn Shift+arrow into a move in the plane across it).
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy  # noqa: E402
from bpy_extras import view3d_utils  # noqa: E402
from mathutils import Vector  # noqa: E402
from maximize.keymaps import activate  # noqa: E402

KEYMAP = os.environ.get("MX_KEYMAP", "Moritz")
failures = []


def say(*a): print("MXCA", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", KEYMAP + ":", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def region(): return [r for r in area().regions if r.type == 'WINDOW'][-1]
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)


P = {}


def s_setup():
    activate(KEYMAP)
    ev('ESC', 'PRESS', 10, 10)
    ev('ESC', 'RELEASE', 10, 10)


def s_tool():
    r = region()
    bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
    with bpy.context.temp_override(window=win(), area=area(), region=r):
        bpy.ops.wm.tool_set_by_id(name="builtin.move")
    obj = bpy.context.active_object
    P['names'] = set(bpy.data.objects.keys())
    P['start'] = obj.matrix_world.translation.copy()
    rv3d = r.data
    c2 = view3d_utils.location_3d_to_region_2d(r, rv3d, P['start'])

    def screen_dir(axis):
        return view3d_utils.location_3d_to_region_2d(r, rv3d, P['start'] + axis * 0.5) - c2
    # X: in the default view the Y and Z arrows lie close together on screen.
    axis = Vector((1, 0, 0))
    P['axis'] = axis
    co = c2 + screen_dir(axis).normalized() * 55 * bpy.context.preferences.system.ui_scale
    P['x'], P['y'] = r.x + co.x, r.y + co.y
    say("arrow", tuple(axis))


def s_drag():
    x, y = P['x'], P['y']
    ev('MOUSEMOVE', 'NOTHING', x, y)
    ev('LEFT_SHIFT', 'PRESS', x, y, shift=True)
    ev('LEFTMOUSE', 'PRESS', x, y, shift=True)
    for i in range(1, 8):
        ev('MOUSEMOVE', 'NOTHING', x + i * 9, y + i * 4, shift=True)


def s_release():
    for i in range(8, 13):
        ev('MOUSEMOVE', 'NOTHING', P['x'] + i * 9, P['y'] + i * 4, shift=True)
    ev('LEFTMOUSE', 'RELEASE', P['x'] + 108, P['y'] + 48, shift=True)
    ev('LEFT_SHIFT', 'RELEASE', P['x'] + 108, P['y'] + 48)


def s_confirm():
    # The Clone Options dialog: OK.
    ev('RET', 'PRESS', P['x'] + 108, P['y'] + 48)
    ev('RET', 'RELEASE', P['x'] + 108, P['y'] + 48)


def s_check():
    new = set(bpy.data.objects.keys()) - P['names']
    check("a clone was made", len(new) == 1, sorted(new))
    if new:
        clone = bpy.data.objects[new.pop()]
        moved = clone.matrix_world.translation - P['start']
        d = moved.normalized() if moved.length > 1e-6 else Vector()
        check("the clone moved along the arrow", moved.length > 0.05 and abs(d.dot(P['axis'])) > 0.99,
              "moved", tuple(round(x, 3) for x in moved))
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_setup, s_tool, s_drag, s_release, s_confirm, s_check]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say("ERR", repr(e))
    return 0.6 if steps else None


bpy.app.timers.register(run, first_interval=2.0)

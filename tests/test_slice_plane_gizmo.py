# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_slice_plane_gizmo.py
# (MX_SHOT=<file.png> also saves a screenshot with the plane shown.)
# Slice Plane's move handle (Seb: "what is that white sphere?"): a big white disk drawn at twice the
# plane's position. It must sit on the plane, and a drag must move the plane with the mouse.
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy  # noqa: E402
from bpy_extras import view3d_utils  # noqa: E402
from mathutils import Vector  # noqa: E402

failures = []
P = {}


def say(*a): print("MXSP", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def region(): return [r for r in area().regions if r.type == 'WINDOW'][-1]
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)


def s_setup():
    ev('ESC', 'PRESS', 10, 10)
    ev('ESC', 'RELEASE', 10, 10)
    obj = bpy.context.active_object
    obj.location = (0.0, 0.0, 2.0)
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.maximize.slice_plane_mode(action='TOGGLE')
        bpy.ops.view3d.view_axis(type='FRONT')
        bpy.ops.view3d.view_all()
    wm = bpy.context.window_manager
    check("the plane is shown through the selection", wm.maximize_slice_active and
          (Vector(wm.maximize_slice_location) - Vector((0, 0, 2))).length < 1e-4,
          tuple(wm.maximize_slice_location))


def s_shot():
    if os.environ.get("MX_SHOT"):
        with bpy.context.temp_override(window=win()):
            bpy.ops.screen.screenshot(filepath=os.environ["MX_SHOT"])
    r = region()
    wm = bpy.context.window_manager
    co = view3d_utils.location_3d_to_region_2d(r, r.data, Vector(wm.maximize_slice_location))
    P['start'] = Vector(wm.maximize_slice_location)
    P['x'], P['y'] = r.x + co.x, r.y + co.y
    # Grab the handle where the plane is, not where it used to be drawn (twice as far up).
    ev('MOUSEMOVE', 'NOTHING', P['x'], P['y'])


def s_press():
    ev('LEFTMOUSE', 'PRESS', P['x'], P['y'])
    for i in range(1, 11):
        ev('MOUSEMOVE', 'NOTHING', P['x'] + i * 4, P['y'] + i * 3)


def s_release():
    # More moves once the gizmo's tweak runs, as a real drag keeps moving.
    for i in range(11, 21):
        ev('MOUSEMOVE', 'NOTHING', P['x'] + i * 4, P['y'] + i * 3)
    P['dx'], P['dy'] = 80, 60
    say("during", [op.bl_idname for op in win().modal_operators], tuple(bpy.context.window_manager.maximize_slice_location), tuple(bpy.context.window_manager.maximize_slice_rotation))
    ev('LEFTMOUSE', 'RELEASE', P['x'] + 80, P['y'] + 60)


def s_check():
    r = region()
    wm = bpy.context.window_manager
    end = Vector(wm.maximize_slice_location)
    moved = view3d_utils.location_3d_to_region_2d(r, r.data, end) - \
        view3d_utils.location_3d_to_region_2d(r, r.data, P['start'])
    check("a drag on the handle at the plane moves the plane with the mouse",
          (moved - Vector((P['dx'], P['dy']))).length < 3.0, "screen move", tuple(round(c, 1) for c in moved))
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_setup, s_shot, s_press, s_release, s_check]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say("ERR", repr(e))
    return 0.6 if steps else None


bpy.app.timers.register(run, first_interval=2.0)

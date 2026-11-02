# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_view_fly.py
# (MX_KEYMAP=Max for the Max keymap; Moritz by default.)
# Middle mouse: pans as before; held with W A S D it flies (Q E down / up), the wheel sets the speed
# (Seb: "when i hold middle mouse button and use wasd for camera controls", "holding middle mouse +
# scrolling to increase or decrease speed", "also add up and down").
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
from maximize.keymaps import activate  # noqa: E402

KEYMAP = os.environ.get("MX_KEYMAP", "Moritz")
failures = []


def say(*a): print("MXFLY", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", KEYMAP + ":", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(): return max((a for a in win().screen.areas if a.type == 'VIEW_3D'), key=lambda a: a.width * a.height)
def region(): return [r for r in area().regions if r.type == 'WINDOW'][-1]
def rv3d():
    """The view under the test's mouse (the new-file layout may have made a quad view)."""
    for r in area().regions:
        if r.type == 'WINDOW' and r.x <= P.get('x', -1) < r.x + r.width and r.y <= P.get('y', -1) < r.y + r.height:
            return r.data
    return region().data
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)


def eye():
    r = rv3d()
    return r.view_location + r.view_rotation @ Vector((0.0, 0.0, r.view_distance))


def forward():
    return rv3d().view_rotation @ Vector((0.0, 0.0, -1.0))


def modal():
    return [op.bl_idname for op in win().modal_operators]


P = {}


def s_setup():
    activate(KEYMAP)
    ev('ESC', 'PRESS', 10, 10)
    ev('ESC', 'RELEASE', 10, 10)
    space = area().spaces.active
    if space.region_quadviews:
        with bpy.context.temp_override(window=win(), area=area(), region=region()):
            bpy.ops.screen.region_quadview()
    r = rv3d()
    r.view_perspective = 'PERSP'
    bpy.context.preferences.inputs.walk_navigation.walk_speed = 2.0
    reg = region()
    P['x'], P['y'] = reg.x + reg.width // 2, reg.y + reg.height // 2
    ev('MOUSEMOVE', 'NOTHING', P['x'], P['y'])


def s_pan_press():
    P['loc'], P['rot'] = rv3d().view_location.copy(), rv3d().view_rotation.copy()
    ev('MIDDLEMOUSE', 'PRESS', P['x'], P['y'])


def s_pan_move():
    # A step after the press: simulated events queued with it would start the pan at the last one.
    for i in range(1, 6):
        ev('MOUSEMOVE', 'NOTHING', P['x'] + i * 10, P['y'])


def s_pan_release():
    say("during pan", modal())
    check("middle mouse pans", (rv3d().view_location - P['loc']).length > 1e-3
          and rv3d().view_rotation.rotation_difference(P['rot']).angle < 1e-5,
          tuple(round(c, 3) for c in rv3d().view_location - P['loc']))
    ev('MIDDLEMOUSE', 'RELEASE', P['x'] + 50, P['y'])


def s_pan_done():
    check("the pan ends on release", not modal(), modal())
    P['loc'] = rv3d().view_location.copy()
    ev('MOUSEMOVE', 'NOTHING', P['x'] + 80, P['y'])


def s_pan_stays():
    check("no pan after the release", (rv3d().view_location - P['loc']).length < 1e-6)
    ev('MOUSEMOVE', 'NOTHING', P['x'], P['y'])


def s_fly_press():
    P['eye'], P['fwd'] = eye(), forward()
    ev('MIDDLEMOUSE', 'PRESS', P['x'], P['y'])
    ev('W', 'PRESS', P['x'], P['y'])


def s_fly_mid():
    say("flying", modal(), "header")
    moved = eye() - P['eye']
    check("W flies forward", moved.length > 0.05 and moved.normalized().dot(P['fwd']) > 0.99,
          round(moved.length, 3), round(moved.normalized().dot(P['fwd']), 4) if moved.length else 0)
    ev('W', 'RELEASE', P['x'], P['y'])
    P['eye'] = eye()
    ev('E', 'PRESS', P['x'], P['y'])


def s_fly_up():
    moved = eye() - P['eye']
    check("E flies up", moved.length > 0.05 and moved.normalized().z > 0.99, tuple(round(c, 3) for c in moved))
    ev('E', 'RELEASE', P['x'], P['y'])
    P['speed'] = bpy.context.preferences.inputs.walk_navigation.walk_speed
    ev('WHEELUPMOUSE', 'PRESS', P['x'], P['y'])
    P['fwd'] = forward()
    P['eye'] = eye()
    ev('MOUSEMOVE', 'NOTHING', P['x'] + 40, P['y'] + 20)


def s_fly_look():
    speed = bpy.context.preferences.inputs.walk_navigation.walk_speed
    check("the wheel speeds up", abs(speed - P['speed'] * 1.25) < 1e-4, P['speed'], "->", speed)
    f = forward()
    check("the mouse looks around (right and up)", f.cross(P['fwd']).length > 0.01 and f.z > P['fwd'].z,
          tuple(round(c, 3) for c in f))
    check("looking keeps the eye in place", (eye() - P['eye']).length < 1e-4)
    P['before_release'] = (rv3d().view_location.copy(), rv3d().view_rotation.copy())
    ev('MIDDLEMOUSE', 'RELEASE', P['x'], P['y'])


def s_fly_done():
    check("flying ends on release", not modal(), modal())
    loc, rot = P['before_release']
    check("the view stays where it flew", (rv3d().view_location - loc).length < 1e-5)
    # Q flies down; Esc puts the view back.
    P['loc'], P['rot'] = rv3d().view_location.copy(), rv3d().view_rotation.copy()
    ev('MIDDLEMOUSE', 'PRESS', P['x'], P['y'])
    ev('Q', 'PRESS', P['x'], P['y'])


def s_cancel():
    check("Q flies down", rv3d().view_location.z < P['loc'].z - 0.05, round(rv3d().view_location.z - P['loc'].z, 3))
    ev('ESC', 'PRESS', P['x'], P['y'])
    ev('ESC', 'RELEASE', P['x'], P['y'])
    ev('Q', 'RELEASE', P['x'], P['y'])
    ev('MIDDLEMOUSE', 'RELEASE', P['x'], P['y'])


def s_cancel_check():
    check("Esc puts the view back", (rv3d().view_location - P['loc']).length < 1e-4,
          round((rv3d().view_location - P['loc']).length, 4))
    check("and nothing keeps running", not modal(), modal())
    # Through a camera, the camera flies (as Walk Navigation), with one undo step.
    rv3d().view_perspective = 'CAMERA'
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.ed.undo_push(message="Camera view")
    P['cam'] = bpy.context.scene.camera.matrix_world.copy()
    ev('MIDDLEMOUSE', 'PRESS', P['x'], P['y'])


def s_camera_w():
    ev('W', 'PRESS', P['x'], P['y'])


def s_camera_release():
    ev('W', 'RELEASE', P['x'], P['y'])
    ev('MIDDLEMOUSE', 'RELEASE', P['x'], P['y'])


def s_check():
    cam = bpy.context.scene.camera
    fwd = P['cam'].to_quaternion() @ Vector((0.0, 0.0, -1.0))
    moved = cam.matrix_world.translation - P['cam'].translation
    check("through a camera the camera flies forward", moved.length > 0.05 and moved.normalized().dot(fwd) > 0.99,
          round(moved.length, 3))
    check("still looking through it", rv3d().view_perspective == 'CAMERA', rv3d().view_perspective)
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.ed.undo()
    cam = bpy.context.scene.camera
    check("one undo puts the camera back", (cam.matrix_world.translation - P['cam'].translation).length < 1e-5)
    check("nothing keeps running", not modal(), modal())
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_setup, s_pan_press, s_pan_move, s_pan_release, s_pan_done, s_pan_stays, s_fly_press, s_fly_mid, s_fly_up,
         s_fly_look, s_fly_done, s_cancel, s_cancel_check, s_camera_w, s_camera_release, s_check]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say("ERR", repr(e))
    return 0.6 if steps else None


bpy.app.timers.register(run, first_interval=2.0)

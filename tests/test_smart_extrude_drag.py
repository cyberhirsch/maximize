# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_smart_extrude_drag.py
# (MX_KEYMAP=Max for the Max keymap; Moritz by default; MX_GIZMO=1 drags the Move gizmo's arrow;
# MX_NO_EDIT_STEP=1: the Move is the first undo step in Edit Mode.)
# Shift+drag of polygons with the Move tool: Smart Extrude stays after the release (Seb: "when i
# release it snaps back to the before state").
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bmesh  # noqa: E402
import bpy  # noqa: E402
from bpy_extras import view3d_utils  # noqa: E402
from maximize.keymaps import activate  # noqa: E402

KEYMAP = os.environ.get("MX_KEYMAP", "Moritz")
GIZMO = os.environ.get("MX_GIZMO") == "1"
failures = []


def say(*a): print("MXSE", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", KEYMAP + (" gizmo" if GIZMO else "") + ":", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(): return next(a for a in win().screen.areas if a.type == 'VIEW_3D')
def region(): return [r for r in area().regions if r.type == 'WINDOW'][-1]
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)


P = {}


def counts():
    me = bpy.context.active_object.data
    if bpy.context.mode == 'EDIT_MESH':
        bm = bmesh.from_edit_mesh(me)
        return len(bm.verts), len(bm.faces)
    return len(me.vertices), len(me.polygons)


def s_setup():
    activate(KEYMAP)
    ev('ESC', 'PRESS', 10, 10)
    ev('ESC', 'RELEASE', 10, 10)


def s_edit():
    r = region()
    with bpy.context.temp_override(window=win(), area=area(), region=r):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.wm.tool_set_by_id(name="builtin.move")
        if os.environ.get("MX_NO_EDIT_STEP") != "1":
            # Tab makes an undo step on entering Edit Mode; the script call above does not.
            bpy.ops.ed.undo_push(message="Toggle Edit Mode")
    obj = bpy.context.active_object
    bm = bmesh.from_edit_mesh(obj.data)
    # The face toward the viewer.
    rv3d = r.data
    from mathutils import Vector
    view = rv3d.view_rotation @ Vector((0, 0, 1))
    normal_world = obj.matrix_world.to_3x3()
    face = max(bm.faces, key=lambda f: (normal_world @ f.normal).dot(view))
    face.select = True
    bm.select_flush(True)
    bmesh.update_edit_mesh(obj.data)
    center = obj.matrix_world @ face.calc_center_median()
    c2 = view3d_utils.location_3d_to_region_2d(r, rv3d, center)
    if GIZMO:
        # Along the Move gizmo's arrow that shows longest on screen.
        def screen_dir(axis):
            d = view3d_utils.location_3d_to_region_2d(r, rv3d, center + axis * 0.1) - c2
            return d
        d = max((screen_dir(Vector(a)) for a in ((1, 0, 0), (0, 1, 0), (0, 0, 1))), key=lambda d: d.length)
        co = c2 + d.normalized() * 55 * bpy.context.preferences.system.ui_scale
    else:
        # On the face, away from the gizmo's center ring.
        corner = view3d_utils.location_3d_to_region_2d(r, rv3d, obj.matrix_world @ face.verts[0].co)
        co = c2.lerp(corner, 0.6)
    P['x'], P['y'] = r.x + co.x, r.y + co.y
    P['before'] = counts()
    say("before", P['before'], "tool", bpy.context.workspace.tools.from_space_view3d_mode('EDIT_MESH').idname)


def s_drag():
    x, y = P['x'], P['y']
    ev('MOUSEMOVE', 'NOTHING', x, y)
    # Shift held as a key: the click-drag event takes its modifiers from the key state.
    ev('LEFT_SHIFT', 'PRESS', x, y, shift=True)
    ev('LEFTMOUSE', 'PRESS', x, y, shift=True)
    for i in range(1, 8):
        ev('MOUSEMOVE', 'NOTHING', x + i * 6, y + i * 8, shift=True)


def s_mid():
    say("during", counts(), [op.bl_idname for op in win().modal_operators])
    ev('LEFTMOUSE', 'RELEASE', P['x'] + 42, P['y'] + 56, shift=True)
    ev('LEFT_SHIFT', 'RELEASE', P['x'] + 42, P['y'] + 56)


def s_wait():
    say("after release", counts())


def s_check():
    after = counts()
    check("the extrusion stays after the release", after != P['before'] and after[1] > P['before'][1],
          P['before'], "->", after)
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.ed.undo()
    check("one undo takes it away", counts() == P['before'], counts())
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_setup, s_edit, s_drag, s_mid, s_wait, s_wait, s_check]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say("ERR", repr(e))
    return 0.6 if steps else None


bpy.app.timers.register(run, first_interval=2.0)

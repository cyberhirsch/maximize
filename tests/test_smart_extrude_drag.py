# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_smart_extrude_drag.py
# (MX_KEYMAP=Max for the Max keymap; Moritz by default; MX_GIZMO=ARROW drags the Move gizmo's arrow,
# MX_GIZMO=RING its center ring; MX_NO_EDIT_STEP=1: the Move is the first undo step in Edit Mode.)
# Shift+drag of polygons with the Move tool: Smart Extrude stays after the release (Seb: "when i
# release it snaps back to the before state"), also from the gizmo's ring, and with an arrow it goes
# along that arrow in the Transform Orientation (Global here, on a tilted cube), not the normal.
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
# MX_TOOL=rotate / scale: Shift+drag with the Rotate or Scale tool (Seb: "smart extrude should also
# work in scale and rotate").
TOOL = os.environ.get("MX_TOOL", "move")
GIZMO = {"1": "ARROW"}.get(os.environ.get("MX_GIZMO", ""), os.environ.get("MX_GIZMO", ""))
failures = []


def say(*a): print("MXSE", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", KEYMAP + " " + TOOL + (" " + GIZMO.lower() if GIZMO else "") + ":", name, *info)
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
    from mathutils import Vector
    r = region()
    obj = bpy.context.active_object
    # Tilted, so no Global axis lies along a face normal.
    obj.rotation_euler = (0.35, 0.0, 0.5)
    bpy.context.view_layer.update()
    bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
    with bpy.context.temp_override(window=win(), area=area(), region=r):
        # A rotation by hand has its undo step; the one by script would be undone with the drag.
        bpy.ops.ed.undo_push(message="Rotate")
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.wm.tool_set_by_id(name="builtin." + TOOL)
        if os.environ.get("MX_NO_EDIT_STEP") != "1":
            # Tab makes an undo step on entering Edit Mode; the script call above does not.
            bpy.ops.ed.undo_push(message="Toggle Edit Mode")
    bm = bmesh.from_edit_mesh(obj.data)
    rv3d = r.data
    view = rv3d.view_rotation @ Vector((0, 0, 1))
    normal_world = obj.matrix_world.to_3x3()
    face = max(bm.faces, key=lambda f: (normal_world @ f.normal).normalized().dot(view))
    face.select = True
    bm.select_flush(True)
    bmesh.update_edit_mesh(obj.data)
    center = obj.matrix_world @ face.calc_center_median()
    P['center'] = center
    P['normal'] = (normal_world @ face.normal).normalized()
    P['area'] = face.calc_area()
    c2 = view3d_utils.location_3d_to_region_2d(r, rv3d, center)
    if GIZMO == 'ARROW':
        # The Global arrow nearest the face normal (but off it), long enough on screen to grab.
        def screen_dir(axis):
            return view3d_utils.location_3d_to_region_2d(r, rv3d, center + axis * 0.5) - c2
        axes = [Vector(a) for a in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
        axis = max((a for a in axes if screen_dir(a).length > 0.4 * max(screen_dir(b).length for b in axes)),
                   key=lambda a: abs(a.dot(P['normal'])))
        P['axis'] = axis
        co = c2 + screen_dir(axis).normalized() * 55 * bpy.context.preferences.system.ui_scale
        say("arrow", tuple(axis), "normal . axis", round(abs(axis.dot(P['normal'])), 3))
    elif GIZMO == 'PLANE':
        # The plane handle of the two Global axes across the view: a small square on their
        # diagonal, 0.8 gizmo units out (Blender's MAN_AXIS_SCALE_PLANE_SCALE 0.7 + 0.1).
        view = rv3d.view_rotation @ Vector((0, 0, 1))
        axes = [Vector(a) for a in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
        normal_axis = max(axes, key=lambda a: abs(a.dot(view)))
        u, v = [a for a in axes if a is not normal_axis]
        # World units per gizmo unit at the center (the gizmo keeps its size on screen).
        right = rv3d.view_rotation @ Vector((1, 0, 0))
        ppu = (view3d_utils.location_3d_to_region_2d(r, rv3d, center + right) - c2).length
        unit = bpy.context.preferences.view.gizmo_size * bpy.context.preferences.system.ui_scale / ppu
        point = center + (u + v).normalized() * 0.8 * unit
        co = view3d_utils.location_3d_to_region_2d(r, rv3d, point)
        P['plane_normal'] = normal_axis
        say("plane across", tuple(normal_axis))
    elif GIZMO == 'RING':
        co = c2
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
    # More moves once the drag has started, as a real drag keeps moving.
    for i in range(8, 13):
        ev('MOUSEMOVE', 'NOTHING', P['x'] + i * 6, P['y'] + i * 8, shift=True)
    ev('LEFTMOUSE', 'RELEASE', P['x'] + 72, P['y'] + 96, shift=True)
    ev('LEFT_SHIFT', 'RELEASE', P['x'] + 42, P['y'] + 56)


def s_wait():
    say("after release", counts())


def s_check():
    after = counts()
    check("the extrusion stays after the release", after != P['before'] and after[1] > P['before'][1],
          P['before'], "->", after)
    if TOOL != "move":
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        cap = [f for f in bm.faces if f.select]
        normal = sum(((obj.matrix_world.to_3x3() @ f.normal) for f in cap), P['center'] * 0).normalized()
        cap_area = sum(f.calc_area() for f in cap)
        if TOOL == "rotate":
            check("the cap is turned", len(cap) > 0 and normal.dot(P['normal']) < 0.999,
                  "normal . before", round(normal.dot(P['normal']), 4))
        else:
            check("the cap is scaled", len(cap) > 0 and abs(cap_area - P['area']) > 1e-3 * P['area'],
                  "area", round(P['area'], 4), "->", round(cap_area, 4))
    if 'axis' in P:
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        cap = [obj.matrix_world @ f.calc_center_median() for f in bm.faces if f.select]
        moved = (sum(cap, P['center'] * 0) / max(len(cap), 1)) - P['center']
        d = moved.normalized()
        check("along the arrow, not the normal", len(cap) > 0 and abs(d.dot(P['axis'])) > 0.99,
              "dir . axis", round(abs(d.dot(P['axis'])), 3), "dir . normal", round(abs(d.dot(P['normal'])), 3))
    if 'plane_normal' in P:
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        cap = [obj.matrix_world @ f.calc_center_median() for f in bm.faces if f.select]
        moved = (sum(cap, P['center'] * 0) / max(len(cap), 1)) - P['center']
        across = abs(moved.dot(P['plane_normal']))
        in_plane = (moved - P['plane_normal'] * moved.dot(P['plane_normal']))
        check("in the handle's plane, on both of its axes", len(cap) > 0 and across < 1e-4 and
              min(abs(c) for i, c in enumerate(in_plane) if P['plane_normal'][i] == 0) > 1e-3,
              "moved", tuple(round(c, 3) for c in moved))
        # Not held to the handle's diagonal (what treating it as an arrow did).
        from mathutils import Vector
        diagonal = Vector([0.0 if c else 1.0 for c in P['plane_normal']]).normalized()
        check("a free move in the plane, not along the handle", abs(moved.normalized().dot(diagonal)) < 0.999,
              round(abs(moved.normalized().dot(diagonal)), 4))
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

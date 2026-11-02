# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_lights.py
# Lights in the Create tab, dragged out like V-Ray's Plane, Disc and Sphere lights (Seb: "add vray
# style area lights, that can be clicked and dragged to the create panel").
import os
import sys

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy  # noqa: E402
from bpy_extras import view3d_utils  # noqa: E402
from mathutils import Vector  # noqa: E402

failures = []


def say(*a): print("MXLT", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(): return max((a for a in win().screen.areas if a.type == 'VIEW_3D'), key=lambda a: a.width * a.height)
def ev(t, v, x, y, **k): win().event_simulate(type=t, value=v, x=int(x), y=int(y), **k)


def region():
    """The view the test drags in: the one at the area's center (the layout may make a quad view)."""
    a = area()
    cx, cy = a.x + a.width // 2, a.y + a.height // 2
    regions = [r for r in a.regions if r.type == 'WINDOW']
    return min(regions, key=lambda r: abs(r.x + r.width / 2 - cx) + abs(r.y + r.height / 2 - cy))


P = {}


def ground(x, y):
    """The ground point under window position (x, y)."""
    r = region()
    co = (x - r.x, y - r.y)
    origin = view3d_utils.region_2d_to_origin_3d(r, r.data, co)
    d = view3d_utils.region_2d_to_vector_3d(r, r.data, co)
    return origin + d * (-origin.z / d.z)


def start(shape):
    a, r = area(), region()
    with bpy.context.temp_override(window=win(), area=a, region=r):
        bpy.ops.maximize.add_light('INVOKE_DEFAULT', shape=shape)


def drag(x0, y0, x1, y1):
    ev('MOUSEMOVE', 'NOTHING', x0, y0)
    ev('LEFTMOUSE', 'PRESS', x0, y0)
    for i in range(1, 6):
        ev('MOUSEMOVE', 'NOTHING', x0 + (x1 - x0) * i / 5, y0 + (y1 - y0) * i / 5)
    ev('LEFTMOUSE', 'RELEASE', x1, y1)


def shines(obj):
    return obj.matrix_world.to_3x3() @ Vector((0.0, 0.0, -1.0))


def s_setup():
    ev('ESC', 'PRESS', 10, 10)
    ev('ESC', 'RELEASE', 10, 10)
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob)
    if area().spaces.active.region_quadviews:
        with bpy.context.temp_override(window=win(), area=area(), region=region()):
            bpy.ops.screen.region_quadview()
    r = region()
    with bpy.context.temp_override(window=win(), area=area(), region=r):
        bpy.ops.view3d.view_axis(type='TOP')
    P['cx'], P['cy'] = r.x + r.width // 2, r.y + r.height // 2


def s_plane():
    start('PLANE')
    x, y = P['cx'], P['cy']
    drag(x, y, x + 120, y + 60)
    P['plane'] = (ground(x, y), ground(x + 120, y + 60))


def s_plane_check():
    lights = [o for o in bpy.data.objects if o.type == 'LIGHT']
    check("a plane light", len(lights) == 1 and lights[0].data.type == 'AREA' and lights[0].data.shape == 'RECTANGLE',
          [(o.name, o.data.type) for o in lights])
    if lights:
        o = lights[0]
        a, b = P['plane']
        check("its size follows the drag", abs(o.data.size - abs(b.x - a.x)) < 1e-3 and
              abs(o.data.size_y - abs(b.y - a.y)) < 1e-3, round(o.data.size, 3), round(o.data.size_y, 3))
        check("centered on the rectangle", (o.matrix_world.translation - (a + b) / 2).length < 1e-3)
        check("shines down from the top view", shines(o).z < -0.999, tuple(round(c, 3) for c in shines(o)))
        check("named like Max", o.name == "PlaneLight001", o.name)
        check("the Create tab shows it", bpy.context.window_manager.maximize_created == o.name)
        check("bright enough", o.data.energy == 100.0, o.data.energy)
        P['plane_obj'] = o.name
    # Still in create mode: a click without a drag makes nothing; then a disc.
    ev('LEFTMOUSE', 'PRESS', P['cx'] - 100, P['cy'])
    ev('LEFTMOUSE', 'RELEASE', P['cx'] - 100, P['cy'])
    ev('RIGHTMOUSE', 'PRESS', P['cx'], P['cy'])
    ev('RIGHTMOUSE', 'RELEASE', P['cx'], P['cy'])


def s_disc():
    check("a click makes nothing", sum(o.type == 'LIGHT' for o in bpy.data.objects) == 1)
    start('DISC')
    x, y = P['cx'] - 150, P['cy'] - 80
    drag(x, y, x + 40, y + 30)
    P['disc'] = (ground(x, y), ground(x + 40, y + 30))


def s_disc_check():
    o = bpy.data.objects.get("DiscLight001")
    check("a disc light", o is not None and o.data.shape == 'DISK')
    if o:
        a, b = P['disc']
        check("its diameter is twice the drag", abs(o.data.size - 2 * (b - a).length) < 1e-3,
              round(o.data.size, 3), round(2 * (b - a).length, 3))
        check("centered where the drag began", (o.matrix_world.translation - a).length < 1e-3)
    ev('ESC', 'PRESS', P['cx'], P['cy'])
    ev('ESC', 'RELEASE', P['cx'], P['cy'])


def s_sphere():
    start('SPHERE')
    x, y = P['cx'] + 150, P['cy'] - 80
    drag(x, y, x + 30, y)
    P['sphere'] = (ground(x, y), ground(x + 30, y))


def s_sphere_check():
    o = bpy.data.objects.get("SphereLight001")
    check("a sphere light (a point light with a radius)", o is not None and o.data.type == 'POINT')
    if o:
        a, b = P['sphere']
        check("its radius follows the drag", abs(o.data.shadow_soft_size - (b - a).length) < 1e-3,
              round(o.data.shadow_soft_size, 3))
    ev('ESC', 'PRESS', P['cx'], P['cy'])
    ev('ESC', 'RELEASE', P['cx'], P['cy'])


def s_autogrid():
    # AutoGrid on a box's top: the light shines up, away from it.
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, -1.0))
    bpy.context.scene.maximize_autogrid = True
    # A perspective view from above, so the ray hits the box top.
    # Drag over the box's top (around the world origin, seen from the top view).
    reg = region()
    o = view3d_utils.location_3d_to_region_2d(reg, reg.data, Vector((0.0, 0.0, 0.0)))
    x, y = reg.x + o.x, reg.y + o.y
    start('PLANE')
    drag(x - 10, y - 10, x + 20, y + 15)


def s_autogrid_check():
    o = bpy.data.objects.get("PlaneLight002")
    check("an AutoGrid plane light", o is not None)
    if o:
        check("on the box's top", abs(o.matrix_world.translation.z) < 1e-3, round(o.matrix_world.translation.z, 4))
        check("shines away from the surface", shines(o).z > 0.999, tuple(round(c, 3) for c in shines(o)))
    ev('ESC', 'PRESS', P['cx'], P['cy'])
    ev('ESC', 'RELEASE', P['cx'], P['cy'])


def s_target():
    o = bpy.data.objects[P['plane_obj']]
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.maximize.light_target()
    t = o.constraints.get("Target")
    check("Targeted adds a target", t is not None and t.target is not None and t.target.type == 'EMPTY')
    if t and t.target:
        t.target.location = o.matrix_world.translation + Vector((3.0, 0.0, 0.0))
        bpy.context.view_layer.update()
        check("and the light aims at it", shines(o).dot(Vector((1, 0, 0))) > 0.999,
              tuple(round(c, 3) for c in shines(o)))
    name = t.target.name if t and t.target else ""
    bpy.ops.maximize.light_target()
    check("again removes it", o.constraints.get("Target") is None and name not in bpy.data.objects)
    from maximize import ui
    bpy.context.window_manager.maximize_created = o.name
    check("the Create tab's Parameters show for it", ui.MAXIMIZE_PT_create_parameters.poll(bpy.context) ==
          ui.has_command_panel())
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_setup, s_plane, s_plane_check, s_disc, s_disc_check, s_sphere, s_sphere_check, s_autogrid, s_autogrid_check,
         s_target]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say("ERR", repr(e))
    return 0.6 if steps else None


bpy.app.timers.register(run, first_interval=2.0)

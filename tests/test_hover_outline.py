# Run: moritz.exe --factory-startup --enable-event-simulate --python tests/test_hover_outline.py
# The hover highlight goes away when the mouse leaves the view, and shows the object's outer outline,
# not all its edges (Seb: "it is still active when the mouse is no longer on the viewport and it is
# highlighting all edges and not only the outline as in 3dsmax").
import os
import sys
import tempfile

import addon_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
addon_utils.enable("maximize", default_set=True)

import bpy  # noqa: E402
from bpy_extras import view3d_utils  # noqa: E402
from mathutils import Vector  # noqa: E402
from maximize import hover  # noqa: E402

failures = []


def say(*a): print("MXHV", " ".join(str(x) for x in a), flush=True)


def check(name, ok, *info):
    say("OK" if ok else "FAIL", name, *info)
    if not ok:
        failures.append(name)


def win(): return bpy.context.window_manager.windows[0]
def area(): return max((a for a in win().screen.areas if a.type == 'VIEW_3D'), key=lambda a: a.width * a.height)
def region(): return [r for r in area().regions if r.type == 'WINDOW'][-1]
def move(x, y): win().event_simulate(type='MOUSEMOVE', value='NOTHING', x=int(x), y=int(y))


def shot(name="shot"):
    """The window as (width, height, pixels), via a screenshot file."""
    path = os.path.join(tempfile.gettempdir(), "moritz_hover_{:s}.png".format(name))
    with bpy.context.temp_override(window=win()):
        bpy.ops.screen.screenshot(filepath=path)
    image = bpy.data.images.load(path, check_existing=False)
    width, height = image.size
    pixels = list(image.pixels)
    bpy.data.images.remove(image)
    return width, height, pixels


def is_highlight(image, x, y):
    width, _height, pixels = image
    i = (int(y) * width + int(x)) * 4
    # A thin line blends a little with what is behind it: its hue, not its exact color.
    r, g, b = pixels[i:i + 3]
    return r > 0.75 and g > 0.55 and r - b > 0.2


def count_highlight(image, x0, y0, x1, y1):
    return sum(is_highlight(image, x, y) for y in range(int(y0), int(y1)) for x in range(int(x0), int(x1)))


def on_screen(co):
    r = region()
    p = view3d_utils.location_3d_to_region_2d(r, r.data, Vector(co))
    return r.x + p.x, r.y + p.y


P = {}


def s_setup():
    # The splash screen would hide the middle of the view.
    win().event_simulate(type='ESC', value='PRESS', x=10, y=10)
    win().event_simulate(type='ESC', value='RELEASE', x=10, y=10)
    space = area().spaces.active
    if space.region_quadviews:
        with bpy.context.temp_override(window=win(), area=area(), region=region()):
            bpy.ops.screen.region_quadview()
    space = area().spaces.active
    space.overlay.show_outline_selected = False
    space.overlay.show_overlays = True
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    # A box seen corner on: its three inner edges meet in the middle.
    r = region().data
    r.view_perspective = 'PERSP'
    with bpy.context.temp_override(window=win(), area=area(), region=region()):
        bpy.ops.view3d.view_axis(type='TOP')
    from mathutils import Euler
    r.view_rotation = Euler((0.9553, 0.0, 0.7854)).to_quaternion()
    r.view_location = (0.0, 0.0, 0.0)
    r.view_distance = 8.0
    r.view_perspective = 'PERSP'


def s_hover():
    # Seen corner on, the corner nearest the eye is inside the outline: its edges are inner edges.
    r = region().data
    eye = r.view_matrix.inverted().translation
    corners = [Vector((x, y, z)) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    near = min(corners, key=lambda c: (c - eye).length)
    P['inner'] = [on_screen(near.lerp(c, 0.5)) for c in corners if abs((c - near).length - 2.0) < 1e-3]
    P['outer'] = [on_screen(c) for c in corners if (c - near).length > 2.5 and (c + near).length > 0.1]
    P['center'] = on_screen((0.0, 0.0, 0.0))
    x, y = P['center']
    move(x - 1, y)
    move(x, y)


def s_hover_check():
    check("the box lights up", hover.state["key"] == ("OBJECT", "Cube"), hover.state["key"])


def s_shot():
    image = shot("near")
    P['near'] = image
    inner = sum(count_highlight(image, p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8) for p in P['inner'])
    check("no inner edges are drawn", inner == 0, inner)
    outer = sum(count_highlight(image, p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8) for p in P['outer'])
    check("the outer outline is drawn", outer > 20, outer)
    # Off the box.
    r = region()
    move(r.x + r.width + 40 if r.x + r.width + 40 < win().width else r.x - 40, r.y + r.height // 2)


def s_left():
    pass


def s_left_check():
    x, y = P['center']
    image = shot()
    total = sum(count_highlight(image, p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8) for p in P['outer'])
    say("highlight pixels after leaving", total)
    check("gone when the mouse leaves the view", total == 0, total)
    check("the state says so", hover.state["key"] is None, hover.state["key"])
    # And back, without another object or empty space between.
    move(x - 1, y)
    move(x, y)


def s_back():
    pass


def s_back_check():
    check("back on the box, it lights up", hover.state["key"] == ("OBJECT", "Cube"), hover.state["key"])
    image = shot()
    total = sum(count_highlight(image, p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8) for p in P['outer'])
    check("and draws again", total > 20, total)
    # The view turns: the outline follows.
    r = region().data
    from mathutils import Euler
    r.view_rotation = Euler((1.2, 0.0, 0.2)).to_quaternion()
    area().tag_redraw()


def s_turned():
    pass


def s_turned_check():
    image = shot()
    corner = on_screen((1.0, -1.0, 1.0))
    cx, cy = on_screen((0.0, 0.0, 0.0))
    total = count_highlight(image, cx - 200, cy - 200, cx + 200, cy + 200)
    check("the view turned: an outline still shows", total > 0, total)
    # (1, -1, 1) is now on the top face's front edge, not on the outer outline only if inside; check
    # the screen outline matches the new view: a point just outside the old silhouette has no line.
    say("turned corner", tuple(round(c) for c in corner))
    P['old'] = P['near']
    changed = sum(is_highlight(image, x, y) != is_highlight(P['old'], x, y)
                  for y in range(int(cy - 200), int(cy + 200), 2) for x in range(int(cx - 200), int(cx + 200), 2))
    check("and it is a different outline", changed > 20, changed)
    say("FAILURES", len(failures), failures)
    bpy.ops.wm.quit_blender()


steps = [s_setup, s_hover, s_hover_check, s_shot, s_left, s_left, s_left, s_left_check, s_back, s_back_check, s_turned,
         s_turned_check]


def run():
    try:
        steps.pop(0)()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say("ERR", repr(e))
        if not steps:
            bpy.ops.wm.quit_blender()
    return 0.6 if steps else None


bpy.app.timers.register(run, first_interval=2.0)

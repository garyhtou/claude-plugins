"""Headless Blender build scaffold for a hard-surface, web-bound GLB.

Run:  blender --background --factory-startup --python-exit-code 1 --python build_scaffold.py
(or with the pip `bpy` module: `python build_scaffold.py`)

This is a COMPLETE, RUNNABLE example you adapt. It builds a tiny "instrument
pod" (a chamfered body, a crinkled-foil panel, a wheel, and a deployable lid on a
named pivot) to demonstrate every technique that matters, then applies modifiers,
joins for fewer draw calls, and exports a GLB. Replace the BUILD section with your
object; keep the helpers and the FINALIZE pipeline.

Pinned facts (verified 2026, re-check against your Blender version):
- The `bpy` PyPI wheel pins an EXACT Python: 4.1-4.5/5.0 -> 3.11, 5.1 -> 3.13.
- `--factory-startup` keeps a dev machine's prefs out of CI output.
- `--python-exit-code 1` makes a Python traceback fail the process (without it,
  an exception can still exit 0 and CI passes silently).
- Author Z-up; the glTF exporter's "+Y Up" (default ON) converts to Y-up for
  three.js. Do NOT pre-rotate to compensate, and APPLY all object transforms.
- GLB export is NOT byte-reproducible (tangent floats jitter, the generator
  string embeds the version). Pin the Blender version; don't diff bytes.
"""
import math, os
import bpy
from mathutils import Vector

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.glb')
bpy.ops.wm.read_factory_settings(use_empty=True)
C, D = bpy.context, bpy.data
ALL = []  # every mesh object, for the finalize pass


# ---------------------------------------------------------------------------
# materials. Realism is MATERIAL CONTRAST: metal next to dielectric next to
# painted next to dark-anodized. Metals: metallic=1, low roughness, no diffuse.
# ---------------------------------------------------------------------------
def mat(name, color, metal=0.0, rough=0.5, emit=None, emit_str=0.0, coat=0.0):
    m = D.materials.new(name); m.use_nodes = True  # harmless no-op on Blender 5.0+ (always True); needed <5.0
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if emit is not None:
        b.inputs['Emission Color'].default_value = (*emit, 1)
        b.inputs['Emission Strength'].default_value = emit_str
    b.inputs['Coat Weight'].default_value = coat  # -> KHR_materials_clearcoat
    return m


# An aerospace/metal palette: an EXAMPLE art direction, not a universal default. A
# consumer device (drone, phone, appliance) is mostly painted dielectric (metallic 0)
# with a few metal/glass accents. Override these to match YOUR object.
MATS = {
    'alu':   mat('alu',   (0.50, 0.52, 0.55), metal=0.92, rough=0.40),
    'steel': mat('steel', (0.66, 0.68, 0.71), metal=0.96, rough=0.28),
    'anod':  mat('anod',  (0.06, 0.07, 0.09), metal=0.85, rough=0.45),
    'gold':  mat('gold',  (0.80, 0.50, 0.11), metal=0.90, rough=0.42),
    'paint': mat('paint', (0.80, 0.82, 0.85), metal=0.10, rough=0.55),
    'glass': mat('glass', (0.02, 0.03, 0.05), metal=0.0, rough=0.05, coat=1.0),  # dark glass; CLEAR/refractive glass is NOT a baked factor: author transmission at runtime (see glb-web-pipeline.md)
    'accent':mat('accent',(0.04, 0.10, 0.13), metal=0.30, rough=0.30, emit=(0.24, 0.70, 0.92), emit_str=2.4),
}


def _act(o):
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True); C.view_layer.objects.active = o  # operators need active+selected


def _finish(o, m, bevel, seg, smooth):
    o.data.materials.append(m)
    _act(o)
    if bevel > 0:
        bm = o.modifiers.new('bvl', 'BEVEL')      # a chamfer on EVERY edge, the
        bm.width = bevel; bm.segments = seg       # single biggest "machined not toy" win
        bm.limit_method = 'ANGLE'; bm.angle_limit = math.radians(40)
        # The machined-metal recipe: plain shade_smooth() (works headless) + a Weighted
        # Normal modifier that re-weights normals by face area, so big panels stay
        # DEAD-FLAT and only the chamfer carries the smooth highlight. WITHOUT the WN, a
        # smooth-shaded beveled box smears a gradient across the panel (the "putty" look);
        # WITHOUT shade_smooth the WN is inert. They go together.
        bpy.ops.object.shade_smooth()
        wn = o.modifiers.new('wn', 'WEIGHTED_NORMAL'); wn.keep_sharp = True
    elif smooth:
        bpy.ops.object.shade_smooth()             # genuinely round primitives only
    # else: leave flat-shaded (e.g. a wheel/rotor drum, see below).
    # NB: shade_auto_smooth / shade_smooth_by_angle SILENTLY NO-OP in --background
    # (bug #117399), so use plain shade_smooth() (which works) + WN, never those.
    ALL.append(o)
    return o


def box(name, dims, loc, m, bevel=0.015, seg=2, rot=(0, 0, 0), smooth=False):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = C.object; o.name = name; o.scale = dims
    bpy.ops.object.transform_apply(scale=True)  # APPLY SCALE before bevel/solidify,
    return _finish(o, m, bevel, seg, smooth)    # else non-uniform scale warps them


def cyl(name, r, depth, loc, m, rot=(0, 0, 0), verts=32, bevel=0.0, seg=2, smooth=True):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = C.object; o.name = name
    return _finish(o, m, bevel, seg, smooth)


def strut(name, p1, p2, r, m, verts=18):
    """Cylindrical structural member between two 3D points (tubes, hinge rods)."""
    p1, p2 = Vector(p1), Vector(p2); d = p2 - p1; L = d.length
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=(p1 + p2) * 0.5, vertices=verts)
    o = C.object; o.name = name
    if L > 1e-6:
        z = Vector((0, 0, 1)); axis = z.cross(d)
        if axis.length > 1e-6:
            o.rotation_mode = 'AXIS_ANGLE'
            o.rotation_axis_angle = (z.angle(d), *axis)
            bpy.ops.object.transform_apply(rotation=True); o.rotation_mode = 'XYZ'
    return _finish(o, m, 0, 1, True)


def foil(name, w, h, loc, m, cuts=30, strength=0.04):
    """A crinkled multi-layer-insulation blanket: subdivided plane + procedural
    noise displacement + a little thickness. A signature SPACECRAFT surface. The
    TECHNIQUE generalizes (one displaced panel beats a grid of identical cubes, which
    reads as Minecraft); the gold-foil LOOK does not: on a clean consumer device it
    reads wrong. Use molded/painted surfaces there instead."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    o = C.object; o.name = name; o.scale = (w, h, 1)
    bpy.ops.object.transform_apply(scale=True)
    _act(o); bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=cuts); bpy.ops.object.mode_set(mode='OBJECT')
    tex = D.textures.new(name + '_t', 'CLOUDS')
    tex.noise_scale = 0.09; tex.noise_depth = 3; tex.noise_type = 'HARD_NOISE'
    dsp = o.modifiers.new('disp', 'DISPLACE'); dsp.texture = tex
    dsp.texture_coords = 'LOCAL'; dsp.strength = strength
    dsp.mid_level = 0.0   # push UP only, so the blanket never dips below its base
    o.modifiers.new('sol', 'SOLIDIFY').thickness = 0.02
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); ALL.append(o)
    return o


def empty(name, loc):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=loc, radius=0.15)
    e = C.object; e.name = name
    return e


def parent(empty_obj, children):
    bpy.ops.object.select_all(action='DESELECT')
    for c in children:
        c.select_set(True)
    empty_obj.select_set(True); C.view_layer.objects.active = empty_obj
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)


# ===========================================================================
# BUILD: replace this block with your object. (Research the REAL object's
# anatomy, exact materials, and proportions first; "highly engineered" is a
# research problem before it's a modeling one.)
# This example is MECHANICAL (beveled hardware + spinners + a hinged lid). For a
# STYLIZED/flat look, pass bevel=0 and the WN is skipped; for a STATIC product, drop the
# spinners and the deployable. Keep the FINALIZE pipeline regardless.
# ===========================================================================
body = [
    box('body', (1.6, 1.0, 0.5), (0, 0, 0.5), MATS['alu'], bevel=0.03, seg=3),
    box('belly', (1.4, 0.85, 0.12), (0, 0, 0.2), MATS['anod']),
    foil('deck', 1.4, 0.85, (0, 0, 0.77), MATS['gold']),          # crinkled hero surface
    box('light', (0.05, 0.7, 0.05), (0.81, 0, 0.6), MATS['accent']),  # emissive trim
]

# a SPINNER (any continuously-rotating radial part: wheel, rotor, prop, fan, turbine).
# Name them wheel0../rotor0..; the app spins each about a PER-NODE axis. Flat-shade the
# drum (smooth=False, no bevel): a smooth+beveled short cylinder domes into a sphere.
WX, WY, WZ = 0.7, 0.62, 0.25
spinners = []
for i, (x, y) in enumerate([(WX, WY), (-WX, WY), (WX, -WY), (-WX, -WY)]):
    drum = cyl(f'w{i}', 0.25, 0.18, (x, y, WZ), MATS['anod'],
               rot=(math.pi / 2, 0, 0), verts=28, smooth=False)
    piv = empty(f'wheel{i}', (x, y, WZ)); parent(piv, [drum])  # rename to rotor{i} for a drone
    spinners.append(piv)

# a DEPLOYABLE lid on a NAMED pivot placed EXACTLY on the physical hinge line, with
# the moving geometry's connecting edge coincident with the pivot (no gap) + a
# coaxial hinge knuckle. The web app rotates 'pivot_lid' about its local axis.
HINGE_Y = -0.5  # back edge of the deck
lid = box('lid', (1.4, 0.85, 0.04), (0, HINGE_Y + 0.425, 0.80), MATS['steel'], bevel=0.01)
knuckle = strut('lid_knuckle', (-0.7, HINGE_Y, 0.80), (0.7, HINGE_Y, 0.80), 0.025, MATS['steel'])
pivot_lid = empty('pivot_lid', (0, HINGE_Y, 0.80))   # ON the hinge axis
parent(pivot_lid, [lid, knuckle])


# ===========================================================================
# FINALIZE: apply modifiers, join groups, export. ORDER MATTERS.
# ===========================================================================
# Apply EVERY modifier before any join: bpy.ops.object.join() keeps only the
# ACTIVE object's modifiers and silently drops the rest: your foil Displace and
# all bevels would vanish at join time, and export_apply can't recover them.
for o in list(D.objects):
    if o.type == 'MESH' and o.modifiers:
        _act(o)
        for mn in [md.name for md in o.modifiers]:
            try:
                bpy.ops.object.modifier_apply(modifier=mn)
            except RuntimeError as e:
                print('[apply] skip', o.name, mn, e)


def join_group(name, objs):
    objs = [o for o in objs if o.name in D.objects]
    if not objs:
        return
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    C.view_layer.objects.active = objs[0]
    bpy.ops.object.join(); C.object.name = name


def join_children(piv):
    kids = [c for c in piv.children if c.type == 'MESH']
    if len(kids) > 1:
        join_group(piv.name + '_mesh', kids)


join_group('body', body)                 # static parts -> one mesh
for p in [pivot_lid] + spinners:          # collapse each deployable/spinner under its
    join_children(p)                      # pivot, but KEEP the pivot empties so they animate

print(f'[build] objects: {len(D.objects)}  mesh: {sum(1 for o in D.objects if o.type == "MESH")}')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format='GLB',
    export_apply=True,        # exporter bakes any remaining modifiers (Y-up default ON)
    use_selection=True,
)
print(f'[build] exported -> {OUT}')
# Then Draco-compress:  node compress.mjs model.glb

# Rigging deployables + detecting clips

Moving parts (a fold-out wing, a raising mast, a multi-joint arm, spinning wheels)
are where models break: parts detach, float, or sweep through the body. This is
about making articulation clean and *proving* it with a tool instead of eyeballing.

> **Scope: this is RIGID-BODY articulation**, discrete parts rotating about fixed pivots,
> plus continuous spinners. It is the WRONG paradigm for **organic deformation** (a
> character's limbs or face bending as one continuous skin). For that, use skeletal
> **skinning** (an armature + a weighted `SkinnedMesh`) and **morph targets / blendshapes**
> for the face (driven via `mesh.morphTargetInfluences`), compressed with **Meshopt, not
> Draco** (Draco can't compress morphs). Building a "wave" out of rigid Empty-rotated
> sub-meshes gives you a stiff, detached limb. That authoring is out of scope for this skill.

## The rig contract (keep it stable)

Animate moving parts by rotating **named nodes** (Empties) about a fixed local axis.
Keep the contract (node names + axes) stable, and you can re-author the mesh freely
without touching app code. There are two kinds of motion, and both are just config:

- **Deployables** (a fold-out wing, a raising mast, an arm) move once between two poses.
  Config is a list of `(node, axis, foldRadians)` per joint; the app eases `lerp(from, 0,
  t)` as a deploy progress `t` goes 0→1.
- **Spinners**, any continuously-rotating radial part: a **wheel, rotor, propeller, fan,
  turbine, drill**. Config is `(node, axis, rate)`; the app adds `rate * dt` to that axis
  every frame. The "wheel" naming in the assets is just the spinner convention. Rename
  to `rotor0..N` etc. and point the matcher (`SPINNER_RE`) at it.

The [`build_scaffold.py`](../assets/build_scaffold.py) emits named pivots (`pivot_*`,
`arm_j2/j3`) and spinners (`wheel0..N` / `rotor0..N`); [`inspector.html`](../assets/inspector.html)
and the app both find them by name. **The spin axis is per-node config, never hardcoded**:
after Blender Z-up → glTF Y-up a radial disc's axle can land on any three.js axis, so
verify it empirically (a `Box3` dump) and set the axis, don't assume `z`.

## The pivot must be ON the hinge

Detach/float/clip during animation almost always means **the pivot is not on the real
hinge line, and the moving geometry doesn't start there**. A wing whose pivot sits
0.36 units inboard of its first panel swings through an arc that opens a gap.

1. Put the pivot **exactly on the physical hinge axis** (the body edge for a fold-out
   wing, the base for a mast).
2. The moving part's connecting end must **coincide with the pivot** (no gap). Add a
   coaxial hinge knuckle there, plus a *fixed* matching bracket on the body, so the
   joint reads as a real hinge and never separates.
3. **Orient the hinge hardware along the rotation axis.** A fold-up wing hinges about
   the forward axis, so its hinge rod runs along forward, not laterally. Getting that
   90° wrong looks subtly broken.
4. Tune the fold angle to clear clipping **across the whole transition**, not just at
   the endpoints.

**You cannot debug this from static end-poses.** Use the inspector's **deploy scrubber**
(a 0→1 slider that sets every joint rotation *absolutely* each frame) and the **pivot-
axis markers**. Watching the transition frame-by-frame makes a bad pivot obvious in
seconds. Build the scrubber before trying to fix joints.

## Articulated chains (an arm that genuinely unfolds)

A part that swings rigidly about one pivot looks like a prop and sweeps through the
body. Real arms articulate:
- **Nest named Empties:** `pivot_arm` (shoulder) → `arm_j2` (elbow) → `arm_j3` (wrist).
  Parent each segment's meshes to its joint, then each joint Empty to the previous.
- **Author in the DEPLOYED pose** so rest = deployed; the app folds each joint toward
  stow with `lerp(from, 0, t)` independently → the chain genuinely unfolds. A 3-joint
  arm is three config entries; no new app code. **Convention: `t=1` = deployed (the rest
  pose as built); `t=0` = fully stowed/folded** (`lerp(from,0,t)` gives `0` at t=1 = rest,
  `from` at t=0 = the fold). The inspector's scrubber and `auditClip` use the same t.
- **Join meshes WITHIN a segment** (draw-call win) but **never across joint Empties**
  (that collapses the hierarchy). Keep the joint Empties.
- **Hover/scale effects apply to the ROOT node only**: scaling every nested joint
  compounds (1.05³).

## Two classic radial-part bugs

- **A short fat cylinder seen down its axle + smooth shading reads as a sphere.** Smooth
  shading averages the flat cap's rim normals into a dome; a bevel makes it a bowling
  ball. Fix: flat-shade the drum, don't bevel it, and hide the cap behind a face plate
  (a real wheel has a hub disc there anyway).
- **Radial detail rotated about the wrong axis flies off as spikes** (grousers become a
  sea-urchin; rotor blades fan out wrong). Things placed around a wheel/rotor must rotate
  about the *axle* axis. When you place N things around a circle, write down which plane
  the circle lives in and rotate about its normal. Verify the axle axis empirically
  (`Box3` dump). Z-up→Y-up conversion makes "which axis" non-obvious.
- **High-RPM parts read as a translucent disc, not discrete blades.** A propeller/rotor
  spun fast strobes or wagon-wheels at 60 fps. For the premium read, swap in (or
  crossfade to) a **semi-transparent rotor-disc mesh** at speed, or a motion-blur shader,
  rather than spinning sharp blades.

## A programmatic clip detector beats eyeballing

Eyeballing misses clips and wastes rounds ("you missed one"). Build a real intersection
auditor. It's in [`inspector.html`](../assets/inspector.html) (`window.auditClip()`).

- **True mesh∩mesh via `three-mesh-bvh`, not bounding boxes.** AABBs overlap constantly
  on a compact model. `MeshBVH.intersectsGeometry(otherGeo, matrixAToB)` is triangle-
  accurate and fast enough to **sweep the whole deploy animation (t = 0…1)** and report
  the exact t-range a clip occurs.
- **glTF splits joined multi-material meshes into one primitive per material under a
  Group.** A naive detector grabs only the first primitive and reports "no clips" while
  the part visibly spears the body. Fix: **collect EVERY mesh primitive and group it by
  its nearest joint/wheel ancestor** (else `static`), then test list-vs-list.
- **Curate pairs that should NEVER touch** (distal part vs body, cross-appendage). A
  joint's own root always contacts the body, which shows as a permanent intersection,
  so omit joint-adjacent pairs, or they drown the report in false positives.
- **DANGER: excluding a whole joint pair hides real clips in that segment.** We excluded
  `arm_sh ∩ body` as "just the shoulder mount", but the *upper arm* lives in that same
  segment and was spearing the body in *every* pose; the auditor reported CLEAN while
  the user kept sending videos of the clip. **Fix: mount the root link with a tiny air-
  gap (~0.015, visually invisible) instead of embedding it**, so the whole segment is
  genuinely clear of the body. Then that pair becomes a *real* test.
- **Audit both endpoints, and know which is which.** The sweep covers t=0→1, so it
  catches clips at either end and in between. A clip at **t=1 (deployed rest) is built
  GEOMETRY**: no fold angle fixes it; re-mount / re-route in the builder. A clip at
  **t=0 (stowed) or mid-fold is usually fold-angle-tunable**: search for a clean angle
  (below). A part that clips "when folded closed" is the t=0 case, not t=1.
- **The detector sweeps the FOLD, not the SPIN.** It tests spinners at one blade angle,
  so a folding leg passing through a spinning rotor's *disc*, or a blade tip clipping an
  arm, slips through. For spinners, also sweep the spin axis (a few angles) or test
  against the swept-disc volume. Otherwise the CLEAN report is a false sense of safety
  for exactly the motion a drone/fan/turbine is defined by.
- **Watch the lateral lane.** A front appendage gets squeezed between center clutter and
  the outboard wheels; that gap is often too narrow for a joint boss. Going *under* an
  obstacle (clear it vertically) often beats threading a too-narrow gap.
- **Search, don't guess.** Once clips are a number, script a sweep over candidate fold
  angles and have the tool print which are `CLEAN`:
  ```js
  for (const c of candidates) { window.__STOW.arm_j2 = ['z', c]; console.log(c, window.auditClip(31)); }
  ```
  Two clip-free configs found in one pass beats nudging angles by eye.
- **Detection is objective; the pose still needs a human aesthetic check.** A clip-free
  fold can still look awkward (drill sticking out sideways). The tool narrows the search
  to the clean candidates; you pick the best-looking one.

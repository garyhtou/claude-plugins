---
name: building-3d-for-web
description: Use when creating, fixing, or optimizing a 3D model for a website: procedurally authoring a model in Blender via Python/headless (bpy), exporting glTF/GLB (Draco, Meshopt, KTX2), and loading it in Three.js or React-Three-Fiber. Triggers when a model looks like a toy / Minecraft / Roblox, materials don't read as real, exported geometry shades flat or comes out wrong, deployable or rigged parts clip / detach / sweep through the body when animated, a GLB is too large, shade_auto_smooth no-ops headless, join() drops modifiers or bevels, wheels spin on the wrong axis, or you need to inspect and verify a 3D model in the browser. Covers Blender bpy gotchas, hard-surface realism, the GLB web pipeline, articulated rigging, and programmatic clip detection.
---

# Building 3D for the Web

Procedurally author a believable hard-surface 3D model in Blender, ship it to the web
as an optimized GLB, and verify it in the browser. This is the specialization that
powers a WebGL hero or 3D product piece for an awwwards-grade site (pairs with the
`high-fidelity-web` skill, which builds the surrounding page).

**Core principle:** for hard-surface hardware, **proportions + material contrast + a
few signature details win, and polygon count barely matters.** Most of the work is
diagnosis (looking from the right angles), not modeling. Build a dedicated inspector
*first*; it pays for itself in the first hour.

## When to use

- Building or fixing a 3D model destined for a website (a product, vehicle, device, prop).
- Procedural / parametric / reproducible authoring in Blender via `bpy` (headless, CI).
- A model reads as "toy", materials look flat, exports shade wrong, rigged parts clip,
  or a GLB is too heavy.

**This skill is for REALISTIC, HARD-SURFACE objects** (manufactured hardware: vehicles,
devices, props, products): a single object or a few composed parts. If your subject is
different, the *pipeline* (build → export → Draco → R3F → inspect) still applies, but the
*aesthetic and rigging* guidance does not. Route accordingly:

- **Stylized / flat-shaded / low-poly** (cozy, toon, Monument-Valley): **invert** the
  realism playbook: flat shading on purpose (`flatShading: true`, or `MeshToonMaterial`
  + a gradient map), **vertex colors** instead of textures, **no** bevels or weighted
  normals (the sharp facets are the look). See "Stylized targets" in
  [`references/realism.md`](references/realism.md).
- **A multi-object scene / diorama** (forest, city, scattered props): model a few
  **archetypes** and **instance** them at runtime (drei `<Instances>` / `InstancedMesh`),
  scattered in R3F. Don't bake hundreds of copies into the GLB. Budget draw calls. See
  [`references/glb-web-pipeline.md`](references/glb-web-pipeline.md).
- **Organic / characters** (creatures, faces, anything that *deforms*): a different
  discipline: sculpt → retopo (quad loops) → armature + **skinning** (`SkinnedMesh`) →
  **morph targets / blendshapes** for the face, with **Meshopt not Draco** (Draco can't
  compress morphs). This skill covers only the export/ship tail; for a base mesh see the
  asset/AI sourcing landscape in [`references/realism.md`](references/realism.md).

## The pipeline (mental model)

1. **Research the real object first:** anatomy, exact materials/hues, reference
   proportions. "Highly engineered" is a research problem before a modeling one.
2. **Build** in Blender headless (`build_scaffold.py` helpers): chamfered boxes, a
   crinkled-foil hero surface, named pivots for deployables.
3. **Apply modifiers → join → export.** In that order, or you lose bevels/displacement.
4. **Compress** to GLB: Draco (geometry) and/or KTX2 (textures).
5. **Load** in three.js / R3F with the right decoders.
6. **Verify** in the inspector: orbit, scrub articulation, run the clip detector. Fix,
   rebuild. Keep the loop tight.

## Quick reference (the gotchas that cost the most)

| Symptom | Cause | Fix | More |
|---|---|---|---|
| Reads as Minecraft/Lego/toy | Grid of identical cubes; one uniform material; sharp 90° edges | One crinkled-foil surface; material *contrast*; bevel every edge | [realism](references/realism.md) |
| Everything exports faceted/flat | relied on `shade_auto_smooth`/`shade_smooth_by_angle`, which no-op headless (#117399) | plain `shade_smooth()` (works) + Bevel + Weighted Normal | [blender](references/blender-procedural.md) |
| Flat panel shows a smeared gradient ("putty") | smooth-shaded without weighted normals | add Weighted Normal modifier (last, `keep_sharp`) so panels stay flat, chamfer carries the highlight | [realism](references/realism.md) |
| Bevels/displacement vanish | `join()` keeps only the active object's modifiers | Apply ALL modifiers BEFORE join | [blender](references/blender-procedural.md) |
| `npm install` fails / hangs | `@gltf-transform/cli` or `/functions` pull native `sharp` | core + extensions + draco3dgltf only (`compress.mjs`) | [pipeline](references/glb-web-pipeline.md) |
| Clearcoat/emissive disappear after compress | Extension not registered before `io.read()` | `registerExtensions(ALL_EXTENSIONS)` | [pipeline](references/glb-web-pipeline.md) |
| Clear glass renders as a dark blob | exported as an opaque dielectric factor | author transmission at runtime: `MeshPhysicalMaterial` (metalness 0, `transmission` 1, `ior` 1.5) + a scene env map | [pipeline](references/glb-web-pipeline.md) |
| Need a printed label / decal / screen | material-factor-only can't address a surface region | UV-unwrap that part + a `baseColorTexture` (sRGB); triangulate before export | [pipeline](references/glb-web-pipeline.md) |
| Part lies on its side / wheels spin wrong axis | Blender Z-up → glTF Y-up (+Y → −Z); un-applied transform | Apply all transforms; keep "+Y Up"; verify axis empirically | [pipeline](references/glb-web-pipeline.md) |
| Deployable detaches / floats / sweeps through body | Pivot not on the hinge; rigid single-pivot swing; rest-pose geometry clips | Pivot ON hinge; articulate (nested joints); audit t=1 separately | [rigging](references/rigging-and-clips.md) |
| Short wheel looks like a sphere | Smooth shading domes the flat cap | Flat-shade the drum; hide the cap behind a face plate | [rigging](references/rigging-and-clips.md) |

## How to use this skill (progressive disclosure)

This file is the spine. Load reference files as each step needs them, to keep context
lean:

- [`references/realism.md`](references/realism.md): what makes hard-surface read as
  real vs toy, plus game-ready fundamentals (topology, normal-map baking, PBR materials,
  UVs, LODs) and the asset-sourcing / AI-3D landscape. (Research + Build.)
- [`references/blender-procedural.md`](references/blender-procedural.md): headless `bpy`
  gotchas, the modifier → join → export pipeline, version removals, geometry nodes,
  reproducible runs. (Build.)
- [`references/glb-web-pipeline.md`](references/glb-web-pipeline.md): Draco / Meshopt /
  KTX2, the `sharp` pitfall, extension preservation, three.js/R3F loading, performance
  budgets, Z-up → Y-up. (Compress + Load.)
- [`references/rigging-and-clips.md`](references/rigging-and-clips.md): pivot-on-hinge,
  articulated chains, the rig contract, and the programmatic clip detector. (Build + Verify.)
- [`references/verifying-in-browser.md`](references/verifying-in-browser.md): the
  inspector, review lenses, ingesting a user's screen recording, integration gotchas. (Verify.)

**Assets (copy and adapt):**
- [`assets/build_scaffold.py`](assets/build_scaffold.py), runnable Blender headless
  scaffold: helper library + the correct build → apply → join → export pipeline.
- [`assets/compress.mjs`](assets/compress.mjs): Draco compressor with no native deps,
  preserves material extensions.
- [`assets/inspector.html`](assets/inspector.html), standalone auditor: orbit + deploy
  scrubber + per-part bounding boxes + BVH clip detector.

## Common mistakes

- **Modeling before looking.** Screenshot from four angles and name the two worst tells
  first; most fixes aren't "more geometry."
- **Trusting training-data API.** Blender's API shifts every release. Probe the real
  version (`print` the BSDF inputs, list operators) instead of guessing.
- **Eyeballing clips.** Use the BVH detector and *sweep* the animation; audit the
  deployed (t=1) rest pose separately, since rest-pose clips are geometry, not fold angles.
- **Compressing every iteration.** A DRACOLoader-configured loader reads uncompressed
  GLBs fine. Iterate raw, compress at the end.

## Real-world impact

The VANTA Prospector rover went from "looks like a Roblox plugin" to an awwwards-grade
hero: a sculpted ~190 KB Draco GLB (smaller than the earlier, cruder model), with a
fold-out solar/mast/arm rig that articulates clip-free, verified end-to-end in the
browser.

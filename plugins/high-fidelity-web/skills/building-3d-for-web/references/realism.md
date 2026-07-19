# Making a model read as real (not toy) + game-ready fundamentals

The first VANTA rover "looked like a Roblox/Minecraft plugin." None of the fixes
were more geometry. This is what actually moves a hard-surface model up a tier, plus
the real-time fundamentals (topology, baking, PBR, UVs, LODs) and where to source
assets when you shouldn't model from scratch.

**The principles here are universal; the surface vocabulary is art-directed.**
Material contrast, bevels + weighted normals, real scale, surface imperfection, and
grounded proportions apply to anything. But the *examples* below lean spacecraft
(gold Kapton foil, dense greebles, a metal-heavy palette) because they came from a
rover. A sleek consumer device wants the opposite read: clean injection-molded matte,
soft-touch dielectric, minimal greebles, a couple of metal/glass accents. Keep the
principles; choose the vocabulary that fits your object.

**Stylized targets invert most of this.** For a deliberately flat-shaded, low-poly, toon,
or "cozy" look (Monument Valley, hand-crafted indie), the realistic-surface techniques
below are the *wrong* tool. You want **flat shading on purpose** (`flatShading: true`, or
`MeshToonMaterial` + a 2-3 step gradient map), **vertex colors** (`COLOR_0`) instead of
textures, a saturated palette, a soft gradient/hemisphere sky, and **no bevels or weighted
normals**. The sharp facets *are* the aesthetic. Don't bevel-and-weighted-normal a
stylized model into smooth plastic. What still carries over: grounded proportions, real-ish
scale, negative space, and color used for meaning.

## The toy tells, in priority order

1. **A grid of identical primitives** reads as Minecraft instantly. Replace a waffle of
   cubes with **one crinkled-foil surface** (a subdivided plane + noise displacement,
   the `foil()` helper). The single biggest upgrade we made.
2. **Chrome ball-bolts / repeated shiny spheres** read as Lego. Use subtle recessed
   battens/panel lines instead.
3. **A single uniform material** = toy. Real hardware is **material contrast in close
   proximity**: machined aluminum next to gold Kapton next to black anodized next to
   white radiator. That juxtaposition is most of the "engineered" read.
4. **Toy proportions** (a thin slab on huge wheels). Ground it in real reference ratios.
   Model at real metric scale; wrong scale is the fastest toy tell. Note: even at correct
   dimensions, **over-thick parts and over-large bevels make it read as a miniature**.
   Bevel scale is itself a proportion cue.
5. **Hard 90° corners.** Light never strikes an infinitely sharp edge; every real edge
   has a micro-bevel that catches a specular highlight. A flat-shaded box + a 1-2 segment
   bevel reads as a CNC chamfer (more "machined" than a rounded fillet). Production
   benchmark: roughly a **2-3 px** edge-highlight width.
6. **No greebles.** Real spacecraft are covered in fasteners, cabling, labels, warning
   placards, a calibration target. A handful sell authenticity (the "used future" look,
   coined at ILM). Layer detail density but **preserve negative space** so the detailed
   areas read.

**"Highly engineered" is a research problem first.** Before modeling, research the real
object's anatomy and exact materials/hues.

## Bevels + weighted normals (the machined-metal recipe)

Smooth shading averages vertex normals; on a low-poly beveled mesh the tiny bevel faces
share vertices with big panels, smearing a gradient across the panel (the "putty" look).
**Face-weighted normals** re-weight by face area so large faces stay dead-flat and the
smooth transition is confined to the bevel. **Bevel + Weighted Normal is the recipe.**
(Blender mechanics: [`blender-procedural.md`](blender-procedural.md). Real-time alt with
no geometry: Marmoset's bevel shader fakes it at runtime via normals.)

## Surface imperfection and wear

This is for *used, real-world* hardware. A **luxury, clinical, or brand-new** product wants
the OPPOSITE: flawless, uniform surfaces. Wear and grime there read as *cheap*. For those,
skip this section and lean on form, material purity, and lighting instead.

Uniform clean surfaces read synthetic. Highest-impact lever is **roughness variation**
(fingerprints, polish, grime shift roughness far more than albedo). **Edge wear** via a
baked **curvature map** so chips cluster on raised edges (the same edges the bevels
light); **dirt/grime via AO** so it collects in crevices. Vary opacity within a damage
type. Identical repeated damage reads fake.

## PBR materials (metallic-roughness, the glTF/web standard)

glTF 2.0 core *is* metallic-roughness; spec-glossiness was archived by Khronos in 2021
(don't author new spec-gloss). Physically plausible values:

- **Metalness is binary:** use 0 (dielectric) or 1 (metal), **never a mid-grey ~0.5**
  (a hair under 1 for grunge is fine; intermediate values otherwise only for transition
  pixels / dirt-over-metal). Getting this binary-correct is the single biggest "is it
  metal" cue. (Glass and other dielectrics are **0**, not a low metalness.)
- **Dielectrics reflect ~4% (F0 = 0.04, IOR ~1.5).** Their base color (albedo) must sit
  inside an **sRGB ~30/50 to ~240 window**: nothing pure black or pure white, or you
  lose headroom for AO/roughness/lighting.
- **Metals have ~zero diffuse;** the base color encodes the colored F0 specular,
  roughly **sRGB 180-255**. Measured: aluminum `#e8eaea`, iron `#c4c6c6`, gold `#ffd891`,
  copper `#f7bc9e`, silver `#f7f4e8`.
- **Painted metal = dielectric (metallic 0)**: light hits the paint. Only worn-through
  spots expose bare metal (metallic 1); that worn-paint boundary is a top realism cue.
  **Anodized aluminum** = colored dielectric oxide → treat as dielectric too.

Texture color space (three.js `MeshStandardMaterial` mirrors this):

| Map | Color space | glTF packing |
|---|---|---|
| Base color / emissive | **sRGB** | `baseColorTexture` / `emissiveTexture` |
| Metalness | linear | **blue** of metallicRoughness |
| Roughness | linear | **green** of metallicRoughness |
| Normal / AO | linear | `normalTexture` / **red** (ORM); `aoMap` needs a 2nd UV set |

For a material-factor-only model (no image maps) you set these as Principled BSDF
factors. No textures, no UVs needed.

## Topology and polycount

- **Hard-surface/static props: tris and n-gons are fine if shading is clean.** N-gons are
  great for capping broad flat areas; keep poles (3-/5-edge verts) out of curved zones.
  **Deforming/skinned meshes** (characters) need clean quad edge loops following the
  deformation. That's a different discipline.
- **glTF triangulates everything** (only triangle primitives). **Triangulate before
  export** to lock the result (different tools triangulate differently and can break a
  baked normal map). Blender gotcha: **tangents won't export unless you triangulate
  first.** UV seam = hard edge; match smoothing groups to UV islands.
- **Budgets (indicative, vary by platform):** web/real-time prop low-thousands; web hero
  focal object ~40k-60k tris (device-safe ceiling ~50k, flagships ~120k-150k). But
  **draw calls dominate over raw triangles** in three.js: a scene of 1,000 tiny cubes is
  slower than one 100k-tri mesh. Target < 100 draw calls desktop, < 50 mobile; instance.

## Normal-map baking (the lightness lever)

- **High-to-low:** sculpt/model a dense high-poly, ray-project its detail onto a low-poly
  mesh's normal map via a **cage** (expanded low-poly bounding the rays; extend just far
  enough to enclose the high-poly).
- **The silhouette rule:** *normal maps can't change the silhouette.* So **model
  silhouette/profile-defining detail** (large bevels, protruding bolts on the outline)
  and **bake fine surface detail** (screws, scratches, panel grooves, weave). This is how
  web assets stay light. Rotate the model to find what defines the silhouette; spend tris
  only there.
- **Tangent-space, OpenGL (+Y green)** for glTF/three. GLTFLoader sets `normalScale =
  (1, -1)`; if bumps read as dents, your map is DirectX (-Y). Flip green. Bake ≥16-bit
  to avoid banding.

## UVs, trim sheets, atlases

- **UVs are needed only when image textures drive the surface.** A material-factor-only
  or vertex-colored model needs none. There's nothing to address. (Big reason the
  procedural hard-surface path stays simple.)
- **Trim sheets** (one tiling strip of reusable panels/pipes mapped across many surfaces)
  and **atlases** (many objects' UVs in one image → one shared material → one draw call)
  cut texture count and draw calls, the highest-leverage perf move when you do use
  textures. Keep texel density consistent (~512 px/m props, ~1024 px/m hero).

## LODs: the candid web take

For a **single hero asset on a landing page, LODs are usually not the priority** (one
model = few draw calls, no distant geometry to thin). The bigger lever is **compression:
Draco/Meshopt + KTX2** (see [`glb-web-pipeline.md`](glb-web-pipeline.md)). Add LODs only
for many-object scenes, large worlds, or configurators. glTF has no ratified core LOD
(only vendor `MSFT_lod`); three.js has `THREE.LOD`.

## When NOT to model from scratch (sourcing + AI)

- **Procedural has a ceiling.** Excellent for hard-surface hardware (parametric,
  reproducible). For organic forms (creatures, faces, hand-sculpted asymmetry) it's the
  wrong tool. That's interactive Sculpt Mode.
- **CC0 asset libraries** (safe, commercial OK, no attribution): Quaternius, Poly Haven,
  ambientCG, Kenney, and CC0 items on Poly Pizza. **Check licenses** elsewhere: Sketchfab
  is per-model; Quixel Megascans is paid again (2025+) inside Fab; Fab uses royalty-free,
  not the full CC spectrum.
- **Photogrammetry / scanning** (RealityScan, Metashape, Polycam, KIRI) always needs
  retopo + bake to be web-ready.
- **AI text/image-to-3D (Rodin, Meshy, Tripo, Hunyuan3D, TRELLIS, Edify):** candid 2026
  verdict: **almost all output dense triangle/marching-cubes meshes, not artist-clean
  quads**; "quad" options are AI quads, not hand edge-flow. None ship a zero-cleanup
  awwwards hero. They're genuinely useful **upstream**: concepting, blockout, props, set
  dressing, kitbash parts, and as high-poly/texture donors you then retopo + rebake.
  Watch license/territory traps (e.g. Hunyuan3D's license excludes EU/UK/South Korea;
  several free tiers are CC-BY, requiring attribution). Rodin/Hyper3D is currently closest
  to a drop-in *static* prop with light cleanup.

**Best moves for a Three.js/glTF hero:** model hard-surface procedurally (this skill);
use AI/scan/library assets as donors or for secondary props; bake silhouette-irrelevant
detail into normal maps; ship GLB with Draco + KTX2.

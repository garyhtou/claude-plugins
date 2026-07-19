# The GLB → web pipeline (Draco / Meshopt / KTX2, loading, budgets)

Getting a model onto the web cheaply. Two orthogonal axes: **geometry compression**
(Draco *or* Meshopt) saves download/parse; **GPU texture compression** (KTX2/Basis)
saves VRAM. They combine freely and solve different bottlenecks.

## Decide first: does your model have textures?

Inspect the GLB (`npx @gltf-transform/cli inspect model.glb`: the `inspect` command is
sharp-free; it lists meshes, triangles, textures, and extensions). No `images`/`textures`
arrays (PBR via material *factors* only: `baseColorFactor`, `metallicFactor`,
`roughnessFactor`, `emissiveFactor`, or `COLOR_0` vertex colors) → **KTX2 gives you
nothing**; all the win is geometry. This is the common case for a
procedurally-built hard-surface model, and it lets you skip the entire texture
toolchain (and the `sharp` pitfall below). Texture-heavy model (2K-4K atlases,
normal/ORM maps) → KTX2 is the highest-leverage move.

**When you DO need a texture for one region** (a printed label, a decal, a screen, a
sticker, a wood grain): material factors can't do it. UV-unwrap that part and assign a
`baseColorTexture` (authored **sRGB**; roughness/normal maps are **linear**).
**Triangulate before export or tangents won't export** (and normal maps break). Decision:
**one small texture (a 256-1024px label) → just ship the PNG/JPG and Draco the geometry**;
the KTX2 toolchain (and its `sharp`/`ktx` native builds) isn't worth it until you have
several large maps.

## Glass, transmission, and runtime-only materials

Some materials are **not** glTF material factors and shouldn't be baked into the model:
clear glass, liquid, gems, anything refractive. Exported as an opaque dielectric factor,
glass renders as a **dark blob**. Author it at load time in three.js:

```js
mesh.material = new THREE.MeshPhysicalMaterial({
  metalness: 0, roughness: 0.03, transmission: 1, ior: 1.5,
  thickness: 0.5,                 // volume: required for refraction to bend
  attenuationColor: 0x88bbaa, attenuationDistance: 0.4,  // the glass/liquid tint
});
```
- **Transmission shows NOTHING without a `scene.environment`** (an HDRI or `RoomEnvironment`).
  There is nothing to refract/reflect. This is the #1 "my glass is black" cause.
- Keep the GLB pure geometry + named material slots; swap the physical material in by mesh
  name after load. Draco-compressing the geometry is still fine.
- If you author transmission in Blender and export it (`KHR_materials_transmission` /
  `_volume` / `_ior`), `ALL_EXTENSIONS` (below) preserves it through compression, but the
  env-map requirement still holds in three.js.
- Nested refraction (liquid in glass in air) is single-bounce-approximate; tune
  `thickness`/attenuation by eye, and give the inspector a real studio HDRI first (its
  default metal lighting won't read glass).

## Geometry: Draco vs Meshopt (pick one, not both, per primitive)

| | Draco (`KHR_draco_mesh_compression`) | Meshopt (`EXT_meshopt_compression`) |
|---|---|---|
| Ratio | **Highest** geometry compression (smallest download) | ~2-4x; closes the gap when CDN serves brotli/zstd (`gltfpack -cc`) |
| Decode | WASM decoder, slower | 3-6 GB/s, smaller decoder, **much faster** |
| Render | **Disturbs vertex/index order** → less GPU-cache-friendly | Preserves vertex-cache locality |
| Animation/morphs | Cannot compress morph targets | Compresses geometry + morphs + keyframe animation |
| Default quantization | pos 11, normal 8, uv 10 bits (don't drop pos < 11: visible snapping) | composes with `KHR_mesh_quantization` |

- **Static, material-only hero, smallest download is the goal → Draco.** That's the
  VANTA rover case: a vertex-dense procedural mesh went **~1.4 MB → ~190 KB**.
- **Animation/morphs, many models, render perf matters, you control CDN → Meshopt.**
  It's the modern default for richer scenes.

## Textures: KTX2 / Basis Universal (`KHR_texture_basisu`)

GPU-supercompressed; transcoded at load to the GPU's native block format and
**stays compressed in VRAM** (the point). A 4096² RGBA texture is ~64 MB in VRAM
(~90 MB with mipmaps) decompressed from a ~200 KB PNG; KTX2 cuts that 4-8x.
- **ETC1S** = smaller, lower quality → base color / emissive / flat maps.
- **UASTC** = BC7-class, larger (zstd-wrap) → **normal maps, ORM/packed maps**.
- Caveat: KTX2 is not guaranteed smaller *on disk* than JPEG/PNG; the win is VRAM +
  upload speed. Must be encoded before glTF integration; mark the extension required.

## The toolchain and the `sharp` pitfall (critical for CI/sandbox)

`sharp` is a native libvips build that fails in restricted-network / sandboxed CI.
Avoid pulling it.

- **`@gltf-transform/cli`** pulls `sharp` for any **texture** command
  (`webp`/`avif`/`png`/`jpeg`/`etc1s`/`uastc`/`optimize --texture-compress`).
  Geometry-only commands are sharp-free.
- **`@gltf-transform/functions`** → `textureCompress()` requires `sharp` as its
  encoder. But `dedup`, `prune`, `weld`, `quantize`, `reorder`, `simplify`, `join`,
  `instance`, **`draco`, and `meshopt`** are pure JS/WASM, no native build.
- **KTX2 encoding never goes through sharp**: `etc1s`/`uastc` shell out to the
  external KTX-Software (`ktx`/`toktx`) binary (a *second* native install).

**Three CI-safe routes:**
1. **Geometry-only, no textures:** the [`compress.mjs`](../assets/compress.mjs) asset
   (core + extensions + draco3dgltf only). Pure JS/WASM. Run `node compress.mjs model.glb`.
   This is the default. (It marks Draco `required`, so the GLB then needs a Draco decoder
   to open at all, fine for your app, but a generic/preview viewer without one will fail.)
2. **gltf-transform CLI, geometry only:** `gltf-transform optimize in.glb out.glb
   --compress meshopt --texture-compress false` (or à-la-carte `dedup` → `weld` →
   `prune` → `reorder` → `quantize` → `meshopt`/`draco`).
3. **gltfpack native binary** (from GitHub Releases, not npm): one self-contained
   binary does meshopt geometry **and** KTX2 textures: `gltfpack -i in.glb -o out.glb
   -cc -tc`. (The npm/WASM gltfpack does mesh only: `-tc` is unavailable there.)

## Preserve extensions through a re-write (silent-drop footgun)

To round-trip an extension, **register its class on the IO BEFORE `io.read()`**.
If a present extension isn't registered, gltf-transform drops it on write with only
a console warning. This silently kills clearcoat, emissive-strength, transmission,
lights, and instancing. The [`compress.mjs`](../assets/compress.mjs) asset does this:

```js
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS); // not KHRONOS_EXTENSIONS
```
`KHRONOS_EXTENSIONS` misses vendor `EXT_*` (meshopt, gpu_instancing, texture_webp);
use `ALL_EXTENSIONS` unless you have a reason. Clearcoat round-trips Blender → glTF →
three.js (`KHR_materials_clearcoat` → `MeshPhysicalMaterial.clearcoat`); Coat IOR/Tint
do not.

## Loading in three.js / R3F

GLTFLoader has no built-in decoders. Attach one per extension used.

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const loader = new GLTFLoader();
loader.setDRACOLoader(new DRACOLoader().setDecoderPath('/draco/'));   // local, not CDN
loader.setMeshoptDecoder(MeshoptDecoder);
loader.setKTX2Loader(new KTX2Loader().setTranscoderPath('/basis/').detectSupport(renderer));
```
- **`KTX2Loader.detectSupport(renderer)` is required before loading**: the transcode
  target (ASTC/BC7/ETC2/…) is hardware-dependent and read from the renderer.
- **drei `useGLTF`:** `useGLTF(url, true, true, extendLoader)`. Draco defaults to the
  **gstatic CDN**. Pass a string for a local path: `useGLTF(url, '/draco/')`. Meshopt
  is auto-wired; **KTX2 is NOT**: attach it via the `extendLoader` callback.
  `useGLTF.preload(url)` at module scope avoids load waterfalls. Wrap consumers in
  `<Suspense>` (the loader suspends by throwing a promise).
- **Host decoders locally in production** (`/public/draco/`, `/public/basis/`): copy
  from `three/examples/jsm/libs/`. Version-matches your three, works offline, dodges
  CDN/CORS outages. A DRACOLoader-configured loader still loads uncompressed GLBs, so
  you can iterate without compressing every build.

## Draw-call reduction (often matters more than triangle count)

- **Merge by material** (`BufferGeometryUtils.mergeGeometries`) for static scenery,
  but you lose per-object move/cull/raycast. Joining in Blender before export does the
  same (collapses N objects to one primitive per material).
- **Instancing** (`THREE.InstancedMesh`, drei `<Instances>`) for many copies needing
  individual transforms (one draw call for N). **This is also how you author a scene**
  (a forest, a city, scattered props): export a few **archetypes**, then scatter them at
  runtime in R3F with randomized position/rotation/scale (and per-instance color via
  `instanceColor`), rather than baking hundreds of copies into the GLB.
- **`three-mesh-bvh`** for fast raycasting/pointer-events on large imported meshes
  (default raycast is O(n) per mesh). Also the engine for the clip detector.

## Budgets for an awwwards-grade hero

- 60 fps = **16.67 ms/frame**. Instrument with `renderer.info` (draw calls, triangles).
- **Draw calls are the dominant lever:** < ~100/frame holds 60 fps broadly; > ~500
  struggles even on strong GPUs.
- Triangles: hero focal object ~50k-100k; whole scene < ~500k for broad compatibility.
- Textures: 2K default for the hero's main maps, 1K for secondary, 4K only for the
  single closest surface. Power-of-two for clean mipmaps.
- **GLB file size: target < ~4 MB total** after optimization (heroes are often 18-25 MB
  raw). Geometry (Draco/Meshopt) for download + KTX2 for VRAM.
- **A geometry-only GLB that's still huge (e.g. 9 MB, no textures) is a pathological
  mesh, not a compression problem.** Draco shrinks the download but can't fix the cause:
  `weld` duplicate/unwelded verts, `prune` unused data, and `simplify`/decimate the mesh
  first. A hard-surface prop should be low thousands to tens of thousands of triangles
  raw (the VANTA rover was ~1.4 MB before Draco). 9 MB means runaway subdivision or
  unmerged duplicates.

## Blender Z-up → glTF Y-up (the axis footgun)

Blender is Z-up (forward −Y); glTF and three.js are Y-up (forward +Z). Conversion:
`(x, y, z)_blender → (x, z, −y)_gltf`, so **Blender +Y → three −Z**. Half of all
"wrong axis" bugs trace to this (e.g. wheels spinning on the wrong axis).
- Keep the exporter's **"+Y Up" ON** (default). Off → the model lies on its side in
  standards viewers.
- **Apply all object transforms before export** (`Ctrl+A` → All Transforms / script
  `transform_apply`). An un-applied object rotation stacks on top of the Y-up
  conversion → sideways or upside-down. Do NOT manually pre-rotate to compensate (it
  double-rotates).
- Round-tripping a glTF back into Blender re-adds +90° X; don't manually re-rotate.
- **Don't solve axis bugs analytically under pressure: verify empirically** in the
  inspector (a `Box3` dump of a part reveals which axis it actually spans) and set the
  app to match.
- glTF/GLB export is **not byte-reproducible** (tangent floats jitter run-to-run; the
  `asset.generator` string embeds the version). Pin the Blender version; don't gate CI
  on byte-identical output.

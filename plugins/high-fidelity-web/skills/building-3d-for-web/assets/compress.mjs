// Draco-compress a .glb in place, preserving material extensions
// (clearcoat / emissive-strength / transmission / etc).
//
//   npm i -D @gltf-transform/core @gltf-transform/extensions draco3dgltf
//   node compress.mjs path/to/model.glb
//
// WHY this and not `@gltf-transform/cli` or `@gltf-transform/functions`:
// those pull `sharp` (a native libvips build that fails in sandboxed / CI /
// restricted-network environments). The core + extensions + draco3dgltf path is
// pure JS/WASM with no native build. Draco compresses GEOMETRY only, which is
// exactly what you need for a material-factor-only model (no image textures).
// If your model HAS textures, that is a separate axis (KTX2/Basis). See the
// glb-web-pipeline reference; do textures with `ktx` or native `gltfpack -tc`,
// still avoiding sharp.
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS, KHRDracoMeshCompression } from '@gltf-transform/extensions';
import draco3d from 'draco3dgltf';
import { statSync } from 'node:fs';

const GLB = process.argv[2];
if (!GLB) { console.error('usage: node compress.mjs <model.glb>'); process.exit(1); }

// REGISTER ALL EXTENSIONS BEFORE read(). If an extension present in the file is
// not registered here, gltf-transform silently drops it on write(): you lose
// clearcoat/emissive/transmission/lights/instancing with only a console warning.
const io = new NodeIO()
  .registerExtensions(ALL_EXTENSIONS)
  .registerDependencies({
    'draco3d.encoder': await draco3d.createEncoderModule(),
    'draco3d.decoder': await draco3d.createDecoderModule(),
  });

const before = statSync(GLB).size;
const doc = await io.read(GLB);
doc.createExtension(KHRDracoMeshCompression)
  .setRequired(true)
  .setEncoderOptions({ method: KHRDracoMeshCompression.EncoderMethod.EDGEBREAKER });
await io.write(GLB, doc);
const after = statSync(GLB).size;

const kept = doc.getRoot().listExtensionsUsed().map((e) => e.extensionName).join(', ') || '(none)';
console.log(`[compress] ${(before / 1024).toFixed(0)} KB -> ${(after / 1024).toFixed(0)} KB`);
console.log(`[compress] extensions preserved: ${kept}`);

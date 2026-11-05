# Figure-skating 3D demo asset attribution

## Human reference mesh

- Asset: **CesiumMan** from the Khronos glTF Sample Assets collection
- Source: <https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/CesiumMan>
- License: **CC BY 4.0**
- License text: <https://creativecommons.org/licenses/by/4.0/>
- Local file: `human_cesiumman.glb`

The page now deforms the opaque mesh with its original skin weights. Nineteen skin bones are mapped to the MotionExpert joint positions using segment frames. The original integral shoes are masked where the imported skate boots take over. Materials and pose are modified. This is a generic stylized body, not a scan of the recorded athlete. Bone twist and wrist orientation are approximate.

## Ice skates

- Asset: **Ice Skates**, by **IsaacTheMaverick**
- Original: https://sketchfab.com/3d-models/623771273fd44848bd3e4e55dc358190
- Public distribution: https://huggingface.co/datasets/allenai/objaverse/resolve/main/glbs/000-051/623771273fd44848bd3e4e55dc358190.glb
- License: Creative Commons Attribution (`by` in the archived Objaverse metadata).
- License information: https://creativecommons.org/licenses/by/4.0/
- Evidence: `metadata-051.json.gz`, entry `623771273fd44848bd3e4e55dc358190`.
- Original local file: `ice_skates_isaac.glb`.
- Modifications: extracted one skate from the posed pair, removed display objects and ice, normalized orientation and size, mirrored for the second foot, recolored materials. Generated geometry: `skate-derived.json`.
- Build conversion: `node prepare_skate.cjs`, then `node build_skater_viewer.cjs` from the workspace root.

The first candidate by UniverseGames23234 was not imported: its download API required authentication. The IsaacTheMaverick asset is independently available in the public Objaverse collection. The model is artist-created and is not a certified measurement of standard skating equipment.

### Foot attachment correction (2026-09-24)

The estimated boot ankle landmark `(0, .035, -.045)` and forefoot landmark `(0, -.055, .065)` define a downward-sloping local reference vector. That reference, not the horizontal blade axis, is mapped to the recorded ankle-to-foot joint direction. This removes an approximately 39-degree artificial downward pitch in the flat-foot fixture. These are visual registration estimates, not athlete-calibrated anatomical measurements. Foot roll is underdetermined by joint positions: the renderer transports the previous orientation, restores the up reference gradually (at most four degrees of roll correction per source frame), and applies symmetric five-frame quaternion smoothing. The ankle anchor remains exact. Grounding uses actual blade vertices rather than bounding-box corners. The recorded pelvis-centred motion and illustrative trajectory remain unchanged; this does not certify the action as a biomechanically accurate Axel.

## Motion and height limitations

The MotionExpert coordinates are pelvis-centred. The displayed lift is a relative foot-position proxy; the ice clearance is illustrative. Neither gives a calibrated world-space jump height or verified flight phase. The five-frame smoothing and playback interval are presentation choices. The old Python builder creates the previous procedural version; use the Node builder for this version.

## Procedural face details

- No additional third-party head mesh or texture was downloaded. The viewer adds a low-complexity head surface and facial features with the already-bundled Three.js geometry primitives (`SphereGeometry` and `BufferGeometry`) so the page remains self-contained and works offline.
- Three.js geometry references: <https://threejs.org/docs/pages/SphereGeometry.html>, <https://threejs.org/docs/pages/BufferGeometry.html>, and <https://threejs.org/manual/pages/primitives.html>.
- The head is a generic stylized replacement aligned to the recorded neck/head direction, not an athlete scan. Original head-weighted triangles are removed, and the new opaque head is centered above the neck rather than offset in front of the old head. The earlier claim that head masking necessarily removes the torso was incorrect; the corrected filtering preserves the body.


## MotionExpert
Source: https://github.com/MotionXperts/MotionExpert (Apache-2.0 repository license, verified 2026-11-05). The released dataset is described in its README and stored in its dataset directory. This existing demo uses one Single Axel sequence, cropped to 200 display frames, mirrored, smoothed and combined with illustrative travel. The motion is not Olympic athlete capture. Full repository license: LICENSE.MOTIONEXPERT.txt.

## Three.js and GLTFLoader
Three.js by the Three.js authors, MIT license. Source: https://github.com/mrdoob/three.js. Full license: LICENSE.THREE.txt.

## Integration changes
The original demo was copied from the user’s existing generated Single Axel page; only presentation CSS was changed to separate its canvas, statistics and controls. The overlay and return navigation are part of the CSC316 application.

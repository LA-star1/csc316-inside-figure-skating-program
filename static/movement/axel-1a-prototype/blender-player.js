import { findExportedNameMatch } from './camera-name.mjs';

const THREE = globalThis.THREE;
const GLTFLoader = THREE?.GLTFLoader;

const FILE = '/movement/axel-1a-prototype/single-axel-1a-human-rink-v69-web.glb';
const CAMERA_NAMES = [
	'Action side view · horizontal follow composition',
	'Action front view',
	'Skate inspection · close view',
	'Arena overview · full 60×30 rink',
];
const canvas = document.querySelector('#blender-stage');
const shell = document.querySelector('#stage-shell');
const message = document.querySelector('#stage-message');
const playButton = document.querySelector('#blender-play');
const resetButton = document.querySelector('#blender-reset');
const frameSlider = document.querySelector('#blender-frame');
const counter = document.querySelector('#blender-counter');
const speedSelect = document.querySelector('#blender-speed');
const fullscreenButton = document.querySelector('#blender-fullscreen');
const cameraButtons = [...document.querySelectorAll('[data-camera]')];

let renderer;
let modelScene;
let sceneObjects = [];
let activeCamera;
let mixer;
let clipActions = [];
let animationTrackCount = 0;
let duration = 0;
let frameCount = 160;
let playbackTime = 0;
let speed = Number(speedSelect.value);
let playing = false;
let lastTick = 0;
let inspectionRunner;
let inspectionBoot;
let inspectionCamera;
let followInspection = false;
const inspectionDirection = new THREE.Vector3();
const inspectionTarget = new THREE.Vector3();
const inspectionCameraPosition = new THREE.Vector3();
const inspectionBox = new THREE.Box3();

const phaseAt = (frame) => {
	if (frame < 38) return 'Approach · simulated';
	if (frame === 38) return 'Take-off · simulated';
	if (frame < 72) return 'Ascent · simulated';
	if (frame === 72) return 'Apex · simulated';
	if (frame < 92) return 'Descent · simulated';
	if (frame === 92) return 'Landing · simulated';
	return 'Exit glide · simulated';
};

function frameFromTime(time) {
	return Math.min(frameCount - 1, Math.max(0, Math.round(time / duration * (frameCount - 1))));
}

function updateInspectionCamera() {
	if (!followInspection || !inspectionRunner || !activeCamera) return;
	modelScene.updateMatrixWorld(true);
	inspectionBox.setFromObject(inspectionRunner);
	if (inspectionBoot) inspectionBox.union(new THREE.Box3().setFromObject(inspectionBoot));
	inspectionBox.getCenter(inspectionTarget);
	inspectionTarget.y += 0.04;
	const size = inspectionBox.getSize(new THREE.Vector3());
	const halfFov = THREE.MathUtils.degToRad(inspectionCamera.fov * 0.5);
	const aspect = inspectionCamera.aspect || 1.5;
	const verticalFit = size.y * 0.5 / Math.tan(halfFov);
	const horizontalFit = size.x * 0.5 / (Math.tan(halfFov) * aspect);
	const fitDistance = Math.max(verticalFit, horizontalFit, size.z * 0.5) * 2.0;
	inspectionCameraPosition.copy(inspectionTarget).addScaledVector(inspectionDirection, fitDistance);
	if (activeCamera.parent) {
		activeCamera.parent.updateWorldMatrix(true, false);
		activeCamera.position.copy(activeCamera.parent.worldToLocal(inspectionCameraPosition.clone()));
	} else {
		activeCamera.position.copy(inspectionCameraPosition);
	}
	activeCamera.up.set(0, 1, 0);
	activeCamera.lookAt(inspectionTarget);
	activeCamera.updateMatrixWorld(true);
}

function resize() {
	if (!renderer || !activeCamera) return;
	const width = Math.max(1, shell.clientWidth);
	const height = Math.max(1, shell.clientHeight);
	renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
	renderer.setSize(width, height, false);
	if (activeCamera.isPerspectiveCamera) {
		activeCamera.aspect = width / height;
		activeCamera.updateProjectionMatrix();
	}
	renderer.render(modelScene, activeCamera);
}

function setPlaybackTime(time, updateSlider = true) {
	if (!activeCamera) throw new Error('The v69 GLB camera was not resolved.');
	playbackTime = Math.max(0, Math.min(duration, time));
	mixer.setTime(playbackTime);
	updateInspectionCamera();
	const frame = frameFromTime(playbackTime);
	if (updateSlider) frameSlider.value = String(frame);
	counter.textContent = `Frame ${frame + 1} / ${frameCount} · ${phaseAt(frame)}`;
	renderer.render(modelScene, activeCamera);
}

function chooseCamera(name) {
	const sourceCamera = findExportedNameMatch(sceneObjects, name);
	if (!sourceCamera?.isCamera) {
		const available = [];
		modelScene.traverse((object) => { if (object.isCamera) available.push(`${object.name}:${object.constructor.name}`); });
		throw new Error(`Camera not found: ${name}; available cameras: ${available.join(', ') || '(none)'}`);
	}
	if (activeCamera) modelScene.remove(activeCamera);
	sourceCamera.updateWorldMatrix(true, false);
	activeCamera = sourceCamera;
	followInspection = sourceCamera === inspectionCamera;
	updateInspectionCamera();
	for (const button of cameraButtons) {
		button.setAttribute('aria-pressed', String(button.dataset.camera === name));
	}
	resize();
}

function animate(now) {
	requestAnimationFrame(animate);
	if (!renderer || !activeCamera) return;
	const elapsed = lastTick ? Math.min((now - lastTick) / 1000, 0.1) : 0;
	lastTick = now;
	if (playing) {
		const next = playbackTime + elapsed * speed;
		setPlaybackTime(next);
		if (next >= duration) {
			playing = false;
			playButton.textContent = 'Play';
		}
	}
	renderer.render(modelScene, activeCamera);
}

async function start() {
	try {
		if (!THREE || !GLTFLoader) throw new Error('The bundled Three.js runtime did not load.');
		renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
		renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
		renderer.outputColorSpace = THREE.SRGBColorSpace;
		renderer.toneMapping = THREE.ACESFilmicToneMapping;
		renderer.toneMappingExposure = 1.05;
		modelScene = new THREE.Scene();
		modelScene.background = new THREE.Color('#c9dce1');
		modelScene.add(new THREE.HemisphereLight(0xeaf7ff, 0x415667, 1.5));
		const key = new THREE.DirectionalLight(0xfff6e9, 2.3);
		key.position.set(-8, 12, 10);
		modelScene.add(key);
		const fill = new THREE.DirectionalLight(0xc4e8ff, 1.0);
		fill.position.set(10, 7, -8);
		modelScene.add(fill);

		const loader = new GLTFLoader();
		const gltf = await loader.loadAsync(FILE);
		modelScene.add(gltf.scene);
		modelScene.traverse((object) => sceneObjects.push(object));
		inspectionRunner = findExportedNameMatch(sceneObjects, 'Right skate · website blade v64');
		inspectionBoot = findExportedNameMatch(sceneObjects, 'Right skate · website boot v64');
		inspectionCamera = findExportedNameMatch(sceneObjects, CAMERA_NAMES[2]);
		if (!inspectionRunner || !inspectionBoot || !inspectionCamera?.isCamera) {
			throw new Error('The v69 skate inspection camera or figure blade is missing.');
		}
		const clips = gltf.animations;
		animationTrackCount = clips.reduce((count, clip) => count + clip.tracks.length, 0);
		if (!clips.length || animationTrackCount < 80) {
			throw new Error('The v69 GLB did not contain the expected articulated 3D action.');
		}
		duration = Math.max(...clips.map((clip) => clip.duration));
		if (!Number.isFinite(duration) || duration <= 0) throw new Error('The v69 animation has no usable duration.');
		mixer = new THREE.AnimationMixer(gltf.scene);
		clipActions = clips.map((clip) => {
			const action = mixer.clipAction(clip);
			action.setLoop(THREE.LoopOnce, 1);
			action.clampWhenFinished = true;
			action.play();
			return action;
		});
		mixer.setTime(duration * (94 - 1) / (frameCount - 1));
		modelScene.updateMatrixWorld(true);
		inspectionBox.setFromObject(inspectionRunner);
		inspectionBox.union(new THREE.Box3().setFromObject(inspectionBoot));
		inspectionBox.getCenter(inspectionTarget);
		inspectionCamera.getWorldPosition(inspectionCameraPosition);
		inspectionDirection.copy(inspectionCameraPosition).sub(inspectionTarget).normalize();
		inspectionCamera.zoom = 1.0;
		inspectionCamera.near = 0.01;
		inspectionCamera.updateProjectionMatrix();
		mixer.setTime(0);
		modelScene.updateMatrixWorld(true);
		chooseCamera(CAMERA_NAMES[0]);
		frameSlider.disabled = false;
		playButton.disabled = false;
		resetButton.disabled = false;
		fullscreenButton.disabled = false;
		setPlaybackTime(0);
		message.textContent = `Ready · Blender v69 · ${(duration).toFixed(2)} s · ${animationTrackCount} animated channels · ${renderer.info.render.calls} draw calls`;
		requestAnimationFrame(animate);
	} catch (error) {
		console.error('Blender v69 player failed to load:', error);
		message.textContent = `3D playback failed: ${error.message}. Open README for the .blend and fallback previews.`;
		message.setAttribute('data-error', 'true');
	}
}

playButton.addEventListener('click', () => {
	if (!duration) return;
	if (!playing && playbackTime >= duration) setPlaybackTime(0);
	playing = !playing;
	lastTick = 0;
	playButton.textContent = playing ? 'Pause' : 'Play';
});

resetButton.addEventListener('click', () => {
	playing = false;
	playButton.textContent = 'Play';
	setPlaybackTime(0);
});

frameSlider.addEventListener('input', () => {
	playing = false;
	playButton.textContent = 'Play';
	setPlaybackTime((Number(frameSlider.value) / (frameCount - 1)) * duration, false);
});

speedSelect.addEventListener('change', () => { speed = Number(speedSelect.value); });
cameraButtons.forEach((button) => button.addEventListener('click', () => chooseCamera(button.dataset.camera)));
fullscreenButton.addEventListener('click', async () => {
	if (!document.fullscreenElement) await shell.requestFullscreen();
	else await document.exitFullscreen();
	resize();
});
window.addEventListener('resize', resize);
new ResizeObserver(resize).observe(shell);
start();
window.addEventListener('keydown', (event) => {
	if (event.key !== 'Escape' || window.parent === window) return;
	window.parent.postMessage({ type: 'motion-escape' }, location.origin);
});




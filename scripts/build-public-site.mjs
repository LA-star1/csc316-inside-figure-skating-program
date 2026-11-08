import { cpSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { build } from 'vite';
import viteConfig from '../vite.config.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'dist');

await build({
	...viteConfig,
	configFile: false,
	root,
	publicDir: false,
	build: {
		...viteConfig.build,
		outDir: output,
		emptyOutDir: true
	}
});

const publicFiles = [
	'data/competition.json',
	'movement-reference.png',
	'movement/index.html',
	'movement/LICENSE.MOTIONEXPERT.txt',
	'movement/LICENSE.THREE.txt',
	'movement/THIRD_PARTY_NOTICES.md',
	'movement/axel-1a-prototype/README.md',
	'movement/axel-1a-prototype/blender-player.js',
	'movement/axel-1a-prototype/index.html',
	'movement/axel-1a-prototype/player.html',
	'movement/axel-1a-prototype/vendor/GLTFLoader.js',
	'movement/axel-1a-prototype/vendor/three.umd.js',
	...[
		'single-axel-1a-human-rink-v67-frame039-side.png',
		'single-axel-1a-human-rink-v67-frame074-front.png',
		'single-axel-1a-human-rink-v67-frame074-side.png',
		'single-axel-1a-human-rink-v67-frame074-skate-inspection.png',
		'single-axel-1a-human-rink-v67-frame093-side.png',
		'single-axel-1a-human-rink-v67-public.blend',
		'single-axel-1a-human-rink-v67-web.glb'
	].map((name) => `movement/axel-1a-prototype/${name}`)
];

for (const relative of publicFiles) {
	const source = path.join(root, 'static', relative);
	const destination = path.join(output, relative);
	mkdirSync(path.dirname(destination), { recursive: true });
	cpSync(source, destination);
}

console.log(`Prepared ${publicFiles.length} curated static files in dist; full historical Blender assets stay out of the public build.`);

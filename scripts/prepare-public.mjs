// Copies the atlas page and its skill index into public/, so the static export serves them at /atlas.html and /skills-index.js.
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
mkdirSync(join(root, 'public'), { recursive: true });
copyFileSync(join(root, 'docs', 'skill-atlas.html'), join(root, 'public', 'atlas.html'));
copyFileSync(join(root, 'docs', 'skills-index.js'), join(root, 'public', 'skills-index.js'));
console.log('Copied the atlas and the skill index into public/');

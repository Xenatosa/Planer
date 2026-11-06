const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..', '..');
function build() {
  execFileSync('python3', ['baue_html.py'], { cwd: root, env: { ...process.env, RELIEF_NEU: '1' }, stdio: 'pipe' });
  return fs.readFileSync(path.join(root, 'neu', 'index.html'));
}
const first = build();
const second = build();
if (!crypto.timingSafeEqual(crypto.createHash('sha256').update(first).digest(), crypto.createHash('sha256').update(second).digest())) throw new Error('HTML-Ausgabe ist nicht deterministisch');
const html = first.toString('utf8');
for (const text of ['Relief-Neu Geländemesh', 'neu_mesh_tiles', 'window.__test.neuMeshDraw', 'D1', 'G1', 'D2']) {
  if (!html.includes(text)) throw new Error(`Viewer-Integration fehlt: ${text}`);
}
if (html.includes('<script src=')) throw new Error('Viewer enthaelt externe Skripte');
console.log(JSON.stringify({ offline: true, three_d_viewer: true, kacheln: ['D1', 'G1', 'D2'] }));

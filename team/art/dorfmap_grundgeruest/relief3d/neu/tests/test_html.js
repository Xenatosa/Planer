const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..', '..');
function build() {
  const env = { ...process.env, RELIEF_NEU: '1' };
  execFileSync('python3', ['gen_relief.py'], { cwd: root, env, stdio: 'pipe' });
  execFileSync('python3', ['baue_html.py'], { cwd: root, env, stdio: 'pipe' });
  return fs.readFileSync(path.join(root, 'index.html'));
}
const first = build();
const second = build();
if (!crypto.timingSafeEqual(crypto.createHash('sha256').update(first).digest(), crypto.createHash('sha256').update(second).digest())) throw new Error('HTML-Ausgabe ist nicht deterministisch');
const html = first.toString('utf8');
for (const text of ['Relief-Neu Geländemesh', 'neu_mesh_tiles', 'window.__test.neuMeshDraw', 'D1', 'G1', 'D2']) {
  if (!html.includes(text)) throw new Error(`Viewer-Integration fehlt: ${text}`);
}
if (!html.includes('data-core="relief-neu-mesh"')) throw new Error('Echter Mesh-Viewer fehlt');
for (const tile of ['D1', 'G1', 'D2']) {
  if (!html.includes(`data-tile="${tile}"`)) throw new Error(`Prototypkachel ${tile} fehlt`);
}
if (!html.includes('window.RELIEF_NEU_VIEWER=1')) throw new Error('main.js waehlt den Relief-Neu-Meshpfad nicht');
if (!html.includes('separate Wände D1/G1')) throw new Error('Separate Wandebene fehlt');
if (/<(?:script|link|img)\b[^>]*(?:src|href)=["']https?:\/\//i.test(html)) throw new Error('Viewer enthaelt externe Ressourcen');
if (html.includes('<script src=')) throw new Error('Viewer enthaelt externe Skripte');
console.log(JSON.stringify({ offline: true, mesh: true, kacheln: ['D1', 'G1', 'D2'] }));

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
for (const tile of ['D1', 'G1', 'D2']) {
  if (!html.includes(`debug_${tile}.png`)) throw new Error(`Diagnoseansicht ${tile} fehlt`);
}
if ((html.match(/<section>/g) || []).length !== 3) throw new Error('Viewer zeigt nicht genau drei Prototypkacheln');
if (/https?:\/\//.test(html)) throw new Error('Viewer enthaelt externe Ressourcen');
console.log(JSON.stringify({ offline: true, kacheln: ['D1', 'G1', 'D2'] }));

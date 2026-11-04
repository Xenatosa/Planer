'use strict';
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const root = path.resolve(__dirname, '../..');
const delta = path.resolve(__dirname, '../delta.py');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'test-neu-delta-'));
const before = path.join(tmp, 'vor'), after = path.join(tmp, 'nach');
fs.mkdirSync(before); fs.mkdirSync(after);
function save(dir, name, value) { fs.writeFileSync(path.join(dir, name), JSON.stringify(value)); }
for (const [dir, n] of [[before, 1], [after, 2]]) {
  save(dir, 'regeln.json', { treffer: Array.from({ length: n }, () => ({ regel: 'R5_loch', feld: 'D1' })) });
  save(dir, 'r8.json', { je_feld: { D2: { R8_stufe: 0 } } });
  save(dir, 'r9.json', { je_feld: {} });
  save(dir, 'loch.json', { offen_innen: 0, punkte: [] });
  save(dir, 'nahbild_werte.json', { images: [
    { tile: 'D1', mode: 'clay', camera: 'draufsicht', kantenzaehne: n },
    { tile: 'D1', mode: 'textur', camera: 'draufsicht', kantenzaehne: n * 1000 },
  ] });
}
let r = spawnSync('python3', [delta, '--before', before, '--after', after, '--out', path.join(tmp, 'delta.md')], { cwd: root, encoding: 'utf8' });
assert.strictEqual(r.status, 1, r.stdout + r.stderr);
assert.match(fs.readFileSync(path.join(tmp, 'delta.md'), 'utf8'), /D1/);
for (const f of fs.readdirSync(after)) {
  const p = path.join(after, f);
  if (f === 'regeln.json') save(after, f, { treffer: [{ regel: 'R5_loch', feld: 'D1' }] });
  if (f === 'nahbild_werte.json') save(after, f, { images: [
    { tile: 'D1', mode: 'clay', camera: 'draufsicht', kantenzaehne: 1 },
    { tile: 'D1', mode: 'textur', camera: 'draufsicht', kantenzaehne: 99999 },
  ] });
}
r = spawnSync('python3', [delta, '--before', before, '--after', after, '--out', path.join(tmp, 'delta-zero.md')], { cwd: root, encoding: 'utf8' });
assert.strictEqual(r.status, 0, r.stdout + r.stderr);
process.stdout.write(JSON.stringify({ test: 'delta', anstieg_exit: 1, stabil_exit: 0 }) + '\n');

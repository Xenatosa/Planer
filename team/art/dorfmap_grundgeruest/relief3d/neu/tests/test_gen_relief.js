'use strict';
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const root = path.resolve(__dirname, '../..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'test-neu-gen-'));
const source = path.join(tmp, 'source.json.gz');
const a = path.join(tmp, 'a'), b = path.join(tmp, 'b');
const control = path.join(tmp, 'control');
function py(code, args = []) {
  const r = spawnSync('python3', ['-c', code, ...args], { cwd: root, encoding: 'utf8' });
  if (r.status !== 0) throw new Error(`${r.stdout}\n${r.stderr}`);
  return r.stdout.trim();
}
py('from neu.tests.helpers import make_data; from pathlib import Path; import sys; make_data(Path(sys.argv[1]))', [source]);
py('from neu.gen_relief import build; from pathlib import Path; import sys; build(Path(sys.argv[1]), Path(sys.argv[2]), "1")', [source, a]);
py('from neu.gen_relief import build; from pathlib import Path; import sys; build(Path(sys.argv[1]), Path(sys.argv[2]), "1")', [source, b]);
py('from neu.gen_relief import build; from pathlib import Path; import sys; build(Path(sys.argv[1]), Path(sys.argv[2]))', [source, control]);
assert.deepStrictEqual(fs.readFileSync(path.join(a, 'relief_daten_neu.json.gz')), fs.readFileSync(path.join(b, 'relief_daten_neu.json.gz')));
const meta = JSON.parse(fs.readFileSync(path.join(a, 'relief_neu_meta.json'), 'utf8'));
assert.strictEqual(meta.quellspalten_diff_summe, 0);
assert.ok(Object.values(meta.D2_anzeige_bytegleich).every(Boolean));
assert.ok(meta.geaenderte_gb_punkte > 0);
const controlMeta = JSON.parse(fs.readFileSync(path.join(control, 'relief_neu_meta.json'), 'utf8'));
assert.strictEqual(controlMeta.variante, '0');
assert.strictEqual(controlMeta.geaenderte_gb_punkte, 0);
process.stdout.write(JSON.stringify({ test: 'gen_relief', deterministisch: true, default: controlMeta.variante, quellspalten_diff: meta.quellspalten_diff_summe, d2: meta.D2_anzeige_bytegleich }) + '\n');

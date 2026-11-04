'use strict';
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const root = path.resolve(__dirname, '../..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'test-neu-cams-'));
const source = path.join(tmp, 'source.json.gz'), out = path.join(tmp, 'cameras.json');
const code = `from pathlib import Path
import json,sys,gzip
from neu.tests.helpers import make_data
from neu.nahbild import camera_list
p=Path(sys.argv[1]); d=make_data(p)
Path(sys.argv[2]).write_text(json.dumps(camera_list(d, ('D1','G1','D2'))))`;
const r = spawnSync('python3', ['-c', code, source, out], { cwd: root, encoding: 'utf8' });
if (r.status !== 0) throw new Error(`${r.stdout}\n${r.stderr}`);
const cams = JSON.parse(fs.readFileSync(out, 'utf8'));
assert.strictEqual(cams.length, 18);
for (const tile of ['D1', 'G1', 'D2']) assert.strictEqual(cams.filter(c => c.n.startsWith(`${tile}_`)).length, 6);
assert.strictEqual(cams.find(c => c.n === 'D1_streiflicht_west').az, 45);
assert.strictEqual(cams.find(c => c.n === 'D1_streiflicht_ost').az, 225);
process.stdout.write(JSON.stringify({ test: 'nahbild-kameras', kacheln: 3, bilder_pro_modus: cams.length }) + '\n');

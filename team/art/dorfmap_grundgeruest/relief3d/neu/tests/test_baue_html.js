'use strict';
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { gzipSync } = require('zlib');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '../..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'test-neu-html-'));
fs.writeFileSync(path.join(tmp, 'relief_daten_neu.json.gz'), gzipSync(Buffer.from('{}')));
const r = spawnSync('python3', ['neu/baue_html.py'], {
  cwd: root,
  encoding: 'utf8',
  env: { ...process.env, RELIEF_NEU_DIR: tmp, NODE_DIR: '/tmp/w3' },
});
assert.strictEqual(r.status, 0, r.stdout + r.stderr);
const htmlPath = path.join(tmp, 'index_neu.html');
const html = fs.readFileSync(htmlPath, 'utf8');
assert.match(html, /Epodarien Dorf – Relief NEU Prototyp pnahbild/);
assert.match(html, /window\.NEU_GZ="H4sI/);
assert.match(html, /window\.__test=/);
process.stdout.write(JSON.stringify({ test: 'baue-html', standalone: true, groesse: fs.statSync(htmlPath).size }) + '\n');

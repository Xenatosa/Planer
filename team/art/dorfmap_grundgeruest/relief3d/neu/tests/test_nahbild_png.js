'use strict';
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const zlib = require('zlib');
const { spawnSync } = require('child_process');
const analyzer = path.resolve(__dirname, '../nahbild.js');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'test-neu-png-'));
const image = path.join(tmp, 'sample.png'), out = path.join(tmp, 'metrics.json');
function crc32(buf) {
  let c = 0xffffffff;
  for (const byte of buf) { c ^= byte; for (let k = 0; k < 8; k++) c = (c >>> 1) ^ ((c & 1) ? 0xedb88320 : 0); }
  return (c ^ 0xffffffff) >>> 0;
}
function chunk(name, data) {
  const type = Buffer.from(name), body = Buffer.concat([type, data]), len = Buffer.alloc(4), crc = Buffer.alloc(4);
  len.writeUInt32BE(data.length); crc.writeUInt32BE(crc32(body));
  return Buffer.concat([len, body, crc]);
}
const w = 48, h = 48, raw = Buffer.alloc(h * (1 + w * 3));
for (let y = 0; y < h; y++) {
  raw[y * (w * 3 + 1)] = 0;
  for (let x = 0; x < w; x++) {
    const dark = x >= 8 && x < 13 && y >= 8 && y < 13;
    const bright = x >= 30 && x < 35 && y >= 30 && y < 35;
    const value = dark ? 15 : bright ? 250 : 150, i = y * (w * 3 + 1) + 1 + x * 3;
    raw[i] = raw[i + 1] = raw[i + 2] = value;
  }
}
const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 2;
fs.writeFileSync(image, Buffer.concat([Buffer.from('89504e470d0a1a0a', 'hex'), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw)), chunk('IEND', Buffer.alloc(0))]));
const run = spawnSync('node', [analyzer, '--files', image, '--out', out], { encoding: 'utf8' });
if (run.status !== 0) throw new Error(`${run.stdout}\n${run.stderr}`);
const result = JSON.parse(fs.readFileSync(out, 'utf8')).images[0];
assert.ok(result.loecher >= 1, JSON.stringify(result));
assert.ok(result.flecken >= 1, JSON.stringify(result));
process.stdout.write(JSON.stringify({ test: 'nahbild-png', loecher: result.loecher, flecken: result.flecken }) + '\n');

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { gunzipSync } = require('node:zlib');

const relief3d = path.resolve(__dirname, '../..');
const mapRoot = path.resolve(relief3d, '..');
const sourcePath = path.join(mapRoot, 'raster_c20_z25_zellen.csv');
const legacyPath = path.join(relief3d, 'relief_daten.json.gz');

function crop(raw, sourceWidth, x0, x1, y0, y1, channels, itemSize) {
  const stride = sourceWidth * channels * itemSize;
  const rowBytes = ((x1 - x0) * 2 + 1) * channels * itemSize;
  const rows = [];
  for (let y = y0 * 2; y <= y1 * 2; y++) {
    const start = y * stride + x0 * 2 * channels * itemSize;
    rows.push(raw.subarray(start, start + rowBytes));
  }
  return Buffer.concat(rows);
}

test('source-driven tiles are deterministic and D2 reference fields stay byte-identical', () => {
  const outDir = fs.mkdtempSync(path.join(os.tmpdir(), 'relief-neu-pregeln-'));
  const r = spawnSync('python3', ['gen_relief.py'], {
    cwd: relief3d,
    encoding: 'utf8',
    env: { ...process.env, RELIEF_NEU: '1', RELIEF_NEU_DIR: outDir },
  });
  assert.equal(r.status, 0, r.stderr);
  const outputPath = path.join(outDir, 'prototyp.json');
  const first = fs.readFileSync(outputPath);
  const data = JSON.parse(first.toString('utf8'));
  assert.deepEqual(data.tiles.map(t => t.tile), ['D1', 'D2', 'G1']);
  assert.ok(data.lod1_triangle_estimate < 1_300_000);

  const secondDir = fs.mkdtempSync(path.join(os.tmpdir(), 'relief-neu-pregeln-repeat-'));
  const repeat = spawnSync('python3', ['gen_relief.py'], {
    cwd: relief3d,
    encoding: 'utf8',
    env: { ...process.env, RELIEF_NEU: '1', RELIEF_NEU_DIR: secondDir },
  });
  assert.equal(repeat.status, 0, repeat.stderr);
  assert.deepEqual(fs.readFileSync(path.join(secondDir, 'prototyp.json')), first);

  const legacy = JSON.parse(gunzipSync(fs.readFileSync(legacyPath)).toString('utf8'));
  const d2 = data.tiles.find(t => t.tile === 'D2');
  const sourceWidth = legacy.nx * legacy.rs + 1;
  for (const [name, channels, size] of [['GB', 1, 4], ['VC', 3, 1], ['WV', 1, 4], ['WEGA', 1, 1]]) {
    const expected = crop(Buffer.from(legacy[name], 'base64'), sourceWidth, 126, 168, 43, 86, channels, size);
    const actual = Buffer.from(d2.display_fields[name].bytes_b64, 'base64');
    assert.deepEqual(actual, expected, `${name} D2 bytes changed`);
  }

  const header = fs.readFileSync(sourcePath, 'utf8').split(/\r?\n/, 1)[0].split(',');
  const sourceRows = fs.readFileSync(sourcePath, 'utf8').split(/\r?\n/).slice(1).filter(Boolean).map(line => line.split(','));
  const ix = Object.fromEntries(header.map((key, i) => [key, i]));
  const sourceD2 = sourceRows.filter(row => Number(row[ix.cx]) >= 126 && Number(row[ix.cx]) < 168 && Number(row[ix.cy]) >= 43 && Number(row[ix.cy]) < 86);
  assert.equal(sourceD2.length, d2.cells.length);
  const fields = ['untergrund', 'hindernis_id', 'hindernis_art', 'wasser_eis', 'ebene', 'bauzone_bestand', 'bauzone_plan', 'begehbar', 'bebaubar'];
  for (let i = 0; i < sourceD2.length; i++) {
    for (const field of fields) assert.equal(d2.cells[i][field], sourceD2[i][ix[field]], `D2 ${field} row ${i}`);
  }
});

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const relief3d = path.resolve(__dirname, '../..');

test('source map measurement is deterministic and covers requested gaps', () => {
  const a = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'regelmessung-pregeln-')), 'a.json');
  const b = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'regelmessung-pregeln-repeat-')), 'b.json');
  for (const out of [a, b]) {
    const r = spawnSync('python3', ['pruefung/regelmessung.py', '--out', out], { cwd: relief3d, encoding: 'utf8' });
    assert.equal(r.status, 0, r.stderr);
  }
  assert.deepEqual(fs.readFileSync(a), fs.readFileSync(b));
  const d = JSON.parse(fs.readFileSync(a, 'utf8'));
  assert.equal(d.quelle.rows, 336 * 303);
  assert.equal(d.elemente.wald_boden.source_cells, 11217);
  assert.equal(d.elemente.baeume_einzeln.eligible_planting_cells_deko_baum_ok, 34705);
  assert.equal(d.elemente.gebaeude_platzhalter.E40_plan_polygons, 233);
  assert.equal(d.elemente.fels.eligible_placement_cells_deko_fels_ok, 62391);
  assert.equal(d.elemente.deko.positive_capacity_cells, 62391);
  assert.equal(d.elemente.gebirge.named_wall_bands.Nord.source_cells, 6661);
});

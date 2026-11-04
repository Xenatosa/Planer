const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const relief3d = path.resolve(__dirname, '../..');

test('HTML builder creates a self-contained D1/D2/G1 inspection page', () => {
  const outDir = fs.mkdtempSync(path.join(os.tmpdir(), 'relief-neu-html-pregeln-'));
  let r = spawnSync('python3', ['gen_relief.py'], {
    cwd: relief3d,
    encoding: 'utf8',
    env: { ...process.env, RELIEF_NEU: '1', RELIEF_NEU_DIR: outDir },
  });
  assert.equal(r.status, 0, r.stderr);
  r = spawnSync('python3', ['baue_html.py'], {
    cwd: relief3d,
    encoding: 'utf8',
    env: { ...process.env, RELIEF_NEU: '1', RELIEF_NEU_DIR: outDir },
  });
  assert.equal(r.status, 0, r.stderr);
  const page = fs.readFileSync(path.join(outDir, 'index.html'), 'utf8');
  for (const text of ['D1 · source_cell_centres_mean_at_vertices', 'D2 · locked_legacy_reference', 'G1 · source_cell_centres_mean_at_vertices', 'D2-GB SHA-256', 'Bestehenden Relief-Viewer öffnen']) {
    assert.ok(page.includes(text), `missing ${text}`);
  }
  assert.ok(!page.includes('<script src='), 'page unexpectedly depends on a remote script');
});

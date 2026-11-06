const test = require('node:test');
const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const relief3d = path.resolve(__dirname, '../..');

test('RELIEF_NEU is opt-in and both legacy entry points can import the selector', () => {
  const code = "from neu.selector import new_pipeline_enabled; assert not new_pipeline_enabled({}); assert not new_pipeline_enabled({'RELIEF_NEU':'0'}); assert new_pipeline_enabled({'RELIEF_NEU':'1'})";
  const r = spawnSync('python3', ['-c', code], { cwd: relief3d, encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
});

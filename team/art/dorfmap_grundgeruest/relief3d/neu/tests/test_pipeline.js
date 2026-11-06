const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..', '..');
function runBuild() {
  const lines = execFileSync('python3', ['gen_relief.py'], {
    cwd: root, encoding: 'utf8', env: { ...process.env, RELIEF_NEU: '1' }
  }).trim().split('\n');
  return JSON.parse(lines[lines.length - 1]);
}
const a = runBuild();
const files = ['vektor.json', 'felder.npz', 'felder.json', 'build.json', 'zellen_relief.csv', 'debug_D1.png', 'debug_G1.png', 'debug_D2.png'];
const before = Object.fromEntries(files.map(f => [f, crypto.createHash('sha256').update(fs.readFileSync(path.join(root, 'neu', f))).digest('hex')]));
const b = runBuild();
const after = Object.fromEntries(files.map(f => [f, crypto.createHash('sha256').update(fs.readFileSync(path.join(root, 'neu', f))).digest('hex')]));
if (JSON.stringify(before) !== JSON.stringify(after) || a.vektor_sha256 !== b.vektor_sha256 || a.felder_sha256 !== b.felder_sha256 || a.zellen_quell_diff !== 0 || b.zellen_quell_diff !== 0) throw new Error('Zwei Generatorlaeufe weichen ab oder aendern Zellquellen');
console.log(JSON.stringify({ deterministisch: true, hashes: after }));

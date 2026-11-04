const { execFileSync } = require('node:child_process');
const path = require('node:path');
const root = path.resolve(__dirname, '..', '..');
const code = String.raw`
import json, numpy as np
from neu.vektor import ROOT, NX, NY
from neu.felder import CELL_M
m=json.loads((ROOT/'neu/felder.json').read_text())
f=np.load(ROOT/'neu/felder.npz')
assert m['global_tiles']==56 and m['shape']==[NY,NX] and len(f.files)==6
for name in f.files:
 a=f[name]
 assert a.shape==(NY,NX) and np.isfinite(a).all(), name
 # Die Rasterkante liegt im selben globalen Feld, auch an jedem Kachelwechsel.
 # Diskrete Vorzeichenwechsel gehen von +1,2 m auf -1,2 m; das ist die
 # erwartete maximale Nachbarstufe des kontinuierlich interpolierbaren Felds.
 assert np.max(np.abs(np.diff(a,axis=1))) <= CELL_M*2+1e-4, name+' x-Naht'
 assert np.max(np.abs(np.diff(a,axis=0))) <= CELL_M*2+1e-4, name+' y-Naht'
 for edge in range(42,NX,42):
  assert np.max(np.abs(a[:,edge]-a[:,edge-1])) <= CELL_M*2+1e-4, name+' tile-x'
 for edge in range(43,NY,43):
  assert np.max(np.abs(a[edge,:]-a[edge-1,:])) <= CELL_M*2+1e-4, name+' tile-y'
for name in ('weg','wand','wasser','bauzone_bestand','bauzone_plan'):
 a=f[name]
 assert (a<0).any() and (a>0).any(), name+' Vorzeichen'
print(json.dumps({'shape':[NY,NX],'fields':sorted(f.files),'nahttest':'ok'}))
`;
console.log(execFileSync('python3', ['-c', code], { cwd: root, encoding: 'utf8' }));

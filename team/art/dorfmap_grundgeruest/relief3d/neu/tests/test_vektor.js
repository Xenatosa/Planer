const { execFileSync } = require('node:child_process');
const path = require('node:path');
const root = path.resolve(__dirname, '..', '..');
const code = String.raw`
import json, csv, numpy as np
from pathlib import Path
from shapely.geometry import Polygon
from neu.vektor import ROOT, SOURCE, _rows, NX, NY
d=json.loads((ROOT/'neu/vektor.json').read_text())
assert d['prototype_kacheln']==['D1','G1','D2']
from scipy.spatial import cKDTree
ov=list(csv.DictReader(open(ROOT.parent/'raster_c20_z25_overlay_plaetze_wege.csv', newline='')))
by_id={}
for o in ov:
 if o['weg_id']: by_id.setdefault(o['weg_id'],[]).append((int(o['cx']),int(o['cy'])))
assert d['quellen']['wegzellzahl']==sum(map(len,by_id.values()))
for wid,cells in by_id.items():
 lines=[w for w in d['wege'] if w['id']==wid]
 cloud=np.concatenate([np.asarray(w['mittellinie_m']) for w in lines])
 dist,_=cKDTree(cloud).query(np.asarray([[(x+.5)*1.2,(y+.5)*1.2] for x,y in cells]))
 width=max(w['breite_m'] for w in lines)
 assert np.all(dist<=width/2+0.85), f"{wid}: Wegzellen ausserhalb des Splines"
 assert all(len(w['mittellinie_m'])==len(w['laengsprofil_m']) for w in lines)
for c in d['kreuzungen']:
    assert Polygon(c['polygon_m']).is_valid and c['weg_ids'] and (len(c['weg_ids'])>=2 or c['platz_ids'])
for tile in ('D1','G1'):
    crossings=[]
    for c in d['kreuzungen']:
        if any((v['cx']//42, v['cy']//43)==(('ABCDEFGH'.index(tile[0])),int(tile[1:])-1) for v in c['quellzellen']): crossings.append(c)
    assert crossings, f"keine Kreuzungsflaeche in {tile}"
assert d['waende'] and all(w['breite_min_m']>=1.2 and len(w['hoehe_oben_m'])==len(w['hoehe_unten_m'])==len(w['mittellinie_m']) for w in d['waende'])
assert d['wasser'] and d['bauzonen']['bestand'] and d['bauzonen']['plan']
assert all('innenringe_m' in f for f in d['wasser']+d['bauzonen']['bestand']+d['bauzonen']['plan'])
ends={tile:[e for w in d['wege'] for e in w['wegenden'] if e['kachel']==tile] for tile in ('F1','C1','G1')}
for tile in ('F1','G1'):
 assert ends[tile] and min(e['auslauf_m'] for e in ends[tile])>=4, f"Wegende ohne Auslauf in {tile}"
assert not ends['C1'], 'C1 hat laut Overlay keine Quelle fuer einen Wegendpunkt'
print(json.dumps({'wegzellen':d['quellen']['wegzellzahl'],'splines':len(d['wege']),'kreuzungen_D1_G1':True,'waende':len(d['waende']),'auslaeufe':{k:len(v) for k,v in ends.items()}}))
`;
console.log(execFileSync('python3', ['-c', code], { cwd: root, encoding: 'utf8' }));

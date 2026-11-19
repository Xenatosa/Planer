"""Laedt einen detail_v2-Datensatz (Formatannahmen: PLAN_QA_DV2.md Abschnitt 2) in einen Kontext."""
import json
from pathlib import Path
import numpy as np
from . import glb
from .geom import KLASSEN, Ortung

QA = Path(__file__).resolve().parents[1]
STANDARD_KONFIG = QA / 'konfig.json'


def lade_konfig(pfad=None):
    k = json.loads(Path(pfad or STANDARD_KONFIG).read_text())
    return k


def _klasse(prim):
    e = prim['extras']
    for k in ('klasse', 'flaeche'):
        if k in e:
            v = e[k]
            return KLASSEN[v] if isinstance(v, int) else str(v)
    nm = prim['mesh'] or prim['knoten']
    for k in KLASSEN:
        if nm.endswith('_' + k): return k
    return 'grund'


class Fehlt(Exception):
    """Eingabe fehlt -> Regel 'offen' (Exit 2)."""


class Kontext:
    def __init__(self, wurzel, referenz=None, abnahme=None, konfig=None):
        self.wurzel = Path(wurzel); self.k = lade_konfig(konfig)
        self.referenz = Path(referenz) if referenz else None
        self.abnahme = Path(abnahme) if abnahme else None
        self._cache = {}

    # ---------- Mesh ----------
    @property
    def manifest(self):
        if 'manifest' not in self._cache:
            p = self.wurzel / self.k['mesh_manifest']
            if not p.exists(): raise Fehlt(f'{p} fehlt')
            self._cache['manifest'] = json.loads(p.read_text())
        return self._cache['manifest']

    @property
    def kacheln(self):
        """{id: {'bounds', 'prims': [...] }} – Primitive mit Feld 'art' (gelaende|wasser|wand) und 'klasse'."""
        if 'kacheln' not in self._cache:
            out = {}
            for kd in self.manifest['kacheln']:
                p = (self.wurzel / self.k['mesh_manifest']).parent / kd['datei']
                if not p.exists(): raise Fehlt(f'{p} fehlt')
                _, prims = glb.lies_glb(p)
                for pr in prims:
                    nm = (pr['mesh'] or pr['knoten']).lower()
                    pr['art'] = 'wasser' if nm.startswith('wasser') else 'wand' if nm.startswith('wand') else 'gelaende'
                    pr['klasse'] = _klasse(pr) if pr['art'] == 'gelaende' else pr['art']
                    pr['kachel'] = kd['id']
                out[kd['id']] = {'bounds': kd['bounds'], 'prims': prims, 'dreiecke_manifest': kd.get('dreiecke')}
            self._cache['kacheln'] = out
        return self._cache['kacheln']

    def netz(self, arten=('gelaende',), modelle=False):
        """Verschweisstes Netz (float32-bitgleiche Positionen) -> dict V, T, klasse(T), kachel(T), uv0/uv1/uv2 je Ecke."""
        key = ('netz', arten, modelle)
        if key in self._cache: return self._cache[key]
        prims = [p for kd in self.kacheln.values() for p in kd['prims'] if p['art'] in arten]
        if modelle: prims += [p for m in self.modelle().values() for p in m]
        if not prims: raise Fehlt(f'keine Primitive der Art {arten}')
        P32 = np.vstack([p['pos32'] for p in prims]).astype(np.float32)
        off = np.cumsum([0] + [len(p['pos32']) for p in prims])
        T = np.vstack([p['idx'] + o for p, o in zip(prims, off[:-1])])
        key32 = np.ascontiguousarray(P32).view(np.dtype((np.void, 12))).ravel()
        _, first, inv = np.unique(key32, return_index=True, return_inverse=True)
        V = P32[first].astype(np.float64)
        TT = inv.ravel()[T]
        def ecke(name, dim=2):
            if not all(name in p for p in prims): return None
            A = np.vstack([p[name] for p in prims]); return A[T]
        kl = np.concatenate([[p['klasse']] * len(p['idx']) for p in prims])
        kc = np.concatenate([[p.get('kachel', 'modell')] * len(p['idx']) for p in prims])
        art = np.concatenate([[p['art']] * len(p['idx']) for p in prims])
        r = {'V': V, 'T': TT, 'klasse': kl, 'kachel': kc, 'art': art, 'uv0': ecke('uv0'), 'uv1': ecke('uv1'), 'uv2': ecke('uv2'),
             'roh': prims}
        self._cache[key] = r
        return r

    def ortung(self, arten=('gelaende',), modelle=False):
        key = ('ort', arten, modelle)
        if key not in self._cache:
            n = self.netz(arten, modelle); self._cache[key] = Ortung(n['V'], n['T'])
        return self._cache[key]

    def modelle(self):
        if 'modelle' not in self._cache:
            out = {}
            d = self.wurzel / self.k['modelle_ordner']
            for p in sorted(d.glob('*.glb')) if d.exists() else []:
                _, prims = glb.lies_glb(p)
                for pr in prims:
                    nm = (pr['knoten'] or pr['mesh']).lower(); pr['art'] = 'wand' if 'wand' in p.stem.lower() else 'modell'
                    pr['klasse'] = pr['art']; pr['teil'] = nm; pr['kachel'] = 'modell'
                out[p.stem] = prims
            self._cache['modelle'] = out
        return self._cache['modelle']

    # ---------- Vektoren ----------
    def geojson(self, name, pflicht=True):
        p = self.wurzel / self.k['vektor_ordner'] / name
        if not p.exists():
            if pflicht: raise Fehlt(f'{p} fehlt')
            return []
        return json.loads(p.read_text()).get('features', [])

    def linien(self, quelle):
        """quelle = {'datei', 'filter'?: {prop: wert|[werte]}, 'raender'?: bool} -> Liste (np.array n x 2, geschlossen, props)."""
        out = []
        for f in self.geojson(quelle['datei'], pflicht=quelle.get('pflicht', True)):
            pr = f.get('properties') or {}
            ok = True
            for k, v in (quelle.get('filter') or {}).items():
                vv = v if isinstance(v, list) else [v]
                if pr.get(k) not in vv: ok = False
            if not ok: continue
            g = f['geometry']; t = g['type']; c = g['coordinates']
            if t == 'LineString': out.append((np.array(c, float), False, pr))
            elif t == 'MultiLineString': out += [(np.array(x, float), False, pr) for x in c]
            elif t in ('Polygon', 'MultiPolygon') and quelle.get('raender', True):
                polys = [c] if t == 'Polygon' else c
                for poly in polys:
                    for ring in poly: out.append((np.array(ring, float), True, pr))
        return out

    def polygone(self, datei, filter=None, pflicht=True):
        from shapely.geometry import shape
        out = []
        for f in self.geojson(datei, pflicht):
            pr = f.get('properties') or {}
            if filter and any(pr.get(k) not in (v if isinstance(v, list) else [v]) for k, v in filter.items()): continue
            g = shape(f['geometry'])
            if g.geom_type in ('Polygon', 'MultiPolygon'): out.append((g, pr))
        return out

    def constraint_linien(self):
        out = []
        for q in self.k['constraint_quellen']:
            for pl, geschl, pr in self.linien(q):
                out.append((pl, geschl, pr, q['datei']))
        return out

    # ---------- Datenschicht ----------
    def png(self, name):
        from PIL import Image
        p = self.wurzel / self.k['daten_ordner'] / name
        if not p.exists(): raise Fehlt(f'{p} fehlt')
        return np.array(Image.open(p))

"""Laedt einen detail_v2-Datensatz in einen Kontext.
Format verbindlich nach Entscheidung Grundgeruest 19.11.2026 (PLAN_QA_DV2.md Abschn. 8):
mesh/manifest.json {version:1, einheit:"m", ursprung:"weltecke", karte, klassen{0..5}, attribute{flaeche:"_FLAECHE"}, uv,
kacheln:[{id, glb, bbox, dreiecke, klassen_anteil}], modelle:[{id, glb, klasse}]}; Dreiecke klassenrein ueber das
Vertex-Attribut _FLAECHE, Vertices an Klassengrenzen dupliziert.
Nachtrag 19.11. (Grundgeruest, P6 #55 Runde 2): Gelaendemesh geschlossen inkl. Bachbett (Klasse 4 = Bett-Dreiecke);
Wasseroberflaeche = eigenes Modell in modelle[] (klasse 4), NICHT Teil des Gelaendes/Q1."""
import json
from pathlib import Path
import numpy as np
from . import glb
from .geom import KLASSEN, Ortung

QA = Path(__file__).resolve().parents[1]
STANDARD_KONFIG = QA / 'konfig.json'
ALIAS = {'typ': 'art', 'art': 'typ'}


def lade_konfig(pfad=None):
    return json.loads(Path(pfad or STANDARD_KONFIG).read_text())


def kachel_grenzen(kid):
    i = 'ABCDEFGH'.index(kid[0]); j = int(kid[1:]) - 1
    return [42 * i, 43 * j, 42 * (i + 1), 303 if j == 6 else 43 * (j + 1)]


class Fehlt(Exception):
    """Eingabe fehlt -> Regel 'offen' (Exit 2)."""


def _passt(pr, filt):
    for k, v in (filt or {}).items():
        val = pr.get(k, pr.get(ALIAS.get(k, ''), None))
        vv = v if isinstance(v, list) else [v]
        if val not in vv: return False
    return True


def verschweisse(P, tol=1e-4):
    """Positionsgleiche Vertices (Toleranz tol) zu einem Index zusammenfassen -> (V_rep, inv)."""
    from scipy.spatial import cKDTree
    q = np.round(P / tol).astype(np.int64)
    _, first, inv = np.unique(q, axis=0, return_index=True, return_inverse=True)
    inv = inv.ravel(); R = P[first]
    pairs = cKDTree(R).query_pairs(tol, output_type='ndarray')
    if len(pairs):                                             # Rundungsgrenzen: Union-Find
        par = np.arange(len(R))
        def f(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for a, b in pairs:
            ra, rb = f(a), f(b)
            if ra != rb: par[max(ra, rb)] = min(ra, rb)
        root = np.array([f(a) for a in range(len(R))])
        u, neu = np.unique(root, return_inverse=True)
        R = R[u]; inv = neu[inv]
    return R, inv


class Kontext:
    def __init__(self, wurzel, referenz=None, abnahme=None, konfig=None):
        self.wurzel = Path(wurzel); self.k = lade_konfig(konfig)
        self.referenz = Path(referenz) if referenz else None
        self.abnahme = Path(abnahme) if abnahme else None
        self._cache = {}

    @property
    def mesh_dir(self):
        return (self.wurzel / self.k['mesh_manifest']).parent

    @property
    def manifest(self):
        if 'manifest' not in self._cache:
            p = self.wurzel / self.k['mesh_manifest']
            if not p.exists(): raise Fehlt(f'{p} fehlt')
            self._cache['manifest'] = json.loads(p.read_text())
        return self._cache['manifest']

    def manifest_fehler(self):
        m = self.manifest; f = []
        for k, soll in (('version', 1), ('einheit', 'm'), ('ursprung', 'weltecke')):
            if m.get(k) != soll: f.append(f'{k}={m.get(k)!r} statt {soll!r}')
        if m.get('karte') != {'breite': 336, 'tiefe': 303}: f.append(f"karte={m.get('karte')}")
        kl = {int(a): b for a, b in (m.get('klassen') or {}).items()}
        if kl != dict(enumerate(KLASSEN)): f.append(f'klassen={kl}')
        if (m.get('attribute') or {}).get('flaeche') != '_FLAECHE': f.append(f"attribute={m.get('attribute')}")
        for kd in m.get('kacheln', []):
            if list(map(float, kd.get('bbox', []))) != list(map(float, kachel_grenzen(kd['id']))):
                f.append(f"{kd['id']}: bbox {kd.get('bbox')} statt {kachel_grenzen(kd['id'])}")
        return f

    @property
    def kacheln(self):
        """{id: {'bounds', 'prims'}}; Primitive mit 'art' (gelaende) und 'klasse' je Dreieck (aus _FLAECHE)."""
        if 'kacheln' not in self._cache:
            out = {}
            attr = (self.manifest.get('attribute') or {}).get('flaeche', '_FLAECHE')
            for kd in self.manifest['kacheln']:
                datei = kd.get('glb') or kd.get('datei') or f"{kd['id']}.glb"
                p = self.mesh_dir / datei
                if not p.exists(): raise Fehlt(f'{p} fehlt')
                _, prims = glb.lies_glb(p)
                for pr in prims:
                    pr['art'] = 'gelaende'; pr['kachel'] = kd['id']
                    pr['tri_klasse'], pr['gemischt'] = _tri_klasse(pr)
                out[kd['id']] = {'bounds': kd.get('bbox') or kd.get('bounds') or kachel_grenzen(kd['id']), 'prims': prims,
                                 'dreiecke_manifest': kd.get('dreiecke')}
            self._cache['kacheln'] = out
        return self._cache['kacheln']

    def netz(self, arten=('gelaende',), modelle=False, klassen=None):
        """Verschweisstes Netz (Position, Toleranz 1e-4 m) -> dict V, T, klasse(T), kachel(T), uv0/uv1/uv2 je Ecke (NaN wo fehlend)."""
        key = ('netz', arten, modelle, klassen)
        if key in self._cache: return self._cache[key]
        prims = [p for kd in self.kacheln.values() for p in kd['prims'] if p['art'] in arten]
        if modelle == 'wasser': prims += [p for mid in self.wasser_ids() for p in self.modelle()[mid]]
        elif modelle: prims += [p for mid, m in self.modelle().items() if mid not in self.wasser_ids() for p in m]
        if not prims: raise Fehlt(f'keine Primitive der Art {arten}')
        P = np.vstack([p['pos'] for p in prims])
        off = np.cumsum([0] + [len(p['pos']) for p in prims])
        T = np.vstack([p['idx'] + o for p, o in zip(prims, off[:-1])])
        kl = np.concatenate([p['tri_klasse'] for p in prims])
        kc = np.concatenate([[p.get('kachel', 'modell')] * len(p['idx']) for p in prims])
        hat = {n: np.concatenate([[n in p] * len(p['idx']) for p in prims]) for n in ('uv0', 'uv1', 'uv2')}
        if klassen is not None:
            m = np.isin(kl, klassen); T, kl, kc = T[m], kl[m], kc[m]; hat = {a: b[m] for a, b in hat.items()}
        def ecke(name):
            A = np.vstack([p[name] if name in p else np.full((len(p['pos']), 2), np.nan) for p in prims]); return A[T]
        V, inv = verschweisse(P)
        r = {'V': V, 'T': inv[T], 'T_roh': T, 'P_roh': P, 'klasse': kl, 'kachel': kc, 'hat': hat,
             'uv0': ecke('uv0'), 'uv1': ecke('uv1'), 'uv2': ecke('uv2'), 'roh': prims,
             'duplikate': int(len(P) - len(V)), 'gemischt': int(sum(p.get('gemischt', 0) for p in prims))}
        self._cache[key] = r
        return r

    def ortung(self, arten=('gelaende',), modelle=False):
        key = ('ort', arten, modelle)
        if key not in self._cache:
            n = self.netz(arten, modelle); self._cache[key] = Ortung(n['V'], n['T'])
        return self._cache[key]

    def wasser_ortung(self):
        """Ortung nur ueber die Wasserspiegel-Modelle (Fehlt, wenn keins vorhanden)."""
        if not self.wasser_ids(): raise Fehlt('kein Wasserspiegel-Modell (manifest.modelle klasse 4)')
        return self.ortung((), 'wasser')

    def wasser_ids(self):
        """Wasserspiegel-Modelle: manifest.modelle mit klasse 4 (oder id mit Praefix aus konfig wasser_modell.id_praefix)."""
        wk = self.k.get('wasser_modell', {}); kl = wk.get('klasse', 4); pf = wk.get('id_praefix', 'wasser')
        ids = []
        try: eintraege = self.manifest.get('modelle', [])
        except Fehlt: eintraege = []
        for m in eintraege:
            if (m.get('klasse') == kl or str(m.get('id', '')).lower().startswith(pf)) and m['id'] in self.modelle(): ids.append(m['id'])
        return ids

    def modelle(self):
        """{id: [prims]} aus manifest.modelle (+ optional Ordner 'modelle_ordner')."""
        if 'modelle' not in self._cache:
            out = {}
            eintraege = []
            try: eintraege = [(m['id'], self.mesh_dir / m['glb'], m.get('klasse')) for m in self.manifest.get('modelle', [])]
            except Fehlt: pass
            for mid, p, klasse in eintraege:
                if not p.exists(): continue
                _, prims = glb.lies_glb(p)
                for pr in prims:
                    pr['teil'] = (pr['knoten'] or pr['mesh']).lower(); pr['art'] = 'modell'; pr['kachel'] = 'modell'
                    tk, g = _tri_klasse(pr, klasse if klasse is not None else 5); pr['tri_klasse'], pr['gemischt'] = tk, g
                out[mid] = prims
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
        """quelle = {'datei', 'filter'?: {prop: wert|[werte]} (typ<->art austauschbar), 'raender'?: bool}
        -> Liste (np.array n x 2, geschlossen, props)."""
        out = []
        for f in self.geojson(quelle['datei'], pflicht=quelle.get('pflicht', True)):
            pr = f.get('properties') or {}
            if not _passt(pr, quelle.get('filter')): continue
            g = f['geometry']; t = g['type']; c = g['coordinates'] if 'coordinates' in g else None
            geoms = g['geometries'] if t == 'GeometryCollection' else [g]
            for gg in geoms:
                t = gg['type']; c = gg['coordinates']
                if t == 'LineString':
                    a = np.array(c, float); out.append((a, bool(len(a) > 2 and np.allclose(a[0], a[-1])), pr))
                elif t == 'MultiLineString': out += [(np.array(x, float), False, pr) for x in c]
                elif t in ('Polygon', 'MultiPolygon') and quelle.get('raender', True):
                    for poly in ([c] if t == 'Polygon' else c):
                        for ring in poly: out.append((np.array(ring, float), True, pr))
        return out

    def polygone(self, datei, filter=None, pflicht=True):
        from shapely.geometry import shape
        out = []
        for f in self.geojson(datei, pflicht):
            pr = f.get('properties') or {}
            if not _passt(pr, filter): continue
            g = shape(f['geometry'])
            if g.geom_type in ('Polygon', 'MultiPolygon'): out.append((g, pr))
        return out

    def constraint_linien(self):
        out = []
        for q in self.k['constraint_quellen']:
            for pl, geschl, pr in self.linien(q):
                out.append((pl, geschl, pr, q['datei']))
        return out


def name_in(p, n):
    return n in p


def _tri_klasse(pr, standard=0):
    """Dreiecksklasse aus _FLAECHE je Vertex; gemischte Dreiecke zaehlen (Verstoss 'klassenrein')."""
    if 'flaeche' not in pr:
        return np.full(len(pr['idx']), KLASSEN[standard], dtype=object).astype(str), 0
    f = np.round(pr['flaeche']).astype(int)[pr['idx']]
    gemischt = int((~((f[:, 0] == f[:, 1]) & (f[:, 1] == f[:, 2]))).sum())
    k = np.clip(f[:, 0], 0, 5)
    return np.array(KLASSEN)[k], gemischt

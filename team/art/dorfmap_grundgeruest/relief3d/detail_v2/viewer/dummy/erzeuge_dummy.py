"""P3 Viewer v2: Dummy-Mesh im verbindlichen Format (Grundgeruest 19.11.2026, DETAIL_V2_PLAN.md 3.2) [S].

Grob aus dem alten Raster (relief_daten.json.gz, 0,5 m): Hoehe GB, Klassen aus WV (Wasser), WEGA (Weg), Neigung (Fels).
NUR zum Testen des Viewers, kein echtes Mesh [A]. Schreibt nie nach detail_v2/mesh/ (dort liefert P2).

Ausgabe <out>/manifest.json, <out>/kacheln/A1.glb ... H7.glb, <out>/modelle/bruecke_E2.glb
  manifest = {version:1, einheit:"m", ursprung:"weltecke", karte:{breite:336,tiefe:303}, klassen:{0..5},
              attribute:{flaeche:"_FLAECHE"}, uv:{TEXCOORD_0:welt_xz_m, TEXCOORD_1:karte_norm, TEXCOORD_2:wegband},
              kacheln:[{id, glb:"kacheln/A1.glb", bbox:[x0,z0,x1,z1], dreiecke, klassen_anteil:{name: Anteil}}],
              modelle:[{id:"bruecke_E2", glb:"modelle/bruecke_E2.glb", klasse:5}]}
  glb: glTF 2.0 binaer, kein Draco, Welt-Meter ohne Node-Transform, y oben, x Ost, z Sued.
       POSITION, NORMAL, TEXCOORD_0 = (x, z) m, TEXCOORD_1 = (x/336, z/303), _FLAECHE (u8, Klasse 0-5) je Vertex,
       Dreiecke klassenrein (Vertices an Klassengrenzen doppelt). TEXCOORD_2 (Wegband) hat der Dummy nicht [A].
Kacheln A-H x 1-7, Schnitt x = 42*i, z = 43*j, Zeile 7 bis z = 303.
Klassen (Prioritaet Wasser > Bruecke > Weg > Ufer > Fels/Klippe > Grund):
  4 wasser WV > -900 | 1 weg WEGA >= 100 | 2 ufer <= 2 m neben Wasser | 3 fels_klippe Neigung > 40 Grad | 0 grund.
  Dreiecksklasse = hoechste Prioritaet unter den Rasterpunkten der Dreiecksecken + Schwerpunkt.
Aufruf (im Ordner relief3d): python3 detail_v2/viewer/dummy/erzeuge_dummy.py --out /tmp/dv2_viewer/dummy_mesh [--schritt 2] [--kacheln A1,B1]
"""
import argparse, base64, gzip, json, struct
from pathlib import Path
import numpy as np
from scipy import ndimage as nd

ROOT = Path(__file__).resolve().parents[3]          # relief3d/
NX, NZ, KX, KZ = 336, 303, 42, 43
SPALTEN = "ABCDEFGH"
KLASSEN = {0: "grund", 1: "weg", 2: "ufer", 3: "fels_klippe", 4: "wasser", 5: "bruecke"}
PRIO = np.array([0, 3, 2, 1, 5, 4])                  # Rang je Klasse: wasser 5 > bruecke 4 > weg 3 > ufer 2 > fels 1 > grund 0
VON_RANG = np.argsort(PRIO)                          # Rang -> Klasse
BRUECKE_E2 = dict(x0=186.0, x1=198.0, z0=73.0, z1=76.0, oben=0.3, dicke=0.25)   # aus relief_daten 'bruecken' (Planken 186,5-197,5 | 73,5-75,5, y 0,3) [S]


def schnitte():
    return [KX * i for i in range(9)], [KZ * j for j in range(7)] + [NZ]


def glb(name, pos, nor, uv0, uv1, fl, idx, extras):
    teile, views, acc = [], [], []
    def add(arr, ziel, typ, komp, mm=False):
        b = arr.tobytes(); off = sum(len(t) for t in teile)
        teile.append(b + b"\0" * (-len(b) % 4))
        views.append({"buffer": 0, "byteOffset": off, "byteLength": len(b), **({"target": ziel} if ziel else {})})
        a = {"bufferView": len(views) - 1, "componentType": komp, "count": int(arr.shape[0]), "type": typ}
        if mm: a["min"] = arr.min(0).tolist(); a["max"] = arr.max(0).tolist()
        acc.append(a); return len(acc) - 1
    at = {"POSITION": add(pos, 34962, "VEC3", 5126, True), "NORMAL": add(nor, 34962, "VEC3", 5126),
          "TEXCOORD_0": add(uv0, 34962, "VEC2", 5126), "TEXCOORD_1": add(uv1, 34962, "VEC2", 5126),
          "_FLAECHE": add(fl.astype(np.uint8), 34962, "SCALAR", 5121)}
    ai = add(idx.astype(np.uint32), 34963, "SCALAR", 5125)
    binb = b"".join(teile)
    js = {"asset": {"version": "2.0", "generator": "dv2 viewer dummy (P3)"}, "scene": 0, "scenes": [{"nodes": [0]}],
          "nodes": [{"mesh": 0, "name": name, "extras": extras}],
          "meshes": [{"name": name, "primitives": [{"attributes": at, "indices": ai, "mode": 4}]}],
          "buffers": [{"byteLength": len(binb)}], "bufferViews": views, "accessors": acc}
    j = json.dumps(js, separators=(",", ":")).encode(); j += b" " * (-len(j) % 4)
    return struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(j) + 8 + len(binb)) + struct.pack("<II", len(j), 0x4E4F534A) + j + struct.pack("<II", len(binb), 0x004E4942) + binb


def anteile(fl_tri):
    n = max(1, len(fl_tri)); z = np.bincount(fl_tri, minlength=6)
    return {KLASSEN[k]: round(float(z[k]) / n, 4) for k in range(6) if z[k]}


def bruecke():
    b = BRUECKE_E2; x0, x1, z0, z1, y1 = b["x0"], b["x1"], b["z0"], b["z1"], b["oben"]; y0 = y1 - b["dicke"]
    flaechen = [((0, 1, 0), [(x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)]),     # Deck oben
                ((0, -1, 0), [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)]),
                ((0, 0, -1), [(x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0)]),
                ((0, 0, 1), [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]),
                ((-1, 0, 0), [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)]),
                ((1, 0, 0), [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)])]
    pos, nor, idx = [], [], []
    for n, q in flaechen:
        s = len(pos); pos += q; nor += [n] * 4; idx += [s, s + 1, s + 2, s, s + 2, s + 3]
    pos = np.array(pos, np.float32); nor = np.array(nor, np.float32); idx = np.array(idx, np.uint32)
    uv0 = pos[:, [0, 2]].copy(); uv1 = np.stack([pos[:, 0] / NX, pos[:, 2] / NZ], -1).astype(np.float32)
    return glb("bruecke_E2", pos, nor, uv0, uv1, np.full(len(pos), 5, np.uint8), idx, {"modell": "bruecke_E2", "dummy": True}), len(idx) // 3


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--schritt", type=int, default=2)
    ap.add_argument("--kacheln", default=""); ap.add_argument("--daten", default=str(ROOT / "relief_daten.json.gz")); a = ap.parse_args()
    D = json.load(gzip.open(a.daten)); rs = int(D["rs"]); GX, GZ = NX * rs + 1, NZ * rs + 1
    lies = lambda k, t: np.frombuffer(base64.b64decode(D[k]), t)
    G = lies("GB", np.float32).reshape(GZ, GX).astype(np.float64)
    WV = lies("WV", np.float32).reshape(GZ, GX); WEGA = lies("WEGA", np.uint8)[:GX * GZ].reshape(GZ, GX)
    gy, gx = np.gradient(G, 1.0 / rs)
    N = np.dstack([-gx, np.ones_like(G), -gy]); N /= np.linalg.norm(N, axis=2, keepdims=True)
    wasser = WV > -900; ufer = nd.binary_dilation(wasser, iterations=2 * rs) & ~wasser
    fels = np.degrees(np.arctan(np.hypot(gx, gy))) > 40
    K = np.zeros(G.shape, np.uint8); K[fels] = 3; K[ufer] = 2; K[WEGA >= 100] = 1; K[wasser] = 4   # Prioritaet durch Reihenfolge
    R = PRIO[K]                                                                                  # Rang je Rasterpunkt
    out = Path(a.out); (out / "kacheln").mkdir(parents=True, exist_ok=True); (out / "modelle").mkdir(exist_ok=True)
    xs, zs = schnitte(); wahl = set(a.kacheln.split(",")) if a.kacheln else None; kacheln = []; s = a.schritt
    for j in range(7):
        for i in range(8):
            kid = f"{SPALTEN[i]}{j + 1}"
            if wahl and kid not in wahl: continue
            x0, x1, z0, z1 = xs[i], xs[i + 1], zs[j], zs[j + 1]
            ii = np.arange(x0 * rs, x1 * rs + 1, s); jj = np.arange(z0 * rs, z1 * rs + 1, s)
            if ii[-1] != x1 * rs: ii = np.append(ii, x1 * rs)
            if jj[-1] != z1 * rs: jj = np.append(jj, z1 * rs)
            J, I = np.meshgrid(jj, ii, indexing="ij"); w, h = len(ii), len(jj)
            a_ = (np.arange(h - 1)[:, None] * w + np.arange(w - 1)[None, :]).ravel(); b_ = a_ + 1; c_ = a_ + w; d_ = c_ + 1
            tri = np.stack([a_, c_, b_, b_, c_, d_], -1).reshape(-1, 3)                          # Wicklung: Normale nach +y
            Jf, If = J.ravel(), I.ravel()
            cj = np.rint(Jf[tri].mean(1)).astype(int); ci = np.rint(If[tri].mean(1)).astype(int)
            rang = np.maximum(R[Jf[tri], If[tri]].max(1), R[cj, ci])
            kl = VON_RANG[rang].astype(np.uint8)                                                    # Dreiecksklasse
            key = tri.astype(np.int64) * 6 + kl[:, None]                                            # Vertex je (Gitterpunkt, Klasse)
            uk, inv = np.unique(key.ravel(), return_inverse=True)
            g = uk // 6; fl = (uk % 6).astype(np.uint8); idx = inv.reshape(-1).astype(np.uint32)
            pos = np.stack([If[g] / rs, G[Jf[g], If[g]], Jf[g] / rs], -1).astype(np.float32)
            nor = N[Jf[g], If[g]].astype(np.float32)
            uv0 = pos[:, [0, 2]].copy(); uv1 = np.stack([pos[:, 0] / NX, pos[:, 2] / NZ], -1).astype(np.float32)
            data = glb(f"gelaende_{kid}", pos, nor, uv0, uv1, fl, idx, {"kachel": kid, "dummy": True})
            (out / "kacheln" / f"{kid}.glb").write_bytes(data)
            kacheln.append({"id": kid, "glb": f"kacheln/{kid}.glb", "bbox": [x0, z0, x1, z1], "dreiecke": int(len(kl)), "klassen_anteil": anteile(kl)})
    modelle = []
    if not wahl or "E2" in wahl:
        data, nt = bruecke(); (out / "modelle" / "bruecke_E2.glb").write_bytes(data)
        modelle.append({"id": "bruecke_E2", "glb": "modelle/bruecke_E2.glb", "klasse": 5})
    man = {"version": 1, "einheit": "m", "ursprung": "weltecke", "karte": {"breite": NX, "tiefe": NZ},
           "klassen": {str(k): v for k, v in KLASSEN.items()}, "attribute": {"flaeche": "_FLAECHE"},
           "uv": {"TEXCOORD_0": "welt_xz_m", "TEXCOORD_1": "karte_norm", "TEXCOORD_2": "wegband"},
           "kacheln": kacheln, "modelle": modelle,
           "quelle": f"DUMMY aus relief_daten.json.gz (GB/WV/WEGA), Schritt {s / rs:g} m - kein echtes Mesh, ohne TEXCOORD_2"}
    (out / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print(json.dumps({"kacheln": len(kacheln), "dreiecke_gesamt": sum(k["dreiecke"] for k in kacheln), "max_je_kachel": max(k["dreiecke"] for k in kacheln),
                      "modelle": len(modelle), "bytes": sum(f.stat().st_size for f in out.rglob("*.glb"))}))


if __name__ == "__main__":
    main()

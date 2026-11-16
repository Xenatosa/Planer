#!/usr/bin/env python3
"""P2b (Wege & Deko, 16.11.2026): zwei sichtbare L3-Reststellen, abschaltbarer Nachschritt auf GB (nach relief_l3.py).
  python3 relief_p2b.py [--trocken]   anwenden (nur wenn GB = Stand nach L3, Hash in pruefung/p2_analyse/p2b/p2b_stellen.json)
  python3 relief_p2b.py --aus         rueckgaengig (pruefung/p2_analyse/p2b/p2b_rueck.npz)
Stelle 03 D1 (rampe_2): Rampenboeschung neu = Rampenkern (Abstand <= KERN Zellen, Wegoberflaeche) bleibt bytegleich,
  daneben eine einfache Boeschung: h = Kernprofil(s) + (Gelaende_glatt - Kernprofil(s)) * smoothstep((d-KERN)/B),
  Gelaende_glatt = harmonische Fuellung (Laplace, keine inneren Extrema -> keine Dellen) des Korridors aus dem Rand.
Stelle 23 G6: Rippen am Wandfuss; L3 schuetzte dort den Weg G017, aber vektor.json ist in METERN (P10c), relief_l3.schutz
  liest es als Zellen -> G017 lag fuer L3 bei 272|230 statt richtig 227|192 (F5). Ohne diesen Scheinschutz: Ersatz wie
  L3 (Schliessung + Gauss) mit korrektem Schutz.
Fest (Gewicht 0): WEGA/Wegzellen/Bruecken, Wasser, andere Rampenkerne, vektor-Wege und Kreuzungen (in Zellen = m/1,2), D2 (+3).
Einheiten: alle Laengen in Zellen (GB-Raster 0,5 Zelle), wie gen_relief/rampenwege.
"""
import base64, gzip, hashlib, json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage as nd
from matplotlib.path import Path as MP
R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import relief_l3 as L3
CFG = R / "pruefung" / "p2_analyse" / "p2b" / "p2b_stellen.json"
RUECK = R / "pruefung" / "p2_analyse" / "p2b" / "p2b_rueck.npz"
CELL_M = 1.2

def _poly_dist(P, GY, GX, rs, sl):
    """Abstand (Zellen) und Station s (Zellen) jedes GB-Vertex im Ausschnitt sl zur Polylinie P (Zellen)."""
    zz, xx = np.mgrid[sl[0], sl[1]] / float(rs)
    best = np.full(zz.shape, 1e9); st = np.zeros(zz.shape); L0 = 0.0
    for a, b in zip(P[:-1], P[1:]):
        ab = b - a; l2 = float(ab @ ab) or 1e-9
        t = np.clip(((xx - a[0]) * ab[0] + (zz - a[1]) * ab[1]) / l2, 0, 1)
        d = np.hypot(xx - (a[0] + t * ab[0]), zz - (a[1] + t * ab[1]))
        m = d < best; best[m] = d[m]; st[m] = L0 + t[m] * np.sqrt(l2); L0 += np.sqrt(l2)
    return best, st, L0

def fest_maske(D, GY, GX, rs, ohne_rampe=None, kern_andere=2.0, frei=None, ohne_vektor=False):
    WV = np.frombuffer(base64.b64decode(D["WV"]), np.float32).reshape(GY, GX); F = WV > -900
    WEGA = np.frombuffer(base64.b64decode(D["WEGA"]), np.uint8).reshape(GY, GX); F |= WEGA > 0
    for x, z in D["wege"]: F[z * rs:z * rs + rs + 1, x * rs:x * rs + rs + 1] = True
    for b in D.get("bruecken", []): F[int(round(b[2] * rs)), int(round(b[0] * rs))] = True
    lin = np.zeros((GY, GX), bool)
    for i, p in enumerate(D.get("rampenwege", [])):
        if i == ohne_rampe or i in (frei or ()): continue
        P = np.asarray(p, float); L = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]; t = np.arange(0, L[-1] + 1e-9, 0.25)
        lin[np.clip(np.rint(np.interp(t, L, P[:, 1]) * rs).astype(int), 0, GY - 1), np.clip(np.rint(np.interp(t, L, P[:, 0]) * rs).astype(int), 0, GX - 1)] = True
    F |= nd.distance_transform_edt(~lin, sampling=1.0 / rs) <= kern_andere   # andere Rampen: nur Kern (Wegoberflaeche) fest
    V = json.loads((R / "neu" / "vektor.json").read_text(encoding="utf-8"))
    lin = np.zeros((GY, GX), bool); halb = np.zeros((GY, GX))
    for wv in ([] if ohne_vektor else V.get("wege", [])):
        P = np.asarray(wv["mittellinie_m"], float) / CELL_M
        if len(P) < 2: continue
        L = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]; t = np.arange(0, L[-1] + 1e-9, 0.25)
        zi = np.clip(np.rint(np.interp(t, L, P[:, 1]) * rs).astype(int), 0, GY - 1); xi = np.clip(np.rint(np.interp(t, L, P[:, 0]) * rs).astype(int), 0, GX - 1)
        lin[zi, xi] = True; halb[zi, xi] = np.maximum(halb[zi, xi], wv["breite_m"] / 2 / CELL_M + 0.5)
    d, (iz, ix) = nd.distance_transform_edt(~lin, sampling=1.0 / rs, return_indices=True); F |= d <= halb[iz, ix]
    zz, xx = np.mgrid[0:GY, 0:GX] / float(rs); pts = np.c_[xx.ravel(), zz.ravel()]
    for k in V.get("kreuzungen", []):
        poly = np.asarray(k["polygon_m"], float) / CELL_M; r_ = (float(k.get("uebergang_m", 0.0)) + 0.5) / CELL_M
        F |= MP(poly).contains_points(pts, radius=r_).reshape(GY, GX) | MP(poly).contains_points(pts, radius=-r_).reshape(GY, GX)
    x0, z0, x1, z1 = L3.D2_BOX; d2 = np.zeros((GY, GX), bool); d2[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1] = True
    return F, d2

def gewicht_fest(F, d2, rs):
    w = L3._ss(nd.distance_transform_edt(~F, sampling=1.0 / rs) / 1.0)
    w *= L3._ss((nd.distance_transform_edt(~d2, sampling=1.0 / rs) - 0.5) / 3.0); w[F | d2] = 0; return w

def harmonisch(H, frei, it=3000):
    T = H.copy()
    for _ in range(it):
        A = 0.25 * (np.roll(T, 1, 0) + np.roll(T, -1, 0) + np.roll(T, 1, 1) + np.roll(T, -1, 1)); T[frei] = A[frei]
    return T

def rampe_boeschung(H, D, s, rs, GY, GX):
    P = np.asarray(D["rampenwege"][s["rampe"]], float)
    zs = (P[:, 1].min() - 12) * rs; ze = (P[:, 1].max() + 12) * rs; xs = (P[:, 0].min() - 12) * rs; xe = (P[:, 0].max() + 12) * rs
    sl = (slice(max(int(zs), 1), min(int(ze), GY - 1)), slice(max(int(xs), 1), min(int(xe), GX - 1)))
    d, st, Lg = _poly_dist(P, GY, GX, rs, sl)
    K, B = s["kern"], s["boeschung"]; s0, s1 = s.get("von_s", 0) , Lg - s.get("bis_ende", 0)
    inS = (st >= s0) & (st <= s1)
    korr = (d <= s.get("flach", K) + B + 0.5) & inS
    E = H[sl].astype(float).copy()
    # Kernprofil(s): Median der Kernvertices je 0,5-Zellen-Station, entlang s geglaettet
    kern = d <= K; bins = np.round(st / 0.5).astype(int); prof = {}
    for b in np.unique(bins[kern]): prof[b] = float(np.median(E[kern & (bins == b)]))
    bb = np.array(sorted(prof)); pv = nd.gaussian_filter1d(np.array([prof[b] for b in bb]), 2, mode="nearest")
    Pk = np.interp(st / 0.5, bb, pv)
    kfix = np.zeros_like(kern)
    if s.get("kern_ausreisser_m"):   # nur Ausreisser im Kern (Reste des anderen Rampenkerns aus dem Zellraster) auf das Kernprofil
        kfix = kern & inS & (np.abs(E - Pk) > s["kern_ausreisser_m"]); E[kfix] = Pk[kfix]
    frei = korr & ~kern; frei[[0, -1], :] = False; frei[:, [0, -1]] = False
    T = harmonisch(E, frei)
    t = L3._ss((d - K) / B)
    fl = s.get("flach", K)   # K<d<=flach: Querschnitt auf Kernprofil (Wegoberflaeche verlaengert, R3 misst +-1,5), danach Boeschung
    t = L3._ss((d - fl) / B)
    neu = np.where(frei, Pk + (T - Pk) * t, E)
    # weicher Auslauf an den Stationsenden (2 Zellen)
    we = L3._ss((st - s0 + 2) / 2) * L3._ss((s1 + 2 - st) / 2)
    w = np.zeros_like(E); w[frei | kfix] = 1; w = np.maximum(w, 0) * np.where(inS, 1, we)
    E0 = H[sl].astype(float); out = H.astype(float).copy(); out[sl] = E0 + w * (neu - E0)
    wg = np.zeros((GY, GX)); wg[sl] = w
    return out, wg

def feinband(D, GBn, W, rs):
    """FW.h (Feinband, Maske/vid eingefroren) im P2b-Gewicht W auf die neue Boeschung (bilinear aus GB) ziehen.
    Ohne das zeigt das Feinband weiter die alte Treppe (L3-Rest 03). Kern (W=0), Wege, D2 bleiben unveraendert."""
    FW = D["FW"]; FS = int(FW["fs"]); FX = D["nx"] * FS + 1
    vid = np.frombuffer(base64.b64decode(FW["vid"]), np.uint32).astype(np.int64)
    h = np.frombuffer(base64.b64decode(FW["h"]), np.float32).astype(float)
    fz = (vid // FX) / FS * rs; fx = (vid % FX) / FS * rs
    wv = nd.map_coordinates(W, [fz, fx], order=1, mode="nearest", prefilter=False)
    g = nd.map_coordinates(GBn.astype(float), [fz, fx], order=1, mode="nearest", prefilter=False)
    hn = (h + wv * (g - h)).astype(np.float32); ge = hn != h.astype(np.float32)
    FW["h"] = base64.b64encode(hn.tobytes()).decode()
    return np.flatnonzero(ge), h.astype(np.float32)[ge], float(np.abs(hn - h)[ge].max()) if ge.any() else 0.0

def main():
    arg = sys.argv[1:]; cfg = json.loads(CFG.read_text(encoding="utf-8"))
    D = json.load(gzip.open(L3.QUELLE)); N = json.load(gzip.open(L3.NEU))
    nx, ny, rs = D["nx"], D["ny"], D["rs"]; GY, GX = ny * rs + 1, nx * rs + 1
    GB = np.frombuffer(base64.b64decode(D["GB"]), np.float32).reshape(GY, GX).copy()
    x0, z0, x1, z1 = L3.D2_BOX; d2s = L3._sha(GB[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1])
    if "--aus" in arg:
        r = np.load(RUECK); GBf = GB.reshape(-1).copy(); GBf[r["idx"]] = r["alt"]; GBn = GBf.reshape(GY, GX)
        delta = GBn.astype(float) - GB; D["GB"] = N["GB"] = base64.b64encode(GBn.tobytes()).decode()
        for X in (D, N):
            h = np.frombuffer(base64.b64decode(X["FW"]["h"]), np.float32).copy(); h[r["fw_idx"]] = r["fw_alt"]; X["FW"]["h"] = base64.b64encode(h.tobytes()).decode()
        L3.objekte(D, delta, rs); L3.objekte(N, delta, rs); L3.prototypen(N, GBn, GBn != GB)
        L3._schreibe(D, L3.QUELLE, False); L3._schreibe(N, L3.NEU, True); RUECK.unlink(); print("p2b aus"); return
    if L3._sha(GB) != cfg["basis_gb_sha256"]: sys.exit("GB entspricht nicht der P2b-Basis")
    H = GB.astype(float); ber = []; W = np.zeros((GY, GX))
    for s in cfg["stellen"]:
        if not s.get("aktiv", True): continue
        F, d2 = fest_maske(D, GY, GX, rs, ohne_rampe=s.get("rampe"), frei=s.get("frei_rampen"), ohne_vektor=s.get("ohne_vektor", False), kern_andere=s.get("kern_andere_m", 2.0))
        wf = gewicht_fest(F, d2, rs)
        if s["verfahren"] == "rampe_boeschung":
            E, wr = rampe_boeschung(H, D, s, rs, GY, GX); w = wf * L3.gewicht(s, GY, GX, rs) if "rx_m" in s else wf
            W = np.maximum(W, w * wr)
        else:
            w = L3.gewicht(s, GY, GX, rs) * wf; E = L3.ersatz(H, s, rs); W = np.maximum(W, w)
        alt = H.copy(); H = alt + w * (E - alt); dd = H - alt
        ber.append({"id": s["id"], "max_m": round(float(np.abs(dd).max()), 3), "vertices": int((np.abs(dd) > 1e-4).sum())})
    GBn = H.astype(np.float32); delta = GBn.astype(float) - GB.astype(float); ge = GBn != GB
    d2n = L3._sha(GBn[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1])
    info = {"stellen": ber, "vertices_geaendert": int(ge.sum()), "d2_vorher": d2s, "d2_nachher": d2n}
    if d2n != d2s: sys.exit("D2 geaendert - Abbruch")
    if "--trocken" in arg: print(json.dumps(info, indent=1)); np.save("/tmp/p2b_trocken_delta.npy", delta); return
    D["GB"] = N["GB"] = base64.b64encode(GBn.tobytes()).decode()
    fi, fa, fmax = feinband(D, GBn, W, rs); fi2, _, _ = feinband(N, GBn, W, rs)
    if not np.array_equal(fi, fi2): sys.exit("Feinband D/N ungleich")
    info["feinband"] = {"punkte": int(len(fi)), "max_m": round(fmax, 3)}
    idx = np.flatnonzero(ge.reshape(-1)); np.savez_compressed(RUECK, idx=idx, alt=GB.reshape(-1)[idx], fw_idx=fi, fw_alt=fa)
    info["objekte"] = L3.objekte(D, delta, rs); L3.objekte(N, delta, rs); info["prototypen"] = L3.prototypen(N, GBn, ge)
    L3._schreibe(D, L3.QUELLE, False); L3._schreibe(N, L3.NEU, True)
    (CFG.parent / "p2b_bericht.json").write_text(json.dumps(info, indent=1), encoding="utf-8"); print(json.dumps(info, indent=1))

if __name__ == "__main__":
    main()

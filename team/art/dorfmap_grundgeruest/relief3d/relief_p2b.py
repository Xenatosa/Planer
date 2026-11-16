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

def _profil(E, maske, st, schritt=0.5, sigma=2):
    bins = np.round(st / schritt).astype(int); prof = {}
    for b in np.unique(bins[maske]): prof[b] = float(np.median(E[maske & (bins == b)]))
    bb = np.array(sorted(prof)); pv = nd.gaussian_filter1d(np.array([prof[b] for b in bb]), sigma, mode="nearest")
    return lambda x: np.interp(x / schritt, bb, pv)

def _misch_profil(P, GY, GX, rs, sl, sg, prof, b=0.7):
    """Profilwert je Vertex als gewichtetes Mittel ueber alle Segmente (Gewicht exp(-((d_i-d_min)/b)^2)):
    stetig auch auf der Winkelhalbierenden einer Kehre, wo die naechste Projektion zwischen zwei Schenkeln springt."""
    zz, xx = np.mgrid[sl[0], sl[1]] / float(rs); ds, vs = [], []; L0 = 0.0
    for a, c in zip(P[:-1], P[1:]):
        ab = c - a; l2 = float(ab @ ab) or 1e-9
        t = np.clip(((xx - a[0]) * ab[0] + (zz - a[1]) * ab[1]) / l2, 0, 1)
        ds.append(np.hypot(xx - (a[0] + t * ab[0]), zz - (a[1] + t * ab[1]))); vs.append(np.interp(L0 + t * np.sqrt(l2), sg, prof)); L0 += np.sqrt(l2)
    ds = np.array(ds); vs = np.array(vs); g = np.exp(-(((ds - ds.min(0)) / b) ** 2)); return (g * vs).sum(0) / g.sum(0)

def rampe_anheben(H, D, s, rs, GY, GX):
    """P2c Variante A: Rampe s['rampe'] (X084) an der Kreuzung mit s['kreuzt'] (rampe_2) auf deren Hoehe anheben.
    Kreuzungsflaeche (beide Kerne) = glattes Profil von rampe_2 (stufenfrei), X084-Kern = altes Profil + Delta * Kosinus-Fenster
    (Plateau +-w0, Auslauf Lt Zellen beidseitig, sanftes Laengsgefaelle zurueck auf die alte Hoehe), Boeschung harmonisch neu."""
    P8 = np.asarray(D["rampenwege"][s["rampe"]], float); P2 = np.asarray(D["rampenwege"][s["kreuzt"]], float)
    zs = (P8[:, 1].min() - 12) * rs; ze = (P8[:, 1].max() + 12) * rs; xs = (P8[:, 0].min() - 12) * rs; xe = (P8[:, 0].max() + 12) * rs
    sl = (slice(max(int(zs), 1), min(int(ze), GY - 1)), slice(max(int(xs), 1), min(int(xe), GX - 1)))
    d8, st8, L8 = _poly_dist(P8, GY, GX, rs, sl); d2, st2, L2 = _poly_dist(P2, GY, GX, rs, sl)
    E = H[sl].astype(float).copy(); K, fl, B = s["kern"], s["flach"], s["boeschung"]; K2 = s.get("kern_kreuzt", 2.0)
    pk8 = _profil(E, (d8 <= K) & (d2 > K2 + 0.5), st8)
    # Kreuzungsstation: Polylinien-Punkt von P8 mit kleinstem Abstand zu P2
    L8v = np.r_[0, np.cumsum(np.hypot(*np.diff(P8, axis=0).T))]; L2v = np.r_[0, np.cumsum(np.hypot(*np.diff(P2, axis=0).T))]
    dd = np.hypot(P8[:, None, 0] - P2[None, :, 0], P8[:, None, 1] - P2[None, :, 1]); i8, i2 = np.unravel_index(dd.argmin(), dd.shape)
    sc, s2c = L8v[i8], L2v[i2]
    # rampe_2-Profil an der Kreuzung: quadratischer Fit ueber den ungestoerten rampe_2-Kern +-W Zellen (die alte X084-Rinne quert ihn)
    m2 = (d2 <= 1.0) & (d8 > fl + 0.5) & (np.abs(st2 - s2c) <= s.get("fit_kreuzt", 8.0)); c2 = np.polyfit(st2[m2], E[m2], 2)
    pk2 = lambda x: np.polyval(c2, x)
    s["_fit"] = {"koeff": c2.round(5).tolist(), "rest_max_m": round(float(np.abs(E[m2] - pk2(st2[m2])).max()), 3)}
    delta = float(pk2(np.array(s2c)) - pk8(np.array(sc)))
    w0 = s["plateau"]; H2 = float(pk2(np.array(s2c))); se = L8v[-1]
    # P2c v2: rampe_2 bleibt unveraendert (Kreuzungsflaeche = vorhandene rampe_2-Oberflaeche).
    # Mittellinie X084: Abschnitt [sa, sb] im rampe_2-Band (d2 <= K2) folgt rampe_2 (pk2 an der Projektion),
    # bergseitig weiches Maximum aus altem Profil und Eintrittshoehe, talseitig lineares Offset zurueck auf das alte Endprofil.
    sg = np.arange(0, se + 0.25, 0.25); p8 = pk8(sg)
    cx = np.interp(sg, L8v, P8[:, 0]); cz = np.interp(sg, L8v, P8[:, 1])
    cd = np.full(sg.shape, 1e9); cs = np.zeros(sg.shape); L0 = 0.0
    for a_, b_ in zip(P2[:-1], P2[1:]):
        ab = b_ - a_; l2 = float(ab @ ab) or 1e-9; tt = np.clip(((cx - a_[0]) * ab[0] + (cz - a_[1]) * ab[1]) / l2, 0, 1)
        dd_ = np.hypot(cx - (a_[0] + tt * ab[0]), cz - (a_[1] + tt * ab[1])); m = dd_ < cd; cd[m] = dd_[m]; cs[m] = L0 + tt[m] * np.sqrt(l2); L0 += np.sqrt(l2)
    ink = cd <= K2; sa, sb = float(sg[ink].min()), float(sg[ink].max()); h2l = pk2(cs)
    ha, hb = float(pk2(np.array(cs[ink][0]))), float(pk2(np.array(cs[ink][-1])))
    k = s.get("weich_m", 0.4); hi = 0.5 * (p8 + ha + np.sqrt((p8 - ha) ** 2 + k * k))
    a = np.clip((sg - sb) / max(se - sb, 1e-6), 0, 1); pbb = float(pk8(np.array(sb)))
    prof = np.where(sg < sa, hi, np.where(sg <= sb, h2l, p8[-1] + (hb - p8[-1]) * (1 - a) ** s.get("tal_exponent", 1.5)))   # talseitig: zum Ende hin flacher (Exponent 1,5), altes Profil hatte dort die 0,8-m-Stufe
    prof = nd.gaussian_filter1d(prof, s.get("glatt_s", 1.0) / 0.25, mode="nearest"); prof[-1] = p8[-1]; T8 = _misch_profil(P8, GY, GX, rs, sl, sg, prof, s.get("kehre_mix", 0.7))
    s["_profil"] = {"s": sg[::4].round(2).tolist(), "h": prof[::4].round(3).tolist(), "alt": p8[::4].round(3).tolist(), "sa": round(sa, 2), "sb": round(sb, 2)}
    Lt = s.get("auslauf_berg", 10.0)
    flat8 = d8 <= fl; flat2 = d2 <= K2
    # neben dem rampe_2-Band weich auf die rampe_2-Hoehe an der Projektion ueberblenden (stufenfrei)
    b2 = L3._ss((d2 - K2) / s.get("ueberblend_kreuzt", 1.0)); Z8 = pk2(st2) + (T8 - pk2(st2)) * b2
    ziel = E.copy(); ziel[flat8 & ~flat2] = Z8[flat8 & ~flat2]
    k2z = flat2 & (d8 <= fl + B); wk = 1 - L3._ss((d8 - fl) / B)   # rampe_2-Band an der Kreuzung: alte Rinne schliessen, weich auf den Bestand
    ziel[k2z] = (E + (pk2(st2) - E) * wk)[k2z]
    s0 = sa - Lt - 1; s1 = se
    inS = (st8 >= s0) & (st8 <= s1)
    frei = (d8 <= fl + B + 0.5) & ~flat8 & ~flat2 & inS; frei[[0, -1], :] = False; frei[:, [0, -1]] = False
    # Boeschung: wegnah reine harmonische Fuellung (alte Rinnenwaende weg, keine Mulden), zum Korridorrand hin
    # Bestand + harmonisch fortgesetzte Anhebung (Gelaendeform bleibt); beide stimmen an Kern und Rand ueberein -> stetig
    Hh = harmonisch(ziel, frei); Vh = E + harmonisch(np.where(frei, 0.0, ziel - E), frei)
    neu = Hh + (Vh - Hh) * L3._ss((d8 - fl) / B)
    we = L3._ss((st8 - s0 + 2) / 2) * L3._ss((s1 + 2 - st8) / 2)
    w = np.zeros_like(E); w[(flat8 & ~flat2) | frei | k2z] = 1; w *= np.where(inS, 1, we)
    out = H.astype(float).copy(); out[sl] = E + w * (neu - E)
    wg = np.zeros((GY, GX)); wg[sl] = w
    s["_info"] = {"station_kreuzung": round(float(sc), 2), "delta_m": round(delta, 3), "hoehe_kreuzung": round(H2, 3), "rampe2_band_s": [round(sa, 2), round(sb, 2)], "hoehe_ein_aus": [round(ha, 3), round(hb, 3)], "fit_kreuzt": s.pop("_fit")}
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
        if s["verfahren"] == "rampe_anheben":
            E, wr = rampe_anheben(H, D, s, rs, GY, GX); w = wf * wr; W = np.maximum(W, w)
        elif s["verfahren"] == "rampe_boeschung":
            E, wr = rampe_boeschung(H, D, s, rs, GY, GX); w = wf * L3.gewicht(s, GY, GX, rs) if "rx_m" in s else wf
            W = np.maximum(W, w * wr)
        else:
            w = L3.gewicht(s, GY, GX, rs) * wf; E = L3.ersatz(H, s, rs); W = np.maximum(W, w)
        alt = H.copy(); H = alt + w * (E - alt); dd = H - alt
        ber.append({"id": s["id"], "max_m": round(float(np.abs(dd).max()), 3), "vertices": int((np.abs(dd) > 1e-4).sum()), **s.pop("_info", {}), **({"profil": s.pop("_profil")} if "_profil" in s else {})})
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

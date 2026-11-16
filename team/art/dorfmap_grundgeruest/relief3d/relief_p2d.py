#!/usr/bin/env python3
"""P2d (Wege & Deko, 16.11.2026, QA P4d PR #30): Nachschritt nach L3c2 auf relief_daten.json.gz + neu/relief_neu.json.gz.
  python3 relief_p2d.py            anwenden (nur auf Basis-GB-Hash b3698e0 = Stand nach L3d, siehe BASIS_GB)
  python3 relief_p2d.py --aus      rueckgaengig (pruefung/p2_analyse/p2d/p2d_rueck.npz)
S7 rampe_5 D4/D5 "milchiges Band": Ursache [S] = Runde O16 (runde_o16.entfernen, alte rampe_9 + Ruecken 133|173):
  GB und VC wurden dort harmonisch gefuellt -> Farbdetail 1,6 statt 3,8 (Fleck-Energie), Gelaendedetail 0,023 statt 0,048 m.
  Ton (L 208 vs 210), WEGA (0), WV (Land), Payload/Bruecken: unauffaellig. Abhilfe: Farbe UND Mikrorelief aus einem normal
  texturierten Spenderstreifen (Versatz 26 Zellen West, Ersatz 18 West / 14 Ost) per Poisson-Einpassung (Rand stetig),
  Relief nur Hochpass-Anteil, max +-0,08 m, nicht naeher als 4 Zellen an rampe_5 / 2 Zellen an Wegen, Wasser +6, nur Steigung < 0,12.
S10 Bruecken E2/E3 Ostufer: Hakenzellen (E2 197,5|72,5 und |73,5; E3 186,5|126,5 und 185,5|129,5) raus, Deckhoehe E3
  einheitlich 0,3; Land-Anschluss: Gelaende hinter dem Ostende in 5 Zellen auf Decklage (0,33) angerampt (nur Land,
  >= 2 Zellen vom Wasser, keine Wasser-/Uferzellen, WV unveraendert).
D2 bleibt bitgleich (Box nicht beruehrt, Pruefung im Skript)."""
import base64, gzip, hashlib, json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage as nd
R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import relief_l3 as L3
from relief_p2b import feinband, harmonisch
AUSD = R / "pruefung" / "p2_analyse" / "p2d"; RUECK = AUSD / "p2d_rueck.npz"
BASIS_GB = "bd5e8ca239235ee3ccd04903db4f963f6ce7d68f2635ea7e2cfb6a5f73c10002"
SPENDER = ((-26, 0), (-18, 0), (14, 0))       # (dx, dz) in Zellen
RELIEF_MAX = 0.08
HAKEN = [(197.5, 72.5), (197.5, 73.5), (186.5, 126.5), (185.5, 129.5)]
DECK_E3 = (174, 187, 127, 129)                # x0,x1,z0,z1 (Zellen) -> y 0,3
RAMPEN = [  # Ostende (x Zellen), z-Bereich Deck, Laenge
    {"id": "E2", "x0": 198.0, "z0": 74.0, "z1": 76.0, "lang": 5.0},
    {"id": "E3", "x0": 187.0, "z0": 127.0, "z1": 129.0, "lang": 5.0}]
DECK_OBEN = 0.33

def maske_r5(D, G, V, WV, A, GY, GX):
    L = V.mean(-1); ev = nd.uniform_filter(np.abs(L - nd.gaussian_filter(L, 2)), 9)
    box = np.zeros((GY, GX), bool); box[150 * 2:199 * 2, 124 * 2:142 * 2] = True
    nass = nd.binary_dilation(WV > -900, iterations=6); weg = nd.binary_dilation(A > 0, iterations=4)
    m = (ev < 2.6) & box & ~nass & ~weg; m = nd.binary_opening(m, iterations=2)
    lab, n = nd.label(m); gr = nd.sum(m, lab, range(1, n + 1)); m = np.isin(lab, 1 + np.flatnonzero(gr >= 300))
    m = nd.binary_closing(m, iterations=4) & ~nass & ~weg
    return m, ev, nass, weg

def spender(F, ok, m, axis_last=False):
    """gewichtetes Spenderfeld: je Versatz Gueltigkeit weich (Gauss 2), Vorrang nach Reihenfolge"""
    acc = 0; wsum = 0; rest = np.ones(m.shape)
    for dx, dz in SPENDER:
        sh = lambda a: np.roll(np.roll(a, -dz * 2, 0), -dx * 2, 1)
        g = nd.gaussian_filter(sh(ok).astype(float), 2) * rest; Fd = sh(F)
        acc = acc + (g[..., None] * Fd if Fd.ndim == 3 else g * Fd); wsum = wsum + g; rest = rest * (1 - np.clip(g, 0, 1))
    wsum = np.maximum(wsum, 1e-6)
    return acc / (wsum[..., None] if F.ndim == 3 else wsum), wsum

def poisson(C, S, m):
    """C im Bereich m durch S + harmonische Fortsetzung von (C - S) vom Rand ersetzen"""
    frei = m.copy(); frei[[0, -1], :] = False; frei[:, [0, -1]] = False
    d = np.where(frei, 0.0, C - S); return S + harmonisch(d, frei, it=2500)

def main():
    arg = sys.argv[1:]
    D = json.load(gzip.open(L3.QUELLE)); N = json.load(gzip.open(L3.NEU)); rs = D["rs"]; GY, GX = D["ny"] * rs + 1, D["nx"] * rs + 1
    GB = np.frombuffer(base64.b64decode(D["GB"]), np.float32).reshape(GY, GX).copy()
    x0, z0, x1, z1 = L3.D2_BOX; d2s = L3._sha(GB[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1])
    if "--aus" in arg:
        r = np.load(RUECK, allow_pickle=True); GBf = GB.reshape(-1).copy(); GBf[r["idx"]] = r["alt"]; GBn = GBf.reshape(GY, GX)
        delta = GBn.astype(float) - GB
        for X in (D, N):
            X["GB"] = base64.b64encode(GBn.tobytes()).decode()
            h = np.frombuffer(base64.b64decode(X["FW"]["h"]), np.float32).copy(); h[r["fw_idx"]] = r["fw_alt"]; X["FW"]["h"] = base64.b64encode(h.tobytes()).decode()
            vc = np.frombuffer(base64.b64decode(X["VC"]), np.uint8).reshape(-1, 3).copy(); vc[r["vc_idx"]] = r["vc_alt"]; X["VC"] = base64.b64encode(vc.tobytes()).decode()
            X["bruecken"] = json.loads(str(r["bruecken_alt"]))
        L3.objekte(D, delta, rs); L3.objekte(N, delta, rs); L3.prototypen(N, GBn, GBn != GB)
        L3._schreibe(D, L3.QUELLE, False); L3._schreibe(N, L3.NEU, True); RUECK.unlink(); print("p2d aus"); return
    if L3._sha(GB) != BASIS_GB: sys.exit("GB entspricht nicht der P2d-Basis (b3698e0, Stand nach L3d)")
    G = GB.astype(float); V = np.frombuffer(base64.b64decode(D["VC"]), np.uint8).reshape(GY, GX, 3).astype(float)
    WV = np.frombuffer(base64.b64decode(D["WV"]), np.float32).reshape(GY, GX); A = np.frombuffer(base64.b64decode(D["WEGA"]), np.uint8).reshape(GY, GX)
    info = {}
    # --- S7 rampe_5 / O16-Band ---
    m, ev, nass, weg = maske_r5(D, G, V, WV, A, GY, GX)
    gy, gx = np.gradient(G, 1.0 / rs); ok = ~nass & ~weg & (np.hypot(gx, gy) < 0.5) & (ev >= 2.5) & ~m
    S, wsum = spender(V, ok, m); Vn = V.copy()
    for k in range(3): Vn[..., k] = poisson(V[..., k], S[..., k], m)
    kante = L3._ss(nd.distance_transform_edt(m) / 3.0); Vn = V + kante[..., None] * (Vn - V)
    Vn = np.clip(np.round(Vn), 0, 255).astype(np.uint8)
    # Mikrorelief: Hochpass des Spender-GB, nur fern von rampe_5 und Wegen
    P5 = np.asarray(D["rampenwege"][5], float); Lp = np.r_[0, np.cumsum(np.hypot(*np.diff(P5, axis=0).T))]; t = np.arange(0, Lp[-1], 0.25)
    lin = np.zeros((GY, GX), bool); lin[np.rint(np.interp(t, Lp, P5[:, 1]) * rs).astype(int), np.rint(np.interp(t, Lp, P5[:, 0]) * rs).astype(int)] = True
    d5 = nd.distance_transform_edt(~lin, sampling=1.0 / rs); dw = nd.distance_transform_edt(A == 0, sampling=1.0 / rs)
    HP = G - nd.gaussian_filter(G, 2); Hs, _ = spender(HP, ok, m)
    wr = L3._ss(nd.distance_transform_edt(m) / 6.0) * L3._ss((d5 - 4.0) / 2.0) * L3._ss((dw - 2.0) / 2.0)
    wr *= L3._ss((0.12 - nd.gaussian_filter(np.hypot(gx, gy), 1)) / 0.04)   # nur flaches Gelaende (G6 misst ab Steigung 0,15)
    dG = np.clip(Hs, -RELIEF_MAX, RELIEF_MAX) * wr; dG[~m] = 0
    Gn = G + dG
    Lm = Vn.astype(float).mean(-1); ev2 = nd.uniform_filter(np.abs(Lm - nd.gaussian_filter(Lm, 2)), 9)
    ring = nd.binary_dilation(m, iterations=8) & ~m & ~nass
    eg2 = nd.uniform_filter(np.abs(Gn - nd.gaussian_filter(Gn, 2)), 9); eg1 = nd.uniform_filter(np.abs(G - nd.gaussian_filter(G, 2)), 9)
    info["S7_rampe5"] = {"maske_knoten": int(m.sum()), "farbdetail_vorher": round(float(ev[m].mean()), 2), "farbdetail_nachher": round(float(ev2[m].mean()), 2),
                         "farbdetail_ring": round(float(ev[ring].mean()), 2), "relief_detail_vorher_m": round(float(eg1[m].mean()), 4),
                         "relief_detail_nachher_m": round(float(eg2[m].mean()), 4), "relief_detail_ring_m": round(float(eg1[ring].mean()), 4),
                         "ton_L_vorher": round(float(V.mean(-1)[m].mean()), 1), "ton_L_nachher": round(float(Lm[m].mean()), 1), "ton_L_ring": round(float(V.mean(-1)[ring].mean()), 1),
                         "relief_max_m": round(float(np.abs(dG).max()), 3), "spender_zellen": SPENDER}
    # --- S10 Bruecken ---
    br_alt = json.dumps(D["bruecken"]); haken = {(x, z) for x, z in HAKEN}
    nb = []
    for b in D["bruecken"]:
        if (b[0], b[2]) in haken: continue
        if DECK_E3[0] <= b[0] <= DECK_E3[1] and DECK_E3[2] <= b[2] <= DECK_E3[3]: b = [b[0], 0.3, b[2]]
        nb.append(b)
    info["S10_bruecken"] = {"vorher": len(D["bruecken"]), "nachher": len(nb), "entfernt": sorted(haken)}
    zz, xx = np.mgrid[0:GY, 0:GX] / float(rs); dn = nd.distance_transform_edt(WV <= -900, sampling=1.0 / rs)
    # Sperrbereich Art Umgebung: von L3d geaenderte Knoten (GB/WV/VC, pruefung/l3d/l3d_rueck.npz) + 2 Knoten Saum nicht anfassen
    sperr = np.zeros(GY * GX, bool); LR = np.load(R / "pruefung" / "l3d" / "l3d_rueck.npz")
    for k in ("gb_idx", "wv_idx", "vc_idx"): sperr[LR[k]] = True
    sperr = nd.binary_dilation(sperr.reshape(GY, GX), iterations=2)
    for r in RAMPEN:
        a = L3._ss(np.clip(1 - (xx - r["x0"]) / r["lang"], 0, 1)) * L3._ss((xx - (r["x0"] - 2.5)) / 1.5)
        q = L3._ss((zz - (r["z0"] - 2.5)) / 2.5) * L3._ss(((r["z1"] + 2.5) - zz) / 2.5)
        w = a * q * L3._ss((dn - 2.0) / 2.0); w[WV > -900] = 0; w[sperr] = 0
        ziel = np.maximum(Gn, DECK_OBEN - 0.03); Gn = Gn + w * (ziel - Gn)
        info["S10_bruecken"]["rampe_" + r["id"]] = {"max_m": round(float((w * (ziel - G)).max()), 3), "knoten": int((w > 1e-3).sum())}
    GBn = Gn.astype(np.float32); ge = GBn != GB; delta = GBn.astype(float) - GB.astype(float)
    d2n = L3._sha(GBn[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1])
    if d2n != d2s: sys.exit("D2 geaendert - Abbruch")
    if (WV[ge] > -900).any(): sys.exit("Wasserzelle geaendert - Abbruch")
    if (ge & sperr).any() or (vc_ge_v := (Vn != V.astype(np.uint8)).any(-1) & sperr).any(): sys.exit("L3d-Sperrbereich geaendert - Abbruch")
    vc_ge = (Vn != V.astype(np.uint8)).any(-1)
    if vc_ge[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1].any(): sys.exit("D2-VC geaendert - Abbruch")
    info.update({"gb_knoten": int(ge.sum()), "vc_knoten": int(vc_ge.sum()), "d2": d2n})
    W = np.zeros((GY, GX)); W[nd.binary_dilation(ge, iterations=1)] = 1
    vi = np.flatnonzero(vc_ge.reshape(-1)); vc_alt = V.astype(np.uint8).reshape(-1, 3)[vi]
    for X in (D, N):
        X["GB"] = base64.b64encode(GBn.tobytes()).decode(); X["VC"] = base64.b64encode(Vn.tobytes()).decode(); X["bruecken"] = [list(b) for b in nb]
    fi, fa, fmax = feinband(D, GBn, W, rs); fi2, _, _ = feinband(N, GBn, W, rs)
    if not np.array_equal(fi, fi2): sys.exit("Feinband D/N ungleich")
    # FW.c im VC-Bereich nachziehen (Feinbandfarbe = VC wie O16)
    for X in (D, N):
        FW = X["FW"]; FS = int(FW["fs"]); FX = X["nx"] * FS + 1; vid = np.frombuffer(base64.b64decode(FW["vid"]), np.uint32).astype(np.int64)
        gi = np.clip(np.rint((vid // FX) / FS * rs).astype(int), 0, GY - 1); gj = np.clip(np.rint((vid % FX) / FS * rs).astype(int), 0, GX - 1)
        c = np.frombuffer(base64.b64decode(FW["c"]), np.uint8).reshape(-1, 3).copy(); sel = vc_ge[gi, gj]; c[sel] = Vn[gi[sel], gj[sel]]
        FW["c"] = base64.b64encode(c.tobytes()).decode(); info["fw_c_punkte"] = int(sel.sum())
    info["feinband"] = {"punkte": int(len(fi)), "max_m": round(fmax, 3)}
    idx = np.flatnonzero(ge.reshape(-1))
    np.savez_compressed(RUECK, idx=idx, alt=GB.reshape(-1)[idx], fw_idx=fi, fw_alt=fa, vc_idx=vi, vc_alt=vc_alt, bruecken_alt=np.array(br_alt))
    info["objekte"] = L3.objekte(D, delta, rs); L3.objekte(N, delta, rs); info["prototypen"] = L3.prototypen(N, GBn, ge)
    L3._schreibe(D, L3.QUELLE, False); L3._schreibe(N, L3.NEU, True)
    (AUSD / "p2d_bericht.json").write_text(json.dumps(info, indent=1, default=str), encoding="utf-8"); print(json.dumps(info, indent=1, default=str))

if __name__ == "__main__":
    main()

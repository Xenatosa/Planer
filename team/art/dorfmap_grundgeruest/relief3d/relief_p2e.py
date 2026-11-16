#!/usr/bin/env python3
"""P2e (Wege & Deko, 16.11.2026, QA P4e PR #36): Nachschritt nach L3f/L3g (bau_endstand Schritt 16).
  python3 relief_p2e.py          anwenden (nur auf Basis-Hash GB+VC bfe8dce, siehe BASIS_*)
  python3 relief_p2e.py --aus    rueckgaengig (pruefung/p2_analyse/p2e/p2e_rueck.npz)
S7 rampe_5 D4 ~133|155 / D5 ~135|185 "Milchband/-fleck": Messung [S] auf bfe8dce: P2d-Flaeche (1842 Knoten) L 213,1 / Ring 208,2,
  L-Streuung 13,8 / 22,5, L10 195 / 176 -> heller und ohne dunkle Flecken (Poisson-Einpassung hat die Spenderfarbe geglaettet).
Abhilfe NUR VC: Farbe je Knoten 1:1 aus einem Spender-Versatz kopiert (kein Mitteln), Versatz je Knoten nach gleicher Hangneigung
  (geglaettete Wahl, zusammenhaengende Flecken), danach Mittel-RGB je Zone (Nord D4 / Sued D5) auf den Zonenring gezogen (Ziel |dL| <= 1, dS klein), Rand 6 Knoten weich, Versatzwechsel weich (exp-Gewicht TAU 0,4 Grad).
GB, WV, WEGA, Wege, Bruecken unveraendert (kein Mikrorelief). FW.c der Prototypen folgt VC wie in P2d. D2 und Sperrbereiche unberuehrt."""
import base64, gzip, hashlib, json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage as nd
R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import relief_l3 as L3
AUSD = R / "pruefung" / "p2_analyse" / "p2e"; RUECK = AUSD / "p2e_rueck.npz"
BASIS_GB = "fd798f6d6e3fe8f76527ca59303d42b06b1ce284fbe8007c91299781875b9c00"
BASIS_VC = "710ac7a30dd8b3df110b8920d5d7b8d181ac1f4184fbe1e7d45a549cf3f54ddb"
SPENDER = ((-26, 0), (-18, 0), (14, 0), (-34, 0), (22, 0), (0, -30), (0, 24))   # (dx, dz) Zellen
ZGRENZE = 170.0   # Zellen, Nord-/Suedzone
TAU = 0.4         # Grad Hangunterschied, weiche Spenderwahl
KANTE = 6.0       # Knoten weicher Rand
KANTE_T1 = 55.0   # Farbsprung-Grenze Spenderfeld (T1 zaehlt ab 70)
SPERR_BOXEN = [(168, 86, 210, 172), (0, 258, 336, 303)]   # E3/E4 (Baeche) und Zeile 7 (A7-H7), Zellen x0,z0,x1,z1

def kenn(V, M):
    v = V[M].astype(float); L = v.mean(1); S = (v.max(1) - v.min(1)) / np.maximum(v.max(1), 1)
    return {"n": int(M.sum()), "L": round(float(L.mean()), 2), "S": round(float(S.mean()), 4), "L_streuung": round(float(L.std()), 2),
            "L10": round(float(np.percentile(L, 10)), 1), "RGB": [round(float(v[:, k].mean()), 1) for k in range(3)]}

def lade_fw_c(X):
    return np.frombuffer(base64.b64decode(X["FW"]["c"]), np.uint8).reshape(-1, 3).copy()

def main():
    D = json.load(gzip.open(L3.QUELLE)); N = json.load(gzip.open(L3.NEU)); rs = D["rs"]; GX, GY = D["nx"] * rs + 1, D["ny"] * rs + 1
    if "--aus" in sys.argv:
        r = np.load(RUECK)
        for X, k in ((D, "fwd"), (N, "fwn")):
            vc = np.frombuffer(base64.b64decode(X["VC"]), np.uint8).reshape(-1, 3).copy(); vc[r["vc_idx"]] = r["vc_alt"]; X["VC"] = base64.b64encode(vc.tobytes()).decode()
            c = lade_fw_c(X); c[r[k + "_idx"]] = r[k + "_alt"]; X["FW"]["c"] = base64.b64encode(c.tobytes()).decode()
        L3._schreibe(D, L3.QUELLE, False); L3._schreibe(N, L3.NEU, True); RUECK.unlink(); print("p2e aus"); return
    if hashlib.sha256(base64.b64decode(D["GB"])).hexdigest() != BASIS_GB or hashlib.sha256(base64.b64decode(D["VC"])).hexdigest() != BASIS_VC:
        sys.exit("GB/VC entspricht nicht der P2e-Basis (bfe8dce)")
    if D["VC"] != N["VC"]: sys.exit("VC relief_daten/relief_neu ungleich")
    G = np.frombuffer(base64.b64decode(D["GB"]), np.float32).reshape(GY, GX).astype(float)
    V = np.frombuffer(base64.b64decode(D["VC"]), np.uint8).reshape(GY, GX, 3)
    WV = np.frombuffer(base64.b64decode(D["WV"]), np.float32).reshape(GY, GX); A = np.frombuffer(base64.b64decode(D["WEGA"]), np.uint8).reshape(GY, GX)
    # Flaeche = P2d-Farbflaeche S7 (p2d_rueck vc_idx)
    m = np.zeros(GY * GX, bool); m[np.load(R / "pruefung" / "p2_analyse" / "p2d" / "p2d_rueck.npz")["vc_idx"]] = True; m = m.reshape(GY, GX)
    box = np.zeros((GY, GX), bool); box[150 * rs:199 * rs, 124 * rs:142 * rs] = True; m &= box
    nass = nd.binary_dilation(WV > -900, iterations=6); weg = nd.binary_dilation(A > 0, iterations=4)
    sperr = np.zeros(GY * GX, bool)
    for st in ("l3d", "l3e", "l3f"):
        LR = np.load(R / "pruefung" / st / (st + "_rueck.npz"))
        for k in ("gb_idx", "wv_idx", "vc_idx"):
            if k in LR.files: sperr[LR[k]] = True
    sperr = nd.binary_dilation(sperr.reshape(GY, GX), iterations=2)
    for x0, z0, x1, z1 in SPERR_BOXEN + [L3.D2_BOX]: sperr[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1] = True
    m &= ~sperr & ~nass & ~weg
    ring = nd.binary_dilation(m, iterations=16) & ~nd.binary_dilation(m, iterations=2) & ~nass & ~weg & ~sperr
    gy, gx = np.gradient(G, 1.0 / rs); hang = np.degrees(np.arctan(np.hypot(gx, gy)))
    ok = ~nass & ~weg & ~nd.binary_dilation(m, iterations=2) & ~sperr
    # Spender je Knoten: Versatz mit kleinstem geglaetteten Hangunterschied (ungueltig = Strafe), Farbe 1:1 kopiert
    kosten = []; kopien = []
    for dx, dz in SPENDER:
        sh = lambda a: np.roll(np.roll(a, -dz * rs, 0), -dx * rs, 1)
        k = np.abs(sh(hang) - hang) + 1000.0 * ~sh(ok); kosten.append(nd.gaussian_filter(k, 4)); kopien.append(sh(V))
    K = np.stack(kosten); wahl = np.argmin(K, 0); gueltig = np.take_along_axis(K, wahl[None], 0)[0] < 300
    # weiche Uebergaenge zwischen Versaetzen (sonst Saegezahn-Naht): Gewichte exp(-(K-Kmin)/TAU), Wahl Gauss 1 geglaettet
    Wt = np.exp(-(K - K.min(0)) / TAU); Wt = np.stack([nd.gaussian_filter(w, 1) for w in Wt]); Wt /= Wt.sum(0)
    S = (Wt[..., None] * np.stack(kopien).astype(float)).sum(0)
    ziel = m & gueltig
    # harte Farbkanten im Spenderfeld entschaerfen (T1: |dRGB| > 70 zwischen Nachbarknoten), nur in der Flaeche
    for it in range(6):
        dc = np.zeros((GY, GX)); dc[:-1, :-1] = np.linalg.norm(np.diff(S, axis=1)[:-1], axis=2) + np.linalg.norm(np.diff(S, axis=0)[:, :-1], axis=2)
        H = nd.binary_dilation(dc > KANTE_T1, iterations=1) & nd.binary_dilation(m, iterations=1)
        if not H.any(): break
        Sg = np.stack([nd.gaussian_filter(S[..., k], 1.0) for k in range(3)], -1); S = np.where(H[..., None], Sg, S)
    kante = L3._ss(nd.distance_transform_edt(m) / KANTE)
    ring_k = kenn(V, ring); vorher = kenn(V, m)
    # Farbangleich je Zone (Nord D4 / Sued D5, Grenze z ZGRENZE weich ueber 6 Zellen): Mittel-RGB der fertigen Flaeche = Mittel des Zonenrings
    zz = np.arange(GY)[:, None] / rs * np.ones((1, GX)); ws = L3._ss((zz - (ZGRENZE - 3)) / 6.0); zonen = ((1 - ws) > 0.5, ws >= 0.5)
    sh_z = [np.zeros(3), np.zeros(3)]; zring = [np.array(kenn(V, ring & z)["RGB"]) for z in zonen]
    for it in range(10):
        shift = (1 - ws)[..., None] * sh_z[0] + ws[..., None] * sh_z[1]
        Vc = np.where(ziel[..., None], S + shift, V.astype(float)); Vn = V + kante[..., None] * (Vc - V)
        Vn = np.clip(np.round(Vn), 0, 255).astype(np.uint8)
        d = [zring[i] - Vn[m & zonen[i]].astype(float).mean(0) for i in range(2)]; sh_z = [sh_z[i] + d[i] for i in range(2)]
        if max(np.abs(x).max() for x in d) < 0.2: break
    nachher = kenn(Vn, m)
    vc_ge = (Vn != V).any(-1)
    if (vc_ge & sperr).any(): sys.exit("Sperrbereich/D2 geaendert - Abbruch")
    if (vc_ge & ~nd.binary_dilation(box, iterations=2)).any(): sys.exit("VC ausserhalb S7-Box - Abbruch")
    vi = np.flatnonzero(vc_ge.reshape(-1)); rueck = {"vc_idx": vi, "vc_alt": V.reshape(-1, 3)[vi]}
    for X, k in ((D, "fwd"), (N, "fwn")):
        X["VC"] = base64.b64encode(Vn.tobytes()).decode()
        FW = X["FW"]; FS = int(FW["fs"]); FX = X["nx"] * FS + 1; vid = np.frombuffer(base64.b64decode(FW["vid"]), np.uint32).astype(np.int64)
        gi = np.clip(np.rint((vid // FX) / FS * rs).astype(int), 0, GY - 1); gj = np.clip(np.rint((vid % FX) / FS * rs).astype(int), 0, GX - 1)
        c = lade_fw_c(X); sel = np.flatnonzero(vc_ge[gi, gj]); rueck[k + "_idx"] = sel; rueck[k + "_alt"] = c[sel].copy()
        c[sel] = Vn[gi[sel], gj[sel]]; FW["c"] = base64.b64encode(c.tobytes()).decode()
    info = {"flaeche_knoten": int(m.sum()), "spender_knoten": int(ziel.sum()), "vc_knoten": int(vc_ge.sum()),
            "fw_c_punkte": [int(len(rueck["fwd_idx"])), int(len(rueck["fwn_idx"]))], "spender": SPENDER,
            "spender_anteil": {str(SPENDER[i]): int(((wahl == i) & ziel).sum()) for i in range(len(SPENDER))},
            "farbverschiebung_rgb_nord_sued": [[round(float(x), 2) for x in z] for z in sh_z], "zonen": {nm: {"ring": kenn(V, ring & z), "vorher": kenn(V, m & z), "nachher": kenn(Vn, m & z)} for nm, z in (("nord_D4", zonen[0]), ("sued_D5", zonen[1]))}, "ring": ring_k, "flaeche_vorher": vorher, "flaeche_nachher": nachher,
            "dL_vorher": round(vorher["L"] - ring_k["L"], 2), "dL_nachher": round(nachher["L"] - ring_k["L"], 2),
            "dS_vorher": round(vorher["S"] - ring_k["S"], 4), "dS_nachher": round(nachher["S"] - ring_k["S"], 4),
            "hang_grad": {"flaeche": round(float(hang[m].mean()), 1), "ring": round(float(hang[ring].mean()), 1)},
            "gb_geaendert": 0}
    stellen = {}
    for nm, (cx, cz) in (("D4_133_155", (133, 155)), ("D5_135_185", (135, 185))):
        um = np.zeros((GY, GX), bool); um[(cz - 8) * rs:(cz + 8) * rs, (cx - 8) * rs:(cx + 8) * rs] = True
        a, b = kenn(V, m & um), kenn(Vn, m & um); rk = kenn(V, ring & nd.binary_dilation(um, iterations=24))
        stellen[nm] = {"ring": rk, "vorher": a, "nachher": b, "dL_vorher": round(a["L"] - rk["L"], 2), "dL_nachher": round(b["L"] - rk["L"], 2),
                       "dS_vorher": round(a["S"] - rk["S"], 4), "dS_nachher": round(b["S"] - rk["S"], 4)}
    info["stellen"] = stellen
    AUSD.mkdir(parents=True, exist_ok=True); np.savez_compressed(RUECK, **rueck)
    L3._schreibe(D, L3.QUELLE, False); L3._schreibe(N, L3.NEU, True)
    (AUSD / "p2e_bericht.json").write_text(json.dumps(info, indent=1, default=str), encoding="utf-8"); print(json.dumps(info, indent=1, default=str))

if __name__ == "__main__":
    main()

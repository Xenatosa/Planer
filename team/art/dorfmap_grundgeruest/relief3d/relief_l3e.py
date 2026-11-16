#!/usr/bin/env python3
"""L3e (16.11.2026): Uferlinien E7-H7 (F7-Nordufer-Zaehnchen, G7-Nordufer-Treppe, G7-Plaettchen 283,5|268,8) und Rest E3-West.
Abschaltbarer Nachschritt NACH L3d (bau_endstand.sh Schritt 13), eigener Basis-Hash und Rueckweg.
  python3 relief_l3e.py            anwenden (nur wenn GB/WV/VC dem Stand nach L3d = b3698e0 entsprechen)
  python3 relief_l3e.py --trocken  nur rechnen und berichten
  python3 relief_l3e.py --aus      rueckgaengig (pruefung/l3e/l3e_rueck.npz)
Ursache (gemessen): Am Ufer liegt das Land direkt neben der Maske nur 0-0,2 m ueber dem Spiegel, das Bett im ersten Wasservertex
  schon > 0,3 m darunter (teils Land unter dem Spiegel, teils Bett ueber dem Spiegel). Die Hoehenlinie Gelaende = Spiegel, an der der
  weiche Viewer-Rand (P12b) das Wasser schneidet, liegt damit immer im selben Bruchteil der Rasterkante -> Treppe/Zaehnchen auf dem
  0,5-Zellen-Raster der Maske.
Art "ufer" (Weg A): glatte Uferkurve = Nullinie des geglaetteten Vorzeichenabstands zur Maske (sigma), um "versatz" landwaerts
  verschoben, damit kein altes Wasser landseitig liegt. Im Uferband wird das Gelaende auf ein Profil Spiegel + neigung * Abstand gelegt
  (weich ausgeblendet), die Maske waechst bis zur Kurve (nur Wachstum, WV = naechster Spiegel). Damit liegt die Hoehenlinie
  Gelaende = Spiegel (und die sichtbare Wasserkante) subzellig auf der glatten Kurve statt auf den Zellstufen.
Fest: D2, Wege/Kreuzungen/Rampenkerne/WEGA (relief_l3.feste_flaechen, richtiger Massstab): 0 Vertices.
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage as nd
R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import relief_l3 as L3
import relief_l3d as L3D
CFG = R / "pruefung" / "l3e" / "l3e_stellen.json"
RUECK = R / "pruefung" / "l3e" / "l3e_rueck.npz"
BERICHT = R / "pruefung" / "l3e" / "l3e_bericht.json"
QUELLE, NEU = L3D.QUELLE, L3D.NEU
_arr, _b64, _sha = L3D._arr, L3D._b64, L3D._sha
import gzip

def ufer(GB, WV, s, rs, F):
    GY, GX = GB.shape; m = WV > -900
    w = L3D.box_gewicht(s, GY, GX, rs); w[F] = 0.0
    sd0 = np.where(m, -nd.distance_transform_edt(m) + 0.5, nd.distance_transform_edt(~m) - 0.5)
    sdg = nd.gaussian_filter(sd0, s.get("sigma_vertices", 2.0)) - s.get("versatz_vertices", 0.6) * w   # Versatz blendet zur Box-Kante aus
    _, (iz, ix) = nd.distance_transform_edt(~m, return_indices=True); Wn = WV.astype(np.float64)[iz, ix]
    Wn = np.where(m, WV, Wn)
    # Spiegel glatt fortsetzen (Viewer zeigt den geglaetteten Spiegel WR, nicht WV): Naechster-Nachbar-Fuellung hat Stufen
    # quer zum Ufer, wo der Fluss faellt -> Rippel/Kerben in Boeschung und Kante. Glatter Bezug Ws, auf altem Wasser wie WR geklemmt.
    Ws = nd.gaussian_filter(Wn, s.get("spiegel_sigma_vertices", 2.0))
    Ws = np.where(m, np.clip(Ws, WV - 0.6, WV + 0.3), Ws)
    Wa = Wn; Wn = Ws
    B = s.get("band_vertices", 5.0)
    if s.get("profil", True):
        # Ufer-Querprofil aus den Daten (Median GB - Spiegel je Abstandsklasse, P(0) = 0, monoton), auf die glatte Kurve gelegt;
        # Rest (Abweichung vom Profil) geglaettet und an der Kurve ausgeblendet -> natuerliche Boeschung, Kante subzellig glatt
        H = GB.astype(np.float64) - Wn; sel = (w > 0.999) & (np.abs(sd0) <= B + 2)
        bins = np.arange(-B - 1.5, B + 2.0, 1.0); P = np.full(len(bins), np.nan)
        for i, b in enumerate(bins):
            q = sel & (np.abs(sd0 - b) <= 0.5)
            if q.sum() >= 3: P[i] = np.median(H[q])
        ok = ~np.isnan(P); bb = np.r_[bins[ok], 0.0]; PP = np.r_[P[ok], 0.0]; o = np.argsort(bb); bb, PP = bb[o], PP[o]
        PP = np.where(bb < 0, np.minimum.accumulate(PP[::-1])[::-1].clip(max=-s.get("bett_min_m", 0.05) * 0), PP)
        PP[bb < 0] = np.minimum(PP[bb < 0], 0.0); PP[bb > 0] = np.maximum.accumulate(np.maximum(PP[bb > 0], 0.0))
        prof0 = lambda t: np.interp(t, bb, PP)
        # Kern |t| <= L linear durch 0: die lineare Dreiecksinterpolation im Viewer trifft die Nullinie dann exakt (keine
        # Phasen-Zacken der Rasterabtastung eines geknickten Profils entlang schraeger Ufer)
        L = s.get("linear_vertices", 1.5); s0 = max((prof0(L) - prof0(-L)) / (2 * L), s.get("neigung_min_m", 0.0))
        # neigung_min_m: steiler Kern -> erster Wasservertex schon tief (dunkle Wasserfarbe), kein heller Saum mit Rasterbogen
        prof = lambda t: np.where(np.abs(t) <= L, s0 * t, s0 * t * (1 - L3._ss((np.abs(t) - L) / 1.0)) + prof0(t) * L3._ss((np.abs(t) - L) / 1.0))
        tm = s.get("tiefe_min_m", 0.0)
        if tm > 0:
            # Wasserseite: Bett faellt mindestens mit s0 bis tiefe_min_m -> schmaler Flachwassersaum (keine hellen Rasterstreifen)
            prof1 = prof; prof = lambda t: np.where(t < 0, np.minimum(prof1(t), np.maximum(s0 * t, -tm)), prof1(t))
        rest = nd.gaussian_filter(H - prof(sdg), s.get("rest_sigma_vertices", 3.0)) * L3._ss((np.abs(sdg) - L - 1.5) / 2.5)
        T = Wn + prof(sdg) + rest
    else:
        T = Wn + np.where(sdg > 0, s.get("neigung_land_m", 0.12), s.get("neigung_wasser_m", 0.35)) * sdg
    a = w * (1.0 - L3._ss((np.abs(sdg) - 1.0) / max(B - 1.0, 1e-6)))
    G0 = GB.astype(np.float64); G = G0 * (1 - a) + T * a
    kern = w > 0.999
    neu = (w > 0) & ~m & (sdg < 0) & ~F
    # Vorzeichen im Kern erzwingen: neues/altes Wasser unter dem Spiegel, Land knapp darueber
    eps = s.get("eps_m", 0.005)
    wa = (m | neu) & (w > 0)
    G = np.where(wa & (G > np.minimum(Wn, np.where(m, WV, Wn)) - eps), np.minimum(G, np.minimum(Wn, np.where(m, WV, Wn)) - eps), G)
    la = (~(m | neu)) & (w > 0) & nd.binary_dilation(m | neu, np.ones((3, 3)))
    G = np.where(la & (G < Wn + eps), Wn + eps, G)
    # nur Komponenten, die an bestehendes Wasser grenzen
    lab, n = nd.label(neu, np.ones((3, 3)))
    if n:
        an = np.unique(lab[nd.binary_dilation(m, np.ones((3, 3))) & neu]); neu = np.isin(lab, an[an > 0])
    wv = np.where(neu, Wn, WV.astype(np.float64))
    G[F] = G0[F]
    return neu, wv, G, int((m & (sdg >= 0) & kern).sum()), a

def fw_ufer(D, GB, GBn, A, rs):
    """Feinband FW.h: folgt der GB-Aenderung (bilinear) und wird im Uferband mit Gewicht A auf die bilineare neue Grobhoehe
    gelegt - sonst bliebe die feine Rastertreppe des Feinbands (eigene Hoehen) am Ufer sichtbar."""
    FW = D["FW"]; fs = int(FW["fs"]); fxn = int(D["nx"]) * fs + 1
    vid = np.frombuffer(L3D.base64.b64decode(FW["vid"]), np.uint32)
    fh = np.frombuffer(L3D.base64.b64decode(FW["h"]), np.float32).copy()
    fz, fx = (vid // fxn) / fs * rs, (vid % fxn) / fs * rs
    mc = lambda F: nd.map_coordinates(F, [fz, fx], order=1, mode="nearest", prefilter=False)
    d = mc(GBn.astype(np.float64) - GB.astype(np.float64)); a = mc(A); g = mc(GBn.astype(np.float64))
    neu = (fh + d) * (1 - a) + g * a
    sel = np.flatnonzero((np.abs(d) > 1e-5) | (a > 1e-4))
    alt = fh[sel].copy(); fh[sel] = neu[sel].astype(np.float32)
    return sel, alt, L3D.base64.b64encode(fh.tobytes()).decode()

def main():
    arg = sys.argv[1:]; cfg = json.loads(CFG.read_text(encoding="utf-8"))
    D = json.load(gzip.open(QUELLE)); N = json.load(gzip.open(NEU)); rs = D["rs"]; GY, GX = D["ny"] * rs + 1, D["nx"] * rs + 1
    GB = _arr(D, "GB", np.float32, (GY, GX)); WV = _arr(D, "WV", np.float32, (GY, GX)); VC = _arr(D, "VC", np.uint8, (GY, GX, 3))
    if "--aus" in arg:
        if not RUECK.exists(): print("L3e nicht aktiv"); return
        r = np.load(RUECK)
        Gf = GB.reshape(-1).copy(); Gf[r["gb_idx"]] = r["gb_alt"]; Gn = Gf.reshape(GY, GX); delta = Gn.astype(np.float64) - GB
        Wf = WV.reshape(-1); Wf[r["wv_idx"]] = r["wv_alt"]; Vf = VC.reshape(-1, 3); Vf[r["vc_idx"]] = r["vc_alt"]
        for X in (D, N):
            X["WV"] = _b64(Wf); X["VC"] = _b64(Vf); X["GB"] = _b64(Gn); L3.objekte(X, delta, rs)
            c = np.frombuffer(L3D.base64.b64decode(X["FW"]["c"]), np.uint8).reshape(-1, 3).copy(); c[r["fc_idx"]] = r["fc_alt"]; X["FW"]["c"] = _b64(c)
            if r["fh_idx"].size: L3.fw_setzen(X, r["fh_idx"], r["fh_alt"])
        L3.prototypen(N, Gn, Gn != GB)
        L3._schreibe(D, QUELLE, False); L3._schreibe(N, NEU, True); RUECK.unlink(); print(json.dumps({"l3e": "aus"})); return
    if RUECK.exists(): sys.exit("L3e schon aktiv")
    if _sha(GB, WV, VC) != cfg["basis_gb_wv_vc_sha256"]: sys.exit(f"Basis passt nicht ({_sha(GB, WV, VC)[:12]}); Reihenfolge pruefen")
    if D["VC"] != N["VC"] or D["WV"] != N["WV"] or D["FW"]["c"] != N["FW"]["c"]: sys.exit("relief_daten/relief_neu ungleich (VC/WV/FW.c)")
    F = L3.feste_flaechen(D, GY, GX, rs)
    x0, z0, x1, z1 = L3.D2_BOX; d2 = np.zeros((GY, GX), bool); d2[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1] = True
    WVn = WV.astype(np.float64).copy(); VCn = VC.copy(); GBn = GB.astype(np.float64).copy(); bericht = []; A = np.zeros(GB.shape)
    for s in cfg["stellen"]:
        if not s.get("aktiv", True): bericht.append({"id": s["id"], "aktiv": False}); continue
        if s["art"] == "ufer":
            nw, wv, G, rest, aa = ufer(GBn, np.where(WVn > -900, WVn, -999.0), s, rs, F | d2)
            WVn[nw] = wv[nw]; d = np.abs(G - GBn); GBn = G; A = np.maximum(A, aa)
            bericht.append({"id": s["id"], "neue_wasser_vertices": int(nw.sum()), "gb_vertices": int((d > 1e-5).sum()), "gb_max_m": round(float(d.max()), 3), "altes_wasser_landseitig": rest})
        elif s["art"] == "farbe":
            Vn, a = L3D.e3_farbe(VCn, WV, s, rs); Vn[(F | d2)] = VCn[(F | d2)]
            bericht.append({"id": s["id"], "vc_vertices": int((Vn != VCn).any(-1).sum())}); VCn = Vn
    WVn = WVn.astype(np.float32); GBn = GBn.astype(np.float32); gb_ge = GBn != GB
    if (gb_ge & (F | d2)).any(): sys.exit("GB auf fester Flaeche/D2 geaendert - Abbruch")
    m0, m1 = WV > -900, WVn > -900
    if (m0 & ~m1).any(): sys.exit("Wasser entfernt - Abbruch")
    if (GBn[m1] >= WVn[m1]).sum() > (GB[m0] >= WV[m0]).sum(): sys.exit("mehr Bett ueber dem Spiegel als vorher - Abbruch")
    wv_ge = WVn != WV; vc_ge = (VCn != VC).any(-1)
    if (wv_ge & ~(m1 & ~m0)).any(): sys.exit("WV auf altem Wasser geaendert - Abbruch")
    if ((wv_ge | vc_ge) & (F | d2)).any(): sys.exit("feste Flaeche/D2 beruehrt - Abbruch")
    lab0, n0 = nd.label(m0, np.ones((3, 3))); lab1, n1 = nd.label(m1, np.ones((3, 3)))
    loch = nd.binary_fill_holes(m1) & ~m1 & ~(nd.binary_fill_holes(m0) & ~m0)
    if loch.any(): sys.exit(f"neue eingeschlossene Landinseln: {int(loch.sum())} - Abbruch")
    if n1 != n0: sys.exit(f"Wasserkomponenten {n0} -> {n1} - Abbruch")
    info = {"stellen": bericht, "wasser_neu": int((m1 & ~m0).sum()), "wasser_entfernt": 0, "wasser_komponenten": [int(n0), int(n1)],
            "bett_ueber_spiegel": [int((GB[m0] >= WV[m0]).sum()), int((GBn[m1] >= WVn[m1]).sum())],
            "vc_vertices": int(vc_ge.sum()), "gb_vertices": int(gb_ge.sum()), "gb_max_abs_m": round(float(np.abs(GBn.astype(float) - GB).max()), 3),
            "basis": cfg["basis_gb_wv_vc_sha256"], "nachher_sha256": _sha(GBn, WVn, VCn)}
    c, fidx, falt = L3D.fw_c_aus_vc(D, VCn, vc_ge); info["fw_c_punkte"] = int(fidx.size)
    hidx, halt, fh_neu = fw_ufer(D, GB, GBn, A, rs); info["fw_h_punkte"] = int(hidx.size)
    if "--trocken" in arg: print(json.dumps(info, indent=1)); return
    widx = np.flatnonzero(wv_ge.reshape(-1)); vidx = np.flatnonzero(vc_ge.reshape(-1)); gidx = np.flatnonzero(gb_ge.reshape(-1))
    np.savez_compressed(RUECK, gb_idx=gidx, gb_alt=GB.reshape(-1)[gidx], wv_idx=widx, wv_alt=WV.reshape(-1)[widx], vc_idx=vidx, vc_alt=VC.reshape(-1, 3)[vidx],
                        fc_idx=fidx, fc_alt=falt, fh_idx=hidx, fh_alt=halt)
    for X in (D, N):
        X["WV"] = _b64(WVn); X["VC"] = _b64(VCn); X["FW"]["c"] = _b64(c); X["GB"] = _b64(GBn)
        if hidx.size: X["FW"]["h"] = fh_neu
    delta = GBn.astype(np.float64) - GB.astype(np.float64)
    info["objekte_angepasst"] = L3.objekte(D, delta, rs); L3.objekte(N, delta, rs)
    info["prototypen"] = L3.prototypen(N, GBn, gb_ge)
    L3._schreibe(D, QUELLE, False); L3._schreibe(N, NEU, True)
    BERICHT.write_text(json.dumps(info, indent=1, ensure_ascii=False), encoding="utf-8"); print(json.dumps(info, indent=1))

if __name__ == "__main__":
    main()

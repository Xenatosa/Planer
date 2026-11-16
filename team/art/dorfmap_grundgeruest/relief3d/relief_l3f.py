#!/usr/bin/env python3
"""L3f/L3g (16.11.2026): E3-Westufer (~188|100 / 190|106) und F7/G7-Lichtspitzen (Nordufer ~240-252|265-271) + kartenweite WV-Randstufen.
Abschaltbarer Nachschritt NACH P2d (bau_endstand.sh Schritt 15), eigener Basis-Hash und Rueckweg.
  python3 relief_l3f.py            anwenden (nur wenn GB/WV/VC dem Stand nach Schritt 14 = art/dorfmap-fertig 8c1fc80 entsprechen)
  python3 relief_l3f.py --trocken  nur rechnen und berichten
  python3 relief_l3f.py --aus      rueckgaengig (pruefung/l3f/l3f_rueck.npz)
Ursache (gemessen, pruefung/l3f/l3f_ursache.json + Nahbilder diag_*): Die Zickzacklinie am E3-Westufer steckt NICHT in der Farbe.
  VC ist dort seit L3d schon glatt (Gradientenlinien glatt); ein Testlauf mit stark geglaetteter VC (Gauss 3) laesst die Linie stehen,
  ein Testlauf mit geglaettetem GB nimmt sie weg. Sie ist Schattierung einer Gelaendekante: die Boeschung des Bachbetts knickt genau auf
  den 0,5-Zellen-Stufen der Wassermaske (Bett gegenueber dem Ufer abgesenkt) -> treppige Normalen, auf dem dunklen Bett-VC als dunkle Zacke.
Art "boeschung": im Band |Abstand zur Maske| <= band_vertices wird GB weich (Gewicht, Box-Fade, Abstand zu festen Flaechen) zum
  Gauss-geglaetteten GB hin gemischt (Mischung ueber ein Abstandsfeld zum Ufer, nicht ueber Zellklassen). Wassermaske, WV und VC bleiben
  bitgleich; das Bett wird nie angehoben; Vorzeichen bleiben: Bett unter dem Spiegel bleibt >= eps darunter, Ufer-Land darueber bleibt >= eps darueber.
Stand: E3-West alle Versuche gescheitert (ERGEBNIS_L3f.md, "aktiv": false). Nachtrag FG7_sued (Art "ufer" wie L3e): Landecken knapp ueber
  dem Spiegel am Suedufer werden Wasser bzw. liegen auf dem Profil; Maske waechst nur (kein Wasser entfernt, keine Loecher).
L3g (freigegeben von Grundgeruest): Art "wv_ring" hebt den aeusseren WV-Ring (deutlich unter dem geglaetteten Innenniveau) an, nie ueber das
  Nachbargelaende, Maske bleibt; Art "ufer" mit Versatz verbreitert/verflacht die E3-Rinne (nur Wasser hinzu).
Fest: D2, Wege/Kreuzungen/Rampenkerne/WEGA (relief_l3.feste_flaechen, richtiger Massstab): 0 Vertices.
"""
import json, sys, gzip
from pathlib import Path
import numpy as np
from scipy import ndimage as nd
R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import relief_l3 as L3
import relief_l3d as L3D
import relief_l3e as L3E
CFG = R / "pruefung" / "l3f" / "l3f_stellen.json"
RUECK = R / "pruefung" / "l3f" / "l3f_rueck.npz"
BERICHT = R / "pruefung" / "l3f" / "l3f_bericht.json"
QUELLE, NEU = L3D.QUELLE, L3D.NEU
_arr, _b64, _sha = L3D._arr, L3D._b64, L3D._sha

def ufer_fest(GB, WV, s, rs, F):
    """Wie L3e Art "ufer" (Profil ueber den geglaetteten Vorzeichenabstand zur Maske, linearer Kern durch den Spiegel), aber die Maske
    bleibt bitgleich: die glatte Kurve liegt um versatz wasserwaerts (versatz_vertices < 0), Vertices, die L3e zu Wasser gemacht haette,
    bleiben Land (>= Spiegel + eps). Wasser-Randvertices duerfen dabei flacher werden (nie ueber Spiegel - eps)."""
    m = WV > -900
    nw, _wv, G, _rest, a = L3E.ufer(GB, WV, s, rs, F)
    eps = s.get("eps_m", 0.005)
    _, (iz, ix) = nd.distance_transform_edt(~m, return_indices=True); Wn = WV.astype(np.float64)[iz, ix]
    G = np.where(~m, np.maximum(G, np.where(GB >= Wn, Wn + eps, G)), G)   # Land bleibt Land (Vorzeichen wie vorher)
    G = np.where(m & (GB < WV), np.minimum(G, WV - eps), G)
    G[F] = GB.astype(np.float64)[F]
    return G, a, int(nw.sum())

def boeschung(GB, WV, s, rs, F):
    GY, GX = GB.shape; m = WV > -900
    w = L3D.box_gewicht(s, GY, GX, rs)
    dF = nd.distance_transform_edt(~F)                       # Vertices
    w = w * L3._ss((dF - s.get("fest_abstand_vertices", 2.0)) / s.get("fest_fade_vertices", 3.0)); w[F] = 0.0
    sd = np.where(m, -nd.distance_transform_edt(m) + 0.5, nd.distance_transform_edt(~m) - 0.5)
    B = s.get("band_vertices", 6.0)
    a = w * (1.0 - L3._ss((np.abs(sd) - B) / 2.0))
    G0 = GB.astype(np.float64)
    Gs = nd.gaussian_filter(G0, s.get("sigma_vertices", 2.0))
    G = G0 * (1 - a) + Gs * a
    eps = s.get("eps_m", 0.005)
    _, (iz, ix) = nd.distance_transform_edt(~m, return_indices=True); Wn = WV.astype(np.float64)[iz, ix]
    # Bett hoechstens bis tiefe_min_m unter den Spiegel anheben (Wasser bleibt dunkel/sichtbar, P12b-Farbe e ~ 0), tiefer liegendes
    # Bett darf der Glaettung folgen; Bett ueber dem Spiegel nie anheben
    dmin = s.get("tiefe_min_m", 0.35)
    G = np.where(m, np.minimum(G, np.maximum(G0, WV - dmin)), G)
    unten = m & (G0 < WV); G = np.where(unten, np.minimum(G, WV - eps), G)
    ring = ~m & nd.binary_dilation(m, np.ones((3, 3)), iterations=2)
    oben = ring & (G0 >= Wn)
    G = np.where(oben, np.maximum(G, Wn + eps), G)
    G[F] = G0[F]
    return G, a

def main():
    arg = sys.argv[1:]; cfg = json.loads(CFG.read_text(encoding="utf-8"))
    D = json.load(gzip.open(QUELLE)); N = json.load(gzip.open(NEU)); rs = D["rs"]; GY, GX = D["ny"] * rs + 1, D["nx"] * rs + 1
    GB = _arr(D, "GB", np.float32, (GY, GX)); WV = _arr(D, "WV", np.float32, (GY, GX)); VC = _arr(D, "VC", np.uint8, (GY, GX, 3))
    if "--aus" in arg:
        if not RUECK.exists(): print("L3f nicht aktiv"); return
        r = np.load(RUECK)
        Gf = GB.reshape(-1).copy(); Gf[r["gb_idx"]] = r["gb_alt"]; Gn = Gf.reshape(GY, GX); delta = Gn.astype(np.float64) - GB
        Wf = WV.reshape(-1); Wf[r["wv_idx"]] = r["wv_alt"]; Vf = VC.reshape(-1, 3); Vf[r["vc_idx"]] = r["vc_alt"]
        for X in (D, N):
            X["WV"] = _b64(Wf); X["VC"] = _b64(Vf); X["GB"] = _b64(Gn); L3.objekte(X, delta, rs)
            c = np.frombuffer(L3D.base64.b64decode(X["FW"]["c"]), np.uint8).reshape(-1, 3).copy(); c[r["fc_idx"]] = r["fc_alt"]; X["FW"]["c"] = _b64(c)
            if r["fh_idx"].size: L3.fw_setzen(X, r["fh_idx"], r["fh_alt"])
        L3.prototypen(N, Gn, Gn != GB)
        L3._schreibe(D, QUELLE, False); L3._schreibe(N, NEU, True); RUECK.unlink(); print(json.dumps({"l3f": "aus"})); return
    if RUECK.exists(): sys.exit("L3f schon aktiv")
    if not any(s.get("aktiv", True) for s in cfg["stellen"]):
        # Stand L3f: keine Stelle aktiv (Versuche a-d gescheitert, Grundgeruest entscheidet) -> nichts rechnen, nichts schreiben
        print(json.dumps({"l3f": "keine aktive Stelle, nichts geschrieben", "versuche": [s["id"] for s in cfg["stellen"]]})); return
    if _sha(GB, WV, VC) != cfg["basis_gb_wv_vc_sha256"]: sys.exit(f"Basis passt nicht ({_sha(GB, WV, VC)[:12]}); Reihenfolge pruefen")
    if D["VC"] != N["VC"] or D["WV"] != N["WV"] or D["FW"]["c"] != N["FW"]["c"]: sys.exit("relief_daten/relief_neu ungleich (VC/WV/FW.c)")
    F = L3.feste_flaechen(D, GY, GX, rs)
    x0, z0, x1, z1 = L3.D2_BOX; d2 = np.zeros((GY, GX), bool); d2[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1] = True
    WVn = WV.astype(np.float64).copy(); VCn = VC.copy(); GBn = GB.astype(np.float64).copy(); bericht = []; A = np.zeros(GB.shape)
    RING = np.zeros(GB.shape, bool); zz, xx = np.mgrid[0:GY, 0:GX] / float(rs)
    sperr_d1 = np.hypot(xx - 159.0, zz - 22.9) <= 20.0   # Sperrzone D1 Mulde 159|22,9 (Radius 20 Zellen); Rampenkerne stecken in F
    for s in cfg["stellen"]:
        if not s.get("aktiv", True): bericht.append({"id": s["id"], "aktiv": False}); continue
        if s["art"] == "ufer":
            # wie L3e (Weg A): Maske waechst bis zur glatten Kurve (nur Wachstum), Boeschung auf Profil durch den Spiegel
            nw, wv, G, rest, aa = L3E.ufer(GBn, np.where(WVn > -900, WVn, -999.0), s, rs, F | d2)
            WVn[nw] = wv[nw]; d = np.abs(G - GBn); GBn = G; A = np.maximum(A, aa)
            ne = 0
            if s.get("ecken_fuellen"):
                # Versuch 2 (Nachtrag FG7): Treppenecken der Maske (Land mit >= min_nachbarn Wasser-Nachbarn, knapp ueber dem Spiegel)
                # werden Wasser; Bett unter den Spiegel. Nur Wachstum, nur in der Box, nie auf fester Flaeche/D2.
                e = s["ecken_fuellen"]; box = np.zeros(GBn.shape, bool)
                box[int(s["z0"] * rs):int(s["z1"] * rs) + 1, int(s["x0"] * rs):int(s["x1"] * rs) + 1] = True
                G = GBn.copy()
                for _ in range(e.get("runden", 3)):
                    ok = WVn > -900; P = np.pad(np.where(ok, WVn, 0.0), 1); O = np.pad(ok, 1)
                    PM = np.pad(np.where(ok, WVn, -999.0), 1); H, W_ = GBn.shape
                    nb = [(dj, di) for dj in (-1, 0, 1) for di in (-1, 0, 1) if dj or di]
                    cnt = sum(O[1 + dj:1 + dj + H, 1 + di:1 + di + W_].astype(int) for dj, di in nb)
                    sm = sum(P[1 + dj:1 + dj + H, 1 + di:1 + di + W_] for dj, di in nb)
                    mx = np.max([PM[1 + dj:1 + dj + H, 1 + di:1 + di + W_] for dj, di in nb], 0)
                    sel = box & ~ok & ~(F | d2) & (cnt >= e.get("min_nachbarn", 4)) & (G < mx + e.get("hoehe_max_m", 0.35))
                    if not sel.any(): break
                    wvn = sm / np.maximum(cnt, 1); WVn[sel] = wvn[sel]; G[sel] = np.minimum(G[sel], wvn[sel] - e.get("tiefe_m", 0.3)); ne += int(sel.sum())
                dd = np.abs(G - GBn); A = np.maximum(A, (dd > 1e-6).astype(float)); GBn = G; d = np.maximum(d, dd)
            bericht.append({"id": s["id"], "neue_wasser_vertices": int(nw.sum()) + ne, "davon_ecken": ne, "gb_vertices": int((d > 1e-5).sum()), "gb_max_m": round(float(d.max()), 3), "altes_wasser_landseitig": rest})
        if s["art"] == "wv_ring":
            # L3g (1): aeusserer WV-Ring deutlich unter dem Innenniveau (auf dem Maskenraster gestuft) -> auf das geglaettete Innenmittel heben.
            # Maske/Uferlinie bleiben; nur Anheben; nie ueber das benachbarte Gelaende (3x3 Land-Minimum - eps), sonst bleibt der Wert.
            ok = WVn > -900; dist = nd.distance_transform_edt(ok); inn = ok & (dist >= s.get("innen_ab_vertices", 3.0))
            sg = s.get("sigma_vertices", 3.0); w = nd.gaussian_filter(inn.astype(float), sg)
            Rr = nd.gaussian_filter(np.where(inn, WVn, 0.0), sg) / np.maximum(w, 1e-9)
            landmin = nd.minimum_filter(np.where(ok, 1e9, GBn), size=3); eps = s.get("eps_m", 0.02)
            box = np.ones(GB.shape, bool) if s.get("kartenweit") else ((xx >= s["x0"]) & (xx <= s["x1"]) & (zz >= s["z0"]) & (zz <= s["z1"]))
            kand = box & ok & (dist < s.get("innen_ab_vertices", 3.0)) & (w > 0.05) & (WVn < Rr - s.get("schwelle_m", 0.15)) & ~(F | d2 | sperr_d1)
            lab, n = nd.label(kand, np.ones((3, 3)))
            if n:
                gr = nd.sum(kand, lab, range(1, n + 1)); kand &= np.isin(lab, 1 + np.flatnonzero(gr >= s.get("min_cluster", 10)))
            if s.get("kappen"): ziel = np.minimum(Rr, landmin - eps); sel = kand & (ziel > WVn + 0.01)
            if s.get("max_hebung_m"): ziel = np.minimum(ziel, WVn + s["max_hebung_m"])   # grosse Spruenge (Inselspitzen) nur teilweise
            else: ziel = Rr; sel = kand & (ziel <= landmin - eps)
            liste = []
            lab, n = nd.label(kand, np.ones((3, 3)))
            for k in range(1, n + 1):
                q = lab == k; qs = q & sel
                liste.append({"x": round(float(xx[q].mean()), 1), "z": round(float(zz[q].mean()), 1), "ring_vertices": int(q.sum()), "angehoben": int(qs.sum()),
                              "ring_minus_innen_vorher_m": round(float((WVn - Rr)[q].mean()), 3),
                              "ring_minus_innen_nachher_m": round(float((np.where(sel, ziel, WVn) - Rr)[q].mean()), 3),
                              "max_hebung_m": round(float((ziel - WVn)[qs].max()), 3) if qs.any() else 0.0})
            WVn[sel] = ziel[sel]; RING |= sel
            bericht.append({"id": s["id"], "kandidaten": int(kand.sum()), "angehoben": int(sel.sum()), "bleibt_wegen_gelaende": int((kand & ~sel).sum()), "stellen": liste})
        if s["art"] == "ufer_fest":
            G, aa, nn = ufer_fest(GBn, np.where(WVn > -900, WVn, -999.0), s, rs, F | d2)
            d = np.abs(G - GBn); GBn = G; A = np.maximum(A, aa * s.get("fw_glatt", 1.0))
            bericht.append({"id": s["id"], "gb_vertices": int((d > 1e-5).sum()), "gb_max_m": round(float(d.max()), 3), "haette_wasser_vertices_bleiben_land": nn})
        if s["art"] == "boeschung":
            G, aa = boeschung(GBn, np.where(WVn > -900, WVn, -999.0), s, rs, F | d2)
            d = np.abs(G - GBn); GBn = G; A = np.maximum(A, aa * s.get("fw_glatt", 0.0))
            bericht.append({"id": s["id"], "gb_vertices": int((d > 1e-5).sum()), "gb_max_m": round(float(d.max()), 3)})
    WVn = WVn.astype(np.float32); GBn = GBn.astype(np.float32); gb_ge = GBn != GB
    if (gb_ge & (F | d2)).any(): sys.exit("GB auf fester Flaeche/D2 geaendert - Abbruch")
    m0, m1 = WV > -900, WVn > -900
    if (m0 & ~m1).any(): sys.exit("Wasser entfernt - Abbruch")
    if (GBn[m1] >= WVn[m1]).sum() > (GB[m0] >= WV[m0]).sum(): sys.exit("mehr Bett ueber dem Spiegel als vorher - Abbruch")
    wv_ge = WVn != WV; vc_ge = (VCn != VC).any(-1)
    if (wv_ge & ~(m1 & ~m0) & ~RING).any(): sys.exit("WV auf altem Wasser ausserhalb wv_ring geaendert - Abbruch")
    if (RING & (WVn < WV)).any(): sys.exit("wv_ring hat WV gesenkt - Abbruch")
    lm = nd.minimum_filter(np.where(m1, 1e9, GBn.astype(np.float64)), size=3)
    if (RING & (WVn >= lm)).any(): sys.exit("wv_ring ueber benachbartem Gelaende - Abbruch")
    if ((wv_ge | vc_ge) & (F | d2)).any(): sys.exit("feste Flaeche/D2 beruehrt - Abbruch")
    lab0, n0 = nd.label(m0, np.ones((3, 3))); lab1, n1 = nd.label(m1, np.ones((3, 3)))
    loch = nd.binary_fill_holes(m1) & ~m1 & ~(nd.binary_fill_holes(m0) & ~m0)
    if loch.any(): sys.exit(f"neue eingeschlossene Landinseln: {int(loch.sum())} - Abbruch")
    if n1 != n0: sys.exit(f"Wasserkomponenten {n0} -> {n1} - Abbruch")
    info = {"stellen": bericht, "wasser_neu": int((m1 & ~m0).sum()), "wasser_entfernt": 0, "wasser_komponenten": [int(n0), int(n1)],
            "bett_ueber_spiegel": [int((GB[m0] >= WV[m0]).sum()), int((GBn[m1] >= WVn[m1]).sum())],
            "wv_ring_vertices": int(RING.sum()), "vc_vertices": int(vc_ge.sum()), "gb_vertices": int(gb_ge.sum()), "gb_max_abs_m": round(float(np.abs(GBn.astype(float) - GB).max()), 3),
            "basis": cfg["basis_gb_wv_vc_sha256"], "nachher_sha256": _sha(GBn, WVn, VCn)}
    c, fidx, falt = L3D.fw_c_aus_vc(D, VCn, vc_ge); info["fw_c_punkte"] = int(fidx.size)
    hidx, halt, fh_neu = L3E.fw_ufer(D, GB, GBn, A, rs); info["fw_h_punkte"] = int(hidx.size)
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

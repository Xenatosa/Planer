#!/usr/bin/env python3
"""L3k (16.11.2026, Kritiker P8): Kerbe am Grat an der Kachelecke B3/C3/B4/C4 bei 84|129.
Ursache (gemessen): Die steile Westflanke laeuft von z 118 bis 125 nach Suedwesten (Hoehenlinie 5 m von x 85,7 auf 83,7), steht dann von z 125,5 bis 130
senkrecht auf der Kachelnaht x = 84 bzw. springt sogar zurueck nach Osten (83,7 -> 84,0) und knickt erst ab z 130,5 (Naht z = 129) wieder nach Suedwesten ab;
dazu eine Delle von ~0,3 m in der Gratkante x 86,5 bei z 128. Das stammt aus der kachelweisen Grundgenerierung (kein spaeterer L3-/P2-Schritt hat dort
etwas geaendert, geprueft ueber alle *_rueck.npz).
Art "laengs_glatt": GB im Kreis um die Kerbe laengs der Gratrichtung ("richtung" dx,dz bzw. achse) mit einer Gauss-Glaettung ausgleichen, weich eingeblendet; Wandquellzellen
(vektor.json waende[].quellzellen) und feste Flaechen/Sperrzonen bleiben unberuehrt, kein Wasser in der Naehe (Abbruch sonst). Arten wie relief_l3j.py.
Abschaltbarer Nachschritt NACH L3j (bau_endstand.sh Schritt 20; Schritt 19 = L3j), eigener Basis-Hash und Rueckweg.
  python3 relief_l3k.py            anwenden (nur wenn GB/WV/VC dem Stand nach Schritt 19 = art/dorfmap-fertig cc33fd1 entsprechen)
  python3 relief_l3k.py --trocken  nur rechnen und berichten
  python3 relief_l3k.py --aus      rueckgaengig (pruefung/l3k/l3k_rueck.npz)
Fest: D2, Wege/Kreuzungen/Rampenkerne/WEGA/Bruecken (relief_l3.feste_flaechen): 0 Vertices. Sperrzonen: D4/D5 (x 126-168, z 129-215, rampe_5),
D1 (x 126-168, z 0-43 inkl. X084/rampe_2) und Mulde 159|22,9 (Radius 20) - Abbruch, wenn dort etwas geaendert wuerde.
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
CFG = R / "pruefung" / "l3k" / "l3k_stellen.json"
RUECK = R / "pruefung" / "l3k" / "l3k_rueck.npz"
BERICHT = R / "pruefung" / "l3k" / "l3k_bericht.json"
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
        if not RUECK.exists(): print("L3k nicht aktiv"); return
        r = np.load(RUECK)
        Gf = GB.reshape(-1).copy(); Gf[r["gb_idx"]] = r["gb_alt"]; Gn = Gf.reshape(GY, GX); delta = Gn.astype(np.float64) - GB
        Wf = WV.reshape(-1); Wf[r["wv_idx"]] = r["wv_alt"]; Vf = VC.reshape(-1, 3); Vf[r["vc_idx"]] = r["vc_alt"]
        for X in (D, N):
            X["WV"] = _b64(Wf); X["VC"] = _b64(Vf); X["GB"] = _b64(Gn); L3.objekte(X, delta, rs)
            c = np.frombuffer(L3D.base64.b64decode(X["FW"]["c"]), np.uint8).reshape(-1, 3).copy(); c[r["fc_idx"]] = r["fc_alt"]; X["FW"]["c"] = _b64(c)
            if r["fh_idx"].size: L3.fw_setzen(X, r["fh_idx"], r["fh_alt"])
        L3.prototypen(N, Gn, Gn != GB)
        L3._schreibe(D, QUELLE, False); L3._schreibe(N, NEU, True); RUECK.unlink(); print(json.dumps({"l3k": "aus"})); return
    if RUECK.exists(): sys.exit("L3k schon aktiv")
    if not any(s.get("aktiv", True) for s in cfg["stellen"]):
        print(json.dumps({"l3k": "keine aktive Stelle, nichts geschrieben", "versuche": [s["id"] for s in cfg["stellen"]]})); return
    if _sha(GB, WV, VC) != cfg["basis_gb_wv_vc_sha256"]: sys.exit(f"Basis passt nicht ({_sha(GB, WV, VC)[:12]}); Reihenfolge pruefen")
    if D["VC"] != N["VC"] or D["WV"] != N["WV"] or D["FW"]["c"] != N["FW"]["c"]: sys.exit("relief_daten/relief_neu ungleich (VC/WV/FW.c)")
    F = L3.feste_flaechen(D, GY, GX, rs)
    x0, z0, x1, z1 = L3.D2_BOX; d2 = np.zeros((GY, GX), bool); d2[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1] = True
    WVn = WV.astype(np.float64).copy(); VCn = VC.copy(); GBn = GB.astype(np.float64).copy(); bericht = []; A = np.zeros(GB.shape)
    RING = np.zeros(GB.shape, bool); WEG = np.zeros(GB.shape, bool); WVHOCH = np.zeros(GB.shape, bool); zz, xx = np.mgrid[0:GY, 0:GX] / float(rs)
    sperr_d1 = (np.hypot(xx - 159.0, zz - 22.9) <= 20.0) | ((xx >= 126) & (xx <= 168) & (zz <= 43))   # D1 + Mulde
    sperr_d1 |= (xx >= 126) & (xx <= 168) & (zz >= 129) & (zz <= 215)                                  # D4/D5 (rampe_5, Wege & Deko)
    for s in cfg["stellen"]:
        if not s.get("aktiv", True): bericht.append({"id": s["id"], "aktiv": False}); continue
        if s["art"] == "ufer":
            # wie L3e (Weg A): Maske waechst bis zur glatten Kurve (nur Wachstum), Boeschung auf Profil durch den Spiegel
            nw, wv, G, rest, aa = L3E.ufer(GBn, np.where(WVn > -900, WVn, -999.0), s, rs, F | d2 | sperr_d1)
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
        if s["art"] == "bett_tiefer":
            # L3h (1): Bett im Kern tiefer und Bett-VC dunkler; Gewicht ueber geglaetteten Abstand zum Ufer (Vertices), Ufer-Vertex (Abstand <= d0) bleibt.
            ok = WVn > -900; box = L3D.box_gewicht(s, GY, GX, rs); box[F | d2 | sperr_d1] = 0.0
            dist = nd.gaussian_filter(nd.distance_transform_edt(ok), s.get("sigma_vertices", 1.0))
            w = box * L3._ss((dist - s.get("d0", 1.0)) / max(s.get("d1", 3.0) - s.get("d0", 1.0), 1e-6)) * ok
            if s.get("laengs_sigma"):
                # Tiefe laengs der Rinne verschmieren (normierte Faltung nur ueber Wasser): keine Perlenkette aus Tuempeln an breiten Stellen
                ls = s["laengs_sigma"]; wl = nd.gaussian_filter(w * ok, ls) / np.maximum(nd.gaussian_filter(ok.astype(float), ls), 1e-6)
                w = np.maximum(w, s.get("laengs_anteil", 0.7) * wl * box * L3._ss((dist - s.get("d0", 1.0)) / 0.6)) * ok   # Ufer-Vertex bleibt
            ziel = WVn - s.get("tiefe_kern_m", 0.7)
            G = np.where(ok, np.minimum(GBn, GBn + w * (ziel - GBn)), GBn)
            d = np.abs(G - GBn); GBn = G
            wc = box * L3._ss((dist - s.get("vc_d0", 0.5)) / max(s.get("vc_d1", 2.5) - s.get("vc_d0", 0.5), 1e-6)) * ok * s.get("vc_mix", 0.0)
            if s.get("vc_glatt_sigma"):
                # VC-Uebergang am Ufer ueber geglaettetes Vorzeichen-Abstandsfeld weichzeichnen (Farbstufe auf dem Maskenraster -> Verlauf)
                sd = nd.gaussian_filter(np.where(ok, -nd.distance_transform_edt(ok) + 0.5, nd.distance_transform_edt(~ok) - 0.5), 1.5)
                wb = box * (1.0 - L3._ss((np.abs(sd) - s.get("vc_glatt_band", 4.0)) / 2.0)); wb[F | d2 | sperr_d1] = 0.0
                Vf = VCn.astype(float); Vg = np.stack([nd.gaussian_filter(Vf[..., k], s["vc_glatt_sigma"]) for k in range(3)], -1)
                VCn = np.clip(np.round(Vf + wb[..., None] * (Vg - Vf)), 0, 255).astype(np.uint8)
            if s.get("vc_mix", 0.0) > 0:
                ton = np.asarray(s["vc_ton"], float); Vf = VCn.astype(float); Vf = Vf + wc[..., None] * (ton - Vf)
                VCn = np.clip(np.round(Vf), 0, 255).astype(np.uint8)
            bericht.append({"id": s["id"], "gb_vertices": int((d > 1e-5).sum()), "gb_max_m": round(float(d.max()), 3), "vc_vertices": int((VCn != VC).any(-1).sum())})
        if s["art"] == "hang_glatt":
            # Freigabe L3h (2): Talhang neben einer Rinnenverbreiterung glaetten (G6-Facetten): nur Land, Abstand zum Wasser >= wasser_abstand,
            # weiche Kreise um die Punkte, mehrfach Gauss (sigma) eingeblendet; Feinband folgt (A). Nie auf fester Flaeche/D2/Sperrzone.
            ok = WVn > -900; w = np.zeros(GB.shape)
            for px, pz in s["punkte"]: w = np.maximum(w, 1.0 - L3._ss((np.hypot(xx - px, zz - pz) - s.get("r_kern", 1.5)) / s.get("r_fade", 2.0)))
            w *= L3._ss((nd.distance_transform_edt(~ok) - s.get("wasser_abstand", 1.0)) / 1.0); w[F | d2 | sperr_d1 | ok] = 0.0
            G = GBn.copy()
            for _ in range(s.get("runden", 3)): G = G + w * (nd.gaussian_filter(G, s.get("sigma_vertices", 1.5)) - G)
            d = np.abs(G - GBn); GBn = G; A = np.maximum(A, (w > 1e-3) * s.get("feinband", 1.0))
            bericht.append({"id": s["id"], "gb_vertices": int((d > 1e-5).sum()), "gb_max_m": round(float(d.max()), 3)})
        if s["art"] == "kanal":
            # L3i (1): Kanal gleicher Breite ueber die Tuempelkette. Mittellinie = je Vertexzeile Mitte des Wasserlaufs in [x0,x1], geglaettet (sigma_z).
            # Kanal = |x - cx(z)| <= halbbreite (Zellen) fuer z0..z1. Spiegel im Kanal = spiegel_m (alte Werte nur angehoben, nie gesenkt);
            # Bett: Kern spiegel - tiefe_m, Randzelle linear auf rand_tiefe_m; Land im Band b: Profil spiegel + rand_hoehe + neigung*d (nur absenken,
            # nie unter spiegel + eps), weich eingeblendet. VC: Kern/Rand-Ton, Land im Band Richtung geglaettetem Land-VC.
            ok = WVn > -900; zr = np.arange(GY) / float(rs); cx = np.full(GY, np.nan)
            for j in range(int(s["z0"] * rs) - 6, int(s["z1"] * rs) + 7):
                xs = np.flatnonzero(ok[j, int(s["x0"] * rs):int(s["x1"] * rs) + 1])
                if xs.size: cx[j] = (xs.min() + xs.max()) / 2.0 / rs + s["x0"]
            jj = np.flatnonzero(~np.isnan(cx)); cxi = np.interp(np.arange(GY), jj, cx[jj])
            cxs = nd.gaussian_filter1d(cxi, s.get("sigma_z_vertices", 4.0)); cxs[:jj.min()] = np.nan; cxs[jj.max() + 1:] = np.nan
            dx = np.abs(xx - cxs[:, None])
            # L3j: Trichter - Halbbreite/Tiefe linear von *_start (bei z0) auf den Endwert (bei z1); ohne *_start konstant wie L3i
            fz = np.clip((zz - s["z0"]) / max(s["z1"] - s["z0"], 1e-6), 0.0, 1.0)
            hb = s.get("halbbreite_start_zellen", s["halbbreite_zellen"]) + (s["halbbreite_zellen"] - s.get("halbbreite_start_zellen", s["halbbreite_zellen"])) * fz
            zin = (zz >= s["z0"]) & (zz <= s["z1"])
            kan = zin & (dx <= hb) & ~(F | d2 | sperr_d1)
            Wc = np.full(GB.shape, float(s["spiegel_m"])); eps = s.get("eps_m", 0.03)
            if s.get("spiegel_start_aus_oberlauf"):
                # L3j: Spiegel je Spalte stetig vom Oberlauf (Zeile vor z0, naechster Wasser-Vertex) auf spiegel_m (bei z1)
                j0 = int(round(s["z0"] * rs)) - 1; xw = np.flatnonzero(ok[j0]); xw = xw[np.abs(xw / rs - np.nanmean(cxs[j0:j0 + 2])) < 4]
                wup = np.interp(np.arange(GX), xw, WVn[j0, xw].astype(float))
                Wc = wup[None, :] + (float(s["spiegel_m"]) - wup[None, :]) * fz
            neu = kan & ~ok; WVn[neu] = Wc[neu]; alt = kan & ok & (WVn < Wc - 1e-6); WVHOCH |= alt; WVn[alt] = Wc[alt]
            t_k = s.get("tiefe_start_m", s["tiefe_m"]) + (s["tiefe_m"] - s.get("tiefe_start_m", s["tiefe_m"])) * fz; t_r = s.get("rand_tiefe_m", 0.08); rz = s.get("randzone_zellen", 1.0)
            tief = t_r + (t_k - t_r) * L3._ss((hb - dx) / rz)
            G = GBn.copy(); G[kan] = np.minimum(GBn[kan], Wc[kan] - tief[kan]) if s.get("nur_absenken") else Wc[kan] - tief[kan]
            # Land neben dem Kanal: Abstand zur Kanalkante (Zellen), Profil
            band = s.get("band_zellen", 3.0); dl = dx - hb
            zf = 1.0 - L3._ss((np.maximum(s["z0"] - zz, zz - s["z1"]) ) / max(band, 1e-6))   # 1 im Kanalbereich, faellt ueber band Zellen ab
            land = (zf > 1e-3) & ~kan & (dl <= band) & ~(WVn > -900) & ~(F | d2 | sperr_d1)
            prof = Wc + s.get("rand_hoehe_m", 0.04) + s.get("neigung_m_je_zelle", 0.35) * np.maximum(dl, 0)
            wl = (1.0 - L3._ss((dl - band * 0.5) / (band * 0.5))) * zf
            Gl = np.where(G > prof, G + wl * (prof - G), G); Gl = np.maximum(Gl, Wc + eps)
            G[land] = Gl[land]
            # Enden weich: Gewicht ueber z (fade_z Zellen ausserhalb z0..z1 nichts, innerhalb voll)
            d = np.abs(G - GBn); GBn = G; A = np.maximum(A, (kan | land).astype(float))
            Vf = VCn.astype(float)
            tk, tr = np.asarray(s["ton_kern"], float), np.asarray(s["ton_rand"], float)
            ww = L3._ss((hb - dx) / rz)[..., None]; Vk = tr + (tk - tr) * ww
            Vf[kan] = Vk[kan]
            Vg = np.stack([nd.gaussian_filter(Vf[..., k], s.get("vc_sigma", 1.5)) for k in range(3)], -1)
            wb = np.where(land, wl, 0.0)[..., None]; Vf = Vf + wb * (Vg - Vf)
            VCn = np.clip(np.round(Vf), 0, 255).astype(np.uint8)
            bericht.append({"id": s["id"], "neue_wasser_vertices": int(neu.sum()), "wv_angehoben": int(alt.sum()), "kanal_vertices": int(kan.sum()),
                            "land_band_vertices": int(land.sum()), "gb_max_m": round(float(d.max()), 3),
                            "mittellinie_x": [round(float(np.nanmin(cxs[zin[:, 0]])), 2), round(float(np.nanmax(cxs[zin[:, 0]])), 2)]})
        if s["art"] == "wasser_zu_schnee":
            # L3i (2): isolierte Wasserkomponenten (ueber der Schneegrenze, ohne Bach) -> Land. Nur die Komponenten, die einen der Punkte enthalten.
            # GB im Gebiet (Komponente + Ring) harmonisch aus dem Rand aufgefuellt (Laplace), dann weich geglaettet; VC ebenso aus dem Rand (Schnee).
            ok = WVn > -900; lab, n = nd.label(ok, np.ones((3, 3))); sel = np.zeros(GB.shape, bool); ks = []
            for px, pz in s["punkte"]:
                j, i = int(round(pz * rs)), int(round(px * rs)); r = 3
                ll = np.unique(lab[max(j - r, 0):j + r + 1, max(i - r, 0):i + r + 1]); ll = ll[ll > 0]
                for l in ll:
                    m_ = lab == l
                    if m_.sum() > s.get("max_vertices", 60): sys.exit(f"wasser_zu_schnee: Komponente {int(l)} zu gross ({int(m_.sum())}) - Abbruch")
                    sel |= m_; ks.append(int(m_.sum()))
            if (sel & (F | d2 | sperr_d1)).any(): sys.exit("wasser_zu_schnee in fester Flaeche/Sperrzone - Abbruch")
            reg = nd.binary_dilation(sel, np.ones((3, 3)), iterations=s.get("ring_vertices", 2)) & ~(F | d2 | sperr_d1) & ~(ok & ~sel)
            G = GBn.copy(); Vf = VCn.astype(float)
            rand = nd.binary_dilation(reg, np.ones((3, 3))) & ~reg
            G[reg] = G[rand].mean(); 
            for k in range(3): Vf[..., k][reg] = Vf[..., k][rand].mean()
            for _ in range(s.get("laplace_runden", 400)):
                Gm = (np.roll(G, 1, 0) + np.roll(G, -1, 0) + np.roll(G, 1, 1) + np.roll(G, -1, 1)) / 4.0; G[reg] = Gm[reg]
                for k in range(3):
                    V = Vf[..., k]; Vm = (np.roll(V, 1, 0) + np.roll(V, -1, 0) + np.roll(V, 1, 1) + np.roll(V, -1, 1)) / 4.0; V[reg] = Vm[reg]
            wz = np.minimum(1.0, nd.gaussian_filter(reg.astype(float), s.get("blend_sigma_vertices", 1.0)) * s.get("blend_verstaerkung", 1.0)); wz[F | d2 | sperr_d1] = 0.0; wz[ok & ~sel] = 0.0
            Gs = nd.gaussian_filter(G, s.get("sigma_vertices", 1.0)); G = G + wz * (Gs - G)
            d = np.abs(G - GBn); GBn = G; A = np.maximum(A, (wz > 1e-3).astype(float))
            WVn[sel] = -999.0; WEG |= sel
            VCn = np.where((wz > 1e-3)[..., None] | reg[..., None], np.clip(np.round(Vf), 0, 255), VCn).astype(np.uint8)
            bericht.append({"id": s["id"], "komponenten_vertices": ks, "wasser_entfernt": int(sel.sum()), "gebiet_vertices": int(reg.sum()),
                            "gb_vertices": int((d > 1e-5).sum()), "gb_max_m": round(float(d.max()), 3)})
        if s["art"] == "laengs_glatt":
            # L3k: Kerbe an der Kachelnaht - GB laengs einer Achse (achse 0 = z, 1 = x) Gauss-glaetten, im Kreis um den Punkt weich eingeblendet.
            ok = WVn > -900; px, pz = s["punkt"]; dist = np.hypot(xx - px, zz - pz)
            if s.get("halblaenge", 0) > 0 and "richtung" in s:
                # Gebiet als Stadion entlang der Gratrichtung: Kern = Strecke +-halblaenge um den Punkt, Radius r_kern
                ux, uz = np.asarray(s["richtung"], float) / np.hypot(*s["richtung"]); al = (xx - px) * ux + (zz - pz) * uz
                dist = np.hypot(np.maximum(np.abs(al) - s["halblaenge"], 0.0), (xx - px) * uz - (zz - pz) * ux)
            w = 1.0 - L3._ss((dist - s.get("r_kern", 2.5)) / s.get("r_fade", 2.0))
            if (ok & (w > 0)).any(): sys.exit("laengs_glatt: Wasser im Gebiet - Abbruch")
            if s.get("waende_frei", True):
                V = json.loads((R / "neu" / "vektor.json").read_text(encoding="utf-8")); nxz = int(D["nx"]); wz_ = np.zeros(GB.shape, bool)
                q = np.unique(np.concatenate([np.asarray(t["quellzellen"], int) for t in V["waende"]]))
                for c in q[(np.abs(q % nxz - px) < 12) & (np.abs(q // nxz - pz) < 12)]:
                    cz, cx = int(c // nxz), int(c % nxz); wz_[cz * rs:cz * rs + rs + 1, cx * rs:cx * rs + rs + 1] = True
                w *= L3._ss((nd.distance_transform_edt(~wz_) - s.get("wand_abstand_vertices", 1.0)) / s.get("wand_fade_vertices", 1.0))
            if "nur_ueber_m" in s:
                # Hangfuss (Basis unter der Schwelle) bleibt, weich ueber 1 m eingeblendet - die Fusskante laeuft unveraendert durch
                w *= L3._ss((GBn - s["nur_ueber_m"]) / 1.0)
            w[F | d2 | sperr_d1] = 0.0
            G = GBn.copy()
            sig = s.get("sigma_vertices", 3.0)
            if "richtung" in s:
                # Glaettung entlang der Gratrichtung (dx, dz in Zellen): Gauss-Mittel der Hoehen auf der Linie durch jeden Vertex
                tx, tz = np.asarray(s["richtung"], float) / np.hypot(*s["richtung"]); K = int(np.ceil(3 * sig)); ks = np.arange(-K, K + 1)
                gk = np.exp(-0.5 * (ks / sig) ** 2); gk /= gk.sum(); vz, vx = np.mgrid[0:GY, 0:GX].astype(float)
                def glatt(H):
                    return sum(g * nd.map_coordinates(H, [vz + k * tz, vx + k * tx], order=1, mode="nearest") for g, k in zip(gk, ks))
            else:
                def glatt(H): return nd.gaussian_filter1d(H, sig, axis=s.get("achse", 0))
            for _ in range(s.get("runden", 2)): G = G + w * (glatt(G) - G)
            if "nicht_senken_ueber_m" in s:
                # Gratkrone/Plateau (Basis ueber der Schwelle) wird nur gehoben, nie gesenkt - sonst entstuende eine neue Delle in der Krone
                hoch = GBn > s["nicht_senken_ueber_m"]; G[hoch] = np.maximum(G[hoch], GBn[hoch])
            d = np.abs(G - GBn); GBn = G; A = np.maximum(A, (d > s.get("feinband_ab_m", -1.0)) * (w > 1e-3) * s.get("feinband", 1.0))
            bericht.append({"id": s["id"], "gb_vertices": int((d > 1e-5).sum()), "gb_max_m": round(float(d.max()), 3)})
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
    if (m0 & ~m1 & ~WEG).any(): sys.exit("Wasser ausserhalb wasser_zu_schnee entfernt - Abbruch")
    if (GBn[m1] >= WVn[m1]).sum() > (GB[m0 & ~WEG] >= WV[m0 & ~WEG]).sum(): sys.exit("mehr Bett ueber dem Spiegel als vorher - Abbruch")
    wv_ge = WVn != WV; vc_ge = (VCn != VC).any(-1)
    if (wv_ge & ~(m1 & ~m0) & ~RING & ~WEG & ~WVHOCH).any(): sys.exit("WV auf altem Wasser ausserhalb wv_ring/kanal geaendert - Abbruch")
    if (WVHOCH & (WVn < WV)).any(): sys.exit("kanal hat WV gesenkt - Abbruch")
    lmk = nd.minimum_filter(np.where(m1, 1e9, GBn.astype(np.float64)), size=3)
    if ((WVHOCH | (m1 & ~m0)) & (WVn >= lmk)).any(): sys.exit("Kanal-Spiegel ueber benachbartem Gelaende - Abbruch")
    if (RING & (WVn < WV)).any(): sys.exit("wv_ring hat WV gesenkt - Abbruch")
    lm = nd.minimum_filter(np.where(m1, 1e9, GBn.astype(np.float64)), size=3)
    if (RING & (WVn >= lm)).any(): sys.exit("wv_ring ueber benachbartem Gelaende - Abbruch")
    if ((wv_ge | vc_ge) & (F | d2)).any(): sys.exit("feste Flaeche/D2 beruehrt - Abbruch")
    if ((wv_ge | vc_ge | gb_ge) & sperr_d1).any(): sys.exit("Sperrzone D1/D4/D5/Mulde beruehrt - Abbruch")
    lab0, n0 = nd.label(m0, np.ones((3, 3))); lab1, n1 = nd.label(m1, np.ones((3, 3)))
    loch = nd.binary_fill_holes(m1) & ~m1 & ~(nd.binary_fill_holes(m0) & ~m0) & ~WEG
    if loch.any(): sys.exit(f"neue eingeschlossene Landinseln: {int(loch.sum())} - Abbruch")
    nweg = len(np.unique(lab0[WEG])) if WEG.any() else 0
    if n1 != n0 - nweg: sys.exit(f"Wasserkomponenten {n0} -> {n1} (erwartet {n0 - nweg}) - Abbruch")
    info = {"stellen": bericht, "wasser_neu": int((m1 & ~m0).sum()), "wasser_entfernt": int(WEG.sum()), "wasser_entfernt_komponenten": int(nweg), "wv_kanal_angehoben": int(WVHOCH.sum()), "wasser_komponenten": [int(n0), int(n1)],
            "bett_ueber_spiegel": [int((GB[m0 & ~WEG] >= WV[m0 & ~WEG]).sum()), int((GBn[m1] >= WVn[m1]).sum())],
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

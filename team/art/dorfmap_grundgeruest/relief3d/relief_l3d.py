#!/usr/bin/env python3
"""L3d (16.11.2026): zwei Restbefunde aus P12b (weicher Wasserrand), die im Renderer nicht loesbar sind.
Abschaltbarer Nachschritt NACH L3c2 (bau_endstand.sh Schritt 12), eigener Basis-Hash und Rueckweg.
  python3 relief_l3d.py            anwenden (nur wenn GB/WV/VC dem Stand nach L3c2 entsprechen)
  python3 relief_l3d.py --trocken  nur rechnen und berichten
  python3 relief_l3d.py --aus      rueckgaengig (pruefung/l3d/l3d_rueck.npz)
Stelle E3_west (Farbe): Die Zickzacklinie am Bach E3 steckt in der Gelaendefarbe VC (dunkles Bachband folgt dem
  0,5-Zellen-Raster der Maske). Das Farbprofil quer zum Bach wird auf einen geglaetteten Abstand zur Bachmaske gelegt:
  VC_neu = P(sd_glatt) + glatt(VC - P(sd)), P = mittleres VC je Abstandsklasse im Ausschnitt. Nur VC und FW.c, lokal.
  Zusatz (rinne): Die eigentliche Zickzacklinie ist die Rinnenwand im GB (Stufe bis 0,7 m genau auf dem Maskenraster,
  dunkle Schattierung, auch im Ton-Bild ohne Wasser). GB = Basis (Land harmonisch) + Rinnenprofil(sd_glatt) + glatter Rest.
Stelle G7_nord (Wassermaske): Am Nordufer westlich x~265 endet die Maske WV>-900 vor dem Ufer (Gelaende liegt dort
  noch unter dem Spiegel). Die Maske waechst vom bestehenden Fluss aus in genau diese Vertices (Gelaende < Spiegel des
  Nachbarwassers, Wasser liegt suedlich/oestlich = Nordufer) bzw. bis 0,25 m darueber, WV = Mittel der Wassernachbarn (Spiegel flach fortgesetzt). Die
  Maskentreppe liegt dann unter dem Gelaende, sichtbar ist die glatte Schnittlinie Spiegel/Gelaende. Kein Wasser entfernt,
  GB dort unveraendert, keine neuen Inseln/Loecher (fill_holes-Pruefung), Zusammenhang erhalten.
Fest: D2 (Abbruch bei Aenderung), Wege/Kreuzungen/Rampenkerne/WEGA (relief_l3.feste_flaechen, richtiger Massstab): 0 Vertices.
"""
import base64, gzip, hashlib, json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage as nd
R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import relief_l3 as L3
CFG = R / "pruefung" / "l3d" / "l3d_stellen.json"
RUECK = R / "pruefung" / "l3d" / "l3d_rueck.npz"
BERICHT = R / "pruefung" / "l3d" / "l3d_bericht.json"
QUELLE, NEU = R / "relief_daten.json.gz", R / "neu" / "relief_neu.json.gz"

def _arr(D, k, dt, sh): return np.frombuffer(base64.b64decode(D[k]), dt).reshape(sh).copy()
def _b64(a): return base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()
def _sha(*a): h = hashlib.sha256(); [h.update(np.ascontiguousarray(x).tobytes()) for x in a]; return h.hexdigest()

def box_gewicht(b, GY, GX, rs):
    x = np.arange(GX)[None, :] / rs; z = np.arange(GY)[:, None] / rs; f = b.get("fade_m", 2.0)
    dx = np.maximum(np.maximum(b["x0"] - x, x - b["x1"]), 0); dz = np.maximum(np.maximum(b["z0"] - z, z - b["z1"]), 0)
    return 1.0 - L3._ss(np.hypot(dx, dz) / f)

def g7_maske(GB, WV, s, rs, F):
    GY, GX = GB.shape; m = WV > -900; wv = WV.astype(np.float64).copy()
    bx = box_gewicht(s, GY, GX, rs) > 0.999
    neu = np.zeros_like(m)
    for it in range(s.get("schritte", 8)):
        mm = m | neu
        nb = nd.convolve(mm.astype(float), np.ones((3, 3)), mode="constant")
        sw = nd.convolve(np.where(mm, wv, 0.0), np.ones((3, 3)), mode="constant")
        lvl = np.where(nb > 0, sw / np.maximum(nb, 1), -1e9)
        # Richtung zum Wasser: Wasser suedlich/oestlich (Nordwestufer) -> Schwerpunkt der Wassernachbarn
        dz = nd.correlate(mm.astype(float), np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], float), mode="constant")
        dx = nd.correlate(mm.astype(float), np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], float), mode="constant")
        kand = (~mm) & bx & ~F & (nb > 0) & (GB < lvl + s.get("ueber_spiegel_m", 0.0)) & ((dz > 0) | (dx > 0))
        if not kand.any(): break
        wv[kand] = lvl[kand]; neu |= kand
    return neu, wv

def e3_farbe(VC, WV, s, rs):
    GY, GX = WV.shape; m = WV > -900
    w = box_gewicht(s, GY, GX, rs)
    sd = nd.distance_transform_edt(~m) - nd.distance_transform_edt(m)   # Vertices, >0 an Land
    sdg = nd.gaussian_filter(sd, s.get("sigma_vertices", 2.0))
    band = s.get("band_vertices", 7.0)
    sel = (w > 0.999) & (np.abs(sd) <= band + 2)
    bins = np.arange(-band - 2, band + 3, 1.0)
    V = VC.astype(np.float64); P = np.zeros((len(bins), 3))
    for i, b in enumerate(bins):
        q = sel & (np.abs(sd - b) <= 0.5)
        P[i] = V[q].mean(0) if q.any() else np.nan
    ok = ~np.isnan(P[:, 0]); P = np.stack([np.interp(bins, bins[ok], P[ok, c]) for c in range(3)], 1)
    prof = lambda t: np.stack([np.interp(np.clip(t, bins[0], bins[-1]), bins, P[:, c]) for c in range(3)], -1)
    res = V - prof(sd)
    resg = np.stack([nd.gaussian_filter(res[..., c], s.get("rest_sigma_vertices", 2.5)) for c in range(3)], -1)
    neu = prof(sdg) + resg
    a = w * (1.0 - L3._ss((np.abs(sd) - band) / 2.0))
    out = V * (1 - a[..., None]) + neu * a[..., None]
    return np.clip(np.rint(out), 0, 255).astype(np.uint8), a

def harmonisch(H, frei, it=400):
    E = H.copy(); E[frei] = H[~frei].mean() if (~frei).any() else 0.0
    for _ in range(it):
        A = 0.25 * (np.roll(E, 1, 0) + np.roll(E, -1, 0) + np.roll(E, 1, 1) + np.roll(E, -1, 1)); E[frei] = A[frei]
    return E

def e3_rinne(GB, WV, s, rs):
    """Bachrinne quer glaetten: GB = Basis (Landflaeche harmonisch ueber den Bach) + Rinne(sd_glatt) + glatter Rest.
    Die Rinnenwand folgte bisher dem Maskenraster (Stufe bis 0,7 m) -> dunkle Zickzack-Schattierung."""
    GY, GX = GB.shape; m = WV > -900; w = box_gewicht(s, GY, GX, rs)
    sd = nd.distance_transform_edt(~m) - nd.distance_transform_edt(m)
    band = s.get("rinne_band_vertices", 4.0)
    zs, xs = np.where(w > 0); pad = 12
    sl = (slice(max(zs.min() - pad, 0), zs.max() + pad + 1), slice(max(xs.min() - pad, 0), xs.max() + pad + 1))
    H = GB[sl].astype(np.float64); frei = (sd[sl] <= band) & (w[sl] > 0)
    base = harmonisch(H, frei)
    g = H - base; sds = sd[sl]; sdg = nd.gaussian_filter(sd, s.get("sigma_vertices", 2.0))[sl]
    bins = np.arange(-8, band + 3, 1.0); P = np.full(len(bins), np.nan); sel = (w[sl] > 0.999)
    for i, b in enumerate(bins):
        q = sel & (np.abs(sds - b) <= 0.5)
        if q.any(): P[i] = np.median(g[q])
    ok = ~np.isnan(P); P = np.interp(bins, bins[ok], P[ok]); P[bins >= band] = 0.0
    prof = lambda t: np.interp(np.clip(t, bins[0], bins[-1]), bins, P)
    rest = nd.gaussian_filter(g - prof(sds), s.get("rest_sigma_vertices", 2.5))
    neu = base + prof(sdg) + rest
    a = w[sl] * (1.0 - L3._ss((sds - band) / 2.0)) * (1.0 - L3._ss((-sds - 8.0) / 2.0))
    out = GB.astype(np.float64).copy(); out[sl] = H * (1 - a) + neu * a
    # Wasser-/Landgrenze halten: Bett bleibt unter dem Spiegel, Land faellt nicht unter den naechsten Spiegel
    G0 = GB.astype(np.float64); W = WV.astype(np.float64)
    _, (iz, ix) = nd.distance_transform_edt(~m, return_indices=True); Wn = W[iz, ix]
    out[m] = np.minimum(out[m], G0[m])   # Bett nie anheben (sonst wird der Bach flach und verschwindet im Viewer)
    land = ~m
    def klemmen(o):
        o[m] = np.minimum(o[m], G0[m]); o[land] = np.maximum(o[land], np.minimum(G0[land], Wn[land] + s.get("land_ueber_m", 0.05))); return o
    out = klemmen(out)
    for _ in range(int(s.get("nachglatt_runden", 0))):   # Klemmkanten (Spitzen/Facetten) im Rinnenband nachglaetten, danach wieder klemmen
        g2 = nd.gaussian_filter(out[sl], s.get("nachglatt_sigma", 1.0)); out[sl] = out[sl] * (1 - a) + g2 * a; out = klemmen(out)
    return out

def fw_c_aus_vc(D, VCn, ge):
    FW = D["FW"]; FS = int(FW["fs"]); FX = D["nx"] * FS + 1; GY, GX = VCn.shape[:2]
    vid = np.frombuffer(base64.b64decode(FW["vid"]), np.uint32).astype(np.int64)
    gz = (vid // FX) / FS * 2; gx = (vid % FX) / FS * 2
    z0 = np.clip(np.floor(gz).astype(int), 0, GY - 2); x0 = np.clip(np.floor(gx).astype(int), 0, GX - 2); tz = gz - z0; tx = gx - x0
    near = ge[z0, x0] | ge[z0 + 1, x0] | ge[z0, x0 + 1] | ge[z0 + 1, x0 + 1]
    c = np.frombuffer(base64.b64decode(FW["c"]), np.uint8).reshape(-1, 3).copy(); V = VCn.astype(float)
    bil = (V[z0, x0] * ((1 - tz) * (1 - tx))[:, None] + V[z0 + 1, x0] * (tz * (1 - tx))[:, None] + V[z0, x0 + 1] * ((1 - tz) * tx)[:, None] + V[z0 + 1, x0 + 1] * (tz * tx)[:, None])
    idx = np.flatnonzero(near); alt = c[idx].copy(); c[idx] = np.clip(np.rint(bil[idx]), 0, 255).astype(np.uint8)
    return c, idx, alt

def main():
    arg = sys.argv[1:]; cfg = json.loads(CFG.read_text(encoding="utf-8"))
    D = json.load(gzip.open(QUELLE)); N = json.load(gzip.open(NEU)); rs = D["rs"]; GY, GX = D["ny"] * rs + 1, D["nx"] * rs + 1
    GB = _arr(D, "GB", np.float32, (GY, GX)); WV = _arr(D, "WV", np.float32, (GY, GX)); VC = _arr(D, "VC", np.uint8, (GY, GX, 3))
    if "--aus" in arg:
        if not RUECK.exists(): print("L3d nicht aktiv"); return
        r = np.load(RUECK)
        Gf = GB.reshape(-1).copy(); Gf[r["gb_idx"]] = r["gb_alt"]; Gn = Gf.reshape(GY, GX); delta = Gn.astype(np.float64) - GB
        Wf = WV.reshape(-1); Wf[r["wv_idx"]] = r["wv_alt"]; Vf = VC.reshape(-1, 3); Vf[r["vc_idx"]] = r["vc_alt"]
        for X in (D, N):
            X["WV"] = _b64(Wf); X["VC"] = _b64(Vf); X["GB"] = _b64(Gn); L3.objekte(X, delta, rs)
            c = np.frombuffer(base64.b64decode(X["FW"]["c"]), np.uint8).reshape(-1, 3).copy(); c[r["fc_idx"]] = r["fc_alt"]; X["FW"]["c"] = _b64(c)
        L3.prototypen(N, Gn, Gn != GB)
        L3._schreibe(D, QUELLE, False); L3._schreibe(N, NEU, True); RUECK.unlink(); print(json.dumps({"l3d": "aus"})); return
    if RUECK.exists(): sys.exit("L3d schon aktiv")
    if _sha(GB, WV, VC) != cfg["basis_gb_wv_vc_sha256"]: sys.exit(f"Basis passt nicht ({_sha(GB, WV, VC)[:12]}); Reihenfolge pruefen")
    if D["VC"] != N["VC"] or D["WV"] != N["WV"] or D["FW"]["c"] != N["FW"]["c"]: sys.exit("relief_daten/relief_neu ungleich (VC/WV/FW.c)")
    F = L3.feste_flaechen(D, GY, GX, rs)
    x0, z0, x1, z1 = L3.D2_BOX; d2 = np.zeros((GY, GX), bool); d2[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1] = True
    WVn = WV.astype(np.float64).copy(); VCn = VC.copy(); GBn = GB.astype(np.float64).copy(); bericht = []
    for s in cfg["stellen"]:
        if not s.get("aktiv", True): bericht.append({"id": s["id"], "aktiv": False}); continue
        if s["art"] == "wassermaske":
            neu, wv = g7_maske(GBn.astype(np.float32), np.where(WVn > -900, WVn, -999.0).astype(np.float32), s, rs, F | d2)
            WVn[neu] = wv[neu]; bericht.append({"id": s["id"], "neue_wasser_vertices": int(neu.sum()), "wv_min": round(float(wv[neu].min()), 3) if neu.any() else None,
                                                "gb_unter_spiegel_max_m": round(float((wv - GB)[neu].max()), 3) if neu.any() else None})
        elif s["art"] == "farbe":
            Vn, a = e3_farbe(VCn, WV, s, rs); a[F | d2] = 0; Vn[(F | d2)] = VCn[(F | d2)]
            ge = (Vn != VCn).any(-1); VCn = Vn
            if s.get("rinne", False):
                Gn = e3_rinne(GBn, WV, s, rs); Gn[F | d2] = GBn[F | d2]; GBn = Gn
            bericht.append({"id": s["id"], "vc_vertices": int(ge.sum()), "vc_max_aenderung": int(np.abs(Vn.astype(int) - VC.astype(int)).max())})
    WVn = WVn.astype(np.float32); GBn = GBn.astype(np.float32); gb_ge = GBn != GB
    if (gb_ge & (F | d2)).any(): sys.exit("GB auf fester Flaeche/D2 geaendert - Abbruch")
    mw = WV > -900
    if (GBn[mw] >= WVn[mw]).sum() > (GB[mw] >= WV[mw]).sum(): sys.exit("Bachbett ueber den Spiegel gehoben - Abbruch")
    m0, m1 = WV > -900, WVn > -900
    if (m0 & ~m1).any(): sys.exit("Wasser entfernt - Abbruch")
    wv_ge = WVn != WV; vc_ge = (VCn != VC).any(-1)
    if (wv_ge & ~(m1 & ~m0)).any(): sys.exit("WV auf altem Wasser geaendert - Abbruch")
    if ((wv_ge | vc_ge) & (F | d2)).any(): sys.exit("feste Flaeche/D2 beruehrt - Abbruch")
    lab0, n0 = nd.label(m0, np.ones((3, 3))); lab1, n1 = nd.label(m1, np.ones((3, 3)))
    loch = nd.binary_fill_holes(m1) & ~m1 & ~(nd.binary_fill_holes(m0) & ~m0)
    if loch.any(): sys.exit(f"neue eingeschlossene Landinseln: {int(loch.sum())} - Abbruch")
    info = {"stellen": bericht, "wasser_neu": int((m1 & ~m0).sum()), "wasser_entfernt": 0, "wasser_komponenten": [int(n0), int(n1)],
            "fill_holes_neu_nur_neue_vertices": bool(((nd.binary_fill_holes(m1) ^ nd.binary_fill_holes(m0)) == (m1 & ~m0)).all()),
            "vc_vertices": int(vc_ge.sum()), "gb_vertices": int(gb_ge.sum()), "gb_max_abs_m": round(float(np.abs(GBn.astype(float) - GB).max()), 3), "basis": cfg["basis_gb_wv_vc_sha256"], "nachher_sha256": _sha(GBn, WVn, VCn)}
    c, fidx, falt = fw_c_aus_vc(D, VCn, vc_ge); info["fw_c_punkte"] = int(fidx.size)
    if "--trocken" in arg: print(json.dumps(info, indent=1)); return
    widx = np.flatnonzero(wv_ge.reshape(-1)); vidx = np.flatnonzero(vc_ge.reshape(-1)); gidx = np.flatnonzero(gb_ge.reshape(-1))
    np.savez_compressed(RUECK, gb_idx=gidx, gb_alt=GB.reshape(-1)[gidx], wv_idx=widx, wv_alt=WV.reshape(-1)[widx], vc_idx=vidx, vc_alt=VC.reshape(-1, 3)[vidx], fc_idx=fidx, fc_alt=falt)
    for X in (D, N): X["WV"] = _b64(WVn); X["VC"] = _b64(VCn); X["FW"]["c"] = _b64(c); X["GB"] = _b64(GBn)
    delta = GBn.astype(np.float64) - GB.astype(np.float64)
    info["objekte_angepasst"] = L3.objekte(D, delta, rs); L3.objekte(N, delta, rs)
    info["prototypen"] = L3.prototypen(N, GBn, gb_ge)
    L3._schreibe(D, QUELLE, False); L3._schreibe(N, NEU, True)
    BERICHT.write_text(json.dumps(info, indent=1, ensure_ascii=False), encoding="utf-8"); print(json.dumps(info, indent=1))

if __name__ == "__main__":
    main()

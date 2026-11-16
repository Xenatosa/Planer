#!/usr/bin/env python3
"""L3 (16.11.2026): lokale Ersatzstuecke mit einfacher Geometrie fuer die sichtbaren QA-P4b-Stellen.

Abschaltbarer Nachschritt auf dem sichtbaren Hoehenfeld GB (relief_daten.json.gz + neu/relief_neu.json.gz).
  python3 relief_l3.py            -> anwenden (nur wenn GB noch der L3-Basis entspricht)
  python3 relief_l3.py --aus      -> rueckgaengig (Originalwerte aus pruefung/l3_rueck.npz)
  python3 relief_l3.py --trocken  -> nur rechnen und berichten, nichts schreiben
Stellenliste: pruefung/l3_stellen.json. Je Stelle Ellipse (x_m, z_m, rx_m, rz_m, Drehung) mit flachem Kern
und weichem Auslauf (fade_m, Standard 3,5 m = 3-5 Zellen). Ersatzform je Stelle (verfahren):
  oeffnen_m   : graue Oeffnung (entfernt duenne Grate, Zaehne, Splitter, Wuelste nach oben)
  schliessen_m: graue Schliessung (fuellt Kerben, Trichter, Rillen nach unten)
  sigma_m     : Gauss-Glaettung danach (glatter Hang / runde Ober- und Unterkante, kein 0,5-m-Zickzack)
  stufe       : "ebene" -> Kern auf Median des Kerns ziehen (ebene Stufe)
Fest bleiben: Wasser (+1,5 m), Wege/Wegflaechen/Kreuzungen/Bruecken (+1,5 m), Kachel D2 komplett (+3 m Fade).
G (Quellfeld) bleibt bytegleich. D1/G1 (Prototyp-Kacheln) werden mit neu.mesh.tile_mesh aus dem neuen GB
neu vermascht; Objekt-Hoehen (baeume, steine, geroell, findlinge) folgen der Hoehenaenderung.
"""
from __future__ import annotations
import base64, gzip, hashlib, json, os, sys
from pathlib import Path
import numpy as np
from scipy import ndimage as nd

R = Path(__file__).resolve().parent
STELLEN = R / "pruefung" / "l3_stellen.json"
RUECK = R / "pruefung" / "l3_rueck.npz"
QUELLE = R / "relief_daten.json.gz"
NEU = R / "neu" / "relief_neu.json.gz"
D2_BOX = (126, 43, 168, 86)


def _sha(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def _ss(t): t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)


def _schreibe(D, pfad, kompakt):
    js = json.dumps(D, ensure_ascii=False, separators=(",", ":")) if kompakt else json.dumps(D, ensure_ascii=False)
    pfad.write_bytes(gzip.compress(js.encode("utf-8"), 9, mtime=0))


def schutz(D, GY, GX, rs, weg_abstand_m=1.5, mit_wasser=True, weg_rand_m=0.5, rampe_m=2.0):
    """Gewicht 0 auf festen Flaechen, weicher Anstieg auf 1 daneben (Wege: Abstand weg_abstand_m, Wasser 1,5 m)."""
    fest = np.zeros((GY, GX), bool)
    WV = np.frombuffer(base64.b64decode(D["WV"]), np.float32).reshape(GY, GX)
    wasser = WV > -900
    WEGA = np.frombuffer(base64.b64decode(D["WEGA"]), np.uint8).reshape(GY, GX)
    weg = WEGA > 0
    for x, z in D["wege"]:
        weg[z * rs:z * rs + rs + 1, x * rs:x * rs + rs + 1] = True
    for b in D.get("bruecken", []):
        weg[int(round(b[2] * rs)), int(round(b[0] * rs))] = True
    rampe = np.zeros((GY, GX), bool)
    for p in D.get("rampenwege", []):   # Rampen sind Wege: Mittellinie dicht abtasten, Rampenkern 1,8 m (gen_relief kern rr<=1.8) + 0,2 m Rand fest
        P = np.asarray(p, float)
        if len(P) < 2: continue
        L = np.r_[0.0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]; t = np.arange(0.0, L[-1] + 1e-9, 0.25)
        x = np.interp(t, L, P[:, 0]); z = np.interp(t, L, P[:, 1])
        rampe[np.clip(np.rint(z * rs).astype(int), 0, GY - 1), np.clip(np.rint(x * rs).astype(int), 0, GX - 1)] = True
    weg |= nd.distance_transform_edt(~rampe, sampling=1.0 / rs) <= rampe_m   # L3b: rampe_m=5 schuetzt auch die Boeschung (1,8-5 m)
    # Wegnetz aus neu/vektor.json (Gassen, Anbindungen, Hauswege): halbe Breite + 0,5 m fest; Kreuzungsflaechen + Uebergang fest
    V = json.loads((R / "neu" / "vektor.json").read_text(encoding="utf-8"))
    for wv in V.get("wege", []):
        P = np.asarray(wv["mittellinie_m"], float)
        if len(P) < 2: continue
        L = np.r_[0.0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]; t = np.arange(0.0, L[-1] + 1e-9, 0.25)
        lin = np.zeros((GY, GX), bool)
        lin[np.clip(np.rint(np.interp(t, L, P[:, 1]) * rs).astype(int), 0, GY - 1), np.clip(np.rint(np.interp(t, L, P[:, 0]) * rs).astype(int), 0, GX - 1)] = True
        zs, xs = np.where(lin); pad = int((wv["breite_m"] / 2 + max(1.0, weg_rand_m + 0.5)) * rs) + 1
        sl = (slice(max(zs.min() - pad, 0), zs.max() + pad + 1), slice(max(xs.min() - pad, 0), xs.max() + pad + 1))
        weg[sl] |= nd.distance_transform_edt(~lin[sl], sampling=1.0 / rs) <= wv["breite_m"] / 2 + weg_rand_m
    from matplotlib.path import Path as _MP
    zz, xx = np.mgrid[0:GY, 0:GX] / float(rs); pts = np.c_[xx.ravel(), zz.ravel()]
    for k in V.get("kreuzungen", []):
        weg |= _MP(k["polygon_m"]).contains_points(pts, radius=float(k.get("uebergang_m", 0.0)) + 0.5).reshape(GY, GX) | \
               _MP(k["polygon_m"]).contains_points(pts, radius=-(float(k.get("uebergang_m", 0.0)) + 0.5)).reshape(GY, GX)
    dw = nd.distance_transform_edt(~wasser, sampling=1.0 / rs)
    dr = nd.distance_transform_edt(~weg, sampling=1.0 / rs)
    w = _ss((dw - 1.5) / 1.5) if mit_wasser else np.ones((GY, GX))   # Wasser: 0 bis 1,5 m Abstand, voll ab 3 m (L3b: Wasserstellen ohne)
    if weg_abstand_m >= 1.5:
        w *= _ss((dr - 1.5) / 1.5)         # Wege Standard wie Wasser
    else:
        w *= _ss((dr - weg_abstand_m) / 1.0)   # enger Wegabstand (Boeschung direkt am Weg), Wegvertices bleiben fest
    w[weg | (wasser if mit_wasser else False)] = 0.0
    d2 = np.zeros((GY, GX), bool); x0, z0, x1, z1 = D2_BOX
    d2[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1] = True
    dd2 = nd.distance_transform_edt(~d2, sampling=1.0 / rs)
    w *= _ss((dd2 - 0.5) / 3.0)
    w[d2] = 0.0
    return w


def gewicht(s, GY, GX, rs):
    x = np.arange(GX)[None, :] / rs - s["x_m"]; z = np.arange(GY)[:, None] / rs - s["z_m"]
    a = np.radians(s.get("drehung_grad", 0.0)); u = x * np.cos(a) + z * np.sin(a); v = -x * np.sin(a) + z * np.cos(a)
    n = np.sqrt((u / s["rx_m"]) ** 2 + (v / s["rz_m"]) ** 2)
    phys = np.minimum(s["rx_m"], s["rz_m"]) * np.maximum(n - 1.0, 0)
    return 1.0 - _ss(phys / s.get("fade_m", 3.5))


def ersatz(H, s, rs):
    E = H.copy()
    if s.get("oeffnen_m"):
        k = max(3, int(round(s["oeffnen_m"] * rs)) | 1); E = nd.grey_opening(E, size=(k, k))
    if s.get("schliessen_m"):
        k = max(3, int(round(s["schliessen_m"] * rs)) | 1); E = nd.grey_closing(E, size=(k, k))
    if s.get("oeffnen2_m"):
        k = max(3, int(round(s["oeffnen2_m"] * rs)) | 1); E = nd.grey_opening(E, size=(k, k))
    if s.get("sigma_m"):
        E = nd.gaussian_filter(E, s["sigma_m"] * rs, mode="nearest")
    return E


def anwenden(GB, D, stellen, rs, WV=None):
    """GB (und bei L3b-Wasserstellen den Wasserspiegel WV) lokal ersetzen. Wassergrundriss (WV > -900) bleibt gleich."""
    GY, GX = GB.shape
    H = GB.astype(np.float64)
    W0 = schutz(D, GY, GX, rs); Wcache = {}
    neu = H.copy(); bericht = []
    wv = None if WV is None else WV.astype(np.float64).copy()
    wasser = None if WV is None else WV > -900
    for s in stellen:
        if not s.get("aktiv", True):
            bericht.append({"id": s["id"], "aktiv": False}); continue
        wa = s.get("weg_abstand_m"); mw = not s.get("wasser", False)
        wr = s.get("weg_rand_m", 0.5)
        rm = s.get("rampe_m", 2.0)
        key = (wa, mw, wr, rm)
        if key not in Wcache:
            Wcache[key] = schutz(D, GY, GX, rs, 1.5 if wa is None else wa, mw, wr, rm)
        w = gewicht(s, GY, GX, rs) * Wcache[key]
        m = w > 1e-4
        if not m.any():
            bericht.append({"id": s["id"], "max_m": 0.0}); continue
        zs, xs = np.where(m); pad = 12
        sl = (slice(max(zs.min() - pad, 0), zs.max() + pad + 1), slice(max(xs.min() - pad, 0), xs.max() + pad + 1))
        E = ersatz(neu[sl], s, rs)
        if s.get("stufe") == "ebene":
            kern = gewicht(s, GY, GX, rs)[sl] > 0.99
            E = np.where(kern, np.median(E[kern]), E)
            E = nd.gaussian_filter(E, 1.0 * rs, mode="nearest") if s.get("sigma_m") else E
        info = {"id": s["id"], "kachel": s.get("kachel")}
        if s.get("wasser") and wv is not None:
            wm = wasser[sl]
            if wm.any():
                # Wasserspiegel: Landvertices mit naechstem Wasserwert fuellen, gleiche Ersatzform, nur auf Wasser zurueckschreiben
                idx = nd.distance_transform_edt(~wm, return_distances=False, return_indices=True)
                F = wv[sl][idx[0], idx[1]]
                Ew = ersatz(F, {k: v for k, v in s.items() if k not in ("oeffnen_m", "oeffnen2_m")}, rs) if s.get("wasserspiegel", True) else F
                altw = wv[sl].copy()
                neuw = np.where(wm, altw + w[sl] * (Ew - altw), altw)
                wv[sl] = neuw
                info["max_wv_m"] = round(float(np.abs(neuw - altw).max()), 3)
                if s.get("ufer_heben_m") is not None:
                    # Uferband: aeusserste Wasservertices (<= ufer_band_m vom Grundrissrand) so heben, dass das Gelaende knapp
                    # ueber dem Spiegel liegt -> sichtbare Uferlinie = glatte Hoehenlinie statt Rastertreppe
                    rand = nd.distance_transform_edt(wm, sampling=1.0 / rs) <= s.get("ufer_band_m", 0.75)
                    ziel = neuw + s["ufer_heben_m"]
                    E = np.where(wm & rand, np.maximum(E, ziel), E)
                    E = nd.gaussian_filter(E, 0.5 * rs, mode="nearest")
                    E = np.where(wm & rand, np.maximum(E, ziel), E)
        alt = neu[sl].copy()
        neu[sl] = alt + w[sl] * (E - alt)
        d = neu[sl] - alt
        info.update({"max_m": round(float(np.abs(d).max()), 3), "vertices_geaendert": int((np.abs(d) > 1e-4).sum())})
        bericht.append(info)
    return neu.astype(np.float32), bericht, (None if wv is None else wv.astype(np.float32))


def objekte(D, delta, rs):
    n = 0
    GY, GX = delta.shape
    for key in ("baeume", "steine", "geroell", "findlinge"):
        for o in D.get(key, []):
            ix, iz = int(round(o[0] * rs)), int(round(o[2] * rs))
            if 0 <= iz < GY and 0 <= ix < GX and abs(delta[iz, ix]) > 1e-4:
                o[1] = round(o[1] + float(delta[iz, ix]), 3); n += 1
    return n


def fw_folgen(D, dfw, rs):
    """L3b: Feinband-Hoehen FW.h folgen der Hoehenaenderung der Stellen mit "fw_folgen" (bilinear)."""
    from scipy import ndimage as ndi
    FW = D["FW"]; fs = int(FW["fs"]); fxn = int(D["nx"]) * fs + 1
    vid = np.frombuffer(base64.b64decode(FW["vid"]), np.uint32)
    fh = np.frombuffer(base64.b64decode(FW["h"]), np.float32).copy()
    fx = (vid % fxn) / fs; fz = (vid // fxn) / fs
    d = ndi.map_coordinates(dfw, [fz * rs, fx * rs], order=1, mode="nearest", prefilter=False)
    sel = np.flatnonzero(np.abs(d) > 1e-5)
    alt = fh[sel].copy(); fh[sel] = (fh[sel] + d[sel]).astype(np.float32)
    return sel, alt, base64.b64encode(fh.tobytes()).decode()


def fw_setzen(D, idx, werte):
    fh = np.frombuffer(base64.b64decode(D["FW"]["h"]), np.float32).copy(); fh[idx] = werte
    D["FW"]["h"] = base64.b64encode(fh.tobytes()).decode()


def prototypen(N, GBn, geaendert):
    sys.path.insert(0, str(R))
    from neu import mesh as M
    tiles = N["neu_mesh_tiles"]["tiles"]; out = {}
    src = M.load_relief(QUELLE)
    rs = 2
    for t, it in tiles.items():
        x0, z0, x1, z1 = it["bounds"]
        slab_neu = GBn[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1]
        if not geaendert[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1].any():
            out[t] = "unveraendert"; continue
        if t == "D2":
            raise RuntimeError("D2 waere geaendert - Abbruch")
        P, I = M.tile_mesh(src, t, slab_neu.astype("<f4"))
        it["vertices_xyz_f32"] = base64.b64encode(P.astype("<f4").tobytes()).decode()
        it["indices_u32"] = base64.b64encode(I.astype("<u4").tobytes()).decode()
        it["vertices"] = int(len(P)); it["triangles"] = int(len(I) // 3)
        it["height_sha256"] = hashlib.sha256(P[:, 1].astype("<f4").tobytes()).hexdigest()
        it["mesh_sha256"] = hashlib.sha256(P.astype("<f4").tobytes() + I.astype("<u4").tobytes()).hexdigest()
        out[t] = "neu vermascht (tile_mesh)"
    return out


def main():
    arg = sys.argv[1:]
    cfg = json.loads(STELLEN.read_text(encoding="utf-8"))
    D = json.load(gzip.open(QUELLE)); N = json.load(gzip.open(NEU))
    nx, ny, rs = D["nx"], D["ny"], D["rs"]; GY, GX = ny * rs + 1, nx * rs + 1
    GB = np.frombuffer(base64.b64decode(D["GB"]), np.float32).reshape(GY, GX).copy()
    x0, z0, x1, z1 = D2_BOX
    d2_sha = _sha(GB[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1])
    if "--aus" in arg:
        if not RUECK.exists(): print("kein l3_rueck.npz - L3 nicht aktiv"); return
        r = np.load(RUECK); idx = r["idx"]; GBf = GB.reshape(-1).copy(); GBf[idx] = r["alt"]
        if "wv_idx" in r.files:
            WVa = np.frombuffer(base64.b64decode(D["WV"]), np.float32).copy(); WVa[r["wv_idx"]] = r["wv_alt"]
            D["WV"] = N["WV"] = base64.b64encode(WVa.tobytes()).decode()
        if "fw_idx" in r.files:
            fw_setzen(D, r["fw_idx"], r["fw_alt"])
            if "FW" in N: fw_setzen(N, r["fw_idx"], r["fw_alt"])
        GBn = GBf.reshape(GY, GX); delta = GBn.astype(np.float64) - GB
        geaendert = GBn != GB
        D["GB"] = N["GB"] = base64.b64encode(GBn.tobytes()).decode()
        no = objekte(D, delta, rs); objekte(N, delta, rs)
        pt = prototypen(N, GBn, geaendert)
        _schreibe(D, QUELLE, False); _schreibe(N, NEU, True); RUECK.unlink()
        print(json.dumps({"l3": "aus", "objekte": no, "prototypen": pt})); return
    if _sha(GB) != cfg["basis_gb_sha256"]:
        sys.exit(f"GB entspricht nicht der L3-Basis ({_sha(GB)[:12]}); zuerst 'relief_l3.py --aus'")
    if os.environ.get("RELIEF_L3", "1") == "0":
        print("RELIEF_L3=0: nichts angewendet"); return
    WV = np.frombuffer(base64.b64decode(D["WV"]), np.float32).reshape(GY, GX).copy()
    GBn, bericht, WVn = anwenden(GB, D, cfg["stellen"], rs, WV)
    wv_geaendert = WVn != WV
    if not np.array_equal(WVn > -900, WV > -900): sys.exit("Wassergrundriss geaendert - Abbruch")
    delta = GBn.astype(np.float64) - GB.astype(np.float64)
    geaendert = GBn != GB
    d2n = _sha(GBn[z0 * rs:z1 * rs + 1, x0 * rs:x1 * rs + 1])
    info = {"stellen": bericht, "vertices_geaendert": int(geaendert.sum()), "wv_vertices_geaendert": int(wv_geaendert.sum()),
            "wv_max_abs_m": round(float(np.abs(WVn.astype(float) - WV).max()), 3), "max_abs_m": round(float(np.abs(delta).max()), 3),
            "d2_gb_sha256_vorher": d2_sha, "d2_gb_sha256_nachher": d2n, "gb_sha256_nachher": _sha(GBn)}
    if d2n != d2_sha: sys.exit("D2 geaendert - Abbruch")
    if "--trocken" in arg:
        print(json.dumps(info, indent=1)); return
    idx = np.flatnonzero(geaendert.reshape(-1))
    widx = np.flatnonzero(wv_geaendert.reshape(-1))
    GBo, _b, _w = anwenden(GB, D, [t for t in cfg["stellen"] if not t.get("fw_folgen")], rs, WV)
    fidx, falt, fh_neu = fw_folgen(D, GBn.astype(np.float64) - GBo.astype(np.float64), rs)
    np.savez_compressed(RUECK, idx=idx, alt=GB.reshape(-1)[idx], wv_idx=widx, wv_alt=WV.reshape(-1)[widx], fw_idx=fidx, fw_alt=falt)
    if fidx.size:
        D["FW"]["h"] = fh_neu
        if "FW" in N: N["FW"]["h"] = fh_neu
    info["fw_vertices_geaendert"] = int(fidx.size)
    if widx.size: D["WV"] = N["WV"] = base64.b64encode(WVn.tobytes()).decode()
    D["GB"] = N["GB"] = base64.b64encode(GBn.tobytes()).decode()
    info["objekte_angepasst"] = objekte(D, delta, rs); objekte(N, delta, rs)
    info["prototypen"] = prototypen(N, GBn, geaendert)
    _schreibe(D, QUELLE, False); _schreibe(N, NEU, True)
    (R / "pruefung" / "l3_bericht.json").write_text(json.dumps(info, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    main()

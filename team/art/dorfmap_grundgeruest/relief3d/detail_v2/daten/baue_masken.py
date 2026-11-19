#!/usr/bin/env python3
"""P4 detail_v2 Datenschicht: flaeche.png, untergrund.png, begehbar.png (+ hoehe.png ab P2-Mesh).

GeoJSON-Schema (Entscheidung Grundgeruest 19.11.2026) [F]:
  FeatureCollection, Koordinaten in Viewer-Metern (1 Einheit = 1 Zelle = 1 m, Ursprung Weltecke wie UV1),
  Properties: klasse (int 0-5, s. legende.json flaeche.klassen), untergrund (Schnee/Wald/Boden/Sand), id.
Gerastert werden alle (Multi)Polygon-Features aus detail_v2/vektor/*.geojson:
  - flaeche.png: Feature mit Property klasse, Prioritaet Wasser > Bruecke > Weg > Ufer > Fels/Klippe > Grund,
    Pixelmitten-Regel; nicht abgedeckte Pixel = 0 (Grund).
  - untergrund.png: Features mit Property untergrund (zonen.geojson); fehlt sie ueberall -> 1-m-Fallback aus
    zellen_relief.csv (im Lauf ausgewiesen). Wo flaeche wasser/fels_klippe/bruecke ist -> 0 [A].
  - Mesh (mesh/manifest.json, mesh_raster.py): Hoehe/Neigung je Pixel; Bruecken aus manifest.modelle setzen im
    Deck-Fussabdruck flaeche = 5 (ueberschreibt Wasser), Hoehe = Deck, untergrund = 0 [F ueber Grundgeruest].
  - begehbar.png: Klasse nicht in {3,4} UND Neigung <= 35 Grad [F]; Pixel ohne Mesh-Treffer = 0 (gezaehlt).
    Mit --ohne-mesh nur aus der Flaeche (ausgewiesen). Linien-/Punkt-Features werden nicht gerastert.
  - hoehe.png: 16 bit, hoehe_m = offset_m + wert * skala_m (skala 1 mm), Werte in masken_meta.json.
  - wege.geojson: klasse ist dort der Weg-TYP aus P1a (GASSE/ANBINDUNG/HAUSWEG ...), keine Flaechenklasse [F Befund
    Grundgeruest 19.11.]: nicht-numerische klasse -> Flaechenklasse 1 (Weg), Typ bleibt als weg_typ erhalten
    (weg_typ.png + masken_meta.weg_typen); unbekannter Typ -> 1 mit WARNUNG. In allen anderen Dateien: Fehler.
  - zonen.geojson (Schema #61): Punkte mit Property zellen ([cx, cz], 1 m, Ursprung Weltecke) und flaeche_m2.
    typ bauzone -> bauzone.png (1 bit), typ slot_bau/slot_deko -> slot_zonen.png (8 bit: 0 frei, 1 Bau, 2 Deko),
    Abgleich gegen slot.png/slots.json -> abgleich_slots.json (nur Bericht).
  - F10 [F Grundgeruest 19.11.]: Wasserspiegel zaehlt nur, wo er UEBER dem Gelaende liegt. Mit Mesh: Pixel mit
    flaeche = wasser, deren oberste Mesh-Flaeche kein Wasser ist (Spiegel steckt im Ufer), bekommen Klasse und
    Hoehe des Gelaendes (mesh_raster.rastere waehlt Wasser nur bei y_wasser > y_gelaende). Ohne Mesh nicht pruefbar.
  - Bericht: Abgleich begehbar (1-m-Mehrheit) gegen zellen_relief.csv begehbar_3d, Abweichung > 1 % = WARNUNG
    (keine harte Regel) -> abgleich_begehbar_3d.json.

Aufruf:
    python3 baue_masken.py --pruefe-quellen
    python3 baue_masken.py --selbsttest
    python3 baue_masken.py --out <ordner> [--vektor <ordner>] [--ohne-mesh]
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

HIER = Path(__file__).resolve().parent
DV2 = HIER.parent                      # relief3d/detail_v2/
RELIEF = DV2.parent
NX, NY, PX_PRO_M = 336, 303, 10
W, H = NX * PX_PRO_M, NY * PX_PRO_M
RAND_TOL_M = 0.01

KLASSE = {"grund": 0, "weg": 1, "ufer": 2, "fels_klippe": 3, "wasser": 4, "bruecke": 5}
KLASSE_NAME = {v: k for k, v in KLASSE.items()}
PRIORITAET = ["wasser", "bruecke", "weg", "ufer", "fels_klippe", "grund"]   # hoechste zuerst
UNTERGRUND = {"schnee": 1, "wald": 2, "boden": 3, "sand": 4}
UNTERGRUND_ALT = {"SCHNEE": 1, "WALD": 2, "BODEN": 3, "SAND": 4}
OHNE_UNTERGRUND = (KLASSE["wasser"], KLASSE["fels_klippe"], KLASSE["bruecke"])
NICHT_BEGEHBAR = (KLASSE["wasser"], KLASSE["fels_klippe"])
WEG_DATEI = "wege.geojson"
WEG_TYPEN = ["HAUSWEG", "ANBINDUNG", "GASSE"]       # bekannte P1a-Typen, niedrigste Prioritaet zuerst (weg_typ.png 1..3)
SLOT_ZONEN = {"slot_bau": 1, "slot_deko": 2}

QUELLEN = {
    "wege": "wege.geojson", "kreuzungen": "kreuzungen.geojson",          # P1a
    "wasser": "wasser.geojson", "ufer": "ufer.geojson",                  # P1b
    "zonen": "zonen.geojson", "kanten": "kanten.geojson", "grat": "grat.geojson",  # P1c
}
MESH_MANIFEST = DV2 / "mesh" / "manifest.json"                           # P2 (Fr)


sys.path.insert(0, str(HIER))


def pruefe_quellen(vektor: Path, manifest: Path | None = MESH_MANIFEST) -> list[str]:
    fehlt = []
    for k, n in QUELLEN.items():
        ok = (vektor / n).exists(); fehlt += [] if ok else [k]
        print(f"{'ok   ' if ok else 'FEHLT'} {k:14s} {vektor / n}")
    if manifest is not None:
        ok = manifest.exists(); fehlt += [] if ok else ["mesh_manifest"]
        print(f"{'ok   ' if ok else 'FEHLT'} {'mesh_manifest':14s} {manifest}")
    return fehlt


def lies_features(pfad: Path) -> list[dict]:
    """FeatureCollection lesen und gegen das Schema pruefen. Rueckgabe: Polygon-Features
    {id, quelle, geom, klasse|None, untergrund|None}. Fehler -> ValueError mit Datei + id."""
    from shapely.geometry import shape
    d = json.loads(pfad.read_text(encoding="utf-8"))
    if d.get("type") != "FeatureCollection":
        raise ValueError(f"{pfad.name}: keine FeatureCollection")
    out = []
    for n, f in enumerate(d.get("features", [])):
        p = f.get("properties") or {}
        fid = p.get("id", f.get("id", f"#{n}"))
        g = f.get("geometry")
        if not g or g.get("type") not in ("Polygon", "MultiPolygon"):
            continue                                   # Linien/Punkte: nicht rastern
        geom = shape(g)
        if not geom.is_valid:
            raise ValueError(f"{pfad.name} id={fid}: Polygon ungueltig")
        x0, z0, x1, z1 = geom.bounds
        if x0 < -RAND_TOL_M or z0 < -RAND_TOL_M or x1 > NX + RAND_TOL_M or z1 > NY + RAND_TOL_M:
            raise ValueError(f"{pfad.name} id={fid}: ausserhalb 0-{NX}|0-{NY} m (bounds {geom.bounds}) - Einheit pruefen (1,2-m-Zellen?)")
        kl, weg_typ = p.get("klasse"), None
        if pfad.name == WEG_DATEI and isinstance(kl, str) and not kl.strip().lstrip("-").isdigit():
            weg_typ, kl = kl, KLASSE["weg"]                # Weg-Typ (P1a) -> Flaechenklasse Weg
            if weg_typ not in WEG_TYPEN:
                print(f"WARNUNG {pfad.name} id={fid}: unbekannter Weg-Typ {weg_typ!r} -> klasse 1 (weg)", file=sys.stderr)
        if kl is not None:
            if isinstance(kl, bool) or not isinstance(kl, int) or kl not in KLASSE_NAME:
                raise ValueError(f"{pfad.name} id={fid}: klasse {kl!r} nicht 0-5")
        ug = p.get("untergrund")
        if ug is not None:
            if str(ug).lower() not in UNTERGRUND:
                raise ValueError(f"{pfad.name} id={fid}: untergrund {ug!r} nicht Schnee/Wald/Boden/Sand")
            ug = UNTERGRUND[str(ug).lower()]
        out.append({"id": fid, "quelle": pfad.name, "geom": geom, "klasse": kl, "untergrund": ug, "weg_typ": weg_typ})
    return out


def lies_zellen_punkte(pfad: Path) -> list[dict]:
    """Punkt-Features mit Property zellen (Schema #61): [{id, typ, zellen: ndarray (n,2) [cx, cz]}].
    Prueft Zellformat, Kartenbereich, Doppelte und flaeche_m2 = Zellzahl (1 m^2 je Zelle)."""
    if not pfad.exists():
        return []
    d = json.loads(pfad.read_text(encoding="utf-8"))
    out = []
    for n, f in enumerate(d.get("features", [])):
        p = f.get("properties") or {}
        if (f.get("geometry") or {}).get("type") != "Point" or "zellen" not in p:
            continue
        fid = p.get("id", f"#{n}")
        z = np.asarray(p["zellen"])
        if z.ndim != 2 or z.shape[1] != 2 or z.dtype.kind not in "iu":
            raise ValueError(f"{pfad.name} id={fid}: zellen nicht [[cx, cz], ...] ganzzahlig")
        if (z < 0).any() or (z[:, 0] >= NX).any() or (z[:, 1] >= NY).any():
            raise ValueError(f"{pfad.name} id={fid}: Zelle ausserhalb 0-{NX - 1}|0-{NY - 1}")
        if len(np.unique(z, axis=0)) != len(z):
            raise ValueError(f"{pfad.name} id={fid}: Zelle doppelt")
        if "flaeche_m2" in p and abs(float(p["flaeche_m2"]) - len(z)) > 1e-6:
            raise ValueError(f"{pfad.name} id={fid}: flaeche_m2 {p['flaeche_m2']} != {len(z)} Zellen")
        out.append({"id": fid, "typ": p.get("typ"), "zellen": z})
    return out


def zellen_maske_1m(zellen: list[np.ndarray]) -> np.ndarray:
    m = np.zeros((NY, NX), bool)
    for z in zellen:
        m[z[:, 1], z[:, 0]] = True
    return m


def auf_px(m1: np.ndarray) -> np.ndarray:
    return np.kron(m1.astype(np.uint8), np.ones((PX_PRO_M, PX_PRO_M), np.uint8))


def rastere_weg_typ(features: list[dict], flaeche: np.ndarray) -> tuple[np.ndarray, dict]:
    typen = list(WEG_TYPEN) + sorted({f["weg_typ"] for f in features if f["weg_typ"] and f["weg_typ"] not in WEG_TYPEN})
    out = np.zeros((H, W), np.uint8)
    for n, t in enumerate(typen, 1):                   # GASSE zuletzt = gewinnt bei Ueberlappung
        for f in features:
            if f["weg_typ"] == t:
                male(out, f["geom"], n)
    out[flaeche != KLASSE["weg"]] = 0                  # nur wo die Flaeche Weg ist (Wasser/Bruecke gewinnen)
    return out, {str(n): t for n, t in enumerate(typen, 1)}


def abgleich_slots(punkte: list[dict], slot_png: Path, slots_json: Path) -> dict:
    """Bericht: Slot-Zellen aus zonen.geojson gegen slot.png (Bit 14 Bauplatz-Zelle, ID-Bits) und slots.json."""
    from PIL import Image
    sp = np.array(Image.open(slot_png)).astype(np.uint16)[PX_PRO_M // 2::PX_PRO_M, PX_PRO_M // 2::PX_PRO_M]  # Zellmitten
    sj = {s["id"]: s for s in json.loads(slots_json.read_text(encoding="utf-8"))["slots"]}
    sid = sp & 0x0FFF
    art = np.vectorize(lambda i: sj[i]["art"] if i in sj else "", otypes=[object])(sid)
    soll = {"slot_bau": (sp & (1 << 14)) > 0, "slot_deko": art == "deko"}
    ber = {"regel": "Bericht; Zelle = 1 m, slot.png an Zellmitten gelesen; slot_bau ~ Bit 14 (Bauplatz-Zelle), slot_deko ~ ID mit art deko"}
    for typ, s_m in soll.items():
        ps = [p for p in punkte if p["typ"] == typ]
        ist = zellen_maske_1m([p["zellen"] for p in ps])
        nur_z, nur_s = ist & ~s_m, s_m & ~ist
        # je Punkt: welche slots.json-ID deckt die Zellen? (Mehrheit), eindeutig?
        zuord, mehrdeutig, ohne = {}, [], []
        for p in ps:
            ids = sid[p["zellen"][:, 1], p["zellen"][:, 0]]
            ids = ids[ids > 0]
            if not len(ids):
                ohne.append(p["id"]); continue
            w, c = np.unique(ids, return_counts=True)
            zuord[p["id"]] = int(w[c.argmax()])
            if len(w) > 1: mehrdeutig.append(p["id"])
        doppelt = sorted({i for i in zuord.values() if list(zuord.values()).count(i) > 1})
        sj_art = {"slot_bau": ("bauplatz",), "slot_deko": ("deko",)}[typ]
        ids_soll = {i for i, s in sj.items() if s["art"] in sj_art}
        ber[typ] = {"punkte": len(ps), "zellen_zonen": int(ist.sum()), "zellen_slot_png": int(s_m.sum()),
                    "gleich": int((ist & s_m).sum()), "nur_zonen": int(nur_z.sum()), "nur_slot_png": int(nur_s.sum()),
                    "beispiele_nur_zonen": [[int(x), int(z)] for z, x in zip(*np.nonzero(nur_z))][:20],
                    "beispiele_nur_slot_png": [[int(x), int(z)] for z, x in zip(*np.nonzero(nur_s))][:20],
                    "slots_json_ids_soll": len(ids_soll), "slots_json_ids_getroffen": len(set(zuord.values()) & ids_soll),
                    "ids_fehlend": sorted(ids_soll - set(zuord.values()))[:50],
                    "punkte_ohne_slot_id": ohne[:50], "punkte_mehrere_ids": mehrdeutig[:50], "ids_mehrfach": doppelt[:50]}
    ber["abweichung"] = any(ber[t]["nur_zonen"] or ber[t]["nur_slot_png"] for t in soll)
    return ber


def pixelmitten(bbox_m):
    x0, z0, x1, z1 = bbox_m
    i0, j0 = max(0, int(np.floor(x0 * PX_PRO_M))), max(0, int(np.floor(z0 * PX_PRO_M)))
    i1, j1 = min(W, int(np.ceil(x1 * PX_PRO_M))), min(H, int(np.ceil(z1 * PX_PRO_M)))
    return i0, j0, (np.arange(i0, i1) + 0.5) / PX_PRO_M, (np.arange(j0, j1) + 0.5) / PX_PRO_M


def male(out: np.ndarray, geom, wert: int) -> int:
    import shapely
    if geom.is_empty:
        return 0
    shapely.prepare(geom)
    i0, j0, xs, zs = pixelmitten(geom.bounds)
    if xs.size == 0 or zs.size == 0:
        return 0
    X, Z = np.meshgrid(xs, zs)
    m = shapely.contains_xy(geom, X, Z)
    out[j0:j0 + m.shape[0], i0:i0 + m.shape[1]][m] = wert
    return int(m.sum())


def rastere_flaeche(features: list[dict]) -> np.ndarray:
    out = np.zeros((H, W), np.uint8)
    for kl in reversed(PRIORITAET):                    # niedrigste zuerst, hoechste zuletzt
        for f in features:
            if f["klasse"] == KLASSE[kl]:
                male(out, f["geom"], KLASSE[kl])
    return out


def untergrund_fallback_1m() -> np.ndarray:
    import csv
    z = np.zeros((NY, NX), np.uint8)
    with (RELIEF / "zellen_relief.csv").open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            z[int(r["cy"]), int(r["cx"])] = UNTERGRUND_ALT.get(r["untergrund"], 0)
    return np.kron(z, np.ones((PX_PRO_M, PX_PRO_M), np.uint8))


def rastere_untergrund(features: list[dict], flaeche: np.ndarray) -> tuple[np.ndarray, str]:
    ug = [f for f in features if f["untergrund"] is not None]
    if ug:
        out = np.zeros((H, W), np.uint8)
        for f in ug:
            male(out, f["geom"], f["untergrund"])
        quelle = f"Polygone ({len(ug)} Features)"
    else:
        out, quelle = untergrund_fallback_1m(), "FALLBACK 1 m zellen_relief.csv (keine untergrund-Polygone)"
    out[np.isin(flaeche, OHNE_UNTERGRUND)] = 0
    return out, quelle


def begehbar_aus_flaeche(flaeche: np.ndarray) -> np.ndarray:
    return (~np.isin(flaeche, NICHT_BEGEHBAR)).astype(np.uint8)


def schreibe_png(arr: np.ndarray, ziel: Path, bit: int) -> None:
    from PIL import Image
    if bit == 1:
        img = Image.fromarray((arr > 0).astype(np.uint8) * 255).convert("1")
    elif bit == 8:
        img = Image.fromarray(arr.astype(np.uint8), "L")
    else:
        img = Image.fromarray(arr.astype(np.uint16))
    img.save(ziel)
    chk = np.array(Image.open(ziel))
    soll = (arr > 0) if bit == 1 else arr
    assert (chk.astype(soll.dtype) == soll).all(), f"Rueckleseprobe {ziel.name} fehlgeschlagen"


def abgleich_begehbar_3d(be: np.ndarray) -> dict:
    """1-m-Zelle begehbar, wenn >= 50 % ihrer 100 Pixel begehbar; Vergleich mit zellen_relief.csv begehbar_3d (nur Bericht)."""
    import csv
    alt = np.zeros((NY, NX), np.uint8)
    with (RELIEF / "zellen_relief.csv").open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            alt[int(r["cy"]), int(r["cx"])] = r["begehbar_3d"] == "1"
    neu = be.reshape(NY, PX_PRO_M, NX, PX_PRO_M).mean((1, 3)) >= 0.5
    ab = neu != alt.astype(bool)
    anteil = float(ab.mean())
    je_kachel = {}
    for j in range(7):
        for i in range(8):
            z1 = NY if j == 6 else 43 * (j + 1)
            n = int(ab[43 * j:z1, 42 * i:42 * (i + 1)].sum())
            if n: je_kachel["ABCDEFGH"[i] + str(j + 1)] = n
    zz, xx = np.nonzero(ab)
    return {"regel": "Bericht, keine harte Regel [F ueber Grundgeruest]; Zelle begehbar wenn >= 50 % Pixel",
            "zellen": NX * NY, "abweichend": int(ab.sum()), "anteil": round(anteil, 5),
            "neu_begehbar_alt_nicht": int((neu & ~alt.astype(bool)).sum()), "alt_begehbar_neu_nicht": int((~neu & alt.astype(bool)).sum()),
            "warnung": anteil > 0.01, "je_kachel": je_kachel,
            "beispiele": [[int(x), int(z)] for x, z in zip(xx[:200], zz[:200])]}


def schreibe_hoehe(h: np.ndarray, ziel: Path) -> dict:
    ok = ~np.isnan(h)
    skala = 0.001
    off = float(np.floor(np.nanmin(h) * 1000) / 1000) if ok.any() else 0.0
    while ok.any() and (np.nanmax(h) - off) / skala > 65535:
        skala *= 2
    w = np.zeros(h.shape, np.uint16)
    w[ok] = np.round((h[ok] - off) / skala).astype(np.uint16)
    schreibe_png(w, ziel, 16)
    rest = float(np.nanmax(np.abs(off + w[ok] * skala - h[ok]))) if ok.any() else 0.0
    return {"offset_m": off, "skala_m": skala, "max_quantisierung_m": round(rest, 6), "ohne_wert_px": int((~ok).sum())}


def baue(vektor: Path, out: Path, manifest: Path | None = None) -> dict:
    feats = []
    for n in sorted(vektor.glob("*.geojson")):
        feats += lies_features(n)
    if not any(f["klasse"] is not None for f in feats):
        raise ValueError("kein Polygon-Feature mit Property klasse gefunden")
    fl = rastere_flaeche(feats)
    wt = {}
    for f in feats:
        if f["weg_typ"]: wt[f["weg_typ"]] = wt.get(f["weg_typ"], 0) + 1
    info = {"features": len(feats), "weg_typen": {"regel": "wege.geojson klasse = Weg-Typ -> Flaechenklasse 1", "polygone": wt}}
    out.mkdir(parents=True, exist_ok=True)
    if manifest is not None:
        import mesh_raster as MR
        m = MR.lade_mesh(manifest)
        r = MR.rastere(m)
        # F10: Wasser aus den Vektoren gilt nur, wo das Mesh dort Wasser oben hat (Spiegel ueber Gelaende)
        f10 = (fl == KLASSE["wasser"]) & (r["klasse"] >= 0) & (r["klasse"] != KLASSE["wasser"]) & ~r["deck_maske"]  # Deck folgt unten
        fl[f10] = r["klasse"][f10]
        info["f10_wasser_zu_gelaende_px"] = int(f10.sum()); info["f10_quelle"] = r.get("f10", {})
        fl[r["deck_maske"]] = KLASSE["bruecke"]
        be = MR.begehbar_regel(fl, r["neigung"]).astype(np.uint8)
        info.update({"mesh": {"kacheln": len(m["manifest"]["kacheln"]), "vollstaendig": m["vollstaendig"],
                              "gemischte_dreiecke": m["gemischte_dreiecke"], "ohne_mesh_px": r["ohne_mesh_px"], "deck": r["deck"]},
                     "begehbar_regel": "klasse nicht in {3,4} und neigung <= 35 Grad; ohne Mesh-Treffer 0",
                     "hoehe": schreibe_hoehe(r["hoehe"], out / "hoehe.png")})
    else:
        be = begehbar_aus_flaeche(fl)
        info["begehbar_regel"] = "OHNE MESH: nur Flaeche (Neigung fehlt)"
        info["f10"] = "OHNE MESH nicht anwendbar (keine Gelaendehoehe); wirkt im Lauf mit Mesh"
    ug, ug_quelle = rastere_untergrund(feats, fl)
    schreibe_png(fl, out / "flaeche.png", 8)
    schreibe_png(ug, out / "untergrund.png", 8)
    schreibe_png(be, out / "begehbar.png", 1)
    wtp, wt_leg = rastere_weg_typ(feats, fl)
    schreibe_png(wtp, out / "weg_typ.png", 8)
    info["weg_typen"]["legende"] = wt_leg
    info["weg_typen"]["anteil"] = {t: round(float((wtp == int(n)).mean()), 5) for n, t in wt_leg.items()}
    punkte = lies_zellen_punkte(vektor / "zonen.geojson")
    bz = [p["zellen"] for p in punkte if p["typ"] == "bauzone"]
    if bz:
        bm = zellen_maske_1m(bz)
        schreibe_png(auf_px(bm), out / "bauzone.png", 1)
        info["bauzone"] = {"punkte": len(bz), "zellen": int(bm.sum()), "zellen_summe": int(sum(len(z) for z in bz))}
    sz = [p for p in punkte if p["typ"] in SLOT_ZONEN]
    if sz:
        sm = np.zeros((NY, NX), np.uint8)
        for typ, v in SLOT_ZONEN.items():
            m1 = zellen_maske_1m([p["zellen"] for p in sz if p["typ"] == typ])
            if (sm[m1] > 0).any(): raise ValueError(f"zonen.geojson: {typ}-Zellen ueberlappen andere Slot-Zellen")
            sm[m1] = v
        schreibe_png(np.kron(sm, np.ones((PX_PRO_M, PX_PRO_M), np.uint8)), out / "slot_zonen.png", 8)
        info["slot_zonen"] = {t: {"punkte": sum(p["typ"] == t for p in sz), "zellen": int((sm == v).sum())} for t, v in SLOT_ZONEN.items()}
        if (HIER / "slot.png").exists():
            ab_s = abgleich_slots(punkte, HIER / "slot.png", HIER / "slots.json")
            (out / "abgleich_slots.json").write_text(json.dumps(ab_s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            info["abgleich_slots"] = {t: {k: ab_s[t][k] for k in ("punkte", "zellen_zonen", "zellen_slot_png", "nur_zonen", "nur_slot_png", "slots_json_ids_soll", "slots_json_ids_getroffen")} for t in SLOT_ZONEN}
            info["abgleich_slots"]["abweichung"] = ab_s["abweichung"]
    if not punkte:
        info["zellen_punkte"] = "keine Punkte mit zellen in zonen.geojson (Schema #61 fehlt?) -> keine bauzone/slot_zonen"
    info["flaeche_anteil"] = {KLASSE_NAME[k]: round(float((fl == k).mean()), 5) for k in KLASSE_NAME}
    info["untergrund_quelle"] = ug_quelle
    ab = abgleich_begehbar_3d(be)
    (out / "abgleich_begehbar_3d.json").write_text(json.dumps(ab, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    info["abgleich_begehbar_3d"] = {k: ab[k] for k in ("abweichend", "anteil", "warnung")}
    if ab["warnung"]:
        print(f"WARNUNG begehbar vs. begehbar_3d: {ab['anteil']:.2%} der Zellen abweichend (> 1 %), s. abgleich_begehbar_3d.json", file=sys.stderr)
    (out / "masken_meta.json").write_text(json.dumps(info, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return info


def selbsttest() -> None:
    fc = lambda feats: {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": p, "geometry": {"type": "Polygon", "coordinates": [c]}} for p, c in feats]}
    box = lambda x0, z0, x1, z1: [[x0, z0], [x1, z0], [x1, z1], [x0, z1], [x0, z0]]
    with tempfile.TemporaryDirectory(prefix="dv2_daten_selbst_", dir="/tmp") as t:
        v = Path(t) / "vektor"; v.mkdir()
        (v / "zonen.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": fc([
            ({"id": "z1", "klasse": 0, "untergrund": "Schnee"}, box(0, 0, NX, NY)),
            ({"id": "z2", "klasse": 0, "untergrund": "Wald"}, box(50, 50, 60, 60)),
            ({"id": "f1", "klasse": 3}, box(10, 10, 20, 20))])["features"] + [
            {"type": "Feature", "properties": {"id": "bz1", "typ": "bauzone", "zellen": [[1, 1], [2, 1]], "flaeche_m2": 2.0},
             "geometry": {"type": "Point", "coordinates": [2.0, 1.5]}},
            {"type": "Feature", "properties": {"id": "sb1", "typ": "slot_bau", "zellen": [[3, 3]], "flaeche_m2": 1.0},
             "geometry": {"type": "Point", "coordinates": [3.5, 3.5]}},
            {"type": "Feature", "properties": {"id": "sd1", "typ": "slot_deko", "zellen": [[4, 4], [5, 4]], "flaeche_m2": 2.0},
             "geometry": {"type": "Point", "coordinates": [5.0, 4.5]}}]}))
        # wege.geojson: klasse = Weg-Typ (P1a) -> Flaeche 1, Typ in weg_typ.png; unbekannter Typ -> 1 + Warnung
        (v / "wege.geojson").write_text(json.dumps(fc([({"id": "w1", "klasse": 1}, box(15, 0, 16, 303)),
                                                      ({"id": "g1", "klasse": "GASSE"}, box(60, 0, 62, 10)),
                                                      ({"id": "h1", "klasse": "HAUSWEG"}, box(61, 5, 64, 10)),
                                                      ({"id": "n1", "klasse": "NEUTYP"}, box(70, 0, 71, 10))])))
        (v / "wasser.geojson").write_text(json.dumps(fc([({"id": "a1", "klasse": 4}, box(15.2, 12, 40, 18))])))
        (v / "linien.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": [
            {"type": "Feature", "properties": {"id": "l1"}, "geometry": {"type": "LineString", "coordinates": [[0, 0], [5, 5]]}}]}))
        info = baue(v, Path(t) / "out")
        from PIL import Image
        fl = np.array(Image.open(Path(t) / "out" / "flaeche.png"))
        ug = np.array(Image.open(Path(t) / "out" / "untergrund.png"))
        be = np.array(Image.open(Path(t) / "out" / "begehbar.png"))
        px = lambda a, x, z: a[int(z * 10), int(x * 10)]
        assert fl.shape == (H, W) and fl.dtype == np.uint8
        assert px(fl, 5, 5) == 0 and px(fl, 12, 12) == 3 and px(fl, 15.5, 5) == 1
        assert px(fl, 15.5, 15) == 4, "Wasser muss Weg ueberschreiben"
        assert px(fl, 15.15, 15) == 1 and px(fl, 15.25, 15) == 4   # Kante 15,2 m an Pixelmitten
        assert px(ug, 5, 5) == 1 and px(ug, 55, 55) == 2 and px(ug, 30, 15) == 0 and px(ug, 12, 12) == 0
        assert px(ug, 15.5, 5) == 1                                 # Weg behaelt Untergrund [A]
        assert bool(px(be, 5, 5)) and not bool(px(be, 30, 15)) and not bool(px(be, 12, 12))
        assert info["untergrund_quelle"].startswith("Polygone")
        wt = np.array(Image.open(Path(t) / "out" / "weg_typ.png")); leg = {v_: int(k) for k, v_ in info["weg_typen"]["legende"].items()}
        assert px(fl, 60.5, 2) == 1 and px(fl, 70.5, 2) == 1 and px(fl, 63, 7) == 1
        assert px(wt, 60.5, 2) == leg["GASSE"] and px(wt, 61.5, 7) == leg["GASSE"] and px(wt, 63, 7) == leg["HAUSWEG"]  # GASSE gewinnt
        assert px(wt, 70.5, 2) == leg["NEUTYP"] and px(wt, 15.5, 5) == 0 and px(wt, 5, 5) == 0
        assert info["weg_typen"]["polygone"] == {"GASSE": 1, "HAUSWEG": 1, "NEUTYP": 1}
        bz = np.array(Image.open(Path(t) / "out" / "bauzone.png")).astype(bool); sz = np.array(Image.open(Path(t) / "out" / "slot_zonen.png"))
        assert px(bz, 1.05, 1.05) and px(bz, 2.95, 1.95) and not px(bz, 3.05, 1.5) and not px(bz, 0.95, 1.5) and bz.sum() == 200
        assert px(sz, 3.5, 3.5) == 1 and px(sz, 4.5, 4.5) == 2 and px(sz, 5.95, 4.05) == 2 and px(sz, 6.05, 4.5) == 0 and (sz > 0).sum() == 300
        assert info["bauzone"]["zellen"] == 2 and info["slot_zonen"]["slot_deko"]["zellen"] == 2
        assert info["abgleich_slots"]["abweichung"] is True                     # Fake-Zellen weichen von slot.png ab
        # GASSE ausserhalb wege.geojson und falsches flaeche_m2/Zellformat bleiben Fehler
        for feats_, msg in [([{"type": "Feature", "properties": {"id": "x", "klasse": "GASSE"}, "geometry": {"type": "Polygon", "coordinates": [box(1, 1, 2, 2)]}}], "klasse"),
                            ([{"type": "Feature", "properties": {"id": "x", "typ": "bauzone", "zellen": [[1, 1]], "flaeche_m2": 2}, "geometry": {"type": "Point", "coordinates": [1, 1]}}], "flaeche_m2"),
                            ([{"type": "Feature", "properties": {"id": "x", "typ": "bauzone", "zellen": [[1, 400]]}, "geometry": {"type": "Point", "coordinates": [1, 1]}}], "ausserhalb")]:
            (v / "kaputt.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": feats_}))
            try:
                lies_features(v / "kaputt.geojson"); lies_zellen_punkte(v / "kaputt.geojson"); raise AssertionError(f"{msg}-Fehler nicht erkannt")
            except ValueError as e:
                assert msg in str(e), e
        # Schemafehler werden erkannt
        for p, msg in [({"id": "x", "klasse": 7}, "klasse"), ({"id": "y", "klasse": 0, "untergrund": "Eis"}, "untergrund")]:
            (v / "kaputt.geojson").write_text(json.dumps(fc([(p, box(1, 1, 2, 2))])))
            try:
                lies_features(v / "kaputt.geojson"); raise AssertionError(f"{msg}-Fehler nicht erkannt")
            except ValueError as e:
                assert msg in str(e)
        (v / "kaputt.geojson").write_text(json.dumps(fc([({"id": "e", "klasse": 0}, box(0, 0, 400, 10))])))
        try:
            lies_features(v / "kaputt.geojson"); raise AssertionError("Einheitenfehler nicht erkannt")
        except ValueError as e:
            assert "ausserhalb" in str(e)
        (v / "kaputt.geojson").unlink()
        selbsttest_mesh(Path(t), v)
    print("selbsttest ok")


def _glb(prims: list[dict]) -> bytes:
    """Minimaler glb-Schreiber fuer den Selbsttest: prims = [{pos (n,3) float32, idx (m,) uint32, fl (n,) uint8|float32|None}]."""
    import struct
    binb, views, accs, gp = bytearray(), [], [], []

    def add(arr, ct, typ, target):
        b = arr.tobytes(); views.append({"buffer": 0, "byteOffset": len(binb), "byteLength": len(b), "target": target})
        accs.append({"bufferView": len(views) - 1, "componentType": ct, "count": len(arr) if arr.ndim == 1 else arr.shape[0], "type": typ})
        binb.extend(b + b"\0" * ((4 - len(b) % 4) % 4)); return len(accs) - 1
    for p in prims:
        a = {"POSITION": add(p["pos"].astype(np.float32), 5126, "VEC3", 34962)}
        if p.get("fl") is not None:
            a["_FLAECHE"] = add(p["fl"], 5126 if p["fl"].dtype == np.float32 else 5121, "SCALAR", 34962)
        gp.append({"attributes": a, "indices": add(p["idx"].astype(np.uint32), 5125, "SCALAR", 34963), "mode": 4})
    js = json.dumps({"asset": {"version": "2.0"}, "buffers": [{"byteLength": len(binb)}], "bufferViews": views, "accessors": accs,
                     "meshes": [{"primitives": gp}], "nodes": [{"mesh": 0}], "scenes": [{"nodes": [0]}], "scene": 0}).encode()
    js += b" " * ((4 - len(js) % 4) % 4)
    return (struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(binb)) + struct.pack("<II", len(js), 0x4E4F534A) + js
            + struct.pack("<II", len(binb), 0x004E4942) + bytes(binb))


def _quads(liste) -> dict:
    """Quads mit Aufwaerts-Wicklung (glTF CCW von oben): (p0,p3,p1), (p1,p3,p2)."""
    pos, idx, fl = [], [], []
    for x0, z0, x1, z1, f, k in liste:
        b = len(pos)
        for x, z in [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]:
            pos.append((x, f(x, z), z)); fl.append(k)
        idx += [b, b + 3, b + 1, b + 1, b + 3, b + 2]
    return {"pos": np.array(pos, np.float32), "idx": np.array(idx, np.uint32), "fl": np.array(fl, np.uint8)}


def selbsttest_mesh(t: Path, vektor: Path) -> None:
    """Fake-Manifest (2 Kacheln + Bruecke), gleiche Geometrie wie test/query.test.mjs."""
    import math
    from PIL import Image
    st, f30 = math.tan(math.radians(40)), math.tan(math.radians(30))
    md = t / "mesh"; (md / "kacheln").mkdir(parents=True); (md / "modelle").mkdir()
    a1 = _quads([(0, 0, 20, 43, lambda x, z: 0, 0), (20, 0, 25, 43, lambda x, z: (x - 20) * st, 0),
                 (25, 0, 30, 43, lambda x, z: (x - 25) * f30, 0), (30, 0, 42, 43, lambda x, z: -0.3, 4)])
    a1["fl"] = a1["fl"].astype(np.float32)                         # float-_FLAECHE pruefen
    # A2: Weg 0,1 m; F10: Spiegel 0,05 m steckt im Weg (x 0-10) -> Gelaende; Spiegel 0,2 m ueber Weg (x 20-30) -> Wasser
    a2 = _quads([(0, 43, 42, 86, lambda x, z: 0.1, 1), (0, 43, 10, 86, lambda x, z: 0.05, 4), (20, 43, 30, 86, lambda x, z: 0.2, 4)])
    br = _quads([(33, 10.5, 39, 12.5, lambda x, z: 0.45, 5), (32, 10, 40, 13, lambda x, z: 0.5, 5), (32, 10, 40, 10.1, lambda x, z: 1.5, 5)])
    br["fl"] = None
    (md / "kacheln" / "A1.glb").write_bytes(_glb([a1])); (md / "kacheln" / "A2.glb").write_bytes(_glb([a2]))
    (md / "modelle" / "bruecke_E2.glb").write_bytes(_glb([br]))
    man = {"version": 1, "einheit": "m", "ursprung": "weltecke", "karte": {"breite": 336, "tiefe": 303},
           "klassen": {"0": "grund", "1": "weg", "2": "ufer", "3": "fels_klippe", "4": "wasser", "5": "bruecke"},
           "attribute": {"flaeche": "_FLAECHE"}, "uv": {"TEXCOORD_0": "welt_xz_m", "TEXCOORD_1": "karte_norm", "TEXCOORD_2": "wegband"},
           "kacheln": [{"id": "A1", "glb": "kacheln/A1.glb", "bbox": [0, 0, 42, 43], "dreiecke": 8},
                       {"id": "A2", "glb": "kacheln/A2.glb", "bbox": [0, 43, 42, 86], "dreiecke": 6}],
           "modelle": [{"id": "bruecke_E2", "glb": "modelle/bruecke_E2.glb", "klasse": 5}]}
    (md / "manifest.json").write_text(json.dumps(man))
    # Vektoren passend: Wasser x30-42 z0-43, Weg in A2
    for n in list(vektor.glob("*.geojson")):
        n.unlink()
    poly = lambda x0, z0, x1, z1: [[x0, z0], [x1, z0], [x1, z1], [x0, z1], [x0, z0]]
    feats = [({"id": "g", "klasse": 0, "untergrund": "Schnee"}, poly(0, 0, NX, NY)), ({"id": "w", "klasse": 4}, poly(30, 0, 42, 43)),
             ({"id": "s", "klasse": 1}, poly(0, 43, 42, 86)), ({"id": "f10a", "klasse": 4}, poly(0, 43, 10, 86)),
             ({"id": "f10b", "klasse": 4}, poly(20, 43, 30, 86))]
    (vektor / "zonen.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": p, "geometry": {"type": "Polygon", "coordinates": [c]}} for p, c in feats]}))
    out = t / "out_mesh"
    info = baue(vektor, out, md / "manifest.json")
    fl = np.array(Image.open(out / "flaeche.png")); be = np.array(Image.open(out / "begehbar.png")).astype(bool)
    ug = np.array(Image.open(out / "untergrund.png")); hw = np.array(Image.open(out / "hoehe.png")).astype(float)
    hm = info["hoehe"]; h = hm["offset_m"] + hw * hm["skala_m"]
    px = lambda a, x, z: a[int(z * 10), int(x * 10)]
    assert info["mesh"]["gemischte_dreiecke"] == 0 and not info["mesh"]["vollstaendig"]
    assert px(fl, 5, 5) == 0 and px(be, 5, 5) and abs(px(h, 5, 5)) < 1e-3
    assert not px(be, 22, 20) and abs(px(h, 22.05, 20.05) - 2.05 * st) < 2e-3      # 40 Grad: nicht begehbar
    assert px(be, 27, 20)                                                         # 30 Grad: begehbar
    assert px(fl, 35, 30) == 4 and not px(be, 35, 30) and abs(px(h, 35, 30) + 0.3) < 1e-3
    for x, z in [(36.05, 11.55), (32.55, 10.75), (36.05, 10.05)]:                  # Deck statt Traeger/Handlauf/Wasser
        assert px(fl, x, z) == 5 and px(be, x, z) and abs(px(h, x, z) - 0.5) < 1e-3 and px(ug, x, z) == 0, (x, z, px(h, x, z))
    assert px(fl, 10, 50) == 1 and px(be, 10, 50)
    # F10: Spiegel im Gelaende -> Gelaende-Klasse/-Hoehe; Spiegel ueber Gelaende -> Wasser
    assert px(fl, 5, 50) == 1 and px(be, 5, 50) and abs(px(h, 5, 50) - 0.1) < 1e-3, (px(fl, 5, 50), px(h, 5, 50))
    assert px(fl, 25, 50) == 4 and not px(be, 25, 50) and abs(px(h, 25, 50) - 0.2) < 1e-3
    assert info["f10_wasser_zu_gelaende_px"] == 100 * 430 and info["f10_quelle"]["spiegel_im_gelaende_px"] == 100 * 430
    assert px(be, 100, 100) == 0 and info["mesh"]["ohne_mesh_px"] > 0            # ausserhalb der Fake-Kacheln kein Mesh
    ab = json.loads((out / "abgleich_begehbar_3d.json").read_text())
    assert {"abweichend", "anteil", "warnung", "je_kachel"} <= ab.keys() and ab["warnung"] is True   # Fake-Karte weicht ab
    meta = json.loads((out / "masken_meta.json").read_text())
    assert meta["hoehe"]["skala_m"] == 0.001 and meta["mesh"]["deck"][0]["id"] == "bruecke_E2"
    # Schema-/Dreiecksfehler
    import mesh_raster as MR
    man["kacheln"][0]["dreiecke"] = 9; (md / "manifest.json").write_text(json.dumps(man))
    try:
        MR.lade_mesh(md / "manifest.json"); raise AssertionError("dreiecke-Fehler nicht erkannt")
    except ValueError as e:
        assert "dreiecke" in str(e)
    man["kacheln"][0]["dreiecke"] = 8; man["einheit"] = "zelle"; (md / "manifest.json").write_text(json.dumps(man))
    try:
        MR.lade_mesh(md / "manifest.json"); raise AssertionError("Schemafehler nicht erkannt")
    except ValueError as e:
        assert "einheit" in str(e)
    print("selbsttest_mesh ok", json.dumps({k: info[k] for k in ("hoehe", "abgleich_begehbar_3d")}))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pruefe-quellen", action="store_true")
    ap.add_argument("--selbsttest", action="store_true")
    ap.add_argument("--vektor", type=Path, default=DV2 / "vektor")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--ohne-mesh", action="store_true", help="flaeche/untergrund/begehbar ohne Mesh (kein hoehe.png)")
    ap.add_argument("--manifest", type=Path, default=MESH_MANIFEST)
    a = ap.parse_args()
    if a.selbsttest:
        selbsttest(); return
    fehlt = pruefe_quellen(a.vektor, None if a.ohne_mesh else a.manifest)
    if a.pruefe_quellen or not a.out:
        sys.exit(2 if fehlt else 0)
    if fehlt:
        print(f"Abbruch: Quellen fehlen {fehlt} (s. STATUS.md). Keine Masken erzeugt.", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(baue(a.vektor, a.out, None if a.ohne_mesh else a.manifest), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

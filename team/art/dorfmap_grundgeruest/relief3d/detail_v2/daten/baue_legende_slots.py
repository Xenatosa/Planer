#!/usr/bin/env python3
"""P4 detail_v2 Datenschicht: legende.json + slots.json aus den Alt-Quellen (Do-Teil, ohne Vektoren/Mesh).

Aufruf (aus diesem Ordner):
    python3 baue_legende_slots.py                       # schreibt legende.json, slots.json
    python3 baue_legende_slots.py --slot-png /tmp/dv2_daten/slot.png   # zusaetzlich slot.png (NICHT committen, s. STATUS.md)
    python3 baue_legende_slots.py --pruefe              # nur pruefen, ob legende.json/slots.json aktuell sind

Quellen (Pfad + Git-Blob-SHA stehen im Ergebnis unter "quellen"):
  - ../../../raster_c20_z25_overlay_plaetze_wege.csv  (platz, bauplatz, dekoplaetze_netz)  [S]
  - ../../zellen_relief.csv                           (deko_baum_ok, deko_fels_ok, untergrund) [S]
  - ../../../raster_c20_z25_meta.json                 (Sollzahlen plaetze=99, dekoplaetze_netz=627) [S]
Zelle (cx, cy) = Weltquadrat x in [cx, cx+1), z in [cy, cy+1) (main.js zelle(): floor(x), floor(z)) [S].
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
RELIEF = HIER.parent.parent                      # relief3d/
GG = RELIEF.parent                               # dorfmap_grundgeruest/
Q_OVERLAY = GG / "raster_c20_z25_overlay_plaetze_wege.csv"
Q_ZELLEN = RELIEF / "zellen_relief.csv"
Q_META = GG / "raster_c20_z25_meta.json"

NX, NY = 336, 303            # Zellen = Meter [S]
PX_PRO_M = 10                # 0,1 m/px [F ueber Plan 3.3]
W, H = NX * PX_PRO_M, NY * PX_PRO_M

# slot.png 16 bit: Bitbelegung abgestimmt [F ueber Grundgeruest 19.11.2026]
BIT_ID = 0x0FFF              # Bits 0-11: Slot-ID (0 = kein Slot)
BIT_DEKO_BAUM = 1 << 12      # Zelle deko_baum_ok=1 (Alt-Abgleich)
BIT_DEKO_FELS = 1 << 13      # Zelle deko_fels_ok=1 (Alt-Abgleich)
BIT_BAUPLATZ = 1 << 14       # Zelle bauplatz=1 innerhalb eines Platzes
ID_PLATZ_START = 1           # 1..999 Plaetze/Bauplaetze
ID_DEKO_START = 1001         # 1001..  Deko-Netz-Slots (je Zelle ein Slot)


def git_blob(p: Path) -> str:
    try:
        rel = p.resolve().relative_to(Path(subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], cwd=HIER, text=True).strip()))
        return subprocess.check_output(["git", "rev-parse", f"HEAD:{rel}"], cwd=HIER, text=True).strip()
    except Exception:
        return "unbekannt"


def quelle(p: Path) -> dict:
    return {"pfad": str(p.relative_to(GG.parent.parent.parent)), "git_blob": git_blob(p),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def lies_csv(p: Path, spalten: list[str]) -> list[dict]:
    with p.open(newline="", encoding="utf-8") as f:
        return [{k: r[k] for k in spalten} for r in csv.DictReader(f)]


def baue() -> tuple[dict, dict, dict]:
    ov = lies_csv(Q_OVERLAY, ["cx", "cy", "zone", "platz", "bauplatz", "hof", "feuer", "dekoplaetze_netz"])
    ze = lies_csv(Q_ZELLEN, ["cx", "cy", "untergrund", "deko_baum_ok", "deko_fels_ok"])
    meta = json.loads(Q_META.read_text(encoding="utf-8"))

    flags: dict[tuple[int, int], int] = {}
    ug_zaehl: dict[str, int] = {}
    for r in ze:
        c = (int(r["cx"]), int(r["cy"]))
        f = (BIT_DEKO_BAUM if r["deko_baum_ok"] == "1" else 0) | (BIT_DEKO_FELS if r["deko_fels_ok"] == "1" else 0)
        if f:
            flags[c] = f
        ug_zaehl[r["untergrund"]] = ug_zaehl.get(r["untergrund"], 0) + 1
    if len(ze) != NX * NY:
        sys.exit(f"zellen_relief.csv: {len(ze)} Zeilen statt {NX*NY}")

    plaetze: dict[str, list] = {}
    deko: list[tuple[int, int]] = []
    for r in ov:
        c = (int(r["cx"]), int(r["cy"]))
        if r["platz"]:
            plaetze.setdefault(r["platz"], []).append((c, r))
        if r["dekoplaetze_netz"] == "1":
            deko.append(c)

    slots = []
    zell_slot: dict[tuple[int, int], int] = {}
    for i, pid in enumerate(sorted(plaetze)):
        sid = ID_PLATZ_START + i
        zellen = sorted(plaetze[pid], key=lambda t: (t[0][1], t[0][0]))
        bp = [c for c, r in zellen if r["bauplatz"] == "1"]
        zonen = sorted({r["zone"] for _, r in zellen if r["zone"]})
        for c, r in zellen:
            if c in zell_slot:
                sys.exit(f"Zelle {c} doppelt belegt")
            zell_slot[c] = sid | (BIT_BAUPLATZ if r["bauplatz"] == "1" else 0)
        xs = [c[0] for c, _ in zellen]; zs = [c[1] for c, _ in zellen]
        slots.append({
            "id": sid, "art": "bauplatz" if bp else "platz", "name": pid, "zone": zonen,
            "zellen": len(zellen), "bauplatz_zellen": len(bp),
            "hof_zellen": sum(r["hof"] == "1" for _, r in zellen),
            "feuer_zellen": sum(r["feuer"] == "1" for _, r in zellen),
            "bbox_m": [min(xs), min(zs), max(xs) + 1, max(zs) + 1],
            "schwerpunkt_m": [round(sum(xs) / len(xs) + 0.5, 3), round(sum(zs) / len(zs) + 0.5, 3)],
            "zellen_liste": [[c[0], c[1]] for c, _ in zellen],
        })
    for j, c in enumerate(sorted(deko, key=lambda t: (t[1], t[0]))):
        sid = ID_DEKO_START + j
        if c in zell_slot:
            sys.exit(f"Deko-Zelle {c} liegt in Platz-Slot {zell_slot[c]}")
        zell_slot[c] = sid
        slots.append({"id": sid, "art": "deko", "name": f"DK{j+1:04d}", "zellen": 1,
                      "bbox_m": [c[0], c[1], c[0] + 1, c[1] + 1],
                      "schwerpunkt_m": [c[0] + 0.5, c[1] + 0.5],
                      "deko_baum_ok": bool(flags.get(c, 0) & BIT_DEKO_BAUM),
                      "deko_fels_ok": bool(flags.get(c, 0) & BIT_DEKO_FELS),
                      "zellen_liste": [[c[0], c[1]]]})
    max_id = max(s["id"] for s in slots)
    if max_id > BIT_ID:
        sys.exit(f"Slot-ID {max_id} passt nicht in 12 bit")

    # Abgleich gegen Sollzahlen der Meta [S]
    n_platz = sum(s["art"] != "deko" for s in slots)
    n_deko = sum(s["art"] == "deko" for s in slots)
    n_bp_z = sum(s.get("bauplatz_zellen", 0) for s in slots)
    abgleich = {
        "plaetze": {"ist": n_platz, "soll_meta": meta["plaetze"], "ok": n_platz == meta["plaetze"]},
        "dekoplaetze_netz": {"ist": n_deko, "soll_meta": meta["dekoplaetze_netz"], "ok": n_deko == meta["dekoplaetze_netz"]},
        "bauplatz_zellen": {"ist": n_bp_z, "soll_plan_abschnitt_2": 3292, "ok": n_bp_z == 3292},
    }
    quellen = {"overlay": quelle(Q_OVERLAY), "zellen_relief": quelle(Q_ZELLEN), "meta": quelle(Q_META)}

    slots_json = {
        "schema": "dv2-slots/1",
        "hinweis": "Erzeugt von baue_legende_slots.py. Zellen = 1 m, Weltquadrat [cx,cx+1) x [cy,cy+1).",
        "quellen": quellen, "abgleich": abgleich,
        "zaehlung": {"plaetze_gesamt": n_platz,
                     "bauplaetze": sum(s["art"] == "bauplatz" for s in slots),
                     "plaetze_ohne_bauplatzzelle": [s["name"] for s in slots if s["art"] == "platz"],
                     "deko_slots": n_deko, "bauplatz_zellen": n_bp_z},
        "slots": slots,
    }

    legende = {
        "schema": "dv2-datenschicht/1",
        "stand": "P4 Do-Geruest; Masken aus Vektoren/Mesh folgen Fr (s. STATUS.md)",
        "massstab": {
            "einheit": "1 Viewer-Einheit = 1 Zelle = 1 m [S]",
            "px_pro_m": PX_PRO_M, "m_pro_px": 1 / PX_PRO_M,
            "raster_px": [W, H], "welt_m": [NX, NY],
            "ursprung": "(0,0) = Weltecke x=0, z=0; px = floor(x*10), py = floor(z*10); Zeile py waechst mit z",
            "uv1": "UV1 = (x/336, z/303); px = u*3360, py = v*3030 (deckungsgleich)",
            "pixelmitte_m": "x = (px+0.5)/10, z = (py+0.5)/10",
            "rand": "x=336 bzw. z=303 (Kartenrand) wird auf das letzte Pixel geklemmt; ausserhalb [0,336]x[0,303] = Fehler",
            "vektor_json_umrechnung": "neu/vektor.json rechnet 1,2 m/Zelle (zellweite_m): Werte durch 1,2 teilen [S]",
        },
        "dateien": {
            "flaeche.png": {"format": "PNG 8 bit Graustufe, 1 Kanal, Wert = Klassen-Index", "status": "offen (Fr, aus Vektoren+Mesh)"},
            "begehbar.png": {"format": "PNG 1 bit Graustufe, 1 = begehbar", "status": "offen (Fr)"},
            "slot.png": {"format": "PNG 16 bit Graustufe, Bitfeld s. slot_bits", "status": "fertig, committet (zellbasiert, Freigabe Grundgeruest 19.11.2026)"},
            "hoehe.png": {"format": "PNG 16 bit Graustufe, hoehe_m = offset_m + wert * skala_m", "offset_m": None, "skala_m": None,
                          "status": "offen (Fr, aus Mesh gerastert); offset/skala werden beim Rastern eingetragen"},
            "untergrund.png": {"format": "PNG 8 bit Graustufe, Wert = untergrund-Code (s. untergrund.codes)",
                               "quelle": "zonen.geojson Property untergrund (Polygone); 1-m-Fallback zellen_relief.csv nur falls fehlend",
                               "status": "abgestimmt als Zusatzdatei [F ueber Grundgeruest 19.11.2026], Erzeugung Fr"},
        },
        "flaeche": {
            "prioritaet": ["wasser", "bruecke", "weg", "ufer", "fels_klippe", "grund"],
            "prioritaet_quelle": "Plan 3.1 / Auftrag P4: Wasser > Bruecke > Weg > Ufer > Fels/Klippe > Grund [F ueber Plan]",
            "klassen": [
                {"wert": 0, "name": "grund", "label": "Wiese/Grund", "farbe": "#c8d8b0"},
                {"wert": 1, "name": "weg", "label": "Weg", "farbe": "#b08a5a"},
                {"wert": 2, "name": "ufer", "label": "Ufer", "farbe": "#d8c890"},
                {"wert": 3, "name": "fels_klippe", "label": "Fels/Klippe", "farbe": "#7a7a80"},
                {"wert": 4, "name": "wasser", "label": "Wasser", "farbe": "#3a78c8"},
                {"wert": 5, "name": "bruecke", "label": "Bruecke", "farbe": "#8a4a20"},
            ],
            "farben_hinweis": "Farben nur fuer Debug-/Legendenbilder, keine Texturen [A]",
            "quelle": "detail_v2/vektor/*.geojson: FeatureCollection, Viewer-Meter, Properties klasse (0-5), untergrund, id [F ueber Grundgeruest 19.11.2026]",
            "mesh_attribut": "P2-glTF: Vertex-Attribut _FLAECHE (0-5), Dreiecke an Kanten klassenrein, Klassenliste im manifest [F ueber Grundgeruest 19.11.2026]",
        },
        "untergrund": {
            "hinweis": "Untertyp der Flaeche. Quelle zonen.geojson Property untergrund (Schnee/Wald/Boden/Sand) [F ueber Grundgeruest]; 0 wo flaeche wasser/fels_klippe/bruecke [A]; Alt-Werte zellen_relief.csv nur Fallback [S]",
        "status": "abgestimmt",
            "codes": [
                {"wert": 0, "name": None, "label": "kein Untertyp (Wasser, Fels/Klippe, Bruecke)", "farbe": "#000000"},
                {"wert": 1, "name": "schnee", "label": "Schnee", "farbe": "#f2f4f8", "alt": ["SCHNEE"]},
                {"wert": 2, "name": "wald", "label": "Wald", "farbe": "#3c6a3c", "alt": ["WALD"]},
                {"wert": 3, "name": "boden", "label": "Boden", "farbe": "#8a6a4a", "alt": ["BODEN"]},
                {"wert": 4, "name": "sand", "label": "Sand", "farbe": "#e0cc90", "alt": ["SAND"]},
            ],
            "alt_ohne_untertyp": {"WASSER_EIS": "flaeche wasser", "FELS": "flaeche fels_klippe",
                                  "KLIPPE_WAND": "flaeche fels_klippe", "KLIPPE_KANTE": "flaeche fels_klippe"},
            "alt_zaehlung_zellen": dict(sorted(ug_zaehl.items(), key=lambda t: -t[1])),
        },
        "begehbar": {"werte": {"0": "nicht begehbar", "1": "begehbar"},
                     "regel": "offen: aus Mesh-Neigung + Flaeche (Wasser/Fels nicht begehbar, Bruecke begehbar); Alt-Abgleich begehbar_3d [A]"},
        "slot_bits": {
            "id_maske": BIT_ID, "deko_baum_ok": BIT_DEKO_BAUM, "deko_fels_ok": BIT_DEKO_FELS, "bauplatz_zelle": BIT_BAUPLATZ,
            "reserviert": 1 << 15,
            "id_bereiche": {"platz": [ID_PLATZ_START, ID_PLATZ_START + n_platz - 1],
                            "deko": [ID_DEKO_START, ID_DEKO_START + n_deko - 1]},
            "status": "abgestimmt (Grundgeruest 19.11.2026): Bit 0-11 ID, 12 Baum, 13 Fels, 14 Bauplatz-Zelle, 15 reserviert (immer 0)",
            "hinweis": "deko_baum_ok/deko_fels_ok sind Zell-Eignungen (1 m) und gelten auch ausserhalb von Slots",
        },
        "slots": {
            "datei": "slots.json",
            "quelle_bauplaetze": "Overlay platz (99 Plaetze) + bauplatz (3292 Zellen) [S]",
            "quelle_deko": "Overlay dekoplaetze_netz (627 Zellen = 627 Slots), Eignung deko_baum_ok/deko_fels_ok aus zellen_relief.csv [S]",
            "zaehlung": slots_json["zaehlung"], "abgleich": abgleich,
        },
        "kacheln": {
            "schema": "56 Kacheln A-H x 1-7; Buchstabe = Spalte in x, Zahl = Zeile in z [S baue_alle_kacheln.py]",
            "spalte_m": 42, "zeile_m": 43,
            "schnitte_x": [42 * i for i in range(9)], "schnitte_z": [43 * j for j in range(7)] + [303],
            "regel": "Spalte = min(floor(x/42),7) -> A..H; Zeile = min(floor(z/43),6)+1; Zeile 7 reicht bis z=303 (z 301-303 angehaengt, P10b) [S]",
            "schnittlinie": "Punkt genau auf x=42*i bzw. z=43*j gehoert zur hoeheren Kachel; Kartenrand x=336/z=303 zur letzten [A]",
        },
        "quellen": quellen,
    }
    return legende, slots_json, zell_slot


def schreibe_slot_png(zell_slot: dict, flags: dict, ziel: Path) -> None:
    import numpy as np
    from PIL import Image
    zell = np.zeros((NY, NX), np.uint16)
    for (cx, cy), f in flags.items():
        zell[cy, cx] |= f
    for (cx, cy), v in zell_slot.items():
        zell[cy, cx] |= v
    px = np.kron(zell, np.ones((PX_PRO_M, PX_PRO_M), np.uint16))
    assert px.shape == (H, W)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(px).save(ziel)  # Pillow: uint16 -> PNG 16 bit Graustufe
    chk = np.array(Image.open(ziel))
    assert chk.dtype == np.uint16 and (chk == px).all(), "slot.png Rueckleseprobe fehlgeschlagen"


def dump(o) -> str:
    return json.dumps(o, ensure_ascii=False, indent=1) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot-png", type=Path)
    ap.add_argument("--pruefe", action="store_true")
    a = ap.parse_args()
    legende, slots_json, zell_slot = baue()
    out = {HIER / "legende.json": dump(legende), HIER / "slots.json": json.dumps(slots_json, ensure_ascii=False, separators=(",", ":")) + "\n"}
    if a.pruefe:
        alt = [p.name for p, t in out.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
        print("aktuell" if not alt else f"veraltet: {alt}")
        sys.exit(1 if alt else 0)
    for p, t in out.items():
        p.write_text(t, encoding="utf-8")
    z = slots_json["zaehlung"]
    print(f"Plaetze {z['plaetze_gesamt']} (Bauplaetze {z['bauplaetze']}), Deko-Slots {z['deko_slots']}, Bauplatz-Zellen {z['bauplatz_zellen']}")
    print("Abgleich:", {k: v["ok"] for k, v in slots_json["abgleich"].items()})
    if a.slot_png:
        flags = {}
        for r in lies_csv(Q_ZELLEN, ["cx", "cy", "deko_baum_ok", "deko_fels_ok"]):
            f = (BIT_DEKO_BAUM if r["deko_baum_ok"] == "1" else 0) | (BIT_DEKO_FELS if r["deko_fels_ok"] == "1" else 0)
            if f:
                flags[(int(r["cx"]), int(r["cy"]))] = f
        schreibe_slot_png(zell_slot, flags, a.slot_png)
        print("slot.png:", a.slot_png, a.slot_png.stat().st_size, "Byte")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""P10: Lochscan-Ergebnis(se) von pruefung/loch_o18g.js je Kachel auswerten (JSON + Markdown).

Aufruf: python3 pruefung/alle_kacheln/loch_auswertung.py LAUF.json [LAUF2.json ...] --out ERG.json --md ERG.md
Mehrere Laeufe (z. B. Kachelgruppen ueber Q=?kacheln=...) werden summiert; doppelte Punkte
(gleiche Koordinate) werden nur einmal gezaehlt. Kachelzuordnung wie pruefe_regeln.feld().
"""
import argparse, json
from pathlib import Path

BUCHST = "ABCDEFGH"


def feld(x, z):
    return BUCHST[int(min(max(x // 42, 0), 7))] + str(int(min(max(z // 43, 0), 6)) + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("laeufe", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--md", required=True)
    ap.add_argument("--titel", default="P10 Lochscan alle 56 Kacheln")
    ap.add_argument("--basis", default="")
    a = ap.parse_args()
    je = {f"{c}{r}": 0 for r in range(1, 8) for c in BUCHST}
    punkte, gesehen, laeufe = [], set(), []
    for p in a.laeufe:
        d = json.loads(Path(p).read_text())
        laeufe.append({"datei": p, "meshes": d["meshes"], "dreiecke": d["dreiecke"],
                       "offen_innen": d["offen_innen"], "bb": d["bb"]})
        for x, y, z in d["punkte"]:
            k = (x, y, z)
            if k in gesehen:
                continue
            gesehen.add(k)
            t = feld(x, z)
            je[t] += 1
            punkte.append({"kachel": t, "x": x, "y": y, "z": z})
    summe = sum(je.values())
    if summe != len(punkte):
        raise SystemExit("Summenfehler")
    if len(a.laeufe) == 1 and summe != laeufe[0]["offen_innen"]:
        raise SystemExit(f"Summe {summe} != offen_innen {laeufe[0]['offen_innen']}")
    erg = {"titel": a.titel, "basis": a.basis, "regel": "R5_loch (offene Innenkanten, loch_o18g.js unveraendert)",
           "laeufe": laeufe, "summe": summe, "je_kachel": je,
           "top": sorted(((t, n) for t, n in je.items() if n), key=lambda x: (-x[1], x[0]))[:10],
           "punkte": sorted(punkte, key=lambda p: (p["kachel"], p["x"], p["z"]))}
    Path(a.out).write_text(json.dumps(erg, ensure_ascii=False, indent=1) + "\n")
    L = [f"# {a.titel}", ""]
    if a.basis:
        L += [f"Basis: {a.basis}", ""]
    L += ["Regel: R5_loch = offene Kanten (nur 1 Dreieck) aller sichtbaren Meshes der Ebene `gelaende`, "
          "global 2 cm verschweisst, Kartenrand 0,6 ausgenommen (`pruefung/loch_o18g.js`, unveraendert).", ""]
    for l in laeufe:
        dr = f"{l['dreiecke']:,}".replace(",", ".")
        L.append(f"- Lauf `{l['datei']}`: {l['meshes']} Meshes, {dr} Dreiecke, offen_innen {l['offen_innen']}, bb {l['bb']}")
    L += ["", f"**Summe R5_loch: {summe}**", "", "| Zeile | " + " | ".join(BUCHST) + " |", "|---|" + "---|" * 8]
    for r in range(1, 8):
        L.append(f"| {r} | " + " | ".join(str(je[f'{c}{r}']) for c in BUCHST) + " |")
    L += ["", "## Trefferliste", ""]
    if punkte:
        L += ["| Kachel | x | y | z |", "|---|---|---|---|"]
        L += [f"| {p['kachel']} | {p['x']} | {p['y']} | {p['z']} |" for p in erg["punkte"]]
    else:
        L.append("Keine Treffer.")
    Path(a.md).write_text("\n".join(L) + "\n")
    print(json.dumps({"summe": summe, "top": erg["top"], "laeufe": len(laeufe)}))


if __name__ == "__main__":
    main()

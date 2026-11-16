# P10d – Wandhöhen an das sichtbare Gelände gebunden, neue Prüfregel W1

Basis `art/dorfmap-fertig` @ d181fa6, Auftrag Dorfmap-Grundgerüst. Geändert: `neu/wand.py` (Mesh-Bau), neue Regel
`pruefung/w1_wand.py` + ein Aufruf in `pruefung/export_gate.sh`, W1-Abschnitt in `REGELN_VERPFLICHTEND.md`,
`pruefung/alle_kacheln/baue_alle_kacheln.py` (ruft dieselbe Bindung für alle 56 Kacheln), Trefferkarte liest W1 optional.
Wandteil in `neu/relief_neu.json.gz` + NEU_GZ-Zeile in `index.html`/`neu/index.html` über den Einsetz-Weg
`pruefung/p10c/waende_einsetzen.py` neu gesetzt (Bundle bytegleich; `neu/pipeline.py`/p3d17 nicht angefasst).
Unverändert (sha256 vorher = nachher): `neu/vektor.json` (aac6afff…), `zellen_relief.csv`, `neu/zellen_relief.csv`,
`neu/felder.json`, `gen_relief.py`, `neu/gen_relief.py`, alle vorhandenen Prüfer (`pruefung/*.py`, `loch_o18g.js`).

## Methode Höhenbindung (`neu/wand.py`, `bind_chunk_to_terrain`, `_network_solid`)
Je Station der (Chaikin-geglätteten, an die Kachel geclippten) Mittellinie, alles in Zellen wie das Gelände-Mesh:
1. **Nachbarschaft quer zur Linie:** 11 Stützstellen auf der Normalen von −(Breite/2 + 0,5) bis +(Breite/2 + 0,5) Zellen
   (Breite 1,2 m = 1 Zelle → ±1 Zelle), abgetastet auf den gerenderten Gelände-Dreiecken (`_sample_grid`, Diagonale a–d).
   Krone = Maximum, Fuß = Minimum.
2. **Krone glätten:** untere Hülle entlang der Linie (gleitendes Minimum, dann Mittel, je ±1,5 Zellen Bogenlänge),
   nie höher als die lokale Krone – nimmt die Zacken, wo die Linie über die Kante pendelt (H6).
3. **Oberkante = Krone − 0,15 m** (embed); zusätzlich je Kappenvertex höchstens **Gelände darunter + 1,0 m [A]**
   (keine Finnen/Gesimse, die aus dem Hang ragen).
4. **Unterkante = Gelände darunter − 0,15 m** je Kappenvertex (bestehende Fußvariante 2, an jeder Gelände-Dreieckskante
   geteilt) → liegt immer am lokalen Geländefuß oder darunter, kann nicht schweben.
5. **Nicht gebaut (nur nicht gerendert, nichts gelöscht):** ganze Stücke < 1 Zelle (Schnittreste); Stationen mit
   Krone − Fuß < **2,0 m [A]** (keine Geländestufe – Wand läge flach auf/im Gelände und erschiene als dunkler Streifen
   oder flimmernde Punkte, so im ersten Versuch auf D1/C6 gesehen); danach verbleibende Läufe < **3 Zellen [A]**
   (einzelne dunkle Klötze, gesehen in C2/C3/D1). Liste: `ergebnis/nicht_gerendert.json` (56 Kacheln: 297 Einträge,
   davon 16 Schnittreste < 1 Zelle, 232 ohne Stufe, 30 nur Klötze, 19 teilweise; index.html D1/G1: 15).
Parameter stehen als Konstanten oben in `wand.py` und im Manifest (`top_binding`, `top_embed_m`, …).

## W1 (`pruefung/w1_wand.py`, Schwellen/Begründung in `REGELN_VERPFLICHTEND.md`)
Liest die gerenderten Wandkörper aus `index.html` (NEU_GZ), `neu/relief_neu.json.gz` oder einem 56-Kachel-Paket.
W1a außerhalb Karte · W1b > 0,5 m über Krone (Kreis 1,5 Zellen) · W1c Unterkante > 0,5 m über Gelände darunter ·
W1d > 1 Zelle (+ halbe Breite) von den Quellzellen. Exit 1 bei Treffern; `export_gate.sh` setzt dann ROT.
Positivkontrolle: Stand 7944b33 (vor P10c-Einheitenfix) → W1b 140, W1d 461.

**Wichtig:** Im Gate prüft W1 `index.html` (nur D1/G1/D2). Dort lagen die Wände schon vor P10d ganz im Gelände →
W1 0 → 0. Die frei stehenden Wände (C6–H6, A4, C7 …) gibt es nur im 56-Kachel-Viewer; dort W1 1621 → 0
(`python3 pruefung/w1_wand.py /tmp/p10d/alle_nachher/alle_kacheln.json.gz <aus.json>`).

## Ergebnisse (`ergebnis/`)
`gate_vergleich.md` (alle Regeln vorher/nachher, W1-Tabellen, Statistik, Lochscan, D2), `gate_vorher|gate_nachher/`,
`w1_alle56_vorher|nachher.json`, `w1_positivkontrolle_7944b33.json`, `wand_statistik.json`, `nicht_gerendert.json`,
`hash_index_vorher_nachher.json`, `einsetzen.json`, `lochscan_*`, `trefferkarte_vergleich*.png`,
`vergleich_vorher_nachher.png` (C6, F7, H6, A4, C7, D1, G1), `vergleich_nah.png` (H6/C6 nah, Blick Nord/Süd).

## Befehle (relief3d/)
```sh
python3 pruefung/p10c/waende_einsetzen.py                      # Wandteil in relief_neu.json.gz + index.html setzen
O17REF=/tmp/p10c/o17.json.gz sh pruefung/p10d/gate_eigene_pfade.sh index.html /tmp/p10d/gate_nachher
python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/p10d/alle_nachher     # ~30 s (vorher ~7 min)
python3 pruefung/w1_wand.py /tmp/p10d/alle_nachher/alle_kacheln.json.gz /tmp/p10d/w1_alle.json
KONTROLLE=C3 sh pruefung/alle_kacheln/lochscan_alle.sh /tmp/p10d/alle_nachher
NODE_PATH=/tmp/w3/node_modules node pruefung/alle_kacheln/nahbild.js --html /tmp/p10d/alle_nachher/alle_kacheln.html --kachel C6 --out /tmp/p10d/c6.png
python3 pruefung/p10d/wand_statistik.py <vorher.json.gz> <nachher.json.gz>
```

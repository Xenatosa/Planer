# Trefferkarte (P6, Dev UI)

8×7-Raster der Kacheln A–H × 1–7 aus den Gate-JSONs, eingefärbt nach Trefferzahl, mit Aufteilung je Regelfamilie.

**Aufruf** (im Ordner `relief3d/`, nach `sh pruefung/export_gate.sh`):

    python3 pruefung/trefferkarte/trefferkarte.py

Ausgabe hier: `trefferkarte.html` (offline, Umschalter je Familie, Tooltip mit Einzelregeln), `trefferkarte.png`, `trefferkarte.json`. Laufzeit unter 1 s. Nur Python 3 und Pillow (für das PNG).

**Vergleich vorher/nachher:** die drei JSONs eines alten Stands in einen Ordner kopieren, dann

    python3 pruefung/trefferkarte/trefferkarte.py --vorher /pfad/zum/alten_stand

Ergebnis: `vergleich.html` / `vergleich.png` mit Differenz je Kachel (grün weniger, rot mehr).

**Eingaben:** `pruefung/regeln_letzter_lauf.json`, `pruefung/r8_letzter_lauf.json`, `pruefung/r9_letzter_lauf.json` (andere Pfade mit `--regeln --r8 --r9`, Ausgabeordner mit `--aus`). Das Skript liest nur.

**Regelfamilien:** Höhen = `G*`, `R3_*`, `R5_*` · Wege = `R1_*`, `R2_*`, `R6_*` · Texturen = `T*` (alle aus der regeln-Datei) · R8 = alle Treffer der r8-Datei · R9 = alle Treffer der r9-Datei (auch `R8b_delle`) · Sonstige = unbekanntes Präfix (fällt nie still weg).

**Kartenweit:** Treffer ohne gültige Kachel (z. B. `feld = "-"`) stehen in einem eigenen Block unter dem Raster.

**Summenprüfung:** Für jede Datei muss gelten `summe` = Anzahl `treffer` = Summe `je_regel` = Raster + kartenweit. Sonst Exit-Code 1 mit Meldung.

Ausgangsstand 8e374b0: regeln 570 (568 Raster + 2 kartenweit), r8 48, r9 334; Höhen 429, Wege 43, Texturen 98.

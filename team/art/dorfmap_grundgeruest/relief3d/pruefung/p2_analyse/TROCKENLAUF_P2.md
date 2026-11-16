# P2 Trockenlauf (16.11.2026, ca. 07:30 Uhr MEZ, Wege & Deko)

Entscheidung Dorfmap-Grundgerüst (16.11.): Rampen raus (Variante 2), Verbinder D2/F4/E3, G2 nicht schließen, R6 nicht anfassen, relief_daten.json.gz **nicht** neu erzeugen (Kollision L1).
Marker: [S] gemessen, [A] Annahme, [R] gerechnet. Trockenlauf nur in /tmp (eigene detached Worktrees 8e374b0 + geänderte gen_relief.py), keine Repo-Datei überschrieben. **Kein Gate gelaufen** (Vorgabe).

## Änderungen (Commit auf wege/dorfmap-p2)
- `gen_relief.py`
  - `P2_RAMPEN` (Standard 1): `_rampen()` wählt die Rampen wie bisher, schneidet sie aber nicht ins Gelände und legt keinen Rampenweg an (Pfad nur in `RAMP_ENTFERNT` gemerkt). `_serp('X069')` (Gate rampe_12) entfällt. Wand/Hang bleibt wie ohne Rampe.
  - O16 (`runde_o16.entfernen`, Rücken 133|173) läuft weiter auf dem gemerkten Pfad der alten Krater-Rampe (Index 9, Assertion 130,26|198,39 bestanden) → Bereich wie bisher [A].
  - `_anschluss_gang` (Gelände-Gang rampe_1-Ende → Dorfweg) entfällt mit rampe_1, sonst bliebe eine Rinne [A].
  - `P2_X084_RAUS` (Standard 0): X084 (Gate rampe_11) bleibt drin, weil ihre Entnahme D2 ändert (s. u.).
  - `P2_VERBINDER` (Standard 1): liest `p2_verbinder.json` und setzt zusätzliche `weg`-/`br`-Zellen direkt nach dem Einlesen der Wegquelle `../raster_c20_z25_overlay_plaetze_wege.csv` (Spalten weg_id/bruecke). Die Overlay-CSV selbst bleibt unverändert.
  - `P2_D2_LOCK` (Standard 1): setzt D2 (Zellen x126–168, z43–86; GB- und VC-Ausschnitt) am Ende auf `p2_d2_referenz.npz` zurück; prüft vorher, dass die Referenz den Hash 749d3c4b hat.
  - Leer-Schutz für `RAMPPROF`/`RAMPWEGE` (nur nötig bei P2_X084_RAUS=1).
  - Alter Stand: `P2_RAMPEN=0 P2_VERBINDER=0 P2_D2_LOCK=0`.
- `p2_verbinder.json`: P2_D2_bruecke (18 Zellen, Brücke G014 über den Fluss, Zeilen 127–128, x176–184, ganz außerhalb D2), P2_F4 (16 Zellen 246|129→243|136, 2 breit), P2_E3 (30 Zellen 196|112→188|126, 2 breit).
- `p2_d2_referenz.npz`: D2-Ausschnitt GB (sha 749d3c4b…) und VC (b67dc719…) aus relief_daten.json.gz 8e374b0.

## D2-Hash [S]
Der Hash 749d3c4b bezieht sich auf SHA-256 der float32-Höhen GB im D2-Ausschnitt `GB[86:173, 252:337]` (Zellen x126–168, z43–86, rs=2; = `height_sha256` in neu/build.json / neu/mesh.py TILE_BOUNDS). Nachgerechnet auf 8e374b0: 749d3c4b… ✔. Nullprobe: gen_relief.py ohne Änderung neu erzeugt → relief_daten.json.gz bitgleich (5e8fdb51…), Laufzeit 80 s.

| Lauf (ohne D2-Lock) | D2 GB geänderte Ecken | max |
|---|---|---|
| rampe_0–10 + 12 raus, X084 drin | 335 (Zeilen z43–52,5, x126–160) | 8,8 mm |
| zusätzlich X084 raus | 744 | 14,2 mm; X084 allein: 547 Ecken, 14,2 mm |

→ **rampe_11 (X084) bleibt drin** (Entscheidung: nur raus, wenn D2 bitgleich). Die Fernwirkung der übrigen Rampen-Entnahme (≤ 8,8 mm in den oberen D2-Randzeilen, 19 VC-Ecken) fängt der D2-Lock ab: mit Lock D2 GB = 749d3c4b…, VC = b67dc719…, WV/WEGA unverändert [S]. Folge: an der D1|D2-Kante (z=43) entsteht eine Stufe von höchstens 8,8 mm [S], erwartet unsichtbar [A]. **Entscheidung nötig**, ob der Lock so akzeptiert wird.

## Ergebnis Trockenlauf (mit Lock, X084 drin) [S]
- Skript läuft fehlerfrei (exit 0, ca. 70 s). Rampenwege 13 → 1, Wegzellen 2839 → 2900, Brückenzellen 20 → 38.
- GB geändert: 108 184 Ecken, davon > 10 cm 52 915, max 13,3 m (Wand an Stelle der früheren Rampe). Kacheln mit Änderung > 1 cm: B1 C1 D1 E1 F1 G1 B2 C2 F2 B3 C3 D3 E3 G3 B4 C4 D4 E4 G4 H4 B5 C5 D5 H5 C6 D6 E6 F6 G6 H6 C7 F7 G7; D2 0.
- Regenerierte Dateien (nur /tmp): relief_daten.json.gz, zellen_relief.csv, dorfmap_relief_z25.glb, relief_zaehlung.json, pruefung/o18/aenderungen_o18.json, pruefung/platzierung_t59u.json, pruefung/runde_m_aenderungen_t65u.json.
- Eigene Topologie-Nachrechnung (p2_analyse.py, **nicht das Gate**): verbleibende getrennte Teile nur X084 (62 Zellen, Lücke 9,5) und G2 (1588 Zellen, jetzt 8,0 Zellen bei 196|74). Erwartung Gate [A]: R1_blind 24 → 1 (X084-Ende 156,5|37,5; Anfang liegt am Kartenrand), R2 15 → 2 (X084, G2), R6 4 unverändert. R3/R8a sollten mit den Rampen stark fallen; G5/G6/R5/T1 an den Rampenstellen können sich in beide Richtungen bewegen – erst das Gate nach L1 zeigt das.
- Bilder: `trockenlauf_rampen_vorher_nachher.png` (12 Rampenorte), `trockenlauf_verbinder.png`, `ausnahmen_x084_g2_nahbild.png` (Hillshade + VC aus relief_daten, keine Viewer-Renderings).

## Ausnahmen / Kandidaten für QA P4
| Stelle | Regel | Messwert | Nahbild | Begründung |
|---|---|---|---|---|
| D1 156,5\|37,5 (rampe_11 = X084, Ende) | R1_blind, R2_getrennt | Lücke 9,0 Zellen = 10,8 m zum Netz; Komponente 62 Zellen (Trockenlauf) | ausnahmen_x084_g2_nahbild.png links | Entnahme würde D2 ändern (547 Ecken, 14,2 mm); Weg neu ziehen ist nicht freigegeben |
| G2 270,9\|62,2 | R2_getrennt | 1588 Zellen; Lücke 41,2 Zellen vor P2, 8,0 Zellen (9,6 m) bei 196\|74 nach Trockenlauf | ausnahmen_x084_g2_nahbild.png rechts | laut Entscheidung nicht schließen |

## Risiken
- Rampen-Entnahme ändert Höhen in 33 Kacheln deutlich (Wände kommen zurück) → kollidiert inhaltlich mit L1-Ergebnissen dort; das Gate nach L1 entscheidet, ob eine Familie schlechter wird (Regel: keine darf).
- O16-Fläche (Krater) bleibt aus dem alten Rampenpfad abgeleitet; ohne Rampe ist das eine harmonische Füllfläche wie bisher.
- `p2_verbinder.json` wirkt nur im Legacy-`gen_relief.py`; `neu/vektor.py`/vektor.json kennen die Verbinder nicht.
- `baue_html.py` schreibt fest nach `/tmp/w3/bundle_r.js` (geteilt mit anderen Bots).

## Nachtrag 16.11. ca. 07:45 Uhr MEZ: D2-Sperre freigegeben, weicher Übergang D1|D2 [S]
Bedingung Dorfmap-Grundgerüst: keine harte Stufe an der D2-Kante. Umsetzung in `gen_relief.py` (`P2_D2_UEBERGANG`, Standard 4 Zellen):
die Differenz Referenz − neu an der D2-Randecke wird außerhalb von D2 linear über 4 Zellen (8 Ecken, Gewicht 1 − d/9) ausgebaut; D2 selbst wird danach exakt auf die Referenz gesetzt.
Gilt für alle vier Kanten; geändert hat sich nur Nord (D1) und West (C2).

Trockenlauf (nur /tmp, /tmp/w3 nicht berührt, baue_html.py nicht gelaufen), Vergleich gegen relief_daten.json.gz 8e374b0:
- D2 Höhen 749d3c4b…, Farben b67dc719…, Wasser 4b33ed17…, Wegtextur e6cf61d2… unverändert; D2 innen max. Differenz 0.
- Rohdifferenz an der Kante (ohne Sperre): 387 Ecken, max 8,8 mm; Übergang verändert 865 Ecken (Farben ebenso gewichtet).
- Korrektur-Verlauf an der stärksten Spalte x = 128,0: 7,78 / 6,81 / 5,84 / 4,86 / 3,89 / 2,92 / 1,95 / 0,97 / 0 mm (Ecke 1 bis 9) = linear, 0,97 mm je Ecke (0,6 m), entspricht 0,16 %.
- Knick an der Kante (Kantenstufe minus Mittel der Nachbarstufen), Änderung gegenüber Basis: harte Sperre max 9,39 mm, weich **max 1,16 mm** (x = 127,5).
- Stufenänderung an der Kante gegenüber Basis: Nord hart 18,3 mm → weich 10,6 mm (x = 128,5), West hart 5,9 mm → weich 0,41 mm, Süd/Ost 0.
  Die verbleibenden 10,6 mm Nord sind kein Sprung: Das D1-Gelände an der C2/D1/D2-Ecke sinkt durch die Rampen-Entnahme stetig ab (neu minus Basis je Ecke ab Kante 0 / −10,6 / −30,1 / −65,8 / −147,5 / −297 / −421 / −562 / −889 mm).
- Gate-Prüfung der Kante (G2/G3/G6) folgt nach L1, Schritt 6 in NACH_L1.md.

`baue_html.py`: Bundle-Pfad per `BUNDLE_OUT` einstellbar, Standard unverändert `/tmp/w3/bundle_r.js`. Nicht ausgeführt.

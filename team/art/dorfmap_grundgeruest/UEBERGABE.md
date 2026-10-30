# Übergabe Dorfkarten-Grundgerüst c20 (Stand t32u, 30.10.2026)
Marker: [S] gemessen oder aus der Quelle, [A] Annahme, [R] gerechnet, [F] Entscheidung.
Die Karte c20 ist unverändert. Das Grundgerüst liest sie nur aus.

## Was drin ist
- **Raster:** z25 hat 336 × 303 Zellen [S]. Eine Zelle ist 25 px groß und entspricht 1 m [A]. z50 hat 168 × 152 Zellen [S].
- **Felder je Zelle (39):** siehe `schema_zelle.json`. Die wichtigsten:
  - `untergrund`: SCHNEE, WALD, FELS, BODEN, SAND, WASSER_EIS, SCHATTEN, KLIPPE_WAND, KLIPPE_KANTE [S]
  - `begehbar`, `bebaubar`, `bebaubar_erweitert`, `bauzone_plan` [R]
  - `ebene`, `hoehe_m` [A]
  - `wand_name`: Nord, Krater, Suedgrat, Ostgrat [S]
  - `deko_kapazitaet`, `deko_baum_ok`, `deko_fels_ok` [R]
  - `hindernis_id` und `hindernis_art` [S]
- **Ebenen [A]:**
  - SENKE: Talkessel, Bezug 0 m
  - HANG (t34u): freie Flaeche ohne Wand zwischen den Stufen, Hoehe glatt interpoliert −7,1 bis +6,2 m
  - GIPFEL (t34u): Schneekuppe noerdlich des Kraters, +7,7 m
  - SIMS (t34u): kleine von Wand umschlossene Flaechen, Hoehe aus Umgebung
  - PLATEAU_NORD: +8,6 m
  - OSTPLATEAU: +6,7 m
  - TAL_SUED: −7,6 m
  - KRATER: eigenes Becken
  - WAND: Klippen
  - Die Höhen sind geschätzt, nicht gemessen.
- **bebaubar oder bebaubar_erweitert:**
  - `bebaubar`: nur im Talkessel (senke_becken) und mindestens 2 m von Wand und Wasser entfernt. z25 hat 27 140 Zellen, z50 hat 7 240 [R].
  - `bebaubar_erweitert`: dieselben Regeln, aber auf allen Ebenen. z25 hat 54 409 Zellen, z50 hat 15 056 [R].
  - Je Ebene in z25 [R]: SENKE 28 269, HANG 13 719, TAL_SUED 7 718, PLATEAU_NORD 3 162, KRATER 1 180, OSTPLATEAU 361, GIPFEL 0, SIMS 0 (t34u).
  - Ob Bauen außerhalb des Kessels erlaubt ist, entscheidet Fabian. Das ist noch offen [F fehlt].
- **Plätze:** 355 Plätze bis E100 [S].
  - Mindestens 95 % auf bebaubar: 149 Plätze [R].
  - Mindestens 95 % auf bebaubar_erweitert: 317 Plätze [R].
- **Korrekturen:** 427 Zeilen in `overrides_t12u.csv`, jede mit Beleg [S]. In z50 gelten sie ab 2 von 4 Teilzellen. Korrekturen nach FELS gelten schon ab 1 von 4 [F].

## So nutzt ihr es
- **Wege- und Deko-Bot:**
  - Wege nur auf `begehbar=1` legen.
  - Häuser und Plätze auf `bebaubar` legen, oder auf `bebaubar_erweitert`, wenn Fabian zustimmt.
  - Deko nur auf Zellen mit `deko_kapazitaet>0` setzen. Bäume nur bei `deko_baum_ok`, Felsen nur bei `deko_fels_ok`.
  - Plätze und Wege stehen in der Overlay-CSV.
- **Art Director:**
  - `ebene` und `wand_name` zeigen, wo Höhenstufen gemalt werden müssen.
  - `pruefung/t34u_nachher_ebenen.png` zeigt die Ebenen im Überblick.
  - Die Karte selbst bleibt unverändert.

## Was offen ist
1. 38 Plätze liegen in E100 auch auf bebaubar_erweitert nicht zu 95 % innen. Je Epoche: E16 5, E40 16, E70 23, E100 38 [R].
2. 800 Dekoplätze haben nur eine Zahl und keinen Ort. Sie sind nur gerechnet, 629 haben eine Position [R].
3. 32 Plätze haben keinen zeichenbaren Weg: 13 mit weg_m = 0 und 19 mit nur 1 Punkt [R].
4. X084 geht über die Nordklippe. Entschieden ist eine Treppe oder ein Steg über 8,6 m [F t28u, R]. Welchen Wegtyp das wird, muss Art festlegen.
5. Alle Höhen sind Annahmen [A].
6. Offene Befunde:
   - 3 SCHNEE-Zellen am Gipfel in z50.
   - Kleine Sandbänke sind in z50 nur teilweise SAND. Beides ist begehbar.
   - Findling #17 und #1–#9 sind nur Befund.
   - Der Rand bei cx 329–335 ist seit t34u TAL_SUED (behoben).
7. Es gibt noch keine Nachricht an andere Bots. Dafür fehlt Fabians Go.

## t34u
- Ebenen neu nach Waenden: Fehlerliste `pruefung/t34u_fehlerliste.csv` (F1–F10 behoben, B1–B8 offen).
- Vorher/Nachher: `pruefung/t34u_vorher_fehler.png`, `pruefung/t34u_nachher_ebenen.png`.
- Regelpruefung aller Zellen: `pruef_konsistenz_t34u.py` (0 Verstoesse z25/z50).
- 3D-Modell: `modell3d/` (t36u, GLB+OBJ, Sidecar, Abweichungen [F], BRAUCHE.md).

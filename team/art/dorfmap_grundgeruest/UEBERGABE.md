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

## Für den Wege/Deko-Bot (O12, Relief-Bot, Gelände NICHT geändert)
- rampe_4 (Kamera in relief3d/pruefung/nah_kameras_t65u.json): In der Textur läuft nahe der Kamera ein unscharfes Weg-Band quer durchs Bild, im Clay-Render nicht zu sehen → Weg-Overlay liegt über/über die Hangkante hinaus. Bild: /workspace/t65/n2 (rampe_4, c/t).
- rampe_13: Der Weg endet abrupt an der Kante, mit einem dunklen Rechteck am Ende → Overlay-Ende bzw. Platzhalter prüfen. Bild: /workspace/t65/n2 (rampe_13).
- Das Gelände ist an beiden Stellen im Clay unauffällig. Bitte im Weg-Overlay beheben, nicht im Relief.

## O16 (F t77u) – für alle Bots
- rampe_9 (Krater, (130,161)->(140,198)) samt Ruecken 133|173 entfernt, nur Anzeige. Jetzt 13 Rampen; alte rampe_10..13 = neue rampe_9..12. Zellwerte unveraendert (nur boden_anzeige_m). Korridor bleibt in der CSV begehbar – Wege-/Deko-Bot: dort keinen Rampenweg mehr erwarten. Details relief3d/pruefung/runde_o_status.md.

## O18 – Steinpfad D1/F1 (Overlay-Teil, nicht im Grundgeruest)
- D1: Die Luecke auf der Gelaendeseite ist durch die O18-Glaettung und Wegschutz geschlossen. Die Pfadsteine selbst (Overlay) muessen in der Pfad-Ebene durchgezogen und an die Abzweigungen angeschlossen werden.
- F1 (O18c geprueft): Der Steinpfad ist rampenwege[1] (50 Punkte, Start G1 273,4|21,2 auf der Nordwand-Oberkante, Ende F1 227,1|37,0 = Zelle 227|36, zell_id 12323, boden_anzeige 0,39 m).
  Das Ende liegt 2 Zellen suedlich vom Wandfuss der Nordwand (227|34 WAND_FUSS 11,1 m; 225|34 und 226|34 WAND 13,7 / 12,7 m) und endet dort blind: der naechste andere Weg-Punkt ist 18,4 m entfernt (245|41).
  Gelaendeseitig ist die Rampe durchgehend (Hoehenschritt je Punkt <=0,45 m in F1, max 0,78 m bei 267|23 in G1). Ursache ist also overlayseitig: Endpunkt/Anschluss des Pfads, nicht das Gelaende. Overlay: Ende an das Wegnetz (z. B. 245|41) anschliessen oder vor der Wand enden lassen. Zellwerte unveraendert.
- Wege duerfen nicht schluchtartig eingesenkt werden: Overlay auf boden_anzeige_m legen, nicht tiefer.

## O18k – Wegnetz-Befund Overlay (t105u/t106u, nur Doku, nicht gesendet)
Messung `pruefung/o18/wegnetz_o18k.py` (Ergebnis `pruefung/o18/wegnetz_{vor,nach}_o18k.json`): Alle 13 `rampenwege` sind eigene Graph-Komponenten, keines der 26 Enden liegt ≤2 m an einem Dorfweg (`wege`/WEGA). Dorfnetz selbst zerfällt in Hauptnetz + G2 (1588 Zellen), D2 (1227), F4 (94), E3 (38).
Vorschläge (Overlay-Daten, Koordinaten m):
- rampe_1 F1/G1: Ende 227.1|37.0 im Wandfuß-Kessel (2 m weiter +2 m Fels). Verlängern 227.1|37.0 → 232|40 → 245|41 (Dorfweg). Gelände dafür in O18k bereits als Gang abgesenkt (`_anschluss_gang`). Oben 273.4|21.2 Plateau ohne Weg.
- rampe_11 D1: Start 148.5|2.5 am Kartenrand (vorher Kerbe 14→2.1 m). Start ins Innere verlegen oder Plateau-Weg entlang z≈5 ergänzen; Gelände läuft jetzt auf Randhöhe aus (`_rand_auslauf`).
- rampe_2 D1/E1: Ende 175.2|25.7 läuft in Hang (+1.9 m/2 m) → bis nächster Dorfweg verlängern.
- rampe_4 H6 Anfang 295.3|222.9 (+1.7 m), rampe_8 C4 Ende 89.5|171.4 (+1.7 m), rampe_12 Anfang D4 127.5|133.5 (Wand 1.33 m/m): enden an Fels → Endpunkt 3–5 m ins freie Gelände verschieben und an Dorfweg anbinden.
- Übrige Rampen-Enden (0,3,5,6,7,9,10): freies Gelände, aber ohne Wegnetz-Anschluss → je Verbindungsstück zum nächsten Dorfweg.

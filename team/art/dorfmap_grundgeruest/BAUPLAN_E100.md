# BAUPLAN E100, gültiger Stand (t26u, Zahlen geprüft t31u, 30.10.2026)
Quelle: Wege-&-Deko-Bot, Plan **v4b** (t25u), `team/art/wege_deko_system/WEGE_ANTWORT_DORFMAP.md` und `umrechnung_25pxm/e100/*_v4b*`. Nur gelesen, nichts übernommen, was dort nicht steht. Vorfassung: `_alt/BAUPLAN_E100_t16u.md` (v8/ausbau-Basis, überholt).
Marker: [S] gemessen/Quelle · [R] gerechnet · [A] Annahme · [F] Fabian.

## 1 Zahlen v4b, nachgezählt
| Größe | Quelle | eigene Nachzählung | ok |
|---|---|---|---|
| Slots E100 | 355 = 99 + 256 [S] | 99 (zonen_c20_v9) + 256 (stand_E100) [R] | ja |
| 4×4 / 6×6 / 8×8 / 10×8 / 8×6 | 213/103/23/15/1 [S] | Bestand 63/27/3/5/1 + neu 150/76/20/10 [R] | ja |
| Slots E16 / E40 / E70 | – | 142 / 203 / 279 (99 + 43/104/180) [R] | – |
| Wegmeter neu / gesamt | 2.396 / 4.280 [S] | 2.395,7 Summe weg_m [R] | ja |
| Brücken | 17, 49,2 m [S] | 17 Zeilen, 49,2 m [R] | ja |
| Dekoplätze E100 | 1.429 [S] | 629 mit Position (netz_e1) + 800 **nur gerechnet** (2.396 m × 0,334/m) [R] | Zahl ja, aber 800 ohne Ort |
| deko_limit E40/E70/E100 | 161/270/380 [S] | Formel e100.py: Häuser gebaut + 3 + 2 + E//2 [S] | ja |
| „0 ohne Weg“ | [S] | 13 Slots weg_m = 0, 19 weitere nur 1 Polylinienpunkt (32 ohne zeichenbaren Weg) [R] | Widerspruch, siehe §4 |

## 2 Abweichungen zur Vorfassung (t16u)
- t16u nutzte den v8/ausbau-Plan: E16 140, E40 233 Plätze. v4b: E16 142, E40 203, E100 355 [R]. Der v8-Plan ist laut Quelle überholt (83 Plätze schneiden E1-Wege) [S].
- t16u-Projektion H1 410 / H2 245 entfällt; gültig ist 355 [S].
- Footprint-Konflikt GDD (16/36/24/36/48 m²) gegen GÜLTIG bleibt offen; v4b nutzt 4×4/6×6/8×8/10×8 (+B11 8×6) als [A] des Wege-Bots.
- GDD-Deckel 18 Häuser: laut Fabian falsch, Korrektur beim Game Designer [F].
- Bauzone: neu Planmaske BB4_plan_v2 (BB4 + A18 mit 1 m Rand, +21 m²) [F t25u 1a]; Feld `bauzone_plan` im Raster.

## 3 Prüfung gegen Gelände-Raster z25 (nur Overlay) → `pruefung/t26u_*`
- Slots ≥95 % bebaubar: **149 / 355** [R]; mittlerer Anteil 0,44. Je Stand nicht innen: E16 12/142 · E40 54/203 · E70 130/279 · E100 206/355.
- Bestand 95/99 innen; nicht: D16, D13, A18, D15D.
- Ursache der Fehlzellen fast nur „begehbar, nicht bebaubar“ (6.336 von 11.471 Slotzellen): Schnee außerhalb senke_becken/Wandabstand, wie in der Quelle („Schneezonen außerhalb BB4“, 151 Slots).
- Slots auf Wand 0 · Wasser 1 (X103, 1 Zelle) · Schatten 0 · Fels 1 (Stand t31u) · Hindernis 2 (A18 9 Zellen, X033 6) · Wald 12 Slots / 31 Zellen [R].
- Wald unter Wegen: 18 Wege, 164 Zellen (t26u: 169) (Weg 2 Zellen breit [A]). Quelle meldet 66 Slots / 99 Wege „Wald/ungeprüft“ nach ausbau-Maske; im Raster sind es nur 12/18 WALD — die übrigen sind dort „ungeprüft“, nicht Wald.
- Brücken: Mitte auf WASSER_EIS nur **3/17** (X045, X047, X135). 12 Brücken mit 0,4–0,8 m liegen im Raster ganz auf SCHNEE (0,4-m-Maske der Quelle feiner als 1-m-Zelle). **X069 (11,6 m) und X084 (22,4 m) queren KLIPPE_WAND, nicht Wasser** (t27u: X069 war Fehlklassifikation → Schnee korrigiert; X084 Wand mit Eisfall korrekt); Enden dort nicht beide begehbar. Liste `t26u_bruecken.csv`.
- Deko (629 mit Position): 0 auf Wand, 0 auf Wasser; 625 SCHNEE, 4 BODEN; 6 auf Zellen mit deko_kapazitaet 0. Summe Kapazitätsfeld 27.452 (t31u) ≫ deko_limit 380 → Limit passt in das Feld. Die 800 gerechneten Plätze sind nicht prüfbar (kein Ort).

## 4 Offene Entscheidungen
1. **Schneezonen (206 Slots außerhalb bebaubar).** a) bauzone_plan um die Schneezonen erweitern (+13.290 m² laut Quelle): Plan bleibt, Raster-Regel `bebaubar` braucht dann eine Ausnahme für senke_becken. b) Slots in die heutige Fläche verdichten: weniger als 355 Slots. c) Schneezonen erst ab E41 freigeben: E16/E40 fast sauber, Rest später.
2. **X084 über Klippe — entschieden [F t28u]:** Treppe/Steg über den Höhenunterschied, 8,6 m [R] (klippe_hoehe_m der Wandzellen, Wand Nord). Gelände bleibt unverändert. Alternativen (anders anbinden, streichen) verworfen. X069 war Fehlklassifikation, korrigiert (t27u).
3. **Dekoplätze ohne Ort (800).** a) Wege-Bot setzt Positionen in Schritt 2–5. b) Zahl als reine Kapazität führen, keine Plätze. 
4. **„0 ohne Weg“ vs. 32 ohne Polylinie.** a) gilt als „liegt direkt am Weg“, nur dokumentieren. b) fehlende Stichwege nachziehen.

## 5 Befund Bauzone (offen)
- 206 von 355 Slots liegen nicht zu ≥95 % auf bebaubar (Schneezonen außerhalb senke_becken). `bebaubar` und `bauzone_plan` bleiben unverändert.
- Seit t29u gibt es das Zusatzfeld `bebaubar_erweitert` (ohne senke_becken) [A]. Damit liegen **317/355** Slots zu ≥95 % innen. Nicht innen je Epoche: E16 5 · E40 16 · E70 23 · E100 38 [R, Stand t31u]. §4.1 bleibt als Entscheidung offen. Den Weg über bebaubar_erweitert nutzt das Raster bereits.

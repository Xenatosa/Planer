# Prüfprotokoll Gelände-Raster c20 z25 (Stand t9u/t10u/t11u)

## Methode
- Vergleich c20-Ausschnitt (links) gegen Klassenbild (rechts), Nearest-Neighbour vergrößert.
- Stichprobenraster: 12 Kacheln mit je 56×56 Zellen (≈ 37 600 Zellen ≈ 37 % der Karte [R]), Gitter über Nord, Mitte, Süd, West und Ost inklusive Randzeilen und Randspalten (`pruef_raster_1.png`, `pruef_raster_2.png`).
- Gezielte Ausschnitte: Senke, Westwald, Südwald und Fluss, Ostgrat, Nordwand (`pruef_randausschnitte.png`).
- Bewertet wird je Kachel und Region nach Augenschein. Zellgenaues Auszählen ist **nicht** erfolgt.

## Gefundene und behobene Fehler
| Fehlklasse | Befund | Korrektur | Zellen |
|---|---|---|---|
| WEG/HOF/FEUER/BRUECKE im Gelände | gehören nicht ins Gelände (t10u) | in den Overlay verschoben, Gelände darunter per Farbe | siehe meta `zaehlung_vor_t9u` |
| BODEN-Flecken in der Senke | c20 zeigt dort Schnee | BODEN mit Schneeanteil ≥ 0,3 → SCHNEE [R] | meta `boden_zu_schnee` |
| Baumstämme als KLIPPE_WAND/FELS (West- und Südwald) | braune Stämme als Wand erkannt | Komponenten < 200 Zellen, deren Ring zu ≥ 40 % WALD ist → WALD [A] | meta `wald_aus_wand` |
| Randzeile 302 (nur 10 px hoch) als BODEN | Abtastartefakt | Wert der Zeile 301 übernommen | 336 |
| Salzrauschen und kleine Inseln | Magenta- und Kantenpunkte | Mehrheitsfilter und Inselfilter | meta `glaettung_zellen` |
| UNBEKANNT | 1 189 | Filter | 25 übrig |

## Restfehler (nicht behoben)
1. **Teich im Nordwesten** (ca. Zellen 5–20, 15–30): als SCHATTEN statt WASSER_EIS erkannt. Fehler.
2. **Gefrorener Bach westlich des Kraters** (ca. x 0–60, y 110–230): breiter Eiskanal, im Raster größtenteils SCHNEE/SCHATTEN mit nur kleinen blauen Resten. Fehler. Er wäre begehbar markiert, obwohl er Eis/Wasser ist.
3. **Verschneiter Wald im Südosten und am Westrand**: lückig erkannt, einzelne Bäume als SCHNEE.
4. **Bebaubar endet gerade** bei x ≈ 103 und y ≈ 153 (Kante des BB4-Fensters). Das ist keine Geländegrenze.
5. **Wassertiefe** fehlt (keine Quelle). Die Höhenstufen sind Annahmen [A].
6. **25 UNBEKANNT-Zellen** (Fluss-Süd, Magenta).
7. **Fehlerquote:** 5 von 12 Kacheln haben sichtbare Fehlklassen (Punkte 1–3). Die Zellquote ist nicht ausgezählt.

**Ergebnis: nicht fertig.** Die Punkte 1–4 müssen vor einer Freigabe behoben werden.

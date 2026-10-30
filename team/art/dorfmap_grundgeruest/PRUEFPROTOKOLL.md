# Prüfprotokoll Gelände-Raster c20 z25 (Stand t9u/t10u/t11u)

## Methode
- Vergleich c20-Ausschnitt (links) gegen Klassenbild (rechts), Nearest-Neighbour vergrößert.
- Stichprobenraster: 12 Kacheln mit je 56×56 Zellen (≈ 37 600 Zellen ≈ 37 % der Karte [R]), Gitter über Nord, Mitte, Süd, West und Ost inklusive Randzeilen und Randspalten (`_alt/pruef_raster_1.png`, `_alt/pruef_raster_2.png`).
- Gezielte Ausschnitte: Senke, Westwald, Südwald und Fluss, Ostgrat, Nordwand (`_alt/pruef_randausschnitte.png` (überholt, ersetzt durch `pruefung/kacheln_r5_*.png`)).
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

## t12u (30.10.2026)
**Geaendert**
- Teich NW + gefrorener Westbach = WASSER_EIS [S] (Farbdetektor G−R≥10, B−R≥18; Unterlauf/Verbindung als Linie nach c20 in `override_wasser_t12u.png`). begehbar=0 auf Wasser (Bruecken ausgenommen, wie bisher).
- Nordbach-Luecke y 37–71 ergaenzt [S].
- Fehl-Klippen → FELS/WALD: `overrides_t12u.csv` (5 Rechtecke, Blockfeld, Felsgruppe, Findling, tote Baeume) [S].
- Verschneiter Suedwald: dunkle Kronenumrisse (V<150, H 95–140, 3×3-Mittel ≥0,04 [A]) im Suedband → WALD, Closing. WALD 10 127 → 11 459 Zellen [R].
- Vorschau ohne Schraffur/Streifen; bebaubar in `raster_c20_z25_bebaubar.png`.
- bebaubar neu aus Gelaende (siehe SPEC), `bauzone_bestand` = alte Grenze. bebaubar 27 140, Bestand 23 123, ausserhalb Bestand 4 887 Zellen [R].

**Kachelpruefung r4: 182 Kacheln à 24×24, alle angesehen (Seitenvergleich c20 | Raster)**
- ok: 172.
- Mangel: K3_11, K4_11, K5_11, K0_11 (SCHATTEN-Flecken auf Flusseis statt WASSER_EIS); K1_0–K4_0 (frostige Buesche/Felshaufen als WALD, Klasse unsicher); K13_12 (helle Schneebaeume teils SCHNEE).
- Fehlerquote: je Kachel 10/182 mit Mangel (5,5 %) [R]. Zellgenau NICHT auszaehlbar (kein Referenzraster); geschaetzt < 1 % der Zellen [A].

**Restfehler**
1. SCHATTEN im Flusseis (Sueden), ca. 100–200 Zellen [A].
2. NW-Rand der Senke: senkrechte Grenze x=136 (offenes Gelaende, keine Wand) [A].
3. NO-Ecke: Ostgrenze ohne Wand = Kartenrand [A].
4. Buesche K1_0–K4_0: WALD oder FELS offen.

## t14u
- **Flusseis K0_11, K3_11, K4_11, K5_11:** Die SCHATTEN-Flecken, die am Eis liegen, werden jetzt per Filter zu WASSER_EIS. Der echte Wandschatten oben bleibt. Vorher/Nachher: `pruefung/t14u_flusseis_*`.
- **K1_0–K4_0:** Die Felshaufen und das Blockfeld werden per Override (Zeilen 6–8) zu FELS. Einzelne Kiefern bleiben WALD. Belege: `pruefung/t14u_felshaufen_*`.
- **K13_12:** Die Schneelücken zwischen den Bäumen sind echt, deshalb keine Änderung (`pruefung/t14u_K13_12_schneebaeume.png`).
- **Restfehler:**
  - Eisschollen im Fluss sind als SCHNEE klassiert [A].
  - Die Westgrenze x=136 und die Nordost-Ecke bleiben [A].
  - Die Kachelbögen r5_0–2 habe ich nur grob angesehen.
  - z50 ist nicht neu erzeugt und zeigt noch den Stand von t13u.

## t16u
- **Quellplätze (Plan-m ×1,2 umgerechnet):**
  - E16: 118/140 innerhalb bebaubar.
  - E40: 119/233.
  - Fehlstellen liegen fast nur außerhalb der Senke auf freiem Schnee (96 von 114 bei E40 ≥95 % frei).
- **Bilder angesehen:** t16u_plaetze_E16/E40, overlay_plaetze_erweiterung, z50-Vorschau (neu erzeugt).
- **Restfehler:**
  - Die Polygone sind aus ausbau.py exportiert (Quelle unverändert, Lauf in /tmp). Die Rasterung geht über fillPoly mit Zellmittelpunkt, Randzellen ±1.
  - Die Schwelle 95 % ist [A].
  - Die Kapazität in §4 ist grob (8-m-Raster).

## t26u
- Quelle v4b nachgezählt: 355/213/103/23/15/1, 17 Brücken 49,2 m, 1.429 Deko (629 Ort + 800 gerechnet), deko_limit-Formel — stimmt [R].
- bauzone_plan: 31.893 Zellen; bebaubar 27.140. In Planmaske, nicht bebaubar: 5.386 (5.166 Abstand/außerhalb senke_becken, 112 Wasser, 98 Hindernis, 3 Wand, 3 Fels, 2 Schatten, 1 Wald, 1 nicht begehbar). Bebaubar, nicht in Planmaske: 633.
- Slots ≥95 % bebaubar 149/355; Brücken-Mitte auf Wasser 3/17; X069/X084 über KLIPPE_WAND; Deko 0 auf Wand/Wasser.
- Bilder E16/E40/E70/E100 selbst angesehen; Gelände-PNGs z25/z50 unverändert (nur CSV/Meta wegen neuem Feld).
- Restfehler: Brücken <1 m unter Zellauflösung; Wegbreite 2 Zellen [A].

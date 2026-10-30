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
- **Bilder angesehen:** _alt/pruefung/t16u_plaetze_E16/E40 (ersetzt durch t26u_overlay_E*), overlay_plaetze_erweiterung, z50-Vorschau (neu erzeugt).
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

## t27u Brücken X069/X084 gegen Original c20
- Methode: Weg-Polylinie (v4b) auf c20-Pixel gelegt, Zellen entlang Weg gelistet, Schneeanteil je Zelle aus Pixelfarbe (B≥R−5, B>140, geringe Sättigung) [A], Sichtprüfung in 1,4–1,6× Ausschnitten. Bild: `pruefung/t27u_bruecken_X069_X084_original_raster.png`.
- **X069 (11,6 m): Fehlklassifikation belegt [S].** Original zeigt offenen Schnee zwischen Felsbrocken, einem Busch und einer flachen Felsrippe; kein Wasser, keine Wand. Raster hatte Brocken/Busch-Ränder als KLIPPE_WAND/KANTE/WALD/FELS über den Schnee gezogen. Korrektur: 22 Einzel-Overrides (nr 9–30, `overrides_t12u.csv`) → SCHNEE, nur Zellen am Weg mit Schneeanteil ≥0,80. Rest: 17 Wegzellen bleiben Kante/Wand/Wald/Fels (Weg streift Brockenecken; Kanten werden aus Wandrand neu abgeleitet) → X069 ist ein Landweg, keine Brücke nötig; Wege-Bot sollte Linie um ≈0,5 m von den Brocken weg legen.
- **X084 (22,4 m): Wand korrekt [S].** Original zeigt senkrechte Felswand mit gefrorenem Wasserfall (Eisfall) in einer Spalte; der Weg führt die Wand hinab. Kein begehbarer Boden, kein ebenes Wasser. Keine Änderung. Brücke unpassend; nötig wäre Treppe/Steg über Höhensprung oder anderer Weg.
- Abhängige Dateien neu: z25 (Overrides nur z25), z50, `pruefung/t26u_*`. Zahlen danach: Slots ≥95 % bebaubar weiter 149/355; Wald unter Wegen 169→164 Zellen; bebaubar ohne Planmaske 633→635.
- Gelände sonst unverändert. Bauzone-Erweiterung für die 206 Slots bleibt offen (keine Wahl von Fabian).

## t28u X084 Treppe/Steg [F]
- Fabian: X084 bekommt Treppe/Steg über den Höhenunterschied; Gelände unverändert (Wand bleibt KLIPPE_WAND).
- Overlay/Daten: `pruefung/t26u_bruecken.csv` Spalte `wegtyp` = 'Treppe/Steg (Hoehe)', `hoehenunterschied_m` = 8,6 [R] aus `klippe_hoehe_m` der Wandzellen am Weg (Wand Nord, alle 8,6; oben hoehe_m 8,6 [A], unten 0,0 [A]). Übrige 16: 'Bruecke (Wasser)'. Overlay-Kreis blau.
- Alternativen b/c waren keine eigenen Dateien → nichts nach `_alt/` verschoben.

## t29u bebaubar_erweitert und Restfehler (30.10.2026)
**bebaubar_erweitert** (neu, Regel in SPEC.md, [A]):
- Zellen z25: 54 416 [R]. bebaubar bleibt bei 27 142, bauzone_plan bei 31 893 (unverändert).
- Slots ≥ 95 %: 149/355 bei bebaubar → **317/355 bei bebaubar_erweitert** [R].
- Nicht innen (bebaubar → erweitert) [R]: E16 12→5, E40 54→16, E70 130→23, E100 206→38.
- Vorschau: `pruefung/t29u_bebaubar_erweitert_E100.png`.

**Geprüft und korrigiert** (Overrides in z25, Quelle je Zeile):
- **Sandbänke Südfluss:** Die Randzellen waren SCHNEE. 57 Zellen → SAND [S].
  - Sandpixel-Anteil ≥ 0,50, im Bild geprüft: `t29u_zoom_sand.png`.
- **Eisschollen Südfluss:** Sie waren WASSER_EIS. 63 Zellen → SCHNEE [A].
  - Bild: `t29u_fluss_schollen.png`.
  - Die Wasserfall-Gischt bei x ≥ 312 ist ausgenommen.
  - Schollenzellen sind jetzt begehbar. Bebaubar sind sie nicht (2 m Abstand zum Wasser).
- **Schneegipfel westlich der Senke** (cx 90–122, cy 92–120): Die Flanken waren SCHNEE und damit begehbar und erweitert bebaubar. 270 Zellen → FELS [S].
  - Bilder: `t29u_zoom_gipfel.png`, `t29u_kacheln_r5_1_1.png`.
- **Klassen z25 vorher → nachher:**
  - SAND 483→537, FELS 1 846→2 116, SCHNEE 60 067→59 823;
  - WASSER_EIS 6 756→6 695, WALD 11 227→11 217, SCHATTEN 1 781→1 772;
  - begehbar 62 597→62 398 [R].

**Geprüft, ohne Korrektur:**
- **UNBEKANNT-Splitter:** 197 Zellen in 27 Gruppen, vom Filter an die Nachbarn vergeben. Jede Gruppe im c20-Ausschnitt angesehen: `t29u_splitter_c20.png`.
  - Es sind fast nur Übergangszellen (Felskante/Schnee, Ufer, Baumschatten). Die Zuordnung ist plausibel [A].
  - Eine einzelne richtige Klasse ist nicht belegbar, darum gibt es keine Overrides.
  - Ausnahme: Die Sandinsel S23 ist mit der Sandkorrektur erledigt.
- **Westgrenze x=136** (`t29u_rand_x136.png`):
  - In c20 gibt es dort keine Wand und keine Kante. Offener Schnee läuft bis x≈100 weiter. Die Grenze von senke_becken ist also keine Geländegrenze [S].
  - senke_becken und bebaubar habe ich nicht geändert (Bauzone offen). bebaubar_erweitert schließt die Fläche an.
- **NO-Ecke** (`t29u_rand_nordost.png`):
  - Die Senke endet senkrecht bei x≈320 (cy 37–72) im offenen Schnee. In c20 geht der Schnee bis zum Kartenrand weiter. Auch das ist keine Geländegrenze [S].
  - Nicht geändert. In bebaubar_erweitert ist die Fläche enthalten.
- **Kachelbögen r5_0–2** (y 0–215): neu aus dem aktuellen Raster, `t29u_kacheln_r5_{0,1,2}_{0..3}.png`. Alle 126 Kacheln angesehen.
  - Gefunden und korrigiert: der Schneegipfel (siehe oben).

**Weiter offen (nicht behoben, nicht belegbar korrigiert):**
1. **Findlinge mit Schneehaube** zählen als SCHNEE, z. B. cx 24–48/cy 144–168 und mehrere in der Senke. Sie sind begehbar und bebaubar_erweitert, obwohl sie Hindernisse sind. Ein Pixel-Detektor ist nicht zuverlässig (Schneehaube weiß, Flanke braun wie Klippe).
2. **Schmaler Strich cx 190–195/cy 40–100** (Nordbach oder Spur) ist 1–2 Zellen WASSER_EIS. Nicht entschieden, ob Bach oder Spur.
3. **Höhenstufe in bebaubar_erweitert:** Plateau über der Nordwand, Kraterboden und Ostplateau zählen ohne Höhenprüfung [A].
4. **z50 hat keine Overrides.** Dort ist der Gipfel weiter SCHNEE.
5. **Kachelbögen r5_3/r5_4** (y ≥ 216): in t29u nicht erneut angesehen.

## t30u Pruefung

- Senke-Grenze und `bebaubar` sind unveraendert. Es gibt keine Gelaendegrenze bei x=136 und im Nordosten [F]. Die Ausnahme sind 2 Zellen durch einen Findling (siehe unten).
- Ebenen-Bild: _alt/pruefung/t30u_ebenen.png (ersetzt durch pruefung/t33u_ebenen_vollstaendig.png), selbst angesehen. Plateau Nord, Ostplateau, Krater und Senke liegen plausibel. Bei TAL_SUED gibt es Spalten-Luecken [A], offen.
- Findling-Detektor: brauner Anteil >15 % in SCHNEE-Zellen, nicht neben Waenden. 19 Treffer, alle im Bild angesehen (pruefung/t30u_findling_treffer.png):
  - **4 belegt → FELS-Override (Zeilen 421-424, 7 Zellen)** [S]: #0 cx320/cy52-53, #11 cx10-11/cy223, #13 cx14/cy229-230, #14 cx9/cy242.
  - Unsicher, nur dokumentiert: #1-#9 sind flache braune Flecken (Erde oder Moos? keine Blockform). #10 ist Bodenrand. #12 und #15-#18 sind Sandbank-Raender (vielleicht SAND statt SCHNEE).
  - Nicht erfasst: viele kleine Steine unter Zellgroesse (z. B. cx 0-24/cy 216-240 und cx 168-216/cy 240-264). Sie bleiben SCHNEE [A].
- Kachelblaetter r5_3 und r5_4 (y ≥ 216) angesehen: pruefung/t30u_kacheln_r5_3_{0..3}.png und r5_4_{0,1}.png. Fluss, Sandbaenke und Suedwald passen grob. Auffaellig: Bei cx 207-210/cy 295-301 steht ein BODEN-Streifen im Wald (Baumstamm oder Pfad?), unklar, nicht geaendert.
- Linie cx 190-195 / cy 40-100: Das ist ein **zugefrorener Bach** (hellblaue Eisfuellung, doppelte Ufer), kein Weg. Er ist 1 Zelle breit als WASSER_EIS erfasst und passt (pruefung/t30u_linie_cx190.png).
- z50 hat jetzt Overrides (150 Zellen) [R].
- Ungeprueft: ob die z50-Uebernahme an Sandbank-Raendern zu viel oder zu wenig aendert. Die z50-Zellen wurden nicht einzeln angesehen.

## t31u Pruefung
- **TAL_SUED:** Die echten Luecken waren cx 0–25, 56–80 und 246–249. Die Angabe „35–50, 150–152“ aus t30u war falsch abgelesen. Alles in c20 angesehen (pruefung/t31u_talsued_a.png, t31u_talsued_b.png):
  - Westlich von cx 81 gibt es keine Gratwand. Der Block cx 26–55 ist frei stehend. Darum gilt dort WEST [A]; vorher war TAL_SUED an cx 26–55 nicht belegt.
  - Die Schlucht cx 246–249 ist geschlossen [S].
  - Ergebnis: _alt/pruefung/t31u_ebenen.png (ersetzt durch pruefung/t33u_ebenen_vollstaendig.png), selbst angesehen.
  - Offen: Rand cx 329–335.
- **z50-Stichproben** (pruefung/t31u_z50_gipfel.png, t31u_z50_sand_w.png, t31u_z50_sand_m.png, t31u_z50_sand_o.png):
  - Gipfel: Im Umriss liegen 96 WAND, 31 FELS, 17 KANTE und 3 SCHNEE [R]. Die 3 SCHNEE-Zellen sind offen.
  - Sandbänke: Grob richtig. Kleine Bänke sind in z50 teils SCHNEE (zu wenig SAND); beides ist begehbar. Ungeprüft: sand_o habe ich nur erzeugt, nicht einzeln angesehen.
  - Neue Regel: FELS-Regeln gelten ab 1 von 4 z25-Zellen.
- **z50 bebaubar 7 233 → 7 240, erklärt [R]:**
  - +7 Zellen (cx 63–68, cy 22–23): Override 3 (toter Baumstamm KLIPPE_WAND→WALD) gilt jetzt auch in z50. Dadurch liegt die Nordwand-Grenze von senke_becken dort 1–2 Zellen höher, so wie in z25.
  - +1 Zelle (63,49): Overrides 29/30 (X069-Weg FELS→SCHNEE).
  - −1 Zelle (160,26): Findling 421 → FELS.
- **Findlinge 4x** (pruefung/t31u_findling_4x_0.png und _1.png):
  - #1–#9: flache Erdflecken mit Kontur, keine Blockform. Bleibt SCHNEE (beides begehbar), nur Befund.
  - #10 und #12: Rand einer Bodenflaeche. Befund, keine Änderung.
  - #15, #16, #18: dunkler Saum der Sandbank, belegt → SAND (Overrides 425–427).
  - #17: Saum diagonal durch die Zelle, unsicher, bleibt.
- **BODEN-Streifen cx 207–210 / cy 295–301:** In c20 ist das freier graugrüner Waldboden mit Schneebällen, kein Stamm und kein Pfad. BODEN passt, keine Änderung.
- **Konsistenz:**
  - SPEC §3: Die alte Spaltentabelle und die Zaehlung waren überholt und sind ersetzt (Vorfassung _alt/SPEC_t30u.md). Die Angabe „z50 ohne CSV“ war falsch und ist korrigiert.
  - schema_zelle.json: 6 Overlay-Felder entfernt, 8 fehlende Felder ergänzt. Enums passen zu den Daten.
  - Datentyp-Fehler behoben: OVERRI→OVERRIDE, Krat/Sued/Ostg → volle Namen.
  - BAUPLAN_E100.md: §5 auf bebaubar_erweitert aktualisiert, dazu Fels 1, Wald unter Wegen 164, Kapazitaet 27 452 (Vorfassung _alt/BAUPLAN_E100_t26u.md).
  - Ältere Abschnitte im PRUEFPROTOKOLL sind Verlauf und behalten ihre damaligen Zahlen.
- Ungeprüft: Die Zahlen in _alt/ habe ich nicht geprüft. Die Zahlen in älteren pruefung/t1x-Bildern sind nicht neu erzeugt.

## t32u
- Das Bild pruefung/t31u_z50_sand_o.png habe ich selbst angesehen:
  - Der Fluss und der Wald im Süden liegen richtig.
  - Die mittlere und die linke Sandbank sind in z50 nur zur Hälfte SAND, der Rest ist SCHNEE. Auch die Sandzunge unten links ist nur teilweise SAND.
  - Der Grund ist die 2-von-4-Regel bei kleinen Flächen. Beides ist begehbar, deshalb keine Korrektur. Das bleibt als Befund [F].
- Diese Dateien habe ich mit git mv nach _alt/pruefung/ verschoben: kacheln_r4_*, kacheln_r5_* (ersetzt durch t29u/t30u-Kacheln), t30u_ebenen.png (ersetzt durch t31u) und t16u_plaetze_E16/E40.png (ersetzt durch t26u_overlay).
- Die t16u-CSV und -JSON bleiben im Ordner, weil gen_bauzone_befund.py sie als Eingabe liest.
- Neu: INDEX.md und UEBERGABE.md.

## t33u Ebenen-Bild vollständig
- Skriptprüfung [R]: Alle 101 808 z25-Zellen haben eine Ebene, keine ist leer. SENKE 31 265, WEST 29 842, WAND 18 752, TAL_SUED 14 110, PLATEAU_NORD 4 005, OSTPLATEAU 2 014, KRATER 1 820.
- Das alte Bild hatte Lücken, weil WEST und WAND dort nicht eingefärbt waren. In den Daten fehlte nichts.
- Neues Bild: pruefung/t33u_ebenen_vollstaendig.png, erzeugt mit gen_ebenen_bild.py.
  - 4 px je Zelle, Farbe deckend zu 70 % über c20 in Grau.
  - Die Legende zeigt Name, Farbe und Zellzahl.
- Abgleich Pixel zu Zelle [R]: Für alle 1 629 312 Pixel habe ich die Farbe zurückgerechnet und mit `ebene` verglichen. 0 Abweichungen.
- Selbst angesehen. Befund [A], noch offen: An mehreren Stellen ist schmaler Rand als WEST eingetragen, also auf Bezugshöhe:
  - zwischen Kessel und Wänden
  - im Kraterring
  - nördlich der Nordwand
  - am Ostrand
  - In c20 ist das oft Hang- oder Kantenfläche. Die Höhe dort ist nicht belegt.

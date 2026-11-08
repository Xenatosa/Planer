# Ergebnis p3d7

**Status: Ziel nicht erreicht.** Variante 3 erzeugt einen anderen D1-Höhenhash, hält G1 und D2 auf den verlangten Hashes und bleibt unter dem LOD1-Budget. Die Kreuzungsstufe und die D1-R3-Zahl verschlechtern sich gegen p3d6; das Delta-Ziel und mehrere Bildziele werden verfehlt.

- Branch: art/dorfmap-p3d7; Basis: origin/art/dorfmap-p3d6 @ 0cdb862.
- Runtime-Nachweis laut /workspace/codex_jobs/log_p3d7.txt: gpt-6-luna, xhigh.
- Es gab keine Quellzell-, Overlay-, Referenz-, Prüfer- oder Schwellenwert-Änderung. zellen_quell_diff = 0.
- Es wurde nichts gelöscht; Kosten: 0 EUR.

## Änderung

neu/mesh.py fügt einen deterministischen HiGHS-LP für die Profile der D1-Rampen rampe_2 und rampe_11 an deren Schnitt hinzu. Der Solver bildet die R3-Längsformel h - gaussian_filter1d(h, sigma=8) abschnittsweise ab, minimiert Profilbewegung und R3-Schlupf und beschränkt die Profilneigung. Die gemeinsam geführte Ebene deckt den R8-Prüfradius ab; das Profil wird als Wegkorridor mit seitlichem Übergang in die D1-Fläche übertragen. G1 fällt weiterhin auf die p3d6-Kreuzung zurück; D2 wird nicht bearbeitet.

RELIEF_KREUZUNG_VAR=3 ist Standard. 4 vergrößert das Längsfenster, 5 vergrößert die seitliche Anschlussbreite. Die Variablen und Auswahl sind in neu/README.md dokumentiert. neu/README.md, neu/mesh.py, die erzeugten HTML/Build-Dateien, Bilder und dieser Bericht sind die Änderungen.

## Build, Erhaltung und Topologie

Der vorgeschriebene Build lief im Ordner relief3d mit RELIEF_NEU=1 und RELIEF_KREUZUNG_VAR=3 für gen_relief.py, danach RELIEF_NEU=1 für baue_html.py.

| Messung | p3d7 |
|---|---:|
| LOD1-Dreiecke | 134.316 / 1.300.000 |
| Gelände-Dreiecke | 88.728 |
| Wand-Dreiecke | 45.588 |
| Xvfb-Lochscan | offen_innen 0; punkte 0 |
| Eigener vertikaler Raycast gegen die sichtbaren Neu-Mesh-Dreiecke | 88/88 Treffer; 0 ohne Treffer (D1 45/45, G1 36/36, D2 7/7) |
| pruefe_t42u.py | summe 0; alle neun Abweichungsfelder 0 |
| D1 Klippenhöhe bei 140|35 | Quelle 7,8840365 m; p3d6 7,8840365 m; p3d7 7,8840365 m |
| D2 Mesh-Höhenhash | 749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6; bytegleich |
| G1 Mesh-Höhenhash | 38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb; bytegleich |
| D1 Mesh-Höhenhash | bbc2de2fe035800122fae0b222e55247e5cece3d0ebba131447cf41a367c97e2 -> ad0264561c2a825acef64107f926a9118df65f7b18c237464ee616a25ace6004 |
| D1 geänderte Meshvertices | 2.996 |
| D1 größte Höhendifferenz zur Quelle | 5,97074 m bei 144,5|21,5 |
| G1 geänderte Meshvertices | 480; größte Höhendifferenz 0,558914 m |

Der D1-Hashnachweis ist erfüllt; die geforderte lokale Maximalabweichung von 1,33 m wird mit 5,97074 m klar verfehlt. Auch die p3d6-Tests mit einer 4-m-Grenze schlagen deshalb neu an. Die Messung 5,97074 m liegt außerhalb des eigentlichen Rampenprofils in dessen seitlichem Übergang. Die Ursache ist der starke Höhenunterschied zwischen Quellhang und Korridorprofil; das ist eine gemessene Korrelation, keine bewiesene Einzelursache.

Das vorhandene legacy Raycast-Skript test_strahl_t62u.js ist mit dem Neu-Viewer nicht kompatibel, weil dieser keine __test.strahl-Funktion bereitstellt. Für den obigen Nachweis habe ich unter Xvfb die sichtbaren Oberflächenmeshes aus __test.dump gelesen und vertikale Strahlen durch die 88 Objektpositionen gegen deren Dreiecke geprüft. Das belegt Treffer, nicht die Höhentoleranz für schwebende oder versunkene Objekte.

## Variantenvergleich

Die drei Endvarianten wurden mit dem finalen 4-m-Ebenenradius und denselben Adapter-Gates verglichen. Die Messwerte für Regelzähler sind Adapterwerte; p3d6 ist die frisch reproduzierte Variante 2.

| Variante | pruefe_regeln gesamt; R3_längs D1 | R8 gesamt | R8 D1 Schnitt Stufe / Gitter | R8-Endpunkt 156,5|37,5 Stufe / Gitter / Quergefälle | R9 gesamt | Auswahl |
|---|---:|---:|---:|---:|---:|---|
| p3d6, Variante 2 | 563; 10 | 39 | 0,116 / 0,000 m | 0,188 / 0,089 m / 1,4 % | 336 | Ausgang |
| 3 | 567; 13 | 41 | 0,572 / 0,067 m | 0,123 / 0,132 m / 1,4 % | 337 | Standard: niedrigste R8/R9-Summe gemeinsam mit 5 |
| 4 | 571; 15 | 41 | 0,543 / 0,067 m | 0,121 / 0,119 m / 1,4 % | 341 | verworfen, mehr R3 und R9 |
| 5 | 574; 13 | 44 | 0,572 / 0,067 m | 0,288 / 0,428 m / 12,1 % | 337 | verworfen, R8 und Endpunkt schlechter |

Die Korrektur verkleinert die Gitterabweichung, löst die Stufe aber nicht. Bei Variante 3 bleibt der D1-Schnitt um 0,372 m über dem Grenzwert 0,20 m. Das Ende 156,5|37,5 liegt mit 0,123 m unter 0,20 m; R8a wertet dort dennoch 0,12 m gegen eine 0,10-m-Grenze. Ein mathematischer Unmöglichkeitsbeweis für R3 <=6 wurde nicht erbracht. Die beste gemessene Variante hat 13 D1-Treffer, also drei mehr als p3d6 und sieben mehr als VAR0.

## Profil rampe_2 und rampe_11

Station s verwendet die Rohweg-Strecke wie der unveränderte Prüfer; Höhen sind bilinear aus dem sichtbaren GB-Feld an denselben Profilpunkten gelesen. lr_p3d7 ist h minus Gaußprofil (sigma 8), mit Vorzeichen. Werte sind in Metern; s und x|z in Rohwegkoordinaten.

### rampe_2

| s | x|z | h_quelle | h_p3d6 | h_p3d7 | lr_p3d7 |
|---:|---:|---:|---:|---:|---:|
| 14.12 | 140.41|29.93 | 9.483 | 9.483 | 8.544 | +0.068 |
| 18.12 | 144.38|29.44 | 8.168 | 8.168 | 6.225 | -0.075 |
| 22.12 | 148.35|28.96 | 6.776 | 5.169 | 4.524 | -0.239 |
| 26.12 | 152.32|28.47 | 5.691 | 5.030 | 4.419 | -0.010 |
| 30.12 | 156.29|27.99 | 5.009 | 5.029 | 4.448 | +0.075 |
| 34.12 | 160.26|27.50 | 4.108 | 4.108 | 3.967 | +0.075 |
| 38.12 | 164.23|27.02 | 2.987 | 2.987 | 2.840 | -0.059 |

### rampe_11

| s | x|z | h_quelle | h_p3d6 | h_p3d7 | lr_p3d7 |
|---:|---:|---:|---:|---:|---:|
| 22.66 | 156.74|18.24 | 7.302 | 7.302 | 7.302 | +0.073 |
| 26.66 | 156.16|21.48 | 6.198 | 6.198 | 5.664 | -0.075 |
| 30.66 | 154.27|25.01 | 5.066 | 5.032 | 4.631 | -0.113 |
| 34.66 | 152.40|28.54 | 5.604 | 5.030 | 4.423 | -0.024 |
| 38.66 | 150.51|32.06 | 2.739 | 4.894 | 4.224 | +0.273 |
| 42.66 | 152.65|34.69 | 1.468 | 1.507 | 2.388 | +0.054 |
| 46.66 | 155.88|37.05 | 0.614 | 0.614 | 0.614 | -0.220 |


Die exakten D1-R3-Trefferabschnitte p3d7 sind:

| Weg | Abschnittsanfang x|z | max. |h-Gauss8| |
|---|---:|---:|
| rampe_2 | 126.5|31.6 | 0.100 |
| rampe_2 | 134.5|30.6 | 0.122 |
| rampe_2 | 142.4|29.7 | 0.093 |
| rampe_2 | 146.4|29.2 | 0.239 |
| rampe_2 | 150.3|28.7 | 0.083 |
| rampe_11 | 148.5|2.5 | 0.124 |
| rampe_11 | 154.5|16.6 | 0.088 |
| rampe_11 | 157.5|19.1 | 0.089 |
| rampe_11 | 155.6|22.6 | 0.114 |
| rampe_11 | 153.7|26.1 | 0.081 |
| rampe_11 | 151.8|29.6 | 0.273 |
| rampe_11 | 150.4|33.1 | 0.087 |
| rampe_11 | 153.7|35.4 | 0.269 |

### pruefe_regeln

| Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| G11_baum_an_wand | 0 -> 1 (+1) | 0 -> 1 | 0 -> 0 | 0 -> 0 |
| G2_spitze_oben | 3 -> 3 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| G2_spitze_oben_fein | 8 -> 8 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| G3_spitze_unten | 3 -> 3 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| G3_spitze_unten_fein | 2 -> 2 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| G5_beule_klippe | 67 -> 67 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| G6_facette | 216 -> 217 (+1) | 0 -> 1 | 3 -> 3 | 0 -> 0 |
| G7_wand_glatte_flaeche | 1 -> 1 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| G7b_wandkontur_feld | 25 -> 25 (+0) | 1 -> 1 | 0 -> 0 | 0 -> 0 |
| G7b_wandkontur_kantenschaerfe | 1 -> 1 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| G7b_wandkontur_rauheit | 1 -> 1 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| G8_fluss_nicht_bis_rand | 1 -> 1 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| R1_blind | 24 -> 24 (+0) | 2 -> 2 | 1 -> 1 | 0 -> 0 |
| R2_getrennt | 15 -> 15 (+0) | 1 -> 1 | 0 -> 0 | 1 -> 1 |
| R3_laengs_m | 39 -> 42 (+3) | 10 -> 13 | 1 -> 1 | 0 -> 0 |
| R3_quer_pct | 19 -> 18 (-1) | 7 -> 6 | 0 -> 0 | 0 -> 0 |
| R3_woelb_m | 19 -> 18 (-1) | 7 -> 6 | 0 -> 0 | 0 -> 0 |
| R5_loch | 17 -> 18 (+1) | 0 -> 1 | 0 -> 0 | 0 -> 0 |
| R6_wasser_schnee | 4 -> 4 (+0) | 0 -> 0 | 3 -> 3 | 0 -> 0 |
| T1_fleckrand | 94 -> 94 (+0) | 0 -> 0 | 3 -> 3 | 7 -> 7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 -> 1 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 -> 1 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 -> 1 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 -> 1 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |

### R8

| Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| R8_gitter | 8 -> 8 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| R8_quer | 4 -> 4 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| R8_stufe | 7 -> 8 (+1) | 0 -> 1 | 0 -> 0 | 0 -> 0 |
| R8a_wegende | 20 -> 21 (+1) | 0 -> 1 | 0 -> 0 | 0 -> 0 |

### R9

| Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| R8b_delle | 22 -> 22 (+0) | 0 -> 0 | 0 -> 0 | 0 -> 0 |
| R9_saegezahn | 34 -> 34 (+0) | 1 -> 1 | 1 -> 1 | 0 -> 0 |
| R9w_wellen | 280 -> 281 (+1) | 21 -> 22 | 12 -> 12 | 0 -> 0 |


R8/R8a sind in G1 und D2 bei 0 geblieben; D1 hat je einen neuen Treffer: R8_stufe am Schnitt mit 0,572 m und R8a am Wegende. R8_gitter am Schnitt liegt bei 0,067 m; es gibt dort keinen R8_quer-Treffer. D2 hat in keiner der drei Gate-Gruppen einen neuen Treffer.

## Delta-Läufe und einzelne Anstiege

Die Delta-Läufe nutzen frische Adapter-Gates für VAR0, p3d6 und p3d7. Die fünf gemeinsamen Nahbild-Kameras haben Clay-Metriken; die zusätzliche Streiflichtkamera ist nicht in den Deltasnapshot aufgenommen.

VAR0 -> p3d7: 24 Anstiege (Ziel <19 verfehlt); p3d6 -> p3d7: 21 Anstiege (Ziel 0 verfehlt). Beide Delta-Läufe enden mit Code 1 wegen positiver Werte. Alle Anstiege sind unten einzeln mit Einordnung aufgeführt.
### VAR0 -> p3d7: alle positiven Zeilen

| Gruppe | Regel/Metrik | Kachel/Kamera | vorher -> nachher (Δ) | Einordnung |
|---|---|---|---:|---|
| regeln | G11_baum_an_wand | D1 | 0 -> 1 (+1) | Neuer D1-Wandkontakt; wahrscheinlich Höhe/Objektbindung, Objekt nicht isoliert. |
| regeln | G3_spitze_unten_fein | C1 | 0 -> 1 (+1) | Außerhalb D1; bereits im p3d6-Vergleich enthalten. |
| regeln | G6_facette | G1 | 2 -> 3 (+1) | Außerhalb D1; bereits im p3d6-Vergleich enthalten. |
| regeln | G7b_wandkontur_feld | D1 | 0 -> 1 (+1) | D1-Wandkonturtreffer ist gegen p3d6 unverändert; der Anstieg ist nur gegenüber VAR0 vorhanden. |
| regeln | R3_laengs_m | D1 | 6 -> 13 (+7) | D1-Profil: Restabweichung bleibt abschnittsweise über 0,08 m. |
| regeln | R5_loch | D1 | 0 -> 1 (+1) | Neuer D1-Senken-Treffer; Bezug zum Seitenübergang möglich, Ursache offen. |
| r9 | R9w_wellen | D1 | 21 -> 22 (+1) | Zusätzlicher D1-Wellentreffer. |
| r9 | R9w_wellen | F1 | 5 -> 6 (+1) | F1-Wellentreffer ist gegen p3d6 unverändert; der Anstieg ist nur gegenüber VAR0 vorhanden. |
| bild | facetten | D1 / kreuzung | 445 -> 535 (+90) | D1-Profil erzeugt sichtbare Facetten/Grat; Streiflicht bestätigt. |
| bild | kantenzaehne | D1 / kreuzung | 0 -> 28 (+28) | D1-Profil erzeugt sichtbare Facetten/Grat; Streiflicht bestätigt. |
| bild | normale_sprung_inseln | D1 / kreuzung | 94 -> 124 (+30) | D1-Profil erzeugt sichtbare Facetten/Grat; Streiflicht bestätigt. |
| bild | facetten | D1 / wandfuss_140_35 | 382 -> 536 (+154) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | kantenzaehne | D1 / wandfuss_140_35 | 1562 -> 1728 (+166) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | normale_spruenge | D1 / wandfuss_140_35 | 3696 -> 4027 (+331) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | normale_sprung_inseln | D1 / wandfuss_140_35 | 173 -> 434 (+261) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | facetten | D1 / wegende | 787 -> 920 (+133) | Mehr Wegende-Facetten/Flecken; Kontur wirkt stärker gestuft. |
| bild | facetten | D2 / draufsicht | 0 -> 5 (+5) | D2-Mesh bytegleich; Screenshotpixel weichen höchstens 8 Tonwerte ab, Ursache offen. |
| bild | normale_spruenge | D2 / draufsicht | 2266 -> 2275 (+9) | D2-Mesh bytegleich; Screenshotpixel weichen höchstens 8 Tonwerte ab, Ursache offen. |
| bild | normale_sprung_inseln | D2 / draufsicht | 6 -> 9 (+3) | D2-Mesh bytegleich; Screenshotpixel weichen höchstens 8 Tonwerte ab, Ursache offen. |
| bild | flecken | G1 / wandfuss | 21 -> 34 (+13) | G1-Hash und p3d6-Bild sind gleich; Anstieg gegenüber VAR0 geerbt. |
| bild | loch_flecken | G1 / wandfuss | 62 -> 78 (+16) | G1-Hash und p3d6-Bild sind gleich; Anstieg gegenüber VAR0 geerbt. |
| bild | loecher | G1 / wandfuss | 41 -> 44 (+3) | G1-Hash und p3d6-Bild sind gleich; Anstieg gegenüber VAR0 geerbt. |
| bild | normale_spruenge | G1 / wandfuss | 2877 -> 3393 (+516) | G1-Hash und p3d6-Bild sind gleich; Anstieg gegenüber VAR0 geerbt. |
| bild | normale_sprung_inseln | G1 / wandfuss | 172 -> 182 (+10) | G1-Hash und p3d6-Bild sind gleich; Anstieg gegenüber VAR0 geerbt. |
### p3d6 -> p3d7: alle positiven Zeilen

| Gruppe | Regel/Metrik | Kachel/Kamera | vorher -> nachher (Δ) | Einordnung |
|---|---|---|---:|---|
| regeln | G11_baum_an_wand | D1 | 0 -> 1 (+1) | Neuer D1-Wandkontakt; wahrscheinlich Höhe/Objektbindung, Objekt nicht isoliert. |
| regeln | G6_facette | D1 | 0 -> 1 (+1) | Neuer D1-Facettentreffer im geänderten Höhenfeld; die Einzelstelle wurde nicht isoliert. |
| regeln | R3_laengs_m | D1 | 10 -> 13 (+3) | D1-Profil: Restabweichung bleibt abschnittsweise über 0,08 m. |
| regeln | R5_loch | D1 | 0 -> 1 (+1) | Neuer D1-Senken-Treffer; Bezug zum Seitenübergang möglich, Ursache offen. |
| r8 | R8_stufe | D1 | 0 -> 1 (+1) | D1-Kreuzungs-/Wegendeffekt; siehe Einzelwerte oben. |
| r8 | R8a_wegende | D1 | 0 -> 1 (+1) | D1-Kreuzungs-/Wegendeffekt; siehe Einzelwerte oben. |
| r9 | R9w_wellen | D1 | 21 -> 22 (+1) | Zusätzlicher D1-Wellentreffer. |
| bild | facetten | D1 / kreuzung | 351 -> 535 (+184) | D1-Profil erzeugt sichtbare Facetten/Grat; Streiflicht bestätigt. |
| bild | normale_sprung_inseln | D1 / kreuzung | 117 -> 124 (+7) | D1-Profil erzeugt sichtbare Facetten/Grat; Streiflicht bestätigt. |
| bild | facetten | D1 / wandfuss_140_35 | 535 -> 536 (+1) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | flecken | D1 / wandfuss_140_35 | 45 -> 48 (+3) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | kantenzaehne | D1 / wandfuss_140_35 | 1258 -> 1728 (+470) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | loch_flecken | D1 / wandfuss_140_35 | 89 -> 98 (+9) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | loecher | D1 / wandfuss_140_35 | 44 -> 50 (+6) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | normale_spruenge | D1 / wandfuss_140_35 | 3322 -> 4027 (+705) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | normale_sprung_inseln | D1 / wandfuss_140_35 | 333 -> 434 (+101) | Mehr Kerben/Flecken/Normalensprünge; zusätzliche Artefakte im D1-Bild sichtbar. |
| bild | facetten | D1 / wegende | 807 -> 920 (+113) | Mehr Wegende-Facetten/Flecken; Kontur wirkt stärker gestuft. |
| bild | flecken | D1 / wegende | 31 -> 41 (+10) | Mehr Wegende-Facetten/Flecken; Kontur wirkt stärker gestuft. |
| bild | loch_flecken | D1 / wegende | 63 -> 83 (+20) | Mehr Wegende-Facetten/Flecken; Kontur wirkt stärker gestuft. |
| bild | loecher | D1 / wegende | 32 -> 42 (+10) | Mehr Wegende-Facetten/Flecken; Kontur wirkt stärker gestuft. |
| bild | facetten | D2 / draufsicht | 0 -> 5 (+5) | D2-Mesh bytegleich; Screenshotpixel weichen höchstens 8 Tonwerte ab, Ursache offen. |

Die Adapter-Gesamtwerte sind VAR0 -> p3d7: pruefe_regeln 565 -> 567, R8 45 -> 41 und R9 338 -> 337. Gegen p3d6 sind es 563 -> 567, 39 -> 41 und 336 -> 337. Das R3-D1-Delta gegen p3d6 ist +3; gegen VAR0 ist es +7. Die D2-Gate-Zahlen bleiben gleich. p3d6 -> p3d7 hat sieben Gate-Anstiege und vierzehn Bildindikator-Anstiege. VAR0 -> p3d7 hat acht Gate- und sechzehn Bildindikator-Anstiege.

Der direkte Legacy-Lauf bleibt davon getrennt: pruefe_regeln 570, R8 48 (Stufe 9, Gitter 10, Quer 5, Wegende 24), R9 334 (Delle 25, Sägezahn 34, Wellen 275). Die Aufgabenbasis nennt für pruefe_regeln 596; dieser Wert war in p3d6 und p3d7 nicht reproduzierbar. Für das sichtbare Neu-Mesh sind deshalb die Adapterzahlen oben maßgeblich.

## Bilder und Clay-Messung

Gleiche Kameras aus bilder_p3d6/kameras.json. Vorher: bilder_p3d6/mesh/clay. Nachher: bilder_p3d7/mesh/clay. Die zusätzliche D1-Streiflichtansicht entlang rampe_11 liegt unter bilder_p3d7/streiflicht/clay.

| Ansicht | Zähne p3d6 -> p3d7 | Facetten | Normalensprünge | Sprunginseln | Löcher/Flecken |
|---|---:|---:|---:|---:|---:|
| D1 Kreuzung | 51 -> 28 | 351 -> 535 | 802 -> 451 | 117 -> 124 | 0/0 -> 0/0 |
| D1 Wandfuß 140|35 | 1258 -> 1728 | 535 -> 536 | 3322 -> 4027 | 333 -> 434 | 44/45 -> 50/48 |
| D1 Wegende | 887 -> 829 | 807 -> 920 | 2137 -> 2120 | 212 -> 212 | 32/31 -> 42/41 |
| G1 Wandfuß | 911 -> 911 | 530 -> 530 | 3393 -> 3393 | 182 -> 182 | 44/34 -> 44/34 |
| D2 Draufsicht | 313 -> 313 | 0 -> 5 | 2275 -> 2275 | 9 -> 9 | 12/6 -> 12/6 |

Ich habe alle fünf Vorher/Nachher-Paare und die Streiflichtaufnahme angesehen. Am D1-Schnitt ist p3d7 sichtbar gratig und unruhiger; das Streiflicht zeigt eine Kante im Übergang. Am D1-Wandfuß bleiben treppige Kerben und kleine zusätzliche Sprenkel sichtbar. Am D1-Wegende ist die Kontur stärker gestuft. G1 ist byte- und pixelgleich zur p3d6-Aufnahme. D2-Mesh ist bytegleich; die D2-Aufnahme hat 3.294 Pixel mit Abweichungen von 1 bis 8 Tonwerten, kein Pixel weicht um mehr als 8 ab. Der D2-Bildhash unterscheidet sich deshalb trotz identischem Mesh; die Ursache der kleinen Rasterabweichung ist offen.

Die Bildindikatoren sind Sichtproxys, keine geometrische Wahrheit. Sie bestätigen hier aber, dass die D1-Facetten- und Wandfußziele nicht erreicht sind. Insbesondere die geforderte D1-Kreuzungs-Clay-Bedingung gegen p3d6 ist für Facetten verletzt (535 statt höchstens 351).

- D1-Kreuzung: [p3d6](bilder_p3d6/mesh/clay/D1_kreuzung.png) / [p3d7](bilder_p3d7/mesh/clay/D1_kreuzung.png)
- D1-Wandfuß 140|35: [p3d6](bilder_p3d6/mesh/clay/D1_wandfuss_140_35.png) / [p3d7](bilder_p3d7/mesh/clay/D1_wandfuss_140_35.png)
- D1-Wegende: [p3d6](bilder_p3d6/mesh/clay/D1_wegende.png) / [p3d7](bilder_p3d7/mesh/clay/D1_wegende.png)
- G1-Wandfuß: [p3d6](bilder_p3d6/mesh/clay/G1_wandfuss.png) / [p3d7](bilder_p3d7/mesh/clay/G1_wandfuss.png)
- D2-Draufsicht: [p3d6](bilder_p3d6/mesh/clay/D2_draufsicht.png) / [p3d7](bilder_p3d7/mesh/clay/D2_draufsicht.png)
- D1-Kreuzung Streiflicht entlang rampe_11: [p3d7](bilder_p3d7/streiflicht/clay/D1_kreuzung_streiflicht_rampe11.png)

## Annahmen und Grenzen

- VAR0-Gates wurden mit RELIEF_GELAENDE_VAR=0 frisch erzeugt; p3d6-Gates stammen aus einem frischen Bau mit RELIEF_KREUZUNG_VAR=2. Die Clay-Vergleiche verwenden die bereits gespeicherten p3d6-Kontroll- und Meshbilder sowie die p3d7-Bilder mit derselben Kameraliste.
- h_quelle in den Profiltabellen stammt aus dem ursprünglichen sichtbaren GB-Höhenfeld. lr_p3d7 ist an den 0,25-Rohwegschritten mit derselben sigma-8-Gaußformel wie R3 berechnet.
- Die Aufgabenbasiszahl 596 für den direkten pruefe_regeln-Lauf wurde hier nicht reproduziert; der direkte Lauf ergibt 570. Deshalb stehen die Neu-Mesh-Vorher/Nachher-Werte zusätzlich und getrennt in den Adaptertabellen.
- Der Browser-Raycastrun zählt vertikale Treffer auf dem gerenderten Terrainmesh; er prüft keine Objekt-Höhentoleranz und erfasst nur Objekte in den drei Mesh-Kacheln.
- Ein mathematischer Beweis, dass R3 <=6 unmöglich ist, liegt nicht vor. Die ausgewählte Lösung ist nur die beste der drei gemessenen Endvarianten.

## Tests und offene Punkte

pytest -q neu/tests: 23 bestanden, 8 fehlgeschlagen. Die Schwellen und Tests wurden nicht geändert. Fehler:
- test_kreuzung_d1_g1_mesh_stufe: 0,572 m > 0,20 m.
- test_wegende_allgemein_mesh_ohne_blindenden: 21 R8a-Treffer.
- test_saegezahn_d1_mesh_count: D1 weiterhin 46 Zähne.
- test_verwaschene_wand_d1_kantenschaerfe: 2,24 < 3,00.
- test_wegende_f1_c1_meshmessung: F1 0,17 m und kein C1-Wegende.
- test_schattenartefakt_renderbild: 0,307 > 0,25.
- test_profile_mesh_changes_only_d1_and_g1_and_preserves_cliff_and_tile_edges und test_both_profile_options_are_deterministic_and_distinct: D1 max_abs_delta 5,97074 m > 4,0 m.

Offene Punkte:
- Kreuzungsstufe und D1-R3-Längszahl reduzieren, ohne seitliche R8-/R9- oder Bildartefakte zu erzeugen.
- Die Ursache des D1-Quellabstands von 5,97074 m und des neuen R5-Treffers eingrenzen.
- p3d6 -> p3d7-Delta-Anstiege (21) abbauen; VAR0 -> p3d7 bleibt mit 24 über dem Ziel <19.
- D1 Wandfuß, Wegende und Kreuzung visuell verbessern. G1/G7b/Sägezahn/R9w und andere nicht beauftragte Ziele wurden nicht bearbeitet.
- Der direkte Legacy-Raycaster ist nicht für den Neu-Viewer verdrahtet; der separate Browser-Dreieckstest prüft nur Treffer, keine Objekt-Höhentoleranz.

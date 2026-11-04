# Ergebnis Welle 5 – g6c

Stand: Basis `e7a5874`, Arbeitsbranch `art/dorfmap-g6c`, Start-Commit `d410234`. Vergleich und Prüfungen am 04.11.2026.

## Ergebnis

- `pruefe_regeln`: **570 → 534** (−36); `G6_facette` **220 → 189** (−31). `G2_spitze_oben_fein` 8→4 und `G3_spitze_unten_fein` 2→1. `G11_objekt_schwebt_sinkt` bleibt gegenüber der Basis bei **0**; die drei durch g6 veralteten Objekt-Höhen sind korrigiert.
- Keine Regelklasse in `pruefe_regeln`, R8 oder R9 steigt. R8 bleibt **48**, R9 **334**; zusammen sinkt die Summe 952→916.
- Raycast-Lochscan: **0 offene Innenkanten**, 7 Gelände-Meshes, 1.700.454 Dreiecke im Scan. `lod=1`: **1.174.584** gerenderte Dreiecke (<1,3 Mio.). t42u: **Summe 0**.
- D2: G und GB bytegleich; 17 Feinband-IDs und deren h/c/t/s bytegleich; keine Bandzellen- oder Regel-Trefferänderung in D2. `pruefe_regeln` 8→8 (0 neue), R8 0→0, R9 0→0.
- Die Ton-Nahbilder für alle **28 Kacheln mit geänderter Trefferzahl** wurden mit gleicher Kamera, `clay=1`, 960×720 gerendert und paarweise angesehen. Am B5-Fokus **75|195** ist keine neue Treppe, Kerbe oder Falte sichtbar. Auch in den übrigen Paaren sehe ich keine neu entstandene Kante, Treppe, Riss oder Absatz. Die veränderten Zählungen pro Kachel stehen unten; lokale Zunahmen sind damit sichtbar dokumentiert.

## Änderung

`_falten_glatt` verwendete bisher für den Feinmesh die Maximum-Mischung aus Grob- und Feinbandmaske, während das angrenzende Grobnetz nur die Grobmaske erhielt. Damit wurde der Feinmesh in zusätzlichen Bereichen geglättet, an denen das Grobnetz kantig blieb. Die neue Standardvariante `FALT_KOH=1` führt beide Masken vor der Grob- und Feinbandkorrektur zusammen und verwendet so dasselbe Gewicht an beiden Netzen. `FALT_KOH=0` schaltet auf das vorherige Verhalten zurück. D2 bleibt durch die bestehende Feinmaske-Sperre unverändert.

Die in t134u vorgeschlagene sichtflächenbasierte G11-Korrektur wurde ergänzt. Sie setzt nur die y-Koordinate eines Objekts neu, wenn dessen gespeicherte Höhe mehr als 0,6 m von der sichtbaren Feinband-/Grobfläche abweicht. `G11SICHT=0` schaltet diese Korrektur ab. Die drei korrigierten Objekte (alte → neue y-Höhe in m):

| Objekt | x|z | y vorher → nachher | Δy |
|---|---:|---:|---:|
| Baum | 286.25|103.50 | 7.721 → 7.102 | −0.619 |
| Baum | 104.25|211.00 | −0.822 → −1.628 | −0.806 |
| Stein | 205.60|40.28 | 0.321 → 1.069 | +0.748 |

Zellquellwerte, Overlay, Referenzdaten und Prüfer/Schwellen wurden nicht geändert. `zellen_relief.csv` ist nach dem Build auf dem Branch-Stand.

## Prüfprotokoll und Grenzen

Der vorgeschriebene Headless-Aufruf von `loch_o18g.js` lief nach dem Build in `page.waitForFunction` in den 300-s-Timeout, weil Chromium in diesem Headless-Kontext keinen WebGL-Kontext bereitstellte. Prüferdatei und Schwellen blieben unverändert. Für die Messung wurde dieselbe `loch_o18g.js`-Logik aus einer eigenen `/tmp`-Kopie mit `headless:false` gestartet; das ergab 0 offene Innenkanten und 1.700.454 Dreiecke. Die Bilder und `lod=1`-Zählung wurden ebenfalls im sichtbaren Browser gerendert. Das ist eine Ausführungsumgebung-Abweichung, kein Prüfer- oder Schwellenwechsel.

Es bleiben 189 G6-Treffer. Die Kachelwerte steigen lokal in B3, B6, D6, F6, G4, H1 und H5, obwohl die Gesamtregel G6 um 31 sinkt; die Tonpaare dieser Kacheln sind unten verlinkt. Diese Koordinatenverschiebung und die verbleibenden G6-Treffer sind offene Punkte.

## Werte je Regel

### pruefe_regeln

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| `G2_spitze_oben` | 3 | 3 | +0 |
| `G2_spitze_oben_fein` | 8 | 4 | -4 |
| `G3_spitze_unten` | 3 | 3 | +0 |
| `G3_spitze_unten_fein` | 2 | 1 | -1 |
| `G5_beule_klippe` | 68 | 68 | +0 |
| `G6_facette` | 220 | 189 | -31 |
| `G7_wand_glatte_flaeche` | 1 | 1 | +0 |
| `G7b_wandkontur_feld` | 24 | 24 | +0 |
| `G7b_wandkontur_kantenschaerfe` | 1 | 1 | +0 |
| `G7b_wandkontur_rauheit` | 1 | 1 | +0 |
| `G8_fluss_nicht_bis_rand` | 1 | 1 | +0 |
| `R1_blind` | 24 | 24 | +0 |
| `R2_getrennt` | 15 | 15 | +0 |
| `R3_laengs_m` | 35 | 35 | +0 |
| `R3_quer_pct` | 23 | 23 | +0 |
| `R3_woelb_m` | 22 | 22 | +0 |
| `R5_loch` | 17 | 17 | +0 |
| `R6_wasser_schnee` | 4 | 4 | +0 |
| `T1_fleckrand` | 94 | 94 | +0 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 |

### R8

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| `R8_gitter` | 10 | 10 | +0 |
| `R8_quer` | 5 | 5 | +0 |
| `R8_stufe` | 9 | 9 | +0 |
| `R8a_wegende` | 24 | 24 | +0 |

### R9

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| `R8b_delle` | 25 | 25 | +0 |
| `R9_saegezahn` | 34 | 34 | +0 |
| `R9w_wellen` | 275 | 275 | +0 |

## Kacheln (A–H × 1–7)

| Kachel | pruefe_regeln vorher | nachher | R8 vorher | nachher | R9 vorher | nachher |
|---|---:|---:|---:|---:|---:|---:|
| A1 | 11 | 10 | 0 | 0 | 2 | 2 |
| A2 | 9 | 9 | 0 | 0 | 7 | 7 |
| A3 | 1 | 1 | 0 | 0 | 0 | 0 |
| A4 | 0 | 0 | 0 | 0 | 0 | 0 |
| A5 | 0 | 0 | 0 | 0 | 0 | 0 |
| A6 | 0 | 0 | 0 | 0 | 5 | 5 |
| A7 | 3 | 3 | 0 | 0 | 3 | 3 |
| B1 | 4 | 4 | 1 | 1 | 3 | 3 |
| B2 | 1 | 1 | 0 | 0 | 7 | 7 |
| B3 | 13 | 15 | 0 | 0 | 7 | 7 |
| B4 | 22 | 14 | 0 | 0 | 12 | 12 |
| B5 | 15 | 14 | 0 | 0 | 11 | 11 |
| B6 | 4 | 5 | 0 | 0 | 3 | 3 |
| B7 | 1 | 1 | 0 | 0 | 1 | 1 |
| C1 | 7 | 7 | 0 | 0 | 5 | 5 |
| C2 | 7 | 5 | 1 | 1 | 4 | 4 |
| C3 | 45 | 42 | 4 | 4 | 19 | 19 |
| C4 | 32 | 26 | 2 | 2 | 15 | 15 |
| C5 | 48 | 43 | 5 | 5 | 12 | 12 |
| C6 | 11 | 9 | 3 | 3 | 19 | 19 |
| C7 | 4 | 4 | 0 | 0 | 3 | 3 |
| D1 | 36 | 35 | 8 | 8 | 26 | 26 |
| D2 | 8 | 8 | 0 | 0 | 0 | 0 |
| D3 | 11 | 11 | 0 | 0 | 2 | 2 |
| D4 | 23 | 21 | 2 | 2 | 7 | 7 |
| D5 | 4 | 2 | 0 | 0 | 11 | 11 |
| D6 | 16 | 21 | 4 | 4 | 12 | 12 |
| D7 | 1 | 1 | 0 | 0 | 0 | 0 |
| E1 | 13 | 11 | 1 | 1 | 8 | 8 |
| E2 | 14 | 14 | 0 | 0 | 0 | 0 |
| E3 | 9 | 9 | 0 | 0 | 12 | 12 |
| E4 | 9 | 9 | 0 | 0 | 8 | 8 |
| E5 | 1 | 1 | 0 | 0 | 1 | 1 |
| E6 | 5 | 4 | 1 | 1 | 5 | 5 |
| E7 | 8 | 8 | 0 | 0 | 0 | 0 |
| F1 | 16 | 15 | 1 | 1 | 7 | 7 |
| F2 | 6 | 5 | 0 | 0 | 3 | 3 |
| F3 | 0 | 0 | 0 | 0 | 0 | 0 |
| F4 | 3 | 3 | 0 | 0 | 0 | 0 |
| F5 | 14 | 14 | 0 | 0 | 0 | 0 |
| F6 | 7 | 8 | 1 | 1 | 8 | 8 |
| F7 | 4 | 3 | 0 | 0 | 0 | 0 |
| G1 | 13 | 13 | 1 | 1 | 8 | 8 |
| G2 | 4 | 4 | 0 | 0 | 0 | 0 |
| G3 | 14 | 12 | 3 | 3 | 11 | 11 |
| G4 | 16 | 17 | 0 | 0 | 6 | 6 |
| G5 | 4 | 4 | 0 | 0 | 0 | 0 |
| G6 | 11 | 8 | 0 | 0 | 8 | 8 |
| G7 | 0 | 0 | 0 | 0 | 0 | 0 |
| H1 | 2 | 4 | 0 | 0 | 7 | 7 |
| H2 | 9 | 8 | 0 | 0 | 6 | 6 |
| H3 | 4 | 4 | 0 | 0 | 9 | 9 |
| H4 | 7 | 6 | 4 | 4 | 6 | 6 |
| H5 | 19 | 20 | 5 | 5 | 12 | 12 |
| H6 | 18 | 15 | 1 | 1 | 11 | 11 |
| H7 | 1 | 1 | 0 | 0 | 2 | 2 |

## Ton-Nahbilder je Kachel mit geänderter Trefferzahl

Vorher: `e7a5874`-HTML. Nachher: finaler g6c-Build. Alle Bilder verwenden dieselbe Kamera pro Paar (`clay=1`, `lod=0`, Licht Azimut 315°/Höhe 45°/Stärke 60). Fokuskoordinaten stehen in der Tabelle; B5 ist auf den gemeldeten Ort 75|195 gesetzt.

| Kachel | Fokus (x|z) | pruefe_regeln vorher → nachher | Befund | Vorher | Nachher |
|---|---:|---:|---|---|---|
| A1 | 24.1|33.1 | 11 → 10 | 24.1|33.1: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/A1.png) | [PNG](o18/g6c_nach/A1.png) |
| B3 | 70.2|114.2 | 13 → 15 | 70.2|114.2: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/B3.png) | [PNG](o18/g6c_nach/B3.png) |
| B4 | 71.5|156.6 | 22 → 14 | 71.5|156.6: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/B4.png) | [PNG](o18/g6c_nach/B4.png) |
| B5 | 75.0|195.0 | 15 → 14 | 75|195: keine neue Treppe/Kerbe/Falte; die feine Linie am Klippenfuß ist in beiden Bildern vorhanden. | [PNG](o18/g6c_vor/B5.png) | [PNG](o18/g6c_nach/B5.png) |
| B6 | 70.8|215.0 | 4 → 5 | 70.8|215.0: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/B6.png) | [PNG](o18/g6c_nach/B6.png) |
| C2 | 95.8|80.3 | 7 → 5 | 95.8|80.3: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/C2.png) | [PNG](o18/g6c_nach/C2.png) |
| C3 | 104.0|107.4 | 45 → 42 | 104.0|107.4: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/C3.png) | [PNG](o18/g6c_nach/C3.png) |
| C4 | 111.4|153.9 | 32 → 26 | 111.4|153.9: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/C4.png) | [PNG](o18/g6c_nach/C4.png) |
| C5 | 100.7|190.3 | 48 → 43 | 100.7|190.3: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/C5.png) | [PNG](o18/g6c_nach/C5.png) |
| C6 | 103.0|222.6 | 11 → 9 | 103.0|222.6: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/C6.png) | [PNG](o18/g6c_nach/C6.png) |
| D1 | 152.7|18.7 | 36 → 35 | 152.7|18.7: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/D1.png) | [PNG](o18/g6c_nach/D1.png) |
| D4 | 140.2|165.1 | 23 → 21 | 140.2|165.1: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/D4.png) | [PNG](o18/g6c_nach/D4.png) |
| D5 | 147.0|176.1 | 4 → 2 | 147.0|176.1: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/D5.png) | [PNG](o18/g6c_nach/D5.png) |
| D6 | 143.3|232.6 | 16 → 21 | 143.3|232.6: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/D6.png) | [PNG](o18/g6c_nach/D6.png) |
| E1 | 193.0|33.4 | 13 → 11 | 193.0|33.4: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/E1.png) | [PNG](o18/g6c_nach/E1.png) |
| E6 | 200.1|235.7 | 5 → 4 | 200.1|235.7: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/E6.png) | [PNG](o18/g6c_nach/E6.png) |
| F1 | 231.5|28.4 | 16 → 15 | 231.5|28.4: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/F1.png) | [PNG](o18/g6c_nach/F1.png) |
| F2 | 211.8|43.1 | 6 → 5 | 211.8|43.1: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/F2.png) | [PNG](o18/g6c_nach/F2.png) |
| F6 | 233.9|235.7 | 7 → 8 | 233.9|235.7: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/F6.png) | [PNG](o18/g6c_nach/F6.png) |
| F7 | 233.4|268.6 | 4 → 3 | 233.4|268.6: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/F7.png) | [PNG](o18/g6c_nach/F7.png) |
| G3 | 279.6|107.2 | 14 → 12 | 279.6|107.2: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/G3.png) | [PNG](o18/g6c_nach/G3.png) |
| G4 | 280.3|145.1 | 16 → 17 | 280.3|145.1: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/G4.png) | [PNG](o18/g6c_nach/G4.png) |
| G6 | 266.1|234.8 | 11 → 8 | 266.1|234.8: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/G6.png) | [PNG](o18/g6c_nach/G6.png) |
| H1 | 310.7|34.9 | 2 → 4 | 310.7|34.9: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/H1.png) | [PNG](o18/g6c_nach/H1.png) |
| H2 | 316.9|82.8 | 9 → 8 | 316.9|82.8: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/H2.png) | [PNG](o18/g6c_nach/H2.png) |
| H4 | 295.0|157.1 | 7 → 6 | 295.0|157.1: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/H4.png) | [PNG](o18/g6c_nach/H4.png) |
| H5 | 307.8|189.3 | 19 → 20 | 307.8|189.3: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/H5.png) | [PNG](o18/g6c_nach/H5.png) |
| H6 | 317.3|233.3 | 18 → 15 | 317.3|233.3: keine neue sichtbare Kante, Kerbe, Treppe, Riss oder Absatz. | [PNG](o18/g6c_vor/H6.png) | [PNG](o18/g6c_nach/H6.png) |

Zusatzansicht für B5, flacher Blick über den Hang ab 75|195: [vorher](o18/g6c_vor/B5_flach.png), [nachher](o18/g6c_nach/B5_flach.png).

## Annahmen und offene Punkte

- Die sichtbare Geländeoberfläche besteht aus Feinband-Höhen, wo vorhanden, und sonst aus dem Grobnetz; G11 wird daher gegen dieselbe Fläche geprüft.
- `FALT_KOH=1` ist die Standardvariante; die Rückschaltung auf das Vorher-Verhalten erfolgt über `FALT_KOH=0`. `G11SICHT=0` schaltet die Objekt-Höhenkorrektur ab.
- Bildprüfung deckt alle Kacheln ab, deren Gesamtzahl in `pruefe_regeln` zwischen Basis und Ergebnis abweicht. Die Zahlen pro Regel und für alle 56 Kacheln folgen.
- Rest: 189 G6-Treffer. Die lokalen Kachelzunahmen sind keine globalen Regelanstiege; ihre Bilder und Zählungen sind aufgeführt. Die genaue Verteilung neuer und entfallener G6-Koordinaten wurde nicht als dauerhaftes Artefakt abgelegt.
- Kein kostenpflichtiger Dienst und keine Prozesspools verwendet; `RAND=0.6` war für den Lochscan fest vorgegeben.

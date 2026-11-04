# Ergebnis g5r5c — 04.11.2026

**Status: nicht mergefähig nach dem strengen Welle-5-Kriterium.** R5 ist 0 und G5 sinkt, aber G5 bleibt mit 56 über dem Ziel 50; G6 steigt von 220 auf 224. Im Ton-Nahbild bleibt bei G4 eine kleine Einkerbung sichtbar. D2 ist bytegleich, t42u ist 0, R8/R9 und Lochscan sind unverändert bzw. 0.

## Änderung

In [gen_relief.py](../gen_relief.py) ergänzt `_g5_r5_r6_lokal()` eine Korrektur der angezeigten Fläche `GB` und der Feinrelief-Höhen `FW`; Quellfeld `G`, Wasser, Zellquellen und Overlay werden nicht verändert. Standard ist `G5R5_VARIANT=3`, `G5R5_TARGET=0.55`. Variante 3 blendet die G5-Absenkung mit einer 0,35-m-Gaußstütze am Rand ein. Die R5-Füllung beginnt kontinuierlich bei 0,95 m Fülltiefe und prüft bis zu drei Mal auf neu freigelegte Restmulden.

Varianten sind reproduzierbar schaltbar: `G5R5_VARIANT=1|2|3` (Standard 3); `G5R5_LOCAL=0` schaltet die lokale Korrektur aus; `G5R5_TARGET=0.55|0.59` wählt die G5-Zielhöhe. Drei Kandidaten wurden geprüft; es gab keinen vierten Versuch.

| Variante | pruefe_regeln | G5 | R5 | G6 | T1 |
|---|---:|---:|---:|---:|---:|
| 1: additive G5-Stütze, weiche R5-Schwelle | 543 | 48 | 3 | 226 | 95 |
| 2: G5-Gaußkorrektur, kontinuierliche R5-Füllung | 554 | 66 | 0 | 223 | 94 |
| 3: G5-Randüberblendung, kontinuierliche R5-Füllung (Standard) | 545 | 56 | 0 | 224 | 94 |

Variante 3 ist der beste Gesamtkompromiss unter den drei Messungen: R5 bleibt 0, T1 steigt nicht, und die Gesamtzahl liegt bei 545. Sie erfüllt dennoch weder G5≤50 noch G6≤220.

## Prüfungen

| Prüfung | Basis `e7a5874` | g5r5c | Δ |
|---|---:|---:|---:|
| `pruefe_regeln` gesamt | 570 | 545 | −25 |
| `r8_kreuzung` | 48 | 48 | 0 |
| `r9_form` | 334 | 334 | 0 |
| Lochscan `offen_innen` | 0 | 0 | 0 |
| t42u Summe | 0 | 0 | 0 |
| LOD1 gerenderte Dreiecke | 1.700.454 Raycast-Basis | 1.174.670 | <1,3 Mio. |

LOD1 wurde mit `test_dreiecke_l1.js` gemessen (mit und ohne Schatten: jeweils 1.174.670). Der Raycast-Lochscan meldet 7 Meshes, 1.700.454 Dreiecke und `offen_innen=0`. Der vorgeschriebene Aufruf ohne Query lief in `waitForFunction` nach 300 s in den Timeout. Derselbe unveränderte Prüfer lief mit `Q=?nosh=1` erfolgreich und meldete 0 Innenlöcher; die Prüfschwellen wurden nicht geändert.

`python3 pruefung/pruefe_t42u.py` meldet Summe 0. `zellen_relief.csv` wurde nach dem Generatorlauf auf den Branch-Stand zurückgesetzt und ist bytegleich. Hashes nach zwei Standardbuilds waren identisch: `relief_daten.json.gz` `d26e685c56f36aa0e5b7e4c90e212f6696aff16a329ad5d8908b9dd1dbe7caa7`; `index.html` `d756978e6914170c4b013503a41867cb718b89b0ca07c6275f499b98f715c601`.

### Zahlen je Regel

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| `G2_spitze_oben` | 3 | 3 | +0 |
| `G2_spitze_oben_fein` | 8 | 8 | +0 |
| `G3_spitze_unten` | 3 | 3 | +0 |
| `G3_spitze_unten_fein` | 2 | 2 | +0 |
| `G5_beule_klippe` | 68 | 56 | -12 |
| `G6_facette` | 220 | 224 | +4 |
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
| `R5_loch` | 17 | 0 | -17 |
| `R6_wasser_schnee` | 4 | 4 | +0 |
| `T1_fleckrand` | 94 | 94 | +0 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 |

R8 und R9 im Einzelnen:

| R8-Regel | Vorher | Nachher |
|---|---:|---:|
| `R8_stufe` | 9 | 9 |
| `R8_gitter` | 10 | 10 |
| `R8_quer` | 5 | 5 |
| `R8a_wegende` | 24 | 24 |
| **R8 Summe** | **48** | **48** |

| R9-Regel | Vorher | Nachher |
|---|---:|---:|
| `R8b_delle` | 25 | 25 |
| `R9_saegezahn` | 34 | 34 |
| `R9w_wellen` | 275 | 275 |
| **R9 Summe** | **334** | **334** |

G6 ist die einzige Regelklasse mit Anstieg (+4). Sechs neue G6-Komponenten liegen bei `20.7|44.6` (A2), `114.7|112.1` (C3), `86.5|170.4` (C4), `167.3|260.2` (D7), `174.2|261.9` (E7) und `331.9|278.0` (H7); zwei vorherige Komponenten entfallen, netto +4. G5 sinkt netto um 12 Treffer, R5 um 17.

### Treffer je Kachel

`pr` enthält alle `pruefe_regeln`-Treffer der Kachel. Zwei globale Treffer (`feld=-`) sind in der Gesamtsumme enthalten und bleiben 2→2.

| Kachel | `pr` vorher → nachher | R8 vorher → nachher | R9 vorher → nachher |
|---|---:|---:|---:|
| A1 | 11 → 9 | 0 → 0 | 2 → 2 |
| A2 | 9 → 7 | 0 → 0 | 7 → 7 |
| A3 | 1 → 1 | 0 → 0 | 0 → 0 |
| A4 | 0 → 0 | 0 → 0 | 0 → 0 |
| A5 | 0 → 0 | 0 → 0 | 0 → 0 |
| A6 | 0 → 0 | 0 → 0 | 5 → 5 |
| A7 | 3 → 2 | 0 → 0 | 3 → 3 |
| B1 | 4 → 4 | 1 → 1 | 3 → 3 |
| B2 | 1 → 1 | 0 → 0 | 7 → 7 |
| B3 | 13 → 13 | 0 → 0 | 7 → 7 |
| B4 | 22 → 22 | 0 → 0 | 12 → 12 |
| B5 | 15 → 15 | 0 → 0 | 11 → 11 |
| B6 | 4 → 4 | 0 → 0 | 3 → 3 |
| B7 | 1 → 1 | 0 → 0 | 1 → 1 |
| C1 | 7 → 7 | 0 → 0 | 5 → 5 |
| C2 | 7 → 7 | 1 → 1 | 4 → 4 |
| C3 | 45 → 44 | 4 → 4 | 19 → 19 |
| C4 | 32 → 26 | 2 → 2 | 15 → 15 |
| C5 | 48 → 38 | 5 → 5 | 12 → 12 |
| C6 | 11 → 11 | 3 → 3 | 19 → 19 |
| C7 | 4 → 4 | 0 → 0 | 3 → 3 |
| D1 | 36 → 35 | 8 → 8 | 26 → 26 |
| D2 | 8 → 8 | 0 → 0 | 0 → 0 |
| D3 | 11 → 11 | 0 → 0 | 2 → 2 |
| D4 | 23 → 20 | 2 → 2 | 7 → 7 |
| D5 | 4 → 4 | 0 → 0 | 11 → 11 |
| D6 | 16 → 15 | 4 → 4 | 12 → 12 |
| D7 | 1 → 3 | 0 → 0 | 0 → 0 |
| E1 | 13 → 13 | 1 → 1 | 8 → 8 |
| E2 | 14 → 14 | 0 → 0 | 0 → 0 |
| E3 | 9 → 9 | 0 → 0 | 12 → 12 |
| E4 | 9 → 9 | 0 → 0 | 8 → 8 |
| E5 | 1 → 1 | 0 → 0 | 1 → 1 |
| E6 | 5 → 5 | 1 → 1 | 5 → 5 |
| E7 | 8 → 8 | 0 → 0 | 0 → 0 |
| F1 | 16 → 14 | 1 → 1 | 7 → 7 |
| F2 | 6 → 6 | 0 → 0 | 3 → 3 |
| F3 | 0 → 0 | 0 → 0 | 0 → 0 |
| F4 | 3 → 3 | 0 → 0 | 0 → 0 |
| F5 | 14 → 14 | 0 → 0 | 0 → 0 |
| F6 | 7 → 6 | 1 → 1 | 8 → 8 |
| F7 | 4 → 4 | 0 → 0 | 0 → 0 |
| G1 | 13 → 13 | 1 → 1 | 8 → 8 |
| G2 | 4 → 4 | 0 → 0 | 0 → 0 |
| G3 | 14 → 14 | 3 → 3 | 11 → 11 |
| G4 | 16 → 19 | 0 → 0 | 6 → 6 |
| G5 | 4 → 4 | 0 → 0 | 0 → 0 |
| G6 | 11 → 11 | 0 → 0 | 8 → 8 |
| G7 | 0 → 0 | 0 → 0 | 0 → 0 |
| H1 | 2 → 2 | 0 → 0 | 7 → 7 |
| H2 | 9 → 9 | 0 → 0 | 6 → 6 |
| H3 | 4 → 4 | 0 → 0 | 9 → 9 |
| H4 | 7 → 7 | 4 → 4 | 6 → 6 |
| H5 | 19 → 19 | 5 → 5 | 12 → 12 |
| H6 | 18 → 17 | 1 → 1 | 11 → 11 |
| H7 | 1 → 2 | 0 → 0 | 2 → 2 |

D2 hat 8→8 `pr`-Treffer; kein D2-Treffer kommt neu hinzu. R8/R9 bleiben dort bei 0. Die Kacheln mit geänderten `pr`-Trefferzahlen sind A1, A2, A7, C3, C4, C5, D1, D4, D6, D7, F1, F6, G4, H6 und H7.

### Nahbilder und Sichtprüfung

Vorher/Nachher wurden mit denselben Kameras und `?clay=1&lod=0&nosh=1`, 1280×800, gerendert. `nosh=1` schaltet nur Schatten ab. Für jede Kachel mit geänderter Trefferzahl liegen beide Ansichten in `bilder_g5r5c/vor/` und `bilder_g5r5c/nachher/`. Koordinaten sind `x|z` in Metern.

| Kachel | Blick(e) `x|z` | Vorher | Nachher | Sichtbefund |
|---|---|---|---|---|
| A1 | 16|38.5 | [vorher](bilder_g5r5c/vor/A1_R5.png) | [nachher](bilder_g5r5c/nachher/A1_R5.png) | R5-Füllkante wirkt flach; keine neue Kante erkennbar. |
| A2 | 17|50; 30|58.5 | [vorher](bilder_g5r5c/vor/A2_G5.png); [vorher](bilder_g5r5c/vor/A2_R5.png) | [nachher](bilder_g5r5c/nachher/A2_G5.png); [nachher](bilder_g5r5c/nachher/A2_R5.png) | kleine Glättung; keine neue sichtbare Kerbe. |
| A7 | 24|263 | [vorher](bilder_g5r5c/vor/A7_G5.png) | [nachher](bilder_g5r5c/nachher/A7_G5.png) | Kontur leicht gerundet; keine neue Kante auffällig. |
| C3 | 115|110; 101|104 | [vorher](bilder_g5r5c/vor/C3_nord.png); [vorher](bilder_g5r5c/vor/C3_sued.png) | [nachher](bilder_g5r5c/nachher/C3_nord.png); [nachher](bilder_g5r5c/nachher/C3_sued.png) | Änderungen gering; keine neue scharfe Stufe in diesen Blicken. |
| C4 | 121|162; 86.5|170 | [vorher](bilder_g5r5c/vor/C4_ost.png); [vorher](bilder_g5r5c/vor/C4_west.png) | [nachher](bilder_g5r5c/nachher/C4_ost.png); [nachher](bilder_g5r5c/nachher/C4_west.png) | Füllung wirkt weich; keine klare neue Kerbe. |
| C5 | 122|189; 89|176 | [vorher](bilder_g5r5c/vor/C5_berg.png); [vorher](bilder_g5r5c/vor/C5_senke.png) | [nachher](bilder_g5r5c/nachher/C5_berg.png); [nachher](bilder_g5r5c/nachher/C5_senke.png) | Rücken und Senke bleiben ähnlich; kein deutlicher neuer Absatz. |
| D1 | 152|28.5 | [vorher](bilder_g5r5c/vor/D1_G5.png) | [nachher](bilder_g5r5c/nachher/D1_G5.png) | Spitze leicht verändert; keine neue deutliche Kante. |
| D4 | 135|139 | [vorher](bilder_g5r5c/vor/D4_G5.png) | [nachher](bilder_g5r5c/nachher/D4_G5.png) | subtile Formänderung; keine neue Kerbe in diesem Blick. |
| D6 | 151|229; 159|228 | [vorher](bilder_g5r5c/vor/D6_senke.png); [vorher](bilder_g5r5c/vor/D6_rand.png) | [nachher](bilder_g5r5c/nachher/D6_senke.png); [nachher](bilder_g5r5c/nachher/D6_rand.png) | Füllrand weicher als g5r5b; am Übergang bei 151|229 bleibt eine schwache Schulter, vollständige Absatzfreiheit ist nicht belegt. |
| D7 | 167|260 | [vorher](bilder_g5r5c/vor/D7_G5.png) | [nachher](bilder_g5r5c/nachher/D7_G5.png) | kleine neue Einbuchtung am Rücken; passend zu 1→3 Kachel-Treffern. |
| F1 | 223|42 | [vorher](bilder_g5r5c/vor/F1_G5.png) | [nachher](bilder_g5r5c/nachher/F1_G5.png) | leichte Rundung; keine neue scharfe Kante auffällig. |
| F6 | 215|223.5 | [vorher](bilder_g5r5c/vor/F6_G5.png) | [nachher](bilder_g5r5c/nachher/F6_G5.png) | Änderung klein; keine neue Kante auffällig. |
| G4 | 280|139; 274|132 | [vorher](bilder_g5r5c/vor/G4_rand.png); [vorher](bilder_g5r5c/vor/G4_sued.png) | [nachher](bilder_g5r5c/nachher/G4_rand.png); [nachher](bilder_g5r5c/nachher/G4_sued.png) | kleine sichtbare Einkerbung bleibt bei etwa 280|139; Kachel-Treffer steigen 16→19. Ziel nicht erreicht. |
| H6 | 335|249 | [vorher](bilder_g5r5c/vor/H6_G5.png) | [nachher](bilder_g5r5c/nachher/H6_G5.png) | leichte Rundung; keine neue scharfe Kante auffällig. |
| H7 | 332|278 | [vorher](bilder_g5r5c/vor/H7_G5.png) | [nachher](bilder_g5r5c/nachher/H7_G5.png) | kleine Kerbe am Gipfel bleibt sichtbar; Kachel-Treffer steigen 1→2. |

### Unverändertheit D2 und Quellwerte

`G`, `WV`, `VC` und `WEGA` stimmen global byteweise mit `e7a5874` überein. Das D2-Teilfeld von `GB` ist bytegleich. D2-Feinrelief-IDs und Höhen stimmen für alle 17 D2-Stützpunkte byteweise überein. Der D2-Treffervergleich hat keine neuen Treffer. `zellen_relief.csv` ist bytegleich zum Branch-Stand; `main.js` (Overlay) wurde nicht geändert.

### Annahmen, Grenzen und offene Punkte

- Die Kachelgrenzen entsprechen der Prüferzuordnung A–H × 1–7. Globale Treffer ohne Kachel werden separat gezählt.
- Die lokale Korrektur ändert ausschließlich die angezeigte Geländeoberfläche (`GB`, `FW`), nicht das Quellfeld `G` oder die Zellquellwerte.
- Das strenge Merge-Kriterium ist verfehlt: G5 56>50, G6 224>220 und eine sichtbare G4-Einkerbung bei etwa `280|139`. Für D6 ist die Füllkante weicher, aber ein schwacher Absatz bei `151|229` bleibt als offener Sichtpunkt.
- Die drei Varianten schöpfen das Versuchslimit aus. Eine vierte Variante wurde nicht geprüft. Der aktuelle Zweig ist daher ein dokumentierter Zwischenstand, keine Freigabe zum Merge.
- Kein Prüfer und keine Schwelle wurde geändert.

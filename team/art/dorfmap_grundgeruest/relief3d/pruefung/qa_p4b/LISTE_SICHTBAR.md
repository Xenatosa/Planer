# QA P4b: sichtbare Höhen- und Formfehler, alle 56 Kacheln

Stand: `art/dorfmap-fertig` @ dc8c174. Viewer `pruefung/alle_kacheln/alle_kacheln.html` (P10), ohne Schatten (`nosh=1`), damit Schattenakne nicht als Geländefehler zählt. Bewertet wird nur das Gelände. Wege, Wasser und eigene Wände fehlen auf 53 Kacheln, das ist kein Fehler.

Diese Liste ist das Ziel für den Höhenlauf L2.

## Fazit

| Urteil | Anzahl | Kacheln |
|---|---|---|
| stark | 3 | C3, D1, D4 |
| leicht | 17 | B4, C4, C5, C6, D6, E1, E2, E7, F1, F6, F7, G3, G4, G6, H2, H3, H6 |
| sauber | 36 | alle übrigen. A2, E6 und H7 haben einzelne unklare Stellen, siehe unten. |

**Schlimmste Kacheln:**
- **C3:** Sägezahn-Ring um die Mulde und Sägezahn-Kämme auf zwei Graten. Die Kämme sind auch in der Spielansicht aus 40 m deutlich.
- **D1:** Treppen- und Rippenrillen am Hang östlich der Wand. Das ist eine Prototyp-Kachel.
- **D4:** Zahnkante am Blockrand.

**Häufigstes Muster:** Sägezahn oder Kamm auf scharfen Graten und Kanten, also Zickzack im 0,5-m-Raster. Der Messwert `zacke_m` liegt dort meist zwischen 0,7 und 1,8 m.

**Saubere Kacheln:**
- Ebenen und weiche Hänge (A3–A6, F3, F4, G5 usw.) sind ohne Befund.
- Die alten P4-Stellen sind im P10-Mesh nicht mehr zu sehen: C3-Beule, C3-Finne, C5-Horn und die C4-Treppenstufen.

### Bewertungsregeln
- **stark sichtbar:** im 30-m-Quadrantenbild (35°, von Süden) oder in der Kachelübersicht klar erkennbar.
- **leicht sichtbar:** erst im Nahbild (15–25 m) auffällig.
- **Wandzone:** Steilflächen ohne eigene Wand.
  - Senkrechte Streifen auf Steilflächen werden nicht bewertet.
  - Sägezahn-Kämme auf Wandkronen stehen als eigene Kategorie „Wandzone“ in der Liste. Sie könnten mit eigenen Wänden entfallen, bleiben aber sichtbar, solange es keine Wand gibt.

### Messwerte
Die Messwerte kommen aus dem GB-Höhenfeld (`relief_daten.json.gz`, 0,5 m) im Radius 3 m, berechnet mit `messung.py`. Für die Prototyp-Kachel D1 ist GB nur eine Näherung.
- **zacke_m:** größte Abweichung vom 2,5-m-Mittel.
- **hang:** steilste Zellneigung in Grad.

## Liste, nach Schwere sortiert

Die Spalte z ist in Metern. x verläuft nach Osten, z nach Süden.

| Nr | Kachel | x | z (m) | Art | Schwere | Nahbild | Gate-Treffer | Notiz (Messwert) |
|---|---|---|---|---|---|---|---|---|
| 1 | C3 | 94 | 97 | Sägezahn-Ring am Mulden-/Kraterrand | stark sichtbar | [C3_kammQ1](bilder_dc8c174/nah/C3_kammQ1.jpg) | G5 (96,99–101: 0,63–0,96), G6 (94,96:11), R5 (96,101: 1,01) | zacke 0,83 m, hang max 72°. In der C3-Übersicht klar. |
| 2 | C3 | 105–112 | 112–118 | Sägezahn-Kamm auf dem Grat | stark sichtbar | [C3_kamm_spiel](bilder_dc8c174/nah/C3_kamm_spiel.jpg), [C3_kammQ4](bilder_dc8c174/nah/C3_kammQ4.jpg) | G5 (104–117,106–116: 0,61–1,29), G6 (106,116:18), (111,112:14) | zacke 0,81 m. Deutlich in der Spielansicht aus 40 m. |
| 3 | D1 | 145–158 | 15–30 | Treppen- und Rippenrillen (diagonale Stufen) am Hang | stark sichtbar | [D1_rampe_spiel](bilder_dc8c174/nah/D1_rampe_spiel.jpg), [D1_zickzack](bilder_dc8c174/nah/D1_zickzack.jpg), [D1_rampe](bilder_dc8c174/nah/D1_rampe.jpg) | R3q/R3w (146–154,26–30: bis 99°/1,79), G5 (152,28: 0,62) | zacke 0,70 m bei (152,17), 1,79 m bei (151,28). Prototyp-Kachel; das Wandstück steht davor. |
| 4 | C3 | 114,8 | 120,7 | Kamm auf dem linken Grat | stark sichtbar | [C3_kamm_spiel](bilder_dc8c174/nah/C3_kamm_spiel.jpg) | G6 (115,121:25) | zacke 1,66 m, hang max 82°. Die alte P4-„Finne“ ist dort rund; der Kamm sitzt auf der Gratkante. |
| 5 | D4 | 135 | 139 | Zahn- bzw. Kammkante am Blockrand | stark sichtbar (Grenzfall zu leicht) | [D4_falte](bilder_dc8c174/nah/D4_falte.jpg) | G5 (135,139: 1,01), (136,140: 0,78) | zacke 1,70 m, hang max 80°. Im Q1-Bild erkennbar. Das ist die alte P4-Wandfalte. |
| 6 | C4 | 112–121 | 158–168 | Sägezähne auf einem kleinen Simsgrat | leicht sichtbar (Grenzfall zu stark) | [C4_g5](bilder_dc8c174/nah/C4_g5.jpg) | G5 (118–120,166–168: 0,69–1,18), G6 (113,167:26), R5 (122,162: 1,25) | zacke 0,72 m. |
| 7 | D6 | 150–160 | 226–229 | Zwei trapezförmige Tafeln bzw. Stufen am Wandfuß | leicht sichtbar | [D6_tafel_hoch](bilder_dc8c174/nah/D6_tafel_hoch.jpg), [D6_r5](bilder_dc8c174/nah/D6_r5.jpg) | R5 (152,228: 2,57), (159,228: 2,51) | zacke 1,32 / 1,54 m. Geometrische Kastenform an einem natürlichen Wandfuß. |
| 8 | B4 | 74–78 | 145–149 | Zahnreihe an einer kleinen Stufe | leicht sichtbar | [B4_zahn](bilder_dc8c174/nah/B4_zahn.jpg) | nahe G2f (73,142: 0,59), G6 (79,152:48) | zacke 0,89 m, hang max 75°. Aus 15 m scharf zu sehen. |
| 9 | C5 | 104–112 | 180–184 | Sägezahn-Kamm in der Rinnen- bzw. Gratlinie | leicht sichtbar | [C5_zickzackO](bilder_dc8c174/nah/C5_zickzackO.jpg) | G2f (110,180: 0,54), R5 (103,180: 1,52), G6 (109,182:6), G5 (114,182: 0,67) | zacke 0,95 m. |
| 10 | E7/F7 | 199–216 | 273–276 | Gerade Stufenlinie quer durchs Flussbett | leicht sichtbar | [E7_rinne_hoch](bilder_dc8c174/nah/E7_rinne_hoch.jpg), [F7_rinne](bilder_dc8c174/nah/F7_rinne.jpg) | G3 (199,275: 0,45), (207,275: 0,53), G2/G3 (212–216,275–276: 0,48–0,57) | zacke 0,60 m. Das Wasser fehlt noch; mit Wasser eventuell verdeckt. |
| 11 | C4/C5 | 84–95 | 168–176 | Gezackte Gratkante | leicht sichtbar | [C4C5_zickzack](bilder_dc8c174/nah/C4C5_zickzack.jpg) | R5 (85,172: 1,37), (86–93,174–176: 1,0–1,55), G5 (84,175: 0,61) | zacke 3,44 m: höchster Wert der Liste, liegt aber an einer Steilkante. |
| 12 | D6 | 133–138 | 231–236 | Sägezahnlinie am Hangrand mit kleiner Spitze | leicht sichtbar | [D6_zickzackW](bilder_dc8c174/nah/D6_zickzackW.jpg) | G6 (134,232:14), R3 (134–138,231–232) | zacke 0,65 m. |
| 13 | G4 | 274 / 281 | 133 / 139 | Aufgeblähte, kissenförmige Felsblöcke mit kleinem Zickzack am Fuß | leicht sichtbar | [G4_g5a](bilder_dc8c174/nah/G4_g5a.jpg), [G4_g5b](bilder_dc8c174/nah/G4_g5b.jpg), [G4_zickzack](bilder_dc8c174/nah/G4_zickzack.jpg) | G5 (274,133: 4,44), (281,139: 2,53) | zacke 1,05 / 0,79 m. Form weich, nicht spitz. |
| 14 | E1 | 181 | 20 | Dünner senkrechter Splitter bzw. Finne an der Klippenecke | leicht sichtbar (Wandzone) | [E1_krone_hoch](bilder_dc8c174/nah/E1_krone_hoch.jpg) | – (nächster G6 bei 185,24:8) | zacke 2,72 m, hang max 85°. |
| 15 | C6 | 97 | 221 | Dunkler Trichter bzw. Mulde am Wandfuß (im Clay-Bild deutlich) | leicht sichtbar | [C6_knollen_hoch](bilder_dc8c174/nah/C6_knollen_hoch.jpg) | G6 (100,220:12), (98,218:7) | zacke 0,53 m. |
| 16 | H6 | 315 | 226 | Kleine Kammzähne auf der Wandkrone | leicht sichtbar (Wandzone) | [H6_g6](bilder_dc8c174/nah/H6_g6.jpg) | G6 (315,226:36) | zacke 1,14 m. |
| 17 | H3 | 316 | 90 | Kleine Knubbel am Terrassenrand | leicht sichtbar | [H3_g6](bilder_dc8c174/nah/H3_g6.jpg) | G6 (316,90:58) | zacke 0,48 m. |
| 18 | H2 | ≈322–330 | ≈65–69 | Kammzähne auf dem Grat und eine Spitze am Kartenrand | leicht sichtbar (Wandzone) | [H2_zickzack](bilder_dc8c174/nah/H2_zickzack.jpg) | G7b (315,64: 0,67) | zacke 0,79 m bei (330,69). Die Kamera aus 15 m kam nicht ran (Kartenrand); erst das Bild aus 20 m zeigt die Stelle. |
| 19 | G3 | ≈285 | ≈108 | Kleine Spitzen bzw. ein Knick am Rücken | leicht sichtbar | [G3_huegel](bilder_dc8c174/nah/G3_huegel.jpg) | G6 (286,104:20) | zacke 0,22 m. Knapp, eher Form als Zacke. |
| 20 | E2 | ≈200 | 55–60 | Feiner Zickzack an der Uferkante der Bachrinne | leicht sichtbar | [E2_bach](bilder_dc8c174/nah/E2_bach.jpg) | G6 (197,57:6) | zacke 0,26 m. Mit Wasser eventuell verdeckt. |
| 21 | F6 | Wandkrone (aus dem Kachelbild) | – | Kamm auf der Krone | leicht sichtbar (Wandzone) | [Kachel F6](bilder_dc8c174/kacheln/F6.jpg) | G5 (215,224: 0,85) in der Nähe | Nur im Kachelbild gesehen, Stelle nicht vermessen. |
| 22 | F1 | Wandkrone (aus dem Kachelbild) | – | Kamm auf der Krone | leicht sichtbar (Wandzone) | [Kachel F1](bilder_dc8c174/kacheln/F1.jpg) | G6 (212,18:25) in der Nähe | Nur im Kachelbild gesehen, Stelle nicht vermessen. Die G5-Knollen (223,41) selbst sind rund und unauffällig. |
| 23 | G6 | ≈283 | ≈226 | Dunkle Kerbe bzw. Kammkante an der Krone | leicht sichtbar (Wandzone) | [G6_krone](bilder_dc8c174/nah/G6_krone.jpg) | – | zacke 0,65 m. Grenzfall, Wandzone. |

## Übersicht aller 56 Kacheln

Zu jeder Kachel gibt es ein Übersichtsbild unter `bilder_dc8c174/kacheln/<Kachel>.jpg` (U plus Q1–Q4).

| Kachel | Urteil | Kurz | Kachel | Urteil | Kurz |
|---|---|---|---|---|---|
| A1 | sauber | Steilwände, nur senkrechte Streifen | E1 | leicht | Splitter (181,20), Kronenkamm |
| A2 | sauber | Becken wirkt natürlich (G5/R5/G8) | E2 | leicht | Zickzack am Ufer (200,57) |
| A3 | sauber | – | E3 | sauber | – |
| A4 | sauber | – | E4 | sauber | – |
| A5 | sauber | – | E5 | sauber | weiche Rille (189,189) |
| A6 | sauber | – | E6 | sauber | flaches dunkles Band (178,231) unklar, eher sauber |
| A7 | sauber | G5 am Ufer unauffällig | E7 | leicht | Stufenlinie im Flussbett |
| B1 | sauber | kleine Kerbe (81,42) nur aus 20 m zu sehen | F1 | leicht | Kronenkamm (Wandzone) |
| B2 | sauber | – | F2 | sauber | – |
| B3 | sauber | Fleck (64,115) ist nur Textur | F3 | sauber | – |
| B4 | leicht | Zahnreihe (76,147) | F4 | sauber | – |
| B5 | sauber | – | F5 | sauber | feine Rille (213,195) nur nah zu sehen |
| B6 | sauber | – | F6 | leicht | Kronenkamm (Wandzone) |
| B7 | sauber | – | F7 | leicht | Stufenlinie Flussbett (214,276); Knollen (243,273) unklar |
| C1 | sauber | – | G1 | sauber | Wandflächen ohne Befund |
| C2 | sauber | – | G2 | sauber | – |
| C3 | **stark** | Kraterring (94,97), Gratkämme | G3 | leicht | Rückenknick (285,108) |
| C4 | leicht | Simszähne (118,162), Gratzacken zu C5 | G4 | leicht | Kissenblöcke (274,133), (281,139) |
| C5 | leicht | Kamm (106,182); alter Horn rund | G5 | sauber | – |
| C6 | leicht | Trichter am Wandfuß (97,221) | G6 | leicht | Kronenkerbe (283,226), Wandzone |
| C7 | sauber | – | G7 | sauber | Flussbett weich |
| D1 | **stark** | Treppenrillen (152,17–28) | H1 | sauber | Wand ohne Befund |
| D2 | sauber | Prototyp | H2 | leicht | Gratkamm und Randspitze (330,69) |
| D3 | sauber | – | H3 | leicht | Knubbel (316,90) |
| D4 | **stark** | Zahnkante (135,139) | H4 | sauber | – |
| D5 | sauber | „Splitter“ (162,208) nicht auffindbar | H5 | sauber | Kissen (306,185), (305,204) unauffällig |
| D6 | leicht | Tafeln (152/159,228), Sägelinie (135,234) | H6 | leicht | Kronenkamm (315,226) |
| D7 | sauber | – | H7 | sauber | Bettknollen (310,272) unklar |

## Unklar (mit Grund)

| Kachel | Stelle | Grund |
|---|---|---|
| F7, H7, G7 | Knollen im Flussbett (243,273), (310,272) | Es sind runde Brocken im leeren Bett. Ob sie stören, lässt sich erst mit Wasser beurteilen. |
| D5 | „Splitter“ (162,208), (165,214) | An der Stelle ist nichts zu sehen; zacke 0,00 m. Nicht auffindbar, vermutlich sauber. |
| E6 | (178,231) | Nur ein flaches dunkles Band; zacke 0,27 m. Eher Textur bzw. Schattierung, vermutlich sauber. |
| H2 | Grat (322,65), Bild aus 15 m | Die Kamera liegt am Kartenrand, in zwei Versuchen ist nichts erkennbar. Das Bild aus 20 m (H2_zickzack) zeigt einen Kamm, darum steht H2 oben als „leicht“. |
| F1, F6 | Kronenkamm | Gesehen nur im Kachelbild, Koordinate nicht vermessen. |

## Nebenbefunde (kein Gelände-Höhenfehler, nur zur Weitergabe)

1. **Schattenakne im P10-Viewer:** In Nahbildern mit Schatten erscheinen streifige Muster. Das ist ein Problem der Schatten-Bias und gehört an Dev UI. Alle Bilder hier sind mit `nosh=1` gerendert.
2. **Haarlinien entlang der Kachelnähte:** dünne dunkle Linien, z. B. in B4, F5, A1.
3. **Dunkle Wandobjekte aus D1/G1 stehen frei über dem Gelände bzw. dem Kachelrand:**
   - T-förmige Stücke in G1 bei ≈(265–275, 28–35).
   - Pfeiler in C1, C2, D1, D2, F1, F2, G2 und G3.
4. **Senkrechte Streifen auf Steilflächen (Wandzone):** Sie werden bewertet, wenn eigene Wände da sind.
5. **Alte P4-Stellen, im P10-Mesh weg:**
   - C3-Beule (125,5, 96,2): glatter Kegel.
   - C3-Finne (114,8, 120,7): runder Hügel, Kamm nur an der Gratkante (Nr. 4).
   - C5-Horn (123,5, 185,8): rund.
   - C4-Treppenstufen: nicht vorhanden.

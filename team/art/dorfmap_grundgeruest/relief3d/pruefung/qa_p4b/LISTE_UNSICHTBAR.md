# QA P4b: Ausnahme-Kandidaten (Gate-Treffer ohne sichtbaren Fehler)

Stand: dc8c174. Diese Gate-Treffer wurden nachgesehen und zeigen im Bild keinen sichtbaren Höhen- oder Formfehler. Nach Fabians Regel („Optik ist alles“) kommen sie auf die Ausnahmeliste. Schwellen und Checker bleiben unverändert.

- Messwerte kommen aus `messung.py` (GB, Radius 3 m), Treffer aus `regeln_letzter_lauf.json` (siehe `gate_treffer_je_kachel.txt`).
- Nahbilder liegen unter `bilder_dc8c174/nah/`, links Farbe, rechts Clay.

| Kachel | Gate-Treffer (x,z:Wert) | Messwert (zacke_m / hang max) | Nahbild | Befund |
|---|---|---|---|---|
| A2 | G5 (21,45: 1,05), (17,50: 1,09); R5 (10,48: 1,06), (30,58: 1,07); G8 (22,49) | 0,56 m / 48° | [A2_basin](bilder_dc8c174/nah/A2_basin.jpg) | Becken mit natürlicher Form; keine Zacke, kein Loch zu sehen. |
| A7 | G5 (26,262: 1,3), (22,264: 1,05), (24,264: 0,9) | 0,40 m / 50° | [A7_ufer](bilder_dc8c174/nah/A7_ufer.jpg) | Uferhang glatt. |
| B3 | G6 (79,126: 103) | 0,16 m / 43° | [B3_g6](bilder_dc8c174/nah/B3_g6.jpg) | Hang glatt. Hoher G6-Wert, aber nichts zu sehen. |
| B3 | G6 (65,116: 11), (63,125: 13) | 0,29 m / 54° | [B3_flecken](bilder_dc8c174/nah/B3_flecken.jpg) | Brauner, rechteckiger Fleck: nur Textur, keine Form im Clay. |
| B4 | G6 (64,161: 42) | 0,08 m / 40° | [B4_g6b](bilder_dc8c174/nah/B4_g6b.jpg) | Glatt. |
| B4 | G6 (57,151: 16), (59,142: 13) | 0,11 m / 24° | [B4_flanke](bilder_dc8c174/nah/B4_flanke.jpg) | Flanke glatt. |
| C3 | G5 (126,96: 2,27) | 0,63 m / 69° | [C3_beule](bilder_dc8c174/nah/C3_beule.jpg) | Die alte P4-Beule ist jetzt ein glatter Kegel. |
| C4 | R5 (99,139: 1,12) | 1,14 m / 77° | [C4_r5_hoch](bilder_dc8c174/nah/C4_r5_hoch.jpg) | Wandecke; kein Loch zu sehen. |
| C4 | G5 (124,150: 0,65) | 0,62 m / 56° | [C4_buckel](bilder_dc8c174/nah/C4_buckel.jpg) | Weicher Buckel. |
| C5 | R5 (95,177) bzw. (93,174: 1,0) | 1,63 m / 80° | [C5_r5](bilder_dc8c174/nah/C5_r5.jpg) | Kein Loch zu sehen. Die gezackte Gratkante daneben ist sichtbar (LISTE_SICHTBAR Nr. 11). |
| C5 | G5 (114,200: 2,63), (112,200: 1,98), (114,201: 1,62) | 1,39 m / 80° | [C5_g5](bilder_dc8c174/nah/C5_g5.jpg) | Steilkante glatt, keine Beule. |
| C5 | G5 (123,185: 0,83), (124,186: 0,91) | 1,05 m / 63° | [C5_horn](bilder_dc8c174/nah/C5_horn.jpg) | Das alte P4-Horn ist rund. |
| E6 | G6 (201,235: 40) | 0,09 m / 25° | [E6_g6](bilder_dc8c174/nah/E6_g6.jpg) | Glatt. |
| F1 | G5 (222,41: 0,68), (223,42: 1,07), (224,42: 0,97) | 2,16 m / 83° | [F1_g5](bilder_dc8c174/nah/F1_g5.jpg) | Runde Knollen, natürlich wirkend. |
| G3 | G6 (277,99: 30) | 0,52 m / 70° | [G3_g6](bilder_dc8c174/nah/G3_g6.jpg) | Unauffällig. |
| G3 | G5 (276,114: 1,25) | 0,24 m / 50° | [G3_zickzack](bilder_dc8c174/nah/G3_zickzack.jpg) | Rückenkante weich. |
| H5 | G6 (306,193: 24), (305,204: 6) | 0,87 / 0,41 m | [H5_kissenA](bilder_dc8c174/nah/H5_kissenA.jpg), [H5_kissenB](bilder_dc8c174/nah/H5_kissenB.jpg) | Weiche Kissen, unauffällig. |
| H6 | (304,247), ohne Gate-Treffer, nur Sichtprüfung | 0,00 m / 0,6° | [H6_delle](bilder_dc8c174/nah/H6_delle.jpg) | Fleck in Farbe, im Clay keine Delle: nur Textur. |
| G7 | keiner (Flussbett 258,281) | 0,07 m / 20° | [G7_bett](bilder_dc8c174/nah/G7_bett.jpg) | Flussbett weich. |
| B1 | G6 (62,37: 31); Zickzack-Suche (81,42) | 1,32 m / 81° | [B1_zickzack](bilder_dc8c174/nah/B1_zickzack.jpg) | Kleine Kerbe an der Kante, erst aus 20 m zu sehen. Grenzfall. |
| F5 | G6 (218,198: 27), (215,199: 10) | 0,36 m / 50° | [F5_zickzack](bilder_dc8c174/nah/F5_zickzack.jpg) | Feine Rille an der Kante, nur nah zu sehen. Grenzfall. |
| E5 | G6 (189,184: 8) | – | [E5_zickzack](bilder_dc8c174/nah/E5_zickzack.jpg) | Natürliche Rinne. |
| H4 | G6 (294,157: 6), (296,158: 6) | – | [H4_zickzack](bilder_dc8c174/nah/H4_zickzack.jpg) | Unauffällig. |
| A1, G1, H1 | G6 an Steilwänden, z. B. A1 (16,32: 12), G1 (277,22: 15), H1 (317,33: 12) | Wandzone | [A1_zickzack](bilder_dc8c174/nah/A1_zickzack.jpg), [G1_zickzack](bilder_dc8c174/nah/G1_zickzack.jpg), [H1_zickzack](bilder_dc8c174/nah/H1_zickzack.jpg) | Nur senkrechte Streifen auf der Wand, keine Zacke an der Krone. |

Nicht einzeln nachgesehen wurden die kleinen G6-Treffer (Wert 6–15) in Kacheln, die im Kachelbild sauber wirken: B5, B6, B7, C1, C2, C7, E3, E4, D5, D7, G6, H4 und H5. Ohne Nahbild sind sie keine Ausnahme-Kandidaten. Werden sie gebraucht, folgt ein Nahbild über `PUNKTE`.

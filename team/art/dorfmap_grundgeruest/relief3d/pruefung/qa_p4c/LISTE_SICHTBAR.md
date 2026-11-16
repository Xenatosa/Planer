# QA P4c: sichtbare Fehler, alle 56 Kacheln, jetzt mit Wegen und Wasser

Stand: `art/dorfmap-fertig` @ 8cd6d37 (L3 eingespielt, PR 7 = cc2a02b gemergt). Viewer `pruefung/alle_kacheln/alle_kacheln.html`, gebaut mit `baue_alle_kacheln.py` (56 Kacheln, Naht max 0 m, Wand-Dreiecke 0). Wege und Wasser werden mitgerendert.

**Alle Bilder ohne Schatten (`nosh=1`).** Mit Schatten stört Schattenakne auf Steilflächen; sie würde sonst als Geländefehler gelesen. Wenn ein Befund nur mit Schatten auftreten sollte, ist er hier nicht erfasst.

Bewertung wie P4b:
- **stark:** im 30-m-Quadrantenbild (35°, von Süden) oder in der Kachelübersicht klar erkennbar.
- **leicht:** erst im Nahbild (15–25 m) auffällig.
- **Wandzone:** senkrechte Streifen auf Steilflächen werden nicht bewertet.

Bilder: `bilder_8cd6d37/vn/` = vorher (P4b, dc8c174, oben) / nachher (P4c, 8cd6d37, unten), gleiche Kamera, je links Farbe, rechts Ton. `bilder_8cd6d37/nah/` = neue Nahbilder (Farbe | Ton). `bilder_8cd6d37/kacheln/` = Kachelübersicht U + Q1–Q4. Messwerte: `messung_23_nachher.json`, `messung_p4c.json` (GB-Höhenfeld, Radius 3 m).

## Fazit

| Urteil Gelände | Anzahl | Kacheln |
|---|---|---|
| stark | 4 | D1, E2, E7, F7 – alle vier sind Stellen in Arbeit (03, 20, 10) |
| leicht | 5 | C4, D4, D5, E1, G6 |
| sauber | 47 | alle übrigen |

- **L3 hat gewirkt.** Von den 23 P4b-Stellen sind **18 nicht mehr sichtbar** (17 weg, dazu F1 unauffällig). E1 (14) ist nur teilweise besser. 03 D1, 10 E7/F7 und 20 E2 bleiben stark; 23 G6 ist teilweise besser. Diese fünf sind schon in Arbeit (P2b/L3b) und zählen nicht als neue Befunde.
- **40 neue L3-Treffer: 7 sichtbar, 33 unsichtbar.** Sichtbar sind T11–T15 an der Naht C4/D4 und T17/T37 an der D1-Rampe (gehört zu 03).
- **Rand C4/D4 (x 124–128): ja, wirkt wolkig.** Zwei Dinge:
  1. Eine harte, gerade senkrechte Helligkeitslinie genau auf x = 126 (z ≈ 133–160), in Farbe und Ton. Die Höhen an der Naht sind gleich (0 m), es ist ein Sprung in der Schattierung. Daneben wirkt die Gratzone unruhig und fleckig.
  2. Ein milchiges, texturarmes Band läuft von D4 (≈130–140|147) nach C5/D5 (≈117–135|185). Laut Gate ist das `rampe_5` (R1_blind / R3_laengs_m bei 134,3|149,3). Die geglättete Rampe hat dort weder Wegtextur noch Geländezeichnung.
  - Aus 20 m deutlich, aus 40 m von Süden schwach, aus 35 m von Osten nicht zu sehen. Urteil: **leicht** in der Spielansicht, im Nahbild Grenzfall zu stark.
  - Dieselbe Nahtlinie gibt es schwach auch an B6/C6 (x = 84, [N12](bilder_8cd6d37/nah/N12_B6C6_naht_hang.jpg)). Sie ist also eher allgemein und an C4/D4 nur am stärksten.
- **P2-Kandidaten: beide unsichtbar.** G2_fein C5 (107,8|183,8): glatter Hang. G7b_feld D3 (147|107): flache Wiese neben dem Weg. Details in `LISTE_UNSICHTBAR.md`.
- **Neue Top-Stellen, alle an Wasser und Wegen (Nebenbefunde, siehe unten):**
  1. **G7 (≈258–262|266–276):** Treppen- und Leiterstrukturen sowie gerade helle Linien stoßen durch das Wasser.
  2. **Brücken fehlen E2/E3:** Wege enden beidseits am Bach mit braunen L-Brettstummeln, aber keine Brücke führt übers Wasser. Gesehen bei (≈184|87)/(≈193|87) und (≈187|75)/(≈196|75), dazu einzelne Bretter in F2 (≈213|80) und F3 (≈211|95).
  3. **C7 (≈90–100|278–282):** helle Platten mit Treppenrand mitten im Fluss.
  4. **H7 (≈315–335|268–280):** helle Geländeblöcke im Wasser, treppiger Wasserrand.
  5. **E3 Bachufer (≈188–192|95–125):** Sägezahn- bzw. Treppenrand im 0,5-m-Raster, schon in der Übersicht sichtbar.

## Liste, nach Schwere sortiert (Gelände)

x läuft nach Osten, z nach Süden, beides in Metern. Stellen in Arbeit sind nur mit ihrem Zustand vermerkt.

| Kachel | x | z | Art | Schwere | Nahbild | Gate-Treffer | Notiz |
|---|---|---|---|---|---|---|---|
| D1 | 145–158 | 15–30 | Treppen- und Rippenrillen an `rampe_2`/`rampe_8` (Stelle 03) | stark – **in Arbeit (P2b/L3b)** | [D1_rampe_spiel](bilder_8cd6d37/vn/D1_rampe_spiel.jpg), [D1_zickzack](bilder_8cd6d37/vn/D1_zickzack.jpg), [T17](bilder_8cd6d37/nah/T17_G6_D1.jpg), [T37](bilder_8cd6d37/nah/T37_G7b_D1.jpg) | R3q/R3w (150,3\|28,7: 99 %/1,79 m), (151,8\|29,6: 99 %/1,56 m), G6 (157,4\|24,2), G7b (147\|21), R2 (150,9\|23,6: 116) | Der Hang ist glatter, aber die Rillen direkt an der Rampe bleiben. Ohne Wandkörper liegen sie jetzt frei. zacke D1_rippen 1,79 → 1,75 m. |
| E7/F7 | 195–216 | 273–276 | Gerade helle Linie quer übers Wasser; helle Geländeplatten ragen aus dem Wasser (≈195–200\|275, 216\|274); Treppenrand (Stelle 10) | stark – **in Arbeit** | [E7_rinne_hoch](bilder_8cd6d37/vn/E7_rinne_hoch.jpg), [F7_rinne](bilder_8cd6d37/vn/F7_rinne.jpg) | G3 (199,275), (207,275), G2/G3 (212–216,275–276) | Wasser verdeckt die Stufe nicht, die Linie liegt sichtbar über dem Wasser. zacke 0,60 / 0,61 m (unverändert). |
| E2 | ≈195–200 | 55–80 | Starker Sägezahn am Ufer der Bachrinne (Stelle 20) | stark – **in Arbeit** | [E2_bach](bilder_8cd6d37/vn/E2_bach.jpg), [N02](bilder_8cd6d37/nah/N02_E2_bretter.jpg) | G6 (197,57), (190,5\|71,1), (188,4\|78,1) | Mit Wasser deutlicher als vorher: Der helle Treppenrand zeichnet das Wasser nach. zacke 0,26 m (unverändert). |
| C4/D4 | 124–128 | 133–160 | Gerade senkrechte Helligkeitslinie auf der Naht x = 126; daneben unruhige, fleckige Gratzone | leicht (Nahbild Grenzfall zu stark) | [z133](bilder_8cd6d37/nah/C4D4_rand_z133.jpg), [z145](bilder_8cd6d37/nah/C4D4_rand_z145.jpg), [z157](bilder_8cd6d37/nah/C4D4_rand_z157.jpg), [z168](bilder_8cd6d37/nah/C4D4_rand_z168.jpg), [Süd 40 m](bilder_8cd6d37/nah/C4D4_rand_sued.jpg), [Ost 35 m](bilder_8cd6d37/nah/C4D4_rand_ost.jpg) | G5 T11–T15 (126,0\|138,0 … 125,0\|150,5: 0,61–1,48), R2 (125,9\|165,4: 58) | Naht-Höhe 0 m, also ein Normalen- bzw. Schattierungssprung. zacke 0,66 / 0,92 / 0,23 / 0,06 m (z 133/145/157/168). Bei z 168 ist nichts mehr zu sehen. |
| D4/D5 (C5) | ≈117–140 | 147–200 | Milchiges, texturarmes Band entlang `rampe_5` („wolkig“) | leicht | [N04](bilder_8cd6d37/nah/N04_D4_milchstreifen.jpg), [N05](bilder_8cd6d37/nah/N05_D5_milchfleck.jpg), [Kachel D4](bilder_8cd6d37/kacheln/D4.jpg), [Kachel D5](bilder_8cd6d37/kacheln/D5.jpg) | R1_blind rampe_5 (117,1\|185,4 / 135,4\|146,8), R3_laengs (134,3\|149,3: 0,112) | Im Ton ist es eine weiche, breite Rampe, also formal ok. In Farbe wirkt es wie ein Nebelstreifen ohne Weg. zacke 0,10 / 0,00 m. |
| E1 | 181 | 20 | Dünne Finne an der Klippenecke (Stelle 14) | leicht (Wandzone) | [E1_krone_hoch](bilder_8cd6d37/vn/E1_krone_hoch.jpg) | – | Dünner als vorher, aber noch zu sehen. zacke 2,72 → 1,04 m. |
| G6 | ≈283 | ≈222–226 | Feine Zähne an der Kronenkante (Stelle 23) | leicht – **in Arbeit** | [G6_krone](bilder_8cd6d37/vn/G6_krone.jpg), [T35](bilder_8cd6d37/nah/T35_G6_G6.jpg), [T36](bilder_8cd6d37/nah/T36_G6_G6.jpg) | G6 T35/T36 (287,2\|221,2), (283,8\|222,3) | Die Kerbe ist weg, die Randzähne bleiben. zacke 0,65 → 0,44 m. |
| C3 | ≈108–115 | ≈115–121 | Sehr feiner Restkamm am linken unteren Grat | sauber (nur im Ton aus 40 m) | [C3_kamm_spiel](bilder_8cd6d37/vn/C3_kamm_spiel.jpg) | – | In Farbe unauffällig, nur zur Beobachtung. |

### Sichtbare L3-Treffer (7 von 40)

| Nr | Kachel | x | z | Regel | Messwert | Nahbild | Urteil |
|---|---|---|---|---|---|---|---|
| T11 | D4 | 126,0 | 138,0 | G5 | zacke 0,79 m, hang 69° | [T11](bilder_8cd6d37/nah/T11_G5_D4.jpg) | sichtbar, leicht: Nahtlinie x = 126 läuft durchs Bild |
| T12 | D4 | 127,3 | 144,2 | G5 | zacke 0,87 m, hang 76° | [T12](bilder_8cd6d37/nah/T12_G5_D4.jpg) | sichtbar, leicht: Nahtlinie |
| T13 | D4 | 127,6 | 147,2 | G5 | zacke 0,92 m, hang 76° | [T13](bilder_8cd6d37/nah/T13_G5_D4.jpg) | sichtbar, leicht: Nahtlinie |
| T14 | C4 | 124,5 | 150,0 | G5 | zacke 0,51 m, hang 65° | [T14](bilder_8cd6d37/nah/T14_G5_C4.jpg) | sichtbar, leicht: Nahtlinie |
| T15 | C4 | 125,0 | 150,5 | G5 | zacke 0,88 m, hang 72° | [T15](bilder_8cd6d37/nah/T15_G5_C4.jpg) | sichtbar, leicht: Nahtlinie |
| T17 | D1 | 157,4 | 24,2 | G6 | zacke 0,24 m, hang 56° | [T17](bilder_8cd6d37/nah/T17_G6_D1.jpg) | sichtbar, stark: Rampentreppe, gehört zu Stelle 03 (in Arbeit) |
| T37 | D1 | 147 | 21 | G7b | zacke 0,20 m, hang 58° | [T37](bilder_8cd6d37/nah/T37_G7b_D1.jpg) | sichtbar, stark: Rampentreppe, gehört zu Stelle 03 (in Arbeit) |

## Die 23 P4b-Stellen vorher/nachher

Bild = `bilder_8cd6d37/vn/<Name>.jpg`, oben P4b (dc8c174), unten P4c (8cd6d37), gleiche Kamera.

| Nr | Kachel | P4b-Befund | P4b-Schwere | zacke vorher → nachher (m) | Bild | P4c-Urteil |
|---|---|---|---|---|---|---|
| 01 | C3 | Sägezahn-Ring am Krater | stark | 0,83 → 0,19 | [C3_kammQ1](bilder_8cd6d37/vn/C3_kammQ1.jpg) | **weg.** Die Mulde ist jetzt eine glatte Kuppe, die Form hat sich also geändert. |
| 02 | C3 | Sägezahn-Kamm auf dem Grat | stark | 0,81 → 0,21 | [C3_kamm_spiel](bilder_8cd6d37/vn/C3_kamm_spiel.jpg), [C3_kammQ4](bilder_8cd6d37/vn/C3_kammQ4.jpg) | **weg.** Nur im Ton bleibt ein feiner Restkamm. |
| 03 | D1 | Treppen- und Rippenrillen | stark | 0,70 → 0,43 / 1,79 → 1,75 | [D1_rampe_spiel](bilder_8cd6d37/vn/D1_rampe_spiel.jpg), [D1_zickzack](bilder_8cd6d37/vn/D1_zickzack.jpg) | **in Arbeit:** Hang glatter, Rillen an der Rampe bleiben. stark. |
| 04 | C3 | Kamm auf dem linken Grat | stark | 1,66 → 0,12 | [C3_finne](bilder_8cd6d37/vn/C3_finne.jpg) | **weg** |
| 05 | D4 | Zahnkante am Blockrand | stark | 1,70 → 0,33 | [D4_falte](bilder_8cd6d37/vn/D4_falte.jpg) | **weg** |
| 06 | C4 | Sägezähne am Simsgrat | leicht | 0,72 → 0,12 | [C4_g5](bilder_8cd6d37/vn/C4_g5.jpg) | **weg** |
| 07 | D6 | Trapez-Tafeln am Wandfuß | leicht | 1,32 / 1,54 → 0,42 / 0,48 | [D6_tafel_hoch](bilder_8cd6d37/vn/D6_tafel_hoch.jpg) | **weg**, nur eine schwache Linie bleibt |
| 08 | B4 | Zahnreihe an der Stufe | leicht | 0,89 → 0,33 | [B4_zahn](bilder_8cd6d37/vn/B4_zahn.jpg) | **weg** |
| 09 | C5 | Sägezahn-Kamm | leicht | 0,95 → 0,14 | [C5_zickzackO](bilder_8cd6d37/vn/C5_zickzackO.jpg) | **weg** |
| 10 | E7/F7 | Stufenlinie im Flussbett | leicht | 0,60 / 0,61 → unverändert | [E7_rinne_hoch](bilder_8cd6d37/vn/E7_rinne_hoch.jpg), [F7_rinne](bilder_8cd6d37/vn/F7_rinne.jpg) | **in Arbeit:** Mit Wasser ist es eine gerade helle Linie über dem Wasser, mit Platten und Treppenrand. stark. |
| 11 | C4/C5 | Gezackte Gratkante | leicht | 3,44 → 0,17 | [C4C5_zickzack](bilder_8cd6d37/vn/C4C5_zickzack.jpg) | **weg** |
| 12 | D6 | Sägezahnlinie am Hangrand | leicht | 0,65 → 0,19 | [D6_zickzackW](bilder_8cd6d37/vn/D6_zickzackW.jpg) | **weg** |
| 13 | G4 | Kissenblöcke mit Zickzack | leicht | 1,05 / 0,79 → 0,66 / 0,72 | [G4_g5a](bilder_8cd6d37/vn/G4_g5a.jpg), [G4_zickzack](bilder_8cd6d37/vn/G4_zickzack.jpg) | **weg.** Der Zickzack ist weg; die Blöcke bleiben, wirken aber weich. |
| 14 | E1 | Splitter bzw. Finne | leicht | 2,72 → 1,04 | [E1_krone_hoch](bilder_8cd6d37/vn/E1_krone_hoch.jpg) | **teilweise:** dünner, aber noch sichtbar. leicht. |
| 15 | C6 | Dunkler Trichter | leicht | 0,53 → 0,16 | [C6_knollen_hoch](bilder_8cd6d37/vn/C6_knollen_hoch.jpg) | **weg** |
| 16 | H6 | Kammzähne auf der Krone | leicht | 1,14 → 0,46 | [H6_g6](bilder_8cd6d37/vn/H6_g6.jpg) | **weg** |
| 17 | H3 | Knubbel am Terrassenrand | leicht | 0,48 → 0,28 | [H3_g6](bilder_8cd6d37/vn/H3_g6.jpg) | **weg**, der Weg ist jetzt zu sehen |
| 18 | H2 | Kammzähne und Randspitze | leicht | 0,79 → 0,82 | [H2_zickzack](bilder_8cd6d37/vn/H2_zickzack.jpg) | **weg.** Die Randspitze am Kartenrand bleibt, ist aber unauffällig. Der Messwert sitzt auf dieser Spitze. |
| 19 | G3 | Spitzen bzw. Knick am Rücken | leicht | 0,22 → 0,08 | [G3_huegel](bilder_8cd6d37/vn/G3_huegel.jpg) | **weg** |
| 20 | E2 | Zickzack am Ufer | leicht | 0,26 → unverändert | [E2_bach](bilder_8cd6d37/vn/E2_bach.jpg) | **in Arbeit:** Mit Wasser ein starker Sägezahn am Ufer. stark. |
| 21 | F6 | Kamm auf der Krone | leicht | – | [Kachel F6](bilder_8cd6d37/kacheln/F6.jpg) | **weg** (kein Kamm in der Übersicht). Der Wasserrand-Zickzack steht unter den Nebenbefunden. |
| 22 | F1 | Kamm auf der Krone | leicht | – | [Kachel F1](bilder_8cd6d37/kacheln/F1.jpg) | **in Arbeit:** In der Übersicht unauffällig, die Rinne ist mit Wasser gefüllt. Kein eigenes Nahbild. |
| 23 | G6 | Kerbe an der Krone | leicht | 0,65 → 0,44 | [G6_krone](bilder_8cd6d37/vn/G6_krone.jpg) | **in Arbeit / teilweise:** Kerbe weg, feine Randzähne bleiben. leicht. |

**Zählung:**
- **17 weg:** 01, 02, 04–09, 11–13, 15–19, 21.
- **F1 (22) unauffällig.** Zusammen mit den 17 sind also 18 nicht mehr sichtbar. Das deckt sich mit „18 weg“ in `ERGEBNIS_L3.md`.
- **Teilweise besser:** E1 (14) und G6 (23).
- **Weiter stark:** 03, 10 und 20.

Zum Wert bei H2: zacke 0,79 → 0,82 m. Der Messkreis erfasst die Randspitze, nicht den früheren Kamm.

## Nebenbefunde Wege und Wasser (getrennt vom Gelände)

| Nr | Kachel | x | z | Art | Schwere | Nahbild | Gate-Treffer | Notiz |
|---|---|---|---|---|---|---|---|---|
| W1 | G7 | ≈255–265 | ≈265–276 | Treppen- bzw. Leiterstrukturen und gerade helle Linien stoßen durchs Wasser; helle Insel | stark | [N06](bilder_8cd6d37/nah/N06_G7_leiter_im_wasser.jpg), [Kachel G7](bilder_8cd6d37/kacheln/G7.jpg) | – | Schon in der Übersicht klar. Gleiches Bild wie Stelle 10, aber weiter östlich. |
| W2 | E2/E3 (F2, F3) | 184/193, 187/196; 213; 211 | 87; 75; 80; 95 | Wege enden am Bach mit braunen L-Brettstummeln, aber es gibt keine Brücke über das Wasser | stark | [N01](bilder_8cd6d37/nah/N01_E3_bruecke_stummel.jpg), [N02](bilder_8cd6d37/nah/N02_E2_bretter.jpg), [Kachel E3](bilder_8cd6d37/kacheln/E3.jpg) | nur G6 in der Nähe | Ganze Brücken gibt es z. B. bei E3 (≈185\|128), D4 (≈150\|130) und E4 (≈180\|135). Unklar, ob die Stummel Absicht sind (Furt?). In den Übersichten C3/D3/D4 sieht man weitere Stummel am Bach um z ≈ 86–88, nicht vermessen. |
| W3 | C7 | ≈88–100 | ≈276–284 | Helle Platten mit Treppenrand mitten im Fluss | stark | [N08](bilder_8cd6d37/nah/N08_C7_platte_im_wasser.jpg), [Kachel C7](bilder_8cd6d37/kacheln/C7.jpg) | – | – |
| W4 | H7 | ≈315–335 | ≈268–280 | Helle Geländeblöcke im Wasser, treppiger Wasserrand, kleine Insel | stark | [N07](bilder_8cd6d37/nah/N07_H7_flecken_im_wasser.jpg), [Kachel H7](bilder_8cd6d37/kacheln/H7.jpg) | – | – |
| W5 | E3 | ≈186–193 | ≈88–128 | Sägezahn- bzw. Treppenrand am Bach (0,5-m-Raster) | stark | [N10](bilder_8cd6d37/nah/N10_E3_bachrand.jpg), [N01](bilder_8cd6d37/nah/N01_E3_bruecke_stummel.jpg) | G6 (187,8\|108,0) | Gleicher Bach wie Stelle 20 (E2), läuft aber durch E3 bis E4 weiter. |
| W6 | D7, E6, G6 | ≈160–168 / 205–210 / 262–290 | ≈262 / 250–258 / 245–256 | Gerade helle Linien und kleine Platten im Wasser | leicht | Kacheln [D7](bilder_8cd6d37/kacheln/D7.jpg), [E6](bilder_8cd6d37/kacheln/E6.jpg), [G6](bilder_8cd6d37/kacheln/G6.jpg), [N09](bilder_8cd6d37/nah/N09_G6_platten_im_wasser.jpg) | – | E6 und D7 schließen an Stelle 10 an. N09 zeigt in G6 vor allem einen Zackenrand; die Platten liegen außerhalb des Bildes. |
| W7 | A6/B6, A7, B7, C6 | ≈40–45, 35–42, 45–80, ≈125 | ≈245, 268, 262–268, 240 | Kleine helle Flecken bzw. Inseln im Fluss | leicht | Kacheln [A6](bilder_8cd6d37/kacheln/A6.jpg), [A7](bilder_8cd6d37/kacheln/A7.jpg), [B7](bilder_8cd6d37/kacheln/B7.jpg), [C6](bilder_8cd6d37/kacheln/C6.jpg) | – | Nur aus der Übersicht, kein Nahbild. |
| W8 | A1, B1, B2, A3, D2, E5, D5, F6 | – | – | Zickzack- bzw. Treppenrand an See- und Flussufern | leicht | [N11 E5](bilder_8cd6d37/nah/N11_E5_seerand_treppe.jpg), Kacheln | R6 (F1, G1), G8 (A2) | Am deutlichsten an schmalen Bächen, an großen Seen schwach. |
| W9 | alle mit Wegen (z. B. G3, G4, D2, F4) | – | – | Wegränder treppig im 0,5-m-Raster, im Ton deutlicher als in Farbe | leicht | [T40](bilder_8cd6d37/nah/T40_G7b_G4.jpg), [N03](bilder_8cd6d37/nah/N03_D2_bruecke_daneben.jpg) | – | Im Spielabstand kaum störend. |
| W10 | E1 | ≈183 / 196 | ≈40 | Zwei Wegstummel enden am Klippenfuß | unklar | [Kachel E1](bilder_8cd6d37/kacheln/E1.jpg) | R1_blind rampe_2 (175,1\|25,7) | Unklar, ob gewollt (Sackgasse). Kein Nahbild. |
| W11 | D2 | ≈162–167 | ≈58–62 | Braune Brücken- bzw. Brettteile neben dem Bach statt darüber (aus der Übersicht) | unklar | [N03](bilder_8cd6d37/nah/N03_D2_bruecke_daneben.jpg) | – | Das Nahbild bei (164\|60) zeigt nur den Weg, kein Brett. Die Lage aus der Übersicht ist nicht genau; vermutlich dasselbe Muster wie W2. |

## Urteil je Kachel (alle 56)

„Gelände“ = Höhen- und Formfehler. „Wasser/Wege“ = Nebenbefund.

| Kachel | Gelände | Wasser/Wege | Kachel | Gelände | Wasser/Wege |
|---|---|---|---|---|---|
| A1 | sauber | Seerand gezackt (W8) | E1 | leicht (Finne 14) | Wegstummel am Klippenfuß (W10); Bachrand treppig |
| B1 | sauber | Wasserrand gezackt (W8) | F1 | sauber (22 in Arbeit, unauffällig) | – |
| C1 | sauber | – | G1 | sauber | – |
| D1 | stark (03, in Arbeit) | – | H1 | sauber | – |
| A2 | sauber | Seen natürlich | E2 | stark (20, in Arbeit) | Brettstummel ohne Brücke (W2) |
| B2 | sauber | Flussrand gezackt (W8) | F2 | sauber | Brett am Bach (W2), Bachrand gezackt |
| C2 | sauber | – | G2 | sauber | – |
| D2 | sauber | Bachrand gezackt; Bretter unklar (W11) | H2 | sauber (Randspitze unauffällig) | – |
| A3 | sauber | Flussrand leicht gezackt | E3 | sauber | Brettstummel ohne Brücke (W2), Bachrand stark (W5) |
| B3 | sauber | Flussrand gezackt | F3 | sauber | Brett am Bach (W2) |
| C3 | sauber (Restkamm nur im Ton) | – | G3 | sauber | Wegränder treppig (W9) |
| D3 | sauber | Brücke ok | H3 | sauber | – |
| A4 | sauber | – | E4 | sauber | Brücke ok, Bachrand gezackt |
| B4 | sauber | – | F4 | sauber | – |
| C4 | leicht (Nahtlinie x = 126) | – | G4 | sauber | Wegränder treppig (W9) |
| D4 | leicht (Nahtlinie, Milchband rampe_5) | Brücke ok | H4 | sauber | – |
| A5 | sauber | – | E5 | sauber | Seerand treppig (W8) |
| B5 | sauber | – | F5 | sauber | – |
| C5 | sauber (Ausläufer Milchband) | – | G5 | sauber | – |
| D5 | leicht (Milchband rampe_5) | Seerand leicht gezackt | H5 | sauber | – |
| A6 | sauber | helle Flecken im Fluss (W7) | E6 | sauber | gerade Linie im Wasser (W6) |
| B6 | sauber (schwache Nahtlinie x = 84) | – | F6 | sauber (21 weg) | Wasserrand Sägezahn (W8) |
| C6 | sauber | helle Punkte im Wasser (W7) | G6 | leicht (23, in Arbeit) | Platten/Linien im Wasser (W6) |
| D6 | sauber | kleine Insel | H6 | sauber | helle Flecken am Wasser |
| A7 | sauber | Flecken im Fluss (W7) | E7 | stark (10, in Arbeit) | Linie/Platten im Wasser |
| B7 | sauber | Flecken im Fluss (W7) | F7 | stark (10, in Arbeit) | Linie/Platten/Treppen im Wasser |
| C7 | sauber | Platten im Fluss stark (W3) | G7 | sauber | Leiter/Treppen im Wasser stark (W1) |
| D7 | sauber | Linie/Flecken im Wasser (W6) | H7 | sauber | Blöcke im Wasser stark (W4) |

## Unklar

- **W2:** Sind die Brettstummel ohne Brücke Absicht (Furt bzw. Steg-Anfang)? Optisch wirken sie wie abgeschnittene Brücken.
- **W10:** Wegstummel in E1. Kein Nahbild.
- **W11:** D2-Bretter. Das Nahbild am vermuteten Punkt zeigt sie nicht.
- **Schatten:** Alle Bilder sind ohne Schatten. Mit Schatten ist auf Steilflächen Schattenakne zu erwarten; das ist nicht geprüft.
- **Messwerte für 21 F6 und 22 F1:** Es gibt keinen eigenen Messpunkt. Das Urteil stammt aus der Kachelübersicht.

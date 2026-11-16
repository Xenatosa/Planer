# P4d – sichtbare Restfehler (Stand 2771f70)

Methode wie P4c: Render ohne Schatten (`nosh=1`), Farbe + Ton (`clay=1`), plus Schatten-Stichprobe an 5 Nähten.
Vergleichsbilder `bilder_2771f70/vn/<name>.jpg`: oben vorher (P4c-Stand 8cd6d37), unten jetzt (2771f70), links Farbe, rechts Ton.
Neue Nahbilder (nur jetzt): `bilder_2771f70/nah/<name>.jpg`. Koordinaten x|z in m (x nach Osten, z nach Süden).

## Bleibt sichtbar

| # | Ort | Art | Schwere | Nahbild | Messung / Gate |
|---|---|---|---|---|---|
| S1 | E7 ≈193\|276 (~4 m), klein ≈202\|275 | helle, flache, scharfkantige Polygon-Platte im Flussbett | stark | nah/E7_platte_gross, vn/E7_rinne_hoch | – |
| S2 | F7 ≈218\|274 | dreieckige helle Platte im Fluss | stark | nah/F7_platte_219, vn/F7_rinne | – |
| S3 | F7 ≈237\|275 | Platte mit Treppenrand im Fluss | stark | nah/F7_platte_240, vn/F7_knollen_243_273 | zacke 0,18 (Punkt 243\|273) |
| S4 | H7 ≈303\|268 und ≈308\|268 | zwei eckige helle Blöcke im Fluss | stark | nah/H7_bloecke, vn/H7_knollen_310_272 | zacke 0,31 |
| S5 | H7 Südostbucht ≈333\|276 | weiche weiße Kuppe im Wasser, wirkt wie Schneefels | leicht (Grenzfall) | vn/H7_suedost_bucht, vn/H7_suedost_weit | zacke 0,35 |
| S6 | H7 Kartenrand x=336, z≈280–286 | Wasserfläche endet mit V-Kerbe/ragt über den Rand | leicht | nah/H7_rand_336 | – |
| S7 | D4/D5 rampe_5 ≈133\|155 bis ≈135\|185 | milchiges Band/Fleck, unverändert seit P4c | leicht | vn/N04_D4_milchstreifen, vn/N05_D5_milchfleck | zacke 0,10 / 0,0 (Farbe, keine Geometrie) |
| S8 | A7, B7, C7 ≈124\|268, D7 ≈135\|269, G7 ≈280–283\|266 (korrigiert in P4e, vorher fälschlich ≈255\|282) | kleine helle Plättchen im Fluss (gleiche Art wie S1–S4, kleiner) | leicht | nah/C7_flecken, kacheln/A7…G7 | – |
| S9 | G6 rampe_4-Unterrand ≈268\|242 | rechts leichte Restzacken, nur im Ton | leicht (Farbe unauffällig) | vn/rampe4_unterrand_268 | zacke 0,47, hang 46,3° |
| S10 | E2/E3-Brücken, Ostufer | Ufer weicher, Ostseite noch leicht treppig | leicht | vn/N01_E3_bruecke_stummel, vn/N02_E2_bretter | zacke 0,06–0,25 |

S1–S4 und S8 sind dieselbe Fehlerart: Geländezellen im Flussbett ragen als flache, eckige Platten über die Wasserfläche. Die alten P4c-Befunde dieser Art an anderen Stellen (G7-Leiter, C7-Platten 97|275, gerade Linie F7) sind weg.

## Behoben (vorher → jetzt)

- X084/rampe_8: Kreuzung 152|29,5, Kehre 151|33, Steilstück 154,6|36, Blick von Nord – Treppenzähne und Kerbe weg; im Ton kleine helle Kuppe an der Kehre (vn/X084_*).
- D1_zickzack glatt; D1_rampe_spiel deutlich besser, feine helle Streifen nur im Ton.
- T37 (D1 147|21): Sägezahn weg (vn/T37_G7b_D1) → Ausnahmekandidat.
- G6-Restkerbe 283|226 weg (vn/G6_krone).
- rampe_4-Unterrand 282 und 256 glatt (256 mit dünner Böschungskante wie vorher).
- Nähte C4|D4 x=126 (z133/145/157, Süd), x=84 (B6|C6, B4|C4), D1|D2 z=43: keine Nahtlinie (P12). Die dünne gelbe Linie ist der Kachelrahmen-Overlay.
- Schatten-Stichprobe (schatten/*.jpg, 5 Punkte): keine Nahtlinie, keine sichtbare Schattenakne.
- E2/E3-Brücken durchgehend (vn/E2_bruecke_*).
- G7-Leiter/Treppen im Wasser 260|270 weg (vn/N06_G7_leiter_im_wasser, vn/G7_bett).
- C7-Platten 97|275 weg (vn/N08_C7_platte_im_wasser).
- G7_bett_272_265 glatt, F7-Rinne: gerade Linie weg.

## Nur vermerkt, nicht bewertet

- E3-Westufer ≈186|110: leicht gezackte Uferkante (vn/notiz_E3_westufer) – läuft als L3d bei Art Umgebung.
- G7-Nordufer westlich x≈265 (≈258|262): diagonale Kante (vn/notiz_G7_nordufer_west) – L3d.
- D2 geschützt, Bretter bleiben.
- E1: zwei Wegstummel enden am Wandfuß ≈183|40 / ≈196|40 (nah/E1_wegstummel) – Gestaltung, keine Geometrie.

## Koordinaten-Gegenprüfung

- Die P4c-Brückenstummel „bei z 87“ liegen tatsächlich bei z≈84; im Nahbild `E2_bruecke_184_87`/`193_87` steht die Brücke am oberen Bildrand, nicht im Zentrum. Brückenzellen laut `relief_daten.json.gz` (bruecken): E2 z 74,5–75,5 (x 186,5–197,5), E3 z≈127.
- Platten: Zentrum E7 193|276 und F7 218|274 bestätigt (Fehler im Fadenkreuz). F7-Platte liegt ≈3 m westlich des P4c-Punkts 240|276 (→ ≈237|275). H7-Blöcke liegen ≈3 m nördlich des Punkts 307|271 (→ z≈268).
- Die Flecken in den Übersichten von A6/C6/E6/F6/G6 liegen außerhalb des Kachelrahmens (Fluss Reihe 7); Gegenprobe an der Kachelstelle ohne Befund.

## Korrektur (P4e)

„G7 ≈255|282“ in S8 war ein Schätzfehler aus der Übersicht ohne Nahbild. Das Plättchen lag westlich außerhalb des G7-Rahmens (vermutlich F7-Platte ≈237|275). Die echte G7-Stelle sind zwei kleine Kiesel im Fluss bei ≈280–283|266. Nahbild: `../qa_p4e/bilder_bfe8dce/vn/G7_NO_kiesel_281_266.jpg` (oben 2771f70, unten bfe8dce: weg).

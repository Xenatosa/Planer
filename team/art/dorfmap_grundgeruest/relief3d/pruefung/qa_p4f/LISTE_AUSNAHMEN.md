# P4f – konsolidierte Ausnahmeliste: Gate-/Ton-Auffälligkeiten, mit bloßem Auge unsichtbar (Stand a6b00ba)

Prüfer und Schwellen unverändert. Messung: `messung.py` (zacke_m = max. Abweichung vom 5×5-Mittel im Radius 3 m; hang_max in Grad) → `messung_p4f.json`. Gate-Treffer aus `pruefung/regeln_letzter_lauf.json` dieses Laufs (Radius 4 m). Vergleich vorher/jetzt in `bilder_a6b00ba/vn/` (oben bfe8dce, unten a6b00ba).

**16 Einträge: 14 aus P4e (13 weiter unsichtbar, A1 weiter unsichtbar mit geändertem Bild), 2 neu (A15, A16). Keiner entfällt, keiner ist sichtbar geworden.**

| # | Ort | Gate-Treffer | zacke / hang | Nahbild | Status P4f | Begründung |
|---|---|---|---|---|---|---|
| A1 | G6-Facette E3 189,5\|119,5 | G6_facette 7 | 0,14 / 32,6° | vn/G6fac_E3_189_119, vn/G6fac_E3_weit | weiter unsichtbar (Bild geändert durch L3h) | Fadenkreuz liegt jetzt am Rand des verbreiterten Bachs; weiche Böschung, keine Facette |
| A2 | rampe_4-Unterrand 268\|242 | keiner ≤4 m | 0,47 / 46,3° | vn/rampe4_unterrand_268 | weiter unsichtbar, bildgleich P4e | Restwelle nur im Ton |
| A3 | E3-Brücke West 175\|128 | G6_facette 178,7\|127,0: 10 | 0,25 / 46,5° | vn/E3_bruecke_west | weiter unsichtbar | feine Uferstufe nur im Ton; Farbe unauffällig |
| A4 | T37 D1 147\|21 | G7b_feld 0,427; G6 145,6\|19,2: 20 | 0,37 / 57,9° | vn/T37_G7b_D1 | weiter unsichtbar, bildgleich | glatt |
| A5 | P2 C5 107,8\|183,8 | G2_spitze_oben_fein 0,59 | 0,25 / 60,8° | vn/P2_G2fein_C5 | weiter unsichtbar, bildgleich | keine Spitze |
| A6 | P2 D3 147\|107 | G7b_feld 0,256 | 0,0 / 0,0° | vn/P2_G7b_D3 | weiter unsichtbar, bildgleich | ebene Fläche |
| A7 | X084-Kreuzung ≈152\|29,5 | R3_quer 76,1; R3_laengs 0,693; R3_woelb 0,309 | 0,64 / 65,8° | vn/X084_kreuzung | weiter unsichtbar, bildgleich | glatt |
| A8 | X084-Kehre ≈151\|33 | R3_quer 36,1 | 0,89 / 66,1° | vn/X084_kehre | weiter unsichtbar, bildgleich | kleine Kuppe nur im Ton |
| A9 | X084-Steilstück ≈154,6\|36 | R3_laengs 0,197; R1_blind | 0,46 / 51,3° | vn/X084_steilstueck, vn/X084_steil_von_nord | weiter unsichtbar, bildgleich | glatt |
| A10 | Naht C4\|D4 x=126 | G5 1,65 / 1,32; G2_fein 0,63; G6 17 | 0,66 / 0,95 / 0,32 | vn/C4D4_rand_z133/z145/z157, schatten/C4D4_rand_* | weiter unsichtbar | keine Nahtlinie, auch mit Schatten |
| A11 | G6-Krone 283\|226 | G6 10 | 0,19 / 56,6° | vn/G6_krone | weiter unsichtbar, bildgleich | glatt |
| A12 | G7 260\|270 | (P4e: G6 18) | – | vn/N06_G7_leiter_im_wasser | weiter unsichtbar, bildgleich | Leiter weg |
| A13 | rampe_4 256 / 282 | R3_laengs 0,12 | 0,11 / 31,3° bzw. 0,39 / 73,4° | vn/rampe4_unterrand_256, vn/rampe4_unterrand_282 | weiter unsichtbar, bildgleich | glatt |
| A14 | Nähte x=84, z=43 | – | 0,05–0,10 | vn/naht_B4C4_x84, vn/naht_D1D2_z43_a/b, schatten/naht_* | weiter unsichtbar, bildgleich | keine Linie, Schatten durchgehend |
| A15 | **neu:** Mulde C2 ≈93,5\|77 | keiner ≤4 m | 0,46 / 59,9° | vn/C2_delle_935_775, vn/C2_delle_weit | unsichtbar (seit bfe8dce gleich) | im Ton dunkle kleine Delle; in Farbe nur weiche, natürlich wirkende Schneemulde |
| A16 | **neu:** G1 273,4\|21,2 | R1_blind 0; R3_laengs_m 0,095 | 0,22 / 34,3° | vn/G1_delle_273_21, vn/G1_delle_weit | unsichtbar | am Fadenkreuz glatter Hang. (Der sichtbare Krater 10 m nördlich steht als S2 in LISTE_SICHTBAR) |

„bildgleich“ = mittlere Pixelabweichung vorher/jetzt 0,00 und kein Pixel > 25.

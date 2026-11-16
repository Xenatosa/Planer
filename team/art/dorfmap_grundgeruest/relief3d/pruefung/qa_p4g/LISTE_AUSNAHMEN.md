# P4g – Ausnahmeliste: Gate-/Ton-Auffälligkeiten, mit bloßem Auge unsichtbar (Stand 0a0b83a)

Prüfer und Schwellen unverändert. Messung `messung.py` → `messung_p4g.json` (zacke_m = max. Abweichung vom 5×5-Mittel im Radius 3 m, hang_max in Grad). Gate-Treffer aus `regeln_letzter_lauf.json` des P4g-Laufs. Gate-Differenz P4f→P4g: nur 4 Treffer entfallen (R6_wasser_schnee 272,5\|9,8 / 273,1\|7,3 / 275,0\|6,1, G6_facette 271,7\|11,1 – alle G1-Krater), keine neuen.

**17 Einträge = 16 aus P4f (alle weiter gültig und unsichtbar) + 1 neu (A17). Geändert: A12 (Messwert nachgetragen), A1 (neu angesehen, weil E3 geändert).**

| # | Ort | Gate-Treffer | zacke / hang | Nahbild | Status P4g |
|---|---|---|---|---|---|
| A1 | G6-Facette E3 189,5\|119,5 | G6_facette 7 | 0,14 / 32,6° | vn/A1_G6fac_E3_189_119 | weiter unsichtbar; neu gerendert, weil E3 geändert: am Fadenkreuz unverändert (Änderung nur am oberen Bildrand = Kanal), Perlen oben jetzt weg |
| A2 | rampe_4-Unterrand 268\|242 | keiner | 0,47 / 46,3° | qa_p4f vn/rampe4_unterrand_268 | übernommen (G6 bildgleich) |
| A3 | E3-Brücke West 175\|128 | G6_facette 178,7\|127,0: 10 | 0,25 / 46,5° | qa_p4f vn/E3_bruecke_west | übernommen; neu gerendert: bildgleich (Δ 0,004, kein Pixel > 25) |
| A4 | T37 D1 147\|21 | G7b_feld 0,427; G6 145,6\|19,2: 20 | 0,37 / 57,9° | qa_p4f vn/T37_G7b_D1 | übernommen (D1 bildgleich) |
| A5 | P2 C5 107,8\|183,8 | G2_spitze_oben_fein 0,59 | 0,25 / 60,8° | qa_p4f vn/P2_G2fein_C5 | übernommen (C5 nur Rauschen) |
| A6 | P2 D3 147\|107 | G7b_feld 0,256 | 0,0 / 0,0° | qa_p4f vn/P2_G7b_D3 | übernommen (D3-Änderung nur E3-Kanal im Hintergrund) |
| A7 | X084-Kreuzung ≈152\|29,5 | R3_quer 76,1; R3_laengs 0,693; R3_woelb 0,309 | 0,64 / 65,8° | qa_p4f vn/X084_kreuzung | übernommen (D1 bildgleich) |
| A8 | X084-Kehre ≈151\|33 | R3_quer 36,1 | 0,89 / 66,1° | qa_p4f vn/X084_kehre | übernommen |
| A9 | X084-Steilstück ≈154,6\|36 | R3_laengs 0,197; R1_blind | 0,46 / 51,3° | qa_p4f vn/X084_steilstueck | übernommen |
| A10 | Naht C4\|D4 x=126 | G5 1,65 / 1,32; G2_fein 0,63; G6 17 | 0,66 / 0,95 / 0,32 | qa_p4f vn/C4D4_rand_* | übernommen (C4/D4-Änderung nur Bach im Hintergrund) |
| A11 | G6-Krone 283\|226 | G6 10 | 0,19 / 56,6° | qa_p4f vn/G6_krone | übernommen (G6 bildgleich) |
| A12 | G7 260\|270 | **kein Treffer ≤12 m** – weder in P4f noch P4g. Der alte Wert „G6 18“ stammt aus P4d (Treffer 264\|268,8) und wird seit P4e nicht mehr gemeldet. | **neu: 0,23 / 47,2° (260\|270); 0,19 / 43,9° (264\|268,8)** | vn/A12_G7_260_270 | weiter unsichtbar: glatte Uferböschung, vorher/jetzt bildgleich (Δ 0,00 in Farbe und Ton, also ΔL = 0). Hang > 45° = Böschung zum Wasser, keine Zacke (zacke 0,23 m). Ein Gate-Wert ist nicht bestimmbar, weil das Gate dort nichts mehr meldet. |
| A13 | rampe_4 256 / 282 | R3_laengs 0,12 | 0,11 / 31,3° bzw. 0,39 / 73,4° | qa_p4f vn/rampe4_unterrand_* | übernommen |
| A14 | Nähte x=84, z=43 | – | 0,05–0,10 | qa_p4f vn/naht_* | übernommen (B4/C4/D1/D2 ohne echte Änderung) |
| A15 | Mulde C2 ≈93,5\|77 | keiner | 0,46 / 59,9° | qa_p4f vn/C2_delle_935_775 | übernommen (C2 bildgleich) |
| A16 | G1 273,4\|21,2 | R1_blind 0; R3_laengs_m 0,095 (unverändert) | 0,22 / 34,3° | vn/G1_gate_273_21 | **gilt weiter**: Treffer unverändert, am Fadenkreuz glatter Hang; Bildänderung (Δ 0,36) nur durch den Krater im Hintergrund, der jetzt Schnee ist |
| A17 | **neu:** G1 Clay-Ring ≈272,5\|9 | keiner (die 4 Krater-Treffer sind entfallen) | 0,04 / 9,4° | vn/G1_krater_12 (Ring über dem Fadenkreuz), vn/G1_ring_272_9, vn/G1_krater_22 | nur im Ton als schwacher Bogen sichtbar (auch in den 30-m-Quadranten Q1/Q2 im Ton); in Farbe aus 8, 12, 22 und 60 m unsichtbar. Hinweis: G1 ist Prototyp-Kachel mit lokalem Profil, die GB-Messung ist dort nur Näherung. |

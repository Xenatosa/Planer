# P2 Wegnetz v2 – Ergebnis (Basis art/dorfmap-fertig @d181fa6 = 2cdd6d9 + P10b/P10c, Reliefdaten gleich)

Branch `wege/dorfmap-p2-v3`. v2 lag auf 7944b33, dann kam P10c dazu (Konflikt index.html/neu). Deshalb gibt es einen neuen Branch statt eines Force-Push. Cherry-Picks: a0c8697, 93398fc, bee3f99 (Analyse), danach v2-Commit.
Ersetzt PR #9 (wege/dorfmap-p2-gen, Basis dc8c174).

## Was v2 anders macht [S]
1. **Rampen gezielt entnommen** (`P2_BEHALTEN`, Standard `0,1,2,3,4,7,10,11` = Originalnummern in der Erzeugungsreihenfolge von `_rampen`). Jede Rampe wurde einzeln entnommen und das Gate dazu gemessen (12 Läufe). Entnommen werden nur Rampen, die keine Familie verschlechtern:
   - Rampennamen unten = Gate-Nummern des Vorher-Stands (im Nachher-Gate sind die verbleibenden Rampen neu durchnummeriert, rampe_0…8).
   - **raus:** Original 5 (Gate rampe_5, C6/C7), 6 (rampe_6, C5), 8 (rampe_8, C4), X069 (rampe_12, D4/C3, „Pfeil“-Wegenden), Original 9 wie bisher über O16
   - **bleiben (Ausnahme R1/R8a):** rampe_0 (B1–C2), rampe_1 (G1–F1), rampe_2 (D1–E1), rampe_3 (E6–C6), rampe_4 (H6–F6), rampe_7 (C5–D4), rampe_9 (H4–G3), rampe_10 (H5), X084/rampe_11 (D1)
   - Gründe aus den Einzelläufen (Delta gegen „alle Rampen da“): ohne rampe_7 R5 +10 (**das war die Rinne um das Plateau in C4**, 1,5→147,5 m²), ohne 0/1/3 G3f +1/+2/+5, ohne 1/2/3/4/10 G7b +1…+2, ohne 2 G2f +2.
2. **Ursache des G6/G3f-Rauschens weit weg von den Rampen behoben:** Die Feinband-Zufallsauswahl (Kuppen rng 212, Tropfen-Erosion rng 78, Überhänge rng 611) mischt per `argwhere`-Index. Jede lokale Änderung verschob deshalb die Auswahl auf der ganzen Karte (174 000 Feinpunkte geändert). Die Kandidatenmasken werden jetzt aus dem Stand mit Rampen eingefroren: `p2_fw_masken.npz`, analog zu `erosion_start_t63u.npy`. Ergebnis bei Entnahme aller Rampen: G6 239 → 226.
3. G11-Block (Objekte auf die sichtbare Fläche) wie in v1. Der Absturzschutz in pruefe_regeln.py ist toter Code, die Nullprobe ist unverändert (476).
4. Spitzen-Glättung im Rampensaum (`P2_SPITZEN`, Standard aus): 2 Versuche gescheitert (1.: G2f 9→13, 2.: 0 Punkte) → abgebrochen, G2f C5 als Ausnahme.

## Erzeugung
```
python3 gen_relief.py
RELIEF_NEU=1 RELIEF_GELAENDE_VAR=0 python3 gen_relief.py
python3 gen_textur.py vc                                   # P3: T1/FW.c
python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py  # index.html Nutzlast
python3 pruefung/p10c/waende_einsetzen.py                 # P10c-Waende in relief_neu/index.html
Gate: loch_o18g.js (eigene Datei /tmp/p2v2_gate_loch.json), pruefe_regeln.py, r8_kreuzung.py, r9_form.py
RELIEF_GELAENDE_VAR=0 sh pruefung/alle_kacheln/alles.sh /tmp/p2v2_p10_{vorher,nachher}
```
`RELIEF_GELAENDE_VAR=0`: Kreuzungsvariante 24 braucht die alten Gate-Nummern rampe_2/rampe_11. Auf der Basis bricht die Standard-Variante ohnehin ab, weil die p3d17-Quelle nicht passt (siehe ERGEBNIS_P3). Vorher und nachher wurden deshalb gleich gebaut.

## Gate vorher (d181fa6, laut P10c gleich 2cdd6d9) → nachher
regeln 476 → 397, r8 48 → 33, r9 334 → 325, Trefferkarte 858 → 755, lochscan offen_innen 0 → 0, T1 0 → 0, G11 0 → 0.

| Familie | vorher 2cdd6d9 | nachher | |
|---|---:|---:|---|
| G2_spitze_oben | 3 | 3 | gleich |
| G2_spitze_oben_fein | 8 | 9 | schlechter |
| G3_spitze_unten | 3 | 3 | gleich |
| G3_spitze_unten_fein | 2 | 2 | gleich |
| G5_beule_klippe | 68 | 63 | besser |
| G6_facette | 220 | 205 | besser |
| G7_wand_glatte_flaeche | 1 | 1 | gleich |
| G7b_wandkontur_feld | 24 | 25 | schlechter |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | gleich |
| G7b_wandkontur_rauheit | 1 | 1 | gleich |
| G8_fluss_nicht_bis_rand | 1 | 1 | gleich |
| R1_blind | 24 | 17 | besser |
| R2_getrennt | 15 | 9 | besser |
| R3_laengs_m | 35 | 20 | besser |
| R3_quer_pct | 23 | 11 | besser |
| R3_woelb_m | 22 | 10 | besser |
| R5_loch | 17 | 8 | besser |
| R6_wasser_schnee | 4 | 4 | gleich |
| R8_gitter | 10 | 7 | besser |
| R8_quer | 5 | 3 | besser |
| R8_stufe | 9 | 6 | besser |
| R8a_wegende | 24 | 17 | besser |
| R8b_delle | 25 | 22 | besser |
| R9_saegezahn | 34 | 34 | gleich |
| R9w_wellen | 275 | 269 | besser |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | gleich |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | gleich |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | gleich |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | gleich |
| T1_fleckrand | 0 | 0 | gleich |
| G11 | 0 | 0 | gleich |


## D2 bitgleich [S]
GB 749d3c4b…, VC 8d7a7b82… (P3-Stand), WV 4b33ed17…, WEGA e6cf61d2… – vorher = nachher. alle_kacheln D2-Vertex-Hash identisch.
## Kante D1|D2 [S]
z 40–46, x 120–174: keine G2/G3/G6-Treffer vorher und nachher.

## Ausnahmen (Messwert + Nahbild)
| Familie | Stelle | Messwert | Grund | Bild |
|---|---|---|---|---|
| G2_spitze_oben_fein 8→9 | C5 107.8\|183.8 und 107.2\|184.8 (vorher C5 109.8\|179.8, B4 verschoben) | 0,61 / 0,59 m (Schwelle 0,45) | Wand statt früherer rampe_6. Zwei Glättungsversuche gescheitert. Die Entnahme bringt G5 −18 und R5 −3. | ausnahme_G2f_C5.jpg |
| G7b_wandkontur_feld 24→25 | D3 | 0,256 (Schwelle 0,85) | Messartefakt: Die O17-Referenz enthält die Serpentine X069 als steile Fläche. Ohne X069 ist D3 dort Hang ohne Wandkontur. Ein sichtbarer Fehler ist das nicht [A] | ausnahme_G7b_D3.jpg |
| R1/R8a | 9 verbleibende Rampen (17 Enden) | – | siehe oben, Entnahme würde eine Familie verschlechtern | – |
| R2 | G2 270.9\|62.2 (1588) u. a., 9 gesamt | – | wie freigegeben, QA P4 | – |
| R6 | 4 | – | liegt beim Dorfmap-Bot | – |

## Nahbilder
Betroffene Kacheln: `nahbilder_vorher/`, `nahbilder_nachher/` (alle_kacheln, beide mit RELIEF_GELAENDE_VAR=0). C4: `c4_vorher_nachher.jpg` (Rinne weg, rampe_7 bleibt), D4: `d4_vorher_nachher.jpg` (Pfeil-Wegenden der X069 weg, keine neue Rinne sichtbar). alle_kacheln-Lochscan 56 Kacheln: vorher 0, nachher 0. Werkzeug P10c, beide Läufe. Vorher-Lauf: Der Hashvergleich D1/G1 gegen index.html der Basis schlägt fehl, weil die Basis-index.html mit Variante 24 gebaut ist. Nahbilder und Lochscan wurden dort deshalb einzeln nachgezogen. Nachher: Hashvergleich alle identisch, Wände identisch. Trefferkarte: `trefferkarte/vergleich.html|png`.

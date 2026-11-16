# P2c – Entscheidungen Dorfmap-Grundgerüst zu P2b (16.11.2026, Wege & Deko)

Basis: `wege/dorfmap-p2b-v2` @ 2633f1d (PR #21), art/dorfmap-fertig unverändert d5b17e2 (ls-remote 13:2x MEZ).
Kein Merge, kein Force-Push, Prüfer/Schwellen unverändert, eingefrorene Feinband-Masken (FW.vid), VC nur lokal (p2b_vc_lokal.py).

## Umsetzung (relief_p2b.py, Stellen in p2b/p2b_stellen.json)
- **03d D1 Variante A (neu, `rampe_anheben`)**: X084 = rampe_8 an der Kreuzung mit rampe_2 angehoben (Δ ≈ 1,94 m, Kreuzung s = 34,9).
  - Kreuzungsfläche = rampe_2-Oberfläche (quadratischer Fit über den ungestörten rampe_2-Kern ±8 Zellen, Rest ≤ 0,12 m); die alte X084-Rinne im rampe_2-Band ist geschlossen, rampe_2 selbst bleibt in Lage/Gefälle.
  - X084 bergseitig: weiches Maximum aus altem Profil und Eintrittshöhe (5,47 m); im rampe_2-Band (s 32,3–37,0) folgt X084 der rampe_2-Oberfläche (5,47 → 6,12 m, weil rampe_2 dort quer zu X084 fällt); talseitig Gefälle zurück auf die alte Endhöhe 0,58 m (Exponent 1,5, zum Ende flacher).
  - Kehren stetig (Profil je Vertex über alle Segmente gemischt), Böschung wegnah harmonisch (keine Mulden), zum Rand Bestand + harmonischer Versatz.
- **03m D1 Mulde (neu, `glaetten`)**: geschlossene Senke 0,87 m bei 163–164,5|20–21 (im QA-Nahbild 159|22,9 die U-Mulde rechts), Schließen 3,5 + Gauß 0,75. Senke danach 0,03 m. Keine Ausnahme.
- 03/14/23 unverändert aus P2b; rampe_5, E2-Westufer, W10 E1 nicht angefasst.

## Gate je Regel (vorher 2633f1d → nachher)
| Prüfer | vorher | nachher | Änderung |
|---|---|---|---|
| pruefe_regeln gesamt | 373 | 371 | −2 |
| R3_laengs_m | 20 | 21 | +1 |
| R3_quer_pct | 10 | 8 | −2 |
| R3_woelb_m | 10 | 8 | −2 |
| G6_facette | 214 | 215 | +1 |
| G7b (inkl. T37) | 29 | 29 | 0 |
| r8_kreuzung | 33 | 31 | −2 (R8_gitter rampe_2×8 152,5|28,5 weg, R8a rampe_8-Ende weg) |
| r9_form | 325 | 325 | 0 |
| W1 index / 56 Kacheln | 0/0 | 0/0 | 0 |
| Lochscan index / 56 Kacheln | 0/0 | 0/0 | 0 |
| D2 GB/VC/WV/WEGA + D2-Mesh | – | bitgleich | 749d3c4b…/8d7a7b82…/4b33ed17…/e6cf61d2… |

Weg: rampe_2 R3 146,4|29,2 (quer 69 %, wölb 1,28), 150,3|28,7 (quer 90 %, längs 0,25, wölb 1,69), 154,3|28,2; rampe_8 wölb 153,7|26,1 (1,65); G6 159,0|22,9, 146,1|17,5, 145,2|20,0, 165,6|15,7.
Weiter vorhanden, aber deutlich kleiner: rampe_8 Kreuzungsabschnitt 151,8|29,6 quer 100,6 → 76 %, wölb 1,55 → 0,31; 153,7|26,1 längs 1,38 → 0,26.
Neu: siehe Ausnahmen. alles.sh: /tmp/p2c_p10_nachher (Hash D1/G1/D2 identisch, Naht 0, Lochscan 0), Berichte in `kacheln/`. Trefferkarte `--vorher /tmp/p2c_vorher` in `trefferkarte/`.

## Ausnahmen (R3-Anstieg nur unsichtbar; Messwert + Nahbild)
| Treffer | Messwert | Ursache | Nahbild |
|---|---|---|---|
| R3 rampe_8 155,6|22,6 (Abschnitt s 28–32) | quer 16,9 %, längs 0,178, wölb 0,211 | Querschnitt läuft in die schräg gekreuzte rampe_2 (Gefälle ~0,24/Zelle) | NEU_G6_D1_157_23, 03_D1_zickzack: keine Kante sichtbar |
| R3 längs rampe_8 150,4|33,1 (Kehre) | 0,145 | Gefälle talseitig steiler (Anhebung), Kehre | R3_D1_rampe8_kehre_talseite: glatt |
| R3 wölb rampe_8 153,7|35,4 | 0,087 (Schwelle 0,08) | talseitiger Auslauf | R3_D1_rampe8_kehre_talseite |
| G6 157,0|15,7 (11), 145,6|19,2 (20, Umgruppierung von 146,1|17,5 + 145,2|20,0), 157,4|22,7 (16), 152,3|24,3 (15), 165,6|15,6 (6, war 7) | Facettenzahl | Böschung der Anhebung | NEU_G6_* : keine Rippen/Mulden sichtbar |

## Nicht erledigt / ehrlich
- **T37 (G7b_wandkontur_feld D1, 147|21)**: 0,515 → 0,458, weiter Treffer (Schwelle 0,85). G7b misst die Wandrauheit im ganzen Feld D1 gegen O17; das Schließen der alten Rinne und das Glätten senken sie zwangsläufig. Ohne neue Rauheit (= Dellen, verboten) nicht lösbar → Entscheidung Grundgerüst/QA nötig (Ausnahme oder Regel-Lesart).
- R3 rampe_8 im Kreuzungsabschnitt bleibt (quer 76 %), da rampe_2 dort quer zu X084 fällt; Kreuzungsfläche ist stufenfrei, aber nicht eben. Eben ginge nur mit Umbau von rampe_2.

## Risiken
- X084 talseitig steiler: von 6,12 m (s 37) auf 0,58 m (s 47,6), anfangs ~0,75 m/Zelle, zum Ende flacher.
- Kuppe auf X084 am Kreuzungsausgang (s ≈ 37) durch die rampe_2-Neigung.
- 03m hebt die Senke bis 2,18 m an (Wandfuß-Bucht), sichtbar glatt, Wand oberhalb unverändert.
- bau_endstand.sh: Nachschritte L3/P2b/P2c nur als Kommentar eingetragen (L3 fehlt im Skript, deshalb kein ausführbarer Schritt; der Endbau-Vergleich gilt weiter für P11).

## Nahbilder (vorher 2633f1d / nachher P2c; Farbe | Ton)
`nahbilder/`: 03_D1_zickzack (Zickzack-Wand weg), T37_G7b_D1, Mulde_D1_159_23 (Mulde weg), NEU_G6_D1_157_16, NEU_G6_D1_146_19, NEU_G6_D1_157_23, NEU_G6_D1_152_24, NEU_G6_D1_166_16, R3_D1_rampe8_kehre_talseite.

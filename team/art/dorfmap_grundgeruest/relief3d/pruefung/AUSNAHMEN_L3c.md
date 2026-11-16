# AUSNAHMEN L3c (Branch art/dorfmap-L3c, Basis d5b17e2 = L3b-Kopf)

## Stellen, die Ausnahme bleiben

| Stelle | Feld | Befund | Versuche | Grund | Nahbild |
|---|---|---|---|---|---|
| W5 Bachrand | E3 (≈186–193\|88–128) | Sägezahn-/Treppenrand am Bach | 1: `L3c_E3` (Uferglättung + Landufer +0,08 m), im Nahbild unverändert. 2 (nach Maßstab-Fix): Wasserrand-Ansatz mit Landufer +0,12 m und WV-Randband −0,15 m. Der Bach verschwindet dabei teilweise → schlechter, verworfen | **Renderer-Rasterkante des Wassermeshes**: `viewer_alle.js` (Wassermesh aus WV) setzt Nicht-Wasser-Vertices auf `min(mittleres WR, GL+0,02)`, dadurch folgt die Kante dem 0,5er Raster. Über die Daten nicht glättbar. **Korrektur:** Die frühere Begründung „Bach liegt 0–5 m an/unter Gasse G013“ beruhte auf dem Maßstab-Fehler (Meter als Zellen). G013 liegt tatsächlich bei x 152–173 Zellen und ist nicht betroffen. Vorschlag Dev UI: Wasserrand im Viewer per Randinterpolation/Alpha weich zeichnen statt Höhen-Clamp | [E3](l3c_nahbilder/paare/E3_vorher_nachher.jpg), [Versuch](l3c_nahbilder/versuch_wasserrand_e1/E3_versuch_verworfen.jpg) |
| 20 Westufer | E2 (≈198–204\|50–66) | treppiger Wasserrand am Westufer | L3b: 2 Versuche (Ufer heben). L3c: Wasserrand-Ansatz wie bei E3 → Treppe bleibt unverändert, verworfen | Gleiche Ursache wie E3 (Renderer-Rasterkante). **Korrektur:** Die L3b-Begründung „Böschung Gasse G013/K009“ war maßstabsbedingt falsch; der kleinste Abstand von Stelle 20 zum Weg beträgt richtig 7,0 Zellen. → Dev UI | [E2](l3c_nahbilder/paare/E2_vorher_nachher.jpg), [Versuch](l3c_nahbilder/versuch_wasserrand_e1/E2_versuch_verworfen.jpg) |
| H7 Rest | H7 Bucht Südost (≈330–338\|274–284) | treppiger Wasserrand der Bucht | 1: `L3c_H7` (Blöcke am Klippenfuß weg). 2: `L3c_H7b` (Landufer +0,12 m) → im Nahbild kein Unterschied, verworfen | Gleiche Renderer-Rasterkante der Wassermaske; die Außenkontur darf nicht geändert werden | [H7](l3c_nahbilder/paare/H7_vorher_nachher.jpg) |
| H7 Ring | H7 (≈313\|268) | kleiner heller Ring im QA-Blick N07 | – | Kein Wasser- oder Inselproblem in den Daten; vorher = nachher, nicht angefasst | [H7](l3c_nahbilder/paare/H7_vorher_nachher.jpg) |

Nicht angefasst: Wege, Kreuzungen, Rampen samt Böschung (`rampe_m` und `weg_rand_m` 5, nach dem Maßstab-Fix korrekt in Zellen), Sperrzone D1 (X084/rampe_2, Mulde 159|22,9: 0 Vertices geändert), D2.

## Neue Gate-Treffer (pruefe_regeln, Abgleich ±1,5 m) – im Nahbild unsichtbar

| # | Regel | Feld | x\|z | Wert | Urteil (Ton + Farbe, vorher/nachher) | Nahbild |
|---|---|---|---|---|---|---|
| N01 | `G5_beule_klippe` | G4 | 283.5\|140.0 | 0,69 | Unsichtbar: Folge des Maßstab-Fix bei Stelle 13 (Wegfläche zurückgesetzt). Die Klippenkante ist vorher und nachher gleich, keine Beule erkennbar | [t00](l3c_nahbilder/neue_treffer/t00_G5_beule_klippe_farbe_fx.jpg) |
| N02 | `G6_facette` | G6 | 268.2\|237.8 | 6 | Unsichtbar: Folge des Maßstab-Fix bei Stelle 23. Der Hang ist nachher eher glatter | [t01](l3c_nahbilder/neue_treffer/t01_G6_facette_farbe_fx.jpg) |
| N03 | `G6_facette` | G7 | 264.0\|268.8 | 18 | Unsichtbar: glattes, durchgehendes Flussbett unter Wasser; vorher standen hier die Leitern | [t02](l3c_nahbilder/neue_treffer/t02_G6_facette_farbe_fx.jpg) |
| N04 | `G6_facette` | H7 | 319.1\|275.4 | 9 | Unsichtbar: glatter Uferhang, Wasser durchgehend | [t03](l3c_nahbilder/neue_treffer/t03_G6_facette_farbe_fx.jpg) |

Sammelblatt: [neue_treffer_vorher_nachher.jpg](l3c_nahbilder/neue_treffer/neue_treffer_vorher_nachher.jpg). Entfallen: `G5_beule_klippe` H7 331.8|278.0.

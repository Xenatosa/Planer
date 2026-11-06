# Ergebnis pnahbild

## Ergebnis und Auswahl

Die beiden Prüfwerkzeuge und der opt-in-Prototyp sind umgesetzt. Die Standardauswahl ist `RELIEF_NEU_VAR=0` (Kontrolllauf): Sie exportiert die Quellanzeige unverändert und hat im gemessenen Delta keine Zunahme. Der Filterversuch `RELIEF_NEU_VAR=1` bleibt optional; er hat die Nahbildzahlen überwiegend verschlechtert und einen zusätzlichen G7b-Treffer erzeugt. Das angestrebte sichtbare Qualitätsplus wurde damit nicht erreicht.

Der neue Pfad liegt unter `neu/` und wird mit `RELIEF_NEU=1` in `gen_relief.py` und `baue_html.py` gewählt. Ohne den Schalter läuft die alte Pipeline. Der Prototyp erzeugt `neu/build/relief_daten_neu.json.gz` und `neu/build/index_neu.html`.

## Änderungen

- `neu/nahbild.py` erzeugt pro Kachel sechs feste Ansichten (Draufsicht, Streiflicht West/Ost, Kreuzung, Wegende, Wandfuß), je in Clay und Textur. Die Positionen stammen aus Kachelgrenzen, Straßen-/Rampenvektoren und Zellspalten. Der D2-Wandfuß fällt mangels markierter Wandfußzelle auf die Kachelmitte zurück.
- `neu/nahbild.js` misst Kanten-Zähne, Facetten, Helligkeitssprünge, Löcher und Flecken. `pruefung/nahbild_pnahbild/` enthält den vollständigen Nachher-Lauf mit 36 Bildern, Kameraliste und JSON.
- Die Nahbildaufnahme stoppt die Animation, setzt die Wasserzeit auf null, wartet auf geladene Texturen, schaltet Schattenkarten aus und verwendet feste Kameraposen sowie feste Lichtwerte. Die Richtungsbeleuchtung bleibt aktiv.
- `neu/delta.py` vergleicht Gate-Treffer nach Regel und Kachel sowie Clay-Bildzahlen. Texturwerte und Texturbilder bleiben für die Sichtkontrolle im Nahbild-JSON; Gebäude und Texturschattierung überlagern dort die Messung der Geländeform.
- `neu/gen_relief.py` exportiert einen getrennten Prototyp für D1, G1 und D2. Variante 0 ist der bytegleiche Kontrolllauf. Variante 1 filtert das Anzeige-Restfeld `GB-G` mit Sigma 0,60 m und Blend 0,40; Wege und Wasser bleiben ausgenommen, an Kachelgrenzen liegt eine 8-m-Fadezone.
- Die Wrapper in `gen_relief.py` und `baue_html.py` leiten nur bei `RELIEF_NEU=1` an den Prototyp weiter. Manuelle Render-Hooks greifen nur mit `?manual=1`; normale Ansichten behalten ihre Animation und Kamerasteuerung.

## Gates und Regelzahlen

Vergleich vor/nachher innerhalb dieses Worktrees (`7c0df80` → Kontrollvariante 0):

| Gate | vorher | nachher | Δ |
|---|---:|---:|---:|
| `pruefe_regeln` | 570 | 570 | 0 |
| R8 | 48 | 48 | 0 |
| R9 | 334 | 334 | 0 |
| offene Innenkanten | 0 | 0 | 0 |

Der übergebene historische Ausgangswert für `pruefe_regeln` ist 596 bei `9d3f8fc`. Der Start-Commit dieses Worktrees ist `7c0df80`; dort ergab dieselbe Prüfung vor der Änderung 570. Die R8- und R9-Werte stimmen mit den übergebenen Ausgangswerten überein. Die Vorher/Nachher-Tabellen unten verwenden den gemessenen Worktree-Stand, nicht die Differenz zwischen verschiedenen Commits.

| `pruefe_regeln` – Regel | vorher | nachher |
|---|---:|---:|
| R1_blind | 24 | 24 |
| R2_getrennt | 15 | 15 |
| R3_laengs_m | 35 | 35 |
| R3_quer_pct | 23 | 23 |
| R3_woelb_m | 22 | 22 |
| R5_loch | 17 | 17 |
| R6_wasser_schnee | 4 | 4 |
| G2_spitze_oben | 3 | 3 |
| G3_spitze_unten | 3 | 3 |
| G2_spitze_oben_fein | 8 | 8 |
| G3_spitze_unten_fein | 2 | 2 |
| G5_beule_klippe | 68 | 68 |
| G6_facette | 220 | 220 |
| G7_wand_glatte_flaeche | 1 | 1 |
| G8_fluss_nicht_bis_rand | 1 | 1 |
| T1_fleckrand | 94 | 94 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 |
| G7b_wandkontur_rauheit | 1 | 1 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 |
| G7b_wandkontur_feld | 24 | 24 |

| R8 – Regel | vorher | nachher |
|---|---:|---:|
| R8_stufe | 9 | 9 |
| R8_gitter | 10 | 10 |
| R8_quer | 5 | 5 |
| R8a_wegende | 24 | 24 |

| R9 – Regel | vorher | nachher |
|---|---:|---:|
| R8b_delle | 25 | 25 |
| R9_saegezahn | 34 | 34 |
| R9w_wellen | 275 | 275 |

## Treffer je Kachel

| Gate | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher | Gesamt vorher → nachher |
|---|---:|---:|---:|---:|
| `pruefe_regeln` | 36 → 36 | 13 → 13 | 8 → 8 | 570 → 570 |
| R8 | 8 → 8 | 1 → 1 | 0 → 0 | 48 → 48 |
| R9 | 26 → 26 | 8 → 8 | 0 → 0 | 334 → 334 |
| offene Innenkanten | 0 → 0 | 0 → 0 | 0 → 0 | 0 → 0 |

D2 hat in R8/R9 weiterhin null Treffer; `pruefe_regeln` hat dort keine neuen Treffer. Im optionalen Filterversuch stieg `G7b_wandkontur_feld` um einen Treffer in D1 (570 → 571 gesamt). R8 und R9 blieben dabei gleich, D2 bekam keine neuen Treffer. Keine Regel stieg um mehr als 5.

## Anzeige-, Zellquellen- und Dreieckszahlen

| Prüfung | Ergebnis |
|---|---|
| D2 `G`, `GB`, `VC`, `WEGA`, `WV`, `FW.h` | alle in D2 bytegleich |
| kodierte Zellquellspalten | 0 geänderte Werte in jeder Spalte, Summe 0 |
| Zellquellspalten geprüft | `untergrund`, `hindernis_id`, `hindernis_art`, `wasser_eis`, `ebene`, `bauzone_bestand`, `bauzone_plan`, `begehbar`, `bebaubar` |
| t42u-Abgleich mit Prototypdaten und Sidecar | 0 Abweichungen |
| lod1 gerenderte Dreiecke | 1.174.554 (< 1,3 Mio.) |
| Nahbild-Laufzeit, 3 Kacheln, 36 Bilder je Stand | vorher 59,174 s; nachher 57,797 s |

`hindernis` wird in der Quelldatei als `hindernis_id` und `hindernis_art` gespeichert; `bauzone` als `bauzone_bestand` und `bauzone_plan`. Im Kontrolllauf blieb `G` unverändert und `GB-G` wurde nicht angepasst. Die Werte von Variante 1 sind abgeleitete Anzeige-Werte; sie ändern keine kodierten Quellspalten.

## Nahbildzahlen

Je Zelle sind Summen der sechs Kameras für eine Kachel und einen Modus angegeben. Reihenfolge: Kanten-Zähne, Facetten, Helligkeitssprünge, Löcher+Flecken.

| Kachel / Modus | Zähne vorher → nachher | Facetten vorher → nachher | Sprünge vorher → nachher | Löcher+Flecken vorher → nachher |
|---|---:|---:|---:|---:|
| D1 / Clay | 3309 → 3309 | 7448 → 7448 | 6458 → 6458 | 84 → 84 |
| D1 / Textur | 32326 → 32347 | 4051 → 4056 | 175926 → 175817 | 3919 → 3904 |
| G1 / Clay | 2644 → 2644 | 7711 → 7711 | 3878 → 3878 | 49 → 49 |
| G1 / Textur | 29116 → 29110 | 5156 → 5156 | 118646 → 118641 | 2687 → 2683 |
| D2 / Clay | 24 → 24 | 649 → 649 | 2 → 2 | 0 → 0 |
| D2 / Textur | 37823 → 37826 | 4936 → 4934 | 201370 → 201374 | 3341 → 3341 |

Alle Clay-Zahlen und Clay-Bilder waren vor/nach bytegleich. Die Textur-Zahlen sind im JSON enthalten. Sie weichen zwischen den beiden HTML-Ständen leicht ab, obwohl die D2- und Kontroll-Anzeige-Arrays gleich sind; Häuser, Vegetation und Texturbeleuchtung belegen Pixel außerhalb der Geländeform. `delta.py` vergleicht deshalb für die Geometrieentscheidung nur Clay-Zahlen. Der gespeicherte Delta-Bericht weist 0 Anstiege aus.

Beispiele aus dem Nachher-Lauf: [D1 Draufsicht, Clay](nahbild_pnahbild/clay/D1_draufsicht.png), [D1 Kreuzung, Textur](nahbild_pnahbild/textur/D1_kreuzung.png), [G1 Streiflicht West, Clay](nahbild_pnahbild/clay/G1_streiflicht_west.png), [D2 Draufsicht, Textur](nahbild_pnahbild/textur/D2_draufsicht.png). Vollständige Messwerte: [nahbild_werte.json](nahbild_pnahbild/nahbild_werte.json); Kameras: [kameras.json](nahbild_pnahbild/kameras.json); [Delta-Bericht](nahbild_pnahbild/delta_pnahbild.md).

## Kalibrierung der Bildzahlen

- Bekannter Kreuzungsfehler, `/workspace/o18_kreuzung/nach2/D1_ton.png` → `/workspace/o18_kreuzung/nach3/D1_ton.png`: Kanten-Zähne 226 → 50; Facetten 2463 → 2627; Helligkeitssprünge 312 → 340; Sprung-Inseln 50 → 17. Das Zahnmaß reagiert auf die sichtbare Verbesserung; Facetten und Sprünge sind keine monotone Qualitätsnote.
- Bekanntes G6-Vorher/Nachher-Bild `pruefung/o18/t134u/g6_B5_vor_nach.png` (für die Messung in `/tmp/pnahbild_g6_vor.png` und `/tmp/pnahbild_g6_nach.png` geteilt): Zähne 0 → 26; Facetten 164 → 196; Sprünge 780 → 786; Löcher 0 → 1. Diese Signale markieren eine Änderung, klassifizieren die Ursache aber nicht zuverlässig.

## Tests, Annahmen und Grenzen

Ausgeführt und bestanden: `node neu/tests/test_nahbild_png.js`, `test_nahbild.js`, `test_nahbild_render.js`, `test_delta.js`, `test_gen_relief.js`, `test_baue_html.js`. Der Node-Satz prüft PNG-Messung, Kameraliste, Render-Orchestrierung, Delta-Exitcodes, deterministischen Export, Quellspalten/D2 und HTML-Erzeugung. `pytest` war in der Umgebung nicht installiert; die Node-Tests decken die Werkzeuge ab.

Der vorgegebene headless Chromium-Aufruf wartete 300 s auf `window.__test.bereit`, weil WebGL headless nicht startete. Die unveränderten Loch- und lod1-Prüfer liefen mit Xvfb und einem temporären Playwright-Start-Hook im headful Chromium; Gate-Code und Schwellen wurden nicht geändert.

Annahmen und Grenzen:

- Das sichtbare Restfeld `GB-G` kann für einen Anzeigeversuch gefiltert werden, während `G` die kanonische Zellhöhe bleibt. Das hält t42u bei 0.
- Nahbild-Zahlen sind Bild-Proxys. Texturwerte vermischen Gelände, Objekte und Beleuchtung; sie brauchen weitere Kalibrierung an eindeutig markierten Fehlerklassen.
- D2s Anzeigegeometrie ist auf den geprüften Arrays bytegleich. Textur-Screenshots sind keine Bytegleichheitsprüfung für die Anzeige.
- Variante 1 ist nicht freigegeben als Standard: maximale `GB`-Änderung 1,276628 m an 8.458 Punkten; ein zusätzlicher D1-G7b-Treffer und überwiegend steigende Clay-Bildsignale im damaligen Versuch. Der Kontrolllauf bleibt Standard.
- Keine Kosten (0 EUR). Die Gates und alten Schwellen blieben unangetastet; `../referenz/*`, Overlay- und Quellspalten wurden nicht editiert.

Offen ist eine besser kalibrierte, geometriespezifische Textur-Messung und eine Filtervariante, die sowohl die Sichtprüfung als auch die Gates nachweislich verbessert.

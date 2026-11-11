# Ergebnis p3d20

## Ergebnis

**Kein baubares p3d20-Mesh.** Der gemeinsame numerische MIP fand mehrfach optimale Punkte für die Modellgrenzen. In keinem geprüften Float32-Direkttransfer-Kandidaten hielten die unveränderten offiziellen Prüfer zugleich die p3d20-Ziele für G5, R5-Loch und R4. Das ist **kein Beweis**, dass jede exakte Formulierung dieser Zähler unlösbar ist; die hier verwendete iterative Ereignisformulierung erreichte keinen gültigen Kandidaten. Deshalb wurde weder der Schrittwert optimiert noch `gen_relief.py`/`baue_html.py` ausgeführt.

Der beste geprüfte Kandidat ist Runde 05. Er erfüllt die numerischen R8/R3/Endpunktgrenzen und die übrigen genannten D1-Ziele, verfehlt aber G5 um einen Treffer gesamt und einen in D1, R5-Loch um einen gesamt und einen in D1 sowie R4 um einen D1-Treffer.

## Änderungen und Modell

- Den offiziellen R3-Operator und den direkten p3d18-Transfer, Variante 24, weiterverwendet. Die unveränderte p3d17-Referenz kalibriert weiterhin auf D1 `6/17/19`; Bytevergleich erfolgreich. Beleg: [`kalibrierung_p3d17.json`](../../../../../codex_jobs/tools/p3d20_r3/kalibrierung_p3d17.json).
- Keine Änderung an Prüfern, Schwellen, Wegführung, Zellquellen, Overlay, D2 oder Ebenenkern `r=2,00 m`. Es gibt weder lokale Höhen-Pinning-Surrogate noch eine R9w-Gleichheitsfixierung.
- G5 wird an den offiziellen Wandabstands-, Richtungs- und Vier-Referenzpunkten als disjunktive Bedingung modelliert. Nach einer Gate-Auswertung werden neue Ereignisse pixelweise ergänzt; bei ausgewählten Komponenten umfassen spätere Schnitte alle aktuell positiven Pixel.
- R5-Loch wird mit derselben morphologischen Rekonstruktion wie der offizielle Prüfer ausgewertet. Die Schnitte beziehen sich auf den ermittelten Flutsattel und die aktuellen Tiefenpixel. Neue Senken können sich nach einer Höhenänderung an anderer Stelle bilden; deshalb ist das keine globale exakte MILP-Formulierung der Flood-Fill-Topologie.
- R4 nutzt die offiziellen 0,25-m-Weg-Samples und den Prüfer-Sprung von 16 Samples. Für jeden gefundenen Samplepunkt erzwingt eine Zwei-Wege-Disjunktion, dass mindestens eine Seite höchstens `1,5 m` über der Wegmitte liegt. Neue Treffer an benachbarten Samples werden erst nach dem jeweiligen Solve ergänzt.
- Für R9w wurde in einer Diagnose ein einzelner erkannter Bandpass-Peak linear begrenzt. Es wurden keine alten Höhenwerte gleichgesetzt. Der beste Kandidat hält R9w bereits bei 280.
- Die p3d18-Referenzkalibrierung des sekundären Tie-Breaks wurde geprüft. Für ein Referenzmesh wird die affine Übertragung auf die Modellvariablen zurückgerechnet; der vorangegangene direkte Vergleich von finaler Meshhöhe und Vor-Transfer-Variable war dimensionsmäßig falsch.

Das MIP verwendete in den geprüften Läufen Stufe `≤0,116 m`, Gitter `≤0,019 m`, Quergefälle `≤2,95 %`, Einzelquerung `≤19,5 %`, D1-R3 `≤6/≤7/≤7`, Achsstützen `±0,02 m` und am Wegende `156.5|37.5` Stufe `≤0,054 m`. Der 2-m-Kern blieb fest. Runde 05 fand eine optimale Modelllösung mit 7.945 Variablen und 11.295 Bedingungen. Der offizielle Prüfer sah den Float32-Direkttransfer, nicht ein mit `gen_relief.py` gebautes Exportmesh.

## Zahlen je Regel

Historischer Startwert laut Auftrag/Stand `9d3f8fc`: `pruefe_regeln=596`. Die Einzelregeln unten verwenden die archivierten p3d17-Zähler; im damaligen Artefakt fehlt die Kategorie G11, daher ist sie dort konservativ als `0` notiert. Ein Replay der unveränderten p3d17-Referenz mit dem aktuellen Prüfer ergibt `600` einschließlich `G11=4`; Runde 05 ergibt mit demselben aktuellen Prüfer `563`. Der Schemaunterschied ist offengelegt, nicht als Verbesserung verbucht.

| Regel | historisch vorher | p3d20 Runde 05 | Δ |
|---|---:|---:|---:|
| G11_objekt_schwebt_sinkt | 0* | 4 | +4 |
| G2_spitze_oben | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten | 4 | 3 | -1 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 69 | 70 | +1 |
| G6_facette | 219 | 218 | -1 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G7b_wandkontur_feld | 25 | 25 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 33 | -2 |
| R3_quer_pct | 29 | 12 | -17 |
| R3_woelb_m | 31 | 16 | -15 |
| R4_rand | 1 | 0 | -1 |
| R4_schlucht | 0 | 1 | +1 |
| R5_loch | 25 | 23 | -2 |
| R5_spitze | 0 | 0 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| **Summe** | **596** | **563** | **-33** |

\* Die archivierte 596er-Regeltabelle stammt aus einem Prüferstand ohne G11-Zähler. Der aktuelle-schema p3d17-Replay hat G11 `4`, Runde 05 ebenfalls `4`; gegenüber diesem Replay ist Δ `0`. Keine Regel steigt gegenüber dem passenden Zählerstand um mehr als `+5`.

| R8-Regel | Start `9d3f8fc` | p3d20 Runde 05 | Δ |
|---|---:|---:|---:|
| R8_stufe | 9 | 7 | -2 |
| R8_gitter | 10 | 8 | -2 |
| R8_quer | 5 | 4 | -1 |
| R8a_wegende | 24 | 20 | -4 |
| **R8 gesamt** | **48** | **39** | **-9** |

| R9-Regel | Start `9d3f8fc` | p3d20 Runde 05 | Δ |
|---|---:|---:|---:|
| R8b_delle | 25 | 23 | -2 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 280 | +5 |
| **R9 gesamt** | **334** | **337** | **+3** |

Der p3d17-Referenz-Replay mit dem aktuellen Prüfer zählt R9w `287`; dieser ältere Vergleichswert lockert das Ziel ausdrücklich nicht. Runde 05 bleibt auf `≤280`.

## D1, G1 und D2

Die folgende Tabelle vergleicht die p3d18-Variante-24-Probe mit dem besten p3d20-Float32-Modellprobe-Kandidaten. Alle nicht aufgeführten D1-Regeln sind unverändert. G1 und D2 sind regelweise unverändert.

| Regel / Messwert | D1 p3d18 → p3d20 | G1 p3d18 → p3d20 | D2 p3d18 → p3d20 |
|---|---:|---:|---:|
| G3_spitze_unten | 2 → 0 | 0 → 0 | 0 → 0 |
| G5_beule_klippe | 2 → 3 | 0 → 0 | 0 → 0 |
| G6_facette | 7 → 2 | 3 → 3 | 0 → 0 |
| R3_laengs_m | 6 → 4 | 1 → 1 | 0 → 0 |
| R3_quer_pct | 5 → 0 | 0 → 0 | 0 → 0 |
| R3_woelb_m | 6 → 4 | 0 → 0 | 0 → 0 |
| R4_schlucht | 0 → 1 | 0 → 0 | 0 → 0 |
| R5_loch | 5 → 6 | 0 → 0 | 0 → 0 |
| R5_spitze | 5 → 0 | 0 → 0 | 0 → 0 |
| R8b_delle | 3 → 1 | 0 → 0 | 0 → 0 |
| R9w_wellen | 23 → 21 | 12 → 12 | 0 → 0 |
| R8-Treffer an Zielkreuz / Wegende | 1 Quer-Treffer am Kreuz → 0 | 0 → 0 | 0 → 0 |

Übrige ausgewiesene D1-Regeln blieben auf ihren p3d18-Zählerständen: G11 `2`, G7b-Feld `1`, R1 `2`, R2 `1`; D2 blieb bei R2 `1` und T1 `7`. G1 blieb bei G11 `2`, G6 `3`, R1 `1`, R3 längs `1`, R6 Wasser/Schnee `3`, T1 `3`.

## Modellwerte und nicht erfüllte Zähler

| Messung in Runde 05 | Modell / Float32-Probe | Ziel | Ergebnis |
|---|---:|---:|---|
| R8 Kreuzung `152.5|28.5`, Stufe | `0,11526 m` | Modell `≤0,116 m`, Prüfer `≤0,116 m` | erfüllt |
| R8 Kreuzung, Gitter | `0,01900 m` | Modell `≤0,019 m`, Prüfer `≤0,020 m` | erfüllt, Modellgrenze bindet |
| R8 Kreuzung, Quergefälle | `2,9500 %` | Modell `≤2,95 %`, Prüfer `≤3 %` | erfüllt, Modellgrenze bindet |
| D1 R3 längs/quer/wölbung | `4/0/4` | `≤6/≤7/≤7` | erfüllt |
| Modell-Einzelquerung | `≤19,5 %` | `≤19,5 %` | erfüllt |
| Achsstützen | 359 Stützpunkte mit `±0,02 m`-Bedingungen | `±0,02 m` | Modellbedingungen erfüllt |
| Wegende `156.5|37.5`, Stufe | `0,054 m` | `≤0,054 m` | erfüllt |
| Wegende, R8a | 0 Treffer | 0 | erfüllt |
| G5 gesamt / D1 | `70 / 3` | `≤69 / ≤2` | **verfehlt um 1 / 1** |
| R5-Loch gesamt / D1 | `23 / 6` | `≤22 / ≤5` | **verfehlt um 1 / 1** |
| R4-Schlucht D1 | `1` | `0` | **verfehlt um 1** |
| R5-Spitze D1 | `0` | `0` | erfüllt |
| G6-Facette D1 | `2` | `≤3` | erfüllt |
| R8b-Delle D1 | `1` | `≤1` | erfüllt |
| G3-Spitze unten D1 | `0` | `≤1` | erfüllt |
| R9w gesamt | `280` | `≤280` | erfüllt |

Neue D1-Ereignisse im besten Probe-Kandidaten:

- **G5**: Komponentenzentrum `161,375|28,125`, Prüferausgabe `161,4|28,1`; Peak `0,713 m` am Rasterpunkt `161,0|28,0` gegen `0,60 m`. Kein Rampenweg ist beteiligt. Die Komponente ist ein zusätzlicher D1-Treffer.
- **R5-Loch**: neuer Tiefenpunkt `158,0|17,5`, Fülltiefe `1,020 m`, Fläche `0,2 m²`; der Prüfer meldet `1,02 m`. Erhöht D1 von 5 auf 6.
- **R4-Schlucht**: Weg `rampe_2`, offizieller Sampleindex `67` (Wegstation `16,75` bei 0,25-m-Sampling), Mittelpunkt `143,1364|29,5895`. Modellprobe `1,5416 m` (Prüfer `1,54 m`), Ziel `≤1,50 m`. Seitliche Samples: `143,6177|33,5605` und `142,6551|25,6186`.

Bestkandidatenbeleg: [`machbarkeit_round05.json`](../../../../../codex_jobs/tools/p3d20_r3/machbarkeit_round05.json), [`best_probe_round05.json`](../../../../../codex_jobs/tools/p3d20_r3/official_gates/best_probe_round05.json) und unveränderte Prüferausgaben unter [`official_gates/`](../../../../../codex_jobs/tools/p3d20_r3/official_gates/). Runde 12 belegt die Nichtkonvergenz der lokalen Schnittfolge: Der numerische MIP blieb optimal, aber die Gate-Probe lag bei G5 `72`, R5-Loch `26`, R4 D1 `1` und erzeugte wieder einen D1-Gittertreffer (`0,247 m`). Siehe [`latest_probe_round12.json`](../../../../../codex_jobs/tools/p3d20_r3/official_gates/latest_probe_round12.json).

## Kacheln, Quellen und offene Prüfungen

- D1-Höhenhash der besten Float32-Probe: `2c8c93b294285ed2fb4c1b9729544b2c6b7103958813022ba32620a73bc74ed4` (verschieden von `9619da5083720eb43f736043452b28f87dd2f9aa946dc2cb453b5ed972d02c6c`, `28f6f9abb2033d561d49ab3b688b470eecf63f352d00faaa29ffb5af8e9ce45c` und früheren Hashes).
- G1-Höhenhash unverändert: `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb`.
- D2-Höhenhash unverändert: `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`; D2-Regelzahlen unverändert. R8/R9 haben auf D2 weiterhin 0 Treffer.
- Quellreliefhash: `5e8fdb51c3f3dff9ad2c03c32c7a39ee1a4f97a3bc0942d47a352b1d0b4f0e88`; `vektor.json`/Wegführung und Zellquellen wurden nicht bearbeitet.
- Im Modellprobe-Prüfer wurde `LOCHSCAN` auf `{offen_innen:0}` gesetzt, damit die übrigen Regelzähler berechnet werden. Das ist **kein** echter Lochscan. Es wurden weder Raycast/xvfb noch `t42u`, `pytest`, `delta.py`, LOD1-Dreieckszahl oder Bildvergleich ausgeführt, weil kein Mesh gebaut wurde.
- Keine Bilder unter `bilder_p3d20/`, kein tatsächlicher `relief_daten.json.gz`-Build und keine HTML-Ausgabe. Daher sind Klippenhöhe `140|35`, Textur-/Streiflichtqualität und reale Mesh-LOD nicht bestätigt.
- Laufzeit-/Modellnachweis liegt außerhalb des Worktrees in `/workspace/codex_jobs/log_p3d20.txt`: `gpt-6-luna`, reasoning effort `xhigh`.

Offener Punkt: Die gemeinsame numerische Modellmenge ist nicht leer. Die geprüften Kandidaten verfehlen jedoch die offiziellen G5/R5/R4-Zähler; die adaptiven lokalen Schnitte sind keine vollständige globale Zählermodellierung. Damit ist die geforderte End-to-End-Machbarkeit **nicht nachgewiesen**, aber auch nicht mathematisch widerlegt. Kein Mesh wurde gebaut oder übernommen.

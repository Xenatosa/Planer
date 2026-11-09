# Ergebnis p3d13 — stetiger Transfer an Rampeninnenecken

Stand: 09.11.2026 · Branch `art/dorfmap-p3d13` · Basis `origin/art/dorfmap-p3d12` / `8366bd1`.

## Ergebnis in Kürze

Variante `16` ist Standard. Sie überträgt die gelösten Stationen über ein globales Thin-Plate-Feld, verwendet die nur aus den Profilstationen bestimmte Ebene im Kernradius 2,25 m und blendet sie bis 4 m C1-stetig aus. Variante `15` bleibt über `RELIEF_KREUZUNG_VAR=15` verfügbar; Varianten `5`, `10`–`14` bleiben ebenfalls anwählbar.

Der Hauptfehler ist **nicht behoben**. Die R8-Stufe an `152.5|28.5` bleibt `0,535 m` (Ziel `≤0,116 m`). Variante 15 senkt sie auf `0,209 m`, verfehlt den Zielwert aber ebenfalls und hat mehr Gate-Treffer. Variante 16 entfernt dort den R8-Gittertreffer und hat die niedrigsten Gesamtzähler. Im Streiflicht bleibt an rampe_11 eine sichtbare Falte.

Es wurden nur `neu/mesh.py`, generierte Viewerdateien, das neue MILP-Werkzeug und Prüfartefakte geändert. Zellquellwerte, `vektor.json`, Overlay, Referenzen, Prüfer, Schwellen und Tests blieben unverändert. D2 ist bytegleich geblieben.

## Änderung und Variantenvergleich

- `neu/mesh.py`: Varianten 15 und 16 ergänzen den vorhandenen räumlichen MILP-Transfer. Für die D1-Höhenfläche verwendet Variante 15 `scipy.interpolate.RBFInterpolator` mit Thin-Plate-Spline-Kern und allen gelösten Stationen. Der Rampenabstand wird über eine stetige Soft-Min-Funktion bestimmt; die vorhandene Wegführung und Wegebreite werden nicht angefasst.
- Variante 15 verwendet `g=0,45` und die aus dem Profil gelöste Ebene für unbedeckte Flächen im Radius `2,25–4 m`. Variante 16 nutzt dieselben Profile und dieselbe Ebene auch über der Profilfläche im Kern. Beide MILP-Ebenen haben maximal `0,05 m` Stationsabweichung und höchstens `3 %` Neigung.
- Der Solver koppelt nun auch Stationen derselben Rampe, wenn `d≤4,5 m` und der Bogenabstand `>1,5·d` ist. Auf den D1-Rampen erfüllt **kein** Same-Route-Paar diese Kriterien; alle 857 berücksichtigten Paare sind zwischen rampe_2 und rampe_11. Der gemessene Selbstüberlappungsfall wird daher von diesen MILP-Paarbedingungen nicht beschränkt.

| Variante | Transfer | R8 Kreuzung: Stufe / Gitter / Quer | Prüfer-Summen: Regeln / R8 / R9 |
|---|---|---:|---:|
| 15 | Thin-Plate-Feld, Ebene nur außerhalb der Profilabdeckung | `0,209 m` / `0,209 m` / `6,2 %` | `583 / 51 / 341` |
| **16 Standard** | Thin-Plate-Feld, Ebene über Profilfläche im Kern, C1-Auslauf | `0,535 m` / `0,015 m` / `3,6 %` | `567 / 42 / 338` |

Die 2-cm-Probe für Variante 16 wurde verworfen: Die Kreuzungsstufe blieb dabei etwa `0,55 m`; der Endstand verwendet wieder die 5-cm-Toleranz. Es gibt keine dritte Variante.

## Ecken und Mehrfachminima vor dem Transfer

Die Ecken wurden an den D1-Polylinien aus Drei-Punkt-Krümmung und Richtungswechsel gemessen. `R` ist der kleinste lokale Krümmungsradius; der Winkel ist der gesamte Richtungswechsel im kurzen Eckfenster. Die Bandhalbbreite des Transfers beträgt `1,81 m`.

| Rampe | s (m) | x\|z | R min (m) | Richtungswechsel |
|---|---:|---:|---:|---:|
| rampe_2 | — | — | keine Ecke unter 1,81 m | — |
| rampe_11 | 9,30–9,60 | `144.8252\|9.5397` | 0,264 | 81,51° (lokal max. 62,20°) |
| rampe_11 | 28,50 | `157.5350\|18.8411` | 0,241 | 72,83° |
| rampe_11 | 47,40–47,70 | `150.1723\|32.7338` | 0,366 | 79,94° (lokal max. 42,51°) |

Die vollständigen Mesh-Knotenlisten stehen in [`ueberlappungen_band_1_81m_vorher.csv`](bilder_p3d13/ueberlappungen_band_1_81m_vorher.csv) und [`ueberlappungen_coord_1_81_einheiten_vorher.csv`](bilder_p3d13/ueberlappungen_coord_1_81_einheiten_vorher.csv). Erfasst wurden D1-Punkte im 0,25-Kartenkoordinatenraster (0,30 m), lokale Abstandminima mit mindestens 1 m Bogenabstand und Sollhöhen aus dem MILP-Profil. Mit der tatsächlichen physischen Bandhalbbreite `1,81 m` gibt es 236 Knoten mit mindestens zwei Minima; mit dem unskalierten Koordinaten-Schwellenwert `1,81` (entspricht `2,172 m`) sind es 348.

| Mesh-Knoten | Minimum A: Rampe / s / d / Soll | Minimum B: Rampe / s / d / Soll | Δ Soll | Zwei Minima im physischen 1,81-m-Kern? |
|---|---|---|---:|---|
| `152.00\|32.00` | rampe_11 / 45,587 m / 1,549 m / 3,703091 m | rampe_11 / 48,780 m / 2,146 m / 2,316364 m | 1,386727 m | nein; B liegt im Auslauf |
| `152.00\|32.25` | rampe_11 / 45,859 m / 1,690 m / 3,567011 m | rampe_11 / 48,955 m / 1,903 m / 2,252370 m | 1,314641 m | nein; B liegt 0,093 m außerhalb |

Damit ist die Behauptung einer **doppelten Überdeckung innerhalb 1,81 m physisch** an genau diesen beiden Punkten widerlegt. Die im Ausgangshinweis genannten Distanzen `1,29` bzw. `1,59–1,79` entsprechen Kartenkoordinaten, nicht Metern. In den Koordinateneinheiten liegen beide Minima innerhalb `1,81`; in Metern ist jeweils nur A im Kern. Der Höhenkonflikt und die benachbarte Stufe bleiben dennoch vorhanden.

## MILP-Machbarkeit

Die unabhängige Neuberechnung ist unter [`codex_jobs/tools/p3d13_milp/`](../../../../../codex_jobs/tools/p3d13_milp/) abgelegt. Es wurden 2 Rampenprofile mit Schrittweite `0,30 m` und 857 räumliche Paare ausgewertet; kein zusätzliches Dorfwegprofil liegt innerhalb 6 m.

| g | Quer-Rampen-Paare | Same-Route-Paare | Paarungleichungen | Status | R3-Abschnitte gesamt / D1 | Hc (m) | max. Quellenabweichung (m) | L1-Änderung (m) | max. Paargefälle |
|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 0,60 | 857 | 0 | 1.714 | optimal | 5 / 3 | 4,340800 | 1,758260 | 103,999558 | 0,60 |
| 0,45 | 857 | 0 | 1.714 | optimal | 5 / 3 | 4,303255 | 1,804759 | 107,471639 | 0,45 |

Beide MILPs sind mit höchstens sechs D1-R3-Abschnitten machbar (je drei). Das belegt nur die 1D-Profillösung; die nachfolgende 2D-Meshprüfung findet weiterhin mehr R3-Treffer als erlaubt.

## Regeln vorher/nachher

Die unmittelbar vor p3d13 gespeicherten p3d12-Zahlen stehen neben dem Endstand. Für den älteren Rohstand `9d3f8fc` lagen im Auftrag nur die Aggregate und die R8/R9-Regelzähler vor; deshalb sind dessen `pruefe_regeln`-Einzelregeln als `—` markiert.

| Prüfer | 9d3f8fc | p3d12 | p3d13 | Δ p3d12→p3d13 |
|---|---:|---:|---:|---:|
| `pruefe_regeln` Summe | 596 | 568 | 567 | −1 |
| R8 Summe | 48 | 43 | 42 | −1 |
| R9 Summe | 334 | 338 | 338 | 0 |

| `pruefe_regeln` Regel | 9d3f8fc | p3d12 | p3d13 | Δ p3d12→p3d13 |
|---|---:|---:|---:|---:|
| R1_blind | — | 24 | 24 | 0 |
| R2_getrennt | — | 15 | 15 | 0 |
| R3_laengs_m | — | 37 | 39 | +2 |
| R3_quer_pct | — | 21 | 20 | −1 |
| R3_woelb_m | — | 21 | 19 | −2 |
| R5_loch | — | 17 | 17 | 0 |
| R6_wasser_schnee | — | 4 | 4 | 0 |
| G2_spitze_oben | — | 3 | 3 | 0 |
| G3_spitze_unten | — | 3 | 3 | 0 |
| G2_spitze_oben_fein | — | 8 | 8 | 0 |
| G3_spitze_unten_fein | — | 2 | 2 | 0 |
| G5_beule_klippe | — | 67 | 67 | 0 |
| G6_facette | — | 217 | 217 | 0 |
| G7_wand_glatte_flaeche | — | 1 | 1 | 0 |
| G7b_wandkontur_feld | — | 25 | 25 | 0 |
| G7b_wandkontur_kantenschaerfe | — | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | — | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | — | 1 | 1 | 0 |
| G11_baum_an_wand | — | 2 | 2 | 0 |
| T1_fleckrand | — | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | — | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | — | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | — | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | — | 1 | 1 | 0 |

| R8/R9 Regel | 9d3f8fc | p3d12 | p3d13 | Δ roh→p3d13 |
|---|---:|---:|---:|---:|
| R8_stufe | 9 | 8 | 8 | −1 |
| R8_gitter | 10 | 9 | 8 | −2 |
| R8_quer | 5 | 5 | 5 | 0 |
| R8a_wegende | 24 | 21 | 21 | −3 |
| R8b_delle | 25 | 22 | 22 | −3 |
| R9_saegezahn | 34 | 34 | 34 | 0 |
| R9w_wellen | 275 | 282 | 282 | **+7** |

Die +5-Grenze wird bei `R9w_wellen` gegenüber dem genannten Rohstand weiterhin um 2 überschritten. Diese Regel und die Sägezähne wurden nicht bearbeitet.

### D1, G1 und D2

| Kachel | `pruefe_regeln` p3d12→p3d13 | R8 p3d12→p3d13 (Stufe/Gitter/Quer/Wegende) | R9 p3d12→p3d13 (Delle/Sägezahn/Wellen) |
|---|---:|---:|---:|
| D1 | 33→32 | `1/1/1/1` → `1/0/1/1` | `0/1/21` → `0/1/21` |
| G1 | 11→11 | `0/0/0/0` → `0/0/0/0` | `0/1/12` → `0/1/12` |
| D2 | 8→8 | `0/0/0/0` → `0/0/0/0` | `0/0/0` → `0/0/0` |

D2 hat gegenüber p3d12 keine neuen `pruefe_regeln`-Treffer; die acht Treffer haben dieselben Regel-/Koordinatensignaturen. R8 und R9 bleiben in D2 bei null.

## Profilabgleich, verbleibende D1-Treffer und Zielwerte

Die 359 D1-Achsstationen sind in [`profil_tabelle.csv`](bilder_p3d13/profil_tabelle.csv) enthalten. Bilinear aus dem finalen 0,5-m-Mesh gelesen weichen 80/359 Stationen um mehr als `±0,02 m` vom MILP-Soll ab: rampe_2 `34/168`, rampe_11 `46/191`. Der größte Fehler bei rampe_2 ist `−0,338097 m` bei `s=28,5 m`, `150.0849|28.7422`; bei rampe_11 `−0,207696 m` bei `s=44,1 m`, `151.4502|30.2991`. Achsgenauigkeit ist nicht erreicht.

| Verbleibender D1-R8-Treffer | Checkerwert / Ort | Maximaler Feinpunkt-Sprung und Höhen | Beteilgte Stationen |
|---|---|---|---|
| R8_stufe | `0,535 m` bei `152.5|28.5` | `152.00|32.00`: `3,645063 m` → `152.00|32.25`: `3,110064 m` (`Δ=0,534999 m`) | zwei lokale Minima derselben rampe_11: `s=45,587 m`, Soll `3,703091 m`; `s=48,780 m`, Soll `2,316364 m` |
| R8_quer | `3,6 %` bei `152.5|28.5` | dieselbe lokale Stufenstelle wie oben; der Querwert ist der Ebenenfit im Prüfkreis, kein einzelnes Höhenpaar | rampe_11 `s=45,587/48,780 m`; A liegt im Kern, B im Auslauf |
| R8a_wegende | `0,23 m` am Wegende `156.5|37.5` | `157.50|35.50`: `0,574869 m` → `157.75|35.50`: `0,805194 m` (`Δ=0,230325 m`) | beide Feinpunkte nahe rampe_11 `s≈56,7 m`; Soll an der Station `0,546556 m` |

R8_stufe und R8a bleiben Treffer. Der Wegendwert `0,086 m` ist außerdem schlechter als p3d11 (`0,054 m`); der Endpunkt hat weiterhin einen R8a-Treffer, wo p3d11 keinen hatte. G1 bleibt unverändert bei null R8-Treffern.

Die acht D1-R3_quer-Treffer enthalten vier Werte über 20 %: `35,1 %` bei `150.4|33.1`, `31,1 %` bei `151.8|29.6`, `21,0 %` bei `154.5|16.6` und `20,1 %` bei `157.5|19.1`. R3_laengs hat 10 D1-Treffer (Maximum `0,396 m` bei `150.3|28.7`); R3_woelb hat 7 (Maximum `0,453 m` bei `150.4|33.1`).

| Ziel | p3d13 | Ergebnis |
|---|---:|---|
| Kreuzungsstufe `≤0,116 m` | 0,535 m | verfehlt |
| Kreuzungsgitter `≤0,02 m` | 0,015 m | erreicht |
| R3_laengs D1 `≤6` | 10 Treffer | verfehlt |
| R3_quer D1 `≤7`, kein Wert `>20 %` | 8; max. `35,1 %` | verfehlt |
| R3_woelb D1 `≤7` | 7 Treffer | erreicht (Grenzwert) |
| D1-Achse: Mesh/Soll `±0,02 m` | 80/359 außerhalb | verfehlt |
| R8/R8a D1/G1 `0` | D1: 3; G1: 0 | verfehlt |
| Clay-Facetten an Kreuzung `≤317` | 397 (p3d8: 317; p3d12: 391) | verfehlt |
| Geländeänderung `≤4,0 m` | max. 3,643326 m | erreicht |
| D1-Hash neu | `8aa69a17…` | erfüllt; verschieden von allen gesperrten Hashes |
| G1-Hash | `38afeb30…` | unverändert |
| D2-Hash | `749d3c4b…` | bytegleich zum p3d12-Stand |
| Klippe `140|35` | `7,88403654 m` | erreicht |
| LOD1-Dreiecke | 134.316 / 1.300.000 | erreicht |

G6 und G11 in D1 sind gegenüber p3d8 schlechter: G6 `0→1`, G11 `0→2`. D1 R8b, Sägezahn und Wellen bleiben bei p3d8 (`0/1/21`). Die übrigen R8-Treffer außerhalb D1, andere Wegenden, Wände/Wandfüße, G1, D2 und Sägezähne wurden nicht bearbeitet.

## Deltas, Bilder und Prüfungen

Die Delta-Vergleiche stehen in [`delta_p3d6_p3d13.md`](bilder_p3d13/delta_p3d6_p3d13.md), [`delta_p3d8_p3d13.md`](bilder_p3d13/delta_p3d8_p3d13.md), [`delta_p3d12_p3d13.md`](bilder_p3d13/delta_p3d12_p3d13.md) und [`delta_VAR0_p3d13.md`](bilder_p3d13/delta_VAR0_p3d13.md). Gate-/Bild-Anstiege: p3d6 `8/16` (gesamt 24), p3d8 `7/16` (23), p3d12 `1/4` (5), VAR0 `7/23` (30). Die geforderten null Gate-Anstiege von p3d6 und p3d8 sind nicht erreicht. Der einzelne Gate-Anstieg p3d12→p3d13 ist `R3_laengs_m` in D1 (`8→10`, +2). Es gibt in keinem dieser Deltas einen neuen D2-Treffer.

Für p3d6, p3d8 und VAR0 waren keine ursprünglichen Gate-JSON-Snapshots vorhanden; die Referenzzähler wurden aus den gespeicherten p3d12-Delta-JSONs (`vorher`-Spalte) rekonstruiert und unter `bilder_p3d13/referenzstaende/` abgelegt. Deren D1/G1/D2-Regel- und Clay-Kamerazähler gehen zeilenweise in `neu/delta.py` ein.

Die geforderten Bilder sind in [`bilder_p3d13/`](bilder_p3d13/) gespeichert. D1-Kreuzung, rampe_11-Streiflicht, D1-Wandfuß, D1-Wegende, G1-Wandfuß und D2-Draufsicht wurden für p3d8, p3d12 und p3d13 selbst angesehen. Die Kreuzung wirkt im Clay großflächig ruhiger als der frühe p3d8-Stand; im Streiflicht bleibt aber ein sichtbarer Querknick/Falz über rampe_11. Die D2-Draufsicht p3d12→p3d13 ist pixelidentisch (1000×700, 0 geänderte Farbkanäle); es gibt hier keine Screenshot-Differenz trotz bytegleichem Mesh.

| Prüfung | Ergebnis |
|---|---|
| Standardbau `python3 gen_relief.py && python3 baue_html.py` | ausgeführt |
| Neu-Mesh-Bau mit `RELIEF_NEU=1` | ausgeführt; Wiederholungsbau ergab identische SHA-256 für `index.html`, `neu/index.html`, `neu/build.json`, `neu/relief_neu.json.gz` und `relief_daten.json.gz` |
| Lochscan/Raycast mit xvfb | Exit 0; 9 Meshes, 88.728 Dreiecke, `offen_innen=0` |
| `pruefe_regeln` / R8 / R9 | 567 / 42 / 338; Exit 1 wegen aufgeführter Treffer |
| `pruefe_t42u.py` | Summe 0; alle Abweichungsfelder 0 |
| `pytest neu/tests` | **25 passed, 6 failed** (Ziel mindestens 26/5 verfehlt); `test_gelaende_mesh`: 4/4 bestanden |

Die sechs Pytest-Fehler: `test_kreuzung_d1_g1_mesh_stufe` (`0,535>0,20 m`), `test_wegende_allgemein_mesh_ohne_blindenden` (21 Treffer), `test_saegezahn_d1_mesh_count` (D1 31 Elemente), `test_verwaschene_wand_d1_kantenschaerfe` (2,24<3,00), `test_wegende_f1_c1_meshmessung` (0,17>0,10 m; keine C1-Endpunkte) und `test_schattenartefakt_renderbild` (0,307>0,25). Prüfer, Schwellen und Tests wurden nicht verändert.

## Annahmen, Grenzen und offene Punkte

- Die Distanzen und Stationswerte sind physisch in Metern angegeben; Koordinaten in der Karte werden mit `CELL_M=1,2` umgerechnet. Dadurch liegt das zweite Minimum der beiden hervorgehobenen Knoten nicht innerhalb des 1,81-m-Kerns, obwohl es im unskalierten Koordinatenwert 1,81 liegt.
- Der Thin-Plate-RBF ist eine global interpolierende Fläche über alle D1-Profilstationen. Die gemessene Reststufe, die 80 Achsabweichungen und die Streiflichtfalte zeigen, dass diese Variante den Wechsel an der Innenecke noch nicht ausreichend löst.
- R3-Zahlen gelten für den finalen Mesh-Adapter. Die drei MILP-Abschnitte je D1-Rampe sagen die R3-Trefferzahl des fertigen 2D-Meshes nicht voraus.
- Laufzeitnachweis: [`/workspace/codex_jobs/log_p3d13.txt`] (Modell `gpt-6-luna`, reasoning effort `xhigh`). Kosten: 0 EUR.

# Ergebnis p3d11 — Kreuzungsprofil ohne harten Rampenwechsel

Stand: 09.11.2026 · Branch `art/dorfmap-p3d11` · Basis `origin/art/dorfmap-p3d10` / `992f191`. Variante `12` ist Standard; Varianten `5`, `10` und `11` bleiben über `RELIEF_KREUZUNG_VAR` wählbar.

## Änderung

- `neu/mesh.py`: Varianten `11` und `12` ergänzen p3d10s vollständigen 1D-MILP-Profillöser. In den überlappenden Vollbreitenstreifen werden an 46 gemeinsamen Rasterpunkten im Radius 5 m Profilhöhen mit maximal 0,004 m Abweichung gekoppelt.
- Der 2D-Transfer verwendet einen normalisierten, glatten Gewichtsmix statt eines harten Wechsels zur nächstgelegenen Rampe. Das volle Band reicht bis 1,81 m Halbbreite; der Geländefade beginnt außerhalb und ist 9,5 m lang. Variante `12` blendet eine gemeinsame Ebene im 5-m-Kern ein und lässt sie außerhalb der Wegprofile auslaufen.
- Die bisherigen Transfers der Varianten `8`–`10` bleiben erhalten. Für Variante `10` ist der D1-Höhenhash bytegleich mit p3d10: `2b3655e774fe0cb3035ba3f9967a29c1d8ff91ddda6860e3576663eade6f1b39`.
- Variante `12` ist trotz verfehlter Zielwerte die bessere der beiden neuen Varianten: sie verbessert die Stufe und die gezählten R3-Querfehler gegenüber `11` und p3d10. Die Zielwerte sind damit nicht erreicht.
- Keine Zellquellen, Prüfer, Schwellen, Overlay-, Referenz- oder D2-Geometrie geändert. Tests blieben unverändert.

## Gate-Ergebnisse

| Vergleichsstand | `pruefe_regeln` | R8 | R9 |
|---|---:|---:|---:|
| p3d6, Adapter-Snapshot | 563 | 39 | 336 |
| p3d8, Adapter-Snapshot | 570 | 39 | 336 |
| p3d10, Adapter-Snapshot | 565 | 43 | 340 |
| **p3d11, Adapter** | **560** | **40** | **338** |

Der vom Auftrag genannte Roh-Ausgangswert `596 / 48 / 334` stammt aus `9d3f8fc`. Das p3d10-Protokoll reproduzierte auf der damaligen Quellbasis roh `570 / 48 / 334`; die p3d6/p3d8/p3d10-Vergleiche hier verwenden daher die protokollierten, vergleichbaren Adapter-Snapshots. Gegen p3d10 steigt keine globale Regel um mehr als +2. Die strengeren Delta-Ziele werden trotzdem verfehlt: p3d6→p3d11 hat drei Gate-Anstiege; p3d8→p3d11 ebenfalls drei.

### Zahlen vorher/nachher je Regel (p3d10 → p3d11)

| Gruppe | Regel | vorher | nachher | Δ |
|---|---|---:|---:|---:|
| pruefe_regeln | `G11_baum_an_wand` | 2 | 0 | -2 |
| pruefe_regeln | `G2_spitze_oben` | 3 | 3 | +0 |
| pruefe_regeln | `G2_spitze_oben_fein` | 8 | 8 | +0 |
| pruefe_regeln | `G3_spitze_unten` | 3 | 3 | +0 |
| pruefe_regeln | `G3_spitze_unten_fein` | 2 | 2 | +0 |
| pruefe_regeln | `G5_beule_klippe` | 67 | 67 | +0 |
| pruefe_regeln | `G6_facette` | 218 | 220 | +2 |
| pruefe_regeln | `G7_wand_glatte_flaeche` | 1 | 1 | +0 |
| pruefe_regeln | `G7b_wandkontur_feld` | 25 | 25 | +0 |
| pruefe_regeln | `G7b_wandkontur_kantenschaerfe` | 1 | 1 | +0 |
| pruefe_regeln | `G7b_wandkontur_rauheit` | 1 | 1 | +0 |
| pruefe_regeln | `G8_fluss_nicht_bis_rand` | 1 | 1 | +0 |
| pruefe_regeln | `R1_blind` | 24 | 24 | +0 |
| pruefe_regeln | `R2_getrennt` | 15 | 15 | +0 |
| pruefe_regeln | `R3_laengs_m` | 35 | 34 | -1 |
| pruefe_regeln | `R3_quer_pct` | 21 | 18 | -3 |
| pruefe_regeln | `R3_woelb_m` | 19 | 18 | -1 |
| pruefe_regeln | `R5_loch` | 17 | 17 | +0 |
| pruefe_regeln | `R6_wasser_schnee` | 4 | 4 | +0 |
| pruefe_regeln | `T1_fleckrand` | 94 | 94 | +0 |
| pruefe_regeln | `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 |
| pruefe_regeln | `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 |
| pruefe_regeln | `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 |
| pruefe_regeln | `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 |
| R8 | `R8_gitter` | 9 | 8 | -1 |
| R8 | `R8_quer` | 5 | 4 | -1 |
| R8 | `R8_stufe` | 8 | 8 | +0 |
| R8 | `R8a_wegende` | 21 | 20 | -1 |
| R9 | `R8b_delle` | 23 | 22 | -1 |
| R9 | `R9_saegezahn` | 34 | 34 | +0 |
| R9 | `R9w_wellen` | 283 | 282 | -1 |

### D1, G1 und D2 je Kachel (p3d10 → p3d11)

| Kachel | Prüfe-Regeln | R8: Stufe / Gitter / Quer / Wegende | R9: Delle / Sägezahn / Wellen |
|---|---:|---|---|
| D1 | 30 → 25 | 1/1/1/1 → 1/0/0/0 | 1/1/21 → 0/1/23 |
| G1 | 11 → 11 | 0/0/0/0 → 0/0/0/0 | 0/1/12 → 0/1/12 |
| D2 | 8 → 8 | 0/0/0/0 → 0/0/0/0 | 0/0/0 → 0/0/0 |

D2 bleibt bei `pruefe_regeln=8`, R8 `0`, R9 `0`; kein D2-Treffer kam hinzu. D1 hat nur noch einen R8-Treffer (`R8_stufe`); G1 hat keine R8-Treffer. D1 R8a-Wegende bleibt bei 0. Die D1-R9-Wellen steigen aber von 21 auf 23; damit ist die geforderte p3d8-Regressionfreiheit verfehlt.

## 1D-Profil und 2D-Transfer

Der MILP-Löser endet optimal: 6 R3-Abschnitte über 0,075 m, Zielfunktionssumme `|ΔQuelle|=132,84814 m`, maximale Profiländerung `1,678721 m`. Die gemeinsame Ebene liegt bei `4,554548 m`; ihr Solverfehler ist höchstens `0,002 m`. Sechs gekoppelte Abschnitte sind in `neu/build.json` ausgewiesen.

| D1-Regel | p3d11 | Ziel | Ergebnis |
|---|---:|---:|---|
| R3 längs | 5 | ≤6 | erreicht |
| R3 quer | 6 Treffer | ≤7 und kein Wert >20 % | Anzahl erreicht, Querziel verfehlt |
| R3 Wölbung | 6 | ≤7 | erreicht |

R3-Querwerte über 20 % bleiben: `20,9 %` bei `154,5|16,6`, `23,5 %` bei `157,5|19,1`, `47,8 %` bei `151,8|29,6` und `36,3 %` bei `150,4|33,1`. Das weist auf die 2D-Übertragung entlang der engen Kurve hin: die MILP-Nebenbedingungen optimieren das 1D-Längsprofil und koppeln die gemeinsamen Rasterpunkte, setzen aber kein queres 2D-Flächenprofil durch.

| Messstelle | p3d10 | p3d11 | Ziel |
|---|---:|---:|---:|
| Kreuzung `152.5|28.5`, R8-Stufe | 1,028 m | 0,791 m | ≤0,116 m |
| Kreuzung `152.5|28.5`, R8-Gitter | 0,037 m | 0,004 m | ≤0,020 m |
| Wegende `156.5|37.5`, R8-Stufe | 0,119 m | 0,054 m | ≤0,20 m |
| Wegende `156.5|37.5`, R8-Gitter / Quer | 0,236 m / 3,7 % | 0,082 m / 0,7 % | kein neuer Treffer ggü. p3d8 |
| Wegende `156.5|37.5`, R8a | 0,23 m | kein Treffer | kein neuer Treffer ggü. p3d8 |

Die Kreuzungsstufe bleibt deutlich zu hoch; der R8-Prüfer misst im finalen Mesh `0,791 m`, obwohl der 1D-Löser eine gemeinsame Ebene hält. Das belegt, dass die verbleibende Stufe im 2D-Transfer/der finalen Rasterfläche entsteht. Der Gitterwert ist im Ziel.

Achsenabgleich aus [`profil_tabelle.csv`](bilder_p3d11/profil_tabelle.csv), 388 Stationen insgesamt und 359 in D1:

| Rampe | D1-Stationen über ±0,02 m | Maximum Mesh−Soll | Station | x|z |
|---|---:|---:|---:|---|
| rampe_2 | 5 / 168 | +0,077568 m | 21,75 | 148,1003|28,9900 |
| rampe_11 | 7 / 191 | −0,047508 m | 39,50 | 150,1723|32,7338 |

Der verpflichtende ±0,02-m-Abgleich ist **nicht erfüllt**. Die verbleibenden Achsfehler liegen zwischen den Solverstationswerten und der 0,5-m-Mesh-Rasterinterpolation; die Profilkopplung allein beseitigt diesen Transferfehler nicht.

## Mesh, D2/G1 und weitere Prüfungen

- D1-Höhenhash `146bfdacfa17e10a678d311131bc79b8400c421cbc95330f38f8899ebe403bd9`; er weicht von allen verbotenen Hashes ab. G1 bleibt `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb`; D2 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`. Der Adapter meldet `d2_gb_mesh_bytegleich=true`; `zellen_quell_diff=0`.
- D1-Quellabweichung im Gelände-Mesh: Maximum `2,607691 m` bei `148.0|31.5` (unter 4,0 m). Am früheren Testproblem `128.5|37.5` ist sie `+0,000358 m`. Der festgehaltene Klippenwert bei `140|35` bleibt `7,8840365 m`.
- t42u: Summe `0`. Lochscan mit xvfb: `0` offene Innenkanten, `0` Punkte, `88.728` Terrain-Dreiecke. LOD1: `134.316` Dreiecke (`<1,3 Mio.`).
- Zwei unmittelbar aufeinanderfolgende Standard-Builds hatten bytegleiche `index.html`, `neu/index.html`, `neu/build.json` und `neu/relief_neu.json.gz` (SHA-256 der HTML `20d3425dd53e3ebf1b08d4f0901144699c72ce448abfe7737ca487a6edd3cbc8`).

### Screenshots

Die p3d8- und p3d10-Vorherbilder wurden neben den sechs neu gerenderten p3d11-Pflichtansichten geprüft. Die Kreuzungsfalte ist im p3d11-Crossing und Streiflicht weiter sichtbar; visuell ist die Fläche nicht weich genug. Die Clay-Facettenzahl an der Kreuzung ist `317` (p3d8) → `562` (p3d10) → `640` (p3d11), also über dem p3d8-Ziel. p3d11 Kreuzung, Streiflicht, Wandfuss, Wegende, G1 und D2 liegen unter [`nachher/`](bilder_p3d11/nachher/).

| Kamera | p3d8 | p3d10 | p3d11 |
|---|---:|---:|---:|
| D1 Kreuzung – Facetten | 317 | 562 | 640 |
| D1 Wandfuss – Facetten | 515 | 418 | 796 |
| D1 Wegende – Facetten | 825 | 982 | 811 |
| G1 Wandfuss – Facetten | 530 | 530 | 530 |
| D2 Draufsicht – Facetten | 0 | 21 | 0 |

D2 blieb meshseitig unverändert. Screenshot-Hashes: p3d8 `e8db06e608ee2bb6c833c7ca4112a487b5671c5fc2141798c4efd2321350158a`; p3d10 `558b76f28b8417786eb568b4f5cdf62639154fded1bad330179e40531bf3b8b0`; p3d11 `ed4c0264468ee7ccca2fb55fddfcb0fd3778affc23275f3ca7e6a66478c33982`. Der reproduzierte p3d11-Render weicht von p3d8 nur in 153 Pixeln und höchstens 1 Graustufe ab. Die größere p3d10-Abweichung (7.955 Pixel, maximal 25 Graustufen) lässt sich aus den gespeicherten Artefakten nicht eindeutig einer Licht- oder Renderursache zuordnen; sie wurde mit dem p3d11-Aufbau nicht reproduziert.

### Delta-Berichte

`neu/delta.py` wurde für VAR0, p3d6, p3d8 und p3d10 gegen p3d11 ausgeführt. Die alten Einzel-Gate-Snapshots liegen nicht als separate JSONs vor; die vorher/nachher-Zähler für VAR0/p3d6/p3d8 wurden aus den committed p3d10-Delta-JSONs rekonstruiert. Die Gate-Erhöhungen p3d6→p3d11 und p3d8→p3d11 sind jeweils `G6_facette D1 +4`, `R8_stufe D1 +1` und `R9w_wellen D1 +2`. Gegen p3d10 kommen `G6_facette D1 +2` und `R9w_wellen D1 +2` hinzu.

| Delta | positive Gate/Image-Metriken | Gate-Anstiege | Bildmetriken-Anstiege |
|---|---:|---:|---:|
| VAR0 → p3d11 | 22 | 6 | 16 |
| p3d6 → p3d11 | 17 | 3 | 14 |
| p3d8 → p3d11 | 11 | 3 | 8 |
| p3d10 → p3d11 | 13 | 2 | 11 |

Die vollständigen JSON-/Markdown-Tabellen stehen bei [`delta_p3d6_p3d11`](bilder_p3d11/delta_p3d6_p3d11.md), [`delta_p3d8_p3d11`](bilder_p3d11/delta_p3d8_p3d11.md), [`delta_p3d10_p3d11`](bilder_p3d11/delta_p3d10_p3d11.md) und [`delta_var0_p3d11`](bilder_p3d11/delta_var0_p3d11.md).

## Tests und offene Punkte

`pytest -q neu/tests`: **25 bestanden, 6 fehlgeschlagen**. p3d10 referenzierte 23/8; die verlangte Grenze 26/5 wird um einen Test verfehlt. Fehlschläge: Kreuzungsstufe 0,791 m; allgemeine Wegenden 20; D1 Sägezahn 73 Elemente; D1 Wandkantenschärfe 2,24 (Grenze 3,00); F1 Wegende 0,17 m / C1-Prüfstellen 0; Schattenartefakt-Score 0,307 (Grenze 0,25). Prüfer und Schwellen wurden nicht verändert.

Annahmen und Grenzen: `R8` misst den Kreuzungskern bis 4 m Karteneinheiten (etwa 4,8 m). Das 5-m-Profilfenster koppelt die überlappenden Rasterpunkte; es löst jedoch nicht das gekrümmte 2D-Querprofil. Die Achsentabelle nutzt die p3d10-Abtaststationen und sampelt das tatsächlich gebaute Mesh bilinear. Der p3d10-D2-Screenshot-Ausreißer bleibt ohne nachweisbare Einzelursache.

Offen: Für den Zielzustand braucht es ein queres 2D-Flächenprofil oder eine Kopplung, die gleichzeitig die R8-Stufe, die >20-%-Querwerte und die ±0,02-m-Achsabweichung beseitigt, ohne die verfehlten Gate-Delta-Ziele zurückzubringen. Diese Variante erreicht das nicht. Laufzeitnachweis (Modell/Reasoning Effort): `/workspace/codex_jobs/log_p3d11.txt`.

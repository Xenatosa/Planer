# Ergebnis p3d12 — räumlich gekoppelte Rampenprofile

Stand: 09.11.2026 · Branch `art/dorfmap-p3d12` · Basis `origin/art/dorfmap-p3d11` / `4dd4c62`.
Variante `14` ist Standard. Die bisherigen Varianten `5`, `10`, `11`, `12` und die neue Vergleichsvariante `13` bleiben über `RELIEF_KREUZUNG_VAR` anwählbar.

## Änderung

- `neu/mesh.py`: Für Variante 13/14 werden die Profile von rampe_2 und rampe_11 gemeinsam mit räumlichen Nebenbedingungen gelöst. Die Stationen werden in Abständen von 0,25 Kartenkoordinaten (0,30 m) genommen. Ein MILP minimiert zuerst die R3-Abschnitte über 0,075 m, danach die Summe der absoluten Änderungen zur unveränderten GB-Quelle.
- Der Ebenenkern endet bei 2,25 m um `152.5|28.5`; Stationshöhen liegen höchstens 0,05 m von einer Ebene mit höchstens 3 % Neigung entfernt. Zwischen den 857 zulässigen Stationspaaren mit Abstand bis 4,5 m gilt `|dh| <= g*d`; Variante 13 verwendet `g=0,60`, Variante 14 `g=0,45`. Die Längsänderung je 0,25-Kartenkoordinaten ist auf 0,15 m begrenzt. End- und Wandrandbindungen folgen dem p3d10-Ansatz.
- Der 2D-Transfer mischt die Profile glatt und normalisiert, auch dort, wo sich Rampenabschnitte räumlich überlagern. Das volle Profilband reicht bis 1,81 m Halbbreite; erst außerhalb beginnt der 9,5-m-Fade. Die Ebene kommt ausschließlich aus dem gelösten Profil und läuft C1-stetig von 2,25 m bis 4 m aus.
- Beide MILPs sind optimal und mit höchstens sechs R3-Abschnitten machbar. Variante 14 ist Standard, weil sie die gemessene Kreuzungsstufe gegenüber 13 weiter verringert (0,535 statt 0,581 m); ihre strengere Paargrenze benötigt jedoch mehr Profilbewegung.
- Keine Zellquellwerte, Wegevektoren, Prüfer, Schwellen, Overlay- oder Wandgeometrie wurden geändert. `zellen_quell_diff=0`.

## Ausgangswerte und Gate-Ergebnisse

| Stand | `pruefe_regeln` | R8 | R9 |
|---|---:|---:|---:|
| Im Auftrag genannter Roh-Ausgangspunkt `9d3f8fc` | 596 | 48 | 334 |
| p3d11-Adapter, gleicher Neu-Mesh-Prüfpfad | 560 | 40 | 338 |
| **p3d12-Adapter, Variante 14** | **568** | **43** | **338** |

R8 p3d12: `Stufe 8`, `Gitter 9`, `Quer 5`, `Wegende 21`. R9: `Delle 22`, `Sägezahn 34`, `Wellen 282`.

Die vollständige Regeländerung p3d11 → p3d12 steht in der Tabelle. Kein einzelner Eintrag steigt dabei um mehr als 3. Gegen den ausdrücklich genannten Roh-Ausgangspunkt steigt `R9w_wellen` jedoch von 275 auf 282 (**+7**) und überschreitet damit die +5-Vorgabe.

| Regel laut Roh-Ausgangspunkt | 9d3f8fc | p3d12 | Δ |
|---|---:|---:|---:|
| `R8_stufe` | 9 | 8 | -1 |
| `R8_gitter` | 10 | 9 | -1 |
| `R8_quer` | 5 | 5 | 0 |
| `R8a_wegende` | 24 | 21 | -3 |
| `R8b_delle` | 25 | 22 | -3 |
| `R9_saegezahn` | 34 | 34 | 0 |
| `R9w_wellen` | 275 | 282 | +7 |

| Regel | p3d11 | p3d12 | Δ |
|---|---:|---:|---:|
| `G11_baum_an_wand` | 0 | 2 | +2 |
| `G2_spitze_oben` | 3 | 3 | 0 |
| `G2_spitze_oben_fein` | 8 | 8 | 0 |
| `G3_spitze_unten` | 3 | 3 | 0 |
| `G3_spitze_unten_fein` | 2 | 2 | 0 |
| `G5_beule_klippe` | 67 | 67 | 0 |
| `G6_facette` | 220 | 217 | -3 |
| `G7_wand_glatte_flaeche` | 1 | 1 | 0 |
| `G7b_wandkontur_feld` | 25 | 25 | 0 |
| `G7b_wandkontur_kantenschaerfe` | 1 | 1 | 0 |
| `G7b_wandkontur_rauheit` | 1 | 1 | 0 |
| `G8_fluss_nicht_bis_rand` | 1 | 1 | 0 |
| `R1_blind` | 24 | 24 | 0 |
| `R2_getrennt` | 15 | 15 | 0 |
| `R3_laengs_m` | 34 | 37 | +3 |
| `R3_quer_pct` | 18 | 21 | +3 |
| `R3_woelb_m` | 18 | 21 | +3 |
| `R5_loch` | 17 | 17 | 0 |
| `R6_wasser_schnee` | 4 | 4 | 0 |
| `T1_fleckrand` | 94 | 94 | 0 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | 0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | 0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | 0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | 0 |
| `R8_stufe` | 8 | 8 | 0 |
| `R8_gitter` | 8 | 9 | +1 |
| `R8_quer` | 4 | 5 | +1 |
| `R8a_wegende` | 20 | 21 | +1 |
| `R8b_delle` | 22 | 22 | 0 |
| `R9_saegezahn` | 34 | 34 | 0 |
| `R9w_wellen` | 282 | 282 | 0 |

### D1, G1 und D2 je Kachel

Die `pruefe_regeln`-Spalte zählt alle Regeln für die jeweilige Kachel. R8 steht als `Stufe/Gitter/Quer/Wegende`, R9 als `Delle/Sägezahn/Wellen`.

| Kachel | Regeln p3d11 → p3d12 | R8 p3d11 → p3d12 | R9 p3d11 → p3d12 |
|---|---:|---|---|
| D1 | 25 → 33 | 1/0/0/0 → 1/1/1/1 | 0/1/23 → 0/1/21 |
| G1 | 11 → 11 | 0/0/0/0 → 0/0/0/0 | 0/1/12 → 0/1/12 |
| D2 | 8 → 8 | 0/0/0/0 → 0/0/0/0 | 0/0/0 → 0/0/0 |

D2 hat keine neuen `pruefe_regeln`-Treffer; R8 und R9 bleiben dort bei 0. G1 bleibt beim p3d11-Höhenhash `38afeb30…`. D2 bleibt bytegleich mit dem sichtbaren GB-Mesh, Hash `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`.

Die engere Vorgabe „p3d6→p3d12 und p3d8→p3d12 ohne Gate-Anstieg“ ist **nicht erreicht**. `neu/delta.py` zählt p3d6→p3d12 10 Gate-Anstiege (26 Anstiege insgesamt), p3d8→p3d12 9 Gate-Anstiege (25 insgesamt). p3d11→p3d12 ergibt 9 Gate- und 15 Bildmetrik-Anstiege (24 insgesamt). JSON- und Markdown-Details liegen bei [`delta_p3d6_p3d12`](bilder_p3d12/delta_p3d6_p3d12.md), [`delta_p3d8_p3d12`](bilder_p3d12/delta_p3d8_p3d12.md), [`delta_var0_p3d12`](bilder_p3d12/delta_var0_p3d12.md) und [`delta_p3d11_p3d12`](bilder_p3d12/delta_p3d11_p3d12.md).

Gegen p3d8 ist D1 außerdem schlechter bei `G6_facette` (0 → 1) und `G11_baum_an_wand` (0 → 2). D1 `R8b_delle`, `R9_saegezahn` und `R9w_wellen` sind nicht schlechter (0/1/21 in beiden Ständen).

## MILP-Machbarkeit

Nur rampe_2 und rampe_11 haben Rampen-/Wegfläche im 6-m-Umkreis der Kreuzung; es kam kein weiterer Weg hinzu. Die Tabellen der beiden vollständigen Läufe liegen in [`machbarkeit_g60.json`](../../../../../codex_jobs/tools/p3d12_milp/machbarkeit_g60.json) und [`machbarkeit_g45.json`](../../../../../codex_jobs/tools/p3d12_milp/machbarkeit_g45.json). Das wiederverwendbare Werkzeug ist [`feas2d_p3d12.py`](../../../../../codex_jobs/tools/p3d12_milp/feas2d_p3d12.py).

| Variante | g | zulässige Stationspaare | optimale Abschnitte >0,075 m gesamt / D1 | Hc | max. paarweises dh | max. Profiländerung zur Quelle | L1-Quelle | Ebene: Neigung / max. Abweichung | ≤6 Abschnitte machbar |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 13 | 0,60 | 857 (1.714 Ungleichungen) | 5 / 3 | 4,340800 m | 2,101597 m | 1,758260 m | 103,999558 m | 3,0 % / 0,05 m | ja |
| 14 | 0,45 | 857 (1.714 Ungleichungen) | 5 / 3 | 4,303255 m | 2,010206 m | 1,804759 m | 107,471639 m | 3,0 % / 0,05 m | ja |

Bindende Paarbedingungen bei `g=0,60` liegen am Kreuzungskern: rampe_2 `s=26,00`, `152.3184|28.4702`, gegen rampe_11 `s=34,75`, `152.3953|28.5365` (`d=0,121850 m`, `|dh|=0,073110 m`); sowie rampe_2 `s=26,25`, `152.5666|28.4401`, gegen rampe_11 `s=34,50`, `152.5121|28.3155` (`d=0,163226 m`, `|dh|=0,097935 m`). Beide liegen exakt auf der 0,60-Grenze.

Bei `g=0,45` binden zusätzlich die nahen Kehrenäste: `rampe_2 s=22,25` gegen `rampe_11 s=38,75` (`d=4,402139 m`, `|dh|=1,980962 m`) und `s=22,50` gegen `s=39,00` (`d=4,467123 m`, `|dh|=2,010206 m`). Beide liegen auf der 0,45-Grenze. Die zwei Kreuzungspaare binden auch in Variante 14 mit `|dh|=0,054833 m` bzw. `0,073452 m`.

Die 1D-Machbarkeit ist damit nachgewiesen. Die verbleibenden Verstöße entstehen beim 2D-Transfer in die endgültige Oberfläche: der Checker findet nach dem Transfer in D1 8 R3-Längs-, 9 R3-Quer- und 9 R3-Wölbungstreffer. Die Zielzahlen waren ≤6/≤7/≤7. Der größte R3-Querwert ist 35,1 % bei `150.4|33.1`; dort beträgt R3-Längs 0,121 m und Wölbung 0,453 m. Weitere Querwerte über 20 %: 21,0 % bei `154.5|16.6`, 20,1 % bei `157.5|19.1` und 31,1 % bei `151.8|29.6`.

## Profilachse und Kreuzung

Die vollständige 388-Stationen-Tabelle mit Quelle, MILP-Soll und bilinear aus dem finalen 0,5-m-Mesh abgetasteter Höhe steht in [`profil_tabelle.csv`](bilder_p3d12/profil_tabelle.csv). 359 Stationen liegen in D1; 63 davon weichen um mehr als 0,02 m vom Soll ab.

| Rampe | D1-Stationen | über ±0,02 m | größte Abweichung Mesh−Soll | Station | x, z |
|---|---:|---:|---:|---:|---|
| rampe_2 | 168 | 26 | +0,089834 m | 24,75 | 151,077307, 28,619417 |
| rampe_11 | 191 | 37 | −0,175288 m | 36,75 | 151,450216, 30,299076 |

Der Achsabgleich ist **nicht erfüllt**. Die maximale Terrainänderung innerhalb D1 beträgt 3,643326 m und bleibt unter der geforderten 4,0-m-Grenze.

| Messstelle | p3d11 | p3d12 | Ziel | Ergebnis |
|---|---:|---:|---:|---|
| Kreuzung `152.5|28.5`, R8-Stufe | 0,791 m | 0,535 m | ≤0,116 m | verfehlt |
| Kreuzung, R8-Gitter | 0,004 m | 0,197 m | ≤0,020 m | verfehlt |
| Kreuzung, R8-Quer | 3,7 % | 4,3 % | höchstens 3 % (Prüfschwelle) | verfehlt |
| Wegende `156.5|37.5`, R8-Stufe | 0,054 m | 0,086 m | nicht schlechter als p3d11 | schlechter |
| Wegende, R8-Gitter / Quer | 0,082 m / 0,7 % | 0,118 m / 1,8 % | nicht schlechter als p3d11 | schlechter |
| Wegende, R8a | kein Treffer | 0,23 m | nicht schlechter als p3d11 | schlechter |

Alle acht verbleibenden R8-Stufentreffer mit größter Feinpunktkante und beiden Meshhöhen:

| Kachel | R8-Kreuzungszentrum (x, z) | Δh | Feinpunkt A → B (x, z) | Höhe A → B |
|---|---|---:|---|---:|
| C3 | 125,269, 126,547 | 0,951252 m | 123,25, 127,00 → 123,25, 127,25 | 4,908997 → 5,860250 m |
| C5 | 124,477, 197,978 | 0,254107 m | 125,00, 199,25 → 125,25, 199,25 | 0,264129 → 0,010022 m |
| C6 | 113,285, 228,611 | 0,222929 m | 113,75, 230,25 → 114,00, 230,25 | −12,673061 → −12,450132 m |
| D1 | 152,550, 28,490 | 0,534999 m | 152,00, 32,00 → 152,00, 32,25 | 3,645063 → 3,110064 m |
| D6 | 132,906, 232,436 | 0,461526 m | 136,25, 230,75 → 136,50, 230,75 | −9,450435 → −8,988909 m |
| G3 | 269,805, 117,257 | 0,339302 m | 268,75, 118,25 → 269,00, 118,25 | 0,001774 → 0,341076 m |
| H4 | 298,160, 149,250 | 0,343021 m | 298,00, 148,00 → 298,25, 148,00 | 11,656979 → 12,000000 m |
| H5 | 319,963, 213,983 | 0,260971 m | 321,00, 213,00 → 321,25, 213,00 | 7,129098 → 6,868127 m |

Die Kreuzungsstufe liegt weiterhin auf der Kehrenseite: zwischen `152.00|32.00` und `152.00|32.25` fällt die Feinmesh-Höhe von 3,645063 auf 3,110064 m. Das erklärt auch, warum ein machbares gemeinsames 1D-Profil die Stufe im finalen 2D-Mesh nicht beseitigt hat.

## Bilder und Regressionen

Die sechs Ansichten sind unter [`bilder_p3d12/nachher`](bilder_p3d12/nachher/) gespeichert. Verwendet wurden die fünf Kameras aus p3d6 und das Streiflicht aus p3d10. Die Clay-Bilder von p3d8 und p3d11 sowie die sechs neuen Ansichten wurden visuell geprüft. Die Kreuzung wirkt im normalen Clay-Bild ruhiger als p3d11, aber die Falte bleibt im Streiflicht deutlich sichtbar. Die p3d12-Kreuzungsansicht zählt 391 Facetten: besser als p3d11 (640), aber über p3d8 (317) und damit über dem Ziel von 317. D1 Wandfuß: 421 Facetten; Wegende: 840; G1 Wandfuß: 530.

Der D2-Meshhash bleibt exakt unverändert. Das neu gerenderte D2-Bild ist aber nicht pixelgleich zu den archivierten Ansichten: SHA-256 `06b898bb432032a776c1fcbc423d40ccc66dbff1889f586ba30a5cca37e3a381`, gegenüber p3d11 `ed4c0264468ee7ccca2fb55fddfcb0fd3778affc23275f3ca7e6a66478c33982`. 6.517 Pixel weichen ab, maximal um 17 Kanalstufen; der Clay-Bildindikator zählt 13 statt 0 Facetten. Eine direkte Wiederholung des p3d12-Renderings war bytegleich. Ursache dieser Differenz zu den gespeicherten D2-Bildern ist ungeklärt; D2-Geometrie und -Höhenbytes sind unverändert.

## Mesh, Determinismus und Tests

- D1-Höhenhash: `e1b5250808fba3a51b7bc1a801afa2453b275362a0a50e5de483e8e8b6f4b53d`; verschieden von allen im Auftrag ausgeschlossenen Hashes. G1: `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb`; D2 wie oben bytegleich.
- Klippenkontrolle `140|35`: 7,8840365 m. `t42u`: Summe 0, alle Teilfelder 0. Lochscan unter xvfb: 9 Meshes, 88.728 Terrain-Dreiecke, 0 offene Innenkanten, 0 Punkte.
- LOD1: 134.316 Dreiecke von 1.300.000; darunter.
- Der Standardbau `python3 gen_relief.py && python3 baue_html.py` sowie der Neu-Mesh-Bau mit `RELIEF_NEU=1` wurden ausgeführt. Zwei aufeinanderfolgende Neu-Mesh-Bauten ergaben dieselben Hashes: `index.html`/`neu/index.html` `b66e6589…`, `neu/build.json` `3392bd76…`, `neu/relief_neu.json.gz` `fc369323…`, `relief_daten.json.gz` `5e8fdb51…`.
- `python3 -m pytest -q neu/tests`: **25 bestanden, 6 fehlgeschlagen**; Ziel ≥26/5 verfehlt. Unveränderte Tests melden Kreuzungsstufe 0,535 m, 21 allgemeine Wegenden, 32 D1-Sägezähne, D1-Wandkantenschärfe 2,24 (Grenze 3,00), F1-Wegende 0,17 m/C1 ohne Messung sowie Schattenbild-Score 0,307 (Grenze 0,25).
- `pruefe_regeln.py`, `r8_kreuzung.py` und `r9_form.py` enden wie vorgesehen mit Exit 1 wegen vorhandener Treffer; Zahlen stehen in den JSONs unter `bilder_p3d12/nachher/`. `pruefe_t42u.py` endet mit Exit 0.

## Annahmen, Grenzen und offene Punkte

- Die MILP-Ebene wird nur an Profilstationen im Radius 2,25 m bewertet. Der 2D-Transfer und der nachfolgende 0,5-m-Meshraster garantieren keine ±0,02-m-Übereinstimmung zwischen diesen Stationen; das zeigen 63 Abweichungen.
- Die Nachbarschaftsbedingung derselben Rampe gilt entsprechend Auftrag erst bei Bogenabstand über 8 m. Der Prüfer bewertet dagegen die komplette Wegfläche bis 4 m um die Kreuzung.
- Nicht erreicht sind die Kreuzungsziele für R8-Stufe, Gitter, Quergefälle, Clay-Facetten und die sichtbare Faltenfreiheit; außerdem die R3-Zahlen, der Achsabgleich, der spezielle Wegendpunkt, die p3d6/p3d8-Delta-Grenze, die p3d8-G6/G11-Vorgabe, die +5-Grenze für `R9w_wellen` gegen den Roh-Ausgangspunkt, pytest ≥26/5 und die Pixelgleichheit des D2-Screenshots.
- Die Wand-/Wandfuß-Logik wurde nicht bearbeitet. Außer `156.5|37.5` wurden keine Wegenden gezielt optimiert.
- Laufzeitnachweis: Modell `gpt-6-luna`, Reasoning effort `xhigh`, laut [`log_p3d12.txt`](/workspace/codex_jobs/log_p3d12.txt).

Die 1D-Machbarkeit ist belegt; das geforderte p3d12-Endziel ist **nicht erreicht**. Das Hauptproblem liegt im 2D-Transfer der räumlich benachbarten Rampenabschnitte und bleibt im fein gerasterten Mesh sichtbar.

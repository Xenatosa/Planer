# Ergebnis p3d9

**Ergebnis: teilweise erreicht; das Kernziel wurde nicht erreicht.** Variante 6 entfernt die zweite radiale Einebnung und erhält den echten Höhen-Fade des gemeinsam gelösten Längsprofils. Die Kreuzungsstufe bleibt unter 0,20 m, aber sie ist schlechter als der p3d6-Vergleichswert; die R3-Zielzahlen werden nicht erfüllt. R9w D1 steigt gegenüber p3d8 um einen Treffer.

**Branch:** `art/dorfmap-p3d9`
**Basis:** `origin/art/dorfmap-p3d8` bei `123408b`
**Laufzeitnachweis:** `/workspace/codex_jobs/log_p3d9.txt` (`gpt-6-luna`, `xhigh`).

## Änderung

- `neu/mesh.py` bietet die Kreuzungsvarianten `5`, `6` und `7` über `RELIEF_KREUZUNG_VAR` an. Variante 5 bleibt die p3d8-Referenz. Variante 6 lässt `plane_mix` weg; das LP-Ziel wird weiter mit `target * weight + background * (1-weight)` in die p3d6-Fläche gemischt. Variante 7 blendet die gemeinsame Ebene nur innerhalb der LP-Rampenabschnitte ein.
- **Variante 6 ist Standard.** Sie hat die kleinere Kreuzungsstufe der beiden neuen Varianten (0,177 statt 0,195 m) und mehr Abstand zur Obergrenze von 0,20 m. Variante 7 hat die kleinere Gitterabweichung (0,004 statt 0,032 m) und etwas bessere Kreuzungsbild-Proxys. Beide verfehlen den p3d6-Stufenwert 0,116 m.
- Die Solver-Ebene der ausgewählten Variante liegt bei rund 4,01 m. Die zweite radiale Ebene wurde entfernt, der Solver-Höhenverlauf dadurch aber nicht auf p3d6-Höhe angehoben.
- Änderungen: `neu/mesh.py`, `neu/README.md`, gebaute Viewer-Dateien, Ergebnisbericht und Bild-/Delta-Artefakte. Schwellen, Prüfer, Tests, `gen_relief.py`, Zellquellwerte, Overlay und `../referenz/*` wurden nicht geändert.

### Variantenvergleich

| Variante | R8-Stufe am D1-Schnitt | R8-Gitter | Kreuzung Clay-Facetten | Kantenzähne | Normalsprünge | Inseln | R3 längs / quer / Wölbung D1 | R9w gesamt |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 (p3d8-Referenz) | 0,043 m | 0,000 m | 317 | 36 | 484 | 57 | 14 / 9 / 8 | 280 |
| **6 (Standard)** | **0,177 m** | 0,032 m | 362 | 32 | 520 | 74 | 14 / 10 / 8 | 281 |
| 7 | 0,195 m | 0,004 m | 359 | 32 | 513 | 69 | 14 / 10 / 8 | 281 |

## Build und Schutzprüfungen

Gebaut im Relief-Ordner mit `RELIEF_NEU=1 python3 gen_relief.py && RELIEF_NEU=1 python3 baue_html.py`; anschließend wurde der Standard-Adapter mit `pruefung/neu_mesh_adapter.py` erzeugt.

| Messung | p3d9 |
|---|---:|
| LOD1 gesamt | 134.316 / 1.300.000 Dreiecke |
| Gelände / Wände | 88.728 / 45.588 Dreiecke |
| Lochscan | 0 offene Innenkanten, 0 Punkte; 9 Meshes, 88.728 Geländedreiecke |
| `t42u` | Summe 0; alle neun Abweichungsfelder 0 |
| Zellquell-Diff | 0 |
| D1-Klippenwert bei `140\|35` | 7,8840365 m; unverändert |

Der D1-Adapter-Hash wechselte vom p3d8-Wert `d8d44ff95c7d748e77696a3d0b9027007836c5b18b5e362df0b97db7969a9ecc` auf `3f196347690ef4cd203c8156d6d3250cd538e71fef018f04fb1457609d363222`. Er ist weder der p3d6-Hash `bbc2de2fe035800122fae0b222e55247e5cece3d0ebba131447cf41a367c97e2` noch der p3d7-Crash-Hash `ad026456...`. G1 blieb `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb`; D2 blieb `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` und der Adapter meldet `d2_gb_mesh_bytegleich: true`.

Der größte D1-Höhenunterschied zur Quelle ist 2,815859 m bei `148.0|29.5` (Quelle 6,967429 m; Mesh 4,151570 m). Bei `144.5|21.5` liegen Quelle und Mesh bei 12,865277 m beziehungsweise 12,863120 m, also 0,002157 m auseinander. Damit gibt es dort keinen Mehr-Meter-Absturz.

Die direkten, unveränderten Quell-Prüfer liefen auf `relief_daten.json.gz`: `pruefe_regeln` 570, R8 48 (Stufe 9, Gitter 10, Quer 5, Wegende 24), R9 334 (Delle 25, Sägezahn 34, Wellen 275). Der in der Aufgabenbasis genannte direkte Ausgangswert 596 ließ sich in diesem Worktree wie bereits im p3d8-Bericht nicht reproduzieren. Für Änderungen am neuen Mesh sind daher zusätzlich die Adapter-Ergebnisse maßgeblich: `pruefe_regeln` 571, R8 39, R9 337.

## Adapter-Prüfergebnisse nach Regel und Kachel

Die Tabellen zeigen Gesamtzahlen und die Zähler für D1, G1 und D2 jeweils in der Reihenfolge **p3d6 / p3d8 / p3d9**. Damit sind sowohl die p3d6-Regressionsbasis als auch die direkte p3d8-Vergleichsbasis sichtbar.

### `pruefe_regeln` (Adapter)

| Regel | Gesamt p3d6 / p3d8 / p3d9 | D1 p3d6 / p3d8 / p3d9 | G1 p3d6 / p3d8 / p3d9 | D2 p3d6 / p3d8 / p3d9 |
|---|---:|---:|---:|---:|
| G2_spitze_oben | 3 / 3 / 3 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| G2_spitze_oben_fein | 8 / 8 / 8 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| G3_spitze_unten | 3 / 3 / 3 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| G3_spitze_unten_fein | 2 / 2 / 2 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| G5_beule_klippe | 67 / 67 / 67 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| G6_facette | 216 / 216 / 216 | 0 / 0 / 0 | 3 / 3 / 3 | 0 / 0 / 0 |
| G7_wand_glatte_flaeche | 1 / 1 / 1 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| G7b_wandkontur_feld | 25 / 25 / 25 | 1 / 1 / 1 | 0 / 0 / 0 | 0 / 0 / 0 |
| G7b_wandkontur_kantenschaerfe | 1 / 1 / 1 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| G7b_wandkontur_rauheit | 1 / 1 / 1 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| G8_fluss_nicht_bis_rand | 1 / 1 / 1 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| R1_blind | 24 / 24 / 24 | 2 / 2 / 2 | 1 / 1 / 1 | 0 / 0 / 0 |
| R2_getrennt | 15 / 15 / 15 | 1 / 1 / 1 | 0 / 0 / 0 | 1 / 1 / 1 |
| R3_laengs_m | 39 / 43 / 43 | 10 / 14 / 14 | 1 / 1 / 1 | 0 / 0 / 0 |
| R3_quer_pct | 19 / 21 / 22 | 7 / 9 / 10 | 0 / 0 / 0 | 0 / 0 / 0 |
| R3_woelb_m | 19 / 20 / 20 | 7 / 8 / 8 | 0 / 0 / 0 | 0 / 0 / 0 |
| R5_loch | 17 / 17 / 17 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| R6_wasser_schnee | 4 / 4 / 4 | 0 / 0 / 0 | 3 / 3 / 3 | 0 / 0 / 0 |
| T1_fleckrand | 94 / 94 / 94 | 0 / 0 / 0 | 3 / 3 / 3 | 7 / 7 / 7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 / 1 / 1 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 / 1 / 1 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 / 1 / 1 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 / 1 / 1 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
Gesamt: **563 / 570 / 571**. Gegen p3d6 steigt kein einzelner Regelzähler um mehr als 4; R3 längs D1 ist +4, R3 quer D1 +3 und R3 Wölbung D1 +1. D2 erhält bei keiner `pruefe_regeln`-Regel einen neuen Treffer.

### R8 / R8a

| Regel | Gesamt p3d6 / p3d8 / p3d9 | D1 p3d6 / p3d8 / p3d9 | G1 p3d6 / p3d8 / p3d9 | D2 p3d6 / p3d8 / p3d9 |
|---|---:|---:|---:|---:|
| R8_gitter | 8 / 8 / 8 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| R8_quer | 4 / 4 / 4 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| R8_stufe | 7 / 7 / 7 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| R8a_wegende | 20 / 20 / 20 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
Gesamt R8: **39 / 39 / 39**. D1, G1 und D2 bleiben für alle vier R8/R8a-Regeln trefferfrei.

### R8b / R9

| Regel | Gesamt p3d6 / p3d8 / p3d9 | D1 p3d6 / p3d8 / p3d9 | G1 p3d6 / p3d8 / p3d9 | D2 p3d6 / p3d8 / p3d9 |
|---|---:|---:|---:|---:|
| R8b_delle | 22 / 22 / 22 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| R9_saegezahn | 34 / 34 / 34 | 1 / 1 / 1 | 1 / 1 / 1 | 0 / 0 / 0 |
| R9w_wellen | 280 / 280 / 281 | 21 / 21 / 22 | 12 / 12 / 12 | 0 / 0 / 0 |
Gesamt R9: **336 / 336 / 337**. D2 bleibt ohne R8b-/R9-Treffer. D1-R9-Sägezahn bleibt bei 1 Treffer und Testwert 47 (p3d6: 46; p3d8: 47), G1-G6 bleibt 3, D1-G7b bleibt 1 und G1-R9w bleibt 12. D1-R9w steigt von 21 auf 22; der zusätzliche Treffer liegt bei `149.8|32.5` (Wert 0,25).

### Kreuzung und Wegende

| Messstelle | p3d6 | p3d8 | p3d9 |
|---|---:|---:|---:|
| D1 `152.5\|28.5` R8-Stufe | 0,116 m | 0,043 m | 0,177 m |
| D1 `152.5\|28.5` R8-Gitter | 0,000 m | 0,000 m | 0,032 m |
| D1 `156.5\|37.5` R8a-Stufe | 0,188 m | 0,135 m | 0,135 m |
| D1 `156.5\|37.5` R8-Gitter | 0,089 m | 0,090 m | 0,090 m |
| D1 `156.5\|37.5` Querneigung | 1,4 % | 1,4 % | 1,4 % |

Die Kreuzungsstufe unterschreitet 0,20 m, ist aber um 0,061 m schlechter als p3d6 und um 0,134 m schlechter als p3d8. Das Ziel „nicht schlechter als p3d6“ ist nicht erreicht. Am Wegende bleibt die p3d8-Verbesserung erhalten.

### R3-Profile rampe_2 und rampe_11

Die Profile folgen den unveränderten `rampenwege` aus `relief_daten.json.gz`, in 0,25-Schritten wie im R3-Prüfer. `s` ist relativ zum Profilpunkt am D1-Schnitt; `lr_p3d9 = h_p3d9 - gaussian_filter1d(h_p3d9, sigma=8)` wurde auf dem vollständigen Rampenprofil gerechnet (Randmodus `nearest`), nicht nur auf den 24 Tabellenpunkten. Höhen sind Meter.

**rampe_2**

| s | x\|z | h Quelle | h p3d6 | h p3d8 | h p3d9 | lr p3d9 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -12 | 140.66\|29.90 | 9,402 | 9,402 | 9,402 | 9,402 | +0,085 |
| -10 | 142.64\|29.65 | 8,718 | 8,718 | 8,679 | 8,679 | +0,252 |
| -8 | 144.63\|29.41 | 8,076 | 8,076 | 7,416 | 7,416 | +0,304 |
| -6 | 146.61\|29.17 | 7,355 | 7,189 | 5,130 | 5,207 | -0,380 |
| -4 | 148.60\|28.93 | 6,702 | 5,061 | 4,012 | 4,037 | -0,469 |
| -2 | 150.58\|28.68 | 6,151 | 5,030 | 4,012 | 4,012 | -0,082 |
| 0 | 152.57\|28.44 | 5,519 | 5,030 | 4,012 | 4,009 | -0,006 |
| +2 | 154.55\|28.20 | 5,262 | 5,030 | 4,012 | 4,006 | -0,001 |
| +4 | 156.54\|27.96 | 4,964 | 5,024 | 4,012 | 3,949 | -0,071 |
| +6 | 158.52\|27.71 | 4,542 | 4,546 | 4,145 | 4,141 | +0,133 |
| +8 | 160.51\|27.47 | 4,042 | 4,042 | 3,981 | 3,981 | +0,148 |
| +10 | 162.49\|27.23 | 3,491 | 3,491 | 3,489 | 3,490 | +0,053 |
| +12 | 164.48\|26.99 | 2,915 | 2,915 | 2,915 | 2,915 | +0,001 |

**rampe_11**

| s | x\|z | h Quelle | h p3d6 | h p3d8 | h p3d9 | lr p3d9 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| -12 | 156.74\|18.24 | 7,302 | 7,302 | 7,296 | 7,296 | -0,017 |
| -10 | 157.11\|19.72 | 6,820 | 6,820 | 6,794 | 6,794 | +0,174 |
| -8 | 156.16\|21.48 | 6,198 | 6,198 | 5,854 | 5,854 | +0,091 |
| -6 | 155.22\|23.24 | 5,595 | 5,558 | 4,610 | 4,657 | -0,235 |
| -4 | 154.27\|25.01 | 5,066 | 5,032 | 4,012 | 4,096 | -0,214 |
| -2 | 153.34\|26.77 | 4,700 | 5,030 | 4,012 | 4,016 | -0,057 |
| 0 | 152.40\|28.54 | 5,604 | 5,030 | 4,012 | 4,016 | +0,011 |
| +2 | 151.45\|30.30 | 3,383 | 5,030 | 4,012 | 3,995 | +0,080 |
| +4 | 150.51\|32.06 | 2,739 | 4,894 | 4,009 | 3,889 | +0,312 |
| +6 | 151.03\|33.51 | 2,114 | 3,151 | 3,462 | 3,191 | +0,386 |
| +8 | 152.65\|34.69 | 1,468 | 1,507 | 1,552 | 1,552 | -0,289 |
| +10 | 154.26\|35.87 | 0,987 | 0,987 | 0,988 | 0,988 | -0,134 |
| +12 | 155.88\|37.05 | 0,614 | 0,614 | 0,614 | 0,614 | -0,116 |

Im 18-m-Fenster sinkt der größte Betrag von `lr` bei rampe_2 von p3d8 0,725 m auf p3d9 **0,643 m** (s=-5, `147.604|29.050`). Bei rampe_11 sinkt er von 0,579 m auf **0,402 m** (s=+5,75, `150.831|33.361`). Das verbessert die Profilform-Messung, beseitigt aber nicht die Regelverletzungen: R3 längs D1 bleibt bei 14 Treffern.

Die vier in p3d8 neu auffälligen 4-m-Abschnitte bleiben über der 0,08-m-Grenze:

| Rampenabschnitt ab | p3d8 | p3d9 | Ergebnis |
|---|---:|---:|---|
| rampe_2 `138.4\|30.2` | 0,200 | 0,198 | weiter >0,08 |
| rampe_2 `158.3\|27.7` | 0,165 | 0,174 | weiter >0,08; +0,009 m |
| rampe_11 `157.5\|19.1` | 0,180 | 0,177 | weiter >0,08 |
| rampe_11 `153.7\|26.1` | 0,086 | 0,100 | weiter >0,08; +0,014 m |

**LP-Soll gegen angewandtes Mesh** an den gleichen ±6-Stellen des R3-Profils. Der Wert „LP“ ist der auf den R3-Rampenpunkt projizierte gelöste 1D-Profilwert; das Mesh enthält zusätzlich die räumliche Fade-Mischung.

| Rampe / s | x\|z | LP p3d9 | Mesh p3d9 | Mesh p3d6 | Mesh p3d8 |
|---|---:|---:|---:|---:|---:|---:|
| rampe_2 / -6 | 146.61\|29.17 | 4,807 | 5,207 | 7,189 | 5,130 |
| rampe_2 / +6 | 158.52\|27.71 | 3,877 | 4,141 | 4,546 | 4,145 |
| rampe_11 / -6 | 155.22\|23.24 | 4,505 | 4,657 | 5,558 | 4,610 |
| rampe_11 / +6 | 151.03\|33.51 | 3,036 | 3,191 | 3,151 | 3,462 |

Der p3d9-Fade lässt die 1D-Sollhöhe dort nicht unverändert in die Fläche durch; besonders bei rampe_2 s=-6 liegt das Mesh 0,401 m über dem projizierten LP-Ziel. Die resultierende Höhe liegt nahe an p3d8, nicht am p3d6-Ausgangsprofil. Das erklärt, warum die berechneten LP-Übergänge nicht genügen, um die R3-Zähler auf p3d6 zurückzuführen.

## Bilder

Mit demselben Satz von fünf Clay-Kameras wie p3d6 gerendert; `kameras.json` ist bytegleich zu `bilder_p3d6/kameras.json`. Dazu kam die geforderte seitliche Streiflichtkamera entlang rampe_11. Die Vorher-Serien liegen in `bilder_p3d9/vorher_p3d8/` und `bilder_p3d9/stichprobe_p3d6/`, die p3d9-Aufnahmen in `bilder_p3d9/nachher/`.

| Kachel / Kamera | p3d6: Facetten / Zähne / Normalsprünge / Inseln | p3d8: Facetten / Zähne / Normalsprünge / Inseln | p3d9: Facetten / Zähne / Normalsprünge / Inseln |
|---|---:|---:|---:|
| D1 / kreuzung | 351 / 51 / 802 / 117 | 317 / 36 / 484 / 57 | 362 / 32 / 520 / 74 |
| D1 / wandfuss_140_35 | 535 / 1258 / 3322 / 333 | 515 / 1255 / 3503 / 364 | 513 / 1264 / 3481 / 357 |
| D1 / wegende | 807 / 887 / 2137 / 212 | 825 / 866 / 2308 / 220 | 841 / 871 / 2340 / 217 |
| D2 / draufsicht | 0 / 313 / 2275 / 9 | 0 / 313 / 2275 / 9 | 0 / 313 / 2275 / 9 |
| G1 / wandfuss | 530 / 911 / 3393 / 182 | 530 / 911 / 3393 / 182 | 530 / 911 / 3393 / 182 |

D1-Kreuzung: p3d9 hat weniger Kantenzähne als p3d6 und p3d8 (32), aber 362 Facetten gegenüber 351 bei p3d6 und 317 bei p3d8; die geforderte Clay-Facettenzahl ≤351 wird verfehlt. Die Normalensprünge und Inseln sind ebenfalls höher als p3d8. Die Nahaufnahme zeigt eine weichere Kreuzungsfläche ohne p3d7-artigen Grat, aber die Fläche ist tiefer als p3d6.

D1-Wandfuß und Wegende wurden visuell mit p3d6 und p3d8 verglichen. Die Silhouette bleibt ähnlich; die Metriken verschieben sich leicht. G1-Wandfuß und D2-Draufsicht sind über alle drei Serien pixelgleich: G1 SHA-256 `6a391991ecdee07c10383399b917bcc04b56efe8dfb85ae311b1510393cc6781`, D2 SHA-256 `e8db06e608ee2bb6c833c7ca4112a487b5671c5fc2141798c4efd2321350158a`. Die D1-Kreuzung hat SHA-256 `7534abb1e69acef403aeaa3d03c0c15277db8ff59e2d5c62e79b3110a42ebc74`. Das zusätzliche Streiflicht p3d9 hat SHA-256 `6490868dea59fed43b66cead18d12a9855df1772aaa9f701bd56143ba08c737c`; p3d8 hat `d76e8bc43eb2fa127d19831e03ae08c72a54de6e8ccc308e1b01bb8854317805`. Die Streiflichtansichten zeigen eine ähnliche Rampensilhouette.

## Deltas

`neu/delta.py` wurde für VAR0→p3d9, p3d6→p3d9 und p3d8→p3d9 ausgeführt. Positive Gate-Zähler und positive Clay-Proxys zählen jeweils als Anstieg; die vollen Zeilen und JSON-Daten liegen neben den Bildern:

- [VAR0 → p3d9](bilder_p3d9/delta_var0_p3d9.md): **22 Anstiege** (6 Gate-Zeilen, 16 Bild-Proxys); Ziel `<19` verfehlt.
- [p3d6 → p3d9](bilder_p3d9/delta_p3d6_p3d9.md): **17 Anstiege** (4 Gate-Zeilen, 13 Bild-Proxys); Ziel 0 Gate-Anstiege verfehlt.
- [p3d8 → p3d9](bilder_p3d9/delta_p3d8_p3d9.md): **14 Anstiege** (2 Gate-Zeilen, 12 Bild-Proxys). Die Gate-Anstiege sind R3 quer D1 +1 und R9w D1 +1; damit gibt es neben dem erhofften R3-Rückgang neue Gate-Anstiege.

Der VAR0-Vergleich enthält positive D2-Bildproxys, obwohl D2 zwischen p3d6, p3d8 und p3d9 pixelidentisch ist. Der VAR0-Kontrollbildsatz ist daher kein pixelneutraler Geometrievergleich; die Deltas werden trotzdem vollständig ausgewiesen.

## Tests, Annahmen und offene Punkte

- `~/.local/bin/pytest -q neu/tests`: **26 bestanden, 5 fehlgeschlagen**. Dieselben fünf Fehlschläge wie in p3d6/p3d8: globales R8a (20), D1-Sägezahn (47), D1-Wandkantenschärfe (2,24 < 3,00), F1-Wegende (0,17 > 0,10; C1 ohne Messwerte) und Schatten-HF (0,307 > 0,25).
- Die zwei neuen Profileingriffe sind lokal über `RELIEF_KREUZUNG_VAR=6|7` schaltbar; Variante 5 bleibt als bestehende p3d8-Referenz auswählbar. Der Fade bleibt eine Höhenmischung, kein harter Schreibvorgang.
- Varianten mit angehobener LP-Ebene (4,65 m bzw. 5,03 m) wurden verworfen: die D1-Kreuzungsstufe stieg auf 0,290 m bzw. 0,343 m und überschritt damit 0,20 m. Auch der rampengeführte Planar-Fade der Variante 7 erreicht zwar 0,004 m Gitterabweichung, aber 0,195 m Stufe und senkt R3 nicht.
- Bildzahlen sind deterministische Sichtindikatoren; sie ersetzen weder die Höhenwerte noch die Gate-Prüfer. Die p3d8-/p3d6-Bilder und Messwerte wurden als Referenzen übernommen; die p3d9-Serie wurde neu mit denselben fünf Kameras plus Streiflicht gerendert und visuell geprüft.
- **Nicht erreicht:** R3 längs D1 ≤6 (oder wenigstens ≤10), R3 quer D1 ≤7, R3 Wölbung D1 ≤7, Kreuzungsstufe ≤0,116 m, D1-Kreuzungsfacetten ≤351, kein R9w-Anstieg, 0 Gate-Anstiege p3d6→p3d9 und VAR0→p3d9 `<19` Anstiege. Offen bleibt, wie die Schulter vom LP-Profil in die p3d6-Fläche übergeht, ohne die Kreuzungsebene oder R9w zu verschlechtern.

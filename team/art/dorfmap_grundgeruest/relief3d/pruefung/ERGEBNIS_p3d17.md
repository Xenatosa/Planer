# Ergebnis p3d17

**Status: Variante 22 gebaut; direkter Rastertransfer gelingt, Gesamtziel verfehlt.**
Stand: 10.11.2026 · Branch `art/dorfmap-p3d17` · Basis `origin/art/dorfmap-p3d16` @ `3021164` · Kosten **0 EUR**.

Bau im Ordner `relief3d`: `RELIEF_NEU=1 python3 gen_relief.py && RELIEF_NEU=1 python3 baue_html.py`.

## Änderung und Transferdiagnose

V21 übernimmt die gemeinsame LP/MILP-Fläche direkt auf das D1-Meshraster. Die Rasterstützen im Wegband (Halbbreite 1,81 m) und im unveränderten Ebenenkern (Radius 2,00 m) treffen die gemeinsame Lösung hart; nur außerhalb der Stützen läuft sie weich ins Gelände aus. Kein harter Umschalter, keine Dämpfung.

Der erste V21-Lauf zeigte eine messbare Restlücke am wirklichen, ungerundeten R8-Zentrum `152.549857|28.489545`, das knapp außerhalb des nominalen 4-Karten-Einheiten-Gate-Fußabdrucks lag: R8 maß dort Stufe `0,202 m`, Gitter `0,151 m`, Quergefälle `3,8 %`. V22 erweitert daher die direkte Stützung auf den exakt gemessenen Gate-Fußabdruck und lässt sie über `9,5 m` weich auslaufen. Der Kernradius bleibt `2,00 m`. `RELIEF_KREUZUNG_VAR=22` ist Standard; V21 bleibt schaltbar. Es wurde keine dritte Variante gebaut.

V22 ist optimal (HiGHS Gap 0) auf dem tatsächlichen 0,5-Karten-Einheiten-Meshraster mit bilinearer Prüfauswertung im 0,25-Karten-Einheiten-Raster. Die LP-Untergrenze für den lokalen Nachbarschritt ist `0,080423851 m` (Ziel `≤0,116 m`). Das gebaute Mesh liegt an allen 359 Achsstützen maximal `0,000474586 m` von der gemeinsamen Lösung entfernt; keine Stütze überschreitet `±0,02 m`.

Der Transferverlust aus p3d16 ist damit geschlossen. Die R3-Fehler sind bereits in der gemeinsamen Lösung sichtbar: Mit der offiziellen Prüferformel gezählt, ergeben Lösungsraster und Mesh dieselben D1-Zähler `6/17/19` (längs/quer/Wölbung). Die internen Modellzähler `6/5/4` bilden die Prüferformel für Querung und Wölbung nicht ausreichend ab. Auf `rampe_11`, Abschnitt `s=43,20–47,70 m`, beträgt das Quergefälle im Lösungsraster `20,000000 %`, im Mesh `20,002199 %`; die Vorgabe „kein Wert >20 %“ wird um `0,002199 Prozentpunkte` überschritten.

### D1-Hauptkreuzung `152.5|28.5`

| Messung | gemeinsame Lösung / Mesh | Ziel | Bewertung |
|---|---:|---:|---|
| R8-Stufe am tatsächlichen Zentrum | `0,080424 m` / Checker `0,080 m` | `≤0,116 m` | erreicht |
| R8-Gitter | `0,020000000000119 m` / Checker `0,020 m` | `≤0,020 m` | numerisch an Grenze |
| R8-Quergefälle | `3,000000000000013 %`; kein R8-Quer-Treffer | `≤3 %` | numerisch an Grenze; kein Checker-Treffer |

Die gemeldete Checker-Koordinate `152.5|28.5` ist gerundet; die Rechnung nutzt `152.549857|28.489545`. Die restlichen D1-Kreuzungen und Wegenden bleiben auffällig.

## Mesh- und Quellprüfungen

| Prüfung | Ergebnis | Bewertung |
|---|---:|---|
| LOD1-Dreiecke gesamt | `134.316` | unter `1,3 Mio.` |
| D1-Höhenhash | `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29` | neu; nicht in Ausschlussliste |
| G1-Höhenhash | `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` | unverändert |
| D2-Höhenhash | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` | unverändert; Adapter meldet bytegleich |
| maximale D1-Höhenänderung | `3,013915 m` | `test_gelaende_mesh`-Grenze `4,0 m` eingehalten |
| Klippenpunkt `140|35` | `GB = 7,88403654 m` | Soll `7,8840365 m` |
| Vektor | SHA-256 `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e` | unverändert |
| Zellquellwerte | `zellen_quell_diff = 0` | unverändert |
| t42u | Summe `0`; alle Abweichungsfelder `0` | bestanden |
| xvfb-Lochscan | 9 Meshes, 88.728 Geländedreiecke, 0 offene Innenkanten, 0 Punkte | bestanden |
| `pytest -q neu/tests/test_gelaende_mesh.py` | 4 bestanden | bestanden |
| `pytest -q neu/tests` | 26 bestanden, 5 fehlgeschlagen | Ziel `≥26/5` erreicht; Suite nicht grün |

Die fünf Suite-Fehler: 23 R8a-Wegenden statt 0; D1-Sägezahnwert 116 statt 0; D1-Wandkantenschärfe 2,24 statt mindestens 3,00; F1-Wegende 0,17 m statt höchstens 0,10 m und keine C1-Endpunktmessung; Schatten-Hochfrequenz 0,307 statt höchstens 0,25. Prüfer und Tests blieben unverändert.

## `pruefe_regeln`: Zahlen je Regel

Für `9d3f8fc` ist nur die Gesamtsumme `596` überliefert, nicht die vollständige Einzelregelverteilung. Die Einzelregeltabelle vergleicht deshalb p3d16 → p3d17; Spalten D1/G1/D2 zeigen jeweils vorher → nachher.

| Regel | p3d16 | p3d17 | Δ | D1 | G1 | D2 |
|---|---:|---:|---:|---:|---:|---:|
| G11_baum_an_wand | 2 | 0 | -2 | 2→0 | 0→0 | 0→0 |
| G2_spitze_oben | 3 | 3 | +0 | 0→0 | 0→0 | 0→0 |
| G2_spitze_oben_fein | 8 | 8 | +0 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten | 3 | 4 | +1 | 0→1 | 0→0 | 0→0 |
| G3_spitze_unten_fein | 2 | 2 | +0 | 0→0 | 0→0 | 0→0 |
| G5_beule_klippe | 67 | 69 | +2 | 0→2 | 0→0 | 0→0 |
| G6_facette | 221 | 219 | -2 | 5→3 | 3→3 | 0→0 |
| G7_wand_glatte_flaeche | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_feld | 25 | 25 | +0 | 1→1 | 0→0 | 0→0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_rauheit | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| R1_blind | 24 | 24 | +0 | 2→2 | 1→1 | 0→0 |
| R2_getrennt | 15 | 15 | +0 | 1→1 | 0→0 | 1→1 |
| R3_laengs_m | 46 | 35 | -11 | 17→6 | 1→1 | 0→0 |
| R3_quer_pct | 34 | 29 | -5 | 22→17 | 0→0 | 0→0 |
| R3_woelb_m | 27 | 31 | +4 | 15→19 | 0→0 | 0→0 |
| R4_rand | 0 | 1 | +1 | 0→1 | 0→0 | 0→0 |
| R5_loch | 17 | 25 | +8 | 0→8 | 0→0 | 0→0 |
| R6_wasser_schnee | 4 | 4 | +0 | 0→0 | 3→3 | 0→0 |
| T1_fleckrand | 94 | 94 | +0 | 0→0 | 3→3 | 7→7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |

Gesamtsummen: `9d3f8fc 596` → p3d16 `600` → p3d17 `596`. D1/G1/D2-Summen p3d16 → p3d17: `65→61`, `11→11`, `8→8`. `R5_loch` steigt p3d16→17 `17→25` (`+8`) und überschreitet damit die +5-Regelgrenze. Die acht D2-Regeltreffer sind identisch; kein D2-Treffer kam hinzu.

### R8

| Regel | 9d3f8fc | p3d16 | p3d17 | Δ ggü. Ausgang | D1 p3d16→17 | G1 | D2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| R8_stufe | 9 | 7 | 9 | +0 | 0→2 | 0→0 | 0→0 |
| R8_gitter | 10 | 11 | 10 | +0 | 3→2 | 0→0 | 0→0 |
| R8_quer | 5 | 5 | 4 | -1 | 1→0 | 0→0 | 0→0 |
| R8a_wegende | 24 | 23 | 23 | -1 | 3→3 | 0→0 | 0→0 |

R8 gesamt `48→46→46`. D1 bleibt bei 7 Treffern (p3d16: Stufe/Gitter/Quer/Wegende `0/3/1/3`; p3d17: `2/2/0/3`). G1 und D2 bleiben bei 0.

### R9

| Regel | 9d3f8fc | p3d16 | p3d17 | Δ ggü. Ausgang | D1 p3d16→17 | G1 | D2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| R8b_delle | 25 | 22 | 23 | -2 | 0→1 | 0→0 | 0→0 |
| R9_saegezahn | 34 | 34 | 34 | +0 | 1→1 | 1→1 | 0→0 |
| R9w_wellen | 275 | 291 | 287 | +12 | 31→27 | 12→12 | 0→0 |

R9 gesamt `334→347→344`. Gegen den Ausgang steigt `R9w_wellen` `275→287` um `12` und verletzt die +5-Grenze. Gegen p3d16 sinkt die R9-Summe um 3.

## D1-R8/R8a-Feinpunkte

| Regel | Weg | Station | Zentrum | Feinpunktpaar | Sollgrenze | Meshwert | Höhen / Transferterm |
|---|---|---|---|---|---:|---:|---|
| R8_stufe | rampe_2 | 0.00 (Start) | 126.510000|31.620000 | 130.250|32.500 → 130.250|32.750 | 0.20 m | 0.208414 m | 12.30418 → 12.09577 · joint_dirichlet_raster; volles Wegband |
| R8_stufe | rampe_11 | 0.00 (Start) | 148.500000|2.500000 | 147.000|4.000 → 147.000|4.250 | 0.20 m | 0.651355 m | 12.76606 → 12.11471 · joint_dirichlet_raster; volles Wegband |
| R8_gitter | rampe_11 | 0.00 (Start) | 148.500000|2.500000 | 147.500|2.500 → 147.500|3.500 | 0.15 m | 0.596448 m | 12.86228 → 12.16072 · joint_dirichlet_raster; volles Wegband |
| R8_gitter | rampe_11 | 57.00 (Ende) | 156.484516|37.488831 | 154.750|36.500 → 155.750|36.500 | 0.15 m | 0.263076 m | 1.03936 → 0.67528 · joint_dirichlet_raster; volles Wegband |
| R8a_wegende | rampe_2 | 0.00 (Start) | 126.510000|31.620000 | 127.500|33.750 → 127.750|33.750 | 0.10 m | 0.118947 m | 12.24426 → 12.12531 · rampenenden_lokaler_auslauf_ge4m_weich; weicher Uebergang ausserhalb 1.81-m-Band |
| R8a_wegende | rampe_11 | 0.00 (Start) | 148.500000|2.500000 | 150.500|3.750 → 150.500|4.000 | 0.10 m | 0.178342 m | 12.72958 → 12.55123 · rampenenden_lokaler_auslauf_ge4m_weich; weicher Uebergang ausserhalb 1.81-m-Band |
| R8a_wegende | rampe_11 | 57.00 (Ende) | 156.484516|37.488831 | 157.500|35.500 → 157.750|35.500 | 0.10 m | 0.169395 m | 0.86382 → 0.69442 · rampenenden_lokaler_auslauf_ge4m_weich; weicher Uebergang ausserhalb 1.81-m-Band |

Damit ist das Ziel R8/R8a D1=0 verfehlt. Am Wegende `156.5|37.5` misst R8-Stufe `0,131 m` (p3d11: `0,054 m`) und R8a `0,169 m` (p3d11: kein Treffer). Die Stufen- und Gittertreffer im Wegband liegen direkt in der gemeinsamen Rasterlösung; sie entstehen nicht durch einen nachträglichen Transferverlust. R8a misst teils außerhalb des 1,81-m-Stützbandes, wo der lokale Wegend-Auslauf weich zurückführt.

## D1-R3-Profiltabelle je Treffer

Der unveränderte Prüfer wertet Abschnitte von 4,8 m aus (16 Schritte à 0,25 Karten-Einheiten bei 1,2 m je Einheit). `Gate-Schwelle` ist die Prüferschelle 0,08 m längs/Wölbung bzw. 3,5 % quer. LP- und Meshwerte verwenden dieselbe offizielle Prüferformel auf dem Lösungsraster bzw. ausgegebenen Mesh. `H LP→Mesh` und `ΔH` sind die Höhen am Abschnittsanfang. Die lateralen Querstützen liegen bei ±1,5 Karten-Einheiten (1,8 m) innerhalb des 1,81-m-Bands; dort ist die Transferabdeckung 1.

| Regel | Weg | Station [m] | Feinpunkt x|z | Gate-Schwelle | LP-Prüfung | Mesh-Prüfung | H LP→Mesh [m] | ΔH [m] | Transferterm |
|---|---|---:|---|---:|---:|---:|---:|---:|---|
| R3_woelb_m | rampe_2 | 0.00–4.50 | 126.51|31.62 | 0.08 m | 0.080000 | 0.080259 | 12.46981→12.46986 | +0.000046 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_2 | 4.80–9.30 | 130.48|31.14 | 0.08 m | 0.080000 | 0.080607 | 12.09784→12.09784 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_2 | 9.60–14.10 | 134.45|30.65 | 0.08 m | 0.080000 | 0.080107 | 11.22443→11.22443 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_2 | 14.40–18.90 | 138.42|30.17 | 3.5% | 3.500000 | 3.516488 | 9.75491→9.75491 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_2 | 19.20–23.70 | 142.39|29.68 | 3.5% | 3.500000 | 3.539224 | 7.65326→7.65326 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_2 | 19.20–23.70 | 142.39|29.68 | 0.08 m | 0.080000 | 0.082092 | 7.65326→7.65326 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_laengs_m | rampe_2 | 24.00–28.50 | 146.36|29.20 | 0.08 m | 0.184493 | 0.184493 | 5.64778→5.64778 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_2 | 24.00–28.50 | 146.36|29.20 | 3.5% | 20.000000 | 20.000066 | 5.64778→5.64778 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_2 | 24.00–28.50 | 146.36|29.20 | 0.08 m | 0.207866 | 0.207865 | 5.64778→5.64778 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_laengs_m | rampe_2 | 28.80–33.30 | 150.33|28.71 | 0.08 m | 0.225532 | 0.225532 | 4.21555→4.21555 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_2 | 28.80–33.30 | 150.33|28.71 | 3.5% | 18.999765 | 18.999769 | 4.21555→4.21555 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_2 | 28.80–33.30 | 150.33|28.71 | 0.08 m | 0.157038 | 0.157038 | 4.21555→4.21555 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_2 | 33.60–38.10 | 154.30|28.23 | 3.5% | 3.500000 | 3.500003 | 4.04543→4.04543 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_2 | 33.60–38.10 | 154.30|28.23 | 0.08 m | 0.080000 | 0.080000 | 4.04543→4.04543 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_2 | 38.40–42.90 | 158.27|27.74 | 0.08 m | 0.080000 | 0.080508 | 3.45498→3.45498 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_2 | 43.20–47.70 | 162.24|27.26 | 0.08 m | 0.080000 | 0.080797 | 3.16825→3.16825 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_laengs_m | rampe_11 | 0.00–4.50 | 148.50|2.50 | 0.08 m | 0.338207 | 0.338207 | 12.90509→12.90509 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 0.00–4.50 | 148.50|2.50 | 3.5% | 3.500000 | 3.813388 | 12.90509→12.90509 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 0.00–4.50 | 148.50|2.50 | 0.08 m | 0.080000 | 0.080587 | 12.90509→12.90509 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 4.80–9.30 | 146.62|6.03 | 3.5% | 3.500000 | 3.510282 | 11.57104→11.57104 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 4.80–9.30 | 146.62|6.03 | 0.08 m | 0.080000 | 0.080866 | 11.57104→11.57104 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 9.60–14.10 | 144.83|9.54 | 3.5% | 3.500000 | 3.531276 | 10.96750→10.96750 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 9.60–14.10 | 144.83|9.54 | 0.08 m | 0.080000 | 0.081077 | 10.96750→10.96750 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 14.40–18.90 | 148.05|11.90 | 3.5% | 3.500000 | 3.554683 | 10.02310→10.02310 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 14.40–18.90 | 148.05|11.90 | 0.08 m | 0.080000 | 0.081126 | 10.02310→10.02310 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 19.20–23.70 | 151.29|14.25 | 3.5% | 3.500000 | 3.521712 | 8.43487→8.43487 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 19.20–23.70 | 151.29|14.25 | 0.08 m | 0.080000 | 0.082290 | 8.43487→8.43487 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 24.00–28.50 | 154.52|16.61 | 3.5% | 3.500000 | 3.736312 | 7.02841→7.02841 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 24.00–28.50 | 154.52|16.61 | 0.08 m | 0.080000 | 0.082637 | 7.02841→7.02841 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 28.80–33.30 | 157.46|19.05 | 3.5% | 3.500000 | 3.509075 | 6.27371→6.27371 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 28.80–33.30 | 157.46|19.05 | 0.08 m | 0.080000 | 0.080461 | 6.27371→6.27371 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 33.60–38.10 | 155.57|22.58 | 3.5% | 20.000000 | 19.999472 | 5.51032→5.51032 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 33.60–38.10 | 155.57|22.58 | 0.08 m | 0.080000 | 0.080105 | 5.51032→5.51032 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_laengs_m | rampe_11 | 38.40–42.90 | 153.69|26.11 | 0.08 m | 0.210688 | 0.210688 | 4.31531→4.31531 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 38.40–42.90 | 153.69|26.11 | 3.5% | 15.755014 | 15.755016 | 4.31531→4.31531 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_laengs_m | rampe_11 | 43.20–47.70 | 151.80|29.64 | 0.08 m | 0.290793 | 0.290793 | 4.04939→4.04939 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 43.20–47.70 | 151.80|29.64 | 3.5% | 20.000000 | 20.002199 | 4.04939→4.04939 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 43.20–47.70 | 151.80|29.64 | 0.08 m | 0.508958 | 0.508925 | 4.04939→4.04939 | -0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 48.00–52.50 | 150.43|33.07 | 3.5% | 3.500000 | 3.540130 | 2.59112→2.59112 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_woelb_m | rampe_11 | 48.00–52.50 | 150.43|33.07 | 0.08 m | 1.020288 | 1.019686 | 2.59112→2.59112 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_laengs_m | rampe_11 | 52.80–57.00 | 153.66|35.42 | 0.08 m | 0.199548 | 0.199548 | 1.39269→1.39269 | +0.000000 | joint_dirichlet_raster (w≈1) |
| R3_quer_pct | rampe_11 | 52.80–57.00 | 153.66|35.42 | 3.5% | 3.500000 | 3.767005 | 1.39269→1.39269 | +0.000000 | joint_dirichlet_raster (w≈1) |

Die D1-R3-Zähler sind längs `6` (Ziel ≤6), quer `17` (Ziel ≤7) und Wölbung `19` (Ziel ≤7). Die beiden letzteren Ziele werden verfehlt. Das maximale Quergefälle beträgt `20,002199 %` am oben genannten rampe_11-Abschnitt. Am Startpunkt der 42 beanstandeten Abschnitte beträgt die größte Höhenabweichung Mesh−Lösung `0,0000461 m`; der globale Achsfehler über alle Stützen beträgt `0,0004746 m`. Die Prüfmetrik ist somit schon im gemeinsamen Lösungsfeld vorhanden.

## R8/R9 je Kachel und Delta-Vergleiche

Aktuell: R8 D1/G1/D2=`7/0/0`; R9=`29/13/0`. Gegen p3d8 ist „D1 G6/G11/R8b/R9w/Sägezahn nicht schlechter“ verfehlt: G6 `0→3`, R8b `0→1`, R9w `21→27`; G11 bleibt 0 und Sägezahn bleibt 1.

`neu/delta.py` zählt positive Regel/Kachelzeilen und positive Clay-Bildindikatoren separat. Kein verlangter Vergleich hat null Gate-Anstiege.

| Vergleich | positive Gate-Zeilen | positive Bildindikatoren | zusammen |
|---|---:|---:|---:|
| VAR0 → p3d17 | 15 | 23 | 38 |
| p3d6 → p3d17 | 13 | 16 | 29 |
| p3d8 → p3d17 | 13 | 18 | 31 |
| p3d16 → p3d17 | 8 | 15 | 23 |

Positive Gate/Kachel-Zeilen p3d16→p3d17:

| Gruppe | Regel | Kachel | vorher→nachher |
|---|---|---|---:|
| regeln | G3_spitze_unten | D1 | 0→1 (+1) |
| regeln | G5_beule_klippe | D1 | 0→2 (+2) |
| regeln | R3_woelb_m | D1 | 15→19 (+4) |
| regeln | R4_rand | D1 | 0→1 (+1) |
| regeln | R5_loch | D1 | 0→8 (+8) |
| r8 | R8_stufe | D1 | 0→2 (+2) |
| r9 | R8b_delle | D1 | 0→1 (+1) |
| r9 | R9w_wellen | E1 | 7→8 (+1) |

Vollständige Delta-Berichte und JSONs liegen in [`bilder_p3d17/`](bilder_p3d17/).

## Bilder und Sichtprüfung

Die sechs Vorherbilder aus p3d8 und p3d16 sowie alle sechs p3d17-Ansichten wurden angesehen. Die p3d17-Bilder sind in [`bilder_p3d17/nachher/`](bilder_p3d17/nachher/) gespeichert. Bildindikatoren sind reproduzierbare Hilfswerte; sie ersetzen die Sichtprüfung nicht.

| Ansicht | Facetten p3d16→17 | Kanten-Zähne | Normalensprünge | Löcher | Flecken |
|---|---:|---:|---:|---:|---:|
| D1 / kreuzung | 244→566 | 204→344 | 536→756 | 0→0 | 0→0 |
| D1 / kreuzung_streiflicht_rampe11 | 803→1850 | 190→1143 | 2302→5938 | 1→52 | 1→42 |
| D1 / wandfuss_140_35 | 443→719 | 1079→1258 | 3542→3597 | 65→66 | 70→61 |
| D1 / wegende | 816→1069 | 1059→1049 | 2419→2459 | 62→63 | 53→64 |
| D2 / draufsicht | 13→0 | 313→313 | 2275→2275 | 12→12 | 6→6 |
| G1 / wandfuss | 530→530 | 911→911 | 3393→3393 | 44→44 | 34→34 |

Der Kreuzungs-Clayindikator steigt `244→566`; das Ziel `≤317` ist verfehlt. Die Kernfläche ist durchgehend, aber links bleibt eine spitze Rinne/Erhebung und im entfernten Auslauf kleine Wellen. Im rampe_11-Streiflicht sind weiterhin starke wellige Falten am Wandfuß sichtbar. Das Wegende bleibt gefaltet und eingedellt. Der Wandfuß `140|35` lag außerhalb dieses Themas. G1 ist hashgleich und visuell unverändert. D2 ist mesh-bytegleich und in der Draufsicht visuell unverändert; der Clay-Facettenindikator sinkt dort `13→0`, ohne D2-Meshänderung.

## Annahmen, Grenzen, offene Punkte

- Kartenkoordinaten werden mit 1,2 m je Einheit in die physische Rasterrechnung überführt; Gate-Abtastungen bleiben unverändert und bilinear.
- Die LP-Untergrenze `0,080424 m` gilt für das ausgewiesene lokale Modell mit tatsächlichem R8-Fußabdruck und seinen R3-Stützen. Sie beweist nicht, dass jede unabhängige Prüferformel erfüllt wird.
- Der Transferfehler an der Achse ist geschlossen. Offen ist die Abbildung des offiziellen R3-Abschnittsoperators im Optimierungsmodell; Quer und Wölbung liefern im gemeinsamen Lösungsraster selbst 17 bzw. 19 Treffer.
- Wegend-Ausläufe sowie Wände/Wandfüße außerhalb des rampe_11-Bandrandes wurden nicht weiter bearbeitet. Ihre Gates und Bilder stehen oben.
- Keine Schwellen, Tests, Quellzellen, `vektor.json`, G1 oder D2 wurden geändert. Nach V22 wurde kein weiterer Bau begonnen.

**Gesamtergebnis:** Die LP-Lösung wird direkt ins Mesh übertragen; das Hauptzentrum erreicht die Stufenvorgabe. Der Gesamtauftrag ist nicht erreicht: D1-R3 quer/Wölbung, mehrere D1-R8/R8a-Punkte, der 20-%-Querwert, Clay-Facetten, die +5-Grenze für R5/R9w und die Null-Delta-Vorgabe bleiben offen.

Laufzeitnachweis: `/workspace/codex_jobs/log_p3d17.txt` — model `gpt-6-luna`, reasoning effort `xhigh`.

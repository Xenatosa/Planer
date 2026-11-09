# Ergebnis p3d14

**Stand:** 09.11.2026 · **Branch:** `art/dorfmap-p3d14` · **Basis:** `origin/art/dorfmap-p3d13` (`1bf25853`)

## Ergebnis

Die Same-Route-Paarregel erfasst jetzt die Kehre A/B von rampe_11. Beide MILPs (g=0,60 und g=0,45) sind mit der exakten R3-Abschnittsbedingung lösbar. Der anschließende 2D-Transfer senkt die Kreuzungsstufe auf 0,216 m und das Gitter auf 0,010 m. Das Hauptziel 0,116 m wird verfehlt; im Streiflicht bleibt eine Falte sichtbar. R9 steigt gegenüber dem vorgegebenen Stand um sechs Treffer, also einen mehr als die erlaubten fünf. Diese Fassung ist damit **nicht als Zielerreichung belegt**.

## Änderung und Annahmen

- `neu/mesh.py`: neue, über `RELIEF_KREUZUNG_VAR=17` schaltbare und standardmäßige Variante 17. Die Paarregel verwendet für Same-Route-Paare `Bogen > 1,25 × Sehne`; die gekoppelten Profile werden räumlich weich übertragen. Die adaptive Selektorverbreiterung greift nur im Bereich der untersuchten D1-Kehre. Die Profilebene wird aus den Profilstationen bestimmt (r≤2,25 m, höchstens 3 % Neigung, ±0,05 m) und C1 bis r=4 m ausgeblendet.
- Die Wegführung, Breite, Zellquellwerte, Overlay, Wände und Wandfüße wurden nicht geändert. Der Hilfsblend wirkt nur in der Höhenberechnung.
- Die Profileinheiten verwenden `CELL_M=1,2`; s-Werte in der Profiltabelle sind physische Meter. Das Neu-Mesh meldet `zellen_quell_diff=0`; `neu/vektor.json` hat weiter den Hash `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e`.
- Delta-Zähler enthalten auch Bildproxy-Anstiege aus `nahbild_werte.json`; deshalb werden Gate-Treffer und Bildproxy-Treffer getrennt ausgewiesen.
- Die volle Paarliste, MILP-Ergebnisse und das Werkzeug liegen unter [`codex_jobs/tools/p3d14_milp/`](../../../../../codex_jobs/tools/p3d14_milp/). Der p3d13-Vergleichsstand und alle Ausgaben sind zusätzlich unter [`bilder_p3d14/`](bilder_p3d14/) abgelegt.

### Kehre A/B und Machbarkeit

Die gemessenen Stationen sind A: rampe_11, s=45,6 m, 150,857128|31,399410, Soll 3,696611 m; B: rampe_11, s=48,9 m, 151,033546|33,507795, Soll 2,272361 m. Der Bogen beträgt 3,30 m, die Sehne 2,538903 m (Verhältnis 1,299774), der Sollhöhenunterschied 1,424250 m. Damit gilt `3,30 > 1,25 × 2,538903`; A/B ist in den 218 Same-Route-Paaren enthalten. Zusätzlich gibt es 857 Quer-Rampen-Paare.

| g | Status | Bindende / maßgebliche Paare | Hc (m) | max. Paar-Δh (m) | max. Paargefälle | R3-Abschnitte gesamt / D1 | Quellenabweichung max. (m) |
|---:|---|---|---:|---:|---:|---:|---:|
| 0,60 | optimal, innerhalb der Grenze | rampe_11 s=47,4→47,7: dh=0,138085 m bei d=0,230141 m, bindend; A/B dh=1,023513 m bei Grenze 1,523342 m, Rest 0,499829 m | 4,061716 | 2,157019 | 0,600 | 5 / 3 | 2,000 |
| 0,45 | optimal, innerhalb der Grenze | rampe_2 s=26,4 → rampe_11 s=46,2: dh=1,982237 m bei d=4,404971 m, bindend; A/B dh=1,015088 m bei Grenze 1,142506 m, Rest 0,127418 m | 4,061716 | 1,982237 | 0,450 | 5 / 3 | 2,000 |

Die Plane hat in beiden Lösungen 3,000 % Gefälle und höchstens 0,050 m Profilabweichung. Die drei D1-R3-Abschnitte liegen bei rampe_2 ab s=20,0 m (g=0,60) bzw. s=24,0 m (g=0,45), sowie bei rampe_11 ab s=36,0 m und s=44,0 m. Zwei weitere Abschnitte liegen außerhalb D1 bei rampe_2 s=44,0 m und s=48,0 m. „Max. Paar-|dh|“ bezeichnet den größten Höhenunterschied unter allen MILP-Paarbedingungen; die 2,000 m Quellenabweichung ist separat.

## Prüfergebnisse

Die Standardprüfung auf `relief_daten.json.gz` lief nach `python3 gen_relief.py && python3 baue_html.py`: **570 Regeln, R8 48 (Stufe 9, Gitter 10, Quer 5, Wegende 24), R9 334 (R8b 25, Sägezahn 34, Wellen 275), t42u 0**. Die Summen aus dem Neu-Mesh-Adapter sind die produktbezogenen Werte; der Unterschied zum Standardlauf ist in den Dateien unter `bilder_p3d14/legacy_standard/` und `bilder_p3d14/nachher/` nachvollziehbar.

| Neu-Mesh-Prüfer | p3d13 | p3d14 | Δ |
|---|---:|---:|---:|
| pruefe_regeln gesamt | 567 | 569 | +2 |
| R8 gesamt | 42 | 42 | 0 |
| R8 Stufe / Gitter / Quer / Wegende | 8 / 8 / 5 / 21 | 8 / 8 / 5 / 21 | 0 / 0 / 0 / 0 |
| R9 gesamt | 338 | 340 | +2 |
| R8b / Sägezahn / R9w | 22 / 34 / 282 | 22 / 34 / 284 | 0 / 0 / +2 |

### pruefe_regeln nach Einzelregel

Die vollständigen Treffer je Regel und Kachel stehen im [p3d13→p3d14-Delta](bilder_p3d14/delta_p3d13_p3d14.md) und dessen [JSON](bilder_p3d14/delta_p3d13_p3d14.json). Hier die Zähler (p3d13→p3d14):

| Regel | vorher | nachher | Δ |
|---|---:|---:|---:|
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 39 | 40 | +1 |
| R3_quer_pct | 20 | 21 | +1 |
| R3_woelb_m | 19 | 19 | 0 |
| R5_loch | 17 | 17 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G2_spitze_oben / fein | 3 / 8 | 3 / 8 | 0 / 0 |
| G3_spitze_unten / fein | 3 / 2 | 3 / 2 | 0 / 0 |
| G5_beule_klippe | 67 | 67 | 0 |
| G6_facette | 217 | 217 | 0 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G7b_wandkontur_feld / kantenschaerfe / rauheit | 25 / 1 / 1 | 25 / 1 / 1 | 0 / 0 / 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| G11_baum_an_wand | 2 | 2 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2 / T3 / T4 / T5 Bildprüfung offen | 1 / 1 / 1 / 1 | 1 / 1 / 1 / 1 | 0 / 0 / 0 / 0 |

### D1, G1 und D2 je Kachel

Die Kachel-Summen und Einzelregeln stehen vollständig in den verlinkten Delta-Dateien. Gegen p3d13 sind die Regel-Treffer D1 32→34, G1 11→11 und D2 8→8; R8 D1 3→3, G1 0→0, D2 0→0; R9 D1 22→24, G1 13→13, D2 0→0. In D1 sind gegenüber p3d8 G6 0→1, G11 0→2, R9w 21→23 und der Sägezahnwert 31→38 schlechter. G1 bleibt bei G6=3, R9w=12 und einem Sägezahn-Eintrag. D2 hat keine neuen Treffer in pruefe_regeln, R8 oder R9.

| D1-R8-Treffer | Prüferort / Wert | Feinpunkt-Lage und Meshhöhen | beteiligte Stationen |
|---|---|---|---|
| R8_stufe | Kreuzung 152,5\|28,5: 0,216 m (Ziel ≤0,116) | größter Nachbarsprung im 4-m-Prüffeld: 152,25\|31,75, h=3,298649 m → 152,25\|32,00, h=3,082554 m, dh=0,216095 m | rampe_11, s≈45,3→45,6 m |
| R8_quer | Kreuzung 152,5\|28,5: 3,6 % | nächste Armproben: rampe_2 152,566552\|28,440115, h=4,064475 m → rampe_11 152,395286\|28,536486, h=4,059365 m | rampe_2 s≈31,5 m; rampe_11 s≈41,7 m |
| R8a_wegende | rampe_11 Ende 156,5\|37,5: 0,21 m (p3d11: 0,054 m, kein R8a) | größter Nachbarsprung im Endauslauf: 157,50\|35,50, h=0,588784 m → 157,75\|35,50, h=0,802925 m, dh=0,214141 m | rampe_11-Endstation s≈56,7 m; beide Punkte liegen im Auslaufstreifen hinter dem Ende |

Beim Querwert ist die Höhenpaarung eine nahe Armprobe; der Prüferwert selbst ist die Neigung seiner angepassten Ebene, nicht dieser Höhenunterschied. R8-Gitter D1 beträgt 0,010 m und erfüllt das Ziel ≤0,020 m. G1 und D2 haben keine R8/R8a-Treffer.

### Weitere Zielwerte

| Ziel | p3d14 | Ergebnis |
|---|---:|---|
| D1 R3 längs ≤6 | 11 Treffer; Maximum 0,368 m bei 150,3\|28,7, rampe_2 | verfehlt |
| D1 R3 quer ≤7, kein Wert >20 % | 9 Treffer; Maximum 33,0 % bei 151,8\|29,6, rampe_11 | verfehlt |
| D1 R3 Wölbung ≤7 | 7 Treffer; Maximum 0,252 m bei 150,4\|33,1, rampe_11 | erfüllt |
| Mesh/Soll an D1-Profilstationen ±0,02 m | 95/388 außerhalb; Maximum −0,315383 m bei rampe_2 s=28,5 m, 150,084881\|28,742187 | verfehlt |
| Clay-Facetten D1-Kreuzung ≤317 | 365 | verfehlt |
| R8/R8a D1/G1 0 | D1: Stufe 1, Quer 1, Wegende 1; G1: 0 | verfehlt |
| D1 R9w nicht schlechter als p3d8 | 23 statt 21 | verfehlt |
| Endpunkt 156,5\|37,5 nicht schlechter als p3d11 | Stufe 0,088 m; R8a 0,21 m | verfehlt |
| D1-Meshhash neu | `d4f9a844012ee161bbc490c4b762d538af4731b96188b0ad3d92a03bf1c49688` | erfüllt, gegenüber gesperrten Hashes verschieden |
| G1-Hash | `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` | unverändert |
| D2-Height-Hash | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` | bytegleich / unverändert |
| Klippe 140\|35 | 7,8840365 m | unverändert |
| t42u | 0 Abweichungen | erfüllt |
| Neu LOD1 | 134.316 Dreiecke von 1.300.000 | erfüllt |

Die vollständige Profilmessung steht in [`profil_tabelle.csv`](bilder_p3d14/profil_tabelle.csv). Beim renderbasierten Mesh-Check meldeten `neu/index.html` 9 Meshes, 88.728 Dreiecke und 0 offene Innenkanten. Der separate Standard-Viewer-Check auf `index.html` meldete ebenfalls 0 offene Innenkanten, aber 1.700.454 Dreiecke für seine 7 Meshes; die LOD1-Budgetzahl oben stammt aus dem Neu-Mesh-Build.

## Delta-Prüfungen

`neu/delta.py` meldet Anstiege; der verlangte Null-Anstieg wird in keinem Vergleich erreicht. Jeder Bericht enthält alle Regel-, Kachel- und Bildproxy-Zähler:

| Vergleich | Anstiege gesamt | Gate-Zähler | Bildproxy-Zähler |
|---|---:|---:|---:|
| VAR0→p3d14 | 29 | 8 | 21 |
| p3d6→p3d14 | 26 | 10 | 16 |
| p3d8→p3d14 | 23 | 8 | 15 |
| p3d13→p3d14 | 15 | 3 | 12 |

Berichte: [VAR0](bilder_p3d14/delta_VAR0_p3d14.md), [p3d6](bilder_p3d14/delta_p3d6_p3d14.md), [p3d8](bilder_p3d14/delta_p3d8_p3d14.md), [p3d13](bilder_p3d14/delta_p3d13_p3d14.md). Die D2-Meshhashes sind identisch und D2 hat keine neuen Regel-/R8-/R9-Treffer. Der p3d13-Bildproxy zählt für D2 dennoch +1 Facette; der D2-Draufsicht-Pixelvergleich ändert 3.359 Pixel höchstens um 2 RGB-Stufen. Das ist ein Bildproxy-Anstieg trotz unverändertem Mesh und kein neuer Regel-Treffer.

## Bilder und Tests

Die Bilder aus p3d8 und p3d13 wurden für Kreuzung, Streiflicht rampe_11, Wandfuß 140|35, Wegende, G1-Wandfuß und D2-Draufsicht angesehen. Die sechs p3d14-Aufnahmen liegen in [`bilder_p3d14/nachher/`](bilder_p3d14/nachher/). Die D1-Kreuzung wirkt im Clay großflächig ruhiger als p3d13; im Streiflicht ist der Knick über rampe_11 weiterhin sichtbar. Wandfuß und G1 bleiben außerhalb des bearbeiteten Themas; die D2-Draufsicht ist visuell gleich.

- `pytest neu/tests`: **25 bestanden, 6 fehlgeschlagen**. Fehlgeschlagen: Kreuzungsstufe (0,216>0,20 m), allgemeine Wegenden (21), D1-Sägezahn (38 Elemente), D1-Wandkantenschärfe (2,24<3,00), F1-Wegende (0,17>0,10 m; keine C1-Endpunkte), Schattenartefakt (0,307>0,25). Ziel ≥26/5 nicht erreicht. `test_gelaende_mesh`: 4/4 bestanden; maximaler D1-Höhenversatz 3,643326 m ≤4,0 m.
- Lochscan/Raycast mit xvfb: Neu-Mesh Exit 0, `offen_innen=0`; Standard-Viewer ebenfalls 0. Neu LOD1 134.316 Dreiecke.
- Standard-Gate-Build und t42u liefen erfolgreich; t42u bleibt 0.
- Laufzeitnachweis (Modell und Reasoning-Effort): [`/workspace/codex_jobs/log_p3d14.txt`](/workspace/codex_jobs/log_p3d14.txt), `gpt-6-luna`, `xhigh`.

## Grenzen und offene Punkte

Die Machbarkeit der 1D-Profile ist belegt, aber nicht die geforderte 2D-Zielfläche. Die 2D-R3-Zähler, Achsabweichungen, R8-Stufe, Quergefälle, Wegende, Clay-Facetten, p3d6/p3d8/p3d13-Delta-Anstiege und Pytest-Zahl verfehlen ihre Ziele. Die Stufe 0,216 m und die Restfalte zeigen, dass die lokale Same-Route-Kopplung allein die 2D-Übergangsfläche noch nicht ausreichend glättet. Zellquellwerte, D2, G1 und Wegführung sind unverändert. Keine Schwellen oder Prüfer wurden geändert.

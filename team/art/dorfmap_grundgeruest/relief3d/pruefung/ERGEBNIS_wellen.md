# Ergebnis: wellen

Branch `art/dorfmap-wellen`, Ausgangsstand `9d3f8fc`.

## Ergebnis und Messmethode

Das formale Ziel ist nicht erreicht: `r9_form.py` misst `D["G"]`. Die unveränderte Quelle `G` enthält die 275 R9w- und 25 R8b-Treffer. Die Änderung betrifft ausschließlich die Anzeigehöhen `GB` und `FW`; deshalb bleiben diese beiden formalen Zähler zwingend gleich. Prüfskripte und Schwellenwerte blieben unverändert.

Die folgende Stufenmessung wendet dieselbe R9w/R8b-Formel auf die jeweiligen Zwischenfelder an. Dabei werden die finalen Wasser-, Wand- und Wegmasken verwendet. `GB`-Zeilen sind eine zusätzliche Anzeige-Diagnose, keine offiziellen Gate-Zahlen.

| Stufe | Feld | R9w | R8b | G1-Muldentiefe bei x/z (m): 278,5 / 27,0 |
|---|---|---:|---:|---:|
| Wand-/Geländemodell, vor Erosion | `G` | 243 | 27 | 0,781 m |
| Thermische und hydraulische Erosion | `G` | 235 | 33 | 0,423 m |
| Rampen-/Serpentinenprofil ins Gitter geblendet | `G` | 275 | 25 | 0,423 m |
| Anzeige vor O18 | `GB` | 411 | 23 | 0,423 m |
| Anzeige nach O18-Kern | `GB` | 510 | 12 | 0,015 m |
| Anzeige vor der neuen Glättung | `GB` | 453 | 7 | 0,000 m |
| Anzeige nach der neuen Glättung | `GB` | 433 | 7 | 0,000 m |

Der Rampenblend-Schritt erhöht die R9w-Komponentenzahl netto um 40 (235 auf 275). Beim komponentenweisen Pixel-Überlappungsvergleich entstehen dort 33 Komponenten ohne Pixelüberlappung zur vorherigen Stufe; 21 vorherige Komponenten verschwinden. Die Erosionsstufe verändert die G1-Mulde von 0,781 auf 0,423 m. Der O18-Anzeigekern füllt sie auf 0,015 m, der bestehende Anzeige-Endschliff auf 0 m. Die neue Glättung ändert diese Stelle nicht. `G` selbst wurde bytegleich übernommen.

## Änderung

`gen_relief.py` glättet jetzt nach dem bisherigen Hang-Endschliff nur Anzeigehöhen auf Landhängen mit Neigung 0,15–0,8, mindestens 1,5 m von steilen Wänden und 3 m von Wegen/Rampen entfernt. Ein Gauß-Tiefpass mit 0,75 m Sigma liefert die Korrektur; sie ist pro Punkt begrenzt. Das Feinband erhält dieselbe Korrektur, danach wird die Grob-/Feinbandnaht erneut exakt angeglichen. `D2` ist explizit ausgenommen.

| `WELLEN` | Anzeige-R9w-Diagnose | Maximale Höhenänderung |
|---:|---:|---:|
| `0` (aus) | 453 | 0 m |
| `0.25` | 437 | 0,250 m |
| `0.4` | 435 | 0,286 m |
| `0.6` (Standard) | 433 | 0,286 m |

Die Variantenwerte wurden mit derselben Messformel auf dem gespeicherten Anzeige-Ausgangsfeld verglichen; der Standard `0.6` wurde zusätzlich im vollständigen Build und Gate-Lauf geprüft. Die Anzeige-R8b-Diagnose bleibt bei 7. Diese Anzeigezahlen ersetzen die unveränderten offiziellen R8/R9-Zähler nicht.

## Regeln vorher/nachher

| `pruefe_regeln.py` | Vorher | Nachher | Änderung |
|---|---:|---:|---:|
| Summe | 596 | 570 | -26 |
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 35 | 0 |
| R3_quer_pct | 23 | 23 | 0 |
| R3_woelb_m | 22 | 22 | 0 |
| R5_loch | 17 | 17 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten | 3 | 3 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 66 | 69 | +3 |
| G6_facette | 249 | 220 | -29 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 23 | 23 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |

| Gate-Regel | Vorher | Nachher | Änderung |
|---|---:|---:|---:|
| R8_summe | 48 | 48 | 0 |
| R8_stufe | 9 | 9 | 0 |
| R8_gitter | 10 | 10 | 0 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 24 | 24 | 0 |
| R9_summe | 334 | 334 | 0 |
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |

Die größte Regelzunahme beträgt +3 (`G5_beule_klippe`) und bleibt innerhalb der erlaubten +5.

## D1, G1 und D2

Die offiziellen Treffer je Kachel sind vor und nach der Änderung gleich:

| Prüfung / Kachel | Vorher | Nachher | Aufteilung |
|---|---:|---:|---|
| `pruefe_regeln.py` / D1 | 36 | 36 | R1 2, R2 1, R3 längs 6, R3 quer 11, R3 Wölbung 10, G5 1, G6 5 |
| `pruefe_regeln.py` / G1 | 13 | 13 | R1 1, R3 längs 1, R6 3, G3 fein 1, G6 4, T1 3 |
| `pruefe_regeln.py` / D2 | 8 | 8 | R2 1, T1 7; kein neuer Treffer |
| R8 / D1 | 8 | 8 | Stufe 2, Gitter 2, quer 1, Wegende 3 |
| R8 / G1 | 1 | 1 | Wegende 1 |
| R8 / D2 | 0 | 0 | – |
| R9 / D1 | 26 | 26 | R8b 2, Sägezahn 1, Wellen 23 |
| R9 / G1 | 8 | 8 | R8b 1, Sägezahn 1, Wellen 6 |
| R9 / D2 | 0 | 0 | – |

Der D2-Ausschnitt von `GB` ist bytegleich, Form `(87, 85)`, SHA-256 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` vorher und nachher. Alle 17 Feinband-Höhenwerte und IDs in D2 sind ebenfalls bytegleich. Das komplette Quellfeld `G` ist bytegleich; SHA-256 `056b84f4f57045a905cdb7676b4dec94b71552c5c34e7c0c484c2155011965ff`.

## Gates

| Prüfung | Ergebnis |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` | Erfolgreich; Standard `WELLEN=0.6` |
| Raycast `loch_o18g.js` | `offen_innen=0`, `punkte=0` |
| lod1 gerenderte Dreiecke | 1.174.554, unter 1,3 Mio. |
| `pruefe_t42u.py` | Summe 0 |
| D2-Displayvergleich | Bytegleich, siehe Hash oben |
| `pruefe_regeln.py` | 570 Treffer; keine Regel steigt um mehr als 5 |
| `r8_kreuzung.py` | 48 Treffer, unverändert |
| `r9_form.py` | 334 Treffer, unverändert |
| `sh pruefung/export_gate.sh` | `GATE ROT`, Exit 1: Das Skript verlangt null Gesamttreffer; vorhandene Treffer bleiben bestehen. |

`zellen_relief.csv` wurde nach dem Build auf den Branch-Stand zurückgesetzt. Overlay, Zellquellwerte und die Prüfscripte blieben unverändert. `_weg_eben` und Wegband wurden nicht geändert.

## Annahmen, Grenzen und offene Punkte

- Die Vorgabe, `G` nicht zu ändern, und das Verbot, `r9_form.py` zu ändern, schließen eine Senkung der offiziellen R8b-/R9w-Zahlen durch diese Anzeigeänderung aus. Dafür müsste entweder die Quellhöhe oder die Messgrundlage geändert werden.
- Die Anzeige-Glättung senkt den gleichartig berechneten R9w-Wert auf `GB` von 453 auf 433. Sie senkt die formalen 275 Treffer auf `G` nicht; R8b auf `GB` bleibt bei 7.
- Die Trefferzählung auf Zwischenstufen ist eine Ursachenmessung, kein Ersatz für den End-Gate-Lauf. Die Zähler hängen zusätzlich von Wand-/Wasser-Masken und Komponentenbildung ab.
- Es wurde kein manueller Vorher/Nachher-Sichtvergleich gerendert. Die gemessene Höhenänderung ist auf maximal 0,286 m begrenzt.

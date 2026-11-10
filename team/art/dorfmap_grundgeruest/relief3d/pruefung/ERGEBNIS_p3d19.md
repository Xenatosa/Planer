# Ergebnis p3d19

**Machbarkeit: nein im festgelegten p3d19-Modell. Es wurde kein Mesh gebaut.** Die numerischen Sicherheitsabstände sind für sich genommen erfüllbar. Sobald die konservativen D1-Rückhaltebedingungen für die regressionskritischen Oberflächen sowie die R9w-Bandpassfixierung dazukommen, findet HiGHS keinen zulässigen Punkt. Der direkt übertragene Modellkandidat ohne diese Sperren besteht die R8- und R3-Zielwerte, verletzt aber mehrere harte Regressionsziele und darf daher nicht gebaut werden.

Stand: 10.11.2026 · Worktree `/workspace/wt_dorfmap_p3d19` · Branch `art/dorfmap-p3d19` · Basis `ee46fe5` (`origin/art/dorfmap-p3d18`) · Kosten **0 EUR**.

## Kalibrierung und Modell

Die unveränderte p3d17-Variante 22 wurde erneut durch den offiziellen R3-Prüfer geschickt. Der rekonstruierten D1-Fläche fehlte kein Byte; ihr Hash stimmt mit dem p3d17-Bericht überein. D1 zählte wieder **R3 längs/quer/Wölbung = 6/17/19**. Kalibrierungsbeleg: `codex_jobs/tools/p3d18_r3/calibrate_p3d17.py`.

Der Solver verwendet den offiziellen R3-Operator und den direkten p3d18-Transferoperator der Variante 24. Route, Ebenenkern `r=2,00 m`, Wegführung und Prüfer blieben unverändert. Die Modellgrenzen waren Stufe `≤0,116 m`, Gitter `≤0,019 m`, Quergefälle `≤2,95 %`, Einzelquerung `≤19,5 %`, D1-R3 `≤6/≤7/≤7`, Achsstützen `±0,02 m` sowie am Endpunkt `156.5|37.5` Stufe `≤0,054 m` und kein R8a. Diese Sicherheitsabstände stehen nur im Optimierungsmodell; Prüfer und Schwellen wurden nicht geändert.

Die vollständige harte Kombination aus numerischen Grenzen, allen D1-Sperren (R5-Spitze 0, G6 ≤3, R8b ≤1, G3 ≤1, plus lokale Rückhaltebedingungen) und der R9w-Bandpassfixierung ist **infeasible**: 7.858 Variablen, 34.365 Bedingungen, HiGHS Status `Infeasible`. Beleg: [`machbarkeit_voll.json`](../../../../../codex_jobs/tools/p3d19_r3/machbarkeit_voll.json). Die frühere Teilkonfiguration mit vier D1-Sperren und R9w-Fixierung war ebenfalls infeasible (33.483 Bedingungen; [`machbarkeit_strikt.json`](../../../../../codex_jobs/tools/p3d19_r3/machbarkeit_strikt.json)). In isolierten Diagnosen waren schon die modellierte G6-Rückhaltezone, die lokale G5-Sperre, die lokale R5-Loch-Sperre und die R9w-Bandpassfixierung jeweils mit den numerischen Limits infeasible. Das belegt die Unlösbarkeit dieser konkreten Kombination linearer Rückhaltebedingungen, nicht welcher einzelne exakte Prüferzähler allein mathematisch bindend wäre.

Die lokalen Rückhaltebedingungen pinnen den übertragenen Höhenwert in einer Umgebung bekannter Treffer auf eine Referenzfläche. Das ist eine konservative lineare Ersatzbedingung für die nichtlinearen Komponenten- und Morphologieprüfer, kein mathematischer Beweis, dass jede denkbare Formulierung der exakten Trefferzähler infeasible wäre. Entsprechend ist das Ergebnis **„infeasible im festgelegten Modell“**, nicht ein Beweis für Unmöglichkeit über alle Modellformulierungen.

Ohne diese Regression-Surrogate und ohne die überstrenge R9w-Gleichheitsfixierung fand der Solver einen zulässigen Kernpunkt. Die unveränderten Regel-, R8- und R9-Skripte wurden auf dem float32-Direkttransfer mit Neu-Mesh-Adapter ausgeführt; das ist ein Modell-Probe, kein gebautes Mesh. Für `pruefe_regeln.py` kam dabei ein Nullwert als `LOCHSCAN`-Eingabe zum Einsatz, damit die übrigen Regeln ausgewertet werden konnten. Das ersetzt keinen Lochscan und belegt insbesondere nicht `G1_loch_offen=0`.

| Messung im Modell-Probe | Wert | Grenze | Ergebnis |
|---|---:|---:|---|
| R8-Stufe `152.5|28.5` | 0,115251639 m | ≤0,116 m | erfüllt |
| R8-Gitter `152.5|28.5` | 0,0190000000001 m | ≤0,019 m Modell | erfüllt |
| R8-Quergefälle `152.5|28.5` | 2,9500000000 % | ≤2,95 % Modell | erfüllt |
| D1-R3 längs/quer/Wölbung | 4/0/4 | ≤6/≤7/≤7 | erfüllt |
| D1-Modell-Einzelquerung | ≤19,5 % | ≤19,5 % | erfüllt |
| Achsstützen | 359 geprüft | ±0,02 m | Modellbedingungen erfüllt |
| R8-Stufe `156.5|37.5` | 0,054 m (Gate-Ausgabe, auf mm gerundet) | ≤0,054 m | erfüllt |
| R8a `156.5|37.5` | kein Treffer | kein Treffer | erfüllt |
| R8/R8a D1 und G1 am Zielkreuz | 0 Treffer | 0 | erfüllt |

Als erreichbare Diagnosewerte bei gehaltenen numerischen Modellgrenzen (Stufe, Gitter, Quergefälle, Einzelquerung, R3, Achse und Endpunkt) ergibt der Kandidat ohne Rückhalte- und R9w-Fixierung: R5-Spitze D1 **0**, G6 D1 **3**, R8b D1 **0**, G3 D1 **0**, R9w gesamt **279**; am Zielkreuz Gitter **0,019 m**, Quer **2,95 %**, Stufe **0,115251639 m**, am Endpunkt Stufe **0,054 m**. Das sind erreichbare Werte für diesen Diagnosepunkt, keine kombinierte feasibility-Lösung mit allen Sperren.

Der Kandidat ist nicht baubar: G5 steigt von 69 auf 76 (+7; zulässig wären höchstens 74), D1-G5 steigt 2→9, D1-R5-Loch 5→12 und D1-R4-Schlucht 0→1. G5 trifft D1 unter anderem bei `159.2|21.2` (0,81), `156.0|26.0` (1,00) und `157.7|30.7` (1,65); R5-Loch enthält zwölf D1-Treffer, darunter `155.0|15.5` (1,1 m²) und `157.0|17.0` (3,61 m²); R4-Schlucht trifft bei `142.4|29.7` (1,5). Damit entstehen neue D1-Fehler gegenüber p3d18. Der gemessene `pruefe_regeln`-Probe-Zähler fällt zwar von 596 auf 576, aber die Einzelregelgrenze und die D1-Nullregression sind verletzt. Der Live-Lochscan ist darin nicht enthalten.

## Regelzähler

Die folgenden Vergleichs-Probes wurden alle mit demselben Neu-Mesh-Adapter und denselben offiziellen Regel-, R8- und R9-Prüfern ausgewertet. Der Live-Lochscan war bei allen drei Probes durch denselben Nullwert ersetzt; diese Zahlen enthalten daher keine Aussage zu `G1_loch_offen`. Die archivierten p3d17/p3d18-Berichte zählen 596/577 Regeln. Die reproduzierten Modell-Probes zählen 600/581, weil die Adapterprüfung jeweils vier identische `G11_objekt_schwebt_sinkt`-Treffer (D1 2, G1 2) für die unveränderte Objektbindung hinzufügt. Diese vier Treffer sind in p3d17, p3d18 und dem p3d19-Probe gleich; für die +5-Prüfung gilt weiterhin der angegebene Ausgangswert 596.

| Regel | p3d17 | p3d18 | p3d19 Modell-Probe | D1 p3d17→18→19 | G1 p3d17→18→19 | D2 p3d17→18→19 |
|---|---:|---:|---:|---|---|---|
| G11_objekt_schwebt_sinkt | 4 | 4 | 4 | 2→2→2 | 2→2→2 | 0→0→0 |
| G2_spitze_oben | 3 | 3 | 3 | 0→0→0 | 0→0→0 | 0→0→0 |
| G2_spitze_oben_fein | 8 | 8 | 8 | 0→0→0 | 0→0→0 | 0→0→0 |
| G3_spitze_unten | 4 | 5 | 3 | 1→2→0 | 0→0→0 | 0→0→0 |
| G3_spitze_unten_fein | 2 | 2 | 2 | 0→0→0 | 0→0→0 | 0→0→0 |
| G5_beule_klippe | 69 | 69 | **76** | 2→2→**9** | 0→0→0 | 0→0→0 |
| G6_facette | 219 | 223 | 219 | 3→7→3 | 3→3→3 | 0→0→0 |
| G7_wand_glatte_flaeche | 1 | 1 | 1 | 0→0→0 | 0→0→0 | 0→0→0 |
| G7b_wandkontur_feld | 25 | 25 | 25 | 1→1→1 | 0→0→0 | 0→0→0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 1 | 0→0→0 | 0→0→0 | 0→0→0 |
| G7b_wandkontur_rauheit | 1 | 1 | 1 | 0→0→0 | 0→0→0 | 0→0→0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 1 | 0→0→0 | 0→0→0 | 0→0→0 |
| R1_blind | 24 | 24 | 24 | 2→2→2 | 1→1→1 | 0→0→0 |
| R2_getrennt | 15 | 15 | 15 | 1→1→1 | 0→0→0 | 1→1→1 |
| R3_laengs_m | 35 | 35 | 33 | 6→6→4 | 1→1→1 | 0→0→0 |
| R3_quer_pct | 29 | 17 | 12 | 17→5→0 | 0→0→0 | 0→0→0 |
| R3_woelb_m | 31 | 18 | 16 | 19→6→4 | 0→0→0 | 0→0→0 |
| R4_rand | 1 | 0 | 0 | 1→0→0 | 0→0→0 | 0→0→0 |
| R4_schlucht | 0 | 0 | **1** | 0→0→**1** | 0→0→0 | 0→0→0 |
| R5_loch | 25 | 22 | **29** | 8→5→**12** | 0→0→0 | 0→0→0 |
| R5_spitze | 0 | 5 | 0 | 0→5→0 | 0→0→0 | 0→0→0 |
| R6_wasser_schnee | 4 | 4 | 4 | 0→0→0 | 3→3→3 | 0→0→0 |
| T1_fleckrand | 94 | 94 | 94 | 0→0→0 | 3→3→3 | 7→7→7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 1 | 0→0→0 | 0→0→0 | 0→0→0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 1 | 0→0→0 | 0→0→0 | 0→0→0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 1 | 0→0→0 | 0→0→0 | 0→0→0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 1 | 0→0→0 | 0→0→0 | 0→0→0 |

Die anderen durch den Probe-Prüfer gezählten Regelwerte sind unverändert. Gegen den p3d17-Probe-Ausgang ist `G5_beule_klippe` die einzige ausgewertete Regel über der allgemeinen Grenze +5; `R5_loch` liegt mit 29 gegenüber 25 bei +4. D2 hat in diesem Regel-Probe keine neuen Treffer; D2 blieb im Probe-Adapter bytegleich. Ein echter Lochscan wurde nicht ausgeführt.

## R8 und R9

| Prüfer | Ausgang 9d3f8fc | p3d17 Probe | p3d18 Probe | p3d19 Modell-Probe | D1 p3d17→18→19 | G1/D2 p3d17→18→19 |
|---|---:|---:|---:|---:|---|---|
| R8 gesamt | 48 | 46 | 40 | 39 | Zielkreuz: keine Treffer; Endpunktstufe 0,054 m, kein R8a | 0 / 0 Treffer |
| R8_stufe | 9 | 9 | 7 | 7 | Zielkreuz 0,080→0,076→0,115 m | 0 / 0 Treffer |
| R8_gitter | 10 | 10 | 8 | 8 | Zielkreuz 0,020→0,020→0,019 m | 0 / 0 Treffer |
| R8_quer | 5 | 4 | 5 | 4 | Zielkreuz R8-Treffer 0→1→0 | 0 / 0 Treffer |
| R8a_wegende | 24 | 23 | 20 | 20 | D1 3→0→0 | G1/D2 0 / 0 |
| R9 gesamt | 334 | 344 | 341 | 335 | D1 R9w 27→23→20 | G1 R9w 12→12→12; D2 0 |
| R8b_delle | 25 | 23 | 25 | 22 | D1 1→3→0 | G1/D2 0 / 0 |
| R9_saegezahn | 34 | 34 | 34 | 34 | D1 1→1→1 | G1 1; D2 0 |
| R9w_wellen | 275 | 287 | 282 | 279 | D1 27→23→20 | G1 12→12→12; D2 0 |

Die p3d19 Modell-Probe hält die verlangte R9w-Obergrenze 287 und die allgemeine R9-Ausgangsgrenze +5 ein. Die R8-Ergebnisse sind keine Messung eines gebauten Meshes. Das Zielkreuz und der Wegendpunkt haben im Gate-Probe mit unveränderten Prüfern keine Treffer.

## Grenzen, offene Punkte und nicht ausgeführte Schritte

- Der Modell-Probe-D1-Hash ist `28f6f9abb2033d561d49ab3b688b470eecf63f352d00faaa29ffb5af8e9ce45c`; er ist kein gebauter Artefakt-Hash. G1 blieb `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb`, D2 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`.
- Die strengere lokale Höhenfixierung kann die nichtlinearen Trefferzähler nicht exakt abbilden. Ihr infeasible Ergebnis ist daher als Grenze dieser festen Modellierung dokumentiert. Der ungefixte Probe-Kandidat scheitert unabhängig davon an G5, D1-R5-Loch und D1-R4-Schlucht; er wurde nicht gebaut.
- Die Optimierung wurde im Feasibility-Modus beendet; die Minimierung der Stufe wurde nach der Unmachbarkeit nicht gestartet. Es wurde keine weitere Variante 26 angesetzt.
- `gen_relief.py`, `baue_html.py`, der xvfb-Lochscan, `pruefe_t42u.py`, pytest, `test_gelaende_mesh.py`, delta.py, LOD1-Prüfung und Bildpflicht wurden nicht ausgeführt, weil die Machbarkeit verneint wurde. Es gibt keine finalen p3d19-Mesh-/Bildwerte.
- Zellquellwerte, Overlay, `vektor.json`, Wegführung und D2 wurden nicht verändert. Der Prüfer und seine Schwellen wurden nicht verändert. `t42u` wurde in diesem Lauf nicht neu ausgeführt; es gab keinen Build, der den Wert verändern könnte.
- Modell-/Reasoning-Nachweis: `/workspace/codex_jobs/log_p3d19.txt`. Kosten: **0 EUR**.

Belege und Modellskripte: `codex_jobs/tools/p3d19_r3/`, insbesondere `machbarkeit_voll.json`, `machbarkeit_strikt.json`, `variante25_machbarkeit.json`, `gate_probe_p3d17_reference.json`, `gate_probe_p3d18_reference.json` und `gate_probe_ohne_regressionssperren.json`. Kalibrierung: `codex_jobs/tools/p3d18_r3/calibrate_p3d17.py`.

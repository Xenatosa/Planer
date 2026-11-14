# Ergebnis p3d31

Stand 14.11.2026 · Worktree `/workspace/wt_dorfmap_p3d31` · Branch `art/dorfmap-p3d31` · Basis `origin/art/dorfmap-p3d30` @ `1c2c4e3` · Kosten 0 EUR.

Marker: `[S]` direkt gemessen · `[R]` Modellbefund/abgeleitete Diagnose · `[A]` Annahme oder Grenze · `[F]` Freigabe-/Abbruchentscheidung.

## Zwischenstand

`[S]` Schritt 0 ist abgeschlossen. Der p3d30-Infeasibility-Grund ist durch ein LP-IIS lokalisiert; die p3d31-V1-Konstruktion und der Float32-Checkerlauf sind vorbereitet, aber noch nicht ausgewertet. Daher sind die p3d31-Probezahlen, die Zielerfüllung und ein Mesh derzeit nicht gemessen.

## 0. Ursache der p3d30-Infeasibility

`[S]` Der aktive Solver ist `highspy` 1.15.1 aus `/tmp/p3d18_highspy`. Das originale harte V1-Modell blieb mit HiGHS-Status 8 infeasible (95.347 Variablen, 173.134 Zeilen). Der Standardaufruf `getIis()` lieferte für dieses MIP keine IIS-Zeilen. HiGHS dokumentiert die volle IIS-Suche als LP-Funktion; sie wurde deshalb auf der Integritätsrelaxation mit `iis_strategy=6` (Elasticity-Filter plus Reduktion) ausgeführt. Ergebnis: gültiges IIS mit 7 Zeilen und 6 Spalten. [HiGHS-IIS-Dokumentation](https://github.com/ERGO-Code/HiGHS/blob/master/docs/src/guide/advanced.md).

`[S]` Die 7 IIS-Zeilen bestehen aus einer `p3d30_drainage_successor_choice`-Bedingung und sechs `p3d30_drainage_selected_edge_height`-Bedingungen am Punkt `150,5|1,0`. Die Auswahlbedingung verlangt mindestens einen Nachfolger; alle sechs möglichen Nachbarn liegen im p3d17-Referenzrelief höher. Die Differenzen betragen 0,005548 bis 0,172322 m. Alle sieben Knoten haben Transferdeckung 0, liegen im aktiven Kern und außerhalb des Übergangsrings. Jede der sechs Kanten hat bereits `eps=0`. Das vollständige IIS steht in `codex_jobs/tools/p3d31/results/p3d31_step0_lp_iis.json`.

`[R]` Damit war weder eine über viele Kanten aufsummierte 1-mm-Epsilonstufe noch die Ringlokalität der konkrete Konflikt: Die strikte interne Abflusspflicht verlangte an einer unveränderten p3d17-Lokalsenke einen tiefer liegenden Nachfolger, obwohl kein solcher Kandidat existiert. Der p3d30-All-open-LP-Maximalschlupf von 0,017688 m an `150,0|0,5` → `149,5|1,0` ist ein Relaxationsbefund und nicht die IIS-Ursache. Zusätzliche Lockerungen an Wegzellen, Ring oder Rand-Auslässen waren nach dem konkreten LP-IIS nicht erforderlich.

## 1. Modellaenderungen gegen p3d30

`[R]` Die p3d31-Tools liegen getrennt unter `codex_jobs/tools/p3d31/`. Variante V1 entfernt Nachfolgerwahl, Flussbilanz und Abflusskantenbedingungen vollständig. Senken werden ausschließlich anhand frischer offizieller G5-, R5-Loch- und G6-Komponentenereignisse sowie ihrer unveränderten Zielbudgets behandelt. Die offiziellen Prüfer `pruefe_regeln.py`, `r8_kreuzung.py`, `r8a_policy.py`, `r9_form.py` und `relief_o18n.py` blieben unverändert.

`[A]` V1 ist die Standardvariante (`P3D31_VARIANT=1`). Ein konstruktiver Rückfall V2 ist nur erforderlich, falls V1 infeasible bleibt oder innerhalb der vier erlaubten Prüferrunden keinen gültigen Punkt liefert; über seine Ausführung wird hier später berichtet.

## 2. Machbarkeit je Variante

`[S]` Noch nicht gemessen. Der harte V1-Solve mit allen übrigen p3d30/p3d29-Bedingungen ist vorbereitet. Variablenzahl, Zeilenzahl, Status und ein etwaiger Fallback werden nach dem Solve ergänzt.

## 3. Float32-Gate-Probe mit Checker-in-the-loop

`[S]` Runde 3 abgeschlossen; Checker-in-the-loop wird fortgesetzt Höchstens vier serielle Runden, je Solve höchstens 600 s. Jede Probe lief über den unveränderten Float32-Direkttransfer und die vier unveränderten offiziellen Prüfer.

| Runde | Solve | `pruefe_regeln` gesamt (D1/G1/D2) | R8 gesamt (D1/G1/D2) | R9 gesamt (D1/G1/D2) | offene Ziele |
|---:|---|---|---|---|---|
| 1 | Optimal | 574 (37/13/8) | 42 (3/0/0) | 343 (28/13/0) | R9w_total, R5_loch_total, R5_loch_D1; [JSON](../../../../../codex_jobs/tools/p3d31/results/p3d31_V3_round01_official_probe.json) |
| 2 | Optimal | 578 (41/13/8) | 42 (3/0/0) | 341 (26/13/0) | R9w_total, G5_total, G5_D1, R5_loch_total, R5_loch_D1; [JSON](../../../../../codex_jobs/tools/p3d31/results/p3d31_V3_round02_official_probe.json) |
| 3 | Optimal | 576 (39/13/8) | 42 (3/0/0) | 340 (25/13/0) | R9w_total, G5_total, G5_D1, R5_loch_total, R5_loch_D1; [JSON](../../../../../codex_jobs/tools/p3d31/results/p3d31_V3_round03_official_probe.json) |

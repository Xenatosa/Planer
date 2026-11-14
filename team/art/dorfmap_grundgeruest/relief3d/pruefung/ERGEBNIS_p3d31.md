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

`[S]` Noch nicht gestartet. Es gibt bislang keine Float32-Probe, keine neuen Prüfertreffer und keine gemessenen D1/G1/D2-Kachelzahlen.

## 4. Mesh-Gates, Hashes und Prüfer-Diff

`[S]` Meshbau und Mesh-Gates sind noch nicht gestartet. Vorher-/Nachherwerte und die geforderten Eingabehashes werden nach Abschluss der zulässigen Proberunden ergänzt.

`[S]` Der Prüfer-/Test-Diff gegen `89c61ce` wurde vor der p3d31-Bearbeitung geprüft: ausschließlich die bereits freigegebenen Unterschiede `r8_kreuzung.py`, `r8a_policy.py` und `test_r8a_policy_p3d26.py`; keine Prüferdatei wurde für p3d31 verändert.

## 5. Annahmen, Grenzen und offene Punkte

`[A]` Modellierte Ereignisschnitte sind eine lokale lineare Annäherung für bereits vom offiziellen Prüfer erkannte Ereignisse. Die Gate-Entscheidung basiert immer auf dem vollständigen unveränderten Float32-Prüferlauf, nicht allein auf Modellindikatoren.

## Anforderungen 0–8: Selbstprüfung

| Nr. | Selbstprüfung |
|---:|---|
| 0 | `[S]` Infeasibility durch LP-IIS mit Ort und Kantenhöhen lokalisiert; Details siehe Abschnitt 0 und JSON-Beleg. |
| 1 | `[S]` Unveränderte harte Modellfamilien und V3-Wegführung sind in den separaten p3d31-Modellkopien übernommen; Gate-Nachweis folgt. |
| 2 | `[R]` V1 entfernt nur die interne strikte Abflusspflicht; offizielle Prüfer und Schwellen bleiben unverändert. |
| 3 | `[S]` V1-Solve noch ausstehend; V2 nur bei erforderlichem Rückfall. |
| 4 | `[S]` Höchstens vier Float32-Runden; noch nicht gestartet. |
| 5 | `[F]` Harte Ziele noch nicht gemessen. |
| 6 | `[F]` Meshbau nur nach erfolgreichem Float32-Gate; noch nicht freigegeben. |
| 7 | `[F]` Kein Mesh, keine Bilder. |
| 8 | `[S]` Prüfer-Diff kontrolliert; Hashes und vollständige Zahlen folgen. |

## Drei-Satz-Schluss

`[R]` Die p3d30-Infeasibility entstand an einer p3d17-Lokalsenke mit sechs ausschließlich höher liegenden, transferfixierten Nachbarn und nicht durch das 1-mm-Epsilon. `[S]` V1 entfernt diese interne Abflusspflicht und prüft Senken mit den offiziellen G5-, R5-Loch- und G6-Komponentenbudgets. `[F]` Ob die harten Zielwerte erreicht werden und ein Mesh zulässig ist, bleibt bis zum V1-Solve und Float32-Gate offen.

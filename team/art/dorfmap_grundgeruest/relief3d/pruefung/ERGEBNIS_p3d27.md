# Ergebnis p3d27

Stand 13.11.2026 · Worktree `/workspace/wt_dorfmap_p3d27` · Branch `art/dorfmap-p3d27` · Basis `5089c33` (`origin/art/dorfmap-p3d26`) · Kosten **0 EUR**.

Arbeitsstand: Aufräumen und Kalibrierung abgeschlossen; die V3-Float32-Probe steht aus. Keine Geometrie-, Zellquellwert-, Overlay- oder Prüferänderung in p3d27.

Marker: `[S]` direkt gemessen oder unverändert ausgeführter Prüfer/Test · `[R]` Modellbefund oder abgeleitete Diagnose · `[A]` Annahme · `[F]` Freigabe.

## 0. Bestandstests und p3d23-Werkzeug

`[S]` Die Suite `python3 -m pytest -q neu/tests` wurde am aktuellen p3d26-HEAD `5089c33` und in einem abgetrennten Worktree auf Basis `89c61ce` ausgeführt. Beide Läufe ergaben **26 bestanden, dieselben 5 fehlgeschlagen**; Laufzeiten waren 85,74 s und 84,33 s. Die Fehlermeldungen und Messwerte stimmen überein:

| Test | Fehler in beiden Läufen |
|---|---|
| `test_wegende_allgemein_mesh_ohne_blindenden` | 20 R8a-Wegenden statt 0 |
| `test_saegezahn_d1_mesh_count` | D1-Sägezahnwert 86 statt 0 |
| `test_verwaschene_wand_d1_kantenschaerfe` | 2,24 statt mindestens 3,00 Graustufen/Pixel |
| `test_wegende_f1_c1_meshmessung` | F1 0,17 m statt höchstens 0,10 m; C1 meldet 0 explizite Wegenden |
| `test_schattenartefakt_renderbild` | 0,307 statt höchstens 0,25 Graustufen |

`[R]` Alle fünf Fehler bestehen bereits auf `89c61ce`; sie wurden nicht durch die p3d26-R8a-Ausnahme ausgelöst. Tests, Schwellen und Ausnahme-Implementierung wurden deshalb nicht geändert.

`[S]` Die unbeauftragten Änderungen an `codex_jobs/tools/p3d23/diagnose_slack_p3d23.py` wurden auf den Inhalt von `89c61ce` zurückgesetzt. Die für V3 benötigte ausnahmefähige Fassung liegt separat in `codex_jobs/tools/p3d27/diagnose_slack_p3d27.py`; p3d27-eigene Runner, Float32-Probe und Kalibrierung liegen ebenfalls unter `codex_jobs/tools/p3d27/`.

`[S]` Die unveränderte p3d17-R3-Kalibrierung wurde einmal nach der Prüferänderung ausgeführt: D1 `6/17/19`, D1-Höhenhash `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29`, bytegleicher Transfer. Beleg: [`p3d27_R3_calibration_after.json`](../../../../../codex_jobs/tools/p3d27/results/p3d27_R3_calibration_after.json).

## 1. V3 Float32-Gate-Probe

`[S]` Status: nach Runde 3 beendet (two_rounds_without_score_improvement); Zielabweichungen sind in der Tabelle aufgeführt Maximal sechs serielle Solve-Runden zu höchstens 600 s; V3, alle Familien und unveränderte Prüfer. Die Quelle und Transferbasis haben die im Abschnitt 0 angegebenen Hashes. Frische offizielle G5-/R5-Loch-/G11- Ereignisse werden nach jeder Probe ergänzt; R5-Komponenten ohne ableitbaren Flutsattel bleiben ausdrücklich als nicht geschnittene Ereignisse dokumentiert. Nach den ersten Float32-Gates nutzt das Modell 0,00001 m interne Rundungspuffer innerhalb der unveränderten Stufen- und R8a-Limits.

| Runde | `pruefe_regeln` gesamt (D1/G1/D2) | R8 gesamt (D1/G1/D2) | R9 gesamt (D1/G1/D2) | Ziele / Beleg |
|---:|---|---|---|---|
| 1 | 777 (242/13/8) | 49 (10/0/0) | 333 (14/13/0) | offen: G5_D1, G5_total, R4_schlucht_D1, R5_loch_D1, R5_loch_total, R8a_D1_unpermitted, R8b_D1; [JSON](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round01_official_probe.json) |
| 2 | 833 (298/13/8) | 50 (11/0/0) | 331 (12/13/0) | offen: R8b_D1, G5_total, G5_D1, R5_loch_total, R5_loch_D1, R4_schlucht_D1, R8a_D1_unpermitted; R5 ohne Flutsattel 141.5|2.0, 141.5|6.5, 139.0|11.5, 141.5|13.5, 141.5|16.0, 146.0|23.0; [JSON](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round02_official_probe.json) |
| 3 | 812 (277/13/8) | 44 (5/0/0) | 331 (12/13/0) | offen: R8b_D1, G5_total, G5_D1, R5_loch_total, R5_loch_D1, R4_schlucht_D1; R5 ohne Flutsattel 157.5|9.5, 163.5|15.0, 140.0|21.5, 141.5|22.0, 141.0|22.5, 142.5|22.5, 143.5|22.5, 142.0|23.5, 146.0|23.0; [JSON](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round03_official_probe.json) |

## 2. Mesh-Gate

`[S]` Ein Mesh wird nur gebaut, wenn eine Proberunde alle festgelegten Ziele erfüllt. Deshalb sind Mesh-Gate, Delta-, Hash- und Bildnachweise noch offen.

## Annahmen, Grenzen und offene Punkte

`[A]` Die p3d17-D1-R3-Kalibrierung dient als Referenz für die unveränderte Übertragung. Die V3-Quelle und der temporäre Probe-Relief bleiben unter `/tmp`; die offiziellen Quelldaten bleiben unangetastet.

`[R]` Die fünf Bestandstestfehler sind historische Fehler des p3d18-Testbestands und keine p3d27-Regression. Das sagt nichts über den noch ausstehenden V3-Probelauf aus.

## Drei-Satz-Schluss

`[S]` Die fünf roten Bestandstests wurden auch auf `89c61ce` bestätigt, das p3d23-Tool wurde zurückgesetzt und R3 ist mit `6/17/19` kalibriert. `[S]` Die V3-Float32-Probe ist noch offen; bisher gibt es weder Probe-Nachherzahlen noch einen Meshbau. `[A]` Ob V3 sämtliche Zielwerte einhält und ein Mesh gebaut werden darf, ist noch nicht festgestellt.

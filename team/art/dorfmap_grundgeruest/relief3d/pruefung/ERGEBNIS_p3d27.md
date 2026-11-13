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

`[S]` Noch nicht ausgeführt. Der vorbereitete serielle Checker-in-the-loop ist auf V3, sechs Solve-Runden zu höchstens 600 s und die unveränderten Familien begrenzt. Er verwendet die p3d23-V3-Quelle aus `/tmp/p3d22_v3_source.json.gz` (SHA-256 `b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6`), die p3d21-Transferbasis `p3d21_transfer_base_route3_v29.json` und die p3d26-ausnahmefähige Solverfassung. Frische offizielle G5-/R5-Loch-/G11-Ereignisse werden nach jeder Probe ergänzt. Die Regeln, R8- und R9-Prüfer bleiben unverändert.

| Runde | `pruefe_regeln` gesamt / D1 / G1 / D2 | R8 gesamt / D1 / G1 / D2 | R9 gesamt / D1 / G1 / D2 | Zielstatus |
|---:|---|---|---|---|
| 1–6 | noch nicht gemessen | noch nicht gemessen | noch nicht gemessen | offen |

## 2. Mesh-Gate

`[S]` Ein Mesh wird nur gebaut, wenn eine Proberunde alle festgelegten Ziele erfüllt. Deshalb sind Mesh-Gate, Delta-, Hash- und Bildnachweise noch offen.

## Annahmen, Grenzen und offene Punkte

`[A]` Die p3d17-D1-R3-Kalibrierung dient als Referenz für die unveränderte Übertragung. Die V3-Quelle und der temporäre Probe-Relief bleiben unter `/tmp`; die offiziellen Quelldaten bleiben unangetastet.

`[R]` Die fünf Bestandstestfehler sind historische Fehler des p3d18-Testbestands und keine p3d27-Regression. Das sagt nichts über den noch ausstehenden V3-Probelauf aus.

## Drei-Satz-Schluss

`[S]` Die fünf roten Bestandstests wurden auch auf `89c61ce` bestätigt, das p3d23-Tool wurde zurückgesetzt und R3 ist mit `6/17/19` kalibriert. `[S]` Die V3-Float32-Probe ist noch offen; bisher gibt es weder Probe-Nachherzahlen noch einen Meshbau. `[A]` Ob V3 sämtliche Zielwerte einhält und ein Mesh gebaut werden darf, ist noch nicht festgestellt.

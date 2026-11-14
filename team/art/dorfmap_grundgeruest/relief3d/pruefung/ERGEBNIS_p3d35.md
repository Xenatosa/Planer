# Ergebnis p3d35 — Zwischenstand

Stand 14.11.2026 · Worktree `/workspace/wt_dorfmap_p3d35` · Branch `art/dorfmap-p3d35` · Basis `cc3693e` · Kosten 0 EUR.

Laufzeitnachweis: `/workspace/codex_jobs/log_p3d35.txt` (`gpt-6-luna`, reasoning effort `xhigh`). Marker: `[S]` gemessen · `[R]` Modell-/Diagnosebefund · `[A]` Annahme/Grenze · `[F]` Entscheidung.

## Zwischenstand

`[R]` Neue Werkzeuge liegen ausschließlich unter `codex_jobs/tools/p3d35/`. `P3D35_POLICY=official` ist der Standard; `P3D35_POLICY=p3d34` reproduziert den p3d34-Standardzustand. Die offizielle Variante gibt die gemeinsame Plattformhöhe frei, hält den 1,5-%-Auslaufgradienten fest, öffnet rampe_2 Station 0–50 m und rampe_11 Station 70–90 m und bindet die inneren Übergänge C1-stetig an feste Profilabschnitte. Die offiziellen R3/R8/R8a-Zeilen und Projektbudgets bleiben im Modell aktiv.

`[S]` Die drei geschützten Eingaben wurden vor dem Solve gehasht. `neu/zellen_relief.csv` = `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa`, `neu/vektor.json` = `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e`, `neu/felder.json` = `e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435`. Diese stimmen mit den vorgegebenen Präfixen überein.

`[R]` Die Prüferquellen haben in p3d35 keinen Diff. Der geerbte Diff gegen `89c61ce` enthält für den Prüfer nur `r8_kreuzung.py`, `r8a_policy.py` und `test_r8a_policy_p3d26.py`; `pruefe_regeln.py`, `r9_form.py` und `relief_o18n.py` sind unverändert.

`[A]` Der p3d35-LP-Lauf und der Float32-Probe-/Regel-Gate stehen noch aus. Es gibt daher bisher weder eine Machbarkeitsaussage noch Nachherzahlen, Übergangswerte, Kachelvergleiche oder einen Meshentscheid. Die Vorwerte bleiben die im Auftrag und in p3d34 dokumentierten Vergleichswerte: Ausgang `596 / R8 48 / R9 334`; p3d31 Runde 3 `G5 71/4`, `R5_loch 24/7`, `G6 D1 2`, `R5_spitze D1 0`, `R8b D1 1`, `R3 D1 6/7/7`, `R9w 283`, Kreuzung `0,073/0,019 m`.

## Noch offen

`[A]` Ausstehend sind: p3d35-Hart-LP und gegebenenfalls HiGHS-IIS samt Iterationstabelle; zulässige Profiltabellen und C0/C1-Nachweis; bis zu vier Float32-Proberunden mit Treffern und Zahlen je Regel/Kachel; vollständige +5- und D2-Regressionsprüfung; Mesh-Gates, Bilder und Delta ausschließlich dann, wenn alle harten Zielwerte erfüllt sind.

`[F]` Dieser Zwischenstand behauptet kein erreichtes Qualitätsziel. Der endgültige Bericht ersetzt diese offene Statusfassung nach den Solves und Gates.

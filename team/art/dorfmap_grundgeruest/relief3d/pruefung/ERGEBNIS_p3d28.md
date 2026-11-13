# Ergebnis p3d28

Stand 13.11.2026 · Worktree `/workspace/wt_dorfmap_p3d28` · Branch `art/dorfmap-p3d28` · Basis `0dfd939` (`origin/art/dorfmap-p3d27`) · Kosten **0 EUR**.

Marker: `[S]` gemessen oder unverändert ausgeführter Prüfer · `[R]` Modellbefund/abgeleitete Diagnose · `[A]` Annahme · `[F]` Freigabe.

## 1. Diagnose der p3d27-Runden 1 und 6

`[S]` Die p3d17-D1-Referenz wurde aus dem gespeicherten Float32-Relief `/tmp/relief_p3d27_r3_reference_after.json.gz` ausgelesen. Ihr Hash ist `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29`; er stimmt mit der dokumentierten p3d17-R3-Kalibrierung überein. Die zwei offiziellen p3d27-Probereliefs wurden direkt aus ihren `GB`-Float32-Rastern verglichen; der D1-Ausschnitt hat 7.395 Punkte bei 0,5 Karten-Einheiten Abstand.

| Runde | mittlere absolute Abweichung | P95 `|Δh|` | Maximum `|Δh|` | Punkte `>1 mm` | Punkte `>1 cm` | Punkte `>10 cm` |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2,269 m | 4,687 m | 7,014 m | 4.923 | 4.899 | 4.771 |
| 6 | 2,285 m | 4,719 m | 7,014 m | 4.922 | 4.906 | 4.784 |

`[S]` Runde 1: R5-Loch 104, G5-Beule 78, R4-Schlucht 5 und R8b-Delle 11. Runde 6: R5-Loch 169, G5-Beule 34, R4-Schlucht 7 und R8b-Delle 5. Alle jeweiligen Treffer liegen auf D1-Gitterpunkten, deren nächste 0,5er-Meshhöhe mehr als 1 cm von p3d17 abweicht. In Runde 6 liegen die R5-Punkte über `x=127,0..167,5`, `z=2,0..42,5`; ihre mediane absolute Abweichung ist 4,000 m (Spannweite −5,323 bis −2,024 m). G5 liegt über `x=131,0..162,5`, `z=2,0..39,0`; mediane Abweichung +4,081 m (Spannweite +3,832 bis +5,932 m). R4 liegt über `x=128,0..156,2`, `z=2,5..31,4`; mediane absolute Abweichung 0,755 m. Damit liegen die Senken und Beulen überwiegend in großflächig veränderten Zellen außerhalb der unmittelbaren Weg-/Kreuzungsstützen.

`[R]` Der p3d27-Solve lief mit `objective_mode=diagnostic`. Bei Familienschlupf 0 wird darin keine Bewegung zur p3d17-Höhenfläche minimiert; der sekundäre L1-Tie-Break wird in diesem Modus übersprungen. Das Feld hat 7.395 freie D1-Meshhöhen. Die `variable_bounds` begrenzen abgedeckte Höhen nur auf ±4 m gegenüber dem Quellfeld; die 22 Familien (u. a. 2.244 Routenpaar-, 2.222 R8-Nachbar-, 718 Achs- und 772 Profilgefälle-Zeilen) sichern lokale Weg-/Kreuzungsbeziehungen, pinnen die übrige D1-Fläche aber nicht an p3d17. Das erklärt, warum zusätzliche Ereignisschnitte die weit verteilten R5-/G5-Ereignisse nicht stabil beseitigten.

`[S]` Die Karte mit beiden Differenzfeldern und den R5/G5/R4/R8b-Treffern sowie die vollständigen Float32-Differenzraster und Koordinaten stehen in [`p3d28_d1_delta_comparison.svg`](../../../../../codex_jobs/tools/p3d28/results/p3d28_d1_delta_comparison.svg) und [`p3d28_diagnose_d1.json`](../../../../../codex_jobs/tools/p3d28/results/p3d28_diagnose_d1.json).

## 2. Konstruktionsmodell und offizielle Probe

Modelländerung, Arbeitsbereich-/Ringbreite, Priority-Flood-Abflussbaum, `eps`, Klippen-/Schluchtkrümmung, Machbarkeit, Checker-Runden und Gatezahlen werden nach Durchführung hier dokumentiert. Noch nicht gemessen.


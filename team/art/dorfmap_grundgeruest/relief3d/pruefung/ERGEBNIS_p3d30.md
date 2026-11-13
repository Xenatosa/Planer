# Ergebnis p3d30

Stand 13.11.2026 · Worktree `/workspace/wt_dorfmap_p3d30` · Branch `art/dorfmap-p3d30` · Basis `origin/art/dorfmap-p3d29` @ `177989a` · Kosten 0 EUR.

Marker: `[S]` direkt gemessen oder unverändert ausgeführter Prüfer · `[R]` Modellbefund/abgeleitete Diagnose · `[A]` Annahme · `[F]` Freigabe.

## Zwischenstand

`[R]` Die p3d29-Modellkopie ist unter `codex_jobs/tools/p3d30/` um eine dynamische 8er-Nachfolgerwahl im aktiven Kern plus 7,5-m-Ring erweitert. Die gewählte Kante wird an die Höhe gekoppelt; eine Single-Commodity-Flussbilanz erzwingt, dass jeder Nicht-Auslass zu einem Rand-Auslass entwässert. Auf Wegbandzellen sind nur Bewegungen entlang des lokalen Rampenverlaufs oder vom Verlauf weg zugelassen.

`[S]` Die Konstruktion zählt 5.980 aktive Zellen, 402 Auslässe und 37.686 gerichtete Kandidatenkanten. Alle 5.578 Nicht-Auslasszellen erreichen im Kandidatengraph einen Auslass. Die engere Referenz-Abwärtsfiltervariante wurde als Vergleich geprüft und verworfen: Sie lässt 56 Zellen ohne Nachfolger.

`[A]` Bis zur harten HiGHS-Rechnung ist noch keine Machbarkeit, Float32-Probe oder Zielerfüllung belegt. Es wurde noch kein Mesh gebaut.

## Anforderungen 1–7: vorläufige Selbstprüfung

| Nr. | Stand |
|---:|---|
| 1 | `[R]` p3d29-Kern, Ring, Familien, Formbindung und V3-Transfer sind in der Modellkopie übernommen; vollständige Modellprüfung folgt. |
| 2 | `[S]` Dynamischer gerichteter Kandidatengraph und Erreichbarkeit sind berechnet; MIP-Formulierung wird jetzt hart gelöst. |
| 3 | `[A]` Harte Machbarkeit, LP-Gruppenfilter und gegebenenfalls der einzige Soft-Fallback stehen noch aus. |
| 4 | `[A]` Float32-Checker-Schleifen stehen noch aus. |
| 5 | `[A]` Harte Zielwerte sind noch nicht gemessen. |
| 6 | `[F]` Kein Meshbau, da keine bestandene offizielle Probe vorliegt. |
| 7 | `[A]` Verbleibende Treffer und Schlussbewertung stehen noch aus. |

Weitere Anforderungen, Prüfer-Diff, Hashes, Regelzahlen, Kachelwerte, Annahmen und Grenzen werden nach den Läufen hier ergänzt.

# Ergebnis p3d32

Stand 14.11.2026 · Worktree `/workspace/wt_dorfmap_p3d32` · Branch `art/dorfmap-p3d32` · Basis `origin/art/dorfmap-p3d31` @ `dc98146` · Kosten 0 EUR.

Marker: `[S]` direkt gemessen · `[R]` Modellbefund · `[A]` Annahme/Grenze · `[F]` Entscheidung.

## Zwischenstand vor der ersten Float32-Probe

`[R]` Der p3d32-Hauptweg ist eine kontinuierliche LP im p3d31-Kern-plus-7,5-m-Ringfenster. Kreuzungsplattform, rampe_2-Start, Priority-Flood und offizielle Float32-Lazy-Cuts sind in neuen Werkzeugen unter `codex_jobs/tools/p3d32/` umgesetzt. Die p3d31-Basis wird dort kopiert und erweitert; Prüfer, Schwellen und Zellquellwerte werden nicht geändert.

`[S]` Der erste LP-Aufruf war infeasible. Der anschließende All-Familien-LP-Gruppenfilter war optimal und benötigte ausschließlich 0,05154638898 m Schlupf in `variable_bounds_extra_m`. Das Maximum liegt am Profil `rampe_2`, Station 14,7 m, Karte `138.68964|30.34365`; der gelockerte Wert 7,9467885 m unterschreitet die p3d31-Bewegungsuntergrenze 7,9983349 m. Der schlimmste vom Infeasible-Lauf ausgegebene ungültige Solvervektor war an `r3_cross_constraints`, Zeile 72746; er ist kein IIS und wird nicht als Ursachenbeweis gewertet.

`[R]` Die Diagnose zeigte, dass die erste Modellkopie p3d31-Rampenprofile variabel ließ. Das widerspricht der p3d32-Anforderung fester Wegzellenhöhen. Die Korrektur setzt deshalb alle Wegprofilhöhen auf die p3d31-V3-Runde-3-Lösung fest und dokumentiert die Profilhashes. Der erste Versuch samt Gruppenfilter bleibt als Vorversuch in `codex_jobs/tools/p3d32/results/_alt/` erhalten.

`[F]` Bis zu dieser Korrektur wurde keine offizielle Float32-Probe und kein Mesh gebaut. Der Hauptlauf wird nach der Wegprofil-Fixierung fortgesetzt; die Zwischenmessung ist kein abschließendes Ergebnis.

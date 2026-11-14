# Ergebnis p3d32

Stand 14.11.2026 · Worktree `/workspace/wt_dorfmap_p3d32` · Branch `art/dorfmap-p3d32` · Basis `origin/art/dorfmap-p3d31` @ `dc98146` · Kosten 0 EUR.

Marker: `[S]` direkt gemessen · `[R]` Modellbefund · `[A]` Annahme/Grenze · `[F]` Entscheidung.

## Zwischenstand: LP-Diagnose, noch keine Float32-Probe

`[R]` Der p3d32-Hauptweg ist eine kontinuierliche LP im p3d31-Kern-plus-7,5-m-Ringfenster. Kreuzungsplattform, rampe_2-Start, Priority-Flood und offizielle Float32-Lazy-Cuts sind in neuen Werkzeugen unter `codex_jobs/tools/p3d32/` umgesetzt. Die p3d31-Basis wird dort kopiert und erweitert; Prüfer, Schwellen und Zellquellwerte werden nicht geändert.

`[S]` Der erste LP-Aufruf war infeasible. Der anschließende All-Familien-LP-Gruppenfilter war optimal und benötigte ausschließlich 0,05154638898 m Schlupf in `variable_bounds_extra_m`. Das Maximum liegt am Profil `rampe_2`, Station 14,7 m, Karte `138.68964|30.34365`; der gelockerte Wert 7,9467885 m unterschreitet die p3d31-Bewegungsuntergrenze 7,9983349 m. Der schlimmste vom Infeasible-Lauf ausgegebene ungültige Solvervektor war an `r3_cross_constraints`, Zeile 72746; er ist kein IIS und wird nicht als Ursachenbeweis gewertet.

`[R]` Die Diagnose zeigte, dass die erste Modellkopie p3d31-Rampenprofile variabel ließ. Das widerspricht der p3d32-Anforderung fester Wegzellenhöhen. Die Korrektur setzt deshalb alle Wegprofilhöhen auf die p3d31-V3-Runde-3-Lösung fest und dokumentiert die Profilhashes. Der erste Versuch samt Gruppenfilter bleibt als Vorversuch in `codex_jobs/tools/p3d32/results/_alt/` erhalten.

`[S]` Mit festgesetzten p3d31-V3-Runde-3-Wegprofilen lief das reine LP in Variante 1 600 s und endete mit HiGHS `Time limit reached` (Code 13), ohne primal zulässigen Punkt. Modell: 20.411 kontinuierliche Variablen, 76.616 Zeilen, ein Thread; Prioritäts-Flood hatte 0 Cuts angefordert. Das ist ein Zeitlimit, kein Unmachbarkeitsnachweis und kein IIS. Der gespeicherte unzulässige Solvervektor stammt aus dem abgebrochenen Solve und ist kein Kandidat.

`[S]` Ein nachfolgender Gruppenfilterlauf wurde bei etwa 170 s beendet, weil er denselben großen, ohne Presolve erzeugten LP nicht rechtzeitig diagnostizierte. Er liefert keinen Gruppenbefund. Laufdateien, einschließlich Konstruktion und leeren Cut-Katalogen, sind als Beleg unter `_alt/` abgelegt.

`[A]` Die 600-s-Runde lief mit Presolve aus: die p3d31-Hilfsroutine schaltete es bei `--relax-integrality` ab. Für den nächsten begrenzten Solve ist deterministisches HiGHS-Presolve aktiviert. Das ändert weder Modellbedingungen noch Zielfunktion; die Solve-Grenze bleibt 600 s und der Threadcount 1. Die Runde wird als nächste Probe dokumentiert, auch wenn sie ebenfalls ohne Float32-Punkt endet.

`[F]` Bis hier wurde keine offizielle Float32-Probe und kein Mesh gebaut. Der erste Vorversuch verletzte die feste-Weghöhen-Anforderung; der korrigierte Lauf ist zeitlich ungelöst. Die Zahlen dieses Abschnitts sind Zwischenbefunde und kein Erreichen des Ziels.

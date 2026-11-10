# Ergebnis p3d16

**Zwischenstand: Machbarkeit nachgewiesen; Mesh-Build und Produktprüfungen laufen noch.**

Stand: 10.11.2026 · Branch: `art/dorfmap-p3d16` · Basis: `origin/art/dorfmap-p3d15` @ `cbb1368`

## Machbarkeit vor dem Build

Die gemeinsame lokale Minimierung koppelt die Rampenprofile und das 0,25-Map-Einheiten-Raster der R8-Kreuzung. Sie hält die Achse und alle Stützen im Ebenenkern auf ±0,02 m, den Ebenengradienten auf höchstens 3 %, die p3d15-Profilgrenzen, die Same-Route-Paare (Bogenabstand > 1,25 × Sehne, bis 4,5 m) und die festgelegten Grade `g` ein. Der R3-Lauf benutzt den p3d15-Gaußoperator (σ=8 Stationen, Toleranz 0,075 m, Abschnitte zu 16 Stationen) und höchstens sechs R3-Abschnitte, deren Startstation in D1 liegt.

CELL_M=1,2 m; das lokale Prüfraster hat 1.114 R8-Nachbarpaare, 68 Achsstützen und 137 Ebenenkernstützen. HiGHS meldet für beide R3-MILPs Status optimal und MIP-Gap 0.

| g (m/m) | Stufenminimum ohne R3 (m) | Stufenminimum mit R3 D1 ≤6 (m) | R3-Abschnitte D1 im Optimum | Engstes lokales Paar im R3-Lauf | Ziel ≤0,116 m |
|---:|---:|---:|---:|---|---|
| 0,45 | 0,064738629 | 0,064738629 | 6 | 156,00\|28,00: 3,723869 → 156,00\|28,25: 3,788608 m | erreichbar |
| 0,60 | 0,052649210 | 0,052649210 | 6 | 150,25\|30,75: 3,923068 → 150,25\|31,00: 3,870419 m | erreichbar |

Die gemessene Untergrenze liegt damit 0,051261 m (g=0,45) beziehungsweise 0,063351 m (g=0,60) unter dem Grenzwert. Ohne R3 wurden die R3-Zeilen vollständig ausgelassen; alle übrigen Rampen-, Achs-, Ebenen- und Paarbedingungen blieben aktiv. Der gemeinsame R3-Lauf ist der maßgebliche Machbarkeitsnachweis. Die Werte sind lokale Optimierungsuntergrenzen für die ausgewiesene R8-Maske und noch keine Messung des ausgelieferten Meshes.

Zusätzlicher p3d16-Profil-MILP-Lauf bei Radius 2,00 m, vor dem gemeinsamen Rasterlauf:

| g | MILP-Status | Hc (m) | Ebenenneigung | R3-Abschnitte gesamt / D1 | Paare / Same-Route-Paare | größte Paarneigung | rampe_11 s=45,6→48,9 m: Δh / Sehne / Grad |
|---:|---|---:|---:|---:|---:|---:|---|
| 0,45 | optimal | 4,009337 | 3,000 % | 6 / 4 | 1.075 / 218 | 0,450 | 0,646163 m / 2,538903 m / 25,450 % |
| 0,60 | optimal | 4,029060 | 3,000 % | 5 / 3 | 1.075 / 218 | 0,600 | 1,226331 m / 2,538903 m / 48,302 % |

Dieser Profil-Lauf optimiert zuerst die R3-Abschnittszahl, dann Same-Route-Summe und Quellverschiebung. Er ist von der gemeinsamen Minimax-Rechnung zu unterscheiden; dort verwendet der Solver sein minimax-optimales Profil und erreicht R3 D1=6 für beide g-Werte.

Die reproduzierbaren Eingaben, Skripte und Rohresultate liegen in [`codex_jobs/tools/p3d16_milp`](../../../../../codex_jobs/tools/p3d16_milp/). Die frühere sequenzielle Rechnung mit festgehaltenem p3d16-Profil ergab 0,154846 m bei g=0,45 und 0,192894 m bei g=0,60; sie wird durch die gemeinsame Minimierung abgelöst und war kein Nachweis der Unmachbarkeit. Das gemeinsame Modell variiert das Profil innerhalb der dokumentierten harten Grenzen.

## Als Nächstes

Aufgrund der gemeinsamen Machbarkeit wird Variante 20 auf Variante 19 aufgebaut: `plane_radius_m=2.00`, `plane_inner_m=2.00`, `plane_outer_m=4.0`; Wegführung, Schwellen und Prüfer bleiben unverändert. Danach folgen Build, Adapter, Lochscan, Regeln, R8/R9, Tests, Delta-Vergleiche und die sechs vorgeschriebenen Bildpaare. Dieser Zwischenbericht wird um die gemessenen Produktwerte ergänzt.

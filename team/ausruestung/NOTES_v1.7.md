# Ausrüstung v1.7.2 – Rechen- und Datenhinweise

## Budget und Referenzlevel

`ref_gear_factor_max_e1 = 1.127` ist das Gesamtbudget von 12,7 Faktor-Prozentpunkten. Die zehn aktiven Shares in `gear_slots.csv` summieren sich auf 100 %: acht Gear-Slots teilen 80 %, zwei Artefaktslots je 10 %. In E1 ist Artefakt 2 noch gesperrt; ein voll ausgerüsteter Held trägt acht Gearteile und Artefakt 1. Sein Maximalfaktor beträgt daher **1.1143** und bleibt unter 1.127.

Die E1-Referenz ist Meister-Gear Stufe 9 (Häuptlingsfeuer 10 minus 1). E2 hat Häuptlingsfeuer bis Stufe 15, daher ist die Gear-Obergrenze dort Stufe 14. Die Hauptwerte bleiben auf E1 Stufe 9 budgetiert; `gear_stat_per_level_pct = 5` skaliert sie bis Stufe 14 mit `1.65 / 1.40`. Artefakt 2 belegt ab E2 den zweiten 10-%-Share. `ref_gear_factor_max_e2 = 1.16` ist der bindende E2-Gesamtdeckel.

## Hauptwerte und Setreserve

Für jede Klasse und jeden Gear-Slot gilt:

`main_stat_base_pct = (12.7 × slot_share × class_scale / stat_weight) / (master_mult × level_mult_e1)`

`level_mult_e1 = 1 + 0.05 × (9 − 1) = 1.40`; `master_mult = 1.40`; `stat_weight` ist ATK 0,5 und HP/DEF 0,25. `slot_share` ist der Anteil aus `stat_budget_share_pct` als Dezimalzahl. Gegenüber der alten Berechnung mit Meister 1,32 wurden sämtliche Hauptwerte mit `1.32 / 1.40` neu berechnet.

Die gewichteten 6er-Setboni werden vorab aus dem 80-%-Gearanteil reserviert. `class_scale = (0.127 × 0.80 − set_factor_pct/100) / (0.127 × 0.80)`. Die Reserve beträgt Mammutfell 1,75 Faktor-Pp, Jägerzeichen 1,50 Pp und Ahnenglut 0,75 Pp. Hauptwerte plus aktiver 6er-Setbonus bleiben zusammen innerhalb des Gear-Anteils. Krit und Ult-CD sind aus dem Kampfkraftbudget ausgenommen; ihre eigenen Grenzen bleiben Krit höchstens 25 % und Ult-CD mindestens 10 Sekunden.

Für die Vollausstattung ergeben die aktuellen CSV-Werte E1 **1.114300** (acht Meisterteile Stufe 9, aktives 6er-Set, ein maximales Artefakt) und E2 höchstens **1.143804** (acht Meisterteile Stufe 14, aktives 6er-Set, zwei maximale Artefakte). Beide Werte liegen unter den jeweiligen Deckeln 1.127 und 1.16.

## Raritätenverhältnis und Quelle der 1,15-Grenze

Die Rohmultiplikatoren sind Grob 1,00, Geschliffen 1,20 und Meister 1,40. Der rohe Quotient Meister/Geschliffen ist damit 1,1667; **das ist nicht die geprüfte Fairnesskennzahl**. Geprüft wird der Quotient der Gesamtfaktoren voll ausgerüsteter Helden. Die konservative Budgetformel lautet `(1 + B_master) / (1 + B_master × 1.20 / 1.40)`. Mit den E1-/E2-Referenzbudgets B = 0,127 beziehungsweise 0,16 ergeben sich 1,0164 beziehungsweise 1,0201. Die Berechnung aus den konkreten CSV-Builds liegt darunter (maximal 1,0141).

Die Grenze 1,15 stammt aus der Helden-Regel **SSR ≤ 1,15 × SR** in `team/helden/Helden-System_v1.md`. Diese Grenze wird auf den Gesamt-Statfaktor Meister gegen Geschliffen übertragen, nicht auf den Rohmultiplikator.

## Artefakte

Jeder Artefaktslot umfasst 10 % des Gesamtbudgets. Ein Signaturbonus von 5 % ist bei ATK/HP/DEF bereits so berücksichtigt, dass der Maximalwert mit Signatur höchstens 1,27 gewichtete Faktor-Pp beiträgt: ATK `2.419048 × 1.05 × 0.5 = 1.27`; HP/DEF `4.838095 × 1.05 × 0.25 = 1.27`. Die E2-Startartefakte verwenden dieselben Werte: ATK Stufe 1 = 1.209524, Maximum = 2.419048; HP/DEF Stufe 1 = 2.419048, Maximum = 4.838095. Das feste Startartefakt für Slot 2 ist `art_e2_atk_focus`; HP- und DEF-Varianten sind ebenfalls verfügbar.

## Sets, Freischaltungen und Sim

Setwerte bleiben in Summe unverändert und sind auf 2/4/6 Teile verteilt. Die Gear-Slots sind Waffe, Rüstung, Helm, Schultern, Beine, Schuhe, Ring 1 und Ring 2. Sie werden bei Kampagne 14/16/18/20/22/24 freigeschaltet; Slot 2 des Rings kommt ebenfalls bei 24. Jede Gear-Freischaltung gibt ein passendes Grobteil. Artefakt 1 kommt bei Kampagne 25 mit einem festen Startartefakt, Artefakt 2 beim E2-Aufstieg.

Die isolierte v1.7-Simulation liegt unter `team/ausruestung/sim/sim_f2p.py`. Sie liest Ausrüstungsdaten aus `../` und die übrigen Ökonomie-/Kampagnendaten aus `../../gdd/`. Upgrades kosten Gold, Stein und Holz; es gibt keine separate Schmiedemarkenwährung. Der Laufbericht für Seeds 1–20 liegt daneben in `sim_seeds_1_20.txt`.

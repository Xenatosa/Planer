# Ausrüstung v1.7.2 – Codex-Lauf abgeschlossen

Stand 17.10.2026. Der Ein-Lauf-Abnahmestand ist erfolgreich; dieses Paket wird auf dem Ausrüstungsbranch committed und gepusht. Kein Merge nach main.

- Meister-Multiplikator ist in Konfiguration, Raritäten und Hauptwert-Budget 1,40.
- E2-Feuerobergrenze 15 und maximale Gear-Stufe 14 sind aus `team/aufbau/delta-e2-uebergang.csv` übernommen; es gibt keinen Stufe-20-Fallback.
- E2-Artefaktvarianten für ATK, HP und DEF enthalten die geforderten Start- und Maximalwerte. Signatur +5 % bleibt innerhalb des jeweiligen Anteils.
- E1-Faktor 1,114300 ≤ 1,127; E2-Faktor 1,143804 ≤ 1,16.
- Gesamtfaktor-Ratio Meister/Geschliffen: Budgetformel max. 1,020101; konkrete CSV-Builds max. 1,014046; beide ≤ 1,15.
- Die 1,15-Grenze ist aus der Helden-Regel SSR ≤ 1,15 × SR in `team/helden/Helden-System_v1.md` abgeleitet.
- `validate_v1_7.py` prüft Budget, Faktoren, Raritätsverhältnis und Artefakte. Die v1.7-Sim liegt in `sim/sim_f2p.py`; Ergebnis Seeds 1–20 steht in `sim/sim_seeds_1_20.txt`.

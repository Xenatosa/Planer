# Ausrüstung v1.7.3 – Rechner-Blocker

Stand 17.10.2026. Diese Notiz dokumentiert die Entscheidungen und Abnahmeregeln für den v1.7.3-Blocker-Fix; die ausführlichen Rechenhinweise stehen in `NOTES_v1.7.md`.

- Meister-Multiplikator ist in Konfiguration und Raritäten-CSV 1,38; der Hauptwert-Budget-Multiplikator ist ebenfalls 1,38.
- Meister/Geschliffen beträgt pro Teil bei gleicher Stufe exakt 1,38/1,20 = 1,15. Es gibt keine Gesamtfaktor-Ratio-Prüfung.
- E1-Gesamtfaktor ≤ 1,127; E2-Gesamtfaktor ≤ 1,16 mit Gear bis Stufe 14.
- Zufall wirkt nur auf Beschwörungen. Ein Standardlauf mit Seed 1 genügt; Seeds 1–20 sind keine Pflicht.
- Die Simulation nutzt den versionierten GDD-CSV-Snapshot unter `sim/data/`; `MANIFEST.sha256` dokumentiert die SHA-256-Prüfsummen.

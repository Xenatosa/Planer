# Änderungsbericht: Ranking-Docs v1.6.11 Event-Helden-Fragmente

**Ergebnis:** `team/ranking/` · Branch `ranking/docs-v1611-event-shards`
**Stand:** 23.10.2026 · **Kosten:** 1 Codex/Claude-Lauf
**Kritiker:** geprüft nein · **Geprüft von:** ungeprüft → danach Epochen Ranking + Aufseher
**Nächster Empfänger:** Epochen Ranking

## Geänderte Dateien

- `team/ranking/hilfe-ahnenzeichen.md` – Platzpreise an `ranking_rewards.csv` angepasst; Event-Helden-Fragmente und Meilensteinwerte eingetragen. Law-Wortlaut v1.6.3 blieb unverändert.
- `team/ranking/ranking-konzept-v1.6.md` – Änderungsprotokoll ergänzt; aktuelle Wettstreit- und Weltboss-Platzpreise, Meilensteine und ruhende Fallback-Dokumentation aufgenommen.
- `team/ranking/BERICHT_docs_v1611_shards_2026-10-23.md` – dieser Bericht.

## Abnahmechecks

1. **Aktive Dateien:** `rg` findet den alten Fragmentbegriff weder in `hilfe-ahnenzeichen.md` noch in `ranking-konzept-v1.6.md`. Abnahme-Soll = aktive Hilfe + aktives Konzept. Historische Ranking-Dateien (v1.1–v1.5, Law-/Würfel-Reviews, Paket, Logs) = Altstand, nicht gültig; blieben unangetastet.
2. **Platzpreise:** Die Hilfetabelle wurde mit `ranking_rewards.csv` abgeglichen. Wettstreit: Kristalle 500/400/300/200/120/60, Event-Helden-Fragmente 15/10/10/6/3/0, EP 2.000/1.500/1.200/800/500/300 und Kosmetik/Titel wie in der CSV. `hero_shards_choice` ist in den regulären Wettstreit- und Weltboss-Platzpreisen 0. Der Würfel-Guard in `team/gdd/validate.py` prüft, dass Meilenstein- und Platzpreise dort keine Fragmente enthalten.
3. **Ruhender Fallback:** Dokumentationsansicht und CSV: 0 Kristalle, 0 Event-Helden-Fragmente, `hero_shards_choice=0`; EP, Kosmetik und Titel unverändert. GD-Datenpunkt 23.10.: Fallback-CSV angeglichen, Tabelle weiter ruhend (`ranking_rewards_table = regular`).
4. **Meilensteinwerte:** Weltboss-Kristalle 20/0/20/30; `ms_sw_4` gems_free=55 (GDD 31.2 + `event_milestones.csv`, von Ranking und GD bestätigt).
5. **Weitere Leitplanken:** Änderungsprotokolle stehen am Kopf der aktiven Hilfe und des v1.6-Konzepts. Es wurden keine Shop-Links oder spielerseitigen Aussagen „nie kaufbar“ ergänzt. Die bestehenden Law-Texte v1.6.3 blieben erhalten. Keine GDD-/CSV-Änderung und keine Simulation.

## Übergabe

**Offene Fragen:** keine. GD-Datenpunkt 23.10.: Fallback-CSV angeglichen; `ms_sw_4=55` bestätigt. Kritik M1 (A7/`free_only`) in Hilfe + Konzept A nachgezogen; Recheck-Reste S4/S5 geschlossen; Law-Strings v1.6.3 unberührt. Abnahme „Wahl-Fragment“ gilt für aktive Hilfe + aktives Konzept; Historie = Altstand. Repo-Spiegel epodarien noch alt (Paket `team/dev/pakete/2026-10-23_ranking_fallback_shards_zero.md`).
**Arbeitsstatus:** Ranking-Docs v1.6.11 Shards · `team/ranking/` · bereit zur Prüfung.

DONE 2026-10-23T19:49:46+02:00 (S4/S5 nach Recheck 1)

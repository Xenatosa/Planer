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

1. **Aktive Dateien:** `rg` findet den alten Fragmentbegriff weder in `hilfe-ahnenzeichen.md` noch in `ranking-konzept-v1.6.md`. Der verlangte folderweite Check trifft zusätzlich historische Ranking-Konzepte v1.1–v1.4, `law-review-v1.2.md`, `review-wuerfel-event-v1.md` und das unveränderte Aufgabenpaket. Die Hilfe-Archive v1.3–v1.5 sowie diese historischen Texte und das Aufgabenpaket blieben unangetastet; dadurch ist das folderweite Soll „nur Hilfe-Archive“ im vorhandenen Bestand nicht erfüllt.
2. **Platzpreise:** Die Hilfetabelle wurde mit `ranking_rewards.csv` abgeglichen. Wettstreit: Kristalle 500/400/300/200/120/60, Event-Helden-Fragmente 15/10/10/6/3/0, EP 2.000/1.500/1.200/800/500/300 und Kosmetik/Titel wie in der CSV. `hero_shards_choice` ist in den regulären Wettstreit- und Weltboss-Platzpreisen 0. Der Würfel-Guard in `team/gdd/validate.py` prüft, dass Meilenstein- und Platzpreise dort keine Fragmente enthalten.
3. **Ruhender Fallback:** Die neue Dokumentationsansicht hat 0 Kristalle und 0 Event-Helden-Fragmente; EP, Kosmetik und Titel folgen den Fallback-Zeilen. `ranking_rewards_fallback.csv` wurde wie beauftragt nicht geändert und enthält weiterhin `hero_shards_choice` 30/20/15/10/5. Der Fallback ist deshalb laut Dokumentation bis zum Abgleich durch den Datenverantwortlichen nicht aktivierbar.
4. **Meilensteinwerte:** Die Doku führt Weltboss-Kristalle 20/0/20/30 und `ms_sw_4` mit 75 entsprechend der expliziten Quellenangabe im Auftrag. Hinweis zur Quelle: GDD v1.6.13 Abschnitt 31.2 und `event_milestones.csv` führen `ms_sw_4` derzeit mit 55; beide Dateien blieben unverändert.
5. **Weitere Leitplanken:** Änderungsprotokolle stehen am Kopf der aktiven Hilfe und des v1.6-Konzepts. Es wurden keine Shop-Links oder spielerseitigen Aussagen „nie kaufbar“ ergänzt. Die bestehenden Law-Texte v1.6.3 blieben erhalten. Keine GDD-/CSV-Änderung und keine Simulation.

## Übergabe

**Offene Fragen:** keine; die im Bericht genannten Datenabweichungen sind für Epochen Ranking und Aufseher sichtbar.
**Arbeitsstatus:** Ranking-Docs v1.6.11 Shards · `team/ranking/` · bereit zur Prüfung.

DONE 2026-10-23T19:39:27+02:00

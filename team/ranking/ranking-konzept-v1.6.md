# Ranking-Konzept v1.6 – Epodarien (Delta zu v1.5)

**Für:** Fabian Schwegler · **Stand:** 23.10.2026 · Version 1.6 (kurze Delta-Version, Epochen Ranking)
**Basis:** `ranking-konzept-v1.5.md` (gilt weiter, soweit hier nichts geändert wird) · **Fabian-Entscheidung vom 14.10.2026: Variante A** · GDD v1.6.13 Kap. 24/28/31 · Law-Review v1.4.
**Lesart:** Bei Widerspruch gilt **GDD > Fabian-Entscheidung > dieses Delta > v1.5**. GDD v1.6.13 bildet Variante A in den Daten ab; der frühere Auftrag K-GD30 ist damit erledigt. Ältere Versionen bleiben unverändert. **Keine Rechtsberatung.**
**Spielerhilfe:** `hilfe-ahnenzeichen.md` auf Variante A umgestellt. Vorstand gesichert als `hilfe-ahnenzeichen-v1.5.md`.
**Gültigkeit:** Aktiv sind nur `ranking-konzept-v1.6.md` und `hilfe-ahnenzeichen.md`. Historische Ranking-Dateien (ältere Konzept-/Hilfe-/Review-Versionen, Paket, Logs) = Altstand, nicht gültig.

---

## Änderungsprotokoll v1.6.11+ (23.10.2026)

| # | Änderung | Quelle |
|---|---|---|
| 1 | Stammeswettstreit- und Weltboss-Platzpreise verwenden `event_hero_shards`; `hero_shards_choice = 0` in den regulären Platzpreisen. | `team/gdd/ranking_rewards.csv` |
| 2 | Platzbelohnungswerte und Meilensteine in Abschnitt D ergänzt; Würfel-Event bleibt fragmentfrei. | GDD v1.6.13, `ranking_rewards.csv`, `event_milestones.csv` |
| 3 | Ruhende Law-Fallback-Tabelle ohne Fragmentwerte; CSV angeglichen (`hero_shards_choice=0`), weiter ruhend. | GDD 24.5, `ranking_rewards_fallback.csv` |
| 4 | Law-Wortlaute nach GDD v1.6.3 beibehalten. | bestehender Abschnitt A/B |
| 5 | K-GD30 geschlossen: Variante A ist in GDD v1.6.13 abgebildet. | GDD 24.4a/24.6 |
| 6 | Fallback-CSV: `hero_shards_choice` auf 0 gesetzt (GD 23.10.); Docs-Hinweis „nicht aktivierbar“ entfällt. | GD-Datenpunkt, `ranking_rewards_fallback.csv` |
| 7 | Event-Helden-Fragment-Meilensteine: Hilfe + Abschn. A an Law A7 / `event_hero_points_basis=free_only` angeglichen (Paid nur Kristalle/EP/Emote). Law-Strings v1.6.3 unberührt. | Kritik M1, GDD 28.4 |
| 8 | Recheck-Reste S4/S5: Wochen-Beispieltabelle ohne „Fragmente“ in Paid-Zeile; QA-RK-10 mit free_only-Fußnote. | Kritik Recheck 1 |

---

## Änderungsprotokoll v1.5 → v1.6

| # | Änderung | ersetzt in v1.5 |
|---|---|---|
| 1 | **Entscheidung Variante A:** Rang, Kristall-Platzbelohnungen und Gleichstand nur aus **Gratis-Versuchen**. Gekaufte Fackeln bringen **Übung und Meilenstein-Fortschritt** (ohne Festmünzen) | B (Variantentabelle → Entscheidungsvermerk) |
| 2 | **Spielertexte** auf Variante A festgelegt; Status-quo-Pflichtsatz „erhöhen deine Chance … auf einen höheren Platz“ entfällt; der mittelbare Weg zu Meilensteinen wird offen genannt | C Nr. 3, Hilfe |
| 3 | **AGB 12.8 Nr. 7 und Nr. 8** auf die Variante-A-Fassung festgelegt | D |
| 4 | Ahnenprüfung-Regeln, Balken-Anzeige und Beispiele angepasst | A |
| 5 | Neue Daten-/UI-Aufträge an GD/Dev (K-GD30–32) | F |
| 6 | **Law-Texte nach GDD v1.6.3:** Wettstreit-Pflichtformel ohne „Punkte nur erspielbar“; Kaufdialog mit Meilenstein-Beispielen; U18-Hinweis ohne Altersbezug; QA-RK-05 erwartet neuen Hint | C Nr. 3, D, QA |

---

## A. Entscheidungsvermerk (ersetzt v1.5 Abschn. B)

> **Entschieden durch Fabian am 14.10.2026: Variante A** (Law-Hauptempfehlung, Law-Review v1.4 Nr. 0).
> Rang, Kristall-Platzbelohnungen und Gleichstand im Stammeswettstreit werden **nur aus Gratis-Versuchen** gewertet (Tages-Gratisversuche und Fackeln aus Quests/Gratisquellen). Gekaufte Fackeln (für Kristalle oder €) bringen **Übung und Meilenstein-Fortschritt** bei **Zeitkristallen, Heldenerfahrung und Emote**, aber **keine Festmünzen** und **keinen Fortschritt** bei Event-Helden-Fragment-Meilensteinen (`event_hero_points_basis = free_only` / Law A7).
> **Verworfen:** Status quo (alle Versuche zählen für den Rang) und Variante B (getrennte Wertungen). Die Abwägung steht in v1.5 Abschn. B.
> **Folgen laut Law v1.4:** Nr. 1 (§ 10b) → 🟢; Nr. 3, 4, 7, 8 je mindestens eine Stufe besser. Die Google-Policy-Anfrage vor M6 bleibt, mit dem Sachverhalt „gekaufte Versuche zählen nur für Meilensteine“. Die Fallback-Tabelle bleibt ruhend (`ranking_rewards_table = regular`); die CSV ist angeglichen (`hero_shards_choice=0`, Kristalle und `event_hero_shards=0`).

**Regeln Ahnenprüfung (ersetzt v1.5 A, Zeilen „Rang“ und „Gleichstand“):**
| Zweck | gewerteter Versuch je Tag |
|---|---|
| **Rang, Platzbelohnungen (Kristalle, Event-Helden-Fragmente, EP, Krone, Titel)** | bester **Gratis**-Versuch |
| **Gleichstand** | nur beste **Gratis**-Versuche je Tag: Σ ‰ → Σ Sekunden (weniger gewinnt) → geteilter Platz 1, 2, 2, 4 |
| **Festmünzen-Meilensteine** | bester **Gratis**-Versuch (unverändert `coins_best_free`) |
| **Event-Helden-Fragment-Meilensteine** | bester **Gratis**-Versuch (`event_hero_points_basis = free_only` / Law A7) |
| **Übrige Meilensteine** (Kristalle, EP, Emote) | bester Versuch **insgesamt**, auch gekaufter |
Bester Versuch jeweils: höchste ‰, bei gleichen ‰ weniger Sekunden (PvP). Tageslimit gekaufter Fackeln 2, Verbrauch Tagesgratis → Quest-Fackeln → gekaufte, U18 gesperrt (v1.5, unverändert).

**Mittelbarer Weg (offen nennen, Law K-L7/Nr. 3):** € → (Kristalle →) Fackel → besserer Versuch → **Meilenstein-Kristalle/EP/Emote**. **Nicht** für Event-Helden-Fragment-Meilensteine (A7/`free_only`). Der Weg ist klein (höchstens 300 Punkte/Tag aus der Ahnenprüfung, nur diese Meilensteine, keine Platzbelohnung). Er wird in Hilfe, Kaufdialog und AGB genannt und **nie** als „bringt keinen Vorteil“ beschrieben. Law-Pflichtformeln v1.6.3 bleiben generisch („Fragmente“) und unverändert.

**UI (ersetzt v1.4/v1.5 Balken-Regel):** Ein Balken „Punkte“ = Rang- und Festmünzen-Punkte (nur Gratis-Versuche). Zusätzlich zeigt die Meilenstein-Leiste die Zahl „Meilenstein-Punkte“, aber nur wenn sie abweicht (nach einem gekauften Versuch, der besser war als der beste Gratis-Versuch). Kein Kauf-Button und keine verzögerten Angebote (v1.5 C), QA-Testfälle QA-RK-01 bis 09 gelten weiter. **Neu: QA-RK-10:** Ein gekaufter Versuch ist besser als der beste Gratis-Versuch → Rang, Bracket-Liste und Tie-Break-Werte unverändert; nur die Meilenstein-Punkte (Kristalle/EP/Emote) steigen; Festmünzen und Event-Helden-Fragment-Meilensteine unverändert (`free_only`).

**Telemetrie (GDD 24.9):** Die Auslöser bleiben (Gewinnquote Spar-Zahler vs. F2P-Sparer, F2P < 30 % der Titel). Erwartung unter Variante A: Die Lücke beim Platz verschwindet weitgehend [Annahme, neue Sim durch GD]. Zusätzlich messen: **Meilenstein-Vorsprung** durch Fackeln (Anteil Spieler, die einen Kristall-/EP-/Emote-Meilenstein nur dank gekaufter Versuche erreichen; Fragment-Meilensteine ausgeschlossen). Weiterhin nur mit Analytics-Einwilligung.

**Texte (ersetzt v1.5 C Nr. 3):**
- Pflichtformel auf Wettstreit-Screens (reiner Text, ohne Link): **„Zusätzliche Versuche kaufbar (Tageslimit 2). Für Platz, Platzbelohnungen und Festmünzen zählen nur Gratis-Versuche.“** (`trial_contest_screen_text`, GDD 24.4a)
- Kaufdialog (nur im Shop): Menge, Kristallpreis + ungefährer €-Wert bzw. 0,99 €, „heute noch X verfügbar“, **„Gekaufte Versuche zählen nicht für Platz, Platzbelohnungen und Festmünzen. Sie zählen für die übrigen Meilensteine (z. B. Kristalle, Fragmente, EP).“** (`trial_paid_rank_text`, GDD 24.4a), Widerrufsbelehrung (§ 356 Abs. 6 BGB [Stand prüfen]).
- U18-Hinweis (`minor_attempts_hint_text`, GDD 24.7): **„Zusätzliche Versuche können nicht gekauft werden.“** (ohne Altersbezug; ersetzt „Zusätzliche Versuche sind erst ab 18 verfügbar.“).
- **QA-RK-05** (Override zu v1.5): Konto U18 → Shop: nicht gelistet; Hinweis **„Zusätzliche Versuche können nicht gekauft werden.“**
- Verbotene Claims unverändert, auch „Geld bringt keinen Vorteil“. Keine Sim-Zahlen.

## B. AGB-Sätze (festgelegt, ersetzt v1.5 D)

**12.8 Nr. 7 (Gleichstand):** „Bei gleicher Punktzahl entscheidet die Summe der Rest-HP-Promille deiner besten Gratis-Versuche je Tag, danach die geringere Summe ihrer Kampfsekunden. Herrscht dann noch Gleichstand, teilen sich die Spieler den Platz. Jeder erhält die volle Belohnung dieses Rangs, der nächste Rang wird übersprungen (1, 2, 2, 4). Versuche mit gekauften Prüfungsfackeln werden dabei nicht gewertet. Die Uhrzeit entscheidet nie.“

**12.8 Nr. 8 (Fackeln/Tickets):** „Prüfungsfackeln und Arena-Tickets geben zusätzliche Versuche innerhalb eines Tageslimits (Fackeln 2, Tickets 3 pro Tag). Sie bringen keine Punkte direkt. **Versuche mit gekauften Prüfungsfackeln zählen nicht für Platzierung, Platzbelohnungen, Gleichstand und Festmünzen. Sie können aber dein Tagesergebnis für die übrigen Meilensteine verbessern.** Als gekauft gilt jede Fackel, die mit Zeitkristallen oder Echtgeld erworben wurde. In der Arena gibt es Ligapunkte nur aus den Gratis-Kämpfen. Mit Echtgeld erworbene Ressourcen bringen im Stammeswettstreit keine Punkte (Event-Zeitraum und 7 Tage davor). Wird ein Kauf von Prüfungsfackeln oder Arena-Tickets erstattet oder zurückgebucht, werden nicht verbrauchte Fackeln/Tickets entfernt. Bereits erzielte Platzierungen bleiben bestehen. Bei wiederholten Erstattungen nach erzielter Platzierung (Missbrauchsmuster) können wir nach menschlicher Prüfung die betroffenen Belohnungen zurückbuchen oder den Spieler nach Nr. 1 (e) von Wettbewerben ausschließen. Für Spieler unter 18 können zusätzliche Versuche nicht gekauft werden (Prüfungsfackeln und Arena-Tickets). Regeländerungen nur zwischen Events mit Vorankündigung.“

DSGVO-Baustein, Erstattung und Voided Purchases: unverändert aus v1.5 D.

## C. Offene Punkte v1.6
| # | Thema | Auftrag |
|---|---|---|
| K-GD31 | UI-Key für die Anzeige „Meilenstein-Punkte“ bei Abweichung (bisher `ui_event_progress_bars = 1_plus_coin_marker`, umgekehrte Logik) | GD/Dev UI, z. B. `1_plus_milestone_marker` |
| K-GD32 | Neue Sim für Variante A (Gewinnquote, Titel-Anteil F2P, Fackel-Umsatz) | GD (`sim_liveops`) |
| K-L11 | U18: Law hält unter Variante A 1 Fackel/Tag für vertretbar; v1.5 sperrt Fackeln **und** Tickets. Bleibt gesperrt, bis Fabian anders entscheidet | Fabian (optional), Law |
| aus v1.5 | K-GD23, K-GD25–28, K-P10, K-L10, Moderation (F-2) | unverändert offen |

## D. Datenabgleich ab GDD v1.6.11

### Platzbelohnungen (`ranking_rewards.csv`)

| Rang | Stammeswettstreit: Kristalle / `event_hero_shards` / EP / Extra |
|---|---|
| 1 | 500 / 15 / 2.000 / Stammeskrone + Titel „Stammesfürst“ |
| 2 | 400 / 10 / 1.500 / Rahmen „Wettstreit“ |
| 3 | 300 / 10 / 1.200 / Rahmen „Wettstreit“ |
| 4–10 | 200 / 6 / 800 / – |
| 11–25 | 120 / 3 / 500 / – |
| 26–50 | 60 / 0 / 300 / – |

| Rang | Weltboss: Kristalle / `event_hero_shards` / EP / Extra |
|---|---|
| 1 | 300 / 10 / 0 / Mammutkrone + Titel „Mammutbezwinger“ |
| 2–10 | 150 / 5 / 0 / – |
| 11–50 | 80 / 2 / 0 / – |
| 51–100 | 40 / 0 / 0 / – |

Für beide Ranglisten ist `hero_shards_choice = 0`. Beim Würfel-Event gibt es keine Fragmente.

### Meilensteine

| Event | Stufe | Kristalle | `event_hero_shards` | EP / Extra |
|---|---|---:|---:|---|
| Stammeswettstreit | 2.000 | 30 | 0 | 500 EP |
| Stammeswettstreit | 6.000 | 50 | 5 | 800 EP |
| Stammeswettstreit | 12.000 | 70 | 0 | 1.000 EP |
| Stammeswettstreit | 20.000 (`ms_sw_4`) | 55 | 5 | 1.500 EP |
| Stammeswettstreit | 30.000 | 0 | 0 | Emote „Ahnen“ |
| Weltboss | 25 % | 20 | 0 | 500 EP |
| Weltboss | 50 % | 0 | 5 | 500 EP |
| Weltboss | 75 % | 20 | 0 | 500 EP |
| Weltboss | 100 % | 30 | 10 | 1.000 EP + Banner |

Für Event-Helden-Fragmente aus Meilensteinen gilt `event_hero_points_basis = free_only`.

### Ruhende Law-Fallback-Tabelle

Die folgende Dokumentationsansicht hält Kristalle und Fragmentwerte aus der Fallback-Tabelle heraus. Sie übernimmt EP, Kosmetik und Titel der ruhenden `ranking_rewards_fallback.csv`:

| Rang | Kristalle | `event_hero_shards` | EP | Kosmetik / Titel |
|---|---:|---:|---:|---|
| 1 | 0 | 0 | 4.000 | Stammeskrone + Rahmen „Stammesfürst“ / Titel „Stammesfürst“ |
| 2 | 0 | 0 | 3.000 | Rahmen „Wettstreit“ |
| 3 | 0 | 0 | 2.400 | Rahmen „Wettstreit“ |
| 4–10 | 0 | 0 | 1.600 | Emblem „Top 10“ |
| 11–25 | 0 | 0 | 1.000 | – |
| 26–50 | 0 | 0 | 600 | – |

**Datenhinweis:** `ranking_rewards_fallback.csv` ist angeglichen: `hero_shards_choice`, Kristalle und `event_hero_shards` sind 0; EP/Kosmetik/Titel unverändert. Die Tabelle bleibt ruhend (`ranking_rewards_table = regular`).

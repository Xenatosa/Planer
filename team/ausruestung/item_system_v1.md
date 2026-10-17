# Item-System v1.7.2 – Inventar & allgemeine Items (Epodarien)
Stand 17.10.2026 · Epochen Ausrüstung · Daten: `items.csv` (allgemein), `equipment.csv` (Ausrüstung, siehe ausruestung_konzept_v1.md). [GDD] = aus GDD v0.7, [Annahme] = Vorschlag.

## 0. Grundsätze (aktueller Stand, GDD v1.6.12 Kap. 0 und 0.2)
- Alles änderbar: Stapel, Plätze, Kurse, Limits, Verfallsfristen als Keys (`game_config_ausruestung.csv`, `items.csv`); Entscheidungen = aktueller Stand; Kategorien/Shops modular.
- **Grundregel 0.2:** Zeitkristalle kauft man nur für **Items, Boosts und Event-Teilnahme**, **nie für Punkte oder Rang**; **alles ist limitiert** (`crystal_use_scope`, `purchasable_points = none`, `participation_items_limit_rule = daily_and_per_event`).

## 1. Kategorien
| category | Beispiele | Hinweis |
|---|---|---|
| consumable | Ressourcenkisten als **Produktionsstunden** (wie Minigames, GDD Nr. 49), Heldenerfahrung | skaliert mit Fortschritt |
| material | Echosplitter | Fortschrittsmaterial; Schmiedekosten verwenden Ressourcen direkt |
| consumable (Glutuhr) | `itm_clock_5m/15m/60m/180m`: stack_max 999, verfallen nie, verdient **und** kaufbar, wirken **nur auf Forschung**; `itm_glut_*` entfällt | Erstattung gekaufter ungenutzter Uhren (GDD 21.3) |
| consumable (Teilnahme) | Würfelbeutel `itm_dice_energy` (verfällt nie), Arena-Ticket, Prüfungsfackel | Tages- + Event-Limit |
| currency_ref | Festmünzen `cur_event_coin` (nie kaufbar, Event-Shop) | Deckel `event_coin_cap_28d` |
| hero_fragment | Event-Helden-Fragmente (`frag_*`, `itm_frag_event_hero`) | aus GDD übernommen |
| ticket | Ahnenruf-Ticket [GDD cur_summon_ticket] | Zufall erst beim Einsatz am Banner → Chancen dort |
| fragment | Heldenfragment, Wahl-Fragment [GDD] | deterministisch |
| chest | Kapitel-Truhe (fester Inhalt), Wahl-Truhe | **Standard: kein Zufall** |
| event | Mammut-Trophäe (Minigame `mg_speerwurf`; Weltboss hat keine Marke), Baumeister-Plakette | einzige verfallende Kategorie |
| event_saving | Ahnenzeichen [GDD] | kein Verfall, Bankdeckel |
| cosmetic | Skins, Rahmen | power_bonus 0 |
| equipment / artifact | equipment.csv / artifacts.csv | eigener Tab, nicht stapelbar |
Währungen bleiben in `currencies.csv`; items.csv verweist per `ref_id`, damit keine Doppelbuchung entsteht (Inventar zeigt sie nur an).

## 2. Inventar-Regeln
- **Plätze:** Allgemeine Items **unbegrenzt**. Ausrüstung: 200 Plätze (`gear_inventory_slots`), **nie kaufbar**; bei vollem Inventar geht alles in die Post mit Ablaufhinweis (Dev UI). ⚠ Ablauf der Post nur für verdiente, unkaufbare Inhalte; gekaufte Inhalte in der Post verfallen nie (Law).
- **Stapel:** stack_max je Item (999/9.999/99.999; Ahnenzeichen 4.000 = `mark_bank_cap`); Ausrüstung, Truhen mit festem Inhalt, Kosmetik nicht stapelbar.
- **Sortierung:** Tabs Verbrauch · Materialien · Helden · Beschwörung · Truhen · Event · Kosmetik · Ausrüstung. Innerhalb: `sort_order`, dann Seltenheit absteigend, dann Name. Filter Epoche/Slot/Set bei Ausrüstung.
- **Verfall:** **nur** category `event` und nur, wenn `obtainable_purchase = no` und keine Quelle aus IAP/Kristallen (auch mittelbar Gekauftes zählt als gekauft). **Gekaufte Items verfallen nie.** Regel: Ende + 3 Tage, Restbestand automatisch zum **festen, vorab veröffentlichten Kurs** umgetauscht (nie nachträglich verschlechtert, mindestens Event-Shop-Wert).
  - Mammut-Trophäe: **1 Trophäe = 1 h Nahrung**, **max. 1 Umtausch pro Tag**, **kein Trophäen-Shop** (GDD Entsch. 74) → Kurs ist der einzige Wert, Law-Bedingung „≥ Shop-Wert“ entfällt. **Beim Verfall** wird der Rest automatisch in Nahrungskisten (je 1 h) umgewandelt, **max. 14 Stück**; beim Öffnen wird nur bis zum Lagerlimit aufgefüllt, der Rest bleibt als Kiste (`trophy_expiry_convert`, `_max`, `_fill_to_cap`).
  - Baumeister-Plakette: 1 Plakette = 1 Holzkiste (1 h).
  - Verfallshinweis + Kurs **vor Erhalt** sichtbar (Event-Info, Tooltip, Uhr-Chip); Countdown nur im Event, ohne Shop-Link.
- **Nutzen:** Einzeln/Mehrfach/„Alle verwenden“ mit Vorschau des Ergebnisses; Verbrauchsgüter werden nie automatisch eingesetzt.
- **Kein Handel/Verkauf** zwischen Spielern [GDD helden nicht handelbar, analog].

## 2b. Shops & Limits (aktueller Stand)
- Alle Shops (`guild_shop`, `arena_shop`, `event_shop`, `gem_shop`, `iap_products`) haben `daily_limit` (0 = keins) und `limit_reset` ∈ {daily, weekly, daily+weekly, once, monthly, per_event, per_epoch, per_season, none}; Reset `shop_limit_reset_time`.
- `event_shop.csv` zahlt nur in `cur_event_coin` (nie kaufbar, nicht aus Kristallen).
- Gear-Aufwertung und Artefaktstufen kosten Gold, Stein und Holz gemäß `gear_upgrade_costs.csv`; eine separate Schmiedewährung und tägliche Zusatzeinnahmen dafür gibt es nicht. Fortschrittsangebote im Gilden-/Arena-Shop verwenden bestehende Gildenmünzen bzw. Arena-Marken; Tageseinnahmen bleiben Gold und Materialien.
- Inventar: Limits wirken beim Kauf, nicht im Inventar – gekaufte/erhaltene Items stapeln normal und **verfallen nicht** wegen eines Limit-Resets. Verfall bleibt ausschließlich category `event` + unkaufbar.
- Limit-Text neutral „Heute noch X verfügbar.“, keine Countdowns/Knappheits-Optik.
- **Würfelbrett:** Glutuhr 15 min nur bei **Gratis-Würfen**, max. **3 je Event** (`dice_clock_field_rule`, `dice_clock_limit_per_event`); gekaufte Würfe nur Punkte; **keine Ausrüstung oder Artefakte** (`board_gear_rewards = none`).

## 2a. Validierungs-Anforderung (an Game Designer, validate.py nicht von mir geändert)
- `expires = yes` ⇒ `obtainable_purchase = no` und `source` ohne `iap`/Kristalle. Geprüft gegen items.csv v1.3: 0 Verstöße.
- Gear und Artefakte nicht aus `ev_stammeswettstreit`-Meilensteinen und nicht aus `ranking_rewards`.
- Vorschlag Code: `for x in L('items.csv'): chk(x['expires']!='yes' or (x['obtainable_purchase']=='no' and 'iap' not in x['source']),'Verfall nur unkaufbar '+x['item_id'])`

## 3. Truhen & Zufall (Law)
- Alle Truhen v1 haben **festen, vorab sichtbaren** Inhalt oder Wahl-Inhalt.
- Hard Rule: **Keine Kauf-Truhe mit Zufall ohne offen angezeigte Chancen.** Empfehlung v1 darüber hinaus: gar keine kaufbaren Zufallstruhen (Beschwörung bleibt einzige Zufallsmechanik → USK-/BE-Risiko nicht vergrößern; iap_products `random_content = no` [GDD]).
- **Checkliste Zufallstruhe (law-review-v1, Frage 3) – vor Implementierung, ohne Law-Freigabe kein Merge:**
  1. Spezifikation an Law: Inhalt, Wahrscheinlichkeiten (Summe 100 %), Quelle (verdient/kaufbar/Paket/Ticket), Preis €/Währung, Pity, Limits, Länder, Zielgruppe.
  2. Bevorzugt nur verdiente Währung; kaufbar/gekaufte Währung = Lootbox → Punkte 3–9 voll.
  3. Google Play: Chancen vor dem Kauf am Kauf-/Öffnen-Knopf (auch bei kostenlosen Truhen).
  4. Belgien: Flag aus (Store-Land serverseitig).
  5. Niederlande: Lage beobachten, Flag vorbereitet.
  6. USK/IARC: Deskriptor „In-Game-Käufe (+ zufällige Objekte)“, § 10b JuSchG bewerten.
  7. Pity/Garantie offenlegen, serverseitig; keine „nur noch X bis…“-Kaufbuttons.
  8. Minderjährige: keine Kaufappelle, u18-Limit, keine Pushs mit Shop-Link.
  9. Kein Echtgeld-/Sachgewinn, kein Handel (GlüStV).
  10. Doku: Raten versioniert (`random_content`, `odds_disclosed_required`), Ziehungen geloggt, validate-Check, Eintrag in ENTSCHEIDUNGEN.
  11. Ampel + Auflagen → Fabian entscheidet → Umsetzung → Abnahme durch Law vor Release.

## 4. Inventar-Screen (Dev UI)
| # | Frage | Antwort Dev UI |
|---|---|---|
| 1 | Eigener Screen? | ✓ eigener Screen, erreichbar über Menü bzw. Helden-Ausrüstung, Deep Link aus der Post; untere Tab-Leiste bleibt bei 5 Haupt-Tabs |
| 2 | 8 Tabs auf kleinen Displays | ✓ horizontal scrollbare Filter-Chips (`ui_filter_chip`) mit Icon + kurzem Label; unter 360 dp nur Icons |
| 3 | Kistenwert | ✓ primär konkrete Menge („+1.240 Holz“), „1 h“ als Zweitzeile; berechnet beim Öffnen des Screens |
| 4 | Überlauf | ✓ bei vollem Inventar alles in die Post mit Ablaufhinweis (gekaufte Inhalte ohne Ablauf, s. 2) |
| 5 | Badges | ✓ dezenter Punkt für neue Items, verschwindet nach dem Ansehen; kein Pulsieren, kein Countdown |
| 6 | Verfallsanzeige | ✓ Uhr-Chip mit Datum am Item + Zeile im Detail-Panel (inkl. Umtauschkurs); keine Shop-Verknüpfung |
| 7 | Icons | ✓ `icon_itm_<kategorie>_<id>`, 256 px; Seltenheit nur über Rahmen `ui_rarity_*`, nicht ins Icon eingebrannt → Spalte `icon_key` in items.csv |

## UI-Anbindung

Für Ausrüstung gelten die Pflichtaktionen und Anzeigezustände in `gear_qol_spec_v1.md`: Beste anlegen, Alle verbessern, Vergleichspfeile, Filter und optionales Auto-Zerlegen.

## Changelog
- **v1.6 (14.10.2026):** Grundsätze Kap. 0/0.2; Glutuhren `itm_clock_*` (itm_glut_* entfällt), `itm_dice_energy` verfällt nie, `itm_event_coin`; Shop-Limits `daily_limit`/`limit_reset`; Würfelbrett-Regeln; alle GDD-Items in items.csv übernommen; Minigame-ID mg_speerwurf (Entsch. 177).
- **v1.5 (14.10.2026):** Trophäen-Verfall → max. 14 Nahrungskisten, Öffnen bis Lagerlimit.
- **v1.4 (14.10.2026):** Trophäe ohne Shop, 1 Umtausch/Tag (Entsch. 74).
- **v1.7.2 (17.10.2026):** Gear-Inventar mit acht Slots; keine separate Schmiedewährung; Upgrade- und Zerlegekosten nur Gold/Stein/Holz; UI-QoL gemäß `gear_qol_spec_v1.md`.
- **v1 (14.10.2026):** Erstfassung.

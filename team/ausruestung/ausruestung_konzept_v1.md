# Ausrüstung & Artefakte – Konzept v1.7.2 (Epodarien)

Stand 17.10.2026. Aktive Tabellen: `equipment.csv`, `artifacts.csv`, `gear_slots.csv`, `gear_rarities.csv`, `gear_sets.csv`, `gear_upgrade_costs.csv`, `stat_definitions.csv`, `items.csv`, `game_config_ausruestung.csv`. Rechenregeln: `NOTES_v1.7.md`; UI-Pflichten: `gear_qol_spec_v1.md`.

## 0. Grundsätze

- Ausrüstung erweitert Helden um acht sichtbare Gear-Slots und bis zu zwei Artefaktslots. E1 hat Artefakt 1; Artefakt 2 wird erst ab E2 freigeschaltet.
- Alle Werte, Freischaltungen und Limits bleiben konfigurierbar. Ausrüstung und Artefakte sind nicht für Echtgeld oder Kristalle kaufbar.
- Das gesamte E1-Budget bleibt auf Faktor 1,127 begrenzt. Mehr Slots verteilen das vorhandene Budget, sie erhöhen es nicht.
- Es gibt keine separate Schmiedewährung. Ausrüstungsverbesserungen kosten Gold, Stein und Holz.

## 1. Slots und Freischaltungen

| Freischaltung | Slots | Garantierter Startgegenstand |
|---|---|---|
| camp_14 | Waffe, Rüstung | je 1 passendes Grob-Teil |
| camp_16 | Helm | 1 passendes Grob-Teil |
| camp_18 | Ring 1 | 1 passendes Grob-Teil |
| camp_20 | Beine | 1 passendes Grob-Teil |
| camp_22 | Schultern | 1 passendes Grob-Teil |
| camp_24 | Schuhe, Ring 2 | je 1 passendes Grob-Teil |
| camp_25 | Artefakt 1 | 1 fixes Start-Artefakt |
| Epoche 2 | Artefakt 2 | 1 fixes Start-Artefakt |

Die Gear-Slots sind Waffe, Rüstung, Helm, Schultern, Beine, Schuhe, Ring 1 und Ring 2. Jede aktive Slot-Freischaltung wird über `gear_slots.csv` und den jeweiligen `gear_unlock_slot_*`-Key gesteuert; `gear_slot_unlock_grants_item=1` schaltet die Garantieteile ein.

## 2. Wertebudget und Seltenheiten

Die Slot-Shares in `gear_slots.csv` summieren sich auf genau 100 %: acht Gear-Slots teilen 80 %, die beiden Artefaktslots je 10 %. Der E1-Referenzdeckel ist `ref_gear_factor_max_e1=1.127`; Hauptwerte werden mit `gear_main_value_mode=derived_from_budget` aus Share, Statgewicht, Rarität und Stufe abgeleitet. Es gibt keinen festen 4-%-Basiswert und keinen 12-%-Deckel je Gegenstand.

Für die Referenzrechnung gelten E1-Meister Stufe 9, `gear_stat_per_level_pct=5` sowie die Kampfgewichte ATK 0,5 und HP/DEF 0,25. Die gewichteten Setboni werden innerhalb des Gear-Anteils von 80 % reserviert. Formel und klassenspezifische Setreserve stehen in `NOTES_v1.7.md`.

| Seltenheit | Multiplikator | Maximalstufe | Freie Quelle |
|---|---:|---:|---|
| Grob | 1,00 | 10 | Kampagne; garantiert beim Gear-Slot-Unlock |
| Geschliffen | 1,20 | 15 | Kampagne ab camp_20 und Slot-Freischaltung |
| Meister | 1,32 | 20 | Kampagne ab camp_30 und Slot-Freischaltung |

Meister/Geschliffen beträgt bei gleicher Stufe 1,10. Der E1-Held erreicht mit acht maximalen Gearteilen, vollem 6er-Set und einem maximalen Artefakt höchstens Faktor **1,1143**. Das zweite Artefakt nutzt die verbleibenden 10 % erst ab E2.

## 3. Sets und Nebenwerte

Sets sind ab Geschliffen verfügbar und über die acht Gear-Slots verteilt. Alle Boni haben Schwellen bei 2, 4 und 6 Teilen. Die Summe je Set bleibt gleich wie im alten Modell:

| Set | Klassen | Bonus gesamt | Verteilung |
|---|---|---|---|
| Mammutfell | Infanterie/Speer | HP +3, DEF +4 | 2: HP +1/DEF +1; 4: HP +1/DEF +1; 6: HP +1/DEF +2 |
| Jägerzeichen | Fernkampf/Kavallerie | ATK +3, Krit +3 | je Schwelle ATK +1/Krit +1 |
| Ahnenglut | Support/Belagerung | DEF +3, Ult-CD +5 | 2: DEF +1/CD +1; 4: DEF +1/CD +2; 6: DEF +1/CD +2 |

Der Setfortschritt ist der spürbare Nebenwert für Helm, Schultern und Schuhe. Es gibt keine zufälligen Nebenwerte. Die bestehende Ult-CD-Untergrenze von 10 Sekunden bleibt aktiv.

## 4. Artefakte und Bindung

Ein Held trägt je einen Artefaktgegenstand pro freigeschaltetem Artefaktslot. `artifacts.csv` hält jeden Wert innerhalb des jeweiligen 10-%-Budgets; ATK/HP/DEF werden nach den Statgewichten bewertet. Signaturwerte sind relativ 5 % und bereits im Maximalbudget berücksichtigt.

Artefakte bleiben frei tauschbar, bis der Signaturbonus auf passender Rolle oder Epoche gebunden wird. Eine Signaturbindung sperrt den Tausch auf einen anderen Helden. Umbinden kostet `gear_artifact_rebind_cost_hours=1.5` Stunden Goldproduktion der aktuellen Epoche (`gear_artifact_rebind_cost_mode=gold_production_hours`). Jedes Artefakt hat `gear_artifact_rebind_free_per_artifact=1` kostenloses Umbinden. Es gibt keine Kristall- oder Echtgeldkosten.

## 5. Verbesserung, Aufwertung und Zerlegen

- Jede Stufe kostet ausschließlich Gold, Stein und Holz; Wachstum und Seltenheitskosten stehen in `gear_upgrade_costs.csv`.
- Verfeinerung Grob → Geschliffen kostet 800 Gold und 600 Stein. Geschliffen → Meister kostet 2.500 Gold und 1.800 Stein; die Stufe bleibt erhalten.
- Artefaktstufen kosten Gold. Gear-Stufe ist durch `gear_level_cap_rule=center_level_minus_1` begrenzt.
- Zerlegen erstattet `gear_dismantle_refund_pct=100` Prozent der Gold-, Stein- und Holzkosten. Ein zusätzlicher Markenbonus entfällt.
- Schmiede-Angebote nutzen vorhandene Gildenmünzen oder Arena-Marken. Tageseinnahmen für Fortschritt laufen über Gold und Materialien.
- Die Warnung `forge_reserve_warning=1` zeigt den Ressourcenbedarf für das nächste Häuptlingsfeuer, ohne die Schmiede zu sperren.

## 6. Quellen und Inventar

Grobteile kommen aus der Kampagne und den Slot-Garantien. Geschliffene Teile beginnen ab camp_20; Meisterstücke ab camp_30. Artefakte stammen aus den festen Kampagnen-, Event-, Gilden- und Arenaquellen in `artifacts.csv`. Keine Ausrüstung kommt aus kaufbar beschleunigten Ranglisten- oder Stammeswettstreit-Meilensteinen.

`gear_inventory_slots=200`; Ausrüstungsplätze sind nicht kaufbar. Bei Überlauf geht der Gegenstand in die Post. Ablaufregeln gelten nur für verdiente, unkaufbare Inhalte; gekaufte Inhalte verfallen nicht. Filter, Sortierung und Auto-Zerlegen stehen in `item_system_v1.md` und `gear_qol_spec_v1.md`.

## 7. Dev UI – Pflichtumfang v1

`gear_qol_required` verlangt Beste anlegen (Held und Formation), Alle verbessern, Vergleichspfeile, Inventarfilter und Auto-Zerlegen. Die konkreten Eingaben, Ausschlüsse, Bestätigungen und Konfigurationskeys sind in `gear_qol_spec_v1.md` festgelegt.

## 8. Kampfkraft und PvP

Ausrüstungsfaktor: `1 + Ø über Formationshelden (0,5 × ATK % + 0,25 × HP % + 0,25 × DEF %)`. Kein zusätzlicher Epochenbonus für Ausrüstung; `epoch_bonus_pct` wirkt nach additiven Boni multiplikativ.

Im PvP gelten `gear_pvp_cap_pct=40`, `gear_crit_cap_pct=25`, `battle_heal_cap_pct=40` sowie die Ult-CD-Untergrenze von 10 Sekunden. Bei Kürzung werden Gear, Set und Artefakt in dieser Reihenfolge reduziert. Normierte Modi verwenden die konfigurierten Budget-Shares statt einer festen Basis pro Teil.

## 9. Monetarisierung und Shops

Ausrüstung, Artefakte und Verbesserungen sind nicht für Echtgeld oder Kristalle kaufbar. Shops für Fortschrittsmaterial verwenden Gildenmünzen beziehungsweise Arena-Marken. Ausrüstungsskins bleiben rein kosmetisch (`power_bonus=0`); Preisvorschläge stehen in `cosmetic_products_vorschlag.csv`. Keine Kauf- oder Countdown-Popups nach Niederlagen und keine Shop-Links in Warn- oder Ergebnisbildschirmen.

## 10. Abnahmestand v1.7.2

- Slots: 10 aktive Einträge, davon 8 Gear und 2 Artefakte; Sharesumme 100 %.
- E1: 9 ausgerüstete Einträge verfügbar; Faktor höchstens 1,127, mit dem berechneten Maximalbuild 1,1143.
- Rarität: Meister/Geschliffen = 1,10 bei gleicher Stufe.
- Sets: 2/4/6; Gesamtwerte unverändert; höchstens 6 benötigte Teile.
- Unlocks und Garantieteile folgen der Tabelle in Abschnitt 1.
- Finanzen: Rebind 1,5 Stunden aktueller Epochen-Goldproduktion, 1 Gratisumbinden je Artefakt; keine separate Schmiedewährung.
- UI-QoL: alle fünf Funktionen sind v1-Pflicht.

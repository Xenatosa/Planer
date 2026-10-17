# Ausrüstung & Artefakte – Konzept v1.7.2 (Epodarien)

Stand 17.10.2026. Aktive Tabellen: `equipment.csv`, `artifacts.csv`, `gear_slots.csv`, `gear_rarities.csv`, `gear_sets.csv`, `gear_upgrade_costs.csv`, `stat_definitions.csv`, `items.csv`, `game_config_ausruestung.csv`. Rechenregeln: `NOTES_v1.7.md`; UI-Pflichten: `gear_qol_spec_v1.md`.

## 0. Grundsätze

- Acht sichtbare Gear-Slots und bis zu zwei Artefaktslots. E1 hat Artefakt 1; Artefakt 2 wird erst ab E2 freigeschaltet.
- Werte, Freischaltungen und Limits bleiben konfigurierbar. Ausrüstung und Artefakte sind nicht für Echtgeld oder Kristalle kaufbar.
- Der E1-Gesamtdeckel ist Faktor 1,127. Die zehn Slot-Shares verteilen dieses Budget; zusätzliche Slots erhöhen es nicht.
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
| camp_25 | Artefakt 1 | 1 fixes Start-Artefakt (`art_e1_firestone`) |
| Epoche 2 | Artefakt 2 | 1 fixes Start-Artefakt (`art_e2_atk_focus`) |

Jede Gear-Slot-Freischaltung gibt ein passendes Grob-Teil. Artefakt-Slots geben das konfigurierte feste Start-Artefakt. Die acht Gear-Slots sind Waffe, Rüstung, Helm, Schultern, Beine, Schuhe, Ring 1 und Ring 2.

## 2. Wertebudget und Seltenheiten

Die Slot-Shares in `gear_slots.csv` summieren sich auf genau 100 %: acht Gear-Slots teilen 80 %, die beiden Artefaktslots je 10 %. Hauptwerte werden über `gear_main_value_mode=derived_from_budget` aus Anteil, Statgewicht, Seltenheit und Stufe abgeleitet. Es gibt keinen festen 4-%-Basiswert und keinen 12-%-Deckel je Gegenstand.

| Seltenheit | Rohmultiplikator | Maximalstufe | Freie Quelle |
|---|---:|---:|---|
| Grob | 1,00 | 10 | Kampagne; garantiert beim Gear-Slot-Unlock |
| Geschliffen | 1,20 | 15 | Kampagne ab camp_20 und Slot-Freischaltung |
| Meister | 1,40 | 20 | Kampagne ab camp_30 und Slot-Freischaltung |

Die E1-Referenz ist Meister Stufe 9 (Feuer 10 minus 1); ein voll ausgerüsteter E1-Held erreicht mit acht Gearteilen, aktivem 6er-Set und maximalem Artefakt 1 höchstens Faktor **1,114300**. Der Gesamtdeckel bleibt 1,127. Für E2 gilt `e2_center_max_level=15`, also maximal Gear-Stufe 14. Mit acht Meisterteilen Stufe 14, aktivem 6er-Set und zwei maximalen Artefakten beträgt der höchste CSV-Faktor **1,143804**, unter dem bindenden Deckel `ref_gear_factor_max_e2=1.16`.

Die 1,15-Grenze wird aus der Helden-Fairnessregel **SSR ≤ 1,15 × SR** übernommen (`team/helden/Helden-System_v1.md`). Sie begrenzt hier das Verhältnis der Gesamt-Statfaktoren eines voll ausgerüsteten Meister- und Geschliffen-Helden. Geprüft wird `(1 + B_master) / (1 + B_fine)`; die Rohmultiplikatoren 1,40 und 1,20 werden nicht direkt ins Verhältnis zur Grenze gesetzt. Mit E1-Budget 0,127 und E2-Budget 0,16 liefert die konservative Formel `(1+B)/(1+B×1,20/1,40)` 1,0164 beziehungsweise 1,0201. Die konkrete Rechnung mit festen Set- und Artefaktwerten bleibt darunter.

Formel, Setreserve und Detailwerte stehen in `NOTES_v1.7.md`.

## 3. Sets und Nebenwerte

Sets sind ab Geschliffen verfügbar und über die acht Gear-Slots verteilt. Alle Boni haben Schwellen bei 2, 4 und 6 Teilen. Die Summe je Set bleibt gleich wie im alten Modell:

| Set | Klassen | Bonus gesamt | Verteilung |
|---|---|---|---|
| Mammutfell | Infanterie/Speer | HP +3, DEF +4 | 2: HP +1/DEF +1; 4: HP +1/DEF +1; 6: HP +1/DEF +2 |
| Jägerzeichen | Fernkampf/Kavallerie | ATK +3, Krit +3 | je Schwelle ATK +1/Krit +1 |
| Ahnenglut | Support/Belagerung | DEF +3, Ult-CD +5 | 2: DEF +1/CD +1; 4: DEF +1/CD +2; 6: DEF +1/CD +2 |

Der Setfortschritt ist der spürbare Nebenwert für Helm, Schultern und Schuhe. Es gibt keine zufälligen Nebenwerte. Krit ist auf 25 % gedeckelt; Ult-CD kann nicht unter 10 Sekunden fallen. Beide Werte sind aus dem Gear-Kampfkraftbudget ausgeschlossen.

## 4. Artefakte und Bindung

Jeder Artefaktslot nutzt 10 % des Gesamtbudgets. ATK/HP/DEF-Werte berücksichtigen den 5-%-Signaturbonus bereits innerhalb dieses Limits: bei maximaler Stufe höchstens 1,27 gewichtete Faktor-Prozentpunkte je Artefakt. Die Startwerte für E2 sind ATK 1,209524 → 2,419048 sowie HP und DEF 2,419048 → 4,838095. Damit bleibt auch E2 mit zwei Artefakten und Gear bis Stufe 14 unter Faktor 1,16.

Artefakte bleiben frei tauschbar, bis der Signaturbonus auf passender Rolle oder Epoche gebunden wird. Danach kostet das Umbinden `gear_artifact_rebind_cost_hours=1.5` Stunden Goldproduktion der aktuellen Epoche. Jedes Artefakt hat ein kostenloses Umbinden. Es gibt keine Kristall- oder Echtgeldkosten.

## 5. Verbesserung, Aufwertung und Zerlegen

- Jede Stufe kostet ausschließlich Gold, Stein und Holz; Wachstum und Seltenheitskosten stehen in `gear_upgrade_costs.csv`.
- Verfeinerung Grob → Geschliffen kostet 800 Gold und 600 Stein. Geschliffen → Meister kostet 2.500 Gold und 1.800 Stein; die Stufe bleibt erhalten.
- Gear-Stufe ist durch `gear_level_cap_rule=center_level_minus_1` begrenzt: E1 höchstens 9, E2 höchstens 14.
- Zerlegen erstattet `gear_dismantle_refund_pct=100` Prozent der Gold-, Stein- und Holzkosten.
- Schmiede-Angebote nutzen vorhandene Gildenmünzen oder Arena-Marken. Die Warnung `forge_reserve_warning=1` zeigt den Bedarf für das nächste Häuptlingsfeuer, ohne die Schmiede zu sperren.

## 6. Quellen und Inventar

Grobteile kommen aus der Kampagne und den Slot-Garantien. Geschliffene Teile beginnen ab camp_20; Meisterstücke ab camp_30. Die E2-Startartefakte werden beim Freischalten von Slot 2 ausgegeben; weitere Artefakte stammen aus den festen Kampagnen-, Event-, Gilden- und Arenaquellen in `artifacts.csv`. Keine Ausrüstung kommt aus kaufbar beschleunigten Ranglisten- oder Stammeswettstreit-Meilensteinen.

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
- E1: acht Gearteile und Artefakt 1; Maximalfaktor 1,114300 ≤ 1,127.
- E2: Feuer max. 15, Gear max. 14; acht Gearteile und zwei Artefakte; Maximalfaktor 1,143804 ≤ 1,16.
- Rarität: Meister 1,40, Geschliffen 1,20; Gesamtfaktor-Ratio nach Referenzformel E1 1,0164 und E2 1,0201, jeweils ≤ 1,15.
- Sets: 2/4/6; Gesamtwerte unverändert; höchstens 6 benötigte Teile.
- Freischaltungen und Startgegenstände folgen Abschnitt 1.
- Finanzen: Verbesserungen nur Gold/Stein/Holz; Umbinden 1,5 Stunden aktueller Epochen-Goldproduktion, 1 Gratisumbinden je Artefakt.
- UI-QoL: alle fünf Funktionen sind v1-Pflicht.

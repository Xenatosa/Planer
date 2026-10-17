# Ausrüstung v1.7 – Rechen- und Datenhinweise

## Hauptwerte und Budget

`ref_gear_factor_max_e1 = 1.127` setzt das verfügbare E1-Kampfkraftbudget auf 12,7 Prozentpunkte. Die 10 aktiven Slot-Shares in `gear_slots.csv` ergeben 100 %. E1 hat neun ausrüstbare Slots (acht Gearteile und Artefakt 1), also höchstens 90 % des Budgets: Faktor 1,1143.

Für Gear entfallen 80 % des Gesamtbudgets auf acht Teile. Die gewichteten 6er-Setboni werden innerhalb dieses Gear-Anteils reserviert. Der Hauptwert eines Teils wird pro Klasse und Slot so berechnet:

`main_stat_base_pct = (12.7 × slot_share × class_scale / stat_weight) / (master_mult × level_mult_e1)`

`level_mult_e1 = 1 + 0.05 × (9 − 1) = 1.4`; `master_mult = 1.32`; `stat_weight` ist ATK 0,5, HP/DEF 0,25. `class_scale = (0.127 × 0.80 − set_factor_pct/100) / (0.127 × 0.80)`. Die Setreservierung beträgt Mammutfell 1,75 Faktor-Pp, Jägerzeichen 1,50 Pp und Ahnenglut 0,75 Pp. Sie wird pro rata auf die acht Gear-Shares verteilt: Hauptwert plus zugerechneter Setanteil je Slot ergibt wieder genau dessen Share. Hauptwerte plus aktiver 6er-Setbonus bleiben zusammen innerhalb der 80 % Gear-Anteil.

Artefakt 1 kann höchstens 10 % des Gesamtbudgets beitragen. Bei ATK/HP/DEF wird der Rohwert durch das jeweilige Statgewicht geteilt; der +5-%-Signaturbonus ist bereits in diesem Limit berücksichtigt. Andere Artefaktwerte bleiben ebenfalls unter einem Rohwert von 1,27 Pp. Artefakt 2 belegt die verbleibenden 10 % erst ab E2.

Die feste Raritätskurve ist Grob 1,00, Geschliffen 1,20 und Meister 1,32. Bei gleicher Stufe ist Meister/Geschliffen damit genau 1,10. Die alte feste 4-%-Basis und der 12-%-Deckel pro Teil werden nicht mehr verwendet.

## Sets und kleine Slots

Setwerte bleiben in Summe unverändert und werden auf 2/4/6 Teile verteilt. Der Setfortschritt über mehrere Slots ist der spürbare Nebenwert für Helm, Schultern und Schuhe; es gibt keine zufälligen Nebenwerte. Die maximalen 6 Setstücke passen in die acht Gear-Slots.

## Freischaltungen und Bindung

Aktive Reihenfolge: camp_14 Waffe/Rüstung, camp_16 Helm, camp_18 Ring 1, camp_20 Beine, camp_22 Schultern, camp_24 Schuhe/Ring 2, camp_25 Artefakt 1, Artefakt 2 ab E2. Jede Gear-Slot-Freischaltung gibt ein passendes Grob-Teil; beim Artefaktslot gibt es ein fixes Start-Artefakt.

Artefakte sind frei tauschbar, bis ein Signaturbonus auf passender Rolle/Epoche gebunden wird. Danach kostet das Umbinden 1,5 Stunden Goldproduktion der aktuellen Epoche. Jede Artefakt-ID hat ein kostenloses Umbinden. Es gibt keine Kristall- oder Echtgeldkosten.

## Kosten und UI-Pflichten

Gear-Aufwertung bezahlt nur Gold, Stein und Holz. Zerlegen erstattet 100 % dieser drei Ressourcen. Die Schmiede hat keine separate Markenwährung oder tägliche Markeneinnahme. Shop-Angebote verwenden die bestehenden Gildenmünzen beziehungsweise Arena-Marken.

`gear_qol_required` ist v1-Pflicht: Beste anlegen für Held und Formation, Alle verbessern bis zum verfügbaren Kostenlimit, Vergleichspfeile, Inventarfilter und optionales Auto-Zerlegen für Grob. Details stehen in `gear_qol_spec_v1.md`.

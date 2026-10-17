# Gear-QoL-Spec v1 – Dev UI

Alle Punkte sind v1-Pflicht (`gear_qol_required`). Die jeweilige Funktion muss auf Touch-Geräten ohne Einzelverwaltung jedes Ausrüstungsteils bedienbar sein.

## Beste anlegen

- **Held:** bewertet alle passenden, freien Gegenstände für jeden freigeschalteten Slot und legt die Kombination mit dem höchsten berechneten Machtwert an. Setfortschritt und Signaturbindung fließen in die Bewertung ein. Bereits gebundene Signatur-Artefakte bleiben beim gebundenen Helden.
- **Formation:** berechnet die beste legale Verteilung für alle Formationshelden gemeinsam. Ein Gegenstand oder Artefakt kann nie gleichzeitig zwei Helden zugewiesen sein.
- Ergebnisvorschau zeigt die Nettoänderung je Held und Formation. Anwenden erfolgt mit einer Bestätigung; es gibt kein Goldlimit, da Anlegen nichts kostet.
- Config: `gear_auto_equip=best_equip_hero;best_equip_formation`.

## Alle verbessern

- Verbessert angelegte Teile schrittweise nach priorisierter Auswahl, bis Gold, Stein oder Holz für den nächsten Schritt nicht mehr reicht oder die Stufenobergrenze erreicht ist.
- Vor dem Start stehen Gesamtverbrauch je Ressource und die betroffenen Teile in einer Vorschau. Der Spieler kann abbrechen oder bestätigen.
- Nie werden Kristalle, Echtgeld oder Shop-Artikel verwendet. Die Reserve-Warnung für das nächste Häuptlingsfeuer bleibt sichtbar.
- Config: `gear_bulk_upgrade=all_up_to_gold_limit`; die Implementierung stoppt ebenfalls bei zu wenig Stein oder Holz.

## Vergleichspfeile

- Grün zeigt einen positiven und Rot einen negativen Nettovergleich mit dem aktuell ausgerüsteten Teil.
- Verglichen werden Hauptwert, Setstufe, Signaturstatus und die resultierende Machtänderung. Der Pfeil ersetzt keine Zahlenvorschau.
- Config: `gear_compare_arrows=green_upgrade;red_downgrade`.

## Inventarfilter

- Filter nach Slot, Seltenheit, Set, Epoche und Stufe; Sortierung nach Macht, anschließend Seltenheit und Name.
- Bereits ausgerüstete, gebundene und gesperrte Gegenstände sind erkennbar. Freie Teile können direkt über die Liste verglichen werden.
- Config: `gear_inventory_filter=slot;rarity;set;epoch;level;power`; Kapazität `gear_inventory_slots`.

## Auto-Zerlegen

- Grobe Teile können automatisch zerlegt werden. Funktion ist standardmäßig aus und muss vom Spieler ausdrücklich aktiviert werden.
- Geschliffene/Meisterteile, angelegte Teile, Setstücke und Signatur-Artefakte sind ausgeschlossen. Vor Aktivierung erscheint eine Bestätigung mit der Rückerstattung von Gold, Stein und Holz.
- Config: `gear_auto_salvage=gr_common;off_by_default;confirm`; Rückerstattung `gear_dismantle_refund_pct`.

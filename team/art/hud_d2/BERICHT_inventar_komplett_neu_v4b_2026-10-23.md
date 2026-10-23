# Inventar v4b · Kurzbericht

## Was neu ist

- Die Inventarübersicht zeigt Tabs, Suche, Sortierung, Kartenraster und Lagerkapazität. Das feststehende Detailpanel und sein Aktionsknopf sind entfernt.
- Das Raster nutzt vier vollständige Kartenreihen im sichtbaren Bereich. Die Gegenstandsbilder sind auf 84 px verkleinert; das entspricht rund 67 % der Breite ihres 126-px-Bildfelds.
- Ein Tipp auf eine Karte öffnet ein modales Detailsheet mit großem Bild, Seltenheit und Werten. Ausrüstung zeigt **ANLEGEN**, Ressourcen und Verbrauchsgüter **VERWENDEN**. Fragmente zeigen ihren Sammelfortschritt ohne Aktionsknopf.
- Das Sheet schließt über X, Zurück, Außentipp oder Escape. D2-Hallenbühne, Scrim, Ressourcenleiste und aktives Inventar-Dock bleiben erhalten.
- Maßplan und drei Keyframes wurden aktualisiert.

## Prüfung

- Die Keyframes Alle, Ausrüstung und Detailsheet wurden mit Chrome gerendert und auf **1080 × 1920 px** geprüft.
- Interaktion im Headless-Chrome geprüft: Übersicht ohne sichtbares Detail/CTA, Ausrüstung öffnet mit **ANLEGEN**, Ressource mit **VERWENDEN**, Fragment mit **12 / 80** und verborgenem Aktionsknopf; X und Zurück schließen das Sheet.
- `git diff --check` ist sauber.

## Kosten

- **0 $ Bildgenerierung.** Vorhandene D2-Sprites, Equip-Icons, Schriften und Lagerhallen-Hintergrund wurden wiederverwendet.

DONE · 2026-10-23 20:49:36 CEST (Europe/Berlin)

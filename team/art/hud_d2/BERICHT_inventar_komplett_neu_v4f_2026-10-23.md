# Inventar v4f · Zerlegen im Detailsheet

## Was neu ist

- Das Detailsheet hat jetzt neben dem typabhängigen Primärknopf einen klar sekundären **ZERLEGEN**-Knopf.
- Die Vorschau nennt **+12 Schrott · für den Shop**. Im HTML-Prototyp bestätigt ein kurzer Toast die Aktion.
- Ausrüstung behält **ANLEGEN**, Ressourcen und Verbrauch behalten **VERWENDEN**. Fragmente zeigen weiterhin den Fortschritt ohne Aktionsknöpfe.
- Das v4e-Raster, seine fünf Spalten, die Karten, Tabs, Dock, Ressourcenleiste und Übersicht bleiben unverändert.

## Prüfung

- Detailsheet neu mit Chrome gerendert und visuell kontrolliert; PNG ist **1080 × 1920 px**.
- Interaktion geprüft: Zerlegen zeigt den Schrott-Toast; Ausrüstung zeigt **ANLEGEN**, Ressourcen **VERWENDEN**, Fragmente Fortschritt ohne Aktionsleiste.
- Fünf Rasterspalten im HTML geprüft. Die PNGs für Alle und Ausrüstung blieben byte-identisch.
- `git diff --check` ist sauber.

## Kosten

0 $ · vorhandene D2-Sprites und HTML/CSS verwendet, keine Bildgenerierung.

DONE · 2026-10-23 21:23 CEST (Europe/Berlin)

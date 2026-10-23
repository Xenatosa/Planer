# Bericht · Mail v7b Detail-Sheet

**DONE · 2026-10-23 21:41 CEST (Europe/Berlin)**

- Nachrichtenkarten öffnen ein modales Detail-Sheet mit Absender, Zeit und vollständigem Nachrichtentext; das Beispiel enthält drei Absätze.
- System-Mails zeigen Belohnungen und Annahmestatus im Sheet. Die Belohnung kann dort angenommen werden.
- Spieler-Mails zeigen den vollständigen Text ohne Belohnungsmodul.
- Schließen per X, Zurück-Schaltfläche, Außenbereich oder Escape; nach dem Schließen erhält die Karte wieder den Tastaturfokus.
- Neue Vorschau `vorschau_overlay_mail_d2_v7_detail.png` mit System-Langtext und offener Belohnung.
- Maßplan und Fenster-Scope aktualisiert. Die drei bestehenden v7-Listen-PNGs blieben unverändert, da sich das Listenlayout nicht geändert hat.
- Keine neue Bildgenerierung; 0 $ Bildgenerierung.

## Prüfung

- Detail-PNG: 1080 × 1920 px, drei Absätze vollständig lesbar.
- HTML: System- und Spielerkarte öffnen; X, Zurück, Außenbereich und Escape schließen; System-Belohnung im Sheet annehmen.
- `git diff --check` sauber.

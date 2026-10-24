# Bericht · Chat-Fenster D2 v1

**Status: DONE · 24.10.2026**

## Ausgabe

- `vorschau_menu_chat_d2_v1.png` und `vorschau_menu_chat_d2_v1_optionen.png` — je 576×1024 px
- `render_vorschau_menu_chat_d2_v1.py` — Renderer für Haupt- und Optionen-Screen

Der Hauptscreen zeigt den Welt-Reiter mit ungelesenen Badges, freundliche einspaltige Nachrichten, eine dezente Eventmeldung sowie Emote-, Eingabe- und Senden-Steuerung. Der Optionen-Screen öffnet das Spieler-Sheet für Profil, Privatnachricht, Stummschalten, Melden und rot markiertes Blockieren.

Die Meldeauswahl zeigt den konkreten Weltchat-Bezug, Gründe für Regelverstöße und möglicherweise rechtswidrige Inhalte, ein erforderliches Begründungsfeld, die Bestätigung zu Richtigkeit und Vollständigkeit sowie die übermittelten Absenderdaten. „Meldung senden“ bleibt bis zur Auswahl und Bestätigung deaktiviert. Der Ablauf bildet die Eingabeelemente aus Art. 16 Abs. 2 DSA ab; die Umsetzung des gesamten Melde- und Moderationsprozesses ist nicht Teil dieser Vorschau.

## GDD-Abgleich und Sichtprüfung

Das neueste GDD `team/gdd/kernvision_fabian.md` betont gemeinschaftliches Zusammenspiel, ohne Chat- oder Meldevorgaben. Der kooperative, ruhige Beispielchat passt dazu. Gold bleibt UI-Akzent; im HUD wird die Goldwährung als Muscheln gezeigt.

Renderer erfolgreich ausgeführt. Beide PNGs wurden bei 100 % sowie an allen vier Kanten mit 300%-Crops geprüft; Rahmen, Text, Badges, Chat-Inhalt, Sheet und Dock bleiben vollständig im Bild.

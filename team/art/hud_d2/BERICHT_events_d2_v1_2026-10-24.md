# Events-Fenster D2 v1

## Grundlage

- Maßgeblich: `/workspace/handygame-plan/team/gdd/GDD_v1.6.13.md`, insbesondere Kapitel 25.7 und 26.
- Kalenderdetails: `/workspace/handygame-plan/team/events/event_kalender_soft_launch_3m.md` und `/workspace/handygame-plan/team/events/event_calendar.csv`.
- Verbindliche Stilregel: `/workspace/handygame-plan/team/art/GUELTIG.md`.
- Stil: freigegebene D2-Vorschauen Quests v2b und Shop v1c; HUD-Assets aus `team/art/hud_d2/icons_v1/`.
- Die Kalenderdaten enthalten relative Tage, aber kein absolutes Startdatum. Der gezeigte Woche-4-Snapshot setzt Woche 1 auf Montag, 28.09.2026; daraus folgen die dargestellten Startdaten.

## Inhalt

- Übersicht mit einzeln breiten Event-Zeilen, aktivem Stammeswettstreit, Helden-Festival und den nächsten Starts für Kriegsmammut, Turnier, Baumeister und Würfel-Event.
- Detailansicht des Stammeswettstreits mit den vier GDD-Aufgaben, 25 Punkten je Aufgabe, 2.000–30.000-Punkte-Meilensteinen und den zugehörigen Festmünzen.
- Klarer Hinweis: Für Rang und Festmünzen zählen nur Gratis-Versuche. Keine Shop-Angebote auf dem Ranglisten-Event-Bildschirm.
- Der globale Goldbestand bleibt im freigegebenen HUD als Muscheln dargestellt; Festmünzen stehen als getrennte Event-Währung.

## Prüfung

- Beide PNGs: 576×1024 RGBA.
- Sichtprüfung bei 100 % und 300%-Crops aller vier Kanten: keine abgeschnittenen Texte, Symbole oder Rahmen.
- Panel endet direkt vor dem inaktiven Dock; Zurück-Pfeil und Statuspunkte sind sichtbar.
- Renderer: `_src/render_vorschau_menu_events_d2_v1.py`.

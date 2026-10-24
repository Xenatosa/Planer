# Mail / Postfach D2 v7 · Maßplan

**Status:** neuer Vollbild-Aufbau · 1080 × 1920 px · CSS-Referenzcanvas 1:1
**Stil:** D2 Obsidian & Glut, Comic-Schrift, warme Systempost und kühler Spielerchat.
**Quelle:** `team/art/ui-kit/menus_v3/_src/html/v3_2_obsidian_mail_v7_interaktiv.html`
**Hintergrund:** bestehende `bg_menu_mail_comic_v1.png`, per Cover eingepasst; schwarzer Scrim mit 70 % Grunddeckung (≥62 %).
**Navigation:** Dock A, Dorf aktiv. Top-Ressourcen wie Inventar/Beschwören.

## Canvas-Zonen

| Zone | x | y | Breite | Höhe | Funktion |
|---|---:|---:|---:|---:|---|
| Hintergrund/Scrim | 0 | 0 | 1080 | 1920 | Comic-Schriftstube, Scrim 70 % + Randabdunklung |
| Ressourcenleiste | 30 | 18 | 1020 | 92 | Kristall, Plus, Wissen, Gold |
| Kopf | 30 | 128 | 1020 | 112 | Zurück, POSTFACH, ungelesen/offene Belohnungen, Schließen |
| Tab-Leiste | 30 | 255 | 1020 | 126 | SYSTEM und SPIELER, je 503 × 126, Badge für ungelesen |
| Aktionen | 30 | 397 | 1020 | 184 | ALLES GELESEN + ALLE GELESENEN LÖSCHEN, Gate-Erklärung |
| Listen-Kopf | 42 | 596 | 996 | 36 | Bereichstitel und Anzahl |
| Nachrichtenliste | 30 | 640 | 1020 | 1013 | kompakte scrollbare Karten, Dock-Abstand 27 px |
| Dock A | 0 | 1680 | 1080 | 240 | Dorf · Helden · Karte · Armee · Gilde · Inventar |
| Modal-Scrim | 0 | 0 | 1080 | 1920 | rgba(4,3,3,.72); dimmt Liste, Kopf, Tabs und Dock |
| Mail-Detail-Sheet | 38 | 430 | 1004 | 950 | Dialog mit Absender/Zeit, vollem Text, optionaler Belohnung und Aktionen |

## Nachrichtenkarten

| Variante | Außenmaß | Aufbau | Status / Aktion |
|---|---:|---|---|
| System mit Belohnung | 1016 × 205 | Siegel-Emblem 104 × 104 links; rechts Titel, Absender/Zeit, Kurztext, Belohnungs-Chips | UNGELESEN / BELOHNUNG HOLEN oder ANGENOMMEN |
| System ohne Belohnung | 1016 × 184 | Siegel-Emblem 104 × 104 links; rechts Titel, Metazeile, Kurztext | UNGELESEN oder GELESEN |
| Spieler-Chat | 1016 × 192 | Avatar 94 × 94 links; rechts Betreff, Kontakt/Zeit und Chatblase | UNGELESEN oder GELESEN |
| Listenabstand | — | 12 px zwischen Karten; scrollbarer Innenbereich | fünf Beispielnachrichten pro Tab |

Je fünf Nachrichten sind ohne Scrollen sichtbar. Systemkarten nutzen Bronze/Glut, Siegel-Embleme und eingebaute Belohnungszeile. Spielerkarten nutzen kühle Türkis-/Petrolflächen, runde Avatare und Chatblasen. Der Unterschied bleibt auch ohne Lesen der Tab-Titel sichtbar.

## Interaktionen und Regeln

- **SYSTEM / SPIELER:** wechseln den Listeninhalt; die Zähler zeigen ungelesene Nachrichten des jeweiligen Tabs.
- **ALLES GELESEN:** markiert beide Postfächer als gelesen und setzt alle System-Belohnungen auf angenommen.
- **BELOHNUNG HOLEN:** nimmt eine einzelne System-Belohnung an und markiert die Nachricht als gelesen.
- **ALLE GELESENEN LÖSCHEN:** bleibt gesperrt, solange eine Nachricht ungelesen oder eine System-Belohnung offen ist. Bei null ungelesenen Nachrichten und null offenen Belohnungen werden nur gelesene Nachrichten mit angenommenen Belohnungen entfernt.
- **Karte antippen:** öffnet das Detail-Sheet. Systemtexte können mehrere Absätze enthalten; Belohnung und Annahmestatus bleiben im Sheet sichtbar. Spielerpost zeigt den vollständigen Nachrichtentext ohne Belohnungsmodul.
- **Detail-LÖSCHEN:** entfernt nur die geöffnete Nachricht und schließt das Sheet; bei Systempost steht es nach „BELOHNUNG HOLEN“, vor „ZURÜCK“.
- **Schließen:** X, „ZURÜCK“, Kopf-Zurück, Escape oder Tipp auf den abgedunkelten Außenbereich; Fokus geht zur geöffneten Karte zurück.
- Renderer-Zustände: `?view=system`, `?view=player`, `?view=read` und `?view=detail`.

## Farb- und Typotokens

| Verwendung | Wert |
|---|---|
| Grundfläche / Karte | `#0B0908` / `#17110E` |
| Haupttext / Sekundärtext | `#F7EAD2` / `#B9A988` |
| System-Akzent | `#FF8A2A`, `#FFC06A`, Bronze `#C98A4A` |
| Spieler-Akzent | Türkis `#4BD2C8`, Mint `#A0FFF1`, Petrol `#123638` |
| Gelesen / angenommen | `#A9E586` |
| Display / Fließtext | Lilita One / Baloo 2 |

## Ausgaben

- `vorschau_overlay_mail_d2_v7.png` — System, ungelesene Post + offene Belohnung.
- `vorschau_overlay_mail_d2_v7_spieler.png` — Spieler-Tab im Chat-Look.
- `vorschau_overlay_mail_d2_v7_gelesen.png` — Post gelesen, Belohnungen angenommen, Löschen aktiv.
- `vorschau_overlay_mail_d2_v7_detail.png` — geöffnete System-Mail mit drei lesbaren Absätzen und offener Belohnung.

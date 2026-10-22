# Icon-Liste Dorf-HUD D2 v1 (Basis: Massplan v6.3)

Stand: 22.10.2026. Erzeugt von `_src/icon_liste_hud_d2_v1.py`, Übersicht als `icon_liste_hud_d2_v1.png`.
Insgesamt 60 Icon-Dateien, davon P1 55 (nötig für das HUD) und P2 5 (später).
Rahmen, Pills, Buttons, Dock-Platten und Dropdowns sind keine Icons; sie kommen aus dem D2-Sprite-Set „Obsidian & Glut“ und sind hier nicht enthalten.

## Stil (gilt für alle)
- **Epoche 1 Steinzeit**: Materialien sind Stein, Obsidian, Holz, Leder, Fell, Knochen, Muscheln und Pflanzenfasern. Kein Metall, keine Schrift.
- **D2 „Obsidian & Glut“**: warme Grundtöne, Akzente in leuchtendem Glutorange (#FFB347 / glut.plus #FFD27A). Kühles Mondtürkis (#3FE0D0) nur für Magisches (Ahnen).
- **Comic-Stil**, reich detailliert wie Clash of Clans, nicht flach: Volumen mit 3 Tonstufen, ein Glanzlicht und Materialtextur.
- **Licht** immer von oben links. Eigenschatten nach unten rechts, kein Schlagschatten auf den Boden.
- **Outline**: dunkelbraun (#1A120C), 6 px bei 256-px-Master (ca. 2 px im Einsatz), außen geschlossen.
- **Hintergrund transparent**: kein Boden, keine Plakette, kein Rahmen. Das Motiv füllt ca. 85 % der Fläche, zentriert, mit 8 % Rand.
- **Silhouette** muss bei Einsatzgröße 28–96 px eindeutig lesbar bleiben (Graustufen-Test).
- **Master**: 256×256 PNG, RGBA, sRGB. Gezeigt wird per Downscale auf die Einsatzgröße.
- **Zustände**:
  - **inaktiv** (Dock): eigene Datei, entsättigt auf ca. 35 %, ohne Glut, Helligkeit −20 %.
  - **gedrückt/offen**: über den Button-Sprite, kein eigenes Icon.
  - **gesperrt**: Icon in Graustufen plus Overlay `d2_ico_schloss` unten rechts, keine eigene Datei.
  - **aktiv** (Dock): volle Farbe, Glut-Akzente leuchten.

## Liste
| Nr | Dateiname | Bereich | Einsatz px | Export | Motiv | Zustand | Prio |
|---|---|---|---|---|---|---|---|
| 1 | d2_ico_zeitkristall.png | Top: Waehrung | 64 | 256 | Facettierter Obsidian-Splitter mit glutorange leuchtendem Kern, feine Risse mit Lichtadern, kleiner Funken oben links | normal | P1 |
| 2 | d2_ico_wissen.png | Top: Waehrung | 64 | 256 | Steintafel mit eingeritzten Hoehlenzeichen (Sonne, Hand, Spirale), Ritzungen glimmen warm orange | normal | P1 |
| 3 | d2_ico_gold_muschel.png | Top: Waehrung | 64 | 256 | Drei gestapelte Kauri-Muscheln, perlmuttgold glaenzend, an Lederschnur, warme Kanten-Highlights | normal | P1 |
| 4 | d2_ico_plus.png | Top: Plus an Zeitkristalle | 48 | 256 | Dickes Plus aus zwei gekreuzten Knochenstaeben, mit Glutorange-Kern und dunkler Outline | normal/gedrueckt | P1 |
| 5 | d2_ico_avatar_rahmen.png | Top: Avatar | 128 | 256 | Runder Rahmen aus Obsidian mit Leder-Umwicklung und zwei Zahn-Spitzen oben, innen Glut-Rand (Portraet austauschbar) | normal | P1 |
| 6 | d2_ico_stufe_badge.png | Top: Avatar-Stufe | 60x40 | 256 | Kleines Steinschild mit Kerbrand, Glutfuge oben; Zahl wird per Text gesetzt | normal | P1 |
| 7 | d2_ico_kiste.png | Top: Ressourcen-Knopf | 72 | 256 | Geflochtene Weidenkiste mit Fellabdeckung, Holzspitze und Steinbrocken schauen heraus, Glut-Schimmer im Spalt | normal/offen | P1 |
| 8 | d2_ico_holz.png | Ressourcen-Liste | 72 | 256 | Gebundenes Buendel Rundholz mit Rinde, Schnittflaechen mit Jahresringen, Lederband | normal | P1 |
| 9 | d2_ico_stein.png | Ressourcen-Liste | 72 | 256 | Haufen grober Bruchsteine, oberster mit Feuerstein-Schlag-Kante, kuehles Grau mit warmem Reflex | normal | P1 |
| 10 | d2_ico_nahrung.png | Ressourcen-Liste | 72 | 256 | Gebratene Keule am Knochen auf Blatt, dazu Beeren, Dampfwoelkchen, fettiger Glanz | normal | P1 |
| 11 | d2_ico_lager_voll.png | Ressourcen-Liste | 32 | 256 | Kleines Ausrufe-Steinchen mit Glutrand (Lager voll / Produktion stockt) | normal | P2 |
| 12 | d2_ico_events.png | Links: Events | 88 | 256 | Lagerfeuer-Fahne: Lederwimpel an Speer, darunter kleines Feuer mit Funken | normal/offen | P1 |
| 13 | d2_ico_event_erntefest.png | Event-Liste | 72 | 256 | Korb mit Wildgetreide, Beeren und Pilzen, kleine Bluetenkette | normal | P1 |
| 14 | d2_ico_event_turnier.png | Event-Liste | 72 | 256 | Zwei gekreuzte Steinkeulen vor rundem Fellschild | normal | P1 |
| 15 | d2_ico_event_haendler.png | Event-Liste | 72 | 256 | Wanderbuendel mit Fellen, Muscheln und Krug, Wanderstab | normal | P1 |
| 16 | d2_ico_event_bauwoche.png | Event-Liste | 72 | 256 | Hammer aus Stein auf halbfertigem Holzgeruest, Staubwoelkchen | normal | P1 |
| 17 | d2_ico_event_gildenjagd.png | Event-Liste | 72 | 256 | Mammut-Silhouette hinter drei Speeren, Fussspuren | normal | P1 |
| 18 | d2_ico_uhr.png | Event-Liste / Timer | 28 | 256 | Sonnenuhr aus Stein mit Schattenstab, Glutpunkt in der Mitte | normal | P1 |
| 19 | d2_ico_wettkampf.png | Links: Wettkampf-Hub | 88 | 256 | Siegerkranz aus Knochen und Federn um gekreuzte Speere | normal | P1 |
| 20 | d2_ico_arena.png | Wettkampf-Hub | 88 | 256 | Steinkreis-Arena mit Fackeln, zwei kleine Figuren-Silhouetten | normal/gesperrt | P1 |
| 21 | d2_ico_ranglisten.png | Wettkampf-Hub | 88 | 256 | Totempfahl mit drei Stufen-Koepfen, oberster mit Glutaugen | normal/gesperrt | P1 |
| 22 | d2_ico_ahnenpruefung.png | Wettkampf-Hub | 88 | 256 | Schaedel eines Ahnen mit Bemalung auf Steinpodest, blaue Geisterflamme (accent.moon) dahinter | normal/gesperrt | P1 |
| 23 | d2_ico_beschwoeren.png | Rechts: Beschwoeren | 88 | 256 | Schamanen-Trommel mit Spiralmuster, darueber wirbelnder Glutrauch und Funken | normal (Glow-Ring) | P1 |
| 24 | d2_ico_angebote.png | Rechts: Angebote | 88 | 256 | Geschnuerter Fellbeutel, aus dem Zeitkristalle und Muscheln quellen, Preisschnur | normal | P1 |
| 25 | d2_ico_shop.png | Angebote-Reiter | 64 | 256 | Marktstand-Dach aus Fell auf zwei Pfaehlen, darunter Kruege | aktiv/inaktiv | P1 |
| 26 | d2_ico_gratis_login.png | Angebote-Reiter | 64 | 256 | Geschenk in Blatt gewickelt, mit Ranke verschnuert, kleiner Kalender-Kerbstock | aktiv/inaktiv | P1 |
| 27 | d2_ico_abo.png | Angebote-Reiter | 64 | 256 | Halskette mit grossem Glutstein-Anhaenger (Dauer-Vorteil) | aktiv/inaktiv | P1 |
| 28 | d2_ico_pass.png | Rechts: Pass | 88 | 256 | Lederrolle mit Kerb-Stufen und eingesetztem Glutstein, Siegelband | normal | P1 |
| 29 | d2_ico_mail.png | Mini: Mail | 64 | 256 | Zusammengerollte Birkenrinde mit Lederband und Feder-Siegel | normal | P1 |
| 30 | d2_ico_mehr.png | Mini: Mehr | 64 | 256 | Drei Glutsteine nebeneinander auf Steinplatte (Mehr-Punkte) | normal/offen | P1 |
| 31 | d2_ico_forschung.png | Mehr-Kachel | 88 | 256 | Feuerstein und Funkenschlag ueber Hoehlenzeichnung, Glimmen | normal/gesperrt | P1 |
| 32 | d2_ico_minigames.png | Mehr-Kachel | 88 | 256 | Knochenwuerfel und Steinkugeln in Ledermulde | normal/gesperrt | P1 |
| 33 | d2_ico_erfolge.png | Mehr-Kachel | 88 | 256 | Sternfoermiger Glutstein-Orden an Lederband | normal | P1 |
| 34 | d2_ico_artefakte.png | Mehr-Kachel | 88 | 256 | Geschnitzte Venus-Figur bzw. Amulett aus Elfenbein mit Glutritzung | normal/gesperrt | P1 |
| 35 | d2_ico_aufwertung.png | Mehr-Kachel | 88 | 256 | Steinklinge auf Amboss-Stein, Pfeil-Funke nach oben | normal/gesperrt | P1 |
| 36 | d2_ico_kosmetik.png | Mehr-Kachel | 88 | 256 | Bemalter Fellumhang mit Federschmuck und Farbtoepfchen | normal/gesperrt | P1 |
| 37 | d2_ico_einstellungen.png | Mehr-Kachel | 88 | 256 | Steinzahnrad (behauen) mit Holzachse | normal | P1 |
| 38 | d2_ico_hilfe.png | Mehr-Kachel | 88 | 256 | Fragezeichen aus Ranken in Steinkreis, warm leuchtend | normal | P1 |
| 39 | d2_ico_chat.png | Links: Chat | 88 | 256 | Zwei Sprechblasen aus Rauchwolken ueber kleinem Feuer | normal | P1 |
| 40 | d2_ico_quest.png | Quest-Leiste | 72 | 256 | Eingeritzter Kerbstock mit Haken-Kerbe, Glut in den Kerben | normal/fertig | P1 |
| 41 | d2_ico_quest_fertig.png | Quest-Leiste | 40 | 256 | Haken aus Glutlinie auf Stein (Belohnung abholbar) | normal | P1 |
| 42 | d2_ico_bauen.png | Rechts unten: Bauen | 88 | 256 | Steinhammer mit Lederbindung, Glutfunken am Kopf, schraeg nach rechts oben | normal/aktiv (Bau-Modus) | P1 |
| 43 | d2_ico_dock_dorf.png | Dock | 96 | 256 | Rundzelt/Huette mit Rauchfahne und Feuerschein im Eingang | aktiv | P1 |
| 44 | d2_ico_dock_dorf_inaktiv.png | Dock | 80 | 256 | dito, entsaettigt, ohne Glut, Rauchfahne grau | inaktiv | P1 |
| 45 | d2_ico_dock_helden.png | Dock | 96 | 256 | Helm aus Schaedel mit Hornern und Federn, Glutaugen | aktiv | P1 |
| 46 | d2_ico_dock_helden_inaktiv.png | Dock | 80 | 256 | dito, entsaettigt, Augen dunkel | inaktiv | P1 |
| 47 | d2_ico_dock_karte.png | Dock | 96 | 256 | Fellkarte mit gemalten Pfaden, Glut-X als Ziel | aktiv | P1 |
| 48 | d2_ico_dock_karte_inaktiv.png | Dock | 80 | 256 | dito, entsaettigt | inaktiv | P1 |
| 49 | d2_ico_dock_armee.png | Dock | 96 | 256 | Drei gebuendelte Speere mit Fellschild | aktiv | P1 |
| 50 | d2_ico_dock_armee_inaktiv.png | Dock | 80 | 256 | dito, entsaettigt | inaktiv | P1 |
| 51 | d2_ico_dock_gilde.png | Dock | 96 | 256 | Clan-Banner mit Handabdruck in Glutfarbe an Totemstab | aktiv | P1 |
| 52 | d2_ico_dock_gilde_inaktiv.png | Dock | 80 | 256 | dito, entsaettigt | inaktiv | P1 |
| 53 | d2_ico_dock_inventar.png | Dock | 96 | 256 | Lederrucksack mit Knochenknebel, Werkzeug schaut heraus | aktiv | P1 |
| 54 | d2_ico_dock_inventar_inaktiv.png | Dock | 80 | 256 | dito, entsaettigt | inaktiv | P1 |
| 55 | d2_ico_badge_zahl.png | Badges (alle) | 48x38 / 40x34 | 256 | Glutorange Kieselstein-Plakette mit dunkler Outline; Zahl per Text | normal | P1 |
| 56 | d2_ico_badge_punkt.png | Badges (ohne Zahl) | 24 | 256 | Kleiner Glutpunkt mit hellem Kern | normal | P2 |
| 57 | d2_ico_schloss.png | Gesperrte Features | 40 | 256 | Holzriegel mit Lederknoten vor Steinring (Steinzeit-Schloss) | gesperrt | P1 |
| 58 | d2_ico_neu.png | Freischalt-Hinweis | 40 | 256 | Kleine Funkenexplosion mit hellem Kern (neu freigeschaltet) | normal | P2 |
| 59 | d2_ico_schliessen.png | Dropdowns/Popups | 48 | 256 | Kreuz aus zwei Knochen, dunkle Outline | normal/gedrueckt | P2 |
| 60 | d2_ico_info.png | Ressourcen/Hub | 32 | 256 | Kleiner Stein mit eingeritztem i, Glutfuge | normal | P2 |

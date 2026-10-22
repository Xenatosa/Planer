# Icon-Liste Dorf-HUD D2 v1 (Basis Massplan v6.3) -> md + Uebersichts-PNG. 0 $, nur PIL.
import os, re
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
M = 256
# (datei, bereich, einsatz, motiv, zustand, prio)
I = [
 # Waehrungen / Top
 ("zeitkristall", "Top: Waehrung", "64", "Facettierter Obsidian-Splitter mit glutorange leuchtendem Kern, feine Risse mit Lichtadern, kleiner Funken oben links", "normal", "P1"),
 ("wissen", "Top: Waehrung", "64", "Steintafel mit eingeritzten Hoehlenzeichen (Sonne, Hand, Spirale), Ritzungen glimmen warm orange", "normal", "P1"),
 ("gold_muschel", "Top: Waehrung", "64", "Drei gestapelte Kauri-Muscheln, perlmuttgold glaenzend, an Lederschnur, warme Kanten-Highlights", "normal", "P1"),
 ("plus", "Top: Plus an Zeitkristalle", "48", "Dickes Plus aus zwei gekreuzten Knochenstaeben, mit Glutorange-Kern und dunkler Outline", "normal/gedrueckt", "P1"),
 ("avatar_rahmen", "Top: Avatar", "128", "Runder Rahmen aus Obsidian mit Leder-Umwicklung und zwei Zahn-Spitzen oben, innen Glut-Rand (Portraet austauschbar)", "normal", "P1"),
 ("stufe_badge", "Top: Avatar-Stufe", "60x40", "Kleines Steinschild mit Kerbrand, Glutfuge oben; Zahl wird per Text gesetzt", "normal", "P1"),
 ("kiste", "Top: Ressourcen-Knopf", "72", "Geflochtene Weidenkiste mit Fellabdeckung, Holzspitze und Steinbrocken schauen heraus, Glut-Schimmer im Spalt", "normal/offen", "P1"),
 ("holz", "Ressourcen-Liste", "72", "Gebundenes Buendel Rundholz mit Rinde, Schnittflaechen mit Jahresringen, Lederband", "normal", "P1"),
 ("stein", "Ressourcen-Liste", "72", "Haufen grober Bruchsteine, oberster mit Feuerstein-Schlag-Kante, kuehles Grau mit warmem Reflex", "normal", "P1"),
 ("nahrung", "Ressourcen-Liste", "72", "Gebratene Keule am Knochen auf Blatt, dazu Beeren, Dampfwoelkchen, fettiger Glanz", "normal", "P1"),
 ("lager_voll", "Ressourcen-Liste", "32", "Kleines Ausrufe-Steinchen mit Glutrand (Lager voll / Produktion stockt)", "normal", "P2"),
 # Events
 ("events", "Links: Events", "88", "Lagerfeuer-Fahne: Lederwimpel an Speer, darunter kleines Feuer mit Funken", "normal/offen", "P1"),
 ("event_erntefest", "Event-Liste", "72", "Korb mit Wildgetreide, Beeren und Pilzen, kleine Bluetenkette", "normal", "P1"),
 ("event_turnier", "Event-Liste", "72", "Zwei gekreuzte Steinkeulen vor rundem Fellschild", "normal", "P1"),
 ("event_haendler", "Event-Liste", "72", "Wanderbuendel mit Fellen, Muscheln und Krug, Wanderstab", "normal", "P1"),
 ("event_bauwoche", "Event-Liste", "72", "Hammer aus Stein auf halbfertigem Holzgeruest, Staubwoelkchen", "normal", "P1"),
 ("event_gildenjagd", "Event-Liste", "72", "Mammut-Silhouette hinter drei Speeren, Fussspuren", "normal", "P1"),
 ("uhr", "Event-Liste / Timer", "28", "Sonnenuhr aus Stein mit Schattenstab, Glutpunkt in der Mitte", "normal", "P1"),
 # Wettkampf
 ("wettkampf", "Links: Wettkampf-Hub", "88", "Siegerkranz aus Knochen und Federn um gekreuzte Speere", "normal", "P1"),
 ("arena", "Wettkampf-Hub", "88", "Steinkreis-Arena mit Fackeln, zwei kleine Figuren-Silhouetten", "normal/gesperrt", "P1"),
 ("ranglisten", "Wettkampf-Hub", "88", "Totempfahl mit drei Stufen-Koepfen, oberster mit Glutaugen", "normal/gesperrt", "P1"),
 ("ahnenpruefung", "Wettkampf-Hub", "88", "Schaedel eines Ahnen mit Bemalung auf Steinpodest, blaue Geisterflamme (accent.moon) dahinter", "normal/gesperrt", "P1"),
 # Rechte Spalte
 ("beschwoeren", "Rechts: Beschwoeren", "88", "Schamanen-Trommel mit Spiralmuster, darueber wirbelnder Glutrauch und Funken", "normal (Glow-Ring)", "P1"),
 ("angebote", "Rechts: Angebote", "88", "Geschnuerter Fellbeutel, aus dem Zeitkristalle und Muscheln quellen, Preisschnur", "normal", "P1"),
 ("shop", "Angebote-Reiter", "64", "Marktstand-Dach aus Fell auf zwei Pfaehlen, darunter Kruege", "aktiv/inaktiv", "P1"),
 ("gratis_login", "Angebote-Reiter", "64", "Geschenk in Blatt gewickelt, mit Ranke verschnuert, kleiner Kalender-Kerbstock", "aktiv/inaktiv", "P1"),
 ("abo", "Angebote-Reiter", "64", "Halskette mit grossem Glutstein-Anhaenger (Dauer-Vorteil)", "aktiv/inaktiv", "P1"),
 ("pass", "Rechts: Pass", "88", "Lederrolle mit Kerb-Stufen und eingesetztem Glutstein, Siegelband", "normal", "P1"),
 # Mini-Reihe / Mehr
 ("mail", "Mini: Mail", "64", "Zusammengerollte Birkenrinde mit Lederband und Feder-Siegel", "normal", "P1"),
 ("mehr", "Mini: Mehr", "64", "Drei Glutsteine nebeneinander auf Steinplatte (Mehr-Punkte)", "normal/offen", "P1"),
 ("forschung", "Mehr-Kachel", "88", "Feuerstein und Funkenschlag ueber Hoehlenzeichnung, Glimmen", "normal/gesperrt", "P1"),
 ("minigames", "Mehr-Kachel", "88", "Knochenwuerfel und Steinkugeln in Ledermulde", "normal/gesperrt", "P1"),
 ("erfolge", "Mehr-Kachel", "88", "Sternfoermiger Glutstein-Orden an Lederband", "normal", "P1"),
 ("artefakte", "Mehr-Kachel", "88", "Geschnitzte Venus-Figur bzw. Amulett aus Elfenbein mit Glutritzung", "normal/gesperrt", "P1"),
 ("aufwertung", "Mehr-Kachel", "88", "Steinklinge auf Amboss-Stein, Pfeil-Funke nach oben", "normal/gesperrt", "P1"),
 ("kosmetik", "Mehr-Kachel", "88", "Bemalter Fellumhang mit Federschmuck und Farbtoepfchen", "normal/gesperrt", "P1"),
 ("einstellungen", "Mehr-Kachel", "88", "Steinzahnrad (behauen) mit Holzachse", "normal", "P1"),
 ("hilfe", "Mehr-Kachel", "88", "Fragezeichen aus Ranken in Steinkreis, warm leuchtend", "normal", "P1"),
 # Unten
 ("chat", "Links: Chat", "88", "Zwei Sprechblasen aus Rauchwolken ueber kleinem Feuer", "normal", "P1"),
 ("quest", "Quest-Leiste", "72", "Eingeritzter Kerbstock mit Haken-Kerbe, Glut in den Kerben", "normal/fertig", "P1"),
 ("quest_fertig", "Quest-Leiste", "40", "Haken aus Glutlinie auf Stein (Belohnung abholbar)", "normal", "P1"),
 ("bauen", "Rechts unten: Bauen", "88", "Steinhammer mit Lederbindung, Glutfunken am Kopf, schraeg nach rechts oben", "normal/aktiv (Bau-Modus)", "P1"),
 # Dock
 ("dock_dorf", "Dock", "96", "Rundzelt/Huette mit Rauchfahne und Feuerschein im Eingang", "aktiv", "P1"),
 ("dock_dorf", "Dock", "80", "dito, entsaettigt, ohne Glut, Rauchfahne grau", "inaktiv", "P1"),
 ("dock_helden", "Dock", "96", "Helm aus Schaedel mit Hornern und Federn, Glutaugen", "aktiv", "P1"),
 ("dock_helden", "Dock", "80", "dito, entsaettigt, Augen dunkel", "inaktiv", "P1"),
 ("dock_karte", "Dock", "96", "Fellkarte mit gemalten Pfaden, Glut-X als Ziel", "aktiv", "P1"),
 ("dock_karte", "Dock", "80", "dito, entsaettigt", "inaktiv", "P1"),
 ("dock_armee", "Dock", "96", "Drei gebuendelte Speere mit Fellschild", "aktiv", "P1"),
 ("dock_armee", "Dock", "80", "dito, entsaettigt", "inaktiv", "P1"),
 ("dock_gilde", "Dock", "96", "Clan-Banner mit Handabdruck in Glutfarbe an Totemstab", "aktiv", "P1"),
 ("dock_gilde", "Dock", "80", "dito, entsaettigt", "inaktiv", "P1"),
 ("dock_inventar", "Dock", "96", "Lederrucksack mit Knochenknebel, Werkzeug schaut heraus", "aktiv", "P1"),
 ("dock_inventar", "Dock", "80", "dito, entsaettigt", "inaktiv", "P1"),
 # Zustaende / allgemein
 ("badge_zahl", "Badges (alle)", "48x38 / 40x34", "Glutorange Kieselstein-Plakette mit dunkler Outline; Zahl per Text", "normal", "P1"),
 ("badge_punkt", "Badges (ohne Zahl)", "24", "Kleiner Glutpunkt mit hellem Kern", "normal", "P2"),
 ("schloss", "Gesperrte Features", "40", "Holzriegel mit Lederknoten vor Steinring (Steinzeit-Schloss)", "gesperrt", "P1"),
 ("neu", "Freischalt-Hinweis", "40", "Kleine Funkenexplosion mit hellem Kern (neu freigeschaltet)", "normal", "P2"),
 ("schliessen", "Dropdowns/Popups", "48", "Kreuz aus zwei Knochen, dunkle Outline", "normal/gedrueckt", "P2"),
 ("info", "Ressourcen/Hub", "32", "Kleiner Stein mit eingeritztem i, Glutfuge", "normal", "P2"),
]
rows = []
for n, (f, b, e, mo, z, p) in enumerate(I, 1):
    fn = f"d2_ico_{f}" + ("_inaktiv" if z == "inaktiv" else "") + ".png"
    rows.append((str(n), fn, b, e, f"{M}" if p == "P1" else f"{M}", mo, z, p))
cnt = {p: sum(r[7] == p for r in rows) for p in ("P1", "P2")}
md = f"""# Icon-Liste Dorf-HUD D2 v1 (Basis: Massplan v6.3)

Stand: 22.10.2026. Erzeugt von `_src/icon_liste_hud_d2_v1.py`, Übersicht als `icon_liste_hud_d2_v1.png`.
Insgesamt {len(rows)} Icon-Dateien, davon P1 {cnt['P1']} (nötig für das HUD) und P2 {cnt['P2']} (später).
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
""" + "\n".join("| " + " | ".join(r) + " |" for r in rows) + "\n"
open(os.path.join(OUT, "icon_liste_hud_d2_v1.md"), "w").write(md)
# PNG
FONTS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(OUT))), "team/art/ui/fonts")
fb = ImageFont.truetype(os.path.join(FONTS, "Baloo2-Variable.ttf"), 20)
try: fb.set_variation_by_axes([700])
except Exception: pass
fh = ImageFont.truetype(os.path.join(FONTS, "LilitaOne-Regular.ttf"), 22); ft = ImageFont.truetype(os.path.join(FONTS, "LilitaOne-Regular.ttf"), 36)
cols = [("Nr", 50), ("Dateiname", 330), ("Bereich", 250), ("Einsatz", 120), ("Export", 80), ("Motiv", 1060), ("Zustand", 230), ("Prio", 60)]
W = sum(c[1] for c in cols) + 40; RH = 30; H = 110 + RH * (len(rows) + 1) + 30
im = Image.new("RGB", (W, H), (28, 22, 18)); d = ImageDraw.Draw(im)
d.text((20, 20), f"Icon-Liste Dorf-HUD D2 v1 (Massplan v6.3)  -  {len(rows)} Icons: P1 {cnt['P1']}, P2 {cnt['P2']}  -  Master 256 px, transparent, Licht oben links", font=ft, fill=(255, 217, 168))
y = 80; x = 20
d.rectangle([20, y, W - 20, y + RH], fill=(74, 50, 32))
for (c, w) in cols: d.text((x + 6, y + RH / 2), c, font=fh, fill=(255, 210, 122), anchor="lm"); x += w
for k, r in enumerate(rows):
    y += RH; x = 20
    d.rectangle([20, y, W - 20, y + RH], fill=(40, 32, 26) if k % 2 else (34, 27, 22))
    for (c, w), v in zip(cols, r):
        while d.textlength(v, font=fb) > w - 10: v = v[:-2] + "…"
        col = (255, 179, 71) if (c == "Prio" and v == "P1") else (243, 231, 207)
        d.text((x + 6, y + RH / 2), v, font=fb, fill=col, anchor="lm"); x += w
im.save(os.path.join(OUT, "icon_liste_hud_d2_v1.png"))
print(len(rows), cnt)

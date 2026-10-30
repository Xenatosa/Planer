# Dorfmap-Grundgerüst E1 (c20): Zellraster ohne Texturen
Stand 30.10.2026. Marker: [S] gemessen/Quelle, [A] Annahme, [R] gerechnet, [F] Entscheidung Fabian. 0 $, keine Bildgenerierung.

## 1 Basis
- Karte: `karten_konzept/dorfkarte_e1_final_neu/master_v18_p7/KANDIDAT_NICHT_FREIGEGEBEN_master_v18_p7_c20.png`, 8400×7560 px, md5 d916c6ac…, Epoche E1 Eisland [F 30.10., AD_ANTWORT.md]. Die Karte bleibt unverändert.
- Maßstab 25 px/m [F], Band 20–30 [S MASSGRUNDLAGE_E1_v1.md]. 30 px/m (layout_e1_v9, groessen_25slots, massplan_v3_7_8) ist überholt [F].
- Die Weltmeter in zonen_c20_v9.json folgen noch der Formel PX=((x+200)·30,(y+40)·30). Das Raster rechnet deshalb in **px** und rechnet Zonen-Polygone mit genau dieser Formel in px um [R]. Echte Meter = px/25 [R].

## 2 Zellmaß (Parameter `ZELLE_PX`)
Ein Zellmaß ist nirgends festgelegt [S AD_ANTWORT]. Default **25 px = 1,0 m** [A], begründet aus den Kartenmaßen [S MASSGRUNDLAGE]:
- Mensch 41 px ≈ 1,6 Zellen [R]
- Fels klein 50 px = 2 Zellen, Fels mittel 130 px ≈ 5, Findling 210 px ≈ 8 [R]
- Pfad ≈ 30 px ≈ 1,2 Zellen, Bach Süd 185–250 px ≈ 7–10 Zellen, Klippe Nord 190–240 px ≈ 8–10 Zellen [R]
- Tür E1 35×20 px ≈ 1,4×0,8 Zellen [R], Quelle abgeleitet [A]

Rastergröße: ceil(8400/25)×ceil(7560/25) = **336×303 Zellen** [R]; die letzte Zeile ist nur 10 px hoch [R]. Variante 50 px (2 m) ergibt 168×152 Zellen [R]; davon liegen Meta und Vorschau bei (`raster_c20_z50_*`). Neu erzeugen mit `python3 gen_raster.py <px>`.

## 3 Ebenen und Eigenschaftsfelder (je Zelle, CSV-Spalten, Schema `schema_zelle.json`)
Eine Zelle wird gesetzt, wenn mindestens 50 % ihrer px in der Maske liegen. Ausnahme Wege und Brücke: dort reichen 30 %, damit schmale Wege nicht wegfallen [A].

| Feld | Werte | Quelle |
|---|---|---|
| untergrund | BODEN, UNBEKANNT, SAND, WALD, FELS_KLIPPE, SCHNEE, FELS_WALD, WASSER_EIS, HOF, FEUER, WEG, BRUECKE | aus den Masken unten abgeleitet, Vorrang von links nach rechts steigend [A] |
| zone | A–E | layout_e1_v9/ebenen/10_zonenboden_*_maske.png [S] |
| platz | nr (99 Plätze) | zonen_c20_v9.json `plaetze[].poly` [S] |
| weg_id / weg_klasse | G001…, haus_A11 … / GASSE, ANBINDUNG, HAUSWEG | 20_wege_*_maske.png [S]; Breiten 2,4/1,8/1,2 „m“ stehen in v9 noch auf der 30-px-Basis, das sind real 2,9/2,2/1,4 m [R] |
| hindernis | Index in hindernisse_c20_v2.json (Schneehügel, Eisriss, Moos) | slots_c20/hindernisse_c20_v2.npz [S]; deckt nur das Fenster der Bauzone ab |
| wasser_eis | 0/1 | arbeit/bach_schutz.npy [S]. **Wasser und Eis lassen sich per Farbe nicht trennen** [S PLAN_LOOK_SYSTEM_v1]; das Feld bedeutet „Bach/See inkl. Schutzband“ [A] |
| schnee | 0/1 | arbeit/F4.npy [S] |
| senke_bb4 | 0/1 | arbeit/BB4.npy (Senke/Bauzone) [S] |
| h4_ext | 0/1 | arbeit/H4_ext.npy [S]; Bedeutung nicht dokumentiert [A] |
| frei_e2 | 0/1 | slots_c20/mp/frei_e2.npy (ohne Fels, Wald, Wasser, Schluchtpfad) [S] |
| begehbar | 0/1 | [R]: nicht KLIPPE_WAND, KLIPPE_KANTE, FELS, WASSER_EIS, FELS_WALD, UNBEKANNT oder Hindernis (GESPERRT gibt es nicht mehr); WEG und BRUECKE sind immer begehbar |
| bebaubar | 0/1 | [R]: senke_bb4 ∧ frei_e2 ∧ ¬Wasser ∧ ¬Fels ∧ ¬Hindernis ∧ ¬Weg ∧ ¬Brücke ∧ ¬Feuer |
| klippe | KANTE/leer | Übergang von BB4 zu Fels/Rand [R aus Masken]. Grob, weil die Klippenmaske grob ist [S] |
| skin_slot | ug_<untergrund> | Brücke zum Skin-System (Abschnitt 5) |

Zählung bei 25 px [R, raster_c20_z25_meta.json]: GESPERRT 61 555, SCHNEE 20 454, BODEN 9 040, FELS_WALD 5 999, WEG 2 825, WASSER_EIS 1 214, HOF 430, FEUER 271, BRUECKE 20. Davon begehbar 32 414 und bebaubar 19 931.

## 2a Abdeckung der ganzen Karte (Fabian t5u)
Das Raster deckt alle 336×303 = 101 808 Zellen ab (8400×7560 px, letzte Zeile 10 px). Jede Zelle hat einen Untergrund und eine `untergrund_quelle`.

**Befund vorher (bis Commit a57c4c3):** 61 555 Zellen (60,5 %) standen ohne Daten als GESPERRT da. Dazu gehörten:
- Westrand mit Wald und Teich
- Krater
- Plateau und Klippe im Norden
- Ostwald
- Südgrat
- Südfluss mit Sandbänken
- Südwald

**Ursachen:**
1. Die Masken BB4, F4 und frei_e2 decken nur die Senke bzw. das Becken ab. BB4 hat die bbox x 1642–8359 und y 631–6071 px [S BB4.json]. Die gerade Kante im Westen ist diese Maskengrenze, kein Gelände.
2. Die Hindernisse (hindernisse_c20_v2) gibt es nur im Fenster x 3900–8100 und y 540–3060 px [S npz X0/Y0, 420×252 Zellen à 10 px].
3. Für die Kartenteile außerhalb der Senke gab es bisher keine Masken.

**Behoben [R]:** Zellen ohne Maske bekommen jetzt eine Farbklasse aus der Original-c20, gezählt in HSV-Anteilen je Zelle (Code in `gen_raster.py`). Die Klassen:

| Klasse | Regel |
|---|---|
| SCHNEE | ≥ 30 % hell und ungesättigt |
| SAND | ≥ 35 % beige |
| FELS_KLIPPE | ≥ 3 % braun und < 50 % Schnee |
| WALD | ≥ 15 % dunkel oder grün |
| WASSER_EIS | ≥ 35 % blau-türkis |

Die Schwellen sind gesetzt [A]. Ich habe sie durch Vergleich mit der Karte geprüft, aber nicht gemessen.

**Abdeckung jetzt:**

| Quelle | Anteil |
|---|---|
| MASKE [S] | 39,5 % |
| FARBE [R] | 46,3 % |
| KEINE (UNBEKANNT, in der Vorschau magenta) | 14,1 % = 14 398 Zellen |

**Rest UNBEKANNT:**
- Das sind vor allem Klippenwände und deren Schattenseiten (Nordwand, Krater, Südgrat, Ostgrat). Dort mischen sich Fels, Schatten und Schnee, sodass keine Farbklasse eindeutig ist.
- Diese Zellen sind nicht begehbar. Sie sollen von Hand oder mit einer echten Klippenmaske nachgezogen werden.

**Risiko [A]:** Blaue Schatten am Fuß der Nordklippe können als WASSER_EIS erkannt werden. Wasser aus der Farbe trägt `fluss_id` WASSER_FARBE, ohne Richtung und ohne Höhe.

**Vergleichsbilder:**
- `raster_c20_z25_vergleich.png`: Original links, Raster rechts
- `raster_c20_z25_overlay.png`: 50 % überblendet

## 3a Höhe, Flüsse, 3D (Fabian t4u)
Eine Höhenkarte gibt es nicht [S]. Werte stehen nur dort, wo eine Quelle sie trägt. Alles andere bleibt leer.

| Feld | Herleitung | Marker |
|---|---|---|
| hoehe_m | Senke (BB4 ohne Wasser) = `BEZUG_M` (Standard 0). Nordklippen-Kante = Bezug + 8,6 m. Sonst leer: Hochflächen, Schneefelder im Westen und Rand | Senke flach [A]; 8,6 [R] |
| klippe_hoehe_m | nur Nordwand (obere 25 % der Karte [A]): (190+240)/2 px / 25 = 8,6 m | Maße [S], Rechnung [R], ohne Verkürzung [A] |
| neigung_grad | atan(Δhoehe/Zellmaß), nur wo hoehe_m bekannt ist. Senke 0°, Klippenkante steil | [R] |
| fluss_id | BACH_NORD, SEE, BACH_SUED aus bach_schutz, zugeordnet über die Bachpolylinie in slots_c20/mp/frei_e2.py | Maske [S], Zuordnung [R] |
| fliess_richtung | 8 Richtungen entlang der Polylinie: Nord → See → Süd | Polylinie [S], Richtung [R] |
| fluss_breite_m | 2 × Uferabstand auf der Mittellinie (Skelett) von bach_schutz. Median Nord 2,0 m, Süd 2,5 m | [R] |
| wasser_tiefe_m | leer | keine Quelle |
| ufer / furt | Ufer: begehbare Nachbarzelle von Wasser (510 Zellen). Furt: Weg quert Wasser ohne Brücke (0 Zellen, Querungen nur über Brücken) | [R] |
| begehbar_3d | begehbar ∧ neigung ≤ 30°. Furt gilt als begehbar | Schwelle [A] |

**Widerspruch Bachbreite:** Laut Maßgrundlage ist der Bach Süd 185–250 px breit, also 7,4–10 m [R]. Die Maske bach_schutz ergibt nur ≈ 2,5 m.
- Vermutlich trägt die Maske nur das Rinnsal oder Schutzband und nicht das ganze Bachbett [A].
- Das Raster nimmt den Maskenwert. Für ein 3D-Bachbett sollte die Breite 7,4–10 m aus der Maßgrundlage genommen werden.

**3D-Konvention:**
- Achsen: X nach Osten = cx, Y nach Süden = cy (Bild), Z nach oben in Metern.
- 1 m = 25 px; Unity-Einheit = px/256 (PPU 256), also 1 m = 0,0977 Einheiten [R].
- Weltposition = (cx·Z/256, −cy·Z/256, hoehe_m·25/256).
- Leere Höhen bedeuten: nicht begehbar, solange niemand eine Höhe setzt.

**Lücken:**
- Höhe der Hochflächen und des Rands
- Höhe der übrigen Kanten (Süd, West), Höhe des Sees und Wassertiefe
- echte Projektionsverkürzung der Klippe
- Gefälle innerhalb der Senke

## 4 Schnittstellen
- **Wege-/Deko-System** (team/art/wege_deko_system):
  - `weg_id` entspricht den Gassen-IDs in zonen_c20_v9 und netz_e1.json.
  - `untergrund` lässt sich auf 02_UNTERGRUND_TYPEN abbilden: WEG→UG_ERDE/STEIN/PFLASTER je nach Epoche, BRUECKE→UG_HOLZ, sonst UG_KEIN [A].
  - Die Deko-Slots (netz_e1.json, 629) bleiben Anker. Das Raster liefert nur `begehbar`/`bebaubar` für die Prüfung.
  - Nach Regel §2 erscheinen Wege erst, wenn ein Gebäude steht. Das Raster speichert nur die mögliche Lage, die Anzeige steuert baustand.json [S REGEL_MODULSYSTEM].
- **Terrain-Art/Unity:** Zelle (cx,cy) → px (cx·Z, cy·Z) → Unity-Einheiten px/256 (PPU 256) [S].
  - Hinweis: Die Sorting-Bänder (L1 Boden −8600…−8000, L2 Wege −4999…−2000, Brücken −1999…−1000) passen zu den Untergrundklassen [S].
- **Modulsystem v3b:** Module bleiben Masken plus JSON. Das Raster ersetzt sie nicht, es ist die grobe Abfrage-Ebene (Pfadsuche, Bauprüfung).

## 5 Skins
- Jede Zelle trägt nur Eigenschaften, keinen Look. `skin_slot` verweist auf einen material_slot. Ein Skin ist eine Tabelle {skin_slot → Textur/Farbe} pro Look, Saison oder Epoche [A].
- Der Raster-Inhalt bleibt dabei gleich, nur die Tabelle wechselt (Regel „Karte gleich, Look ändert sich“, Fabian 30.10.).
- Neue Details (z. B. Spuren, Eisschollen) kommen als zusätzliche Spalte oder Ebene dazu, ohne bestehende Felder zu ändern.
- `epochen_variante` = "fest_c20": eine feste Einzelkarte für alle Epochen [F 30.10.]. Neue Standorte kommen als zusätzliche Plätze dazu.

## 6 Bestand: vorhanden / fehlt
**Vorhanden** [S]:
- c20-Karte
- MASSGRUNDLAGE_E1_v1 und messwerte.csv
- Masken BB4, F4, H4_ext, bach_schutz, frei_e2 und hindernisse_c20_v2
- layout_e1_v9/ebenen (Zonen, Wege, Höfe, Feuer, Brückenzugänge)
- zonen_c20_v9.json (99 Plätze)
- netz_e1/modulsystem_e1 und die Spezifikation wege_deko_system

**Fehlt oder lückenhaft** [S]:
- Höhenkarte fehlt.
- Wasser und Eis lassen sich nicht trennen.
- Die Klippenmaske ist nur grob.
- Ein festgelegtes Zellmaß fehlt.
- Hindernis-Erkennung gibt es nur im Fenster der Bauzone. Im Westen entsteht dadurch eine gerade Kante in FELS_WALD/GESPERRT, die vom Maskenfenster kommt und nicht aus dem Gelände.
- dorf-gesamtkarte-plan, dorf-wachstum-plan und f2-gelaende-konzept fehlen im Repo.
- dorf_e1/ enthält nur kosten.md.
- GUELTIG.md nennt c20 noch nicht, und die Dateinamen tragen noch „NICHT_FREIGEGEBEN“.
- Die Platz-Meter in v9 stehen noch auf der 30-px-Basis.

## 7 Entscheidungen
1. **Epochen: ENTSCHIEDEN [F Fabian 30.10.2026, t3u]**
   - Für alle Epochen gilt dieselbe Karte, nur der Look wechselt.
   - Neue Standorte kommen nur hinzu, bestehende bleiben.
   - `epochen_variante` = "fest_c20": Der Parameter bleibt erhalten, wird aber nicht genutzt.
2. **Zellmaß: Standard gewählt [A]:** 25 px = 1 m. Die Alternativen 50 px und 12,5 px bleiben über den Parameter `ZELLE_PX` möglich.
3. **Höhe/Klippe: erweitert (t4u):** Höhe, Klippe, Fluss und 3D stehen in §3a. Was keine Quelle hat, bleibt leer.
4. **Wasser/Eis: Standard gewählt [A]:** Beides bleibt ein gemeinsames Feld `wasser_eis`. Die Unterscheidung macht der Skin.
5. **Wegbreiten: Standard gewählt [A]:** Die v9-Angaben (Meter auf 30-px-Basis) bleiben, mit Umrechnungsfaktor 1,2 auf echte Meter (25 px/m).

## Dateien
- `gen_raster.py`: Generator, liest nur, schreibt nur in diesen Ordner.
- `raster_c20_z25_zellen.csv` (101 808 Zeilen) und `raster_c20_z25_meta.json`.
- `schema_zelle.json`
- `raster_c20_z25_hoehe_fluss.png`: Höhen-/Fluss-Ansicht.
- `raster_c20_z25_vorschau.png`: Flachfarben plus Legende, schraffiert = bebaubar. Dazu `raster_c20_z50_*`.


## §2b Klippenmaske aus Bildanalyse (t6u)

- Ersetzt die meisten UNBEKANNT-Zellen: **14 398 → 2 477 (14,1 % → 2,4 %)** [R].
- Methode je Zelle (25×25 px aus c20, HSV, OpenCV-Skala H 0–179):
  - Wald: Anteil dunkler blaugrüner Pixel (V<170, H 80–127, S≥40) ≥ 0,20 und größer als Anteil Wand-dunkel → WALD. Gemessen: Wald H≈113 [S].
  - KLIPPE_WAND: Anteil dunkel-violett/braun (V<150, H≥128 oder H<25) ≥ 0,12 und Canny-Kanten (60/140) ≥ 0,04, oder Fels-Brauntöne ≥ 0,03 bei wenig Schnee. Gemessen: Wände H≈146–148 [S].
  - FELS: Wand-Komponenten < 30 Zellen [A].
  - KLIPPE_KANTE: Wandzelle, deren nördlicher Nachbar weder Wand noch UNBEKANNT ist (Draufsicht von Süden) [A].
  - SCHATTEN: blaugrau (H 100–135, S 15–100, V 120–215) ≥ 0,35, wenig Kanten. Zusätzlich werden kleine längliche „Wasser“-Flecken (< 1500 Zellen, Seitenverhältnis ≥ 2,5, ≥ 50 % Rand an Wand, f_shade ≥ 0,2) zu SCHATTEN: 42 Zellen [R]. Runde Teiche bleiben Wasser.
  - Mehrheitsfilter 3×3, 2 Durchläufe, nur auf Farbzellen: Inseln < 4 Zellen und UNBEKANNT mit ≥ 5 gleichen Nachbarn gehen an die Mehrheit [A].
- klippe_hoehe_m: siehe §2c.
- Rest-UNBEKANNT (magenta) mit Zellbereichen: `raster_c20_z25_unbekannt_pruefliste.csv` (43 Komponenten ≥ 10 Zellen, größte: cx 77–115/cy 16–27 am Nordwandfuß).

## §2c Sichtprüfung und Wandhöhen (t7u)

- 43 Bereiche der Prüfliste als vergrößerte c20-Ausschnitte (mit 200 px Rand) angesehen. Die Entscheidungen stehen in `overrides_c20_z25.csv` (Zellbereich, Klasse, Marker, Begründung). gen_raster.py wendet sie nach der Automatik an, nur auf UNBEKANNT-Zellen und nur bei 25 px.
- 42 Bereiche gesetzt (1 288 Zellen), 1 Bereich bleibt offen (Eis/Schnee-Rand, cx 222–224/cy 267–272). UNBEKANNT 2 477 → 1 189 (2,4 % → 1,2 %) [R]. Der Rest sind Splitter unter 10 Zellen.
- Gesetzte Klassen: BODEN 6 (Absatz auf der Nordwand, Wiese), SCHATTEN 9, WASSER_EIS 6, KLIPPE_WAND 6, FELS 4, SAND 4, SCHNEE 4, WALD 2, KLIPPE_KANTE 1. Davon 25 [R] und 17 [A].
- Wandhöhen [A]: Gemessen wird der Median der senkrechten Felslaufweite in c20 (Fels-Pixel V<190, S≥25, H≥128 oder H<25, Close 9×9, Läufe ≥ 60 px, jede 10. Spalte). Daraus h = 8,6 m × px / 163 px (Nordwand-Median = 8,6 m [R]):
  - Krater: 145 px → 7,7 m
  - Südgrat: 144 px → 7,6 m
  - Ostgrat: 127 px → 6,7 m
  - Sonstige Wände (außerhalb dieser Fenster): 8,6 m [A]
  - Die Schattenlänge war nicht verwertbar (Median 5–15 px, Schatten verschmilzt mit Schnee) und geht nicht ein.
  - Die Fenster je Wand stehen in gen_raster.py (WAND_H) und in der Meta (`wand_hoehe_m`).

## §2d Layer-Trennung und Prüfung (t9u/t10u/t11u)
- Die Gelände-CSV `raster_c20_z25_zellen.csv` enthält nur Gelände-Spalten. Zone, Platz, Weg, Hof, Feuer, Brücke, Furt, Bauplatz und die Dekoplätze des Netzes stehen in `raster_c20_z25_overlay_plaetze_wege.csv` (Vorschau `_overlay_plaetze_wege.png`).
- Unter früheren Weg-, Hof-, Feuer- und Brückenzellen wurde das Gelände per Farbe neu gesetzt.
- Glättung: Mehrheitsfilter, Inselfilter, BODEN→SCHNEE, Stämme→WALD, Randzeile. Zahlen siehe `meta.json`.
- Höhenstufen [A]:

  | Bereich | Höhe |
  |---|---|
  | Nordplateau | +8,6 [R] |
  | Ostplateau | +6,7 |
  | Südvorland | −7,6 |
  | Senke und Rest | 0 |

- Deko-Kapazität: 0,44 je m² [R] aus Mindestabstand 1,5 m (BERICHT_NETZ_E1 §9.2).
- Restfehler und Prüfmethode: siehe PRUEFPROTOKOLL.md.
- z50: nur Meta und PNG, keine CSV.

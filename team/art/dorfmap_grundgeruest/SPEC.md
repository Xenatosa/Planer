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

**Stand t31u:** Die gültige Spaltenliste (39 Spalten) mit Werten und Markern steht in `schema_zelle.json`. Die Tabelle aus t3u (zone, platz, weg_id, hindernis, furt, alte Klassen FELS_KLIPPE/FELS_WALD/HOF/WEG) ist überholt und liegt in `_alt/SPEC_t30u.md`. Zone, Platz, Weg, Furt stehen seit t9u in der Overlay-CSV (§2d).

Zählung bei 25 px [R, raster_c20_z25_meta.json, t31u]: SCHNEE 59 807, KLIPPE_WAND 17 574, WALD 11 217, WASSER_EIS 6 695, FELS 2 123, SCHATTEN 1 772, KLIPPE_KANTE 1 178, BODEN 896, SAND 546. Begehbar 62 391, bebaubar 27 140, bebaubar_erweitert 54 409, bauzone_plan 31 893, senke_becken 31 325.
z50 [R]: begehbar 15 245, bebaubar 7 240, bebaubar_erweitert 15 056.

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
| hoehe_m | Senke = `BEZUG_M` (0). Stufen [A] siehe §2d und Feld `ebene` (t30u/t31u): Nordplateau +8,6, Ostplateau +6,7, Tal Süd −7,6, sonst 0 | Senke flach [A]; 8,6 [R] |
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
- z50: Meta, PNG und CSV (`raster_c20_z50_zellen.csv`, gleiche Spalten) [Stand t31u].

## bebaubar (t12u)
`senke_becken`: je Zeile rechts der Kraterwand (ohne Kraterwand: x ≥ 136 [A]) bis links der Ostgratwand, unter der Nordwand, ueber dem Suedgrat; Opening 9×9 kappt Paesse; Zusammenhangskomponente am Seed (230,120).
`bebaubar = senke_becken & begehbar & Untergrund ∈ {SCHNEE,BODEN,SAND} & hindernis==0 & Abstand Wand ≥ BAU_ABST_WAND_M & Abstand Wasser ≥ BAU_ABST_WASSER_M` (Default je 2 m [A], per Umgebungsvariable).
`bauzone_bestand` = alte Grenze BB4 & frei_e2. Plaetze unveraendert.
Vorschau `_vorschau.png` zeigt nur Gelaendefarben; `_bebaubar.png` gruen halbtransparent, Bestand schwarz, Becken violett.

## t16u Dateien
- `pruef_plaetze_quellen.py`: prüft die Plätze WACHSTUM E16 / AUSBAU E40 (`pruefung/quelle_plaetze_wachstum_ausbau_planm.json`, Plan-m) gegen bebaubar. Ergebnisse: `pruefung/t16u_*`.
- `gen_bauzone_befund.py`: schreibt `overlay_plaetze_erweiterung.json/.csv/.png`. Das ist nur ein Befund, wo die Bauzone nicht reicht; es sind keine eigenen Standorte.
- `BAUPLAN_E100.md`: neu. Ältere Fassungen liegen in `_alt/` (BAUPLAN_E100_t14u.md, BAUPLAN_ABGLEICH.md, gen_bauplan_e100.py, bauplan_e100_bedarf.json, alte overlay_plaetze_erweiterung.*).

## t26u Dateien
- `BAUPLAN_E100.md`: neu auf Plan v4b (Wege-&-Deko-Bot t25u). Vorfassung `_alt/BAUPLAN_E100_t16u.md`.
- Neues Zellfeld `bauzone_plan` (0/1): Zelle ≥50 % in `wege_deko_system/umrechnung_25pxm/bauzone/BB4_plan_v2_25pxm.npy` [S/A]. Nur gelesen.
- `gen_overlay_e100.py` → `pruefung/t26u_*`: Overlay E16/E40/E70/E100 (PNG), Slots gegen Gelände, Brücken, Deko, Wald unter Slots/Wegen, Konflikte bauzone_plan↔bebaubar (beide Richtungen, mit Ursache), Zusammenfassung JSON. Slots, Brücken, Deko nur im Overlay; Gelände bleibt nackt.

## t29u bebaubar_erweitert und Restfehler
- Neues Zellfeld `bebaubar_erweitert` (0/1) [A]: `bebaubar | (begehbar & Untergrund ∈ {SCHNEE,BODEN,SAND} & hindernis==0 & Abstand Wand ≥ 2 m & Abstand Wasser ≥ 2 m)`, **ohne** die Bedingung `senke_becken`; nur 4-zusammenhängende Flächen ≥ 16 Zellen (kleinster Slot 4×4 m) [A].
  - Ausnahme Senke: in der Senke bleibt die bestehende Regel `bebaubar` (keine Änderung).
  - `bebaubar` und `bauzone_plan` bleiben unverändert. Fabian hat die Bauzone nicht entschieden.
  - Höhenstufe ist nicht geprüft: Plateaus über der Nordwand und der Kraterboden zählen mit [A].
  - Stand t29u: z25 54 416 (bebaubar 27 142), z50 15 091 (bebaubar 7 233) [R]. Aktuell t31u: z25 54 409 (27 140), z50 15 056 (7 240) [R].
- Overrides t29u in `overrides_t12u.csv` (Zeilen 31–420), nur z25:
  - 57× SCHNEE→SAND am Rand der Sandbänke im Südfluss (Sandpixel-Anteil ≥ 0,50 [S]);
  - 63× WASSER_EIS→SCHNEE für Eisschollen im Südfluss (Weißanteil min RGB > 225 ≥ 0,60, y 258–285, x < 312 [A]);
  - 270× Schneegipfel westlich der Senke (Umriss c20) → FELS [S].
- `gen_overlay_e100.py` schreibt zusätzlich `anteil_bebaubar_erweitert` je Slot und `pruefung/t29u_bebaubar_erweitert_E100.png`.
- Die Splitter-Prüfliste schreibt gen_raster.py nach /tmp (`unb_split1/2_z25.npy`). Prüfbilder: `pruefung/t29u_*`.

## t30u Ebenen, Findlinge, z50-Overrides

- **Fakt [F]:** Die Senke-Grenze und `bebaubar` bleiben wie sie sind. Bei x=136 und im Nordosten gibt es **keine Gelaendegrenze** (Sicht t29u_rand_x136.png, t29u_rand_nordost.png). Mehr Bauflaeche gibt es nur ueber `bebaubar_erweitert`.
- **Neues Feld `ebene`** [A]: SENKE, PLATEAU_NORD, OSTPLATEAU, KRATER, TAL_SUED, WEST, WAND. Abgeleitet aus den `hoehe_m`-Stufen (alle [A]) und dem Kraterfenster cx71-136/cy92-204. `ebene_hoeher`=1 fuer PLATEAU_NORD und OSTPLATEAU. Das Kraterinnere liegt auf Bezugshoehe [A].
- Zahlen je Ebene: siehe t31u.
- (t30u, ueberholt durch t31u) Luecken-Befund TAL_SUED: siehe t31u.
- **z50:** Die z25-Overrides gelten auch fuer z50 (Regel siehe t31u).

## t31u Talboden Süd, z50-Regel, Datentyp-Fehler
- **TAL_SUED-Regel [S/F]:** Der Südgrat beginnt in c20 bei cx 81. Westlich davon gibt es keine Gratwand. Der Block bei cx 26–55 / cy 223–247 steht frei, das Gelände fällt dort sanft zum Fluss ab (Sicht `pruefung/t31u_talsued_a.png`). Deshalb gilt westlich von cx 81 jetzt **WEST (Bezugshöhe) [A]** statt TAL_SUED. Vorher war cx 26–55 TAL_SUED, das war nicht belegt.
- Schlucht cx 246–249: Ein Bach läuft durch den Grat, und der Talboden ist in c20 durchgehend (`pruefung/t31u_talsued_b.png`). Lücken von höchstens 8 Spalten werden mit der tieferen Startzeile der Nachbarn geschlossen [S].
- Rand cx 329–335: seit t34u TAL_SUED (Schleife bis Kartenrand).
- z25 je Ebene [R]: SENKE 31 265, WEST 29 842, WAND 18 752, TAL_SUED 14 110, PLATEAU_NORD 4 005, OSTPLATEAU 2 014, KRATER 1 820.
- bebaubar_erweitert je Ebene z25 [R]: SENKE 27 140, WEST 17 501, TAL_SUED 5 501, PLATEAU_NORD 2 759, KRATER 1 187, OSTPLATEAU 321.
- **z50-Regel [F]:** Eine z50-Zelle übernimmt eine z25-Override-Regel, wenn mindestens 2 ihrer 4 z25-Zellen sie tragen. Regeln nach FELS (Gipfel, Findling) gelten schon ab 1 von 4, weil nicht begehbar die sicherere Seite ist. Das betrifft 159 z50-Zellen.
- **Fehler behoben:** `untergrund_quelle` wurde als „OVERRI“ abgeschnitten (Datentyp zu kurz), `wand_name` als „Krat/Sued/Ostg“. Jetzt stehen dort OVERRIDE bzw. Krater/Suedgrat/Ostgrat. schema_zelle.json passt jetzt zu den 39 CSV-Spalten, alle Enum-Werte sind geprüft [R].
- Overrides t31u: Zeilen 425–427 (Sandbank-Ränder SCHNEE→SAND, 9 Zellen) [S].

## t34u Ebenen nach Waenden [A]
- `ebene` ∈ SENKE, PLATEAU_NORD, OSTPLATEAU, KRATER, GIPFEL, TAL_SUED, HANG, SIMS, WAND. WEST entfaellt (war Rest auf 0 m, falsch).
- Freie Zellen (keine Wand) werden in 4er-Zusammenhangsteile zerlegt. Getrennt von der grossen Flaeche und noerdlich cy 40: PLATEAU_NORD (+8,6). Im Kraterwall: KRATER (0); Schneekuppe noerdlich: GIPFEL (+7,7). Andere kleine umschlossene Flaechen: SIMS (Mittel der Umgebung).
- Grosse Flaeche: feste Stufen SENKE (senke_becken, 0), TAL_SUED (suedlich Suedgrat bis Kartenrand; westlich cx 81 ab erstem Wasser cy ≥ 252; −7,6), OSTPLATEAU (+6,7). Dazwischen Laplace-Hoehe. Zellen innerhalb 0,5 m einer Stufe und mit ihr verbunden tragen deren Namen, sonst HANG.
- `ebene_hoeher`=1 fuer PLATEAU_NORD, OSTPLATEAU, GIPFEL.
- z25 [R]: SENKE 33 395, HANG 21 148, TAL_SUED 19 234, WAND 18 752, PLATEAU_NORD 5 049, OSTPLATEAU 2 365, KRATER 1 604, GIPFEL 160, SIMS 101.
- z50 [R]: SENKE 8 426, HANG 4 928, TAL_SUED 4 888, WAND 5 367, PLATEAU_NORD 971, OSTPLATEAU 493, KRATER 379, GIPFEL 33, SIMS 51.
- bebaubar_erweitert je Ebene z25 [R]: SENKE 28 269, HANG 13 719, TAL_SUED 7 718, PLATEAU_NORD 3 162, KRATER 1 180, OSTPLATEAU 361.
- begehbar, bebaubar, bebaubar_erweitert unveraendert (z25 62 391 / 27 140 / 54 409; z50 15 245 / 7 240 / 15 056).

## Kamera frei drehbar [F]
- Fabian (t32u): Die Spielkamera lässt sich frei in jeden Blickwinkel drehen [F].
- Folge: Gelände braucht echte Höhen, Wandtexturen, einen Sockel am Kartenrand, Wasserflächen und Normalen. Sprites und Gebäude brauchen Rückseiten.
- Details und offene Fragen: `ANFORDERUNGEN_3D_WELTKARTE.md`.

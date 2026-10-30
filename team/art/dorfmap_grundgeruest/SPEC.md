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
| untergrund | BODEN, GESPERRT, SCHNEE, FELS_WALD, WASSER_EIS, HOF, FEUER, WEG, BRUECKE | aus den Masken unten abgeleitet, Vorrang von links nach rechts steigend [A] |
| zone | A–E | layout_e1_v9/ebenen/10_zonenboden_*_maske.png [S] |
| platz | nr (99 Plätze) | zonen_c20_v9.json `plaetze[].poly` [S] |
| weg_id / weg_klasse | G001…, haus_A11 … / GASSE, ANBINDUNG, HAUSWEG | 20_wege_*_maske.png [S]; Breiten 2,4/1,8/1,2 „m“ stehen in v9 noch auf der 30-px-Basis, das sind real 2,9/2,2/1,4 m [R] |
| hindernis | Index in hindernisse_c20_v2.json (Schneehügel, Eisriss, Moos) | slots_c20/hindernisse_c20_v2.npz [S]; deckt nur das Fenster der Bauzone ab |
| wasser_eis | 0/1 | arbeit/bach_schutz.npy [S]. **Wasser und Eis lassen sich per Farbe nicht trennen** [S PLAN_LOOK_SYSTEM_v1]; das Feld bedeutet „Bach/See inkl. Schutzband“ [A] |
| schnee | 0/1 | arbeit/F4.npy [S] |
| senke_bb4 | 0/1 | arbeit/BB4.npy (Senke/Bauzone) [S] |
| h4_ext | 0/1 | arbeit/H4_ext.npy [S]; Bedeutung nicht dokumentiert [A] |
| frei_e2 | 0/1 | slots_c20/mp/frei_e2.npy (ohne Fels, Wald, Wasser, Schluchtpfad) [S] |
| begehbar | 0/1 | [R]: nicht GESPERRT, WASSER_EIS, FELS_WALD oder Hindernis; WEG und BRUECKE sind immer begehbar |
| bebaubar | 0/1 | [R]: senke_bb4 ∧ frei_e2 ∧ ¬Wasser ∧ ¬Fels ∧ ¬Hindernis ∧ ¬Weg ∧ ¬Brücke ∧ ¬Feuer |
| hoehe_stufe | leer | **Es gibt keine Höhenkarte** [S AD_ANTWORT]; der Wert muss von Hand gesetzt werden [A] |
| klippe | leer | Die Klippenmaske ist nur grob [S]; Kanten werden von Hand gesetzt [A] |
| skin_slot | ug_<untergrund> | Brücke zum Skin-System (Abschnitt 5) |

Zählung bei 25 px [R, raster_c20_z25_meta.json]: GESPERRT 61 555, SCHNEE 20 454, BODEN 9 040, FELS_WALD 5 999, WEG 2 825, WASSER_EIS 1 214, HOF 430, FEUER 271, BRUECKE 20. Davon begehbar 32 414 und bebaubar 19 931.

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
- Für eine eigene Epochen-Karte gibt es den Meta-Parameter `epochen_variante` (null = c20/E1).

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

## 7 Offene Entscheidungen
1. **Epochen: eigene Karte (26.10.) oder gleiche Karte mit anderem Look (30.10.)?**
   - a) Eine Karte, nur Skins: Das Raster bleibt fest, das ist am einfachsten.
   - b) Eigene, größere Karte je Epoche: Je Karte läuft der Generator mit `epochen_variante`, die Felder bleiben gleich.
   - c) Mischform: c20 bleibt der Kern, später kommen Randflächen als zusätzliche Zellen dazu (das Raster wächst nach außen, cx/cy werden verschoben).
2. **Zellmaß:**
   - a) 25 px = 1 m: fein genug für kleine Felsen und Hauswege, 102 k Zellen.
   - b) 50 px = 2 m: leichter, aber Hauswege (≈1,4 m) und kleine Felsen gehen verloren.
   - c) 12,5 px = 0,5 m: genau für Türen und Figuren, aber 4× Datenmenge.
3. **Höhe und Klippe:**
   - a) Von Hand in Stufen 0–3 setzen, ohne Kosten, Aufwand etwa 1 Tag.
   - b) Aus der Schattierung der Karte schätzen: ungenau, muss als [A] markiert werden.
   - c) Erst einmal weglassen: Das Spiel nutzt nur begehbar/bebaubar.
4. **Wasser gegen Eis:**
   - a) Bleibt ein gemeinsames Feld, die Unterscheidung macht der Skin.
   - b) Wasser und Eis von Hand trennen (Bach offen gegen See gefroren).
   - c) Dem Bach-Polygon (frei_e2.py) die Eigenschaft „fließend“ geben, dem See „gefroren“.
5. **Weg-Meter auf 25 px/m umstellen:**
   - a) Die Breiten in v9 neu in Metern angeben, Masken bleiben gleich.
   - b) Die alte Angabe (30-px-Meter) mit Umrechnungsfaktor 1,2 behalten.

## Dateien
- `gen_raster.py`: Generator, liest nur, schreibt nur in diesen Ordner.
- `raster_c20_z25_zellen.csv` (101 808 Zeilen) und `raster_c20_z25_meta.json`.
- `schema_zelle.json`
- `raster_c20_z25_vorschau.png`: Flachfarben plus Legende, schraffiert = bebaubar. Dazu `raster_c20_z50_*`.

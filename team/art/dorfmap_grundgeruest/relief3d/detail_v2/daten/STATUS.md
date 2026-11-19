# STATUS P4 Datenschicht detail_v2

Stand **Do 19.11.2026, 14:54 Europe/Berlin** (Do-Teil ohne Vektoren/Mesh). Bearbeiter: Epochen Tools. Auftrag: Epochen Dorfmap-Grundgerüst (P4, DETAIL_V2_PLAN.md 3.3/9).
Basis `art/dorfmap-fertig` @ d2d4824, Branch `art/dv2-daten`. Marker: [S] gemessen/Quelle, [A] Annahme, [R] gerechnet, [F] Entscheidung.

**Kostenzeile:** 0 €. Kein Codex-Lauf. Laufzeit Do 19.11.2026 14:46–14:54 Europe/Berlin (Epochen Tools, Box-CPU, Node 24 / Python 3 mit numpy, shapely 2.2, Pillow 12).

## Fertig (Do)

- `legende.json`: Flächenklassen 0–5 mit Farben und Priorität, Untertyp `untergrund` (Schnee, Wald, Boden, Sand + Alt-Zuordnung), Slot-Bitfeld, Maßstab, Kachelschema (56 Kacheln, Schnitte x = 42·i, z = 43·j, Zeile 7 bis 303), Quellen mit Git-Blob + SHA-256.
- `slots.json` + `baue_legende_slots.py` (reproduzierbar, `--pruefe` = aktuell):
  - **99 Plätze**, davon **97 Bauplätze** (mit `bauplatz`-Zellen), 2 Plätze ohne Bauplatz-Zelle (D15D, D16). **3 292 Bauplatz-Zellen.** [S]
  - **627 Deko-Slots** (je 1 Zelle aus `dekoplaetze_netz`; 626 4-Komponenten, ein Paar liegt nebeneinander). [S]
  - Abgleich gegen `raster_c20_z25_meta.json` (plaetze 99, dekoplaetze_netz 627) und Plan Abschnitt 2 (bauplatz 3 292): alle gleich. Keine Zelle doppelt belegt, keine Deko-Zelle in einem Platz. [S]
  - `slot.png` (3360 × 3030, 16 bit) wird per `--slot-png` erzeugt und per Rücklesen geprüft (59 KB), aber **nicht committet** (Vorgabe: PNGs erst bei echter Vektor/Mesh-Herkunft). Die Slots selbst sind zellbasiert, die PNG wäre also schon endgültig – Freigabe zum Committen durch Grundgerüst offen. [A]
- `query.mjs` (ESM, Node + Browser): Schnittstelle `queryPoint(x,z)` → `{hoehe, flaeche, untergrund, begehbar, slot, kachel}`. Fertig: Kachel-ID, Maßstab/Pixel/UV1, Bereichsprüfung (RangeError außerhalb), Slot-Dekodierung (mit `slots.json`), Mesh-Gitterindex mit baryzentrischer Höhe (an synthetischem Mesh exakt), `hoehe.png`-Weg mit Offset/Skala, Lader `ladeDatenschicht()` (fehlende Datei → Wert `null`, nichts vorgetäuscht).
- `png.mjs`: PNG-Decoder ohne Abhängigkeiten (Node zlib / Browser DecompressionStream). Geprüft mit eigenem Encoder (1/8/16 bit, Filter 0–4) und mit der von Pillow geschriebenen `slot.png` (alle 4 058 Slot-Zellen über `queryPoint` richtig).
- `baue_masken.py`: Gerüst. Quellenprüfung (`--pruefe-quellen`, Exit 2 solange Quellen fehlen) und Prioritäts-Rasterung an Pixelmitten (`--selbsttest` ok). Die Zuordnung GeoJSON-Eigenschaft → Klasse fehlt bewusst, weil das P1-Schema noch nicht vorliegt.

## Tests (`node --test`, Do 14:54)

17 Tests: **12 grün, 3 skip, 2 todo, 0 rot.** Mit `DV2_SLOT_PNG=/tmp/dv2_daten/slot.png`: 13 grün, 2 skip, 2 todo.
- grün: Kachel-ID an festen Punkten (Dorfkern 209|118 = E3, E3-Wasser 189|100 = E3, Brücke E2 192|74,5 = E2, Nordwand 206,5|35,5 = E1, D2-Mitte 147|64,5 = D2), Kartenränder/Schnittlinien, Bereichsfehler, Maßstab/UV1, Legende ↔ query.mjs, Slot-Zählung, Slot D2-Mitte = A19 (Bauplatz), Slot-Bits, PNG-Decoder, Mesh-Index, leere Datenschicht, Lader.
- skip: `slot.png` an festen Punkten (Datei nicht committet), Masken an festen Punkten (wartet P1+P2), Höhe aus Mesh (wartet P2).
- todo: Q11 Höhe vs. Mesh-Strahl ≤ 2 cm an 10 000 Zufallspunkten; Q11 Flächentyp = Dreiecksklasse ≥ 99,5 %.
- Python: `baue_masken.py --selbsttest` ok, `baue_legende_slots.py --pruefe` aktuell.
- Regression: `git diff d2d4824 --stat -- . ':!team/art/dorfmap_grundgeruest/relief3d/detail_v2/daten'` = leer (alte Dateien unverändert). Altes Raster-Gate nicht neu gerechnet, weil keine alte Datei berührt ist.

## Quellen (Pfad, Git-Blob @ d2d4824)

| Quelle | Pfad | Git-Blob | genutzt für |
|---|---|---|---|
| Overlay Plätze/Wege (E1, c20, z25) | `team/art/dorfmap_grundgeruest/raster_c20_z25_overlay_plaetze_wege.csv` | 996a818df38e9c69307016e958a1236d781a24e2 | platz, bauplatz, dekoplaetze_netz, hof, feuer |
| Zellendaten | `team/art/dorfmap_grundgeruest/relief3d/zellen_relief.csv` | 3095a63bdf903808cca50626c6beddd1257a6731 | deko_baum_ok, deko_fels_ok, untergrund (Zählung) |
| Raster-Meta | `team/art/dorfmap_grundgeruest/raster_c20_z25_meta.json` | ee7fb9c970f9af80b3f0735cb952dc15786329e1 | Sollzahlen 99 / 627 |
| Kachelgrenzen | `relief3d/pruefung/alle_kacheln/baue_alle_kacheln.py` `kachel_grenzen()` | – | Kachelschema |
| Zellzuordnung | `relief3d/main.js` Z. 317/324 `zelle()` | – | Zelle = floor(x), floor(z) |

SHA-256 je Quelle steht in `legende.json` → `quellen`.

## Offene Punkte / Befunde

1. **Masken fehlen bis Fr** (`flaeche`, `begehbar`, `untergrund`, `hoehe`): Quellen `detail_v2/vektor/{wege,kreuzungen,wasser,ufer,zonen,kanten,grat}.geojson` (P1a/b/c, Do 19:00) und `detail_v2/mesh/manifest.json` + Kachel-.glb (P2, Fr ~10–12) liegen noch nicht vor.
2. **Q11 Flächentyp = Dreiecksklasse** braucht eine Klasse je Dreieck im P2-Export (z. B. glTF-Attribut oder Primitive je Klasse). Format mit Art Umgebung (P2) klären, sonst ist die 99,5-%-Prüfung nicht messbar.
3. **Slot-Bitfeld** (Bits 0–11 ID, 12 Baum, 13 Fels, 14 Bauplatz-Zelle) und **`untergrund.png` als Zusatzdatei** sind [A]-Vorschläge von Tools; Freigabe durch Grundgerüst/Rechner offen. Begründung: `flaeche.png` ist laut Auftrag auf 0–5 festgelegt, `untergrund` braucht daher eine eigene Datei.
4. **Untergrund-Quelle**: Alt-Werte sind 1-m-Zellen (`zellen_relief.csv`). Ob P1c (`zonen.geojson`) den Untertyp als Polygon liefert, ist offen. Ohne Polygone wäre `untergrund.png` blockig (1 m) – dann im Viewer nur als Untertyp, nicht als Kante verwenden.
5. `deko_fels_ok` ist in `zellen_relief.csv` identisch mit `begehbar` (62 333 Zellen) [S]; `deko_baum_ok` nur auf SCHNEE (32 435) und BODEN (534). Übernommen wie in der Quelle.
6. `overlay_plaetze_erweiterung.json` (136 Einträge, Stände E16/E40, eigene ID-Nummern) ist **nicht** in `slots.json`: Es beschreibt Ausbau-Plätze späterer Epochen, die Dorfmap ist E1. Wenn E16/E40-Slots gewünscht sind, bitte festlegen.
7. Brückenfläche: Overlay `bruecke` hat 20 Zellen (E2 x 186–197 | z 72–75, E3-West x 174–186 | z 126–129); der Plan nennt 25/27 Boxen. Für `flaeche = 5` gilt Fr die Brückengeometrie aus P2/P5, nicht das Overlay.
8. Repo: `art/dorfmap-fertig` liegt in **Xenatosa/Planer** (origin), nicht in Xenatosa/epodarien. Der PR geht deshalb nach Planer.

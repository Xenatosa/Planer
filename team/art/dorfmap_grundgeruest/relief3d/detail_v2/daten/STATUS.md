# STATUS P4 Datenschicht detail_v2

Stand **Do 19.11.2026, 15:00 Europe/Berlin** (Do-Teil ohne Vektoren/Mesh, Nachtrag nach Entscheidungen Grundgerüst). Bearbeiter: Epochen Tools. Auftrag: Epochen Dorfmap-Grundgerüst (P4, DETAIL_V2_PLAN.md 3.3/9).
Basis `art/dorfmap-fertig` @ d2d4824, Branch `art/dv2-daten`. Marker: [S] gemessen/Quelle, [A] Annahme, [R] gerechnet, [F] Entscheidung.

**Kostenzeile:** 0 €. Kein Codex-Lauf. Laufzeit Do 19.11.2026 14:46–14:54 und 14:55–15:00 Europe/Berlin (Epochen Tools, Box-CPU, Node 24 / Python 3 mit numpy, shapely 2.2, Pillow 12).

## Entscheidungen Grundgerüst (19.11.2026, nach Commit 238c901) [F über Grundgerüst]

1. P2 exportiert je Vertex das glTF-Attribut `_FLAECHE` (0–5), Dreiecke an Kanten klassenrein, Klassenliste im manifest. → `glb.mjs` liest `_FLAECHE`, `baueMeshIndex(..., flaechen)` liefert `klasseAus()`/`gemischteDreiecke()`, `pruefeDreiecksklasse()` misst Q11 (synthetisch getestet).
2. `zonen.geojson` bekommt Untergrund-Polygone (Property `untergrund`: Schnee/Wald/Boden/Sand); 1-m-Fallback aus `zellen_relief.csv` nur, falls sie fehlen. → in `baue_masken.py` umgesetzt.
3. Slot-Bitfeld bestätigt: Bit 0–11 ID, 12 Baum, 13 Fels, 14 Bauplatz-Zelle, 15 reserviert. → `legende.json` Status „abgestimmt“.
4. `untergrund.png` als Zusatzdatei ok. → in `legende.json` aufgenommen.
5. `slot.png` jetzt committen. → committet (59 KB, 3360 × 3030, 16 bit).
6. GeoJSON-Schema bis Do 19:00: FeatureCollection, Viewer-Meter (1 Einheit = 1 Zelle, Ursprung Weltecke wie UV1), Properties `klasse` (0–5), `untergrund`, `id`. → `baue_masken.py` liest und prüft genau dieses Schema (Klasse 0–5, Untergrundname, Polygon gültig, Koordinaten in 0–336 | 0–303 m, sonst Fehler mit Datei + id).

## Fertig (Do)

- `legende.json`: Flächenklassen 0–5 mit Farben und Priorität, Untertyp `untergrund` (Schnee, Wald, Boden, Sand + Alt-Zuordnung), Slot-Bitfeld, Maßstab, Kachelschema (56 Kacheln, Schnitte x = 42·i, z = 43·j, Zeile 7 bis 303), Quellen mit Git-Blob + SHA-256.
- `slots.json` + `baue_legende_slots.py` (reproduzierbar, `--pruefe` = aktuell):
  - **99 Plätze**, davon **97 Bauplätze** (mit `bauplatz`-Zellen), 2 Plätze ohne Bauplatz-Zelle (D15D, D16). **3 292 Bauplatz-Zellen.** [S]
  - **627 Deko-Slots** (je 1 Zelle aus `dekoplaetze_netz`; 626 4-Komponenten, ein Paar liegt nebeneinander). [S]
  - Abgleich gegen `raster_c20_z25_meta.json` (plaetze 99, dekoplaetze_netz 627) und Plan Abschnitt 2 (bauplatz 3 292): alle gleich. Keine Zelle doppelt belegt, keine Deko-Zelle in einem Platz. [S]
  - `slot.png` (3360 × 3030, 16 bit, 59 KB) per `--slot-png slot.png` erzeugt, per Rücklesen geprüft und **committet** (Freigabe Grundgerüst 19.11.).
- `query.mjs` (ESM, Node + Browser): Schnittstelle `queryPoint(x,z)` → `{hoehe, flaeche, untergrund, begehbar, slot, kachel}`. Fertig: Kachel-ID, Maßstab/Pixel/UV1, Bereichsprüfung (RangeError außerhalb), Slot-Dekodierung (mit `slots.json`), Mesh-Gitterindex mit baryzentrischer Höhe (an synthetischem Mesh exakt), `hoehe.png`-Weg mit Offset/Skala, Lader `ladeDatenschicht()` (fehlende Datei → Wert `null`, nichts vorgetäuscht).
- `png.mjs`: PNG-Decoder ohne Abhängigkeiten (Node zlib / Browser DecompressionStream). Geprüft mit eigenem Encoder (1/8/16 bit, Filter 0–4) und mit der von Pillow geschriebenen `slot.png` (alle 4 058 Slot-Zellen über `queryPoint` richtig).
- `baue_masken.py`: auf das abgestimmte Schema eingestellt. Liest alle `detail_v2/vektor/*.geojson`, rastert Polygon-Features mit `klasse` nach Priorität an Pixelmitten → `flaeche.png`; `untergrund` → `untergrund.png` (0 unter Wasser/Fels/Brücke [A], Fallback 1 m nur ohne Polygone, im Lauf ausgewiesen); `begehbar.png` vorerst nur aus der Fläche (Wasser, Fels/Klippe = 0) [A]. Linien/Punkte werden nicht gerastert. `--ohne-mesh` erlaubt den Lauf vor P2. `hoehe.png` und Neigungsgrenze für `begehbar` folgen mit dem Mesh. `--selbsttest` (synthetische FeatureCollections inkl. Schemafehlern) ok; `--pruefe-quellen` Exit 2, solange Vektoren fehlen.
- `glb.mjs`: glb-Leser (POSITION, Indizes, `_FLAECHE`), Kacheln zusammenführen; bricht bei Node-Transformation oder `_FLAECHE` > 5 ab.

## Tests (`node --test`, Do 15:00)

19 Tests: **15 grün, 3 skip, 1 todo, 0 rot** (ohne Env-Variable; `slot.png` liegt jetzt im Ordner).
- grün zusätzlich: `slot.png` an festen Punkten (alle 4 058 Slot-Zellen), glb-Leser mit `_FLAECHE`, Dreiecksklasse/Q11-Quote (synthetisch: 100 % bei passendem Raster, < 99,5 % bei 2 m Versatz, gemischtes Dreieck erkannt), Legende abgestimmt.
- grün: Kachel-ID an festen Punkten (Dorfkern 209|118 = E3, E3-Wasser 189|100 = E3, Brücke E2 192|74,5 = E2, Nordwand 206,5|35,5 = E1, D2-Mitte 147|64,5 = D2), Kartenränder/Schnittlinien, Bereichsfehler, Maßstab/UV1, Legende ↔ query.mjs, Slot-Zählung, Slot D2-Mitte = A19 (Bauplatz), Slot-Bits, PNG-Decoder, Mesh-Index, leere Datenschicht, Lader.
- skip: Masken an festen Punkten (wartet P1+P2), Höhe aus Mesh (wartet P2), Q11 Flächentyp am echten Mesh (wartet P2 + `flaeche.png`; Manifest-Einbindung Fr).
- todo: Q11 Höhe vs. Mesh-Strahl ≤ 2 cm an 10 000 Zufallspunkten.
- Python: `baue_masken.py --selbsttest` ok, `baue_legende_slots.py --pruefe` aktuell.
- Erster Stand (238c901): 17 Tests, 12 grün, 3 skip, 2 todo.
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

1. **Masken fehlen bis Fr** (`flaeche`, `begehbar`, `untergrund`, `hoehe`): Quellen `detail_v2/vektor/*.geojson` (P1a/b/c, Do 19:00) und `detail_v2/mesh/manifest.json` + Kachel-.glb (P2, Fr ~10–12) liegen noch nicht vor.
2. **Manifest-Format P2**: Pfade der Kachel-.glb und Klassenliste im manifest sind noch nicht bekannt; Einbindung in den Q11-Test Fr. `glb.mjs` erwartet Welt-Meter ohne Node-Transformation.
3. *(erledigt)* Slot-Bitfeld und `untergrund.png` abgestimmt (s. Entscheidungen).
4. *(erledigt)* Untergrund als Polygone in `zonen.geojson`; 1-m-Fallback nur ohne Polygone.
4a. `begehbar.png` heute nur aus der Fläche [A]; die Neigungsgrenze (z. B. aus `begehbar_3d`-Regel) kommt mit dem Mesh und ist noch festzulegen.
5. `deko_fels_ok` ist in `zellen_relief.csv` identisch mit `begehbar` (62 333 Zellen) [S]; `deko_baum_ok` nur auf SCHNEE (32 435) und BODEN (534). Übernommen wie in der Quelle.
6. `overlay_plaetze_erweiterung.json` (136 Einträge, Stände E16/E40, eigene ID-Nummern) ist **nicht** in `slots.json`: Es beschreibt Ausbau-Plätze späterer Epochen, die Dorfmap ist E1. Wenn E16/E40-Slots gewünscht sind, bitte festlegen.
7. Brückenfläche: Overlay `bruecke` hat 20 Zellen (E2 x 186–197 | z 72–75, E3-West x 174–186 | z 126–129); der Plan nennt 25/27 Boxen. Für `flaeche = 5` gilt Fr die Brückengeometrie aus P2/P5, nicht das Overlay.
8. Repo: `art/dorfmap-fertig` liegt in **Xenatosa/Planer** (origin), nicht in Xenatosa/epodarien. Der PR geht deshalb nach Planer.

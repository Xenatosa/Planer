# STATUS P4 Datenschicht detail_v2

Stand **Do 19.11.2026, 15:07 Europe/Berlin** (Do-Teil ohne echte Vektoren/Mesh; Nachträge nach Entscheidungen Grundgerüst 1 und 2). Bearbeiter: Epochen Tools. Auftrag: Epochen Dorfmap-Grundgerüst (P4, DETAIL_V2_PLAN.md 3.3/9).
Basis `art/dorfmap-fertig` @ d2d4824, Branch `art/dv2-daten`. Marker: [S] gemessen/Quelle, [A] Annahme, [R] gerechnet, [F] Entscheidung.

**Kostenzeile:** 0 €. Kein Codex-Lauf. Laufzeit Do 19.11.2026 14:46–14:54, 14:55–15:00 und 15:00–15:07 Europe/Berlin (Epochen Tools, Box-CPU, Node 24 / Python 3 mit numpy, shapely 2.2, Pillow 12).

## Entscheidungen Grundgerüst (19.11.2026, nach Commit 238c901) [F über Grundgerüst]

1. P2 exportiert je Vertex das glTF-Attribut `_FLAECHE` (0–5), Dreiecke an Kanten klassenrein, Klassenliste im manifest. → `glb.mjs` liest `_FLAECHE`, `baueMeshIndex(..., flaechen)` liefert `klasseAus()`/`gemischteDreiecke()`, `pruefeDreiecksklasse()` misst Q11 (synthetisch getestet).
2. `zonen.geojson` bekommt Untergrund-Polygone (Property `untergrund`: Schnee/Wald/Boden/Sand); 1-m-Fallback aus `zellen_relief.csv` nur, falls sie fehlen. → in `baue_masken.py` umgesetzt.
3. Slot-Bitfeld bestätigt: Bit 0–11 ID, 12 Baum, 13 Fels, 14 Bauplatz-Zelle, 15 reserviert. → `legende.json` Status „abgestimmt“.
4. `untergrund.png` als Zusatzdatei ok. → in `legende.json` aufgenommen.
5. `slot.png` jetzt committen. → committet (59 KB, 3360 × 3030, 16 bit).
6. GeoJSON-Schema bis Do 19:00: FeatureCollection, Viewer-Meter (1 Einheit = 1 Zelle, Ursprung Weltecke wie UV1), Properties `klasse` (0–5), `untergrund`, `id`. → `baue_masken.py` liest und prüft genau dieses Schema (Klasse 0–5, Untergrundname, Polygon gültig, Koordinaten in 0–336 | 0–303 m, sonst Fehler mit Datei + id).

## Entscheidungen Grundgerüst, Teil 2 (19.11.2026, nach Commit f5a137b) [F über Grundgerüst]

1. `mesh/manifest.json`-Schema festgelegt (version 1, einheit m, ursprung weltecke, karte 336 × 303, klassen 0–5, attribute.flaeche `_FLAECHE`, uv, kacheln[id, glb, bbox, dreiecke, klassen_anteil], modelle[id, glb, klasse]). `_FLAECHE` uint8 oder float, Dreiecke klassenrein (doppelte Vertices an Klassengrenzen).
   → `manifest.mjs` (JS) und `mesh_raster.py` (Python): Schemaprüfung (inkl. bbox = Kachelgrenzen, Pfade relativ ohne `..`), Lesen aller Kachel-/Modell-.glb, Abgleich `dreiecke`, Klassenreinheit, `vollstaendig` = 56 Kacheln. float-`_FLAECHE` muss ganzzahlig 0–5 sein.
2. begehbar = Klasse ∉ {3, 4} UND Neigung ≤ 35°. → `begehbarRegel()` in `query.mjs`, `begehbar_regel()` in `mesh_raster.py`; `baue_masken.py` nutzt Fläche (Vektoren + Brücken-Deck) und Mesh-Neigung. Pixel ohne Mesh-Treffer = nicht begehbar (gezählt in `masken_meta.json`).
3. Brücke (5) begehbar auf dem Deck, Höhe = Deck: Modelle aus `manifest.modelle` gelten in ihrem Fußabdruck für Höhe, Neigung und Fläche (überschreibt Wasser). Deck-Regel [A]: unter den Aufwärtsflächen (Normale y ≥ 0,5, glTF-Wicklung CCW) die höchste, die höchstens 0,5 m über der tiefsten liegt → Bohle statt Träger darunter, nicht Handlauf/Pfosten darüber. Bohlenfugen (1 cm): JS sucht ±2 cm, Python schließt den Fußabdruck um 1 px und übernimmt die Höhe des nächsten Deckpixels. **Voraussetzung an P5:** Modelle mit korrekter Außen-Wicklung, Deck ≤ 0,5 m über Trägeroberseite.
4. Abgleich mit `begehbar_3d` nur als Bericht: `abgleich_begehbar_3d.json` (1-m-Zelle begehbar bei ≥ 50 % Pixel), Abweichung > 1 % → Warnung auf stderr + `warnung: true`, keine harte Regel.

## Folge-PR Do 19.11.2026 abends: Befund Grundgerüst (GASSE, Zellen-Masken, F10) [F über Grundgerüst]

Branch `art/dv2-daten-masken` von `art/dorfmap-fertig` @ bf9f62d (#52 und #61 gemergt). **Kostenzeile:** 0 €, kein Codex, Laufzeit Do 19.11.2026 18:39–18:52 Europe/Berlin (Epochen Tools, Box-CPU).

1. **Weg-Typ statt Flächenklasse:** In `wege.geojson` ist `klasse` der P1a-Weg-Typ (GASSE 40, ANBINDUNG 11, HAUSWEG 10 Band-Polygone). `lies_features()` bildet nicht-numerische `klasse` **nur in wege.geojson** auf Flächenklasse 1 ab und behält den Typ als `weg_typ` → `weg_typ.png` (1 HAUSWEG, 2 ANBINDUNG, 3 GASSE; GASSE gewinnt bei Überlappung; nur wo `flaeche` = Weg) und `masken_meta.weg_typen`. Unbekannter Typ → 1 mit WARNUNG; in anderen Dateien bleibt nicht-numerische `klasse` ein Fehler. Quelldatei unverändert.
2. **Bauzone/Slots aus Zelllisten (#61):** `lies_zellen_punkte()` liest Punkte mit `zellen` [[cx, cz]] (geprüft: ganzzahlig, im Kartenbereich, ohne Doppelte, `flaeche_m2` = Zellzahl) → `bauzone.png` (1 bit, 25 Punkte, 31 893 Zellen) und `slot_zonen.png` (1 Bau, 2 Deko). Abgleich gegen `slot.png`/`slots.json` → `abgleich_slots.json`: Bau 3 292 = 3 292 Zellen, 97/97 IDs, 0 Abweichungen; Deko 627 = 627 Zellen, 0 Abweichungen, aber 626 Punkte für 627 Slots: `slot_deko_0532` fasst das bekannte Nachbarpaar (2 Zellen, IDs inkl. 1538) zusammen. #61 hatte `baue_masken.py` **nicht** geändert (nur zonen.geojson/kanten-Skripte) – nichts doppelt gebaut.
3. **F10:** Wasserspiegel zählt nur, wo er über dem Gelände liegt. `mesh_raster.rastere()` führt oberste Wasser- und oberste Gelände-Fläche getrennt (Wasser nur bei y_wasser > y_gelände, Gleichstand → Gelände); `baue_masken.py` setzt Vektor-Wasser dort auf die Mesh-Gelände-Klasse (`f10_wasser_zu_gelaende_px`). `query.mjs`: `baueMeshIndex` gleiche Regel (`f10Aus()`), `queryPoint` ersetzt `flaeche.png`=Wasser durch die Mesh-Klasse, `flaecheRoh()` für Q11 (ehrlicher Rastervergleich). Ohne Mesh nicht anwendbar (in `masken_meta` ausgewiesen).
4. **Masken ohne Mesh committet** in `masken_ohne_mesh/` (zusammen ≈ 0,3 MB, wie `slot.png` klein; Quellen-Blobs in `QUELLE.md`).

**Klassenanteile (ohne Mesh) [S]:** Grund 63,78 %, Weg 5,26 %, Ufer 5,06 %, Fels/Klippe 19,35 %, Wasser 6,51 %, Brücke 0,03 %. Untergrund aus 46 Polygonen.
**Befunde:**
- Fels/Klippe 19,35 % ist deutlich mehr als die 13 296 Fels-/Wand-Zellen der alten Daten: 11 545 neue Fels-Zellen sind dort SCHNEE ohne Klippe, aber `untergrund_c20` = KLIPPE_WAND/KANTE, `begehbar` 0, `begehbar_3d` 1. #61 baut Fels aus c20 – bitte entscheiden, ob Fels/Klippe (nicht begehbar) für diese Zellen gewollt ist.
- Abgleich begehbar (ohne Neigung) gegen `begehbar_3d`: 30,6 % abweichend (19 426 neu begehbar/alt nicht, 11 725 umgekehrt) → WARNUNG; mit Mesh-Neigung Fr neu.
- Brücken in den Vektoren sind P5-Platzhalter (34 m²); Fixpunkt `bruecke_e2` (192|74,5) ist ohne Mesh Ufer, die Brücke gilt Fr über das Deck.

**Tests (frischer Lauf 18:49):** `node --test` 25 Tests: 21 grün, 3 skip, 1 todo, 0 rot (neu: F10 synthetisch; Masken ohne Mesh an festen Punkten inkl. aller 4 058 Slot-Zellen aus slots.json gegen `slot_zonen.png`). `python3 baue_masken.py --selbsttest` ok (neu: GASSE/HAUSWEG/unbekannter Typ, Fehler bei GASSE außerhalb wege.geojson, Zellpunkte, F10 mit Fake-Mesh). `baue_legende_slots.py --pruefe` aktuell.
**Offen (Fr ab Mittag, nach `art/dv2-mesh`):** `hoehe.png`, Masken mit Mesh (F10 wirkt dann real), Q11-Tests.

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
- `glb.mjs`: glb-Leser (POSITION, Indizes, Attributname aus dem manifest, uint8 oder float), Kacheln zusammenführen; bricht bei Node-Transformation oder Wert ≠ ganzzahlig 0–5 ab.
- `manifest.mjs`: `pruefeManifest()`, `ladeMesh()` → `gelaende` (Kacheln + Brücken-Deck) mit `hoeheAus/klasseAus/neigungAus/begehbarAus/deckAus`.
- `mesh_raster.py`: manifest/glb in Python, vektorisierte Rasterung an Pixelmitten (oberste Fläche, Neigung, Klasse, Deck). Benchmark: 3,26 Mio. Dreiecke (0,25-m-Gitter, 2× Budget) in 5,6 s, 1,3 GB RAM, 0 Lücken, Höhenabweichung ≤ 0,5 mm gegen die Funktion.
- `baue_masken.py` mit Mesh: zusätzlich `hoehe.png` (Skala 1 mm, Offset/Skala in `masken_meta.json`), `begehbar.png` nach Regel, Brücken-Deck in `flaeche.png`, `abgleich_begehbar_3d.json`.

## Tests (`node --test`, Do 15:06)

23 Tests: **19 grün, 3 skip, 1 todo, 0 rot.**
- neu grün (synthetisch, Fake-Manifest mit Kacheln A1/A2 + `bruecke_E2`): Manifest-Schemaprüfung (8 Fehlerfälle), `ladeMesh` mit `_FLAECHE` uint8 und float, Fehler bei falscher `dreiecke`-Zahl/`ursprung`, begehbar-Regel (40°-Hang nicht, 30°-Hang begehbar, Wasser nicht), Brücken-Deck (Höhe 0,5 m statt Wasser −0,3 / Träger 0,45 / Handlauf 1,5; Klasse 5; begehbar; Fugensuche).
- Python `baue_masken.py --selbsttest`: gleiche Fake-Geometrie inkl. float-`_FLAECHE`, Brücken-Deck in flaeche/hoehe/begehbar/untergrund, `hoehe.png` (max. Quantisierung 0,5 mm), Abgleich-Bericht (Warnung greift), Schema-/Dreiecksfehler → ok.
- grün zusätzlich: `slot.png` an festen Punkten (alle 4 058 Slot-Zellen), glb-Leser mit `_FLAECHE`, Dreiecksklasse/Q11-Quote (synthetisch: 100 % bei passendem Raster, < 99,5 % bei 2 m Versatz, gemischtes Dreieck erkannt), Legende abgestimmt.
- grün: Kachel-ID an festen Punkten (Dorfkern 209|118 = E3, E3-Wasser 189|100 = E3, Brücke E2 192|74,5 = E2, Nordwand 206,5|35,5 = E1, D2-Mitte 147|64,5 = D2), Kartenränder/Schnittlinien, Bereichsfehler, Maßstab/UV1, Legende ↔ query.mjs, Slot-Zählung, Slot D2-Mitte = A19 (Bauplatz), Slot-Bits, PNG-Decoder, Mesh-Index, leere Datenschicht, Lader.
- skip: Masken an festen Punkten (wartet P1+P2), Höhe aus Mesh (wartet P2), Q11 Flächentyp am echten Mesh – lädt `../mesh/manifest.json` (oder `DV2_MANIFEST`), prüft 56 Kacheln, 0 gemischte Dreiecke, Quote ≥ 99,5 %; läuft automatisch, sobald manifest + `flaeche.png` da sind.
- todo: Q11 Höhe vs. Mesh-Strahl ≤ 2 cm an 10 000 Zufallspunkten.
- Python: `baue_masken.py --selbsttest` ok, `baue_legende_slots.py --pruefe` aktuell.
- Erster Stand (238c901): 17 Tests, 12 grün, 3 skip, 2 todo. Stand f5a137b: 19 Tests, 15 grün, 3 skip, 1 todo.
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
2. *(erledigt)* Manifest-Format festgelegt und eingebunden. `glb.mjs`/`mesh_raster.py` erwarten Welt-Meter ohne Node-Transformation (sonst Fehler).
3. *(erledigt)* Slot-Bitfeld und `untergrund.png` abgestimmt (s. Entscheidungen).
4. *(erledigt)* Untergrund als Polygone in `zonen.geojson`; 1-m-Fallback nur ohne Polygone.
4a. *(erledigt)* begehbar-Regel mit Neigung ≤ 35° festgelegt und umgesetzt.
4b. Offen bis Fr: Q11-Höhe gegen unabhängigen Mesh-Strahl (todo); Deck-Regel an den echten P5-Brücken prüfen (Wicklung, Fenster 0,5 m).
5. `deko_fels_ok` ist in `zellen_relief.csv` identisch mit `begehbar` (62 333 Zellen) [S]; `deko_baum_ok` nur auf SCHNEE (32 435) und BODEN (534). Übernommen wie in der Quelle.
6. `overlay_plaetze_erweiterung.json` (136 Einträge, Stände E16/E40, eigene ID-Nummern) ist **nicht** in `slots.json`: Es beschreibt Ausbau-Plätze späterer Epochen, die Dorfmap ist E1. Wenn E16/E40-Slots gewünscht sind, bitte festlegen.
7. Brückenfläche: Overlay `bruecke` hat 20 Zellen (E2 x 186–197 | z 72–75, E3-West x 174–186 | z 126–129); der Plan nennt 25/27 Boxen. Für `flaeche = 5` gilt Fr die Brückengeometrie aus P2/P5, nicht das Overlay.
8. Repo: `art/dorfmap-fertig` liegt in **Xenatosa/Planer** (origin), nicht in Xenatosa/epodarien. Der PR geht deshalb nach Planer.

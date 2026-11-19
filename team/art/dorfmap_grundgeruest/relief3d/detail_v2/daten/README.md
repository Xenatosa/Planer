# detail_v2 Datenschicht (P4)

Datenschicht zum neuen Vektor-Mesh der Dorfmap (DETAIL_V2_PLAN.md Abschnitt 3.3, Auftrag P4).
Stand und offene Punkte: [STATUS.md](STATUS.md). Marker: [S] gemessen/Quelle, [A] Annahme, [R] gerechnet, [F] Entscheidung.

## Koordinaten und Maßstab

- 1 Viewer-Einheit = 1 Zelle = 1 m. Karte x 0–336, z 0–303. [S]
- `neu/vektor.json` rechnet 1,2 m/Zelle → durch 1,2 teilen. [S]
- Raster 0,1 m/px, 3360 × 3030, Ursprung (0,0) = Weltecke, `px = floor(x·10)`, `py = floor(z·10)`, deckungsgleich mit UV1 = (x/336, z/303). Kartenrand 336/303 → letztes Pixel. [F über Plan]
- Alt-Zelle (cx, cy) = Weltquadrat [cx, cx+1) × [cy, cy+1) (`main.js` `zelle()`: floor(x), floor(z)). [S]
- Kacheln A–H × 1–7: Spalte floor(x/42), Zeile floor(z/43)+1; Zeile 7 reicht bis z = 303 (P10b). Punkt auf einer Schnittlinie gehört zur höheren Kachel. [S]/[A]

## Dateien

| Datei | Inhalt | Stand |
|---|---|---|
| `legende.json` | Klassen + Farben, Untertyp `untergrund`, Slot-Bits, Slots-Zählung, Maßstab, Kachelschema, Quellen mit SHA | fertig |
| `slots.json` | 99 Plätze (97 mit Bauplatz-Zellen) + 627 Deko-Slots, je mit Zellenliste | fertig |
| `baue_legende_slots.py` | erzeugt `legende.json`, `slots.json`; `--slot-png` schreibt `slot.png`; `--pruefe` | fertig |
| `baue_masken.py` | `flaeche/begehbar/untergrund/hoehe.png` aus Vektoren + Mesh | Schema abgestimmt (klasse/untergrund/id); hoehe.png Fr |
| `query.mjs` | `queryPoint(x,z)` → `{hoehe, flaeche, untergrund, begehbar, slot, kachel}`, ESM Node + Browser | Gerüst, Kachel/Maßstab/Slot/Mesh-Index fertig |
| `glb.mjs` | glb-Leser (POSITION, Indizes, `_FLAECHE`), Kacheln zusammenführen | fertig (synthetisch getestet) |
| `manifest.mjs` | `mesh/manifest.json` prüfen + laden → Gelände inkl. Brücken-Deck | fertig (synthetisch getestet) |
| `mesh_raster.py` | Mesh → 0,1-m-Raster (Höhe, Neigung, Klasse, Deck), Python | fertig (synthetisch + Benchmark) |
| `png.mjs` | PNG-Decoder ohne Abhängigkeiten (Graustufe 1/8/16 bit, indiziert 8 bit) | fertig |
| `test/query.test.mjs` | `node --test` | s. STATUS.md |
| `slot.png` | Slot-Bitfeld 16 bit | fertig, committet |
| `flaeche.png`, `begehbar.png`, `hoehe.png`, `untergrund.png` | Masken | Fr |

## Masken-Formate

- `flaeche.png` 8 bit: 0 Grund, 1 Weg, 2 Ufer, 3 Fels/Klippe, 4 Wasser, 5 Brücke. Priorität Wasser > Brücke > Weg > Ufer > Fels/Klippe > Grund.
- `begehbar.png` 1 bit (1 = begehbar): Klasse ∉ {3, 4} und Neigung ≤ 35°; Brücke: Deck. Abgleich `begehbar_3d` nur als Bericht.
- `slot.png` 16 bit Bitfeld (abgestimmt Grundgerüst 19.11.): Bits 0–11 Slot-ID (0 = kein Slot; 1–99 Plätze, 1001–1627 Deko), Bit 12 `deko_baum_ok`, Bit 13 `deko_fels_ok`, Bit 14 Bauplatz-Zelle, Bit 15 reserviert.
- `hoehe.png` 16 bit, `hoehe_m = offset_m + wert · skala_m` (Werte in `legende.json` → `dateien.hoehe.png`). `query.mjs` nimmt die Höhe bevorzugt exakt aus dem Mesh.
- `untergrund.png` 8 bit (Zusatzdatei, abgestimmt): 0 keiner, 1 Schnee, 2 Wald, 3 Boden, 4 Sand.

## Nutzung

```js
import { ladeDatenschicht } from './query.mjs';
import { ladeMesh } from './manifest.mjs';
const { gelaende } = await ladeMesh('relief3d/detail_v2/mesh/manifest.json');      // Browser: URL
const d = await ladeDatenschicht('relief3d/detail_v2/daten', { gelaende });
d.queryPoint(209, 118); // {hoehe, flaeche, untergrund, begehbar, slot, kachel:'E3'}
d.quellen();            // welche Quellen geladen sind; fehlende Quelle -> Wert null
```

GeoJSON-Eingang (abgestimmt): FeatureCollection in Viewer-Metern, Properties `klasse` (0–5), `untergrund` (Schnee/Wald/Boden/Sand), `id`. Mesh: glTF-Vertex-Attribut `_FLAECHE` (0–5), Dreiecke klassenrein.

Tests: `cd relief3d/detail_v2/daten && node --test`.

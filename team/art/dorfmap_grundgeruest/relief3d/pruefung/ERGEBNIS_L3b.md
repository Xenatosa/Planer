# ERGEBNIS L3b – Wasserstellen, Rand C4/D4, QA-P4c-Nachträge

> **Korrektur (L3c, 16.11.2026):** Die Aussage „Wege: Kreuzungsflächen … max 0,0 m, vektor.json-Wege … max 0,0 m“ war **falsch**, weil sie mit falschem Maßstab gemessen wurde (Meter aus `vektor.json` als Zellen gelesen, Faktor 1,2). Mit richtigem Maßstab hatte `d5b17e2` 7 geänderte Vertices auf Wegflächen (13 G4 max 0,284 m; 18 H2 max 0,06 m). Behoben in L3c2 (Rücksetzen der 7 Vertices im Nachschritt `relief_l3.py --stufe-c`). Auch die Ausnahme-Begründung zu Stelle 20 E2 („Böschung Gasse G013/K009“) war maßstabsbedingt falsch. Der richtige Abstand zum Weg beträgt 7,0 Zellen; Ursache ist die Renderer-Rasterkante des Wassers (siehe `AUSNAHMEN_L3c.md`).

Branch `art/dorfmap-L3b`, Basis `8cd6d37` (art/dorfmap-fertig). Kein Codex, keine Bildgenerierung, 0 €.
Umsetzung als Erweiterung des schaltbaren Nachschritts `relief_l3.py` (Stellen `L3b_*` in `pruefung/l3_stellen.json`).
`python3 relief_l3.py --aus` schaltet L3 + L3b komplett ab (GB, WV, FW.h, Objekte, Prototyp-Kacheln); erneutes Einschalten ist bytegleich (Beleg in `l3b_sha_belege.json`).

## Neu in relief_l3.py
- `"wasser": true`: Wasserschutz der Stelle aufgehoben. WV (Wasserspiegel) bekommt dasselbe Ersatzstück, geschrieben nur auf Wasser-Vertices. Abbruch, falls sich der Wassergrundriss (WV > -900) ändert.
- `"wasserspiegel": false`: WV bleibt; `"ufer_heben_m"`/`"ufer_band_m"`: äußerstes Wasserband knapp über den Spiegel, dann glätten.
- `"fw_folgen": true`: Feinband-Höhen FW.h folgen der Höhenänderung (sonst stünde das Feinband im Hauptviewer und in der Gate-Messung auf alter Höhe; behebt u. a. einen G11-„Baum schwebt“-Scheintreffer).
- `"rampe_m"` (L3b: 5,0 m = ganze Rampenböschung geschützt) und `"weg_rand_m"` (L3b: 5,0 m neben jedem vektor.json-Weg geschützt). Für die alten L3-Stellen bleibt alles wie gemergt.

## Ergebnis je Stelle (Nahbild entscheidet)

| Stelle | Feld | Befund vorher | Maßnahme | Ergebnis | Nahbild-Paar |
|---|---|---|---|---|---|
| 10 | E7/F7 | gerade graue Stufenlinie quer durchs Flussbett (Rille z = 275/276 in GB und WV) | `L3b_10`: Rille in Bett und Wasserspiegel gefüllt (WV max 0,78 m, GB max 0,75 m) | **weg** | `l3b_nahbilder/paare/stelle_10_vorher_nachher.jpg` |
| 20 | E2 | Ufer-Zickzack | 2 Versuche, beide ohne sichtbare Wirkung | **Ausnahme** (Westufer = Böschung Gasse G013/K009) | `paare/stelle_20_vorher_nachher.jpg` |
| 22 | F1 | Krone an der Wasserrinne + treppige Rinnenwände | `L3b_22`: Krone geöffnet, Rand geglättet, Ufer +0,08 m | **teilweise**: Krone weg, Rinne ruhiger; Stufenwände bleiben schwächer → Rest als Ausnahme | `paare/stelle_22_vorher_nachher.jpg` |
| C4/D4 Rand (Auftrag 2) + QA T11–T15 | C4/D4 | wolkige, unruhige Gratzone x 120–128, z 136–152 | `L3b_24`: weich nachgezogen (max 1,20 m), über die Naht hinweg; Normalenlinie x = 126 **nicht** angefasst (Dev UI) | **wolkig weg** (Ton und Farbe); Naht-Helligkeitslinie bleibt (Dev UI) | `paare/stelle_24_vorher_nachher.jpg`, `paare/stelle_25_vorher_nachher.jpg` (QA-Blickpunkte T11/T13/T15 + Ost) |
| 14 | E1 | dünne Finne an der Klippenecke | 2 Versuche | **Ausnahme**: Finne liegt 5,4 m neben `rampe_2`, im Böschungsschutz | `paare/stelle_14_vorher_nachher.jpg` |

Paarblätter: Spalten Ton vorher | Ton nachher | Farbe vorher | Farbe nachher. Einzelbilder in `l3b_nahbilder/einzel/` (`*_vorher.jpg` / `*_fin.jpg`).
`AUSNAHMEN_L3.md`: Einträge T11–T15 ehrlich auf „sichtbar, leicht“ korrigiert.

## Gate vorher/nachher (8cd6d37 → L3b), Details `L3b_gate_vorher_nachher.json`

| Prüfer | vorher | nachher |
|---|---:|---:|
| pruefe_regeln (export_gate) | 378 | **374** |
| pruefe_regeln mit eigenem Lochscan `/tmp/gate_loch_L3b.json` | 378 | 374 (identische Trefferliste) |
| r8 | 33 | 33 |
| r9 | 325 | 325 |
| W1 / W1 alle56 | 0 / 0 | 0 / 0 |

Geänderte Regeln: G2_spitze_oben 3→2, G3_spitze_unten 3→0, G5_beule_klippe 38→35, G6_facette 211→213, T1_fleckrand 0→1. Alle anderen gleich, insbesondere **R6_wasser_schnee 4→4, G8_fluss_nicht_bis_rand 1→1, R5_loch 4→4**.
Neue Treffer: 11, alle im Nahbild unsichtbar (Tabelle in `AUSNAHMEN_L3b.md`); entfallen: 13.

## Wasser-/Flussbelege
- Wassergrundriss (WV > -900) SHA256 vorher = nachher `c897e44c…21c5`; Flusslauf unverändert.
- WV geändert: 2386 Vertices, nur auf Wasser, max 0,778 m (nur Stelle 10, Rille gefüllt).
- R6 4 → 4, G8 1 → 1; Wasserfälle liegen nicht in den Stellen (Sichtprüfung der Nahbilder: unverändert).

## SHA- und Schutzbelege (`l3b_sha_belege.json`)
- D2: GB-Slab und Kachel-height_sha256 = `749d3c4b…80f6` (bitgleich).
- Unverändert: G, WEGA, wege, rampenwege, bruecken, felsen, findlinge, haeuser, wand*; vektor.json, felder.json, alle Prüfer (pruefe_regeln, export_gate, loch_o18g, r8/r9).
- Geändert (gewollt): GB, WV (nur Werte), FW.h (folgt), VC (gen_textur vc), Objekthöhen (folgen).
- Wege: Kreuzungsflächen 17644 Vertices max 0,0 m, vektor.json-Wege 19272 Vertices max 0,0 m. Keine geänderten Vertices innerhalb 5 m einer Rampe oder innerhalb Rand+5 m eines Weges.
- 56 Kacheln (`alles.sh`): Prototyp D1/G1/D2 = index.html identisch, Wände identisch, Naht max 0,0 m, Lochscan 56: nur die 3 offenen Kanten der C3-Positivkontrolle (= 0 echte Löcher). Hauptviewer-Lochscan 0 offene Kanten.

## Pipeline
`relief_l3.py` → `gen_textur.py vc` → `pruefung/p10c/waende_einsetzen.py` → `html_payload_p3.py` → Gate → `alles.sh /tmp/l3b/p10`.

# ERGEBNIS L3 – einfache Ersatzgeometrie für die sichtbaren Höhenfehler

Stand 16.11.2026 · Branch `art/dorfmap-L3` · Basis `art/dorfmap-fertig` @ c6a3db0 · Auftrag Dorfmap-Grundgerüst (Prio 1, Fabian: „Optik ist alles“)

## Kurzfassung

- **18 von 23 QA-Stellen sind im Nahbild weg**, 5 sind Ausnahmen (3 im Wasser, 2 teilweise an geschützten Wegen/Rampen, Details in [`AUSNAHMEN_L3.md`](AUSNAHMEN_L3.md)). Die drei starken Kacheln: C3 (alle drei Stellen) und D4 sind sauber; D1 ist nur teilweise sauber, die Rillen direkt an `rampe_2` bleiben.
- Gate pruefe_regeln **397 → 378** (G5 63 → 38, R5_loch 8 → 4, G6 205 → 211, G7b-Feld 25 → 29); r8 33 → 33, r9 325 → 325, W1 0 → 0, W1 alle 56: 0 → 0; T1 bleibt 0. Alle 40 neuen Treffer sind im Nahbild unsichtbar und stehen einzeln mit Messwert und Bild in `AUSNAHMEN_L3.md`.
- D2 bitgleich (`749d3c4b…`), Wege, Rampenkerne, Wasser, Kreuzungsflächen und das Quellfeld G unverändert (Δ = 0,0 m). Lochscan Hauptviewer 0 offene Innenkanten, Lochscan alle 56 Kacheln **0** (Positivkontrolle C3 = 3).

## Methode

Neuer, abschaltbarer Nachschritt [`relief_l3.py`](../relief_l3.py) mit Stellenliste [`l3_stellen.json`](l3_stellen.json). Je Stelle eine (drehbare) Ellipse mit flachem Kern und **3,5 m weichem Auslauf** (smoothstep, kein gerader Rand). Im Bereich ersetzt eine einfache Form das sichtbare Höhenfeld `GB`:
- graue **Öffnung** (1–3 m): entfernt dünne Grate, Zähne, Splitter und Klippenwülste;
- graue **Schließung** (2–3 m): füllt Kerben und Trichter (C6, G6);
- danach **Gauß-Glättung** σ 1,0–1,5 m: glatter Hang bzw. runde Ober-/Unterkante statt 0,5-m-Zickzack.

Fest (Gewicht 0, weicher Anstieg daneben): Wasser +1,5 m, Wegzellen/WEGA, Brücken, Rampenkerne ±2,0 m (gen_relief: Kern 1,8 m), Wegnetz aus `neu/vektor.json` (halbe Breite + 0,5 m), Kreuzungsflächen + Übergang + 0,5 m, Kachel D2 komplett mit 3 m Fade. D1 (Prototyp) wird mit `neu.mesh.tile_mesh` aus dem neuen GB neu vermascht; Objekthöhen (Bäume, Steine, Geröll, Findlinge: 193 Objekte) folgen der Höhenänderung.

Ein- und Ausschalten: `python3 relief_l3.py` (nur auf L3-Basis-GB) · `python3 relief_l3.py --aus` (stellt GB, D1-Mesh und Objekthöhen aus `l3_rueck.npz` wieder her; danach `gen_textur.py vc` usw. neu) · `--trocken` (nur rechnen). Rundlauf an/aus war vor `gen_textur.py vc` bytegleich zur Basis.

Pipeline danach (Ordner relief3d): `python3 gen_textur.py vc` → `python3 pruefung/p10c/waende_einsetzen.py` → `python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py` → Gate → `sh pruefung/alle_kacheln/alles.sh /tmp/l3/p10`.

Umfang: 20061 GB-Vertices geändert, max. |Δ| 3.22 m (E1-Splitter).

## 23 Stellen

Kamera der Nahbilder: P10-Viewer, Ziel = QA-Koordinate, Blick nach Norden; Abstand/Neigung wie in den QA-Punktdateien, sonst 18 m / 40°; ohne Schatten; je Stelle Clay und Farbe, vorher (Basis c6a3db0, selbst gerendert) und nachher. Paarbild = oben Clay, unten Farbe, links vorher, rechts nachher. Einzelbilder: `l3_nahbilder/<Nr>_<Name>_<clay|farbe>_<vorher|nachher>.jpg`.

| Nr | Kachel | Befund (QA) | Ergebnis | zacke_m vorher → nachher | Stellen: max. Δ / Vertices | Nahbild |
|---|---|---|---|---|---|---|
| 01 | C3 | Sägezahn-Ring Kraterrand | **weg** | C3_krater 0,84 → 0,19 | 01: 2,40 m / 2144 V | [vorher/nachher](l3_nahbilder/paare/01_C3_ring_paar.jpg) |
| 02 | C3 | Sägezahn-Kamm Grat | **weg** | C3_kamm 0,76 → 0,21 | 02: 1,51 m / 1465 V | [vorher/nachher](l3_nahbilder/paare/02_C3_gratkamm_paar.jpg) |
| 03 | D1 | Treppen-/Rippenrillen | **Ausnahme (teilweise)** – Hang glatt, Rillen direkt an rampe_2 bleiben (Weg fest) | D1_rampe 0,70 → 0,43; D1_rippen 1,79 → 1,75 | 03: 2,35 m / 1401 V | [vorher/nachher](l3_nahbilder/paare/03_D1_zickzack_paar.jpg) |
| 04 | C3 | Kamm linker Grat | **weg** | C3_kamm_links 0,44 → 0,12 | 04: 0,88 m / 694 V | [vorher/nachher](l3_nahbilder/paare/04_C3_linker_grat_paar.jpg) |
| 05 | D4 | Zahnkante Blockrand | **weg** | D4_kante 1,74 → 0,33 | 05: 2,40 m / 1001 V | [vorher/nachher](l3_nahbilder/paare/05_D4_zahnkante_paar.jpg) |
| 06 | C4 | Simsgrat-Zähne (+06b Rippenklippe nördlich) | **weg** | C4_sims 0,64 → 0,12 | 06: 1,60 m / 700 V, 06b: 1,52 m / 734 V | [vorher/nachher](l3_nahbilder/paare/06_C4_simsgrat_paar.jpg) |
| 07 | D6 | Trapeztafeln Wandfuß | **weg** | D6_tafeln 1,32 → 0,42; D6_tafeln2 1,54 → 0,48 | 07: 2,54 m / 883 V | [vorher/nachher](l3_nahbilder/paare/07_D6_tafeln_paar.jpg) |
| 08 | B4 | Zahnreihe kleine Stufe | **weg** | B4_zahnreihe 0,82 → 0,33 | 08: 1,29 m / 688 V | [vorher/nachher](l3_nahbilder/paare/08_B4_zahnreihe_paar.jpg) |
| 09 | C5 | Kamm Rinne/Grat | **weg** | C5_kamm 0,11 → 0,14 | 09: 1,14 m / 764 V | [vorher/nachher](l3_nahbilder/paare/09_C5_kamm_paar.jpg) |
| 10 | E7/F7 | Stufenlinie Flussbett | **Ausnahme** – liegt im Wasser, Wasser fest | E7_stufe 0,60 → 0,60; F7_stufe 0,61 → 0,61 | 10: 0,01 m / 57 V | [vorher/nachher](l3_nahbilder/paare/10_E7_stufe_paar.jpg) |
| 11 | C4/C5 | gezackte Gratkante | **weg** | C4C5_grat 0,68 → 0,17 | 11: 1,10 m / 1059 V | [vorher/nachher](l3_nahbilder/paare/11_C4C5_gratkante_paar.jpg) |
| 12 | D6 | Sägezahnlinie Hangrand | **weg** (2. Versuch); gerade Oberkante des Hangs bleibt als Form | D6_saege_W 0,66 → 0,19 | 12: 1,18 m / 420 V | [vorher/nachher](l3_nahbilder/paare/12_D6_saegelinie_paar.jpg) |
| 13 | G4 | Kissenblöcke, Zickzack am Fuß | **weg** (Zickzack weg, Blöcke weicher) | G4_block_a 1,05 → 0,66; G4_block_b 0,79 → 0,72 | 13: 2,00 m / 659 V | [vorher/nachher](l3_nahbilder/paare/13_G4_kissen_paar.jpg) |
| 14 | E1 | Splitter Klippenecke | **weg** (2. Versuch) | E1_splitter 2,72 → 1,04 | 14: 3,22 m / 613 V | [vorher/nachher](l3_nahbilder/paare/14_E1_splitter_paar.jpg) |
| 15 | C6 | Trichter Wandfuß | **weg** | C6_trichter 0,53 → 0,16 | 15: 1,01 m / 689 V | [vorher/nachher](l3_nahbilder/paare/15_C6_trichter_paar.jpg) |
| 16 | H6 | Kammzähne Wandkrone | **weg** | H6_kamm 1,14 → 0,46 | 16: 1,92 m / 838 V | [vorher/nachher](l3_nahbilder/paare/16_H6_kammkrone_paar.jpg) |
| 17 | H3 | Knubbel Terrassenrand | **weg** | H3_knubbel 0,48 → 0,28 | 17: 0,71 m / 471 V | [vorher/nachher](l3_nahbilder/paare/17_H3_knubbel_paar.jpg) |
| 18 | H2 | Kammzähne Grat + Randspitze | **weg** (Kamm); Randspitze am Kartenrand bleibt, unauffällig | H2_rand 0,79 → 0,82 | 18: 1,24 m / 1132 V | [vorher/nachher](l3_nahbilder/paare/18_H2_gratkamm_paar.jpg) |
| 19 | G3 | Spitzen/Knick Rücken | **weg** | G3_grat 0,22 → 0,08 | 19: 1,03 m / 1051 V | [vorher/nachher](l3_nahbilder/paare/19_G3_ruecken_paar.jpg) |
| 20 | E2 | Zickzack Uferkante | **Ausnahme** – Wasserrand, Wasser fest | E2_ufer 0,26 → 0,26 | 20: 0,06 m / 116 V | [vorher/nachher](l3_nahbilder/paare/20_E2_ufer_paar.jpg) |
| 21 | F6 | Kronenkamm (+21b Flanke) | **weg** (Rippen deutlich weicher) | nicht vermessen (QA ohne Koordinate) | 21: 1,08 m / 289 V, 21b: 1,86 m / 1023 V | [vorher/nachher](l3_nahbilder/paare/21_F6_krone_paar.jpg) |
| 22 | F1 | Kronenkamm | **Ausnahme** – Wasserrinne, Wasser fest | nicht vermessen (QA ohne Koordinate) | 22: 0,08 m / 499 V | [vorher/nachher](l3_nahbilder/paare/22_F1_krone_paar.jpg) |
| 23 | G6 | Kerbe/Kammkante Krone | **Ausnahme (teilweise)** – Kerbe weg, Rippen am Weg G017 bleiben | G6_kerbe 0,65 → 0,44 | 23: 0,83 m / 539 V | [vorher/nachher](l3_nahbilder/paare/23_G6_kerbe_paar.jpg) |

## Gate vorher / nachher

Befehl (relief3d): `rm -f /tmp/gate_loch_L3.json; NODE_PATH=/tmp/w3/node_modules HTML=index.html OUT=/tmp/gate_loch_L3.json RAND=0.6 node pruefung/loch_o18g.js && LOCHSCAN=/tmp/gate_loch_L3.json sh pruefung/export_gate.sh`. Hinweis: `export_gate.sh` setzt für pruefe_regeln fest `LOCHSCAN=/tmp/gate_loch.json` (die übergebene Variable wirkt dort nicht). Gegenprobe: pruefe_regeln direkt mit der eigenen Datei `/tmp/gate_loch_L3.json` ergibt dieselben 378 Treffer, Trefferliste identisch. Lochscan Hauptviewer vorher und nachher: 9 Meshes, 88 728 Dreiecke, 0 offene Innenkanten. Das Skript schreibt sonst nur die `*_letzter_lauf.json` im eigenen Ordner und ein Temp-Verzeichnis unter /tmp; `/tmp/gate_loch.json` habe ich nicht geschrieben.

**pruefe_regeln: 397 → 378**

| Regel | vorher | nachher | Δ |
|---|---:|---:|---:|
| `G2_spitze_oben` | 3 | 3 | +0 |
| `G2_spitze_oben_fein` | 9 | 9 | +0 |
| `G3_spitze_unten` | 3 | 3 | +0 |
| `G3_spitze_unten_fein` | 2 | 2 | +0 |
| `G5_beule_klippe` | 63 | 38 | -25 |
| `G6_facette` | 205 | 211 | +6 |
| `G7_wand_glatte_flaeche` | 1 | 1 | +0 |
| `G7b_wandkontur_feld` | 25 | 29 | +4 |
| `G7b_wandkontur_kantenschaerfe` | 1 | 1 | +0 |
| `G7b_wandkontur_rauheit` | 1 | 1 | +0 |
| `G8_fluss_nicht_bis_rand` | 1 | 1 | +0 |
| `R1_blind` | 17 | 17 | +0 |
| `R2_getrennt` | 9 | 9 | +0 |
| `R3_laengs_m` | 20 | 20 | +0 |
| `R3_quer_pct` | 11 | 11 | +0 |
| `R3_woelb_m` | 10 | 10 | +0 |
| `R5_loch` | 8 | 4 | -4 |
| `R6_wasser_schnee` | 4 | 4 | +0 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 |
| `T1_fleckrand` | 0 | 0 | +0 |

**r8 Kreuzungen: 33 → 33**

| Regel | vorher | nachher | Δ |
|---|---:|---:|---:|
| `R8_gitter` | 7 | 7 | +0 |
| `R8_quer` | 3 | 3 | +0 |
| `R8_stufe` | 6 | 6 | +0 |
| `R8a_wegende` | 17 | 17 | +0 |

**r9 Form (misst Quellfeld G, von L3 nicht geändert): 325 → 325**

| Regel | vorher | nachher | Δ |
|---|---:|---:|---:|
| `R8b_delle` | 22 | 22 | +0 |
| `R9_saegezahn` | 34 | 34 | +0 |
| `R9w_wellen` | 269 | 269 | +0 |

**W1 Wände Hauptviewer: 0 → 0**

| Regel | vorher | nachher | Δ |
|---|---:|---:|---:|
| `W1a_ausserhalb_karte` | 0 | 0 | +0 |
| `W1b_ueber_krone` | 0 | 0 | +0 |
| `W1c_schwebend` | 0 | 0 | +0 |
| `W1d_quellabstand` | 0 | 0 | +0 |

**W1 Wände alle 56 Kacheln: 0 → 0**

| Regel | vorher | nachher | Δ |
|---|---:|---:|---:|
| `W1a_ausserhalb_karte` | 0 | 0 | +0 |
| `W1b_ueber_krone` | 0 | 0 | +0 |
| `W1c_schwebend` | 0 | 0 | +0 |
| `W1d_quellabstand` | 0 | 0 | +0 |

Einzeltreffer neu/entfallen: [`L3_gate_vorher_nachher.json`](L3_gate_vorher_nachher.json) (40 neu, 59 entfallen). Gate bleibt ROT wie vorher (u. a. G6, R1–R3, R8, R9w aus anderen Familien).

## 56 Kacheln (alles.sh)

- Build: alle 56 Kacheln, Naht 97 Paare, max. Abweichung 0 m; Prototypen D1/G1/D2 mit `tile_mesh` reproduzierbar.
- Hashvergleich index.html ↔ alle_kacheln.html: D1, G1, D2 identisch (Oberfläche, Seiten, Boden).
- Lochscan alle 56 Kacheln: **0**; Positivkontrolle C3: 3 offene Kanten (erwartet).

## SHA-Belege ([`l3_sha_belege.json`](l3_sha_belege.json))

| Prüfgegenstand | vorher → nachher |
|---|---|
| D2-Höhe GB 87×85 | `749d3c4b637cf513…` → `749d3c4b637cf513…` (gleich) |
| D2 Prototyp height_sha256 | `749d3c4b637cf513…` → `749d3c4b637cf513…` (gleich) |
| G1 Prototyp height_sha256 | gleich (`b06ffb0e913947da…`) |
| D1 Prototyp height_sha256 | `6838b44c59453cfc…` → `60d9e4a579a26d5f…` (geändert, Stelle 03) |
| Quellfeld G | `d7db7b469d920925…` → `d7db7b469d920925…` (gleich) |
| Wasser WV | `976ddf0e71a0eb25…` → `976ddf0e71a0eb25…` (gleich) |
| Wegalpha WEGA | `d4067ef282df49c6…` → `d4067ef282df49c6…` (gleich) |
| wege / brücken / rampenwege | `9b718f37ae2d743c…` → `9b718f37ae2d743c…` (gleich) / gleich / gleich |
| neu/vektor.json | `aac6afff89ecba52…` → `aac6afff89ecba52…` (gleich) |
| neu/zellen_relief.csv · zellen_relief.csv | gleich · gleich |
| neu/felder.json · felder.npz | gleich · gleich |
| Prüfer pruefe_regeln.py, r8, r9, w1, export_gate.sh, loch_o18g.js | alle gleich |
| GB gesamt | `ae279bc21c9d04eb…` → `2e63683df5cf6563…` (geändert) |

Gemessene Höhenänderung auf festen Flächen: Wasser-Vertices 0.0 m, Wegzellen 0.0 m, Rampenkern 1,8 m 0.0 m, Wegnetz vektor.json (19272 Vertices) 0.0 m, Kreuzungsflächen (17644 Vertices) 0.0 m.

## Geänderte Dateien

- neu: `relief_l3.py`, `pruefung/l3_stellen.json`, `pruefung/l3_rueck.npz` (Originalwerte zum Abschalten), `pruefung/l3_bericht.json`, `pruefung/l3_sha_belege.json`, `pruefung/l3_zacke_vorher_nachher.json`, `pruefung/L3_gate_vorher_nachher.json`, `pruefung/AUSNAHMEN_L3.md`, `pruefung/ERGEBNIS_L3.md`, `pruefung/l3_nahbilder/` (104 Nahbilder, 26 Paarbilder, 40 Trefferbilder)
- geändert: `relief_daten.json.gz` (GB, VC/FW.c durch `gen_textur.py vc`, Objekthöhen), `neu/relief_neu.json.gz` (dasselbe + D1-Mesh, Wand-Metadaten `nicht_gerendert/D1`), `index.html` und `neu/index.html` (nur NEU_GZ-Datenzeile), `pruefung/regeln_letzter_lauf.json`, `pruefung/w1_alle56_letzter_lauf.json`
- nicht geändert: Prüfer, Schwellen, zellen_relief, vektor.json, Wege, Wasser, D2

## Offene Punkte

1. D1-Rillen an `rampe_2`, G6-Rippen am Weg G017: sichtbar, liegen im Wegschutz. Lösung nur mit Änderung am Rampen-/Wegprofil (Wege & Deko) oder einer Freigabe, die Böschung innerhalb des Rampenkerns anzufassen.
2. E2, E7/F7, F1: Wasserränder bzw. Linie im Wasser, Zuständigkeit Wasser.
3. QA sichtet die 23 Paarbilder und die 56 Kachelbilder (`alles.sh`, Ausgabe /tmp/l3/p10, nicht eingecheckt).
4. Die Zusatz-Formbefunde aus `AUSNAHMEN_P3.md` sind nicht bearbeitet.

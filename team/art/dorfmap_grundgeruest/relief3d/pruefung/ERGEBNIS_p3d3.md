# Ergebnis p3d3

Stand: 2026-11-06 · Branch `art/dorfmap-p3d3` · Basis `origin/art/dorfmap-p3d2` (`c0a2678`)

## Aenderungen

- `neu/mesh.py`, Variante `2` (Standard, schaltbar mit `RELIEF_GELAENDE_VAR`): Die D1-Rampen-Kreuzung erhaelt eine gemeinsame Flaeche mit seitlichem und laengsgerichtetem Smoothstep-Auslauf. Der radiale Uebergang wurde erweitert, damit die gemessene Kreuzungsflaeche keinen harten Plattenrand hat. Das Viewer-HTML bindet weiterhin das echte `neu_mesh_tiles`-3D-Mesh fuer D1/G1/D2 ein.
- `neu/tests/test_beanstandungen.py`: Die absoluten Wegende-Grenzen sind wieder aktiv: kein R8a-Treffer ueber 0,10 m; F1 maximal 0,10 m und mindestens ein explizit vermessenes C1-Wegende. Es wurden keine Pruefschwellen gelockert.
- Die drei veralteten Testimporte wurden auf die vorhandenen APIs `neu.baue_viewer`, `neu.mesh` und `neu.felder` umgestellt. Die Tests laufen wieder; die fachlich roten Tests bleiben rot.
- `neu/build.json`, beide Viewer-HTMLs und die Vorher/Nachher-Nahbilder wurden neu erzeugt.

## Ergebnis in Zahlen

### Vorgeschriebene Legacy-Pruefung

Die Auftragsnotiz nennt vor der Aenderung `pruefe_regeln=596`, `R8=48` und `R9=334`. Auf dem aktuellen Quellartefakt zaehlt die unveraenderte direkte Pruefung `570`, `48` und `334`. Der p3d2-Bericht dokumentiert dieselbe Abweichung: 596 liess sich dort nicht reproduzieren; gemessen wurden 570. R8 und R9 stimmen mit den genannten Ausgangswerten ueberein.

| Lauf auf `relief_daten.json.gz` | Ausgangswert laut Auftrag | p3d3 direkt | Exit |
|---|---:|---:|---:|
| `pruefe_regeln.py` | 596 | 570 | 1 (Treffer vorhanden) |
| `r8_kreuzung.py` | 48 (Stufe 9, Gitter 10, Quer 5, Wegende 24) | 48 (9, 10, 5, 24) | 1 (Treffer vorhanden) |
| `r9_form.py` | 334 (Delle 25, Saegezahn 34, Wellen 275) | 334 (25, 34, 275) | 1 (Treffer vorhanden) |

Der direkte aktuelle `pruefe_regeln`-Lauf zaehlt: R1 24, R2 15, R3 laengs 35, R3 quer 23, R3 Woelbung 22, R5 17, R6 4, G2 oben 3, G3 unten 3, G2 fein 8, G3 fein 2, G5 68, G6 220, G7 1, G8 1, T1 94, T2–T5 je 1 sowie G7b Rauheit 1, Kantenschaerfe 1 und Feld 24. Diese Werte sind unveraenderte Quellpruefungen und kein Meshvergleich.

### Neu-Mesh gegen Neu-Mesh-Kontrolle

Verglichen wurden dieselben Eingaben, derselbe Viewer und dieselben Wandmeshes: Kontrolle Variante 0 gegen p3d3 Variante 2. `neu/delta.py` meldet **10 positive Deltas** und Exit 1: zwei Regel/Kachelwerte und acht Clay-Bildmetriken. Damit ist das Delta-Abbruchkriterium nicht erfuellt. Kein Wert steigt um mehr als +5; R3-laengs D1 steigt genau um +5. Alle Zaehler fuer D2 bleiben unveraendert.

#### Regelzaehler nach Regel und Kachel

Je Tabellenzelle: Kontrolle → p3d3. Die Gesamtspalte enthaelt den Zaehler fuer alle Kacheln.

| Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| G11_objekt_schwebt_sinkt | 4→4 | 2→2 | 2→2 | 0→0 |
| G2_spitze_oben | 3→3 | 0→0 | 0→0 | 0→0 |
| G2_spitze_oben_fein | 8→8 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten | 3→3 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten_fein | 1→1 | 0→0 | 0→0 | 0→0 |
| G5_beule_klippe | 68→67 | 1→0 | 0→0 | 0→0 |
| G6_facette | 216→216 | 1→1 | 2→2 | 0→0 |
| G7_wand_glatte_flaeche | 1→1 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_feld | 24→25 | 0→1 | 0→0 | 0→0 |
| G7b_wandkontur_kantenschaerfe | 1→1 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_rauheit | 1→1 | 0→0 | 0→0 | 0→0 |
| G8_fluss_nicht_bis_rand | 1→1 | 0→0 | 0→0 | 0→0 |
| R1_blind | 24→24 | 2→2 | 1→1 | 0→0 |
| R2_getrennt | 15→15 | 1→1 | 0→0 | 1→1 |
| R3_laengs_m | 35→40 | 6→11 | 1→1 | 0→0 |
| R3_quer_pct | 23→19 | 11→7 | 0→0 | 0→0 |
| R3_woelb_m | 22→20 | 10→8 | 0→0 | 0→0 |
| R5_loch | 17→17 | 0→0 | 0→0 | 0→0 |
| R6_wasser_schnee | 4→4 | 0→0 | 3→3 | 0→0 |
| T1_fleckrand | 94→94 | 0→0 | 3→3 | 7→7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |
| T3_streifen_ringe_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |
| T5_textur_vs_clay_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |

#### R8/R9 nach Regel und Kachel

| Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| R8_gitter | 9→8 | 1→0 | 0→0 | 0→0 |
| R8_quer | 5→4 | 1→0 | 0→0 | 0→0 |
| R8_stufe | 8→8 | 1→1 | 0→0 | 0→0 |
| R8a_wegende | 23→23 | 2→2 | 1→1 | 0→0 |
| R8b_delle | 23→22 | 1→0 | 0→0 | 0→0 |
| R9_saegezahn | 34→34 | 1→1 | 1→1 | 0→0 |
| R9w_wellen | 281→280 | 21→20 | 13→13 | 0→0 |

Am D1-Schnittpunkt `rampe_2x11` bei (152,5; 28,5) sinkt die Stufe von **1,746 m auf 0,038 m** und das Gitter von **2,353 m auf 0,000 m**. Der weiche Rand ist im Clay-Bild sichtbar. Ein anderer D1-Endpunkt `rampe_11_ende` bei (156,5; 37,5) verschlechtert sich jedoch von **0,064 m auf 0,380 m** Stufe. Der D1-Saegezahn bleibt bei **47** Elementen (Ziel 0; vorher 49 im p3d2-Bericht). R9w sinkt von **281 auf 280** und erfuellt damit den Grenzwert. D1/G1-Wegende-Treffer bleiben drei mit zusammen **0,59 m** (D1 0,25 + 0,12 m; G1 0,22 m); die absolute Null-Grenze wird verfehlt.

#### Positive Clay-Bildmetriken

| Kachel/Kamera | Metrik | Kontrolle | p3d3 | Δ |
|---|---|---:|---:|---:|
| D1 Kreuzung | normale Spruenge | 511 | 650 | +139 |
| D1 Kreuzung | normale Sprunginseln | 94 | 105 | +11 |
| D1 Wandfuss 140\|35 | Facetten | 382 | 415 | +33 |
| D1 Wandfuss 140\|35 | normale Spruenge | 3696 | 3811 | +115 |
| D1 Wandfuss 140\|35 | normale Sprunginseln | 173 | 240 | +67 |
| D1 Wandfuss 140\|35 | Loecher | 51 | 52 | +1 |
| D1 Wegende | Facetten | 787 | 873 | +86 |
| D1 Wegende | normale Sprunginseln | 217 | 224 | +7 |

Die D1-Kreuzung hat zugleich 445→303 Facetten (−142), zeigt aber mehr Normalenspruenge. G1-Bildmetriken bleiben gleich, weil das G1-Gelaende in Variante 2 **0 geaenderte Vertices** hat. D2 Clay- und Textur-Bilder sind jeweils bytegleich zur Kontrolle.

## Build, Integritaet und Tests

- `lod1`: **168.600 Dreiecke** bei Budget 1.300.000; D1/G1/D2 sind echte Meshes im Viewer.
- Lochscan unter `xvfb-run`: **9 Meshes, 88.728 Terrain-Dreiecke, 0 offene Innenkanten, 0 Punkte**.
- D2 Hoehenbytes: unveraendert; SHA-256 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`. D2 Clay- und Textur-Nahbilder sind ebenfalls bytegleich.
- Zellquellspalten: `zellen_quell_diff=0`; die neun Quellspalten sind im Build ausgewiesen. t42u: **0 Abweichungen**.
- Gezielte Suite: **13 bestanden, 9 fehlgeschlagen**. Die drei Importfehler sind behoben. Rot bleiben G1-Variante/Profiltests, R8a-Wegende-Verbesserung und Nullgrenze, D1-Saegezahn=0, F1/C1-Wegende, sowie zwei unveraenderte Negativreferenztests (D1-Wandkantenschaerfe 2,24 statt mindestens 3,00; Schatten-Hochfrequenz 0,307 statt hoechstens 0,25).
- `git diff --check`: sauber. Keine Zellquellen, Referenzdateien, Overlay- oder Legacy-Pruefer wurden geaendert. Es wurde kein Prozesspool verwendet. Codex-Konfiguration blieb unangetastet; der Lauf war auf `gpt-6-luna`/`xhigh` eingestellt.

## Nahbildkontrolle

Die Tonbilder wurden jeweils vor/nachher angesehen. Die Kameradaten stehen in [`bilder_p3d3/kameras.json`](bilder_p3d3/kameras.json); Bilder liegen paarweise in `bilder_p3d3/control/clay/` und `bilder_p3d3/mesh/clay/` (Texturvarianten ebenfalls vorhanden).

| Ansicht | Kontrolle | p3d3 | Beobachtung |
|---|---|---|---|
| D1 Kreuzung | [Bild](bilder_p3d3/control/clay/D1_kreuzung.png) | [Bild](bilder_p3d3/mesh/clay/D1_kreuzung.png) | Weicherer Uebergang, keine dunkle harte Platte; R8-Schnittpunkt 0,038 m. |
| D1 Wandfuss 140\|35 | [Bild](bilder_p3d3/control/clay/D1_wandfuss_140_35.png) | [Bild](bilder_p3d3/mesh/clay/D1_wandfuss_140_35.png) | Naht-/Risslinien am T-Anschluss bleiben sichtbar; Bildmetriken steigen. |
| G1 Wandanschluss | [Bild](bilder_p3d3/control/clay/G1_wandanschluss.png) | [Bild](bilder_p3d3/mesh/clay/G1_wandanschluss.png) | Kamera verdeckt den Wandfuss groesstenteils; G1-Mesh und Bild sind unveraendert, daher keine Aussage ueber eine Behebung. |
| D1 Wegende | [Bild](bilder_p3d3/control/clay/D1_wegende.png) | [Bild](bilder_p3d3/mesh/clay/D1_wegende.png) | Gefaelle bleibt weich, aber der Wegende-Zaehler verbessert sich nicht. |
| D2 Draufsicht | [Bild](bilder_p3d3/control/clay/D2_draufsicht.png) | [Bild](bilder_p3d3/mesh/clay/D2_draufsicht.png) | Visuell und byteweise identisch. |

## Annahmen, Grenzen und offene Punkte

- Die Delta-Kontrolle ist Variante 0 gegen Variante 2 dieses Worktrees. Der separate historische Quellenwert 596 ist mit dem aktuellen Quellartefakt nicht reproduzierbar; p3d2 dokumentierte 570. Die unveraenderte direkte R8/R9-Messung stimmt mit den Auftragswerten ueberein.
- Der Prototyp umfasst nur D2, G1 und D1. Die absolute Wegendegrenze gilt global und bleibt wegen 23 R8a-Treffern ausserhalb der gezielten D1-Kreuzung unerfuellt.
- G1 wird in der gewaehlten Variante nicht geaendert. Der G1-Wandanschluss und die Naht am D1-Wandfuss sind damit nicht behoben. D1-Saegezahn, F1/C1-Wegenden und der schlechtere R8-Endpunkt bleiben offen.
- Das Hauptziel ist **nicht vollstaendig erreicht**: der Delta-Checker hat 10 Anstiege, die gezielte Suite ist rot, und der G1-Wandanschluss bleibt offen. Die Messwerte und Bilder dokumentieren diese Grenzen ohne Schwellenlockerung.

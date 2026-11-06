# Ergebnis p3d – Integration von Gelände- und Wandmesh

**Status: teilweise erreicht.** Die beiden Branches sind integriert und der
Opt-in-Viewer zeichnet D1, G1 und D2 als eigene Three.js-Geländemeshes. D1/G1
haben Relief aus GB und separate geschlossene Wandmeshes. D2, Zellquellen und
Overlay blieben unverändert. Die geforderte sichtbar wirksame Profilvariante
ohne Clay-Anstieg ist noch nicht erreicht: Die einzige Variante ohne
Metrikanstieg ist in den festen Nahbildern pixelgleich zur Kontrollvariante,
und alle sieben unveränderten Beanstandungstests bleiben rot.

## Änderungen

- `RELIEF_NEU=1` wählt über `main.js` den neuen Three.js-Kernviewer. Der
  Opt-in-Builder erzeugt `index.html` und `neu/index.html` bytegleich und
  offline nutzbar. Der Legacy-Build ohne Schalter bleibt verfügbar.
- `neu/mesh.py` baut D1/G1 aus dem sichtbaren GB-Höhenfeld auf dem 0,5-m-Raster.
  Wege, Kreuzungen, Bauzonen und Wasser erhalten lokale Profile. `D2` wird ohne
  Höhenänderung aus GB kopiert. `RELIEF_GELAENDE_VAR=0|1|2` schaltet drei
  Profilstärken; Standard ist Variante 2.
- `neu/wand.py` glättet Profilpolylinien mit Chaikin und baut die Wände mit
  gerundetem Querschnitt und gemeinsam genutzten Vertices. `WANDVAR=1` ist
  Standard, `WANDVAR=0` die breitere Alternative. D1/G1-Wände sind separate
  Meshes; D2 bleibt wandfrei.
- `neu/pipeline.py` weist Terrain, geschlossene Kachelfundamente und Wände im
  LOD1-Budget gemeinsam aus. Die erzeugten Wandnetze sind geschlossen: alle
  ungerichteten Dreieckskanten werden je zweimal verwendet.
- Zusammengeführt wurden `80de512` (`pgelaende`) und `cc9e42e` (`pwand`) in
  `art/dorfmap-p3d` über Merge-Commits `ab73b48` und `506b3d6`. Die Konflikte
  wurden in `index.html`, `neu/mesh.py` und `neu/pipeline.py` sowie den
  kollidierenden Viewer-Tests aufgelöst; `main.js` wurde automatisch
  zusammengeführt.

## Gelände- und Meshwerte je Kachel

| Kachel | Terrainvertices | Oberflächen-Dreiecke | geschlossene Terrain-Dreiecke | GB-Höhenbereich | Profiländerung Variante 2 | Wandfeatures / Dreiecke |
|---|---:|---:|---:|---:|---:|---:|
| D1 | 7.395 | 14.448 | 29.576 | 0 bis 14 m | 84 Vertices, max. 0,000588 m | 7 / 32.976 |
| G1 | 7.395 | 14.448 | 29.576 | ca. 0 bis 14 m | 209 Vertices, max. 0,001436 m | 13 / 46.896 |
| D2 | 7.395 | 14.448 | 29.576 | −0,632906 bis 0,043032 m | 0 Vertices, 0 m | 0 / 0 |

LOD1 hat **168.600 Dreiecke**: 88.728 geschlossene Terrain-Dreiecke plus
79.872 Wanddreiecke. Das bleibt unter 1,3 Mio. Der D1-Punkt (140,35) ist
7,8840365 m hoch und stimmt exakt mit GB überein. D2s GB-Tilebytes stimmen
byteweise mit der Ausgangsrevision 9d3f8fc und mit dem D2-Mesh überein
(SHA-256 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`).
Die neun Zellquellspalten haben `zellen_quell_diff=0`; t42u ist `summe=0`.
`wege`, `WEGA` und `bruecken` stimmen mit der Ausgangsrevision bytegleich
überein.

## Prüfergebnisse je Regel

Die Vorherwerte stammen aus `9d3f8fc`; die Nachherwerte aus dem finalen Lauf.
Ein Plus bei einer Regel bleibt innerhalb der erlaubten +5. Der Relief-Datensatz
selbst wurde in p3d nicht geändert (SHA-256 unverändert zu Startcommit
`2995b95`: `5e8fdb51c3f3dff9ad2c03c32c7a39ee1a4f97a3bc0942d47a352b1d0b4f0e88`).
Die Abweichung 596→570 war bereits in der bestehenden Branch-Basis enthalten;
die vorherige pgelände-Ergebnisdatei weist dort ebenfalls 570 aus.

| Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 35 | 0 |
| R3_quer_pct | 23 | 23 | 0 |
| R3_woelb_m | 22 | 22 | 0 |
| R5_loch | 17 | 17 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten | 3 | 3 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 66 | 68 | +2 |
| G6_facette | 249 | 220 | −29 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 23 | 24 | +1 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| **Summe pruefe_regeln** | **596** | **570** | **−26** |

| R8-Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| R8_stufe | 9 | 9 | 0 |
| R8_gitter | 10 | 10 | 0 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 24 | 24 | 0 |
| **Summe R8** | **48** | **48** | **0** |

| R9-Regel | Vorher | Nachher | Δ |
|---|---:|---:|---:|
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |
| **Summe R9** | **334** | **334** | **0** |

### Gate-Zahlen je Kachel

| Prüfer | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
|---|---:|---:|---:|
| pruefe_regeln | 36 → 36 | 13 → 13 | 8 → 8 |
| R8 | 8 → 8 | 1 → 1 | 0 → 0 |
| R9 | 26 → 26 | 8 → 8 | 0 → 0 |

R8 D1: Stufe 2, Gitter 2, Quer 1, Wegende 3; G1: Wegende 1. R9 D1:
Delle 2, Sägezahn 1, Wellen 23; G1: Delle 1, Sägezahn 1, Wellen 6. Im
Treffervergleich von pruefe_regeln kam **kein Treffer in D2 neu hinzu**.

## Varianten, Bilder und verbleibende Fehler

| Variante | D1/G1 geänderte Terrainvertices | max. Höhenänderung | Clay-Metrikanstiege gegen Variante 0 |
|---|---:|---:|---:|
| `RELIEF_GELAENDE_VAR=0` | 0 / 0 | 0 m | 0 |
| `=1` | 184 / 293 | 0,029399 / 0,071783 m | 6, alle in G1, größter Einzelanstieg +2 |
| `=2` (Standard) | 84 / 209 | 0,000588 / 0,001436 m | 0 |

Variante 2 ist damit die einzige getestete aktive Profilvariante ohne
Clay-Metrikanstieg. Die Höhenänderung ist auf den Nahbildern nicht sichtbar:
die fünf individuellen Tonkameras sind gegen Variante 0 pixelgleich. Die
Profile sind numerisch aktiv, aber für die gewünschte sichtbare Ausformung von
Wegen/Kreuzungen/Wegenden zu schwach. Variante 1 macht sie stärker, verletzt
aber die Clay-Delta-Vorgabe.

Ich habe die Ton-Nahbilder vor und nach dem Variantenvergleich selbst geprüft.
Die Kamera `D1_wand_140_35_fuss` zielt auf die geforderte Klippe bei 140|35;
zusätzlich wurden D1/G1-Streiflicht und D2-Draufsicht betrachtet:

- Vorher: `/tmp/nahbilder_p3d_custom_v0/D1_wand_140_35_fuss.png`,
  `/tmp/nahbilder_p3d_custom_v0/G1_wand_260_25_fuss.png`,
  `/tmp/nahbilder_p3d_custom_v0/D2_draufsicht.png`.
- Nachher: `/tmp/nahbilder_p3d_custom_v2/D1_wand_140_35_fuss.png`,
  `/tmp/nahbilder_p3d_custom_v2/G1_wand_260_25_fuss.png`,
  `/tmp/nahbilder_p3d_custom_v2/D2_draufsicht.png`.

Die D1-Klippenform und D2 sind erhalten. Die Wandkörper haben geglättete
Konturen und geschlossene Rundprofile, aber an den angrenzenden GB-Terrainkanten
sind im Bild weiterhin Stufen sichtbar. Der Sägezahn- und Wellenbefund ist
unverändert; das Ziel „kein Sägezahn“ ist nicht erreicht.

Die sieben unveränderten Funktionen aus `neu/tests/test_beanstandungen.py`
wurden direkt ausgeführt und bleiben alle rot:

| Beanstandung | Ist | Grenze |
|---|---:|---:|
| Kreuzungsstufe D1/G1 | 1,389 m | ≤ 0,20 m |
| Wegenden allgemein | 24 Treffer | 0 |
| Delle G1 bei 278,5|27,0 | 0,42 m | ≤ 0,30 m |
| Sägezahn D1 | 41 Elemente | 0 |
| D1-Wandkantenstärke | 2,24 | ≥ 3,00 |
| F1-Wegende / C1-Messung | 0,17 m / 0 Messpunkte | ≤ 0,10 m / mindestens 1 |
| Schattenbild-Hochfrequenz | 0,307 | ≤ 0,25 |

Die Prüfdateien und ihre Negativreferenzen wurden nicht geändert. `pytest` ist
in der Laufzeit nicht installiert; die Mesh-/Wandfunktionen wurden direkt
ausgeführt (7 bestanden), und die sieben Beanstandungsfunktionen separat
aufgerufen (7 fehlgeschlagen). `node neu/tests/test_html.js` und
`node neu/tests/test_pipeline.js` bestanden; der zweite Pipeline-Lauf lieferte
dieselben Artefakthashes.

## Prüfläufe und offene Punkte

- Lochscan mit WebGL unter `xvfb-run`: `index.html` und `neu/index.html` melden
  je 0 offene Innenkanten, 0 Punkte und 88.728 geprüfte Terrain-Dreiecke. Die
  separaten Wandnetze wurden zusätzlich auf geschlossene Kanten geprüft.
- `pruefe_regeln.py`: 570 Treffer; der Prozess liefert wegen der verbliebenen
  Befunde Exit 1. R8=48 und R9=334 liefern ebenfalls Exit 1 wegen bestehender
  Treffer. t42u: `summe=0`.
- `git diff --check` und Python-Syntaxprüfung bestanden.
- Codex-Konfiguration geprüft: `model = gpt-6-luna`,
  `model_reasoning_effort = xhigh`; nicht geändert. Ein separater Lauf-Log war
  in dieser Umgebung nicht zugänglich, daher konnte ich den Logeintrag selbst
  nicht verifizieren.
- Annahme: `RELIEF_GELAENDE_VAR=2` ist wegen 0 Clay-Anstiegen der beste
  Standard, obwohl seine Profilwirkung in den festen Bildern nicht aufgelöst
  wird. Das ist ein bewusster Zielkonflikt, kein visueller Erfolg.
- Offene Arbeit: sichtbar wirksame Wege-/Kreuzungs-/Wegendprofile ohne
  Bildmetrikanstieg finden; GB-Stufen an D1/G1-Wandanschlüssen beheben, ohne
  D2 oder die Klippenform bei D1 140|35 zu ändern; die sieben
  Beanstandungsbefunde beseitigen.

Kosten: **0 EUR**. Es wurden keine Secrets gelesen und keine Nachrichten
versendet.

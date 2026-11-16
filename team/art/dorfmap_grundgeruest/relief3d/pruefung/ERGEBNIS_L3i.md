# ERGEBNIS L3i – E3-Nord durchgehender Kanal, G1-Krater Wasser → Schnee (QA P4f S1/S2) – Basis art/dorfmap-fertig @ a6b00ba

Kosten: 0 € · Codex: nein · Laufzeit: 21:18–21:54

Worktree /workspace/wt_dorfmap_L3i, Branch art/dorfmap-L3i auf origin/art/dorfmap-fertig = **a6b00ba** (geprüft, #38 gemergt).
Neues Skript `relief_l3i.py` = bau_endstand **Schritt 18** nach L3h-Schritt 17 (`L3I=0` schaltet ab, L3I=1 mit L3H=0 bricht ab; Rückweg `--aus` mit `pruefung/l3i/l3i_rueck.npz`).
Stellen in `pruefung/l3i/l3i_stellen.json`, Basis-Hash GB/WV/VC = Stand nach Schritt 17 (8b1aa2b8…). Grundlage QA P4f (#39, `qa_p4f/bilder_a6b00ba/vn/E3_tuempelkette_190_103.jpg`, `G1_krater_z10.jpg`).
Checker und Schwellen unverändert.

## Kurz
| Stelle | Ergebnis |
|---|---|
| (1) E3-Nordufer ≈190\|103 (Tümpelkette) | **gelöst**: ein durchgehender Kanal mit gleicher Breite (7 Vertices in jeder Zeile z 96–107, vorher 4–6) und konstanter Tiefe (0,50–0,51 m, vorher 0,28–0,55 m), Spiegel einheitlich −1,30 m (vorher Treppe −1,39/−1,30). Aus 12, 22 und 60 m in Farbe und Clay ein gleichmäßiges blaues Band, keine Perlen, keine Schnee-Engstellen. Westufer weich, keine Kante, kein Zackenrand. Rest: Der Kanal ist sehr regelmäßig (fast gerade Uferlinien) – wirkt nah etwas „gebaut“, aber nicht fehlerhaft. |
| (2) G1-Krater ≈272,5\|10 | **Wasser entfernt, mit Schnee aufgefüllt** (Begründung unten). In Farbe aus 12/22/60 m kein Fleck mehr, nur Schnee. Ehrlich: In Clay bleibt ein schwacher kreisförmiger Schattenring der aufgefüllten Mulde sichtbar (ganz leicht, in Farbe nicht erkennbar); drei Varianten getestet, v3 am weichsten. |

## (2) Wahl am G1-Krater – Begründung
- Geprüft, ob ein Bach daran hängt: Nein. Die Wasserfläche besteht aus zwei **isolierten** Komponenten (29 Vertices bei 271,5–273,5\|6,5–11,5 und 6 Vertices bei 274,5–275,5\|5,5–6,5, Spiegel 12,84–12,89 m), ohne Verbindung zu einem anderen Wasser (nächstes Wasser: Bach 211–217\|0–31, > 50 Zellen entfernt). In `neu/vektor.json` sind es kleine Einzeltümpel (Polygone 5/10/15, z 8,6 m) wie mehrere andere Plateau-Tümpel, die im Relief schon Land sind; keine Linie/Quelle eines Bachs.
- Regelwerk: `R6_wasser_schnee` zählt jedes Wasser über 10 m (Schneegrenze) als Fehler – der Fleck liegt bei 12,8 m. Ein runder Kratersee wäre dort weiter ein Regeltreffer und ein blauer Fleck im Schnee; Entfernen + Auffüllen behebt den Regel- und den Sichtfehler.
- Umsetzung (Art `wasser_zu_schnee`): nur die zwei Komponenten (Abbruch, wenn eine größer als 60 Vertices wäre oder in Sperr-/fester Fläche liegt), Gebiet = Komponenten + 3 Vertices Ring; GB harmonisch (Laplace) aus dem Rand aufgefüllt, dann weich (σ 2) eingeblendet (Blend σ 2,5); VC ebenso aus dem Rand (Schnee). 35 Wasser-Vertices entfernt, Füllung max 1,41 m.
- W1 bleibt 0 (W1 prüft Wände, keine Wand betroffen).

## (1) Verfahren E3
- Art `kanal` (`E3_kanal`): Mittellinie = Mitte des Wasserlaufs je Vertexzeile (x 185–194), geglättet (σ 5 Vertices); Kanal = |x − Mitte| ≤ 1,75 Zellen für z 95,5–107,5.
  Nur Wasser hinzufügen (47 neue Wasser-Vertices), Spiegel im Kanal −1,30 m (107 alte Wasser-Vertices von −1,39 auf −1,30 **angehoben**, nie gesenkt; Prüfung: Spiegel nie über dem benachbarten Gelände).
  Bett: Kern −0,50 m unter Spiegel, äußere Zelle weich auf −0,08 m. Land im Band 3 Zellen: Profil Spiegel + 0,04 m + 0,35 m/Zelle (nur absenken, nie unter Spiegel + 0,03 m), zu den Kanalenden weich ausgeblendet. VC: Kern-/Randton des Bachbetts, Land im Band weich.
- Art `hang_glatt` (`E3_hang`, wie L3h): Osthang am Nordende 193\|93–96,5 (eine neue G6 193,2\|94,8 aus dem ersten Lauf), 203 GB-Vertices, max 0,23 m.

## Gate (Endstand)
regeln **359** (Basis 363), R8 **31**, R9 **321**, W1 **0**, W1 alle 56 **0**, Lochscan **0** (offen_innen 0).
Gegen a6b00ba nur Wegfall: R6_wasser_schnee G1 272,5\|9,8 (22), 273,1\|7,3 (7), 275,0\|6,1 (6), G6_facette G1 271,7\|11,1 (8). Keine neuen Treffer.
`pruefung/*_letzter_lauf.json` und `pruefung/l3i/gate/` (inkl. lochscan.json) = dieser Lauf. export_gate.sh meldet lokal wie immer „GATE ROT: kein Export/ZIP“ (kein Export-ZIP im Worktree).

## Abstände / Wasser (`pruefung/l3i/l3i_abstaende.py` → `.json`, Basis a6b00ba, zellweite 1,2 m)
Geändert 1714 Vertices (GB 1683, WV 189, VC 711), Box 184,5–281,5\|0–110.
| Sperre | geänderte Vertices darauf | kleinster Abstand |
|---|---|---|
| Wege (Vektor) | 0 | 0,6 m |
| Kreuzungen | 0 | 2,55 m |
| Rampenkern | 0 | 1,8 m |
| WEGA/Wege/Brücken | 0 | 1,9 m |
| D2 | 0 | 21,5 m (GB-sha 749d3c4b… vorher = nachher) |
| rampe_5 | 0 | 62,1 Zellen = 74,5 m |
| Kachel D4/D5 | 0 Änderungen | 26,2 Zellen |
| D1 (inkl. X084/rampe_2) | 0 | 52,5 Zellen |
| Mulde 159\|22,9 | 0 | gemessen 74,6 Zellen = 89,5 m (54,6 Zellen außerhalb Sperrkreis r 20) |
Wasser: entfernt nur die 35 G1-Vertices (2 Komponenten, 9 → 7), sonst 0; neu 47 (nur E3-Kanal); WV auf altem Wasser nur die 107 angehobenen E3-Vertices; fill_holes-Differenz = genau 47 + 35 (keine Löcher); Bett über Spiegel 506 → 493.

## bau_endstand.sh
Schritt 18 (relief_l3i.py → html_payload_p3.py → waende_einsetzen.py), Nebenausgaben l3i_rueck.npz + l3i_bericht.json mitverglichen.
Volllauf: **ENDBAU BITGLEICH (515 s)**, 39/39 Ausgaben gleich (inkl. l3h_rueck/bericht und l3i_rueck/bericht), Schritt 18 l3i 15 s.

## Rückweg
`relief_l3i.py --aus` + html_payload_p3 + waende_einsetzen → relief_daten f99fe115…, relief_neu 04bb0df4…, index 0e845b39… = **exakt a6b00ba** (geprüft), danach wieder Commit-Stand.

## SHA (Endstand)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | 643bc530807540024d7cb87879342ffd57c2d36707d469f96c890d685e3e703b |
| neu/relief_neu.json.gz | d7b66b023add4b4791da451949c689f2e056f60c5075f00b26ceb66ea4b70994 |
| index.html = neu/index.html | e1561e91c0e422fbe1390448d751c8db00d826fe93d79603b53830e8f2323dbb |
| relief_l3i.py | b81f60ac00be6289aeda47fae299acad31eb8a1fd68b3261d4028d8427d59943 |
| bau_endstand.sh | 310cc249a915dd690df6ed55aa952da27be4a8af91abd82ffbce83db2b1034f0 |
| pruefung/l3i/l3i_rueck.npz | 3aafe17f233b3cdc1493e164a6e788f4532fb0eacbe959687986b5776a2f088f |

## Nahbilder (`pruefung/l3i_nahbilder/`, selbst angesehen)
- `paar_E3_kanal.jpg`: E3 190\|103 aus 12 m, 190\|104 aus 22 m, 189\|104 aus 60 m (von Süden); je Farbe vorher (a6b00ba) | nachher, Clay vorher | nachher.
- `paar_G1_krater.jpg`: G1 272,5\|10 aus 12 m, 272,5\|11 aus 22 m, 273\|14 aus 60 m; gleiche Anordnung.
- Einzelbilder `einzel/<Kamera>_{farbe,clay}_{vorher,nachher}.jpg`; Versuche G1 `versuche/` (v1 Ring 2/σ 1, v2 Ring 4/σ 2; Endstand v3 Ring 3/σ 2/Blend 2,5).
Bewertung: E3 klar gelöst (durchgehendes Band, gleichmäßiger Ton, Westufer weich). G1: in Farbe sauber; in Clay ein leichter runder Schattenring der Füllung – sichtbar nur in Clay, aus 60 m kaum.

# ERGEBNIS L3l – Sägezahn-Facetten auf der Südflanke des vorderen Grats (x 81–84 | z 133–137) – Basis art/dorfmap-L3k @ 9d04f67

Kosten: 0 € · Codex: nein · Laufzeit: 23:45–00:05

Worktree /workspace/wt_dorfmap_L3l, Branch art/dorfmap-L3l auf **9d04f67** (L3k). #46 ist inzwischen gemergt (art/dorfmap-fertig = 9d04f67, Fast-Forward), der Branch basiert damit direkt auf art/dorfmap-fertig.
Neues Skript `relief_l3l.py` = bau_endstand **Schritt 21** nach L3k-Schritt 20 (`L3L=0` schaltet ab, L3L=1 mit L3K=0 bricht ab; Rückweg `--aus` mit `pruefung/l3l/l3l_rueck.npz`).
Stelle in `pruefung/l3l/l3l_stellen.json`, Basis-Hash GB/WV/VC = Stand nach Schritt 20 (5914ca80…). Checker und Schwellen unverändert. Viewer-Dateien (index.html-Logik, Shader, Viewer-Code) nicht angefasst; index.html / neu/index.html sind nur die neu erzeugte Pipeline-Ausgabe. Vorher wurde der Platz mit df geprüft (22 GB frei); aufgeräumt wurden nur eigene /tmp-Reste (/tmp/l3k_bau1, /tmp/l3h, /tmp/l3i).

## Ursache (gemessen)
Die Gratkrone der Südflanke ist eine nur **1 Vertex breite Linie genau auf der 45°-Diagonale**: (85,0|133,5) 10,28 → (84,5|134) 10,31 → (84|134,5) 10,29 → (83,5|135) 10,27 → (83|135,5) 10,24 → (82,5|136) 10,14 m.
Direkt östlich dahinter liegt eine **0,4–0,5 m tiefere Rinne** (9,76–9,86 m), z. B. bei z 134,5: x 84 = 10,29, x 84,5 = 9,76.
Das Dreiecksnetz teilt jedes Gitterquadrat auf dieser Krone quer zur Kronenlinie. Krone und Rinne wechseln sich also je Quadrat ab, und so entstehen die Zähne. Sie stammen aus der Basisgenerierung; L3k hat dort nichts geändert.

## Ergebnis
**Gelöst.** Aus 15 m (Punkt 82|135,5 auf die Flanke und Kritikerkamera pk3 84|129) sind weder in Farbe noch in Clay Sägezähne zu sehen. Auch aus 30 m ist nichts zu sehen. Die Flanke steigt jetzt stetig zum Plateau an, ohne Messerkrone und ohne Rinne, z. B. z 134,5: … 9,33 9,58 9,75 9,85 9,97 10,06 10,16 m.
Bild selbst angesehen: `pruefung/l3l_nahbilder/paar_suedflanke.jpg`, dazu ein Ausschnitt in Clay mit 2-facher Vergrößerung.
Die L3k-Kerbe 84|129 kommt nicht wieder. Die 5-m-Höhenlinie z 125–136 ist auf 0,01 Zellen gleich wie in L3k, die Kritikeransicht 84|129 zeigt den Grat unverändert durchgehend. In der L3k-Box (bis z 133) wurden nur Kronenvertices x ≥ 83,5 bei z 131–133 um höchstens 0,41 m angepasst.
Änderung: 191 GB-Vertices, Box 79,5–88 | 131–139,5, max. 0,70 m (die Krone wird abgesenkt, die Rinne leicht gehoben). Wasser, WV und VC sind unverändert.
Ehrlich: Die dünnen dunklen Silhouettenlinien entlang der Flankenkante sind in vorher und nachher gleich. Sie sind die Kantenlinie des Renderers, keine Zähne.

## Verfahren
- Art `laengs_glatt` (aus L3k) mit neuem Gebietsparameter `gebiet_richtung`: Das Gebiet ist ein schmales Stadion entlang der Krone (Richtung −1,1, Halblänge 3 Zellen um 83,5|135,3, Kern r 1, weich bis r 2,5).
- Geglättet wird **längs der Falllinie** (Richtung 1,1, quer zur Krone), Gauss σ 1,5 Vertices, 2 Runden. Der Hangfuß unter 3 m bleibt, Wandquellzellen haben ≥ 1 Vertex Abstand. Das Feinband wird weich mit dem Gebietsgewicht nachgeführt (neuer Schalter `feinband_weich`).
- Wege dahin, Gate in Klammern:
  - Die erste Fassung war optisch schon sauber, hatte aber eine neue G6 bei 87,1|133,9, weil das Gebiet zu breit nach Osten reichte (360).
  - „Nur Rinne heben“ ließ die Zähne stehen (360).
  - Ohne Feinband-Nachführung blieb die feine Eigenstruktur und gab eine Kante am Gebietsende (360).
  - Mit binärem Feinbandgewicht entstand eine Kante am NO-Ende (360).
  - Erst das weiche Feinbandgewicht und das NO-Ende bei 85,6|133,2 ergaben 359 mit identischer Trefferliste.

## Gate (Endstand)
regeln **359** (Basis 359), R8 **31**, R9 **321**, W1 **0**, W1 alle 56 **0**, Lochscan **0** (offen_innen 0). Die Trefferliste ist identisch zur Basis.
`pruefung/*_letzter_lauf.json` und `pruefung/l3l/gate/` = dieser Lauf. export_gate.sh meldet lokal wie immer „GATE ROT: kein Export/ZIP“.

## Abstände / Wasser (`pruefung/l3l/l3l_abstaende.py` → `.json`, Basis 9d04f67, Zellweite 1,2 m)
| Sperre | geänderte Vertices darauf | kleinster Abstand |
|---|---|---|
| Wege (Vektor) | 0 | 85,6 m |
| Kreuzungen | 0 | 83,7 m |
| Rampenkern | 0 | 56,4 m |
| WEGA/Wege/Brücken | 0 | 83,9 m |
| D2 | 0 | 71,9 m (GB-sha 749d3c4b… vorher = nachher) |
| rampe_5 | 0 | 48,5 Zellen = 58,2 m |
| Kachel D4/D5 | 0 Änderungen | 38,0 Zellen = 45,6 m |
| D1 (inkl. X084/rampe_2) | 0 | 96,5 Zellen = 115,8 m |
| Mulde 159\|22,9 | 0 | 130,2 Zellen = 156,2 m (110,2 Zellen außerhalb Sperrkreis r 20) |
Wasser: entfernt 0, neu 0, Komponenten 7 → 7, Maske und WV gleich, fill_holes gleich (keine Löcher), Bett über Spiegel 493 → 493.

## bau_endstand.sh
Schritt 21 läuft so: relief_l3l.py → html_payload_p3.py → waende_einsetzen.py. Die Nebenausgaben l3l_rueck.npz und l3l_bericht.json werden mitverglichen.
Volllauf: **ENDBAU BITGLEICH (532 s)**, 45/45 Ausgaben gleich (inkl. l3k_rueck/bericht und l3l_rueck/bericht), Schritt 21 l3l 11 s.

## Rückweg
`relief_l3l.py --aus` + html_payload_p3 + waende_einsetzen → relief_daten 0d0296ba…, relief_neu 2b49e689…, index f356c5a3… = **exakt L3k 9d04f67** (Datendateien git-sauber). Danach erneut angewendet → bitgleich zum Commit-Stand.

## SHA (Endstand)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | 2d69e9e1553461d49174614902900beec31297e1dacda83bc05a64d41675cc77 |
| neu/relief_neu.json.gz | 5a8c87b4c24bc1f2e27fbbbe883ea55f09adaca94f1382a224130469911abb8a |
| index.html = neu/index.html | a964d923b8aaa3d9813c0558c6d1263f1c59d7bbf85d11463be30d0b889d305b |
| relief_l3l.py | 3ef221031a848f072064d9257d603cc20a2b71e3bcf5d59888f6f0717a0134be |
| bau_endstand.sh | 932909cce7faa4a1ccc2e1b97f0e71732c834f369e049e7d9d61ffefb27b91ac |
| pruefung/l3l/l3l_rueck.npz | db0f99bab8d29a1c71568c9e4aeb2a7ab1e1339686b6a1a0047846d257c94269 |

## Nahbilder (`pruefung/l3l_nahbilder/`, selbst angesehen)
- `paar_suedflanke.jpg`: Kritikerkamera `pruefung/qa_p4f/rendere_kacheln.js` (el 35, az 0). Zeilen: Punkt 82|135,5 d15 / d30, Kritiker pk3 84|129 d15 / d30. Spalten: Farbe vorher (L3k) | Farbe nachher | Clay vorher (L3k) | Clay nachher.
- Einzelbilder `<punkt>_{vorher,nachher}_{farbe,clay}.jpg`.

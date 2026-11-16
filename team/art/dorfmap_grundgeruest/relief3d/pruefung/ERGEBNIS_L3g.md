# ERGEBNIS L3g – F7/G7-Lichtspitzen (WV-Randring) + E3-West einfachere Rinne – Basis art/dorfmap-L3f2 @ 00735fb (auf 8c1fc80)

Kosten: 0 € · Codex: nein · Laufzeit: 17:44–18:26

art/dorfmap-fertig vor Beginn geprüft: steht auf 8c1fc80. Weiter auf art/dorfmap-L3f2 (normale Commits, kein Force-Push), geliefert in PR #35.
Freigaben von Grundgerüst: (1) WV-Randring am Nordufer anheben (kartenweit dieselbe Stufung, wo sichtbar), (2) E3-Rinne breiter/flacher, Maske darf nur wachsen.
Umsetzung in `relief_l3f.py` (bau_endstand **Schritt 15**, jetzt aktiv), Stellen `L3g_WV_ring` und `L3g_E3_breit` in `pruefung/l3f/l3f_stellen.json`.
Viewer für alle Nahbilder: normaler Viewer (P12c), vorher = 8c1fc80, nachher = Endstand.

## Kurz
| Stelle | Ergebnis |
|---|---|
| (1) F7/G7-Nordufer 236–256\|261–272 | **gelöst bis auf einen schwachen Punkt**: die Reihe der 4–5 hellen Spitzen ist aus der Distanz (Dev-UI-Kamera von Norden) weg, ein kleiner schwacher Fleck bleibt (`blatt_fg7_zoom_und_insel.jpg`). 75 Ring-Vertices angehoben. |
| (1) kartenweit | **gemessen, nicht übernommen**: 20 weitere Stufen-Stellen gefunden (Liste unten). Im Probelauf erzeugte das Anheben an der Inselspitze 172\|259 einen neuen hellen Splitter und an 285\|269 neue helle Streifen (`blatt_kartenweit_probelauf_nicht_uebernommen.jpg`); an den übrigen Stellen war in den Nahbildern kein Gewinn sichtbar. Deshalb nur F7/G7. |
| (2) E3-West 179–198\|89–124 | **gelöst**: Rinne breiter (139 neue Wasser-Vertices, nichts entfernt) und flacher, Böschung über ≈2–3 Vertices statt Sprung auf einem; die Zickzacklinie ist weg, das Ufer verläuft organisch. Ehrlich: der Bach wirkt in Farbe etwas heller/blasser als vorher, bleibt aber klar sichtbar; in Clay nur schwach. |

## (1) WV-Randring – Verfahren und Messwerte
- Regel: Wasser-Vertices mit Abstand < 3 Vertices zum Land, WV > 0,15 m unter dem geglätteten Innenmittel (Gauß σ 3 über Wasser mit Abstand ≥ 3), Gruppen ≥ 10.
  Ziel = Innenmittel, **gedeckelt auf Nachbargelände (3×3-Land-Minimum) − 2 cm** und höchstens +0,4 m. WV steigt nie über das benachbarte Gelände; wo das
  Ziel nicht über dem alten Wert liegt, bleibt der Wert (8 Vertices). Nur Anheben, Maske und Uferlinie unverändert, D1-Mulde (Radius 20) und feste Flächen ausgenommen.
- Versuch 1 (ohne Deckel, nur wo Innenmittel ≤ Gelände, sonst Wert bleibt): nur die Hälfte angehoben → Spitzen verschoben, neue kleine Spitzen. Versuch 2 (gedeckelt): Spitzen weg.
- **Übernommen:** F7/G7-Nordufer, Mittelpunkt 246,0|268,7: 83 Ring-Vertices, 75 angehoben, Ring−Innen **vorher −0,394 m → nachher −0,167 m**, max. Hebung 0,40 m.
- **Kartenweit gemessen** (`pruefung/l3f/l3g_wv_karte_probelauf.json`, Probelauf mit derselben Regel; Ring−Innen vorher → im Probelauf, Anzahl Ring/angehoben):

| x\|z | Ring | angehoben | vorher m | Probelauf m | Bewertung |
|---|---|---|---|---|---|
| 70,5\|271,2 | 150 | 119 | −0,391 | −0,194 | kein sichtbarer Gewinn → nicht übernommen |
| 317,7\|275,0 | 120 | 106 | −0,374 | −0,195 | dto. |
| 284,8\|269,3 | 102 | 83 | −0,371 | −0,164 | neue helle Streifen → nicht übernommen |
| 145,0\|263,4 | 101 | 80 | −0,469 | −0,256 | kein sichtbarer Gewinn |
| 244,0\|269,2 | 98 | 90 | −0,381 | −0,147 | = F7/G7 → **übernommen** (Box-Lauf: 83/75, −0,394 → −0,167) |
| 114,1\|271,1 | 47 | 44 | −0,403 | −0,143 | kein sichtbarer Gewinn |
| 253,6\|273,5 | 47 | 45 | −0,341 | −0,143 | kein sichtbarer Gewinn |
| 171,9\|258,7 | 46 | 37 | −0,418 | −0,198 | neuer Splitter an der Inselspitze → nicht übernommen |
| 9,7\|270,2 | 42 | 27 | −0,223 | −0,083 | kein sichtbarer Gewinn |
| 83,4\|269,2 | 41 | 29 | −0,220 | −0,065 | dto. |
| 215,2\|11,1 | 32 | 30 | −0,312 | −0,139 | dto. |
| 150,1\|271,1 | 26 | 18 | −0,208 | −0,069 | dto. |
| 219,7\|224,0 | 24 | 9 | −0,495 | −0,384 | dto. |
| 285,9\|261,2 | 23 | 13 | −0,178 | −0,101 | dto. |
| 40,4\|260,4 | 20 | 12 | −0,217 | −0,100 | dto. |
| 12,0\|275,0 | 18 | 13 | −0,204 | −0,056 | dto. |
| 221,9\|264,5 | 17 | 14 | −0,224 | −0,090 | dto. |
| 1,8\|252,8 | 16 | 15 | −0,263 | −0,116 | dto. |
| 43,2\|268,9 | 15 | 12 | −0,224 | −0,100 | dto. |
| 192,0\|268,5 | 11 | 6 | −0,197 | −0,089 | dto. |
Nahbilder je Stelle (vorher / Probelauf): `l3g_nahbilder/versuche/C<x>_<z>_farbe_n3.jpg`. Grundgerüst kann einzelne Stellen per Box nachziehen.

## (2) E3-West – Verfahren
Art „ufer“ (wie L3e) mit Versatz 1,5 Vertices (Maske wächst nur), Glättung σ 3, Band 8 Vertices, linearer Kern 2,5 Vertices, Mindestneigung 0,15 m/Vertex,
Bett mind. 0,30 m unter dem Spiegel, Box-Fade 5 Zellen. 139 neue Wasser-Vertices (Gruppen entlang 180–190,5|88–125), 0 entfernt, Komponenten 9→9, keine Löcher
(fill_holes-Differenz = genau die neuen Vertices). Brücke E3 und Wege nicht angefasst (0 Vertices). Versuch 1 (Versatz 2, Band 6, Fade 3) gab 4 neue G6 → v2.

## Gate (Endstand bd8ab05)
regeln **367** (vorher 368), R8 **31**, R9 **321** (vorher 325), W1 **0**, W1 alle 56 0, Lochscan **0**. Gegen 8c1fc80: neu G6_facette E3 189,5|119,5 (Wert 7);
weg G6 E3 189,0|102,7 und 183,2|119,9 sowie 4 R8b-Dellen E3. Laufergebnisse `pruefung/l3f/gate_l3g/`, `pruefung/*_letzter_lauf.json` = dieser Lauf.

## Abstände / Wasser (`pruefung/l3f/l3g_abstaende.py` → `.json`, Basis 8c1fc80, zellweite_m 1,2)
Geänderte Vertices 1884 (GB 1809, WV 214 = 139 neue + 75 Ring, VC 0). Darauf: Wege **0** (kleinster Abstand 0,5 Zellen/0,6 m), Kreuzungen **0** (1,5/1,8 m),
Rampenkern **0** (9,19/11,0 m), WEGA/Wege/Brücken **0** (0,5/0,6 m), D2 **0** (15 Zellen; D2-GB sha 749d3c4b… vorher = nachher), Sperrzone D1 Mulde 159|22,9: 66 Zellen.
Wasser entfernt 0, WV auf altem Wasser nur die 75 Ring-Vertices (nur angehoben, alle < Nachbargelände), Bett über Spiegel 515 → 512.

## bau_endstand.sh
Schritt 15 aktiv (relief_l3f.py → html_payload_p3.py → waende_einsetzen.py), Nebenausgaben l3f_rueck.npz + l3f_bericht.json werden mitverglichen, `L3F=0` schaltet ab.
Volllauf `sh bau_endstand.sh /tmp/l3f_bau4` auf bd8ab05: **ENDBAU BITGLEICH (511 s)**, 33/33 gleich.

## Rückweg
`relief_l3f.py --aus` + html_payload_p3 + waende_einsetzen → relief_daten 98a6c8c4…, relief_neu 275ee752…, index 9b362957… = exakt 8c1fc80 (geprüft), danach wieder auf den Commit-Stand.

## SHA (Endstand)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | 4ce9daddbe113649e3664e3f7b725dfbf1eaf97ac2c21d7cdb25e71141e4c30f |
| neu/relief_neu.json.gz | a901f27b6131bd4eb9c0977c50628fb7973d06850a0fb88fe000dd211375a2a3 |
| index.html = neu/index.html | 70ce454b67f7c08fe23142fed2f469ca581cffad38a70e5f858f5255e3cab920 |
| relief_l3f.py | 502408c3fff0b34bcba4dbdc064c3c04f1de150a81f5a89784b8ece4315daf4d |
| bau_endstand.sh | 06e6698f4c97e1bc7da6818f0e1e14b1ae318ae86e42b45e400c2d711b1ed64d |
| pruefung/l3f/l3f_rueck.npz | 6f5ea9d9c26080c7c42969efb147e4c0c2b9afa49b8e18a2adc2c1b36b0bfd10 |
| GB/WV/VC (nachher_sha256) | 830c2304f7b4b1d2b7b4bd12c3afc7cd696805db8c821ebdb92b04f1b920e7bd |

## Nahbilder (`pruefung/l3g_nahbilder/`, selbst angesehen)
- `blatt_fg7_farbe_clay.jpg` (F7/G7 Distanz von Norden + nah, vorher|nachher Farbe, vorher|nachher Clay), `blatt_fg7_zoom_und_insel.jpg` (Ausschnitt der Spitzen + Inselspitze 172|259 unverändert).
- `blatt_e3_farbe_clay.jpg` (E3 Distanz von Norden und von Süden, nah 189|103 und 188|100; je Farbe/Clay vorher|nachher).
- `blatt_kartenweit_probelauf_nicht_uebernommen.jpg` (Begründung, warum nicht kartenweit).
- Einzelbilder `einzel/<Kamera>_{farbe,clay}_{vorher,nachher}.jpg`, Versuche `versuche/` (n2 = Versuchsstand v2 mit kartenweitem WV, C* = Probelauf je Stelle).
Bewertung: F7/G7 deutlich besser (Reihe weg, 1 schwacher Punkt bleibt); E3 Zacke weg und Ufer organisch, Bach etwas blasser; sonst keine sichtbare Änderung.

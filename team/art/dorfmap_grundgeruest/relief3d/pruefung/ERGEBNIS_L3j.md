# ERGEBNIS L3j – E3-Kanalanfang ≈190|97 als Trichter (QA P4g S1) – Basis art/dorfmap-fertig @ 0a0b83a

Kosten: 0 € · Codex: nein · Laufzeit: 22:10–22:42

Worktree /workspace/wt_dorfmap_L3j, Branch art/dorfmap-L3j auf origin/art/dorfmap-fertig = **0a0b83a** (geprüft, #40 gemergt; #41 QA-Doku noch offen → nicht darauf basiert, keine Überschneidung).
Neues Skript `relief_l3j.py` = bau_endstand **Schritt 19** nach L3i-Schritt 18 (`L3J=0` schaltet ab, L3J=1 mit L3I=0 bricht ab; Rückweg `--aus` mit `pruefung/l3j/l3j_rueck.npz`).
Stellen in `pruefung/l3j/l3j_stellen.json`, Basis-Hash GB/WV/VC = Stand nach Schritt 18 (7250e3bf…). Grundlage QA P4g (#41, `qa_p4g/bilder_0a0b83a/vn/E3_hals_190_97.jpg`). Checker und Schwellen unverändert.

## Ergebnis
**Gelöst.** Vorher sprang der Lauf bei z 95,5 von 5 auf 7 Vertices Breite und von ≈0,1–0,4 m auf 0,5 m Tiefe; der Spiegel im Oberlauf hatte eine Spaltentreppe (−1,31/−1,39 m) gegen −1,30 m im Kanal → dunkle Schulter.
Jetzt läuft der Übergang über 6 Zellen (z 89,5–95,5) trichterförmig: Breite 5 → 5 → 4–5 → 6 → 6 → 7 Vertices, tiefste Stelle je Zeile 0,22 → 0,50 m stetig, Spiegel je Spalte stetig vom Oberlauf auf −1,30 m (nur angehoben).
Bild (selbst angesehen, `l3j_nahbilder/paar_E3_hals.jpg`): aus 8, 12 und 22 m in Farbe und Clay keine Schulter mehr, der Oberlauf weitet sich gleichmäßig in den Kanal; Ufer weich, keine Kante, kein Zackenrand.
Ehrlich: Aus 8 m in Farbe bleibt am Westufer des Trichters ein ganz schwacher dunklerer Hauch (Hangschatten), deutlich schwächer als die alte Schulter; bei z 91 ist der Lauf in einer Vertexzeile 4 statt 5 Vertices breit (im Bild nicht erkennbar).

## Verfahren
- Art `kanal` aus relief_l3i.py, erweitert um einen Trichter: Halbbreite linear von 1,0 auf 1,75 Zellen, Kerntiefe linear von 0,15 auf 0,50 m über z 89,5–95,5; Spiegel je Spalte linear vom Oberlauf (Zeile vor z0) auf −1,30 m (`spiegel_start_aus_oberlauf`), alte Wasser-Vertices nur angehoben (25), nie gesenkt.
  Nur Wasser hinzugefügt (13 neue Wasser-Vertices), nichts entfernt. Land im Band 3 Zellen nur abgesenkt (Profil Spiegel + 0,04 m + 0,35 m/Zelle, nie unter Spiegel + 0,03 m), zu den Enden weich ausgeblendet; VC Kern-/Randton wie L3i.
- Art `hang_glatt` (`E3_hang_west`, wie L3h/L3i): Westhang 184,5\|91–94,5 – der erste Lauf hatte dort eine neue G6 184,5\|92,8 (Wert 6), danach weg.

## Gate (Endstand)
regeln **359** (Basis 359), R8 **31**, R9 **321**, W1 **0**, W1 alle 56 **0**, Lochscan **0** (offen_innen 0). Trefferliste identisch zur Basis (keine neue, keine weggefallene).
`pruefung/*_letzter_lauf.json` und `pruefung/l3j/gate/` (inkl. lochscan.json) = dieser Lauf. export_gate.sh meldet lokal wie immer „GATE ROT: kein Export/ZIP“ (kein Export-ZIP im Worktree).

## Abstände / Wasser (`pruefung/l3j/l3j_abstaende.py` → `.json`, Basis 0a0b83a, zellweite 1,2 m)
Geändert 439 Vertices (GB 367, WV 38, VC 277), Box 181,5–193,5\|87–98.
| Sperre | geänderte Vertices darauf | kleinster Abstand |
|---|---|---|
| Wege (Vektor) | 0 | 3,0 m |
| Kreuzungen | 0 | 2,47 m |
| Rampenkern | 0 | 66,4 m |
| WEGA/Wege/Brücken | 0 | 1,2 m |
| D2 | 0 | 16,7 m (GB-sha 749d3c4b… vorher = nachher) |
| rampe_5 | 0 | 68,2 Zellen = 81,9 m |
| Kachel D4/D5 | 0 Änderungen | 34,9 Zellen |
| D1 (inkl. X084/rampe_2) | 0 | 47,0 Zellen |
| Mulde 159\|22,9 | 0 | gemessen 69,0 Zellen = 82,8 m (49 Zellen außerhalb Sperrkreis r 20) |
Wasser entfernt 0, Komponenten 7 → 7, neu 13 (nur Trichter), WV auf altem Wasser nur die 25 angehobenen Vertices, fill_holes-Differenz = genau die 13 neuen (keine Löcher), Bett über Spiegel 493 → 493.

## bau_endstand.sh
Schritt 19 (relief_l3j.py → html_payload_p3.py → waende_einsetzen.py), Nebenausgaben l3j_rueck.npz + l3j_bericht.json mitverglichen.
Volllauf: **ENDBAU BITGLEICH (784 s)**, 41/41 Ausgaben gleich (inkl. l3i_rueck/bericht und l3j_rueck/bericht), Schritt 19 l3j 12 s.

## Rückweg
`relief_l3j.py --aus` + html_payload_p3 + waende_einsetzen → relief_daten 643bc530…, relief_neu d7b66b02…, index e1561e91… = **exakt 0a0b83a** (geprüft), danach wieder Commit-Stand.

## SHA (Endstand)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | 2aa3cfe4f89c4971a137580e7b965f08e616397ce0ddbf39a66f77adebad8ee9 |
| neu/relief_neu.json.gz | f4a23c64f26e6ce41b2b17c023c3bf3769dc7ac215452846373eb4c281267055 |
| index.html = neu/index.html | 3d4aade0e4361655f920b695ae071728f694b66db300c36e6cb2fcc4cab91ba2 |
| relief_l3j.py | c5638e58917afc02671d80a6a947ee5a80b47dfe29cd9f4cdfad786be6fccbd3 |
| bau_endstand.sh | aac60ce049ec9611430384805ab5fd78e7aa62a27c3abb82337bb3b6e0e622e8 |
| pruefung/l3j/l3j_rueck.npz | 164c4310a25b806b2cc0c944f53526a5a23f307ecc6b558c1136408c9790dbb0 |

## Nahbilder (`pruefung/l3j_nahbilder/`, selbst angesehen)
- `paar_E3_hals.jpg`: E3 190\|97 aus 8 m und 12 m, 190\|98 aus 22 m; je Farbe vorher (0a0b83a) | nachher, Clay vorher | nachher.
- Einzelbilder `einzel/E3_hals_d{8,12,22}_{farbe,clay}_{vorher,nachher}.jpg`.

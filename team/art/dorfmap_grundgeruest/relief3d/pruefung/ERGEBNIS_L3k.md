# ERGEBNIS L3k – Kerbe am Grat an der Kachelecke B3/C3/B4/C4 bei 84|129 (Kritiker P8) – Basis art/dorfmap-fertig @ cc33fd1

Kosten: 0 € · Codex: nein · Laufzeit: 23:12–23:43

Worktree /workspace/wt_dorfmap_L3k, Branch art/dorfmap-L3k auf origin/art/dorfmap-fertig = **cc33fd1** (geprüft).
Neues Skript `relief_l3k.py` = bau_endstand **Schritt 20** nach L3j-Schritt 19 (`L3K=0` schaltet ab, L3K=1 mit L3J=0 bricht ab; Rückweg `--aus` mit `pruefung/l3k/l3k_rueck.npz`).
Stelle in `pruefung/l3k/l3k_stellen.json`, Basis-Hash GB/WV/VC = Stand nach Schritt 19 (5ac12adb…). Checker und Schwellen unverändert. Viewer-Dateien (index.html-Logik, Shader, Viewer-Code) nicht angefasst; index.html / neu/index.html sind nur die neu erzeugte Pipeline-Ausgabe (html_payload_p3 + waende_einsetzen).

## Ursache
Kein früherer Glättungsschritt: kein `*_rueck.npz` aus L3d–L3j berührt x 80–89 \| z 124–133, die Form stammt aus der Basisgenerierung.
Es ist ein **Lage-Versatz der Westkante/des Grats über die Kachelecke**: Die 5-m-Höhenlinie der Steilkante steht in Kachelreihe 3 bis z ≈ 130 fest bei x ≈ 84 (genau auf der Naht B|C), in Reihe 4 springt sie innerhalb von 2 Zellen (z 130,5–132) auf x ≈ 81,5 und läuft dann normal weiter. Der Grat aus dem Süden (Krone x 83–84, z 134–137) und die Kante aus dem Norden (Krone x 86, z 122–127, Wandquellzellen Krater teil 6) treffen deshalb versetzt aufeinander. Von der Kritikerkamera aus sieht man genau dort einen Einschnitt, wo der vordere Grat auf die steile Flanke trifft (15 m: Kerbe; 30 m: „Häkchen“). Ein Höhen-Versatz an der Naht selbst (Sprung zwischen Nachbarvertices) besteht nicht.
Lage per Markierungs-Render bestätigt: Spalten x 84/86/88 und Zeilen z 126/129/132 wurden testweise eingefärbt, nur im /tmp-Viewer, die Daten wurden danach bitgleich zurückgesetzt.

## Ergebnis
**Gelöst für die Kerbe.** Die Steilkante läuft jetzt stetig diagonal: 5-m-Linie x 84 (z 125) → 83 (z 129) → 82 (z 133) → 81 (z 136), also kein Sprung mehr. Der vordere Grat geht ohne Einschnitt in die Flanke über.
Änderung: GB von 113 Vertices in x 80,5–86 \| z 125–133, max. 2,38 m (die Kante wird an der Ecke aufgefüllt). Wasser, WV und VC sind unverändert.
Bild (selbst angesehen, `pruefung/l3k_nahbilder/paar_grat_84_129.jpg`): Aus 15 m ist die Kerbe in Farbe und Clay weg, und es gibt keine neue Stufe. Aus 30 m ist das Häkchen zu einer weichen Biegung geworden.
**Ehrlich:** Die sägezahnartigen Facetten auf der Südflanke des vorderen Grats (≈ x 81–84 \| z 133–137, in Clay aus 15 m deutlich, in Farbe schwach) bleiben. Sie sind vorher und nachher gleich, gehören nicht zur Kerbe und liegen außerhalb dieser Änderung. Ein Versuch, auch sie mitzunehmen, erzeugte neue G6-Facetten, deshalb ist das Gebiet eng gefasst.

## Verfahren
- Neue Art `laengs_glatt`: Gauss-Mittel (σ 6 Vertices, 2 Runden) **entlang der Gratrichtung** (dx −3,4, dz 9 Zellen) im Kreis um 83,2\|129 (Kern r 2, weich bis r 4,5).
- Gratkrone/Plateau (> 9 m) wird nur gehoben, nie gesenkt, damit keine neue Delle in der Krone entsteht. Der Hangfuß (< 3 m) bleibt unverändert, damit die vorhandene Fußkante nicht zerschnitten wird.
- Wandquellzellen haben ≥ 3 Vertices Abstand, weich über 3 Vertices. Das Feinband wird nur auf geänderten Vertices nachgeführt. Bei Wasser im Gebiet bricht das Skript ab.
- Zwischenstände waren 360–363, wegen neuer G6 bei 75,9\|135,8, 86,5\|134,5 und 87,8\|128,9. Die Ursachen: zerschnittene Fußkante, Delle in der Krone, Feinband auf ungeänderten Vertices. Daraus folgen die Schutzregeln oben. Endstand 359.

## Gate (Endstand)
regeln **359** (Basis 359), R8 **31**, R9 **321**, W1 **0**, W1 alle 56 **0**, Lochscan **0** (offen_innen 0). Die Trefferliste ist identisch zur Basis: keine neue, keine weggefallene.
`pruefung/*_letzter_lauf.json` und `pruefung/l3k/gate/` = dieser Lauf. export_gate.sh meldet lokal wie immer „GATE ROT: kein Export/ZIP“ (kein Export-ZIP im Worktree).

## Abstände / Wasser (`pruefung/l3k/l3k_abstaende.py` → `.json`, Basis cc33fd1, Zellweite 1,2 m)
Geändert: 113 Vertices (GB 113, WV 0, VC 0), Box 80,5–86\|125–133.
| Sperre | geänderte Vertices darauf | kleinster Abstand |
|---|---|---|
| Wege (Vektor) | 0 | 85,6 m |
| Kreuzungen | 0 | 83,5 m |
| Rampenkern | 0 | 59,0 m |
| WEGA/Wege/Brücken | 0 | 84,1 m |
| D2 | 0 | 67,9 m (GB-sha 749d3c4b… vorher = nachher) |
| rampe_5 | 0 | 50,8 Zellen = 60,9 m |
| Kachel D4/D5 | 0 Änderungen | 40,0 Zellen = 48,0 m |
| D1 (inkl. X084/rampe_2) | 0 | 91,7 Zellen = 110,0 m |
| Mulde 159\|22,9 | 0 | 126,1 Zellen = 151,3 m (106,1 Zellen außerhalb Sperrkreis r 20) |
Wasser: entfernt 0, neu 0, Komponenten 7 → 7, Maske und WV gleich, fill_holes gleich (keine Löcher), Bett über Spiegel 493 → 493.

## bau_endstand.sh
Schritt 20 läuft so: relief_l3k.py → html_payload_p3.py → waende_einsetzen.py. Die Nebenausgaben l3k_rueck.npz und l3k_bericht.json werden mitverglichen.
Volllauf: **ENDBAU BITGLEICH (521 s)**, 43/43 Ausgaben gleich (inkl. l3j_rueck/bericht und l3k_rueck/bericht), Schritt 20 l3k 12 s.

## Rückweg
`relief_l3k.py --aus` + html_payload_p3 + waende_einsetzen → relief_daten 2aa3cfe4…, relief_neu f4a23c64…, index 3d4aade0… = **exakt cc33fd1** (geprüft, Datendateien git-sauber). Danach erneut angewendet → bitgleich zum Commit-Stand.

## SHA (Endstand)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | 0d0296bab993012267fa02f48b6b8d0c7127dd0dabb498e29d72de42150a3549 |
| neu/relief_neu.json.gz | 2b49e689b68e4285d05dbf443839a3a89a227099890ececfe5b29ce56d196c3d |
| index.html = neu/index.html | f356c5a3dc2326be75d3a4bd136192dc98598192166b7f92e7d137ca188bac08 |
| relief_l3k.py | bca2e289b8ff21d76cd25552ac6e50e11e9ea584f12d685a4ec03cf771e836f2 |
| bau_endstand.sh | ca59a55aff08f91066dcf3b86fa708cf6dfb74152a1d7a872cd0c581350c312a |
| pruefung/l3k/l3k_rueck.npz | 4b59f6e78bf00228182b7674e3799ad9f36615af026238aec3cc41c680b3ea47 |

## Nahbilder (`pruefung/l3k_nahbilder/`, selbst angesehen)
- `paar_grat_84_129.jpg`: Kritikerkamera (`pruefung/qa_p4f/rendere_kacheln.js`, PUNKTE wie `tmp_kritik_p8/pk3.json`: 84\|129, el 35, az 0, d 15 oben / d 30 unten). Spalten: Farbe vorher (cc33fd1) | Farbe nachher | Clay vorher | Clay nachher.
- Einzelbilder `naht_84_129_d{15,30}_{vor,n5}_{0=Farbe,1=Clay}.jpg`.

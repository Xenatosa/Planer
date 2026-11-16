# ERGEBNIS L3m – dunkle Linie am Ufer des E3-Kanals bei x≈188 | z≈97 (P13b, Dev UI) – Basis art/dorfmap-fertig @ 087c124

Kosten: 0 € · Codex: nein · Laufzeit: 00:35–00:54

Worktree /workspace/wt_dorfmap_L3m, Branch art/dorfmap-L3m auf **087c124**. #45 (P13) war beim Start schon gemergt, deshalb setzt der Branch direkt auf dem neuen Kopf auf.
Neues Skript `relief_l3m.py` = bau_endstand **Schritt 22** nach L3l-Schritt 21 (`L3M=0` schaltet ab, L3M=1 mit L3L=0 bricht ab; Rückweg `--aus` mit `pruefung/l3m/l3m_rueck.npz`).
Stelle in `pruefung/l3m/l3m_stellen.json`, Basis-Hash GB/WV/VC = Stand nach Schritt 21 (41e5ccd4…). Checker und Schwellen unverändert. Viewer-Dateien nicht angefasst; index.html / neu/index.html sind nur per Pipeline neu erzeugt, nicht von Hand gemergt.
Beurteilt wurde im neuen Viewer (Gelände nur Vorderseite), nicht mit ?silh=0. Vorher wurde der Platz mit df geprüft (21 GB frei); aufgeräumt wurden nur eigene /tmp-Reste (/tmp/l3l_bau1, Viewer-Builds).

## Ergebnis: **Farbe allein hat gereicht, Geometrie war nicht nötig**
Nur VC geändert, und zwar 234 Uferecken entlang des ganzen E3-Kanalabschnitts der Runden L3i/L3j (Box x 186,5–191 | z 86–112). GB und WV sind bitgleich zur Basis, kein Wasser wurde entfernt, der Wasserspiegel bleibt bei −1,30 m.
Die Linie trat nicht nur bei z 97 auf: Längs des ganzen Kanals (z 86–112) tragen die erste nasse Ecke an beiden Ufern R 141–150 und die trockene Nachbarecke R 167–186. Deshalb wurde der ganze Abschnitt behandelt.
Verfahren (Art `ufer_farbe`): Die nassen Ecken mit trockenem 8er-Nachbarn (Rand, 122 Vertices) werden zu 70 % zur mittleren Farbe des angrenzenden trockenen Ufers (5×5) verschoben, die nächste nasse Reihe (innen, 112 Vertices) zu 30 %. Das Bett in der Kanalmitte bleibt dunkel.

### Messwerte z = 97,5 (vorher → nachher)
| x | 187,0 | 187,5 | 188,0 | 188,5 | 189,0 | 190,0 | 190,5 | 191,0 | 191,5 |
|---|---|---|---|---|---|---|---|---|---|
| GB (unverändert) | −1,063 | −1,238 | −1,549 | −1,795 | −1,800 | −1,800 | −1,631 | −1,385 | −1,108 |
| WV (unverändert) | – | – | −1,30 | −1,30 | −1,30 | −1,30 | −1,30 | −1,30 | – |
| VC R vorher | 186 | 171 | **146** | 141 | 141 | 141 | 145 | **150** | 175 |
| VC R nachher | 186 | 171 | **170** | 151 | 141 | 148 | 154 | **171** | 175 |
Ecke 188,0: VC (146,155,160) → (170,180,188). Die Uferstufe von 0,31 m auf 0,5 Zellen bleibt in der Geometrie, ist in Farbe aber nicht mehr als Linie zu sehen.

Bildmessung, p13b-Kamera D3_U (gleiches Bild wie `p13b_d3/D3_U_base.png`, vorher pixelgleich), Luminanz-Transekt Spalte 690, Zeilen 158–187:
- vorher … 113 119 125 131 **116** 151 171 …: die dunkle Linie ist eine Senke von 116 zwischen 131 und 151.
- nachher … 113 119 128 139 **142** 156 171 …: monoton, keine Senke mehr.

Quer zum Ufer aus 15 m (az 90), Spalte 200: vorher fällt die Luminanz am Ufer von 164 bis 108, nachher läuft sie über 163–155 weich aus und fällt erst im Wasser.

### Bilder (selbst angesehen)
`pruefung/l3m_nahbilder/paar_E3_ufer_188_97.jpg`. Zeilen: 188|97,5 aus 8, 15 und 30 m (el 35, az 0), D3_U (p13b-Kamera, focus D3, 30 m) und 15 m quer zum Ufer (az 90). Spalten: Farbe vorher | nachher | Clay vorher | nachher. Dazu `D3_U_ausschnitt_686_178_x5_vorher_nachher.jpg`.
- Farbe: Der dunkle Saum an der Wasserlinie ist aus 8, 15 und 30 m weg. Das Ufer verläuft weich vom Schnee ins Wasser, im Ausschnitt ×5 ist die 1-px-Linie verschwunden.
- Ehrlich: Ein ganz weicher grauer Übergang am Wasserrand bleibt. Er kommt vom halbtransparenten Wasser über dem dunkleren Bett, nicht von einer Linie.
- Clay (ohne VC) ist erwartungsgemäß unverändert: Die Uferstufe zeichnet dort weiter nur schwach, wie in P13b gemessen (114 gegen 118).
- Der L3i/L3j-Kanal und der Trichter sind nicht verschlechtert: Geometrie und Wasser sind bitgleich, nur die Uferfarbe ist heller.

## Gate (Endstand)
regeln **359** (Basis 359), R8 **31**, R9 **321**, W1 **0**, W1 alle 56 **0**, Lochscan **0** (offen_innen 0). Die Trefferliste ist identisch zur Basis.
`pruefung/*_letzter_lauf.json` und `pruefung/l3m/gate/` = dieser Lauf. export_gate.sh meldet lokal wie immer „GATE ROT: kein Export/ZIP“.

## Abstände / Wasser (`pruefung/l3m/l3m_abstaende.py` → `.json`, Basis 087c124, Zellweite 1,2 m)
| Sperre | geänderte Vertices darauf | kleinster Abstand |
|---|---|---|
| Wege (Vektor) | 0 | 2,4 m |
| Kreuzungen | 0 | 5,4 m |
| Rampenkern | 0 | 67,2 m |
| WEGA/Wege/Brücken | 0 | 4,6 m |
| D2 | 0 | 23,4 m (GB-sha 749d3c4b… vorher = nachher) |
| rampe_5 | 0 | 61,6 Zellen = 73,9 m |
| Kachel D4/D5 | 0 Änderungen | 25,1 Zellen = 30,1 m |
| D1 (inkl. X084/rampe_2) | 0 | 47,2 Zellen = 56,6 m |
| Mulde 159\|22,9 | 0 | 69,2 Zellen = 83,1 m (49,2 Zellen außerhalb Sperrkreis r 20) |
Wasser: entfernt 0, neu 0, Komponenten 7 → 7, Maske und WV gleich, GB gleich, fill_holes gleich (keine Löcher), Bett über Spiegel 493 → 493.

## bau_endstand.sh
Schritt 22 läuft so: relief_l3m.py → html_payload_p3.py → waende_einsetzen.py. Die Nebenausgaben l3m_rueck.npz und l3m_bericht.json werden mitverglichen.
Volllauf: **ENDBAU BITGLEICH (530 s)**, 47/47 Ausgaben gleich (inkl. l3l_rueck/bericht und l3m_rueck/bericht), Schritt 22 l3m 12 s.

## Rückweg
`relief_l3m.py --aus` + html_payload_p3 + waende_einsetzen → relief_daten 2d69e9e1…, relief_neu 5a8c87b4…, index 842cc952… = **exakt 087c124** (Datendateien git-sauber). Danach erneut angewendet → bitgleich zum Commit-Stand.

## SHA (Endstand)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | 4c2d045a0d84f605b03506ee18134eada5f2dab7df8227e4337f47b4f4e18fd4 |
| neu/relief_neu.json.gz | c64e0262f693ebc4095e62116514c715d5fa2f02659c0221ba822babb40fd127 |
| index.html = neu/index.html | 34b5a9e7499e3b1947d9e36dcd4a7dd140c18e7c811402b8e6f7deb700bbf5da |
| relief_l3m.py | 5c976fa06f305683c1997c7330570b4ab3bd830143ac2548e711f40308e3f600 |
| bau_endstand.sh | 6c9a4f51c75e2ceb403f417f8830d409c990c366291700b21436fb1d516f8502 |
| pruefung/l3m/l3m_rueck.npz | b80c04cbca574e4da461717f082fb28c43f42b16a48303aa275499fe9ed27988 |

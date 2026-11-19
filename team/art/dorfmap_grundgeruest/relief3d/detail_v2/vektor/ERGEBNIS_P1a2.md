# ERGEBNIS P1a2 – Nachbesserung Q3-Zacken (Branch art/dv2-vektor-wege-q3)

Kosten: 0 € · Codex: nein · Laufzeit: 15:47–16:38 (Unterbrechung ~16:35–16:37) (Europe/Berlin, 19.11.2026)

Basis: art/dorfmap-fertig 8a38922 (#56 ist gemergt, daher nicht gestapelt). Geändert werden nur Dateien in detail_v2/vektor/.

## Entscheidungen Dorfmap zu #56 (19.11.)
- Kreuzungsüberstand bis 1,5 m ist ok, R8 „eben“ gilt innerhalb der Platte.
- Die E2-Lücke gehört zum Brückenmodul P5.
- Wegenden bleiben ungekürzt.
- ERG01–03 sind ok.

## PLAN
1. Die QA-Methode nachbauen und die Abweichung zu unserer Messung belegen. Zwischenziel: G903a mit 3,12 cm reproduziert.
2. test_wege.py misst beide Methoden, hart ≤ 3,0 cm, und meldet die Top 5 sowie die Zahl der Linien über 2,7 cm.
3. Ränder nachglätten: Innenrundung größer, Ring-σ adaptiv, lokales Nachglätten, Einzug bei U-Wegen. Zwischenziel: alle Ränder ≤ 2,7 cm.
4. Kreuzungen mit Radius ≥ 2,35 m einpassen, Überstand ≤ 1,5 m. Zwischenziel: alle Umrisse ≤ 2,7 cm.
5. Übrige Abnahmewerte halten, altes Gate, PR.

## Ursache
Die Zackenmessung in test_wege.py (Methode **A**) hat die Linie auf 0,05 m nachgetastet und gegen ein *kontinuierliches* 1-m-Mittel gemessen. Die QA (Methode **B**) mittelt über die gespeicherten 0,25-m-Stützpunkte (±2 Punkte).

Auf einem Kreisbogen mit Radius R ergibt das folgende Sehnenfehler:
- A: etwa 4,2 cm / R
- B: etwa 6,25 cm / R, also um den Faktor 1,5 mehr

Unsere Eigenprüfung lag mit 2,9 cm (A) knapp unter der Grenze. Nach B lagen deshalb enge Kurven und alle Kreuzungsumrisse (Eckradius 1,85–2,0 m) über 3 cm.

B reproduziert G903a genau mit 3,12 cm. Für G003_anb ergibt B 3,53 cm, die QA meldet 3,45 cm. Die QA behandelt Fenster oder Enden vermutlich leicht anders. B ist hier eher strenger.

## Methode [A]
- **Ziel:** beide Methoden ≤ 2,7 cm (Eigennote im Extraktor), hart ≤ 3,0 cm im Test.
- **Bänder:**
  - Innenrundung bis 2,6 m (vorher 2,2 m).
  - Ring-Gauß σ adaptiv 0,3–1,0 m.
  - Reicht das nicht, glättet `ring_lokal` lokal nach: Gauß σ 0,5 m nur um die Stützpunkte mit Zacken über 2,4 cm.
- **U- und Schleifenwege (G015, G018):**
  - Der freie Innenraum hat einen Inkreisradius von nur etwa 1,8 m. Seine Randradien liegen damit zwangsläufig unter 2,1 m, also bei B über 3 cm.
  - Deshalb wird der Innenrand um 0,7 m eingezogen. Der Weg ist dort innen schmaler, etwa 2,3 statt 3,0 m.
- **Kreuzungen:**
  - Radius 2,6 / 2,45 m.
  - Zweiter Durchgang für schmale Platten: Kern (P ∩ Netz) um 0,25–1,45 m verdickt, damit die Platte mittig liegt, dort auch r 2,35 m.
  - Wahl nach kleinstem Überstand ≤ 1,45 m (Grenze 1,5 m, 5 cm Reserve). Die Abdeckung von P ∩ Netz ist ≥ 90 %, in 2 Fällen ≥ 50 %.

## Messwerte vorher (#56, 8a38922) / nachher
| Prüfung | vorher | nachher | Grenze |
|---|---|---|---|
| Zacken A Ränder max | 2,89 cm (G018/0 re) | **2,18 cm** (G018/0 re) | ≤ 3,0 (Ziel 2,7) |
| Zacken B Ränder max | 3,73 cm (G018/0 re), 7 Linien > 3, 51 > 2,7 | **2,70 cm** (G018/0 re), 0 > 3, 0 > 2,7 | ≤ 3,0 (Ziel 2,7) |
| Zacken A Kreuzungen max | 2,74 cm (K068), 36 > 2,7 | **2,16 cm** (K044), 0 > 2,7 | ≤ 3,0 |
| Zacken B Kreuzungen max | 3,40 cm (K041), 88 > 3 | **2,67 cm** (K004), 0 > 2,7 | ≤ 3,0 |
| Knick max Ränder / Kreuzungen | 8,59° / 7,86° | 7,14° / 6,20° | ≤ 15° |
| Mittellinie max | 0,246 m (G018/0) | 0,246 m (G018/0) | ≤ 0,3 m |
| Offene Wegenden | 0 | 0 | 0 |
| Netzteile / WEGA-Komponenten | 2 / 2 | 2 / 2 | |
| WEGA außerhalb Netz | 194 (98,64 %) | 164 (**98,85 %**), größter Cluster 19 | nicht schlechter |
| Plätze angeschlossen | 30/30 | 30/30 | 30/30 |
| Kreuzungsüberstand max / Median | 1,39 / 0,60 m | 1,45 / 1,01 m | ≤ 1,5 m |
| Randvollständigkeit | ok | ok (min 0,46, Bandfläche ≤ 1,07 × Soll) | |

Top 5 vorher, Methode B, Ränder (cm): G018/0 re 3,73 · G003_anb re 3,53 · G015 li 3,49 · G018/0 li 3,38 · G903a li 3,12
Top 5 nachher, Methode B, Ränder (cm): G018/0 re 2,70 · G903a li 2,65 · G003_anb re 2,63 · G009/1 re 2,62 · G015 li 2,62
Top 5 vorher, Methode A, Ränder (cm): G018/0 re 2,89 · G015 li 2,81 · G003_anb re 2,77 · G018/0 li 2,67 · G903a li 2,50
Top 5 nachher, Methode A, Ränder (cm): G018/0 re 2,18 · G009/1 re 2,12 · G015 li 2,12 · G903a li 2,12 · G003_anb re 2,07
Top 5 vorher, Methode B, Kreuzungen (cm): K041 3,40 · K025 3,40 · K014 3,40 · K083 3,39 · K077 3,39
Top 5 nachher, Methode B, Kreuzungen (cm): K004 2,67 · K043 2,67 · K011 2,67 · K013 2,66 · K005 2,65

## Gate-Regression, über export_gate.sh
Das Gate lief NUR über `pruefung/export_gate.sh`, mit Lochscan:
1. `NODE_PATH=/tmp/relief3d_bau_node/node_modules HTML=index.html OUT=/tmp/dv2_wege/loch.json RAND=0.6 node pruefung/loch_o18g.js` ergab 9 Meshes, 88 728 Dreiecke, offen_innen 0.
2. `GATE_LOCH_JSON=/tmp/dv2_wege/loch.json sh pruefung/export_gate.sh` lief in einem Wegwerf-Worktree des PR-Stands unter /tmp. So landen die `*_letzter_lauf.json` des Skripts nicht im Repo.

| Prüfer | Ergebnis | Referenz |
|---|---|---|
| pruefe_regeln.py (mit LOCHSCAN) | **359** | 359 |
| R8 | 31 (21 Kreuzungen) | 31 |
| R9 | 321 | 321 |
| W1 index.html | 0 | 0 |
| W1 alle 56 Kacheln | 0 | 0 |

Das Gate meldet „GATE ROT“ wie auf der Referenz. Die 359 Treffer bestehen schon vorher. Die Regeln lesen nur relief_daten.json.gz und index.html, dieser PR ändert nur detail_v2/vektor/.

**Korrektur zu #56:** Dort stand „pruefe_regeln 360, identisch auf d2d4824“. Das war falsch. Ursache: Ich habe pruefe_regeln.py direkt aufgerufen, ohne LOCHSCAN. Dann zählt die Regel `G1_lochscan_fehlt` +1. Über export_gate.sh mit GATE_LOCH_JSON ergeben d2d4824 (laut Aufseher) und der neue Stand **359**. Künftig läuft das Gate nur so.

## Restrisiken / Vereinfachungen
- **G018/0 re:** Zacken B genau 2,70 cm, also keine Reserve unter dem Ziel. Gegen 3,0 cm bleiben 0,3 cm.
- **G015 und G018:** Innenrand 0,7 m eingezogen. Die Wege sind dort innen lokal schmaler. Rand gegen Offset ±b/2 bis 1,58 m.
- **Kreuzungsplatten:**
  - Größer als vorher: Überstand im Median 1,0 m statt 0,6 m.
  - K050 deckt nur 51 % und K063 nur 71 % von P ∩ Netz, weil die Quellpolygone lange Arme haben. Die Platte deckt den Kern, die Arme bleiben Band.
  - K004 trägt stufe 2 nur wegen Rundung (Überstand 1,4500 ≥ 1,45); alle Grenzwerte hält sie ein.
- **Laufzeit:** Der Extraktor braucht jetzt etwa 6 min (Kreuzungssuche).

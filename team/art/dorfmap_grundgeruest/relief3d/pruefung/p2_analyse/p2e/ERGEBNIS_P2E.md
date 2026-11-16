# P2e – rampe_5 Milchband D4 (≈133|155) und Milchfleck D5 (≈135|185), QA P4e (#36)

**Kosten 0 €, Codex nein, Laufzeit ~0,8 h (18:45–19:30 MEZ)**

Basis: art/dorfmap-fertig **bfe8dce**. Branch wege/dorfmap-p2e, kein Force-Push. Der alte Branch wege/dorfmap-p2d bleibt bestehen.

## Messung vorher [S]
Gemessen wurde auf der P2d-Farbfläche S7 (1842 Knoten) gegen einen Ring (2–16 Knoten außerhalb, ohne Wasser und Wege).
- **Helligkeit:** L 213,1 in der Fläche, 208,2 im Ring, also **ΔL +4,8**.
- **Sättigung:** S 0,0717 in der Fläche, 0,0700 im Ring, also ΔS +0,0017.
- **Streuung:** L-Streuung 13,8 in der Fläche, 22,5 im Ring; L10 195 in der Fläche, 176 im Ring.
- **Ergebnis:** Die Fläche war heller und hatte zu wenige dunkle Flecken. Die Poisson-Einpassung aus P2d hatte die Spenderfarbe geglättet.
- **Nicht die Ursache:** die Schattierung. Lambert ist in der Fläche 0,40, im Ring 0,46.

## Maßnahme (nur VC, relief_p2e.py)
- **Farbe aus dem Umfeld:** Die Farbe wird je Knoten **1:1 aus einem Spender-Versatz kopiert**. Zur Auswahl stehen 7 Versätze (−26/−18/+14/−34/+22 Zellen in x, −30/+24 in z). Gewählt wird der Versatz mit der **gleichsten Hangneigung** (geglättete Kosten). Nur dort, wo zwei Versätze fast gleich gut sind, wird weich gemischt (exp-Gewicht τ 0,4°). Das verhindert Sägezahn-Nähte.
- **Harte Farbsprünge** über 55 (T1 zählt ab 70) werden lokal geglättet.
- **Angleich je Zone:** Das Mittel-RGB jeder Zone (Nord D4 / Süd D5, Grenze z 170) wird auf ihren Ring gezogen. Der Rand ist über 6 Knoten weich.
- **Unverändert:** GB, WV, WEGA, Wege und Brücken. Es gibt **kein Mikrorelief**. FW.c der Prototypen folgt der VC (6112 Punkte). Kein gen_textur-Lauf.
- **Sperren:** D2, E3/E4 (x168–210, z86–172), Zeile 7 und alle von L3d/L3e/L3f geänderten Knoten (+2) sind im Skript gesperrt, mit Abbruchprüfung.

## Messwerte ΔL / ΔS (Fläche minus Ring, p2e_bericht.json)
| Bereich | ΔL vorher | ΔL nachher | ΔS vorher | ΔS nachher | L-Streuung vorher → nachher (Ring) |
|---|---|---|---|---|---|
| Gesamt (1842 Kn.) | +4,83 | **−0,20** | +0,0017 | −0,0037 | 13,8 → 16,8 (22,5) |
| Zone Nord D4 | +5,71 | **−0,03** | +0,0011 | −0,0087 | 13,5 → 16,8 (25,9) |
| Zone Süd D5 | +4,44 | **−0,11** | +0,0023 | 0,0000 | 13,7 → 16,3 (19,9) |
| Fenster ±8 Zellen um 133\|155 (kleiner Ring) | −3,08 | −1,77 | −0,0165 | −0,0111 | – |
| Fenster ±8 Zellen um 135\|185 (kleiner Ring) | +1,13 | +3,16 | −0,0037 | +0,0065 | – |

Das Ziel ΔL ≤ 1 ist für die Gesamtfläche und beide Zonen erfüllt. In den kleinen ±8-Zellen-Fenstern streut der Wert stark, weil der Ring dort nur wenige Knoten hat. Im Fenster D5 liegt er bei +3,2 (Restrisiko, siehe unten).

## Gate (P2E_gate_vorher_nachher.json)
| Regel | vorher (bfe8dce) | nachher |
|---|---|---|
| regeln | 367 | 367 (0 neu, 0 weg) |
| R8 | 31 | 31 |
| R9 | 321 | 321 |
| W1 index / alle 56 | 0 / 0 | 0 / 0 |
| Loch index / alle 56 | 0 / 0 | 0 / 0 |

- **D2:** bitgleich (GB/VC/WV/WEGA).
- **Vertex-Hash D1/G1/D2:** index.html und alle_kacheln identisch (belege/hash_vergleich.md), Lochscan 56 Kacheln 0 (belege/lochscan_alle.md).
- **T1 im Zwischenlauf:** Ein Zwischenlauf ergab einen neuen T1_fleckrand bei D5 134.9\|172.6. Er ist durch die Kantenglättung des Spenderfelds behoben.

## bau_endstand
- Neuer **Schritt 16 P2e** nach L3f/L3g (15): relief_p2e.py, html_payload_p3.py, waende_einsetzen.py.
- **Abschaltbar** mit `P2E=0`. P2E folgt standardmäßig L3F.
- Nachweis: `sh bau_endstand.sh /tmp/p2e_endstand` → **ENDBAU BITGLEICH (476 s)**, 35/35 Ausgaben gleich, einschließlich p2e_rueck.npz und p2e_bericht.json (belege/endstand_sha256_vergleich.txt).

## Nahbilder (nahbilder/, Farbe und Ton; oben vorher bfe8dce, unten nachher)
- **Nah:** D4_nah (133\|163, 15 m), D5_nah (135\|185, 15 m), N04_D4_milchband (35 m), N05_D5_milchfleck (35 m).
- **Distanz:** D4D5_distanz (80 m), D4D5_draufsicht (45 m, senkrecht).

## Restrisiken
- Im Tonbild bleibt die Fläche glatt, weil GB unverändert ist und auf Mikrorelief bewusst verzichtet wurde. Der Hang ist in der Fläche etwas steiler (18,6° gegenüber 15,3° im Ring).
- Die L-Streuung (Fleckung) liegt mit 16,8 noch unter dem Ring (22,5). Die weiche Spenderwahl dämpft den Kontrast etwas; die harte 1:1-Wahl ergab sichtbare Sägezahn-Nähte.
- Lokales Fenster D5 135\|185: ΔL +3,2 gegenüber dem kleinen Nahring. Die Zone erfüllt das Ziel, im Bild ist der Fleck deutlich schwächer. Sollte per QA-Sicht bestätigt werden.

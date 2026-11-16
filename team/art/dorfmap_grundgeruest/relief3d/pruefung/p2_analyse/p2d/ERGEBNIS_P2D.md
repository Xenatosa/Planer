# P2d – rampe_5-Band (D4/D5) und Brückenanschlüsse E2/E3 (QA-Befund P4d)

**Kosten 0 €, Codex nein, Laufzeit ~1,7 h (15:45–17:25 MEZ, inkl. Unterbrechung)**

Basis: art/dorfmap-fertig **1778473** (nach L3d-Merge #31 und L3e). Der Auftrag nannte 2771f70. Die Basis ist während der Arbeit zweimal weitergerückt (b3698e0 L3d, 1778473 L3e). Deshalb wurde P2d auf 1778473 neu aufgesetzt: Basis-Hash im Skript angepasst, Gate-Vorher neu gemessen, P2d-Ergebniswerte identisch. Branch **wege/dorfmap-p2d-v2** (neuer Name statt Force-Push; der Zwischenstand wege/dorfmap-p2d @4804c27 auf b3698e0 ist überholt).

## Ursache rampe_5 / „milchiges Band“ [S]
- In den Daten gibt es keine Reste der entfernten Rampe: WEGA = 0, WV = Land, relief_neu = relief_daten (VC/GB/WV/WEGA), die index.html-Payload enthält nur D1/D2/G1.
- Ursache ist runde_o16.entfernen (alte rampe_9 und Grat bei 133|173). Dort wurden GB **und** VC harmonisch gefüllt. Das Ergebnis ist eine glatte Fläche ohne Fleckung und ohne Mikrorelief.
  - Farbdetail: 1,58 im Band gegenüber 3,77 im Ring.
  - Reliefdetail: 0,023 m im Band gegenüber 0,048 m im Ring.
  - Der Ton ist dagegen gleich: L 208 gegenüber 210.
- Das Band wirkt also „milchig“, weil die Textur fehlt, nicht wegen einer falschen Farbe.

## Stellen
| Stelle | Maßnahme | Ergebnis |
|---|---|---|
| S7 rampe_5 (D4/D5, Maske 1912 Knoten) | Spender-Fleckung (Versätze −26/−18/+14 Zellen) als Poisson-Einpassung, Rand 3 Knoten weich. Dazu Hochpass-Mikrorelief des Spender-GB, höchstens ±0,08 m, nur bei Steigung < 0,12, mindestens 4 Zellen Abstand zu rampe_5, 2 Zellen zu Wegen, 6 zu Wasser | Farbdetail 1,58 → 4,03 (Ring 3,77); Ton L 208 → 212,9 (Ring 209,5); Reliefdetail 0,0233 → 0,0236 m, real ±0,035 m. In N05 ist die Fleckung deutlich besser, in N04 nur mäßig. |
| S10 Brücke E2 Ost | Hakenzellen (197.5\|72.5/73.5) entfernt; Landrampe x0 198, 5 Zellen lang, auf Decköberkante 0,33 m, seitlich weich, nur Land ≥ 2 Zellen vom Wasser | Keine Stufe und kein Haken mehr (E2_ostende, N02) |
| S10 Brücke E3 Ost | Streuzellen (186.5\|126.5, 185.5\|129.5) entfernt; Deck x174–187 einheitlich auf y 0,3; Landrampe x0 187 | Deck eben, Anschluss ohne Treppe (E3_ostende, N01) |
| (3) rampe_4 268\|242 | **ausgelassen** (optional, aus Zeitgründen) | unverändert |

## Sperrbereich (Art Umgebung / L3d + L3e)
- Alle von L3d und L3e geänderten Knoten (GB/WV/VC aus pruefung/l3d/l3d_rueck.npz und pruefung/l3e/l3e_rueck.npz) plus 2 Knoten Saum sind in relief_p2d.py gesperrt. Das Skript bricht ab, falls dort etwas geändert würde.
- Gemessene Überlappung mit L3d/L3e: GB 0, VC 0, WV 0. Keine Wasserzelle geändert (WV 0 Knoten, Abbruchprüfung im Skript).
- Bei E3 wurden nur Brückeneinträge und der Landanschluss geändert.

## Gate (je Regel, P2D_gate_vorher_nachher.json)
| Regel | vorher (1778473) | nachher |
|---|---|---|
| regeln | 368 | 368 (0 neu, 0 weg) |
| R8 Kreuzung | 31 | 31 |
| R9 Form | 325 | 325 |
| W1 index / alle 56 | 0 / 0 | 0 / 0 |
| Loch index / alle 56 | 0 / 0 | 0 / 0 |

- D2 ist bitgleich (GB/VC/WV/WEGA-Hashes).
- Vertex-Hash D1/G1/D2 index ↔ alle_kacheln: alle identisch (belege/hash_vergleich.md).
- Die Trefferkarte (--vorher 1778473) liegt unter trefferkarte/.

## Bau
- bau_endstand.sh hat einen neuen **Schritt 14 P2d** nach L3d (12) und L3e (13), die bereits eingetragen waren. P2D=0 lässt Schritt 14 weg.
- Nachweis: `sh bau_endstand.sh /tmp/p2d_endstand2` → **ENDBAU BITGLEICH (487 s)**, 31/31 Ausgaben gleich, einschließlich p2d_rueck.npz und p2d_bericht.json (belege/endstand_sha256_vergleich.txt).
- Die Pipeline lautet: relief_p2d.py → gen_textur.py vc → p2d_vc_lokal.py (VC auf ±16 Knoten um die P2d-Änderungen begrenzt, D2 ausgenommen) → html_payload_p3.py → waende_einsetzen.py. Danach wurde alle_kacheln/alles.sh ausgeführt.
- Rückweg: `python3 relief_p2d.py --aus`.

## Nahbilder (nahbilder/, oben vorher 1778473, unten nachher; links Farbe, rechts Ton)
N04_rampe5, N04_rampe5_nah, N05_rampe5, N01_E3, N02_E2, E2_ostende, E3_ostende, C4_124_157 (Kontrolle des früheren G6-Zwischentreffers).

## Ausnahmen und Risiken
- Die Basis wurde von 2771f70 auf 1778473 gewechselt, weil L3d und L3e während der Arbeit gemergt wurden. Die Gate-Basis ist deshalb 368 statt 372.
- S7: Das Mikrorelief ist wegen der G6-Facettenregel nur schwach. Ein Zwischenstand mit ±0,08 m auf Hängen erzeugte einen neuen G6-Treffer bei C4 124.9\|157.7, deshalb gilt jetzt die Steigungsgrenze 0,12. Im Tonbild bleibt die Fläche glatt; der Ausgleich geschieht über die Farbe/Fleckung. Das Band ist in N04 noch leicht erkennbar und sollte per QA-Sicht geprüft werden.
- Der Ton im Band ist etwas heller als im Ring (L 212,9 gegenüber 209,5).
- Die Landrampen heben das Gelände an den Ostenden um bis zu 0,33–0,36 m (sanft über 5 Zellen). Gegenüber Wasser und Ufer bleibt ein Saum von 2 Zellen.
- rampe_4 (3) ist nicht bearbeitet.

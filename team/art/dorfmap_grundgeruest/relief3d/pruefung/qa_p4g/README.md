# QA P4g – gezielte Nachsicht nach L3i (art/dorfmap-fertig @ 0a0b83a)

## 1. Gate (Prüfer/Schwellen unverändert)
`loch_o18g.js` (RAND=0.6) + `export_gate.sh` wie in qa_p4f; `w1_alle56_letzter_lauf.json` danach zurückgesetzt.

| Größe | Ist 0a0b83a | Soll (Grundgerüst) |
|---|---|---|
| regeln | 359, Ausnahmen 0 | 359 |
| R8 | 31 (21 Kreuzungen) | 31 |
| R9 | 321 | 321 |
| W1 / W1 alle 56 | 0 / 0 | 0 |
| Loch offen_innen | 0 | 0 |

„GATE ROT“, Exit 1 = erwartete Exportsperre. 363 → 359: genau die 4 G1-Krater-Treffer entfallen, keine neuen.

## 2. E3-Kanal und G1-Krater
Je Farbe + Ton aus 12, 22, 60 m, oben a6b00ba, unten 0a0b83a (`bilder_0a0b83a/vn/`).
- **E3** (190\|102): Tümpelkette behoben, durchgehendes Wasserband. Rest: am Kanalanfang ≈190\|97 kleiner Breitensprung mit dunkler Schulter, nur aus ≤12 m erkennbar → **leicht (Grenzfall)**, S1.
- **G1** (272,5\|10): Krater/Wasserfleck weg, in Farbe unsichtbar → **sauber**; schwacher Ring nur im Ton → Ausnahme A17.

## 3. Pixelvergleich 56 Übersichten gegen P4f
U + Q1–Q4, Farbe + Ton, je Kachel neu gerendert (`rendere_kacheln.js`) und gegen /tmp/p4f verglichen.
- bildgleich: 37 Kacheln
- nur Renderrauschen (≤ 0,001, kein Pixel > 25): C5, D2, F5
- echte Änderung: 16 Kacheln. E3, G1 sowie 14 Nachbarn: C3, C4, D3, D4, D5, E2, E4, E5, F3, F4 (E3/E4-Bach im Bild) und E1, F1, G2, H1 (G1-Krater im Bild). Alle 14 einzeln angesehen (`pixelvergleich/ausschnitte_vorher_jetzt.jpg`): jede Änderung ist der verbesserte Bach bzw. der verschwundene Krater, nichts Neues.

## 4. Ergebnis
**55 sauber / 1 leicht (E3, Grenzfall) / 0 stark** → `TABELLE.md`, `LISTE_SICHTBAR.md`
Ausnahmen: 17 (16 aus P4f weiter gültig, A12 mit Messwert, A16 gilt weiter, A17 neu) → `LISTE_AUSNAHMEN.md`

Dateien: `punkte_p4g.json`, `punkte_p4g_zusatz.json`, `punkte_a1_a3.json`, `messung_p4g.json`, Werkzeuge aus qa_p4f.

## Kosten
0 € extern, kein Codex, nur lokale Renderläufe auf der Box (21:57–22:12 MEZ, ≈¼ h).

# QA P4h – Mini-Nachsicht E3-Kanalanfang (Stand 42f05de, L3j #42)

Prüfer und Schwellen unverändert. Maßstab Fabian: „Wenn man es nicht sieht ist es mir egal. Aber hier geht es prinzipiell um Optik ist alles.“

## Gate (Soll 359 / 31 / 321, W1 0, Loch 0)
| Prüfung | Ist |
|---|---|
| regeln (Treffer) | 359 (Ausnahmen 0), Treffermenge identisch zu P4g (weg 0, neu 0) |
| R8 | 31 (21 Kreuzungen) |
| R9 | 321 |
| W1 | 0, alle 56 Kacheln 0 |
| Loch offen_innen | 0 |

Export-Sperre „GATE ROT“ (Exit 1) wie erwartet. Die vom Gate geschriebene `w1_alle56_letzter_lauf.json` wurde zurückgesetzt.

## E3 190|97
Vorher (0a0b83a) / jetzt (42f05de), Farbe und Ton, aus 8, 12, 22, 60 m und von Nord: `bilder_42f05de/vn/E3_trichter_*`. **Urteil: sauber** – Schulter/Breitensprung weg, keine neuen Artefakte. Messung 0,18 m / 29,6°, kein Gate-Treffer. Bestes Bild: `vn/E3_trichter_12.jpg` (Ausschnitt: `vn/E3_trichter_12_ausschnitt.jpg`).

## Pixelvergleich 56 gegen P4g
- 44 bildgleich.
- 12 mit Abweichung: E3 (L3j) sowie C3, C4, C5, D2, D3, D4, E2, E4, E5, F3, F4 (mittl. Δ ≤ 0,05; D2 ohne Pixel > 25). Alle einzeln angesehen (`pixelvergleich/montage_geaendert.jpg`, `kacheln/`): mit bloßem Auge gleich.

## Ergebnis
**56 sauber / 0 leicht / 0 stark.** Ausnahmeliste: 17 Einträge, unverändert übernommen (A1 neu gerendert, gleich).

Dateien: TABELLE.md, LISTE_SICHTBAR.md, LISTE_AUSNAHMEN.md, punkte_p4h.json, messung_p4h.json, Skripte (Kopien aus qa_p4g).

Kosten: 0 € extern, kein Codex; nur Grok-Laufzeit des QA-Subagenten (ab 22:45 MEZ).

# P10e – P10d auf P2-Stand (9ace686), Wandfarbe, Wandkörper wo Gelände die Klippe formt entfallen, W1 alle 56 im Gate

Auftrag Dorfmap-Grundgerüst (PR #14 nicht mergbar). Branch `devui/dorfmap-p10e` ab 9ace686, P10d-Branch unverändert.

## Konfliktauflösung
- Code aus P10d 3d59cd3 per `git checkout 3d59cd3 -- <datei>` übernommen: `neu/wand.py`, `pruefung/w1_wand.py`,
  `pruefung/export_gate.sh`, `pruefung/alle_kacheln/baue_alle_kacheln.py`, `pruefung/trefferkarte/trefferkarte.py`,
  `REGELN_VERPFLICHTEND.md`, `pruefung/p10d/`. P2 (d181fa6..9ace686) hat keine dieser Dateien und auch nicht
  `pruefung/p10c/` (Einsetz-Weg) geändert → kein inhaltlicher Konflikt. P2 änderte im Gate-Umfeld nur
  `pruefe_regeln.py` (Absturzschutz `_KP`), unverändert übernommen.
- Datendateien NICHT aus P10d: `neu/relief_neu.json.gz`, `index.html`, `neu/index.html` auf 9ace686-Stand mit
  `python3 pruefung/p10c/waende_einsetzen.py` neu gesetzt (Serialisierung bytegleich = True; nur `waende` + lod1,
  index.html außer der NEU_GZ-Zeile bytegleich, Bundle unverändert).
- Neu nötig: `baue_alle_kacheln.py` fällt jetzt auch bei `build_manifest`-Fehler „Erwartete D1-Kreuzung
  rampe_2/rampe_11 fehlt“ (seit P2, Rampen entnommen) auf das gespeicherte Manifest zurück (wie schon bei p3d17).
  Ohne das baut der 56-Kachel-Viewer auf 9ace686 gar nicht.

## Viewer (nur `pruefung/alle_kacheln/viewer_alle.js`, nicht der index.html-Bundle)
Wandkörper bekommen die Gelände-Vertexfarbe (VC, `tileColor`) an derselben Stelle und dasselbe Lambert-Material wie das
Gelände (`?wandvc=0` = alter Stand). index.html braucht keine Änderung: D1/G1/D2 haben keine Wandkörper mehr.
Beleg Gelände/Wege/Wasser unverändert: Nahbilder mit `--ohne waende` aus vorher-/nachher-HTML pixelgleich
(`ergebnis/render_ohne_waende_vergleich.txt`, 0 abweichende Pixel in allen 7 Bildern).

## Wandkörper entfallen, wo das Gelände die Klippe selbst formt (`neu/wand.py`, `SKIP_WHERE_TERRAIN_FORMS_CLIFF`)
Auch in Klippenfarbe blieben die Körper auf den Nahbildern als Fremdkörper erkennbar (Plattenkanten, Schattenlinien,
gestreifte Flächen; E6, H6 nah, Zwischenstand in `/workspace/p10e_nahbilder/zwischenstand_klippenfarbe/`). Jeder Lauf,
der nach P10d noch gebaut wurde, liegt per Bau auf einer Geländestufe ≥ 2 m quer über 2,4 m (≥ 40°) – dort formt das
Gelände die Klippe selbst. Diese 20 Läufe (B4, C3, C6, D4, D6, E6, F6, G6, H2, H3, H6) werden nicht gerendert, nichts
gelöscht; Liste `ergebnis/nicht_gerendert.json` (299 Einträge gesamt). Ergebnis: 0 Wandkörper auf allen 56 Kacheln.
Die Konstante auf `False` stellt den Zwischenstand (Klippenfarbe) her.

## Gate
`export_gate.sh` ruft zusätzlich W1 für alle 56 Kacheln auf (Paket in mktemp-Ordner, `--ohne-html`), Laufzeit ~18–25 s.
Ergebnisse und Zahlen: `ergebnis/gate_vergleich.md`.

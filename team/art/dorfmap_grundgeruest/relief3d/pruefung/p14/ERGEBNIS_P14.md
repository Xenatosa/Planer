# P14 – Kamera-Mindestabstand der Nutzersteuerung 25 m

Basis: art/dorfmap-fertig @ 80489c5. Kosten: 0 € zusätzlich, Codex: nein (Dev UI selbst), Laufzeit: 01:24–01:53 MEZ, bau_endstand 2 Läufe (Übernahme + leerer Ordner)

## Änderung
- `neu/viewer.js` (index.html, D1/G1/D2) und `pruefung/alle_kacheln/viewer_alle.js` (56 Kacheln): `controls.minDistance = 25` (vorher 2). Mit **`?nah=1`** gilt der alte Wert 2 m.
- Programmkameras sind nicht geklemmt. Das betrifft `setCamera` für Presets/focus und `__test.kam` für Prüf-/Nahbilder. `setCamera` setzt `minDistance` für sein `controls.update()` kurz auf 2 m (wie bisher) und danach wieder auf 25 m.
- Grund: `controls.update()` klemmt den Abstand auf `minDistance`. Ohne diese Ausnahme würden alle Nahbilder mit 8/15 m auf 25 m springen.
- Neuer Testhaken (nur lesend): `__test.abstand()` und `__test.minAbstand()`.
- **`main.js` unverändert.** Die Pipeline baut `main.js` fest aus 6e58af0 (`VIEWER_SHA`). Für index.html setzt der Relief-Neu-Viewer die Controls: `main.js` Zeile 19 ruft `renderNeuCore` aus `neu/viewer.js` auf und kehrt zurück. Das `oc.minDistance=3` in `main.js` Zeile 44 gehört zum Legacy-Pfad und ist für index.html nicht erreichbar. Eine Änderung dort hätte keine Wirkung und ginge am Pipeline-Mechanismus vorbei.
- Doku: `../ANFORDERUNGEN_3D_WELTKARTE.md` Z.39 und Z.73: Eintrag „Mindestabstand 25 m [A], Entscheidung Dorfmap-Grundgerüst vom 17.11.2026, Begründung Ausnahmen A18/A19, neu zu bewerten, sobald Gebäude auf der Karte stehen.“

## index.html / Soll (`soll_sha.json`)
- Erzeugt über `UEBERNEHMEN=1 sh bau_endstand.sh` (esbuild 0.24.2 / three 0.170.0). In diesem Lauf waren 45 Ausgaben gleich, nur index.html und neu/index.html abweichend.
- index.html und neu/index.html: `34b5a9e7499e3b1947d9e36dcd4a7dd140c18e7c811402b8e6f7deb700bbf5da` → **`fae60249d9156426c34c24fa4eaa3d4634f63ea67dae5df463d510626aadfb0f`**.
- bau_endstand.sh aus leerem Ordner: **ENDBAU BITGLEICH, 47/47** zum neuen Soll (758 s, `sha256_bau_p14.txt`).

## Skript-Befund (`skripte_bytegleich.json`)
Alle Prüf- und Bildskripte setzen die Kamera über `__test.kam`/`focus` → `setCamera` → `controls.update()`. Sie bleiben **unverändert**. Stichprobe als natives PNG gegen 80489c5, **13/13 bytegleich**:
- `qa_p4h/rendere_kacheln.js` (PUNKTE, Kritiker/QA): E3 8 m, B4-Grat 15 m, G7 15 m, auf dem P14-Build mit Testhaken wiederholt, ebenfalls gleich.
- `alle_kacheln/nahbild.js --liste` (P12c-Werkzeug): 8 m und 15 m.
- `p13/werkzeug/render_p13.js`: 56 Kacheln mit 8 m, 15 m und Q 30 m; index.html mit 8 m, 15 m, Q 30 m und Wandfuß 15 m.

## Nutzer-Zoom (`zoom_messung.json`, echte Mausrad-Events, Animationsschleife aktiv)

| Viewer | Start | nach 60 × hinein | nach 10 × hinaus | Programmkamera 8,6 m, dann 1 Mausradschritt |
|---|---|---|---|---|
| 56 Kacheln | 40,2 m | **25,0 m** | 194,5 m | → 25,0 m |
| index.html | 40,2 m | **25,0 m** | 194,5 m | → 25,0 m |
| `?nah=1` (beide) | 40,2 m | 2,0 m (alter Stand) | | 8,6 → 8,2 m |

Hinweis: Nach einer Programmkamera unter 25 m springt der erste Nutzer-Zoom auf 25 m.

## Bedingungen
- Gate 359/31/321, W1 0/0, Lochscan auf neuem index.html ok, Loch 0 (`gate_lauf.json`).
- D2 56 Kacheln: Positionen ebeb46a1/6835acf2/b33d5a64, Nahtnormalen 52eb1840, gleich 80489c5. index.html D1/G1/D2: Positionen und Indizes gleich (`d2_hashes.json`).
- Reliefdaten unverändert, keine Konsolenfehler.
- Schalter `?silh=0`, `?wfeld=0` und `?wrand=0` wirken (`schalter.json`).

# QA P4b: Ablauf (dc8c174)

Alle Befehle laufen im Ordner `relief3d`.

1. Viewer bauen:
   ```
   python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/p4b
   ```
2. Kachelbilder rendern, je Kachel U plus Q1–Q4:
   ```
   NODE_PATH=<playwright node_modules> HTML=/tmp/p4b/alle_kacheln.html DIR=/tmp/p4b/roh node pruefung/qa_p4b/rendere_kacheln.js
   ```
3. Komposite bauen:
   ```
   python3 pruefung/qa_p4b/komposit.py /tmp/p4b/roh /tmp/p4b/komp
   ```
4. Nahbilder rendern, einmal in Farbe und einmal in Clay:
   ```
   PUNKTE=pruefung/qa_p4b/punkte.json ... DIR=/tmp/p4b/detail/farbe
   ```
   und dasselbe mit `CLAY=1 ... DIR=/tmp/p4b/detail/clay`. Danach die Paarbilder bauen:
   ```
   python3 pruefung/qa_p4b/paar.py <punkte.json>
   ```
   - Die Punktdateien sind `punkte.json`, `punkte2.json` und `punkte3.json`.
   - Felder je Punkt: `n`, `x`, `z`, `d`, `el`, `az`.
   - `paar.py` liest aus `/tmp/p4b/detail` und schreibt nach `/tmp/p4b/paar`.
5. Messwerte berechnen:
   ```
   python3 pruefung/qa_p4b/messung.py pruefung/qa_p4b/liste_punkte.json
   ```
   Das Ergebnis ist `messung_liste.json`.

Alle Renders laufen ohne Schatten (`nosh=1`), damit keine Schattenakne entsteht.

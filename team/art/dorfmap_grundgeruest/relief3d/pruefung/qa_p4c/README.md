# QA P4c: Ablauf (8cd6d37)

Alle Befehle laufen im Ordner `relief3d`. Gerendert wird ohne Schatten (`nosh=1`), mit Wegen und Wasser.

1. Viewer bauen:
   ```
   python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/p4c
   ```
2. Kachelbilder (U + Q1–Q4) rendern und Komposite bauen:
   ```
   NODE_PATH=<playwright node_modules> HTML=/tmp/p4c/alle_kacheln.html DIR=/tmp/p4c/roh node pruefung/qa_p4c/rendere_kacheln.js
   python3 pruefung/qa_p4c/komposit.py /tmp/p4c/roh /tmp/p4c/komp
   ```
3. Nahbilder rendern, in Farbe und mit `CLAY=1`:
   ```
   PUNKTE=<datei> HTML=/tmp/p4c/alle_kacheln.html DIR=/tmp/p4c/detail/farbe node pruefung/qa_p4c/rendere_kacheln.js
   CLAY=1 PUNKTE=<datei> HTML=/tmp/p4c/alle_kacheln.html DIR=/tmp/p4c/detail/clay node pruefung/qa_p4c/rendere_kacheln.js
   WURZEL=/tmp/p4c STAND=8cd6d37 python3 pruefung/qa_p4c/paar.py <datei>
   ```
   Die Punktdateien sind:
   - `punkte.json`, `punkte2.json`, `punkte3.json`: die P4b-Kameras
   - `punkte_p4c.json`: 40 L3-Treffer, Rand C4/D4 und die P2-Kandidaten
   - `punkte_neben.json`: Wege und Wasser
4. Vorher/Nachher-Bilder (P4b-Paar oben, P4c-Paar unten):
   ```
   python3 pruefung/qa_p4c/vergleich.py /tmp/p4b/paar /tmp/p4c/paar /tmp/p4c/vn <namen…>
   ```
5. Messwerte:
   ```
   python3 pruefung/qa_p4c/messung.py pruefung/qa_p4c/liste_punkte.json > pruefung/qa_p4c/messung_23_nachher.json
   ```
   Für `messung_p4c.json` dasselbe mit `punkte_p4c.json` + `punkte_neben.json`.

`gate_treffer_je_kachel.txt` ist ein Auszug aus `pruefung/regeln_letzter_lauf.json` (378 Treffer).

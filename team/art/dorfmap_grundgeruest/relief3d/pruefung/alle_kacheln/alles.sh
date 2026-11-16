#!/bin/sh
# P10/P10b komplett: Build -> Hash-Vergleich D1/G1/D2 -> Lochscan 56 Kacheln (+ Positivkontrolle C3) -> Nahbilder -> Uebersicht.
# Nutzung: sh pruefung/alle_kacheln/alles.sh [AUSGABE=/tmp/p10]   (ERGEBNIS=<ordner> kopiert die Berichte dorthin)
set -e
cd "$(dirname "$0")/../.." || exit 2
OUT=${1:-${P10_OUT:-/tmp/p10}}
case "$OUT" in /tmp/w3*) echo "Ausgabe nach /tmp/w3 gesperrt"; exit 2;; esac
mkdir -p "$OUT"
export NODE_PATH=${NODE_PATH:-${NODE_DIR:-/tmp/w3}/node_modules}
S=pruefung/alle_kacheln
z() { date +%s; }
t=$(z); python3 $S/baue_alle_kacheln.py --out "$OUT"; echo "ZEIT build $(( $(z)-t )) s"
t=$(z); REF=index.html NEU="$OUT/alle_kacheln.html" OUT="$OUT/hash_vergleich.json" node $S/hash_vergleich.js; echo "ZEIT hash $(( $(z)-t )) s"
python3 $S/hash_bericht.py "$OUT/hash_vergleich.json" "$OUT/alle_kacheln_build.json" "$OUT/hash_vergleich.md"
t=$(z); KONTROLLE=${KONTROLLE-C3} sh $S/lochscan_alle.sh "$OUT"; echo "ZEIT lochscan $(( $(z)-t )) s"
t=$(z); HTML="$OUT/alle_kacheln.html" DIR="$OUT/nahbilder" node $S/nahbild_alle.js; echo "ZEIT nahbilder $(( $(z)-t )) s"
python3 $S/darstellung_bericht.py "$OUT/nahbilder/darstellung.json" "$OUT/alle_kacheln_build.json" "$OUT/darstellung.md"
python3 $S/uebersicht.py "$OUT/nahbilder" "$OUT/nahbilder_uebersicht.png" 240 "$OUT/lochscan_alle.json"
# P10b: zweiter Satz ohne Wandkoerper (Wandlagen siehe wand_herkunft.json), Wasser-Satz F7/G7/H7 (mit/ohne Wasser, ohne Waende)
t=$(z); HTML="$OUT/alle_kacheln.html" DIR="$OUT/nahbilder_ohne_waende" KARTE=0 Q='&ohne=waende' node $S/nahbild_alle.js; echo "ZEIT nahbilder_ohne_waende $(( $(z)-t )) s"
python3 $S/uebersicht.py "$OUT/nahbilder_ohne_waende" "$OUT/nahbilder_ohne_waende_uebersicht.png" 240 "$OUT/lochscan_alle.json"
python3 - "$S/wasser_F7_G7_H7_liste.json" "$OUT/liste_ohne_wasser.json" <<'PY'
import json, sys
L = json.load(open(sys.argv[1]))
for o in L:
    o['out'] = o['out'].replace('mit_wasser', 'ohne_wasser'); o['titel'] = o['titel'].replace('mit wasser', 'ohne wasser')
json.dump(L, open(sys.argv[2], 'w'))
PY
t=$(z); node $S/nahbild.js --html "$OUT/alle_kacheln.html" --liste $S/wasser_F7_G7_H7_liste.json --dir "$OUT/wasser_F7_G7_H7" --ohne waende > "$OUT/wasser_mit.json"
node $S/nahbild.js --html "$OUT/alle_kacheln.html" --liste "$OUT/liste_ohne_wasser.json" --dir "$OUT/wasser_F7_G7_H7" --ohne wasser,waende > "$OUT/wasser_ohne.json"; echo "ZEIT wasserbilder $(( $(z)-t )) s"
python3 $S/naht_pruefung.py "$OUT/alle_kacheln.json.gz" > "$OUT/naht_vertex.json"
python3 $S/wand_herkunft.py > "$OUT/wand_herkunft.json"
if [ -n "$ERGEBNIS" ]; then
  mkdir -p "$ERGEBNIS"
  cp "$OUT"/alle_kacheln_build.json "$OUT"/hash_vergleich.json "$OUT"/hash_vergleich.md "$OUT"/lochscan_alle.json "$OUT"/lochscan_alle.md "$ERGEBNIS"/
  if [ -f "$OUT/lochscan_kontrolle_C3.json" ]; then cp "$OUT"/lochscan_kontrolle_C3.json "$OUT"/lochscan_kontrolle_C3.md "$ERGEBNIS"/; fi
  cp "$OUT/naht_vertex.json" "$OUT/wand_herkunft.json" "$ERGEBNIS"/
  cp "$OUT/nahbilder/nahbilder.json" "$OUT/nahbilder/darstellung.json" "$OUT/darstellung.md" "$OUT/nahbilder/karte.png" "$ERGEBNIS"/
  python3 $S/uebersicht.py "$OUT/nahbilder" "$ERGEBNIS/nahbilder_uebersicht_240.png" 240 "$OUT/lochscan_alle.json"
fi
echo "fertig: $OUT"

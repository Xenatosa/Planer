#!/bin/sh
# P10 komplett: Build -> Hash-Vergleich D1/G1/D2 -> Lochscan 56 Kacheln (+ Positivkontrolle C3) -> Nahbilder -> Uebersicht.
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
python3 $S/uebersicht.py "$OUT/nahbilder" "$OUT/nahbilder_uebersicht.png" 320 "$OUT/lochscan_alle.json"
if [ -n "$ERGEBNIS" ]; then
  mkdir -p "$ERGEBNIS"
  cp "$OUT"/alle_kacheln_build.json "$OUT"/hash_vergleich.json "$OUT"/hash_vergleich.md "$OUT"/lochscan_alle.json "$OUT"/lochscan_alle.md "$ERGEBNIS"/
  if [ -f "$OUT/lochscan_kontrolle_C3.json" ]; then cp "$OUT"/lochscan_kontrolle_C3.json "$OUT"/lochscan_kontrolle_C3.md "$ERGEBNIS"/; fi
  cp "$OUT/nahbilder/nahbilder.json" "$OUT/nahbilder/karte.png" "$ERGEBNIS"/
  python3 $S/uebersicht.py "$OUT/nahbilder" "$ERGEBNIS/nahbilder_uebersicht_240.png" 240 "$OUT/lochscan_alle.json"
fi
echo "fertig: $OUT"

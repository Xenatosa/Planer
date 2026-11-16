#!/bin/sh
# P10: Lochscan (R5_loch) ueber alle 56 Kacheln. Ruft pruefung/loch_o18g.js UNVERAENDERT mit
# eigenem HTML/OUT auf (nicht /tmp/gate_loch.json) und wertet je Kachel aus.
# Nutzung (aus beliebigem Ordner): sh pruefung/alle_kacheln/lochscan_alle.sh [AUSGABE=/tmp/p10]
#   KONTROLLE=C3  -> zusaetzlich Positivkontrolle mit 1 entferntem Dreieck in C3
set -e
cd "$(dirname "$0")/../.." || exit 2
OUT=${1:-${P10_OUT:-/tmp/p10}}
case "$OUT" in /tmp/w3*) echo "Ausgabe nach /tmp/w3 gesperrt"; exit 2;; esac
mkdir -p "$OUT"
export NODE_PATH=${NODE_PATH:-${NODE_DIR:-/tmp/w3}/node_modules}
[ -f "$OUT/alle_kacheln.html" ] || python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out "$OUT"
BASIS="$(git rev-parse --short HEAD) $(git rev-parse --abbrev-ref HEAD)"
HTML="$OUT/alle_kacheln.html" OUT="$OUT/loch_alle_roh.json" RAND=0.6 node pruefung/loch_o18g.js
python3 pruefung/alle_kacheln/loch_auswertung.py "$OUT/loch_alle_roh.json" --out "$OUT/lochscan_alle.json" --md "$OUT/lochscan_alle.md" --basis "$BASIS"
if [ -n "$KONTROLLE" ]; then
  [ -f "$OUT/alle_kacheln_testloch_$KONTROLLE.html" ] || python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out "$OUT" --testloch "$KONTROLLE"
  HTML="$OUT/alle_kacheln_testloch_$KONTROLLE.html" OUT="$OUT/loch_kontrolle_roh.json" RAND=0.6 node pruefung/loch_o18g.js
  python3 pruefung/alle_kacheln/loch_auswertung.py "$OUT/loch_kontrolle_roh.json" --out "$OUT/lochscan_kontrolle_$KONTROLLE.json" --md "$OUT/lochscan_kontrolle_$KONTROLLE.md" --basis "$BASIS (Positivkontrolle, 1 Dreieck in $KONTROLLE entfernt)" --titel "P10 Lochscan Positivkontrolle $KONTROLLE"
fi

#!/bin/sh
# Pflicht-Gate vor jedem Export/ZIP (REGELN_VERPFLICHTEND.md). Bricht ab, solange pruefe_regeln.py Treffer meldet.
# Nutzung: sh pruefung/export_gate.sh && <export/zip-Befehl>
cd "$(dirname "$0")/.." || exit 2
LOCH=${LOCHSCAN:-/tmp/gate_loch.json}
TAG=${LOCH##*/gate_loch_};TAG=${TAG%.json}
if [ "$TAG" != "$LOCH" ] && [ -n "$TAG" ]; then
    REGELN_OUT=${REGELN_OUT:-/tmp/regeln_${TAG}.json}
    R8_OUT=${R8_OUT:-/tmp/r8_${TAG}.json}
    R9_OUT=${R9_OUT:-/tmp/r9_${TAG}.json}
else
    REGELN_OUT=${REGELN_OUT:-pruefung/regeln_letzter_lauf.json}
    R8_OUT=${R8_OUT:-pruefung/r8_letzter_lauf.json}
    R9_OUT=${R9_OUT:-pruefung/r9_letzter_lauf.json}
fi
[ -f "$LOCH" ] || HTML=index.html OUT="$LOCH" RAND=0.6 NODE_PATH=${NODE_PATH:-/tmp/w3/node_modules} node pruefung/loch_o18g.js >/dev/null 2>&1
ROT=0
LOCHSCAN="$LOCH" python3 pruefung/pruefe_regeln.py relief_daten.json.gz "$REGELN_OUT" || ROT=1
python3 pruefung/r8_kreuzung.py relief_daten.json.gz "$R8_OUT" || ROT=1   # t120u-t122u R8/R8a kartenweit
python3 pruefung/r9_form.py relief_daten.json.gz "$R9_OUT" || ROT=1       # t122u/t123u R8b Delle, R9 Saegezahn, R9w Wellen
[ $ROT = 0 ] || { echo "GATE ROT: kein Export/ZIP"; exit 1; }
echo "GATE GRUEN"

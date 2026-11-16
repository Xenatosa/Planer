#!/bin/sh
# Pflicht-Gate vor jedem Export/ZIP (REGELN_VERPFLICHTEND.md). Bricht ab, solange pruefe_regeln.py Treffer meldet.
# Nutzung: sh pruefung/export_gate.sh && <export/zip-Befehl>
# P11b: Lochscan-JSON nicht mehr fest /tmp/gate_loch.json, sondern eigener Temp-Ordner (mktemp, per trap
# aufgeraeumt). GATE_LOCH_JSON=<datei> (oder LOCHSCAN=<datei>, GATE_LOCH_JSON hat Vorrang): vorhandene Datei wird
# genutzt, fehlende dort erzeugt (bleibt liegen). Uebergabe an pruefe_regeln.py wie bisher per LOCHSCAN.
# Pruefer und Schwellen unveraendert. Test: sh pruefung/test_export_gate_lochscan.sh
cd "$(dirname "$0")/.." || exit 2
GATE_TMP=$(mktemp -d "${TMPDIR:-/tmp}/export_gate.XXXXXX") || exit 2
trap 'rm -rf "$GATE_TMP"' EXIT
trap 'exit 2' HUP INT TERM
GATE_LOCH_JSON=${GATE_LOCH_JSON:-${LOCHSCAN:-$GATE_TMP/gate_loch.json}}
[ -f "$GATE_LOCH_JSON" ] || HTML=index.html OUT="$GATE_LOCH_JSON" RAND=0.6 node pruefung/loch_o18g.js >/dev/null 2>&1
ROT=0
LOCHSCAN="$GATE_LOCH_JSON" python3 pruefung/pruefe_regeln.py relief_daten.json.gz pruefung/regeln_letzter_lauf.json || ROT=1
python3 pruefung/r8_kreuzung.py relief_daten.json.gz pruefung/r8_letzter_lauf.json || ROT=1   # t120u-t122u R8/R8a kartenweit
python3 pruefung/r9_form.py relief_daten.json.gz pruefung/r9_letzter_lauf.json || ROT=1       # t122u/t123u R8b Delle, R9 Saegezahn, R9w Wellen
python3 pruefung/w1_wand.py index.html pruefung/w1_letzter_lauf.json || ROT=1                # P10d W1 Wandkoerper am Gelaende
W1T="$GATE_TMP/w1_alle56" && python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out "$W1T" --ohne-html >/dev/null && python3 pruefung/w1_wand.py "$W1T/alle_kacheln.json.gz" pruefung/w1_alle56_letzter_lauf.json || ROT=1; rm -rf "$W1T"   # P10e W1 alle 56 Kacheln (~25 s)
[ $ROT = 0 ] || { echo "GATE ROT: kein Export/ZIP"; exit 1; }
echo "GATE GRUEN"

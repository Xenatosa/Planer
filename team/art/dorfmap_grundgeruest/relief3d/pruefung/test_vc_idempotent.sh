#!/bin/sh
# P11b: gen_textur.py vc muss idempotent sein. Zwei Laeufe nacheinander auf einer Kopie des Repo-Stands
# (relief_daten.json.gz + neu/relief_neu.json.gz) duerfen nichts aendern (Repo-Stand = Fixpunkt).
cd "$(dirname "$0")/.." || exit 2
T=$(mktemp -d "${TMPDIR:-/tmp}/vc_idem.XXXXXX") || exit 2; trap 'rm -rf "$T"' EXIT
cp relief_daten.json.gz "$T/rd.json.gz"; cp neu/relief_neu.json.gz "$T/rn.json.gz"
s0=$(cat "$T/rd.json.gz" "$T/rn.json.gz" | sha256sum)
python3 gen_textur.py vc "$T/rd.json.gz" "$T/rn.json.gz" > "$T/l1.log" || exit 1
s1=$(cat "$T/rd.json.gz" "$T/rn.json.gz" | sha256sum)
python3 gen_textur.py vc "$T/rd.json.gz" "$T/rn.json.gz" > "$T/l2.log" || exit 1
s2=$(cat "$T/rd.json.gz" "$T/rn.json.gz" | sha256sum)
echo "repo  ${s0%% *}"; echo "lauf1 ${s1%% *}"; echo "lauf2 ${s2%% *}"
[ "$s0" = "$s1" ] && [ "$s1" = "$s2" ] && { echo "VC IDEMPOTENT: OK"; exit 0; }
echo "VC NICHT IDEMPOTENT"; exit 1

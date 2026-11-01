#!/bin/sh
# Alle 11 Kameras in 3 parallelen Teil-Laeufen (frischer Browser je Teil, kein Timeout am Ende). Aufruf: SUF=r5 OUT=/tmp/r5 sh rendere_alle.sh
export NODE_PATH=${NODE_PATH:-/tmp/w3/node_modules} KURZ=1 MODI=neu HTML=${HTML:-index.html}
mkdir -p "$OUT"
VIEWS=schraeg,nordwand,krater,suedwand node test_relief.js > "$OUT/log1.txt" 2>&1 &
VIEWS=oben,unten,rand,rueck node test_relief.js > "$OUT/log2.txt" 2>&1 &
VIEWS=dorf,sued,fluss_ost node test_relief.js > "$OUT/log3.txt" 2>&1 &
wait

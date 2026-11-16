#!/bin/sh
# P11: Ein-Befehl-Endbau. Erzeugt aus den Quelldaten in einem LEEREN Ausgabeordner alle Ausgaben des
# Endstands (art/dorfmap-fertig, c6a3db0) und vergleicht sie per sha256 mit dem Repo-Stand.
#
#   sh bau_endstand.sh [AUSGABE]          (Standard /tmp/relief3d_endstand; muss leer sein oder fehlen)
#   UEBERNEHMEN=1 sh bau_endstand.sh ...  kopiert die gebauten Ausgaben danach ins Repo (sonst nur Vergleich)
#
# Schritte (genau die Erzeugung aus ERGEBNIS_P2_V2.md + P10e, in einer Arbeitskopie unter AUSGABE):
#   1 python3 gen_relief.py                                   Relief (relief_daten.json.gz, zellen_relief.csv, ...)
#   2 RELIEF_NEU=1 RELIEF_GELAENDE_VAR=0 python3 gen_relief.py vektor.json, felder, neu/zellen_relief.csv,
#                                                             build.json, neu/relief_neu.json.gz (neu/pipeline.py)
#   2a python3 gen_textur.py vc                               (Stand P11/dc257c9, Basis fuer L3)
#   2b L3 (8cd6d37) wie entstanden: relief_l3.py in drei Runden (232f113, 3e68969, aktueller Stand), je Runde
#      --aus der Vorrunde, anwenden, gen_textur.py vc. Grund: gen_textur.py vc ist nicht idempotent (VC/FW.c
#      werden aus dem vorhandenen VC weichgezeichnet), daher haengen VC/FW.c von jeder vc-Runde der
#      L3-Entwicklung ab; GB/Objekte/D1 haengen nur von der letzten Runde ab. Die beiden alten relief_l3.py
#      und die damalige l3_stellen.json (in 232f113 und 3e68969 gleich, 253b914 aenderte Stellen 12/14/23) kommen per
#      git show (sha256 geprueft).
#   3 python3 gen_textur.py vc                                P3 T1/FW.c in relief_daten + relief_neu
#   4 RELIEF_NEU=1 python3 baue_html.py                       index.html + neu/index.html (Bundle + Daten)
#   5 python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py   NEU_GZ-Zeile (hier ohne Wirkung, Kontrolle)
#   6 python3 pruefung/p10c/waende_einsetzen.py               Wandkoerper (P10e: 0) in relief_neu + index.html
#
# Gelaendevariante: RELIEF_GELAENDE_VAR=0 ist die Variante des Endstands (P2 9ace686, manifest terrain_variant "0").
#
# Bundle (esbuild-Drift, P11 geklaert): Das Bundle in index.html ist seit 6e58af0 (p3d5) unveraendert und wurde mit
# esbuild 0.19.12..0.24.2 aus main.js@6e58af0 gebaut. /tmp/w3 (= /workspace/.p3_node) hat esbuild 0.28.2; ab 0.25 aendert
# der Minifier Konstantenfaltung/Inlining und damit Bytes und Bezeichner. Gepinnt: esbuild 0.24.2 + three 0.170.0
# (bau/package.json + bau/package-lock.json, npm ci). Viewer-Quelle: main.js@6e58af0 (sha256 unten). Die einzige spaetere
# main.js-Aenderung (b90b0a6, P3 QA-C3 Feinband/Bump) liegt im Legacy-Pfad hinter dem RELIEF_NEU_VIEWER-Return (main.js
# Zeile 19) und ist im Relief-Neu-Viewer nicht erreichbar. VIEWER_MAIN=arbeitsbaum baut stattdessen das aktuelle main.js
# (Bundle dann absichtlich NICHT bitgleich).
set -eu
R=$(cd "$(dirname "$0")" && pwd)
AUS=${1:-/tmp/relief3d_endstand}
case "$AUS" in /tmp/w3|/tmp/w3/*) echo "Ausgabe nach /tmp/w3 gesperrt"; exit 2;; esac
if [ -e "$AUS" ] && [ -n "$(ls -A "$AUS" 2>/dev/null)" ]; then echo "Ausgabeordner $AUS ist nicht leer"; exit 2; fi
mkdir -p "$AUS"; AUS=$(cd "$AUS" && pwd)
VIEWER_REV=6e58af0
VIEWER_SHA=3a942b26be0fcc0e81e781e05fd6b81b2316d7b63c5a518bfa4834a2973d59f4
NODE_BAU=${NODE_BAU:-/tmp/relief3d_bau_node}
T0=$(date +%s)
z() { echo "ZEIT $1 $(( $(date +%s) - $2 )) s"; }

# 0) gepinnte Werkzeuge (nur eigener Ordner; /tmp/w3 wird nicht benutzt)
if [ "$("$NODE_BAU/node_modules/.bin/esbuild" --version 2>/dev/null)" != "0.24.2" ] || \
   ! grep -q '"version": "0.170.0"' "$NODE_BAU/node_modules/three/package.json" 2>/dev/null; then
  mkdir -p "$NODE_BAU"; cp "$R/bau/package.json" "$R/bau/package-lock.json" "$NODE_BAU/"
  (cd "$NODE_BAU" && npm ci --no-audit --no-fund --silent)
fi
echo "esbuild $("$NODE_BAU/node_modules/.bin/esbuild" --version), three $(python3 -c "import json;print(json.load(open('$NODE_BAU/node_modules/three/package.json'))['version'])")"

# Ausgaben (werden NICHT in die Arbeitskopie kopiert, muessen also neu entstehen)
AUSGABEN="relief_daten.json.gz zellen_relief.csv relief_zaehlung.json pruefung/platzierung_t59u.json pruefung/o18/aenderungen_o18.json
pruefung/runde_m_aenderungen_t65u.json neu/vektor.json neu/felder.json neu/felder.npz neu/zellen_relief.csv neu/debug_D1.png
neu/debug_D2.png neu/debug_G1.png dorfmap_relief_z25.glb pruefung/l3_rueck.npz pruefung/l3_bericht.json neu/build.json neu/relief_neu.json.gz index.html neu/index.html"

# 1) Arbeitskopie: versionierte Quelldateien (ohne Pruefbilder/-seiten, pruefung/ nur .json/.py, ohne Ausgaben); _alt nur lesend verlinkt
W="$AUS/dorfmap_grundgeruest"; mkdir -p "$W/relief3d"
mkdir -p "$W/pruefung"   # Eingaben aus dem Elternordner (gen_relief.py B='../', neu/vektor.py ROOT.parent)
cp "$R/../raster_c20_z25_zellen.csv" "$R/../raster_c20_z25_overlay_plaetze_wege.csv" "$W/"
cp "$R/../pruefung/quelle_plaetze_wachstum_ausbau_planm.json" "$W/pruefung/"
ln -s "$R/../_alt" "$W/_alt"
(cd "$R" && git ls-files . ) | grep -v -E '^(pruefung/|_alt/|test/|referenz/|dorfmap_relief_z25\.glb$)' > "$AUS/.liste"
(cd "$R" && git ls-files pruefung) | grep -E '\.(json|py)$|^pruefung/p3_nahbilder/werkzeug/' >> "$AUS/.liste"
for f in $AUSGABEN; do grep -vxF "$f" "$AUS/.liste" > "$AUS/.liste2" || true; mv "$AUS/.liste2" "$AUS/.liste"; done
(cd "$R" && tar -cf - -T "$AUS/.liste") | (cd "$W/relief3d" && tar -xf -)
mkdir -p "$W/relief3d/pruefung/o18"
B="$W/relief3d"
for f in $AUSGABEN; do [ ! -e "$B/$f" ] || { echo "Ausgabe $f schon in der Arbeitskopie"; exit 2; }; done
if [ "${VIEWER_MAIN:-stand}" = stand ]; then
  (cd "$R" && git show "$VIEWER_REV:./main.js") > "$B/main.js"
  echo "$VIEWER_SHA  $B/main.js" | sha256sum -c --quiet
fi
touch "$AUS/.start"; sleep 1
cd "$B"
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
t=$(date +%s); python3 gen_relief.py > "$AUS/1_gen_relief.log" 2>&1; z gen_relief $t
t=$(date +%s); RELIEF_NEU=1 RELIEF_GELAENDE_VAR=0 python3 gen_relief.py > "$AUS/2_gen_relief_neu.log" 2>&1; z gen_relief_neu $t
t=$(date +%s); python3 gen_textur.py vc > "$AUS/2a_gen_textur_vc.log" 2>&1; z gen_textur_vc_p11 $t
t=$(date +%s); VOR=""
for RUNDE in 232f113:8f0c96074a243934134e2f611096ec895a96d65f4e1c1d0713bb58361f21567d 3e68969:b3fbf5eaeb539ab589c502667c8d968d409a13a9aa6cfb1bbe90ff60bf307086; do
  REV=${RUNDE%%:*}; H="$AUS/l3_runde_$REV"; mkdir -p "$H/pruefung"
  (cd "$R" && git show "$REV:./relief_l3.py") > "$H/relief_l3.py"; echo "${RUNDE#*:}  $H/relief_l3.py" | sha256sum -c --quiet
  (cd "$R" && git show "$REV:./pruefung/l3_stellen.json") > "$H/pruefung/l3_stellen.json"
  echo "2f0fe77f355f77c8d549b2c1d1cc47fc522da1d651f991394ff0ed76510eaa5b  $H/pruefung/l3_stellen.json" | sha256sum -c --quiet
  ln -s "$B/neu" "$H/neu"; ln -s "$B/relief_daten.json.gz" "$H/relief_daten.json.gz"
  if [ -n "$VOR" ]; then mv "$VOR/pruefung/l3_rueck.npz" "$H/pruefung/"; python3 "$H/relief_l3.py" --aus >> "$AUS/2b_relief_l3.log" 2>&1; fi
  python3 "$H/relief_l3.py" >> "$AUS/2b_relief_l3.log" 2>&1
  python3 gen_textur.py vc >> "$AUS/2b_relief_l3.log" 2>&1; VOR=$H
done
mv "$VOR/pruefung/l3_rueck.npz" pruefung/; python3 relief_l3.py --aus >> "$AUS/2b_relief_l3.log" 2>&1
python3 relief_l3.py >> "$AUS/2b_relief_l3.log" 2>&1; z relief_l3_runden $t
t=$(date +%s); python3 gen_textur.py vc > "$AUS/3_gen_textur_vc.log" 2>&1; z gen_textur_vc $t
t=$(date +%s); NODE_DIR="$NODE_BAU" RELIEF_NEU=1 python3 baue_html.py > "$AUS/4_baue_html.log" 2>&1; z baue_html $t
t=$(date +%s); python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py > "$AUS/5_html_payload_p3.log" 2>&1; z html_payload_p3 $t
t=$(date +%s); python3 pruefung/p10c/waende_einsetzen.py > "$AUS/6_waende_einsetzen.log" 2>&1; z waende_einsetzen $t
z gesamt_bau $T0

# 2) Kontrolle: keine unerwarteten geschriebenen Dateien, sha256 je Ausgabe gegen den Repo-Stand
find . -type f -newer "$AUS/.start" ! -name '*.pyc' | sed 's|^\./||' | sort > "$AUS/geschrieben.txt"
for f in $AUSGABEN; do echo "$f"; done | sort > "$AUS/.soll"
if ! diff -u "$AUS/.soll" "$AUS/geschrieben.txt" > "$AUS/geschrieben_diff.txt"; then echo "WARNUNG: geschriebene Dateien weichen ab (geschrieben_diff.txt)"; fi
ROT=0; : > "$AUS/sha256_vergleich.txt"
for f in $AUSGABEN; do
  a=$(sha256sum "$R/$f" | cut -c1-64); b=$(sha256sum "$B/$f" | cut -c1-64)
  [ "$a" = "$b" ] && s=gleich || { s=ABWEICHUNG; ROT=1; }
  printf '%s %s %s %s\n' "$s" "$a" "$b" "$f" | tee -a "$AUS/sha256_vergleich.txt"
done
if [ "${UEBERNEHMEN:-0}" = 1 ]; then for f in $AUSGABEN; do cp "$B/$f" "$R/$f"; done; echo "Ausgaben ins Repo uebernommen"; fi
[ $ROT = 0 ] && echo "ENDBAU BITGLEICH ($(( $(date +%s) - T0 )) s)" || { echo "ENDBAU ABWEICHEND"; exit 1; }

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
#   3 python3 gen_textur.py vc                                P3 T1/FW.c in relief_daten + relief_neu
#   4 RELIEF_NEU=1 python3 baue_html.py                       index.html + neu/index.html (Bundle + Daten)
#   5 python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py   NEU_GZ-Zeile (hier ohne Wirkung, Kontrolle)
#   6 python3 pruefung/p10c/waende_einsetzen.py               Wandkoerper (P10e: 0) in relief_neu + index.html
#
# Nachschritte seit P11 (NICHT in diesem Skript, Stand 16.11.2026): relief_l3.py (L3/L3b, art/dorfmap-fertig d5b17e2) und
# danach P2b/P2c (PR #21) auf relief_daten.json.gz + neu/relief_neu.json.gz, jeweils mit Basis-Hash-Pruefung:
#   7 python3 relief_p2b.py                                   GB-Stellen 03/03d/03m/14/23 (pruefung/p2_analyse/p2b/p2b_stellen.json)
#   8 python3 pruefung/p2_analyse/p2b/p2b_bruecken.py         Bruecke E2 (W2)
#   9 python3 gen_textur.py vc, dann pruefung/p2_analyse/p2b/p2b_vc_lokal.py <vorher-daten> <vorher-neu>  VC nur lokal
#  10 pruefung/p2_analyse/p2b/p2b_r5_textur.py, html_payload_p3.py, p10c/waende_einsetzen.py
# Da Schritt L3 hier fehlt, baut dieses Skript weiterhin den P11-Stand (c6a3db0); der Endbau-Vergleich gilt nur dafuer.
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
neu/debug_D2.png neu/debug_G1.png dorfmap_relief_z25.glb neu/build.json neu/relief_neu.json.gz index.html neu/index.html"

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

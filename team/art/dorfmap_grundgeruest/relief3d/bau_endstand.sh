#!/bin/sh
# P11: Ein-Befehl-Endbau. Erzeugt aus den Quelldaten in einem LEEREN Ausgabeordner alle Ausgaben des
# Endstands (art/dorfmap-L3d = L3 + L3b + P2b/P2c + L3c2 + L3d auf 2771f70, + L3e, ab P2d + Schritt 14) und vergleicht sie per sha256 mit dem Repo-Stand.
#
#   sh bau_endstand.sh [AUSGABE]          (Standard /tmp/relief3d_endstand; muss leer sein oder fehlen)
#   UEBERNEHMEN=1 sh bau_endstand.sh ...  kopiert die gebauten Ausgaben danach ins Repo (sonst nur Vergleich)
#
# Schritte (genau die Erzeugung aus ERGEBNIS_P2_V2.md + P10e, in einer Arbeitskopie unter AUSGABE):
#   1 python3 gen_relief.py                                   Relief (relief_daten.json.gz, zellen_relief.csv, ...)
#   2 RELIEF_NEU=1 RELIEF_GELAENDE_VAR=0 python3 gen_relief.py vektor.json, felder, neu/zellen_relief.csv,
#                                                             build.json, neu/relief_neu.json.gz (neu/pipeline.py)
#   2a python3 gen_textur.py vc                               (Stand P11/dc257c9, Basis fuer L3)
#   2b L3 (8cd6d37) wie entstanden: relief_l3.py in drei Runden (232f113, 3e68969, 8cd6d37), je Runde --aus der
#      Vorrunde und anwenden, nach den ersten beiden je gen_textur.py vc. Grund: gen_textur.py vc ist nicht idempotent
#      (VC/FW.c werden aus dem vorhandenen VC weichgezeichnet, Maske aus GB), daher haengen VC/FW.c von jeder vc-Runde
#      der L3/L3b-Entwicklung ab; GB/WV/FW.h/Objekte/Prototypen haengen nur von der letzten Runde ab. Alle historischen
#      relief_l3.py und l3_stellen.json kommen per git show (sha256 geprueft).
#   3 python3 gen_textur.py vc                                P3 T1/FW.c in relief_daten + relief_neu
#   4 RELIEF_NEU=1 python3 baue_html.py                       index.html + neu/index.html (Bundle + Daten)
#   5 python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py   NEU_GZ-Zeile (hier ohne Wirkung, Kontrolle)
#   6 python3 pruefung/p10c/waende_einsetzen.py               Wandkoerper (P10e: 0) in relief_neu + index.html
#     (bis hier = Endstand 8cd6d37)
#   7 L3b (d5b17e2) wie entstanden: Runde e7dadd6 (ohne vc), dann je Runde vc -> waende -> payload; Runden e193584,
#      9bb5d10, 1b8a477 (= d5b17e2). Aufruf relief_l3.py unveraendert (die L3b-Schalter wasser, fw_folgen,
#      rampe_m, weg_rand_m stehen je Stelle in l3_stellen.json). Jede Runde einzeln gegen ihren Commit nachgemessen.
#     (bis hier = Endstand d5b17e2; alle vc-Laeufe 2a-7 mit dem historischen gen_textur.py@d5b17e2, s. GT_ALT)
#   8 P2b/P2c (a6a4831) wie entstanden (pruefung/p2_analyse/p2c/p2b2_pipe.sh): Vorher-Stand sichern, relief_p2b.py,
#      p2b_bruecken.py, gen_textur.py vc (aktuell), p2b_vc_lokal.py <Vorher-Stand>, p2b_r5_textur.py,
#      html_payload_p3.py, waende_einsetzen.py. Nebenausgaben p2b_rueck.npz + p2b_bericht.json werden mitverglichen.
#  11 L3c2 (81b6f94): relief_l3.py --stufe-c, gen_textur.py vc, pruefung/l3c_vc_lokal.py <Vorher-Stand>, html_payload_p3.py,
#      waende_einsetzen.py. Nebenausgaben l3c_rueck.npz, l3c_bericht.json, l3c_vc_rueck.npz werden mitverglichen.
#  12 L3d (ERGEBNIS_L3d): relief_l3d.py (QA-P4d-Platten/Bucht/Kerbe H7, E3-Westufer Rinne/Farbe lokal, Basis-Hash GB/WV/VC = Stand nach 11, Rueckweg
#      relief_l3d.py --aus mit pruefung/l3d/l3d_rueck.npz), html_payload_p3.py, waende_einsetzen.py. Kein gen_textur-Lauf
#      (VC/FW.c schreibt relief_l3d.py selbst und nur in seiner Box). L3D=0 laesst Schritt 12 weg (Stand nach 11).
#  13 L3e (ERGEBNIS_L3e): relief_l3e.py (Ufer F7-Nord/G7-Nord/G7-Plaettchen: Wassermaske und Boeschung folgen der Hoehenlinie
#      Gelaende = Spiegel, Basis-Hash GB/WV/VC = Stand nach 12, Rueckweg relief_l3e.py --aus mit pruefung/l3e/l3e_rueck.npz),
#      html_payload_p3.py, waende_einsetzen.py. Kein gen_textur-Lauf, VC unveraendert. L3E=0 laesst Schritt 13 weg (Stand nach 12);
#      L3E folgt standardmaessig L3D (Schritt 13 setzt den Stand nach 12 voraus).
#  14 P2d (ERGEBNIS_P2D): relief_p2d.py (S7 rampe_5/O16-Band Farbe+Mikrorelief, S10 Bruecken E2/E3 Ostende; Basis-GB-Hash
#      = Stand nach 13, Sperrbereich L3d/L3e), gen_textur.py vc, p2d_vc_lokal.py <Vorher-Stand>, html_payload_p3.py, waende_einsetzen.py.
#      Nebenausgaben p2d_rueck.npz + p2d_bericht.json werden mitverglichen. Setzt Schritt 12+13 voraus (P2D=0 laesst 14 weg).
#  15 L3f (ERGEBNIS_L3f): relief_l3f.py (E3-Westufer + Nachtrag F7/G7; Basis-Hash = Stand nach 14, Rueckweg relief_l3f.py --aus mit pruefung/l3f/l3f_rueck.npz),
#      html_payload_p3.py, waende_einsetzen.py. Stand L3f: alle Versuche gescheitert, keine Stelle aktiv -> relief_l3f.py schreibt nichts,
#      keine Nebenausgaben, Ergebnis bitgleich zu Schritt 14. L3F=0 laesst Schritt 15 weg; L3F folgt standardmaessig P2D.
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
GT_ALT_SHA=0db3fe771f1870952353056c6c15cd90c50c7000284e79323cacca7dfcdd4089
VIEWER_SHA=3a942b26be0fcc0e81e781e05fd6b81b2316d7b63c5a518bfa4834a2973d59f4
NODE_BAU=${NODE_BAU:-/tmp/relief3d_bau_node}
T0=$(date +%s)
z() { echo "ZEIT $1 $(( $(date +%s) - $2 )) s"; }

# 0) gepinnte Werkzeuge (nur eigener Ordner; /tmp/w3 wird nicht benutzt). P12: playwright 1.65.1 fuer den Gate-Lochscan.
if [ "$("$NODE_BAU/node_modules/.bin/esbuild" --version 2>/dev/null)" != "0.24.2" ] || \
   ! grep -q '"version": "0.170.0"' "$NODE_BAU/node_modules/three/package.json" 2>/dev/null || \
   ! grep -q '"version": "1.65.1"' "$NODE_BAU/node_modules/playwright/package.json" 2>/dev/null; then
  mkdir -p "$NODE_BAU"; cp "$R/bau/package.json" "$R/bau/package-lock.json" "$NODE_BAU/"
  (cd "$NODE_BAU" && npm ci --no-audit --no-fund --silent)
fi
echo "esbuild $("$NODE_BAU/node_modules/.bin/esbuild" --version), three $(python3 -c "import json;print(json.load(open('$NODE_BAU/node_modules/three/package.json'))['version'])")"

# Ausgaben (werden NICHT in die Arbeitskopie kopiert, muessen also neu entstehen)
AUSGABEN="relief_daten.json.gz zellen_relief.csv relief_zaehlung.json pruefung/platzierung_t59u.json pruefung/o18/aenderungen_o18.json
pruefung/runde_m_aenderungen_t65u.json neu/vektor.json neu/felder.json neu/felder.npz neu/zellen_relief.csv neu/debug_D1.png
neu/debug_D2.png neu/debug_G1.png dorfmap_relief_z25.glb pruefung/l3_rueck.npz pruefung/l3_bericht.json neu/build.json neu/relief_neu.json.gz index.html neu/index.html
pruefung/p2_analyse/p2b/p2b_rueck.npz pruefung/p2_analyse/p2b/p2b_bericht.json
pruefung/l3c_rueck.npz pruefung/l3c_bericht.json pruefung/l3c_vc_rueck.npz"
[ "${L3D:-1}" = 0 ] || AUSGABEN="$AUSGABEN pruefung/l3d/l3d_rueck.npz pruefung/l3d/l3d_bericht.json"
L3E=${L3E:-${L3D:-1}}
if [ "$L3E" != 0 ] && [ "${L3D:-1}" = 0 ]; then echo "L3E braucht Schritt 12 (L3D=0 und L3E=1 geht nicht)"; exit 2; fi
[ "$L3E" = 0 ] || AUSGABEN="$AUSGABEN pruefung/l3e/l3e_rueck.npz pruefung/l3e/l3e_bericht.json"
P2D=${P2D:-$L3E}
if [ "$P2D" != 0 ] && [ "$L3E" = 0 ]; then echo "P2D braucht Schritt 13 (L3E=0 und P2D=1 geht nicht)"; exit 2; fi
[ "$P2D" = 0 ] || AUSGABEN="$AUSGABEN pruefung/p2_analyse/p2d/p2d_rueck.npz pruefung/p2_analyse/p2d/p2d_bericht.json"
L3F=${L3F:-$P2D}
if [ "$L3F" != 0 ] && [ "$P2D" = 0 ]; then echo "L3F braucht Schritt 14 (P2D=0 und L3F=1 geht nicht)"; exit 2; fi
# L3f: solange keine Stelle aktiv ist, entstehen keine Nebenausgaben (l3f_rueck.npz/l3f_bericht.json) -> nichts zu ergaenzen.

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
# Historisches gen_textur.py (a10fc1e..d5b17e2 unveraendert, sha256 geprueft) fuer alle vc-Laeufe bis L3b: genau damit
# ist der Stand entstanden. Das aktuelle gen_textur.py (P11b: vc_fleckrand_p3 bis Fixpunkt) weicht davon nur dort ab,
# wo die alte Fassung nach 200 Iterationen nicht konvergiert war (E4); es wird ab P2b (Schritt 8) benutzt.
GT_ALT="$AUS/gen_textur_d5b17e2.py"
(cd "$R" && git show "d5b17e2:./gen_textur.py") > "$GT_ALT"; echo "$GT_ALT_SHA  $GT_ALT" | sha256sum -c --quiet
t=$(date +%s); python3 gen_relief.py > "$AUS/1_gen_relief.log" 2>&1; z gen_relief $t
t=$(date +%s); RELIEF_NEU=1 RELIEF_GELAENDE_VAR=0 python3 gen_relief.py > "$AUS/2_gen_relief_neu.log" 2>&1; z gen_relief_neu $t
t=$(date +%s); python3 "$GT_ALT" vc > "$AUS/2a_gen_textur_vc.log" 2>&1; z gen_textur_vc_p11 $t
t=$(date +%s); VOR=""
# l3_runde REV:SHA_PY:SHA_STELLEN  (historische relief_l3.py + l3_stellen.json per git show, sha256 geprueft;
# --aus mit dem l3_rueck.npz der Vorrunde, dann anwenden). Arbeitet ueber Links auf relief_daten/neu der Arbeitskopie.
l3_runde() {
  REV=$(echo "$1" | cut -d: -f1); H="$AUS/l3_runde_$REV"; mkdir -p "$H/pruefung"
  (cd "$R" && git show "$REV:./relief_l3.py") > "$H/relief_l3.py"; echo "$(echo "$1" | cut -d: -f2)  $H/relief_l3.py" | sha256sum -c --quiet
  (cd "$R" && git show "$REV:./pruefung/l3_stellen.json") > "$H/pruefung/l3_stellen.json"
  echo "$(echo "$1" | cut -d: -f3)  $H/pruefung/l3_stellen.json" | sha256sum -c --quiet
  ln -s "$B/neu" "$H/neu"; ln -s "$B/relief_daten.json.gz" "$H/relief_daten.json.gz"
  if [ -n "$VOR" ]; then mv "$VOR/pruefung/l3_rueck.npz" "$H/pruefung/"; python3 "$H/relief_l3.py" --aus >> "$AUS/2b_relief_l3.log" 2>&1; fi
  python3 "$H/relief_l3.py" >> "$AUS/2b_relief_l3.log" 2>&1; VOR=$H
}
SF=2f0fe77f355f77c8d549b2c1d1cc47fc522da1d651f991394ff0ed76510eaa5b
for RUNDE in 232f113:8f0c96074a243934134e2f611096ec895a96d65f4e1c1d0713bb58361f21567d:$SF \
             3e68969:b3fbf5eaeb539ab589c502667c8d968d409a13a9aa6cfb1bbe90ff60bf307086:$SF; do
  l3_runde "$RUNDE"; python3 "$GT_ALT" vc >> "$AUS/2b_relief_l3.log" 2>&1
done
l3_runde 8cd6d37:b3fbf5eaeb539ab589c502667c8d968d409a13a9aa6cfb1bbe90ff60bf307086:713999a13dab4c844dbeffbb015ddd0a20280016efe31696ebe6c1d2ed3b05e5
z relief_l3_runden $t
t=$(date +%s); python3 "$GT_ALT" vc > "$AUS/3_gen_textur_vc.log" 2>&1; z gen_textur_vc $t
t=$(date +%s); NODE_DIR="$NODE_BAU" RELIEF_NEU=1 python3 baue_html.py > "$AUS/4_baue_html.log" 2>&1; z baue_html $t
t=$(date +%s); python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py > "$AUS/5_html_payload_p3.log" 2>&1; z html_payload_p3 $t
t=$(date +%s); python3 pruefung/p10c/waende_einsetzen.py > "$AUS/6_waende_einsetzen.log" 2>&1; z waende_einsetzen $t
# 7) L3b (d5b17e2) wie entstanden: e7dadd6 anwenden (ohne vc), dann je Runde vc -> waende -> payload
#    (ERGEBNIS_L3b "Pipeline"); e193584, 9bb5d10 und 1b8a477 (= d5b17e2) je --aus, anwenden, Pipeline.
#    Die L3b-Schalter (wasser, fw_folgen, rampe_m, weg_rand_m, ...) stehen je Stelle in l3_stellen.json, kein CLI-Flag.
t=$(date +%s)
l3b_pipeline() {
  python3 "$GT_ALT" vc >> "$AUS/7_l3b.log" 2>&1
  python3 pruefung/p10c/waende_einsetzen.py >> "$AUS/7_l3b.log" 2>&1
  python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py >> "$AUS/7_l3b.log" 2>&1
}
l3_runde e7dadd6:ba1d747b22806a0885a85e7a990cbd6387da6825bf13d0427fba8fc6f85d3591:558185481df3344c64d2667c268028f73368deba783dbe73824ea8141b127c36
l3b_pipeline
l3_runde e193584:aaf9f624d61c32ada519f0bc7b76bec48eb3d9d9cf3560c939613166df98e076:6d80c96b694126c9451a0e5c032de69aa643286157b2cef116e16cd156bfa6c0
l3b_pipeline
l3_runde 9bb5d10:5f593ef676eada30af1adcf8f7d9f89c060ff21f9cb469d12f2a8c7a593051f7:b4a4c024943008b91f5d01aef6dd4e740eb1e11c1e6690a6e453c29fb492765e
l3b_pipeline
# letzte L3b-Runde = relief_l3.py/l3_stellen.json von 1b8a477 (= d5b17e2). Das aktuelle relief_l3.py ohne Option rechnet
# dieselben Daten (eingefroren, L3c2), schreibt aber in l3_bericht.json zusaetzlich "stufe"; der Repo-Bericht stammt von 1b8a477.
l3_runde 1b8a477:5f593ef676eada30af1adcf8f7d9f89c060ff21f9cb469d12f2a8c7a593051f7:8186f502d21ba5b2fb10f462c94077989415de707c1c781731bfc51e1f783f05
cp "$VOR/pruefung/l3_rueck.npz" "$VOR/pruefung/l3_bericht.json" pruefung/
l3b_pipeline
z l3b_runden $t
# 8) P2b/P2c (a6a4831) wie entstanden (pruefung/p2_analyse/p2c/p2b2_pipe.sh, ERGEBNIS_P2B/P2C): Vorher-Stand sichern,
#    relief_p2b.py (Stellen 03/03b/03c/03d/03m/14/23 aus p2b_stellen.json, Basis-GB-Hash-Pruefung im Skript),
#    Bruecke E2, gen_textur.py vc (aktuell), VC/FW.c nur lokal (p2b_vc_lokal.py gegen den Vorher-Stand), Farbe rampe_5,
#    payload, waende. P2c ist kein eigener Lauf: P2c hat Stellen/relief_p2b.py erweitert und dieselbe Pipeline auf den
#    L3b-Stand (d5b17e2) neu ausgefuehrt.
t=$(date +%s); V2="$AUS/p2b_vorher"; mkdir -p "$V2"; cp relief_daten.json.gz neu/relief_neu.json.gz "$V2/"
python3 relief_p2b.py > "$AUS/8_p2b.log" 2>&1
python3 pruefung/p2_analyse/p2b/p2b_bruecken.py >> "$AUS/8_p2b.log" 2>&1
python3 gen_textur.py vc >> "$AUS/8_p2b.log" 2>&1
python3 pruefung/p2_analyse/p2b/p2b_vc_lokal.py "$V2/relief_daten.json.gz" "$V2/relief_neu.json.gz" >> "$AUS/8_p2b.log" 2>&1
python3 pruefung/p2_analyse/p2b/p2b_r5_textur.py >> "$AUS/8_p2b.log" 2>&1
python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py >> "$AUS/8_p2b.log" 2>&1
python3 pruefung/p10c/waende_einsetzen.py >> "$AUS/8_p2b.log" 2>&1
z p2b_p2c $t
# 11) L3c2 (81b6f94, ERGEBNIS_L3c2 Abschnitt 1 + 8): Vorher-Stand sichern, relief_l3.py --stufe-c (eigener Basis-Hash und
#     Rueckweg pruefung/l3c_rueck.npz, richtiger Massstab), gen_textur.py vc (aktuell), l3c_vc_lokal.py <Vorher>, payload, waende.
#     relief_l3.py ohne Option (Schritt 7) bleibt der eingefrorene L3/L3b-Lauf (massstab_l3_l3b_eingefroren in l3_stellen.json).
t=$(date +%s); V3="$AUS/l3c_vorher"; mkdir -p "$V3"; cp relief_daten.json.gz neu/relief_neu.json.gz "$V3/"
python3 relief_l3.py --stufe-c > "$AUS/11_l3c.log" 2>&1
python3 gen_textur.py vc >> "$AUS/11_l3c.log" 2>&1
python3 pruefung/l3c_vc_lokal.py "$V3/relief_daten.json.gz" "$V3/relief_neu.json.gz" >> "$AUS/11_l3c.log" 2>&1
python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py >> "$AUS/11_l3c.log" 2>&1
python3 pruefung/p10c/waende_einsetzen.py >> "$AUS/11_l3c.log" 2>&1
z l3c2 $t

# 12) L3d (ERGEBNIS_L3d): eigener Basis-Hash im Skript, Rueckweg pruefung/l3d/l3d_rueck.npz (relief_l3d.py --aus).
if [ "${L3D:-1}" != 0 ]; then
t=$(date +%s)
python3 relief_l3d.py > "$AUS/12_l3d.log" 2>&1
python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py >> "$AUS/12_l3d.log" 2>&1
python3 pruefung/p10c/waende_einsetzen.py >> "$AUS/12_l3d.log" 2>&1
z l3d $t
fi
# 13) L3e (ERGEBNIS_L3e): eigener Basis-Hash im Skript, Rueckweg pruefung/l3e/l3e_rueck.npz (relief_l3e.py --aus).
if [ "$L3E" != 0 ]; then
t=$(date +%s)
python3 relief_l3e.py > "$AUS/13_l3e.log" 2>&1
python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py >> "$AUS/13_l3e.log" 2>&1
python3 pruefung/p10c/waende_einsetzen.py >> "$AUS/13_l3e.log" 2>&1
z l3e $t
fi
# 14) P2d (= pruefung/p2_analyse/p2d/p2d_pipe.sh, inline weil die Arbeitskopie aus pruefung/ nur .json/.py uebernimmt)
if [ "$P2D" != 0 ]; then
t=$(date +%s); V4="$AUS/p2d_vorher"; mkdir -p "$V4"; cp relief_daten.json.gz neu/relief_neu.json.gz "$V4/"
python3 relief_p2d.py > "$AUS/14_p2d.log" 2>&1
python3 gen_textur.py vc >> "$AUS/14_p2d.log" 2>&1
python3 pruefung/p2_analyse/p2d/p2d_vc_lokal.py "$V4/relief_daten.json.gz" "$V4/relief_neu.json.gz" >> "$AUS/14_p2d.log" 2>&1
python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py >> "$AUS/14_p2d.log" 2>&1
python3 pruefung/p10c/waende_einsetzen.py >> "$AUS/14_p2d.log" 2>&1
z p2d $t
fi
# 15) L3f (ERGEBNIS_L3f): eigener Basis-Hash im Skript, Rueckweg pruefung/l3f/l3f_rueck.npz (relief_l3f.py --aus).
if [ "$L3F" != 0 ]; then
t=$(date +%s)
python3 relief_l3f.py > "$AUS/15_l3f.log" 2>&1
python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py >> "$AUS/15_l3f.log" 2>&1
python3 pruefung/p10c/waende_einsetzen.py >> "$AUS/15_l3f.log" 2>&1
z l3f $t
fi
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

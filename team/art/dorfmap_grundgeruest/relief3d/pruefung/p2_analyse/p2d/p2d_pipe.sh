#!/bin/sh
# P2d-Pipeline (relief3d/): Basis = Stand art/dorfmap-fertig b3698e0 (nach L3d) im Arbeitsbaum. V = Ordner fuer den Vorher-Stand.
set -e
V=${1:?Vorher-Ordner}; mkdir -p "$V"; cp relief_daten.json.gz neu/relief_neu.json.gz "$V/"
python3 relief_p2d.py
python3 gen_textur.py vc
python3 pruefung/p2_analyse/p2d/p2d_vc_lokal.py "$V/relief_daten.json.gz" "$V/relief_neu.json.gz"
python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py
python3 pruefung/p10c/waende_einsetzen.py

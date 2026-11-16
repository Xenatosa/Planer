#!/usr/bin/env python3
"""P10c: Wandkoerper in neu/relief_neu.json.gz mit dem korrigierten neu/wand.py neu bauen.

Warum nicht neu/pipeline.py: Seit a10fc1e (P3, nur VC/FW geaendert) passt relief_daten.json.gz
nicht mehr zur source_relief_sha256 der p3d17-Rasterloesung; build_manifest() bricht fuer D1 ab.
Die Wandkoerper haengen nur von neu/vektor.json und den gespeicherten Terrain-Kacheln ab
(build_wall_manifest(terrain_tiles=...)), genau wie in pipeline.build(). Daher:
  1. Manifest aus neu/relief_neu.json.gz lesen; Kontrolle: alles ausser 'waende' und lod1-Wandzahlen bleibt.
  2. --pruefen: mit dem aktuellen wand.py neu bauen und nur vergleichen (nichts schreiben).
  3. Sonst 'waende' + lod1 ersetzen, gzip wie pipeline.py (level 9, mtime 0) schreiben und in
     index.html / neu/index.html nur die NEU_GZ-Datenzeile ersetzen (Bundle bytegleich, wie
     pruefung/p3_nahbilder/werkzeug/html_payload_p3.py).
Aufruf (relief3d/): python3 pruefung/p10c/waende_einsetzen.py [--pruefen]
"""
import base64
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from neu.wand import build_wall_manifest  # noqa: E402

pfad = ROOT / "neu" / "relief_neu.json.gz"
roh = pfad.read_bytes()
paket = json.loads(gzip.decompress(roh))
# Serialisierung wie pipeline.py muss das gespeicherte Paket exakt reproduzieren.
neu_roh = gzip.compress(json.dumps(paket, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), compresslevel=9, mtime=0)
reproduzierbar = neu_roh == roh
man = paket["neu_mesh_tiles"]
alt = man["waende"]
neu = build_wall_manifest(ROOT / "neu" / "vektor.json", terrain_tiles=man["tiles"])
bericht = {
    "serialisierung_bytegleich": reproduzierbar,
    "tiles": {t: {"alt_sha256": alt["tiles"][t]["mesh_sha256"], "neu_sha256": neu["tiles"][t]["mesh_sha256"],
                  "gleich": alt["tiles"][t]["mesh_sha256"] == neu["tiles"][t]["mesh_sha256"],
                  "alt_dreiecke": alt["tiles"][t]["triangles"], "neu_dreiecke": neu["tiles"][t]["triangles"],
                  "alt_features": alt["tiles"][t]["features"], "neu_features": neu["tiles"][t]["features"],
                  "alt_vertices": alt["tiles"][t]["vertices"], "neu_vertices": neu["tiles"][t]["vertices"]}
              for t in alt["tiles"]},
    "foot_vertices_lowered": [alt["foot_vertices_lowered"], neu["foot_vertices_lowered"]],
}
if "--pruefen" in sys.argv:
    print(json.dumps(bericht, indent=1))
    sys.exit(0)
if not reproduzierbar:
    raise SystemExit("relief_neu.json.gz laesst sich nicht bytegleich neu serialisieren - Abbruch")
terrain_vorher = {k: hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest() for k, v in man.items() if k not in ("waende", "lod1")}
man["waende"] = neu
wall = sum(t["triangles"] for t in neu["tiles"].values())
man["lod1"]["wall_triangles"] = wall
man["lod1"]["total_triangles"] = man["lod1"]["terrain_closed_triangles"] + wall
if man["lod1"]["total_triangles"] >= man["lod1"]["budget_triangles"]:
    raise SystemExit("LOD1-Budget ueberschritten")
terrain_nachher = {k: hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest() for k, v in man.items() if k not in ("waende", "lod1")}
assert terrain_vorher == terrain_nachher
daten = gzip.compress(json.dumps(paket, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), compresslevel=9, mtime=0)
pfad.write_bytes(daten)
d64 = base64.b64encode(daten).decode()
for p in (ROOT / "index.html", ROOT / "neu" / "index.html"):
    h = p.read_text(encoding="utf-8")
    i = h.index('window.NEU_GZ="') + len('window.NEU_GZ="')
    j = h.index('"', i)
    p.write_text(h[:i] + d64 + h[j:], encoding="utf-8")
bericht["lod1"] = man["lod1"]
bericht["relief_neu_sha256"] = [hashlib.sha256(roh).hexdigest(), hashlib.sha256(daten).hexdigest()]
print(json.dumps(bericht, indent=1))

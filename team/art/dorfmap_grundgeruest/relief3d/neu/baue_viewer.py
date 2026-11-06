"""Build the standalone HTML viewer for the opt-in tiled 3D core."""
from __future__ import annotations

import base64
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def run() -> None:
    node_dir = Path(os.environ.get("NODE_DIR", "/tmp/w3"))
    env = {**os.environ, "NODE_PATH": str(node_dir / "node_modules")}
    with tempfile.TemporaryDirectory(prefix="relief_neu_bundle_") as tmp:
        bundle = Path(tmp) / "main.js"
        subprocess.run(
            [str(node_dir / "node_modules" / ".bin" / "esbuild"), "main.js", "--bundle",
             "--minify", "--format=iife", f"--outfile={bundle}"],
            cwd=ROOT, env=env, check=True,
        )
        js = bundle.read_text(encoding="utf-8")

    data = _b64(ROOT / "neu" / "relief_neu.json.gz")
    doc = f'''<!doctype html><html lang="de" data-core="relief-neu-mesh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Relief-Neu Geländemesh · Drei Kachelmeshes</title>
<style>
html,body{{margin:0;width:100%;height:100%;overflow:hidden;font:14px system-ui,sans-serif;color:#202322}}
#lade{{position:absolute;inset:0;display:grid;place-items:center;background:#dce4e8;font-size:20px;z-index:3}}
#p,#info{{position:absolute;z-index:2;background:#fffd;padding:10px;border-radius:6px;box-shadow:0 1px 6px #0003}}
#p{{left:8px;top:8px;max-width:320px}}#info{{right:8px;top:8px;font:11px monospace;white-space:pre;max-height:90vh;overflow:auto}}
button{{margin:2px;padding:4px 8px}}label{{display:block;margin:3px 0}}.sel{{font-weight:bold;background:#d4dfda}}
input[type=range]{{width:110px;vertical-align:middle}}
</style></head><body>
<div id="lade">Lade die drei echten Kachelmeshes …</div>
<div id="p"><b>Relief-Neubau · 3D-Mesh</b><br><span id="modus"></span><hr>
Kacheln: D1, G1, D2 · Oberfläche 0,5 m · D2 unverändert<br>
<button data-tile="D1">D1</button><button data-tile="G1">G1</button><button data-tile="D2">D2</button><br>
<button id="reset">Schräg</button><button id="voben">Oben</button><button id="vwand">D1 Wandfuß</button><br>
<label><input type="checkbox" data-l="gelaende" checked> Gelände</label>
<label><input type="checkbox" data-l="waende" checked> separate Wände D1/G1</label>
Licht Richtung <input id="az" type="range" min="0" max="360" value="315"><br>
Licht Höhe <input id="el" type="range" min="5" max="90" value="35"><br>
Licht Stärke <input id="st" type="range" min="0" max="150" value="90"><br>
Maus: links drehen, rechts verschieben, Rad zoomen.
</div><div id="info">3D Meshes: D1 · G1 · D2</div>
<script>window.NEU_GZ="{data}";window.RELIEF_NEU_VIEWER=1;</script><script>{js}</script>
</body></html>'''
    # Three.js embeds multiline shader strings with trailing source whitespace.
    # Match the legacy builder's deterministic cleanup without changing code.
    doc = "\n".join(line.rstrip() for line in doc.splitlines()) + "\n"
    (ROOT / "index.html").write_text(doc, encoding="utf-8")
    (ROOT / "neu" / "index.html").write_text(doc, encoding="utf-8")
    print(f"index.html und neu/index.html {len(doc)} Bytes; Relief-Neu-Viewer mit D1/G1/D2")

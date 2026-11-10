"""Kleiner lokaler Diagnose-Viewer fuer D1/G1/D2."""
from __future__ import annotations

import html
import json
from pathlib import Path

from .vektor import OUT


def run() -> None:
    vector = json.loads((OUT / "vektor.json").read_text(encoding="utf-8"))
    tiles = vector["prototype_kacheln"]
    imgs = "".join(
        f'<section><h2>{html.escape(tile)}</h2><img src="debug_{html.escape(tile)}.png" alt="Vektor-Debug {html.escape(tile)}"></section>'
        for tile in tiles
    )
    doc = f'''<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dorfkarte – Vektor-Prototyp</title><style>body{{font:14px system-ui;margin:24px;background:#eef0ed;color:#202525}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:20px}}section{{background:white;padding:14px;border-radius:8px}}img{{width:100%;image-rendering:pixelated;border:1px solid #333}}p{{max-width:850px;line-height:1.45}}</style>
<h1>Vektorschicht – Diagnoseansicht</h1><p>Quellraster mit abgeleiteten Wegen, Kreuzungen, Waenden, Wasser und Bauzonen. Die globale Abstandsfeld-Datei liegt in <code>felder.npz</code>; dargestellt sind nur {', '.join(tiles)}.</p><main>{imgs}</main></html>'''
    (OUT / "index.html").write_text(doc, encoding="utf-8")
    print(f"{OUT / 'index.html'} ({len(doc)} Zeichen)")

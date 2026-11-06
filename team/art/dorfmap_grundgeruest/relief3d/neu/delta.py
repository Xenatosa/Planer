"""Compare gate and nahbild snapshots by tile/rule; non-zero on every increase."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


FILES = {"regeln": ("regeln.json", "pruefe_regeln.json"), "r8": ("r8.json",), "r9": ("r9.json",), "loch": ("loch.json", "lochscan.json"), "nahbild": ("nahbild_werte.json", "nahbild.json")}
IMAGE_METRICS = ("kantenzaehne", "facetten", "normale_spruenge", "normale_sprung_inseln", "loecher", "flecken", "loch_flecken")


def _read(directory: Path, name: str) -> dict | None:
    for candidate in FILES[name]:
        p = directory / candidate
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return None


def _field_counts(data: dict | None, kind: str) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = {}
    if not data:
        return counts
    if kind == "regeln":
        for hit in data.get("treffer", []):
            rule = str(hit.get("regel", "?"))
            tile = str(hit.get("feld", "-"))
            counts[(rule, tile)] = counts.get((rule, tile), 0) + 1
    elif kind in ("r8", "r9"):
        for tile, rules in data.get("je_feld", {}).items():
            for rule, n in rules.items():
                counts[(str(rule), str(tile))] = int(n)
    elif kind == "loch":
        for point in data.get("punkte", []):
            if len(point) >= 3:
                x, z = float(point[0]), float(point[2])
                tile = "ABCDEFGH"[max(0, min(7, int(x // 42)))] + str(max(1, min(7, int(z // 43) + 1)))
                counts[("G1_loch_offen", tile)] = counts.get(("G1_loch_offen", tile), 0) + 1
        # Some accepted lochscan formats carry only an aggregate.
        if not data.get("punkte") and data.get("offen_innen", 0):
            counts[("G1_loch_offen", "-")] = int(data["offen_innen"])
    return counts


def _image_counts(data: dict | None) -> dict[tuple[str, str, str, str], int]:
    result = {}
    if not data:
        return result
    for image in data.get("images", []):
        tile, mode, camera = image.get("tile"), image.get("mode"), image.get("camera")
        # Clay isolates terrain geometry. Textured frames remain in the capture
        # JSON for visual review, but include houses and view-dependent texture
        # shading that make pixel proxies unsuitable for a geometry gate.
        if not tile or mode != "clay" or not camera:
            continue
        for metric in IMAGE_METRICS:
            value = image.get(metric)
            if isinstance(value, (int, float)):
                result[(str(tile), str(mode), str(camera), metric)] = int(value)
    return result


def compare(before: Path, after: Path) -> dict:
    rule_rows = []
    for kind in ("regeln", "r8", "r9", "loch"):
        a, b = _field_counts(_read(before, kind), kind), _field_counts(_read(after, kind), kind)
        for rule, tile in sorted(set(a) | set(b)):
            av, bv = a.get((rule, tile), 0), b.get((rule, tile), 0)
            rule_rows.append({"gruppe": kind, "regel": rule, "kachel": tile, "vorher": av, "nachher": bv, "delta": bv - av})
    a_img = _image_counts(_read(before, "nahbild"))
    b_img = _image_counts(_read(after, "nahbild"))
    image_rows = []
    for key in sorted(set(a_img) | set(b_img)):
        av, bv = a_img.get(key, 0), b_img.get(key, 0)
        image_rows.append({"kachel": key[0], "modus": key[1], "kamera": key[2], "metrik": key[3], "vorher": av, "nachher": bv, "delta": bv - av})
    increases = [row for row in rule_rows + image_rows if row["delta"] > 0]
    return {"regel_und_kachel": rule_rows, "bildzahlen": image_rows, "anstiege": increases, "exit_code": 1 if increases else 0}


def markdown(result: dict, label_before: str, label_after: str) -> str:
    lines = [
        "# Delta-Bericht Nahbild/Gates",
        "",
        f"Vergleich: **{label_before}** → **{label_after}**. Ein positiver Delta-Wert gilt als Anstieg.",
        "Bildzahl-Deltas verwenden Clay-Bilder als Geometrie-Messung; Textur-Bilder bleiben zur visuellen Kontrolle in den Nahbild-JSONs.",
        f"",
        f"Anstiege: **{len(result['anstiege'])}**; Exit-Code: **{result['exit_code']}**.",
        "",
        "## Gate-Treffer je Regel und Kachel",
        "",
        "| Gruppe | Regel | Kachel | vorher | nachher | Δ |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in result["regel_und_kachel"]:
        lines.append(f"| {row['gruppe']} | {row['regel']} | {row['kachel']} | {row['vorher']} | {row['nachher']} | {row['delta']:+d} |")
    lines += ["", "## Bildzahlen je Kachel, Kamera und Modus", "", "| Kachel | Modus | Kamera | Metrik | vorher | nachher | Δ |", "|---|---|---|---|---:|---:|---:|"]
    for row in result["bildzahlen"]:
        lines.append(f"| {row['kachel']} | {row['modus']} | {row['kamera']} | {row['metrik']} | {row['vorher']} | {row['nachher']} | {row['delta']:+d} |")
    if not result["regel_und_kachel"]:
        lines.append("| — | — | — | — | 0 | 0 | +0 |")
    if not result["bildzahlen"]:
        lines.append("| — | — | — | — | 0 | 0 | +0 |")
    lines += ["", "Ein positiver Anstieg in einer Gate-Regel/Kachel oder einer Bildmetrik liefert Exit-Code 1.", ""]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--before", required=True, type=Path, help="Verzeichnis mit regeln/r8/r9/loch/nahbild JSON")
    ap.add_argument("--after", required=True, type=Path, help="Verzeichnis mit regeln/r8/r9/loch/nahbild JSON")
    ap.add_argument("--out", required=True, type=Path, help="Markdown-Datei")
    ap.add_argument("--json", type=Path, help="optionaler JSON-Delta-Bericht")
    ap.add_argument("--before-label", default="vorher")
    ap.add_argument("--after-label", default="nachher")
    args = ap.parse_args()
    result = compare(args.before, args.after)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markdown(result, args.before_label, args.after_label), encoding="utf-8")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"anstiege": len(result["anstiege"]), "markdown": str(args.out), "exit_code": result["exit_code"]}, ensure_ascii=False))
    raise SystemExit(result["exit_code"])


if __name__ == "__main__":
    main()

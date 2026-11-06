import json
import struct
import subprocess
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).resolve().parents[1] / "nahbild.js"


def png(path, width, height, pixels):
    def chunk(name, data):
        body = name + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    scan = bytearray()
    for y in range(height):
        scan.append(0)
        for x in range(width):
            scan.extend(pixels[y][x])
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(bytes(scan))) + chunk(b"IEND", b"")
    path.write_bytes(data)


def test_png_metrics_find_dark_and_bright_local_spots(tmp_path):
    w = h = 48
    pixels = [[(150, 150, 150) for _ in range(w)] for _ in range(h)]
    for y in range(8, 13):
        for x in range(8, 13):
            pixels[y][x] = (15, 15, 15)
    for y in range(30, 35):
        for x in range(30, 35):
            pixels[y][x] = (250, 250, 250)
    image = tmp_path / "sample.png"
    png(image, w, h, pixels)
    out = tmp_path / "metrics.json"
    subprocess.run(["node", str(SCRIPT), "--files", str(image), "--out", str(out)], check=True, capture_output=True, text=True)
    result = json.loads(out.read_text())["images"][0]
    assert result["loecher"] >= 1
    assert result["flecken"] >= 1
    assert result["ground_pixel"] > 0

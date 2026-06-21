from __future__ import annotations

import struct
import zlib
from pathlib import Path


def _chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_bar_chart(path: Path, values: list[float], width: int = 900, height: int = 420) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bg = (247, 243, 234)
    ink = (19, 33, 26)
    tide = (31, 122, 140)
    clay = (184, 95, 69)
    pixels = bytearray()
    canvas = [[bg for _ in range(width)] for _ in range(height)]

    margin = 60
    chart_h = height - margin * 2
    chart_w = width - margin * 2
    max_value = max(values or [1.0])
    bar_gap = 18
    bar_w = max(18, int((chart_w - bar_gap * max(0, len(values) - 1)) / max(1, len(values))))
    for index, value in enumerate(values):
        bar_h = int((value / max_value) * chart_h) if max_value else 0
        x0 = margin + index * (bar_w + bar_gap)
        y0 = height - margin - bar_h
        color = tide if value >= 0.5 else clay
        for y in range(y0, height - margin):
            for x in range(x0, min(width - margin, x0 + bar_w)):
                canvas[y][x] = color

    for x in range(margin, width - margin):
        canvas[height - margin][x] = ink
    for y in range(margin, height - margin + 1):
        canvas[y][margin] = ink

    for row in canvas:
        pixels.append(0)
        for r, g, b in row:
            pixels.extend([r, g, b])

    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += _chunk(b"IDAT", zlib.compress(bytes(pixels), 9))
    png += _chunk(b"IEND", b"")
    path.write_bytes(png)

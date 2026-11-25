"""
icons.py — tiny pixel icons embedded as data-URI logos in shields.io badges
(for brands whose logos were removed from simple-icons: C#, VS Code, CapCut/剪映,
LinkedIn) plus a mini pixel shark for the portfolio badge.

Usage:  python icons.py <out_dir>   -> writes <name>.svg files + icons.json
"""
from __future__ import annotations
import base64, json, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelkit import text_pixels, mono_rects

MINI_SHARK = [
    "......#......",
    ".#....##.....",
    ".##..#####...",
    "..##########.",
    "..####.######",
    ".##.######.#.",
    ".#....##.....",
    "......#......",
]
CLAPPER = [
    "#.##.##.#",
    "##.##.##.",
    "#########",
    "#.......#",
    "#.......#",
    "#.......#",
    "#.......#",
    "#########",
]
LINKEDIN = [
    "#.....",
    "......",
    "#.####",
    "#.#..#",
    "#.#..#",
    "#.#..#",
    "#.#..#",
]
SHIELD = [
    ".#######.",
    "#########",
    "####.####",
    "###...###",
    "####.####",
    ".#######.",
    ".#######.",
    "..#####..",
    "...###...",
    "....#....",
]
SEARCH = [
    ".####....",
    "#....#...",
    "#....#...",
    "#....#...",
    "#....#...",
    ".####.#..",
    ".....###.",
    "......###",
    ".......##",
]
TROPHY = [
    "#########",
    "#.#####.#",
    "#.#####.#",
    ".#.###.#.",
    "..#####..",
    "...###...",
    "....#....",
    "...###...",
    "..#####..",
]


def grid_points(rows):
    return {(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == "#"}, len(rows[0]), len(rows)


def icon_svg(points, w, h, color, pad=1):
    body = mono_rects(points, color, 1, pad, pad)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 2 * pad} {h + 2 * pad}" '
            f'shape-rendering="crispEdges">{body}</svg>')


def build(color_map: dict[str, str]):
    icons = {}
    pts, w = text_pixels("C#")
    icons["csharp"] = icon_svg(pts, w, 7, color_map["csharp"])
    pts, w = text_pixels("<>")
    icons["vscode"] = icon_svg(pts, w, 7, color_map["vscode"])
    pts, w, h = grid_points(CLAPPER)
    icons["capcut"] = icon_svg(pts, w, h, color_map["capcut"])
    pts, w, h = grid_points(LINKEDIN)
    icons["linkedin"] = icon_svg(pts, w, h, color_map["linkedin"])
    pts, w, h = grid_points(MINI_SHARK)
    icons["shark"] = icon_svg(pts, w, h, color_map["shark"])
    pts, w, h = grid_points(SHIELD)
    icons["shield"] = icon_svg(pts, w, h, color_map["shield"])
    pts, w, h = grid_points(SEARCH)
    icons["search"] = icon_svg(pts, w, h, color_map["search"])
    pts, w, h = grid_points(TROPHY)
    icons["trophy"] = icon_svg(pts, w, h, color_map["trophy"])
    return icons


def data_uri(svg: str) -> str:
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return "data:image/svg+xml;base64," + b64


def shields_logo_param(svg: str) -> str:
    # shields wants the data URI URL-encoded (base64 '+', '/', '=' must be escaped)
    return urllib.parse.quote(data_uri(svg), safe="")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    colors = {"csharp": "#FF3CAC", "vscode": "#00F7FF", "capcut": "#00FF41",
              "linkedin": "#00F7FF", "shark": "#00FF41", "shield": "#00FF41",
              "search": "#00F7FF", "trophy": "#FFD166"}
    icons = build(colors)
    meta = {}
    for name, svg in icons.items():
        with open(os.path.join(out, f"{name}.svg"), "w") as f:
            f.write(svg)
        meta[name] = {"svg_bytes": len(svg), "logo_param": shields_logo_param(svg)}
    with open(os.path.join(out, "icons.json"), "w") as f:
        json.dump(meta, f, indent=1)
    for n, m in meta.items():
        print(n, m["svg_bytes"], "bytes; param len", len(m["logo_param"]))

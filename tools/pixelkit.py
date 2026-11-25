"""
pixelkit.py — tiny pixel-art toolkit used to build the Blaze Eternum README assets.

Everything here is pure data + SVG string generation. No external deps except
Pillow for the optional PNG export (run with the venv python).
"""
from __future__ import annotations

# --------------------------------------------------------------------------- #
# Palette (from the master prompt + a few derived shades)
# --------------------------------------------------------------------------- #
PALETTE = {
    "o": "#0A1025",  # outline / dark navy
    "B": "#008CFF",  # body electric blue
    "D": "#0066CC",  # body shade
    "C": "#00F7FF",  # neon cyan highlight / circuit lines
    "W": "#D8FAFF",  # belly
    "P": "#A020F0",  # neon purple fin edges
    "V": "#C45CFF",  # light purple
    "K": "#FF3CAC",  # accent pink circuit nodes
    "F": "#050510",  # sunglasses frame / deep black
    "1": "#8EFCFF",  # lens top (gloss)
    "2": "#2EEBFF",  # lens middle
    "3": "#00BFEF",  # lens bottom
    "G": "#FFFFFF",  # lens glint
    "M": "#1A0B2E",  # mouth interior
    "T": "#FFFFFF",  # teeth
    "N": "#0057B8",  # gill slits
    "g": "#00FF41",  # matrix green (text use)
}

# --------------------------------------------------------------------------- #
# The cyber shark sprite (46 x 28, facing right)
# --------------------------------------------------------------------------- #
SHARK_W, SHARK_H = 46, 28


def build_shark() -> dict[tuple[int, int], str]:
    """Return {(x, y): palette_key} for the shark sprite (outline included)."""
    px: dict[tuple[int, int], str] = {}

    def span(y, x0, x1, key):
        for x in range(x0, x1 + 1):
            px[(x, y)] = key

    # --- body silhouette (row: left..right), chibi head on the right -------- #
    body = {
        7: (33, 37), 8: (30, 40), 9: (18, 41), 10: (15, 42), 11: (13, 42),
        12: (11, 42), 13: (10, 43), 14: (10, 43), 15: (10, 43), 16: (10, 43),
        17: (11, 42), 18: (13, 42), 19: (15, 41), 20: (18, 40), 21: (24, 39),
        22: (31, 37),
    }
    for y, (a, b) in body.items():
        span(y, a, b, "B")

    # --- tail stem (caudal peduncle) --------------------------------------- #
    for y, (a, b) in {12: (9, 10), 13: (7, 9), 14: (7, 9), 15: (7, 9), 16: (9, 9)}.items():
        span(y, a, b, "B")

    # --- chunky chevron tail fin ------------------------------------------ #
    tail = {
        4: (2, 2), 5: (2, 3), 6: (2, 4), 7: (3, 5), 8: (3, 6), 9: (4, 6), 10: (4, 7),
        11: (5, 8), 12: (5, 8), 13: (5, 6), 14: (5, 6), 15: (5, 6), 16: (5, 8),
        17: (5, 8), 18: (4, 7), 19: (4, 6), 20: (3, 6), 21: (3, 5), 22: (2, 4),
        23: (2, 3), 24: (2, 2),
    }
    for y, (a, b) in tail.items():
        span(y, a, b, "B")
        px[(a, y)] = "P"                      # neon trailing edge
        if y in (4, 5, 23, 24):               # lobe tips fully purple
            span(y, a, b, "P")
        elif y in (6, 7, 21, 22):
            px[(a + 1, y)] = "V"

    # --- dorsal fin (tip leans back toward the tail) ----------------------- #
    dorsal = {3: (19, 19), 4: (19, 21), 5: (19, 22), 6: (19, 24), 7: (20, 26), 8: (20, 28)}
    for y, (a, b) in dorsal.items():
        span(y, a, b, "B")
        px[(a, y)] = "P"
        if y in (3, 4):
            span(y, a, b, "P")
        if y >= 5:
            px[(b, y)] = "C"                  # cyan leading edge

    # --- shading + highlights --------------------------------------------- #
    span(17, 12, 29, "D")
    span(18, 14, 29, "D")
    px[(41, 13)] = "D"
    span(14, 37, 38, "D")
    span(15, 33, 34, "D")
    span(16, 29, 30, "D")
    span(7, 34, 36, "C")                      # top-of-head gloss
    span(9, 28, 30, "C")
    span(10, 16, 17, "C")

    # --- belly ------------------------------------------------------------- #
    belly = {13: (42, 43), 14: (39, 43), 15: (35, 43), 16: (31, 43), 17: (30, 42),
             18: (30, 42), 19: (30, 41), 20: (31, 40), 21: (32, 39), 22: (32, 36)}
    for y, (a, b) in belly.items():
        span(y, a, b, "W")
    span(19, 17, 23, "W")
    span(20, 19, 23, "W")

    # --- circuit lines (Tron style) ---------------------------------------- #
    span(13, 13, 25, "C")
    for y in (12, 11):
        px[(24, y)] = "C"
    px[(24, 10)] = "K"
    for y in (14, 15):
        px[(18, y)] = "C"
    px[(18, 16)] = "K"
    px[(16, 13)] = "K"
    px[(22, 13)] = "K"

    # --- gill slits -------------------------------------------------------- #
    for y in (13, 14, 15):
        px[(28, y)] = "N"
        px[(30, y)] = "N"

    # --- pectoral fin (hangs under the belly, swept back) ------------------ #
    pect = {21: (17, 22), 22: (16, 21), 23: (16, 19), 24: (15, 17)}
    for y, (a, b) in pect.items():
        span(y, a, b, "D")
        if y >= 22:
            px[(a, y)] = "P"
    span(24, 15, 17, "P")

    # --- cyber sunglasses -------------------------------------------------- #
    span(10, 33, 40, "F")
    span(14, 33, 40, "F")
    for y in (11, 12, 13):
        px[(33, y)] = "F"
        px[(40, y)] = "F"
    span(11, 34, 39, "1")
    span(12, 34, 39, "2")
    span(13, 34, 39, "3")
    px[(38, 11)] = "G"
    px[(39, 11)] = "G"
    px[(39, 12)] = "G"
    span(11, 28, 32, "F")                     # temple arm

    # --- smile with two tiny teeth ---------------------------------------- #
    px[(32, 16)] = "M"
    px[(42, 16)] = "M"
    span(17, 33, 41, "M")
    span(18, 34, 40, "M")
    px[(35, 18)] = "T"
    px[(39, 18)] = "T"

    # --- shift by (1,1) to leave room for the auto outline ---------------- #
    px = {(x + 1, y + 1): k for (x, y), k in px.items()}

    # --- auto outline (4-neighbourhood) ----------------------------------- #
    outline = set()
    for (x, y) in list(px.keys()):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in px:
                outline.add(n)
    for n in outline:
        px[n] = "o"
    return px


# --------------------------------------------------------------------------- #
# 5x7 bitmap font (uppercase + digits + punctuation)
# --------------------------------------------------------------------------- #
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#..##", "#...#", "#...#", ".####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": ["..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
    ".": [".", ".", ".", ".", ".", ".", "#"],
    ":": [".", ".", "#", ".", ".", "#", "."],
    "|": ["#", "#", "#", "#", "#", "#", "#"],
    ">": ["#...", ".#..", "..#.", "...#", "..#.", ".#..", "#..."],
    "<": ["...#", "..#.", ".#..", "#...", ".#..", "..#.", "...#"],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
    "-": ["....", "....", "....", "####", "....", "....", "...."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "(": [".#", "#.", "#.", "#.", "#.", "#.", ".#"],
    ")": ["#.", ".#", ".#", ".#", ".#", ".#", "#."],
    "[": ["##", "#.", "#.", "#.", "#.", "#.", "##"],
    "]": ["##", ".#", ".#", ".#", ".#", ".#", "##"],
    "&": [".##..", "#..#.", "#..#.", ".##..", "#.#.#", "#..#.", ".##.#"],
    "'": ["#", "#", ".", ".", ".", ".", "."],
    "!": ["#", "#", "#", "#", "#", ".", "#"],
    ",": ["..", "..", "..", "..", "..", ".#", "#."],
    "#": [".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "=": [".....", ".....", "#####", ".....", "#####", ".....", "....."],
    "@": [".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."],
    "~": [".....", ".....", ".#..#", "#.#.#", "#..#.", ".....", "....."],
    "*": [".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "%": ["##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"],
    "█": ["#####", "#####", "#####", "#####", "#####", "#####", "#####"],  # full block
}
FONT_H = 7


def text_pixels(text: str, spacing: int = 1) -> tuple[set[tuple[int, int]], int]:
    """Rasterise `text` with the bitmap font. Returns (set of (x,y), total width)."""
    pts: set[tuple[int, int]] = set()
    cx = 0
    for ch in text.upper():
        glyph = FONT.get(ch)
        if glyph is None:
            glyph = FONT["?"]
        w = len(glyph[0])
        for y, row in enumerate(glyph):
            for x, c in enumerate(row):
                if c == "#":
                    pts.add((cx + x, y))
        cx += w + spacing
    return pts, max(cx - spacing, 0)


def text_width(text: str, spacing: int = 1) -> int:
    return text_pixels(text, spacing)[1]


# --------------------------------------------------------------------------- #
# SVG helpers
# --------------------------------------------------------------------------- #
def rle_runs(pixels: dict[tuple[int, int], str]):
    """Yield (x0, y, width, key) horizontal runs of identical colour."""
    rows: dict[int, list[tuple[int, str]]] = {}
    for (x, y), k in pixels.items():
        rows.setdefault(y, []).append((x, k))
    for y in sorted(rows):
        run = sorted(rows[y])
        i = 0
        while i < len(run):
            x0, k = run[i]
            j = i
            while j + 1 < len(run) and run[j + 1][0] == run[j][0] + 1 and run[j + 1][1] == k:
                j += 1
            yield x0, y, run[j][0] - x0 + 1, k
            i = j + 1


def rle_rects(pixels: dict[tuple[int, int], str], colors: dict[str, str], scale: float = 1,
              ox: float = 0, oy: float = 0, extra_attr: str = "") -> str:
    """Emit <rect>s, merging horizontal runs of the same colour."""
    out = []
    for x0, y, w, k in rle_runs(pixels):
        out.append(
            f'<rect x="{fmt(ox + x0 * scale)}" y="{fmt(oy + y * scale)}" '
            f'width="{fmt(w * scale)}" height="{fmt(scale)}" fill="{colors[k]}"{extra_attr}/>'
        )
    return "\n".join(out)


def rle_paths(pixels: dict[tuple[int, int], str], colors: dict[str, str], scale: float = 1,
              ox: float = 0, oy: float = 0, extra_attr: str = "") -> str:
    """Emit ONE <path> per colour (much smaller than rects for big sprites/text)."""
    by_color: dict[str, list[str]] = {}
    for x0, y, w, k in rle_runs(pixels):
        by_color.setdefault(k, []).append(
            f"M{fmt(ox + x0 * scale)} {fmt(oy + y * scale)}h{fmt(w * scale)}v{fmt(scale)}h-{fmt(w * scale)}z")
    return "".join(f'<path fill="{colors[k]}" d="{"".join(d)}"{extra_attr}/>' for k, d in by_color.items())


def mono_rects(points: set[tuple[int, int]], color: str, scale: float = 1,
               ox: float = 0, oy: float = 0, extra_attr: str = "") -> str:
    return rle_rects({p: "x" for p in points}, {"x": color}, scale, ox, oy, extra_attr)


def mono_path(points: set[tuple[int, int]], color: str, scale: float = 1,
              ox: float = 0, oy: float = 0, extra_attr: str = "") -> str:
    return rle_paths({p: "x" for p in points}, {"x": color}, scale, ox, oy, extra_attr)


def fmt(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"


def flip_x(pixels: dict[tuple[int, int], str], width: int) -> dict[tuple[int, int], str]:
    return {(width - 1 - x, y): k for (x, y), k in pixels.items()}


# --------------------------------------------------------------------------- #
# PNG export (Pillow) — used for shark.png
# --------------------------------------------------------------------------- #
def write_png(pixels: dict[tuple[int, int], str], colors: dict[str, str], w: int, h: int,
              scale: int, path: str, bg: str | None = None) -> None:
    from PIL import Image

    def hex_to_rgba(hx):
        hx = hx.lstrip("#")
        return (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), 255)

    img = Image.new("RGBA", (w, h), hex_to_rgba(bg) if bg else (0, 0, 0, 0))
    for (x, y), k in pixels.items():
        if 0 <= x < w and 0 <= y < h:
            img.putpixel((x, y), hex_to_rgba(colors[k]))
    img = img.resize((w * scale, h * scale), Image.NEAREST)
    img.save(path, optimize=True)


def ascii_dump(pixels: dict[tuple[int, int], str], w: int, h: int) -> str:
    lines = []
    for y in range(h):
        lines.append("".join(pixels.get((x, y), ".") for x in range(w)))
    return "\n".join(lines)

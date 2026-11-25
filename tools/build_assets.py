"""
build_assets.py — generates every SVG/PNG asset for the Blaze Eternum profile README.

    /tmp/venv/bin/python build_assets.py

Writes into ../blazeeternum-profile/assets/ :
    banner.svg      hero (matrix ocean + pixel shark + pixel title)
    footer.svg      signature strip (mini shark + status line)
    divider.svg     neon section divider with a swimming pixel fin
    shark.svg       standalone animated mascot (transparent)
    shark-left.svg  mirrored mascot
    shark.png       static 10x PNG export (transparent)
    projects/*      project thumbnails copied from the makeit repo
"""
from __future__ import annotations
import math, os, random, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelkit import (PALETTE, SHARK_W, SHARK_H, build_shark, flip_x, rle_paths, mono_path,
                      text_pixels, write_png, fmt)

HERE = os.path.dirname(os.path.abspath(__file__))
# works both from the dev folder (../blazeeternum-profile) and from <repo>/tools/
if os.path.basename(HERE) == "tools":
    ROOT = os.path.abspath(os.path.join(HERE, ".."))
else:
    ROOT = os.path.abspath(os.path.join(HERE, "..", "blazeeternum-profile"))
ASSETS = os.path.join(ROOT, "assets")
PREVIEW = os.environ.get("PREVIEW_DIR", "/tmp/preview/assets")
RENDER_JS = os.environ.get("RENDER_JS", "/tmp/render/render.js")
os.makedirs(ASSETS, exist_ok=True)
os.makedirs(os.path.join(ASSETS, "projects"), exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)

SHARK = build_shark()

CYAN, BLUE, PURPLE, GREEN, PINK = "#00F7FF", "#008CFF", "#A020F0", "#00FF41", "#FF3CAC"
BLACK, NAVY = "#050510", "#0A1025"
LPURPLE = "#C45CFF"
DIM = "#5FB7C4"
MONO = "Consolas,'Courier New','DejaVu Sans Mono',monospace"

KATA = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン"
RAIN_CHARS = list("0101010101" + "0123456789ABCDEF") + list(KATA)


# --------------------------------------------------------------------------- #
# shared defs
# --------------------------------------------------------------------------- #
def defs(extra: str = "") -> str:
    return f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BLACK}"/><stop offset="1" stop-color="{NAVY}"/>
  </linearGradient>
  <linearGradient id="neon" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="rainG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="0.75" stop-color="{GREEN}" stop-opacity="0.9"/><stop offset="1" stop-color="#CFFFD8"/>
  </linearGradient>
  <linearGradient id="rainC" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.75" stop-color="{CYAN}" stop-opacity="0.9"/><stop offset="1" stop-color="#E0FEFF"/>
  </linearGradient>
  <radialGradient id="sharkGlow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0.35"/><stop offset="0.6" stop-color="{BLUE}" stop-opacity="0.12"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{CYAN}" stroke-opacity="0.07" stroke-width="1"/>
  </pattern>
  <pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse">
    <rect width="3" height="1" fill="#000" fill-opacity="0.16"/>
  </pattern>
  <filter id="glow" x="-20%" y="-60%" width="140%" height="220%">
    <feGaussianBlur stdDeviation="0.7"/>
  </filter>
  <filter id="glowBig" x="-20%" y="-60%" width="140%" height="220%">
    <feGaussianBlur stdDeviation="1.2"/>
  </filter>
  <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="3"/>
  </filter>
  {extra}
</defs>"""


# --------------------------------------------------------------------------- #
# building blocks
# --------------------------------------------------------------------------- #
def rain(width: int, height: int, n: int, seed: int, font_size: int = 14, opacity: float = 0.55,
         cyan_ratio: float = 0.25) -> str:
    rnd = random.Random(seed)
    out = []
    col_w = width / n
    for i in range(n):
        x = int(i * col_w + rnd.uniform(0, col_w * 0.7))
        length = rnd.randint(7, 16)
        chars = "".join(f'<tspan x="{x}" dy="{font_size}">{rnd.choice(RAIN_CHARS)}</tspan>' for _ in range(length))
        dur = rnd.uniform(6, 13)
        begin = -rnd.uniform(0, dur)
        grad = "rainC" if rnd.random() < cyan_ratio else "rainG"
        h_col = length * font_size
        out.append(
            f'<text font-family="{MONO}" font-size="{font_size}" fill="url(#{grad})" opacity="{opacity}" y="0">{chars}'
            f'<animateTransform attributeName="transform" type="translate" from="0 {-h_col}" to="0 {height + font_size}" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></text>')
    return "\n".join(out)


def wave(width: int, height: int, y_base: float, amp: float, period: int, color: str, dur: float,
         phase: float = 0.0, block: int = 6, opacity: float = 1.0, steps: int = 12) -> str:
    """Stepped (pixel) sine wave as a single path, scrolling left in discrete steps."""
    total = width + period
    d = []
    x = 0
    first = True
    while x <= total:
        yy = y_base + amp * math.sin(2 * math.pi * (x / period) + phase)
        yy = round(yy / block) * block
        if first:
            d.append(f"M{x} {yy}")
            first = False
        else:
            d.append(f"V{yy}")
        x += block
        d.append(f"H{x}")
    d.append(f"V{height + 10} H0 Z")
    shift = -period
    vals = ";".join(f"{fmt(shift * i / steps)} 0" for i in range(steps + 1))
    kt = ";".join(fmt(i / steps) for i in range(steps + 1))
    return (f'<path d="{" ".join(d)}" fill="{color}" opacity="{opacity}">'
            f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kt}" '
            f'calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/></path>')


def ptext(text: str, scale: float, x: float, y: float, color: str, glow: str | None = None,
          opacity: float = 1.0, spacing: int = 1, ghost: bool = False) -> tuple[str, float]:
    """Pixel-font text. Returns (svg, rendered width)."""
    pts, w = text_pixels(text, spacing)
    body = mono_path(pts, color)
    layers = []
    if ghost:  # chromatic-aberration ghosts (pink left, purple right)
        layers.append(f'<g transform="translate(-0.45 0)" opacity="0.55">{mono_path(pts, PINK)}</g>')
        layers.append(f'<g transform="translate(0.45 0)" opacity="0.55">{mono_path(pts, PURPLE)}</g>')
    if glow:
        layers.append(f'<g filter="url(#{glow})" opacity="0.9">{body}</g>')
    layers.append(body)
    op = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return (f'<g transform="translate({fmt(x)} {fmt(y)}) scale({fmt(scale)})"{op}>{"".join(layers)}</g>', w * scale)


def cursor(x: float, y: float, scale: float, color: str, dur: float = 1.0) -> str:
    return (f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(4 * scale)}" height="{fmt(7 * scale)}" fill="{color}">'
            f'<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/></rect>')


def shark_group(scale: float, x: float, y: float, bob: bool = True, bubbles: bool = True,
                flip: bool = False, glow: bool = True, bob_dur: float = 2.4) -> str:
    px = flip_x(SHARK, SHARK_W) if flip else SHARK
    base = {p: k for p, k in px.items() if k != "K"}
    nodes = {p: k for p, k in px.items() if k == "K"}
    parts = []
    if glow:
        parts.append(f'<ellipse cx="{SHARK_W / 2}" cy="{SHARK_H / 2 + 1}" rx="{SHARK_W * 0.62}" ry="{SHARK_H * 0.75}" '
                     f'fill="url(#sharkGlow)" shape-rendering="auto"/>')
    parts.append(rle_paths(base, PALETTE))
    parts.append(f'<g>{rle_paths(nodes, PALETTE)}'
                 f'<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></g>')
    # lens scan sweep across the middle lens row (sprite coords after the +1 shift)
    xs = list(range(35, 41))
    if flip:
        xs = [SHARK_W - 1 - v for v in xs][::-1]
    vals = ";".join(str(v) for v in xs) + ";-99;-99"
    kt = ";".join(fmt(i * 0.035) for i in range(len(xs) + 1)) + ";1"
    parts.append(f'<rect x="{xs[0]}" y="13" width="1" height="1" fill="#FFFFFF" opacity="0.95">'
                 f'<animate attributeName="x" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="4s" '
                 f'begin="1s" repeatCount="indefinite"/></rect>')
    if bubbles:
        bx = SHARK_W - 2 if not flip else 1
        sgn = 1 if not flip else -1
        for i, (dx, dur, size) in enumerate(((0, 3.0, 1), (1.5, 3.8, 2), (-1, 4.4, 1))):
            parts.append(
                f'<rect x="{fmt(bx + dx)}" y="12" width="{size}" height="{size}" fill="#9FFDFF" opacity="0">'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;{sgn} -6;{2 * sgn} -14" '
                f'dur="{dur}s" begin="{i * 1.1:.1f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;0.9;0.9;0" keyTimes="0;0.1;0.7;1" dur="{dur}s" '
                f'begin="{i * 1.1:.1f}s" repeatCount="indefinite"/></rect>')
    inner = "\n".join(parts)
    if bob:
        inner = (f'<g>{inner}<animateTransform attributeName="transform" type="translate" '
                 f'values="0 0;0 -1;0 0;0 1;0 1" keyTimes="0;0.25;0.5;0.75;1" calcMode="discrete" '
                 f'dur="{bob_dur}s" repeatCount="indefinite"/></g>')
    return f'<g transform="translate({fmt(x)} {fmt(y)}) scale({fmt(scale)})">{inner}</g>'


def hud_corners(w: int, h: int, size: int = 26, t: int = 3, color: str = CYAN, op: float = 0.7, inset: int = 10) -> str:
    i = inset
    c = []
    for (x, y, sx, sy) in ((i, i, 1, 1), (w - i, i, -1, 1), (i, h - i, 1, -1), (w - i, h - i, -1, -1)):
        hx = x if sx > 0 else x - size
        vy = y if sy > 0 else y - size
        rx = x if sx > 0 else x - t
        ry = y if sy > 0 else y - t
        c.append(f'<rect x="{hx}" y="{ry}" width="{size}" height="{t}" fill="{color}" opacity="{op}"/>')
        c.append(f'<rect x="{rx}" y="{vy}" width="{t}" height="{size}" fill="{color}" opacity="{op}"/>')
    return "".join(c)


def signal_bars(x: float, y: float, scale: float = 2) -> str:
    """5 bars that fill up and reset, like a signal meter."""
    bars = []
    for i in range(5):
        h = (i + 1) * 2
        bars.append(f'<rect x="{fmt(x + i * 4 * scale)}" y="{fmt(y + (10 - h) * scale)}" width="{fmt(3 * scale)}" '
                    f'height="{fmt(h * scale)}" fill="{GREEN}">'
                    f'<animate attributeName="opacity" values="0.15;1;1;0.15" keyTimes="0;{0.15 + i * 0.12:.2f};0.95;1" '
                    f'calcMode="discrete" dur="3s" repeatCount="indefinite"/></rect>')
    return "".join(bars)


def frame(w: int, h: int) -> str:
    return (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="none" stroke="{CYAN}" stroke-opacity="0.45" stroke-width="2"/>'
            f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" fill="none" stroke="{PURPLE}" stroke-opacity="0.25" stroke-width="1"/>')


def svg_open(w: int, h: int, label: str, width_attr: str | None = None) -> str:
    wa = f' width="{width_attr}"' if width_attr else f' width="{w}" height="{h}"'
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"{wa} role="img" '
            f'aria-label="{label}" shape-rendering="crispEdges">\n'
            f'<title>{label}</title>')


# --------------------------------------------------------------------------- #
# banner
# --------------------------------------------------------------------------- #
def build_banner() -> str:
    W, H = 1200, 400
    s = [svg_open(W, H, "Blaze Eternum - pixel cyber shark swimming through the digital ocean"), defs()]
    s.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    s.append(rain(W, H, 30, seed=7, font_size=14, opacity=0.5))
    # ocean floor waves
    s.append(wave(W, H, 352, 9, 240, "#0B1736", 7.2, phase=0.0, opacity=1))
    s.append(wave(W, H, 368, 7, 180, "#101F4A", 5.0, phase=1.7, opacity=1))
    # shark
    s.append(shark_group(7, 52, 96, bob=True, bubbles=True))
    # text block
    tx = 440
    line, w = ptext("> INITIALIZING BLAZE ETERNUM...", 2, tx, 72, GREEN)
    s.append(line)
    s.append(cursor(tx + w + 6, 72, 2, GREEN))
    title, tw = ptext("BLAZE ETERNUM", 7, tx, 104, CYAN, glow="glowBig", ghost=True)
    s.append(title)
    s.append(f'<rect x="{tx}" y="166" width="{fmt(tw)}" height="4" fill="url(#neon)"/>')
    sub, sw = ptext("CYBERSECURITY | CREATIVE TECHNOLOGY", 3, tx, 186, LPURPLE, glow="glow")
    s.append(sub)
    l2, _ = ptext("WELCOME TO MY DIGITAL OCEAN.", 2, tx, 224, PINK, opacity=0.95)
    s.append(l2)
    l3, _ = ptext("EVOLVING ALONGSIDE TECHNOLOGY.", 2, tx, 248, CYAN, opacity=0.8)
    s.append(l3)
    l4, _ = ptext("LAU ZEN HAO  //  MALAYSIA  //  BUILDER > DEFENDER", 2, tx, 290, DIM, opacity=0.9)
    s.append(l4)
    # HUD labels
    hl, _ = ptext("BLAZE_OS v2026.11", 2, 24, 26, DIM, opacity=0.8)
    s.append(hl)
    hr, hw = ptext("SIGNAL", 2, W - 24 - 4 * 10 - 8 - 6 * 12, 26, DIM, opacity=0.8)
    s.append(hr)
    s.append(signal_bars(W - 24 - 5 * 4 * 2 + 2, 22, 2))
    # overlays
    s.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    s.append(f'<rect x="0" y="{H - 4}" width="{W}" height="4" fill="url(#neon)"/>')
    s.append(frame(W, H))
    s.append(hud_corners(W, H))
    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------------------- #
# footer
# --------------------------------------------------------------------------- #
def build_footer() -> str:
    W, H = 1200, 150
    s = [svg_open(W, H, "SYSTEM ONLINE | SHARK MODE ACTIVE | ALWAYS EVOLVING"), defs()]
    s.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    s.append(rain(W, H, 20, seed=42, font_size=12, opacity=0.35))
    s.append(wave(W, H, 126, 5, 200, "#0B1736", 6.5, opacity=1))
    s.append(wave(W, H, 136, 4, 150, "#101F4A", 4.6, phase=2.1, opacity=1))
    s.append(f'<rect x="0" y="0" width="{W}" height="4" fill="url(#neon)"/>')
    s.append(shark_group(3, 40, 30, bob=True, bubbles=True, bob_dur=2.0))
    # status line (three coloured segments)
    x, y, sc = 236, 44, 3
    s.append(f'<rect x="{x - 16}" y="{y + 8}" width="8" height="8" fill="{GREEN}">'
             f'<animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></rect>')
    segs = [("SYSTEM ONLINE", GREEN), (" | ", DIM), ("SHARK MODE ACTIVE", CYAN), (" | ", DIM), ("ALWAYS EVOLVING", LPURPLE)]
    cx = x
    for text, col in segs:
        g, w = ptext(text, sc, cx, y, col, glow="glow" if col != DIM else None)
        s.append(g)
        cx += w + sc  # one pixel gap in font units
    s.append(cursor(cx + 2, y, sc, GREEN))
    l2, _ = ptext("> EVERY SYSTEM HAS A WEAKNESS. EVERY WEAKNESS IS AN OPPORTUNITY TO LEARN.", 2, x, 92, DIM, opacity=0.95)
    s.append(l2)
    l3, _ = ptext("BLAZE ETERNUM // 2026 // BUILDER > DEFENDER", 2, x, 116, DIM, opacity=0.6)
    s.append(l3)
    s.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    s.append(frame(W, H))
    s.append(hud_corners(W, H, size=18, inset=8))
    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------------------- #
# divider
# --------------------------------------------------------------------------- #
def build_divider() -> str:
    W, H = 1200, 20
    s = [svg_open(W, H, "", width_attr="100%"), defs()]
    s.append(f'<rect x="0" y="9" width="{W}" height="2" fill="url(#neon)" opacity="0.8"/>')
    # tick marks
    ticks = "".join(f'<rect x="{x}" y="7" width="2" height="6" fill="{CYAN}" opacity="0.35"/>' for x in range(0, W + 1, 100))
    s.append(ticks)
    # swimming pixel dorsal fin + wake
    fin = {(0, 3): "B", (1, 2): "B", (1, 3): "B", (2, 1): "P", (2, 2): "B", (2, 3): "B", (3, 0): "P", (3, 1): "P", (3, 2): "B", (3, 3): "B", (4, 2): "C", (4, 3): "B"}
    fin_svg = rle_paths(fin, PALETTE, 3, 0, -2)
    wake = f'<rect x="-26" y="8" width="26" height="4" fill="{CYAN}" opacity="0.5"/><rect x="-48" y="9" width="18" height="2" fill="{CYAN}" opacity="0.25"/>'
    s.append(f'<g transform="translate(0 0)">{wake}{fin_svg}'
             f'<animateTransform attributeName="transform" type="translate" from="-40 0" to="{W + 40} 0" dur="9s" repeatCount="indefinite"/></g>')
    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------------------- #
# standalone shark
# --------------------------------------------------------------------------- #
def build_shark_svg(flip: bool = False) -> str:
    W, H = SHARK_W + 2, SHARK_H + 2
    s = [svg_open(W, H, "Blaze Eternum pixel cyber shark mascot", width_attr=None).replace(
        f' width="{W}" height="{H}"', f' width="{W * 8}" height="{H * 8}"'), defs()]
    s.append(shark_group(1, 1, 1, bob=True, bubbles=True, flip=flip, glow=False))
    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def write(name: str, content: str) -> None:
    path = os.path.join(ASSETS, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"wrote {path} ({len(content.encode()) / 1024:.1f} KB)")


def preview(name: str, width: int) -> None:
    """Optional PNG preview via @resvg/resvg-js (skipped when the renderer isn't installed)."""
    if not os.path.exists(RENDER_JS):
        return
    src = os.path.join(ASSETS, name)
    out = os.path.join(PREVIEW, name.replace(".svg", ".png"))
    subprocess.run(["node", RENDER_JS, src, out, str(width)], check=False, capture_output=True)


if __name__ == "__main__":
    write("banner.svg", build_banner())
    write("footer.svg", build_footer())
    write("divider.svg", build_divider())
    write("shark.svg", build_shark_svg())
    write("shark-left.svg", build_shark_svg(flip=True))
    write_png(SHARK, PALETTE, SHARK_W, SHARK_H, 10, os.path.join(ASSETS, "shark.png"))
    print("wrote shark.png")
    # project thumbnails from the makeit repo (only when building from the dev folder)
    src_dir = os.path.join(HERE, "..", "makeit", "portfolio-main", "images")
    if os.path.isdir(src_dir):
        for f in ("themaskguardian.jpg", "SpeakUP_VR.jpg", "Encryptor.png"):
            shutil.copy(os.path.join(src_dir, f), os.path.join(ASSETS, "projects", f))
        print("copied project thumbnails")
    for name, w in (("banner.svg", 1200), ("footer.svg", 1200), ("divider.svg", 1200), ("shark.svg", 384), ("shark-left.svg", 384)):
        preview(name, w)
    print("previews in", PREVIEW)

"""
make_readme.py — fills the pixel-icon data URIs into README.template.md.

    /tmp/venv/bin/python make_readme.py

Reads  ../blazeeternum-profile/README.template.md  (kept out of the final repo)
Writes ../blazeeternum-profile/README.md
Also writes the icon SVGs to ../blazeeternum-profile/assets/icons/ for reference.
"""
from __future__ import annotations
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from icons import build, shields_logo_param  # noqa: E402

if os.path.basename(HERE) == "tools":          # running from <repo>/tools/
    ROOT = os.path.abspath(os.path.join(HERE, ".."))
else:                                           # running from the dev folder
    ROOT = os.path.abspath(os.path.join(HERE, "..", "blazeeternum-profile"))
TEMPLATE = os.path.join(HERE, "README.template.md")
OUT = os.path.join(ROOT, "README.md")
ICON_DIR = os.path.join(ROOT, "assets", "icons")
os.makedirs(ICON_DIR, exist_ok=True)

COLORS = {"csharp": "#FF3CAC", "vscode": "#00F7FF", "capcut": "#00FF41", "linkedin": "#00F7FF",
          "shark": "#00FF41", "shield": "#00FF41", "search": "#00F7FF", "trophy": "#FFD166"}

icons = build(COLORS)
params = {}
for name, svg in icons.items():
    with open(os.path.join(ICON_DIR, f"{name}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    params[f"LOGO_{name.upper()}"] = shields_logo_param(svg)

with open(TEMPLATE, encoding="utf-8") as f:
    tpl = f.read()

missing = set(re.findall(r"{{(\w+)}}", tpl)) - set(params)
if missing:
    sys.exit(f"missing placeholders: {missing}")

out = re.sub(r"{{(\w+)}}", lambda m: params[m.group(1)], tpl)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(out)
print(f"wrote {OUT} ({len(out.encode()) / 1024:.1f} KB), icons: {', '.join(icons)}")
with open(os.path.join(HERE, "icons.json"), "w") as f:
    json.dump(params, f, indent=1)

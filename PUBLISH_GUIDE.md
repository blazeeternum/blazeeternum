# 🦈 Publishing guide — Blaze Eternum profile README

Everything you need is in this folder. The README is plain GitHub-flavored Markdown plus
HTML that GitHub allows; the visuals are hand-built SVG files (no JavaScript, no custom CSS,
no canvas) plus a few live badge/stat services.

```
blazeeternum-profile/
├── README.md                 ← the profile README (ready to copy)
├── PUBLISH_GUIDE.md          ← this file (do not need to upload it)
├── assets/
│   ├── banner.svg            hero: matrix ocean + pixel shark + pixel title (animated)
│   ├── divider.svg           neon section divider with a swimming pixel fin
│   ├── shark.svg             standalone mascot, transparent, animated (bob, glint, bubbles)
│   ├── shark-left.svg        same mascot mirrored (facing left)
│   ├── shark.png             static mascot, transparent, 460×280 (use as avatar, etc.)
│   ├── footer.svg            signature strip: mini shark + SYSTEM ONLINE status line
│   ├── icons/                pixel icons that are embedded inside the badges (reference)
│   ├── projects/             the three project thumbnails (from your makeit repo)
│   └── extra/shark-ai.png    optional AI-generated alternative mascot (transparent)
└── tools/                    Python scripts that regenerate every asset (optional)
```

---

## 1. Publish it

Your profile repository **github.com/blazeeternum/blazeeternum already exists** (it was
created on 24 Nov 2026 and currently holds the previous README with a vector shark banner).
So this is a *replace*, not a *create*. A profile README only needs three things, and you
already have them: repo name equal to your username, public visibility, a `README.md` at the root.

### Option A — Git (recommended)

```bash
# 1. clone your profile repo
git clone https://github.com/blazeeternum/blazeeternum.git
cd blazeeternum

# 2. replace the old README + assets with the new ones
rm -rf README.md assets
cp -r /path/to/blazeeternum-profile/README.md /path/to/blazeeternum-profile/assets .

# 3. ship it
git add -A
git commit -m "Pixel cyber shark profile README"
git push origin main
```

### Option B — GitHub web UI

1. Open <https://github.com/blazeeternum/blazeeternum>.
2. Delete the old `assets` folder and `README.md` (or just overwrite them).
3. **Add file → Upload files**, drag in `README.md` and the whole `assets` folder, commit to `main`.

### Then check

Open <https://github.com/blazeeternum>. The README renders at the top of your profile.
Check it on your phone too (the banner, tables and badges scale down).

> **Images not updating?** GitHub proxies and caches images. If an edited asset still shows
> the old version, append a cache-buster to its URL in `README.md`, e.g.
> `assets/banner.svg?v=2`. Relative paths like `assets/banner.svg` are correct for a profile
> README: GitHub rewrites them to the raw file URL automatically.

---

## 2. What is external (and what happens if it is down)

| Service | Used for | If unavailable |
|:--|:--|:--|
| `readme-typing-svg.demolab.com` | the animated typing line under the banner | the line is simply not shown |
| `img.shields.io` | all badges | badges are not shown |
| `github-readme-stats.vercel.app` | GitHub stats + top-languages cards | cards are not shown |
| `streak-stats.demolab.com` | contribution streak card | card is not shown |
| `github-readme-activity-graph.vercel.app` | contribution activity graph | graph is not shown |

The banner, mascot, dividers, footer and project thumbnails live in your repo, so the page
stays presentable even if every external service is offline. No statistics are hard-coded;
every number comes live from GitHub through those services.

---

## 3. Badges and the pixel icons inside them

shields.io's icon set (simple-icons) no longer ships logos for **C#**, **Visual Studio Code**,
**CapCut (剪映)** and **LinkedIn**, and the old `css3` slug was renamed to `css`. Instead of
showing badges with missing icons, those badges embed tiny **pixel-art icons** drawn for this
README (C#, `<>`, a clapperboard, "in", a shield, a magnifier, a trophy and a mini shark).
They are inlined as `logo=data:image/svg+xml;base64,...` so nothing extra has to be hosted.
The SVG sources are in `assets/icons/` for reference.

To change a badge: edit the `img.shields.io/badge/...` URL in `README.md`.
Syntax: `badge/LABEL-COLOR?style=for-the-badge&logo=SLUG&logoColor=HEX`
(use `_` for spaces, `--` for a literal dash, `%C2%B7` for `·`).

---

## 4. Regenerate or customize the artwork (optional)

Requirements: Python 3.11+, `pip install pillow` (for the PNG export only).
PNG previews additionally use Node + `npm i @resvg/resvg-js`, but they are optional.

```bash
cd tools
python build_assets.py     # rebuilds assets/banner.svg, footer.svg, divider.svg, shark*.svg, shark.png
python make_readme.py      # rebuilds README.md from README.template.md with the inline icons
```

Where things live:

- **Text on the banner / footer** → `tools/build_assets.py`, functions `build_banner()` and
  `build_footer()`. Text is rendered with a 5×7 bitmap font (uppercase A–Z, 0–9 and basic
  punctuation; lowercase is uppercased automatically).
- **The shark sprite** → `tools/pixelkit.py`, function `build_shark()`. The body, fins,
  sunglasses, smile and circuit lines are plain row/column spans on a 46×28 grid, so you can
  reshape it with a text editor. The palette is at the top of the same file.
- **README wording** → `tools/README.template.md` (then run `make_readme.py`), or edit
  `README.md` directly if you do not plan to regenerate it.

Palette used everywhere: `#050510` deep black · `#0A1025` dark navy · `#00F7FF` neon cyan ·
`#008CFF` electric blue · `#A020F0` neon purple · `#00FF41` matrix green · `#FF3CAC` accent pink.

---

## 5. The mascot

- **Primary (hand-built, true pixel art):** `assets/shark.svg` (animated), `assets/shark.png`
  (static, transparent), `assets/shark-left.svg` (mirrored). It is drawn pixel by pixel, so
  edges stay crisp at any size.
- **Alternative (AI-generated):** `assets/extra/shark-ai.png`, generated from the prompt below,
  then snapped to its pixel grid and background-removed. It is more detailed but slightly less
  "clean" than the hand-built sprite. Use whichever you prefer; the README uses the hand-built one.

Prompt used (reuse it in any image generator):

> True 16-bit pixel art sprite of a cute chibi cyber shark mascot, side view facing right,
> swimming. Strict visible square pixel grid, hard edges, no anti-aliasing, no gradients,
> limited palette: electric blue body (#008CFF), neon cyan highlights (#00F7FF), pale cyan
> belly, neon purple fin tips (#A020F0), tiny hot-pink circuit-node accents (#FF3CAC), dark
> navy outline (#0A1025). The shark wears sleek pixel sunglasses with glowing cyan lenses, has
> a small happy smile with two tiny white teeth, a round friendly body, dorsal fin, crescent
> tail, and thin glowing circuit lines on its side like a retro cyberpunk arcade character.
> A few small square pixel bubbles rise beside it. Solid flat deep black background (#050510),
> centered, large sprite filling most of the frame, retro arcade game character style.

Ideas: upload `assets/shark.png` as your GitHub avatar, use it as the favicon of
blazewebsite.dpdns.org, or as the social-preview image of your repos.

---

## 6. Optional upgrade: contribution snake

The classic "snake eating your contributions" animation needs a GitHub Action that runs in
your profile repo and writes the SVG to an `output` branch. Only add the image to the README
**after** the action has run once, otherwise it shows a broken image.

1. In the profile repo create `.github/workflows/snake.yml`:

   ```yaml
   name: generate contribution snake
   on:
     schedule: [{ cron: "0 */12 * * *" }]
     workflow_dispatch:
   permissions: { contents: write }
   jobs:
     generate:
       runs-on: ubuntu-latest
       steps:
         - uses: Platane/snk@v3
           with:
             github_user_name: blazeeternum
             outputs: dist/github-contribution-grid-snake-dark.svg?palette=github-dark&color_snake=#00F7FF
         - uses: crazy-max/ghaction-github-pages@v4
           with: { target_branch: output, build_dir: dist }
           env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
   ```

2. Run it once from the **Actions** tab, then add to the stats section of `README.md`:

   ```html
   <img src="https://raw.githubusercontent.com/blazeeternum/blazeeternum/output/github-contribution-grid-snake-dark.svg" alt="contribution snake" width="100%">
   ```

---

## 7. Housekeeping spotted in your other repo (please fix)

While reading `blazeeternum/makeit` for your details I noticed two things in `index.html`
that are public right now:

1. **A live Discord webhook URL** (around line 504, inside `handleFormSubmit`). Anyone who
   finds it can post messages into that channel. Delete that webhook in Discord
   (*Server Settings → Integrations → Webhooks*), create a new one, and never put the new URL
   in client-side code — route the form through a tiny serverless function or a form service.
2. **Your phone number** (around line 339). Consider removing it from the public page.

Neither of these appears anywhere in the new README.

---

## 8. Pre-push checklist

- [ ] `README.md` and `assets/` copied into the `blazeeternum/blazeeternum` repo
- [ ] Optional: add the encryptor source link in **Project 03** (there is an HTML comment placeholder)
- [ ] Optional: set `assets/shark.png` as your avatar
- [ ] Open <https://github.com/blazeeternum> on desktop *and* mobile and scroll through once

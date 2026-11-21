#!/usr/bin/env python3
"""Render the 20 November 2026 front page: a 1024x1024 poster.

"THE WORLD - Friday 20 November 2026". Six verified stories of the
day in a 2x3 grid, each card with a region tag, a headline and a
one-line deck, plus a small line pictogram. Everything is drawn with
Pillow primitives; no photos, no copied artwork. Deterministic: no
randomness, no timestamps baked in.

Stories (verified in-session against reporting dated 20 Nov 2026):
- Russia strikes Kyiv bridges; two missiles and a drone enter Polish
  airspace; nine killed across Ukraine (Reuters, 20 Nov 08:39 UTC).
- Mexico captures "El Chapo Isidro": FBI Top 10 fugitive Fausto
  Isidro Meza Flores seized in Guasave, Sinaloa, Friday night;
  cartel gunmen answer with burning roadblocks (Reuters / AP).
- Stocks plunge into correction: S&P 500 falls 3.7% to 6,910.39,
  seventh straight loss; Nvidia dives ~14% after Reuters reports
  the SEC is examining its accounting (Reuters, 20 Nov).
- UK and EU seal post-Brexit deals: food trade, linked carbon
  markets and youth mobility agreed at the second EU-UK summit in
  Brussels (20 Nov summit reporting).
- COP31 overruns its deadline: Antalya talks pass their Friday
  close with no deal; the latest draft drops every mention of
  fossil fuels and the $120bn adaptation-finance goal (20 Nov).
- Senate passes permitting bill 62-33: sweeping energy permitting
  overhaul clears the US Senate, heads to the House; the chamber
  also rejects an Iran war-powers resolution 51-48 (Reuters, 20 Nov).
"""
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (250, 246, 238)
NAVY = (18, 38, 66)
GOLD = (198, 158, 40)
INK = (26, 26, 26)
GREY = (88, 88, 88)
RULE = (186, 176, 152)
WHITE = (255, 255, 255)

# (region, accent colour, headline, deck, pictogram)
STORIES = [
    ("UKRAINE & POLAND", (28, 58, 138),
     "RUSSIAN STRIKES HIT KYIV BRIDGES",
     "Nine killed; two missiles and a drone enter Polish airspace",
     "bridge"),
    ("MEXICO", (28, 118, 78),
     "MEXICO CAPTURES \u201cEL CHAPO ISIDRO\u201d",
     "FBI Top 10 fugitive seized in Sinaloa; cartel gunmen burn trucks",
     "shield"),
    ("MARKETS", (138, 58, 18),
     "STOCKS PLUNGE INTO CORRECTION",
     "S&P 500 falls 3.7%; Nvidia dives 14% on SEC probe report",
     "chart"),
    ("EUROPE", (88, 58, 118),
     "UK AND EU SEAL POST-BREXIT DEALS",
     "Food trade, linked carbon markets and youth mobility agreed",
     "clasp"),
    ("CLIMATE", (18, 88, 118),
     "COP31 OVERRUNS ITS DEADLINE",
     "Antalya draft drops fossil-fuel phase-out and $120bn goal",
     "globe"),
    ("UNITED STATES", (118, 38, 38),
     "SENATE PASSES PERMITTING BILL 62\u201333",
     "Sweeping energy overhaul clears the Senate; House vote next",
     "dome"),
]


def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for folder in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts"):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width, limit):
    """Greedy word wrap, capped at `limit` lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > limit:
        print(f"OVERFLOW ({limit} max): {text!r} -> {lines}")
        lines = lines[:limit]
    return lines


def mark(d, kind, x, y, s, color):
    """Small line-art mark in an s x s box at (x, y)."""
    if kind == "bridge":
        d.line([(x, y + 0.72 * s), (x + s, y + 0.72 * s)], fill=color, width=5)
        for fx in (0.15, 0.5, 0.85):
            d.line([(x + fx * s, y + 0.15 * s), (x + fx * s, y + 0.72 * s)],
                   fill=color, width=4)
        d.line([(x, y + 0.15 * s), (x + 0.5 * s, y + 0.72 * s)],
               fill=color, width=3)
        d.line([(x + s, y + 0.15 * s), (x + 0.5 * s, y + 0.72 * s)],
               fill=color, width=3)
    elif kind == "shield":
        d.ellipse([x + 0.2 * s, y + 0.15 * s, x + 0.8 * s, y + 0.75 * s],
                  outline=color, width=5)
        d.polygon([(x + 0.5 * s, y + 0.32 * s), (x + 0.6 * s, y + 0.52 * s),
                   (x + 0.4 * s, y + 0.52 * s)], fill=color)
        d.rectangle([x + 0.43 * s, y + 0.68 * s, x + 0.57 * s, y + 0.88 * s],
                    fill=color)
    elif kind == "chart":
        d.line([(x, y + 0.85 * s), (x + s, y + 0.85 * s)], fill=color, width=4)
        pts = [(x + 0.1 * s, y + 0.25 * s), (x + 0.35 * s, y + 0.45 * s),
               (x + 0.6 * s, y + 0.35 * s), (x + 0.9 * s, y + 0.8 * s)]
        d.line(pts, fill=color, width=5, joint="curve")
        d.polygon([(x + 0.9 * s, y + 0.8 * s), (x + 0.78 * s, y + 0.78 * s),
                   (x + 0.9 * s, y + 0.66 * s)], fill=color)
    elif kind == "clasp":
        d.arc([x + 0.05 * s, y + 0.3 * s, x + 0.5 * s, y + 0.75 * s],
              90, 270, fill=color, width=5)
        d.arc([x + 0.5 * s, y + 0.3 * s, x + 0.95 * s, y + 0.75 * s],
              270, 90, fill=color, width=5)
        d.line([(x + 0.28 * s, y + 0.52 * s), (x + 0.72 * s, y + 0.52 * s)],
               fill=color, width=5)
    elif kind == "globe":
        d.ellipse([x + 0.1 * s, y + 0.1 * s, x + 0.9 * s, y + 0.9 * s],
                  outline=color, width=5)
        d.ellipse([x + 0.35 * s, y + 0.1 * s, x + 0.65 * s, y + 0.9 * s],
                  outline=color, width=3)
        d.line([(x + 0.1 * s, y + 0.5 * s), (x + 0.9 * s, y + 0.5 * s)],
               fill=color, width=3)
    elif kind == "dome":
        d.polygon([(x + 0.5 * s, y + 0.08 * s), (x + 0.78 * s, y + 0.32 * s),
                   (x + 0.22 * s, y + 0.32 * s)], fill=color)
        d.rectangle([x + 0.18 * s, y + 0.32 * s, x + 0.82 * s, y + 0.42 * s],
                    fill=color)
        for fx in (0.25, 0.5, 0.75):
            d.rectangle([x + (fx - 0.05) * s, y + 0.42 * s,
                         x + (fx + 0.05) * s, y + 0.85 * s], fill=color)
        d.rectangle([x + 0.12 * s, y + 0.85 * s, x + 0.88 * s, y + 0.92 * s],
                    fill=color)


def card(d, region, color, head, deck, kind, cx, cy, cw, ch):
    d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                        fill=WHITE, outline=RULE, width=1)
    d.rectangle([cx + 10, cy, cx + cw - 10, cy + 5], fill=color)
    tx = cx + 16
    d.text((tx, cy + 14), region, font=font(True, 13), fill=color)
    # Pictogram, bottom right, clear of the headlines.
    mark(d, kind, cx + cw - 72, cy + ch - 66, 52, color)
    lines = wrap(d, head, font(True, 23), cw - 32, 2)
    hy = cy + 40
    for line in lines:
        d.text((tx, hy), line, font=font(True, 23), fill=INK)
        hy += 27
    deck_lines = wrap(d, deck, font(False, 15), cw - 32, 2)
    dy = hy + 6
    for line in deck_lines:
        d.text((tx, dy), line, font=font(False, 15), fill=GREY)
        dy += 19


def render():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead.
    d.rectangle([0, 0, SIZE, 110], fill=NAVY)
    d.rectangle([0, 110, SIZE, 114], fill=GOLD)
    d.text((24, 57), "THE WORLD", font=font(True, 62), fill=WHITE,
           anchor="lm")
    d.text((1000, 38), "FRIDAY 20 NOVEMBER 2026",
           font=font(True, 26), fill=GOLD, anchor="rm")
    d.text((1000, 76), "THE DAY IN ONE IMAGE",
           font=font(True, 18), fill=WHITE, anchor="rm")
    # Subhead strip.
    d.text((24, 132),
           "SIX STORIES THAT DEFINED THE DAY  \u00b7  FROM KYIV TO SINALOA",
           font=font(True, 16), fill=NAVY)
    d.text((1000, 132), "FULL-DAY EDITION",
           font=font(True, 16), fill=GREY, anchor="ra")
    # 2 x 3 story grid.
    cw, ch, gx, gy = 476, 244, 24, 156
    for i, (region, color, head, deck, kind) in enumerate(STORIES):
        cx = gx + (i % 2) * (cw + 20)
        cy = gy + (i // 2) * (ch + 16)
        card(d, region, color, head, deck, kind, cx, cy, cw, ch)
    # Footer.
    d.rectangle([0, 964, SIZE, SIZE], fill=NAVY)
    d.text((SIZE // 2, 994),
           "FRIDAY 20 NOVEMBER 2026  \u00b7  SIX STORIES  \u00b7  SOURCES: REUTERS, AP",
           font=font(True, 20), fill=WHITE, anchor="mm")
    img.save("entry.png", optimize=True)
    print("wrote entry.png", os.path.getsize("entry.png"), "bytes")
    print("stories:", len(STORIES))


if __name__ == "__main__":
    render()

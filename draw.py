#!/usr/bin/env python3
"""Draw the 20 November 2026 front page: one 1024x1024 poster.

"THE WORLD - Friday 20 November 2026". Six stories, two columns by
three rows, each card with a region tag, a short headline and a
one-line deck, plus a small pictogram drawn with Pillow primitives.

Every story was verified in-session against reporting dated
20 November 2026:
- Russia strikes Kyiv bridges; missiles enter Poland (Reuters,
  20 Nov 08:39 UTC): overnight barrage kills nine across Ukraine,
  damages three Kyiv bridges; two Russian missiles and a
  jet-powered drone enter Polish airspace; Warsaw calls it a
  deliberate provocation.
- Mexico captures "El Chapo Isidro" (Reuters/AP, reported 21 Nov
  of the Friday-night operation): Mexican special forces seize
  Fausto Isidro Meza Flores, an FBI Top 10 fugitive, in Guasave,
  Sinaloa; cartel gunmen answer with burning roadblocks.
- Stocks plunge into correction (Reuters, 20 Nov): S&P 500 falls
  3.7% to 6,910.39, a seventh straight loss; Nvidia dives about
  14% after Reuters reports the SEC is examining its accounting.
- UK and EU seal post-Brexit deals (20 Nov, Brussels summit):
  food trade, linked carbon markets and youth mobility agreed at
  the second EU-UK summit, hosted with PM Burnham.
- COP31 overruns its deadline (Antalya, 20 Nov): the Friday close
  passes with no deal; the latest draft drops every mention of
  fossil fuels and the $120bn adaptation-finance goal.
- Senate passes energy permitting bill 62-33 (Reuters, 20 Nov):
  a sweeping permitting overhaul clears the US Senate and heads
  to the House; the chamber also rejects an Iran war-powers
  resolution 51-48.
Everything is drawn with Pillow primitives; no photos, no copied
artwork. Deterministic: no randomness, no timestamps baked in.
"""
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
GREY = (70, 70, 70)
RULE = (180, 170, 150)
WHITE = (255, 255, 255)

# (region, colour, headline, deck, pictogram)
STORIES = [
    ("UKRAINE & POLAND", (30, 60, 140),
     "RUSSIAN STRIKES HIT KYIV BRIDGES",
     "Nine killed; two missiles and a drone enter Polish airspace",
     "bridge"),
    ("MEXICO", (30, 120, 80),
     "MEXICO CAPTURES \u201cEL CHAPO ISIDRO\u201d",
     "FBI Top 10 fugitive seized in Sinaloa; cartel gunmen burn trucks",
     "badge"),
    ("MARKETS", (140, 60, 20),
     "STOCKS PLUNGE INTO CORRECTION",
     "S&P 500 falls 3.7%; Nvidia dives 14% on SEC probe report",
     "chart"),
    ("EUROPE", (90, 60, 120),
     "UK AND EU SEAL POST-BREXIT DEALS",
     "Food trade, linked carbon markets and youth mobility agreed",
     "handshake"),
    ("CLIMATE", (20, 90, 120),
     "COP31 OVERRUNS ITS DEADLINE",
     "Antalya draft drops fossil-fuel phase-out and $120bn goal",
     "globe"),
    ("UNITED STATES", (120, 40, 40),
     "SENATE PASSES PERMITTING BILL 62\u201333",
     "Sweeping energy overhaul clears the Senate; House vote next",
     "capitol"),
]


def load_font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for folder in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts"):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fit_lines(draw, text, font, width, max_lines):
    """Greedy word wrap, capped at max_lines."""
    out, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    if len(out) > max_lines:
        print(f"OVERFLOW ({max_lines} lines max): {text!r} -> {out}")
        out = out[:max_lines]
    return out


def pictogram(d, kind, x, y, s, color):
    """Small line-art pictogram in a s x s box at (x, y)."""
    if kind == "bridge":
        d.line([(x, y + s * 0.7), (x + s, y + s * 0.7)], fill=color, width=5)
        for fx in (0.15, 0.5, 0.85):
            d.line([(x + s * fx, y + s * 0.15), (x + s * fx, y + s * 0.7)],
                   fill=color, width=4)
        d.line([(x, y + s * 0.15), (x + s * 0.5, y + s * 0.7)], fill=color, width=3)
        d.line([(x + s, y + s * 0.15), (x + s * 0.5, y + s * 0.7)], fill=color, width=3)
    elif kind == "badge":
        d.ellipse([x + s * 0.2, y + s * 0.15, x + s * 0.8, y + s * 0.75],
                  outline=color, width=5)
        d.polygon([(x + s * 0.5, y + s * 0.35), (x + s * 0.62, y + s * 0.55),
                   (x + s * 0.38, y + s * 0.55)], fill=color)
        d.rectangle([x + s * 0.42, y + s * 0.7, x + s * 0.58, y + s * 0.9],
                    fill=color)
    elif kind == "chart":
        d.line([(x, y + s * 0.85), (x + s, y + s * 0.85)], fill=color, width=4)
        pts = [(x + s * 0.1, y + s * 0.25), (x + s * 0.35, y + s * 0.45),
               (x + s * 0.6, y + s * 0.35), (x + s * 0.9, y + s * 0.8)]
        d.line(pts, fill=color, width=5, joint="curve")
        d.polygon([(x + s * 0.9, y + s * 0.8), (x + s * 0.78, y + s * 0.78),
                   (x + s * 0.9, y + s * 0.66)], fill=color)
    elif kind == "handshake":
        d.arc([x + s * 0.05, y + s * 0.3, x + s * 0.5, y + s * 0.75],
              90, 270, fill=color, width=5)
        d.arc([x + s * 0.5, y + s * 0.3, x + s * 0.95, y + s * 0.75],
              270, 90, fill=color, width=5)
        d.line([(x + s * 0.28, y + s * 0.52), (x + s * 0.72, y + s * 0.52)],
               fill=color, width=5)
    elif kind == "globe":
        d.ellipse([x + s * 0.1, y + s * 0.1, x + s * 0.9, y + s * 0.9],
                  outline=color, width=5)
        d.ellipse([x + s * 0.35, y + s * 0.1, x + s * 0.65, y + s * 0.9],
                  outline=color, width=3)
        d.line([(x + s * 0.1, y + s * 0.5), (x + s * 0.9, y + s * 0.5)],
               fill=color, width=3)
    elif kind == "capitol":
        d.polygon([(x + s * 0.5, y + s * 0.08), (x + s * 0.78, y + s * 0.32),
                   (x + s * 0.22, y + s * 0.32)], fill=color)
        d.rectangle([x + s * 0.18, y + s * 0.32, x + s * 0.82, y + s * 0.42],
                    fill=color)
        for fx in (0.25, 0.5, 0.75):
            d.rectangle([x + s * (fx - 0.05), y + s * 0.42,
                         x + s * (fx + 0.05), y + s * 0.85], fill=color)
        d.rectangle([x + s * 0.12, y + s * 0.85, x + s * 0.88, y + s * 0.92],
                    fill=color)


def story_card(d, region, color, head, deck, kind, cx, cy, cw, ch):
    d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                        fill=WHITE, outline=RULE, width=1)
    d.rectangle([cx + 10, cy, cx + cw - 10, cy + 5], fill=color)
    tx = cx + 16
    d.text((tx, cy + 14), region, font=load_font(True, 13), fill=color)
    # Pictogram, bottom right (keeps headlines clear of it).
    pictogram(d, kind, cx + cw - 72, cy + ch - 66, 52, color)
    head_lines = fit_lines(d, head, load_font(True, 24), cw - 32, 2)
    hy = cy + 40
    for line in head_lines:
        d.text((tx, hy), line, font=load_font(True, 24), fill=INK)
        hy += 28
    deck_lines = fit_lines(d, deck, load_font(False, 16), cw - 32, 2)
    dy = hy + 6
    for line in deck_lines:
        d.text((tx, dy), line, font=load_font(False, 16), fill=GREY)
        dy += 20


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead.
    d.rectangle([0, 0, SIZE, 96], fill=NAVY)
    d.rectangle([0, 96, SIZE, 100], fill=GOLD)
    d.text((24, 50), "THE WORLD", font=load_font(True, 58), fill=WHITE,
           anchor="lm")
    d.text((1000, 34), "FRIDAY 20 NOVEMBER 2026",
           font=load_font(True, 26), fill=GOLD, anchor="rm")
    d.text((1000, 68), "THE DAY IN ONE IMAGE",
           font=load_font(True, 18), fill=WHITE, anchor="rm")
    # Dateline strip.
    d.text((24, 118),
           "SIX STORIES THAT DEFINED THE DAY  \u00b7  FROM KYIV TO SINALOA",
           font=load_font(True, 16), fill=NAVY)
    d.text((1000, 118), "FULL-DAY EDITION",
           font=load_font(True, 16), fill=GREY, anchor="ra")
    # 2 x 3 story grid.
    cw, ch, gx, gy = 478, 246, 24, 148
    for i, (region, color, head, deck, kind) in enumerate(STORIES):
        cx = gx + (i % 2) * (cw + 20)
        cy = gy + (i // 2) * (ch + 16)
        story_card(d, region, color, head, deck, kind, cx, cy, cw, ch)
    # Footer.
    d.rectangle([0, 966, SIZE, SIZE], fill=NAVY)
    d.text((SIZE // 2, 995),
           "FRIDAY 20 NOVEMBER 2026  \u00b7  SIX STORIES  \u00b7  SOURCES: REUTERS, AP",
           font=load_font(True, 20), fill=WHITE, anchor="mm")
    img.save("entry.png", optimize=True)
    print("wrote entry.png", os.path.getsize("entry.png"), "bytes")
    print("stories:", len(STORIES))


if __name__ == "__main__":
    build()

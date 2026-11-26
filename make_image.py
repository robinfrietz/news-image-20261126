"""Draw entry.png: the world news of Thursday 26 November 2026 in one image.

A clean 1024x1024 infographic built with Pillow only: a big date header,
six story cards (region tag, key number, headline, one-line detail, simple
drawn icon) and an "also today" ticker. Text is kept short and large so the
image stays readable when shrunk to 300px wide.

Run:  python3 make_image.py   ->  writes entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (11, 18, 38)            # deep navy
PANEL = (244, 246, 251)      # near-white card
INK = (18, 24, 43)           # card text
MUTED = (74, 85, 110)        # card detail text
WHITE = (255, 255, 255)
SOFT = (168, 182, 214)       # header secondary text

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap by pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, kind, cx, cy, r, color):
    """Tiny geometric icons, drawn with plain shapes."""
    if kind == "storm":  # cloud + rain
        d.ellipse([cx - r, cy - r * 0.55, cx + r * 0.1, cy + r * 0.35], fill=color)
        d.ellipse([cx - r * 0.35, cy - r * 0.8, cx + r * 0.75, cy + r * 0.35], fill=color)
        d.rectangle([cx - r, cy - r * 0.1, cx + r * 0.75, cy + r * 0.35], fill=color)
        for dx in (-0.55, -0.05, 0.45):
            d.line([cx + dx * r, cy + r * 0.55, cx + dx * r - r * 0.18, cy + r * 0.95],
                   fill=color, width=4)
    elif kind == "tag":  # price tag with %
        d.polygon([(cx - r * 0.8, cy - r * 0.45), (cx + r * 0.25, cy - r * 0.45),
                   (cx + r * 0.85, cy + r * 0.15), (cx + r * 0.25, cy + r * 0.8),
                   (cx - r * 0.8, cy + r * 0.8)], fill=color)
        d.ellipse([cx - r * 0.58, cy - r * 0.22, cx - r * 0.3, cy + r * 0.06], fill=PANEL)
        d.line([cx - r * 0.15, cy + r * 0.55, cx + r * 0.45, cy - r * 0.25], fill=PANEL, width=4)
    elif kind == "flame":
        d.polygon([(cx, cy - r), (cx + r * 0.62, cy + r * 0.1), (cx + r * 0.45, cy + r * 0.75),
                   (cx - r * 0.45, cy + r * 0.75), (cx - r * 0.62, cy + r * 0.1)], fill=color)
        d.polygon([(cx, cy - r * 0.25), (cx + r * 0.3, cy + r * 0.35), (cx + r * 0.18, cy + r * 0.75),
                   (cx - r * 0.18, cy + r * 0.75), (cx - r * 0.3, cy + r * 0.35)], fill=(255, 214, 90))
    elif kind == "atom":
        d.ellipse([cx - r * 0.16, cy - r * 0.16, cx + r * 0.16, cy + r * 0.16], fill=color)
        for ang in (0, 60, 120):
            d.ellipse([cx - r, cy - r * 0.38, cx + r, cy + r * 0.38], outline=color, width=3)
            # rotate by redrawing is overkill; two crossing ellipses read as an atom
            break
        d.ellipse([cx - r * 0.38, cy - r, cx + r * 0.38, cy + r], outline=color, width=3)
    elif kind == "chart":
        base = cy + r * 0.8
        for i, hgt in enumerate((0.5, 0.9, 1.35)):
            x0 = cx - r * 0.85 + i * r * 0.62
            d.rectangle([x0, base - hgt * r, x0 + r * 0.42, base], fill=color)
        d.line([cx - r, base, cx + r, base], fill=color, width=4)
    elif kind == "satellite":
        d.rectangle([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28], fill=color)
        d.rectangle([cx - r * 1.0, cy - r * 0.18, cx - r * 0.38, cy + r * 0.18], fill=color)
        d.rectangle([cx + r * 0.38, cy - r * 0.18, cx + r * 1.0, cy + r * 0.18], fill=color)
        d.line([cx, cy + r * 0.28, cx, cy + r * 0.6], fill=color, width=3)
        d.ellipse([cx - r * 0.12, cy + r * 0.55, cx + r * 0.12, cy + r * 0.8], fill=color)


STORIES = [
    # tag, stat, headline, detail, color, icon
    ("USA · WEATHER", "100th",
     "Storm postpones Macy's 100th Parade",
     "First move in 100 years: parade shifts to Saturday. "
     "81.5M travellers hit; 100k+ lose power.",
     (38, 102, 184), "storm"),
    ("GLOBAL TRADE", "14",
     "US proposes new tariffs on 14 trading partners",
     "China 20%, EU 15%, Vietnam up to 35% over factory "
     "overcapacity. Comments due 5 January.",
     (184, 96, 20), "tag"),
    ("EUROPE · WAR", "113",
     "Russia hits Kyiv with missiles and 113 drones",
     "Overnight strikes hit a shopping centre; 7 wounded. "
     "Moscow says drone sites were targeted.",
     (172, 44, 44), "flame"),
    ("ASIA · SECURITY", "NUCLEAR",
     "Kim Jong Un vows more nuclear weapons",
     "Tours uranium plants; tactical nukes across domains "
     "'urgent'. Nuclear status 'irreversible'.",
     (92, 52, 168), "atom"),
    ("US ECONOMY", "8 of 12",
     "Fed Beige Book: growth holds, prices stay sticky",
     "Inflation 3.8%, Q3 GDP revised to 4.3%. "
     "Next rate decision due 8-9 December.",
     (20, 120, 92), "chart"),
    ("SPACE · TECH", "1M",
     "SpaceX cleared for 1 million satellites",
     "FCC approves 'Starmind' orbital AI data centres. First satellite "
     "due by 2033, full constellation by 2040.",
     (24, 130, 170), "satellite"),
]

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- header ---------------------------------------------------------------
d.text((48, 34), "THURSDAY · WORLD NEWS IN ONE IMAGE", font=font(BOLD, 25), fill=SOFT)
d.text((44, 66), "26 NOVEMBER 2026", font=font(BOLD, 72), fill=WHITE)
d.text((48, 152), "Thanksgiving Day in the USA - US markets closed",
       font=font(REG, 26), fill=(255, 196, 110))

# --- story cards: 2 columns x 3 rows --------------------------------------
MARGIN, GAP = 32, 16
CARD_W = (W - 2 * MARGIN - GAP) // 2          # 472
CARD_H = 216
TOP = 200

for i, (tag, stat, headline, detail, color, icon) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x0 = MARGIN + col * (CARD_W + GAP)
    y0 = TOP + row * (CARD_H + GAP)
    x1, y1 = x0 + CARD_W, y0 + CARD_H
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=PANEL)
    # coloured tag strip
    d.rounded_rectangle([x0, y0, x1, y0 + 46], radius=18, fill=color)
    d.rectangle([x0, y0 + 28, x1, y0 + 46], fill=color)
    d.text((x0 + 20, y0 + 10), tag, font=font(BOLD, 21), fill=WHITE)
    sf = font(BOLD, 30)
    d.text((x1 - 20 - d.textlength(stat, font=sf), y0 + 7), stat, font=sf, fill=WHITE)
    # headline + detail, leaving room for the icon at bottom-right
    text_w = CARD_W - 40
    y = y0 + 60
    for line in wrap(d, headline, font(BOLD, 27), text_w):
        d.text((x0 + 20, y), line, font=font(BOLD, 27), fill=INK)
        y += 33
    y += 4
    for line in wrap(d, detail, font(REG, 20), text_w - 70)[:3]:
        d.text((x0 + 20, y), line, font=font(REG, 20), fill=MUTED)
        y += 25
    draw_icon(d, icon, x1 - 52, y1 - 48, 30, color)

# --- footer ticker ----------------------------------------------------------
fy = TOP + 3 * (CARD_H + GAP) + 8
d.text((48, fy), "ALSO TODAY", font=font(BOLD, 22), fill=(255, 196, 110))
ticker = ("Israeli strikes kill 9 in Gaza  ·  Fuel tanker fire near Cairo kills 31  ·  "
          "Houthis strike Jizan Port in Saudi Arabia")
y = fy + 32
for line in wrap(d, ticker, font(REG, 21), W - 96):
    d.text((48, y), line, font=font(REG, 21), fill=WHITE)
    y += 28
d.text((48, y + 2), "Sources: Reuters, AP, Federal Reserve, FCC, NWS - reported 25-26 Nov 2026",
       font=font(REG, 16), fill=SOFT)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)

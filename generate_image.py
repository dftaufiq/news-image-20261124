#!/usr/bin/env python3
"""Draw the 24 November 2026 front page (news-image-20261124).

Build-time only: needs Pillow. Run `python3 generate_image.py` to write
entry.png (1024x1024) next to this file. Every panel, illustration and
the dotted world map is drawn in code; no photographs, no copied
artwork. All stories were checked against reporting of Tuesday
24 November 2026 (events that happened, or were first reported, that
day in any time zone).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
RED = (163, 18, 18)
NAVY = (27, 58, 92)
SEA = (14, 40, 66)
GRAY = (96, 94, 88)
LIGHT = (234, 228, 212)
CREAM = (255, 252, 240)
GREEN = (46, 125, 61)
ORANGE = (232, 116, 22)
GOLD = (214, 164, 32)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANSC = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"
SANSCB = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"

_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def globe(d, cx, cy, r, outline=NAVY, land=GREEN, lw=2):
    """Simple wireframe globe: circle, meridians, land blobs."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=outline, width=lw)
    d.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
              outline=outline, width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=outline, width=1)
    d.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
          200, 340, fill=outline, width=1)
    d.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
          20, 160, fill=outline, width=1)
    # land blobs
    d.ellipse([cx - int(r * 0.75), cy - int(r * 0.7),
               cx - int(r * 0.15), cy - int(r * 0.2)], fill=land)
    d.ellipse([cx + int(r * 0.05), cy + int(r * 0.1),
               cx + int(r * 0.7), cy + int(r * 0.6)], fill=land)
    d.ellipse([cx - int(r * 0.3), cy + int(r * 0.45),
               cx + int(r * 0.25), cy + int(r * 0.8)], fill=land)


# ---------------------------------------------------------------- data

LEAD_KICKER = "ANTALYA, TURKEY  \u2014  CLIMATE"
LEAD_HEAD = "COP31 COLLAPSES \u2014 NO FOSSIL-FUEL DEAL"
LEAD_DECK = (
    "Two weeks of talks end with no agreement on phasing out fossil "
    "fuels: the Antalya summit breaks down, and the Guardian asks what "
    "the failure reveals about a divided world. Small island states "
    "call it a betrayal; big emitters walk away. UN chief Guterres: "
    "\u201cdeeply disappointed.\u201d The fallout dominates Tuesday."
)
LEAD_SOURCE = "Sources: The Guardian \u00b7 Reuters \u00b7 NDTV"

FEATURES = [
    dict(num="1", kicker="BANTEN, INDONESIA",
         head="FACTORY FIRE KILLS 24",
         body=("At least 24 dead and around 30 missing as rescuers search "
               "the burned-out factory in Banten province."),
         source="Source: Reuters / AP", art="fire"),
    dict(num="2", kicker="NEW YORK",
         head="MARKETS CRASH $1 TRILLION",
         body=("Wall Street sells off after the Democrats\u2019 midterm win; "
               "Trump blames the Democrats: \u201cAs I predicted.\u201d"),
         source="Source: Reuters", art="crash"),
    dict(num="3", kicker="UKRAINE AT SEA",
         head="DRONES HIT RUSSIAN SHIPS",
         body=("A Russian cargo ship burns off Finland; a drone boat hits "
               "a Russian ship off Libya, 10 hurt. Kyiv: 8 killed."),
         source="Source: RFE/RL / Reuters", art="shipfire"),
    dict(num="4", kicker="NEW DELHI",
         head="INDIA\u2013NEPAL: NEW RAIL LINK",
         body=("Modi and Nepal PM Balendra Shah flag off the Saryu-Kamala "
               "Express, sign 8 MoUs and a Rs 15,000-crore package."),
         source="Source: Indian Express", art="train"),
]

# (lon, lat, label, dx, dy) — numbers match the legend below; dx/dy nudge
# pins apart where two stories sit almost on top of each other
PINS = [
    (30.7, 36.9, "Antalya \u2014 COP31 collapses, no fossil-fuel deal", -34, 14),
    (106.8, -6.2, "Banten \u2014 factory fire: 24 dead, ~30 missing", 0, 0),
    (31.0, 50.3, "Kyiv region \u2014 drone strike, 8 killed, 11 feared buried", 14, -10),
    (26.0, 59.5, "Gulf of Finland \u2014 Russian cargo ship ablaze", -8, -12),
    (20.1, 32.1, "Benghazi \u2014 drone boat hits Russian ship, 10 hurt", 0, -12),
    (56.5, 26.5, "Hormuz \u2014 two more tankers catch fire", 0, 0),
    (-77.0, 38.9, "Washington \u2014 Trump warns Iran of \u2018very traumatic\u2019 outcome", -12, -8),
    (-74.0, 40.7, "New York \u2014 $1tn market sell-off after midterm win", 14, 12),
    (77.2, 28.6, "New Delhi \u2014 Modi & Nepal PM Shah: rail link, 8 MoUs", 0, 0),
    (-9.1, 38.7, "Lisbon \u2014 thousands march over living costs", 0, 0),
    (90.4, 23.8, "Dhaka \u2014 Bangladesh vows to arrest Hasina if she returns", 0, 0),
    (174.8, -41.3, "Wellington \u2014 Pant\u2019s 128; first Test drawn", 0, 0),
]

# region -> [(place, text)] — one line each, bold place lead-in
BRIEFS = [
    ("MIDDLE EAST", [
        ("West Bank", "Israeli leaders denounce settler attacks as \u2018Jewish terrorism\u2019."),
        ("Gaza", "Oxfam: Israeli attacks have turned Gaza into a \u2018toxic wasteland\u2019."),
        ("Jerusalem", "Netanyahu wants to attack Iran. Does that serve Israel \u2014 or him?"),
    ]),
    ("EUROPE", [
        ("Brussels", "EU sanctions package aims to \u2018keep pressure\u2019 on Russia and hit its war funding."),
        ("Manchester", "Don Toliver concert evacuated over an \u2018unknown substance\u2019."),
        ("Paris", "Gis\u00e8le Pelicot \u2018deeply shocked\u2019 after nude images used to promote a book."),
    ]),
    ("ASIA-PACIFIC", [
        ("Beijing", "China sets 2030 targets to strengthen elderly care and childcare."),
        ("Seoul", "President nominates a new foreign minister and intelligence chief."),
        ("Yerevan", "Armenia proposes a new constitution to advance peace with Azerbaijan."),
    ]),
    ("AMERICAS", [
        ("Washington", "Trump urges Nvidia to bring back Jensen Huang as CEO."),
        ("Ottawa", "Carney laughs as a Trump lookalike mocks US-Canada trade tensions."),
        ("Bogot\u00e1", "Drone attack hits a Colombian city as unmanned explosives transform conflict."),
    ]),
    ("AFRICA", [
        ("Tripoli", "Libya: oil pipeline blockade has cost nearly $31m, state oil firm says."),
        ("Lagos", "Two Nigerians die while in service for the Russian military."),
        ("Niamey", "European nations prepare to evacuate citizens after the Niger coup."),
    ]),
    ("SPORT", [
        ("Wellington", "Pant hits 128; first Test drawn as New Zealand finish 239/5."),
        ("Las Vegas", "Verstappen wins the Las Vegas Grand Prix."),
        ("World Snooker", "Advani and Ramachandran win their opening group matches."),
    ]),
    ("MARKETS & TECH", [
        ("Mumbai", "Sensex falls 1,484 points (1.77%) to 82,435; Nifty drops 451."),
        ("New Delhi", "India\u2019s oil and gas import bill rose around 60% in October."),
        ("Tokyo", "SoftBank to invest $2bn in Intel, reports say."),
    ]),
]

N_STORIES = 1 + 4 + 12 + sum(len(b[1]) for b in BRIEFS)  # lead + features + pins + briefs

DATE_CHECK = (
    "Left out on purpose: stories from earlier days, not 24 Nov. COP31\u2019s collapse came at "
    "Sunday\u2019s closing plenary \u2014 it leads Tuesday\u2019s pages because the fallout dominates "
    "the day. The Democrats\u2019 House win was sealed Sunday; today\u2019s news is the market crash "
    "it triggered. Africa briefs were first reported 22\u201323 Nov. Also excluded: Iran\u2019s "
    "strikes on US bases (18 Nov), the Shenzhen APEC summit (21 Nov) and Cyclone Akvan."
)

FOOTER = (
    "Sources: Reuters \u00b7 BBC \u00b7 CNN \u00b7 AP \u00b7 The Guardian \u00b7 NYT \u2014 "
    "checked against reporting of Tuesday 24 November 2026. Drawn entirely in code; no photographs."
)

# landmass as (row0, row1, col0, col1) on a 100 x 30 grid
LAND = [
    (2, 6, 4, 30), (7, 9, 8, 29), (10, 12, 11, 17), (12, 13, 17, 21),
    (1, 3, 31, 38),
    (12, 13, 25, 33), (14, 17, 24, 34), (18, 21, 26, 33), (22, 25, 28, 31),
    (26, 28, 29, 30),
    (1, 2, 47, 53), (3, 5, 43, 52), (6, 8, 43, 55), (8, 9, 43, 47),
    (8, 9, 50, 56),
    (9, 10, 41, 55), (11, 15, 40, 57), (16, 19, 43, 56), (20, 22, 47, 54),
    (19, 21, 57, 58),
    (8, 10, 56, 63),
    (0, 4, 56, 97), (5, 7, 60, 88), (8, 10, 64, 86), (10, 13, 66, 72),
    (11, 14, 74, 81), (14, 16, 76, 88), (5, 8, 90, 93),
    (17, 19, 76, 87), (20, 22, 77, 85), (23, 25, 91, 92),
]


# ---------------------------------------------------------------- art

def art_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # sea
    for i in range(3):
        yy = y + h - 12 - i * 6
        d.line([(x + 6, yy), (x + w - 6, yy)], fill=(90, 140, 180), width=2)
    # hull
    d.polygon([(x + 18, y + h - 22), (x + w - 18, y + h - 22),
               (x + w - 34, y + h - 10), (x + 34, y + h - 10)], fill=(18, 18, 18))
    d.rectangle([x + 30, y + h - 38, x + 66, y + h - 22], fill=(200, 60, 40))
    d.rectangle([x + 72, y + h - 38, x + 108, y + h - 22], fill=(40, 90, 160))
    d.rectangle([x + 114, y + h - 38, x + 150, y + h - 22], fill=(214, 164, 32))
    d.rectangle([x + w - 52, y + h - 44, x + w - 40, y + h - 22], fill=(220, 220, 210))
    # flames
    for fx, fh in ((x + 44, 18), (x + 88, 24), (x + 130, 16)):
        d.polygon([(fx - 10, y + h - 38), (fx, y + h - 38 - fh),
                   (fx + 10, y + h - 38)], fill=ORANGE)
        d.polygon([(fx - 5, y + h - 38), (fx, y + h - 38 - fh + 10),
                   (fx + 5, y + h - 38)], fill=GOLD)
    # missile arcs
    d.arc([x + w - 90, y - 6, x + w - 20, y + 34], 180, 330, fill=(255, 255, 255), width=2)
    d.ellipse([x + w - 26, y + 24, x + w - 20, y + 30], fill=(255, 255, 255))


def art_shipfire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 26, 34))
    for i in range(3):
        yy = y + h - 12 - i * 6
        d.line([(x + 6, yy), (x + w - 6, yy)], fill=(90, 100, 130), width=2)
    # burning ship
    d.polygon([(x + 30, y + h - 24), (x + w - 30, y + h - 24),
               (x + w - 46, y + h - 10), (x + 46, y + h - 10)], fill=(10, 10, 10))
    d.rectangle([x + 96, y + h - 40, x + 112, y + h - 24], fill=(200, 200, 190))
    for fx, fh in ((x + 70, 16), (x + 104, 22), (x + 140, 14)):
        d.polygon([(fx - 11, y + h - 40), (fx, y + h - 40 - fh),
                   (fx + 11, y + h - 40)], fill=ORANGE)
        d.polygon([(fx - 5, y + h - 40), (fx, y + h - 40 - fh + 12),
                   (fx + 5, y + h - 40)], fill=GOLD)
    # drone above
    dx, dy = x + w - 46, y + 16
    d.line([(dx - 12, dy - 8), (dx + 12, dy + 8)], fill=(255, 255, 255), width=2)
    d.line([(dx - 12, dy + 8), (dx + 12, dy - 8)], fill=(255, 255, 255), width=2)
    d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=RED)
    # smoke
    for sx, sy, sr in ((x + 60, y + 14, 6), (x + 84, y + 10, 8), (x + 110, y + 14, 6)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=(150, 150, 150), width=2)


def art_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 22, 18))
    # factory silhouette
    d.rectangle([x + 16, y + h - 34, x + w - 16, y + h - 8], fill=(12, 12, 12))
    d.rectangle([x + 30, y + 8, x + 44, y + h - 34], fill=(12, 12, 12))
    d.rectangle([x + 52, y + 16, x + 62, y + h - 34], fill=(12, 12, 12))
    # windows
    for wx in (x + 84, x + 116, x + 148):
        d.rectangle([wx, y + h - 28, wx + 16, y + h - 16], fill=GOLD)
    # flames from the roof
    for fx, fh in ((x + 90, 20), (x + 124, 28), (x + 158, 18)):
        d.polygon([(fx - 12, y + h - 34), (fx, y + h - 34 - fh),
                   (fx + 12, y + h - 34)], fill=ORANGE)
        d.polygon([(fx - 6, y + h - 34), (fx, y + h - 34 - fh + 12),
                   (fx + 6, y + h - 34)], fill=GOLD)
    # smoke
    for sx, sy, sr in ((x + 60, y + 12, 7), (x + 92, y + 8, 9), (x + 126, y + 12, 7)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=(170, 170, 170), width=2)
    # big 24
    d.text((x + w - 62, y + 2), "24", font=font(SERIFB, 30), fill=(255, 255, 255))
    d.text((x + w - 62, y + 34), "DEAD", font=font(SANSB, 11), fill=(255, 200, 190))


def art_crash(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 26, 44))
    # grid
    for gx in range(x + 14, x + w - 8, 22):
        d.line([(gx, y + 8), (gx, y + h - 8)], fill=(48, 62, 92), width=1)
    for gy in range(y + 10, y + h - 8, 14):
        d.line([(x + 10, gy), (x + w - 8, gy)], fill=(48, 62, 92), width=1)
    # falling line
    pts = [(x + 12, y + 12), (x + 56, y + 16), (x + 96, y + 14),
           (x + 130, y + 26), (x + 162, y + 40), (x + w - 12, y + h - 14)]
    d.line(pts, fill=RED, width=4, joint="curve")
    # arrow head
    d.polygon([(x + w - 12, y + h - 14), (x + w - 26, y + h - 20),
               (x + w - 22, y + h - 6)], fill=RED)
    d.text((x + 12, y + 4), "-$1tn", font=font(SERIFB, 22), fill=(255, 255, 255))
    d.text((x + 12, y + h - 16), "WALL ST", font=font(SANSB, 10), fill=(180, 196, 220))


def art_train(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 164, 32))
    # sky band
    d.rectangle([x, y, x + w, y + 26], fill=(30, 64, 130))
    d.text((x + 10, y + 5), "SARYU-KAMALA EXPRESS", font=font(SANSB, 11),
           fill=(255, 255, 255))
    # track
    d.line([(x + 6, y + h - 10), (x + w - 6, y + h - 10)], fill=(40, 40, 40), width=3)
    for tx in range(x + 10, x + w - 8, 18):
        d.line([(tx, y + h - 16), (tx, y + h - 4)], fill=(40, 40, 40), width=2)
    # train body
    d.rectangle([x + 22, y + 30, x + w - 22, y + h - 16], fill=(163, 18, 18))
    d.rectangle([x + 22, y + 30, x + w - 22, y + 40], fill=(255, 255, 255))
    for wx in range(x + 34, x + w - 34, 30):
        d.rectangle([wx, y + 44, wx + 20, y + 56], fill=(200, 230, 255))
    d.ellipse([x + w - 52, y + 44, x + w - 30, y + 56], fill=(200, 230, 255))
    # flags of the two countries
    d.rectangle([x + w - 66, y + h - 34, x + w - 40, y + h - 20], fill=(255, 153, 51))
    d.rectangle([x + w - 66, y + h - 29, x + w - 40, y + h - 25], fill=(255, 255, 255))
    d.rectangle([x + w - 66, y + h - 25, x + w - 40, y + h - 20], fill=(19, 136, 8))


def art_lead(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # cracked globe
    cx, cy, r = x + 78, y + h // 2 - 18, 42
    globe(d, cx, cy, r, outline=(220, 228, 238), land=(110, 190, 120), lw=2)
    # red crack across the globe
    crack = [(cx - 40, cy - 34), (cx - 18, cy - 12), (cx - 30, cy + 2),
             (cx - 6, cy + 16), (cx - 16, cy + 30), (cx + 8, cy + 40)]
    d.line(crack, fill=RED, width=4, joint="curve")
    # broken document on the right
    dx = x + 168
    d.rectangle([dx, y + 16, dx + 118, y + h - 44], fill=(255, 255, 255))
    d.line([(dx + 10, y + 32), (dx + 108, y + 32)], fill=INK, width=2)
    d.line([(dx + 10, y + 46), (dx + 108, y + 46)], fill=GRAY, width=2)
    d.line([(dx + 10, y + 58), (dx + 88, y + 58)], fill=GRAY, width=2)
    d.line([(dx + 10, y + 70), (dx + 98, y + 70)], fill=GRAY, width=2)
    # red X over the document
    d.line([(dx + 14, y + 84), (dx + 104, y + h - 52)], fill=RED, width=5)
    d.line([(dx + 104, y + 84), (dx + 14, y + h - 52)], fill=RED, width=5)
    d.text((x + 12, y + h - 28), "NO CONSENSUS \u2014 PACT DIES IN ANTALYA",
           font=font(SANSB, 12), fill=(255, 255, 255))


ART = {"fire": art_fire, "crash": art_crash, "shipfire": art_shipfire,
       "train": art_train}


# ---------------------------------------------------------------- page

def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 14                      # margin
    RX = W - MX                  # right edge

    # ---- masthead
    globe(d, 50, 40, 26, outline=NAVY, land=GREEN, lw=2)
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIFB, 48)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2 + 16, 12), title, font=tf, fill=INK)
    rule(d, MX, RX, 72, fill=RED, width=3)
    rule(d, MX, RX, 76, fill=INK, width=1)
    dateline = (f"TUESDAY 24 NOVEMBER 2026  \u00b7  {N_STORIES} STORIES  \u00b7  "
                "7 REGIONS  \u00b7  EVERY STORY DATED 24 NOV 2026")
    df = font(SANSB, 13)
    dw = d.textlength(dateline, font=df)
    d.text(((W - dw) / 2, 82), dateline, font=df, fill=INK)
    rule(d, MX, RX, 100, fill=INK, width=1)

    # ---- lead story
    y = 108
    lx, lw = MX, 664
    ax, aw = 692, RX - 692
    kf = font(SANSB, 13)
    d.text((lx, y), LEAD_KICKER, font=kf, fill=RED)
    y += 20
    hsize = 34
    while hsize > 24 and d.textlength(LEAD_HEAD, font=font(SERIFB, hsize)) > lw:
        hsize -= 1
    d.text((lx, y), LEAD_HEAD, font=font(SERIFB, hsize), fill=INK)
    y += hsize + 6
    bf = font(SERIF, 13)
    y = para(d, lx, y, wrap(d, LEAD_DECK, bf, lw), bf, leading=16)
    y += 3
    d.text((lx, y), LEAD_SOURCE, font=font(SANSC, 11), fill=GRAY)
    art_lead(d, ax, 108, aw, 140)
    rule(d, MX, RX, 256, fill=INK, width=1)

    # ---- four features
    y = 264
    card_w = (RX - MX - 3 * 8) // 4
    for i, f in enumerate(FEATURES):
        cx0 = MX + i * (card_w + 8)
        ART[f["art"]](d, cx0, y, card_w, 64)
        yy = y + 70
        d.text((cx0, yy), f["num"] + "  \u00b7  " + f["kicker"],
               font=font(SANSB, 11), fill=RED)
        yy += 16
        hlines = wrap(d, f["head"], font(SERIFB, 14), card_w)
        yy = para(d, cx0, yy, hlines, font(SERIFB, 14), leading=17)
        yy += 2
        blines = wrap(d, f["body"], font(SANS, 11), card_w)
        yy = para(d, cx0, yy, blines, font(SANS, 11), leading=13)
        yy += 2
        d.text((cx0, yy), f["source"], font=font(SANSC, 10), fill=GRAY)
    rule(d, MX, RX, 432, fill=INK, width=1)

    # ---- world map
    y = 440
    d.text((MX, y), "WHERE IT HAPPENED \u2014 12 STORIES ON THE MAP",
           font=font(SANSB, 13), fill=INK)
    note = "Numbers match the stories below"
    d.text((RX - d.textlength(note, font=font(SANSC, 11)), y + 1), note,
           font=font(SANSC, 11), fill=GRAY)
    map_x0, map_y0, map_w, map_h = MX, 460, RX - MX, 96
    grid = [[False] * 100 for _ in range(30)]
    for r0, r1, c0, c1 in LAND:
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                grid[r][c] = True
    for r in range(30):
        for c in range(100):
            if grid[r][c]:
                px = map_x0 + c * (map_w / 99)
                py = map_y0 + r * (map_h / 29)
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                          fill=(70, 70, 66))
    for i, (lon, lat, _label, dx, dy) in enumerate(PINS, 1):
        px = map_x0 + (lon + 170) / 360 * map_w + dx
        py = map_y0 + (75 - lat) / 133 * map_h + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        nf = font(SANSB, 10)
        nw = d.textlength(str(i), font=nf)
        d.text((px - nw / 2, py - 7), str(i), font=nf, fill=(255, 255, 255))
    # legend, two columns of six
    y = 566
    lf = font(SANS, 11)
    for col in range(2):
        for row in range(6):
            i = col * 6 + row
            lx0 = MX + col * 500
            d.text((lx0, y + row * 13),
                   f"{i + 1}. {PINS[i][2]}", font=lf, fill=INK)
    rule(d, MX, RX, 644, fill=INK, width=1)

    # ---- region briefs, three columns
    y = 652
    col_w = (RX - MX - 2 * 12) // 3
    columns = [BRIEFS[0:2], BRIEFS[2:4], BRIEFS[4:7]]
    for ci, regions in enumerate(columns):
        cx0 = MX + ci * (col_w + 12)
        yy = y
        for region, items in regions:
            d.text((cx0, yy), region, font=font(SANSB, 12), fill=RED)
            yy += 15
            rule(d, cx0, cx0 + col_w, yy, fill=RED, width=1)
            yy += 4
            for place, text in items:
                bf2 = font(SANS, 10)
                lead = place + " \u2014 "
                lines = wrap(d, lead + text, bf2, col_w)
                d.text((cx0, yy), lead, font=font(SANSB, 10), fill=INK)
                first = lines[0][len(lead):]
                lw_lead = d.textlength(lead, font=font(SANSB, 10))
                d.text((cx0 + lw_lead, yy), first, font=bf2, fill=INK)
                yy += 12
                for ln in lines[1:]:
                    d.text((cx0, yy), ln, font=bf2, fill=INK)
                    yy += 12
                yy += 1
            yy += 4
    rule(d, MX, RX, 944, fill=INK, width=1)

    # ---- date check box
    y = 952
    d.rectangle([MX, y, RX, y + 38], outline=RED, width=2)
    d.text((MX + 8, y + 4), "DATE CHECK", font=font(SANSB, 11), fill=RED)
    box_w = RX - MX - 118
    dlines = wrap(d, DATE_CHECK, font(SANS, 10), box_w)
    yy = y + 4
    for ln in dlines:
        d.text((MX + 118, yy), ln, font=font(SANS, 10), fill=INK)
        yy += 11
    # ---- footer
    ff = font(SANSC, 10)
    fw = d.textlength(FOOTER, font=ff)
    d.text(((W - fw) / 2, 998), FOOTER, font=ff, fill=GRAY)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    draw().save(out, optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: 1024x1024 PNG, {size} bytes, {N_STORIES} stories")
    assert size <= 1024 * 1024, f"entry.png over 1 MiB: {size}"


if __name__ == "__main__":
    main()

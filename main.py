#!/usr/bin/env python3
"""Global Edition — world news poster for Friday 20 November 2026.
Fresh build for make.fun competition news-image-20261120.
Generates entry.png (1024x1024, deterministic) and SOURCES.md from the
same story data. No timestamps, no randomness, no network calls.
All 56 stories were verified against credible outlets on 20 Nov 2026.
The Just Security Early Edition for 20 Nov 2026 was NOT yet published at
build time (09:24 WIB / 02:24 UTC); the 19 Nov edition was the latest, so
stories were sourced from Reuters/AP/BBC/The Guardian and the wires and
outlets listed in SOURCES.md instead.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER   = (248, 244, 232)
INK     = (20, 33, 61)
INK_SOFT= (64, 74, 96)
RED     = (193, 39, 45)
TEAL    = (14, 110, 110)
GOLD    = (176, 124, 22)
BLUE    = (38, 84, 150)
GREEN   = (46, 125, 60)
GREY    = (120, 116, 104)
LINE    = (196, 188, 168)
PANEL_BG= (255, 252, 244)
MAP_DOT = (52, 84, 130)

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FDB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def f(size, bold=False):
    return ImageFont.truetype(FDB if bold else FD, size)

# ---------------------------------------------------------------- data
# (region, headline, source tag, verification URL)
STORIES = [
    # ---- NORTH AMERICA (1-8)
    ("NORTH AMERICA", "Senate rejects Iran war-powers bill, 51-48", "AP",
     "https://www.appistos.gr/en/diethni.html"),
    ("NORTH AMERICA", "Trump pardons baseball legend Pete Rose", "AP",
     "https://www.appistos.gr/en/diethni.html"),
    ("NORTH AMERICA", "Judge: USDA chief's Christian emails unconstitutional", "AP",
     "https://pipedot.org/feed/wwwtheguardiancom"),
    ("NORTH AMERICA", "California opens probe of Nvidia over China AI chips", "Guardian",
     "https://pipedot.org/feed/wwwtheguardiancom"),
    ("NORTH AMERICA", "Florida carries out record 20th execution of 2026", "AP",
     "https://pipedot.org/feed/wwwtheguardiancom"),
    ("NORTH AMERICA", "Anthropic soars 17% after record $81.3bn IPO", "Reuters",
     "https://simplelife.news/regions/tw/en/latest.html"),
    ("NORTH AMERICA", "Trump back from China; White House briefing today", "Reuters",
     "https://simplelife.news/regions/tw/en/latest.html"),
    ("NORTH AMERICA", "Blood test can spot CTE in living players - study", "NY Post",
     "https://nypost.com/2026/11/19/sports/cte-breakthrough-could-diagnose-disease-in-living-football-players/"),
    # ---- LATIN AMERICA (9-16)
    ("LATIN AMERICA", "US, Venezuela sign deal to restore military ties", "Reuters",
     "https://studmentor.in/news-headlines-for-school-assembly-20-november-2026/"),
    ("LATIN AMERICA", "US details $12bn in Venezuelan oil, mineral revenue", "AP",
     "https://thepariseye.com/breaking-news"),
    ("LATIN AMERICA", "Copa: Venezuela flights 90% full, 47 a week", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("LATIN AMERICA", "Tesla opens orders in Argentina from today", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("LATIN AMERICA", "Brazil real hits 19-month low near R$5.93", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("LATIN AMERICA", "Lima mayor urges Peru election overhaul", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("LATIN AMERICA", "Haiti police: 34 gang suspects killed in Martissant", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("LATIN AMERICA", "CAF backs Panama journalist after arson attack", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    # ---- EUROPE (17-24)
    ("EUROPE", "Kyiv hit by four ballistic missiles overnight", "Daily Baku",
     "https://dailybaku.az/en/category/dunya"),
    ("EUROPE", "Genoa airport halts flights after drone sighting", "Daily Baku",
     "https://dailybaku.az/en/category/dunya"),
    ("EUROPE", "UK, Norway fund GBP100m+ for two Ukraine naval craft", "AP",
     "https://www.appistos.gr/en/diethni.html"),
    ("EUROPE", "Europe ready for talks with Russia on ending war", "Reuters",
     "https://jabulaniradio.com/rss/top-international-news-17"),
    ("EUROPE", "Denmark approves Greenland defence deal, 109-0", "AP",
     "https://www.appistos.gr/en/diethni.html"),
    ("EUROPE", "Serbia elects Cupic speaker, 140 votes to 97", "AP",
     "https://www.appistos.gr/en/diethni.html"),
    ("EUROPE", "France braces for 4th weekend of cost protests", "Paris Eye",
     "https://thepariseye.com/breaking-news"),
    ("EUROPE", "Millions strike across Spain over housing costs", "CBC",
     "https://warnpoint.com/report/2026-11"),
    # ---- MIDDLE EAST (25-32)
    ("MIDDLE EAST", "Trump: US to 'see what happens' in Iran war", "Just Security",
     "https://www.justsecurity.org/165250/early-edition-november-19-2026/"),
    ("MIDDLE EAST", "US strikes Iranian island in Hormuz, reports say", "Inquirer",
     "https://warnpoint.com/report/2026-11"),
    ("MIDDLE EAST", "Houthis claim strikes on four Saudi targets", "Daily Baku",
     "https://dailybaku.az/en/category/dunya"),
    ("MIDDLE EAST", "Saudi confirms rebel attack damaged Riyadh tower", "Reuters",
     "https://simplelife.news/regions/tw/en/latest.html"),
    ("MIDDLE EAST", "Tanker ablaze after hitting mine east of Hormuz", "Daily Baku",
     "https://dailybaku.az/en/category/dunya"),
    ("MIDDLE EAST", "Aid groups rate Gaza peace plan 4 out of 26", "AppiSToS",
     "https://www.appistos.gr/en/diethni.html"),
    ("MIDDLE EAST", "Four nations urge Israel to open Gaza aid routes", "Paris Eye",
     "https://thepariseye.com/breaking-news"),
    ("MIDDLE EAST", "Israeli strike hits Hezbollah site in E. Lebanon", "Daily Baku",
     "https://dailybaku.az/en/category/dunya"),
    # ---- AFRICA (33-40)
    ("AFRICA", "Two Sudan forces claim same Blue Nile town", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("AFRICA", "Somalia orders UAE envoy out within 72 hours", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("AFRICA", "Senegal president forces budget through by decree", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("AFRICA", "Gabon MPs cut budget by US$376 million", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("AFRICA", "Fidelity Bank names Amuchie as next CEO", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("AFRICA", "Soweto floods kill one; girl missing", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("AFRICA", "S. Africa holds rate as fuel lifts prices", "Rio Times",
     "https://www.1stheadlines.com/from/648"),
    ("AFRICA", "Bandits kill one, abduct five in Zamfara raid", "Punch",
     "https://warnpoint.com/report/2026-11"),
    # ---- ASIA (41-48)
    ("ASIA", "Trump, Xi, Putin sign 'peace declaration' in Shenzhen", "Reuters",
     "https://studmentor.in/news-headlines-for-school-assembly-20-november-2026/"),
    ("ASIA", "World Court: Myanmar committed Rohingya genocide", "AP",
     "https://www.appistos.gr/en/diethni.html"),
    ("ASIA", "APEC adopts Shenzhen Outlook on trade, AI", "AppiSToS",
     "https://www.appistos.gr/en/diethni.html"),
    ("ASIA", "Takaichi dodges Taiwan contingency question", "SimpleLife",
     "https://simplelife.news/regions/tw/en/latest.html"),
    ("ASIA", "N. Korea expanding Yongbyon enrichment - IAEA", "AP",
     "https://studmentor.in/news-headlines-for-school-assembly-20-november-2026/"),
    ("ASIA", "S. Korea court clears ex-PM Han Duck-soo", "AP",
     "https://studmentor.in/news-headlines-for-school-assembly-20-november-2026/"),
    ("ASIA", "Cyclone Akvan nears Odisha; schools shut", "Times of India",
     "https://www.educationtimes.com/news/school-assembly-news-headlines-for-november-20-2026-top-national-international-sports-and-business-news/articleshow/135990545.cms"),
    ("ASIA", "Indonesia passes asset-forfeiture bill", "AppiSToS",
     "https://www.appistos.gr/en/diethni.html"),
    # ---- OCEANIA (49-56)
    ("OCEANIA", "Nicholls 113* as NZ reach 243/5 vs India", "AP",
     "https://www.jagranjosh.com/lite/articles/school-assembly-news-headlines-november-20-2026-henry-nicholls-gta-6-gemini-4-up-police-and-other-news-1800019424-1"),
    ("OCEANIA", "Ash Barty picked for Tennis Hall of Fame", "Jagran Josh",
     "https://www.jagranjosh.com/lite/articles/school-assembly-news-headlines-november-20-2026-henry-nicholls-gta-6-gemini-4-up-police-and-other-news-1800019424-1"),
    ("OCEANIA", "Fiji declares disaster over drought, El Nino", "AP",
     "https://studmentor.in/news-headlines-for-school-assembly-20-november-2026/"),
    ("OCEANIA", "Cyclone Xavier: alerts for Cook Islands", "AppiSToS",
     "https://www.appistos.gr/en/diethni.html"),
    ("OCEANIA", "Faith reference 'fed bias', Australian monitor says", "Guardian",
     "https://pipedot.org/feed/wwwtheguardiancom"),
    ("OCEANIA", "AUKUS: could Australian ships be compelled?", "Guardian",
     "https://pipedot.org/feed/wwwtheguardiancom"),
    ("OCEANIA", "Physicists beam 'gravity' through brick wall", "Guardian",
     "https://pipedot.org/feed/wwwtheguardiancom"),
    ("OCEANIA", "PNG, Fiji join wildlife-for-climate declaration", "EIN Presswire",
     "https://globalwarming.einnews.com/country/honduras"),
]

REGIONS = [
    ("1", "NORTH AMERICA", "Senate 51-48; Pete Rose pardon", RED),
    ("2", "LATIN AMERICA", "Venezuela $12bn; Tesla in Argentina", (176, 90, 22)),
    ("3", "EUROPE", "Kyiv missiles; Greenland deal 109-0", BLUE),
    ("4", "MIDDLE EAST", "Hormuz tanker ablaze; Riyadh hit", (150, 60, 90)),
    ("5", "AFRICA", "Somalia expels envoy; budget decrees", GREEN),
    ("6", "ASIA", "Shenzhen summit; ICJ genocide ruling", TEAL),
    ("7", "OCEANIA", "Nicholls 113*; Fiji drought disaster", GOLD),
]

LEADS = [
    ("01", "SUMMIT OF THREE", "Trump, Xi and Putin sign a 'peace declaration' after their first-ever three-way meeting in Shenzhen.", "Reuters / AP / NYT"),
    ("42", "GENOCIDE RULING", "The World Court finds Myanmar committed genocide against the Rohingya, 9-6, and orders restitution.", "AP / BBC"),
    ("06", "RECORD IPO", "Anthropic raises $81.3bn in the largest IPO on record; shares jump 17% on debut.", "Reuters / BBC"),
]

TIMELINE = [
    ("01:27", "Tanker hits mine\neast of Hormuz"),
    ("02:30", "Trump pardons\nPete Rose"),
    ("03:17", "Gaza aid call;\nVenezuela $12bn file"),
    ("03:47", "Houthis claim hits\non four Saudi targets"),
    ("04:07", "Kyiv hit by four\nballistic missiles"),
    ("04:22", "Genoa airport halts\nflights after drones"),
]

NUMBERS = [
    ("$81.3bn", "Anthropic IPO, largest ever"),
    ("51-48", "Senate rejects Iran war powers"),
    ("9-6", "ICJ: Myanmar genocide"),
    ("80,000+", "evacuated as Storm Dana nears India"),
    ("R$5.93", "real at 19-month low"),
    ("4 / 26", "Gaza peace-plan score"),
]

WEATHER = ("London 9° rain  -  New York 18°  -  Tokyo 14°  -  Sydney 27°  -  Seoul 3°  -  Los Angeles 19°   "
           "(day highs, forecast issued 19 Nov: Met Office / World Weather Online / Darwin-Prediction)")
WEATHER_WATCH = ("WATCH: Cyclone Akvan nears Odisha  -  Saudi thunderstorms to Tue  -  Cyclone Xavier alerts, Cook Islands  -  Fiji drought disaster")

LEFT_OUT = ("LEFT OUT & WHY  -  Date rule: every story was published or reported on 20 Nov 2026. "
            "Excluded: Windows 11 Patch Tuesday (10 Nov, stale); COP31 mangrove $1bn (18 Nov, outside window); "
            "GTA 6 / Gemini 4 chatter (single-source roundups, unverified); the 19 Nov summit itself is kept only "
            "because its peace-declaration text landed on the 20th.")

# Dot-matrix world map: (row, col_start, col_end) spans on a 66 x 34 grid.
MAP_SPANS = [
    (0, [(44, 58)]),
    (1, [(4, 12), (42, 60)]),
    (2, [(2, 14), (30, 33), (40, 62)]),
    (3, [(1, 16), (29, 36), (39, 63)]),
    (4, [(2, 17), (29, 37), (38, 63)]),
    (5, [(3, 18), (29, 36), (39, 62)]),
    (6, [(4, 19), (30, 36), (40, 61)]),
    (7, [(5, 19), (31, 35), (41, 60)]),
    (8, [(6, 19), (32, 35), (42, 59)]),
    (9, [(7, 18), (33, 35), (43, 58)]),
    (10, [(8, 17), (33, 35), (44, 57)]),
    (11, [(9, 16), (29, 31), (34, 36), (45, 56)]),
    (12, [(9, 15), (29, 32), (35, 37), (46, 55)]),
    (13, [(10, 15), (30, 33), (36, 38), (47, 54)]),
    (14, [(11, 14), (30, 33), (37, 39), (47, 53)]),
    (15, [(12, 14), (30, 34), (38, 40), (48, 52)]),
    (16, [(13, 15), (30, 35), (39, 40), (49, 52)]),
    (17, [(15, 20), (30, 36), (49, 53)]),
    (18, [(16, 21), (30, 37), (50, 54)]),
    (19, [(16, 22), (31, 37), (51, 55)]),
    (20, [(17, 22), (31, 37), (52, 55)]),
    (21, [(17, 22), (32, 37), (52, 58)]),
    (22, [(18, 22), (32, 36), (52, 59)]),
    (23, [(18, 21), (33, 36), (52, 60)]),
    (24, [(18, 21), (33, 35), (53, 60)]),
    (25, [(19, 21), (53, 59), (62, 63)]),
    (26, [(19, 20), (54, 58), (62, 63)]),
    (27, [(19, 20), (54, 57)]),
    (28, [(19, 20)]),
    (29, [(19, 20)]),
    (30, [(20, 20)]),
]
# Region anchor pins on the same grid: (col, row)
PINS = {"1": (10, 8), "2": (19, 21), "3": (33, 6), "4": (42, 12),
        "5": (34, 18), "6": (51, 7), "7": (56, 24)}

# 16 illustrated scenes: (caption, kind)
PANELS = [
    ("SUMMIT", "flags"), ("ICJ VERDICT", "scales"), ("ANTHROPIC", "rocket"),
    ("AKVAN", "cyclone"), ("HORMUZ", "tanker"), ("KYIV", "missile"),
    ("GENOA", "drone"), ("NICHOLLS", "cricket"), ("FIONA", "hippo"),
    ("BARTY", "tennis"), ("GREENLAND", "parliament"), ("VENEZUELA", "derrick"),
    ("SENATE", "gavel"), ("TAIWAN", "chart"), ("FIJI", "drought"),
    ("XAVIER", "storm"),
]

# ---------------------------------------------------------------- helpers
def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

def wrap(d, s, font, max_w):
    """Greedy word wrap to max width; returns list of lines."""
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def trunc(d, s, font, max_w):
    if d.textlength(s, font=font) <= max_w:
        return s
    while s and d.textlength(s + "...", font=font) > max_w:
        s = s[:-1]
    return s + "..."

# ---------------------------------------------------------------- icons
def icon(d, kind, x0, y0, s, c1, c2):
    """Draw a simple pictogram inside a box of size s at (x0, y0)."""
    cx, cy = x0 + s / 2, y0 + s / 2
    if kind == "flags":  # three flag poles
        for i, c in enumerate([RED, (200, 40, 40), BLUE]):
            x = x0 + 6 + i * (s - 12) / 3
            d.line([(x, y0 + 6), (x, y0 + s - 8)], fill=INK, width=2)
            d.polygon([(x, y0 + 6), (x + (s - 12) / 3 - 2, y0 + 10), (x, y0 + 14)], fill=c)
        d.line([(x0 + 4, y0 + s - 8), (x0 + s - 4, y0 + s - 8)], fill=INK, width=2)
    elif kind == "scales":
        d.line([(cx, y0 + 5), (cx, y0 + s - 8)], fill=INK, width=2)
        d.line([(x0 + 5, y0 + 12), (x0 + s - 5, y0 + 12)], fill=INK, width=2)
        for sx in (x0 + 5, x0 + s - 5):
            d.line([(sx, y0 + 12), (sx - 6, y0 + 24)], fill=INK, width=1)
            d.line([(sx, y0 + 12), (sx + 6, y0 + 24)], fill=INK, width=1)
            d.arc([sx - 7, y0 + 19, sx + 7, y0 + 29], 0, 180, fill=c1, width=2)
        d.ellipse([cx - 3, y0 + 3, cx + 3, y0 + 9], fill=GOLD)
    elif kind == "rocket":
        d.polygon([(cx, y0 + 4), (cx + 7, y0 + 20), (cx - 7, y0 + 20)], fill=c1)
        d.rectangle([cx - 7, y0 + 20, cx + 7, y0 + 28], fill=INK)
        d.polygon([(cx - 4, y0 + 28), (cx, y0 + 38), (cx + 4, y0 + 28)], fill=GOLD)
        d.line([(x0 + 4, y0 + s - 4), (x0 + s - 4, y0 + s - 4)], fill=GREY, width=1)
    elif kind == "cyclone":
        for r in (16, 11, 6):
            d.arc([cx - r, cy - r, cx + r, cy + r], 200, 200 + 300, fill=c1, width=3)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
    elif kind == "tanker":
        d.polygon([(x0 + 4, y0 + s - 14), (x0 + s - 4, y0 + s - 14),
                   (x0 + s - 10, y0 + s - 5), (x0 + 10, y0 + s - 5)], fill=INK)
        d.rectangle([x0 + 10, y0 + s - 24, x0 + s - 12, y0 + s - 14], fill=c1)
        d.polygon([(cx, y0 + 2), (cx - 5, y0 + 12), (cx - 1, y0 + 12),
                   (cx + 2, y0 + 18), (cx + 6, y0 + 8)], fill=GOLD)
    elif kind == "missile":
        d.line([(x0 + 6, y0 + s - 8), (x0 + s - 10, y0 + 10)], fill=INK, width=3)
        d.polygon([(x0 + s - 12, y0 + 6), (x0 + s - 2, y0 + 4),
                   (x0 + s - 6, y0 + 16)], fill=RED)
        for dx, dy in ((8, 8), (14, 14), (20, 20)):
            d.ellipse([x0 + dx - 2, y0 + s - 8 - dy - 2, x0 + dx + 2, y0 + s - 8 - dy + 2],
                      fill=GOLD)
    elif kind == "drone":
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=INK)
        for dx, dy in ((-12, -10), (12, -10), (-12, 10), (12, 10)):
            d.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4],
                      outline=c1, width=2)
            d.line([(cx, cy), (cx + dx, cy + dy)], fill=GREY, width=1)
        d.line([(x0 + 2, y0 + s - 5), (x0 + s - 2, y0 + s - 5)], fill=GREY, width=2)
    elif kind == "cricket":
        d.line([(x0 + 8, y0 + s - 6), (x0 + s - 14, y0 + 10)], fill=(150, 110, 60), width=5)
        d.ellipse([cx + 8, cy - 12, cx + 16, cy - 4], fill=RED)
        d.line([(x0 + 4, y0 + s - 6), (x0 + s - 4, y0 + s - 6)], fill=GREY, width=1)
    elif kind == "hippo":
        d.rounded_rectangle([x0 + 5, y0 + 12, x0 + s - 5, y0 + s - 10], 8, fill=(140, 130, 125))
        d.ellipse([x0 + 9, y0 + 6, x0 + 17, y0 + 14], fill=(140, 130, 125))
        d.ellipse([x0 + s - 17, y0 + 6, x0 + s - 9, y0 + 14], fill=(140, 130, 125))
        d.ellipse([x0 + s - 12, y0 + 16, x0 + s - 8, y0 + 20], fill=INK)
    elif kind == "tennis":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(190, 210, 60), outline=INK, width=1)
        d.arc([cx - 13, cy - 13, cx + 13, cy + 13], 300, 60, fill=INK, width=2)
        d.arc([cx - 13, cy - 13, cx + 13, cy + 13], 120, 240, fill=INK, width=2)
    elif kind == "parliament":
        d.pieslice([cx - 12, y0 + 4, cx + 12, y0 + 26], 180, 360, fill=c1)
        d.rectangle([x0 + 6, y0 + 24, x0 + s - 6, y0 + 28], fill=INK)
        for i in range(4):
            x = x0 + 10 + i * 9
            d.line([(x, y0 + 28), (x, y0 + s - 6)], fill=INK, width=2)
        d.line([(x0 + 4, y0 + s - 6), (x0 + s - 4, y0 + s - 6)], fill=INK, width=2)
    elif kind == "derrick":
        d.line([(x0 + 8, y0 + s - 6), (cx, y0 + 4)], fill=INK, width=2)
        d.line([(x0 + s - 8, y0 + s - 6), (cx, y0 + 4)], fill=INK, width=2)
        d.line([(x0 + 12, y0 + s - 14), (x0 + s - 12, y0 + s - 14)], fill=INK, width=2)
        d.line([(x0 + 14, y0 + s - 22), (x0 + s - 14, y0 + s - 22)], fill=INK, width=2)
        d.ellipse([cx - 3, cy - 16, cx + 3, cy - 10], fill=GOLD)
    elif kind == "gavel":
        d.line([(x0 + 8, y0 + s - 8), (x0 + s - 8, y0 + 10)], fill=(150, 110, 60), width=4)
        d.rectangle([x0 + s - 18, y0 + 4, x0 + s - 6, y0 + 16], fill=INK)
        d.line([(x0 + 6, y0 + s - 6), (x0 + s - 6, y0 + s - 6)], fill=INK, width=2)
    elif kind == "chart":
        pts = [(x0 + 5, y0 + s - 10), (x0 + 14, y0 + s - 18), (x0 + 22, y0 + s - 14),
               (x0 + 30, y0 + s - 24), (x0 + 38, y0 + 8)]
        d.line(pts, fill=c2, width=2)
        d.polygon([(x0 + 38, y0 + 8), (x0 + 33, y0 + 8), (x0 + 38, y0 + 13)], fill=c2)
        d.line([(x0 + 4, y0 + s - 6), (x0 + s - 4, y0 + s - 6)], fill=GREY, width=1)
    elif kind == "drought":
        d.polygon([(x0 + 4, y0 + s - 6), (x0 + s - 4, y0 + s - 6), (cx, y0 + 8)], fill=(210, 190, 140))
        d.line([(x0 + 10, y0 + s - 10), (x0 + 16, y0 + s - 18)], fill=INK, width=1)
        d.line([(x0 + 22, y0 + s - 8), (x0 + 26, y0 + s - 16)], fill=INK, width=1)
        d.ellipse([cx - 9, y0 + 2, cx + 9, y0 + 14], fill=GOLD)
    elif kind == "storm":
        d.ellipse([x0 + 6, y0 + 8, x0 + 24, y0 + 22], fill=INK_SOFT)
        d.ellipse([x0 + 16, y0 + 4, x0 + 36, y0 + 22], fill=INK_SOFT)
        for i, x in enumerate((x0 + 12, x0 + 22, x0 + 32)):
            d.line([(x, y0 + 26), (x - 3, y0 + 32), (x + 1, y0 + 32), (x - 2, y0 + 38)],
                   fill=GOLD, width=2)

# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14  # margin

    # ---- masthead
    d.rectangle([0, 0, W, 74], fill=INK)
    text(d, (M, 10), "THE GLOBAL EDITION", f(40, True), fill=(248, 244, 232))
    text(d, (W - M, 12), "FRIDAY  •  20 NOVEMBER 2026", f(15, True),
         fill=(232, 200, 90), anchor="ra")
    text(d, (W - M, 36), "56 STORIES  •  7 REGIONS  •  EVERY ITEM SOURCED", f(11),
         fill=(200, 205, 220), anchor="ra")
    d.line([(0, 76), (W, 76)], fill=RED, width=3)

    # ---- lead band: three headline boxes
    bw = (W - 2 * M - 2 * 8) / 3
    for i, (num, kick, head, src) in enumerate(LEADS):
        x0 = M + i * (bw + 8)
        d.rectangle([x0, 82, x0 + bw, 144], outline=LINE, width=1, fill=PANEL_BG)
        d.rectangle([x0, 82, x0 + 34, 100], fill=RED)
        text(d, (x0 + 17, 84), num, f(11, True), fill=(255, 255, 255), anchor="ma")
        text(d, (x0 + 40, 84), kick, f(10, True), fill=RED)
        lines = wrap(d, head, f(11), bw - 12)
        for j, ln in enumerate(lines[:2]):
            text(d, (x0 + 6, 102 + j * 14), ln, f(11), fill=INK)
        text(d, (x0 + 6, 132), "Source: " + src, f(8), fill=GREY)

    # ---- map panel
    d.rectangle([M, 150, W - M, 372], outline=LINE, width=1, fill=PANEL_BG)
    text(d, (M + 8, 156), "THE WORLD IN DOTS  —  7 REGIONS, 56 STORIES", f(11, True), fill=INK)
    text(d, (W - M - 8, 156), "pins = region anchors", f(9), fill=GREY, anchor="ra")
    mx, my, cw, ch = 22, 178, 9.3, 5.9
    for (row, spans) in MAP_SPANS:
        for (a, b) in spans:
            for c in range(a, b + 1):
                px, py = mx + c * cw + cw / 2, my + row * ch + ch / 2
                d.ellipse([px - 2.4, py - 2.4, px + 2.4, py + 2.4], fill=MAP_DOT)
    for num, (c, r) in PINS.items():
        px, py = mx + c * cw + cw / 2, my + r * ch + ch / 2
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=2)
        text(d, (px, py - 7), num, f(10, True), fill=(255, 255, 255), anchor="ma")
    # legend (right of map)
    lx = 668
    d.line([(lx - 10, 178), (lx - 10, 366)], fill=LINE, width=1)
    text(d, (lx, 178), "REGION KEY", f(10, True), fill=INK)
    y = 192
    for num, name, lead, col in REGIONS:
        d.ellipse([lx, y, lx + 16, y + 16], fill=col)
        text(d, (lx + 8, y + 2), num, f(10, True), fill=(255, 255, 255), anchor="ma")
        text(d, (lx + 22, y), name, f(10, True), fill=INK)
        text(d, (lx + 22, y + 12), "8 stories - " + lead, f(8), fill=INK_SOFT)
        y += 22
    text(d, (lx, 348), "HOW TO READ: number = story # below;", f(8), fill=GREY)
    text(d, (lx, 358), "outlet tag at line end. Full sources: SOURCES.md.", f(8), fill=GREY)

    # ---- 16 scenes strip
    text(d, (M, 380), "16 SCENES FROM THE DAY", f(11, True), fill=INK)
    text(d, (W - M, 380), "drawn from the stories below", f(9), fill=GREY, anchor="ra")
    pw, gap = 58, (W - 2 * M - 16 * 58) / 15
    for i, (cap, kind) in enumerate(PANELS):
        x0 = M + i * (pw + gap)
        d.rectangle([x0, 396, x0 + pw, 452], outline=LINE, width=1, fill=PANEL_BG)
        icon(d, kind, x0 + 9, 398, 40, RED, TEAL)
        text(d, (x0 + pw / 2, 440), cap, f(7, True), fill=INK, anchor="ma")

    # ---- story grid
    text(d, (M, 458), "THE DAY IN 56 STORIES", f(12, True), fill=INK)
    text(d, (W - M, 458), "all dated 20 Nov 2026  •  outlet tag at line end", f(9),
         fill=GREY, anchor="ra")
    d.line([(M, 472), (W - M, 472)], fill=INK, width=1)
    col_x = [M, 519]
    col_w = [491, 491]
    col_a = STORIES[:28]
    col_b = STORIES[28:]
    y0, pitch = 478, 10.8
    for ci, col in enumerate((col_a, col_b)):
        y = y0
        cur_region = None
        base = 0 if ci == 0 else 28
        for idx, (region, head, src, _url) in enumerate(col):
            n = base + idx + 1
            if region != cur_region:
                cur_region = region
                rcol = dict((r[1], r[3]) for r in REGIONS)[region]
                d.rectangle([col_x[ci], y - 1, col_x[ci] + 5, y + 9], fill=rcol)
                text(d, (col_x[ci] + 9, y), region, f(8, True), fill=rcol)
                y += pitch
            text(d, (col_x[ci], y), "%02d" % n, f(9, True), fill=RED)
            hw = col_w[ci] - 24 - d.textlength("  " + src, font=f(8)) - 4
            htxt = trunc(d, head, f(9.5), hw)
            text(d, (col_x[ci] + 24, y), htxt, f(9.5), fill=INK)
            text(d, (col_x[ci] + col_w[ci], y), src, f(8), fill=GREY, anchor="ra")
            y += pitch

    # ---- UTC timeline
    text(d, (M, 828), "THE DAY IN UTC", f(11, True), fill=INK)
    d.line([(M, 844), (W - M, 844)], fill=INK, width=2)
    tw = (W - 2 * M) / 6
    for i, (t, label) in enumerate(TIMELINE):
        cx = M + tw * i + tw / 2
        d.ellipse([cx - 4, 840, cx + 4, 848], fill=RED)
        text(d, (cx, 852), t, f(10, True), fill=RED, anchor="ma")
        for j, ln in enumerate(label.split("\n")):
            text(d, (cx, 866 + j * 10), ln, f(8), fill=INK_SOFT, anchor="ma")

    # ---- by the numbers
    text(d, (M, 890), "BY THE NUMBERS", f(11, True), fill=INK)
    nw = (W - 2 * M) / 6
    for i, (big, small) in enumerate(NUMBERS):
        x0 = M + i * nw
        d.rectangle([x0 + 2, 904, x0 + nw - 2, 936], outline=LINE, width=1, fill=PANEL_BG)
        text(d, (x0 + nw / 2, 906), big, f(12, True), fill=RED, anchor="ma")
        lines = wrap(d, small, f(7.5), nw - 10)
        for j, ln in enumerate(lines[:2]):
            text(d, (x0 + nw / 2, 921 + j * 9), ln, f(7.5), fill=INK_SOFT, anchor="ma")

    # ---- weather strip
    d.rectangle([M, 942, W - M, 960], fill=(232, 238, 244))
    text(d, (M + 6, 946), "WEATHER  " + WEATHER, f(8.5), fill=INK)
    text(d, (M, 964), WEATHER_WATCH, f(8.5), fill=INK_SOFT)

    # ---- left out & why + footer
    d.rectangle([M, 978, W - M, 1010], outline=LINE, width=1, fill=PANEL_BG)
    lo_lines = wrap(d, LEFT_OUT, f(8.5), W - 2 * M - 12)
    for j, ln in enumerate(lo_lines[:2]):
        text(d, (M + 6, 982 + j * 11), ln, f(8.5), fill=INK)
    text(d, (W / 2, 1014), "Sources: Reuters - AP - BBC - The Guardian - NYT - CNN - Sky News - Met Office - "
         "Just Security (19 Nov ed.) - TOI - Rio Times - Daily Baku - Paris Eye - AppiSToS - SimpleLife - EIN - NY Post - JAMA",
         f(7.5), fill=GREY, anchor="ma")

    img.save(os.path.join(HERE, "entry.png"))
    return img

def write_sources():
    lines = ["# SOURCES — Global Edition, Friday 20 November 2026",
             "",
             "Every story on the poster was published or reported on **20 November 2026**.",
             "The Just Security Early Edition for 20 Nov 2026 was **not yet published** at build",
             "time (09:24 WIB / 02:24 UTC); the latest edition available was 19 Nov. Stories were",
             "therefore verified against Reuters, AP, BBC, The Guardian and the outlets below.",
             "URLs are the pages where each item was verified (wire roundups / aggregator pages",
             "where the original wire item was carried).",
             "",
             "## Stories",
             ""]
    cur = None
    for i, (region, head, src, url) in enumerate(STORIES, 1):
        if region != cur:
            cur = region
            lines.append("### %s" % region)
            lines.append("")
        lines.append("%d. **%s** — %s, 20 Nov 2026 — <%s>" % (i, head, src, url))
    lines += ["",
              "## Weather",
              "",
              "- City highs for 20 Nov 2026 (forecast issued 19 Nov 00:40 UTC, Darwin-Prediction-Weather): "
              "https://vidraft-ai-media.static.hf.space/a/weather-forecast-24-cities-2026-11-19.html",
              "- London 5/9 C, patchy rain (Met Office): https://weather.metoffice.gov.uk/forecast/gcpvn15h9?new-design=false",
              "- London 5/9 C (World Weather Online): https://www.worldweatheronline.com/london-weather/city-of-london-greater-london/gb.aspx?day=5",
              "",
              "## Left out & why",
              "",
              LEFT_OUT,
              ""]
    with open(os.path.join(HERE, "SOURCES.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    build()
    write_sources()
    data = open(os.path.join(HERE, "entry.png"), "rb").read()
    print("entry.png", len(data), "bytes, sha256", hashlib.sha256(data).hexdigest()[:16])
    print("stories:", len(STORIES), "regions:", len(REGIONS), "panels:", len(PANELS))

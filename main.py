#!/usr/bin/env python3
# news-image-20261118 v3 — "Wednesday 18 November 2026 in 43 stories"
# Written fresh from the top-5 analysis + locked news list (no old code read).
# Stdlib only, deterministic: same input -> byte-identical entry.png.
# Fonts are embedded as a compressed bitmap blob (rasterized from DejaVu /
# Liberation at build time); the entrypoint needs no system fonts.
import base64
import binascii
import json
import math
import struct
import zlib

W, H = 1024, 1024

FONT_BLOB = "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"

FONTS = json.loads(zlib.decompress(base64.b64decode(FONT_BLOB)))


def save_png(path, buf, w, h):
    """Minimal PNG writer (color type 2, 8-bit, filter 0 per row)."""
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += buf[y * w * 3:(y + 1) * w * 3]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", binascii.crc32(typ + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(bg * (w * h))

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(c)

    def hline(self, x0, x1, y, c):
        if y < 0 or y >= self.h:
            return
        x0 = max(0, x0)
        x1 = min(self.w - 1, x1)
        if x1 < x0:
            return
        i = (y * self.w + x0) * 3
        self.buf[i:(y * self.w + x1 + 1) * 3] = bytes(c) * (x1 - x0 + 1)

    def vline(self, x, y0, y1, c):
        if x < 0 or x >= self.w:
            return
        for y in range(max(0, y0), min(self.h - 1, y1) + 1):
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            self.hline(x, x + w - 1, yy, c)

    def outline(self, x, y, w, h, c):
        self.hline(x, x + w - 1, y, c)
        self.hline(x, x + w - 1, y + h - 1, c)
        self.vline(x, y, y + h - 1, c)
        self.vline(x + w - 1, y, y + h - 1, c)

    def line(self, x0, y0, x1, y1, c):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def ellipse(self, cx, cy, rx, ry, c):
        for yy in range(cy - ry, cy + ry + 1):
            t = (yy - cy) / ry
            if abs(t) > 1:
                continue
            dx = int(rx * math.sqrt(1 - t * t))
            self.hline(cx - dx, cx + dx, yy, c)

    def circle(self, cx, cy, r, c):
        self.ellipse(cx, cy, r, r, c)

    def poly(self, pts, c):
        """Scanline polygon fill."""
        if len(pts) < 3:
            return
        ymin = min(p[1] for p in pts)
        ymax = max(p[1] for p in pts)
        for y in range(ymin, ymax + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.hline(int(math.ceil(xs[i])), int(xs[i + 1]), y, c)

    def ring(self, cx, cy, r, c):
        """1px circle outline (for the cyclone spiral + stars)."""
        for a in range(360):
            t = math.radians(a)
            self.px(int(cx + r * math.cos(t)), int(cy + r * math.sin(t)), c)


# ---------------- bitmap text (from the embedded font tables) ----------------

def text_w(font, s, scale=1.0):
    tab = FONTS[font]
    return sum(tab.get(ch, tab[" "])[0] for ch in s) * scale


def text_h(font):
    return FONTS[font]["A"][1]


def draw_text(cv, font, x, y, s, color, scale=1.0):
    """Draw text at (x, y) = top of the 'A' glyph. Returns end x."""
    tab = FONTS[font]
    cx = x
    for ch in s:
        g = tab.get(ch)
        if g is None:
            g = tab[" "]
        w, h, yoff, hx = g
        if w == 0:
            cx += tab[" "][0] * scale
            continue
        ow = max(1, int(round(w * scale)))
        oh = max(1, int(round(h * scale)))
        raw = bytes.fromhex(hx)
        nb = (w + 7) // 8
        # area-coverage downscale: ink a pixel if >=35% of its source is ink
        for oy in range(oh):
            sy0 = oy / scale
            sy1 = (oy + 1) / scale
            for ox in range(ow):
                sx0 = ox / scale
                sx1 = (ox + 1) / scale
                ink = 0
                tot = 0
                for sy in range(int(sy0), min(h, int(math.ceil(sy1)))):
                    for sx in range(int(sx0), min(w, int(math.ceil(sx1)))):
                        tot += 1
                        if raw[sy * nb + sx // 8] & (1 << (7 - sx % 8)):
                            ink += 1
                if tot and ink / tot >= 0.35:
                    cv.px(int(cx + ox), int(y + yoff * scale + oy), color)
        cx += w * scale
    return cx


def draw_text_c(cv, font, cx, y, s, color, scale=1.0):
    x = cx - text_w(font, s, scale) / 2
    return draw_text(cv, font, int(round(x)), y, s, color, scale)


def wrap(font, s, maxw, scale=1.0):
    lines, cur = [], ""
    for word in s.split(" "):
        t = word if not cur else cur + " " + word
        if text_w(font, t, scale) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

# ---------------- palette ----------------
NAVY = (21, 38, 74)
NAVY_DK = (14, 26, 52)
GOLD = (201, 162, 39)
GOLD_LT = (226, 196, 96)
PAPER = (250, 248, 240)
CARD = (255, 255, 255)
CARD_LN = (216, 212, 198)
INK = (26, 26, 26)
INK_SOFT = (74, 74, 74)
RED = (178, 34, 34)
TEAL = (14, 58, 58)
TEAL_LT = (32, 96, 96)
MAP_DOT = (150, 140, 110)
MAP_BG = (238, 240, 235)
GRAY = (140, 140, 140)

# ---------------- locked content (news-20261118.md section E) ----------------
# Headlines are the locked wording, trimmed only where the v3 brief allows it
# (lead headlines shortened to fit 2 lines at 25.5 pt; facts unchanged).
LEADS = [
    dict(num=1, kicker="MIDDLE EAST | CONFLICT", tag="REPORTED",
         head="Iran's drones reach Kuwait and Bahrain",
         deck="Iran fired drones at the US-hosted Ali Al Salem base in Kuwait and renewed attacks on Bahrain early Wednesday.",
         caption="ALI AL SALEM BASE | KUWAIT"),
    dict(num=2, kicker="ASIA | DIPLOMACY", tag="REPORTED",
         head="Xi greets Trump in Shenzhen",
         deck="Xi welcomed Trump at the airport, a rare break with protocol; the three leaders shook hands at the banquet. Talks are Thursday.",
         caption="SHENZHEN | APEC"),
    dict(num=3, kicker="INDIA | WEATHER", tag="REPORTED",
         head="Cyclone Akvan bears down on India",
         deck="Akvan strengthened to a severe cyclonic storm 580 km east of Chennai; landfall is due around noon Friday.",
         caption="BAY OF BENGAL | 580 KM EAST OF CHENNAI"),
]

CARDS = [
    dict(num=4, kicker="US | TECH/MARKETS", tag="REPORTED",
         head="Nvidia \u2014 $115.8B revenue, up 103%, but shares fall",
         deck="Record Q3 revenue beat forecasts and guided Q4 to $130B, yet the stock fell 2.9% to $150.96."),
    dict(num=5, kicker="AFRICA | CONFLICT", tag="REPORTED",
         head="UN: 2,230 civilians killed, most by drones",
         deck="UN rights office counts 2,230 civilian deaths in Jan-Oct, over 1,630 by drone strikes."),
    dict(num=6, kicker="EUROPE | WAR", tag="REPORTED",
         head="Ukraine drops a span of the Kerch bridge",
         deck="Two nights of strikes brought down a road span and a steel arch; road traffic is cut."),
    dict(num=7, kicker="ISRAEL | POLITICS", tag="REPORTED",
         head="Kahana elected speaker 66-52, a blow to Netanyahu",
         deck="Matan Kahana beat Likud's Ofir Katz for speaker; Netanyahu stays caretaker PM."),
    dict(num=8, kicker="EUROPE | ECONOMY", tag="REPORTED",
         head="Brussels proposes a EUR 45B loan for Ukraine",
         deck="Brussels proposed on Wednesday a EUR 45B loan for 2027: EUR 20B aid, EUR 25B military."),
    dict(num=9, kicker="MIDDLE EAST | DIPLOMACY", tag="REPORTED",
         head="Board of Peace warns Gaza truce may collapse",
         deck="A Board of Peace report, seen by AP, says the 2025 ceasefire \"cannot be sustained indefinitely\"."),
    dict(num=10, kicker="UK | FOREIGN POLICY", tag="REPORTED",
         head="Britain sanctions 8 settler firms and Tzav 9",
         deck="Asset freezes and director bans hit eight Israeli construction firms and the Tzav 9 group."),
    dict(num=11, kicker="ASIA | TRADE", tag="REPORTED",
         head="Xi meets Carney; Beijing cuts tariffs",
         deck="China offered about C$400M in tariff relief on Canadian pork and seafood as Xi met Carney."),
    dict(num=12, kicker="CLIMATE | SUMMIT", tag="SCHEDULED",
         head="30+ nations join Turkiye's 35x35 clean-power goal",
         deck="Turkiye's COP31 target lifts clean power to 35% of final energy by 2035, from about 20%."),
    dict(num=13, kicker="US | POLITICS", tag="REPORTED",
         head="Peltola flips Senate seat; Democrats lead 56-44",
         deck="Mary Peltola beat Dan Sullivan 144,302 to 131,844; Democrats now hold a 56-44 majority."),
]

ALSO = [
    "14. Guinea: 224 sentenced in mining crackdown",
    "15. An-12 crash: ministry says all 19 aboard killed",
    "16. Dhoni ends IPL playing career, to mentor CSK",
    "17. Voyager 1 reaches one light-day from Earth",
    "18. Anthropic prices IPO at $83, a $1.5T valuation",
    "19. GTA VI unlocks begin in New Zealand, 11:00 UTC",
    "20. Fed minutes point to a Dec hike; Dow -561",
    "21. NSA's NSANet still down; no sign of a hack",
    "22. Estonia to shut Russia border from 1 Dec",
    "23. Jordan and Iraq block Telegram",
    "24. Costa Rica journalist shot dead in his car",
    "25. Japan scrambles jets after Russian breach",
    "26. Apple outage hits App Store and iCloud",
    "27. Pope Leo forgives rosary thrower in Peru",
    "28. Amazon to invest $7B in India renewables",
    "29. Peru quake M5.9 off Ica; no tsunami",
    "30. NZ lifts tsunami advisory after surge",
    "31. Tencent revenue misses as AI capex surges",
    "32. Bank Indonesia hikes rate to 6.00%",
    "33. Cyclone Xavier nears Cook Islands",
    "34. Gold sinks to a 14-month low near $3,726",
    "35. UK inflation rises to 3.6%, one-year high",
    "36. DR Congo Ebola toll passes 11,500 cases",
    "37. US loses measles elimination status",
    "38. ASX 200 falls a fifth day to 8,821.8",
    "39. Mozambique's Mondlane goes on trial",
    "40. Colombia's economy slows to 0.5% in Q3",
    "41. Grimes scores 47 as Lakers win ninth straight",
    "42. Haiti signs pact with El Salvador",
    "43. US and Thailand agree trade pact in principle",
]

NUMBERS = [
    ("$115.8B", "NVIDIA Q3 REVENUE, +103% YOY"),
    ("56-44", "DEMOCRATS LEAD THE US SENATE"),
    ("2,230", "CIVILIANS KILLED IN SUDAN (UN)"),
    ("1 LIGHT-DAY", "VOYAGER 1 FROM EARTH, 25.9B KM"),
]

FOOTER_1 = "Every story was reported on Wednesday 18 November 2026. Drawn entirely in code; no photos, no AI images."
FOOTER_2 = "Gaza toll: Gaza health authorities via AP. An-12 toll: Russian ministry. Sources: AP, Reuters, AFP, BBC, UN, NASA and others."

# ---------------- world map data (authored from geographic knowledge) ----------------
# Grid: lon -180..175 in 5-degree columns (72 cols); rows every 5 degrees lat.
LAND_ROWS = [
    (75, [(2, 17), (24, 32), (38, 42), (43, 71)]),
    (70, [(2, 23), (25, 31), (40, 42), (44, 71)]),
    (65, [(2, 24), (31, 33), (37, 71)]),
    (60, [(6, 17), (20, 25), (27, 28), (35, 71)]),
    (55, [(2, 4), (5, 25), (35, 71)]),
    (50, [(11, 25), (35, 65)]),
    (45, [(11, 23), (35, 41), (44, 45), (46, 62), (64, 65)]),
    (40, [(11, 21), (34, 64)]),
    (35, [(12, 21), (34, 64)]),
    (30, [(12, 20), (34, 60)]),
    (25, [(13, 21), (33, 59)]),
    (20, [(15, 18), (32, 58), (60, 60)]),
    (15, [(17, 19), (32, 47), (50, 52), (54, 57), (60, 60)]),
    (10, [(19, 23), (32, 46), (51, 52), (54, 57), (59, 60)]),
    (5, [(20, 25), (33, 46), (55, 59), (62, 64)]),
    (0, [(20, 29), (33, 44), (55, 59), (62, 64)]),
    (-5, [(20, 29), (33, 44), (55, 60), (62, 64)]),
    (-10, [(20, 29), (33, 44), (57, 58), (60, 64)]),
    (-15, [(21, 28), (33, 46), (58, 64)]),
    (-20, [(22, 28), (33, 46), (58, 66)]),
    (-25, [(22, 26), (33, 45), (58, 66)]),
    (-30, [(22, 26), (33, 42), (58, 66)]),
    (-35, [(21, 25), (32, 41), (59, 66), (69, 71)]),
    (-40, [(21, 23), (64, 66), (69, 70)]),
    (-45, [(21, 22), (69, 70)]),
    (-50, [(21, 22)]),
    (-55, [(22, 22)]),
]

# Story locations (lon, lat). Voyager (17) sits at JPL Pasadena, which
# operates the spacecraft.
PLACES = {
    1: (47.5, 29.3), 2: (114.05, 22.55), 3: (86.0, 16.0),
    4: (-121.95, 37.35), 5: (32.5, 15.6), 6: (36.5, 45.3),
    7: (35.21, 31.77), 8: (4.35, 50.85), 9: (34.47, 31.5),
    10: (-0.13, 51.5), 11: (114.05, 22.55), 12: (30.7, 36.9),
    13: (-149.9, 61.2), 14: (-13.71, 9.51), 15: (86.09, 55.36),
    16: (80.27, 13.08), 17: (-118.13, 34.2), 18: (-122.42, 37.77),
    19: (174.78, -41.29), 20: (-77.04, 38.9), 21: (-76.77, 39.11),
    22: (24.75, 59.44), 23: (35.93, 31.95), 24: (-84.09, 9.93),
    25: (130.4, 33.59), 26: (-122.03, 37.32), 27: (-77.04, -12.05),
    28: (77.21, 28.61), 29: (-75.73, -14.07), 30: (176.92, -39.49),
    31: (114.05, 22.55), 32: (106.85, -6.21), 33: (-159.77, -21.23),
    34: (-74.01, 40.71), 35: (-0.13, 51.5), 36: (30.06, 0.71),
    37: (-84.39, 33.75), 38: (151.21, -33.87), 39: (32.58, -25.97),
    40: (-74.07, 4.71), 41: (-118.24, 34.05), 42: (-72.34, 18.54),
    43: (100.5, 13.76),
}

# Hand-tuned pixel offsets for markers that share (or nearly share) a spot.
# A hairline connects each offset marker back to its true location.
MAP_OFFSETS = {
    1: (26, 16), 6: (18, -20), 7: (-28, -20), 8: (-24, -8), 9: (-32, 2),
    11: (0, 18), 12: (-14, 24), 17: (12, 10), 21: (6, -16), 22: (6, -10),
    23: (28, 8), 25: (-4, -12), 26: (0, 14), 27: (-12, -8), 30: (0, -12),
    31: (18, -8), 34: (18, -12), 35: (-20, 14), 37: (0, 14), 40: (12, 10),
    41: (-4, 16),
}

# ---------------- scene drawing (all original PIL-primitive compositions) ----------------

def _flag_us(cv, x, y, w, h):
    for i in range(7):
        cv.rect(x, y + i * h // 7, w, h // 7 + 1,
                (178, 34, 52) if i % 2 == 0 else (240, 240, 240))
    cv.rect(x, y, w * 2 // 5, h * 4 // 7, (30, 50, 110))
    for dx in (2, 6, 10):
        for dy in (2, 5):
            cv.px(x + dx, y + dy, (255, 255, 255))


def _flag_cn(cv, x, y, w, h):
    cv.rect(x, y, w, h, (222, 32, 32))
    cv.px(x + 3, y + 3, (255, 220, 60))
    cv.px(x + 6, y + 2, (255, 220, 60))
    cv.px(x + 7, y + 5, (255, 220, 60))
    cv.px(x + 5, y + 7, (255, 220, 60))


def _flag_ru(cv, x, y, w, h):
    cv.rect(x, y, w, h // 3, (245, 245, 245))
    cv.rect(x, y + h // 3, w, h // 3, (30, 80, 180))
    cv.rect(x, y + 2 * h // 3, w, h - 2 * h // 3, (200, 30, 30))


def _flag_ca(cv, x, y, w, h):
    cv.rect(x, y, w // 4, h, (200, 30, 30))
    cv.rect(x + 3 * w // 4, y, w // 4, h, (200, 30, 30))
    cv.rect(x + w // 4, y, w // 2, h, (245, 245, 245))
    cv.poly([(x + w // 2, y + 2), (x + w // 2 + 3, y + h // 2),
             (x + w // 2, y + h - 2), (x + w // 2 - 3, y + h // 2)],
            (200, 30, 30))


def _star4(cv, cx, cy, r, c):
    cv.poly([(cx, cy - r), (cx + r // 3, cy - r // 3), (cx + r, cy),
             (cx + r // 3, cy + r // 3), (cx, cy + r),
             (cx - r // 3, cy + r // 3), (cx - r, cy),
             (cx - r // 3, cy - r // 3)], c)


def scene_gulf(cv, x, y, w, h):
    cv.rect(x, y, w, 22, (198, 214, 224))
    cv.rect(x, y + 22, w, h - 22, (28, 68, 88))
    cv.rect(x, y + 22, w, 2, (120, 170, 190))
    # warship: hull + superstructure + mast + radar dome
    cv.poly([(x + 88, y + 40), (x + 212, y + 40), (x + 200, y + 52),
             (x + 100, y + 52)], (20, 30, 44))
    cv.rect(x + 128, y + 30, 52, 10, (36, 48, 64))
    cv.vline(x + 152, y + 20, y + 30, (20, 30, 44))
    cv.circle(x + 152, y + 18, 3, (20, 30, 44))
    # two drones + missile trail
    cv.ellipse(x + 248, y + 12, 7, 3, (30, 30, 30))
    cv.hline(x + 243, x + 260, y + 12, (30, 30, 30))
    cv.ellipse(x + 272, y + 6, 6, 3, (30, 30, 30))
    cv.hline(x + 268, x + 282, y + 6, (30, 30, 30))
    cv.line(x + 250, y + 14, x + 228, y + 30, (240, 240, 240))
    # explosion starburst + smoke
    _star4(cv, x + 226, y + 30, 9, (255, 170, 40))
    _star4(cv, x + 226, y + 30, 5, (255, 230, 120))
    cv.circle(x + 218, y + 16, 4, (150, 150, 150))
    cv.circle(x + 226, y + 11, 5, (170, 170, 170))
    cv.circle(x + 234, y + 16, 4, (150, 150, 150))
    # waves
    cv.line(x + 20, y + 48, x + 60, y + 48, (140, 190, 210))
    cv.line(x + 240, y + 48, x + 290, y + 48, (140, 190, 210))


def scene_apec(cv, x, y, w, h):
    cv.rect(x, y, w, h, (245, 238, 214))
    cv.circle(x + 296, y + 13, 8, (230, 180, 60))
    # skyline: four towers with lit windows
    for tx, th in ((8, 30), (34, 38), (238, 34), (266, 26), (292, 36)):
        cv.rect(x + tx, y + 54 - th, 20, th, (60, 70, 92))
        for wy in range(y + 54 - th + 4, y + 50, 7):
            for wx in (x + tx + 4, x + tx + 12):
                cv.px(wx, wy, (240, 210, 110))
    # round table + three flags + three seated figures
    cv.ellipse(x + 160, y + 46, 58, 9, (150, 96, 44))
    cv.ellipse(x + 160, y + 44, 58, 9, (178, 122, 62))
    for fx, fl in ((118, _flag_us), (152, _flag_cn), (186, _flag_ru)):
        cv.vline(x + fx + 7, y + 18, y + 36, (90, 70, 40))
        fl(cv, x + fx, y + 8, 15, 10)
    for hx in (128, 160, 192):
        cv.circle(x + hx, y + 34, 4, (40, 40, 40))
        cv.ellipse(x + hx, y + 40, 8, 4, (40, 40, 40))
    cv.rect(x + 102, y + 52, 116, 2, (178, 34, 52))


def scene_akvan(cv, x, y, w, h):
    cv.rect(x, y, w, 30, (205, 225, 235))
    cv.rect(x, y + 30, w, h - 30, (40, 110, 150))
    # coastline + two buildings
    cv.rect(x, y + 46, w, 8, (120, 100, 70))
    cv.rect(x + 20, y + 38, 12, 8, (90, 80, 60))
    cv.rect(x + 280, y + 40, 14, 6, (90, 80, 60))
    # cyclone spiral: rings + arms + eye
    cx, cy = x + 160, y + 26
    for r in (7, 13, 19):
        cv.ring(cx, cy, r, (255, 255, 255))
    for a0 in (20, 140, 260):
        pts = []
        for k in range(7):
            t = math.radians(a0 + k * 18)
            r = 4 + k * 3
            pts.append((int(cx + r * math.cos(t)), int(cy + r * math.sin(t))))
        for i in range(len(pts) - 1):
            cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
                    (255, 255, 255))
    cv.circle(cx, cy, 3, (30, 80, 120))
    # rain streaks + clouds + waves
    for rx in (30, 55, 80, 250, 275, 300):
        cv.line(x + rx, y + 6, x + rx - 4, y + 16, (220, 235, 245))
    cv.ellipse(x + 18, y + 8, 16, 5, (255, 255, 255))
    cv.ellipse(x + 288, y + 6, 14, 5, (255, 255, 255))
    cv.line(x + 60, y + 40, x + 100, y + 40, (200, 230, 240))
    cv.line(x + 220, y + 42, x + 260, y + 42, (200, 230, 240))


def scene_nvidia(cv, x, y, w, h):
    cv.rect(x, y, w, h, (18, 24, 40))
    cv.rect(x + 16, y + 14, 30, 30, (212, 175, 55))
    cv.rect(x + 22, y + 20, 18, 18, (140, 105, 25))
    for px in (20, 26, 32, 38):
        cv.vline(x + px, y + 8, y + 14, (212, 175, 55))
        cv.vline(x + px, y + 44, y + 50, (212, 175, 55))
    # chart line: up, dip, then red fall
    cv.line(x + 6, y + 56, x + 22, y + 44, (60, 200, 90))
    cv.line(x + 22, y + 44, x + 34, y + 48, (60, 200, 90))
    cv.line(x + 34, y + 48, x + 52, y + 30, (60, 200, 90))
    cv.line(x + 52, y + 30, x + 60, y + 40, (220, 60, 60))
    cv.poly([(x + 60, y + 40), (x + 56, y + 40), (x + 58, y + 46)], (220, 60, 60))
    # bars bottom-right
    cv.rect(x + 48, y + 50, 4, 8, (60, 200, 90))
    cv.rect(x + 54, y + 46, 4, 12, (60, 200, 90))
    cv.rect(x + 60, y + 52, 3, 6, (220, 60, 60))
    cv.line(x + 6, y + 12, x + 14, y + 12, (120, 130, 160))


def scene_sudan(cv, x, y, w, h):
    cv.rect(x, y, w, 30, (250, 220, 180))
    cv.rect(x, y + 30, w, h - 30, (210, 170, 110))
    cv.circle(x + 48, y + 12, 7, (240, 180, 60))
    cv.ellipse(x + 8, y + 40, 26, 6, (190, 145, 85))
    cv.ellipse(x + 34, y + 46, 26, 7, (175, 130, 75))
    # drone + small second drone + dust
    cv.ellipse(x + 26, y + 16, 7, 3, (50, 40, 30))
    cv.hline(x + 20, x + 38, y + 16, (50, 40, 30))
    cv.ellipse(x + 46, y + 8, 5, 2, (50, 40, 30))
    cv.hline(x + 42, x + 52, y + 8, (50, 40, 30))
    for dx, dy in ((14, 54), (30, 58), (50, 52)):
        cv.px(x + dx, y + dy, (150, 110, 60))
        cv.px(x + dx + 1, y + dy, (150, 110, 60))


def scene_kerch(cv, x, y, w, h):
    cv.rect(x, y, w, 38, (180, 195, 205))
    cv.rect(x, y + 38, w, h - 38, (50, 100, 140))
    # bridge spans with a gap in the middle
    cv.rect(x + 2, y + 28, 24, 5, (120, 125, 130))
    cv.rect(x + 38, y + 28, 24, 5, (120, 125, 130))
    cv.rect(x + 8, y + 33, 4, 10, (100, 105, 110))
    cv.rect(x + 48, y + 33, 4, 10, (100, 105, 110))
    # fallen arch in the water + smoke + waves
    cv.poly([(x + 26, y + 42), (x + 34, y + 38), (x + 38, y + 46),
             (x + 30, y + 50)], (90, 95, 100))
    cv.circle(x + 30, y + 18, 4, (150, 150, 150))
    cv.circle(x + 32, y + 12, 5, (170, 170, 170))
    cv.circle(x + 28, y + 24, 3, (150, 150, 150))
    cv.line(x + 6, y + 50, x + 22, y + 50, (200, 225, 235))
    cv.line(x + 44, y + 52, x + 58, y + 52, (200, 225, 235))


def scene_knesset(cv, x, y, w, h):
    cv.rect(x, y, w, h, (240, 238, 228))
    cv.rect(x + 10, y + 30, 44, 24, (226, 214, 180))
    cv.ellipse(x + 32, y + 14, 13, 13, (90, 110, 140))
    cv.rect(x + 19, y + 27, 26, 3, (90, 110, 140))
    for cx in (16, 26, 36, 46):
        cv.rect(x + cx, y + 32, 4, 20, (250, 248, 240))
    cv.rect(x + 8, y + 54, 48, 3, (200, 190, 165))
    cv.rect(x + 6, y + 57, 52, 3, (185, 175, 150))
    # small flag + two seat blocks
    cv.vline(x + 54, y + 12, y + 26, (90, 70, 40))
    cv.rect(x + 54, y + 6, 8, 6, (240, 240, 250))
    cv.px(x + 57, y + 8, (30, 60, 160))
    cv.px(x + 58, y + 9, (30, 60, 160))
    cv.rect(x + 12, y + 44, 8, 6, (178, 34, 34))
    cv.rect(x + 44, y + 44, 8, 6, (30, 60, 160))


def scene_eu(cv, x, y, w, h):
    cv.rect(x, y, w, h, (20, 60, 140))
    for k in range(12):
        t = math.radians(k * 30)
        sx = int(x + 32 + 20 * math.cos(t))
        sy = int(y + 32 + 20 * math.sin(t))
        _star4(cv, sx, sy, 3, (255, 220, 60))
    cv.circle(x + 32, y + 32, 11, (212, 175, 55))
    cv.circle(x + 32, y + 32, 8, (230, 195, 90))
    draw_text(cv, "LABEL", x + 27, y + 28, "EUR", NAVY_DK, 0.6)
    cv.rect(x + 6, y + 52, 52, 2, (255, 220, 60))


def scene_gaza(cv, x, y, w, h):
    cv.rect(x, y, w, h, (238, 232, 218))
    for bx, bh in ((4, 26), (18, 34), (36, 22)):
        cv.rect(x + bx, y + 54 - bh, 12, bh, (150, 145, 135))
        cv.rect(x + bx + 2, y + 56 - bh, 3, 3, (90, 90, 85))
    # tents + document with seal + rubble
    cv.poly([(x + 8, y + 58), (x + 14, y + 46), (x + 20, y + 58)], (250, 248, 240))
    cv.poly([(x + 22, y + 58), (x + 28, y + 48), (x + 34, y + 58)], (245, 242, 232))
    cv.rect(x + 40, y + 34, 20, 24, (255, 255, 255))
    cv.outline(x + 40, y + 34, 20, 24, (120, 120, 115))
    for ly in (40, 45, 50):
        cv.hline(x + 43, x + 54, y + ly, (150, 150, 145))
    cv.circle(x + 52, y + 54, 3, (178, 34, 34))
    cv.poly([(x + 44, y + 62), (x + 50, y + 58), (x + 56, y + 62)], (130, 125, 115))
    cv.poly([(x + 56, y + 62), (x + 61, y + 59), (x + 62, y + 62)], (140, 135, 125))


def scene_uk(cv, x, y, w, h):
    cv.rect(x, y, w, h, (200, 210, 220))
    cv.rect(x + 24, y + 8, 16, 46, (60, 65, 75))
    cv.rect(x + 22, y + 4, 20, 5, (45, 50, 60))
    cv.circle(x + 32, y + 20, 8, (245, 245, 240))
    cv.circle(x + 32, y + 20, 7, (60, 65, 75))
    cv.circle(x + 32, y + 20, 6, (245, 245, 240))
    cv.line(x + 32, y + 20, x + 32, y + 15, (30, 30, 30))
    cv.line(x + 32, y + 20, x + 36, y + 22, (30, 30, 30))
    # simplified Union Jack + gavel + base
    cv.rect(x + 46, y + 10, 12, 8, (30, 50, 110))
    cv.hline(x + 46, x + 57, y + 13, (240, 240, 240))
    cv.vline(x + 51, y + 10, y + 17, (240, 240, 240))
    cv.hline(x + 46, x + 57, y + 14, (200, 30, 30))
    cv.rect(x + 6, y + 44, 10, 5, (120, 80, 40))
    cv.line(x + 16, y + 46, x + 24, y + 40, (120, 80, 40))
    cv.rect(x + 6, y + 54, 52, 6, (90, 95, 105))


def scene_china_canada(cv, x, y, w, h):
    cv.rect(x, y, w, 40, (225, 235, 240))
    cv.rect(x, y + 40, w, h - 40, (60, 120, 160))
    # cargo ship + containers
    cv.poly([(x + 6, y + 44), (x + 58, y + 44), (x + 52, y + 56),
             (x + 12, y + 56)], (40, 45, 55))
    cv.rect(x + 16, y + 34, 10, 10, (200, 60, 50))
    cv.rect(x + 28, y + 34, 10, 10, (50, 90, 170))
    cv.rect(x + 40, y + 36, 10, 8, (60, 160, 90))
    cv.rect(x + 22, y + 26, 10, 8, (230, 180, 60))
    # flags + waves
    cv.vline(x + 14, y + 12, y + 26, (90, 70, 40))
    _flag_cn(cv, x + 14, y + 6, 11, 7)
    cv.vline(x + 48, y + 12, y + 26, (90, 70, 40))
    _flag_ca(cv, x + 48, y + 6, 11, 7)
    cv.line(x + 6, y + 60, x + 20, y + 60, (200, 230, 240))
    cv.line(x + 44, y + 60, x + 58, y + 60, (200, 230, 240))


def scene_cop31(cv, x, y, w, h):
    cv.rect(x, y, w, h, (220, 240, 225))
    cv.circle(x + 52, y + 11, 5, (240, 200, 70))
    # globe + land blobs
    cv.circle(x + 24, y + 32, 16, (50, 110, 180))
    cv.ellipse(x + 18, y + 24, 8, 5, (70, 170, 90))
    cv.ellipse(x + 28, y + 36, 9, 5, (70, 170, 90))
    cv.ellipse(x + 22, y + 40, 5, 4, (70, 170, 90))
    # two wind turbines
    for tx, ty, s in ((46, 44, 1.0), (56, 48, 0.7)):
        cv.vline(x + tx, y + ty - int(16 * s), y + ty + 8, (245, 245, 245))
        hx, hy = x + tx, y + ty - int(16 * s)
        for a in (90, 210, 330):
            t = math.radians(a)
            cv.line(hx, hy, int(hx + 9 * s * math.cos(t)),
                    int(hy + 9 * s * math.sin(t)), (245, 245, 245))
        cv.px(hx, hy, (200, 200, 200))
    for dx, dy in ((8, 12), (14, 8), (58, 20)):
        cv.px(x + dx, y + dy, (70, 170, 90))
        cv.px(x + dx + 1, y + dy, (70, 170, 90))


def scene_peltola(cv, x, y, w, h):
    cv.rect(x, y, w, h, (230, 235, 245))
    for sx, sy in ((10, 8), (54, 6), (30, 4)):
        _star4(cv, x + sx, y + sy, 3, (230, 190, 70))
    # capitol dome + columns + base
    cv.ellipse(x + 32, y + 12, 14, 13, (240, 240, 238))
    cv.rect(x + 18, y + 25, 28, 3, (225, 225, 222))
    for cx in (20, 28, 36, 44):
        cv.rect(x + cx, y + 28, 3, 12, (240, 240, 238))
    cv.rect(x + 14, y + 40, 36, 4, (210, 210, 208))
    # 56 / 44 bars with numbers
    cv.rect(x + 12, y + 50, 16, 12, (40, 80, 170))
    cv.rect(x + 34, y + 54, 16, 8, (178, 34, 34))
    draw_text(cv, "LABEL", x + 15, y + 51, "56", CARD, 0.62)
    draw_text(cv, "LABEL", x + 37, y + 55, "44", CARD, 0.62)


LEAD_SCENES = [scene_gulf, scene_apec, scene_akvan]
CARD_SCENES = [scene_nvidia, scene_sudan, scene_kerch, scene_knesset,
               scene_eu, scene_gaza, scene_uk, scene_china_canada,
               scene_cop31, scene_peltola]

# ---------------- layout + render ----------------

def wrap_widths(font, s, widths, scale=1.0):
    """Greedy wrap with a different max width per line."""
    words = s.split(" ")
    lines, cur, li = [], "", 0
    for word in words:
        t = word if not cur else cur + " " + word
        if text_w(font, t, scale) <= widths[li] or not cur:
            cur = t
        else:
            lines.append(cur)
            li += 1
            if li >= len(widths):
                return None
            cur = word
    if cur:
        lines.append(cur)
    return lines


def check():
    """Self-check: every text block must fit its column (0 overflow)."""
    errs = []
    # masthead
    if text_w("MASTHEAD", "WEDNESDAY 18 NOVEMBER 2026") > 992:
        errs.append("date too wide")
    if text_w("ITALIC", "Every story on this page happened, or was first reported, on this day.") > 992:
        errs.append("italic line too wide")
    # leads
    for L in LEADS:
        if text_w("LABEL", L["kicker"]) > 322:
            errs.append("lead kicker %d" % L["num"])
        h = wrap("HEADSR", L["head"], 322, 0.75)
        if len(h) != 2:
            errs.append("lead head %d: %d lines" % (L["num"], len(h)))
        d = wrap("DECK", L["deck"], 322, 0.80)
        if len(d) != 3:
            errs.append("lead deck %d: %d lines" % (L["num"], len(d)))
        if text_w("LABEL", L["caption"], 0.85) > 322:
            errs.append("lead caption %d" % L["num"])
    # cards
    for C in CARDS:
        if text_w("LABEL", C["kicker"]) > 248:
            errs.append("card kicker %d" % C["num"])
        h = wrap("HEAD", C["head"], 248, 0.60)
        if len(h) != 2:
            errs.append("card head %d: %d lines" % (C["num"], len(h)))
        d = wrap_widths("DECK", C["deck"], [248, 248, 168], 0.80)
        if d is None or len(d) > 3:
            errs.append("card deck %d" % C["num"])
    # also
    for a in ALSO:
        if text_w("ALSO11", a, 1.0) > 314:
            errs.append("also too wide: %s" % a[:20])
    # numbers + footer
    for num, _lab in NUMBERS:
        if text_w("HEADSR", num, 0.80) > 248:
            errs.append("number too wide: %s" % num)
    if text_w("ALSO11", FOOTER_1, 1.0) > 992:
        errs.append("footer 1")
    if text_w("ALSO11", FOOTER_2, 1.0) > 992:
        errs.append("footer 2")
    # every string must be renderable (chars in the tables)
    for s in ([L["head"] for L in LEADS] + [L["deck"] for L in LEADS]
              + [C["head"] for C in CARDS] + [C["deck"] for C in CARDS]
              + ALSO + [FOOTER_1, FOOTER_2]):
        for ch in s:
            if ch not in FONTS["DECK"] and ch not in ("\u2014", "\u2019"):
                errs.append("bad char %r in %r" % (ch, s[:24]))
    if errs:
        raise AssertionError("LAYOUT CHECK FAILED: " + "; ".join(errs))


def _badge(cv, cx, cy, r, num, scale):
    cv.circle(cx, cy, r, RED)
    cv.circle(cx, cy, r, RED)
    s = str(num)
    tw = text_w("LABEL", s, scale)
    th = text_h("LABEL") * scale
    draw_text(cv, "LABEL", int(cx - tw / 2), int(cy - th / 2), s, CARD, scale)


def _tag(cv, x, y, w, h, s, scale):
    cv.rect(x, y, w, h, CARD)
    cv.outline(x, y, w, h, RED)
    tw = text_w("LABEL", s, scale)
    draw_text(cv, "LABEL", int(x + (w - tw) / 2),
              int(y + (h - text_h("LABEL") * scale) / 2), s, RED, scale)


def render():
    cv = Canvas(W, H, PAPER)
    # ---- masthead ----
    cv.rect(0, 0, W, 100, NAVY)
    draw_text_c(cv, "LABEL", 512, 8, "THE WORLD IN ONE DAY", GOLD, 1.0)
    draw_text_c(cv, "MASTHEAD", 512, 24, "WEDNESDAY 18 NOVEMBER 2026", CARD, 1.0)
    draw_text_c(cv, "ITALIC", 512, 66,
                "Every story on this page happened, or was first reported, on this day.",
                GOLD_LT, 1.0)
    draw_text_c(cv, "LABEL", 512, 84, "43 STORIES  |  6 CONTINENTS  |  ONE DAY",
                CARD, 1.0)
    cv.rect(0, 98, W, 2, GOLD)
    # ---- leads ----
    for i, L in enumerate(LEADS):
        x = 16 + i * 335
        LEAD_SCENES[i](cv, x, 108, 322, 68)
        cv.rect(x, 160, 322, 16, TEAL)
        draw_text_c(cv, "LABEL", x + 161, 163, L["caption"], CARD, 0.85)
        _tag(cv, x + 238, 113, 76, 14, L["tag"], 0.85)
        _badge(cv, x + 11, 119, 10, L["num"], 0.9)
        draw_text(cv, "LABEL", x, 186, L["kicker"], RED, 1.0)
        for j, ln in enumerate(wrap("HEADSR", L["head"], 322, 0.75)):
            draw_text(cv, "HEADSR", x, 202 + j * 30, ln, INK, 0.75)
        for j, ln in enumerate(wrap("DECK", L["deck"], 322, 0.80)):
            draw_text(cv, "DECK", x, 256 + j * 15, ln, INK_SOFT, 0.80)
    # ---- section divider ----
    draw_text(cv, "LABEL", 16, 298, "TOP STORIES", INK_SOFT, 1.0)
    t = "CARDS 4-13"
    draw_text(cv, "LABEL", 1008 - int(text_w("LABEL", t)), 298, t, INK_SOFT, 1.0)
    # ---- cards ----
    for i, C in enumerate(CARDS):
        x = 16 + (i % 3) * 335
        y = 310 + (i // 3) * 104
        cv.rect(x, y, 322, 96, CARD)
        cv.outline(x, y, 322, 96, CARD_LN)
        CARD_SCENES[i](cv, x + 4, y + 16, 64, 64)
        _badge(cv, x + 12, y + 24, 8, C["num"], 0.62)
        tx = x + 72
        draw_text(cv, "LABEL", tx, y + 6, C["kicker"], RED, 1.0)
        for j, ln in enumerate(wrap("HEAD", C["head"], 248, 0.60)):
            draw_text(cv, "HEAD", tx, y + 20 + j * 19, ln, INK, 0.60)
        for j, ln in enumerate(wrap_widths("DECK", C["deck"], [248, 248, 168], 0.80)):
            draw_text(cv, "DECK", tx, y + 54 + j * 15, ln, INK_SOFT, 0.80)
        _tag(cv, x + 244, y + 82, 72, 12, C["tag"], 0.80)
    # ---- map + also header ----
    draw_text(cv, "HEADXS", 16, 724, "THE WORLD IN 43 STORIES", NAVY, 1.0)
    draw_text(cv, "HEADXS", 368, 724, "ALSO TODAY | 30 MORE STORIES", NAVY, 1.0)
    # ---- map ----
    MX0, MY0, MW, MH = 16, 742, 340, 150
    cv.rect(MX0, MY0, MW, MH, MAP_BG)

    def proj(lon, lat):
        return (MX0 + (lon + 180) / 360.0 * MW,
                MY0 + (75 - lat) / 130.0 * MH)

    for lat, ranges in LAND_ROWS:
        for a, b in ranges:
            for c in range(a, b + 1):
                px, py = proj(c * 5 - 180 + 2.5, lat)
                cv.rect(int(px) - 1, int(py) - 1, 2, 2, MAP_DOT)
    # hairlines + true points first, markers on top
    pts = {}
    for n, (lon, lat) in PLACES.items():
        tx, ty = proj(lon, lat)
        dx, dy = MAP_OFFSETS.get(n, (0, 0))
        pts[n] = (tx, ty, tx + dx, ty + dy)
    for n in range(1, 44):
        tx, ty, x, y = pts[n]
        if (x, y) != (tx, ty):
            cv.line(int(tx), int(ty), int(x), int(y), GRAY)
            cv.circle(int(tx), int(ty), 2, RED)
    for n in range(1, 14):
        _, _, x, y = pts[n]
        _badge(cv, int(x), int(y), 7, n, 0.62)
    for n in range(14, 44):
        _, _, x, y = pts[n]
        cv.circle(int(x), int(y), 2, RED)
    draw_text(cv, "ALSO11", 16, 895,
              "PINS 1-13: LEADS + CARDS  |  DOTS 14-43: ALSO", INK_SOFT, 1.0)
    draw_text(cv, "ALSO11", 16, 909,
              "Hairlines lead from crowded spots to the true place.", INK_SOFT, 1.0)
    # ---- also ----
    for i, a in enumerate(ALSO):
        col = i // 15
        row = i % 15
        ax = 368 + col * 322
        ay = 742 + row * 14
        num, rest = a.split(". ", 1)
        nx = draw_text(cv, "ALSO11", ax, ay, num + ".", RED, 1.0)
        draw_text(cv, "ALSO11", int(nx + 3), ay, rest, INK, 1.0)
    # ---- by the numbers ----
    cv.rect(16, 958, 992, 40, NAVY)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = 16 + i * 248 + 124
        draw_text_c(cv, "HEADSR", cx, 964, num, GOLD_LT, 0.80)
        draw_text_c(cv, "DECKSM", cx, 986, lab, CARD, 0.85)
        if i:
            cv.vline(16 + i * 248, 964, 994, NAVY_DK)
    # ---- footer ----
    draw_text(cv, "ALSO11", 16, 997, FOOTER_1, INK_SOFT, 1.0)
    draw_text(cv, "ALSO11", 16, 1011, FOOTER_2, INK_SOFT, 1.0)
    return cv


def main():
    check()
    cv = render()
    save_png("entry.png", cv.buf, W, H)
    print("rendered entry.png", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()

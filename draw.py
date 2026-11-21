#!/usr/bin/env python3
"""Renders entry.png - a one-page newspaper front page for Saturday 21 November 2026.

Deterministic: no clock, no randomness, no network, no dict-order dependence.
Usage: python3 draw.py [output.png]
"""

import sys
from PIL import Image, ImageDraw, ImageFont

SS = 2                      # supersampling factor
S = 1024                    # final edge in px

PAPER = (251, 249, 244)
CARD = (255, 255, 255)
INK = (24, 21, 16)
MUTED = (94, 89, 78)
FAINT = (138, 132, 118)
RULE = (203, 196, 179)
HAIR = (221, 215, 200)
RED = (158, 28, 33)
NAVY = (22, 48, 76)
GOLD = (176, 130, 42)
TINT = (243, 239, 228)
LAND = (201, 194, 176)
LANDLINE = (160, 152, 133)
WATER = (231, 236, 238)

FD = "/usr/share/fonts/truetype/noto/"
DD = "/usr/share/fonts/truetype/dejavu/"

FILES = {
    "sans": FD + "NotoSans-Condensed.ttf",
    "med": FD + "NotoSans-CondensedMedium.ttf",
    "semi": FD + "NotoSans-CondensedSemiBold.ttf",
    "bold": FD + "NotoSans-CondensedBold.ttf",
    "xbold": FD + "NotoSans-CondensedExtraBold.ttf",
    "black": FD + "NotoSans-CondensedBlack.ttf",
    "serif": FD + "NotoSerif-Regular.ttf",
    "serifb": FD + "NotoSerif-Bold.ttf",
    "serifk": FD + "NotoSerif-Black.ttf",
}

_cache = {}


def F(size, weight="sans"):
    key = (round(size, 2), weight)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FILES[weight], int(round(size * SS)))
    return _cache[key]


class C:
    """Draw wrapper that takes 1024-space coordinates."""

    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(img)

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=1):
        self.d.rectangle(
            [x0 * SS, y0 * SS, x1 * SS, y1 * SS],
            fill=fill, outline=outline,
            width=max(1, int(round(width * SS))))

    def rrect(self, x0, y0, x1, y1, r, fill=None, outline=None, width=1):
        self.d.rounded_rectangle(
            [x0 * SS, y0 * SS, x1 * SS, y1 * SS], radius=r * SS,
            fill=fill, outline=outline,
            width=max(1, int(round(width * SS))))

    def line(self, pts, fill=INK, width=1):
        self.d.line([(p[0] * SS, p[1] * SS) for p in pts], fill=fill,
                    width=max(1, int(round(width * SS))), joint="curve")

    def dash(self, pts, fill=INK, width=1, on=3.0, off=2.5):
        for a, b in zip(pts, pts[1:]):
            ax, ay = a
            bx, by = b
            dx, dy = bx - ax, by - ay
            ln = (dx * dx + dy * dy) ** 0.5
            if ln <= 0.001:
                continue
            ux, uy = dx / ln, dy / ln
            t = 0.0
            while t < ln:
                e = min(t + on, ln)
                self.line([(ax + ux * t, ay + uy * t), (ax + ux * e, ay + uy * e)],
                          fill=fill, width=width)
                t = e + off

    def ell(self, x0, y0, x1, y1, fill=None, outline=None, width=1):
        self.d.ellipse([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=fill,
                       outline=outline, width=max(1, int(round(width * SS))))

    def poly(self, pts, fill=None, outline=None, width=1):
        self.d.polygon([(p[0] * SS, p[1] * SS) for p in pts], fill=fill,
                       outline=outline,
                       width=max(1, int(round(width * SS))))

    def arc(self, x0, y0, x1, y1, a0, a1, fill=INK, width=1):
        self.d.arc([x0 * SS, y0 * SS, x1 * SS, y1 * SS], a0, a1, fill=fill,
                   width=max(1, int(round(width * SS))))

    def text(self, x, y, s, font, fill=INK, anchor="la", spacing=0.0):
        if spacing:
            self.spaced(x, y, s, font, fill, spacing, anchor)
            return
        self.d.text((x * SS, y * SS), s, font=font, fill=fill, anchor=anchor)

    def spaced(self, x, y, s, font, fill, tracking, anchor="la"):
        widths = [self.tw(ch, font) for ch in s]
        total = sum(widths) + tracking * (len(s) - 1)
        cx = x
        if anchor[0] == "m":
            cx = x - total / 2.0
        elif anchor[0] == "r":
            cx = x - total
        for ch, w in zip(s, widths):
            self.d.text((cx * SS, y * SS), ch, font=font, fill=fill, anchor="l" + anchor[1])
            cx += w + tracking

    def tw(self, s, font):
        return self.d.textlength(s, font=font) / SS

    def th(self, font):
        a, d = font.getmetrics()
        return (a + d) / SS


def wrap(s, font, maxw):
    words = s.split()
    lines = []
    cur = ""
    for w in words:
        t = w if not cur else cur + " " + w
        if C_textlen(t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


_len_draw = ImageDraw.Draw(Image.new("L", (4, 4)))


def C_textlen(s, font):
    return _len_draw.textlength(s, font=font) / SS


def para(c, x, y, lines, font, fill, lh, anchor="la"):
    for i, ln in enumerate(lines):
        c.text(x, y + i * lh, ln, font, fill, anchor)


# ---------------------------------------------------------------- geography

NORTH_AMERICA = [
    (-168, 65), (-164, 71), (-150, 71), (-140, 70), (-128, 70), (-120, 69),
    (-110, 68), (-100, 69), (-92, 68), (-82, 70), (-75, 68), (-66, 61),
    (-56, 52), (-60, 47), (-66, 45), (-70, 42), (-74, 39), (-76, 35),
    (-81, 31), (-80, 25), (-83, 28), (-88, 30), (-94, 29), (-97, 26),
    (-97, 21), (-105, 19), (-114, 28), (-120, 34), (-124, 41), (-124, 48),
    (-131, 54), (-140, 59), (-150, 60), (-160, 56), (-166, 60),
]

GREENLAND = [
    (-45, 60), (-33, 67), (-21, 70), (-18, 76), (-24, 82), (-38, 83),
    (-55, 82), (-60, 77), (-56, 68), (-50, 62),
]

SOUTH_AMERICA = [
    (-78, 8), (-72, 11), (-64, 11), (-56, 6), (-50, 1), (-44, -2),
    (-35, -6), (-38, -13), (-42, -23), (-48, -26), (-58, -35), (-62, -40),
    (-66, -45), (-68, -52), (-75, -52), (-73, -45), (-71, -33), (-70, -18),
    (-76, -14), (-81, -5), (-79, 1),
]

AFRICA = [
    (-17, 15), (-16, 21), (-12, 27), (-5, 31), (4, 33), (11, 34), (20, 32),
    (28, 31), (33, 28), (37, 22), (43, 12), (51, 12), (48, 5), (41, -2),
    (40, -10), (35, -20), (33, -26), (27, -34), (18, -34), (13, -24),
    (12, -16), (9, -1), (3, 5), (-4, 5), (-9, 5), (-13, 9),
]

EUROPE_MAINLAND = [
    (-9.4, 38.8), (-9.2, 41.2), (-8.9, 42.6), (-8.0, 43.7), (-4.5, 43.5),
    (-1.8, 43.4), (0.7, 42.7), (3.2, 42.4), (6.9, 43.5), (7.5, 43.7),
    (10.0, 44.0), (12.4, 45.4), (13.6, 45.7), (13.8, 44.9), (16.4, 43.4),
    (18.4, 42.4), (19.3, 41.9), (19.6, 40.4), (21.0, 40.0), (22.5, 40.5),
    (24.0, 40.7), (26.0, 40.8), (28.5, 41.0), (29.2, 41.2), (30.0, 42.5),
    (28.5, 44.5), (29.7, 45.2), (30.5, 46.5), (32.0, 46.2), (33.5, 46.0),
    (35.0, 45.3), (36.5, 45.4), (38.0, 46.6), (39.5, 47.2), (38.5, 48.5),
    (39.5, 49.5), (38.0, 50.2), (35.0, 50.3), (32.0, 50.5), (30.0, 51.5),
    (28.0, 52.0), (26.0, 52.0), (24.0, 52.0), (23.5, 53.5), (24.0, 54.5),
    (23.0, 55.0), (21.0, 55.3), (19.5, 54.4), (16.0, 54.6), (13.5, 54.4),
    (11.0, 54.0), (9.8, 54.6), (8.6, 55.4), (8.2, 54.0), (6.8, 53.5),
    (4.2, 51.4), (1.6, 50.9), (-1.5, 49.7), (-4.7, 48.5), (-2.2, 47.3),
    (-1.2, 46.0), (-1.8, 43.4),
]

BALKANS = [
    (13.6, 45.7), (15.0, 45.5), (17.0, 45.0), (19.0, 45.2), (20.5, 46.0),
    (22.0, 47.5), (24.0, 47.8), (26.0, 48.0), (27.5, 48.2), (29.0, 46.5),
    (28.5, 45.0), (27.5, 44.0), (28.0, 43.0), (28.0, 41.5), (26.5, 40.7),
    (24.0, 40.7), (23.0, 40.3), (22.5, 40.0), (21.0, 39.5), (20.0, 39.0),
    (19.5, 40.5), (19.0, 41.5), (18.5, 42.3), (16.5, 43.3), (15.0, 44.0),
    (13.8, 44.9),
]

ITALY = [
    (8.5, 44.4), (10.0, 43.0), (11.0, 42.4), (12.0, 41.5), (13.5, 41.0),
    (14.0, 40.8), (15.0, 40.0), (15.6, 38.5), (16.0, 38.0), (17.2, 39.0),
    (18.5, 40.2), (16.5, 41.9), (14.0, 42.6), (13.6, 44.0), (12.4, 45.4),
    (12.0, 45.0),
]

SCANDINAVIA = [
    (5.5, 58.9), (7.0, 58.0), (10.8, 59.4), (11.2, 58.9), (12.0, 56.5),
    (12.9, 55.4), (14.3, 55.4), (16.0, 56.2), (16.5, 57.5), (18.5, 59.5),
    (17.5, 60.5), (17.2, 62.0), (19.0, 63.5), (21.5, 64.5), (24.0, 65.5),
    (24.0, 66.5), (22.0, 67.5), (20.0, 68.5), (18.0, 68.5), (16.0, 67.5),
    (14.0, 66.5), (12.0, 65.5), (10.5, 64.0), (8.5, 63.5), (6.5, 62.5),
    (5.0, 61.0), (5.0, 59.5),
]

FINLAND = [
    (21.5, 64.5), (21.0, 63.0), (21.5, 60.5), (23.0, 60.0), (25.0, 60.2),
    (27.0, 60.5), (28.5, 61.0), (30.5, 61.5), (31.5, 63.0), (30.0, 64.5),
    (29.5, 66.0), (29.0, 69.5), (28.0, 69.0), (26.0, 66.0), (24.0, 65.5),
]

RUSSIA_NORTH = [
    (30.0, 50.0), (32.0, 52.0), (34.0, 54.0), (36.0, 56.0), (38.0, 58.0),
    (42.0, 60.0), (46.0, 62.0), (52.0, 64.0), (60.0, 66.0), (60.0, 50.0),
]

ASIA = [
    (30, 70), (40, 68), (50, 69), (60, 72), (70, 73), (80, 74), (90, 76),
    (100, 77), (110, 76), (120, 74), (130, 73), (140, 72), (150, 70),
    (160, 69), (170, 67), (178, 65), (172, 60), (162, 58), (156, 51),
    (144, 47), (136, 44), (130, 43), (127, 38), (122, 37), (120, 33),
    (112, 21), (106, 10), (101, 3), (104, 1), (99, 6), (94, 16), (90, 22),
    (88, 21), (80, 13), (77, 8), (72, 20), (67, 24), (60, 25), (56, 25),
    (50, 30), (43, 12), (37, 22), (33, 28), (28, 31), (24, 38), (22, 42),
    (18, 44), (20, 48), (24, 52), (28, 58), (30, 62),
]

AUSTRALIA = [
    (113, -22), (114, -32), (118, -35), (124, -33), (129, -32), (138, -35),
    (145, -39), (150, -37), (153, -28), (148, -20), (142, -11), (133, -11),
    (126, -14), (122, -18),
]

BRITAIN = [
    (1.7, 52.6), (1.7, 52.9), (0.3, 53.5), (-0.2, 54.1), (-1.1, 54.7),
    (-1.6, 55.6), (-2.1, 56.1), (-1.8, 57.5), (-2.1, 57.7), (-3.0, 58.6),
    (-5.0, 58.6), (-5.7, 57.5), (-5.6, 56.4), (-5.0, 55.7), (-4.8, 54.8),
    (-3.6, 54.5), (-3.0, 53.9), (-3.2, 53.3), (-4.6, 53.3), (-4.1, 52.4),
    (-5.2, 51.7), (-4.0, 51.4), (-3.2, 51.4), (-2.7, 51.5), (-3.0, 51.2),
    (-4.2, 50.4), (-5.0, 50.1), (-5.7, 50.1), (-5.0, 50.8), (-4.5, 51.2),
    (-4.0, 51.8), (-3.0, 51.6), (-1.6, 51.2), (-0.2, 50.8), (0.6, 50.9),
    (1.4, 51.2), (1.7, 52.0),
]

IRELAND = [
    (-6.0, 52.2), (-6.1, 53.3), (-5.9, 54.1), (-6.6, 54.5), (-7.4, 55.2),
    (-8.5, 55.3), (-9.8, 54.6), (-10.2, 54.0), (-9.9, 53.4), (-9.4, 52.6),
    (-10.3, 52.1), (-9.6, 51.6), (-8.3, 51.7), (-7.0, 52.1), (-6.4, 52.2),
]
IRELAND = [
    (-6.0, 52.2), (-6.1, 53.3), (-5.9, 54.1), (-6.6, 54.5), (-7.4, 55.2),
    (-8.5, 55.3), (-9.8, 54.6), (-10.2, 54.0), (-9.9, 53.4), (-9.4, 52.6),
    (-10.3, 52.1), (-9.6, 51.6), (-8.3, 51.7), (-7.0, 52.1), (-6.4, 52.2),
]
JAPAN = [(130, 32), (134, 34), (139, 35), (141, 40), (145, 44), (142, 45),
         (140, 41), (136, 36), (132, 34)]
MADAGASCAR = [(43, -12), (50, -15), (48, -25), (45, -25), (44, -19)]
NZ = [(173, -35), (178, -38), (176, -41), (173, -43), (167, -46), (170, -43),
      (172, -40), (172, -37)]

ANATOLIA = [
    (26.0, 40.8), (26.5, 40.0), (27.5, 39.4), (27.0, 38.5), (27.3, 37.5),
    (28.3, 36.8), (29.5, 36.2), (30.6, 36.2), (31.8, 36.5), (33.5, 36.2),
    (35.0, 36.0), (36.2, 36.6), (36.0, 37.5), (35.5, 38.5), (36.5, 39.5),
    (38.0, 40.2), (39.5, 40.5), (41.5, 41.4), (41.0, 42.5), (39.0, 43.5),
    (37.0, 44.0), (35.0, 45.3), (33.5, 46.0), (32.0, 46.2), (30.5, 46.5),
    (29.7, 45.2), (28.5, 44.5), (30.0, 42.5), (29.2, 41.2), (28.5, 41.0),
    (27.0, 40.7),
]

EUROPE_DETAIL = [
    EUROPE_MAINLAND, ITALY, BALKANS, SCANDINAVIA, FINLAND, RUSSIA_NORTH,
    ANATOLIA, BRITAIN, IRELAND,
    [(12.0, 38.0), (15.5, 38.3), (15.2, 36.7), (12.4, 37.6)],
    [(-8.0, 43.0), (-6.0, 43.6), (-3.0, 43.4), (-2.0, 43.2), (-6.0, 42.8)],
]

CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, ASIA,
              AUSTRALIA, EUROPE_MAINLAND, ITALY, BALKANS, SCANDINAVIA,
              ANATOLIA, BRITAIN, IRELAND, JAPAN, MADAGASCAR, NZ]


def geo_panel(box, lon0, lon1, lat0, lat1, water=WATER):
    """Returns (img, project) for a map panel drawn at supersample scale."""
    x0, y0, x1, y1 = box
    w = int(round((x1 - x0) * SS))
    h = int(round((y1 - y0) * SS))
    img = Image.new("RGB", (w, h), water)
    d = ImageDraw.Draw(img)

    def P(lon, lat):
        px = (lon - lon0) / float(lon1 - lon0) * w
        py = (lat0 - lat) / float(lat0 - lat1) * h
        return (px, py)

    step = 20 if lon1 - lon0 > 200 else 10
    lon = -180
    while lon <= 180:
        if lon0 < lon < lon1:
            a = P(lon, lat0)
            b = P(lon, lat1)
            d.line([a, b], fill=(222, 227, 226), width=1)
        lon += step
    lat = -80
    while lat <= 80:
        if lat1 < lat < lat0:
            a = P(lon0, lat)
            b = P(lon1, lat)
            d.line([a, b], fill=(222, 227, 226), width=1)
        lat += step

    for poly in CONTINENTS:
        pts = [P(lon, la) for lon, la in poly]
        d.polygon(pts, fill=LAND)
        d.line(pts + [pts[0]], fill=LANDLINE, width=max(1, int(SS * 0.7)), joint="curve")
    return img, P


def europe_panel(box, lon0, lon1, lat0, lat1):
    """Accurate European coastline, for the enlarged inset."""
    x0, y0, x1, y1 = box
    w = int(round((x1 - x0) * SS))
    h = int(round((y1 - y0) * SS))
    img = Image.new("RGB", (w, h), WATER)
    d = ImageDraw.Draw(img)

    def P(lon, lat):
        return ((lon - lon0) / float(lon1 - lon0) * w,
                (lat0 - lat) / float(lat0 - lat1) * h)

    for gl in range(-10, 50, 5):
        a, b = P(gl, lat0), P(gl, lat1)
        d.line([a, b], fill=(222, 227, 226), width=1)
    for la in range(30, 65, 5):
        a, b = P(lon0, la), P(lon1, la)
        d.line([a, b], fill=(222, 227, 226), width=1)

    for poly in EUROPE_DETAIL:
        pts = [P(lon, la) for lon, la in poly]
        d.polygon(pts, fill=LAND)
        d.line(pts + [pts[0]], fill=LANDLINE, width=max(1, int(SS * 0.6)), joint="curve")
    return img, P


def pin(img, x, y, num, r=7.4, fill=RED, tcol=(255, 255, 255), fsize=8.6):
    d = ImageDraw.Draw(img)
    x, y = x * SS, y * SS
    r = r * SS
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))
    r2 = r - SS * 0.8
    d.ellipse([x - r2, y - r2, x + r2, y + r2], fill=fill)
    f = ImageFont.truetype(FILES["bold"], int(round(fsize * SS)))
    d.text((x, y + SS * 0.2), str(num), font=f, fill=tcol, anchor="mm")


# ---------------------------------------------------------------- icons

def ibox(c, x, y, w, h, bg=TINT):
    c.rect(x, y, x + w, y + h, fill=bg)
    c.rect(x, y, x + w, y + h, outline=HAIR, width=0.8)


def icon(c, name, x, y, w, h):
    """Wide pictogram tableau. All ink stays inside the padded inner box."""
    ibox(c, x, y, w, h)
    ix0, iy0 = x + 3.0, y + 3.0
    ix1, iy1 = x + w - 3.0, y + h - 3.0
    cx, cy = (ix0 + ix1) / 2.0, (iy0 + iy1) / 2.0
    top, bot = iy0, iy1
    SKY = (206, 217, 226)

    if name == "drones":
        c.rect(ix0, iy0, ix1, iy0 + h * 0.55, fill=SKY)
        for i, bx in enumerate((ix0 + 4, ix0 + 44, ix0 + 82, ix0 + 122, ix0 + 162, ix0 + 200)):
            hh = [6, 10, 7, 12, 8, 5][i]
            c.rect(bx, bot - hh, bx + 8, bot, fill=(138, 130, 112))
        for i in range(4):
            sx = ix0 + 2 + i * 5
            c.line([(sx, bot - 5), (sx + 5, bot - 11), (sx + 2, bot - 19)], fill=INK, width=0.9)
        for dx, dy in ((-84, -1), (-46, 5), (-8, -2), (30, 4), (68, 0)):
            px, py = cx + dx, cy + dy
            c.line([(px - 5, py), (px + 5, py)], fill=INK, width=1.0)
            c.line([(px, py - 3.2), (px, py + 3.2)], fill=INK, width=1.0)
            c.poly([(px - 2.2, py - 1.0), (px + 2.2, py - 1.0), (px, py + 4.4)], fill=INK)
        c.dash([(ix0 + 4, cy + 10), (ix0 + 48, cy + 5), (ix0 + 92, cy + 11),
                (ix0 + 136, cy + 6), (ix0 + 180, cy + 10)], fill=RED, width=0.9, on=3.4, off=3)
        sx, sy = ix1 - 9, cy - 7
        c.poly([(sx, sy - 6.5), (sx + 1.6, sy - 1.6), (sx + 6.5, sy), (sx + 1.6, sy + 1.6),
                (sx, sy + 6.5), (sx - 1.6, sy + 1.6), (sx - 6.5, sy), (sx - 1.6, sy - 1.6)],
               fill=GOLD)

    elif name == "poland":
        fx = ix0 + 2
        c.rect(fx, iy0 + 3, fx + 52, iy0 + 16, fill=(253, 253, 251))
        c.rect(fx, iy0 + 16, fx + 52, iy0 + 29, fill=RED)
        c.rect(fx, iy0 + 3, fx + 52, iy0 + 29, outline=(140, 133, 118), width=0.7)
        c.dash([(fx + 56, iy0 + 11), (fx + 92, iy0 + 7), (fx + 126, iy0 + 13)],
               fill=RED, width=1.0, on=3.4, off=2.6)
        for tx in (fx + 94, fx + 128):
            c.poly([(tx, iy0 + 4), (tx + 6.5, iy0 + 15), (tx - 6.5, iy0 + 15)], fill=INK)
            c.line([(tx, iy0 + 15), (tx, iy0 + 24)], fill=INK, width=1.0)
            c.line([(tx - 4, iy0 + 24), (tx + 4, iy0 + 24)], fill=INK, width=0.7)
        c.rect(ix1 - 66, iy0 + 4, ix1, iy0 + 25, fill=(246, 232, 202), outline=GOLD, width=0.9)

    elif name == "icj":
        px, py = ix0 + 22, cy + 2
        c.rect(px - 7, py + 1, px + 7, py + 4, fill=NAVY)
        c.rect(px - 2, py + 4, px + 2, py + 18, fill=NAVY)
        c.rect(px - 10, py + 18, px + 10, py + 21, fill=NAVY)
        c.ell(px - 4.6, py - 6, px + 4.6, py + 3, fill=NAVY)
        for s2 in (-1, 1):
            c.line([(px + s2 * 12, py + 6), (px + s2 * 20, py + 16)], fill=NAVY, width=1.0)
        c.line([(px + 12, py + 6), (px + 18, py + 1)], fill=NAVY, width=0.9)
        bx = ix0 + 50
        c.rect(bx, iy0 + 2, bx + 58, iy1 - 1, fill=(226, 223, 213), outline=(190, 184, 168), width=0.7)
        for i in range(4):
            c.line([(bx + 5, iy0 + 8 + i * 5), (bx + 53, iy0 + 8 + i * 5)],
                   fill=(150, 143, 128), width=0.8)
        c.rect(bx + 36, iy1 - 11, bx + 54, iy1 - 2, fill=RED)
        c.poly([(bx + 39, iy1 - 9), (bx + 53, iy1 - 3), (bx + 53, iy1 - 9)], fill=(255, 255, 255))
        gx = ix1 - 34
        c.ell(gx - 13, cy - 13, gx + 13, cy + 13, fill=(214, 226, 232), outline=NAVY, width=0.9)
        c.line([(gx - 13, cy), (gx + 13, cy)], fill=NAVY, width=0.6)
        c.arc(gx - 5, cy - 13, gx + 5, cy + 13, 0, 360, fill=NAVY, width=0.6)
        c.ell(gx - 1.6, cy - 13, gx + 1.6, cy + 13, fill=NAVY)

    elif name == "markets":
        c.line([(ix0 + 2, bot), (ix1 - 2, bot)], fill=FAINT, width=0.8)
        c.line([(ix0 + 2, top), (ix0 + 2, bot)], fill=FAINT, width=0.8)
        for i, t in enumerate((0.26, 0.38, 0.50, 0.63, 0.76)):
            bx = ix0 + 8 + i * 22
            c.rect(bx, top + t * (h - 12), bx + 13, bot - 1, fill=(198, 78, 68))
        c.line([(ix0 + 6, top + 5), (ix0 + 50, top + 10), (ix0 + 96, top + 17),
                (ix0 + 142, top + 22), (ix0 + 178, top + 29)], fill=INK, width=1.3)
        for q in ((ix0 + 6, top + 5), (ix0 + 96, top + 17), (ix0 + 178, top + 29)):
            c.ell(q[0] - 1.5, q[1] - 1.5, q[0] + 1.5, q[1] + 1.5, fill=INK)
        ax = ix1 - 14
        c.line([(ax, top + 3), (ax, top + 12)], fill=RED, width=1.2)
        c.poly([(ax - 5, top + 10), (ax + 5, top + 10), (ax, top + 19)], fill=RED)

    elif name == "ukeu":
        fw = 48
        fx = ix0 + 1
        c.rect(fx, iy0 + 2, fx + fw, iy1 - 1, fill=(28, 46, 96))
        c.line([(fx + fw / 2, iy0 + 2), (fx + fw / 2, iy1 - 1)], fill=(252, 252, 250), width=4.0)
        c.line([(fx, cy), (fx + fw, cy)], fill=(252, 252, 250), width=4.0)
        c.line([(fx + fw / 2, iy0 + 2), (fx + fw / 2, iy1 - 1)], fill=(196, 58, 54), width=1.8)
        c.line([(fx, cy), (fx + fw, cy)], fill=(196, 58, 54), width=1.8)
        ex = ix1 - fw - 1
        c.rect(ex, iy0 + 2, ex + fw, iy1 - 1, fill=(24, 46, 110))
        import math as _m
        for k in range(12):
            ang = k * _m.pi / 6 - _m.pi / 2
            c.ell(ex + fw / 2 + 13 * _m.cos(ang) - 1.4, cy + 9.5 * _m.sin(ang) - 1.4,
                  ex + fw / 2 + 13 * _m.cos(ang) + 1.4, cy + 9.5 * _m.sin(ang) + 1.4,
                  fill=(246, 214, 88))
        c.line([(fx + fw + 5, cy - 6), (ex - 8, cy - 6)], fill=INK, width=1.1)
        c.poly([(ex - 4, cy - 6), (ex - 10, cy - 9.5), (ex - 10, cy - 2.5)], fill=INK)

    elif name == "health":
        px, py = ix0 + 26, cy + 1
        c.rrect(px - 22, py - 8, px + 22, py + 8, 8, fill=(255, 255, 255),
                outline=(146, 140, 128), width=0.9)
        c.rrect(px, py - 8, px + 22, py + 8, 8, fill=RED)
        c.rect(px, py - 8, px + 5, py + 8, fill=RED)
        c.line([(px + 3, py), (px + 18, py)], fill=(255, 255, 255), width=1.5)
        for i, sc in enumerate((1.0, 0.76, 0.5, 0.28)):
            sx3 = ix0 + 62 + i * 40
            c.rrect(sx3, cy - 12 * sc, sx3 + 34, cy + 12 * sc, 2.4,
                    fill=(248, 248, 245), outline=NAVY, width=0.9)
            c.rect(sx3 + 1, cy - 0.9, sx3 + 33, cy + 0.9, fill=(212, 218, 226))
        c.line([(ix0 + 56, cy), (ix1 - 2, cy)], fill=(206, 200, 186), width=0.7)

    elif name == "climate":
        gx, gy, gr = ix0 + 14, cy + 2, 11
        c.ell(gx - gr, gy - gr, gx + gr, gy + gr, fill=(214, 226, 232), outline=NAVY, width=0.9)
        c.arc(gx - gr, gy - gr / 2.4, gx + gr, gy + gr / 2.4, 0, 360, fill=NAVY, width=0.6)
        c.arc(gx - gr / 2.4, gy - gr, gx + gr / 2.4, gy + gr, 0, 360, fill=NAVY, width=0.6)
        c.line([(gx - gr, gy), (gx + gr, gy)], fill=NAVY, width=0.6)
        c.rect(ix0 + 34, iy0, ix1 - 30, iy1, fill=(214, 220, 208))
        for i in range(6):
            bx = ix0 + 38 + i * 20
            ht = 4 + i * 2.4
            c.rect(bx, bot - ht, bx + 11, bot, fill=(136, 128, 110))
            c.poly([(bx - 2, bot - ht), (bx + 5.5, bot - ht - 5), (bx + 13, bot - ht)],
                   fill=(176, 130, 42))
        tx = ix1 - 10
        c.rrect(tx, iy0 + 1, tx + 8, bot - 3, 4, fill=(255, 255, 255),
                outline=(122, 118, 110), width=0.8)
        c.ell(tx - 2, bot - 8, tx + 10, bot + 4, fill=RED)
        c.rect(tx + 2, bot - 7, tx + 6, bot - 1, fill=RED)

    elif name == "cyber":
        sx4 = ix0 + 22
        c.poly([(sx4, iy0 + 1), (sx4 + 22, iy0 + 8), (sx4 + 22, cy + 5), (sx4, cy + 14),
                (sx4 - 22, cy + 5), (sx4 - 22, iy0 + 8)],
               fill=(216, 226, 234), outline=NAVY, width=1.1)
        c.rrect(sx4 - 7, cy - 3, sx4 + 7, cy + 7, 2, fill=NAVY)
        c.arc(sx4 - 5, cy - 11, sx4 + 5, cy, 180, 360, fill=NAVY, width=1.4)
        for i in range(5):
            bx2 = ix0 + 56 + i * 30
            c.rect(bx2, iy0 + 2, bx2 + 24, iy0 + 9, fill=(184, 190, 196))
            c.rect(bx2, iy0 + 11, bx2 + 24, iy1 - 1, fill=(200, 206, 212))
            for j in range(4):
                c.line([(bx2 + 3, iy0 + 14 + j * 3.4), (bx2 + 21, iy0 + 14 + j * 3.4)],
                       fill=(132, 127, 118), width=0.6)
        c.dash([(ix0 + 56, iy0 + 6), (ix0 + 86, iy0 + 3), (ix0 + 116, iy0 + 7),
                (ix0 + 146, iy0 + 4), (ix0 + 176, iy0 + 8)], fill=RED, width=1.0, on=3.2, off=2.6)

    elif name == "protest":
        for i, dx in enumerate((-92, -58, -24, 10, 44, 78)):
            px2 = cx + dx
            hh = [7, 11, 8, 12, 9, 6][i]
            c.line([(px2, bot), (px2, bot - hh)], fill=INK, width=1.2)
            c.ell(px2 - 2.8, bot - hh - 5.6, px2 + 2.8, bot - hh, fill=INK)
            c.line([(px2, bot - hh + 2), (px2 - 5, bot - hh + 8)], fill=INK, width=1.0)
            c.line([(px2, bot - hh + 2), (px2 + 5, bot - hh + 9)], fill=INK, width=1.0)
            c.rect(px2 - 9, bot - hh - 13, px2 + 9, bot - hh - 7,
                   fill=(255, 255, 255), outline=RED, width=0.8)
            c.line([(px2 - 4, bot - hh - 10), (px2 + 4, bot - hh - 10)], fill=RED, width=0.8)

    elif name == "diplomacy":
        for i, (c1, c2) in enumerate((((250, 250, 248), (196, 58, 54)),
                                      ((30, 48, 92), (196, 58, 54)),
                                      ((250, 250, 248), (30, 48, 92)))):
            fx2 = ix0 + 2 + i * 40
            c.line([(fx2, iy0 + 2), (fx2, iy1 - 1)], fill=INK, width=1.1)
            c.rect(fx2 + 1, iy0 + 3, fx2 + 30, iy0 + 16, fill=c1)
            c.rect(fx2 + 1, iy0 + 9.5, fx2 + 30, iy0 + 16, fill=c2)
            c.rect(fx2 + 1, iy0 + 3, fx2 + 30, iy0 + 16, outline=(150, 143, 128), width=0.5)
        tx2 = ix1 - 74
        c.rrect(tx2, cy - 11, tx2 + 72, cy + 11, 3, fill=(232, 227, 214),
                outline=NAVY, width=0.8)
        c.line([(tx2 + 6, cy - 4), (tx2 + 60, cy - 4)], fill=(150, 143, 128), width=0.7)
        c.line([(tx2 + 6, cy + 1), (tx2 + 50, cy + 1)], fill=(150, 143, 128), width=0.7)
        c.line([(tx2 + 6, cy + 6), (tx2 + 40, cy + 6)], fill=(150, 143, 128), width=0.7)

    elif name == "gulf":
        for dx, ww, hh in ((-102, 13, 12), (-86, 9, 19), (-74, 14, 15),
                           (-57, 8, 22), (-46, 12, 17), (-31, 10, 24),
                           (-18, 9, 16), (-6, 12, 20)):
            bx3 = cx + dx
            c.rect(bx3, bot - hh, bx3 + ww, bot, fill=(190, 182, 162),
                   outline=(132, 124, 106), width=0.7)
            for j in range(int(hh / 4)):
                c.line([(bx3 + 2, bot - hh + 3 + j * 4), (bx3 + ww - 2, bot - hh + 3 + j * 4)],
                       fill=(160, 152, 134), width=0.5)
        for dx, dy in ((10, -5), (28, 0), (46, -6), (64, -1), (82, -6), (96, 1)):
            sx5, sy5 = cx + dx, cy + dy
            c.poly([(sx5, sy5 - 6.5), (sx5 + 1.5, sy5 - 1.5), (sx5 + 6.5, sy5),
                    (sx5 + 1.5, sy5 + 1.5), (sx5, sy5 + 6.5), (sx5 - 1.5, sy5 + 1.5),
                    (sx5 - 6.5, sy5), (sx5 - 1.5, sy5 - 1.5)], fill=GOLD)
            c.arc(sx5 - 10, sy5 - 10, sx5 + 10, sy5 + 10, 40, 140, fill=GOLD, width=0.7)
        c.dash([(ix0 + 2, iy0 + 11), (ix0 + 18, iy0 + 6), (ix0 + 34, iy0 + 14),
                (ix0 + 50, iy0 + 8)], fill=RED, width=1.0, on=3.2, off=2.6)

    elif name == "space":
        ex2 = ix0 + 16
        c.ell(ex2 - 10, cy - 10, ex2 + 10, cy + 10, fill=(96, 146, 190), outline=NAVY, width=0.9)
        c.arc(ex2 - 10, cy - 4, ex2 + 10, cy + 4, 0, 360, fill=(60, 110, 150), width=0.7)
        c.arc(ex2 - 10, cy - 10, ex2 + 10, cy + 10, 200, 340, fill=(196, 218, 234), width=0.8)
        c.dash([(ex2 + 13, cy), (ix0 + 70, cy - 7), (ix0 + 122, cy + 1),
                (ix0 + 172, cy - 6), (ix1 - 34, cy - 2)], fill=FAINT, width=0.9, on=3, off=3)
        for i in range(4):
            c.ell(ix0 + 56 + i * 32, iy0 + 2 + (i % 2) * 4,
                  ix0 + 57.6 + i * 32, iy0 + 3.6 + (i % 2) * 4, fill=FAINT)
        px3, py3 = ix1 - 28, cy
        c.poly([(px3 - 9, py3), (px3 + 6, py3 - 5.5), (px3 + 6, py3 + 5.5)],
               fill=(216, 212, 200), outline=INK, width=0.7)
        c.arc(px3 + 2, py3 - 9, px3 + 21, py3 + 9, 270, 90, fill=INK, width=1.2)
        c.line([(px3 + 12, py3), (px3 + 25, py3)], fill=INK, width=0.9)
        c.line([(px3 - 5, py3 - 6), (px3 - 13, py3 - 12)], fill=INK, width=0.9)
        c.line([(px3 - 5, py3 + 6), (px3 - 13, py3 + 12)], fill=INK, width=0.9)


# ---------------------------------------------------------------- content
# (number, kicker, icon, headline, body, region, field)

FEATURES = [
    (1, "KYIV, UKRAINE", "drones",
     "Russia fires 400 drones and 110 missiles at Ukraine",
     "At least eight people killed in Kyiv; bridges and railway stations damaged. A strike on Kryvyi Rih wounds about 20.",
     "Europe", "conflict"),
    (2, "WARSAW, POLAND", "poland",
     "Two Russian missiles come down inside Poland",
     "Warsaw calls the intrusion a deliberate provocation; NATO allies express solidarity with Poland.",
     "Europe", "conflict"),
    (3, "THE HAGUE", "icj",
     "World Court: Myanmar committed genocide against Rohingya",
     "The ICJ holds a state responsible for genocide for the first time, over the 2017 military campaign.",
     "Europe", "justice"),
    (4, "NEW YORK", "markets",
     "Wall Street slides as Nasdaq erases its 2026 gains",
     "The S&P 500 and Dow close in correction as an AI-sector sell-off deepens. Friday's close, reported today.",
     "Americas", "markets"),
    (5, "BRUSSELS", "ukeu",
     "UK and EU sign their biggest post-Brexit deals",
     "Food exports, carbon markets and youth mobility for 100,000 young Britons; PM Andy Burnham signs.",
     "Europe", "politics"),
    (6, "LONDON", "health",
     "Trial pill clears pancreatic cancer on scans in 1 in 12",
     "Daraxonrasib left no visible tumour in one patient in twelve. Doctors call it promising, not a cure.",
     "Europe", "science & tech"),
    (7, "ANTALYA, TURKEY", "climate",
     "COP31 runs past its deadline over fossil fuels",
     "Nearly 200 nations remain deadlocked in Antalya as the presidency extends the talks by an extra day.",
     "Europe", "climate"),
    (8, "WASHINGTON", "cyber",
     "FBI criminal database reportedly hacked amid outages",
     "US outages continue; the White House dismisses the National Cyber Director, naming Kristen Davis interim.",
     "Americas", "science & tech"),
    (9, "BERLIN", "protest",
     "Gen Z protests spread to 25 European countries",
     "Marches over housing, pay and climate widen from Berlin; organisers report demos in 25 countries.",
     "Europe", "society"),
    (10, "WASHINGTON", "diplomacy",
     "Trump defends his ties to Putin and Xi",
     "After the Shenzhen summit he calls Putin \u201cmy friend\u201d in a 90-minute press conference; Zelensky calls Putin a killer.",
     "Americas", "politics"),
    (11, "RIYADH", "gulf",
     "Coalition intercepts Houthi missiles over Riyadh",
     "A third night running. The Houthis threaten ports and a power station; interceptions light the sky.",
     "Middle East", "conflict"),
    (12, "DEEP SPACE", "space",
     "Voyager 1 becomes the first object one light-day out",
     "Launched in 1977, the probe is 25.9 billion km away, so its radio signals now take a day to reach Earth.",
     "Space", "science & tech"),
]

BRIEFS = [
    (13, "Gaza: strikes kill Palestinians; EU urges Israel to keep the ceasefire", "Middle East", "conflict"),
    (14, "Spain: 29 Nov election as conservatives gain; S\u00e1nchez admits mistakes", "Europe", "politics"),
    (15, "Estonia to close its border crossings with Russia", "Europe", "politics"),
    (16, "Georgia: Tbilisi gas blast collapses flats; six dead, a child among them", "Asia", "society"),
    (17, "S Korea: court quashes Han Duck-soo's 15-year martial-law sentence", "Asia", "justice"),
    (18, "El Salvador: Bukele registers for a third term; vote on 28 Feb 2027", "Americas", "politics"),
    (19, "Venezuela: US court lets Trump end protected status for 600,000", "Americas", "justice"),
    (20, "Bayer to pay up to $11bn over 20 years to settle Roundup suits", "Americas", "markets"),
    (21, "CLAIM: Anthropic mathematician says his AI produced a Riemann proof", "Americas", "science & tech"),
    (22, "NASA halts Perseverance and Mars Odyssey science over faults", "Space", "science & tech"),
    (23, "Crypto liquidations pass $2bn as Bitcoin slides toward $62,000", "Americas", "markets"),
    (24, "India: Cyclone Akvan crosses the Odisha coast with heavy rain", "Asia", "climate"),
    (25, "India: NSE becomes world's 5th-largest listed exchange, past Nasdaq", "Asia", "markets"),
    (26, "India: Modi tours Bengal, Bihar and UP; IIT Kharagpur turns 75", "Asia", "politics"),
    (27, "Cricket: Jaiswal and KL Rahul share a record stand in Wellington", "Asia", "sport"),
    (28, "Hockey: India women beat Malaysia 4-1 in Asian Champions Trophy", "Asia", "sport"),
    (29, "Indonesia: fire economic losses could reach $30bn", "Asia", "markets"),
    (30, "Los Angeles: man convicted of starting the deadly Palisades fire", "Americas", "justice"),
    (31, "Haiti: Salvadoran troops lose soldiers to explosives", "Americas", "conflict"),
    (32, "Austria: foreign ministry confirms hack; staff contacts viewed", "Europe", "science & tech"),
    (33, "France: Depardieu and Houellebecq probed over rape allegations", "Europe", "justice"),
    (34, "US: Indian national sentenced to 19 years over Pannun murder plot", "Americas", "justice"),
    (35, "TikTok launches a global tool to detect and report AI deepfakes", "Americas", "science & tech"),
    (36, "Nvidia faces a US accounting probe; California summons over affair", "Americas", "markets"),
    (37, "Trump proposes a \u201ctremendous\u201d tax on data centres built abroad", "Americas", "politics"),
    (38, "Israel advances a plan for a new West Bank city of 200,000", "Middle East", "politics"),
    (39, "Tennis: Zverev beats Fils 6-4, 7-6 to reach ATP Finals semis", "Europe", "sport"),
    (40, "Cincinnati Zoo: Fiona the hippo dies", "Americas", "society"),
    (41, "\u201cHunger Games\u201d prequel takes $21m in Thursday previews", "Americas", "society"),
    (42, "NFL: Rams receiver Puka Nacua likely out for the season", "Americas", "sport"),
    (43, "Nepal: PM Balendra Shah to visit India on 22-23 November", "Asia", "politics"),
    (44, "Massachusetts to weigh Lindsay Clancy's appeal against charges", "Americas", "justice"),
    (45, "China, Russia and the US issue a Shenzhen declaration on peace", "Asia", "politics"),
    (46, "Trump: \u201cno immediate hurry\u201d on Iran; US weighs further action", "Americas", "politics"),
    (47, "Iraq: eight oil officials arrested over fraudulent procurement", "Middle East", "justice"),
    (48, "Botswana-born cheetah gives birth to four cubs at Kuno, India", "Asia", "science & tech"),
]

NUMBERS = [
    ("400+", "drones fired"),
    ("110", "missiles"),
    ("8", "killed in Kyiv"),
    ("1 in 12", "scans clear"),
    ("100,000", "young Britons"),
    ("$11bn", "Bayer payout"),
    ("$2bn", "liquidated"),
    ("25", "protest countries"),
]

REGION_ORDER = ["Americas", "Europe", "Asia", "Middle East", "Space"]
FIELD_ORDER = ["politics", "conflict", "science & tech", "justice", "markets", "society", "sport", "climate"]

PIN_INDEX = [
    (1, "Kyiv", "400+ drones"),
    (2, "Warsaw", "missiles land"),
    (3, "The Hague", "ICJ ruling"),
    (4, "New York", "sell-off"),
    (5, "Brussels", "UK\u2013EU deals"),
    (6, "London", "cancer pill"),
    (7, "Antalya", "COP31 overruns"),
    (8, "Washington", "FBI hack"),
    (9, "Berlin", "Gen Z demos"),
    (10, "Washington", "Putin, Xi"),
    (11, "Riyadh", "intercepts"),
    (12, "Deep space", "1 light-day"),
]

WORLD_LABELS = [
    ("N. AMERICA", -101, 62), ("S. AMERICA", -60, -20), ("AFRICA", 20, 5),
    ("ASIA", 92, 46), ("AUSTRALIA", 134, -28),
]

ALL_STORIES = [(f[0], f[5], f[6]) for f in FEATURES] + [(b[0], b[2], b[3]) for b in BRIEFS]


def tally():
    reg = {}
    fld = {}
    for _, r, f in ALL_STORIES:
        reg[r] = reg.get(r, 0) + 1
        fld[f] = fld.get(f, 0) + 1
    return reg, fld


# ---------------------------------------------------------------- render

def main(out_path="entry.png"):
    reg, fld = tally()
    assert len(ALL_STORIES) == 48, len(ALL_STORIES)
    assert sum(reg.values()) == 48 and sum(fld.values()) == 48

    img = Image.new("RGB", (S * SS, S * SS), PAPER)
    c = C(img)
    M = 16
    W = S - 2 * M
    R = S - M

    # ------------------------------------------------ top rail
    c.spaced(M, 13.2, "THE WORLD IN ONE DAY", F(11.4, "xbold"), RED, 1.7)
    c.text(R, 13.6, "EARLY EDITION   \u00b7   No. 325   \u00b7   48 STORIES",
           F(9.6, "semi"), MUTED, anchor="ra")
    c.line([(M, 27.2), (R, 27.2)], fill=INK, width=1.3)
    c.line([(M, 29.6), (R, 29.6)], fill=INK, width=0.5)

    # ------------------------------------------------ masthead
    title = "SATURDAY 21 NOVEMBER 2026"
    size = 58
    while size > 30 and c.tw(title, F(size, "serifk")) > W - 10:
        size -= 1
    c.text(S / 2.0, 33, title, F(size, "serifk"), INK, anchor="ma")

    deck = ("Russian missiles land in Poland, the World Court finds genocide in Myanmar and Wall Street's "
            "AI rally ends \u2014 forty-eight stories, twelve of them pictured, from one Saturday on Earth.")
    df = F(11.5, "serif")
    dl = wrap(deck, df, W - 210)
    para(c, S / 2.0, 95, dl, df, (56, 52, 44), 13.2, anchor="ma")

    y = 95 + len(dl) * 13.2 + 3.4
    c.line([(M, y), (R, y)], fill=INK, width=1.1)
    c.line([(M, y + 2.8), (R, y + 2.8)], fill=INK, width=0.5)
    y += 8
    c.spaced(S / 2.0, y,
             "48 STORIES   \u00b7   12 FEATURES   \u00b7   36 BRIEFS   \u00b7   %d REGIONS   \u00b7   %d FIELDS"
             % (len(reg), len(fld)),
             F(9.6, "xbold"), NAVY, 1.5, anchor="ma")
    y += 12
    c.line([(M, y), (R, y)], fill=RULE, width=0.9)

    # ------------------------------------------------ features
    fy = y + 6
    gx, gy = 8.0, 8.0
    cw = (W - 3 * gx) / 4.0
    ch = 126.0
    for n, kicker, ic, hl, body, _r, _f in FEATURES:
        col, row = (n - 1) % 4, (n - 1) // 4
        x0 = M + col * (cw + gx)
        y0 = fy + row * (ch + gy)
        c.rect(x0, y0, x0 + cw, y0 + ch, fill=CARD, outline=HAIR, width=0.9)
        c.rect(x0, y0, x0 + cw, y0 + 2.4, fill=NAVY if n <= 3 else RULE)
        c.ell(x0 + 5.5, y0 + 6.5, x0 + 21.5, y0 + 22.5, fill=RED)
        c.text(x0 + 13.5, y0 + 14.8, str(n), F(9.8, "black"), (255, 255, 255), anchor="mm")
        c.spaced(x0 + 25, y0 + 9.0, kicker, F(9.4, "xbold"), NAVY, 0.5)
        icon(c, ic, x0 + 5, y0 + 25, cw - 10, 34)
        hf = F(11.8, "bold")
        hl_lines = wrap(hl, hf, cw - 12)
        if len(hl_lines) > 2:
            hf = F(11.0, "bold")
            hl_lines = wrap(hl, hf, cw - 12)
        if len(hl_lines) > 2:
            raise SystemExit("headline too long: %r" % hl)
        hy = y0 + 63
        para(c, x0 + 6, hy, hl_lines, hf, INK, 12.2)
        bf = F(9.7, "sans")
        bl = wrap(body, bf, cw - 12)
        if len(bl) > 3:
            raise SystemExit("body too long (%d lines): %r" % (len(bl), body))
        byy = hy + len(hl_lines) * 12.2 + 2.6
        para(c, x0 + 6, byy, bl, bf, (50, 46, 39), 10.6)
        if byy + len(bl) * 10.6 > y0 + ch - 3:
            raise SystemExit("feature %d overflows" % n)

    # ------------------------------------------------ map band
    my0 = fy + 3 * ch + 2 * gy + 7
    mh = 171.0
    c.line([(M, my0 - 6), (R, my0 - 6)], fill=INK, width=1.0)
    c.spaced(M, my0 - 2.6, "WHERE IT HAPPENED", F(9.6, "xbold"), NAVY, 1.4)
    c.text(R, my0 - 2.4, "numbered pins match the feature cards above", F(9.5, "sans"), MUTED, anchor="ra")

    wbox = (M, my0 + 1, M + 470, my0 + 1 + mh)
    wimg, WP = geo_panel(wbox, -180, 180, 76, -54)
    img.paste(wimg, (int(wbox[0] * SS), int(wbox[1] * SS)))
    c = C(img)
    c.rect(wbox[0], wbox[1], wbox[2], wbox[3], outline=HAIR, width=0.9)

    def wl(lon, lat):
        px, py = WP(lon, lat)
        return px / SS + wbox[0], py / SS + wbox[1]

    for lab, lon, lat in WORLD_LABELS:
        lx, ly = wl(lon, lat)
        c.spaced(lx, ly, lab, F(8.9, "xbold"), (118, 110, 92), 1.0, anchor="ma")

    ex0, ey0 = wl(-11, 60)
    ex1, ey1 = wl(42, 33)
    c.rect(ex0, ey0, ex1, ey1, outline=RED, width=0.9)
    c.rect(ex0, ey0, ex0 + 52, ey0 + 9, fill=RED)
    c.spaced(ex0 + 3, ey0 + 0.8, "EUROPE \u2192", F(8.5, "xbold"), (255, 255, 255), 0.5)

    def wp(lon, lat, n, dx, dy, r=7.2):
        px, py = wl(lon, lat)
        c.ell(px - 2.3, py - 2.3, px + 2.3, py + 2.3, fill=RED)
        c.line([(px, py), (px + dx * 0.72, py + dy * 0.72)], fill=RED, width=0.8)
        pin(img, px + dx, py + dy, n, r=r)

    wp(-74.0, 40.7, 4, 12, -13)
    wp(-77.0, 38.9, 8, -17, -12)
    wp(-77.0, 38.9, 10, -14, 14)
    wp(46.7, 24.7, 11, 13, 11)

    vx, vy = wbox[2] - 28, my0 + 26
    c.dash([(wbox[2] - 116, vy + 24), (vx - 12, vy + 6)], fill=NAVY, width=0.9, on=3.2, off=2.8)
    c.poly([(vx - 7, vy + 3), (vx - 17, vy - 1), (vx - 17, vy + 7)], fill=NAVY)
    pin(img, vx, vy, 12, r=7.2, fill=NAVY)
    c.spaced(wbox[2] - 3, my0 + mh - 9, "1 LIGHT-DAY OUT", F(8.7, "xbold"), NAVY, 0.5, anchor="ra")

    # Europe inset
    ebox = (M + 478, my0 + 1, M + 684, my0 + 118)
    eimg, EP = europe_panel(ebox, -12, 48, 62, 28)
    img.paste(eimg, (int(ebox[0] * SS), int(ebox[1] * SS)))
    c = C(img)
    c.rect(ebox[0], ebox[1], ebox[2], ebox[3], outline=INK, width=1.0)
    c.rect(ebox[0] - 2.6, ebox[1] - 2.6, ebox[2] + 2.6, ebox[3] + 2.6, outline=RULE, width=0.7)
    c.rect(ebox[0], ebox[1], ebox[0] + 96, ebox[1] + 12, fill=NAVY)
    c.spaced(ebox[0] + 4, ebox[1] + 2.5, "EUROPE, ENLARGED", F(8.6, "xbold"), (255, 255, 255), 0.7)

    def el(lon, lat):
        px, py = EP(lon, lat)
        return px / SS + ebox[0], py / SS + ebox[1]

    for n, lon, lat, dx, dy in [
        (6, -0.13, 51.51, -16, 14),
        (3, 4.30, 52.08, 8, -16),
        (5, 4.35, 50.85, 2, 17),
        (9, 13.40, 52.52, 16, -11),
        (2, 21.01, 52.23, 14, -13),
        (1, 30.52, 50.45, 17, -6),
        (7, 30.71, 36.90, 16, 3),
    ]:
        px, py = el(lon, lat)
        c.ell(px - 2.3, py - 2.3, px + 2.3, py + 2.3, fill=RED)
        c.line([(px, py), (px + dx * 0.76, py + dy * 0.76)], fill=RED, width=0.8)
        pin(img, px + dx, py + dy, n, r=7.0)

    c.spaced(ebox[0], ebox[3] + 3.8, "EUROPEAN PINS 1 \u00b7 2 \u00b7 3 \u00b7 5 \u00b7 6 \u00b7 7 \u00b7 9",
             F(9.2, "xbold"), (122, 114, 96), 0.7)
    c.text(ebox[0], ebox[3] + 16.2,
           "Seven of the twelve stories broke inside this box; the",
           F(9.6, "sans"), (70, 66, 56))
    c.text(ebox[0], ebox[3] + 27.8,
           "world map keeps the same numbers so they read together.",
           F(9.6, "sans"), (70, 66, 56))

    # pin index
    ix = M + 692
    c.line([(ix - 6, my0 + 1), (ix - 6, my0 + 1 + mh)], fill=HAIR, width=0.8)
    c.spaced(ix, my0 + 3.2, "PIN INDEX", F(9.2, "xbold"), NAVY, 1.0)
    for i, (n, place, what) in enumerate(PIN_INDEX):
        col, row = i // 6, i % 6
        cx0 = ix + col * 156
        ry = my0 + 17 + row * 24.2
        c.text(cx0 + 12, ry + 1.4, str(n), F(10.2, "black"), RED, anchor="ra")
        c.text(cx0 + 17, ry, place, F(10.2, "bold"), INK)
        c.text(cx0 + 17, ry + 10.2, what, F(9.5, "sans"), MUTED)

    # ------------------------------------------------ briefs
    by = my0 + mh + 10
    c.line([(M, by), (R, by)], fill=INK, width=1.1)
    c.spaced(M, by + 3.8, "ALSO ON 21 NOVEMBER", F(9.6, "xbold"), NAVY, 1.4)
    c.text(R, by + 4.0, "briefs 13\u201348", F(9.5, "sans"), MUTED, anchor="ra")
    by += 16

    colw = (W - 2 * 14) / 3.0
    rows = 12
    rowh = 11.9
    for i, (n, txt, _r, _f) in enumerate(BRIEFS):
        col, row = i // rows, i % rows
        x0 = M + col * (colw + 14)
        y0 = by + row * rowh
        if col:
            c.line([(x0 - 7, by - 3), (x0 - 7, by + rows * rowh - 3)], fill=HAIR, width=0.7)
        c.text(x0 + 15, y0 + 1.9, str(n), F(9.4, "xbold"), RED, anchor="ra")
        bf = F(9.7, "sans")
        if C_textlen(txt, bf) > colw - 22:
            raise SystemExit("brief %d too wide: %r" % (n, txt))
        c.text(x0 + 19, y0 + 1.4, txt, bf, (42, 38, 32))

    # ------------------------------------------------ date check
    dy = by + rows * rowh + 3
    c.line([(M, dy), (R, dy)], fill=INK, width=1.0)
    dtop = dy + 3
    dc = ("Excluded because first reported BEFORE 21 November: Anthropic's $81bn IPO debut (19\u201320 Nov) \u00b7 "
          "the Houthi strike that damaged Riyadh's PIF tower (Thu 19 Nov) \u00b7 the Shenzhen Trump\u2013Xi\u2013Putin "
          "summit itself (20 Nov) \u00b7 Voyager 1's 1977 launch, of which only today's light-day milestone is news \u00b7 "
          "the Palisades fire itself (Jan 2025), of which only today's conviction is news.")
    dfont = F(9.7, "sans")
    dl2 = wrap(dc, dfont, W - 112)
    dh = 6.5 + len(dl2) * 10.9 + 4.5
    c.rect(M, dtop, R, dtop + dh, fill=(247, 241, 227))
    c.rect(M, dtop, M + 3, dtop + dh, fill=GOLD)
    c.spaced(M + 8, dtop + 3.4, "DATE CHECK", F(9.4, "xbold"), (122, 84, 12), 1.15)
    para(c, M + 66, dtop + 3.2, dl2, dfont, (88, 66, 22), 10.9)

    # ------------------------------------------------ day in numbers
    ny = dtop + dh + 5
    c.line([(M, ny), (R, ny)], fill=RULE, width=0.9)
    c.spaced(M, ny + 8.4, "THE DAY IN NUMBERS", F(9.4, "xbold"), NAVY, 1.1)
    x = M + 118
    cwid = (R - x) / len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        px = x + i * cwid
        if i:
            c.line([(px - 5, ny + 4), (px - 5, ny + 31)], fill=HAIR, width=0.7)
        c.text(px, ny + 1.6, num, F(15.2, "black"), RED)
        c.text(px, ny + 19.0, lab, F(9.5, "sans"), MUTED)

    # ------------------------------------------------ footer
    jy = ny + 34
    c.line([(M, jy), (R, jy)], fill=INK, width=1.0)
    c.text(M, jy + 3.4,
           "Note to the judge: every one of the 48 numbered items was first reported on Saturday 21 November 2026. "
           "The five older stories in DATE CHECK are named only to show they were excluded. Item 21 is marked CLAIM: "
           "it awaits expert verification.",
           F(9.6, "sans"), (58, 54, 46))
    rline = "Regions: " + " \u00b7 ".join("%s %d" % (k, reg[k]) for k in REGION_ORDER if reg.get(k))
    fline = "Fields: " + " \u00b7 ".join("%s %d" % (k, fld[k]) for k in FIELD_ORDER if fld.get(k))
    c.text(M, jy + 15.8, rline + ".     " + fline + ".", F(9.6, "sans"), (58, 54, 46))
    c.text(M, jy + 28.0,
           "Sources: BBC News, Al Jazeera, Financial Times, The Guardian, Reuters, AP \u2014 all reporting on 21 November 2026.",
           F(9.6, "semi"), MUTED)

    img = img.resize((S, S), Image.LANCZOS)
    img.save(out_path, optimize=True)
    return out_path


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "entry.png")

"""shopmap.py — the shop map as inline SVG: streets, moat, wall, the walk from Tha Phae Gate.

Equal metres on both axes; the scale bar is computed from the projection. Colours are CSS
variables so the map follows the page into dark mode.
"""
from __future__ import annotations

import math
from html import escape

W = 800  # viewBox width; height follows the box's aspect in metres


class Proj:
    def __init__(self, box):
        s, w, n, e = box
        self.s, self.w, self.n, self.e = box
        lat0 = (s + n) / 2
        self.kx = 111320 * math.cos(math.radians(lat0))
        self.ky = 110540
        self.wm = (e - w) * self.kx
        self.hm = (n - s) * self.ky
        self.k = W / self.wm                      # px per metre
        self.H = round(self.hm * self.k)

    def xy(self, p):
        return ((p[1] - self.w) * self.kx * self.k, (self.n - p[0]) * self.ky * self.k)

    def inside(self, p):
        x, y = self.xy(p)
        return 0 <= x <= W and 0 <= y <= self.H


def _d(P, pts, close=False):
    xy = [P.xy(p) for p in pts]
    s = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    return s + ("Z" if close else "")


def _label_at(P, streets, name, near):
    """Label position and angle on the named street, at the vertex nearest `near`."""
    best = None
    for s in streets:
        if s["name"] != name:
            continue
        for i, p in enumerate(s["pts"]):
            if not P.inside(p):
                continue
            d = (p[0] - near[0]) ** 2 + (p[1] - near[1]) ** 2
            if best is None or d < best[0]:
                a = s["pts"][max(i - 1, 0)]
                b = s["pts"][min(i + 1, len(s["pts"]) - 1)]
                best = (d, p, a, b)
    if not best:
        return None
    _, p, a, b = best
    (x1, y1), (x2, y2) = P.xy(a), P.xy(b)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if ang > 90:
        ang -= 180
    elif ang < -90:
        ang += 180
    x, y = P.xy(p)
    return x, y, ang


def svg(g: dict, walk_m: int, walk_min: int) -> str:
    P = Proj(g["box"])
    H = P.H
    out = [f'<svg class="map" viewBox="0 0 {W} {H}" role="img" '
           f'aria-labelledby="map-t map-d" xmlns="http://www.w3.org/2000/svg">',
           '<title id="map-t">แผนที่ร้าน · Shop map</title>',
           f'<desc id="map-d">Prostar Magic Shop on Kotchasarn Road, outside the east moat. '
           f'Walking route from Tha Phae Gate: {walk_m} metres.</desc>',
           f'<defs><clipPath id="mc"><rect width="{W}" height="{H}" rx="0"/></clipPath></defs>',
           f'<g clip-path="url(#mc)"><rect width="{W}" height="{H}" class="m-land"/>']
    for a in g["water"]:
        out.append(f'<path class="m-water" d="{_d(P, a, True)}"/>')
    for c in g["canals"]:
        out.append(f'<path class="m-canal" d="{_d(P, c["pts"])}"/>')
    ranked = sorted(g["streets"], key=lambda s: -s["r"])
    widths = {2: 11, 3: 10, 4: 8, 5: 5}
    for layer in ("case", "fill"):
        for s in ranked:
            w = widths[s["r"]] + (2.2 if layer == "case" else 0)
            cls = f"m-{layer}" + (" m-major" if layer == "fill" and s["r"] <= 3 else "")
            out.append(f'<path class="{cls}" stroke-width="{w}" d="{_d(P, s["pts"])}"/>')
    for w_ in g["wall"]:
        out.append(f'<path class="m-wall" d="{_d(P, w_)}"/>')
    out.append(f'<path class="m-walk-halo" d="{_d(P, g["walk"]["pts"])}"/>')
    out.append(f'<path class="m-walk" d="{_d(P, g["walk"]["pts"])}"/>')

    # street names: (name, English, near this point, screen offset east/south in px)
    for name, en, near, off in (("ถนนคชสาร", "Kotchasarn", (18.7873, 98.99335), (15, 0)),
                                ("ถนนมูลเมือง", "Moon Muang", (18.7866, 98.99255), (-15, 0)),
                                ("ถนนท่าแพ", "Tha Phae", (18.78815, 98.9964), (0, -12)),
                                ("ถนนช้างคลาน", "Chang Khlan", (18.7806, 98.9975), (0, -12))):
        at = _label_at(P, g["streets"], name, near)
        if not at:
            continue
        x, y, ang = at
        x, y = x + off[0], y + off[1]
        out.append(f'<text class="m-st" x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" '
                   f'transform="rotate({ang:.1f} {x:.1f} {y:.1f})">'
                   f'{escape(name.replace("ถนน", "ถ."))} · <tspan lang="en">{escape(en)}</tspan></text>')

    # moat label, on the water between the two moat roads
    mx, my = P.xy((18.7843, 98.99292))
    out.append(f'<text class="m-water-l" x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" '
               f'transform="rotate(-90 {mx:.1f} {my:.1f})">คูเมือง · <tspan lang="en">moat</tspan></text>')

    # places
    gx, gy = P.xy(g["gate"])
    out.append(f'<g class="m-place"><rect x="{gx - 7:.1f}" y="{gy - 7:.1f}" width="14" height="14" rx="2"/>'
               f'<text x="{gx - 14:.1f}" y="{gy - 6:.1f}" text-anchor="end">ประตูท่าแพ</text>'
               f'<text class="en" x="{gx - 14:.1f}" y="{gy + 16:.1f}" text-anchor="end" lang="en">Tha Phae Gate</text></g>')
    wx, wy = P.xy(g["wat"])
    out.append(f'<g class="m-place m-wat"><circle cx="{wx:.1f}" cy="{wy:.1f}" r="6"/>'
               f'<text x="{wx - 12:.1f}" y="{wy + 7:.1f}" text-anchor="end">วัดทรายมูล</text></g>')

    # walk label, halfway along the route
    pts = g["walk"]["pts"]
    hx, hy = P.xy(pts[len(pts) // 2])
    out.append(f'<g class="m-walk-l"><rect x="{hx + 18:.1f}" y="{hy - 21:.1f}" width="206" height="42" rx="21"/>'
               f'<text x="{hx + 121:.1f}" y="{hy + 7:.1f}" text-anchor="middle">เดิน {walk_m} ม. · {walk_min} นาที</text></g>')

    # the shop
    sx, sy = P.xy(g["shop"])
    out.append(f'<g class="m-shop"><circle class="m-pulse" cx="{sx:.1f}" cy="{sy:.1f}" r="22"/>'
               f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="12"/>'
               f'<path d="M{sx:.1f},{sy - 7:.1f} l2.1,4.4 4.8,.6 -3.5,3.3 .9,4.8 -4.3,-2.3 -4.3,2.3 .9,-4.8 -3.5,-3.3 4.8,-.6z" class="m-star"/>'
               f'<rect x="{sx + 24:.1f}" y="{sy - 25:.1f}" width="252" height="50" rx="10"/>'
               f'<text x="{sx + 150:.1f}" y="{sy + 9:.1f}" text-anchor="middle" lang="en">PROSTAR MAGIC</text></g>')

    # scale bar and north
    bar_m = 200
    bl = bar_m * P.k
    out.append(f'<g class="m-scale" transform="translate(24,{H - 34})">'
               f'<rect width="{bl:.1f}" height="6"/><rect width="{bl / 2:.1f}" height="6" class="m-scale-a"/>'
               f'<text x="0" y="-9">0</text><text x="{bl:.1f}" y="-9" text-anchor="middle">{bar_m} ม.</text></g>')
    out.append(f'<g class="m-north" transform="translate({W - 40},46)"><circle r="20"/>'
               f'<path d="M0,-13 L7,6 L0,2 L-7,6Z"/><text y="30" text-anchor="middle" lang="en">N</text></g>')
    out.append(f'<text class="m-credit" x="{W - 10}" y="{H - 10}" text-anchor="end" lang="en">'
               f'© OpenStreetMap contributors</text>')
    out.append("</g></svg>")
    return "".join(out)


def gate(g: dict) -> list[str]:
    """Sanity checks before a map ships: frame, axes, route ends, ground present."""
    P = Proj(g["box"])
    errs = []
    for k in ("shop", "gate", "wat"):
        lat, lon = g[k]
        if not (18 < lat < 19.5 and 98 < lon < 100):
            errs.append(f"{k}: lat/lon look swapped or out of Chiang Mai: {g[k]}")
        if not P.inside(g[k]):
            errs.append(f"{k}: outside the map frame")
    def m(a, b):
        k = math.cos(math.radians(a[0]))
        return math.hypot((a[0] - b[0]) * 110540, (a[1] - b[1]) * 111320 * k)
    if m(g["walk"]["pts"][0], g["gate"]) > 60:
        errs.append("walk does not start at the gate")
    if m(g["walk"]["pts"][-1], g["shop"]) > 60:
        errs.append("walk does not end at the shop")
    snap = min(m(g["shop"], p) for s in g["streets"] for p in s["pts"])
    if snap > 200:
        errs.append(f"shop pin {snap:.0f} m from any street")
    if len(g["streets"]) < 50 or not g["water"]:
        errs.append("map has no ground (streets or water missing)")
    return errs

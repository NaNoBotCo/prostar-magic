"""art.py — the drawn pictures: the stage (hero and share card) and the Burn tile.

Inline SVG, seeded so every build draws the same sparkles. Sparkles carry class "tw"; the page
animates them only when reduced motion is not asked for.
"""
from __future__ import annotations

import random

from magic import rabbit_g

GOLD = "#f0c454"


def _sparkle(uid, x, y, s, delay, cls="tw"):
    return (f'<use href="#{uid}spk" class="{cls}" style="animation-delay:{delay:.2f}s" '
            f'transform="translate({x:.0f},{y:.0f}) scale({s:.2f})"/>')


def _card(x, y, rot, rank, suit, red, i=0, origin=(1240, 616)):
    col = "#c3142d" if red else "#1b1424"
    anim = f'--dx:{origin[0] - x}px;--dy:{origin[1] - y}px;--d:{.9 + i * .18:.2f}s'
    return (f'<g transform="translate({x},{y}) rotate({rot})"><g class="rise" style="{anim}">'
            f'<rect x="-36" y="-52" width="72" height="104" rx="9" fill="#fdf8ee" stroke="#d9c79c" stroke-width="2"/>'
            f'<text x="-26" y="-28" font-size="22" font-weight="700" fill="{col}" font-family="Georgia,serif">{rank}</text>'
            f'<text x="0" y="16" font-size="40" text-anchor="middle" fill="{col}">{suit}</text></g></g>')


def stage_svg(uid: str = "s") -> str:
    rnd = random.Random(7)
    stars = "".join(f'<circle cx="{rnd.uniform(0, 1600):.0f}" cy="{rnd.uniform(90, 620):.0f}" '
                    f'r="{rnd.uniform(.8, 2.2):.1f}" fill="#fff" opacity="{rnd.uniform(.15, .6):.2f}"/>'
                    for _ in range(90))
    hx, fy = 1240, 800           # hat centre, stage floor
    # cards and sparkles rising out of the hat along an arc to the upper left
    cards = "".join(_card(x, y, r, k, s, red, i) for i, (x, y, r, k, s, red) in enumerate((
        (1190, 520, -12, "A", "♥", True), (1105, 405, -26, "K", "♠", False),
        (1040, 300, -40, "Q", "♦", True), (975, 200, -55, "J", "♣", False))))
    sp = [(1265, 560, 1.4), (1150, 470, 1.0), (1215, 430, .7), (1060, 350, 1.2), (980, 400, .6),
          (960, 250, .9), (860, 170, 1.3), (1040, 200, .5), (820, 280, .7), (1320, 480, .8),
          (1290, 380, .5), (760, 150, .6), (1180, 300, .6), (700, 230, .9), (1400, 300, .7),
          (560, 160, .5), (1480, 180, 1.0), (620, 330, .6)]
    sparks = "".join(_sparkle(uid, x, y, s, i * .37) for i, (x, y, s) in enumerate(sp))
    valance = "M0,0 H1600 V70 " + " ".join(
        f"Q{1600 - i * 100 - 50},{128} {1600 - (i + 1) * 100},70" for i in range(16)) + " Z"
    fringe = "M0,70 " + " ".join(
        f"Q{i * 100 + 50},{132} {(i + 1) * 100},70" for i in range(16))
    return f'''<svg class="stage" viewBox="0 0 1600 900" preserveAspectRatio="xMaxYMax slice" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
<defs>
<radialGradient id="{uid}bg" cx="72%" cy="62%" r="80%"><stop offset="0" stop-color="#3d1344"/><stop offset=".5" stop-color="#1c0b25"/><stop offset="1" stop-color="#08040c"/></radialGradient>
<linearGradient id="{uid}cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4cf" stop-opacity=".55"/><stop offset="1" stop-color="#fff4cf" stop-opacity=".04"/></linearGradient>
<radialGradient id="{uid}pool" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffe9a8" stop-opacity=".55"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
<radialGradient id="{uid}glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffd76a" stop-opacity=".85"/><stop offset=".4" stop-color="#f0a83a" stop-opacity=".35"/><stop offset="1" stop-color="#f0a83a" stop-opacity="0"/></radialGradient>
<linearGradient id="{uid}fold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3b040d"/><stop offset=".3" stop-color="#8e1024"/><stop offset=".5" stop-color="#c41f39"/><stop offset=".72" stop-color="#7c0c1d"/><stop offset="1" stop-color="#34030b"/></linearGradient>
<pattern id="{uid}velvet" width="64" height="900" patternUnits="userSpaceOnUse"><rect width="64" height="900" fill="url(#{uid}fold)"/></pattern>
<linearGradient id="{uid}shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset=".35" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></linearGradient>
<linearGradient id="{uid}gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbe39a"/><stop offset=".5" stop-color="#e2b04a"/><stop offset="1" stop-color="#9b6b1c"/></linearGradient>
<linearGradient id="{uid}hat" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b0a10"/><stop offset=".45" stop-color="#2c2a36"/><stop offset=".6" stop-color="#15141b"/><stop offset="1" stop-color="#050408"/></linearGradient>
<clipPath id="{uid}hatclip"><rect x="-200" y="0" width="400" height="{fy - 182}"/></clipPath>
<path id="{uid}spk" d="M0,-12 C1.8,-1.8 1.8,-1.8 12,0 C1.8,1.8 1.8,1.8 0,12 C-1.8,1.8 -1.8,1.8 -12,0 C-1.8,-1.8 -1.8,-1.8 0,-12Z" fill="{GOLD}"/>
</defs>
<rect width="1600" height="900" fill="url(#{uid}bg)"/>
<g>{stars}</g>
<polygon points="{hx - 60},0 {hx + 60},0 {hx + 330},{fy + 10} {hx - 330},{fy + 10}" fill="url(#{uid}cone)" opacity=".55"/>
<rect y="{fy}" width="1600" height="{900 - fy}" fill="#140914"/>
<path d="M0,{fy} H1600" stroke="url(#{uid}gold)" stroke-width="3" opacity=".7"/>
<ellipse cx="{hx}" cy="{fy + 8}" rx="380" ry="62" fill="url(#{uid}pool)"/>
<ellipse cx="{hx}" cy="{fy - 190}" rx="240" ry="190" fill="url(#{uid}glow)"/>
<g>{cards}</g>
<g class="sparks">{sparks}</g>
<g transform="translate({hx},0)">
 <ellipse cx="0" cy="{fy + 4}" rx="118" ry="20" fill="#000" opacity=".55"/>
 <path d="M-92,{fy - 180} L-80,{fy} Q0,{fy + 14} 80,{fy} L92,{fy - 180} Z" fill="url(#{uid}hat)"/>
 <path d="M-90,{fy - 150} L-88,{fy - 120} Q0,{fy - 108} 88,{fy - 120} L90,{fy - 150} Q0,{fy - 138} -90,{fy - 150}Z" fill="#b3122b"/>
 <ellipse cx="0" cy="{fy - 182}" rx="150" ry="30" fill="#1a1820" stroke="#3a3744" stroke-width="2"/>
 <ellipse cx="0" cy="{fy - 184}" rx="96" ry="17" fill="#000"/>
 <ellipse cx="0" cy="{fy - 186}" rx="80" ry="11" fill="#ffd76a" opacity=".35"/>
 <g clip-path="url(#{uid}hatclip)"><g class="bun"><g transform="translate(-72,{fy - 184 - 150}) scale(1.2)">{rabbit_g()}</g></g></g>
 <path d="M-96,{fy - 184} A96,17 0 0 0 96,{fy - 184}" fill="none" stroke="#2c2a36" stroke-width="4"/>
</g>
<g transform="translate({hx + 190},{fy - 20}) rotate(-28)"><rect x="-7" y="-150" width="14" height="300" rx="4" fill="#0d0c12"/><rect x="-7" y="-150" width="14" height="40" rx="4" fill="#fdf8ee"/><rect x="-7" y="110" width="14" height="40" rx="4" fill="#fdf8ee"/></g>
<path d="M0,0 H300 C280,260 230,430 170,560 C140,640 160,770 220,900 H0Z" fill="url(#{uid}velvet)"/>
<path d="M0,0 H300 C280,260 230,430 170,560 C140,640 160,770 220,900 H0Z" fill="url(#{uid}shade)"/>
<path d="M1600,0 H1500 C1510,260 1530,430 1555,560 C1570,640 1560,770 1540,900 H1600Z" fill="url(#{uid}velvet)"/>
<path d="M1600,0 H1500 C1510,260 1530,430 1555,560 C1570,640 1560,770 1540,900 H1600Z" fill="url(#{uid}shade)"/>
<path d="M150,585 q30,-24 58,-6" stroke="url(#{uid}gold)" stroke-width="10" fill="none" stroke-linecap="round"/>
<circle cx="214" cy="582" r="11" fill="url(#{uid}gold)"/>
<path d="{valance}" fill="url(#{uid}velvet)"/>
<path d="{valance}" fill="url(#{uid}shade)"/>
<path d="{fringe}" stroke="url(#{uid}gold)" stroke-width="7" fill="none"/>
</svg>'''


def burn_svg() -> str:
    return f'''<svg viewBox="0 0 400 310" preserveAspectRatio="xMidYMid slice" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
<defs>
<radialGradient id="bbg" cx="55%" cy="40%" r="75%"><stop offset="0" stop-color="#4a1630"/><stop offset="1" stop-color="#0c0610"/></radialGradient>
<linearGradient id="bfl" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ff5a1f"/><stop offset=".5" stop-color="#ffb02e"/><stop offset="1" stop-color="#fff2a8"/></linearGradient>
<radialGradient id="bgl" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffb02e" stop-opacity=".6"/><stop offset="1" stop-color="#ffb02e" stop-opacity="0"/></radialGradient>
<path id="spk2" d="M0,-12 C1.8,-1.8 1.8,-1.8 12,0 C1.8,1.8 1.8,1.8 0,12 C-1.8,1.8 -1.8,1.8 -12,0 C-1.8,-1.8 -1.8,-1.8 0,-12Z" fill="{GOLD}"/>
</defs>
<rect width="400" height="310" fill="url(#bbg)"/>
<ellipse cx="236" cy="96" rx="120" ry="90" fill="url(#bgl)"/>
<g transform="translate(220,150) rotate(12)">
 <rect x="-62" y="-88" width="124" height="176" rx="12" fill="#fdf8ee" stroke="#d9c79c" stroke-width="3"/>
 <path d="M-62,-40 L-30,-88 H62 V-10 Q30,-30 10,-60 Q-10,-30 -62,-40Z" fill="#2a1a14" opacity=".85"/>
 <text x="-46" y="70" font-size="30" font-weight="700" fill="#c3142d" font-family="Georgia,serif">7</text>
 <text x="0" y="40" font-size="58" text-anchor="middle" fill="#c3142d">♥</text>
</g>
<path d="M250,70 C215,40 238,10 226,-10 C262,14 280,40 272,62 C290,52 292,34 288,22 C312,48 306,84 282,98 C270,104 256,92 250,70Z" fill="url(#bfl)"/>
<path d="M262,84 C250,66 262,50 258,38 C276,52 282,70 274,86Z" fill="#fff6c8"/>
<use href="#spk2" class="tw" transform="translate(110,70) scale(1)"/>
<use href="#spk2" class="tw" style="animation-delay:.6s" transform="translate(330,220) scale(.8)"/>
<use href="#spk2" class="tw" style="animation-delay:1.2s" transform="translate(80,200) scale(.6)"/>
<use href="#spk2" class="tw" style="animation-delay:1.8s" transform="translate(350,60) scale(.5)"/>
</svg>'''


def card_html(fonts_dir: str, count: int, lo: int, hi: int) -> str:
    """The 1200×630 share card as a page, for headless Chrome to photograph."""
    return f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:600;src:url({fonts_dir}/prompt-600-latin.woff2)}}
@font-face{{font-family:P;font-weight:600;src:url({fonts_dir}/prompt-600-thai.woff2);unicode-range:U+0E00-0E7F}}
@font-face{{font-family:S;font-weight:600;src:url({fonts_dir}/sarabun-600-latin.woff2)}}
@font-face{{font-family:S;font-weight:600;src:url({fonts_dir}/sarabun-600-thai.woff2);unicode-range:U+0E00-0E7F}}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#08040c}}
.stage{{position:absolute;inset:0;width:1200px;height:630px}}
.scrim{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,4,12,.92) 0%,rgba(8,4,12,.75) 42%,rgba(8,4,12,0) 68%)}}
.tx{{position:absolute;left:70px;top:112px;color:#fff;font-family:S}}
.m1{{font:600 124px/1 P;color:#f0c454;letter-spacing:4px;text-shadow:2px 2px 0 #c3142d,4px 4px 0 #9a1024,6px 6px 0 #5a0915,0 0 40px rgba(240,196,84,.4)}}
.m2{{font:600 44px/1 P;letter-spacing:14px;margin:14px 0 30px 4px}}
.th{{font:600 44px/1.3 P}}
.l{{font:600 30px/1.5 S;color:#e9dfcf}}
.g{{font:600 30px/1.5 S;color:#f0c454;margin-top:14px}}
</style></head><body>{stage_svg("c")}<div class="scrim"></div>
<div class="tx"><div class="m1">PROSTAR</div><div class="m2">MAGIC SHOP</div>
<div class="th">โปรสตาร์ แมจิก ช้อป</div><div class="l">อุปกรณ์มายากล · โชว์ · สอน · ถนนคชสาร เชียงใหม่</div>
<div class="g">{count} tricks · ฿{lo:,}–฿{hi:,}</div></div></body></html>'''

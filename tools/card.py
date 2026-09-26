"""card.py — the 1200×630 share card and the graded hero photo.

Background (the storefront), scrim (heaviest where the words sit), text. Figures on the card
are passed in from the build, which computes them from the catalogue.
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from common import ASSETS, DATA

FONTS = ASSETS / "fonts"
GOLD = (240, 196, 84)
INK = (18, 13, 28)


def font(name: str, size: int):
    return ImageFont.truetype(str(FONTS / name), size)


FACE = {"display": "prompt-600", "bold": "sarabun-600", "body": "sarabun-400"}


def mixed(d, xy, text: str, size: int, face: str, fill) -> None:
    """Draw text run by run: Thai-range characters (including ฿) in the thai subset, the rest
    in the latin subset, since each woff2 carries one script."""
    x, y = xy
    for run in re.findall(r"[\u0e00-\u0e7f]+|[^\u0e00-\u0e7f]+", text):
        script = "thai" if "\u0e00" <= run[0] <= "\u0e7f" else "latin"
        f = font(f"{FACE[face]}-{script}.woff2", size)
        d.text((x, y), run, font=f, fill=fill)
        x += d.textlength(run, font=f)


def graded_storefront() -> Image.Image:
    """The ride photo is washed out by the sun; pull the levels back before using it."""
    im = Image.open(DATA / "snapshot" / "motdang-storefront.jpg").convert("RGB")
    im = ImageOps.autocontrast(im, cutoff=(2, 1))
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.15)
    return im


def cover(im: Image.Image, w: int, h: int, focus_y: float = 0.62) -> Image.Image:
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * focus_y)
    return im.crop((x, y, x + w, y + h))


def hero(out: Path) -> None:
    im = graded_storefront()
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    im.save(out, "JPEG", quality=76, optimize=True, progressive=True)


def share_card(out: Path, count: int, lo: int, hi: int) -> None:
    W, H = 1200, 630
    bg = cover(graded_storefront(), W, H)
    scrim = Image.new("L", (W, H))
    px = scrim.load()
    for x in range(W):
        a = 245 if x < 520 else max(70, int(245 - (x - 520) * 0.3))
        for y in range(H):
            px[x, y] = a
    dark = Image.new("RGB", (W, H), INK)
    card = Image.composite(dark, bg, scrim)
    d = ImageDraw.Draw(card)
    d.rectangle((0, 0, 14, H), fill=(195, 20, 45))
    # marquee bulbs along the top edge
    for i in range(0, W, 34):
        d.ellipse((i + 20, 22, i + 30, 32), fill=GOLD if (i // 34) % 2 == 0 else (120, 90, 40))
    d.text((64, 96), "PROSTAR", font=font("prompt-600-latin.woff2", 118), fill=GOLD)
    d.text((64, 214), "MAGIC SHOP", font=font("prompt-600-latin.woff2", 72), fill=(255, 255, 255))
    mixed(d, (66, 318), "โปรสตาร์ แมจิก ช้อป", 50, "display", (255, 255, 255))
    mixed(d, (66, 392), "อุปกรณ์มายากล · โชว์ · สอน", 38, "bold", (230, 222, 210))
    mixed(d, (66, 452), f"{count} tricks · ฿{lo:,}–฿{hi:,}", 34, "display", GOLD)
    d.text((66, 548), "Kotchasarn Rd · Chiang Mai", font=font("sarabun-400-latin.woff2", 30), fill=(210, 200, 190))
    card.save(out, "JPEG", quality=86, optimize=True, progressive=True)

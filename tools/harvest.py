#!/usr/bin/env python3
"""harvest.py — the catalogue, read off the shop's own homepage.

prostar-magic.com serves one frozen page (a June 2024 copy); every product, cart and menu
link on it returns 404. That page still carries 140 products with names, codes and prices,
so it is the source. Product pictures come from the shop's image host and are resized here,
so the built site loads them from its own folder.

    python3 tools/harvest.py            # parse + fetch missing pictures
    python3 tools/harvest.py --no-fetch # parse only
"""
from __future__ import annotations

import base64
import html
import io
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ASSETS, DATA, UA, jdump  # noqa: E402

SNAP = DATA / "snapshot" / "prostar-magic.com-home.html"
SNAP_DATE = "2024-06-18"   # the archive stamp in the page's own image URLs (20240618020513)
PICS = ASSETS / "products"

# Code prefix → shelf. DvD-* rows are instruction videos and downloads of other magicians'
# work; they are left out of this site and counted in the build log.
SHELF = {"Card": "cards", "J": "cards", "Coin": "coins", "Bill": "coins", "Mind": "mind",
         "Stage": "stage", "Dove": "stage", "Ball": "stage", "GE": "closeup", "ST": "closeup",
         "Glass": "closeup", "Dice": "closeup", "Toy": "closeup", "Pro": "closeup"}
# Pro-* is a starter line that mixes shelves; these names say which.
PRO = {"Pro-023": "cards", "Pro-002": "cards", "Pro-017": "coins", "Pro-013": "coins"}
TEACH = re.compile(r"คลิปสอน|แผ่นสอน|VCD\s*สอน|DVD\s*สอน|วิธีการแสดง|Instructions|สอนการแสดง", re.I)


def parse() -> tuple[list, dict]:
    s = SNAP.read_text(encoding="utf-8", errors="ignore")
    seen, rows, left_out = set(), [], {"video": 0, "download": 0}
    for m in re.finditer(r'<div class="entry-thumbnail.*?<div class="entry-utility">', s, re.S):
        b = m.group(0)
        g = lambda p: (re.search(p, b, re.S) or [None, None])[1]  # noqa: E731
        pid = g(r'"id":(\d+)')
        if not pid or pid in seen:
            continue
        seen.add(pid)
        code = (g(r"รหัสสินค้า ([^<]*)</span>") or "").strip()
        desc = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                             g(r'<div class="entry-content clearfix">(.*?)</div>') or ""))).strip()
        if code.startswith("DvD"):
            left_out["video"] += 1
            continue
        if re.search(r"download", desc, re.I):
            left_out["download"] += 1
            continue
        prefix = re.sub(r"[-\d]+$", "", code)
        shelf = PRO.get(code) or SHELF.get(prefix)
        if not shelf:
            raise SystemExit(f"no shelf for {code}")
        nums = [float(x.replace(",", "")) for x in
                re.findall(r"฿([\d,\.]+)", g(r'class="product-price[^"]*">(.*?)</span>') or "")]
        thumb = g(r'<img[^>]+src="(https://thumbnail[^"]+)"')
        orig = None
        if thumb:
            token = thumb.split("/resize/")[1].split("/")[0]
            q = urllib.parse.parse_qs(base64.b64decode(token + "==").decode("utf-8", "ignore"))
            orig = q.get("img", [None])[0]
        name = html.unescape(g(r'title="([^"]*)"') or "").strip()
        desc = desc.rstrip(".").rstrip()
        rows.append({
            "id": pid, "code": code, "name": name, "shelf": shelf,
            "price": int(nums[-1]) if nums else None,
            "was": int(nums[0]) if len(nums) == 2 else None,
            "blurb": desc, "teach": bool(TEACH.search(desc)),
            "img_src": orig, "img": f"products/{pid}.jpg" if orig else None,
        })
    return rows, left_out


def fetch(rows: list) -> None:
    from PIL import Image
    PICS.mkdir(parents=True, exist_ok=True)
    for r in rows:
        out = PICS / f"{r['id']}.jpg"
        if out.exists() or not r["img_src"]:
            continue
        raw = subprocess.run(["curl", "-sL", "-m", "40", "-A", UA, r["img_src"]],
                             capture_output=True, check=False).stdout
        try:
            im = Image.open(io.BytesIO(raw)).convert("RGB")
        except Exception:  # noqa: BLE001 — a dead picture leaves the card with none
            print(f"   no picture: {r['code']} {r['img_src']}")
            r["img"] = None
            continue
        im.thumbnail((480, 480))
        canvas = Image.new("RGB", (480, 480), (255, 255, 255))
        canvas.paste(im, ((480 - im.width) // 2, (480 - im.height) // 2))
        canvas.save(out, "JPEG", quality=74, optimize=True, progressive=True)
    for r in rows:
        if r["img"] and not (ASSETS / r["img"]).exists():
            r["img"] = None


def main() -> int:
    rows, left_out = parse()
    if "--no-fetch" not in sys.argv:
        fetch(rows)
    jdump({"source": "prostar-magic.com homepage, frozen copy", "snapshot": SNAP_DATE,
           "left_out": left_out, "products": rows}, DATA / "products.json")
    kb = sum((ASSETS / r["img"]).stat().st_size for r in rows if r["img"]) / 1e3
    print(f"{len(rows)} products, {sum(1 for r in rows if r['img'])} pictures ({kb:.0f} kB), "
          f"left out {left_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

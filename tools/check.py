#!/usr/bin/env python3
"""check.py — gates on docs/ before anything ships. Exit 1 on any failure.

    python3 tools/check.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shopmap  # noqa: E402
from common import GEO, ROOT, SITE, jload  # noqa: E402

STYLECHECK = Path.home() / ".claude" / "bin" / "stylecheck.py"


def main() -> int:
    errs: list[str] = []
    html = (SITE / "index.html").read_text(encoding="utf-8")
    cat = jload(ROOT / "data" / "products.json")

    errs += [f"map: {e}" for e in shopmap.gate(jload(GEO / "shop-map.json"))]

    # the page asks nothing of another host: scripts, styles, pictures, fonts are local
    for m in re.finditer(r'<(script|img|link)\b[^>]*\b(src|href)="([^"]+)"', html):
        tag, _, url = m.groups()
        if tag == "link" and "canonical" in m.group(0):
            continue
        if re.match(r"https?://", url):
            errs.append(f"outside request: <{tag}> {url}")
    for url in re.findall(r"url\(([^)]+)\)", html):
        if re.match(r"['\"]?https?://", url):
            errs.append(f"outside request in CSS: {url}")

    for needle in ('translate="no"', 'class="notranslate"', 'name="google" content="notranslate"',
                   'name="robots" content="notranslate"', "translate[.]goog"):
        if needle not in html:
            errs.append(f"notranslate: missing {needle}")
    if "X-Robots-Tag: notranslate" not in (SITE / "_headers").read_text():
        errs.append("notranslate: _headers")

    from PIL import Image
    if Image.open(SITE / "card.jpg").size != (1200, 630):
        errs.append("share card is not 1200×630")
    for k in ("og:image", "og:image:width", "og:image:height", "twitter:card", "twitter:image"):
        if f'"{k}"' not in html:
            errs.append(f"share card meta missing: {k}")

    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    try:
        d = json.loads(ld.group(1).replace("<\\/", "</"))
        if len(d["hasOfferCatalog"]["itemListElement"]) != len(cat["products"]):
            errs.append("JSON-LD offer count differs from the catalogue")
    except Exception as e:  # noqa: BLE001
        errs.append(f"JSON-LD: {e}")

    n_cards = html.count('<article class="p"')
    if n_cards != len(cat["products"]):
        errs.append(f"{n_cards} cards for {len(cat['products'])} products")
    for src in re.findall(r'src="(assets/[^"]+)"', html) + re.findall(r"url\((assets/[^)]+)\)", html):
        if not (SITE / src).exists():
            errs.append(f"missing file: {src}")

    if STYLECHECK.exists():
        r = subprocess.run([sys.executable, str(STYLECHECK), str(SITE / "index.html"),
                            str(ROOT / "README.txt")], capture_output=True, text=True)
        if r.returncode:
            errs.append("stylecheck:\n" + r.stdout.strip())

    for e in errs:
        print("✗", e)
    print(f"{'FAIL' if errs else 'ok'} · {n_cards} cards · {len(html) // 1000} kB page")
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())

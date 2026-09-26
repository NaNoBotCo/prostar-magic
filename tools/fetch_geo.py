#!/usr/bin/env python3
"""fetch_geo.py — the ground under the shop map, and the walk from Tha Phae Gate.

Streets (with names) come from the Roads of Chiang Mai harvest on this disk; the moat and
the wall from the Ghost Chiang Mai base sheet; both are OpenStreetMap, ODbL. The walk is
asked of OSRM's foot profile once and cached. Nothing here is fetched by a reader's page.

    python3 tools/fetch_geo.py
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import GEO, ROOT, UA, jdump, jload  # noqa: E402

PROJECTS = ROOT.parent
ROADS = PROJECTS / "chiang-mai-roads" / "data" / "harvest" / "osm-city.json"
BASE = PROJECTS / "ghost-chiang-mai" / "data" / "geo" / "base-city.json"

SHOP = (18.782429, 98.993240)      # Overture, via motdang.net listing (updated 2026-09-07)
GATE = (18.788463, 98.993142)      # ประตูท่าแพ, OSM
WAT = (18.781436, 98.991242)       # วัดทรายมูล (พม่า), OSM — on the shop's own map
BOX = (18.7792, 98.9868, 18.7902, 98.9990)   # south, west, north, east

DROP = {"footway", "path", "track", "steps", "corridor", "elevator", "construction",
        "proposed", "cycleway", "bridleway", "service"}
RANK = {"primary": 2, "secondary": 3, "tertiary": 4, "unclassified": 5, "residential": 5,
        "living_street": 5, "pedestrian": 5, "road": 5}


def clip_in(pts, m=0.0015):
    s, w, n, e = BOX
    return any(s - m <= p[0] <= n + m and w - m <= p[1] <= e + m for p in pts)


def metres(a, b):
    k = math.cos(math.radians((a[0] + b[0]) / 2))
    return math.hypot((a[0] - b[0]) * 110540, (a[1] - b[1]) * 111320 * k)


def osrm_foot(a, b) -> dict:
    url = (f"https://routing.openstreetmap.de/routed-foot/route/v1/foot/"
           f"{a[1]},{a[0]};{b[1]},{b[0]}?overview=full&geometries=geojson")
    out = subprocess.run(["curl", "-sS", "-m", "60", "-A", UA, url],
                         capture_output=True, text=True, check=True).stdout
    r = json.loads(out)["routes"][0]
    return {"m": round(r["distance"]), "s": round(r["duration"]),
            "pts": [[round(c[1], 6), round(c[0], 6)] for c in r["geometry"]["coordinates"]]}


def main() -> int:
    d = jload(ROADS)
    streets = []
    for w in d["ways"]:
        h = w["tags"].get("highway", "")
        base = h.replace("_link", "")
        if h in DROP or base not in RANK or not clip_in(w["pts"]):
            continue
        streets.append({"r": RANK[base], "name": w["tags"].get("name", ""),
                        "en": w["tags"].get("name:en", ""), "pts": w["pts"]})
    b = jload(BASE)
    water = [a for a in b["water"] if clip_in(a)]
    canals = [l for l in b["rivers"] if clip_in(l["pts"])]
    wall = [w for w in b["wall"] if clip_in(w)]

    cache = GEO / "walk-gate.json"
    walk = jload(cache) if cache.exists() else osrm_foot(GATE, SHOP)
    jdump(walk, cache, indent=0)

    jdump({"box": BOX, "shop": SHOP, "gate": GATE, "wat": WAT,
           "source": "OpenStreetMap contributors, ODbL — streets from the Roads of Chiang Mai "
                     "harvest (Overpass, 2026-09-21); moat and wall from the Ghost Chiang Mai "
                     "base sheet; walk by OSRM foot profile (routing.openstreetmap.de)",
           "streets": streets, "water": water, "canals": canals, "wall": wall, "walk": walk},
          GEO / "shop-map.json", indent=0)
    snap = min(metres(SHOP, p) for s in streets for p in s["pts"])
    print(f"{len(streets)} streets, {len(water)} water, {len(wall)} wall · walk {walk['m']} m "
          f"{walk['s'] // 60} min · shop pin {snap:.0f} m from nearest street vertex")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

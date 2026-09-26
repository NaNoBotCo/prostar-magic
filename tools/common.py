"""common.py — paths and small helpers shared by the tools."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GEO = DATA / "geo"
ASSETS = ROOT / "assets"
SITE = ROOT / "docs"
UA = "prostar-magic-site/0.1 (hongdam.net)"


def jload(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def jdump(obj, p: Path, indent: int | None = 1) -> None:
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")

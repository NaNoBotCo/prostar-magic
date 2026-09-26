==============================================================================
PROSTAR-MAGIC
==============================================================================


A one-page site for Prostar Magic Shop (โปรสตาร์ แมจิก ช้อป), 95/10 Kotchasarn
Road, Chiang Mai: the shop's 83 props with prices, a list that goes to the
shop on LINE, shows, lessons, opening hours with an open-now line, and a
street map with the walk from Tha Phae Gate. Thai first, English under it.

Live: https://nanobotco.github.io/prostar-magic/ (GitHub Pages, main /docs)

RUN
------------------------------------------------------------------------------


      python3 tools/harvest.py     # catalogue + pictures from the shop's frozen homepage
      python3 tools/fetch_geo.py   # map ground from the local OSM harvests; walk from OSRM (cached)
      python3 tools/build.py       # → docs/
      python3 tools/check.py       # gates
      python3 tools/serve.py 8852  # http://localhost:8852/


SOURCES
------------------------------------------------------------------------------


      Products, prices, codes, pictures, phone, LINE, YouTube, show banner
          From: prostar-magic.com homepage, a frozen copy stamped 2024-06-18
              (data/snapshot/)

      THAI NAME, HOUSE NUMBER (95/10), FACEBOOK, COORDINATES
          From: Overture Maps via the motdang.net listing, updated 2026-09-07

      SHOP-FRONT PHOTO
          From: motdang.net listing photo

      STREETS, MOAT, WALL
          From: OpenStreetMap contributors (ODbL), via chiang-mai-roads and
              ghost-chiang-mai

      WALK FROM THA PHAE GATE
          From: OSRM foot profile, routing.openstreetmap.de

      OPENING HOURS, POSTCODE
          From: the shop's Google Maps listing, read 2026-09-26

      FONTS
          From: Prompt, Sarabun (SIL OFL, assets/fonts/)


Product pictures and descriptions belong to the shop. Terms: NOTICE.txt.

LEFT OPEN
------------------------------------------------------------------------------


  -  Show prices: not on this disk. The page says to ask on LINE.
  -  57 DVD and instruction-video rows on the old store are left off (left_out
     in data/products.json).
  -  data/snapshot/ (the shop's homepage copy) is in .gitignore;
     tools/harvest.py needs that folder to run.

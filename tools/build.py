#!/usr/bin/env python3
"""build.py — data/ + assets/ → docs/ (one page, its pictures, its share card).

    python3 tools/build.py

Every figure on the page is computed here from data/products.json and data/geo/.
"""
from __future__ import annotations

import json
import shutil
import statistics
import sys
from datetime import date
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import card as C  # noqa: E402
import shopmap  # noqa: E402
from common import ASSETS, DATA, GEO, SITE, jload  # noqa: E402
from css import CSS  # noqa: E402

TH_MONTH = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
SHELVES = [("stage", "เวที", "Stage"), ("cards", "ไพ่", "Cards"), ("closeup", "ระยะใกล้", "Close-up"),
           ("coins", "เหรียญ·แบงก์", "Coins & notes"), ("mind", "ทายใจ", "Mind reading")]
BINS = [(0, 100), (101, 250), (251, 500), (501, 1000), (1001, 2500), (2501, 10 ** 9)]

NOTRANSLATE_JS = ('<script>if(/[.]translate[.]goog$/.test(location.hostname))location.replace("https://"'
                  '+location.hostname.slice(0,-15).replace(/--/g,"~").replace(/-/g,".").replace(/~/g,"-")'
                  '+location.pathname+location.search.replace(/([?&])_x_tr_[^&]*/g,"$1")'
                  '.replace(/[?&]+$/,"").replace(/[?]&+/,"?")+location.hash)</script>')


def th_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.day} {TH_MONTH[d.month - 1]} {d.year + 543}"


def en_date(iso: str) -> str:
    return date.fromisoformat(iso).strftime("%-d %b %Y")


def baht(n: int) -> str:
    return f"฿{n:,}"


def bi(th: str, en: str, tag: str = "span") -> str:
    """Thai line with its English line under it."""
    return f'{escape(th)} <{tag} class="en" lang="en">{escape(en)}</{tag}>'


DAY_TH = ["จ.", "อ.", "พ.", "พฤ.", "ศ.", "ส.", "อา."]
DAY_EN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DAY_LD = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def hour_runs(hours: list) -> list[tuple[int, int, str, str]]:
    """Consecutive days with the same hours, Monday first: (first, last, opens, closes)."""
    runs = []
    for i, h in enumerate(hours):
        if runs and runs[-1][1] == i - 1 and (runs[-1][2], runs[-1][3]) == tuple(h):
            runs[-1] = (runs[-1][0], i, *h)
        else:
            runs.append((i, i, *h))
    return runs


def hours_table(hours: list) -> str:
    rows = []
    for a, b, o, c in hour_runs(hours):
        th = DAY_TH[a] if a == b else f"{DAY_TH[a]}–{DAY_TH[b]}"
        en = DAY_EN[a] if a == b else f"{DAY_EN[a]}–{DAY_EN[b]}"
        rows.append(f'<tr><th scope="row">{th} <span class="en" lang="en">{en}</span></th>'
                    f'<td>{o}–{c}</td></tr>')
    return f'<table class="hrs"><tbody>{"".join(rows)}</tbody></table>'


def price_strip(prices: list[int]) -> str:
    counts = [sum(1 for p in prices if a <= p <= b) for a, b in BINS]
    top = max(counts)
    labels = ["≤ ฿100", "฿101–250", "฿251–500", "฿501–1,000", "฿1,001–2,500", "> ฿2,500"]
    bars = "".join(
        f'<li><span class="h-bar" style="--h:{c / top:.3f}"><b>{c}</b></span>'
        f'<span class="h-l">{escape(l)}</span></li>' for c, l in zip(counts, labels))
    return f'<ol class="hist" aria-label="Price spread">{bars}</ol>'


def product_card(i: int, p: dict, shelf_names: dict) -> str:
    off = round(100 * (p["was"] - p["price"]) / p["was"]) if p["was"] else 0
    was = f'<s aria-label="เดิม">{baht(p["was"])}</s><em class="off">−{off}%</em>' if p["was"] else ""
    teach = '<span class="tag">มีคลิปสอน</span>' if p["teach"] else ""
    img = (f'<img src="assets/{p["img"]}" width="240" height="240" loading="lazy" decoding="async" alt="">'
           if p["img"] else '<span class="noimg" aria-hidden="true">✦</span>')
    key = f'{p["name"]} {p["code"]} {p["blurb"]} {shelf_names[p["shelf"]]}'.lower()
    return (f'<article class="p" id="p-{p["id"]}" data-id="{p["id"]}" data-i="{i}" data-p="{p["price"]}" '
            f'data-off="{off}" data-shelf="{p["shelf"]}" data-teach="{int(p["teach"])}" '
            f'data-k="{escape(key)}" data-name="{escape(p["name"])}" data-code="{escape(p["code"])}">'
            f'<div class="p-img">{img}{teach}</div>'
            f'<div class="p-body"><h3>{escape(p["name"])}</h3>'
            f'<p class="p-blurb">{escape(p["blurb"])}</p>'
            f'<p class="p-code">{escape(p["code"])}</p>'
            f'<p class="p-price"><strong>{baht(p["price"])}</strong>{was}</p>'
            f'<button class="add needs-js" type="button" aria-pressed="false">+ ใส่รายการ</button></div></article>')


def jsonld(shop: dict, g: dict, products: list) -> str:
    offers = [{"@type": "Offer", "name": p["name"], "sku": p["code"], "price": p["price"],
               "priceCurrency": "THB"} for p in products]
    d = {"@context": "https://schema.org", "@type": "Store", "name": shop["name"],
         "alternateName": shop["name_th"], "url": shop["base_url"],
         "image": shop["base_url"] + "card.jpg", "telephone": shop["phone_intl"],
         "address": {"@type": "PostalAddress",
                     "streetAddress": f'{shop["house_no"]} {shop["street_en"]}',
                     "addressLocality": "Chang Khlan, Mueang Chiang Mai", "postalCode": shop["postcode"],
                     "addressRegion": "Chiang Mai", "addressCountry": "TH"},
         "geo": {"@type": "GeoCoordinates", "latitude": g["shop"][0], "longitude": g["shop"][1]},
         "openingHoursSpecification": [
             {"@type": "OpeningHoursSpecification", "dayOfWeek": DAY_LD[a:b + 1], "opens": o, "closes": c}
             for a, b, o, c in hour_runs(shop["hours"])],
         "sameAs": [shop["facebook"], shop["youtube"]],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Magic props",
                             "itemListElement": offers}}
    return json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def page(shop: dict, cat: dict, g: dict) -> str:
    products = cat["products"]
    prices = sorted(p["price"] for p in products)
    n, lo, hi = len(products), prices[0], prices[-1]
    med = int(statistics.median(prices))
    p90 = prices[int(0.9 * (n - 1))]
    walk_m = g["walk"]["m"]
    walk_min = round(g["walk"]["s"] / 60)
    n_teach = sum(p["teach"] for p in products)
    shelf_names = {k: f"{th} {en}" for k, th, en in SHELVES}
    by_code = {p["code"]: p for p in products}
    own = by_code.get(shop["own_trick"])
    line_url = f'https://line.me/ti/p/~{shop["line_id"]}'
    tel = f'tel:{shop["phone_intl"]}'
    lat, lon = g["shop"]
    osm = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}"
    gmaps = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
    snap_th, snap_en = th_date(cat["snapshot"]), en_date(cat["snapshot"])
    title = "Prostar Magic Shop · โปรสตาร์ แมจิก ช้อป · ร้านมายากล เชียงใหม่"
    desc = (f"ร้านมายากล ถนนคชสาร เชียงใหม่ — อุปกรณ์มายากล {n} ชิ้น ราคา {baht(lo)}–{baht(hi)}, "
            f"โชว์มายากล และสอนมายากล · Magic shop on the Chiang Mai moat: props, shows, lessons.")

    chips = [f'<button class="chip" type="button" data-shelf="all" aria-pressed="true">'
             f'{bi("ทั้งหมด", "All")} <b>{n}</b></button>']
    for k, th, en in SHELVES:
        c = sum(1 for p in products if p["shelf"] == k)
        chips.append(f'<button class="chip" type="button" data-shelf="{k}" aria-pressed="false">'
                     f'{bi(th, en)} <b>{c}</b></button>')
    chips.append(f'<button class="chip" type="button" data-shelf="teach" aria-pressed="false">'
                 f'{bi("มีคลิปสอน", "With lessons")} <b>{n_teach}</b></button>')
    cards = "".join(product_card(i, p, shelf_names) for i, p in enumerate(products))

    own_tile = ""
    if own:
        own_tile = (f'<figure class="tile tile-shot"><a class="shot" href="#p-{own["id"]}">'
                    f'<span class="bg" style="background-image:url(assets/{own["img"]})"></span>'
                    f'<span class="scrim"></span><span class="sp"></span>'
                    f'<span class="tx"><small>กลของโจนาธานเอง · <span lang="en">Jonathan\'s own trick</span></small>'
                    f'<strong>Burn</strong><em>{baht(own["price"])}</em></span></a></figure>')

    return f"""<!doctype html>
<html lang="th" translate="no" class="notranslate">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="google" content="notranslate">
<meta name="robots" content="notranslate">
<meta name="theme-color" content="#120d1c">
<link rel="canonical" href="{shop['base_url']}">
<meta property="og:type" content="website">
<meta property="og:title" content="Prostar Magic Shop · โปรสตาร์ แมจิก ช้อป">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{shop['base_url']}">
<meta property="og:image" content="{shop['base_url']}card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="th_TH">
<meta property="og:locale:alternate" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{shop['base_url']}card.jpg">
<link rel="icon" href="assets/icon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/prompt-600-latin.woff2" as="font" type="font/woff2" crossorigin>
{NOTRANSLATE_JS}
<script>document.documentElement.classList.add('js')</script>
<style>{CSS}</style>
<script type="application/ld+json">{jsonld(shop, g, products)}</script>
</head>
<body>
<a class="skip" href="#shop">ข้ามไปที่ร้าน</a>
<header class="top">
  <a class="mark" href="#top" aria-label="Prostar Magic, top"><span class="star" aria-hidden="true">✦</span><span class="mark-t">PROSTAR</span><span class="mark-sub">MAGIC</span></a>
  <nav aria-label="Sections"><a href="#shop">ร้าน</a><a href="#shows">โชว์</a><a href="#learn">เรียน</a><a href="#visit">แผนที่</a></nav>
  <a class="pill line" href="{line_url}" target="_blank" rel="noopener">LINE</a>
</header>

<main id="top">
<section class="band hero" aria-label="Prostar Magic Shop">
  <span class="bg" style="background-image:url(assets/photos/storefront.jpg)"></span>
  <span class="scrim"></span><span class="sp"></span>
  <div class="tx">
    <p class="kicker">{bi("ถนนคชสาร ริมคูเมือง เชียงใหม่", "Kotchasarn Road, on the moat, Chiang Mai")}</p>
    <h1 class="marquee"><svg class="bulbs" aria-hidden="true"><rect class="b0" width="100%" height="100%" rx="14"/><rect class="b1" width="100%" height="100%" rx="14"/></svg><span class="m1">PROSTAR</span><span class="m2">MAGIC SHOP</span></h1>
    <p class="thname">{escape(shop['name_th'])}</p>
    <p class="lede">{bi("อุปกรณ์มายากล โชว์ และสอนมายากล", "Magic props, shows and lessons")}</p>
    <p class="now needs-js" data-now aria-live="polite"></p>
    <p class="ctas">
      <a class="btn btn-line" href="{line_url}" target="_blank" rel="noopener"><span>แอด LINE</span><small lang="en">{shop['line_id']}</small></a>
      <a class="btn btn-gold" href="{tel}"><span>โทร</span><small>{shop['phone']}</small></a>
      <a class="btn btn-ghost" href="#visit"><span>แผนที่</span><small lang="en">Map</small></a>
    </p>
  </div>
</section>

<ul class="stats" aria-label="The shop in numbers">
  <li><b>{n}</b>{bi("ชิ้นในร้าน", "props in the shop")}</li>
  <li><b>{baht(lo)}–{hi:,}</b>{bi("ราคา", "price range")}</li>
  <li><b>≤ {baht(med)}</b>{bi("ครึ่งร้านราคาไม่เกิน", "half the shop costs this or less")}</li>
  <li><b>{walk_min} นาที</b>{bi("เดินจากประตูท่าแพ", "walk from Tha Phae Gate")}</li>
</ul>

<section id="shop" class="sec shop">
  <div class="sec-h">
    <h2>{bi("ร้าน", "Shop", "small")}</h2>
    <p>{bi("เลือกของ ใส่รายการ แล้วส่งทาง LINE — ส่งตรงถึงบ้านท่าน", "Pick, add to your list, send it on LINE.")}</p>
    <p class="note">{bi(f"ราคาจากเว็บร้าน ณ {snap_th}", f"Prices from the shop's web store, {snap_en}")}</p>
  </div>
  <div class="spread">
    {price_strip(prices)}
    <p class="spread-l">{bi(f"ครึ่งหนึ่งไม่เกิน {baht(med)} · 9 ใน 10 ไม่เกิน {baht(p90)}", f"Half cost {baht(med)} or less; nine in ten, {baht(p90)} or less")}</p>
  </div>
  <div class="tools needs-js">
    <div class="chips" role="group" aria-label="Shelves">{''.join(chips)}</div>
    <div class="row">
      <label class="float"><input id="q" type="search" placeholder=" " autocomplete="off"><span>ค้นหา · <i lang="en">Search</i></span></label>
      <label class="sort"><span class="vh">เรียง</span><select id="sort">
        <option value="i">เรียงตามร้าน · Shop order</option>
        <option value="up">ถูก → แพง · Low to high</option>
        <option value="down">แพง → ถูก · High to low</option>
        <option value="off">ลดมากสุด · Biggest discount</option>
      </select></label>
      <p class="shown"><b id="count">{n}</b> ชิ้น</p>
    </div>
  </div>
  <p class="nojs">{bi("สั่งทาง LINE: บอกรหัสสินค้า", "To order on LINE, send the item code.")}</p>
  <div id="grid" class="grid">{cards}</div>
  <p id="none" class="none" hidden>{bi("ไม่พบ — ลองคำอื่น หรือถามทาง LINE", "Nothing found. Try another word, or ask on LINE.")}</p>
</section>

<section id="shows" class="sec shows">
  <div class="sec-h">
    <h2>{bi("โชว์มายากล", "Magic shows", "small")}</h2>
    <p class="perf" lang="en">{escape(shop['performer'])}</p>
    <p>{bi("มายากลเวทีและระยะใกล้ สำหรับงานบริษัท โรงเรียน และงานเลี้ยง", "Stage and close-up magic for company events, schools and parties.")}</p>
  </div>
  <figure class="banner"><img src="assets/photos/shows.jpg" width="1000" height="300" loading="lazy" decoding="async"
    alt="Jonathan performing: card magic, stage shows with an assistant, the Thailand's Got Talent set, a company event stage">
    <figcaption>{bi("ภาพจากงานที่ผ่านมา", "From past shows")}</figcaption></figure>
  <p class="ctas"><a class="btn btn-line" href="{line_url}" target="_blank" rel="noopener"><span>ถามคิวและราคาทาง LINE</span><small lang="en">Ask for a date and price</small></a>
  <a class="btn btn-gold" href="{tel}"><span>โทร</span><small>{shop['phone']}</small></a></p>
</section>

<section id="learn" class="sec learn">
  <div class="sec-h"><h2>{bi("เรียนมายากล", "Lessons", "small")}</h2></div>
  <div class="tiles">
    <div class="tile"><h3>{escape(shop['course_note'])}</h3>
      <p>{bi("ถามรอบเรียนทาง LINE", "Ask on LINE for the next class.")}</p>
      <a class="btn btn-line sm" href="{line_url}" target="_blank" rel="noopener"><span>LINE</span><small lang="en">{shop['line_id']}</small></a></div>
    <div class="tile"><h3><b class="big">{n_teach}</b> {escape("ชิ้นมีคลิปหรือแผ่นสอนการแสดง")}</h3>
      <p class="en" lang="en">{n_teach} props come with a how-to clip or sheet.</p>
      <a class="btn btn-ghost-dark sm show-teach" href="#shop" data-shelf="teach"><span>ดู</span><small lang="en">See them</small></a></div>
    {own_tile}
  </div>
</section>

<section id="visit" class="sec visit">
  <div class="sec-h"><h2>{bi("มาที่ร้าน", "Visit", "small")}</h2></div>
  <div class="visit-grid">
    <figure class="map-wrap">{shopmap.svg(g, walk_m, walk_min)}
      <figcaption>{bi(f"เส้นทางเดินจากประตูท่าแพ {walk_m} ม.", f"Walking route from Tha Phae Gate, {walk_m} m")}</figcaption></figure>
    <div class="addr">
      <p class="a1">{escape(shop['house_no'])} {escape(shop['street_th'])} {escape(shop['tambon_th'])} {escape(shop['amphoe_th'])}</p>
      <p class="en" lang="en">{escape(shop['house_no'])} {escape(shop['street_en'])}, Chang Khlan, Chiang Mai {shop['postcode']}</p>
      <p>{bi(f"ฝั่งนอกคูเมือง ใต้ประตูท่าแพ — เดิน {walk_m} ม. ประมาณ {walk_min} นาที", f"Outside the moat, south of Tha Phae Gate: {walk_m} m on foot, about {walk_min} min.")}</p>
      <div class="hours"><p class="hours-h">{bi("เวลาเปิด", "Hours")}</p>
        <p class="now needs-js" data-now></p>
        {hours_table(shop['hours'])}
        <p class="hours-src">{bi(f"ตาม Google Maps · {th_date(shop['hours_checked'])}", f"From Google Maps, {en_date(shop['hours_checked'])}")}</p></div>
      <p class="ctas"><a class="btn btn-gold sm" href="{osm}" target="_blank" rel="noopener"><span>เส้นทาง</span><small lang="en">OpenStreetMap</small></a>
        <a class="btn btn-ghost-dark sm" href="{gmaps}" target="_blank" rel="noopener"><span>เส้นทาง</span><small lang="en">Google Maps</small></a></p>
      <figure class="front"><img src="assets/photos/storefront-sm.jpg" width="480" height="320" loading="lazy" decoding="async"
        alt="The shop front: a two-storey building with the PROSTAR MAGIC SHOP sign over the door">
        <figcaption>{bi("หน้าร้าน", "The shop front")}</figcaption></figure>
    </div>
  </div>
</section>
</main>

<div id="bar" class="bar" hidden>
  <details class="bar-list"><summary><b id="bar-n">0</b> ชิ้น · รวม <b>฿<span id="bar-t">0</span></b></summary>
    <ul id="bar-items"></ul>
    <label class="msg"><span>ข้อความที่จะส่ง · <i lang="en">Message</i></span><textarea id="bar-msg" rows="5" readonly></textarea></label>
    <button id="bar-clear" class="linkish" type="button">ล้างรายการ · <span lang="en">Clear</span></button>
  </details>
  <a id="bar-send" class="btn btn-line" href="{line_url}" target="_blank" rel="noopener"><span>ส่งรายการทาง LINE</span><small lang="en">Copy list, open LINE</small></a>
</div>

<footer class="foot">
  <p class="f-name">Prostar Magic Shop · {escape(shop['name_th'])}</p>
  <p>{escape(shop['house_no'])} {escape(shop['street_th'])} เชียงใหม่ · <a href="{tel}">{shop['phone']}</a> · <a href="{line_url}" target="_blank" rel="noopener">LINE {shop['line_id']}</a> · <a href="{shop['facebook']}" target="_blank" rel="noopener">Facebook</a> · <a href="{shop['youtube']}" target="_blank" rel="noopener">YouTube</a></p>
  <p class="credit">{bi("ภาพสินค้าและรายละเอียด: prostar-magic.com · แผนที่: © ผู้ร่วมพัฒนา OpenStreetMap (ODbL) · ภาพหน้าร้าน: motdang.net", "Product pictures and text: prostar-magic.com · Map: © OpenStreetMap contributors (ODbL) · Shop front: motdang.net")}</p>
  <p class="credit maker">เว็บไซต์ · <a href="https://hongdam.net/" target="_blank" rel="noopener">หงส์ดำ เชียงราย · <span lang="en">Hongdam, Chiang Rai</span></a> · <a href="{shop['repo']}" target="_blank" rel="noopener"><span lang="en">Source</span></a></p>
</footer>
<script>const HOURS={json.dumps(shop['hours'])};</script>
<script>{JS}</script>
</body>
</html>
"""


JS = r"""
(()=>{
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const grid=$('#grid'),cards=$$('.p'),chips=$$('.chip'),q=$('#q'),sort=$('#sort'),bar=$('#bar'),send=$('#bar-send');
const KEY='prostar-list';let shelf='all';let list={};
try{list=JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(e){list={}}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(list))}catch(e){}};
const fmt=n=>n.toLocaleString('en-US');
function apply(){const t=q.value.trim().toLowerCase();let n=0;
 cards.forEach(c=>{const s=shelf==='all'||(shelf==='teach'?c.dataset.teach==='1':c.dataset.shelf===shelf);
  const ok=s&&(!t||c.dataset.k.includes(t));c.hidden=!ok;if(ok)n++});
 $('#count').textContent=n;$('#none').hidden=n>0}
function setShelf(k){shelf=k;chips.forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.shelf===k)));apply()}
function order(){const k=sort.value,a=[...cards];
 a.sort((x,y)=>k==='up'?x.dataset.p-y.dataset.p:k==='down'?y.dataset.p-x.dataset.p:k==='off'?(y.dataset.off-x.dataset.off)||(x.dataset.p-y.dataset.p):x.dataset.i-y.dataset.i);
 a.forEach(c=>grid.appendChild(c))}
function message(items,tot){return 'สวัสดี สนใจสั่งของจากเว็บไซต์ Prostar Magic\n'+items.map(c=>'• '+c.dataset.code+' '+c.dataset.name+' ฿'+fmt(+c.dataset.p)).join('\n')+'\nรวม ฿'+fmt(tot)+' ('+items.length+' ชิ้น)'}
function render(){const items=cards.filter(c=>list[c.dataset.id]).sort((a,b)=>a.dataset.i-b.dataset.i);
 Object.keys(list).forEach(id=>{if(!document.getElementById('p-'+id))delete list[id]});
 const tot=items.reduce((s,c)=>s+(+c.dataset.p),0);
 cards.forEach(c=>{const on=!!list[c.dataset.id],b=c.querySelector('.add');b.setAttribute('aria-pressed',String(on));b.textContent=on?'✓ ในรายการ':'+ ใส่รายการ';c.classList.toggle('on',on)});
 bar.hidden=!items.length;document.body.classList.toggle('has-bar',items.length>0);
 $('#bar-n').textContent=items.length;$('#bar-t').textContent=fmt(tot);
 $('#bar-items').innerHTML='';items.forEach(c=>{const li=document.createElement('li');
  li.innerHTML='<span></span><b></b><button type="button" aria-label="เอาออก">×</button>';
  li.querySelector('span').textContent=c.dataset.name;li.querySelector('b').textContent='฿'+fmt(+c.dataset.p);
  li.querySelector('button').onclick=()=>{delete list[c.dataset.id];save();render()};$('#bar-items').appendChild(li)});
 $('#bar-msg').value=items.length?message(items,tot):''}
cards.forEach(c=>c.querySelector('.add').addEventListener('click',()=>{const id=c.dataset.id;if(list[id])delete list[id];else list[id]=1;save();render()}));
chips.forEach(ch=>ch.addEventListener('click',()=>setShelf(ch.dataset.shelf)));
$$('.show-teach').forEach(a=>a.addEventListener('click',()=>{q.value='';setShelf('teach')}));
q.addEventListener('input',apply);sort.addEventListener('change',order);
$('#bar-clear').addEventListener('click',()=>{list={};save();render()});
send.addEventListener('click',async e=>{const t=$('#bar-msg').value;if(!t)return;const lab=send.querySelector('span');
 let ok=false;try{await navigator.clipboard.writeText(t);ok=true}catch(err){const m=$('#bar-msg');m.focus();m.select();try{ok=document.execCommand('copy')}catch(e2){}}
 lab.textContent=ok?'คัดลอกแล้ว — วางในแชท LINE':'เปิดรายการ แล้วคัดลอกข้อความ';
 if(!ok){e.preventDefault();$('.bar-list').open=true}
 setTimeout(()=>{lab.textContent='ส่งรายการทาง LINE'},7000)});
function fromHash(){const h=location.hash;if(h.startsWith('#p-')){const c=document.querySelector(h);if(c&&c.hidden){q.value='';setShelf('all')}}}
window.addEventListener('hashchange',fromHash);fromHash();render();
// open now, by the clock in Chiang Mai (UTC+7, no daylight saving)
const mins=t=>{const[h,m]=t.split(':');return h*60+ +m};
function now(){const d=new Date(Date.now()+7*36e5),day=(d.getUTCDay()+6)%7,m=d.getUTCHours()*60+d.getUTCMinutes();
 const[o,c]=HOURS[day].map(mins);let th,en,open=false;
 if(m>=o&&m<c){open=true;const left=c-m;
  th='เปิดอยู่ · ปิด '+HOURS[day][1]+(left<=60?' (อีก '+left+' นาที)':'');en='Open now · closes '+HOURS[day][1]}
 else if(m<o){th='ยังไม่เปิด · เปิดวันนี้ '+HOURS[day][0];en='Closed · opens today '+HOURS[day][0]}
 else{const t=HOURS[(day+1)%7][0];th='ปิดแล้ว · เปิดพรุ่งนี้ '+t;en='Closed · opens tomorrow '+t}
 $$('[data-now]').forEach(p=>{p.dataset.open=open;p.innerHTML='<b></b><span class="en" lang="en"></span>';p.querySelector('b').textContent=th;p.querySelector('.en').textContent=en})}
now();setInterval(now,60000);
})();
"""


def icon_svg() -> str:
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" '
            'fill="#120d1c"/><path fill="#f0c454" d="M32 9l6.6 14.1 15.4 1.9-11.3 10.6 2.9 15.3L32 43.4 '
            '18.4 50.9l2.9-15.3L10 25l15.4-1.9z"/></svg>')


def main() -> int:
    shop = jload(DATA / "shop.json")
    cat = jload(DATA / "products.json")
    g = jload(GEO / "shop-map.json")
    errs = shopmap.gate(g)
    if errs:
        raise SystemExit("map gate:\n  " + "\n  ".join(errs))

    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets" / "photos").mkdir(parents=True)
    shutil.copytree(ASSETS / "products", SITE / "assets" / "products")
    shutil.copytree(ASSETS / "fonts", SITE / "assets" / "fonts")
    C.hero(SITE / "assets" / "photos" / "storefront.jpg")
    sm = C.graded_storefront()
    sm.thumbnail((480, 480))
    sm.save(SITE / "assets" / "photos" / "storefront-sm.jpg", "JPEG", quality=78, optimize=True, progressive=True)
    from PIL import Image
    Image.open(DATA / "snapshot" / "Magic_station.jpg").convert("RGB").save(
        SITE / "assets" / "photos" / "shows.jpg", "JPEG", quality=78, optimize=True, progressive=True)
    (SITE / "assets" / "icon.svg").write_text(icon_svg())

    prices = sorted(p["price"] for p in cat["products"])
    C.share_card(SITE / "card.jpg", len(prices), prices[0], prices[-1])
    (SITE / "index.html").write_text(page(shop, cat, g), encoding="utf-8")
    (SITE / "_headers").write_text("/*\n  X-Robots-Tag: notranslate\n")
    (SITE / ".nojekyll").write_text("")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {shop['base_url']}sitemap.xml\n")
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'<url><loc>{shop["base_url"]}</loc><lastmod>{date.today().isoformat()}</lastmod></url></urlset>\n')
    kb = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file()) / 1e3
    html_kb = (SITE / "index.html").stat().st_size / 1e3
    print(f"docs/: {len(prices)} products, page {html_kb:.0f} kB, site {kb:.0f} kB · "
          f"left out {cat['left_out']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

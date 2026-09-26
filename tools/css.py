"""css.py — the page's stylesheet, inlined by build.py.

Stage night for the hero and footer, paper for the shop. Motion is transform/opacity only
and sits behind prefers-reduced-motion; the fixed-background trick is off for coarse pointers.
"""

FONTS = "".join(
    f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;"
    f"src:url(assets/fonts/{file}-{w}-{sub}.woff2) format('woff2');unicode-range:{rng}}}"
    for fam, file, ws in (("Prompt", "prompt", (600,)), ("Sarabun", "sarabun", (400, 600)))
    for w in ws
    for sub, rng in (("thai", "U+02D7,U+0303,U+0331,U+0E01-0E5B,U+200C-200D,U+25CC"),
                     ("latin", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
                               "U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,"
                               "U+2212,U+2215,U+FEFF,U+FFFD")))

CSS = FONTS + r"""
:root{--stage:#120d1c;--stage2:#241733;--gold:#f0c454;--gold-ink:#8a5a00;--red:#c3142d;--red-ink:#a10f24;
--paper:#fbf6ec;--panel:#fff;--ink:#1b1424;--muted:#5d5468;--line:#e6dccb;--line-btn:#06803d;
--m-land:#f3ecdd;--m-case:#d6c9ae;--m-road:#fff;--m-major:#fff1c2;--m-water:#9fcbe6;--m-water-ink:#2f6d95;
--m-wall:#a0714f;--m-label:#3c3346;--shadow:0 10px 30px -12px rgba(27,20,36,.35);
--display:'Prompt','Sukhumvit Set','Thonburi','Noto Sans Thai',system-ui,sans-serif;
--body:'Sarabun','Sukhumvit Set','Thonburi','Noto Sans Thai',system-ui,sans-serif;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--gold-ink:#f0c454;--red-ink:#ff7a8c;--paper:#14101b;--panel:#1e1829;
--ink:#f2ede5;--muted:#b9afc4;--line:#352c42;--m-land:#1d1826;--m-case:#0f0b15;--m-road:#3b3249;--m-major:#5a4a2c;
--m-water:#1e4a66;--m-water-ink:#8cc3e6;--m-wall:#c29070;--m-label:#e6dfd5;--shadow:0 10px 30px -12px rgba(0,0,0,.7);color-scheme:dark}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;background:var(--paper);color:var(--ink);font:400 1.0625rem/1.6 var(--body);overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit}
h1,h2,h3{font-family:var(--display);font-weight:600;line-height:1.2;margin:0}
.en{display:block;font-size:.8em;opacity:.78;font-weight:400;font-family:var(--body);letter-spacing:0}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.skip{position:absolute;left:-999px;top:8px;z-index:50;background:var(--gold);color:var(--stage);padding:8px 14px;border-radius:10px}
.skip:focus{left:8px}
:focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:6px}
html:not(.js) .needs-js{display:none!important}
html.js .nojs{display:none}

/* header */
.top{position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:14px;padding:10px 16px;
 background:rgba(18,13,28,.78);-webkit-backdrop-filter:blur(14px) saturate(1.4);backdrop-filter:blur(14px) saturate(1.4);color:#fff;
 border-bottom:1px solid rgba(240,196,84,.18)}
.mark{font:600 1.05rem/1 var(--display);letter-spacing:.14em;color:var(--gold);text-decoration:none;display:flex;align-items:center;gap:6px;white-space:nowrap}
.mark-sub{color:#fff;letter-spacing:.14em;margin-left:4px}
.star{color:var(--red);font-size:1.1rem}
.top nav{display:flex;gap:4px;margin-left:auto;overflow-x:auto;scrollbar-width:none}
.top nav a{text-decoration:none;padding:6px 10px;border-radius:999px;font-size:.98rem;white-space:nowrap}
.top nav a:hover{background:rgba(255,255,255,.1)}
.pill{padding:7px 14px;border-radius:999px;text-decoration:none;font:600 .92rem/1 var(--body)}
.pill.line{background:var(--line-btn);color:#fff}
@media (max-width:560px){.mark-sub{display:none}.top{gap:4px;padding:8px 10px}.top nav a{padding:6px 6px;font-size:.92rem}.mark{font-size:.92rem;letter-spacing:.08em}}
@media (max-width:420px){.mark-t{display:none}.pill{padding:7px 11px}}

/* the band formula: background · scrim · spacer · text */
.band{position:relative;overflow:hidden;background:var(--stage);color:#fff}
.band>.bg,.band>.scrim{position:absolute;inset:0}
.band>.bg{background-size:cover;background-position:center 62%}
.band>.scrim{background:linear-gradient(90deg,rgba(18,13,28,.95) 0%,rgba(18,13,28,.82) 38%,rgba(18,13,28,.35) 75%,rgba(18,13,28,.2) 100%),
 linear-gradient(0deg,rgba(18,13,28,.96) 0%,rgba(18,13,28,0) 45%)}
.band>.sp{display:block;padding-top:max(600px,46%)}
.band>.tx{position:absolute;left:0;right:0;bottom:0;padding:0 16px 34px;max-width:1180px;margin:0 auto}
@media (min-width:900px){.band>.tx{padding:0 32px 56px}}
.kicker{margin:0 0 18px;color:#e9e1d4;font-size:1rem}
.kicker .en{display:block}
.marquee{position:relative;display:inline-flex;flex-direction:column;padding:18px 26px 16px;margin:0 0 12px;
 border-radius:18px;background:rgba(18,13,28,.55)}
.bulbs{position:absolute;left:5px;top:5px;width:calc(100% - 10px);height:calc(100% - 10px);overflow:visible;pointer-events:none}
.bulbs rect{fill:none;stroke-linecap:round;stroke-width:7}
.bulbs .b0{stroke:#6b4f1d;stroke-dasharray:0 16}
.bulbs .b1{stroke:var(--gold);stroke-dasharray:0 32;filter:drop-shadow(0 0 3px rgba(240,196,84,.9))}
.m1{font-size:clamp(3rem,11vw,6.6rem);letter-spacing:.06em;line-height:.95;color:var(--gold);
 text-shadow:1px 1px 0 #c3142d,2px 2px 0 #c3142d,3px 3px 0 #9a1024,4px 4px 0 #6d0b19,5px 5px 0 #420712,0 0 32px rgba(240,196,84,.35)}
.m2{font-size:clamp(1.3rem,4.4vw,2.5rem);letter-spacing:.32em;color:#fff;margin-top:6px}
.thname{font:600 clamp(1.25rem,3.6vw,1.8rem)/1.3 var(--display);margin:0 0 6px}
.lede{margin:0 0 20px;font-size:1.15rem;color:#f1ebe1}
.lede .en{display:block}
.ctas{display:flex;flex-wrap:wrap;gap:10px;margin:0}
.btn{display:inline-flex;flex-direction:column;justify-content:center;min-height:52px;padding:9px 18px;border-radius:14px;
 text-decoration:none;font:600 1.06rem/1.15 var(--body);border:0;cursor:pointer;transition:transform .35s cubic-bezier(.34,1.56,.64,1),box-shadow .3s}
.btn small{font-weight:400;font-size:.8rem;opacity:.9}
.btn.sm{min-height:44px;padding:7px 14px;font-size:.98rem}
.btn-line{background:var(--line-btn);color:#fff}
.btn-gold{background:var(--gold);color:var(--stage)}
.btn-ghost{box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.75);color:#fff}
.btn-ghost-dark{box-shadow:inset 0 0 0 1.5px var(--ink);color:var(--ink)}

/* numbers */
.stats{list-style:none;margin:0;padding:22px 16px 28px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;
 background:linear-gradient(180deg,var(--stage) 0%,var(--stage2) 100%);color:#e9e1d4}
.stats li{max-width:280px;justify-self:center;text-align:center;font-size:.95rem;line-height:1.35}
.stats b{display:block;font:600 clamp(1.4rem,4vw,2.1rem)/1.1 var(--display);color:var(--gold);font-variant-numeric:tabular-nums;margin-bottom:4px}
@media (max-width:700px){.stats{grid-template-columns:repeat(2,1fr)}}

/* sections */
.sec{max-width:1180px;margin:0 auto;padding:56px 16px}
@media (min-width:900px){.sec{padding:72px 32px}}
.sec-h{margin-bottom:22px;max-width:760px}
.sec-h h2{font-size:clamp(1.9rem,5vw,2.6rem)}
.sec-h h2 .en{font-size:.45em;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-ink);opacity:1;margin-top:4px}
.sec-h p{margin:.5em 0 0}
.sec-h .en{display:block}
.note{color:var(--muted);font-size:.92rem}

/* price spread */
.spread{display:grid;grid-template-columns:minmax(0,420px) 1fr;gap:12px 22px;align-items:end;margin:0 0 24px}
@media (max-width:760px){.spread{grid-template-columns:1fr}}
.hist{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,1fr);gap:6px;align-items:end}
.hist li{display:flex;flex-direction:column;align-items:stretch;gap:4px}
.h-bar{display:flex;align-items:flex-start;justify-content:center;height:calc(10px + var(--h) * 70px);background:var(--gold);border-radius:6px 6px 2px 2px;
 color:var(--stage);font:600 .78rem/1.6 var(--body)}
.h-l{font-size:.68rem;color:var(--muted);text-align:center;line-height:1.2;font-variant-numeric:tabular-nums}
.spread-l{margin:0;font-size:.95rem}

/* tools */
.tools{z-index:10;background:color-mix(in srgb,var(--paper) 92%,transparent);
 -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);padding:10px 0;margin:0 -4px 14px}
.chips{display:flex;gap:8px;overflow-x:auto;padding:2px 4px 8px;scrollbar-width:thin}
.chip{flex:none;display:inline-flex;align-items:center;gap:6px;border:1.5px solid var(--line);background:var(--panel);color:var(--ink);
 border-radius:999px;padding:7px 14px;font:600 .95rem/1.2 var(--body);cursor:pointer;transition:transform .3s cubic-bezier(.34,1.56,.64,1),background .2s}
.chip .en{display:inline;font-size:.8rem}
.chip b{font-size:.78rem;background:var(--paper);border-radius:999px;padding:1px 7px;font-variant-numeric:tabular-nums}
.chip[aria-pressed=true]{background:var(--stage);border-color:var(--stage);color:var(--gold)}
.chip[aria-pressed=true] b{background:var(--gold);color:var(--stage)}
@media (prefers-color-scheme:dark){.chip[aria-pressed=true]{background:var(--gold);color:var(--stage);border-color:var(--gold)}
 .chip[aria-pressed=true] b{background:var(--stage);color:var(--gold)}}
.row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:0 4px}
.float{position:relative;flex:1 1 220px}
.float input{width:100%;font:400 1rem var(--body);padding:20px 14px 6px;border-radius:12px;border:1.5px solid var(--line);background:var(--panel);color:var(--ink)}
.float span{position:absolute;left:15px;top:14px;color:var(--muted);pointer-events:none;transition:transform .2s,font-size .2s;transform-origin:left top}
.float input:focus+span,.float input:not(:placeholder-shown)+span{transform:translateY(-9px);font-size:.75rem}
.sort select{font:400 .95rem var(--body);padding:13px 12px;border-radius:12px;border:1.5px solid var(--line);background:var(--panel);color:var(--ink);max-width:100%}
.shown{margin:0;color:var(--muted);font-size:.95rem;font-variant-numeric:tabular-nums}
.nojs{color:var(--muted)}

/* products */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(172px,1fr));gap:14px}
@media (max-width:420px){.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}
.p{display:flex;flex-direction:column;background:var(--panel);border:1.5px solid var(--line);border-radius:16px;overflow:hidden;
 transition:transform .35s cubic-bezier(.34,1.56,.64,1),box-shadow .3s,border-color .2s}
.p[hidden]{display:none}
.p.on{border-color:var(--gold)}
.p:target{box-shadow:0 0 0 4px var(--gold),var(--shadow)}
.p-img{position:relative;aspect-ratio:1;background:#fff;display:grid;place-items:center}
.p-img img{width:100%;height:100%;object-fit:contain}
.noimg{font-size:3rem;color:var(--gold)}
.tag{position:absolute;left:8px;top:8px;background:var(--stage);color:var(--gold);font:600 .72rem/1 var(--body);padding:5px 8px;border-radius:999px}
.p-body{display:flex;flex-direction:column;gap:4px;padding:10px 12px 12px;flex:1}
.p h3{font:600 .98rem/1.3 var(--body);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.6em}
.p-blurb{margin:0;font-size:.8rem;line-height:1.4;color:var(--muted);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.p-code{margin:0;font-size:.72rem;color:var(--muted);letter-spacing:.04em}
.p-price{margin:auto 0 6px;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px;font-variant-numeric:tabular-nums}
.p-price strong{font:600 1.35rem/1.1 var(--display)}
.p-price s{color:var(--muted);font-size:.85rem}
.off{font-style:normal;font:600 .72rem/1 var(--body);background:var(--red);color:#fff;padding:3px 6px;border-radius:6px}
.add{font:600 .92rem/1 var(--body);padding:11px 10px;border-radius:10px;border:1.5px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer;
 transition:transform .3s cubic-bezier(.34,1.56,.64,1),background .2s}
.add[aria-pressed=true]{background:var(--gold);border-color:var(--gold);color:var(--stage)}
.none{color:var(--muted)}

/* shows */
.shows .perf{font:600 1.3rem/1.2 var(--display);color:var(--gold-ink);margin-top:8px;letter-spacing:.04em}
.banner{margin:0 0 20px}
.banner img{width:100%;height:auto;border-radius:18px;box-shadow:var(--shadow)}
.banner figcaption,.map-wrap figcaption,.front figcaption{font-size:.85rem;color:var(--muted);margin-top:8px}
.banner figcaption .en,.map-wrap figcaption .en,.front figcaption .en{display:inline;margin-left:.4em}

/* lessons */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}
.tile{margin:0;background:linear-gradient(135deg,var(--panel) 0%,color-mix(in srgb,var(--gold) 14%,var(--panel)) 100%);
 border:1.5px solid var(--line);border-radius:18px;padding:22px;display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.tile h3{font-size:1.25rem}
.tile p{margin:0}
.big{font:600 2.6rem/1 var(--display);color:var(--gold-ink);display:block}
.tile-shot{padding:0;overflow:hidden;background:var(--stage)}
.shot{position:relative;display:block;width:100%;height:100%;color:#fff;text-decoration:none}
.shot>.bg,.shot>.scrim{position:absolute;inset:0}
.shot>.bg{background-size:cover;background-position:center;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.shot>.scrim{background:linear-gradient(0deg,rgba(18,13,28,.95) 0%,rgba(18,13,28,.55) 45%,rgba(18,13,28,0) 75%)}
.shot>.sp{display:block;padding-top:78%}
.shot>.tx{position:absolute;left:0;right:0;bottom:0;padding:18px 20px;display:flex;flex-direction:column;gap:2px}
.shot small{font-size:.88rem;opacity:.9}
.shot strong{font:600 2rem/1.1 var(--display);color:var(--gold)}
.shot em{font:600 1.1rem/1.2 var(--display);font-style:normal}

/* visit */
.visit-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:28px;align-items:start}
@media (max-width:860px){.visit-grid{grid-template-columns:1fr}}
@media (max-width:520px){.map-wrap{margin:0 -16px}.map{border-radius:0;border-left:0;border-right:0}.map-wrap figcaption{padding:0 16px}}
.map-wrap{margin:0}
.map{display:block;width:100%;height:auto;border-radius:18px;border:1.5px solid var(--line);background:var(--m-land);box-shadow:var(--shadow)}
.m-land{fill:var(--m-land)}.m-water{fill:var(--m-water)}.m-canal{fill:none;stroke:var(--m-water);stroke-width:4}
.m-case,.m-fill{fill:none;stroke-linecap:round;stroke-linejoin:round}.m-case{stroke:var(--m-case)}.m-fill{stroke:var(--m-road)}.m-major{stroke:var(--m-major)}
.m-wall{fill:none;stroke:var(--m-wall);stroke-width:5;stroke-linecap:round}
.m-walk-halo{fill:none;stroke:var(--m-land);stroke-width:10;stroke-linecap:round;stroke-linejoin:round;opacity:.9}
.m-walk{fill:none;stroke:var(--red);stroke-width:5.5;stroke-dasharray:.1 11;stroke-linecap:round;stroke-linejoin:round}
.m-st{font:600 19px var(--body);fill:var(--m-label);paint-order:stroke;stroke:var(--m-land);stroke-width:4px;stroke-linejoin:round}
.m-water-l{font:italic 600 17px var(--body);fill:var(--m-water-ink);letter-spacing:.08em}
.m-place rect,.m-place circle{fill:var(--ink)}
.m-place text{font:600 23px var(--body);fill:var(--ink);paint-order:stroke;stroke:var(--m-land);stroke-width:4px}
.m-place .en{font-size:18px;font-weight:400}
.m-shop circle{fill:var(--red);stroke:#fff;stroke-width:3}
.m-shop .m-pulse{fill:var(--red);stroke:none;opacity:.22;transform-box:fill-box;transform-origin:center}
.m-star{fill:var(--gold)}
.m-shop rect{fill:var(--stage);stroke:var(--gold);stroke-width:2}
.m-shop text{font:600 25px var(--display);fill:var(--gold);letter-spacing:.08em}
.m-walk-l rect{fill:var(--panel);stroke:var(--red);stroke-width:2}
.m-walk-l text{font:600 20px var(--body);fill:var(--red-ink)}
.m-scale rect{fill:var(--ink)}.m-scale .m-scale-a{fill:var(--m-land);stroke:var(--ink);stroke-width:1}
.m-scale text{font:600 17px var(--body);fill:var(--ink)}
.m-north circle{fill:var(--panel);stroke:var(--line);stroke-width:1.5}.m-north path{fill:var(--red)}
.m-north text{font:600 12px var(--body);fill:var(--ink)}
.m-credit{font:400 14px var(--body);fill:var(--muted)}
.addr p{margin:0 0 12px}
.addr .a1{font:600 1.2rem/1.4 var(--display)}
.addr .en{display:block}
.hours{padding:14px 16px;border-radius:14px;background:var(--panel);border:1.5px solid var(--line);margin:0 0 14px}
.hours p{margin:0 0 8px}
.hours-h{font:600 1.1rem/1.3 var(--display)}
.hours-h .en{display:inline;margin-left:.4em}
.hrs{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
.hrs th,.hrs td{text-align:left;padding:6px 0;border-top:1px solid var(--line);font-weight:400}
.hrs th .en{display:inline;margin-left:.35em}
.hrs td{text-align:right;font:600 1.05rem var(--body)}
.hours-src{font-size:.8rem;color:var(--muted);margin:8px 0 0!important}
.hours-src .en{display:inline;margin-left:.4em}
.now{display:inline-flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin:0 0 14px;padding:6px 14px 6px 30px;border-radius:999px;position:relative;
 background:rgba(195,20,45,.14);font-size:.98rem}
.now:empty{display:none}
.now::before{content:"";position:absolute;left:12px;top:50%;width:9px;height:9px;margin-top:-4.5px;border-radius:50%;background:var(--red)}
.now[data-open=true]{background:rgba(6,128,61,.16)}
.now[data-open=true]::before{background:#1fb45a;box-shadow:0 0 0 4px rgba(31,180,90,.25)}
.now .en{display:inline;font-size:.82em}
.hero .now{color:#fff;background:rgba(255,255,255,.1)}
.hero .now[data-open=true]{background:rgba(31,180,90,.2)}
.front{margin:18px 0 0}
.front img{border-radius:14px;width:100%;height:auto}

/* order bar */
.bar{position:fixed;left:12px;right:12px;bottom:12px;z-index:40;max-width:760px;margin:0 auto;display:flex;align-items:flex-end;gap:12px;
 padding:12px 12px 12px 18px;border-radius:20px;color:#fff;background:rgba(18,13,28,.88);
 -webkit-backdrop-filter:blur(16px) saturate(1.4);backdrop-filter:blur(16px) saturate(1.4);box-shadow:0 18px 50px -12px rgba(0,0,0,.55);
 border:1px solid rgba(240,196,84,.3)}
.bar[hidden]{display:none}
body.has-bar{padding-bottom:110px}
.bar-list{flex:1;min-width:0}
.bar-list summary{cursor:pointer;padding:12px 0;font-size:1.02rem;list-style:none}
.bar-list summary::-webkit-details-marker{display:none}
.bar-list summary::before{content:"▸ ";color:var(--gold)}
.bar-list[open] summary::before{content:"▾ "}
.bar-list summary b{color:var(--gold);font-variant-numeric:tabular-nums}
#bar-items{list-style:none;margin:0 0 10px;padding:0;max-height:34vh;overflow:auto}
#bar-items li{display:flex;gap:10px;align-items:center;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.12);font-size:.92rem}
#bar-items li span{flex:1;min-width:0}
#bar-items li b{font-variant-numeric:tabular-nums;color:var(--gold)}
#bar-items button{border:0;background:rgba(255,255,255,.12);color:#fff;width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:1.1rem}
.msg{display:block;font-size:.8rem;opacity:.9}
.msg textarea{width:100%;margin-top:4px;border-radius:10px;border:0;padding:8px;font:400 .85rem/1.4 var(--body);background:rgba(255,255,255,.1);color:#fff}
.linkish{background:none;border:0;color:#f3b0ba;text-decoration:underline;cursor:pointer;font:400 .88rem var(--body);padding:8px 0}
#bar-send{flex:none}
@media (max-width:520px){.bar{flex-direction:column;align-items:stretch}#bar-send{align-items:center}}

/* footer */
.foot{background:var(--stage);color:#d9d0c3;padding:40px 16px 56px;text-align:center;font-size:.95rem}
.foot p{margin:.4em auto;max-width:900px}
.foot a{color:var(--gold)}
.f-name{font:600 1.2rem var(--display);color:#fff}
.credit{font-size:.8rem;opacity:.8}
.credit .en{display:block}

/* motion — only when wanted, only on fine pointers */
@media (min-width:760px){.tools{position:sticky;top:57px}}
@media (prefers-reduced-motion:no-preference){
 .bulbs .b1{animation:chase .9s steps(2) infinite}
 @keyframes chase{to{stroke-dashoffset:-32}}
 .m-pulse{animation:pulse 2.2s ease-out infinite}
 @keyframes pulse{0%{transform:scale(.6);opacity:.35}100%{transform:scale(1.8);opacity:0}}
 @media (hover:hover) and (pointer:fine){
  .band>.bg,.stats,.tile{background-attachment:fixed}
  .btn:hover,.chip:hover{transform:scale(1.05)}
  .btn:active,.chip:active,.add:active{transform:scale(.96)}
  .p:hover{transform:translateY(-4px);box-shadow:var(--shadow)}
  .shot:hover>.bg{transform:scale(1.06)}
 }
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

"""magic.py — the moving parts: the rabbit, the hat you pull tricks from, the card trick, the
flipping product cards, the curtain, the sparkle trail. HTML pieces, CSS and JS for build.py.

Every motion sits behind prefers-reduced-motion; with it set, the page shows the end states.
"""
from __future__ import annotations

from html import escape


def rabbit_g() -> str:
    """A white rabbit, head and ears, in a 120×150 box; head centre at (60, 112)."""
    return ('<ellipse cx="42" cy="48" rx="13" ry="44" transform="rotate(-14 42 48)" fill="#fbf8f2" stroke="#d6ccbd" stroke-width="2"/>'
            '<ellipse cx="42" cy="54" rx="6" ry="31" transform="rotate(-14 42 54)" fill="#f2b3c0"/>'
            '<ellipse cx="80" cy="44" rx="13" ry="46" transform="rotate(12 80 44)" fill="#fbf8f2" stroke="#d6ccbd" stroke-width="2"/>'
            '<ellipse cx="80" cy="50" rx="6" ry="33" transform="rotate(12 80 50)" fill="#f2b3c0"/>'
            '<ellipse cx="60" cy="112" rx="42" ry="36" fill="#fbf8f2" stroke="#d6ccbd" stroke-width="2"/>'
            '<circle cx="45" cy="106" r="5.5" fill="#1b1424"/><circle cx="47" cy="104" r="1.8" fill="#fff"/>'
            '<circle cx="75" cy="106" r="5.5" fill="#1b1424"/><circle cx="77" cy="104" r="1.8" fill="#fff"/>'
            '<circle cx="36" cy="121" r="7" fill="#f2b3c0" opacity=".55"/><circle cx="84" cy="121" r="7" fill="#f2b3c0" opacity=".55"/>'
            '<path d="M55,116 Q60,112 65,116 Q60,123 55,116Z" fill="#e0879a"/>'
            '<path d="M60,121 V126 M60,126 Q55,131 51,128 M60,126 Q65,131 69,128" stroke="#8a7a88" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
            '<path d="M30,118 H13 M31,125 L14,130 M90,118 H107 M89,125 L106,130" stroke="#b9aeb6" stroke-width="1.4" stroke-linecap="round"/>')


def sprite() -> str:
    return ('<svg class="sprite" aria-hidden="true" width="0" height="0" style="position:absolute">'
            f'<defs><symbol id="rabbit" viewBox="0 0 120 150">{rabbit_g()}</symbol></defs></svg>')


def peek(cls: str) -> str:
    """The rabbit cut off below the eyes, as if behind an edge."""
    return (f'<svg class="{cls}" viewBox="0 0 120 108" aria-hidden="true">'
            '<use href="#rabbit" width="120" height="150"/></svg>')


def hat_widget(bi) -> str:
    return f'''<div class="hatpull needs-js">
  <button id="hat" class="hat-btn" type="button" aria-label="หยิบกลจากหมวก · Pull a trick from the hat">
    <svg viewBox="0 0 160 150" aria-hidden="true">
      <defs><clipPath id="hatclip"><rect x="0" y="0" width="160" height="58"/></clipPath>
      <linearGradient id="hatg" x1="0" x2="1"><stop offset="0" stop-color="#0b0a10"/><stop offset=".45" stop-color="#34313f"/><stop offset=".6" stop-color="#17161d"/><stop offset="1" stop-color="#050408"/></linearGradient></defs>
      <g clip-path="url(#hatclip)"><g class="ears"><use href="#rabbit" x="38" y="-6" width="84" height="105"/></g></g>
      <path d="M32,58 L40,140 Q80,148 120,140 L128,58Z" fill="url(#hatg)"/>
      <path d="M33,70 L35,88 Q80,95 125,88 L127,70 Q80,77 33,70Z" fill="#b3122b"/>
      <ellipse cx="80" cy="58" rx="66" ry="14" fill="#1a1820" stroke="#3a3744" stroke-width="2"/>
      <path d="M38,58 A42,8 0 0 0 122,58" fill="none" stroke="#000" stroke-width="3"/>
    </svg>
  </button>
  <div class="hat-t"><p class="hat-l">{bi("หยิบกลจากหมวก", "Pull a trick from the hat")}</p><p class="hat-s">แตะหมวก · <span lang="en">Tap the hat</span></p></div>
  <div id="pulled" class="pulled" hidden aria-live="polite">
    <span class="pulled-img"><img alt="" width="120" height="120"></span>
    <div class="pulled-t"><b class="pn"></b><span class="pp"></span>
      <span class="pulled-b"><button id="pulled-see" class="btn btn-ghost-dark sm" type="button"><span>ดูในร้าน</span><small lang="en">See it</small></button>
      <button id="pulled-add" class="btn btn-gold sm" type="button"><span>+ ใส่รายการ</span><small lang="en">Add to list</small></button></span></div>
  </div>
</div>'''


def trick_section(bi, line_url: str) -> str:
    return f'''<section id="trick" class="sec trick needs-js">
  <div class="sec-h"><h2>{bi("ลองกลนี้", "Try a trick", "small")}</h2>
    <p id="trick-say" class="trick-say" aria-live="polite"></p></div>
  <div class="felt">{peek("peek peek-felt")}<div id="trick-cards" class="pcs" aria-live="polite"></div></div>
  <p class="ctas"><button id="trick-go" class="btn btn-gold" type="button"><span>จำได้แล้ว</span><small lang="en">Got it</small></button></p>
  <div id="trick-end" class="trick-end" hidden>
    <p>{bi("อยากเล่นกลแบบนี้เป็น? ทักโจนาธานทาง LINE", "Want to do tricks like this? Ask Jonathan on LINE.")}</p>
    <a class="btn btn-line" href="{line_url}" target="_blank" rel="noopener"><span>LINE</span><small lang="en">jonathan2512</small></a>
  </div>
</section>'''


def flip(img_html: str, blurb: str, name: str) -> str:
    back = escape(blurb) + "…" if blurb else "ถามรายละเอียดทาง LINE · <span lang=\"en\">Ask on LINE</span>"
    return (f'<button class="p-flip" type="button" aria-pressed="false" '
            f'aria-label="พลิกดูว่ากลนี้ทำอะไร · Flip: what {escape(name)} does">'
            f'<span class="p-img">{img_html}<span class="flip-hint" aria-hidden="true">↻</span></span>'
            f'<span class="p-back"><span class="p-back-h">กลนี้ · <span lang="en">The trick</span></span>'
            f'<span class="p-back-t">{back}</span></span></button>')


HEAD_JS = ("<script>try{if(!sessionStorage.getItem('prostar-intro')&&matchMedia('(prefers-reduced-motion: no-preference)').matches)"
           "{document.documentElement.classList.add('intro');sessionStorage.setItem('prostar-intro','1')}}catch(e){}</script>")

CURTAINS = '<div class="curtains" aria-hidden="true"><i class="cl"></i><i class="cr"></i></div>'

CSS = r"""
/* rabbit */
.peek{position:absolute;width:74px;height:auto;pointer-events:none}
.foot{position:relative}
.foot{border-top:3px solid #d4a441}
.peek-foot{top:-69px;left:12%}
.none .peek-none{position:static;display:block;width:56px;margin:0 0 6px}

/* curtain, once a session */
.curtains{display:none}
html.intro .curtains{display:block;position:absolute;inset:0;z-index:6;pointer-events:none}
.curtains i{position:absolute;top:0;bottom:0;width:51%;
 background:linear-gradient(180deg,rgba(0,0,0,.35),transparent 30%,rgba(0,0,0,.45)),repeating-linear-gradient(90deg,#3b040d 0,#8e1024 20px,#c41f39 34px,#7c0c1d 50px,#3b040d 68px);
 box-shadow:inset 0 -6px 0 #d4a441}
.curtains .cl{left:0;animation:openL 1.6s cubic-bezier(.7,0,.2,1) .35s forwards}
.curtains .cr{right:0;animation:openR 1.6s cubic-bezier(.7,0,.2,1) .35s forwards}
@keyframes openL{to{transform:translateX(-102%)}}
@keyframes openR{to{transform:translateX(102%)}}
.stage .rise,.stage .bun{transform-box:fill-box;transform-origin:center}
html.intro .stage .rise{animation:rise 1.3s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d)}
@keyframes rise{from{opacity:0;translate:var(--dx) var(--dy);scale:.25}}
html.intro .stage .bun{animation:bun .9s cubic-bezier(.34,1.56,.64,1) 1.9s both}
@keyframes bun{from{translate:0 120px}}

/* the hat */
.hatpull{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;align-items:center;margin:0 0 22px;padding:14px 18px;border-radius:18px;
 background:linear-gradient(135deg,#1c0b25,#3d1344);color:#f3ede3;box-shadow:var(--shadow)}
.hat-btn{all:unset;cursor:pointer;width:112px;height:105px;border-radius:14px}
.hat-btn:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.hat-btn svg{width:100%;height:100%;overflow:visible}
.hat-l{margin:0;font:600 1.2rem/1.3 var(--display)}
.hat-l .en{display:block;color:var(--gold);font-size:.72em}
.hat-s{margin:4px 0 0;font-size:.85rem;opacity:.8}
.pulled{grid-column:1/-1;display:flex;gap:14px;align-items:center;margin-top:10px;padding:12px;border-radius:14px;background:#fdf8ee;color:#1b1424}
.pulled[hidden]{display:none}
.pulled-img{flex:none;width:96px;height:96px;border-radius:10px;overflow:hidden;background:#fff;box-shadow:inset 0 0 0 1px #e7d9b8}
.pulled-img img{width:100%;height:100%;object-fit:contain}
.pulled-t{display:flex;flex-direction:column;gap:4px;min-width:0}
.pn{font:600 1rem/1.3 var(--body)}
.pp{font:600 1.3rem/1.1 var(--display)}
.pulled-b{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.pulled .btn-ghost-dark{box-shadow:inset 0 0 0 1.5px #1b1424;color:#1b1424}
@media (min-width:760px){.hatpull{grid-template-columns:auto auto 1fr}.pulled{grid-column:auto;margin:0}}

/* the card trick, on felt */
.trick{position:relative;isolation:isolate;color:#f3ede3}
.trick::before{content:"";position:absolute;top:0;bottom:0;left:calc(50% - 50vw);right:calc(50% - 50vw);z-index:-1;
 background:radial-gradient(ellipse at 50% 40%,#1f7a4f 0%,#0f4a30 55%,#07281a 100%)}
.trick .sec-h h2 .en{color:var(--gold)}
.trick{text-align:center}
.trick .sec-h{margin-left:auto;margin-right:auto}
.trick .ctas{justify-content:center}
.trick-say{font:600 1.15rem/1.5 var(--body);min-height:3.2em}
.trick-say .en{display:block;font-size:.8em;font-weight:400}
.felt{position:relative;max-width:780px;margin:0 auto;padding:40px 0 22px}
.peek-felt{top:-28px;right:4%;width:72px}
.pcs{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;perspective:900px}
.pc{position:relative;width:clamp(72px,14vw,108px);aspect-ratio:5/7;border-radius:10px;transform-style:preserve-3d;
 transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.pc>span{position:absolute;inset:0;border-radius:10px;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.pc .f{background:#fdf8ee;box-shadow:0 10px 20px -10px rgba(0,0,0,.6),inset 0 0 0 1.5px #d9c79c;color:#1b1424}
.pc.red .f{color:#c3142d}
.pc .r{position:absolute;left:8px;top:6px;font:700 clamp(1rem,2.6vw,1.35rem)/1 Georgia,serif}
.pc .s{position:absolute;inset:0;display:grid;place-items:center;font-size:clamp(2rem,6vw,3rem)}
.pc .r2{position:absolute;right:8px;bottom:6px;font:700 clamp(1rem,2.6vw,1.35rem)/1 Georgia,serif;transform:rotate(180deg)}
.pc .b{transform:rotateY(180deg);box-shadow:0 10px 20px -10px rgba(0,0,0,.6);
 background:radial-gradient(circle at 50% 50%,#f0c454 0 7%,transparent 8%),
 repeating-linear-gradient(45deg,#8e1024 0 6px,#a8182f 6px 12px);border:4px solid #fdf8ee}
.pc.down{transform:rotateY(180deg)}
.trick-end p{margin:0 0 10px}
.trick-end .en{display:block}

/* products turn over */
.p-flip{all:unset;position:relative;display:block;margin:26px 10px 0;aspect-ratio:1;cursor:pointer;perspective:900px;border-radius:10px}
.p-flip:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.p-flip .p-img{position:absolute;inset:0;margin:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.p-back{position:absolute;inset:0;display:flex;flex-direction:column;gap:6px;padding:12px;border-radius:10px;overflow:auto;
 background:linear-gradient(160deg,#3d1344,#1c0b25);color:#f3ede3;box-shadow:inset 0 0 0 1.5px var(--gold);
 transform:rotateY(180deg);backface-visibility:hidden;-webkit-backface-visibility:hidden;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.p-back-h{font:600 .8rem/1.2 var(--display);color:var(--gold);letter-spacing:.04em}
.p-back-t{font-size:.84rem;line-height:1.45}
.p.flipped .p-img{transform:rotateY(-180deg)}
.p.flipped .p-back{transform:rotateY(0)}
.flip-hint{position:absolute;right:7px;bottom:6px;width:24px;height:24px;border-radius:50%;display:grid;place-items:center;
 background:rgba(18,13,28,.72);color:var(--gold);font-size:.9rem}
html.js .p-blurb{display:none}

/* sparkle trail — faint, short */
.trail{position:fixed;inset:0;pointer-events:none;z-index:60;overflow:hidden}
.trail i{position:absolute;width:9px;height:9px;margin:-4.5px 0 0 -4.5px;background:#f0c454;opacity:0;
 clip-path:polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%);animation:trail .75s ease-out forwards}
@keyframes trail{0%{opacity:.5;transform:scale(var(--s))}100%{opacity:0;transform:translate(var(--dx),-12px) scale(calc(var(--s) * .3))}}

@media (prefers-reduced-motion:no-preference){
 .hat-btn.shake svg{animation:shake .5s cubic-bezier(.36,.07,.19,.97)}
 @keyframes shake{20%{transform:rotate(-7deg)}45%{transform:rotate(6deg)}70%{transform:rotate(-3deg)}}
 .hat-btn.shake .ears{animation:ears .7s cubic-bezier(.34,1.56,.64,1)}
 @keyframes ears{40%{transform:translateY(-14px)}}
 .pulled.pop{animation:pop .5s cubic-bezier(.34,1.56,.64,1)}
 @keyframes pop{from{opacity:0;transform:translateY(-14px) scale(.9)}}
}
@media (prefers-reduced-motion:reduce){.pc,.p-flip .p-img,.p-back{transition:none}}
"""

JS = r"""
// products turn over
cards.forEach(c=>{const f=c.querySelector('.p-flip');if(f)f.addEventListener('click',()=>{const on=c.classList.toggle('flipped');f.setAttribute('aria-pressed',String(on))})});

// pull a trick from the hat
(()=>{const hat=$('#hat'),box=$('#pulled');if(!hat)return;let pick=null;
 hat.addEventListener('click',()=>{const pool=cards.filter(c=>c!==pick);pick=pool[Math.floor(Math.random()*pool.length)];
  hat.classList.remove('shake');void hat.offsetWidth;hat.classList.add('shake');
  const im=pick.querySelector('.p-img img');box.querySelector('img').src=im?im.getAttribute('src'):'';
  box.querySelector('.pn').textContent=pick.dataset.name;box.querySelector('.pp').textContent='฿'+(+pick.dataset.p).toLocaleString('en-US');
  box.hidden=false;box.classList.remove('pop');void box.offsetWidth;box.classList.add('pop')});
 $('#pulled-see').addEventListener('click',()=>{if(!pick)return;location.hash='p-'+pick.dataset.id;const c=pick;setTimeout(()=>c.scrollIntoView({block:'center'}),30)});
 $('#pulled-add').addEventListener('click',()=>{if(!pick)return;const b=pick.querySelector('.add');if(b.getAttribute('aria-pressed')!=='true')b.click();
  const l=$('#pulled-add span');l.textContent='✓ ในรายการ';setTimeout(()=>{l.textContent='+ ใส่รายการ'},2500)});
})();

// the card trick: six court cards shown; five come back, none of them the six
(()=>{const say=$('#trick-say'),table=$('#trick-cards'),go=$('#trick-go'),end=$('#trick-end');if(!go)return;
 const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const court=[];['J','Q','K'].forEach(r=>['♠','♥','♦','♣'].forEach(s=>court.push([r,s])));
 let step=0,shown=[],left=[];
 const lines={1:['นึกถึงไพ่ 1 ใบในนี้ แล้วจำไว้ — ไม่ต้องกด','Pick one card in your head and remember it. Don\'t tap it.'],
  2:['ตั้งใจนึกถึงไพ่ใบนั้นไว้…','Concentrate on your card…'],
  3:['ไพ่ของคุณหายไปแล้ว','Your card has vanished.']};
 const tell=n=>{say.innerHTML='';const b=document.createElement('span');b.textContent=lines[n][0];const e=document.createElement('span');
  e.className='en';e.lang='en';e.textContent=lines[n][1];say.append(b,e)};
 const deal=(set,down)=>{table.innerHTML='';set.forEach(([r,s])=>{const d=document.createElement('div');
  d.className='pc'+(s==='♥'||s==='♦'?' red':'')+(down?' down':'');d.setAttribute('aria-label',r+s);
  d.innerHTML='<span class="f"><span class="r"></span><span class="s"></span><span class="r2"></span></span><span class="b"></span>';
  d.querySelector('.r').textContent=r;d.querySelector('.r2').textContent=r;d.querySelector('.s').textContent=s;table.append(d)})};
 const flipAll=down=>table.querySelectorAll('.pc').forEach((c,i)=>setTimeout(()=>c.classList.toggle('down',down),still?0:i*90));
 function start(){const d=court.slice().sort(()=>Math.random()-.5);shown=d.slice(0,6);left=d.slice(6,11);step=1;
  deal(shown,false);tell(1);end.hidden=true;go.querySelector('span').textContent='จำได้แล้ว';go.querySelector('small').textContent='Got it';go.disabled=false}
 go.addEventListener('click',()=>{if(step===1){step=2;go.disabled=true;tell(2);flipAll(true);
   setTimeout(()=>{deal(left,true);setTimeout(()=>{flipAll(false);tell(3);end.hidden=false;step=3;
    go.querySelector('span').textContent='อีกครั้ง';go.querySelector('small').textContent='Again';go.disabled=false},still?0:120)},still?300:1700)}
  else if(step===3)start()});
 start();
})();

// sparkle trail, faint
if(matchMedia('(prefers-reduced-motion: no-preference)').matches){const layer=document.createElement('div');layer.className='trail';layer.setAttribute('aria-hidden','true');
 document.body.append(layer);let t0=0,lx=-99,ly=-99,alive=0;
 addEventListener('pointermove',e=>{const t=performance.now();if(t-t0<55||alive>14)return;if(Math.hypot(e.clientX-lx,e.clientY-ly)<18)return;
  t0=t;lx=e.clientX;ly=e.clientY;const s=document.createElement('i');s.style.left=lx+'px';s.style.top=ly+'px';
  s.style.setProperty('--s',(.45+Math.random()*.45).toFixed(2));s.style.setProperty('--dx',(Math.random()*14-7).toFixed(1)+'px');
  layer.append(s);alive++;s.addEventListener('animationend',()=>{s.remove();alive--})},{passive:true})}
"""

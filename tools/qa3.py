#!/usr/bin/env python3
"""v3 全面 QA（含三级目录折叠、拖宽到最小/最大、滚动高亮）。v2 部分：：7 种宽度 × 全部页面；逐一点击目录开关/折叠、图例、标记模式、details、地图三视图（实时地图在 390/1440 抽测）、翻卡、故事播放、测验、背诵模式、视频；
断言：无横向溢出、无越界元素、兄弟元素无重叠、无 JS 错误、无坏锚点/坏站内链接。用法：python3 tools/qa2.py [页面...]"""
import os, sys, json, re, subprocess, time
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(R, "docs")
PAGES = sys.argv[1:] or [f[:-5] for f in sorted(os.listdir(D)) if f.endswith(".html")]
WS = [360, 390, 430, 768, 1024, 1440, 1920]
PORT = 8731
srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
CHECK = r"""()=>{const vw=document.documentElement.clientWidth;const over=[];
const skip='.sky,.era,.profile,.tw,.mind,.emp,.scene,.gm-view,.lm,svg,.toc,.nav,pre,.leaflet-container,.vbox';
document.querySelectorAll('body *').forEach(e=>{if(e.closest(skip))return;const r=e.getBoundingClientRect();if(!r.width||!r.height)return;
 const cs=getComputedStyle(e);if(cs.position==='fixed'||cs.visibility==='hidden'||cs.display==='none')return;
 if(r.right>vw+1||r.left<-1)over.push(e.tagName+'.'+String(e.className).slice(0,40)+' ['+Math.round(r.left)+','+Math.round(r.right)+']')});
const SEL='.toc-tools,.toc-tabs,.lvb,.tree .row,.grid,.flow,.chips,.mx-tabs,.tools,.pager,.lm-bar,.vact,.op,.dots,.gm-bar,.msteps,.ess .pil,.ane,.vids,.gm-leg,.sbar,.anno .lg,.fab,.top';
const ovl=[];document.querySelectorAll(SEL).forEach(c=>{if(c.offsetParent===null&&getComputedStyle(c).position!=='fixed')return;
 const ch=[...c.children].filter(x=>{const s=getComputedStyle(x);return s.display!=='none'&&s.position!=='absolute'&&s.position!=='fixed'&&x.getBoundingClientRect().width>0});
 for(let i=0;i<ch.length;i++)for(let j=i+1;j<ch.length;j++){const a=ch[i].getBoundingClientRect(),b=ch[j].getBoundingClientRect();
  const w=Math.min(a.right,b.right)-Math.max(a.left,b.left),h=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
  if(w>2&&h>2)ovl.push(c.className.toString().slice(0,24)+': '+(ch[i].textContent||'').trim().slice(0,12)+' × '+(ch[j].textContent||'').trim().slice(0,12)+' ('+Math.round(w)+'x'+Math.round(h)+')')}});
const ids=new Set([...document.querySelectorAll('[id]')].map(e=>e.id));const miss=[...new Set([...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(h=>h&&!ids.has(h)))];
return {sw:document.documentElement.scrollWidth,vw,over:over.slice(0,6),ovl:ovl.slice(0,6),miss}}"""
INTERACT = r"""async(o)=>{const sl=ms=>new Promise(r=>setTimeout(r,ms));const n={};const c=(sel,k)=>{const L=[...document.querySelectorAll(sel)];L.forEach(e=>{try{e.click()}catch(x){}});n[k]=(n[k]||0)+L.length};
document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));document.querySelectorAll('section.sec').forEach(s=>s.style.contentVisibility='visible');
c('.toc [role=tab][data-tt=site]','tocTab');document.querySelectorAll('.site details').forEach(d=>d.open=true);c('.toc [role=tab][data-tt=page]','tocTab');
document.querySelectorAll('details').forEach(d=>{d.open=true});n.details=document.querySelectorAll('details').length;
c('[data-mode=cloze]','cloze');await sl(50);c('main .k','clozeReveal');c('[data-mode=cloze]','cloze');c('[data-mode=plain]','plain');c('[data-mode=plain]','plain');
c('#thBtn','theme');await sl(80);c('#thBtn','theme');
for(const p of ['t','c']){c('.mx-tabs [data-p='+p+']','mapTab_'+p);await sl(120)}
c('.gm-leg li:nth-child(2)','legend');c('.gm-z [data-z="1"]','zoom');c('.gm-z [data-z="0"]','zoom');
c('.flip','flip');c('#flipAll','flipAll');
document.querySelectorAll('.story').forEach(s=>{const b=s.querySelector('[data-a=n]');if(b){b.click();b.click();n.story=(n.story||0)+1}const d=s.querySelectorAll('.dot');if(d.length)d[d.length-1].click()});
document.querySelectorAll('.quiz .qq').forEach(q=>{const b=q.querySelector('button.o');if(b){b.click();n.quiz=(n.quiz||0)+1}});
c('[data-recite]','recite');c('.creed .ln','reciteLine');c('[data-recite]','recite');
if(o.video){const v=document.querySelector('.vid [data-a=yt]');if(v){v.click();n.video=1}const m=document.querySelectorAll('.vid [data-a=mp4]');if(m[1]){m[1].click();n.mp4=1}}
await sl(400);document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));return n}"""

TOCT = r"""async()=>{const sl=ms=>new Promise(r=>setTimeout(r,ms));const n={tg:0,lv:0};const T=document.getElementById('toc');
for(const k of [3,1,2,3]){T.querySelector('.lvb [data-lv="'+k+'"]').click();n.lv++;await sl(20)}
const tgs=[...T.querySelectorAll('.tree .tg')];for(const b of tgs){b.click();b.click();n.tg+=2}
const A=()=>T.querySelector('#tocAll').click();const st=()=>[!T.querySelector('.tree li.has.closed'),T.querySelectorAll('.tree li.has:not(.closed)').length===0];let allOpen=false,allClosed=false;for(let i=0;i<3;i++){A();const [o,c]=st();allOpen=allOpen||o;allClosed=allClosed||c}
T.querySelector('#tocWrap').click();await sl(30);T.querySelector('#tocWrap').click();
// 编号一致：目录编号 = 正文标题 data-no
let bad=[];T.querySelectorAll('.tree a').forEach(a=>{const h=document.getElementById(a.getAttribute('href').slice(1));const no=a.querySelector('.no').textContent;if(!h||h.getAttribute('data-no')!==no)bad.push(no)});
const lv=[1,2,3].map(k=>T.querySelectorAll('.tree li.lv'+k).length);
return {n,allOpen,allClosed,bad:bad.slice(0,5),lv}}"""
TOCCHK = r"""(st)=>{const T=document.getElementById('toc'),r=T.getBoundingClientRect(),m=document.getElementById('main').getBoundingClientRect(),vw=document.documentElement.clientWidth;
const clip=[];if(!document.documentElement.classList.contains('toc-nw'))T.querySelectorAll('.tree .tx').forEach(x=>{if(x.offsetParent&&x.scrollWidth>x.clientWidth+1)clip.push(x.textContent.slice(0,12))});
const bd=T.querySelector('.toc-bd');const hov=!document.documentElement.classList.contains('toc-nw')&&bd.scrollWidth>bd.clientWidth+1;
return {w:Math.round(r.width),right:Math.round(r.right),mainL:Math.round(m.left),mainW:Math.round(m.width),vw,sw:document.documentElement.scrollWidth,clip:clip.slice(0,4),hov,
 lim:window.ProphetsToc?window.ProphetsToc.lim():null}}"""
def drag(pg, cdp, mob, to_x):
    bb = pg.locator(".toc-rs").bounding_box(); x0 = bb["x"] + bb["width"] / 2; y0 = bb["y"] + bb["height"] / 2
    if mob:   # 触控：CDP 触摸事件 → Pointer Events
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x0, "y": y0}]})
        for i in range(1, 9): cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x0 + (to_x - x0) * i / 8, "y": y0}]}); pg.wait_for_timeout(16)
        cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    else:
        pg.mouse.move(x0, y0); pg.mouse.down(); pg.mouse.move(to_x, y0, steps=8); pg.mouse.up()
    pg.wait_for_timeout(120)
fails = 0; out = {}; inter_tot = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    def run_one(b, pg_, w):
        global fails
        mob = w < 768
        ctx = b.new_context(viewport={"width": w, "height": 860}, device_scale_factor=1, is_mobile=mob, has_touch=mob)
        ctx.route(re.compile(r"youtube|mux\.com|ytimg"), lambda r: r.abort())
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
        pg.on("console", lambda m: errs.append("console:" + m.text[:120]) if m.type == "error" and "net::ERR" not in m.text and "Failed to load resource" not in m.text else None)
        pg.goto(f"http://127.0.0.1:{PORT}/{pg_}.html"); pg.wait_for_timeout(250)
        pg.wait_for_timeout(700)
        cdp = ctx.new_cdp_session(pg); terr = []
        if mob or w < 1100: pg.click("#tocBtn"); pg.wait_for_timeout(300)
        tt = pg.evaluate(TOCT)
        if tt["bad"]: terr.append("toc numbering mismatch " + str(tt["bad"]))
        if not (tt["allOpen"] and tt["allClosed"]): terr.append("expand/collapse-all failed")
        sizes = {}
        for lab, tx in (("min", 0), ("max", w + 50)):
            drag(pg, cdp, mob, tx); c = pg.evaluate(TOCCHK, None); c2 = pg.evaluate(CHECK); sizes[lab] = c["w"]
            lo, hi = c["lim"]
            if abs(c["w"] - (lo if lab == "min" else hi)) > 2: terr.append(f"drag {lab}: w={c['w']} lim={c['lim']}")
            if c["sw"] > c["vw"] or c2["over"] or c2["ovl"]: terr.append(f"overflow at toc {lab}: sw={c['sw']} {c2['over'][:2]} {c2['ovl'][:2]}")
            if w >= 1100 and c["mainL"] < c["right"] - 1: terr.append(f"toc overlaps main at {lab}")
            if c["clip"] or c["hov"]: terr.append(f"toc text clipped at {lab}: {c['clip']}")
        pg.dblclick(".toc-rs"); pg.wait_for_timeout(100)
        pg.evaluate("localStorage.removeItem('prophets.tocw');localStorage.removeItem('prophets.tocwm')")
        # 滚动高亮：跳到页面后部某标题，检查目录高亮
        pg.evaluate("()=>{const hs=[...document.querySelectorAll('main [data-no]')];const h=hs[Math.floor(hs.length*0.7)];document.querySelectorAll('section.sec').forEach(s=>s.style.contentVisibility='visible');h.scrollIntoView();window.__spy=h.id}")
        pg.wait_for_timeout(450)
        spy = pg.evaluate("()=>{const a=document.querySelector('#toc .tree a.on');return a?a.getAttribute('href').slice(1):null}")
        if not spy: terr.append("scrollspy: no active link")
        if mob or w < 1100: pg.click(".scrim", force=True) if pg.locator(".scrim").is_visible() else None; pg.evaluate("document.documentElement.classList.remove('toc-open')")
        n = pg.evaluate(INTERACT, {"video": w in (390, 1440)})
        n.update({"tocToggle": tt["n"]["tg"], "tocLevel": tt["n"]["lv"], "tocDrag": 2, "tocL1": tt["lv"][0], "tocL2": tt["lv"][1], "tocL3": tt["lv"][2]})
        if w in (390, 1440) and pg.locator(".mx-tabs [data-p=l]").count():
            pg.locator(".mx-tabs [data-p=l]").first.click(); pg.wait_for_timeout(2500); n["live"] = pg.evaluate("document.querySelectorAll('.leaflet-container').length")
        for k, v in n.items(): inter_tot[k] = inter_tot.get(k, 0) + (v if isinstance(v, int) else 0)
        r = pg.evaluate(CHECK); r["errs"] = errs + terr; r["n"] = n; r["toc"] = sizes
        if w in (390, 1440) and "live" in n and n["live"] < 1: r["errs"].append("live map did not init")
        bad = r["sw"] > r["vw"] or r["over"] or r["ovl"] or errs or r["miss"]
        fails += bool(bad); out[f"{pg_}@{w}"] = r
        print(("❌" if bad else "✅"), pg_, w, "" if not bad else {k: r[k] for k in ("sw", "vw", "over", "ovl", "miss", "errs")}, flush=True)
        ctx.close()

    for pg_ in PAGES:
        for w in WS:
            for attempt in range(3):
                try:
                    run_one(b, pg_, w); break
                except Exception as ex:
                    print("⚠️ retry", pg_, w, str(ex)[:100], flush=True)
                    try: b.close()
                    except Exception: pass
                    time.sleep(3); b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
            else:
                fails += 1; print("❌", pg_, w, "crashed 3x", flush=True)
    b.close()
srv.terminate()
ids = {f: set(re.findall(r'id="([^"]+)"', open(f"{D}/{f}.html", encoding="utf-8").read())) for f in [x[:-5] for x in os.listdir(D) if x.endswith(".html")]}
xm = []
for f in ids:
    s = open(f"{D}/{f}.html", encoding="utf-8").read()
    for h, a in re.findall(r'href="([a-z0-9]+)\.html(?:#([^"]+))?"', s):
        if h not in ids or (a and a not in ids[h]): xm.append((f, h, a))
    for src in re.findall(r'(?:src|data-src|href)="(assets/[^"?#]+)', s):
        if not os.path.exists(os.path.join(D, src)): xm.append((f, "asset", src))
print("internal link/asset misses:", xm); fails += len(xm)
print("interactions:", json.dumps(inter_tot, ensure_ascii=False))
json.dump(dict(results=out, interactions=inter_tot, misses=xm), open(os.path.join(R, "build", "data", "qa3_report.json"), "w"), ensure_ascii=False, indent=1)
print("FAILS", fails); sys.exit(1 if fails else 0)

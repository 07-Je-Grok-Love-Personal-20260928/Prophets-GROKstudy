#!/usr/bin/env python3
"""v2 全面 QA：7 种宽度 × 全部页面；逐一点击目录开关/折叠、图例、标记模式、details、地图三视图（实时地图在 390/1440 抽测）、翻卡、故事播放、测验、背诵模式、视频；
断言：无横向溢出、无越界元素、兄弟元素无重叠、无 JS 错误、无坏锚点/坏站内链接。用法：python3 tools/qa2.py [页面...]"""
import os, sys, json, re, subprocess, time
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(R, "docs")
PAGES = sys.argv[1:] or [f[:-5] for f in sorted(os.listdir(D)) if f.endswith(".html")]
WS = [360, 390, 430, 768, 1024, 1440, 1920]
PORT = 8730
srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
CHECK = r"""()=>{const vw=document.documentElement.clientWidth;const over=[];
const skip='.sky,.era,.profile,.tw,.mind,.emp,.scene,.gm-view,.lm,svg,.toc,.nav,pre,.leaflet-container,.vbox';
document.querySelectorAll('body *').forEach(e=>{if(e.closest(skip))return;const r=e.getBoundingClientRect();if(!r.width||!r.height)return;
 const cs=getComputedStyle(e);if(cs.position==='fixed'||cs.visibility==='hidden'||cs.display==='none')return;
 if(r.right>vw+1||r.left<-1)over.push(e.tagName+'.'+String(e.className).slice(0,40)+' ['+Math.round(r.left)+','+Math.round(r.right)+']')});
const SEL='.grid,.flow,.chips,.mx-tabs,.tools,.pager,.lm-bar,.vact,.op,.dots,.gm-bar,.msteps,.ess .pil,.ane,.vids,.gm-leg,.sbar,.anno .lg,.fab,.top';
const ovl=[];document.querySelectorAll(SEL).forEach(c=>{if(c.offsetParent===null&&getComputedStyle(c).position!=='fixed')return;
 const ch=[...c.children].filter(x=>{const s=getComputedStyle(x);return s.display!=='none'&&s.position!=='absolute'&&s.position!=='fixed'&&x.getBoundingClientRect().width>0});
 for(let i=0;i<ch.length;i++)for(let j=i+1;j<ch.length;j++){const a=ch[i].getBoundingClientRect(),b=ch[j].getBoundingClientRect();
  const w=Math.min(a.right,b.right)-Math.max(a.left,b.left),h=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
  if(w>2&&h>2)ovl.push(c.className.toString().slice(0,24)+': '+(ch[i].textContent||'').trim().slice(0,12)+' × '+(ch[j].textContent||'').trim().slice(0,12)+' ('+Math.round(w)+'x'+Math.round(h)+')')}});
const ids=new Set([...document.querySelectorAll('[id]')].map(e=>e.id));const miss=[...new Set([...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(h=>h&&!ids.has(h)))];
return {sw:document.documentElement.scrollWidth,vw,over:over.slice(0,6),ovl:ovl.slice(0,6),miss}}"""
INTERACT = r"""async(o)=>{const sl=ms=>new Promise(r=>setTimeout(r,ms));const n={};const c=(sel,k)=>{const L=[...document.querySelectorAll(sel)];L.forEach(e=>{try{e.click()}catch(x){}});n[k]=(n[k]||0)+L.length};
document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));document.querySelectorAll('section.sec').forEach(s=>s.style.contentVisibility='visible');
c('#tocBtn','toc');await sl(150);c('.toc .tg','tocGroup');c('#tocAll','tocAll');c('#tocAll','tocAll');c('#tocBtn','toc');
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
fails = 0; out = {}; inter_tot = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for pg_ in PAGES:
        for w in WS:
            mob = w < 768
            ctx = b.new_context(viewport={"width": w, "height": 860}, device_scale_factor=1, is_mobile=mob, has_touch=mob)
            ctx.route(re.compile(r"youtube|mux\.com|ytimg"), lambda r: r.abort())
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
            pg.on("console", lambda m: errs.append("console:" + m.text[:120]) if m.type == "error" and "net::ERR" not in m.text and "Failed to load resource" not in m.text else None)
            pg.goto(f"http://127.0.0.1:{PORT}/{pg_}.html"); pg.wait_for_timeout(250)
            n = pg.evaluate(INTERACT, {"video": w in (390, 1440)})
            if w in (390, 1440) and pg.locator(".mx-tabs [data-p=l]").count():
                pg.locator(".mx-tabs [data-p=l]").first.click(); pg.wait_for_timeout(2500); n["live"] = pg.evaluate("document.querySelectorAll('.leaflet-container').length")
            for k, v in n.items(): inter_tot[k] = inter_tot.get(k, 0) + (v if isinstance(v, int) else 0)
            r = pg.evaluate(CHECK); r["errs"] = errs; r["n"] = n
            if w in (390, 1440) and "live" in n and n["live"] < 1: r["errs"].append("live map did not init")
            bad = r["sw"] > r["vw"] or r["over"] or r["ovl"] or errs or r["miss"]
            fails += bool(bad); out[f"{pg_}@{w}"] = r
            print(("❌" if bad else "✅"), pg_, w, "" if not bad else {k: r[k] for k in ("sw", "vw", "over", "ovl", "miss", "errs")}, flush=True)
            ctx.close()
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
json.dump(dict(results=out, interactions=inter_tot, misses=xm), open(os.path.join(R, "build", "data", "qa2_report.json"), "w"), ensure_ascii=False, indent=1)
print("FAILS", fails); sys.exit(1 if fails else 0)

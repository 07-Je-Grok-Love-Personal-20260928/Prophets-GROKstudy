#!/usr/bin/env python3
"""响应式 QA：390/768/1440 宽度下检查横向溢出、越界元素、JS 错误、坏的内部链接锚点。"""
import os, sys, json, re
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(R, "docs")
PAGES = [f[:-5] for f in sorted(os.listdir(D)) if f.endswith(".html")]
WS = [390, 768, 1440]; out = {}; bad = 0
JS = """()=>{const vw=document.documentElement.clientWidth;const o=[];
document.querySelectorAll('body *').forEach(e=>{if(e.closest('.era,.profile,.tw,.scrollx,svg,.toc,.nav,nav,pre,.mapwrap'))return;const r=e.getBoundingClientRect();
if(r.width&&(r.right>vw+1||r.left<-1)){const cs=getComputedStyle(e);if(cs.position!=='fixed'&&cs.visibility!=='hidden')o.push(e.tagName+'.'+e.className+' '+Math.round(r.left)+'-'+Math.round(r.right))}});
const ids=new Set([...document.querySelectorAll('[id]')].map(e=>e.id));const miss=[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(h=>h&&!ids.has(h));
return {sw:document.documentElement.scrollWidth,vw,over:o.slice(0,8),miss:[...new Set(miss)]}}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for pg_ in PAGES:
        for w in WS:
            pg = b.new_page(viewport={"width": w, "height": 900}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(f"file://{D}/{pg_}.html"); pg.wait_for_timeout(300)
            pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))"); pg.wait_for_timeout(300)
            r = pg.evaluate(JS); r["errs"] = errs
            fail = r["sw"] > r["vw"] or r["over"] or errs or r["miss"]
            bad += bool(fail); out[f"{pg_}@{w}"] = r
            print(("❌" if fail else "✅"), pg_, w, "" if not fail else r)
            pg.close()
    # cross-page anchors
    ids = {}
    for f in PAGES: ids[f] = set(re.findall(r'id="([^"]+)"', open(f"{D}/{f}.html", encoding="utf-8").read()))
    xm = []
    for f in PAGES:
        for h, a in re.findall(r'href="([a-z]+)\.html#([^"]+)"', open(f"{D}/{f}.html", encoding="utf-8").read()):
            if h not in ids or a not in ids[h]: xm.append((f, h, a))
    print("cross-page anchor misses:", xm); bad += len(xm)
json.dump(out, open(os.path.join(R, "build", "data", "qa_report.json"), "w"), ensure_ascii=False, indent=1)
print("FAILS", bad); sys.exit(1 if bad else 0)

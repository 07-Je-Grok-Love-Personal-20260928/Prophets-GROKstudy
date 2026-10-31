# -*- coding: utf-8 -*-
import re, html as H
from lib import VER
PAGES = [("index", "🏠 首页"), ("bible", "📖 整本圣经"), ("history", "🗺️ 史地文化"), ("isaiah", "👑 以赛亚书"), ("jeremiah", "😢 耶利米·哀歌"),
         ("ezekiel", "🔥 以西结书"), ("daniel", "🦁 但以理书"), ("minor1", "🦅 亚述期小先知"), ("minor2", "⚔️ 巴比伦期小先知"), ("minor3", "🏛️ 波斯期小先知"),
         ("confessions", "📚 信条对照"), ("creeds", "✨ 三大信经"), ("compare", "⚖️ 信经对比"), ("memory", "🧠 速记自测"), ("sources", "🔖 来源")]
TITLE = "先知书 · 欧陆改革宗深读"
def toc(body):
    hs = re.findall(r'<h([23]) id="([^"]+)"[^>]*>(.*?)</h\1>', body)
    groups = []
    for lv, id, t in hs:
        t = re.sub(r"<[^>]+>", "", t)
        if lv == "2" or not groups: groups.append([(id, t), []])
        else: groups[-1][1].append((id, t))
    out = []
    for (id, t), ch in groups:
        if ch:
            sub = "".join(f'<li class="l3"><a href="#{i}">{x}</a></li>' for i, x in ch)
            out.append(f'<li class="l2 has"><div class="grp"><a href="#{id}">{t}</a><button class="tg" aria-label="展开/收起" aria-expanded="true">▼</button></div><ol>{sub}</ol></li>')
        else: out.append(f'<li class="l2"><a href="#{id}">{t}</a></li>')
    return "".join(out)
def page(slug, title, body, desc=""):
    nav = "".join(f'<a href="{s}.html"{" class=on" if s == slug else ""}>{t}</a>' for s, t in PAGES)
    i = [s for s, _ in PAGES].index(slug)
    pv = PAGES[i - 1] if i > 0 else None; nx = PAGES[i + 1] if i + 1 < len(PAGES) else None
    pager = '<nav class="pager">' + (f'<a href="{pv[0]}.html"><small>← 上一页</small>{pv[1]}</a>' if pv else "<span></span>") + (f'<a href="{nx[0]}.html"><small>下一页 →</small>{nx[1]}</a>' if nx else "") + "</nav>"
    tc = toc(body)
    return f'''<!doctype html><html lang="zh-Hans" data-theme="night"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{H.escape(title)} · {TITLE}</title><meta name="description" content="{H.escape(desc or title)}"><meta name="theme-color" content="#0b1020">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🔥%3C/text%3E%3C/svg%3E">
<script>(function(h){{h.classList.add('js');try{{var t=localStorage.getItem('prophets.theme');if(t)h.setAttribute('data-theme',t);if(localStorage.getItem('prophets.toc')==='off')h.classList.add('toc-off')}}catch(e){{}}}})(document.documentElement)</script>
<link rel="stylesheet" href="assets/site.css?v={VER}"></head><body>
<div class="prog" aria-hidden="true"></div>
<header class="top"><button class="ib" id="tocBtn" aria-label="显示/隐藏目录">☰ <small>目录</small></button><a class="brand" href="index.html">📜 <span>{TITLE}</span></a><nav class="nav" aria-label="页面">{nav}</nav><button class="ib" id="thBtn" aria-label="切换深色/羊皮纸主题">🌓</button></header>
<div class="wrap"><aside class="toc" aria-label="本页目录"><h5>本页目录 · {H.escape(title)}</h5><input id="tocQ" type="search" placeholder="🔍 筛选目录…" aria-label="筛选目录"><div class="tools"><button class="ib" id="tocAll">⇅ 全部展开/收起</button></div><ol>{tc}</ol></aside><div class="scrim"></div>
<main id="main">{body}{pager}</main></div>
<footer>📜 {TITLE} · 版本 {VER} · GROKstudy｜三大普世信经与三项联合信条引文逐字取自 <a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>（脚注编号省略）；经文为和合本。其余讲解为本站学习概述。<a href="sources.html">来源与核对 →</a></footer>
<div class="fab"><button class="ib" id="toTop" aria-label="回到顶部">⬆</button></div>
<script src="assets/site.js?v={VER}" defer></script></body></html>'''

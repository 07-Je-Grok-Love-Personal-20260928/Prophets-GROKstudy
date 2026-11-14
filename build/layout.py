# -*- coding: utf-8 -*-
import re, html as H
from lib import VER
PAGES = [("index", "🏠 首页"), ("bible", "📖 整本圣经"), ("history", "🏺 史地文化"), ("atlas", "🗺️ 地图集"), ("isaiah", "👑 以赛亚书"), ("jeremiah", "😢 耶利米·哀歌"),
         ("ezekiel", "🔥 以西结书"), ("daniel", "🦁 但以理书"), ("minor1", "🦅 亚述期小先知"), ("minor2", "⚔️ 巴比伦期小先知"), ("minor3", "🏛️ 波斯期小先知"),
         ("confessions", "📚 信条对照"), ("creeds", "✨ 三大信经"), ("compare", "⚖️ 信经对比"), ("memory", "🧠 速记自测"), ("sources", "🔖 来源")]
TITLE = "先知书 · 欧陆改革宗深读"
GROUPS = [("🧭 导论 · 史地", ["index", "bible", "history", "atlas"]), ("👑 大先知书", ["isaiah", "jeremiah", "ezekiel", "daniel"]),
          ("🦅 十二小先知", ["minor1", "minor2", "minor3"]), ("📚 信条 · 记忆", ["confessions", "creeds", "compare", "memory", "sources"])]
CN = re.compile(r'^((?:<[^>]+>|[^\w<])*?\s*)(?:[一二三四五六七八九十]+、|\d+[\.、]\s*)')
def outline(body):
    """三级大纲：h2/h3/h4（带 id）按嵌套编号 1 / 1.1 / 1.1.1，并生成可折叠目录树。"""
    if not re.search(r'<h4 id=', body):   # 无显式三级标题的页面：卡片标题 h4 自动成为三级
        n = [0]
        def aid(m):
            n[0] += 1; return f'<h4 id="s{n[0]}" data-aid{m.group(1)}>'
        body = re.sub(r'<h4((?![^>]*\bid=)[^>]*)>', aid, body)
    nodes, stack, cnt = [], [], {}
    def rep(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        lv = 1 if 'class="part"' in attrs else int(tag[1]); id = re.search(r'id="([^"]+)"', attrs).group(1)
        while stack and stack[-1][0] >= lv: stack.pop()
        depth = len(stack) + 1
        if depth > 3: return m.group(0)
        parent = stack[-1][1] if stack else None
        key = parent["no"] if parent else ""
        cnt[key] = cnt.get(key, 0) + 1
        no = (key + "." if key else "") + str(cnt[key])
        inner = CN.sub(r'\1', inner, count=1)
        node = {"id": id, "no": no, "t": re.sub(r"<[^>]+>", "", inner).strip(), "ch": [], "d": depth}
        (parent["ch"] if parent else nodes).append(node)
        stack.append((lv, node))
        show = "data-aid" not in attrs
        return f'<{tag}{attrs} data-no="{no}">' + (f'<span class="hn">{no}</span>' if show else "") + f'{inner}</{tag}>'
    body = re.sub(r'<(h[234])(\s[^>]*\bid="[^"]+"[^>]*)>(.*?)</\1>', rep, body, flags=re.S)
    def li(nd):
        ch = "".join(li(c) for c in nd["ch"])
        cls = f'lv{nd["d"]}' + (" has" if ch else "") + (" closed" if ch and nd["d"] >= 2 else "")
        tg = f'<button class="tg" aria-expanded="{"false" if nd["d"] >= 2 else "true"}" aria-label="展开/收起">▾</button>' if ch else '<i class="sp"></i>'
        return (f'<li class="{cls}"><div class="row">{tg}<a href="#{nd["id"]}"><b class="no">{nd["no"]}</b><span class="tx">{H.escape(nd["t"])}</span></a></div>'
                + (f'<ol>{ch}</ol>' if ch else "") + "</li>")
    return body, "".join(li(n) for n in nodes), nodes
PARTS = {
 "index": [("start", "go", "🚀", "入门"), ("books", "map17", "📚", "十七卷与四百年"), ("why", "whyp", "💎", "为什么读")],
 "bible": [("canon", "b-a", "📚", "正典与主线"), ("covenant", "b-b", "🔗", "神学骨架：约与职分"), ("reading", "b-c", "🔍", "读法与金线")],
 "history": [("chrono", "h-time", "⏳", "时间：年代 · 帝国 · 列王"), ("map", "h-space", "🌍", "空间与文化：地图 · 古近东"), ("treaty", "h-cov", "📜", "约与世界：条约 · 被掳 · 考古")],
 "atlas": [("atl-how", "a-use", "🧭", "用法"), ("atl-land", "a-maps", "🗺️", "十一幅地图（五组）"), ("atl-anim", "a-media", "🎬", "动画 · 视频 · 来源")],
 "confessions": [("conf-what", "c-know", "🧾", "认识三项联合信条"), ("conf-themes", "c-th", "🔍", "逐主题对照"), ("conf-idx", "c-more", "🔎", "索引 · 比较 · 关系")],
 "compare": [("cmp-id", "k-who", "🪪", "是什么：身份与对比"), ("cmp-heresy", "k-why", "🛡️", "为什么：异端 · 历史 · 和子"), ("cmp-why", "k-so", "🧠", "所以：三个的必要 · 连接 · 自测")],
 "creeds": [("cr-how", "r-how", "🧠", "方法"), ("cr-apostles", "r-text", "📜", "三大信经干净背诵版"), ("cr-hist", "r-link", "🔗", "连接先知书")],
 "memory": [("m-big", "y-hook", "🔑", "记忆钩：口诀 · 君王 · 术语"), ("m-flip", "y-drill", "🃏", "练习：翻卡 · 测验"), ("m-plan", "y-plan", "📅", "计划")],
 "sources": [("src-cci", "z-text", "📜", "原文与核对"), ("src-bible", "z-ref", "🌐", "资料与参考"), ("src-ver", "z-ver", "🗂️", "版本")],
}
def addparts(slug, body):
    for before, pid, ic, t in PARTS.get(slug, []):
        tag = f'<h2 id="{before}"'
        assert tag in body, (slug, before)
        body = body.replace(tag, f'<h2 id="{pid}" class="part" data-lv="1">{ic} {t}</h2>' + tag, 1)
    return body
def sitenav(slug):
    lab = dict(PAGES); o = []
    for g, ss in GROUPS:
        a = "".join(f'<a href="{x}.html"{" class=on aria-current=page" if x == slug else ""}>{lab[x]}</a>' for x in ss)
        o.append(f'<details class="sg"{" open" if slug in ss else ""}><summary>{g} <small>{len(ss)}</small></summary><div>{a}</div></details>')
    return "".join(o)
ANNO = ('<details class="anno"><summary>🖍️ 笔记标记图例 · 背诵工具 <span class="v2b">v3</span></summary><div class="lg">'
        '<span><b class="k">金色荧光＝重点</b>：必记的核心句</span><span><span class="h">红色波浪线＝难点</span>：易误解处</span>'
        '<span><span class="xr">紫色双线＝基督</span>：指向基督</span><span><span class="cv">青色虚线＝圣约</span>：约的线索</span>'
        '<span><span class="ap">绿色实线＝应用</span>：今天怎么活</span><span><span class="mm">粉色底纹＝记忆钩</span>：口诀/画面</span>'
        '<span><span class="box">框＝术语</span>：定义要会讲</span><span><span class="ul-r">红实线＝审判/警告</span></span><span><span class="ul-b">蓝双线＝应许</span></span><span><span class="d">蓝色年代</span> · <span class="pl">绿色地点</span> · <span class="pn">橙色人物</span></span><span>区块：⭐重点 ⚠️难点 ✝️基督 🔗圣约 🌱应用 🧠记忆</span></div>'
        '<div class="tools"><button class="ib" data-mode="cloze" aria-pressed="false">🙈 遮盖重点（点击逐个揭开）</button><button class="ib" data-mode="plain" aria-pressed="false">🎨 彩色 / 简洁 切换</button></div></details>')
SPEC = '<script type="speculationrules">{"prefetch":[{"source":"document","where":{"href_matches":"*.html"},"eagerness":"moderate"}]}</script>'
def sections(body):
    """按 h2 切分为 <section class=sec>，供 content-visibility 按需渲染。"""
    parts = re.split(r'(?=<h[23] id=|<h4 id="[^"]+" class="?hs4)', body)
    head, rest = parts[0], parts[1:]
    return head + ANNO + "".join(f'<section class="sec">{p}</section>' for p in rest)
def page(slug, title, body, desc=""):
    nav = "".join(f'<a href="{s}.html"{" class=on" if s == slug else ""}>{t}</a>' for s, t in PAGES)
    i = [s for s, _ in PAGES].index(slug)
    pv = PAGES[i - 1] if i > 0 else None; nx = PAGES[i + 1] if i + 1 < len(PAGES) else None
    pager = '<nav class="pager">' + (f'<a href="{pv[0]}.html"><small>← 上一页</small>{pv[1]}</a>' if pv else "<span></span>") + (f'<a href="{nx[0]}.html"><small>下一页 →</small>{nx[1]}</a>' if nx else "") + "</nav>"
    body = addparts(slug, body)
    body, tc, _ = outline(body)
    return f'''<!doctype html><html lang="zh-Hans" data-theme="night"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{H.escape(title)} · {TITLE}</title><meta name="description" content="{H.escape(desc or title)}"><meta name="theme-color" content="#0c1024"><meta name="view-transition" content="same-origin">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🔥%3C/text%3E%3C/svg%3E">
<script>(function(h){{h.classList.add('js');try{{var t=localStorage.getItem('prophets.theme');if(t)h.setAttribute('data-theme',t);if(localStorage.getItem('prophets.toc')==='off')h.classList.add('toc-off');if(localStorage.getItem('prophets.plain')==='1')h.classList.add('plain');var w=+localStorage.getItem('prophets.tocw'),m=+localStorage.getItem('prophets.tocwm');if(w)h.style.setProperty('--tocw',w+'px');if(m)h.style.setProperty('--tocm',m+'px');if(localStorage.getItem('prophets.tocnw')==='1')h.classList.add('toc-nw')}}catch(e){{}}}})(document.documentElement)</script>
<link rel="stylesheet" href="assets/site.css?v={VER}">{SPEC}</head><body>
<div class="prog" aria-hidden="true"></div>
<header class="top"><button class="ib" id="tocBtn" aria-label="显示/隐藏目录">☰ <small>目录</small></button><a class="brand" href="index.html">📜 <span>{TITLE}</span></a><nav class="nav" aria-label="页面">{nav}</nav><button class="ib" id="thBtn" aria-label="切换深色/羊皮纸主题">🌓</button></header>
<div class="wrap"><aside class="toc" id="toc" aria-label="目录"><div class="toc-hd"><div class="toc-tabs" role="tablist"><button role="tab" data-tt="page" aria-selected="true">📑 本页目录</button><button role="tab" data-tt="site" aria-selected="false">🗂️ 全站 16 页</button></div></div><div class="toc-bd"><div class="toc-pane on" data-tt="page"><h5>{H.escape(title)}</h5><input id="tocQ" type="search" placeholder="🔍 筛选目录…" aria-label="筛选目录"><div class="toc-tools"><span class="lvb" role="group" aria-label="展开到第几级"><button class="ib" data-lv="1">一级</button><button class="ib" data-lv="2">二级</button><button class="ib" data-lv="3">三级</button></span><button class="ib" id="tocAll" title="全部展开 / 全部收起">⇅ 全部</button><button class="ib" id="tocWrap" aria-pressed="false" title="长标题：换行 / 单行（可拖宽目录）">↔ 单行</button></div><nav class="tree" aria-label="本页三级目录"><ol>{tc}</ol></nav></div><div class="toc-pane" data-tt="site"><nav class="site" aria-label="全站页面">{sitenav(slug)}</nav></div></div><div class="toc-rs" role="separator" aria-orientation="vertical" aria-label="拖动调整目录宽度（双击恢复）" tabindex="0"><i></i></div></aside><div class="scrim"></div>
<main id="main">{sections(body)}{pager}</main></div>
<footer>📜 {TITLE} · 版本 {VER} · GROKstudy｜三大普世信经与三项联合信条引文逐字取自 <a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>（脚注编号省略）；经文为和合本。其余讲解为本站学习概述。<a href="sources.html">来源与核对 →</a></footer>
<div class="fab"><button class="ib" id="toTop" aria-label="回到顶部">⬆</button></div>
<script src="assets/site.js?v={VER}" defer></script></body></html>'''

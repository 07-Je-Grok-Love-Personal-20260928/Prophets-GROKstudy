# -*- coding: utf-8 -*-
import json, re, os, html as H, math
import bible
CCI = os.environ.get("CCI_DIR", "/workspace/cci")
VER = "20261031-v1"
_h = json.load(open(f"{CCI}/heidelberg.json")); _b = json.load(open(f"{CCI}/belgic.json")); _d = json.load(open(f"{CCI}/dort.json")); CREEDS = json.load(open(f"{CCI}/creeds.json"))
HCQ = {q["q"]: dict(q, ld=ld["number"], url=ld.get("url")) for ld in _h["lordsdays"] for q in ld["questions"]}
BCA = {a["number"]: a for a in _b["articles"]}
DT = {i + 1: {a["number"]: dict(a, head=hd["title"]) for a in hd["articles"]} for i, hd in enumerate(_d["heads"])}
DTN = {1: "第一项教义", 2: "第二项教义", 3: "第三、四项教义", 4: "第五项教义"}
def clean(t):
    t = re.sub(r"\^\d+", "", t)
    t = "\n".join(l for l in t.split("\n") if not l.strip().startswith("- "))
    return re.sub(r"\n{3,}", "\n\n", t).strip()
USED = []
def src(doc, n, h=None):
    if doc == "HC":
        q = HCQ[n]; return f"《海德堡要理问答》第{n}问（主日{q['ld']}）", q["url"], clean(q["question"]), clean(q["answer"])
    if doc == "BC":
        a = BCA[n]; return f"《比利时信条》{a['title']}", a["url"], "", clean(a["text"])
    a = DT[h][n]; return f"《多特信经》{DTN[h]} {a['title']}", a["url"], "", clean(a["text"])
def cq(doc, n, h=None, part=None, note=""):
    """三项联合信条逐字引文（来自 ccifellowship.org 抓取数据；脚注上标省略）"""
    lab, url, q, t = src(doc, n, h)
    if part:
        for p in (part if isinstance(part, list) else [part]):
            assert p in t, (doc, n, h, p)
        body = "……".join(part if isinstance(part, list) else [part])
        body = ("……" if not t.startswith((part if isinstance(part, list) else [part])[0]) else "") + body + ("……" if not t.endswith((part if isinstance(part, list) else [part])[-1]) else "")
    else: body = t
    key = f"{doc}{h or ''}.{n}"
    USED.append(dict(key=key, doc=doc, n=n, h=h, label=lab, url=url, parts=(part if isinstance(part, list) else [part]) if part else None, q=q))
    qq = f'<div class="cq-q">{H.escape(q)}</div>' if q else ""
    return (f'<blockquote class="cq reveal" data-k="{key}"><div class="cq-h">📜 {H.escape(lab)} <span class="badge">CCI 逐字</span></div>{qq}'
            f'<div class="cq-t">{H.escape(body)}</div><cite>出处：<a href="{url}" target="_blank" rel="noopener">{url.replace("https://","")}</a>（脚注编号省略）{note}</cite></blockquote>')
VUSED = []
def V(ref, note=""):
    t = bible.verses(ref); VUSED.append(ref)
    return f'<blockquote class="vs reveal"><div>{H.escape(t)}</div><cite>📖 {ref}（和合本）{note}</cite></blockquote>'
def vt(ref): VUSED.append(ref); return bible.verses(ref)
# ---------- components ----------
def H2(id, ic, t, c="var(--blue)"): return f'<h2 id="{id}" style="--c:{c}">{ic} {t}</h2>'
def H3(id, ic, t): return f'<h3 id="{id}">{ic} {t}</h3>'
def co(kind, title, body):
    return f'<div class="co {kind} reveal"><span class="ct">{title}</span>{body}</div>'
KEY = lambda b, t="⭐ 重点": co("key", t, b)
HARD = lambda b, t="⚠️ 难点": co("hard", t, b)
APP = lambda b, t="🌱 应用": co("app", t, b)
BG = lambda b, t="🏺 历史文化背景": co("bg", t, b)
XP = lambda b, t="✝️ 指向基督": co("xp", t, b)
COV = lambda b, t="🔗 圣约神学": co("cov", t, b)
MEM = lambda b, t="🧠 记忆钩": co("mem", t, b)
WHY = lambda b, t="❓ 为什么写": co("why", t, b)
def grid(items, mn=260): return f'<div class="grid" style="--min:{mn}px">{"".join(items)}</div>'
def card(t, b, ic="", c="var(--blue)", cls=""):
    return f'<div class="card top-c reveal {cls}" style="--c:{c}">{("<div class=ic>"+ic+"</div>") if ic else ""}<h4>{t}</h4>{b}</div>'
def table(head, rows, cls=""):
    th = "".join(f"<th>{x}</th>" for x in head)
    tr = "".join("<tr>" + "".join((f'<td class="{c[0]}">{c[1]}</td>' if isinstance(c, tuple) else f"<td>{c}</td>") for c in r) + "</tr>" for r in rows)
    return f'<div class="tw reveal"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
def flow(nodes):
    o = []
    for i, n in enumerate(nodes):
        t, s, c = (n + ("var(--blue)",))[:3] if len(n) < 3 else n
        if i: o.append('<span class="fa" aria-hidden="true">➜</span>')
        o.append(f'<div class="fn" style="--c:{c}"><b>{t}</b><small>{s}</small></div>')
    return f'<div class="flow reveal">{"".join(o)}</div>'
def tl(items, cols=False):
    o = "".join(f'<div class="ti" style="--c:{c}"><span class="y">{y}</span>{t}</div>' for y, t, c in items)
    return f'<div class="tl{" cols" if cols else ""} reveal">{o}</div>'
def story(steps, c="var(--gold)"):
    dots = "".join(f'<button class="dot" aria-label="第{i+1}步">{i+1}</button>' for i in range(len(steps)))
    st = "".join(f'<div class="st"><span class="em">{e}</span><h4>{t}</h4><p>{b}</p></div>' for e, t, b in steps)
    return (f'<div class="story reveal" style="--c:{c}"><div class="sbar"><div class="dots">{dots}</div><button class="ib" data-a="p">◀</button><button class="ib" data-a="n">▶</button><button class="ib" data-a="play">▶ 自动播放</button></div><div class="stage">{st}</div></div>')
def mnem(t, s=""): return f'<div class="mnem reveal">{t}{("<small>"+s+"</small>") if s else ""}</div>'
def kv(pairs): return '<dl class="kv">' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in pairs) + "</dl>"
def quiz(qs, id="q"):
    o = []
    for i, (q, ops, ans, ex) in enumerate(qs):
        b = "".join(f'<button class="o"{" data-ok" if j == ans else ""}>{chr(65+j)}. {op}</button>' for j, op in enumerate(ops))
        o.append(f'<div class="qq"><p>{i+1}. {q}</p><div class="op">{b}</div><div class="ex">💡 {ex}</div></div>')
    return f'<div class="quiz reveal" id="{id}"><div class="tools"><span class="score">得分 0 / {len(qs)}</span><button class="ib" data-a="reset">↺ 重做</button></div>{"".join(o)}</div>'
def flips(items):
    return grid([f'<div class="flip reveal" style="--c:{c}"><div class="fi"><div class="ff"><div class="big">{e}</div><b>{t}</b><small>点击翻面</small></div><div class="fb">{b}</div></div></div>' for e, t, b, c in items], 250)
PALC = ["#f2c14e", "#5aa9ff", "#3ccf8e", "#a98bff", "#ff6b5b", "#2ed3c6", "#ff9f43", "#ff7eb6"]
def mind(center, branches, W=1200, Hh=720):
    """径向思维导图（SVG）。branches: [(title, [leaf,...]), ...]"""
    cx, cy = W / 2, Hh / 2; n = len(branches); o = []
    o.append(f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="思维导图：{H.escape(center)}">')
    for i, (bt, leaves) in enumerate(branches):
        a = -math.pi / 2 + 2 * math.pi * i / n; c = PALC[i % len(PALC)]
        bx, by = cx + math.cos(a) * W * .25, cy + math.sin(a) * Hh * .29
        o.append(f'<g class="br" style="animation-delay:{i*0.08:.2f}s;transform-origin:{cx}px {cy}px">')
        o.append(f'<path class="ml" stroke="{c}" d="M{cx:.0f},{cy:.0f} Q{(cx+bx)/2:.0f},{(cy+by)/2 - 30:.0f} {bx:.0f},{by:.0f}"/>')
        right = math.cos(a) >= -0.05
        lx = bx + (110 if right else -110)
        for j, lf in enumerate(leaves):
            ly = by + (j - (len(leaves) - 1) / 2) * 30
            o.append(f'<path class="ml" stroke="{c}" stroke-width="1.4" d="M{bx + (70 if right else -70):.0f},{by:.0f} C{lx - (20 if right else -20):.0f},{by:.0f} {lx - (30 if right else -30):.0f},{ly:.0f} {lx:.0f},{ly:.0f}"/>')
            o.append(f'<g class="lf"><text x="{lx + (6 if right else -6):.0f}" y="{ly + 5:.0f}" text-anchor="{"start" if right else "end"}">{H.escape(lf)}</text></g>')
        w = max(120, 17 * len(bt) + 28)
        o.append(f'<g class="mb"><rect x="{bx - w/2:.0f}" y="{by - 20:.0f}" width="{w}" height="40" rx="20" fill="{c}" fill-opacity=".22" stroke="{c}"/><text x="{bx:.0f}" y="{by + 6:.0f}" text-anchor="middle" font-weight="800" font-size="16">{H.escape(bt)}</text></g></g>')
    w = max(200, 22 * len(center) + 40)
    o.append(f'<g class="mc"><rect x="{cx - w/2:.0f}" y="{cy - 30:.0f}" width="{w}" height="60" rx="30" fill="#f2c14e"/><text x="{cx:.0f}" y="{cy + 7:.0f}" text-anchor="middle" font-size="21">{H.escape(center)}</text></g></svg>')
    return f'<div class="mind reveal">{"".join(o)}</div>'
def era(rows, y0=-1500, y1=-400, W=1200, title=""):
    """时间跨度条形图（主前年代，负数）。rows: [(label, start, end, color, note)]"""
    rh = 34; top = 30; Hh = top + rh * len(rows) + 40
    X = lambda y: 160 + (y - y0) / (y1 - y0) * (W - 190)
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="{H.escape(title)}">']
    for yy in range((y0 // 100) * 100, y1 + 1, 100):
        if yy < y0: continue
        x = X(yy); o.append(f'<line class="ax" x1="{x:.0f}" y1="{top-6}" x2="{x:.0f}" y2="{Hh-30}"/><text class="tx" x="{x:.0f}" y="{Hh-12}" text-anchor="middle">主前{-yy}</text>')
    for i, (lab, a, b, c, note) in enumerate(rows):
        y = top + i * rh; x1, x2 = X(a), X(b)
        o.append(f'<text x="150" y="{y+20}" text-anchor="end" font-size="14" font-weight="700">{H.escape(lab)}</text>')
        o.append(f'<rect class="bar" style="animation-delay:{i*0.07:.2f}s" x="{x1:.0f}" y="{y+5}" width="{max(4,x2-x1):.0f}" height="{rh-10}" rx="7" fill="{c}" fill-opacity=".85"/>')
        tx = x2 + 6; anc = "start"
        tw = 13.5 * len(note); fill = ""
        if tx + tw > W - 8:
            tx = x1 - 6; anc = "end"
            if tx - tw < 162: tx = x1 + 10; anc = "start"; fill = ' fill="#111" font-weight="700"'
        o.append(f'<text x="{tx:.0f}" y="{y+21}" font-size="13" text-anchor="{anc}"{fill}>{H.escape(note)}</text>')
    o.append("</svg>")
    return f'<div class="era reveal"><div class="in">{"".join(o)}</div></div>'
def book(d):
    p = d["id"]; c = d.get("color", "var(--gold)"); o = []
    o.append(H2(p, d["icon"], d["name"], c))
    o.append(f'<p class="lead" style="font-size:1.08em">{d["lead"]}</p>')
    o.append(H3(p + "-glance", "👁️", "一眼速览"))
    o.append(grid([f'<div class="card reveal" style="--c:{c}"><h4>📌 基本资料</h4>{kv(d["glance"])}</div>',
                   f'<div class="card reveal" style="--c:{c}"><h4>🔑 钥字 · 钥节</h4><p>{d["keys"]}</p>{"".join(V(v) for v in d["kv"])}</div>'], 320))
    o.append(mnem(*d["mnem"]))
    o.append(H3(p + "-why", "❓", "为什么写：前因与目的"))
    o.append(WHY(d["why"], "❓ 写作处境与目的"))
    o.append(H3(p + "-what", "🧭", "写了什么：结构与故事线"))
    o.append(flow(d["outline"]))
    o.append(story(d["story"], c))
    o.append(H3(p + "-time", "⏳", "时间线"))
    o.append(tl(d["timeline"], cols=True))
    if d.get("maps"):
        o.append(H3(p + "-map", "🗺️", "地理位置（地图）"))
        o.append(d.get("mapintro", ""))
        for m in d["maps"]: o.append(MAP(m))
    o.append(H3(p + "-bg", "🏺", "真实历史背景与文化区域特征"))
    o.append(grid(d["bg"], 280))
    if d.get("extra"): o.append(d["extra"])
    o.append(H3(p + "-cov", "🔗", "圣经神学 · 圣约神学"))
    o.append(d["cov"])
    o.append(H3(p + "-xp", "✝️", "指向基督"))
    o.append(d["christ"])
    o.append(H3(p + "-hard", "⚠️", "难点剖析"))
    o.append("".join(HARD(b, "⚠️ 难点：" + t) for t, b in d["hard"]))
    o.append(H3(p + "-conf", "📜", "信条对照（三项联合信条 · 逐字）"))
    o.append(d["conf"])
    o.append(H3(p + "-angles", "🔭", "多角度解读"))
    o.append(grid([card(t, f"<p>{b}</p>", ic, PALC[i % 8]) for i, (ic, t, b) in enumerate(d["angles"])], 250))
    o.append(H3(p + "-apply", "🌱", "如何应用"))
    o.append(APP("<ol>" + "".join(f"<li>{a}</li>" for a in d["apply"]) + "</ol>", "🌱 今日应用（先信神所作，再行神所命）"))
    o.append(H3(p + "-quiz", "✅", "小测验"))
    o.append(quiz(d["quiz"], p + "-q"))
    return "".join(o)
MAP = None
def _story_idx():
    import re as _re
    d = {}
    for l in open("/workspace/cci/text/INDEX.md", encoding="utf-8"):
        p = [x.strip() for x in l.split("|")]
        m = _re.match(r"books_bible-story_2_(\d+)\.txt", p[1]) if len(p) > 4 else None
        if m: d[int(m.group(1))] = (p[2], p[3])
    return d
_SI = None
def reading(nums, title="CCI《圣经故事》第二册 · 延伸阅读"):
    global _SI
    if _SI is None: _SI = _story_idx()
    li = "".join(f'<li><a href="{_SI[n][1]}" target="_blank" rel="noopener">{_SI[n][0]}</a></li>' for n in nums if n in _SI)
    return co("bg", "📚 " + title, f'<p>以下篇章取自 ccifellowship.org 的《圣经故事》（改革宗立场的家庭读本），适合家庭敬拜时配合本页使用：</p><ul class="rd">{li}</ul>')
BOOKN = {"赛": "以赛亚书", "耶": "耶利米书", "哀": "耶利米哀歌", "结": "以西结书", "但": "但以理书", "何": "何西阿书", "珥": "约珥书", "摩": "阿摩司书", "俄": "俄巴底亚书", "拿": "约拿书",
         "弥": "弥迦书", "鸿": "那鸿书", "哈": "哈巴谷书", "番": "西番雅书", "该": "哈该书", "亚": "撒迦利亚书", "玛": "玛拉基书"}
def proofidx():
    """三项联合信条（CCI 版本）脚注经文中显式引用先知书的位置索引。"""
    out = []
    pat = re.compile(r'(赛|耶|哀|结|但|何|珥|摩|俄|拿|弥|鸿|哈|番|该|亚|玛)(\d+:[\d,\-–]+)')
    for ld in _h["lordsdays"]:
        for q in ld["questions"]:
            out.append((f"海德堡 第{q['q']}问", ld.get("url"), " ".join(q.get("refs") or []), ("HC", q["q"])))
    for a in _b["articles"]: out.append((f"比利时 第{a['number']}条", a["url"], " ".join(a.get("refs") or []), ("BC", a["number"])))
    for i, hd in enumerate(_d["heads"]):
        for a in hd["articles"]: out.append((f"多特 {DTN[i+1]}第{a['number']}条", a["url"], " ".join(a.get("refs") or []), ("DT", i + 1, a["number"])))
    res = []
    for lab, url, refs, k in out:
        for m in pat.finditer(refs.replace("：", ":")): res.append((m.group(1), m.group(1) + m.group(2), lab, url))
    return res
_PI = None
def prooftexts(abbrs, title="信条脚注里的本卷经文（索引）"):
    global _PI
    if _PI is None: _PI = proofidx()
    rows = {}
    for ab, ref, lab, url in _PI:
        if ab in abbrs: rows.setdefault((lab, url), []).append(ref)
    if not rows: return ""
    tr = [[f'<a href="{u}" target="_blank" rel="noopener">{l}</a>', ("vr", "、".join(dict.fromkeys(r)))] for (l, u), r in rows.items()]
    return (f'<h4 style="margin-top:18px">🔎 {title}</h4><p class="sm">下列条目在 ccifellowship.org 版本的脚注中引用了本卷经文（自动从抓取数据检索；只列出带有书卷缩写的经文）。点击可读该条全文。</p>' + table(["信条条目", "引用经文"], tr))

# -*- coding: utf-8 -*-
from lib import *
import lib, twelve
ANCH = {"以赛亚书": "isa", "耶利米书": "jer", "耶利米哀歌": "lam", "以西结书": "eze", "但以理书": "dan", "何西阿书": "hos", "约珥书": "joel", "阿摩司书": "amos", "俄巴底亚书": "oba",
        "约拿书": "jonah", "弥迦书": "micah", "那鸿书": "nahum", "哈巴谷书": "hab", "西番雅书": "zeph", "哈该书": "hag", "撒迦利亚书": "zech", "玛拉基书": "mal"}
ICON = {"以赛亚书": "🔥", "耶利米书": "😭", "耶利米哀歌": "🕯️", "以西结书": "🌀", "但以理书": "🦁", "何西阿书": "💍", "约珥书": "🦗", "阿摩司书": "🌊", "俄巴底亚书": "🦅",
        "约拿书": "🐋", "弥迦书": "🌟", "那鸿书": "🏚️", "哈巴谷书": "🗼", "西番雅书": "🎶", "哈该书": "🧱", "撒迦利亚书": "🐴", "玛拉基书": "☀️"}
CANON = ["以赛亚书", "耶利米书", "耶利米哀歌", "以西结书", "但以理书", "何西阿书", "约珥书", "阿摩司书", "俄巴底亚书", "约拿书", "弥迦书", "那鸿书", "哈巴谷书", "西番雅书", "哈该书", "撒迦利亚书", "玛拉基书"]
def card17():
    by = {b[1]: b for b in twelve.ALL}; o = []
    for i, n in enumerate(CANON):
        slug, _, er, (a, b), aud, th, kv, c = by[n]
        yr = f"约{a}" if a == b else (f"约{a}–{b}（不确定）" if er == "不确定" else f"约{a}–{b}")
        tag = "大先知书" if i < 5 else "小先知书"
        o.append(f'<a class="card bk reveal" href="{slug}.html#{ANCH[n]}" style="--c:{c};text-decoration:none;color:inherit;position:relative"><span class="no">{i+1}</span><div class="ic">{ICON[n]}</div><h4>{n}</h4>'
                 f'<p><span class="d">主前 {yr}</span> · <span class="pl">{er}时期</span></p><p>🎯 对象：{aud}</p><p>{th}</p><p style="opacity:.8;font-size:.9em">🔑 {kv} · {tag}</p></a>')
    return '<div class="grid" style="--min:250px">' + "".join(o) + "</div>"
def chapters_chart():
    B = [("赛", 66, "a"), ("耶", 52, "b"), ("哀", 5, "b"), ("结", 48, "b"), ("但", 12, "b"), ("何", 14, "a"), ("珥", 3, "a"), ("摩", 9, "a"), ("俄", 1, "a"),
         ("拿", 4, "a"), ("弥", 7, "a"), ("鸿", 3, "b"), ("哈", 3, "b"), ("番", 3, "b"), ("该", 2, "c"), ("亚", 14, "c"), ("玛", 4, "c")]
    C = {"a": "#ff6b5b", "b": "#ff9f43", "c": "#3ccf8e"}
    W, H0, bw, gap, top = 720, 300, 30, 11, 26
    sc = (H0 - top - 46) / 66
    o = [f'<svg viewBox="0 0 {W} {H0}" role="img" aria-label="十七卷章数柱状图" style="width:100%;height:auto">']
    x0 = 34
    for i, (n, c, g) in enumerate(B):
        x = x0 + i * (bw + gap); h = c * sc; y = H0 - 40 - h
        o.append(f'<rect x="{x}" y="{y:.1f}" width="{bw}" height="{h:.1f}" rx="5" style="fill:{C[g]}"><title>{n} {c} 章</title></rect>')
        o.append(f'<text x="{x+bw/2}" y="{y-6:.1f}" text-anchor="middle" font-size="13" font-weight="800" style="fill:var(--hd)">{c}</text>')
        o.append(f'<text x="{x+bw/2}" y="{H0-20}" text-anchor="middle" font-size="15" font-weight="700" style="fill:var(--ink)">{n}</text>')
    xs = x0 + 5 * (bw + gap) - gap / 2
    o.append(f'<line x1="{xs}" y1="{top}" x2="{xs}" y2="{H0-36}" style="stroke:var(--mut)" stroke-dasharray="4 4"/>')
    o.append(f'<text x="{x0}" y="16" font-size="13" style="fill:var(--mut)">五卷大先知书 183 章</text><text x="{xs+8}" y="16" font-size="13" style="fill:var(--mut)">十二小先知书 67 章</text>')
    o.append("</svg>")
    leg = "".join(f'<span class="chip" style="border-color:{C[k]}"><i style="display:inline-block;width:10px;height:10px;border-radius:3px;background:{C[k]};margin-right:6px"></i>{t}</span>' for k, t in (("a", "亚述时期"), ("b", "巴比伦时期"), ("c", "波斯时期")))
    return (f'<div class="era reveal"><div class="in">{"".join(o)}</div></div><div class="chips">{leg}</div>'
            + MEM('<p><span class="mm">66 · 52 · 48</span>：以赛亚、耶利米、以西结三卷就占 166 章（≈ 三分之二）；<b class="k">最长的以赛亚 66 章 ≈ 圣经 66 卷</b>；最短的俄巴底亚只有 1 章 21 节。</p>'))
def body():
    o = []
    o.append(f'''<section class="hero reveal"><div class="kick">THE PROPHETS · CONTINENTAL REFORMED · GROKstudy {lib.VER}</div>
<h1>🔥 先知书深读<br><small style="font-size:.5em;opacity:.85">以赛亚书 → 玛拉基书 · 大先知书5卷 + 十二小先知书 · 欧陆改革宗正统视角</small></h1>
<p class="lead">十七卷书、约四百年（主前约800–430年）、三个帝国（<span class="pl">亚述</span> → <span class="pl">巴比伦</span> → <span class="pl">波斯</span>）、一个信息：<b class="k">守约的神</b>差遣祂的仆人众先知，控诉背约的百姓，宣告审判，又应许一个<b class="k">新约</b>、一位<b class="k">受苦的仆人</b>、一位<b class="k">大卫的苗裔</b>、一位驾云而来的<b class="k">人子</b>——<b class="xr">耶稣基督</b>。“众先知都为他作见证”（徒10:43）。</p>
<div class="chips"><span class="chip">📖 先整体后细节</span><span class="chip">🔗 圣约神学 · 圣经神学</span><span class="chip">🗺️ 9 幅三视图地图（讲解图 · 地形图 · 实时多源）</span><span class="chip">🎬 21 段中文视频导览</span><span class="chip">🖍️ 笔记标记 · 遮盖背诵</span><span class="chip">📜 三项联合信条逐字引用</span><span class="chip">✨ 三大信经背诵版与深度对比</span><span class="chip">🧠 口诀 · 卡片 · 测验</span></div></section>''')
    o.append(H2("start", "🧭", "怎样使用本站", "var(--gold)"))
    o.append(flow([("① 整本圣经", "先知书在正典与救赎历史中的位置", "var(--gold)"), ("② 史地文化", "亚述、巴比伦、波斯；列王与先知", "var(--green)"), ("③ 逐卷深读", "17卷：为什么写、写了什么、如何应用", "var(--red)")]))
    o.append(flow([("④ 信条对照", "三项联合信条 × 先知书十大主题", "var(--teal)"), ("⑤ 三大信经", "背诵版、深度对比、为什么需要三个", "var(--purple)"), ("⑥ 速记自测", "口诀、翻卡、测验、读经计划", "var(--blue)")]))
    o.append(H2("v3new", "🆕", "v3 新增（2026-11-14）", "var(--pink)"))
    o.append(grid([card("📑 三级目录", '<p>全站统一 <b class="k">1 / 1.1 / 1.1.1</b> 编号；每级可折叠，可一键展开到一级/二级/三级；<b class="k">拖动目录右边缘可左右拉宽</b>（鼠标、触屏都可），宽度自动记住；手机抽屉同样可拉宽；另有“全站 16 页”分组导航。</p>', "", "var(--blue)"),
                   card("⚡ 更顺滑", '<p>移除最后的毛玻璃顶栏、漂浮动画层与滚动渐显；进度条改为 CSS 滚动驱动（零 JS）；滚动高亮只用 IntersectionObserver；非首屏交互延后到空闲时初始化。</p>', "", "var(--teal)"),
                   card("🗺️ 11 幅地图", '<p>新增 <b class="k">列国神谕图</b>（古实到以拦，赛13–23 / 耶46–51 / 结25–32 / 摩1–2）与 <b class="k">下埃及图</b>（耶40–46）。每幅仍是讲解图＋地形图＋12 源实时地图。<a href="atlas.html">打开地图集 →</a></p>', "", "var(--gold)"),
                   card("🧠 背诵升级", '<p>每卷新增 <b class="k">一页背诵卡</b>；速记页新增 <span class="box">十二个关键术语</span>；标记新增 <span class="box">框＝术语</span>、<span class="ul-r">红实线＝审判/警告</span>、<span class="ul-b">蓝双线＝应许</span>。</p>', "", "var(--pink)")], 240))
    o.append(KEY('<p><b>v2 回顾</b>：地图三视图、本质一句话＋三根柱子、历史深挖、古近东文化、笔记标记系统、BibleProject 中文视频——全部保留。</p>'))
    o.append(H3("v2vid", "🎬", "先看两段总览视频（BibleProject 中文）"))
    o.append(lib.vids("prophets") + lib.vids("ot", False))
    o.append(H2("books", "📚", "十七卷先知书一览（按正典顺序）", "var(--red)"))
    o.append(card17())
    o.append(mnem("赛耶哀结但 · 何珥摩俄拿弥 · 鸿哈番 · 该亚玛", "五卷大先知书 + 十二小先知书（中文和合本顺序）；“大/小”指篇幅，不指重要性"))
    o.append(mnem("亚述六（何珥摩俄拿弥）· 巴比伦三（鸿哈番）· 波斯三（该亚玛）", "十二小先知书按帝国分组（约珥、俄巴底亚的年代有争议，按正典顺序归组）"))
    o.append(H3("books-chart", "📊", "篇幅一图：十七卷共 250 章"))
    o.append(chapters_chart())
    o.append(H2("arc", "🌈", "四百年的故事线", "var(--purple)"))
    rows = sorted(twelve.ALL, key=lambda b: -b[3][0])
    o.append(era([(b[1], -b[3][0], -b[3][1] if b[3][1] != b[3][0] else -b[3][1] + 4, b[7], ("年代不确定" if b[2] == "不确定" else b[2])) for b in rows], -850, -400, title="十七卷先知书事工年代（约）"))
    o.append(story([("🦁", "亚述的威胁（约760–700）", "北国繁荣却腐败：阿摩司、何西阿呼吁悔改；约拿被差往尼尼微。722年撒玛利亚陷落。以赛亚、弥迦在犹大宣告以马内利与伯利恒的统治者。"),
                    ("⚖️", "亚述衰亡（约660–612）", "那鸿宣告尼尼微必倾覆（612年应验）；西番雅在约西亚改革前夕宣告“耶和华的大日”。"),
                    ("🔥", "巴比伦与圣殿被焚（605–586）", "哈巴谷问“为什么”；耶利米流泪宣告七十年与新约；以西结在被掳之地看见荣耀离开；耶利米哀歌哀悼废墟。"),
                    ("🏛️", "被掳之中（586–539）", "但以理在巴比伦宫廷见证“至高者掌权”；以西结看见枯骨复活与新殿。"),
                    ("🧱", "归回与重建（538–430）", "古列下诏；哈该、撒迦利亚激励建殿（516年完工）；玛拉基责备冷淡，应许以利亚与立约的使者——然后是四百年的沉默，直到施洗约翰。")]))
    o.append(table(["阶段", "核心问题", "神的作为", "指向基督"], [
        ["亚述时期", "神的百姓背约，神还会守约吗？", "差遣先知控诉；用亚述作“怒气的棍”；保留余民", "以马内利（赛7:14）；伯利恒的统治者（弥5:2）"],
        ["巴比伦时期", "圣殿被焚，应许落空了吗？", "照约审判；应许新约与新心", "新约的中保（耶31；来8）；大卫的苗裔（耶23:5）"],
        ["被掳之中", "外邦帝国是历史的主人吗？", "“至高者在人的国中掌权”", "驾云而来的人子（但7:13）"],
        ["归回时期", "小小的余民有将来吗？", "激动古列；兴起建殿", "骑驴的王（亚9:9）；立约的使者（玛3:1）"]]))
    o.append(H2("why", "💎", "为什么要读先知书？", "var(--teal)"))
    o.append(grid([card("它是神的话", "<p>“先知的预言从来没有出于人意的，乃是人被圣灵感动说出神的话来”（彼后1:21）。先知的口头禅是“<b class=k>耶和华如此说</b>”。</p>", "🗣️", "var(--gold)"),
                   card("它是约的法庭", "<p>先知不是“算命的”，而是<b class=k>约的使者</b>：按着摩西之约的祝福与咒诅，控诉、警告、呼召回转（申28–30）。</p>", "⚖️", "var(--red)"),
                   card("它满了福音", "<p>“这救恩……众先知早已详细地寻求考察”（彼前1:10-11）。受苦的仆人（赛53）、新约（耶31）、新心（结36）、圣灵浇灌（珥2）。</p>", "🕊️", "var(--green)"),
                   card("它是为我们写的", "<p>同样的罪（偶像、不义、敷衍的敬拜）今天仍在；同样的神仍然说：“你们要归向我，我就归向你们”（亚1:3）。</p>", "🪞", "var(--blue)"),
                   card("它指向基督", "<p>“从摩西和众先知起，凡经上所指着自己的话，都给他们讲解明白了”（路24:27）。</p>", "✝️", "var(--pink)")], 230))
    o.append(V("彼前1:10-11"))
    o.append(KEY('<p><b>阅读原则（改革宗）：</b>① 唯独圣经（BC 7）——经文本身是最高权威；② 以经解经——用新约对先知书的引用作钥匙；③ 救赎历史——先问“当时对以色列是什么意思”，再问“在基督里怎样成就”；④ 圣约框架——审判与应许都从神与亚伯拉罕、摩西、大卫所立的约而来；⑤ 不臆测——预言的目的是使人悔改与安慰，不是制作末日时刻表。</p>'))
    o.append(cq("BC", 7, part="我们相信，圣经中包含了神全部的旨意；我们也相信它对人得救所必须信的一切真理作了充分的教导。"))
    return "".join(o)

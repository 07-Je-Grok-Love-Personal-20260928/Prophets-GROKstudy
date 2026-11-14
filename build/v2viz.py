# -*- coding: utf-8 -*-
"""v2 可视化：帝国更替动态图、条约 vs 圣约诉讼结构图、被掳时期三个世界、先知时空矩阵。纯内联 SVG/HTML，离线可用。"""
import html as H
from twelve import ALL
def emp_anim():
    y0, y1, W = -900, 0, 1200; L0 = 150
    X = lambda y: L0 + (y - y0) / (y1 - y0) * (W - L0 - 20)
    rows = [("🦁 亚述", -911, -609, "#ff6b6b", "新亚述帝国 911–609"), ("🏰 新巴比伦", -626, -539, "#ffa94d", "626–539"), ("👑 波斯", -550, -330, "#34d399", "550–330"),
            ("🐐 希腊", -334, -63, "#60a5fa", "亚历山大 → 托勒密 / 塞琉古"), ("🦅 罗马", -63, 0, "#b197fc", "63 庞培 →"),
            ("北国以色列", -930, -722, "#c084fc", "930–722"), ("南国犹大", -930, -586, "#ffc94d", "930–586"), ("被掳", -586, -538, "#94a3b8", "586–538"), ("归回 · 第二圣殿", -538, 0, "#2dd4bf", "538 → 第二圣殿时期 → 基督降生")]
    # 先排先知泳道
    lanes, P = [], []
    for slug, name, era, (a, b), to, theme, key, col in sorted(ALL, key=lambda r: -r[3][0]):
        if name == "约珥书": continue
        nm = name[:-1] if name.endswith("书") else name
        x1, x2 = X(-a), X(-b)
        lane = next((k for k, end in enumerate(lanes) if end < x1 - 6), None)
        if lane is None: lanes.append(0); lane = len(lanes) - 1
        lanes[lane] = x2 + 14 + 14 * len(nm)
        P.append((lane, x1, x2, nm, col))
    rh = 34; top = 26; py = top + rh * len(rows) + 16; Hh = py + len(lanes) * 24 + 44
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="帝国更替与先知分布动态图（主前900–100）">']
    for yy in range(y0, y1 + 1, 100):
        x = X(yy); o.append(f'<line x1="{x:.0f}" y1="{top - 8}" x2="{x:.0f}" y2="{Hh - 30}" stroke="currentColor" stroke-opacity=".12"/><text x="{x:.0f}" y="{Hh - 10}" text-anchor="{"middle" if yy else "end"}" font-size="13" opacity=".7">{"主前" + str(-yy) if yy else "基督降生"}</text>')
    for i, (lab, a, b, c, note) in enumerate(rows):
        y = top + i * rh; x1, x2 = X(max(a, y0)), X(min(b, y1))
        if i == 5: o.append(f'<line x1="10" y1="{y - 4}" x2="{W - 10}" y2="{y - 4}" stroke="currentColor" stroke-opacity=".25" stroke-dasharray="4 6"/>')
        o.append(f'<text x="{L0 - 10}" y="{y + 21}" text-anchor="end" font-size="15" font-weight="800">{lab}</text>')
        o.append(f'<rect class="seg" style="animation-delay:{i * .12:.2f}s" x="{x1:.0f}" y="{y + 5}" width="{max(6, x2 - x1):.0f}" height="{rh - 10}" rx="8" fill="{c}" fill-opacity=".88"/>')
        if x2 - x1 > 13 * len(note) + 16: o.append(f'<text x="{x1 + 8:.0f}" y="{y + 22}" font-size="13" font-weight="700" style="fill:#111">{H.escape(note)}</text>')
        elif x2 + 8 + 13 * len(note) < W: o.append(f'<text x="{x2 + 6:.0f}" y="{y + 22}" font-size="13" font-weight="700">{H.escape(note)}</text>')
        else: o.append(f'<text x="{x1 - 6:.0f}" y="{y + 22}" text-anchor="end" font-size="13" font-weight="700">{H.escape(note)}</text>')
    o.append(f'<text x="{L0 - 10}" y="{py + 16}" text-anchor="end" font-size="15" font-weight="800">📜 十七位先知</text>')
    for lane, x1, x2, nm, col in P:
        y = py + lane * 24
        o.append(f'<rect class="seg" x="{x1:.0f}" y="{y}" width="{max(8, x2 - x1):.0f}" height="14" rx="7" fill="{col}"/><text x="{x2 + 6:.0f}" y="{y + 12}" font-size="13" font-weight="700">{nm}</text>')
    o.append(f'<g class="now" style="--sw:{W - L0 - 20}px"><line x1="{L0}" y1="{top - 10}" x2="{L0}" y2="{Hh - 30}" stroke="#ff7eb6" stroke-width="2.5" stroke-dasharray="6 5"/><circle cx="{L0}" cy="{top - 10}" r="6" fill="#ff7eb6"/></g>')
    o.append('</svg>')
    return f'<div class="emp reveal">{"".join(o)}</div><p class="sm">粉色虚线自动扫过时间轴：看帝国怎样一个接一个兴起又倒下（但2:21“祂改变时候、日期，废王、立王”）。约珥书年代未定，未画入。</p>'
def treaty():
    rows = [["① 序言：宗主自称", "“我是亚述大王……”", "“我是耶和华你的神”（出20:2）", "“耶和华如此说”"],
            ["② 历史序言：过去的恩惠", "宗主列举对附庸的恩典", "“曾将你从埃及地为奴之家领出来”", "何11:1；摩2:9-10；弥6:4"],
            ["③ 条款：专一效忠", "不可另投他国", "十诫：除我以外不可有别的神", "控诉拜偶像、倚靠埃及/亚述"],
            ["④ 存放与宣读", "条约存于神庙，定期宣读", "法版放约柜（申31:26）", "约西亚宣读律法书（王下23:2）"],
            ["⑤ 见证", "双方诸神为证", "“我今日呼天唤地作见证”（申30:19）", "“诸山哪，要听耶和华争辩的话”（弥6:2）"],
            ["⑥ 祝福与咒诅", "背约者天如铜、地如铁", "申28 祝福与咒诅", "刀剑、饥荒、瘟疫、被掳（耶14:12）"]]
    head = ["结构", "古近东宗主条约（如以撒哈顿继位条约，主前672）", "西乃之约（申命记）", "先知的“约的诉讼”（rîb）"]
    th = "".join(f"<th>{x}</th>" for x in head); tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw reveal"><table class="cmp"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
def worlds():
    W = [("🏚️ 留在犹大的人", "var(--orange)", "穷苦人被留下修理葡萄园（王下25:12）；省长基大利驻米斯巴，被以实玛利刺杀（耶40–41）。圣殿废墟上仍有人献素祭（耶41:5）。", "耶利米哀歌、耶40–42"),
         ("🏙️ 在巴比伦的人", "var(--purple)", "聚居迦巴鲁河畔（提勒亚毕）、“犹大城”（Al-Yahudu 泥版）；可置业、经商、保有长老制度（结8:1）。会堂、安息日、割礼与圣经抄写成为认同的核心。", "以西结、但以理、诗137"),
         ("🔺 逃到埃及的人", "var(--blue)", "违背耶利米的劝告下埃及，住答比匿、挪弗、巴特罗；向“天后”烧香（耶44）。后来象岛有犹太军事殖民地与自建圣殿（象岛蒲草纸）。", "耶43–44")]
    return '<div class="ane">' + "".join(f'<div class="reveal" style="--c:{c}"><h5>{t}</h5><p>{b}</p><p class="sm">📖 {r}</p></div>' for t, c, b, r in W) + '</div>'
def matrix():
    """先知时空矩阵：横轴时间、纵轴听众（北国 / 南国 / 外邦 / 被掳 / 归回）。"""
    W, Hh = 1200, 420; y0, y1 = -850, -420; L0 = 140
    X = lambda y: L0 + (y - y0) / (y1 - y0) * (W - L0 - 30)
    lanes = [("北国以色列", "#c084fc"), ("南国犹大", "#ffc94d"), ("外邦城邦", "#ff6b6b"), ("被掳者", "#94a3b8"), ("归回者", "#2dd4bf")]
    who = {"何西阿书": 0, "阿摩司书": 0, "以赛亚书": 1, "弥迦书": 1, "西番雅书": 1, "哈巴谷书": 1, "耶利米书": 1, "耶利米哀歌": 1, "约拿书": 2, "那鸿书": 2, "俄巴底亚书": 2,
           "以西结书": 3, "但以理书": 3, "哈该书": 4, "撒迦利亚书": 4, "玛拉基书": 4}
    lh = (Hh - 60) / len(lanes)
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="先知时空矩阵">']
    for i, (n, c) in enumerate(lanes):
        y = 20 + i * lh; o.append(f'<rect x="{L0}" y="{y:.0f}" width="{W - L0 - 30}" height="{lh - 6:.0f}" rx="12" fill="{c}" fill-opacity=".1"/><text x="{L0 - 10}" y="{y + lh / 2 + 4:.0f}" text-anchor="end" font-size="15" font-weight="800" style="fill:{c}">{n}</text>')
    for yy in range(-850, -419, 50):
        x = X(yy); o.append(f'<text x="{x:.0f}" y="{Hh - 12}" text-anchor="middle" font-size="12" opacity=".7">{-yy}</text>')
    for ev, yy, c in ((" 722 北国亡", -722, "#c084fc"), (" 586 圣殿焚", -586, "#ff6b6b"), (" 538 归回", -538, "#2dd4bf")):
        x = X(yy); o.append(f'<line x1="{x:.0f}" y1="14" x2="{x:.0f}" y2="{Hh - 30}" stroke="{c}" stroke-width="2" stroke-dasharray="5 5"/><text x="{x + 3:.0f}" y="14" font-size="12.5" font-weight="800" style="fill:{c}">{ev}</text>')
    pts = {}
    for slug, name, era, (a, b), to, theme, key, col in ALL:
        if name not in who: continue
        pts.setdefault(who[name], []).append((X((-a - b) / 2), name.replace("书", ""), col))
    for ln, arr in pts.items():
        ends = []
        for x, nm, col in sorted(arr):
            sub = next((k for k, e in enumerate(ends) if e < x - 12), None)
            if sub is None: ends.append(0); sub = len(ends) - 1
            ends[sub] = x + 18 + 14 * len(nm)
            y = 20 + ln * lh + 18 + sub * 22
            o.append(f'<g class="pulse" style="animation-delay:{(sub + ln) % 5 * .35:.2f}s"><circle cx="{x:.0f}" cy="{y:.0f}" r="8" fill="{col}" stroke="#fff" stroke-width="2"/></g><text x="{x + 13:.0f}" y="{y + 5:.0f}" font-size="13.5" font-weight="800">{nm}</text>')
    o.append('</svg>')
    return f'<figure class="scene reveal">{"".join(o)}<figcaption>先知时空矩阵：圆点＝事奉中点（约），行＝主要听众。三条虚线是先知书的三个转折：北国灭亡、圣殿被焚、归回重建。约珥书年代未定，未画入。</figcaption></figure>'

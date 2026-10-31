# -*- coding: utf-8 -*-
import json, re, html as H
from lib import *
import lib
CR = json.load(open(lib.CCI + "/creeds.json"))
def _intro(k): 
    t = CR[k].get("intro_text"); return t[0] if isinstance(t, list) else t
def cpq(k, part, note=""):
    """三大信经 CCI 介绍文字逐字引用"""
    t = _intro(k); assert part in t, (k, part)
    lib.USED.append(dict(key="CR-intro." + k, doc="CR", n=k, parts=[part], url=CR[k]["url"], label=CR[k]["title"] + " · 简介"))
    pre = "" if t.startswith(part) else "……"; post = "" if t.endswith(part) else "……"
    return (f'<blockquote class="cq reveal" data-k="CR-intro.{k}"><div class="cq-h">📜 {CR[k]["title"]} · CCI 简介 <span class="badge">CCI 逐字</span></div>'
            f'<div class="cq-t">{pre}{H.escape(part)}{post}</div><cite>出处：<a href="{CR[k]["url"]}" target="_blank" rel="noopener">{CR[k]["url"].replace("https://","")}</a>{note}</cite></blockquote>')
def lines(k, p):
    if k == "athanasian": return [x for x in re.split(r"(?<!\d)(?=\d+\) )", p) if x]
    return [x for x in re.split(r"(?<=[；。])(?=.)(?!阿们)", p) if x]
LAB = {"apostles": {0: "🅰️ 论圣父与我们的受造", 1: "🅱️ 论圣子与我们的得赎", 2: "🅲 论圣灵与我们的成圣"},
       "nicene": {0: "🅰️ 圣父", 1: "🅱️ 圣子：永恒的神性", 2: "🅱️ 圣子：道成肉身与救赎", 3: "🅲 圣灵", 4: "⛪ 教会 · 洗礼 · 盼望"},
       "athanasian": {0: "🚪 引言（1–2）", 1: "🔺 第一部分：三位一体（3–28）", 7: "✝️ 第二部分：道成肉身（29–41）", 12: "🔚 结语（42）"}}
def creed(k):
    t = CR[k]["text"]; ps = t.split("\n\n"); o = []; n = 0
    for i, p in enumerate(ps):
        if i in LAB[k]: o.append(f'<span class="art">{LAB[k][i]}</span>')
        ls = lines(k, p); assert "".join(ls) == p
        sp = []
        for l in ls:
            n += 1
            dn = f' data-n="{n}"' if k != "athanasian" else ""
            sp.append(f'<span class="ln"{dn}>{H.escape(l)}</span>')
        o.append(f'<div class="cp">{"".join(sp)}</div>')
    return (f'<div class="tools reveal"><button class="ib" data-recite="cr-{k}">🙈 背诵模式（遮盖）</button><button class="ib" data-big="cr-{k}" data-d="+">A＋</button><button class="ib" data-big="cr-{k}" data-d="-">A－</button>'
            f'<a class="ib" href="{CR[k]["url"]}" target="_blank" rel="noopener">🔗 CCI 原文</a></div><div class="creed" id="cr-{k}" data-creed="{k}">{"".join(o)}</div>')
def body():
    o = []
    o.append('''<section class="hero reveal"><div class="kick">THE THREE ECUMENICAL CREEDS · RECITATION EDITION</div><h1>✨ 三大普世信经 · 阅读背诵版</h1>
<p class="lead">《使徒信经》《尼西亚信经》《亚他那修信经》全文<b class="k">逐字</b>取自 ccifellowship.org《赞美诗集》信经部分，并由程序验证与原文完全一致。点击 <b>🙈 背诵模式</b> 遮盖全文，再逐行点击揭开自测；<b>A＋/A－</b> 调整字号。</p>
<div class="chips"><span class="chip">🅰️ 使徒信经 · 12 条</span><span class="chip">🅱️ 尼西亚信经 · 325/381</span><span class="chip">🅲 亚他那修信经 · 42 点</span></div></section>''')
    o.append(H2("cr-how", "🧠", "背诵方法", "var(--gold)"))
    o.append(story([("📖", "1 读", "先整段朗读 3 遍，注意分段标题（父—子—灵）"), ("🙈", "2 遮", "打开背诵模式，按行回忆，想不起来再点开"), ("🔗", "3 链", "用“三位一体骨架”串起：父造—子救—灵圣—教会—盼望"), ("⛪", "4 用", "在主日崇拜中与会众一同宣认；把条文与先知书经文挂钩")]))
    o.append(MEM('<p>三大信经都按<b class="k">三位一体</b>排列（海德堡第24问）：父（创造）→ 子（救赎）→ 灵（成圣）。背诵时先记这副骨架，再往里填细节。</p>'))
    o.append(cq("HC", 24))
    o.append(H2("cr-apostles", "🅰️", "使徒信经", "var(--gold)"))
    o.append(cpq("apostles", "这一信经被称为《使徒信经》，并不是因为它是使徒写的，而是因为它是对使徒教导所作的总结。"))
    o.append(creed("apostles"))
    o.append(mnem("父造 · 子降—难—死—活—升—坐—来 · 灵 · 会 · 赦 · 复 · 永", "使徒信经 12 条速记"))
    o.append(H2("cr-nicene", "🅱️", "尼西亚信经", "var(--blue)"))
    o.append(cpq("nicene", "《尼西亚信经》又称《尼西亚-君士坦丁堡信经》，它是早期基督教会的正统信仰告白，旨在驳斥某些异端，尤其是亚流主义。"))
    o.append(creed("nicene"))
    o.append(mnem("出于神且是神 · 出于光且是光 · 出于真神且是真神 · 受生却非被造 · 与父同质", "尼西亚核心五句——专门对付亚流“子是受造者”"))
    o.append(H2("cr-athanasian", "🅲", "亚他那修信经", "var(--purple)"))
    o.append(cpq("athanasian", "撇开信经的开头和结尾，《亚他那修信经》可以分为两个部分："))
    o.append(creed("athanasian"))
    o.append(mnem("位格不紊 · 本质不分 ‖ 神性不变 · 二性不混", "亚他那修信经两大支柱：前半防撒伯流/三神论，后半防基督论异端"))
    o.append(H2("cr-hist", "🔗", "信经条文 × 先知书", "var(--teal)"))
    o.append(table(["信经条文", "先知书中的根据与伏笔", "说明"], [
        ["“我信神，全能的父，创造天地的主”", "赛40:12-28；44:24；耶10:12；摩4:13", "先知们用“创造主”对抗偶像：“我是耶和华，是创造万物的”（赛44:24，海德堡第26问脚注）"],
        ["“因圣灵感孕，从童贞女马利亚所生”", "赛7:14；弥5:2", "以马内利的兆头与伯利恒的统治者（比利时信条第17–18条脚注）"],
        ["“在本丢·彼拉多手下受难，被钉于十字架”", "赛53；亚12:10；13:7", "“他为我们的过犯受害”；“仰望我，就是他们所扎的”；“击打牧人”"],
        ["“第三天从死人中复活”", "拿1:17（太12:40）；何6:2；赛53:10-11", "约拿的神迹；“他必看见后裔”"],
        ["“将来必从那里降临，审判活人死人”", "但7:9-14；玛3:1-3；珥2:31", "人子驾云而来；立约的使者如炼金之人的火"],
        ["“他的国没有穷尽”（尼西亚）", "但2:44；7:14；赛9:7", "“天上的神必另立一国，永不败坏”"],
        ["“他曾藉众先知说话”（尼西亚）", "亚7:12；彼后1:21", "“万军之耶和华用灵藉从前的先知所说的话”——信经直接为先知书作见证"],
        ["“我信圣灵”", "珥2:28；结36:27；亚4:6", "圣灵浇灌、内住、成事"],
        ["“罪得赦免”", "弥7:18-19；耶31:34；赛43:25", "“我必赦免他们的罪孽，不再记念他们的罪恶”"],
        ["“身体复活 · 永生”", "但12:2；赛25:8；26:19；结37", "旧约最清楚的复活经文在先知书（比利时信条第37条脚注引用但12:2）"]]))
    return "".join(o)

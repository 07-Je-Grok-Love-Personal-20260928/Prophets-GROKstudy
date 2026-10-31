# -*- coding: utf-8 -*-
from lib import *
import lib
def body():
    o = []
    o.append('''<section class="hero reveal"><div class="kick">SOURCES · VERIFICATION · VERSION</div><h1>🔖 来源与核对</h1>
<p class="lead">本站所有信条与信经引文均取自 <b class="k">ccifellowship.org</b>（华人改革宗团契 · 加拿大归正教会《赞美诗集》中文版），经文取自<b class="k">和合本</b>；每条引文在构建与发布前由程序逐字比对。</p></section>''')
    o.append(H2("src-cci", "📜", "信条与信经原文来源", "var(--gold)"))
    o.append(table(["文献", "网址", "本站用法"], [
        ["比利时信条（37条）", '<a href="https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession" target="_blank" rel="noopener">ccifellowship.org/…/the-belgic-confession</a>', "逐字引用（整条或连续片段）"],
        ["海德堡要理问答（129问）", '<a href="https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism" target="_blank" rel="noopener">ccifellowship.org/…/heidelberg-catechism</a>', "逐字引用问与答"],
        ["多特信经", '<a href="https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort" target="_blank" rel="noopener">ccifellowship.org/…/canons-of-dort</a>', "逐字引用"],
        ["使徒信经", '<a href="https://ccifellowship.org/books/book-of-praise/creeds/apostles-creed" target="_blank" rel="noopener">ccifellowship.org/…/apostles-creed</a>', "全文 + 简介逐字"],
        ["尼西亚信经", '<a href="https://ccifellowship.org/books/book-of-praise/creeds/nicene-creed" target="_blank" rel="noopener">ccifellowship.org/…/nicene-creed</a>', "全文 + 简介逐字"],
        ["亚他那修信经", '<a href="https://ccifellowship.org/books/book-of-praise/creeds/athanasian-creed" target="_blank" rel="noopener">ccifellowship.org/…/athanasian-creed</a>', "全文 + 简介逐字"],
        ["《圣经故事》第二册（CCI）", '<a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>', "各卷“延伸阅读”章节链接"],
        ["CCI 讲道文本", '<a href="https://ccifellowship.org/sermons" target="_blank" rel="noopener">ccifellowship.org/sermons</a>', "相关讲道链接（阿摩司书、约拿书）"]]))
    o.append(KEY('<p>引文处理规则：① 只省略原网页的<b>脚注上标编号</b>；② 片段引用时，在省略处加“……”；③ 不改字、不改标点，连原文中的特殊空格也保留；④ 威斯敏斯特标准只作转述，不作引号引用。</p>', "⭐ 逐字规则"))
    o.append(H2("src-verify", "🧪", "怎样核对", "var(--green)"))
    o.append(flow([("① 抓取", "CCI 网页 → JSON（比利时 37 · 海德堡 129 · 多特 · 三信经）", "var(--gold)"), ("② 构建断言", "每个引文片段 assert 必须是原文子串，否则构建失败", "var(--red)"), ("③ 发布后核验", "tools/verify_quotes.py 解析成品 HTML，逐条再比对", "var(--green)"), ("④ 信经全文", "背诵版逐行拼接 == 原文（逐字相等）", "var(--blue)")]))
    n = len({u["key"] for u in lib.USED})
    o.append(f'<p>本次构建共登记引文 <b class="k">{len(lib.USED)}</b> 处（不同条目 {n} 个）——见仓库 <code>build/data/quotes_used.json</code> 与 <code>build/data/verify_report.json</code>。</p>')
    o.append(H2("src-bible", "📖", "圣经与史地资料", "var(--blue)"))
    o.append(table(["类别", "来源", "说明"], [
        ["经文", "《和合本》（CUS，getbible 数据）", "经文引用由程序按章节取出，未改字"],
        ["年代", "列王年代采用 Thiele 体系；亚述名年官表（主前763年日蚀）、巴比伦编年史、波斯王表为外部锚点", "约数以“约”标示；不同学者±1–10年"],
        ["地图", "Natural Earth 公共领域地理数据，本站自绘", "古地名位置为近似，供学习之用"],
        ["考古与古近东", "撒珥根二世铭文、泰勒棱柱（西拿基立）、拉吉浮雕与拉吉书信、巴比伦编年史、约雅斤配给泥版、拿波尼度圆柱、居鲁士圆柱、贝希斯敦铭文、象岛蒲草纸、死海古卷以赛亚大卷（1QIsaᵃ）", "作为佐证，不作信仰根基"]]))
    o.append(H2("src-ref", "🌐", "参考的改革宗网站", "var(--purple)"))
    o.append(grid([card(t, f'<p><a href="{u}" target="_blank" rel="noopener">{u.replace("https://","")}</a></p><p class="mut">{d}</p>', ic, c) for t, u, ic, d, c in [
        ("CCI 华人改革宗团契", "https://ccifellowship.org", "📜", "信条、信经、圣经故事、讲道（本站唯一逐字来源）", "var(--gold)"),
        ("加拿大归正教会 CanRC", "https://canrc.org", "🇨🇦", "《赞美诗集》与三项联合信条", "var(--red)"),
        ("北美联合归正教会 URCNA", "https://www.urcna.org", "⛪", "三项联合信条与教会秩序", "var(--blue)"),
        ("Heritage Reformed", "https://heritagereformed.com", "🏛️", "欧陆改革宗传统", "var(--green)"),
        ("PRCA", "https://prca.org", "📘", "改革宗信条与圣约神学", "var(--purple)"),
        ("OPC 正统长老会", "https://www.opc.org", "🌐", "威斯敏斯特标准（仅转述）", "var(--teal)"),
        ("改革宗入门 reformedbeginner", "https://www.reformedbeginner.net", "🌱", "中文改革宗入门资料", "var(--pink)"),
        ("ccreformed", "https://www.ccreformed.org", "📗", "中文改革宗资源", "var(--gold)"),
        ("加拿大归正神学院 CRTS", "https://canadianreformedseminary.ca", "🎓", "加拿大归正教会神学院（旧约与先知书课程资源）", "var(--blue)"),
        ("CRTS（crts.edu）", "https://crts.edu", "🎓", "加拿大归正神学院官方网站（crts.edu）", "var(--green)"),
        ("威斯敏斯特神学院 WTS", "https://www.wts.edu", "📚", "改革宗圣经神学与旧约研究（威斯敏斯特标准仅转述）", "var(--purple)")]], 250))
    o.append(H2("src-ver", "🗂️", "版本记录", "var(--teal)"))
    o.append(table(["版本", "日期（台北时间）", "说明"], [
        [("g", "v1.0（20261031-v1）"), "2026-10-31", "首次发布：15 页；整本圣经视角、三大帝国史地文化、十七卷先知书逐卷深读、6 幅地图、三项联合信条对照与深度比较、信条脚注先知书经文索引、三大信经背诵版与深度对比、速记自测、来源核对"]]))
    o.append(BG('<p>本站为学习辅助材料，不能取代教会的讲道、教导与牧养。若发现错误，请在 GitHub 仓库提交 Issue。</p>', "📝 说明"))
    return "".join(o)

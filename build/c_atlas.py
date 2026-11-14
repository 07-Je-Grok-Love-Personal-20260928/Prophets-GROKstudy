# -*- coding: utf-8 -*-
from lib import *
import lib
from v2viz import emp_anim, matrix
GROUPS = [("atl-land", "🏞️", "一、应许之地：先知的家乡、列国包围圈与锡安", "var(--gold)", ["land", "amos", "jerusalem"],
           '<p>以色列地南北约 250 公里，却夹在<span class="pl">埃及</span>与<span class="pl">两河流域</span>之间的“陆桥”上——这是她蒙福之地，也是兵家必争之地。先知们的家乡多在乡村（<span class="pl">提哥亚</span>、<span class="pl">摩利沙</span>、<span class="pl">亚拿突</span>），信息却直指首都与圣殿。</p>'),
          ("atl-assyria", "🦁", "二、亚述时期：约拿、以赛亚、弥迦、那鸿", "var(--red)", ["jonah", "assyria"],
           '<p>亚述从<span class="pl">尼尼微</span>出发，沿肥沃月湾向西推进：<span class="d">732</span> 大马士革 → <span class="d">722</span> 撒玛利亚 → <span class="d">701</span> 耶路撒冷（不破）。</p>'),
          ("atl-babylon", "🏰", "三、巴比伦与被掳：耶利米、以西结、但以理、哀歌", "var(--orange)", ["babylon", "exile"],
           '<p>被掳者不是横越沙漠，而是沿幼发拉底河北上再南下——约 1,400 公里、四个月的路程（拉7:9）。</p>'),
          ("atl-persia", "👑", "四、波斯与归回：哈该、撒迦利亚、玛拉基", "var(--green)", ["persia"], '<p>古列的诏书应验了以赛亚 150 年前的预言（赛44:28）；归回者只是小小的“河西省”中的一个小省。</p>'),
          ("atl-daniel", "🐐", "五、但以理的四国：从巴比伦到罗马", "var(--teal)", ["daniel"], '<p>金、银、铜、铁——列国一个接一个，而“非人手凿出来的石头”（但2:34）要充满天下。</p>')]
def body():
    o = []
    o.append('''<section class="hero reveal"><div class="kick">ATLAS · MAPS · SCENES · MEDIA · v2</div><h1>🗺️ 先知书地图集 · 情景图 · 视频</h1>
<p class="lead">9 幅地图 × 3 种视图：<b class="k">🎨 讲解图</b>（动态路线、图标、情景）＋<b class="k">🏔️ 地形图</b>（Natural Earth 真实地貌）——都存在本站，<b class="k">断网也能显示</b>；再配 <b class="k">🌐 实时地图</b>，可在 12 个全球底图源之间切换（CARTO、Esri 地形/卫星/国家地理/自然地貌、OpenStreetMap、OpenTopoMap、OSM HOT、高德矢量/卫星……），任何一个源加载失败会<b class="k">自动换下一个</b>；全部失败时自动回到讲解图。</p>
<div class="chips"><span class="chip">🏞️ 应许之地</span><span class="chip">🦁 亚述</span><span class="chip">🏰 巴比伦</span><span class="chip">👑 波斯</span><span class="chip">🐐 但以理四国</span><span class="chip">🎞️ 动态图</span><span class="chip">🎬 视频全集</span></div></section>''')
    o.append(H2("atl-how", "🧭", "怎样用地图", "var(--blue)"))
    o.append(flow([("① 讲解图", "先看故事：谁、从哪里、到哪里", "var(--gold)"), ("② 地形图", "再看真实地貌：山、河、海、沙漠", "var(--orange)"), ("③ 实时地图", "缩放到遗址：卫星、等高线", "var(--teal)"), ("④ 列表", "点编号 → 地图定位并弹出说明", "var(--purple)")]))
    o.append(MEM('<p><span class="mm">先知地理口诀</span>：“<b class="k">北亚述、南埃及，中间夹着以色列；东巴比伦、再东波斯，归回走的是月湾路</b>”。</p>'))
    for gid, ic, t, c, ks, intro in GROUPS:
        o.append(H2(gid, ic, t, c)); o.append(intro)
        for k in ks: o.append(lib.MAP(k).replace('<span class="mx-t">', f'<h4 class="mx-t" id="t-{k}">', 1).replace('</span><div class="mx-tabs"', '</h4><div class="mx-tabs"', 1))
    o.append(H2("atl-anim", "🎞️", "六、动态图：四百年一图看完", "var(--purple)"))
    o.append(emp_anim()); o.append(matrix())
    o.append(H2("atl-vid", "🎬", "七、视频导览全集（BibleProject 简体中文）", "var(--pink)"))
    o.append('<p>点击才加载（不拖慢页面）。YouTube 无法访问时，点 <b class="k">📼 备用直链 MP4</b>（Mux 视频 CDN）。</p>')
    for t, keys in (("总览", ["prophets", "ot"]), ("大先知书", ["isa", "jer", "lam", "eze", "dan"]), ("十二小先知书", ["hos", "joel", "amos", "oba", "jonah", "micah", "nahum", "hab", "zeph", "hag", "zech", "mal"])):
        o.append(f'<h3 id="atl-vid-{keys[0]}">🎬 {t}</h3>')
        for k in keys: o.append(lib.vids(k))
    o.append(H2("atl-src", "🔖", "八、地图与视频来源", "var(--teal)"))
    o.append(table(["来源", "用途", "说明"], [["Natural Earth（公有领域）", "讲解图、地形图底图", "构建时预投影为本地 SVG，无需网络"], ["Leaflet 1.9.4（BSD-2）", "实时地图引擎", "自托管于 assets/vendor/leaflet，无 CDN 依赖"],
        ["CARTO · OpenStreetMap · Esri · OpenTopoMap · OSM France HOT · 高德", "在线瓦片底图（12 个）", "各自版权见地图右下角；加载失败自动换源"], ["BibleProject 简体中文", "视频导览", "YouTube（youtube-nocookie）与 Mux MP4 直链；非改革宗机构，仅作结构导览"]]))
    return "".join(o)

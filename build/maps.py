# -*- coding: utf-8 -*-
"""先知书地图：Natural Earth 公有领域底图（/workspace/ne），构建时预投影为静态 SVG（docs/assets/maps/*.svg），无 CDN。
地点坐标为通行考古/历史地理认定（多处为“约”）；古代海岸线（如波斯湾）与今日不同；路线为示意方向。"""
import os, html as H, re
import rmap
from rmap import PAL, ink
def M(k, n, en, lon, lat, y, t, c='blue', hl=False, ylab=False):
    return dict(k=k, n=n, en=en, ll=(lon, lat), y=y, t=t, c=c, hl=hl, ylab=ylab)
SPECS = {}
def S(**k): SPECS[k["id"]] = k; return k

# 1 先知的家乡与以色列地
S(id="land", title="先知们的家乡与工作地：以色列、犹大与列邻国（主前8–5世纪）", bbox=(33.9, 37.0, 29.9, 34.0), fine=True, fs=16,
  markers=[M("jeru","耶路撒冷 · 锡安","Jerusalem",35.23,31.78,"赛·耶·珥·番·该·亚·玛","以赛亚在圣殿蒙召；耶利米在殿门口讲道；归回后哈该、撒迦利亚催促重建圣殿。","gold",True),
    M("ana","亚拿突","Anathoth",35.26,31.81,"耶1:1","耶利米的家乡：祭司之城，距耶路撒冷约5公里——连同乡也想杀他（耶11:21）。","red",True),
    M("tek","提哥亚","Tekoa",35.22,31.63,"摩1:1","阿摩司的家乡：犹大旷野边缘的牧人与修理桑树的人。","orange",True),
    M("mor","摩利沙（迦特）","Moresheth-gath",34.90,31.60,"弥1:1","弥迦的家乡：犹大低地（示非拉）的乡村，靠近非利士边界与拉吉。","green"),
    M("lac","拉吉","Lachish",34.85,31.56,"弥1:13; 赛36","701年西拿基立围攻拉吉；拉吉信件（588）见证巴比伦围城的最后日子。","red"),
    M("bet","伯特利","Bethel",35.22,31.93,"摩7:10–13","北国王家圣所；阿摩司在此宣讲，被祭司亚玛谢驱逐。","purple",True),
    M("sam","撒玛利亚","Samaria",35.19,32.28,"何·摩·弥1","北国首都；“撒玛利亚山上巴珊的母牛”（摩4:1）；722 陷落。","purple",True),
    M("gat","迦特希弗","Gath-hepher",35.32,32.74,"王下14:25","约拿的家乡（加利利，靠近后来的拿撒勒）。","blue"),
    M("jop","约帕","Joppa",34.75,32.05,"拿1:3","约拿在此上船逃往他施。","blue"),
    M("jez","耶斯列","Jezreel",35.33,32.56,"何1:4","何西阿长子名“耶斯列”：宣告耶户家流血之罪的审判。","purple"),
    M("dam","大马士革","Damascus",36.29,33.51,"摩1:3; 赛17","亚兰首都；列国神谕第一站；732 被亚述攻陷。","teal"),
    M("tyr","推罗","Tyre",35.20,33.27,"摩1:9; 结26–28","腓尼基海上商业帝国；以西结的“推罗哀歌”。","teal"),
    M("gaz","迦萨","Gaza",34.46,31.50,"摩1:6; 番2:4","非利士五城之一；列国神谕。","orange"),
    M("rab","拉巴（亚扪）","Rabbah",35.93,31.95,"摩1:13; 耶49","亚扪首都（今安曼）。","pink"),
    M("bos","波斯拉（以东）","Bozrah",35.60,30.73,"俄; 赛63:1","以东重镇：“这从以东的波斯拉来……的是谁呢？”","red",True),
    M("moa","摩押（基珥哈列设）","Kir-hareseth",35.70,31.18,"赛15–16; 摩2:1","摩押首府；以赛亚为摩押哀哭。","pink")],
  regions=[("北国以色列",35.35,32.45,.42,.36,"purple"),("南国犹大",35.05,31.55,.35,.25,"gold"),("以东",35.55,30.45,.35,.4,"red"),("非利士",34.55,31.55,.15,.25,"orange")],
  water=[("大海（地中海）",34.3,32.9),("盐海",35.55,31.35)], rcap="区域为示意椭圆；先知家乡位置为通行认定（摩利沙、迦特希弗为约）")
# 2 约拿：他施与尼尼微
S(id="jonah", title="约拿书：往西逃向他施，神却差他往东去尼尼微", bbox=(-10.0, 48.0, 27.0, 44.5), fs=19,
  markers=[M("jop","约帕","Joppa",34.75,32.05,"拿1:3","约拿下到约帕，买船票“要躲避耶和华”。","blue",True),
    M("tar","他施（可能是西班牙塔特索斯）","Tarshish (Tartessos?)",-6.3,37.2,"拿1:3","当时已知世界的西极（另说撒丁岛）——与尼尼微方向正好相反。","gray",True),
    M("nin","尼尼微","Nineveh",43.15,36.36,"拿3","亚述大城，“三日的路程”；全城披麻蒙怜悯——约百年后仍因残暴灭亡（鸿3）。","red",True),
    M("gat","迦特希弗","Gath-hepher",35.32,32.74,"王下14:25","约拿的家乡，在耶罗波安二世时代预言北国扩张。","green"),
    M("tyr","推罗","Tyre",35.20,33.27,"腓尼基","他施船（远洋商船）的母港。","teal")],
  routes=[("jop","tar","gray",.10),("jop","nin","red",-.18)],
  water=[("大海（地中海）",18.0,35.0),("黑海",34.0,43.2)], rcap="灰：约拿逃往他施（约3,500公里，西）；红：神的差遣——尼尼微（约900公里，东）")
# 3 亚述帝国
S(id="assyria", title="亚述帝国与北国灭亡（主前745–612）", bbox=(28.5, 52.0, 26.0, 39.5), fs=19,
  markers=[M("nin","尼尼微","Nineveh",43.15,36.36,"612 陷落","西拿基立的首都；那鸿预言其倾覆。","red",True),
    M("ash","亚述城（亚述尔）","Assur",43.26,35.46,"古都","亚述神亚述尔的宗教中心。","red"),
    M("kal","迦拉（尼姆鲁德）","Calah / Nimrud",43.33,36.10,"黑色方尖碑","撒缦以色三世黑色方尖碑：耶户俯伏纳贡（841）。","orange"),
    M("goz","歌散（哈博河）","Gozan",40.04,36.83,"王下17:6","北国被掳者被安置之地。","gray"),
    M("har","哈兰","Harran",39.03,36.86,"610","亚述残部最后据点。","gray"),
    M("dam","大马士革","Damascus",36.29,33.51,"732","提革拉毗列色三世攻陷亚兰（赛7–8 叙利亚—以法莲战争）。","teal"),
    M("sam","撒玛利亚","Samaria",35.19,32.28,"722","北国灭亡；撒珥根二世迁民。","purple",True),
    M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"701","西拿基立围城，“十八万五千人”一夜被击杀（赛37:36）。","gold",True),
    M("lac","拉吉","Lachish",34.85,31.56,"701","尼尼微宫墙浮雕刻画攻陷拉吉。","orange"),
    M("tha","挪亚们（底比斯）","Thebes (No-Amon)",32.65,25.70,"663","亚述巴尼帕攻陷底比斯；那鸿用它警告尼尼微（鸿3:8）。","blue"),
    M("mem","孟斐斯","Memphis",31.25,29.85,"671","以撒哈顿攻入埃及。","blue"),
    M("bab","巴比伦","Babylon",44.42,32.54,"米罗达巴拉但","巴比伦使者访问希西家（赛39）。","orange")],
  routes=[("nin","dam","red",.12),("dam","sam","red",.2),("sam","goz","gray",-.15),("nin","jeru","red",-.1)],
  regions=[("亚述本土",43.3,36.0,1.8,1.2,"red"),("埃及",31.0,27.5,2.0,2.4,"blue"),("巴比伦尼亚",45.3,31.8,1.6,1.1,"orange")],
  water=[("大海（地中海）",31.5,33.9),("波斯湾",50.5,27.6)], rcap="红：亚述西征（大马士革732 → 撒玛利亚722 → 耶路撒冷701）；灰：北国被掳者被迁往歌散与玛代")
# 4 巴比伦与被掳
S(id="babylon", title="新巴比伦与南国被掳：耶利米、以西结、但以理的世界（主前626–539）", bbox=(28.5, 52.0, 26.0, 39.5), fs=19,
  markers=[M("bab","巴比伦","Babylon",44.42,32.54,"605–539","尼布甲尼撒的首都；但以理在宫廷事奉。","orange",True),
    M("nip","尼普尔 · 迦巴鲁河","Nippur / Chebar",45.23,32.13,"结1:1","以西结在提勒亚毕（迦巴鲁河边）见神的荣耀异象。","purple",True),
    M("car","迦基米施","Carchemish",38.01,36.83,"605","尼布甲尼撒击败法老尼哥——巴比伦称霸（耶46:2）。","gray",True),
    M("rib","利比拉","Riblah",36.55,34.45,"586","西底家在此被剜眼（耶39:5–7）。","gray"),
    M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"605/597/586","三次被掳；586 圣殿被焚（哀1–5）。","gold",True),
    M("miz","米斯巴","Mizpah",35.21,31.88,"耶40–41","基大利省长驻地；耶利米留在此地。","green"),
    M("tah","答比匿","Tahpanhes",32.10,30.98,"耶43","余民挟持耶利米逃往埃及；耶利米最后的预言。","blue",True),
    M("tyr","推罗","Tyre",35.20,33.27,"结26–29","尼布甲尼撒围城十三年（约585–572）。","teal"),
    M("nin","尼尼微","Nineveh",43.15,36.36,"612","巴比伦与米底联军攻陷亚述首都。","red"),
    M("ecb","埃克巴他拿（米底）","Ecbatana",48.52,34.80,"米底","米底王国首都——后为波斯所并。","teal")],
  routes=[("jeru","rib","gray",.15),("rib","bab","orange",.25),("jeru","tah","blue",.2),("car","bab","gray",-.15)],
  regions=[("巴比伦尼亚",45.0,32.0,1.8,1.2,"orange"),("米底",48.8,35.3,2.0,1.3,"teal"),("埃及",31.0,27.5,2.0,2.4,"blue")],
  water=[("大海（地中海）",31.5,33.9),("波斯湾",50.5,27.6)], rcap="橙：被掳者沿肥沃月湾北上再南下往巴比伦（非直线横越沙漠）；蓝：余民挟耶利米下埃及（耶43）")
# 5 但以理：四大帝国
S(id="daniel", title="但以理书的四国：巴比伦 → 玛代波斯 → 希腊 → 罗马（但2; 7）", bbox=(10.0, 64.0, 20.0, 45.0), fs=20,
  markers=[M("bab","巴比伦","Babylon",44.42,32.54,"金头 · 狮子","尼布甲尼撒（但2:38）；伯沙撒之宴（但5，539）。","gold",True),
    M("sus","书珊","Susa",48.26,32.19,"银 · 熊","但以理在书珊城的异象（但8:2）；波斯王宫。","green",True),
    M("per","波斯波利斯","Persepolis",52.89,29.93,"波斯","大流士、薛西的礼仪首都。","green"),
    M("pel","佩拉（马其顿）","Pella",22.52,40.76,"铜 · 豹","亚历山大大帝的故乡；“公山羊”（但8:5–8，主前334–323 东征）。","blue",True),
    M("ale","亚历山大城","Alexandria",29.92,31.20,"南方王","托勒密王朝（“南方王”，但11）。","blue"),
    M("ant","安提阿","Antioch",36.16,36.20,"北方王","塞琉古王朝（“北方王”）；安提阿古四世亵渎圣殿（167）。","purple"),
    M("rom","罗马","Rome",12.50,41.90,"铁 · 第四兽","第四国：大而可怕；在它的日子“天上的神必另立一国”（但2:44）。","red",True),
    M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"“荣美之地”","但8:9; 11:16 的“荣美之地”。","gold")],
  routes=[("pel","sus","blue",-.12)],
  regions=[("巴比伦",44.5,32.2,2.6,1.6,"gold"),("玛代波斯",52.0,32.0,5.0,3.4,"green"),("希腊（马其顿）",22.5,39.5,2.6,2.2,"blue"),("罗马（意大利）",13.0,42.3,2.4,1.8,"red")],
  water=[("大海（地中海）",19.0,34.5),("波斯湾",51.6,26.8),("黑海",34.0,43.4)], rcap="改革宗通常解释（加尔文等）：金头＝巴比伦、银＝玛代波斯、铜＝希腊、铁＝罗马；蓝箭头：亚历山大东征")
# 6 波斯时期归回
S(id="persia", title="波斯时期：归回、重建圣殿与最后的先知（主前539–430）", bbox=(28.5, 56.0, 23.5, 39.5), fs=19,
  markers=[M("sus","书珊","Susa",48.26,32.19,"尼1","波斯王宫；尼希米在此作酒政。","green",True),
    M("ecb","亚马他（埃克巴他拿）","Ecbatana",48.52,34.80,"拉6:2","找到古列诏书的卷轴（520）。","green"),
    M("bab","巴比伦","Babylon",44.42,32.54,"539","古列不战而入巴比伦；古列圆柱。","orange",True),
    M("per","波斯波利斯","Persepolis",52.89,29.93,"大流士","大流士一世（522–486）在位第二年，哈该、撒迦利亚开始说预言（520）。","green"),
    M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"538 / 520–516","所罗巴伯与约书亚带领归回；第二圣殿 516 完成。","gold",True),
    M("sam","撒玛利亚","Samaria",35.19,32.28,"拉4","撒玛利亚人阻挠重建。","purple"),
    M("mem","孟斐斯","Memphis",31.25,29.85,"埃及省","冈比西斯 525 征服埃及。","blue")],
  routes=[("bab","jeru","gold",-.14),("sus","jeru","green",.18)],
  regions=[("波斯（帕尔斯）",53.0,29.8,2.4,1.6,"green"),("米底",49.5,35.6,2.4,1.5,"teal"),("“河西省”（犹大省 Yehud）",35.6,32.3,1.6,1.3,"gold")],
  water=[("大海（地中海）",31.5,33.6),("波斯湾",51.2,27.4),("红海",36.0,24.8)],
  rcap="金：所罗巴伯（538）归回，沿幼发拉底河北绕；绿：尼希米（445）。哈该、撒迦利亚（520）、玛拉基（约460–430）都在犹大省说预言")
def build(outdir, ver):
    os.makedirs(outdir, exist_ok=True); out = {}
    for k, sp in SPECS.items():
        W = 1000 if sp["bbox"][1]-sp["bbox"][0] < 10 else 1200
        svg, w, h, hs = rmap.real_svg(sp, W)
        # 动态：路线虚线流动（SVG 内 CSS；尊重减少动态）
        svg = svg.replace('</defs>', '</defs><style>path[marker-end]{animation:fl 1.6s linear infinite}@keyframes fl{to{stroke-dashoffset:-26}}@media (prefers-reduced-motion:reduce){path[marker-end]{animation:none}}</style>', 1)
        open(os.path.join(outdir, k + ".svg"), "w").write(svg)
        out[k] = (sp, w, h, hs)
    return out
def html(k, built, ver):
    sp, w, h, hs = built[k]
    t = H.escape(sp["title"])
    hsb = "".join(f'<button class="hs" style="left:{x:.2f}%;top:{y:.2f}%" data-i="{i}" aria-label="{i+1} {H.escape(m["n"])}"></button>' for i, (m, (x, y)) in enumerate(hs))
    li = "".join(f'<li data-i="{i}" tabindex="0" style="--c:{PAL[m.get("c","blue")]};--t:{ink(PAL[m.get("c","blue")])}"><b>{i+1}</b><span><strong>{H.escape(m["n"])}</strong> <i>{H.escape(m["en"])}</i> · <em>{H.escape(m["y"])}</em>：{H.escape(m["t"])}</span></li>' for i, m in enumerate(sp["markers"]))
    return (f'<figure class="gmap" id="map-{k}"><div class="gm-bar"><span>🗺️ {t}</span><span class="gm-z"><button data-z="-1" aria-label="缩小">－</button><button data-z="0" aria-label="复位">⟲</button><button data-z="1" aria-label="放大">＋</button></span></div>'
            f'<div class="gm-view"><div class="gm-in" style="aspect-ratio:{w}/{h}"><img src="assets/maps/{k}.svg?v={ver}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{t}">{hsb}</div></div>'
            f'<figcaption>真实地形底图：Natural Earth（公有领域），本站绘制；地点为通行历史地理认定（部分为“约”）。{H.escape(sp.get("rcap",""))}。点编号或下方列表可高亮地点。</figcaption><ol class="gm-leg">{li}</ol></figure>')

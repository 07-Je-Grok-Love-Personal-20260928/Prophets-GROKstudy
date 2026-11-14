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
# ---------------- v2 新增地图 ----------------
# 7 阿摩司列国神谕包围圈
S(id="amos", title="阿摩司的“包围圈”：神谕从外邦一圈圈收紧到以色列（摩1–2）", bbox=(33.6, 37.2, 30.3, 33.9), fine=True, fs=16,
  markers=[M("dam","① 大马士革（亚兰）","Damascus",36.29,33.51,"摩1:3","用打粮食的铁器打基列——战争暴行。","teal"),
    M("gaz","② 迦萨（非利士）","Gaza",34.46,31.50,"摩1:6","掳掠全群的人交给以东——贩卖人口。","orange"),
    M("tyr","③ 推罗（腓尼基）","Tyre",35.20,33.27,"摩1:9","不记念弟兄的盟约——背约贩奴。","teal"),
    M("bos","④ 以东（波斯拉）","Edom",35.60,30.73,"摩1:11","拿刀追赶兄弟——世仇（雅各与以扫）。","red"),
    M("rab","⑤ 亚扪（拉巴）","Ammon",35.93,31.95,"摩1:13","剖开基列的孕妇——为扩张疆界。","pink"),
    M("moa","⑥ 摩押","Moab",35.70,31.18,"摩2:1","将以东王的骸骨焚烧成灰——亵渎死者。","pink"),
    M("jeru","⑦ 犹大（耶路撒冷）","Judah",35.23,31.78,"摩2:4","厌弃耶和华的训诲——背弃律法。","gold",True),
    M("sam","⑧ 以色列（撒玛利亚）","Israel",35.19,32.28,"摩2:6","为一双鞋卖了穷人——靶心！","purple",True)],
  routes=[("dam","gaz","red",.25),("gaz","tyr","red",.25),("tyr","bos","red",.15),("bos","rab","red",.2),("rab","moa","red",.2),("moa","jeru","red",.2),("jeru","sam","red",.3)],
  water=[("大海（地中海）",34.3,32.9),("盐海",35.55,31.35)], rcap="红色箭头＝神谕的次序：先东北、西南、西北、东南……像绳索绕圈，最后落在以色列身上（3×4 的“三番四次”公式）", seq=True)
# 8 被掳与归回：三波出、三波回
S(id="exile", title="三次被掳 · 三次归回：从耶路撒冷到巴比伦，再回到锡安（主前605–445）", bbox=(31.0, 52.0, 27.5, 38.5), fs=19,
  markers=[M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"605 / 597 / 586","① 605 但以理等贵族被掳 ② 597 约雅斤与以西结被掳 ③ 586 城与圣殿被焚。","gold",True),
    M("rib","利比拉","Riblah",36.55,34.45,"586","尼布甲尼撒大本营：西底家眼见众子被杀后被剜眼（王下25:6-7）。","gray"),
    M("car","迦基米施","Carchemish",38.01,36.83,"605","巴比伦击败埃及，夺得叙利亚—巴勒斯坦（耶46:2）。","gray"),
    M("bab","巴比伦","Babylon",44.42,32.54,"605–539","被掳之地；但以理事奉四朝；539 古列不战而入城。","orange",True),
    M("che","迦巴鲁河（尼普尔）","Chebar / Nippur",45.23,32.13,"结1:1","被掳者聚居的提勒亚毕；以西结见荣耀异象。","purple",True),
    M("sus","书珊","Susa",48.26,32.19,"445","尼希米从书珊王宫出发（尼1–2）。","green"),
    M("ecb","亚马他","Ecbatana",48.52,34.80,"拉6:2","找到古列诏书的卷轴。","teal")],
  routes=[("jeru","rib","gray",.2),("rib","car","gray",.2),("car","bab","red",-.1),("bab","jeru","green",-.25),("sus","jeru","teal",.3)],
  regions=[("巴比伦尼亚",45.0,32.0,1.8,1.2,"orange"),("“河西省”",35.8,32.6,1.4,1.4,"gold")],
  water=[("大海（地中海）",33.0,34.4),("波斯湾",50.3,28.4)], rcap="灰→红：被掳者沿肥沃月湾北上再南下（约1,400公里，四个月路程，拉7:9）；绿：538 所罗巴伯、458 以斯拉归回；青：445 尼希米",
  steps=[("605","第一次被掳：但以理与三友（但1）","red"),("597","第二次：约雅斤、以西结与一万人（王下24）","red"),("586","第三次：圣殿被焚、城墙拆毁（王下25；哀1–5）","red"),
         ("538","第一次归回：所罗巴伯与约书亚，约五万人（拉1–2）","green"),("458","第二次：以斯拉带律法归回（拉7–8）","green"),("445","第三次：尼希米重修城墙（尼1–6）","teal")])
# 9 耶路撒冷城（希西家—尼希米）
S(id="jerusalem", title="耶路撒冷城：701 被围不破，586 城破殿焚（锡安的地理）", bbox=(35.222, 35.248, 31.762, 31.786), fs=16, scene=True,
  markers=[M("tem","圣殿山（摩利亚）","Temple Mount",35.2355,31.7781,"赛6; 结8–11","以赛亚见主坐在宝座上；以西结见荣耀离殿。","gold",True),
    M("cod","大卫城（俄斐勒）","City of David",35.2353,31.7735,"撒下5:7","最古老的耶路撒冷，锡安的保障。","orange",True),
    M("gih","基训泉","Gihon Spring",35.2365,31.7731,"代下32:30","城中唯一常年水源——围城生死所系。","blue"),
    M("sil","西罗亚池","Pool of Siloam",35.2350,31.7704,"赛8:6; 约9:7","希西家水道终点（西罗亚碑文）；“西罗亚缓流的水”。","blue",True),
    M("bro","宽墙","Broad Wall",35.2312,31.7760,"赛22:10; 尼3:8","为抵御亚述拆房修城，约7米厚（犹太区遗迹）。","red"),
    M("mol","橄榄山","Mount of Olives",35.2441,31.7784,"结11:23; 亚14:4","荣耀停在城东的山上；主再来时脚站在橄榄山。","green",True),
    M("kid","汲沦谷","Kidron Valley",35.2385,31.7760,"耶31:40","城东的谷——将来“归耶和华为圣”。","teal"),
    M("hin","欣嫩子谷（陀斐特）","Hinnom / Topheth",35.2310,31.7690,"耶7:31; 19","焚烧儿女献给摩洛之地——“杀戮谷”。","red"),
    M("eg","东门（金门遗址）","East Gate",35.2373,31.7788,"结10:19; 43:4","荣耀从东门离去，又从东门回来。","purple")],
  routes=[("gih","sil","blue",.25),("tem","mol","purple",-.2)], rcap="蓝：希西家水道（约533米，基训泉→西罗亚池，王下20:20）；紫：荣耀离开圣殿的路线（结10:19 → 11:23）")
# v3 列国神谕
S(id="nations", title="列国神谕：从古实到以拦，神是万国的主（赛13–23；耶46–51；结25–32；摩1–2）", bbox=(24.0, 52.0, 14.0, 39.0), fs=19,
  markers=[M("bab","巴比伦","Babylon",44.42,32.54,"赛13–14；耶50–51","骄傲之城终必倾覆；启18 用“大巴比伦”象征与神为敌的世界。","orange",True),
    M("nin","尼尼微（亚述）","Nineveh",43.15,36.36,"赛10；鸿1–3；番2:13","神用亚述作“怒气的棍”，又因它的狂傲审判它（赛10:5-12）。","red",True),
    M("sus","苏萨（以拦）","Susa / Elam",48.25,32.19,"耶49:34-39","“到末后，我还要使以拦被掳的人归回”——审判中仍有怜悯。","purple"),
    M("dam","大马士革（亚兰）","Damascus",36.29,33.51,"赛17；耶49:23；摩1:3","“用铁打粮的器具打过基列”——战争暴行被追讨。","teal"),
    M("tyr","推罗","Tyre",35.20,33.27,"赛23；结26–28；摩1:9","海上商业帝国；结28 写推罗王的骄傲与堕落。","blue"),
    M("gaz","迦萨（非利士）","Gaza / Philistia",34.46,31.50,"耶47；摩1:6；番2:4","掳掠全群人口卖给以东——贩卖人口被神记账。","gray"),
    M("rab","拉巴（亚扪）","Rabbah / Ammon",35.93,31.95,"耶49:1-6；结25:1-7；摩1:13","为扩张境界剖开基列的孕妇。","orange"),
    M("moa","基珥哈列设（摩押）","Kir-hareseth / Moab",35.70,31.18,"赛15–16；耶48；摩2:1","赛16:5：审判中竟应许“大卫帐幕”里坚立的宝座。","pink"),
    M("bos","波斯拉（以东）","Bozrah / Edom",35.60,30.73,"赛34；63:1；俄巴底亚书","以扫后裔幸灾乐祸；赛63 那位“从以东的波斯拉来”的得胜者。","red"),
    M("ked","度玛 · 基达（阿拉伯）","Dumah / Kedar",39.87,29.81,"赛21:11-17；耶49:28-33","“守望的啊，夜里如何？”——旷野商队之民也在神手中。","gold"),
    M("mem","挪弗（埃及）","Memphis / Egypt",31.25,29.85,"赛19；耶46；结29–32","赛19:24-25：埃及、亚述、以色列同称为神的子民——惊人的万国应许。","blue",True),
    M("cus","古实（纳帕塔）","Cush / Napata",31.82,18.53,"赛18；番3:10","“从古实河外”也要有人带供物到锡安。","green"),
    M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"赛22；摩2:4-5","列国神谕的圆心：审判从神的家起首（摩2 包围圈收口）。","gold",True)],
  routes=[("nin","jeru","red",-.12),("bab","jeru","orange",.12),("mem","jeru","blue",-.2)],
  steps=[("赛13–23","以赛亚：十个“重担”，巴比伦开头、推罗结尾","red"),("耶46–51","耶利米：从埃及一路到巴比伦","orange"),("结25–32","以西结：七国，推罗与埃及最详","purple"),("摩1–2","阿摩司：包围圈一圈圈收口到以色列","teal"),("俄 · 鸿","俄巴底亚审以东；那鸿审尼尼微","gray")],
  water=[("大海（地中海）",28.5,34.2),("红海",37.6,21.0),("波斯湾",50.0,28.2)], rcap="红/橙/蓝箭头：亚述、巴比伦、埃及三强对以色列的压力方向；编号＝神谕对象")
# v3 下埃及
S(id="egypt", title="下埃及：耶利米最后的旅程与埃及神谕（耶40–46；结29–32）", bbox=(26.0, 38.8, 23.6, 33.2), fs=19,
  markers=[M("jeru","耶路撒冷","Jerusalem",35.23,31.78,"586","城破后，巴比伦立基大利为省长（耶40）。","gold",True),
    M("miz","米斯巴","Mizpah",35.22,31.88,"耶40–41","基大利在此被以实玛利刺杀，余民惊惶。","red"),
    M("ger","金罕寓（伯利恒旁）","Geruth Chimham",35.20,31.70,"耶41:17","余民聚集，执意要下埃及。","orange"),
    M("tah","答比匿","Tahpanhes",32.13,30.86,"耶43:7-13","耶利米在法老宫门口埋大石：尼布甲尼撒要在此设宝座。","purple",True),
    M("mig","密夺","Migdol",32.36,30.98,"耶44:1；结29:10","东北边防要塞；“从密夺到色弗尼”＝全埃及。","teal"),
    M("mem","挪弗（孟斐斯）","Noph / Memphis",31.25,29.85,"耶44:1；46:14","下埃及古都；犹太难民散居之处。","blue"),
    M("tha","巴忒罗（上埃及 · 底比斯）","Pathros / Thebes",32.65,25.70,"耶44:1,15","犹太人在此向“天后”烧香，公然拒绝先知（耶44）。","gray"),
    M("syn","色弗尼 · 象岛","Syene / Elephantine",32.89,24.09,"结29:10；30:6","埃及南境；象岛纸草（主前5世纪）记有犹太殖民地及其自建的殿。","green")],
  routes=[("miz","ger","gray",0.0),("ger","tah","red",.18),("tah","mem","red",.12),("mem","tha","gray",.1)],
  steps=[("586","耶路撒冷陷落，基大利任省长（耶40）","red"),("约582","基大利遇刺，余民惧怕巴比伦报复（耶41）","orange"),("约582","不听“不要下埃及”，挟耶利米同去（耶42–43）","purple"),("568/567","尼布甲尼撒攻入埃及，耶43:10-13 开始应验","red")],
  water=[("大海（地中海）",33.3,32.6),("尼罗河",31.2,27.2),("红海",34.6,26.6)], rcap="红线：余民违背神的话下埃及的路线；灰线：散居上下埃及")
ICON = {"jeru": "🏛️", "tem": "🏛️", "nin": "🦁", "bab": "🏰", "sus": "👑", "per": "🏛️", "rom": "🦅", "pel": "🐐", "tar": "⛵", "jop": "⚓", "tyr": "⛵", "dam": "🏯",
        "sam": "🐄", "lac": "⚔️", "ana": "🏡", "tek": "🐑", "mor": "🌾", "bet": "🐂", "gat": "🏡", "jez": "🩸", "gaz": "🏺", "rab": "🏕️", "bos": "🏔️", "moa": "🔥",
        "ash": "🗿", "kal": "🗿", "goz": "⛓️", "har": "🌙", "tha": "🏺", "mem": "🔺", "nip": "👁️", "che": "👁️", "car": "⚔️", "rib": "⛓️", "miz": "🌿", "tah": "🔺",
        "ecb": "📜", "ale": "📚", "ant": "🐏", "cod": "🏰", "gih": "💧", "sil": "💧", "bro": "🧱", "mol": "🫒", "kid": "🌊", "hin": "🔥", "eg": "🚪", "cus": "🏹", "ked": "🐪", "ger": "🏕️", "mig": "🗼", "syn": "🐘"}
from rmap import base, proj, Placer, spread, tw
import json, math
def concept_svg(sp, W):
    """🎨 讲解图：卡通化底图（Natural Earth 简化）+ 大图标 + 编号 + 动态路线（SMIL 小圆点沿路线移动）。独立 SVG 文件，离线可用。"""
    P, sx, sy, H, land, lakes, riv = base(sp["bbox"], W, False)
    fs = 26 if W >= 1000 else 22
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="\'Noto Sans CJK SC\',\'PingFang SC\',\'Microsoft YaHei\',sans-serif">',
         '<defs><linearGradient id="sea" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a8dcf5"/><stop offset="1" stop-color="#6fb8e6"/></linearGradient>',
         '<linearGradient id="ld" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff3d1"/><stop offset="1" stop-color="#f3d99b"/></linearGradient>',
         '<filter id="sh" x="-5%" y="-5%" width="110%" height="110%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#3b2a10" flood-opacity=".28"/></filter>',
         '<pattern id="wv" width="60" height="24" patternUnits="userSpaceOnUse"><path d="M0,12 q15,-8 30,0 t30,0" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width="2"/></pattern>']
    cols = sorted({PAL[r[2]] for r in sp.get("routes", ())})
    for c in cols: o.append(f'<marker id="a{c[1:]}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="{c}"/></marker>')
    o.append('</defs><style>.wv{animation:wv 6s linear infinite}@keyframes wv{to{transform:translateX(60px)}}.rt{stroke-dasharray:14 10;animation:fl 1.4s linear infinite}@keyframes fl{to{stroke-dashoffset:-48}}'
             '.pin{transform-box:fill-box;transform-origin:center;animation:bob 3.2s ease-in-out infinite}@keyframes bob{50%{transform:translateY(-4px)}}'
             '@media (prefers-reduced-motion:reduce){.wv,.rt,.pin{animation:none}}</style>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#sea)"/><g class="wv"><rect x="-60" width="{W + 120}" height="{H}" fill="url(#wv)"/></g>')
    o.append(f'<path d="{land}" fill="url(#ld)" stroke="#b58a3a" stroke-width="3" stroke-linejoin="round" fill-rule="evenodd" filter="url(#sh)"/>')
    if lakes: o.append(f'<path d="{lakes}" fill="#8fd0f0" stroke="#4a9fd0" stroke-width="2"/>')
    if riv: o.append(f'<path d="{riv}" fill="none" stroke="#3a92d6" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')
    for lab, lon, lat, rx, ry, c in sp.get("regions", ()):
        x, y = P(lon, lat)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx * sx:.0f}" ry="{ry * sy:.0f}" fill="{PAL[c]}" fill-opacity=".22" stroke="{PAL[c]}" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>')
    pl = Placer(W, H); mk = sp["markers"]; R = 24 if W >= 1000 else 20
    pos = spread(mk, P, R + 2, R)
    for m in mk:
        x, y, r = pos[m["k"]]; pl.add((x - r - 4, y - r - 4, x + r + 4, y + r + 4))
    pl.add((W - 70, 6, W - 6, 76))
    for n_, (a, b, c, *rest) in enumerate(sp.get("routes", ())):
        (x1, y1, r1), (x2, y2, r2) = pos[a], pos[b]
        L = math.hypot(x2 - x1, y2 - y1) or 1; ux, uy = (x2 - x1) / L, (y2 - y1) / L
        x1, y1, x2, y2 = x1 + ux * (r1 + 4), y1 + uy * (r1 + 4), x2 - ux * (r2 + 8), y2 - uy * (r2 + 8)
        bend = (rest[0] if rest else .18) * L; mx, my = (x1 + x2) / 2 + uy * bend, (y1 + y2) / 2 - ux * bend
        d = f"M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}"
        o.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".7"/><path class="rt" d="{d}" fill="none" stroke="{PAL[c]}" stroke-width="6" stroke-linecap="round" marker-end="url(#a{PAL[c][1:]})"/>')
        dur = 3 + L / 260; beg = (n_ * .9) if sp.get("seq") else 0
        o.append(f'<circle r="7" fill="{PAL[c]}" stroke="#fff" stroke-width="2.5"><animateMotion dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite" path="{d}"/></circle>')
    halo = 'paint-order="stroke" stroke="#fffaf0" stroke-width="6" stroke-linejoin="round"'
    T = []
    for i in sorted(range(len(mk)), key=lambda i: (not mk[i].get("hl"), i)):
        m = mk[i]; x, y, r = pos[m["k"]]
        lab = m["n"]; res = pl.label(x, y, r + 2, lab, fs if m.get("hl") else fs - 4)
        if not res: continue
        bx, by, an, far = res
        T.append(f'<text x="{bx:.0f}" y="{by:.0f}" text-anchor="{an}" font-size="{fs if m.get("hl") else fs - 4}" font-weight="{900 if m.get("hl") else 700}" fill="#2a1d08" {halo}>{H_(lab)}</text>')
    for lab, lon, lat in sp.get("water", ()):
        x, y = P(lon, lat); w = tw(lab, fs - 4); b = (x - w / 2, y - fs, x + w / 2, y + 4)
        if pl.free(b): pl.add(b); T.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-size="{fs - 4}" font-style="italic" font-weight="700" fill="#1d5f8f" letter-spacing="3">{H_(lab)}</text>')
    for lab, lon, lat, rx, ry, c in sp.get("regions", ()):
        x, y = P(lon, lat); res = pl.label(x, y - ry * sy * .3, 0, lab, fs - 5)
        if res: T.append(f'<text x="{res[0]:.0f}" y="{res[1]:.0f}" text-anchor="{res[2]}" font-size="{fs - 5}" font-weight="900" fill="{_dk(PAL[c])}" {halo}>{H_(lab)}</text>')
    o += T
    for i, m in enumerate(mk):
        x, y, r = pos[m["k"]]; c = PAL[m.get("c", "blue")]; ic = ICON.get(m["k"], "📍")
        o.append(f'<g class="pin" style="animation-delay:{(i % 5) * .4:.1f}s"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fffdf6" stroke="{c}" stroke-width="5"/>'
                 f'<text x="{x:.0f}" y="{y + r * .36:.0f}" text-anchor="middle" font-size="{r * 1.05:.0f}">{ic}</text>'
                 f'<circle cx="{x + r * .78:.0f}" cy="{y - r * .78:.0f}" r="11" fill="{c}" stroke="#fff" stroke-width="2"/><text x="{x + r * .78:.0f}" y="{y - r * .78 + 4.5:.0f}" text-anchor="middle" font-size="13" font-weight="900" fill="{ink(c)}">{i + 1}</text></g>')
    o.append(f'<g transform="translate({W - 38},40)"><circle r="28" fill="#fffaf0" stroke="#b58a3a" stroke-width="2"/><path d="M0,-22L7,0L0,-4L-7,0z" fill="#d94a38"/><path d="M0,22L7,0L0,4L-7,0z" fill="#8a7a5a"/><text y="-8" x="12" font-size="12" font-weight="900" fill="#2a1d08">N</text></g>')
    o.append('</svg>')
    return "".join(o), H
def _dk(c):
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16); return "#%02x%02x%02x" % (int(r * .5), int(g * .5), int(b * .5))
H_ = H.escape
def jerusalem_svg(sp):
    """耶路撒冷情景图（手绘风，示意比例）：地势、城墙、圣殿、水道、亚述营与巴比伦破城。"""
    W, Hh = 1000, 700
    pt = {"tem": (520, 205), "eg": (622, 196), "cod": (515, 340), "gih": (600, 352), "sil": (470, 478), "bro": (330, 262), "mol": (845, 230), "kid": (688, 420), "hin": (300, 585)}
    lab = {"tem": None, "eg": ("start", 18, -14), "cod": ("end", -20, 6), "gih": ("start", 20, 6), "sil": ("end", -20, 6), "bro": ("end", -20, 6), "mol": ("middle", 0, -26), "kid": ("start", 20, 6), "hin": ("start", 20, 6)}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" font-family="\'Noto Sans CJK SC\',\'PingFang SC\',\'Microsoft YaHei\',sans-serif">',
         '<defs><radialGradient id="hl" cx=".45" cy=".4" r=".75"><stop offset="0" stop-color="#fbe9bd"/><stop offset="1" stop-color="#e3c27e"/></radialGradient>',
         '<linearGradient id="vl" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#a9cf94"/><stop offset="1" stop-color="#76a96a"/></linearGradient>',
         '<marker id="ab" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0L10,5L0,10z" fill="#2f7fd0"/></marker>',
         '<marker id="ap" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0L10,5L0,10z" fill="#8b5cf6"/></marker></defs>',
         '<style>.fl{stroke-dasharray:12 9;animation:f 1.3s linear infinite}@keyframes f{to{stroke-dashoffset:-42}}.fire{transform-box:fill-box;transform-origin:50% 100%;animation:fi 1.1s ease-in-out infinite alternate}@keyframes fi{to{transform:scale(1.12,1.22)}}'
         '.glow{animation:gl 3s ease-in-out infinite}@keyframes gl{50%{opacity:.3}}@media (prefers-reduced-motion:reduce){.fl,.fire,.glow{animation:none}}</style>',
         f'<rect width="{W}" height="{Hh}" fill="url(#hl)"/>',
         # 汲沦谷（东）与欣嫩子谷（西、南），中谷
         '<path d="M668,0 C700,160 700,330 690,470 C680,560 640,620 600,700 L700,700 C730,620 760,520 760,420 C760,300 750,150 735,0Z" fill="url(#vl)"/>',
         '<path d="M150,180 C200,300 200,470 250,560 C320,650 470,660 640,640 L620,700 L400,700 C260,690 170,620 130,520 C100,420 110,300 95,190Z" fill="url(#vl)"/>',
         '<path d="M445,110 C440,250 450,380 462,500" fill="none" stroke="#8fbf7c" stroke-width="22" stroke-linecap="round" opacity=".55"/>',
         '<ellipse cx="855" cy="300" rx="120" ry="270" fill="#bcd690"/>']
    for i in range(15):
        tx, ty = 800 + (i % 3) * 48, 110 + (i // 3) * 82
        o.append(f'<circle cx="{tx}" cy="{ty}" r="15" fill="#6f9a4a"/><rect x="{tx - 2}" y="{ty + 12}" width="4" height="10" fill="#7a5a30"/>')
    wall = "M425,118 L645,118 L652,300 L570,425 L505,505 L420,508 L262,440 L248,190Z"
    o.append(f'<path d="{wall}" fill="#f2e0b8" stroke="#8a6a3a" stroke-width="10" stroke-linejoin="round"/><path d="{wall}" fill="none" stroke="#c9a46a" stroke-width="3" stroke-dasharray="4 10"/>')
    for i in range(16): o.append(f'<rect x="{462 + (i % 4) * 26 + (i // 4) % 2 * 8}" y="{285 + (i // 4) * 28}" width="20" height="16" fill="#e6c88e" stroke="#9a7a48" stroke-width="1.5"/>')
    for i in range(16): o.append(f'<rect x="{290 + (i % 4) * 30}" y="{300 + (i // 4) * 30}" width="22" height="17" fill="#ead2a0" stroke="#9a7a48" stroke-width="1.5"/>')
    tx_, ty_ = pt["tem"]
    o.append(f'<circle class="glow" cx="{tx_}" cy="{ty_}" r="62" fill="#ffd54a" opacity=".5"/><rect x="{tx_ - 60}" y="{ty_ - 48}" width="120" height="92" rx="8" fill="#fff5d8" stroke="#a37b2c" stroke-width="4"/>'
             f'<rect x="{tx_ - 18}" y="{ty_ - 34}" width="36" height="58" fill="#e9b949" stroke="#8a6a1a" stroke-width="3"/><text x="{tx_}" y="{ty_ + 72}" text-anchor="middle" font-size="22" font-weight="900" fill="#5a3d0a" paint-order="stroke" stroke="#fff5d8" stroke-width="5">圣殿</text>')
    o.append(f'<text class="fire" x="{tx_ - 92}" y="{ty_ - 40}" font-size="34">🔥</text><text class="fire" x="{tx_ + 62}" y="{ty_ - 46}" font-size="28" style="animation-delay:.3s">🔥</text>')
    gx, gy = pt["gih"]; sx_, sy_ = pt["sil"]
    o.append(f'<path class="fl" d="M{gx - 6},{gy + 14} C{gx - 10},{gy + 90} {sx_ + 80},{sy_ - 10} {sx_ + 20},{sy_ - 4}" fill="none" stroke="#2f7fd0" stroke-width="7" marker-end="url(#ab)"/>')
    o.append(f'<path class="fl" d="M{tx_ + 30},{ty_ - 52} Q700,70 {pt["mol"][0] - 30},{pt["mol"][1] - 6}" fill="none" stroke="#8b5cf6" stroke-width="6" marker-end="url(#ap)"/>')
    o.append('<g><text x="40" y="70" font-size="40">⛺⛺⛺</text><text x="40" y="108" font-size="21" font-weight="900" fill="#b03a2a">701 亚述大军围城</text><text x="40" y="134" font-size="16" fill="#5a3d0a">城未被攻破：一夜十八万五千人（赛37:36）</text></g>')
    o.append('<g><text x="40" y="236" font-size="38">🏹🛡️</text><text x="40" y="272" font-size="21" font-weight="900" fill="#b03a2a">586 巴比伦破城</text><text x="40" y="298" font-size="16" fill="#5a3d0a">城墙拆毁、圣殿焚烧（王下25:9-10）</text></g>')
    o.append(f'<text x="{pt["hin"][0] - 44}" y="{pt["hin"][1] + 12}" font-size="28">🔥</text>')
    halo = 'paint-order="stroke" stroke="#fffaf0" stroke-width="5" stroke-linejoin="round"'
    for i, m in enumerate(sp["markers"]):
        x, y = pt[m["k"]]; c = PAL[m["c"]]
        o.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{c}" stroke="#fff" stroke-width="3"/><text x="{x}" y="{y + 5}" text-anchor="middle" font-size="14" font-weight="900" fill="{ink(c)}">{i + 1}</text>')
        L = lab[m["k"]]
        if L: o.append(f'<text x="{x + L[1]}" y="{y + L[2]}" text-anchor="{L[0]}" font-size="19" font-weight="800" fill="#2a1d08" {halo}>{H_(m["n"])}</text>')
    o.append(f'<g transform="translate({W - 40},{Hh - 44})"><circle r="26" fill="#fffaf0" stroke="#b58a3a" stroke-width="2"/><path d="M0,-20L6,0L0,-4L-6,0z" fill="#d94a38"/><text y="18" text-anchor="middle" font-size="11" font-weight="900">N</text></g>')
    o.append(f'<text x="20" y="{Hh - 16}" font-size="14" fill="#3d2a08">情景示意图（本站手绘；比例与城墙走向为示意，位置依通行考古认定）· 蓝：希西家水道　紫：荣耀离殿路线</text></svg>')
    return "".join(o), W, Hh
def build(outdir, ver):
    os.makedirs(outdir, exist_ok=True); out = {}
    for k, sp in SPECS.items():
        W = 1000 if sp["bbox"][1] - sp["bbox"][0] < 10 else 1200
        if sp.get("scene"):
            svg, w, h = jerusalem_svg(sp); open(os.path.join(outdir, k + "-c.svg"), "w").write(svg)
            out[k] = (sp, w, h, None, w, h); continue
        svg, w, h, hs = rmap.real_svg(sp, W)
        svg = svg.replace('</defs>', '</defs><style>path[marker-end]{animation:fl 1.6s linear infinite}@keyframes fl{to{stroke-dashoffset:-26}}@media (prefers-reduced-motion:reduce){path[marker-end]{animation:none}}</style>', 1)
        open(os.path.join(outdir, k + ".svg"), "w").write(svg)
        for m in sp["markers"]: m.pop("_nolab", None)
        csvg, ch = concept_svg(sp, W); open(os.path.join(outdir, k + "-c.svg"), "w").write(csvg)
        out[k] = (sp, w, h, hs, W, ch)
    return out
def html(k, built, ver):
    sp, w, h, hs, cw, ch = built[k]
    t = H.escape(sp["title"])
    data = dict(b=sp["bbox"], m=[[m["ll"][1], m["ll"][0], m["n"], m["y"], m["t"], PAL[m.get("c", "blue")], ICON.get(m["k"], "📍")] for m in sp["markers"]],
                r=[[[sp["markers"][[x["k"] for x in sp["markers"]].index(a)]["ll"][1], sp["markers"][[x["k"] for x in sp["markers"]].index(a)]["ll"][0]],
                    [sp["markers"][[x["k"] for x in sp["markers"]].index(b)]["ll"][1], sp["markers"][[x["k"] for x in sp["markers"]].index(b)]["ll"][0]], PAL[c]] for a, b, c, *_ in sp.get("routes", ())])
    js = H.escape(json.dumps(data, ensure_ascii=False), quote=True)
    li = "".join(f'<li data-i="{i}" tabindex="0" style="--c:{PAL[m.get("c","blue")]};--t:{ink(PAL[m.get("c","blue")])}"><b>{i+1}</b><span><strong>{ICON.get(m["k"],"📍")} {H.escape(m["n"])}</strong> <i>{H.escape(m["en"])}</i> · <em>{H.escape(m["y"])}</em>：{H.escape(m["t"])}</span></li>' for i, m in enumerate(sp["markers"]))
    tabs = '<div class="mx-tabs" role="tablist" aria-label="地图视图"><button role="tab" aria-selected="true" data-p="c">🎨 讲解图</button>' + ('' if sp.get("scene") else '<button role="tab" aria-selected="false" data-p="t">🏔️ 地形图</button>') + '<button role="tab" aria-selected="false" data-p="l">🌐 实时地图</button></div>'
    cpane = f'<div class="mx-pane on" data-p="c"><div class="gm-view"><div class="gm-in" style="aspect-ratio:{cw}/{ch}"><img src="assets/maps/{k}-c.svg?v={ver}" width="{cw}" height="{ch}" loading="lazy" decoding="async" alt="{t}（讲解图）"></div></div></div>'
    tpane = "" if sp.get("scene") else (f'<div class="mx-pane" data-p="t"><div class="gm-view"><div class="gm-in" style="aspect-ratio:{w}/{h}"><img data-src="assets/maps/{k}.svg?v={ver}" width="{w}" height="{h}" decoding="async" alt="{t}（地形图）">'
                                        + "".join(f'<button class="hs" style="left:{x:.2f}%;top:{y:.2f}%" data-i="{i}" aria-label="{i+1} {H.escape(m["n"])}"></button>' for i, (m, (x, y)) in enumerate(hs)) + '</div></div></div>')
    lpane = ('<div class="mx-pane" data-p="l"><div class="lm-bar"><label>🧭 底图源 <select class="lm-src" aria-label="选择在线底图"></select></label><span class="lm-st" role="status" aria-live="polite">点“实时地图”后加载（自托管 Leaflet，多源自动切换）</span></div>'
             '<div class="lm" aria-label="实时在线地图"></div></div>')
    steps = ""
    if sp.get("steps"):
        steps = '<ol class="msteps">' + "".join(f'<li style="--c:{PAL[c]}"><b>{H.escape(y)}</b>{H.escape(tt)}</li>' for y, tt, c in sp["steps"]) + '</ol>'
    return (f'<figure class="gmap mx" id="map-{k}" data-map="{js}"><div class="gm-bar"><span class="mx-t">🗺️ {t}</span>{tabs}<span class="gm-z"><button data-z="-1" aria-label="缩小">－</button><button data-z="0" aria-label="复位">⟲</button><button data-z="1" aria-label="放大">＋</button></span></div>'
            f'<div class="mx-panes">{cpane}{tpane}{lpane}</div>'
            f'<figcaption>🎨 讲解图／🏔️ 地形图为本站本地 SVG（Natural Earth 公有领域底图），断网也能显示；🌐 实时地图可在 12 个全球底图源间切换，加载失败会自动换源。{H.escape(sp.get("rcap",""))}。点编号或列表可定位地点。</figcaption>{steps}<ol class="gm-leg">{li}</ol></figure>')

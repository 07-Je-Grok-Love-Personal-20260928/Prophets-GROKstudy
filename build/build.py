# -*- coding: utf-8 -*-
import os, json, importlib, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib, layout, maps
OUT = os.path.join(os.path.dirname(__file__), "..", "docs")
MAPS = maps.build(os.path.join(OUT, "assets", "maps"), lib.VER)
lib.MAPS = MAPS
lib.MAP = lambda k: maps.html(k, MAPS, lib.VER)
DESC = {"index": "旧约先知书（以赛亚书—玛拉基书，十七卷）欧陆改革宗深读：时间线、故事线、地图、圣经神学与圣约神学、三项联合信条与三大信经"}
TITLES = {"index": "首页", "bible": "从整本圣经看先知书", "history": "史地与古近东文化", "isaiah": "以赛亚书", "jeremiah": "耶利米书 · 耶利米哀歌", "ezekiel": "以西结书", "daniel": "但以理书",
          "minor1": "亚述时期小先知：何西阿—弥迦", "minor2": "巴比伦时期小先知：那鸿—西番雅", "minor3": "波斯时期小先知：哈该—玛拉基", "confessions": "三项联合信条对照", "creeds": "三大普世信经 · 阅读背诵版",
          "compare": "三大信经深度对比", "memory": "速记与自测", "sources": "来源与核对"}
only = sys.argv[1:]
for slug, _ in layout.PAGES:
    if only and slug not in only: continue
    try: m = importlib.import_module("c_" + slug)
    except ModuleNotFoundError: print("skip", slug); continue
    html = layout.page(slug, TITLES[slug], m.body(), DESC.get(slug, TITLES[slug] + " · 旧约先知书 欧陆改革宗深读"))
    open(os.path.join(OUT, slug + ".html"), "w").write(html); print("wrote", slug, len(html))
os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
if not only:
    json.dump(dict(confessions=lib.USED, bible=sorted(set(lib.VUSED))), open(os.path.join(os.path.dirname(__file__), "data", "quotes_used.json"), "w"), ensure_ascii=False, indent=1)

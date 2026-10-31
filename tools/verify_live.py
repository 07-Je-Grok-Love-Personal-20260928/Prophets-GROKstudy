#!/usr/bin/env python3
"""抽样在线复核：重新抓取 ccifellowship.org 页面，确认本站所用文本仍在网页中逐字出现。"""
import json, re, sys, os, urllib.request, html
from bs4 import BeautifulSoup
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = json.load(open(os.path.join(R, "build", "data", "quotes_used.json")))["confessions"]
def page(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    t = BeautifulSoup(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"), "html.parser")
    for s in t.select("sup"): s.decompose()
    x = t.get_text(""); return re.sub(r"\s+", "", x)
seen = {}; ok = bad = 0; fails = []
for u in U:
    url = u["url"]
    if url not in seen:
        try: seen[url] = page(url)
        except Exception as e: seen[url] = None; print("fetch fail", url, e)
    t = seen[url]
    if t is None: continue
    parts = u.get("parts")
    if not parts:
        import sys as _s; _s.path.insert(0, os.path.join(R, "build")); import lib
        parts = [lib.src(u["doc"], u["n"], u.get("h"))[3]]
    if u["doc"] == "CR" and u["key"].startswith("CR.") and False: pass
    for p in parts:
        if p is None: continue
        if re.sub(r"\s+", "", p) in t: ok += 1
        else: bad += 1; fails.append((u["key"], p[:40]))
CR = json.load(open("/workspace/cci/creeds.json"))
for k, v in CR.items():
    t = seen.get(v["url"]) or page(v["url"])
    for para in v["text"].split("\n\n"):
        if re.sub(r"\s+", "", para) in t: ok += 1
        else: bad += 1; fails.append(("CREED." + k, para[:40]))
print("pages", len(seen), "parts ok", ok, "missing", bad)
for f in fails[:30]: print("  ", f)

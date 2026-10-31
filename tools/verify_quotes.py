#!/usr/bin/env python3
"""发布后核验：解析 docs/*.html，把每条信条/信经/经文引文与 CCI 原始数据逐字比对。"""
import sys, os, re, json, glob
from bs4 import BeautifulSoup
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, "build"))
import lib, bible
CR = json.load(open(lib.CCI + "/creeds.json"))
def src_text(k):
    if k.startswith("CR-intro."):
        t = CR[k[9:]]["intro_text"]; return t[0] if isinstance(t, list) else t, None
    m = re.match(r"(HC|BC|DT)(\d*)\.(\d+)$", k); doc, h, n = m.group(1), m.group(2), int(m.group(3))
    lab, url, q, t = lib.src(doc, n, int(h) if h else None); return t, q
rep = dict(cq=0, crq=0, creed=0, verse=0, fail=[])
for f in sorted(glob.glob(os.path.join(R, "docs", "*.html"))):
    s = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser"); pg = os.path.basename(f)
    for b in s.select("blockquote.cq"):
        k = b["data-k"]; t, q = src_text(k); body = b.select_one(".cq-t").get_text()
        parts = [p for p in body.split("……") if p]
        ok = all(p in t for p in parts) and (body.startswith("……") or t.startswith(parts[0])) and (body.endswith("……") or t.endswith(parts[-1]))
        qq = b.select_one(".cq-q")
        if qq is not None and qq.get_text() != q: ok = False
        rep["cq"] += 1
        if not ok: rep["fail"].append((pg, k, body[:60]))
    for c in s.select("span.crq"):
        k = c["data-cr"]; txt = c.get_text()[1:]; txt = txt[1:-1] if txt.startswith("“") and txt.endswith("”") else txt
        rep["crq"] += 1
        if txt not in CR[k]["text"]: rep["fail"].append((pg, "CR." + k, txt))
    for c in s.select(".creed[data-creed]"):
        k = c["data-creed"]; joined = "\n\n".join("".join(l.get_text() for l in p.select(".ln")) for p in c.select(".cp"))
        rep["creed"] += 1
        if joined != CR[k]["text"]: rep["fail"].append((pg, "CREED." + k, "full text mismatch"))
    for v in s.select("blockquote.vs"):
        ref = re.sub(r"（和合本）.*$", "", v.cite.get_text().replace("📖", "").strip()).strip()
        rep["verse"] += 1
        if v.div.get_text() != bible.verses(ref): rep["fail"].append((pg, ref, "verse mismatch"))
json.dump(rep, open(os.path.join(R, "build", "data", "verify_report.json"), "w"), ensure_ascii=False, indent=1)
print({k: v for k, v in rep.items() if k != "fail"}, "FAIL:", len(rep["fail"]))
for x in rep["fail"]: print("  ", x)
sys.exit(1 if rep["fail"] else 0)

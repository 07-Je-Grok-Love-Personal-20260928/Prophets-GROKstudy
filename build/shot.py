import sys,os
from playwright.sync_api import sync_playwright
pages=sys.argv[1].split(','); ws=[int(x) for x in sys.argv[2].split(',')]; full='--full' in sys.argv
D='/workspace/Prophets-GROKstudy/docs'; O='/workspace/Prophets-GROKstudy/_shots'; os.makedirs(O,exist_ok=True)
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
  for pg_ in pages:
    for w in ws:
      pg=b.new_page(viewport={'width':w,'height':900}); errs=[]
      pg.on('pageerror',lambda e:errs.append(str(e)))
      pg.goto('file://%s/%s.html'%(D,pg_)); pg.wait_for_timeout(400)
      pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))"); pg.wait_for_timeout(700)
      r=pg.evaluate("()=>({sw:document.documentElement.scrollWidth,vw:document.documentElement.clientWidth,h:document.documentElement.scrollHeight})")
      pg.screenshot(path='%s/%s_%d.png'%(O,pg_,w),full_page=full)
      print(pg_,w,r,errs); pg.close()

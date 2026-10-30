from playwright.sync_api import sync_playwright
from pathlib import Path
import json,os
URL=os.environ.get("TARGET_URL","https://pedroalread.github.io/portafolio-pedro-v6-revision/")
results=[]
def ck(name,val):
 results.append((name,bool(val)));print(("PASS" if val else "FAIL"),name,flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
 for w,h in [(2560,1440),(1440,900),(390,844),(320,700)]:
  ctx=b.new_context(viewport={"width":w,"height":h});page=ctx.new_page();errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
  resp=page.goto(URL,wait_until="domcontentloaded",timeout=60000)
  page.wait_for_timeout(850)
  ck(f"{w}: status",resp.status==200)
  ck(f"{w}: 4 featured cases",page.locator(".p6-card").count()==4)
  ck(f"{w}: no horizontal overflow",page.evaluate("document.documentElement.scrollWidth<=innerWidth"))
  ck(f"{w}: no JS errors",len(errors)==0)
  ck(f"{w}: cross-link to laboratory",page.locator('.p6-actions a[href*="laboratorio-de-producto"]').count()==1)
  ck(f"{w}: cross-link to decisions",page.locator('.p6-actions a[href*="sala-de-decisiones"]').count()==1)
  if w==2560:
   ck("Original work cases preserved",page.locator("#proyectos").count()==1)
   ck("Contact link preserved",page.locator('a[href^="mailto:pedro18@gmail.com"]').count()>=1)
   ck("Portfolio source stylesheet loaded",page.evaluate("getComputedStyle(document.querySelector('.p6-section')).backgroundColor !== 'rgba(0, 0, 0, 0)'"))
   Path("qa").mkdir(exist_ok=True);page.screenshot(path="qa/portfolio-v6-qhd.png",full_page=True,timeout=20000)
  if w==390:page.screenshot(path="qa/portfolio-v6-movil.png",full_page=True,timeout=20000)
  ctx.close()
 b.close()
n=sum(x[1] for x in results);Path("qa").mkdir(exist_ok=True);Path("qa/resultado.json").write_text(json.dumps({"url":URL,"passed":n,"total":len(results),"tests":results},ensure_ascii=False,indent=2))
print("RESULT:",n,"/",len(results),flush=True);assert n==len(results)

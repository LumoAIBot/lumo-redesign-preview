import glob,os,json,sys
from playwright.sync_api import sync_playwright
ROOT='/workspace/lumo-redesign-preview'; pages=sorted(os.path.basename(f) for f in glob.glob(ROOT+'/*.html'))
JS=r'''()=>{const out={long:[],btn:{}};const c=document.createElement('canvas').getContext('2d');
for(const e of document.querySelectorAll('main p, main li, main dd, main td, main summary+*')){const s=getComputedStyle(e);if(s.display==='none'||!e.textContent.trim())continue;
 c.font=s.fontSize+' '+s.fontFamily;const cw=c.measureText('abcdefghijklmnopqrstuvwxyz ').width/27;const ch=e.clientWidth/cw;if(ch>80&&e.textContent.length>90)out.long.push([e.tagName,Math.round(ch),e.textContent.trim().slice(0,40)])}
for(const b of document.querySelectorAll('.btn')){const s=getComputedStyle(b),r=b.getBoundingClientRect();if(!r.width)continue;const k=[Math.round(r.height),s.fontSize,s.paddingLeft,b.classList.contains('sm')?'sm':b.classList.contains('ghost')?'ghost':'solid'].join('/');out.btn[k]=(out.btn[k]||0)+1}
return out}'''
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for th in ['dark','light']:
        for w in [390,900,1440]:
            pg=b.new_page(viewport={'width':w,'height':1000});pg.add_init_script(f"localStorage.setItem('lumo-prev-theme','{th}')")
            for n in pages:
                pg.goto('http://localhost:8811/'+n);pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))");pg.wait_for_timeout(250)
                pg.screenshot(path=f'review/{n[:-5]}-{w}-{th}.png',full_page=True)
                if th=='dark': res[f'{n} {w}']=pg.evaluate(JS)
            pg.close()
json.dump(res,open('review/metrics.json','w'),indent=0)
for k,v in res.items():
    if v['long']: print('LONG',k,v['long'][:4])
allb={}
for k,v in res.items():
    for bk,c in v['btn'].items(): allb.setdefault(bk,set()).add(k.split()[1])
print('BUTTON VARIANTS',{k:sorted(v) for k,v in allb.items()})

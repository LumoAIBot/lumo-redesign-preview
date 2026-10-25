"""Overlap/overflow audit for every preview page. Fails (exit 1) on horizontal scroll, elements past the
viewport, text boxes overlapping each other or images, plate captions overlapping the plate, and orrery
labels outside their SVG. Usage: python3 audit.py [base_url] [widths]"""
import sys, glob, os
from playwright.sync_api import sync_playwright
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8811'
ROOT='/workspace/lumo-redesign-preview'
WIDTHS=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else [360,390,430,600,768,900,1024,1280,1440,1920]
JS=r'''()=>{
const vw=document.documentElement.clientWidth,out=[];
if(document.documentElement.scrollWidth>vw+1)out.push('hscroll '+document.documentElement.scrollWidth);
const clipped=e=>{for(let a=e.parentElement;a&&a!==document.body;a=a.parentElement){const o=getComputedStyle(a).overflowX;if(o!=='visible')return true}return false};
const vis=e=>{const s=getComputedStyle(e);if(s.display==='none'||s.visibility==='hidden'||+s.opacity===0)return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
for(const e of document.querySelectorAll('body *')){if(e.id==='sky'||(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')||!vis(e))continue;const s=getComputedStyle(e);if(s.position==='fixed')continue;
 const r=e.getBoundingClientRect();if((r.right>vw+1||r.left<-1)&&!clipped(e))out.push('past-viewport '+e.tagName+'.'+e.className+' '+Math.round(r.left)+'..'+Math.round(r.right))}
const hiddenIn=e=>{const d=e.closest('details');return (d&&!d.open&&!e.closest('summary'))||e.closest('.visually-hidden')};
const texts=[];for(const e of document.querySelectorAll('body *')){if(e.closest('svg,.pv-label,.marquee,.dc-window,.stage,.fig,.menu-p')||!vis(e)||hiddenIn(e))continue;
 for(const n of e.childNodes){if(n.nodeType!==3||!n.textContent.trim())continue;const rg=document.createRange();rg.selectNodeContents(n);for(const r of rg.getClientRects())if(r.width>1)texts.push([e,r])}}
const imgs=[...document.querySelectorAll('img,svg.orrery')].filter(i=>vis(i)&&!i.closest('.marquee,.dc-window,.stage,.fig,.pv-label,.menu-p,.plate')).map(i=>[i,i.getBoundingClientRect()]);
for(const p of document.querySelectorAll('.plate'))if(vis(p))imgs.push([p,p.querySelector('svg.orrery')?p.querySelector('svg.orrery').getBoundingClientRect():p.getBoundingClientRect()]);
const ov=(a,b)=>Math.min(a.right,b.right)-Math.max(a.left,b.left)>2&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>2;
for(let i=0;i<texts.length;i++){const[a,ra]=texts[i];for(let j=i+1;j<texts.length;j++){const[b,rb]=texts[j];if(a===b||a.contains(b)||b.contains(a))continue;if(ov(ra,rb)){out.push('text-overlap "'+a.textContent.trim().slice(0,30)+'" / "'+b.textContent.trim().slice(0,30)+'"');if(out.length>40)return out}}
 for(const[im,ri]of imgs){if(im.contains(a)||a.contains(im))continue;if(ov(ra,ri))out.push('text-on-image "'+a.textContent.trim().slice(0,30)+'" / '+(im.className.baseVal!==undefined?'svg':im.className||im.tagName))}}
for(const p of document.querySelectorAll('.plate')){const s=p.querySelector('svg.orrery'),c=p.querySelector('figcaption');if(!s||!c||!vis(c))continue;const rs=s.getBoundingClientRect(),rc=c.getBoundingClientRect();if(rc.top<rs.bottom-1)out.push('caption-on-plate');
 const rp=p.getBoundingClientRect();if(rp.right>vw+1||rp.left<-1)out.push('plate-past-viewport');
 for(const t of s.querySelectorAll('text')){if(!vis(t))continue;const r=t.getBoundingClientRect();if(r.left<rs.left-.5||r.right>rs.right+.5||r.top<rs.top-.5||r.bottom>rs.bottom+.5)out.push('label-outside-svg '+t.textContent)}}
const mas=[...document.querySelectorAll('img')].filter(i=>vis(i)&&/robot\/|wave-|happy-|salute-|logo/.test(i.getAttribute('src')||'')&&!i.closest('.menu-p,.marquee,.dc-window'));
const grp=new Map();for(const i of mas){const c=i.closest('.h-mini')||i.closest('section.cta')||i.closest('.final-cta,section,figure,article,aside,.card,header,footer,.dash-side,li')||document.body;grp.set(c,(grp.get(c)||0)+1)}
for(const[c,n]of grp)if(n>1)out.push('duplicate-mascot x'+n+' in '+c.tagName+'.'+c.className);
return [...new Set(out)]}'''
pages=sorted(os.path.basename(f) for f in glob.glob(ROOT+'/*.html'))
# (label, context kwargs, ignore meta viewport)
CONFIGS=[(f'w{w}',dict(viewport={'width':w,'height':900}),False) for w in WIDTHS]
if len(sys.argv)<=2:
    CONFIGS+=[('desktopmode-980x2.6',dict(viewport={'width':980,'height':1800},device_scale_factor=2.6,is_mobile=True,has_touch=True),True),
              ('phone412-noviewport',dict(viewport={'width':412,'height':915},device_scale_factor=2.6,is_mobile=True,has_touch=True),True)]
IGN="new MutationObserver(()=>{const m=document.querySelector('meta[name=viewport]');if(m&&m.content!=='width=980')m.setAttribute('content','width=980')}).observe(document,{childList:true,subtree:true})"
fails=0
with sync_playwright() as p:
    b=p.chromium.launch()
    for theme in ['dark','light']:
        for hol in ['off','halloween']:
            for label,kw,ign in CONFIGS:
                c=b.new_context(**kw);pg=c.new_page()
                pg.add_init_script(f"localStorage.setItem('aeth-theme','{theme}');localStorage.setItem('lumo-holiday','{hol}')")
                if ign: pg.add_init_script(IGN)
                for n in pages:
                    pg.goto(f'{BASE}/{n}')
                    if ign: pg.evaluate("()=>{const m=document.querySelector('meta[name=viewport]');if(m)m.setAttribute('content','width=980')}")
                    pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))");pg.wait_for_timeout(100)
                    r=pg.evaluate(JS)
                    if r: fails+=1; print(f'FAIL {theme} {hol} {label} {n}:',r[:8],flush=True)
                c.close()
print('pages',len(pages),'configs',len(CONFIGS)*4,'fails',fails); sys.exit(1 if fails else 0)

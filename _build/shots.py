import sys
from playwright.sync_api import sync_playwright
pages=sys.argv[1].split(','); modes=sys.argv[2].split(',') if len(sys.argv)>2 else ['dark']
with sync_playwright() as p:
    b=p.chromium.launch()
    for pg_ in pages:
        for w,n in[(1440,'desktop'),(390,'mobile')]:
            for t in modes:
                pg=b.new_page(viewport={'width':w,'height':900},device_scale_factor=1)
                pg.add_init_script(f"localStorage.setItem('lumo-prev-theme','{t}')")
                pg.goto(f'http://localhost:8811/{pg_}.html');pg.evaluate('''async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}scrollTo(0,0);document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))}''');pg.wait_for_timeout(1000)
                pg.screenshot(path=f'/workspace/review_oct24/redesign/shots/{pg_}-{n}-{t}.png',full_page=True);pg.close()

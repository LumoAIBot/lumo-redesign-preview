import re, os, shutil, html
from bs4 import BeautifulSoup, Comment
from orrery import orrery, check as orrery_check
SITE='/workspace/site-repo'; OUT='/workspace/lumo-redesign-preview'
INVITE='https://discord.com/oauth2/authorize?client_id=1545140271073722378&permissions=309576723664&scope=bot+applications.commands'
SUPPORT='https://discord.gg/KZjebts36C'; ORI='https://discord.com/users/1022200760018161684'
PAGES={'getting-started':'Get started','features':'Features','starkeepers':'How to play','commands':'Commands','premium':'Premium','faq':'FAQ','changelog':'Changelog','status':'Status','privacy':'Privacy Policy','terms':'Terms of Service','dashboard':'About the dashboard','404':'Lost in space'}
RENAME={'dashboard.html':'dashboard-info.html'}
used=set()
def asset(src):
    src=src.split('?')[0].lstrip('/')
    if src.startswith('assets/') and os.path.exists(f'{SITE}/{src}'):
        os.makedirs(os.path.dirname(f'{OUT}/{src}'),exist_ok=True); shutil.copy(f'{SITE}/{src}',f'{OUT}/{src}'); used.add(src)
    return src
def link(h):
    if not h: return h
    if h.startswith('https://dashboard.lumobot.org'): return 'dashboard-servers.html'
    if h in('/','index.html','./'): return 'index.html'
    m=re.match(r'^/?([a-z0-9-]+\.html)(#.*)?$',h)
    if m: return RENAME.get(m.group(1),m.group(1))+(m.group(2) or '')
    return h
EMOJI=re.compile('[\U0001F000-\U0001FAFF\u2600-\u26FF\u23E9-\u23FA\u2B50\u2728\u2705\u274C\uFE0F\u200d]+')
def clean(node):
    for t in node.find_all(['script','style','svg','noscript']): t.decompose()
    for c in node.find_all(string=lambda s:isinstance(s,Comment)): c.extract()
    for t in node.find_all(class_=re.compile(r'^lang-(only|note)')):
        if 'lang-only-en' not in t.get('class',[]): t.decompose()
    for t in node.find_all(attrs={'aria-hidden':'true'}):
        if t.name in('span','i') and EMOJI.fullmatch(t.get_text(strip=True) or 'x'): t.decompose()
    for s in node.find_all(string=True):
        if EMOJI.search(s): s.replace_with(EMOJI.sub('',s))
    for t in node.find_all(class_='grad'): t.unwrap()
    for t in node.find_all(True):
        if t.name=='img' and t.get('src','').endswith('px/star.png'): t['src']='sparkle.png'
        elif t.name=='img': t['src']=asset(t.get('src','')); t.attrs.pop('fetchpriority',None)
        if t.name in('source','img') and t.get('srcset'): t['srcset']=', '.join(asset(x.strip().split(' ')[0])+(' '+x.strip().split(' ')[1] if ' ' in x.strip() else '') for x in t['srcset'].split(','))
        if t.name=='a':
            t['href']=link(t.get('href'))
            if t['href'] and t['href'].startswith('http'): t['rel']='noopener'
            c=' '.join(t.get('class',[]))
            if 'btn' in c: t['class']=['btn']+(['ghost'] if re.search('ghost|secondary|alt',c) else [])
        for a in list(t.attrs):
            if a.startswith('data-') or a in('style','loading','decoding'): del t[a]
        if 'reveal' in t.get('class',[]): t['class']=[x for x in t['class'] if x!='reveal']
    return node
FIGN=[0]
def figcap(node):
    for st in node.find_all(class_='stage'):
        f=st.find('figure'); lab=(f.get('aria-label') if f else None) or (st.find('img').get('alt') if st.find('img') else '')
        FIGN[0]+=1
        if lab: st.append(BeautifulSoup(f'<p class="mono figcap">Fig. {FIGN[0]}. {html.escape(lab.replace("Illustration of the ","").replace("Illustration of ",""))}</p>','lxml').p)
    return node
def unwrap_wraps(node):
    for t in node.find_all('div',class_=re.compile(r'^(wrap|wrap-mid|section-head|frow|guide-row|table-scroll|faq-layout)$')):
        t.unwrap()
    return node
def inner(t): return ''.join(str(c) for c in t.contents)

THEMEPOP=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'themepop.html')).read()
HEADNAV=[('getting-started.html','Get started',None),('features.html','Features','sparkle.png'),('starkeepers.html','How to play',None),('commands.html','Commands',None),('premium.html','Premium',None),('faq.html','FAQ',None),('dashboard-info.html','Dashboard','moon-full.png')]
def head(title,cls=''):
    return f'''<!doctype html><html lang=en data-theme=dark><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>{title} · Lumo (preview)</title><link rel=icon href=lumo-head.png><link rel=stylesheet href=base.css><script>try{{var t=localStorage.getItem('aeth-theme')||'dark',d=document.documentElement;d.dataset.themePref=t;d.dataset.theme=t=='auto'?(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'):(t=='light'?'light':'dark')}}catch(e){{}}</script></head><body class="{cls}">'''
def site_header(active):
    nav=''.join(f'<a href="{h}"{" aria-current=page" if h==active else ""}>'+(f'<img class="px bob" src={i} width=13 alt="">' if i else '')+f'{l}</a>' for h,l,i in HEADNAV)
    return f'''<header class=top><a class=brand href=index.html><img class=logo-head src=assets/logo.webp width=30 height=30 alt="">Lumo</a><nav class=main-nav>{nav}</nav><div class=hr><a class="btn sm" href="{INVITE}" rel=noopener>Add to Discord</a>'''+THEMEPOP+f'''<details class=menu><summary class=hbtn aria-label=Menu>Menu</summary><div class=menu-p>{"".join(f'<a href="{h}">{l}</a>' for h,l,i in HEADNAV)}<a href="{INVITE}" rel=noopener>Add to Discord</a></div></details></div></header>'''
FOOT=f'''<footer class=colophon><div class=c1><img src=wave-96.webp width=44 alt=""><div><b>Lumo</b><p>A Discord bot with a night sky in it. Made by Oriyi, one person, with help from the support server.</p><p class=mono>This preview is English only.</p></div></div>
<div><p class=mono>Explore</p><a href=getting-started.html>Get started</a><a href=features.html>Features</a><a href=starkeepers.html>How to play</a><a href=commands.html>Commands</a><a href=premium.html>Premium</a><a href=changelog.html>Changelog</a></div>
<div><p class=mono>Help</p><a href=faq.html>FAQ</a><a href=dashboard-info.html>About the dashboard</a><a href="{SUPPORT}" rel=noopener>Support server</a><a href="{ORI}" rel=noopener>Message Ori</a><a href=faq.html#claim>Claim Premium</a></div>
<div><p class=mono>The fine print</p><a href=status.html>Status</a><a href=terms.html>Terms</a><a href=privacy.html>Privacy</a><a href="https://github.com/OniSyris" rel=noopener>@OniSyris</a></div></footer>'''
TAIL='<script src=sky.js></script><div class=pv-label>Preview, not live</div><script src=theme.js></script><script src=assets/lumo-holiday.js></script><script src=mascot.js></script><script src=assets/lumo-stats.js></script><script src=assets/lumo-music.js data-slot=".top .hr .theme-pop" data-src="assets/audio/outer-space-loop.mp3" data-volume="0.16" data-fade="2.5"></script></body></html>'
from moons import moon_svg
MOONROW=''.join(moon_svg(f,w,22,f'r{k}') for k,(f,w) in enumerate([(.22,0),(.6,0),(1,0),(.6,1),(.22,1)]))
ROMAN='I II III IV V VI VII VIII IX X XI XII XIII'.split()
def plate(img,cap,n,size=''):
    if 'robot' not in img and 'wave' not in img: return f'<figure class="fig tilt"><img src="{img}" alt=""><figcaption class=mono>Plate {ROMAN[n]}. {cap}</figcaption></figure>'
    return f'<figure class="plate {size}"><span class=glow></span>{orrery(n*13+3)}<img class=bot src="{img}" alt=""><figcaption class=mono>Plate {ROMAN[n]}. {cap}</figcaption></figure>'

POSE={'getting-started':('assets/robot/salute-192.webp','Lumo, reporting for duty'),'features':('assets/robot/idea-320.webp','Lumo with an idea'),'commands':('assets/robot/working-320.webp','Lumo at the console'),'premium':('assets/robot/money-256.webp','Lumo counting coins'),'faq':('assets/robot/thinking-256.webp','Lumo, thinking it over'),'changelog':('assets/robot/celebrating-256.webp','Lumo after a release'),'privacy':('assets/robot/cool-256.webp','Lumo keeping things private'),'terms':('assets/robot/thumbsup-256.webp','Lumo agreeing to the rules'),'dashboard':('assets/robot/gaming-320.webp','Lumo with the controls'),'404':('assets/robot/confused-384.webp','Lumo, slightly lost'),'starkeepers':('assets/starkeepers-hero-960.webp','A server sky, a few nights in')}
for p in POSE.values(): asset(p[0])

def hero_from(h,name,n):
    clean(h)
    kick=h.find(class_='kicker'); k=kick.get_text(' ',strip=True) if kick else PAGES[name]
    h1=h.find('h1'); t=inner(h1) if h1 else PAGES[name]
    paras=''.join(str(p) for p in h.find_all('p') if 'kicker' not in p.get('class',[]))
    btns=''.join(str(a) for a in h.find_all('a',class_='btn'))
    extra=''
    if name=='premium':
        card=h.find(class_=re.compile('plan|price-card|card'))
        ul=h.find('ul'); big=h.find(class_='big')
        extra=f'<div class=price-tag>{inner(big) if big else ""}</div>{str(ul) if ul else ""}'
    img,cap=POSE[name]
    return f'<section class="hero page-hero"><div><p class=mono>{k}</p><h1>{t}</h1><div class=lede>{paras}</div>{extra}<div class=btns>{btns}</div></div>{plate(img,cap,n)}</section>'

def page(name,n):
    s=BeautifulSoup(open(f'{SITE}/{name}.html'),'lxml'); m=s.find('main')
    layout={'features':'L-alt','starkeepers':'L-chapters','commands':'L-ledger','faq':'L-qa','changelog':'L-diary','privacy':'L-legal','terms':'L-legal','premium':'L-plain','getting-started':'L-steps','dashboard':'L-plain','404':'L-lost'}[name]
    out=[]
    if name in('privacy','terms'):
        lw=m.find(class_='legal-wrap') or m; clean(lw)
        lh=lw.find(class_='legal-head'); img,cap=POSE[name]
        out.append(f'<section class="hero page-hero"><div><p class=mono>The fine print</p>{inner(lh) if lh else ""}</div>{plate(img,cap,n,"small")}</section>')
        summ=lw.find(class_='legal-summary'); toc=lw.find(class_='legal-toc')
        out.append('<div class=legal>'+(f'<aside class=toc><p class=mono>Contents</p>{inner(toc)}</aside>' if toc else '')+'<div class=legal-body>'+(f'<div class=summary>{inner(summ)}</div>' if summ else '')+''.join(str(x) for x in lw.find_all('section',recursive=False))+'</div></div>')
    else:
        h=m.find('header',class_='page-hero')
        if h: out.append(hero_from(h,name,n)); h.decompose()
        FIGN[0]=0; clean(m); figcap(m); unwrap_wraps(m)
        i=0
        for sec in m.find_all(['section','nav','div'],recursive=False):
            if sec.name=='nav':
                out.append(f'<nav class=toc-strip><span class=mono>In this guide</span>{inner(sec)}</nav>'); continue
            if 'cmd-bar' in sec.get('class',[]):
                out.append('<div class=cmd-find><label class=mono for=q>Find a command</label><input id=q type=search placeholder="Try sky, play, or top" autocomplete=off></div>'); continue
            cta='section-cta' in sec.get('class',[])
            if cta:
                out.append(f'<section class=cta><img src=happy-256.webp alt="" width=96><div>{inner(sec)}</div></section>'); continue
            i+=1
            sid=f' id="{sec.get("id")}"' if sec.get('id') else ''
            body=inner(sec)
            num=f'<div class=no>{i:02d}</div>' if layout in('L-alt','L-chapters','L-plain') else ''
            out.append(f'<section class=ed{sid}>{num}<div class=body>{body}</div></section>')
    html_=head(PAGES[name],layout)+site_header(RENAME.get(name+'.html',name+'.html'))+'<main>'+''.join(out)+'</main>'+FOOT
    if name=='commands': html_+='<script>var q=document.getElementById("q");q&&q.addEventListener("input",function(){var v=q.value.toLowerCase();document.querySelectorAll(".cmd").forEach(function(c){c.hidden=v&&c.textContent.toLowerCase().indexOf(v)<0})})</script>'
    return html_+TAIL

REWRITE=[(' colours',' colors'),('Everything Lumo can do','What Lumo does, roughly in order of how much fun it is'),('Small features, big difference','And a pile of smaller things'),('Music that just works','Music, from SoundCloud'),
('Unlock the AI side of your server','Premium: the AI&#8209;powered part of Lumo'),('Questions, answered','Questions people actually asked'),('No surprises','Renewals, plainly'),('Three steps','How to get it')]
for n,name in enumerate([p for p in PAGES if p!='status']):
    fn=RENAME.get(name+'.html',name+'.html'); h=page(name,(n%12)+1)
    if name not in('privacy','terms'):
        for a,b in REWRITE: h=h.replace(a,b)
    open(f'{OUT}/{fn}','w').write(h)
print(len(used),'assets')

# ---------- home ----------
HOME=f'''<section class="hero home"><div><p class=mono>A Discord bot · Starkeepers in beta</p><h1>A night sky that lives in your <em>Discord server.</em></h1>
<div class=lede><p>Every night a new batch of stars turns up. Catch one, keep your watch streak going, and fill in constellations with the rest of your server. Every so often a wild star shows up, and you hunt it down as a team.</p></div>
<div class=btns><a class=btn href="{INVITE}" rel=noopener>Add Lumo to Discord</a><a class="btn ghost" href=starkeepers.html>How to play</a></div>
<p class=mono style="margin-top:16px">Free to add · Nothing to install</p><p class=live-stats data-live-stats hidden aria-label="Lumo right now"><span class=dot></span><span><b data-stat=servers></b><span data-unit=servers>servers</span></span><span><b data-stat=members></b>members</span></p></div>
{plate('wave-512.webp','Lumo, keeper of the night',0)}</section>
<div class=marquee aria-label="A few real Lumo commands"><div class=mq><code>/sky watch</code><img src=sparkle.png alt=""><code>/sky view</code><img src=sparkle.png alt=""><code>/sky hunt</code><img src=sparkle.png alt=""><code>/sky team</code><img src=sparkle.png alt=""><code>/sky boss</code><img src=sparkle.png alt=""><code>/play</code><img src=sparkle.png alt=""><code>/queue view</code><img src=sparkle.png alt=""><code>/game</code><img src=sparkle.png alt=""><code>/slots</code><img src=sparkle.png alt=""><code>/connect4</code><img src=sparkle.png alt=""><code>/rank</code><img src=sparkle.png alt=""><code>/top</code><img src=sparkle.png alt=""><code>/profile</code><img src=sparkle.png alt=""><code>/giveaway start</code><img src=sparkle.png alt=""><code>/poll create</code><img src=sparkle.png alt=""><code>/setup status</code><img src=sparkle.png alt=""><code>/help</code><img src=sparkle.png alt=""><code>/sky watch</code><img src=sparkle.png alt=""><code>/sky view</code><img src=sparkle.png alt=""><code>/sky hunt</code><img src=sparkle.png alt=""><code>/sky team</code><img src=sparkle.png alt=""><code>/sky boss</code><img src=sparkle.png alt=""><code>/play</code><img src=sparkle.png alt=""><code>/queue view</code><img src=sparkle.png alt=""><code>/game</code><img src=sparkle.png alt=""><code>/slots</code><img src=sparkle.png alt=""><code>/connect4</code><img src=sparkle.png alt=""><code>/rank</code><img src=sparkle.png alt=""><code>/top</code><img src=sparkle.png alt=""><code>/profile</code><img src=sparkle.png alt=""><code>/giveaway start</code><img src=sparkle.png alt=""><code>/poll create</code><img src=sparkle.png alt=""><code>/setup status</code><img src=sparkle.png alt=""><code>/help</code><img src=sparkle.png alt=""></div></div>
<section class=ed><div class=no>01</div><div class="body two"><div><h2>One star a night, if you show up.</h2><p>Run <code>/sky watch</code> once a night. Do the three little nightly tasks, keep the streak alive, and check your collection with <code>/sky view</code>. Miss a night and the streak resets, so maybe set a reminder.</p></div><figure class=fig><img src=mysky.webp alt="A player's sky in Lumo"><figcaption class=mono>Fig. 1. Ori's sky, a few weeks in</figcaption></figure></div></section>
<section class=spot-band id=hunts><div><p class=mono>02 · Hunts · Beta</p><h2>Sometimes a star <em>fights back.</em></h2><p>Bring your three best stars to a hunt. Specials charge on the third move, ultimates on the eighth. Win, and the wild star might decide to stay.</p>
<table class=rates><thead><tr><th>Rarity</th><th>Chance it joins you</th></tr></thead><tbody><tr><td>Common</td><td>15%</td></tr><tr><td>Uncommon</td><td>12%</td></tr><tr><td>Rare</td><td>8%</td></tr><tr><td>Radiant</td><td>5%</td></tr><tr><td>Celestial</td><td>3%</td></tr></tbody></table><div class=moonrow aria-hidden=true>{MOONROW}<span class=mono>A full moon makes a won star a little likelier to join</span></div></div><figure class=fig><img src=assets/hunt-battle.webp alt="A star hunt playing out, as Lumo animates it in Discord" width=480 height=360><figcaption class=mono>Fig. 2. A hunt, playing out. Animated by Lumo in Discord.</figcaption></figure></section>
<section class=ed><div class=no>03</div><div class=body><h2>It also does the normal bot stuff.</h2><dl class=ledger>
<dt>Music</dt><dd>SoundCloud in your voice channel, with a queue anyone in the channel can push buttons on.</dd>
<dt>Games &amp; Coins</dt><dd>Blackjack, slots, poker and a few more, all on Lumo Coins. Play money, nothing real.</dd>
<dt>Levels</dt><dd>Chat XP, a <code>/rank</code> card and level roles if you want them.</dd>
<dt>Server tools</dt><dd>Giveaways, polls, a join role, welcome cards, logs, purge, a Void bait channel for spam bots, and a light AutoMod.</dd></dl>
<p style="margin-top:20px"><a href=features.html>See everything on the features page →</a></p></div></section>
<section class=cta><img src=happy-256.webp alt="" width=96><div><span class=kicker>Premium</span><h2>AI-powered chat for the whole server.</h2><p>It can look at pictures, search the web, talk in voice and make images. $4.99 a month per server on Ko-fi, cancel whenever.</p></div><a class=btn href=premium.html>See Premium</a></section>'''
open(f'{OUT}/index.html','w').write(head('Home','L-home')+site_header('index.html')+'<main>'+HOME+'</main>'+FOOT+TAIL)

# ---------- status ----------
STATUS=f'''<section class="hero"><div><p class=mono>Status</p><h1 id=st-h>Checking on Lumo…</h1><div class=lede><p id=st-s>Asking Lumo how it's doing.</p></div>
<dl class="ledger st-facts"><dt>Ping</dt><dd id=st-ping>—</dd><dt>Online since</dt><dd id=st-since>—</dd><dt>Checked</dt><dd id=st-at>—</dd></dl></div>
<figure class="plate small"><span class=glow></span>{orrery(97)}<img id=st-bot class=bot src=assets/robot/thinking-256.webp alt=""><figcaption class=mono>Plate VII. Lumo, right now</figcaption></figure></section>
<section class=ed><div class=no>01</div><div class=body><h2>Parts of Lumo</h2><dl class="ledger parts">
<dt>Discord</dt><dd>Commands, buttons and replies <b class=pill id=p-gw>…</b></dd>
<dt>AI chat</dt><dd>Chat, pictures and voice (Premium) <b class=pill id=p-ai>…</b></dd>
<dt>Music</dt><dd>SoundCloud in voice channels <b class=pill id=p-mu>…</b></dd>
<dt>Dashboard</dt><dd>dashboard.lumobot.org <b class=pill id=p-db>…</b></dd></dl>
<p class=mono style="margin-top:16px">This page checks Lumo live every time you open it.</p></div></section>
<section class=cta><img src=assets/robot/surprised-96.webp alt="" width=72><div><h2>Something not working?</h2><p>Tell us on Discord and Ori will take a look.</p></div><a class=btn href="{SUPPORT}" rel=noopener>Support server</a></section>
<script>
(function(){{var $=function(i){{return document.getElementById(i)}};function set(i,ok,t){{var e=$(i);e.textContent=t;e.className='pill '+(ok?'ok':'bad')}}
fetch('https://dashboard.lumobot.org/api/public/status').then(function(r){{return r.json()}}).then(function(d){{
var up=d.ready&&d.gateway_connected,ai=d.ai=='ok',mu=d.music=='ok';
$('st-h').innerHTML=up?(ai&&mu?'Lumo is <em>online.</em>':'Lumo is <em>partly down.</em>'):(d.gateway_connected===false&&d.started_at?'Lumo is <em>starting.</em>':'Lumo is <em>offline.</em>');
$('st-s').textContent=!up?"Lumo can't reach Discord right now. It usually comes back on its own within a few minutes.":ai&&mu?'Everything is working: commands, music and AI chat.':!ai&&!mu?'Commands work, but AI chat and music are having trouble right now.':!ai?'Most things work, but AI chat is having trouble and may be slow.':'Most things work, but music is having trouble and may not start.';
$('st-bot').src=up?'assets/robot/thumbsup-256.webp':'assets/robot/sleeping-96.webp';
$('st-ping').textContent=d.latency_ms!=null?d.latency_ms+' ms':'—';
$('st-since').textContent=d.started_at?new Date(d.started_at*1000).toLocaleString():'—';
$('st-at').textContent=d.checked_at?new Date(d.checked_at*1000).toLocaleTimeString():'—';
set('p-gw',up,up?'Working':'Down');set('p-ai',ai,ai?'Working':'Trouble');set('p-mu',mu,mu?'Working':'Trouble');set('p-db',true,'Working');
}}).catch(function(){{$('st-h').textContent="Couldn't reach Lumo";$('st-s').textContent='The status check did not answer. Try again in a minute.';['p-gw','p-ai','p-mu','p-db'].forEach(function(i){{$(i).textContent='Unknown'}})}})}})();
</script>'''
for a in['assets/robot/thinking-256.webp','assets/robot/thumbsup-256.webp','assets/robot/sleeping-96.webp','assets/robot/surprised-96.webp']: asset(a)
open(f'{OUT}/status.html','w').write(head('Status','L-status')+site_header('status.html')+'<main>'+STATUS+'</main>'+FOOT+TAIL)

# ---------- dashboard mock ----------
DNAV=[('dashboard.html','Overview'),('dashboard-starkeepers.html','Starkeepers'),('dashboard-features.html','Features'),('dashboard-settings.html','Settings')]
def dash(fn,title,helper,pose,body,server=True):
    side=''.join(f'<a href="{h}"{" class=on" if h==fn else ""}>{l}</a>' for h,l in DNAV)
    side+='<span class=sep></span><span class=off title="Not part of this preview">Reaction roles</span><span class=off title="Not part of this preview">Customize</span><span class=off title="Not part of this preview">Economy</span><a href=dashboard-servers.html>Switch server</a>'
    hdr=f'''<header class="top app"><a class=brand href=index.html><img class=logo-head src=assets/logo.webp width=30 height=30 alt="">Lumo</a><span class="mono crumb">Dashboard{" · The Night Owls" if server else ""} <span class=badge>Beta</span></span><div class=hr><a class="btn sm" href="https://dashboard.lumobot.org" rel=noopener>Open dashboard</a>'''+THEMEPOP+f'''<span class=prof><span class=av>O</span><span class=pn>Oriyi</span></span></div></header>'''
    ph=f'<div class=ph><img src="{pose}" alt="" width=72><div><p class=mono>{"The Night Owls" if server else "Signed in as Oriyi"}</p><h1>{title}</h1><p class=help>{helper}</p></div></div>'
    if server:
        main=f'<div class=app-wrap><aside class=side>{side}</aside><main class=app-main>{ph}{body}</main></div>'
    else: main=f'<main class="app-main solo">{ph}{body}</main>'
    open(f'{OUT}/{fn}','w').write(head(title+' · Dashboard','L-app')+hdr+main+'<footer class=app-foot><a href=privacy.html>Privacy</a> · <a href="'+SUPPORT+'" rel=noopener>Support</a> · <a href=index.html>Back to lumobot.org</a></footer>'+TAIL)
for a in['assets/robot/working-96.webp','assets/robot/wave-96.webp','assets/robot/idea-96.webp','assets/robot/happy-96.webp']: asset(a)
def row(icon,name,desc,on,tag='',delay=0):
    t=f' <span class=badge>{tag}</span>' if tag else ''
    return f'<div class=row><img class="px bob" src={icon} style="animation-delay:{delay}s" alt=""><div><b>{name}{t}</b><p>{desc}</p></div><span class="tg{" on" if on else ""}" role=switch aria-checked={"true" if on else "false"}></span></div>'
dash('dashboard-servers.html','Pick a server','Choose the server you want to set up. Only servers you manage are shown.','assets/robot/wave-96.webp',
 '<div class=servers><a class=srv href=dashboard.html><span class=sav>NO</span><span><b>The Night Owls</b><small>Lumo is here · Manage Server</small></span><span class=go>Open →</span></a><a class=srv href=dashboard.html><span class=sav>SG</span><span><b>Sample guild</b><small>Lumo is here · Administrator</small></span><span class=go>Open →</span></a><a class="srv off" href="'+INVITE+'" rel=noopener><span class=sav>+</span><span><b>Another server</b><small>Lumo isn\'t here yet</small></span><span class=go>Add Lumo</span></a></div><p class="mono note">Server names on this page are placeholders.</p>',server=False)
dash('dashboard.html','Overview','How your server is doing and what to do next.','salute-192.webp',
 '<section class=spot><img src=mysky.webp alt="The server sky"><div><p class=mono>Starkeepers</p><h2>Your server\'s sky</h2><p>The shared night sky your members build together.</p><a class="btn ghost sm" href=dashboard-starkeepers.html>Open Starkeepers</a></div></section>'
 '<h2 class=sec>Setup checklist</h2><p class=help>The same checklist as <code>/setup status</code>: what is set up, what to fix next and the command that fixes it.</p><ol class=check>'
 '<li class=done><b>Welcome channel</b><span>Set</span></li><li class=done><b>Join role</b><span>Set</span></li><li><b>Server logs</b><span>Not set up · <code>/setup logs</code></span></li><li><b>Void bait channel</b><span>Not set up · <code>/setup void</code></span></li></ol>'
 '<h2 class=sec>Usage and plan</h2><dl class="ledger usage"><dt>AI replies today</dt><dd>0 of 100</dd><dt>Images and videos this month</dt><dd>0 of 15</dd><dt>Premium</dt><dd>Not active</dd><dt>House wallet</dt><dd>Placeholder</dd></dl>')
dash('dashboard-features.html','Features','Turn things on or off for this server. Starkeepers, hunts, the observatory and bosses are on by default.','assets/robot/idea-96.webp',
 '<h2 class=sec>Starkeepers <span class=badge>Beta</span></h2><div class=rows>'+row('sparkle.png','Nightly catches','Members catch one star a night with /sky watch.',1)+row('moon-eclipse.png','Hunts','Wild stars appear and the server fights them together.',1,'',.6)+row('moon-full.png','Observatory &amp; bosses','Shared server sky and boss stars.',1,'',1.2)+'</div>'
 '<h2 class=sec>Server</h2><div class=rows>'+row('sparkle.png','Level-up messages &amp; roles','Chat XP and level-up cards. Off until you turn it on.',0,'',.3)+row('sparkle.png','Welcome card','Greet new members with a card and your own words.',1,'',.9)+row('sparkle.png','AutoMod','Light filtering for invite links, scam links and mass mentions.',0,'',1.5)+row('moon-full.png','AI chat','AI-powered chat in the channels you pick.',0,'Premium',2)+'</div>')
dash('dashboard-starkeepers.html','Starkeepers','The shared night sky your members build together. It updates by itself while this page is open.','assets/robot/happy-96.webp',
 '<figure class=fig><img src=assets/starkeepers-sky-1200.webp alt="The server sky with constellations"><figcaption class=mono>Fig. 1. The Night Owls\' sky (sample render)</figcaption></figure><dl class="ledger usage" style="margin-top:28px"><dt>Moon tonight</dt><dd>Placeholder</dd><dt>Tonight\'s server goal</dt><dd>Placeholder</dd><dt>Hunts</dt><dd>On</dd></dl>')
asset('assets/starkeepers-sky-1200.webp')
dash('dashboard-settings.html','Settings','Pick a channel or role from the lists and press Save. Changes apply right away.','assets/robot/working-96.webp',
 '<p class=jump><a href=#welcome>Welcome</a><a href=#autorole>Join role</a><a href=#logs>Server logs</a><a href=#language>Language</a></p>'
 '<section class=set id=welcome><h2>Welcome new members <span class="pill ok">On</span></h2><p class=help>Lumo greets new members in the channel you pick.</p><label>Welcome channel<small>Only channels Lumo can post in are listed.</small><select><option>#welcome</option></select></label><button class="btn sm">Save welcome channel</button></section>'
 '<section class=set id=autorole><h2>Join role <span class="pill bad">Off</span></h2><p class=help>Gives every new member a role automatically when they join.</p><label>Role for new members<small>Only roles below Lumo\'s own role can be handed out, so only those are listed.</small><select><option>Off (no join role)</option></select></label><button class="btn sm">Save join role</button></section>'
 '<section class=set id=logs><h2>Server logs <span class="pill bad">Off</span></h2><p class=help>A private record of what happens in your server, for moderators.</p><label>Log channel<select><option>No log channel yet</option></select></label><button class="btn sm">Save server logs</button></section>'
 '<section class=set id=language><h2>Language</h2><label>Lumo\'s language in this server<select><option>English</option></select></label><button class="btn sm">Save language</button></section>')

import shutil,glob as _g
HERE=os.path.dirname(os.path.abspath(__file__))
for x in ['base.css','theme.js','sky.js']:
    if os.path.exists(os.path.join(HERE,x)): shutil.copy(os.path.join(HERE,x),OUT)
shutil.copytree(os.path.join(HERE,'assets'),OUT+'/assets',dirs_exist_ok=True)
pass  # holiday outfits: option B redrawn waving Lumo for large poses, plain for small (assets/robot/<holiday>/)
CAPFIX=[("A hunt, playing out. Animated by Lumo in Discord.","A hunt playing out in Discord")]
for f in _g.glob(OUT+'/*.html'):
    t=open(f).read()
    for a,b in CAPFIX: t=t.replace(a,b)
    t=re.sub(r'(?:Fig\.\s*\d+|Plate\s+[IVXL]+)\.\s*([\w/])',lambda m:m.group(1).upper(),t)
    t=re.sub(r'src=(["\']?)((?:wave|happy|salute|thinking|idea)-\d+\.webp)',r'src=\1assets/robot/\2',t)
    open(f,'w').write(t)
print('done',len(used))
bad=orrery_check(); assert not bad, bad; print('orrery ok')

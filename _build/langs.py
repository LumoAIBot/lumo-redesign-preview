"""Language pages (es/, pt-br/, ja/) for the preview, plus hreflang, the language switcher and per-page SEO tags.
import warnings; warnings.filterwarnings("ignore")
Runs after build.py. Text is translated by its English with the live site's tables (/workspace/site-repo/i18n/*.json,
the same htmltr.py as lumobot.org); preview-only text is in _build/i18n/<code>.json. Missing keys are listed and fail
the build. Safe to rerun: everything added sits between <!--L--> markers or replaces generated files."""
import json, os, re, sys, html
sys.path.insert(0, '/workspace/site-repo/i18n')
import htmltr
from bs4 import BeautifulSoup
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); SITE = '/workspace/site-repo'; LIVE = 'https://lumobot.org/'
LANGS = {'en': ('', 'English', 'EN'), 'es': ('es/', 'Español', 'ES'), 'pt-BR': ('pt-br/', 'Português (Brasil)', 'PT'), 'ja': ('ja/', '日本語', '日本')}
PAGES = ['index.html', 'features.html', 'commands.html', 'getting-started.html', 'starkeepers.html', 'faq.html', 'premium.html', 'dashboard-info.html', 'status.html', 'changelog.html', '404.html']
EN_ONLY = ['privacy.html', 'terms.html']
LIVEOF = {'dashboard-info.html': 'dashboard.html'}
ONLY_EN = {'en': 'This page is only in English.', 'es': 'Esta página solo está en inglés.', 'pt-BR': 'Esta página só está em inglês.', 'ja': 'このページは英語のみです。'}
CL_NOTE = 'The entries below are in English.'
GLOBE = '<svg class=lang-g viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>'
M = re.compile(r'<!--L-->.*?<!--/L-->', re.S)

def table(code):
    d = json.load(open(f'{SITE}/i18n/{code}.json')); d.pop('_about', None)
    p = f'{HERE}/i18n/{code}.json'
    if os.path.exists(p): x = json.load(open(p)); x.pop('_about', None); d.update(x)
    return d

EMO = re.compile('[\U0001F000-\U0001FAFF\u2600-\u26FF\u23E9-\u23FA\u2B50\u2728\u2705\u274C\uFE0F\u200d]+')
def nrm(s): return re.sub(r'<(\d+)> +', r'<\1>', EMO.sub('', s))
class Look:
    def __init__(s, d):
        s.d = d; s.strip = {}
        for k, v in d.items():
            a = re.fullmatch(r'<1>[^<]*</1> ?([^<>]+)', k); b = re.fullmatch(r'<1>[^<]*</1> ?([^<>]+)', v or '')
            if a and b: s.strip.setdefault(a.group(1).strip(), b.group(1).strip())
        s.norm = {}
        for k, v in d.items():
            if isinstance(v, str): s.norm.setdefault(nrm(k), nrm(v))
    def __contains__(s, k): return s.get(k) is not None
    def get(s, k, default=None):
        d = s.d
        if k in d: return d[k]
        if re.fullmatch(r'/[a-z0-9 ]+', k): return k
        if k in s.strip: return s.strip[k]
        if nrm(k) in s.norm: return s.norm[nrm(k)]
        m = re.fullmatch(r'(<1/>)([^<>{}]+)', k)
        if m and m.group(2) in d: return m.group(1) + d[m.group(2)]
        m = re.fullmatch(r'([^<>{}]+?) (<1>\{1\}</1>)', k)
        if m and m.group(1) in d: return d[m.group(1)] + ' ' + m.group(2)
        m = re.fullmatch(r'([^<>]+) · Lumo \(preview\)', k)
        if m and s.get(m.group(1)): return s.get(m.group(1)) + ' · Lumo (preview)'
        return default
    def items(s): return s.d.items()

def live_url(code, page):
    lp = LIVEOF.get(page, page); return LIVE + LANGS[code][0] + ('' if lp == 'index.html' else lp)

def seo(code, page):
    """description, canonical, Open Graph and Twitter tags, copied from the live page in that language."""
    lp = LIVEOF.get(page, page); f = f'{SITE}/{LANGS[code][0] if page not in EN_ONLY else ""}{lp}'
    s = BeautifulSoup(open(f), 'lxml'); out = []
    for t in s.head.find_all(['meta', 'link']):
        n = t.get('name', '') or t.get('property', ''); r = ' '.join(t.get('rel', []))
        if n == 'description' or n.startswith('og:') or n.startswith('twitter:') or r == 'canonical':
            out.append(str(t).replace('/>', '>'))
    if page not in EN_ONLY and page != '404.html':
        out += [f'<link rel="alternate" hreflang="{c}" href="{live_url(c, page)}">' for c in LANGS] + [f'<link rel="alternate" hreflang="x-default" href="{live_url("en", page)}">']
    return out

def redirect(code, page):
    homes = {c: v[0] for c, v in LANGS.items()}; rel = '' if page == 'index.html' else page; has = 'true' if page in PAGES else 'false'
    root = '' if code == 'en' else '../'
    return ('<script>(function(){var D=' + json.dumps(homes) + ',cur="' + code + '",has=' + has + ',rel="' + rel + '",p=null;try{p=localStorage.getItem("lumo-lang")}catch(e){}'
            'if(!p){if(cur!=="en")return;var n=navigator.languages||[navigator.language||""];for(var i=0;i<n.length;i++){var c=String(n[i]).toLowerCase();'
            'var m=c.indexOf("pt")===0?"pt-BR":c.indexOf("es")===0?"es":c.indexOf("ja")===0?"ja":c.indexOf("en")===0?"en":null;if(m){p=m;break}}if(!p||p==="en")return}'
            'if(p===cur||D[p]===undefined||!has)return;location.replace("' + root + '"+D[p]+(rel||"index.html")+location.search+location.hash)})()</script>')

def switcher(code, page, tr):
    label = tr.get('Language', 'Language'); root = '' if code == 'en' else '../'; items = []
    for c, (d, native, _) in LANGS.items():
        target = page if page in PAGES else 'index.html'
        cur = ' aria-current="true"' if c == code else ''
        items.append(f'<a href="{root}{d}{target}" hreflang="{c}" lang="{c}" data-lang="{c}"{cur}><span translate="no">{native}</span>{"<span class=lang-ck aria-hidden=true>✓</span>" if c == code else ""}</a>')
    return (f'<!--L--><details class="lang-pop"><summary class=lang-btn aria-label="{html.escape(label)}: {LANGS[code][1]}" title="{html.escape(label)}">{GLOBE}<span class="lang-code" translate="no">{LANGS[code][2]}</span></summary>'
            f'<div class="lang-menu"><span class="lang-h">{html.escape(label)}</span>{"".join(items)}</div></details><!--/L-->')

def add_bits(t, code, page, tr):
    t = M.sub('', t)
    head = '<!--L-->' + ''.join(seo(code, page)) + redirect(code, page) + '<!--/L-->'
    t = t.replace('</head>', head + '</head>', 1)
    t = t.replace('<div class="theme-pop">', switcher(code, page, tr) + '<div class="theme-pop">', 1)
    if code != 'en':
        js = {k[3:]: v for k, v in tr.items() if k.startswith('js:')}
        t = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '<!--L--><script type="application/json" id="lumo-t">' + json.dumps(js, ensure_ascii=False).replace('</', '<\\/') + '</script><!--/L-->', t, 1)
    t = re.sub(r'<script src=("?)((?:\.\./)?)assets/lumo-music\.js', lambda m: f'<!--L--><script src="{m.group(2)}assets/lumo-lang.js"></script><!--/L-->' + m.group(0), t, count=1)
    return t

SKIP = re.compile(r'^(?:[a-z]+:|//|/|#|\?|\.\./)', re.I)
def rewrite_urls(t):
    def fix(u):
        if not u or SKIP.match(u): return u
        return u if re.split(r'[?#]', u, 1)[0] in PAGES else '../' + u
    def attr(m):
        name, q, val = m.group(1), m.group(2), m.group(3) if m.group(3) is not None else m.group(4)
        if name == 'srcset': val = ', '.join(' '.join([fix(p.strip().split(' ')[0])] + p.strip().split(' ')[1:]) for p in val.split(','))
        else: val = fix(val)
        return f'{name}="{val}"'
    return re.sub(r'\b(href|src|srcset|poster|data-src|data-rank)=(?:"([^"]*)"|([^\s>"\']+))', lambda m: attr(type('m', (), {'group': lambda s, i: [m.group(0), m.group(1), None, m.group(2), m.group(3)][i]})()), t)

def build_lang(code, page, en, tr, miss):
    src = M.sub('', en)
    if page == 'index.html':
        sys.path.insert(0, HERE); import importlib
        dd = json.load(open(f'{HERE}/demo-data.json'))[code]; dd['ui'] = json.load(open(f'{HERE}/demo_ui.json'))[code]
        src = re.sub(r'<!--demo-data-->.*?<!--/demo-data-->', lambda m: '<!--demo-data--><script type=application/json id=demo-data>' + json.dumps(dd, ensure_ascii=False).replace('</', '<\\/') + '</script><!--/demo-data-->', src, flags=re.S)
        src = src.replace('assets/demo/rank-card-en.webp', f'assets/demo/rank-card-{code.lower()}.webp')
    if page == 'changelog.html':
        src = re.sub(r'(<div class=lede>)', r'\1<p class="lang-note">' + CL_NOTE + '</p>', src, 1)
    for k in htmltr.collect(src):
        if k not in tr and not (page == 'changelog.html' and k.startswith('<1>')): miss.setdefault(k, set()).add(page)
    out = htmltr.translate(src, tr.get, lang=code)
    out = re.sub(r'<html lang=en', f'<html lang={code}', out, 1)
    out = rewrite_urls(out)
    return add_bits(out, code, page, tr)

def main():
    strict = '--strict' in sys.argv
    en_tr = {'Language': 'Language'}; report = {}
    srcs = {p: M.sub('', open(f'{OUT}/{p}').read()) for p in PAGES + EN_ONLY}
    for p in PAGES: open(f'{OUT}/{p}', 'w').write(add_bits(srcs[p], 'en', p, en_tr))
    for p in EN_ONLY:
        t = add_bits(srcs[p], 'en', p, en_tr)
        note = ''.join(f'<span lang="{c}">{v}</span>' for c, v in ONLY_EN.items())
        t = re.sub(r'(<div class=legal-body>)', r'\1<!--L--><p class="lang-note lang-only-en">' + note + '</p><!--/L-->', t, 1)
        open(f'{OUT}/{p}', 'w').write(t)
    for code in LANGS:
        if code == 'en': continue
        tr = Look(table(code)); miss = {}
        os.makedirs(f'{OUT}/{LANGS[code][0]}', exist_ok=True)
        for p in PAGES: open(f'{OUT}/{LANGS[code][0]}{p}', 'w').write(build_lang(code, p, srcs[p], tr, miss))
        report[code] = miss
        print(code, len(miss), 'missing')
    json.dump({c: {k: sorted(v) for k, v in m.items()} for c, m in report.items()}, open('/tmp/missing.json', 'w'), ensure_ascii=False, indent=1)
    if strict and any(report.values()): sys.exit(1)
main()

"""Internal link check: every relative href/src/srcset/data-src on every page (incl. language pages) must exist, and #anchors must exist on the target page."""
import glob, os, re, sys
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); bad = []; ids = {}
files = [f for d in ('', 'es/', 'pt-br/', 'ja/') for f in glob.glob(f'{ROOT}/{d}*.html')] + glob.glob(f'{ROOT}/dashboard-preview/*.html')
def idset(f):
    if f not in ids: ids[f] = {t.get('id') for t in BeautifulSoup(open(f), 'lxml').find_all(id=True)}
    return ids[f]
for f in files:
    s = BeautifulSoup(open(f), 'lxml')
    for t in s.find_all(True):
        for a in ('href', 'src', 'srcset', 'data-src', 'data-rank'):
            v = t.get(a)
            if not v: continue
            for u in ([x.strip().split(' ')[0] for x in v.split(',')] if a == 'srcset' else [v]):
                if re.match(r'^(?:[a-z]+:|//|data:)', u, re.I): continue
                path, _, frag = u.partition('#'); path = path.split('?')[0]
                tgt = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
                if not os.path.exists(tgt): bad.append((os.path.relpath(f, ROOT), u)); continue
                if frag and tgt.endswith('.html') and frag not in idset(tgt): bad.append((os.path.relpath(f, ROOT), u + ' (no anchor)'))
for b in sorted(set(bad)): print('BROKEN', *b)
print('files', len(files), 'broken', len(set(bad))); sys.exit(1 if bad else 0)

"""One mascot per CTA: the live site's .final-cta already carries its own Lumo, so when build.py wraps it in
section.cta (which adds a second Lumo) keep only the inner one and drop the extra wrapper."""
import re
PAT=re.compile(r'<section class=cta><img [^>]*><div>\s*<div class="final-cta">\s*(<img [^>]*class="cta-bot"[^>]*>)(.*?)</div>\s*</div></section>',re.S)
def fix(t): return PAT.sub(lambda m:f'<section class=cta>{m.group(1)}<div>{m.group(2).strip()}</div></section>',t)
if __name__=='__main__':
    import glob
    for f in glob.glob('/workspace/lumo-redesign-preview/*.html'):
        t=open(f).read();n=fix(t)
        if n!=t: open(f,'w').write(n);print('fixed',f)

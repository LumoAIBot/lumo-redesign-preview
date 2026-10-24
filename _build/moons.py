import math
CR=[(-.35,-.3,.22),(.3,.25,.16),(.1,-.5,.11),(-.15,.45,.13),(.45,-.1,.09)]
def lit_path(cx,cy,r,f):
    """lit region for lit fraction f (0..1), lit on the right (waxing)."""
    if f>=.999: return f'M{cx-r:.2f} {cy:.2f}a{r:.2f} {r:.2f} 0 1 0 {2*r:.2f} 0a{r:.2f} {r:.2f} 0 1 0 {-2*r:.2f} 0Z'
    rx=abs(1-2*f)*r; sw=0 if f<.5 else 1
    return f'M{cx:.2f} {cy-r:.2f}A{r:.2f} {r:.2f} 0 0 1 {cx:.2f} {cy+r:.2f}A{rx:.2f} {r:.2f} 0 0 {sw} {cx:.2f} {cy-r:.2f}Z'
def craters(cx,cy,r,fill,op):
    return ''.join(f'<circle cx="{cx+a*r:.2f}" cy="{cy+b*r:.2f}" r="{c*r:.2f}" fill="{fill}" opacity="{op}"/>' for a,b,c in CR)
def moon_svg(f,waning=False,size=22,uid='m'):
    """standalone round moon icon, phase f; fixed square so it never squashes"""
    r=9; c=12; g=f'mg{uid}'; cl=f'mc{uid}'
    lit=lit_path(c,c,r,f)
    t=f' transform="translate(24 0) scale(-1 1)"' if waning else ''
    return (f'<svg class=moon viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true" focusable="false">'
      f'<defs><radialGradient id="{g}"><stop offset=".55" stop-color="#f3dc9a" stop-opacity="{.18+.25*f:.2f}"/><stop offset="1" stop-color="#f3dc9a" stop-opacity="0"/></radialGradient>'
      f'<clipPath id="{cl}"><path d="{lit}"{t}/></clipPath></defs>'
      f'<circle cx="12" cy="12" r="12" fill="url(#{g})"/>'
      f'<circle cx="12" cy="12" r="{r}" class="m-dark"/>{craters(c,c,r,"#000",.18)}'
      f'<g clip-path="url(#{cl})"><circle cx="12" cy="12" r="{r}" fill="#f1e2b4"/>{craters(c,c,r,"#b9a679",.55)}</g>'
      f'<circle cx="12" cy="12" r="{r}" fill="none" class="m-rim"/></svg>')
def orbit_moon(mx,my,r,sun_ang,uid):
    """moon for the orrery: dark disc, sun-facing half lit with a soft terminator, craters, glow"""
    d=math.degrees(sun_ang)
    return (f'<defs><linearGradient id="ol{uid}" x1="0" x2="1"><stop offset=".42" stop-color="#f1e2b4" stop-opacity="0"/><stop offset=".55" stop-color="#f1e2b4"/></linearGradient></defs>'
      f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{r*1.9:.1f}" fill="#f3dc9a" opacity=".12"/>'
      f'<g transform="rotate({d:.1f} {mx:.1f} {my:.1f})"><circle cx="{mx:.1f}" cy="{my:.1f}" r="{r}" fill="#2a2c3a"/>'
      f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{r}" fill="url(#ol{uid})"/>'
      f'{craters(mx,my,r,"#6d6450",.45)}<circle cx="{mx:.1f}" cy="{my:.1f}" r="{r}" fill="none" stroke="#f1e2b4" stroke-opacity=".35" stroke-width=".25"/></g>')

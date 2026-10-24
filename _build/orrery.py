from moons import orbit_moon
"""Hand-built SVG orrery for the hero plates. Lumo is the sun; one body per orbit, no crossings,
periods follow Kepler (T ~ a^1.5), everything turns the same way. check() asserts the clearances."""
import random, math
C=200; LUMO_R=40; HI=186; MIN_GAP=3
CHECK=[]
SHADE='#05060f'
def soft(uid): return f'url(#sf{uid})'
# planet kinds (inner -> outer, like a real system). r = body radius, ext = radial reach incl. rings / moon track
KINDS={
 'rocky':  dict(r=5.8,ext=lambda r:r+1.5),
 'mars':   dict(r=6.5,  ext=lambda r:r+1.5),
 'cloud':  dict(r=7.2,ext=lambda r:r*1.7+2.6+1),   # has a moon
 'gas':    dict(r=11.5, ext=lambda r:r+2),
 'ringed': dict(r=9,ext=lambda r:r*1.9+1),
 'ice':    dict(r=8,ext=lambda r:r+2),
}
def shade(x,y,r,uid,lite):
    a=math.atan2(C-y,C-x)
    return (f'<circle cx="{x+math.cos(a)*r*.4:.1f}" cy="{y+math.sin(a)*r*.4:.1f}" r="{r*.7:.1f}" fill="{lite}" opacity=".25" filter="{soft(uid)}"/>'
            f'<circle cx="{x-math.cos(a)*r*.95:.1f}" cy="{y-math.sin(a)*r*.95:.1f}" r="{r*1.2:.1f}" fill="{SHADE}" opacity=".62" filter="{soft(uid)}"/>')
def wavy(x,y,r,yy,h,col,op,R):
    w=2*r; n=6; pts=[(x-r+w*k/n, yy+R.uniform(-h*.35,h*.35)) for k in range(n+1)]
    d=f'M{x-r:.1f},{yy:.1f} '+' '.join(f'Q{(pts[k][0]+pts[k+1][0])/2:.1f},{pts[k][1]+h*.6:.1f} {pts[k+1][0]:.1f},{pts[k+1][1]:.1f}' for k in range(n))
    d+=f' L{x+r:.1f},{yy+h:.1f} L{x-r:.1f},{yy+h:.1f}Z'
    return f'<path d="{d}" fill="{col}" opacity="{op}"/>'
def body(kind,x,y,r,uid,R):
    g=[];top=''
    if kind=='rocky':
        base,lite,dark='#a8a29a','#e2ddd4','#4d4842'; g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/>')
        for k in range(6):
            cx=x+R.uniform(-.65,.65)*r; cy=y+R.uniform(-.65,.65)*r; cr=R.uniform(.1,.24)*r
            g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{cr:.1f}" fill="{dark}" opacity=".45"/><circle cx="{cx-cr*.3:.1f}" cy="{cy-cr*.3:.1f}" r="{cr*.55:.1f}" fill="{lite}" opacity=".25"/>')
    elif kind=='mars':
        base,lite,dark='#c4673f','#f0a77a','#6b2a16'; g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/>')
        g.append(f'<path d="M{x-r},{y+r*.1} q{r*.6},{-r*.5} {r*1.2},{-r*.1} t{r*.8},{r*.3}" stroke="{dark}" stroke-width="{r*.25:.1f}" fill="none" opacity=".45"/>')
        g.append(f'<ellipse cx="{x}" cy="{y-r*.92:.1f}" rx="{r*.45:.1f}" ry="{r*.16:.1f}" fill="#fff" opacity=".85"/>')
        for k in range(3): g.append(f'<circle cx="{x+R.uniform(-.5,.5)*r:.1f}" cy="{y+R.uniform(-.2,.6)*r:.1f}" r="{r*.12:.1f}" fill="{dark}" opacity=".5"/>')
    elif kind=='cloud':
        base,lite='#2f6fb0','#bfe3ff'; g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/>')
        g.append(f'<path d="M{x-r*.8},{y-r*.2} q{r*.4},{-r*.6} {r*.9},{-r*.1} q{r*.2},{r*.5} {-r*.3},{r*.7} z" fill="#4f9a5a" opacity=".9"/><path d="M{x+r*.1},{y+r*.3} q{r*.5},{-r*.2} {r*.7},{r*.3} q{-r*.3},{r*.4} {-r*.7},{r*.1}z" fill="#6aa65a" opacity=".85"/>')
        g.append(f'<ellipse cx="{x}" cy="{y-r*.93:.1f}" rx="{r*.55:.1f}" ry="{r*.2:.1f}" fill="#fff"/><ellipse cx="{x}" cy="{y+r*.95:.1f}" rx="{r*.45:.1f}" ry="{r*.16:.1f}" fill="#fff" opacity=".9"/>')
        for k in range(3): g.append(f'<path d="M{x-r:.1f},{y+(k-1)*r*.45+R.uniform(-1,1):.1f} q{r*.5},{-r*.25} {r},0 t{r},0" stroke="#fff" stroke-width="{r*.14:.1f}" fill="none" opacity=".55" stroke-linecap="round"/>')
    elif kind=='gas':
        base,lite,dark='#c98f55','#f3d2a2','#7a4a22'; g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/>')
        cols=[lite,dark,'#e0b07a',dark,lite,'#a8683a',lite]
        for k,col in enumerate(cols): g.append(wavy(x,y,r,y-r+k*2*r/len(cols),2*r/len(cols)*.8,col,.55,R))
        sx=x+R.uniform(-.35,.35)*r; sy=y+r*.35
        g.append(f'<ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="{r*.3:.1f}" ry="{r*.17:.1f}" fill="#b2462c"/><ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="{r*.38:.1f}" ry="{r*.24:.1f}" fill="none" stroke="{lite}" stroke-width=".5" opacity=".8"/>')
    elif kind=='ringed':
        base,lite,dark='#d8c28a','#f6e8bd','#8a7340'; g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/>')
        for k in range(5): g.append(wavy(x,y,r,y-r+k*2*r/5,2*r/5*.6,lite if k%2 else dark,.35,R))
    elif kind=='venus':
        base,lite,dark='#e3c98a','#fbefc8','#a8874a'; g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/>')
        for k in range(4): g.append(f'<path d="M{x-r:.1f},{y+(k-1.5)*r*.45:.1f} q{r*.5},{-r*.35} {r},{R.uniform(-.1,.1)*r:.1f} t{r},0" stroke="{lite if k%2 else dark}" stroke-width="{r*.22:.1f}" fill="none" opacity=".45" stroke-linecap="round"/>')
    elif kind=='neptune':
        base,lite,dark='#2f55c8','#9bb6ff','#152a6e'; g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/>')
        for k in range(3): g.append(f'<rect x="{x-r}" y="{y-r*.55+k*r*.45:.1f}" width="{2*r}" height="{r*.14:.1f}" fill="{lite}" opacity=".28"/>')
        g.append(f'<ellipse cx="{x-r*.2:.1f}" cy="{y+r*.25:.1f}" rx="{r*.28:.1f}" ry="{r*.15:.1f}" fill="{dark}" opacity=".9"/><ellipse cx="{x-r*.05:.1f}" cy="{y+r*.12:.1f}" rx="{r*.18:.1f}" ry="{r*.05:.1f}" fill="#fff" opacity=".6"/>')
    elif kind=='ice':
        base,lite,dark='#9fd9df','#e6fbfc','#4f9aa6'; g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/>')
        for k in range(3): g.append(f'<rect x="{x-r}" y="{y-r*.6+k*r*.5:.1f}" width="{2*r}" height="{r*.18:.1f}" fill="{lite}" opacity=".3"/>')
        g.append(f'<ellipse cx="{x}" cy="{y-r*.8:.1f}" rx="{r*.8:.1f}" ry="{r*.35:.1f}" fill="{lite}" opacity=".45"/>')
    g.append(shade(x,y,r,uid,lite))
    return base,lite,''.join(g)
def planet(kind,x,y,r,uid,R,spd,label=''):
    pid=f'{uid}{kind}'; o=[]; base,lite,surf=body(kind,x,y,r,uid,R)
    o.append(f'<defs><clipPath id="c{pid}"><circle cx="{x}" cy="{y}" r="{r}"/></clipPath></defs>')
    ring_back=ring_front=''
    lvl=lambda inner:f'<g class="spin rev" style="animation-duration:{spd}s;transform-origin:{x:.1f}px {y:.1f}px">{inner}</g>'
    if kind=='ringed':
        rc='var(--ring)'
        def rings(clip): return (f'<g clip-path="url(#{clip}{pid})"><ellipse cx="{x}" cy="{y}" rx="{r*1.95:.1f}" ry="{r*.46:.1f}" fill="none" stroke="{rc}" stroke-width="{r*.22:.1f}" opacity=".75"/>'
                                 f'<ellipse cx="{x}" cy="{y}" rx="{r*1.55:.1f}" ry="{r*.37:.1f}" fill="none" stroke="{rc}" stroke-width="{r*.36:.1f}" opacity=".9"/>'
                                 f'<ellipse cx="{x}" cy="{y}" rx="{r*1.22:.1f}" ry="{r*.29:.1f}" fill="none" stroke="{rc}" stroke-width="{r*.12:.1f}" opacity=".35"/></g>')
        o.append(f'<defs><clipPath id="t{pid}"><rect x="{x-r*3}" y="{y-r*2}" width="{r*6}" height="{r*2}"/></clipPath><clipPath id="b{pid}"><rect x="{x-r*3}" y="{y}" width="{r*6}" height="{r*2}"/></clipPath></defs>')
        shadow=f'<g clip-path="url(#c{pid})"><ellipse cx="{x}" cy="{y+r*.3:.1f}" rx="{r*1.6:.1f}" ry="{r*.32:.1f}" fill="none" stroke="{SHADE}" stroke-width="{r*.2:.1f}" opacity=".5"/></g>'
        ring_back=lvl(rings('t')); ring_front=lvl(shadow+rings('b'))
    if kind=='ice':
        o.append(f'<defs><clipPath id="t{pid}"><rect x="{x-r*3}" y="{y-r*3}" width="{r*3}" height="{r*6}"/></clipPath><clipPath id="b{pid}"><rect x="{x}" y="{y-r*3}" width="{r*3}" height="{r*6}"/></clipPath></defs>')
        ur=lambda c:f'<g clip-path="url(#{c}{pid})"><ellipse cx="{x}" cy="{y}" rx="{r*.42:.1f}" ry="{r*1.65:.1f}" fill="none" stroke="#cfeff2" stroke-width=".7" opacity=".7" transform="rotate(-8 {x} {y})"/></g>'
        ring_back=lvl(ur('t')); ring_front=lvl(ur('b'))
    o.append(ring_back)
    o.append(f'<circle cx="{x}" cy="{y}" r="{r+1.3:.1f}" fill="none" stroke="{lite}" stroke-width="1.4" opacity=".3" class="atmo"/>')
    o.append(f'<g clip-path="url(#c{pid})">{surf}</g><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="var(--ink-o)" stroke-width=".5" opacity=".5"/>')
    o.append(ring_front)
    if label: o.append(lvl(f'<text class=plabel x="{x}" y="{y-(r*1.0+3.5):.1f}" text-anchor=middle>{label}</text>'))
    if kind=='cloud':
        mr=r*1.7
        o.append(f'<circle cx="{x}" cy="{y}" r="{mr:.1f}" fill="none" stroke="var(--ink-o)" stroke-width=".4" stroke-dasharray="1 3" opacity=".5"/>'
                 f'<g class="spin" style="animation-duration:13.5s;transform-origin:{x:.1f}px {y:.1f}px"><g class="spin rev" style="animation-duration:13.5s;transform-origin:{x+mr:.1f}px {y:.1f}px">'+orbit_moon(x+mr,y,2.6,math.atan2(200-y,200-x-mr),pid)+'</g></g>')
    return ''.join(o)
# The real solar system, compressed for looks: radius ~ (true radius)^0.4, distance ~ log(AU) then nudged
# apart so nothing touches, period = 21.15 s * years^0.315 (Mercury ~9 s, Neptune ~70 s; every rank kept).
SOL=[('Mercury','rocky',0.383,0.387,0.241),('Venus','venus',0.949,0.723,0.615),('Earth','cloud',1.0,1.0,1.0),('Mars','mars',0.532,1.524,1.881),
     ('Jupiter','gas',11.21,5.203,11.86),('Saturn','ringed',9.45,9.537,29.46),('Uranus','ice',4.01,19.19,84.0),('Neptune','neptune',3.88,30.07,164.8)]
EXTF={'rocky':lambda r:r+1,'venus':lambda r:r+1,'cloud':lambda r:r*1.7+2.6+.8,'mars':lambda r:r+1,'gas':lambda r:r+1.5,'ringed':lambda r:r*1.95+r*.11+.5,'ice':lambda r:r*1.65+.8,'neptune':lambda r:r+1}
def solve(k):
    rs=[k*t**0.4 for _,_,t,_,_ in SOL]; ext=[EXTF[kind](r) for (_,kind,_,_,_),r in zip(SOL,rs)]
    la=[math.log(a) for *_,a,_ in SOL]; lo,hi=LUMO_R,HI
    o=[lo+(hi-lo)*(v-la[0])/(la[-1]-la[0]) for v in la]
    o[0]=max(o[0],lo+MIN_GAP+ext[0])
    for i in range(1,8): o[i]=max(o[i],o[i-1]+ext[i-1]+MIN_GAP+ext[i])
    o[7]=min(o[7],hi-MIN_GAP-ext[7])
    for i in range(6,-1,-1): o[i]=min(o[i],o[i+1]-ext[i+1]-MIN_GAP-ext[i])
    ok=o[0]-ext[0]>=lo+MIN_GAP-1e-9 and all(o[i+1]-ext[i+1]-(o[i]+ext[i])>=MIN_GAP-1e-9 for i in range(7)) and o[7]+ext[7]<=hi-MIN_GAP+1e-9
    return ok,rs,ext,o
def best():
    lo,hi=0.5,12
    for _ in range(40):
        m=(lo+hi)/2
        if solve(m)[0]: lo=m
        else: hi=m
    return solve(lo)
def orrery(seed):
    R=random.Random(seed); uid=f'o{seed}'
    ok,rs,ext,orbit=best(); assert ok
    CHECK.append((seed,[s[0] for s in SOL],list(zip(orbit,ext)),0))
    o=[f'<svg class=orrery viewBox="-14 -14 428 428" aria-hidden="true"><defs><filter id="sf{uid}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="1.2"/></filter></defs>']
    o.append('<g class=rings fill="none" stroke="var(--ink-o)"><circle cx=200 cy=200 r=196 stroke-width=".8" opacity=".55"/>')
    for d in range(0,360,5):
        a=math.radians(d); l=8 if d%30==0 else 4 if d%10==0 else 2.5
        o.append(f'<line x1="{200+math.cos(a)*196:.1f}" y1="{200+math.sin(a)*196:.1f}" x2="{200+math.cos(a)*(196-l):.1f}" y2="{200+math.sin(a)*(196-l):.1f}" stroke-width="{.9 if d%30==0 else .5}" opacity=".7"/>')
    o.append('</g><g class=deg fill="var(--ink-o)" font-family="IBM Plex Mono" font-size="6.5" text-anchor="middle" opacity=".55">')
    for d in range(0,360,30):
        a=math.radians(d-90); o.append(f'<text x="{200+math.cos(a)*204:.1f}" y="{200+math.sin(a)*204+2.3:.1f}">{d}°</text>')
    o.append('</g><g fill="none" stroke="var(--ink-o)">')
    for k,orb in enumerate(orbit): o.append(f'<circle cx=200 cy=200 r={orb:.2f} stroke-width=".5" stroke-dasharray="{["1 3","2 4","4 3","6 3 1 3"][k%4]}" opacity=".45"/>')
    o.append('</g>')
    for (name,kind,_,_,yrs),orb,r in zip(SOL,orbit,rs):
        T=21.15*yrs**0.315; ang=R.uniform(0,360)
        x=round(200+math.cos(math.radians(ang))*orb,2); y=round(200+math.sin(math.radians(ang))*orb,2)
        o.append(f'<g class=spin style="animation-duration:{T:.1f}s">{planet(kind,x,y,round(r,2),uid,R,round(T,1),label=name if kind in ('gas','ringed','ice','neptune') else '')}</g>')
    for k in range(10):
        a=R.uniform(0,6.28); d=R.uniform(212,232) if k%2 else R.uniform(LUMO_R-14,LUMO_R-4); s=R.choice([5,6,8,10,12])
        o.append(f'<image class=twk href="sparkle.png" x="{200+math.cos(a)*d-s/2:.1f}" y="{200+math.sin(a)*d-s/2:.1f}" width="{s}" height="{s}" style="animation-delay:-{R.uniform(0,4):.1f}s"/>')
    o.append('</svg>'); return ''.join(o)
def check():
    bad=[]
    for seed,names,bodies,_ in CHECK:
        edges=[(0,LUMO_R)]+[(o-e,o+e) for o,e in bodies]+[(HI,HI)]
        gs=[edges[i+1][0]-edges[i][1] for i in range(len(edges)-1)]
        if min(gs)<MIN_GAP-1e-6: bad.append((seed,[round(g,1) for g in gs]))
    return bad

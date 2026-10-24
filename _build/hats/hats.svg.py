# hats drawn in a 400x400 box, crown (seat point on Lumo's head) at (200,300), sized for a 265px-wide head.
OUT='#14102a'
FILT='''<filter id="st" x="-20%" y="-20%" width="140%" height="140%"><feMorphology in="SourceAlpha" operator="dilate" radius="9" result="d"/><feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/><feGaussianBlur in="SourceAlpha" stdDeviation="3" result="b"/><feOffset in="b" dy="4" result="o"/><feFlood flood-color="#000" flood-opacity=".25"/><feComposite in2="o" operator="in" result="sh"/><feMerge><feMergeNode in="sh"/><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''
def wrap(body,defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="1200" height="1200"><defs>{FILT}{defs}</defs><g filter="url(#st)" stroke="{OUT}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">{body}</g></svg>'
witch=wrap('''
<ellipse cx="200" cy="296" rx="104" ry="24" fill="url(#wb)"/>
<path d="M150 292 C160 240 172 190 190 150 C202 122 214 104 238 92 C258 84 276 92 282 104 C268 100 252 104 244 118 C232 140 236 200 252 290 Z" fill="url(#wc)"/>
<path d="M153 270 C185 280 220 280 250 268 L253 290 C220 300 185 300 150 290 Z" fill="url(#gold)"/>
<rect x="188" y="268" width="26" height="26" rx="4" fill="none" stroke="#7a5212" stroke-width="5"/>
<path d="M196 150 C186 190 176 230 170 266" fill="none" stroke="#b79cf0" stroke-width="5" stroke-opacity=".55"/>
<path d="M212 232 l3 7 7 1-5 5 1 7-6-4-6 4 1-7-5-5 7-1z" fill="#ffe08a" stroke-width="2.5"/>
<path d="M118 302 C160 316 240 316 282 302" fill="none" stroke="#b79cf0" stroke-width="4" stroke-opacity=".5"/>
''','''<linearGradient id="wc" x1="0" x2="1"><stop offset="0" stop-color="#9c6fe0"/><stop offset=".5" stop-color="#6a3fb8"/><stop offset="1" stop-color="#3b1f73"/></linearGradient>
<linearGradient id="wb" y1="0" y2="1"><stop offset="0" stop-color="#5a33a0"/><stop offset="1" stop-color="#2c1658"/></linearGradient>
<linearGradient id="gold" y1="0" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset=".55" stop-color="#e2a92e"/><stop offset="1" stop-color="#9c6a14"/></linearGradient>''')
pilgrim=wrap('''
<ellipse cx="200" cy="294" rx="108" ry="25" fill="url(#pb)"/>
<path d="M146 290 L156 176 C180 166 220 166 244 176 L254 290 C220 302 180 302 146 290 Z" fill="url(#pc)"/>
<ellipse cx="200" cy="176" rx="44" ry="10" fill="#2e2a3a"/>
<path d="M150 252 C182 262 218 262 250 252 L253 284 C220 296 180 296 147 284 Z" fill="#3a2a18"/>
<rect x="182" y="250" width="36" height="34" rx="3" fill="url(#gold)"/>
<rect x="193" y="260" width="14" height="14" rx="1" fill="#3a2a18" stroke-width="3"/>
<path d="M162 186 L156 240" fill="none" stroke="#6b6680" stroke-width="5" stroke-opacity=".7"/>
<g transform="translate(244 252) rotate(28)"><path d="M0 22 L0 10 C-10 14 -20 10 -22 2 C-15 0 -14 -6 -18 -12 C-10 -10 -6 -14 -6 -22 C-2 -16 2 -16 6 -22 C6 -14 10 -10 18 -12 C14 -6 15 0 22 2 C20 10 10 14 0 10" fill="url(#leaf)" stroke-width="3.5"/><path d="M0 20 L0 -12" fill="none" stroke="#7a2e0e" stroke-width="2.5"/></g>
''','''<linearGradient id="pc" x1="0" x2="1"><stop offset="0" stop-color="#4a4560"/><stop offset=".45" stop-color="#26232f"/><stop offset="1" stop-color="#121018"/></linearGradient>
<linearGradient id="pb" y1="0" y2="1"><stop offset="0" stop-color="#3a3648"/><stop offset="1" stop-color="#131118"/></linearGradient>
<linearGradient id="gold" y1="0" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset=".55" stop-color="#e2a92e"/><stop offset="1" stop-color="#9c6a14"/></linearGradient>
<radialGradient id="leaf" cx=".4" cy=".35"><stop offset="0" stop-color="#ffcf6a"/><stop offset=".5" stop-color="#e9701e"/><stop offset="1" stop-color="#a8360e"/></radialGradient>''')
santa=wrap('''
<path d="M140 284 C142 220 160 168 200 150 C236 134 280 150 300 196 C306 212 304 232 296 246 C290 222 278 206 262 200 C258 230 258 262 262 286 Z" fill="url(#sr)"/>
<path d="M168 182 C160 210 156 244 156 276" fill="none" stroke="#ff8a7a" stroke-width="6" stroke-opacity=".55"/>
<circle cx="296" cy="256" r="22" fill="url(#fur)"/>
<path d="M126 282 C130 264 150 258 166 262 C182 254 200 256 214 262 C230 254 252 256 266 264 C280 260 292 270 290 288 C292 304 276 312 262 306 C246 314 226 312 210 306 C194 314 172 314 158 306 C140 312 122 302 126 282 Z" fill="url(#fur)"/>
<path d="M150 286 q6 -6 12 0 M196 284 q6 -6 12 0 M240 288 q6 -6 12 0 M286 252 q5 -5 10 0" fill="none" stroke="#c9d3e6" stroke-width="3"/>
''','''<linearGradient id="sr" x1="0" x2="1" y1="0" y2=".3"><stop offset="0" stop-color="#ff5a4a"/><stop offset=".5" stop-color="#d81f2a"/><stop offset="1" stop-color="#8e0f1c"/></linearGradient>
<radialGradient id="fur" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".7" stop-color="#eef2f8"/><stop offset="1" stop-color="#c3cde0"/></radialGradient>''')
for n,s in [('halloween',witch),('thanksgiving',pilgrim),('christmas',santa)]: open(n+'.svg','w').write(s)

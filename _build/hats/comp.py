import json,os,math,glob,sys
from PIL import Image
H=json.load(open('heads.json'));SRC='/workspace/site-repo/assets/robot/';OUT=sys.argv[1] if len(sys.argv)>1 else 'out'
K=float(os.environ.get('K','0.80'));DY=float(os.environ.get('DY','10'))
ADJ=json.load(open('adj.json')) if os.path.exists('adj.json') else {}
HS={'halloween':1.0,'thanksgiving':1.08,'christmas':0.94}
hats={n:Image.open(n+'.png').convert('RGBA') for n in ['halloween','thanksgiving','christmas']}
for n,hat in hats.items():
    os.makedirs(f'{OUT}/{n}',exist_ok=True)
    for f,h in H.items():
        a=ADJ.get(f,{})
        src=Image.open(SRC+f).convert('RGBA');S=src.width;Z=float(os.environ.get('Z','0.82'))
        im=Image.new('RGBA',(S,S),(0,0,0,0));sm=src.resize((int(S*Z),int(S*Z)),Image.LANCZOS);ox=int((S-S*Z)/2);oy=S-int(S*Z)-int(S*.01);im.alpha_composite(sm,(ox,oy));u=S*Z/512
        w=min(max(h['w'],240),290);k=K*(w/265)*a.get('s',1)*HS[n]
        ang=a.get('ang',max(-8,min(8,h['ang']*.5)))
        size=int(400*k*u)
        if size<4: continue
        hh=hat.resize((size,size),Image.LANCZOS).rotate(-ang,resample=Image.BICUBIC,center=(size*.5,size*.75))
        cx=ox+(h['x']+a.get('dx',0))*u;cy=oy+(h['y']+DY+a.get('dy',0))*u
        im.alpha_composite(hh,(int(round(cx-size*.5)),int(round(cy-size*.75))))
        im.save(f'{OUT}/{n}/{f}',quality=92)

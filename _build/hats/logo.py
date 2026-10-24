from PIL import Image,ImageDraw
L=Image.open('/workspace/site-repo/assets/logo.webp').convert('RGBA');S=432;D=330
hats={n:Image.open(n+'.png').convert('RGBA') for n in ['halloween','thanksgiving','christmas']}
HS={'halloween':1.0,'thanksgiving':1.08,'christmas':0.94}
for n,hat in hats.items():
    c=Image.new('RGBA',(S,S),(0,0,0,0))
    ox=(S-D)//2;oy=S-D-8
    d=ImageDraw.Draw(c);d.ellipse([ox-7,oy-7,ox+D+7,oy+D+7],fill=(201,165,74,255))
    m=Image.new('L',(D,D),0);ImageDraw.Draw(m).ellipse([0,0,D-1,D-1],fill=255)
    c.paste(L.resize((D,D),Image.LANCZOS),(ox,oy),m)
    k=D/144;u=84*k/265;size=int(400*0.8*u*HS[n]*1.12)
    hh=hat.resize((size,size),Image.LANCZOS)
    cx=ox+72*k;cy=oy+(35+48*84/265)*k
    c.alpha_composite(hh,(int(cx-size*.5),int(cy-size*.75)))
    c.resize((144,144),Image.LANCZOS).save(f'out/logo-{n}.webp',quality=92,lossless=False)
sh=Image.new('RGBA',(3*256+3*48,256),(12,14,30,255))
for i,n in enumerate(hats):
    im=Image.open(f'out/logo-{n}.webp').convert('RGBA');sh.alpha_composite(im.resize((256,256)),(i*256,0))
    sh.alpha_composite(im.resize((36,36),Image.LANCZOS),(768+i*48,20))
sh.save('logos2.png')

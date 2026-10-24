import numpy as np, glob, os, json, math
from PIL import Image, ImageDraw
from scipy import ndimage
fs=sorted(glob.glob('/workspace/site-repo/assets/robot/*.webp'))
out={}
def disk(r):
    y,x=np.ogrid[-r:r+1,-r:r+1];return x*x+y*y<=r*r
for f in fs:
    I=Image.open(f).convert('RGBA').resize((512,512),Image.LANCZOS)
    A=np.asarray(I).astype(int);V=A[...,:3].max(-1)
    dark=(A[...,3]>200)&(V<110)
    m=ndimage.binary_closing(dark,disk(4))
    m=ndimage.binary_fill_holes(m)
    m=ndimage.binary_opening(m,disk(26))
    lab,n=ndimage.label(m)
    if n==0: continue
    sizes=ndimage.sum(m,lab,range(1,n+1));m=lab==(np.argmax(sizes)+1)
    ys,xs=np.nonzero(m);top=ys.min()
    def chord(y):
        r=np.nonzero(m[y])[0];return (r.min(),r.max()) if len(r) else None
    c1=chord(top+18);c2=chord(top+70)
    mid1=(c1[0]+c1[1])/2;mid2=(c2[0]+c2[1])/2
    # tilt: direction from mid2 to mid1
    ang=math.degrees(math.atan2(mid1-mid2,52))
    # crown: top of mask along column mid1
    col=np.nonzero(m[:,int(mid1)])[0];cy=col.min() if len(col) else top
    out[os.path.basename(f)]=dict(x=float(mid1),y=float(cy),w=float(c2[1]-c2[0]),ang=float(ang))
json.dump(out,open('heads.json','w'),indent=0)
for k,v in out.items(): print(k,{a:round(b) for a,b in v.items()})

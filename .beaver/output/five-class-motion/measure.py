from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,json
from collections import deque

root=Path(__file__).parent
def components(mask):
    h,w=mask.shape;seen=np.zeros_like(mask,dtype=bool);out=[]
    for y,x in zip(*np.where(mask)):
        if seen[y,x]:continue
        q=deque([(int(x),int(y))]);seen[y,x]=True;n=0;xs=[];ys=[]
        while q:
            x,y=q.popleft();n+=1;xs.append(x);ys.append(y)
            for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if 0<=nx<w and 0<=ny<h and mask[ny,nx] and not seen[ny,nx]:
                    seen[ny,nx]=True;q.append((nx,ny))
        if n>=30:out.append((n,min(xs),min(ys),max(xs)+1,max(ys)+1))
    return out

def hair(path,cid):
    original=Image.open(path).convert('RGBA');im=original.resize((320,320));a=np.asarray(im).astype(float)
    r,g,b,alpha=[a[:,:,i] for i in range(4)];yy,xx=np.indices(r.shape)
    if cid=='paladin':mask=(r>110)&(g>b*1.06)&(r>=g*.99)&(r-g<90)&(g-b<95)&((r-b)/np.maximum(r,1)<.6)
    elif cid=='dark-knight':mask=(r>40)&(r<160)&(b<r+15)&(g<r+10)&(r-g<28)
    elif cid=='night-lord':mask=(b>r*1.06)&(r>g*1.08)&(b>60)&(r>35)
    else:mask=(r>100)&(g>100)&(b>100)&(np.maximum.reduce([r,g,b])-np.minimum.reduce([r,g,b])<28)
    mask&=(alpha>128)&(yy<205)&(xx>45)&(xx<285)
    closed=Image.fromarray((mask*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    cs=components(np.array(closed)>0)
    cs=[c for c in cs if c[3]-c[1]>25 and c[4]-c[2]>20]
    if not cs:raise ValueError((cid,str(path),'hair not found'))
    # Prefer the broad central head component over narrow weapons or armor.
    best=max(cs,key=lambda c:c[0]/(1+abs((c[1]+c[3])/2-165)/55+max(0,(c[2]+c[4])/2-200)/35))
    return {'bbox':best[1:],'span':(best[3]-best[1])*original.width/320,'componentPixels':best[0]}

def feet(path):
    im=Image.open(path).convert('RGBA');a=np.asarray(im);h,w=a.shape[:2]
    yy,xx=np.indices((h,w));rgb=a[:,:,:3].astype(float);neutral=rgb.max(2)-rgb.min(2)<75
    mask=(a[:,:,3]>128)&neutral&(yy>h*.72)&(xx>w*.31)&(xx<w*.72)
    ys,xs=np.where(mask)
    if not len(xs):return w/2,h*.909
    bottom=int(ys.max());mask&=yy>bottom-h*.045
    ys,xs=np.where(mask)
    return float((xs.min()+xs.max())/2),float(bottom+1)

base={cid:hair(root/'base'/f'{cid}.png',cid) for cid in ['paladin','dark-knight','night-lord','shadower']}
rows=[];corrections={}
for p in sorted((root/'generated').glob('*.json')):
    row=json.loads(p.read_text(encoding='utf-8'));cid=row['id'];src=Path(row['source'])
    if cid=='phantom':continue
    found=hair(src,cid);head=147*found['span']/base[cid]['span'];x,y=feet(src)
    corrections[row['key']]={'head':head,'footX':x,'footY':y,'method':'hair silhouette size matched to approved base; feet lower neutral pixels; visually verify'}
    rows.append({'key':row['key'],'hair':found,'reference':base[cid],'head':head,'feet':[x,y]})
existing=root/'corrections.json'
if existing.exists():
    old=json.loads(existing.read_text(encoding='utf-8'))
    for k,v in old.items():
        if v.get('manual') or k.startswith('phantom--'):corrections[k]=v
existing.write_text(json.dumps(corrections,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'measurements.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('measured',len(rows),'frames; requires visual review')

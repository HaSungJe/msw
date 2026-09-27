from pathlib import Path
from PIL import Image
import json,numpy as np
r=Path(__file__).parent;work=r.parent/'five-class-motion';throw=r.parent/'phantom-joker-throw'
# Reuse only pure measurement functions; do not execute the old generation pipeline.
scope={'__file__':str(work/'measure.py')};exec((work/'measure.py').read_text(encoding='utf-8').split('base={')[0],scope)
hair,feet=scope['hair'],scope['feet']
bases={j['id']:j for p in r.glob('*-base.json') for j in [json.loads(p.read_text(encoding='utf-8'))]}
def hatspan(path):
    a=np.array(Image.open(path).convert('RGBA')).astype(float);h,w=a.shape[:2];yy,xx=np.indices((h,w));red,green,blue,alpha=[a[:,:,i] for i in range(4)]
    m=(alpha>128)&(blue>red*1.15)&(blue>green*1.06)&(yy<h*.53)
    ys,xs=np.where(m);return xs.max()-xs.min()+1
scales={}
for cid,b in bases.items():
    if cid=='phantom':scales[cid]=147/355
    else:scales[cid]=hair(work/'base'/f'{cid}.png',cid)['span']/hair(b['source'],cid)['span']
rows=[]
for cid,b in bases.items():
    for n in [1,2,3]:
        if n!=1 and not (r/f'{cid}-{n}.json').exists():continue
        j=b if n==1 else json.loads((r/f'{cid}-{n}.json').read_text(encoding='utf-8'))
        span=hatspan if cid=='phantom' else lambda p:hair(p,cid)['span']
        scale=scales[cid]*span(b['source'])/span(j['source']);x,y=feet(j['source'])
        rows.append({**j,'skill':'wait','size':576,'scale':scale,'footX':x,'footY':y})
b=bases['phantom']
for n in range(1,7):
    if n not in [1,6] and not (throw/f'throw{n}.json').exists():continue
    j=b if n in [1,6] else json.loads((throw/f'throw{n}.json').read_text(encoding='utf-8'))
    scale=scales['phantom']*hatspan(b['source'])/hatspan(j['source']);x,y=feet(j['source'])
    rows.append({**j,'id':'phantom','n':n,'skill':'joker','size':704,'scale':scale,'footX':x,'footY':y})
(r/'alignment.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('prepared',len(rows),'corrected frames')

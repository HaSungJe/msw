from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
r=Path(__file__).parent
ref=json.loads((r.parent/'phantom-joker-throw/idle-base.json').read_text(encoding='utf-8'))['source']
def span(p):
 a=np.asarray(Image.open(p).convert('RGBA')).astype(float);h,w=a.shape[:2];yy,xx=np.indices((h,w));red,green,blue,alpha=[a[:,:,i] for i in range(4)]
 m=(alpha>128)&(blue>red*1.15)&(blue>green*1.06)&(yy<h*.54);ys,xs=np.where(m);return xs.max()-xs.min()+1
def eyes(p):
 a=np.asarray(Image.open(p).convert('RGBA')).astype(float);h,w=a.shape[:2];yy,xx=np.indices((h,w));red,green,blue,alpha=[a[:,:,i] for i in range(4)]
 m=(alpha>128)&(red>90)&(blue>red*1.03)&(red>green*1.4)&(blue>100)&(yy>h*.43)&(yy<h*.64)&(xx>w*.3)&(xx<w*.69)
 xs=np.where(m.sum(axis=0)>4)[0]
 return int(xs.max()-xs.min()+1)
rows=[]
for p in sorted(r.glob('motion[0-9][0-9].json')):
 j=json.loads(p.read_text(encoding='utf-8'));fix=r/f"fixed-{p.name}"
 if fix.exists():j.update(json.loads(fix.read_text(encoding='utf-8')))
 im=Image.open(j['source']).convert('RGBA');a=np.array(im);h,w=a.shape[:2];rgb=a[:,:,:3].astype(float);yy,xx=np.indices((h,w))
 m=(a[:,:,3]>128)&(rgb.max(2)-rgb.min(2)<75)&(yy>h*.74)&(xx>w*.25)&(xx<w*.88);ys,xs=np.where(m);bottom=int(ys.max());m&=yy>bottom-h*.05;ys,xs=np.where(m)
 scale=(147/355)*eyes(ref)/eyes(j['source']);j.update(scale=scale,footX=float((xs.min()+xs.max())/2),footY=float(bottom+1),size=704,eyeSpan=eyes(j['source']))
 rows.append(j)
(r/'alignment.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print('aligned',len(rows))

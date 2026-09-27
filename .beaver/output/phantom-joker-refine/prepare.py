from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,shutil
r=Path(__file__).parent
def measure(path):
 a=np.asarray(Image.open(path).convert('RGBA')).astype(float);h,w=a.shape[:2];yy,xx=np.indices((h,w));red,green,blue,alpha=[a[:,:,i] for i in range(4)]
 m=(alpha>128)&(red>90)&(blue>red*1.03)&(red>green*1.4)&(blue>100)&(yy>h*.3)&(yy<h*.70)&(xx>w*.20)&(xx<w*.75)
 hist=m.sum(axis=1); row=int(hist.argmax()); m&=(abs(yy-row)<h*.035);xs=np.where(m.sum(axis=0)>max(2,h*.002))[0];eye=int(xs.max()-xs.min()+1)
 rgb=a[:,:,:3];mask=(alpha>128)&(rgb.max(2)-rgb.min(2)<75)&(yy>h*.7)&(xx>w*.2)&(xx<w*.88);ys,xs=np.where(mask);bottom=int(ys.max());mask&=yy>bottom-h*.025;ys,xs=np.where(mask)
 dark=(alpha>128)&(rgb.max(2)<115)&(yy>bottom+1-h*.027)&(yy<bottom+1)
 cols=np.where(dark.sum(0)>h*.004)[0];groups=np.split(cols,np.where(np.diff(cols)>3)[0]+1);groups=[g for g in groups if len(g)>h*.018]
 if len(groups)==2:xs=np.concatenate(groups)
 return {'eye':eye,'footX':float((xs.min()+xs.max())/2),'footY':float(bottom+1),'footSpan':float(xs.max()-xs.min()+1)}
rows=[]
for n in range(1,9):
 j=json.loads((r/f'motion{n:02}.json').read_text());old=measure(r/'previous'/f'motion{n:02}.png');new=measure(j['source']);s=old['eye']/new['eye'];j.update(n=n,scale=s,footX=new['footX'],footY=new['footY'],before=old,after=new,normalizedFootSpan=new['footSpan']*s);rows.append(j)
(r/'alignment.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps([{k:j[k] for k in ['n','scale','before','after','normalizedFootSpan']} for j in rows],indent=2))

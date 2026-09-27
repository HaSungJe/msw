from pathlib import Path
import json
import numpy as np
from PIL import Image
r=Path(__file__).parent
c=json.loads((r/'corrections.json').read_text(encoding='utf-8'))
for key,head in [('paladin--divine-charge--05',260),('paladin--sanctuary--01',250),('paladin--sanctuary--02',230)]:
    c[key].update(head=head,manual=True,method='visual correction of hammer merging with blond hair measurement')
c['paladin--sanctuary--04'].update(footX=700,footY=1180,manual=True)
c['dark-knight--spear-buster--05']['footX']-=35
c['dark-knight--spear-buster--05']['manual']=True
for p in (r/'generated').glob('phantom*.json'):
    j=json.loads(p.read_text(encoding='utf-8'));im=Image.open(j['source']).convert('RGBA');a=np.array(im);h,w=a.shape[:2];yy,xx=np.indices((h,w))
    mask=(a[:,:,3]>128)&(yy>h*.7)&(xx>w*.39)&(xx<w*.65)
    ys,xs=np.where(mask);bottom=int(ys.max());mask&=yy>bottom-h*.04;ys,xs=np.where(mask)
    scale=(576 if j['skill']=='wait' else 704)/w
    if j['key']=='phantom--joker--01':scale*=.72
    c[j['key']]={'head':147/scale,'footX':float((xs.min()+xs.max())/2),'footY':float(bottom+1),'manual':True,'method':'preserve generated scale, align boots; visually reduce oversized corrected preparation frame'}
(r/'corrections.json').write_text(json.dumps(c,indent=2),encoding='utf-8')

from pathlib import Path
import json,re,shutil,hashlib
from PIL import Image,ImageDraw,ImageFont

root=Path(__file__).parent
out=root/'concepts'
out.mkdir(exist_ok=True)
ids=['paladin','dark-knight','night-lord','shadower','phantom']
manifest=[]
for name in ids:
    record=root/f'{name}-generation.json'
    if not record.exists(): continue
    data=json.loads(record.read_text(encoding='utf-8'))
    revision=root/f'{name}-revision.json'
    if revision.exists():
        data=json.loads(revision.read_text(encoding='utf-8'))
    result=data.get('result',{})
    source=data.get('source')
    if not source:
        source=re.search(r'as (C:\\[^\n]+?\.png) by default',result['output_hint'])[1]
    source=Path(source)
    dest=out/f'{name}.png'
    shutil.copy2(source,dest)
    im=Image.open(dest).convert('RGBA')
    assert im.getchannel('A').getextrema()==(0,255), name
    bbox=im.getchannel('A').point(lambda a:255 if a>32 else 0).getbbox()
    # Low-alpha generation noise can touch a canvas edge; report it without
    # altering the generated art. Inspect the visible silhouette separately.
    data.pop('result',None)
    data['source']=str(source)
    data['output']=str(dest)
    record.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    manifest.append({'id':name,'path':str(dest),'size':im.size,'alpha_bbox':bbox,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'status':'review candidate, not game-connected'})
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False))

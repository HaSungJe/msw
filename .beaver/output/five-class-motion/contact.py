from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
root=Path(__file__).parent
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',16)
rows=json.loads((root/'normalized.json').read_text(encoding='utf-8'))
for cid in ['paladin','dark-knight','night-lord','shadower','phantom']:
    items=[r for r in rows if r['id']==cid]
    if not items:continue
    cols=5;cell=280;high=310
    out=Image.new('RGB',(cols*cell,((len(items)+cols-1)//cols)*high),'#e6e6eb')
    d=ImageDraw.Draw(out)
    for k,r in enumerate(items):
        im=Image.open(r['normalized']).convert('RGBA')
        if im.width==576:
            padded=Image.new('RGBA',(704,704));padded.paste(im,(64,128));im=padded
        im.thumbnail((cell,cell))
        x=k%cols*cell;y=k//cols*high
        out.paste(im,(x,y+25),im)
        d.text((x+4,y+3),r['skill']+' '+str(r['n']),font=font,fill='#222633')
    out.save(root/f'{cid}-contact.jpg',quality=95)
print('contact sheets updated')

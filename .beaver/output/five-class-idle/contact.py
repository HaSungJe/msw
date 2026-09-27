from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
r=Path(__file__).parent;project=r.parents[2];font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',18)
names={'paladin':'팔라딘','dark-knight':'다크나이트','night-lord':'나이트로드','shadower':'섀도어','phantom':'팬텀'}
out=Image.new('RGB',(1560,300),'#e5e7ed');d=ImageDraw.Draw(out)
paths=[('기준 비숍',project/'assets/design/characters/bishop/frames/wait/motion01.png')]+[(name,r/'normalized'/cid/'wait/motion01.png') for cid,name in names.items()]
for k,(name,p) in enumerate(paths):
    im=Image.open(p).convert('RGBA');im.thumbnail((260,260));out.paste(im,(k*260,35),im);d.text((k*260+8,5),name,font=font,fill='#222633')
out.save(r/'idle-comparison.jpg',quality=95)
rows=json.loads((r/'alignment.json').read_text(encoding='utf-8'))
for cid,name in names.items():
    chosen=[j for j in rows if j['id']==cid];out=Image.new('RGB',(280*3,310*((len(chosen)+2)//3)),'#e5e7ed');d=ImageDraw.Draw(out)
    for k,j in enumerate(chosen):
        im=Image.open(j['normalized']).convert('RGBA')
        if im.width==576:
            bg=Image.new('RGBA',(704,704));bg.paste(im,(64,128));im=bg
        im.thumbnail((280,280));x=k%3*280;y=k//3*310;out.paste(im,(x,y+30),im);d.text((x+5,y+3),f"{name} {j['skill']} {j['n']}",font=font,fill='#222633')
    out.save(r/f'{cid}-contact.jpg',quality=95)
print('comparison and frame sheets saved')

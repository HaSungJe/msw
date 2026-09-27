from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
r=Path(__file__).parent;rows=json.loads((r/'alignment.json').read_text(encoding='utf-8'));out=Image.new('RGB',(1280,360*((len(rows)+3)//4)),'#e5e7ed');d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',17)
for k,j in enumerate(rows):
 im=Image.open(j['normalized']).convert('RGBA');im.thumbnail((320,320));x=k%4*320;y=k//4*360;out.paste(im,(x,y+30),im);d.text((x+8,y+6),f"{j['n']:02} {j['title']}",font=font,fill='#202633')
out.save(r/'contact.jpg',quality=95);print('contact saved')

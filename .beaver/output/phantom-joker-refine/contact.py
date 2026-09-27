from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
r=Path(__file__).parent;rows=json.loads((r/'alignment.json').read_text());font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',18)
out=Image.new('RGB',(1280,720),'#e5e7ed');d=ImageDraw.Draw(out)
for k,j in enumerate(rows):
 im=Image.open(j['normalized']).convert('RGBA');im.thumbnail((320,320));x=k%4*320;y=k//4*360;out.paste(im,(x,y+30),im);d.text((x+8,y+6),f'{k+1:02} 다리 간격·반동 수정',font=font,fill='#202633')
out.save(r/'contact.jpg',quality=95);out.save(r.parent/'phantom-joker-video/contact.jpg',quality=95)
compare=Image.new('RGB',(1280,720),'#e5e7ed');d=ImageDraw.Draw(compare)
for i,n in enumerate([2,4,5,7]):
 for row,folder,label in [(0,'previous','이전'),(1,'normalized','수정')]:
  im=Image.open(r/folder/f'motion{n:02}.png').convert('RGBA');im.thumbnail((320,320));compare.paste(im,(i*320,row*360+30),im);d.text((i*320+8,row*360+6),f'{n:02} {label}',font=font,fill='#202633')
compare.save(r/'comparison.jpg',quality=95)

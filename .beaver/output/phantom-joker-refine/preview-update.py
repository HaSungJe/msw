from pathlib import Path
import shutil
r=Path(__file__).parent;dest=r.parent/'phantom-joker-video';p=dest/'preview.py';text=p.read_text(encoding='utf-8')
shutil.copyfile(p,r/'previous-preview.py')
text=text.replace("'gameIntegration':False}","'gameIntegration':False,'cardDisplaySize':[72,108],'ringDisplaySize':[158,158],'projectileSprite':'assets/design/effects/phantom-joker/card.png','ringSprite':'assets/design/effects/phantom-joker/ring.png'}")
text=text.replace('영상의 팔 동작과 카드 연사를 참고한 수정본. 몸 회전은 제외했습니다.', '다리 간격과 무릎·상체 반동을 조정했습니다. 큰 카드와 원형 소용돌이는 각각 별도 이미지입니다.')
text=text.replace('card=new Image();','card=new Image(),ring=new Image();').replace("card.src='card.png';", "card.src='card.png';ring.src='ring.png';")
start=text.index("c.strokeStyle='#ffe5bacc'");end=text.index('c.restore()}}',start)
text=text[:start]+"c.save();c.rotate(age*5+phase);if(ring.complete&&ring.naturalWidth)c.drawImage(ring,-79,-79,158,158);c.restore();c.rotate(-age*8+phase*.3);let w=72*(.6+.4*Math.abs(Math.cos(age*7+phase)));c.drawImage(card,-w/2,-54,w,108);"+text[end:]
text=text.replace("card=Image.open(r/'card.png').convert('RGBA');frames=[]", "card=Image.open(r/'card.png').convert('RGBA');ring=Image.open(r/'ring.png').convert('RGBA').resize((119,119),Image.Resampling.LANCZOS);frames=[]")
start=text.index("  fx=Image.new('RGBA',(110,110))");end=text.index("\n frames.append",start)
text=text[:start]+'''  fx=Image.new('RGBA',(180,180));halo=ring.rotate(-math.degrees(age*5+phase),resample=Image.Resampling.BICUBIC,expand=True);halo.putalpha(halo.getchannel('A').point(lambda a:int(a*fade)));fx.alpha_composite(halo,((180-halo.width)//2,(180-halo.height)//2))
  cw=max(1,int(72*scale*(.6+.4*abs(math.cos(age*7+phase)))));sprite=card.resize((cw,81),Image.Resampling.LANCZOS).rotate(math.degrees(age*8-phase*.3),resample=Image.Resampling.BICUBIC,expand=True);sprite.putalpha(sprite.getchannel('A').point(lambda a:int(a*fade)));fx.alpha_composite(sprite,((180-sprite.width)//2,(180-sprite.height)//2));out.alpha_composite(fx,(round(x)-90,round(y)-90))'''+text[end:]
p.write_text(text,encoding='utf-8')
for n in range(1,9):shutil.copyfile(r/'normalized'/f'motion{n:02}.png',dest/'normalized'/f'motion{n:02}.png')
for name in ['card.png','ring.png','alignment.json']:shutil.copyfile(r/name,dest/name)
print('preview inputs updated')

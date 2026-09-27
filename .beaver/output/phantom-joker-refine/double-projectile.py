from pathlib import Path
import json
project=Path('C:/workspace/msw');r=project/'.beaver/output/phantom-joker-video'
p=r/'preview.py';s=p.read_text(encoding='utf-8')
changes=[("'cardDisplaySize':[144,216]","'cardDisplaySize':[288,432]"),("'ringDisplaySize':[316,316]","'ringDisplaySize':[632,632]"),('c.drawImage(ring,-158,-158,316,316)','c.drawImage(ring,-316,-316,632,632)'),('let w=144*','let w=288*'),('c.drawImage(card,-w/2,-108,w,216)','c.drawImage(card,-w/2,-216,w,432)'),('resize((237,237)','resize((474,474)'),('int(144*scale*','int(288*scale*'),('card.resize((cw,162)','card.resize((cw,324)'),('(360,360)','(720,720)'),('(360-halo.width)','(720-halo.width)'),('(360-halo.height)','(720-halo.height)'),('(360-sprite.width)','(720-sprite.width)'),('(360-sprite.height)','(720-sprite.height)'),('(round(x)-180,round(y)-180)','(round(x)-360,round(y)-360)')]
for a,b in changes:
 assert a in s,a
 s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
for p in [project/'assets/design/characters/phantom/motion.json',project/'.beaver/output/five-class-motion/manifest.json']:
 data=json.loads(p.read_text(encoding='utf-8'));items=data if isinstance(data,list) else [data]
 for item in items:
  if item['id']=='phantom':item.update(projectileDisplaySize=[288,432],ringDisplaySize=[632,632])
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
p=r/'install.py';s=p.read_text(encoding='utf-8').replace('projectileDisplaySize=[144,216]','projectileDisplaySize=[288,432]').replace('ringDisplaySize=[316,316]','ringDisplaySize=[632,632]').replace("'cardDisplaySize':[144,216]","'cardDisplaySize':[288,432]").replace("'ringDisplaySize':[316,316]","'ringDisplaySize':[632,632]");p.write_text(s,encoding='utf-8')
p=r/'verification.json';data=json.loads(p.read_text(encoding='utf-8'));data.update(cardDisplaySize=[288,432],ringDisplaySize=[632,632],cardSizePrevious=[144,216],ringSizePrevious=[316,316],cardDisplayScaleChange=2);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
p=project/'docs/design/phantom-joker-motion.md';s=p.read_text(encoding='utf-8').replace('최신 사용자 요청으로 카드 표시 크기만 72×108에서 144×216으로 2배 확대했다.','최신 사용자 요청으로 승인된 카드·고리 외형 비율을 유지하며 카드 표시 크기를 144×216에서 288×432로 다시 2배 확대했다.').replace('고리도 316×316으로 확대했다.','고리도 카드에 맞춰 316×316에서 632×632로 다시 2배 확대했다.');p.write_text(s,encoding='utf-8')
for name in ['.info/character.md','.info/motion.md','.info/skill.md','.beaver/memory/MEMORY.md','docs/design/five-class-motion.md','docs/design/five-class-idle.md']:
 p=project/name;s=p.read_text(encoding='utf-8').replace('144×216(직전 72×108의 2배)','288×432(직전 144×216의 2배)').replace('144×216','288×432') if name.startswith('docs/') else p.read_text(encoding='utf-8').replace('144×216(직전 72×108의 2배)','288×432(직전 144×216의 2배)')
 s=s.replace('316×316','632×632');p.write_text(s,encoding='utf-8')
print('card and ring doubled together; motion and flight unchanged')

from pathlib import Path
import json
project=Path('C:/workspace/msw');r=project/'.beaver/output/phantom-joker-video'
p=r/'preview.py';s=p.read_text(encoding='utf-8')
for a,b in [("'cardDisplaySize':[72,108]","'cardDisplaySize':[144,216]"),('let w=72*','let w=144*'),('c.drawImage(card,-w/2,-54,w,108)','c.drawImage(card,-w/2,-108,w,216)'),('int(72*scale*','int(144*scale*'),('card.resize((cw,81)','card.resize((cw,162)'),('(180,180)','(240,240)'),('(180-halo.width)','(240-halo.width)'),('(180-halo.height)','(240-halo.height)'),('(180-sprite.width)','(240-sprite.width)'),('(180-sprite.height)','(240-sprite.height)'),('(round(x)-90,round(y)-90)','(round(x)-120,round(y)-120)')]:
 assert a in s,a
 s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
for p in [project/'assets/design/characters/phantom/motion.json',project/'.beaver/output/five-class-motion/manifest.json']:
 data=json.loads(p.read_text(encoding='utf-8'));items=data if isinstance(data,list) else [data]
 for item in items:
  if item['id']=='phantom':item['projectileDisplaySize']=[144,216]
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
p=r/'install.py';s=p.read_text(encoding='utf-8').replace('projectileDisplaySize=[72,108]','projectileDisplaySize=[144,216]').replace("'cardDisplayScaleChange':1.5","'cardDisplayScaleChange':2,'cardDisplaySize':[144,216],'ringDisplaySize':[158,158]");p.write_text(s,encoding='utf-8')
p=r/'verification.json';data=json.loads(p.read_text(encoding='utf-8'));data.update(cardDisplayScaleChange=2,cardDisplaySize=[144,216],ringDisplaySize=[158,158],cardSizePrevious=[72,108]);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
p=project/'docs/design/phantom-joker-motion.md';s=p.read_text(encoding='utf-8').replace('표시 크기는 기존 48×72에서 72×108로 1.5배 확대했다.','최신 사용자 요청으로 카드 표시 크기만 72×108에서 144×216으로 2배 확대했다. 원본 카드 PNG와 캐릭터 모션·비행 속도·간격은 그대로다.').replace('각 카드에 158×158 크기의','고리는 기존과 같은 158×158 크기의');p.write_text(s,encoding='utf-8')
for name in ['.info/character.md','.info/motion.md','.info/skill.md','.beaver/memory/MEMORY.md']:
 p=project/name;s=p.read_text(encoding='utf-8').replace('미리보기 카드 표시 크기 72×108(기존의 1.5배), 고리 158×158','미리보기 카드 표시 크기 144×216(직전 72×108의 2배), 고리 158×158 유지');p.write_text(s,encoding='utf-8')
for name in ['docs/design/five-class-motion.md','docs/design/five-class-idle.md']:
 p=project/name;s=p.read_text(encoding='utf-8').replace('카드 표시 1.5배 확대.','카드 표시 144×216(직전의 2배), 고리는 158×158 유지.').replace('카드 표시 크기는 이전의 1.5배다.','카드 표시 크기는 144×216으로 직전의 2배이며 고리는 158×158을 유지한다.');p.write_text(s,encoding='utf-8')
print('card display doubled; ring and motion unchanged')

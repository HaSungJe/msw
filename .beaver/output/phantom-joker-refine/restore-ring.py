from pathlib import Path
import json
project=Path('C:/workspace/msw');r=project/'.beaver/output/phantom-joker-video'
p=r/'preview.py';s=p.read_text(encoding='utf-8')
for a,b in [("'ringDisplaySize':[158,158]","'ringDisplaySize':[316,316]"),('c.drawImage(ring,-79,-79,158,158)','c.drawImage(ring,-158,-158,316,316)'),('resize((119,119)','resize((237,237)'),('(240,240)','(360,360)'),('(240-halo.width)','(360-halo.width)'),('(240-halo.height)','(360-halo.height)'),('(240-sprite.width)','(360-sprite.width)'),('(240-sprite.height)','(360-sprite.height)'),('(round(x)-120,round(y)-120)','(round(x)-180,round(y)-180)')]:
 assert a in s,a
 s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
for p in [project/'assets/design/characters/phantom/motion.json',project/'.beaver/output/five-class-motion/manifest.json']:
 data=json.loads(p.read_text(encoding='utf-8'));items=data if isinstance(data,list) else [data]
 for item in items:
  if item['id']=='phantom':item['ringDisplaySize']=[316,316]
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
p=r/'install.py';s=p.read_text(encoding='utf-8').replace('ringDisplaySize=[158,158]','ringDisplaySize=[316,316]').replace("'ringDisplaySize':[158,158]","'ringDisplaySize':[316,316]");p.write_text(s,encoding='utf-8')
p=r/'verification.json';data=json.loads(p.read_text(encoding='utf-8'));data.update(ringDisplaySize=[316,316],ringSizePrevious=[158,158],ringVisibilityFix='same proportional enlargement as card');p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
p=project/'docs/design/phantom-joker-motion.md';s=p.read_text(encoding='utf-8').replace('고리는 기존과 같은 158×158 크기의','카드 확대 뒤 기존 고리가 가려지는 문제를 수정하여, 고리도 316×316으로 확대했다. 각 카드에는 이 크기의');p.write_text(s,encoding='utf-8')
for name in ['.info/character.md','.info/motion.md','.info/skill.md','.beaver/memory/MEMORY.md','docs/design/five-class-motion.md','docs/design/five-class-idle.md']:
 p=project/name;s=p.read_text(encoding='utf-8').replace('고리 158×158 유지','고리 316×316(카드에 가려지지 않도록 함께 확대)').replace('고리는 158×158 유지','고리는 316×316으로 함께 확대').replace('고리는 158×158을 유지한다','고리도 316×316으로 확대해 카드 바깥으로 보이게 한다');p.write_text(s,encoding='utf-8')
print('ring scaled proportionally to 316; card remains 144 x 216')

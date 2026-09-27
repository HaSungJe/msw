from pathlib import Path
import json, hashlib, shutil
root=Path('C:/workspace/msw')
out=root/'.beaver/output/five-class-portraits-phantom'
rows=[]
for folder,count in [('wait',3),('joker',8)]:
 for n in range(1,count+1):
  p=root/f'assets/design/characters/phantom/frames/{folder}/motion{n:02}.png'
  rows.append({'key':f'phantom/{folder}/{n:02}','file':str(p),'name':f'RtsPhantom_{folder}{n:02}'})
for effect in ['card','ring']:
 rows.append({'key':f'phantom/{effect}','file':str(root/f'assets/design/effects/phantom-joker/{effect}.png'),'name':f'RtsPhantom_{effect}'})
for row in rows:
 data=Path(row['file']).read_bytes();row.update(size=len(data),sha256=hashlib.sha256(data).hexdigest())
(out/'upload-files.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
for name in ['RtsJobTableLogic','RtsSkillFxLogic']:
 shutil.copy2(root/f'RootDesk/MyDesk/{name}.mlua',out/f'{name}.before.mlua')
prompts=json.loads((out/'prompts.json').read_text())
for p in prompts:
 p['referenceHashes']={r:hashlib.sha256(Path(r).read_bytes()).hexdigest() for r in p['refs']}
(out/'prompts.json').write_text(json.dumps(prompts,indent=2),encoding='utf-8')
shutil.copy2(root/'.beaver/output/night-lord-shadower-motion/upload-pngs.py',out/'upload-pngs.py')
print(json.dumps(rows))

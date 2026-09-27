from pathlib import Path
import json,shutil,hashlib,re
root=Path(__file__).parent
assets=Path('assets/design/characters/dark-knight/frames/spear-buster')
resources=json.loads((root/'resource-manifest.json').read_text(encoding='utf-8'))
ruid={r['n']:r['ruid'] for r in resources}
ruid[1]=ruid[2];ruid[8]=ruid[6]
orders={'dkBuster':list(range(1,9)),'dkGiantBuster':[1,2,3,4,5,6,7,2,3,4,5,6,7,8]}
backup=root/'before';backup.mkdir(exist_ok=True)
for n in range(1,9):
 p=assets/('motion%02d.png'%n);shutil.copyfile(p,backup/p.name)
 sourceN=2 if n==1 else 6 if n==8 else n
 shutil.copyfile(root/'normalized'/('motion%02d.png'%sourceN),p)
code=Path('RootDesk/MyDesk/RtsJobTableLogic.mlua'); data=code.read_bytes();(backup/'RtsJobTableLogic.mlua').write_bytes(data)
s=data.decode('utf-8').replace('\r\n','\n')
for action,order in orders.items():
 pattern=r'('+action+r' = \{ )"[^\n]+?( \},)'
 values=', '.join('"'+ruid[n]+'"' for n in order)
 s,count=re.subn(pattern,lambda m:m[1]+values+m[2],s,count=1)
 assert count==1,action
code.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
current=[]
for n in range(1,9):
 p=assets/('motion%02d.png'%n)
 current.append({'n':n,'key':'dark-knight/frames/spear-buster/'+p.name,'file':str(p.resolve()),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'ruid':ruid[n]})
(root/'applied-frames.json').write_text(json.dumps(current,indent=2),encoding='utf-8')
for file in ['assets/design/characters/dark-knight/motion.json','.beaver/output/five-class-motion/manifest.json']:
 p=Path(file);j=json.loads(p.read_text(encoding='utf-8'));items=j if isinstance(j,list) else [j]
 for item in items:
  if item['id']!='dark-knight':continue
  item['revision']='spear-buster-up-down-front-body-lunge'
  item['attackCanvasBySkill']={'spear-buster':832,'dragon-roar':704}
  item['attackFeetBySkill']={'spear-buster':[416,768],'dragon-roar':[352,640]}
  for f in item['frames']:
   if '/spear-buster/' in f['file']:
    n=int(Path(f['file']).stem[-2:]);r=current[n-1]
    f.update(sha256=r['sha256'],ruid=r['ruid'],width=832,height=832)
  for c in item.get('runtimeActions',[]):
   if c['action'] in orders:
    c['order']=orders[c['action']]
    c['files']=['assets/design/characters/dark-knight/frames/spear-buster/motion%02d.png'%n for n in c['order']]
    c['poseOrder']='upper-lower-front' if c['action']=='dkBuster' else 'upper-lower-front-upper-lower-front'
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
planpath=Path('.beaver/output/paladin-dark-knight-motion/connection-plan.json');plan=json.loads(planpath.read_text(encoding='utf-8'))
for c in plan['connections']:
 if c['action'] in orders:
  c['order']=orders[c['action']];c['files']=['assets/design/characters/dark-knight/frames/spear-buster/motion%02d.png'%n for n in c['order']]
  c['revision']='upper-lower-front-body-lunge'
planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(root/'upload-requests.private.json').unlink()
print('Applied 6 new RUIDs to 8 frame files; giant repeats upper/lower/front twice; timings preserved.')

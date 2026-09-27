from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
work=Path(__file__).parent
action={'night-lord':{'wait':'stand1','quadruple-throw':'nlThrow'},'shadower':{'wait':'stand1','savage-blow':'shadSavage','meso-explosion':'shadMeso','blade-tornado-karma-fury':'shadDualblade'}}
rows=[];connections=[];tiles=[]
for folder in action:
 base=Path('assets/design/characters')/folder
 j=json.loads((base/'motion.json').read_text(encoding='utf-8'))
 for p in sorted((base/'frames').glob('*/*.png')):
  im=Image.open(p);size=576 if p.parent.name=='wait' else 704
  assert im.mode=='RGBA' and im.size==(size,size) and im.getchannel('A').getextrema()==(0,255),p
  key=p.as_posix().split('characters/')[1]
  rows.append({'key':key,'file':str(p.resolve()),'name':'RtsArt_'+key.replace('/','_').replace('.png','').replace('-','_'),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  tile=Image.new('RGB',(176,200),'#e1e6eb');small=im.copy();small.thumbnail((176,176));tile.paste(small,((176-small.width)//2,0),small);ImageDraw.Draw(tile).text((3,180),folder[:2]+' '+p.parent.name[:12]+' '+p.stem[-2:],fill='black');tiles.append(tile)
 for seq in j['playback']:
  c=dict(seq);c['jobId']='nl' if folder=='night-lord' else 'shad';c['action']=action[folder][seq['skill']]
  c['files']=[f'assets/design/characters/{folder}/frames/{seq["skill"]}/motion{n:02}.png' for n in seq['order']]
  c['duration']=round(sum(c['times']),3);connections.append(c)
assert len(rows)==35
(work/'upload-files.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
(work/'connection-plan.json').write_text(json.dumps({'status':'prepared','files':35,'connections':connections},ensure_ascii=False,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(176*7,200*5),'#e1e6eb')
for n,t in enumerate(tiles):sheet.paste(t,((n%7)*176,(n//7)*200))
sheet.save(work/'contact.jpg')
shutil.copyfile('.beaver/output/dark-knight-buster/upload-pngs.py',work/'upload-pngs.py')
print(json.dumps(rows))

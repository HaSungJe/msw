from pathlib import Path
import json,re
root=Path('C:/workspace/msw');out=root/'.beaver/output/five-class-portraits-phantom'
rows=json.loads((out/'resource-manifest.json').read_text(encoding='utf-8'))
assert len(rows)==18
ruid={r['key']:r['ruid'] for r in rows}
p=root/'RootDesk/MyDesk/RtsJobTableLogic.mlua';s=p.read_text(encoding='utf-8')
assert 'phantomJoker' not in s
s=s.replace('or jobId == "shad"\n','or jobId == "shad" or jobId == "phantom"\n',1)
def quoted(keys):return ', '.join('"'+ruid[k]+'"' for k in keys)
stand=quoted([f'phantom/wait/{n:02}' for n in [1,2,1,3]])
joker=quoted([f'phantom/joker/{n:02}' for n in range(1,9)])
s=s.replace('method table GetMageSkinFrames(string jobId)\n','method table GetMageSkinFrames(string jobId)\n\t\tif jobId == "phantom" then\n\t\t\treturn {\n\t\t\t\tstand1 = { '+stand+' },\n\t\t\t\tphantomJoker = { '+joker+' },\n\t\t\t}\n\t\tend\n',1)
s=s.replace('method table GetMageSkinFrameDurations(string jobId)\n','method table GetMageSkinFrameDurations(string jobId)\n\t\tif jobId == "phantom" then\n\t\t\treturn { stand1 = { 0.65, 0.45, 0.65, 0.45 }, phantomJoker = { 0.06, 0.05, 0.04, 0.06, 0.04, 0.05, 0.05, 0.05 } }\n\t\tend\n',1)
a=s.index('method string GetMagePortraitRUID');b=s.index('\n\tend',a);part=s[a:b]
for id,job in [('paladin','paladin'),('dark-knight','dk'),('night-lord','nl'),('shadower','shad')]:
 part,n=re.subn(r'(if jobId == "'+job+r'" then return ")[^"]+(" end)',lambda m:m[1]+ruid[id+'/portrait']+m[2],part);assert n==1
part=part.replace('-- 전용 흉상 제작 전에는 승인된 대기 첫 컷을 임시 사용한다.','-- 비숍 흉상과 승인 원화를 참조한 직업별 전용 흉상.')
part=part.replace('method string GetMagePortraitRUID(string jobId)\n','method string GetMagePortraitRUID(string jobId)\n\t\tif jobId == "phantom" then return "'+ruid['phantom/portrait']+'" end\n')
s=s[:a]+part+s[b:]
lines=s.splitlines()
for i,line in enumerate(lines):
 if 'fx = { motions = { "swingOF", "swingO1", "swingO1", "stabO1" }' in line:
  assert '01eff730' in lines[i+1] and 'projCount = 2' in lines[i+2]
  lines[i]='\t\t\t\t\tfx = { motion = "phantomJoker", motionLoop = true,'
  lines[i+1]='\t\t\t\t\t\tproj = "'+ruid['phantom/card']+'", projRing = "'+ruid['phantom/ring']+'", projWidth = 1.152, projRingSize = 2.528, projSpin = 458.37, projRingSpin = 286.48,'
  lines[i+2]='\t\t\t\t\t\tprojCount = 2, projStagger = 0.05, projSec = 0.4, projDx = 0.568, projDy = 0.84, projNoRotate = true, projArc = 1.0, projArcByDist = { 1.0, 1.1, 1.2, 1.3 }, assetFacesLeft = true,'
  break
else:raise AssertionError('Phantom fx not found')
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
for id in ['paladin','dark-knight','night-lord','shadower','phantom']:
 mp=root/f'assets/design/characters/{id}/motion.json';d=json.loads(mp.read_text(encoding='utf-8'))
 d['portrait']={'file':'portrait.png','ruid':ruid[id+'/portrait'],'width':512,'height':512}
 if id=='phantom':
  d['status']='game-connected-verification-pending'
  for f in d['frames']:
   path=Path(f['file']);key='phantom/'+path.parent.name+'/'+path.stem[-2:];f['ruid']=ruid[key]
  d['runtimeActions']={'stand1':{'order':[1,2,1,3],'times':[.65,.45,.65,.45]},'phantomJoker':{'order':list(range(1,9)),'times':[.06,.05,.04,.06,.04,.05,.05,.05],'loop':True}}
  d['projectileRUID']=ruid['phantom/card'];d['ringRUID']=ruid['phantom/ring'];d['projectileWorldSize']=[1.152,1.728];d['ringWorldSize']=[2.528,2.528]
 mp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Connected 18 new resources; portraits 5, Phantom frames 11, effects 2.')

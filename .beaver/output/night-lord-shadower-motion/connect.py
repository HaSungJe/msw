from pathlib import Path
import json,re,difflib
work=Path(__file__).parent
rows=json.loads((work/'resource-manifest.json').read_text(encoding='utf-8'))
plan=json.loads((work/'connection-plan.json').read_text(encoding='utf-8'))
ruids={r['key']:r['ruid'] for r in rows}
assert len(ruids)==35 and len(set(ruids.values()))==35
path=Path('RootDesk/MyDesk/RtsJobTableLogic.mlua');original=path.read_bytes();s=original.decode('utf-8').replace('\r\n','\n')
assert 'nlThrow = {' not in s
(work/'RtsJobTableLogic.before.mlua').write_bytes(original)
s=s.replace('or jobId == "dk"\n','or jobId == "dk" or jobId == "nl" or jobId == "shad"\n',1)
for method,frames in [('GetMageSkinFrames',True),('GetMageSkinFrameDurations',False)]:
 blocks=[]
 for job in ['nl','shad']:
  blocks.append('\t\tif jobId == "'+job+'" then\n\t\t\treturn {')
  for c in plan['connections']:
   if c['jobId']!=job:continue
   values=[json.dumps(ruids[f.split('characters/')[1]]) for f in c['files']] if frames else [str(t) for t in c['times']]
   assert len(values)==len(c['times'])
   blocks.append('\t\t\t\t'+c['action']+' = { '+', '.join(values)+' },')
  blocks.append('\t\t\t}\n\t\tend')
 anchor='\tmethod table '+method+'(string jobId)\n';assert s.count(anchor)==1;s=s.replace(anchor,anchor+'\n'.join(blocks)+'\n',1)
anchor='\tmethod string GetMagePortraitRUID(string jobId)\n';addition=''
for job,folder in [('nl','night-lord'),('shad','shadower')]:addition+='\t\tif jobId == "'+job+'" then return "'+ruids[folder+'/frames/wait/motion01.png']+'" end\n'
s=s.replace(anchor,anchor+addition,1)
for old,new,clip in [('swingO1','nlThrow','ff9ced53e871474c9a2ae167e0c75ef1'),('swingO2','shadSavage','895ac1e384ea42ca8dd084f54ff3346b'),('swingO1','shadMeso','61840689ea7b44f09f91960734232e34')]:
 s,n=re.subn(r'motion = "'+old+r'"(?=[^\n]*clip = "'+clip+r'")','motion = "'+new+'"',s);assert n==1
old='motions = { "swingD1", "swingD2" }, motionGap = 0.3, noFlip = true'
assert s.count(old)==1;s=s.replace(old,'motion = "shadDualblade", noFlip = true',1)
s=s.replace('모션 = swingO1 + 무기 가림','모션 = nlThrow PNG (이전 swingO1) + 아바타 경로 무기 가림').replace('빠른 한손 베기 모션(swingO2)','빠른 단검 베기 PNG(shadSavage)').replace('모션 swingD1 → 0.3초 뒤 swingD2','모션 shadDualblade PNG 3.2초(0.3초 방출 자세)')
path.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
(work/'job-table.diff').write_text(''.join(difflib.unified_diff(original.decode('utf-8').splitlines(True),s.splitlines(True))),encoding='utf-8')
path=Path('RootDesk/MyDesk/RtsSkillFxLogic.mlua');original=path.read_bytes();s=original.decode('utf-8').replace('\r\n','\n');(work/'RtsSkillFxLogic.before.mlua').write_bytes(original)
old='\t\t\tbody.RtsUnitComponent:PlayMageAction(name)\n\t\t\treturn\n\t\tend\n\t\t-- frameA·frameB(있으면) = 재생 프레임 범위. 같은 값이면 그 프레임에 멈춘 자세(조커 — 지팡이를 앞으로 뻗은 stabO1 마지막 프레임 유지)\n\t\tif frameA ~= nil then'
new='\t\t\tbody.RtsUnitComponent:PlayMageAction(name)\n\t\t-- PNG 본체도 아래 쉐도우 파트너 지연 재생을 거친다.\n\t\telseif frameA ~= nil then'
assert s.count(old)==1;s=s.replace(old,new,1)
anchor='\tmethod string ShadowClip(string action)\n';assert s.count(anchor)==1
s=s.replace(anchor,anchor+'\t\t-- 원화 투척의 분신은 기존 검은 실루엣 투척 액션을 유지한다.\n\t\tif action == "nlThrow" then action = "swingO1" end\n',1)
path.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
(work/'skill-fx.diff').write_text(''.join(difflib.unified_diff(original.decode('utf-8').splitlines(True),s.splitlines(True))),encoding='utf-8')
for file in ['assets/design/characters/night-lord/motion.json','assets/design/characters/shadower/motion.json','.beaver/output/five-class-motion/manifest.json']:
 p=Path(file);j=json.loads(p.read_text(encoding='utf-8'));items=j if isinstance(j,list) else [j]
 for item in items:
  if item['id'] not in ['night-lord','shadower']:continue
  item['status']='connected-awaiting-maker-verification';item['runtimeActions']=[c for c in plan['connections'] if c['id']==item['id']];item['portraitStatus']='wait-motion01-temporary; dedicated-portrait-pending'
  for f in item['frames']:
   key=f['file'].replace('\\','/').split('characters/')[-1]
   if key in ruids:f['ruid']=ruids[key]
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
plan.update(status='connected-awaiting-maker-verification',uploaded=35)
(work/'connection-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Connected 35 PNGs, 6 action sequences, shadow partner delayed motion preserved.')

from pathlib import Path
import json, re
root=Path(__file__).parent
rows=json.loads((root/'resource-manifest.json').read_text(encoding='utf-8'))
plan=json.loads((root/'connection-plan.json').read_text(encoding='utf-8'))
ruids={r['key']:r['ruid'] for r in rows}
assert len(ruids)==32 and len(set(ruids.values()))==32
def resource(file):
    return ruids[file.split('assets/design/characters/')[-1]]
path=Path('RootDesk/MyDesk/RtsJobTableLogic.mlua')
original=path.read_bytes()
s=original.decode('utf-8').replace('\r\n','\n')
assert 'paladinCharge = {' not in s
(root/'RtsJobTableLogic.before.mlua').write_bytes(original)
s=s.replace('or jobId == "bow"\n','or jobId == "bow" or jobId == "paladin" or jobId == "dk"\n',1)
for method,is_frames in [('GetMageSkinFrames',True),('GetMageSkinFrameDurations',False)]:
    blocks=[]
    for job in ['paladin','dk']:
        blocks.append('\t\tif jobId == "'+job+'" then\n\t\t\treturn {')
        for c in plan['connections']:
            if c['jobId']!=job: continue
            values=[json.dumps(resource(f)) for f in c['files']] if is_frames else [str(t) for t in c['times']]
            assert len(values)==len(c['times'])
            blocks.append('\t\t\t\t'+c['action']+' = { '+', '.join(values)+' },')
        blocks.append('\t\t\t}\n\t\tend')
    anchor='\tmethod table '+method+'(string jobId)\n'
    s=s.replace(anchor,anchor+'\n'.join(blocks)+'\n',1)
anchor='\tmethod string GetMagePortraitRUID(string jobId)\n'
addition='\t\t-- 전용 흉상 제작 전에는 승인된 대기 첫 컷을 임시 사용한다.\n'
for job,folder in [('paladin','paladin'),('dk','dark-knight')]:
    addition+='\t\tif jobId == "'+job+'" then return "'+ruids[folder+'/frames/wait/motion01.png']+'" end\n'
s=s.replace(anchor,anchor+addition,1)
for old,new,clip in [('swingTF','paladinCharge','cb9cff6c57fd4cb18a05db3d47277031'),('swingT1','paladinSanctuary','d577178a8212489e8319a4c5b16e897b'),('stabT1','dkBuster','c7051cc242c54208a7c22df2b4bcc28e'),('swingT3','dkRoar','5468cadd2f60428e925bc368968e1a1e')]:
    pattern=r'motion = "'+old+r'"(?=[^\n]*clip = "'+clip+r'")'
    s,n=re.subn(pattern,'motion = "'+new+'"',s)
    assert n==1,(old,n)
start=s.index('elseif id == "giant" then')
pos=s.index('\t\t\t\tlocal fx = self:CopyTable(k.fx)\n',start)+len('\t\t\t\tlocal fx = self:CopyTable(k.fx)\n')
s=s[:pos]+'\t\t\t\tfx.motion = "dkGiantBuster" -- 같은 창 프레임으로 6회 찌르기\n'+s[pos:]
s=s.replace('= character.md 값): swingTF +','= character.md 값): paladinCharge PNG +').replace('생츄어리 연출(character.md 값): swingT1 +','생츄어리 연출(character.md 값): paladinSanctuary PNG +').replace('드래곤 로어 연출(character.md 값): swingT3 +','드래곤 로어 연출(character.md 값): dkRoar PNG +')
s=s.replace('모션 stabT1은 0.5초 뒤(motionDelay — 찌르기 3개 0.6~0.95초를 덮음).','PNG dkBuster는 준비 0.5초를 첫 프레임 유지 시간에 포함한다(찌르기 3개 0.6~0.95초를 덮음; motionDelay는 기존 아바타 경로용).')
path.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
plan.update(status='connected-awaiting-maker-verification',gameCodeChanged=True,uploaded=32)
(root/'connection-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(root/'upload-requests.private.json').unlink()
print('Connected 32 resources / 7 sequences; preserved existing code changes.')

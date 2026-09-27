from pathlib import Path
from PIL import Image
import json,hashlib
project=Path('C:/workspace/msw');work=Path(__file__).parent
uploads=json.loads((work/'upload-files.json').read_text(encoding='utf-8'))
for row in uploads:
 p=Path(row['file']);assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],p
 im=Image.open(p);expected=576 if '/wait/' in row['key'] else 704
 assert im.size==(expected,expected) and im.mode=='RGBA',p
 assert im.getchannel('A').getextrema()==(0,255),p
action={'paladin':{'wait':'stand1','divine-charge':'paladinCharge','sanctuary':'paladinSanctuary'},'dark-knight':{'wait':'stand1','spear-buster':'dkBuster','dragon-roar':'dkRoar'}}
items=json.loads((project/'.beaver/output/five-class-motion/manifest.json').read_text(encoding='utf-8'));connections=[]
for item in items:
 if item['id'] not in action:continue
 for seq in item['playback']:
  c=dict(seq);c['jobId']='dk' if item['id']=='dark-knight' else 'paladin';c['action']=action[item['id']][seq['skill']]
  c['files']=[f"assets/design/characters/{item['id']}/frames/{seq['skill']}/motion{n:02}.png" for n in seq['order']]
  if seq.get('delay',0):c['times']=list(seq['times']);c['times'][0]+=seq['delay'];c['delay']=0;c['note']='기존 PNG 재생 경로는 motionDelay를 사용하지 않으므로 첫 준비 자세에 0.5초를 포함한다.'
  connections.append(c)
giant={'jobId':'dk','action':'dkGiantBuster','skill':'spear-buster','order':[1,2,3,4,5,6,7,6,5,6,7,6,7,8],'times':[.6,.05,.04,.035,.04,.035,.04,.035,.04,.035,.04,.035,.04,.135],'hit':[.65,.725,.8,.875,.95,1.025]}
giant['files']=[f'assets/design/characters/dark-knight/frames/spear-buster/motion{n:02}.png' for n in giant['order']];connections.append(giant)
for c in connections:
 assert len(c['files'])==len(c['times']);c['duration']=round(sum(c['times']),3)
plan={'status':'awaiting-upload-approval','worldId':'c7127d5fb5e64537bf0520c1418932e4','accountUserId':'20372100000235013','destination':'MSW current account resource storage, sprite/etc','files':32,'bytes':sum(x['size'] for x in uploads),'validatedPngFiles':32,'connections':connections,'plannedChanges':['RtsJobTableLogic.HasMageSkin: paladin/dk 추가','GetMageSkinFrames/GetMageSkinFrameDurations: 대기와 5개 공격 시퀀스 연결','기존 fx.motion을 대응 PNG action으로 변경; 거대화는 전용 반복 시퀀스','별도 흉상 제작 전 선택창은 대기 1번 이미지를 사용해 빈 RUID 방지'],'verification':['새 RUID 32개 LoadSpriteAndWait 완료 확인','좌우 반전, 모든 공격 프레임과 대기 복귀 확인','다크나이트 0.5초 준비 및 거대화 6회 동작 확인','Maker build/normal 로그 검사'],'unchanged':['피해량','타격 시각','쿨타임','기존 스킬 이펙트','다른 직업 모션'],'gameCodeChanged':False,'uploaded':0}
(work/'connection-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 팔라딘·다크나이트 모션 연결 준비','', '상태: 업로드 자동 승인 거절로 대기. 파일 검수 완료, 업로드 0장, 게임 코드 변경 없음.','',f"업로드 대상: 승인된 PNG 32장, {plan['bytes']:,}바이트. 현재 월드 계정 MSW resource storage의 sprite/etc로 각각 새 RUID 등록.",'','| 직업 | 동작 키 | 재생 길이 |','|---|---|---:|']
lines += [f"| {c['jobId']} | {c['action']} | {c['duration']:.3f}초 |" for c in connections]
lines += ['','스피어 버스터는 첫 준비 자세에 0.5초를 포함한다. 거대화는 기존 프레임의 찌르기·회수를 반복하며 기존 6회 타격 시각을 유지한다. 별도 흉상은 만들지 않고 대기 첫 이미지를 선택창에 연결할 예정이다.','', '## 검수한 업로드 파일','']+[f"- `{x['key']}` ({x['size']:,} bytes)" for x in uploads]
(work/'connection-plan.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(json.dumps({'pngVerified':32,'bytes':plan['bytes'],'uploaded':0,'gameCodeChanged':False,'sequences':[(x['action'],x['duration']) for x in connections]}))

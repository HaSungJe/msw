from pathlib import Path
import json
root=Path(__file__).parent
rows=json.loads((root/'resource-manifest.json').read_text(encoding='utf-8'))
plan=json.loads((root/'connection-plan.json').read_text(encoding='utf-8'))
summary='팔라딘·다크나이트 모션 적용: 승인된 PNG 32장을 새 RUID로 업로드하고 대기·디바인 차지·생츄어리·스피어 버스터·드래곤 로어·거대화 버스터를 연결했다. Maker 32/32 로딩, 양방향 모든 공격 프레임, 대기 3/3, 복귀 24/24, 실행 오류 0 확인. 전용 흉상은 미제작이며 선택·상세 이미지는 대기 01을 임시 사용한다. docs/design/paladin-dark-knight-motion.md 참고.'
for file in ['.beaver/memory/MEMORY.md','.info/character.md','.info/motion.md','.info/skill.md']:
 p=Path(file); s=p.read_text(encoding='utf-8')
 s=s.replace('docs/design/five-class-idle.md가 이전 회전 기록보다 우선한다. 게임 연결 전.','docs/design/five-class-idle.md가 이전 회전 기록보다 우선한다. 팔라딘·다크나이트 게임 연결 완료, 나이트로드·섀도어·팬텀은 연결 전.')
 s=s.replace('게임 업로드·연결과 흉상은 아직 미완료다.','팔라딘·다크나이트 32장은 업로드·게임 연결·Maker 검증 완료. 나이트로드·섀도어·팬텀 게임 연결과 5종 전용 흉상은 미완료다.')
 s=s.replace('나머지 5종은 원화·대기·스킬 PNG 78장 제작 완료, 게임 연결 전으로 현재 게임에서는 기존 아바타 액션을 유지한다.','5종 원화·대기·스킬 PNG 78장 중 팔라딘·다크나이트 32장은 게임 연결 완료. 나이트로드·섀도어·팬텀만 기존 아바타 액션을 유지한다.')
 s=s.replace('게임 업로드·연결 전이므로 아래 기존 아바타 액션·이펙트·카드 투사체·판정은 현재 적용 정보로 유지한다.','팔라딘·다크나이트 몸체 모션은 전용 PNG 적용 완료. 나이트로드·섀도어·팬텀은 연결 전이며 기존 이펙트·카드 투사체·판정은 유지한다.')
 s=summary+'\n\n'+s
 if file.endswith('character.md'):
  s=s.replace('히어로(hero)·썬콜(il)·불독(fp)·비숍(bishop)은 전용 PNG 프레임·흉상, 나머지 직업은 MSW 아바타(장비 RUID 세트).','히어로(hero)·썬콜(il)·불독(fp)·비숍(bishop)·신궁(marks)·보우마스터(bow)는 전용 PNG 프레임·흉상. 팔라딘(paladin)·다크나이트(dk)도 전용 PNG 프레임이며 흉상 대신 대기 01을 임시 사용. 나머지 직업은 MSW 아바타(장비 RUID 세트).')
  for folder,ko in [('paladin','팔라딘'),('dark-knight','다크나이트')]:
   lines=s.splitlines()
   for i,line in enumerate(lines):
    if '후속 디자인용 확정 원화: assets/design/characters/'+folder+'/concept.png' in line:
     lines[i]=line.replace('흉상·게임 적용 전이며 현재 게임 외형은 아래 아바타 세트 유지. 인계: docs/design/five-class-motion.md.','전용 PNG 게임 적용 완료. 전용 흉상 제작 전 대기 01 임시 사용. 연결: docs/design/paladin-dark-knight-motion.md.')
   s='\n'.join(lines)+'\n'
   s=s.replace('외형 (모험가 '+ko+' 세트)','과거 아바타 외형 (모험가 '+ko+' 세트, 현재는 위 PNG 적용)')
 if file.endswith('skill.md'):
  for old,new in [('모션: swingTF (0.65초)','모션: paladinCharge — divine-charge PNG 6장, 총 0.75초, 타격 0.30초'),('모션: swingT1 (0.7초, 도끼 내려찍기)','모션: paladinSanctuary — sanctuary PNG 6장, 총 0.90초, 타격 0.50초'),('모션: stabT1(창 찌르기) — 시전 0.5초 뒤(motionDelay) 찌르기 3개(0.6~0.95초)에 맞춰','모션: dkBuster — spear-buster PNG 8장, 첫 준비 자세 0.60초에 기존 준비 0.50초 포함. 총 1.20초, 타격 0.65/0.80/0.95초. 거대화는 dkGiantBuster 14단계로 6회 찌르기, 총 1.20초'),('모션: swingT3','모션: dkRoar — dragon-roar PNG 6장, 총 1.40초, 타격 0.60초')]: s=s.replace(old,new)
 if file.endswith('motion.md'):
  s=s.replace('팔라딘 생츄어리 모션','과거 팔라딘 생츄어리 아바타 모션').replace('드래곤 로어 모션','과거 드래곤 로어 아바타 모션').replace('팔라딘 디바인 차지 모션','과거 팔라딘 디바인 차지 아바타 모션').replace('다크나이트 스피어 버스터 모션','과거 다크나이트 스피어 버스터 아바타 모션')
  s=s.replace('현재 히어로·썬콜·불독·비숍·신궁은','현재 히어로·썬콜·불독·비숍·신궁·보우마스터·팔라딘·다크나이트는')
 p.write_text(s,encoding='utf-8')
p=Path('docs/unit-art.md'); s=p.read_text(encoding='utf-8')
s=s.replace('나머지 [5종](design/five-class-motion.md)은 원화와 대기·공격 PNG 78장까지 저장했고 게임 적용 전이다.','[5종](design/five-class-motion.md)의 원화와 대기·공격 PNG 78장 중 [팔라딘·다크나이트 32장](design/paladin-dark-knight-motion.md)은 게임 연결·Maker 검증 완료. 나이트로드·섀도어·팬텀은 적용 전이다. 팔라딘·다크나이트의 전용 흉상은 미제작이며 대기 01을 임시 사용한다.')
s=s.replace('게임 연결 (히어로·썬콜·불독·비숍·신궁·보우마스터)','게임 연결 (히어로·썬콜·불독·비숍·신궁·보우마스터·팔라딘·다크나이트)')
p.write_text(s,encoding='utf-8')
p=Path('docs/design/five-class-motion.md');s=p.read_text(encoding='utf-8')
a=s.index('2026-09-27');b=s.index('\n\n',a)
s=s[:a]+'2026-09-27 승인 원화 기반 PNG 78장. **팔라딘·다크나이트 32장은 업로드·게임 연결·Maker 재생 검증 완료**했다. 나이트로드·섀도어·팬텀 46장은 로컬 제작 완료·게임 연결 전이다. 전용 흉상은 미제작이며 적용한 두 직업의 선택·상세 이미지는 대기 01을 임시 사용한다. [적용 기록](paladin-dark-knight-motion.md).'+s[b:]
s=s.replace('거대화의 6회 찌르기는 이 프레임의 찌르기·회수 구간을 반복해 연결할 것','거대화는 같은 프레임을 14단계·1.20초로 반복 연결 완료')
s=s.replace('Maker 실행 검증은 게임 연결 후 진행할 항목이며 이번 완료 상태에 포함하지 않는다.','팔라딘·다크나이트는 Maker 32/32 로딩, 좌우 모든 공격 프레임과 대기 복귀를 확인했다. 나머지 세 직업은 Maker 검증 전이다.')
p.write_text(s,encoding='utf-8')
p=Path('docs/design/five-class-idle.md');s=p.read_text(encoding='utf-8').replace('게임 업로드·리소스 연결·Maker 검증은 이번 작업에 포함하지 않는다. 현재 게임에서는 여전히 기존 아바타 동작을 사용한다.','후속 적용: 팔라딘·다크나이트는 업로드·게임 연결·Maker 검증 완료(docs/design/paladin-dark-knight-motion.md). 나이트로드·섀도어·팬텀은 기존 아바타 동작을 유지한다.');p.write_text(s,encoding='utf-8')
aggregate=Path('.beaver/output/five-class-motion/manifest.json'); items=json.loads(aggregate.read_text(encoding='utf-8'))
for item in items:
 if item['id'] not in ['paladin','dark-knight']: continue
 folder=item['id'];job='dk' if folder=='dark-knight' else folder
 item['status']='game-connected-maker-verified'
 item['runtimeActions']=[c for c in plan['connections'] if c['jobId']==job]
 item['portraitStatus']='wait-motion01-temporary; dedicated-portrait-pending'
 for frame in item['frames']:
  frame['ruid']=next(r['ruid'] for r in rows if r['key']==folder+'/'+frame['file'])
 Path('assets/design/characters/'+folder+'/motion.json').write_text(json.dumps(item,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
aggregate.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
plan['status']='game-connected-maker-verified'
(root/'connection-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
doc=['# 팔라딘·다크나이트 모션 적용','',summary,'','## 연결','', '| 직업 | 액션 | 재생 순서 | 프레임 시간(초) | 합계 |','|---|---|---|---|---|']
for c in plan['connections']: doc.append('| '+c['jobId']+' | '+c['action']+' | '+','.join(map(str,c['order']))+' | '+','.join(map(str,c['times']))+' | '+str(c['duration'])+' |')
doc+=['','기존 피해·타격 시각·쿨타임·스킬 이펙트는 유지한다. PNG 경로에서 motionDelay는 사용하지 않으므로 버스터의 첫 준비 자세에 기존 0.50초를 포함했다. 거대화는 기존 8장을 반복해 타격 간격 0.075초에 맞춘다. 비홀더 구체는 없다.','', '## 리소스','', '| PNG (assets/design/characters/ 아래) | 새 RUID |','|---|---|']
for r in rows: doc.append('| '+r['key']+' | `'+r['ruid']+'` |')
doc+=['','## 검증','', '- Maker RtsMap, refresh → save → play. 빌드 오류 0, 기존 다른 메서드 정적 경고 10개는 남아 있다.','- LoadSpriteAndWait 32/32, 프레임·시간표 연결 오류 0.','- 실제 SpawnUnit 경로로 팔라딘·다크나이트·거대화 유닛 생성, AvatarRenderer 없음 확인.','- PlayCast 경로 좌우 재생: 차지 6/6, 생츄어리 6/6, 버스터 8/8, 로어 6/6, 거대화 8/8(고유 프레임). 대기 각 3/3, 복귀 총 24/24, 기존 시전 효과 생성 확인.','- 피해량 회귀 및 선택·상세 UI 크기 육안 검수는 이번 모션 확인에 포함하지 않았다. 전용 흉상은 후속 작업.','- 로그·연결 전후 diff: `.beaver/output/paladin-dark-knight-motion/`.']
Path('docs/design/paladin-dark-knight-motion.md').write_text('\n'.join(doc)+'\n',encoding='utf-8')
print('Updated integration records, character manifests, framework docs and .info.')

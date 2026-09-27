from pathlib import Path
import json,re
work=Path(__file__).parent
plan=json.loads((work/'connection-plan.json').read_text(encoding='utf-8'));rows=json.loads((work/'resource-manifest.json').read_text(encoding='utf-8'))
note='나이트로드·섀도어 모션 적용: 저장된 대기·공격 PNG 35장(나이트로드 11, 섀도어 24)을 새 RUID로 연결했다. 나이트로드 nlThrow는 쿼드러플 스로우·풍마수리검 공용, 섀도어는 shadSavage·shadMeso·shadDualblade를 사용한다. 쉐도우 파트너는 기존 검은 실루엣으로 0.5초 늦게 동작한다. 흉상은 대기 01 임시 사용. 현재 연결·검증 기록: docs/design/night-lord-shadower-motion.md.'
approval='사용자 최종 확정: 팔라딘·다크나이트는 현재 게임 모션 그대로 승인. 다크나이트는 상단 → 하단 → 정면, 거대화는 같은 순서 두 번 반복.'
files=['.beaver/memory/MEMORY.md','.info/character.md','.info/motion.md','.info/skill.md','docs/design/five-class-idle.md','docs/design/five-class-motion.md','docs/unit-art.md']
for file in files:
 p=Path(file);s=p.read_text(encoding='utf-8')
 s=s.replace('나이트로드·섀도어·팬텀은 연결 전','나이트로드·섀도어도 연결 완료, 팬텀은 연결 전').replace('나이트로드·섀도어·팬텀은 적용 전','나이트로드·섀도어도 적용 완료, 팬텀은 적용 전')
 s=s.replace('나이트로드·섀도어·팬텀 게임 연결과 5종 전용 흉상은 미완료다.','나이트로드·섀도어 35장도 게임에 연결했다. 팬텀 게임 연결과 5종 전용 흉상은 미완료다.')
 s=s.replace('나이트로드·섀도어·팬텀은 기존 아바타 동작을 유지한다.','나이트로드·섀도어도 전용 PNG에 연결했다(docs/design/night-lord-shadower-motion.md). 팬텀은 기존 아바타 동작을 유지한다.')
 s=s.replace('나이트로드·섀도어·팬텀만 기존 아바타 액션을 유지한다.','나이트로드·섀도어도 PNG 연결 완료, 팬텀만 기존 아바타 액션을 유지한다.')
 if file in ['.beaver/memory/MEMORY.md','.info/character.md','.info/motion.md','.info/skill.md']:s=note+'\n\n'+(approval+'\n\n' if 'MEMORY' in file else '')+s
 if file=='.info/character.md':
  s=s.replace('팔라딘(paladin)·다크나이트(dk)도 전용 PNG 프레임이며','팔라딘(paladin)·다크나이트(dk)·나이트로드(nl)·섀도어(shad)도 전용 PNG 프레임이며')
  for folder,ko,count,actions in [('night-lord','나이트로드',11,'stand1 / nlThrow(쿼드러플 스로우·풍마수리검 공용, 0.70초)'),('shadower','섀도어',24,'stand1 / shadSavage(0.50초) / shadMeso(0.50초) / shadDualblade(3.20초)')]:
   s=re.sub(r'            - 후속 디자인용 확정 원화: assets/design/characters/'+folder+r'/concept.png[^\n]*',f'            - 현재 외형: assets/design/characters/{folder}/concept.png 기준의 전용 PNG {count}장. frames/와 motion.json을 게임에 연결했다. {actions}. 대기 576×576·공격 704×704, 발 (288,512)/(352,640), 픽셀당 0.002유닛. 전용 흉상은 미제작이며 대기 01 임시 사용. docs/design/night-lord-shadower-motion.md.',s)
   s=s.replace('            - 외형 (모험가 '+ko+' 세트)','            - 과거 아바타 외형 (현재 전용 PNG, 모험가 '+ko+' 세트)')
 if file=='.info/skill.md':
  a=s.index('        - 나이트로드');b=s.index('- 히든 캐릭터',a);part=s[a:b]
  part=re.sub(r'- 모션: swingO1 \+ 무기 가림 0.6초[^\n]*','- 모션: nlThrow — quadruple-throw PNG 8장·10단계·0.70초. 풍마수리검도 같은 몸체 모션.',part)
  part=part.replace('본체 액션과 같은 이름의 그림자 클립','본체 nlThrow를 기존 swingO1로 대응한 그림자 클립').replace('0.15초 늦게 어두운 보라색','0.5초 늦게 어두운 보라색')
  part=part.replace('시전 클립·swingO1·무기 가림은 쿼드러플 스로우 것.','시전 클립·nlThrow PNG 모션은 쿼드러플 스로우와 공유한다.')
  part=re.sub(r'- 모션: swingO2[^\n]*','- 모션: shadSavage — savage-blow PNG 8장·10단계·0.50초, 타격 시각 0.10~0.45초 유지.',part)
  part=part.replace('- 모션: swingO1 (2026-09-20 1차)','- 모션: shadMeso — meso-explosion PNG 5장·0.50초, 0.30초 폭발 자세.')
  part=part.replace('모션 swingD1.','모션 shadDualblade PNG 8장·3.20초.').replace('모션 swingD2(0.3초 뒤)','모션 shadDualblade 공용(0.3초 방출 자세, 3.2초까지 유지·복귀)')
  s=s[:a]+part+s[b:]
 if file=='.info/motion.md':
  s=s.replace('## 아크메이지(썬·콜)','## 나이트로드·섀도어\n\n나이트로드: 대기 3장·투척 8장(10단계 0.70초). 섀도어: 대기 3장·새비지 8장(10단계 0.50초)·메소 폭발 5장(0.50초)·토네이도/카르마 8장(3.20초). 현재 액션 키와 프레임별 시간은 docs/design/night-lord-shadower-motion.md를 따른다. 대기 01→02→01→03은 2.20초. 나이트로드 분신은 nlThrow를 기존 swingO1 실루엣에 매핑해 0.5초 늦게 재생한다. 피해·판정·투사체 자산·쿨타임은 유지한다.\n\n## 아크메이지(썬·콜)',1)
 if file=='docs/design/five-class-motion.md':
  s=s.replace('나이트로드·섀도어·팬텀 46장은 로컬 제작 완료·게임 연결 전이다.','[나이트로드·섀도어 35장](night-lord-shadower-motion.md)도 게임 연결 완료. 팬텀 11장은 로컬 제작 완료·게임 연결 전이다.')
  s=s.replace('나머지 세 직업은 Maker 검증 전이다.','나이트로드·섀도어의 후속 검증은 [적용 기록](night-lord-shadower-motion.md), 팬텀은 Maker 검증 전이다.')
 if file=='docs/unit-art.md':s=s.replace('## 4. 게임 연결 (히어로·썬콜·불독·비숍·신궁·보우마스터·팔라딘·다크나이트)','## 4. 게임 연결 (히어로·썬콜·불독·비숍·신궁·보우마스터·팔라딘·다크나이트·나이트로드·섀도어)')
 p.write_text(s,encoding='utf-8')
lines=['# 나이트로드·섀도어 모션 적용','',note,'',approval,'','## 연결','','| 직업 | 액션 | 순서 | 프레임 시간(초) | 합계 |','|---|---|---|---|---|']
for c in plan['connections']:lines.append('| '+c['jobId']+' | '+c['action']+' | '+','.join(map(str,c['order']))+' | '+','.join(map(str,c['times']))+' | '+str(c['duration'])+' |')
lines+=['','기존 원화·프레임 그림을 그대로 적용했다. 대기 576×576·발 (288,512), 공격 704×704·발 (352,640), 픽셀당 로컬 0.002유닛. 쿼드러플 스로우·풍마수리검은 몸체를 공유하며 투사체는 별도 기존 자산이다. 섀도어 토네이도·카르마는 0.30초 방출, 3.20초까지 몸체와 효과가 이어진다. 피해·판정·쿨타임·투사체 설정은 변경하지 않았다.','','PNG 재생의 조기 return 때문에 그림자 동작이 생략되던 SendAction을 수정했다. 본체를 재생한 뒤 기존 그림자 지연 경로로 이어지며 nlThrow는 swingO1 실루엣 클립을 선택한다. 다른 아바타 이벤트 경로는 유지한다.','','## 현재 리소스','','| PNG (assets/design/characters/ 아래) | RUID |','|---|---|']
lines += ['| '+r['key']+' | `'+r['ruid']+'` |' for r in rows]
lines += ['','파일·SHA256·RUID: `.beaver/output/night-lord-shadower-motion/resource-manifest.json`. 연결: `connection-plan.json`, 검증 스크립트: `verify.lua`, 자동 재생: `autoplay.lua`. 전용 흉상은 미제작이며 선택·상세 정보는 대기 01을 임시 사용한다. 피해량 회귀 검증은 이번 외형 연결 범위에 포함하지 않는다.']
Path('docs/design/night-lord-shadower-motion.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=Path('docs/design/paladin-dark-knight-motion.md');s=p.read_text(encoding='utf-8');p.write_text(s+'\n'+approval+'\n',encoding='utf-8')
print('Synchronized art guide, current character/skill/motion descriptions and resource records.')

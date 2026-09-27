from pathlib import Path
import json,re
root=Path('.beaver/output/dark-knight-buster')
rows=json.loads((root/'applied-frames.json').read_text())
note='다크나이트 스피어 버스터 후속 교체: 승인한 상단 → 하단 → 정면의 깊은 찌르기를 적용했다. 거대화는 같은 순서를 두 번 반복한다. 8파일(고유 그림·RUID 6개), 832×832·발 기준 (416,768), 기존 신체 표시 배율·타격 시각·피해·쿨타임은 유지한다. 최신 자산 기록은 .beaver/output/dark-knight-buster/applied-frames.json이다.'
for name in ['.info/character.md','.info/motion.md','.info/skill.md','.beaver/memory/MEMORY.md']:
 p=Path(name);s=p.read_text(encoding='utf-8');s=note+'\n\n초기 적용 검증 이력: '+s
 if name.endswith('character.md'):
  s=s.replace('        - 다크나이트\n','        - 다크나이트\n            - 현재 스피어 버스터: 상단 → 하단 → 정면으로 어깨·상체·팔을 깊게 뻗는 승인 모션. frames/spear-buster/motion01~08.png, 832×832, 발 (416,768). 로어는 704×704 유지. 거대화도 동일한 세 방향을 두 번 반복.\n')
 if name.endswith('skill.md'):
  s=s.replace('dkBuster — spear-buster PNG 8장,','dkBuster — 상단 → 하단 → 정면의 깊은 찌르기, spear-buster PNG 8파일(고유 그림 6개),')
  s=s.replace('dkGiantBuster 14단계로 6회 찌르기','dkGiantBuster 14단계로 상단 → 하단 → 정면을 두 번 반복해 6회 찌르기')
 p.write_text(s,encoding='utf-8')
p=Path('docs/design/paladin-dark-knight-motion.md');s=p.read_text(encoding='utf-8')
s=s.replace('## 연결',note+'\n\n## 연결',1).replace('1,2,3,4,5,6,7,6,5,6,7,6,7,8','1,2,3,4,5,6,7,2,3,4,5,6,7,8')
s=s.replace('거대화는 기존 8장을 반복해','거대화는 상단·하단·정면을 두 번 반복해')
s=s.replace('## 검증','## 초기 적용 검증 (버스터 후속 교체 전)',1)
for row in rows:
 pattern=r'(\| '+re.escape(row['key'])+r' \| `)[a-f0-9]+(` \|)'
 s,n=re.subn(pattern,lambda m:m[1]+row['ruid']+m[2],s);assert n==1
s+='\n## 버스터 후속 교체\n\n03번 상단·05번 하단·07번 정면이 타격 자세다. 01=02 준비, 08=06 회수 자세를 공유한다. 긴 창의 전진 폭을 확보하기 위해 이 스킬만 832×832 투명 캔버스를 사용하며 픽셀당 0.002유닛과 바닥 여백 64px을 유지한다. 생성 프롬프트·참조 원본은 `.beaver/output/dark-knight-buster/generated.json`, 정렬은 `normalization.json`, 현재 8파일·RUID·SHA256은 `applied-frames.json`에 저장했다. 이전 32개 업로드 manifest는 초기 버전 이력이다.\n'
p.write_text(s,encoding='utf-8')
p=Path('docs/design/five-class-motion.md');s=p.read_text(encoding='utf-8').replace('스킬별 고유 프레임','스킬별 PNG 파일').replace('spear-buster 8, dragon-roar 6','spear-buster 8(고유 6), dragon-roar 6')
s=s.replace('대기 576×576, 공격 704×704 투명 PNG이며','대기 576×576, 기본 공격 704×704 투명 PNG이며')
s=s.replace('정규화는 균등 배율','다크나이트 스피어 버스터의 후속 승인본은 832×832·발 (416,768) 예외를 사용한다. 상단 → 하단 → 정면으로 깊게 찌르며 거대화는 두 번 반복한다. 현재 파일·RUID는 [적용 기록](paladin-dark-knight-motion.md)을 따른다.\n\n정규화는 균등 배율')
s=s.replace('| 스피어 버스터 | 8장','| 스피어 버스터 | 상단 → 하단 → 정면, 8파일(고유 6장)').replace('거대화는 같은 프레임을 14단계','거대화는 세 방향을 두 번 반복하는 14단계')
s=s.replace('스피어 버스터 6번의 창 방향,','초기 제작 당시 스피어 버스터 6번의 창 방향,')
p.write_text(s,encoding='utf-8')
p=Path('docs/unit-art.md');s=p.read_text(encoding='utf-8');s=s.replace('- 캔버스: 대기 576×576·발 (288,512), 공격 704×704·발 (352,640).','- 캔버스: 대기 576×576·발 (288,512), 기본 공격 704×704·발 (352,640). 다크나이트 스피어 버스터 승인본은 긴 창을 깊게 뻗기 위해 832×832·발 (416,768)을 사용한다.');p.write_text(s,encoding='utf-8')
print('Synced current resource table, giant order, canvas exception and local character/skill/motion records.')

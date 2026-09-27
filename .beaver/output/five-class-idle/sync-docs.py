from pathlib import Path
r=Path(__file__).parent;project=r.parents[2]
def edit(rel,replacements):
 p=project/rel;s=p.read_text(encoding='utf-8')
 for a,b in replacements:
  assert a in s,(rel,a);s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
edit('docs/design/five-class-motion.md',[
 ('로컬 PNG 80장','로컬 PNG 76장'),
 ('| 팬텀 / phantom | 3 | joker 10 | 13 |','| 팬텀 / phantom | 3 | joker 6 | 9 |'),
 ('고유 공격 PNG는 65장이고 대기는 15장이다. 대기 첫 장은 승인 원화를 공통 프레임에 정렬한 것이며, 나머지 75장은 ImageGen으로 자세를 생성했다. 동일 프레임을 반복하는 연타는 재생 순서에 명시하고 파일을 중복 생산하지 않았다.','현재 공격·스킬 PNG는 61장이고 대기는 15장이다. 사용자 피드백으로 5직업 대기를 모두 자연스러운 대기 자세로 다시 그렸으며, 팬텀 회전 10장은 연속 투척 6장으로 교체했다. 팬텀 준비·복귀는 같은 중립 자세를 사용한다. [대기·조커 수정 기록](five-class-idle.md)이 이전 제작 기록보다 우선한다.'),
 ('| 조커 | 준비 1번, 회전 2~9번(각 0.10초, 한 바퀴 0.80초), 종료 10번. 미리보기는 3회 회전. 연속 공격 시 몸 회전 시계를 매 0.10초 카드 발사마다 초기화하지 말 것 |','| 조커 | 준비 1번, 카드 당김·뿌리기·회수 2~5번(각 0.05초, 한 주기 0.20초), 종료 6번. 몸 회전 없음. 목을 쥐어 띄운 케인은 그대로 유지. 연속 공격마다 동작 시계를 초기화하지 말 것 |'),
 ('팬텀은 사용자 영상의 준비→앞·옆·등 회전→복귀를 참고했다.','팬텀은 사용자의 명시 정정에 따라 몸 회전 해석을 폐기하고 같은 방향으로 카드를 연속 투척한다.'),
 ('80개 파일의 수·크기·알파·캔버스 가장자리 잘림 검사를 통과했고','수정된 21개 파일의 크기·알파·캔버스 가장자리 검사를 통과했고 전체 파일 수는 76개다.')
])
for rel in ['docs/unit-art.md','docs/design/character-concepts.md','docs/design/five-class-concepts.md']:
 p=project/rel;s=p.read_text(encoding='utf-8').replace('PNG 80장','PNG 76장').replace('대기·공격 PNG 80장','대기·공격 PNG 76장')
 if rel.endswith('five-class-concepts.md'):
  s=s.replace('제작한 모션: 준비 → 앞·옆·등 방향 제자리 회전 반복 → 기본 자세 복귀, 조커 고유 프레임 10장.','수정된 모션: 몸 회전 없이 카드 당김 → 연속 투척 → 기본 자세 복귀, 조커 6장. 케인은 목 부분을 쥐어 바닥에서 띄운다.')
 p.write_text(s,encoding='utf-8')
for rel in ['.info/character.md','.info/motion.md','.info/skill.md','.beaver/memory/MEMORY.md']:
 p=project/rel;s=p.read_text(encoding='utf-8').replace('5직업 합계 80장','5직업 합계 76장').replace('대기 15장·스킬 65장(총 80장)','대기 15장·스킬 61장(총 76장)').replace('대기 15장·스킬 65장','대기 15장·스킬 61장').replace('대기·스킬 PNG 80장','대기·스킬 PNG 76장')
 note='5직업 대기·팬텀 수정: 대기 15장은 팔과 무기를 내린 자연스러운 자세로 재작화했다. 팬텀 조커는 회전 해석을 폐기하고 카드 연속 투척 6장으로 교체했으며 케인은 목을 쥐고 바닥에서 띄운다. docs/design/five-class-idle.md가 이전 회전 기록보다 우선한다. 게임 연결 전.\n\n'
 lines=s.splitlines(keepends=True);lines.insert(2,note);p.write_text(''.join(lines),encoding='utf-8')
p=project/'.beaver/output/five-class-design/phantom-video-study.md';s=p.read_text(encoding='utf-8');s=s.replace('## 직접 확인한 특징','## 이전 관찰 기록 — 몸 회전 해석은 폐기')
s=s.replace('# 팬텀 조커 영상 관찰 — 2026-09-27','# 팬텀 조커 영상 관찰 — 2026-09-27\n\n**사용자 정정:** 캐릭터는 몸을 회전시키는 것이 아니라 카드를 빠르게 던지는 동작이다. 아래 앞·옆·등 회전으로 해석한 항목과 이에 따른 프레임 제작안은 잘못된 과거 해석이며 사용하지 않는다. 현재 기준은 `docs/design/five-class-idle.md`다. 케인은 목 부분을 쥐어 들고 지팡이처럼 짚지 않는다.')
p.write_text(s,encoding='utf-8')
print('current documents synchronized; old rotation interpretation explicitly rejected')

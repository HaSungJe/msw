from pathlib import Path
r=Path(__file__).parent;project=r.parents[2]
paths=['docs/unit-art.md','docs/design/character-concepts.md','docs/design/five-class-concepts.md','docs/design/five-class-motion.md','docs/design/five-class-idle.md','.info/character.md','.info/motion.md','.info/skill.md','.beaver/memory/MEMORY.md']
for rel in paths:
 p=project/rel;s=p.read_text(encoding='utf-8')
 for a,b in [('PNG 76장','PNG 78장'),('합계 76장','합계 78장'),('총 76장','총 78장'),('합계는 76개','합계는 78개'),('파일 수는 76개','파일 수는 78개'),('전체 파일 수는 76개','전체 파일 수는 78개'),('스킬 61장','스킬 63장'),('스킬 61)','스킬 63)'),('공격·스킬 PNG는 61장','공격·스킬 PNG는 63장'),('카드 연속 투척 6장','카드 연속 투척 8장'),('연속 투척 6장','연속 투척 8장'),('조커 6장','조커 8장'),('| joker 6 | 9 |','| joker 8 | 11 |')]:s=s.replace(a,b)
 if rel=='docs/design/five-class-idle.md':
  a=s.index('팬텀 조커는 6장 구성:');b=s.index('\n\n',a)
  s=s[:a]+'팬텀의 작은 제스처 6장은 사용자에게 반려됐고, [영상 기준 재작화](phantom-joker-motion.md)의 8장으로 교체했다. 몸 회전만 빼고 영상의 팔·무릎 동작을 따른다. 왼쪽을 향해 몸 앞을 가로지르는 투척이며 1~8번 총 0.40초 반복이다. 카드 자체는 별도 투사체 PNG로 저장했다. 해당 문서가 이전 모션 설명보다 우선한다.'+s[b:]
  s=s.replace('팬텀 준비·복귀는 같은 중립 자세를 사용한다.','팬텀은 준비·후속 동작을 포함한 8컷 연사 루프를 사용한다.')
 if rel=='docs/design/five-class-motion.md':
  lines=s.splitlines();lines=[('| 조커 | [영상 기준 8장](phantom-joker-motion.md), 1~8번 총 0.40초 연사 반복. 몸 회전 없음. 케인 목을 쥐어 들고 왼쪽으로 투척. 카드 PNG 별도. |' if line.startswith('| 조커 |') else line) for line in lines];s='\n'.join(lines)+'\n'
  s=s.replace('팬텀 준비·복귀는 같은 중립 자세를 사용한다.','팬텀은 영상 기준 8컷 연사 루프를 사용하며 [최신 기록](phantom-joker-motion.md)이 우선한다.')
 if rel.startswith('.info/') or rel=='.beaver/memory/MEMORY.md':
  note='팬텀 최신 모션: 사용자 제공 영상에서 몸 회전만 제외한 팔·손·무릎 동작으로 8장 재작화. 이전 작은 팔 제스처 6장은 반려. 카드 투사체 PNG와 영상 비교 미리보기도 저장. docs/design/phantom-joker-motion.md 참고. 게임 연결 전.\n\n';lines=s.splitlines(keepends=True);lines.insert(2,note);s=''.join(lines)
 p.write_text(s,encoding='utf-8')
print('current documentation and local .info synchronized')

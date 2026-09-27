from pathlib import Path
r=Path(__file__).parent;project=r.parents[2]
p=project/'docs/design/phantom-joker-motion.md';s=p.read_text(encoding='utf-8')
s=s.replace('승인 원화와 새 대기는 유지한다.', '승인 원화와 새 대기는 유지한다. 후속 요청에서 사용자는 현재 투척을 괜찮다고 평가했고, 다리 간격 축소·더 강한 반동·큰 카드·영상의 원형 고리를 요청했다. 현재 8컷은 그 요청을 반영한 수정본이며 최종 사용자 확인 전이다.')
s=s.replace('128×192 투명 카드 뒷면. 캐릭터 프레임과 분리했다.', '256×384 투명 카드 뒷면. 캐릭터 프레임과 분리했다.\n- `assets/design/effects/phantom-joker/ring.png`: 512×512 투명 원형 소용돌이. 카드와도 분리한 흰색·분홍색 고리 이미지.')
s=s.replace('금색·분홍색의 얇은 호를 함께 표시한다.', '표시 크기는 기존 48×72에서 72×108로 1.5배 확대했다. 각 카드에 158×158 크기의 흰색·분홍색 원형 소용돌이 PNG를 함께 표시하고 독립적으로 회전시킨다. 기존 절차형 얇은 호는 이 이미지로 교체했다.')
s=s.replace('별도 카드 PNG 1장이 추가됐다.', '별도 카드 PNG와 원형 소용돌이 PNG, 총 2장의 효과 자산을 둔다.')
s=s.replace('작업 원본·완성 프롬프트·참조 경로·보정 값·검사 결과는', '후속 다리 간격·반동 수정은 기존 각 프레임을 편집 대상으로 built-in ImageGen에 전달했다. 프롬프트는 발 간격을 약 18% 줄이고 무릎·상체 반동만 보강하도록 지정하며, 캐릭터 정체성·비율·손 궤적·케인 목 그립·몸 회전 금지를 유지한다. 생성된 원본과 9개 완성 프롬프트(몸 8 + 고리 1)는 `.beaver/output/phantom-joker-refine/`의 `motion01.json`~`motion08.json`, `ring.json`에 있다. 기존 카드 그림은 고해상도 원본으로 다시 저장했다.\n\n이전 작업 원본·참조 경로와 현재 재생·검사 결과는')
p.write_text(s,encoding='utf-8')
note='팬텀 후속 수정: 승인된 카드 투척 흐름에서 다리 간격을 좁히고 무릎·상체 반동을 보강한 8컷을 저장했다. 별도 카드 PNG는 256×384, 원형 소용돌이 ring.png는 512×512. 미리보기 카드 표시 크기 72×108(기존의 1.5배), 고리 158×158이며 각각 독립 이동·회전한다. docs/design/phantom-joker-motion.md 참고. 게임 연결 전, 새 수정본 사용자 확인 전.'
for name in ['.info/character.md','.info/motion.md','.info/skill.md','.beaver/memory/MEMORY.md']:
 p=project/name;s=p.read_text(encoding='utf-8');lines=s.splitlines();lines=[note if line.startswith('팬텀 최신 모션:') else line for line in lines];p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
for name in ['docs/design/five-class-motion.md','docs/design/five-class-idle.md']:
 p=project/name;s=p.read_text(encoding='utf-8');s=s.replace('카드 PNG 별도.', '카드·원형 소용돌이 PNG 별도, 카드 표시 1.5배 확대.');s=s.replace('카드 자체는 별도 투사체 PNG로 저장했다.', '다리 간격과 무릎·상체 반동을 후속 보정했고, 카드와 원형 소용돌이는 각각 별도 PNG로 저장했다. 카드 표시 크기는 이전의 1.5배다.');p.write_text(s,encoding='utf-8')
print('design and local info synchronized')

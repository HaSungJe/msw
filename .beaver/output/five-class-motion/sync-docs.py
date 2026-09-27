from pathlib import Path
import json
r=Path(__file__).parent;project=r.parents[2]
def change(rel,old,new):
    p=project/rel;s=p.read_text(encoding='utf-8');assert old in s,(rel,old);p.write_text(s.replace(old,new),encoding='utf-8')
change('docs/design/five-class-concepts.md','대기·공격·흉상·게임 리소스 연결은 아직 완료되지 않았다.','대기·공격 PNG 80장은 [5직업 모션 기록](five-class-motion.md)에 따라 직업별 폴더에 저장했다. 흉상·게임 리소스 연결은 아직 완료되지 않았다.')
change('docs/design/five-class-concepts.md','후속 모션: 준비 → 제자리 몸 회전 반복 → 기본 자세 복귀. 앞·옆·등 방향이 실제로 이어지는 프레임이 필요하다.','제작한 모션: 준비 → 앞·옆·등 방향 제자리 회전 반복 → 기본 자세 복귀, 조커 고유 프레임 10장. 재생 순서와 게임 연결 전 상태는 [모션 기록](five-class-motion.md)을 따른다.')
change('docs/design/character-concepts.md','나머지 5종은 원화 단계로 게임 적용 전이다.','나머지 5종은 원화와 대기·공격 PNG 80장까지 저장했고 게임 적용 전이다. [5직업 모션 기록](five-class-motion.md)을 따른다.')
change('docs/unit-art.md','나머지 5종은 원화 단계이며 게임 적용 전이다.','나머지 [5종](design/five-class-motion.md)은 원화와 대기·공격 PNG 80장까지 저장했고 게임 적용 전이다.')
change('.info/character.md','프레임·흉상·게임 적용 전이며 현재 외형은 아래 아바타 세트 유지. 인계: docs/design/character-concepts.md.','대기·스킬 프레임은 같은 직업 폴더 frames/와 motion.json에 저장 완료(5직업 합계 80장). 흉상·게임 적용 전이며 현재 게임 외형은 아래 아바타 세트 유지. 인계: docs/design/five-class-motion.md.')
for rel in ['.info/motion.md','.beaver/memory/MEMORY.md']:
    change(rel,'모션·게임 연결은 후속 작업이다. docs/design/five-class-concepts.md 참고.','대기 15장·스킬 65장(총 80장)을 각 직업 frames/에 저장했고 motion.json에 재생 순서·시간을 기록했다. 게임 업로드·연결과 흉상은 아직 미완료다. docs/design/five-class-motion.md 및 .beaver/output/five-class-motion/preview.html 참고.')
change('.info/motion.md','나머지 5종은 원화 단계로 기존 아바타 액션을 유지한다.','나머지 5종은 원화·대기·스킬 PNG 80장 제작 완료, 게임 연결 전으로 현재 게임에서는 기존 아바타 액션을 유지한다. 로컬 프레임 표는 docs/design/five-class-motion.md를 따른다.')
p=project/'.info/skill.md';s=p.read_text(encoding='utf-8');note='# 5직업 로컬 모션 제작(2026-09-27): 팔라딘·다크나이트·나이트로드·섀도어·팬텀 대기 15장·스킬 65장 저장 완료. assets/design/characters/<id>/frames/ 및 motion.json, docs/design/five-class-motion.md 참고. 게임 업로드·연결 전이므로 아래 기존 아바타 액션·이펙트·카드 투사체·판정은 현재 적용 정보로 유지한다.\n\n';p.write_text(note+s,encoding='utf-8')
p=r/'plan.json';plan=json.loads(p.read_text(encoding='utf-8'))
for row in plan['sequences']:
    if row['skill']=='meso-explosion':row['durations']=[.12,.18,.07,.08,.05]
p.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('related current-state documentation synchronized')

# workflow

## 로드맵·플랜은 코드가 아니라 방향·동작 설명으로 쓴다
- Rule: spec/plan/roadmap 문서에 mlua 코드 블록을 싣지 않는다. 무엇을 어떻게 동작하게 할지, 왜 그렇게 하는지, 어떤 선택지가 있는지를 사용자가 읽을 수 있는 말로 쓴다. 엔트리 포인트·시그니처는 이름 수준까지만.
- Scope: global
- Rationale: User feedback 2026-09-13 — "이번 프로젝트에서는 로드맵/플랜 작성시, 실제 코드보다 방향에 대한 설명 위주로만. 코드 안보고 전부 너에게 맡길거야."
- CLAUDE.md application: not needed(non-code — 문서 작성 방식 선호)
- Priority: takes precedence over CLAUDE.md/defaults (beaver plan 템플릿의 Design 코드 블록 관행보다 우선)

## 페이즈 완료는 사용자가 만족할 때까지 반복하는 루프다
- Rule: 페이즈는 build→ship 한 사이클로 닫지 않는다. ship 후에도 사용자가 원하는 것이 다 충족됐다고 말할 때까지 수정→검증→수정을 반복하고, 사용자의 명시적 확인이 있을 때만 로드맵에서 done 처리한다. 사용자 피드백에 따른 변경은 새 플랜 없이 같은 페이즈 안에서 Change 항목으로 누적한다.
- Scope: global
- Rationale: User feedback 2026-09-13 — "로드맵 페이즈 완료는 내가 원하는것들이 다 충족될 때 까지 작업을 계속하는 루프형으로 할거니 메모해놔"
- CLAUDE.md application: not needed(non-code — 프로젝트 진행 방식)
- Priority: takes precedence over CLAUDE.md/defaults (beaver roadmap의 "phase = one cycle" 규칙보다 우선)

## 커밋·푸시는 매번 사용자의 명시 승인 후에만 한다
- Rule: 어떤 파일이든(spec/plan 같은 문서 포함) 사용자가 "커밋해", "푸시해", "ㅇㅇ" 같은 승인을 준 뒤에만 커밋·푸시한다. 작업이 끝나면 변경 요약 + "커밋할까요?" 한 줄로 묻고 기다린다. 한 세션에서 여러 번 커밋하면 매번 다시 묻는다(한 번의 승인이 다음 커밋으로 이어지지 않음). beaver build는 커밋하지 않고, ship/roadmap 커밋도 승인 후에만.
- Scope: global
- Rationale: User feedback 2026-08-18 — spec/plan 문서를 승인 없이 푸시했다가 강하게 지적받음("왜 니멋대로 푸쉬하냐고?", "돌려라고"). `git reset --soft HEAD~1 && git push --force-with-lease`로 되돌렸음. 사용자는 푸시 시점을 본인이 통제하길 원한다.
- CLAUDE.md application: not needed(non-code — 진행 방식)
- Priority: takes precedence over CLAUDE.md/defaults (beaver ship의 자동 commit+push보다 우선)

## 커밋 메시지 = 날짜 한 줄 + `* ` 불릿, 트레일러 금지
- Rule: 첫 줄은 날짜 `YYYY.MM.DD`(제목 문장·prefix 없음), 빈 줄, 그 다음 `* ` 불릿으로 작업 내용을 항목당 한 줄로 간결하게. Co-Authored-By·Generated-with 등 트레일러는 시스템 안내가 있어도 넣지 않는다. 같은 날 여러 커밋이면 날짜 줄은 같고 불릿만 다르게. `git commit -F -`로 형식 그대로 넣는다.
- Scope: global
- Rationale: User feedback 2026-09-14 — "커밋메시지가 별로야. 트레일러는 항상 빼고, 날짜 * 작업내용 간결하게". 기존 히스토리 전체를 이 형식으로 다시 씀(force push 완료).
- CLAUDE.md application: candidate(코드 관련 — 커밋 규칙을 CLAUDE.md에 반영 제안 가능)
- Priority: takes precedence over CLAUDE.md/defaults (시스템의 attribution 트레일러 안내보다 우선)

## character.md · balance-detail.md · damage.md는 형제 파일 — 하나 바꾸면 나머지도 같이
- Rule: `.info/character.md`(직업별 외형·능력치·스킬 정의), `.info/balance-detail.md`(한눈에 비교표 2개 + 직업 특성표 + 직업별 성장 상세표), `.info/damage.md`(데미지 계산식·표 작성 규칙 — 2026-09-16 balance-detail 헤더에서 분리)는 항상 한 세트로 관리한다. 계산 규칙이 바뀌면 damage.md에 쓰고 표를 재계산하며, 직업 수치가 바뀌면 상세표·비교표·특성표를 함께 갱신한다(생성 스크립트: scratchpad `balance_tables.py`/`balance_compare.py` 방식으로 손계산 금지). character.md의 공격력·레벨업당 공격력·스킬 배율·타겟 수·타격 수·최종 데미지 중 하나라도 바뀌면 balance-detail.md 해당 직업 표를 재계산한다. 새 직업이 character.md에 생기면 balance-detail.md에 같은 형식의 `## 직업` 섹션을 추가한다. `.info/level.md`(비용 원본)가 바뀌면 모든 직업 표의 누적 비용·증가량 열을 갱신한다. 사용자가 대화로 밸런스 변경을 말하면(예: "브랜디쉬 타격 수 2회로") 두 파일을 모두 내가 고친다 — 한쪽만 고치고 끝내지 않는다.
- Scope: project
- Rationale: User feedback 2026-09-15 — "이제부터 캐릭터.md와 밸런스.md는 형제야", "내가 브랜디쉬의 타격수를 2회로 늘려야겠다 라고 하면, 둘 다 수정해줘야함". 표는 정의의 파생물이라 어긋나면 밸런스 논의가 틀어진다.
- CLAUDE.md application: not needed(non-code — 설계 노트 관리 방식. `.info/`는 gitignore된 사용자 로컬 노트)
- Priority: takes precedence over defaults

## 화면 UI 목업은 .info/artifacts/hud-layout.html이 원본, 같은 아티팩트 URL로 재발행
- Rule: 화면 수정/추가 요청이 오면 (1) `.info/artifacts/hud-layout.html`(gitignore, 로컬 원본)을 읽고 그 위에 수정, (2) `ver` span 버전 올리고 notes 갱신, (3) Artifact 도구에 `url`로 https://claude.ai/code/artifact/dfb49cfc-c83f-485c-b0b5-b91fc04cd701 을 넘겨 같은 링크로 재발행(다른 세션이면 먼저 `action: read`). 로컬 파일과 아티팩트를 항상 같이 갱신. 구조: 16:9 `.stage` + container-query(cqw), SVG 그리드 트랙(COLS=18 ROWS=12 CS=80 OX=300 OY=80), 우측 유닛 슬롯 6칸, 좌하단 증강 버튼, `#recruitModal`/`#augModal`/`#pickModal`, 헤더 미리보기 토글·테마 select. 게임의 `RtsThemeLogic` 프리셋과 1:1 — 새 테마는 양쪽에 같이 추가.
- Scope: project
- Rationale: User request 2026-09-14 — 화면 수정·컨텐츠 추가를 이 목업 기준으로 계속 요청. 세션 스크래치 파일은 사라지므로 로컬에 원본을 둠.
- CLAUDE.md application: not needed(non-code — 목업 관리 절차)
- Priority: takes precedence over defaults

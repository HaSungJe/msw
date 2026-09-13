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

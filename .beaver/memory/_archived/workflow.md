# archived — 컨벤션 문서로 이관된 메모리 원문(복구용, 스킬은 읽지 않음)

<!-- 2026-09-24 ship: CLAUDE.md Commit 절 · Testing 절 + docs/testing.md 로 이관 -->
## 커밋 메시지 = 날짜 한 줄 + `* ` 불릿, 트레일러 금지
- Rule: 첫 줄은 날짜 `YYYY.MM.DD`(제목 문장·prefix 없음), 빈 줄, 그 다음 `* ` 불릿으로 작업 내용을 항목당 한 줄로 간결하게. Co-Authored-By·Generated-with 등 트레일러는 시스템 안내가 있어도 넣지 않는다. 같은 날 여러 커밋이면 날짜 줄은 같고 불릿만 다르게. `git commit -F -`로 형식 그대로 넣는다.
- Scope: global
- Rationale: User feedback 2026-09-14 — "커밋메시지가 별로야. 트레일러는 항상 빼고, 날짜 * 작업내용 간결하게". 기존 히스토리 전체를 이 형식으로 다시 씀(force push 완료).
- CLAUDE.md application: candidate(코드 관련 — 커밋 규칙을 CLAUDE.md에 반영 제안 가능)
- Priority: takes precedence over CLAUDE.md/defaults (시스템의 attribution 트레일러 안내보다 우선)

## Play 중에 고친 스크립트는 Stop 뒤 `maker_refresh_workspace` 없이는 안 반영된다
- Rule: Play Test가 돌아가는 동안 외부(파이썬/에디터)로 `.mlua`를 고쳤다면, `maker_stop` → **`maker_refresh_workspace`** → `maker_save` → `maker_play` 순서로 돌린다. refresh 없이 save+play 하면 Maker 메모리의 옛 스크립트로 실행된다(디스크 파일은 덮이지 않았지만 Play는 옛 값).
- Scope: project
- Rationale: 2026-09-18 — RtsCombatLogic `UnitNo`를 7→1로 고친 뒤 stop→save→play 했는데 로그가 계속 "unit 7"; refresh 후에야 "unit 1". 실행 결과가 파일과 다르면 먼저 이걸 의심.
- CLAUDE.md application: candidate(Testing 절차에 refresh 단계 추가 제안 가능)
- Priority: takes precedence over defaults

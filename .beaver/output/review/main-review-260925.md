# Review — main — 260925

> ship 전 셀프 리뷰(direct 모드). 기준: `.beaver/memory/` 규칙 → CLAUDE.md 컨벤션 → plan/spec 의도.

## Target
- 브랜치: `main`(direct 모드, 워크트리 없음) → origin/main
- 포함 기능: 맵 테마 프리셋 + 몬스터 아이콘 + 유저 카드 — `.beaver/output/plan/rts-custom/theme-icon-preset-plan.md` (로드맵 Phase 10 #38 · Phase 14 #40 · Phase 11 #41)
- 변경 규모: 수정 13파일 + 신규 `RtsProfileLogic`(mlua + codeblock) · `docs/theme-presets.md` · `assets/textures/circle-mask.png` · spec/plan/report

## Convention Check (against CLAUDE.md)
| Item | Result | Notes |
|------|------|------|
| Naming | pass | `RtsProfileLogic` PascalCase + Logic 접미사. 새 메서드 PascalCase |
| Structure & layering | pass | 테마 표·적용 = `RtsThemeLogic`, 구역 엔티티 = `RtsZoneLogic`, 타일 = `RtsBootstrapLogic`, 유저 프로필 = 새 Logic, 화면 = HUD/Popup Client 메서드 |
| 실행 공간 명시 | pass | 조작 RPC `RequestSetTheme`·`RequestSetIcon` = `@ExecSpace("Server")` + `senderUserId`, 저장·획득 = `ServerOnly`, 전달 = `@ExecSpace("Client")` + 마지막 인자 userId |
| 권한 민감 로직 Server | pass | 저장(DataStorage)·획득 굴림·보유 검증·테마 키 검증 모두 서버. 클라는 받은 값만 표시 |
| 로그 규칙 | pass | `_RtsConfigLogic:Log`만 사용 |
| 숫자 포맷 | pass | 엔티티 이름·표기 `Int`/`string.format("%d")` |
| 시그니처 변경(메모리: 분석기 인자 수 캐시) | pass | `AddPlayerRow` 인자가 늘어 새 이름 `AddPlayerCard`로(옛 메서드 삭제). `RefreshPlayerList(string)` 서명 유지 |
| 생성기 규칙(메모리 09-25) | pass | 몬스터 표 `icon`은 `tools/gen-stage-table.py`로 생성, diff = icon 칸만 |
| NativeScripts 무수정 | pass | `Environment` 변경 없음 |
| 새 Logic codeblock | pass | `RtsProfileLogic.codeblock` 동봉(Maker 생성) |
| Test strength | pass(스택 규칙) | CLI 테스트 없음 — Maker Play로 plan Test Cases 전부 확인(report Verification) |
| 데이터 접근 스모크 | 해당 없음 | DataStorage는 엔진 키-값 API(쿼리 매핑 없음) |

## Intended Behavior Check (against plan/spec)
- 테마 5종(탭 '기본')·테마 상자·확인 예/아니오·내 구역만 적용·밸런스 무관 — 구현·확인됨.
- 아이콘 247종·기본 M001·매우어려움에서만 처치 1%(보스 포함, 극악 제외)·획득 일시 저장·획득 팝업·정보(획득 여부·획득처·확률·획득일)·보유만 변경 — 구현·확인됨.
- 유저 카드(테마 배경·원형 아이콘 칸·닉네임·내 카드 초록 테두리·[수정]) — 구현·확인됨. 원형 마스크는 업로드 전이라 네모 칸.
- 서버가 입장·변경·획득 때 전체 전달, 재시작 뒤 유지 — 확인됨.
- plan과 달라진 점(report에 기록): 아이콘 창 = 스크롤 대신 32칸 쪽 넘기기(UI 1,000개 방지) · 8구역 일괄 `SetDecor`/`SetGridRUID`는 호출처가 없어 삭제(구역 단위만) · `AddPlayerRow` → `AddPlayerCard`.
- `docs/theme-presets.md`(draft) 내용을 코드와 대조 — 칸 이름·크기(썸네일 250×150·104×48·카드 280×56)·RPC·키 일치 → draft 표시 제거.

## Findings
| # | Severity | Location (path:line) | Description | Recommendation |
|---|--------|-----------------|------|------|
| 1 | Low | `RtsProfileLogic.SerializeOwned` | 획득 시각(정수 ms ≈ 6.4e16)에 `+0.5`를 더해 실수로 바뀐 뒤 `math.floor` — 실수 정밀도 때문에 최대 수 ms가 틀어질 수 있다(날짜 표기엔 영향 없음) | `+0.5` 제거(값은 원래 정수) |
| 2 | Low | `RtsZoneLogic.SetZoneDecor` | 지울 장식 개수를 `DecorCountByZone`에만 의존 — `EnsureZoneVisuals`의 "이미 ZoneGrid1 있음" 조기 반환 경로에선 개수가 0이라 옛 장식이 남을 수 있다(지금 흐름에선 안 탐) | 이름으로 1번부터 없을 때까지 지우기 |
| 3 | Info | `.beaver/memory/workflow.md` "생성기로만 고친다" | 코드 규칙인데 CLAUDE.md 미반영 | CLAUDE.md Conventions에 한 줄 + 메모리 보관(_archived) 제안 |
| 4 | Info | `RtsHudLogic.CircleMaskRUID` | 원형 마스크 미업로드 — 카드 아이콘 칸이 네모 | 사용자 확인 후 업로드 |

## Verdict
Pass — High/Medium 없음. 사용자 결정(2026-09-25)에 따라 커밋 전 처리:
- #1 반영 — `SerializeOwned`가 정수 그대로 `math.floor(v)`
- #2 반영 — `SetZoneDecor`가 기록 개수 + 이름이 이어지는 동안 지움
- #3 반영 — CLAUDE.md Conventions에 생성기 규칙(조항 전부) 추가, 메모리 항목은 `.beaver/memory/_archived/workflow.md`로
- #4 반영 — `RtsCircleMask` 업로드(`69e2dced65e443d3bb391464fd64b123`) → `RtsHudLogic.CircleMaskRUID`, Maker에서 카드 아이콘 원형 확인
- 처리 뒤 Maker 빌드 로그 오류 0, `docs/theme-presets.md` draft 표시 제거(코드와 대조 완료)

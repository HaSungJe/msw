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

## character.md · balance-detail.md · damage.md · augmentation.md · weapon.md는 형제 파일 — 하나 바꾸면 나머지도 같이
- Rule: `.info/character.md`(직업별 외형·능력치·스킬 정의), `.info/balance-detail.md`(한눈에 비교표 2개 + 직업 특성표 + 직업별 성장 상세표), `.info/damage.md`(데미지 계산식·표 작성 규칙 — 2026-09-16 balance-detail 헤더에서 분리), `.info/augmentation.md`(증강 정의 — 2026-09-16 사용자가 만들어 직접 채우는 중. 헤더 규칙: 라운드별 정해진 등급 지급, 총 43개 = 브론즈 15 / 실버 15 / 골드 10 / 프리즘 3(자쿰·루시드·진 힐라), 스킬 강화 증강은 스킬 데미지%에 합연산)는 항상 한 세트로 관리한다. 증강 계산 규칙이 생기면 damage.md에도 쓴다. 계산 규칙이 바뀌면 damage.md에 쓰고 표를 재계산하며, 직업 수치가 바뀌면 상세표·비교표·특성표를 함께 갱신한다(생성 스크립트: scratchpad `balance_tables.py`/`balance_compare.py` 방식으로 손계산 금지). character.md의 공격력·레벨업당 공격력·스킬 배율·타겟 수·타격 수·최종 데미지 중 하나라도 바뀌면 balance-detail.md 해당 직업 표를 재계산한다. 새 직업이 character.md에 생기면 balance-detail.md에 같은 형식의 `## 직업` 섹션을 추가한다. `.info/level.md`(비용 원본)가 바뀌면 모든 직업 표의 누적 비용·증가량 열을 갱신한다. 사용자가 대화로 밸런스 변경을 말하면(예: "레이징 블로우 타격 수 2회로") 두 파일을 모두 내가 고친다 — 한쪽만 고치고 끝내지 않는다.
- Scope: project
- Rationale: User feedback 2026-09-15 — "이제부터 캐릭터.md와 밸런스.md는 형제야", "내가 레이징 블로우의 타격수를 2회로 늘려야겠다 라고 하면, 둘 다 수정해줘야함". 표는 정의의 파생물이라 어긋나면 밸런스 논의가 틀어진다.
- CLAUDE.md application: not needed(non-code — 설계 노트 관리 방식. `.info/`는 gitignore된 사용자 로컬 노트)
- Priority: takes precedence over defaults

## 화면 UI 목업은 .info/artifacts/hud-layout.html이 원본, 같은 아티팩트 URL로 재발행
- Rule: 화면 수정/추가 요청이 오면 (1) `.info/artifacts/hud-layout.html`(gitignore, 로컬 원본)을 읽고 그 위에 수정, (2) `ver` span 버전 올리고 notes 갱신, (3) Artifact 도구에 `url`로 https://claude.ai/code/artifact/dfb49cfc-c83f-485c-b0b5-b91fc04cd701 을 넘겨 같은 링크로 재발행(다른 세션이면 먼저 `action: read`). 로컬 파일과 아티팩트를 항상 같이 갱신. 구조: 16:9 `.stage` + container-query(cqw), SVG 그리드 트랙(COLS=18 ROWS=12 CS=80 OX=300 OY=80), 우측 유닛 슬롯 6칸, 좌하단 증강 버튼, `#recruitModal`/`#augModal`/`#pickModal`, 헤더 미리보기 토글·테마 select. 게임의 `RtsThemeLogic` 프리셋과 1:1 — 새 테마는 양쪽에 같이 추가.
- Scope: project
- Rationale: User request 2026-09-14 — 화면 수정·컨텐츠 추가를 이 목업 기준으로 계속 요청. 세션 스크래치 파일은 사라지므로 로컬에 원본을 둠.
- CLAUDE.md application: not needed(non-code — 목업 관리 절차)
- Priority: takes precedence over defaults

## 스킬 이펙트·모션·투사체는 전부 "보는 방향"을 확인하고 올린다
- Rule: 새 연출을 올릴 때마다 **등록 전에** 클립의 그림 방향을 확인한다 — 방법: 로컬 캐시(`resource_cache/msw/<xx>-animationclip/<yy>/<ruid>.win.mod`)의 프레임 GUID 목록(.NET 혼합 엔디안, 첫 GUID = 클립 자신)을 뽑아 `https://mod-thumbnail.dn.nexoncdn.co.kr/<r0-1>/<r2-3>/<ruid>_64.png` 썸네일을 시트로 붙여 보면 화살촉·바람 방향이 바로 보인다(scratchpad `clipsheet.py out.png 라벨=ruid …` — 캐시에 없으면 Play 클라에서 `SpriteRUID`로 한 번 스폰(probe)해 내려받게 한 뒤). 썸네일은 그림 방향만 알려 주고 **원점(어느 쪽으로 뻗는지)은 안 보인다** → 원점은 sprite .win.mod 헤더(ox, oy-바닥기준)로 읽거나 표식과 같이 스폰해 실측(msw-engine 참조). 시험대 확인은 허수아비 3기(우측 세로줄 14,2·14,3·14,4)로 다수 타겟까지, 1초짜리 연출은 슬로모 미리보기(PlayRate 0.05)로 잡는다. 그 뒤 (1) 오른쪽/왼쪽 보기 둘 다 이펙트가 앞(대상 쪽)으로 나가는지 스크린샷, (2) 요소별 방향 옵션(`assetFacesLeft`, `clipFacesLeft`/`framesFacesLeft`/`bodyFacesLeft`/`loopFacesLeft`/`projFacesLeft`, `noFlip`)을 클립 단위로, (3) 투사체는 대상 방향으로 반전, (4) 모션 전환도 방향 유지. 작은 스크린샷만 보고 판단하지 말 것 — 2026-09-18 두 번 틀려 사용자가 화냄.
- Scope: global(전투 연출 전부)
- Rationale: User feedback 2026-09-18 — 팔라딘 이펙트가 등 뒤로 나감 → "공격 이펙트도 반대로 나가네. 바라보는 방향으로 나가야함. 모든 캐릭 공통" / 폭풍의 시 keydown 반대 → "스킬 이펙트나 모션 등 전부 방향 신경써" / 신궁 피어싱에서 또 뒤집었다 되돌림 → "너 왜 자꾸 공격 이펙트 반대로 넣어서 꼭 한번 더 말하게 하게끔 하는거야?" — 사용자에게 보여주기 전에 내가 확인해야 한다
- CLAUDE.md application: not needed(non-code 검증 습관)
- Priority: takes precedence over defaults

## Play 중에 고친 스크립트는 Stop 뒤 `maker_refresh_workspace` 없이는 안 반영된다
- Rule: Play Test가 돌아가는 동안 외부(파이썬/에디터)로 `.mlua`를 고쳤다면, `maker_stop` → **`maker_refresh_workspace`** → `maker_save` → `maker_play` 순서로 돌린다. refresh 없이 save+play 하면 Maker 메모리의 옛 스크립트로 실행된다(디스크 파일은 덮이지 않았지만 Play는 옛 값).
- Scope: project
- Rationale: 2026-09-18 — RtsCombatLogic `UnitNo`를 7→1로 고친 뒤 stop→save→play 했는데 로그가 계속 "unit 7"; refresh 후에야 "unit 1". 실행 결과가 파일과 다르면 먼저 이걸 의심.
- CLAUDE.md application: candidate(Testing 절차에 refresh 단계 추가 제안 가능)
- Priority: takes precedence over defaults

## Play 화면은 사용자가 보고 있다 — 루프 정지·슬로모 같은 화면 개입은 먼저 알리고, 끝나면 바로 복구
- Rule: 시험대 공격 루프 정지, 슬로모(PlayRate), 홀드 미리보기, 모션 캡처 등 Play 화면 상태를 바꾸는 작업은 시작 전에 한 줄로 알리고("캡처하느라 n분 루프 멈춥니다"), 끝나는 즉시 원래 상태(루프 재시작 또는 stop→refresh→save→play)로 되돌린다. 캡처 작업이 길면(5분↑) 중간에 진행 상황을 한 번 말한다.
- Scope: project
- Rationale: User feedback 2026-09-19 — 모션 35종 캡처하느라 히어로 루프를 멈춘 채 10분 넘게 진행 → "머해", "캐릭터 멈췃잖아", "눈으로 보게 해줘야할거아냐". 사용자는 Play 화면을 계속 보며 결과를 확인한다.
- CLAUDE.md application: not needed(진행 방식)
- Priority: takes precedence over defaults

## 마크다운 표를 스크립트로 고칠 땐 표 범위를 먼저 잘라낸 뒤 행을 치환한다
- Rule: `^\| 직업명 \|` 같은 정규식으로 행을 바꿀 때 같은 이름으로 시작하는 행이 여러 표(직업 특성 표·사거리 표·요약표)에 있으므로, 반드시 `## 절 제목`으로 그 표 구간을 먼저 슬라이스한 뒤 그 안에서만 치환한다. 치환 뒤엔 바뀐 표 전체를 한 번 눈으로 확인(열 개수·텍스트 칸이 숫자로 바뀌지 않았는지).
- Scope: project
- Rationale: 2026-09-19 balance-detail.md — 사거리 표를 겨냥한 정규식이 위쪽 직업 특성 표 행을 먼저 매치해 공격속도·역할 칸을 DPS 숫자로 덮어씀. 두 번의 패치를 거친 뒤에야 발견해 11행을 원문에서 다시 써야 했다.
- Priority: takes precedence over defaults

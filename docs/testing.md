# Testing

## 원칙
이 스택(MSW Maker)에는 `.mlua`를 실행하는 CLI 테스트 러너·빌드 명령이나 자동화 스펙 파일이 **없다**. Maker Play Test + 로그/스크린샷으로 검증한다. `.beaver/config.json`의 `commands`와 `test_glob`은 비워 둔다. `@Logic`·`script … extends Logic`·`@Sync` 같은 확장 문법을 일반 Lua 문법 검사기로 판정하지 않는다 (`RootDesk/MyDesk/RtsStageLogic.mlua:5-14`).

`python tools/gen-stage-table.py --check`는 파일을 쓰지 않고 132개 스테이지와 참조·메소·체력 제약을 검산한다 (`tools/gen-stage-table.py:19,28,598-643`). 게임 코드의 빌드나 Play Test를 대신하지 않는다.

## 검증 절차 (msw-maker-mcp)
1. `maker_save` — 편집 내용 저장 (미저장 상태로 맵 이동/플레이 시 유실 위험)
2. `maker_logs(kind:"build")` — 스크립트 문법/검증 오류 먼저 확인 (빌드 콘솔)
3. `maker_play` — Play Test 시작
4. `maker_logs(kind:"normal")` — 런타임(클라이언트/서버) 로그·에러 확인. 게임 스크립트 로그는 기본으로 꺼져 있다(`RtsConfigLogic.DebugLog = false`) — 흐름 로그가 필요하면 Play 중 `maker_execute_script`로 `server_main`과 `client` 각각 `_RtsConfigLogic.DebugLog = true`. 엔진 오류(LEA-…)는 스위치와 상관없이 찍힌다
5. `maker_screenshot` — 화면 상태 확인, `maker_keyboard_input`/`maker_mouse_input`으로 조작 재현
6. `maker_stop` — 편집 모드 복귀
- Play 중에 외부(파이썬/에디터)로 `.mlua`를 고쳤다면: `maker_stop` → **`maker_refresh_workspace`** → `maker_save` → `maker_play`. refresh 없이 save+play하면 Maker 메모리의 옛 스크립트로 실행된다(디스크 파일은 그대로지만 Play는 옛 값). 실측 2026-09-18 — `UnitNo`를 7→1로 고친 뒤 stop→save→play 했는데 로그가 계속 "unit 7", refresh 후에야 "unit 1". 실행 결과가 파일과 다르면 먼저 이것을 의심한다.

## 케이스 규칙 (standard)
- 기능당 최소: 정상 동작 1건 + 실패/경계 1건(잘못된 입력, 권한 없는 클라이언트 호출 등)을 Play Test 시나리오로 기술하고 로그로 확인한다.
- 서버 검증 로직은 클라이언트에서 우회 호출이 막히는지 확인한다 (WorldConfig의 AuthorityCheck 활성 상태, 근거: Global/WorldConfig.config:17-18).

## 데이터 검증 (Data-Access Smoke)
- 현재 저장 경로: `RtsProfileLogic`은 UserDataStorage의 선택·보유 키를 읽고 쓴다 (`RootDesk/MyDesk/RtsProfileLogic.mlua:14-31,184-239`). `RtsRunResultLogic`은 `BestRun`과 난이도별 `RtsBm4Clear_D<n>`(어려움 이상 검은 마법사 4페이즈 클리어 횟수 순위), `RtsRankNick`을 쓴다 (`RootDesk/MyDesk/RtsRunResultLogic.mlua:25-44,181-215,265-291`).
- Play Test 전 `maker_reset_data_storage`로 로컬 저장소를 초기화해 시나리오를 재현 가능하게 만들고, 저장→재접속(재플레이)→로드 왕복을 1회 확인한다.
- 데이터 접근을 모킹하는 단위 테스트가 없으므로 저장 키 호환성·콜백 실패·서버/클라이언트 동기화는 위의 실제 저장 왕복으로 확인한다.
- 몬스터 크기를 시각적으로 점검할 때는 각 구역에 6×3 격자로 세우고 `RtsTrackWalkerComponent`를 `Paused`·`Enable=false`로 둔다. 한 번에 50~70마리씩 나눠 스폰하고 F1~F8로 구역을 본다. 사용자가 직접 플레이 중이면 먼저 허락을 받아야 한다 (`.beaver/memory/workflow.md:117-122`).

## 회귀 실패 처리
- 빌드 콘솔 오류(문법)는 즉시 수정 후 재확인. 런타임 오류는 로그의 스택/메시지를 근거로 원인 스크립트를 수정하고 동일 시나리오를 재실행한다.

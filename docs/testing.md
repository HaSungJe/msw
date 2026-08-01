# Testing

## 원칙
이 스택(MSW Maker)에는 CLI로 실행 가능한 테스트 러너·빌드 명령이 **없다**. 자동화된 스펙 파일 대신 Maker Play Test + 로그/스크린샷 확인이 검증 수단이다. (`.beaver/config.json`의 `commands.test`는 비워 둔다 — 존재하지 않는 명령을 발명하지 않는다.)

## 검증 절차 (msw-maker-mcp)
1. `maker_save` — 편집 내용 저장 (미저장 상태로 맵 이동/플레이 시 유실 위험)
2. `maker_logs(kind:"build")` — 스크립트 문법/검증 오류 먼저 확인 (빌드 콘솔)
3. `maker_play` — Play Test 시작
4. `maker_logs(kind:"normal")` — 런타임(클라이언트/서버) 로그·에러 확인
5. `maker_screenshot` — 화면 상태 확인, `maker_keyboard_input`/`maker_mouse_input`으로 조작 재현
6. `maker_stop` — 편집 모드 복귀

## 케이스 규칙 (standard)
- 기능당 최소: 정상 동작 1건 + 실패/경계 1건(잘못된 입력, 권한 없는 클라이언트 호출 등)을 Play Test 시나리오로 기술하고 로그로 확인한다.
- 서버 검증 로직은 클라이언트에서 우회 호출이 막히는지 확인한다 (WorldConfig의 AuthorityCheck 활성 상태, 근거: Global/WorldConfig.config:17-18).

## 데이터 검증 (Data-Access Smoke)
- 현재 데이터 저장 계층(DataStorage) 사용 없음 — 도입 시 이 절을 갱신한다.
- 도입 후: Play Test 전 `maker_reset_data_storage`로 로컬 저장소를 초기화해 시나리오를 재현 가능하게 만들고, 저장→재접속(재플레이)→로드 왕복을 1회 확인한다.

## 회귀 실패 처리
- 빌드 콘솔 오류(문법)는 즉시 수정 후 재확인. 런타임 오류는 로그의 스택/메시지를 근거로 원인 스크립트를 수정하고 동일 시나리오를 재실행한다.

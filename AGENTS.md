# 프로젝트 작업 규칙

## 먼저 읽을 것

- 작업 전 `.beaver/memory/MEMORY.md`와 관련 주제 파일을 읽는다. 우선순위는 사용자 지시 → `.beaver/memory/` → 이 문서와 연결된 `docs/` → 일반 관례다. 답변과 진행 보고는 한국어로 쓴다 (`.beaver/memory/workflow.md:70-71`).
- 화면은 `docs/ui-screens.md`, 엔진 실측은 `docs/msw-engine.md`, 맵 테마는 `docs/theme-presets.md`, 유닛 원화는 `docs/unit-art.md`를 따른다. 남은 일은 `.beaver/output/roadmap/maple-augment-defense-roadmap.md`에서 확인한다.
- `.info/`는 로컬 설계 원본이다. 관련 기능을 만들거나 수치를 바꿀 때 읽되 커밋하지 않는다 (`.beaver/memory/workflow.md:64-65`).

## 주의

- `Environment/NativeScripts/**/*.d.mlua`는 엔진 선언 레퍼런스이므로 수정하지 않는다. `.mcp.json`과 `.codex/`에는 접속 정보가 있을 수 있어 커밋하지 않는다 (`docs/architecture.md`, `.gitignore`).
- `*.map`, `*.model`, `*.config`는 Maker 직렬화 자산이다. 구조를 추측해 직접 바꾸지 말고 가능하면 Maker 도구를 쓴다. 맵 이동·Play 전에 `maker_save`를 한다 (`docs/testing.md`).
- 사용자가 Maker에서 플레이 중이면 시험 스폰이나 화면 조작을 하지 않는다. Play 화면에 영향을 주는 캡처·슬로모·루프 중지는 미리 알리고 끝나면 복구한다 (`.beaver/memory/workflow.md:45-49,117-122`).

## 구조

- MapleStory Worlds Maker(CoreVersion 26.7.0.0)의 ExtendedScriptFormat mlua 프로젝트다 (`Environment/config:1`, `Global/WorldConfig.config:16-21`). 현재 맵은 `map/RtsMap.map`, 게임 코드는 `RootDesk/MyDesk/Rts*.mlua` 30개와 대응 `.codeblock` 30개다 (`docs/architecture.md`).
- 입장 이벤트 → `RtsBootstrapLogic` → 구역·카메라·스테이지·프로필 초기화 → HUD와 서버 스테이지 루프의 흐름을 따른다. 엔티티별 동작은 `Component`, 전역 게임 규칙·표·UI는 해당 `Logic`에 둔다 (`docs/architecture.md`).
- 정의만 있는 기능을 활성 기능으로 취급하지 않는다. 진입점과 호출 지점까지 확인한다.

## 코드 작성

- 게임 스크립트는 PascalCase의 `Rts…Logic`·`Rts…Component`; `property`·`method`는 PascalCase, 지역 변수는 camelCase다 (`docs/conventions.md`).
- 서버 RPC는 `@ExecSpace("Server")`로 표시하고 `senderUserId`로 호출자·소유 구역·유닛·상태·입력 범위를 재검증한다. 서버 내부 처리와 클라이언트 연출은 해당 실행 공간으로 나눈다. 공용 계산 메서드는 주석이 없는 기존 사례도 있으므로 모든 메서드에 `@ExecSpace`를 강제하지 않는다 (`docs/conventions.md`).
- 로그는 `_RtsConfigLogic:Log`를 사용한다. `DebugLog=false`가 기본이다 (`RootDesk/MyDesk/RtsConfigLogic.mlua:1-9`). 숫자 식별자·표시값에는 정수 포맷을 쓴다 (`docs/conventions.md`).
- `RtsStageTableLogic.mlua`의 생성 구간은 직접 수정하지 않는다. `.info/` 또는 `tools/gen-stage-table.py`를 고치고 `python tools/gen-stage-table.py --check`로 검산한다 (`docs/conventions.md`).
- 입력 거부와 화면 전달은 [요청·결과 규칙](docs/error-handling.md), 영구 저장은 [데이터 규칙](docs/data-layer.md)을 따른다. 불확실한 mlua API는 엔진 선언 또는 msw-mcp 문서 검색으로 확인한다.

## 화면·자산 협업

- 일반 UI 디자인은 ChatGPT가 이미지와 `docs/design/<주제>.md` 가이드라인을 만들고 `assets/design/<주제>/`에 둔다. Claude는 구현 요청 상태의 가이드라인을 바탕으로 리소스 연결·코드·Maker 확인을 맡는다. 가이드에 없는 디자인 판단은 사용자에게 묻는다 (`.beaver/memory/workflow.md:139-143`, `docs/design-handoff.md`).
- 캐릭터 원화·대기·스킬 프레임·흉상은 별도 규칙인 `docs/unit-art.md`를 따른다. 맡은 에이전트가 생성·적용·검증까지 한다. 원화의 표정·외모·의상을 사용자에게 보여 주고 OK를 받은 뒤에만 프레임을 만든다.
- 팝업 일부가 바뀌면 해당 컨테이너·선택 표시만 갱신하고 창 전체를 다시 열지 않는다 (`docs/ui-screens.md:510-518`). 화면 문구에는 티어·서포터 같은 개발용 분류를 쓰지 않는다 (`.beaver/memory/workflow.md:110-114`).

## 검증과 기록

- `.mlua`용 CLI 테스트·빌드 러너는 없다. Maker의 build 로그, Play Test, normal 로그, 화면 확인으로 검증한다. 외부에서 Play 중 코드를 고쳤다면 `maker_stop → maker_refresh_workspace → maker_save → maker_play` 순서로 다시 시작한다 (`docs/testing.md`).
- 커밋·푸시는 각각 사용자의 명시 승인을 받은 뒤에만 한다 (`.beaver/memory/workflow.md:17-22`). 커밋 메시지는 첫 줄 `YYYY.MM.DD vYYMMDD-N`(N은 그날의 순번, 날짜가 바뀌면 1), 빈 줄 뒤 `* ` 불릿으로 쓰고 Co-Authored-By·Generated-with 같은 트레일러를 붙이지 않는다 (`.beaver/memory/workflow.md:97-101`).

## 점검

- [ ] 엔진 선언과 비밀 설정을 수정·커밋하지 않았다.
- [ ] 새 스크립트 이름과 책임이 `Logic`·`Component` 경계에 맞는다.
- [ ] 서버 요청이 `senderUserId`와 소유권·입력 범위를 검증한다.
- [ ] 생성 테이블을 직접 고치지 않았고 필요하면 생성기 검산을 했다.
- [ ] UI는 바뀐 부분만 갱신하며 기존 화면 상태를 보존한다.
- [ ] 저장 기능은 재접속 후 읽기까지 확인했다.
- [ ] Maker build·Play 로그와 화면에서 관련 기능을 확인했다.

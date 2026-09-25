# 코드 작성 규약

## 이름과 파일

- 게임 스크립트는 `Rts…Logic.mlua` 또는 `Rts…Component.mlua`이고 파일명과 스크립트명이 일치한다 (`RootDesk/MyDesk/RtsBootstrapLogic.mlua:2-3`, `RootDesk/MyDesk/RtsUnitAttackComponent.mlua:5-6`). 대응하는 `.codeblock`도 유지한다.
- `property`와 `method`는 PascalCase, 지역 변수는 camelCase다 (`RootDesk/MyDesk/RtsProfileLogic.mlua:15,41,91-94`, `RootDesk/MyDesk/RtsUnitLogic.mlua:323-327`).
- 숫자를 엔티티 이름·키·화면 문구에 넣을 때는 `tostring`의 `1.0` 형태를 피하고 정수 포맷을 쓴다 (`RootDesk/MyDesk/RtsUnitLogic.mlua:351-360`, `docs/msw-engine.md:26-28`).

## 실행 공간과 서버 요청

- `@ExecSpace("Server")`는 클라이언트가 호출하는 요청, `ServerOnly`는 서버 내부 처리, `Client`·`ClientOnly`는 클라이언트 갱신·연출에 사용한다 (`RootDesk/MyDesk/RtsProfileLogic.mlua:270-291,410-420`). 모든 공용 계산 메서드에 주석을 붙이는 규칙은 현재 코드와 다르다 (`RootDesk/MyDesk/RtsStageLogic.mlua:103-130`).
- 서버 요청은 `senderUserId`에서 호출자를 얻고 판 상태·소유 유닛 또는 구역·입력 범위를 서버에서 다시 확인한 뒤 변경한다. 클라이언트 버튼 숨김만으로 권한을 대신하지 않는다 (`RootDesk/MyDesk/RtsUnitLogic.mlua:322-361,508-528`, `RootDesk/MyDesk/RtsProfileLogic.mlua:288-319`).
- 거부는 현재 요청 메서드에서 주로 조기 `return`한다. 개발 로그는 `_RtsConfigLogic:Log`로만 남기며 기본 `DebugLog=false`다 (`RootDesk/MyDesk/RtsUnitLogic.mlua:322-361`, `RootDesk/MyDesk/RtsConfigLogic.mlua:1-9`).

## 상태·생성 데이터·화면

- 엔티티 상태·수명주기는 `Component`, 판 진행·표·UI·유저 상태는 해당 `Logic`에 둔다 (`RootDesk/MyDesk/RtsUnitComponent.mlua:7-58`, `RootDesk/MyDesk/RtsStageLogic.mlua:9-18`, `RootDesk/MyDesk/RtsProfileLogic.mlua:40-86`).
- `RtsStageTableLogic.mlua`의 `BEGIN GENERATED`부터 `END GENERATED`까지는 손으로 고치지 않는다. `.info/monster-wave.md`·`.info/monster.md` 또는 `tools/gen-stage-table.py`의 `MOB_SIZE`·`DISPLAY_THEME` 등을 고친 뒤 `python tools/gen-stage-table.py --check`로 검산하고 재생성 전후 diff를 확인한다. 표시 이름만 바꿀 때는 체력 압박에 쓰는 `THEMES` 대신 `DISPLAY_THEME`을 쓴다 (`RootDesk/MyDesk/RtsStageTableLogic.mlua:1-8,82-86`, `tools/gen-stage-table.py:19,28`).
- 팝업 일부가 바뀌면 고정 틀을 유지하고 바뀐 컨테이너·선택 표시만 갱신한다. `Open(같은 kind)`로 창 전체를 다시 열지 않는다. 상세 방식은 [화면 설계](ui-screens.md) 7.3절을 따른다 (`docs/ui-screens.md:505-518`, `.beaver/memory/workflow.md:132-136`).

불확실한 MSW API·리소스 조작은 [엔진 기록](msw-engine.md)과 엔진 선언을 확인한다. UI 디자인, 캐릭터 그림, 맵 테마는 각각 [화면 설계](ui-screens.md), [유닛 원화](unit-art.md), [테마 프리셋](theme-presets.md)을 따른다.

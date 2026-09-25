# 구조와 실행 경계

## 현재 구성

| 위치 | 역할과 근거 |
|---|---|
| `map/RtsMap.map` | 현재 맵과 RectTileMap 직렬화 자산 (`map/RtsMap.map:4,18-42,109-164`). 맵 구조는 Maker에서 다룬다. |
| `Global/` | 월드 설정과 공용 엔티티. `Global/WorldConfig.config:16-21`은 권한 검사와 ExtendedScriptFormat을 켠다. `Global/common.gamelogic:17-32`는 현재 비어 있다. |
| `RootDesk/MyDesk/` | 게임 코드: `Rts*.mlua` 30개와 대응하는 `.codeblock` 30개. `Logic`은 게임 규칙·UI·테이블을, `Component`는 엔티티 수명주기·상태를 담당한다 (`RtsBootstrapLogic.mlua:2-3`, `RtsUnitComponent.mlua:1-58`). |
| `Environment/NativeScripts/` | 엔진이 제공하는 `.d.mlua` 선언과 API 서명. 프로젝트 코드가 아니므로 수정하지 않는다. |
| `tools/`, `assets/`, `docs/` | 오프라인 생성·검산 도구, 게임 자산, 제작·검증 절차. `RtsStageTableLogic.mlua:1-8`은 표의 생성 원본을 `tools/gen-stage-table.py`로 지정한다. |

## 시작에서 화면과 전투까지

1. `RtsBootstrapLogic`의 입장·퇴장 이벤트가 구역을 배정하고 지형을 준비하고 `RtsCameraAnchorComponent`를 붙이고 스테이지와 프로필 로드를 시작한다 (`RtsBootstrapLogic.mlua:5-38`).
2. 카메라 앵커의 클라이언트 `OnBeginPlay`가 HUD를 만들고, HUD는 `/ui` 그룹을 채운다 (`RtsCameraAnchorComponent.mlua:10-15,28-54`; `RtsHudLogic.mlua:353-373`).
3. `RtsStageLogic`의 서버 타이머가 카운트다운과 스테이지를 진행하며 웨이브 또는 보스를 호출한다 (`RtsStageLogic.mlua:103-108,154-164,363-408`).
4. `RtsWaveLogic`은 몬스터에 `RtsMonsterComponent`와 `RtsTrackWalkerComponent`를 붙인다 (`RtsWaveLogic.mlua:68-111`). `RtsUnitLogic`은 영입 유닛에 `RtsUnitAttackComponent`와 `RtsUnitComponent`를 붙이고 공격 루프를 시작한다 (`RtsUnitLogic.mlua:195-239`).
5. 화면 입력은 `RtsUnitSelectLogic` 등을 거쳐 서버 요청으로 들어간다. 서버는 `senderUserId`, 판 상태, 구역, 발판, 한도를 다시 확인한다 (`RtsUnitSelectLogic.mlua:459-470`; `RtsUnitLogic.mlua:322-361`).

스크립트 간 호출은 엔진 전역 `_RtsXLogic`을 사용한다. `@Sync` 프로퍼티와 `@ExecSpace`로 서버·클라이언트 경계를 표시한다 (`RtsStageLogic.mlua:9-10,190-199`). 공용 읽기·계산 메서드는 실행 공간 주석 없이 정의된 경우도 있다 (`RtsStageLogic.mlua:103-130`).

## 새 기능을 붙이는 순서

1. 상태가 전역 게임 규칙인지 엔티티별 수명주기인지 결정한다. 전자는 `Rts…Logic`, 후자는 `Rts…Component`의 기존 책임을 확인한다 (`RtsStageLogic.mlua:5-18`; `RtsUnitComponent.mlua:1-58`).
2. 게임 진입점과 실제 호출 지점을 연결한다. 파일 정의만으로 활성 기능으로 기록하지 않는다. 예를 들어 `RtsBossLogic:OnBossReachedEnd`의 호출은 존재하지만 현재 보스는 `Paused=true`로 생성되어 이동 종료 경로는 일반 플레이에서 닿지 않는다 (`RtsTrackWalkerComponent.mlua:65-67`; `RtsBossLogic.mlua:79-85`).
3. 클라이언트 입력·연출과 서버 판정·저장을 나누고, 서버 요청에서 사용자 소유권을 검증한다. [코딩 규약](conventions.md)과 [데이터](data-layer.md)를 따른다.
4. 맵·모델·설정은 Maker 직렬화 자산이므로 Maker에서 연결하고 [Play Test 절차](testing.md)로 확인한다.

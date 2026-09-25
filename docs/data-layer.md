# 데이터와 상태

## 상태 소유

- `RtsStageLogic`의 `@Sync` 값은 판 진행 정보를 양쪽 실행 공간에 전달한다 (`RootDesk/MyDesk/RtsStageLogic.mlua:9-18`). `RtsUnitComponent`에는 엔티티별 상태가 있다 (`RootDesk/MyDesk/RtsUnitComponent.mlua:7-58`).
- 프로필은 서버의 `ThemeByUser`·`IconByUser`·`TombByUser`·보유 목록이 원본이고 클라이언트의 `MyTheme` 등은 `SendProfileState`로 갱신된다 (`RootDesk/MyDesk/RtsProfileLogic.mlua:40-86,270-276,412-420`).

## 영구 저장

| 소유 스크립트 | 저장소·키 | 근거 |
|---|---|---|
| `RtsProfileLogic` | UserDataStorage의 `theme`, `icon`, `tomb`, `icons`, `themes`, `tombs`. 기존 키를 바꾸면 저장된 사용자 데이터와 호환되지 않는다. | `RootDesk/MyDesk/RtsProfileLogic.mlua:14-31,184-239` |
| `RtsRunResultLogic` | UserDataStorage의 `BestRun`, 난이도별 SortableDataStorage의 `RtsBm4Clear_D<n>`, GlobalDataStorage의 `RtsRankNick`. 순위 저장은 어려움 이상·비시험 판의 검은 마법사 4페이즈 클리어에 적용된다. | `RootDesk/MyDesk/RtsRunResultLogic.mlua:25-44,181-215,265-291` |

프로필은 읽기 결과를 확인하고 기본값을 마련하며, 변경 요청에서 소유자·선택 가능 여부를 검증하고 `SetAsync` 콜백 결과를 확인한 뒤 상태를 보낸다 (`RootDesk/MyDesk/RtsProfileLogic.mlua:184-239,288-319`). 결과·순위 저장도 비동기이지만 일부 쓰기 콜백은 성공 코드를 검사하지 않는다 (`RootDesk/MyDesk/RtsRunResultLogic.mlua:213,271,277`). 모든 쓰기의 성공이 확인됐다고 가정하지 않는다.

새 사용자 필드는 서버 소유 키와 기본값, 기존 데이터가 없는 경우, 저장 성공 후 클라이언트 전달, 재접속 시 복원을 한 묶음으로 설계하고 [검증 절차](testing.md)에서 왕복을 확인한다.

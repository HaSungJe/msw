# 데이터와 상태

## 상태 소유

- `RtsStageLogic`의 `@Sync` 값은 판 진행 정보를 양쪽 실행 공간에 전달한다 (`RootDesk/MyDesk/RtsStageLogic.mlua:9-18`). `RtsUnitComponent`에는 엔티티별 상태가 있다 (`RootDesk/MyDesk/RtsUnitComponent.mlua:7-58`).
- 프로필은 서버의 `ThemeByUser`·`IconByUser`·`TombByUser`·보유 목록이 원본이고 클라이언트의 `MyTheme` 등은 `SendProfileState`로 갱신된다 (`RootDesk/MyDesk/RtsProfileLogic.mlua:40-86,270-276,412-420`).
- 화면 모드는 서버 `UiModeByUser`가 원본이고 클라이언트 `MyUiMode`는 `ReceiveUiMode`로 갱신한다. 기본은 `light`, 선택값 `dark`는 해당 계정의 다음 접속에도 읽는다. 저장 성공 전 화면을 변경하지 않고, 읽기 실패 시 저장을 막아 기존 값을 보존한다.

## 영구 저장

| 소유 스크립트 | 저장소·키 | 근거 |
|---|---|---|
| `RtsProfileLogic` | UserDataStorage의 `theme`, `icon`, `tomb`, `icons`, `themes`, `tombs`. 기존 키를 바꾸면 저장된 사용자 데이터와 호환되지 않는다. | `RootDesk/MyDesk/RtsProfileLogic.mlua:14-31,184-239` |
| `RtsProfileLogic` 화면 설정 | 동일한 사용자 저장소의 `uiMode`: `light` / `dark`. 값 없음은 `light`; 신규 기본값 쓰기는 생략하며, 실제 변경 때만 저장한다. | `Load`, `RequestSetUiMode`, `ReceiveUiMode`; 검증 상태는 `docs/design/ui-dark-mode.md` |
| `RtsRunResultLogic` | UserDataStorage의 `BestRun`(도전모드 개인 최고), 난이도별 SortableDataStorage의 `RtsBestRound_D<n>`(n = 1~6, 값 = 최대 클리어 라운드 × 10^10 + 먼저 도달한 순 보정), GlobalDataStorage의 `RtsRankNick`. 순위 저장은 도전모드·비시험 판이 끝날 때(탈락·클리어) 기존보다 높을 때만 한다(`SaveBestRound`, 2026-09-28). 경주모드 판은 아무것도 저장하지 않는다. 옛 `RtsBm4Clear_D4~6`(클리어 횟수)은 지우지 않고 더 쓰지 않는다. | `RootDesk/MyDesk/RtsRunResultLogic.mlua` `Finish`·`SaveBestRound`·`RequestRanking` |

프로필은 읽기 결과를 확인하고 기본값을 마련하며, 변경 요청에서 소유자·선택 가능 여부를 검증하고 `SetAsync` 콜백 결과를 확인한 뒤 상태를 보낸다 (`RootDesk/MyDesk/RtsProfileLogic.mlua:184-239,288-319`). 결과·순위 저장도 비동기이지만 일부 쓰기 콜백은 성공 코드를 검사하지 않는다 (`RootDesk/MyDesk/RtsRunResultLogic.mlua:213,271,277`). 모든 쓰기의 성공이 확인됐다고 가정하지 않는다.

새 사용자 필드는 서버 소유 키와 기본값, 기존 데이터가 없는 경우, 저장 성공 후 클라이언트 전달, 재접속 시 복원을 한 묶음으로 설계하고 [검증 절차](testing.md)에서 왕복을 확인한다.

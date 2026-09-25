# 요청 거부와 결과 전달

이 게임의 진입점은 HTTP 경로가 아니라 엔진 이벤트·화면 입력·서버 RPC다. HTTP 상태 코드나 공통 JSON 오류 포맷은 없다. 화면 입력은 서버 요청으로 이어지고, 서버가 상태·사용자·구역·칸·한도를 다시 검사한다 (`RootDesk/MyDesk/RtsUnitSelectLogic.mlua:459-470`, `RootDesk/MyDesk/RtsUnitLogic.mlua:322-361`).

| 상황 | 현재 처리 |
|---|---|
| 잘못된 입력·권한 없음 | 서버 요청에서 조기 `return`; 일부 경우에만 조건부 개발 로그 (`RootDesk/MyDesk/RtsUnitLogic.mlua:322-361`). |
| 사용자에게 반영할 상태 | 서버에서 `Client` 메서드로 값을 보내고 대상 `userId`를 전달 (`RootDesk/MyDesk/RtsProfileLogic.mlua:270-276,412-420`, `RootDesk/MyDesk/RtsRunResultLogic.mlua:295-299`). |
| 저장 실패 | `RtsProfileLogic`의 일부 `SetAsync` 콜백은 결과 코드를 확인한다. `RtsRunResultLogic`의 일부 콜백은 확인하지 않으므로 성공 보장을 일반화하지 않는다 (`RootDesk/MyDesk/RtsProfileLogic.mlua:307-318,393-405`, `RootDesk/MyDesk/RtsRunResultLogic.mlua:213,271,277`). |
| 로그 | `_RtsConfigLogic:Log`만 사용한다. `DebugLog=false`가 기본이며 서버·클라이언트에서 확인할 때만 켠다 (`RootDesk/MyDesk/RtsConfigLogic.mlua:1-9`). |

새 RPC는 변경 전에 서버에서 호출자와 대상의 관계를 검증한다. 실패를 사용자에게 보여줘야 한다면 기존 클라이언트 결과 전달 형태를 확인하고 해당 화면의 계약에 맞춰 보낸다. 조기 반환만으로 화면에 오류가 표시된다고 가정하지 않는다.

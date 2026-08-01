# Architecture

## 스택
| 항목 | 값 | 근거 |
|---|---|---|
| 엔진 | MapleStory Worlds Maker, CoreVersion 26.7.0.0 | Environment/config:1 |
| 스크립트 | mlua (ExtendedScriptFormat) | Global/WorldConfig.config:21 |
| 소스 언어 | ko | Global/WorldConfig.config:20 |
| 월드 | 개인 월드 (worldId c7127d5fb5e64537bf0520c1418932e4) | maker_get_world_info 측정 |
| MCP | msw-maker-mcp(로컬 Maker 제어), msw-mcp(원격: mlua 문서/API, 월드 아이템·배지, 리소스 스토리지) | .mcp.json |

## 디렉터리 레이아웃
- `map/map01.map` — 유일한 맵. 엔티티: `/maps/map01` (MapComponent + FootholdComponent), Background, MapleMapLayer, TileMap(타일 비어 있음). (측정: map/map01.map:15-168)
- `Global/` — 월드 전역 자산:
  - `WorldConfig.config` — 월드 설정(권한 체크 활성: PlayerEntityAuthorityCheck/ServiceAuthorityCheck true)
  - `common.gamelogic` — 공용 게임로직 루트 엔티티 `/common` (아직 컴포넌트 없음)
  - `DefaultPlayer.model`, `CustomAvatarAction`/`CustomBodyAction`, `CollisionGroupSet`, `CustomFontGroupSet`
- `RootDesk/MyDesk.directory` — 사용자 작업 공간 루트. 새 스크립트·모델·UI는 Maker를 통해 이 아래에 생성된다.
- `Environment/NativeScripts/` — 엔진 제공 `.d.mlua` 선언(Component/Logic/Service/Struct 등 약 600파일). **읽기 전용 API 레퍼런스** — 사용 가능한 컴포넌트·이벤트·서비스 시그니처는 여기서 확인.

## 레이어/유닛 경계 (standard: MSW 권장)
- **Component** — 엔티티에 부착되는 동작 단위. 엔티티 수명주기(OnBeginPlay/OnUpdate 등) 이벤트를 받는다.
- **Logic** — 엔티티와 무관한 전역 로직/유틸. `_LogicName`으로 어디서든 접근.
- **EventType** — 커스텀 이벤트 정의. Component/Logic 간 통신은 이벤트 발행·핸들러로.
- 실행 공간: Server(권한 로직·저장), Client(입력·연출), ServerOnly/ClientOnly 프로퍼티 sync 규칙을 따른다.

## 새 도메인(기능) 추가 최소 구조 (standard: MSW 권장)
1. `RootDesk/MyDesk` 아래에 `<Domain>Component` (엔티티 동작) 및 필요 시 `<Domain>Logic` (전역 규칙) 생성.
2. 서버 권한 로직은 `@ExecSpace("Server")`, 클라이언트 입력/연출은 `@ExecSpace("Client")`로 분리.
3. Component ↔ Logic 통신이 느슨해야 하면 EventType 정의 후 이벤트로 연결.
4. 맵 배치가 필요하면 Maker에서 엔티티에 Component 부착(모델화 권장).
5. Play Test로 검증(→ docs/testing.md).

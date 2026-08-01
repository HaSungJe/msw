# CLAUDE.md

## ⚠️ Cautions
- `Environment/NativeScripts/**/*.d.mlua`는 엔진이 생성한 선언 파일(읽기 전용 레퍼런스)이다. 절대 수정하지 않는다. (측정: Environment/NativeScripts/ 전체)
- `.mcp.json`에는 msw-mcp Bearer 토큰이 포함되어 있다. 커밋 금지(.gitignore에 등록됨).
- 맵/모델/설정 파일(`*.map`, `*.model`, `*.config` 등)은 Maker가 직렬화하는 JSON이다. 구조를 임의로 바꾸지 말고, 가능하면 Maker MCP 도구(maker_* )로 조작한다.
- Play Test 실행/중지는 Maker MCP(`maker_play`/`maker_stop`)로 수행한다. 저장되지 않은 편집이 있는 상태에서 `maker_move_map`을 호출하면 유실된다 — 먼저 `maker_save`.

## Architecture
스택: MapleStory Worlds (Maker CoreVersion 26.7.0.0, 측정: Environment/config:1) · 스크립트 언어 mlua(Lua 기반, ExtendedScriptFormat 사용, 측정: Global/WorldConfig.config:21) · 로컬 Maker 에디터 + msw-maker-mcp / msw-mcp(원격 API) 연동(측정: .mcp.json)

```
map/          # 맵 엔티티 (map01.map — MapComponent/Foothold/Background/TileMap)
Global/       # 월드 전역 설정: WorldConfig, common.gamelogic(공용 게임로직 루트), 아바타 액션, 충돌 그룹
RootDesk/     # 사용자 작업 공간(MyDesk) — 스크립트·모델·UI 등 제작물이 여기에 추가됨
Environment/  # 엔진 제공 환경 — NativeScripts/*.d.mlua 선언(Component/Logic/Service 등), 수정 금지
.mswai/       # MSW AI CLI 부트스트랩 메타데이터(lock.json)
```
→ 상세: [docs/architecture.md](docs/architecture.md)

## Conventions (standard: MSW 권장)
- 스크립트 단위: `Component`(엔티티에 부착) / `Logic`(전역 로직) — 파일명 = 스크립트명, PascalCase (예: `PlayerMoveComponent`, `GameManagerLogic`). 엔진 네이티브 스크립트 네이밍과 동일 규칙(측정: Environment/NativeScripts/Component/*.d.mlua).
- Component 접미사 `Component`, Logic 접미사 `Logic`, EventType 접미사 없음(도메인 명사형).
- 프로퍼티·메서드는 PascalCase, 지역 변수는 camelCase.
- 실행 공간은 항상 명시: `@ExecSpace("Server")` / `@ExecSpace("Client")` / 멀티캐스트. 서버 권한 검증이 필요한 로직(재화·데이터 저장)은 Server 전용으로 작성.
- mlua API·문법이 불확실하면 추측하지 말고 msw-mcp의 `mlua_api_retriever` / `mlua_document_retriever`로 확인 후 작성.

## Shared Logic Separation (standard: MSW 권장)
- 순수 계산/유틸 함수 → `Logic` 스크립트로 분리(전역 접근 `_LogicName`).
- 엔티티 상태·수명주기에 묶인 로직 → `Component`.
- 공용 게임로직 루트는 `Global/common.gamelogic` 하위에 위치(측정: Global/common.gamelogic:18).

## Testing (standard: MSW — CLI 테스트 러너 없음)
- 이 스택에는 실행 가능한 CLI 테스트/빌드 명령이 없다. 검증은 Maker Play Test로 수행한다:
  1. `maker_save` → 2. `maker_play` → 3. `maker_logs(kind:"normal")`·`maker_screenshot`으로 동작/에러 확인 → 4. `maker_stop`.
- 스크립트 문법·검증 오류는 `maker_logs(kind:"build")`에서 확인한다.
- 서버 데이터 검증 시 `maker_reset_data_storage`로 로컬 DataStorage를 초기화할 수 있다.
→ 상세: [docs/testing.md](docs/testing.md)

## Checklist
- [ ] `Environment/NativeScripts` 하위 파일을 수정하지 않았다
- [ ] 새 스크립트가 PascalCase + 역할 접미사(`Component`/`Logic`) 네이밍을 따른다
- [ ] 모든 스크립트 메서드에 실행 공간(`@ExecSpace`)이 명시되어 있다
- [ ] 재화·저장 등 권한 민감 로직이 Server 실행 공간에만 있다
- [ ] 불확실한 mlua API는 `mlua_api_retriever`로 확인했다
- [ ] 맵/설정 JSON을 직접 수정한 경우 Maker에서 정상 로드되는지 확인했다
- [ ] Play Test(`maker_play` → `maker_logs`)에서 런타임/빌드 에러가 없다
- [ ] 변경 후 `maker_save`를 호출했다

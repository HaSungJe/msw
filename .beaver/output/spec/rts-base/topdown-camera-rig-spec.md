---
feature_goal: "탑다운 맵·카메라 리그 — RectTile 탑다운 맵 위에서 숨긴 아바타를 카메라 앵커로 삼아 스타크래프트식 화면 스크롤(방향키+엣지+휠줌+커서 가두기)을 제공"
domain: "rts-base"
api_method: "Scene + Client Input"
api_path: "map://RtsMap · RtsCameraAnchorComponent (DefaultPlayer 부착) · RtsConfigLogic"
affected_data: []
---

## Feature Description
벽짓살(탑다운 풀 RTS 디펜스)의 무대가 되는 기반 유닛. 이후 모든 유닛(#2 그리드, #3 선택/명령, #4 건설…)이 이 맵과 카메라 위에서 동작한다.

- MSW 네이티브 **RectTile 맵 모드**로 탑다운 필드를 만든다 (중력 영향 없음, 상하좌우 이동 — 근거: RectTileMap 공식 문서 "You can create a top-down view map", KinematicbodyComponent "top-down gameplay with RectTiles").
- 플레이어 아바타는 **숨기고 기본 조작을 끈 뒤 카메라 앵커로 재사용**한다. MSW 기본 카메라는 항상 자기 아바타를 따라오므로(유저별 분리가 공짜), 숨긴 아바타를 스크롤 입력으로 움직이면 그게 곧 RTS 카메라다. 별도 리그 엔티티 스폰/소유권 관리가 불필요해지고 멀티(#13)에도 그대로 확장된다.
- 스크롤: 방향키 + 마우스 엣지 스크롤(창 가장자리), 커서는 `CursorLockMode.Confined`로 창 안에 가둔다(창모드 이탈 방지, Windows PC 전용). 휠 줌은 카메라의 네이티브 zoom in/out 허용 옵션을 사용.

## Entry Point
- Method: Scene 진입(자동) + Client Input (InputService)
- Path: `map://RtsMap` (RectTile 모드, UseCustomBound 256×256셀 영역) / `RtsCameraAnchorComponent` (DefaultPlayer 모델에 부착) / `RtsConfigLogic` (튜너블 상수)
- Request(입력): 방향키(Arrow) KeyDown/KeyUp, 마우스 커서 위치(`GetCursorPosition()` 폴링), 마우스 휠(네이티브 줌)
- Response(결과): 카메라(=숨긴 아바타)가 맵 영역 안에서 스크롤·줌 됨. 아바타·이름표·그림자는 화면에 보이지 않음. 기본 점프/이동 조작 무효.

## Business Rules
1. **맵 크기 256×256셀** (사용자 확정). 셀 크기(월드 유닛 환산)는 Play Test에서 실측 후 `RtsConfigLogic.CellSize`로 고정한다. 맵 영역은 `MapComponent.UseCustomBound + LeftBottom/RightTop`으로 정의 — 이후 조정 가능.
2. 카메라 앵커 이동은 **클라이언트 전용**(자기 아바타만). 다른 유저 화면에 영향 없음. 서버는 아바타 숨김 처리만 담당(전 클라이언트 공통 표시를 위해 Enable(Sync) 프로퍼티를 서버에서 끔).
3. 카메라 앵커는 맵 영역(카메라 제한 영역) 밖으로 나가지 못한다 — `UseCustomBound` 영역 클램프 + 타일 충돌 비활성(`EnableTileCollision=false`, 카메라는 지형에 걸리면 안 됨).
4. 엣지 스크롤 발동 조건: 커서가 화면 가장자리 `EdgeMarginPx`(기본 20px) 이내. 방향키 입력과 합산되며 대각 이동 시 정규화한다.
5. 키보드/엣지 스크롤은 PC 전용. 모바일 대응은 로드맵 Open Decision에 따름(1차 제외).
6. UI 위에 커서가 있을 때(`IsPointerOverUI()`)는 엣지 스크롤을 계속 허용한다(스타크래프트 동일 동작). 단, 이후 유닛에서 문제가 되면 재검토.

## Notes
- **근거 API**(전부 msw-mcp 공식 문서로 확인, 2026-08-01): RectTileMap 문서(탑다운 모드), `KinematicbodyComponent`(MoveVelocity/SpeedFactor/EnableTileCollision/EnableShadow), `InputService`(GetCursorPosition·CursorLockMode.Confined·IsKeyPressed·KeyDown/UpEvent), `CameraComponent`(DeadZone/isAllowZoomInOut/UseCustomBound), `_UILogic.ScreenWidth/Height`, CustomPlayerController 패턴 문서(PlayerControllerComponent.Enable=false 후 직접 제어).
- DefaultPlayer는 Rigidbody/Kinematicbody/Sideviewbody를 모두 갖고 있고 맵 모드에 따라 제어 주체가 바뀜(RectTile → Kinematicbody) — 별도 컴포넌트 추가 불필요.
- 기존 `map01`(MapleTile 기본 맵)은 유지하고 `RtsMap`을 새로 만든다. 시작 맵 전환(또는 map01→RtsMap 이동)은 build 단계에서 Maker로 설정.
- 이 유닛에는 영속 데이터 없음(DataStorage 미사용).

## Proposals (Codebase-Based)
- [x] 신규 프로젝트라 재사용할 기존 코드 없음. CLAUDE.md 컨벤션(Component/Logic 분리, PascalCase, @ExecSpace 명시)을 그대로 적용 — 튜너블 상수는 로드맵 공통 규칙("밸런스 수치는 테이블로 일원화")에 따라 `RtsConfigLogic`으로 분리.

## Decisions
- [x] 맵 크기 — **256×256셀** (사용자 확정, 2026-08-01). 셀→월드 유닛 환산은 Play Test 실측 후 고정.
- [x] 카메라 구조 — **숨긴 아바타 = 카메라 앵커** (리그 스폰 방식 대신; 유저별 분리가 네이티브라 단순·멀티 안전). 설계 승인 시 사용자 동의.
- [x] 조작 세트 — 방향키 + 엣지 스크롤 + Confined 커서 + 휠 줌(네이티브). 브레인스토밍에서 확정.
- [x] 스크롤 속도·엣지 폭·줌 범위 — 튜너블 상수(`RtsConfigLogic`), 기본값 SCROLL_SPEED=8, EDGE_MARGIN_PX=20. Play Test에서 조정.

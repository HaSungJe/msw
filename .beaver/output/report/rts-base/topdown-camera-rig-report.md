# Report — 탑다운 맵·카메라 리그 (rts-base #1)

## Feature Summary
- **Feature**: RectTile 탑다운 맵(256×256셀) 위에서 숨긴 아바타를 카메라 앵커로 삼아 스타식 화면 스크롤(방향키+엣지+휠줌+Confined 커서) 제공
- **Entry point**: `Scene map://rtsmap` + `RtsCameraAnchorComponent`(런타임 부착) + `RtsBootstrapLogic`
- **Domain**: rts-base

## Created/Modified/Deleted Files
| File | Change Type | Description |
|------|-----------|------|
| `map/RtsMap.map` | created | RectTile(TileMapMode=1) 탑다운 맵. Maker 저장 시 정규화됨(EntryKey 소문자화, tileMap:[] 추가) |
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | created | 튜너블 상수(맵 256×256셀, CellSize 1, ScrollSpeed 8, EdgeMarginPx 20) + 게터/경계 계산 |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | created | 서버: 아바타/이름표/그림자/점프 비활성. 클라: 기본조작 차단, Confined 커서, DeadZone 0, 휠줌 허용, 카메라 경계, 맵 중앙 스폰, 방향키+엣지 스크롤, 경계 클램프 |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | created | UserEnterEvent(서버)에서 유저 엔티티에 컴포넌트 런타임 부착 |
| `RootDesk/MyDesk/*.codeblock` ×3 | created | Maker가 생성한 스크립트 메타 |

## 플랜 대비 변경점 (구현 중 확정)
1. **DefaultPlayer.model 수정 → 런타임 `AddComponent` 부착으로 대체** — 모델 JSON의 컴포넌트 직렬화 포맷이 미문서화라, 공식 문서에 있는 `Entity:AddComponent(string)` 패턴(RtsBootstrapLogic)으로 안전하게 구현.
2. **OnBeginPlay 이중 정의 → 단일 정의 + IsServer() 분기** — mlua는 동명 메서드 중복 정의 불가.
3. **Logic 프로퍼티 직접 접근 → 게터 메서드 경유** — 크로스 엔트리 프로퍼티 접근이 정적 분석 경고(LIA 1114/1115)를 유발해 메서드 호출로 변경.
4. **엣지 스크롤에 화면 밖 커서 가드 추가** — `GetCursorPosition()`이 뷰포트 밖 OS 커서 좌표를 그대로 반환해(실측: (60435,-57683)) 화면 범위 밖이면 엣지 스크롤을 무시하도록 수정. 이 가드가 없으면 창모드에서 카메라가 코너로 밀려남.
5. **시작 위치 = 맵 중앙(128,128)** — SetupClient에서 `SetWorldPosition`.

## Tests Written
CLI 러너 없음(docs/testing.md) — 플랜의 Play Test 시나리오가 테스트 명세이며, build 단계에서 1회 실측 완료(아래). `/beaver:test` 시 동일 절차로 회귀 확인.

## Verification (Play Test 실측, 2026-08-01)
| 시나리오 | 결과 | 근거 |
|---|---|---|
| 아바타/이름표/그림자 비표시 | ✅ | 스크린샷 2매 — 화면에 아바타 없음 |
| 방향키 스크롤 | ✅ | RightArrow 1.5s: x 128→139.95 (8유닛/초 정확), UpArrow 1.0s: y 128→135.98 |
| 스폰 = 맵 중앙 | ✅ | 로그 `spawn pos: 128.0, 128.0` |
| 경계 클램프 | ✅ | 커서 가드 수정 전 (256,0) 코너에 정확히 고정됨(=클램프 동작 실증) |
| 엣지 스크롤 | ✅(간접) | 가드 수정 전 화면 밖 커서에 반응해 지속 스크롤됨(동작 실증). 창 안 커서 실조작 확인은 수동 테스트 권장 |
| 휠 줌 / Confined 커서 | ⚠️ 미실측 | `IsAllowZoomInOut=true`·`CursorLockMode(Confined)` 설정 코드는 실행됨(에러 없음). MCP로 휠/OS커서 재현 불가 — 수동 확인 필요 |
| 기본 조작 무효 | ✅ | PlayerController/EnableJump 비활성, 이동이 MoveVelocity로만 발생 |
| 런타임/빌드 에러 | ✅ 0건 | build 콘솔 0, normal 로그에 스크립트 에러 없음 |

## Change - 260802-1 (평지 타일 + 카메라 마진)
**요청**: 맵에 기본 타일 깔기(평지), 유닛 자유 이동(상하좌우+대각) 유지.

**구현**:
- `RootDesk/MyDesk/NewTileSet.tileset` — RectTile 타일셋(사용자가 Maker UI로 생성, 잔디 스프라이트 연결은 파일 편집으로: `datas[].Id` = 스프라이트 RUID `0e7a7c37…`). **타일셋 직렬화 스키마 확보**: `{Id(스프라이트 RUID), Name, IsCollidable}`.
- `map/RtsMap.map` — `RectTileMap` 엔티티(RectTileMapComponent, GridSize 4×4유닛, TileSetRUID 연결). 맵 타일 직렬화 스키마: `tileMap: [{type, position:{x,y}, tileIndex(0-based)}]`.
- `RtsBootstrapLogic.EnsureGroundTiles()` — 유저 입장 시 타일 0이면 `BoxFill`로 64×64=4,096타일 전체 채움(멱등). **65,536타일(GridSize 1) 일괄 채우기는 에디터 ~3분 프리즈 유발 → GridSize 4로 1/16 경량화(즉시 완료)**.
- `RtsCameraAnchorComponent` — 카메라 앵커 클램프에 마진(26×15) 추가: 카메라가 맵 밖을 비추지 않는 스타식 경계 정지. `ZoomRatioMin=100`(줌아웃 제한, 마진 계산 기준 고정).
- 임시 스프라이트 바닥(Ground_0_0~3_3 16장) 제거 — SpriteRenderer 타일드 바닥은 맵 구석 근처에서 렌더링이 끊기는 엔진 컬링 문제가 있어 폐기(원인: 배경/z/레이어/이동방식 전부 배제 후 확인된 위치 의존 현상). **진짜 타일맵은 코너(5,5)에서도 정상 렌더 실측**.

**검증(Play Test, 2026-08-02)**: 중앙·코너(5,5) 평지 렌더 ✓ / 4,096타일 즉시 채움(프리즈 없음) ✓ / 이동·클램프 기존 동작 유지 ✓. 타일은 시각 전용(IsCollidable=false)이라 상하좌우+대각 자유 이동 유지.

**알려진 경고**: LEA-3035 "RectTileMapComponent 수동 추가" 경고 세션당 2회 — 기능 정상 동작 확인됨. 제거하려면 Maker UI로 타일맵 엔티티 재생성 필요(선택).

## Change - 260802-2 (개미굴 테마 바닥 교체)
**요청**: 컨셉 변경(마왕 발록 + 개미굴-신전). 잔디 → 동굴 암석 바닥, 타일 이음새/균열 무늬 제거, 일관된 표면.

**구현**:
- 공식 리소스 스캔(~80종)에서 무이음새 탑다운 동굴 바닥을 찾지 못해 **절차적 생성 커스텀 텍스처**로 전환: 256px 무이음새(래핑 노이즈) 청회색 동굴 바닥 PNG를 코드로 생성, msw-mcp 리소스 업로드 API(프리사인 URL 2단계)로 계정 리소스 등록. **RUID `e9683cc55ec14f05b9c93a19f73fb74e`** (v2: 균열 없는 소프트 셰이딩, 34KB).
- `NewTileSet.tileset` datas → LimestoneFloor 단일 타일. 타일맵 GridSize 4→**8유닛**(1024타일, 반복 패턴 완화).
- 생성 스크립트: `tools/gen-cave-floor.js` (톤/균열/스케일 파라미터로 재생성 가능 — 같은 RUID에 데이터 교체만 하면 전 맵 반영).

**검증**: 전체 맵 무이음새 렌더 ✓, 프리즈 없음 ✓. 배경(산악)은 여전히 미스매치 — #16에서 동굴 배경으로 교체 예정.

## Remaining Issues
1. ~~[경고] RectTileMapComponent 수동 추가 경고(LEA-3035)~~ — **해결됨(2026-08-01)**: 빈 타일맵 엔티티를 맵에서 제거(탑다운 이동은 MapComponent.TileMapMode=1로 동작, 실측 재확인: 스폰 128,128 · 좌이동 정상 · 경고 0건). 타일 시각화가 필요한 #2에서 Maker로 정식 생성 예정.
2. **[수동 1클릭 필요] 릴리즈용 시작 맵 지정** — Maker Hierarchy에서 RtsMap 우클릭 → "시작 맵으로 설정". Play Test는 현재 열린 맵에서 시작하므로 개발 중엔 불필요.
3. **[수동 확인 권장] 휠 줌·Confined·실마우스 엣지 스크롤** — MCP 입력 시뮬레이션 한계로 실제 마우스로 1회 확인 필요.
4. 멀티(2클라) 동기화 검증은 로드맵 #13에서 정식 수행.

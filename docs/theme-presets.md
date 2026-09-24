# 맵 테마 프리셋 — 디자인 인계 (ChatGPT용)

> 2026-09-25 기능 뼈대 완료(plan `.beaver/output/plan/rts-custom/theme-icon-preset-plan.md`). **디자인(바닥·트랙·장식·썸네일)은 이 문서를 보고 이어받는다.**
> 화면 요소 전체·디자인 규칙은 `docs/ui-screens.md`, 엔진 관례는 `docs/msw-engine.md`.

## 1. 테마는 무엇인가
- 유저마다 **자기 구역(16×13 칸 그리드 한 판 + 좌우 여백)**의 겉모습을 고른다. 다른 사람 구역은 그 사람 테마 그대로.
- 바뀌는 것 = **바닥 타일 · 트랙 판(그리드 텍스처 1장) · 여백 장식**. 트랙 경로·발판·보스 영역·사거리는 **절대 바뀌지 않는다**(밸런스 영향 없음).
- 선택·저장은 서버(`RtsProfileLogic`, 유저 DataStorage `"theme"`), 적용은 `RtsThemeLogic.ApplyToZone(zone, key)`(서버).
- 화면: 좌상단 **테마 상자**(썸네일 + 이름, 누르면 테마 창) · **테마 창**(탭 + 카드) · **유저 카드 배경**(그 유저 테마 썸네일).

## 2. 프리셋 한 줄 = 테마 하나 — `RootDesk/MyDesk/RtsThemeLogic.mlua` `GetPresets()`

| 칸 | 뜻 | 바꿔도 되나 |
|---|---|---|
| `key` | 저장 값·RPC 인자(`henesys` `ellinia` `perion` `kerning` `lith`) | **안 됨**(바꾸면 저장된 선택이 사라짐). 새 테마는 새 key |
| `name` | 화면 이름 | 됨 |
| `tab` | 테마 창 탭 이름(같은 이름끼리 한 탭, 표 순서대로). 지금 전부 `기본` | 됨 — 새 탭은 새 이름만 쓰면 창에 탭이 생김 |
| `floorTile` · `floorVariants` · `variantRatio` | 바닥 타일(`CaveFloorTileSet` 안의 Name) · 섞을 변형 타일 · 비율(0~1) | 됨 |
| `gridRUID` | 트랙 판 텍스처(16×13 칸, 1280×1040, 투명 배경) | 됨 |
| `gridTint` | 트랙 판 색 입히기(임시 모양 구분용) | 됨 — **디자인 텍스처를 넣으면 `Color(1,1,1,1)`** |
| `decor` | 여백 장식 `{ ruid, col, row, scale }` 목록(칸 좌표) | 됨 — 규칙은 4절 |
| `thumb` | 썸네일 스프라이트 RUID(`""` = 없음) | 됨 — 권장 400×240(5:3). 테마 창 카드 250×150 · 테마 상자 104×48 · 유저 카드 배경 280×56에 같이 쓰임 |
| `color` | 썸네일이 없을 때 대신 칠하는 색 | 됨 |

## 3. 지금 상태(임시 모양 — 교체 대상)

| key | 이름 | 바닥 | 트랙 판 | 장식 | 썸네일 |
|---|---|---|---|---|---|
| `henesys` | 헤네시스 | HenesysGrass1 + 2·3 (12%) | `95b3ec9d…`(헤네시스 16×13) 흰색 | 헤네시스 탑뷰 23개 | 없음(초록) |
| `ellinia` | 엘리니아 | HenesysGrassFloor | 같은 판 **청록 틴트** | 없음 | 없음(청록) |
| `perion` | 페리온 | HenesysSoil | 같은 판 **황토 틴트** | 없음 | 없음(갈색) |
| `kerning` | 커닝시티 | HenesysStone1 | 같은 판 **회보라 틴트** | 없음 | 없음(회보라) |
| `lith` | 리스항구 | ElnathSnowFloor | 같은 판 **하늘 틴트** | 없음 | 없음(파랑) |

공식 위에서 본 장식 자산은 `topview_henesys`뿐이다(2026-09-25 검색 — ellinia·perion·kerning·lith 탑뷰 없음). 다른 마을은 원작 옆모습 오브젝트(예 `maplestory/map/obj/partem/ruin_rock/perion`)를 쓰거나 새로 그려야 한다.

## 4. 새 테마 만들기 / 임시 모양 바꾸기
1. **바닥 타일** — 256px 무이음새 PNG(생성기 예: `tools/gen-henesys-floor.js`, `gen-snow-floor.js`) → msw-mcp로 **새 리소스** 업로드 → `RootDesk/MyDesk/CaveFloorTileSet.tileset`에 타일 항목 추가(Name 새로) → 프리셋 `floorTile`.
   - 타일 한 장 = 4유닛(`RtsConfigLogic.FloorTileUnit`). 구역 경계가 타일 12×8칸에 딱 맞으니 크기는 그대로.
2. **트랙 판** — `tools/gen-track-grid.js`(16×13, 칸 80px, 1280×1040)의 포석·연석·발판·선 색을 바꿔 생성 → 업로드 → `gridRUID`, `gridTint`는 흰색. **경로(SEQ)·칸 수는 건드리지 않는다**(바꾸면 `RtsZoneLogic.GetTurnPoints`·`RtsConfigLogic`까지 바뀌어야 함).
3. **장식** — 좌우 여백에만. 칸 좌표(1-기반, col 1 = 첫 열 가운데): 왼쪽 여백 `col −3.5 ~ −0.6`, 오른쪽 `col 16.6 ~ 19.4`, 행 `0 ~ 12.9`. **트랙·발판 칸(col 1~16) 금지**. 오른쪽 `row < 8`은 영입 HUD 밑이라 큰 건물 금지. 층 110(그리드 100 위, 유닛·몹 200 아래). 공식 스프라이트면 PPU 100(1칸 = 1.78유닛 = 178px).
4. **썸네일** — 400×240 PNG(그 테마 구역을 위에서 본 모습 권장) → 업로드 → `thumb`.
5. 새 테마면 `GetPresets`에 한 줄 추가(표 순서 = 창 순서). 새 탭이면 `tab`에 새 이름.
6. 확인: Maker `maker_refresh_workspace` → Play → 좌상단 테마 상자 → 테마 선택 → 예 → **내 구역만** 바뀌는지, 다른 구역(F2~F8)은 그대로인지 스크린샷.

업로드는 기존 RUID 데이터를 교체하지 말고 **새 리소스로**(Maker 캐시 때문에 교체가 반영 안 됨 — `assets/textures/README.md` 교체 절차).

## 5. 바꾸면 안 되는 것
- 프리셋 `key` 값, DataStorage 키 `theme`·`icon`·`icons`
- RPC 서명: `RtsProfileLogic.RequestSetTheme(key)` · `RequestSetIcon(id)` · `SendProfile(theme, icon, owned, userId)` · `ShowIconGot(id, userId)` · `RtsHudLogic.RefreshPlayerList(packed)`
- 서버 메서드(`@ExecSpace("Server")`·`"ServerOnly"`) 전부, `RtsThemeLogic.ApplyToZone`의 적용 순서(타일 → 트랙 판 → 장식)
- 트랙 경로·칸 수·발판·보스 영역

화면 쪽(테마 상자·테마 창·유저 카드의 배치·색·글꼴)은 `docs/ui-screens.md` 7장 규칙대로 Client 메서드 안에서 바꾼다.

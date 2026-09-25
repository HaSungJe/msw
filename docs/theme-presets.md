# 맵 테마 프리셋 — 디자인 인계 (ChatGPT용)

> 2026-09-25 기능 뼈대 완료(plan `.beaver/output/plan/rts-custom/theme-icon-preset-plan.md`). **디자인(바닥·트랙·장식·썸네일)은 이 문서를 보고 이어받는다.**
> 화면 요소 전체·디자인 규칙은 `docs/ui-screens.md`, 엔진 관례는 `docs/msw-engine.md`.

시각 방향 시안 5종과 원작 마을 랜드마크 근거는 `assets/theme-concepts/README.md`에 있다. `assets/theme-concepts/comparison.html`에서 한눈에 비교할 수 있다. 시안은 실제 트랙 텍스처가 아니므로 RUID로 바로 올리지 않는다.
사용자가 2026-09-25 기본맵 5종 방향을 승인했다. 처음 만든 트랙형 썸네일은 풍경형으로 교체했다. 현재 배경·썸네일 원본과 RUID는 `assets/design/260925-theme-scenery/`, `assets/textures/README.md`를 따른다.

## 1. 테마는 무엇인가
- 유저마다 **자기 구역(16×13 칸 그리드 한 판 + 좌우 여백)**의 겉모습을 고른다. 다른 사람 구역은 그 사람 테마 그대로.
- 바뀌는 것 = **마을 풍경 배경 · 바닥 타일 · 트랙 판(그리드 텍스처 1장) · 여백 장식 · 풍경 썸네일**. 트랙 경로·발판·보스 영역·사거리는 **절대 바뀌지 않는다**(밸런스 영향 없음).
- 선택·보유·저장은 서버(`RtsProfileLogic`, 유저 DataStorage `"theme"` 선택 · `"themes"` 보유 — 방이 바뀌어도 입장 때 다시 읽어 유지), 적용은 `RtsThemeLogic.ApplyToZone(zone, key)`(서버).
- 화면: 좌상단 **상자 배경**(프로필 + 정보 합친 400×240 상자 = 썸네일 원본 크기 그대로 — 2026-09-25, 왼쪽 위는 내 아이콘) · **프로필 창 [테마] 탭**(카드) · **유저 카드 배경**(그 유저 테마 썸네일). 같은 창 [아이콘] 탭 = 아이콘, [비석] 탭 = 비석 프리셋(6절). 좌상단 상자·유저 카드(250×150)는 둘 다 썸네일과 같은 5:3이라 늘리거나 자르지 않는다.

## 2. 프리셋 한 줄 = 테마 하나 — `RootDesk/MyDesk/RtsThemeLogic.mlua` `GetPresets()`

| 칸 | 뜻 | 바꿔도 되나 |
|---|---|---|
| `key` | 저장 값·RPC 인자(`henesys` `ellinia` `perion` `kerning` `lith`) | **안 됨**(바꾸면 저장된 선택이 사라짐). 새 테마는 새 key |
| `name` | 화면 이름 | 됨 |
| `tab` | 테마 종류 이름(같은 이름끼리 한 탭, 표 순서대로). 지금 전부 `기본` | 됨 — 종류가 2개 이상이 되면 [테마][비석] 오른쪽에 종류 탭이 생김 |
| `free` | `true` = 누구나 보유(지금 5종 전부). `false`면 유저 보유 목록(`"themes"`)에 있어야 고를 수 있다(얻는 방법은 아직 없음) | 됨 |
| `floorTile` · `floorVariants` · `variantRatio` | 바닥 타일(`CaveFloorTileSet` 안의 Name) · 섞을 변형 타일 · 비율(0~1) | 됨 |
| `gridRUID` | 트랙 판 텍스처(16×13 칸, 1280×1040, 투명 배경) | 됨 |
| `gridTint` | 트랙 판 색 입히기(임시 모양 구분용) | 됨 — **디자인 텍스처를 넣으면 `Color(1,1,1,1)`**(2026-09-25부터 5종 모두 흰색) |
| `backgroundRUID` · `backgroundAlpha` | 화면을 채우는 마을 풍경(1920×1080) · 투명도(현재 0.78). 순서 90으로 트랙 판(100) 아래 | 됨 — 전투 판독성은 Maker에서 확인 |
| `decor` | 여백 장식 `{ ruid, col, row, scale, flip }` 목록(칸 좌표). `flip = true` = 좌우 뒤집기(2026-09-25 추가, `RtsZoneLogic.SetZoneDecor`) | 됨 — 규칙은 4절 |
| `thumb` | 같은 마을 풍경을 줄인 썸네일 스프라이트 RUID(`""` = 없음) | 됨 — 권장 400×240(5:3). 프로필 창 카드 250×200(정사각 카드 270 안) · 좌상단 상자 배경 400×240(프로필 + 정보 합친 상자) · 유저 카드 배경 250×150(2026-09-25 — 둘 다 5:3)에 같이 쓰임 |
| `color` | 썸네일이 없을 때 대신 칠하는 색 | 됨 |

## 3. 지금 상태(2026-09-25 기본 마을 5종 디자인 적용 — `docs/design/260925-theme-presets.md`, Maker 검증 완료)

| key | 이름 | 바닥 | 트랙 판 | 장식 | 풍경 배경 | 풍경 썸네일 |
|---|---|---|---|---|---|---|
| `henesys` | 헤네시스 | HenesysGrass1 + 2·3 (12%) | `a752d95a…` 따뜻한 포석·꽃 | 없음(2026-09-25 사용자 "헤네시스 좌/우 오브젝트 제거" — 탑뷰 23개 뺌) | `e1886576…` | `bf5c2956…` |
| `ellinia` | 엘리니아 | `ElliniaMoss` | `7831f90d…` 이끼 돌·뿌리 | 거목 2(왼쪽 큰 것 + 오른쪽 아래 작은 것 뒤집음) | `83bbe809…` | `f307b6ca…` |
| `perion` | 페리온 | `PerionEarth` | `9ed4e22a…` 붉은 사암·자갈 | 절벽 마을 1(왼쪽) | `cf6f24aa…` | `fd0451c4…` |
| `kerning` | 커닝시티 | `KerningPavement` | `e0721799…` 벽돌·안전 표식 | 공사장 1(오른쪽 아래, 뒤집음) | `e2f7cda1…` | `457ec944…` |
| `lith` | 리스항구 | `LithSand` | `7b1ad42c…` 목재 부두·항구석 | 범선 1(왼쪽 아래) | `89b81c54…` | `7653fa3a…` |

트랙 판은 모두 `gridTint` 흰색. 전체 RUID·원본 PNG·생성기는 `assets/textures/README.md`(바닥 타일 · 구역 그리드 트랙 · 테마 썸네일·마을 장식 절).

공식 위에서 본 장식 자산은 `topview_henesys`뿐이다(2026-09-25 검색 — ellinia·perion·kerning·lith 탑뷰 없음). 다른 마을은 원작 옆모습 오브젝트(예 `maplestory/map/obj/partem/ruin_rock/perion`)를 쓰거나 새로 그려야 한다.

## 4. 새 테마 만들기 / 임시 모양 바꾸기
1. **바닥 타일** — 256px 무이음새 PNG(생성기 예: `tools/gen-henesys-floor.js`, `gen-snow-floor.js`, 이미지 초안 보정은 `tools/gen-theme-floors.py`) → msw-mcp로 **새 리소스** 업로드 → `RootDesk/MyDesk/CaveFloorTileSet.tileset`에 타일 항목 추가(Name 새로) → 프리셋 `floorTile`.
   - 타일 한 장 = 4유닛(`RtsConfigLogic.FloorTileUnit`). 구역 경계가 타일 12×8칸에 딱 맞으니 크기는 그대로.
2. **트랙 판** — `tools/gen-track-grid.js`(16×13, 칸 80px, 1280×1040 — 2026-09-25 M2 경로 77칸·매듭 3곳·보스 영역 가운데 2×2는 비움, S = 진행 방향 화살표 · E = 되돌리기 아이콘)의 포석·연석·발판·선 색을 바꿔 생성(테마 재료 프리셋 `TH` — `node tools/gen-track-grid.js <out.png> <key>`) → 업로드 → `gridRUID`, `gridTint`는 흰색. **경로(SEQ)·칸 수는 건드리지 않는다**(바꾸면 `RtsZoneLogic.GetTurnPoints`·`RtsConfigLogic`까지 바뀌어야 함).
3. **장식** — 좌우 여백에만. 칸 좌표(1-기반, col 1 = 첫 열 가운데): 왼쪽 여백 `col −3.5 ~ −0.6`, 오른쪽 `col 16.6 ~ 19.4`, 행 `0 ~ 12.9`. **트랙·발판 칸(col 1~16) 금지**. 오른쪽 `row < 8`은 영입 HUD 밑이라 큰 건물 금지. 층 110(그리드 100 위, 유닛·몹 200 아래). 공식 스프라이트면 PPU 100(1칸 = 1.78유닛 = 178px).
4. **풍경 배경과 썸네일** — 마을 풍경 한 장에서 1920×1080 배경·400×240 썸네일을 만든다. 두 파일을 각각 새 리소스로 업로드 → `backgroundRUID`·`thumb`. 전투판의 트랙·격자·유닛은 이 그림에 그리지 않는다. 배경은 `MapLayer0` 순서 90, 트랙 판은 100이다.
5. 새 테마면 `GetPresets`에 한 줄 추가(표 순서 = 창 순서). 새 탭이면 `tab`에 새 이름.
6. 확인: Maker `maker_refresh_workspace` → Play → 좌상단 프로필 상자 → [테마] → 테마 선택 → 예 → **내 구역만** 바뀌는지, 다른 구역(F2~F8)은 그대로인지 스크린샷.

업로드는 기존 RUID 데이터를 교체하지 말고 **새 리소스로**(Maker 캐시 때문에 교체가 반영 안 됨 — `assets/textures/README.md` 교체 절차).

## 5. 바꾸면 안 되는 것
- 프리셋 `key` 값(테마·비석), DataStorage 키 `theme`·`icon`·`tomb`(선택) · `icons`·`themes`·`tombs`(보유), 아이콘 없음 값 `none`
- RPC 서명: `RtsProfileLogic.RequestSetTheme(key)` · `RequestSetIcon(id)` · `RequestSetTomb(key)` · `SendProfileState(theme, icon, tomb, owned, themes, tombs, userId)` · `ShowIconGot(id, userId)` · `RtsHudLogic.RefreshPlayerList(packed)`
- 서버 메서드(`@ExecSpace("Server")`·`"ServerOnly"`) 전부, `RtsThemeLogic.ApplyToZone`의 적용 순서(타일 → 풍경 배경 → 트랙 판 → 장식)
- 트랙 경로·칸 수·발판·보스 영역

화면 쪽(테마 상자·테마 창·유저 카드의 배치·색·글꼴)은 `docs/ui-screens.md` 7장 규칙대로 Client 메서드 안에서 바꾼다.

## 6. 비석 프리셋 — `RootDesk/MyDesk/RtsTombLogic.mlua` `GetPresets()` (2026-09-25)
- 유저마다 탈락했을 때 자기 구역 가운데에 서는 비석을 고른다(`RtsRunResultLogic.SpawnTomb` — 그 구역 주인 것, 주인이 없으면 기본). 다른 사람에게도 그 모양.
- 선택·보유·저장은 서버(`RtsProfileLogic` — DataStorage `"tomb"` 선택 · `"tombs"` 보유), 창은 프로필 창 [비석] 탭.

| 칸 | 뜻 | 바꿔도 되나 |
|---|---|---|
| `key` | 저장 값·RPC 인자(`basic`) | **안 됨**. 새 비석은 새 key |
| `name` · `tab` | 화면 이름 · 종류(지금 `기본`) | 됨 |
| `ruid` · `scale` | 월드 비석 스프라이트 · 월드 스케일(현재 기본 0.6) | 됨 |
| `w` · `h` | 원본 그림 px — 프로필 창 카드(250×190 안)에 비율 맞춰 넣을 때 | 그림을 바꾸면 같이 |
| `free` | `true` = 누구나 보유. `false`면 보유 목록(`"tombs"`)에 있어야 고를 수 있다 | 됨 |

지금 1종: `basic` 기본 비석 = 단풍잎 문양의 카툰풍 비석 `31d8e058…`(1199×1312, 투명 PNG). 원본은 `assets/design/260925-cartoon-tomb/basic-cartoon-source.png`. 이전 원작 묘비 `29e864c6…`는 보관한다.
새 비석 = 그림 업로드(새 리소스) → `GetPresets`에 한 줄.

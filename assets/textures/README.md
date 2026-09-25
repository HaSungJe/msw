# 텍스처 레지스트리

## 기본 비석 (2026-09-25)

`assets/design/tombstone/basic-cartoon-source.png` — 1199×1312 투명 카툰 비석(단풍잎 문양·이끼·데이지). RUID `31d8e05805664acea73d37b04ca92f68` (`RtsTombCartoonBasic`, sprite/object). `RtsTombLogic.GetPresets().basic`에 월드 스케일 0.6으로 적용. 이전 원작 묘비 RUID `29e864c67e6c451d917b34519a4a9373`은 보관.

## 바닥 타일 (256px 무이음새)

현재 적용: 테마별(`RtsThemeLogic.GetPresets().floorTile`) — 헤네시스 `HenesysGrass1/2/3`, 엘리니아 `ElliniaMoss`, 페리온 `PerionEarth`, 커닝 `KerningPavement`, 리스 `LithSand` (CaveFloorTileSet 안 Name)

| 파일 | 톤 | 생성기 | RUID | 상태 |
|---|---|---|---|---|
| `floor-ellinia.png` | 엘리니아 이끼(진한 비취 `#168E73`) — 2026-09-25 테마 디자인(`docs/design/theme-presets.md`). 큰 잎무늬는 대비를 낮춰(0.68) 반복이 덜 보이게 | `tools/gen-theme-floors.py` (초안 `assets/design/themes/floors/*-floor-256.png` → 알파를 평균색에 합성 → 대비·목표색 이동 → 가로·세로 반바퀴 굴린 사본과 sin² 가중 합성 = 무이음새, 알파 255) | `e3089b8f17144a4ca0a3b80117627a8e` (ThemeFloorEllinia → ElliniaMoss) | **적용 중**(테마 `ellinia`) |
| `floor-perion.png` | 페리온 적갈색 흙 `#E99245` | 같은 생성기 | `272e8d94a1f8432c876b676c315bfe9d` (ThemeFloorPerion → PerionEarth) | **적용 중**(테마 `perion`) |
| `floor-kerning.png` | 커닝 회보라 도시 바닥 `#596588` | 같은 생성기 | `8dce7ba39e1447f0bd5e87cdb52bc936` (ThemeFloorKerning → KerningPavement) | **적용 중**(테마 `kerning`) |
| `floor-lith.png` | 리스 옅은 모래·석회암 `#F1DFB8` | 같은 생성기 | `fa1020b1c467413bac7538a1f040a165` (ThemeFloorLith → LithSand) | **적용 중**(테마 `lith`) |
| `henesys-grass.png` | 헤네시스 잔디(연두) — 사용자 지시 2026-09-14 "트랙/타일 배경을 헤네시스로" | `tools/gen-henesys-floor.js` | `d908c425553c42c5b11016ab40b306f4` (HenesysGrassFloor) | **적용 중** |
| `elnath-snow.png` | 엘나스 눈(흰색) — 2026-08-18 확정, 09-14 헤네시스로 교체 | `tools/gen-snow-floor.js` | `df8df44de6e64c25a74f465ef88ef4c8` (ElnathSnowFloor) | 프리셋 `elnath` |
| `cave-brown.png` | 갈색(개미굴 흙) — 2026-08-02 확정, 컨셉 변경으로 교체 | `tools/gen-cave-floor.js` | `9bddf00f17224983b4037a1fe48986e0` (CaveFloorBrown) | 보관 |
| `cave-navy.png` | 감색(짙은 네이비) | `tools/gen-cave-floor.js` | `eac1d52283474a3d9d6f72a82f913376` (CaveFloorNavy) | 보관 |
| `cave-gray.png` | 청회색(석회암, 초기 v2) | `tools/gen-cave-floor.js` | `e9683cc55ec14f05b9c93a19f73fb74e` (LimestoneFloorTile — 주의: 데이터가 네이비로 덮인 상태) | 보관 |

> 타일셋 파일명·EntryKey는 `CaveFloorTileSet`인 채로 두었습니다(맵이 `tileset://` GUID로 참조 중이라 이름을 바꾸면 참조가 깨집니다). 이름 정리가 필요하면 별도로 요청해 주세요.

## 구역 그리드 트랙 (화면 v2 — **16×13칸**, 칸 80px, 1280×1040, 투명 배경. 2026-09-20: 18×12에서 우측 2열 삭제·아래 1행 추가 — 좌우 대칭)

현재 적용: `assets/design/themes/tracks/track-v3-*.png` 5종. M2 경로·발판은 공통이며 마을마다 길의 재질과 가장자리 장식이 다르다. 출발·되돌리기는 원형 배지를 제거하고 길 표면에 화살표만 새겼다. 생성기는 `tools/gen-track-grid.js`; 경로 좌표는 이전과 같다. 구버전 트랙 PNG와 스타디움 생성기는 정리했으며 현재 트랙 5종만 유지한다.

| 테마 | 길 디자인 | RUID |
|---|---|---|
| 헤네시스 | 따뜻한 포석, 풀과 작은 꽃 | `a752d95ae8f84f9291047ae34b00416f` |
| 엘리니아 | 이끼빛 둥근돌, 뿌리·잎·은은한 빛 | `7831f90d580d4c1e92629f326c82eaa9` |
| 페리온 | 붉은 사암 블록, 균열·자갈 | `9ed4e22a587c4e068b7b832b890aa019` |
| 커닝시티 | 청회색 벽돌, 노란 공사장 안전 표식 | `e0721799e39d4ecebf723b842c013b74` |
| 리스항구 | 목재 부두와 항구석, 로프·물결 | `7b1ad42ce59245eea17e52ab201b4dde` |

구역마다 스프라이트 1장(PPU 100 → 스케일 2.2222 = 28.44×23.11유닛, RtsConfigLogic.GridTextureScale). 경로를 바꾸면 생성기의 `SEQ`와 `RtsZoneLogic.GetTurnPoints`를 같이 고친다. 칸 수를 바꾸면 생성기 COLS/ROWS + RtsConfigLogic GridCols/GridRows/GridLeft/GridTop + 장식물 자리(RtsThemeLogic)도 같이.

## 테마 풍경 배경·썸네일 (2026-09-25)

`assets/design/themes/scenery/`의 마을 풍경 원본에서 1920×1080 배경과 400×240 썸네일을 만들었다. 배경은 구역 중심에 PPU 100·스케일 `GridTextureScale`로 배치하며, `MapLayer0` 순서 90·알파 0.78이다. 트랙 판은 순서 100으로 그 위에 놓인다. 두 자산은 같은 그림이므로 테마 선택 카드에서 본 풍경이 실제 전장에도 나온다.

| 테마 | 배경 파일 · RUID | 썸네일 파일 · RUID |
|---|---|---|
| 헤네시스 | `henesys-background-1920x1080.png` · `e1886576584e4e3f99c9912abf75c489` | `henesys-thumb-400x240.png` · `bf5c2956120046aab843eb14f562b925` |
| 엘리니아 | `ellinia-background-1920x1080.png` · `83bbe809e077494094ebdaa6dfd1a720` | `ellinia-thumb-400x240.png` · `f307b6caed814747aec03e3483777254` |
| 페리온 | `perion-background-1920x1080.png` · `cf6f24aaecac4f5e88464b8e02a21c2a` | `perion-thumb-400x240.png` · `fd0451c462a14c91ab45582a08484353` |
| 커닝시티 | `kerning-background-1920x1080.png` · `e2f7cda163294b3b8d8ab956f2966bda` | `kerning-thumb-400x240.png` · `457ec944d357431ba1642520d7d4eb16` |
| 리스항구 | `lith-background-1920x1080.png` · `89b81c540feb454796ba78a0025b7223` | `lith-thumb-400x240.png` · `7653fa3a53314b43a2aa4b16ccae3adc` |

## 이전 테마 썸네일·마을 장식 (2026-09-25 — `docs/design/theme-presets.md`, ChatGPT 시안)

장식 원본은 `assets/design/themes/decor/`. 아래 옛 썸네일 5장의 디자인 원본은 `.beaver/output/archive/design-cleanup-260925/old-theme-thumbnails/`로 분리했다. 이 표의 `assets/textures/thumb-*.png`와 기존 업로드 RUID는 유지하며, 프리셋은 위의 새 풍경 썸네일을 사용한다. 장식은 투명 컷아웃을 **반으로 줄여**(최대 변 ≤ 768) 올렸다 → 프리셋 `scale`은 가이드라인 값 × 2. 전부 sprite/etc, PPU 100.

| 파일 | 내용 | RUID | 쓰는 곳 |
|---|---|---|---|
| `thumb-henesys.png` | 헤네시스 옛 트랙형 썸네일 400×240 | `613ffc1b909d4cb39533976ff37f73f7` (ThemeThumbHenesys) | 보관 |
| `thumb-ellinia.png` | 엘리니아 옛 트랙형 썸네일 | `757c012621d0461b97828c4677c3ccbb` (ThemeThumbEllinia) | 보관 |
| `thumb-perion.png` | 페리온 옛 트랙형 썸네일 | `11af968b62404f0684ec946967428449` (ThemeThumbPerion) | 보관 |
| `thumb-kerning.png` | 커닝시티 옛 트랙형 썸네일 | `8c5a69978ca74c0eada03ab25e52c848` (ThemeThumbKerning) | 보관 |
| `thumb-lith.png` | 리스항구 옛 트랙형 썸네일 | `427f046934aa4e489c5bbb39f0670b46` (ThemeThumbLith) | 보관 |
| `decor-ellinia-giant-tree.png` | 엘리니아 거목 512×768 | `487afe0def6249baad65871d93a81cb7` (ThemeDecorElliniaTree) | `RtsThemeLogic.GetElliniaDecor` — 왼쪽 col −1.8·row 5.6·scale 0.86, 오른쪽 아래 col 18.2·row 10.5·scale 0.6·flip |
| `decor-perion-cliff-village.png` | 페리온 절벽 마을 568×691 | `d5ea7c706994465d93b72b44bc5b4241` (ThemeDecorPerionCliff) | `GetPerionDecor` — col −1.8·row 8.5·scale 0.8 |
| `decor-kerning-construction.png` | 커닝 공사장 512×768 (추락주의 표식이 오른쪽 면) | `0dff7e125801459099ca68b008841616` (ThemeDecorKerningConstruction) | `GetKerningDecor` — col 18.1·row 10.0·scale 0.76·flip(표식을 전투판 쪽으로) |
| `decor-lith-harbor-ship.png` | 리스 범선 601×653 | `4801d34b001d49dabda05a25d265ac42` (ThemeDecorLithShip) | `GetLithDecor` — col −1.7·row 9.8·scale 0.7 |

## 몬스터·보스 썸네일 (2026-09-25 — ChatGPT 제작 `assets/design/monster-thumbnails/`)

247종(몬스터 M001~M229 · 보스 B01~B18) 256×256 투명 PNG(그림 최대 216, 가운데)를 **각각 새 스프라이트**(sprite/etc, 이름 `RtsThumb<ID>`)로 올렸다. ID → RUID 표 = `assets/textures/monster-thumbs.tsv`(ID · RUID · 이름) → `python tools/gen-monster-thumbs.py` → `RtsMonsterThumbLogic.mlua` GENERATED 구간. `RtsHudLogic.SpawnMonsterPortrait`가 이 표를 먼저 본다 — 아이콘 탭·프로필 상자·유저 카드·아이콘 정보·획득 팝업·몬스터 정보 창 초상 전부. 그림을 바꾸면 새 리소스로 올려 tsv만 고치고 생성기를 다시 돌린다.

## HUD 프레임 (폐기 — 화면 v2에서 미니맵/초상화/정보창 제거)
`tools/gen-hud-frame.js` — 구 스타식 HUD 프레임. RUID `3c4c2394686a46cf86a34f520d31c3f0`(340) · `3c81e689753f4c0eb2a58418963fdf2f`(240) · `28511390f76c42c08a9105751ced4051`(info). 보관.

## 발판 강조 틀 (2026-09-15 — 위치 이동 모드)

| 파일 | 내용 | 생성 | RUID | 상태 |
|---|---|---|---|---|
| `pad-frame.png` | 80px, 흰 테두리 6px + 안쪽 흰 알파 70. 색은 `SpriteRenderer.Color` 틴트(빈 발판 금색 / 내 유닛 자리 파랑). PPU 100 → 스케일 2.222 = 한 칸, 코드는 2.12 | PIL 한 줄(`RtsUnitSelectLogic` 주석) | `2c03a06fb9ee495e80e3935eb033bccf` (RtsPadFrame, sprite/object) | **적용 중** |

## 월드 상점 상품 썸네일 (2026-09-15)

| 파일 | 내용 | RUID / 상품 | 상태 |
|---|---|---|---|
| `world-avatar.png` (2026-09-24) | 120px, 금색 틀 + 아바타 실루엣 + "월드 아바타 / 영구" — 영구 이용권용(`world-avatar-30d.png`에서 아래 줄만 교체) | 상품 `QK03ZI15E` 썸네일(2026-09-24 업로드, 파일 `1790232456396.png`) — 상점 상세의 썸네일 RUID 칸은 아직 옛 `46652e80…` | **적용 중** |
| `world-avatar-30d.png` | 120px, 금색 틀 + 아바타 실루엣 + "월드 아바타 30일" | 썸네일 RUID `46652e80572242ec96ae94c3088b4a15`, 상품 `QK03ZI15E`(아이템, 1,600 월드코인, **비공개**) | 교체됨(2026-09-24 → `world-avatar.png`) |

## 옛 스피어 크러셔 이펙트 (2026-09-16 — 다크 임페일 후보, 영상 추출)

| 파일 | 내용 | 생성 | RUID | 상태 |
|---|---|---|---|---|
| `crusher/crusher_01..11.png` | 292×250 알파 PNG 11프레임(≈11fps, 90ms 간격, 1.0초). 옛 용기사 3차 스피어 크러셔(1311001 — 라이브러리엔 소리만 남음) 이펙트를 나무위키 mp4(302×296, 흰 배경 + 용기사 캐릭터)에서 추출. 흰 배경 → 알파(a = 1 − min(RGB)/255), 캐릭터 실루엣(idle + 찌르기 포즈)은 **구멍(알파 0)** — 게임에선 그 자리에 우리 아바타가 선다. 흰 하이라이트는 원리상 복원 불가라 외곽선 속을 연한 시안 반투명으로 메움 → 용머리 발사 구간(8~11)은 원본보다 빈약. `meta.json`: crop·발 위치(157,208)·fps | `crusher/extract_crusher.py`(ffmpeg 프레임 추출 + cv2/numpy) | 업로드 완료(2026-09-16, sprite/skill `RtsCrusherFx01..11`): cfbb29c1bc164b1f9fcd7172a48edd84, 01785f5c43984033a3b01349f2577a5e, 512cf540171a479499f1e29954c26b6e, 85ce003c137347f2b2951a157b6e542c, 364932f1809b4c8298974d0aeaf7b151, 6bb848a925174ef58436b4f474e1ed14, b93ed9948ce4456e87ffb0f1f7809a3f, 5a7d68c91f5e40dfa0e5cd82cefc1cfc, c9cb83a286f241aab46823416c819a9b, 9ebbdf97148d48db9ca76af0dd9b4372, 3718a78d28b341f2822c207baa5c65c9 — 목록은 `crusher/meta.json` `ruids` | **후보 — 게임 데모 확인**. v1(외곽선만)은 사용자 피드백 "너무 비어있고 테두리만" → **v2 속 채움**(`crusher/v2/`, `RtsCrusherFx2_01..11`, 외곽선을 크게 닫은 영역 안 저알파를 흰빛 시안 α0.55로 채움 + 감마 0.7) 재업로드 → **v3 진하게**(`crusher/v3/`, `RtsCrusherFx3_01..11`: 속 흰빛 α0.85 + 선 ×1.8 + 감마 0.6, 용머리 프레임은 median 5 + 닫힘 25로 덩어리화) → v3는 "너무 어색"으로 **v2로 복귀** — 현재 `meta.json` `ruids`가 v2(v3 RUID는 `ruids_v3_dense`에 보관). 데모: stabT1 + 플립북 90ms + 옛 시전음 `fcac442d…`, 스케일 1.7, 발 오프셋 (−0.11, +0.83)×스케일, Default/300. 다크나이트 창은 캐시 무기(afterImage swordTS = 빨간 참격)라 진짜 스피어로 바꿔야 함(`assets.md` 메모) |

## 테마 프리셋 (2026-09-14 → 2026-09-25 유저별 5종)
바닥 타일 + 그리드 트랙 텍스처(+틴트) + 장식 + 썸네일은 `RootDesk/MyDesk/RtsThemeLogic.mlua`의 프리셋 표로 묶는다 — 헤네시스·엘리니아·페리온·커닝시티·리스항구(헤네시스 외 4종은 임시 모양). **유저마다 자기 구역에만** 적용(`_RtsThemeLogic:ApplyToZone(zone, key)`, 서버). 옛 `elnath` 프리셋은 표에서 뺐다(자산은 위 표에 '보관').
**새 테마 추가·디자인 교체 절차는 `docs/theme-presets.md`** (ChatGPT 인계용).

## 원형 마스크 (2026-09-25 — 유저 카드 동그란 아이콘)

| 파일 | 내용 | 생성 | RUID | 상태 |
|---|---|---|---|---|
| `circle-mask.png` | 128px 흰 원(가장자리 안티앨리어싱), 투명 배경. `MaskComponent` 칸의 이미지로 쓰면 자식(몬스터 초상)이 원 모양으로 잘린다 | PIL(4배 크기로 그린 뒤 축소) | `69e2dced65e443d3bb391464fd64b123` (RtsCircleMask, sprite/etc, 2026-09-25) → `RtsHudLogic.CircleMaskRUID` | **적용 중** |
| `radar-web.png` | 512×512 투명 — 정오각형 5겹(단계 1~5, 반지름 = 단계 ÷ 5 × 240px) + 축 5개, 흰색(게임에서 α0.9). 영입 상세 오각형 바탕 | `tools/gen-radar-assets.py` | `de902441f2e74e89a7fefa81ef29da0e` (RtsRadarWeb, sprite/etc, 2026-09-25) | 적용(RtsPopupLogic.RadarWebRUID) |
| `right-tri.png` | 128×128 흰 직각삼각형(직각 왼쪽 아래, 다리 = 아래·왼쪽 변). 오각형 값 다각형을 직각삼각형 10장으로 채울 때(회전 + 가로세로 크기) | `tools/gen-radar-assets.py` | `c62bf5fb88994fe48ca88e725fa458aa` (RtsRightTri, sprite/etc, 2026-09-25) | 적용(RtsPopupLogic.RightTriRUID) |

헤네시스 배경 마을(그리드 아래 반투명 58개)은 공식 MSW 탑뷰 오브젝트 `maplestory/map/obj/msw/topview_henesys/{building,tree,acc,flag}/N/0`(msw-mcp `asset_search_resources` 쿼리 `*topview_henesys`). 월드 프롭 엔티티는 네이티브 모델 `model://MapObject`(Transform + SpriteRenderer).

## 교체 절차 (공통)
1. 생성기의 색/파라미터 수정 → PNG 생성
2. **새 리소스로 업로드** (msw-mcp `asset_create_account_resource_storage_item` 2단계 — 기존 RUID 데이터 교체는 Maker 캐시 때문에 반영 안 됨)
3. 참조처 교체
   - 바닥: `RootDesk/MyDesk/CaveFloorTileSet.tileset`의 해당 타일 `Id`(이름은 그대로 두면 프리셋 표를 안 고쳐도 됨)
   - 트랙: `RootDesk/MyDesk/RtsThemeLogic.GetPresets`의 `gridRUID`
4. Maker `refresh_workspace` → Play Test 확인 → `maker_save`

## 도트 퍼니셔 불구슬 (2026-09-18 — 사용자 지정 아이콘 컷)

| 파일 | 내용 | 생성 | RUID | 상태 |
|---|---|---|---|---|
| `dotorb/dotorb_01..04.png` | 64px 알파 PNG. 도트 퍼니셔(400021001) 스킬 아이콘 `d998c591…`(icon)·`20a64945…`(iconmouseover)의 CDN 64px 썸네일을 중심 반지름 26.5px 원으로 잘라 둥근 사각 테두리를 제거(가장자리 0.8px 블러). 01 = icon, 03 = mouseover(밝음), 02 = 04 = 둘의 50% 블렌드(맥동 중간) | PIL(scratchpad 한 번, 스크립트는 `RtsJobTableLogic` 도트 퍼니셔 주석 참조) | `3769c672d4f94a2e9f37b2477ab66d5b`(RtsDotOrb01) · `b0b300d3c83749198c5c146ab1ac5e84`(RtsDotOrb02) · `da5ad791c75e4ef4941d722d39e1f334`(RtsDotOrb03) — 04는 02와 같아 미업로드 | **적용 중** — `projFlySprites` 01→02→03→02, 0.12초, 스케일 1.25(≈0.8유닛) |

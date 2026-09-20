# 텍스처 레지스트리

## 바닥 타일 (256px 무이음새)

현재 적용: **henesys-grass** (CaveFloorTileSet → HenesysGrassFloor)

| 파일 | 톤 | 생성기 | RUID | 상태 |
|---|---|---|---|---|
| `henesys-grass.png` | 헤네시스 잔디(연두) — 사용자 지시 2026-09-14 "트랙/타일 배경을 헤네시스로" | `tools/gen-henesys-floor.js` | `d908c425553c42c5b11016ab40b306f4` (HenesysGrassFloor) | **적용 중** |
| `elnath-snow.png` | 엘나스 눈(흰색) — 2026-08-18 확정, 09-14 헤네시스로 교체 | `tools/gen-snow-floor.js` | `df8df44de6e64c25a74f465ef88ef4c8` (ElnathSnowFloor) | 프리셋 `elnath` |
| `cave-brown.png` | 갈색(개미굴 흙) — 2026-08-02 확정, 컨셉 변경으로 교체 | `tools/gen-cave-floor.js` | `9bddf00f17224983b4037a1fe48986e0` (CaveFloorBrown) | 보관 |
| `cave-navy.png` | 감색(짙은 네이비) | `tools/gen-cave-floor.js` | `eac1d52283474a3d9d6f72a82f913376` (CaveFloorNavy) | 보관 |
| `cave-gray.png` | 청회색(석회암, 초기 v2) | `tools/gen-cave-floor.js` | `e9683cc55ec14f05b9c93a19f73fb74e` (LimestoneFloorTile — 주의: 데이터가 네이비로 덮인 상태) | 보관 |

> 타일셋 파일명·EntryKey는 `CaveFloorTileSet`인 채로 두었습니다(맵이 `tileset://` GUID로 참조 중이라 이름을 바꾸면 참조가 깨집니다). 이름 정리가 필요하면 별도로 요청해 주세요.

## 구역 그리드 트랙 (화면 v2 — **16×13칸**, 칸 80px, 1280×1040, 투명 배경. 2026-09-20: 18×12에서 우측 2열 삭제·아래 1행 추가 — 좌우 대칭)

현재 적용: **track-grid**(16×13). 이전 18×12는 `track-grid-18x12.png`로 보관

| 파일 | 내용 | 생성기 | RUID | 상태 |
|---|---|---|---|---|
| `track-grid.png` | 아티팩트 v17 경로 그대로(16×13). 트랙 칸 = 헤네시스 포석 + 연석 + 흰 점선 진행선, 발판 = 흰 반투명 칸(잔디 위), 빈 칸 = 짙은 초록 선, S/E 원 + 글자, E→S 복귀 화살표 | `tools/gen-track-grid.js` | `95b3ec9d377e46ecb9d394467d27dada` (ZoneTrackGridHenesys16) | **적용 중** |
| `track-grid-18x12.png` | 이전 18×12 판 | 같은 생성기(COLS 18·ROWS 12) | `f8bf4274602c4d22b2e6643e114fbc5f` (ZoneTrackGridHenesys) | 보관 |
| (눈 배경판) | 같은 경로, 회청 선·회청 발판(엘나스 눈 위 용) — **아직 18×12**, 다시 쓰려면 16×13 재생성 | `tools/gen-track-grid.js` (색만 다름) | `651583e1c1ee44cdb6d2a891755ab528` (ZoneTrackGrid) | 프리셋 `elnath` |

구역마다 스프라이트 1장(PPU 100 → 스케일 2.2222 = 28.44×23.11유닛, RtsConfigLogic.GridTextureScale). 경로를 바꾸면 생성기의 `SEQ`와 `RtsZoneLogic.GetTurnPoints`를 같이 고친다. 칸 수를 바꾸면 생성기 COLS/ROWS + RtsConfigLogic GridCols/GridRows/GridLeft/GridTop + 장식물 자리(RtsThemeLogic)도 같이.

## 구역 트랙 — 스타디움 (폐기, 2026-09-14 화면 v2로 교체)

| 파일 | 재질 | 생성기 | RUID | 상태 |
|---|---|---|---|---|
| `track-henesys-stone.png` | 헤네시스 돌길 포석(2줄 엇갈림 + 연석) | `tools/gen-track-stone.js` | `faf04ce588484d07847a8b34f13f4b9e` (ZoneTrackHenesysStone) | 보관 |
| (초판) | 베이지 흙 노면 | `tools/gen-track-texture.js` | `b4672b0c52eb4bd4b5a0a22c075b2aea` (ZoneTrackStadium) | 보관 |

`gen-track-stone.js`는 중심선 라운드 사각형을 촘촘히 샘플링해 픽셀마다 (호길이 s, 수직거리 d)를 구한 뒤 (s, d) 공간에 포석을 그립니다 → 돌이 트랙 진행 방향을 따라 눕습니다. 둘레는 정수 개의 돌로 나눠 이음매가 맞물립니다.

## HUD 프레임 (폐기 — 화면 v2에서 미니맵/초상화/정보창 제거)
`tools/gen-hud-frame.js` — 구 스타식 HUD 프레임. RUID `3c4c2394686a46cf86a34f520d31c3f0`(340) · `3c81e689753f4c0eb2a58418963fdf2f`(240) · `28511390f76c42c08a9105751ced4051`(info). 보관.

## 발판 강조 틀 (2026-09-15 — 위치 이동 모드)

| 파일 | 내용 | 생성 | RUID | 상태 |
|---|---|---|---|---|
| `pad-frame.png` | 80px, 흰 테두리 6px + 안쪽 흰 알파 70. 색은 `SpriteRenderer.Color` 틴트(빈 발판 금색 / 내 유닛 자리 파랑). PPU 100 → 스케일 2.222 = 한 칸, 코드는 2.12 | PIL 한 줄(`RtsUnitSelectLogic` 주석) | `2c03a06fb9ee495e80e3935eb033bccf` (RtsPadFrame, sprite/object) | **적용 중** |

## 월드 상점 상품 썸네일 (2026-09-15)

| 파일 | 내용 | RUID / 상품 | 상태 |
|---|---|---|---|
| `world-avatar-30d.png` | 120px, 금색 틀 + 아바타 실루엣 + "월드 아바타 30일" | 썸네일 RUID `46652e80572242ec96ae94c3088b4a15`, 상품 `QK03ZI15E`(아이템, 1,600 월드코인, **비공개**) | 적용 중 |

## 옛 스피어 크러셔 이펙트 (2026-09-16 — 다크 임페일 후보, 영상 추출)

| 파일 | 내용 | 생성 | RUID | 상태 |
|---|---|---|---|---|
| `crusher/crusher_01..11.png` | 292×250 알파 PNG 11프레임(≈11fps, 90ms 간격, 1.0초). 옛 용기사 3차 스피어 크러셔(1311001 — 라이브러리엔 소리만 남음) 이펙트를 나무위키 mp4(302×296, 흰 배경 + 용기사 캐릭터)에서 추출. 흰 배경 → 알파(a = 1 − min(RGB)/255), 캐릭터 실루엣(idle + 찌르기 포즈)은 **구멍(알파 0)** — 게임에선 그 자리에 우리 아바타가 선다. 흰 하이라이트는 원리상 복원 불가라 외곽선 속을 연한 시안 반투명으로 메움 → 용머리 발사 구간(8~11)은 원본보다 빈약. `meta.json`: crop·발 위치(157,208)·fps | `crusher/extract_crusher.py`(ffmpeg 프레임 추출 + cv2/numpy) | 업로드 완료(2026-09-16, sprite/skill `RtsCrusherFx01..11`): cfbb29c1bc164b1f9fcd7172a48edd84, 01785f5c43984033a3b01349f2577a5e, 512cf540171a479499f1e29954c26b6e, 85ce003c137347f2b2951a157b6e542c, 364932f1809b4c8298974d0aeaf7b151, 6bb848a925174ef58436b4f474e1ed14, b93ed9948ce4456e87ffb0f1f7809a3f, 5a7d68c91f5e40dfa0e5cd82cefc1cfc, c9cb83a286f241aab46823416c819a9b, 9ebbdf97148d48db9ca76af0dd9b4372, 3718a78d28b341f2822c207baa5c65c9 — 목록은 `crusher/meta.json` `ruids` | **후보 — 게임 데모 확인**. v1(외곽선만)은 사용자 피드백 "너무 비어있고 테두리만" → **v2 속 채움**(`crusher/v2/`, `RtsCrusherFx2_01..11`, 외곽선을 크게 닫은 영역 안 저알파를 흰빛 시안 α0.55로 채움 + 감마 0.7) 재업로드 → **v3 진하게**(`crusher/v3/`, `RtsCrusherFx3_01..11`: 속 흰빛 α0.85 + 선 ×1.8 + 감마 0.6, 용머리 프레임은 median 5 + 닫힘 25로 덩어리화) → v3는 "너무 어색"으로 **v2로 복귀** — 현재 `meta.json` `ruids`가 v2(v3 RUID는 `ruids_v3_dense`에 보관). 데모: stabT1 + 플립북 90ms + 옛 시전음 `fcac442d…`, 스케일 1.7, 발 오프셋 (−0.11, +0.83)×스케일, Default/300. 다크나이트 창은 캐시 무기(afterImage swordTS = 빨간 참격)라 진짜 스피어로 바꿔야 함(`assets.md` 메모) |

## 테마 프리셋 (2026-09-14)
바닥 타일 + 그리드 트랙 텍스처는 `RootDesk/MyDesk/RtsThemeLogic.mlua`의 프리셋 표로 묶어서 고른다(기본 `henesys`, 보관 `elnath`). `CaveFloorTileSet`에는 두 타일이 모두 들어 있다(HenesysGrassFloor·ElnathSnowFloor).
**새 테마 추가** = ① 바닥 256px 타일 생성·업로드 → 타일셋 `datas`에 항목 추가 ② `gen-track-grid.js`의 선/발판 색을 그 배경에 맞춰 생성·업로드 ③ `RtsThemeLogic.GetPresets`에 한 줄 + 장식물 목록(`decor`: 공식 스프라이트 RUID + 칸 좌표) ④ 아티팩트 `.stage[data-theme=…]` 변수 한 벌 + `DECOR` 목록. 런타임 전환은 서버에서 `_RtsThemeLogic:ApplyPreset(key)`.

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


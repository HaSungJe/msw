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

## 구역 그리드 트랙 (화면 v2 — 18×12칸, 칸 80px, 1440×960, 투명 배경)

현재 적용: **track-grid**

| 파일 | 내용 | 생성기 | RUID | 상태 |
|---|---|---|---|---|
| `track-grid.png` | 아티팩트 v17 경로 그대로. 트랙 칸 = 헤네시스 포석 + 연석 + 흰 점선 진행선, 발판 = 흰 반투명 칸(잔디 위), 빈 칸 = 짙은 초록 선, S/E 원 + 글자, E→S 복귀 화살표 | `tools/gen-track-grid.js` | `f8bf4274602c4d22b2e6643e114fbc5f` (ZoneTrackGridHenesys) | **적용 중** |
| (눈 배경판) | 같은 경로, 회청 선·회청 발판(엘나스 눈 위 용) | `tools/gen-track-grid.js` (색만 다름) | `651583e1c1ee44cdb6d2a891755ab528` (ZoneTrackGrid) | 프리셋 `elnath` |

구역마다 스프라이트 1장(업로드 PPU 30 실측 → 스케일 0.667 = 32×21.33유닛). 경로를 바꾸면 생성기의 `SEQ`와 `RtsZoneLogic.GetTurnPoints`를 같이 고친다.

## 구역 트랙 — 스타디움 (폐기, 2026-09-14 화면 v2로 교체)

| 파일 | 재질 | 생성기 | RUID | 상태 |
|---|---|---|---|---|
| `track-henesys-stone.png` | 헤네시스 돌길 포석(2줄 엇갈림 + 연석) | `tools/gen-track-stone.js` | `faf04ce588484d07847a8b34f13f4b9e` (ZoneTrackHenesysStone) | 보관 |
| (초판) | 베이지 흙 노면 | `tools/gen-track-texture.js` | `b4672b0c52eb4bd4b5a0a22c075b2aea` (ZoneTrackStadium) | 보관 |

`gen-track-stone.js`는 중심선 라운드 사각형을 촘촘히 샘플링해 픽셀마다 (호길이 s, 수직거리 d)를 구한 뒤 (s, d) 공간에 포석을 그립니다 → 돌이 트랙 진행 방향을 따라 눕습니다. 둘레는 정수 개의 돌로 나눠 이음매가 맞물립니다.

## HUD 프레임 (폐기 — 화면 v2에서 미니맵/초상화/정보창 제거)
`tools/gen-hud-frame.js` — 구 스타식 HUD 프레임. RUID `3c4c2394686a46cf86a34f520d31c3f0`(340) · `3c81e689753f4c0eb2a58418963fdf2f`(240) · `28511390f76c42c08a9105751ced4051`(info). 보관.

## 테마 프리셋 (2026-09-14)
바닥 타일 + 그리드 트랙 텍스처는 `RootDesk/MyDesk/RtsThemeLogic.mlua`의 프리셋 표로 묶어서 고른다(기본 `henesys`, 보관 `elnath`). `CaveFloorTileSet`에는 두 타일이 모두 들어 있다(HenesysGrassFloor·ElnathSnowFloor).
**새 테마 추가** = ① 바닥 256px 타일 생성·업로드 → 타일셋 `datas`에 항목 추가 ② `gen-track-grid.js`의 선/발판 색을 그 배경에 맞춰 생성·업로드 ③ `RtsThemeLogic.GetPresets`에 한 줄 ④ 아티팩트 `.stage[data-theme=…]` 변수 한 벌. 런타임 전환은 서버에서 `_RtsThemeLogic:ApplyPreset(key)`.

## 교체 절차 (공통)
1. 생성기의 색/파라미터 수정 → PNG 생성
2. **새 리소스로 업로드** (msw-mcp `asset_create_account_resource_storage_item` 2단계 — 기존 RUID 데이터 교체는 Maker 캐시 때문에 반영 안 됨)
3. 참조처 교체
   - 바닥: `RootDesk/MyDesk/CaveFloorTileSet.tileset`의 해당 타일 `Id`(이름은 그대로 두면 프리셋 표를 안 고쳐도 됨)
   - 트랙: `RootDesk/MyDesk/RtsThemeLogic.GetPresets`의 `gridRUID`
4. Maker `refresh_workspace` → Play Test 확인 → `maker_save`

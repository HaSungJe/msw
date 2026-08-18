# 텍스처 레지스트리

## 바닥 타일 (256px 무이음새)

현재 적용: **elnath-snow** (CaveFloorTileSet → ElnathSnowFloor)

| 파일 | 톤 | 생성기 | RUID | 상태 |
|---|---|---|---|---|
| `elnath-snow.png` | 엘나스 눈(흰색) — 사용자 확정 2026-08-18 | `tools/gen-snow-floor.js` | `df8df44de6e64c25a74f465ef88ef4c8` (ElnathSnowFloor) | **적용 중** |
| `cave-brown.png` | 갈색(개미굴 흙) — 2026-08-02 확정, 컨셉 변경으로 교체 | `tools/gen-cave-floor.js` | `9bddf00f17224983b4037a1fe48986e0` (CaveFloorBrown) | 보관 |
| `cave-navy.png` | 감색(짙은 네이비) | `tools/gen-cave-floor.js` | `eac1d52283474a3d9d6f72a82f913376` (CaveFloorNavy) | 보관 |
| `cave-gray.png` | 청회색(석회암, 초기 v2) | `tools/gen-cave-floor.js` | `e9683cc55ec14f05b9c93a19f73fb74e` (LimestoneFloorTile — 주의: 데이터가 네이비로 덮인 상태) | 보관 |

> 타일셋 파일명·EntryKey는 `CaveFloorTileSet`인 채로 두었습니다(맵이 `tileset://` GUID로 참조 중이라 이름을 바꾸면 참조가 깨집니다). 이름 정리가 필요하면 별도로 요청해 주세요.

## 구역 트랙 (스타디움 외곽선, 740×270 / 코너 50px / 밴드 32px)

현재 적용: **track-henesys-stone**

| 파일 | 재질 | 생성기 | RUID | 상태 |
|---|---|---|---|---|
| `track-henesys-stone.png` | 헤네시스 돌길 포석(2줄 엇갈림 + 연석) — 사용자 확정 2026-08-18 | `tools/gen-track-stone.js` | `faf04ce588484d07847a8b34f13f4b9e` (ZoneTrackHenesysStone) | **적용 중** |
| (초판) | 베이지 흙 노면 | `tools/gen-track-texture.js` | `b4672b0c52eb4bd4b5a0a22c075b2aea` (ZoneTrackStadium) | 보관 |

`gen-track-stone.js`는 중심선 라운드 사각형을 촘촘히 샘플링해 픽셀마다 (호길이 s, 수직거리 d)를 구한 뒤 (s, d) 공간에 포석을 그립니다 → 돌이 트랙 진행 방향을 따라 눕습니다. 둘레는 정수 개의 돌로 나눠 이음매가 맞물립니다.

## HUD 프레임
`tools/gen-hud-frame.js` — 미니맵/초상화/정보창 장식 프레임. RUID는 `RtsHudLogic.mlua` 상단 프로퍼티 참조.

## 교체 절차 (공통)
1. 생성기의 색/파라미터 수정 → PNG 생성
2. **새 리소스로 업로드** (msw-mcp `asset_create_account_resource_storage_item` 2단계 — 기존 RUID 데이터 교체는 Maker 캐시 때문에 반영 안 됨)
3. 참조처 교체
   - 바닥: `RootDesk/MyDesk/CaveFloorTileSet.tileset`의 `datas[0].Id` + `RtsHudLogic.FloorRUID`(미니맵 셀)
   - 트랙: `RootDesk/MyDesk/RtsZoneLogic.TrackRUID`
4. Maker `refresh_workspace` → Play Test 확인 → `maker_save`

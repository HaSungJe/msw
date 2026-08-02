# 바닥 텍스처 변형 (256px 무이음새, tools/gen-cave-floor.js로 생성)

현재 적용: **cave-brown** (CaveFloorTileSet → CaveFloorBrown)

| 파일 | 톤 | 업로드된 계정 리소스 RUID | 상태 |
|---|---|---|---|
| `cave-brown.png` | 갈색(개미굴 흙) — 사용자 확정 2026-08-02 | `9bddf00f17224983b4037a1fe48986e0` (CaveFloorBrown) | **적용 중** |
| `cave-navy.png` | 감색(짙은 네이비) | `eac1d52283474a3d9d6f72a82f913376` (CaveFloorNavy) | 보관 |
| `cave-gray.png` | 청회색(석회암, 초기 v2) | `e9683cc55ec14f05b9c93a19f73fb74e` (LimestoneFloorTile — 주의: 데이터가 네이비로 덮인 상태) | 보관 |

## 톤 교체 방법
1. `tools/gen-cave-floor.js`의 `stops` 색 램프 수정 → PNG 생성
2. **새 리소스로 업로드** (msw-mcp `asset_create_account_resource_storage_item` 2단계 — 기존 RUID 데이터 교체는 Maker 캐시 때문에 반영 안 됨)
3. `RootDesk/MyDesk/CaveFloorTileSet.tileset`의 `datas[0].Id`를 새 RUID로 교체
4. Maker `refresh_workspace` → Play Test 확인 → `maker_save`

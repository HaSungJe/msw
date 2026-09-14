# Report — 화면 v2 (아티팩트 v16 → 실제 화면)

## Feature Summary
- **Feature**: 그리드 트랙(18×12·발판 81) + HUD v2(하단 제거, 시간/메소, 플레이어 목록, 영입+슬롯 6, 증강) + 팝업 공통 셸·영입/증강/3택1 껍데기
- **Entry point**: `RtsBootstrapLogic`(입장 → 그리드 시각화·배정·목록 통지) → `RtsZoneLogic`(좌표) / `RtsCameraAnchorComponent`(카메라·HUD) → `RtsHudLogic`·`RtsPopupLogic`(클라 UI)
- **Domain**: rts-base
- **기준 목업**: `.info/artifacts/hud-layout.html` v16 — Play Test 스크린샷을 픽셀 단위로 대조(그리드 좌 300·상 80·칸 80px 일치)

## Created/Modified/Deleted Files
| File | Change Type | Description |
|------|-----------|------|
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | modified | 구역 42.66×24(피치 48×32 유지), 카메라 오프셋 0, 스타디움 상수 5개+게터 삭제 → 그리드 상수(18×12, 칸 16/9, 좌 −14.667, 상 +10.222, 텍스처 스케일) |
| `RootDesk/MyDesk/RtsZoneLogic.mlua` | modified | 스타디움 경로·둘레·부호거리·슬롯 10×3·경계선 삭제 → 꺾임점 17개 → 경로 67칸/트랙 65/발판 81 생성, `GetTrackPoint(t∈[0,1])`·`GetTrackLength`·`GetCellCenter`·`IsRoadCell`·`IsPadCell`·`GetPadCount`·`GetPadCell`·`GetPlacementSlot`·`CellDistance`·`GetBossPoint`, 시각화 = 구역당 그리드 텍스처 1장 |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified(재작성) | 하단 바·미니맵·초상화·정보·스킬칸·툴팁·부대지정·Ctrl 핸들러·프레임 삭제 → 시간/메소 칩, 플레이어 목록(n/8·생존·비석·나·보는 중·클릭→구역), 영입 버튼 + 슬롯 6, 증강 버튼. API: `SetTime/SetMeso/RefreshPlayerList/SetPlayerAlive/SetWatchedZone/SetUnitSlot/ClearUnitSlot` |
| `RootDesk/MyDesk/RtsPopupLogic.mlua` + `.codeblock` | created | 팝업 공통 셸(딤·패널·제목·X·ESC) + 영입(모험가 탭·4계열 10직업·보유 0/6) / 증강(탭 5·빈 목록·상세) / 3택1(카드 3·대상 칩·대상 없이 수령, B 미리보기) |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | modified | `UpdateMinimapZone`→`SetWatchedZone`; **줌 잠금 해제 후 ZoomTo → 0.2초 뒤 잠금**(잠긴 채로는 ZoomTo가 무시됨) |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | modified | 배정/해제 뒤 `BroadcastPlayerList` — 닉네임·구역·생존을 탭/줄바꿈 문자열로 전 클라에 통지 |
| `tools/gen-track-grid.js` | created | 그리드 텍스처 생성기(1440×960, 포석 트랙·발판·점선·S/E·복귀 화살표) |
| `assets/textures/track-grid.png` | created | 생성 결과. 업로드 RUID `651583e1c1ee44cdb6d2a891755ab528` (ZoneTrackGrid, sprite/object) |
| `assets/textures/README.md` | modified | 그리드 트랙 항목, 스타디움·HUD 프레임 "보관", 교체 절차의 참조처 갱신 |
| `.beaver/output/roadmap/maple-augment-defense-roadmap.md` | modified | #2·#4 in-progress(화면 v2), 결정 대기 #1~#3 확정, 증강 흐름 기록 |

## Tests Written
CLI 러너 없음(docs/testing.md). 플랜의 `[CASES]`는 Play Test 중 `maker_execute_script`로 실행해 로그로 확인했다(아래). 위임형(목록 통지 호출·SetWatchedZone 호출)은 플랜대로 생략.

## Verification
Play Test(2026-09-14, 콜드 스타트 3회) — `maker_logs(build)` 0건, 런타임 스크립트 에러 0건(RectTileMap 수동 추가 경고는 기존과 동일).

**계산형 [CASES] — 15/15 PASS** (client `maker_execute_script`)
- `GetTrackPoint` t=0 → 구역중앙+(−10.222, +0.444) = (3열6행) / t=1 → (−10.222, −10.222) = (3열12행) / t=4/66 → (3열2행) / t=15/66 → (14열2행) / t=0.5/66 → 두 칸 중간 / t=1.3·−0.2 → 양끝 클램프
- `GetTrackLength` 117.333 · `IsRoadCell` (3,6)(12,6) true, (1,1)(4,6) false · `IsPadCell` (4,6)(6,3) true, (1,1)(3,6) false · `GetPadCount` 81 · `GetPadCell` 1=(3,1), 81=(8,12), 0·82 클램프 · `CellDistance` 0/1/4/6 · `GetBossPoint` = 구역 중앙 · 줌 30%

**화면 — 스크린샷 대조**
- 그리드 텍스처: 좌 299.6 · 상 79.6 · 칸 80.06px @1920 (목업 300·80·80). 8구역 전부 생성(F4 확인), 경계선 없음
- HUD: 좌상단 시간·메소 칩, 좌측 "1 / 8" + 내 행(금색 바·(나)), 우측 영입 + 빈 슬롯 6, 좌하단 증강. 하단 바·미니맵·스킬칸 없음
- `SetTime("12:34")`·`SetMeso(1250)` → "12:34"·"1,250" / `SetPlayerAlive(me,false)` → 회색 + 비석 / `SetUnitSlot` 3개 + 슬롯 2 선택 → 금색 테두리, 긴 직업명은 잘림 / F4 → 구역 4로 이동 + 내 행 하이라이트 해제
- 영입 팝업: 모험가 탭·4계열·10직업·"무료"·보유 0/6, ESC로 닫힘 / 증강 팝업: 탭 5(0)·"아직 얻은 증강이 없어요"·상세 / B → 3택1: 카드 3, 칩 선택 시 "3. 비숍에 수령"(금색), ESC 무시, 수령 → 닫힘(로그)

**빌드 중 실측으로 바뀐 것(플랜과 다른 점)**
1. **업로드 스프라이트 PPU = 30**(스타디움 텍스처의 100과 다름 — 1440px급 대형 이미지라 그런 듯). 텍스처 스케일 2.222 → **0.667**. 서브카테고리(background/object)는 무관.
2. **`IsAllowZoomInOut=false`면 `ZoomTo`가 무시된다.** ClaimCamera에서 허용 → ZoomTo → 0.2초 뒤 잠금으로 변경. (이전 빌드가 됐던 이유는 미상 — 지금 코드가 확실한 순서)
3. 팝업 안 반투명 색은 테두리 백킹이 비쳐 보여 **패널 기본색에 미리 합성한 불투명 색**(`Mix`)으로 통일.
4. `OverflowType.ellipsis`는 박스보다 긴 글이 오면 이전 글을 그대로 보여주는 문제 → 슬롯 직업명은 `Truncate`.
5. 스프라이트 중심 = 구역 중앙 + (+1.33, **−0.44**) (플랜의 −1.78은 오기 — 코드는 GridLeft/GridTop에서 계산).

## Remaining Issues
- 플레이어 목록은 **1인 Play Test로만 확인**(행 1개). 여러 명·퇴장 시 재정렬은 Phase 8 멀티 검증에서.
- 3택1 미리보기 **B 키**는 Phase 6에서 트리거 연결과 함께 제거.
- 슬롯의 긴 직업명("아크메이지(썬·콜)")은 잘려 보임 — 슬롯 폭을 더 늘리거나 약칭 도입은 사용자 판단.
- 영입 카드 가격은 "무료" 고정 문자열 — Phase 2 경제표 연결 시 교체.
- `.info/artifacts/hud-layout.html`(v16)과 화면을 계속 같이 맞춘다 — 페이즈 완료는 사용자 만족 루프.

## Change - 260914-1 · 배경 헤네시스로 (아티팩트 + 맵)
- **요청**: "트랙/타일 배경을 헤네시스로 변경. 아티팩트와 맵 모두"
- **변경**: 바닥 타일 엘나스 눈 → **헤네시스 잔디**(`tools/gen-henesys-floor.js` → `assets/textures/henesys-grass.png`, RUID `d908c425553c42c5b11016ab40b306f4`, `CaveFloorTileSet.tileset` datas[0] 교체). 트랙은 헤네시스 포석 유지, 잔디 위에서 읽히도록 그리드 텍스처 색만 재생성(빈 칸 선 짙은 초록·발판 흰 반투명, RUID `f8bf4274602c4d22b2e6643e114fbc5f` → `RtsZoneLogic.GridRUID`). 아티팩트 v17(`.ground` 잔디 톤·`.cell/.pad` 색) 같은 URL로 재발행, `.info/artifacts/hud-layout.html` 동기화. README 갱신(눈·회청판은 보관).
- **검증**: Play Test 콜드 스타트 — 잔디 바닥 + 포석 트랙, 그리드 위치·크기 불변, 빌드/런타임 에러 없음. 스크린샷이 아티팩트 v17과 같은 톤.
- **남은 것**: 없음(사용자 확인 대기).

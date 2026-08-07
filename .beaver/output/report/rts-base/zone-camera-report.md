# Report — 카메라·맵 개편 (운빨 디펜스 #3)

## Feature Summary
- **Feature**: 맵 192×56(8구역, 4열×2행) + F1~F8/미니맵 구역 스냅 카메라 + 자유 카메라 전면 제거
- **Entry point**: `RtsCameraAnchorComponent`(F키·JumpToZone) · `RtsHudLogic`(미니맵 구역 클릭) · `RtsConfigLogic`(구역 변환 단일 소스)
- **Domain**: rts-base

## Created/Modified/Deleted Files
| File | Change Type | Description |
|------|-----------|------|
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | modified | 구역 상수(4×2, 48×28)·`GetZoneCenter(n)`·맵 크기 파생(192×56). 삭제: ScrollSpeed/EdgeMarginPx/CameraMarginX·Y/고정 MapCells와 게터 |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | modified(전면) | F1~F8→JumpToZone(구역 중앙 순간이동)만 남김. 삭제: 방향키/엣지 스크롤, Confined 커서, 휠 줌(IsAllowZoomInOut=false), 경계 클램프, OnUpdate 전체 |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified | 미니맵 v6: 340 프레임 내 192:56 스트립 + 구역 경계선 + 번호 1~8 + 현재 구역 하이라이트. `UpdateMinimapViewport`(매 프레임)→`UpdateMinimapZone`(전환 시), 클릭은 구역 스냅으로 교체 |
| `RtsBootstrapLogic.mlua` / `map/RtsMap.map` | unchanged | 게터 경유 설계라 자동 적응 (타일 24×7=168) |

## 플랜 대비 변경점
- SetupClient에서 **BuildHud를 JumpToZone(1)보다 먼저** 호출 (하이라이트 초기 반영 순서 — 플랜은 역순이었음).

## Verification (Play Test 실측, 2026-08-03)
| 시나리오 | 결과 |
|---|---|
| 입장 시 구역 1 중앙(24,42) 시작 + 이웃 구역 미노출 | ✅ 좌표 로그 + 스크린샷 |
| 바닥 타일이 새 맵을 정확히 덮음 | ✅ tiles=168 (24×7) |
| F8 → (168,14)=구역 8 중앙, F3 → (120,42)=구역 3 중앙 | ✅ 좌표 로그 |
| 미니맵 스트립·경계선·번호·하이라이트 렌더 + 전환 시 하이라이트 이동(1→3) | ✅ 스크린샷 2매 |
| **방향키 2초 입력에도 카메라 부동** (자유 카메라 제거) | ✅ 좌표 불변 실측 |
| 무효 키(F9~) 무시 | ✅ (매핑 없음 — 코드 경로상 -1 반환) |
| 빌드/런타임 에러 | ✅ 0건 (기지 LEA-3035 제외) |
| 미니맵 클릭 → 구역 스냅 | ⚠️ 실마우스 확인 필요 (시뮬 클릭 불가 — #14 때 클릭 핸들러 자체는 검증됨) |

## Remaining Issues
1. **[수동 확인] 미니맵 클릭 구역 스냅** — 실마우스로 미니맵의 다른 구역 클릭 → 해당 구역 이동 확인.
2. 구역 배정 스텁 — 현재 입장 시 무조건 구역 1. 정식 유저→구역 배정은 #4 구역 시스템.
3. 구역 경계(맵 위 시각 구분선)는 #4에서 — 현재는 미니맵에만 경계 표시.

## Change - 260807-1 (구역 2열×4행 + 미니맵 셀 + 반응형)
**요청**: 미니맵 4×2 → 2×4, 미니맵 영역 꽉 채우기, 번호는 셀 중앙, 셀마다 해당 구역 축소 화면. 추가로 화면 늘렸다 줄이면 UI가 깨짐.

**구현**:
- `RtsConfigLogic`: ZoneCols 4→**2**, ZoneRows 2→**4**. 맵 192×56 → **96×112**(구역 48×28 유지). `GetZoneCenter`는 cols/rows 파생이라 수정 불필요.
- `RtsHudLogic` 미니맵 재구성: 단일 스트립+경계선 → **구역 셀 8개**(각 셀 = 바닥 텍스처 축소 화면, 2px 간격). 스트립 320×93 → **340×340**(미니맵 영역 꽉 채움, 셀 170×85). 번호는 **셀 중앙**, 하이라이트보다 나중에 생성해 가려지지 않음.
- **반응형 수정**: ① 하단 바를 고정폭 1920 → **가로 스트레치 앵커**(AnchorsMin(0,0)/Max(1,0)+OffsetMin/Max), ② 선택영역을 고정폭 계산 → **좌우 스트레치**(미니맵+초상화 ~ 스킬칸 사이 자동 신축), ③ 미니맵 클릭 좌표를 `cursor*1920/ScreenWidth` 수동 환산 → **`_UILogic:ScreenToLocalUIPosition`**(해상도·레터박스 무관). 신규 헬퍼 `SpawnStretch`/`AttachFrameStretch`.

**검증(Play Test 2026-08-07)**: 맵 96×112·타일 168 ✓ / 입장 구역1=(24,98) ✓ / F6→(72,42)=GetZoneCenter(6) 일치 ✓ / 미니맵 2×4 꽉 채움·번호 중앙·하이라이트 1→6 이동 ✓ / 빌드·런타임 에러 0건 ✓.

**미확인**: 실제 창 리사이즈 테스트는 Maker 창 크기를 MCP로 바꿀 수 없어 미실측 — 앵커/변환 API 기준의 구조적 수정입니다. 늘렸다 줄여보고 남는 깨짐이 있으면 알려주세요.

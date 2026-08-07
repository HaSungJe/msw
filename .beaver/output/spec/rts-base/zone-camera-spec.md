---
feature_goal: "카메라·맵 개편 — 맵을 8구역(4열×2행, 구역=한 화면)으로 축소, F1~F8/미니맵 구역 스냅 전환, 자유 카메라 전면 제거"
domain: "rts-base"
api_method: "Client Input (F1~F8, 미니맵 클릭)"
api_path: "RtsCameraAnchorComponent(개편) · RtsConfigLogic(구역 상수) · RtsHudLogic(미니맵 개편)"
affected_data: []
---

## Feature Description
운빨 디펜스 피벗(로드맵 #3, 사용자 지시). 맵을 "카메라 한 화면 = 1인 구역" × 8로 재구성하고, 카메라를 자유 이동에서 **구역 시점 전환 전용**으로 바꾼다.

- **맵**: 구역 48×28유닛(카메라 뷰 44.5×25가 여유 있게 들어가는 크기) × **4열×2행** = **192×56유닛**. 바닥 타일(8유닛)로 24×7=168타일 — 기존 부트스트랩 채우기가 상수만 바꾸면 그대로 동작.
- **구역 번호**: 화면 감각 기준 좌상단부터 행 우선 — 윗줄 1·2·3·4, 아랫줄 5·6·7·8. Fn키 = 구역 n.
- **카메라**: 항상 어떤 구역의 중앙에 고정. F1~F8로 해당 구역 중앙으로 즉시 이동. 게임 입장 시 자기 구역(배정은 #4 — 1차는 구역 1 고정 스텁)으로.
- **미니맵**: 340 프레임 안에 **맵 비율 스트립(192:56)** 표시 + 구역 경계선 + 구역 번호. **클릭 시 해당 구역으로 스냅 이동**(자유 위치 이동 아님 — 사용자 확정). 뷰포트 표시는 현재 보고 있는 구역 하이라이트로 대체.
- **제거**: 방향키 스크롤, 엣지 스크롤, 커서 가두기(Confined), 휠 줌, 카메라 경계 클램프/마진 — 전부 삭제 (자유 카메라 금지).

## Entry Point
- Method: Client Input — `KeyDownEvent`(F1~F8), 미니맵 `ButtonClickEvent`
- Path: `RtsCameraAnchorComponent`(전면 개편) / `RtsConfigLogic`(구역 상수·좌표 변환) / `RtsHudLogic`(미니맵 v6)
- Request: F1~F8 키, 미니맵 클릭 좌표
- Response: 카메라(숨긴 아바타)가 대상 구역 중앙으로 `SetWorldPosition`, 미니맵 구역 하이라이트 갱신

## Business Rules
1. 구역 크기 48×28 > 카메라 뷰 44.5×25 — 구역 중앙 고정 시 **이웃 구역이 화면에 안 보인다** (구역 여백 각 1.75/1.5유닛).
2. F1~F8은 언제나 유효(다른 유저 구역 구경 허용 — 스타 관례). 미니맵 클릭도 동일하게 구경 이동.
3. 구역 인덱스↔월드 변환은 `RtsConfigLogic` 게터 단일 소스(#4 구역 시스템이 이어받음): `GetZoneCenter(n)`, `GetZoneCols/Rows/Width/Height`.
4. 카메라 이동은 순간 이동(트윈 없음 — 스타 동일). DeadZone 0 유지로 즉시 고정.
5. 기존 부대지정(Ctrl+숫자)·스킬칸 단축키와 키 충돌 없음(F키 사용).

## Notes
- 수정 대상 근거: RtsCameraAnchorComponent.mlua(스크롤/Confined/클램프 전부 — 삭제 대상), RtsConfigLogic.mlua(MapCells 256→맵 192×56·구역 상수), RtsHudLogic.mlua(미니맵 사각 340 전제 → 스트립+구역), RtsBootstrapLogic.mlua(변경 불필요 — 게터 경유라 자동 적응).
- §1.7 삭제 체크: ScrollSpeed·EdgeMarginPx·CameraMarginX/Y 상수와 게터, InputDirection 프로퍼티, 방향키 KeyDown/Up 핸들러(카메라용), IsPointerOverUI 엣지 가드 — 모두 제거. HUD 훅·아바타 숨김·뷰포트 갱신 훅은 유지.
- 미니맵 스트립: 340 내부에 320×93px(192:56 비율) 중앙 배치. 구역 1칸 = 80×46.5px — 클릭 판정 충분.

## Proposals (Codebase-Based)
- [x] 구역 좌표 변환을 RtsConfigLogic에 두고 #4 구역 시스템이 그대로 승계 (Cross-Cutting Rule "구역 좌표 단일 소스" 선행 이행).
- [x] 미니맵 개편 시 뷰포트 사각형을 "현재 구역 하이라이트"로 재사용 (기존 UpdateMinimapViewport 훅 유지).

## Decisions
- [x] 구역 배열 — **4열×2행** (사용자 확정 2026-08-02, "가로 2줄 세로 4줄").
- [x] 미니맵 클릭 — **유지, 구역 스냅 이동** (사용자 확정).
- [x] 구역 크기 48×28 / 맵 192×56 — 뷰(44.5×25) 실측 기반 제안값, Play Test 튜닝 가능.
- [x] 휠 줌 — 제거 (자유 카메라 금지 취지에 포함. 원작도 줌 없음).
- [x] 입장 시 시점 — 자기 구역(1차는 구역 1 스텁, 정식 배정은 #4).

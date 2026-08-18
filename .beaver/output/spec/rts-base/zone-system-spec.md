---
feature_goal: "구역 시스템 — 8구역 구획·경계 시각화, 유저→구역 배정(빈 구역 처리), 구역 내부 스타디움(라운드 사각형) 트랙(11시 스폰·반시계) + 안쪽 유닛 배치 슬롯"
domain: "rts-base"
api_method: "Server(배정·시각화) + Shared(구역/트랙 좌표 변환)"
api_path: "RtsZoneLogic(신규) · RtsConfigLogic(트랙·슬롯 수치) · RtsBootstrapLogic(입장 시 배정) · RtsCameraAnchorComponent(배정 구역으로 점프)"
affected_data: []
---

## Feature Description
로드맵 #4. 8구역을 실제 무대로 만들고, 각 구역 안에 **스타디움 트랙 + 안쪽 유닛 배치 영역**을 세운다. 이후 #5(몹 웨이브)·#6(뽑기 배치)·#7(전투)이 전부 이 좌표계를 사용한다.

- **구역 구획·시각화**: 8구역(2열×4행, 구역 40×16, 배치 피치 48×32)의 경계를 월드에 선으로 표시. 구역별 스타디움 트랙과 안쪽 배치 영역도 함께 표시.
- **스타디움 트랙**: 화면 가로로 긴 라운드 사각형(외곽 35×12.77, 코너 반경 2.37 — 사용자가 스크린샷에 그린 빨간 박스 기준). 몹은 **11시(좌상단 코너)에서 스폰 → 반시계 순환** — #5가 이 API로 이동시킨다.
- **유닛 배치 영역**: 트랙 안쪽. **10열×3행 그리드 슬롯**(트랙에 가까운 윗줄 → 아랫줄 → 가운데줄 순으로 채움).
- **유저→구역 배정**: 입장 순서대로 빈 구역 배정(서버 권위), 퇴장 시 해제. 배정 즉시 그 유저 카메라가 자기 구역으로 이동.
- **빈 구역 처리**: 미배정 구역은 흐리게 표시하고 `IsZoneOccupied`로 조회 가능 — #5가 이걸 보고 몹을 안 뿌린다.

## Entry Point
- Method: Server(UserEnterEvent 배정·시각화 생성) / Shared(좌표 변환 게터) / Client(배정 구역 카메라 점프)
- Path: `RtsZoneLogic` — `AssignZone/ReleaseZone/GetZoneOfUser/IsZoneOccupied`, `GetTrackPoint(zone,t)/GetSpawnPoint(zone)/GetTrackPerimeter`, `GetPlacementSlot(zone,index)/GetPlacementSlotCount/IsInPlacementArea`, `TrackSignedDistance`, `EnsureZoneVisuals`
- Request: 유저 입장/퇴장, 좌표 질의(둘레 파라미터 t·슬롯 인덱스)
- Response: 배정 구역 번호, 월드 좌표, 구역 경계·트랙 선 엔티티

## Business Rules
1. **경로 규약**: 트랙 위 위치는 둘레 정규화 파라미터 `t∈[0,1)`. **t=0 = 11시(좌상단 코너 진입)**, **t 증가 = 반시계**(좌변 하강 → 아랫변 → 우변 상승 → 윗변). 각도 대신 t를 쓰는 이유는 정원이 아니라서 등속 이동에 호길이 파라미터가 필요하기 때문.
2. **트랙 스타디움**: 외곽 35×12.77, 코너 반경 2.37, 레인 반폭 0.8. 중심선 직선부 반길이 hw=14.23 / hh=3.11, 둘레 84.27. 구역 40×16 안에 좌우·상하 여백을 남긴다.
2-1. **구역 간 여백**: 뷰(42.66×24)가 구역(40×16)보다 커서 간격 0이면 이웃 구역이 화면에 들어온다. 여백 가로 8·세로 16 → **배치 피치 48×32, 맵 96×128**. 구역 크기와 배치 간격은 별개 값이다(`GetZonePitchX/Y`).
3. **배치 슬롯**: 트랙 안쪽 10열×3행 = **30슬롯**. 채우기 순서는 **윗줄 → 아랫줄 → 가운데줄**(트랙에 가까운 쪽 우선). (#6 자동 배치가 이 순서를 사용)
4. **배정**: 서버가 유일 권위. 가장 낮은 빈 구역부터 배정, 8구역 만석이면 0 반환(관전 — #10 방 시스템에서 인원 제한으로 정식 처리).
5. **시각화는 서버가 1회 생성**(EnsureGroundTiles와 동일한 멱등 패턴) — 클라마다 중복 생성 금지.
6. 좌표 변환의 단일 소스는 `RtsZoneLogic`(Cross-Cutting Rule). 원시 수치만 `RtsConfigLogic`에 둔다. 기존 `GetZoneCenter`는 카메라(#3)가 이미 쓰므로 Config에 그대로 두고 Zone이 이를 사용.

## Notes
- 근거: `RtsConfigLogic.mlua`(ZoneCols 2·ZoneRows 4·GetZoneCenter), `RtsBootstrapLogic.mlua`(UserEnterEvent + 멱등 EnsureGroundTiles 패턴), `RtsCameraAnchorComponent.mlua`(JumpToZone·SetupClient 스텁 `JumpToZone(1)`).
- 구역 크기는 카메라 실측에 맞춰 48×28 → **40×16**으로 축소(뷰 42.66×24, HUD가 하단 31.5%를 가려 실사용 밴드 16.44). 구역 사이에는 여백을 둬 이웃 구역이 뷰에 들어오지 않게 한다.
- 트랙/경계 렌더는 `LineRendererComponent`가 아니라 **스프라이트**(빌드 중 LineRenderer가 월드에서 신뢰성 있게 그려지지 않아 폐기).
- §1.7: SetupClient의 `JumpToZone(1)` 하드코딩 스텁은 **배정 구역 사용으로 대체**(제거 대상). 그 외 삭제될 코드 없음.
- §1.8: 서버 권위·멱등 생성은 `RtsBootstrapLogic.EnsureGroundTiles`의 형제 패턴을 그대로 따름(존재 확인 후 조기 반환).
- 월드 빈 엔티티 모델 id는 존재하지 않아 **`model://defaultplayer` + 렌더러/카메라 비활성 폴백**을 사용(빌드 중 실증). 복제본이 CameraComponent를 들고 오므로 반드시 꺼야 하고, 그래도 활성 카메라를 뺏기는 경우가 있어 클라이언트가 `SwitchCameraTo`로 되찾는다.

## Proposals (Codebase-Based)
- [x] 구역 시각화를 서버 1회 생성으로 (EnsureGroundTiles 형제 패턴 재사용).
- [x] 배정 구역 전달은 Client 실행공간 메서드의 **마지막 파라미터 UserId** 규약으로 해당 클라에만 전송(공식 문서 패턴).

## Decisions
- [x] 트랙 주체 — **몹이 순환, 내 유닛은 원 안쪽 배치** (사용자 확정 2026-08-07).
- [x] 트랙 모양 — **스타디움(라운드 사각형) 외곽 35×12.77, 코너 반경 2.37** (사용자가 스크린샷에 그린 빨간 박스 기준, 2026-08-18 확정). 초안의 정원 r=12는 폐기.
- [x] 스폰 지점 — 11시(t=0), 반시계(t 증가).
- [x] 배치 슬롯 — 10×3 그리드 30슬롯, 윗줄→아랫줄→가운데줄 순 (튜너블).
- [x] 구역 간 여백 — 가로 8·세로 16(피치 48×32) (사용자 지시 2026-08-18: 이웃 구역이 화면에 잘려 보임).
- [x] 빈 구역 — 흐리게 표시 + `IsZoneOccupied` 제공(몹 미스폰은 #5에서).

# Plan — 화면 v2 (아티팩트 v16 → 실제 화면)

## Feature Summary
- **Feature**: 그리드 트랙(18×12·발판 81) + HUD v2(하단 제거, 시간/메소, 플레이어 목록, 영입+슬롯 6, 증강) + 팝업 공통 셸·영입/증강/3택1 껍데기
- **Entry point**: `RtsBootstrapLogic`(입장 → 시각화·배정·목록 통지) → `RtsZoneLogic`(좌표) / `RtsCameraAnchorComponent`(카메라·HUD 생성) → `RtsHudLogic`·`RtsPopupLogic`(클라 UI)
- **Domain**: rts-base
- **기준 목업**: `.info/artifacts/hud-layout.html` v16 — 빌드 중 화면과 나란히 놓고 맞춘다
- **작성 방식**: 이 문서는 코드가 아니라 **동작·방향 설명**(`.beaver/memory/workflow.md`). 코드는 build가 쓴다.

---

## File List

| File | Action |
|------|------|
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | modified — 구역 42.66×24, 카메라 오프셋 0, 스타디움 상수 삭제, 그리드 상수(열·행·칸·원점) 추가 |
| `RootDesk/MyDesk/RtsZoneLogic.mlua` | modified — 스타디움 트랙/슬롯/부호거리 삭제 → 그리드 경로·발판·8방향 거리·보스 자리, 시각화는 그리드 텍스처 1장/구역, 경계선 삭제 |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified(사실상 재작성) — 하단 바·미니맵·스킬칸·부대지정 삭제, 시간/메소 칩·플레이어 목록·영입+슬롯·증강 버튼 |
| `RootDesk/MyDesk/RtsPopupLogic.mlua` | new — 팝업 공통 셸 + 영입/증강/3택1 내용 |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | modified — `UpdateMinimapZone` 호출 → `SetWatchedZone` |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | modified — 배정/해제 뒤 전 클라에 플레이어 목록 통지 |
| `tools/gen-track-grid.js` | new — 그리드 트랙 텍스처 생성기(1440×960) |
| `assets/textures/track-grid.png` | new — 생성 결과(업로드 원본) |
| `assets/textures/README.md` | modified — 그리드 트랙 항목 추가, 스타디움 2종 "보관" |
| `RootDesk/MyDesk/CaveFloorTileSet.tileset`, `map/*.map` | unchanged |

---

## Design

> 근거: `RtsConfigLogic.mlua`(ZoneWidth 40·ZoneHeight 16·CameraOffsetY −3.8·Track* 상수), `RtsZoneLogic.mlua`(GetTrackPoint 스타디움·GetPlacementSlot 10×3·SpawnProp·EnsureZoneVisuals 멱등), `RtsHudLogic.mlua`(SpawnUI/SpawnStretch/SpawnText/Tint·BuildHud·OnMinimapClick→JumpToZone), `RtsCameraAnchorComponent.mlua`(SetupClient→BuildHud·JumpToZone→UpdateMinimapZone), `RtsBootstrapLogic.mlua`(UserEnter→AssignZone→ApplyAssignedZone).

### 화면 배치 (1920×1080 기준 — 목업 v16 그대로)

```text
┌──────────────────────────────────────────────────────────────────────┐
│[시간 --:--]                                          (MSW 시스템 버튼)│
│[메소 0    ]                                                          │
│┌────────┐   ┌─── 그리드 18×12 (x 300~1740, y 80~1040) ───┐  ┌──────┐ │
││ n / 8  │   │  S(3,6)↑ … 트랙 65칸, 발판 81칸, 교차 2   │  │ 영입 │ │
││● 나(나)│   │  E(3,12) → 왼쪽 점선으로 S 복귀            │  ├──────┤ │
││● 유저2 │   │  보스 자리 = 화면 중앙 (960,540)           │  │1 빈  │ │
││▩ 탈락  │   │                                            │  │2 빈  │ │
│└────────┘   └────────────────────────────────────────────┘  │ … 6  │ │
│[증강]                                                        └──────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

### 좌표 환산 (RtsConfigLogic — 원시 수치만)

```text
1유닛 = 45px (뷰 42.66×24 ↔ 1920×1080)
칸     = 80px = 1.778유닛          그리드 = 18×12칸 = 32 × 21.33유닛
그리드 좌상단 = 구역 중앙 + (−14.67, +10.22)   ← 목업 OX=300, OY=80
칸(col,row) 중심 = (좌 + (col+0.5)·칸,  상 − (row+0.5)·칸)   ※ row는 위에서 아래로
구역 = 42.66×24 (뷰와 동일), 피치 48×32 유지 → 맵 96×128 불변, 카메라 오프셋 0
텍스처 1440×960 → 스케일은 업로드 PPU에 따름(실측 PPU 30 → 0.667), 중심 = 구역 중앙 + (+1.33, −0.44) = 그리드 중앙
```

- 스타디움 상수(`TrackOuterW/H`, `TrackTextureScale`, `TrackCornerR`, `TrackLaneHalf`)와 게터는 **삭제**. 대신 `GridCols=18`, `GridRows=12`, `GridCell=16/9`, `GridLeft=−14.667`, `GridTop=10.222`, `GridTextureScale`(실측 0.667)와 게터.
- `ZoneWidth/Height`는 42.66/24, `ZoneGapX/Y`는 5.34/8(피치 48/32 유지 — 주석의 "HUD 31.5% 가림" 근거는 지운다). `CameraOffsetY=0`.

### 그리드 트랙·발판 (RtsZoneLogic — 좌표 단일 소스)

- **경로 정의**: 목업의 꺾임점 17개 (3,6)→(3,2)→(14,2)→(14,6)→(9,6)→(9,8)→(14,8)→(14,10)→(12,10)→(12,4)→(7,4)→(7,8)→(3,8)→(3,10)→(7,10)→(7,12)→(3,12) [1-기반 열,행]을 상수 표로 두고, 스크립트 시작 시 한 번 펼쳐 **칸 목록 67개**(순서 보존)·**트랙 칸 집합 65**·**발판 목록 81**(행 우선)을 만들어 둔다. 목업 `seq`와 0-기반/1-기반만 다르고 같은 값.
- `GetTrackLength()` = 66 × 칸 = 117.33. `GetTrackPoint(zone, t)`: t를 0~1로 잘라 길이에 곱한 뒤 몇 번째 칸 사이인지 찾아 두 칸 중심을 보간. `GetSpawnPoint`=t 0, `GetEndPoint`=t 1.
- `GetCellCenter(zone,col,row)`, `IsRoadCell(col,row)`, `IsPadCell(col,row)`, `GetPadCount()`=81, `GetPlacementSlot(zone,index)`=index번째 발판 중심(이름 유지 — 로드맵 #14 참조), `GetPadCell(index)`=(col,row).
- `CellDistance(c1,r1,c2,r2)` = max(|Δ열|,|Δ행|). 사거리 상수는 여기 두지 않는다(Phase 2 직업 테이블).
- `GetBossPoint(zone)` = 구역 중앙(그리드 9~10열·6~7행 사이). Phase 7이 사용.
- **삭제**: `GetTrackHalfW/H`, `GetTrackPerimeter`, 스타디움 `GetTrackPoint`, `TrackSignedDistance`, `IsInPlacementArea`, `TrackRUID`(스타디움), 경계선 4장 생성 루프. `GetPlacementSlotCount`는 이름을 남기되 81을 돌려준다.
- **시각화** `EnsureZoneVisuals`: 멱등 가드(첫 프롭 존재 확인)는 그대로. 구역마다 `SpawnProp("ZoneGrid"..n, …)` 1개 — 그리드 텍스처 RUID, 스케일 0.667(PPU 30 실측), 위치 = 그리드 중앙(GridLeft/GridTop에서 계산). 프롭 이름을 `ZoneTrack`→`ZoneGrid`로 바꾸면 가드도 같이.

### 그리드 텍스처 (tools/gen-track-grid.js → assets/textures/track-grid.png)

```text
1440×960, 투명 배경, 칸 80px, 같은 경로 표를 스크립트 안에 복사
  빈 칸   : 테두리만 rgba(120,135,160,.22) 1.5px
  발판    : 채움 rgba(120,135,160,.10) + 테두리 .35 1.5px
  트랙 칸 : 헤네시스 포석(gen-track-stone의 돌 패턴을 칸 단위로) + 테두리 #6b645a 3px
  진행선  : 칸 중심을 잇는 흰 점선(#e9e2d2, 14/22) — 정적
  S / E   : 초록(S, 3열6행)·빨강(E, 3열12행) 원 + 5×7 비트맵 글자
  복귀    : 3열 왼쪽 여백에 빨간 점선 세로선(12행→6행) + 위쪽 화살촉
```
- 업로드는 README "교체 절차": 새 리소스 생성(msw-mcp) → RUID를 `RtsZoneLogic.GridRUID`에. 스타디움 텍스처 2종은 README에 "보관".

### HUD v2 (RtsHudLogic — 전면 교체)

```text
좌상단  RtsTimeChip  (x 16, y −16, 200×44)  "시간  --:--"
        RtsMesoChip  (x 16, y −66, 200×44)  "M  0"
좌측    RtsPlayers   (x 16, 세로 중앙보다 위, 230×(48+40n))
          RtsPlayerHead "n / 8"
          RtsPlayerRow{i}: 상태점(초록 ●/비석) + 닉네임 (+ "(나)" · 금색 바)
우측    RtsRecruitBtn (우 −16, 상 −16, 190×56) "영입"
        RtsUnitSlot1~6 (그 아래 190×52 간격 8) "빈 자리" 점선
좌하단  RtsAugBtn (x 16, y 16, 150×56) "증강"
```
- 기존 헬퍼 4개(`SpawnUI/SpawnStretch/SpawnText/Tint`)는 유지. 프레임 오버레이(`AttachFrame*`)와 프레임 RUID 3종·`FloorRUID`·미니맵/스킬/툴팁/부대지정 전부 삭제. `HandleKeyDownEvent/Up`(Ctrl 감지)·`KeyToDigit` 삭제.
- **API**: `SetTime(text)`, `SetMeso(n)`(천 단위 콤마), `RefreshPlayerList(entries)`(서버 통지: 유저별 닉네임·구역·생존·userId, 구역순), `SetPlayerAlive(userId, alive)`, `SetWatchedZone(n)`(그 구역 유저 행 밝게), `SetUnitSlot(i, no, jobName, level, series)`, `ClearUnitSlot(i)`.
- **클릭**: 플레이어 행 → 그 유저의 구역으로 `JumpToZone`(`OnMinimapClick`의 역할을 행 클릭이 이어받음). 영입 버튼 → `_RtsPopupLogic:Open("recruit")`, 증강 버튼 → `Open("augment")`. 슬롯 클릭 → 선택 표시만(금색 테두리), 발판 링은 Phase 4.
- 나 표시: `_UserService.LocalPlayer`의 userId와 비교.

### 팝업 셸 (RtsPopupLogic — new)

```text
RtsPopupGroup(uigroup, 기본 숨김)
  RtsPopupDim   (전체 스트레치, 검정 45%, 클릭 → Close)
  RtsPopupPanel (중앙, 1114×N, 배경 rgba(28,24,19,.96), 금색 테두리)
    RtsPopupTitle · RtsPopupClose(✕)
    RtsPopupBody  ← kind별로 비우고 다시 채움
```
- `Open(kind)`: 이미 열려 있으면 `Close()` 후 진행. body를 kind 빌더로 채우고 그룹 표시. `Close()`: 그룹 숨김 + body 비우기. `IsOpen()`.
- **ESC**: PopupLogic이 InputService KeyDown을 직접 받아 열린 팝업을 닫는다(3택1은 예외). **B**: 3택1 미리보기(Phase 6에서 제거 — 코드에 그 표시).
- **recruit 빌더**: 탭 줄(모험가 [on] · …) → 계열 4묶음(전사·궁수·마법사·도적 라벨 + 직업 카드) → 푸터 `보유 0 / 6`. 카드 = 직업명 + 다음 영입가(지금은 `무료`). 카드 클릭은 로그만.
- **augment 빌더**: 패널 높이 960. 탭 줄(전체·브론즈·실버·골드·프리즘, 개수 0) → 좌 목록(비어 있음 → `아직 얻은 증강이 없어요`) · 우 상세(빈 상태). 미지정 `!`·유닛 지정 UI는 항목이 생길 때(Phase 6).
- **pick(3택1) 빌더**: 제목 `보스 처치 — 증강 선택`, 카드 3장(예시: 실버 공격력 +12% / 브론즈 드랍 메소 +3% / 골드 광역 사거리 +1). 카드 = 등급색 상단 띠 + 등급 배지 + 이름 + 설명 + 대상 칩 5개(예시 유닛) + `대상 없이 수령` 버튼(칩 선택 시 `n. 직업에 수령`). 수령 클릭 → 닫고 로그. 닫기 ✕ 없음, ESC·딤 무시.
- 색·크기는 목업 CSS 값을 1cqw=19.2px로 환산.

### 카메라·부트스트랩 연결

- `RtsCameraAnchorComponent.JumpToZone`: `UpdateMinimapZone(n)` → `SetWatchedZone(n)`. 그 외 그대로(F1~F8·ClaimCamera).
- `RtsBootstrapLogic`: `AssignZone` 뒤와 `ReleaseZone` 뒤에 현재 배정 표(닉네임·구역·생존)를 만들어 **모든 클라**의 `RefreshPlayerList`를 호출. 늦게 들어온 유저도 자기 입장 통지로 전체 표를 받는다. 닉네임 조회 API는 빌드 시 `mlua_api_retriever`로 확인.

### 삭제 목록 (§1.7 — 추가와 함께 반드시 제거)
- RtsConfigLogic: 스타디움 상수 5개 + 게터 5개, HUD 가림 주석
- RtsZoneLogic: 스타디움 경로·둘레·부호거리·슬롯 10×3·경계선 4장·`TrackRUID`
- RtsHudLogic: 하단 바·미니맵(셀·번호·하이라이트·클릭)·초상화·정보 영역·스킬칸(버튼·키·툴팁)·부대지정 탭·Ctrl 핸들러·프레임 첨부·프레임 RUID
- RtsCameraAnchorComponent: `UpdateMinimapZone` 호출

---

## Test Cases
> Play Test 시나리오 (`maker_save → logs(build) → play → logs·screenshot → stop`). CLI 러너 없음(docs/testing.md). 계산형은 Play 중 `maker_execute_script`로 값을 찍어 확인한다.

```
[CASES:GetTrackPoint]  zone1 t=0   → (3열6행) 중심 = 구역중앙 + (−10.22, +0.44)
[CASES:GetTrackPoint]  zone1 t=1   → (3열12행) 중심 = 구역중앙 + (−10.22, −10.22)
[CASES:GetTrackPoint]  zone1 t=4/66 → (3열2행) 중심 (첫 꺾임점, 위로 4칸)
[CASES:GetTrackPoint]  zone1 t=15/66 → (14열2행) 중심 (두 번째 꺾임점)
[CASES:GetTrackPoint]  zone1 t=0.5/66 → (3열6행)과 (3열5행)의 중간
[CASES:GetTrackPoint]  t=1.3 → t=1과 같은 점 (클램프) / t=−0.2 → t=0과 같은 점
[CASES:GetTrackLength] → 117.33 (66 × 1.778)
[CASES:IsRoadCell]     (3,6)=true · (12,6)=true(교차) · (1,1)=false · (4,6)=false
[CASES:IsPadCell]      (4,6)=true(3열6행 오른쪽) · (6,3)=true(궁수 자리) · (1,1)=false(비면접) · (3,6)=false(트랙)
[CASES:GetPadCount]    → 81
[CASES:GetPlacementSlot] index 1 = 행 우선 첫 발판 / index 81 = 마지막 / 0·82 → index 1·81로 클램프
[CASES:CellDistance]   (5,3)-(5,3)=0 · (5,3)-(6,4)=1 · (5,3)-(9,3)=4 · (2,2)-(5,8)=6
[SUCCESS] 입장 시 8구역 각각 그리드 텍스처 1장, 경계선 없음 (F1/F4/F8 스크린샷이 목업과 같은 배치)
[SUCCESS] 카메라: 구역 중앙이 화면 중앙, 그리드 왼쪽 300px·위 80px에서 시작(스크린샷 자로 확인)
[SUCCESS] HUD: 좌상단 시간·메소, 좌측 목록 "1 / 8" + 내 행 (나) 금색, 우측 영입+빈 슬롯 6, 좌하단 증강 — 하단 바·미니맵·스킬칸 없음
[SUCCESS] SetTime("12:34")·SetMeso(1250) → 칩 텍스트 "12:34"·"1,250"
[SUCCESS] 플레이어 행 클릭 → 그 구역으로 카메라 이동 + 그 행 밝게 (F키 이동도 행 하이라이트 동기)
[SUCCESS] 영입 클릭 → 딤+패널, 모험가 탭·4계열·직업 10종·"보유 0 / 6"; ✕·딤·ESC로 닫힘
[SUCCESS] 증강 클릭 → 세로 긴 패널, 탭 5개(0), "아직 얻은 증강이 없어요"
[SUCCESS] B → 3택1 카드 3장; ESC·딤으로 안 닫힘; 칩 선택 시 버튼 문구 "n. 직업에 수령"; 수령 → 닫힘
[SUCCESS] 팝업 하나 열린 채 다른 버튼 → 이전 팝업 닫히고 새 팝업
[SUCCESS] SetPlayerAlive(me,false) → 내 행 회색 테두리 + 비석
[SUCCESS] logs(build)·logs(normal)에 에러 없음, 카메라 하이재킹 없음(ClaimCamera 유지)
```
DataStorage 미사용 → [SMOKE:data-access] 해당 없음.
테스트 생략(위임형): `RtsBootstrapLogic`의 목록 통지 호출(전달만), `RtsCameraAnchorComponent`의 `SetWatchedZone` 호출(전달만).

---

## Response Codes
| 결과 | 원인 |
|------|------|
| 좌표 반환 | `GetTrackPoint/GetCellCenter/GetPlacementSlot` — 항상 값. t·index는 범위로 클램프, zone 밖(1~8 외)은 구역 1로 |
| 시각화 생성/생략 | `EnsureZoneVisuals` — 첫 호출 생성, 이후 조기 반환(로그 1회) |
| HUD 갱신 무시 | `Set*` 호출이 `BuildHud` 전이면 무시(로그 없음) |
| 팝업 열림/닫힘 | `Open(kind)` 알 수 없는 kind → 로그 후 무시 |
| 목록 갱신 | `RefreshPlayerList` — 통지 표 그대로 다시 그림(행 수 변동 허용) |

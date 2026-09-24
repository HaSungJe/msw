# Plan — 맵 테마 프리셋 + 몬스터 아이콘 + 유저 카드 (로드맵 ① Phase 10 #38 + Phase 14 #40 + Phase 11 #41)

## Feature Summary
- **Feature**: 내 구역 외형 테마 5종(헤네시스·엘리니아·페리온·커닝시티·리스항구, 뼈대 + 임시 모양) · 몬스터 아이콘 247종 수집(매우어려움 처치 1%, 획득 일시 저장)·선택 · 좌측 유저 카드(테마 썸네일 배경·동그란 아이콘·닉네임·내 카드 초록 테두리·[수정]) · 디자인 인계 문서
- **Entry point**: `RtsProfileLogic.RequestSetTheme(key)` · `RtsProfileLogic.RequestSetIcon(monsterId)` (Server, senderUserId) · `RtsProfileLogic.OnMonsterKilled(zone, monsterId)` (ServerOnly, `RtsMonsterComponent.Die`에서) · `RtsProfileLogic.SendProfile` / `ShowIconGot` (Client, 그 유저에게만) · `RtsHudLogic.RefreshPlayerList(packed)`(서명 그대로, 줄에 테마·아이콘 칸 추가)
- **Domain**: rts-custom (spec: `.beaver/output/spec/rts-custom/theme-icon-preset-spec.md`)
- **진행 방식**: 문서는 방향·동작 설명(메모리 workflow — 코드 블록은 구조·흐름 도식만). 사용자가 만족할 때까지 같은 작업 안에서 수정 루프. 디자인(텍스처·장식·썸네일·색)은 ChatGPT 몫 — 이 작업은 기능 뼈대와 인계 문서까지.

---

## Prerequisites
- [x] 엔진 API 확인 — `RectTileMapComponent.ToCellPosition / BoxFill / SetTile`(구역만 다시 칠하기), DataStorage 한도(값 300,000바이트·4,000바이트당 1크레딧) — 2026-09-25 mlua 문서
- [x] 공식 탑뷰 장식 자산 조사 — `topview_henesys`만 있음(엘리니아·페리온·커닝·리스 없음) → 새 4종은 임시 모양, 장식은 ChatGPT

---

## File List

| File | Action |
|------|------|
| `RootDesk/MyDesk/RtsProfileLogic.mlua` | **new** — 유저별 테마·선택 아이콘·보유 아이콘(획득 일시) 서버 상태, 불러오기·저장, 변경 RPC, 처치 훅(1% 획득), 그 유저에게 전달 |
| `RootDesk/MyDesk/RtsThemeLogic.mlua` | modified — 프리셋 5종(탭·썸네일·틴트 칸 추가), 전역 `ActiveKey`·`ApplyPreset` → 구역 단위 `ApplyToZone(zone, key)`, 구역별 적용 상태 |
| `RootDesk/MyDesk/RtsZoneLogic.mlua` | modified — 구역 하나의 그리드 텍스처·틴트(`SetZoneGrid`), 구역 하나의 장식(`SetZoneDecor`). 8구역 일괄 `SetDecor`·`SetGridRUID`는 이 둘을 도는 형태로 |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | modified — 구역 사각형만 다시 칠하는 `FillZoneTiles(zone, tile, variants, ratio)`, 입장 때 프로필 불러오기 → 구역 테마 적용 → 전달, 나갈 때 구역 기본 복귀, 플레이어 목록 줄에 테마·아이콘 |
| `RootDesk/MyDesk/RtsMonsterComponent.mlua` | modified — `Die`에서 `_RtsProfileLogic:OnMonsterKilled(self.Zone, self.MonsterId)` |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified — 테마 상자(정보 카드 위), 정보 카드·목록 아래로, 유저 카드(키움·배경 썸네일·원형 아이콘·닉네임·내 카드 초록 테두리·[수정]), 공용 초상 `SpawnMonsterPortrait`, `CircleMaskRUID` |
| `RootDesk/MyDesk/RtsPopupLogic.mlua` | modified — kind `theme`(탭 '기본' + 5종 카드) · `themeconfirm`(예/아니오) · `icon`(탭 '기본' + 247 격자) · `iconinfo`(획득 여부·획득처·확률·획득일 + [이 아이콘 사용]) · `iconconfirm`(예/아니오) · `iconget`(획득 팝업) |
| `RootDesk/MyDesk/RtsMonsterInfoLogic.mlua` | modified — 초상 그리기를 `RtsHudLogic.SpawnMonsterPortrait`로(움직이는 그림 그대로) |
| `tools/gen-stage-table.py` | modified — 몬스터 행에 `icon`(걷기 클립 첫 프레임 스프라이트 GUID) |
| `RootDesk/MyDesk/RtsStageTableLogic.mlua` | modified(생성물) — 몬스터 행 `icon` 칸 |
| `assets/textures/circle-mask.png` · `assets/textures/README.md` | new / modified — 원형 마스크 등록 |
| `docs/theme-presets.md` | **new** — ChatGPT 인계: 테마 프리셋 구조·새 테마 추가 절차·임시 모양 목록·바꿔도 되는 곳/안 되는 곳 (draft 표시) |
| `docs/ui-screens.md` | modified — 테마 상자·유저 카드·팝업 6종 자리·크기·동작 |
| `AGENT.md` | modified — 인계 읽을 순서에 `docs/theme-presets.md` |
| `.beaver/output/roadmap/maple-augment-defense-roadmap.md` | modified — #38·#40·#41 in-progress |
| `RootDesk/MyDesk/RtsUnitSelectLogic.mlua` | unchanged — 월드 클릭(몬스터 정보)은 그대로 |

새 `.mlua`의 `.codeblock`은 Maker가 `maker_refresh_workspace` 때 만든다.

---

## Design

> 근거: 프리셋 표·전역 적용 `RtsThemeLogic.mlua:57-64,113-125` · 바닥 전체 칠하기 `RtsBootstrapLogic.mlua:63-102` · 입장·퇴장 `RtsBootstrapLogic.mlua:5-37` · 플레이어 목록 줄 `RtsBootstrapLogic.mlua:39-58` · 구역 그리드·장식 `RtsZoneLogic.mlua:269-297,313-351` · 구역 배정 `RtsZoneLogic.mlua:219-244` · 처치 `RtsMonsterComponent.mlua:392-408` · 난이도 `RtsDifficultyLogic.mlua:55` · 테스트 모드 `RtsUnitLogic.mlua:14` · 계정 저장 형제 `RtsUnitLogic.mlua:545-576`(GetAndWait·SetAndWait·실패 코드) · 그 유저에게만 보내기 `RtsCameraAnchorComponent.ApplyAssignedZone(zone, userId)` · 팝업 셸 `RtsPopupLogic.mlua:126`(Open) · 탭 `:297`(SpawnTab) · 예/아니오 `:535-`(OpenRestartConfirm·BuildRestart) · 정보 카드·목록 `RtsHudLogic.mlua:346,374` · 목록 행 `:872-1010`(RefreshPlayerList·AddPlayerRow·ApplyPlayerLook·OnPlayerRowClick) · 초상 `RtsMonsterInfoLogic.mlua:114-136`.

### 1. 테마 프리셋 — RtsThemeLogic

```text
프리셋 행(표 한 줄 = 테마 하나)
  key        henesys | ellinia | perion | kerning | lith   (저장 값·RPC 인자)
  name       헤네시스 | 엘리니아 | 페리온 | 커닝시티 | 리스항구
  tab        "기본"                (테마 창 탭 — 새 탭은 여기 이름만 새로 쓰면 창에 탭이 생김)
  floorTile  바닥 타일 이름(CaveFloorTileSet 안)   + floorVariants · variantRatio
  gridRUID   구역 트랙 판 텍스처   + gridTint(Color — 임시 모양용 색 입히기, 디자인 텍스처가 오면 흰색)
  decor      여백 장식 { ruid, col, row, scale } 목록
  thumb      썸네일 스프라이트 RUID(지금 "" → 칸 색 color로 대신 칠함)
  color      썸네일 없을 때 대신 쓰는 색(테마 창 카드·테마 상자·유저 카드 배경)

임시 모양(ChatGPT가 바꿀 자리)
  헤네시스  HenesysGrass1+2·3 12% · 95b3ec9d…(흰색) · 헤네시스 탑뷰 장식 23개   ← 지금과 같음
  엘리니아  HenesysGrassFloor     · 95b3ec9d…(청록 틴트) · 장식 없음
  페리온    HenesysSoil           · 95b3ec9d…(황토 틴트) · 장식 없음
  커닝시티  HenesysStone1         · 95b3ec9d…(회보라 틴트) · 장식 없음
  리스항구  ElnathSnowFloor       · 95b3ec9d…(하늘 틴트) · 장식 없음
  (elnath 프리셋은 표에서 뺀다 — 자산은 README에 '보관')

구역 단위 적용(서버)
  ZoneTheme[zone] = key                               ← 구역별 지금 테마(기본 henesys)
  ApplyToZone(zone, key)
    키 검사(없으면 false) → 같으면 아무것도 안 함
    RtsBootstrapLogic.FillZoneTiles(zone, floorTile, floorVariants, variantRatio)
    RtsZoneLogic.SetZoneGrid(zone, gridRUID, gridTint)
    RtsZoneLogic.SetZoneDecor(zone, decor)
    ZoneTheme[zone] = key
  GetZoneTheme(zone) · GetPreset(key) · GetPresets() · GetTabs()(탭 이름, 표 순서대로 중복 없이)
  없애는 것: ActiveKey · ApplyPreset · GetActiveKey · GetFloorTileName · GetFloorVariants · GetFloorVariantRatio · GetGridRUID · GetDecor
             (부르던 곳 RtsBootstrapLogic:74 · RtsZoneLogic:282,292 → 기본 프리셋 GetPreset("henesys")로)
```

### 2. 구역만 다시 칠하기 — RtsBootstrapLogic · RtsZoneLogic

```text
FillZoneTiles(zone, tile, variants, ratio)          (서버)
  구역 사각형(세계) = 구역 중심 ± (구역 폭 + 가로 여백)/2 , ± (구역 높이 + 세로 여백)/2
     RtsConfigLogic.GetZoneCenter(n) · ZoneWidth 42.66 · ZoneGapX 5.34 · ZoneHeight 24 · ZoneGapY 8
     맨 바깥 구역은 맵 테두리 여유(사방 16유닛, EnsureGroundTiles의 pad)까지 늘림
  → tilemap:ToCellPosition(왼아래) · ToCellPosition(오른위) → BoxFill(tile, from, to)
  → 변형 타일: 그 칸 범위만 기존 해시식((x+97)·374761393 + (y+89)·668265263)으로 SetTile
  EnsureGroundTiles(맵 전체 기본 칠하기)는 그대로 두되 기본 프리셋을 GetPreset("henesys")에서 읽음

SetZoneGrid(zone, ruid, tint)   ZoneGrid{zone}.SpriteRUID = ruid, Color = tint
SetZoneDecor(zone, list)         ZoneDecor{zone}_1..N 지우고 목록대로 다시(구역마다 개수 DecorCountByZone[zone])
SetDecor(list) / SetGridRUID(ruid) = 1..8구역에 위 둘을 돌림(EnsureZoneVisuals가 처음 세울 때)
```

### 3. 유저 프로필 — RtsProfileLogic (새 Logic)

```text
서버 상태(ServerOnly, 유저별)
  ThemeByUser[userId] = "henesys"
  IconByUser[userId]  = "M001"
  OwnedByUser[userId] = { ["M001"] = 0, ["M005"] = 1790000000000, … }   ← 값 = 획득 시각(UTC ms, M001은 0)

저장소(유저 DataStorage, 형제 RtsUnitLogic.LoadAvatarPass·ProcessPurchase와 같은 GetAndWait/SetAndWait·실패 코드 처리)
  "theme" = "perion"
  "icon"  = "M005"
  "icons" = "M005:1790000000000,M131:1790000123456"      ← M001은 적지 않아도 보유

Load(userId)                 입장 때 3칸 읽기 → 없거나 틀린 값은 기본(henesys·M001), 보유에 없는 아이콘이 선택돼 있으면 M001
SendProfile(theme, icon, owned, userId)   @ExecSpace("Client") — 마지막 인자 userId = 그 클라에만
   owned = "M001:0,M005:1790000000000,…"(보유 전체·획득 시각 포함) → 클라 MyTheme·MyIcon·MyOwned 갱신 → 열린 창 다시 그림
PushProfile(userId)          SendProfile(...) + RtsBootstrapLogic.BroadcastPlayerList()

RequestSetTheme(key)   @ExecSpace("Server")
   userId = senderUserId, zone = RtsZoneLogic.GetZoneOfUser(userId)  (0이면 거부)
   프리셋에 없는 키 → 로그만, 끝
   저장 SetAndWait("theme", key) 실패 → 로그만, 끝(메모리 그대로)
   ThemeByUser 갱신 → RtsThemeLogic.ApplyToZone(zone, key) → PushProfile
RequestSetIcon(monsterId)   @ExecSpace("Server")
   senderUserId 보유에 없으면 → 로그만, 끝
   저장 SetAndWait("icon", id) 실패 → 끝 / 성공 → IconByUser 갱신 → PushProfile

OnMonsterKilled(zone, monsterId)   ServerOnly — RtsMonsterComponent.Die에서
   userId = 그 구역 주인(RtsZoneLogic.ZoneByUser 역조회) 없으면 끝
   RtsUnitLogic.DevTools면 끝 · RtsDifficultyLogic.Of(userId) ≠ 5(매우어려움)면 끝 · 이미 보유면 끝
   RandomDouble() ≥ 0.01이면 끝
   now = DateTime.UtcNow.Elapsed → 보유에 추가 → SetAndWait("icons", 직렬화) 실패면 되돌리고 끝
   PushProfile(userId) + ShowIconGot(monsterId, userId)(그 클라: 획득 팝업)

입장·퇴장 연결(RtsBootstrapLogic.HandleUserEnterEvent / HandleUserLeaveEvent)
   입장: AssignZone → Load(userId) → ApplyToZone(zone, 테마) → ApplyAssignedZone … → PushProfile(목록 포함)
   퇴장: ApplyToZone(zone, "henesys")(빈 구역은 기본으로) → 프로필 메모리 지움
```

### 4. 플레이어 목록 줄 · 유저 카드 — RtsBootstrapLogic · RtsHudLogic

```text
줄 형식(RefreshPlayerList 서명 그대로 — 문자열 칸만 늘림)
  userId \t 닉 \t 구역 \t 생존 \t 테마키 \t 아이콘id        (칸이 모자라면 henesys·M001)

좌상단 배치(위 → 아래)
  테마 상자   RtsThemeBox   a(0,1) p(0,1) (16,-16)  440×64
              왼쪽 썸네일 104×48(thumb 없으면 color 칠) · "맵 테마"(작게, 흐리게) · 테마 이름(굵게) · 오른쪽 "변경 ›"
              누르면 _RtsPopupLogic:Open("theme")
  정보 카드   RtsInfoCard   (16,-88)  440×138   (내용 그대로, 자리만 아래로)
  유저 카드 목록 RtsPlayers  (16,-236)  280 폭, 카드 280×56 · 간격 6 · 머리 "n / 8"

유저 카드 한 장(AddPlayerRow 대체)
  배경      그 유저 테마 thumb(없으면 color) + 어두운 막(α0.35)으로 글자 읽히게
  왼쪽      지름 44 원형 칸(MaskComponent + CircleMaskRUID) 안에 아이콘 초상(멈춘 그림)
  오른쪽    닉네임(굵게 16, 길면 BestFit) — "(나)" 글자 없음
  내 카드   테두리 3px 초록(0.35,0.8,0.42) · 오른쪽 위 [수정] 44×22 → _RtsPopupLogic:Open("icon")
  보는 중   (내 카드가 아닐 때) 금색 테두리 1.5 — 지금 규칙 그대로
  탈락      카드 전체 흐리게(α0.45) + 아이콘 회색 + 작은 비석 표시
  클릭      카드 = 그 구역으로 카메라(OnPlayerRowClick 그대로), [수정]만 아이콘 창
```

### 5. 공용 초상 — RtsHudLogic.SpawnMonsterPortrait

```text
SpawnMonsterPortrait(parent, monsterId, size, animated) → 초상 엔티티
  칸 가운데에 몬스터 그림: animated = 걷기 클립(정보 창), 멈춤 = 표 icon(걷기 첫 프레임 스프라이트)
  크기·위치 = 지금 정보 창 식 그대로(RtsMonsterInfoLogic.mlua:119-135): 그림 테두리 = boxW/0.7·boxH/0.8,
     fit = min(칸/폭, 칸/높이, 2.5), NativeSize, LocalScale = fit, LocalPosition = −(boxX, boxY)×100×fit
     ※ RUID를 넣은 뒤에 크기·위치(표시 설정 되돌림 방지 — 정보 창 주석)
  쓰는 곳: 정보 창(animated) · 아이콘 격자 · 유저 카드 · 아이콘 정보 팝업 · 획득 팝업(멈춤)
생성기: 몬스터 행에 icon = clip_frames(walk)[0] 의 스프라이트 GUID (tools/gen-stage-table.py — 기존 clip_frames 재사용)

원형 마스크(build 첫 단계): assets/textures/circle-mask.png(128px 흰 원, 투명 배경, PPU 100)를 만들고
  사용자 확인 뒤 msw-mcp로 스프라이트 업로드 → RtsHudLogic.CircleMaskRUID. 업로드 전에는 네모 칸(지금 정보 창 초상 칸과 같음)으로 그린다
```

### 6. 팝업 — RtsPopupLogic

```text
theme        900×560 "맵 테마"   탭 줄 = GetTabs()(지금 '기본' 하나, SpawnTab) · 카드 5장(썸네일 200×120 + 이름 + '사용 중')
             사용 중이 아닌 카드 클릭 → PendingTheme = key → Open("themeconfirm")
themeconfirm 640×260 "맵 테마"   "맵 테마를 변경하시겠습니까?" + 고른 테마 이름 · [예] → RequestSetTheme(PendingTheme) · Close / [아니오] → Open("theme")
icon         900×820 "아이콘"    탭 줄(지금 '기본') · 머리 "보유 n / 247" · 격자(8열, 칸 88×88, 스크롤 — SpawnScrollList 형제)
             보유 = 원래 색, 미보유 = 검은 실루엣(Color 0,0,0,0.55) + 자물쇠, 사용 중 = 금 테두리
             칸 클릭 → PendingIcon = id → Open("iconinfo")
iconinfo     640×420 "아이콘"    큰 초상 120 · 이름 · 상태(사용 중 / 보유 · 획득일 YYYY-MM-DD / 미획득)
             "획득처: 매우어려움 · n라운드 지역 - 맵"(그 몬스터가 처음 나오는 스테이지 — RtsStageTableLogic.Stages 첫 등장)
             "확률: 처치 시 1% (매우어려움)"
             [이 아이콘 사용](보유·미사용일 때만) → Open("iconconfirm") / [닫기] → Open("icon")
iconconfirm  640×260 "아이콘"    "아이콘을 변경하시겠습니까?" · [예] → RequestSetIcon(PendingIcon) · Close / [아니오] → Open("iconinfo")
iconget      640×360 "새 아이콘 획득!" 초상 · 이름 · 획득처 · 획득일 · [확인] — ShowIconGot가 연다
             (다른 팝업이 열려 있으면 그 팝업을 닫고 연다 — 판 진행 중 3택1과 겹치면 3택1 우선: 대기열에 넣고 3택1 닫힐 때)
예/아니오 모양은 BuildRestart 형제(금 [예] + SpawnTab [아니오])
```

### 7. 디자인 인계 문서 — docs/theme-presets.md (새, draft 표시)

```text
1) 테마 = RtsThemeLogic.GetPresets 한 줄 — 칸 설명(key는 저장 값이라 바꾸지 않음)
2) 새 테마·새 탭 추가 절차: 바닥 타일(CaveFloorTileSet에 타일 추가 — 256px 무이음새, tools/gen-*-floor.js 참고)
   · 트랙 판(16×13, 칸 80px, 1280×1040, tools/gen-track-grid.js 색·재질 바꿔 생성 → 업로드 → gridRUID, gridTint는 흰색으로)
   · 장식(좌우 여백 칸 좌표만 — 트랙·발판 칸 금지, 오른쪽 18칸 이후 HUD 밑 주의) · 썸네일(권장 400×240, 테마 창·테마 상자·유저 카드 배경 공용)
3) 지금 임시 모양 목록(엘리니아·페리온·커닝시티·리스항구 = 기존 타일 + 틴트, 장식·썸네일 없음) — 교체 대상
4) 바꿔도 되는 곳: 프리셋 행의 floorTile·gridRUID·gridTint·decor·thumb·color·name·tab, Client 그리기 메서드
   바꾸면 안 되는 곳: key 값, RPC 서명(RequestSetTheme·RequestSetIcon·SendProfile·RefreshPlayerList), DataStorage 키(theme·icon·icons), 서버 메서드
5) 확인 절차: Maker Play → 테마 상자 → 테마 선택 → 예 → 내 구역만 바뀌는지 스크린샷
```

### 8. 삭제·정리 목록 (§1.7)

```text
RtsThemeLogic   ActiveKey · ApplyPreset · GetActiveKey · GetFloorTileName · GetFloorVariants · GetFloorVariantRatio · GetGridRUID · GetDecor · elnath 행
RtsHudLogic     목록 행의 초록 점(RtsPlayerDot) · "(나)" 리치 글자 · 221×32 행 크기 → 카드로 교체
RtsMonsterInfoLogic  초상 그리기 본문(:119-135) → SpawnMonsterPortrait 호출 한 줄
docs/ui-screens.md   3.2 좌측 플레이어 목록 표 → 유저 카드 표로 교체, 8장 #38·#40·#41 '미구현' 줄 갱신
```

---

## Test Cases
이 스택엔 CLI 테스트 러너가 없다(CLAUDE.md Testing) — 검증은 Maker Play(`maker_save → maker_play → maker_logs · maker_screenshot → maker_stop`)와 `maker_execute_script`(서버 `server_main`)로 한다. 계산형(입력→출력 고정) 유닛은 없음(획득은 난수, 저장 문자열 변환은 자르고 붙이기뿐).

```
[FAIL:validation] RequestSetTheme("nope") → 테마·타일·저장소 그대로, 로그 "unknown theme"
[FAIL:validation] RequestSetIcon("M200")(미보유) → 선택 그대로
[FAIL:validation] 남의 구역 — 서버에서 senderUserId가 아닌 구역은 바꿀 방법 없음(인자에 구역이 없음) 확인: RequestSetTheme 후 다른 구역 ZoneGrid·타일 그대로
[FAIL:validation] OnMonsterKilled — 난이도 보통·극악이면 1,000번 불러도 획득 0 / DevTools면 0 / 이미 보유면 0
[SUCCESS] 난이도 매우어려움에서 OnMonsterKilled를 서버 스크립트로 1,000번(같은 몬스터 id 여러 개) → 약 1%씩 획득, 획득 팝업, icons에 id:시각 저장
[SUCCESS] 테마 변경 → 내 구역 바닥·트랙 틴트만 바뀜(다른 구역 헤네시스 그대로) · 테마 상자·유저 카드 배경 갱신
[SUCCESS] Play를 끄고 다시 켜도(maker_reset_data_storage 안 함) 테마·선택 아이콘·보유 목록·획득일 유지 — 서버가 입장 때 보냄
[SUCCESS] 아이콘 창: 247칸, 보유 원색·미보유 실루엣, 칸 클릭 → 정보(획득처 라운드·맵·확률·획득일) → [이 아이콘 사용] → 예 → 내 카드 아이콘 바뀜
[SUCCESS] 정보 창 초상 — 공용 초상으로 옮긴 뒤에도 지금과 같은 자리·크기(초록버섯·보스 스크린샷 비교)

테스트 생략(위임형): FillZoneTiles 좌표 변환(엔진 ToCellPosition 그대로) · SendProfile/BroadcastPlayerList 전달 배선 — 위 SUCCESS 스크린샷으로 함께 확인
```

---

## Response Codes

| Code | Cause |
|------|------|
| 성공(테마) | 저장 → 내 구역 외형 적용 → SendProfile + 플레이어 목록 |
| 성공(아이콘) | 저장 → SendProfile + 플레이어 목록(카드 아이콘) |
| 획득 | 매우어려움·미보유·1% → 저장 → SendProfile + ShowIconGot(획득 팝업) |
| 무시: 구역 없음 | senderUserId 구역 0(입장 전·나간 뒤) |
| 무시: 모르는 테마 | 프리셋에 없는 키 |
| 무시: 미보유 아이콘 | 보유 목록에 없는 id |
| 무시: 저장 실패 | DataStorage 코드 ≠ 0 — 메모리 값 되돌림, 알림 없음 |
| 무시(획득 조건) | 테스트 모드 · 난이도 ≠ 매우어려움 · 이미 보유 · 난수 ≥ 1% · 구역 주인 없음 |

# Report — 맵 테마 프리셋 + 몬스터 아이콘 + 유저 카드

## Feature Summary
- **Feature**: 내 구역 외형 테마 5종(헤네시스 + 임시 모양 4종) · 몬스터 아이콘 247종 수집(매우어려움 처치 1%, 획득 일시 저장)·선택 · 좌측 유저 카드 · 디자인 인계 문서
- **Entry point**: `RtsProfileLogic.RequestSetTheme(key)` · `RequestSetIcon(id)` (Server, senderUserId) · `OnMonsterKilled(zone, id)` (ServerOnly ← `RtsMonsterComponent.Die`) · `SendProfile` / `ShowIconGot` (Client, 그 유저에게만) · `RtsHudLogic.RefreshPlayerList(packed)`(서명 그대로, 줄 끝 테마·아이콘)
- **Domain**: rts-custom

## Created/Modified/Deleted Files
| File | Change Type | Description |
|------|-----------|------|
| `RootDesk/MyDesk/RtsProfileLogic.mlua` | created | 유저별 테마·선택 아이콘·보유 아이콘(획득 시각) 서버 상태, DataStorage `theme`·`icon`·`icons` 읽기/쓰기(SetAsync, 실패 시 되돌림), 변경 RPC 2종, 처치 훅(매우어려움·미보유·1%), 구역 주인 캐시(`OwnerByZone`), 클라 수신·획득 팝업 대기열·획득처/획득일 |
| `RootDesk/MyDesk/RtsThemeLogic.mlua` | modified | 프리셋 5종(tab·gridTint·thumb·color 칸), `GetTabs`·`HasKey`·`GetZoneTheme`·`ApplyToZone`. 삭제: `ActiveKey`·`ApplyPreset`·`GetActiveKey`·`GetFloorTileName`·`GetFloorVariants`·`GetFloorVariantRatio`·`GetGridRUID`·`GetDecor`·`elnath` 행 |
| `RootDesk/MyDesk/RtsZoneLogic.mlua` | modified | `SetZoneDecor(zone, list)`·`SetZoneGrid(zone, ruid, tint)`, `DecorCountByZone`. 삭제: 8구역 일괄 `SetDecor`·`SetGridRUID`·`DecorCount` |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | modified | `FillZoneTiles`(구역 12×8 타일 + 바깥 여유)·`ScatterVariants`(공용), 입장 `RtsProfileLogic.OnUserEnter` · 퇴장 `OnUserLeave`, 목록 줄에 테마·아이콘 |
| `RootDesk/MyDesk/RtsMonsterComponent.mlua` | modified | `Die`에서 `_RtsProfileLogic:OnMonsterKilled` |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified | 테마 상자(`BuildThemeBox`·`RefreshThemeBox`·`PaintThumb`), 정보 카드 y −88·목록 y −236, 유저 카드(`AddPlayerCard` — 옛 `AddPlayerRow` 대체, 서명이 달라 새 이름), `ApplyPlayerLook` 새 모양, 공용 초상 `SpawnMonsterPortrait`, `CircleMaskRUID` |
| `RootDesk/MyDesk/RtsPopupLogic.mlua` | modified | kind `theme`·`themeconfirm`·`icon`(32칸 쪽 넘기기)·`iconinfo`·`iconconfirm`·`iconget`, 공용 `BuildConfirm`(다시하기 확인도 이것으로)·`BuildTabRow`, 창 닫힐 때 `FlushGot` |
| `RootDesk/MyDesk/RtsMonsterInfoLogic.mlua` | modified | 초상 → `SpawnMonsterPortrait(…, true)`. 삭제: `IconMaxFit` |
| `tools/gen-stage-table.py` · `RootDesk/MyDesk/RtsStageTableLogic.mlua` | modified | 몬스터 행 `icon`(크기 기준 걷기 프레임 스프라이트) — 246/247(B11 더스크는 그림 없음 → 초상이 걷기 클립으로 대신) |
| `assets/textures/circle-mask.png` · `assets/textures/README.md` | created / modified | 원형 마스크(미업로드), 테마 프리셋 절 갱신 |
| `docs/theme-presets.md` | created | ChatGPT 인계(프리셋 칸·임시 모양·새 테마 절차·바꾸면 안 되는 것) — draft 표시 |
| `docs/ui-screens.md` · `AGENT.md` | modified | 테마 상자 3.0 · 유저 카드 3.2 · 팝업 6종 4.2 · 8장 #38·#40·#41 · AGENT 읽기 순서 |

## Tests Written
이 스택엔 CLI 테스트 러너가 없다(CLAUDE.md Testing) — plan의 Test Cases를 Maker Play + `maker_execute_script`로 확인(아래 Verification).

## Verification
Maker(2026-09-25): 빌드 로그 오류 0(경고는 기존 것 + `ParseOwned` 다중 반환 경고뿐), 실행 로그 오류 0.
- [SUCCESS] HUD — 테마 상자(헤네시스 썸네일 색·이름·변경 ›) · 정보 카드 아래로 · 유저 카드(초록달팽이 아이콘·닉네임·[수정]·초록 테두리)
- [SUCCESS] 테마 창(탭 '기본' + 5종 카드, '사용 중') → 확인 창 → 예 → **구역 1만** 페리온 임시 모양(HenesysSoil + 황토 틴트, 장식 없음), F2 구역은 헤네시스 그대로 · 테마 상자·카드 배경 갱신
- [SUCCESS] `GrantIcon` → 획득 팝업(뿔버섯, 획득처 "매우어려움 · 5라운드 · 빅토리아 - 개미굴", 획득일 2026-09-25) · 아이콘 창(32칸, 1/8, 보유 원색·미보유 실루엣·사용 중 금색) · 정보 → [이 아이콘 사용] → 확인 → 카드 아이콘 뿔버섯
- [FAIL:validation] `RequestSetTheme("nope")` → "unknown theme" 거부 · `RequestSetIcon("M200")`(미보유) → "not owned" 거부
- [FAIL:validation] 처치 훅 — 보통 300회·극악 300회 획득 0, 매우어려움 600회 중 약 1%씩 획득(저장 → 전달 → 팝업)
- [SUCCESS] Play 재시작 뒤 서버가 불러옴: 테마 perion·아이콘 M010·보유 15 → 구역 1 페리온 다시 적용, 카드 아이콘 유지
- [SUCCESS] 몬스터 정보 창 초상(돼지) — 공용 초상으로 바꾼 뒤에도 칸 가운데
- 참고: `maker_execute_script`에서 다른 스크립트 메서드 300회 호출이 0.5초(실행기 비용) — 처치 훅 자체 비용 아님

## Remaining Issues
- (해결 2026-09-25) 원형 마스크 업로드 `RtsCircleMask` 69e2dced… → `CircleMaskRUID` — 카드 아이콘 원형 확인
- 헤네시스 외 4종 테마는 임시 모양(기존 타일 + 틴트, 장식·썸네일 없음) — 디자인은 ChatGPT(`docs/theme-presets.md`)
- Maker 로컬 DataStorage에 시험으로 준 아이콘 14개·테마 perion이 남아 있다(Maker 전용 — 출시 월드와 무관, 필요하면 `maker_reset_data_storage`)

## Change - 260925-1
- **Change summary**: 아이콘 창 쪽 넘기기 → 스크롤 격자(사용자 "페이징 말고 스크롤"), 맵 테마 창 고정 3열 → 스크롤 격자(사용자 "여러 개 생길 수도")
- **Changed files**: `RtsPopupLogic.mlua`(`SpawnScrollGrid` 공용 · `SpawnIconCell` · `IconBatch` 나눠 채우기, 삭제: `IconPage`·`IconPerPage`·이전/다음 버튼) · `docs/ui-screens.md`
- **Verification**: Maker 빌드 로그 오류 0, 아이콘 창 스크롤 막대 + 위에서부터 칸 채움 확인(사용자가 Maker에서 플레이 중이라 추가 확인은 중단)
- **Remaining issues**: 테마 창 스크롤은 화면 확인 전(테마 5종이라 한 화면에 다 들어감)

## Change - 260925-2
- **Change summary**: 맵 테마 창 — 격자 스크롤이 설정을 늦게 받아 카드가 100px 간격으로 겹침(사용자 화면) → 세로 스크롤 + 줄마다 정사각형 카드 3장, 한 화면에 2줄(사용자 "맵별로 정사각형, 가로 3개 2줄, 스크롤"). 창 900×730. 목록 위 문구에서 "보이는 것만 달라지고 밸런스는 그대로"·"매우어려움에서 … 1% 확률로 획득" 삭제(사용자 "목록에 있을 내용이 아니다" — 획득 조건·확률은 아이콘 정보 창에만). 아이콘 격자는 설정을 0.05초 뒤 한 번 더 넣음
- **Changed files**: `RtsPopupLogic.mlua`(`BuildTheme` 세로 목록 `RtsThemeList` + 줄 `RtsThemeRow{n}` 830×270 + 카드 270×270·썸네일 250×200, `theme` 높이 730, `SpawnScrollGrid` 설정 다시 넣기, 문구 2곳) · `docs/ui-screens.md` · `docs/theme-presets.md`
- **Verification**: Maker 빌드 로그 오류 0, 테마 창 3장 × 2줄 한 화면·'사용 중' 금색 테두리 확인. Play 시작 직후(약 5초) 스크립트로 연 한 번은 창 안이 비었고(목록 부모 nil 경고), 닫고 다시 열면 정상 — 재현 안 됨
- **Remaining issues**: 위 빈 창 1회(Play 직후 스크립트로 연 경우) — 다시 나오면 원인 조사

## Change - 260925-3 (프로필 설정 — 테마·비석 탭, 비석 프리셋, 기본값)
- **Change summary**: 사용자 2026-09-25 "비석도 프리셋, 좌상단 맵 테마 창을 프로필 설정으로, 탭 테마/비석, 기본값 아이콘 없음·테마 헤네시스·비석 기본, 설정값이 없으면 게임 시작 시 자동 설정", "테마·비석·아이콘 모두 영구 소유 — 선택 정보랑 보유 정보 서버 저장". revision: `.beaver/output/revision/rts-custom/theme-icon-preset-revision-260925-1.md`
- **Changed files**: `RtsTombLogic`(새 — 비석 프리셋 1종 basic, w·h·free) · `RtsProfileLogic`(tomb·themes·tombs 키, FreeIcon M001 · IconNone "none", 입장 때 빈 선택 키 기본값 저장(읽기 성공일 때만), `PresetOwned`, `RequestSetTomb`, `SendProfileState` — 옛 `SendProfile` 삭제) · `RtsThemeLogic`(프리셋 free = true) · `RtsRunResultLogic.SpawnTomb`(주인 비석 — TombRUID·TombScale 삭제) · `RtsHudLogic`(프로필 상자 `BuildProfileBox`·`RefreshProfileBox` — 옛 테마 상자 삭제, 카드 아이콘 없음) · `RtsPopupLogic`(kind `profile`·`tombconfirm`, `SpawnPresetList·Row·Card` 공용, `BuildTabRowAt`, 아이콘 '없음' 칸) · docs(ui-screens·theme-presets 6절)
- **Verification**(Maker 2026-09-25): 빌드 오류 0 · 프로필 상자 "프로필 설정 / 테마 커닝시티 · 비석 기본 비석" · 프로필 창 [비석] 탭(기본 비석 '사용 중') · 아이콘 창 첫 칸 '없음' · 비석 그림이 칸을 넘쳐 이름을 덮음 → 원본 w·h 비율로 250×190 안에 맞춤(재시작 뒤 사용자 확인 중)
- **Remaining issues**: 기본값 저장은 `maker_reset_data_storage` 뒤 입장 로그("RtsProfile: default …")로 확인 전 · 빈 키를 읽을 때 엔진이 코드 0 + 빈 값을 주는지(아니면 기본값 저장이 안 됨) 실측 필요

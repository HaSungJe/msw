# 코드베이스 교통정리 계획

- 요청: 2026-09-28 사용자 "프로젝트 코드베이스 확인하고 불필요한 부분들 제거하고, 통합할 부분은 통합해서 교통정리좀하자"
- 상태: **완료(2026-09-28, 커밋 전)** — 아래 '결과'. 처음엔 사용자 결정 "모바일 작업 끝날 때까지 전부 대기". 모바일 보드 표시 작업(RtsBoardViewLogic·UI/RtsUiLayoutLogic 신규, 전투·유닛·팝업·HUD 등 15개 파일 수정)이 커밋된 뒤 시작한다.
- 시작 전: 이 문서의 줄 번호는 2026-09-28 분석 시점 기준이라 모바일 커밋 뒤 달라진다. 항목마다 이름으로 다시 찾고, 모바일 작업이 새로 쓰기 시작한 것은 없는지 호출처를 다시 확인한 뒤 지운다(`deadscan` 방식: 메서드·속성 이름을 주석 제외 전체 .mlua + .ui/.map/.model에서 검색).
- 검증: 단계마다 Maker stop → refresh → save → build 로그(에러 0, 기존 경고 외 새 경고 없음) → Play → 전투·영입·증강·상세창·보스 한 판 확인. 데미지 공식 통합은 BossDps가 전과 같은 값을 내는지 11직업 × 프리즘 유무로 대조(balance-calc rotation_dps 0.3% 안 유지).

## 사용자 결정 (2026-09-28)

| 항목 | 결정 |
|---|---|
| 진행 순서 | 모바일 작업 커밋 뒤 한 번에 |
| 랭킹 팝업(여는 곳 없음, 약 150줄, Phase 13 예정) | **유지** |
| 안 쓰는 스킬 연출 기능(플립북·다중 모션·다중 투사체 등, FxOverrides 실험용) | **유지** |
| 아바타 대체 외형(HasMageSkin 전 직업 true — GetCostume 약 57줄 + 대체 분기) | **삭제** |
| 보스 전용 최종 데미지 finBoss(늘 fin과 같음) | **삭제** |
| 데미지 공식 한 곳으로(전투·상세창 BossDps) | **진행** — 결과값 동일 유지 |
| 직업별 조회 if문 12벌 → 직업 표 하나 | **진행** |
| 영입 가능 판정 5벌 통일(규칙이 서로 다름) | 이번엔 안 함 |
| 큰 파일(탈락·이전 시안, 외부 참고 영상, 중복 zip, 안 쓰는 텍스처 ≈ 55MB) | **삭제** |

## 0. 먼저 할 것
- `.gitignore`에 `*.private.json` 추가 — `.beaver/output/hero-motion/upload-requests.private.json`(서명 업로드 주소)이 규칙 없이 untracked라 `git add -A` 한 번에 커밋될 수 있다. hero-motion 폴더를 지우기 전에 이 파일은 밖으로 옮긴다(커밋 금지).
- **버그**: `RtsCombatLogic.StopLoop`가 `ReadyAt`(key userId_no_idx)·`BusyUntil`·`FaceLockUntil`·`Focus`(key userId_no)를 지우지 않는다 → 같은 번호로 새 유닛을 들이면 이전 유닛의 같은 순번 스킬 남은 쿨이 이어진다(게임 시계는 판을 넘어 계속 흐름). StopLoop는 유닛 제거 때만 불리므로(SpawnUnit 교체·해고·ClearUnits·RemoveUnits·StartLoop 엔티티 없음) 여기서 비워도 이동으로 쿨 초기화 악용은 없다.

## 1. 안 쓰는 코드 삭제 (동작 변화 없음)

### 데이터·설정
- RtsAugmentLogic: `FoldPick`·`ExpandPick`(HUD 펼치기 버튼 삭제됨), 증강 `d.stack` 분기(core_ign 삭제됨)
- RtsAugmentTableLogic: `Totals`, `ApplyToStat`(모든 호출은 RtsUnitBuffLogic 쪽), `d.ign` 분기(방무 증강 삭제 — 주석도 곱연산이라 틀림), `RollShared`의 `shareOf`(늘 nil), 스탯 증강 `w = 1`(StatChoices로 고르므로 가중치 안 씀), `Roll`로 프리즘 남았는지 확인하는 곳(RtsAugmentLogic)은 난수 소모 없는 확인 함수로
- RtsConfigLogic: `GetZoneWidth`·`GetZoneHeight`·`GetCameraViewWidth`·`GetCameraViewHeight`·`GetMapLeftBottom`·`GetMapRightTop`, 속성 `CameraViewWidth`·`CameraViewHeight`·`CellSize`
- RtsJobTableLogic: `GetCumCost`, `IsWallLevel`, `GetTargetSkillLevel`(RtsUnitLogic.TargetSkillLevelFor가 대체), `Calc`(모두 CalcStat 사용), `PrismLockLevel`(늘 1), 도달 못 하는 대체값("(미정)" 스킬·일반 능력치), ApplyPrismStat의 빈 truesnipe·transcend 분기
- **finBoss 삭제(사용자 결정)**: GetStatRaw의 finBoss, 증강·버프의 finBoss 곱, 읽는 곳(RtsCombatLogic 보스 배율, JobTable BossDps, RtsUnitPopupLogic 표시) 약 28줄. 스킬 `bossFinal`·`shred` 필드도 쓰는 스킬이 없음(RtsCombatLogic·RtsMonsterComponent ApplyShred/ShredNow 포함) — 같이 정리
- **아바타 대체 외형 삭제(사용자 결정)**: `HasMageSkin`(전 직업 true)와 분기 — RtsUnitLogic 스폰, RtsUnitComponent.ApplyLook, RtsSkillFxLogic 2곳, RtsUnitPopupLogic 미리보기, JobTable `GetCostume`(약 57줄)
- RtsUnitBuffLogic: 범위 "near"(쓰는 버프 없음) — InScope 분기·ScopeText·RtsZoneLogic.CellDistance
- 몬스터 `icon` 필드(생성 표 246개)와 RtsHudLogic 대체 — 모든 몬스터에 썸네일이 있음 → **생성기(tools/gen-stage-table.py)에서** 빼기

### 전투·유닛
- RtsMonsterComponent: `PlayHitFx`(PlayHitFxAt만 사용), `PlayHitFxAt`의 안 쓰는 `crit` 인자(HitFx RPC 시그니처 — Maker 빌드 검사기 캐시 주의 메모 있음, 바꾸면 refresh 후 확인)
- RtsSkillFxLogic: `DemoLoop`·`PlayBasic`·속성 `DemoTimers`
- RtsUnitComponent: `IsFacingRight`(RtsSkillFxLogic.FacingRight가 대체)
- RtsUnitLogic: `GetCooldownSec`, `SetPermaLock`(SyncPrismLocks가 대체 — JobTable 주석의 이름도 갱신)
- RtsZoneLogic: `IsRoadCell`·`GetSpawnT`·`GetSpawnPoint`·`GetEndPoint`·`GetPlacementSlotCount`·`GetPlacementSlot`
- 걷는 보스 코드(보스는 Paused로 두고 풀지 않음): RtsTrackWalkerComponent의 BossMode 분기·`Reached`·`UnitsPerSec`, RtsBossLogic `OnBossReachedEnd`·YOffset 쓰기·중복 `Loop=false`
- RtsUnitAttackComponent `Hits`(늘 1) — 속성 삭제, GetDisplayHitCount는 1 반환(엔진 오버라이드 5개는 유지 — 실제 타격 경로)
- `IsBossRound(zone)`의 안 쓰는 zone 인자, `NearestTargetableAt`의 늘 같은 r

### 화면 (모바일 개편으로 가려진 것 포함 — 모바일 커밋 뒤 다시 확인)
- RtsHudLogic: `SetPlayerAlive`, 배속 스위치(SpeedBox 늘 꺼짐 — 배속 선택은 UI/RtsUiLayoutLogic MobileSpeeds·설정 페이지로 대체: BuildHud 스위치 부분·RefreshSpeedUi·SpeedKnob/Side/Shown/Track, RtsStageLogic의 RefreshSpeedUi 호출), 옛 영입·증강 버튼 꾸밈(Layout이 RtsLegacyHudState 아래로 숨김 — AugLabel·AugNotice·AugShown·RefreshAugEntry·RecruitFlash 등, 단 RecruitText.Text·PendingShown은 Layout이 읽으므로 유지 여부 확인), `RestartConfirmUntil` 확인 모드(늘 0), `PendingUnits`, `SetPendingOffers`의 visible 인자
- RtsMonsterInfoLogic: `IconSize`, "1%p" 하드코딩 → `ArmorBreakPer`
- RtsPopupLogic: `SpawnScrollGrid`, 속성 `Dim`·`AugTabs`·`AugBar`·`_T.AugList`, 기본색을 다시 칠하는 분기(BuildAugContent·RestyleAugRows), 모바일 닫기 버튼 중복(Open ↔ RefreshMobilePopup)
- RtsUnitPopupLogic: `SpawnPreview`, `BondBtn`, `SpawnScrollList`의 안 쓰는 rows(호출처의 줄 세기까지), BuildTargetRow의 rx·sy, BuildLockToggle의 total, BuildSkillTab 중복 줄
- RtsUnitSelectLogic: `IsPlaceMode`, 증강 창 Tab 키 분기(증강 등급 탭 없음)
- RtsRunResultLogic: 이용자에게 보이는 힌트 "재시작 버튼은 오른쪽 아래" 문구 확인(버튼이 상단으로 이동)
- **랭킹 팝업은 유지(사용자 결정)** — BuildRank·SetRanking·RequestRanking 등 그대로

## 2. 중복 통합

### 동작 변화 없음
- 키캡 그리기 6곳(RtsUnitSelectLogic.SpawnKeyCap·RtsPopupLogic.SpawnTabKeyHint·팝업·상세창·HUD·Layout.ActionKey) → `RtsHudLogic.SpawnKeyCap` 하나
- 금색 버튼(패널+글자+클릭) 약 11곳, 탭 재배치 5곳 → RtsPopupLogic `SpawnButton(style)`, BuildDismiss → 빨간 스타일
- 세로 스크롤 설정 4곳 → `RtsHudLogic.AddVScroll`
- 0.12초 늦은 삭제 4벌 → `SwapContent` 하나
- 선분·삼각형 채우기(오각형 레이더 ↔ 상세창 능력치 도형) → RtsHudLogic 공용. Layout.Icon의 두 인자 `math.atan`은 쓰지 말라는 주석이 있으니 같이 교체
- 글자 줄 수 추정 5벌 → `RtsHudLogic.TextLines`
- HUD 버튼 색 세트 약 10곳 → `RtsHudLogic.PaintButton(state)`, 팝업 `Ink`/`Muted` → HUD `ColInk`/`ColMuted` 호출(다크 모드 값과 같아야 함), 금색 위 글자색 6곳 상수화
- 증강 합계 → 문구 6벌(표기가 이미 어긋남: "보스 데미지" / "보스 공격 시 데미지") → `RtsAugmentTableLogic:StatLines`
- 증강 효과 적용 `ApplyToStat`·문구 `EffectText`(증강표 ↔ 버프) → `ApplyMods`·`ModText` 하나
- 등급 표(이름·RUID) 2벌, 탭 색 계산 2벌, 수동 탭 2곳 → SpawnTabBar, 상세창 CycleTab → `BarNext`
- 칸 설치 표시 루프 2벌(BeginMove·BeginPlace)
- 조준점(위치 + 충돌 오프셋 × 배율) 8곳(RtsCombatLogic·RtsMonsterComponent·RtsSkillFxLogic) → `RtsBoardViewLogic:AimPoint`
- 칸 거리(체비쇼프) 4곳 → `CellDist` 하나
- 보드 경로 문자열 `/maps/RtsMap/RtsBoard/` 약 9곳 → 상수/함수 하나
- 유닛 발 높이 0.75 3곳 → `UnitFootDy` 하나, SpawnUnit이 PlaceAt 사용
- 유닛 찾기 `RtsUnitBuffLogic.UnitAt` ↔ `RtsUnitLogic.GetZoneUnit`(ClientOnly만 풀면 같음)
- `ClearUnits` ↔ `RemoveUnits` 루프, 보스 `ClearAll` → `ClearZone` 반복
- RtsStageLogic 방 인원 세기 6번 → `RoomUserCount`
- 구역 번호 → 칸(RtsConfigLogic ↔ RtsBootstrapLogic), 구역 수(RtsCameraAnchorComponent → GetZoneCount), 타일 수·여백 계산 3번·타일맵 경로 3번(Bootstrap)
- 방어 깎기 캐시·스캔(GuardCrush ↔ ArmorBreak)과 클라 사본(RtsMonsterInfoLogic의 팔라딘 10/40 기준) → `GuardCrushFor(u)`
- 증강 개수 상한(ArmorBreakCap) 3곳 → `CappedAugCount(u)`
- 쉼표 목록(Prisms/Augs) 루프 약 9곳 → `PrismIds`/공용 split
- 한 번 재생 클립(생성·렌더러·마지막 프레임 삭제·대비 타이머) 약 8곳 → `SpawnOneShot` (연출 확인 필요)
- 스프라이트 크기 캐시 중복(SpawnProjectileEx 두 번)
- 적중 적용 3벌(일반·쉐도우 파트너·지대 틱) → `ApplyHit` — 파트너가 mobMul/빙결/shred/vuln을 건너뛰는 것, 지대가 3×3 재시도를 건너뛰는 것이 의도인지 확인 후
- Themes/RtsActionThemeLogic: 배경 RUID·"zakum_altar"·1672/941을 프리셋에서 읽기
- 프리셋 공통 메서드(RtsThemeLogic ↔ RtsTombLogic의 GetTabs·HasKey·GetPreset)
- 프로필 `PackOwned`/`ParseOwned` → `PackIcons`/`ParseIcons`로 이름만(증강 것과 형식이 달라 합치지 않음)

### 구조 개편 (사용자 결정 — 결과값은 그대로)
- **데미지 공식 한 곳으로**: 1타 공식 `floor(atk*pct*ratio*fin+0.0001)`(RtsCombatLogic 3곳 · JobTable BossDps 3곳), 보스 배율(bossBase + bossRatio), 스킬 순서(쿨 스킬 뒤에서부터 → 기본) → RtsJobTableLogic `PerHit`·`BossMul`·`SkillOrder`. finBoss 삭제와 같이
- **직업별 조회 표 하나로**: GetJobName·GetSeries·GetBaseAttack·GetAttackPerLevel·GetBaseSpeed·GetWeaponType·TierOf·GetJobFaction·MageSkin/Portrait 3개·GetRadar 고정표 → 직업 id를 키로 한 JOBS 표. HasMageSkin·GetCostume는 삭제(위)
- 레벨 비용 블록(JobTable)이 생성기 LEVEL_COST_BLOCKS와 중복 → 생성기가 생성 구역에 내보내게(생성 구역은 손으로 고치지 않는다)

## 3. 주석 정리
- 이력 주석은 남기되 **지금 코드와 다른 설명**을 고친다: JobTable 도트 퍼니셔(속도·비율), 초월(옛 값 사슬), finBoss 규칙, "target=true는 나중에", 떨어진 TierOf 주석, 고아 주석(GetTargetSkillLevel 설명), 반복 문구
- JobTable 2천 자 한 줄(연출 필드 설명) → docs로 옮기고 한 줄 링크
- 화면 파일 머리말·크기 주석(팝업 높이 730↔780, 상세창 960↔780, 카드 3장↔4장, 증강 등급 탭, HUD 숨긴 버튼 등), RtsUnitPopupLogic 머리말의 `Calc`

## 4. 도구
- 삭제(실행하면 IndexError — .info/balance-detail.md 표 구조 변경): `tools/route-sim.py`, `tools/combo-check.py`, `tools/difficulty-sim.py`
- 삭제(대체됨): `tools/balance-table.py`
- 삭제(결과물 보관·폐기): `tools/gen-cave-floor.js`, `tools/gen-hud-frame.js`. `gen-snow-floor.js`는 엘나스 프리셋이 빠졌으니 삭제하고 docs/theme-presets.md 예시 줄 갱신. `gen-henesys-floor.js`는 유지하되 assets/textures/README의 "적용 중" 줄 확인(실제는 HenesysGrass1/2/3 사용)
- 삭제(개인 경로·클라이언트명 하드코딩, .beaver/output/hero-motion/maker-call.py와 중복): `tools/maker-mcp-call.py`
- 기준 도구: balance-calc·clear-sim·gen-stage-table(+ hp-model-anchors.json, mob-visual.json). 메모리(balance.md)의 difficulty-sim·balance-table 언급 갱신
- 로컬 `tools/__pycache__/` 삭제

## 5. 저장소·문서
- 추적 해제: `.mswai/lock.json`·`.mswai/logs/cli.jsonl`(폴더 규칙 `*`인데 추적 중 — 커밋마다 변경분). 메모리의 "cli.jsonl 커밋" 규칙도 같이 갱신
- `.beaver/output`의 옛 .mlua 사본 삭제(검색·LSP 오염): job-table-before-connect.mlua, dark-knight-buster/before/RtsJobTableLogic.mlua, *.before.mlua 4개
- 폐기 로드맵 삭제: roadmap/wall-survival-roadmap.md(SUPERSEDED), pivot-luck-defense.md
- **큰 파일 삭제(사용자 결정)**: 탈락·이전 시안(phantom-joker-throw/rejected-rotation, phantom-joker-video/rejected-small-gesture, five-class-idle/previous, five-class-design/previous-concepts, phantom-joker-refine/previous, bishop-standard/*-before.png ≈ 26MB), phantom-joker-video/reference.mp4(13MB 외부 영상), assets/promo/promo-screenshots.zip(screenshots/와 같은 6장, 9.8MB), assets/textures의 crusher/ v1~v3·thumb-*(보관)·cave-*·world-avatar*
- 완료된 작업의 `normalized/` 프레임(assets/design/characters/*/frames/와 바이트 동일 118개), 문서에서 참조 없는 hero-motion/(→ .private.json 먼저 옮김)·bowmaster-concept/
- 문서: docs/theme-presets.md ↔ docs/design/theme-presets.md 합치기, 디자인 문서 7곳에 복사된 "현재 적용(2026-09-27)" 줄 → docs/unit-art.md 한 곳, five-class-concepts.md(검토본)·unit-motion.md(스스로 옛 기록이라 밝힘) 정리, docs/ui-screens.md의 월드 아바타 패스 "완료" 줄(09-25 삭제된 기능)
- 깨진 참조: balance.md의 augment-prism-spec.md, assets/design/README(없는 260925-world-thumbnail, 빠진 characters·ui·effects), assets/textures/README의 빈 보관 폴더 경로, archive/design-cleanup-260925 README(하위 폴더 7개가 비어 있음)
- 유지: `.claude/skills` ↔ `.agents/skills`(Claude·Codex 둘 다 사용), assets/theme-concepts(문서가 링크), promo mp4, dotorb 프레임, 타일셋의 안 쓰는 타일 6개(Maker에서만 — 인덱스로 칠해졌을 수 있음)
- git 기록 크기(≈370MB)는 파일을 지워도 줄지 않는다 — 이력 재작성은 하지 않는다

## 결과 (2026-09-28)

- 코드 29개 파일 −2,008 / +1,019줄(게임 코드 .mlua 합계 약 18,000줄). 저장소 파일 약 280개 삭제(≈55MB), 도구 8개 삭제.
- 검증: Maker build 에러 0(경고 12개 = 정리 전과 같은 종류). Play에서 웨이브가 끝까지 돌고 영입·영입 상세(오각형)·증강 뽑기·도감·프로필 창을 열어 오류 0.
  상세창 보스 DPS는 정리 전 BossDps 코드를 그대로 Maker에서 같이 돌려 11직업 × 프리즘 유무 22경우 **차이 0**, tools/balance-calc.py rotation_dps와 0.5% 안(프리즘 잠금 반영).
  직업 정의 표(JobDefs) 조회값 11직업 전부 정리 전 getter와 같음(원화 RUID 250개·시간표 35개 기계 대조).
- 유닛을 쓰는 전투·스킬 연출·상세창은 시험 스폰 금지라 Maker에서 돌리지 못했다 — 사용자 플레이 확인 필요.
- 의도한 동작 변화: ① 쿨타임 기록 미삭제 버그 수정(RtsCombatLogic.StopLoop) ② 원화 유닛이 돌아설 때 쉐도우 파트너 그림자·루프 클립이 따라 뒤집히게(RtsUnitComponent.ApplyFace — 아바타가 없어 일찍 끝나던 것) ③ 상세창 '증강으로 오른 수치'의 "보스 데미지" → "보스 공격 시 데미지"(StatLines로 통일) ④ 게임 끝 안내 "다시하기는 오른쪽 아래" → "왼쪽 아래"(실제 위치).
- 계획과 다르게 한 것: 방어율 감소(shred) 장치는 유지(코드에 '일부러 남겨 둠', 몬스터 정보 창 디버프까지 연결 — 대비 코드 결정 목록에 없음). docs/theme-presets.md ↔ docs/design/theme-presets.md는 합치지 않음(절차 문서와 ChatGPT 디자인 가이드라인 — design-handoff 규칙상 따로). 디자인 문서 7곳의 상태 줄 중복은 캐릭터 원화 작업 문서라 손대지 않음.
  하지 않은 것: 레벨 비용 블록 생성기 이전(생성 구역 변경 위험), 몬스터 icon 필드 생성기 삭제(효과 작음), 적중 적용 3벌 통합(쉐도우 파트너·지대의 차이가 의도일 수 있음), PlayHitFxAt의 안 쓰는 crit 인자(RPC 시그니처 캐시), 증강·버프 EffectText 통합(형식이 다름), Layout.ActionKey 키캡(모양이 다름).
- 새 공용 함수: RtsJobTableLogic JobDefs·JobDef·PerHit·SkillBossRatio·BossMul·SkillOrder·CappedAugCount / RtsAugmentTableLogic StatLines·HasAny / RtsThemeLogic TabsOf·FindPreset / RtsConfigLogic ZoneColRow / RtsBootstrapLogic GroundTilemap·GroundBounds /
  RtsBoardViewLogic BoardChild·AimPoint / RtsZoneLogic CellDistance(세계 좌표 ÷ 칸) / RtsUnitLogic UnitFootDy·UnitFootPos·GetZoneUnit(양쪽) / RtsSkillFxLogic SpawnOneShot·ProjectileSprite /
  RtsHudLogic SpawnKeyCap·SpawnButtonKeyCap·AddVScroll·PaintButton·Atan2·SetSegment·SetRightTri·SplitTri·TextLines·TextLinesRough·ColGoldInk / RtsPopupLogic SpawnButton·TabColors·GradeIcon / RtsUnitSelectLogic SpawnPadMarkers.
- 원래 있던 사소한 표시 문제(이번에 생긴 것 아님): 영입 상세 스킬 목록 오른쪽 위 [Tab] 키캡이 목록에 반쯤 가린다.

# Revision — 구역 시스템(트랙·보스 영역) — 260925-1

> 원 plan/report: `.beaver/output/plan/rts-base/zone-system-plan.md` · `.beaver/output/report/rts-base/zone-system-report.md`(보스 쪽은 `rts-stage/stage-wave-boss-*`). 원 문서는 고치지 않고 참고만 한다.
> 메모리 workflow "로드맵·플랜은 코드가 아니라 방향·동작 설명으로" — 아래 Code Changes는 mlua 코드 대신 파일별로 무엇을 어떻게 바꾸는지 적는다.
> 로드맵: 맞는 페이즈 없음(Phase 1 #4 구역 시스템 · Phase 7 #27 보스는 done) — 출시 뒤 개편.

## Reason for Change Request
사용자 2026-09-25: "보스영역도 바꿔야겠어. 맵의 가운데쪽에 보스영역 타일 4개 만들고, 거기로 보스가 오도록. 그에 맞게 트랙이나 배치 가능한 타일도 조정" — 후보 비교 뒤 **M2안**(불규칙한 길 + 트랙 매듭 3개: 둘은 붙고 하나는 멀리 — "전사가 효율을 내는 구간", "너무 정직해 … 좀 난잡한 형태")으로 확정.
같은 흐름에서 "S 자리에는 화살표, E에는 되돌리기 아이콘, E→S로 돌아간다는 표식 제거".

## Spec Before → After

| Item | Before | After |
|------|--------|-------|
| 보스 영역 | 8~11열 × 9~13행(4×5칸, 아래 가운데 — 2026-09-23) | **8~9열 × 6~7행(2×2칸)**. 그리드가 13줄이라 정중앙이 없어 반 칸 위(화면 아래 가운데는 몬스터 정보창이 덮음). 붉은 반투명 판·배치 불가 규칙은 그대로 |
| 트랙 경로 | 꺾임점 17개, 66칸, 교차 2곳. S = 3열 6행, E = 3열 12행 | **M2**: 꺾임점 20개, **77칸**, 교차 4곳(6,4)(10,11)(12,11)(14,4). S = 15열 9행(왼쪽으로 출발), E = 11열 6행(보스 오른쪽 발판 한 칸 건너) |
| 매듭(전사 자리) | 없음 | 트랙이 발판 한 칸을 네 방향으로 한 바퀴 감는 매듭 3곳 — 둘레 8칸이 전부 트랙인 칸 **(9,10)·(13,12)**(붙은 두 개) · **(5,3)**(멀리 하나). 사거리 1 유닛이 몬스터를 두 번씩 만난다 |
| 보스 둘레 | 트랙이 보스 영역 위·옆으로만 | 트랙이 보스 네 면을 다 지나간다(4행·6열·9행·11열 쪽), 보스 둘레 한 겹(7~10열 × 5~8행)은 발판 |
| 발판 | 123칸(규칙: 그리드 안의 트랙·보스 영역이 아닌 칸 전부) | **130칸**(규칙 그대로). 옛 보스 영역 중 트랙이 아닌 칸은 이제 배치 가능 |
| 보스 크기 | 4×5 영역을 꽉 채움(2체면 가로 반씩) | 2×2 영역 가운데에 **3×3칸 상자**를 꽉 채움(사용자 "3x3 정도로 조금 넘치게") — 영역 둘레 발판 반 칸까지 걸친다. 2체(아이온·얄다바오트)면 상자를 가로로 반씩(1.5×3) |
| 보스 ↔ 유닛 겹침 | 보스·몬스터와 유닛 모두 그리는 순서 200 | **유닛이 보스 위에 보인다**(사용자 "보스보다 유닛이 우선해서 위로"). 보스 몸·부위·체력바를 유닛 아래 순서로 |
| 클릭 | 유닛 상자 → 넓힌 유닛 상자 → 몬스터(보스 포함) 순(`RtsUnitSelectLogic.HandleScreenTouchEvent` :475-487) | **그대로** — 이미 유닛 우선(사용자 "클릭도 유닛 우선"). 겹친 자리에서 확인만 |
| 보스 등장 | 보스 라운드 시작 때 영역에 바로 선다(트랙 걷기 없음) | 그대로(사용자 선택) |
| 보스 라운드 사거리 | 모든 유닛·스킬 16칸(`RtsCombatLogic.BossRange`) | 값 그대로(가운데로 옮겨도 전원이 친다), 주석만 "구석이라" → "그리드 어디서든" |
| 트랙 그림 S/E | S = 초록 원 + 'S', E = 빨강 원 + 'E', 3열 왼쪽 여백에 E→S 붉은 점선 화살표 | **S = 진행 방향(첫 칸 쪽) 화살표 아이콘, E = 되돌리기(↺) 아이콘**, E→S 점선 **삭제** |
| 트랙 그림 발판 칸 | 트랙에 4방향으로 붙은 칸만 흰 반투명 채움(2026-09-23 규칙 바뀌기 전 그대로) | 게임 규칙과 같게 **배치 가능한 칸 전부** 채움, 보스 영역 2×2는 비움(붉은 판은 게임이 그린다) |
| 트랙 텍스처 | `95b3ec9d…`(16×13, 테마 5종 공용 `gridRUID`) | 새로 생성·**새 리소스로 업로드**한 RUID로 5종 일괄 교체(옛 RUID는 README에 보관 표시) |
| 사냥 밸런스 | — | 수치 변경 없음. 한 바퀴 66 → 77칸, 좋은 자리 사거리 3 유닛이 한 바퀴 중 사거리 안에 두는 비율 약 44% → 33%(`scratchpad` 계산). Play 뒤 사용자가 보고 몬스터 수·체력 조정 여부를 정한다 |

## Affected Files
| File | Change Type | Description |
|------|-------------|-------------|
| `RootDesk/MyDesk/RtsZoneLogic.mlua` | modify | 꺾임점 표(M2), 보스 영역 값(8·6·2·2), 머리·보스 영역 주석, 이동 칸 수 주석(66 → 77) |
| `RootDesk/MyDesk/RtsBossLogic.mlua` | modify | 크기 상자 = 영역 가운데 `BossFitCells`(3)칸 정사각, 2체면 가로 반씩. 머리 주석 |
| `RootDesk/MyDesk/RtsWaveLogic.mlua` | modify | `SpawnMonsterEntity` — 보스면 그리는 순서를 유닛 아래 값으로(부위·체력바는 이 값을 따라감) |
| `RootDesk/MyDesk/RtsCombatLogic.mlua` | modify | `BossRange` 주석만 |
| `tools/gen-track-grid.js` | modify | 경로 SEQ(M2), 발판 규칙(트랙·보스 영역이 아닌 칸 전부), S 화살표·E 되돌리기 아이콘, 복귀 점선 삭제, 머리 주석 |
| `assets/textures/track-grid.png` · `assets/textures/README.md` | modify | 새 텍스처 + 표(새 RUID, 옛 `95b3ec9d…` 보관) |
| `RootDesk/MyDesk/RtsThemeLogic.mlua` | modify | 프리셋 5종 `gridRUID` → 새 RUID |
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | modify | 그리드 주석(경로 출처 "아티팩트 v16" → 2026-09-25 M2) — 값 변경 없음 |
| `docs/ui-screens.md` | modify | 보스 영역 행(2×2·위치), 보스 라운드 설명(3×3 상자·유닛이 위), 트랙 S/E 표시 |
| `docs/theme-presets.md` | modify | 트랙 판 절(경로 M2·77칸·S/E 아이콘·새 RUID), 헤네시스 행 RUID |
| `.beaver/output/report/rts-base/zone-system-report.md` | modify | build 뒤 `## Change - 260925-1` |

## Code Changes

```text
RootDesk/MyDesk/RtsZoneLogic.mlua
- GetTurnPoints(1-기반 {col,row}) = M2 20점:
    (15,9) (12,9) (12,13) (14,13) (14,11) (8,11) (8,9) (10,9) (10,13) (2,13)
    (2,11) (6,11) (6,2) (4,2) (4,4) (16,4) (16,1) (14,1) (14,6) (11,6)
  EnsurePath가 이 표로 경로 칸(78개 — 교차 칸은 두 번)·트랙 집합(74칸)·발판(130칸)을 만든다. 경로 생성·교차 처리 코드는 그대로(지금도 교차 2곳을 같은 방식으로 다룬다).
- BossAreaCol 8 → 8, BossAreaRow 9 → 6, BossAreaCols 4 → 2, BossAreaRows 5 → 2. IsBossAreaCell·GetBossAreaCenter·SpawnBossArea(붉은 판 크기 = 영역 칸 수)는 값만 따라간다.
- 머리 주석: 트랙(2026-09-25 M2, 77칸, 매듭 3곳 좌표, S/E), 보스 영역(8~9열 × 6~7행 2×2 — 사용자 "가운데 4칸").
```

```text
RootDesk/MyDesk/RtsBossLogic.mlua — SpawnBoss 크기·위치
- before: 보스 슬롯 = 영역(4×5칸)을 보스 수로 가로 등분, 그림 테두리가 슬롯을 꽉 채우는 배율.
- after : 새 프로퍼티 BossFitCells = 3(칸). 맞출 상자 = 영역 가운데를 중심으로 한 3×3칸(가로 3칸 × 세로 3칸).
          slotW = 상자 폭 ÷ 보스 수, 높이 = 상자 높이. 배율 계산(그림 = 피격 박스 ÷ 0.7·0.8)·몸 가운데를 슬롯 가운데에·체력바 폭 = 슬롯 폭 − 0.12는 그대로.
- 머리 주석: 보스 영역 2×2 가운데 + 3×3 상자, 유닛이 보스 위(그리는 순서).
```

```text
RootDesk/MyDesk/RtsWaveLogic.mlua — SpawnMonsterEntity(name, zone, mobId, hp, isBoss)
- 지금 SpawnProp(…, 200)으로 모든 몬스터를 순서 200에 둔다(유닛 아바타도 200).
- 보스(isBoss)면 RtsBossLogic.BossOrder(새 프로퍼티)로 스폰 → 부위(순서 + p.order)·체력바(+5/+6)는 몸 순서를 읽어 자동으로 그 아래 대역.
- 값은 build 첫 단계에서 Maker로 실측해 정한다: 유닛 아바타(AvatarRenderer 200 + 부품)·그림자(−5)와 보스 몸·부위·체력바가 겹칠 때 유닛이 항상 위인 값
  (예 150 — 트랙 판 100·장식 110·보스 영역 판 105보다 위, 유닛 200보다 아래). 같은 SortingLayer에서 안 되면 보스만 한 층 아래 SortingLayer.
```

```text
RootDesk/MyDesk/RtsCombatLogic.mlua
- BossRange = 16 값 그대로. 주석 "보스 영역이 아래 구석이라 그리드 어디서든 닿게" → "보스 라운드엔 그리드 어디서든 보스에 닿게(보스 영역 가운데 2×2 — 2026-09-25)".
```

```text
tools/gen-track-grid.js
- SEQ(0-기반) = [[14,8],[11,8],[11,12],[13,12],[13,10],[7,10],[7,8],[9,8],[9,12],[1,12],[1,10],[5,10],[5,1],[3,1],[3,3],[15,3],[15,0],[13,0],[13,5],[10,5]]
- BOSS = 0-기반 7~8열 × 5~6행. isPad = 트랙도 보스 영역도 아닌 칸(게임 IsPadCell과 같은 규칙). 보스 영역 칸은 아무것도 그리지 않는다.
- 4) S: 초록 원 + 흰 삼각 화살표(첫 칸 → 둘째 칸 방향, 지금은 왼쪽). E: 짙은 빨강 원 + 흰 되돌리기 화살(원호 약 300° + 끝 화살촉). 글자 'S'·'E' 삭제.
- 5) E→S 복귀 점선 화살표 블록 삭제.
- 머리 주석·마지막 출력(steps=77, pads=130, road=74) 갱신.
- 교차 칸: 연석은 "옆 칸이 트랙이 아니면" 그리는 규칙이라 교차·매듭 칸은 자연히 네 면이 열린다(추가 처리 없음). 진행 점선은 경로 순서대로라 교차에서 겹쳐 그려진다.
```

```text
assets/textures/track-grid.png — node tools/gen-track-grid.js 로 다시 생성(1280×1040)
→ msw-mcp asset_create_account_resource_storage_item 으로 새 리소스 업로드(기존 RUID 데이터 교체 금지 — Maker 캐시, README 교체 절차)
→ RtsThemeLogic 프리셋 5종 gridRUID(헤네시스 흰색, 나머지 4종 틴트는 그대로) 새 RUID로
→ README 표: track-grid.png 행 = M2 설명 + 새 RUID, 옛 95b3ec9d… 는 "보관(66칸 경로)"
```

```text
docs/ui-screens.md · docs/theme-presets.md
- 보스 영역: 8~9열 × 6~7행(2×2), order 105, 보스는 가운데 3×3 상자·유닛 아래에 그려짐, 클릭은 유닛 우선
- 트랙: M2 경로 77칸·매듭 3곳, S = 화살표 · E = 되돌리기, 복귀 점선 없음 / theme-presets 헤네시스 행 RUID·"트랙 판" 절의 경로 설명
```

## Test Cases (Maker Play — CLI 테스트 없음, CLAUDE.md Testing)

```
[CASES:zone-grid]   (execute_script, server_main) GetTrackSteps() → 77 · GetPadCount() → 130 · #PathCells → 78
                    IsBossAreaCell(8,6)·(9,7) → true, (10,6)·(8,8) → false
                    IsPadCell(9,6) → false(보스) · (9,10)·(13,12)·(5,3) → true(매듭 칸) · (10,11) → false(교차 트랙) · (11,10) → true(옛 보스 영역, 이제 발판)
                    GetSpawnPoint = 15열 9행 칸 가운데 · GetEndPoint = 11열 6행 칸 가운데
[SUCCESS]           구역 화면: 텍스처 트랙 칸 = 게임 트랙 칸(몬스터가 포석 위로만 걷는다), S 화살표·E 되돌리기 보임, E→S 점선 없음 — 테마 5종 모두(틴트 유지)
[SUCCESS]           일반 라운드: 몬스터가 S에서 왼쪽으로 나와 매듭 3곳·교차 4곳을 지나 E에서 S로 돌아간다
[SUCCESS]           매듭 칸(9,10)에 근접 유닛 → 둘레 8칸 몬스터를 친다
[SUCCESS]           보스 라운드(주니어 발록): 가운데 2×2 붉은 판 위에 바로 서고 그림이 약 3×3칸, 체력바 폭 = 3칸
[SUCCESS]           2체 보스(어둠의 신전 아이온·얄다바오트): 3×3 상자를 가로로 반씩, 서로 안 겹침
[SUCCESS]           보스 둘레 발판의 유닛이 보스 그림 위에 보이고, 겹친 곳 클릭 → 유닛 메뉴(보스 정보창 아님). 보스만 있는 곳 클릭 → 보스 정보창
[SUCCESS]           모든 유닛이 보스를 공격(사거리 16)
[FAIL:validation]   보스 영역 칸·트랙 칸으로 영입(RequestRecruitAt)·이동(RequestMove) → 서버가 발판 아님으로 무시(기존 IsPadCell 검증)
[SUCCESS]           빌드 로그 오류 0, 실행 로그 오류 0

테스트 생략(위임형): SpawnBossArea·IsBossAreaCell·GetBossAreaCenter(값만 따라감 — zone-grid 케이스로 대신), 테마 gridRUID 교체(화면 확인으로 대신)
```

## Outcome Contract (Response Codes)
| Entry point | Outcome |
|---|---|
| `RtsUnitLogic.RequestRecruitAt(jobId, col, row)` · `RequestMove(no, col, row)` (Server, senderUserId) | 발판(`IsPadCell`)이 아니면 무시 — 보스 영역 2×2·트랙 74칸. 규칙은 그대로, 칸 집합만 바뀜 |
| `RtsBossLogic.SpawnBoss` (ServerOnly) | 보스가 영역 가운데 3×3 상자에 맞춰 선다, 순서 = `BossOrder` |
| 구역 그림(`RtsThemeLogic.ApplyToZone` → `SetZoneGrid`) | 새 트랙 텍스처 |

## Decisions
- [x] 트랙 모양 — **M2**(2026-09-25 사용자 "2번으로 가자"). A/B/C·B1~B3·M1·M3는 탈락
- [x] 매듭 — 3개, 둘은 붙고 하나는 멀리, 커브 섞인 불규칙한 길(사용자 "너무 정직해 … 난잡한 형태")
- [x] 보스 영역 위치 — 8~9열 × 6~7행(가운데 반 칸 위, 후보 그림 그대로 확정)
- [x] 보스 크기 — 3×3칸 정도로 조금 넘치게, **유닛이 위·클릭도 유닛 우선**(사용자)
- [x] 보스 등장 — 영역에 바로 나타남(사용자)
- [x] S/E 표시 — S 화살표 · E 되돌리기 아이콘 · E→S 표식 삭제(사용자)
- [x] 발판 규칙 — 그대로(트랙·보스 영역이 아닌 칸 전부), 트랙 그림도 이 규칙으로 칠함(게임과 그림을 맞추는 기본값)
- [x] 밸런스 수치 — 이번엔 안 바꾸고 Play 뒤 사용자 판단(길이 77칸·밀도 감소는 위 표에 기록)

## Build Order (선행 조건 대신 — 업로드도 build 단계)
1. Maker 실측: 유닛과 보스가 겹칠 때의 그리는 순서 → `BossOrder` 값 확정
2. `gen-track-grid.js` 수정 → PNG 생성 → 눈으로 확인(경로·매듭·S/E) → 새 리소스 업로드 → RUID
3. mlua 수정(Zone·Boss·Wave·Combat 주석·Theme RUID·Config 주석) → `maker_refresh_workspace` → 빌드 로그
4. Play로 위 Test Cases → 문서(ui-screens·theme-presets·README) → report Change

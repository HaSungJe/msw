# Plan — 스테이지·몬스터 웨이브·보스 (로드맵 Phase 6 + Phase 7, #22~#30)

## Feature Summary
- **Feature**: 한 판 진행 — 132 스테이지 방 전역 타이머, 구역별 몹 웨이브·처치·메소 드랍, 필드 110 탈락, 보스전(트랙 60초), 클리어·결과 팝업·개인 최고 기록
- **Entry point**: `RtsStageLogic.OnUserEnter → StartRun → BeginStage(n)/EndStage` · `RtsWaveLogic.SpawnTick` · `RtsBossLogic.SpawnBosses/OnBossReachedEnd` · `RtsRunResultLogic.Eliminate/Clear/ShowResult/RequestExit` · `RtsMonsterComponent.Die`
- **Domain**: rts-stage (spec: `.beaver/output/spec/rts-stage/stage-wave-boss-spec.md`)
- **진행 방식**: 문서는 방향·동작 설명(메모리 workflow — 코드 블록은 구조·흐름 도식만). 사용자가 만족할 때까지 같은 페이즈에서 수정 루프.

---

## Prerequisites
- [x] 편성 원본 `.info/monster-wave.md`(132) · `monster.md`(247종) · `level.md` · `balance-detail.md` · `memo.md`(보스 규칙) — 로컬에 있음
- [x] 라운드별 체력·메소 첫 값 — `.info/monster.md` 끝 표(2026-09-23 3차 계산: 총 768,000·보스 체크포인트·보스 = 최적 보스딜 조합·일반 = 테마 계단 + 라인 클리어 한계, 사용자 검토용) · 경제 원본 `.info/level.md` 메소 수입 절 교체
- [x] 공식 자산 이름 검색 동작 확인(파란 달팽이 → `mob/0100101/move·die1`, `sound/mob/0100101/die`)

---

## File List

| File | Action |
|------|------|
| `RootDesk/MyDesk/RtsStageTableLogic.mlua` | new — 132 스테이지 + 몬스터 247종 표(생성물) |
| `RootDesk/MyDesk/RtsStageLogic.mlua` | new — 방 전역 진행(카운트다운·스테이지 전환·조기 종료·판 종료) |
| `RootDesk/MyDesk/RtsWaveLogic.mlua` | new — 구역별 스폰·필드 수·보관/복귀·몬스터 엔티티 생성 |
| `RootDesk/MyDesk/RtsBossLogic.mlua` | new — 보스 생성·트랙 60초 이동·E 도달·처치 |
| `RootDesk/MyDesk/RtsRunResultLogic.mlua` | new — 유저별 결과 상태·탈락·클리어·기록 저장·나가기 |
| `RootDesk/MyDesk/RtsMonsterComponent.mlua` | modified — `Die`(드랍·처치 수·사망 연출·제거), 보관 표시, 보스 감속 무시 |
| `RootDesk/MyDesk/RtsTrackWalkerComponent.mlua` | modified — 정지(보관)·보스 모드(순환 없음·E 도달 알림·감속 무시) |
| `RootDesk/MyDesk/RtsCombatLogic.mlua` | modified — 시험대 삭제, `SpawnMonster` 이전, `IsBossRound` = 스테이지 종류, 보스전 사거리 10, 보관 몹 제외, **방어 단계(damage.md 8단계) 추가 — 보스 방어율 50%, 검은 마법사 4페이즈 100%** |
| `RootDesk/MyDesk/RtsUnitLogic.mlua` | modified — 영입 Lv1·**영입 한도(5라운드마다 1칸)**·TestBench 게이트 삭제, 시연 유닛·시연 메소 삭제(시작 0), 드랍 적립 `AddMeso`, 탈락 시 유닛 전멸 |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | modified — 시연 순회·시험대·시연 유닛 호출 삭제 → `RtsStageLogic.OnUserEnter`, 퇴장 시 웨이브·결과 정리 |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified — 시간 칩(스테이지 번호·맵 이름·남은 시간·카운트다운), 필드 칩 n/110, **영입 버튼 우측 → 화면 상단 가운데(크게, 한도 표시)** |
| `RootDesk/MyDesk/RtsPopupLogic.mlua` | modified — kind `result`(결과 + 나가기 + 닫기), 영입 팝업 하단 문구(한도·다음 영입 라운드), 테스트 프리즘·팬텀 카드 게이트 `DevTools` |
| `RootDesk/MyDesk/RtsJobTableLogic.mlua` | modified — 레벨업 비용표(`EnsureCosts` 구간 표) 교체: 70×8·440 / 350×9·1,140 / 470×9·1,420 / 630×9·1,710 / 6,900×9·47,580 (level.md 5차) |
| `RootDesk/MyDesk/RtsUnitSelectLogic.mlua` | unchanged(영입 배치 모드 그대로) |
| `RootDesk/MyDesk/RtsDemoLogic.mlua` (+ `.codeblock`) | **deleted** — 시연 순회 몹 |
| `tools/gen-stage-table.py` | new — `.info` 원본 → `RtsStageTableLogic` 표 부분 재생성 + 검산 + monster.md 라운드 표 갱신 |
| `.info/monster.md` · `.info/level.md` · `.info/augmentation.md` | modified(로컬 전용, 커밋 안 함) — 자산 RUID·스케일·체력·메소 / 수입·비용표 5차(교체 완료) / 프리즘 라운드 자쿰·시그너스·스우·루시드·진 힐라(교체 완료) |
| `.beaver/output/roadmap/maple-augment-defense-roadmap.md` | modified — Phase 6·7 in-progress, 보스 규칙 갱신 |

새 `.mlua`의 `.codeblock`은 Maker가 `maker_refresh_workspace` 때 만든다.

---

## Design

> 근거: 트랙 이동 `RtsTrackWalkerComponent.mlua:5-44`(t 등속·E→S 순환·빙결 감속) · 몬스터 생성 `RtsCombatLogic.mlua:78-101`(스프라이트·HitComponent·DamageSkinSpawner·RtsMonsterComponent) · 구역 몹 목록 `RtsCombatLogic.mlua:106-119` · 보스 라운드 `RtsCombatLogic.mlua:227-230` · HP 차감 `RtsMonsterComponent.mlua:233-237` · 보스 체력바 `RtsMonsterComponent.mlua:43-54` · 입장 흐름 `RtsBootstrapLogic.mlua:5-26` · 메소 `RtsUnitLogic.mlua:10-12,182-214` · 영입 `RtsUnitLogic.mlua:329-361` · 레벨업 `RtsUnitLogic.mlua:552` · 시간 칩 `RtsHudLogic.mlua:200-207,315` · 생존 표시 `RtsHudLogic.mlua:450` · 팝업 셸 `RtsPopupLogic.mlua:83-141` · 방출 팝업 형식 `RtsPopupLogic` kind `dismiss`.

### 1. 표 — RtsStageTableLogic (생성물)

```text
스테이지 행 132개 (순번 = 1..132)
  no · tag("1".."115" / "보스") · name · kind(mob|boss|rest) · region · bgm("sound-127")
  mobs = { "M001", "M002", … }   ([73]은 [59]~[65] 8종, 어둠의 신전은 B14·B15)
  hp   = 몹 1마리 체력(몬스터 라운드) / 보스 1체 체력(보스 라운드) / 0(쉬는)
  meso = 라운드 메소 총액(몬스터 라운드만, 나머지 0)
  sec  = 20 | 60 | 30
몬스터 행 247개 (M001~M229, B01~B18)
  name · move(이동 클립, 없으면 stand) · die(die1) · dieSound(sound/mob/<id>/die)
  scale · boxW·boxH·boxY(피격 박스, 로컬) · barY(체력바 높이, 세계) · dieSec(사망 클립 길이)
조회: GetStageCount · GetStage(no) · GetMonster(id) · GetMobMeso(no, spawnIndex) · IsBossStage(no)
```

- 표는 `tools/gen-stage-table.py`가 스크립트 안의 `-- BEGIN GENERATED` ~ `-- END GENERATED` 사이만 다시 쓴다(조회 메서드는 손으로 쓴 부분).
- 마리당 메소 = 총액 ÷ 40, 나머지는 앞 순번부터 +1 → 40마리 합 = 총액(생성 시 검산).
- 영입 한도 일정(1·5·10·15·20·25)과 구간 배율 경계(26·64·89·121)도 표의 상수로 — 코드는 순번만 비교한다.

### 2. 생성 스크립트 — tools/gen-stage-table.py

```text
입력(로컬 .info)                         처리                                    출력
monster-wave.md ─ 132 스테이지 ─┐
monster.md ─── 자산 RUID·크기 ──┼─▶ 체크포인트 메소 ⇄ 표준 빌드(레벨) ⇄ 체력 ─▶ ① RtsStageTableLogic 표 부분
level.md ───── 체크포인트·비용 ──┤    (반복 계산으로 수렴) [검산 실패 시 아무것도 안 씀] ② monster.md 몬스터별 체력·메소 칸
balance-detail.md ─ 직업 DPS ───┘                                                 ③ monster.md 끝 '라운드별 체력·메소' 표
```

- 계산식은 spec '경제 — 오름세 수입 + 스페셜 스테이지 + 레벨업 비용 재조정'·'체력 — 보스는 최적 조합 고점의 %, 일반은 테마 계단 + 라인 클리어 한계'와 monster.md 표 머리말 그대로(검토용으로 이미 돌린 식 — 2026-09-23 scratch `stage_calc.py`(직업 DPS·편성 파서)·`stage_calc3.py`(일반 체력)·`stage_calc5.py`(수입·표준 빌드·보스 고점)·`opt5.py`(비용표 맞춤)를 이 파일로 옮긴다. 비용표는 확정값을 상수로 두고, 맞춤은 다시 돌릴 때만). 체크포인트 7개(자쿰 67,000 · 혼테일 124,000 · 핑크빈 206,000 · 시그너스 270,000 · 루시드 576,000 · 진 힐라 704,000 · 듄켈 768,000 — 레벨대 가운데)·테마 23개와 압박표·기대 증강 계수·영입 일정은 파일 맨 위 상수.
- 메소 → 표준 빌드 → 체력 → (구간 안 √체력 비례) 메소 분배가 서로 물려 있어 40회 반복 후 정수화(구간 안 반올림 오차는 그 구간 마지막 라운드에)하고, 정수 메소로 체력을 한 번 더 계산한다.
- 몬스터 크기: 이동 클립 첫 프레임의 가로·세로(px, 스프라이트 `.win.mod` 헤더)를 읽어 목표 높이로 맞춘 스케일 — 일반 몹 목표 세로 1.2유닛(0.9~1.6 사이로 자름), 보스 3.0유닛. 피격 박스 = 프레임 크기 × 0.8, 체력바·데미지 숫자 높이 = 프레임 위.
- 사망 클립 길이 = 클립 `.win.mod` 프레임 시간 합(기존 연출 작업의 파서).

### 3. 자산 매칭 (build 첫 단계, MCP로 수행 → monster.md에 기록)

```text
몬스터 이름 ─ asset_search_resources(cat=animationclip,audioclip, query="*<이름>") ─▶ 후보 RUID
   └ metadata_bulk의 mapleImgFullPath "maplestory/mob/<몹번호>/<동작>"으로 몹 번호 확정
       (이름이 여러 몹 번호에 걸리면: move가 있는 번호 → 원작 등장 지역과 맞는 번호 순)
몹 번호 ─▶ mob/<번호>/move (없으면 stand) · mob/<번호>/die1 · sound/mob/<번호>/die
결과 ─▶ .info/monster.md 기본·사망 애니메이션·사망 보이스 칸 + 썸네일 시트(scratch)로 확인
```

- 못 찾은 몹은 목록으로 보고하고, 그동안은 초록달팽이 자산으로 대체해 판은 돈다(표에 대체 표시).
- 보스 18종은 시트를 사용자에게 보여 주고 바꿀 수 있게 한다(프리즘 자산 때 방식). 여러 부위 보스(자쿰·혼테일·검은 마법사)는 대표 몸통 클립 1개로 시작.
- 이동 속도 100 · 방어율 0은 monster.md 칸에도 채운다.

### 4. 방 전역 진행 — RtsStageLogic (서버, 상태는 @Sync로 클라에)

```text
            첫 유저 입장                  5초                BeginStage(1)
 idle ─────────────────▶ countdown ─────────────▶ running ────────────────┐
  ▲                                                  │  스테이지 시간 끝 / 보스 조기 종료
  │ (판 종료 뒤 새 유저 입장: 맵 초기화)              ▼
 ended ◀──── 모든 유저 탈락·클리어 ──── EndStage → BeginStage(n+1) … (132 끝나면 ended)

 @Sync: RunState(idle/countdown/running/ended) · StageNo · StageEndsAt(ServerElapsedSeconds) · CountdownEndsAt
 BeginStage(n): 종류별 호출 — mob → RtsWaveLogic:StartSpawn(n) / boss → RtsWaveLogic:Stash() + RtsBossLogic:SpawnBosses(n)
                / rest → 없음.  훅: OnStageStarted(n) (Phase 4 증강 지급·Phase 10 BGM이 여기에)
 EndStage():    mob → 스폰 정지(남은 몹은 계속 돔) / boss → 살아 있는 보스 = E 미도달이어도 시간 끝 = 탈락 처리 후 제거, Unstash()
                생존 유저의 '마지막 버틴 스테이지' = n 기록(RtsRunResultLogic)
 보스 조기 종료: 생존 유저 전원의 보스가 죽으면 3초 뒤 EndStage
 타이머: _TimerService 반복 0.25초로 StageEndsAt 확인(HUD는 클라가 StageEndsAt으로 직접 남은 시간 계산)
```

- 진행 중 입장: 구역 배정만, 스폰 대상 목록엔 다음 `BeginStage`부터 들어간다.
- 시간 칩 표기: 카운트다운 `시작까지 5` / 몬스터 `12/132 골드비치 해변 0:17` / 보스 `보스 · 자쿰의 제단 0:43` / 쉬는 `쉬는 시간 0:25`.

### 5. 웨이브 — RtsWaveLogic (서버)

```text
StartSpawn(n): 대상 = 생존 구역 전부. 구역마다 '스폰 순서' = 스테이지 몹 목록을 40칸에 고르게 채우고 섞은 배열
SpawnTick(0.5초): 구역마다 1마리 — SpawnMob(zone, mobId, n, spawnIndex) → 트랙 t=0에서 출발, 속도 100, 순환
SpawnMob: 몬스터 표로 엔티티(스프라이트 move·스케일·HitComponent 박스·DamageSkinSpawner·RtsMonsterComponent{MonsterId, MaxHp=Hp=stage.hp, Zone, Meso=GetMobMeso(n, i)})
          이름 = "Mob<zone>_<일련번호>" (시험대 RtsDummy 이름 규칙 대체 — 유닛 공격 IsAttackTarget은 이름 비교 그대로)
FieldCountByZone(SyncTable): 스폰 +1, Die −1 → 110 이상이면 RtsRunResultLogic:Eliminate(owner, "field")
Stash(): 구역 몹 전부 Stashed = true(숨김·걷기 정지·대상 제외)   Unstash(): 원래대로(같은 t에서 다시 돔)
ClearZone(zone): 탈락·퇴장 시 그 구역 몹 전부 제거
```

- `RtsCombatLogic.GetZoneMonsters`는 `Stashed` 몹을 뺀다 → 보스전엔 보스만 대상.

### 6. 몬스터 생애 — RtsMonsterComponent · RtsTrackWalkerComponent

```text
피격(OnHitServer) → Hp 0 → Die(): Dead = true(대상 제외) → 구역 주인에게 Meso 적립(RtsUnitLogic:AddMeso) · 처치 수 +1
                                   → 필드 수 −1 → 전 클라 사망 연출(die 클립 + 사망음) → dieSec 뒤 Destroy
보스면: 메소 없음, RtsBossLogic:OnBossKilled(zone)
TrackWalker: Paused(보관 중 정지) / BossMode(Speed = 트랙 길이 ÷ 60초를 속도 수치로, Loop = false, 빙결 감속 무시, t ≥ 1이면 RtsBossLogic:OnBossReachedEnd(zone) 한 번)
몬스터 스프라이트: 표의 scale·flip 규칙(기본 왼쪽 보기 — 기존 SetFacing 그대로)
```

### 7. 보스 — RtsBossLogic (서버)

```text
SpawnBosses(n): 생존 구역마다 스테이지 보스(1체, 어둠의 신전은 2체 — 둘째는 1초 뒤) 를 트랙 t=0에
                IsBoss = true(긴 체력바) · MaxHp = stage.hp · BossMode 걷기 · 이름 "Boss<zone>_<k>"
OnBossKilled(zone): 그 구역 보스가 다 죽었으면 구역 '보스 처치' 표시. 마지막 스테이지(검은 마법사 4페이즈)면 RtsRunResultLogic:Clear(owner)
                    생존 유저 전원 처치 → RtsStageLogic 조기 종료 예약(3초)
OnBossReachedEnd(zone) / 스테이지 시간 끝에 보스 생존: 보스 HP 깎은 비율 = 1 − 남은 HP 합 ÷ 최대 HP 합 → RtsRunResultLogic:Eliminate(owner, "boss", 비율)
보스전 사거리: RtsCombatLogic 사거리 계산에서 IsBossRound(zone)이면 사거리 10(스킬·기본 공격 공통), 보스전 잠금 스킬 제외는 기존 SkillUsable 그대로
```

### 8. 결과·탈락·클리어 — RtsRunResultLogic (서버) + 결과 팝업(클라)

```text
유저별: State(alive/eliminated/cleared) · LastClearedNo · Kills · BossPct · Reason(field/boss)
Eliminate(userId, reason, pct): State = eliminated → RtsWaveLogic:ClearZone · RtsBossLogic 보스 제거
       → RtsUnitLogic:WipeUnits(userId)(공격 루프 정지·엔티티 제거) → 구역 중앙에 비석 스프라이트
       → 플레이어 목록 탈락(BroadcastPlayerList의 생존 열 = State) → SaveBest → ShowResult(…, userId)
Clear(userId): State = cleared, LastClearedNo = 132 → SaveBest → ShowResult
모두 alive가 아니면 RtsStageLogic 판 종료
SaveBest: 점수 = LastClearedNo × 100000 + round(BossPct × 10000)
          _DataStorageService:GetUserDataStorage(userId):GetAsync("BestRun") → 더 높을 때만 SetAsync
          값 = "점수|순번|맵 이름|클리어 0/1|날짜" (전광판 등록은 Phase 8 #42)
ShowResult(@ExecSpace Client, 마지막 인자 userId): RtsPopupLogic:OpenResult(…)
RequestExit(@Server): senderUserId 확인 → _UserService:KickUser(senderUserId, KickReason.WorldContent)
```

```text
결과 팝업 (kind "result", 640×360 — 방출 확인 팝업과 같은 셸)
┌────────────────────────── 결과 ──────────────────────────┐
│  클리어!  /  탈락 — 필드 110  /  탈락 — 보스 시간 초과      │
│  도달: 57 / 132 · 스카이라인 올라가는 길                    │
│  처치 1,834마리   ·   보스 HP 72.4% (보스전 탈락일 때만)    │
│  개인 최고: 64 / 132 · 세계수 정상                         │
│                         [ 닫기 ]   [ 나가기 ]               │
└──────────────────────────────────────────────────────────┘
닫기 = 팝업만 닫고 관전(F1~F8·목록 클릭). 나가기 = RequestExit
```

### 9. 기존 코드 연결·변경

- **RtsBootstrapLogic**: `_RtsDemoLogic:EnsureWalkers()`·`EnsureDemoUnits`·`SetupTestBench` 호출 삭제 → 구역 배정 뒤 `_RtsStageLogic:OnUserEnter(userId)`. 퇴장 시 `RtsWaveLogic:ClearZone`·`RtsRunResultLogic:OnLeave`. 플레이어 목록 생존 열은 `RtsRunResultLogic` 상태.
- **방어 단계**(RtsCombatLogic 데미지 계산, damage.md 8단계): 대상이 보스면 남은 방어율 = 보스 방어율(표 — 일반 50, 검은 마법사 4페이즈 100) − 유닛 방무(히어로는 ign + ignBoss 합: 50레벨 110, 방어구 부수기 +30), 0 미만 0 → 데미지 × (1 − 남은 방어율). 결과가 0이면 타격 연출·숫자 없음. 일반 몬스터는 방어율 0.
- **RtsJobTableLogic**: `EnsureCosts` 구간 표를 level.md 5차 값으로 교체(10 단위). 방출 환급(RtsUnitLogic.RequestDismiss)은 10메소 단위로 내림.
- **RtsUnitLogic**: `RequestRecruitAt`의 `TestBench` 게이트 삭제·레벨 50 → 1. `DemoMeso`·`EnsureDemoUnits` 삭제(시작 메소 0). `AddMeso(userId, n)`(서버, OnChanged로 HUD) 추가. `WipeUnits(userId)` = 기존 `RemoveUnits` 재사용(공격 루프 정지 포함 확인). `RequestMove`의 개발모드 쿨 0 예외 삭제.
- **RtsCombatLogic**: `TestBench`·`SetupTestBench`·`BossRUID`·`Boss*`/`Unit*` 칸·`DummyName`·`TestBigHit` 삭제, `SpawnMonster` → RtsWaveLogic, `IsBossRound(zone)` = `RtsStageLogic` 현재 스테이지가 보스, 사거리 계산에 보스전 10, `GetZoneMonsters`에서 `Stashed`·`Dead` 제외.
- **RtsHudLogic**: 시간 칩 폭 170 → 넓게(맵 이름이 들어가도록 ≈ 360), 라벨 '시간' 대신 스테이지 문구, 스페셜 라운드는 '스페셜' 금색 표시. 필드 칩(메소 칩 아래) `필드 23 / 110`, 90 이상 붉게. 클라는 `StageEndsAt`·`FieldCountByZone`(내 구역) 동기화로 매 0.25초 갱신.
- **영입 버튼 이동**(사용자): 우측 `RtsRecruitBtn`(RtsHudLogic.mlua:224-229, 130×50)을 빼고 화면 상단 가운데 큰 버튼(≈ 320×64, 글자 26)으로. 우측 패널은 유닛 슬롯 6칸만(위로 당김).

```text
            ┌────────────────────────────────┐
            │   영입 가능 1   (금색 강조)      │   ← 한도가 남았을 때
            └────────────────────────────────┘
            ┌────────────────────────────────┐
            │   다음 영입 · 10라운드  (흐리게) │   ← 한도를 다 썼을 때 / 6명이면 '영입 완료'
            └────────────────────────────────┘
판 시작(카운트다운) 때 영입 팝업 자동 열림. 이후 칸이 열리면 버튼만 강조(짧은 반짝임), 팝업은 누를 때만
```

- **RtsUnitLogic 영입 한도**: `RecruitLimit()` = 1 + floor(현재 순번 ÷ 5), 최대 6(카운트다운·1~4라운드 = 1). `RequestRecruitAt`는 보유 수 < 한도일 때만(방출로 빈 칸은 다시 영입 가능). 탈락·클리어 유저는 거부.
- **RtsPopupLogic**: kind `result` + `OpenResult`. 테스트 프리즘 버튼·팬텀 카드 조건을 `_RtsCombatLogic.TestBench` → `DevTools`(RtsPopupLogic 프로퍼티, 기본 true).
- **비석**: 원작 비석 스프라이트를 자산 검색으로 찾아(`*비석`/`effect/Tomb`) RtsRunResultLogic 상수로.

### 10. 삭제 목록 (§1.7)

- `RtsDemoLogic.mlua` + `.codeblock` 전체(시연 순회 몹).
- `RtsCombatLogic`: 시험대 프로퍼티·`SetupTestBench`·`TestBigHit` 분기·`IsBossRound`의 `TestBench` 분기·`SpawnMonster`(이전).
- `RtsUnitLogic`: `DemoMeso`·`EnsureDemoUnits`·`TestBench` 게이트 2곳(영입·이동 쿨).
- `RtsBootstrapLogic`: 시연·시험대 호출 3줄과 주석.
- `RtsMonsterComponent` 머리말의 "허수아비·무적 시험" 설명(Invincible 필드는 남김 — 쓰지 않으면 삭제 검토).
- 로드맵 Notes의 "시험대 코드는 Phase 6에서 지운다" 항목 → 완료 표시.

---

## Test Cases
이 스택엔 CLI 테스트 러너가 없다(CLAUDE.md Testing). 계산은 **생성 스크립트 검산**(실패 시 표를 쓰지 않고 멈춤 — 2026-09-23 사용자 선택 3종), 동작은 **Maker Play 시나리오**로 확인한다.

```
[CASES:gen-stage-table 메소]   전부 잡으면 합계 768,000
[CASES:gen-stage-table 메소]   표준 빌드(번 메소를 다 씀)가 7개 보스 직전 목표 레벨대 안 / 보스 직전 남는 메소 ≤ 번 것의 10%
[CASES:gen-stage-table 메소]   마리당 메소 10 단위 / 스페셜 제외 기본 곡선은 줄지 않음 / 아케인 첫 라운드 ≥ 직전 기본 라운드 × 1.8 / 스페셜 = 같은 자리 기본의 2배
[CASES:gen-stage-table 비용]   레벨업 비용 10 단위, 1→50 합 128,000, 일반·벽 비용 모두 레벨대가 오를수록 비쌈
[CASES:gen-stage-table 메소]   듄켈 뒤(쉬는·검은 마법사) 메소 = 0
[CASES:gen-stage-table 메소]   각 몬스터 라운드: GetMobMeso(n, 1..40) 합 = 라운드 총액
[CASES:gen-stage-table 메소]   보스·쉬는 라운드 메소 = 0
[CASES:gen-stage-table 편성]   132 라운드 = 몬스터 114(풀 [73] 포함) · 쉬는 1 · 보스 17
[CASES:gen-stage-table 편성]   모든 몹 id가 monster.md에 있음 / [73] 몹 8종 / 어둠의 신전 보스 2체
[CASES:gen-stage-table 편성]   일반 몹 전부 자산 3개(이동·사망·사망음) — 대체(초록달팽이) 몹은 목록으로 출력
[CASES:gen-stage-table 체력]   표준 빌드 유닛 수 = 1(1~4) · 2(5~9) · … · 6(25~) / 듄켈 시작 시 전원 50
[CASES:gen-stage-table 체력]   같은 테마 안 연속 몬스터 라운드는 체력이 줄지 않음 / 테마가 바뀌면 오른다
[CASES:gen-stage-table 체력]   아케인리버 첫 라운드 체력 ≥ 직전 몬스터 라운드 × 2
[CASES:gen-stage-table 체력]   모든 몬스터 라운드 체력 ≤ 라인 클리어 조합 한계 × 0.95 (클리어 불가 금지)
[CASES:gen-stage-table 보스]   보스 체력 = 고점 × 60 × 보스별 기준 — 고점 조합의 60초 딜 ÷ 체력 = 1/기준
[CASES:gen-stage-table 보스]   4페이즈: 방무 없는 직업의 딜 = 0 / 히어로+증강 · 팬텀+증강 · 방어구 부수기 세 경로 모두 60초 딜 ≥ 체력

[SUCCESS] Play: 입장 5초 뒤 1/132 달팽이 동산 시작, 0.5초마다 1마리씩 20초에 40마리, 시간 칩 남은 시간 감소
[SUCCESS] Play: 스페셜 라운드(9 저주받은 신전 등)에서 시간 칩 '스페셜', 처치 메소가 기본의 2배
[SUCCESS] Play: 몹 처치 → 사망 클립·사망음 → 사라짐, 메소 칩이 라운드 몫만큼 증가, 필드 칩 −1
[SUCCESS] Play: 카운트다운 때 영입 팝업이 자동으로 열리고 상단 버튼 '영입 가능 1' → 1명 영입 뒤 '다음 영입 · 5라운드', 5라운드가 되면 다시 강조
[SUCCESS] Play: Lv1 영입 → 레벨업 버튼이 드랍 메소로 동작
[SUCCESS] Play: 보스 라운드 — 일반 몹이 사라졌다가 보스전 뒤 같은 자리에서 다시 돔, 보스가 60초에 트랙 한 바퀴, 모든 유닛이 보스를 침(사거리 10)
[SUCCESS] Play: 보스 처치 → (혼자면) 3초 뒤 다음 라운드
[SUCCESS] Play(execute_script로 라운드 점프): 어둠의 신전 2체 / 검은 마법사 4페이즈 처치 → 클리어 팝업
[FAIL:elimination] Play: 필드 110 도달 → 유닛 전멸·비석·목록 탈락·결과 팝업(나가기/닫기)
[FAIL:elimination] Play: 보스가 E 도달 → 탈락 팝업에 보스 HP% 표시, BestRun 저장값 확인(maker_reset_data_storage 후 재확인)
[SUCCESS] Play(execute_script로 132 점프): 4페이즈에서 방무 없는 유닛 데미지 0(숫자 안 뜸), 히어로(50)·팬텀은 그대로, 방어구 부수기 유닛은 30%
[SUCCESS] Play: 보스 피격 데미지가 방무 없는 직업은 절반, 50레벨 히어로는 그대로
[FAIL:validation]  나가기 요청은 senderUserId 본인만 / 탈락 유저의 영입·레벨업·이동 요청은 서버가 무시 / 영입 한도를 넘는 영입 요청은 서버가 무시

테스트 생략(위임형): HUD 문구 갱신·팝업 배치(표시만, Play 스크린샷으로 확인), 조회 메서드(GetStage/GetMonster — 표 그대로 반환)
```

---

## Response Codes
| Code | Cause |
|------|------|
| 스테이지 시작 | `BeginStage(n)` — HUD 시간 칩 갱신, 몬스터면 스폰 시작 / 보스면 보관 + 보스 생성 / 쉬는이면 없음 |
| 처치 | 드랍 적립(구역 주인)·처치 수 +1·필드 −1·사망 연출 |
| 탈락(field) | 필드 110 — 구역 정리·유닛 전멸·비석·결과 팝업 |
| 탈락(boss) | 보스 E 도달 또는 보스 라운드 시간 끝에 생존 — 보스 HP% 기록·결과 팝업 |
| 클리어 | 검은 마법사 4페이즈 처치 — 결과 팝업 |
| 판 종료 | 모든 유저 탈락·클리어 — 스폰·타이머 정지 |
| 거부(무시) | 탈락·클리어 유저의 영입·레벨업·이동·방출 요청 / 영입 한도 초과 / 남의 나가기 요청 / 발판 아님·자리 있음(기존) |
| 생성 중단 | `gen-stage-table.py` 검산 실패 — 표·monster.md를 쓰지 않고 실패 항목 출력 |

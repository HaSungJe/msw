# Plan — 증강·프리즘 (로드맵 Phase 4 #14~#18)

## Feature Summary
- **Feature**: 라운드별 등급 지급 → 3택1 → 증강창에서 유닛 지정(브·실·골 능력치 합연산) / 프리즘 12종 = 직업 전용 스킬 표 변경 + 팬텀 해금 / 개발용 지급 트리거(B 키) / 밸런스 재계산
- **Entry point**: `RtsAugmentLogic`(서버: `Grant`·`RequestChoose`·`RequestAssign`·`DevGrantNext` → 클라 `ShowOffer`·`OnAugmentChanged`) / `RtsAugmentTableLogic`(표) / `RtsAugmentPopupLogic`(3택1·증강창, `RtsPopupLogic` 셸 위) / `RtsJobTableLogic.GetSkillsFor/GetStatFor`(프리즘 반영 표)
- **Domain**: rts-base
- **spec**: `.beaver/output/spec/rts-base/augment-prism-spec.md`
- **작성 방식**: 코드가 아니라 **동작·방향 설명**(`.beaver/memory/workflow.md`). 코드는 build가 쓴다. 정의 원본 `.info/augmentation.md`·`.info/character.md`·`.info/damage.md`·`.info/attack.md`.

---

## Prerequisites
- [x] 증강 정의·가중치·라운드 지급표 확정 — `.info/augmentation.md`(2026-09-22)
- [x] 프리즘 12종 정의 — `.info/character.md` '종류: 프리즘' + 자유전직이 주는 액티브 2종(2026-09-22)
- [x] 유닛 전투·팝업·잠금 인프라 — Phase 3 done(`RtsCombatLogic.DoAttack`, `RtsUnitPopupLogic`, `SetPermaLock`)
- [x] 팝업 껍데기 — `RtsPopupLogic.BuildAugment/BuildPick`(화면 v2)
- 인프라 부재 없음. 프리즘 연출 자산은 인레이지만 확보 — 나머지는 기존 연출 재사용 후 사용자가 주는 대로 교체(차단 아님)

---

## File List

| File | Action |
|------|--------|
| `RootDesk/MyDesk/RtsAugmentTableLogic.mlua` | new — 증강 항목(4등급, 가중치, 효과), 프리즘 12종(직업·효과·잠금·연출 키), 라운드 지급표 32칸, 조회 함수 |
| `RootDesk/MyDesk/RtsAugmentLogic.mlua` | new — 서버 권위: 지급·3장 추첨·선택·대상 지정·프리즘 적용·팬텀 해금·능력치 합산, SyncTable 보유 목록, 개발용 트리거 |
| `RootDesk/MyDesk/RtsAugmentPopupLogic.mlua` | new — 3택1 팝업 내용, 증강창 내용(탭·목록·상세·대상 지정), 관전 읽기 전용 |
| `RootDesk/MyDesk/RtsPopupLogic.mlua` | modified — `augment`/`pick` 내용을 `RtsAugmentPopupLogic`에 위임, 예시 카드·예시 유닛·B 키 미리보기·`Pick/AugTabs` 상태 **삭제**, `pick` 제목 "증강 선택" |
| `RootDesk/MyDesk/RtsJobTableLogic.mlua` | modified — `GetSkillsFor(u)`/`GetStatFor(u)`(프리즘 오버레이), 프리즘이 주는 신규 액티브 4종(애로우 레인·트루 스나이핑·디바인 퍼니시먼트·블레이드 토네이도+카르마 퓨리)의 스킬 항목·연출 정의, 스킬 항목 `bossHits`·`bossFinal` 키 |
| `RootDesk/MyDesk/RtsUnitComponent.mlua` | modified — `@Sync Prisms`(문자열), 동기화 시 팝업·연출 갱신 |
| `RootDesk/MyDesk/RtsUnitLogic.mlua` | modified — `SpawnUnit` 끝에서 `RtsAugmentLogic:OnUnitSpawned`(미보유 직업 프리즘 자동 적용 훅), `ApplyPrism(userId, no, id)`(Prisms 갱신 + 영구 잠금 + OnChanged) |
| `RootDesk/MyDesk/RtsCombatLogic.mlua` | modified — `DoAttack`: `GetSkillsFor/GetStatFor` 사용, 증강 합산 한 줄, 보스 15타 집중(`bossHits`·`bossFinal`), 시험대에 보스 1기 플래그 |
| `RootDesk/MyDesk/RtsUnitBuffLogic.mlua` | modified — `GetAugmentsFor` 스텁 → `RtsAugmentLogic` 위임, 홀리 유니티 bond 활성 조건 = 프리즘 보유(lv 99 우회) |
| `RootDesk/MyDesk/RtsUnitPopupLogic.mlua` | modified — 능력치 표에 증강 합산 한 줄, 스킬 탭이 `GetSkillsFor` 사용(프리즘 스킬 표시, 직업명 듀얼블레이드), 증강 탭 실데이터 |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified — 증강 버튼 미지정 배지(빨간 n), 관전 전환 시 배지 숨김 |
| `RootDesk/MyDesk/RtsSkillFxLogic.mlua` | modified — 프리즘 연출 키(인레이지판 fx 교체는 스킬 표에서 오므로 여기선 `bossHits` 반복 타격 연출: 같은 대상에 마크 n개·타격 클립 n회) |
| `.beaver/output/report/rts-base/augment-prism-report.md` | new(build) |
| `.info/balance-detail.md` '증강 반영' 절, scratchpad `augcalc.py` | modified — #18 재계산(I/II/III·10/10/7·프리즘 5) |
| `.info/attack.md` | modified — §2에 "프리즘이 바꾼 스킬 표(GetSkillsFor)" 한 줄, §5 시험대에 B 키 지급 |

---

## Design

> 근거: 팝업 셸·위임 꼴 `RtsPopupLogic.Open`(RtsPopupLogic.mlua:80-127, 유닛은 `_RtsUnitPopupLogic:BuildBody`), 3택1 껍데기(:330-401), 증강창 껍데기(:267-309) / 서버 RPC 꼴 `RtsUnitLogic.RequestLevelUp`(senderUserId, 잘못된 값 조용히 무시, RtsUnitLogic.mlua:350) + 클라 알림 `OnChanged(no, meso, userId)`(:165) / 능력치 흐름 `GetStat → ApplyToStat → CalcStat`(RtsCombatLogic.mlua:236-238, RtsUnitPopupLogic.mlua:120-124) / 잠금 `GetLock/SetLock/SetPermaLock`(RtsJobTableLogic.mlua:497-540, RtsUnitLogic.mlua:407) / SyncTable 꼴 `MesoByUser`(RtsUnitLogic.mlua:10) / 버프 정의 `GetDefs`(RtsUnitBuffLogic.mlua:30)

### 1. 증강 테이블 (RtsAugmentTableLogic — augmentation.md의 코드판)

```text
항목 = { id, grade(bronze/silver/gold/prism), name, weight, effect }
  능력치 effect: crit +n / critDmg +n / flat +n / pct +n / boss +n   (damage.md ①~④ 자리)
  프리즘 effect: { job, kind = "prism", ... 스킬 변경 내용은 RtsJobTableLogic 프리즘 오버레이가 id로 찾는다 }
브론즈 12 = 약점 찾기·급소 찌르기·무기 연마·전투 감각 × I/II/III (12/8/5)
실버 15 = 위 4계열 × I/II/III (13.5/9/4.5) + 보스 사냥꾼 I/II/III (6/4/2)
골드 15 = 위 4계열 × I/II/III + 거인 학살자 I/II/III (골드 III 약점 찾기는 [4])
프리즘 12 = 팬텀(5) · 자유전직-듀얼블레이드(5) · 인레이지·홀리 유니티·거대화·엘릭서·초월·디바인 퍼니시먼트·애로우 레인·트루 스나이핑·풍마수리검(10) · 블리자드 템페스트(10, [?]는 사용자 재배분 전 임시)
가중치는 상대값 — 등급 안에서 weight ÷ 합. 이름·수치 문자열은 여기 한 곳(팝업·카드·유닛 탭이 같은 글자를 쓴다)

라운드 지급표 32칸(순서 = 게임 진행 순): { stage = n, grade } 27개 + { boss = "자쿰"…, grade = "prism" } 5개
  브 [4·17·30·38·51·63·76·84·97·110] / 실 [8·21·34·42·55·68·80·89·101·114] / 골 [13·25·46·59·72·93·106] / 프리즘 자쿰([25] 뒤)·핑크빈([42] 뒤)·시그너스([50] 뒤)·루시드([80] 뒤)·진 힐라([109] 뒤)
  GetSchedule() = 이 32칸(진행 순 정렬), GetGradeAt(stage 번호 또는 보스 이름) = 등급 또는 없음
  Phase 6 스테이지 로직이 전환 이벤트에서 GetGradeAt을 부른다 — 이번 페이즈엔 DevGrantNext가 32칸을 순서대로 걷는다
```

### 2. 서버 상태·흐름 (RtsAugmentLogic)

```text
상태
  OwnedByUser  SyncTable<string,string>  userId → "seq:id:target;seq:id:target;…"  (target 0 = 미지정, 프리즘은 적용 유닛 번호 또는 0 = 미보유 직업)
  UnlockByUser SyncTable<string,string>  userId → "phantom" 등 쉼표 목록
  서버 메모리: NextRound[userId](개발용 32칸 커서), Pending[userId] = { grade, label, cards = {id×3} }, Queue[userId] = 대기 지급 목록, SeqByUser

Grant(userId, grade, label)                                   ServerOnly
  이미 Pending이면 Queue에 넣고 끝. 아니면 카드 3장 추첨(§3) → Pending 저장 → 클라 ShowOffer(label, 카드 3장 표시용 {id,grade,name,desc}, userId)

RequestChoose(cardIdx)                                        Server(senderUserId)
  Pending 없음·1~3 밖이면 무시. 고른 id를 보유에 추가(seq 증가)
   - 브·실·골: target 0 → OwnedByUser 갱신 → 클라 OnAugmentChanged(seq, "choose", userId) → 클라가 증강창을 그 항목 선택 상태로 연다
   - 프리즘 팬텀: UnlockByUser에 phantom 추가 → OnAugmentChanged
   - 프리즘 직업 전용: 그 직업 유닛이 있으면 RtsUnitLogic.ApplyPrism(userId, no, id)(Prisms 갱신·영구 잠금·OnChanged), target = 그 번호. 없으면 target 0(미보유 직업 — 목록에 "영입 시 적용")
  Pending 비움 → Queue에 남은 게 있으면 다음 Grant

RequestAssign(seq, no)                                        Server(senderUserId)
  내 보유의 seq이고 target 0이고 브·실·골이고 no가 내 구역의 살아 있는 내 유닛이면 target = no → OwnedByUser 갱신 → OnAugmentChanged(seq, "assign", userId)
  프리즘·이미 지정·남의 유닛·없는 유닛 → 무시(변경 불가 규칙)

OnUnitSpawned(userId, no, jobId)                              ServerOnly — RtsUnitLogic.SpawnUnit 끝에서 호출(훅)
  내 보유 중 target 0인 그 직업 프리즘이 있으면 ApplyPrism → target = no  (Phase 5 영입 때 살아나는 자리. 시험대 시연 유닛 스폰에도 그대로 동작)

읽기(서버·클라 공용 — SyncTable 파싱)
  GetOwned(userId) → { {seq,id,grade,target} … } 순서대로
  GetAugmentsFor(zone, no) → 그 유닛(구역의 소유자 userId 역조회 = RtsZoneLogic.ZoneByUser)에 지정된 항목 { g, t, d } — 유닛 팝업 증강 탭·유닛 팝업 능력치·전투가 쓴다
  ApplyToStat(st, zone, no) → 지정된 능력치 증강을 합연산: st.flat += / st.pct += / st.crit += / st.critDmg += / st.bossAdd += ; crit 상한 100 (RtsUnitBuffLogic.ApplyToStat 형제 — 버프 다음에 호출)
  IsUnlocked(userId, key)
  CountUnassigned(userId) → HUD 배지

DevGrantNext()                                                Server(senderUserId), TestBench일 때만
  NextRound[userId] 커서의 칸을 Grant(등급, 라벨 "[4] 헤네시스 언덕" / "자쿰")하고 커서 +1. 32를 넘으면 무시. Phase 6에서 삭제
```

### 3. 3장 추첨 (계산형 — [CASES] 대상)

```text
Roll(userId, grade) → {idA, idB, idC}
  풀 = 그 등급 항목. 프리즘이면 풀에서 (이미 얻은 프리즘) 제외, 팬텀은 이미 해금이면 제외
  A = 가중치 추첨. B = 추첨하되 A와 같으면 다시(상한 없음 — 풀이 2개 이상이면 반드시 끝남). C = A·B와 다를 때까지
  풀이 3개 미만이면(이론상 프리즘 12−5 = 7이라 안 생김) 있는 만큼만 카드
  난수는 _UtilLogic:RandomDouble()(전투와 같은 출처) — 검증 케이스는 난수 대신 "제외 규칙"과 "서로 다름"을 확인한다
  브·실·골은 보유 여부와 무관(같은 항목을 여러 라운드에 걸쳐 여러 번 얻을 수 있음 — 합연산 중복)
```

### 4. 프리즘 오버레이 (RtsJobTableLogic.GetSkillsFor / GetStatFor)

```text
GetSkillsFor(u) = GetSkills(u.JobId)의 새 복사본에 u.Prisms의 각 id를 순서대로 적용한 표. GetStatFor(u) = GetStat에 같은 적용
  인레이지      레이징 블로우: hits 3, range +1, fx → 인레이지판(클립 71d8513c…·타격 b79cbdf6…·사운드 e794c138…·hitDelay 0.3/0.2 간격), stat.bossAdd +200
  홀리 유니티   RtsUnitBuffLogic bond 정의를 활성(lv 99 대신 "프리즘 보유" 조건), 스킬 목록에 target=true 항목 추가(팝업 셀렉트 박스가 뜨는 조건)
  거대화        스피어 버스터 range 6, ratio +29, stat.bossAdd +185
  애로우 레인   폭풍의 시 잠금 3(SetPermaLock) + 신규 액티브 "애로우 레인"(range 6, 54%×2, period 0.2, 연출 = 폭풍의 시 것 재사용 → 자산 오면 교체), stat.bossAdd +220
  트루 스나이핑 피어싱·스나이핑 잠금 3 + 신규 액티브(cd 2, range 6, 130%×10, 반드시 크리 = crit 100, 연출 = 스나이핑 표식 재사용), stat.bossAdd +135
  엘릭서        블리자드 cd 2 (after 3.0은 그대로 → 3초마다)
  템페스트      블리자드 bossHits 15, bossFinal 0.9 (RtsCombatLogic이 읽음)
  초월          도트 퍼니셔 구체 ratio +169, stat.bossAdd +335
  디바인 퍼니시먼트  엔젤레이 잠금 3 + 신규 액티브(range 3, 27%×1, period 0.2, 연출 = 엔젤레이 투사체 재사용), stat.bossAdd +1350
  풍마수리검    쿼드러플 스로우 ratio +20(쉐도우 파트너 ½ 유지), stat.bossAdd +360, 투사체 연출 키 교체(자산 오면)
  자유전직      새비지·메익 잠금 3 + 신규 액티브 2개(블레이드 토네이도 39%×24·카르마 퓨리 51%×15, cd 5, range 3, 같은 주기에 항상 동시 = 한 항목 "블레이드 토네이도 + 카르마 퓨리"로 묶어 타격 39 = 24+15를 순서대로), 각 bossAdd +575 → 합 +1150, 직업 표시명 "듀얼블레이드"(GetJobName이 Prisms를 보고)
  팬텀          유닛 표 변화 없음(해금 플래그)
잠금 문자열 길이: 프리즘이 스킬 항목을 추가하면 SkillLocks도 그 길이로 늘려 채운다(DefaultLocks가 GetSkillsFor 기준). 신규 액티브의 기본 잠금 = 사용(0)
전투(RtsCombatLogic.DoAttack)·유닛 팝업 스킬 탭·연출(CastFx의 skills[idx])·잠금 토글 — 지금 GetSkills(u.JobId)를 부르는 자리 전부를 GetSkillsFor(u)로 바꾼다(§1.7 — 옛 호출 남기지 않음)
```

### 5. 보스전 15타 집중 (RtsCombatLogic.DoAttack + RtsSkillFxLogic)

```text
대상 목록을 고른 뒤: 스킬에 bossHits가 있고 목록이 보스 1마리(IsBoss)뿐이면 → 목록을 그 보스 × bossHits로 채운다(15타 = 같은 대상 15회, 판정도 15회 따로·크리 따로)
  데미지 ×bossFinal(0.9) — damage.md ⑥ 최종 데미지 곱(증강으로 상쇄 안 됨)
  연출: CastFx 대상 이름 목록에 같은 이름 15개 → 마크(낙하 얼음) 15개가 그 자리에 조금씩 흩어져(±0.3칸 무작위) 떨어지고 타격 클립 15회
  보스가 아니면(사냥) 기존 그대로(15마리 각 1타). 다른 스킬엔 bossHits 없음
시험대: RtsDummy<zone>_1에 IsBoss = true(체력바 2.6) — 15타 집중 확인용. Phase 7 보스가 생기면 그쪽으로
```

### 6. 클라 팝업 (RtsAugmentPopupLogic — RtsPopupLogic 셸 위)

```text
RtsPopupLogic.Open("pick")   → 제목 "증강 선택 — <라벨>", 닫기 없음 → _RtsAugmentPopupLogic:BuildOffer(body, offer)
  카드 3장(등급 띠·배지·이름·효과 글자). 대상 칩 없음(사용자 결정). 카드 클릭 → 그 카드만 강조 + 하단 "이 증강 받기" 버튼 → RequestChoose(cardIdx)
  프리즘 카드: 직업 이름 표시("[썬콜 전용]"), 내가 그 직업을 안 가졌으면 "미보유 — 영입 시 적용" 회색 부제
RtsPopupLogic.Open("augment") → _RtsAugmentPopupLogic:BuildList(body, userId = 내가 보고 있는 구역의 주인)
  탭 전체/브/실/골/프리즘(개수), 목록 = GetOwned 순서(행: 배지·이름·효과·대상 "3. 팬텀" 또는 빨간 !), 스크롤(RtsUnitPopupLogic 스크롤 목록 꼴)
  상세: 등급·이름·효과·적용 유닛. 미지정 + 내 것이면 유닛 칩(내 구역 유닛, 직업명·번호) → 클릭 → 확인 문구("2. 팔라딘에 지정 — 바꿀 수 없음") → RequestAssign(seq, no). 지정 후 🔒
  관전(남의 구역) = 목록·상세만, 칩 없음
OnAugmentChanged(seq, why, userId) 클라
  why = "choose": pick 닫고 augment를 열어 seq 행 선택(프리즘·팬텀이면 열지 않고 토스트 "적용됨")  /  "assign": 열려 있으면 행 갱신
  HUD 증강 버튼 배지 = CountUnassigned(내 것) — 0이면 숨김
유닛 팝업(RtsUnitPopupLogic) 증강 탭 = GetAugmentsFor(zone, no) 실데이터, 능력치 = GetStatFor + 버프 + 증강 합산, 직업명 = 듀얼블레이드 반영
B 키: RtsPopupLogic의 미리보기 핸들러 삭제 → RtsAugmentPopupLogic이 TestBench일 때만 DevGrantNext 호출
```

### 7. 삭제 목록 (§1.7)

```text
RtsPopupLogic: BuildAugment/SelectAugTab/BuildPick/TogglePickChip/TakePick 본문과 예시 offers/units, Pick·AugTabs 프로퍼티, B 키 미리보기 → 전부 RtsAugmentPopupLogic으로 대체
RtsUnitBuffLogic.GetAugmentsFor 빈 스텁 → RtsAugmentLogic 위임 한 줄
RtsJobTableLogic 팔라딘 표의 "홀리 유니티 프리즘은 Phase 6에서" 주석·RtsUnitLogic.SetPermaLock 주석의 옛 프리즘 이름(광전사·일격필살·나도 던진다!) → 현재 이름으로
```

### 8. 밸런스 재계산 (#18 — 문서·스크립트)

```text
augcalc.py: TIERS를 augmentation.md I/II/III 값·개수 10/10/7로, 프리즘 = 그 직업 것(썬콜 2개·섀도어 자유전직 1개) 적용, 최고점 탐색 그대로
balance-detail '증강 반영' 절 재생성: 능력치 1개 가치 표, 프리즘 표, 32개 최고점 표·순위(썬콜 1위 허용 확인), 헤더의 "재계산 전" 문구 제거
```

---

## Test Cases
> Play Test 시나리오(`maker_save → logs(build) → play → logs·screenshot → stop`, CLI 러너 없음). 계산형은 Play 중 `maker_execute_script`(server_main)로 값을 찍는다. 시험대(시연 유닛 8기 + 순회 몬스터 100기) 위에서.

```
[CASES:GetGradeAt]   [4]→bronze · [8]→silver · [13]→gold · [5]→없음 · [115]→없음 · "자쿰"→prism · "주니어 발록"→없음 · GetSchedule() 길이 32, 등급 개수 10/10/7/5, 진행 순 정렬(첫 = [4] 브, 마지막 = 진 힐라 프리즘)
[CASES:Roll]         브론즈 1000회: 3장이 항상 서로 다름 · 나온 id는 전부 브론즈 12종 안 · 가중치 12/8/5 비율 ±3%p
[CASES:Roll]         프리즘, 보유 {엘릭서, 풍마수리검}: 1000회 동안 두 id 0회 · 3장 서로 다름 · 팬텀 해금 상태면 팬텀 0회
[CASES:Roll]         브론즈, 보유에 "약점 찾기 I" 3개 있어도 다시 나옴(중복 획득 허용)
[CASES:ApplyToStat]  유닛 A에 브 공+25 ×2·실 공+10% ×1·골 크확+15 ×1·실 보스+6% ×1 지정 → flat +50 · pct +10 · crit +15 · bossAdd +6 · critDmg +0
[CASES:ApplyToStat]  같은 유저의 미지정(target 0) 항목은 어느 유닛에도 0 · 유닛 B는 0 · 크확 합 120 → 100 상한
[CASES:Prism]        썬콜 Prisms "elixir" → GetSkillsFor 블리자드 cd 2 · "elixir,tempest" → bossHits 15·bossFinal 0.9 · 없음 → cd 15
[CASES:Prism]        히어로 "enrage" → 레이징 블로우 hits 3·range 3·bossAdd +200 / 보우 "arrowrain" → 폭풍의 시 잠금 3·새 액티브 1개·SkillLocks 길이 +1 / 섀도어 "dualblade" → 새비지·메익 잠금 3·GetJobName "듀얼블레이드"
[CASES:Choose]       Pending 없이 RequestChoose(1) → 보유 변화 없음 · 카드 4 → 무시 · 남의 userId로 위장 불가(senderUserId)
[CASES:Assign]       미지정 seq에 내 유닛 2 → target 2 · 다시 3 → 그대로 2 · 프리즘 seq → 무시 · 없는 유닛 9 → 무시
[SUCCESS] B 키 → "증강 선택 — [4] 헤네시스 언덕" 카드 3장(브론즈 띠), ESC·딤으로 안 닫힘, 카드 클릭 → 받기 → 증강창 자동 열림·그 행 선택·빨간 ! → 유닛 칩 클릭 → 🔒·유닛 팝업 증강 탭에 표시·능력치 총합 반영(공격력 +25면 팝업 공격력 +25)
[SUCCESS] B 연타 → 지급이 줄 서서 순서대로(카드 하나 고르면 다음 카드 뜸), HUD 증강 버튼 배지 = 미지정 개수
[SUCCESS] 6번째 지급(자쿰) → 프리즘 카드 3장(12종 중, 미보유 직업은 "영입 시 적용" 부제) → 엘릭서 선택 → 썬콜 블리자드가 3초마다(로그 간격) · 다음 프리즘 라운드 카드에 엘릭서 없음
[SUCCESS] 템페스트 선택 + 시험대 보스 1기(IsBoss) → 블리자드 15타가 보스 한 자리에(마크 15·데미지 숫자 15개), 데미지 = 1타 × 0.9
[SUCCESS] 인레이지 선택 → 히어로 레이징 블로우 3타·사거리 3·인레이지 클립/사운드 / 자유전직 선택 → 섀도어 팝업 직업명 듀얼블레이드, 새비지·메익 영구 잠금 알약, 5초마다 블토+카르마 39타
[SUCCESS] 팬텀 카드 선택 → 해금 플래그(IsUnlocked true), 유닛 변화 없음(영입은 Phase 5)
[SUCCESS] F2로 남의 구역 보기 → 증강 버튼 → 그 유저 목록만, 칩·받기 없음 / 32칸 다 지급 뒤 B → 아무 일 없음
[SUCCESS] 빌드 Error 0, 런타임 에러 없음(LEA 로그), 재접속 후 SyncTable로 증강창 복원
테스트 생략(위임형): 팝업 그리기·탭 색·스크롤(화면 확인), OnAugmentChanged 전달(RPC 배선), 밸런스 재계산 스크립트(문서 산출물)
```

---

## Response Codes
> 엔트리 포인트 결과 계약(HTTP 없음 — 서버 RPC는 void, 결과는 SyncTable·클라 알림으로)

| Entry | 성공 | 무시(조용히) | 부수 효과 |
|---|---|---|---|
| `Grant(userId, grade, label)` | Pending 생성 + `ShowOffer` | 등급 풀 비어 있음(로그) | Pending 있으면 Queue |
| `RequestChoose(cardIdx)` | 보유 +1, `OnAugmentChanged(seq,"choose")` | Pending 없음·번호 범위 밖·위장 | 프리즘: ApplyPrism/해금, Queue 다음 Grant |
| `RequestAssign(seq, no)` | target 설정, `OnAugmentChanged(seq,"assign")` | 남의 seq·이미 지정·프리즘·남의/없는 유닛 | 전투·팝업 능력치 즉시 반영(다음 공격부터) |
| `DevGrantNext()` | 32칸 커서 지급 | TestBench 아님·32 초과 | Phase 6 삭제 |
| `OnUnitSpawned(userId,no,job)` | 미보유 직업 프리즘 자동 적용 | 해당 없음 | Prisms 동기·영구 잠금 |
| `GetSkillsFor(u)`/`GetStatFor(u)` | 프리즘 반영 표 | Prisms 빈 문자열 = 직업 표 그대로 | — |

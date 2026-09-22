---
feature_goal: "증강·프리즘 — 라운드마다 정해진 등급의 증강 3택1, 능력치 증강은 유닛에 지정해 합연산, 프리즘은 직업 전용 스킬(12종)·팬텀 해금 (로드맵 Phase 4 #14~#18)"
domain: rts-base
api_method: "서버 RPC(senderUserId 검증) + 클라 알림 RPC(userId 마지막 인자) — RtsUnitLogic.RequestLevelUp/OnChanged와 같은 꼴 (RootDesk/MyDesk/RtsUnitLogic.mlua:165, :350)"
api_path: "RtsAugmentLogic: DevGrantNext / Grant(server) → OfferFx(client) / RequestChoose / RequestAssign → OnAugmentChanged(client). 표: RtsAugmentTableLogic. 팝업: RtsAugmentPopupLogic(RtsPopupLogic 셸 위)"
affected_data:
  - "RtsAugmentLogic.OwnedByUser (SyncTable userId → 보유 증강 직렬화 문자열: seq·id·대상 유닛) — 서버 권위, 전 클라 읽기"
  - "RtsAugmentLogic.UnlockByUser (SyncTable userId → 해금 플래그: 팬텀)"
  - "RtsUnitComponent.Prisms (@Sync string — 이 유닛에 적용된 프리즘 id 목록)"
  - "RtsUnitComponent.SkillLocks (영구 잠금 3 — 기존 RtsUnitLogic.SetPermaLock 경유)"
  - "서버 메모리: 유저별 진행 카운터(다음 지급 라운드), 대기 중인 3택1 제시(카드 3장)"
---

## Feature Description
증강은 이 게임의 유일한 랜덤 축이다(로드맵 Direction). 한 판에 **32개**(브론즈 10 / 실버 10 / 골드 7 / 프리즘 5)가 정해진 라운드에 지급되고, 매번 **3장 중 1장**을 고른다. 브~골은 능력치(약점 찾기 = 크리티컬 확률, 급소 찌르기 = 크리티컬 데미지, 무기 연마 = 공격력 +n, 전투 감각 = 공격력 %, 실버·골드는 보스 사냥꾼/거인 학살자 = 보스 공격시 데미지)로, 고른 뒤 **증강창에서 내 유닛 1기에 지정**해야 효과가 난다(전부 합연산 — damage.md ①~④). 프리즘은 **직업 전용 스킬 12종 + 영웅 팬텀 영입**으로, 해당 직업 유닛의 스킬 표를 바꾼다(사거리·비율·타격 수·쿨·보스%·영구 잠금·연출).

아직 스테이지가 없으므로(Phase 6) 지급 트리거는 **개발용**(B 키 = 다음 라운드 지급)으로 두고, Phase 6에서 스테이지 전환 이벤트에 붙인다. 정의 원본은 `.info/augmentation.md`(항목·가중치·라운드표)와 `.info/character.md`('종류: 프리즘' 항목 + 자유전직이 주는 액티브 2종), 계산 규칙은 `.info/damage.md`.

기존에 서 있는 것(재사용): 증강 목록 팝업·3택1 팝업 껍데기(`RtsPopupLogic.BuildAugment/BuildPick`, RootDesk/MyDesk/RtsPopupLogic.mlua:267, :330 — 예시 데이터), 유닛 팝업 증강 탭(`RtsUnitPopupLogic` → `RtsUnitBuffLogic.GetAugmentsFor` 빈 스텁, RtsUnitBuffLogic.mlua:118), HUD 좌하단 증강 버튼(RtsHudLogic.mlua:255), 스킬 영구 잠금 3(`RtsJobTableLogic.GetLock`·`RtsUnitLogic.SetPermaLock`, RtsUnitLogic.mlua:407), 서버 전투의 능력치 흐름 `GetStat → ApplyToStat(버프) → CalcStat`(RtsCombatLogic.mlua:236-238)과 유닛 팝업의 같은 흐름(RtsUnitPopupLogic.mlua:120-124).

## Entry Point
- Method: 서버 RPC / 클라 알림 RPC(기존 꼴)
- Path:
  - `RtsAugmentTableLogic` — `GetItems(grade)`, `GetItem(id)`, `GetSchedule()`(32칸: 몬스터 스테이지 번호 또는 보스 이름 → 등급), `GetGradeAt(round)`, `GetPrismIds()`
  - `RtsAugmentLogic`(서버) — `Grant(userId, grade, roundLabel)` → 카드 3장 결정 → 클라 `ShowOffer(cards, userId)`; `RequestChoose(cardIdx)`(senderUserId) → 보유 추가·프리즘 즉시 적용 → `OnAugmentChanged(seq, userId)`; `RequestAssign(seq, unitNo)`(senderUserId) → 대상 지정 → `OnAugmentChanged`; `DevGrantNext()`(senderUserId, 개발용) → 32칸 순서대로 다음 지급
  - 읽기(서버·클라 공용): `GetOwned(userId)`, `GetAugmentsFor(zone, no)`(유닛에 지정된 것), `ApplyToStat(st, zone, no)`(능력치 합연산), `IsUnlocked(userId, "phantom")`
  - `RtsJobTableLogic` — `GetSkillsFor(unitComp)` / `GetStatFor(unitComp)`: 직업 표에 그 유닛의 프리즘을 얹은 결과(전투·팝업이 이걸로 교체)
  - `RtsAugmentPopupLogic`(클라) — `BuildOffer(body)`(3택1), `BuildList(body)`(증강창: 탭·목록·상세·대상 지정)
- Request: 카드 번호(1~3) / 증강 seq + 유닛 번호. 전부 senderUserId로 소유자 검증, 잘못된 값은 조용히 무시(기존 `RequestLevelUp` 꼴 — RtsUnitLogic.mlua:350)
- Response: 없음(void). 결과는 SyncTable 갱신 + 클라 알림 RPC로 돌아온다

## Business Rules
1. **라운드 지급표**(augmentation.md 헤더, 2026-09-22 확정): 몬스터 스테이지 [4]~[114] 27자리(등간격 4.2칸)에 브·실·골 비례 혼합 — 브 [4·17·30·38·51·63·76·84·97·110] / 실 [8·21·34·42·55·68·80·89·101·114] / 골 [13·25·46·59·72·93·106]; 프리즘은 보스 라운드 자쿰·핑크빈·시그너스·루시드·진 힐라. [115] 쉬는 스테이지·그 외 보스엔 없음. 표는 코드가 아니라 테이블(`RtsAugmentTableLogic`)에만 산다.
2. **3장 뽑기(사용자 2026-09-22)**: A → B → C 순서로 그 등급 풀에서 가중치([n/100]을 상대 가중치로) 추첨. 이미 뽑힌 카드와 **같은 항목이면 다시 굴려** 3장은 서로 다르다. **프리즘은 12종 전부 노출**(내가 보유하지 않은 직업의 전용 프리즘도 카드로 나옴 — 고르면 그 직업을 영입해야 효과) + 영웅 팬텀 영입(이미 해금이면 제외). **이미 얻은 프리즘은 다시 안 나온다**(A부터 제외). 브·실·골은 **라운드를 넘어 같은 항목을 여러 번 얻을 수 있다**(합연산 중복 — 공격력 +3% 두 번 = +6%). 프리즘 풀 12에서 최대 5개를 얻으므로 항상 3장이 남는다.
3. **선택**: 3택1 팝업은 닫기 없음(딤·ESC 무시 — 기존 `pick` 규칙, RtsPopupLogic.mlua:56, :143). 서버가 제시한 카드 3장만 유효, 카드 번호 외 값은 무시. 고르면 보유에 추가되고 제시는 사라진다. 지급이 대기 중에 또 오면(개발용 연타·연속 보스) 줄을 서서 순서대로 제시.
4. **대상 지정**(브·실·골): 고른 직후 **증강창이 자동으로 열려 그 증강이 선택된 채** 대상 유닛(내 유닛 칩)을 고르게 한다. **지정 전엔 효과 없음**, 미지정은 등급 배지 뒤 빨간 !. 나중에 증강창에서 지정해도 된다(HUD 증강 버튼에 미지정 개수 배지). **1번만 지정, 지정 후 변경 불가(🔒)**. 지정 대상은 내 구역의 살아 있는 내 유닛만(관전 중 남의 유닛 불가 — 서버가 소유자·구역 검증).
5. **효과 적용**(damage.md): 지정된 유닛의 능력치 표에 합연산 — 공격력 +n은 ①(추가 공격력), 공격력 +%는 ②(직업 스킬 %와 합), 보스 공격시 데미지 +%는 ③(킷 보스 티어·블스아이·프리즘과 같은 풀), 크확·크뎀은 ④(크확만 상한 100). 서버 전투(`DoAttack`)와 유닛 팝업 능력치(적용 중인 총합)가 같은 함수로 얹는다. 파티 버프(`RtsUnitBuffLogic`)와는 별개 단계 — 순서는 버프 다음.
6. **프리즘 = 직업 전용**: 고른 순간 해당 직업 유닛이 있으면 그 유닛에 **자동 지정**(대상 선택 없음). 없으면 보유 목록에 "미보유 직업"으로 남고, 그 직업을 영입하는 순간 자동 적용(Phase 5 영입이 `RtsAugmentLogic:OnUnitSpawned` 훅을 부른다 — 이번 페이즈엔 훅 자리만). 유닛에 적용되면 `RtsUnitComponent.Prisms`에 id가 실리고, 스킬 표는 `GetSkillsFor/GetStatFor`가 그 프리즘대로 바꿔 준다. 영구 잠금이 딸린 프리즘(애로우 레인 = 폭풍의 시, 트루 스나이핑 = 피어싱·스나이핑, 디바인 퍼니시먼트 = 엔젤레이, 자유전직 = 새비지 블로우·메소 익스플로전)은 기존 `SetPermaLock`로 잠근다.
7. **프리즘 12종의 효과**(character.md 기준, 수치는 표에서 읽음):
   - 인레이지(히어로): 레이징 블로우 타격 2→3·사거리 +1·보스 +200%·연출 인레이지판(자산 확보됨: 71d8513c… / 타격 b79cbdf6… / 사운드 e794c138…)
   - 홀리 유니티(팔라딘): 대상 지정 스킬 활성(지정 유닛 최종 ×1.4, `RtsUnitBuffLogic` bond lv 99 → 획득 시 활성, 변경 쿨 3분 기존 BondNo 흐름)
   - 거대화(DK): 스피어 버스터 사거리 6·데미지 +29%·보스 +185%
   - 애로우 레인(보우): 폭풍의 시 영구 잠금 → 애로우 레인(사거리 6·54%×2·0.2초·보스 +220%)
   - 트루 스나이핑(신궁): 피어싱·스나이핑 영구 잠금 → 트루 스나이핑(쿨 2초·사거리 6·130%×10·반드시 크리·보스 +135%)
   - 엘릭서(썬콜): 블리자드 쿨 15 → 2초
   - 블리자드 템페스트(썬콜, 가칭): 보스전에서 블리자드 15타를 보스 1마리에게 반복 타격 + 보스 최종 ×0.9(곱) — 이 프리즘 전용 규칙(attack.md §3 보스 집중)
   - 초월(불독): 도트 퍼니셔 구체 +169%·보스 +335%
   - 디바인 퍼니시먼트(비숍): 엔젤레이 영구 잠금 → 디바인 퍼니시먼트(사거리 3·27%×1·0.2초·보스 +1,350%)
   - 풍마수리검(나로): 쿼드러플 스로우 +20%·보스 +360%·투사체 연출 교체(쉐도우 파트너도)
   - 자유전직 - 듀얼블레이드(섀도어): 직업명 표시 듀얼블레이드, 새비지·메익 영구 잠금 → 블레이드 토네이도(39%×24) + 카르마 퓨리(51%×15) 5초마다 항상 동시, 각 보스 +575%
   - 영웅 팬텀: 팬텀 영입 해금 플래그(Phase 5 영입 탭이 읽음). 유닛 대상 없음
   **연출 자산이 아직 없는 프리즘은 기존 스킬 연출을 그대로 쓰고**, 자산은 사용자가 주는 대로 같은 페이즈 Change로 교체한다(인레이지만 자산 확보).
8. **보스전 15타 집중**(템페스트): `RtsCombatLogic.DoAttack`이 대상을 고를 때, 대상이 보스 1마리뿐이고 스킬에 `bossHits`가 있으면 그 수만큼 같은 대상을 반복 타격(낙하 얼음 15개도 그 자리에), 최종 데미지에 `bossFinal`(0.9)을 곱한다. 다른 광역기엔 없음. 보스 개체는 Phase 7 — 이번 페이즈에선 시험대 몬스터에 `IsBoss`를 켜서 확인.
9. **관전 읽기 전용**(2026-09-19): 다른 유저 구역을 볼 때 증강창은 그 유저의 보유 목록을 보여 주되 지정·선택 불가, 3택1은 내 것만 뜬다. 서버는 senderUserId 외 유저의 데이터를 바꾸는 요청을 무시.
10. **개발용 트리거**: 클라 B 키 → `DevGrantNext` → 그 유저의 다음 라운드(32칸 순서) 지급. `RtsCombatLogic.TestBench`가 켜져 있을 때만 동작, Phase 6에서 스테이지 이벤트로 교체·삭제. `RtsPopupLogic`의 B 키 미리보기·예시 카드·예시 유닛은 삭제(§1.7).
11. **밸런스 재계산**(#18): augcalc를 I/II/III 값·10/10/7·프리즘 5(내 직업 것 + 팬텀 규칙)로 다시 돌려 balance-detail '증강 반영' 절을 새로 쓴다. 코드 아님 — 문서·스크립트.

## Notes
- 서버 권위: 지급·추첨·선택·지정·효과 전부 서버(`@ExecSpace("Server")`/`ServerOnly`). 클라는 표시·입력만. 전 클라가 남의 증강도 봐야 하므로(관전) 보유 목록은 `SyncTable<string,string>`(userId → 직렬화)로 내려간다 — `RtsUnitLogic.MesoByUser`와 같은 꼴(RtsUnitLogic.mlua:10).
- 유닛별 프리즘은 `RtsUnitComponent`의 @Sync 문자열 `Prisms`("elixir,tempest")로 — 팝업·전투·연출이 같은 값을 읽는다(SkillLocks와 같은 방식, RtsUnitComponent.mlua:44).
- 스킬 표는 지금 `GetSkills(jobId)`가 캐시 없이 매번 새 테이블을 만든다(RtsSkillFxLogic ProjIdx 키 사건, 2026-09-20) — 프리즘 오버레이도 매번 새 복사본에 얹으면 되고, 연출 라운드로빈 키는 RUID 문자열이라 영향 없음.
- 시험대(개발용)에서 검증: 시연 유닛 8기 + 무적 순회 몬스터 100기 위에서 B 키로 32라운드를 돌려 본다. 보스 15타는 몬스터 1기에 `IsBoss`를 켜서.
- 형제 문서 동기(workflow 메모리): 이 페이즈에서 바뀌는 수치 없음. 템페스트 이름이 확정되면 4개 문서 일괄 치환.

## Proposals (Codebase-Based)
- [x] 증강 팝업 내용을 `RtsPopupLogic`에서 떼어 `RtsAugmentPopupLogic`으로 — 유닛 팝업이 `RtsPopupLogic.Open("unit") → _RtsUnitPopupLogic:BuildBody(body)`로 위임하는 꼴 그대로(RtsPopupLogic.mlua:121). 셸(딤·패널·제목·닫기·ESC·한 번에 하나)은 그대로 재사용.
- [x] 능력치 합산은 `RtsUnitBuffLogic.ApplyToStat`(RtsUnitBuffLogic.mlua:104)의 형제로 `RtsAugmentLogic.ApplyToStat(st, zone, no)`를 두고, 전투(RtsCombatLogic.mlua:237)와 팝업(RtsUnitPopupLogic.mlua:123) 두 호출부에 한 줄씩 추가.
- [x] 프리즘의 스킬 표 변경은 `RtsJobTableLogic.GetSkillsFor(u)`/`GetStatFor(u)` 한 곳에서 — 전투·팝업·연출·잠금 문자열(DefaultLocks 길이)이 전부 여기서 나온 표를 쓴다. 직업표 원본(`GetSkillsRaw`)은 손대지 않는다.
- [x] 미지정 증강 배지: HUD 증강 버튼에 빨간 숫자(미지정 n) — 목업 v16 증강창의 "!" 규칙을 버튼까지 확장.
- [ ] (보류) 증강 획득 이력·통계 표시 — Phase 7 결과 화면에서.

## Decisions
- [x] 프리즘 라운드 후보 = **11직업 전용 전부 노출 + 팬텀 영입**(미보유 직업 것도 나옴, 꽝 가능) — 사용자 2026-09-22
- [x] 3장은 **서로 다른 항목**(A→B→C 순서로 중복이면 재추첨), 브·실·골은 라운드를 넘어 **중복 획득 허용**, 프리즘은 **한 번 얻으면 다시 안 나옴** — 사용자 2026-09-22
- [x] 브~골 대상 지정 = 고른 뒤 **증강창에서 지정**(카드엔 대상 칩 없음), 지정 전 효과 없음, 1회 지정·변경 불가 — 사용자 2026-09-22("그 중에서 선택하면 증강 창에서 증강 대상을 선택")
- [x] 계산형 유닛 3개(라운드→등급, 뽑기 제외 규칙, 합산→능력치)에 Play 중 값을 찍는 `[CASES]` 검증 — 사용자 "넣자"
- [x] 개발용 지급 트리거 = B 키(시험대에서만), Phase 6에서 제거 — 기존 미리보기 키 재사용(RtsPopupLogic.mlua:148)
- [x] 확률 = 상대 가중치(합 100 아니어도 됨). 블리자드 템페스트 `[?]`는 10으로 시작 — augmentation.md는 사용자가 재배분
- [x] 미보유 직업 프리즘을 고른 경우: 보유 목록에 남고 그 직업 영입 시 자동 적용(Phase 5 훅) — 후보 전부 노출 결정의 귀결

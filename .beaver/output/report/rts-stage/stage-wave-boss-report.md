# Report — 스테이지·웨이브·보스 (로드맵 Phase 6 + 7, + revision-1 증강 합류)

## Feature Summary
- **Feature**: 132 스테이지(몬스터 115 + 보스 17)를 방 전역 타이머로 진행하고, 구역마다 몬스터를 스폰·순환시키며, 보스 라운드·누적 110 탈락·클리어·결과까지 한 판을 완성. revision-1로 증강 3택1·증강 뽑기가 합류했고, build 중 사용자 지시로 밸런스 재설계·난이도 6단계·다시 하기 투표·UI 정리가 이어졌다.
- **Entry point**: `RtsStageLogic`(방 진행 상태머신: idle → countdown → running → ended) ← `RtsBootstrapLogic`(입장/퇴장) / `RtsWaveLogic`·`RtsBossLogic`(스폰) / `RtsRunResultLogic`(탈락·클리어·기록) / `RtsAugmentLogic`(지급·뽑기) / `RtsDifficultyLogic`(난이도)
- **Domain**: rts-stage

## Created/Modified/Deleted Files
| File | Change Type | Description |
|------|-----------|------|
| `RootDesk/MyDesk/RtsStageTableLogic.mlua` | created | 132 스테이지·몬스터 표(`tools/gen-stage-table.py` 생성 구간) — 체력·메소·방어율·자산 RUID·크기·피격 상자 |
| `RootDesk/MyDesk/RtsStageLogic.mlua` | created | 방 전역 진행(카운트다운 15초·'바로 시작'·라운드 타이머·쉬는 라운드·영입 칸 개방), 다시 하기 찬반 투표(과반·부결·20초) |
| `RootDesk/MyDesk/RtsWaveLogic.mlua` | created | 구역별 몬스터 스폰(체력 × 난이도 `HpMul`), 보스전 동안 일반 몹 보관·복귀 |
| `RootDesk/MyDesk/RtsBossLogic.mlua` | created | 보스 영역(4×5 고정·배치 불가) 등장·초읽기·60초 제한·여러 보스 |
| `RootDesk/MyDesk/RtsRunResultLogic.mlua` | created | 누적 110·보스 시간 초과 탈락, 비석·관전, 클리어 기록(최종 메소 = 보유 + 유닛 판매 30%, 난이도별 저장소 `RtsClearMeso_D<n>`·`RtsClearRecord_D<n>`, 테스트 모드는 저장 안 함) |
| `RootDesk/MyDesk/RtsAugmentTableLogic.mlua` | created | 증강 정의(브·실·골·프리즘), 합연산 적용 `ApplyToStatMul`·`TotalsMul`(티어 배율, 프리즘 등급 제외) |
| `RootDesk/MyDesk/RtsAugmentLogic.mlua` | created | 라운드 지급·3택1·대상 지정, 증강 뽑기(3,000 + 40/회, 브 75.5·실 15·골 4.5·프리즘 5% + 천장 +2%p/회, 판당 프리즘 최대 2) |
| `RootDesk/MyDesk/RtsDifficultyLogic.mlua` | created | 난이도 6단계(0.2·0.4·0.6·0.7·0.8·1.0 × 극악 곡선 `CurveAt`), 대기·카운트다운 난이도 막대 + '바로 시작', 정보 카드 '난이도 X' |
| `RootDesk/MyDesk/RtsMonsterInfoLogic.mlua` | created | 몬스터 정보 창(초상 — 칸 정중앙 맞춤·마스크, 체력, 방어율, 디버프 아이콘 '방어구 부수기') |
| `RootDesk/MyDesk/*.codeblock`(위 9종 + `RtsStageTableLogic`) | created | 새 Logic 등록(GUID·Name·Type 5) |
| `RootDesk/MyDesk/RtsDemoLogic.mlua`·`.codeblock` | deleted | 시연 몬스터(plan §10 삭제 목록) |
| `RootDesk/MyDesk/RtsJobTableLogic.mlua` | modified | 티어(1티어 4·2티어 5·서포터 2), 1티어 증강 배율 램프(자기 직업 프리즘 있을 때만 ×1→×3)·방어구 부수기, 2티어 약점 증강 ×2(프리즘 시)·팬텀 ×1.75, 보스 최종 → ⑤ 스킬 데미지 통합, 프리즘 설명 문구 |
| `RootDesk/MyDesk/RtsCombatLogic.mlua` | modified | ⑤ 보스 스킬 데미지 `bossMulAt`, 합연산 방어(방어구 부수기 차감), 테스트 모드 +100만, 시험대 제거 |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified | 정보 카드(라운드·시간·맵·난이도·메소·필드), 영입 버튼(우측·가능할 때만), 다시 하기·투표 패널, 증강 뽑기·도감 버튼, 효과음(`SpawnClick` 클릭음) |
| `RootDesk/MyDesk/RtsPopupLogic.mlua` | modified | 3택1·결과 팝업·증강 도감(등급 탭·프리즘 칩·펼치기)·열기/닫기 효과음 |
| `RootDesk/MyDesk/RtsUnitLogic.mlua` | modified | 영입은 진행 중에만(`RequestRecruitAt`), 라운드 메소 |
| `RootDesk/MyDesk/RtsUnitPopupLogic.mlua`·`RtsUnitBuffLogic.mlua`·`RtsUnitSelectLogic.mlua` | modified | 증강 탭 합계(티어 배율), 셋째 줄(티어·방어구 부수기), 오라 제거, 메뉴 열기음 |
| `RootDesk/MyDesk/RtsMonsterComponent.mlua`·`RtsTrackWalkerComponent.mlua`·`RtsUnitComponent.mlua`·`RtsSkillFxLogic.mlua`·`RtsZoneLogic.mlua`·`RtsBootstrapLogic.mlua` | modified | 몬스터 생애(사망 클립·사망음·보관), 트랙 순환, 보스 영역, 입장/퇴장 연결 |
| `tools/gen-stage-table.py`·`clear-sim.py`·`balance-calc.py`·`balance-table.py`·`difficulty-sim.py`·`route-sim.py`·`combo-check.py`·`*.json` | created | 표 생성기, 한 판 시뮬레이터(극악 곡선 보정), 밸런스 계산·표 |

## Tests Written
- CLI 테스트 없음(스택 규칙 — docs/testing.md). 검증은 Maker Play Test 시나리오 + 로그.
- 수치 검증 도구: `tools/clear-sim.py`(난이도별 클리어율 — 2,000판 기준 매우쉬움 70.0 / 쉬움 48.7 / 보통 41.9 / 어려움 30.3 / 매우어려움 18.4 / 극악 3.5%), `tools/gen-stage-table.py --check`(메소 합·편성·체력 계단 검산).

## Verification
- Play Test(2026-09-24 마지막 재시작): build 로그 스크립트 에러 0(알려진 `RectTileMapComponent` LEA-3035만), normal 로그로 카운트다운 15초 → 난이도 극악 → 바로 시작 1/1 → 1라운드 영입 → 다시 하기 투표 → 카운트다운 흐름 확인. 정보 카드 '난이도 극악', 뽑기 버튼 '프리즘 2/2 · 5%', 우측 '영입 가능 1' 스크린샷 확인.
- 몬스터 초상 정중앙: 시험 초상 3종(AspectOnly / NativeSize / NativeSize + 역보정)을 나란히 띄워 역보정이 칸 가운데에 오는 것을 스크린샷으로 확인 후 반영.
- 서버 권위: 메소 차감·뽑기·영입 배치·난이도 설정·체력 배율·방어구 부수기·기록 저장 전부 Server/ServerOnly, RPC는 `senderUserId` 검증.

## Remaining Issues
- 사용자 Play 확인 대기: 효과음, 증강 도감 프리즘 펼치기, 관전 시 난이도 막대 비노출, 여러 명 투표 패널, 몬스터 초상 정중앙.
- 쉬운 난이도의 루시드 벽(프리즘 없이 1티어가 루시드에 도달하는 판), 후반 일반 몹 체력 ×10~30 체감 — 플레이로 확인 필요.
- 순위 방식 변경 예정(사용자 2026-09-24: 어려움 이상 검은 마법사 4페이즈 클리어 횟수 순) — 로드맵에 등록.

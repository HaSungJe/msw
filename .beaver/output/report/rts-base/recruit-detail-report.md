# Report — 영입 상세 팝업 + 난이도 창 최상단

## Feature Summary
- **Feature**: 영입 목록 카드 → 직업 상세(기본 외형 · 설명 · 오각형 5축 5단계 · 50레벨·증강 없음 능력치 · [영입]/[취소]), 난이도 창 화면 최상단
- **Entry point**: `RtsPopupLogic.Open("recruitinfo")`(ClientOnly) — [영입] → `RtsUnitSelectLogic.BeginPlace(jobId)` / [취소] → `Open("recruit")`
- **Domain**: rts-base — spec `.beaver/output/spec/rts-base/recruit-detail-spec.md` · plan `.beaver/output/plan/rts-base/recruit-detail-plan.md`

## Created/Modified/Deleted Files
| File | Change Type | Description |
|------|-----------|------|
| `RootDesk/MyDesk/RtsPopupLogic.mlua` | modified | 영입 카드 전부 → `recruitinfo`, `BuildRecruitInfo` · `RecruitBlockReason` · `SpawnRadar`(바탕 그물 1장 + 직각삼각형 10장 + 테두리 5 + 점 5 + 라벨 5) · `Atan2`, `PendingJob`·`RadarWebRUID`·`RightTriRUID` |
| `RootDesk/MyDesk/RtsJobTableLogic.mlua` | modified | `GetConcept`(11직업 설명) · `BasicRange`(전투와 같은 기본 공격 사거리 규칙) · `GetRadar`(speed·range 계산, aug = 분류, boss·hunt = 계산기 상수) · `RatioLevel` · `LevelName` |
| `RootDesk/MyDesk/RtsUnitPopupLogic.mlua` | modified | `SpawnPreviewAt(parent, u, pos, size)` 분리 — `SpawnPreview`는 이걸 부름 |
| `RootDesk/MyDesk/RtsDifficultyLogic.mlua` | modified | 난이도 막대 y −88 → 0 |
| `tools/balance-calc.py` | modified | `--radar`(사냥 = 50레벨·증강 없음 40마리 DPS, 보스 잠재력 = 50레벨 + 자기 프리즘 + 마지막 보스 전 카드 43장 3택1 최선 몰아주기 → 최댓값 비율 80/60/40/20% 5단계, 상수 줄 출력) |
| `tools/gen-radar-assets.py` · `assets/textures/radar-web.png` · `right-tri.png` · README | created / modified | RtsRadarWeb `de902441…` · RtsRightTri `c62bf5fb…` |
| `docs/ui-screens.md` | modified | 좌표 표 F(난이도 0~80), 4.2 `recruit`·`recruitinfo` |

## Plan 대비 변경점
- 직업 설명 초안 중 보우마스터("사냥이 안정적")·불독("광역 사냥꾼")은 계산기 사냥 단계(매우 낮음)와 어긋나 문장을 고쳤다(`GetConcept`).
- 외형 칸: 두손검·창이 캐릭터 왼쪽으로 칸 밖에 나와(실측) 아바타를 칸 오른쪽으로 치우치고 170×240으로.
- 오각형 라벨이 아래 꼭짓점에 겹쳐 라벨 거리 r+40/26 → r+52/36.
- 사용자 피드백(같은 날): "보통/높음 이런 거 빼고 오각형의 정도로" → 축 이름만(`LevelName` 삭제) · "상세한 설명 필요 없어, 오각형에 기본 설명, 스킬 목록만" → 50레벨 능력치 줄 삭제, 오른쪽 = 스킬 목록(기본 표 "Lv n 이름"), 외형 아래 = 계열만
- 이어서 "가로 넓이 줄이고 캐릭터 모습 창 줄이고, 설명 제거, 스킬 클릭하면 상세 펼쳐지게, 직업명 가운데, 영입 → 선택" → 창 760×640, 외형 160×220, `GetConcept` 삭제, 스킬 목록 세로 스크롤 + 줄 펼치기(스킬 desc), 제목 가운데(이 창만), 버튼 [선택]
- 이어서 "누르면 설명 제거, 액티브·패시브 나누고 직업별 프리즘 증강도 — 스킬/패시브/프리즘 3개로" → 목록 안 구역 제목 줄 3개, 프리즘 = `GetPrisms`의 그 직업 것(팬텀은 '영웅 팬텀'), 설명 앞 "[프리즘] " 제거

## Verification
Maker(2026-09-25): 빌드 오류 0.
- [SUCCESS] 히어로 상세 — 외형·"모험가 · 전사 · 공격 속도 보통"·설명·오각형(공격 속도 보통 · 사거리 보통 · 증강 효율 매우 높음 · 보스 높음 · 사냥 매우 높음 — 축마다 값 위치 맞음, 채움 조각 경계 아주 옅게)·능력치(사거리 2칸 · 크리 0% · 크뎀 20% · 공격력 628 · 기본 40 · 레벨당 +12 · 공격력% 0%)·[영입][취소]
- [SUCCESS] 난이도 창이 화면 맨 위에 붙음
- 칸이 프레임마다 나눠 만들어져 상세가 약 1초 동안 차례로 채워진다(엔진 스폰 분산 — 메모리 msw-engine)
- 확인 전: [영입] → 발판 고르기 → 영입, [취소] → 목록, 보유·잠김 카드의 이유 줄 — 재시작 뒤 사용자 확인 중

## Remaining Issues
- 직업 설명 문구는 사용자 검토 대기(초안)
- 보스·사냥 단계는 계산기 상수 — 직업 수치가 바뀌면 `python tools/balance-calc.py --radar` 다시 돌려 `GetRadar` 표에 옮긴다

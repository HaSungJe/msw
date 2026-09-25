# Plan — 영입 상세 팝업 + 난이도 창 최상단

## Feature Summary
- **Feature**: 영입 목록에서 직업을 누르면 직업 상세 팝업(외형·설명·오각형 5축·50레벨 능력치 + 영입/취소), 난이도 창을 화면 최상단으로
- **Entry point**: `RtsPopupLogic.Open("recruitinfo")` (ClientOnly) — 영입 카드 클릭 → PendingJob → [영입] `RtsUnitSelectLogic.BeginPlace(jobId)` / [취소] `Open("recruit")`
- **Domain**: rts-base
- spec: `.beaver/output/spec/rts-base/recruit-detail-spec.md` · 메모리 workflow에 따라 코드 블록 대신 동작 설명

---

## Prerequisites
(없음 — 자산 2개 업로드는 build 1단계에서 한다. 예전 원형 마스크처럼 build 단계로)

---

## File List

| File | Action |
|------|------|
| `RootDesk/MyDesk/RtsPopupLogic.mlua` | modified — 영입 카드 클릭 → 상세, kind `recruitinfo`, `BuildRecruitInfo`, `SpawnRadar` |
| `RootDesk/MyDesk/RtsJobTableLogic.mlua` | modified — `GetConcept(jobId)`(설명), `GetRadar(jobId)`(5축 단계 상수), `LevelName(n)` |
| `RootDesk/MyDesk/RtsUnitPopupLogic.mlua` | modified — `SpawnPreviewAt(parent, u, pos, size)` 분리, 옛 `SpawnPreview`는 이걸 부름 |
| `RootDesk/MyDesk/RtsDifficultyLogic.mlua` | modified — 난이도 창 y −88 → 0 |
| `tools/balance-calc.py` | modified — `--radar`(사거리·보스·사냥 단계 계산 → 직업 표에 옮길 줄 출력) |
| `tools/gen-radar-assets.py` | new — 오각형 그물 PNG · 흰 직각삼각형 PNG |
| `assets/textures/radar-web.png` · `assets/textures/right-tri.png` · `assets/textures/README.md` | new / modified |
| `docs/ui-screens.md` | modified — 4.2 팝업 표 `recruitinfo`, 난이도 창 위치 |
| `RootDesk/MyDesk/RtsUnitSelectLogic.mlua` | unchanged — `BeginPlace` 그대로 |
| `RootDesk/MyDesk/RtsUnitLogic.mlua` | unchanged — 영입 서버 검증 그대로 |

---

## Design

### 1. 직업 표 — RtsJobTableLogic

```text
- GetConcept(jobId) → 설명 2~3줄(spec 초안 — 사용자 검토 뒤 확정한 문장). 없는 id는 ""
- GetRadar(jobId) → { speed, range, aug, boss, hunt } 각 1~5(5 = 매우 높음). 11직업 상수 표
    speed = GetBaseSpeed(50레벨 기본 공격 속도 이름)에서: 매우빠름 5 · 빠름 4 · 보통 3 · 느림 2 · 매우느림 1 — 상수로 적지 않고 계산
    aug   = 히어로·나이트로드·썬콜·보우 5 · 팬텀 4 · 섀도어·불독·신궁·다크 3 · 비숍·팔라딘 1 — TierOf 기반 계산(팬텀만 4)
    range·boss·hunt = tools/balance-calc.py --radar 출력값(상수 줄, 주석에 계산 날짜·기준)
- LevelName(n) → "매우 높음" "높음" "보통" "낮음" "매우 낮음"
- 실행 공간: 표 조회(서버·클라 공용 — 기존 GetStat 등과 같음)
```

### 2. 계산기 — tools/balance-calc.py `--radar`

```text
- 직업마다(11): 50레벨 kit(프리즘 없음) 기본 공격 사거리 · rotation_dps(사냥, 40마리, 증강 없음)
  · 보스 잠재력 = 50레벨 + 자기 프리즘 + 마지막 보스 시점까지 받을 증강 카드(cards_before 마지막 보스 번호)를 전부 그 유닛에 — 카드마다 best_of_3로 가장 효율 좋은 능력치 — 준 보스 DPS(방어 0)
- 축마다 전체 최댓값 비율 → 0.8/0.6/0.4/0.2 경계로 5~1
- 출력: 표(직업·원값·비율·단계) + 직업 표에 붙일 상수 줄
```

### 3. 자산 — tools/gen-radar-assets.py

```text
- radar-web.png 512×512 투명: 가운데 기준 정오각형(위 꼭짓점 위쪽) 5겹(단계 1~5, 반지름 = 단계 ÷ 5) 선(흰 α0.25, 바깥 α0.45) + 가운데 → 꼭짓점 축 5개(α0.25)
- right-tri.png 128×128 흰색: 직각 = 왼쪽 아래, 두 변 = 아래·왼쪽, 빗변 안티앨리어싱(4배로 그려 축소)
- 업로드: msw-mcp 새 리소스(sprite/etc) RtsRadarWeb · RtsRightTri → RUID를 RtsPopupLogic 프로퍼티에
```

### 4. 팝업 — RtsPopupLogic

```text
- 영입 목록 카드(BuildRecruit): 모든 카드에 클릭 → PendingJob = jid → Open("recruitinfo"). 흐림·'보유 중'·'잠김' 표시는 그대로
- Open: kind "recruitinfo" 900×620, 제목 = 직업 이름
- BuildRecruitInfo(body, W):
    왼쪽 위 아바타 칸 220×260 — _RtsUnitPopupLogic:SpawnPreviewAt(body, { JobId = jid, Skin = 0, Owner = 내 id }, 위치, 크기)
    아바타 아래: 계열(전사/궁수/마법사/도적/영웅 — GetJobGroup) · 공격 속도 이름
    오른쪽 위: 설명(GetConcept, 줄바꿈 허용 16px, ColInk)
    오른쪽 가운데: 오각형(SpawnRadar, 280×280) — 꼭짓점 위(공격 속도)부터 시계 방향 사거리 · 증강 효율 · 보스 · 사냥, 꼭짓점 밖에 "축 이름\n단계" 라벨(단계 색: 매우 높음 금색 … 매우 낮음 옅은 회색)
    오른쪽 아래: 능력치 줄(50레벨 · 증강 없음 표기) — 사거리 n칸 · 크리티컬 확률 x% · 크리티컬 데미지 y% · 공격력 기본 a · 성장 +b/레벨 · 50레벨 c · 공격력% d%
       (GetStat(jid, 50)의 crit·critDmg·pct·range(없으면 기본 공격 사거리 2), GetBaseAttack·GetAttackPerLevel, atk = base + per × 49 + flat)
    아래 가운데 버튼: [영입](영입 가능할 때만 — 목록과 같은 판정 canRecruit·unlocked·not ownedJob) → Close → BeginPlace(jid)
                      불가면 [영입] 자리에 이유 한 줄 · [취소] → Open("recruit")
- SpawnRadar(parent, center, radius, levels):
    바탕 uisprite = RtsRadarWeb(지름 2r)
    꼭짓점 Pi = center + r × 단계/5 × (sin θi, cos θi), θi = 72°·i (위 꼭짓점부터 시계 방향)
    삼각형 (center, Pi, Pi+1)마다 가장 긴 변에 수선 → 직각삼각형 둘 → 각각 RtsRightTri uisprite: 피벗 (0,0) = 직각 꼭짓점, 크기 (다리1 길이, 다리2 길이), 회전 = 다리1 방향 각도
       (다리1→다리2가 반시계가 되게 두 다리를 고른다 — 뒤집기 없이), 색 금색 α0.35
    테두리 = 흰 사각 스프라이트를 선분마다 늘리고 회전(두께 2, 금색), 꼭짓점 점 8px
    UI 회전 프로퍼티 이름은 build에서 mlua_api_retriever로 확인(UITransformComponent 회전 — 추측 금지, CLAUDE.md)
- 목록으로 돌아올 때(취소) 탭(모험가/영웅)은 PendingJob의 계열로 유지
```

### 5. 아바타 미리보기 — RtsUnitPopupLogic

```text
- SpawnPreviewAt(parent, u, pos, size): 지금 SpawnPreview 본문(uiempty + CostumeManager + AvatarGUIRenderer, 기본/월드 스킨) — anchoredPosition·RectSize만 인자로
- SpawnPreview(parent, u) = SpawnPreviewAt(parent, u, Vector2(92, −128), Vector2(120, 190)) — 유닛 정보 창은 그대로
- u 는 유닛 컴포넌트 대신 { JobId, Skin, Owner } 표도 받는다(읽는 칸이 그 셋뿐)
```

### 6. 난이도 창 — RtsDifficultyLogic

```text
- Build: RtsDiffBar 위치 Vector2(0, −88) → Vector2(0, 0)(위 가운데 앵커 그대로 — 화면 맨 위에 붙음). 주석 "영입 버튼 아래" → "화면 최상단(2026-09-25 사용자)"
```

---

## Test Cases

```
[CASES:radar-level]   비율 → 단계: 1.0 → 5 · 0.8 → 5 · 0.79 → 4 · 0.6 → 4 · 0.5 → 3 · 0.4 → 3 · 0.3 → 2 · 0.2 → 2 · 0.19 → 1 · 0 → 1   (balance-calc --radar 안 함수 — 파이썬으로 돌려 확인)
[CASES:radar-speed]   매우빠름 5 · 빠름 4 · 보통 3 · 느림 2 · 매우느림 1 · 증강: hero 5 · phantom 4 · shad 3 · bishop 1 · paladin 1
[SUCCESS]             영입 창 → 히어로 카드 → 상세(아바타 기본 세트 · 설명 · 오각형 5축 라벨 · 능력치 50레벨 값 = 유닛 정보 창 50레벨 값과 같음) → [영입] → 배치 모드(빈 발판 금색) → 발판 클릭 → 영입
[SUCCESS]             [취소] → 영입 목록(같은 탭)
[SUCCESS]             보유 중·잠김(팬텀) 카드 → 상세는 열리고 [영입] 대신 이유 줄
[SUCCESS]             오각형 모양: 공격 속도 매우 높음(보우)·매우 낮음 없음 확인, 삼각형 조각 사이 틈·겹침 없음(스크린샷)
[FAIL:validation]     영입 불가 상태(한도 참 · 보스 중 탈락 등)에선 [영입]이 없다 — 서버 검증(RequestRecruitAt)은 그대로
[SUCCESS]             난이도 창이 화면 맨 위에 붙음(카운트다운 동안)
[SUCCESS]             빌드 로그 오류 0

테스트 생략(위임형): SpawnPreview → SpawnPreviewAt 위임(유닛 정보 창 열어 외형 그대로인지 화면 확인으로 대신)
```

---

## Response Codes
| Code | Cause |
|------|------|
| 팝업 표시 | 영입 카드 클릭(모든 직업) |
| [영입] → 배치 모드 | 영입 가능(한도·진행 상태·생존·해금·미보유) |
| [영입] 없음 + 이유 줄 | 보유 중 / 잠김 / 지금 영입 불가 / 다음 영입 라운드 |
| [취소] → 영입 목록 | 항상 |

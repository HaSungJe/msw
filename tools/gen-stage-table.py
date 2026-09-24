# -*- coding: utf-8 -*-
"""스테이지·몬스터 표 생성기 (로드맵 Phase 6·7, 2026-09-23)

입력(로컬 .info — 커밋 안 함): monster-wave.md(132 스테이지) · monster.md(몬스터 247종 자산 RUID) · balance-detail.md(직업 DPS)
출력:
  1) RootDesk/MyDesk/RtsStageTableLogic.mlua 의 BEGIN GENERATED ~ END GENERATED 사이(스테이지·몬스터 표)
  2) .info/monster.md 몬스터별 체력·메소 칸 + 끝 '라운드별 체력·메소' 표
검산(하나라도 틀리면 아무것도 쓰지 않고 멈춤): 메소 합·편성 구조·레벨대 목표·오름세·체력 계단·보스 기준.

모델(사용자 확정 — spec .beaver/output/spec/rts-stage/stage-wave-boss-spec.md):
  - 메소: 총 768,000(듄켈 직전 6기 전원 50). 기본 곡선 = 몬스터 라운드 체력^ALPHA × 아케인리버부터 ×ARCANE_MUL × 유닛 2명 이하 구간 ×EARLY_MESO_MUL, 스페셜(보스 바로 앞 몬스터 라운드) ×2(SPECIAL_MUL_AT는 그 배율), 마리당 10메소 단위.
  - 레벨업 비용표 = LEVEL_COST_BLOCKS(RtsJobTableLogic.EnsureCosts와 같아야 함 — 검산).
  - 표준 빌드 = 번 메소를 다 쓴다: 이번 보스 레벨대 입구 → 다음 보스들 준비(지금 레벨대 끝까지만) → 남으면 지금 레벨대 끝까지, 가장 낮은 유닛부터. 영입 1·5·10·15·20·25.
  - 일반 체력 = 그 라운드 표준 빌드 라인 클리어 한계 × 테마 압박(라운드마다 한계를 따라감·줄지 않음, 테마가 바뀌면 +3% 이상, 한계 95% 상한, 아케인 첫 라운드 ≥ 직전 2배).
  - 일반 체력 배율 = × NORMAL_HP_MUL(2.3) — 모델 한계가 실제 플레이보다 낮다는 보정(메소 분배·보스 체력엔 영향 없음).
  - 보스 크기 = 세로 2.4~3.6유닛 맞춤 × 3(BOSS_SIZE_MUL).
  - 보스 체력 = 레벨대 조합 최적 보스딜 고점(10직업 배치 + 방어 + 받은 증강 가치를 가장 센 유닛 70%·나머지 30% 고르게, 프리즘은 스우(60)부터만 — 주니어 발록·자쿰·피아누스는 증강도 제외·기준 35%) × 60초 × 보스별 기준.
    검은 마법사 4페이즈 = 방어율 100%, '히어로+증강 / 팬텀+증강 / 방어구 부수기' 중 가장 약한 경로 × 60초 × 80%.
사용: python tools/gen-stage-table.py [--check]   (--check = 검산만, 파일 안 씀)
"""
import io, os, re, sys, json, math, copy, struct, uuid, itertools, tempfile, urllib.request, time

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFO = os.path.join(ROOT, ".info")
LUA = os.path.join(ROOT, "RootDesk", "MyDesk", "RtsStageTableLogic.mlua")
JOBLUA = os.path.join(ROOT, "RootDesk", "MyDesk", "RtsJobTableLogic.mlua")
CHECK_ONLY = "--check" in sys.argv

# ======================================================================== 상수(사용자 확정값)
TOTAL = 768000
SPAWN = 40
# 영입 칸이 열리는 순번(2026-09-23 사용자 "1→2는 기존대로 5, 자쿰 3 · 혼테일 4 · 핑크빈 5 · 시그너스 6" — 전엔 1·5·10·15·20·25)
RECRUIT_AT = [1, 5, 26, 43, 47, 56]
ARCANE = 65                       # 아케인리버 첫 라운드(풍화된 기쁨의 땅)
# 2026-09-23 영입 일정 변경(1·5·26·43·47·56 — 자쿰 전엔 유닛 2명)으로 재맞춤: 0.16·1.56 → 0.08·1.8 + 아래 EARLY_MESO_MUL·SPECIAL_MUL_AT
ALPHA, ARCANE_MUL = 0.08, 1.8     # 메소 기본 곡선(2026-09-23 체력 규칙 변경에 맞춰 0.101·1.67에서 재맞춤 — 자쿰 직전 남는 메소 ≤ 12%와 루시드 레벨대를 함께 만족)
SPECIAL = {9, 25, 28, 42, 46, 55, 59, 63, 88, 109, 113, 120, 126}   # 보스 바로 앞 몬스터 라운드
SPECIAL_MUL = 2.0
# 유닛 2명 이하 구간(1~25라운드) 메소 배율 — 자쿰 직전 2명이 다 쓸 수 있는 만큼(남는 메소 ≤ 12%)
EARLY_MESO_MUL = 0.5
# 보스 전날 보너스(스페셜 ×2 대신): 혼테일·핑크빈 ×4, 시그너스 ×6, 루시드 ×4 — 초반 메소를 줄인 만큼 시그너스(50 1명)·루시드(50 3명) 목표 레벨대에 닿게
SPECIAL_MUL_AT = {42: 4.0, 46: 4.0, 55: 6.0, 88: 4.0}
LEVEL_COST_BLOCKS = [(70, 8, 440), (350, 9, 1140), (470, 9, 1420), (630, 9, 1710), (6900, 9, 47580)]   # (일반, 칸 수, 벽)
TARGETS = [("자쿰", 26, [30, 30, 20, 20, 20, 20]), ("혼테일", 43, [40, 30, 30, 20, 20, 20]), ("핑크빈", 47, [40, 40, 30, 30, 30, 30]),
           ("시그너스", 56, [50, 40, 30, 30, 30, 30]), ("루시드", 89, [50, 50, 50, 40, 40, 40]), ("진 힐라", 121, [50, 50, 50, 50, 50, 40]),
           ("듄켈", 127, [50] * 6)]
STAGE_SEC = {"mob": 20, "boss": 60, "rest": 30}
THEMES = [("빅토리아", 1), ("플로리나 비치", 11), ("오르비스", 15), ("엘나스", 20), ("아쿠아리움", 27), ("아리안트", 30), ("마가티아", 33),
          ("리프레", 35), ("시간의 신전", 44), ("미래의 헤네시스", 48), ("에레브", 54), ("블랙헤븐", 57), ("세계수", 61),
          ("소멸의 여로", 65), ("츄츄 아일랜드", 74), ("레헬른", 82), ("아르카나", 90), ("모라스", 97), ("에스페라", 105),
          ("문브릿지", 111), ("고통의 미궁", 115), ("리멘", 122), ("검은 마법사", 128)]
ARCANE_T = 13
# 테마별 압박 = 그 라운드 표준 빌드 라인 클리어 한계 대비 몹 체력 비율(2026-09-23 사용자 "몬스터가 너무 약함, 유닛 레벨 오르는 것도 감안" →
#   테마 첫 라운드 고정 + 3% 계단을 버리고 라운드마다 한계를 따라가게, 아케인 전 0.14~0.40 → 0.30~0.45. 아케인 전 상한 ≈ 0.47(아케인 첫 라운드 2배 점프가 한계 95% 안에 들어가야 함))
PRESSURE = [0.30, 0.32, 0.34, 0.36,
            0.38, 0.39, 0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.45,
            0.86, 0.87, 0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.94]
# 일반 몬스터 체력 배율(2026-09-23 사용자 "일반 몬스터가 너무 약해서 긴장감이 없다, 몇 배는 올려야" → 3배) — 모델의 라인 클리어 한계가 실제 플레이보다 낮게 잡혀 있다는 보정.
#   모든 몬스터 라운드에 똑같이 곱하므로 메소 분배(체력 비율)·보스 체력은 그대로, 한계 검산도 같은 배율로 본다
NORMAL_HP_MUL = 2.3   # 3 → 2.3 (2026-09-23 사용자 "너무 높다, 2.3배 정도로")
# 보스 크기 배율(2026-09-23 사용자 "보스들은 크기 다 3배로. 크기가 커야 보스지") — 세로 2.4~3.6 맞춤 뒤 곱한다
BOSS_SIZE_MUL = 3.0
IN_THEME, UPTIME, CAP_LIMIT, ARCANE_MIN_JUMP = 0.03, 0.6, 0.95, 2.0
BR = [4, 17, 30, 38, 51, 63, 76, 84, 97, 110]; SV = [8, 21, 34, 42, 55, 68, 80, 89, 101, 114]; GD = [13, 25, 46, 59, 72, 93, 106]
PRISM_AT = [26, 56, 89]   # 자쿰·시그너스·루시드(받은 뒤 다음 보스부터) — 2026-09-23 사용자 "프리즘 3개로"(전 스우·진 힐라 포함 5개)
GAIN = {"b": 0.08, "s": 0.14, "g": 0.22}
# 받은 증강 가치 G의 분배(2026-09-23 사용자 "증강이 부족한 상황에도 고점 기준은 가혹 — 고르게 분배 + 가장 센 유닛 쪽 70%"):
#   가장 센 유닛에 G × 0.7, 나머지 유닛들에 G × 0.3을 고르게(이전: G 전부를 가장 센 유닛에)
AUG_TOP_SHARE = 0.7
# 보스 고점의 프리즘·증강(2026-09-23 사용자 "자쿰·피아누스 동네북 — 증강 없이도", "스우부터 군단장 — 겁나 쎄져야"):
#   시그너스까지는 프리즘 제외, 스우(순번 60)부터 프리즘 포함(이전 방식). NO_AUG_BOSSES는 증강도 제외(레벨만)
PRISM_BOSS_FROM = 60
NO_AUG_BOSSES = {10, 26, 29}
# 2026-09-23 사용자 "자쿰·피아누스는 동네북 수준": 주니어 발록·자쿰·피아누스 60/50/60% → 35%(레벨만, 증강·프리즘 없는 고점 대비)
BOSS_RATIO = {10: 0.35, 26: 0.35, 29: 0.35, 43: 0.50, 47: 0.50, 56: 0.50, 60: 0.55, 64: 0.55, 89: 0.55, 110: 0.55,
              114: 0.70, 121: 0.70, 127: 0.70, 129: 0.60, 130: 0.65, 131: 0.70, 132: 0.80}
# 검은 마법사 4페이즈 방어율 100 → 120(2026-09-23 사용자 "가드 크러쉬 %p 빼기, 4페이즈 방어율을 그만큼 더 올려") — 체력 계산은 팔라딘 40 가드 크러쉬 −20 가정(실질 100)
BOSS_DEF, BM4, BM4_DEF, BUSU_IGN = 50, 132, 120, 50   # 방어구 부수기 30 → 20(중복 적용) → 50(2026-09-23 사용자)
# 후반 보스 방어율·체력(2026-09-23~24 사용자 "루시드·윌은 조합·증강을 적당히 나누면 어떤 프리즘 조합이든 클리어 / 진 힐라는 방무가 더 높아 증강 투자 강요 /
#   듄켈은 그보다 조금 더 어렵게(최종 방어선) / 검마는 히어로 인레이지 + 홀리 유니티 + 프레이에 증강을 몰아주고 2등 딜러들이 방무를 올려 같이 쳐야 겨우 —
#   방무는 조금 조절하고 체력 비중을 늘려", 검마 클리어는 최적으로 해도 50% 미만):
#   방어율 = BOSS_DEF_AT, 체력 = LATE_HP(tools/difficulty-sim.py 몬테카를로 1만 판 보정 — 최적 플레이 생존 루시드 95 · 윌 93 · 더스크 88 · 진 힐라 78 ·
#   듄켈 62 · 검마 1~3 45/40/35 · 4페이즈 28%). 인레이지 + 홀리 유니티 판의 검마 클리어 약 80%, 둘 중 하나라도 없으면 0~30%. 전엔 175~300 방어율 벽이라 최적으로도 5% 미만
#   → 같은 날 "보스 방무 감소 하한치 — 그래야 골고루 분배": 남은 방어율 ≥ 방어율 × 0.3(RtsCombatLogic.BossDefFloor) 넣고 재보정 — 인레이지+홀리+템페스트 93% · 인레이지+홀리 72% · 인레이지만 0%
#   → 같은 날 "하한 50%, 방어율 +10"(하한 0.5) → "메이플식 곱연산 방무 — 방무가 하한이 높아도 깎아야 할 만큼 많다, 보조·본딜러 모두 방무가 많이 필요":
#     데미지 × (1 − (방어율 − 가드 크러쉬) × (1 − 총 방무)), 총 방무 = 1 − Π(1 − 방무). 하한 삭제(곱연산이라 방어를 완전히 못 없앤다)
#   → 같은 날 사용자 방어율 표: 스우·데미안 200 · 루시드·윌 250 · 진 힐라·듄켈·더스크 275 · 검은 마법사 300/300/325/350. 스우·데미안도 몬테카를로 보정 체력으로
#   → 같은 날 사용자 "합연산 + 증강 방무 삭제, 방무 새로 계산"(곱연산 폐기): 남은 방어율 = 방어율 − 가드 크러쉬 − 템페스트 방어 깎기 − 직업 방무(킷·프리즘만)
#     직업 방무(50레벨, 보스) 히어로 70 · 나로(풍마) 70 · 썬콜(템페스트) 15 · 보우·섀도어 50 · 팬텀 60 · 3티어 20(프리즘 35) → 보스 방어율을 스우 100 ~ 검마 4페이즈 150으로
BM4_DEF = 150
BOSS_DEF_AT = {60: 100, 64: 100, 89: 120, 110: 120, 114: 130, 121: 130, 127: 130, 129: 140, 130: 140, 131: 145, 132: BM4_DEF}
# 2026-09-24 사용자 난이도 표(주니어 발록 쉬움 · 자쿰 보통 · 피아누스 쉬움 · 혼테일·핑크빈 보통 · 시그너스 어려움(50레벨 프리즘 딜러 필수) · 스우·데미안 보통 ·
#   루시드·윌 어려움 · 더스크 보통 · 진 힐라 어려움 · 듄켈 매우 어려움 · 검마 1~3 매우 어려움 · 4페이즈 극악) → 보스 17개 전부 tools/difficulty-sim.py 6천 판 보정.
#   기준(같은 날 사용자 "최적 조합을 아는 사람 기준"): 최적 플레이. 시그너스까지 = 그 보스까지 온 판 중 통과율 쉬움 99 · 보통 95 · 어려움 88%(시그너스는 50레벨 프리즘 딜러 — 팬텀 포함 — 있는 판 기준),
#     핑크빈까지는 가장 약한 1% 판 여유 쉬움 ×1.6 · 보통 ×1.25. 스우부터 = 누적 생존 목표: 스우 60 · 데미안 50 · 루시드 35 · 윌 30 · 더스크 25 · 진 힐라 20 · 듄켈 15 ·
#     검마 1페이즈 10 · 2페이즈 = 1페이즈 넘으면 무조건(가장 약한 판 여유 ×1.1) · 3페이즈 5 · 4페이즈 3%
#   → 같은 날 직업 티어 재설계(1티어 히어로·나로·썬콜 / 2티어 보우·섀도어·팬텀 / 3티어 불독·신궁·다크나이트 / 4티어 팔라딘·비숍) + 합연산 방무 + 증강 방무 삭제 +
#     프리즘 보공 → 보스 공격 시 스킬 데미지 배율로 재보정(tools/difficulty-sim.py 티어 모드 6천 판 — 검마 클리어 판 = 썬콜 + 1티어 + 홀리 39% · 1티어 + 홀리 + 퍼니시 21% …)
#   이 표가 BOSS_RATIO·BOSS_HP_MUL(고점 모델)을 덮어쓴다
LATE_HP = {10: 50956, 26: 165126, 29: 312339, 43: 589497, 47: 759361, 56: 3790144, 60: 4634999, 64: 5014372, 89: 6868537, 110: 11036414, 114: 10260359, 121: 11376668, 127: 12209909, 129: 5237425, 130: 9522590, 131: 9934908, 132: 9113349}
# 50레벨 + 직업 프리즘의 보스 방무(곱연산 — 발할라 1 − 0.9 × 0.4 = 64 · 블스아이 60 · 거대화 25 · 풍마수리검 15 · 블리자드 템페스트 15)
JOB_IGN50 = {"히어로": 70, "팬텀": 60, "다크나이트": 50, "신궁": 50, "아크메이지(불·독)": 50, "나이트로드": 70, "아크메이지(썬·콜)": 70, "보우마스터": 70, "섀도어": 50}   # 합연산(2026-09-24 — 1티어 70 · 2티어 50 통일 · 팬텀 60)
# 보스 체력 배율(BOSS_RATIO에 곱함, 2026-09-23 사용자): "보스가 너무 쉽다, 자쿰 ~ 스우 이전까지 체력 2배" → "스우 이전 보스 30% 추가 증가"(2 × 1.3 = 2.6, 주니어 발록은 "그대로, 충분해"라 제외) / "스우·데미안 체력 30% 하락"
#   → 2026-09-23 사용자 "주니어 발록 25%, 자쿰 25%, 피아누스 100%, 혼테일 100% 증가": 10 = 1.25, 26 = 2.6 × 1.25, 29·43 = 2.6 × 2
#   → 2026-09-23 사용자 "스우 포함 이후 보스 체력 50% 증가": 스우·데미안 0.7 × 1.5 = 1.05, 루시드~검은 마법사 4페이즈 1.5
#   → 2026-09-23 사용자 "자쿰 체력 현재 기준 30% 추가 증가": 26 = 3.25 × 1.3 = 4.225
#   → 2026-09-23 사용자 "피아누스 체력 −40%": 29 = 5.2 × 0.6 = 3.12
#   → 2026-09-23 사용자 "자쿰 체력 50% 감소" → "아니다 35% 감소": 26 = 4.225 × 0.65 = 2.74625
#   → 2026-09-23 사용자 "자쿰 체력 3/4로" → "아니다 현재 대비 70%로": 26 = 2.74625 × 0.7 = 1.922375
#   → 2026-09-23 사용자 "피아누스·혼테일도 체력 각각 3/4로": 29 = 3.12 × 0.75 = 2.34, 43 = 5.2 × 0.75 = 3.9
#   → 2026-09-23 사용자 "자쿰 체력 8% 증가": 26 = 1.922375 × 1.08 = 2.076165
#   → 2026-09-23 사용자 "피아누스 체력 50% 증가": 29 = 2.34 × 1.5 = 3.51
#   → 2026-09-23 사용자 "자쿰 체력 10% 증가": 26 = 2.076165 × 1.1 = 2.2837815
#   → 2026-09-23 사용자 "피아누스 체력을 40%로 감소": 29 = 3.51 × 0.4 = 1.404
#   → 2026-09-23 사용자 "자쿰·피아누스 −5%, 혼테일·핑크빈·시그너스 체력 1/4": 26 = 2.2837815 × 0.95, 29 = 1.404 × 0.95, 43·47·56 × 0.25
# 2026-09-23 사용자 "핑크빈 체력 20% 증가": 47 0.65 → 0.78
# 2026-09-23 사용자 "혼테일 ~ 시그너스 보스 체력 30% 증가": 43 0.975 → 1.2675 · 47 0.78 → 1.014 · 56 0.65 → 0.845
#   → 같은 날 "혼테일 30% 증가 · 핑크빈 2배 · 시그너스 3.5배"(+30% 전 값 기준): 43 1.2675 그대로 · 47 0.78 × 2 = 1.56 · 56 0.65 × 3.5 = 2.275
BOSS_HP_MUL = {10: 1.25, 26: 2.169592425, 29: 1.3338, 43: 1.2675, 47: 1.56, 56: 2.275,
               # 2026-09-23 사용자 "그 위 보스들도 체력 1/2로": 스우~검은 마법사 4페이즈 전부 × 0.5
               # 2026-09-23 사용자 "스우 체력 3배, 데미안 2.5배" → 같은 날 "롤백, 방무로 조절하자": 0.525 그대로
               60: 0.525, 64: 0.525, 89: 0.75, 110: 0.75, 114: 0.75, 121: 0.75, 127: 0.75, 129: 0.75, 130: 0.75, 131: 0.75, 132: 0.62}
#   4페이즈(132)만 1.24: 기준 0.8 × 1.5 = 1.2면 세 경로(방무 조합) 중 약한 경로가 60초 안에 못 깬다(검산 '4페이즈 세 경로') — 깰 수 있는 최대(0.8 × 1.24 ≈ 0.99)
# 일반 몬스터 체력 추가 배율(2026-09-23 사용자 "주니어 발록 이후의 몬스터 체력 20% 증가") — 순번 MOB_HP_UP_FROM부터 NORMAL_HP_MUL에 곱한다(메소 분배 영향 없음)
MOB_HP_UP_FROM, MOB_HP_UP = 11, 1.2
# 일반 몬스터 방어율 %(2026-09-23 사용자 "일반 몬스터에도 방어율 — 자쿰 이후 10%, 핑크빈 이후 ~ 시그너스 이전 20%, 아케인리버 30%"):
#   27~46 = 10, 48~64 = 20(시그너스 뒤 블랙헤븐·세계수도 20 — 사용자 확정), 65~ = 30. 체력 모델엔 넣지 않음(방어율만큼 더 단단해짐)
#   → 2026-09-24 사용자 "일반 몬스터에서 방어율 다 빼자. 방무는 이제 보스 옵션이야": 전부 0(체력 모델엔 원래 안 넣었으니 체력은 그대로)
def mob_def(no): return 0
# 2026-09-23 사용자 "피아누스 이후 일반 몬스터 체력 20% 너프 — 너무 안 죽네": 순번 MOB_HP_DOWN_FROM(30)부터 ×0.8
#   → 같은 날 "피아누스 이후의 몬스터 체력 10% 감소": ×0.8 × 0.9 = ×0.72
MOB_HP_DOWN_FROM, MOB_HP_DOWN = 30, 0.72
def mob_hp_mul(no): return NORMAL_HP_MUL * (MOB_HP_UP if no >= MOB_HP_UP_FROM else 1.0) * (MOB_HP_DOWN if no >= MOB_HP_DOWN_FROM else 1.0)
# 여러 부위로 된 보스(2026-09-23 사용자 "혼테일 본체+머리+팔+날개+꼬리 모두"): monster.md의 기본·사망 애니메이션 = 몸통 부위(앞), 여기 부위들은 클라가 자식으로 같은 기준점에 겹쳐 그린다.
#   원작 혼테일은 부위 몹(8810002~8810009)이 한 자리에 나와 그림 기준점으로 맞물린다 — (기본, 사망, 그리기 순서 = 몸통 대비). 판정 상자·체력바 높이는 부위 전체를 합친 테두리
BOSS_PARTS = {
    "B04": [("6659702c6ff14ff0a3cb04566c47bd2a", "7647ecd34e254f67a27cbe2b25569d77", -7),   # 8810007 날개(몸통 포함)
            ("5db717ed98374211a768ec7bdb7de7de", "cf9fbab6876e4434a31cb926ad2ea0da", -6),   # 8810009 꼬리
            ("07aeccb6d2c749b595e5b252208e7165", "4f5df68e9e134bf89cc04b1e4d884259", -5),   # 8810008 다리
            ("ffbb3811965f45589e1875a14f64ffab", "3bcddb0d4ffd4df8b00fb8242b3f6db7", -4),   # 8810005 왼손
            ("7d52719f59154edd93342285462403ef", "d25dbbaa850445b68e4b6136de0eb0c1", -3),   # 8810006 오른손
            ("7636f71624a347b5a4b2783f03294882", "faa36bec27a143b187fcb35be6119cfe", -2),   # 8810002 머리A
            ("98eb69ffe2904d94bc5fe83f9e218239", "ae47432063e3458cad016e51dc56848b", -1)],  # 8810004 머리C
}
BM4_GUARD_ASSUMED = 20
PHANTOM50_BOSS = 25753
JOBS = ["히어로", "팔라딘", "다크나이트", "보우마스터", "신궁", "아크메이지(썬·콜)", "아크메이지(불·독)", "비숍", "나이트로드", "섀도어"]
SUNCOL = "아크메이지(썬·콜)"
PRISM_MUL = {"히어로": [4.1], "팔라딘": [1.0], "다크나이트": [2.9], "보우마스터": [3.1], "신궁": [2.9], SUNCOL: [25.6],
             "아크메이지(불·독)": [4.8], "비숍": [12.6], "나이트로드": [5.4], "섀도어": [12.0]}
FIELD_MOBS = 20   # 불독 포이즌(몹 1마리당) → 트랙 위 20마리 환산
# 배경음 이름(monster-wave.md '배경음: [sound-N]' = 공식 자산 표시 이름) → 오디오 RUID (2026-09-23 자산 검색으로 매칭 — 원작 경로 주석)
BGM_RUID = {
    "sound-1": "003396fbfcc44e00be0ac34fbaf77635",   # bgm46/wierldforestinthegirlsdream
    "sound-6": "02301b8112894626a78f8d517aada78a",   # bgm04/shinin'harbor
    "sound-7": "022d0be8aacf4cb19851c11eeebccb96",   # bgm25/cygnusgarden
    "sound-9": "03bffd70f38943bb9e39c210a6000b78",   # bgm32/thecolossalheart
    "sound-23": "0c319c21fac3449f972215750e3f5515",   # bgm49/conteminatedsea
    "sound-31": "113b6d2d1e064955b1711b617b904a25",   # bgm49/templeinthemirror
    "sound-49": "183b609d03ed43bdb3abb419bd9df933",   # bgm25/destructionperion
    "sound-86": "294d55f89c0241b6b1f708969284f750",   # bgm46/lachelntheillusioncity
    "sound-94": "2c1a8e32b0244da6a42e9067af541fed",   # bgm50/subterminalpoint
    "sound-108": "31d14710b2144ca18d355a8271f2bd32",   # bgm04/warmregard
    "sound-118": "35770accede249f09028bdda10eb5fa5",   # bgm46/cave of rest
    "sound-119": "3561723eb9c6443c9a42d5c9eeb2c8e7",   # bgm14/dragonload
    "sound-121": "35fc8f694a0c4d5abfaa0d9ced5dbe2b",   # bgm47/thetuneofazurelight
    "sound-122": "36da77695eaa4a7791d454aad85869b7",   # bgm50/worldhorizon
    "sound-127": "3926b48759d246dc8464a876ff7fa5ce",   # bgm00/florallife
    "sound-142": "428308f89b6e482ca285feec0aff6dd0",   # bgm16/remembrance
    "sound-148": "49375db3645c46e29c1f003d5a6d5946",   # bgm16/forgetfulness
    "sound-149": "49ec72e4b07c4a9589aa8331a9fc57a4",   # bgm40/battleonthedeck
    "sound-153": "4b1da5b941404fe89d2fd11e48c843cf",   # bgm45/climbing up the worldtree
    "sound-157": "4f16b0b4ffd54477a7dc02174626e155",   # bgm12/aquacave
    "sound-175": "55117072498b4e6bafcfe45da29cd1f8",   # bgm12/dispute
    "sound-194": "5e5d8653aab84efc9aef78698713d919",   # bgm50/lostspace
    "sound-204": "636ff098ea254d3a82e29e311f5be712",   # bgm49/warcloud
    "sound-214": "6ac20b63715b4701b318cbb5842ff1ff",   # bgm00/dragondream
    "sound-220": "6c85d2b102c74461afac455fa678215b",   # bgm46/chewchew maintheme
    "sound-234": "7272cf2a358e483bbe8ca83080ce3894",   # bgm45/pain and sorrow
    "sound-243": "764aa2962eda4610ad5351a1fc2a3199",   # bgm41/gravity lord
    "sound-244": "7671a665727041598c4a358060aeae40",   # bgm25/knightsstronghold
    "sound-248": "76c04a20cb924c17960b4c2f72db9473",   # bgm50/throneofdarkness
    "sound-255": "7a8f657721f7432fa0804dfbf2b8aadc",   # bgm01/ancientmove
    "sound-257": "7b302352b0614439861f89eda29fad3f",   # bgm12/deepsee
    "sound-261": "7ca2c33f65204582959207ac4c7c9870",   # bgm46/chewchew wildworld
    "sound-266": "7f12be7facb84f47b5a4bdbd79858d4a",   # bgm49/heartofsuffering
    "sound-273": "8228f7d5f8a04dfdb024acb1fd98b8ac",   # bgm47/thetuneofazurelight2
    "sound-288": "87ad51b138dc433ab652facf35564a62",   # bgm13/minar'sdream
    "sound-300": "8b57ad3bb40742a1b4955390bf14b36d",   # bgm48/memoryofkritias
    "sound-309": "8ddfa1a102e84ad4be587c789fe8e0d9",   # bgm49/soupoflife
    "sound-312": "8f12929a1da847c79c204595b319c7a5",   # bgm48/blackdungeon
    "sound-346": "9c09f187eeae4be2979e1d344b0925fe",   # bgm17/goldbeach
    "sound-348": "9d050024473c499fa428cd12d65e084c",   # bgm46/volcanic zone of extinction
    "sound-359": "a30bcecb4e1e4662b8b3d6dcb3191087",   # bgm50/theworld’send
    "sound-363": "a3e1d64b93824ddd809a9b81a2ded673",   # bgm49/depthofpain
    "sound-379": "a948300b1354453091ccda7a207535dd",   # bgm50/templeofdarkness
    "sound-388": "af3acec8784a4f80a0a354479b2132ff",   # bgm05/wolfwood
    "sound-391": "b08bfd8846d2478abe64fc8227a7c0f6",   # bgm35/hekaton
    "sound-392": "b096f4699a334cdbb084d78bf7f590a5",   # bgm16/repentance
    "sound-409": "b61f3fa5871841ba9a44ac7681f86817",   # bgm14/hotdesert
    "sound-437": "be5fb97e993e48b29e23b55ca2029610",   # bgm06/comewithme
    "sound-442": "bfa8c3e2a33f4e8d871e03df2737c304",   # bgm02/evileyes
    "sound-469": "c95980d20085430386ea588eda1cc746",   # bgm46/lake of oblivion
    "sound-502": "d51e7664c4724ea1a66d8ad4b46f34cc",   # bgm16/duskofgod
    "sound-504": "d58c658a7f3b4f4691200a4018f99e37",   # bgm48/swampofmemorymoras
    "sound-510": "d95d18fade5942838038c6343a00bad0",   # bgm46/clocktowerofnightmare
    "sound-531": "de5f1d1c7ed644b9a31a31d5c078ed31",   # bgm49/eternalswamp
    "sound-541": "e26ce82e1f9c404dbab50ec6683b4fac",   # bgm49/secretlabyrinth
    "sound-556": "eabdc2ee5dfc4c238104ab9607c3bb11",   # bgm05/hellgate
    "sound-561": "ecc11fe5cb074083bc27ad1334b727d0",   # bgm14/dragonnest
    "sound-564": "eee2a1be2908456cb09fae3921b04e94",   # bgm50/tearsoftheworld
    "sound-571": "f2677ea116ba4474bd80277b32545758",   # bgm14/caveofhontale
    "sound-583": "fb11514a2e2c4580af50d669264feb60",   # bgm49/ferociousbattlefield
}

# ======================================================================== 원본 읽기
def read(name):
    return io.open(os.path.join(INFO, name), encoding="utf-8").read()

def num(x):
    x = x.replace(",", "").strip()
    try: return float(x)
    except Exception: return None

# 직업 DPS 앵커(balance-detail.md 직업별 상세 표)
ANCH = {}
for sec in re.split(r"\n## ", read("balance-detail.md")):
    title = sec.split("\n")[0]
    job = next((j for j in JOBS if title.startswith(j + " ")), None)
    if job is None: continue
    rows = {}
    for l in sec.split("\n"):
        m = re.match(r"^\| (1|10|20|30|40|50) \|(.*)$", l)
        if not m: continue
        c = [x.strip() for x in m.group(2).strip().strip("|").split("|")]
        lv = int(m.group(1)); atk = num(c[0])
        if job == "아크메이지(불·독)":
            hunt = num(c[3]) * FIELD_MOBS; boss = num(c[4]) if num(c[4]) is not None else num(c[3])
        else:
            boss = num(c[5]); hunt = num(c[7])
        rows[lv] = (atk, boss, hunt)
    ANCH[job] = rows
assert len(ANCH) == 10, "balance-detail 직업 표 10개를 못 읽음: %s" % list(ANCH)
# 몬스터 체력 모델은 고정 스냅숏(tools/hp-model-anchors.json)의 직업 DPS를 쓴다 — 2026-09-23 사용자 "몬스터 체력은 유지, 다크나이트 공격력만 초반에 내린 것, 몬스터 건들지 마".
#   직업 밸런스(balance-detail 표)를 바꿔도 몬스터 체력·메소는 그대로. 몬스터를 직업 변경에 맞춰 다시 맞출 땐 그 파일을 지우거나 새로 찍는다
ANCH_FILE = os.path.join(ROOT, "tools", "hp-model-anchors.json")
if os.path.exists(ANCH_FILE):
    _snap = json.load(io.open(ANCH_FILE, encoding="utf-8"))["anchors"]
    ANCH = {j: {int(lv): tuple(v) for lv, v in rows.items()} for j, rows in _snap.items()}
    assert len(ANCH) == 10, "hp-model-anchors.json 직업 10개가 아님"
LVS = [1, 10, 20, 30, 40, 50]

def job_dps(job, L):
    r = ANCH[job]; a = max(x for x in LVS if x <= L)
    if a == L: return r[a][1], r[a][2]
    b = LVS[LVS.index(a) + 1]
    k = (r[a][0] + (r[b][0] - r[a][0]) * (L - a) / (b - a)) / r[a][0]   # 구간 안은 공격력만큼, 스킬은 벽에서
    return r[a][1] * k, r[a][2] * k

def job_boss(job, L):
    b = job_dps(job, L)[0]
    if job == "신궁" and L >= 30: b *= 1.66 + (1.18 - 1.66) * (L - 30) / 20   # 스나이핑
    return b

def job_hunt(job, L): return job_dps(job, L)[1]

ELIX = [False]
def job_hunt_cd(job, L):
    h = job_dps(job, L)[1]
    if job == "비숍" and L >= 20: h *= 4.33
    if job == "다크나이트" and L >= 50: h *= 1.15
    if job == SUNCOL and L >= 30: h *= (2.9 if (ELIX[0] and L >= 50) else 1.13)
    return h

def job_ign_boss(job, L):
    if job == "히어로": return 70 if L >= 50 else (10 if L >= 20 else (5 if L >= 10 else 0))   # 발할라 100 → 60(2026-09-23)
    if job == "아크메이지(불·독)": return 100 if L < 30 else 0
    return 0

def def_mult(job, L, no, extra=0):
    # 고점 모델은 방어 50 가정. 2026-09-24 곱연산으로 바뀌었지만 주니어 발록~시그너스 체력을 그대로 두려고 이 모델만 예전(합연산) 식 유지
    #   (게임에선 히어로 50레벨이 방어 50 보스에 1 − 0.5 × 0.36 = 82% — 예전 100%). 스우부터는 LATE_HP(몬테카를로)
    d = BOSS_DEF
    return 1 - max(0, d - job_ign_boss(job, L) - extra) / 100

def best_comp(levels, fn):
    used = set(); tot = 0; picks = []
    for L in sorted(levels, reverse=True):
        j = max((x for x in JOBS if x not in used), key=lambda x: fn(x, L))
        used.add(j); tot += fn(j, L); picks.append((L, j))
    return tot, picks

def avg_comp(levels, fn):
    return sum(sum(fn(j, L) for j in JOBS) / len(JOBS) for L in levels)

# 편성(monster-wave.md)
ST = []
for e in re.split(r"\n- \[", read("monster-wave.md"))[1:]:
    tag = e[:e.index("]")]; name = e[e.index("]") + 1:e.index("\n")].strip()
    mobs = re.findall(r"\[((?:M|B)\d+)\]", e)
    bgm = (re.search(r"배경음: \[([^\]]*)\]", e) or [None, ""])[1]
    kind = "boss" if tag == "보스" else ("rest" if not mobs and "쉬는" in e else "mob")
    ST.append({"tag": tag, "name": name, "kind": kind, "mobs": mobs, "bgm": bgm})
pool = []
for t in range(59, 66): pool += next(x for x in ST if x["tag"] == str(t))["mobs"]
next(x for x in ST if x["tag"] == "73")["mobs"] = pool
lasttag = 0
for i, s in enumerate(ST, 1):
    s["no"] = i
    if s["tag"].isdigit(): lasttag = int(s["tag"])
    s["tagmax"] = lasttag
    s["sec"] = STAGE_SEC[s["kind"]]
    s["special"] = s["kind"] == "mob" and i in SPECIAL
    t = max(k for k, (_, st0) in enumerate(THEMES) if i >= st0); s["t"] = t; s["theme"] = THEMES[t][0]

# 몬스터(monster.md)
MON = {}
for e in re.split(r"\n- \[", read("monster.md").split("\n# ── 라운드별 체력·메소")[0])[1:]:
    mid = e[:e.index("]")]
    name = re.sub(r"<!--.*?-->", "", e[e.index("]") + 1:e.index("\n")]).strip()
    f = lambda k: (re.search(r"- " + re.escape(k) + r": \[([^\]]*)\]", e) or [None, ""])[1].strip()
    MON[mid] = {"name": name, "walk": f("기본 애니메이션"), "die": f("사망 애니메이션"), "dieSound": f("사망 보이스"),
                "def": int(f("물리방어율") or 0)}

# ======================================================================== 레벨 비용·표준 빌드
COST = {}
lv = 1
for normal, n, wall in LEVEL_COST_BLOCKS:
    for _ in range(n): lv += 1; COST[lv] = normal
    lv += 1; COST[lv] = wall
assert lv == 50 and sum(COST.values()) == 128000, "레벨 비용표 합 ≠ 128,000"

def lo2hi(x): return 50 if x == 50 else x + 9
def units_at(no): return sum(1 for r in RECRUIT_AT if r <= no)

def build_spend(cum, no):
    n = units_at(no); lvls = [1] * n; left = [cum]
    def raise_to(g):
        while True:
            cand = [(lvls[i], i) for i in range(n) if lvls[i] < g[i]]
            if not cand: return True
            _, i = min(cand); c = COST[lvls[i] + 1]
            if c > left[0]: return False
            left[0] -= c; lvls[i] += 1
    k = next((i for i, (_, cno, _) in enumerate(TARGETS) if cno >= no), len(TARGETS) - 1)
    for i in range(k):
        if not raise_to(TARGETS[i][2][:n]): return lvls, left[0]
    cap = [lo2hi(x) for x in TARGETS[k][2][:n]]
    if not raise_to(TARGETS[k][2][:n]): return lvls, left[0]
    for j in range(k + 1, len(TARGETS)):
        if not raise_to([min(a, c) for a, c in zip(TARGETS[j][2][:n], cap)]): return lvls, left[0]
    raise_to(cap)
    return lvls, left[0]

def aug_counts(tagmax):
    return (sum(1 for t in BR if t <= tagmax), sum(1 for t in SV if t <= tagmax), sum(1 for t in GD if t <= tagmax))

# ======================================================================== 보스 고점
def peak(levels, no, tagmax):
    b, s, g = aug_counts(tagmax)
    G = b * GAIN["b"] + s * GAIN["s"] + g * GAIN["g"]
    if no in NO_AUG_BOSSES: G = 0
    P = sum(1 for r in PRISM_AT if r < no) if no >= PRISM_BOSS_FROM else 0
    lv = sorted(levels, reverse=True)
    base = {(j, L): job_boss(j, L) * def_mult(j, L, no) for j in JOBS for L in set(lv)}
    best = (0, None)
    for perm in itertools.permutations(JOBS, len(lv)):
        units = [(perm[i], lv[i], base[(perm[i], lv[i])]) for i in range(len(lv))]
        mult = [1.0] * len(units); opts = []
        for i, (j, L, bb) in enumerate(units):
            if L >= 50 and j != "팔라딘":
                acc = 1.0
                for m in PRISM_MUL[j]:
                    opts.append((bb * acc * (m - 1), i, m)); acc *= m
        opts.sort(reverse=True); used = 0; taken = {}
        for _, i, m in opts:
            if used >= P: break
            if PRISM_MUL[units[i][0]].index(m) > taken.get(i, 0): continue
            mult[i] *= m; taken[i] = taken.get(i, 0) + 1; used += 1
        vals = [units[i][2] * mult[i] for i in range(len(units))]
        top = max(vals); rest = sum(vals) - top
        if len(vals) > 1: tot = sum(vals) + top * G * AUG_TOP_SHARE + rest * G * (1 - AUG_TOP_SHARE) / (len(vals) - 1)
        else: tot = sum(vals) + top * G
        if tot > best[0]: best = (tot, [(u[0], u[1], round(mult[i], 2)) for i, u in enumerate(units)])
    return best, G, P

# ======================================================================== 수입·체력(반복 계산)
def income(hp):
    # 마리당 메소 = 기본 곡선(체력^ALPHA × 아케인 배율)을 10 단위로 반올림(오름세 유지) × 스페셜 2배.
    #   전체 배율 k는 합이 TOTAL 이상이 되는 가장 작은 값(이분 탐색) — 초과분은 반올림 한 단계 이내, 듄켈 직전 전원 50은 그대로
    rounds = [s for s in ST if s["kind"] == "mob" and s["no"] < 127]
    base = {s["no"]: max(hp[s["no"]], 1) ** ALPHA * (ARCANE_MUL if s["no"] >= ARCANE else 1.0) * (EARLY_MESO_MUL if units_at(s["no"]) <= 2 else 1.0) for s in rounds}
    mult = {s["no"]: (SPECIAL_MUL_AT.get(s["no"], SPECIAL_MUL) if s["special"] else 1.0) for s in rounds}
    def per_mob(k):
        return {no: int(round(k * b / 10)) * 10 for no, b in base.items()}
    def total(pm):
        return sum(int(pm[no] * mult[no]) * SPAWN for no in pm)
    lo, hi = 0.0, 1.0
    while total(per_mob(hi)) < TOTAL: hi *= 2
    for _ in range(80):                      # 합이 TOTAL 이상이 되는 가장 작은 배율(오름세를 깨지 않게 보정 없이)
        mid_ = (lo + hi) / 2
        if total(per_mob(mid_)) >= TOTAL: hi = mid_
        else: lo = mid_
    pm = per_mob(hi)
    return {no: int(pm[no] * mult[no]) * SPAWN for no in pm}

def compute(hp, with_boss):
    meso = income(hp)
    cum = 0; out = {}; last_t = None
    for s in ST:
        no = s["no"]; r = {"cum": cum, "meso": meso.get(no, 0)}
        lvls, left = build_spend(cum, no); r["lv"] = lvls; r["left"] = left; r["units"] = units_at(no)
        ELIX[0] = no > 26
        hb, picks = best_comp(lvls, job_hunt_cd)
        pray = 1.10 if any(j == "비숍" and L >= 30 for L, j in picks) else 1.0
        b, sv, g = aug_counts(s["tagmax"])
        r["cap"] = hb * pray * (1 + 0.01 * b + 0.02 * sv + 0.035 * g) * UPTIME * 20 / SPAWN
        r["capAvg"] = avg_comp(lvls, job_hunt) * UPTIME * 20 / SPAWN
        if s["kind"] == "mob":
            # 라운드마다 그 라운드 표준 빌드 한계 × 테마 압박(유닛 레벨이 오르는 만큼 따라 오름). 줄지 않음 · 테마가 바뀌면 직전 +3% 이상 · 아케인 첫 라운드 직전 2배 이상 · 한계 95% 상한
            t = s["t"]
            prevs = [out[x["no"]]["hp"] for x in ST[:no - 1] if x["kind"] == "mob"]
            want = r["cap"] * PRESSURE[t]
            if prevs:
                prev = max(prevs)
                if t != last_t:
                    want = max(want, prev * (1 + IN_THEME))
                    if t == ARCANE_T: want = max(want, prev * ARCANE_MIN_JUMP)
                else:
                    want = max(want, prev)
            r["hp"] = min(want, r["cap"] * CAP_LIMIT)
            last_t = t
        elif s["kind"] == "boss" and with_boss:
            ratio = BOSS_RATIO[no] * BOSS_HP_MUL.get(no, 1.0)
            (pk, comp), G, P = peak(lvls, no, s["tagmax"]); r["comp"] = comp
            r["peak"] = pk; r["ratio"] = ratio; r["hp"] = pk * 60 * ratio / len(s["mobs"])
            # 후반 보스(루시드~4페이즈)는 몬테카를로 보정 체력(LATE_HP — 한 마리당)
            if no in LATE_HP:
                r["hp"] = LATE_HP[no]
                r["late"] = True
        else:
            r["hp"] = 0
        out[no] = r; cum += r["meso"]
    return out

hp = {s["no"]: 1000 for s in ST}
for it in range(6):
    res = compute(hp, with_boss=False)
    hp = {no: r["hp"] for no, r in res.items()}
res = compute(hp, with_boss=True)
for s in ST:
    r = res[s["no"]]
    s.update(r); s["hp"] = int(round(r["hp"] * (mob_hp_mul(s["no"]) if s["kind"] == "mob" else 1)))

# 2026-09-23 사용자 "피아누스 이후 몬스터가 너무 안 죽는다 → 25 이후로 올라가는 상승폭 다 절반으로": 순번 RISE_FROM 뒤 일반 몬스터 체력 =
#   25라운드 체력 + (체력 − 25라운드 체력) × RISE_MUL. 원인은 모델의 히어로 40 사냥 딜(39 → 40에서 ×8.5)이 자쿰 뒤 최강 조합 한계를 3배로 올린 것.
#   체력 표시만 바꾸고 메소 분배(모델 체력^ALPHA)·보스 체력(고점 모델)은 그대로. 아케인 점프 검산은 되돌린 값(unrise)으로 본다
RISE_FROM, RISE_MUL = 25, 0.5
RISE_BASE = next(x["hp"] for x in ST if x["no"] == RISE_FROM)
def unrise(no, hp): return RISE_BASE + (hp - RISE_BASE) / RISE_MUL if no > RISE_FROM and hp > RISE_BASE else hp
for s in ST:
    if s["kind"] == "mob" and s["no"] > RISE_FROM and s["hp"] > RISE_BASE:
        s["hp"] = int(round(RISE_BASE + (s["hp"] - RISE_BASE) * RISE_MUL))

# ======================================================================== 몬스터 크기(CDN 클립 파일)
CDN = "https://mod-resource.dn.nexoncdn.co.kr/"
CACHE = os.path.join(tempfile.gettempdir(), "msw-gen-stage-cache"); os.makedirs(CACHE, exist_ok=True)

def cdn(path):
    fn = os.path.join(CACHE, path.replace("/", "_"))
    if os.path.exists(fn): return open(fn, "rb").read()
    for k in range(3):
        try:
            b = urllib.request.urlopen(CDN + path, timeout=30).read(); open(fn, "wb").write(b); return b
        except Exception:
            if k == 2: raise
            time.sleep(1)

def clip_frames(ruid):
    b = cdn(f"{ruid[:2]}-animationclip/{ruid[2:4]}/{ruid}.win.mod")
    fr = [(uuid.UUID(bytes_le=m.group(2)).hex, struct.unpack("<f", m.group(1))[0]) for m in re.finditer(rb"\x15(.{4})R.\n\x10(.{16})", b, re.S)]
    return [(g, d if 0 < d < 10 else 0.1) for g, d in fr]

def varint(b, i):
    v = 0; sh = 0
    while True:
        c = b[i]; i += 1; v |= (c & 0x7F) << sh; sh += 7
        if not c & 0x80: break
    if v >= 1 << 63: v -= 1 << 64
    return v, i

def sprite_geom(g):
    b = cdn(f"{g[:2]}-sprite/{g[2:4]}/{g}.win.mod")
    i = 19; assert b[i] == 0x10; i += 2
    _, i = varint(b, i)
    assert b[i] == 0x08; w, i = varint(b, i + 1)
    assert b[i] == 0x10; h, i = varint(b, i + 1)
    ox = oy = 0
    if b[i] == 0x1a:
        ln, j = varint(b, i + 1); end = j + ln
        while j < end:
            tag = b[j]; val, j = varint(b, j + 1)
            if tag == 0x08: ox = val
            elif tag == 0x10: oy = val
    return w, h, ox, oy

# 아케인리버 몬스터 크기(2026-09-23 사용자 "리멘 쪽 몬스터 너무 작다" → "아케인리버 몬스터 위주로 너무 작은 것들은 키워 — 리본돼지 크기 기준, 이보다 작으면 이보다 크게"):
#   원본 그림에 빈 여백이 커서(리멘 330px 안팎) 높이 1.6 상한에 맞추면 몸이 작아 보였다. 보이는 테두리(tools/mob-visual.json — 이동 첫 프레임의 투명 제외 bbox px,
#   scratchpad mob_visual_bbox.py로 잼)의 가로·세로 기하평균(세계)이 리본돼지(M006)보다 작은 아케인리버 몬스터는 리본돼지 × MOB_VIS_UP이 되게 키운다
VIS_FILE = os.path.join(ROOT, "tools", "mob-visual.json")
MOB_VIS = json.load(io.open(VIS_FILE, encoding="utf-8")) if os.path.exists(VIS_FILE) else {}
MOB_VIS_REF, MOB_VIS_UP = "M006", 1.1
ARC_MOBS = {mid for _s in ST if _s["kind"] == "mob" and _s["t"] >= ARCANE_T for mid in _s["mobs"]}
REF_GM = [None]
def vis_gm(mid, sc):
    v = MOB_VIS.get(mid)
    if not v: return None
    return sc * math.sqrt(v["vis"][0] * v["vis"][1]) / 100

def monster_geom(mid, m):
    boss = mid.startswith("B")
    icon = ""
    try:
        fr = clip_frames(m["walk"])
        # 아이콘(2026-09-25 — 몬스터 아이콘 수집) = 크기 기준으로 쓴 그 프레임(첫 3프레임 중 가장 높은 것)의 스프라이트 → 표 box로 가운데 맞춤이 그대로 맞는다
        icon, (w, h, ox, oy) = max(((g, sprite_geom(g)) for g, _ in fr[:3]), key=lambda x: x[1][1])
    except Exception:
        w, h, ox, oy = (300, 300, 150, 0) if boss else (40, 30, 20, 0)
    try:
        die_sec = sum(d for _, d in clip_frames(m["die"])) if m["die"] else 0.6
    except Exception:
        die_sec = 0.6
    # 여러 부위 보스: 기준점 기준 테두리를 부위 전체로 넓히고(왼 −ox·오른 w−ox·아래 −oy·위 h−oy), 사망 길이 = 가장 긴 부위
    if mid in BOSS_PARTS:
        x0, x1, y0, y1 = -ox, w - ox, -oy, h - oy
        for pw, pd, _ in BOSS_PARTS[mid]:
            gw, gh, gx, gy = sprite_geom(clip_frames(pw)[0][0])
            x0, x1, y0, y1 = min(x0, -gx), max(x1, gw - gx), min(y0, -gy), max(y1, gh - gy)
            die_sec = max(die_sec, sum(d for _, d in clip_frames(pd)))
        w, h, ox, oy = x1 - x0, y1 - y0, -x0, -y0
    W, H = w / 100, h / 100
    if boss:
        wh = min(max(H * 2.0, 2.4), 3.6); sc = min(wh / H, 5.0 / W) * BOSS_SIZE_MUL
    else:
        wh = min(max(H * 2.5, 0.65), 1.6); sc = min(wh / H, 2.4 / W)
        if mid in ARC_MOBS and REF_GM[0]:
            gm = vis_gm(mid, sc)
            if gm and gm < REF_GM[0]: sc *= REF_GM[0] * MOB_VIS_UP / gm
    return {"icon": icon, "scale": round(sc, 3), "boxW": round(W * 0.7, 3), "boxH": round(H * 0.8, 3), "boxX": round((w / 2 - ox) / 100, 3),
            "boxY": round((h / 2 - oy) / 100, 3), "barY": round((h - oy) / 100 * sc + 0.15, 3), "dieSec": round(min(max(die_sec, 0.3), 3.0), 2)}

# 게임 안 표시 이름(2026-09-23 사용자 "검은마법사 2·3·4페이즈 텍스트 제거, 검은마법사라고만") — monster.md 이름은 그대로(페이즈 구분용)
DISPLAY_NAME = {"B16": "검은마법사", "B17": "검은마법사", "B18": "검은마법사"}
# 일반 몬스터 크기 배율(엔티티 스케일 = scale × size — RtsWaveLogic.SpawnMonsterEntity가 곱하고, 체력바·데미지 숫자 높이도 × size).
#   2026-09-25 사용자 "리프레 켄타우로스부터 2배 · 시간의 신전 3배 · 미래의 헤네시스 2배 · 황혼의 페리온 2배"
#   → 같은 날 크기 점검: "개조당한 안드로이드 수송차 2.5배, 개조당한 레이저 안드로이드·수리로봇·미사일 안드로이드·미사일 안드로이드 블루 1.5배"
MOB_SIZE = {}
for _n in range(79, 92): MOB_SIZE["M%03d" % _n] = 2     # 리프레 붉은 켄타우로스 ~ 죽은 용의 둥지
for _n in range(92, 98): MOB_SIZE["M%03d" % _n] = 3     # 시간의 신전
for _n in range(98, 109): MOB_SIZE["M%03d" % _n] = 2    # 미래의 헤네시스 · 황혼의 페리온
MOB_SIZE["M119"] = 2.5                                   # 개조당한 안드로이드 수송차
for _n in range(120, 124): MOB_SIZE["M%03d" % _n] = 1.5  # 개조당한 레이저 안드로이드 · 수리로봇 · 미사일 안드로이드 · 미사일 안드로이드 블루
# 같은 날 F3 점검: 타락마족 검병·도끼병 1.2 · 방패병은 검병·도끼병과 같은 크기(실제 배율 2.18·2.11 → 1.345 × 1.6 = 2.15) · 늑대기수 1.5,
#   분노·슬픔·즐거움·암석·화염·강인한 영혼의 에르다스 2 · 안식의 에르다스 3 · 아르마 2 · 아르마의 부하 1.2 · 파인디어·큰뿔 파인디어·유나나 1.3
MOB_SIZE.update({"M129": 1.2, "M130": 1.2, "M131": 1.6, "M132": 1.5, "M140": 3, "M141": 2, "M142": 1.2, "M143": 1.3, "M144": 1.3, "M145": 1.3})
for _n in range(134, 140): MOB_SIZE["M%03d" % _n] = 2    # 분노 · 슬픔 · 즐거움 · 암석 · 화염 · 강인한 영혼의 에르다스
# F3 다시 보기: 늑대기수 "현재 기준 1.3배"(1.5 × 1.3 = 1.95) · 기쁨의 에르다스 2 · 파인디어·큰뿔 파인디어 한 번 더 1.3배(1.3 × 1.3 = 1.69)
MOB_SIZE.update({"M132": 1.95, "M133": 2, "M143": 1.69, "M144": 1.69})
MOB_SIZE["M132"] = 2.24   # 늑대기수 "마지막으로 1.15배"(1.95 × 1.15)
# F4 점검: 램나나 ~ 종이봉투 뒷골목주민 1.3, 크릴라 · 족장 크릴라 · 버샤크 · 족장 버샤크 2
for _n in range(146, 164): MOB_SIZE["M%03d" % _n] = 1.3
MOB_SIZE.update({"M155": 2, "M156": 2, "M157": 2, "M158": 2})
# F5 점검: 나무판자 뒷골목주민 · 성난·광기의 무도회주민 · 춤추는 빨간구두 1.3, 약화된 클리너 · 클리너 2, 가고일 2종 ~ 비탄의 정령 2
for _n in range(164, 182): MOB_SIZE["M%03d" % _n] = 2
MOB_SIZE.update({"M164": 1.3, "M165": 1.3, "M166": 1.3, "M168": 1.3})
# F6 점검: 절망의 정령 2 · 기억속의 제네로이드 A·B형 ~ 강한 형님 1.3, 푸른 그림자 ~ 의식에 휘말린 망치병 2.3,
#   의식에 휘말린 마법사·궁병 2.3 · 아투인 · 아투스 · 벨라리온 · 벨라리스 2
MOB_SIZE.update({"M182": 2, "M183": 1.3, "M184": 1.3, "M185": 1.3, "M186": 1.3, "M187": 1.3})
for _n in range(188, 196): MOB_SIZE["M%03d" % _n] = 2.3
for _n in range(196, 200): MOB_SIZE["M%03d" % _n] = 2
# F7 점검: 아라냐 ~ 절망의 칼날 전부 2
for _n in range(200, 218): MOB_SIZE["M%03d" % _n] = 2
# F8 점검: 침묵의 기사 ~ 어센시온 전부 2
for _n in range(218, 230): MOB_SIZE["M%03d" % _n] = 2
for _n in range(225, 230): MOB_SIZE["M%03d" % _n] = 2.6  # 안세스티온 · 트랜센디온 · 포어베리온 · 엠브리온 · 어센시온 "여기서 1.3배 추가"(2 × 1.3)
# 표시 테마(게임 안 "지역 - 맵" · monster.md 라운드 표)만 바꾼다 — 체력 압박·아케인 구분(THEMES 순번 t)은 그대로(2026-09-25 사용자 "황혼의 페리온"):
#   미래의 헤네시스 뒤쪽 4개 맵(인적이 끊긴 남쪽 길 ~ 원혼의 땅)은 원작 황혼의 페리온 맵
DISPLAY_THEME = {50: "황혼의 페리온", 51: "황혼의 페리온", 52: "황혼의 페리온", 53: "황혼의 페리온"}
REF_GM[0] = vis_gm(MOB_VIS_REF, monster_geom(MOB_VIS_REF, dict(MON[MOB_VIS_REF]))["scale"])
for mid, m in MON.items():
    if not m["walk"]:
        raise SystemExit(f"monster.md {mid} {m['name']}: 기본 애니메이션 RUID 없음")
    m.update(monster_geom(mid, m))

# ======================================================================== 검산
errs = []
def check(cond, msg):
    if not cond: errs.append(msg)
mobst = [s for s in ST if s["kind"] == "mob"]
check(len(ST) == 132, "스테이지 132개 아님: %d" % len(ST))
check(all(s["bgm"] in BGM_RUID for s in ST), "RUID 매칭 안 된 배경음: " + ", ".join(sorted(set(s["bgm"] for s in ST if s["bgm"] not in BGM_RUID))))
check(sum(1 for s in ST if s["kind"] == "boss") == 17 and sum(1 for s in ST if s["kind"] == "rest") == 1 and len(mobst) == 114, "편성 종류 수")
check(len(next(s for s in ST if s["tag"] == "73")["mobs"]) == 8, "[73] 풀 8종 아님")
check(len(next(s for s in ST if s["name"] == "어둠의 신전")["mobs"]) == 2, "어둠의 신전 2체 아님")
check(all(mid in MON for s in ST for mid in s["mobs"]), "monster.md에 없는 몹 id")
check(all(MON[mid]["die"] for s in ST for mid in s["mobs"]), "사망 애니메이션 빈 몹")
check(TOTAL <= sum(s["meso"] for s in ST) <= TOTAL + 8000, "메소 합이 768,000 ~ 776,000 밖: %d" % sum(s["meso"] for s in ST))
check(all(s["meso"] % 400 == 0 for s in ST), "라운드 메소가 400 단위(마리당 10) 아님")
check(all(s["meso"] == 0 for s in ST if s["kind"] != "mob" or s["no"] >= 127), "보스·쉬는·듄켈 뒤 메소 ≠ 0")
for name, no, tgt in TARGETS:
    lv = sorted(ST[no - 1]["lv"], reverse=True)
    check(all(lo <= L <= lo2hi(lo) for L, lo in zip(lv, tgt)), f"{name}({no}) 표준 빌드 {lv} ≠ 목표 레벨대 {tgt}")
    if no < 127: check(ST[no - 1]["left"] <= 0.12 * max(ST[no - 1]["cum"], 1), f"{name}({no}) 남는 메소 > 12%")
basep = [s["meso"] / (SPECIAL_MUL_AT.get(s["no"], SPECIAL_MUL) if s["special"] else 1) for s in mobst if s["no"] < 127]
check(all(b2 >= b1 for b1, b2 in zip(basep, basep[1:])), "기본 메소 곡선이 줄어드는 곳 있음")
pre = [s for s in mobst if s["no"] < ARCANE and not s["special"]][-1]
check(ST[ARCANE - 1]["meso"] >= 1.8 * pre["meso"] - 400, "아케인 첫 라운드 메소 점프 < 1.8배")
for a, b in zip(mobst, mobst[1:]):
    # 피아누스 뒤 일반 몬스터 ×0.8(MOB_HP_DOWN_FROM, 사용자 요청)은 그 경계에서 한 번 내려가는 게 의도 — 그 한 쌍만 비율을 빼고 본다
    if a["no"] < MOB_HP_DOWN_FROM <= b["no"]:
        check(b["hp"] / MOB_HP_DOWN >= a["hp"] - 1, f"몬스터 라운드 체력 감소 {a['no']}→{b['no']}(×{MOB_HP_DOWN} 경계 제외)")
        continue
    check(b["hp"] >= a["hp"], f"몬스터 라운드 체력 감소 {a['no']}→{b['no']}")
prev = max(unrise(s["no"], s["hp"]) for s in mobst if s["no"] < ARCANE)
check(unrise(ARCANE, ST[ARCANE - 1]["hp"]) >= ARCANE_MIN_JUMP * prev - 2, "아케인 첫 라운드 체력 < 직전 2배(상승폭 절반 전 값)")
check(all(s["hp"] <= CAP_LIMIT * s["cap"] * mob_hp_mul(s["no"]) + 1 for s in mobst), "라인 클리어 한계(×일반 체력 배율) 95% 초과 라운드")
for s in ST:
    if s["kind"] != "boss": continue
    if s["no"] in LATE_HP:
        if s["no"] < 127: continue
        # 증강 없이는 못 깬다: 인레이지 히어로 + 홀리 유니티(×1.4) + 프레이(×1.1) + 가드 크러쉬 20, 방무·딜 증강 0 → 60초 딜 < 체력(곱연산 방무)
        dps0 = job_boss("히어로", 50) * PRISM_MUL["히어로"][0] * 1.1 * 1.4 * max(0.0, 1 - max(0, BOSS_DEF_AT[s["no"]] - 20 - JOB_IGN50["히어로"]) / 100)
        if s["no"] >= 127: check(dps0 * 60 < s["hp"] * len(s["mobs"]), f"보스 {s['no']}: 증강 없이(인레이지 + 홀리 + 프레이) 깨짐")
    else:
        check(abs(s["peak"] * 60 * s["ratio"] / len(s["mobs"]) - s["hp"]) <= 1, f"보스 {s['no']} 체력 ≠ 고점×60×기준")
jl = io.open(JOBLUA, encoding="utf-8").read()
blocks_lua = "{ " + ", ".join("{ %d, %d, %d }" % b for b in LEVEL_COST_BLOCKS) + " }"
check(blocks_lua in jl, "RtsJobTableLogic.EnsureCosts 구간 표가 LEVEL_COST_BLOCKS와 다름: " + blocks_lua)
if errs:
    print("검산 실패 — 아무것도 쓰지 않음:"); [print("  -", e) for e in errs]; sys.exit(1)
print("검산 통과: 132 스테이지 · 몬스터 %d종 · 메소 %s · 보스 17" % (len(MON), f"{sum(s['meso'] for s in ST):,}"))
if CHECK_ONLY: sys.exit(0)

# ======================================================================== 출력 1) RtsStageTableLogic
def lstr(s): return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
def lnum(x): return ("%d" % x) if float(x).is_integer() else ("%g" % x)
L = ["\t-- BEGIN GENERATED", "\t-- tools/gen-stage-table.py가 생성 — 손으로 고치지 않는다", "\tmethod void LoadGenerated()",
     "\t\tself.RecruitAt = { " + ", ".join(str(x) for x in RECRUIT_AT) + " }", "\t\tself.Stages = {"]
for s in ST:
    d = BOSS_DEF_AT.get(s["no"], BOSS_DEF) if s["kind"] == "boss" else (mob_def(s["no"]) if s["kind"] == "mob" else 0)
    L.append("\t\t\t{ no = %d, tag = %s, name = %s, kind = %s, theme = %s, bgm = %s, sec = %d, hp = %d, meso = %d, special = %s, def = %d, mobs = { %s } }," % (
        s["no"], lstr(s["tag"]), lstr(s["name"]), lstr(s["kind"]), lstr(DISPLAY_THEME.get(s["no"], s["theme"])), lstr(BGM_RUID.get(s["bgm"], "")), s["sec"], s["hp"], s["meso"],
        "true" if s["special"] else "false", d, ", ".join(lstr(x) for x in s["mobs"])))
L.append("\t\t}"); L.append("\t\tself.Monsters = {")
for mid, m in MON.items():
    parts = ""
    if mid in BOSS_PARTS:
        parts = ", parts = { " + ", ".join("{ walk = %s, die = %s, order = %d }" % (lstr(pw), lstr(pd), po) for pw, pd, po in BOSS_PARTS[mid]) + " }"
    if mid in MOB_SIZE: parts += ", size = " + lnum(MOB_SIZE[mid])
    if m.get("icon"): parts += ", icon = " + lstr(m["icon"])
    L.append("\t\t\t%s = { name = %s, walk = %s, die = %s, dieSound = %s, dieSec = %s, scale = %s, boxW = %s, boxH = %s, boxX = %s, boxY = %s, barY = %s%s }," % (
        mid, lstr(DISPLAY_NAME.get(mid, m["name"])), lstr(m["walk"]), lstr(m["die"]), lstr(m["dieSound"]), lnum(m["dieSec"]), lnum(m["scale"]),
        lnum(m["boxW"]), lnum(m["boxH"]), lnum(m["boxX"]), lnum(m["boxY"]), lnum(m["barY"]), parts))
L += ["\t\t}", "\tend", "\t-- END GENERATED"]
src = io.open(LUA, encoding="utf-8").read()
a = src.index("\t-- BEGIN GENERATED"); b = src.index("\t-- END GENERATED") + len("\t-- END GENERATED")
io.open(LUA, "w", encoding="utf-8", newline="\n").write(src[:a] + "\n".join(L) + src[b:])

# ======================================================================== 출력 2) monster.md 체력·메소 + 라운드 표
path = os.path.join(INFO, "monster.md"); md = io.open(path, encoding="utf-8").read()
MARK = "\n# ── 라운드별 체력·메소"
head = md[:md.index(MARK)].rstrip("\n") + "\n" if MARK in md else md.rstrip("\n") + "\n"
home = {}
for s in ST:
    if s["tag"] == "73": continue
    for mid in s["mobs"]: home.setdefault(mid, s)
def fill(block):
    mid = block[block.index("[") + 1:block.index("]")]; s = home.get(mid)
    if s is None: return block
    block = re.sub(r"(- 체력: )\[[^\]]*\]", lambda m: m.group(1) + f'[{s["hp"]:,}]', block, count=1)
    return re.sub(r"(- 메소: )\[[^\]]*\]", lambda m: m.group(1) + "[" + (f'{s["meso"] // SPAWN:,}' if s["kind"] == "mob" else "0") + "]", block, count=1)
parts = re.split(r"(?=\n- \[)", head)
head = parts[0] + "".join(fill(p) for p in parts[1:])
T = ["", "# ── 라운드별 체력·메소 (tools/gen-stage-table.py 생성 — Phase 6·7. 위 몬스터별 체력·메소 칸 = 처음 나오는 라운드 값. 모델은 spec stage-wave-boss / level.md)",
     f"# 메소: 총 768,000 · 체력^{ALPHA} 오름세 · 아케인리버 ×{ARCANE_MUL} · 스페셜(보스 바로 앞 라운드) ×2 · 마리당 10메소. 레벨업 비용표 = level.md",
     "# 일반 체력 = 라운드별 표준 빌드 라인 클리어 한계 × 테마 압박 × 일반 체력 배율(한계 대비 열) / 보스 체력 = 레벨대 조합 최적 보스딜 고점 × 60초 × 보스별 기준(방어율 50%, 검은 마법사 4페이즈 100% — 가장 약한 클리어 경로 기준)",
     "", "| 순번 | 태그 | 맵 | 테마 | 종류 | 유닛 | 체력 | 기준 | 마리당 메소 | 라운드 메소 | 누적 메소(시작 시) | 표준 빌드 레벨 |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
KIND = {"mob": "몬스터", "boss": "보스", "rest": "쉬는"}
for s in ST:
    kind = "**스페셜**" if s["special"] else KIND[s["kind"]]
    if s["kind"] == "boss" and len(s["mobs"]) > 1: kind = f'보스 ×{len(s["mobs"])}'
    basis = f'한계 {s["hp"] / s["cap"] / mob_hp_mul(s["no"]):.0%} ×{mob_hp_mul(s["no"]):g}' if s["kind"] == "mob" else ((f'몬테카를로 보정(방어 {BOSS_DEF_AT.get(s["no"], BOSS_DEF)})' if s.get("late") else f'고점 {s["peak"]:,.0f}의 {s["ratio"]:.0%}') if s["kind"] == "boss" else "-")
    T.append(f'| {s["no"]} | {s["tag"]} | {s["name"]} | {DISPLAY_THEME.get(s["no"], s["theme"])} | {kind} | {s["units"]} | {"-" if s["kind"] == "rest" else format(s["hp"], ",")} | {basis} | '
             f'{format(s["meso"] // SPAWN, ",") if s["kind"] == "mob" else "-"} | {s["meso"]:,} | {s["cum"]:,} | {"·".join(str(v) for v in sorted(s["lv"], reverse=True))} |')
io.open(path, "w", encoding="utf-8", newline="\n").write(head + "\n".join(T) + "\n")
print("썼음:", os.path.relpath(LUA, ROOT), "· .info/monster.md")

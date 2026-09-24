# -*- coding: utf-8 -*-
"""보스 난이도 몬테카를로 — 보스 17개 전부(2026-09-24 사용자 난이도 표):
   주니어 발록 쉬움 · 자쿰 보통 · 피아누스 쉬움 · 혼테일 보통 · 핑크빈 보통 · 시그너스 어려움(50레벨 프리즘 딜러 필수) · 스우 보통 · 데미안 보통 ·
   루시드·윌 어려움 · 더스크 보통 · 진 힐라 어려움 · 듄켈 매우 어려움 · 검은 마법사 1/2/3 매우 어려움 · 4페이즈 극악.
   기준(2026-09-24 사용자 "최적 조합을 아는 사람 기준으로 돌아가서 최종 클리어 10%"): 최적 플레이, 난이도 → 그 보스까지 온 판 중 통과율
     쉬움 99 · 보통 95 · 어려움 88 · 매우 어려움 78%, 극악(검마 4페이즈)은 최종 클리어가 FINAL(10%)이 되게 역산.
     → 같은 날 "스우~듄켈 생존율이 너무 높다": 스우부터는 누적 생존 목표(CUM)로 — 스우 60 · 데미안 50 · 루시드 35 · 윌 30 · 더스크 25 · 진 힐라 20 · 듄켈 15 ·
       검마 1페이즈 10 · 2페이즈 = 1페이즈 넘으면 무조건 통과(넘은 판 중 가장 약한 판 여유 ×1.1) · 3페이즈 5 · 4페이즈 3%
     핑크빈까지는 판마다 차이가 자쿰 프리즘 하나라 가장 약한 1% 판의 여유(60초 딜 ÷ 체력)로 — 쉬움 ×1.6 · 보통 ×1.25.
   (같은 날 시험한 '전체 판 중 깰 수 있는 비율 80/70/50/30/10% + 플레이 편차 σ 0.15'는 SIM_MODE=overall SIM_SKILL=0.15 SIM_PASS=... 로 재현)
   방어(2026-09-24): 메이플식 곱연산 방무, 보스 방어율 50(~시그너스) · 스우·데미안 200 · 루시드·윌 250 · 더스크·진 힐라·듄켈 275 · 검마 300/300/325/350, 일반 몬스터 0.

한 판: 프리즘 3번(자쿰·시그너스·루시드 뒤 3택1) + 브~골 27번(3택1) + 루시드 뒤 증강 뽑기(메소의 BUY_SHARE). IGN_FROM 라운드부터 방무(갑옷 꿰뚫기)가 나오면 고르고, 나머지는 딜.
  프리즘 고르기: 자쿰 = 인레이지 → 딜러 직업 프리즘(값 순) → 홀리 유니티 → 방어구 부수기(시그너스에 50레벨 프리즘 딜러가 필요),
               그 뒤 = 인레이지 → 홀리 유니티 → 방어구 부수기 → 딜러 직업 프리즘 → 팬텀 → 일격필살.
  편성: 영입 라운드(RECRUIT_AT)의 유닛 수 중 팔라딘(4명째~)·비숍(5명째~)은 서포터, 나머지 칸은 딜러 — 직업 프리즘을 받은 직업 먼저, 그다음 추천 루트(히어로 · 다크나이트 · 신궁 · 썬콜).
  레벨: 그 라운드 표준 빌드 레벨(높은 순) — 딜러가 위 칸(본딜 d1 · 부딜 d2 순), 서포터가 아래 칸. 가드 크러쉬 = 팔라딘 레벨(40~ 20, 10~ 10 — 스우부터는 20 가정), 프레이 = 비숍 30~.
  방무(곱연산 — 총 방무 = 1 − Π(1 − x)): 받은 방무 증강을 본딜·부딜에 나누는 방법 중 팀 딜 최대, 방어구 부수기(50, 겹침)는 본딜에 전부 또는 하나를 부딜에.
  딜 증강은 가장 센 딜러 70% · 나머지 30%, 홀리 유니티(팔라딘이 있을 때)는 가장 센 딜러 ×1.4.
출력: 보스별 체력(난이도 목표에 맞춘 값) · 통과율 · 누적 생존 · 여유 중앙값, 시그너스 프리즘 유무별 통과율, 조합별 검마 클리어율.
실행: python tools/difficulty-sim.py [판 수]   (SIM_DEF = 보스 방어율 덮어쓰기, SIM_IGNFROM = 방무 고르기 시작 라운드, SIM_PASS = 난이도별 통과율 dict)
"""
import io, os, re, sys, random, math
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
src = io.open(os.path.join(ROOT, "tools", "route-sim.py"), encoding="utf-8").read()
cut = src.index("# ---------------- (2) 탐색")
G = {"__name__": "diff", "__file__": os.path.join(ROOT, "tools", "route-sim.py")}
exec(compile(src[:cut], "route", "exec"), G)
ST, BOSS_DEF_AT, GEN = G["ST"], G["BOSS_DEF_AT"], G["G"]
bwp, ign_of, SUN, PH = G["boss_with_prism"], G["ign_of"], G["SUN"], G["PH"]
FP = "아크메이지(불·독)"
GAIN = GEN["GAIN"]
BOSSES = [s for s in ST if s["kind"] == "boss"]
DEF_OVR = eval(os.environ.get("SIM_DEF", "{}"))
DEFS = {s["no"]: DEF_OVR.get(s["no"], BOSS_DEF_AT.get(s["no"], GEN["BOSS_DEF"])) for s in BOSSES}
# 실험: 프리즘 가진 직업에 방무 더하기(SIM_CIGN — 곱연산), 원딜 배율(SIM_RAW), 방무 증강 값 배율(SIM_IGNMUL)·가중치 배율(SIM_IGNW)
CARRY_IGN = eval(os.environ.get("SIM_CIGN", "{}"))
RAW_MUL = eval(os.environ.get("SIM_RAW", "{}"))
IGN_MUL = float(os.environ.get("SIM_IGNMUL", "1"))
IGN_W_MUL = float(os.environ.get("SIM_IGNW", "1"))

# 난이도(2026-09-24 사용자) → 그 보스까지 온 판 중 통과율
LABEL = {10: "쉬움", 26: "보통", 29: "쉬움", 43: "보통", 47: "보통", 56: "어려움", 60: "보통", 64: "보통", 89: "어려움", 110: "어려움",
         114: "보통", 121: "어려움", 127: "매우 어려움", 129: "매우 어려움", 130: "매우 어려움", 131: "매우 어려움", 132: "극악"}
PASS = eval(os.environ.get("SIM_PASS", '{"쉬움": 0.99, "보통": 0.95, "어려움": 0.88, "매우 어려움": 0.78, "극악": 0.60}'))
MODE = os.environ.get("SIM_MODE", "cond")        # cond = 그 보스까지 온 판 중 통과율 / overall = 전체 판 중 깰 수 있는 비율
FINAL = float(os.environ.get("SIM_FINAL", "0.10"))   # cond에서 마지막 보스 통과율을 역산할 최종 클리어율(0이면 PASS 그대로)
SKILL_SD = float(os.environ.get("SIM_SKILL", "0"))
EARLY = {10, 26, 29, 43, 47}
MARGIN = {"쉬움": 1.6, "보통": 1.25}
CUM = eval(os.environ.get("SIM_CUM", '{60: 0.60, 64: 0.50, 89: 0.35, 110: 0.30, 114: 0.25, 121: 0.20, 127: 0.15, 129: 0.10, 130: "all", 131: 0.05, 132: 0.03}'))
PRISM_GATE = {56}   # 시그너스: 50레벨 프리즘 딜러 필수 — 직업 프리즘 없는 판은 (거의) 못 넘게


aug_src = io.open(os.path.join(ROOT, "RootDesk", "MyDesk", "RtsAugmentTableLogic.mlua"), encoding="utf-8").read()
POOL = {"bronze": [], "silver": [], "gold": []}
for m in re.finditer(r'\{ "(\w+)", "(bronze|silver|gold)", "[^"]*", ([0-9.]+), "(\w+)", ([0-9.]+) \}', aug_src):
    fam = m.group(4); w = float(m.group(3)); v = float(m.group(5))
    if fam == "ign": w *= IGN_W_MUL; v = min(95.0, v * IGN_MUL)
    POOL[m.group(2)].append((m.group(1), w, fam, v))
_bm = re.search(r'id = "core_ign".*?ign = (\d+)', aug_src)
BUSU = float(os.environ.get("SIM_BUSU", _bm.group(1) if _bm else "0"))   # 방어구 부수기(2026-09-24 삭제 — 없으면 0). SIM_BUSU = 실험
PRISM_POOL = {"core_final": 5, "core_boss": 5, "core_ign": 5, "phantom": 5, "dualblade": 5}
for j in ["enrage", "holyunity", "giant", "arrowrain", "truesnipe", "tempest", "transcend", "divinepunish", "fuma"]: PRISM_POOL[j] = 7.5
# 딜러 직업 프리즘(값 순 — 50레벨 프리즘 보스 딜) → 직업
JOB_PRISM = {"enrage": "히어로", "tempest": SUN, "dualblade": "섀도어", "fuma": "나이트로드", "truesnipe": "신궁", "giant": "다크나이트", "arrowrain": "보우마스터", "transcend": FP}
JOB_ORDER = list(JOB_PRISM)
FILL = ["히어로", "다크나이트", "신궁", SUN]   # 추천 루트 딜러
SHORT = {"enrage": "인레이지", "holyunity": "홀리", "tempest": "템페스트", "dualblade": "듀블", "fuma": "풍마", "truesnipe": "트루", "giant": "거대화",
         "arrowrain": "애로우", "transcend": "초월", "phantom": "팬텀"}
GVAL = {"bronze": GAIN["b"], "silver": GAIN["s"], "gold": GAIN["g"]}
GRADE_AT = {}
for s in ST:
    if s["kind"] != "mob": continue
    try: tag = int(s["tag"])
    except Exception: continue
    for grade, tags in (("bronze", GEN["BR"]), ("silver", GEN["SV"]), ("gold", GEN["GD"])):
        if tag in tags: GRADE_AT[s["no"]] = grade
MESO_AT = {s["no"]: s["meso"] for s in ST}
LV_AT = {s["no"]: sorted(s["lv"], reverse=True) for s in BOSSES}   # 그 라운드 표준 빌드 레벨(높은 순)
IGN_FROM = int(os.environ.get("SIM_IGNFROM", "44"))   # 혼테일 뒤부터 방무를 모은다(스우 방어율 200 대비)
BUY_FROM, BUY_SHARE = 90, 0.5

# ---------------- 직업 티어(2026-09-24 사용자): 1티어 히어로·나이트로드·썬콜 = 메인 격수(증강 효율 좋고 기본 스펙은 낮게 — 히어로·나로는 자기가 강하고,
#   썬콜은 블리자드 템페스트로 적중한 적의 방어율을 깎아 다른 격수를 돕는다) / 2티어 보우·섀도어·팬텀 = 기본 스펙 높고 증강 효율 낮음(고점 낮음) /
#   3티어 불독·신궁·다크나이트 = 2티어 하위 호환 / 4티어 팔라딘·비숍 = 서브(비숍 디바인 퍼니시먼트 = 받는 데미지 증가 + 개미딜).
#   "증강 잘 먹은 1티어 + 적절히 먹은 2티어 둘 + 4티어 하나"가 모여야 검마를 깬다.
#   TIER_ON이면 50레벨 보스 원딜(프리즘 있음 RAWP / 없음 RAW0 — 프리즘 전 레벨·사냥은 그대로), 50레벨 킷 방무 IGN_KIT, 프리즘 방무 IGN_PR, 증강 효율 AUG_EFF,
#   템페스트 방어율 감소 SHRED%, 디바인 퍼니시먼트 받는 데미지 VULN%로 계산. SIM_TP = 이 값들 덮어쓰기 dict
TIER_ON = os.environ.get("SIM_TIER", "1") == "1"
TIER = {"히어로": 1, "나이트로드": 1, SUN: 1, "보우마스터": 2, "섀도어": 2, PH: 2, FP: 3, "신궁": 3, "다크나이트": 3}
#   방어(2026-09-24 사용자 "합연산 + 증강 방무 삭제"): 남은 방어율 = 방어율 − 가드 크러쉬 − 템페스트 방어 깎기(SHRED %p) − 직업 방무 → 데미지 × (1 − 남은 ÷ 100)
#   직업 방무(50레벨, 보스) = IGN50(프리즘 없음) / IGN50P(프리즘 있음) — 50레벨 전은 route-sim ign_of(히어로 10 등)
TP = {
    "RAWP": {"히어로": 30000, "나이트로드": 30000, SUN: 25000, "보우마스터": 40000, "섀도어": 40000, FP: 28000, "신궁": 28000, "다크나이트": 28000},
    "RAW0": {PH: 40000, "보우마스터": 15000, "섀도어": 15000},
    "IGN50": {"히어로": 70, "나이트로드": 0, SUN: 0, "보우마스터": 50, "섀도어": 50, PH: 60, FP: 20, "신궁": 20, "다크나이트": 20},
    "IGN50P": {"히어로": 70, "나이트로드": 70, SUN: 15, "보우마스터": 50, "섀도어": 50, PH: 60, FP: 35, "신궁": 35, "다크나이트": 35},
    "AUG_EFF": {1: 1.3, 2: 0.6, 3: 0.6},
    "SHRED": 13, "VULN": 20, "GATE_Q": 0.7,
    "DEF": {60: 100, 64: 100, 89: 120, 110: 120, 114: 130, 121: 130, 127: 130, 129: 140, 130: 140, 131: 145, 132: 150},
}
TP.update(eval(os.environ.get("SIM_TP", "{}")))
if TIER_ON:
    for _no, _d in TP["DEF"].items():
        if _no in DEFS and _no not in DEF_OVR: DEFS[_no] = _d
    PRISM_POOL.pop("core_ign", None)   # 방어구 부수기 삭제(증강 방무 삭제)
def ign_add(j, L, p):
    # 합연산 방무(보스 상대): 50레벨이면 표(IGN50/IGN50P), 전이면 route-sim ign_of(프리즘 0 — 히어로 10 등)
    if L >= 50: return (TP["IGN50P"] if p else TP["IGN50"]).get(j, 0)
    return ign_of(j, L, 0, True) if j == "히어로" else 0

RAW = {}
def raw(j, L, p):
    k = (j, L, p)
    if k not in RAW:
        v = bwp(j, L, p) * RAW_MUL.get(j, 1.0)
        if TIER_ON:
            if p and j in TP["RAWP"]: v *= TP["RAWP"][j] / max(1.0, bwp(j, 50, 1))   # 프리즘 = 모든 레벨 비례
            elif not p and L >= 50 and j in TP["RAW0"]: v = TP["RAW0"][j]            # 50레벨 킷
        RAW[k] = v
    return RAW[k]
BASE = {}
def base_keep(j, L, p):
    # 기본 방무(발할라·블스아이·프리즘 등)의 남은 비율(1 − 방무)
    k = (j, L, p)
    if k not in BASE:
        if TIER_ON:
            keep = 1 - ign_of(j, L, 0, True) / 100
            if L >= 50: keep *= 1 - TP["IGN_KIT"].get(j, 0) / 100
            if p: keep *= 1 - TP["IGN_PR"].get(j, 0) / 100
            BASE[k] = keep
        else:
            i = ign_of(j, L, p, True)
            c = CARRY_IGN.get(j, 0) if (p or j == PH) else 0
            BASE[k] = (1 - i / 100) * (1 - c / 100)
    return BASE[k]
def aug_eff(j):
    return TP["AUG_EFF"].get(TIER.get(j, 0), 1.0) if TIER_ON else 1.0

def pick3(items):
    items = list(items); out = []
    for _ in range(3):
        if not items: break
        tot = sum(w for _, w in items); r = random.random() * tot
        for i, (k, w) in enumerate(items):
            r -= w
            if r <= 0: out.append(k); items.pop(i); break
    return out

def roll_normal(grade):
    ids = pick3([(a, w) for a, w, fam, v in POOL[grade]])
    return [next(x for x in POOL[grade] if x[0] == i) for i in ids]

# 영입: 히어로(1) · 다크나이트(5) · 3번째(26 — 신궁, 자쿰 프리즘이 없는 직업 것이면 그 직업으로 바꿈) · 팔라딘(43) · 비숍(47) · 6번째(56 — 썬콜).
#   그 뒤 받은 직업 프리즘·팬텀이 없는 직업 것이면 지금 있는 프리즘 없는 딜러 중 가장 늦게 뽑은 하나(레벨이 가장 낮음)와 바꾼다(다음 보스부터).
# 레벨: 시그너스 전(~47)은 영입 순서대로 표준 빌드 레벨(히어로·다크나이트끼리만 맞바꿈 가능), 시그너스부터는 딜러가 위 칸을 자유롭게(프리즘 딜러 50).
def swap_in(roster, job, held, units):
    if job in roster: return
    cand = [j for j in roster[:units] if j not in ("팔라딘", "비숍") and j not in held]
    if not cand: cand = [j for j in roster[units:] if j not in ("팔라딘", "비숍") and j not in held][:1]
    if not cand: return
    roster[roster.index(cand[-1])] = job

def lineup(roster, held, no):
    # → (딜러 {직업: 프리즘 0/1}, 레벨 배정 후보 목록[{직업: 레벨}] 또는 자유 배정 레벨, 가드 크러쉬, 프레이 배율, 팔라딘 유무)
    lv = LV_AT[no]; units = len(lv)
    cur = roster[:units]
    pal = "팔라딘" in cur; bis = "비숍" in cur
    ds = [j for j in cur if j not in ("팔라딘", "비숍")]
    dealers = {j: (1 if j in held else 0) for j in ds}
    if no < 56:
        base = {j: lv[i] for i, j in enumerate(cur)}
        fixed = [base]
        if "히어로" in base and "다크나이트" in base:
            sw = dict(base); sw["히어로"], sw["다크나이트"] = base["다크나이트"], base["히어로"]; fixed.append(sw)
        pl = base.get("팔라딘", 0); bl = base.get("비숍", 0)
        free = None
    else:
        if TIER_ON: ds = best_dealers(held, len(ds), no); dealers = {j: (1 if j in held else 0) for j in ds}
        if TIER_ON and SUN in held:
            alt = best_dealers(held, len(ds), no, True)
            ALT["d"] = {j: (1 if j in held else 0) for j in alt}
        else: ALT["d"] = None
        fixed = None; free = lv[:len(ds)]
        sup = lv[len(ds):]
        pl = min(sup) if pal else 0
        bl = (sorted(sup)[1] if len(sup) > 1 else sup[0]) if bis else 0
    guard = 0; pray = 1.0
    if pal: guard = 20 if (no >= 60 or pl >= 40) else (10 if pl >= 10 else 0)
    if bis: pray = 1.1 if (no >= 60 or bl >= 30) else 1.0
    return dealers, fixed, free, guard, pray, pal

UNLOCKED = {"ph": False}
ALT = {"d": None}
def best_dealers(held, n, no, with_sun=False):
    # 딜러 후보(팬텀은 해금했을 때만) 중 이 보스에서 대략 센 n명 — 50레벨·증강 반쯤 어림(최적 편성을 아는 사람). with_sun = 썬콜을 꼭 넣은 편성
    shred = TP["SHRED"] if (with_sun and SUN in held) else 0
    cand = [j for j in TIER if j != PH or UNLOCKED["ph"]]
    def score(j):
        p = 1 if j in held else 0
        rem = max(0.0, DEFS[no] - 20 - shred - ign_add(j, 50, p))
        return raw(j, 50, p) * (1 + 1.5 * aug_eff(j)) * max(0.02, 1 - rem / 100)
    pick = sorted(cand, key=score, reverse=True)
    if with_sun:
        pick = [SUN] + [j for j in pick if j != SUN]
    return pick[:n]

def label(got):
    tag = [SHORT[p] for p in ("enrage", "holyunity") if p in got]
    others = [SHORT[p] for p in JOB_ORDER[1:] + ["phantom"] if p in got]
    if others: tag.append("+".join(others))
    return " · ".join(tag) or "직업 프리즘 없음"

FRACS = (1.0, 0.75, 0.5, 0.25, 0.0)
def split(igns, f):
    # 방무 증강(큰 것부터)을 본딜·부딜에 '−log(1 − x)' 몫이 f : 1 − f가 되게 → 두 딜러의 남은 방어 비율(Π(1 − x))
    lf = [-math.log(1 - x / 100) for x in igns]
    T = sum(lf); s1 = s2 = 0.0; k1 = k2 = 1.0
    for x, l in zip(igns, lf):
        if f * T - s1 >= (1 - f) * T - s2: s1 += l; k1 *= 1 - x / 100
        else: s2 += l; k2 *= 1 - x / 100
    return k1, k2

def team_add(dealers, dmg, holy, defv, lv, guard, pray, fixedL=None, shred=0, vuln=0):
    js = list(dealers)
    best = 0.0
    for d1 in js:
        rest = sorted((j for j in js if j != d1), key=lambda j: -raw(j, 50, dealers[j]))
        order = [d1] + rest
        L = fixedL if fixedL is not None else {j: lv[i] for i, j in enumerate(order)}
        vals = {}
        for j in js:
            rem = max(0.0, defv - guard - shred - ign_add(j, L[j], dealers[j]))
            vals[j] = raw(j, L[j], dealers[j]) * max(0.0, 1 - rem / 100)
        top = max(vals, key=vals.get)
        other = 0.3 / max(1, len(js) - 1)
        ef = {j: (aug_eff(j) if L[j] >= 50 else 1.0) for j in js}   # 증강 효율은 50레벨부터(코드 GetStatFor와 같음)
        v = sum(vals[j] * (1 + dmg * ef[j] * (0.7 if j == top else other)) for j in js)
        if holy: v += vals[top] * (1 + dmg * ef[top] * 0.7) * 0.4
        if v > best: best = v
        if fixedL is not None: break
    return best * pray * (1 + vuln / 100)

def team(dealers, igns, dmg, busu, holy, defv, lv, guard, pray, fixedL=None, shred=0, vuln=0):
    D = max(0.0, defv * (1 - shred / 100) - guard) / 100
    js = list(dealers)
    splits = {f: split(igns, f) for f in FRACS}
    bk = 1 - BUSU / 100
    busu_opts = [(busu, 0)] + ([(busu - 1, 1)] if busu >= 1 and len(js) > 1 else [])
    best = 0.0
    for d1 in js:
        for d2 in js:
            if d2 == d1 and len(js) > 1: continue
            rest = sorted((j for j in js if j not in (d1, d2)), key=lambda j: -raw(j, 50, dealers[j]))
            order = [d1] + ([d2] if d2 != d1 else []) + rest
            L = fixedL if fixedL is not None else {j: lv[i] for i, j in enumerate(order)}
            rw = {j: raw(j, L[j], dealers[j]) for j in js}
            bs = {j: base_keep(j, L[j], dealers[j]) for j in js}
            for f in FRACS:
                k1, k2 = splits[f]
                for b1, b2 in busu_opts:
                    keep = dict(bs)
                    keep[d1] *= k1 * bk ** b1
                    if d2 != d1: keep[d2] *= k2 * bk ** b2
                    vals = {j: rw[j] * max(0.0, 1 - D * keep[j]) for j in js}
                    top = max(vals, key=vals.get)
                    other = 0.3 / max(1, len(js) - 1)
                    v = sum(vals[j] * (1 + dmg * aug_eff(j) * (0.7 if j == top else other)) for j in js)
                    if holy: v += vals[top] * (1 + dmg * aug_eff(top) * 0.7) * 0.4
                    if v > best: best = v
    return best * pray * (1 + vuln / 100)

FIRST_PRIO = ["enrage"] + JOB_ORDER[1:] + ["holyunity", "core_ign", "phantom", "core_final"]
LATER_PRIO = ["enrage", "holyunity", "core_ign"] + JOB_ORDER[1:] + ["phantom", "core_final"]
if TIER_ON:
    # 자쿰: 1티어 → 2티어 → 3티어 직업 프리즘(시그너스에 50레벨 프리즘 딜러) → 홀리 → 디바인 퍼니시먼트 → 방어구 부수기 / 그 뒤: 1티어(아직 없으면) → 홀리 → 디바인 퍼니시먼트 → 방어구 부수기 → 2티어 → 팬텀 → 3티어
    FIRST_PRIO = ["enrage", "fuma", "tempest", "dualblade", "arrowrain", "phantom", "transcend", "truesnipe", "giant", "holyunity", "divinepunish", "core_ign", "core_final"]
    LATER_PRIO = ["T1", "holyunity", "divinepunish", "core_ign", "dualblade", "arrowrain", "phantom", "enrage", "fuma", "tempest", "transcend", "truesnipe", "giant", "core_final"]
def run_one():
    got = set(); st = {"busu": 0, "dmg": 0.0, "offers": 0}
    UNLOCKED["ph"] = False
    roster = ["히어로", "다크나이트", "신궁", "팔라딘", "비숍", SUN]
    igns = []; buys = 0; bank = 0.0
    caps = {}
    def prism_offer(no):
        excl = {p for p in got if not p.startswith("core_")}
        offer = pick3([(k, w) for k, w in PRISM_POOL.items() if k not in excl])
        prio = FIRST_PRIO if st["offers"] == 0 else LATER_PRIO
        st["offers"] += 1
        if "T1" in prio:
            t1 = [] if any(q in got for q in ("enrage", "fuma", "tempest")) else ["enrage", "fuma", "tempest"]
            prio = [x for y in prio for x in (t1 if y == "T1" else [y])]
        for p in prio:
            if p in offer:
                if p == "core_ign": st["busu"] += 1
                elif p == "core_final": st["dmg"] += 0.15 / 0.7
                else:
                    got.add(p)
                    held = {JOB_PRISM[q] for q in JOB_ORDER if q in got}
                    units = GEN["units_at"](no)
                    if p in JOB_PRISM: swap_in(roster, JOB_PRISM[p], held, units)
                    elif p == "phantom":
                        UNLOCKED["ph"] = True
                        swap_in(roster, PH, held, units)
                return
    def take(offer, rnd):
        ig = [x for x in offer if x[2] == "ign"]
        if rnd >= IGN_FROM and ig:
            igns.append(max(x[3] for x in ig)); return
        g = next(k for k, v in POOL.items() if any(x[0] == offer[0][0] for x in v))
        st["dmg"] += GVAL[g]
    for s in ST:
        no = s["no"]
        if no in GRADE_AT: take(roll_normal(GRADE_AT[no]), no)
        if no >= BUY_FROM and s["kind"] == "mob":
            bank += MESO_AT[no] * BUY_SHARE
            while bank >= 3000 + 800 * buys:
                bank -= 3000 + 800 * buys; buys += 1
                r = random.random() * 100
                if r >= 99.5: prism_offer(no)
                else: take(roll_normal("bronze" if r < 80 else ("silver" if r < 95 else "gold")), no)
        if s["kind"] == "boss":
            held = {JOB_PRISM[q] for q in JOB_ORDER if q in got}
            dealers, fixed, free, guard, pray, pal = lineup(roster, held, no)
            ig = sorted(igns, reverse=True); holy = pal and "holyunity" in got
            vuln = TP["VULN"] if (TIER_ON and "divinepunish" in got and "비숍" in roster[:len(LV_AT[no])]) else 0
            if TIER_ON:
                opts = [dealers] + ([ALT["d"]] if (fixed is None and ALT["d"] is not None) else [])
                v = 0.0; pickd = dealers
                for dd in opts:
                    sh = TP["SHRED"] if ("tempest" in got and SUN in dd) else 0
                    if fixed is None: x = team_add(dd, st["dmg"], holy, DEFS[no], free, guard, pray, None, sh, vuln)
                    else: x = max(team_add(dd, st["dmg"], holy, DEFS[no], None, guard, pray, fl, sh, vuln) for fl in fixed)
                    if x > v: v = x; pickd = dd
                dealers = pickd
                shred = TP["SHRED"] if ("tempest" in got and SUN in dealers) else 0
            else:
                shred = 0
                if fixed is None: v = team(dealers, ig, st["dmg"], st["busu"], holy, DEFS[no], free, guard, pray, None, shred, vuln)
                else: v = max(team(dealers, ig, st["dmg"], st["busu"], holy, DEFS[no], None, guard, pray, fl, shred, vuln) for fl in fixed)
            caps["tier" + str(no)] = "·".join(str(TIER.get(j, 0)) for j in sorted(dealers, key=lambda j: TIER.get(j, 9))) + (" 홀리" if holy else "") + (" 퍼니시" if vuln else "") + (" 템페" if shred else "")
            caps[no] = v * 60 * (1 if len(s["mobs"]) == 1 else 0.5)
            caps["jp" + str(no)] = any(p in got for p in JOB_ORDER + ["phantom"])   # 팬텀(영웅 해금)도 50레벨 프리즘 딜러
            caps["combo"] = label(got)
            caps["b" + str(no)] = st["busu"]
        if no in GEN["PRISM_AT"]: prism_offer(no)
    return caps

random.seed(11)
runs = [run_one() for _ in range(N)]
nos = [s["no"] for s in BOSSES]
names = {s["no"]: s["name"] for s in BOSSES}
MOBS = {s["no"]: len(s["mobs"]) for s in BOSSES}
EFF = np.exp(np.random.default_rng(7).normal(0, SKILL_SD, N))   # 판마다 플레이 편차
CAP = {no: np.array([r[no] for r in runs]) * EFF for no in nos}
JPA = {no: np.array([r["jp" + str(no)] for r in runs]) for no in nos}
COMBO = np.array([r["combo"] for r in runs])
HPNOW = {s["no"]: float(s["hp"]) for s in BOSSES}

hp = {}; alive = np.ones(N, dtype=bool); rows = []; P1 = {}
for no in nos:
    want = PASS[LABEL[no]]
    if MODE == "overall":
        h = max(1.0, float(np.quantile(CAP[no], 1 - want)))   # 전체 판 중 want만큼 깰 수 있게
        if no in PRISM_GATE:
            nj = CAP[no][~JPA[no]]
            if len(nj): h = max(h, float(np.quantile(nj, TP.get("GATE_Q", 0.85))))
    else:
        if no == nos[-1] and FINAL > 0: want = min(1.0, FINAL / max(1e-9, alive.mean()))
        if no in CUM and CUM[no] != "all": want = min(1.0, CUM[no] / max(1e-9, alive.mean()))
        c = CAP[no][alive]
        h = max(1.0, float(np.quantile(c, 1 - want)))
        if CUM.get(no) == "all": h = float(c.min()) / 1.1   # 앞을 넘은 판은 무조건 통과
        if no in EARLY and SKILL_SD == 0: h = float(np.quantile(c, 0.01)) / MARGIN[LABEL[no]]
        if no in PRISM_GATE:
            # 50레벨 프리즘 딜러 필수: 통과율 목표는 직업 프리즘이 있는 판 기준, 없는 판은 85% 이상 못 넘게
            wj = CAP[no][alive & JPA[no]]; nj = CAP[no][alive & ~JPA[no]]
            h = float(np.quantile(wj, 1 - want))
            if len(nj): h = max(h, float(np.quantile(nj, TP.get("GATE_Q", 0.85))))
    hp[no] = h
    reach = alive.copy()
    P1[no] = float(np.quantile(CAP[no], 0.01)) / h
    alive &= CAP[no] >= h
    rows.append((no, reach.sum(), alive.sum(), float(np.median(CAP[no]) / h), float((CAP[no] >= h).mean())))
print("방어율", DEFS, f"· 판 수 {N} · 방무 고르기 {IGN_FROM}라운드~ · 루시드 뒤 메소의 {BUY_SHARE:.0%}로 증강 뽑기 · 방어구 부수기 {BUSU:.0f}")
print("기준", "전체 판 중 깰 수 있는 비율" if MODE == "overall" else f"그 보스까지 온 판 중 통과율(마지막 보스는 최종 클리어 {FINAL:.0%}로 역산)", PASS, f"· 플레이 편차 σ {SKILL_SD}")
print("보스 | 난이도 | 방어율 | 체력(한 마리) | 지금 | 깰 수 있는 판(전체) | 앞을 다 넘은 판 중 | 누적 생존 | 여유 하위 1% · 중앙값")
for no, reach, ok, med, solo in rows:
    print(f"  {no:3d} {names[no]} | {LABEL[no]} | {DEFS[no]} | {hp[no]:,.0f}{' ×' + str(MOBS[no]) if MOBS[no] > 1 else ''} | {HPNOW[no]:,.0f}(×{hp[no] / HPNOW[no]:.2f}) | {solo:.1%} | {ok / max(1, reach):.1%} | {ok / N:.1%} | ×{P1[no]:.2f} · ×{med:.2f}")
for no in PRISM_GATE:
    reach = np.ones(N, dtype=bool)
    for x in nos:
        if x == no: break
        reach &= CAP[x] >= hp[x]
    for nm, idx in (("직업 프리즘 있음", JPA[no]), ("없음", ~JPA[no])):
        print(f"  {names[no]} {nm}: {idx.sum() / N:.0%}의 판 · 깰 수 있음 {(CAP[no][idx] >= hp[no]).mean() if idx.any() else 0:.1%}")
print("조합별 검마 클리어율(판 1% 이상):")
for c in sorted(set(COMBO), key=lambda c: -(COMBO == c).sum()):
    idx = COMBO == c
    if idx.mean() < 0.01: continue
    print(f"  {c}: {idx.mean():.0%}의 판 · 클리어 {alive[idx].mean():.1%}")
EN = np.array(["인레이지" in c for c in COMBO]); HO = np.array(["홀리" in c for c in COMBO])
for nm, idx in (("인레이지 + 홀리", EN & HO), ("인레이지만", EN & ~HO), ("홀리만", ~EN & HO), ("둘 다 없음", ~EN & ~HO)):
    print(f"  [{nm}] {idx.mean():.0%}의 판 · 검마 클리어 {alive[idx].mean():.1%}")
b = np.array([r["b132"] for r in runs])
for k in (0, 1, 2):
    idx = (b == k) if k < 2 else (b >= 2)
    if idx.any(): print(f"  방어구 부수기 {k}{'+' if k == 2 else ''}개: {idx.mean():.0%}의 판 · 클리어 {alive[idx].mean():.1%}")
if TIER_ON:
    comp = np.array([r.get("tier132", "") for r in runs])
    print("검마 도달 편성별(딜러 티어 · 서포트 프리즘) — 판 비율 · 클리어:")
    for c in sorted(set(comp), key=lambda c: -(comp == c).sum())[:14]:
        idx = comp == c
        print(f"  {c}: {idx.mean():.0%}의 판 · 클리어 {alive[idx].mean():.1%} · 클리어 판 중 {alive[idx].sum() / max(1, alive.sum()):.0%}")
print("HP_OUT", {no: round(hp[no]) for no in nos})

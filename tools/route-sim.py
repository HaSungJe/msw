# -*- coding: utf-8 -*-
"""루트 분석(2026-09-23 사용자 "프리즘 3개로 줄이고 밸런스표 재작성, 라인 클리어 + 보스 기준 최적 루트 찾아줘").

입력: 생성기(tools/gen-stage-table.py)의 스테이지 표(체력·방어율·메소·표준 빌드 레벨) + .info/balance-detail.md 직업별 상세 표(현재 값 — 체력 모델의 고정 앵커가 아님).
출력: (1) 한눈에 비교 표(보스·몬스터 DPS, 현재 값) (2) 영입 순서 6명 전수 탐색(10P6 = 151,200) → 사냥·보스 여유(요구 대비 배수)의 최솟값이 가장 큰 순서
      (3) 그 루트의 라운드 구간별 여유·프리즘·후반 보스(스우~, 방어율 200~350) 필요 방무.
모델(생성기와 같은 가정): 레벨 = 그 라운드 표준 빌드(메소를 다 레벨업에, 먼저 영입한 유닛이 높은 레벨), 사냥 여유 = 팀 사냥 DPS × 방어 × 프레이 × 증강 × 가동률 0.6 × 20초 ÷ 40마리 ÷ 몹 체력,
      보스 여유 = 팀 보스 DPS(방어 · 프리즘 · 증강 몰아주기 70% · 가드 크러쉬 · 프레이 · 홀리 유니티) × 60초 ÷ 보스 체력.
실행: python tools/route-sim.py  (생성기를 import 대신 실행해 표를 만든 뒤 분석 — 생성기가 파일을 쓰지는 않게 몬스터 크기 절 앞까지만)
"""
import io, os, re, sys, math, itertools
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, "tools", "gen-stage-table.py")
src = io.open(GEN, encoding="utf-8").read()
cut = src.index("# ======================================================================== 몬스터 크기")
G = {"__name__": "route", "__file__": GEN}
exec(compile(src[:cut], "gen", "exec"), G)
ST, JOBS, mob_def, BOSS_DEF_AT, BOSS_DEF = G["ST"], G["JOBS"], G["mob_def"], G["BOSS_DEF_AT"], G["BOSS_DEF"]
aug_counts, GAIN, AUG_TOP, UPTIME, SPAWN, FIELD_MOBS = G["aug_counts"], G["GAIN"], G["AUG_TOP_SHARE"], G["UPTIME"], G["SPAWN"], G["FIELD_MOBS"]
PRISM_MUL, RECRUIT_AT, BUSU_IGN = G["PRISM_MUL"], G["RECRUIT_AT"], G["BUSU_IGN"]
PRISM_AT = G["PRISM_AT"]
LVS = [1, 10, 20, 30, 40, 50]
PH = "팬텀"

# ---------------- 현재 직업 값(balance-detail 상세 표 — 앵커 아님)
def num(x):
    x = x.replace(",", "").strip()
    try: return float(x)
    except Exception: return None
CUR = {}
bd = io.open(os.path.join(ROOT, ".info", "balance-detail.md"), encoding="utf-8").read()
for sec in re.split(r"\n## ", bd):
    title = sec.split("\n")[0]
    job = next((j for j in JOBS + [PH] if title.startswith(j + " ")), None)
    if job is None: continue
    rows = {}
    for l in sec.split("\n"):
        m = re.match(r"^\| (1|10|20|30|40|50) \|(.*)$", l)
        if not m: continue
        c = [x.strip() for x in m.group(2).strip().strip("|").split("|")]
        lv = int(m.group(1)); atk = num(c[0])
        if job == "아크메이지(불·독)":
            hunt = num(c[3]) * FIELD_MOBS; boss = num(c[4]) if num(c[4]) is not None else 0.0
        else:
            boss = num(c[5]); hunt = num(c[7])
        rows[lv] = (atk, boss, hunt)
    if len(rows) == 6: CUR[job] = rows
assert len(CUR) == 11, list(CUR)

def dps(job, L):
    r = CUR[job]; a = max(x for x in LVS if x <= L)
    if a == L: return r[a][1], r[a][2]
    b = LVS[LVS.index(a) + 1]
    k = (r[a][0] + (r[b][0] - r[a][0]) * (L - a) / (b - a)) / max(r[a][0], 1)
    return r[a][1] * k, r[a][2] * k

def boss_raw(job, L):
    b = dps(job, L)[0]
    if job == "신궁" and L >= 30: b *= 1.66 + (1.18 - 1.66) * (L - 30) / 20
    return b

SUN = "아크메이지(썬·콜)"
def hunt_raw(job, L, prisms):
    h = dps(job, L)[1]
    if job == "비숍" and L >= 20: h *= 4.33                  # 제네시스
    if job == "다크나이트" and L >= 50: h *= 1.15             # 드래곤 로어
    if job == SUN and L >= 30: h *= (2.9 if prisms >= 1 else 1.13)   # 블리자드(엘릭서 = 쿨 2초)
    if prisms >= 1:
        h *= {"히어로": 1.5, "다크나이트": 1.16, "보우마스터": 1.16, "나이트로드": 1.18, "섀도어": 1.2, "아크메이지(불·독)": 1.2, "비숍": 1.18}.get(job, 1.0)
    return h

def boss_with_prism(job, L, prisms):
    b = boss_raw(job, L)
    mul = PRISM_MUL.get(job, [1.0])
    for i in range(min(prisms, len(mul))): b *= mul[i]
    return b

# 방무(합연산 — 2026-09-24 사용자 "합연산 + 증강 방무 삭제", 곱연산에서 되돌림). 히어로 발할라(60)는 보스만
def comb(*xs):
    return float(sum(xs))
def ign_of(job, L, prisms, boss):
    parts = []
    if job == "히어로":
        parts.append(10 if L >= 20 else (5 if L >= 10 else 0))
        if boss and L >= 50: parts.append(60)
    if job == PH and L >= 50: parts.append(60)
    if L >= 50: parts.append({"보우마스터": 50, "섀도어": 50, "다크나이트": 20, "신궁": 20, "아크메이지(불·독)": 20}.get(job, 0))   # 2티어·3티어 킷(2026-09-24)
    if prisms >= 1: parts.append({"다크나이트": 15, "나이트로드": 70, "신궁": 15, "아크메이지(불·독)": 15}.get(job, 0))
    if job == SUN and prisms >= 1: parts.append(15)   # 블리자드 템페스트 방무 +15
    return comb(*parts)

# 데미지 배율 = 1 − max(0, 방어율 − 가드 크러쉬 − 방무) ÷ 100  (합연산)
def defm(defv, guard, ign, boss=False):
    return max(0.0, 1 - max(0.0, defv - guard - ign) / 100)

# ---------------- 라운드 표
R = [s for s in ST if s["kind"] in ("mob", "boss")]
NR = len(R)
NO = np.array([s["no"] for s in R])
IS_BOSS = np.array([s["kind"] == "boss" for s in R])
HP = np.array([float(s["hp"]) * len(s["mobs"]) for s in R])
DEF = np.array([float(BOSS_DEF_AT.get(s["no"], BOSS_DEF) if s["kind"] == "boss" else mob_def(s["no"])) for s in R])
UNITS = np.array([G["units_at"](s["no"]) for s in R])
LV = [sorted(s["lv"], reverse=True) + [1] * 6 for s in R]
AUGC = [aug_counts(s["tagmax"]) for s in R]
AUGH = np.array([1 + 0.01 * b + 0.02 * sv + 0.035 * g for b, sv, g in AUGC])
AUGG = np.array([b * GAIN["b"] + sv * GAIN["s"] + g * GAIN["g"] for b, sv, g in AUGC])
HIGHDEF = np.array([s["kind"] == "boss" and s["no"] in BOSS_DEF_AT for s in R])   # 루시드~4페이즈(방어율 175~300)

def prisms_at(no, got):   # got = 받은 프리즘 라운드 목록 → 이 라운드에 가진 수(받은 '뒤' 스테이지부터)
    return sum(1 for r in got if r < no)

# 유닛 1명의 라운드별 사냥·보스 기여(방어·가드 크러쉬 반영 전 원값과 방무) — 가드 크러쉬 0/10/20 세 벌
def unit_arrays(job, slot, got):
    hr = np.zeros(NR); br = np.zeros(NR); ih = np.zeros(NR); ib = np.zeros(NR)
    for k, s in enumerate(R):
        if UNITS[k] <= slot: continue
        L = LV[k][slot]; p = prisms_at(s["no"], got)
        hr[k] = hunt_raw(job, L, p); br[k] = boss_with_prism(job, L, p)
        ih[k] = ign_of(job, L, p, False); ib[k] = ign_of(job, L, p, True)
    out = {}
    for gc in (0, 10, 20):
        hm = np.array([defm(DEF[k], gc, 100 if job == "아크메이지(불·독)" else ih[k]) for k in range(NR)])   # 포이즌 리전 방무 100
        bm = np.array([defm(DEF[k], gc, ib[k], bool(IS_BOSS[k])) for k in range(NR)])
        out[gc] = (hr * hm, br * bm)
    return out

# 팀 버프(슬롯 레벨 기준): 프레이(비숍 30~ ×1.1), 가드 크러쉬(팔라딘 10~ 10, 40~ 20)
def slot_level(slot): return np.array([LV[k][slot] if UNITS[k] > slot else 0 for k in range(NR)])

# ---------------- 프리즘 배정 규칙(루트용): 프리즘 라운드마다 '보스 여유가 가장 크게 오르는' 직업에(직업당 1개 — 썬콜 템페스트는 2026-09-23 엘릭서 통합). 팔라딘 홀리 유니티는 가장 센 유닛 ×1.4
def plan_prisms(order):
    got = {j: [] for j in order}
    for pr in PRISM_AT:
        k = next(i for i, s in enumerate(R) if s["no"] > pr)
        L = LV[k]
        best = None; bestGain = 0
        for idx, j in enumerate(order[:UNITS[k]]):
            cap = 1
            if len(got[j]) >= cap: continue
            if j == "팔라딘":
                others = [boss_with_prism(o, L[i], len(got[o])) for i, o in enumerate(order[:UNITS[k]]) if o != j]
                gain = 0.4 * max(others) if others else 0
            else:
                cur = boss_with_prism(j, L[idx], len(got[j])); nxt = boss_with_prism(j, L[idx], len(got[j]) + 1)
                gain = nxt - cur
            if gain > bestGain: bestGain = gain; best = j
        if best is not None: got[best].append(pr)
    return got

CACHE = {}
def arrays(job, slot, got):
    key = (job, slot, tuple(got))
    if key not in CACHE: CACHE[key] = unit_arrays(job, slot, got)
    return CACHE[key]

def evaluate(order, detail=False):
    got = plan_prisms(order)
    guard = np.zeros(NR); pray = np.ones(NR); holy = np.zeros(NR, dtype=bool)
    for i, j in enumerate(order):
        L = slot_level(i)
        if j == "팔라딘":
            guard = np.where(L >= 40, 20, np.where(L >= 10, 10, 0))
            if got[j]: holy = NO > got[j][0]
        if j == "비숍": pray = np.where(L >= 30, 1.1, 1.0)
    H = np.zeros((6, NR)); B = np.zeros((6, NR))
    for i, j in enumerate(order):
        a = arrays(j, i, got[j])
        for gc in (0, 10, 20):
            m = guard == gc
            H[i][m] = a[gc][0][m]; B[i][m] = a[gc][1][m]
    hunt = H.sum(0) * pray * AUGH * UPTIME * 20 / SPAWN
    top = B.max(0); rest = B.sum(0) - top
    n = np.maximum(UNITS - 1, 1)
    bossv = (B.sum(0) + top * AUGG * AUG_TOP + rest * AUGG * (1 - AUG_TOP) / n + np.where(holy, 0.4 * top, 0)) * pray
    ratio = np.where(IS_BOSS, bossv * 60 / HP, hunt / HP)
    if detail: return ratio, got, B, pray, guard
    return ratio, got

# ---------------- (1) 한눈에 비교 표
def fmt(x): return f"{x:,.0f}"
cols = ["히어로", "팔라딘", "다크나이트", "보우마스터", "신궁", SUN, "비숍", "나이트로드", "섀도어", PH, "아크메이지(불·독)"]
short = {SUN: "썬콜", "아크메이지(불·독)": "불독"}
lines = []
lines.append("| Lv | " + " | ".join(short.get(c, c) for c in cols) + " |")
lines.append("|---" * (len(cols) + 1) + "|")
BOSS_TBL = [l for l in lines]; HUNT_TBL = [l for l in lines]
for L in LVS:
    BOSS_TBL.append(f"| {L} | " + " | ".join(fmt(CUR[c][L][1]) for c in cols) + " |")
    HUNT_TBL.append(f"| {L} | " + " | ".join(fmt(CUR[c][L][2]) for c in cols) + " |")

# ---------------- (2) 탐색: 히어로 포함(후반 방어율 175~300 보스는 방무 증강을 몰아준 히어로·팬텀만 뚫는다), 팬텀은 프리즘 해금이라 영입 후보에서 뺌
MASK = ~HIGHDEF      # 방어율 높은 후반 보스는 여유 계산에서 빼고 따로 본다(필요 방무)
best = []
for order in itertools.permutations(JOBS, 6):
    if "히어로" not in order: continue
    ratio, got = evaluate(order)
    r = ratio[MASK]
    score = (float(r.min()), float(np.exp(np.log(np.maximum(r, 1e-6)).mean())))
    best.append((score, order))
best.sort(reverse=True)

def band(ratio, lo, hi, boss):
    m = (NO >= lo) & (NO <= hi) & (IS_BOSS == boss) & MASK
    return float(ratio[m].min()) if m.any() else None

print("## 한눈에 비교 — 보스 DPS(현재)"); print("\n".join(BOSS_TBL)); print()
print("## 한눈에 비교 — 몬스터 DPS(현재)"); print("\n".join(HUNT_TBL)); print()
print("## 상위 루트(최소 여유, 기하평균 여유)")
for sc, order in best[:15]:
    print(f"{sc[0]:.2f} {sc[1]:.2f}  " + " → ".join(short.get(j, j) for j in order))
print()
# 1위 루트 상세
sc, order = best[0]
ratio, got, B, pray, guard = evaluate(order, True)
print("### 1위 루트 상세:", " → ".join(short.get(j, j) for j in order), "| 프리즘:", {short.get(j, j): v for j, v in got.items() if v})
for lo, hi in [(1, 9), (11, 25), (27, 42), (44, 55), (57, 88), (90, 126)]:
    print(f"  사냥 {lo}~{hi}: 최소 여유 {band(ratio, lo, hi, False):.2f}")
for k, s in enumerate(R):
    if s["kind"] == "boss":
        extra = ""
        if HIGHDEF[k]:
            # 필요 방무: 히어로(프리즘 인레이지 가정)만으로 60초 — 합연산: 방어 − 가드 − 방무 ≤ 100 × (1 − 필요/원딜)
            L = LV[k][order.index("히어로")] if "히어로" in order else 50
            raw = boss_with_prism("히어로", L, 1 if got.get("히어로") and got["히어로"][0] < s["no"] else 0)
            aug = 1 + AUGG[k] * AUG_TOP
            need = HP[k] / 60 / (raw * aug * pray[k])
            rem = 100 * (1 - need) if need < 1 else -1
            ign_need = DEF[k] - guard[k] - rem if rem >= 0 else float("inf")
            extra = f"  | 히어로 혼자 60초: 필요 방무 ≥ {ign_need:.0f}(가드 {guard[k]:.0f} 포함 전 원딜 {raw * aug * pray[k]:,.0f}/초, 필요 {HP[k] / 60:,.0f}/초)"
        print(f"  보스 {s['no']:3d} {s['name']}: 여유 {ratio[k]:.2f} (레벨 {LV[k][:UNITS[k]]}){extra}")

# ---------------- 구간별 비교(최솟값이 모든 루트에서 같은 라운드에 걸려 순위가 무뎌지므로 — 구간 최소·기하평균으로 다시 본다)
def summary(order):
    ratio, got = evaluate(order)
    r = ratio[MASK]
    bands = [band(ratio, lo, hi, False) for lo, hi in [(1, 9), (11, 25), (27, 42), (44, 55), (57, 88), (90, 126)]]
    bosses = [float(ratio[k]) for k, s in enumerate(R) if s["kind"] == "boss" and not HIGHDEF[k]]
    gm = float(np.exp(np.log(np.maximum(r, 1e-6)).mean()))
    return gm, bands, bosses, got
rank2 = []
for sc, order in best:
    gm, bands, bosses, got = summary(order)
    rank2.append((gm, order, bands, bosses, got))
rank2.sort(key=lambda x: -x[0])
print()
print("## 기하평균 여유 순위(후반 고방어 보스 제외) — 구간별 사냥 최소 / 보스 여유(10·26·29·43·47·56·60·64)")
seen = set()
for gm, order, bands, bosses, got in rank2:
    key = order[:3]
    if key in seen: continue
    seen.add(key)
    print(f"{gm:.3f}  " + " → ".join(short.get(j, j) for j in order) + "  | 사냥 " + " ".join(f"{b:.2f}" for b in bands) + "  | 보스 " + " ".join(f"{b:.1f}" for b in bosses)
          + "  | 프리즘 " + ", ".join(f"{short.get(j, j)}@{v}" for j, v in got.items() if v))
    if len(seen) >= 12: break

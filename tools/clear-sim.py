# -*- coding: utf-8 -*-
"""클리어 시뮬레이터(2026-09-24 티어 재설계 뒤 — .info/tier.md).

한 판을 끝까지 재현해 보스마다 '60초 팀 딜(= 잡을 수 있는 체력)'을 구하고, 여러 판의 분포로
  · 보통(지금 체력 — tools/gen-stage-table.py)에서 보스별 통과율 · 누적 생존
  · 극악(최적 조합을 아는 사람 기준 목표 통과율이 나오게 역산한 보스 체력)
을 낸다. 딜 계산은 tools/balance-calc.py(kit · rotation_dps · defmul · aug_mul — 게임 코드와 같은 값).

한 판:
  조합 = 1티어 1 + 2티어 3 + 팔라딘(≤40) + 비숍(≤30). 영입 1·5·26·43·47·56라운드 = 1티어 · 2티어A · 2티어B · 팔라딘 · 비숍 · 2티어C
  레벨 = 그 보스의 표준 빌드 레벨(생성기 lv — 딜러가 높은 순, 서포터는 상한)
  증강 = 라운드 지급 27장(augmentation.md) + 뽑기(여유 메소 — 딜러 4명 50 + 비숍 30 + 팔라딘 40, 3,000 + 40씩, tier.md 3절 시점별 누적 횟수)
         뽑기 등급 브 75.5 · 실 15 · 골 4.5 · 프리즘 5% + 천장(안 나오면 +2%p, 나오면 0 — 판마다 최대 2개)
  프리즘 = 보장 3개(자쿰 26 · 시그너스 56 · 루시드 89 처치 뒤 3택1) + 뽑기 프리즘 — 조합에 맞는 것 우선, 없으면 특수 코어(보스 슬레이어 > 일격필살)는 1티어에
  분배 = 권장(1티어가 30장이 될 때까지 1티어 → 2티어 각 8장까지 → 남으면 1티어). 3택1은 받는 유닛에 가장 좋은 것
  보스전 = 60초, 방어율 − 가드 크러쉬 − 방어구 부수기(1티어 증강 수, 최대 30) − 방무 · 프레이 ×1.1 · 홀리 유니티(1티어 ×1.4) · 디바인 퍼니시먼트(받는 데미지 ×1.2) · 샤프아이즈(신궁 20레벨)
사용: python tools/clear-sim.py [판 수=2000] [--t1 히어로] [--t2 신궁,다크나이트,불독]
"""
import io, os, sys, math, random, importlib.util, argparse, json
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("bc", os.path.join(ROOT, "tools", "balance-calc.py"))
bc = importlib.util.module_from_spec(spec); spec.loader.exec_module(bc)

PRISM_OF = {"히어로": "enrage", "나이트로드": "fuma", "썬콜": "tempest", "보우마스터": "arrowrain", "섀도어": "dualblade", "불독": "transcend",
            "신궁": "truesnipe", "다크나이트": "giant", "팔라딘": "holy", "비숍": "dp", "팬텀": "phantom"}
POOL = {"oneshot": 5, "slayer": 5, "phantom": 5, "dualblade": 5, "enrage": 7.5, "holy": 7.5, "giant": 7.5, "tempest": 7.5,
        "transcend": 7.5, "dp": 7.5, "arrowrain": 7.5, "truesnipe": 7.5, "fuma": 7.5}   # augmentation.md 프리즘
CORE = {"oneshot", "slayer"}
GUAR_PRISM = [26, 56, 89]
CARD_ROUNDS = bc.CARD_ROUNDS
BUY_BY_BOSS = {10: 0, 26: 0, 29: 0, 43: 0, 47: 0, 56: 0, 60: 1, 64: 3, 89: 3, 110: 24, 114: 32, 121: 45, 127: 55, 129: 55, 130: 55, 131: 55, 132: 55}   # tier.md 3절
RECRUIT = [1, 5, 26, 43, 47, 56]
T1_CAP, T2_CAP = 30, 8
# 극악 목표(2026-09-24 사용자 — 최적 조합을 아는 사람 기준): 시그너스까지는 그 보스에 온 판 중 통과율, 스우부터 누적 생존(4페 = 3~4%)
EARLY = {10: 0.99, 26: 0.95, 29: 0.99, 43: 0.95, 47: 0.95, 56: 0.88}
CUM = {60: 0.60, 64: 0.50, 89: 0.35, 110: 0.30, 114: 0.25, 121: 0.20, 127: 0.15, 129: 0.10, 130: 0.10, 131: 0.05, 132: 0.035}

def offer(owned, rng):
    pool = [(k, w) for k, w in POOL.items() if k in CORE or k not in owned]
    out = []
    for _ in range(3):
        tot = sum(w for _, w in pool); r = rng.random() * tot
        for i, (k, w) in enumerate(pool):
            r -= w
            if r <= 0: out.append(k); pool.pop(i); break
    return out

class Unit:
    def __init__(self, job, role): self.job, self.role, self.augs, self.prism = job, role, [], False

def eff_stats(u, L):
    """레벨 L · 프리즘 · 증강(배율 — 1티어는 가진 증강 수 n으로 1 + 2n/30, 이미 받은 것까지)"""
    st, sk = bc.kit(u.job, L, u.prism)
    n = len(u.augs) + (1 if (u.prism and u.role == "t1") else 0)
    for stat, v in u.augs:
        if stat == "slayer": st = bc.apply_aug(st, "boss", 60)
        elif stat == "oneshot": st = bc.apply_aug(st, "fin", 15)
        else: st = bc.apply_aug(st, stat, v, bc.aug_mul(u.job, u.prism, stat, n))
    return st, sk

def power(u, L):
    st, sk = eff_stats(u, L); return bc.power(st) * st["finBoss"]

class Run:
    def __init__(self, t1, t2s, rng):
        self.rng = rng
        self.units = [Unit(t1, "t1"), Unit(t2s[0], "t2"), Unit(t2s[1], "t2"), Unit("팔라딘", "pal"), Unit("비숍", "bis"), Unit(t2s[2], "t2")]
        self.owned = set(); self.cores = []; self.buy_prisms = 0; self.pity = 0
    def present(self, no): return [u for u, r in zip(self.units, RECRUIT) if r <= no]
    def need(self, no):
        need = []
        for u in self.units:
            p = PRISM_OF[u.job]
            if p not in self.owned: need.append(p)
        return need
    def prism_event(self, no):
        o = offer(self.owned, self.rng)
        need = self.need(no)
        # 우선: 1티어 > 서포터(홀리 → 디바인) > 2티어
        order = [PRISM_OF[self.units[0].job], "holy", "dp"] + [PRISM_OF[u.job] for u in self.units if u.role == "t2"]
        pick = next((k for k in order if k in o and k in need), None)
        if pick is None:
            pick = next((k for k in ("slayer", "oneshot") if k in o and k not in self.cores), None)
            if pick: self.cores.append(pick); self.units[0].augs.append((pick, 0))
            return
        self.owned.add(pick)
        for u in self.units:
            if PRISM_OF[u.job] == pick: u.prism = True
    def give_card(self, grade, no, lv):
        pres = [u for u in self.present(no) if u.role in ("t1", "t2")]
        t1 = self.units[0]
        recv = t1
        if len(t1.augs) >= T1_CAP:
            t2s = [u for u in pres if u.role == "t2" and len(u.augs) < T2_CAP]
            if t2s: recv = min(t2s, key=lambda u: len(u.augs))
        opts = bc.draw3(grade, self.rng)
        L = lv.get(recv.role + str(id(recv)), 50)
        best = None
        for a in opts:
            recv.augs.append((a[1], a[2])); pw = power(recv, L); recv.augs.pop()
            if best is None or pw > best[0]: best = (pw, a)
        recv.augs.append((best[1][1], best[1][2]))

def levels_at(run, s):
    lv = sorted(s["lv"], reverse=True); pres = run.present(s["no"])
    dealers = [u for u in pres if u.role in ("t1", "t2")]; sups = [u for u in pres if u.role in ("pal", "bis")]
    out = {}
    for i, u in enumerate(dealers): out[id(u)] = lv[i] if i < len(lv) else 1
    rest = lv[len(dealers):]
    for i, u in enumerate(sups):
        L = rest[i] if i < len(rest) else 1
        out[id(u)] = min(L, 40 if u.role == "pal" else 30)
    return out

def capacity(run, s, G):
    no = s["no"]; lvs = levels_at(run, s); pres = run.present(no)
    defv = G["BOSS_DEF_AT"].get(no, G["BOSS_DEF"])
    pal = next((u for u in pres if u.role == "pal"), None); bis = next((u for u in pres if u.role == "bis"), None)
    guard = 0
    if pal: guard = 20 if lvs[id(pal)] >= 40 else (10 if lvs[id(pal)] >= 10 else 0)
    t1 = run.units[0]
    # 방어구 부수기는 1티어가 자기 직업 프리즘을 가졌을 때만(2026-09-24 게임과 같게 — RtsJobTableLogic.ArmorBreakFor)
    armor = min(len(t1.augs) + 1, 30) if t1.prism else 0
    pray = 1.1 if (bis and lvs[id(bis)] >= 30) else 1.0
    vuln = 1.2 if (bis and bis.prism) else 1.0
    holy = 1.4 if (pal and pal.prism) else 1.0
    sharp = any(u.job == "신궁" and lvs[id(u)] >= 20 for u in pres) or any(u.job == "보우마스터" and lvs[id(u)] >= 40 for u in pres)
    tot = 0.0
    for u in pres:
        st, sk = eff_stats(u, lvs[id(u)])
        if sharp: st = dict(st, crit=st["crit"] + 20, cd=st["cd"] + 20)
        d = bc.rotation_dps(st, sk, True, T=60) * bc.defmul(defv, st["ign"] + st["ignBoss"], guard, armor)
        if u is t1: d *= holy
        tot += d
    return tot * pray * vuln * 60

def one_run(t1, t2s, G, rng):
    run = Run(t1, t2s, rng)
    caps = {}
    bosses = [s for s in G["ST"] if s["kind"] == "boss"]
    card_ev = sorted([(r, g) for g, rs in CARD_ROUNDS.items() for r in rs])
    ci = 0; bought = 0
    for s in bosses:
        no = s["no"]; lvs = levels_at(run, s)
        lv_role = {}
        for u in run.present(no): lv_role[u.role + str(id(u))] = lvs[id(u)]
        while ci < len(card_ev) and card_ev[ci][0] < no:
            run.give_card(card_ev[ci][1], no, lv_role); ci += 1
        while bought < BUY_BY_BOSS[no]:
            # 프리즘 = 5% + 천장(프리즘 없이 뽑을 때마다 +2%p, 나오면 0 — 2026-09-24 사용자), 판마다 최대 2개. 나머지는 브 75.5 · 실 15 · 골 4.5 비율
            pr = (5 + run.pity) if run.buy_prisms < 2 else 0
            r = rng.random() * 100; bought += 1
            if r < pr:
                run.buy_prisms += 1; run.pity = 0; run.prism_event(no)
            else:
                rr = (r - pr) / (100 - pr) * 95
                g = "gold" if rr >= 90.5 else ("silver" if rr >= 75.5 else "bronze")
                if run.buy_prisms < 2: run.pity += 2
                run.give_card(g, no, lv_role)
        caps[no] = capacity(run, s, G)
        if no in GUAR_PRISM: run.prism_event(no)   # 처치 뒤 3택1(다음 보스부터)
    return caps

def boss_hp(s): return float(s["hp"]) * len(s["mobs"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="?", type=int, default=2000)
    ap.add_argument("--t1", default="히어로")
    ap.add_argument("--t2", default="신궁,다크나이트,불독")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    G = bc.load_stages(); rng = random.Random(a.seed)
    t2s = a.t2.split(",")
    bosses = [s for s in G["ST"] if s["kind"] == "boss"]
    runs = []
    for i in range(a.runs):
        runs.append(one_run(a.t1, t2s, G, rng))
        if (i + 1) % 200 == 0: print(f"  … {i + 1}판", flush=True)
    print(f"\n조합: 1티어 {a.t1} + 2티어 {', '.join(t2s)} + 팔라딘 40 + 비숍 30 · {a.runs}판\n")
    # 보통 = 지금 체력
    alive = list(range(len(runs)))
    print("| 보스 | 지금 체력(보통) | 60초 팀 딜 중앙값 | 보통 통과(도달 판 중) | 보통 누적 |")
    print("|---|---|---|---|---|")
    for s in bosses:
        no = s["no"]; hp = boss_hp(s)
        caps = sorted(runs[i][no] for i in alive)
        med = caps[len(caps) // 2] if caps else 0
        passed = [i for i in alive if runs[i][no] >= hp]
        rate = len(passed) / len(alive) if alive else 0
        alive = passed
        print(f"| {no} {s['name']} | {hp:,.0f} | {med:,.0f} | {rate * 100:.1f}% | {len(alive) / len(runs) * 100:.1f}% |")
    # 극악 = 목표 통과율이 나오게 역산
    print("\n| 보스 | 극악 체력 | ÷ 지금 | 목표 | 누적 생존 |")
    print("|---|---|---|---|---|")
    alive = list(range(len(runs))); X = {}
    for s in bosses:
        no = s["no"]; caps = sorted((runs[i][no], i) for i in alive)
        if no in EARLY: keep = EARLY[no] * len(alive)
        else: keep = CUM[no] * len(runs)
        k = max(0, min(len(caps) - 1, len(caps) - int(round(keep))))
        hp = caps[k][0] if caps else 0.0
        if no == 130: hp = min(hp, caps[0][0] if caps else hp)   # 검마 2페 = 1페 넘으면 무조건
        alive = [i for c, i in caps if c >= hp]
        X[no] = hp
        tgt = f"도달 판 {EARLY[no] * 100:.0f}%" if no in EARLY else f"누적 {CUM[no] * 100:.1f}%"
        print(f"| {no} {s['name']} | {hp:,.0f} | ×{hp / boss_hp(s):.2f} | {tgt} | {len(alive) / len(runs) * 100:.1f}% |")
    if a.json:
        json.dump({"X": X, "cur": {s["no"]: boss_hp(s) for s in bosses}}, open(a.json, "w", encoding="utf-8"))

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""조합별 후반 보스 '다 증강했을 때' 깨지는지(2026-09-23 사용자 "비숍은 30, 팔라딘 50이 최적. 나머지 다 증강했을 때 보스 깨지는 기준을 봐야 —
   썬콜+불독+@, 팬텀+다크나이트, 히어로+@ 로는 깨져야 함").

가정: 딜러 50레벨(직업 프리즘), 팔라딘 50(가드 크러쉬 20·홀리 유니티 = 프리즘일 때), 비숍 30(프레이 ×1.1).
      프리즘 3개 = 조합의 핵심 프리즘 + 나머지(홀리 유니티 / 방어구 부수기 중 나은 것).
      브~골 27개(브 10·실 10·골 7, 중간 등급 값: 방무 4/7/12 · 딜 +8/14/22%)를 딜러들에게 '그 보스 기준 팀 딜 최대'로 탐욕 배분(방무 또는 딜).
      후반 보스(스우~)는 방어율 200~350, 방무는 곱연산(2026-09-24) — 방무가 모자란 딜러는 0.
출력: 조합별 보스마다 팀 DPS × 60초 vs 체력(배수).
"""
import io, os, re, sys, math
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = io.open(os.path.join(ROOT, "tools", "route-sim.py"), encoding="utf-8").read()
cut = src.index("# ---------------- (2) 탐색")
G = {"__name__": "combo", "__file__": os.path.join(ROOT, "tools", "route-sim.py")}
exec(compile(src[:cut], "route", "exec"), G)
ST, BOSS_DEF_AT, bwp, ign_of, SUN, PH = G["ST"], G["BOSS_DEF_AT"], G["boss_with_prism"], G["ign_of"], G["SUN"], G["PH"]
aug_src = io.open(os.path.join(ROOT, "RootDesk", "MyDesk", "RtsAugmentTableLogic.mlua"), encoding="utf-8").read()
_bm = re.search(r'id = "core_ign".*?ign = (\d+)', aug_src)
BUSU = float(_bm.group(1)) if _bm else 0.0   # 2026-09-24 방어구 부수기 삭제(곱연산 시절 조합 검산 — 합연산 티어 모델은 difficulty-sim)
DEF_OVR = eval(os.environ.get("SIM_DEF", "{}"))
CARRY_IGN = eval(os.environ.get("SIM_CIGN", "{}"))
DEFS = {no: DEF_OVR.get(no, d) for no, d in BOSS_DEF_AT.items()}
FP = "아크메이지(불·독)"
AUGS = [("b", 4, 0.08)] * 10 + [("s", 7, 0.14)] * 10 + [("g", 12, 0.22)] * 7
# 조합: 딜러(직업 → 프리즘 보유 1/0), 방무를 몰아줄 핵심 딜러 둘. '@'는 프리즘 없는 딜러 하나(신궁) — 히어로(기본 방무 70)를 @로 넣으면 조합 비교가 흐려진다
COMBOS = {
    "히어로+@": ({"히어로": 1, "신궁": 0}, ["히어로", "신궁"]),
    "팬텀+다크나이트": ({PH: 0, "다크나이트": 1}, [PH, "다크나이트"]),
    "썬콜+불독+@": ({SUN: 1, FP: 1, "신궁": 0}, [SUN, FP]),
}

def team_dps(dealers, alloc_ign, alloc_dmg, holy_on, busu_on, defv):
    # alloc_ign[j] = 받은 방무 증강의 남은 비율 Π(1 − x) — 곱연산
    tot = 0.0
    for j, p in dealers.items():
        raw = bwp(j, 50, p) * (1 + alloc_dmg[j]) * 1.1 * (1.4 if j == holy_on else 1.0)
        keep = (1 - ign_of(j, 50, p, True) / 100) * (1 - (CARRY_IGN.get(j, 0) if p else 0) / 100) * alloc_ign[j] * ((1 - BUSU / 100) if j == busu_on else 1)
        tot += raw * max(0.0, 1 - (defv - 20) / 100 * keep)
    return tot

def best_for(dealers, third, defv, keys2):
    # 방무는 벽을 넘어야 이득이라 한 장씩 탐욕 배분하면 못 넘는다 → 핵심 딜러 둘(keys2)에게 방무 장수(k1, k2)를 통째로 나눠 보고,
    #   남은 증강은 딜로 탐욕 배분. 방무 장수 = 방무가 큰 증강부터
    order = sorted(AUGS, key=lambda x: -x[1])
    best = 0
    holys = [None] if third != "holy" else list(dealers)
    busus = [None] if third != "busu" else list(dealers)
    d1 = keys2[0]; d2 = keys2[1] if len(keys2) > 1 else keys2[0]
    for holy_on in holys:
        for busu_on in busus:
            for k1 in range(0, 28, 1):
                for k2 in range(0, 28 - k1, 1 if d2 != d1 else 28):
                    ign = {j: 1.0 for j in dealers}; dmg = {j: 0.0 for j in dealers}
                    rest = []
                    for i, (g, iv, dv) in enumerate(order):
                        if i < k1: ign[d1] *= 1 - iv / 100
                        elif i < k1 + k2: ign[d2] *= 1 - iv / 100
                        else: rest.append(dv)
                    for dv in rest:
                        cands = []
                        for j in dealers:
                            dmg[j] += dv; cands.append((team_dps(dealers, ign, dmg, holy_on, busu_on, defv), j)); dmg[j] -= dv
                        dmg[max(cands)[1]] += dv
                    best = max(best, team_dps(dealers, ign, dmg, holy_on, busu_on, defv))
    return best

LATE = [s for s in ST if s["kind"] == "boss" and s["no"] in BOSS_DEF_AT]
print("방어율", DEFS, "· 캐리 프리즘 추가 방무", CARRY_IGN, "· 방어구 부수기", BUSU)
print("보스 | 체력 | " + " | ".join(COMBOS))
for s in LATE:
    need = float(s["hp"]) * len(s["mobs"]) / 60
    cells = []
    for name, (dealers, keys) in COMBOS.items():
        v = max(best_for(dealers, t, DEFS[s["no"]], keys) for t in ("holy", "busu"))
        cells.append(f"×{v / need:.2f}")
    print(f"{s['no']} {s['name']}(방어 {DEFS[s['no']]}) | {float(s['hp']) * len(s['mobs']):,.0f} | " + " | ".join(cells))

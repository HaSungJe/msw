# -*- coding: utf-8 -*-
"""밸런스 재계산기 — .info 문서만으로 처음부터(2026-09-24 사용자 ".info 파일 전부 참고해. 너가 계산한 거 못 믿겠으니 싹 다 재계산 — 보스 클리어 효율부터 증강 효율까지").

입력(손으로 옮김 — 각 값 옆에 출처): character.md(기본 공격력·레벨업당·공격속도·무기) · skill.md(스킬 인게임 설명 — 비율·타격·대상·쿨·후딜·레벨) ·
  weapon.md(무기 데미지 기대값) · damage.md(8단계 — 무엇끼리 합, 무엇끼리 곱) · augmentation.md(증강 수치·확률) · level.md(레벨 비용) · attack.md(공격 루프 규칙) ·
  monster.md / 생성기(보스 방어율·체력 — tools/gen-stage-table.py).
계산(damage.md): 1타 = 공격력(①) × 공격력%(② 합) × [보스면 (1 + 보스 공격시 데미지 증가 ③ 합)] × 크리 기대값(④: 1 + 확률 × 크뎀) × 스킬 비율(⑤) ×
  최종 데미지(⑥ 곱 — 보스면 보스 최종) × 무기 기대값(⑦) × 방어(⑧ 합연산: 1 − max(0, 방어율 − 가드 크러쉬 − 방어율 감소 − 방무) ÷ 100).
실전 딜(attack.md): 공격 루프를 0.001초 단위 없이 사건 순서로 600초 돌린다 — 첫 공격 1초, 이후 주기마다. 쿨타임 스킬이 준비되면 기본 공격 대신(표에서 뒤 = 높은 레벨 우선),
  쓴 순간부터 쿨, 후딜(after) 동안 주기를 건너뛴다. 보스전 잠금(드래곤 로어)은 보스 상대에서 제외.
출력: --jobs(레벨별 보스·사냥 DPS) · --augs(증강 1장 가치) · --clear(보스별 조합 × 증강 분배 클리어 배율) · 기본은 전부. --md = balance-detail.md용 마크다운
      --radar(영입 상세 오각형 — 보스 잠재력·사냥 단계 → RtsJobTableLogic.GetRadar 상수 줄, 2026-09-25)
"""
import io, os, re, sys, math, argparse
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SPEED = {"매우느림": 1.5, "느림": 1.25, "보통": 1.0, "빠름": 0.75, "매우빠름": 0.5}          # character.md 헤더
WEAPON = {"두손검": (0.8, 1.2), "양손둔기": (0.75, 1.25), "창": (0.7, 1.5), "스태프": (0.9, 1.1), "완드": (0.85, 1.05),
          "아대": (0.8, 1.3), "단검": (0.7, 1.2), "활": (0.75, 1.3), "석궁": (0.6, 1.35), "케인": (0.85, 1.2)}   # weapon.md
def wmean(w): a, b = WEAPON[w]; return (a + b) / 2

# ---------------------------------------------------------------- 2026-09-24 티어 재설계(.info/tier.md) — 목표 맞춤 수치(--tune이 다시 계산해 출력)
#   1티어(히어로·나이트로드·썬콜·보우): 보스 가산 = damage.md ⑤ 스킬 데미지 '보스 공격 시 +m%p'(bossRatio) · 모든 증강(브~골) 효과 ×3 · 50레벨 프리즘 증강 0장 2.5만
#   2티어(섀도어·팬텀·불독·신궁·다크): 약점 증강만 효과 ×2(프리즘) · 팬텀은 모든 증강 ×1.75(2티어 1등) · 50레벨 프리즘 증강 0장 4만(팬텀 4.4만)
TUNE = dict(hero_V=45, hero_E=422, nl_F=247, sun_BH=30, sun_BT=180, bow_W=142.92, bow_A=341, shad_D=82, shad_crit=40, shad_cd=80, phantom_PH=143, fp_TR=314, marks_TS=503, dk_GI=654, shad_RTD=88, bishop_DP=22, sun_BZ=36)
T1_JOBS = ("히어로", "나이트로드", "썬콜", "보우마스터")
def aug_mul(job, p, stat, n=30):
    """증강 효과 배율(tier.md): 1티어 = 1 + 2 × min(n, 30) ÷ 30(그 1티어가 가진 증강 수 n — 이미 받은 것까지 다 같이, 30개에서 ×3) · 팬텀 ×1.75 전부(2티어 1등) · 나머지 2티어는 약점만 ×2(프리즘이 있을 때)"""
    if job in T1_JOBS: return (1 + 2 * min(n, 30) / 30) if p else 1.0   # 자기 프리즘이 있을 때만(09-24 사용자)
    if job == "팬텀": return 1.75
    if not p: return 1.0
    weak = {"섀도어": ("flat",), "불독": ("crit", "cd"), "신궁": ("flat", "cd"), "다크나이트": ("crit", "cd")}.get(job, ())
    return 2.0 if stat in weak else 1.0

# ---------------------------------------------------------------- 직업 킷(skill.md 인게임 설명 — 레벨 L, 프리즘 p)
# 반환: 능력치 st + 스킬 목록. 스킬 = dict(name, ratio(%), hits, targets, period(기본 공격만 — 없으면 공격속도), cd, after, mobMul, bossHits, bossFinal, forceCrit, dot, halfHits, bossLocked)
def kit(job, L, p=False):
    st = dict(flat=0, pct=100, boss=0, crit=0, cd=20, fin=1.0, finBoss=1.0, ign=0, ignBoss=0, shred=0, vuln=0)   # damage.md 기본: 크확 0 · 크뎀 20
    sk = []
    if job == "히어로":                     # character.md: 40 + 12/레벨, 보통, 두손검
        base, per, spd, w = 40, 12, "보통", "두손검"
        rb = dict(name="레이징 블로우", ratio=140, hits=2, targets=3)
        if L >= 10: st["ign"] = 5                                   # 콤보 어택
        if L >= 20: st["ign"] = 10                                  # 어드벤스드 콤보 어택(추가 10 — 합 10: skill.md 설명 '10레벨 5 + 20레벨 10'? 코드 10)
        if L >= 40: st["fin"] *= 2.0; st["finBoss"] *= 2.0; rb.update(ratio=290, targets=6)   # 어드콤 강화 최종 +100% · 레이징 블로우 강화 +150%
        if L >= 50: st["ignBoss"] = 60; st["fin"] *= 1.15; st["finBoss"] *= 1.15; rb["bossRatio"] = TUNE["hero_V"]   # 발할라: 방무 60(보스) · 최종 +15% · 레이징 블로우 보스 공격 시 +V%p(⑤)
        if p: rb["hits"] = 3; rb["ratio"] += TUNE["hero_E"]   # 인레이지: 3회 · 레이징 블로우 +E%(⑤ 모든 대상 — 09-24 프리즘 보스 가산을 스킬 데미지로)
        sk.append(rb)
    elif job == "팔라딘":                   # 80 + 10, 느림, 양손둔기
        base, per, spd, w = 80, 10, "느림", "양손둔기"
        dc = dict(name="디바인 차지", ratio=120, hits=1, targets=4)
        if L >= 30: st["fin"] *= 1.5; st["finBoss"] *= 1.5           # 디바인 블레싱
        if L >= 50: dc.update(ratio=190, hits=2, targets=6); st["boss"] += 40
        sk.append(dc)
        if L >= 20: sk.append(dict(name="생츄어리", ratio=200, hits=1, targets=15, cd=15, after=1.5, mobMul=2.0))
    elif job == "다크나이트":               # 50 + 10, 느림, 창
        base, per, spd, w = 50, 10, "느림", "창"
        sb = dict(name="스피어 버스터", ratio=80, hits=3, targets=3)
        if L >= 10: st["flat"] += 100                                # 비홀더
        if L >= 20: sb["ratio"] += 50                                 # 숙련
        if L >= 30: st["pct"] += 50                                   # 버서크 공격력 +50%
        if L >= 40: sb["ratio"] += 50; st["boss"] += 25               # 강화
        if L >= 50: st["fin"] *= 1.2; st["finBoss"] *= 1.2; st["ign"] += 50   # 드래곤 로어 패시브 · 2티어 방무 50(2026-09-24 통일)
        if p: sb["ratio"] = (sb["ratio"] + 29) / 2; sb["hits"] = 6; sb["ratio"] += TUNE["dk_GI"]   # 거대화: 보스 공격 시 +GI%p(⑤ — 09-24 사용자 "보스 최종 데미지는 없어, 스킬 데미지로")
        sk.append(sb)
        if L >= 50: sk.append(dict(name="드래곤 로어", ratio=300, hits=1, targets=15, cd=15, after=1.5, mobMul=2.0, bossLocked=True))
    elif job == "보우마스터":               # 30 + 10, 매우빠름(폭풍의 시 0.2초 고정), 활
        base, per, spd, w = 30, 10, "매우빠름", "활"
        bs = dict(name="폭풍의 시", ratio=70, hits=1, targets=1, period=0.2)
        if L >= 10: st["crit"] += 30
        if L >= 20: st["pct"] += 25
        if L >= 30: st["pct"] += 25
        if L >= 50: bs["ratio"] += 23; bs["bossRatio"] = TUNE["bow_W"]; st["ign"] += 70   # 폭풍의 시 강화: +23% · 보스 공격 시 +W%p(⑤) · 1티어 방무 70
        if p: bs = dict(name="애로우 레인", ratio=54 + TUNE["bow_A"], hits=2, targets=1, period=0.2)
        sk.append(bs)
    elif job == "신궁":                     # 50 + 15, 느림, 석궁
        base, per, spd, w = 30, 9, "느림", "석궁"   # 09-24 약점 = 공격력·크뎀(50 + 15 → 30 + 9), 비율 ×5/3
        pc = dict(name="피어싱", ratio=110 * 5 / 3, hits=2, targets=6)
        if L >= 10: st["crit"] += 30
        if L >= 40: st["pct"] += 70
        if L >= 50: pc["ratio"] += 155 * 5 / 3; st["boss"] += 30; st["ign"] += 50   # 2티어 방무 50
        sk.append(pc)
        if p: sk.append(dict(name="트루 스나이핑", ratio=130 * 5 / 3 + TUNE["marks_TS"], hits=10, targets=1, cd=2, forceCrit=True))   # 보스 공격 시 +TS%p(⑤ — 09-24 사용자 "보스 최종 대신 보스 추가 스킬 데미지")
        elif L >= 30: sk.append(dict(name="스나이핑", ratio=130 * 5 / 3, hits=10, targets=1, cd=10))
    elif job == "썬콜":                     # 50 + 3, 보통, 스태프
        base, per, spd, w = 50, 3, "보통", "스태프"
        cl = dict(name="체인 라이트닝", ratio=105, hits=1, targets=6)
        if L >= 10: st["flat"] += 150                                # 메디테이션
        if L >= 20: cl["ratio"] = 355                                 # 체인 라이트닝 강화
        if L >= 40: st["fin"] *= 1.5; st["finBoss"] *= 1.5           # 아케인 에임 최종 +50%
        if L >= 50: st["fin"] *= 4 / 3; st["finBoss"] *= 4 / 3       # 인피니티 최종 +33%(보스 최종 +40%는 09-24 삭제 — 1티어 보스 가산은 템페스트)
        sk.append(cl)
        if L >= 30:
            bz = dict(name="블리자드", ratio=965, hits=1, targets=15, cd=15, after=1.8, mobMul=2.0)   # 후딜 1.8초(2026-09-26 모션 교체 — 전 3.0)
            if p:   # 템페스트: 쿨 2 · 일반 몬스터 30마리 · 보스에게 BH회 집중(1회 BT% — ⑤ 보스 공격 시 BT − 비율) · 모든 대상 +BZ%p · 방무 70 (2026-09-26 30마리·30회)
                bz.update(cd=2, targets=30, bossHits=TUNE["sun_BH"], ratio=bz["ratio"] + TUNE["sun_BZ"])
                bz["bossRatio"] = TUNE["sun_BT"] - bz["ratio"]
                st["ign"] += 70
            sk.append(bz)
    elif job == "불독":                     # 20 + 5, 보통, 스태프(weapon.md)
        base, per, spd, w = 20, 5, "보통", "스태프"
        dotpct = 50   # 2026-09-26 30 → 50, 강화 60 → 80
        if L >= 10: st["flat"] += 100
        if L >= 20: dotpct = 80
        if L >= 40: st["pct"] += 50
        if L >= 50: st["fin"] *= 1.3; st["finBoss"] *= 1.3; st["boss"] += 10; st["ign"] += 50   # 2티어 방무 50
        sk.append(dict(name="포이즌 리전", ratio=0, hits=0, targets=0, cd=15, dot=dict(pct=dotpct, period=2, dur=12)))
        if L >= 30:
            dp = dict(name="도트 퍼니셔", ratio=290, hits=30, targets=1, cd=15, mobMul=0.5)
            if p: dp.update(ratio=TUNE["fp_TR"], hits=60, cd=3)   # 초월(보스 최종 삭제 09-24 — 구체 비율로 맞춤)
            sk.append(dp)
    elif job == "비숍":                     # 20 + 5, 보통, 완드
        base, per, spd, w = 20, 5, "보통", "완드"
        ar = dict(name="엔젤레이", ratio=38, hits=3, targets=1)
        if L >= 10: st["flat"] += 100
        if L >= 40: st["pct"] += 50
        if L >= 50: st["fin"] *= 1.2; st["finBoss"] *= 1.2; st["boss"] += 40
        if p: ar = dict(name="디바인 퍼니시먼트", ratio=27 + TUNE["bishop_DP"], hits=1, targets=6, period=0.2, vuln=20)   # 보스 공격 시 +DP%p(⑤)
        sk.append(ar)
        if L >= 20: sk.append(dict(name="제네시스", ratio=300, hits=1, targets=15, cd=15, after=1.5, mobMul=2.0))
    elif job == "나이트로드":               # 20 + 5, 빠름, 아대
        base, per, spd, w = 20, 5, "빠름", "아대"
        qt = dict(name="쿼드러플 스로우", ratio=110, hits=4, targets=1)
        if L >= 10: st["fin"] *= 1.1; st["finBoss"] *= 1.1
        if L >= 20: st["crit"] += 30; st["cd"] += 25
        if L >= 30: qt["halfHits"] = 4                               # 쉐도우 파트너
        if L >= 40: st["fin"] *= 1.1; st["finBoss"] *= 1.1; st["flat"] += 100
        if L >= 50: st["fin"] *= 1.2; st["finBoss"] *= 1.2
        if p: qt["name"] = "풍마수리검"; qt["ratio"] += 20 + TUNE["nl_F"]; st["ign"] += 70   # 보스 공격 시 +F%p(⑤)
        sk.append(qt)
    elif job == "섀도어":                   # 50 + 10, 매우빠름, 단검
        base, per, spd, w = 30, 6, "매우빠름", "단검"   # 09-24 약점 = 공격력(50 + 10 → 30 + 6), 비율 ×5/3
        sv = dict(name="새비지 블로우", ratio=17.5 * 5 / 3, hits=8, targets=1)
        if L >= 10: st["pct"] += 30
        if L >= 20: st["crit"] += 30; st["cd"] += 20
        if L >= 40: st["pct"] += 20; st["fin"] *= 1.05; st["finBoss"] *= 1.05
        if L >= 50: st["fin"] *= 1.2; st["finBoss"] *= 1.2; st["boss"] += 30; st["ign"] += 50; sv["bossRatio"] = TUNE["shad_RTD"]   # 레디 투 다이: 보스 공격 시 새비지 블로우 +RTD%p(⑤, 전 보스 최종 ×3.96)
        if p:   # 자유전직 — 새비지·메소 익스플로전 영구 잠금, 블레이드 토네이도 + 카르마 퓨리(쿨 5초, 같이) · 크확·크뎀 크게(09-24)
            st["crit"] += TUNE["shad_crit"]; st["cd"] += TUNE["shad_cd"]
            sk.append(dict(name="블레이드 토네이도 + 카르마 퓨리", ratio=(13 * 72 + 17 * 45) / 117 * 5 / 3 + TUNE["shad_D"], hits=117, targets=1, cd=5))
        else:
            sk.append(sv)
            if L >= 30: sk.append(dict(name="메소 익스플로전", ratio=50 * 5 / 3, hits=1, targets=10, cd=8))
    elif job == "팬텀":                     # 100 + 0, 매우빠름(조커 0.1초 고정), 케인
        base, per, spd, w = 100, 0, "매우빠름", "케인"
        jk = dict(name="조커", ratio=192.5, hits=1, targets=1, period=0.1)
        if L >= 20: st["flat"] += 150; st["pct"] += 10
        if L >= 30: st["flat"] += 150; st["pct"] += 10
        if L >= 40: st["fin"] *= 1.1; st["finBoss"] *= 1.1
        if L >= 50: st["crit"] += 50; st["cd"] += 30; st["ign"] += 60; st["boss"] += 60; st["fin"] *= 1.2; st["finBoss"] *= 1.2; jk["bossRatio"] = TUNE["phantom_PH"]   # 블스아이: 보스 공격 시 조커 +PH%p(⑤)
        sk.append(jk)
    else:
        raise KeyError(job)
    st["atk"] = base + per * (L - 1) + st["flat"]
    st["period"] = SPEED[spd]
    st["w"] = wmean(w)
    return st, sk

JOBS = ["히어로", "팔라딘", "다크나이트", "보우마스터", "신궁", "썬콜", "불독", "비숍", "나이트로드", "섀도어", "팬텀"]
TIER = {"히어로": 1, "나이트로드": 1, "썬콜": 1, "보우마스터": 1, "섀도어": 2, "팬텀": 2, "불독": 2, "신궁": 2, "다크나이트": 2, "팔라딘": 4, "비숍": 4}   # 2026-09-24 보우 1티어 · 3티어 → 2티어
AUG_EFF = {1: 1.3, 2: 0.6, 3: 0.6, 4: 1.0}   # damage.md '증강 효율'(50레벨부터, 보스 딜만)

# ---------------------------------------------------------------- 1타 · 로테이션
def hit_dmg(st, k, boss, n_hit_ratio=None):
    ratio = n_hit_ratio if n_hit_ratio is not None else k["ratio"]
    if boss and n_hit_ratio is None: ratio += k.get("bossRatio", 0)   # ⑤ 스킬 데미지 '보스 공격 시 +m%p'(1티어, 09-24)
    crit = min(st["crit"], 100) / 100
    critMul = 1 + (1 if k.get("forceCrit") else crit) * st["cd"] / 100
    v = st["atk"] * st["pct"] / 100 * critMul * ratio / 100 * st["w"]
    if boss:
        v *= (1 + st["boss"] / 100) * st["finBoss"] * k.get("bossFinal", 1.0)
    else:
        v *= st["fin"] * k.get("mobMul", 1.0)
    return v

def cast_dmg(st, k, boss, n_targets=1):
    """시전 1번의 총 데미지(방어 전). 보스 = 대상 1마리. 사냥 = 대상 n마리(표 규칙: 타겟 수만큼)"""
    if k.get("dot"):
        d = k["dot"]; ticks = int(round(d["dur"] / d["period"]))
        crit = min(st["crit"], 100) / 100
        per_tick = st["atk"] * st["pct"] / 100 * (1 + crit * st["cd"] / 100) * d["pct"] / 100 * st["fin"] * st["w"]   # 코드: 틱엔 보스 배율 없음, 방무 100
        return per_tick * ticks * (1 if boss else n_targets)
    hits = k["hits"]
    if boss:
        mult = k.get("bossHits", 1) if k.get("bossHits") else 1
        tot = hit_dmg(st, k, True) * hits * mult
        if k.get("halfHits"): tot += hit_dmg(st, k, True) * 0.5 * k["halfHits"]
        return tot
    t = min(k["targets"], n_targets) if n_targets else k["targets"]
    tot = hit_dmg(st, k, False) * hits * t
    if k.get("halfHits"): tot += hit_dmg(st, k, False) * 0.5 * k["halfHits"] * t
    return tot

def rotation_dps(st, sk, boss, n_targets=40, T=600.0):
    """attack.md 루프: 첫 공격 1초, 주기마다. 준비된 쿨 스킬(뒤쪽 우선) → 기본 공격. 후딜 동안 건너뜀"""
    basic = next((k for k in sk if not k.get("cd")), None)
    period = (basic.get("period") if basic else None) or st["period"]
    cds = [k for k in sk if k.get("cd") and not (boss and k.get("bossLocked"))]
    ready = {k["name"]: 0.0 for k in cds}
    busy = 0.0; t = 1.0; total = 0.0
    while t < T:
        if t >= busy - 1e-9:
            used = None
            for k in reversed(cds):
                if t >= ready[k["name"]] - 1e-9: used = k; break
            if used is not None:
                total += cast_dmg(st, used, boss, n_targets)
                ready[used["name"]] = t + used["cd"]
                busy = t + used.get("after", 0)
            elif basic is not None:
                total += cast_dmg(st, basic, boss, n_targets)
        t += period
    return total / (T - 1.0)

def basic_dps(st, sk, boss):
    basic = next((k for k in sk if not k.get("cd")), None)
    if basic is None: return 0.0
    period = basic.get("period") or st["period"]
    return cast_dmg(st, basic, boss, None if not boss else 1) / period

def defmul(defv, ign, guard=0, shred=0):
    return max(0.0, 1 - max(0.0, defv - guard - shred - ign) / 100)

# ---------------------------------------------------------------- 증강(augmentation.md)
AUG = {   # 등급: [(이름, 능력치, 값, 가중치)]
    "bronze": [("약점 찾기", "crit", v, w) for v, w in ((4, 5), (3, 8), (2, 12))] + [("급소 찌르기", "cd", v, w) for v, w in ((4, 5), (3, 8), (2, 12))] +
              [("무기 연마", "flat", v, w) for v, w in ((25, 5), (20, 8), (15, 12))] + [("전투 감각", "pct", v, w) for v, w in ((4, 5), (3, 8), (2, 12))],
    "silver": [("약점 찾기", "crit", v, w) for v, w in ((7, 4.5), (6, 9), (5, 13.5))] + [("급소 찌르기", "cd", v, w) for v, w in ((7, 4.5), (6, 9), (5, 13.5))] +
              [("무기 연마", "flat", v, w) for v, w in ((60, 4.5), (50, 9), (40, 13.5))] + [("전투 감각", "pct", v, w) for v, w in ((7, 4.5), (6, 9), (5, 13.5))] +
              [("보스 사냥꾼", "boss", v, w) for v, w in ((7, 2), (6, 4), (5, 6))],
    "gold": [("약점 찾기", "crit", v, w) for v, w in ((15, 4), (12, 9), (10, 13.5))] + [("급소 찌르기", "cd", v, w) for v, w in ((15, 4.5), (12, 9), (10, 13.5))] +
            [("무기 연마", "flat", v, w) for v, w in ((90, 4.5), (80, 9), (70, 13.5))] + [("전투 감각", "pct", v, w) for v, w in ((15, 4.5), (12, 9), (10, 13.5))] +
            [("거인 학살자", "boss", v, w) for v, w in ((15, 2), (12, 4), (10, 6))],
}
def apply_aug(st, stat, v, eff=1.0):
    st = dict(st)
    if stat == "flat": st["atk"] += v * eff
    elif stat == "pct": st["pct"] += v * eff
    elif stat == "boss": st["boss"] += v * eff
    elif stat == "crit": st["crit"] += v * eff
    elif stat == "cd": st["cd"] += v * eff
    elif stat == "fin": st["fin"] *= 1 + v * eff / 100; st["finBoss"] *= 1 + v * eff / 100
    return st

def eff_of(job, L): return 1.0   # 증강 효율(AugEff) 삭제 2026-09-24 — 모든 직업 수치 그대로

# 3택1에서 고르는 기대: 등급 풀에서 가중치대로 3장(중복 없음) → 그 유닛 보스 딜을 가장 많이 올리는 1장. 정확한 기대값 = 모든 3장 조합 열거
from itertools import combinations
def best_of_3(job, L, p, st, sk, grade, defv=0, ign=0, guard=0, shred=0):
    pool = AUG[grade]
    base = rotation_dps(st, sk, True)
    gains = [rotation_dps(apply_aug(st, a[1], a[2], aug_mul(job, p, a[1])), sk, True) / base - 1 for a in pool]
    W = sum(a[3] for a in pool)
    # 가중치 비복원 3장 추출 확률로 '셋 중 최대'의 기대 — 순서 있는 추출을 전부 더한다
    exp = 0.0; pick = {}
    n = len(pool)
    for i in range(n):
        wi = pool[i][3] / W
        for j in range(n):
            if j == i: continue
            wj = pool[j][3] / (W - pool[i][3])
            for k in range(n):
                if k in (i, j): continue
                wk = pool[k][3] / (W - pool[i][3] - pool[j][3])
                pr = wi * wj * wk
                b = max((i, j, k), key=lambda x: gains[x])
                exp += pr * gains[b]
                pick[b] = pick.get(b, 0) + pr
    top = max(pick, key=pick.get)
    return exp, pool[top]

# ---------------------------------------------------------------- 출력
def jobs_table():
    out = []
    LV = [1, 10, 20, 30, 40, 50]
    out.append("### 레벨별 보스 DPS — 실전(쿨 스킬 로테이션 포함, 1마리, 방어·파티 버프 제외, 프리즘 없음)")
    out.append("")
    out.append("| Lv | " + " | ".join(JOBS) + " |")
    out.append("|---|" + "---|" * len(JOBS))
    for L in LV:
        cells = []
        for j in JOBS:
            st, sk = kit(j, L)
            cells.append(f"{rotation_dps(st, sk, True):,.0f}")
        out.append(f"| {L} | " + " | ".join(cells) + " |")
    out.append("")
    out.append("### 레벨별 사냥 DPS — 실전(쿨 스킬 로테이션 포함, 대상 = 스킬 타겟 수 최대치까지, 방어 0, 파티 버프 제외, 프리즘 없음)")
    out.append("")
    out.append("| Lv | " + " | ".join(JOBS) + " |")
    out.append("|---|" + "---|" * len(JOBS))
    for L in LV:
        cells = []
        for j in JOBS:
            st, sk = kit(j, L)
            cells.append(f"{rotation_dps(st, sk, False, n_targets=40):,.0f}")
        out.append(f"| {L} | " + " | ".join(cells) + " |")
    out.append("")
    out.append("### 50레벨 프리즘 — 보스 DPS(실전, 증강 없음) · 방무")
    out.append("")
    out.append("| 직업 | 프리즘 없음 | 프리즘 | 배율 | 방무(없음 → 있음) | 사냥 DPS 프리즘 없음 → 있음 |")
    out.append("|---|---|---|---|---|---|")
    for j in JOBS:
        s0, k0 = kit(j, 50); s1, k1 = kit(j, 50, True)
        b0, b1 = rotation_dps(s0, k0, True), rotation_dps(s1, k1, True)
        h0, h1 = rotation_dps(s0, k0, False), rotation_dps(s1, k1, False)
        i0 = s0["ign"] + s0["ignBoss"]; i1 = s1["ign"] + s1["ignBoss"]
        out.append(f"| {j} | {b0:,.0f} | **{b1:,.0f}** | ×{b1 / b0:.2f} | {i0} → {i1} | {h0:,.0f} → {h1:,.0f} |")
    out.append("")
    return out

def aug_table():
    out = []
    out.append("### 증강 1장의 가치 — 50레벨 프리즘 딜러 보스 DPS 상승률(실전 로테이션, 증강 효율 반영, 증강 0장 기준)")
    out.append("")
    cards = [("브 무기 연마 II +20", "flat", 20), ("브 전투 감각 II +3%", "pct", 3), ("브 약점 찾기 II +3", "crit", 3), ("브 급소 찌르기 II +3", "cd", 3),
             ("실 무기 연마 II +50", "flat", 50), ("실 전투 감각 II +6%", "pct", 6), ("실 보스 사냥꾼 II +6%", "boss", 6), ("실 약점 찾기 II +6", "crit", 6),
             ("골 무기 연마 II +80", "flat", 80), ("골 전투 감각 II +12%", "pct", 12), ("골 거인 학살자 II +12%", "boss", 12), ("골 약점 찾기 II +12", "crit", 12), ("골 급소 찌르기 II +12", "cd", 12)]
    out.append("| 직업(효율) | " + " | ".join(c[0] for c in cards) + " |")
    out.append("|---|" + "---|" * len(cards))
    for j in JOBS:
        pj = j not in ("팬텀",); st, sk = kit(j, 50, pj)
        base = rotation_dps(st, sk, True)
        cells = [f"+{(rotation_dps(apply_aug(st, s, v, aug_mul(j, pj, s)), sk, True) / base - 1) * 100:.1f}%" for _, s, v in cards]
        out.append(f"| {j} | " + " | ".join(cells) + " |")
    out.append("")
    out.append("### 3택1 한 장의 기대 가치(가중치대로 뽑힌 3장 중 그 유닛에 가장 좋은 1장 — 50레벨 프리즘, 증강 0장 기준)")
    out.append("")
    out.append("| 직업 | 브론즈 | 실버 | 골드 | 주로 고르는 카드(브 / 실 / 골) |")
    out.append("|---|---|---|---|---|")
    for j in JOBS:
        st, sk = kit(j, 50, j not in ("팬텀",))
        r = [best_of_3(j, 50, True, st, sk, g) for g in ("bronze", "silver", "gold")]
        out.append(f"| {j} | +{r[0][0] * 100:.1f}% | +{r[1][0] * 100:.1f}% | +{r[2][0] * 100:.1f}% | {r[0][1][0]} / {r[1][1][0]} / {r[2][1][0]} |")
    out.append("")
    return out

# ---------------------------------------------------------------- 보스 클리어 효율(보스 17개)
# 보스 방어율·체력·그 라운드 표준 빌드 레벨 = 생성기(tools/gen-stage-table.py — monster.md와 같은 값). 증강 카드 = augmentation.md 지급 라운드(브·실·골) + 루시드 뒤 뽑기(메소 절반, 3,000 + 800씩)
def load_stages():
    GEN = os.path.join(ROOT, "tools", "gen-stage-table.py")
    src = io.open(GEN, encoding="utf-8").read()
    G = {"__name__": "calc", "__file__": GEN}
    exec(compile(src[:src.index("# ======================================================================== 몬스터 크기")], "gen", "exec"), G)
    return G

import random
CARD_ROUNDS = {"bronze": [4, 17, 30, 38, 51, 63, 76, 84, 97, 110], "silver": [8, 21, 34, 42, 55, 68, 80, 89, 101, 114], "gold": [13, 25, 46, 59, 72, 93, 106]}   # augmentation.md
PRISM_ROUNDS = [26, 56, 89]   # 자쿰·시그너스·루시드 처치 뒤

def cards_before(no, G, buy_share=0.5):
    """이 보스 전에 받은 카드 등급 목록(받은 순서). 뽑기 = 90라운드부터 메소의 buy_share, 등급 80/15/4.5%(프리즘 0.5%는 골드로 셈)"""
    out = []
    ev = []
    for g, rs in CARD_ROUNDS.items():
        for r in rs:
            if r < no: ev.append((r, g))
    bank = 0.0; buys = 0
    for s in G["ST"]:
        if s["no"] >= no: break
        if s["no"] >= 90 and s["kind"] == "mob":
            bank += s["meso"] * buy_share
            while bank >= 3000 + 800 * buys:
                bank -= 3000 + 800 * buys; buys += 1
                ev.append((s["no"] + 0.5, "buy"))
    ev.sort()
    return [g for _, g in ev]

def power(st):
    c = min(st["crit"], 100) / 100
    return st["atk"] * st["pct"] * (1 + st["boss"] / 100) * (1 + c * st["cd"] / 100)

def draw3(grade, rng):
    pool = list(AUG[grade]); out = []
    for _ in range(3):
        tot = sum(a[3] for a in pool); r = rng.random() * tot
        for i, a in enumerate(pool):
            r -= a[3]
            if r <= 0: out.append(pool.pop(i)); break
    return out

# 조합(보스 순번에 따라): 시그너스 전은 영입 순서(히어로 1 · 다크나이트 5 · 3번째 26 · 팔라딘 43 · 비숍 47 · 6번째 56), 스우부터는 후반 편성.
#   프리즘 = (자쿰, 시그너스, 루시드) 순서, 받은 '뒤' 보스부터
SCEN = {
    "A 1티어 + 2티어 둘 + 홀리 + 퍼니시": dict(prisms=["enrage", "holy", "dp"], third="신궁", late=["히어로", "보우마스터", "섀도어", "나이트로드"], main="히어로"),
    "B 썬콜 + 1티어 + 2티어 둘 + 홀리": dict(prisms=["enrage", "holy", "tempest"], third="신궁", late=["히어로", "썬콜", "보우마스터", "섀도어"], main="히어로"),
    "C 썬콜 + 2티어 셋 + 홀리": dict(prisms=["tempest", "holy", "phantom"], third="썬콜", late=["팬텀", "썬콜", "보우마스터", "섀도어"], main="팬텀"),
}
PRISM_JOB = {"enrage": "히어로", "tempest": "썬콜", "dp": "비숍", "holy": "팔라딘"}

def team_at(sc, no, G):
    s = next(x for x in G["ST"] if x["no"] == no)
    lv = sorted(s["lv"], reverse=True)
    got = [p for r, p in zip(PRISM_ROUNDS, sc["prisms"]) if r < no]
    if no < 60:
        order = ["히어로", "다크나이트", sc["third"], "팔라딘", "비숍", "썬콜" if sc["third"] != "썬콜" else "신궁"][:len(lv)]
        dealers = [j for j in order if j not in ("팔라딘", "비숍")]
        main = "썬콜" if (sc["third"] == "썬콜" and "tempest" in got) else "히어로"
    else:
        dealers = list(sc["late"])
        if "phantom" not in got and "팬텀" in dealers: dealers[dealers.index("팬텀")] = "히어로"   # 팬텀 해금 전엔 히어로
        order = dealers + ["팔라딘", "비숍"]
        main = sc["main"] if sc["main"] in dealers else dealers[0]
    lvmap = {j: lv[i] if i < len(lv) else 1 for i, j in enumerate(sorted(order, key=lambda j: (j != main, order.index(j))))}
    return order, dealers, main, lvmap, got

def eval_team(order, dealers, main, lvmap, got, stats, no, G):
    defv = G["BOSS_DEF_AT"].get(no, G["BOSS_DEF"])
    pal = "팔라딘" in order; bis = "비숍" in order
    guard = 0
    if pal: guard = 20 if lvmap["팔라딘"] >= 40 else (10 if lvmap["팔라딘"] >= 10 else 0)
    pray = 1.1 if (bis and lvmap["비숍"] >= 30) else 1.0
    vuln = 1.2 if (bis and "dp" in got) else 1.0
    joker = 1.05 if ("팬텀" in order and lvmap.get("팬텀", 0) >= 10) else 1.0
    sharp = any(j in order and lvmap.get(j, 0) >= (40 if j == "보우마스터" else 20) for j in ("보우마스터", "신궁"))
    shred = 0   # 템페스트 방어율 감소 삭제(2026-09-24)
    holy = "holy" in got and pal
    tot = 0.0
    for j in order:
        st, sk = stats[j]
        st2 = dict(st)
        if sharp: st2["crit"] += 20; st2["cd"] += 20
        d = rotation_dps(st2, sk, True) * defmul(defv, st["ign"] + st["ignBoss"], guard, shred)
        if holy and j == main: d *= 1.4
        tot += d
    return tot * pray * vuln * joker

def clear_ratio(scname, no, G, strategy, runs=40, seed=7):
    sc = SCEN[scname]
    order, dealers, main, lvmap, got = team_at(sc, no, G)
    s = next(x for x in G["ST"] if x["no"] == no)
    hp = float(s["hp"]) * len(s["mobs"])
    cards = cards_before(no, G)
    rng = random.Random(seed)
    vals = []
    for _ in range(runs):
        stats = {}
        for j in order:
            p = (j in PRISM_JOB.values() and any(PRISM_JOB.get(q) == j for q in got) and j not in ("팔라딘",)) or (j == "팬텀")
            if j == "비숍": p = "dp" in got
            stats[j] = list(kit(j, lvmap[j], p))
        count = {j: 0 for j in dealers}
        for i, g in enumerate(cards):
            grade = g
            if g == "buy":
                r = rng.random() * 100
                grade = "bronze" if r < 80 else ("silver" if r < 95 else "gold")
            opts = draw3(grade, rng)
            if strategy == "몰아주기":
                recv = [main]
            elif strategy == "70:30":
                n_main = count[main]; tot = sum(count.values())
                recv = [main] if n_main <= 0.7 * (tot + 1) else [min((j for j in dealers if j != main), key=lambda j: count[j])]
            elif strategy == "균등":
                recv = [min(dealers, key=lambda j: count[j])]
            else:   # 최적: 팀 딜이 가장 많이 오르는 (유닛, 카드)
                recv = list(dealers)
            best = None
            base_team = eval_team(order, dealers, main, lvmap, got, {k: tuple(v) for k, v in stats.items()}, no, G) if strategy == "최적" else 0
            for j in recv:
                st, sk = stats[j]; e = eff_of(j, lvmap[j])
                for a in opts:
                    st2 = apply_aug(st, a[1], a[2], e)
                    if strategy == "최적":
                        trial = {k: tuple(v) for k, v in stats.items()}; trial[j] = (st2, sk)
                        score = eval_team(order, dealers, main, lvmap, got, trial, no, G) - base_team
                    else:
                        score = power(st2) / power(st)
                    if best is None or score > best[0]: best = (score, j, st2)
            stats[best[1]][0] = best[2]; count[best[1]] += 1
        vals.append(eval_team(order, dealers, main, lvmap, got, {k: tuple(v) for k, v in stats.items()}, no, G) * 60 / hp)
    vals.sort()
    return sum(vals) / len(vals), vals[len(vals) // 10], vals[len(vals) * 9 // 10], len(cards)

def clear_table(runs=30):
    G = load_stages()
    out = []
    bosses = [s for s in G["ST"] if s["kind"] == "boss"]
    names = {10: "주니어 발록", 26: "자쿰", 29: "피아누스", 43: "혼테일", 47: "핑크빈", 56: "시그너스", 60: "스우", 64: "데미안", 89: "루시드", 110: "윌", 114: "더스크",
             121: "진 힐라", 127: "듄켈", 129: "검마 1", 130: "검마 2", 131: "검마 3", 132: "검마 4"}
    for scname in SCEN:
        out.append(f"### {scname} — 60초 딜 ÷ 체력(평균 · 운 나쁜 10% ~ 좋은 10%), 증강 분배별")
        out.append("")
        out.append("| 순번 | 보스 | 방어율 | 체력 | 받은 카드 | 몰아주기 | 70:30 | 균등 | 최적(팀 딜 최대) |")
        out.append("|---|---|---|---|---|---|---|---|---|")
        for s in bosses:
            no = s["no"]
            cells = []; nc = 0
            for stg in ("몰아주기", "70:30", "균등", "최적"):
                m, lo, hi, nc = clear_ratio(scname, no, G, stg, runs=runs if stg != "최적" else max(6, runs // 5))
                cells.append(("**×%.2f**" % m if m >= 1 else "×%.2f" % m) + f" ({lo:.2f}~{hi:.2f})")
            hp = f'{float(s["hp"]):,.0f}' + (f' ×{len(s["mobs"])}' if len(s["mobs"]) > 1 else "")
            out.append(f"| {no} | {names.get(no, s['name'])} | {G['BOSS_DEF_AT'].get(no, G['BOSS_DEF'])} | {hp} | {nc} | " + " | ".join(cells) + " |")
        out.append("")
    return out

# ---------------------------------------------------------------- 영입 상세 오각형(2026-09-25 사용자): 5단계 = 매우 높음 5 … 매우 낮음 1, 전체 직업 최댓값 비율 80/60/40/20%
JOB_ID = {"히어로": "hero", "팔라딘": "paladin", "다크나이트": "dk", "보우마스터": "bow", "신궁": "marks", "썬콜": "il", "불독": "fp",
          "비숍": "bishop", "나이트로드": "nl", "섀도어": "shad", "팬텀": "phantom"}
def radar_level(ratio):
    if ratio >= 0.8: return 5
    if ratio >= 0.6: return 4
    if ratio >= 0.4: return 3
    if ratio >= 0.2: return 2
    return 1

def radar_table():
    """사냥 = 50레벨·증강 없음·프리즘 없음 사냥 DPS(40마리, 로테이션). 보스(성장 잠재력, 사용자 "최대 효율 증강 기준") = 50레벨 + 자기 프리즘(팬텀 제외) +
    마지막 보스 전까지 받는 카드 전부(cards_before — 뽑기는 브론즈로)를 한 장씩 3택1 기대 최선(best_of_3의 가장 자주 고르는 카드)으로 그 유닛에 몰아준 보스 DPS(방어 0).
    1티어 증강 배율은 카드가 30장을 넘으니 ×3(aug_mul 기본 n=30)"""
    G = load_stages()
    last = max(x["no"] for x in G["ST"] if x["kind"] == "boss")
    cards = ["bronze" if g == "buy" else g for g in cards_before(last, G)]
    hunt = {}; boss = {}
    for j in JOBS:
        st, sk = kit(j, 50)
        hunt[j] = rotation_dps(st, sk, False, n_targets=40)
        p = j != "팬텀"
        st, sk = kit(j, 50, p)
        cache = {}
        for g in cards:
            key = (g, round(st["atk"]), round(st["pct"], 3), round(st["boss"], 3), round(st["crit"], 3), round(st["cd"], 3))
            if key not in cache: cache[key] = best_of_3(j, 50, p, st, sk, g)[1]
            a = cache[key]
            st = apply_aug(st, a[1], a[2], aug_mul(j, p, a[1]))
        boss[j] = rotation_dps(st, sk, True)
    mh = max(hunt.values()); mb = max(boss.values())
    out = ["### 영입 상세 오각형 — 보스 잠재력 · 사냥 (카드 %d장 = 마지막 보스 %d 전까지)" % (len(cards), last), "",
           "| 직업 | 사냥 DPS | 비율 | 단계 | 보스 잠재력 DPS | 비율 | 단계 |", "|---|---|---|---|---|---|---|"]
    lua = []
    for j in JOBS:
        hr = hunt[j] / mh; br = boss[j] / mb
        out.append(f"| {j} | {hunt[j]:,.0f} | {hr:.2f} | {radar_level(hr)} | {boss[j]:,.0f} | {br:.2f} | {radar_level(br)} |")
        lua.append(f"\t\t\t{JOB_ID[j]} = {{ boss = {radar_level(br)}, hunt = {radar_level(hr)} }},")
    out += ["", "RtsJobTableLogic.GetRadar 상수 줄:", "```"] + lua + ["```", ""]
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", action="store_true"); ap.add_argument("--augs", action="store_true"); ap.add_argument("--clear", action="store_true")
    ap.add_argument("--radar", action="store_true")
    a = ap.parse_args()
    if a.radar:
        print("\n".join(radar_table()))
        sys.exit(0)
    allp = not (a.jobs or a.augs or a.clear)
    lines = []
    if a.jobs or allp: lines += jobs_table()
    if a.augs or allp: lines += aug_table()
    if a.clear or allp: lines += clear_table()
    print("\n".join(lines))

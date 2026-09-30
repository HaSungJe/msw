# -*- coding: utf-8 -*-
"""로비·방 대기실 그림 생성기 (Phase 8 ①, 2026-09-28)

Claude 시안(Design 캔버스 "로비 · 방 대기실 시안")의 선 아이콘 SVG를 같은 좌표(24칸, 선 굵기 2.2, 둥근 끝)로 그린다.
흰 선 + 투명 바탕 → 게임에서 SpriteGUIRenderer.Color로 물들인다(RtsLobbyUiLogic.Icon, 색 역할 "icon").
점선 테두리는 쓰는 칸과 같은 크기로 그려 늘어나지 않게 한다(RtsLobbyUiLogic.Dash).

출력: assets/design/lobby/icon-*.png(96×96) · dash-quick.png(400×168) · dash-slot.png(422×330) · dash-ring.png(124×124)
업로드한 RUID는 RtsLobbyUiLogic.IconRUID·Dash에 있다. 다시 그리면 새로 업로드하고 그 RUID로 바꾼다.
실행: python tools/gen-lobby-icons.py
"""
import math
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "design", "lobby")
SS = 8  # 8배로 그려 줄인다(부드러운 가장자리)


def cubic(p0, p1, p2, p3, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def arc(p1, p2, r, large, sweep, n=60):
    # SVG 호(끝점 표기) → 중심 표기 → 점들
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    lam = (dx * dx + dy * dy) / (r * r)
    if lam > 1:
        r = r * math.sqrt(lam)
    sign = -1 if large == sweep else 1
    num = r ** 4 - r * r * dy * dy - r * r * dx * dx
    den = r * r * dy * dy + r * r * dx * dx
    co = sign * math.sqrt(max(0, num / den))
    cx, cy = co * dy + (x1 + x2) / 2, -co * dx + (y1 + y2) / 2
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    da = a2 - a1
    if sweep and da < 0:
        da += 2 * math.pi
    if not sweep and da > 0:
        da -= 2 * math.pi
    return [(cx + r * math.cos(a1 + da * i / n), cy + r * math.sin(a1 + da * i / n)) for i in range(n + 1)]


def circle(cx, cy, r, n=90):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def rrect(x, y, w, h, rad):
    pts = [(x + rad, y), (x + w - rad, y)]
    pts += arc((x + w - rad, y), (x + w, y + rad), rad, 0, 1, 12)[1:]
    pts += [(x + w, y + h - rad)]
    pts += arc((x + w, y + h - rad), (x + w - rad, y + h), rad, 0, 1, 12)[1:]
    pts += [(x + rad, y + h)]
    pts += arc((x + rad, y + h), (x, y + h - rad), rad, 0, 1, 12)[1:]
    pts += [(x, y + rad)]
    pts += arc((x, y + rad), (x + rad, y), rad, 0, 1, 12)[1:]
    return pts


def save_mask(mask, w, h, name):
    mask = mask.resize((w, h), Image.LANCZOS)
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    img.putalpha(mask)
    img.save(os.path.join(OUT, name + ".png"))


def draw_icon(name, paths, size=96, stroke=2.2):
    big = size * SS
    k = big / 24.0
    w = stroke * k
    mask = Image.new("L", (big, big), 0)
    d = ImageDraw.Draw(mask)
    for path in paths:
        pts = [(x * k, y * k) for x, y in path]
        if len(pts) > 1:
            d.line(pts, fill=255, width=int(round(w)))
        rr = w / 2
        for x, y in pts:  # 둥근 끝·꺾임
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=255)
    save_mask(mask, size, size, name)


# 시안 SVG(viewBox 0 0 24 24)와 같은 좌표
ICONS = {
    "bolt": [[(13, 2), (4, 14), (11, 14), (10, 22), (19, 10), (12, 10), (13, 2)]],
    "plus": [[(12, 5), (12, 19)], [(5, 12), (19, 12)]],
    "user": [circle(12, 8, 4), cubic((4, 21), (4, 17), (7.6, 14), (12, 14)) + cubic((12, 14), (16.4, 14), (20, 17), (20, 21))[1:]],
    "users": [
        circle(9, 8, 3.5),
        cubic((2.5, 20), (2.5, 16.4), (5.4, 14), (9, 14)) + cubic((9, 14), (12.6, 14), (15.5, 16.4), (15.5, 20))[1:],
        arc((16, 4.5), (16, 11.5), 3.5, 0, 1),
        cubic((18, 14.5), (20.2, 15.2), (21.5, 17.3), (21.5, 20)),
    ],
    "lock": [rrect(5, 11, 14, 10, 2), [(8, 11), (8, 8)] + arc((8, 8), (16, 8), 4, 0, 1)[1:] + [(16, 11)]],
    "crown": [[(3, 8), (7, 12), (12, 5), (17, 12), (21, 8), (19, 19), (5, 19), (3, 8)]],
    "send": [[(22, 2), (11, 13)], [(22, 2), (15, 22), (11, 13), (2, 9), (22, 2)]],
    "exit": [[(10, 17), (5, 12), (10, 7)], [(5, 12), (16, 12)],
             [(14, 4), (19, 4)] + arc((19, 4), (20, 5), 1, 0, 1, 8)[1:] + [(20, 19)] + arc((20, 19), (19, 20), 1, 0, 1, 8)[1:] + [(14, 20)]],
    "check": [[(5, 12), (10, 17), (19, 7)]],
    "refresh": [arc((20, 11), (17.7, 16.7), 8, 1, 0, 90), [(20, 4), (20, 11), (13, 11)]],
    "chevron": [[(15, 6), (9, 12), (15, 18)]],
    "close": [[(6, 6), (18, 18)], [(18, 6), (6, 18)]],
    "info": [circle(12, 12, 9), [(12, 11), (12, 16)], [(12, 8), (12.01, 8)]],
    "sun": [circle(12, 12, 4), [(12, 2), (12, 4)], [(12, 20), (12, 22)], [(4.9, 4.9), (6.3, 6.3)], [(17.7, 17.7), (19.1, 19.1)],
            [(2, 12), (4, 12)], [(20, 12), (22, 12)], [(4.9, 19.1), (6.3, 17.7)], [(17.7, 6.3), (19.1, 4.9)]],
    "moon": [arc((20, 14.5), (9.5, 4), 8, 0, 1) + arc((9.5, 4), (20, 14.5), 8, 1, 0)[1:]],
    # 게임 채팅 [크게](2026-09-29) — 대각선 양쪽 화살표
    "expand": [[(15, 3), (21, 3), (21, 9)], [(21, 3), (14, 10)], [(9, 21), (3, 21), (3, 15)], [(3, 21), (10, 14)]],
    # 프로필 설정 강조(2026-09-29 사용자 "우측에 연필 모양") — 오른쪽 위로 누운 연필(둥근 머리 · 뾰족 끝) + 머리 쪽 띠
    "pencil": [[(3.8, 16.7), (17.2, 3.3)] + arc((17.2, 3.3), (20.7, 6.8), 2.475, 0, 1)[1:] + [(7.3, 20.2), (2.3, 21.7), (3.8, 16.7)],
               [(15.2, 5.3), (18.7, 8.8)]],
}


def dashed_rrect(name, w, h, rad, stroke=2.0, dash=8.0, gap=6.0):
    # 둘레를 고르게 샘플 → 누적 길이로 점선(한 바퀴에 딱 맞게 주기를 조정)
    mask = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(mask)
    inset = stroke / 2 + 0.5
    rad = min(rad, (w - inset * 2) / 2, (h - inset * 2) / 2)
    pts = rrect(inset, inset, w - inset * 2, h - inset * 2, rad)
    dense = []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) * 4))
        for j in range(n):
            t = j / n
            dense.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    dense.append(pts[-1])
    lengths = [0.0]
    for i in range(1, len(dense)):
        lengths.append(lengths[-1] + math.hypot(dense[i][0] - dense[i - 1][0], dense[i][1] - dense[i - 1][1]))
    period = lengths[-1] / max(1, round(lengths[-1] / (dash + gap)))
    on = dash / (dash + gap) * period
    rr = stroke * SS / 2
    for (x, y), s in zip(dense, lengths):
        if (s % period) < on:
            d.ellipse((x * SS - rr, y * SS - rr, x * SS + rr, y * SS + rr), fill=255)
    save_mask(mask, w, h, name)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for key, paths in ICONS.items():
        draw_icon("icon-" + key, paths)
    dashed_rrect("dash-quick", 400, 168, 18)
    dashed_rrect("dash-slot", 422, 330, 20)
    dashed_rrect("dash-ring", 124, 124, 61, dash=7.0)
    print("lobby icons →", OUT)

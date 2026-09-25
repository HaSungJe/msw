# -*- coding: utf-8 -*-
"""영입 상세 오각형 자산(2026-09-25 — RtsPopupLogic.SpawnRadar).
  radar-web.png  512×512 투명: 정오각형(위 꼭짓점 위) 5겹(단계 1~5, 반지름 = 단계 ÷ 5 × 240px) + 가운데 → 꼭짓점 축 5개. 흰색(틴트는 게임에서)
  right-tri.png  128×128 흰 직각삼각형: 직각 = 왼쪽 아래, 두 다리 = 아래 변·왼쪽 변, 빗변 안티앨리어싱(4배로 그려 축소)
사용: python tools/gen-radar-assets.py  → assets/textures/ 에 두 장
"""
import math, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "textures")
SS = 4

def web():
    N = 512 * SS
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = N / 2
    R = 240 * SS
    def pt(level, i):
        a = math.radians(-90 + 72 * i)
        r = R * level / 5
        return (c + r * math.cos(a), c + r * math.sin(a))
    # 채움(바탕) 아주 옅게
    d.polygon([pt(5, i) for i in range(5)], fill=(255, 255, 255, 18))
    for lv in range(1, 6):
        alpha = 115 if lv == 5 else 60
        pts = [pt(lv, i) for i in range(5)]
        d.line(pts + [pts[0]], fill=(255, 255, 255, alpha), width=3 * SS if lv == 5 else 2 * SS, joint="curve")
    for i in range(5):
        d.line([(c, c), pt(5, i)], fill=(255, 255, 255, 60), width=2 * SS)
    im = im.resize((512, 512), Image.LANCZOS)
    im.save(os.path.join(OUT, "radar-web.png"))

def tri():
    N = 128 * SS
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(0, N), (N, N), (0, 0)], fill=(255, 255, 255, 255))
    im = im.resize((128, 128), Image.LANCZOS)
    im.save(os.path.join(OUT, "right-tri.png"))

if __name__ == "__main__":
    web()
    tri()
    for f in ("radar-web.png", "right-tri.png"):
        print(f, os.path.getsize(os.path.join(OUT, f)), "bytes")

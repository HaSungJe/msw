# -*- coding: utf-8 -*-
"""테마 바닥 타일 4종(엘리니아·페리온·커닝·리스) — ChatGPT 초안(assets/design/themes/floors/*-floor-256.png)을 반복 가능한 256×256 불투명 타일로 보정한다.
  1) 알파 255로(초안 가장자리·전체 알파가 254 이하인 것) — 평균색 위에 합성
  2) 대표색 쪽으로 평균을 옮김(가이드라인 docs/design/theme-presets.md 표의 바닥 대표색, 이동량 SHIFT) · 대비 CONTRAST(엘리니아 큰 잎무늬는 낮춤)
  3) 이음새 제거: 가로 → 세로 순서로 '반 칸 돌린 사본'과 섞는다. 가중치 = 가운데 1 · 가장자리 0(sin²) — 가장자리는 돌린 사본(= 원본 가운데라 이어짐), 돌린 사본의 이음새(가운데 줄)는 원본이 덮는다
  4) 3×3 미리보기 + 가장자리 차이(좌우·상하 평균 절대차) 출력
사용: python tools/gen-theme-floors.py [미리보기 폴더]  → assets/textures/floor-<key>.png
"""
import os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "design", "themes", "floors")
OUT = os.path.join(ROOT, "assets", "textures")
PREV = sys.argv[1] if len(sys.argv) > 1 else None

THEMES = {
    # key: (대표색, 평균 이동량, 대비 배율)
    "ellinia": ("#168E73", 0.8, 0.68),   # 잎무늬가 전투 칸에서 반복돼 보이지 않게 대비를 낮춤(가이드라인)
    "perion": ("#E99245", 0.6, 1.0),
    "kerning": ("#596588", 0.6, 1.0),
    "lith": ("#F1DFB8", 0.6, 1.0),
}

def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=float)

def seamless(a):
    n = a.shape[0]
    w = np.sin(np.pi * (np.arange(n) + 0.5) / n) ** 2          # 가운데 1, 가장자리 0
    wx = w[None, :, None]
    a = a * wx + np.roll(a, n // 2, axis=1) * (1 - wx)         # 가로
    wy = w[:, None, None]
    a = a * wy + np.roll(a, n // 2, axis=0) * (1 - wy)         # 세로
    return a

def edge(a):
    return float(np.abs(a[:, 0] - a[:, -1]).mean()), float(np.abs(a[0] - a[-1]).mean())

for key, (hx, shift, contrast) in THEMES.items():
    im = Image.open(os.path.join(SRC, key + "-floor-256.png")).convert("RGBA")
    a = np.asarray(im).astype(float)
    rgb, al = a[..., :3], a[..., 3:4] / 255.0
    mean = (rgb * al).sum((0, 1)) / max(al.sum(), 1)
    rgb = rgb * al + mean * (1 - al)                          # 알파 255로(평균색 위 합성)
    m = rgb.reshape(-1, 3).mean(0)
    rgb = m + (rgb - m) * contrast                            # 대비
    rgb = rgb + (hexrgb(hx) - m) * shift                      # 대표색 쪽으로
    before = edge(rgb)
    rgb = seamless(rgb)
    after = edge(rgb)
    rgb = np.clip(rgb, 0, 255).round().astype(np.uint8)
    out = Image.fromarray(rgb, "RGB").convert("RGBA")
    path = os.path.join(OUT, "floor-" + key + ".png")
    out.save(path)
    print(key, "edge before LR/TB %.1f/%.1f" % before, "after %.1f/%.1f" % after, "mean", rgb.reshape(-1, 3).mean(0).round(0), path)
    if PREV:
        g = Image.new("RGB", (768, 768))
        t = out.convert("RGB")
        for x in range(3):
            for y in range(3):
                g.paste(t, (x * 256, y * 256))
        g.save(os.path.join(PREV, "floor3x3-" + key + ".png"))

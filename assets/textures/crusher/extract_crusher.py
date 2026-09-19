# -*- coding: utf-8 -*-
# 나무위키 스피어 크러셔 영상(흰 배경 + 용기사 캐릭터) → 이펙트만 알파 PNG 프레임으로.
#   1) 정지 배경(연한 용 워터마크)을 idle 프레임으로 상쇄  2) 흰 배경에서 알파 복원(a = 1 - min(RGB)/255)
#   3) 캐릭터(피부·금창·검은 외곽선·명패) 제거 후 inpaint  4) 발 위치 기준으로 공통 캔버스에 저장
import cv2, numpy as np, os, json

SRC = "frames/f_%03d.png"
IDLE = cv2.imread(SRC % 40).astype(np.float32)          # 이펙트 없는 프레임(배경 워터마크 + 캐릭터 idle)
KEEP = list(range(3, 34, 3))                              # 11프레임 ≈ 33fps × 3 = 90ms 간격
OUT = "crusher_frames_v3"
os.makedirs(OUT, exist_ok=True)

H, W = IDLE.shape[:2]
white = np.full_like(IDLE, 255)
bg_dark = white - IDLE                                    # 배경이 흰색에서 얼마나 어두운지(워터마크 + 캐릭터)

# 캐릭터 실루엣(idle) — 워터마크보다 훨씬 진한 픽셀
idle_sil = (IDLE.min(axis=2) < 200)
idle_sil = cv2.dilate(idle_sil.astype(np.uint8), np.ones((5, 5), np.uint8), iterations=1).astype(bool)
# 찌르기 포즈 실루엣: 이펙트가 거의 빠진 뒤 프레임(24~34)에서 '캐릭터다운' 픽셀(따뜻한 색 또는 어두운 무채색)의 합
thrust = np.zeros((H, W), bool)
for j in range(24, 35):
    Fj = cv2.imread(SRC % j).astype(np.float32)
    Bj, Gj, Rj = Fj[..., 0], Fj[..., 1], Fj[..., 2]
    mnj = Fj.min(axis=2)
    thrust |= ((Rj > Bj + 10) & (mnj < 240)) | ((np.abs(Bj - np.maximum(Rj, Gj)) < 24) & (mnj < 200))
CHAR = idle_sil | thrust
CHAR = cv2.morphologyEx(CHAR.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)).astype(bool)
CHAR = cv2.dilate(CHAR.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1).astype(bool)
cv2.imwrite("char_mask.png", CHAR.astype(np.uint8) * 255)

frames = []
for i in KEEP:
    F = cv2.imread(SRC % i).astype(np.float32)
    # 1) 정지 워터마크 상쇄: 캐릭터 실루엣 밖에서만(캐릭터는 따로 지움)
    corr = F.copy()
    wm = bg_dark.copy()
    wm[idle_sil] = 0
    corr = np.clip(corr + wm, 0, 255)
    # 2) 흰 배경에서 알파 복원
    mn = corr.min(axis=2)
    a = np.clip(1.0 - mn / 255.0, 0, 1)
    a[a < 0.03] = 0
    rgb = np.zeros_like(corr)
    nz = a > 0
    rgb[nz] = np.clip((corr[nz] - (1 - a[nz])[:, None] * 255) / a[nz][:, None], 0, 255)
    # 3) 캐릭터 제거: 실루엣(idle + 찌르기 포즈의 합) 자리를 그냥 구멍(알파 0)으로 둔다.
    #    이펙트가 겹친 프레임에선 캐릭터가 파랗게 물들어 색으로는 못 가르고, 게임에선 그 자리에 우리 아바타가 서 있으니 구멍이 자연스럽다.
    a8 = (a * 255).astype(np.uint8)
    rgb8 = rgb.astype(np.uint8)
    a8[CHAR] = 0
    # 준비 포즈의 창 외곽선(거의 검정 무채색) 찌꺼기 — 이펙트엔 검정이 없으니 지운다
    Bc, Gc, Rc = corr[..., 0], corr[..., 1], corr[..., 2]
    speck = (np.abs(Bc - np.maximum(Rc, Gc)) < 30) & (mn < 130)
    speck = cv2.dilate(speck.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1).astype(bool)
    a8[speck] = 0
    # 3.5) 흰 배경에 흰 하이라이트는 복원이 불가능(용머리 몸통·날개 속살) → 이펙트 영역(외곽선을 크게 닫은 덩어리) 안에서
    #    알파가 낮은 곳을 흰빛 시안으로 채워 "속이 찬" 실루엣으로 만든다. v2(2026-09-16): 사용자 피드백 "너무 비어있고 테두리만 있는 느낌"
    a_f = a8.astype(np.float32) / 255.0
    # 용머리 발사 구간(뒤 5프레임)은 선이 드물어 더 크게 닫는다
    kidx = KEEP.index(i)
    thr, ksz = (0.12, 21) if kidx < 6 else (0.035, 25)
    if kidx < 2: thr = 0.07   # 첫 두 프레임(용 실루엣 등장)은 선이 연하다
    a_med = cv2.medianBlur((a_f * 255).astype(np.uint8), 5).astype(np.float32) / 255.0   # 압축 노이즈 제거
    solid = a_med > thr
    solid = cv2.morphologyEx(solid.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)).astype(bool)
    region = cv2.morphologyEx(solid.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksz, ksz))).astype(bool)
    # 영역 안 구멍(닫힘으로 못 메운 큰 속)도 채운다: 바깥에서 flood fill 한 뒤 반전
    ff = region.astype(np.uint8).copy()
    mask = np.zeros((H + 2, W + 2), np.uint8)
    cv2.floodFill(ff, mask, (0, 0), 2)
    interior = region | (ff != 2)
    interior = cv2.erode(interior.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    fill = interior & ~CHAR
    # v3(사용자 "더 진하게, 영상과 같은 퀄리티"): 원본은 흰 몸통 + 진한 파란 선. 속은 거의 흰색(살짝 파란)으로 α0.85, 선은 알파 ×1.8
    FILL_A = 0.85
    FILL_RGB = np.array([255, 247, 238], np.float32)   # BGR = 흰빛(살짝 파랑)
    w = np.clip((FILL_A - a_f) / FILL_A, 0, 1)         # 알파가 낮을수록 채움 색 비중↑
    w[~fill] = 0
    rgb_f = rgb8.astype(np.float32)
    rgb_f = rgb_f * (1 - w[..., None]) + FILL_RGB[None, None, :] * w[..., None]
    a_line = np.clip(a_f * 1.8, 0, 1)                  # 선(원래 알파가 있는 곳)은 진하게
    a_f = np.where(fill, np.maximum(a_line, FILL_A), a_line)
    # 부드럽게 + 전체 불투명도 올리기
    a_f = cv2.GaussianBlur(a_f, (5, 5), 0)
    a_f = np.clip(a_f ** 0.6, 0, 1)
    rgb_f = cv2.medianBlur(np.clip(rgb_f, 0, 255).astype(np.uint8), 3).astype(np.float32)
    a_f[CHAR] = 0
    a8 = (a_f * 255).astype(np.uint8)
    rgb8 = np.clip(rgb_f, 0, 255).astype(np.uint8)
    rgba = np.dstack([rgb8, a8])  # BGRA
    frames.append(rgba)

# 4) 공통 크롭: 모든 프레임 알파의 합 bbox
union = np.zeros((H, W), bool)
for f in frames:
    union |= f[..., 3] > 8
ys, xs = np.where(union)
x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
# 발 위치(캐릭터 idle bbox 바닥 중앙): x≈161, y≈222 → 크롭 좌표계로
feet = (161 - x0, 222 - y0)
meta = {"frames": [], "crop": [int(x0), int(y0), int(x1), int(y1)], "feet": [int(feet[0]), int(feet[1])], "size": [int(x1 - x0), int(y1 - y0)], "fps": 33.33 / 3}
for k, f in enumerate(frames):
    p = os.path.join(OUT, "crusher_%02d.png" % (k + 1))
    cv2.imwrite(p, f[y0:y1, x0:x1])
    meta["frames"].append(p)
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
print(meta)

# 미리보기 시트: 초록 배경 위에 합성
from PIL import Image
cols = 6
cw, ch = x1 - x0, y1 - y0
sheet = Image.new("RGB", (cols * cw, ((len(frames) + cols - 1) // cols) * ch), (120, 190, 60))
for k, f in enumerate(frames):
    im = Image.fromarray(cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGRA2RGBA))
    sheet.paste(im, ((k % cols) * cw, (k // cols) * ch), im)
sheet.save("crusher_preview_v3.png")
print("preview", sheet.size)

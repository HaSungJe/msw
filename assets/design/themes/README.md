# 현재 사용 중인 테마 자산

| 폴더 | 내용 |
|---|---|
| `scenery/` | 마을 5종 풍경 원본, 1920×1080 배경, 400×240 썸네일 |
| `tracks/` | 현재 적용된 `track-v3-*.png` 5종 |
| `floors/` | 바닥 질감 원본과 생성기 입력 `*-floor-256.png` 4종씩 |
| `decor/` | 엘리니아 거목·페리온 절벽 마을·커닝 공사장·리스 범선 원본 |

바닥 초안은 `tools/gen-theme-floors.py`가 읽는다. 최종 바닥 타일과 축소 장식은 `assets/textures/`에 있으며 RUID는 해당 폴더 README에 기록한다. 테마 정의는 `docs/theme-presets.md` 참고.

옛 트랙형 썸네일과 v2 트랙은 작업 폴더에서 제외했다.

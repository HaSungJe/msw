# 마을 테마 방향 시안

2026-09-25. 다섯 장은 **시각 방향을 비교하기 위한 콘셉트 이미지**다. 실제 게임의 `16×13` 경로, 발판, 중앙 보스 영역과 픽셀 단위로 일치하지 않으므로 `gridRUID`에 직접 올리지 않는다. 실제 트랙은 `tools/gen-track-grid.js`의 경로를 유지한 채 재제작한다.

| key | 파일 | 원작 마을에서 가져온 시각적 핵심 | 실제 적용 시 우선 만들 요소 |
|---|---|---|---|
| `henesys` | `henesys-concept.png` | 버섯 지붕 집, 잔디 언덕, 꽃과 울타리 | 밝은 잔디 바닥, 크림색 돌길, 버섯집·나무 여백 장식 |
| `ellinia` | `ellinia-concept.png` | 거대한 나무줄기, 나무 구멍, 목재 발판·사다리 | 청록 숲 바닥, 뿌리 섞인 돌길, 화면 양쪽의 **대형 나무** |
| `perion` | `perion-concept.png` | 층층이 쌓인 붉은 절벽, 사다리, 로프 다리, 천막 | 적갈색 흙 바닥, 밝은 사암길, 절벽 마을 여백 장식 |
| `kerning` | `kerning-concept.png` | 공사장 철골·목재 발판, 사다리, 황흑 안전 표식, 추락주의 | 회보라 도시 바닥, 밝은 벽돌길, **공사장 건물과 안전 표지** |
| `lith` | `lith-concept.png` | 큰 범선, 흰 항구 건물과 파란 지붕, 석조 부두 | 옅은 모래/석회암 바닥, 목재·돌길, 배·바다·항구 여백 장식 |

옛 빅뱅 이전 빅토리아 아일랜드 마을 화면을 지형·랜드마크 참고로 삼고, 증강 디펜스의 위에서 보는 전투판에 맞게 번역했다. 원작 화면의 옆보기 발판 구조를 그대로 복사하는 방식은 아니다. 구체적인 참고:

- [헤네시스 마을 화면](https://www.maplesea.com/info/map/victoria_island), [옛 헤네시스 지도 탐방](https://www.inven.co.kr/board/maple/2316/1535)
- [옛 엘리니아 지도 탐방](https://www.inven.co.kr/board/maple/2316/1536)
- [페리온 지도](https://maplelandzzul.gg/game-maps/%ED%8E%98%EB%A6%AC%EC%98%A8)
- [커닝시티 공사장 지도](https://maplelandzzul.gg/game-maps/%EC%BB%A4%EB%8B%9D%EC%8B%9C%ED%8B%B0-%EA%B3%B5%EC%82%AC%EC%9E%A5), [추락주의 회고](https://forum.nexon.com/maplepedia/board_view?thread=1965542)
- [리스항구 지도](https://mapledb.kr/search.php?q=104000000&t=map)

## 게임 적용 원칙

1. 전투판 내부에는 바닥 질감과 트랙만 둔다. 나무줄기·절벽·공사장·배 같은 랜드마크는 장식 여백과 카드 썸네일에서 강조한다.
2. 건설 가능 칸, 이동 경로, 유닛, 몬스터가 겹쳐도 잘 읽히는 대비를 우선한다.
3. 테마별 400×240 썸네일은 이 시안을 단순 축소하지 않고, 작은 화면에서 랜드마크가 보이도록 별도 구성한다.
4. 리소스 업로드는 새 RUID로 진행한다. `RtsThemeLogic.GetPresets()`의 기존 key는 유지한다.

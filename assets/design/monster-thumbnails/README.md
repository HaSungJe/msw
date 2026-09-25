# 몬스터·보스 썸네일

현재 `RootDesk/MyDesk/RtsStageTableLogic.mlua`의 스테이지에 실제 등장하는 **247종**을 모두 담았습니다. 일반 몬스터 229종은 `monster/M001.png`부터 `monster/M229.png`, 보스 18종은 `boss/B01.png`부터 `boss/B18.png`입니다.

- 규격: 모든 파일 **256 × 256 px, 투명 배경 RGBA PNG**
- 구성: 원본 스프라이트의 투명 여백을 제거하고 비율을 유지한 채 중앙 배치, 그림 최대 216 × 216 px
- 파일명 키: `RtsStageTableLogic.Monsters`의 ID 그대로 사용
- `manifest.json`: ID, 한글 이름, 종류, PNG 상대 경로, 원본 RUID와 크기
- `source-manifest.json`: 제작에 사용한 공식 MSW 스프라이트 경로
- `contact-sheet-monster.jpg` / `contact-sheet-boss.jpg`: 전체 확인용 목록 이미지. 게임 UI에는 개별 PNG를 사용
- `build.py`: 동일한 결과물을 다시 만드는 스크립트. Python 3와 Pillow 필요

## Claude 연결 가이드

몬스터/보스 데이터를 표시할 때 해당 데이터의 ID로 `manifest.json`의 `id`를 조회하고, `file` 경로를 이 폴더에 결합해 PNG를 표시하면 됩니다. 예: `M001` → `assets/design/monster-thumbnails/monster/M001.png`, `B01` → `assets/design/monster-thumbnails/boss/B01.png`. 이미지에는 테두리나 배경을 넣지 않았으므로 현재 카드 UI의 프레임과 함께 쓰면 됩니다. 표시 크기는 기존 몬스터 아이콘 영역에 맞춰 조정하되 원본 비율을 유지하세요.

`B11` 더스크는 게임 데이터에 `icon` 값이 없어 같은 보스의 공식 `stand/0` 스프라이트를 사용했습니다. `B17`과 `B18` 검은마법사는 게임 데이터의 아이콘이 빛 이펙트여서 썸네일도 해당 이펙트를 따릅니다. 보스의 단계별 구분을 유지하기 위한 것입니다.

게임 로직이나 기존 RUID는 이 폴더를 만들면서 수정하지 않았습니다.

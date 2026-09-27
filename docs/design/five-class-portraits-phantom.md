# 5직업 흉상·팬텀 게임 연결

현재 적용(2026-09-27): 팔라딘·다크나이트·나이트로드·섀도어·팬텀 전용 흉상 5종과 팬텀 대기 3장·조커 8장·별도 카드/고리를 게임에 연결했다. 팬텀 카드는 고리 가장자리가 캐릭터와 살짝 겹치도록 대상 방향 앞 1.10유닛, 높이 1.04에서 출발한다. 실제 대상 거리가 1칸 미만이면 직선, 1칸 이상이면 기존 거리별 포물선으로 날아간다. 카드 1.152×1.728유닛·고리 2.528유닛 크기는 유지한다. 현재 11직업 모두 전용 PNG 외형·흉상 사용. 상세: docs/design/five-class-portraits-phantom.md.

- 흉상: 각 직업 concept.png와 비숍 portrait.png를 참조해 새로 생성한 512×512 투명 PNG.
- 팬텀 몸체: 대기 1→2→1→3(2.2초), 조커 8장(0.40초 반복). 공격마다 몸체 프레임을 초기화하지 않는다.
- 카드: 공격 0.1초마다 2장, 0.05초 간격, 비행 0.4초·판정 0.35초. 카드·고리 독립 회전과 함께 이동. 캐릭터 몸 회전 없음.
- 최종 출발점: 대상 방향 ±1.55, 높이 +1.04(기존0.84에서0.20 위로 조정). 프레임별 손 추적은 사용자 의도와 달라 제거했다.
- 검증: 18/18 리소스 로딩, 좌우 조커 8/8·대기 3/3, 몸체 회전 오류 0, 고리 위치/크기 검사 통과. 앞으로 이동한 출발점은 Maker 좌우 자동재생 화면에서 확인.
- 생성 기록: `.beaver/output/five-class-portraits-phantom/prompts.json`, `generated-sources.json`.
- 흉상·팬텀 최종 사용자 승인 대기.

| 자산 | RUID |
|---|---|
| phantom/wait/01 | `283726be0d0e4cf7baf54840aae336f6` |
| phantom/wait/02 | `0bfd511879954157ba0dbd9bfb8003d9` |
| phantom/wait/03 | `862241619fc444eba0449187c43732a6` |
| phantom/joker/01 | `744518d46677462a9676c54bac715c39` |
| phantom/joker/02 | `34c76f3cdddb430291dc1a8bf6592cf7` |
| phantom/joker/03 | `06752f5a312949e9932d573333d650b0` |
| phantom/joker/04 | `243362d8c268465ea112983c96074d66` |
| phantom/joker/05 | `1095f84d2bc0495cb23aff6b99ad8028` |
| phantom/joker/06 | `e671da47876b4393abc19798852b594d` |
| phantom/joker/07 | `4d67e5ce5ae84a7c8d561ac4859e12fe` |
| phantom/joker/08 | `a4720376ddb54f6c9f41a83af69174b7` |
| phantom/card | `019edd955d0e4e3eac59989654278fac` |
| phantom/ring | `dadc8093850a445394ea6b883e89f4a8` |
| paladin/portrait | `0e14a7ba1554474fb46cb13ab22bdbfb` |
| dark-knight/portrait | `bc09a2f673ba42b6b5989e4ac39a0fc5` |
| night-lord/portrait | `ccb44d85f142402da6de7b5c7ed67d94` |
| shadower/portrait | `69652c3bf48b457d86e649a540eefc1e` |
| phantom/portrait | `844dc3e58c214cfc9aafaee9d12c33dd` |

잠금 표시: 영입 카드의 잠김 문구를 제거하고 캐릭터 중앙 자물쇠(36×44px, 불투명도 58%)를 표시한다. Maker에서 아이콘 렌더링·투명도 확인, 빌드 오류 0. 카드 출발점 수정 뒤 양방향 자동재생 화면에서 본체와 고리가 분리됨을 확인했다.

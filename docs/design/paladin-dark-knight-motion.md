현재 적용(2026-09-27): 팔라딘·다크나이트·나이트로드·섀도어·팬텀 전용 흉상 5종과 팬텀 대기 3장·조커 8장·별도 카드/고리를 게임에 연결했다. 팬텀 카드는 고리 가장자리가 캐릭터와 살짝 겹치도록 대상 방향 앞 1.10유닛, 높이 1.04에서 출발한다. 실제 대상 거리가 1칸 미만이면 직선, 1칸 이상이면 기존 거리별 포물선으로 날아간다. 카드 1.152×1.728유닛·고리 2.528유닛 크기는 유지한다. 현재 11직업 모두 전용 PNG 외형·흉상 사용. 상세: docs/design/five-class-portraits-phantom.md.

# 팔라딘·다크나이트 모션 적용

팔라딘·다크나이트 모션 적용: 승인된 PNG 32장을 새 RUID로 업로드하고 대기·디바인 차지·생츄어리·스피어 버스터·드래곤 로어·거대화 버스터를 연결했다. Maker 32/32 로딩, 양방향 모든 공격 프레임, 대기 3/3, 복귀 24/24, 실행 오류 0 확인. 선택·상세 이미지는 직업별 전용 portrait.png로 교체했다. docs/design/paladin-dark-knight-motion.md 참고.

다크나이트 스피어 버스터 후속 교체: 승인한 상단 → 하단 → 정면의 깊은 찌르기를 적용했다. 거대화는 같은 순서를 두 번 반복한다. 8파일(고유 그림·RUID 6개), 832×832·발 기준 (416,768), 기존 신체 표시 배율·타격 시각·피해·쿨타임은 유지한다. 최신 자산 기록은 .beaver/output/dark-knight-buster/applied-frames.json이다.

## 연결

| 직업 | 액션 | 재생 순서 | 프레임 시간(초) | 합계 |
|---|---|---|---|---|
| paladin | stand1 | 1,2,1,3 | 0.65,0.45,0.65,0.45 | 2.2 |
| paladin | paladinCharge | 1,2,3,4,5,6 | 0.15,0.15,0.08,0.1,0.1,0.17 | 0.75 |
| paladin | paladinSanctuary | 1,2,3,4,5,6 | 0.2,0.2,0.1,0.12,0.13,0.15 | 0.9 |
| dk | stand1 | 1,2,1,3 | 0.65,0.45,0.65,0.45 | 2.2 |
| dk | dkBuster | 1,2,3,4,5,6,7,8 | 0.6,0.05,0.08,0.07,0.08,0.07,0.1,0.15 | 1.2 |
| dk | dkRoar | 1,2,3,4,5,6 | 0.2,0.2,0.2,0.2,0.25,0.35 | 1.4 |
| dk | dkGiantBuster | 1,2,3,4,5,6,7,2,3,4,5,6,7,8 | 0.6,0.05,0.04,0.035,0.04,0.035,0.04,0.035,0.04,0.035,0.04,0.035,0.04,0.135 | 1.2 |

기존 피해·타격 시각·쿨타임·스킬 이펙트는 유지한다. PNG 경로에서 motionDelay는 사용하지 않으므로 버스터의 첫 준비 자세에 기존 0.50초를 포함했다. 거대화는 상단·하단·정면을 두 번 반복해 타격 간격 0.075초에 맞춘다. 비홀더 구체는 없다.

## 리소스

| PNG (assets/design/characters/ 아래) | 새 RUID |
|---|---|
| paladin/frames/divine-charge/motion01.png | `a5be5b20b9d8440ab5af38cc595ba2f8` |
| paladin/frames/divine-charge/motion02.png | `1db1a18d2bde472c88e72ab3d70d14bf` |
| paladin/frames/divine-charge/motion03.png | `6c9a71053f3a4f259dd41e270e4c94bd` |
| paladin/frames/divine-charge/motion04.png | `a17d41771324411b9d1b0b78ddb1bb74` |
| paladin/frames/divine-charge/motion05.png | `cc366fbe0bdb40a38b6efd846aaccb48` |
| paladin/frames/divine-charge/motion06.png | `af6ec8fb94ae40f4abb3002779fc8994` |
| paladin/frames/sanctuary/motion01.png | `cdcbfe6d6e9146a6a1920baa69b90751` |
| paladin/frames/sanctuary/motion02.png | `86cd9fda03684baabc4bfdfe050fac74` |
| paladin/frames/sanctuary/motion03.png | `ba408ac01fcd4974a5b9d15fb910cdf0` |
| paladin/frames/sanctuary/motion04.png | `16619a38e9104bd99c5bc0a0b59a3096` |
| paladin/frames/sanctuary/motion05.png | `0a9d251c2a494888a0f1ebc47927bb15` |
| paladin/frames/sanctuary/motion06.png | `371429c6ddab4a1cb26d06fa3149bea6` |
| paladin/frames/wait/motion01.png | `17e0e0811cd742bea27591ffbc9b723b` |
| paladin/frames/wait/motion02.png | `019b667361c1459c819353dcc5a0ed8b` |
| paladin/frames/wait/motion03.png | `2838ebd8b5d044a693a4c43b0bf77879` |
| dark-knight/frames/dragon-roar/motion01.png | `ed125f0a1730494d95c759927e035556` |
| dark-knight/frames/dragon-roar/motion02.png | `310c4f9feeb3407597dcce8138e66cd5` |
| dark-knight/frames/dragon-roar/motion03.png | `7005c13026024b839785ebf274ca4ea9` |
| dark-knight/frames/dragon-roar/motion04.png | `b95f492ef7bf43a2ab0243d81ea9bc20` |
| dark-knight/frames/dragon-roar/motion05.png | `9c54e19b80b54384a2950c3f9905f560` |
| dark-knight/frames/dragon-roar/motion06.png | `1374b63a6fe14ee2ab0d200b61bf0e97` |
| dark-knight/frames/spear-buster/motion01.png | `0e1c9aecd84f4c10984932aa52441481` |
| dark-knight/frames/spear-buster/motion02.png | `0e1c9aecd84f4c10984932aa52441481` |
| dark-knight/frames/spear-buster/motion03.png | `a1c730f53f0249449329a6c5751e3df3` |
| dark-knight/frames/spear-buster/motion04.png | `6fbf840e8da146fd8951de0e68f631c4` |
| dark-knight/frames/spear-buster/motion05.png | `5a4ae361c00240128dab626b00cd7ca7` |
| dark-knight/frames/spear-buster/motion06.png | `d05450084ea54dc7a22c4a61f1b3d42f` |
| dark-knight/frames/spear-buster/motion07.png | `2aac0b1ea953485085c7c0b53fc4dbf4` |
| dark-knight/frames/spear-buster/motion08.png | `d05450084ea54dc7a22c4a61f1b3d42f` |
| dark-knight/frames/wait/motion01.png | `8e918f5a58d84f0880f30802e53ec1cb` |
| dark-knight/frames/wait/motion02.png | `a97d69b1da2244c3bbe72930a3215557` |
| dark-knight/frames/wait/motion03.png | `469c0c8e7bab4319a830615eb520aa25` |

## 초기 적용 검증 (버스터 후속 교체 전)

- Maker RtsMap, refresh → save → play. 빌드 오류 0, 기존 다른 메서드 정적 경고 10개는 남아 있다.
- LoadSpriteAndWait 32/32, 프레임·시간표 연결 오류 0.
- 실제 SpawnUnit 경로로 팔라딘·다크나이트·거대화 유닛 생성, AvatarRenderer 없음 확인.
- PlayCast 경로 좌우 재생: 차지 6/6, 생츄어리 6/6, 버스터 8/8, 로어 6/6, 거대화 8/8(고유 프레임). 대기 각 3/3, 복귀 총 24/24, 기존 시전 효과 생성 확인.
- 피해량 회귀 및 선택·상세 UI 크기 육안 검수는 이번 모션 확인에 포함하지 않았다. 전용 흉상은 후속 작업.
- 로그·연결 전후 diff: `.beaver/output/paladin-dark-knight-motion/`.

사용자 요청 자동 재생: 현재 Play 세션의 상단 중앙에 왼쪽 팔라딘·가운데 다크나이트·오른쪽 거대화 시험 유닛(ZzWarriorMotion*)을 배치했다. 3.5초마다 스킬을 번갈아 재생하고 좌우 방향을 전환한다. 영구 맵 자산이 아니며 Play 종료 시 사라진다. 실행 스크립트는 .beaver/output/paladin-dark-knight-motion/autoplay.lua.

## 버스터 후속 교체

03번 상단·05번 하단·07번 정면이 타격 자세다. 01=02 준비, 08=06 회수 자세를 공유한다. 긴 창의 전진 폭을 확보하기 위해 이 스킬만 832×832 투명 캔버스를 사용하며 픽셀당 0.002유닛과 바닥 여백 64px을 유지한다. 생성 프롬프트·참조 원본은 `.beaver/output/dark-knight-buster/generated.json`, 정렬은 `normalization.json`, 현재 8파일·RUID·SHA256은 `applied-frames.json`에 저장했다. 이전 32개 업로드 manifest는 초기 버전 이력이다.

후속 Maker 검증: 새 RUID 6/6 로딩, 일반·거대화 모두 좌우 실제 재생 순서 일치 및 대기 복귀 확인(관측 13회). 빌드 오류 0·현재 실행 오류 0. 이전 Play 종료 시 미리보기 반복 타이머 3개에 대한 LEA-3051 정리 경고가 기록되었으며 게임 스크립트 오류와 구분했다. 자동 재생을 복원했고 결과 팝업을 닫았다. 증거: .beaver/output/dark-knight-buster/verification.json.

사용자 최종 확정: 팔라딘·다크나이트는 현재 게임 모션 그대로 승인. 다크나이트는 상단 → 하단 → 정면, 거대화는 같은 순서 두 번 반복.

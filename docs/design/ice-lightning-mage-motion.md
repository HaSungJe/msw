# 썬콜 외형·프레임 적용

제작 규칙은 [docs/unit-art.md](../unit-art.md)를 따른다(이 문서는 썬콜 적용 기록). 원화로 디자인을 정한 뒤 그 비율·색감·의상을 유지하며 대기와 스킬 프레임을 만든다. 별도 레퍼런스 사본은 자산 폴더에 보관하지 않는다. 후속 수정의 시각 기준은 현재 wait/motion01.png다.

| 폴더 (assets/design/characters/ice-lightning-mage/frames 기준) | 파일 | 게임 액션 |
|---|---|---|
| wait | motion01.png | stand1 고정 |
| 체인 라이트닝 | motion01.png, motion02.png, motion03.png | swingO1 |
| 블리자드 | motion01.png, motion02.png, motion03.png | swingO3 |

썬콜의 표정 컨셉은 **은은한 미소**다. 대기는 지팡이를 두 손으로 받쳐 든 조심스러운 전투 준비 자세다. 대기 1장 고정·스킬별 3장 순서 재생이며 흔들림·호흡·회전·크기 변형은 없다. RtsUnitComponent는 대기 중 프레임 시계를 진행하지 않는다.

대기 캔버스 576×576, 발 (288,512). 공격 캔버스 704×704, 발 (352,640). 픽셀당 로컬 0.002유닛. 얼굴 영역을 약 101.5px 너비로 맞춰 표시 크기를 통일하고 실제 자세에 따른 변화만 남겼다. 체인은 0.30/0.15/0.35초, 블리자드는 0.50/1.70/0.80초(총 3초). 프레임 표시와 대기 복귀는 GetMageSkinFrameDurations를 공유한다.

RUID는 RtsJobTableLogic.GetMageSkinFrames의 단일 표에 등록한다:

| 결과물 | RUID |
|---|---|
| wait/motion01.png | fe0c6be3795d49e29a311b3edb8e89ab |
| chain-lightning/motion01.png | 66b1f0af75c745bdaf10c9710486b867 |
| chain-lightning/motion02.png | 0c4635067dcc4aae9ed3987fc3820dcd |
| chain-lightning/motion03.png | 307d3b6aa3d7485d932c9fcde44642ed |
| blizzard/motion01.png | cfb678afe3fe423ca87a610f41f5c989 |
| blizzard/motion02.png | 08f5c40cb8fa4af28fab2f6b996fdd41 |
| blizzard/motion03.png | 3821ebdc6c2346c2b2561fec50b9900c |

흉상은 캐릭터 폴더의 portrait.png(512×512 투명 PNG)이며 GetMagePortraitRUID로 연결한다. 선택창 140×140, 상세정보 176×176 표시를 실제 Maker 화면에서 확인했다. 프레임·흉상은 내장 image_gen으로 제작했다.


최종 적용 확인: Maker에서 최종 7장 RUID로 실제 시전을 재생했다. 체인 3장 순서 후 약 0.84초에 대기 복귀, 블리자드 0.001/0.513/2.204초에 각 프레임 진입 후 3.021초에 대기 복귀를 실측했다. 블리자드 도중 이전 효과의 대기 복귀 호출을 넣어도 시전이 유지됐다. 대기 시계 0·회전 0 고정을 확인했다. 게임 대기 화면을 확대해 최종 wait/motion01.png와 비교했으며 표시 RUID fe0c6be3795d49e29a311b3edb8e89ab·576×576 일치, 기본 AvatarRenderer 없음도 확인했다. 스킬 폴더는 chain-lightning·blizzard로 통일한다.

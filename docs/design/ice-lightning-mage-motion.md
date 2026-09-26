# 아크메이지(썬·콜) 외형·모션 적용

승인 원화 기반 PNG를 기본 MSW 아바타 대신 사용한다. 새 프레임과 흉상을 리소스로 등록하고 게임 표에 연결했다. Maker 재생 검증 상태는 [공통 적용 기록](unit-motion.md)을 따른다.

## 외형·표정

연한 파란 긴 머리, 검은 리본과 푸른 보석, 흰색·남색 의상, 푸른 결정 지팡이와 떠 있는 마법책. 표정은 은은한 미소. 지팡이를 두 손으로 받쳐 든 조심스러운 전투 준비 자세를 유지한다.

현재 wait/motion01.png를 외모·비율 기준으로 삼는다. 매끈한 2D SD 그림체와 같은 의상·색·소품을 유지한다. 대기는 3장의 작은 호흡을 반복하며 발을 고정한다. 몸 전체의 회전·확대·이동이나 크로스페이드로 움직이지 않는다.

## 파일·시간

기준 경로: `assets/design/characters/ice-lightning-mage/`. 대기 576×576·발 (288,512), 공격 704×704·발 (352,640), 흉상 512×512 투명. 캐릭터 픽셀당 로컬 0.002유닛이며 모든 자세에 같은 배율을 쓴다.

| 동작 | 폴더·파일 | 선택 키 | 프레임별 시간 | 합계 |
|---|---|---|---|---|
| 대기 | frames/wait/motion01~03.png | stand1 | 0.65/0.45/0.65/0.45초 (01→02→01→03 반복) | 2.20초 |
| 체인 라이트닝 | frames/chain-lightning/motion01~05.png | swingO1 | 0.18/0.12/0.08/0.07/0.35초 | 0.80초 |
| 블리자드 | frames/blizzard/motion01~05.png | swingO3 | 0.21/0.09/0.93/0.09/0.48초 | 1.80초 |

체인 라이트닝은 0.80초, 블리자드·템페스트는 1.8초 뒤 대기로 복귀한다. 블리자드는 1.32초에 타격하며 템페스트는 0.72초부터 0.042초 간격으로 판정한다. 두 버전의 시전·후딜은 1.8초이며 낙하 이펙트도 5/3배속으로 맞춘다. 체인의 빔·타격 시점은 유지한다.

스킬 피해량·공격 주기·대상·쿨타임은 유지한다. 블리자드의 시전·후딜과 판정 지연은 최신 사용자 요청에 따라 0.6배로 줄였다. 패시브는 별도 공격 프레임을 만들지 않는다. 흉상은 portrait.png로 분리하여 영입과 상세정보에 공용 연결한다.

## 리소스 연결

| 결과물 | RUID |
|---|---|
| frames/wait/motion01.png | `fe0c6be3795d49e29a311b3edb8e89ab` |
| frames/wait/motion02.png | `6b91e70ed2a64198a41f368191d834c8` |
| frames/wait/motion03.png | `0f16c5bda207468aa1fe9dcb05cb4ed6` |
| frames/chain-lightning/motion01.png | `66b1f0af75c745bdaf10c9710486b867` |
| frames/chain-lightning/motion02.png | `b2bd84ff10da4d40a6e1f0e80a90c8f6` |
| frames/chain-lightning/motion03.png | `0c4635067dcc4aae9ed3987fc3820dcd` |
| frames/chain-lightning/motion04.png | `263444c070344cceb0196534f9997395` |
| frames/chain-lightning/motion05.png | `307d3b6aa3d7485d932c9fcde44642ed` |
| frames/blizzard/motion01.png | `cfb678afe3fe423ca87a610f41f5c989` |
| frames/blizzard/motion02.png | `d0415a8c09d746868c66b9d776babdf1` |
| frames/blizzard/motion03.png | `08f5c40cb8fa4af28fab2f6b996fdd41` |
| frames/blizzard/motion04.png | `7b877eaff02f4cc6b408f82d4a3f9e19` |
| frames/blizzard/motion05.png | `3821ebdc6c2346c2b2561fec50b9900c` |
| portrait.png | `f93cfcc7a46d428cb6ed2bb3d71fc986` |

`RtsJobTableLogic.HasMageSkin/GetMageSkinFrames/GetMageSkinFrameDurations/GetMagePortraitRUID`가 연결 기준이다. `RtsUnitComponent`는 대기 반복과 공격 시간표를 재생하고 좌우 방향을 맞춘다. `RtsSkillFxLogic.PlayCast/ReturnStand/CheckLoops`가 단발·반복 공격과 복귀를 제어한다.

## 제작·확인

내장 imagegen으로 승인된 앞뒤 자세 사이 연결 프레임을 그렸다. Sharp로 전체 등비 축소·투명 캔버스·발 위치만 정렬하고 얼굴 크기·의상·색과 연속 자세를 나란히 대조했다. 파일 크기·알파·해시·프레임 순서와 시간표를 검사했다. 게임 검증 결과는 공통 적용 기록에 별도 기록한다.

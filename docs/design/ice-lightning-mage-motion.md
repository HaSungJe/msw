# 아크메이지(썬·콜) 외형·모션 적용

승인 원화 기반 PNG를 기본 MSW 아바타 대신 사용한다. 새 프레임과 흉상을 리소스로 등록하고 게임 표에 연결했다. Maker 재생 검증 상태는 [공통 적용 기록](unit-motion.md)을 따른다.

## 외형·표정

연한 파란 긴 머리, 검은 리본과 푸른 보석, 흰색·남색 의상, 푸른 결정 지팡이와 떠 있는 마법책. 표정은 은은한 미소. 지팡이를 두 손으로 받쳐 든 조심스러운 전투 준비 자세를 유지한다.

사용자가 승인한 concept.png의 외형·비율로 대기와 공격 13장 PNG를 보정했다. 수정 PNG 업로드·새 RUID 연결 완료. Maker 재시작 검증 결과는 character-proportions.md 참고. 매끈한 2D SD 그림체와 같은 의상·색·소품을 유지한다. 대기는 3장의 작은 호흡을 반복하며 발을 고정한다. 몸 전체의 회전·확대·이동이나 크로스페이드로 움직이지 않는다.

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
| frames/wait/motion01.png | `31f7d3dc8bde42d6905eca8ca3d3d3aa` |
| frames/wait/motion02.png | `7480c71e7fc7406a89e74930c407ad87` |
| frames/wait/motion03.png | `440ab4519beb44f39a820aab4d2ef864` |
| frames/chain-lightning/motion01.png | `f986bf2671c04e11b2f6aaf708f0c2bb` |
| frames/chain-lightning/motion02.png | `63a019d7ca084d78b084c29536c14999` |
| frames/chain-lightning/motion03.png | `02cde524cf654ae8b6000e402cbd0a4f` |
| frames/chain-lightning/motion04.png | `ebdb54d66e9042ffa2a2d35dd4732c89` |
| frames/chain-lightning/motion05.png | `de4d62586d274d28a336adf401e8ecde` |
| frames/blizzard/motion01.png | `3166883e4dbb4fe68eade2f2605468f1` |
| frames/blizzard/motion02.png | `7b663ea7d9da42bf8a497213cca04848` |
| frames/blizzard/motion03.png | `24bee0fe7428442196ecb31813b6ba59` |
| frames/blizzard/motion04.png | `f1f16a077dee4a718e7f52d73545d2ae` |
| frames/blizzard/motion05.png | `0ca54631539d40e7b708b9f9609daa7e` |
| portrait.png | `f93cfcc7a46d428cb6ed2bb3d71fc986` |

`RtsJobTableLogic.HasMageSkin/GetMageSkinFrames/GetMageSkinFrameDurations/GetMagePortraitRUID`가 연결 기준이다. `RtsUnitComponent`는 대기 반복과 공격 시간표를 재생하고 좌우 방향을 맞춘다. `RtsSkillFxLogic.PlayCast/ReturnStand/CheckLoops`가 단발·반복 공격과 복귀를 제어한다.

## 제작·확인

내장 imagegen으로 승인된 앞뒤 자세 사이 연결 프레임을 그렸다. Sharp로 전체 등비 축소·투명 캔버스·발 위치만 정렬하고 얼굴 크기·의상·색과 연속 자세를 나란히 대조했다. 파일 크기·알파·해시·프레임 순서와 시간표를 검사했다. 게임 검증 결과는 공통 적용 기록에 별도 기록한다.

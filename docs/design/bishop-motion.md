# 비숍 외형·모션 적용

승인 원화 기반 PNG를 기본 MSW 아바타 대신 사용한다. 새 프레임과 흉상을 리소스로 등록하고 게임 표에 연결했다. Maker 재생 검증 상태는 [공통 적용 기록](unit-motion.md)을 따른다.

## 외형·표정

애쉬 베이지 긴 머리와 옆머리 땋은 장식, 금빛 눈, 흰색·금색·딥틸 성직자 의상, 파란 보석, 날개 지팡이와 떠 있는 책. 기본은 차분하고 은은한 미소, 제네시스는 눈 감은 기도 표정.

현재 wait/motion01.png를 외모·비율 기준으로 삼는다. 매끈한 2D SD 그림체와 같은 의상·색·소품을 유지한다. 대기는 3장의 작은 호흡을 반복하며 발을 고정한다. 몸 전체의 회전·확대·이동이나 크로스페이드로 움직이지 않는다.

## 파일·시간

기준 경로: `assets/design/characters/bishop/`. 대기 576×576·발 (288,512), 공격 704×704·발 (352,640), 흉상 512×512 투명. 캐릭터 픽셀당 로컬 0.002유닛이며 모든 자세에 같은 배율을 쓴다.

| 동작 | 폴더·파일 | 선택 키 | 프레임별 시간 | 합계 |
|---|---|---|---|---|
| 대기 | frames/wait/motion01~03.png | stand1 | 0.65/0.45/0.65/0.45초 (01→02→01→03 반복) | 2.20초 |
| 엔젤레이 | frames/angel-ray/motion01~05.png | swingO1 | 0.09/0.06/0.18/0.12/0.35초 | 0.80초 |
| 제네시스 | frames/genesis/motion01~05.png | swingO3 | 0.35/0.15/0.30/0.15/0.55초 | 1.50초 |
| 디바인 퍼니시먼트 | frames/divine-punishment/motion01~05.png | divinePunishment | 0.15/0.10/0.15/0.10/0.30초 (반복) | 0.80초 |

제네시스는 눈 감고 몸 중앙의 지팡이를 양손으로 쥔 기도→오른손에 지팡이를 남겨 양팔 낮게 펼치기→유지다. 판정 1.1초·시전 1.5초 유지. 디바인 퍼니시먼트는 0.2초마다 요청해도 시계를 초기화하지 않고 0.8초 주기를 반복하며, 공격이 끊기면 대기로 돌아간다. 프레이는 비숍 자신을 포함한다.

스킬 피해량·공격 주기·대상·쿨타임은 바꾸지 않는다. 패시브는 별도 공격 프레임을 만들지 않는다. 흉상은 portrait.png로 분리하여 영입과 상세정보에 공용 연결한다.

## 리소스 연결

| 결과물 | RUID |
|---|---|
| frames/wait/motion01.png | `99dcc70fd0c04167aa3c7bebdd72bb5b` |
| frames/wait/motion02.png | `049e7e1c48364faca8efbed9ddca1afc` |
| frames/wait/motion03.png | `7b64b5c05ae444f8baab5737fdcff112` |
| frames/angel-ray/motion01.png | `074de3777cbb42839c997bd1f1f958ae` |
| frames/angel-ray/motion02.png | `72e53ccff7c74860b1cf984fa020720d` |
| frames/angel-ray/motion03.png | `a68dc71362dd47119b9477d261175de5` |
| frames/angel-ray/motion04.png | `9781d9083bac4ea786fd95228d147f92` |
| frames/angel-ray/motion05.png | `2246d2a21d1948c1b1b57d56f7776d63` |
| frames/genesis/motion01.png | `55f8fb5d2d4f45ab9bae87a6a79837af` |
| frames/genesis/motion02.png | `8814b38104ea4eb1bd7e4ee22e88fa0b` |
| frames/genesis/motion03.png | `97aab06bc9c64d6faa2caee8105443cd` |
| frames/genesis/motion04.png | `485d02497a384434a91be5a7396cac8c` |
| frames/genesis/motion05.png | `23f7adea4a5246f2995c3c1593b382ae` |
| frames/divine-punishment/motion01.png | `fa8ad8e0822a45368697bc884853d364` |
| frames/divine-punishment/motion02.png | `a235e087ff374bec8f71c2453dc31bdc` |
| frames/divine-punishment/motion03.png | `bdd116091aa447d9927b5f7ed0375fab` |
| frames/divine-punishment/motion04.png | `e5df8c553e8b4870a0db442531e0057b` |
| frames/divine-punishment/motion05.png | `9345eeebfda54f2690c9849661bcd988` |
| portrait.png | `778abb348ac2432eb2ca8916a0ce24b9` |

`RtsJobTableLogic.HasMageSkin/GetMageSkinFrames/GetMageSkinFrameDurations/GetMagePortraitRUID`가 연결 기준이다. `RtsUnitComponent`는 대기 반복과 공격 시간표를 재생하고 좌우 방향을 맞춘다. `RtsSkillFxLogic.PlayCast/ReturnStand/CheckLoops`가 단발·반복 공격과 복귀를 제어한다.

## 제작·확인

내장 imagegen으로 승인된 앞뒤 자세 사이 연결 프레임을 그렸다. Sharp로 전체 등비 축소·투명 캔버스·발 위치만 정렬하고 얼굴 크기·의상·색과 연속 자세를 나란히 대조했다. 파일 크기·알파·해시·프레임 순서와 시간표를 검사했다. 게임 검증 결과는 공통 적용 기록에 별도 기록한다.

# 아크메이지(불·독) 외형·모션 적용

승인 원화 기반 PNG를 기본 MSW 아바타 대신 사용한다. 새 프레임과 흉상을 리소스로 등록하고 게임 표에 연결했다. Maker 재생 검증 상태는 [공통 적용 기록](unit-motion.md)을 따른다.

## 외형·표정

백금빛 가운데 가르마 웨이브와 검정 리본의 두 갈래 머리, 금빛 눈, 검정·금색 자수 망토와 흰 높은 칼라, 검정 주름치마·레이스·갈색 금장 부츠. 호박색 구체 스태프와 진홍색 마법서. 표정은 차분하고 자신감 있는 옅은 미소.

현재 wait/motion01.png를 외모·비율 기준으로 삼는다. 매끈한 2D SD 그림체와 같은 의상·색·소품을 유지한다. 대기는 3장의 작은 호흡을 반복하며 발을 고정한다. 몸 전체의 회전·확대·이동이나 크로스페이드로 움직이지 않는다.

## 파일·시간

기준 경로: `assets/design/characters/fire-poison-mage/`. 대기 576×576·발 (288,512), 공격 704×704·발 (352,640), 흉상 512×512 투명. 캐릭터 픽셀당 로컬 0.002유닛이며 모든 자세에 같은 배율을 쓴다.

| 동작 | 폴더·파일 | 선택 키 | 프레임별 시간 | 합계 |
|---|---|---|---|---|
| 대기 | frames/wait/motion01~03.png | stand1 | 0.65/0.45/0.65/0.45초 (01→02→01→03 반복) | 2.20초 |
| 포이즌 리전 | frames/poison-region/motion01~05.png | poisonRegion | 0.25/0.15/0.30/0.15/0.35초 | 1.20초 |
| 도트 퍼니셔 | frames/dot-punisher/motion01~05.png | dotPunisher | 0.20/0.15/0.25/0.15/0.45초 | 1.20초 |

포이즌 리전은 지팡이를 들고 무릎을 굽혀 내려찍은 뒤 회복한다. 내려찍는 0.40초에 독 지대·시전음이 시작한다. 도트 퍼니셔·초월은 한쪽 위→머리 위 원호→반대편 휘두르기이며 0.35초부터 구체·시전 효과가 시작한다. 두 스킬은 각 1.20초, 구체 대기 0.85초와 기존 피해 판정 시각을 유지한다.

스킬 피해량·공격 주기·대상·쿨타임은 바꾸지 않는다. 패시브는 별도 공격 프레임을 만들지 않는다. 흉상은 portrait.png로 분리하여 영입과 상세정보에 공용 연결한다.

## 리소스 연결

| 결과물 | RUID |
|---|---|
| frames/wait/motion01.png | `762ba8485e584f60a94bc71631ee7881` |
| frames/wait/motion02.png | `43f43917582b4fe6848b525f32d69652` |
| frames/wait/motion03.png | `49312816d1bb4c2d87f0452e8af0f89b` |
| frames/poison-region/motion01.png | `3d29ef1ad55541d2a91af4400a0a22ed` |
| frames/poison-region/motion02.png | `4669d925ba604b28852c02b0baa4a567` |
| frames/poison-region/motion03.png | `413bb52e0b4f47cabe7600bab0a89919` |
| frames/poison-region/motion04.png | `d3360cf51ebf48e1ba9d5b9f1d58425e` |
| frames/poison-region/motion05.png | `b987d27c6aba4867abfd690cf7960cd8` |
| frames/dot-punisher/motion01.png | `61f1428a7d9d4bd7aa94d7f57ceb3ab2` |
| frames/dot-punisher/motion02.png | `dfd12d4d6d1e4ab28d76cbb4e7779264` |
| frames/dot-punisher/motion03.png | `1f61ca3ebc5e46a381af77bdadf5e3d3` |
| frames/dot-punisher/motion04.png | `16de092651e1436cb7bffb5ec142d6c0` |
| frames/dot-punisher/motion05.png | `2581e6d505a2401aab26d85c57cca9df` |
| portrait.png | `81c1c00cd1aa4ff3b08f9894b42c819b` |

`RtsJobTableLogic.HasMageSkin/GetMageSkinFrames/GetMageSkinFrameDurations/GetMagePortraitRUID`가 연결 기준이다. `RtsUnitComponent`는 대기 반복과 공격 시간표를 재생하고 좌우 방향을 맞춘다. `RtsSkillFxLogic.PlayCast/ReturnStand/CheckLoops`가 단발·반복 공격과 복귀를 제어한다.

## 제작·확인

내장 imagegen으로 승인된 앞뒤 자세 사이 연결 프레임을 그렸다. Sharp로 전체 등비 축소·투명 캔버스·발 위치만 정렬하고 얼굴 크기·의상·색과 연속 자세를 나란히 대조했다. 파일 크기·알파·해시·프레임 순서와 시간표를 검사했다. 게임 검증 결과는 공통 적용 기록에 별도 기록한다.

- 도트 퍼니셔·초월 구체는 최초 생성부터 최대 5초. 소모되지 않은 구체는 현재 위치에서 제거하며 서버의 예약 타격·재조준도 만료 검사한다. 재조준해도 수명은 초기화하지 않는다.

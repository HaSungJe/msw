# 히어로 외형·모션 적용

승인 원화 기반 PNG를 기본 MSW 아바타 대신 사용한다. 새 프레임과 흉상을 리소스로 등록하고 게임 표에 연결했다. Maker 재생 검증 상태는 [공통 적용 기록](unit-motion.md)을 따른다.

## 외형·표정

갈색의 짧고 풍성한 머리, 푸른 눈, 은색 귀걸이, 검정·은색 갑옷과 금색 문양, 붉은 가슴 보석과 망토, 은색 양손검·금색/붉은 보석 손잡이. 대기는 자신감 있는 옅은 미소, 공격은 입을 다문 집중한 표정.

현재 wait/motion01.png를 외모·비율 기준으로 삼는다. 매끈한 2D SD 그림체와 같은 의상·색·소품을 유지한다. 대기는 3장의 작은 호흡을 반복하며 발을 고정한다. 몸 전체의 회전·확대·이동이나 크로스페이드로 움직이지 않는다.

## 파일·시간

기준 경로: `assets/design/characters/hero/`. 대기 576×576·발 (288,512), 공격 704×704·발 (352,640), 흉상 512×512 투명. 캐릭터 픽셀당 로컬 0.002유닛이며 모든 자세에 같은 배율을 쓴다.

| 동작 | 폴더·파일 | 선택 키 | 프레임별 시간 | 합계 |
|---|---|---|---|---|
| 대기 | frames/wait/motion01~03.png | stand1 | 0.65/0.45/0.65/0.45초 (01→02→01→03 반복) | 2.20초 |
| 레이징 블로우 | frames/raging-blow/motion01~08.png | swingO3 | 0.06/0.18/0.06/0.12/0.06/0.12/0.18/0.12초 | 0.90초 |
| 인레이지 레이징 블로우 | frames/enraged-raging-blow/motion01~07.png | enragedRagingBlow | 0.18/0.12/0.12/0.08/0.12/0.08/0.20초 | 0.90초 |

일반기 01~08은 모두 개인 검 없는 몸체다. 원본 fa2bfe8ff4f543fb815dd7ee5e02eac9의 스프라이트 14장을 같은 시계로 재생하고 손·손잡이 좌표를 맞춘다. 기존 이펙트 월드 배율 2.0을 유지한다. 픽셀당 로컬 크기는 2/(부모 배율×PPU)이며 현재 PPU 100·부모 2에서 0.01유닛(캐릭터 픽셀의 5배). 첫 12장 각 0.06초·끝 2장 각 0.03초, 0.78초에 검 효과를 숨기고 0.90초에 대기 복귀. 고정 원점의 일반기 클립은 중복 생성하지 않는다. 인레이지는 개인 검을 제거한 7장과 기존 불꽃 참격 클립을 사용하며 전용 액션 enragedRagingBlow로 구분한다. 주요 자세는 0.30/0.50/0.70초의 타격에 맞춘다. 일반기 판정 0.40/0.65초·사운드 0.24초는 유지한다.

스킬 피해량·공격 주기·대상·쿨타임은 바꾸지 않는다. 패시브는 별도 공격 프레임을 만들지 않는다. 흉상은 portrait.png로 분리하여 영입과 상세정보에 공용 연결한다.

## 리소스 연결

| 결과물 | RUID |
|---|---|
| frames/wait/motion01.png | `fb4c72bd02e24790b948edfd2e78696d` |
| frames/wait/motion02.png | `5c32a751b5864e4f802b1cbfe2f6980d` |
| frames/wait/motion03.png | `bf6a1a79ae3e47419571fb82b46a26fa` |
| frames/raging-blow/motion01.png | `a4b2f29361fd49dda2104ce70a4b4f82` |
| frames/raging-blow/motion02.png | `e81fe579b29846c4a93f4a5e3decd341` |
| frames/raging-blow/motion03.png | `2ab55adc7e964164a2675fe41720dd35` |
| frames/raging-blow/motion04.png | `f952fd92a3b140f1a896e60ea777278f` |
| frames/raging-blow/motion05.png | `a94516dd5ddb4c12b55d7877ce927eca` |
| frames/raging-blow/motion06.png | `a63a0e835c3e46dfb862a1727e898d56` |
| frames/raging-blow/motion07.png | `b8f0b7d9b63d4738ba1c40bf7f7d6ed3` |
| frames/raging-blow/motion08.png | `4ff13f32715d4446b32cc3cd81ac01ad` |
| frames/enraged-raging-blow/motion01.png | `921342b83ead49499ebcb1305c051f79` |
| frames/enraged-raging-blow/motion02.png | `2252822c3c544150b2b11d2c689df015` |
| frames/enraged-raging-blow/motion03.png | `0e8533552bca4a7dbdeca19be5b65e23` |
| frames/enraged-raging-blow/motion04.png | `bd5b06cb3c6e4dcf8708ceae77c33ff5` |
| frames/enraged-raging-blow/motion05.png | `fd0f61326882439783495af1c34284b6` |
| frames/enraged-raging-blow/motion06.png | `b60553dd8f9f48fc8a449df949625cbe` |
| frames/enraged-raging-blow/motion07.png | `6fd0859ce3d44c37a80d2c3c8c21dc1c` |
| portrait.png | `01d1da2e721b4dd893e314ef3d64e2e1` |

`RtsJobTableLogic.HasMageSkin/GetMageSkinFrames/GetMageSkinFrameDurations/GetMagePortraitRUID`가 연결 기준이다. `RtsUnitComponent`는 대기 반복과 공격 시간표를 재생하고 좌우 방향을 맞춘다. `RtsSkillFxLogic.PlayCast/ReturnStand/CheckLoops`가 단발·반복 공격과 복귀를 제어한다.

## 제작·확인

내장 imagegen으로 승인된 앞뒤 자세 사이 연결 프레임을 그렸다. Sharp로 전체 등비 축소·투명 캔버스·발 위치만 정렬하고 얼굴 크기·의상·색과 연속 자세를 나란히 대조했다. 파일 크기·알파·해시·프레임 순서와 시간표를 검사했다. 게임 검증 결과는 공통 적용 기록에 별도 기록한다.

## 공격 프레임 검 제거

내장 imagegen precise-object-edit로 인레이지7장과 일반기08의 개인 검을 제거했다. 프롬프트: 검날·가드·손잡이만 제거하고 양손 위치, 자세, 얼굴, 비율, 의상, 망토, 색감과 투명 캔버스를 유지한다. 남은 손잡이는 같은 조건으로 한 번 더 정리한다. Sharp는 704×704 크기와 기존 발 기준 정렬에만 사용한다. 대기3장은 검을 유지한다. 새 RUID8개로 교체한다.

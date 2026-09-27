# 히어로 외형·모션 적용

승인 원화 기반 PNG를 기본 MSW 아바타 대신 사용한다. 새 프레임과 흉상을 리소스로 등록하고 게임 표에 연결했다. Maker 재생 검증 상태는 [공통 적용 기록](unit-motion.md)을 따른다.

## 외형·표정

갈색의 짧고 풍성한 머리, 푸른 눈, 은색 귀걸이, 검정·은색 갑옷과 금색 문양, 붉은 가슴 보석과 망토, 은색 양손검·금색/붉은 보석 손잡이. 대기는 자신감 있는 옅은 미소, 공격은 입을 다문 집중한 표정.

현재 18장은 확정 콘셉트의 얼굴·갑옷·색과 비숍 기준 약2.3등신으로 다시 맞춘 결과다. 대기01은 승인 콘셉트를 정렬하고 대기02·03과 공격15장은 실제 재작화했다. 이전 전체 축소만 한 모션을 교체했다. 새 RUID18개를 아래 표에 연결했다. Maker 검증 결과는 문서 끝에 기록한다.

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
| frames/wait/motion01.png | `6142e6907e054a4c86bda1719698af21` |
| frames/wait/motion02.png | `66beab16ed794e27b49a33ee52a82b18` |
| frames/wait/motion03.png | `f5ce5824f3a24e069ec0a523028c7f79` |
| frames/raging-blow/motion01.png | `aac52a1acd1f414d9aa9f68167aeb2d0` |
| frames/raging-blow/motion02.png | `a302b38cd51543059e46a3162b209b02` |
| frames/raging-blow/motion03.png | `1b789ed0b21f404297592ca1bd0666af` |
| frames/raging-blow/motion04.png | `29beedf569f7412483c02c99e0e5fe2e` |
| frames/raging-blow/motion05.png | `cdd8a42144c949979ef9a7d1b0fa9e51` |
| frames/raging-blow/motion06.png | `be37495f3da24fa1ba32404daeb1c998` |
| frames/raging-blow/motion07.png | `bfe48ef4838c4d16a3f86ee914cf9440` |
| frames/raging-blow/motion08.png | `b9daa2a09e874aeea2a82b15cfb328ca` |
| frames/enraged-raging-blow/motion01.png | `b64a6805781448eb875ea1d4629f3bc5` |
| frames/enraged-raging-blow/motion02.png | `77faeca61b3e4bec80ec0a66faee52e6` |
| frames/enraged-raging-blow/motion03.png | `29bc48d64e1f4f78bb56cc0948dda058` |
| frames/enraged-raging-blow/motion04.png | `f8199840321d4eed9bfd3395afcc8a77` |
| frames/enraged-raging-blow/motion05.png | `591f6cf9adb34a099a3f435b2e40dbc4` |
| frames/enraged-raging-blow/motion06.png | `8ce4f50c18a04c93b060320e30f68858` |
| frames/enraged-raging-blow/motion07.png | `a992dea232544bdd972d0978a94b25fd` |
| portrait.png | `01d1da2e721b4dd893e314ef3d64e2e1` |

`RtsJobTableLogic.HasMageSkin/GetMageSkinFrames/GetMageSkinFrameDurations/GetMagePortraitRUID`가 연결 기준이다. `RtsUnitComponent`는 대기 반복과 공격 시간표를 재생하고 좌우 방향을 맞춘다. `RtsSkillFxLogic.PlayCast/ReturnStand/CheckLoops`가 단발·반복 공격과 복귀를 제어한다.

## 제작·확인

내장 imagegen으로 승인된 앞뒤 자세 사이 연결 프레임을 그렸다. Sharp로 전체 등비 축소·투명 캔버스·발 위치만 정렬하고 얼굴 크기·의상·색과 연속 자세를 나란히 대조했다. 파일 크기·알파·해시·프레임 순서와 시간표를 검사했다. 게임 검증 결과는 공통 적용 기록에 별도 기록한다.

## 공격 프레임 검 제거

내장 imagegen precise-object-edit로 인레이지7장과 일반기08의 개인 검을 제거했다. 프롬프트: 검날·가드·손잡이만 제거하고 양손 위치, 자세, 얼굴, 비율, 의상, 망토, 색감과 투명 캔버스를 유지한다. 남은 손잡이는 같은 조건으로 한 번 더 정리한다. Sharp는 704×704 크기와 기존 발 기준 정렬에만 사용한다. 대기3장은 검을 유지한다. 새 RUID8개로 교체한다.

## 비숍 기준 모션 재작화

내장 imagegen으로 기존 자세를 편집하고 승인 hero/concept.png와 실제 bishop/frames/wait/motion01.png 및 angel-ray/motion03.png를 참조했다. 대기01을 비숍과 먼저 비교하고 전체 프레임을 제작했다. 머리 길이 약147px로 등비 정렬했으며 Sharp는 신체 변형 없이 캔버스·배율·발 정렬과 검수에만 사용했다. 대기03의 길어진 몸체 시안은 제외하고 승인 콘셉트를 직접 편집한 결과로 교체했다.

대기3장에는 어깨에 걸친 검을 유지하며 공격15장에는 개인 검·중복 효과가 없다. 레이징 블로우의 손 기준점은 최종704px 프레임에서 (391,520), (423,506), (372,496), (365,538), (338,539), (244,515), (243,520)으로 다시 측정했다. 이전338/394 중복 보정은 제거했다. 이펙트 월드 배율2.0, 프레임 순서·시간·판정·피해·쿨타임은 유지한다.

참조 SHA256·원본 백업: `.beaver/output/hero-bishop-motion/manifest.json` 및 `originals/`. 생성 프롬프트: `generated-*.json`. 좌표: `landmarks.json`·`normalized.json`. 새 리소스: `resource-manifest.json`. [몸체 모션 미리보기](../../.beaver/output/hero-bishop-motion/preview.html).

## 최종 확인·확정

Maker 새로고침·저장·실행 후 새 리소스18/18 로딩, 연결/시간표 오류0, 빌드/실행 오류0을 확인했다. 임시 히어로의 본체 로딩 완료와 일반 검 스프라이트14장을 확인했다. 인레이지는 실제 PlayCast 경로로 불꽃 클립71d8513c51fc48c49609837f3d15160b와 함께 재생했으며 왼쪽7/7·오른쪽7/7 프레임 관측, 개인 검 중복 표시0, 불꽃 표시를 확인했다. 최초 짧은 검수 이후 현재 카메라 중앙 아래에서 반복 재생해 사용자에게 보여 주었다. 사용자가 “좋아 이거로 확정할게”로 최종 승인했다. 자동 검증은 인레이지 프레임·방향·효과 표시 범위이며 일반기의 모든 프레임을 새로 관측한 것은 아니다. 검증용 유닛과 효과는 정리했다. 기록: `.beaver/output/hero-bishop-motion/runtime-verification.json`.

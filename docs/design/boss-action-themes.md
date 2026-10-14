# 보스 액션 테마

- 갱신: 2026-10-14. 기존16종을 다시 그리고 시그너스를 보강하여 액션17종+일반5종=총22종. 자쿰 저장 키는 유지한다.
- 승인 일체형 원본/썸네일/RUID: `assets/design/themes/illustrated-boss-scenes/`의 각 폴더 및 `action-scenes.json`. 전체 검수판은 `index.html`.

- 현재 런타임 전체17종 목록은 `assets/design/themes/articulated-scenes/action-scenes.json`. 전체17종이 해당 폴더의 분리 배경·보스 부위·환경 효과를 사용한다.

## 제작 기준

기존 `assets/design/themes/action/zakum-altar/keyframe.png`의 깔끔한 윤곽·둥근 형태·부드러운 음영을 공통 그림체로 사용했다. 기존 승인 장면을 참조하여 배경과 보스를 모두 새로 그렸으며 MSW 저해상도 보스를 확대하여 겹치지 않는다. 사용자 사진은 장소와 정체성 참고이며 픽셀 그대로의 추출본이 아니다. 시그너스는 MSW 초상 참고와 정원 재구성이다.

- 주니어발록·혼테일·피아누스는 중간 발판·로프 없이 정돈한다. 피아누스는 중앙 한 마리.
- 핑크빈은 석상5개를 유지한다. 검은마법사1페이즈는 두 보스, 나머지는 단계별 별도 장면이다.
- 스우는 사진의 코어 속 형상, 더스크는 사진의 거대한 본체를 기준으로 한다.
- 전체 배경 확대·축소·이동·밝기 변화는 제거했다. 자쿰은 고정 배경+팔8개 관절 모션+용암 기포/파열/파문, 혼테일은 고정 배경+머리3개·팔2개·날개2개·꼬리 모션+낙수/물보라를 사용한다. 추가15종에도 머리·팔·날개·꼬리·옷자락·부유·구체 순환 등 보스별 모션을 적용했다.
- 화면 중앙에 배경을 맞추고 원본 크기를 보정한다. 월드·카드는 같은 원화를 사용한다.

## 전투 연결

보스전에는 해당 보스 액션 테마로 자동 전환하고 종료·탈락·재시작 시 개인 선택 테마를 복원한다. 개인 저장 키는 유지하며, 기존 액션 선택값은 헤네시스로 이관한다. 트랙/칸 전체는 모든 액션 테마에서 항상 숨기고 이동·영입 중에만 기존 설치 마커를 표시한다. 중앙 2×2 예약칸과 전투 보스 엔티티·HP·피격·처치·클리어는 유지하며, 몸통과 추가 부위의 SpriteRenderer만 숨긴다. 중앙4칸 클릭은 살아 있는 보스 정보로 연결한다(두 보스는 가까운 슬롯 우선).

테마 표시 상태는 `RtsThemeLogic.BossThemeByZone`, 전투 진입/정리는 `RtsBossLogic`, 본체 숨김은 `RtsMonsterComponent`, 트랙 숨김은 `RtsBoardViewLogic`, 클릭은 `RtsMonsterInfoLogic`가 담당한다. 관전 구역과 열린 카드에 같은 부위 모션·환경 효과를 적용하며 교체·파괴·종료 시 정리한다.

## 원화 목록

| 테마 | 파일 |
|---|---|
| 자쿰의 제단 | `assets/design/themes/illustrated-boss-scenes/zakum-altar/concept.png` |
| 금지된 제단 | `assets/design/themes/illustrated-boss-scenes/forbidden-altar/concept.png` |
| 피아누스의 동굴 | `assets/design/themes/illustrated-boss-scenes/pianus-cave/concept.png` |
| 생명의 동굴 | `assets/design/themes/illustrated-boss-scenes/cave-of-life/concept.png` |
| 신들의 황혼 | `assets/design/themes/illustrated-boss-scenes/twilight-of-gods/concept.png` |
| 시그너스의 정원 | `assets/design/themes/illustrated-boss-scenes/cygnus-garden/concept.png` |
| 블랙헤븐 코어 | `assets/design/themes/illustrated-boss-scenes/black-heaven-core/concept.png` |
| 세계수 정상 | `assets/design/themes/illustrated-boss-scenes/world-tree-summit/concept.png` |
| 무너지는 시계탑 | `assets/design/themes/illustrated-boss-scenes/collapsing-clocktower/concept.png` |
| 바스러지는 빛 | `assets/design/themes/articulated-scenes/crumbling-light/grounded/preview.png` |
| 공허의 눈 | `assets/design/themes/illustrated-boss-scenes/eye-of-void/concept.png` |
| 욕망의 제단 | `assets/design/themes/illustrated-boss-scenes/altar-of-desire/concept.png` |
| 끝에 가까운 곳 | `assets/design/themes/illustrated-boss-scenes/near-the-end/concept.png` |
| 어둠의 신전 | `assets/design/themes/illustrated-boss-scenes/dark-temple/concept.png` |
| 어둠의 왕좌 | `assets/design/themes/illustrated-boss-scenes/dark-throne/concept.png` |
| 시작과 끝의 경계 | `assets/design/themes/illustrated-boss-scenes/boundary-of-beginning-and-end/concept.png` |
| 존재하지 않는 공간 | `assets/design/themes/illustrated-boss-scenes/nonexistent-space/concept.png` |

## 검증

Maker 빌드 오류 0건, 이번 검증 런타임 오류 0건. 전체17종의 월드·카드 모션 검증 이후 데미안 테두리 모션을 재검증했다. 현재 전체183개 부위이며, 데미안36개 부위(고정 날개2개·본체·스카프·테두리 불꽃32개)의 월드·카드 생성과 움직임을 확인했다. 배경·부위 합계122개 고유 리소스가 전부 로딩되었고 크기·중앙 피벗·PPU 검증 오류는0건이다. 17종 모두 배경 위치·크기 고정, 카드 연속 교체, 임시 장식 정리까지 통과했다. 자쿰 용암24개·혼테일 낙수16개는 앞선 검증에서 확인했다. 세밀한 조립 자연스러움은 사용자 검수 대상이다.

보스전 트랙 숨김·본체 렌더러 숨김·중앙4칸 클릭 정보창은 앞선 버전에서 확인했으며, 실제 피격·처치는 아직 미확인이다. 현재 부위 모션 증거: `assets/design/themes/articulated-scenes/action-verification.json`. 이전 illustrated-boss-scenes/action-verification.json의 화면 확대 검증은 폐기된 연출 기록이며 현재 모션 검증으로 간주하지 않는다.


## 전체17종 모션 적용 (2026-10-14)

사용자 승인 후 신규105개 리소스를 등록하고, 기존26개와 합쳐131개를 연결했다. 핑크빈 연결부 보정과 진 힐라 머리카락 보정을 포함한다. 액션17종 전체가 고정 배경+분리 보스 부위 모션을 사용한다. Maker 런타임 검증 결과는 action-verification.json을 따른다.

- 검수: `assets/design/themes/articulated-scenes/preview.html`
- 보스별 모션: `assets/design/themes/articulated-scenes/motion-plan.md`
- 등록 상태: `assets/design/themes/articulated-scenes/registration-progress.json`
- 미등록 자산이 있으면 적용을 차단하는 적용 도구: `build-runtime.cjs`


### 2026-10-14 사용자 검수 보정

- 액션17종은 보스 라운드 여부·탈락 상태와 관계없이 트랙과 격자를 숨긴다. 기본5종 복귀 시 트랙을 복원하며, 이동·영입 설치 마커는 별도로 유지한다.
- 발록: 날개를 어깨 뒤로 올리고 팔 크기·연결 위치를 조정했다. 핑크빈: 몸 높이·작은 팔·꼬리 위치를 원화 비율에 맞췄다.
- 진 힐라: 진홍색 머리·검은 의상·회색 피부·연두색 마법을 보존한 body-palette-clean.png를 사용한다. 낫의 손잡이 (245,290)를 몸 이미지의 쥔 손 (205,535)에 고정하고 같은 부유 주기를 공유한다. 낫은 손 뒤 레이어에서 손을 중심으로만 ±3도 움직인다. 기존 body-fixed.png와 별도 머리/치맛자락은 현재 런타임에서 사용하지 않는다.
- 데미안의 이전14개 상승 불꽃과 전체 날개6프레임은 아래 2026-10-15 테두리 전용32개 불꽃으로 교체했다.
- 현재 자산 경로·RUID는 motion-resources.json, 배치·모션은 new-rig-layout.json과 runtime-rigs.json이 기준이다.


### 2026-10-15 발록·데미안·윌·더스크 후속 검수

- 발록 팔은 몸통·허벅지보다 앞(팔95/몸94)에 표시하고 머리는96으로 둔다. 어깨 고정점과 작은 팔 회전은 유지하여 손만 뒤에서 튀어나오는 가림을 없앤다.
- 이전 인간형 윌 검수 이력(거미형 교체로 미사용): 양팔 배율은0.60→0.38(약37% 축소), 왼팔 회전±6도·오른팔±4도. 책은 축소된 왼손 근처(x710)에 둔다.
- 더스크 네 갑각의 기준점을 중앙(x827~842,y240~250)에 모으고 배율·각도를 원화 구도로 복원했다. 회전폭은1.4~1.7도로 제한하여 원형 본체가 크게 드러나는 벌어짐을 줄였다.
- 데미안: 원래 wing-l.png·wing-r.png를 배율0.8로 사용하여 날개 형태·내부·회전·크기를 고정한다. 날개는 좌+24도·우-24도로 낮고 넓게 펼치며 회전값은 고정한다. 날개 명도20%, 본체28%, 스카프24%로 어둡게 한다. 날개 테두리에만 좌우16개씩 총32개 불꽃을 배치하고, 0.42~0.62초 주기로 몸통(840,550)에서 바깥쪽으로58px 흩어졌다 사라지게 한다(배율0.22~0.27, 최대 알파1, 명도68%). 불꽃 그림 방향도 외향 벡터에 맞춘다. 테두리가 강하게 타들어가는 느낌을 위해 약했던16개 불꽃의 크기·밀도·외향 이동폭을 늘렸다. 본체와 함께하는 소폭 부유·스카프 모션은 유지한다.
- 2026-10-15 테두리만 움직이도록 재보정: 전체 날개6프레임 방식은 사용 중단했다. flame-wing-atlas.png·wing-l-flame-1~3.png·wing-r-flame-1~3.png는 과거 제작 이력으로만 보존한다. 현재 날개/불꽃은 world-tree-summit/wing-l.png·wing-r.png·flame-l.png·flame-r.png이며 최신 RUID/좌표는 motion-resources.json/runtime-rigs.json을 따른다.


### 2026-10-15 윌 거미형 교체 — 현재 적용

- 윌 보스맵과 액션 테마 이름: **바스러지는 빛**. 저장된 선택값 호환을 위해 내부 키 `diffraction_hall`은 유지한다.
- 보라색 균열 공간·어두운 구체·푸른 석재 바닥·붉은 거미줄 배경. 중앙의 검은 거미형 윌은 몸통, 독립 관절 다리 8개, 붉은 눈 문양의 총 10부위로 구성한다. 배경은 고정하고 몸통 부유·다리 관절·문양 발광만 움직인다. 월드와 카드 모두 같은 모션을 사용한다.
- 원화·부위·프롬프트·리소스: `assets/design/themes/articulated-scenes/crumbling-light/`. 인간형 `diffraction-hall/` 자산은 이전 검수 이력이며 현재 미사용이다.
- 110번 윌 보스 스테이지 BGM: `bd23d2f87d734f8ca52ca8824d1b6ff4` (`sound-434`). 일반 에스페라 스테이지 BGM과 전투 판정은 유지한다.
- 액션 테마 트랙 숨김과 중앙 기존 4칸 보스 정보/공격/클리어 판정은 기존 경로를 유지한다.

현재 윌 교체 뒤 전체 17종은 187개 부위·142개 등록 항목이며, 배경/부위에서 사용하는 고유 리소스는126개다. 위 183개/122개 및 인간형 윌 검증 수치는 교체 전 이력이다.

검증: Maker 빌드 오류0건·이번 Play 런타임 오류0건. 새 리소스12/12 로딩·크기/피벗/PPU 검증 통과. 월드/카드 각각10부위 생성·10부위 변화 및 다리8개 관절 움직임, 배경 고정, 임시 카드 정리 통과. 110번 윌 BGM 지정 주소 재생 확인. 스테이지 생성기 검산(132스테이지/247몬스터/17보스) 통과; 생성 표 변경은110번 이름/BGM 두 필드뿐이다.


### 윌 다리 접지 수정 — 현재 적용

- 기존 칼날처럼 겹친 다리를 굽은 상부 관절+아래로 뻗는 다리 형태 8개로 교체했다. 새 자산은 `assets/design/themes/articulated-scenes/crumbling-light/grounded/`이다.
- 발끝은 배경 바닥의 고정 좌표를 짚고, 몸통과 다리의 몸 쪽 접점이 같은 2.4초 주기로 ±18픽셀 들썩인다. 다리 각도/길이는 두 접점에 맞추므로 발끝이 미끄러지거나 공중을 휘젓지 않는다. 몸통 중심은 기존보다100픽셀 아래(y500)로 낮췄다.
- 월드/카드 공통 `GetGroundedPose` 사용. 배경·눈 문양·지정 BGM·전투 판정은 유지. 위의 초기 거미형 부유/자유 다리 회전 기록은 교체 전 이력이다.


### 2026-10-15 액션 테마 보스전 전용 전환 — 현재 정책

- 개인 선택 목록은 헤네시스·엘리니아·페리온·커닝시티·리스항구 5종만 제공한다. 액션 탭과 액션 테마 선택지는 제거했고 서버 변경 요청도 거부한다. 액션 17종은 보스전 자동 연출로만 사용한다.
- 기존 액션 테마 선택 사용자는 다음 접속/프로필 로드 때 헤네시스로 변경·저장한다. 저장소 읽기 실패 시 기존 값을 덮어쓰지 않으며 일반 테마 선택은 유지한다.
- 보스 진입 시 구역별 보스 테마를 임시 적용한다. 그 구역의 마지막 보스 처치 직후 개인 테마를 복원한다(검은 마법사 1페이즈는 두 보스 모두 처치 후). 탈락·종료·재시작에도 복원한다. 다른 구역이 전투 중이어도 클리어한 구역은 즉시 복원한다.
- 보스전 중 개인 일반 테마를 변경하면 임시 보스 배경을 유지하고, 종료 후 새 선택으로 돌아간다. 트랙 숨김도 구역별 보스 상태를 따르며 복귀 시 함께 복원한다.
- 개인 저장 theme 키와 보스 내부 테마 키는 유지한다. 보스 17종 자산·모션·BGM·중앙 4칸 전투/정보 판정은 유지한다.

검증(2026-10-15): Maker에서 개인 카드5개·종류 기본1개 확인, 액션17종 선택 검증 거부, 보스17종 전환/복귀, 보스전 도중 일반 테마 변경 후 복귀, 2체 보스 완료 콜백, 탈락 ClearZone 복귀 경로 통과. 클라이언트 윌 배경/트랙 숨김과 헤네시스/트랙 복귀 확인. 저장 이관은 실제 계정 설정을 바꾸지 않는 모의 저장소로 같은 프로덕션 함수의17종 이관·일반5종 유지·읽기 실패 저장 방지까지 통과했다. 빌드/실행 오류0건.


### 2026-10-15 발록 팔 재작화 — 현재 적용

- 기존 둥근 근육 덩어리·뒤틀린 손목·정면으로 벌린 큰 손바닥을 폐기하고, 어깨에서 손목으로 이어지는 긴 팔과 아래로 향한 작은 발톱으로 재작화했다. 몸통·머리·날개·배경 원화는 유지한다.
- 자산: `assets/design/themes/articulated-scenes/forbidden-altar/arms-v2/`. built-in image_gen 생성 후400×600으로 축소·좌우 반전하고 생성 알파를 유지했다. 프롬프트는 generation-prompt.json.
- 양팔 표시 배율0.48, 어깨 접점 좌(720,455)/우(965,455), 기본 각도±10도, 회전폭±3도, 주기3.6초. 어깨가 몸통에 가려 자연스럽게 연결되도록 팔93/몸94/머리96 순서로 표시하며 손은 허벅지 바깥쪽으로 뺀다. 기존 팔95 설정은 교체 전 기록이다.
- 좌팔 RUID `36045f82765b4042879cda0e7498909e`, 우팔 `1e3d4f3be36f4fba85988d6e40a65b6b`. 액션 테마 보스전 전용 정책과 전투 판정은 유지한다.

발록 팔 Maker 확인(2026-10-15): 신규2장 로딩·400×600/피벗/PPU 통과. 실제 월드 양팔2/2 움직임, 어깨 고정 오차0.000005px 미만, 회전폭±3도·트랙 숨김 확인. 빌드/런타임 오류0건.

# assets

사용자가 확정한 자산 RUID와 자산 규칙. 원본 목록은 `.info/monster.md`, `.info/character.md`(gitignore된 사용자 로컬 노트) — 여기엔 규칙과 기준값만.

## 몬스터 1종 = 이동 클립 · 사망 클립 · 사망 효과음 3개
- Rule: 몬스터마다 ① 이동 애니메이션 클립 ② 사망 애니메이션 클립 ③ 사망 효과음 3개가 기본. 피격음은 몬스터가 아니라 **스킬별 타격음**으로 낸다. 초록달팽이(몹 0100100) 기준값: 이동 `e7d919d7b4724c65b2f53164c2873ae0`, 사망 `a25ed762135448ccb2307604f3179565`, 사망음 `30e5a789e9204111924cafc1bc1ce33f`(`sound/mob/0100100/die`). 몬스터 ID는 `.info/monster.md`의 M001~/B01~(첫 등장 순, 검은마법사 2/3/4페이즈는 B16/B17/B18 별개).
- Scope: project
- Rationale: User decision 2026-09-14 — "몬스터는 각각 초록달팽이처럼 이동 애니메이션, 사망 애니메이션, 사망 효과음 3개를 기본으로"
- CLAUDE.md application: not needed(non-code — 데이터 규칙)
- Priority: takes precedence over defaults

## 이동 속도 수치 100 = 초당 3.5유닛
- Rule: `RtsConfigLogic.SpeedUnitPerSec = 3.5`, 속도 수치는 100 기준(달팽이 시연 속도). 칸 1개 ≈ 0.5초, 트랙 한 바퀴(117.3유닛) ≈ 33.5초. 몬스터 능력치의 이동속도는 이 수치.
- Scope: project
- Rationale: User decision 2026-09-14 — "이동속도도 수치화 시켜서 간편하게 관리. 저 속도를 100으로"
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 히어로 외형 = 공식 "모험가 히어로" 세트
- Rule: 아머(롱코트) `c92ab70d7a064aafaa34298c2e9890e3`, 두손검 `c4f9b9c993754161816092e680584ce3`(1H판 `5c17efb794334d4980987edaace1f546`), 부츠 `186a55d192d24b4da5201801422bebf7`, 헤어 `931c0ed47c3e4df69734fe19247a7b33`(검정 남 — 여 `36456c66…`, 빨강 `62c7e6c8…` 등 색상 변형 있음). 모자 없음, 얼굴 기본. 다른 직업도 "모험가 ○○" 세트가 있음(팔라딘 확인: 아머·부츠·무기 1H/2H) — 같은 방식으로 채운다. 예쁜 외형은 나중에 과금 코디로.
- Scope: project
- Rationale: User decision 2026-09-14 — "오 딱 좋아 내가 원한게 딱 저정도임. 캐릭터 이쁜거는 과금으로 나중에"
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 히어로 브랜디쉬(1레벨 스킬) 자산
- Rule: 모션 `swingTF`(4프레임 0.65초), 이펙트 `5c2c13c481ba476294bff7e9e04df837`(`skill/11101008/effect/1`, 9프레임 0.95초, 캐릭터 발 위치에 스케일 2.0·OrderInLayer 210), 사운드 `f0c0c4016cf04d0d98886227cab56561`(`sound/skill/1101011/use`, t=0에 한 번). 무기 잔상 켬. 레이징 블로우 자산(`1c268072…` 2타 이펙트, `424dcf18…`/`d621d7a5…` 타격음)은 폐기.
- Scope: project
- Rationale: User decision 2026-09-14 — 레이징 블로우 → 브랜디쉬로 변경, "이게 낫다"
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 히어로 발할라(50레벨) 표시 = 등 뒤에 떠 있는 불타는 검
- Rule: `9180909395934b4ab2dfb47f87864813`(`skill/400011001/summon/stand`, 5차 소드 오브 버닝 소울 소환검 대기 루프)을 캐릭터 오른쪽 +0.25유닛, 스케일 1.2, OrderInLayer 199(캐릭터 200보다 뒤)로 상시 표시. 4차 발할라 1121054에는 시전 이펙트(`8153d9f3…`, `7c3028f7…`)만 있어서 안 씀. 획득 연출용 `cb8d8eb3…`(001/summoned), 보스 타격 연출용 `c5695696…`(002/attack1).
- Scope: project
- Rationale: User decision 2026-09-14 — "등 뒤에 칼이 한자루 계속 있으면 좋겠거든" → "9180909…이거하면되겠다", 크기·위치는 비교 후 "중간게 젤 낫네"
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 팔라딘 외형·스킬 자산 (모험가 팔라딘 세트)
- Rule: 아머 `3db1f00384854ab6aa9e6148efa942d9`, 두손둔기(해머) `ba9a04c1dc1f42049f0ec88e95052c76`(1H판 `60add7c2…`), 부츠 `790ae27c0b30414eb369bda472df4799`, 헤어 `9188a9716ae947b5a1e518bd0d1c0252`(검은색 팔라딘 헤어, 은회색 톤 — 65010~65017 색상 변형). 디바인 차지: 모션 swingTF, 이펙트 `cb9cff6c57fd4cb18a05db3d47277031`(`1221004/effect/1`, 9프레임 0.65초), 시전음 `e2989dcac9054d689e379b9feff55f54`. 생츄어리(원작 1221011): 모션 swingT1(도끼 내려찍기), 시전 이펙트 `d577178a8212489e8319a4c5b16e897b`(24프레임 0.9초, **첫 재생 로딩 0.6초 → 미리 로드**), 타격 이펙트 `5df303c326dd488cbeb17028892b5238`, 시전음 `aa96c1117c634a23b56440be8de39037`, 타격음 `2cc05078af454fa3a7856b9fb65ed61f`.
- Scope: project
- Rationale: User decisions 2026-09-15 — 외형 "입혀줘", 디바인 차지 "괜찮아", 생츄어리 "애니메이션 ㅇㅋ, 사운드 나쁘지 않아", 모션은 4종 비교 후 "맨왼쪽(swingT1)"
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 다크나이트 외형·스킬 자산 + 유닛 UI 자산
- Rule: 다크나이트 세트 — 아머 `a529865cf7be417c97b7855eed344004`, 창(2H) `acd581b759f2425282961a4486550006`, 부츠 `f6f89e92db4f498e9b5fb6ec7ee81dda`, 헤어 `e8d9dda3dfd34b68b62426838e951723`. 다크 임페일: stabT1 + 이펙트 `ed38cd53290046eb86ad9244632e950a`(0.7초) + use `f9c8dd4041b943728b8556bc1302797e`, hit `6313ad64a5854e20ab6e0e369e1c2c56` ×3(0.15초 간격). 버서크 오오라 `1b0130f2c28843539045e522d36b5a25`(등 뒤 199 루프). 드래곤 로어(옛 용기사 9001006): swingT3 + `5468cadd2f60428e925bc368968e1a1e`(1.2초, 미리 로드) + 타격 `01c803531e2c4e5aa3c3ef66f14711b8` + 사운드 `eec2f5d35c6f4f6ebe8f19bb52dbf1d1`. 유닛 UI: 발판 강조 틀 `2c03a06fb9ee495e80e3935eb033bccf`(RtsPadFrame, 80px 흰 틀, PPU 100 → 스케일 2.222 = 한 칸, 틴트로 색), 손 커서 `3930c5d2e85b4bff8467aada64fda7f5`(maplestory ui/basic/cursor/0). 파티 버프 아이콘(원작 32px 스킬 아이콘, `skill/<직업>/skill/<id>/icon` — 같은 폴더의 icondisabled·iconmouseover와 헷갈리지 말 것): 결속 = 메이플 용사 `e4b1179780154997a33a1ea985acefd0`(1221000), 샤프아이즈 `4cd1961bc55b47cb80e1a7f8843e225e`(3121002), 프레이 = 홀리 심볼 `39b3159efcc74334b875c94c64a74243`(2311003), 조커 `f1575f7842c740a49f9e19c2514de64e`(24121003) — 카메라가 멀어서 월드에선 스케일 2.2(0.7유닛)는 돼야 읽힌다. 세 직업 세트는 `RtsJobTableLogic.GetCostume`이 단일 소스.
- Scope: project
- Rationale: User decisions 2026-09-15 — 다크나이트 시연 확정("지금 사운드 좋아", 드래곤 로어 sprite 9001006 "굿"), 발판 틀·손 커서는 캐릭터 선택 요청에서 제작
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 테마 프리셋과 헤네시스 자산
- Rule: 트랙/타일/장식은 `RtsThemeLogic` 프리셋(`henesys`, `elnath`)으로 관리 — floorTile + floorVariants(비율) + gridRUID + decor 목록. 헤네시스 바닥 = 공식 RectTile(`HenesysGrass1/2/3`, 타일셋 `CaveFloorTileSet`, 바닥 타일 4유닛), 장식 = 공식 탑뷰 헤네시스 오브젝트 34개를 **트랙 바깥에만** 불투명으로. 새 테마는 게임 프리셋과 화면 목업(`hud-layout.html`) 양쪽에 같이 추가. 절차·RUID 표는 `assets/textures/README.md`.
- Scope: project
- Rationale: User decision 2026-09-14 — "트랙/타일은 프리셋 가능하도록", "사물은 트랙 바깥에 배치해줘… 투명도도 낮출 필요 없을 것 같아"
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

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

## 히어로 1레벨 스킬 = 레이징 블로우 자산
- Rule: **현재 히어로 1레벨 액티브는 '레이징 블로우'** — 클립 `fa2bfe8ff4f543fb815dd7ee5e02eac9`(1121008/effect/2, 14fr 0.78s: 등 뒤 잔상 → 큰 초승달 → 수평 참격), 사운드 `d621d7a5…`(1121008/hit)를 시전음으로 0.24s 지연 1회(hitSound 없음), 타격 클립 `7d4fd3b7…`(1121008/hit/0) 유지, 모션 swingO3 하나를 motionRate 0.58로 늘려 0.78s(클립 길이), 클립과 동시 시작, hideWeapon(캐릭터 검·잔상 숨김, 이펙트의 금색 대검이 검 역할), 판정 0.4/0.65s, 사운드 0.24s — 2026-09-19 사용자 "지금 딱 좋아" 확정. 몸 덧그림(bodyClip 115713a9…)은 맨몸 실루엣이 겹쳐 보여 제거. 프리즘 증강용 강화판 = **1120017**(인레이지 레이징 블로우: effect/0~3 13fr 0.78s 불꽃 참격, hit/0~4, 시전음 없음·타격음 `aa92fddf…` 0.47s만).
- Scope: project
- Rationale: User decision 2026-09-18 — "애니메이션 fa2bfe8f… 사운드 d621d7a5… 스킬명 레이징 블로우". 2026-09-19 사용자: 이전 스킬 이름은 문서·코드 어디에도 남기지 않는다("없었던 것으로").
- Priority: takes precedence over defaults

## 다크나이트 스피어 버스터 = skill/80003291 세트 (2026-09-19 확정 "완전 종결")
- Rule: effect `c7051cc2…`(오라 0.9s, clip) + clips `176da561…`(마법진→용머리) · `852883a5…`/`3c2ee6e6…`/`521bf9f6…`(0.6/0.75/0.9s 시차 찌르기 — 세트 클립들이 빈 프레임으로 자기 시작 시각을 가짐 → 전부 시전 순간에 함께 띄움) / hit/0 `84c06a06…`. 세트에 사운드 없음 → 옛 스피어 크러셔 시전음 `fcac442d…`·타격음 `6313ad64…` 유지. 모션 stabT1을 motionDelay 0.5로. 판정 0.65/0.8/0.95. **사용자가 확정한 상태 그대로 둔다**(클립 마지막 프레임이 EndFrame 정리로 짧게 보이는 것 포함). fx 새 옵션: `clips`(추가 클립 목록, 항목별 dx/dy/scale/delay/life), `motionDelay`, `clipHold`.
- Scope: project
- Rationale: User 2026-09-19 "다크나이트의 스피어 버스터가 skill/80003291 이라는 스킬로 있더라고" → 적용 → "다크나이트 스피어 버스터는 이거로 완전 종결". 이전 영상 추출 플립북(assets/textures/crusher)은 폐기(파일 유지).
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
- Rule: 다크나이트 세트 — 아머 `a529865cf7be417c97b7855eed344004`, 창(2H) **`164067c82a8347d681cf49a8be3db5df` 타임리스 알슈피스**(2026-09-18 최종 — 사용자 "다크나이트만 리버스로": 세트 캐시 창 `acd581b7…`의 빨간 두손검 잔상이 스피어 버스터와 겹쳐서. 리버스 창은 라이브러리에 없음 — `*리버스` avataritem = 니플하임·블래스트 니플하임(2H검)·벨로체(2H둔기)·타바르진(2H도끼)·블랙뷰티·부츠 2종뿐 — 자매 세트 타임리스로. 다른 직업 무기는 세트 그대로. 이전 후보 레볼루션 스피어 `44d92464…`), 부츠 `f6f89e92db4f498e9b5fb6ec7ee81dda`, 헤어 `e8d9dda3dfd34b68b62426838e951723`. **스피어 버스터**(구 다크 임페일, 2026-09-16 확정): stabT1 + 옛 스피어 크러셔 플립북 v2 11프레임(`assets/textures/crusher/meta.json` `ruids`, 90ms, 스케일 1.7, 발 오프셋 (−0.11,+0.83)×스케일) + use `fcac442d953049d980da4b8d7bd766d8`, hit `6313ad64a5854e20ab6e0e369e1c2c56` ×3(0.15초 간격). 연출 정의는 `RtsJobTableLogic.GetSkills("dk")[1].fx`가 단일 소스. 이전 이펙트 `ed38cd53…`·use `f9c8dd40…` 폐기. 버서크 오오라 `1b0130f2c28843539045e522d36b5a25`(등 뒤 199 루프). 드래곤 로어(skill/900 = GM 스킬 폴더의 슈퍼 드래곤 로어 9001006 — 옛 용기사 1311006이 아니다): swingT3 + `5468cadd2f60428e925bc368968e1a1e`(1.2초, 미리 로드) + 타격 `01c803531e2c4e5aa3c3ef66f14711b8` + 사운드 `eec2f5d35c6f4f6ebe8f19bb52dbf1d1`. 유닛 UI: 발판 강조 틀 `2c03a06fb9ee495e80e3935eb033bccf`(RtsPadFrame, 80px 흰 틀, PPU 100 → 스케일 2.222 = 한 칸, 틴트로 색), 손 커서 `3930c5d2e85b4bff8467aada64fda7f5`(maplestory ui/basic/cursor/0). 파티 버프 아이콘(원작 32px 스킬 아이콘, `skill/<직업>/skill/<id>/icon` — 같은 폴더의 icondisabled·iconmouseover와 헷갈리지 말 것): 홀리 유니티(구 결속) `53a38855164a4b64accf68785761c283`(5차 400011003 아이콘 — 2026-09-16 이름·아이콘 변경, 이전 메이플 용사 e4b1179780154997a33a1ea985acefd0), 샤프아이즈 `4cd1961bc55b47cb80e1a7f8843e225e`(3121002), 프레이 = 홀리 심볼 `39b3159efcc74334b875c94c64a74243`(2311003), 조커 `f1575f7842c740a49f9e19c2514de64e`(24121003) — 카메라가 멀어서 월드에선 스케일 2.2(0.7유닛)는 돼야 읽힌다. 옛 용기사 3차 스킬(스피어 크러셔/드래곤 버스터 1311001·폴암 크러셔 1311002·드래곤 퓨리 1311003·새크리파이스 1311005 — 사용자가 '스피어 버스터'로 기억하는 파란 마법진 + 용 실루엣 + 용머리 발사 이펙트, 나무위키 영상으로 확인)의 **이펙트(sprite·animationclip)는 라이브러리에 없다** — 남은 건 시전음만: `sound/skill/1311001/use` `fcac442d953049d980da4b8d7bd766d8`, 1311002 `45c12bdc851c4e6490d96f284e458658`, 1311003 `482235d632bf48398fca6a0e73d82946`(2026-09-16 검색, source 필터 없이도 동일. 900 폴더는 GM 스킬 — 9001001은 '速' 글자 헤이스트 이펙트). **대안으로 영상에서 직접 추출**: 나무위키 mp4 → ffmpeg 프레임 → 흰 배경 알파 복원(a = 1 − min(RGB)/255) + 캐릭터 실루엣 구멍 → 11프레임 sprite/skill 업로드(v1 외곽선만 `RtsCrusherFx01..11` → 사용자 "테두리만 있는 느낌" → v2 속 채움 `RtsCrusherFx2_01..11` → 사용자 "더 진하게, 영상과 같은 퀄리티" → v3 `RtsCrusherFx3_01..11`(속 흰빛 α0.85·선 ×1.8) 시도 → 사용자 "너무 어색" → **v2 `RtsCrusherFx2_01..11`로 복귀, 이게 현재 후보**(과하게 채우면 뭉툭한 흰 덩어리가 되어 어색 — 반투명 시안 채움이 한계선). RUID 목록은 `assets/textures/crusher/meta.json`의 `ruids`) → 게임에선 `SpriteRUID`를 90ms마다 바꾸는 **플립북**으로 재생(애니메이션 클립 리소스는 API로 못 만든다). 스케일 1.7, 발 오프셋 (−0.11, +0.83)×스케일, Default/300. 사용자 확인 대기(후보). 빨간 참격 잔상의 정체 = 다크나이트 세트의 창 `acd581b7…`가 **캐시 무기(01703433, afterImage `swordTS`)** 라 두손검 잔상이 붙는 것. `AvatarRenderer.ShowDefaultWeaponEffects=false`는 클라·서버·재스폰 모두 **효과 없음**(잔상은 아이템 메타의 afterImage가 결정). 진짜 스피어 아이템(afterImage `spear`, 예: 레볼루션 스피어 `44d92464ace847f8a959fddf294e8c4d`, 펌프킨 `3c62e287…`, 네크로 `9539a261…`, 우트가르드 `141025dc…`, 메이플 베리트 `61066ad8…`, 벨룸 `33439875…`)로 바꾸면 하얀 찌르기 잔상(원작 용기사와 같음). 아이템 잔상 타입은 `asset_get_account_resource_metadata_bulk`의 `extraInfo.avatarItemInfo.afterImage`로 확인. **보우마스터 활도 2026-09-18 타임리스 엔가우 `9e8fe977ff9540d180f3f08dc420d087`로 교체**(세트 캐시 활 `37ad1f37…`은 발마다 파란 폭발 잔상 — 폭풍의 시 초당 5발과 겹침). 세 직업 세트는 `RtsJobTableLogic.GetCostume`이 단일 소스.
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

## 나머지 8직업 기본 외형 = 공식 "모험가 ○○" 세트 + 진짜 무기 (2026-09-17)
- Rule: `RtsJobTableLogic.GetCostume`이 단일 소스(원문 `.info/character.md` 각 직업 외형). 세트 검색은 `asset_search_resources(cat=avataritem, query="*직업명")` → 메타 `mapleName`으로 확인. 성별 변형은 롱코트 01050xxx = 남 / 01051xxx = 여, 헤어 65xxx = 남 / 67xxx = 여, 부츠 01070xxx 남 / 01071xxx 여. **성별 확정(사용자 2026-09-17): 전사 3·나로·팬텀 = 남, 보마·신궁·썬콜·불독·비숍·섀도어 = 여**(여 변형 + 얼굴 `9edd3b01…` 청아한 얼굴 21259 공통, `face` 슬롯 = CustomFaceEquip). **세트의 캐시 무기(01703xxx, 1H는 afterImage swordOL·2H cashweapon49는 swordTS)는 전부 제외** — 보우마스터 캐시 활은 shoot 모션에 파란 폭발 잔상이 크게 뜸(실측). **무기 = 각 세트의 전용 무기(사용자 최종 2026-09-17 "얘네들 각 직업별 무기 있지 않나" → 세트 무기로, "마법사 지팡이·섀도어 단검은 한손 무기" → 한손 판)**: 히어로 두손검 `c4f9b9c9…` / 팔라딘 해머 `ba9a04c1…` / DK 스피어 `acd581b7…`(캐시, 빨간 참격 — 스피어 버스터와 겹치면 타임리스 알슈피스 `164067c8…`) / 보마 활 두손 판 `37ad1f37…` / 신궁 석궁 두손 판 `2ae7ec23…` / 썬콜 스태프 한손 판 `3dcc26b9…` / 불독 완드 한손 판 `37d1f2f6…` / 비숍 완드 한손 판 `ffa0f813…` / 나로 표창 한손 판 `37cdd4ce…` / 섀도어 단검 한손 판 `bbbede91…` / 팬텀 팬텀 오리지날티 `19c6b905…`. 세트 무기는 캐시라 공격 모션에 swordTS/swordOL 잔상(실측: DK 빨간 참격, 보마 파란 폭발) — 의상 색 일치를 우선. 대안(잔상 정상) 리버스(라이브러리에 니플하임 `5d0abb01…`·벨로체 `6083bc6e…`·블랙뷰티 `676ca51a…`만)/타임리스(알슈피스·엔가우 `9e8fe977…`·엔릴 티어 `9886e145…`·람피온 `11f2459e…`·킬릭 `f92581fa…`·페르소나 `b5150885…`)는 character.md 각 항목에 기록. 메이플 시리즈(메이플 보우 `edde225a…`·크로스보우 `ad3ef3c5…`·스태프 `2425d401…`·파이롭 완드 `a5a04b4e…`·샤이니 완드 `c6f0d801…`·스론즈 `47058878…`·PMD 와그너 `b7a3cb66…`)와 팬텀 오리지날티 `19c6b905…`는 대안으로 기록만. 완드·스태프·단검·케인은 **CustomOneHandedWeaponEquip**(코스튬 표 `weapon1h`), 모자 `cap` → CustomCapEquip, 섀도어 마스크 `faceAcc` → CustomFaceAccessoryEquip(`RtsUnitComponent.ApplyLook`·팝업 미리보기 둘 다). 팬텀은 공식 세트가 없어 미스틱 팬텀 슈트·할로윈 팬텀 부츠·**노란색 괴도 팬텀 헤어 `e0c743ee…` + 괴도 팬텀 얼굴 `92fc1e76…`**(원작 NPC 1540482 금발 남성 — 검은색 팬텀 뱅 헤어는 "여자처럼 보인다"로 폐기, `face` 슬롯 = CustomFaceEquip 추가)·**Vampire Phantom Hat `cf9ef095…`**(팬텀 모자 실루엣, 사용자 "마스코트 모자가 안 보인다" → 페더는 깃털만이라 교체. 흰 원작 모자는 라이브러리에 없음; 대안 가면신사의 모자 `9dd21c98…`·젠틀맨 모자 `45f83e09…`)로 구성. 라인업 확인용 배치 = 발판 (4~6, 3~7) 5줄: 전사/궁수/마법사/도적/팬텀.
- Scope: project
- Rationale: User request 2026-09-17 "유닛의 기본 외형과 스킬들을 마무리하자 → 1. 나머지 직업 외형 먼저"
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 마법사 3직업 스킬 자산 (2026-09-18 시험대 — 썬콜 확정 "2가 딱 좋네, 썬콜은 이거로 끝")
- Rule: 원문은 `.info/character.md` 각 스킬(RUID·경로·크기·시간·플래그), 코드는 `RtsJobTableLogic.GetSkillsRaw("il"/"fp"/"bishop")`. 요약 — **썬콜** 체인 라이트닝 = 2221006 effect fa693d02(시전)·ball/0 fde245ae(빔 체인 조각 50×36)·use/hit 사운드, 타격은 **썬더볼트 2201005 hit/0 33fc60d9**(하늘에서 내리치는 번개, 사용자 "썬콜은 영…"에 교체); 블리자드 = **skill/80003323 세트(사용자 지정 2026-09-18)**: 등 뒤 effect 96b26165(땅에서 솟는 얼음 결정 군집, 3.0초, 원점 바닥 중앙, model 형식) + 대상마다 hit/0 735ad75a(하늘 고리 → 얼음 낙하 → 발에서 산산조각, 착지 1.68초, 원점 착지점) — tile/0~8은 같은 낙하 얼음의 높이·시각 변형(미사용), 세트 사운드는 없음 → 2221007 use/hit 유지. 빙결 표시 = 21001008/mob 21628ca1(빛나는 눈꽃 루프). 순서: 군집 3.0초, 낙하 0.5초 시작 → 착지·판정 2.2초 → 조각 잔해 3.0초 → 군집 끝(사용자 "캐릭터 이펙트 종료 직전 → 타격 → 타격 이펙트 끝 → 캐릭터 이펙트 종료"), 후딜 3.0. 타격 얼음 스케일은 0.7→0.95→1.5→**2.0**으로 키워 확정(작게 보임 — 원작 px 크기에 비해 이 게임 줌에선 2배쯤이 맞음). 거친 후보: 2221007 effect(눈빛 기둥, 등 뒤 → 거절)·effect0(발밑 결정, 작음)·tile/4(낙하 얼음 옛 판), 2221012 effect(결정 감싸기), 아이스 스트라이크 2211002 기둥·hit, 프리징 브레스 2221011, 2221052 회전 구슬, 엘퀴네스 2221005 attack, 썬더 스피어 2211010. 사용자가 Maker 피커에서 직접 고른 RUID는 metadata_bulk로 정체(skill 경로)를 확인하고 `*<스킬ID>`로 세트 전체(effect/hit/tile)를 훑는다. 옛 블리자드 2221003·옛 레이징 블로우처럼 **빅뱅 이전 4차 클립은 라이브러리에 없음(사운드만)**. **불독**(사용자 OK 2026-09-18) 포이즌 리전 = 3차 포이즌 미스트 2111003 effect b0d47a89 + tile/0~8 독안개 9종(트랙 65칸 루프) + mob e42be518(틱) + use/hit(원작 2121055는 사운드만); 도트 퍼니셔 = 2121052 effect fce52ddb(시전 불꽃 해골) + 사운드 5차 400021001 use/use2(1.18초; 이 ID엔 클립 없음) + 구체 = **자체 업로드 RtsDotOrb01~03**(스킬 아이콘 d998c591·20a64945를 원형 컷, 3769c672·b0b300d3·da5ad791, 1.8배 맥동·240°/초 자전) + 박치기 폭발 12121055 hit/0 9b8b4484(0.7배). 12121055 effect 50781432의 0~4 프레임은 납작한 '불접시', 5~11은 둥근 화염구(폐기). 흐름: 시전음 동안 동심원 고리(2.0/+1.2, 둘레÷1.2개)에 30개 생성·호버 → 시전음 끝에 가장 가까운 적(보스 우선) 중앙으로 4.4유닛/초 → 박치기 판정. **비숍** 엔젤레이 = 2321007 effect e86eef7f(등 뒤 금빛 날개)·ball 77bc39d2(빛살 281px, 촉 왼쪽)·hit/0 341a2fd0·hit 사운드(use 없음); 제네시스 = 2321008 effect0 1c434f7c(천사, 원점 왼쪽 치우침 → assetFacesLeft=false로 항상 등 뒤)·tile/0~5 빛기둥(착지 ≈1.1초)·hit/0 74f50015·use/hit. 빙결 아이콘 = 2221007 icon a05d1321. 아바타 액션에 magic 계열은 없음 → 마법사는 swingO1/O2/O3(한손) + 대기 stand1.
- Scope: project
- Rationale: User request 2026-09-18 "마법사 3 → 도적 2 → 팬텀, 그 뒤 실제 라운드 테스트"
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

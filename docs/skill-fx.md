# 스킬 연출(fx) 필드

`RtsJobTableLogic.GetSkillsRaw`의 스킬 항목 `fx` 표와 스킬 항목 필드 설명. 코드 주석에 한 줄(약 2천 자)로 있던 것을 2026-09-28 정리로 옮겼다.
재생은 `RtsSkillFxLogic`(클라), 판정은 `RtsCombatLogic.DoAttack`(서버)이 읽는다. 연출 실험은 클라 스크립트에서 `_RtsJobTableLogic.FxOverrides["hero:1"] = {...}`로 한다(확정되면 표로 옮기고 비운다).

- 기본: `motion` 원화 동작 이름(RtsJobTableLogic.JobDefs frames의 키) / `frames` 플립북 스프라이트 RUID(`frameSec` 간격) / `scale` 월드 스케일 / `feetDx`·`feetDy` 캔버스 중심→발 오프셋(×scale) / `sound` 시전음 / `hitSound` 타격음
- 스킬 항목: `lock`(액티브만, 없으면 0) 잠금 기본값 0 사용 · 1 보스전 잠금 · 2 잠금 / `cd`(초) 쿨타임 — 준비됐으면 기본 공격보다 먼저

- motion 하나 또는 motions = {…} + motionGap(초)로 아바타 액션을 이어 재생, motionRate = 액션 재생 속도(1 원속, 0.56 = 0.44초 swing이 0.78초), motionLoop = 공격하는 동안 그 액션을 루프로 유지(폭풍의 시; motionFrame·motionFrameEnd = 그 프레임 구간만), motionCycle = motions를 motionGap 간격으로 공격이 이어지는 동안 차례로 반복(조커)
- loopClip·loopScale·loopDx·loopDy·loopAlpha·loopOrder = 공격 중 유닛 위에 계속 도는 클립(시전이 0.6초 끊기면 정리, 유지 자세도 함께; loopOrder 190 = 아바타 뒤 — 조커)
- loopIntro·loopIntroScale·loopIntroDy·loopIntroLife·loopIntroSound = 루프가 처음 생길 때 같은 자리에 1회 클립·소리(그동안 루프는 투명 — 애로우 레인 활 소환)
- loopFrameA·loopFrameB = 루프 클립의 프레임 구간(0부터)만 반복
- loopSound·loopSoundVol = 루프 동안 반복 소리(끝나면 StopSound), loopEnd·loopEndLife·loopEndSound = 루프가 끊길 때 같은 자리 1회 클립·소리(디바인 퍼니시먼트), loopAt "target" = 루프(인트로·엔드 포함)를 유닛이 아니라 메인 대상 몬스터의 자식으로(피격 박스 중앙 + loopDy, loopAtTop이면 박스 윗변 기준, 대상 바뀌면 재생성)
- 요소별 방향: clipFacesLeft·framesFacesLeft·bodyFacesLeft·loopFacesLeft·projFacesLeft가 있으면 assetFacesLeft보다 우선
- proj·projSec·projDy·projScale = 유닛에서 대상까지 날아가는 투사체 클립(비행 방향으로 회전, projNoRotate로 끔; projs = {…}면 발마다 차례로(라운드 로빈) 1개 — 조커 카드 4종)
- markClip·markLife·markLoop = 시전 순간 대상 위 표식 클립(스나이핑 조준; 위치 = 피격 박스 중앙, 크기 = markFit × 박스 긴 쪽 — 없으면 markScale·markDy; markClips = {…} 무작위 1개, markAt = "feet"면 발 위치 + markDx·markDy, markDelay 초 뒤 + 대상마다 markStagger 초씩 늦게(서버 hitStagger와 짝), markPattern "alternate" = 같은 대상 반복 표식을 좌·우 번갈아 markAltDists 거리로(블리자드 템페스트), markScaleX = 가로만 추가 배율; marks = { {clip, clips, delay, life, scale, at, dx, dy, fit, pivotDy, loop, stagger, pattern, scaleX} … } = 표식 여러 벌(블레이드 토네이도 → 카르마 퓨리))
- sound2·sound2Delay·sound2Vol·sound2Pitch = 두 번째 시전음
- beam·beamDelay·beamScale·beamSeg·beamDx·beamDy·beamLife = 유닛 손→대상까지 클립 조각을 이어 붙인 빔(체인 라이트닝)
- projCount·projStagger·projFrom("around" 유닛 주변 / "sky" 대상 머리 위 projSkyHeight에서 ±projSkySpread 흩어져 수직 낙하 — 애로우 레인)·projSpread(안쪽 고리 반지름)·projGap(구체 간격 = 고리 간격)·projLife = 구체 여러 개(도트 퍼니셔, 동심원 고리 채우기 OrbSpawnOffset), projHover = 생성 뒤 떠 있는 초, projSpeed = 유닛/초(있으면 비행 시간 = 거리÷속도, 판정도 그 시각), projFlySprites·projHitSprites·projFrameSec = 비행 중 돌릴 프레임 sprite 목록
- 닿은 뒤 한 번 돌릴 폭발 프레임 목록(클립 프레임 범위 지정은 안 먹음), projSpin = 자전 도/초, projArc = 포물선 높이(유닛; 비행 방향에 수직·항상 위로 4t(1−t) 튀어오름, 발마다 50~100% — projArcRandom=true면 위/아래 무작위; projArcByDist = { 1칸, 2칸, 3칸, 4칸+ } 있으면 대상까지 칸 거리로 고른 값 그대로)
- zoneClips·zoneScale·zoneAlpha·zoneLife·zoneOrder = 구역 트랙 모든 칸 위 지대 클립(포이즌 리전)
- backClip·backScale·backDx·backDy·backLife·backAlpha·backDelay = 캐릭터 뒤(190) 클립(블리자드 기둥; backDelay 초 뒤 — 카르마 퓨리)
- 스킬 항목의 after = 후딜 초(다음 공격까지 쉼), dot = { pct, period, dur } 서버 지속 피해, freeze = 빙결 초, range = 사거리 칸(기본 공격은 st.range가 우선, 없으면 2), targets = 타겟 수(없으면 st.targets), aoe = 메인 대상(사거리 안 가장 가까운 적) 곁 몇 칸까지 나머지 대상을 잡는지(범위 공격 기본 1, 체인 라이트닝만 3 — 2026-09-19 사용자), area = 전체 광역기(제네시스·생츄어리·블리자드·드래곤 로어: 메인 대상 없이 사거리 안 적을 랜덤으로 n마리), 지대 dot·구체 spread(도트 퍼니셔)는 사거리 제한 없이 구역 전체가 후보, zoneWide = 사거리 제한 없이 구역 전체에서 targets마리(블리자드 템페스트) — RtsCombatLogic.PickTargets, spread = 타격을 대상들에 돌아가며 1회씩(도트 퍼니셔), projEach = 대상마다 투사체 1발(RtsCombatLogic)
- clip(있으면) = 플립북 대신 애니메이션 클립 RUID 1회 재생(clipDelay 초 뒤), clips = { ruid 또는 {ruid, dx, dy, scale, delay, life} … } 같은 원점에 함께 띄우는 추가 클립들(스피어 버스터; life = 제거 시각 — 마지막 프레임이 긴 클립은 EndFrame 정리에 잘리므로 클립 총길이를 준다), clipHold = clip도 EndFrame 정리 대신 clipLife까지, clipOrder = 시전 클립 레이어(기본 300 앞, −10 = 아바타 뒤), motionDelay = 첫 모션 지연 초
- hideWeapon·hideWeaponSec = 스킬 동안 캐릭터 무기·무기 잔상 숨김(이펙트에 검이 들어 있는 레이징 블로우)
- bodyClip·bodyScale·bodyDy·bodyLife = 아바타 위 몸 덧그림(원작 effect0, RtsSkillFxLogic.PlayBody)
- assetFacesLeft = 원작(왼쪽 보기) 자산 — 유닛이 보는 방향(RtsUnitComponent.FaceDir)에 맞춰 반전, noFlip = 대칭 오라(반전 안 함)
- sound·soundDelay·soundPitch = 시전음(soundDelay 초 뒤 재생, soundPitch = 재생 속도)
- hitDelay 시전→첫 판정 초
- hitGap 타격 간격(타격마다 따로 판정·크리)
- hitStagger 같은 타격 안에서 대상마다 늦추는 초(블리자드 템페스트 30개 낙하)
- hitClip·hitScale·hitDy 몬스터 위 타격 클립(hitClips = {…}면 타격마다 무작위 1개 — 조커 3색)
- hitSound·hitSoundPitch·hitSoundVol·hitSoundEvery 타격음(피치 = 재생 속도, RtsSkillFxLogic.PlaySfx; hitSoundEvery = n타마다 1번), hitPhases = { {upto, clips, scale, sound, vol} … } 타격 번호 구간별 타격 클립·타격음(sound "" = 무음; hitKinds = { 타격마다 phase 번호 } 가 있으면 구간 대신 그 번호) (RtsCombatLogic·RtsMonsterComponent)

무기 숨기기(`hideWeapon`·`hideWeaponSec`)는 아바타 대체 외형과 함께 2026-09-28 삭제 — 원화엔 따로 그린 무기가 없어 이 필드는 효과가 없다.

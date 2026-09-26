# workflow

## 게임 변경과 .info 설정 문서는 같은 작업에서 동기화한다
- Rule: 게임의 외형·자산·모션·흉상, 능력치·스킬·증강·비용·전투, 테마·UI·진행 규칙이 바뀌면 관련 `.info/` 문서도 같은 작업에서 갱신한다. 문서 첫 줄에 예외를 덧붙이는 것으로 끝내지 않고 기존 본문·요약·표·참조 경로까지 고친다. 관련 형제 문서와 `docs/`도 함께 대조한다. 수치 변경은 계산식과 파생 표까지 반영하고, 미구현 제안·과거 실측은 현재 적용 정보로 쓰지 않는다. `.info/README.md`의 대응표를 작업 전후에 확인한다.
- Scope: project — `.info/` 폴더의 게임 설정 정보 전체. 로컬 전용·커밋 금지는 유지한다.
- Source: 사용자 2026-09-26 "썬콜 정보가 현재와 달라. .info 폴더 안의 설정 정보들은 우리 게임 내용이 바뀔때마다 동기화 되어야 해."
- Priority: takes precedence over defaults. 설정 문서 동기화는 작업 완료 조건이다.

## 로드맵·플랜은 코드가 아니라 방향·동작 설명으로 쓴다
- Rule: spec/plan/roadmap 문서에 mlua 코드 블록을 싣지 않는다. 무엇을 어떻게 동작하게 할지, 왜 그렇게 하는지, 어떤 선택지가 있는지를 사용자가 읽을 수 있는 말로 쓴다. 엔트리 포인트·시그니처는 이름 수준까지만.
- Scope: global
- Rationale: User feedback 2026-09-13 — "이번 프로젝트에서는 로드맵/플랜 작성시, 실제 코드보다 방향에 대한 설명 위주로만. 코드 안보고 전부 너에게 맡길거야."
- AGENTS.md application: not needed(non-code — 문서 작성 방식 선호)
- Priority: takes precedence over AGENTS.md/defaults (beaver plan 템플릿의 Design 코드 블록 관행보다 우선)

## 페이즈 완료는 사용자가 만족할 때까지 반복하는 루프다
- Rule: 페이즈는 build→ship 한 사이클로 닫지 않는다. ship 후에도 사용자가 원하는 것이 다 충족됐다고 말할 때까지 수정→검증→수정을 반복하고, 사용자의 명시적 확인이 있을 때만 로드맵에서 done 처리한다. 사용자 피드백에 따른 변경은 새 플랜 없이 같은 페이즈 안에서 Change 항목으로 누적한다.
- Scope: global
- Rationale: User feedback 2026-09-13 — "로드맵 페이즈 완료는 내가 원하는것들이 다 충족될 때 까지 작업을 계속하는 루프형으로 할거니 메모해놔"
- AGENTS.md application: not needed(non-code — 프로젝트 진행 방식)
- Priority: takes precedence over AGENTS.md/defaults (beaver roadmap의 "phase = one cycle" 규칙보다 우선)

## 커밋·푸시는 매번 사용자의 명시 승인 후에만 한다
- Rule: 어떤 파일이든(spec/plan 같은 문서 포함) 사용자가 "커밋해", "푸시해", "ㅇㅇ" 같은 승인을 준 뒤에만 커밋·푸시한다. 작업이 끝나면 변경 요약 + "커밋할까요?" 한 줄로 묻고 기다린다. 한 세션에서 여러 번 커밋하면 매번 다시 묻는다(한 번의 승인이 다음 커밋으로 이어지지 않음). beaver build는 커밋하지 않고, ship/roadmap 커밋도 승인 후에만.
- Scope: global
- Rationale: User feedback 2026-08-18 — spec/plan 문서를 승인 없이 푸시했다가 강하게 지적받음("왜 니멋대로 푸쉬하냐고?", "돌려라고"). `git reset --soft HEAD~1 && git push --force-with-lease`로 되돌렸음. 사용자는 푸시 시점을 본인이 통제하길 원한다.
- AGENTS.md application: not needed(non-code — 진행 방식)
- Priority: takes precedence over AGENTS.md/defaults (beaver ship의 자동 commit+push보다 우선)

## character.md · skill.md · balance-detail.md · damage.md · augmentation.md · weapon.md는 형제 파일 — 하나 바꾸면 나머지도 같이
- Rule: `.info/character.md`(직업별 외형·능력치·영입 규칙), `.info/skill.md`(2026-09-22 character.md에서 분리 — 직업별 스킬: 종류·획득 레벨·**인게임 설명(팝업 툴팁 문구의 단일 원본, 날짜·근거 없이 "사거리 n 안의 적을 최대 m마리까지 x%의 데미지로 k회 공격한다. 재사용 대기시간 s초" 틀)**·설명(설계 메모)(스킬 아이콘은 안 씀 — 원작에 없는 스킬이 있어 사용자가 뺌)·연출 자산. 스킬 수치를 바꾸면 인게임 설명·설명·코드 desc 셋 다), `.info/balance-detail.md`(한눈에 비교표 2개 + 직업 특성표 + 직업별 성장 상세표), `.info/damage.md`(데미지 계산식·표 작성 규칙 — 2026-09-16 balance-detail 헤더에서 분리), `.info/augmentation.md`(증강 정의 — 2026-09-16 사용자가 만들어 직접 채우는 중. 헤더 규칙: 라운드별 정해진 등급 지급, 총 43개 = 브론즈 15 / 실버 15 / 골드 10 / 프리즘 3(자쿰·루시드·진 힐라), 스킬 강화 증강은 스킬 데미지%에 합연산)는 항상 한 세트로 관리한다. 증강 계산 규칙이 생기면 damage.md에도 쓴다. 계산 규칙이 바뀌면 damage.md에 쓰고 표를 재계산하며, 직업 수치가 바뀌면 상세표·비교표·특성표를 함께 갱신한다(생성 스크립트: scratchpad `balance_tables.py`/`balance_compare.py` 방식으로 손계산 금지). character.md의 공격력·레벨업당 공격력·스킬 배율·타겟 수·타격 수·최종 데미지 중 하나라도 바뀌면 balance-detail.md 해당 직업 표를 재계산한다. 새 직업이 character.md에 생기면 balance-detail.md에 같은 형식의 `## 직업` 섹션을 추가한다. `.info/level.md`(비용 원본)가 바뀌면 모든 직업 표의 누적 비용·증가량 열을 갱신한다. 사용자가 대화로 밸런스 변경을 말하면(예: "레이징 블로우 타격 수 2회로") 두 파일을 모두 내가 고친다 — 한쪽만 고치고 끝내지 않는다.
- Scope: project
- Rationale: User feedback 2026-09-15 — "이제부터 캐릭터.md와 밸런스.md는 형제야", "내가 레이징 블로우의 타격수를 2회로 늘려야겠다 라고 하면, 둘 다 수정해줘야함". 표는 정의의 파생물이라 어긋나면 밸런스 논의가 틀어진다.
- AGENTS.md application: not needed(non-code — 설계 노트 관리 방식. `.info/`는 gitignore된 사용자 로컬 노트)
- Priority: takes precedence over defaults

## 화면 UI 목업은 .info/artifacts/hud-layout.html이 원본, 같은 아티팩트 URL로 재발행
- Rule: 화면 수정/추가 요청이 오면 (1) `.info/artifacts/hud-layout.html`(gitignore, 로컬 원본)을 읽고 그 위에 수정, (2) `ver` span 버전 올리고 notes 갱신, (3) Artifact 도구에 `url`로 https://claude.ai/code/artifact/dfb49cfc-c83f-485c-b0b5-b91fc04cd701 을 넘겨 같은 링크로 재발행(다른 세션이면 먼저 `action: read`). 로컬 파일과 아티팩트를 항상 같이 갱신. 구조: 16:9 `.stage` + container-query(cqw), SVG 그리드 트랙(COLS=18 ROWS=12 CS=80 OX=300 OY=80), 우측 유닛 슬롯 6칸, 좌하단 증강 버튼, `#recruitModal`/`#augModal`/`#pickModal`, 헤더 미리보기 토글·테마 select. 게임의 `RtsThemeLogic` 프리셋과 1:1 — 새 테마는 양쪽에 같이 추가.
- Scope: project
- Rationale: User request 2026-09-14 — 화면 수정·컨텐츠 추가를 이 목업 기준으로 계속 요청. 세션 스크래치 파일은 사라지므로 로컬에 원본을 둠.
- AGENTS.md application: not needed(non-code — 목업 관리 절차)
- Priority: takes precedence over defaults

## 스킬 이펙트·모션·투사체는 전부 "보는 방향"을 확인하고 올린다
- Rule: 새 연출을 올릴 때마다 **등록 전에** 클립의 그림 방향을 확인한다 — 방법: 로컬 캐시(`resource_cache/msw/<xx>-animationclip/<yy>/<ruid>.win.mod`)의 프레임 GUID 목록(.NET 혼합 엔디안, 첫 GUID = 클립 자신)을 뽑아 `https://mod-thumbnail.dn.nexoncdn.co.kr/<r0-1>/<r2-3>/<ruid>_64.png` 썸네일을 시트로 붙여 보면 화살촉·바람 방향이 바로 보인다(scratchpad `clipsheet.py out.png 라벨=ruid …` — 캐시에 없으면 Play 클라에서 `SpriteRUID`로 한 번 스폰(probe)해 내려받게 한 뒤). 썸네일은 그림 방향만 알려 주고 **원점(어느 쪽으로 뻗는지)은 안 보인다** → 원점은 sprite .win.mod 헤더(ox, oy-바닥기준)로 읽거나 표식과 같이 스폰해 실측(msw-engine 참조). 시험대 확인은 허수아비 3기(우측 세로줄 14,2·14,3·14,4)로 다수 타겟까지, 1초짜리 연출은 슬로모 미리보기(PlayRate 0.05)로 잡는다. 그 뒤 (1) 오른쪽/왼쪽 보기 둘 다 이펙트가 앞(대상 쪽)으로 나가는지 스크린샷, (2) 요소별 방향 옵션(`assetFacesLeft`, `clipFacesLeft`/`framesFacesLeft`/`bodyFacesLeft`/`loopFacesLeft`/`projFacesLeft`, `noFlip`)을 클립 단위로, (3) 투사체는 대상 방향으로 반전, (4) 모션 전환도 방향 유지. 작은 스크린샷만 보고 판단하지 말 것 — 2026-09-18 두 번 틀려 사용자가 화냄.
- Scope: global(전투 연출 전부)
- Rationale: User feedback 2026-09-18 — 팔라딘 이펙트가 등 뒤로 나감 → "공격 이펙트도 반대로 나가네. 바라보는 방향으로 나가야함. 모든 캐릭 공통" / 폭풍의 시 keydown 반대 → "스킬 이펙트나 모션 등 전부 방향 신경써" / 신궁 피어싱에서 또 뒤집었다 되돌림 → "너 왜 자꾸 공격 이펙트 반대로 넣어서 꼭 한번 더 말하게 하게끔 하는거야?" — 사용자에게 보여주기 전에 내가 확인해야 한다
- AGENTS.md application: not needed(non-code 검증 습관)
- Priority: takes precedence over defaults

## Play 화면은 사용자가 보고 있다 — 루프 정지·슬로모 같은 화면 개입은 먼저 알리고, 끝나면 바로 복구
- Rule: 시험대 공격 루프 정지, 슬로모(PlayRate), 홀드 미리보기, 모션 캡처 등 Play 화면 상태를 바꾸는 작업은 시작 전에 한 줄로 알리고("캡처하느라 n분 루프 멈춥니다"), 끝나는 즉시 원래 상태(루프 재시작 또는 stop→refresh→save→play)로 되돌린다. 캡처 작업이 길면(5분↑) 중간에 진행 상황을 한 번 말한다.
- Scope: project
- Rationale: User feedback 2026-09-19 — 모션 35종 캡처하느라 히어로 루프를 멈춘 채 10분 넘게 진행 → "머해", "캐릭터 멈췃잖아", "눈으로 보게 해줘야할거아냐". 사용자는 Play 화면을 계속 보며 결과를 확인한다.
- AGENTS.md application: not needed(진행 방식)
- Priority: takes precedence over defaults

## 마크다운 표를 스크립트로 고칠 땐 표 범위를 먼저 잘라낸 뒤 행을 치환한다
- Rule: `^\| 직업명 \|` 같은 정규식으로 행을 바꿀 때 같은 이름으로 시작하는 행이 여러 표(직업 특성 표·사거리 표·요약표)에 있으므로, 반드시 `## 절 제목`으로 그 표 구간을 먼저 슬라이스한 뒤 그 안에서만 치환한다. 치환 뒤엔 바뀐 표 전체를 한 번 눈으로 확인(열 개수·텍스트 칸이 숫자로 바뀌지 않았는지).
- Scope: project
- Rationale: 2026-09-19 balance-detail.md — 사거리 표를 겨냥한 정규식이 위쪽 직업 특성 표 행을 먼저 매치해 공격속도·역할 칸을 DPS 숫자로 덮어씀. 두 번의 패치를 거친 뒤에야 발견해 11행을 원문에서 다시 써야 했다.
- Priority: takes precedence over defaults

## 2026-09-22 커밋 정리: 자동 커밋 2건(39ddeca·cef9743) 위에 cd19489로 덮음 — plan/spec 파일은 그 커밋에서 삭제
- Rule: 원격에 남아 있던 사용자 측 자동 커밋(plan/spec 포함)은 force push가 막혀 되돌리지 못했고, `git reset --soft origin/main` 뒤 작업 트리 전체를 cd19489로 커밋해 내용만 바로잡았다(역사엔 남음). 스킬 문구는 `.info/skill.md` 인게임 설명 → 스크래치 `sync_desc.py`로 RtsJobTableLogic desc 65+11+5개 일괄 반영(2026-09-22). 팔라딘 매직 크러쉬 → 가드 크러쉬(사용자 개명).
- Scope: project
- Rationale: 사용자 "커밋+푸쉬 진행하자"(2026-09-22 저녁).
- Priority: takes precedence over defaults

## .info/ 문서는 로컬 전용(gitignore) — 절대 커밋하지 않지만, 개발할 때는 반드시 읽고 따른다 (2026-09-22 사용자)
- Rule: `.info/*.md`(character·skill·balance-detail·damage·augmentation·weapon·attack 등)는 설계의 원본이고 로컬에만 둔다. 커밋·푸시 대상에서 제외(ignore 예외 제안 금지). 대신 스킬·증강·밸런스·연출 관련 작업을 시작할 때 해당 .info 문서를 먼저 읽고, 수치·문구는 거기서 가져오며, 바뀌면 형제 문서와 코드(예: RtsJobTableLogic desc)에 반영한다.
- Scope: project
- Rationale: 사용자 "이 내용들은 전부 다 로컬 전용이고 안 올릴 거야. 하지만 개발할 때 너가 참고는 해야 해".
- Priority: takes precedence over defaults

## 사용자에게 보내는 답변은 한글로만 쓴다 (2026-09-23 사용자)
- Rule: 채팅 답변·진행 보고·질문은 한국어 문장으로만 쓴다. 영어 문장·영어 요약을 섞지 않는다. 코드 식별자·파일 경로·메서드 이름은 그대로 두되 설명 문장은 한글.
- Scope: global
- Rationale: 사용자 "한글로만"(2026-09-23 — 영어로 쓴 테스트 안내 뒤).
- Priority: takes precedence over defaults

## 2026-09-23 종료 시점 인계 (Phase 6+7 build, direct 모드, 전부 미커밋)
- 마지막 Play 재시작 18:48(빌드 에러 없음). 그 뒤 고친 것 — **아직 한 번도 빌드·Play 확인 안 함**(다음 세션 첫 재시작 때 `maker_logs(build)`부터):
  - 전투: 캐릭터 방향 고정(FaceLockUntil·CastFxFace·LocalFace), 판정 순간 대상 재확정(ResolveTarget·HitOnce), 보스전 사거리 16
  - 보스: 영역 4×5(8~11열×9~13행, 배치 불가·붉은 판) + 그림이 영역을 꽉 채움, 방어율(루시드·윌 175 / 더스크·진 힐라·듄켈 200 / 검마 1~3 250 / 4페 300) + 체력 상한(combo_dps), 4페 2,044,189, 검은마법사 표시 이름
  - 직업: 다크나이트(숙련 20·버서크 30 +50%·드래곤 로어 최종 +20%), 썬콜 체라 강화 355%, 프리즘 50레벨 제한 제거, 발할라·블스아이 방무 60, 초월 60구체, 거대화 방무 25, 엘릭서+템페스트 방무 15, 도트 퍼니셔 5.18유닛/초, 트루 스나이핑 피어싱 잠금 해제
  - 증강: 갑옷 꿰뚫기(방무 브3/4/5·실6/7/8·골10/12/15), 방어구 부수기 20·중복 가능, 뽑기 3,000 + 800, 누적 10개
  - UI: 좌상단 정보 카드(라운드·시간/맵/메소·필드), 다시 하기 = 영입 버튼 오른쪽(언제든 투표), 좌하단 버튼 붙임, 상세보기 Tab 전환, 몬스터 상태창 아이콘, 보스 등장 초읽기
  - 클리어 기록: 최종 메소(보유 + 유닛 판매 30%) → RtsClearMeso(정렬)·RtsClearRecord(조합), 결과 창 순위
  - 몬스터: 25라운드 뒤 체력 상승폭 절반, 아케인리버 작은 몹 리본돼지 × 1.1(tools/mob-visual.json), 보스 체력(혼테일 +30%·핑크빈 ×2·시그너스 ×3.5)
  - 09-24 추가(여전히 미빌드): 프리즘 3개 · 템페스트 통합 · 방어구 부수기 50 · 보스 슬레이어 60 → **곱연산 방무**(AddIgn·DefenseMul, 하한 삭제) · 보스 방어율 스우·데미안 200 ~ 검마4 350 · 일반 몬스터 방어율 0 · 갑옷 꿰뚫기 가중치 ×3 · 스우~검마 체력 재보정(LATE_HP) · 유닛 창 '보스 방어율 무시' · 몬스터 정보 창 방어율은 보스만 · 직업 티어 재설계(합연산 방어 · 증강 방무 삭제 · 프리즘 보공 → 보스 스킬 배율 · 증강 효율 · 템페스트 방어 깎기 · 퍼니시먼트 받는 데미지) + 보스 17개 체력 재보정(검마 클리어 3%) + 몬스터 디버프 아이콘 UI + 1티어 킷(공격력%·보공 → 최종) + 증강 탭 합계 + 증강 창 '적용된 증강 숨기기' + 밸런스 표 재작성(tools/balance-table.py)
- **Why:** 사용자가 "이제 내일 확인할게"로 종료. 변경이 많아 첫 재시작의 빌드 로그·화면 확인이 가장 중요하다.
- **How to apply:** 다음 세션 시작 → Maker 연결 확인 → stop·refresh·build 로그·save·play → 스크린샷으로 정보 카드·보스 영역 확인. 남은 일: build report, 로드맵 상태, 커밋은 사용자 승인 후. 루시드 이후 보스 체력은 사용자가 다시 준다고 함.


## UI 효과음 · 다시 하기 찬반 투표 (2026-09-24)
- Rule: 모든 UI 버튼 = RtsHudLogic.SpawnClick이 클릭음(원작 BtMouseClick 972843e7…)을 붙인다. 창 열기 = MenuUp(585c8f6d…) / 닫기 = MenuDown(69f85d65…) — RtsPopupLogic.Open/Close(다시 그리기 Reopening은 생략, 보스 3택1은 PickSound), 유닛 메뉴·몬스터 정보 창 열 때도. 새 버튼은 SpawnClick으로 만들면 소리가 자동.
- 다시 하기 투표: RestartVotes 1 찬성 · 2 반대, 투표 패널(다시 하기 버튼 아래, 투표 중에만 — 찬성 n · 반대 m / 과반 k · 남은 초), RequestVoteChoice, 과반 불가면 부결 · 20초(VoteTimeout) 지나면 부결.
- Why: 사용자 "버튼 클릭 · 창 오픈 때 다 효과음", "다시 투표 시 찬성/반대 표".
- (09-24) 카운트다운 15초(전 5) + 난이도 막대 오른쪽 '바로 시작'(RtsStageLogic.RequestStartNow — 방 인원 전원이 누르면 즉시, 혼자면 바로). 다시 하기는 카운트다운 중 금지(계속 누르면 타이머 리셋되던 것). 증강 도감 프리즘 탭 = 직업명/공통/팬텀 칩 + 행 클릭으로 설명 펼치기(그 자리에서 행 높이만 바꿈).
- (09-24) 영입은 진행 중에만(RtsUnitLogic.RequestRecruitAt · 카운트다운 영입 팝업 자동 열기 → 1라운드 시작 때). 영입 버튼 = 오른쪽 유닛 슬롯 아래(130×56), 영입 가능할 때·'나가기' 때만 보임. 난이도 막대는 대기·카운트다운에만(혼자면 죽으면 판이 끝나 '관전하기' 때 막대가 뜨던 것).

## 게임 버전 = v + YYMMDD + '-' + 그날 커밋 순번 (2026-09-24 사용자)
- Rule: 게임 버전 표기는 `vYYMMDD-N` — 날짜(연 두 자리·월·일) + 그날 몇 번째 커밋인지(1부터, 날짜가 바뀌면 다시 1). 첫 버전 = **v260924-1**(솔로 출시 — 출시 노트·로드맵 반영 커밋, 이 규칙은 그 커밋부터 센다. 그 전 09-24 커밋 4개는 세지 않음). 커밋 메시지 첫 줄 = `YYYY.MM.DD vYYMMDD-N`(AGENTS.md Commit). 로드맵 머리말·Progress 줄에 현재 버전을 적는다.
- Why: 사용자 "이제부터 버전에 날짜 + 커밋 횟수가 붙어. 이게 게임 버전임" + 출시 노트(버전 v260924-1, 개발 예정 로드맵 1~5).
- How to apply: 커밋할 때 `git log --since=<오늘 0시> --format=%s`로 오늘 버전 붙은 커밋 수를 세서 +1. 출시 노트·패치 노트에 같은 버전을 쓴다.
- AGENTS.md application: AGENTS.md Commit 절 첫 줄 규칙에 반영(2026-09-24)
- Priority: takes precedence over defaults

## 백슬래시가 들어간 패치는 Bash heredoc으로 넘기지 않는다 (2026-09-24)
- Rule: Bash 도구의 heredoc(`python - <<'EOF'`)으로 파이썬 패치를 돌리면 `\128`·`\n` 같은 백슬래시가 한 단계 풀려 `.mlua`에 8진수 문자·실제 줄바꿈이 들어간다(RtsHudLogic `string.gsub(sub, "[\128-\191]")` 줄이 깨졌던 일). 백슬래시가 있는 치환은 Write 도구로 스크래치에 .py를 만들어 실행하거나 Edit 도구로 고친다. 패치 뒤 `grep -c $'\x01'`로 깨진 바이트가 없는지 확인. `python3`은 이 PC에서 스토어 스텁이라 `python`을 쓴다.
- Why: 2026-09-24 두 번 깨짐(맵 이름 글자 크기 줄, 프리즘 Lv 줄).
- AGENTS.md application: not needed(작업 도구 요령)
- Priority: takes precedence over defaults

## 화면 문구에 개발용 분류(티어·서포터)를 쓰지 않는다 (2026-09-24)
- Rule: '1티어/2티어'·'서포터' 같은 직업 분류는 개발 관점 용어라 이용자에게 보이는 모든 문구(팝업·툴팁·디버프 설명·증강 설명)에 쓰지 않는다. 효과가 특정 직업에 걸리면 직업 이름을 직접 쓰고(예: 방어구 부수기 설명 = 효과를 주는 유닛의 직업 이름), 분류 표기만 하던 줄은 통째로 없앤다. 코드·주석·.info·docs의 분류는 그대로 둔다.
- Why: 사용자 "제발 여기에 1티어 이딴 것 좀 없애면 안 돼? 1티어/2티어는 내가 개발 관점에서 나눈 거지 유저는 그런 거 몰라야 해"(캐릭터 상세 증강 합계 칸의 '1티어' 줄).
- How to apply: 새 문구를 넣을 때 `grep -n '"[^"]*티어' RootDesk/MyDesk/*.mlua`로 문자열 안의 티어 표기가 0인지 확인.
- AGENTS.md application: not needed(화면 문구 방침)
- Priority: takes precedence over defaults

## 사용자가 Maker에서 플레이 중이면 시험 스폰·화면 조작을 하지 않는다 (2026-09-25)
- Rule: 사용자가 Maker Play를 직접 하고 있을 때(판이 진행 중, 사용자가 창을 열고 닫는 중)는 execute_script로 UI·엔티티를 만들거나 팝업을 열지 않는다 — 읽기 전용 확인만. 시험 스폰이 꼭 필요하면 먼저 묻고, 만든 것은 한 스크립트 안에서 pcall로 감싸 오류가 나도 반드시 지운다(이름 접두어 `Zz`, 끝에 남은 `Zz*` 정리 확인).
- Why: 격자 레이아웃 시험용 틀을 팝업 그룹 아래 만들었는데, 스크립트 오류로 하나가 안 지워져 사용자 화면에서 증강 창이 뜰 때 흰 박스로 보였다 — 사용자 "증강창 뜰 때 흰 박스 나왔는데 이거 뭐지? 테스트 했어?"
- How to apply: 확인은 사용자에게 Play를 멈춰도 되는지 묻고 내가 새로 Play를 켠 세션에서 한다.
- 2026-09-25 사용자 "이제 재시작 그냥 해도 돼 — 밸런스 테스트 끝났으니": 그 뒤로 화면 확인용 재시작(stop → refresh → save → play)은 묻지 않고 바로 한다. 사용자가 다시 "플레이 중"·"테스트 중"이라고 하면 이 규칙(묻기)으로 돌아간다.
- AGENTS.md application: not needed(작업 방식)
- Priority: takes precedence over defaults

## 트랙(길) 모양은 정직한 반복보다 불규칙하게 — 커브 섞고 특징 지점은 몰렸다 흩어지게 (2026-09-25)
- Rule: 트랙·맵 배치를 새로 짤 때 "긴 직선 → 매듭 → 긴 직선 → 매듭"처럼 규칙적으로 반복하는 모양은 피한다. 꺾임(커브)을 섞고, 특징 지점(매듭·전사 자리 등)은 일부는 붙여 두고 일부는 멀리 떨어뜨린다. 후보는 칸 지도 그림(여러 안 나란히 + 길 칸 수·발판 수)으로 보여주고 고르게 한다.
- Why: 매듭 3개를 모서리마다 하나씩 둔 안에 사용자 "너무 정직해. 좀 난잡해 보이게 … 매듭이 2개는 이어지고 1개는 멀리있고" → 무작위 탐색으로 뽑은 불규칙 안(M2)을 골랐다.
- How to apply: 경로 후보는 조건(보스 둘레 발판 한 겹·차선 사이 발판 한 칸·교차는 직각만)을 거는 탐색으로 여러 개 뽑고, 밀도(좋은 자리 유닛이 한 바퀴 중 사거리 안에 두는 비율)와 길이를 지금 트랙과 나란히 적는다.
- AGENTS.md application: not needed(디자인 취향)
- Priority: takes precedence over defaults

## 화면이 바뀌면 바뀐 부분만 다시 그린다 — 창 전체를 다시 열지 않는다 (2026-09-25)
- Rule: 탭 전환·선택·서버 값 갱신 등으로 창 내용 일부가 바뀌면 **그 부분(컨테이너)만** 지우고 다시 만들거나 제자리에서 색·글자만 바꾼다. `Open(같은 kind)`로 창 전체를 다시 그리지 않는다. 탭 줄은 제자리에서 켜짐/꺼짐 모양만 바꾸고(`SetTabOn`), 바뀌는 목록·상세는 각자 컨테이너 엔티티로 둔다. 선택 표시(체크·테두리)는 해당 칸만 다시 칠한다.
- Why: 엔진이 UI를 여러 프레임에 나눠 만들어서, 창 전체를 다시 그리면 그대로인 부분(오각형·외형·탭)까지 번쩍인다 — 사용자 "탭 넘어갈 때마다 오각형이 번쩍", "화면 내용 바뀔 때마다 필요한 부분만 재랜더링하고 나머지 부분 좀 그만 건드려", "내가 이거 일일이 다 신경 써야 해?"
- How to apply: 새 창·탭을 만들 때 처음부터 "고정 틀 / 바뀌는 칸"으로 나눠 짠다. 사용자가 말하기 전에 스스로 지킨다(새 기능·수정 모두).
- AGENTS.md application: 제안 대상(코드 작성 규칙) — ship 때 docs/ui-screens.md 7장 규칙으로 옮길지 묻는다
- Priority: takes precedence over defaults

## 디자인은 ChatGPT가 이미지·가이드라인, Claude가 구현 (2026-09-25)
- Rule: 유닛 원화·모션 프레임·흉상은 docs/unit-art.md(요약 AGENTS.md Unit Art 절)를 따르며, 맡은 에이전트가 생성·적용·검증을 수행한다. 그 외 일반 UI 인계에서는 이미지 생성과 UI 디자인 판단(색·크기·배치·상태별 모양)을 ChatGPT가 한다. ChatGPT는 가이드라인을 `docs/design/<주제>.md`(양식 `docs/design-handoff.md`)에, 이미지를 `assets/design/<주제>/`에 둔다. Claude는 상태가 '구현 요청'인 가이드라인을 읽고 이미지를 새 리소스로 업로드 → 코드 반영 → Maker 확인 → ui-screens 표 갱신 → 가이드라인 상태 '구현됨(버전)'. 가이드라인에 없는 디자인 판단은 하지 않고 사용자에게 묻는다.
- Why: 사용자 "ChatGPT에서 이미지 생성은 직접 하고, 그 외 UI 같은 것들 디자인적 조절할 때는 가이드라인을 만들어서 너가 이어받을 수 있게 할 거야" — 두 앱은 직접 연결되지 않아 같은 폴더·git·문서로 주고받는다.
- How to apply: 세션을 시작하거나 사용자가 "디자인 반영"을 말하면 `docs/design/`부터 본다. 두 앱이 같은 파일·Maker Play를 동시에 만지지 않게, 작업 단위마다 커밋.
- AGENTS.md application: not needed(작업 분담 — AGENTS.md·docs/design-handoff.md에 적음)
- Priority: takes precedence over defaults

## 캐릭터 원화·모션 제작 규칙
- Rule: 원화 → 프레임 제작, 작은 호흡의 복수 대기 프레임·스킬별 연결 프레임(현재 대기 3장, 마법사 스킬 5장, 히어로 8/7장), 비율·색감·의상 일관성, 폴더/파일명과 결과물 정리는 docs/unit-art.md가 단일 기준이다(결정 배경은 [character-art](_archived/character-art.md)).
- Scope: project
- Rationale: User decision 2026-09-25.
- Priority: takes precedence over earlier character-art conventions.

## 규칙 문서와 자산 폴더는 날짜 대신 용도로 이름 붙인다
- Rule: docs의 지속적인 프로젝트 규칙·디자인 문서는 날짜 접두어 없이 주제명으로 관리한다. 자산 폴더도 실제 용도 이름을 사용한다(예: tombstone). 같은 문서·폴더를 계속 갱신하고 날짜별 복제본을 만들지 않는다. 링크와 템플릿의 경로도 함께 갱신한다.
- Scope: project
- Rationale: User feedback 2026-09-25 — 비석 폴더와 docs 규칙 문서의 날짜 접두어 제거 요청.
- Priority: replaces older dated design-handoff naming convention.

## 현재 게임 UI의 승인된 시각 방향
- Rule: 새하얀 반투명 물결 UI를 사용한다. 기존 크림·브라운/청록 방향을 대체한다. 등급 문양 안에 능력치 그림을 넣고, 직업 프리즘에는 대응 스킬 그림을 넣는다. 보유 증강은 등급별 탭 없이 함께 표시한다.
- Source: 사용자 백색 물결 시안 승인과 프리즘 스킬 아이콘 합성 요청(2026-09-26).
- Scope: 현재 게임 UI. 구현·배치 판단은 사용자가 담당자에게 위임했다. 실제 값과 자산 기준은 docs/design-system.md와 docs/ui-screens.md를 따른다.

- 추가 UI 결정: 프로필 설정/연결창과 좌상단 프로필·정보는 불투명. 유저 카드는 낮은 가로형 한 면의 왼쪽 아이콘·오른쪽 닉네임. 3택1 텍스트는 가로 중앙, 보유 증강 이름/미지정은 세로 중앙. 대상 유닛은 직업명 왼쪽·레벨 오른쪽 한 줄이며 번호는 생략한다(2026-09-26 사용자).
- 추가 UI 결정: 유저 카드 배경은 각자의 선택 테마, 닉네임은 오른쪽 정렬, 내 카드는 테두리 문양으로 구분한다. 프로필 선택 확인은 목록 위에 겹쳐 띄운다. 아이콘 목록은 이름·썸네일 영역을 분리한다. 난이도 선택은 시작 전만 표시하고, 바로 시작은 그 아래에, 진행 중 다시하기는 난이도 선택이 사라진 상단 자리에 표시한다.
- 액션 테마는 게임 배경뿐 아니라 각 사용자 카드 배경에서도 재생한다. 정지 썸네일은 테마 선택 목록에만 쓴다(2026-09-26 사용자).

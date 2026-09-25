# archived — 2026-09-25 AGENTS.md · docs/unit-art.md 대조 완료 (5개 조항)

# character-art

유닛 원화·프레임 작업의 사용자 결정. 수치·파일 구조·코드 연결·확인 절차는 [docs/unit-art.md](../../../docs/unit-art.md)가 단일 기준이다(AGENTS.md의 화면·자산 협업 절은 요약).

## 원화 먼저, 사용자 OK 뒤에 프레임
- Rule: 직업별 외모·의상·소품·표정 컨셉을 정해 원화부터 보여 주고, 사용자가 OK한 뒤에만 대기·스킬 프레임을 만든다. 프레임마다 따로 해석해 다른 캐릭터처럼 만들지 않는다. 이미 승인된 캐릭터는 그 승인과 현재 결과물을 기준으로 필요한 부분만 고친다.
- Why: 사용자 2026-09-25 "1: 원화 그리기 2: 각 모션에 대한 프레임 구성".
- AGENTS.md application: 반영됨(Unit Art 절 · docs/unit-art.md 1절)
- Priority: takes precedence over defaults

## 대기 1장 고정, 스킬마다 약 3장
- Rule: 대기는 정지 1장, 흔들림·호흡·기울기·크기 변화 없음. 공격 스킬마다 약 3장을 준비·시전·마무리 순서로 재생하고 시전이 끝나기 전에 대기로 돌아가지 않는다. 메월 모션을 대체할 때는 원본 자세·순서·타격 시점을 따른다. 패시브에 공격 프레임을 늘리지 않는다.
- Why: 사용자 2026-09-25 "흔들림 제거", "대기 모션 1장", "각 스킬 3장 정도".
- AGENTS.md application: 반영됨(docs/unit-art.md 1·2절)
- Priority: overrides earlier idle sway/breathing requirements

## 그림체·인체 비율 통일 — 썬콜 기준
- Rule: 이후 캐릭터도 썬콜과 같은 매끈한 2D SD 그림체와 약 2.06등신 비율을 따른다. 기준은 실제 결과물 `ice-lightning-mage/frames/wait/motion01.png`(별도 기준 사본 금지). 모든 프레임에서 비율·색감·의상·장식·무기를 일정하게 유지한다.
- Why: 사용자 2026-09-25 "그림체 통일 인체비율 통일", "캐릭터의 인체비율이나 색감, 의상 등을 항상 일정하게", "썬콜과 같은 인체비율 정보를 남겨 놓고 그걸 따르도록".
- AGENTS.md application: 반영됨(docs/unit-art.md 2절 비율 표)
- Priority: takes precedence over defaults; 원화 승인 후 사용자 비율 수정 요청이 최우선

## 표정은 직업마다 원화에서 정한다
- Rule: 통일하는 건 그림체·비율이고 표정은 직업의 성격에 맞게 원화 단계에서 정해 사용자 OK로 확정한다. 모든 직업에 미소를 일괄 적용하지 않는다. **썬콜 = 은은한 미소**(과장된 활짝 웃음·찡그림 금지). 다른 직업은 미정.
- Why: 사용자 2026-09-25 "다른 직업들은 미소가 아닐 수도", "표정 컨셉도 정해서 원화", "썬콜의 표정 컨셉은 은은한 미소".
- AGENTS.md application: 반영됨(docs/unit-art.md 2절)
- Priority: takes precedence over defaults

## 결과물만 남기고 실제 게임에 적용한다
- Rule: 캐릭터 자산 폴더에는 쓰는 프레임과 흉상만 둔다(`frames/wait`, `frames/<english-skill-name>/motion01~`, `portrait.png`). 레퍼런스·원화 사본·반려 시안·프롬프트·미리보기·스크립트·README를 쌓지 않고, 고칠 때는 같은 파일을 교체한다. 적용 요청을 받으면 파일 교체로 끝내지 않고 RUID 연결·프레임 순서·재생 시간·흉상 UI까지 확인한다. 폴더·문서 이름에 날짜 접두어를 붙이지 않는다.
- Why: 사용자 2026-09-25 "대기는 wait 폴더, 각 스킬명 폴더, 파일명은 motion01, 02", "실제 프로젝트 안의 프레임들로 교체", "레퍼런스 이런 것들은 지우자. 결과물만 있으면 돼".
- AGENTS.md application: 반영됨(Unit Art 절 · docs/unit-art.md 3·5절)
- Priority: takes precedence over previous reference/prompt archiving conventions

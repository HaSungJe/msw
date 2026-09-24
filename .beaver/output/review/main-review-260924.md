# Review — main — 260924

> ship 전 셀프 리뷰(direct 모드). 기준: `.beaver/memory/` 규칙 → CLAUDE.md 컨벤션 → plan/spec 의도.

## Target
- 브랜치: `main`(direct 모드, 워크트리 없음) → origin/main
- 포함 기능
  - 로드맵 Phase 6 + 7(한 plan): 스테이지 132·웨이브·보스·클리어/탈락·결과 — `.beaver/output/plan/rts-stage/stage-wave-boss-plan.md` + `revision-1`(Phase 4 증강 합류: 3택1·증강 뽑기·도감)
  - 밸런스 재설계(Phase 9 성격, 09-23~24 사용자 지시): 1·2티어 + 서포터, 1티어 증강 배율 램프(프리즘 있을 때만 ×1→×3)·방어구 부수기 디버프, 2티어 약점 증강 ×2(프리즘 있을 때만)·팬텀 ×1.75, 보스 최종 데미지 전부 ⑤ 스킬 데미지로 통합, 뽑기 3,000 + 40·프리즘 최대 2개·천장 +2%p, 난이도 6단계(체력 × 난이도 × 극악 곡선), 테스트 모드 +100만
  - UI: 난이도 막대 + '바로 시작'(카운트다운 15초), 다시 하기 찬반 투표(20초), 효과음(클릭·열기·닫기), 증강 도감(등급 탭·프리즘 칩·펼치기), 영입 버튼 우측 이동·영입 가능할 때만, 몬스터 정보 초상 마스크·디버프 아이콘
  - 삭제: `RtsDemoLogic`(시연 몬스터 — plan §10 삭제 목록)
- 변경 규모: 수정 22파일(+3,031 / −797) + 신규 Logic 10종(mlua + codeblock) + tools/*.py 시뮬레이터·생성기 9종

## Convention Check (against CLAUDE.md)
| Item | Result | Notes |
|------|------|------|
| Naming | pass | 신규 10종 전부 `Rts*Logic` PascalCase + 역할 접미사. 프로퍼티·메서드 PascalCase, 지역 변수 camelCase |
| Structure & layering | pass | 표/순수 계산 = Logic(`RtsStageTableLogic`·`RtsAugmentTableLogic`·`RtsDifficultyLogic.CurveAt`), 엔티티 수명 = Component(`RtsMonsterComponent`·`RtsTrackWalkerComponent`) |
| 실행 공간 명시 | pass(기존 예외 유지) | `Request*` RPC 전부 `@ExecSpace("Server")` + `senderUserId` 검증. 미표기 메서드는 표·게터 순수 함수와 `OnBeginPlay` — 2026-08-02 리뷰에서 기록한 의도적 예외(호출 공간에서 실행되는 공용 함수)와 같은 패턴 |
| 권한 민감 로직 Server | pass | 메소 차감·뽑기 굴림(`RtsAugmentLogic.RequestBuy`), 영입 배치(`RtsUnitLogic.RequestRecruitAt` — 진행 중만), 난이도 설정(진행 중 거부), 체력 배율(`HpMul` ServerOnly), 방어구 부수기(`RtsCombatLogic.ArmorBreak` ServerOnly), 기록 저장(`SaveClear` ServerOnly) |
| NativeScripts 무수정 | pass | `git diff HEAD -- Environment` 비어 있음 |
| 새 Logic codeblock | pass | 신규 10종 모두 `.codeblock`(새 GUID·Name·Type 5) 동봉, 삭제한 `RtsDemoLogic`은 mlua·codeblock 같이 삭제, 잔존 참조 0 |
| Errors & responses | pass | RPC는 조건 불충족 시 조용히 return, 클라 버튼(`BuyFromHud` 등)이 사유를 힌트로 먼저 안내 |
| Test strength | pass(스택 규칙) | CLI 테스트 없음 — Play Test로 검증: 09-24 마지막 재시작 build 로그 에러 0(알려진 LEA-3035 타일맵 경고만), normal 로그에 난이도 선택·바로 시작 1/1·진행 중 영입·재시작 투표 → 카운트다운 흐름 확인 |
| 데이터 접근 스모크 | 해당 없음 | DataStorage 사용(`SaveClear` — 난이도별 `RtsClearMeso_D<n>`·`RtsClearRecord_D<n>`)은 ORM/쿼리 매핑이 아닌 엔진 API. 읽기·쓰기 이름 일치 확인 |

## Intended Behavior Check (against plan/spec)
- Phase 6 + 7 plan: 표(132 스테이지)·방 전역 진행·구역별 웨이브·보스(영역 고정·60초·몹 보관)·누적 110 탈락·비석·결과 팝업·다시 하기 — 구현됨. revision-1(증강 합류)의 3택1·뽑기·대상 지정도 구현됨.
- plan 이후 사용자 지시로 바뀐 것(뽑기 가격·확률·천장, 난이도, 티어 재설계, 기록 = 최종 메소 순위)은 코드·`.info` 문서·메모리에 반영됨. 다만 **build report가 없어** plan 대비 변경 이력이 산출물에 남아 있지 않음(발견 #1).
- 사용자 Play 확인 대기: 효과음, 증강 도감 프리즘 칩·펼치기, 사망 후 '관전하기' 때 난이도 막대 비노출, 여러 명일 때 투표 패널.

## Findings
| # | Severity | Location (path:line) | Description | Recommendation |
|---|--------|-----------------|------|------|
| 1 | Medium | `.beaver/output/report/rts-stage/`(없음) | Phase 6+7 build report 미작성 — plan·revision-1 이후 사용자 지시 변경분(밸런스 재설계·난이도·UI)이 보고서에 없음. 메모리 인계(09-23)에도 "남은 일: build report" | 커밋 전에 `stage-wave-boss-report.md` 작성(구현 요약 + Change 라운드) |
| 2 | Low | `RootDesk/MyDesk/RtsRunResultLogic.mlua:245` | 테스트 모드(`RtsUnitLogic.DevTools` — 타격마다 +100만)로 클리어해도 `SaveClear`가 순위 저장소에 기록. 기본값 false라 지금은 영향 없음, 켠 채 배포하면 순위 오염 | `SaveClear` 앞에서 DevTools면 점수 표시만 하고 저장 생략 |
| 3 | Low | `.beaver/output/roadmap/maple-augment-defense-roadmap.md:113`, `:143` | 로드맵 #43 증강 구매 메모가 옛 수치(3,000 + 800·프리즘 0.5%·상한 없음), #30 결과 기록이 옛 방식(리더보드 점수 = 라운드 × 100,000) — 현재 코드는 3,000 + 40·5% + 천장 2%p·최대 2개, 난이도별 최종 메소 순위 | 상태 칸 메모만 현재 값으로 갱신(2~3줄 이내) |
| 4 | Low | `tools/__pycache__/` | 파이썬 캐시가 추적 대상 후보로 떠 있음 | 커밋에서 제외 + `.gitignore`에 `__pycache__/` 추가 |

## Memory Reconcile
사용자 승인(2026-09-24 "지금 이관") — 조항 전부 이관 후 원문은 `.beaver/memory/_archived/`로.
- 아카이브: 월드 스프라이트 프롭 model://MapObject · 유닛 아바타 방식 · EndFrameEvent · 줌 잠금 ZoomTo · PPU 30/Truncate · number 정수 포맷 · 입력·터치·UI 좌표 → `docs/msw-engine.md`(대조 완료: Rule 본문 7개 원문 일치 + 근거) + CLAUDE.md Conventions 요약·링크
- 아카이브: 커밋 메시지 형식 → CLAUDE.md `## Commit`(대조 완료: 6개 조항 — 날짜 첫 줄·빈 줄·불릿·트레일러 금지(시스템 안내보다 우선)·같은 날 여러 커밋·`-F -`) + Checklist
- 아카이브: Play 중 수정 시 refresh → CLAUDE.md Testing + docs/testing.md(대조 완료: 3개 조항 — 순서·원인·의심 순서)
- 분리: 타 유저 구역 보기 전용 — 코드 조항(조작 RPC 서버 소유자 검증)만 CLAUDE.md Conventions로, 제품 방향 조항은 메모리에 `not needed`로 유지
- 곁들여: docs/testing.md 데이터 검증 절 — DataStorage 사용처(`SaveClear` 난이도별 저장소) 반영

## Resolution (사용자 결정 2026-09-24 "전부 처리 후 커밋")
| # | 처리 |
|---|---|
| 1 | `.beaver/output/report/rts-stage/stage-wave-boss-report.md` 작성 |
| 2 | `RtsRunResultLogic.SaveClear` — DevTools면 저장소를 열지 않고 점수만 표시 |
| 3 | 로드맵 재정리 커밋에서 처리(사용자 "로드맵 다시 정리" — 증강·밸런스 완료, 순위 방식 변경) |
| 4 | `.gitignore`에 `__pycache__/` |
| + | 리뷰 뒤 사용자 요청: 몬스터 정보 초상 칸 정중앙(`RtsMonsterInfoLogic` NativeSize + 표 테두리로 역보정) — 시험 초상으로 확인 |

## Verdict
통과 — 발견 4건 처리(3은 로드맵 커밋), 커밋 진행.

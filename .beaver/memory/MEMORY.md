# Beaver Memory Index

- [workflow](workflow.md) — 로드맵·플랜은 코드 없이 방향 설명 / 페이즈 완료는 사용자 만족 루프 / 커밋·푸시는 매번 명시 승인 / 커밋 메시지 = 날짜 + `* ` 불릿·트레일러 금지 / character.md ↔ balance-detail.md ↔ damage.md 형제(계산식은 damage.md) / 화면 목업 원본은 .info/artifacts/hud-layout.html
- [msw-engine](msw-engine.md) — 프롭은 model://MapObject / 유닛은 아바타 방식(AddComponent) / 애니 끝은 EndFrameEvent / 줌 잠금 시 ZoomTo 무시 / PPU 30·Truncate / 공식 자산 검색 절차 / number tostring은 "1.0" → Int 포맷 / 터치·커서·UI 좌표·RPC(userId 마지막 인자, senderUserId) / 클라 스폰은 프레임 분산, MCP 도구 유령 클릭 / 스크롤 목록 = ScrollLayoutGroup(프로퍼티는 ScrollBar*, 짧으면 UseScroll 끔)
- [assets](assets.md) — 몬스터 = 이동·사망 클립 + 사망음(달팽이 RUID) / 속도 100 = 3.5u/s / 히어로·팔라딘·다크나이트 모험가 세트와 스킬 자산 RUID / 발판 틀·손 커서·파티 버프 스킬 아이콘 4종 / 테마 프리셋
- [balance](balance.md) — 공격 사이클 배속 규칙 / 사거리·타겟 규칙 / 데미지 계산 순서(합·곱·뺄셈) / 액티브 1개 규칙 / 대상 지정 = 셀렉트 박스 / 대상 변경·위치 이동 쿨 = 유닛당 3분 고정 / 과금 = 월드 아바타 30일 1,600코인(상품 QK03ZI15E) / 히어로 대기만성·팔라딘 초반 캐리 곡선 / 메소 30만 예산·비용 곡선 / 파티 버프 4종 = 발 아래 아이콘 + 팝업 우측 탭(스킬/증강/버프, GetStatRaw엔 안 넣음)

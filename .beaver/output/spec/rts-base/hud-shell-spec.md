---
feature_goal: "스타식 HUD 셸 — 하단 콘솔 바(미니맵+선택정보+커맨드카드 틀) + 우상단 자원/시간 표시, 미니맵 카메라 뷰포트·클릭 점프"
domain: "rts-base"
api_method: "Client UI + Input"
api_path: "RtsHudLogic (전역, 클라 구축) · RtsCameraAnchorComponent 연동(/ui/DefaultGroup 하위 런타임 조립)"
affected_data: []
---

## Feature Description
로드맵 #14. 스타크래프트식 화면 골격을 게임에 얹는다 (사용자 지정: "스타크래프트처럼").

- **하단 콘솔 바** (화면 하단 전체, 어두운 패널):
  - 좌측 **미니맵**: 동굴 바닥 텍스처 축소판 + **카메라 뷰포트 사각형**(스크롤 따라 실시간 이동) + **클릭 시 해당 지점으로 카메라 점프**
  - 중앙 **선택 정보 패널**: 자리 확보 (placeholder 텍스트 "선택된 유닛 없음" — 실데이터는 #3에서)
  - 우측 **커맨드 카드**: 3×4 버튼 슬롯 틀 (클릭 시 로그만 — 실기능은 #4 건설/#9 스킬에서 연결)
- **우상단 자원/시간 표시 자리**: "골드 0 · --:--" placeholder (실데이터는 #5 경제/#11 타이머에서)
- HUD는 **클라이언트 로컬**(각자 자기 화면) — 서버 동기화 불필요.

## Entry Point
- Method: Client UI (런타임 조립) + Input(ButtonClickEvent, GetCursorPosition)
- Path: `RtsHudLogic`(신규 Logic) — `RtsCameraAnchorComponent.SetupClient()`에서 1회 `BuildHud()` 호출로 조립, `OnUpdate`에서 미니맵 뷰포트 갱신 호출. UI 엔티티는 `/ui/DefaultGroup/RtsHud` 하위에 스폰.
- Request(입력): 미니맵 클릭(버튼), 커맨드카드 버튼 클릭, 카메라 앵커 위치(매 프레임)
- Response(결과): HUD 상시 표시, 뷰포트 사각형 이동, 클릭 지점으로 카메라 순간 이동(마진 클램프), 슬롯 클릭 로그

## Business Rules
1. **UI 좌표계는 1920×1080 기준**(MSW UI 기본 해상도). 모든 배치는 앵커(AnchorsMin/Max) 기반 — 해상도가 달라도 하단 바는 하단에 붙는다.
2. **미니맵 ↔ 월드 변환**: 미니맵 사각형(px) ↔ 맵 256×256유닛 선형 매핑. 클릭 좌표는 `GetCursorPosition()`(스크린px) → UI 좌표(×1920/ScreenWidth) → 미니맵 상대좌표 → 월드. 점프 목적지는 #1의 카메라 마진(26×15)으로 클램프.
3. **커서가 UI 위에 있으면 엣지 스크롤 무시** (`IsPointerOverUI()`) — 스타와 동일(콘솔 위에서는 화면 스크롤 안 됨). 키보드 스크롤은 항상 동작.
4. 뷰포트 사각형 크기 = 실제 카메라 뷰(≈44.5×25유닛, #1 실측) 비율. 상수는 튜너블.
5. HUD 구축은 클라당 1회 멱등(`Built` 가드). 서버 로직 없음 — Cross-Cutting Rule("판정은 서버")의 예외가 아니라 표시 전용이므로 해당 없음.
6. 커맨드 카드 슬롯은 12개(3×4) 고정 틀. 슬롯별 기능 바인딩 구조(이후 유닛이 채움)만 잡아둔다.

## Notes
- **근거 API**(전부 확인됨): UI 계층 `/ui/DefaultGroup/...` + `SetEnable`(공식 문서 Controlling UI Entities), 기본 UI 모델 Image/Button/Text(공식 문서 UI Editor — UITransform+SpriteGUIRenderer+ButtonComponent 구성), `UITransformComponent`(AnchorsMin/Max·Pivot·RectSize·anchoredPosition — d.mlua), `SpriteGUIRendererComponent`(ImageRUID(DataRef)·Color·FillAmount — d.mlua), `ButtonComponent`(ButtonClickEvent·KeyCode 단축키 — d.mlua), `TextComponent`(Text·FontColor·Alignment — d.mlua), `IsPointerOverUI`(InputService).
- 미니맵 배경은 #1의 커스텀 동굴 텍스처 RUID(`e9683cc5…`) 재사용 + 어둡게 틴트. 벽/유닛/몹 도트는 각 유닛(#4/#7/#9)에서 이 위에 추가.
- **미확정(빌드에서 실증)**: ① UI 기본 모델의 entry id(`GetModelIdByName` 후보: "Image"/"MODImage" 등) 및 런타임 스폰 가부, ② 런타임 스폰 버튼에 `ConnectEvent`로 클릭 핸들러 연결 패턴. 실패 시 폴백: UI 에디터로 골격 1회 수작업 생성 후 파일 직렬화 스키마 학습(#1 타일셋 때와 동일 수법) → 이후 파일 편집 자동화.
- Maker 실행 필요(빌드/검증 시).

## Proposals (Codebase-Based)
- [x] `RtsCameraAnchorComponent.SetupClient()`(RootDesk/MyDesk/RtsCameraAnchorComponent.mlua)에 HUD 구축 훅 추가 — 신규 진입점을 만들지 않고 기존 클라 초기화 지점 재사용 (§1.7 병합).
- [x] 카메라 뷰 크기·맵 크기 상수는 기존 `RtsConfigLogic` 게터 재사용 (#1 확립 패턴 — 게터 경유 크로스 엔트리 접근).
- [x] 엣지 스크롤 UI 가드(`IsPointerOverUI`)는 기존 OnUpdate 엣지 분기에 조건 1줄 추가 — 스펙 #1의 "UI 위 엣지 스크롤 허용" 규칙을 본 유닛에서 공식 폐기(스타 동작에 맞춤).

## Decisions
- [x] 레이아웃 — **스타크래프트식 하단 콘솔 바** (미니맵 좌/정보 중앙/커맨드카드 우 + 우상단 자원·시간). 사용자 확정(2026-08-02, "스타크래프트처럼").
- [x] 미니맵 렌더 방식(로드맵 key decision) — **색상 타일 방식**: 바닥 텍스처 축소 이미지 + 도트 오버레이(이후 유닛). 월드 축소 캡처는 렌더투텍스처 API 부재로 불가.
- [x] HUD 소유 — 클라이언트 로컬 (동기화 없음).
- [x] 배치 수치(바 높이 240px, 미니맵 220px 등) — 플랜 기본값으로 시작, Play Test 튜닝.

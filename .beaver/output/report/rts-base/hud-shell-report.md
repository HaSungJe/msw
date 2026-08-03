# Report — 스타식 HUD 셸 (rts-base #14)

## Feature Summary
- **Feature**: 스타식 하단 콘솔 HUD (미니맵+초상화+선택영역+스킬칸 3×3+툴팁+부대탭+골드/시간)
- **Entry point**: `RtsHudLogic`(클라 런타임 조립) ← `RtsCameraAnchorComponent.SetupClient()` 훅, UI `/ui/RtsHudGroup` 하위
- **Domain**: rts-base

## Created/Modified/Deleted Files
| File | Change Type | Description |
|------|-----------|------|
| `RootDesk/MyDesk/RtsHudLogic.mlua` | created | HUD 전체 조립·미니맵·스킬칸·부대지정 골격 (v4 — 사용자 피드백 3회 반영) |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | modified | HUD 조립 훅, 매 프레임 뷰포트 갱신, UI 위 엣지스크롤 억제(`IsPointerOverUI`) |
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | modified | 카메라 뷰 크기 상수(44.5×25)·게터 |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | modified | 바닥 채우기 가드 수정(기대 타일 수 미만 시 Clear+재채움 — 떠돌이 타일 이슈 해결) |
| `map/RtsMap.map` | modified | 떠돌이 타일 3개 제거 |
| 업로드 리소스 | created | `UiWhitePixel`(47b5e516…, 틴트 패널용), `UiGoldCoin`(e399bb21…, 골드 아이콘) |

## 최종 레이아웃 (v4 — 사용자 피드백 반영 이력: v1 기본→v2 확대/골드·시간 재배치→v3 플러시/바둑판 제거→v4 스킬칸 3×3·툴팁·프레임)
- 하단 콘솔 바(250px) + **미니맵 340px 좌하단 플러시(프레임 테두리)** + **초상화 240px(프레임)** + **선택영역(SC2식 — 선택 없으면 완전 공백, #3이 채움)** + **스킬칸 3×3(QWE/ASD/ZXC, 빈 슬롯 숨김, 우하단 플러시)**
- **스킬 툴팁**: 스킬칸 위 설명 패널 — 슬롯 호버(ButtonState.Hover) 시 표시
- **부대지정**: Ctrl+숫자열(넘패드 제외) → 콘솔 바 위 부대 탭(번호+유닛수) 표시, 숫자 단독 = 부대 선택. 이벤트 기반 Ctrl 추적(시뮬/실키보드 겸용)
- 골드(코인 아이콘+수치) 좌상단 / 시간 상단 중앙
- **공개 API**(후속 유닛용): `SetSkillSlot(slot,name,desc)`/`ClearSkillSlots()`(#4·#9), `UpdateMinimapViewport`(#1 훅), 부대 탭 갱신(#3)

## 실증으로 확정된 지식 (빌드 중 발견)
1. **UI 런타임 조립 체계**: 기본 UI 모델 = `model://uisprite`/`uibutton`/`uitext`/`uigroup`. `/ui/DefaultGroup`은 지연 생성이라 없음 → UIGroup 런타임 스폰. UISprite는 ImageRUID 지정 전 비가시.
2. **ConnectEvent는 엔티티 레벨만** 유효(컴포넌트 레벨 nil). 영속 Logic의 클로저 핸들러는 실마우스 클릭에서 정상 발화(미니맵 클릭 5회 실측 — rel 좌표 정상, 카메라 점프 동작).
3. **입력 시뮬 한계**: 엔진 UI 버튼은 시뮬 클릭/KeyCode로 발화 불가(실마우스는 됨), 동시 코드 입력은 이벤트 순서가 뒤바뀔 수 있음(modifier 분리 호출 필요), modifier 폴링 상태 미반영 → 이벤트 기반 Ctrl 추적으로 해결.

## Tests Written
CLI 러너 없음 — Play Test 시나리오(플랜) 실측이 검증. 스킬칸은 `SetSkillSlot` 더미 주입으로 표시/빈슬롯 검증.

## Verification (Play Test 실측, 2026-08-02)
| 시나리오 | 결과 |
|---|---|
| HUD 전체 렌더(미니맵/초상화/스킬칸/부대탭/골드/시간) | ✅ 스크린샷 |
| 미니맵 뷰포트가 카메라 스크롤 추적 | ✅ 이동 전후 스크린샷 |
| 미니맵 클릭 → 카메라 점프 | ✅ 실마우스 5회(rel 좌표 로그) — 사용자 실클릭 |
| 스킬 슬롯: 지정된 것만 표시, 빈 슬롯 숨김 | ✅ 더미 3종(Q벽/W밭/S수리) 주입 실측 |
| Ctrl+숫자 부대지정 → 탭 표시(번호+유닛수 0) | ✅ 탭 "1/0" 등장 |
| HUD 멱등(Built 가드) | ✅ 재세션 중복 없음 |
| 빌드/런타임 에러 | ✅ 0건 (LEA-3035 기지 경고 제외) |
| 스킬 호버 툴팁 | ⚠️ 수동 확인 필요(시뮬 호버 불가) — 코드상 ButtonState.Hover 배선 완료 |

## Remaining Issues
1. **[수동 확인] 스킬 툴팁 호버** — 실마우스로 스킬 버튼에 올려 설명 패널 표시 확인 (더미 스킬은 세션 한정이라, 확인하려면 execute_script로 SetSkillSlot 주입 후 테스트).
2. **HUD 장식 프레임(스타 종족 콘솔풍)** — 현재 단색 라인 프레임. 본격 장식 디자인은 #16 테마·아트에서 (로드맵 기록됨).
3. 미니맵 클릭 좌표는 기본 줌 기준 — 줌 변경 시 미세 오차 가능(뷰포트 크기 고정). #3 이후 필요 시 보정.
4. 선택 UI 사양(사용자 확정, #3에서 구현): 부대 최대 144, 8×3=24 표시 + 초과 시 부대 페이지(1/2/3…), 선택 없으면 완전 공백, 초상화=선택 유닛.

# msw-engine

MSW(Maker 26.7) 실측으로 확인한 엔진 동작. 다시 실측하면 30분씩 드니 그대로 쓴다.

## 월드 스프라이트 프롭은 model://MapObject로 스폰한다
- Rule: `_SpawnService:SpawnByModelId("model://MapObject", name, Vector3, parent)` — Transform + SpriteRenderer만 있고 카메라 없음. `SpriteRUID`에 애니메이션 클립 RUID도 그대로 들어간다. `model://sprite/object/empty`는 존재하지 않음. 이전의 `model://defaultplayer` 복제 + CameraComponent 비활성 우회는 폐기.
- Scope: project
- Rationale: 실측 2026-09-14 (증강 디펜스 구역 시각화·데코·달팽이 시연)
- CLAUDE.md application: candidate(코드 관련 — 프롭 스폰 관례로 CLAUDE.md 반영 제안 가능)
- Priority: takes precedence over defaults

## 캐릭터(유닛)는 MSW 아바타 방식 — MapObject에 AvatarRenderer + CostumeManager를 붙인다
- Rule: `model://MapObject` 스폰 → `RemoveComponent("SpriteRendererComponent")` → `AddComponent("AvatarRendererComponent")` + `AddComponent("CostumeManagerComponent")`(서버에서), `UseCustomEquipOnly=true`, `Custom{Longcoat,TwoHandedWeapon,Shoes,Hair,...}Equip`에 아바타 아이템 RUID. 스케일 2.0이 셀(80px)에 맞음. AvatarRenderer `OrderInLayer 200`, `ShowDefaultWeaponEffects=true`면 무기 잔상(모험가 히어로 소드는 불꽃 궤적)이 붙는다. 공격 모션은 클라에서 `AvatarRendererComponent:GetBodyEntity():SendEvent(ActionStateChangedEvent(action, action, playRate, SpriteAnimClipPlayType.Onetime))`, 끝나면 `stand2` Loop로 복귀. **같은 액션을 연달아 보내면 재생되지 않으므로** stand를 거쳐서 다음 공격. 두손검 액션: swingT1/T2/T3(3프레임 0.7초), swingTF(4프레임 0.65초), stabT1/T2/TF.
- Scope: project
- Rationale: 실측 2026-09-14. 스프라이트를 따로 만들 필요 없이 장비 RUID 세트만으로 직업 외형·모션이 나와 사용자가 확정("내가 원한 게 딱 저 정도").
- CLAUDE.md application: candidate(코드 관련 — 유닛 렌더 관례)
- Priority: takes precedence over defaults

## 스프라이트 애니메이션 끝은 SpriteAnimPlayerEndFrameEvent로 잡는다
- Rule: SpriteRenderer에 클립을 넣으면 기본 Loop라 `SpriteAnimPlayerEndEvent`는 **오지 않는다**. 1회 재생 후 제거하려면 `SpriteAnimPlayerEndFrameEvent`(마지막 프레임 진입)를 받고 한 프레임 뒤 Destroy. `StartFrameIndex/EndFrameIndex`로 구간 재생, `PlayRate`로 배속. `PlayRate=0`은 렌더 자체가 안 됨(정지 프레임은 Start=End 같은 값으로). 프레임 길이는 프로브(`SpriteAnimPlayerChangeFrameEvent` + 50ms tick 카운트)로 실측. `wait(0.02)`는 실제로 한 프레임(≈0.034초) 단위로 돈다.
- Scope: project
- Rationale: 실측 2026-09-14 — EndEvent를 기다리다 타임아웃까지 늘어져 사이클이 1.5초가 되고 이펙트가 두 바퀴 돈 원인.
- CLAUDE.md application: candidate(코드 관련)
- Priority: takes precedence over defaults

## 카메라 줌 잠금 상태에선 ZoomTo가 무시된다
- Rule: `CameraComponent.IsAllowZoomInOut=false`이면 `_CameraService:ZoomTo`가 무시됨 → 잠깐 true로 풀고 ZoomTo 후 다시 잠근다(`RtsCameraAnchorComponent.ClaimCamera`). 최대 줌아웃 30%에서 뷰는 42.66×24 유닛, 1유닛 = 45px(1920 기준).
- Scope: project
- Rationale: 실측 2026-09-14
- CLAUDE.md application: candidate(코드 관련)
- Priority: takes precedence over defaults

## 업로드 대형 스프라이트는 PPU 30, 텍스트 넘침은 Truncate
- Rule: 1440px급 업로드 스프라이트는 PPU 30(740px짜리는 100이었음) — 스케일은 스크린샷으로 실측해 맞춘다. `TextComponent.Overflow`의 `ellipsis`는 박스보다 긴 새 글이 오면 이전 글을 그대로 보여주는 버그가 있어 `Truncate` 사용(리치텍스트 태그도 잘리므로 plain text).
- Scope: project
- Rationale: 실측 2026-09-14
- CLAUDE.md application: candidate(코드 관련)
- Priority: takes precedence over defaults

## 공식 자산 검색 절차 (msw-mcp)
- Rule: `asset_search_resources(cat=..., query="*키워드", source="maplestory")` → `asset_get_account_resource_metadata_bulk`(≤50개)의 `mapleImgFullPath`로 정체 확인(아바타 아이템은 `extraInfo.avatarItemInfo.mapleName`에 한글 이름). 미리보기는 `https://mod-thumbnail.dn.nexoncdn.co.kr/<r0-1>/<r2-3>/<ruid>_64.png`(64px만 존재). 메타데이터 결과가 크면 tool-results 파일로 떨어지니 Python으로 파싱. 검색 키 예: 탑뷰 헤네시스 오브젝트 `*topview_henesys`(sprite), 헤네시스 RectTile은 `*henesys` 결과에서 경로로 필터, 몹 사운드 `*<몹ID>`(audioclip → `sound/mob/<id>/die`), 스킬 사운드 `*<스킬ID>`(→ `sound/skill/<id>/use|hit`), 직업 코디 `*모험가 히어로`(avataritem — 한글 이름 검색 됨).
- Scope: project
- Rationale: 실측 2026-09-14
- CLAUDE.md application: not needed(non-code — 자산 탐색 절차)
- Priority: takes precedence over defaults

## number는 tostring하면 "1.0" — 이름·키·표시는 정수로 포맷한다
- Rule: 프로퍼티(`property number`), Sync 값, 클라↔서버 RPC 인자로 온 숫자는 실수 서브타입이라 `tostring(1)`이 `"1.0"`이 된다(리터럴·for 루프 변수·`math.floor` 결과는 `"1"`). 엔티티 이름(`Unit1_2`), 테이블 키(`CellKey`), 화면 표기는 `string.format("%d", math.floor(v + 0.5))` 또는 `_RtsHudLogic:Int(v)`로 만든다. `list[1.0]`은 `list[1]`과 같으니 테이블 인덱스는 괜찮다.
- Scope: project
- Rationale: 실측 2026-09-15 — 클라가 `GetEntityByPath("/maps/RtsMap/Unit1.0_1.0")`을 찾아 슬롯이 비고, `IsPadCell(4.0,3.0)`이 `"4.0,3.0"` 키로 false가 나 이동이 안 됐음.
- CLAUDE.md application: candidate(코드 관련 — 관례로 반영 제안 가능)
- Priority: takes precedence over defaults

## 클라 입력·터치·UI 좌표 실측
- Rule: 월드 클릭은 `@EventSender("Service","InputService") handler HandleScreenTouchEvent` + `_UILogic:ScreenToWorldPosition(event.TouchPoint)`(화면 1920×1080 기준, 좌하 원점), UI 위 클릭은 `_InputService:IsPointerOverUI()`로 거른다. 엔티티 클릭은 `TouchReceiveComponent` + `entity:ConnectEvent(TouchEvent, fn)`인데 **`AutoFitToSize`·`TouchArea`는 동기화되지 않아 클라에서 직접** 설정한다(아바타 스케일 2 = `TouchArea(1.4, 2.2)`, `Offset(0, 1.1)`). 마우스 오버는 `MouseMoveEvent` + `_InputService:GetCursorPosition()`으로 직접 판정, 커서 교체는 `_InputService:SetCursor(ruid, Vector2.zero)` / `ResetCursor()`(메이플 손 커서 `3930c5d2e85b4bff8467aada64fda7f5`). 월드→UI 배치는 `_UILogic:ScreenToUIPosition(_UILogic:WorldToScreenPosition(v))` = 화면 중앙 원점이라 HUD 그룹 자식은 anchor (0.5,0.5)에 그 값을 그대로. 서버가 클라 한 명에게만 보내려면 `@ExecSpace("Client")` 메서드의 **마지막 파라미터 = userId**, 클라가 부른 `@ExecSpace("Server")` 메서드에선 `senderUserId`로 검증. 양쪽 공통 시계는 `_UtilLogic.ServerElapsedSeconds`.
- Scope: project
- Rationale: 실측 2026-09-15 (유닛 팝업·캐릭터 메뉴·위치 이동)
- CLAUDE.md application: candidate(코드 관련)
- Priority: takes precedence over defaults

## 클라 스폰·삭제는 프레임에 나눠 처리된다 / MCP 도구는 유령 클릭을 넣는다
- Rule: 클라 `_SpawnService:SpawnByModelId`·`Destroy`는 호출 즉시 반환되지만 실제 생성·삭제는 여러 프레임(80개 ≈ 1초)에 걸친다 → 같은 이름을 바로 다시 스폰하면 실패하니 이름에 세대 번호를 붙인다. UI 아바타는 `model://uiempty` + `CostumeManagerComponent` + `AvatarGUIRendererComponent`로 그려진다. Maker MCP의 `maker_screenshot`/`maker_execute_script`는 플레이 화면에 **유령 클릭**(ScreenTouchEvent·TouchEvent)을 넣으므로, 클릭에 반응하는 모드(이동 모드 등)를 켜 둔 채 도구를 부르면 엉뚱한 입력이 들어간다 — 테스트할 땐 모드를 끄고 스크린샷을 찍거나 로그로 확인한다. `maker_mouse_input`은 월드 클릭(ScreenTouchEvent·TouchEvent)은 넣지만 UI 버튼은 못 누르고 실제 커서 위치도 안 바꾼다.
- Scope: project
- Rationale: 실측 2026-09-15
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 스크롤 목록 = uisprite + ScrollLayoutGroupComponent (프로퍼티 이름은 ScrollBar*)
- Rule: 스크립트로 스크롤 목록을 만들 땐 `model://uisprite`를 스폰해 `AddComponent("ScrollLayoutGroupComponent")` → `Type = LayoutGroupType.Vertical`, `ChildAlignment`, `Spacing`, `UseScroll`. 자식은 그냥 스폰하면 위에서부터 쌓이고(RectSize 높이 사용) 넘치면 휠 스크롤·핸들이 생긴다. 스크롤바 프로퍼티 이름은 로컬 d.mlua(`Visible`·`Thickness`·`HandleColor`·`BackgroundColor`)와 달리 런타임엔 **`ScrollBarVisible`·`ScrollBarThickness`·`ScrollBarHandleColor`·`ScrollBarBackgroundColor`**(d.mlua 이름으로 쓰면 "cannot set Visible, no such field"). `ScrollBarVisibility.AutoHide`는 내용이 짧아도 핸들이 트랙을 꽉 채운 채 보이고, `Hide`는 흰 트랙 띠가 남는다 → 내용이 다 들어가면 `UseScroll = false`로 끈다. 스크롤 위치는 `SetScrollNormalizedPosition(UITransformAxis.Vertical, v)`. 예: `RtsUnitPopupLogic.SpawnScrollList`.
- Scope: project
- Rationale: 2026-09-16 유닛 팝업 증강·버프 탭 실측(d.mlua 이름 실패 → mlua_api_retriever로 확인)
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

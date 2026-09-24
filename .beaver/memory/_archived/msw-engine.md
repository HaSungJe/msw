# archived — 컨벤션 문서로 이관된 메모리 원문(복구용, 스킬은 읽지 않음)

<!-- 2026-09-24 ship: docs/msw-engine.md 로 이관 -->
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
- Rule: SpriteRenderer에 클립을 넣으면 기본 Loop라 `SpriteAnimPlayerEndEvent`는 **오지 않는다**. 1회 재생 후 제거하려면 `SpriteAnimPlayerEndFrameEvent`(마지막 프레임 진입)를 받고 한 프레임 뒤 Destroy. `StartFrameIndex/EndFrameIndex`로 구간 재생, `PlayRate`로 배속. `PlayRate=0`은 렌더 자체가 안 됨(정지 프레임은 Start=End 같은 값으로). **구간은 SpriteRUID를 넣은 뒤에 줘야 남는다** — RUID 대입이 Start/End를 기본값(0/2147483647)으로 되돌린다(2026-09-20 프로브; 09-18 "카드 클립에 구간이 안 먹음"도 이것). 재생 중 구간을 바꾸면 다음 프레임부터 새 구간, EndFrameEvent는 구간의 마지막 프레임에서(1…12,E12 → Start=End=12로 멈춤 / 13…17,E17 반복 → E17에서 Destroy), ChangeFrameEvent는 1부터 온다. 빙결 결정체(RtsMonsterComponent.SetFrozenFx)가 이 방식(2026-09-20 실측). 프레임 길이는 프로브(`SpriteAnimPlayerChangeFrameEvent` + 50ms tick 카운트)로 실측. `wait(0.02)`는 실제로 한 프레임(≈0.034초) 단위로 돈다.
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

## number는 tostring하면 "1.0" — 이름·키·표시는 정수로 포맷한다
- Rule: 프로퍼티(`property number`), Sync 값, 클라↔서버 RPC 인자로 온 숫자는 실수 서브타입이라 `tostring(1)`이 `"1.0"`이 된다(리터럴·for 루프 변수·`math.floor` 결과는 `"1"`). 엔티티 이름(`Unit1_2`), 테이블 키(`CellKey`), 화면 표기는 `string.format("%d", math.floor(v + 0.5))` 또는 `_RtsHudLogic:Int(v)`로 만든다. `list[1.0]`은 `list[1]`과 같으니 테이블 인덱스는 괜찮다.
- Scope: project
- Rationale: 실측 2026-09-15 — 클라가 `GetEntityByPath("/maps/RtsMap/Unit1.0_1.0")`을 찾아 슬롯이 비고, `IsPadCell(4.0,3.0)`이 `"4.0,3.0"` 키로 false가 나 이동이 안 됐음.
- CLAUDE.md application: candidate(코드 관련 — 관례로 반영 제안 가능)
- Priority: takes precedence over defaults

## 클라 입력·터치·UI 좌표 실측
- Rule: 월드 클릭은 `@EventSender("Service","InputService") handler HandleScreenTouchEvent` + `_UILogic:ScreenToWorldPosition(event.TouchPoint)`(화면 1920×1080 기준, 좌하 원점), UI 위 클릭은 `_InputService:IsPointerOverUI()`로 거른다. 엔티티 클릭에 `TouchReceiveComponent` + `TouchEvent`는 **쓰지 않는다** — 2026-09-22 실측: 유닛 엔티티(서버 AddComponent + 클라 TouchArea 지정)에 클릭 지점이 판정 상자 안인데도 TouchEvent가 오지 않았고 클라에서 넣은 TouchArea도 반영되지 않았다(서버 자동값 0.5×0.8만 남음). 월드 엔티티 클릭은 전부 `ScreenTouchEvent` + 자체 상자 판정(`RtsUnitSelectLogic.UnitAtScreen` 폭 1.4·높이 2.2 발 기준, `CellAtScreen`)으로 한다. 마우스 오버는 `MouseMoveEvent` + `_InputService:GetCursorPosition()`으로 직접 판정, 커서 교체는 `_InputService:SetCursor(ruid, Vector2.zero)` / `ResetCursor()`(메이플 손 커서 `3930c5d2e85b4bff8467aada64fda7f5`). 월드→UI 배치는 `_UILogic:ScreenToUIPosition(_UILogic:WorldToScreenPosition(v))` = 화면 중앙 원점이라 HUD 그룹 자식은 anchor (0.5,0.5)에 그 값을 그대로. 서버가 클라 한 명에게만 보내려면 `@ExecSpace("Client")` 메서드의 **마지막 파라미터 = userId**, 클라가 부른 `@ExecSpace("Server")` 메서드에선 `senderUserId`로 검증. 양쪽 공통 시계는 `_UtilLogic.ServerElapsedSeconds`.
- Scope: project
- Rationale: 실측 2026-09-15 (유닛 팝업·캐릭터 메뉴·위치 이동)
- CLAUDE.md application: candidate(코드 관련)
- Priority: takes precedence over defaults

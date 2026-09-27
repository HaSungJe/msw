# MSW 엔진 관례 (실측)

Maker 26.7에서 실측으로 확인한 엔진 동작과 그에 따른 작성 관례. 다시 실측하면 30분씩 드니 그대로 따른다.
(2026-09-24 `.beaver/memory/msw-engine.md`에서 이관 — 원문 보관: `.beaver/memory/_archived/msw-engine.md`)

## 월드 스프라이트 프롭은 model://MapObject로 스폰한다
- `_SpawnService:SpawnByModelId("model://MapObject", name, Vector3, parent)` — Transform + SpriteRenderer만 있고 카메라 없음. `SpriteRUID`에 애니메이션 클립 RUID도 그대로 들어간다. `model://sprite/object/empty`는 존재하지 않음. 이전의 `model://defaultplayer` 복제 + CameraComponent 비활성 우회는 폐기.
- 근거: 실측 2026-09-14 (증강 디펜스 구역 시각화·데코·달팽이 시연)

## 캐릭터(유닛)는 MSW 아바타 방식 — MapObject에 AvatarRenderer + CostumeManager를 붙인다
- 썬콜(`il`)은 2026-09-25 사용자 요청으로 예외: 두 아바타 컴포넌트를 생성하지 않고 클라이언트 자식 `MageSkin` 스프라이트로 확정 대기 자세와 체인 라이트닝·블리자드 각 3프레임을 표시한다. RUID와 발 기준점은 `docs/design/ice-lightning-mage-motion.md` 참조.
- `model://MapObject` 스폰 → `RemoveComponent("SpriteRendererComponent")` → `AddComponent("AvatarRendererComponent")` + `AddComponent("CostumeManagerComponent")`(서버에서), `UseCustomEquipOnly=true`, `Custom{Longcoat,TwoHandedWeapon,Shoes,Hair,...}Equip`에 아바타 아이템 RUID. 스케일 2.0이 셀(80px)에 맞음. AvatarRenderer `OrderInLayer 200`, `ShowDefaultWeaponEffects=true`면 무기 잔상(모험가 히어로 소드는 불꽃 궤적)이 붙는다. 공격 모션은 클라에서 `AvatarRendererComponent:GetBodyEntity():SendEvent(ActionStateChangedEvent(action, action, playRate, SpriteAnimClipPlayType.Onetime))`, 끝나면 `stand2` Loop로 복귀. **같은 액션을 연달아 보내면 재생되지 않으므로** stand를 거쳐서 다음 공격. 두손검 액션: swingT1/T2/T3(3프레임 0.7초), swingTF(4프레임 0.65초), stabT1/T2/TF.
- 근거: 실측 2026-09-14. 스프라이트를 따로 만들 필요 없이 장비 RUID 세트만으로 직업 외형·모션이 나와 사용자가 확정("내가 원한 게 딱 저 정도").

## 스프라이트 애니메이션 끝은 SpriteAnimPlayerEndFrameEvent로 잡는다
- SpriteRenderer에 클립을 넣으면 기본 Loop라 `SpriteAnimPlayerEndEvent`는 **오지 않는다**. 1회 재생 후 제거하려면 `SpriteAnimPlayerEndFrameEvent`(마지막 프레임 진입)를 받고 한 프레임 뒤 Destroy. `StartFrameIndex/EndFrameIndex`로 구간 재생, `PlayRate`로 배속. `PlayRate=0`은 렌더 자체가 안 됨(정지 프레임은 Start=End 같은 값으로). **구간은 SpriteRUID를 넣은 뒤에 줘야 남는다** — RUID 대입이 Start/End를 기본값(0/2147483647)으로 되돌린다(2026-09-20 프로브; 09-18 "카드 클립에 구간이 안 먹음"도 이것). 재생 중 구간을 바꾸면 다음 프레임부터 새 구간, EndFrameEvent는 구간의 마지막 프레임에서(1…12,E12 → Start=End=12로 멈춤 / 13…17,E17 반복 → E17에서 Destroy), ChangeFrameEvent는 1부터 온다. 빙결 결정체(RtsMonsterComponent.SetFrozenFx)가 이 방식(2026-09-20 실측). 프레임 길이는 프로브(`SpriteAnimPlayerChangeFrameEvent` + 50ms tick 카운트)로 실측. `wait(0.02)`는 실제로 한 프레임(≈0.034초) 단위로 돈다.
- 근거: 실측 2026-09-14 — EndEvent를 기다리다 타임아웃까지 늘어져 사이클이 1.5초가 되고 이펙트가 두 바퀴 돈 원인.

## 카메라 줌 잠금 상태에선 ZoomTo가 무시된다
- `CameraComponent.IsAllowZoomInOut=false`이면 `_CameraService:ZoomTo`가 무시됨 → 잠깐 true로 풀고 ZoomTo 후 다시 잠근다(`RtsCameraAnchorComponent.ClaimCamera`). 최대 줌아웃 30%에서 뷰는 42.66×24 유닛, 1유닛 = 45px(1920 기준).
- 근거: 실측 2026-09-14

## PC·모바일 보드 표시와 서버 전투 좌표 분리
- `RtsMap` 맵 엔티티에는 TransformComponent가 없으므로 맵 자체를 축소하지 않는다. `RtsBoardViewLogic.GetRoot()`가 맵 자식 `RtsBoard`(MapObject의 SpriteRenderer 제거)를 서버에서 생성한다. 트랙·유닛·몬스터·월드 연출의 공통 부모다. 네이티브 RectTileMap과 카메라용 플레이어는 기존 맵에 남는다.
- Maker 실측: 부모 Position=(10,20), Scale=.5일 때 SpawnByModelId의 위치(4,6)는 자식 **로컬 좌표**이고 월드 위치는(12,23)이다. 서버가 만든 컨테이너의 Scale을 클라이언트에서 .5로 바꾸면 서버 자식은(4,6), 클라이언트 자식만(2,3)이 된다.
- 서버 보드는 identity이고 PC·모바일 모두 클라이언트 Transform을 변경한다. 서버 전투 좌표는 보드의 자식 로컬 좌표와 같다. 클라이언트 연출은 `BoardPosition`으로 읽고 `Position`에 쓴다. 화면 클릭은 `ScreenToBoard`, 메뉴 투영은 `BoardToScreen`을 사용한다. `WorldPosition`을 읽어 보드 자식 Position으로 그대로 넣으면 이중 변환되므로 금지한다.
- 카메라 최소 줌30을 낮추는 방식으로 해결하지 않는다. 각 플랫폼의 HUD 영역을 뺀 실제 화면에 보드가 들어오도록 표시 배율을 계산한다. 테마 배경은 별도로 화면을 채운다. Maker Preview는 런타임 `_T.Preview`만 사용하며 일반 PC/실서비스에서는 켜지지 않는다.
- 근거: Maker 서버·클라 좌표 비교, 208칸 클릭 좌표 왕복, 6캐릭터 선택, 투사체·타격·피해 적용 검증(2026-09-27). 실제 모바일 손가락 입력은 별도 검증 대상.

## 업로드 대형 스프라이트는 PPU 30, 텍스트 넘침은 Truncate
- 1440px급 업로드 스프라이트는 PPU 30(740px짜리는 100이었음) — 스케일은 스크린샷으로 실측해 맞춘다. `TextComponent.Overflow`의 `ellipsis`는 박스보다 긴 새 글이 오면 이전 글을 그대로 보여주는 버그가 있어 `Truncate` 사용(리치텍스트 태그도 잘리므로 plain text).
- 근거: 실측 2026-09-14

## number는 tostring하면 "1.0" — 이름·키·표시는 정수로 포맷한다
- 프로퍼티(`property number`), Sync 값, 클라↔서버 RPC 인자로 온 숫자는 실수 서브타입이라 `tostring(1)`이 `"1.0"`이 된다(리터럴·for 루프 변수·`math.floor` 결과는 `"1"`). 엔티티 이름(`Unit1_2`), 테이블 키(`CellKey`), 화면 표기는 `string.format("%d", math.floor(v + 0.5))` 또는 `_RtsHudLogic:Int(v)`로 만든다. `list[1.0]`은 `list[1]`과 같으니 테이블 인덱스는 괜찮다.
- 근거: 실측 2026-09-15 — 클라가 `GetEntityByPath("/maps/RtsMap/Unit1.0_1.0")`을 찾아 슬롯이 비고, `IsPadCell(4.0,3.0)`이 `"4.0,3.0"` 키로 false가 나 이동이 안 됐음.

## 클라 입력·터치·UI 좌표 실측
- 월드 클릭은 `@EventSender("Service","InputService") handler HandleScreenTouchEvent` + `_UILogic:ScreenToWorldPosition(event.TouchPoint)`(화면 1920×1080 기준, 좌하 원점), UI 위 클릭은 `_InputService:IsPointerOverUI()`로 거른다. 엔티티 클릭에 `TouchReceiveComponent` + `TouchEvent`는 **쓰지 않는다** — 2026-09-22 실측: 유닛 엔티티(서버 AddComponent + 클라 TouchArea 지정)에 클릭 지점이 판정 상자 안인데도 TouchEvent가 오지 않았고 클라에서 넣은 TouchArea도 반영되지 않았다(서버 자동값 0.5×0.8만 남음). 월드 엔티티 클릭은 전부 `ScreenTouchEvent` + 자체 상자 판정(`RtsUnitSelectLogic.UnitAtScreen` 폭 1.4·높이 2.2 발 기준, `CellAtScreen`)으로 한다. 마우스 오버는 `MouseMoveEvent` + `_InputService:GetCursorPosition()`으로 직접 판정, 커서 교체는 `_InputService:SetCursor(ruid, Vector2.zero)` / `ResetCursor()`(메이플 손 커서 `3930c5d2e85b4bff8467aada64fda7f5`). 월드→UI 배치는 `_UILogic:ScreenToUIPosition(_UILogic:WorldToScreenPosition(v))` = 화면 중앙 원점이라 HUD 그룹 자식은 anchor (0.5,0.5)에 그 값을 그대로. 서버가 클라 한 명에게만 보내려면 `@ExecSpace("Client")` 메서드의 **마지막 파라미터 = userId**, 클라가 부른 `@ExecSpace("Server")` 메서드에선 `senderUserId`로 검증. 양쪽 공통 시계는 `_UtilLogic.ServerElapsedSeconds`.
- 근거: 실측 2026-09-15 (유닛 팝업·캐릭터 메뉴·위치 이동)

## 스크립트로 만든 UI 그룹(model://uigroup)은 화면 전체로 늘려야 한다
- `_SpawnService:SpawnByModelId("model://uigroup", …, /ui)`로 만든 그룹은 크기·앵커를 주지 않으면 **실제 클라이언트에서 작은 기본 크기로 화면 가운데에** 생긴다 → 그 안에서 모서리 anchor로 붙인 요소가 전부 화면 가운데로 몰린다. **Maker Play에서는 화면 크기로 잡혀 드러나지 않는다.** 만든 직후 `UITransformComponent`를 AnchorsMin (0,0) · AnchorsMax (1,1) · Pivot (0.5,0.5) · OffsetMin/OffsetMax (0,0)으로 늘린다(`RtsHudLogic.StretchFull`).
- 근거: 2026-09-24 v260924-1 출시 클라이언트 스크린샷 — HUD 전체(정보 카드·순위/도감/뽑기/증강 버튼·유닛 슬롯·플레이어 목록)가 화면 가운데 약 100px 사각형에 겹쳐 그려짐.

## 게임 시계는 RtsStageLogic.GameNow() — 일시정지 시간이 빠지고 배속만큼 빨라진다
- 2026-09-25 솔로 일시정지(사용자 "솔로 플레이 한정 일시정지")부터 **판정용 시각은 전부 `_RtsStageLogic:GameNow()`로 적고 비교한다** — 스테이지 끝(`StageEndsAt`)·조기 종료, 스킬 쿨(`ReadyAt`)·후딜(`BusyUntil`)·방향 고정, 빙결·방어율 감소·받는 데미지 증가·중독 끝, 위치 이동·결속 쿨. `GameNow = ClockBase + (ServerElapsedSeconds − ClockSince) × ClockRate`(흐름 속도 — 멈춤 0 · 진행 중 `GameSpeed` 1/2 · 카운트다운·종료 1), 서버·클라 공용(동기화 값). 흐름 속도가 바뀌기 직전(일시정지·배속·판 상태 `SetRunState`)마다 `RebaseClock`으로 기준을 다시 잡는다(2026-09-27 배속 — 전: ServerElapsedSeconds − PausedTotal).
- `_UtilLogic.ServerElapsedSeconds`를 그대로 쓰는 건 **실제 시간이 맞는 것만**: 다시 하기 투표 시간 제한(`VoteStartedAt`), 0.5초 계산 캐시(`ArmorCache`·`GuardCache`). 연출·소리 간격은 `ElapsedSeconds` 그대로.
- 판정이 나는 지연 실행(연타 타격·구체·지속 피해 틱·보스 2차 소환·몬스터 사망 뒤 제거)은 `_TimerService:SetTimerOnce` 대신 **`_RtsStageLogic:After(fn, sec)`**(같은 인자 순서) — 게임 시각 기준(2배속이면 실제 절반), 멈춘 동안 만료되면 풀릴 때까지 0.1초씩 미룬다. 반복 루프(라운드 틱·유닛 공격 루프·소환 틱·트랙 걷기 OnUpdate)는 `_RtsStageLogic.Paused`면 그 회차를 건너뛴다.
- **배속(2026-09-27)**: 실제 시계로 도는 서버 타이머는 `_RtsStageLogic:RealSpeed()`(진행 중 2배면 2)로 나누거나 곱한다 — 유닛 공격 루프 주기(`RtsCombatLogic.StartLoop`, 바뀌면 `RescaleLoops`) · 몬스터 생성 간격(`RtsWaveLogic.RescaleSpawn`) · 트랙 걷기(`delta × RealSpeed`). 클라는 `_UtilLogic:SetClientTimeScale(GameSpeed)`(진행 중·안 멈췄을 때 — `RtsStageLogic.RefreshHud`)로 연출·데미지 숫자·클라 타이머·애니메이션을 같이 빠르게 한다(엔진 문서: `ElapsedSeconds`·소리·서버는 영향 없음). 새 서버 반복 타이머를 만들면 `RealSpeed`를 반영하고 `ApplySpeed`에 다시 걸기를 추가한다.
- 멈춘 동안 게임 조작 RPC(영입·방출·레벨업·결속·스킬 잠금·위치 이동·증강 선택/지정/뽑기)는 서버 첫 줄에서 `if _RtsStageLogic.Paused then return end`. 몬스터 걷기 모션은 `RtsWaveLogic.SetMotionPaused`(본체 스프라이트 `PlayRate` 0/1).
- 새 판정 시각·지연 판정을 추가할 때도 이 규칙을 따른다(서버 시계와 섞으면 한 번 멈춘 뒤부터 어긋난다).


- UI 엔티티 `AttachTo`는 화면 위치를 보존하며 anchoredPosition을 바꿀 수 있다. 새 컨테이너 안의 상대 배치를 유지하려면 재부모화 전 위치를 저장하고 이후 복원한다(`RtsUiLayoutLogic.UnitInfo`, Maker 실측).

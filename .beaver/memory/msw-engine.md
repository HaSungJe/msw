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

## 월드 TouchEvent는 UI 버튼과 같이 발화한다 — UI 우선은 코드로 사각형 판정
- Rule: 유닛(TouchReceiveComponent)의 `TouchEvent`는 그 위에 UI(uigroup 패널·버튼)가 있어도 함께 발화한다(2026-09-17 실측: 나이트로드 컨텍스트 메뉴의 '상세정보' 자리에 선 섀도어가 클릭돼 메뉴가 바뀜). 팝업이 열려 있을 땐 `_RtsPopupLogic:IsOpen()`으로 무시하고, 작은 메뉴는 `RtsUnitSelectLogic.MenuRect`(UI 중앙 원점 좌표, 여백 6px)에 `event.TouchPoint`를 `_UILogic:ScreenToUIPosition`으로 바꿔 넣어 `IsOverMenu`면 유닛 클릭을 버린다(`RtsUnitComponent.OnTouched(screen)`). 새 월드 클릭 대상이 생기면 같은 판정을 붙일 것.
- Scope: project
- Rationale: User bug report 2026-09-17 "상세보기가 클릭이 아니라 섀도어 클릭이 우선시됨. 팝업이 항상 클릭 우선이어야"
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 전투 = 엔진 AttackComponent/HitComponent + 데미지 스킨 파이프라인 위에 얹는다
- Rule: 유닛에 `RtsUnitAttackComponent extends AttackComponent`(CalcDamage/CalcCritical/GetCriticalDamageRate/GetDisplayHitCount/IsAttackTarget을 같은 시그니처로 정의 = override, 값은 프로퍼티 Dmg/Crit/CritRate/Hits/TargetName으로 공격 직전 주입) + `DamageSkinSettingComponent`; 몬스터에 `HitComponent`(BoxSize·ColliderOffset, 기본 CollisionGroups.HitBox) + `DamageSkinSpawnerComponent` + `RtsMonsterComponent`(서버 HitEvent로 HP). 판정은 `atk:AttackFrom(Vector2 size, Vector2 worldPos, attackInfo, CollisionGroups.HitBox)` — 대상은 IsAttackTarget에서 이름으로 고른다(박스로 고르지 않음). 데미지 숫자는 엔진이 알아서 그림(크리는 CalcCritical true면 GetCriticalDamageRate 배). 새 스크립트의 .codeblock은 기존 것을 복제해 EntryKey/Id 새 GUID, Name, Type(Logic 5 / Component 1)만 바꾸면 Maker가 인식. 1회 재생 클립 이펙트 = SpriteRUID에 클립 + `SpriteAnimPlayerEndFrameEvent` 뒤 Destroy(`RtsSkillFxLogic.PlayClip`). 원작 스킬 클립은 왼쪽 보기 → `assetFacesLeft`로 유닛 방향에 맞춰 `FlipX`. **아바타 좌우: 메이플 아바타 기본은 왼쪽 보기(스케일 양수 = 왼쪽)**. 반전은 클라에서 `AvatarRendererComponent:GetAvatarRootEntity().TransformComponent.Scale.x = -1`(유닛 엔티티 스케일을 뒤집으면 자식 버프 아이콘까지 뒤집힌다). 서버는 `RtsUnitComponent.FaceDir`(@Sync, -1 왼쪽/+1 오른쪽)만 정하고 클라 `OnSyncProperty("FaceDir")` → `ApplyFace`. 이펙트 반전은 `RtsSkillFxLogic.FlipFor(fx, facingRight, which)`(assetFacesLeft를 기본으로, `clip/frames/body/loop/projFacesLeft`가 요소별 우선 / noFlip). 투사체는 `PlayProjectile`이 `_TweenLogic:MoveTo`로 직선 비행 + `ZRotation`을 비행 각도로(오른쪽: 반전+각도, 왼쪽: 무반전+각도−180). 2026-09-18 전까지 반대로(스케일 양수 = 오른쪽 가정) 돼 있어 팔라딘이 등 뒤로 이펙트를 쏨 — 사용자 지적으로 수정. 마지막 공격 방향 유지(되돌리지 않음). 시험대는 `RtsCombatLogic.TestBench`(입장 시 순회 정지 `RtsDemoLogic.StopWalkers` + 허수아비 `RtsDummy<zone>` (14,3) 체력 무제한 + 유닛 1을 (13,3)에 놓고 공격 반복) — 웨이브(#10)가 생기면 false.
- Scope: project
- Rationale: 실측 2026-09-17 — 히어로 레이징 블로우 시험대에서 데미지 86×2 표시·타격 클립·번쩍임·좌우 반전 확인
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 데미지 스킨 리소스 = 숫자 글리프 아틀라스. **(유닛) 스킨은 만/억 글리프를 갖고 엔진이 자동 포맷한다**
- Rule: 데미지 스킨은 `resourceType damageskin`, 경로 `maplestory/effect/damageskin/<원작 id>`. 확인된 것: 0 = 기본 `3271c3e79bf04ecba9a107d55495970d` / 1 = MSW 컴포넌트 기본값 `6ba67548…`(픽셀 숫자) / 3 `1e08a7b6…` / 10001 `02c22d93…`(보라) / **208 = 기본 데미지 스킨 (유닛) `7e39645af9454fffb17a5451e9194dda`** — 기본 스킨 숫자 + 만·억 글리프(일반·크리 색), `DamageSkinSettingComponent.DamageSkinId = DataRef(...)`만 바꾸면 엔진이 10000000 → `1000만`, 123456789 → `1억2345만6789`로 찍어 준다(2026-09-18 실전 AttackFrom 경로로 확인) / 322 `bfd6e8bb…` 고딕 유닛 스킨. **현재 게임 = 208**(`RtsCombatLogic.DamageSkinId`, 스케일 2.0, Blade).
- 찾는 법: `asset_search_resources`는 damageskin 카테고리를 못 받고, Maker 리소스 피커도 아이콘+RUID만 보여 준다(설명 없음). 대신 **피커에서 눌러 본 스킨은 `%LocalLow%/nexon/MapleStory Worlds/resource_cache/msw/<xx>-damageskin/`에 캐시**로 떨어지므로 그 RUID를 `asset_get_account_resource_metadata_bulk`로 정체 확인 → `.dxt.mod`(protobuf: 서브 스프라이트 GUID 목록(.NET 혼합 엔디안, `effect/damageskin/<id>/nored0/0` 같은 개별 sprite) + DDS DXT5 아틀라스, 오프셋 = "DXT5" 위치 − 84, 세로 반전)를 Python으로 디코드하면 만/억 글리프 유무가 바로 보인다. 아이템 아이콘(`item/consume/0243/<id>/info/iconraw`, 예: 02438872 = 기본 데미지 스킨 (유닛) 아이콘 `c2d12933…`)은 스킨 데이터가 아니다. 스킨 id는 32자 RUID만(원작 "000000" 로드 실패). 클라 미리보기: `_DamageSkinService:PreloadAsync(id, cb)` 뒤 `Play(entity, id, delay, {dmg…}, tween, {crit…}, offset, scale)`.
- Rationale: 사용자 2026-09-18 "10000000이 1000만으로 뜨는 기본 데미지 스킨(유닛) 있을 것" → 처음엔 캐시 4개만 보고 "없다"고 했다가 틀림. 사용자가 피커에서 눌러 본 208번이 캐시에 남아 확인. **API로 못 세는 리소스는 "확인한 범위에선 없음"으로만 말할 것.**
- Rule: `maker_execute_script`의 서버 실행 인자는 `context = "server_main"`(`execSpace`가 아님 — 잘못 주면 조용히 클라에서 돈다). Maker UI 자동화(마우스 이동·클릭)는 사용자 데스크톱을 가로채므로 하지 않는다 — 2026-09-18 사용자 게임 창 위에 클릭이 들어간 사고. 읽기 전용 화면 캡처(`System.Drawing.CopyFromScreen`)는 무해.

## CostumeManager 커스텀 슬롯은 비우지 않으면 남는다
- Rule: 유닛 외형을 세트(Skin 0) → 월드 아바타(Skin 1, `UseCustomEquipOnly=false` + `DefaultEquipUserId`)로 바꿀 때 `CustomLongcoat/Shoes/Hair`뿐 아니라 **`CustomCapEquip`·`CustomFaceAccessoryEquip`·`CustomFaceEquip`도 ""로** 비워야 유저 본인 모자·얼굴이 나온다(2026-09-18 보우마스터 깃털 모자가 남아 있던 버그). 무기만 직업 것으로 유지. 캐시 무기(01703xxx·cashweapon49 등)는 afterImage가 검/폭발이라 공격 연출과 겹침 → 진짜 무기로: DK 타임리스 알슈피스 `164067c8…`, 보우마스터 타임리스 엔가우 `9e8fe977…`(afterImage bow).

## 원작 클립 프레임은 (ox 왼쪽에서, oy **아래**에서) px 원점을 엔티티 위치에 맞춰 그린다 — 원점·프레임 시간은 .win.mod에서 읽을 수 있다
- Rule: MSW SpriteRenderer는 메이플 클립의 각 프레임을 **원점 기준**으로 놓는다(중앙 정렬이 아님). 스프라이트 캐시 `<xx>-sprite/<yy>/<guid>.win.mod` 헤더 = `14 0a 10 <guid> 10 01 <len> 08 <w> 10 <h> 1a <len> 08 <ox> 10 <oy>`(varint, 음수는 10바이트) — oy는 **바닥에서** 위로 px. oy ≈ 0~20 = 땅에 서는 그림(아이스 스트라이크 기둥 11, 썬더볼트 hit 19 = 타격점), 큰 양수 = 몸 중심(2221012 결정 123), 음수 = 원점 위에 떠 있음(블리자드 tile −118 → 링이 2유닛 위). ox가 폭의 79%면 그림이 원점 왼쪽으로 뻗는다(2221012 결정 → assetFacesLeft + feetDx 0.9로 정중앙). 프레임마다 크기가 달라도 원점 기준이라 튀지 않는다. 클립 `<xx>-animationclip/<yy>/<ruid>.win.mod`의 프레임 메시지(`0a <len>`)에서 field 2 f32 = 그 프레임 시간(초) — 합이 클립 길이(예: 아이스 스트라이크 0.66, 제네시스 tile 1.9~3.1 + 빈 꼬리 프레임 0.7~2.1초). 타격 타이밍(hitDelay)·표식 수명은 이걸로 계산. 마지막 빈 꼬리 프레임이 길면 `SpriteAnimPlayerEndFrameEvent`가 그 프레임 시작에 와서 일찍 지워진다(원하면 markLife로).
- 정렬: 아바타 Body/Face 스프라이트는 **"Default" 레이어 order 0**(SpawnUnit의 `ar.OrderInLayer = 200`은 클라에서 0으로 읽힘) → 캐릭터 뒤 이펙트는 같은 레이어 order 음수(`PlayBack` −10), 위는 250(몸 덧그림)·300(이펙트)·330(표식). 몬스터는 MapLayer0 200이라 Default 이펙트가 항상 위.
- 실측 방법(2026-09-18): 프레임 sprite GUID를 `SpriteRUID`로 스폰하고 옆에 표식(스나이핑 조준 0c76a3bd… 0.35배)을 같은 자리에 놓아 스크린샷 — 원점 위치가 바로 보인다. 연출 확인은 **슬로모 미리보기**: 시험대 루프를 `StopLoop`으로 멈추고 클라에서 `PlayCast(unit, no, fxCopy, target, targets)`(fx 복사본에 clipLife·markLife 60, sound nil) 직후 `mapRoot:GetChildComponentsByTypeName("SpriteRendererComponent")` 중 이름 `RtsFx*/RtsMark*/RtsBeam*`의 `PlayRate = 0.05` → 1초 연출이 20초로 늘어나 스크린샷(도구 지연 1~2초)으로 잡힌다. 몬스터 타격 클립(`RtsHitFx_*`)은 1초 뒤 지워지는 타이머가 있어 슬로모가 안 먹음.
- Scope: project
- Rationale: 2026-09-18 블리자드 tile이 위로 떠 보이고, 2221012 결정이 캐릭터 등 뒤에 그려진 원인 = 원점. 스크린샷 도구 지연으로 1초 연출을 못 잡아 헤맴 → 슬로모로 해결
- CLAUDE.md application: not needed(non-code 절차)
- Priority: takes precedence over defaults

## 흰 사각 스프라이트 바(체력바)는 Scale로 늘린다 — TiledSize는 안 먹고, 자식은 부모 스케일을 나눠야 세계 크기가 고정된다
- Rule: `RtsHudLogic.WhiteRUID`(47b5e516…)를 `SpriteRendererComponent.SpriteRUID`로 쓰면 ≈0.08유닛(스케일 10 → 0.8유닛 실측) 사각. `DrawMode = Tiled` + `TiledSize`는 이 스프라이트에 효과 없음(점만 그려짐) → `TransformComponent.Scale = (W/0.08, H/0.08)`. 몬스터 자식 엔티티(`SpawnByModelId(..., parent)`, 로컬 Position/Scale)로 붙이면 따라다니지만 부모 스케일(2.5)이 곱해지므로 로컬 = 세계 값 ÷ 부모 스케일 → 몬스터 크기가 달라도 같은 폭(사용자 "체력바 크기 통일, 보스만 길게"). 채움은 중심 기준이라 왼쪽 정렬 = Position.x −(W−w)/2. 상태 아이콘(빙결)은 HitComponent 박스 우측 위(ColliderOffset + BoxSize/2 + 여유)에 자식으로, 스킬 아이콘 sprite(32px → 로컬 0.8 × 부모 2.5 ≈ 0.64유닛)를 쓰면 딱 보인다. 색 틴트는 `sr.Color`(빙결 0.55/0.8/1) — 피격 번쩍임이 되돌릴 색은 `RestColor()`로 상태에 따라.
- Scope: project
- Rationale: 실측 2026-09-18 몬스터 체력바·빙결 표시 구현
- CLAUDE.md application: not needed
- Priority: takes precedence over defaults

## 아바타 ActionStateChangedEvent — 같은 프레임에 두 번 보내면 뒤 액션이 늦거나 무시된다 / PlayRate로 슬로모 캡처
- Rule: **같은 액션은 끝난 뒤 다시 보내도 재생되지 않는다**(팔라딘 실측 2026-09-19 — Onetime이 끝나면 화면은 이전 Loop 자세(stand2)로 돌아가지만 상태는 그 액션). 사이에 stand를 보내야 하며 stand→액션 간격 0.05초는 무시, 0.15~0.2초는 재생. 같은 프레임에 두 이벤트를 보내면 뒤 것이 늦거나 무시. 그래서 `RtsSkillFxLogic.PlayMotion`은 (1) 다른 액션이면 바로 보내고, (2) 같은 액션이면 stand → 0.15초 뒤, (3) 액션이 끝나는 시각(0.45초 ÷ motionRate)에 `ReturnStand`로 stand를 보내 `LastMotion`을 stand로 만들어 다음 공격이 지연 0으로 재생되게 한다. `ActionStateChangedEvent` 세 번째 인자 = 재생 속도(`fx.motionRate`): 0.56이면 0.44초 swing이 0.78초 — 클립 길이에 모션을 맞추는 수단. 세 번째 인자 playRate 0.1로 액션을 느리게 재생하면 스크린샷 1장으로 자세를 잡을 수 있다(모션 캡처 절차).
- Scope: project
- Rationale: 사용자 2026-09-19 "스킬 애니메이션이 먼저 나오고 캐릭터가 늦게 따라가서 싱크가 안 맞고 팔이 여러 개처럼 겹쳐 보임" — 원인이 stand+액션 동시 전송과 클립 종료 시 stand 강제 복귀(0.78초, 2타 stabT1은 0.95초까지)였음.
- Priority: takes precedence over defaults

## 이펙트에 무기가 그려진 스킬은 시전 중 캐릭터 무기를 숨긴다 (hideWeapon)
- Rule: 원작 스킬 이펙트 중엔 검·창 같은 무기 그림이 이펙트 안에 들어 있는 것이 있다(레이징 블로우 1121008/effect — 금색 대검). 이런 스킬은 캐릭터의 실제 무기가 옆에 따로 튀어나와 어색하므로 fx에 `hideWeapon = true`(+ `hideWeaponSec`, 없으면 clipLife → 0.9)를 주면 `RtsSkillFxLogic.HideWeapon`이 `AvatarRendererComponent:SetAvatarPartColor(MapleAvatarItemCategory.TwoHandedWeapon/OneHandedWeapon, 1,1,1, 0)`로 무기 파츠를 투명하게 하고 `ShowDefaultWeaponEffects = false`로 무기 잔상(노란 궤적)도 끈다. 한손/두손 구분은 `GetCostume(jobId).weapon1h`. 연속 공격 중엔 복구 타이머를 매 시전마다 미뤄 깜빡이지 않고, 공격이 끊긴 뒤 hideWeaponSec 지나면 alpha 1·잔상 on으로 복구(`HideTimer[unit.Id]`).
- Scope: project
- Rationale: User 2026-09-19 — "캐릭터의 기본 칼이 저 레이징 블로우 애니메이션에 가려지는 게 맞는 것 같아" → 적용 후 "지금 딱 좋아. 스킬 애니메이션 발동 시 무기 가림 처리 필요한 것도 나중에 있을 수 있겠네, 메모리에 적어놔". 새 스킬 이펙트를 등록할 때 클립 썸네일에 무기 그림이 있으면 hideWeapon 후보로 검토.
- Priority: takes precedence over defaults

## 파티 버프는 서버 전투에도 적용해야 한다 — GetBuffsFor를 ClientOnly로 두면 실전 크리 0%
- Rule: RtsUnitBuffLogic.GetBuffsFor/ApplyToStat은 서버(RtsCombatLogic.DoAttack)와 클라(팝업) 양쪽에서 부른다. 유닛 조회는 ClientOnly인 RtsUnitLogic.GetZoneUnit 대신 RtsUnitBuffLogic.UnitAt(엔티티 경로 조회, ExecSpace 없음). DoAttack은 `GetStat → ApplyToStat(buffs) → CalcStat` 순으로 버프 반영 st를 쓴다(Calc()는 기본값만).
- Scope: project
- Rationale: 2026-09-19 사용자 "DK 샤프아이즈로 크확 20%인데 크리가 안 뜬다" — 팝업은 버프 반영값(20%)을 보여줬지만 서버 DoAttack은 Calc(기본값, 크리 0%)로 굴려 크리가 한 번도 안 났다. 수정 후 벤치에서 분홍 크리 스킨(1705 vs 836) 확인.
- Priority: takes precedence over defaults

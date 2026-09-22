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
- Rule: 월드 클릭은 `@EventSender("Service","InputService") handler HandleScreenTouchEvent` + `_UILogic:ScreenToWorldPosition(event.TouchPoint)`(화면 1920×1080 기준, 좌하 원점), UI 위 클릭은 `_InputService:IsPointerOverUI()`로 거른다. 엔티티 클릭에 `TouchReceiveComponent` + `TouchEvent`는 **쓰지 않는다** — 2026-09-22 실측: 유닛 엔티티(서버 AddComponent + 클라 TouchArea 지정)에 클릭 지점이 판정 상자 안인데도 TouchEvent가 오지 않았고 클라에서 넣은 TouchArea도 반영되지 않았다(서버 자동값 0.5×0.8만 남음). 월드 엔티티 클릭은 전부 `ScreenTouchEvent` + 자체 상자 판정(`RtsUnitSelectLogic.UnitAtScreen` 폭 1.4·높이 2.2 발 기준, `CellAtScreen`)으로 한다. 마우스 오버는 `MouseMoveEvent` + `_InputService:GetCursorPosition()`으로 직접 판정, 커서 교체는 `_InputService:SetCursor(ruid, Vector2.zero)` / `ResetCursor()`(메이플 손 커서 `3930c5d2e85b4bff8467aada64fda7f5`). 월드→UI 배치는 `_UILogic:ScreenToUIPosition(_UILogic:WorldToScreenPosition(v))` = 화면 중앙 원점이라 HUD 그룹 자식은 anchor (0.5,0.5)에 그 값을 그대로. 서버가 클라 한 명에게만 보내려면 `@ExecSpace("Client")` 메서드의 **마지막 파라미터 = userId**, 클라가 부른 `@ExecSpace("Server")` 메서드에선 `senderUserId`로 검증. 양쪽 공통 시계는 `_UtilLogic.ServerElapsedSeconds`.
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

## 월드 클릭은 ScreenTouchEvent 한 곳에서 — UI 우선은 IsPointerOverUI + 메뉴 사각형 판정
- Rule: 유닛·발판 클릭은 전부 `RtsUnitSelectLogic.HandleScreenTouchEvent`(배치 모드 → 이동 모드 → 유닛 상자 → 빈 곳 순)에서 판정한다. UI 위 클릭은 `_InputService:IsPointerOverUI()`로 먼저 버리고, 팝업이 열려 있으면 `_RtsPopupLogic:IsOpen()`, 작은 메뉴는 `MenuRect`(UI 중앙 원점, 여백 6px) `IsOverMenu`로 한 번 더 거른다. 엔티티 `TouchEvent`는 2026-09-17엔 UI와 같이 발화하는 문제, 09-22엔 아예 안 오는 문제가 있어 폐기했다 — 새 월드 클릭 대상이 생기면 이 핸들러에 상자 판정을 추가할 것.
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

## shootF는 활 쏘는 자세(기본 활 잔상까지 그림) — 표창 던지기는 swingO1 + hideWeapon
- Rule: 아바타 액션 `shootF`는 표창 직업에 써도 활 쏘는 자세가 나오고 무기 슬롯과 무관하게 기본 활 잔상이 그려진다. 표창·투척 연출은 `swingO1`(한손 머리 위→앞)에 `hideWeapon`(잔상·무기 숨김)을 켜서 팔 움직임만 보이게 한다(나이트로드 쿼드러플 스로우 확정). 모션 후보 비교는 Play 중 `_RtsJobTableLogic.FxOverrides["<job>:<i>"] = fx`(client 컨텍스트, maker_execute_script)로 재시작 없이 바꿔 보여준다.
- Scope: project
- Rationale: 2026-09-20 사용자 "표창 던지는 모션인데 왜 활이 나오지?" → hideWeapon으로 활은 사라졌지만 "캐릭터 모션이 활쏘기 모션" → swingO1로 교체하니 "지금 좋은데 / 던지기 모션이잖아".
- Priority: takes precedence over defaults

## 유닛 부속 그림자(분신)는 자식 스프라이트 + 액션 이름 릴레이 — 아바타 복제·any 타입 파라미터 금지
- Rule: 캐릭터를 따라 움직이는 부속(쉐도우 파트너)은 유닛 엔티티의 자식 MapObject 스프라이트로 만들고, 본체에 ActionStateChangedEvent를 보내는 유일한 통로(RtsSkillFxLogic.SendAction)에서 같은 이름의 클립을 스프라이트에 넣는다(SpriteRUID 교체 + PlayRate). 아바타 부품은 order 0에 그려지므로 뒤에 둘 것은 OrderInLayer 음수. 아바타를 하나 더 붙여 SetColor로 검게 하는 방식은 원작과 다르고(사용자 거부), 서버 메서드 파라미터를 `any cm`으로 받아 CostumeManager 속성을 쓰면 **본체 옷이 안 입혀진다**(타입을 `CostumeManagerComponent`로 명시해야 함 — 2026-09-20 실측).
- Scope: project
- Rationale: 2026-09-20 나이트로드 쉐도우 파트너 1차(아바타 복제)에서 본체가 기본 아바타로 보이는 사고 + 사용자 "똑같은 실루엣이면 안 될 것 같은데" → 원작 4111002/special 클립 방식으로 교체.
- Priority: takes precedence over defaults

## 녹화 영상에서 스킬 사운드 추출 + 사용자 리소스 오디오 업로드는 OGG로(wav·mp3는 msw-mcp 2단계 오류)
- Rule: 사용자가 준 게임 녹화(mp4)에서 효과음을 뽑을 땐 ffmpeg로 wav 추출 → BGM만 있는 구간(RMS 바닥)을 노이즈 프로파일로 STFT 스펙트럼 게이팅(임계 = 평균 + 2.5σ, 소프트 마스크) → 시전 1회 구간을 잘라 페이드·정규화(스크립트 scratchpad/audio/clean.py, 결과 `assets/audio/<skill>/`). 뒤에 남는 잔음은 끝점을 앞당겨 자른다. **오디오는 OGG(Vorbis)로 올려야 한다** — msw-mcp `asset_create_account_resource_storage_item` 2단계 완료 호출이 wav·mp3(44.1k 모노·48k 스테레오)는 전부 'unexpected error', `.ogg`(libvorbis q5)는 즉시 성공(2026-09-20 실측, 사용자 힌트 "오디오클립 확장자가 아니라서"). ffmpeg `-codec:a libvorbis -q:a 5`로 변환 → PUT(put_upload.py) → 2단계. 결과 파일은 SendUserFile + `assets/` 복사 + reveal_path로 전달.
- Scope: project
- Rationale: 2026-09-20 인레이지 레이징 블로우 사운드 — 라이브러리 1120017/hit가 RED 시절 소리라 사용자가 현재 버전 녹화를 제공. BGM 잔량 3%로 정리, 사용자 enrage_sfx2c 확정.
- Priority: takes precedence over defaults

## 유닛 순회는 1~6 고정이 아니라 RtsUnitLogic.ListZoneUnits(구역 엔티티 스캔)
- Rule: 구역의 유닛을 도는 코드(버프 출처·아이콘 갱신·클릭 판정·대상 드롭다운·칸 점유)는 `_RtsUnitLogic:ListZoneUnits(zone)`(맵 루트 자식 이름 `Unit<구역>_<번호>` 스캔, 서버·클라 공용, 오름차순)을 쓴다. `GetMaxUnits()`(6)는 영입 상한·HUD 슬롯 수에만 쓴다 — 시험대 7·8번(불독·비숍)이나 초과 영입 유닛이 순회에서 빠지면 안 된다. HUD 슬롯은 아직 6칸 고정(7번 이상은 HUD에 안 뜸).
- Scope: project
- Rationale: 2026-09-20 사용자 "불독/비숍은 왜 적용 중인 버프와 아이콘이 표시 안 되지? 유닛 6개까지만 적용되게 해둔 것 같은데 제한 있으면 없애" — GetBuffsFor·RefreshZone이 1~6만 돌아 8번 비숍의 프레이가 아무에게도 안 걸리고 7·8번은 아이콘도 못 받았다.
- Priority: takes precedence over defaults

## 라이브러리 sprite 원본 PNG는 mod-resource CDN에서 받는다(썸네일 64px 말고)
- Rule: `asset_get_account_resource_metadata_bulk`의 `files.png.path`(예 `b8-sprite/2d/<ruid>.png.mod`)를 `https://mod-resource.dn.nexoncdn.co.kr/<path>`로 GET하면 .mod 컨테이너가 오고, 그 안의 `PNG…IEND` 구간을 잘라내면 원본 PNG(원 크기)다(스크립트 scratchpad/joker9 fetch). 64px 썸네일(`mod-thumbnail…/<ruid>_64.png`)은 후보 훑기용, 자르기·색 변형·크기 판단은 원본으로. 원본에서 잘라 만든 sprite(카드 1장 등)는 `asset_create_account_resource_storage_item(category sprite, subcategory skill)` 2단계 업로드로 내 리소스가 된다(PNG는 바로 성공).
- Scope: project
- Rationale: 2026-09-20 조커 카드 — 썸네일로는 카드 구분이 안 돼 원본을 받아 400041009/screen/3(104×176 카드 덱)을 찾고 분홍 변형을 만들어 올렸다.
- Priority: takes precedence over defaults

## 유닛에 붙는 지속 연출(loopClip 등)은 유닛 엔티티의 자식으로 스폰한다 — 월드 좌표에 두면 위치 이동 때 남는다
- Rule: 공격 중 캐릭터에 계속 붙어 있는 연출(`RtsSkillFxLogic.EnsureLoopFx`의 loopClip, 버프 아이콘, 그림자)은 `SpawnByModelId(…, unitEntity)`로 유닛의 자식에 두고 로컬 값은 절반(부모 스케일 2)으로 준다. 유닛의 보는 방향은 아바타 루트 자식의 스케일만 뒤집으므로 유닛 엔티티 자식은 영향 없음 — 반전은 `FlipX`로 직접, 방향이 바뀌면 기존 루프 엔티티의 FlipX·Position만 갱신(`RefreshLoopFacing(key)` — 시전마다 + `RtsUnitComponent.ApplyFace`(FaceDir 동기화)에서도 호출: 시전 RPC가 FaceDir 동기화보다 먼저 올 수 있어 시전 때만 맞추면 한 주기 어긋난다). 루프·모션 상태 표의 키는 `LoopKey(zone, no)` = 구역×100+번호(시전 연출은 전 클라에 오므로 유닛 번호만으론 다른 구역과 겹침). 1회성 연출(clip·투사체·타격)은 월드(mapRoot)에 둬도 된다. 클립 방향 플래그는 반드시 원본 PNG로 정한다(폭풍의 시 keydown = 왼쪽 보기 → loopFacesLeft true; 09-18엔 동기화 타이밍 버그를 플래그로 덮어 반대로 넣었었다).
- Scope: project
- Rationale: 2026-09-20 사용자 "조커 애니메이션이 캐릭터 위치 이동해도 안 따라간다" — loopClip을 mapRoot 아래 월드 좌표에 스폰해서 유닛을 옮겨도 제자리에 남았다.
- Priority: takes precedence over defaults

## 투사체 옵션 확장(2026-09-20): projs 무작위·projArc 포물선 — 그리고 proj 게이트 주의
- Rule: `RtsSkillFxLogic.SpawnProjectile`은 `projs = {…}`(발마다 차례로 — 라운드 로빈, 순번 키는 **첫 RUID + 개수** 문자열; fx 테이블은 GetSkills가 부를 때마다 새로 만들어져 테이블을 키로 쓰면 매 공격 1번부터 다시 돌아 2색만 나온다)와 `projArc = h`(직선 보간 + 비행 방향에 수직인 4t(1−t)·h 튀어오름, 수직 벡터는 y≥0으로 맞춰 **항상 위로 볼록**(왼쪽으로 날 때 부호가 뒤집히던 것 수정), 발마다 50~100%, `projArcRandom=true`면 위/아래 무작위, `projArcByDist = { 1칸, 2칸, 3칸, 4칸+ }`가 있으면 PlayProjectile이 넘긴 칸 거리(체비쇼프, 반올림)로 고른 값 그대로; 0.03초 타이머로 WorldPosition 갱신, TweenLogic 대신)를 지원한다. **PlayCast의 투사체 게이트는 `proj` 또는 `projs`가 있어야 열린다** — 새 투사체 키를 추가하면 그 게이트(`if ((fx.proj…) or (fx.projs…)) and target`)와 `Preload`에도 넣을 것. 카드처럼 자전(`projSpin`)하는 투사체는 `projNoRotate=true`.
- Scope: project
- Rationale: 조커 3차에서 `projs`만 주고 `proj`를 빼자 게이트가 닫혀 "카드가 안 날아가잖아". 포물선은 사용자 요구("포물선 그리면서 날아가야 하는 투사체").
- Priority: takes precedence over defaults

## 모션 옵션(2026-09-20): motionCycle 순환·motionFrame 프레임 고정 — 그리고 SendAction 인자 수
- Rule: `fx.motions = {…}, motionCycle = true, motionGap`은 공격이 이어지는 동안 액션을 차례로 반복(RtsSkillFxLogic.CycleTimer, 0.6초 끊기면 CheckLoops가 대기 자세로). `motionLoop` + `motionFrame`/`motionFrameEnd`는 한 액션의 프레임 구간만 루프(ActionStateChangedEvent 5·6번째 인자). `SendAction(body, name, rate, playType, frameA, frameB)`는 6인자라 **모든 호출이 nil, nil까지 넘겨야** 빌드 Error(LEA-1121 인자 수 불일치)가 안 난다. 아바타 액션 전체 목록은 msw 문서 'Controlling Avatar Animations'(35종: stand1/2·walk1/2·alert·prone·proneStab·jump·fly·sit·ladder·rope·dead·heal·blink·swingO1/O2/O3/OF·swingT1/T2/T3/TF·swingP1/P2/PF·stabO1/O2/OF·stabT1/T2/TF·shoot1/shoot2/shootF) — 회전(spin) 액션은 없다.
- Scope: project
- Rationale: 조커 캐릭터 모션 — 사용자가 AvatarItem Editor로 35종을 훑고 "마음에 드는 게 없다" → 3종+찌르기 순환으로 확정.
- Priority: takes precedence over defaults

## 구역 그리드 16×13(2026-09-20) — 칸 수를 바꾸면 5곳을 같이
- Rule: 그리드 = 16열×13행, 칸 1.7778유닛, `GridLeft −14.2222`(뷰 42.66 폭에 좌우 7.11 여백 = 대칭), `GridTop 11.5556`(위아래 0.44 여백). 텍스처 = `tools/gen-track-grid.js`(COLS/ROWS) → 1280×1040 PNG → 내 리소스 sprite 업로드(PPU 100, `GridTextureScale 2.2222`) → `RtsThemeLogic` 프리셋 gridRUID(헤네시스 `95b3ec9d377e46ecb9d394467d27dada`; 엘나스 `651583e1…`는 아직 18×12). 장식물(`GetHenesysDecor`)은 **좌우 여백에만**(col ≤ −0.6 / ≥ 16.9; 위아래 여백은 0.25칸뿐), 오른쪽 x 18칸 이후는 영입 HUD 밑이라 큰 건물은 8행 아래. 트랙 경로(GetTurnPoints·SEQ)는 최대 14열이라 그대로.
- Scope: project
- Rationale: 사용자 "맨 우측 2줄 타일 삭제(좌우 대칭), 맨 아래 한 줄 추가(위 공간 활용해 위로 당김), 타일에 오브젝트 안 겹치게".
- Priority: takes precedence over defaults

## 공격 루프는 유닛마다(SpawnUnit → StartLoop), 메인 대상은 Focus로 고정 — 규칙 원문 .info/attack.md
- Rule: 시험대(개발용)는 2026-09-20부터 무적 순회 몬스터 100기(`RtsCombatLogic.BenchMonsters`, RtsTrackWalkerComponent 루프) — 웨이브 #10이 오면 TestBench 코드째 삭제. `RtsUnitLogic.SpawnUnit`·`RequestLevelUp`이 `_RtsCombatLogic:StartLoop`를 걸어 모든 유닛이 각자 공격한다(시험대 UnitNo만 돌던 것 폐기). `RtsCombatLogic.Focus[userId_no]` = 메인 대상 엔티티 — `PickTargets(…, focus)`가 후보 안에 있으면 맨 앞으로 올려 유지, 죽거나(엔티티 소멸·`GetZoneMonsters`가 HP 0 제외) 사거리 밖이면 가장 가까운 적으로. area·dot·spread는 Focus를 안 쓴다. 공격 규칙 문서는 `.info/attack.md`(사용자가 만든 파일 — 룰 바뀌면 여기 갱신).
- Scope: project
- Rationale: 2026-09-20 사용자 "유닛이 한 마리만 공격하는데 정상임? 모든 유닛이 개별적으로·자율적으로", "메인 대상은 죽거나 거리 밖으로 나가기 전까지 쭉".
- Priority: takes precedence over defaults


## 개발모드(RtsCombatLogic.TestBench) = 주니어 발록 보스 1기 + 유닛 없이 시작·영입 팝업 자유 영입(Lv50) + 우측 하단 '테스트 프리즘'(토글) + 보스 라운드 취급
- Rule: 2026-09-22 사용자 "개발모드부터 만들자. 백만 메소, 프리즘 선택 획득, 몬스터는 주니어 발록 1마리(보스·무적), 한 직업씩 테스트". 입장 시 `SetupTestBench`가 mob/8130100 stand 클립(4b3ad414…) 보스를 (9,7)에(스케일 2, 피격 박스 1.3×1.5, IsBoss → 체력바 BossBarY 3.4), 유닛은 없음(메소 시범값 — 사용자 "100만 빼자"). 영입 팝업 카드 → `RequestRecruit(jobId)`(개발: 무료·Lv50·중복 허용, `FreePadNear`로 보스 곁 빈 발판, 팬텀은 '영웅(개발)' 탭), 이동 쿨 0. 우측 하단 '테스트 프리즘' → `BuildDevPrism`(12종 직업별, `RequestDevPrism` = 있으면 `RemovePrism`(잠금 기본값 복구) 없으면 `ApplyPrism`), '내 유닛 전부 삭제' = `RequestDevClear`. `IsBossRound(zone)` = TestBench면 true → `SkillUsable`이 보스전 잠금(1) 스킬을 거른다(사용자 "드래곤 로어가 발록한테 나감"). 거대화 = 스피어 버스터 fx scale ×3. **프리즘 = `RtsUnitComponent.Prisms`(@Sync 쉼표 목록) + `RtsJobTableLogic.GetPrisms/GetSkillsFor/GetStatFor/GetJobNameFor`**(직업 표 복사본 위에 오버레이: 스킬 항목 교체/추가, st.ratio/hits/period/range/bossAdd, locks → SetLock 3) — GetSkills(jobId)/GetStat(jobId,L)를 직접 부르던 자리(전투·CastFx/HitFx·팝업·HUD 슬롯·잠금·그림자·프리로드)는 전부 For 판으로 바꿨다(HitFx는 zone·no를 받음). 보스 배율은 `DoAttack`에서 대상 IsBoss일 때만 `bossMul = (1+bossAdd/100)·finBoss/fin·bossFinal`. 스킬 항목 키: `bossHits`(보스 1마리에게 n회 반복 — 템페스트 15), `bossFinal`(0.9), `hitRatios`(타격별 비율 — 블토 24×39 + 카르마 15×51), `forceCrit`(트루 스나이핑). 표식 중복 대상은 PlayMark dup로 ±1.2유닛 흩뿌림. 실측: 엘릭서+템페스트 썬콜 Lv50 → 보스에 3초마다 15타 7.7~9.3k(=9,376×0.9×무기 0.9~1.1) ✓, 11직업 프리즘 전부 적용 시 런타임 에러 0.
- Scope: project
- Rationale: 프리즘 자산 선별을 직접 눈으로 하려면 프리즘이 실제로 발동하는 개발 환경이 먼저 필요했음. 웨이브·보스 페이즈가 생기면 삭제.
- Priority: takes precedence over defaults

## 효과음 재생 속도(피치)는 SoundComponent.Pitch로만 — SoundService.PlaySound에는 없다 (2026-09-22)
- Rule: 소리를 빨리/느리게 감으려면 `SoundComponent`(AudioClipRUID·Pitch 0~3·Volume·Loop=false·SetCameraAsListener=false) 엔티티를 두고 `Play()`. 0.2초 간격처럼 겹쳐 나야 하는 소리는 컴포넌트 1개면 Play마다 앞 소리가 끊기므로 풀(RtsSkillFxLogic.SfxPool 6개, 라운드 로빈)로. AudioClipRUID를 넣어야 로드되므로 프리로드 때 풀에 미리 올린다(WarmSfx) — 확인: IsAudioClipLoaded true·Pitch 1.5·IsPlaying true.
- Scope: project
- Rationale: 애로우 레인 타격음 400030002/loop(0.97초)을 사용자 요청으로 1.5배 빨리 감기.
- Priority: takes precedence over defaults

## 프리즘/스킬 연출 자산은 첫 시전 전에 프리로드 — 안 하면 "적용 안 됨"처럼 보인다 (2026-09-22)
- Rule: 클립 자산은 SpriteRUID를 넣는 순간부터 내려받기 시작해 큰 세트(tile 9종 × 21프레임)는 몇 초 걸린다. 그동안 시전하면 서버 판정은 맞는데 표식·클립이 빈 채로 그려져 사용자는 "프리즘이 적용 안 된다 → 껐다 켜니 됨"으로 본다. 유닛이 생길 때 그 직업의 프리즘 변형까지 `PreloadJobFx`로 올려 둔다. 원인 찾을 땐 먼저 서버 표(GetSkillsFor)를 execute_script로 찍어 서버/클라 어느 쪽인지 가른다.
- Scope: project
- Rationale: 엘릭서+템페스트 동시 적용 버그 조사 — 서버 표는 정상(bossHits 15, cd 2), 클라 자산 지연이 원인.
- Priority: takes precedence over defaults

## Maker 빌드 분석기는 메서드 서명을 캐시한다 — 기존 메서드에 인자를 늘리면 옛 서명으로 오류, 새 이름으로 추가 (2026-09-22)
- Rule: 다른 스크립트가 부르는 메서드(예: RtsMonsterComponent.PlayHitFx)의 인자를 늘리면 빌드 콘솔이 옛 서명 `void PlayHitFx(table, boolean)`로 인자 수 오류를 내고(런타임은 정상), refresh·save·재시작으로도 안 지워진다. 인자가 다른 새 메서드(PlayHitFxAt)를 만들고 옛 것은 위임하게 두면 해결. 또 mlua는 메서드 파라미터 재대입(`content = list`)·`any` 값 산술을 거부할 수 있어 새 local로 받는다. 문법 오류는 `maker_clear_logs` → `maker_refresh_workspace` 직후 `maker_logs(normal)`에 `[LEA-3016] InvalidFormat … RtsX.mlua:줄` 로 찍힌다(빌드 콘솔엔 안 나옴).
- Scope: project
- Rationale: 2026-09-22 PlayHitFx 3인자화·BuildSkillTab 파라미터 재대입·DescLines 꼬리 잔여로 두 스크립트가 nil이 됐던 일.
- Priority: takes precedence over defaults

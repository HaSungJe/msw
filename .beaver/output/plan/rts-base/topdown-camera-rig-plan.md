# Plan — 탑다운 맵·카메라 리그 (rts-base #1)

## Feature Summary
- **Feature**: RectTile 탑다운 맵(256×256셀) 위에서 숨긴 아바타를 카메라 앵커로 삼아 스타식 화면 스크롤(방향키+엣지+휠줌+Confined 커서) 제공
- **Entry point**: `Scene map://RtsMap` + `RtsCameraAnchorComponent`(DefaultPlayer 부착, Client Input)
- **Domain**: rts-base

---

## Prerequisites
- [ ] **Maker 실행 + msw-maker-mcp 연결** — 맵 생성·스크립트 생성·Play Test 전부 Maker 경유 (현재 세션에서 연결 확인됨, build 시 재확인)
- [ ] **RectTile 모드 신규 맵 `RtsMap` 생성** — Maker에서 TileMapMode=RectTile로 생성해야 KinematicbodyComponent가 이동 주체가 됨 (스크립트로 모드 전환 불가, Maker 편집 필요)
- [ ] **월드 시작 맵을 RtsMap으로 지정** (또는 테스트 동안 map01→RtsMap 이동 수단 마련) — Maker에서 설정
- [ ] **이벤트 핸들러 데코레이션 문법 확인** — ExtendedScriptFormat의 handler 선언은 Maker 스크립트 에디터가 스캐폴딩을 생성하므로, build에서 생성 후 아래 코드를 이식 (문서 근거: Event Handler 추가 절차)

---

## File List

| File | Action |
|------|------|
| `map/RtsMap.map` | new (Maker 생성 — RectTile 모드, UseCustomBound 영역 256×256셀) |
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | new (튜너블 상수 테이블) |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | new (DefaultPlayer 부착) |
| `Global/DefaultPlayer.model` | modified (Maker에서 RtsCameraAnchorComponent 부착) |
| `map/map01.map` | unchanged (유지 — 시작 맵 지정만 RtsMap으로 변경) |

---

## Design

> 신규 프로젝트라 참조할 기존 사용자 코드 없음. 컨벤션 근거: CLAUDE.md(Component/Logic 분리·PascalCase·@ExecSpace 명시), 문법 근거: Environment/NativeScripts/Component/AIWanderComponent.d.mlua:1-37(ExtendedScriptFormat), 로직 근거: msw-mcp 공식 문서(CustomPlayerController 패턴, KinematicbodyComponent, InputService, CameraComponent).

### Config (튜너블 상수 — Logic)

```lua
-- RootDesk/MyDesk/RtsConfigLogic.mlua — 전역 접근 _RtsConfigLogic
@Logic
script RtsConfigLogic extends Logic

	-- 맵 그리드 (사용자 확정: 256×256셀. CellSize는 Play Test 실측 후 고정)
	property integer MapCellsX = 256
	property integer MapCellsY = 256
	property number CellSize = 1.0

	-- 카메라 스크롤
	property number ScrollSpeed = 8.0      -- 셀/초 단위 감각, Play Test 튜닝
	property integer EdgeMarginPx = 20     -- 엣지 스크롤 발동 폭(px)

	-- 맵 영역(월드 좌표) — RtsMap의 UseCustomBound와 동일 값 유지
	@ExecSpace("ServerAndClient")
	method Vector2 GetMapLeftBottom()
		return Vector2(0, 0)
	end

	@ExecSpace("ServerAndClient")
	method Vector2 GetMapRightTop()
		return Vector2(self.MapCellsX * self.CellSize, self.MapCellsY * self.CellSize)
	end

end
```

### Entry Point (카메라 앵커 — Component)

```lua
-- RootDesk/MyDesk/RtsCameraAnchorComponent.mlua — DefaultPlayer 모델에 부착
@Component
script RtsCameraAnchorComponent extends Component

	property Vector2 InputDirection = Vector2(0, 0)  -- 방향키 누적 입력 (클라 로컬)

	-- [서버] 아바타를 전 클라이언트에서 숨긴다 (Enable은 Sync 프로퍼티)
	@ExecSpace("ServerOnly")
	method void OnBeginPlay()
		local entity = self.Entity
		entity.AvatarRendererComponent.Enable = false     -- 아바타 렌더 숨김
		entity.NameTagComponent.Enable = false            -- 이름표 숨김
		local body = entity.KinematicbodyComponent
		body.EnableShadow = false                         -- 그림자 숨김
		body.EnableJump = false                           -- 점프 무효
	end

	-- [클라] 자기 아바타만: 기본 조작 차단 + 커서 가두기 + 카메라 설정
	@ExecSpace("ClientOnly")
	method void OnBeginPlay()
		if _UserService.LocalPlayer ~= self.Entity then return end

		self.Entity.PlayerControllerComponent.Enable = false   -- 기본 이동/조작 차단 (문서: CustomPlayerController 패턴)
		self.Entity.KinematicbodyComponent.EnableTileCollision = false  -- 카메라는 지형에 안 걸림

		_InputService:CursorLockMode(CursorLockMode.Confined)  -- 창모드에서 커서 이탈 방지 (Windows PC 전용)

		local camera = self.Entity.CameraComponent
		camera.DeadZone = Vector2(0, 0)     -- 즉각 반응 (문서: DeadZone=0이면 미세 이동에도 카메라 반응)
	end

	-- [클라] 매 프레임: 방향키 + 엣지 스크롤 합산 → 앵커 이동
	@ExecSpace("ClientOnly")
	method void OnUpdate(number delta)
		if _UserService.LocalPlayer ~= self.Entity then return end

		local dir = Vector2(self.InputDirection.x, self.InputDirection.y)

		-- 엣지 스크롤: 커서가 화면 가장자리 EdgeMarginPx 이내면 해당 방향 가산
		local cursor = _InputService:GetCursorPosition()   -- 스크린 좌표(원점: 좌하단)
		local margin = _RtsConfigLogic.EdgeMarginPx
		if cursor.x <= margin then dir.x = dir.x - 1
		elseif cursor.x >= _UILogic.ScreenWidth - margin then dir.x = dir.x + 1 end
		if cursor.y <= margin then dir.y = dir.y - 1
		elseif cursor.y >= _UILogic.ScreenHeight - margin then dir.y = dir.y + 1 end

		if dir.x == 0 and dir.y == 0 then
			self.Entity.KinematicbodyComponent.MoveVelocity = Vector2(0, 0)
			return
		end

		-- 대각 정규화 후 속도 적용 (PlayerController가 꺼져 있어 MoveVelocity 직접 제어)
		local len = math.sqrt(dir.x * dir.x + dir.y * dir.y)
		local speed = _RtsConfigLogic.ScrollSpeed
		self.Entity.KinematicbodyComponent.MoveVelocity = Vector2(dir.x / len * speed, dir.y / len * speed)

		-- 맵 영역 클램프 (UseCustomBound 영역 밖 이탈 방지)
		local pos = self.Entity.TransformComponent.WorldPosition
		local lb = _RtsConfigLogic:GetMapLeftBottom()
		local rt = _RtsConfigLogic:GetMapRightTop()
		local cx = math.max(lb.x, math.min(pos.x, rt.x))
		local cy = math.max(lb.y, math.min(pos.y, rt.y))
		if cx ~= pos.x or cy ~= pos.y then
			self.Entity.KinematicbodyComponent:SetWorldPosition(Vector2(cx, cy))
		end
	end

	-- [클라] 방향키 입력 기록 (문서: CustomPlayerController 패턴과 동일 구조)
	@ExecSpace("ClientOnly")
	@EventSender("Service", "InputService")
	handler HandleKeyDownEvent(KeyDownEvent event)
		if _UserService.LocalPlayer ~= self.Entity then return end
		local key = event.key
		if key == KeyboardKey.RightArrow then self.InputDirection.x = self.InputDirection.x + 1
		elseif key == KeyboardKey.LeftArrow then self.InputDirection.x = self.InputDirection.x - 1
		elseif key == KeyboardKey.UpArrow then self.InputDirection.y = self.InputDirection.y + 1
		elseif key == KeyboardKey.DownArrow then self.InputDirection.y = self.InputDirection.y - 1
		end
	end

	@ExecSpace("ClientOnly")
	@EventSender("Service", "InputService")
	handler HandleKeyUpEvent(KeyUpEvent event)
		if _UserService.LocalPlayer ~= self.Entity then return end
		local key = event.key
		if key == KeyboardKey.RightArrow then self.InputDirection.x = self.InputDirection.x - 1
		elseif key == KeyboardKey.LeftArrow then self.InputDirection.x = self.InputDirection.x + 1
		elseif key == KeyboardKey.UpArrow then self.InputDirection.y = self.InputDirection.y - 1
		elseif key == KeyboardKey.DownArrow then self.InputDirection.y = self.InputDirection.y + 1
		end
	end

end
```

> 표기 주의: `@EventSender` 데코레이션·`handler` 키워드는 Maker 스크립트 에디터가 생성하는 스캐폴딩 기준으로 build에서 확정한다(Prerequisites 4번). 로직 본문은 위 코드 그대로 이식.

### Scene (Maker 편집 — 코드 아님)
- `RtsMap` 생성: TileMapMode=**RectTile**, `MapComponent.UseCustomBound=true`, `LeftBottom=(0,0)`, `RightTop=(256×CellSize, 256×CellSize)`.
- 바닥 타일: RectTile 기본 타일로 전 영역(또는 시각 확인용 일부) 채움 — 스폰 위치는 맵 중앙 부근.
- `CameraComponent.isAllowZoomInOut=true` (DefaultPlayer) — 휠 줌 네이티브 활성.
- 월드 시작 맵 지정: RtsMap.

---

## Test Cases
> 이 스택에는 CLI 테스트 러너가 없음(docs/testing.md). 아래는 Play Test 시나리오로, `/beaver:test` 시 `maker_save → maker_logs(build) → maker_play → maker_logs(normal)·maker_screenshot → maker_stop` 절차로 검증한다. DataStorage 미사용 → [SMOKE:data-access] 해당 없음.

```
[SUCCESS] 게임 시작 시 아바타·이름표·그림자가 화면에 보이지 않는다 (스크린샷)
[SUCCESS] 방향키 4방향+대각으로 카메라가 스크롤되고, 키를 떼면 즉시 정지한다
[SUCCESS] 커서를 화면 가장자리(20px 이내)로 옮기면 해당 방향으로 스크롤된다 (창모드 포함)
[SUCCESS] 마우스 휠로 줌 인/아웃 된다 (isAllowZoomInOut)
[FAIL:boundary] 맵 영역 경계에서 카메라가 더 진행하지 않는다 (클램프 SetWorldPosition 동작)
[FAIL:input] 기본 점프/이동(스페이스·기존 조작)이 무효다 (PlayerController/EnableJump 비활성 확인)
[FAIL:sync] 2클라이언트 테스트 시 한 클라의 스크롤이 다른 클라 화면에 영향을 주지 않는다 (멀티는 #13에서 정식 검증, 여기선 로그로 클라 전용 실행만 확인)
```

---

## Response Codes
> HTTP 없음 — 각 진입점의 결과 계약.

| Outcome | Cause |
|------|------|
| 카메라 스크롤(앵커 이동) | 방향키/엣지 입력 |
| 스크롤 정지(MoveVelocity=0) | 입력 없음 |
| 위치 클램프(SetWorldPosition) | 앵커가 맵 영역 경계 도달 |
| 커서 창 내 제한 | Confined 모드 (PC 전용, 모바일은 무동작) |
| 아바타 비표시·기본조작 무효 | 서버 Enable(Sync) off + 클라 PlayerController off |

# Plan — 카메라·맵 개편 (운빨 디펜스 #3)

## Feature Summary
- **Feature**: 맵 192×56(8구역, 4열×2행) 축소 + F1~F8/미니맵 구역 스냅 카메라 + 자유 카메라 제거
- **Entry point**: `RtsCameraAnchorComponent`(F키) · `RtsHudLogic`(미니맵 클릭) · `RtsConfigLogic`(구역 변환)
- **Domain**: rts-base

---

## Prerequisites
- [x] Maker 실행 확인 (빌드 시 재확인 — 현재 연결됨)
- [x] 결정 완료: 4열×2행, 구역 48×28, 미니맵 구역 스냅 (spec Decisions)

---

## File List

| File | Action |
|------|------|
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | modified (맵 192×56, 구역 상수·GetZoneCenter, 스크롤/마진 상수 삭제) |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | modified (전면 개편 — F1~F8 구역 점프만, 자유 카메라 삭제) |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified (미니맵 v6: 맵 비율 스트립+구역 경계/번호+구역 하이라이트+구역 스냅 클릭) |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | unchanged (게터 경유 자동 적응 — 168타일) |
| `map/RtsMap.map` | unchanged (경계 파일 정의 없음, 타일은 런타임 채움) |

---

## Design

> 근거: 기존 코드 통합 지점 — RtsCameraAnchorComponent.mlua(OnUpdate 스크롤 블록·키 핸들러 삭제), RtsConfigLogic.mlua(상수 교체), RtsHudLogic.mlua(BuildHud 미니맵 블록·OnMinimapClick·UpdateMinimapViewport 교체). 삭제 목록은 spec §1.7 체크 참조.

### Config (RtsConfigLogic.mlua — 전체 교체)

```lua
@Logic
script RtsConfigLogic extends Logic

	-- 구역: 4열×2행, 구역 = 카메라 한 화면(뷰 44.5×25 + 여유)
	property number ZoneCols = 4

	property number ZoneRows = 2

	property number ZoneWidth = 48

	property number ZoneHeight = 28

	property number CellSize = 1

	property number CameraViewWidth = 44.5

	property number CameraViewHeight = 25

	method number GetZoneCols() return self.ZoneCols end

	method number GetZoneRows() return self.ZoneRows end

	method number GetZoneWidth() return self.ZoneWidth end

	method number GetZoneHeight() return self.ZoneHeight end

	method number GetMapCellsX()
		return self.ZoneCols * self.ZoneWidth
	end

	method number GetMapCellsY()
		return self.ZoneRows * self.ZoneHeight
	end

	method number GetCameraViewWidth() return self.CameraViewWidth end

	method number GetCameraViewHeight() return self.CameraViewHeight end

	-- 구역 n(1~8, 윗줄 1~4 좌→우, 아랫줄 5~8) → 구역 중앙 월드 좌표
	method Vector2 GetZoneCenter(number n)
		local idx = n - 1
		local col = idx % self.ZoneCols
		local row = math.floor(idx / self.ZoneCols)   -- 0=윗줄
		local cx = col * self.ZoneWidth + self.ZoneWidth * 0.5
		local cy = (self.ZoneRows - 1 - row) * self.ZoneHeight + self.ZoneHeight * 0.5
		return Vector2(cx, cy)
	end

	method Vector2 GetMapLeftBottom() return Vector2(0, 0) end

	method Vector2 GetMapRightTop()
		return Vector2(self:GetMapCellsX(), self:GetMapCellsY())
	end

end
```
(삭제: MapCellsX/Y 고정값·ScrollSpeed·EdgeMarginPx·CameraMarginX/Y와 게터들)

### Entry Point (RtsCameraAnchorComponent.mlua — 전체 교체)

```lua
-- rts-base #3(운빨 디펜스): 숨긴 아바타 = 카메라 앵커, F1~F8 구역 시점 전환 전용 (자유 카메라 없음)
@Component
script RtsCameraAnchorComponent extends Component

	property number CurrentZone = 1

	method void OnBeginPlay()
		if self:IsServer() then
			self:SetupServer()
		else
			self:SetupClient()
		end
	end

	@ExecSpace("ServerOnly")
	method void SetupServer()
		local entity = self.Entity
		entity.AvatarRendererComponent.Enable = false
		entity.NameTagComponent.Enable = false
		local body = entity.KinematicbodyComponent
		body.EnableShadow = false
		body.EnableJump = false
	end

	@ExecSpace("ClientOnly")
	method void SetupClient()
		if _UserService.LocalPlayer ~= self.Entity then return end

		self.Entity.PlayerControllerComponent.Enable = false
		self.Entity.KinematicbodyComponent.EnableTileCollision = false

		local camera = self.Entity.CameraComponent
		camera.DeadZone = Vector2(0, 0)
		camera.IsAllowZoomInOut = false   -- 줌 제거 (자유 카메라 금지)

		-- 입장 시 자기 구역으로 (배정은 #4 — 1차는 구역 1 스텁)
		self:JumpToZone(1)

		_RtsHudLogic:BuildHud(self.Entity)
	end

	@ExecSpace("ClientOnly")
	method void JumpToZone(number n)
		if n < 1 or n > _RtsConfigLogic:GetZoneCols() * _RtsConfigLogic:GetZoneRows() then return end
		self.CurrentZone = n
		local c = _RtsConfigLogic:GetZoneCenter(n)
		self.Entity.KinematicbodyComponent:SetWorldPosition(c)
		_RtsHudLogic:UpdateMinimapZone(n)
	end

	@ExecSpace("ClientOnly")
	method number FKeyToZone(any key)
		if key == KeyboardKey.F1 then return 1 end
		if key == KeyboardKey.F2 then return 2 end
		if key == KeyboardKey.F3 then return 3 end
		if key == KeyboardKey.F4 then return 4 end
		if key == KeyboardKey.F5 then return 5 end
		if key == KeyboardKey.F6 then return 6 end
		if key == KeyboardKey.F7 then return 7 end
		if key == KeyboardKey.F8 then return 8 end
		return -1
	end

	@ExecSpace("ClientOnly")
	@EventSender("Service", "InputService")
	handler HandleKeyDownEvent(KeyDownEvent event)
		if _UserService.LocalPlayer ~= self.Entity then return end
		local zone = self:FKeyToZone(event.key)
		if zone > 0 then self:JumpToZone(zone) end
	end

end
```
(삭제: InputDirection, 방향키 KeyDown/Up 핸들러, OnUpdate의 엣지 스크롤·커서 가드·MoveVelocity·클램프, CursorLockMode(Confined), ZoomRatioMin, 뷰포트 매 프레임 갱신 — 구역 전환 시에만 갱신하면 충분)

### UI (RtsHudLogic.mlua — 미니맵 블록·클릭·뷰포트 교체분)

```lua
	-- BuildHud 내 미니맵 블록 교체: 340 프레임 안에 맵 비율(192:56) 스트립
	-- 스트립: 320×93px 중앙 배치, 구역 경계선(세로 3, 가로 1) + 구역 번호 1~8
	property number MinimapStripW = 320

	property number MinimapStripH = 93

		-- (BuildHud 교체 코드)
		local mm = self:SpawnUI("model://uisprite", "RtsMinimap", bar,
			Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(self.MinimapSize, self.MinimapSize))
		self:Tint(mm, 0.13, 0.105, 0.075, 0.9)   -- 프레임 톤 배경
		local strip = self:SpawnUI("model://uisprite", "RtsMinimapStrip", mm,
			Vector2(0.5, 0.5), Vector2(0.5, 0.5), Vector2(0, 0), Vector2(self.MinimapStripW, self.MinimapStripH))
		strip.SpriteGUIRendererComponent.ImageRUID = DataRef(self.FloorRUID)
		strip.SpriteGUIRendererComponent.Color = Color(0.85, 0.85, 0.88, 1)
		-- 구역 경계선: 세로 3개(x=80,160,240px), 가로 1개(y=46.5px) — 1px 밝은 선
		-- 구역 번호 1~8: 각 구역 셀 중앙에 작은 텍스트
		-- 현재 구역 하이라이트: 구역 1칸 크기(80×46.5px) 반투명 사각형 = 기존 ViewportRect 재사용
		-- 클릭 오버레이 버튼(기존 RtsMinimapClick 유지) → OnMinimapClick

	-- 구역 하이라이트 갱신 (JumpToZone에서 호출 — 매 프레임 아님)
	@ExecSpace("ClientOnly")
	method void UpdateMinimapZone(number n)
		if self.ViewportRect == nil then return end
		local cols = _RtsConfigLogic:GetZoneCols()
		local idx = n - 1
		local col = idx % cols
		local row = math.floor(idx / cols)   -- 0=윗줄
		local cellW = self.MinimapStripW / cols
		local cellH = self.MinimapStripH / _RtsConfigLogic:GetZoneRows()
		self.ViewportRect.UITransformComponent.anchoredPosition =
			Vector2(col * cellW + cellW * 0.5, (_RtsConfigLogic:GetZoneRows() - 1 - row) * cellH + cellH * 0.5)
	end

	-- 미니맵 클릭 → 구역 스냅 (자유 위치 이동 아님)
	@ExecSpace("ClientOnly")
	method void OnMinimapClick()
		if self.AnchorEntity == nil then return end
		local cursor = _InputService:GetCursorPosition()
		local uiX = cursor.x * 1920 / _UILogic.ScreenWidth
		local uiY = cursor.y * 1080 / _UILogic.ScreenHeight
		-- 스트립 원점(UI): 미니맵 340 중앙 배치 → x=(340-320)/2=10, y=(340-93)/2=123.5
		local relX = (uiX - 10) / self.MinimapStripW
		local relY = (uiY - 123.5) / self.MinimapStripH
		if relX < 0 or relX > 1 or relY < 0 or relY > 1 then return end
		local cols = _RtsConfigLogic:GetZoneCols()
		local rows = _RtsConfigLogic:GetZoneRows()
		local col = math.min(cols - 1, math.floor(relX * cols))
		local rowFromBottom = math.min(rows - 1, math.floor(relY * rows))
		local row = rows - 1 - rowFromBottom   -- 0=윗줄
		local zone = row * cols + col + 1
		self.AnchorEntity.RtsCameraAnchorComponent:JumpToZone(zone)
	end
```
(삭제: UpdateMinimapViewport(매 프레임 카메라 추적) — UpdateMinimapZone으로 대체. 기존 자유 좌표 점프 로직 제거)

---

## Test Cases
> Play Test 시나리오 (`maker_save → logs(build) → play → logs·screenshot → stop`).

```
[SUCCESS] 입장 시 카메라가 구역 1 중앙(24,42)에 위치, 이웃 구역 미노출 (스크린샷)
[SUCCESS] F1~F8 각 키로 8구역 중앙 이동 (좌표 로그 + 하이라이트 이동)
[SUCCESS] 미니맵: 192:56 스트립 + 구역 경계선 + 번호 1~8 + 현재 구역 하이라이트 렌더
[SUCCESS] 미니맵 임의 지점 클릭 → 해당 '구역' 중앙으로 스냅 (실마우스)
[FAIL:removed] 방향키/엣지 스크롤로 카메라가 움직이지 않음, 휠 줌 무효, 커서 가두기 없음
[FAIL:boundary] F9 등 무효 키·스트립 밖 클릭 무시
[SUCCESS] 바닥 타일이 새 맵(192×56, 168타일)을 정확히 덮음 (구석 포함)
```
DataStorage 미사용 → [SMOKE] 해당 없음.

---

## Response Codes
| Outcome | Cause |
|------|------|
| 카메라 구역 중앙 순간이동 + 하이라이트 갱신 | F1~F8 / 미니맵 구역 클릭 |
| 무시 | 무효 구역 번호, 스트립 밖 클릭 |
| 카메라 정지 상태 유지 | 방향키/마우스 이동 입력 (자유 카메라 제거됨) |

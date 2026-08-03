# Plan — 스타식 HUD 셸 (rts-base #14)

## Feature Summary
- **Feature**: 스타식 하단 콘솔 바(미니맵+선택정보+커맨드카드 틀) + 우상단 자원/시간 자리, 미니맵 뷰포트·클릭 점프
- **Entry point**: `RtsHudLogic`(클라 조립) ← `RtsCameraAnchorComponent.SetupClient()` 훅 / UI는 `/ui/DefaultGroup/RtsHud` 하위 런타임 스폰
- **Domain**: rts-base

---

## Prerequisites
- [x] **Maker 실행 + msw-maker-mcp 연결** — 연결 확인(2026-08-02)
- [x] **UI 기본 모델 entry id 실증(2026-08-02)** — Image=`model://uisprite`, Button=`model://uibutton`, Text=`model://uitext`, Group=`model://uigroup`. 클라 컨텍스트 SpawnByModelId 동작 확인. 주의: /ui/DefaultGroup은 존재하지 않음(지연 생성) → 런타임에 `RtsHudGroup`(uigroup) 스폰 + UIGroupComponent.DefaultShow. UISprite는 ImageRUID 지정 전까지 비가시.
- [x] **ConnectEvent 실증(부분, 2026-08-02)** — 엔티티 레벨 `ConnectEvent(ButtonClickEvent, fn)` 호출 성공(컴포넌트 레벨은 nil이라 금지). 일회성 MakerScript 컨텍스트에선 발화 미확인 → 영속 Logic에서 연결해 Play Test로 최종 검증. 커맨드카드에 KeyCode 그리드 단축키(QWER/ASDF/ZXCV)를 병행 배선(검증 수단 겸 스타식 UX). 그래도 실패 시 화면좌표 히트테스트 폴백.

---

## File List

| File | Action |
|------|------|
| `RootDesk/MyDesk/RtsHudLogic.mlua` | new (HUD 조립·미니맵 로직 전체) |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | modified (HUD 훅 + UI 위 엣지스크롤 가드 + 뷰포트 갱신 호출) |
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | modified (카메라 뷰 크기 상수·게터 추가) |

---

## Design

> 근거: UI 계층·기본 모델 구성(공식 문서), UITransform/SpriteGUIRenderer/Button/Text 프로퍼티(Environment/NativeScripts/Component/*.d.mlua), 기존 코드 통합 지점 RtsCameraAnchorComponent.mlua:26-46(SetupClient)·48-95(OnUpdate). UI 좌표 1920×1080, 스크린px↔UI 변환은 ScreenWidth/Height 비율 — 원점 차이는 빌드 시 클릭 로그로 캘리브레이션(스펙 Notes).

### Config (RtsConfigLogic.mlua — 추가분)

```lua
	property number CameraViewWidth = 44.5

	property number CameraViewHeight = 25

	method number GetCameraViewWidth()
		return self.CameraViewWidth
	end

	method number GetCameraViewHeight()
		return self.CameraViewHeight
	end
```

### Business Logic (RtsHudLogic.mlua — new)

```lua
@Logic
script RtsHudLogic extends Logic

	property boolean Built = false

	-- 레이아웃 상수 (UI 좌표 1920×1080 기준, Play Test 튜닝)
	property number BarHeight = 240
	property number MinimapSize = 220
	property number MinimapMargin = 10

	-- 런타임 참조
	property Entity HudRoot = nil
	property Entity ViewportRect = nil
	property Entity AnchorEntity = nil
	property string ImageModelId = ""
	property string ButtonModelId = ""
	property string TextModelId = ""

	-- UI 기본 모델 id 해석 (후보 순회 — Prerequisites에서 실증한 조합으로 확정)
	@ExecSpace("ClientOnly")
	method string ResolveUIModelId(string kind)
		local candidates = {}
		if kind == "Image" then candidates = { "MODImage", "Image", "UIImage" }
		elseif kind == "Button" then candidates = { "MODButton", "Button", "UIButton" }
		elseif kind == "Text" then candidates = { "MODText", "Text", "UIText" }
		end
		for _, name in ipairs(candidates) do
			local id = _EntryService:GetModelIdByName(name)
			if id ~= nil and id ~= "" then return id end
		end
		log("RtsHud: UI model not found for " .. kind)
		return ""
	end

	-- 공통 스폰 헬퍼: 앵커/피벗/크기/위치 지정
	@ExecSpace("ClientOnly")
	method Entity SpawnUI(string modelId, string name, Entity parent, Vector2 anchor, Vector2 pivot, Vector2 pos, Vector2 size)
		local e = _SpawnService:SpawnByModelId(modelId, name, Vector3.zero, parent)
		if e == nil then return nil end
		local t = e.UITransformComponent
		t.AnchorsMin = anchor
		t.AnchorsMax = anchor
		t.Pivot = pivot
		t.anchoredPosition = pos
		t.RectSize = size
		return e
	end

	@ExecSpace("ClientOnly")
	method void Tint(Entity e, number r, number g, number b, number a)
		local sr = e.SpriteGUIRendererComponent
		if sr ~= nil then sr.Color = Color(r, g, b, a) end
	end

	-- HUD 1회 조립 (RtsCameraAnchorComponent.SetupClient에서 호출)
	@ExecSpace("ClientOnly")
	method void BuildHud(Entity anchorEntity)
		if self.Built then return end
		self.AnchorEntity = anchorEntity
		self.ImageModelId = self:ResolveUIModelId("Image")
		self.ButtonModelId = self:ResolveUIModelId("Button")
		self.TextModelId = self:ResolveUIModelId("Text")
		if self.ImageModelId == "" then return end
		local uiRoot = _EntityService:GetEntityByPath("/ui/DefaultGroup")
		if uiRoot == nil then log("RtsHud: DefaultGroup not found") return end

		-- 하단 콘솔 바 (가로 전체, 어두운 패널)
		local bar = self:SpawnUI(self.ImageModelId, "RtsHudBar", uiRoot,
			Vector2(0.5, 0), Vector2(0.5, 0), Vector2(0, 0), Vector2(1920, self.BarHeight))
		self:Tint(bar, 0.08, 0.09, 0.12, 0.92)
		self.HudRoot = bar

		-- 미니맵 (바닥 텍스처 축소판) — 좌측
		local mm = self:SpawnUI(self.ImageModelId, "RtsMinimap", bar,
			Vector2(0, 0), Vector2(0, 0), Vector2(self.MinimapMargin, self.MinimapMargin), Vector2(self.MinimapSize, self.MinimapSize))
		local mmSprite = mm.SpriteGUIRendererComponent
		mmSprite.ImageRUID = DataRef("e9683cc55ec14f05b9c93a19f73fb74e")  -- #1 동굴 바닥 텍스처
		mmSprite.Color = Color(0.75, 0.78, 0.85, 1)

		-- 미니맵 클릭 버튼 (투명 오버레이, 전체 덮음)
		local mmBtn = self:SpawnUI(self.ButtonModelId, "RtsMinimapClick", mm,
			Vector2(0.5, 0.5), Vector2(0.5, 0.5), Vector2(0, 0), Vector2(self.MinimapSize, self.MinimapSize))
		self:Tint(mmBtn, 1, 1, 1, 0.02)
		mmBtn.ButtonComponent:ConnectEvent(ButtonClickEvent, function(event)
			self:OnMinimapClick()
		end)

		-- 카메라 뷰포트 사각형 (미니맵 위, 반투명 흰색)
		local vw = self.MinimapSize * _RtsConfigLogic:GetCameraViewWidth() / _RtsConfigLogic:GetMapCellsX()
		local vh = self.MinimapSize * _RtsConfigLogic:GetCameraViewHeight() / _RtsConfigLogic:GetMapCellsY()
		local vp = self:SpawnUI(self.ImageModelId, "RtsMinimapViewport", mm,
			Vector2(0, 0), Vector2(0.5, 0.5), Vector2(0, 0), Vector2(vw, vh))
		self:Tint(vp, 1, 1, 1, 0.35)
		self.ViewportRect = vp

		-- 선택 정보 패널 (중앙)
		local info = self:SpawnUI(self.ImageModelId, "RtsSelectionPanel", bar,
			Vector2(0.5, 0), Vector2(0.5, 0), Vector2(0, self.MinimapMargin), Vector2(700, self.BarHeight - 20))
		self:Tint(info, 0.13, 0.15, 0.19, 1)
		local infoText = self:SpawnUI(self.TextModelId, "RtsSelectionText", info,
			Vector2(0.5, 0.5), Vector2(0.5, 0.5), Vector2(0, 0), Vector2(660, 40))
		infoText.TextComponent.Text = "선택된 유닛 없음"
		infoText.TextComponent.FontColor = Color(0.75, 0.78, 0.85, 1)

		-- 커맨드 카드 (우측 3×4 슬롯)
		local cardW = 4 * 70 + 20
		local cardH = 3 * 70 + 20
		local card = self:SpawnUI(self.ImageModelId, "RtsCommandCard", bar,
			Vector2(1, 0), Vector2(1, 0), Vector2(-self.MinimapMargin, self.MinimapMargin), Vector2(cardW, cardH))
		self:Tint(card, 0.13, 0.15, 0.19, 1)
		for row = 0, 2 do
			for col = 0, 3 do
				local slot = row * 4 + col + 1
				local btn = self:SpawnUI(self.ButtonModelId, "RtsCmd" .. tostring(slot), card,
					Vector2(0, 0), Vector2(0, 0),
					Vector2(10 + col * 70, 10 + (2 - row) * 70), Vector2(64, 64))
				self:Tint(btn, 0.22, 0.25, 0.31, 1)
				btn.ButtonComponent:ConnectEvent(ButtonClickEvent, function(event)
					self:OnCommandSlot(slot)
				end)
			end
		end

		-- 우상단 자원/시간 자리
		local top = self:SpawnUI(self.ImageModelId, "RtsTopBar", uiRoot,
			Vector2(1, 1), Vector2(1, 1), Vector2(-10, -10), Vector2(360, 44))
		self:Tint(top, 0.08, 0.09, 0.12, 0.85)
		local topText = self:SpawnUI(self.TextModelId, "RtsTopText", top,
			Vector2(0.5, 0.5), Vector2(0.5, 0.5), Vector2(0, 0), Vector2(340, 36))
		topText.TextComponent.Text = "골드 0   --:--"
		topText.TextComponent.FontColor = Color(0.95, 0.85, 0.4, 1)

		self.Built = true
	end

	-- 매 프레임: 카메라 위치 → 미니맵 뷰포트 사각형 위치
	@ExecSpace("ClientOnly")
	method void UpdateMinimapViewport(Vector3 camPos)
		if not self.Built or self.ViewportRect == nil then return end
		local mx = camPos.x / _RtsConfigLogic:GetMapCellsX() * self.MinimapSize
		local my = camPos.y / _RtsConfigLogic:GetMapCellsY() * self.MinimapSize
		self.ViewportRect.UITransformComponent.anchoredPosition = Vector2(mx, my)
	end

	-- 미니맵 클릭 → 카메라 점프 (스크린px → UI → 미니맵 상대 → 월드, 마진 클램프)
	@ExecSpace("ClientOnly")
	method void OnMinimapClick()
		if self.AnchorEntity == nil then return end
		local cursor = _InputService:GetCursorPosition()
		local uiX = cursor.x * 1920 / _UILogic.ScreenWidth
		local uiY = cursor.y * 1080 / _UILogic.ScreenHeight
		local relX = (uiX - self.MinimapMargin) / self.MinimapSize
		local relY = (uiY - self.MinimapMargin) / self.MinimapSize
		if relX < 0 or relX > 1 or relY < 0 or relY > 1 then return end
		local mx = _RtsConfigLogic:GetCameraMarginX()
		local my = _RtsConfigLogic:GetCameraMarginY()
		local wx = math.max(mx, math.min(relX * _RtsConfigLogic:GetMapCellsX(), _RtsConfigLogic:GetMapCellsX() - mx))
		local wy = math.max(my, math.min(relY * _RtsConfigLogic:GetMapCellsY(), _RtsConfigLogic:GetMapCellsY() - my))
		self.AnchorEntity.KinematicbodyComponent:SetWorldPosition(Vector2(wx, wy))
	end

	-- 커맨드 카드 슬롯 (이후 유닛에서 실기능 바인딩)
	@ExecSpace("ClientOnly")
	method void OnCommandSlot(number slot)
		log("RtsHud: command slot " .. tostring(slot) .. " (미구현)")
	end

end
```

### Entry Point 통합 (RtsCameraAnchorComponent.mlua — 변경분)

```lua
	-- SetupClient 끝에 추가:
		_RtsHudLogic:BuildHud(self.Entity)

	-- OnUpdate 첫 줄(LocalPlayer 가드 직후)에 추가 — 입력 없어도 뷰포트는 갱신:
		_RtsHudLogic:UpdateMinimapViewport(self.Entity.TransformComponent.WorldPosition)

	-- 엣지 스크롤 블록 조건 변경 (UI 위 커서면 엣지 스크롤 무시 — 스타 동작):
		if not _InputService:IsPointerOverUI()
			and cursor.x >= 0 and cursor.x <= w and cursor.y >= 0 and cursor.y <= h then
			... (기존 엣지 분기 그대로)
		end
```

---

## Test Cases
> CLI 러너 없음(docs/testing.md) — Play Test 시나리오. `maker_save → logs(build) → play → logs(normal)·screenshot → stop`.

```
[SUCCESS] 게임 입장 시 하단 콘솔 바·미니맵·커맨드카드 12슬롯·선택패널·우상단 표시가 모두 렌더 (스크린샷)
[SUCCESS] 방향키/엣지 스크롤 시 미니맵 뷰포트 사각형이 카메라를 따라 이동
[SUCCESS] 미니맵 클릭 → 해당 월드 지점으로 카메라 즉시 점프 (클릭 좌표 캘리브레이션 로그로 오차 확인)
[SUCCESS] 커맨드카드 슬롯 클릭 → "command slot N" 로그
[FAIL:boundary] 미니맵 가장자리(맵 밖 상당) 클릭 → 카메라 마진(26×15)으로 클램프되어 맵 밖 미표시
[FAIL:input] 커서가 HUD 위에 있을 때 엣지 스크롤 미발동(키보드 스크롤은 동작)
[FAIL:idempotent] BuildHud 중복 호출(재입장 등) 시 HUD 중복 생성 없음 (Built 가드)
```
DataStorage 미사용 → [SMOKE:data-access] 해당 없음.

---

## Response Codes
> 진입점별 결과 계약.

| Outcome | Cause |
|------|------|
| HUD 상시 표시(클라 로컬) | SetupClient 1회 조립 |
| 뷰포트 사각형 위치 갱신 | 매 프레임 카메라 위치 |
| 카메라 점프(마진 클램프) | 미니맵 클릭 |
| "command slot N" 로그 | 커맨드카드 클릭 (실기능은 #4/#9) |
| 엣지 스크롤 무시 | 커서가 UI 위 (IsPointerOverUI) |
| HUD 조립 스킵 + 로그 | UI 모델 id 미해석 (Prerequisites 폴백 경로로 전환) |

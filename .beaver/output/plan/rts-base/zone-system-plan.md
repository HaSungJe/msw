# Plan — 구역 시스템 (운빨 디펜스 #4)

## Feature Summary
- **Feature**: 8구역 구획·시각화 + 스타디움 트랙(11시 스폰·반시계) + 안쪽 배치 슬롯 + 유저→구역 배정
- **Entry point**: `RtsZoneLogic`(배정·좌표·시각화) ← `RtsBootstrapLogic`(입장) / `RtsCameraAnchorComponent`(배정 구역 점프)
- **Domain**: rts-base

> ⚠️ **빌드 중 설계 변경 (2026-08-18)** — 아래 Design 코드 블록은 **초안**이며, 실제 구현은 다음과 같이 달라졌습니다. 확정 사양은 spec을 보세요.
> - **트랙 모양**: 정원 r=12 → **스타디움(라운드 사각형) 외곽 35×12.77, 코너 반경 2.37** (사용자가 스크린샷에 그린 빨간 박스 기준).
> - **트랙 파라미터**: 각도(deg) → **둘레 정규화 t∈[0,1)** (정원이 아니라 등속 이동에 호길이 파라미터 필요). t=0=11시, t 증가=반시계.
> - **배치 슬롯**: 동심 3링 36슬롯 → **10열×3행 30슬롯**(윗줄→아랫줄→가운데줄).
> - **구역 크기**: 48×28 → **40×16** (카메라 뷰 42.66×24, HUD가 하단 31.5%를 가려 실사용 밴드 16.44 — 실측 기반).
> - **렌더 수단**: `LineRendererComponent` → **스프라이트**(LineRenderer가 월드에서 신뢰성 있게 그려지지 않음). 트랙은 업로드한 스타디움 외곽선 텍스처 1장(RUID `b4672b0c52eb4bd4b5a0a22c075b2aea`, scale 4.73), 구역 경계는 얇은 흰 스프라이트 4장.
> - **빈 엔티티 모델**: 후보 전부 부재 → `model://defaultplayer` 폴백. 복제본이 **CameraComponent를 들고 와 활성 카메라를 뺏는** 문제가 있어 스폰 시 비활성 + 클라가 `SwitchCameraTo`로 되찾음.
> - **카메라**: `ConfineCameraArea=false` + `ScreenOffset=(0.5,0.5)`로 앵커를 화면 정중앙에 고정(기본값이면 뷰 중심이 앵커보다 +12.4 어긋남). 줌은 엔진 하한 **30%**.

---

## Prerequisites
- [ ] **Maker 실행 + msw-maker-mcp 연결** (빌드 중 실증·Play Test)
- [ ] **월드 빈 엔티티 모델 id 실증** — Play 컨텍스트에서 `_EntryService:GetModelIdByName` 후보("Empty"/"MODEmpty"/"Object"/"Sprite") 프로브 → `RtsZoneLogic.ResolveWorldModelId`에 반영. 전부 실패 시 폴백: `model://defaultplayer` 스폰 + Avatar/NameTag/Shadow 비활성(#1에서 검증된 수법)
- [ ] **LineRendererComponent 월드 렌더 실증** — 스폰 엔티티에 AddComponent 후 Points/Loop 설정이 화면에 그려지는지 1회 확인. 실패 시 폴백: 선분마다 얇은 SpriteRenderer 사각형 배치

---

## File List

| File | Action |
|------|------|
| `RootDesk/MyDesk/RtsZoneLogic.mlua` | new (구역 배정·트랙/슬롯 좌표·시각화 전체) |
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | modified (트랙 반지름/폭, 스폰 각도 게터 추가) |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | modified (입장 시 구역 배정 + 시각화 멱등 생성 + 배정 통지, 퇴장 시 해제) |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | modified (`JumpToZone(1)` 스텁 → 배정 구역, `ApplyAssignedZone` 수신) |

---

## Design

> 근거: RtsConfigLogic.mlua:4-11(구역 상수)·51-59(GetZoneCenter), RtsBootstrapLogic.mlua(UserEnterEvent + 멱등 EnsureGroundTiles 패턴 — 형제 계약), RtsCameraAnchorComponent.mlua(SetupClient의 `JumpToZone(1)` 스텁 — 교체 대상), LineRendererComponent/LinePoint(Environment/NativeScripts).

### Config (RtsConfigLogic.mlua — 추가분)

```lua
	-- 원형 트랙 (정원, 사용자 확정 r=12) / 몹 스폰 11시 = 120°, 반시계 = 각도 증가
	property number TrackRadius = 12

	property number TrackWidth = 2

	property number SpawnAngleDeg = 120

	method number GetTrackRadius()
		return self.TrackRadius
	end

	method number GetTrackWidth()
		return self.TrackWidth
	end

	method number GetSpawnAngleDeg()
		return self.SpawnAngleDeg
	end
```

### Business Logic (RtsZoneLogic.mlua — new)

```lua
-- rts-base #4: 구역 시스템 — 배정(서버 권위) + 트랙/슬롯 좌표(단일 소스) + 경계·트랙 시각화(서버 1회)
@Logic
script RtsZoneLogic extends Logic

	-- userId → zone(1~8). 서버 권위
	property SyncTable<string, number> ZoneByUser

	property boolean VisualsBuilt = false

	property string WorldModelId = ""

	-- ===== 좌표 변환 (단일 소스) =====

	method number GetZoneCount()
		return _RtsConfigLogic:GetZoneCols() * _RtsConfigLogic:GetZoneRows()
	end

	-- 트랙 위 한 점: 0°=3시, 90°=12시, 120°=11시, 각도 증가 = 반시계
	method Vector2 GetTrackPoint(number zone, number angleDeg)
		local c = _RtsConfigLogic:GetZoneCenter(zone)
		local r = _RtsConfigLogic:GetTrackRadius()
		local rad = angleDeg * math.pi / 180
		return Vector2(c.x + r * math.cos(rad), c.y + r * math.sin(rad))
	end

	method Vector2 GetSpawnPoint(number zone)
		return self:GetTrackPoint(zone, _RtsConfigLogic:GetSpawnAngleDeg())
	end

	-- 배치 슬롯: 트랙 안쪽 동심 3링 (바깥부터 index 1..36)
	method number GetPlacementSlotCount()
		return 36
	end

	method Vector2 GetPlacementSlot(number zone, number index)
		local rings = { { r = 8.5, count = 16 }, { r = 5.5, count = 12 }, { r = 2.5, count = 8 } }
		local c = _RtsConfigLogic:GetZoneCenter(zone)
		local remain = index
		for i = 1, #rings do
			local ring = rings[i]
			if remain <= ring.count then
				local step = 360 / ring.count
				local rad = (90 - (remain - 1) * step) * math.pi / 180
				return Vector2(c.x + ring.r * math.cos(rad), c.y + ring.r * math.sin(rad))
			end
			remain = remain - ring.count
		end
		return c
	end

	-- 배치 가능 영역: 트랙 안쪽 밴드 밖
	method boolean IsInPlacementArea(number zone, Vector2 pos)
		local c = _RtsConfigLogic:GetZoneCenter(zone)
		local inner = _RtsConfigLogic:GetTrackRadius() - _RtsConfigLogic:GetTrackWidth() * 0.5
		local dx = pos.x - c.x
		local dy = pos.y - c.y
		return math.sqrt(dx * dx + dy * dy) < inner - 0.5
	end

	-- ===== 배정 (서버 권위) =====

	@ExecSpace("ServerOnly")
	method number AssignZone(string userId)
		local exist = self.ZoneByUser[userId]
		if exist ~= nil then return exist end
		for n = 1, self:GetZoneCount() do
			if not self:IsZoneOccupied(n) then
				self.ZoneByUser[userId] = n
				self:SetZoneOccupiedVisual(n, true)
				return n
			end
		end
		return 0
	end

	@ExecSpace("ServerOnly")
	method void ReleaseZone(string userId)
		local n = self.ZoneByUser[userId]
		if n == nil then return end
		self.ZoneByUser[userId] = nil
		self:SetZoneOccupiedVisual(n, false)
	end

	method number GetZoneOfUser(string userId)
		local n = self.ZoneByUser[userId]
		if n == nil then return 0 end
		return n
	end

	method boolean IsZoneOccupied(number zone)
		for userId, n in pairs(self.ZoneByUser) do
			if n == zone then return true end
		end
		return false
	end

	-- ===== 시각화 (서버 1회 생성 — 멱등, EnsureGroundTiles 형제 패턴) =====

	@ExecSpace("ServerOnly")
	method string ResolveWorldModelId()
		if self.WorldModelId ~= "" then return self.WorldModelId end
		local candidates = { "Empty", "MODEmpty", "Object", "Sprite" }
		for i = 1, #candidates do
			local id = _EntryService:GetModelIdByName(candidates[i])
			if id ~= nil and id ~= "" then
				self.WorldModelId = id
				return id
			end
		end
		self.WorldModelId = "model://defaultplayer"
		return self.WorldModelId
	end

	@ExecSpace("ServerOnly")
	method Entity SpawnLineEntity(string name, Entity parent, Vector2 at)
		local e = _SpawnService:SpawnByModelId(self:ResolveWorldModelId(), name, Vector3(at.x, at.y, 0), parent)
		if e == nil then return nil end
		if e.AvatarRendererComponent ~= nil then e.AvatarRendererComponent.Enable = false end
		if e.NameTagComponent ~= nil then e.NameTagComponent.Enable = false end
		if e.KinematicbodyComponent ~= nil then e.KinematicbodyComponent.EnableShadow = false end
		if e.LineRendererComponent == nil then e:AddComponent("LineRendererComponent") end
		return e
	end

	@ExecSpace("ServerOnly")
	method void EnsureZoneVisuals()
		if self.VisualsBuilt then return end
		local mapRoot = _EntityService:GetEntityByPath("/maps/RtsMap")
		if mapRoot == nil then return end
		if _EntityService:GetEntityByPath("/maps/RtsMap/ZoneVisual1") ~= nil then
			self.VisualsBuilt = true
			return
		end

		local w = _RtsConfigLogic:GetZoneWidth()
		local h = _RtsConfigLogic:GetZoneHeight()
		local r = _RtsConfigLogic:GetTrackRadius()
		local dim = Color(0.45, 0.38, 0.26, 0.8)
		local trackColor = Color(0.75, 0.68, 0.45, 0.35)

		for n = 1, self:GetZoneCount() do
			local c = _RtsConfigLogic:GetZoneCenter(n)

			-- 구역 경계 사각형
			local border = self:SpawnLineEntity("ZoneVisual" .. tostring(n), mapRoot, c)
			if border ~= nil then
				local bl = border.LineRendererComponent
				bl.Loop = true
				bl.Points:Clear()
				bl.Points:Add(LinePoint(Vector2(0 - w * 0.5, 0 - h * 0.5), dim, 0.25))
				bl.Points:Add(LinePoint(Vector2(w * 0.5, 0 - h * 0.5), dim, 0.25))
				bl.Points:Add(LinePoint(Vector2(w * 0.5, h * 0.5), dim, 0.25))
				bl.Points:Add(LinePoint(Vector2(0 - w * 0.5, h * 0.5), dim, 0.25))
			end

			-- 원형 트랙 (36분할 정원)
			local track = self:SpawnLineEntity("ZoneTrack" .. tostring(n), mapRoot, c)
			if track ~= nil then
				local tl = track.LineRendererComponent
				tl.Loop = true
				tl.Points:Clear()
				for i = 0, 35 do
					local rad = i * 10 * math.pi / 180
					tl.Points:Add(LinePoint(Vector2(r * math.cos(rad), r * math.sin(rad)), trackColor, 0.4))
				end
			end
		end
		self.VisualsBuilt = true
		log("RtsZone: visuals built")
	end

	-- 배정된 구역은 진하게, 빈 구역은 흐리게
	@ExecSpace("Multicast")
	method void SetZoneOccupiedVisual(number zone, boolean occupied)
		local track = _EntityService:GetEntityByPath("/maps/RtsMap/ZoneTrack" .. tostring(zone))
		if track == nil or track.LineRendererComponent == nil then return end
		local a = 0.35
		if occupied then a = 0.9 end
		local pts = track.LineRendererComponent.Points
		for i = 0, pts.Count - 1 do
			local p = pts[i]
			p.Color = Color(0.75, 0.68, 0.45, a)
			pts[i] = p
		end
	end

end
```

### Entry Point (RtsBootstrapLogic.mlua — 변경분)

```lua
	@ExecSpace("ServerOnly")
	@EventSender("Service", "UserService")
	handler HandleUserEnterEvent(UserEnterEvent event)
		local userId = event.UserId
		local userEntity = _UserService:GetUserEntityByUserId(userId)
		if userEntity == nil then return end
		if userEntity.RtsCameraAnchorComponent == nil then
			userEntity:AddComponent("RtsCameraAnchorComponent")
		end
		self:EnsureGroundTiles()
		_RtsZoneLogic:EnsureZoneVisuals()

		-- 구역 배정 후 해당 클라에만 통지 (Client 실행공간 + 마지막 파라미터 UserId 규약)
		local zone = _RtsZoneLogic:AssignZone(userId)
		if zone > 0 then
			userEntity.RtsCameraAnchorComponent:ApplyAssignedZone(zone, userId)
		end
	end

	@ExecSpace("ServerOnly")
	@EventSender("Service", "UserService")
	handler HandleUserLeaveEvent(UserLeaveEvent event)
		_RtsZoneLogic:ReleaseZone(event.UserId)
	end
```

### Entry Point (RtsCameraAnchorComponent.mlua — 변경분)

```lua
	property number MyZone = 1

	-- SetupClient 끝 스텁 교체: JumpToZone(1) → JumpToZone(self.MyZone)
	--   서버 통지가 먼저 오면 MyZone이 이미 세팅돼 있고, 늦게 오면 ApplyAssignedZone이 재점프

	@ExecSpace("Client")
	method void ApplyAssignedZone(number zone, string userId)
		self.MyZone = zone
		self:JumpToZone(zone)
	end
```

---

## Test Cases
> Play Test 시나리오 (`maker_save → logs(build) → play → logs·screenshot → stop`). CLI 러너 없음(docs/testing.md).

```
[SUCCESS] 8구역 경계선 + 스타디움 트랙이 각 구역 중앙에 렌더 (F1/F4/F8 스크린샷)
[SUCCESS] GetSpawnPoint(zone) = 구역 중앙 기준 11시(x 작고 y 큼)
[SUCCESS] t 증가 = 반시계 — t=0 → t=0.02 이동 방향이 좌하(좌변 하강)
[SUCCESS] 트랙 위 200개 샘플의 TrackSignedDistance ≈ 0 (형상 일관성)
[SUCCESS] 입장 시 자동 배정(첫 유저 = 구역 1) + 카메라가 그 구역으로 이동
[SUCCESS] 배정 구역 트랙은 진하게(alpha 1.0), 빈 구역은 흐리게(0.45)
[SUCCESS] GetPlacementSlot 30개 전부 IsInPlacementArea = true
[SUCCESS] 같은 userId 재배정 = 같은 구역(멱등)
[FAIL:full] 8구역 만석 상태에서 AssignZone → 0 반환(중복 배정 없음)
[SUCCESS] 해제한 구역이 다음 배정에 재사용됨
[SUCCESS] 재호출에도 시각화 중복 생성 없음(VisualsBuilt 멱등)
[SUCCESS] 미니맵 2×4 셀 → 구역 번호 매핑이 GetZoneCenter 배치와 일치
```
DataStorage 미사용 → [SMOKE:data-access] 해당 없음.

---

## Response Codes
| Outcome | Cause |
|------|------|
| 구역 번호(1~8) + 카메라 자동 이동 | 유저 입장(빈 구역 있음) |
| 0 반환 | 8구역 만석 (관전 처리는 #10) |
| 구역 해제 + 트랙 흐려짐 | 유저 퇴장 |
| 월드 좌표 반환 | GetTrackPoint / GetSpawnPoint / GetPlacementSlot |
| true/false | IsInPlacementArea, IsZoneOccupied |
| 생성 스킵 | 시각화 이미 존재(멱등) 또는 맵 루트 없음 |

local logic=_RtsActionThemeLogic
local host=_RtsBoardViewLogic:BoardChild("ZoneBackground"..string.format("%d",_RtsHudLogic.WatchedZone))
if not isvalid(host) then log("[MOTION] FAIL missing world background") return end
local original=host.SpriteRendererComponent.SpriteRUID
local photo=nil
local passed=0
local resources={}
local function snap(e,ui)
 if ui then local t=e.UITransformComponent return tostring(t.anchoredPosition)..tostring(t.RectSize)..tostring(t.UIRotation)..tostring(e.SpriteGUIRendererComponent.Color) end
 local t=e.TransformComponent return tostring(t.Position)..tostring(t.Scale)..tostring(t.ZRotation)..tostring(e.SpriteRendererComponent.Color)
end
local ok,err=pcall(function()
 for _,d in ipairs(logic:GetDefinitions()) do
  local rig=logic:GetRig(d.key)
  if rig==nil then error("missing rig "..d.key) end
  resources[d.background]=true
  for _,p in ipairs(rig.parts) do resources[p.ruid]=true end
 end
 local loaded,total,metadataErrors=0,0,0
 for ruid,_ in pairs(resources) do
  total=total+1
  local sprite=_ResourceService:LoadSpriteAndWait(ruid)
  if sprite~=nil and sprite.IsLoadComplete and sprite.Width>0 and sprite.Height>0 then
   loaded=loaded+1
   local expected=logic:GetPartSize(ruid)
   if expected~=nil and (sprite.Width~=expected.w or sprite.Height~=expected.h or math.abs(sprite.PixelPerUnit-100)>0.01 or math.abs(sprite.Pivot.x-0.5)>0.001 or math.abs(sprite.Pivot.y-0.5)>0.001) then metadataErrors=metadataErrors+1 log("[MOTION] METADATA "..ruid.." "..sprite.Width.."x"..sprite.Height.." pivot="..tostring(sprite.Pivot).." ppu="..sprite.PixelPerUnit) end
  else log("[MOTION] RESOURCE FAIL "..ruid) end
 end
 log("[MOTION] resources="..loaded.."/"..total.." metadataErrors="..metadataErrors)
 photo=_RtsHudLogic:SpawnUI("model://uisprite","ZzMotionCard",_RtsHudLogic.HudGroup,Vector2(0.5,0.5),Vector2(0.5,0.5),Vector2(0,0),Vector2(320,180))
 photo.SpriteGUIRendererComponent.RaycastTarget=false
 photo.SpriteGUIRendererComponent.Type=ImageType.Simple
 for _,d in ipairs(logic:GetDefinitions()) do
  host.SpriteRendererComponent.SpriteRUID=d.background
  logic:RegisterCard(photo,d.key,320)
  wait(0.7)
  local worldScene,cardScene=nil,nil
  for _,s in ipairs(logic.Scenes) do if s.host==host then worldScene=s elseif s.host==photo then cardScene=s end end
  if worldScene==nil or cardScene==nil then error("missing scene "..d.key) end
  local beforeW,beforeU={},{}
  for _,p in ipairs(worldScene.parts) do if p.rig~=nil then beforeW[p.rig.id]=snap(p.entity,false) end end
  for _,p in ipairs(cardScene.parts) do if p.rig~=nil then beforeU[p.rig.id]=snap(p.entity,true) end end
  local bg=snap(host,false)
  wait(0.67)
  local movedW,movedU,validW,validU=0,0,0,0
  for _,p in ipairs(worldScene.parts) do if p.rig~=nil and isvalid(p.entity) then validW=validW+1 if beforeW[p.rig.id]~=snap(p.entity,false) then movedW=movedW+1 end end end
  for _,p in ipairs(cardScene.parts) do if p.rig~=nil and isvalid(p.entity) then validU=validU+1 if beforeU[p.rig.id]~=snap(p.entity,true) then movedU=movedU+1 end end end
  local fixed=bg==snap(host,false)
  local n=#logic:GetRig(d.key).parts
  local pass=validW==n and validU==n and movedW>0 and movedU>0 and fixed
  if pass then passed=passed+1 end
  log("[MOTION] "..d.key.." world="..validW.."/"..n.." moving="..movedW.." card="..validU.."/"..n.." moving="..movedU.." backgroundFixed="..tostring(fixed).." pass="..tostring(pass))
 end
end)
if isvalid(photo) then photo:Destroy() end
if isvalid(host) then host.SpriteRendererComponent.SpriteRUID=original end
wait(0.8)
local leftovers=0
for _,s in ipairs(logic.Scenes) do if s.host==photo then leftovers=leftovers+1 end end
log("[MOTION] COMPLETE passed="..passed.."/17 cleanup="..tostring(leftovers==0).." ok="..tostring(ok).." error="..tostring(err))

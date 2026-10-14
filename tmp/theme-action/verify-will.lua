local logic=_RtsActionThemeLogic
local host=_RtsBoardViewLogic:BoardChild("ZoneBackground"..string.format("%d",_RtsHudLogic.WatchedZone))
if not isvalid(host) then log("[WILL] FAIL missing world background") return end
local original=host.SpriteRendererComponent.SpriteRUID
local photo=nil
local passed=0
local oldState=_RtsStageLogic.RunState
local oldNo=_RtsStageLogic.StageNo
local oldBgm=_RtsStageLogic.BgmNow
local resources={}
local function snap(e,ui)
 if ui then local t=e.UITransformComponent return tostring(t.anchoredPosition)..tostring(t.RectSize)..tostring(t.UIRotation)..tostring(e.SpriteGUIRendererComponent.Color) end
 local t=e.TransformComponent return tostring(t.Position)..tostring(t.Scale)..tostring(t.ZRotation)..tostring(e.SpriteRendererComponent.Color)
end
local ok,err=pcall(function()
 local stage=_RtsStageTableLogic:GetStage(110)
 if stage.name~="바스러지는 빛" or stage.bgm~="bd23d2f87d734f8ca52ca8824d1b6ff4" then error("stage BGM/name mismatch") end
 _RtsStageLogic.RunState="running"
 _RtsStageLogic.StageNo=110
 _RtsStageLogic:RefreshBgm(stage)
 wait(2)
 if _RtsStageLogic.BgmNow~=stage.bgm or not _SoundService:IsPlayBGM() then error("BGM not playing") end
 log("[WILL] BGM playing=".._RtsStageLogic.BgmNow.." stage="..stage.name)
 for _,key in ipairs({"diffraction_hall"}) do
 local d=logic:GetDefinition(key)
  local rig=logic:GetRig(d.key)
  if rig==nil then error("missing rig "..d.key) end
  if d.name~="바스러지는 빛" then error("theme name mismatch") end
  resources[d.thumb]=true
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
   if expected~=nil and (sprite.Width~=expected.w or sprite.Height~=expected.h or math.abs(sprite.PixelPerUnit-100)>0.01 or math.abs(sprite.Pivot.x-0.5)>0.001 or math.abs(sprite.Pivot.y-0.5)>0.001) then metadataErrors=metadataErrors+1 log("[WILL] METADATA "..ruid.." "..sprite.Width.."x"..sprite.Height.." pivot="..tostring(sprite.Pivot).." ppu="..sprite.PixelPerUnit) end
  else log("[WILL] RESOURCE FAIL "..ruid) end
 end
 log("[WILL] resources="..loaded.."/"..total.." metadataErrors="..metadataErrors)
 photo=_RtsHudLogic:SpawnUI("model://uisprite","ZzMotionCard",_RtsHudLogic.HudGroup,Vector2(0.5,0.5),Vector2(0.5,0.5),Vector2(0,0),Vector2(320,180))
 photo.SpriteGUIRendererComponent.RaycastTarget=false
 photo.SpriteGUIRendererComponent.Type=ImageType.Simple
 for _,key in ipairs({"diffraction_hall"}) do
 local d=logic:GetDefinition(key)
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
  local legsW,legsU=0,0
  for _,p in ipairs(worldScene.parts) do if p.rig and string.sub(p.rig.id,1,4)=="leg-" and beforeW[p.rig.id]~=snap(p.entity,false) then legsW=legsW+1 end end
  for _,p in ipairs(cardScene.parts) do if p.rig and string.sub(p.rig.id,1,4)=="leg-" and beforeU[p.rig.id]~=snap(p.entity,true) then legsU=legsU+1 end end
  if legsW~=8 or legsU~=8 then error("leg animation mismatch") end
  log("[WILL] movingLegs world="..legsW.." card="..legsU)
  local n=#logic:GetRig(d.key).parts
  local pass=validW==n and validU==n and movedW>0 and movedU>0 and fixed
  if pass then passed=passed+1 end
  log("[WILL] "..d.key.." world="..validW.."/"..n.." moving="..movedW.." card="..validU.."/"..n.." moving="..movedU.." backgroundFixed="..tostring(fixed).." pass="..tostring(pass))
 end
end)
_RtsStageLogic.RunState=oldState
_RtsStageLogic.StageNo=oldNo
_RtsStageLogic.BgmNow=oldBgm
if oldBgm~="" then _SoundService:PlayBGM(oldBgm,_RtsStageLogic.BgmVolume) else _SoundService:StopBGM(true) end
if isvalid(photo) then photo:Destroy() end
if isvalid(host) then host.SpriteRendererComponent.SpriteRUID=original end
wait(0.8)
local leftovers=0
for _,s in ipairs(logic.Scenes) do if s.host==photo then leftovers=leftovers+1 end end
log("[WILL] COMPLETE passed="..passed.."/1 cleanup="..tostring(leftovers==0).." ok="..tostring(ok).." error="..tostring(err))

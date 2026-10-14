local logic=_RtsActionThemeLogic
local host=_RtsBoardViewLogic:BoardChild("ZoneBackground"..string.format("%d",_RtsHudLogic.WatchedZone))
if not isvalid(host) then log("[EDGE3] FAIL missing world background") return end
local original=host.SpriteRendererComponent.SpriteRUID
local photo=nil
local passed=0
local resources={}
local function snap(e,ui)
 if ui then local t=e.UITransformComponent return tostring(t.anchoredPosition)..tostring(t.RectSize)..tostring(t.UIRotation)..tostring(e.SpriteGUIRendererComponent.Color) end
 local t=e.TransformComponent return tostring(t.Position)..tostring(t.Scale)..tostring(t.ZRotation)..tostring(e.SpriteRendererComponent.Color)
end
local ok,err=pcall(function()
 for _,key in ipairs({"world_tree_summit"}) do
 local d=logic:GetDefinition(key)
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
   if expected~=nil and (sprite.Width~=expected.w or sprite.Height~=expected.h or math.abs(sprite.PixelPerUnit-100)>0.01 or math.abs(sprite.Pivot.x-0.5)>0.001 or math.abs(sprite.Pivot.y-0.5)>0.001) then metadataErrors=metadataErrors+1 log("[EDGE3] METADATA "..ruid.." "..sprite.Width.."x"..sprite.Height.." pivot="..tostring(sprite.Pivot).." ppu="..sprite.PixelPerUnit) end
  else log("[EDGE3] RESOURCE FAIL "..ruid) end
 end
 log("[EDGE3] resources="..loaded.."/"..total.." metadataErrors="..metadataErrors)
 photo=_RtsHudLogic:SpawnUI("model://uisprite","ZzMotionCard",_RtsHudLogic.HudGroup,Vector2(0.5,0.5),Vector2(0.5,0.5),Vector2(0,0),Vector2(320,180))
 photo.SpriteGUIRendererComponent.RaycastTarget=false
 photo.SpriteGUIRendererComponent.Type=ImageType.Simple
 for _,key in ipairs({"world_tree_summit"}) do
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
  for _,p in ipairs(worldScene.parts) do if p.rig and p.rig.id=="body" and math.abs(p.entity.SpriteRendererComponent.Color.r-0.28)>0.001 then error("body not darkened") end end

  local wingCount,flameCount,changedW,changedU=0,0,0,0
  for _,p in ipairs(worldScene.parts) do
   local b=p.rig
   if b~=nil then
    if b.frameCount~=nil then error("whole-wing frames remain") end
    if b.id=="wing-l" or b.id=="wing-r" then
     wingCount=wingCount+1
     if math.abs(p.entity.SpriteRendererComponent.Color.r-0.2)>0.001 then error("wing not darkened") end
     if b.amp~=0 or b.sx~=0 or b.sy~=0 or math.abs(p.entity.TransformComponent.ZRotation-(b.id=="wing-l" and 24 or -24))>0.001 or math.abs(p.entity.TransformComponent.Scale.x-0.8)>0.001 then error("wing silhouette not fixed") end
    elseif string.sub(b.id,1,10)=="edge-flame" then
     flameCount=flameCount+1
     if b.flowX==nil or math.abs(b.flowX)<0.7 or b.flowX*(b.x-840)<=0 then error("flame not flowing outwards") end
     if b.rise~=58 or b.k<0.22 or b.k>0.271 then error("oversized border flames") end
     if beforeW[b.id]~=snap(p.entity,false) then changedW=changedW+1 end
    end
   end
  end
  for _,p in ipairs(cardScene.parts) do if p.rig~=nil and string.sub(p.rig.id,1,10)=="edge-flame" and beforeU[p.rig.id]~=snap(p.entity,true) then changedU=changedU+1 end end
  if wingCount~=2 or flameCount~=32 or changedW~=32 or changedU~=32 then error("edge motion mismatch "..wingCount.."/"..flameCount.."/"..changedW.."/"..changedU) end
  log("[EDGE3] spread wings=24/-24 dark=0.20 outwardFlow=true flames=32 movingWorld="..changedW.." movingCard="..changedU)
  local n=#logic:GetRig(d.key).parts
  local pass=validW==n and validU==n and movedW>0 and movedU>0 and fixed
  if pass then passed=passed+1 end
  log("[EDGE3] "..d.key.." world="..validW.."/"..n.." moving="..movedW.." card="..validU.."/"..n.." moving="..movedU.." backgroundFixed="..tostring(fixed).." pass="..tostring(pass))
 end
end)
if isvalid(photo) then photo:Destroy() end
if isvalid(host) then host.SpriteRendererComponent.SpriteRUID=original end
wait(0.8)
local leftovers=0
for _,s in ipairs(logic.Scenes) do if s.host==photo then leftovers=leftovers+1 end end
log("[EDGE3] COMPLETE passed="..passed.."/1 cleanup="..tostring(leftovers==0).." ok="..tostring(ok).." error="..tostring(err))

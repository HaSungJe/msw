local map=_EntityService:GetEntityByPath("/maps/RtsMap")
local old=map:GetChildByName("HeroMotionQA") if isvalid(old) then old:Destroy() end
local at=_RtsZoneLogic:GetCellCenter(_RtsUnitLogic:MyZone(),7,3)
local e=_SpawnService:SpawnByModelId("model://MapObject","HeroMotionQA",Vector3(at.x,at.y-0.75,0),map)
if e==nil then log("[HERO_ENRAGE] spawn failed") return end
e:RemoveComponent("SpriteRendererComponent")
e.TransformComponent.Scale=Vector3(2,2,1)
local u=e:AddComponent("RtsUnitComponent")
u.JobId="hero" u.Owner=_RtsUnitLogic:MyUserId() u.Zone=_RtsUnitLogic:MyZone() u.No=99997 u.Prisms="enrage"
u:SetupMageSkin()
local fx=nil
for _,skill in ipairs(_RtsJobTableLogic:GetSkillsFor(u)) do if skill.fx~=nil and skill.fx.motion=="enragedRagingBlow" then fx=skill.fx end end
if fx==nil then e:Destroy() log("[HERO_ENRAGE] missing fx") return end
_RtsSkillFxLogic:Preload(fx)
local seenLeft={} local seenRight={} local swordErrors=0 local effectSeen=false
local seq=_RtsJobTableLogic:GetMageSkinFrames("hero").enragedRagingBlow
local watch=0
watch=_TimerService:SetTimerRepeat(function()
 if not isvalid(e) then _TimerService:ClearTimer(watch) return end
 if u.MageSkinAction=="enragedRagingBlow" and isvalid(u.MageSkinEntity) then
  local sr=u.MageSkinEntity.SpriteRendererComponent
  for i,ruid in ipairs(seq) do if sr.SpriteRUID==ruid then
   if sr.FlipX then seenRight[i]=true else seenLeft[i]=true end
  end end
  if isvalid(u.HeroSwordEntity) and u.HeroSwordEntity.Visible then swordErrors=swordErrors+1 end
 end
 local effect=_RtsSkillFxLogic.Active[99997]
 if isvalid(effect) then effectSeen=true end
end,0.01)
for i=1,8 do
 local n=i
 _TimerService:SetTimerOnce(function()
  if not isvalid(e) then return end
  u:SetLocalFace(n<=4 and -1 or 1)
  _RtsSkillFxLogic:PlayCast(e,99997,fx,nil,{})
  log("[HERO_ENRAGE] cast="..tostring(n).." face="..tostring(u:FaceNow()).." clip="..fx.clip)
  _TimerService:SetTimerOnce(function() if isvalid(e) then log("[HERO_ENRAGE] return="..u.MageSkinAction) end end,1.1)
 end,1+(i-1)*2)
end
_TimerService:SetTimerOnce(function()
 _TimerService:ClearTimer(watch)
 local a=0 local b=0 for _ in pairs(seenLeft) do a=a+1 end for _ in pairs(seenRight) do b=b+1 end
 log("[HERO_ENRAGE] left="..tostring(a).."/7 right="..tostring(b).."/7 personalSwordErrors="..tostring(swordErrors).." effectSeen="..tostring(effectSeen))
 if isvalid(e) then e:Destroy() end
 log("[HERO_ENRAGE] cleanup=true")
end,18)

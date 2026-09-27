local map=_EntityService:GetEntityByPath("/maps/RtsMap")
local zone=_RtsUnitLogic:MyZone()
local owner=_RtsUnitLogic:MyUserId()
_RtsPopupLogic:Close()
local H=_RtsHudLogic
local prev=H.HudGroup:GetChildByName("ZzPortraitSet")
if isvalid(prev) then prev:Destroy() end
local panel=H:SpawnRoundedPanel("ZzPortraitSet",H.HudGroup,Vector2(0.5,0.5),Vector2(0.5,0.5),Vector2(0,275),Vector2(960,215),Color(0.96,0.97,1,1),Color(0.7,0.72,0.8,1),1.5)
local jobs={"paladin","dk","nl","shad","phantom"}
for i,job in ipairs(jobs) do
 _RtsUnitPopupLogic:SpawnPreviewAt(panel,{JobId=job},Vector2((i-0.5)*192,-94),Vector2(180,180))
 H:SpawnLabel("Name"..job,panel,Vector2(0,1),Vector2(0.5,1),Vector2((i-0.5)*192,-187),Vector2(180,24),_RtsJobTableLogic:GetJobName(job),Color(0.2,0.22,0.3,1),18,TextAlignmentType.MiddleCenter,false)
end
for index,face in ipairs({-1,1}) do
 local name="ZzPhantomPreview"..tostring(index)
 local old=map:GetChildByName(name)
 if isvalid(old) then old:Destroy() end
 local at=_RtsZoneLogic:GetCellCenter(zone,index==1 and 7 or 12,9)
 local e=_SpawnService:SpawnByModelId("model://MapObject",name,Vector3(at.x,at.y-0.75,0),map)
 e:RemoveComponent("SpriteRendererComponent")
 e.TransformComponent.Scale=Vector3(2,2,1)
 local u=e:AddComponent("RtsUnitComponent")
 u.JobId="phantom" u.Owner=owner u.Zone=zone u.No=99795+index u.Level=50
 u:SetupMageSkin() u:SetLocalFace(face)
 local target=_SpawnService:SpawnByModelId("model://MapObject","Target",Vector3.zero,e)
 target:RemoveComponent("SpriteRendererComponent")
 local fx=nil
 for _,skill in ipairs(_RtsJobTableLogic:GetSkillsFor(u)) do if skill.name=="조커" then fx=skill.fx end end
 _RtsSkillFxLogic:Preload(fx)
 local started=_UtilLogic.ElapsedSeconds
 local timer=0
 timer=_TimerService:SetTimerRepeat(function()
  if not isvalid(e) then _TimerService:ClearTimer(timer) return end
  local phase=(_UtilLogic.ElapsedSeconds-started)%7
  if phase<3 then
   local p=e.TransformComponent.WorldPosition
   target.TransformComponent.WorldPosition=Vector3(p.x+face*5,p.y+0.2,0)
   _RtsSkillFxLogic:PlayCast(e,u.No,fx,target,{target})
  end
 end,0.1,1)
 log("[PHANTOM_PREVIEW] started="..name.." face="..tostring(face).." action="..tostring(fx.motion))
end
log("[PHANTOM_PREVIEW] portraits=5 size=180 autoplay=3sec idle=4sec")

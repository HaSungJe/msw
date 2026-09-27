local map=_EntityService:GetEntityByPath("/maps/RtsMap")
local zone=_RtsUnitLogic:MyZone()
local owner=_RtsUnitLogic:MyUserId()
local configs={
 {name="ZzWarriorMotionPaladin",job="paladin",no=99781,col=7,actions={"paladinCharge","paladinSanctuary"}},
 {name="ZzWarriorMotionDarkKnight",job="dk",no=99782,col=10,actions={"dkBuster","dkRoar"}},
 {name="ZzWarriorMotionGiant",job="dk",no=99783,col=13,actions={"dkGiantBuster"},prism="giant"}
}
_RtsPopupLogic:Close()
for _,c in ipairs(configs) do
 local old=map:GetChildByName(c.name)
 if isvalid(old) then old:Destroy() end
 local at=_RtsZoneLogic:GetCellCenter(zone,c.col,5)
 local e=_SpawnService:SpawnByModelId("model://MapObject",c.name,Vector3(at.x,at.y-0.75,0),map)
 local ok,err=pcall(function()
 e:RemoveComponent("SpriteRendererComponent")
 e.TransformComponent.Scale=Vector3(2,2,1)
 local u=e:AddComponent("RtsUnitComponent")
 u.JobId=c.job u.Owner=owner u.Zone=zone u.No=c.no u.Level=50 u.Prisms=c.prism or ""
 u:SetupMageSkin()
 local effects={}
 for _,skill in ipairs(_RtsJobTableLogic:GetSkillsFor(u)) do
  if skill.fx~=nil then effects[skill.fx.motion]=skill.fx _RtsSkillFxLogic:Preload(skill.fx) end
 end
 local n=0 local timer=0
 local cast=function()
  if not isvalid(e) then if timer~=0 then _TimerService:ClearTimer(timer) end return end
  n=n+1
  local action=c.actions[((n-1)%#c.actions)+1]
  u:SetLocalFace(math.floor((n-1)/#c.actions)%2==0 and -1 or 1)
  _RtsSkillFxLogic:PlayCast(e,c.no,effects[action],nil,{})
  if n<=2 then log("[WARRIOR_PREVIEW] "..c.name.." action="..action.." face="..tostring(u:FaceNow())) end
 end
 timer=_TimerService:SetTimerRepeat(cast,3.5)
 _TimerService:SetTimerOnce(cast,0.6)
 log("[WARRIOR_PREVIEW] started="..c.name.." interval=3.5")
 end)
 if not ok then if isvalid(e) then e:Destroy() end log("[WARRIOR_PREVIEW] error="..tostring(err)) end
end

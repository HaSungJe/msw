local map=_EntityService:GetEntityByPath("/maps/RtsMap")
local zone=_RtsUnitLogic:MyZone()
local owner=_RtsUnitLogic:MyUserId()
local configs={
 {name="ZzThiefNightLord",job="nl",no=99791,col=7,row=5,skills={"쿼드러플 스로우"}},
 {name="ZzThiefFuma",job="nl",no=99792,col=12,row=5,skills={"풍마수리검"},prism="fuma"},
 {name="ZzThiefShadower",job="shad",no=99793,col=7,row=9,skills={"새비지 블로우","메소 익스플로전"}},
 {name="ZzThiefDualblade",job="shad",no=99794,col=12,row=9,skills={"블레이드 토네이도 + 카르마 퓨리"},prism="dualblade"}
}
_RtsPopupLogic:Close()
for _,c in ipairs(configs) do
 local old=map:GetChildByName(c.name)
 if isvalid(old) then old:Destroy() end
 local at=_RtsZoneLogic:GetCellCenter(zone,c.col,c.row)
 local e=_SpawnService:SpawnByModelId("model://MapObject",c.name,Vector3(at.x,at.y-0.75,0),map)
 e:RemoveComponent("SpriteRendererComponent")
 e.TransformComponent.Scale=Vector3(2,2,1)
 local u=e:AddComponent("RtsUnitComponent")
 u.JobId=c.job u.Owner=owner u.Zone=zone u.No=c.no u.Level=50 u.Prisms=c.prism or ""
 u:SetupMageSkin()
 if c.job=="nl" then
  local sh=_SpawnService:SpawnByModelId("model://MapObject","Shadow",Vector3(at.x,at.y-0.75,0),e)
  sh.SpriteRendererComponent.SpriteRUID=_RtsSkillFxLogic:ShadowClip("stand1")
  sh.SpriteRendererComponent.OrderInLayer=-5
  sh.TransformComponent.Scale=Vector3(1,1,1)
  u:ApplyShadow()
 end
 local target=_SpawnService:SpawnByModelId("model://MapObject","Target",Vector3(at.x-5,at.y,0),e)
 target:RemoveComponent("SpriteRendererComponent")
 local effects={}
 for _,k in ipairs(_RtsJobTableLogic:GetSkillsFor(u)) do
  if k.fx~=nil then effects[k.name]=k.fx _RtsSkillFxLogic:Preload(k.fx) end
 end
 local n=0 local timer=0
 local cast=function()
  if not isvalid(e) then if timer~=0 then _TimerService:ClearTimer(timer) end return end
  n=n+1
  local skill=c.skills[((n-1)%#c.skills)+1]
  local face=math.floor((n-1)/#c.skills)%2==0 and -1 or 1
  u:SetLocalFace(face)
  local p=e.TransformComponent.WorldPosition
  target.TransformComponent.WorldPosition=Vector3(p.x+face*5,p.y+0.5,0)
  _RtsSkillFxLogic:PlayCast(e,c.no,effects[skill],target,{target})
  if n<=2 then log("[THIEF_PREVIEW] "..c.name.." skill="..skill.." face="..tostring(face)) end
 end
 timer=_TimerService:SetTimerRepeat(cast,6,3)
 log("[THIEF_PREVIEW] started="..c.name.." interval=6")
end

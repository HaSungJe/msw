local map=_EntityService:GetEntityByPath("/maps/RtsMap")
local unique={} local loaded=0 local failed=0
for _,job in ipairs({"nl","shad"}) do
 local frames=_RtsJobTableLogic:GetMageSkinFrames(job)
 local times=_RtsJobTableLogic:GetMageSkinFrameDurations(job)
 for action,seq in pairs(frames) do
  if #seq~=#times[action] then failed=failed+1 end
  for _,ruid in ipairs(seq) do
   if not unique[ruid] then
    unique[ruid]=true
    local sprite=_ResourceService:LoadSpriteAndWait(ruid)
    if sprite~=nil and sprite.IsLoadComplete then loaded=loaded+1 else failed=failed+1 end
   end
  end
 end
end
log("[THIEF_QA] loaded="..tostring(loaded).."/35 connectionErrors="..tostring(failed))
local configs={
 {name="ZzThiefNightLord",actions={"nlThrow"}},
 {name="ZzThiefFuma",actions={"nlThrow"}},
 {name="ZzThiefShadower",actions={"shadSavage","shadMeso"}},
 {name="ZzThiefDualblade",actions={"shadDualblade"}}
}
local tracks={}
for _,c in ipairs(configs) do
 local e=map:GetChildByName(c.name)
 if isvalid(e) then
  tracks[#tracks+1]={e=e,u=e.RtsUnitComponent,c=c,seen={},lastAction="",returns=0,shadowAttack=false,shadowStand=false,delays={}}
 else log("[THIEF_QA] missing="..c.name) end
end
local timer=0
timer=_TimerService:SetTimerRepeat(function()
 for _,t in ipairs(tracks) do
  if isvalid(t.e) and isvalid(t.u.MageSkinEntity) then
   local sr=t.u.MageSkinEntity.SpriteRendererComponent
   local a=t.u.MageSkinAction
   local key=a..(sr.FlipX and ":R" or ":L")
   if t.seen[key]==nil then t.seen[key]={} end
   t.seen[key][sr.SpriteRUID]=true
   if a~=t.lastAction then
    if a=="stand1" and t.lastAction~="" then t.returns=t.returns+1 end
    if a=="nlThrow" then t.started=_UtilLogic.ElapsedSeconds end
    t.lastAction=a
   end
   local sh=t.e:GetChildByName("Shadow")
   if isvalid(sh) then
    local r=sh.SpriteRendererComponent.SpriteRUID
    if r==_RtsSkillFxLogic:ShadowClip("nlThrow") then
     t.shadowAttack=true
     if r~=t.lastShadow and t.started~=nil then t.delays[#t.delays+1]=string.format("%.3f",_UtilLogic.ElapsedSeconds-t.started) end
    end
    if r==_RtsSkillFxLogic:ShadowClip("stand1") then t.shadowStand=true end
    t.lastShadow=r
   end
  end
 end
end,0.01)
_TimerService:SetTimerOnce(function()
 _TimerService:ClearTimer(timer)
 for _,t in ipairs(tracks) do
  local seqs=_RtsJobTableLogic:GetMageSkinFrames(t.u.JobId)
  for _,a in ipairs(t.c.actions) do
   local expected={} local count=0
   for _,r in ipairs(seqs[a]) do if not expected[r] then expected[r]=true count=count+1 end end
   for _,face in ipairs({":L",":R"}) do
    local seen=0 for _ in pairs(t.seen[a..face] or {}) do seen=seen+1 end
    log("[THIEF_QA] "..t.c.name.." "..a..face.." frames="..tostring(seen).."/"..tostring(count))
   end
  end
  local idle={} local n=0
  for _,face in ipairs({":L",":R"}) do for r in pairs(t.seen["stand1"..face] or {}) do idle[r]=true end end
  for _ in pairs(idle) do n=n+1 end
  log("[THIEF_QA] "..t.c.name.." returns="..tostring(t.returns).." idle="..tostring(n).."/3 avatarAbsent="..tostring(t.e.AvatarRendererComponent==nil))
  if t.u.JobId=="nl" then log("[THIEF_QA] "..t.c.name.." shadowAttack="..tostring(t.shadowAttack).." shadowStand="..tostring(t.shadowStand).." shadowDelays="..table.concat(t.delays,",")) end
 end
 log("[THIEF_QA] complete")
end,31)

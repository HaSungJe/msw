local zone=_RtsUnitLogic:MyZone()
local setups={{99871,{"paladinCharge","paladinSanctuary"}},{99872,{"dkBuster","dkRoar"}},{99873,{"dkGiantBuster"}}}
for _,setup in ipairs(setups) do
 local no=setup[1] local u=_RtsUnitLogic:GetZoneUnit(zone,no)
 if u==nil then log("[WARRIOR_QA] missing="..tostring(no)) else
 local e=u.Entity
 local actions=setup[2] local durations=_RtsJobTableLogic:GetMageSkinFrameDurations(u.JobId)
 local seqs=_RtsJobTableLogic:GetMageSkinFrames(u.JobId)
 local fxByAction={}
 for _,k in ipairs(_RtsJobTableLogic:GetSkillsFor(u)) do if k.fx~=nil then fxByAction[k.fx.motion]=k.fx end end
 local seen={} local order={} local errors=0 local returns=0 local effect=false local watch=0
 watch=_TimerService:SetTimerRepeat(function()
  if not isvalid(e) then _TimerService:ClearTimer(watch) return end
  if isvalid(u.MageSkinEntity) then
   local sr=u.MageSkinEntity.SpriteRendererComponent
   local key=u.MageSkinAction..(sr.FlipX and ":R" or ":L")
   if seen[key]==nil then seen[key]={} order[key]={} end
   seen[key][sr.SpriteRUID]=true
   local list=order[key]
   if list[#list]~=sr.SpriteRUID then list[#list+1]=sr.SpriteRUID end
  end
  if isvalid(_RtsSkillFxLogic.Active[no]) then effect=true end
 end,0.01)
 for n=1,8 do
  local cast=n
  _TimerService:SetTimerOnce(function()
   if not isvalid(e) then return end
   local action=actions[((cast-1)%#actions)+1]
   local fx=fxByAction[action]
   if fx==nil then errors=errors+1 log("[WARRIOR_QA] missing FX="..action) return end
   u:SetLocalFace(cast<=4 and -1 or 1)
   _RtsSkillFxLogic:PlayCast(e,no,fx,nil,{})
   local duration=0 for _,v in ipairs(durations[action]) do duration=duration+v end
   _TimerService:SetTimerOnce(function()
    if isvalid(e) then
     if u.MageSkinAction=="stand1" then returns=returns+1 else errors=errors+1 end
    end
   end,duration+0.18)
  end,1+(n-1)*2.5)
 end
 _TimerService:SetTimerOnce(function()
  _TimerService:ClearTimer(watch)
  for _,action in ipairs(actions) do
   local unique={} local expected=0
   for _,ruid in ipairs(seqs[action]) do if not unique[ruid] then unique[ruid]=true expected=expected+1 end end
   for _,face in ipairs({":L",":R"}) do
    local count=0 for _ in pairs(seen[action..face] or {}) do count=count+1 end
    log("[WARRIOR_QA] "..action..face.." frames="..tostring(count).."/"..tostring(expected))
   end
  end
  local idle=0 local idleSet={}
  for _,face in ipairs({":L",":R"}) do for r in pairs(seen["stand1"..face] or {}) do idleSet[r]=true end end
  for _ in pairs(idleSet) do idle=idle+1 end
  log("[WARRIOR_QA] no="..tostring(no).." returns="..tostring(returns).."/8 idle="..tostring(idle).."/3 effects="..tostring(effect).." errors="..tostring(errors))
 end,22)
 end
end

local T=_RtsJobTableLogic
local map=_EntityService:GetEntityByPath("/maps/RtsMap")
local ok,total=0,0
local ruids={}
for _,job in ipairs({"paladin","dk","nl","shad","phantom"}) do ruids[T:GetMagePortraitRUID(job)]=true end
for _,seq in pairs(T:GetMageSkinFrames("phantom")) do for _,r in ipairs(seq) do ruids[r]=true end end
local fx=nil
local e=map:GetChildByName("ZzPhantomPreview1")
for _,skill in ipairs(T:GetSkillsFor(e.RtsUnitComponent)) do if skill.name=="조커" then fx=skill.fx end end
ruids[fx.proj]=true ruids[fx.projRing]=true
for r,_ in pairs(ruids) do
 total=total+1
 local sp=_ResourceService:LoadSpriteAndWait(r)
 if sp~=nil and sp.IsLoadComplete then ok=ok+1 else log("[PHANTOM_VERIFY] LOAD_FAIL "..r) end
 if r==fx.proj or r==fx.projRing then log("[PHANTOM_VERIFY] sprite="..r.." width="..tostring(sp.Width).." pivot="..tostring(sp.PivotPixel).." ppu="..tostring(sp.PixelPerUnit)) end
end
log("[PHANTOM_VERIFY] loaded="..tostring(ok).."/"..tostring(total))
local card=_ResourceService:LoadSpriteAndWait(fx.proj)
local rs=_ResourceService:LoadSpriteAndWait(fx.projRing)
local actors={map:GetChildByName("ZzPhantomPreview1"),map:GetChildByName("ZzPhantomPreview2")}
local seen={{},{}} local idle={{},{}} local loopClock={0,0} local maxClock={0,0} local bodyRot=0 local rings=0 local moved=0 local badSize=0 local following=0
local track={} local started=_UtilLogic.ElapsedSeconds local timer=0
timer=_TimerService:SetTimerRepeat(function()
 for i,actor in ipairs(actors) do
  if isvalid(actor) then
   local u=actor.RtsUnitComponent
   local skin=u.MageSkinEntity
   if isvalid(skin) then
    local r=skin.SpriteRendererComponent.SpriteRUID
    if u.MageSkinAction=="phantomJoker" then seen[i][r]=true maxClock[i]=math.max(maxClock[i],u.MageActionClock) else idle[i][r]=true end
    if math.abs(skin.TransformComponent.ZRotation)>0.001 then bodyRot=bodyRot+1 end
   end
  end
 end
 for _,proj in pairs(map.Children) do
  if string.sub(proj.Name,1,8)=="RtsProj_" and isvalid(proj) then
   local ring=proj:GetChildByName("CardRing")
   if isvalid(ring) then
    rings=rings+1
    local p=proj.TransformComponent.WorldPosition
    local rp=ring.TransformComponent.WorldPosition
    if math.abs(p.x-rp.x)<0.001 and math.abs(p.y-rp.y)<0.001 then following=following+1 end
    local old=track[proj.Id]
    if old~=nil and (math.abs(p.x-old.x)>0.01 or math.abs(p.y-old.y)>0.01) then moved=moved+1 end
    track[proj.Id]={x=p.x,y=p.y}
    local width=proj.TransformComponent.Scale.x*card.Width/card.PixelPerUnit
    local ringWidth=ring.TransformComponent.Scale.x*proj.TransformComponent.Scale.x*rs.Width/rs.PixelPerUnit
    if math.abs(width-1.152)>0.001 or math.abs(ringWidth-2.528)>0.001 then badSize=badSize+1 end
   end
  end
 end
 if _UtilLogic.ElapsedSeconds-started>14 then
  _TimerService:ClearTimer(timer)
  for i=1,2 do
   local n,ni=0,0 for _ in pairs(seen[i]) do n=n+1 end for _ in pairs(idle[i]) do ni=ni+1 end
   log("[PHANTOM_VERIFY] face="..tostring(i).." attack="..tostring(n).."/8 idle="..tostring(ni).."/3 loopClock="..tostring(maxClock[i]))
  end
  log("[PHANTOM_VERIFY] bodyRotationErrors="..tostring(bodyRot).." ringSamples="..tostring(rings).." follows="..tostring(following).." moving="..tostring(moved).." sizeErrors="..tostring(badSize))
 end
end,0.02)

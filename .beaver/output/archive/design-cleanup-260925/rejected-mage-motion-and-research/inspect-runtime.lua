local prev = _RtsConfigLogic.DebugLog
_RtsConfigLogic.DebugLog = true
local function out(s) _RtsConfigLogic:Log("MAGE_INSPECT " .. s) end
local c = _RtsJobTableLogic:GetCostume("il")
for k,v in pairs(c) do out("costume " .. k .. "=" .. tostring(v)) end
for _,s in ipairs(_RtsJobTableLogic:GetSkillsRaw("il")) do
 if s.fx ~= nil then out("skill " .. s.name .. " motion=" .. tostring(s.fx.motion)) end
end
local function walk(e, depth)
 if e == nil or depth > 5 then return end
 local sr = e.SpriteRendererComponent
 out(string.rep(" ",depth)..e.Name .. (sr ~= nil and (" sprite="..sr.SpriteRUID.." clip="..sr.ClipName) or ""))
 for _,child in ipairs(e.Children:ToTable()) do walk(child,depth+1) end
end
local map = _EntityService:GetEntityByPath("/maps/RtsMap")
if map ~= nil then
 for _,e in ipairs(map.Children:ToTable()) do
  if e.RtsUnitComponent ~= nil and e.RtsUnitComponent.JobId == "il" then
   out("unit "..e.Name)
   walk(e.AvatarRendererComponent:GetAvatarRootEntity(),0)
  end
 end
end
_RtsConfigLogic.DebugLog = prev

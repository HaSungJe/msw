local before = false
_RtsConfigLogic.DebugLog = true
local function walk(e,n)
 if e == nil or n>9 then return end
 local suffix=""
 if e.SpriteRendererComponent ~= nil then suffix=suffix.." sprite="..tostring(e.SpriteRendererComponent.SpriteRUID) end
 if e.SpriteGUIRendererComponent ~= nil then suffix=suffix.." gui="..tostring(e.SpriteGUIRendererComponent.ImageRUID) end
 _RtsConfigLogic:Log("MAGE_TREE "..string.rep(" ",n)..e.Name..suffix)
 for _,child in ipairs(e.Children:ToTable()) do walk(child,n+1) end
end
local g=_EntityService:GetEntityByPath("/ui/CodexMageMotionReference")
walk(g,0)
_RtsConfigLogic.DebugLog=before

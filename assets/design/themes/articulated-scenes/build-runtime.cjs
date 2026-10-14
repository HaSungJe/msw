const fs=require('node:fs'),path=require('node:path');
const dir=__dirname,root=path.resolve(dir,'../../../..');
const read=n=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const write=(n,v)=>fs.writeFileSync(path.join(dir,n),JSON.stringify(v,null,2)+'\n');
const baseRigs=read('runtime-rigs.json'),layout=read('new-rig-layout.json'),resources=read('motion-resources.json');
const registered=new Map(resources.map(r=>[path.resolve(r.path),r]));
const missing=[];
for(const [key,rig] of Object.entries(layout)){
 for(const p of rig.parts){
  const r=registered.get(path.resolve(p.path));if(!r?.ruid){missing.push(key+':'+p.id);continue;}
  p.ruid=r.ruid;delete p.path;
 }
 baseRigs[key]=rig;
}
const defs=read('action-scenes.json');
for(const d of defs){
 if(!layout[d.key])continue;
 const r=resources.find(r=>r.id===d.key+':background');
 if(!r?.ruid){missing.push(d.key+':background');continue;}
 d.compositeBackground=d.compositeBackground||d.background;
 d.background=r.ruid;d.w=r.w;d.h=r.h;d.rig='runtime-rigs.json';d.mode='articulated';
}
if(missing.length){console.error('등록이 필요한 자산: '+[...new Set(missing)].join(', '));process.exit(2);}
const old=read('resources.json');
const merged=[...old.filter(r=>!r.id.includes(':')),...resources];
const sizes=Object.fromEntries(merged.map(r=>[r.ruid,{w:r.w,h:r.h}]));
const lua=v=>typeof v==='string'?JSON.stringify(v):typeof v==='number'||typeof v==='boolean'?String(v):Array.isArray(v)?'{'+v.map(lua).join(',')+'}':'{'+Object.entries(v).map(([k,v])=>'['+lua(k)+']='+lua(v)).join(',')+'}';
const sourcePath=path.join(root,'RootDesk/MyDesk/Themes/RtsActionThemeLogic.mlua');
let source=fs.readFileSync(sourcePath,'utf8').replace(/\r\n/g,'\n');
const replace=(from,to)=>{if(!source.includes(from))throw Error('교체 위치 없음: '+from.slice(0,70));source=source.replace(from,to);};
source=source.replace(/  if self\._T\.Rigs == nil then self\._T\.Rigs = .* end/, '  if self._T.Rigs == nil then self._T.Rigs = '+lua(baseRigs)+' end');
source=source.replace(/  if self\._T\.PartSizes == nil then self\._T\.PartSizes = .* end/, '  if self._T.PartSizes == nil then self._T.PartSizes = '+lua(sizes)+' end');
for(const d of defs){const re=new RegExp('(key = "'+d.key+'"[^\\n]*background = ")[^"]+(")');if(!re.test(source))throw Error('정의 누락 '+d.key);source=source.replace(re,'$1'+d.background+'$2');}
source=source.replace('    else\n     for _,kind in ipairs({"water-trail","water-splash"}) do','    elseif rig.fx == "water" then\n     for _,kind in ipairs({"water-trail","water-splash"}) do');
const oldMotion="    local wave=math.sin(self.Elapsed*math.pi*2/b.period+b.phase)\n    angle=b.angle+b.amp*wave\n    local rad=angle*math.pi/180\n    local ox=(b.w/2-b.px)*b.k\n    local oy=(b.py-b.h/2)*b.k\n    x=b.x+ox*math.cos(rad)-oy*math.sin(rad)\n    y=b.y-ox*math.sin(rad)-oy*math.cos(rad)-b.dy*wave\n    w=b.w*b.k h=b.h*b.k",newMotion="    local phase=self.Elapsed*math.pi*2/b.period+b.phase\n    local wave=math.sin(phase)\n    angle=b.angle+b.amp*wave+(b.spin or 0)*self.Elapsed\n    local rad=angle*math.pi/180\n    local kx=b.k*(1+(b.sx or 0)*wave)\n    local ky=b.k*(1+(b.sy or 0)*wave)\n    local ox=(b.w/2-b.px)*kx\n    local oy=(b.py-b.h/2)*ky\n    -- 신체에 붙은 부위는 같은 부유/헤엄 주기를 공유하고 관절은 따로 움직인다.\n    local groupPhase=self.Elapsed*math.pi*2/(b.gperiod or 4)+(b.gphase or 0)\n    local orbitPhase=self.Elapsed*math.pi*2/(b.orbitPeriod or 1)+(b.orbitPhase or 0)\n    x=b.x+ox*math.cos(rad)-oy*math.sin(rad)+(b.dx or 0)*math.cos(phase)+(b.gdx or 0)*math.cos(groupPhase)+(b.orbitX or 0)*math.cos(orbitPhase)\n    y=b.y-ox*math.sin(rad)-oy*math.cos(rad)-b.dy*wave-(b.gdy or 0)*math.sin(groupPhase)+(b.orbitY or 0)*math.sin(orbitPhase)\n    w=b.w*kx h=b.h*ky\n    alpha=math.max(0,math.min(1,(b.alpha or 1)+(b.alphaAmp or 0)*wave))\n    color=Color(1,1,1,alpha)";
if(source.includes(oldMotion))replace(oldMotion,newMotion);else if(!source.includes(newMotion))throw Error('모션 코드 변경 충돌');
const output=path.join(root,'tmp/theme-action/action-all-rigs-ready.mlua');fs.writeFileSync(output,source);
if(process.argv.includes('--apply')){fs.writeFileSync(sourcePath,source);write('runtime-rigs.json',baseRigs);write('action-scenes.json',defs);write('resources.json',merged);}
console.log(JSON.stringify({themes:defs.length,rigs:Object.keys(baseRigs).length,resources:merged.length,applied:process.argv.includes('--apply'),output}));

const fs=require('fs');
const root='C:/workspace/msw/',w=root+'.beaver/output/bishop-standard/';
const files=JSON.parse(fs.readFileSync(w+'upload-files.json'));
const done=JSON.parse(fs.readFileSync(w+'upload-registered.json'));
if(done.length!==31)throw Error('Need all31 registered resources');
const source=root+'RootDesk/MyDesk/RtsJobTableLogic.mlua';
let code=fs.readFileSync(source,'utf8'),before=code;
const mapping=files.map(f=>({...f,ruid:done.find(d=>d.key===f.key)?.ruid}));
for(const r of mapping){if(!r.ruid||!code.includes(r.oldRuid))throw Error('Missing old/new mapping: '+r.key);code=code.replaceAll(r.oldRuid,r.ruid);}
const masked=s=>s.replace(/[a-f0-9]{32}/g,'RUID');if(masked(before)!==masked(code))throw Error('Non-resource code changed');
fs.writeFileSync(w+'job-table-before-connect.mlua',before);
fs.writeFileSync(source,code);
for(const id of ['ice-lightning-mage','hero']){
 const file=root+'docs/design/'+id+'-motion.md';let s=fs.readFileSync(file,'utf8');for(const r of mapping.filter(x=>x.key.startsWith(id+'/')))s=s.replaceAll(r.oldRuid,r.ruid);
 s=s.replaceAll('새 PNG 업로드와 RUID 교체 진행 중.','수정 PNG 업로드·새 RUID 연결 완료. Maker 재시작 검증 결과는 character-proportions.md 참고.').replaceAll('새 PNG 업로드와 아래 RUID 표 교체 진행 중.','수정 PNG 업로드·아래 RUID 표 교체 완료. Maker 재시작 검증 결과는 character-proportions.md 참고.');fs.writeFileSync(file,s);
}
for(const rel of ['.beaver/memory/MEMORY.md','.info/motion.md','.info/character.md','.info/skill.md','docs/design/character-proportions.md']){const f=root+rel;let s=fs.readFileSync(f,'utf8');s=s.replaceAll('새 RUID 업로드·연결 진행 중.','새 RUID31개 업로드·연결 코드 반영 완료. Maker 재시작 검증 진행 중.').replaceAll('사용자 요청에 따라 변경31장 새 리소스 업로드·연결 진행 중.','변경31장 새 RUID 업로드·연결 완료. Maker 재시작 검증 진행 중.').replaceAll('PNG 보정 및 리소스 연결 진행 중.','PNG 보정 및 새 리소스 연결 완료. Maker 검증 진행 중.');fs.writeFileSync(f,s);}
const skill=root+'.info/skill.md';let s=fs.readFileSync(skill,'utf8');s='# 히어로 일반기: 본체 비율 보정338/394에 맞춰 검 이펙트 손 부착 좌표도 같은 배율로 보정. 불꽃 월드 크기2.0·재생 시간 유지.\n'+s;fs.writeFileSync(skill,s);
fs.writeFileSync(w+'resource-manifest.json',JSON.stringify(mapping,null,2));
console.log(JSON.stringify({connected:mapping.length,onlyRuidChanges:true}));

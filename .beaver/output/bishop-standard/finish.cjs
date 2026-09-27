const fs=require('fs');const root='C:/workspace/msw/',w=root+'.beaver/output/bishop-standard/';
for(const rel of ['.beaver/memory/MEMORY.md','.info/motion.md','.info/character.md','.info/skill.md','docs/design/character-proportions.md']){
const f=root+rel;let s=fs.readFileSync(f,'utf8');s=s.replaceAll('Maker 재시작 검증 진행 중.','Maker 새로고침·재시작 및 새 리소스31/31 로딩 확인. 연결/시간표 오류0, 빌드/실행 오류0.').replaceAll('Maker 검증 진행 중.','Maker 재시작·새 리소스31/31 로딩 확인. 연결/시간표 오류0, 빌드/실행 오류0.');fs.writeFileSync(f,s);
}
const f=root+'docs/design/character-proportions.md';fs.appendFileSync(f,'\n\n검증 근거: .beaver/output/bishop-standard/runtime-verification.json. [BISHOP_RATIO] loaded=31/31 mappings_or_timing_errors=0 로그 확인. 스킬 전체 자세의 인게임 시각 재생 검수는 별도이며 이번 확인은 리소스 로딩·연결·시간표까지다. 히어로 본체 축소에 맞춰 검의 손 부착 좌표에도338/394를 적용했고, 불꽃 월드 크기2.0은 유지했다. Maker는 Play 상태로 돌려놓았다.\n');
const privatePath=w+'upload-requests.private.json';if(fs.existsSync(privatePath))fs.unlinkSync(privatePath);
const result=JSON.parse(fs.readFileSync(w+'final-files.json'));result.status='31 new RUIDs connected; Maker restarted; all31 sprites loaded; no build/runtime errors';fs.writeFileSync(w+'final-files.json',JSON.stringify(result,null,2));
console.log('Final records and temporary upload credentials cleaned');

const fs=require('fs'),crypto=require('crypto');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root='C:/workspace/msw',out=root+'/.beaver/output/five-class-portraits-phantom';
(async()=>{
 const rows=[];
 for(const source of JSON.parse(fs.readFileSync(out+'/generated-sources.json','utf8'))){
  const file=root+'/assets/design/characters/'+source.id+'/portrait.png';
  await sharp(source.path).resize(496,496,{fit:'inside'}).extend({top:8,bottom:8,left:8,right:8,background:{r:0,g:0,b:0,alpha:0}}).png().toFile(file);
  const data=fs.readFileSync(file),meta=await sharp(file).metadata();
  if(meta.width!==512||meta.height!==512||!meta.hasAlpha)throw Error(source.id+' invalid format');
  rows.push({key:source.id+'/portrait',file,name:'RtsPortrait_'+source.id,size:data.length,sha256:crypto.createHash('sha256').update(data).digest('hex'),source:source.path});
 }
 fs.writeFileSync(out+'/portrait-upload-files.json',JSON.stringify(rows,null,2));
 console.log(JSON.stringify(rows));
})();

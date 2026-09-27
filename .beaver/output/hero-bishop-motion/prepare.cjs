const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root='C:/workspace/msw',work=__dirname,base=root+'/assets/design/characters/hero';
async function main(){
 const tasks=[];
 for(const [action,n] of [['wait',3],['raging-blow',8],['enraged-raging-blow',7]])for(let i=1;i<=n;i++){
  const key=action+'/motion'+String(i).padStart(2,'0')+'.png',file=base+'/frames/'+key,backup=work+'/originals/'+key;
  fs.mkdirSync(path.dirname(backup),{recursive:true});if(!fs.existsSync(backup))fs.copyFileSync(file,backup);
  tasks.push({key,file,backup,size:action==='wait'?576:704});
 }
 const refs=[base+'/concept.png',root+'/assets/design/characters/bishop/frames/wait/motion01.png',root+'/assets/design/characters/bishop/frames/angel-ray/motion03.png'];
 fs.writeFileSync(work+'/manifest.json',JSON.stringify({tasks,refs:refs.map(file=>({file,sha256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')}))},null,2));
 const meta=await sharp(refs[0]).metadata(),u=meta.width/1280,scale=147/(487*u);
 const buf=await sharp(refs[0]).resize(Math.round(meta.width*scale),Math.round(meta.height*scale)).png().toBuffer();
 await sharp({create:{width:576,height:576,channels:4,background:'#00000000'}}).composite([{input:buf,left:Math.round(288-635*u*scale),top:Math.round(512-1198*u*scale)}]).png().toFile(work+'/wait01.png');
 await sharp({create:{width:1152,height:576,channels:4,background:'#384454'}}).composite([{input:refs[1],left:0,top:0},{input:work+'/wait01.png',left:576,top:0}]).png().toFile(work+'/comparison.png');
 console.log(JSON.stringify({tasks:tasks.length,work}));
}main();

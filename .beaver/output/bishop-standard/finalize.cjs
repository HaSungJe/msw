const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root='C:/workspace/msw',work=root+'/.beaver/output/bishop-standard';
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
async function align(src,out,size,scale,fx,fy){
 const m=await sharp(src).metadata();
 const w=Math.round(m.width*scale),h=Math.round(m.height*scale),left=Math.round(size/2-fx*scale),top=Math.round((size===576?512:640)-fy*scale);
 if(left<0||top<0||left+w>size||top+h>size){
  const b=await sharp(src).resize(w,h).png().toBuffer();
  const x=Math.max(0,-left),y=Math.max(0,-top),cw=Math.min(w-x,size-Math.max(0,left)),ch=Math.min(h-y,size-Math.max(0,top));
  const cropped=await sharp(b).extract({left:x,top:y,width:cw,height:ch}).png().toBuffer();
  await sharp({create:{width:size,height:size,channels:4,background:'#00000000'}}).composite([{input:cropped,left:Math.max(0,left),top:Math.max(0,top)}]).png().toFile(out);
 }else await sharp({create:{width:size,height:size,channels:4,background:'#00000000'}}).composite([{input:await sharp(src).resize(w,h).png().toBuffer(),left,top}]).png().toFile(out);
}
async function sheet(files,out,cols=4){const s=352,hh=382,layers=[];for(let i=0;i<files.length;i++){layers.push({input:await sharp(files[i].file).resize(s,s,{fit:'contain'}).png().toBuffer(),left:i%cols*s,top:Math.floor(i/cols)*hh+30});layers.push({input:Buffer.from('<svg width="352" height="30"><text x="8" y="21" fill="white" font-family="Arial" font-size="16">'+files[i].label+'</text></svg>'),left:i%cols*s,top:Math.floor(i/cols)*hh});}await sharp({create:{width:cols*s,height:Math.ceil(files.length/cols)*hh,channels:4,background:'#384454'}}).composite(layers).png().toFile(out);}
async function main(){
 const manifest=JSON.parse(fs.readFileSync(work+'/manifest.json'));
 const il='C:/Users/timec/.codex/generated_images/01a0dbf3-5094-7520-bfc7-f24b6496f5e5/exec-724228c5-65ce-46f0-a256-144eef7136fd.png';
 fs.copyFileSync(il,root+'/assets/design/characters/ice-lightning-mage/concept.png');
 fs.copyFileSync(JSON.parse(fs.readFileSync(work+'/fire-poison-mage-concept-correction.json')).generated,root+'/assets/design/characters/fire-poison-mage/concept.png');
 fs.copyFileSync(JSON.parse(fs.readFileSync(work+'/hero-concept-final.json')).generated,root+'/assets/design/characters/hero/concept.png');
 const bmp=await sharp(il).metadata(),u=bmp.width/1280;
 await align(il,root+'/assets/design/characters/ice-lightning-mage/frames/wait/motion01.png',576,338/(860*u),635*u,1118*u);
 const landmarks={
 'blizzard/motion01.png':[280,635,1105], 'blizzard/motion02.png':[297,650,1144],
 'blizzard/motion03.png':[325,650,1138], 'blizzard/motion04.png':[308,630,1118],
 'blizzard/motion05.png':[323,635,1144], 'chain-lightning/motion01.png':[349,647,1158],
 'chain-lightning/motion02.png':[341,647,1128], 'chain-lightning/motion03.png':[320,650,1135],
 'chain-lightning/motion04.png':[391,670,1138], 'chain-lightning/motion05.png':[342,670,1150],
 'wait/motion02.png':[395,633,1143], 'wait/motion03.png':[397,646,1178]
 };
 const finals=[];
 for(const name of fs.readdirSync(work+'/revisions').filter(n=>n.endsWith('.json'))){const t=JSON.parse(fs.readFileSync(work+'/revisions/'+name));const key=t.rel.replace('frames/','');const lm=landmarks[key];if(!lm)continue;const meta=await sharp(t.generated).metadata(),q=meta.width/1280;const out=root+'/assets/design/characters/'+t.key;await align(t.generated,out,t.width,147/(lm[0]*q),lm[1]*q,lm[2]*q);finals.push({...t,output:out,sha256:hash(out)});}
 for(const t of manifest.tasks.filter(t=>t.id==='hero'&&t.rel.startsWith('frames/'))){await align(t.original,root+'/assets/design/characters/'+t.key,t.width,338/394,t.width/2,t.width===576?512:640);}
 const bishopChanged=manifest.bishopHashes.filter(b=>hash(b.file)!==b.sha256);if(bishopChanged.length)throw Error('Bishop frames changed');
 const files=[{file:root+'/assets/design/characters/bishop/frames/wait/motion01.png',label:'Bishop motion - reference'},...['ice-lightning-mage','fire-poison-mage','hero'].map(id=>({file:root+'/assets/design/characters/'+id+'/frames/wait/motion01.png',label:id}))];
 await sheet(files,work+'/comparison.png');
 await sheet(manifest.tasks.filter(t=>t.id==='ice-lightning-mage'&&t.rel.startsWith('frames/')).map(t=>({file:root+'/assets/design/characters/'+t.key,label:t.rel.replace('frames/','')})),work+'/motion-review.png');
 fs.writeFileSync(work+'/final-files.json',JSON.stringify({status:'local PNG updates; game RUIDs not replaced',finals,bishopFramesUnchanged:true},null,2));
 console.log(JSON.stringify({generatedFramesAligned:finals.length+1,heroFramesScaled:18,bishopFramesUnchanged:true}));
}
main().catch(e=>{console.error(e);process.exit(1)});

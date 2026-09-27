const fs=require('fs'),crypto=require('crypto');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root='C:/workspace/msw',w=root+'/.beaver/output/bishop-standard';
(async()=>{
const m=JSON.parse(fs.readFileSync(w+'/manifest.json'));const errors=[],checked=[];
for(const t of m.tasks){const p=root+'/assets/design/characters/'+t.key,meta=await sharp(p).metadata();if(meta.width!==t.width||meta.height!==t.height||!meta.hasAlpha)errors.push(t.key);const {data,info}=await sharp(p).ensureAlpha().raw().toBuffer({resolveWithObject:true});let edge=0;for(let x=0;x<info.width;x++)edge+=data[x*4+3]+data[((info.height-1)*info.width+x)*4+3];for(let y=0;y<info.height;y++)edge+=data[(y*info.width)*4+3]+data[(y*info.width+info.width-1)*4+3];if(edge&&t.rel.startsWith('frames/'))errors.push(t.key+' edge clipping');checked.push({key:t.key,width:meta.width,height:meta.height,alpha:meta.hasAlpha,sha256:crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')});}
for(const b of m.bishopHashes)if(crypto.createHash('sha256').update(fs.readFileSync(b.file)).digest('hex')!==b.sha256)errors.push('bishop changed: '+b.file);
const hero=m.tasks.filter(t=>t.id==='hero'&&t.rel.startsWith('frames/')),s=280,layers=[];for(let i=0;i<hero.length;i++)layers.push({input:await sharp(root+'/assets/design/characters/'+hero[i].key).resize(s,s).png().toBuffer(),left:i%6*s,top:Math.floor(i/6)*s});await sharp({create:{width:s*6,height:s*3,channels:4,background:'#384454'}}).composite(layers).png().toFile(w+'/hero-review.png');
const result={checked:checked.length,bishopFramesUnchanged:errors.every(e=>!e.startsWith('bishop')),errors,files:checked};fs.writeFileSync(w+'/verification.json',JSON.stringify(result,null,2));console.log(JSON.stringify({checked:checked.length,errors}));
})();

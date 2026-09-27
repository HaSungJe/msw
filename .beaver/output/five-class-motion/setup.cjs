const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root='C:/workspace/msw',work=path.join(root,'.beaver/output/five-class-motion');
const rows={paladin:[180,610,1180,650],'dark-knight':[240,645,1178,585],'night-lord':[230,645,1170,565],shadower:[175,600,1122,595],phantom:[350,705,1200,635]};
(async()=>{const refs=[];for(const [id,[crown,chin,sole,cx]]of Object.entries(rows)){
 const src=path.join(root,'assets/design/characters',id,'concept.png'); const meta=await sharp(src).metadata(); const scale=147/(chin-crown);
 const w=Math.round(meta.width*scale),h=Math.round(meta.height*scale),left=Math.round(288-cx*scale),top=Math.round(512-sole*scale);
 if(left<0||top<0||left+w>576||top+h>576)throw Error(id+' canvas overflow');
 const dest=path.join(work,'base',id+'.png');fs.mkdirSync(path.dirname(dest),{recursive:true});
 await sharp({create:{width:576,height:576,channels:4,background:'#00000000'}}).composite([{input:await sharp(src).resize(w,h).png().toBuffer(),left,top}]).png().toFile(dest);
 refs.push({id,source:src,sha256:crypto.createHash('sha256').update(fs.readFileSync(src)).digest('hex'),base:dest,scale,crown,chin,sole,cx});
 }fs.writeFileSync(path.join(work,'base-manifest.json'),JSON.stringify(refs,null,2));console.log('5 base idle frames aligned');})();

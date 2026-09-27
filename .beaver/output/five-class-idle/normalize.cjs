const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname;
(async()=>{
let rows=JSON.parse(fs.readFileSync(path.join(root,'alignment.json'),'utf8'));
for(const j of rows){
 const m=await sharp(j.source).metadata(),s=j.scale,w=Math.round(m.width*s),h=Math.round(m.height*s),size=j.size;
 const x=Math.round(size/2-j.footX*s),y=Math.round((size===576?512:640)-j.footY*s);
 const resized=await sharp(j.source).resize(w,h).png().toBuffer();
 const sx=Math.max(0,-x),sy=Math.max(0,-y),cw=Math.min(w-sx,size-Math.max(x,0)),ch=Math.min(h-sy,size-Math.max(y,0));
 const buf=await sharp(resized).extract({left:sx,top:sy,width:cw,height:ch}).png().toBuffer();
 const dest=path.join(root,'normalized',j.id,j.skill,`motion${String(j.n).padStart(2,'0')}.png`);fs.mkdirSync(path.dirname(dest),{recursive:true});
 await sharp({create:{width:size,height:size,channels:4,background:'#00000000'}}).composite([{input:buf,left:Math.max(0,x),top:Math.max(0,y)}]).png().toFile(dest);j.normalized=dest;
}
fs.writeFileSync(path.join(root,'alignment.json'),JSON.stringify(rows,null,2));console.log('normalized',rows.length);
})();

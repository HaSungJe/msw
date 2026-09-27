const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root='C:/workspace/msw',work=path.join(root,'.beaver/output/five-class-motion');
const correctionsPath=path.join(work,'corrections.json');
const corrections=fs.existsSync(correctionsPath)?JSON.parse(fs.readFileSync(correctionsPath,'utf8')):{};
(async()=>{
 const rows=[];
 for(const name of fs.readdirSync(path.join(work,'generated')).filter(n=>n.endsWith('.json')).sort()){
  const j=JSON.parse(fs.readFileSync(path.join(work,'generated',name),'utf8'));
  const size=j.skill==='wait'?576:704;
  const correction=corrections[j.key]||{};
  const src=correction.source||j.source;
  const meta=await sharp(src).metadata();
  const dest=path.join(work,'normalized',j.id,j.skill,`motion${String(j.n).padStart(2,'0')}.png`);
  fs.mkdirSync(path.dirname(dest),{recursive:true});
  if(correction.head){
   const scale=147/correction.head,w=Math.round(meta.width*scale),h=Math.round(meta.height*scale);
   const x=Math.round(size/2-correction.footX*scale),y=Math.round((size===576?512:640)-correction.footY*scale);
   const resized=await sharp(src).resize(w,h).png().toBuffer();
   const sx=Math.max(0,-x),sy=Math.max(0,-y),cw=Math.min(w-sx,size-Math.max(x,0)),ch=Math.min(h-sy,size-Math.max(y,0));
   const visible=await sharp(resized).extract({left:sx,top:sy,width:cw,height:ch}).png().toBuffer();
   await sharp({create:{width:size,height:size,channels:4,background:'#00000000'}}).composite([{input:visible,left:Math.max(x,0),top:Math.max(y,0)}]).png().toFile(dest);
  }else await sharp(src).resize(size,size).png().toFile(dest);
  const {data,info}=await sharp(dest).raw().toBuffer({resolveWithObject:true});
  let left=size,top=size,right=-1,bottom=-1,edge=0,alphaMin=255,alphaMax=0;
  for(let y=0;y<size;y++)for(let x=0;x<size;x++){
   const a=data[(y*size+x)*info.channels+3];alphaMin=Math.min(alphaMin,a);alphaMax=Math.max(alphaMax,a);
   if(a>32){left=Math.min(left,x);top=Math.min(top,y);right=Math.max(right,x);bottom=Math.max(bottom,y);if(x===0||y===0||x===size-1||y===size-1)edge++;}
  }
  rows.push({...j,source:src,normalized:dest,size,bbox:[left,top,right,bottom],edgePixels:edge,alphaMin,alphaMax,sha256:crypto.createHash('sha256').update(fs.readFileSync(dest)).digest('hex')});
 }
 for(const id of ['paladin','dark-knight','night-lord','shadower','phantom']){
  const dest=path.join(work,'normalized',id,'wait/motion01.png');fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(path.join(work,'base',id+'.png'),dest);
 }
 fs.writeFileSync(path.join(work,'normalized.json'),JSON.stringify(rows,null,2));
 console.log(JSON.stringify({count:rows.length,edgeIssues:rows.filter(r=>r.edgePixels>0).map(r=>[r.key,r.edgePixels]),nonTransparent:rows.filter(r=>r.alphaMin!==0||r.alphaMax!==255).map(r=>r.key)}));
})();

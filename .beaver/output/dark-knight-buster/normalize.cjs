const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname;
(async()=>{
 const rows=JSON.parse(fs.readFileSync(path.join(root,'generated.json'),'utf8'));
 const out=path.join(root,'normalized');fs.mkdirSync(out,{recursive:true});
 const metrics=[];
 for(const row of rows){
  const {data,info}=await sharp(row.source).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const w=info.width,h=info.height;
  let minX=w,minY=h,maxX=0,maxY=0;
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){if(data[(y*w+x)*4+3]>32){minX=Math.min(minX,x);maxX=Math.max(maxX,x);minY=Math.min(minY,y);maxY=Math.max(maxY,y)}}
  const scale=row.scale;
  const left=Math.round(416-row.footX*scale),top=Math.round(768-row.footY*scale);
  const nw=Math.round(w*scale),nh=Math.round(h*scale);
  const buf=await sharp(row.source).resize(nw,nh).png().toBuffer();
  const sx=Math.max(0,-left),sy=Math.max(0,-top),cw=Math.min(nw-sx,832-Math.max(0,left)),ch=Math.min(nh-sy,832-Math.max(0,top));
  const clipped=await sharp(buf).extract({left:sx,top:sy,width:cw,height:ch}).png().toBuffer();
  const dest=path.join(out,'motion'+String(row.n).padStart(2,'0')+'.png');
  await sharp({create:{width:832,height:832,channels:4,background:'#00000000'}}).composite([{input:clipped,left:Math.max(0,left),top:Math.max(0,top)}]).png().toFile(dest);
  const bounds=[minX*scale+left,minY*scale+top,maxX*scale+left,maxY*scale+top];
  if(bounds[0]<2||bounds[1]<2||bounds[2]>829||bounds[3]>829)throw Error('clipped '+row.n+' '+bounds);
  metrics.push({n:row.n,bounds,scale,footX:row.footX,footY:row.footY});
 }
 fs.writeFileSync(path.join(root,'normalization.json'),JSON.stringify(metrics,null,2));
 const cells=[];
 for(const [i,row] of rows.entries()){
  const p=path.join(out,'motion'+String(row.n).padStart(2,'0')+'.png');
  cells.push({input:await sharp(p).resize(352,352).png().toBuffer(),left:(i%3)*352,top:Math.floor(i/3)*352});
 }
 await sharp({create:{width:1056,height:704,channels:4,background:'#d8d8d8'}}).composite(cells).png().toFile(path.join(root,'contact.png'));
 console.log(metrics);
})();

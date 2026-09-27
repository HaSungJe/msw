const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const w=__dirname,base='C:/workspace/msw/assets/design/characters/hero',lm=JSON.parse(fs.readFileSync(w+'/landmarks.json'));
async function main(){
 const rows=fs.readdirSync(w).filter(n=>n.startsWith('generated-')&&n.endsWith('.json')).map(n=>JSON.parse(fs.readFileSync(w+'/'+n)));
 rows.push({key:'wait/motion01.png',generated:base+'/concept.png',prompt:'Approved concept, uniform size and feet alignment only.'});
 const finals=[];
 for(const row of rows){if(!lm[row.key])continue;
  const m=await sharp(row.generated).metadata(),u=m.width/1280,land=lm[row.key],scale=147/(land[0]*u),size=row.key.startsWith('wait')?576:704;
  const {data,info}=await sharp(row.generated).ensureAlpha().raw().toBuffer({resolveWithObject:true});let bottom=0;
  for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++)if(data[(y*info.width+x)*4+3]>40)bottom=Math.max(bottom,y);
  const left=Math.round(size/2-land[1]*u*scale),top=Math.round(size-64-bottom*scale);
  const out=w+'/normalized/'+row.key;fs.mkdirSync(path.dirname(out),{recursive:true});
  const resized=await sharp(row.generated).resize(Math.round(m.width*scale),Math.round(m.height*scale)).png().toBuffer();
  await sharp({create:{width:size,height:size,channels:4,background:'#00000000'}}).composite([{input:resized,left,top}]).png().toFile(out);
  finals.push({...row,file:out,size,scale,left,top,headLength:147,footY:size-64,hand:land[2]===undefined?null:[Math.round(left+land[2]*u*scale),Math.round(top+land[3]*u*scale)],sha256:crypto.createHash('sha256').update(fs.readFileSync(out)).digest('hex')});
 }
 fs.writeFileSync(w+'/normalized.json',JSON.stringify(finals,null,2));console.log(JSON.stringify(finals.map(f=>({key:f.key,hand:f.hand}))));
 const layers=[];for(let i=0;i<finals.length;i++)layers.push({input:await sharp(finals[i].file).resize(352,352).png().toBuffer(),left:i%4*352,top:Math.floor(i/4)*352});
 await sharp({create:{width:1408,height:Math.ceil(finals.length/4)*352,channels:4,background:'#384454'}}).composite(layers).png().toFile(w+'/normalized-review.png');
}main();

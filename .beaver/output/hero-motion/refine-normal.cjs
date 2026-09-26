const fs=require('fs'),sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const work=__dirname,root='C:/workspace/msw/assets/design/characters/hero';
const inputs=JSON.parse(fs.readFileSync(work+'/refined-prompts.json'));
const specs=[ [.35,647,1207],[.34,613,1207],[.35,631,1220],[.34,599,1214],[.345,622,1203],[.34,611,1203],[.345,643,1183],[.36,624,1224] ];
(async()=>{
const report=[];
for(let i=0;i<inputs.length;i++){
 const [s,fx,fy]=specs[i],meta=await sharp(inputs[i].file).metadata();
 const w=Math.round(meta.width*s),h=Math.round(meta.height*s);
 const im=await sharp(inputs[i].file).resize(w,h).png().toBuffer();
 const left=Math.round(352-fx*s),top=Math.round(640-fy*s);
 if(left<0||top<0||left+w>704||top+h>704)throw Error('Canvas overflow '+i);
 const dest=root+'/frames/raging-blow/motion'+String(i+1).padStart(2,'0')+'.png';
 await sharp({create:{width:704,height:704,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).composite([{input:im,left,top}]).png().toFile(dest);
 report.push({frame:i+1,file:dest,scale:s,sourceFoot:[fx,fy],pivot:[352,640],alpha:meta.hasAlpha,handOnly:i<7});
}
fs.writeFileSync(work+'/refined-normalization.json',JSON.stringify(report,null,2));
const layers=[];
for(let i=0;i<8;i++)layers.push({input:await sharp(root+'/frames/raging-blow/motion'+String(i+1).padStart(2,'0')+'.png').resize(440).png().toBuffer(),left:(i%4)*440,top:Math.floor(i/4)*440});
await sharp({create:{width:1760,height:880,channels:4,background:'#29383f'}}).composite(layers).png().toFile(work+'/normal-contact-sheet.png');
console.log(JSON.stringify(report));
})();

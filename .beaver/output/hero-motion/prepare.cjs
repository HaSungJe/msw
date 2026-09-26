const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/timec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root='C:/workspace/msw',out=root+'/assets/design/characters/hero',work=root+'/.beaver/output/hero-motion';
const gen='C:/Users/timec/.codex/generated_images/01a0d776-11e4-7ba1-9fa1-55aad7174cec/';
const specs=[
{key:'idle',file:'exec-0cbe09cb-c304-4b2e-94ab-914b71191f05.png',scale:.34,feet:[618,1215],size:576,dest:['frames/wait/motion01.png']},
{key:'en01',file:'exec-19fee4dc-bae9-47f0-9d77-0e9953603711.png',scale:.32,feet:[528,1185],size:704,dest:['frames/enraged-raging-blow/motion01.png']},
{key:'up',file:'exec-d9de8bb4-2a61-401a-8669-8b8b928f516b.png',scale:.37,feet:[629,1214],size:704,dest:['frames/enraged-raging-blow/motion02.png']},
{key:'down',file:'exec-32533b6c-e406-406e-bdbd-dbf56750551d.png',scale:.35,feet:[749,1168],size:704,dest:['frames/enraged-raging-blow/motion03.png']},
{key:'thrust',file:'exec-eacc4a37-af94-426c-932d-71d9e9739f0e.png',scale:.415,feet:[794,1020],size:704,dest:['frames/enraged-raging-blow/motion04.png']}
];
(async()=>{
fs.mkdirSync(work,{recursive:true});
for(const s of specs){
const source=gen+s.file,meta=await sharp(source).metadata();
if(!meta.hasAlpha)throw Error('Missing alpha '+s.key);
const w=Math.round(meta.width*s.scale),h=Math.round(meta.height*s.scale);
let left=Math.round(s.size/2-s.feet[0]*s.scale),top=Math.round(s.size-64-s.feet[1]*s.scale);
const raw=await sharp(source).resize(w,h).ensureAlpha().raw().toBuffer();
let x0=w,y0=h,x1=0,y1=0;
for(let y=0;y<h;y++)for(let x=0;x<w;x++)if(raw[(y*w+x)*4+3]>8){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}
left+=x0;top+=y0;
const cw=x1-x0+1,ch=y1-y0+1;
if(left<0||top<0||left+cw>s.size||top+ch>s.size)throw Error('Visible canvas clipping '+s.key+' '+JSON.stringify({left,top,cw,ch,w,h,x0,y0,x1,y1}));
const resized=await sharp(raw,{raw:{width:w,height:h,channels:4}}).extract({left:x0,top:y0,width:cw,height:ch}).png().toBuffer();
const result=await sharp({create:{width:s.size,height:s.size,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).composite([{input:resized,left,top}]).png().toBuffer();
for(const dest of s.dest){const full=out+'/'+dest;fs.mkdirSync(path.dirname(full),{recursive:true});fs.writeFileSync(full,result);}
console.log(s.key,JSON.stringify({size:s.size,feet:[s.size/2,s.size-64],scale:s.scale,alpha:meta.hasAlpha}));
}
await sharp(gen+'exec-c0d464bd-afef-456f-98fc-c35c9df1345c.png').resize(512,512).png().toFile(out+'/portrait.png');
fs.copyFileSync(gen+specs[0].file,work+'/approved-concept.png');
fs.copyFileSync('C:/Users/timec/AppData/Local/Temp/claude/C--workspace-msw/0e9cd6bf-e73c-4685-ac96-e8797a6f7623/scratchpad/sheet_rb.png',work+'/effect-raging-blow.png');
fs.copyFileSync('C:/Users/timec/AppData/Local/Temp/claude/C--workspace-msw/0e9cd6bf-e73c-4685-ac96-e8797a6f7623/scratchpad/sheet_1120017.png',work+'/effect-enrage.png');
fs.writeFileSync(work+'/normalization.json',JSON.stringify(specs,null,2));
const rows=[['frames/wait/motion01.png','frames/raging-blow/motion01.png','frames/raging-blow/motion02.png','frames/raging-blow/motion03.png'],['frames/enraged-raging-blow/motion01.png','frames/enraged-raging-blow/motion02.png','frames/enraged-raging-blow/motion03.png','frames/enraged-raging-blow/motion04.png']];
const layers=[];
for(let y=0;y<2;y++)for(let x=0;x<4;x++){
const fn=rows[y][x],m=await sharp(out+'/'+fn).metadata();
layers.push({input:await sharp(out+'/'+fn).resize(Math.round(m.width*.65),Math.round(m.height*.65)).png().toBuffer(),left:x*460+Math.round((704-m.width)*.325),top:y*460+Math.round((704-m.height)*.65)});
}
await sharp({create:{width:1840,height:920,channels:4,background:'#344348'}}).composite(layers).png().toFile(work+'/contact-sheet.png');
})();

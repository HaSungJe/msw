const fs=require('fs'),crypto=require('crypto');
const root='C:/workspace/msw',w=root+'/.beaver/output/bishop-standard';
const m=JSON.parse(fs.readFileSync(w+'/manifest.json'));
const tasks=m.tasks.filter(t=>['ice-lightning-mage','hero'].includes(t.id)&&t.rel.startsWith('frames/')).map(t=>{
 const doc=fs.readFileSync(root+'/docs/design/'+t.id+'-motion.md','utf8');
 const row=doc.split('\n').find(l=>l.startsWith('| '+t.rel+' |'));
 if(!row)throw Error(t.key);const oldRuid=row.match(/`([0-9a-f]{32})`/)[1];
 const file=root+'/assets/design/characters/'+t.key;
 return {key:t.key,file,oldRuid,name:'RtsBishopRatio_'+t.key.replaceAll('/','_').replace('.png',''),contentLength:fs.statSync(file).size,sha256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')};
});
fs.writeFileSync(w+'/upload-files.json',JSON.stringify(tasks,null,2));console.log(JSON.stringify(tasks));

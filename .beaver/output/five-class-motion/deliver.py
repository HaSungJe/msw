from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib,numpy as np

r=Path(__file__).parent;project=r.parents[2]
names={'paladin':'팔라딘','dark-knight':'다크나이트','night-lord':'나이트로드','shadower':'섀도어','phantom':'팬텀'}
seqs=json.loads((r/'playback.json').read_text(encoding='utf-8'))
records=json.loads((r/'normalized.json').read_text(encoding='utf-8'))
manifest=[]
for cid in names:
    target=project/'assets/design/characters'/cid
    frames=[]
    for p in sorted((r/'normalized'/cid).glob('*/*.png')):
        dest=target/'frames'/p.relative_to(r/'normalized'/cid);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        im=Image.open(dest).convert('RGBA');a=np.array(im);assert im.size==((576,576) if p.parent.name=='wait' else (704,704))
        assert a[:,:,3].min()==0 and a[:,:,3].max()==255
        assert max(a[0,:,3].max(),a[-1,:,3].max(),a[:,0,3].max(),a[:,-1,3].max())<=32
        frames.append({'file':dest.relative_to(target).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'width':im.width,'height':im.height})
    item={'id':cid,'status':'local-frames-complete-game-integration-pending','concept':'concept.png','idleCanvas':576,'attackCanvas':704,'idleFeet':[288,512],'attackFeet':[352,640],'referenceHead':147,'frames':frames,'playback':[s for s in seqs if s['id']==cid]}
    (target/'motion.json').write_text(json.dumps(item,ensure_ascii=False,indent=2),encoding='utf-8');manifest.append(item)
assert sum(len(m['frames']) for m in manifest)==80
for b in json.loads((r/'base-manifest.json').read_text(encoding='utf-8')):
    assert hashlib.sha256(Path(b['source']).read_bytes()).hexdigest()==b['sha256']
(r/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
preview=(r/'preview.html').read_text(encoding='utf-8').replace('normalized/${st.id}/${f.skill}/','../../../assets/design/characters/${st.id}/frames/${f.skill}/')
(r/'preview.html').write_text(preview,encoding='utf-8')
# A compact animated contact preview uses the same finished PNG frames and times.
primary=['divine-charge','spear-buster','quadruple-throw','savage-blow','joker'];font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',20)
animations=[]
for step in range(80):
    canvas=Image.new('RGB',(1400,310),'#e6e6eb');draw=ImageDraw.Draw(canvas)
    for k,(cid,skill) in enumerate(zip(names,primary)):
        s=next(s for s in seqs if s['id']==cid and s['skill']==skill);t=(step*.05)%sum(s['times']);n=s['order'][-1]
        for no,duration in zip(s['order'],s['times']):
            if t<duration:n=no;break
            t-=duration
        im=Image.open(project/'assets/design/characters'/cid/'frames'/skill/f'motion{n:02}.png').convert('RGBA');im.thumbnail((280,280));canvas.paste(im,(k*280,30),im)
        draw.text((k*280+12,3),names[cid],font=font,fill='#222633')
    animations.append(canvas)
animations[0].save(r/'motion-preview.gif',save_all=True,append_images=animations[1:],duration=50,loop=0,optimize=False)
print(json.dumps({'saved':{m['id']:len(m['frames']) for m in manifest},'total':80,'conceptsUnchanged':True,'dimensionAlphaEdgeChecks':'passed'},ensure_ascii=False))

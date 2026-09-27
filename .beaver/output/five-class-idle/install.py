from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib,numpy as np
r=Path(__file__).parent;project=r.parents[2];work=r.parent/'five-class-motion';throw=r.parent/'phantom-joker-throw'
names={'paladin':'팔라딘','dark-knight':'다크나이트','night-lord':'나이트로드','shadower':'섀도어','phantom':'팬텀'}
rows=json.loads((r/'alignment.json').read_text(encoding='utf-8'));assert len(rows)==21
old=json.loads((work/'manifest.json').read_text(encoding='utf-8'));preserved=[]
for item in old:
    if item['id']=='phantom':continue
    for f in item['frames']:
        if '/wait/' not in f['file']:preserved.append((project/'assets/design/characters'/item['id']/f['file'],f['sha256']))
for j in rows:
    p=Path(j['normalized']);im=Image.open(p).convert('RGBA');a=np.array(im)
    assert im.size==(j['size'],j['size']) and a[:,:,3].min()==0 and a[:,:,3].max()==255
    assert max(a[0,:,3].max(),a[-1,:,3].max(),a[:,0,3].max(),a[:,-1,3].max())<=32,(j['id'],j['skill'],j['n'],'edge')
    dest=project/'assets/design/characters'/j['id']/'frames'/j['skill']/p.name;shutil.copyfile(p,dest)
for n in range(7,11):
    p=project/'assets/design/characters/phantom/frames/joker'/f'motion{n:02}.png';dest=throw/'rejected-rotation'/f'unused-motion{n:02}.png'
    assert p.resolve().is_relative_to((project/'assets/design/characters/phantom/frames/joker').resolve())
    assert dest.resolve().is_relative_to(throw.resolve())
    if p.exists():p.replace(dest)
seqs=json.loads((work/'playback.json').read_text(encoding='utf-8'));manifest=[]
for cid in names:
    target=project/'assets/design/characters'/cid;frames=[]
    for p in sorted((target/'frames').glob('*/*.png')):
        im=Image.open(p);frames.append({'file':p.relative_to(target).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'width':im.width,'height':im.height})
    item={'id':cid,'status':'local-frames-revised-game-integration-pending','concept':'concept.png','idleCanvas':576,'attackCanvas':704,'idleFeet':[288,512],'attackFeet':[352,640],'referenceHead':147,'revision':'natural-game-idle; phantom-fixed-facing-card-throw-neck-grip','frames':frames,'playback':[s for s in seqs if s['id']==cid]}
    (target/'motion.json').write_text(json.dumps(item,ensure_ascii=False,indent=2),encoding='utf-8');manifest.append(item)
assert sum(len(m['frames']) for m in manifest)==76
for p,sha in preserved:assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
for b in json.loads((work/'base-manifest.json').read_text(encoding='utf-8')):assert hashlib.sha256(Path(b['source']).read_bytes()).hexdigest()==b['sha256']
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',20)
def board(poses):
    out=Image.new('RGB',(1400,310),'#e5e7ed');d=ImageDraw.Draw(out)
    for k,(cid,skill,n) in enumerate(poses):
        im=Image.open(project/'assets/design/characters'/cid/'frames'/skill/f'motion{n:02}.png').convert('RGBA')
        if im.width==576:
            bg=Image.new('RGBA',(704,704));bg.paste(im,(64,128));im=bg
        im.thumbnail((280,280));out.paste(im,(k*280,30),im);d.text((k*280+10,3),names[cid],font=font,fill='#222633')
    return out
idle=[board([(cid,'wait',n) for cid in names]) for n in [1,2,1,3]]
idle[0].save(r/'idle-preview.gif',save_all=True,append_images=idle[1:],duration=[650,450,650,450],loop=0,optimize=False)
sequence=[1]+[2,3,4,5]*8+[6];durations=[350]+[50]*32+[350];gif=[]
for n in sequence:
    out=Image.new('RGB',(480,510),'#e5e7ed');im=Image.open(project/'assets/design/characters/phantom/frames/joker'/f'motion{n:02}.png').convert('RGBA');im.thumbnail((480,480));out.paste(im,(0,30),im);ImageDraw.Draw(out).text((16,5),'조커 · 연속 카드 투척 (투사체 별도)',font=font,fill='#222633');gif.append(out)
gif[0].save(r/'phantom-throw.gif',save_all=True,append_images=gif[1:],duration=durations,loop=0,optimize=False)
# Replace the previous all-character showcase so it cannot continue to show the rejected spin.
primary=['divine-charge','spear-buster','quadruple-throw','savage-blow','joker'];frames=[]
for step in range(80):
    poses=[]
    for cid,skill in zip(names,primary):
        s=next(s for s in seqs if s['id']==cid and s['skill']==skill);t=(step*.05)%sum(s['times']);n=s['order'][-1]
        for no,dt in zip(s['order'],s['times']):
            if t<dt:n=no;break
            t-=dt
        poses.append((cid,skill,n))
    frames.append(board(poses))
frames[0].save(work/'motion-preview.gif',save_all=True,append_images=frames[1:],duration=50,loop=0,optimize=False)
report={'updated':21,'total':76,'otherAttackFilesUnchanged':len(preserved),'conceptsUnchanged':5,'dimensionsTransparencyEdges':'passed','phantomSpinRemoved':True,'gameIntegration':False}
(r/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))

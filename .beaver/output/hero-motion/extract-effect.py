import sys, pathlib, json, urllib.request
sys.path.insert(0, r'C:/Users/timec/AppData/Local/Temp/claude/C--workspace-msw/0e9cd6bf-e73c-4685-ac96-e8797a6f7623/scratchpad')
import clipinfo as C
out=pathlib.Path(__file__).parent/'effect-raw'
out.mkdir(exist_ok=True)
def cached(guid,kind):
    p=out/f'{guid}.{kind}.mod'
    if not p.exists():
        ext='win' if kind=='animationclip' else 'png'
        url=f'https://mod-resource.dn.nexoncdn.co.kr/{guid[:2]}-{kind}/{guid[2:4]}/{guid}.{ext}.mod'
        p.write_bytes(urllib.request.urlopen(url,timeout=30).read())
    return str(p)
C.cache_path=cached
rows=[]
for index,(sec,guid) in enumerate(C.clip_frames('fa2bfe8ff4f543fb815dd7ee5e02eac9')):
    path=C.cache_path(guid,'sprite')
    d=pathlib.Path(path).read_bytes()
    i=19
    while d[i]==0x10:i+=2
    ln,i=C.varint(d,i)
    f=C.parse_msg(d[i:i+ln]); vals={a:c for a,b,c in f if b==0}
    origin={a:c for a,b,c in C.parse_msg(next(c for a,b,c in f if a==3 and b==2)) if b==0}
    ox,oy=origin.get(1,0),origin.get(2,0)
    if ox>=2**63:ox-=2**64
    if oy>=2**63:oy-=2**64
    dest=out/f'{index:02d}.png'
    if not dest.exists():
        url=f'https://mod-resource.dn.nexoncdn.co.kr/{guid[:2]}-sprite/{guid[2:4]}/{guid}.png.mod'
        blob=urllib.request.urlopen(url,timeout=30).read(); start=blob.index(b'\x89PNG'); end=blob.index(b'IEND',start)+8
        dest.write_bytes(blob[start:end])
    rows.append(dict(index=index,duration=round(sec or 0,3),guid=guid,width=vals[1],height=vals[2],ox=ox,oy=oy))
(out/'frames.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps(rows))

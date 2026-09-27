from pathlib import Path
import json,hashlib,shutil

workspace=Path('C:/workspace/msw')
work=workspace/'.beaver/output/five-class-design'
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
backup=work/'previous-concepts'
backup.mkdir(exist_ok=True)
phantom=json.loads((work/'phantom-revision.json').read_text(encoding='utf-8'))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(Path(phantom['source']))==next(r['sha256'] for r in manifest if r['id']=='phantom')
for row in manifest:
    source=Path(row['path'])
    assert digest(source)==row['sha256'], row['id']
for row in manifest:
    target=workspace/'assets/design/characters'/row['id']/'concept.png'
    assert target.parent.is_dir(),target
    if target.exists():
        old=backup/f"{row['id']}-{digest(target)[:12]}.png"
        if not old.exists():shutil.copy2(target,old)
    shutil.copy2(Path(row['path']),target)
    assert digest(target)==row['sha256'],row['id']
    row['installed_path']=str(target)
    row['status']='user-selected concept saved; motion and game connection pending'
    print(row['id']+': '+str(target))
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

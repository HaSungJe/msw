from pathlib import Path
import shutil
r=Path(__file__).parent;dest=r.parent/'phantom-joker-video';p=dest/'install.py';text=p.read_text(encoding='utf-8');shutil.copyfile(p,r/'previous-install.py')
text=text.replace("card.size==(128,192)","card.size==(256,384)")
text=text.replace("manifest=[]", "ring=effect.with_name('ring.png');shutil.copyfile(r/'ring.png',ring)\n+ringImage=Image.open(ring).convert('RGBA');assert ringImage.size==(512,512) and ringImage.getchannel('A').getextrema()[0]==0\n+manifest=[]".replace('\n+','\n'))
text=text.replace("revision='video-referenced-cross-body-barrage-no-spin'", "revision='compact-stance-dynamic-barrage-ring-projectiles'")
text=text.replace("projectileSprite='assets/design/effects/phantom-joker/card.png',", "projectileSprite='assets/design/effects/phantom-joker/card.png',ringSprite='assets/design/effects/phantom-joker/ring.png',projectileDisplaySize=[72,108],ringDisplaySize=[158,158],")
text=text.replace("'projectileSprite':str(effect),", "'projectileSprite':str(effect),'ringSprite':str(ring),'cardDisplayScaleChange':1.5,")
p.write_text(text,encoding='utf-8')

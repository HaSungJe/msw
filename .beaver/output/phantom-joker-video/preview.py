from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,shutil
r=Path(__file__).parent;project=r.parents[2]
durations=[.06,.05,.04,.06,.04,.05,.05,.05]
meta={'order':list(range(1,9)),'times':durations,'loopDuration':.4,'bodyRotation':False,'facing':'left','referenceVideo':'bandicam 2026-09-27 11-31-51-790.mp4','referencePosesSeconds':[2.333,2.5],'releasePoints':{'low':[210,440],'high':[216,424]},'previewCardInterval':.1,'previewCardFlight':1.05,'gameIntegration':False,'cardDisplaySize':[288,432],'ringDisplaySize':[632,632],'projectileSprite':'assets/design/effects/phantom-joker/card.png','ringSprite':'assets/design/effects/phantom-joker/ring.png'}
(r/'playback.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>팬텀 조커 수정</title><style>body{font:16px system-ui;background:#edf0f6;color:#202634;margin:24px}h1{font-size:25px}canvas{display:block;width:min(100%,1100px);background:#e5e7ed;border-radius:12px}button,select{font:inherit;padding:9px;border:1px solid #b8c1d2;border-radius:6px;background:white;margin:5px}video{width:min(100%,976px)}p{line-height:1.5}</style><h1>팬텀 · 조커</h1><p>다리 간격과 무릎·상체 반동을 조정했습니다. 큰 카드와 원형 소용돌이는 각각 별도 이미지입니다. 게임 연결 전 미리보기입니다.</p><button id="play">일시정지</button><button id="again">다시 재생</button><select id="speed"><option value="1">원래 속도</option><option value=".5">0.5배</option><option value=".25">0.25배</option></select><label><input id="cards" type="checkbox" checked>카드 표시</label><label><input id="flip" type="checkbox">좌우 반전</label><canvas width="1280" height="740"></canvas><p id="caption"></p><input id="seek" type="range" min="0" max="3550" value="0" style="width:min(100%,1100px)"><h2>사용자 참고 영상</h2><video controls src="reference.mp4"></video><script>
const times=[.06,.05,.04,.06,.04,.05,.05,.05],imgs=Array.from({length:8},(_,i)=>{let im=new Image();im.src=`normalized/motion${String(i+1).padStart(2,'0')}.png`;return im}),idle=new Image(),card=new Image(),ring=new Image();idle.src='../../../assets/design/characters/phantom/frames/wait/motion01.png';card.src='card.png';ring.src='ring.png';const canvas=document.querySelector('canvas'),c=canvas.getContext('2d');let t=0,last=performance.now(),running=true,speed=1;function pose(t){let u=((t-.35)%.4+.4)%.4;for(let i=0;i<8;i++){if(u<times[i])return i;u-=times[i]}return 7}function draw(){c.clearRect(0,0,1280,740);c.save();if(document.querySelector('#flip').checked){c.translate(1280,0);c.scale(-1,1)}c.strokeStyle='#b8c1d0';c.beginPath();c.moveTo(0,661);c.lineTo(1280,661);c.stroke();let active=t>=.35&&t<2.75,idx=pose(t);let im=active?imgs[idx]:idle;if(im.complete&&im.naturalWidth){if(active)c.drawImage(im,450,20,704,704);else c.drawImage(im,514,148,576,576)}if(document.querySelector('#cards').checked&&card.complete){for(let j=0;j<23;j++){let born=.50+j*.1,age=t-born;if(age<0||age>1.05)continue;let lane=j%3-1,phase=j*2.094;let x=660-age*660,y=450-age*48+Math.sin(age*9+phase)*(18+age*32)+lane*16;let fade=Math.min(1,age/.035,(1.05-age)/.16);c.save();c.globalAlpha=Math.max(0,fade);c.translate(x,y);c.save();c.rotate(age*5+phase);if(ring.complete&&ring.naturalWidth)c.drawImage(ring,-316,-316,632,632);c.restore();c.rotate(-age*8+phase*.3);let w=288*(.6+.4*Math.abs(Math.cos(age*7+phase)));c.drawImage(card,-w/2,-216,w,432);c.restore()}}c.restore();document.querySelector('#caption').textContent=active?`연속 투척 · ${idx+1}/8 프레임`:'대기';document.querySelector('#seek').value=t*1000}function tick(now){let dt=Math.min(.08,(now-last)/1000);last=now;if(running)t=(t+dt*speed)%3.55;draw();requestAnimationFrame(tick)}requestAnimationFrame(tick);document.querySelector('#play').onclick=e=>{running=!running;e.target.textContent=running?'일시정지':'재생'};document.querySelector('#again').onclick=()=>{t=0;running=true;document.querySelector('#play').textContent='일시정지'};document.querySelector('#speed').onchange=e=>speed=Number(e.target.value);document.querySelector('#seek').oninput=e=>{t=Number(e.target.value)/1000;running=false;document.querySelector('#play').textContent='재생';draw()};
</script></html>'''
(r/'preview.html').write_text(html,encoding='utf-8')
if not (r/'reference.mp4').exists():shutil.copyfile('C:/Users/timec/Documents/Bandicam/bandicam 2026-09-27 11-31-51-790.mp4',r/'reference.mp4')
# Raster preview rendering of the finished sprite animation; no body tweening or morphing.
W,H=960,555;scale=.75;body=[Image.open(r/'normalized'/f'motion{n:02}.png').convert('RGBA').resize((528,528),Image.Resampling.LANCZOS) for n in range(1,9)];idle=Image.open(project/'assets/design/characters/phantom/frames/wait/motion01.png').convert('RGBA').resize((432,432),Image.Resampling.LANCZOS);card=Image.open(r/'card.png').convert('RGBA');ring=Image.open(r/'ring.png').convert('RGBA').resize((474,474),Image.Resampling.LANCZOS);frames=[]
for k in range(89):
 t=k*.04;out=Image.new('RGBA',(W,H),'#e5e7ed');d=ImageDraw.Draw(out);d.line((0,496,W,496),fill='#b8c1d0')
 active=.35<=t<2.75;u=(t-.35)%.4;idx=7
 for i,dt in enumerate(durations):
  if u<dt:idx=i;break
  u-=dt
 if active:out.alpha_composite(body[idx],(338,15))
 else:out.alpha_composite(idle,(386,111))
 for j in range(23):
  age=t-(.50+j*.1)
  if not 0<=age<=1.05:continue
  phase=j*2.094;lane=j%3-1;x=(660-age*660)*scale;y=(450-age*48+math.sin(age*9+phase)*(18+age*32)+lane*16)*scale;fade=max(0,min(1,age/.035,(1.05-age)/.16))
  fx=Image.new('RGBA',(720,720));halo=ring.rotate(-math.degrees(age*5+phase),resample=Image.Resampling.BICUBIC,expand=True);halo.putalpha(halo.getchannel('A').point(lambda a:int(a*fade)));fx.alpha_composite(halo,((720-halo.width)//2,(720-halo.height)//2))
  cw=max(1,int(288*scale*(.6+.4*abs(math.cos(age*7+phase)))));sprite=card.resize((cw,324),Image.Resampling.LANCZOS).rotate(math.degrees(age*8-phase*.3),resample=Image.Resampling.BICUBIC,expand=True);sprite.putalpha(sprite.getchannel('A').point(lambda a:int(a*fade)));fx.alpha_composite(sprite,((720-sprite.width)//2,(720-sprite.height)//2));out.alpha_composite(fx,(round(x)-360,round(y)-360))
 frames.append(out.convert('RGB'))
frames[0].save(r/'preview.gif',save_all=True,append_images=frames[1:],duration=40,loop=0,optimize=False)
frames[33].save(r/'preview-still.png')
print('interactive/video-reference preview and 89-frame GIF saved')

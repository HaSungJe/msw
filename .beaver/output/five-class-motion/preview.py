from pathlib import Path
import json

root=Path(__file__).parent
plan=json.loads((root/'plan.json').read_text(encoding='utf-8'))
names={'paladin':'팔라딘','dark-knight':'다크나이트','night-lord':'나이트로드','shadower':'섀도어','phantom':'팬텀'}
seqs=[]
for cid in names:
    seqs.append({'id':cid,'skill':'wait','ko':'대기','order':[1,2,1,3],'times':[.65,.45,.65,.45]})
for row in plan['sequences']:
    s={'id':row['id'],'skill':row['skill'],'ko':row['ko'],'order':list(range(1,len(row['poses'])+1)),'times':row['durations'],'hit':row.get('hit',[]),'delay':row.get('motionDelay',0)}
    if row['skill']=='quadruple-throw':
        s['order']=[1,2,3,4,5,6,5,6,7,8]
        s['times']=[.10,.05,.05,.05,.05,.05,.05,.05,.10,.15]
    if row['skill']=='savage-blow':
        s['order']=[1,2,3,4,5,6,4,5,7,8]
        s['times']=[.10,.05,.05,.05,.05,.05,.05,.05,.03,.02]
    if row['skill']=='meso-explosion':
        s['times']=[.12,.18,.07,.08,.05]
    if row['skill']=='joker':
        s['order']=list(range(1,9))*6
        s['times']=[.06,.05,.04,.06,.04,.05,.05,.05]*6
        s['loopOrder']=list(range(1,9));s['loopTimes']=[.06,.05,.04,.06,.04,.05,.05,.05]
        s['bodyRotation']=False;s['projectileDirection']='left';s['caneGrip']='neck-below-handle-suspended'
    seqs.append(s)
(root/'playback.json').write_text(json.dumps(seqs,ensure_ascii=False,indent=2),encoding='utf-8')
cards=''.join('<article data-id="'+cid+'"><h2>'+name+'</h2><select>'+''.join('<option value="'+s['skill']+'">'+s['ko']+'</option>' for s in seqs if s['id']==cid)+'</select><canvas width="704" height="704"></canvas><p class="caption"></p><div class="buttons"><button class="play">일시정지</button><button class="step">한 프레임</button><label><input class="flip" type="checkbox">반대 방향</label></div><input class="seek" type="range" min="0" max="1000" value="0"><p class="hint"></p></article>' for cid,name in names.items())
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>5직업 모션 미리보기</title><style>body{margin:24px;background:#f0f0f5;color:#202634;font:16px system-ui}h1{font-size:26px}p{line-height:1.5}.toolbar{position:sticky;top:0;background:#f0f0f5ee;padding:12px;z-index:2}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:18px}article{background:white;border:1px solid #d8dce5;border-radius:16px;padding:16px}h2{margin:0 0 10px;font-size:22px}select{width:100%;padding:10px;border:1px solid #c9cddd;border-radius:8px;font:inherit}canvas{width:100%;display:block;background:#e2e4eb;border-radius:10px;margin-top:12px}.caption,.hint{font-size:13px;min-height:20px}.buttons{display:flex;gap:8px;align-items:center}button{padding:8px;border:1px solid #ccd1dc;border-radius:6px;background:#edf1fa;font:inherit}.seek{width:100%}.hint{color:#596477}label{white-space:nowrap}</style><h1>5직업 대기·스킬 모션</h1><p>승인 원화 · 비숍 공통 그림체와 비율. 캐릭터 프레임 미리보기이며 게임 연결 전입니다. 카드 투사체·공격 이펙트·분신·타격음은 기존 게임에서 별도로 재생하는 요소입니다.</p><div class="toolbar"><label>재생 속도 <select id="speed" style="width:110px"><option value=".25">0.25배</option><option value=".5">0.5배</option><option selected value="1">1배</option><option value="1.5">1.5배</option></select></label> <button id="all">모두 다시 재생</button></div><div class="grid">'''+cards+'''</div><script>const sequences=DATA;const states=[];const cache=new Map();let speed=1;function image(src){if(!cache.has(src)){let im=new Image();im.src=src;cache.set(src,im)}return cache.get(src)}
function list(st){const s=sequences.find(s=>s.id===st.id&&s.skill===st.select.value);let a=[];if(s.skill!=='wait')a.push({skill:'wait',n:1,t:.55+(s.delay||0)});s.order.forEach((n,i)=>a.push({skill:s.skill,n,t:s.times[i]}));if(s.skill!=='wait')a.push({skill:'wait',n:1,t:.6});return a}
function draw(st){let a=list(st),total=a.reduce((v,f)=>v+f.t,0);st.t=((st.t%total)+total)%total;let elapsed=0,idx=0;for(let i=0;i<a.length;i++){if(st.t<elapsed+a[i].t){idx=i;break}elapsed+=a[i].t}const f=a[idx],src=`normalized/${st.id}/${f.skill}/motion${String(f.n).padStart(2,'0')}.png`,im=image(src);const c=st.ctx;c.clearRect(0,0,704,704);c.strokeStyle='#9ba5b7';c.beginPath();c.moveTo(0,641);c.lineTo(704,641);c.stroke();c.save();if(st.flip.checked){c.translate(704,0);c.scale(-1,1)}if(im.complete&&im.naturalWidth){if(f.skill==='wait')c.drawImage(im,64,128,576,576);else c.drawImage(im,0,0,704,704)}c.restore();st.caption.textContent=`${f.skill==='wait'?'대기':st.select.selectedOptions[0].text} · 프레임 ${String(f.n).padStart(2,'0')} · ${st.t.toFixed(2)}초 / ${total.toFixed(2)}초`;st.seek.value=st.t/total*1000;st.index=idx;st.frames=a;st.total=total}
for(const el of document.querySelectorAll('article')){const st={id:el.dataset.id,select:el.querySelector('select'),ctx:el.querySelector('canvas').getContext('2d'),caption:el.querySelector('.caption'),seek:el.querySelector('.seek'),flip:el.querySelector('.flip'),play:el.querySelector('.play'),hint:el.querySelector('.hint'),t:0,running:true};st.select.onchange=()=>{st.t=0;st.hint.textContent=st.select.value==='joker'?'준비 → 회전 8장 × 3회 → 복귀. 카드 발사 주기와 몸 회전 주기는 별도.':st.select.value==='spear-buster'?'시전 후 0.5초 준비를 거쳐 찌르기. 기존 판정 0.65·0.80·0.95초 기준.':''};st.play.onclick=()=>{st.running=!st.running;st.play.textContent=st.running?'일시정지':'재생'};el.querySelector('.step').onclick=()=>{st.running=false;st.play.textContent='재생';const next=(st.index+1)%st.frames.length;st.t=st.frames.slice(0,next).reduce((v,f)=>v+f.t,0)+.001;draw(st)};st.seek.oninput=()=>{st.running=false;st.play.textContent='재생';st.t=Number(st.seek.value)/1000*st.total;draw(st)};states.push(st);draw(st)}document.querySelector('#speed').onchange=e=>speed=Number(e.target.value);document.querySelector('#all').onclick=()=>states.forEach(s=>{s.t=0;s.running=true;s.play.textContent='일시정지'});let last=performance.now();function tick(now){let dt=Math.min(.1,(now-last)/1000);last=now;for(const st of states){if(st.running)st.t+=dt*speed;draw(st)}requestAnimationFrame(tick)}requestAnimationFrame(tick);</script></html>'''.replace('DATA',json.dumps(seqs,ensure_ascii=False))
html=html.replace('normalized/${st.id}/${f.skill}/','../../../assets/design/characters/${st.id}/frames/${f.skill}/')
html=html.replace('준비 → 회전 8장 × 3회 → 복귀. 카드 발사 주기와 몸 회전 주기는 별도.','영상 기준 8장 연속 투척. 몸 회전 없음. 케인은 목을 쥐고 띄워 듦.')
html=html.replace('<div class="grid">','<p><a href="../phantom-joker-video/preview.html">팬텀 카드 연사 포함 · 원본 영상 비교</a></p><div class="grid">')
(root/'preview.html').write_text(html,encoding='utf-8')
print('14 playback sequences and preview saved')

from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
root=Path(__file__).parent
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',22)
small=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',14)
# Approximate anatomical landmarks inspected on the 1280px tool previews.
# Hats, weapons, hair spikes and cape hems are excluded from height alignment.
rows=[('bishop','비숍 기준',None),('paladin','팔라딘',(180,610,1170,650)),('dark-knight','다크나이트',(240,645,1170,585)),('night-lord','나이트로드',(230,645,1170,565)),('shadower','섀도어',(175,600,1115,595)),('phantom','팬텀',(350,705,1190,635))]
board=Image.new('RGBA',(2880,640),(235,235,239,255))
draw=ImageDraw.Draw(board)
landmarks=[]
for i,(name,label,lm) in enumerate(rows):
    cell=Image.new('RGBA',(480,570),(0,0,0,0))
    if name=='bishop':
        im=Image.open('assets/design/characters/bishop/frames/wait/motion01.png').convert('RGBA')
        scale=135/147; x=288; sole=512
    else:
        im=Image.open(root/'concepts'/f'{name}.png').convert('RGBA')
        f=im.width/1280; crown,chin,sole,x=[v*f for v in lm]
        scale=135/(chin-crown)
        landmarks.append({'id':name,'crown':crown,'chin':chin,'sole':sole,'foot_center_x':x,'heads':round((sole-crown)/(chin-crown),2),'approximate':True})
    thumb=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    cell.alpha_composite(thumb,(round(240-x*scale),round(535-sole*scale)))
    board.alpha_composite(cell,(i*480,35))
    draw.text((i*480+240,18),label,font=font,fill='#20242c',anchor='mt')
    draw.line((i*480+8,570,(i+1)*480-8,570),fill='#a9aeb9',width=1)
    if i: draw.line((i*480,0,i*480,605),fill='#d5d6dd',width=1)
draw.text((30,610),'머리 길이와 발 기준선을 맞춘 원화 검토용 비교 · 모자/깃털/무기는 신체 높이에서 제외 · 모션/게임 연결 전',font=small,fill='#404756')
board.convert('RGB').save(root/'comparison.jpg',quality=95)
(root/'landmarks.json').write_text(json.dumps(landmarks,ensure_ascii=False,indent=2),encoding='utf-8')
cards=''.join(f'<article><h2>{label}</h2><a href="concepts/{name}.png"><img src="concepts/{name}.png"></a></article>' for name,label,_ in rows[1:])
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>5직업 원화 검토</title><style>body{margin:32px;font:16px system-ui;background:#eeeef2;color:#20242c}h1{font-size:26px}p{line-height:1.6}.compare{width:100%}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}article{background:#dddde5;border-radius:14px;padding:20px}article img{width:100%}h2{font-size:20px}a{color:#235bb8}</style><h1>팔라딘 · 다크나이트 · 나이트로드 · 섀도어 · 팬텀</h1><p>비숍 작화·인체비율 기준의 원화 검토본. 기존 승인 원화는 보존했습니다. 현재 단계는 원화 후보이며 모션 제작·리소스 연결은 아직 진행하지 않았습니다.</p><img class="compare" src="comparison.jpg"><div class="grid">'''+cards+'''</div><h2>팬텀 조커 참고 영상</h2><p>제자리 몸 회전, 붉은·금빛 잔상, 전방 나선 카드 흐름을 관찰했습니다. 원화에는 짙은 적갈색 바탕·금색 테두리·중앙 별 문양의 카드 뒷면을 반영했습니다. 모션은 원화 확정 뒤 준비·회전 루프·복귀로 제작합니다.</p><a href="reference/joker-contact.png">영상 전체 흐름</a> · <a href="reference/joker-body.png">캐릭터 회전 확대</a> · <a href="phantom-video-study.md">관찰 기록</a></html>'''
(root/'review.html').write_text(html,encoding='utf-8')
print(json.dumps(landmarks,ensure_ascii=False))

# 자쿰의 제단 — 액션 테마 시안

- 상태: 게임 구현·리소스 업로드 완료 — 원화 기반 레이어 애니메이션, MP4 미제작
- 사용자 요청: 자쿰과 제단을 함께 그린 테마. 팔을 움직이는 10초 미만 영상이 무한 반복된다.
- 제안: 8초, 고정 카메라, 16:9 배경. 길이·동작 순서·무음은 이번 시안의 제안값이며 사용자 확정값이 아니다.
- 대상: 개인 테마의 풍경 배경과 유저 카드 배경에서 함께 재생한다. 테마 선택 목록만 정지 원화를 사용한다.
- 원화: [keyframe.png](../../assets/design/themes/action/zakum-altar/keyframe.png), 1672×941 PNG. 영상 목표 해상도와는 다르다.
- 제작: 내장 imagegen. 최초 시안은 외형이 원작과 다르다는 사용자 피드백으로 교체했다. 현재 원화는 사용자가 직접 제공한 자쿰 이미지를 외형 기준으로 삼아 다시 그린 것이다.

## 현재 게임 적용

- 프로필 설정 → 테마 → 액션 → 자쿰의 제단. 기본 테마5종과 같은 무료 선택이며 기존 기본값 헤네시스는 유지한다.
- `RtsActionThemeLogic`가 클라이언트에서 팔8개·몸통1개·화로 불꽃8개를 구성한다. 팔은 개별 위상으로 회전하고 불꽃은 높이·기울기·밝기가 변한다. 현재 팔꿈치를 별도 관절로 굽히거나 용암을 유동시키는 동작은 구현하지 않았다.
- 8초 주기, 최대30fps 갱신. 월드와 유저 카드는 같은 시간·포즈 계산을 사용한다. 유저 카드의 아이콘·닉네임은 고정한다.
- 카메라·몸통·제단은 고정한다. 현재 관전 구역만 월드 레이어를 만들고 테마 변경·카드 재생성·Play 종료 때 정리한다. 배경/트랙은 기존 서버 테마 경로를 사용하며 움직임에는 RPC를 쓰지 않는다.
- 자산과 RUID는 `assets/design/themes/action/zakum-altar/resources.json`. 트랙은 기존 경로 그대로 화산석 색상을 적용했다.
- 검증: Maker build 오류0·기존 경고8. 배경·카드 각각17개 레이어, 같은 팔 회전값이 -10.553°에서0.172°로 변하는 로그와 화면을 확인했다. 임시 미리보기 복구 후 scenes=0. 전체 사용자 테마 변경 검증은 자동 승인 검토가 차단해 실행하지 않았으며, 현재 클라이언트의 배경·내 카드만 임시 변경하고 복구했다. 계정 저장값은 변경하지 않았다. 정리용 MakerScript의 배열 인덱스 오류1건은 nil 검사 후 정리 완료했다.
- 멀티플레이 동시 사용자, 실제 선택 저장 후 재접속 검증은 이번 범위에서 수행하지 않았다.

## 원화의 시각 방향

사용자 피드백 반영: 자쿰의 아기자기한 그림체에 배경도 맞춘다. 자쿰 외형은 유지하며 제단·기둥·바닥·동굴을 둥글고 큼직한 형태, 단정한 외곽선, 부드러운 음영으로 통일했다. 용암은 선명하고 매끈한 주황·금빛 흐름으로, 불꽃은 단순한 카툰 형태로 그린다. 거친 실사 질감·날카로운 바위·지나치게 어두운 붉은 대비는 줄인다. 영상에서도 이 배경 그림체를 유지한다.

자쿰의 관·얼굴·석판·뿌리와 제단이 한 화면에 들어온다. 바깥팔 여덟 개를 개별적으로 읽을 수 있게 배치하고 석판을 잡은 중앙의 작은 손은 고정한다. 붉은 용암 동굴, 오래된 석재 제단과 기둥, 불빛을 함께 그린다. 그림체는 기존 마을 풍경과 이어지는 매끈한 2D 게임 일러스트다.

외형의 기준은 사용자 첨부 이미지다. 낮은 반원형 금빛 관, 작은 상단 얼굴과 층층이 쌓인 넓은 석상 몸통, 둥근 돌 장식, 뭉툭하고 굵은 갈색 팔과 주먹, 앞쪽 석판과 금빛 손목 고리를 유지한다. 커다란 인간형 얼굴·근육질 원통형 팔·길게 뻗은 금빛 관으로 바꾸지 않는다. 영상에서도 이 형태를 고정한다.

영상에서 몸통과 제단은 고정하고 바깥팔·손목의 움직임을 주된 볼거리로 삼는다. 팔이 단순히 떨리는 수준에 머물지 않도록 팔꿈치를 굽혔다 펴고 높이를 교차한다. 손은 화면 밖으로 나가거나 이웃 팔과 융합하지 않는다. 용암·불꽃·불씨는 보조 움직임으로 둔다.

카메라는 이동·줌·흔들림 없이 고정한다. 플레이어·전투판·격자·UI·자막·로고는 원화와 영상에 그리지 않는다. 전투판을 겹쳐 볼 아래쪽은 비교적 차분한 석재 바닥으로 둔다.

## 초기 영상 연출 제안 (아래 관절·용암 동작은 미구현)

| 구간 | 팔의 동작 | 배경 |
|---|---|---|
| 0–2초 | 위쪽 팔들이 차례로 올라가고, 아래쪽 팔은 바깥으로 벌어진다. 좌우에 짧은 시간차를 둔다. | 용암과 화로가 계속 움직이고 불씨가 천천히 오른다. |
| 2–4초 | 위쪽 팔이 접히는 동안 중간·아래 팔이 크게 올라간다. 손목을 약간 회전해 여덟 팔의 움직임이 구분된다. | 불빛이 천천히 밝아지되 화면 전체를 번쩍이지 않는다. |
| 4–6초 | 반대쪽에서 시작하는 물결처럼 팔을 차례로 펼친다. 좌우 모두 같은 순간에 정지하지 않는다. | 몸통과 제단의 형태는 고정한다. |
| 6–8초 | 각 팔이 시작 자세로 자연스럽게 이어진다. 마지막에 일제히 멈추거나 역재생한 듯 꺾이지 않는다. | 밝기·불씨 밀도도 시작 구간과 연결한다. |

## 향후 MP4 영상 제작 조건

- 납품 목표: 1920×1080, 24fps, 8초(192프레임), 무음 MP4. 현재 PNG는 원화이며 영상 파일이 아니다.
- 첫·끝의 팔 위치뿐 아니라 이동 속도와 방향도 이어지게 만든다. 끝 프레임을 중복 삽입해 정지 구간을 만들지 않는다.
- 역재생으로 불꽃·불씨가 거꾸로 흐르는 방식은 피한다.
- 팔 수·손가락·얼굴·관·석판이 프레임 사이에 변형되지 않아야 한다.
- 루프를 최소 3회 이어 보며 경계의 튐·팔 융합·갑작스러운 노출 변화를 확인한다.
- 현재 세션에는 영상 생성 도구가 연결되어 있지 않아 MP4 생성 및 위 검증은 수행하지 않았다.

### 영상 도구에 전달할 프롬프트

첨부 원화의 자쿰과 제단을 유지한 8초짜리 무한 반복 배경 영상. 카메라는 완전히 고정한다. 왼쪽 네 개와 오른쪽 네 개의 거대한 바깥팔을 차례로 크게 들어 올리고, 팔꿈치를 접었다 펴며, 좌우가 교대로 물결치듯 움직인다. 석판을 잡은 중앙의 작은 손과 몸통, 관, 얼굴, 뿌리, 제단, 기둥은 형태와 위치를 유지한다. 위팔이 내려오면 아래팔이 올라가며 팔들이 서로 다른 속도로 연결된 한 주기를 만든다. 모든 팔과 손을 화면 안에 유지하고 팔이 늘어나거나 사라지거나 합쳐지지 않게 한다. 용암은 천천히 흐르고 화로의 불꽃은 흔들리며 불씨가 위로 오른다. 처음과 끝의 팔 자세, 움직임의 방향과 속도, 조명이 자연스럽게 연결되어 반복 경계가 드러나지 않는다. 원화의 2D 일러스트 그림체와 구도를 유지한다. 화면 전환, 줌, 카메라 흔들림, 슬로모션 전환, 자막, UI, 추가 인물, 얼굴 변형, 팔 수 변화, 영상 역재생 없음.

## 게임 적용 시 확인할 것

기본 배경은 `RtsThemeLogic.GetPresets`의 `backgroundRUID`를 `ApplyToZone`에서 `RtsZoneLogic.SetZoneBackground`로 전달한다. 자쿰은 해당 배경을 인식한 `RtsActionThemeLogic`가 클라이언트 레이어를 더한다. MP4 재생 기능은 사용하지 않는다.

테마 변경·관전 구역 이동 시 장식을 정리한다. UI 카드는 원화 비율로 렌더링해 카드 마스크 안에 표시한다.

Maker에서 트랙 뒤의 팔과 몸통, 유저 카드 배경을 확인했다. 트랙이 자쿰 얼굴과 팔 일부를 가리는 것은 현재 전투판 배치의 한계이며 전투 경로를 바꾸지 않았다.

## 참고와 제작 기록

### 배경 그림체 보정 — 현재 원화

내장 imagegen으로 자쿰을 유지하고 배경을 같은 아기자기한 2D 그림체로 보정했다. 사용 프롬프트:

```text
Edit the attached Zakum altar illustration. User request: the central Zakum already has a cute, charming, chunky MapleStory cartoon illustration style, but the background is too harsh and realistic; make the ENTIRE BACKGROUND AND ALTAR match Zakum's charming style.

PRESERVE the existing central Zakum character exactly: the low semicircular gold crown, small upper face, stacked rectangular stone totem body, round stone ornaments, all outer arms and fists, central plaque and golden wrist ring, proportions, pose, scale and position. Do not redesign or cute-ify Zakum any further. The character is the style reference for everything else.

Restyle the environment substantially while preserving the scene layout and subject matter: volcanic cavern with lava, old stone altar steps and columns, roots, braziers and foreground stone floor. Draw these with rounded chunky silhouettes, softly bevelled stone blocks, simpler large shapes, tidy expressive outlines, gently painted shadows and warm, inviting MapleStory fantasy colors. Make the architecture miniature and charming in its detailing, with pleasing rounded edges and coherent illustrated proportions. Simplify excessive tiny cracks, sharp black stalactites, jagged rubble, grungy textures and photorealistic surface noise. Lava should look like smooth luminous orange and golden ribbons and softly bubbling pools, with a few small stylized flame shapes instead of walls of raging inferno. Pillars and steps should feel carved from warm brown and muted mauve rounded blocks, with simple spiral carvings matching the idol. Roots become smooth curved stylized roots, not horror tendrils. Reduce the oppressive black/red darkness and harsh contrast; make environment details pleasantly readable under soft warm amber light, with mauve-brown cavern shadows. Retain a recognizable underground lava temple atmosphere, not outdoors, not candyland, no pastel pink makeover, no new greenery, no added creatures or props.

Style coherence is the main goal: the altar, cavern, floor and Zakum should all look painted by the same artist for one charming polished 2D MapleStory game background. Preserve the same fixed frontal wide composition, full character inside frame, the open calm stone-floor foreground and the landscape aspect ratio. No camera movement, no text, no UI, no labels, no watermark. One complete still keyframe.
```

### 자쿰 외형 보정 기록

- 캐릭터 외형 참고: 사용자가 이 대화에 첨부한 자쿰 이미지. 이미지 편집에 실제 참조 입력으로 사용했다.
- 기존 프로젝트 스타일 확인: `assets/design/themes/scenery/perion-scene-source.png`.
- 아래는 현재 원화의 편집 프롬프트다. 첫 입력은 기존 제단 시안, 두 번째 입력은 사용자 첨부 자쿰 이미지다.

```text
Edit image 1 (the cavern and altar concept) using image 2 as the AUTHORITATIVE character design reference for MapleStory's Zakum. The user says the statue in image 1 does not look like Zakum. Replace the whole central idol and all its arms to faithfully match the exact character in image 2. Preserve image 1's volcanic cavern, stepped altar, wide composition, warm lighting, clean 2D illustrated environment, fixed camera, and calm foreground. Image 2 is a character-design reference, NOT an object to paste in with its white background.

Critical character fidelity: Zakum is a squat, stacked architectural stone totem, NOT a humanoid golem with a broad human face or muscular torso. Precisely follow image 2's silhouette, facial carvings, block divisions, body proportions, arm shapes, hands, bracelets and stone plaque. The crown is a LOW, curved semicircular gold fan / arched halo behind the narrow upper head, with many short gold segments around a round dark inner disk, not tall rectangular golden sun rays or an Aztec feather headdress. Beneath that is a SMALL narrow upper carved face/head over a projecting horizontal stone muzzle with the distinctive row of round stone teeth/tusks seen in the reference. The torso is a WIDE RECTANGULAR stacked stone pillar with engraved panels and round stone protrusions across its upper front. The lower front holds the angular rectangular stone plaque with small squared stone hands and the prominent GOLD / ORANGE wrist ring visible on the viewer-right in the reference. Body stone is muted gray with weathered green-gray nuances. The enormous outer arms are dark earth-brown gnarled carved rootlike stone, broad irregular clustered segments with spiral engravings and big clenched fists, NOT cylindrical muscular human arms with long individual fingers. Their raised silhouettes frame the body and the top outer fists reach above the crown. Copy the reference's recognizable silhouette and poses carefully, keeping the arm structure coherent and the full outer silhouette inside frame. Rebuild the idol from this reference; do not preserve the incorrect face, crown, tablet, spread-finger hands, muscular arm anatomy, or proportions from image 1.

Paint the reference character faithfully at higher resolution, integrated with the altar lighting. This is still a MapleStory 2D game illustration, with readable stylized shapes and original character identity, not a realistic stone sculpture. Maintain the full altar and cavern setting. No other characters, no added props, no text, no labels, no numbers, no watermark, no UI, no motion blur. One 16:9 landscape still keyframe.
```

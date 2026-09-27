# 보우마스터 원화 수정 프롬프트

내장 이미지 생성 도구 사용. 이미지 순서: 보우마스터 기존 concept.png → 비숍 현재 concept.png → 비숍 wait/motion01.png.

참조 SHA256:
- 보우마스터 수정 전: `3eeeb1bc6fc94f0497cb850af8c0ee83eb86f224e90d6603c7d0808370c1f3cc`
- 비숍 원화: `06c5a96b1c8dd24d94385e7e29ef56aea9bf22439460e1f02e25d068c49b454c`
- 비숍 대기: `7949a8bdfd86a72d5ef45c67856df447f4c2e319eb5e9a6978d8800648e45849`

실제 생성 프롬프트:

```text
Use case: style-transfer. Edit image 1, the Bowmaster character concept. Image 2 is the Bishop finished concept, image 3 is the Bishop standing game frame. Deliver ONLY ONE finished full-body Bowmaster on genuinely transparent background, square canvas with comfortable margins.
Reference roles: Image 1 locks Bowmaster identity, outfit, palette, equipment and gentle closed-mouth smile. Images 2 and 3 lock the common drawing style and anatomy. Match the Bishop's exquisite clean 2D chibi linework, smooth modest cel shading, crisp eyes and delicate small mouth, WITHOUT changing the Bowmaster into the Bishop.
Keep faithfully: deep burgundy/plum long wavy hair with braided crown, white feather ornament with red-orange gem on viewer-right, fresh yellow-green eyes, fair skin, calm small closed-mouth smile; forest-green scarf and cape with ivory/gold edging, brown and gold shoulder armor, dark leather tunic and waist belt, ivory sleeves, leather wrist guards, brown boots with gold diamond ornaments, back quiver with white-fletched arrows. Keep the ornate long curved bow in gold, ivory and forest green with two turquoise inset gems and fine visible bowstring. Same gentle three-quarter orientation and relaxed two-handed lowered bow pose as image 1. No nocked arrow or new effects.
CRITICAL ANATOMY CHANGE: current image 1 legs and boots are too long. Redraw actual anatomy, not just scale the whole image. Match Bishop image 3: approximately 2.3 head lengths from anatomical crown to soles, excluding feather/hair tips. Large rounded head, short neck, compact narrow shoulders and torso, SHORT thighs, SHORT shins and especially SHORT compact boots and small feet. Shorten the legs and boots enough that the head takes roughly 43-45% of crown-to-sole height. Below tunic hem to sole should occupy approximately 20-22% of crown-to-sole height, not the long 30% segment in image 1. The boots should be modest little boots, not tall broad adult riding boots. Keep the same detailed boot design miniaturized. Forearms and hands remain compact like Bishop. Keep head width and round cheek shape readable. No mature elongated figure, long waist or exaggerated hips. Preserve Bowmaster's distinctive eye shape and personality.
COMPOSITION: quiet natural upright stance, feet close and comfortably grounded, no extreme perspective. Let the bow angle downward across the body as in source, but both compact feet and leg silhouette must be visible. Hair, feather and bow may extend beyond the body naturally but never determine anatomical scaling. Entire feather, hair, bow and both soles inside the image. Similar high-quality detailed finish to Bishop concept, clean silhouette readable in small game scale. No background, ground shadow, border, text, labels, grids, watermarks or extra figures. Output single polished revised concept ready to become the source of all subsequent motion frames and bust portrait.
```

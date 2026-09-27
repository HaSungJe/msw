# 팔라딘·다크나이트·나이트로드·섀도어·팬텀 원화 검토본

2026-09-27 사용자 요청. `docs/unit-art.md`와 `unit-art-prompts.md`의 비숍 공통 작화·인체비율 기준을 적용했다.

## 현재 상태

사용자가 5종을 각 직업 폴더에 저장하도록 요청해 **`assets/design/characters/<id>/concept.png`에 반영했다.** 팬텀은 사용자가 선택한 아래쪽 마지막 비율 수정본(`exec-18037e5c-2632-4076-9046-6e89e4100183.png`)이다. 이전 원화는 `.beaver/output/five-class-design/previous-concepts/`에 보관했다. 대기·공격 PNG 78장은 [5직업 모션 기록](five-class-motion.md)에 따라 직업별 폴더에 저장했다. 흉상·게임 리소스 연결은 아직 완료되지 않았다.

- 검토 페이지: [review.html](../../.beaver/output/five-class-design/review.html)
- 비숍과 비교: [comparison.jpg](../../.beaver/output/five-class-design/comparison.jpg)
- 원화 후보: `.beaver/output/five-class-design/concepts/{paladin,dark-knight,night-lord,shadower,phantom}.png`
- 실제 첨부 기준 이미지와 SHA256: `.beaver/output/five-class-design/references.json`
- 생성 도구: 내장 ImageGen. 프롬프트: 같은 작업 폴더의 `<id>-generation.json`, 팬텀·섀도어 추가 수정은 `<id>-revision.json`.
- 결과 크기·알파 경계·SHA256: `manifest.json`. 모두 투명 PNG 1254×1254.

## 반영 내용

승인 원화의 얼굴·헤어·눈색·표정·의상·고유 무기를 유지하면서 비숍과 어울리는 짧은 몸통·팔다리로 재작화했다. 다크나이트 비홀더는 넣지 않았다. 팬텀은 큰 모자를 머리 길이에 포함하지 않도록 추가 보정했고, 섀도어도 과하게 커진 머리를 추가 보정했다.

비교 이미지는 머리 길이와 발 기준선을 근사 정렬한 검토용이다. 모자에 가려진 정수리·마스크 안의 턱은 추정이므로 `landmarks.json` 수치는 정밀한 해부학적 실측이 아니다. 원본 PNG의 실제 크기와 게임용 표시 크기도 다르다. 후속 대기 1장을 576×576/발 중심 (288,512)로 제작해 비숍과 다시 검수해야 한다.

## 팬텀 조커

새 사용자 영상 `bandicam 2026-09-27 11-31-51-790.mp4`는 7.433초/976×404/30fps다. 전체 흐름과 캐릭터 확대 프레임을 따로 관찰했다. [영상 관찰 기록](../../.beaver/output/five-class-design/phantom-video-study.md)을 따른다.

- 원화 카드: 적갈색 바탕·금색 테두리·모서리 장식·중앙 별 문양, 손에 든 3장 부채 형태.
- 수정된 모션: 몸 회전 없이 카드 당김 → 연속 투척 → 기본 자세 복귀, 조커 8장. 케인은 목 부분을 쥐어 바닥에서 띄운다. 재생 순서와 게임 연결 전 상태는 [모션 기록](five-class-motion.md)을 따른다.
- 카드 효과: 전방 나선 흐름, 금빛·분홍빛 회전 호, 캐릭터 복귀 후 잠시 남는 투사 카드. 캐릭터 프레임과 별도로 다룬다.
- 영상 속 펫·다른 인물·녹색/청색 겹침 효과·UI는 고유 카드 디자인으로 복사하지 않는다.

실제 게임 스킬 길이·타격 시점은 기존 정의를 확인해 사용한다. 녹화 길이를 그대로 게임 지속시간으로 설정하지 않는다. `.info/character.md`와 `.info/motion.md`에는 새 기준 원화 저장 상태를 반영했고, 게임의 현재 모션·자산 연결은 그대로다.

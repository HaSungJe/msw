# 썬콜 캐릭터 모션 — 디자인 가이드라인

- 상태: 작성 중 (디자인 검토용 시안, 게임 미적용)
- 대상: `RtsJobTableLogic` 직업 `il` / 월드 유닛 `RtsUnitLogic.SpawnUnit`, `RtsUnitComponent`, `RtsSkillFxLogic`
- 한 줄 요약: 사용자 제공 썬콜 일러스트의 외형으로 새 스프라이트를 그리되, 애니메이션은 현재 게임과 메이플 원작의 `stand1`·`swingO1` 액션 구조를 따른다.

## 외형 기준

사용자가 제공한 썬콜 일러스트를 기준으로 **하늘색 긴 머리, 검은 리본 머리띠, 은회색 눈, 검은 끈 장식 드레스와 흰색·빙청색 겉옷, 푸른 눈꽃 스태프, 떠 있는 남색 마법책**을 유지한다. 과거 시안의 회보라 머리·붉은 눈·마법책 없는 의상은 폐기한다. 완성 프레임은 직접 생성한 새 그림이며 원본 MSW 이미지를 이어붙여 쓰지 않는다.

## 모션 기준

| 게임 사용 액션 | 원작 프레임 | 새 시안 | 재생 |
|---|---:|---|---|
| `stand1` | 0·1·2 | `frames/stand1/00.png` ~ `02.png` | 0→1→2→1 왕복 반복 |
| `swingO1` | 0·1·2 | `frames/swingO1/00.png` ~ `02.png` | 150→120→180ms, 1회 후 stand1 |

`swingO1` 자세는 **낮은 준비 → 더 웅크린 중간 → 한손 스태프를 머리 위로 올리는 마무리**다. 앞쪽으로 찌르거나 양손으로 휘두르는 새 동작을 만들지 않는다. `RtsJobTableLogic.GetSkillsRaw("il")`의 체인 라이트닝은 이미 `motion = "swingO1"`; 이 이름을 그대로 연결한다. 현재 `RtsSkillFxLogic`에 기록된 아바타 swing 마지막 프레임 진입 시간 약 0.44~0.49초에 맞춰 시안 합계를 450ms로 잡았다. 체인 라이트닝 빔은 기존 `beamDelay = 0.4`, 타격은 `hitDelay = 0.5`이므로 시각적인 손끝 동작과 타격 순서를 대조해야 한다.

## 이미지

| 파일 | 쓰임 | 크기 | 투명 |
|---|---|---:|---|
| `assets/design/characters/ice-lightning-mage/frames/stand1/*.png` | 대기 3프레임 | 각 512×512 | RGBA |
| `assets/design/characters/ice-lightning-mage/frames/swingO1/*.png` | 공격 3프레임 | 각 512×512 | RGBA |
| `assets/design/characters/ice-lightning-mage/animation.json` | 프레임 순서·시간·발 기준점 | 데이터 | — |
| `assets/design/characters/ice-lightning-mage/pose-preview.png` | 큰 포즈 비교 | 1280×400 | 없음 |
| `assets/design/characters/ice-lightning-mage/game-scale-preview.png` | 80px 셀 가독성 확인 | 512×128 | 없음 |

공통 발 기준점 `(256, 488)`, 기본 방향 오른쪽. 왼쪽 대상이면 수평 반전한다. 기존 80px 셀 안에서 게임 표시 크기를 맞추되 기준점을 흔들지 않는다.

## Claude 구현 시

1. 사용자가 디자인을 확정한 뒤 각 PNG를 MSW에 **새 리소스**로 등록하고 RUID 대응표를 남긴다. 기존 아바타 RUID를 덮어쓰지 않는다.
2. `il` 유닛 표시만 새 프레임 스프라이트로 전환한다. 영입·레벨·타겟·피해 판정·체인 라이트닝 이펙트·사운드는 그대로 유지한다.
3. 본체 방향 반전, `stand1` 복귀, 스킬 중 프레임 중단, 유닛 제거·재스폰, 카드/프로필 미리보기에서 빈 화면이 생기지 않는지 Maker Play로 확인한다.
4. `stand1`의 1·2프레임은 원화의 미세 위치 변형이다. 품질을 더 높이려면 별도 원화를 그려 교체하되 **3프레임 왕복 구조**는 유지한다.

## 참고

- [MSW 공식 아바타 액션](https://maplestoryworlds-creators.nexon.com/ko/docs/?postId=820): `stand1`, `swingO1` 액션 이름과 대기 ZigzagLoop
- [NEXON Open API 프레임 안내](https://openapi.nexon.com/support/notice/2715682/): 두 액션의 프레임 번호 0~2
- `assets/design/characters/ice-lightning-mage/README.md`: 원본·프리뷰·재생성 방법

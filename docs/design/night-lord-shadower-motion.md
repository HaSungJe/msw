현재 적용(2026-09-27): 팔라딘·다크나이트·나이트로드·섀도어·팬텀 전용 흉상 5종과 팬텀 대기 3장·조커 8장·별도 카드/고리를 게임에 연결했다. 팬텀 카드는 고리 가장자리가 캐릭터와 살짝 겹치도록 대상 방향 앞 1.10유닛, 높이 1.04에서 출발한다. 실제 대상 거리가 1칸 미만이면 직선, 1칸 이상이면 기존 거리별 포물선으로 날아간다. 카드 1.152×1.728유닛·고리 2.528유닛 크기는 유지한다. 현재 11직업 모두 전용 PNG 외형·흉상 사용. 상세: docs/design/five-class-portraits-phantom.md.

# 나이트로드·섀도어 모션 적용

나이트로드·섀도어 모션 적용: 저장된 대기·공격 PNG 35장(나이트로드 11, 섀도어 24)을 새 RUID로 연결했다. 나이트로드 nlThrow는 쿼드러플 스로우·풍마수리검 공용, 섀도어는 shadSavage·shadMeso·shadDualblade를 사용한다. 쉐도우 파트너는 기존 검은 실루엣으로 0.5초 늦게 동작한다. 흉상은 직업별 portrait.png 전용 자산 사용. 현재 연결·검증 기록: docs/design/night-lord-shadower-motion.md.

사용자 최종 확정: 팔라딘·다크나이트는 현재 게임 모션 그대로 승인. 다크나이트는 상단 → 하단 → 정면, 거대화는 같은 순서 두 번 반복.

## 연결

| 직업 | 액션 | 순서 | 프레임 시간(초) | 합계 |
|---|---|---|---|---|
| nl | stand1 | 1,2,1,3 | 0.65,0.45,0.65,0.45 | 2.2 |
| nl | nlThrow | 1,2,3,4,5,6,5,6,7,8 | 0.1,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.1,0.15 | 0.7 |
| shad | stand1 | 1,2,1,3 | 0.65,0.45,0.65,0.45 | 2.2 |
| shad | shadSavage | 1,2,3,4,5,6,4,5,7,8 | 0.1,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.03,0.02 | 0.5 |
| shad | shadMeso | 1,2,3,4,5 | 0.12,0.18,0.07,0.08,0.05 | 0.5 |
| shad | shadDualblade | 1,2,3,4,5,6,7,8 | 0.15,0.15,0.1,0.15,0.2,2.1,0.2,0.15 | 3.2 |

기존 원화·프레임 그림을 그대로 적용했다. 대기 576×576·발 (288,512), 공격 704×704·발 (352,640), 픽셀당 로컬 0.002유닛. 쿼드러플 스로우·풍마수리검은 몸체를 공유하며 투사체는 별도 기존 자산이다. 섀도어 토네이도·카르마는 0.30초 방출, 3.20초까지 몸체와 효과가 이어진다. 피해·판정·쿨타임·투사체 설정은 변경하지 않았다.

PNG 재생의 조기 return 때문에 그림자 동작이 생략되던 SendAction을 수정했다. 본체를 재생한 뒤 기존 그림자 지연 경로로 이어지며 nlThrow는 swingO1 실루엣 클립을 선택한다. 다른 아바타 이벤트 경로는 유지한다.

## 현재 리소스

| PNG (assets/design/characters/ 아래) | RUID |
|---|---|
| night-lord/frames/quadruple-throw/motion01.png | `866e55971d3b4ebf96a3dab124e32e00` |
| night-lord/frames/quadruple-throw/motion02.png | `5370617f4c2e403691279d424471f2b5` |
| night-lord/frames/quadruple-throw/motion03.png | `697245aeab1a4ce9abfa1f1a9234d463` |
| night-lord/frames/quadruple-throw/motion04.png | `6599b1f88ea84d7baf53b840da59667d` |
| night-lord/frames/quadruple-throw/motion05.png | `03eb6091d1bb419e9d0cbd00a7db2e45` |
| night-lord/frames/quadruple-throw/motion06.png | `6d729205cc984689b50da0c5fccc7fe8` |
| night-lord/frames/quadruple-throw/motion07.png | `67da87ba78dc4e95a0d8787a84935080` |
| night-lord/frames/quadruple-throw/motion08.png | `aec7d0e3b7ad427b8bc1fd1ab906cdcb` |
| night-lord/frames/wait/motion01.png | `0eb5a0560215452fba5d11fa5b0dbd16` |
| night-lord/frames/wait/motion02.png | `53e0a2cf0bb940bbb7ed86cd65562037` |
| night-lord/frames/wait/motion03.png | `e7f8edd9c9ee4898baaacc1f38ff33db` |
| shadower/frames/blade-tornado-karma-fury/motion01.png | `7200f4b75d9d43a0af2a735e6cd0ba8f` |
| shadower/frames/blade-tornado-karma-fury/motion02.png | `70f2e87473434a68bd3ceb1f56bb41b2` |
| shadower/frames/blade-tornado-karma-fury/motion03.png | `6c6fb1dbd7584b1d8eee7d4bda13ee29` |
| shadower/frames/blade-tornado-karma-fury/motion04.png | `a4b7ae6b436f483b912330a657ad88d4` |
| shadower/frames/blade-tornado-karma-fury/motion05.png | `ef741c7fc3cc4fdeb1d06a71d74ccc14` |
| shadower/frames/blade-tornado-karma-fury/motion06.png | `0a36ccef0202492788c4283d6c52f545` |
| shadower/frames/blade-tornado-karma-fury/motion07.png | `fc0570f63b4945f390bf4e03508a3416` |
| shadower/frames/blade-tornado-karma-fury/motion08.png | `91f0a6cfb7c04e729e1a788a40d283ba` |
| shadower/frames/meso-explosion/motion01.png | `fbef7d6900ee489eb870bb29f04f962f` |
| shadower/frames/meso-explosion/motion02.png | `c5379c189d674cff98b310cca14cad50` |
| shadower/frames/meso-explosion/motion03.png | `4dc51fe6f8554aa3ae727777235460d4` |
| shadower/frames/meso-explosion/motion04.png | `cbdb8dd7ecdd4bc796e6bb2b96a24e01` |
| shadower/frames/meso-explosion/motion05.png | `24ee1e2b9952414d936e483b8ece07ae` |
| shadower/frames/savage-blow/motion01.png | `e0f64485b5db4a95aa412399d5790b00` |
| shadower/frames/savage-blow/motion02.png | `fb2887c0d0b443bda8d7f6d7dc3aaf21` |
| shadower/frames/savage-blow/motion03.png | `10a908c265d64f5aabbff97de72821ae` |
| shadower/frames/savage-blow/motion04.png | `476197fafcaa47938c2c0d9bf011bd45` |
| shadower/frames/savage-blow/motion05.png | `6292265f10a2488bac1ad7258df7034d` |
| shadower/frames/savage-blow/motion06.png | `238fb780543747a085ac1107d7aa765c` |
| shadower/frames/savage-blow/motion07.png | `f74189314f454aa683a7febdd268f0ae` |
| shadower/frames/savage-blow/motion08.png | `bc760d3a8ba7430f899b11057c4ace73` |
| shadower/frames/wait/motion01.png | `2753c58c1aaf413681834dc5d70ecac2` |
| shadower/frames/wait/motion02.png | `96ed758328834446b5d9f9e7adebf101` |
| shadower/frames/wait/motion03.png | `fb4ae0f6c16e49459d28f99139523bf7` |

파일·SHA256·RUID: `.beaver/output/night-lord-shadower-motion/resource-manifest.json`. 연결: `connection-plan.json`, 검증 스크립트: `verify.lua`, 자동 재생: `autoplay.lua`. 전용 흉상은 미제작이며 선택·상세 정보는 대기 01을 임시 사용한다. 피해량 회귀 검증은 이번 외형 연결 범위에 포함하지 않는다.

사용자 최종 확정: 나이트로드·섀도어의 현재 모션을 승인했다. Maker 새 리소스 35/35, 일반·프리즘 모든 공격 프레임 좌우 재생, 대기 3/3 및 복귀, 실제 서버 SpawnUnit의 아바타 제거·나이트로드 분신 생성 확인. 분신 동작 지연 약 0.52초, 빌드·현재 실행 오류 0. 시험용 서버 유닛 2기는 제거했고 화면의 클라이언트 전용 4기는 6초 간격 자동 재생 중이다.

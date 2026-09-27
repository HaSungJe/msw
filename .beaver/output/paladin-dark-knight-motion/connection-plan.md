현재 상태: 사용자 승인 후 32장 업로드·연결·Maker 검증 완료. 실제 결과는 resource-manifest.json·verification.json 및 docs/design/paladin-dark-knight-motion.md. 아래는 승인 당시 적용 계획이다.

# 팔라딘·다크나이트 모션 연결 준비

상태: 업로드 자동 승인 거절로 대기. 파일 검수 완료, 업로드 0장, 게임 코드 변경 없음.

업로드 대상: 승인된 PNG 32장, 7,241,603바이트. 현재 월드 계정 MSW resource storage의 sprite/etc로 각각 새 RUID 등록.

| 직업 | 동작 키 | 재생 길이 |
|---|---|---:|
| paladin | stand1 | 2.200초 |
| paladin | paladinCharge | 0.750초 |
| paladin | paladinSanctuary | 0.900초 |
| dk | stand1 | 2.200초 |
| dk | dkBuster | 1.200초 |
| dk | dkRoar | 1.400초 |
| dk | dkGiantBuster | 1.200초 |

스피어 버스터는 첫 준비 자세에 0.5초를 포함한다. 거대화는 기존 프레임의 찌르기·회수를 반복하며 기존 6회 타격 시각을 유지한다. 별도 흉상은 만들지 않고 대기 첫 이미지를 선택창에 연결할 예정이다.

## 검수한 업로드 파일

- `paladin/frames/divine-charge/motion01.png` (248,794 bytes)
- `paladin/frames/divine-charge/motion02.png` (217,932 bytes)
- `paladin/frames/divine-charge/motion03.png` (239,969 bytes)
- `paladin/frames/divine-charge/motion04.png` (256,480 bytes)
- `paladin/frames/divine-charge/motion05.png` (249,231 bytes)
- `paladin/frames/divine-charge/motion06.png` (233,240 bytes)
- `paladin/frames/sanctuary/motion01.png` (275,776 bytes)
- `paladin/frames/sanctuary/motion02.png` (293,372 bytes)
- `paladin/frames/sanctuary/motion03.png` (246,788 bytes)
- `paladin/frames/sanctuary/motion04.png` (244,507 bytes)
- `paladin/frames/sanctuary/motion05.png` (236,243 bytes)
- `paladin/frames/sanctuary/motion06.png` (230,864 bytes)
- `paladin/frames/wait/motion01.png` (208,602 bytes)
- `paladin/frames/wait/motion02.png` (214,299 bytes)
- `paladin/frames/wait/motion03.png` (208,047 bytes)
- `dark-knight/frames/dragon-roar/motion01.png` (212,588 bytes)
- `dark-knight/frames/dragon-roar/motion02.png` (206,623 bytes)
- `dark-knight/frames/dragon-roar/motion03.png` (212,762 bytes)
- `dark-knight/frames/dragon-roar/motion04.png` (263,346 bytes)
- `dark-knight/frames/dragon-roar/motion05.png` (243,025 bytes)
- `dark-knight/frames/dragon-roar/motion06.png` (229,570 bytes)
- `dark-knight/frames/spear-buster/motion01.png` (210,525 bytes)
- `dark-knight/frames/spear-buster/motion02.png` (196,493 bytes)
- `dark-knight/frames/spear-buster/motion03.png` (190,096 bytes)
- `dark-knight/frames/spear-buster/motion04.png` (214,502 bytes)
- `dark-knight/frames/spear-buster/motion05.png` (209,029 bytes)
- `dark-knight/frames/spear-buster/motion06.png` (198,407 bytes)
- `dark-knight/frames/spear-buster/motion07.png` (202,433 bytes)
- `dark-knight/frames/spear-buster/motion08.png` (212,067 bytes)
- `dark-knight/frames/wait/motion01.png` (211,884 bytes)
- `dark-knight/frames/wait/motion02.png` (216,834 bytes)
- `dark-knight/frames/wait/motion03.png` (207,275 bytes)

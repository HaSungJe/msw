---
feature_goal: "맵 테마 프리셋(내 구역 외형 5종) + 몬스터 아이콘 수집·선택 + 좌측 유저 카드 — 프리셋 기능 뼈대, 디자인은 ChatGPT 인계"
domain: "rts-custom"
api_method: "RtsProfileLogic.RequestSetTheme / RtsProfileLogic.RequestSetIcon (@ExecSpace Server) · RtsProfileLogic.OnMonsterKilled (ServerOnly) · RtsProfileLogic.SendProfile (Client, 그 유저에게만)"
api_path: "RequestSetTheme(string key) · RequestSetIcon(string monsterId) · SendProfile(string theme, string icon, string owned, string userId) · RtsHudLogic.RefreshPlayerList(string packed) — 줄 형식에 테마·아이콘 칸 추가(서명 그대로)"
affected_data:
  - "유저 DataStorage theme (선택한 테마 키, 없으면 henesys)"
  - "유저 DataStorage icon (선택한 아이콘 = 몬스터 id, 없으면 M001 초록달팽이)"
  - "유저 DataStorage icons (획득한 아이콘 = `몬스터id:획득시각` 쉼표 구분 — 획득시각 = UTC ms(DateTime.UtcNow.Elapsed), 영구 누적. M001은 기본 보유라 저장 안 해도 보유로 본다)"
  - "맵 RectTileMap 타일(구역 사각형 단위로 다시 칠함) · 구역 그리드 스프라이트 ZoneGrid{n} · 구역 장식 ZoneDecor{n}_{i}"
---

## Feature Description
로드맵 ① Phase 10(개인 테마 프리셋 #38) + Phase 14(아이콘 프리셋 #40)에, Phase 11의 좌측 유저 카드(#41)를 당겨 함께 한다(2026-09-25 사용자 순서·요청).

- **맵 테마**: 헤네시스 · 엘리니아 · 페리온 · 커닝시티 · 리스항구 5종. 기본은 헤네시스. 고르면 **내 구역**의 바닥 타일·트랙 판·여백 장식이 그 테마로 바뀐다. **보이는 것만 바뀌고 밸런스 영향 없음**. 테마는 종류별 **탭**으로 나누며 지금은 '기본' 탭 하나에 5종.
- **이번 범위는 프리셋 기능의 뼈대**: 헤네시스 외 4종은 기존 바닥 타일·트랙 판 색(틴트)만 바꾼 **임시 모양**으로 둔다. 실제 디자인(바닥·트랙 텍스처·장식·썸네일)은 **ChatGPT가 이어받는다** — 무엇을 어디서 바꾸면 되는지 문서(`docs/theme-presets.md`)로 정리한다(사용자 "트랙 대충 만들어서 프리셋 기능만 구현, 디자인 관련은 ChatGPT에 이양 — 수정 범위만 잘 알려줄 수 있게 문서화").
- **테마 상자**: 좌상단 정보 카드(맵·라운드·난이도·메소) **위에** 새 상자. 지금 테마의 썸네일과 이름. 누르면 테마 창 → 테마를 누르면 "맵 테마를 변경하시겠습니까?" [예]/[아니오] → 예 = 내 테마 변경.
- **아이콘**: 몬스터 정보 창 초상(몬스터 그림)과 같은 그림. 몬스터 247종(일반 229 + 보스 18) = 아이콘 247개. 기본은 **초록달팽이만 보유**, 나머지는 획득해야 한다 — **매우어려움 난이도에서만, 그 몬스터를 처치할 때 1%**(보스 포함). 아이콘 창도 종류별 **탭**(지금 '기본'만).
- **아이콘 창**: 아이콘을 누르면 정보 팝업 — 획득 여부 · 어디서 얻는지(처음 나오는 라운드·맵) · 확률(매우어려움 처치 시 1%). 획득한 것만 [이 아이콘 사용] → [예]/[아니오]로 변경.
- **획득 알림**: 아이콘을 얻으면 **팝업**으로 획득 정보(그림·이름·획득처)를 보여 준다.
- **유저 카드**(좌측 플레이어 목록 대체): 카드를 키워 배경에 **그 유저가 고른 테마의 썸네일**, 왼쪽에 **동그란 아이콘**, 오른쪽에 **닉네임**. 내 카드는 "(나)" 글자 대신 **카드 테두리를 조금 굵은 초록**으로. 내 카드에만 작은 **[수정]** 버튼 → 아이콘 창.
- **영구 정보**: 테마·보유 아이콘·선택 아이콘은 **서버가 계정 DataStorage에 저장**하고, 입장·변경·획득 때마다 **서버가 그 유저에게 전부 보낸다**(사용자 "서버 쪽에서 항상 유저에게 전달해야 누적 — 영구 획득 정보").

## API Spec
- Method: `@ExecSpace("Server")` RPC 2개 + ServerOnly 처치 훅 + `@ExecSpace("Client")` 그 유저 통지 1개 + 기존 플레이어 목록 RPC(서명 그대로)
- Path:
  - `RtsProfileLogic.RequestSetTheme(string key)` — 클라 → 서버. `senderUserId`의 구역만 바뀐다.
  - `RtsProfileLogic.RequestSetIcon(string monsterId)` — 클라 → 서버. 보유한 아이콘만.
  - `RtsProfileLogic.OnMonsterKilled(number zone, string monsterId)` — `RtsMonsterComponent.Die`(RtsMonsterComponent.mlua:392)에서 부른다(서버).
  - `RtsProfileLogic.SendProfile(string theme, string icon, string owned, string userId)` — 서버 → 그 유저(마지막 인자 userId = 그 클라에만, 기존 관례 RtsCameraAnchorComponent.ApplyAssignedZone).
  - `RtsProfileLogic.ShowIconGot(string monsterId, string userId)` — 서버 → 그 유저, 획득 팝업.
  - `RtsHudLogic.RefreshPlayerList(string packed)` — 줄 = `userId\t닉\t구역\t생존\t테마\t아이콘`(끝 두 칸 추가, RtsBootstrapLogic.mlua:39-58). 서명은 바꾸지 않는다(docs/ui-screens.md 3.2).
- Request: 테마 키(`henesys|ellinia|perion|kerning|lith`), 몬스터 id(`M001`~`M229`, `B01`~`B18`)
- Response: 성공 = DataStorage 저장 → 구역 외형 적용(테마) → `SendProfile` + 플레이어 목록 다시 보냄. 실패 = 아무것도 안 바뀜(서버 로그만, `RtsConfigLogic.Log`).

## Business Rules
- **소유자 검증**: 테마·아이콘 변경은 `senderUserId` 본인 것만. 구역은 `RtsZoneLogic.GetZoneOfUser(senderUserId)`로만 정한다(남의 구역 불가 — CLAUDE.md 조작 RPC 규칙).
- **테마 키 검증**: 프리셋 표에 없는 키는 거부. 테마는 5종 모두 **무료**(요청에 구매 없음 — 과금은 나중에 따로).
- **아이콘 검증**: 보유 목록에 없는 id는 거부. `M001`(초록달팽이)은 항상 보유.
- **획득 규칙**: 몬스터가 죽을 때 그 몬스터 **구역의 주인**이 대상. 조건 = 그 유저 난이도가 **매우어려움**(`RtsDifficultyLogic.Of(userId)` = 5, 극악(6) 제외 — 사용자 "무조건 매우어려움에서 1%") · 아직 없는 아이콘 · 테스트 모드(`RtsUnitLogic.DevTools`) 아님. 그때 1%(`RandomDouble() < 0.01`). 보스 포함.
- **획득 일시**: 아이콘마다 **획득 일시를 함께 저장**한다(사용자 "나중에 집계할 수도 있으니"). 형식 `M005:1790000000000`(UTC ms). 247개 모두 모여도 약 5KB — 값 한 칸 한도 300,000바이트·4,000바이트당 1크레딧(엔진 문서 'DataStorage Use Limits'). 집계는 **유저별 기록만**(전역 통계 저장은 하지 않음 — 사용자 선택).
- **저장**: 획득·변경 즉시 서버가 DataStorage에 쓴다. 저장 실패면 메모리 값도 되돌리고 알리지 않는다(다음 처치에서 다시 굴림). 영구 — 지우는 경로 없음.
- **전달**: 입장 때(`HandleUserEnterEvent` → 불러오기 → `SendProfile`) · 변경 때 · 획득 때 서버가 그 유저에게 전체(테마·선택 아이콘·보유 목록)를 보낸다. 클라는 받은 값을 그대로 쓰고 스스로 바꾸지 않는다.
- **테마 적용 범위**: 내 구역 사각형(구역 폭·높이 + 구역 사이 여백의 절반)의 바닥 타일, 내 구역 그리드 스프라이트(텍스처 + 틴트), 내 구역 여백 장식. 다른 구역은 그대로. 나가면 그 구역은 기본(헤네시스)으로 되돌린다.
- **밸런스 영향 없음**: 테마는 타일·스프라이트·장식만. 트랙 경로·발판·보스 영역·사거리 계산은 안 건드린다.
- **진행 중 변경 허용**: 테마·아이콘은 판 진행 중에도 바꿀 수 있다(보이는 것만).

## Notes
- 테마 프리셋 뼈대는 이미 있다: `RtsThemeLogic.GetPresets`(RtsThemeLogic.mlua:57-64, 헤네시스·엘나스) · 전역 `ApplyPreset`(:113-125) — 전역 하나라 **구역 단위로 바꿔야** 한다.
- 바닥 = 맵 전체 RectTileMap 하나(`RtsBootstrapLogic.FillGroundTiles` :80-102). 구역만 다시 칠하려면 `RectTileMapComponent.ToCellPosition`으로 구역 사각형 → 타일 좌표(엔진 API 확인 2026-09-25).
- 그리드 트랙 = 구역마다 스프라이트 1장 `ZoneGrid{n}`(RtsZoneLogic.mlua:269-297), 장식 = `ZoneDecor{n}_{i}`(:313-338) — 이미 구역별 엔티티라 구역 단위 교체 가능.
- 공식 위에서 본 장식 자산은 `topview_henesys`뿐(2026-09-25 검색: ellinia·perion·kerning·lith 탑뷰 없음, 옆모습 오브젝트만 — 예 `map/obj/partem/ruin_rock/perion`). 새 4종 장식은 ChatGPT 몫.
- 바닥 타일셋(`CaveFloorTileSet`)에 있는 타일: HenesysGrass1~3 · HenesysGrassFloor · HenesysSoil · HenesysStone1/3/4 · ElnathSnowFloor — 임시 모양은 이 안에서 고른다.
- 몬스터 초상 = 정보 창 방식(RtsMonsterInfoLogic.mlua:114-136: 걷기 클립, NativeSize, 표 box로 가운데 맞춤). 아이콘 247개를 격자에 한꺼번에 그리므로 **움직이지 않는 첫 프레임 그림**을 쓴다 — 스테이지 표 생성기가 걷기 클립 첫 프레임 스프라이트를 `icon`으로 표에 넣는다(tools/gen-stage-table.py `clip_frames`).
- 계정 저장 형제: `RtsUnitLogic.LoadAvatarPass`(RtsUnitLogic.mlua:545-552, GetAndWait) · `ProcessPurchase`(:555-576, SetAndWait + 실패 코드 처리) · `RtsRunResultLogic` BestRun(:185-).
- 확인 팝업 형제: 다시하기 확인 `RtsPopupLogic.BuildRestart`(예/아니오, 2026-09-24).

## Proposals (Codebase-Based)
- [x] 테마 적용을 전역 `RtsThemeLogic.ApplyPreset`에서 구역 단위 `ApplyToZone(zone, key)`로 바꾸고 전역 `ActiveKey`는 없앤다(§1.7 — 전역 경로가 남으면 한 사람이 바꿀 때 모두 바뀜)
- [x] 쓰지 않는 `elnath` 프리셋은 표에서 뺀다(자산은 assets/textures/README.md에 '보관'으로 남김)
- [x] 초상 그리기를 `RtsHudLogic.SpawnMonsterPortrait`로 공용화 — 정보 창(움직임)·아이콘 격자·유저 카드·획득 팝업(멈춤)이 같이 쓴다(지금 정보 창 안에만 있는 코드 RtsMonsterInfoLogic.mlua:119-136을 옮김)
- [x] 동그란 아이콘은 원형 마스크 스프라이트 1장(흰 원 PNG) 업로드 후 `MaskComponent`(정보 창 초상 칸 :118과 같은 방식)

## Decisions
- [x] 새 4종 테마 모양 — 기존 타일·트랙 판 틴트로 임시, 디자인(바닥·트랙·장식·썸네일)은 ChatGPT가 `docs/theme-presets.md` 보고 이어받음 (사용자 2026-09-25)
- [x] 테마 상자 자리 — 좌상단 정보 카드 위, 테마 썸네일 표시, 누르면 테마 창(탭 '기본') → 확인 예/아니오 (사용자)
- [x] 유저 목록 — 카드를 키워 배경 = 그 유저 테마 썸네일, 왼쪽 동그란 아이콘, 오른쪽 닉네임, 내 카드 = 조금 굵은 초록 테두리("(나)" 글자 없앰) (사용자)
- [x] 아이콘 창 여는 곳 — 내 카드의 작은 [수정] 버튼 (사용자)
- [x] 아이콘 획득 — 매우어려움에서만, 보스 포함, 처치 시 1%. 극악 제외 (사용자 "무조건 매우어려움에서 1%. 보스도 포함")
- [x] 획득 알림 — 팝업(그림·이름·획득처) (사용자)
- [x] 저장·전달 — 서버가 DataStorage에 영구 저장, 입장·변경·획득 때마다 그 유저에게 전체 전달 (사용자)
- [x] 테마 가격 — 5종 무료(요청에 구매 없음). 과금은 나중에 별도 결정
- [x] 획득 일시 — 아이콘마다 획득 일시(UTC ms)를 유저 저장소에 함께 저장, 전역 집계 기록은 안 함 (사용자 "유저별 획득 일시만")

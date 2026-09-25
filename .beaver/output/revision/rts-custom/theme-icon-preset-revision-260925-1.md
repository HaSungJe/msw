# Revision — 맵 테마 + 몬스터 아이콘 + 유저 카드 → 프로필 설정(테마·비석) — 260925-1

> 원 spec/plan/report: `.beaver/output/{spec,plan,report}/rts-custom/theme-icon-preset-*.md`. 원 문서는 고치지 않고 참고만 한다.
> 메모리 workflow "로드맵·플랜은 코드가 아니라 방향·동작 설명으로" — Code Changes는 mlua 대신 파일별 동작 설명.
> 로드맵: Phase 10 #38(개인 테마)·Phase 14 #40(아이콘)·Phase 11 #41(유저 카드) — 이미 in-progress, 상태 그대로(완료는 사용자 확인 때).

## Reason for Change Request
사용자 2026-09-25: "비석도 프리셋 만들자. 좌측 상단 맵 테마 창을 프로필 설정으로 변경. 탭을 테마/비석 두 개로 분리 … 현재 비석 스킨을 기본 스킨으로, 비석 스킨은 일단 1개만.
아이콘/테마/비석 기본 설정 — 아이콘: 없음, 테마: 헤네시스, 비석: 현재 기본 비석. 설정값이 없으면 기본값으로 게임 시작 시 자동 설정."
결정(같은 날 질문): 초록달팽이 기본 보유는 유지(아이콘 창에 '없음' 칸 추가) · 프로필 상자 = 제목 + 테마·비석 이름.

## Spec Before → After

| Item | Before | After |
|------|--------|-------|
| 좌상단 상자 | 테마 상자 — 테마 썸네일 + "맵 테마" + 테마 이름 + "변경 ›" | **프로필 상자** — 테마 썸네일 + 제목 **"프로필 설정"** + 작은 줄 "테마 ○○ · 비석 ○○" + "변경 ›". 누르면 프로필 창 |
| 창 | `theme`(제목 "맵 테마", 탭 = 테마 종류 '기본') | **`profile`**(제목 "프로필 설정", 위 탭 **[테마] [비석]**). 테마 탭 = 지금 테마 카드 그대로(정사각 3장 × 2줄 세로 스크롤). 종류 탭('기본')은 종류가 2개 이상일 때만 둘째 줄에 나온다 |
| 비석 | 모든 유저 같은 비석(`RtsRunResultLogic.TombRUID` 29e864c6… · 스케일 5) | 유저마다 **비석 프리셋**. 1종 '기본 비석'(= 지금 비석). 탈락하면 그 구역 주인의 비석으로 선다(다른 사람에게도 그 모양) |
| 비석 탭 | — | 테마 탭과 같은 정사각 카드(비석 그림 + 이름 + '사용 중'). 카드 클릭 → "비석을 변경하시겠습니까?" 예/아니오(`tombconfirm`) → 서버 저장 |
| 아이콘 기본값 | 초록달팽이(M001) | **없음**. 초록달팽이는 계속 기본 보유(고를 수 있음). 아이콘 창 첫 칸 = **'없음'**(누르면 바로 "아이콘을 없음으로 변경하시겠습니까?") |
| 아이콘 없음 표시 | — | 유저 카드 원형 칸 = 빈 원(어두운 바탕, 초상 없음). 아이콘 창에서 '없음' 칸이 '사용 중'(금색) |
| 기본값 저장 | 저장된 값이 없으면 메모리에서만 기본값(DataStorage엔 안 씀) | 입장 때 읽은 키가 **없으면 기본값을 그 자리에서 저장**(테마 henesys · 아이콘 none · 비석 basic — 사용자 "게임 시작 시 자동 설정"). 이미 저장된 값은 그대로(이미 M001을 저장한 유저는 M001 유지) |
| DataStorage 키 | theme · icon · icons | + **tomb**. icon 값 `none` = 아이콘 없음 |
| 서버 → 클라 전달 | `SendProfile(theme, icon, owned, userId)` | 인자에 비석이 붙어 **새 이름** `SendProfileState(theme, icon, tomb, owned, userId)`(메모리 msw-engine — 분석기가 인자 수를 캐시해 서명을 바꾸면 새 이름). 옛 `SendProfile` 삭제 |
| 조작 RPC | RequestSetTheme · RequestSetIcon | + **`RequestSetTomb(key)`**(Server, senderUserId, 없는 키 거부). `RequestSetIcon("none")` 허용(보유 검사 없음) |

## Affected Files
| File | Change Type | Description |
|------|-------------|-------------|
| `RootDesk/MyDesk/RtsTombLogic.mlua` (+ Maker가 만드는 `.codeblock`) | add | 비석 프리셋 표(`GetPresets` · `HasKey` · `GetPreset` · `DefaultKey` "basic") — `RtsThemeLogic` 프리셋 표와 같은 짜임(RtsThemeLogic:57-80 `GetPresets`·`HasKey`·`GetPreset`) |
| `RootDesk/MyDesk/RtsProfileLogic.mlua` | modify | 비석 상태·키·RPC, 아이콘 기본 none, 기본값 저장, `SendProfileState`, 머리 주석 |
| `RootDesk/MyDesk/RtsRunResultLogic.mlua` | modify | `SpawnTomb(zone)` — 그 구역 주인의 비석 프리셋(RUID·스케일). `TombRUID`·`TombScale` 프로퍼티는 프리셋으로 옮기고 삭제 |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modify | 테마 상자 → 프로필 상자(제목·요약 줄), 유저 카드 아이콘 없음 표시(`ApplyPlayerLook`) |
| `RootDesk/MyDesk/RtsPopupLogic.mlua` | modify | kind `theme` → `profile`(위 탭 테마/비석, `ProfileTab`), `BuildTombTab`, `tombconfirm`, 아이콘 창 '없음' 칸, 확인 창 문구(없음) |
| `docs/theme-presets.md` · `docs/ui-screens.md` | modify | 프로필 상자·창, 비석 프리셋 절(새 비석 추가 절차), 바꾸면 안 되는 것(키 tomb, 새 RPC 서명) |
| `.beaver/output/report/rts-custom/theme-icon-preset-report.md` | modify | build 뒤 `## Change - 260925-3` |

## Code Changes

```text
RtsTombLogic.mlua (새 Logic, 전역 _RtsTombLogic)
- property string DefaultKey = "basic"
- GetPresets(): { { key = "basic", name = "기본 비석", tab = "기본", ruid = "29e864c67e6c451d917b34519a4a9373", scale = 5.0 } }
  (새 비석 = 한 줄 추가. 키는 저장 값이라 바꾸지 않는다)
- HasKey(key) / GetPreset(key)(없으면 기본) / GetTabs() — RtsThemeLogic과 같은 이름·동작
- 실행 공간: 표 조회만(서버·클라 공용, 상태 없음) — RtsThemeLogic의 표 메서드와 같게 실행 공간 표기 없음(양쪽 호출)
```

```text
RtsProfileLogic.mlua
- TombKey = "tomb", DefaultIcon "M001" → "none"(아이콘 없음). IconNone = "none"
- 서버 TombByUser, 클라 MyTomb = "basic", PendingTomb
- Load(userId): theme·icon·icons·tomb 읽기 → 없거나 틀린 값은 기본값. **읽은 키가 없던 것**(코드 ≠ 0 또는 빈 값)은 SetAsync로 기본값을 바로 저장(실패는 로그만 — 다음 입장 때 다시)
    icon: 저장 값이 보유 목록에 없고 none도 아니면 none. M001은 ParseOwned가 늘 보유로 넣는다(그대로)
- PushProfile(userId) → SendProfileState(theme, icon, tomb, PackOwned(owned), userId)
- RequestSetIcon(id): id == "none"이면 보유 검사 없이 저장(기존 흐름 — SetAsync 실패 시 되돌림)
- RequestSetTomb(key) @Server: senderUserId, HasKey 아니면 거부 로그, 같은 값이면 무시, TombByUser 갱신 → SetAsync(TombKey) 실패 시 되돌림 → PushProfile
- TombOf(userId) (서버): 없으면 기본
- SendProfileState @Client(마지막 인자 userId): MyTheme·MyIcon·MyTomb·MyOwned 갱신 → HUD 프로필 상자 갱신 + 열린 프로필/아이콘 창 다시 그리기(지금 SendProfile이 하던 일 그대로 + 비석)
- 옛 SendProfile 삭제, 머리 주석(비석·기본값)
```

```text
RtsRunResultLogic.mlua
- SpawnTomb(zone): owner = OwnerOfZone(zone) → pr = _RtsTombLogic:GetPreset(_RtsProfileLogic:TombOf(owner)) → SpawnProp(…, pr.ruid, 210), 스케일 pr.scale.
  주인이 없으면(퇴장) 기본 프리셋. TombRUID·TombScale 프로퍼티 삭제(소리 TombSound는 공용이라 그대로)
```

```text
RtsHudLogic.mlua
- BuildThemeBox/RefreshThemeBox → BuildProfileBox/RefreshProfileBox(같은 자리 (16,−16) 440×64, 이름만 바꾸고 옛 메서드 삭제):
    썸네일 104×48(PaintThumb — 내 테마) · 제목 "프로필 설정"(ColInk 17) · 요약 "테마 ○○ · 비석 ○○"(ColMuted 14) · "변경 ›"(금색). 클릭 → _RtsPopupLogic:Open("profile")
- ApplyPlayerLook: icon == "none"(또는 빈 값)이면 원형 칸에 초상을 만들지 않고 빈 원(어두운 바탕)만
```

```text
RtsPopupLogic.mlua
- kind "theme" → "profile"(900×730 그대로, 제목 "프로필 설정"). ProfileTab = "theme" | "tomb"(마지막 탭 기억)
- BuildProfile(body, W): 위 탭 줄 [테마] [비석](BuildTabRow 재사용) → 탭에 따라
    BuildThemeTab = 지금 BuildTheme 본문(종류 탭 줄은 종류가 2개 이상일 때만, 안내 줄 "고르면 내 구역의 바닥 · 트랙이 바뀌어요")
    BuildTombTab  = 같은 세로 스크롤 + 줄마다 정사각 카드 3장(270×270): 비석 그림(uisprite ImageRUID = 프리셋 ruid, 원본 비율로 칸 안에) + 이름 + '사용 중'/클릭 → PendingTomb → Open("tombconfirm")
      안내 줄 "탈락하면 내 구역에 이 비석이 서요"
- tombconfirm(640×300): "비석을 변경하시겠습니까?" 예 → RequestSetTomb(PendingTomb) → Open("profile") / 아니오 → Open("profile")(BuildConfirm 재사용)
- themeconfirm의 예/아니오 뒤 돌아가는 창 "theme" → "profile"
- 아이콘 창: 격자 첫 칸 = '없음'(빈 원 + "없음" 글자, 사용 중이면 금색) → 클릭 → PendingIcon = "none" → Open("iconconfirm") (정보 창은 건너뜀). iconconfirm 문구: none이면 "아이콘을 없음으로 변경하시겠습니까?"
- 테마 카드 공용 부분(줄·카드 틀)은 테마·비석 탭이 같이 쓰는 SpawnPresetCard(row, k, …)로 뽑는다(같은 모양 두 번 쓰지 않게)
- Open의 kind 목록·크기 표: theme 삭제, profile·tombconfirm 추가
```

```text
docs
- ui-screens: 3.0 테마 상자 → 프로필 상자, 4.2 팝업 표(profile·tombconfirm, 아이콘 '없음' 칸), 5장 비석 행(주인 프리셋)
- theme-presets: 1절 화면 설명(프로필 창 테마 탭), 새 절 "비석 프리셋"(칸 key·name·tab·ruid·scale, 새 비석 추가 = 업로드 → 한 줄), 5절 바꾸면 안 되는 것(tomb 키, SendProfileState·RequestSetTomb 서명)
```

## Test Cases (Maker Play)

```
[SUCCESS]          DataStorage 초기화(maker_reset_data_storage) 뒤 입장 → 테마 헤네시스 · 아이콘 없음(카드 빈 원) · 비석 기본, 서버 로그에 기본값 저장 3건 → Play 재시작 뒤 같은 값(저장됨)
[SUCCESS]          프로필 상자 "프로필 설정" + "테마 헤네시스 · 비석 기본 비석" → 클릭 → 프로필 창 [테마] 탭(카드 3×2) → [비석] 탭(기본 비석 1장 '사용 중')
[SUCCESS]          테마 변경 흐름 그대로(확인 → 내 구역만 변경 → 프로필 창으로 복귀, 상자 요약 갱신)
[SUCCESS]          아이콘 창 첫 칸 '없음'(사용 중 금색) → 초록달팽이 선택 → 카드에 초상 → '없음' 선택 → 확인 → 카드 빈 원
[SUCCESS]          탈락 → 내 구역에 기본 비석(스케일 5, 소리) — 지금과 같은 모양
[FAIL:validation]  RequestSetTomb("nope") → 거부 로그 · RequestSetIcon("M200")(미보유) → 거부 그대로 · RequestSetIcon("none") → 허용
[SUCCESS]          이미 icon = M001이 저장된 유저 → 입장 뒤에도 M001(덮어쓰지 않음)
[SUCCESS]          빌드 로그 오류 0 · 새 Logic codeblock 생성 확인

테스트 생략(위임형): RtsTombLogic.GetPresets·HasKey(표 조회 — 위 흐름으로 대신)
```

## Decisions
- [x] 비석 스킨 1종 = 지금 비석(기본 비석) — 사용자
- [x] 기본값: 아이콘 없음 · 테마 헤네시스 · 비석 기본 — 사용자
- [x] 설정값이 없으면 입장 때 기본값을 저장 — 사용자 "게임 시작 시 자동 설정"
- [x] 초록달팽이 기본 보유 유지 + 아이콘 창 '없음' 칸 — 사용자(질문 답)
- [x] 프로필 상자 = 테마 썸네일 + "프로필 설정" + "테마 ○○ · 비석 ○○" + "변경 ›" — 사용자(질문 답)
- [x] 창 탭 = [테마] [비석] 두 개(아이콘은 지금처럼 내 카드 [수정]) — 사용자 "탭을 테마/비석 두 개로"
- [x] 비석 프리셋 표는 새 Logic `RtsTombLogic`(테마 표 RtsThemeLogic과 같은 짜임) — 테마 적용 로직과 섞지 않는 기본값

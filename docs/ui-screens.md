# 화면 UI 명세 (디자인 인계용)

이 문서는 화면에 보이는 요소를 모두 정리한 것이다. 요소마다 누가 어디서 만드는지, 어디에 어떤 크기로 놓이는지, 색·글꼴, 언제 보이는지, 누르면 무엇을 하는지를 적었다. 읽는 사람은 ChatGPT(디자인 담당)이고, 이 문서만 보고 게임 로직을 깨지 않고 화면을 다시 꾸밀 수 있게 하는 것이 목적이다.
- 기준 코드: `RootDesk/MyDesk/*.mlua` (2026-09-24, 커밋 a75a69f 이후 작업 트리). 표기는 `파일:줄` 형식이며 파일 접두 `RootDesk/MyDesk/`는 생략했다.
- 읽는 순서(AGENT.md): `AGENT.md` → `.beaver/memory/` → `CLAUDE.md` → 이 문서. 엔진 관례는 `docs/msw-engine.md`를 본다.
- 시각 방향·공통 색·컴포넌트·Claude Code 구현 인계는 `docs/design-system.md`를 본다. 화면의 실제 동작과 좌표는 이 문서가 기준이다.

---

## 1. 개요

### 1.1 기본 전제
- 기준 해상도는 **1920×1080**이다. 모든 UI 좌표는 이 해상도의 px 값이다(RtsHudLogic:5, RtsPopupLogic:4).
- `.ui` 파일은 없다. UI는 **전부 mlua 스크립트가 런타임에 스폰**한다. 엔진의 `/ui` 엔티티를 찾고(RtsHudLogic:284), 그 아래에 두 그룹을 만든다.
  - `RtsHudGroup`(`_RtsHudLogic.HudGroup`, RtsHudLogic:292): HUD, 캐릭터 클릭 메뉴, 몬스터 정보, 난이도 막대가 여기 붙는다.
  - `RtsPopupGroup`(`_RtsPopupLogic.Group`, RtsPopupLogic:73): 팝업 셸이 붙는다. HUD를 다 만든 뒤 `_RtsPopupLogic:Build(ui)`로 생성된다(RtsHudLogic:466).
  - **두 그룹 모두 만든 직후 `_RtsHudLogic:StretchFull(grp)`로 화면 전체(anchor 0,0~1,1, 오프셋 0)로 늘린다.** 안 하면 실제 클라이언트에서 그룹이 작은 기본 크기로 화면 가운데에 생겨 모서리 요소가 전부 가운데로 몰린다(2026-09-24 v260924-1 출시 화면에서 발견 — Maker Play에서는 드러나지 않음). 새 UI 그룹을 만들 때도 똑같이 한다.
- HUD를 만드는 시점: 로컬 플레이어의 카메라 앵커가 클라에서 시작할 때 `RtsCameraAnchorComponent.SetupClient` → `_RtsHudLogic:BuildHud`(RtsCameraAnchorComponent:46)가 한 번 호출된다.
- 쓰는 모델: `model://uigroup`, `model://uisprite`, `model://uitext`, `model://uibutton`, `model://uiempty`(유닛 외형 미리보기).

### 1.2 좌표계 (UITransformComponent)
| 값 | 의미 |
|---|---|
| `AnchorsMin = AnchorsMax = anchor` | 부모 사각형 안의 기준점. (0,0)=왼쪽 아래, (1,1)=오른쪽 위, (0.5,0.5)=가운데 |
| `Pivot` | 자기 사각형 안의 기준점. 위치가 이 점을 기준으로 잡힌다 |
| `anchoredPosition` | anchor에서 pivot까지의 거리(px). **+x는 오른쪽, +y는 위쪽**이다. 그래서 위쪽 anchor에 붙는 요소는 y가 음수다 |
| `RectSize` | 폭×높이(px) |
| 스트레치(`OffsetMin`/`OffsetMax`) | anchor 구간(`aMin`~`aMax`)에 맞춰 늘어난다. 왼쪽 아래 여백은 OffsetMin, 오른쪽 위 여백은 OffsetMax(음수 = 안쪽)로 준다 |

이 문서의 표기: `a(0,1) p(0,1) (16,-16) 440×112` = anchor (0,1), pivot (0,1), 위치 (16,-16), 크기 440×112. 화면 절대 좌표는 **왼쪽 위를 원점**으로 쓴다. 코드의 UI 좌표는 아래로 갈수록 y가 줄어든다는 점에 주의한다.

월드 위치를 UI 위치로 바꿀 때는 `_UILogic:ScreenToUIPosition(_UILogic:WorldToScreenPosition(v))`를 쓴다. 결과는 화면 중앙을 원점으로 하는 좌표라서, HUD 그룹 자식에 anchor (0.5,0.5)로 그대로 넣는다(RtsUnitSelectLogic:139-141, docs/msw-engine.md:31).

### 1.3 공용 생성 도우미 (RtsHudLogic — RtsPopupLogic·RtsUnitPopupLogic·RtsUnitSelectLogic 등도 `_RtsHudLogic`로 호출)
| 도우미 | 줄 | 서명 | 하는 일 |
|---|---|---|---|
| `SpawnUI` | 145 | `(modelId, name, parent, anchor, pivot, pos, size) → Entity` | 모델을 스폰하고 anchor·pivot·위치·크기를 준다. 스프라이트 이미지는 흰 사각 `WhiteRUID`로 둔다 |
| `SpawnStretch` | 163 | `(modelId, name, parent, aMin, aMax, offMin, offMax) → Entity` | 부모에 맞춰 늘어나는 요소 |
| `Tint` | 179 | `(e, r, g, b, a)` | `SpriteGUIRendererComponent.Color`를 바꾼다 |
| `SpawnText` | 186 | `(name, parent, anchor, pivot, pos, size, text, color) → Entity` | `model://uitext`를 만든다. 배경 스프라이트는 알파 0 |
| `SpawnLabel` | 199 | `(... , text, color, fontSize, align, bold) → Entity` | SpawnText에 글자 크기·정렬(`TextAlignmentType`)·굵게를 더한다 |
| `SpawnPanel` | 213 | `(name, parent, anchor, pivot, pos, size, bg, border, thick) → Entity(안쪽)` | 바깥(이름 `name`, 테두리색)과 안쪽(이름 `name.."In"`, 배경색, thick만큼 안으로 들어감) 두 장을 만든다. **돌려주는 것은 안쪽**이고 바깥은 `.Parent`로 얻는다. 자식은 안쪽에 붙인다 |
| `SpawnClick` | 225 | `(name, parent) → Entity` | 부모 전체를 덮는 투명 `uibutton`(알파 0.01). **클릭음(`ClickSound`)이 자동으로 붙는다**(230-232). 동작은 호출 쪽에서 `ConnectEvent(ButtonClickEvent, …)`로 단다 |
| `PlayUi` | 239 | `(ruid)` | UI 효과음을 한 번 튼다 |
| `Int` / `FormatNumber` | 787 / 791 | `(n) → string` | 정수 문자열 / 천 단위 쉼표 |

팝업 쪽 조각 도우미(RtsPopupLogic):
- `SpawnTab(name, parent, pos, size, text, on, fontSize)` (249): 탭이나 작은 버튼을 만든다. 꺼짐은 배경 `Mix(white,0.04)`, 테두리 `Mix(white,0.12)`, 글자 (0.851,0.796,0.651). 켜짐은 배경 `Mix(Gold,0.18)`, 테두리 Gold, 글자 (0.973,0.925,0.784). 테두리 두께는 1.5, anchor·pivot은 (0,1)이다.
- `Base()` (266) = (0.11,0.094,0.075,1)이고, `Mix(top, a)` (270)는 Base 위에 top을 a만큼 섞은 **불투명** 색이다. 테두리 백킹이 비쳐 보이지 않게 하려고 쓴다.
- `SpawnBadge(name, parent, pos, grade)` (293): 등급 배지. 64×22, 등급색 알파 0.3, 글자 13 굵게.
- `SpawnKeyCap(parent, key)` (RtsUnitSelectLogic:297): 오른쪽 끝의 단축키 표시. a(1,0.5) (-6,0) 58×24, 배경 (0.12,0.1,0.08,0.9), 테두리 (0.95,0.9,0.75,0.9), 글자 12 굵게.
- `SpawnLvRow`/`ApplyLvRow` (RtsUnitSelectLogic:244/261): "LV.UP (350[메소 아이콘])" 한 줄. **글자 폭을 잴 수 없어서** 오른쪽부터 `)` → 동전 18×18 → 글자 순으로 붙인다. 최대 레벨이면 "LV.MAX"만 보인다.

### 1.4 색 토큰 (RtsHudLogic:245-276, RtsPopupLogic:266-289)
| 메서드 | Color 값 | 대략 HEX | 쓰임 |
|---|---|---|---|
| `ColInk()` | (0.957, 0.914, 0.812, 1) | #F4E9CF | 기본 글자 |
| `ColMuted()` | (0.788, 0.710, 0.541, 1) | #C9B58A | 보조 글자, 라벨 키 |
| `ColGold()` | (0.878, 0.725, 0.353, 1) | #E0B95A | 강조 테두리, 선택, 스크롤바 손잡이, 강조 글자 |
| `ColPanel()` | (0.094, 0.082, 0.071, 0.86) | #181512 α0.86 | HUD 패널·버튼 배경 |
| `ColBorder()` | (0.788, 0.635, 0.290, 0.55) | #C9A24A α0.55 | HUD 기본 테두리 |
| `ColBorderSoft()` | (0.788, 0.635, 0.290, 0.35) | #C9A24A α0.35 | 약한 테두리, 구분선 |
| `SeriesColor(series)` | war (0.839,0.471,0.353) #D6785A · arc (0.310,0.604,0.388) #4F9A63 · mag (0.357,0.525,0.847) #5B86D8 · thf (0.557,0.357,0.847) #8E5BD8 · 기타 (0.541,0.498,0.439) #8A7F70 | | 유닛 계열 띠(슬롯·증강 칩) |
| `Base()` (팝업) | (0.11, 0.094, 0.075, 1) | #1C1813 | Mix의 바탕 |
| `GradeColor(g)` (팝업) | bronze (0.722,0.451,0.2) #B87333 · silver (0.725,0.761,0.8) #B9C2CC · gold = ColGold · prism (0.769,0.549,0.941) #C48CF0 · 기타 #8A7F70 | | 증강 등급 띠·배지·3택1 빛 |

토큰으로 빼지 않고 여러 곳에 **직접 적힌** 색도 있다. 톤을 바꿀 때는 아래 값도 같이 찾아 바꿔야 한다.
- 켜짐 배경 (0.22,0.185,0.118,0.94) · 금색 채움 버튼 배경 (0.3,0.24,0.12,0.96) + 글자 (1,0.95,0.8) · 반짝임/내 선택 배경 (0.45,0.37,0.18,0.96) + 테두리 (1,0.9,0.55) + 글자 (1,0.97,0.85)
- 위험(나가기·방출·확인 대기) 배경 (0.3,0.13,0.11,0.94), 테두리 (0.8,0.35,0.3), 글자 (0.98,0.72,0.66) · 경고 붉은색 (0.95,0.45,0.4) · 필드 경고 (0.92,0.32,0.28)
- 설명 본문 (0.902,0.863,0.769) · 밝은 글자 (0.973,0.925,0.784) · 흐린 글자 (0.55,0.51,0.45) 계열
- 리치텍스트 문자열 안의 색: `#e0b95a`(스페셜·(나)·보스), `#c9b58a`, `#d7b4ff`/`#8a8378`(뽑기 프리즘), `#8fd18a`/`#e88a7a`(찬성/반대), `#9fd39a`(▲), `#a3957a`, `#d9cba6`, `#c48cf0`(프리즘), `#8a8072`(미획득)

### 1.5 글꼴 크기 관례
글꼴은 엔진 기본 글꼴이다(스크립트에서 바꾸지 않음). 크기는 아래 관례를 따른다.
| 크기 | 쓰는 곳 |
|---|---|
| 27~28 | 팝업 제목(27, RtsPopupLogic:94), 결과 머리글(28, :423) |
| 21~23 | 정보 카드 윗줄·시간·메소(22), 3택1 카드 이름(21), 증강 상세 이름(23) |
| 19~20 | HUD 큰 버튼 글자(영입·증강 20, 다시 하기·펼치기 19), 필드 값(20), 몬스터 이름(19), 결과 줄(19) |
| 17~18 | 맵 이름(18), 안내(17), 목록 행 이름(17), 탭(영입 17), 난이도 카드 글자(17) |
| 14~16 | 버튼·탭 보통 글자(15~16), 설명 본문(14~15), 플레이어 이름(16) |
| 10~13 | 보조 라벨(13), 슬롯 Lv·키캡·잠금 토글(12), 스킨 안내(11) |

### 1.6 효과음 규칙
| 소리 | RUID (프로퍼티) | 언제 |
|---|---|---|
| 클릭(원작 BtMouseClick) | `972843e759204d3e9ad84e7d3fa94f83` (`ClickSound`, RtsHudLogic:125) | `SpawnClick`로 만든 모든 버튼(자동). 팝업 딤은 `SpawnStretch`로 만든 버튼이라 클릭음이 없고, 대신 닫기음이 난다 |
| 창 열기(MenuUp) | `585c8f6d8891403f8717c378ab2f7c78` (`OpenSound`, :127) | 팝업을 처음 열 때(RtsPopupLogic:123 — 다시 그리기와 `pick`은 빠짐), 캐릭터 메뉴(RtsUnitSelectLogic:137), 몬스터 정보(RtsMonsterInfoLogic:97 — 같은 몬스터는 빠짐) |
| 창 닫기(MenuDown) | `69f85d65004541db82615459032e1d4a` (`CloseSound`, :129) | 팝업 닫기(RtsPopupLogic:223 — 다시 그리기와 `pick`은 빠짐) |
| 영입 칸 열림(증강 3택1과 같은 업적 달성음, 2026-09-24) | `dbb38b4f04044499906bd7a2ca9c4d7c` (`RecruitSound`, :45) | 진행 중 영입 한도가 늘어날 때(:755) |
| 3택1 등장(업적 달성음) | `dbb38b4f04044499906bd7a2ca9c4d7c` (`PickSound`, RtsPopupLogic:61) | 3택1 본문을 그릴 때마다(:1090) |
| 레벨업 | `LevelUpSound` `c198d87b…` + 클립 `d92f2ec7…` (RtsUnitLogic:649/653) | 레벨업 버튼·Space(RtsUnitLogic:631-637) |

새 버튼은 반드시 `SpawnClick`으로 만든다. 그래야 클릭음이 저절로 붙는다(로드맵 Cross-Cutting 규칙).

### 1.7 텍스트 관례
- **모든 라벨은 BestFit**(2026-09-24): `SpawnLabel`이 `TextComponent.BestFit = true`, `MaxSize` = 지정 크기, `MinSize` = 60%(최소 9)로 만든다. 글이 칸보다 길면 넘치거나 두 줄로 꺾여 겹치지 않고 칸 안에서 작아진다. 글자 크기를 나중에 바꿀 땐 `FontSize`가 아니라 `_RtsHudLogic:SetLabelSize(e, size)`(MaxSize까지 같이)를 쓴다. 칸 크기는 여전히 넉넉히 잡는다(BestFit은 마지막 안전망).
- 정보 카드(2026-09-24): 440×138 — 윗줄 라운드·시간 / 둘째 줄 '지역 - 맵'(412px) / 셋째 줄 난이도(금색 15) / 구분선 y −94 / 아랫줄 메소·필드. 플레이어 목록은 y −166부터. → **2026-09-25 프로필 상자와 합쳐 좌상단 상자 400×240(배경 = 테마 썸네일) 안 정보 칸으로 — 3.0·3.1**
- 한 줄 라벨이 넘치면 `Overflow = OverflowType.Truncate`로 자른다. `ellipsis` 모드에는 긴 새 글이 오면 이전 글이 그대로 남는 버그가 있다(docs/msw-engine.md:22-24, RtsHudLogic:391).
- **Truncate와 리치텍스트는 같이 쓰지 않는다.** 태그가 잘려서 그대로 드러나기 때문에 잘릴 수 있는 라벨은 평문으로 둔다(RtsHudLogic:975). `UseNBSP = true`를 켜면 단어 중간에서 줄이 끊기지 않는다.
- 이모지는 게임 글꼴에 없어서 안 그려진다(실측, RtsUnitPopupLogic:579). `✓ ▾ ▴ ▼ ▲ · —` 같은 기호는 쓰고 있다.
- 글자 폭을 잴 수 없다. 여러 줄 설명의 높이는 어림으로 계산한다(`DescLines`: 14px 글꼴 기준 한글 13px, 그 외 8px, 1~3줄, RtsUnitPopupLogic:414-427).
- 숫자를 화면에 보일 때는 `Int()`/`FormatNumber()`를 쓴다. 동기화된 number를 `tostring`하면 "1.0"이 된다(CLAUDE.md, docs/msw-engine.md:26-28).

---

## 2. 화면 지도 (1920×1080)

가로는 대략 축척(1칸 ≈ 22px)이고 세로는 줄였다. 정확한 값은 아래 범례와 3장 표에 있다.
```
        x=0                   x=480                 x=960                x=1440           x=1920
y=0    +------------------------------------------------------------------------------------------+
y=16   | +-------------------+                              +--------+                   (engine  |
       | | A                 |                              | D      |                    system  |
y=80   | |                   |                              +--------+                    buttons)|
y=88   | |                   |    +----------------------------------+                            |
       | |                   |    | F diff bar (idle/countdown)      |                            |
y=104  | |                   |    | H hint 720x44 @y92 (same spot)   |                   +-----+  |
       | |                   |    | E vote 260x76 @x1138,y86         |                   |G1   |  |
y=128  | +-------------------+    |                                  |                   +-----+  |
y=140  | +---------+              +----------------------------------+                   |G2   |  |
       | | B       |                                                                     +-----+  |
       | | 0/8     |                                                                     |G3   |  |
       | | row1    |                                                                     +-----+  |
       | | row2 ...|                                                                     |G4   |  |
       | |         |                                                                     +-----+  |
       | |         |                                                                     |G5   |  |
       | | row8    |                                                                     +-----+  |
y=354  | |         |                                                                     |G6   |  |
y=404  | |         |                                                                     +-----+  |
       | |         |                                                                     |R    |  |
y=460  | |         |                                                                     +-----+  |
y=540  | +---------+                                                                              |
       |                  world: my zone grid 16x13 (units / monsters / boss area)                |
       |                        N unit menu 300x214 (right of clicked unit)                       |
       |                  +--------------------------------------------------+                    |
       |                  |  P popup  (centered, dim 0.45, width 640~1229)   |                    |
       |                  +--------------------------------------------------+                    |
y=904  |                                    +--------+                                            |
       |                                    | M2     |                                            |
y=930  | +-----+                            +--------+                                            |
       | | K   |                                                                                  |
y=946  | |     |                       +-------------------------+                                |
y=970  | +-----------+                 | M monster info 576x118  |                                |
       | | Y         |                 |                         |                                |
y=1014 | +-----+-----+                 |                         |                     +-------+  |
       | | U   | X   |                 |                         |                     | V     |  |
y=1064 | +-----+-----+                 +-------------------------+                     +-------+  |
y=1080 +------------------------------------------------------------------------------------------+
```
| 기호 | 요소 (루트 엔티티) | 화면 절대 사각형 (x0~x1, y0~y1) | 근거 |
|---|---|---|---|
| T+A | 좌상단 상자 `RtsTopBox` (2026-09-25 프로필 상자 + 정보 카드를 하나로, 배경 = 테마 썸네일) — 위 64 프로필 줄, 아래 정보 칸 `RtsInfoCard` | 16~416, 16~256 | RtsHudLogic `BuildTopBox` · `BuildHud` |
| B | 유저 카드 목록 `RtsPlayers` (카드 y 290+158·(i−1), 250×150 — 2026-09-25 5:3, 4장) | 16~266, 266~922 | `AddPlayerCard` |
| D | 다시 하기 `RtsRestartBtn` (2026-09-24 오른쪽 아래로) | 1704~1904, 1000~1064 | RtsHudLogic `RtsRestartBtn` |
| E | 투표 패널 `RtsVotePanel` (다시 하기 바로 위) | 1644~1904, 916~992 | RtsHudLogic `RtsVotePanel` |
| F | 난이도 막대 `RtsDiffBar` (폭 780 = 86+6·88+5·6+12+124, 2026-09-25 화면 최상단으로) | 570~1350, 0~80 | RtsDifficultyLogic `Build` |
| H | 안내 `RtsHint` | 600~1320, 92~136 | RtsHudLogic:456 |
| G1~G6 | 유닛 슬롯 `RtsUnitSlot1~6` | 1774~1904, 104+50·(i−1) ~ +44 | :383-384 |
| R | 영입/나가기 `RtsRecruitBtn` | 1774~1904, 404~460 | :339 |
| (sys) | 엔진 시스템 버튼 자리. 비워 둔다 | 오른쪽 위, y < 104 | :381 주석 |
| K | 증강 도감 `RtsCodexBtn` | 16~146, 930~970 | :415 |
| Y | 증강 뽑기 `RtsBuyBtn` | 16~296, 970~1014 | :433 |
| U | 증강 `RtsAugBtn` | 16~146, 1014~1064 | :405 |
| X | 펼치기 `RtsExpandBtn` | 146~296, 1014~1064 | :423 |
| M | 몬스터 정보 `RtsMonInfo` (아래 40px = 디버프 줄 M2) | 672~1248, 904~1064 | RtsMonsterInfoLogic:101 |
| M3 | 디버프 설명 창 `RtsMonInfoTip` (칩에 마우스 오버) | 1256~1596, 904~1064 | RtsMonsterInfoLogic `ShowTip` |
| V | 테스트 프리즘 `RtsDevBtn` (`RtsUnitLogic.DevTools`가 켜졌을 때만 — 지금 기본값 false, RtsUnitLogic:14) | 1536~1696, 1014~1064 (다시 하기 왼쪽) | RtsHudLogic `RtsDevBtn` |
| N | 캐릭터 클릭 메뉴 `RtsUnitMenu` | 클릭한 유닛 오른쪽 어깨 옆, 화면 안쪽으로 밀림 | RtsUnitSelectLogic:139-164 |
| P | 팝업 `RtsPopupPanel` | 화면 정중앙 | RtsPopupLogic:88 |

(위 ASCII 그림의 A·B 자리는 2026-09-25 전 기준 — 지금은 T·A가 한 상자(400×240)로 합쳐졌고 B는 그 아래 y 266부터. 좌표는 이 표가 맞다.)

**겹치는 자리**: F·H·E는 같은 띠(y 86~168)를 쓴다. 막대(F)는 idle·countdown에만 보이고 투표(E)는 누군가 표를 던졌을 때만 보이므로 평소에는 겹치지 않는다. 다만 카운트다운 중에 안내(H) 토스트가 뜨면(예: 뽑기 불가 안내, RtsAugmentLogic:378/383) 막대 위에 겹친다.

---

## 3. HUD 요소 목록

패널은 `SpawnPanel`로 만들었으므로 바깥 이름이 `X`이고 안쪽 이름이 `XIn`이다. "만드는 곳"의 줄 번호는 따로 적지 않으면 `RtsHudLogic.mlua` 기준이다.

### 3.0 좌상단 상자 (T+A) — 프로필 줄 (2026-09-25 사용자 "맵 테마 창을 프로필 설정으로" → "좌측을 아이콘으로, 테마를 배경으로" → "정보 카드와 하나로 합치고 배경을 보여줘")
| 요소 | 엔티티 이름 | 만드는 곳 | anchor·pivot·위치·크기 | 색·글꼴 | 보이는 조건 | 클릭/동작 |
|---|---|---|---|---|---|---|
| 상자 틀 | `RtsTopBox`/`In` | `BuildTopBox` | a(0,1) p(0,1) (16,-16) **400×240**(= 테마 썸네일 원본 크기 — 늘리거나 자르지 않는다), 테두리 1.5 | ColPanel / ColBorder | 항상 | — |
| 배경 | `RtsProfileBg` | 〃 | 상자 전체 | 내 테마 프리셋 `thumb`(없으면 `color` 단색 — `PaintThumb`) | 항상 | — |
| 어두운 막 | `RtsProfileShade` | 〃 | 상자 전체 | (0.06,0.05,0.04,0.55) | 항상 | — |
| 프로필 줄 | `RtsProfileRow` | 〃 | a(0,1)~(1,1) 위 64 | 투명 | 항상 | 이 줄만 클릭 → `_RtsPopupLogic:Open("profile")` |
| 아이콘 칸 | `RtsProfileIconSlot` | 〃 | 줄 안 a(0,0.5) p(0,0.5) (10,0) 48×48 | 이미지 = `CircleMaskRUID`(원형), 투명 (아이콘 없음이면 흰색 α0.15) — 2026-09-25 검정 → 흰색 → 투명, 마스크 없음 — 아이콘 없음이면 빈 원에 α0.45, 글자 없음 | 항상 | — |
| 아이콘 | `RtsPortrait` | `SpawnMonsterPortrait` | 칸 가운데 48, 몬스터 썸네일(`RtsMonsterThumbLogic`) | 원색 | 내 아이콘이 있을 때. `RefreshProfileBox`가 아이콘이 바뀐 때만 다시 만든다 | — |
| "프로필 설정" | `RtsProfileTitle` | 〃 | 줄 안 a(0,1) p(0,1) (70,-6) 220×28 | ColInk 18 굵게 | 항상 | — |
| 요약 | `RtsProfileSummary` | 〃 | 줄 안 a(0,1) p(0,1) (70,-34) 250×24 | (0.86,0.82,0.74) 14 | 항상 | "테마 ○○" — `RefreshProfileBox`(서버 `SendProfileState` 받을 때) |
| "변경 ›" | `RtsProfileChange` | 〃 | 줄 안 a(1,0.5) p(1,0.5) (-14,0) 80×30 | ColGold 16 굵게 | 항상 | — |
| 구분선 | `RtsTopLine` | 〃 | a(0,1) p(0,1) (12,-67) 376×1.5 | ColBorderSoft | 항상 | — |
| 정보 칸 | `RtsInfoCard` | 〃(돌려줌) | 상자 안 위 72 아래 전체(400×168), 투명 | — | 항상 | 3.1 요소들의 부모 |

테마 = 내 구역 바닥·트랙 판·장식만(밸런스 영향 없음). 프리셋·인계 절차는 `docs/theme-presets.md`.

### 3.1 좌상단 상자 (T+A) — 정보 칸 (`RtsInfoCard` 안, 2026-09-25 전엔 따로 440×138 카드)
| 요소 | 엔티티 이름 | 만드는 곳 | anchor·pivot·위치·크기 | 색·글꼴 | 보이는 조건 | 클릭/동작 |
|---|---|---|---|---|---|---|
| 윗줄 제목 | `RtsStageTitle` | BuildHud | a(0,1) p(0,1) (14,-8) 290×32 | ColInk 22 굵게, 리치, Truncate | 항상 | `SetStageCard`(:503)가 씀. 스페셜 라운드면 `  <color=#e0b95a>스페셜</color>`를 붙임 |
| 남은 시간 | `RtsStageClock` | :309 | a(1,1) p(1,1) (-14,-8) 90×32 | ColInk 22 굵게, 오른쪽 정렬 | 항상 (대기·종료엔 빈칸) | 〃 |
| 맵 이름 | `RtsStageSub` | 〃 | a(0,1) p(0,1) (14,-38) 372×28 | (0.86,0.82,0.74) 18, Truncate, NBSP | 항상 | 〃 |
| 난이도 글자 | `RtsDiffCardText` | RtsDifficultyLogic | 칸 안 a(0,1) p(0,1) (14,-64) 372×24 | ColGold 15 굵게 | 항상 ("난이도 보통") | RtsDifficultyLogic.ClientTick |
| 구분선 | `RtsInfoLine` | 〃 | a(0,1) p(0,1) (12,-110) 376×1.5 | ColBorderSoft | 항상 | — |
| 메소 동전 | `RtsMesoCoin` | :319 | a(0,0) p(0,0.5) (14,22) 24×24 | `CoinRUID` 원색 | 항상 | — |
| 메소 | `RtsMesoText` | :322 | a(0,0) p(0,0.5) (46,22) 200×32 | ColInk 22 굵게 | 항상 | `SetMeso`(:804), 천 단위 쉼표 |
| "필드" | `RtsFieldKey` | :325 | a(1,0) p(1,0.5) (-122,22) 44×28 | (0.86,0.82,0.74) 15, 오른쪽 | 항상 | — |
| 필드 값 | `RtsFieldText` | :327 | a(1,0) p(1,0.5) (-14,22) 104×32 | ColInk 20 굵게, 오른쪽. `n ≥ 한도−20`이면 (0.92,0.32,0.28) | 항상 | `SetField`(:516). 한도는 `RtsWaveLogic.FieldLimit` = 110 |

윗줄·맵·시간 글자는 상태마다 다르다(`RtsStageLogic.StageParts`, :414-431). 대기 = "대기 중". 카운트다운 = "시작까지"와 남은 초. 진행 = "n라운드" + 맵 + m:ss. 보스 = "보스" + 맵. 쉬는 = "쉬는 시간". 보스 준비 = "보스 준비" + 다음 맵 + 초. 종료 = "게임 종료".

### 3.2 좌측 유저 카드 (B) — 2026-09-25 (사용자 "영역을 키워서 배경 = 그 사람 테마 썸네일, 좌측 동그라미 아이콘, 우측 닉네임, 나는 (나) 대신 굵은 초록 테두리" → "박스 크기를 배경 사진 비율에 맞게 — 총 4명으로 조절할 거라 조금 높아져도 됨")
| 요소 | 엔티티 이름 | 만드는 곳 | anchor·pivot·위치·크기 | 색·글꼴 | 보이는 조건 | 클릭/동작 |
|---|---|---|---|---|---|---|
| 목록 틀 | `RtsPlayers` | BuildHud | a(0,1) p(0,1) (16,-266) 250×(24 + 4·158) | 투명 | 항상 | — |
| 머리 "n / 8" | `RtsPlayerHead` | 〃 | a(0,1) p(0,1) (6,0) 200×20 | (0.49,0.525,0.584) 13 | 항상 | 분모는 구역 수 |
| 카드 i | `RtsPlayerRow{i}`/`In` | `AddPlayerCard` | a(0,1) p(0,1) (0, −24−158·(i−1)) `CardW`250×`CardH`150(5:3 = 썸네일 비율, 4장 — 5장째부터는 아래 [증강 도감] 버튼과 겹친다). 테두리 = 나 3px 초록(0.35,0.8,0.42) / 남 1.5 | 안쪽 = 그 유저 테마 `thumb`(없으면 테마 `color`). 테두리: 나 초록 · 보는 중 ColGold · 그 외 ColBorderSoft | 서버 통지마다 전부 지우고 다시 만든다 | 클릭 → `OnPlayerRowClick` → 그 구역으로 카메라 |
| 얇은 막 | `RtsPlayerShade` | 〃 | 카드 전체 | 생존 (0.06,0.05,0.04,0.12) / 탈락 α0.68 | 〃 | — |
| 이름 띠 | `RtsPlayerBand` | 〃 | a(0,0)~(1,0) 아래 40 | (0.06,0.05,0.04,0.62) | 〃 | — |
| 아이콘 칸 | `RtsPlayerIconSlot` | 〃 | 카드 사진 영역 가운데 a/p(0.5,0.5), (0,20) 80×80 | 투명(2026-09-25 사용자 검정 → 흰색 → "투명한 색으로" — 전엔 밝은 베이지 α0.72, 뒤 그림자 원·원형 마스크도 뺌). 아이콘 없음이면 칸 자체를 만들지 않아 배경 풍경이 보임 | 아이콘이 있을 때만 | — |
| 아이콘 | `RtsPortrait` | `SpawnMonsterPortrait` | 칸 가운데 80, 몬스터 썸네일(`RtsMonsterThumbLogic`) | 원색, 탈락이면 회색 | 아이콘이 있을 때만 | — |
| 닉네임 | `RtsPlayerName` | 〃 | a(0,0) p(0,0) (10,5) 206×30(이름 띠 안) | ColInk 17 굵게(탈락 (0.604,0.561,0.502)) | 〃 | — |
| 비석 | `RtsPlayerTomb`/`In` | 〃 | a(1,0) p(1,0) (-10,11) 14×17 | (0.29,0.27,0.235) / (0.55,0.51,0.45) | 탈락 | — |

내 카드의 [수정](아이콘 창 열기)은 2026-09-25 사용자 "회원 목록에서의 수정 버튼 삭제"로 뺐다 — 아이콘은 프로필 창 [아이콘] 탭에서 바꾼다.
카드 모양은 `ApplyPlayerLook`이 정한다. 목록 데이터는 서버가 `"userId\t닉\t구역\t생존\t테마\t아이콘\n…"` 문자열로 보낸다(`@ExecSpace("Client") RefreshPlayerList(string)` — 2026-09-25 끝 두 칸 추가, 없으면 henesys·M001). **이 RPC의 서명은 바꾸지 않는다.**

### 3.3 상단 가운데: 난이도 막대·안내 (F·H) + 오른쪽 아래: 다시 하기·투표 (D·E — 2026-09-24 오른쪽 아래로 옮김)
| 요소 | 엔티티 이름 | 만드는 곳 | anchor·pivot·위치·크기 | 색·글꼴 | 보이는 조건 | 클릭/동작 |
|---|---|---|---|---|---|---|
| 다시 하기 | `RtsRestartBtn`/`In` | :349 | a(1,0) p(1,0) (-16,16) 200×64, 테두리 2 (오른쪽 아래) | 모드별(아래 표). 글자 `RtsRestartLabel` 192×56 19 굵게 | 항상 | `OnRestartButton`(:594). 진행 중에는 3초 안에 한 번 더 눌러야 찬성, 종료 뒤에는 바로 찬성, 이미 찬성했으면 취소 |
| 투표 패널 | `RtsVotePanel`/`In` | :359 | a(1,0) p(1,0) (-16,88) 260×76, 테두리 1.5 (다시 하기 바로 위) | ColPanel / ColGold | 찬성+반대 > 0 (`RefreshVotePanel` :667) | — |
| 투표 글 | `RtsVoteText` | :362 | a(0,1) p(0,1) (10,-4) 240×26 | ColInk 14 굵게 리치. `찬성 n`은 #8fd18a, `반대 m`은 #e88a7a, 그 뒤에 과반·남은 초 | 〃 | — |
| 찬성 / 반대 | `RtsVoteYes`/`RtsVoteNo` (+`Text`, `Click`) | :365 / :372 | a(0,0) p(0,0) (10,8) / (135,8) 115×34 | 보통 ColPanel/ColBorder, 내 선택이면 (0.45,0.37,0.18,0.96)/(1,0.9,0.55). 글자 16 굵게 | 〃 | `_RtsStageLogic:RequestVoteChoice(1 또는 2)` (Server) |
| 난이도 막대 | `RtsDiffBar`/`In` | RtsDifficultyLogic `Build` | a(0.5,1) p(0.5,1) **(0,0)** 780×80 — 화면 최상단(2026-09-25 사용자 "최상단에 붙게", 전엔 y −88) | ColPanel / ColBorder | idle·countdown | — |
| "난이도" | `RtsDiffTitle` | RtsDifficultyLogic:162 | a(0,1) p(0,1) (12,-6) 70×36 | ColMuted 16 굵게 | 〃 | — |
| 난이도 6칸 | `RtsDiffBtn1~6` (+`Text`, `RtsDiffClick{i}`) | RtsDifficultyLogic:167 | a(0,1) p(0,1) (86+94·(i−1), -6) 88×36 | 선택: (0.3,0.24,0.12,0.96)/ColGold, 나머지: ColPanel/ColBorder. 글자 15 굵게 | 〃 | `RequestSet(i)` (Server, running이면 거부). 이름: 매우쉬움·쉬움·보통·어려움·매우어려움·극악 |
| 바로 시작 | `RtsDiffStart` (+`Text`, `Click`) | RtsDifficultyLogic:178 | a(1,1) p(1,1) (-12,-6) 112×36, 테두리 2 | (0.3,0.24,0.12,0.96)/ColGold, 글자 (1,0.95,0.8) 15 | countdown만 (:132) | `_RtsStageLogic:RequestStartNow()` (Server). 여럿이면 "바로 시작 r/n", 내가 누른 뒤엔 "대기 r/n" |
| 막대 안내 줄 | `RtsDiffMsg` | RtsDifficultyLogic:163 | a(0,0) p(0,0) (12,6) 756×26 | (1,0.86,0.55) 14 | 막대와 같이 | 남은 초와 지금 선택한 난이도 |
| 안내(힌트) | `RtsHint`/`In` + `RtsHintText` | :456-461 | a(0.5,1) p(0.5,1) (0,-92) 720×44. 글자 700×36 | (0.22,0.185,0.118,0.94)/ColGold, 글자 ColInk 17 굵게 | `ShowHint`(:477, 끌 때까지) / `ShowHintFor`(:491, n초) | 클릭 없음 |

'다시 하기' 모드(`RefreshRestartButton` :616-663):
| 모드 | 조건 | 글자 | 안쪽 / 테두리 / 글자색 |
|---|---|---|---|
| idle | running·ended가 아님 | 다시 하기 | ColPanel / ColBorderSoft / ColMuted |
| off | 표 없음 | 다시 하기 | ColPanel / ColBorder / ColInk |
| on | 누가 찬성함, 또는 ended | 다시 하기 n/k | (0.22,0.185,0.118,0.94) / ColGold / (0.973,0.925,0.784) |
| mine | 내가 찬성함 | 다시 하기 ✓ n/k | (0.45,0.37,0.18,0.96) / (1,0.9,0.55) / (1,0.97,0.85) |
| confirm | 첫 클릭 뒤 3초 | 한 번 더 누르면 찬성 | (0.3,0.13,0.11,0.94) / (0.8,0.35,0.3) / (0.98,0.72,0.66) |

안내(H)에 뜨는 문구와 호출처: 위치 이동(RtsUnitSelectLogic:383, 켜 둠) · 영입 배치(:445, 켜 둠) · 다시 하기 확인(RtsHudLogic:609, 3초) · 보스 등장 초읽기 "○○ 등장까지 n초"(RtsStageLogic:465, 1.2초) · 게임 종료(:472, 6초) · 뽑기 불가(RtsAugmentLogic:378/383, 3초) · 매칭 미연결(RtsRunResultLogic:340, 4초).

### 3.4 우측 유닛 슬롯·영입 (G·R)
| 요소 | 엔티티 이름 | 만드는 곳 | anchor·pivot·위치·크기 | 색·글꼴 | 보이는 조건 | 클릭/동작 |
|---|---|---|---|---|---|---|
| 슬롯 i (1~6) | `RtsUnitSlot{i}`/`In` | :384 | a(1,1) p(1,1) (-16, −104−50·(i−1)) 130×44, 테두리 1.5 | 빈칸: (0.094,0.082,0.071,0.35)/(0.788,0.635,0.29,0.2). 채움: ColPanel/ColBorderSoft. 선택: (0.22,0.185,0.118,0.92)/ColGold (`ApplySlotLook` :1001) | 항상 6칸 | 채워진 칸만 반응. 클릭 → 선택 표시 + `_RtsUnitPopupLogic:OpenUnit(i)` (:1024) |
| 계열 띠 | `RtsUnitSlotBar{i}` | :386 | 스트레치 왼쪽 4px | `SeriesColor(계열)`, 빈칸은 (0.541,0.498,0.439,0.35) | 〃 | — |
| 이름 | `RtsUnitSlotName{i}` | :389 | a(0,0.5) p(0,0.5) (10,0). 빈칸 110×30 14 가운데 "빈 자리" / 채움 80×30 13 왼쪽 "n. 직업" | 채움 ColInk, 빈칸 (0.788,0.71,0.541,0.5). Truncate·NBSP·평문 | 〃 | `SetUnitSlot`(:971) / `ClearUnitSlot`(:986) |
| 레벨 | `RtsUnitSlotLv{i}` | :394 | a(1,0.5) p(1,0.5) (-8,0) 40×30 | ColMuted 12, 오른쪽, "Lv n" | 채운 칸 | — |
| 영입 / 나가기 | `RtsRecruitBtn`/`In`, `RtsRecruitLabel`, `RtsRecruitClick` | :339-347 | a(1,1) p(1,1) (-16,-404) 130×56, 테두리 2. 글자 126×48 20 굵게 | 영입 가능: (0.22,0.185,0.118,0.94)/ColGold/(0.973,0.925,0.784). 칸이 새로 열리면 1.5초 반짝: (0.45,0.37,0.18,0.96)/(1,0.9,0.55)/(1,0.97,0.85). 나가기: (0.3,0.13,0.11,0.94)/(0.8,0.35,0.3)/(0.98,0.72,0.66) | '나가기'(ended, 또는 내가 탈락·클리어) 또는 running이면서 빈 칸이 있을 때만 (:722-724) | `OnTopButton`(:701): 나가기 상태면 `RequestExit`, 아니면 영입 팝업 |

슬롯 위쪽(y < 104)은 엔진 시스템 버튼 자리라서 비워 둔다(:381). 영입 글자는 "영입 가능 n"이다. "영입 불가"·"영입 완료"·"다음 영입 · n라운드" 문구도 계산은 하지만(:738-750), 그 상태에서는 버튼이 숨겨져 있어 실제로 보이지 않는다.

### 3.5 좌하단 증강 버튼 묶음 (U·X·Y·K)
| 요소 | 엔티티 이름 | 만드는 곳 | anchor·pivot·위치·크기 | 색·글꼴 | 보이는 조건 | 클릭/동작 |
|---|---|---|---|---|---|---|
| 증강 | `RtsAugBtn`/`In`, `RtsAugLabel`, `RtsAugClick` | :405-413 | a(0,0) p(0,0) (16,16) 130×50, 테두리 1.5. 글자 126×40 20 굵게 | ColPanel/ColBorder. 미지정 증강이 있으면 테두리 (0.95,0.45,0.4)에 글자 "증강 (n)" (`SetAugmentCount` :528) | 항상 | `_RtsPopupLogic:Open("augment")` |
| 펼치기 | `RtsExpandBtn`/`In`, `RtsExpandLabel`, `RtsExpandClick` | :423-432 | a(0,0) p(0,0) (146,16) 150×50, 테두리 2. 글자 146×40 19 굵게 | (0.3,0.24,0.12,0.96)/ColGold, 글자 (1,0.95,0.8) | 고르지 않은 3택1이 있고 3택1 창이 닫혀 있을 때 (`SetPendingOffers` :583) | `_RtsAugmentLogic:ExpandPick()` → 3택1 다시 열기. n>1이면 "펼치기 (n)" |
| 증강 뽑기 | `RtsBuyBtn`/`In`, `RtsBuyLabel`, `RtsBuyClick` | :433-441 | a(0,0) p(0,0) (16,66) 280×44, 테두리 1.5. 글자 270×38 16 굵게 리치 | 가능: (0.3,0.24,0.12,0.96)/ColGold/(1,0.95,0.8). 불가: ColPanel/ColBorderSoft/ColMuted (`SetBuyButton` :560) | 항상 | `_RtsAugmentLogic:BuyFromHud()` → `RequestBuy`(Server). 글자 예: `증강 뽑기  3,000   <size=13><color=#d7b4ff>프리즘 2/2 · 5%</color></size>` (프리즘이 남지 않으면 #8a8378) |
| 증강 도감 | `RtsCodexBtn`/`In`, `RtsCodexLabel`, `RtsCodexClick` | :415-422 | a(0,0) p(0,0) (16,110) 130×40, 테두리 1.5. 글자 126×34 17 굵게 | ColPanel/ColBorder | 항상 | `_RtsPopupLogic:Open("codex")` |

네 버튼은 사용자 요청으로 틈 없이 붙어 있다(:404). 증강·뽑기·펼치기 값은 `RtsAugmentLogic.ClientTick`이 0.3초마다 밀어 넣는다(RtsAugmentLogic:66, :433-463).

### 3.6 하단 가운데 몬스터 정보 (M·M2) — RtsMonsterInfoLogic
- **2026-09-24 디버프 줄**(사용자 "네모 박스 높이를 키워서 아래에 디버프, 마우스 오버하면 박스 우측에" → "빙/파/약/독 말고 빙결·중독처럼 이름으로"): 정보 창을 118 → 160으로 키우고 **창 안 아래 줄**에 디버프 칩을 둔다. 칩 = 아이콘 그림(있으면) 또는 왼쪽 색 띠 + **디버프 이름**. 효과 수치·남은 시간은 칩에 마우스를 올리면 **정보 창 바로 오른쪽**에 뜨는 설명 창에 나온다(설명 창은 `RaycastTarget = false` — 마우스를 가로채 깜빡이던 문제).
| 요소 | 엔티티 이름 | 만드는 곳 | anchor·pivot·위치·크기 | 색·글꼴 | 비고 |
|---|---|---|---|---|---|
| 패널 | `RtsMonInfo`/`In` | `Open` | HudGroup 기준 a(0.5,0) p(0.5,0) (0,16) 576×`PanelH` 160 (576 = LeftX 118 + BarW 366 + 4 + PctW 70 + 18) | (0.11,0.094,0.075,0.95) / ColGold 1.5 | 몬스터를 클릭하면 열린다. 0.2초마다 갱신 |
| 초상 칸 | `RtsMonInfoIconBack` | `Open` | a(0,1) p(0,1) (12,-10) 94×94 (이름·체력·정보 줄 높이에 맞춤) | (0.2,0.17,0.15). **MaskComponent**로 칸 밖을 자른다 | — |
| 초상 | `RtsMonInfoIcon` | `Open` | 칸 가운데 86×86. 걷기 클립 반복, NativeSize, LocalScale = 칸에 맞춘 배율(최대 2.5) | 원색 | 크기·위치는 ImageRUID를 넣은 **뒤에** 준다 | **2026-09-25부터 썸네일이 있으면 걷기 클립 대신 몬스터 썸네일(256 정사각)을 칸 크기로** — `SpawnMonsterPortrait` |
| 이름 | `RtsMonInfoName` | `Open` | a(0,1) p(0,1) (118,-8) 440×28 | ColInk 19 굵게 리치. 보스면 뒤에 `<color=#e0b95a>보스</color>` | — |
| 체력바 | `RtsMonInfoHpBack` / `RtsMonInfoHpFill` | `Open` | (118,-42) 366×26. 채움 폭 = 366 × 비율 | (0.2,0.17,0.15) / (0.85,0.2,0.2) | — |
| 체력 글자 | `RtsMonInfoHpText` | `Open` | 체력바와 같은 사각형 | 흰색 15 굵게 가운데 "현재 / 최대" | — |
| 체력 % | `RtsMonInfoHpPct` | `Open` | (488,-42) 70×26 | ColInk 16 굵게 오른쪽 "%.1f%" | — |
| 정보 줄 | `RtsMonInfoText` | `Open` | (118,-76) 440×28 | ColMuted 15 | "방어율 n% (보스만) · n라운드 · 지역 - 맵" |
| 디버프 줄 | `RtsMonInfoDebuffs` (+ 구분선 `RtsMonInfoDebuffLine`) | `RefreshDebuffs` | 패널 안쪽 a(0,0) p(0,0) (12,8) 552×34. 구분선 = 줄 위 5px, 552×1.5 | 투명 / ColBorderSoft | 디버프 목록(id 순서)이 바뀔 때만 다시 만든다. 없으면 "걸린 디버프 없음"(ColMuted 14) |
| 디버프 칩 | `RtsMonInfoDebuff{id}`/`In` | `RefreshDebuffs` | 높이 32, 폭 = 앞머리(그림 34 / 색 띠 14) + 이름 글자 수 × 15 + 12, 간격 6. 합이 552를 넘으면 같은 비율로 줄인다(라벨 BestFit) | (0.16,0.135,0.11) / ColBorderSoft 1. 이름 `RtsMonInfoDebuffName` ColInk 14 굵게 | 바깥 틀에 `UITouchReceiveComponent` + UITouchEnter/Exit → `ShowTip`/`HideTip`. 자식은 `RaycastTarget = false` |
| 칩 그림 / 색 띠 | `RtsMonInfoDebuffIcon` 24×24 (PreserveSprite None) / `RtsMonInfoDebuffBar` 4×20 | `RefreshDebuffs` | a(0,0.5) (4,0) | 그림: 가드 크러쉬 `b28058e3…`, 방어구 부수기 `1f4eea78…`. 색 띠: 빙결 (0.45,0.78,1) · 방어율 감소 (0.3,0.55,0.95) · 받는 데미지 증가 (0.95,0.8,0.35) · 중독 (0.45,0.8,0.35) | 표시 이름 = `DebuffList`의 `name` |
| 설명 창 | `RtsMonInfoTip`/`In` + `RtsMonInfoTipText` | `ShowTip` | 패널 바깥 기준 a(1,0) p(0,0) (8,0) — 정보 창 바로 오른쪽, 아래 맞춤. 폭 `DebuffBoxW` 340, 높이 = max(160, 설명 줄 수에 맞춤) | (0.11,0.094,0.075,0.97)/ColGold 1.5, ColInk 16 리치 | "**이름** / 설명(효과 수치 포함) / <금색>남은 시간 n.n초 · 조건이 유지되는 동안</금색>" |

열기와 닫기: 유닛이 아닌 월드를 클릭하면 `MonsterAtScreen`으로 **지금 보는 구역**의 몬스터를 찾는다(RtsUnitSelectLogic:485-490, RtsMonsterInfoLogic:59). 빈 곳 클릭, ESC, 몬스터 사망 시 닫힌다(`Close` :146). 닫기음은 없다.

### 3.7 캐릭터 클릭 메뉴 (N) — RtsUnitSelectLogic.OpenMenu (:130-230)
| 요소 | 엔티티 이름 | 줄 | 위치·크기 | 색·글꼴 | 동작 |
|---|---|---|---|---|---|
| 메뉴 틀 | `RtsUnitMenu`/`In` (HudGroup 자식) | 164 | a(0.5,0.5) p(0,0.5). 유닛 월드 위치 (x+0.9, y+1.2)를 UI 좌표로 바꾼 자리. 300×214(행 40×5 + 14). 화면 가장자리 8px 안쪽으로 밀어 넣는다(:150-163) | (0.11,0.094,0.075,0.97) / ColGold 1.5 | 내 유닛을 클릭하면 토글. 빈 곳 클릭·ESC로 닫힘 |
| 머리줄 | `RtsUnitMenuHead` + 선 `RtsUnitMenuHeadLine` | 171-174 | (12,-6) 276×36 / 선 (8,-43) 284×1.5 | ColGold 17 굵게 "LV.n 직업" / ColBorderSoft | `RefreshMenuLevel`(:307)이 갱신 |
| 위치 이동 [L] | `RtsUnitMenuMove` | 184 | (6,-46) 288×36 | Mix(white,0.05) / Mix(Gold,0.35), 글자 16 굵게. 쿨타임 중이면 "이동 대기 m:ss" (0.6,0.56,0.5)이고 클릭 없음 | `MenuMove` → 위치 이동 모드 |
| 상세정보 [S] | `RtsUnitMenuInfo` | 197 | (6,-86) | 〃 | 유닛 팝업 |
| LV.UP [Space] | `RtsUnitMenuLv` | 208 | (6,-126) | 가능: Mix(Gold,0.9)/Gold, 글자 (0.133,0.114,0.09). 불가: Mix(Gold,0.25)/Mix(Gold,0.4), 글자 (0.6,0.55,0.45) | 메뉴를 연 채로 레벨업(`LevelUpShortcut`) |
| 방출 | `RtsUnitMenuDismiss` | 220 | (6,-166) | Mix(white,0.05) / (0.8,0.35,0.3), 글자 (0.95,0.6,0.55) | 메뉴를 닫고 확인 팝업(`dismiss`)을 연다 |

---

## 4. 팝업 (RtsPopupLogic)

### 4.1 셸 구조 (Build :70-107, 한 번에 하나만 열림)
| 층 | 엔티티 이름 | 줄 | 위치·크기 | 색·글꼴 | 동작 |
|---|---|---|---|---|---|
| 그룹 | `RtsPopupGroup` | 73 | `/ui` 자식 | — | 닫혀 있을 때 `SetEnable(false)` |
| 딤 | `RtsPopupDim` (uibutton) | 81 | 화면 전체 스트레치 | (0.039,0.047,0.063,0.45) | 클릭하면 닫힘(`pick`은 제외) |
| 패널 | `RtsPopupPanel`/`In` | 88 | a(0.5,0.5) p(0.5,0.5) (0,0). 기본 1114×500, 종류마다 `RectSize`를 바꿈(:166) | (0.11,0.094,0.075,0.96) / (0.788,0.635,0.29,1), 두께 2.3 | — |
| 제목 | `RtsPopupTitle` | 93 | a(0,1) p(0,1) (27,-20) 600×36 | ColInk 27 굵게 | 종류마다 글자가 다름 |
| 닫기 X | `RtsPopupClose` + `CloseX`·`CloseClick` | 95-103 | a(1,1) p(1,1) (-27,-20) 38×38 | Base() / Mix(Gold,0.5), "X" 20 굵게 | `pick`에서는 숨김 |
| 본문 | `RtsPopupBody` | 172 | 패널 안쪽 스트레치, 위 70px 뺌 | 투명 | **열 때마다 새로 만들고 닫을 때 통째로 지운다** |

- 여는 법: `_RtsPopupLogic:Open(kind)`(:114). 이미 열려 있으면 `Reopening = true`로 닫았다가 다시 연다. 이렇게 다시 그릴 때는 여닫기 소리가 나지 않는다. 팝업을 열면 영입 배치 모드가 취소된다(:125).
- 닫는 법: X, 딤, ESC(:238-243). `pick`은 셋 다 막혀 있어서 카드를 받거나 '접기'를 눌러야만 닫힌다.
- 탭이나 선택을 바꾸면 `Open(kind)`를 다시 불러 본문 전체를 새로 그린다(`RefreshAugment` :851, `RefreshCodex` :869). 유닛 팝업만 예외로 제자리 갱신을 한다(4.3).

### 4.2 종류별 요약
| kind | 제목 | 크기 | 여는 곳 | 구성 |
|---|---|---|---|---|
| `recruit` | 영입 | 1114×430 | HUD 영입 버튼(RtsHudLogic:707). 판 시작 첫 틱에 자동으로 한 번(RtsStageLogic:444-448). 칸 수가 바뀌면 다시 그림(RtsHudLogic:759) | 탭 2 + 계열 4열 × 직업 카드 + 하단 안내. **카드는 모두 클릭 → `PendingJob` → `recruitinfo`**(2026-09-25 — 보유 중·잠김·영입 불가도 보기) |
| `recruitinfo` | 직업 이름(가운데 — 이 창만 제목 가운데) | 600×640 | 영입 카드 클릭 | 왼쪽 위: 외형 칸 150×170(기본 세트 UI 아바타 — `RtsUnitPopupLogic.SpawnPreviewAt`) + 계열 / 오른쪽 위: 오각형(`SpawnRadar`, 반지름 80 — 위부터 시계 방향 공격 속도·사거리·증강 효율·보스·사냥, 5단계 `GetRadar`, 축 이름만) / 아래: 탭 [액티브] [패시브] [프리즘 증강](`RiSkillTab`, [Tab] 키 순환) + 그 탭의 세로 스크롤 목록(줄 "Lv n  이름" + 바로 아래 설명이 늘 보임 — 펼침/접힘 없음, 길면 스크롤. 프리즘 증강 = 그 직업 프리즘, 팬텀은 '영웅 팬텀') / 맨 아래: [선택](→ 닫고 `BeginPlace` 발판 고르기) 또는 이유 줄(`RecruitBlockReason`) · [취소](→ `recruit`). 2026-09-25 사용자 피드백 반복: 폭 900 → 760 → 600 · 설명 문구·능력치 삭제 · 탭 · 영입 → 선택 |
| `augment` | 증강 | 1114×960 | HUD 증강 버튼 | 등급 탭 5 + 왼쪽 보유 목록(스크롤) + 오른쪽 상세·대상 지정 + 숨기기 체크 |
| `codex` | 증강 도감 | 900×820 | HUD 증강 도감 버튼 | 등급 탭 4 + 안내 줄 + 목록(스크롤, 프리즘은 펼치기) |
| `restart` | 다시하기 | 640×280 | 오른쪽 아래 다시하기 · 결과 창 다시하기 · 판이 끝난 뒤 오른쪽 버튼(`OpenRestartConfirm`, 2026-09-24) | 안내 세 줄 + [다시하기](솔로) / [찬성](여럿) + [아니오]. 이미 찬성했으면 다시하기 버튼 = 바로 찬성 취소 |
| `rank` | 순위 | 720×820 | **지금은 여는 곳 없음**(2026-09-25 사용자 "인게임 순위표 제거" — 대기방 순위표 Phase 13에서 다시 씀) | 난이도 탭 3(어려움·매우어려움·극악, `RankDiff`) + 안내 줄 + 목록(스크롤, 1~3위 금색: 순위·닉네임·클리어 n회) + 아래 내 순위 띠. 목록은 서버 `RequestRanking` → `ShowRanking` → `SetRanking`(`RankCache`, 20초 캐시) |
| `pick` | "<등급> 증강 선택" / "보스 처치 — 프리즘 증강 선택" | 1114×580 | 새 선택지가 오면 자동으로(RtsAugmentLogic:446-449). 펼치기 버튼 | 카드 3장 + 접기. 닫기 없음 |
| `unit` | "n. 직업  Lv n · 직업군" | 1229×720 | 슬롯 클릭, 메뉴 상세정보 | 4.3 참고 |
| `dismiss` | 방출 | 640×290 | 메뉴 '방출' → `OpenDismiss`(:198) | 대상 줄 + 경고문 + [방출][취소] |
| `result` | 결과 | 640×360 | 서버 `ShowResult` → `OpenResult`(:206). 탈락·클리어한 본인에게만 | 머리글 + 줄 4개 (+ 클리어 2줄) + 솔로 [닫기][다시 하기] / 여럿 [관전하기][나가기] |
| `devprism` | 테스트 프리즘 증강 (개발용) | 1114×760 | V 버튼(DevTools일 때만) | 프리즘 2열 목록 + 전부 삭제 |
| `profile` | 프로필 설정 | 900×730 | 프로필 상자(T) 클릭 · 확인 창 뒤 · 아이콘 정보 [목록으로] | 위 탭 [테마] [아이콘] [비석](`ProfileTab` — 2026-09-25 사용자 "테마와 비석 사이에 아이콘, 여기서 수정". 탭을 바꾸면 내용 상자만 다시 — `RefreshProfileContent`, 돌아오기는 `OpenProfileTab(tab)`) + 둘째 줄 종류 탭(`BuildKindTabs` 100×30 — 기본/프리미엄…, 지금 [기본]만, 늘 보임) + 그 오른쪽 안내 줄 + **세로 스크롤** 목록(846×554, `SpawnPresetList`) 안에 줄(830×270, 간격 10 — `SpawnPresetRow`)마다 **정사각 카드 3장**(270×270, x = 0·280·560 — `SpawnPresetCard`: 위 가운데 이름 + 오른쪽 위 체크 칸 26×26(사용 중 = 금색 칸 + 체크 `SpawnSegment` 2개) + 그림 칸 250×200(y −44) / 클릭). 한 화면 2줄. [테마] = 썸네일 `PaintThumb` → `themeconfirm` · [비석] = 비석 그림(원본 w·h 비율로 250×190 안) → `tombconfirm`. 보유하지 않은 프리셋(free 아님)은 흐리게·클릭 안 됨 (2026-09-25). **[아이콘]** = 종류 탭('기본') 오른쪽에 "보유 n / 247 · 유저 카드에 보이는 아이콘이에요"(획득 조건·확률은 목록에 적지 않는다 — 칸을 누른 `iconinfo`에만) + **스크롤 격자** 8열(`SpawnScrollGrid`, 칸 94, 간격 8 — "페이징 말고 스크롤"). **첫 칸 = '없음'**(`SpawnIconNoneCell` — 빈 원, 사용 중이면 금색, 누르면 바로 `iconconfirm`). 칸은 `IconBatch`(40)개씩 0.03초 간격으로 위에서부터 채운다(`SpawnIconCell`, 탭이 바뀌면 멈춤). 보유 원색 · 미보유 실루엣 · 사용 중 금색 칸. 칸 → `PendingIcon` → `iconinfo`. 선택이 바뀌면 칸 색만 제자리에서(`RefreshIconCells`) — 전엔 따로 `icon` 창(900×700, 유저 카드 [수정])이었다 |
| `tombconfirm` | 비석 | 640×300 | 비석 카드 클릭 | "비석을 변경하시겠습니까? → 이름" + [예](`RequestSetTomb`) / [아니오](→ `profile`) — `BuildConfirm` 공용 |
| `themeconfirm` | 맵 테마 | 640×300 | 테마 카드 클릭 | "맵 테마를 변경하시겠습니까? → 이름" + [예](`RequestSetTheme` → `profile`) / [아니오](→ `profile`) — `BuildConfirm` 공용 |
| `iconinfo` | 아이콘 | 640×370 | 아이콘 칸 클릭 · 확인에서 [아니오] | 초상 140(몬스터 썸네일, 미보유는 실루엣) + 이름 + 상태(사용 중 / 보유 · 획득일 / 미획득) + 획득처(`WhereText`: 매우어려움 · n라운드 · 지역 - 맵) + 확률 + [이 아이콘 사용](보유·미사용) · [목록으로](→ `profile` [아이콘] 탭) |
| `iconconfirm` | 아이콘 | 640×280 | [이 아이콘 사용] · '없음' 칸 | "아이콘을 변경하시겠습니까? → 이름"(없음이면 "아이콘을 없음으로 변경하시겠습니까?") + [예](`RequestSetIcon` → `profile` [아이콘] 탭) / [아니오](→ `iconinfo`, 없음이면 `profile` [아이콘] 탭) |
| `iconget` | 새 아이콘 획득! | 640×430 | 서버 `ShowIconGot` → `RtsProfileLogic.FlushGot`(보스 3택1·다른 획득 팝업이 떠 있으면 닫힌 뒤) | 획득음(PickSound) + 초상 140(몬스터 썸네일) + "이름 아이콘을 얻었어요!" + 획득처 · 획득일 + [확인] |

### 4.3 유닛 정보 팝업 (`unit`, RtsUnitPopupLogic, 1229×720 — :11-13)
- **2026-09-24**: 능력치 박스 아래 `RtsUnitAugGain`(27, −256−능력치 높이−8) 365×88 — '증강으로 오른 수치 (n개)' + 2열 격자(공격력·공격력%·보스 데미지·크리티컬 확률/데미지·최종 데미지, `TotalsMul` × `AugMulFor`). 증강 탭 행은 설명 줄 수만큼 높아지고(44 + 줄 × 20, 최대 6줄), 설명의 머리표([직업 전용] [프리즘])는 뗀다. 탭 전환·다시 그리기는 옛 `Content`를 0.12초 남겼다가 지운다.
| 영역 | 엔티티 | 줄 | 위치·크기 (본문 기준) | 비고 |
|---|---|---|---|---|
| 외형 패널 | `RtsUnitLook` | 232 | a(0,1) (27,-10) 365×236 | Mix(white,0.03) / Mix(Gold,0.25). "외형" 13 |
| 미리보기 | `RtsUnitPreview` (uiempty + CostumeManager + AvatarGUIRenderer) | 835-871 | p(0.5,0.5) (92,-128) 120×190 | 모델이 없으면 직업명 글자로 대신 |
| 외형(기본 세트) | `RtsUnitLookGlow` · `RtsUnitPreview` · `RtsUnitLookPlate`/`Name` | `BuildBody` | 원광 a(0,1) p(0.5,0.5) (181,−98) 176×176 · 아바타 (181,−90) 112×140(원 안 — '외형' 제목 줄 없음) · 이름판 a(0.5,0) (0,12) 220×30 | 원광 금색 α0.13(원형 마스크) · 이름판 Mix(Gold,0.14)/Mix(Gold,0.55) · ColInk 15 굵게 | 항상 | 2026-09-25 월드 아바타 스킨 버튼 2개 삭제 → 기본 세트를 가운데 크게(사용자 "기본 스킨이나 이쁘게 꾸며서"). 이름 = "모험가 ○○"(프리즘 직업명) / "영웅 팬텀" |
| 능력치 패널 | `RtsUnitStats` | 289 | (27,-256) 365×290 | 8줄, 줄 간격 30. 키 14 ColMuted, 값 15 ColInk 리치(버프가 반영된 줄은 `#9fd39a ▲`) |
| 탭 | `RtsUnitTab{skill,aug,buff}` + 키캡 `RtsUnitTabKey`("Tab") | 310-334 | x 411부터 폭 120/130/190, 간격 8, 높이 34, 글자 15 | 탭 상태는 팝업을 닫아도 유지된다. Tab 키로 순환(`CycleTab` :808) |
| 목록 | `RtsUnitSkillList` / `RtsUnitAugList` / `RtsUnitBuffList` | 615-636 | 스트레치 x 411~1202(폭 791), y는 −54에서 아래 66px 전까지 | ScrollLayoutGroup 세로, 간격 6. 넘칠 때만 스크롤. 스크롤바 8px, 손잡이 Gold |
| 스킬 행 | `RtsUnitSkill{i}` | 502 | 높이 64 + 20×(줄 수−1) (+36 대상 지정 행) | 왼쪽 4px 띠(액티브 Gold, 패시브 (0.541,0.498,0.439), 미획득 흐림). Lv 12/17, 이름 17 굵게 리치, 설명 14 |
| 잠금 토글 | `RtsUnitLock{idx}_{0,1,2}` | 571-610 | 행 오른쪽 위, 폭 56/100/56 × 28 | 사용 (0.624,0.827,0.604) · 보스전 잠금 (0.91,0.635,0.416) · 잠금 (0.86,0.47,0.44). 영구 잠금이면 프리즘색 알약 120×28 |
| 대상 지정 | `RtsUnitTgtSel` + 드롭다운 `RtsUnitTgtList` | 429-459, 749-791 | (118,-62) 250×30 / 목록 250×(30n+4) | 재지정 쿨 3분. 남은 시간 (0.91,0.635,0.416), 가능하면 (0.624,0.827,0.604) |
| 프리즘 행 | `RtsUnitPrism{i}` | 551 | 스킬 행과 같음 | Mix(prism,0.08)/Mix(prism,0.45) |
| 증강 합계 | `RtsUnitAugSum` | `BuildAugTabFor` | 목록 맨 위 (rw−12)×88, 셋째 줄이 없으면 ×62 | Mix(Gold,0.08)/Mix(Gold,0.4). "증강 n개 합계"(Gold 14) / 합계(Ink 15) / 방어구 부수기 수치(Muted 13 — 켜졌을 때만). **티어·서포터 같은 분류는 화면에 쓰지 않는다**(2026-09-24 사용자) |
| 증강·버프 행 | `RtsUnitAug{i}` / `RtsUnitBuff{i}` | 697 / 723 | (rw−12)×64 | 버프 아이콘 40×40, 효과 글자 (0.624,0.827,0.604) |
| 레벨업 | `RtsUnitLvUp` + 키캡 `RtsUnitLvKey`("Space") | 348-360 | a(1,0) p(1,0) (-27,10) 280×44 / (−317,20) 70×26 | 가능: Mix(Gold,0.92)/Gold, 글자 (0.133,0.114,0.09). 불가: 한 번 더 섞어 흐리게(`ApplyLevelButton` :175) |

갱신 방식: 서버 값이 동기화되면 `OnUnitSynced`(:101)가 0.05초 동안 들어온 것을 모아 `UpdateInPlace`(:115)를 한 번 부른다. 구조 서명(`Signature` :137 — 직업·프리즘·잠금·스킨·대상·탭·획득 스킬 수·버프·증강 수·해금·쿨)이 같으면 제목·능력치 값·레벨업 버튼만 바꾼다. 다르면 `Render`(:211)가 통째로 다시 그린다. 통째로 다시 그리면 깜빡이므로 새 시각 요소는 가능하면 제자리 갱신 경로에 넣는다. 1초 타이머(`Tick` :822)는 대상 지정 쿨 글자를 갱신한다.

### 4.4 나머지 팝업 세부
**영입 (`BuildRecruit` :310-402)**
- 탭: `RtsRcCat{adv,hero}` (27,-10)에서 시작, 폭 100·90, 높이 36, 간격 10, 글자 17. 영웅 탭에는 팬텀만 있다.
- 열: 폭 200, 간격 14, x = 27 + 214·(열−1). 제목 `RtsRcGroup{i}`(y −66, 200×26, Gold 18 굵게)와 선 `RtsRcGroupLine{i}`(y −96)이 있다.
- 직업 카드 `RtsRcJob{g}_{j}`: y = −108 − 48·(j−1), 200×40. 배경 Mix(white,0.04), 테두리 Mix(white,0.08). 이름 17, 오른쪽 라벨 14 ColMuted("Lv 1"/"보유 중"/"잠김"). 누를 수 없는 카드는 글자 (0.55,0.51,0.45), 배경 Mix(white,0.02).
- 카드를 누르면 팝업을 닫고 배치 모드(`BeginPlace`)로 들어간다. 이때 빈 발판이 금색 틀로 강조되고, 발판을 클릭하면 서버 `RequestRecruitAt`로 간다.
- 하단 `RtsRcFoot`: a(1,0) (-27,22) 700×26, 글자 (0.851,0.796,0.651) 15, 오른쪽 정렬.

**증강 (`BuildAugment` :600-827)**
- 등급 탭 `RtsAugTab{g}`: (27+118·(i−1), -10) 110×34, 글자 16. 탭 글자는 "전체/브론즈/실버/골드/프리즘 n".
- 왼쪽 목록 `RtsAugList`: 스트레치 (27,27)~(594,−60), 배경 Mix(white,0.02). 행이 12개를 넘으면 스크롤. 행 `RtsAugRow{i}`는 551×56이고 미지정 행을 항상 위로 올린다.
  - 미지정 행: 배경 Mix(red,0.1), 테두리 (0.85,0.36,0.32), 오른쪽 알약 `RtsAugRowNew` "미지정" 86×30 (0.78,0.25,0.22)/(1,0.62,0.55).
  - 선택된 행: Mix(Gold,0.14)/Gold.
- 오른쪽 상세 `RtsAugDetail`: (617,−60) 470×803. 배지, 이름 23, 효과 15, "적용 유닛" 13. 미지정이면 붉은 안내 14와 유닛 칩 `RtsAugChip{i}`(2열 211×36, 간격 10·42)가 나온다. 지정 버튼 `RtsAugAssign`은 a(0,0) (19,19) 432×46이고, 켜짐이면 Mix(Gold,0.9)에 "<직업>에게 지정" + Space 키캡이 붙는다.
- 오른쪽 아래 체크 `RtsAugHideBox`: a(1,0) (-27,4) 190×24, 네모 20×20, 표시 10×10 Gold, "적용된 증강 숨기기" 14. 하단 요약 `RtsAugFoot`: (−227,4) 620×22.
- 보유 목록이 동기화되면(`RtsAugmentLogic.OnSyncProperty` :465-471) 다시 그린다.

**증강 도감 (`BuildCodex` :877-971)**
- 탭 `RtsCodexTab{g}`: (27+128·(i−1), -10) 120×34. 안내 `RtsCodexInfo`: (27,−52), 14 ColMuted.
- 목록 `RtsCodexList`: 스트레치 (27,27)~(−27,−86), 항상 스크롤. 행은 830×56이고, 오른쪽 위 확률 "%.1f%"(15 굵게 ColMuted)가 있다.
- 브론즈·실버·골드: 이름 (90,0) 300×30 16, 효과 (400,0) 300×30 15.
- 프리즘: 직업 칩 `RtsCodexJob` 140×30(Mix(prism,0.16)/Mix(prism,0.55), 글자 (0.9,0.82,1) 14), 이름 17, "자세히 ▾"가 있다. 행을 누르면 높이가 56 ↔ 132로 바뀌며 설명이 펼쳐진다(다시 그리지 않고 그 자리에서).

**3택1 (`BuildPick` :1062-1121)**
- 안내 줄 `RtsPickSub`: (27,-4) 1060×24, 15 ColMuted.
- 카드 `RtsPickCard{i}`: x = 27 + 359·(i−1), y −40, 340×360, 두께 2.5. 배경 Mix(white,0.04), 테두리 Mix(등급,0.5). 위쪽 6px 등급 띠, 배지, 이름 21 굵게, 효과 15(302×200).
- 뒤쪽 빛 `RtsPickGlow{i}`: 카드보다 사방 7px 크다. 등급색 알파가 0.18~0.68로 숨쉬듯 바뀐다. 카드마다 반짝이 십자 별 5개(`RtsPickStarH/V`)가 붙고 0.04초 타이머로 움직인다(`StartPickFx` :1011).
- 받기 `RtsPickTake`: a(0.5,0) (0,19) 302×44, Mix(Gold,0.9)/Gold, "받기" 18 (0.133,0.114,0.09). 누르면 닫고 `ChooseFromPopup(idx)`.
- 접기 `RtsPickFold`: a(0.5,0) (0,16) 220×44, Mix(white,0.06)/Mix(white,0.3), "접기 (나중에 선택)" 16. 누르면 닫히고 HUD '펼치기'가 나타난다.

**결과 (`BuildResult` :408-483)**
- 머리글 `RtsRsHead`: (27,-4) 586×40, 28 굵게. "클리어!"는 Gold, "탈락 — 필드 110"·"탈락 — 보스 시간 초과"는 (0.95,0.45,0.4).
- 줄: 도달 `RtsRsReach`(y −54, 19), 처치 `RtsRsKills`(−88, 19, 보스 탈락이면 보스 HP%), 개인 최고 `RtsRsBest`(−122, 17 ColMuted).
- (2026-09-25) 클리어 순위 두 줄(`RtsRsFinal`·`RtsRsRank`)은 뺐다 — 사용자 "인게임 순위표 제거". 클리어 기록 저장(`RtsRunResultLogic.SaveClear`)은 그대로 하고, 순위는 대기방 순위표(Phase 13)에서 보인다. 결과 창 높이는 클리어·탈락 모두 360.
- 버튼(y −186), 둘 다 180×44: `RtsRsClose`(SpawnTab, 가운데 왼쪽)는 닫기만 한다 — 솔로 "닫기" / 여럿 "관전하기". `RtsRsExit`(가운데 오른쪽)는 솔로면 "다시 하기"(금색 — `RtsStageLogic.RequestRestartVote`, 혼자 찬성 = 바로 새 판), 여럿이면 "나가기"(위험색 — `RequestExit`). 솔로 판정 = `RtsStageLogic:IsSolo()`(방 인원 1).

**방출 확인 (`BuildDismiss` :554-595)**
- 대상 줄 `RtsDmWho`: (27,-6) 15 ColMuted "Lv.n 직업 · 환급 n 메소". 경고 `RtsDmMsg`: (27,-44) 586×90, 19 굵게 가운데, 두 줄.
- 버튼(y −150, 180×44): `RtsDmYes` "방출"(위험색, 가운데 왼쪽) → `RequestDismiss`. `RtsDmNo` "취소"(탭 모양, 가운데 오른쪽).

---

## 5. 월드 공간 UI

아래는 UI 그룹이 아니라 **맵(`/maps/RtsMap`)이나 유닛·몬스터 엔티티 자식으로 스폰되는 월드 스프라이트**다. 크기는 월드 유닛 단위다. 카메라 줌 30%에서 1유닛은 약 45px이다(docs/msw-engine.md:19).
| 요소 | 엔티티 이름 | 종류 | 만드는 곳 | 크기·층 | 비고 |
|---|---|---|---|---|---|
| 발 아래 버프 아이콘 | `RtsBuffIcon{gen}_{i}` (유닛 자식) | 월드 스프라이트 (`model://MapObject`) | RtsUnitBuffLogic:166-202 | 세계 스케일 2.2(유닛 스케일이 2라서 로컬 1.1), 간격 0.75, 발 아래 −0.52. MapLayer0 / order 210 | 아이콘 RUID는 `GetDefs`(:29-38). 동기화가 오면 0.2초 모아서 다시 그린다(`MarkDirty` :136). **이름 앞 11글자 `RtsBuffIcon`으로 지울 대상을 찾는다(:173)** |
| 몬스터 체력바 | `RtsHpBack` / `RtsHpFill` (몬스터 자식) | 월드 스프라이트 (흰 사각 `WhiteRUID`를 Scale로 늘림) | RtsMonsterComponent:232-307 | 일반 1.4×0.12, 보스 폭 = `BossBarFit`(슬롯 폭 − 0.12 — 2026-09-25 3×3칸 상자라 1체 약 5.2, 2체 약 2.5) × 0.24, `BossBarFit`이 0이면 `BossBarW` 7.8. 높이는 표의 `barY×SizeMul`, 없으면 1.15(보스 3.4). 테두리 +0.04. 몬스터 order +5/+6 | 배경 (0.1,0.1,0.1,0.9), 채움 (0.92,0.18,0.18,1). 보스 폭은 2026-09-23에 2.6에서 7.8로 바뀌었다(:62) |
| 빙결 결정체 | `RtsFrozenFx` | 월드 스프라이트 클립 | RtsMonsterComponent:313-352 | 체력바 바로 위, order +8 | — |
| 데미지 숫자 | (엔진) `DamageSkinSpawnerComponent` 몬스터 / `DamageSkinSettingComponent` 유닛 | **엔진 컴포넌트** | RtsWaveLogic:89-90, RtsBossLogic:105, RtsUnitLogic:259-264 | 스킨 `7e39645a…`, 배율 2.0(RtsCombatLogic:47/49), 트윈 Blade. 시작 높이 = barY + 0.2 | 스크립트로 그리지 않는다 |
| 타격 연출 | `RtsHitFx_*` | 월드 스프라이트 클립 | RtsMonsterComponent:549-566 | Default / order 320 | 마지막 프레임에서 제거 |
| 레벨업 연출 | (EffectService) | 엔진 이펙트 | RtsUnitLogic:666 | Default / order 305 | 클릭하는 순간 클라에서 바로 재생 |
| 발판 강조 틀 | `RtsPadFrame{gen}_{i}` (`/maps/RtsMap` 자식) | 월드 스프라이트 | RtsUnitSelectLogic:387-399 | `MarkerRUID` `2c03a06f…`, 스케일 2.12, MapLayer0 / order 150 | 빈 칸 금색 (1,0.82,0.25), 내 유닛 자리 파랑 (0.4,0.62,1)(맞교환). 위치 이동·영입 배치 모드에서만 |
| 보스 영역 | `ZoneBossArea{n}` | 월드 스프라이트 (서버 생성) | RtsZoneLogic `SpawnBossArea` | **8~9열 × 6~7행(2×2칸, 2026-09-25 맵 가운데 — 13줄이라 반 칸 위)**, order 105 | 반투명 붉은색 (0.85,0.16,0.12,0.28). 보스전이 아닐 때도 늘 보이고, 이 칸에는 배치할 수 없다. 둘레 한 겹은 발판 |
| 보스 몸 | `Boss{zone}_{n}` | 월드 스프라이트 (서버 생성, `RtsWaveLogic.SpawnMonsterEntity`) | RtsBossLogic `SpawnBoss` | 보스 영역 가운데 **3×3칸 상자**(`BossFitCells`)를 꽉 채우는 크기, 2체면 가로 반씩. MapLayer0 / order `BossOrder` 150(부위·체력바는 이 값 +) — 유닛(200)보다 **아래** | 2026-09-25 사용자 "3x3 정도로 조금 넘치게, 보스보다 유닛이 위로·클릭도 유닛 우선"(클릭은 `RtsUnitSelectLogic` 유닛 상자 → 넓힌 유닛 상자 → 몬스터 순) |
| 비석 | `RtsTomb{zone}` | 월드 스프라이트 (서버 생성) | RtsRunResultLogic `SpawnTomb` | 그 구역 주인의 비석 프리셋(`RtsTombLogic` — 기본 `29e864c6…`, 스케일 5), order 210 | 탈락한 구역 가운데. 주인이 없으면 기본 비석 (2026-09-25 비석 프리셋) |
| 그리드·장식 | `ZoneGrid{n}` / `ZoneDecor{n}_{i}` | 월드 스프라이트 (서버 생성) | RtsZoneLogic `SetZoneGrid` / `SetZoneDecor` | order 100 / 110 | 구역마다 그 구역 주인의 테마 프리셋(`RtsThemeLogic.ApplyToZone`)이 트랙 판 텍스처·틴트·장식을 정한다. 트랙 판 = 테마별 1장(헤네시스 `ZoneTrackGridM2` · 엘리니아/페리온/커닝/리스 `ZoneTrackGrid<테마>` — 2026-09-25 M2 경로 77칸·매듭 3곳, S = 초록 원 + 진행 방향 화살표, E = 빨강 원 + 되돌리기 화살, E→S 복귀 점선 없음. 경로·칸·S/E는 같고 길 재료·연석·발판 선색만 다름 — `tools/gen-track-grid.js <out> <key>`). 장식은 `flip`이면 좌우 뒤집기 |
| 마우스 커서 | (InputService) | 엔진 커서 | RtsUnitSelectLogic:100-113 | 기본 `3930c5d2…`, 누르는 동안 `5df970b4…` | 0.03초마다 버튼 상태를 확인 |

월드와 UI의 경계에 있는 것: 캐릭터 메뉴(N)와 몬스터 정보(M)는 **UI**(HudGroup 자식)다. 몬스터 초상은 UI 스프라이트에 몬스터 썸네일(2026-09-25 — 없으면 걷기 클립)을 넣은 것이다. 유닛 외형 미리보기는 UI 아바타(AvatarGUIRenderer)다.

월드 클릭 판정은 엔티티 Touch가 아니라 `ScreenTouchEvent`와 자체 상자로 한다. 유닛 상자는 폭 1.4 × 높이 2.2(발 기준)이고, 못 찾으면 가로 ±0.35·세로 ±0.3을 넓혀 한 번 더 찾는다(RtsUnitSelectLogic:47-49, :475-477). `IsPointerOverUI()`가 참이면 월드 클릭은 무시된다(:462). 그래서 HUD를 월드 위로 넓히면 그만큼 클릭할 수 있는 월드 영역이 줄어든다.

---

## 6. 상태별 화면 변화

`RtsStageLogic.RunState`(@Sync)는 `idle` → `countdown`(15초, RtsStageLogic:21) → `running` → `ended` 순으로 바뀐다. HUD는 `RtsStageLogic.RefreshHud`가 0.25초마다(:90, :434-475), 증강 쪽은 `RtsAugmentLogic.ClientTick`이 0.3초마다, 난이도 막대는 `RtsDifficultyLogic.ClientTick`이 0.3초마다 갱신한다.

| 요소 | idle | countdown | running | ended |
|---|---|---|---|---|
| 정보 카드 윗줄 | 대기 중 | 시작까지 + 초 | n라운드 / 보스 / 쉬는 시간 / 보스 준비 | 게임 종료 |
| 난이도 막대(F) | 보임 | 보임 + '바로 시작' | 숨김 | 숨김 (:136) |
| 카드 '난이도 X' | 보임 | 보임 | 보임 | 보임 |
| 다시 하기(D) | 흐림(idle 모드), 눌러도 무시 | 〃 | 여럿이면 3초 확인, 방에 혼자(솔로)면 바로 새 판 | 누르면 바로 찬성(혼자면 바로 새 판) |
| 투표 패널(E) | 표가 있을 때만 | 〃 | 〃 | 〃 |
| 영입 버튼(R) | 숨김 | 숨김 | 빈 칸이 있을 때만 "영입 가능 n" | 솔로 "다시 하기"(금색) / 여럿 "나가기" |
| 영입 팝업 자동 열기 | — | — | 첫 틱에 한 번(살아 있을 때) | — |
| 증강 뽑기(Y) | 흐림 | 가능하면 금색 | 가능하면 금색 | 흐림 |
| 3택1 팝업 | — | 선택지가 오면 자동 | 선택지가 오면 자동(접어 두면 '펼치기') | — |
| 안내(H) | — | — | 보스 준비 초읽기(1.2초씩) | 끝난 순간 한 번 "게임 종료 — …"(6초) |
| 슬롯·증강·도감·목록 | 항상 | 항상 | 항상 | 항상 |

**탈락·클리어한 나** (`RtsRunResultLogic.StateByUser` 1·2, `IsMeAlive()` = false)
- 결과 팝업이 자동으로 뜬다(본인에게만).
- 영입 버튼 자리가 솔로면 "다시 하기"(금색, 누르면 바로 새 판), 여럿이면 "나가기"(위험색)로 바뀐다(`RtsHudLogic.RefreshRecruitButton` exitMode).
- 뽑기는 클라에서 막히고(RtsAugmentLogic:374), 영입 카드는 누를 수 없다.
- 플레이어 목록에서 내 행이 비석과 회색으로 바뀐다. 구역 가운데에는 비석 월드 스프라이트가 선다.
- 탈락이면 배경음이 꺼진다. 살아 있는 구역을 관전 중이면 그 곡이 나온다(RtsStageLogic:487-496).
- 난이도 막대는 idle·countdown에만 보이므로 관전 중에는 나오지 않는다.

**관전(다른 구역 보기)** — F1~F8(RtsCameraAnchorComponent:132-136) 또는 플레이어 행 클릭
- `JumpToZone` → `SetWatchedZone`이 불리고, 보고 있는 행의 테두리가 금색이 된다.
- 몬스터 정보는 **보고 있는 구역**의 몬스터를 잡는다.
- 유닛 클릭 판정은 **내 구역 유닛만** 본다(RtsUnitSelectLogic:67). 그래서 남의 유닛은 눌러도 반응이 없다. 우측 슬롯도 계속 내 유닛을 보여 준다. 결과적으로 관전은 읽기 전용이다. 조작 RPC는 서버가 `senderUserId`로 다시 검증한다.
- 로드맵은 "관전 중 상세보기"를 말하지만(roadmap:55), 지금 코드에는 남의 유닛 상세를 여는 경로가 없다.

**보스전**
- 보스 준비(`BossPrep`, 5초): 카드가 "보스 준비"로 바뀌고 안내에 "○○ 등장까지 n초"가 뜬다.
- 보스 라운드: 카드가 "보스"로 바뀐다. 보스는 맵 가운데 붉은 보스 영역(2×2칸)에 바로 나타나 고정으로 서고(그림은 3×3칸 크기로 둘레 발판에 조금 걸침), 긴 체력바가 붙는다. 겹치는 자리의 유닛이 보스 위에 보이고 클릭도 유닛이 먼저다. 몬스터 정보에 "보스" 딱지와 방어율이 보인다.
- 60초 안에 못 잡으면 결과가 "탈락 — 보스 시간 초과"가 된다. 보스를 잡은 뒤 프리즘 3택1이 오면 제목이 "보스 처치 — 프리즘 증강 선택"이다.

**모드 (클라 전용)**
- 위치 이동 모드와 영입 배치 모드에서는 발판 틀이 켜지고 안내가 계속 떠 있다. ESC로 취소한다.
- 팝업을 열면 배치 모드가 끝난다. 유닛 팝업을 열면 이동 모드·배치 모드·메뉴가 모두 끝난다(RtsUnitPopupLogic:59-61).

---

## 7. 디자인 작업 규칙 (ChatGPT용)

### 7.1 바꿔도 되는 것
- 색 토큰 메서드의 반환값(`ColInk`…`ColBorderSoft`, `SeriesColor`, `GradeColor`, `Base`/`Mix`)과 각 `Spawn*` 호출에 직접 적힌 Color 값. 톤을 통째로 바꾸려면 1.4의 "직접 적힌 색"도 함께 바꾼다.
- 위치·크기·anchor·pivot·간격·테두리 두께·글꼴 크기·정렬·굵게, 그리고 사용자에게 보이는 문구.
- UI 아트 RUID(`WhiteRUID` 자리에 프레임 스프라이트 넣기, `CoinRUID`, 디버프 아이콘 RUID 등). RUID를 넣은 **뒤에** 크기·위치를 준다(RtsMonsterInfoLogic:123).
- 새 장식 요소 추가. 이때도 새 버튼은 `SpawnClick`으로 만들고, 이름은 `Rts` 접두의 PascalCase로 짓는다.

### 7.2 바꾸면 안 되는 것
- **`@ExecSpace("Server")`·`ServerOnly` 메서드의 내용.** 재화, 영입, 증강, 투표, 난이도 선택, 기록은 서버 권한이다.
- **RPC 서명.** Maker 빌드 분석기는 메서드 서명(인자 수)을 캐시한다. 기존 메서드에 인자를 늘리면 옛 서명으로 오류가 나고 refresh로도 안 지워진다. 인자가 다르면 **새 이름의 메서드를 추가**하고 옛 것은 새 것을 부르게 둔다(.beaver/memory/msw-engine.md:162-165). UI가 부르는 서버 RPC는 아래와 같다.
  - `RtsStageLogic`: `RequestVoteChoice(number)` :213, `RequestRestartVote()` :196, `RequestStartNow()` :152
  - `RtsDifficultyLogic`: `RequestSet(number)` :93
  - `RtsUnitLogic`: `RequestRecruitAt(string,number,number)` :366, `RequestMove(number,number,number)` :736, `RequestDismiss(number)` :433, `RequestLevelUp(number)` :607, `RequestBond(number,number)` :671, `RequestSkillLock(number,number,number)` :689, `RequestSkin(number,number)` :721, 개발용 `RequestDevPrism(string)` :472 · `RequestDevClear()` :462
  - `RtsAugmentLogic`: `RequestChoose(number)` :236, `RequestAssign(number,number)` :257, `RequestBuy()` :327
  - `RtsRunResultLogic`: `RequestExit()` :328
  - 서버→클라 RPC(`@ExecSpace("Client")`, 마지막 인자 userId = 그 한 명에게): `RtsHudLogic.RefreshPlayerList(string)` :813, `RtsUnitLogic.OnChanged(number,number,string)` :168, `RtsRunResultLogic.ShowResult(…9개)` :321 · `ShowClearScore(…7개)` :293 · `PlayTombSound(number)` :313 · `NotifyNoMatching(string)` :339, `RtsCameraAnchorComponent.ApplyAssignedZone(number,string)` :112
- **@Sync 프로퍼티 이름.** UI가 읽는 것들이다: `RunState`, `StageNo`, `StageEndsAt`, `BossPrep`, `ReadyCount`, `RoomCount`, `VoteCount`, `VoteNeed`, `VoteNoCount`, `VoteStartedAt`, `RestartVotes`, `DiffByUser`, `StateByUser`, 몬스터 `Hp/MaxHp/IsBoss/Defense/StageNo/SizeMul/BossBarFit`.
- **이름·경로로 찾는 엔티티.** 이름을 바꾸면 조회가 깨진다.
  - `/ui`(RtsHudLogic:284)
  - `/maps/RtsMap` 및 그 아래 `Unit{zone}_{no}`(RtsUnitLogic:47, :66-71 접두 `Unit{zone}_`, RtsUnitBuffLogic:62), `ZoneGrid{n}`·`ZoneDecor{n}_{i}`(RtsZoneLogic:273/318/344), `RectTileMap`(RtsBootstrapLogic:64/81), 몬스터 이름(RtsCombatLogic:722/733, RtsUnitAttackComponent:40)
  - 유닛 자식 `Shadow`(`GetChildByName`, RtsUnitLogic:295, RtsUnitComponent:111, RtsSkillFxLogic:1113)
  - 버프 아이콘 접두 `RtsBuffIcon`(앞 11글자 비교, RtsUnitBuffLogic:173)
  - HUD·팝업 UI 엔티티는 이름으로 찾지 않고 프로퍼티 참조로 들고 있어서 이름을 바꿔도 동작한다. 다만 `RtsPadFrame{gen}_…`·`RtsBuffIcon{gen}_…`의 세대 번호는 이름 충돌을 막으려고 붙인 것이므로 지우지 않는다.
- **`SpawnPanel`의 반환 약속(안쪽을 돌려주고 바깥은 `.Parent`).** `RecruitBtn.Parent`, `AugBtn.Parent`, `vp.Parent:SetEnable`, `self.Hint = hint.Parent`, 난이도 카드 글자가 `StageSubText.Parent`를 카드로 쓰는 것(RtsDifficultyLogic:189) 등이 이 약속에 기대고 있다.
- 값을 비교해 필요할 때만 다시 그리는 캐시 키(`StageShown`, `RecruitShown`, `RestartShown`, `VoteShown`, `BuyShown`, `ExpandShown`, `AugShown`, `Shown`, 유닛 팝업 `Sig`). 새 시각 상태를 추가하면 그 상태도 키에 넣어야 화면이 바뀐다.
- `Environment/NativeScripts/**/*.d.mlua`는 엔진이 만든 파일이라 읽기 전용이다. 맵·설정 JSON(`*.map`, `*.config`)은 Maker 도구로만 다룬다.
- 단축키: ESC(닫기·취소), Tab(유닛 팝업 탭), Space(레벨업·증강 지정), L/S(메뉴), F1~F8(구역). 처리하는 곳은 RtsPopupLogic:238, RtsUnitSelectLogic:503, RtsCameraAnchorComponent:132다.
- 팝업에 내부 설계 수치(누적 투자, 벽, 예산)를 보이지 않는다(로드맵 규칙).

### 7.3 작업 요령
- **바뀐 칸만 다시 그린다 — 창 전체를 다시 열지 않는다**(2026-09-25 사용자 "화면 내용 바뀔 때마다 필요한 부분만 재랜더링하고 나머지 부분 좀 그만 건드려"): 탭 전환·선택·서버 값 갱신으로 일부가 바뀌면 `Open(같은 kind)`를 부르지 말고
  - 탭 줄 = `RtsPopupLogic.SpawnTabBar`(누르면 제자리에서 켜짐만 — `BarSelect`·`SetTabOn`, 글자는 `SetTabText`, Tab 키 순환 `BarNext`)
  - 바뀌는 목록·상세 = 투명 컨테이너(`SpawnBox`)째 새로 만들고 옛 것은 `DropLater`(0.12초 뒤 지움)
  - 선택 표시(행 색·체크 칸·아이콘 칸 색)는 참조를 들고 있다가 제자리에서 색만(`RestyleAugRows`·`RefreshPresetMarks`·`RefreshIconCells`)
  - 예: 증강 창(`RefreshAugment` = 목록·상세·아래 줄, 행 클릭 = 행 색 + `RefreshAugDetail`), 도감(`RefreshCodex`), 영입 목록(`RefreshRecruit`), 영입 상세(`BuildRiSkills`), 프로필(`RefreshProfileContent`), 유닛 상세(`RenderRight` — 외형은 직업·프리즘 이름이 바뀔 때만 `Render`)
- UI 아바타(`AvatarGUIRendererComponent`, `RtsUnitPopupLogic.SpawnPreviewAt`)는 칸 **아래쪽에** 서서 칸이 크면 위가 빈다 — 칸을 캐릭터 크기에 맞게 낮게, 두손검·창은 캐릭터 왼쪽으로 길게 나오니 칸 안쪽으로(2026-09-25 실측)
- 화면 문구에 개발용 분류(티어·서포터·1티어 등)를 쓰지 않는다(메모리 workflow) — 증강 효율은 오각형 모양으로만
- **다시 그리기는 번쩍이지 않게**(2026-09-24): 같은 팝업을 다시 그릴 때(`RtsPopupLogic.Open`이 같은 kind로 불릴 때) 팝업 그룹은 끄지 않고 옛 body를 0.12초 남겼다가 지운다(`OldBody`/`KeepOldBody`). 유닛 창 `Render`도 옛 `Content`를 0.12초 뒤에 지운다. 엔진이 UI를 여러 프레임에 나눠 만들기 때문에, 지우자마자 새로 만들면 빈 창이 한순간 보인다 — 새 화면 코드도 같은 방식을 쓴다.
- 자기 효과음이 따로 있는 버튼은 `SpawnClickQuiet`(클릭음 없음)로 만든다(예: HUD '펼치기' — 3택1 등장음과 겹쳤다).
- UI 코드만 고치는 작업은 `@ExecSpace("ClientOnly")`(또는 `Client`) 메서드 안에서 끝낸다. 대상은 `Build*`, `Apply*`, `Refresh*`, `Set*`, `Spawn*` 계열이다. 새 스크립트가 필요하면 PascalCase에 `Logic`/`Component` 접미사를 붙이고 모든 메서드에 `@ExecSpace`를 적는다(CLAUDE.md).
- mlua API가 불확실하면 추측하지 말고 msw-mcp `mlua_api_retriever`로 확인한다. 런타임 이름이 선언 파일과 다른 경우가 있다. 예: 스크롤바는 `ScrollBar*`(RtsUnitPopupLogic:629). `AutoHide`/`Hide`는 쓰지 않는다(:613).
- 엔진 동작 실측(텍스트 Truncate, 업로드 스프라이트 PPU, UI 좌표 변환, 입력)은 `docs/msw-engine.md`에 있다.
- 목업 `.info/artifacts/hud-layout.html`(v16)과 플레이어 카드 스케치 `.info/artifacts/player-slot-sketch-260922.png`는 **로컬 전용**(.gitignore)이라 다른 기기에는 없을 수 있다. 목업이 실제와 다르면 **이 문서와 코드가 기준**이다.
- 검증 순서(CLAUDE.md Testing): `maker_stop` → **`maker_refresh_workspace`** → `maker_save` → `maker_play` → `maker_logs(kind:"build")`로 문법 확인 → `maker_logs(kind:"normal")`로 런타임 확인 → `maker_screenshot` → `maker_stop`. refresh를 빼먹으면 옛 스크립트로 돈다. 문법 오류는 `[LEA-3016] InvalidFormat …`으로 normal 로그에 찍힐 수 있다(.beaver/memory/msw-engine.md:163).
- UI를 바꾸면 이 문서의 해당 표도 같이 고친다(.beaver/memory/balance.md:313).

### 7.4 알려진 어긋남 (손대기 전에 확인)
- 안내 문구 "영입 버튼 옆 '다시 하기'"(RtsStageLogic:472, RtsRunResultLogic:340)는 현재 배치와 맞지 않는다. 영입 버튼은 오른쪽 슬롯 아래에 있고 다시 하기는 위쪽 가운데 오른편에 있다. 주석 RtsHudLogic:4·:699·:710과 RtsDifficultyLogic:14·:150의 "상단 가운데 영입 버튼"도 옛 배치 기준이다.
- 안내(H)와 난이도 막대(F)가 같은 자리를 쓴다(2장).
- `RtsHudLogic.SetPlayerAlive`(:927)는 부르는 곳이 없다. 목록은 매번 서버 통지로 전부 다시 만든다.
- `@ExecSpace` 표기가 어긋난 곳이 있다. RtsUnitPopupLogic:412의 표기는 주석 너머 `DescLines`에 붙어 있어서 `BuildTargetRow`(:429)에는 표기가 없다. RtsPopupLogic:975-977에는 같은 표기가 두 번 있다. 동작에는 문제가 없지만 옮길 때 주의한다.

---

## 8. 아직 없는 / 예정 UI (로드맵 `.beaver/output/roadmap/maple-augment-defense-roadmap.md`)

개발 순서(2026-09-25 사용자 — 출시 노트 순서에서 바꿈): ① 개인 테마 프리셋(#38) + 아이콘 프리셋(#40) 동시 → ② 전체 UI 개선(#41 플레이어 카드 · #36 디자인 패스) → ③ 멀티플레이(#31 대기방·매칭·방) → ④ 순위표(#42 대기방 순위표). **게임 안 '순위' 버튼·결과 창 순위 줄은 2026-09-25에 뺐다** — 순위는 대기방에서만 보인다.

#38·#40·#41은 2026-09-25에 기능 뼈대가 들어갔다(표에 표시). 나머지는 **미구현**이다. 로드맵에 적힌 설계 메모만 옮겼고, 결정되지 않은 것은 그대로 "미정"으로 두었다.
| # | 화면 | 로드맵에 적힌 설계 | 미정 |
|---|---|---|---|
| 41 | 좌측 유저 카드 | **2026-09-25 뼈대 구현됨 — 3.2 참고**(배경 = 테마 썸네일, 원형 아이콘(`CircleMaskRUID` 69e2dced…), 닉네임, 내 카드 초록 테두리. [수정]은 2026-09-25 삭제 — 아이콘은 프로필 [아이콘] 탭) | 카드 디자인(ChatGPT) |
| 40 | 아이콘 | **2026-09-25 구현됨 — 4.2 `icon`·`iconinfo`·`iconconfirm`·`iconget` 참고**. 몬스터 247종, 기본 초록달팽이, **매우어려움에서만 처치 시 1%(보스 포함)**, 획득 일시 저장(유저 DataStorage `icons`) | 아이콘 탭 추가(지금 '기본'만) |
| 38 | 맵 테마 | **2026-09-25 뼈대 구현됨 — 3.0 테마 상자 · 4.2 `theme`·`themeconfirm` 참고**. 헤네시스·엘리니아·페리온·커닝시티·리스항구 5종 무료, 내 구역만. **2026-09-25 5종 디자인 적용됨**(바닥·테마별 트랙 판·마을 장식·400×240 썸네일 — `docs/design/260925-theme-presets.md`, Maker 검증) | 장식 추가 배치·길 점선 대비 등 다듬기 — `docs/theme-presets.md` |
| 44 | 순위 기준 교체 (**기록 저장만 동작** — 게임 안 순위 버튼·결과 창 순위 줄은 2026-09-25 제거, `rank` 창 코드는 #42에서 다시 씀) | 순위 = **어려움·매우어려움·극악에서 검은 마법사 4페이즈를 깬 횟수**. 클리어할 때마다 서버가 +1한다(테스트 모드 제외). 결과 창에 내 순위와 횟수를 보여 준다 | 세 난이도 합산 1개 표 vs 난이도별 탭 3개, 동점 2차 기준 |
| 42 | 로비 전광판 | 로비에 #44 순위 Top 10을 보이고 스크롤로 100위까지 본다. 내 순위는 하단에 고정한다. 칸 = 아이콘(#40) · 닉네임 · 클리어 횟수. 엔진 리더보드는 ReleaseOnly라 Maker에서는 로컬 SortableDataStorage 경로를 쓴다 | 시즌(무한 vs 월간 리셋) |
| 31 | 매칭·방(멀티 업데이트 — 솔로 출시 뒤) | 로비(매칭 / 방 만들기 / 혼자 시작) → 방(1~8인) 입장. 결과 창 '나가기'는 로비로 간다. 지금은 `RequestExit`가 안내 토스트만 띄운다(RtsRunResultLogic:340) | 정적 로비 + 인스턴스 방 구조, 빈자리 매칭 규칙 |
| 39 | 아바타 프리셋(후순위) | (월드 아바타 영구 이용권 전환은 2026-09-24 완료) 직업별 아바타 프리셋을 유닛 팝업 외형 영역에서 고른다 | 슬롯 수, 저장 단위 |
| 36 | HUD·화면 디자인 패스 | 프레임 톤, 색 토큰, 아이콘 아트, 레이아웃 다듬기. ChatGPT 담당이며 이 문서 7장 규칙을 따른다 | 인계 시점, 아트 자산 범위 |

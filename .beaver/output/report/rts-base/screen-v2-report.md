# Report — 화면 v2 (아티팩트 v16 → 실제 화면)

## Feature Summary
- **Feature**: 그리드 트랙(18×12·발판 81) + HUD v2(하단 제거, 시간/메소, 플레이어 목록, 영입+슬롯 6, 증강) + 팝업 공통 셸·영입/증강/3택1 껍데기
- **Entry point**: `RtsBootstrapLogic`(입장 → 그리드 시각화·배정·목록 통지) → `RtsZoneLogic`(좌표) / `RtsCameraAnchorComponent`(카메라·HUD) → `RtsHudLogic`·`RtsPopupLogic`(클라 UI)
- **Domain**: rts-base
- **기준 목업**: `.info/artifacts/hud-layout.html` v16 — Play Test 스크린샷을 픽셀 단위로 대조(그리드 좌 300·상 80·칸 80px 일치)

## Created/Modified/Deleted Files
| File | Change Type | Description |
|------|-----------|------|
| `RootDesk/MyDesk/RtsConfigLogic.mlua` | modified | 구역 42.66×24(피치 48×32 유지), 카메라 오프셋 0, 스타디움 상수 5개+게터 삭제 → 그리드 상수(18×12, 칸 16/9, 좌 −14.667, 상 +10.222, 텍스처 스케일) |
| `RootDesk/MyDesk/RtsZoneLogic.mlua` | modified | 스타디움 경로·둘레·부호거리·슬롯 10×3·경계선 삭제 → 꺾임점 17개 → 경로 67칸/트랙 65/발판 81 생성, `GetTrackPoint(t∈[0,1])`·`GetTrackLength`·`GetCellCenter`·`IsRoadCell`·`IsPadCell`·`GetPadCount`·`GetPadCell`·`GetPlacementSlot`·`CellDistance`·`GetBossPoint`, 시각화 = 구역당 그리드 텍스처 1장 |
| `RootDesk/MyDesk/RtsHudLogic.mlua` | modified(재작성) | 하단 바·미니맵·초상화·정보·스킬칸·툴팁·부대지정·Ctrl 핸들러·프레임 삭제 → 시간/메소 칩, 플레이어 목록(n/8·생존·비석·나·보는 중·클릭→구역), 영입 버튼 + 슬롯 6, 증강 버튼. API: `SetTime/SetMeso/RefreshPlayerList/SetPlayerAlive/SetWatchedZone/SetUnitSlot/ClearUnitSlot` |
| `RootDesk/MyDesk/RtsPopupLogic.mlua` + `.codeblock` | created | 팝업 공통 셸(딤·패널·제목·X·ESC) + 영입(모험가 탭·4계열 10직업·보유 0/6) / 증강(탭 5·빈 목록·상세) / 3택1(카드 3·대상 칩·대상 없이 수령, B 미리보기) |
| `RootDesk/MyDesk/RtsCameraAnchorComponent.mlua` | modified | `UpdateMinimapZone`→`SetWatchedZone`; **줌 잠금 해제 후 ZoomTo → 0.2초 뒤 잠금**(잠긴 채로는 ZoomTo가 무시됨) |
| `RootDesk/MyDesk/RtsBootstrapLogic.mlua` | modified | 배정/해제 뒤 `BroadcastPlayerList` — 닉네임·구역·생존을 탭/줄바꿈 문자열로 전 클라에 통지 |
| `tools/gen-track-grid.js` | created | 그리드 텍스처 생성기(1440×960, 포석 트랙·발판·점선·S/E·복귀 화살표) |
| `assets/textures/track-grid.png` | created | 생성 결과. 업로드 RUID `651583e1c1ee44cdb6d2a891755ab528` (ZoneTrackGrid, sprite/object) |
| `assets/textures/README.md` | modified | 그리드 트랙 항목, 스타디움·HUD 프레임 "보관", 교체 절차의 참조처 갱신 |
| `.beaver/output/roadmap/maple-augment-defense-roadmap.md` | modified | #2·#4 in-progress(화면 v2), 결정 대기 #1~#3 확정, 증강 흐름 기록 |

## Tests Written
CLI 러너 없음(docs/testing.md). 플랜의 `[CASES]`는 Play Test 중 `maker_execute_script`로 실행해 로그로 확인했다(아래). 위임형(목록 통지 호출·SetWatchedZone 호출)은 플랜대로 생략.

## Verification
Play Test(2026-09-14, 콜드 스타트 3회) — `maker_logs(build)` 0건, 런타임 스크립트 에러 0건(RectTileMap 수동 추가 경고는 기존과 동일).

**계산형 [CASES] — 15/15 PASS** (client `maker_execute_script`)
- `GetTrackPoint` t=0 → 구역중앙+(−10.222, +0.444) = (3열6행) / t=1 → (−10.222, −10.222) = (3열12행) / t=4/66 → (3열2행) / t=15/66 → (14열2행) / t=0.5/66 → 두 칸 중간 / t=1.3·−0.2 → 양끝 클램프
- `GetTrackLength` 117.333 · `IsRoadCell` (3,6)(12,6) true, (1,1)(4,6) false · `IsPadCell` (4,6)(6,3) true, (1,1)(3,6) false · `GetPadCount` 81 · `GetPadCell` 1=(3,1), 81=(8,12), 0·82 클램프 · `CellDistance` 0/1/4/6 · `GetBossPoint` = 구역 중앙 · 줌 30%

**화면 — 스크린샷 대조**
- 그리드 텍스처: 좌 299.6 · 상 79.6 · 칸 80.06px @1920 (목업 300·80·80). 8구역 전부 생성(F4 확인), 경계선 없음
- HUD: 좌상단 시간·메소 칩, 좌측 "1 / 8" + 내 행(금색 바·(나)), 우측 영입 + 빈 슬롯 6, 좌하단 증강. 하단 바·미니맵·스킬칸 없음
- `SetTime("12:34")`·`SetMeso(1250)` → "12:34"·"1,250" / `SetPlayerAlive(me,false)` → 회색 + 비석 / `SetUnitSlot` 3개 + 슬롯 2 선택 → 금색 테두리, 긴 직업명은 잘림 / F4 → 구역 4로 이동 + 내 행 하이라이트 해제
- 영입 팝업: 모험가 탭·4계열·10직업·"무료"·보유 0/6, ESC로 닫힘 / 증강 팝업: 탭 5(0)·"아직 얻은 증강이 없어요"·상세 / B → 3택1: 카드 3, 칩 선택 시 "3. 비숍에 수령"(금색), ESC 무시, 수령 → 닫힘(로그)

**빌드 중 실측으로 바뀐 것(플랜과 다른 점)**
1. **업로드 스프라이트 PPU = 30**(스타디움 텍스처의 100과 다름 — 1440px급 대형 이미지라 그런 듯). 텍스처 스케일 2.222 → **0.667**. 서브카테고리(background/object)는 무관.
2. **`IsAllowZoomInOut=false`면 `ZoomTo`가 무시된다.** ClaimCamera에서 허용 → ZoomTo → 0.2초 뒤 잠금으로 변경. (이전 빌드가 됐던 이유는 미상 — 지금 코드가 확실한 순서)
3. 팝업 안 반투명 색은 테두리 백킹이 비쳐 보여 **패널 기본색에 미리 합성한 불투명 색**(`Mix`)으로 통일.
4. `OverflowType.ellipsis`는 박스보다 긴 글이 오면 이전 글을 그대로 보여주는 문제 → 슬롯 직업명은 `Truncate`.
5. 스프라이트 중심 = 구역 중앙 + (+1.33, **−0.44**) (플랜의 −1.78은 오기 — 코드는 GridLeft/GridTop에서 계산).

## Remaining Issues
- 플레이어 목록은 **1인 Play Test로만 확인**(행 1개). 여러 명·퇴장 시 재정렬은 Phase 8 멀티 검증에서.
- 3택1 미리보기 **B 키**는 Phase 6에서 트리거 연결과 함께 제거.
- 슬롯의 긴 직업명("아크메이지(썬·콜)")은 잘려 보임 — 슬롯 폭을 더 늘리거나 약칭 도입은 사용자 판단.
- 영입 카드 가격은 "무료" 고정 문자열 — Phase 2 경제표 연결 시 교체.
- `.info/artifacts/hud-layout.html`(v16)과 화면을 계속 같이 맞춘다 — 페이즈 완료는 사용자 만족 루프.

## Change - 260914-1 · 배경 헤네시스로 (아티팩트 + 맵)
- **요청**: "트랙/타일 배경을 헤네시스로 변경. 아티팩트와 맵 모두"
- **변경**: 바닥 타일 엘나스 눈 → **헤네시스 잔디**(`tools/gen-henesys-floor.js` → `assets/textures/henesys-grass.png`, RUID `d908c425553c42c5b11016ab40b306f4`, `CaveFloorTileSet.tileset` datas[0] 교체). 트랙은 헤네시스 포석 유지, 잔디 위에서 읽히도록 그리드 텍스처 색만 재생성(빈 칸 선 짙은 초록·발판 흰 반투명, RUID `f8bf4274602c4d22b2e6643e114fbc5f` → `RtsZoneLogic.GridRUID`). 아티팩트 v17(`.ground` 잔디 톤·`.cell/.pad` 색) 같은 URL로 재발행, `.info/artifacts/hud-layout.html` 동기화. README 갱신(눈·회청판은 보관).
- **검증**: Play Test 콜드 스타트 — 잔디 바닥 + 포석 트랙, 그리드 위치·크기 불변, 빌드/런타임 에러 없음. 스크린샷이 아티팩트 v17과 같은 톤.
- **남은 것**: 없음(사용자 확인 대기).

## Change - 260914-2 · 트랙/타일 테마 프리셋 + 프로토타입 완료
- **요청**: "화면은 일단 만족. 추가 요소는 저기서 추가. 프로토타입 완료. 단, 트랙/타일은 프리셋 가능하도록"
- **변경**: `RtsThemeLogic`(신규) — 프리셋 표 `{key, name, floorTile, gridRUID}`(henesys 기본·elnath 보관), `GetPreset/GetFloorTileName/GetGridRUID`, 서버 `ApplyPreset(key)`(바닥 재채움 + 8구역 그리드 스프라이트 RUID 교체, 없는 키는 false). `CaveFloorTileSet`에 잔디·눈 타일 둘 다 등록, `RtsBootstrapLogic.EnsureGroundTiles`는 프리셋 타일 **이름**으로 채움(`FillGroundTiles(name)` 분리), `RtsZoneLogic`의 `GridRUID` 프로퍼티 삭제 → 프리셋에서 읽고 `SetGridRUID`로 교체. 아티팩트 v18 — 헤더 "테마" 선택(헤네시스/엘나스), `.stage[data-theme]` 변수 한 벌씩. 로드맵 #2·#4 done, Cross-Cutting에 "트랙/타일은 테마 프리셋" 규칙 추가, README에 새 테마 추가 절차.
- **검증**: Play Test — 기본 헤네시스로 시작 → 서버 `ApplyPreset("elnath")` → 눈 바닥 + 회청 그리드로 즉시 전환(스크린샷) → `ApplyPreset("henesys")` 복귀 → 알 수 없는 키 `ludibrium`은 false + 로그. 빌드/런타임 에러 없음.
- **남은 것**: 프리셋 선택 UI·과금 연결(로드맵 #35 메모대로 나중). 새 테마는 README "테마 프리셋" 절차대로 4곳에 한 줄씩.

## Change - 260914-3 · 헤네시스 장식물(버섯집·나무) + 월드 프롭 모델 교체
- **요청**: "배경이 헤네시스인데 타일에 막 버섯집이랑 나무같은거 있으면 좋겠는데"
- **변경**: 공식 MSW **탑뷰 헤네시스 오브젝트**(`maplestory/map/obj/msw/topview_henesys/*` — 버섯집 5·나무 4·덤불 2·건초 2·깃발 2·벤치 1 = 16개)를 테마 프리셋의 `decor` 목록(칸 좌표)으로 추가. 트랙 칸·발판을 피해 빈 칸과 그리드 바깥 여백(HUD와 안 겹치는 아래쪽)에 배치. `RtsZoneLogic.SetDecor`가 8구역 모두에 같은 자리로 세우고, 테마 전환 시 지우고 다시 세움. 엘나스 프리셋은 decor 비어 있음(나중에 눈 소품 추가 가능). 월드 스프라이트 프롭은 `model://MapObject`(Transform+SpriteRenderer, 카메라 없음 — 실측)로 교체 → defaultplayer 복제 우회 폐기. 아티팩트 v19에 같은 자리로 64px 썸네일 표시(헤네시스 테마만).
- **검증**: Play Test — 16종 장식물이 원본 해상도로 표시(스크린샷), 유닛 발판·트랙 안 가림, 카메라 하이재킹 없음. `ApplyPreset("elnath")` → 장식물 0개, `ApplyPreset("henesys")` → 128개(8×16) 재생성. 에러 없음.
- **남은 것**: 장식물 자리·종류는 사용자 취향대로 계속 조정(프리셋 표 한 줄 = 하나). 유닛/몹 OrderInLayer는 110보다 크게(Phase 3·4).

## Change - 260914-4 · 장식물 → 전체 영역 배경 마을
- **요청**: "트랙에 건물을 주기보다, 지금 맵과 타일의 전체 영역 백그라운드로 버섯집을 넣는거로"
- **변경**: 헤네시스 프리셋의 decor를 화면 전체(열 −2.75~20.25·행 0~12.5)에 마을처럼 깐 58개(버섯집 23·나무 17·덤불 7·건초 4·깃발 4·벤치 2)로 교체하고, **그리드 아래**(OrderInLayer 90) **반투명 60%**로 둠 — 트랙·발판·선은 그 위에 그대로. `RtsThemeLogic.GetDecorOrder/GetDecorAlpha`로 공통 지정. 아티팩트 v20 동일(트랙 SVG 아래 레이어, opacity .6).
- **검증**: Play Test 콜드 스타트 — 배경 마을 위에 그리드·트랙 정상, 에러 없음. 테마 전환 시 제거/재생성은 이전 Change와 동일 경로.
- **남은 것**: 밀도·투명도·자리는 취향대로 조정(프리셋 표·`GetDecorAlpha`).

## Change - 260914-5 · 배경 1장 시도 → 배경 마을로 복귀
- **요청**: "버섯집 하나 딱 이미지 크게 1개만 백그라운드" → 지정 스프라이트 `2fceda33`(grassysoil_new/house5) 스케일 3.5 중앙 배치까지 해봤으나 "별로" → **아까의 배경 마을(58개, 그리드 아래 60%)로 복귀**.
- **상태**: 코드·아티팩트(v23)는 Change 260914-4와 동일. 배경 1장 안은 프리셋 표에 한 줄(ruid+scale)로 언제든 재현 가능(원점: topview 건물은 바닥 근처, house5는 중앙 근처).

## Change - 260914-6 · 배경 사물을 트랙 바깥으로, 불투명
- **요청**: "사물은 트랙 바깥에 배치. 안쪽은 유닛 배치 자리라 배경이랑 겹치면 안 됨. 바깥이면 투명도도 낮출 필요 없음"
- **변경**: 헤네시스 decor 34개(버섯집 7·나무 12·덤불 6·건초 5·깃발 3·벤치 1)를 **트랙·발판 영역(2~15열) 바깥**에만 — 왼쪽 여백(열 <0.5), 오른쪽 16~18열+여백, 위쪽 띠(행 <0.5). `GetDecorAlpha` 1(불투명), `GetDecorOrder` 110(그리드 위). 아티팩트 v24 동일(트랙 위 레이어, 불투명).
- **검증**: Play Test — 발판·트랙 위에 사물 없음, HUD(플레이어 목록·우측 슬롯·증강 버튼)와 큰 겹침 없음(왼쪽 위 작은 덤불 2개는 인원 8명 목록 아래 들어갈 수 있음). 에러 없음.

## Change - 260914-7 · 바닥 = 공식 헤네시스 RectTile, 트랙 위 초록달팽이 시연
- **바닥**: MSW 공식 탑뷰 타일 세트 `maplestory/mod/recttile/henesys/{grass 3, soil 22, stone 18}` 발견(검색 `*henesys` → 메타데이터 경로 필터). 타일셋에 잔디 3·흙 1·돌 3 등록, 헤네시스 프리셋 바닥 = `HenesysGrass1` + 변형(`HenesysGrass2/3`, 꽃) 12% 결정적 해시 무작위. `RtsConfigLogic.FloorTileUnit = 4`(8은 흐림 — 실측 비교), `FillGroundTiles(tile, variants, ratio)`가 GridSize도 맞춘다. 아티팩트 v25 바닥 톤.
- **트랙 시연**: `RtsTrackWalkerComponent`(신규, Phase 3 몹 이동의 씨앗) — t를 속도/길이만큼 올려 `GetTrackPoint`로 이동, E→S 순간이동, 좌우 진행에 따라 FlipX. `RtsDemoLogic`(신규, 임시)이 입장 시 구역마다 초록달팽이 3마리(사용자 제공 클립 e7d919d7…, 스케일 2.5, 속도 3.5유닛/초 ≈ 한 바퀴 33초)를 트랙에 올린다. **Phase 3 RtsWaveLogic이 생기면 RtsDemoLogic은 삭제.**
- **검증**: Play Test — 잔디·꽃 타일 정상, 달팽이 3마리가 트랙을 따라 이동(8초 간격 스크린샷 비교), 돌길 위에 그려짐(OrderInLayer 200), 에러 없음.
- **남은 것**: 트랙 텍스처 교체(돌 타일 후보), 몹 이동 동기화 부드러움은 여러 클라에서 확인(Phase 8).

## Change - 260915-1 · 유닛 정보 팝업 + 트랙 위 캐릭터 선택·위치 이동 (아티팩트 v26~v28 → 게임)
- **요청**: "아티팩트에 있는거 화면 UI에 반영. 캐릭터 클릭해서 상태보기/대상지정 스킬 변경/아바타 변경/위치 이동(타일 선택, 쿨타임 유닛마다 3분)" → 이어서 "마우스 오버 손 커서 / 클릭 시 캐릭터 우측 작은 메뉴(위치 이동·상세정보) / 위치 이동은 타일 구분 강조 / 상세정보에서 위치 이동 제거 / 타일 범위 → 사거리"
- **변경**(새 스크립트 5 + 수정 5):
  - `RtsJobTableLogic`(신규, Phase 2 #6 부분) — 히어로·팔라딘·다크나이트 정의(character.md 1:1: 공격력·레벨업당·속도·모험가 세트 RUID·스킬표·레벨별 계수), level.md 비용표, balance-detail 규칙의 `Calc`(공격력·1타·보스/몬스터 DPS). 스킬 설명은 **"사거리 n"**(타일 범위 → 사거리).
  - `RtsUnitComponent`(신규) — 유닛 상태 Sync 프로퍼티(주인·구역·번호·직업·레벨·스킨·칸·결속 대상·이동/대상 변경 쿨 만료 시각). 서버 `ApplyLook`(기본 세트 / **내 아바타** = `CostumeManagerComponent.DefaultEquipUserId`로 주인 코디 복제 + 직업 무기), `PlaceAt`. 클라: 클릭 영역 설정 + TouchEvent → 선택 로직.
  - `RtsUnitLogic`(신규, 서버 권위) — 유저별 유닛 6·메소(SyncTable). 입장 시 **시범 편성 3기**(1. 히어로 Lv12 (13,7) / 2. 팔라딘 Lv40 (6,3) 결속→1 / 3. 다크나이트 Lv20 (5,9)) + 메소 12,400. 요청 처리 `RequestLevelUp/RequestBond/RequestSkin/RequestMove`(senderUserId 검증, 쿨타임 3분 = `CooldownSec`, 이동은 내 유닛 자리면 맞교환). 결과는 `OnChanged`(그 클라에만) + Sync.
  - `RtsUnitPopupLogic`(신규, 클라) — 유닛 정보 팝업(1229×720): 좌 외형(**UI 아바타 미리보기** `model://uiempty` + AvatarGUIRenderer) + 스킨 3(기본/내 아바타/프리미엄 잠김), 능력치 9행, 우 스킬 목록(미획득 흐림, 액티브/패시브 태그), 결속 행 **셀렉트 박스**(미지정/내 다른 유닛, 드롭다운은 body 마지막 자식으로 다른 행 위에) + "재지정까지 m:ss"/"변경 가능 · 쿨타임 3분", 하단 누적 투자·다음 벽·보유 메소·**레벨업 버튼**(벽 붉게, 메소 부족·최대 레벨 비활성). 1초 틱으로 쿨 갱신. **위치 이동 버튼은 없음**(메뉴에서만).
  - `RtsUnitSelectLogic`(신규, 클라) — 마우스 오버 시 메이플 손 커서(`ui/basic/cursor/0` = `3930c5d2…`), 캐릭터 클릭 → 우측 메뉴 **[위치 이동 | 상세정보]**(쿨 중 "이동 대기 m:ss" 비활성), 위치 이동 모드 = 발판마다 **업로드 틀 스프라이트 `RtsPadFrame`(`2c03a06f…`, 스케일 2.12)** 금색/파랑(맞교환) + 상단 안내 바, 발판 클릭 → `RequestMove`, ESC 취소. 발판 위에서도 손 커서.
  - `RtsPopupLogic` — kind `"unit"`(폭 가변, 제목 리치텍스트), 닫을 때 유닛 팝업 정리. `RtsHudLogic` — `Int`(실수→정수 표기), `RefreshMyUnits`(슬롯 6 채움), 슬롯 클릭 → 상세정보, `ShowHint/HideHint`. `RtsBootstrapLogic` — 입장 시 시범 유닛, 퇴장 시 제거. `RtsZoneLogic.CellKey` — 칸 번호 정수 정규화.
  - 자산: `assets/textures/pad-frame.png` 생성·업로드(msw-mcp 2단계, README 항목). 아티팩트 v28(캐릭터 메뉴·이동 모드·사거리) 같은 URL로 재발행, `.info/character.md`·`balance-detail.md`·메모리 동기화.
- **검증**: Play Test 콜드 스타트 4회 — 빌드 에러 0(Info 힌트만), 런타임 에러 0. 3기 아바타가 발판에 서고 슬롯에 "1. 히어로 Lv 12 …". 캐릭터 클릭(월드 좌표 시뮬 클릭) → 메뉴 표시. 팝업: 팔라딘 Lv40 수치가 목업과 일치(568 / 1,090 / 4,362 / 누적 34,000 / 다음 벽 94,000 / 레벨업 6,000). `RequestLevelUp(2)` → Lv41·메소 6,400·슬롯·수치 즉시 갱신. `RequestBond(2,3)` → "3. 다크나이트 Lv20" + "재지정까지 2:54" 카운트다운. `RequestSkin(2,1)` → 주인 아바타 코디 + 해머로 교체(미리보기도). 이동 모드: 발판 80칸 틀 표시(내 유닛 자리 파랑), 발판 (4,3) 클릭 → 서버 로그 "move 2 -> (4,3)" + 실제 이동. 드롭다운 3항목 렌더 확인.
- **실측으로 바뀐 것**: ① 프로퍼티·Sync·RPC로 온 number는 `tostring`이 "1.0" → 이름/키/표시는 `Int`·`string.format("%d")`로(엔티티 이름 `Unit1_1`, `CellKey`). ② `TouchReceiveComponent.AutoFitToSize/TouchArea`는 동기화되지 않아 클라 `SetupClient`에서 직접 설정(1.4×2.2, 오프셋 +1.1). ③ 클라 `SpawnByModelId`/`Destroy`는 여러 프레임에 걸쳐 처리(80개 = 약 1초) → 마커 이름에 세대 번호. ④ `_UtilLogic.ServerElapsedSeconds`로 양쪽 시계 통일. ⑤ MCP 도구(스크린샷·스크립트 실행)가 플레이 화면에 **유령 클릭**을 넣어 이동 모드 중 엉뚱한 이동이 일어난다 — 실기 조작에는 없음.
- **남은 것**: 마우스 오버 손 커서는 실제 마우스로만 확인 가능(도구 커서 시뮬 불가) — 사용자 확인 필요. 시범 편성 3기·메소 12,400은 영입(Phase 5 #18)·경제표가 붙으면 교체. 궁수 이하 직업은 정의 후 `RtsJobTableLogic`에 추가. 프리미엄 스킨은 잠김. 다른 유저 구역의 유닛은 클릭 불가(내 유닛만).

## Change - 260915-2 · 스킨 = 기본 / 월드 아바타(월드코인 1,600 · 30일 결제 해금)
- **요청**: "프리미엄 프리셋은 없어. 월드 아바타는 월드코인 결제해야 사용 가능. 30일 기간동안 해금. 월드코인 1600개" → "결제연동이 되는지부터 찾아줘" → 확인 후 "ㅇㅇ"
- **결제 연동 확인**: MSW 월드 상점(아이템/이용권, 10~10,000 월드코인, 정산 35%). 이 월드 상점 API 정상. 스크립트 `_WorldShopService:PromptPurchase`(클라) + `SetProcessPurchaseCallback`(서버 지급). Maker는 코인 차감 없는 테스트 구매.
- **변경**: 월드 상점 **아이템 "월드 아바타 30일"** 1,600코인 **비공개 등록**(id `QK03ZI15E`, 썸네일 `assets/textures/world-avatar-30d.png`, msw-mcp `world_item_upload_thumbnail`→`world_item_create`). `RtsUnitLogic`: `AvatarProductId`, `AvatarUntilByUser`(Sync, UTC ms), 입장 시 유저 DataStorage `avatarUntil` 로드, `ProcessPurchase`(만료 또는 지금 + 30일 → DataStorage 저장 → 동기화 → 클라 통지, true), `ExpireAvatars`(1분마다 만료 유저의 스킨 1 → 0), `RequestSkin(…,1)`은 해금 중일 때만, 클라 `RequestBuyAvatar` → 구매창. `RtsJobTableLogic` 스킨 2종. 팝업 카드: 기본 / 월드 아바타(잠김 = "1,600 월드코인 · 30일 해금" 클릭 → 구매창, 해금 = "내 메이플월드 코디 · D-n"). 아티팩트 v29 동일(목업은 클릭 즉시 해금 흉내). character.md 헤더·로드맵 확정 목록·메모리 갱신.
- **검증**: Play Test — 팝업에 잠긴 월드 아바타 카드. `RequestBuyAvatar()` → **실제 MSW 구매창**("월드 아바타 30일 · W 1,600 · 테스트 구매 시에는 월드코인을 차감하지 않습니다") 표시. 서버에서 `ProcessPurchase` 시뮬레이션 → DataStorage 저장 code 0, `unlocked=true days=30`, 팝업 카드 "D-30", `RequestSkin(2,1)` → 내 코디로 교체(미리보기 포함). 구매창 버튼은 엔진 UI라 도구로 못 눌러 실제 구매 확정은 사용자 확인 필요. 테스트 후 로컬 DataStorage 초기화(`maker_reset_data_storage`)해 잠김 상태로 되돌림.
- **남은 것**: 출시 전 상품 **공개(isPublished)** 전환. 만료 D-day는 클라 시계 기준(서버와 수 초 오차 무시). 구매 실패/환불 시 처리(환불은 공식 사이트에서 크리에이터가, 해금 회수는 미구현).

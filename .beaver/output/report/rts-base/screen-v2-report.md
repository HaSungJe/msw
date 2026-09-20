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
  - `RtsUnitComponent`(신규) — 유닛 상태 Sync 프로퍼티(주인·구역·번호·직업·레벨·스킨·칸·홀리 유니티 대상·이동/대상 변경 쿨 만료 시각). 서버 `ApplyLook`(기본 세트 / **내 아바타** = `CostumeManagerComponent.DefaultEquipUserId`로 주인 코디 복제 + 직업 무기), `PlaceAt`. 클라: 클릭 영역 설정 + TouchEvent → 선택 로직.
  - `RtsUnitLogic`(신규, 서버 권위) — 유저별 유닛 6·메소(SyncTable). 입장 시 **시범 편성 3기**(1. 히어로 Lv12 (13,7) / 2. 팔라딘 Lv40 (6,3) 홀리 유니티→1 / 3. 다크나이트 Lv20 (5,9)) + 메소 12,400. 요청 처리 `RequestLevelUp/RequestBond/RequestSkin/RequestMove`(senderUserId 검증, 쿨타임 3분 = `CooldownSec`, 이동은 내 유닛 자리면 맞교환). 결과는 `OnChanged`(그 클라에만) + Sync.
  - `RtsUnitPopupLogic`(신규, 클라) — 유닛 정보 팝업(1229×720): 좌 외형(**UI 아바타 미리보기** `model://uiempty` + AvatarGUIRenderer) + 스킨 3(기본/내 아바타/프리미엄 잠김), 능력치 9행, 우 스킬 목록(미획득 흐림, 액티브/패시브 태그), 홀리 유니티 행 **셀렉트 박스**(미지정/내 다른 유닛, 드롭다운은 body 마지막 자식으로 다른 행 위에) + "재지정까지 m:ss"/"변경 가능 · 쿨타임 3분", 하단 누적 투자·다음 벽·보유 메소·**레벨업 버튼**(벽 붉게, 메소 부족·최대 레벨 비활성). 1초 틱으로 쿨 갱신. **위치 이동 버튼은 없음**(메뉴에서만).
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

## Change - 260916-1 · 파티 버프 = 캐릭터 발 아래 아이콘 + 팝업 "적용 중인 버프" 목록 (아티팩트 v32 → 게임)
- **요청**: "적용되는 버프 아이콘이 캐릭터 밑에 표시되도록 하고, 캐릭터 클릭 -> 상세보기에서 적용중인 버프도 추가해서 클릭하면 적용중인 버프 목록과 그 옵션을 확인할 수 있게 하자"
- **변경**: 새 `RtsUnitBuffLogic`(클라) — 정의 `GetDefs`(character.md의 유닛 간 스킬 4종: 홀리 유니티·샤프아이즈·프레이·조커: 날카로운 검, scope all/target/near, 원작 스킬 아이콘 RUID), `GetBuffsFor(zone,no)`(동기화된 RtsUnitComponent 값만으로 계산, 같은 id 1개), `ApplyToStat`(최종 데미지 곱·크리 합), 아이콘 = 유닛 엔티티 자식 MapObject(스케일 2.2 = 칸의 40%, 발 아래 가로 정렬, 세대 번호 이름) — `MarkDirty(zone)`으로 동기화마다 0.2초 모아서 구역 단위 재생성(남의 구역 유닛도). `RtsUnitComponent.SetupClient/OnSyncProperty` → `MarkDirty`. `RtsUnitLogic.GetZoneUnit(zone,no)` 추가(GetMyUnit이 사용). `RtsJobTableLogic.Calc` → `CalcStat(job,L,st)` 분리(파티 버프는 GetStatRaw에 넣지 않는다 — 시전자 자신 포함이라 이중 적용 방지). `RtsUnitPopupLogic`: 능력치에 버프 반영값(▲: 최종 데미지·크리티컬·DPS). 우측 스킬 칸을 **탭 3개**로 — 스킬(`BuildSkillTab`, 그대로) / 증강 n(`BuildAugTab`, `RtsUnitBuffLogic.GetAugmentsFor` 스텁 = 빈 목록, 등급 배지·이름·효과 행) / 적용 중인 버프 n(`BuildBuffTab`, 아이콘·이름·범위 / 효과). 증강·버프는 `SpawnScrollList`(uisprite + ScrollLayoutGroupComponent Vertical, 다 들어가면 UseScroll 끔). 탭은 `Tab` 프로퍼티로 유지. 사용자 피드백 3회: 출처 줄 삭제 → 행의 아이콘 대신 n개 + ▸ 버튼 → "별로야, 우측을 스킬/증강/버프 탭으로" (능력치 버프 행 삭제, PanelH 720 유지). 아티팩트 v32(트랙 SVG 칩 + 팝업 행/목록, 목업은 머리글자 칩). character.md 헤더·메모리(balance·assets) 갱신.
- **검증**: Play Test — 시범 팔라딘 Lv40 홀리 유니티 → 1. 히어로 발 아래 메이플 용사 아이콘(스케일 1.1은 10px라 안 보여 2.2로 실측 조정). 히어로 팝업: 최종 데미지 120% ▲, 보스 DPS 206 ▲(172 × 1.2), 탭 "스킬 / 증강 0 / 적용 중인 버프 1" — 버프 탭 행 "홀리 유니티 지정 유닛 1개 / 최종 데미지 +20%", 증강 탭 빈 안내. 가짜 버프 12개로 휠 스크롤·핸들 동작 확인(ScrollLayoutGroup 프로퍼티는 ScrollBar* 이름 — d.mlua의 Visible은 "no such field"). 서버에서 BondNo 2→3으로 바꾸자 아이콘이 u1 0개 → u3 1개로 이동. 런타임 에러 없음. 목업은 브라우저에서 동일 확인.
- **남은 것**: 지금 게임 직업(히어로·팔라딘·다크나이트)에선 홀리 유니티만 살아 있음 — 궁수·마법사·도적을 `RtsJobTableLogic`에 추가할 때 GetStatRaw에서 샤프아이즈·프레이·조커 자기 적용분을 빼고 버프 정의의 job id(bow/marks/bishop/phantom)를 맞춘다. 남의 구역 아이콘은 그려지지만 그 구역을 보는 카메라 전환은 별도.

## Change - 260916-2 · 홀리 유니티 개명 + 다크나이트 스피어 버스터(영상 추출 이펙트) + 스킬 연출 재생기
- **요청**: "결속 이름 변경. 홀리 유니티, 아이콘 53a38855…" / 다크 임페일에 옛 용기사 스피어 버스터 애니메이션 → 라이브러리에 없음 → "영상에서 이펙트만 빼서 리소스로 저장해놓고 못씀?" → 허용 → 채움 정도 3회 조정(v1 외곽선 → v2 채움 → v3 진하게 → "너무 어색" → v2 복귀) → "다크 임페일을 스피어 버스터로 변경. 애니메이션·사운드·스킬명 모두 적용"
- **변경**: (1) 결속 → **홀리 유니티**(코드·character.md·balance-detail·augmentation·메모리·목업 v38, 아이콘 5차 홀리 유니티 `53a38855…`, 내부 id bond 유지). (2) 나무위키 mp4 → ffmpeg 프레임 → 흰 배경 알파 복원 + 캐릭터 실루엣 구멍 + 속 채움(`assets/textures/crusher/extract_crusher.py`) → 11프레임 × 3버전 sprite/skill 업로드(v2 `RtsCrusherFx2_01..11`이 최종, RUID는 `meta.json` `ruids`). (3) **`RtsJobTableLogic`**: 다크나이트 Lv1 액티브 이름 **스피어 버스터**, `fx` 연출 정의(motion stabT1 / frames 11 / frameSec 0.09 / scale 1.7 / feetDx −0.11 feetDy 0.83 / sound 옛 스피어 크러셔 use `fcac442d…` / hitSound 기존), 창 아이템을 **레볼루션 스피어 `44d92464…`**로(캐시 창 `acd581b7…`은 afterImage swordTS = 빨간 참격 잔상이 이펙트와 겹침; `ShowDefaultWeaponEffects=false`로는 못 끔). (4) 새 **`RtsSkillFxLogic`**(클라): `Preload/PlayCast(unit, no, fx)/PlayBasic(no)/DemoLoop(no, on)` — 모션 + 플립북(SpriteRUID 교체) + 시전음. 전투 루프(Phase 3)가 PlayCast를 부르면 됨. character.md·목업 v39·메모리(assets) 갱신.
- **검증**: Play Test — `_RtsSkillFxLogic:DemoLoop(3, true)`로 다크나이트가 1.25초마다 스피어 버스터 시전(찌르기 + 파란 용 실루엣·마법진·용머리 + 옛 시전음, 빨간 잔상 없음). 팝업 스킬명 스피어 버스터. 런타임 에러 없음.
- **남은 것**: 창 아이템 최종 선택(레볼루션 스피어는 임시 — 은색+금장식 후보: 우트가르드·메이플 베리트·벨룸·네크로 스피어). 히어로·팔라딘도 같은 `fx` 형식으로 연출 정의 옮기기(지금은 character.md 주석에만). 플립북 마지막 2프레임은 옅음. 미커밋.

## Change - 260916-3 · 캐릭터표 2차 수정 반영(레이징 블로우 2회·프레이 자신 제외·로어 사거리 5) + 밸런스표 재작성 + 증강 점검
- **요청**: "캐릭터표 수정했고, 증강 목록을 추가했어. 밸런스표 다시 작성하고, 캐릭터 컨셉과 증강의 종류가 잘 어울리는지 점검해줘. 추가했으면 하는 증강도" + "프리즘 증강에 신궁/보우마스터의 증강명 하나 지어줘"
- **변경**: `.info/balance-detail.md`를 계산 스크립트(scratchpad `balance_gen.py`, damage.md 식 그대로)로 재생성 — 비숍 30~50 ÷1.15(프레이 자신 미적용), 팬텀 조커 0.2초·블스아이(50: 9,009), 히어로 타격 수 2, 팔라딘 50 사거리 2·신궁 50 사거리 4·DK 로어 5(사거리 가중 평가 갱신), 메익 쿨 8초 메모, 새 절 **"증강 반영"**(능력치 증강 가치표 · 스킬 강화 브론즈 상승률 · 직업 전용 증강 풀스택 50레벨 보스 DPS · 컨셉 점검 결론 8개). `damage.md`: 스킬 강화 증강 = 1회 타격 비율 합연산, 보스 데미지 증가 = 최종 항목, 스킬 획득 뒤부터, 파티 버프 자신 포함 예외(홀리 유니티·프레이), 조커 0.2초. `character.md`: 헤더 프레이 제외, 크로스보우 액스퍼트 종류 액티브→패시브(오타). `augmentation.md`: 프리즘 이름 **폭풍의 눈**(보우마스터)·**일격필살**(신궁), `$`→`%` 3곳. 코드: `RtsJobTableLogic` 히어로 GetStatRaw ratio 50/100·hits 2 + 레이징 블로우 설명 2회, 드래곤 로어 설명(사거리 5·보스전 미사용); `RtsUnitBuffLogic.InScope` near는 자신 제외. 목업 v40 재발행(같은 URL). 메모리 balance·MEMORY 갱신.
- **검증**: Play Test — 히어로 팝업 기본 공격 "50% × 3마리 × 2회", DPS 이전과 동일. 빌드·런타임 에러 없음(아래 실측 참고).
- **사용자 회신**: 프리즘 이름 승인(적용됨). 크리 증강 배치·프리즘 스킬 잠금은 **의도된 설계**(크리 = 샤프아이즈/증강 몰기 빌드, 크뎀은 최종 뒤 곱 / 프리즘 = 함부로 집지 말라는 트레이드오프) → balance-detail 결론 0번으로 옮기고 메모리에 재제기 금지로 기록.
- **남은 것**: 열린 결론(골드 쿨 2초 보스 손해·50레벨 스킬 증강·나로 프리즘·히어로 배율·추가 증강 제안)은 사용자 결정 대기 — augmentation.md 수치는 초안 그대로. 팬텀 영입 규칙은 사용자 확정(슬롯 1개 사용, 유닛 버리기 = 메소·증강 소실, 1레벨 시작, 지정 버프 대상 소실 → 재지정) → character.md·balance-detail·메모리에 기록, 구현은 Phase 5/6. 미커밋.

## Change - 260916-4 · 액티브 스킬 잠금 설정 [사용 / 보스전 잠금 / 잠금]
- **요청**: "액티브 스킬 잠금 설정을 할 수 있도록 UI/기능 추가해야겠다. 1. 사용 2. 보스전 잠금 3. 잠금 3개 선택지로" (골드 '쿨 2초' 증강의 보스 손해를 플레이어 설정으로 해소)
- **변경**: `RtsUnitComponent.SkillLocks`(Sync 문자열 — 스킬 목록 순서대로 "0"/"1"/"2", 패시브 자리는 "0") + `RtsJobTableLogic.DefaultLocks/GetLock/SetLock/LockName`(스킬 정의 `lock` 필드 = 기본값, 드래곤 로어 `lock = 1`, 설명의 "보스전 사용하지 않음" 삭제) + `RtsUnitLogic.RequestSkillLock(no, idx, mode)`(획득한 액티브만, mode 0~2, 쿨타임 없음, senderUserId 검증) + `SpawnUnit`에서 기본값 세팅. `RtsUnitPopupLogic.BuildLockToggle`: 스킬 탭의 획득한 액티브 행 우측에 3분할 토글(사용 초록 56 / 보스전 잠금 주황 100 / 잠금 빨강 56, 높이 28, 선택 외 흐림, 클릭 즉시 요청) — 글자 폭은 236 줄임. 목업 v41(`.seg` 토글, 유닛별 `locks`, 로어 `lock: 1`). character.md 헤더 규칙 + 로어 "잠금 기본값: 보스전 잠금", damage.md 표 규칙, balance-detail(생성기) 골드 쿨 2초 결론 "해소", 로드맵 #20, 메모리 balance·MEMORY.
- **검증**: Play Test — 빌드 에러 0(Info 힌트만). 기본값 팔라딘 "0000000", DK "00001"(로어 = 1). 팔라딘 Lv40 팝업: 디바인 차지·생츄어리 행에 [사용 | 보스전 잠금 | 잠금] 토글, 사용이 초록. `RequestSkillLock(2,3,1)` → 생츄어리 주황 "보스전 잠금", 문자열 "0010000"; 패시브(idx 2)·미획득(idx 7) 요청은 거절. 런타임 에러 없음. 목업 스크립트 `node --check` 통과.
- **추가(사용자 회신)**: 드래곤 로어 보스전 잠금 기본값 확정. **영구 잠금 = 값 3** — 프리즘 증강의 "영구적 잠금"은 강제·해제 불가: 서버 `SetPermaLock(userId, no, idx)`만 설정(획득 전 스킬도), `RequestSkillLock`은 3인 스킬 거절·3 요청 거절, 팝업은 토글 대신 프리즘색 알약 "🔒 영구 잠금"(미획득이어도 표시). 목업 v42. 검증: 서버에서 팔라딘 생츄어리(idx 3)·DK 드래곤 로어(idx 5, 미획득) SetPermaLock → 알약 표시, 클라 `RequestSkillLock(2,3,0)` 거절(문자열 유지).
- **남은 것**: 전투 루프(Phase 3 #15)가 액티브를 고를 때 `GetLock` 반영(1 = 보스 라운드 판정 필요, 2·3 = 사용 안 함). 증강 시스템(Phase 6)이 프리즘 선택 시 `SetPermaLock` 호출. 미커밋.

## Change - 260916-5 · 유닛 팝업 하단 정리 — 누적 투자·벽·보유 메소 삭제
- **요청**: "상세정보에서 누적투자, 다음 레벨까지 얼마 이런거 빼. 보유 메소도 빼. 화면 좌측 상단에 메소 있잖아. 레벨업 10단위 구간에 (벽) 이런 문구도 다 지워. 유저에게는 제공할 필요 없는건 빼"
- **변경**: `RtsUnitPopupLogic.Render` 하단 — `RtsUnitInvest`(누적 투자·다음 벽까지)·`RtsUnitMeso`(보유 메소) 라벨 삭제, 레벨업 버튼의 "(벽)" 문구와 벽 붉은색(`IsWallLevel` 분기) 삭제 → 금색 "레벨업 → Lv n" + 비용만, 메소 부족·최대 레벨 비활성은 그대로. 목업 v43 동일(`#unitInvest`/`#unitMeso`/`.btn-lv.wall` 제거, 푸터 우측 정렬, v25 노트에 삭제 표기). 메모리 balance에 원칙 기록(팝업/HUD에 설계용 수치 노출 금지).
- **검증**: Play Test — 히어로 Lv12 팝업 하단에 레벨업 버튼만("레벨업 → Lv 13 · 250 메소"). 서버에서 Lv19로 올려 벽 직전 확인: "레벨업 → Lv 20 · 750 메소" 금색, "(벽)" 없음. 에러 없음. 목업 `node --check` 통과.
- **남은 것**: 미커밋.

## Change - 260916-6 · 밸런스표 — 증강 43개 전부 적용 시 직업별 보스 DPS 최고점
- **요청**: "밸런스쪽에 각 직업당 모든 증강 적용됬을 때 보스전 어떤지도 적어줘. 각 직업별 보스전 DPS 최고점 확인하게"
- **변경**: `balance-detail.md` 새 절 "증강 43개 전부 — 직업별 보스 DPS 최고점": 브 15·실 15·골 10·프 3을 그 직업 보스 DPS 최대로 고른 이론값(탐욕 + 교환 국소 탐색, 생성기 `balance_gen.py`). 직업 스킬 증강은 보스에 유효한 것만(팔라딘·썬콜·비숍의 라인/파티용은 능력치로 대체, 신궁·섀도어·DK의 프리즘 잠금 무효분도 능력치로), 팬텀은 프리즘 1개를 영입에 사용. 열: 증강 0 / 직업 증강만 / 최고점 / 배율 / +파티 풀(홀리 유니티 50%·프레이 30%·조커 5%·샤프아이즈) / 고른 능력치 조합 / 메모. **보스 공격시 데미지 증가 +%는 같은 능력치라 합연산 후 한 번 곱**으로 확정(damage.md 수정 — 곱으로 두면 ×57 폭발). 결과: 신궁 749k > 히어로 464k > 섀도어 418k > DK 245k > 보마 199k > 불독 192k > 팬텀 170k > 나로 82k > 팔라딘 53k > 썬콜 24k > 비숍 18k.
- **검증**: 신궁 손계산(1085×1.725×5.5×10/1.25×1.75×5.2 = 749k) 일치. 기존 표 값 변동 없음(bossAdd 0일 때 동일).
- **남은 것**: 이론 상한이라 실전 분포(라운드별 등급·3택1·6기 분산)는 별도. 미커밋.

## Change - 260916-7 · 데미지 계산식 7단계 정렬 + 파티 시너지 기준
- **요청**: "계산식 다시 정리할게. 1 공격력 합 → 2 공격력% 합 → 3 보스 데미지 증가 합 → 4 크리 데미지 합 → 5 스킬 데미지 → 6 최종 데미지 곱 → 7 방어율 무시. 이렇게 되있나 확인해봐" + "파티 시너지는 샤프아이즈+홀리 유니티+프레이 기준으로 계산"
- **확인**: 기존 구현(damage.md·`RtsJobTableLogic.CalcStat`·`RtsUnitBuffLogic.ApplyToStat`·목업 `calc()`·표 생성기)의 합/곱 그룹이 7단계와 **동일** — 공격력 +수치 합 → 공격력% 합 → 크뎀 합(기본 20) → 스킬 비율(1회 타격) 합 → 최종 곱 → 방어 뺄셈. 다르게 적혀 있던 건 곱 순서 표기(스킬% → 최종 → 크리)뿐이라 값 변화 없음. 보스 데미지 증가는 이번 세션에서 합연산으로 확정한 것 그대로(3단계).
- **변경**: damage.md 계산식을 7단계로 재작성, character.md 헤더·메모리 규칙("데미지 계산식 = 7단계") 교체. 코드 `GetStat`에 `bossAdd`(3단계, 지금 3직업은 0) 필드 + `CalcStat` `bossMul`, 주석을 7단계 순서로. 목업 `calc()`도 `bossAdd` 반영(표시 변화 없음). 표 '+파티 시너지' 열 = 샤프아이즈 + 홀리 유니티 20% + 프레이 15%(조커 제외, 기본값 — 43개를 그 유닛에 다 썼으니), 나로 대왕 표창은 2배(40%·30%). 결과 예: 신궁 749k → +시너지 1.15M, 히어로 464k → 692k, 나로 82k → 171k.
- **검증**: 표 재생성 값 변동 없음(bossAdd 0). 코드는 Play Test에서 히어로 팝업 DPS 확인 예정(다음 실행 시).
- **남은 것**: 7단계 ⑦의 '감소 수치 = 몬스터 방어율 − 방어율 무시'가 사용자 의도와 같은지 확인 대기. 미커밋.

## Change - 260916-8 · 프리즘 4종 너프 (43개 최고점 기준 DK −10만 · 섀도어 −30만 · 히어로 −30만 · 신궁 1/3)
- **요청**: "다크나이트 데미지 10만 정도 너프되도록 하고, 섀도어는 한 30만 정도 너프. 히어로는 30만 정도 너프. 신궁은 1/3로 너프하자"
- **변경**(augmentation.md 프리즘 수치 — 기본 스킬표는 그대로): 영웅 귀환 "데미지 +100%, 타격수 +4" → **+50%, +1**(464k → 177k) / 광전사 "데미지 +150%" → **+50%**(245k → 143k) / 일격필살 "스나이핑 데미지 +450%" → **+80%**(749k → 245k, 총 180%×10회) / 나도 던진다! "300%×2회, 0.2초" → **250%×1회, 0.3초**(418k → 116k). 후보를 생성기로 비교해 목표에 가장 가까운 값 선택(히어로 대안 '빠름·+50·타격+2' 157k, DK '빠름·+120' 143k 동률, 섀도어 '100%×2/0.2초' 139k). balance-detail 풀스택·최고점 표 재생성, 순위·결론 문구 갱신, 메모리 갱신.
- **결과**: 직업 증강만 — 히어로 25k > 신궁 19k > 보마 17k > 팬텀 13.5k > DK 12.4k > 불독 9.8k > 섀도어 7.6k > 나로 4.4k. 43개 최고점 — 신궁 245k > 보마 199k > 불독 192k > 히어로 177k > 팬텀 170k > DK 143k > 섀도어 116k > 나로 82k > 팔라딘 53k > 썬콜 24k > 비숍 18k.
- **남은 것**: 미커밋.

## Change - 260917-1 · 나머지 8직업 기본 외형 등록 (보우마스터·신궁·썬콜·불독·비숍·나이트로드·섀도어·팬텀)
- **요청**: "유닛의 기본 외형과 스킬들을 마무리하자. 어디서 할 차례지?" → "1. 나머지 직업 외형 2. 액티브 스킬 하나씩. 일단 1번"
- **변경**: `RtsJobTableLogic` — `GetJobIds`(11직업), `HasJob/GetJobName/GetJobGroup/GetSeries`(arc/mag/thf) 전 직업, `GetBaseAttack/GetAttackPerLevel/GetBaseSpeed` character.md 수치(보우마스터 30/+10 매우빠름으로 정정), `GetCostume` 8세트 추가(공식 "모험가 ○○" 세트 남성형 + 진짜 무기; 팬텀은 팬텀 코디 아이템), 미등록 직업의 임시 계수는 직업 공격속도만 반영. `RtsUnitComponent.ApplyLook`·`RtsUnitPopupLogic.SpawnPreview`에 `weapon1h`(CustomOneHandedWeaponEquip)·`cap`·`faceAcc` 슬롯. character.md 8직업 외형 RUID 기록(신궁 헤더의 '보우마스터 세트' 오타 정정), 메모리 assets 규칙.
- **검증**: Play Test — 8직업을 11~18번으로 스폰해 라인업 스크린샷(모자·마스크·무기 전부 표시). 보우마스터 세트 캐시 활은 shoot1에서 파란 폭발 잔상이 크게 떠 메이플 보우로 교체(잭이힌 에인션트 보우·메이플 보우 비교). 에러 없음.
- **남은 것**: 사용자 외형 승인(헤어 색·모자 유무·무기 교체 요청 반영). 2단계 = 직업별 액티브 스킬 1개 연출(모션·이펙트·사운드) + `GetSkills/GetStatRaw` 등록. 미커밋.

## Change - 260917-2 · 전 직업 무기 = 리버스/타임리스 라인 + 팬텀 원작 외형 + 라인업 배치
- **요청**: "모든 직업 무기 아바타를 리버스 무기로 변경하자" / "이쪽에 첫줄 전사, 둘째 궁수, 셋째 마법사, 넷째 도적, 다섯째 팬텀 넣어" / "e1b6fdec…(팬텀 NPC stand 클립) 팬텀은 이렇게 생긴 앤데? 남자이고 여자도 아님"
- **변경**: 라이브러리 `*리버스` 무기는 5종(니플하임·블래스트 니플하임·벨로체·타바르진·블랙뷰티)뿐 → 히어로 리버스 니플하임·팔라딘 리버스 벨로체·신궁 리버스 블랙뷰티, 나머지는 같은 모델 라인 **타임리스**(DK 알슈피스 = 창 최종 확정 / 보마 엔가우 / 마법사 3직업 엔릴 티어(완드, 타임리스 스태프 없음) / 나로 람피온 / 섀도어 킬릭 / 팬텀 페르소나). `GetCostume` 갱신, character.md 무기 줄 전부 교체(메이플 시리즈는 대안으로 기록). 팬텀 헤어 → 노란색 괴도 팬텀 헤어 + 괴도 팬텀 얼굴(`face` 슬롯 = CustomFaceEquip, ApplyLook·미리보기). 라인업은 발판 (4~6, 3~7)에 5줄로 재배치(히어로·팔라딘·DK 포함).
- **검증**: Play Test 라이브 교체 스크린샷 — 5줄 블록에 11직업, 무기·모자·마스크 표시, 팬텀 금발+페더+케인. 에러 없음.
- **남은 것**: 사용자 최종 승인 → 2단계(액티브 스킬 연출). 미커밋.

## Change - 260917-3 · 팬텀 모자 + 여캐 6직업
- **요청**: "팬텀의 마스코트인 모자가 안보이는데" / "보우마스터, 신궁, 썬콜, 불독, 비숍, 섀도어는 여캐야"
- **변경**: '팬텀 히어로즈 페더'는 깃털만 붙는 아이템 → **Vampire Phantom Hat** `cf9ef095…`(팬텀 모자 실루엣, 원작 흰 모자는 라이브러리에 없음; 대안 가면신사의 모자·젠틀맨 모자)로 교체. 여캐 6직업은 세트 여성형(롱코트 01051xxx·부츠 01071xxx·헤어 67xxx) + 얼굴 **청아한 얼굴 21259** `9edd3b01…` 공통(`face` 슬롯). `GetCostume`·character.md(남성형 RUID는 대안으로 기록)·메모리 갱신.
- **검증**: Play 라이브 교체 스크린샷 — 5줄 라인업에서 2·3줄 + 섀도어가 여성형(긴 헤어·여 로브), 팬텀 모자 표시. 에러 없음.
- **남은 것**: 얼굴 눈 색(청아한 얼굴은 붉은 눈 변형 하나만 검색됨) 취향 확인. 2단계(액티브 스킬 연출). 미커밋.

## Change - 260917-4 · 무기 = 세트 전용 무기(마법사·섀도어·나로 한손 판)
- **요청**: "얘네들 각 직업별 무기 있지 않나? 지금 직업의상/외형이잖아. 무기도 있을거같은데" → "마법사들 지팡이 한손무기임. 한손으로 드는 모션. 섀도어도 마찬가지."
- **변경**: `GetCostume` 무기를 각 "모험가 ○○" 세트 전용 무기로 되돌림 — 전사·활·석궁은 두손 판, 썬콜 스태프·불독 완드·비숍 완드·섀도어 단검·나로 표창은 **한손 판**(stand1). 팬텀은 팬텀 오리지날티. 리버스/타임리스는 대안 RUID로 character.md·메모리에 기록. 리버스 실제 재고 확인: `*리버스` 무기 5종뿐(니플하임·블래스트 니플하임·벨로체·타바르진·블랙뷰티), ID 토큰 검색(`01432048` 등)은 다른 아이템이 나와 Reverse ID 추정 불가.
- **검증**: Play 라이브 교체 — 마법사 3·섀도어·팬텀이 한손 자세로 무기를 들고, 라인업 5줄 스크린샷 확인. 캐시 무기 잔상(DK 빨간 참격·보마 파란 폭발)은 공격 모션에서만 나오며 `ShowDefaultWeaponEffects=false`로는 안 꺼짐(기존 실측) — 사용자가 의상 일치를 택함.
- **남은 것**: 2단계 스킬 연출 때 각 무기의 공격 모션·잔상 실제 확인(특히 마법사 캐스팅). 미커밋.

## Change - 260917-5 · 팝업 미리보기 싱크 확인 + 컨텍스트 메뉴 클릭 우선
- **요청**: "상세정보랑 트랙이랑 캐릭터 생김새가 싱크 안 되는데?" / "나이트로드 클릭 → 상세보기 클릭 시 섀도어 클릭이 우선시됨. 팝업이 항상 클릭 우선이어야"
- **원인·변경**: (1) 싱크 — 트랙 유닛은 스크립트로 라이브 교체하고 팝업은 그 Play 세션에 로드된 옛 `GetCostume`을 읽어서 어긋났던 것. 둘 다 `GetCostume` 단일 소스라 스크립트 새로고침 + Play 재시작 후 일치(보우마스터 팝업 vs 트랙 스크린샷). (2) 월드 `TouchEvent`가 위에 놓인 UI 버튼과 함께 발화 → `RtsUnitComponent.OnTouched(screen)`이 `RtsUnitSelectLogic:IsOverMenu(screen)`(메뉴 UI 사각형 `MenuRect`, 여백 6px, `ScreenToUIPosition`)이면 유닛 클릭을 무시. 팝업 열림은 기존 `IsOpen` 가드.
- **검증**: Play — 나로(4,6)·섀도어(6,6) 배치, 나로 메뉴를 열고 섀도어 위에 겹친 '상세정보'를 마우스 클릭 → **4. 나이트로드 팝업**이 열림(이전엔 섀도어 메뉴로 바뀜). 에러 없음.
- **남은 것**: 미커밋.

## Change - 260917-6 · 전투 시험대 — 히어로 레이징 블로우 자동 공격 + 데미지 스킨 + 피격 연출 (Phase 3 #15·#16 첫 조각)
- **요청**: "전사부터 다시 시작. 히어로부터. 몬스터와 인접한 곳에 배치, 거기서 테스트 쭉. 고정 위치에서 타격 시 데미지 출력과 몬스터 피격효과까지. 몬스터 순회를 멈추고 한 마리만 체력 무제한으로" → 피드백 "데미지 스킨 너무 작음 / 흔들림 / 메인 대상 지정 + 좌우 반전 / 레이징 블로우 옛 사운드·모션·이펙트 있으면 교체"
- **변경**: 새 `RtsCombatLogic`(TestBench: 입장 시 `RtsDemoLogic.StopWalkers`, 허수아비 `RtsDummy<zone>` (14,3) 체력 무제한, 유닛 1을 (13,3)에 놓고 공격 주기마다 `DoAttack` — damage.md 7단계로 1회 타격 = floor(공격력×공격력%×스킬비율×최종), 타격 수만큼 `AttackFrom`을 hitGap 간격으로 따로(타격마다 크리 굴림), 메인 대상 쪽으로 `FaceTo`, 전 클라 `CastFx`/`HitFx`), 새 `RtsUnitAttackComponent extends AttackComponent`(Dmg/Crit/CritRate/Hits/TargetName 주입, IsAttackTarget 이름 필터), 새 `RtsMonsterComponent`(HP·Invincible, 서버 HitEvent, 클라 `PlayHitFx` = 붉은 번쩍임 0.12초 + 타격 클립 + 타격음). `SpawnUnit`에 RtsUnitAttackComponent + DamageSkinSettingComponent(스케일 2.4, Blade, 0.08). `RtsSkillFxLogic.PlayClip`(클립 1회 재생) + `assetFacesLeft` 방향 반전(플립북도). `RtsUnitComponent.FaceTo`. 히어로 레이징 블로우 `fx` = 원작 1101011(파이터 레이징 블로우 — swingT3 · effect 클립 2.0배 · use 사운드 · hit/0 클립 · hit 사운드 · hitDelay 0.3 · hitGap 0.12; 09-18 정정: 1121008 자산은 현재 레이징 블로우라 폐기). 새 .codeblock 3개(기존 복제, GUID/Name/Type). character.md 헤더(메인 대상·타격마다 판정·데미지 스킨)·레이징 블로우 항목, 메모리 balance/msw-engine/assets/MEMORY.
- **검증**: Play — 순회 달팽이 사라지고 허수아비 1기, 히어로가 1초마다 swingT3 + 옛 레이징 블로우 참격 이펙트(오른쪽 보기로 반전) → 0.3초 뒤 달팽이 위에 타격 스파크 + 데미지 숫자 **86, 86**(Lv12: 172×50%, 크리 0%) + 번쩍임. 엔진 분할(GetDisplayHitCount 2)로는 84/88·75/97처럼 무작위로 쪼개져 타격마다 따로 판정으로 바꿈. 에러 없음.
- **남은 것**: 레이징 블로우 연출은 260918-1에서 확정. 번쩍임 색, 숫자 위치는 사용자 추가 지시 없음(현행 유지). 그 다음 팔라딘·DK 같은 시험대 → 나머지 직업. 파티 버프 서버 계산, 사거리·타겟 선택(#15 본편), 웨이브(#10)는 별도. 미커밋.

## Change - 260918-1 · 레이징 블로우 연출 확정 — 모션 2개 연결(swingT3→swingTF) + 원작 effect0 몸 덧그림
- **요청**: "다시찾아봐"(옛 레이징 블로우 자산) → "일단 원래대로 돌리자. 모션과 사운드는 처음께 젤 낫네. 캐릭터의 애니메이션은 115713a9… 참고" → "모션이 두개 합쳐져야할듯. 직전껏과 지금꺼 두개 이어봐" → "모션 괜찮아. 이거로 하자"
- **조사**: `*레이징 블로우` 태그 검색 — 현재 라이브러리의 `1121008` 자산은 **레이징 블로우(RED)** 라 어제(260917-6) "옛 레이징 블로우"로 넣은 것은 오류. 레이징 블로우는 A) 파이터 1101011(빅뱅 후 2차: effect `8b26a0cd…` 흰 초승달, effect0 `115713a9…` 캐릭터 실루엣, hit/0 `38e9351c…`, use `f0c0c401…`, hit `6c06fe8a…`) B) 소울마스터 11101008(effect/1 `5c2c13c4…`)만 있음. A/B/C를 `RtsJobTableLogic.FxOverrides["hero:1"]`(런타임 미리보기 훅, `GetSkills` = `GetSkillsRaw` + 덮어쓰기)로 Play 중 비교.
- **변경**: 히어로 레이징 블로우 `fx` 최종 = `motions = {"swingT3","swingTF"}, motionGap 0.4` + 시전음 `f0c0c401…` + `bodyClip 115713a9…`(0초, 아바타 위 정렬 250·유닛 스케일) + 참격 `5c2c13c4…`(`clipDelay 0.4`) + 타격 `hitDelay 0.25, hitGap 0.4`(각 휘두름 임팩트) + 타격 클립 `7d4fd3b7…`/타격음 `d621d7a5…`. `RtsSkillFxLogic`: `PlayMotion`(stand2 경유 1회 액션), `motions`/`motionGap` 연결 재생, `clipDelay`, `PlayBody`(effect0 덧그림, `ActiveBody`). 아바타 swing 액션 길이 실측(body 엔티티 `SpriteAnimPlayerEndFrameEvent`): T1 0.45 / T2 0.44 / T3 0.44 / TF 0.49초 → 0.4초 간격으로 1초 주기에 두 동작이 들어감. character.md 레이징 블로우 항목·메모리 assets·리포트 260917-6 문구 정정.
- **검증**: Play — 에러 없음. 6프레임 연속 스크린샷: swingT3 + 주황 실루엣 → 0.4초 뒤 swingTF + 참격 → 달팽이 위 타격 스파크 + 86/86. 사용자 "모션 괜찮아. 이거로 하자".
- **남은 것**: 팔라딘(디바인 차지)·다크나이트(스피어 버스터 타격 클립) 시험대 → 나머지 8직업 액티브 1개씩. 미커밋.

## Change - 260918-2 · 데미지 스킨 = 메이플스토리 기본 데미지 스킨
- **요청**: "데미지 스킨은 기본 데미지 스킨으로 하자. 메이플 자체의 기본적인 데미지 스킨 있잖아. 지금 데미지 스킨은 너무 인위적이야"
- **변경**: 유닛 `DamageSkinSettingComponent.DamageSkinId = DataRef(RtsCombatLogic.DamageSkinId)`. 1차 = `3271c3e7…`(공식 '범용 리소스 모음 > Basic Damage Skin', effect/damageskin/0) → 사용자 "10000000이 1000만으로 뜨는 (유닛) 스킨 있을 것" → API로는 damageskin 카테고리를 못 세서 처음엔 "없다"고 잘못 답함 → 사용자가 Maker 피커에서 눌러 본 스킨이 로컬 캐시에 떨어져 DXT5 아틀라스를 디코드해 확인: **208번 `7e39645af9454fffb17a5451e9194dda` = 기본 데미지 스킨 (유닛)**(기본 숫자 + 만/억 글리프). 최종 = 208번. 이전은 컴포넌트 기본값 `6ba67548…`(MSW 픽셀 숫자). 배율 2.4 → 2.0. 시험대 전용 `RtsCombatLogic.TestBigHit`(매 공격 뒤 허수아비에 추가 타격 1회, 큰 숫자 표기 확인용) — 확인 뒤 사용자 지시로 0. 사용자 "ㅇㅋ 이거 맞아 굿. 히어로 레이징 블로우는 이거로 끝".
- **검증**: Play — `_DamageSkinService:Play` 미리보기로 `1억2345만6789` 포맷 확인 → 실제 `AttackFrom` 경로(TestBigHit)로 허수아비 위에 **`100만`** 표시, 레이징 블로우 86/86은 그대로. 에러 없음.
- **남은 것**: 미커밋.

## Change - 260918-3 · 팔라딘 디바인 차지 시험대 + 유닛 보는 방향 규칙 수정(기본 왼쪽 보기)
- **요청**: "팔라딘은 그냥 지금 거 그대로 쓰자. 원작 거 ㄴㄴ" → "몬스터는 오른쪽, 캐릭터는 왼쪽 보고 있다가 공격할 때만 오른쪽 보고 끝나면 다시 왼쪽. 마지막 공격 방향 계속 보게" → "공격 이펙트도 반대로 나가네. 바라보는 방향으로. 모든 캐릭 공통"
- **원인**: 메이플 아바타는 **기본이 왼쪽 보기**(스케일 양수 = 왼쪽)인데 `FaceTo`가 스케일 양수 = 오른쪽으로 가정 → 오른쪽 대상에 FaceTo(+1)이 아무것도 안 바꿔 왼쪽을 본 채 공격, 이펙트 반전 판정(`Scale.x >= 0` = 오른쪽)도 뒤집혀 등 뒤로 나감. 공격 중 오른쪽으로 보인 건 swingTF 회전 프레임.
- **변경**: `RtsUnitComponent` — `@Sync FaceDir`(-1 왼쪽 기본 / +1 오른쪽), 서버 `FaceTo`는 FaceDir만 설정, 클라 `ApplyFace`(SetupClient + 0.3초 재시도 + `OnSyncProperty("FaceDir")`)가 **아바타 루트 엔티티 스케일 x = ∓1**로 그림(유닛 엔티티 스케일은 그대로 → 자식 버프 아이콘 안 뒤집힘). 되돌리는 코드 없음 = 마지막 공격 방향 유지. `RtsSkillFxLogic` — `FacingRight(unit)`(FaceDir) + `FlipFor(fx, facingRight)`(assetFacesLeft / 새 `noFlip`) 3곳 공통. 팔라딘 `GetSkillsRaw("paladin")[1].fx` = swingTF + `cb9cff6c…`(1221004/effect/1, 스케일 1.4, assetFacesLeft) + `e2989dca…`(1221004/use), hitDelay 0.3, 타격 클립 없음(character.md 값 그대로). `RtsCombatLogic.UnitNo = 2`(시험대 유닛 선택). `maker_execute_script` 서버 실행은 `context="server_main"`.
- **검증**: Play — 팔라딘(Lv40) (13,3)에서 오른쪽 허수아비를 보고 1.25초마다 디바인 차지: 무기 빛(뒤) → 문양 폭발(앞, 허수아비 위) → **1128**(470×200%×1.2). 공격 뒤에도 오른쪽 유지. 히어로도 서버 루프로 붙여 확인 — 오른쪽을 보며 참격·타격 스파크가 앞으로. 에러 없음.
- **남은 것**: 다크나이트 스피어 버스터(타격 클립) 시험대 → 나머지 8직업. 미커밋.

## Change - 260918-4 · 팔라딘 생츄어리 연출 등록 + 쿨타임 스킬 우선 사용 규칙
- **요청**: "팔라딘 스킬 하나 더 있었지?" → "옛날 스킬 찾을 필요 없어(레이징 블로우·스피어 버스터만). 생츄어리는 이미 정했잖아. 타격 이펙트만 보려고"
- **변경**: `GetSkillsRaw("paladin")[3]` 생츄어리 = character.md 값 그대로(swingT1 + `d577178a…` 1221011/effect 스케일 1.2 + `aa96c111…` use / hitDelay 0.5, `5df303c3…` 1221011/hit/0 스케일 1.6 + `2cc05078…` hit) + `cd = 15, ratio = 100, hits = 1`. `RtsCombatLogic.DoAttack`: 액티브를 뒤에서부터 보며 **쿨타임 스킬(cd)은 준비됐으면 기본 공격보다 우선**(`ReadyAt[user_no_idx]`, `_UtilLogic.ServerElapsedSeconds`), 스킬별 `ratio`/`hits`로 1회 타격 = atk × 공격력% × 비율 × 최종. `RtsSkillFxLogic.Preload`가 clip·bodyClip·hitClip도 미리 올리고, `RtsUnitComponent.SetupClient`가 그 직업 스킬 fx 전부를 등장 시 Preload(생츄어리 첫 재생 0.6초 로딩 대비).
- **검증**: Play — 팔라딘 첫 공격이 생츄어리(swingT1 + 하늘 망치 클립, 564 = 1128×½), 이후 디바인 차지 1128, 15초 뒤 다시 생츄어리(`ReadyAt` 서버 확인). 타격 이펙트 = 달팽이 둘레 흰 반투명 파동 링 — 은은해서 사용자 확인 대기. 에러 없음.
- **남은 것**: 생츄어리 타격 링 강도(스케일/다른 클립) 사용자 판단 → 다크나이트. 미커밋.

## Change - 260918-5 · 다크나이트 시험대 — 스피어 버스터 방향·타격 간격 + 드래곤 로어 등록
- **요청**: "이제 다크나이트 가자"
- **변경**: `RtsCombatLogic.UnitNo = 3`. 스피어 버스터 fx에 `assetFacesLeft`(영상 캐릭터가 왼쪽 보기 — 용 머리가 앞으로 발사, 날개는 등 뒤) + `hitDelay 0.3, hitGap 0.15`(3회). 드래곤 로어 = character.md 값 등록(swingT3 + `5468cadd…` 9001006/effect 스케일 1.5, clipLife 1.4 + `eec2f5d3…` use / hitDelay 0.6, `01c80353…` 9001006/hit/0 스케일 1.6) + `cd = 10, ratio = 300, hits = 1, lock = 1`. 1회 타격 내림에 +0.0001(340×2×0.7 = 475.999… → 475로 깎이던 것 → 476).
- **검증**: Play — DK(Lv20) (13,3): 오른쪽을 보고 1.25초마다 스피어 버스터 476×3, 파란 용 머리가 허수아비 쪽으로. 서버에서 Lv50으로 올려 드래곤 로어 순환 확인(`ReadyAt … _3_5`), 클라 미리보기 루프로 보라 마법진 + 허수아비 위 타격 스파크. 에러 없음.
- **무기 교체(사용자 "다크나이트만 리버스로 — 이펙트 때문에")**: 세트 캐시 창 `acd581b7…`의 빨간 두손검 잔상이 스피어 버스터와 겹쳐 `GetCostume("dk").weapon2h = 164067c8…`(타임리스 알슈피스, afterImage spear). 리버스 창(로렌티우스)은 라이브러리에 없음(`*리버스` = 니플하임·벨로체·타바르진·블랙뷰티·부츠). Play 확인: 금색 창, 빨간 참격 사라짐, 용 머리 발사만 남음.
- **남은 것**: 전사 3직업 시험대 완료 → 나머지 8직업(외형 완료, 액티브 fx 미등록: `GetSkillsRaw` 기본 "(미정)"). 미커밋.

## Change - 260918-6 · 보우마스터 폭풍의 시 — 0.2초 주기·투사체·루프 모션
- **요청**: "이제 보우마스터 가자"
- **변경**: `GetStatRaw("bow")`(pct 100+5+5, ratio 50→75(L50), 1회·1마리, crit +30(L10), `period = 0.2`) + `GetPeriod(st)`(period 있으면 공격속도 무관 — CalcStat·StartLoop·DemoLoop 공통). `GetSkillsRaw("bow")` 6종 등록, 폭풍의 시 fx = `motion shoot1 + motionLoop`(공격 중 같은 자세 유지, `LoopMotion[no]`), 시전음 3121004/use, **투사체** `proj` 3121020/ball(`PlayProjectile`: 손 높이 → 대상, `_TweenLogic:MoveTo` 0.15초, 방향 반전), hitDelay 0.15 + 3121020/hit/0 + 3121004/hit. `CastFx(zone,no,idx,targetName)`로 대상 전달. 시범 유닛 4 = 보우마스터 Lv30 (4,6), `UnitNo = 4`.
- **검증**: Play — 보우마스터 (13,3)에서 0.2초마다 176(크리 211) — 활 당긴 자세 유지, 달팽이 위 노란 별 스파크. 에러 없음. 세트 캐시 활(cashweapon49)의 파란 폭발 잔상이 발마다 겹침 → 사용자 판단 대기.
- **추가(사용자 "폭풍의 시 이펙트도 공격 중일 때 계속")**: `fx.loopClip`(3121020/keydown 바람 소용돌이) — `EnsureLoopFx`가 첫 시전에 유닛 위에 루프 클립을 띄우고 시전마다 시각 갱신, 감시 타이머(0.25초)가 `LoopTimeout` 0.6초 동안 시전이 없으면 이펙트 제거 + 유지 자세(motionLoop)도 stand2로. 스케일 1.6은 캐릭터를 가려 1.2·`loopAlpha` 0.75. 확인: "shoot1 유지"는 대기(stand2)와 나란히 찍어 자세 차이 확인(활을 앞에 세워 당김).
- **활 교체(사용자 "파란색 저게 무기 이펙트인가? 타임리스로 변경")**: `GetCostume("bow").weapon2h = 9e8fe977…`(타임리스 엔가우, afterImage bow). 파란 폭발 = 세트 캐시 활(cashweapon49)의 잔상이었음.
- **버그 수정(사용자 "월드 아바타로 교체했더니 모자가 깃털 모자")**: `RtsUnitComponent.ApplyLook` Skin 1(월드 아바타) 분기가 Cap·FaceAccessory·Face 커스텀을 비우지 않아 세트 모자가 남았음 → 세 슬롯도 "" 로. 확인: 보우마스터 Skin 1 → 유저 본인 아바타(보라 뿔 모자) + 타임리스 활.
- **방향 수정(사용자 "폭풍의 시 이펙트 반대로 나오는데?" / "스킬 이펙트나 모션 등 전부 방향 신경써")**: keydown 클립은 같은 폴더의 effect/ball과 그림 방향이 반대 → `fx.loopAssetFacesLeft`(루프 클립 전용 방향 규칙) 추가, 보우마스터 false. 이후 연출 등록 시 좌우 양방향 스크린샷 확인을 규칙으로(메모리 workflow).
- **남은 것**: 신궁. 미커밋.

## Change - 260918-7 · 신궁 피어싱·스나이핑 + 요소별 이펙트 방향 옵션
- **요청**: "신궁으로 가자. 모든 캐릭터 만든 후에 실제 라운드 테스트" → (피어싱 시전 이펙트를 내가 한 번 뒤집어 넣었다 되돌림) "너 왜 자꾸 공격 이펙트 반대로 넣어서…" → "이펙트가 캐릭터랑 너무 겹친다. 조금 더 떨어져야함"
- **변경**: `GetStatRaw("marks")`(atk 50+15/Lv, pct 120(L40), 30%×3→50%×4(L50), 6마리, 느림, crit +30(L10)), `GetSkillsRaw("marks")` 6종: 피어싱 fx = shoot2 + 3221017/effect(스케일 1.2, `feetDx -0.6` 앞쪽) + 3221001/use + ball 1923e540… 0.2초 + hit/3 + 3221001/hit(3회 0.12초); 스나이핑 = `cd 10, ratio 50, hits 10` + 3221007 effect/ball/hit/use/hit(10회 0.08초). `RtsSkillFxLogic.FlipFor(fx, facingRight, which)` — `clipFacesLeft/framesFacesLeft/bodyFacesLeft/loopFacesLeft/projFacesLeft`가 `assetFacesLeft`보다 우선(폭풍의 시 `loopFacesLeft=false`로 이전 옵션 대체). 시범 유닛 5 = 신궁 Lv30 (5,6), `UnitNo = 5`.
- **방향 확인 절차(재발 방지)**: 캐시 `.win.mod`의 프레임 GUID → CDN 64px 썸네일 시트로 클립 그림 방향을 **등록 전에** 확인(피어싱 effect = 촉 왼쪽·날개 오른쪽 = 왼쪽 보기 → 기본 규칙 그대로가 맞았고, 내가 스크린샷만 보고 뒤집은 것이 오답). 메모리 workflow에 방법 기록.
- **검증**: Play — 신궁 (13,3): 피어싱 145×3(크리 174), 화살이 허수아비를 관통해 오른쪽으로, 시전 폭발은 석궁 앞(캐릭터와 분리) + 스나이핑 242×10(첫 공격, 10초 쿨). 에러 없음.
- **남은 것**: 마법사 3직업(썬콜·불독·비숍) → 도적 2 → 팬텀 → 4직업 왼쪽 보기 점검 → 라운드 테스트. 미커밋.

## Change - 260918-8 · 투사체 비행 방향 회전(대각선)
- **요청**: "투사체 날아가는 건 가로/세로만 되고 대각선은 안 되는 거야? 보마·신궁·나로·팬텀 공격이 너무 일직선"
- **변경**: `RtsSkillFxLogic.PlayProjectile` — 출발점→대상 각도(`AngleDeg`, atan 직접 계산)를 `TransformComponent.ZRotation`에. 오른쪽으로 갈 땐 FlipX 뒤 각도 그대로, 왼쪽으로 갈 땐 반전 없이 각도−180(위아래가 뒤집히지 않게). `fx.projNoRotate`로 끌 수 있음. 시험대 유닛 칸을 (13,4)로 내려 허수아비(14,3)가 대각선 위가 되게 함(`UnitRow = 4`).
- **검증**: Play — 신궁 피어싱 화살이 우상향 45°로 회전해 허수아비까지 비행, 유닛은 오른쪽 보기 유지, 타격 145. 에러 없음.
- **남은 것**: 포물선(살짝 뜨는 궤적)은 필요하면 추가. 마법사 3직업. 미커밋.

## Change - 260918-9 · 스나이핑 = 대상 표식(화살 없음)
- **요청**: "30caa285… 스나이핑은 화살 날아가는 게 아니고 대상 몬스터에게 이 표식이 뜨면서 데미지"
- **변경**: `fx.markClip·markScale·markDy·markLife·markLoop` + `RtsSkillFxLogic.PlayMark`(시전 순간 대상 위 클립 1회, 정렬 330). 스나이핑 = `markClip 0c76a3bd…`(3221007/mob 조준 표식, 1.8, +0.3), `proj` 제거. Preload에 markClip 포함. 확인 중 발견: 2024년 이후 'model' 형식 리소스(30caa285…, 0c76a3bd…)는 첫 표시까지 수 초 걸림 → 유닛 등장 시 Preload가 필수.
- **검증**: Play 미리보기 — 시전 시 달팽이 위 황금 조준 표식 → 0.4초 뒤 242×10. 에러 없음.
- **추가(사용자 "표식은 몬스터 정중앙, 커져도 다 감싸게")**: `PlayMark`가 대상 `HitComponent`(ColliderOffset×스케일 = 중심, BoxSize×스케일 = 크기)로 위치·크기를 정함 — `markFit`(박스 긴 쪽 배수, 1.5) + `markPivotDy`(클립 원점이 아래라 그림이 위로 뜨는 것 보정, 0.36×스케일). 허수아비 피격 박스를 스프라이트에 맞게 축소(BoxSize 1.0×0.8 → 0.48×0.4, 오프셋 0.3 → 0.2 — 이전엔 달팽이의 두 배). 확인: 표식이 달팽이를 정중앙에서 감쌈.
- **남은 것**: 마법사 3직업. 미커밋.

## Change - 260918-10 · 마법사 3직업 연출(썬콜·불독·비숍) + 새 연출 장치(빔·대상 클립·구체·지대·지속 피해·빙결)
- **요청**: "신궁으로 가자… 모든 캐릭터 만든 후에 실제 라운드 테스트" 흐름의 마법사 차례.
- **변경**: `RtsJobTableLogic` — `GetStatRaw`/`GetSkillsRaw`에 il·fp·bishop(캐릭터.md 값 그대로: 썬콜 50+3/Lv 체인 100%×1→2 L20 10마리, 블리자드 cd15 15마리 빙결 1초; 불독 20+5/Lv 포이즌 리전 dot 10%/2초×10초(강화 15%·방무 100) + 도트 퍼니셔 구체 10; 비숍 20+5/Lv 엔젤레이 80%·제네시스 cd15). `RtsSkillFxLogic` — `beam*`(유닛→대상들 차례로 잇는 조각 빔), `markClips/markAt "feet"/markDelay`(대상 발 위 클립), `projCount/projStagger/projFrom "around"/projLife/projEach`(구체 여러 개), `zoneClips*`(구역 트랙 65칸 지대), `backClip*`(아바타 뒤 190), `StandName`(한손 무기 stand1). `RtsCombatLogic` — `dot` 서버 틱, `freeze`, `GetZoneMonsters`. `RtsMonsterComponent.Zone`. 시범 유닛 6·7·8 = il·fp·bishop Lv30(9,5)(10,5)(10,9), 시험대 UnitNo 6.
- **검증**: Play — 체인 라이트닝 187, 블리자드 187, 포이즌 리전 틱 32(215×15%) 5회·독안개 65칸 10초, 도트 퍼니셔 215×10, 엔젤레이 172, 제네시스 215. 빌드 에러 없음.
- **원점 실측**: MSW는 원작 클립 프레임을 (ox, oy-바닥) 원점으로 그린다 → 블리자드 tile이 위로 떠 보인 원인. 프레임 시간은 .win.mod field 2.

## Change - 260918-11 · 다수 몬스터 시험대 + 타겟 선택(#15 첫 조각) + 후딜·빙결·체력바·대기 자세
- **요청**: "몬스터 여러 마리로 테스트… 우측 위/아래 2마리 더" / "생츄어리·블리자드·제네시스·드래곤 로어 후딜 1.5초" / "빙결 표시 우측 위 + 파랗게" / "몬스터 체력바, 크기 통일(보스만 길게)" / "썬콜이 스킬 뒤 두손 모션으로 돌아간다" / "도트 퍼니셔 구체는 캐릭터 주변에 골고루 생성돼 가장 가까운 적에게, 보스 우선(도트 퍼니셔만)".
- **변경**: `RtsCombatLogic` — 허수아비 3기(14,2)(14,3)(14,4)(`DummyExtra`), `PickTargets`(체비셰프 칸 거리 ≤ range+0.25, 가까운 순 n), `DoAttack(userId, no)`가 스킬마다 대상 유무를 보고 고름(쿨 스킬은 대상 있을 때만 쿨 소모), `CastFx(zone, no, idx, namesCsv)` 대상 전부 전달, 타격은 대상마다(`spread`면 구체별 대상 — 유닛 주위 36° 간격 지점에서 가장 가까운 적, 보스 있으면 보스만), `BusyUntil`(after). `RtsMonsterComponent` — 체력바(흰 사각 Scale, 세계 1.4×0.12·보스 2.6, 부모 스케일 나눔) · 빙결(`FrozenUntil` @Sync, 틴트 0.55/0.8/1 + 우측 위 아이콘 2221007/icon) · `IsBoss`. `RtsSkillFxLogic` — `PlayCast(…, targets)`, 빔 체인·표식 대상마다·구체 대상 분배, `StandName`. 스킬 표에 `range/targets/after/freeze/spread` 기입(레이징 블로우 1, 디바인 차지 1, 생츄어리 4/15, 스피어 버스터 1, 드래곤 로어 5/15, 폭풍의 시 3, 피어싱 3(projEach), 스나이핑 6/1, 체인 2, 블리자드 6/15, 도트 퍼니셔 6/10, 엔젤레이 3, 제네시스 6/15). 데미지 숫자 시작 1.35(체력바 위).
- **검증**: Play — 체인 라이트닝이 3기를 차례로 잇고 187×3, 도트 퍼니셔 215 분배, 포이즌 틱 32×3, 빙결 아이콘·틴트·체력바 표시(슬로모 미리보기). 빌드 에러 없음.
- **남은 것**: 블리자드 시전 이펙트 사용자 재검토("등 뒤는 이상, 옛날 블리자드 같은 게…" — 현재 2221012 결정 감싸기 + 아이스 스트라이크 기둥, 후보 시트 전달) / 도적 2·팬텀 / 왼쪽 보기 전수 확인 / 불독 표 DPS(지속 피해) / 미커밋.

## Change - 260918-12 · 블리자드 = skill/80003323 세트(사용자 지정) + 빙결 눈꽃 + 시전→타격 순서
- **요청**: "타격 이펙트는 772691a0…, 등 뒤 이펙트는 96b26165…로" → "skill/80003323으로 검색하니 세트가 나오네, 타격도 이거에 맞게" / "시전음·타격음도 있으면" / "빙결 이펙트는 21628ca1…" / "캐릭터 이펙트 종료 직전 → 타격 → 타격 이펙트 끝 → 캐릭터 이펙트 종료".
- **변경**: 블리자드 fx = `backClip 96b26165…`(80003323/effect 3.0초, 아바타 뒤 −10 — 아바타 Body/Face가 Default order 0임을 실측해 PlayBack 190 → −10) + `markClips {735ad75a…}`(80003323/hit/0 낙하 얼음, markDelay 0.5 → 착지 2.18초) + `hitDelay 2.2`, 타격 클립 없음, `after 3.0`(연출 3초를 덮음). 2221012 결정 감싸기·아이스 스트라이크 기둥 제거. 세트 사운드는 라이브러리에 없어 2221007 use/hit 유지. 빙결 표시 = `RtsMonsterComponent.FreezeIconRUID` 21628ca1…(21001008/mob 눈꽃 루프, 로컬 0.65).
- **검증**: 슬로모 미리보기 — 군집이 캐릭터 뒤에서 솟고(캐릭터 가려지지 않음), 3기 위 고리 → 낙하, 눈꽃 3개·틴트. 실제 루프에서 체인 라이트닝 썬더볼트 3연타 187 확인. 빌드·런타임 에러 없음.
- **확정**: 타격 얼음 스케일 0.7 → 0.95 → 1.5 → **2.0**(사용자 "2가 딱 좋네, 썬콜은 이거로 끝" 2026-09-18). 시험대 UnitNo 7(불독)로.
- **남은 것**: 불독·비숍 사용자 확인 → 도적 2·팬텀 → 왼쪽 보기 전수 → 실제 라운드 테스트. 미커밋.

## Change - 260918-13 · 도트 퍼니셔 재설계 — 생성·호버 → 느린 추적 → 박치기
- **요청**: "구체는 저거로. 사운드 시작 → 불구슬이 캐릭터 주위에 넓게 생성 / 사운드 끝 → 주변 적을 탐색해 느리게 추적, 부딪히며 판정" → "날아갈 때 접시처럼 깨져 있다" → "불구슬이 몬스터 중앙에 박치기하며 사라지는 것, 주변에서 터지면 안 됨" / 사운드 = 400021001 use·use2(5차 도트 퍼니셔 — 이 ID엔 클립 없음).
- **변경**: `RtsJobTableLogic.OrbSpawnOffset(i, n, fx)`(공용 생성 오프셋: 36°씩 + 황금비 반지름 흩뿌림). `RtsSkillFxLogic.SpawnProjectile` — `projHover`(떠 있기), `projSpeed`(거리÷속도 비행), `projFlySprites`(프레임 sprite 직접 루프 — 클립 StartFrameIndex/EndFrameIndex가 이 클립에 안 먹음, 실측), `projHitSprites`(선택, 미사용), 도착점 = 피격 박스 중앙, 도착 즉시 제거, 타이머 누수 정리(LEA-3051 경고 수정). `RtsCombatLogic.DoAttack` — 구체별 도착 시각 `orbDelay`로 판정 예약(stagger + hover + 거리÷속도). 도트 퍼니셔 fx: projSpread 2.4, projHover 1.2, projSpeed 2.2, 타격 클립 없음, 사운드 use/use2.
- **검증**: 슬로모·실시간 스크린샷 — 시전 중 불덩이 9~10개가 캐릭터 주위 고리로 떠 있고, 사운드 끝에 각자 가장 가까운 달팽이로 날아가 중앙에서 사라짐, 215 표시. 빌드·런타임 에러 없음(누수 경고는 수정 뒤 재확인 예정).
- **남은 것**: 사용자 확인 → 비숍 확인 → 도적 2·팬텀 → 왼쪽 보기 전수 → 실제 라운드 테스트. 미커밋.

## Change - 260918-14 · 도트 퍼니셔 확정 — 아이콘 컷 불구슬·회전·2배 속도·박치기 폭발·30개·동심원 간격
- **요청**: "불구슬 이펙트 전부 나열" → 아이콘 `d998c591…`/`20a64945…` 지정 → "더 키우고 회전" → "속도 2배 + 달라붙으면 폭발" → "30개(증강으로 개수 늘릴 대비)" → "캐릭터와도 서로도 최소 자기 크기 간격" → "불독 OK".
- **변경**: 자체 업로드 sprite RtsDotOrb01~03(`3769c672…`·`b0b300d3…`·`da5ad791…`, assets/textures/dotorb/ — 스킬 아이콘을 원형 컷) `projFlySprites` 0.12초 맥동, 1.8배, `projSpin` 240°/초(구체마다 방향 엇갈림), `projSpeed` 4.4, 박치기 = 12121055 hit/0 0.7배 + use2, hits/projCount 30, `OrbSpawnOffset` = 동심원 고리 채우기(projSpread 2.0 = 안쪽 반지름, projGap 1.2 = 구체·고리 간격). 시험대 UnitNo 1(히어로)로.
- **검증**: 홀드 미리보기 — 30개가 10·16·4 고리로 간격 있게 배치, 날아가 중앙에서 폭발, 215 표시. 정지 시 LEA-3051(비행 중이던 구체 타이머) 경고는 Play 종료 시점 잔여라 무해.
- **남은 것**: 히어로 재점검(사용자 "히어로로 다시 돌아와보자") → 비숍 확인 → 도적 2·팬텀 → 왼쪽 보기 전수 → 실제 라운드 테스트. 도트 퍼니셔 30개 × 100% 수치 조정은 사용자 결정 대기. 미커밋.

## Change - 260919-1 · 히어로 = 레이징 블로우(레이징 블로우 교체) + 맨몸 덧그림 제거 + 유닛 팝업 능력치 정리
- **요청**: "히어로 레이징 블로우 자세에서 발가벗은 캐릭터가 겹치는데 없애줘" → "UI에서 기본공격/보스DPS/몬스터DPS 싹다 제거, 최종데미지 +만 표시, 크리티컬 확률/데미지 2줄 총합만" → "공격력도 총합만, 공격력%는 +합, 공격속도는 보통 이렇게만" → "레이징 블로우 스킬 변경. 애니메이션 fa2bfe8f… 사운드 d621d7a5… 스킬명 레이징 블로우" (+ 프리즘 강화판 1120017 자산 조사 "사운드가 안보임").
- **변경**: (1) 레이징 블로우 fx의 `bodyClip`(1101011/effect0 — 원작 캐릭터 실루엣 클립이 맨몸으로 아바타 위에 겹쳐 보임) 제거. (2) `RtsUnitPopupLogic` 능력치 7줄(공격속도 등급 / 공격력 총합 / 공격력 % `+n%` / 방무 / 최종 데미지 `+n%` / 크리 확률 / 크리 데미지), 기본 공격·보스 DPS·몬스터 DPS·구분선 삭제, 패널 높이 260. (3) 히어로 1레벨 액티브 → **레이징 블로우**: 클립 `fa2bfe8f…`(1121008/effect/2, 14fr 0.78s) 시전과 동시에, 모션 swingT3→swingTF 0.5s, 판정 0.3/0.6s, 시전음 `d621d7a5…`를 새 옵션 `soundDelay` 0.24s로 초승달 시작에 1회(hitSound 없음), 타격 클립 7d4fd3b7 유지; Lv40 패시브도 '레이징 블로우 강화'. `.info` 4형제·메모리 이름 갱신. (4) 1120017 조사: effect/0~3(13fr 0.78s 불꽃 참격, 인레이지판)·hit/0~4, 오디오는 `sound/skill/1120017/hit` `aa92fddf…`(0.47s)만 — use 없음 → augmentation.md 프리즘 항목에 기록.
- **검증**: 재생 후 시험대 — 레이징 블로우 자세에 맨몸 없음(스크린샷 3장), 팝업 7줄 표시(+20% ▲, 20% ▲, 40% ▲), 레이징 블로우 초승달·수평 참격이 대상(오른쪽) 방향으로 나가며 86×2 표시. 빌드 로그 오류 없음. 왼쪽 보기는 시험대에서 미확인(반전 규칙은 이전 클립과 동일 assetFacesLeft).
- **배운 것**: Play 중 고친 `.mlua`는 `maker_stop → maker_refresh_workspace → maker_save → maker_play` 순이어야 반영(refresh 없으면 옛 스크립트로 실행 — workflow 메모리에 기록).
- **남은 것**: 히어로 재점검 계속(사용자 관찰 대기) → 비숍 확인 → 도적 2·팬텀 → 왼쪽 보기 전수 → 실제 라운드 테스트. 프리즘 '레이징 블로우' 문구 정리는 사용자. 미커밋.

## Change - 260919-2 · 범위 공격 = 메인 대상 곁 1칸(체인 3) + 레이징 블로우 2타 찌르기 + motion.md
- **요청**: "메인 대상 가까운 기준 사거리 범위 1 이내로, 체인 라이트닝은 3" → "달팽이 3마리가 줄지어 와도 트랙이 2칸 벌어지면 사거리 안이라도 안 맞음" → "도트 퍼니셔는 예외, 사거리 제한 없이 구체마다 가장 가까운 적" / "두 번째 모션은 찌르기로" / "모션 종류 모두 motion.md로" / "레이징 블로우 이전 이름은 어디에도 남기지 마라".
- **변경**: `RtsCombatLogic.PickTargets(unit, zone, range, n, aoe)` — 메인 대상 = 사거리 안 가장 가까운 1마리, 나머지 = 메인 곁 aoe칸(+0.25) 안에서 직전 대상과 가장 가까운 순으로 이어 n마리(빔·타격 순서가 한 줄). 모든 범위 공격 aoe 1, 체인 라이트닝 `aoe = 3`, 지대(dot)·구체(spread) 스킬은 range/count 999 + aoe nil(구역 전체, 도트 퍼니셔 구체는 각자 가장 가까운 적). 레이징 블로우 motions `swingT3 → stabT1`(0.5s). `.info/motion.md` 신설(35 액션 설명 + `.info/artifacts/motion/{basic,swing,stab_shoot}.png` 캡처 시트). 이전 스킬 이름은 `.info`·코드 주석·메모리·리포트·로드맵·hud-layout에서 전부 치환/삭제.
- **검증**: 재생 후 시험대 — 허수아비 3기 중 메인(14,4)+곁 1칸(14,3) 2기만 86 표시(14,2 제외), 찌르기 2타 재생. 빌드·런타임 오류 없음.
- **배운 것**: `ActionStateChangedEvent(name, name, playRate, Onetime)`의 세 번째 인자로 액션을 0.1배속 재생해 스크린샷 1장으로 자세를 잡을 수 있다; stand 이벤트와 같은 프레임에 보내면 가끔 무시 → 0.2s 뒤 전송. Play 화면을 멈추는 작업은 먼저 알리고 끝나면 즉시 복구(사용자 지적).
- **남은 것**: 사용자 화면 확인(찌르기 타이밍·범위 체감) → 비숍 확인 → 도적 2·팬텀 → 왼쪽 보기 전수 → 실제 라운드 테스트. 미커밋.

## Change - 260919-3 · 모션 싱크 — stand 경유 제거 + 모션 끝난 뒤 stand 복귀
- **요청**: "레이징 블로우 시작할 때 스킬 애니메이션이 먼저 나오고 캐릭터가 늦게 따라가서 싱크가 안 맞아. 팔이 여러 개인 것처럼 모션이 겹쳐 보임".
- **원인**: `PlayMotion`이 매번 stand → 액션을 같은 프레임에 보냄(같은 액션 반복 재생용) → 두 번째 이벤트가 한 프레임 늦거나 무시(캡처 실측). 클립 종료(0.78초)에 stand 강제 복귀 → 0.5초에 시작한 2타 stabT1(≈0.95초)이 잘림.
- **변경**: `RtsSkillFxLogic` — `LastMotion[body.Id]`·`MotionUntil[body.Id]` 추가. 다른 액션에서 넘어올 땐 바로 보내고 같은 액션 반복일 때만 stand → 0.05초 뒤 액션. `ReturnStand(body, stand)` = 모션이 남아 있으면 끝나는 시각에 복귀(클립·플립북 종료 경로 3곳 교체). motionLoop(폭풍의 시) 경로도 같은 규칙.
- **검증**: 빌드 오류 없음, 시험대 재생 중 — 사용자 육안 확인 대기.
- **남은 것**: 사용자 확인 → 비숍 확인 → 도적 2·팬텀 → 왼쪽 보기 전수 → 실제 라운드 테스트. 미커밋.

## Change - 260919-4 · 레이징 블로우 확정 — 모션 하나를 늘려 싱크 + 무기 숨김(hideWeapon)
- **요청**: 영상 제보 "스킬 시작 전 자세 이상 / 두 번째 베기 없음 / 싱크 안 맞음" → "첫 모션만 늘려서 애니메이션과 싱크" → "초승달 안 어울림" → "칼이 위에서 시작하는 모션은 안 맞음" → "기본 칼이 애니메이션에 가려지는 게 맞다" → "지금 딱 좋아".
- **원인(영상 프레임 분석 + 팔라딘 실측)**: 같은 아바타 액션은 끝난 뒤 다시 보내도 재생되지 않음 → stand 경유 필수, 간격 0.05초는 무시(두 번째 swing 누락). 공격 뒤 stand 복귀가 다음 공격과 겹쳐 안 보내져 alert 자세로 대기. 원작 이펙트에 금색 대검이 들어 있어 캐릭터 검이 옆에 따로 보임.
- **변경**: `PlayMotion(body, name, stand, rate)` — 다른 액션이면 즉시, 같은 액션이면 stand→0.15초; 액션 길이(0.45÷rate) 뒤 `ReturnStand`로 항상 stand 복귀 → 다음 공격 지연 0. `fx.motionRate`(ActionStateChangedEvent playRate). `fx.hideWeapon/hideWeaponSec` → `HideWeapon`: `SetAvatarPartColor(무기 카테고리, alpha 0)` + `ShowDefaultWeaponEffects=false`, 연속 공격 중 유지·끊기면 복구(`HideTimer`). 레이징 블로우 = swingO3 ×0.58(0.78초 = 클립), 클립 동시 시작, hideWeapon 0.85, 판정 0.4/0.65, 사운드 0.24.
- **검증**: 스크린샷 — 시전 중 캐릭터 검 없음, 이펙트 대검이 앞에, 86×2. 사용자 육안 확정.
- **남은 것**: 비숍 확인 → 도적 2·팬텀 → 왼쪽 보기 전수 → 실제 라운드 테스트. 미커밋.

## Change - 260919-5 · 전체 광역기 랜덤 타겟 + 제네시스 크기 + 다크나이트 스피어 버스터 80003291 확정
- **요청**: "비숍 확인" → "제네시스 빛기둥 넓이 2배, 여신 이펙트 1.5배(썬콜과 비슷하게)" → "제네시스/생츄어리/블리자드/드래곤 로어는 전체 광역기 — 메인 타겟 없이 사거리 안 n마리 랜덤" → "다크나이트 스피어 버스터 = skill/80003291" → "이거로 완전 종결".
- **변경**: `PickTargets(…, aoe, randomPick)` + 스킬 `area = true`(4개) → 사거리 안 후보 피셔-예이츠 셔플 n마리. 제네시스 `scale 1.4→2.1`, `markScaleX = 2`(새 옵션, 가로만 배율). 스피어 버스터 fx = 80003291 세트(clip 오라 + `clips` 4개 + hit/0, `motionDelay 0.5`, 판정 0.65/0.15×3, 소리 기존 유지). 새 fx 옵션 `clips`(항목 dx/dy/scale/delay/life)·`motionDelay`·`clipHold`·`markScaleX`. 시험대 기본 유닛 3(다크나이트).
- **검증**: 스크린샷 — 오라·용머리·찌르기 타격 476×2 확인. 사용자 확정.
- **남은 것**: 나이트로드·섀도어·팬텀 → 왼쪽 보기 전수 → 실제 라운드 테스트. 미커밋.

## Change - 260919-6 · 밸런스 패치(10직업 스킬 수치·설명) + 관전 읽기 전용 규칙 메모
- **요청**: "스킬 변경 좀 해야겠다. 설명 변경 및 밸런스 패치" — 히어로·팔라딘·DK·보우·신궁·썬콜·불독·비숍·나로·섀도어 10직업 목록. 별건: 타 유저 구역 보기 = 읽기 전용 규칙(메모리에만).
- **변경(코드, 8직업)**: `RtsJobTableLogic.GetSkillsRaw` 설명 22곳 + `GetStatRaw` 8직업 계수(히어로 ign 40=10·L50 pct +30 / 팔라딘 ratio 120→160·fin 150 / 보우 ratio 40→55·pct +25×2 / 신궁 hits 2·pct 170 / 썬콜 flat 150·ratio 130·pct 150→250·fin 삭제 / 불독 dotPct 15→30·dotIgn 100 기본·flat 100·pct 150·fin 120 / 비숍 ratio 30·hits 3·flat 100·pct 150·fin 120) + 스킬 표(생츄어리 200·로어 cd 15·블리자드 300/freeze 5·제네시스 300·포이즌 dot 15). `RtsUnitBuffLogic` 프레이 scope all·fin 10. 나로·섀도어는 코드 미등록이라 문서만.
- **변경(문서)**: `.info/character.md` 설명 줄마다 "(2026-09-19: 이전 → 새 값)" 표기, 섀도어 공격속도·스킬 구조(대거 부스터 삭제·대거 마스터리 10레벨·레디 투 다이 50), 나로 쿼드러플 스로우. `.info/balance-detail.md` 표 전부 재생성(scratchpad `balcalc.py` — old 모드로 기존 표 100% 재현 확인 후 new), 헤더·특성표·사거리 평가·메모 갱신, 증강 반영 절엔 '패치 전 값' 표시. `damage.md` 프레이 규칙, `augmentation.md` 트리플→쿼드러플·신성 강림/블리자드 프리즘 정리 필요 표시.
- **검증**: 재생 빌드 오류 없음(다크나이트 시험대). 수치 표: 50레벨 보스 DPS 히어로 2,888 / 팔라딘 2,188 / DK 2,688 / 보우 2,574 / 신궁 1,281 / 썬콜 1,127 / 비숍 591 / 나로 913 / 섀도어 3,019.
- **해석(사용자 확인 필요)**: 나로 자벨린 마스터리(10) = 공격력 +50을 최종 +5%로 교체 / 프레이 '모든 유닛' = 자신 포함 / 디바인 차지 강화의 사거리 2·6마리·2회 유지 / 새비지 블로우 강화(40) 20% 유지 / 엔젤레이 3회는 투사체 1발에 3판정(연출 미조정).
- **2차(사용자 확인)**: 해석 1·2·5 확정. 강화 스킬 설명은 '+n%'만 표기(디바인 차지 강화·폭풍의 시 강화·포이즌 리전 강화 — 고정 %처럼 보이지 않게, 증강 합연산). 나로: 다크 세레니티 제거, 자벨린 마스터리(최종 +10%·+100) 40레벨, 레디 투 다이(최종 +20%) 50 신규 → 50레벨 보스 DPS 918.
- **3차(사용자 추가)**: DK 비홀더 강화(공격속도 보통) 제거 → 스피어 버스터 강화(40) +30%(공격속도 끝까지 느림, 50레벨 보스 DPS 2,688 → 3,072) / 신궁 피어싱 강화 = 데미지 +50%만(사거리 4 삭제 → 2,049) / 썬콜 인피니티 공격력 +50%(→ 902) / 불독 인피니티 최종 +30% / 나로 자벨린(10) 최종 +10%(→ 962) / 섀도어 새비지 강화 제거 → 대거 익스퍼트(40) +20%·최종 +5%(→ 1,828) / 팬텀 조커 150%·날카로운 검 +3%(코드 buff fin 3)·문라이트/프레이 오브 아리아 +150·+10%·케인 익스퍼트 최종 +10%·블스아이 크확 +50·크뎀 +30·방무·보스 +50·최종 +20(→ 9,177). 레이징 블로우 강화 설명 '+50%'로. 팬텀 모델을 balcalc에 추가해 표 재생성.
- 프레이 오브 아리아 '+150%'는 '+150(수치)' — 사용자 확인.
- **남은 것**: 증강 반영 절 재계산 → 나이트로드·섀도어·팬텀 코드 등록 시 이 값으로. 미커밋.

## Change - 260919-7 · 무기 데미지(weapon.md) — 타격마다 무기별 최소~최대 비율 난수
- **요청**: "weapon.md 각 직업별 무기와 무기별 데미지 계산식 추가했음. 이거로 데미지에 랜덤성도 추가됐어".
- **변경**: `RtsJobTableLogic.GetWeaponType(jobId)/GetWeaponRange(weapon)/RollWeapon(jobId)/WeaponMean(jobId)` 추가(팬텀 케인은 목록에 없어 1.0). `RtsCombatLogic.DoAttack` 직접 타격·지속 피해 틱 `atk.Dmg = max(1, floor(perHit × 굴림))` — 최종 데미지 뒤·방어 전, 균등 난수. 문서: damage.md 7단계 '무기 데미지' 삽입(방어는 8), 표 규칙에 기대값 (최소+최대)/2, balance-detail 표 전부 기대값 반영(창 ×1.1·아대 ×1.05·활 ×1.025·석궁 ×0.975·완드·단검 ×0.95), character.md 직업마다 '무기' 줄, 형제 파일에 weapon.md 추가(워크플로 메모리).
- **검증**: 코드 재생 전(다음 재생 때 빌드 확인). 50레벨 보스 DPS(기대값): 히어로 2,888 / 팔라딘 2,188 / DK 3,379 / 보우 2,638 / 신궁 1,998 / 썬콜 902 / 비숍 561 / 나로 1,010 / 섀도어 1,737 / 팬텀 9,177.
- **남은 것**: 증강(사용자 작업 중, 대기) → 도적 3직업 코드 등록·연출. 미커밋.

## Change - 260919-8 · 증강 개편 반영 — balance-detail '증강 반영' 절 재작성
- **요청**: "증강도 업데이트했어. 총 개수도 줄였고 기존거 다 없애버림. 밸런스표 다시 작성해봐".
- **변경**: `.info/balance-detail.md` '증강 반영' 절을 통째로 교체(scratchpad `augcalc.py`) — ① 능력치 증강 1개 가치(50레벨, 직업 5종 + 크리 100% 빌드) ② 프리즘 직업 증강 10개의 보스·몬스터 DPS 배율 ③ 43개 최고점(브15·실15·골10 좌표 하강 최적 + 직업 프리즘) + 파티 시너지. 옛 절(브론즈 스킬 증강 표·풀스택 표·점검 결론)은 삭제. 메모리 balance.md에 개편 규칙·결과.
- **결과**: 최고점 히어로 660k > 보우 442k > 불독 278k > 비숍 244k > 팬텀 183k > DK 168k > 신궁 77k > 팔라딘 51k > 섀도어 44k > 나로 43k > 썬콜 17k. 골드 10개 = 전 직업 보스 +40%, 실버 = 공격력, 크리 계열은 신궁만.
- **확인 필요**: augmentation.md 상단에 옛 '프리즘' 블록(영웅 귀환·광전사·감전사·신성 강림·대왕 표창·나도 던진다!)이 남아 있음 — 하단 새 목록만 반영. '드래곤 스피어' = 스피어 버스터로 해석. 헤더 '총 43개'는 그대로 두었음(총 개수 줄였다는 말과 다르면 알려달라).
- **사용자 확인**: 옛 프리즘 블록 삭제 / '드래곤 스피어' → 스피어 버스터 수정 / 총 개수 **7/6/4/3 = 20개**로 축소(헤더·표 재생성: 히어로 210k > 보우 121k > 불독 72k > 비숍 63k > DK 52k > 팬텀 48k > 신궁 24k > 팔라딘 13k > 섀도어 12k > 나로 11k > 썬콜 4.8k) / 나로 프리즘 쉐파 풍마수리검 ½ 확인.
- **남은 것**: 증강 코드(테이블·팝업) 반영은 별도 → 도적 3직업. 미커밋.

## Change - 260919-9 · 목표 DPS 조정안 적용(스킬 데미지) + 특성/사거리 표 복구
- **요청**: 보스 기준 최고점 목표표(나로 12.4만 … 썬콜 1.2만) → "스킬데미지에서만 조정", "프리즘 스킬옵션은 건드려도 됨", "프리즘 후(현재) 없애고 제안 조정안으로 일단 쓰자", 프리즘 전 값도 표시.
- **변경(코드)**: `RtsJobTableLogic` 디바인 차지 120→200·강화 +40→+140(ratio 340) / 스나이핑 ratio 50→130 / 블리자드 300→750 / 도트 퍼니셔 100→123. **변경(문서)**: character.md 해당 설명, augmentation.md 프리즘 5개(히어로 +65%, 에로우 플래터 100%×2, 비숍 +190%, 나로 +215% 추가, 블토 185%·카르마 125%), balance-detail 표 재생성 + 증강 절(프리즘 전 최고점 열 추가, '현재' 열 제거) + 헤더 3행. 메모리 '목표 DPS 조정' 항목.
- **사고 복구**: patch3/patch4의 사거리 표 정규식이 **직업 특성 표 행을 먼저 매치**해 공격속도·역할 칸을 숫자로 덮어썼던 것을 발견 → 특성 표 11행·사거리 표 11행을 원문 기준으로 재작성(`repair_tables.py`). 교훈: 같은 이름으로 시작하는 행이 여러 표에 있으면 표 범위를 잘라서 치환.
- **검증**: 20개 최고점 표가 목표치와 일치(±1%). 코드는 다음 재생 때 빌드 확인.
- **남은 것**: 프리즘 전 딜 손보기(사용자) → 증강 코드 반영 → 도적 3직업 코드 등록. 미커밋.

## Change - 260919-10 · 프리즘 전 조정(기본 스킬 데미지) + 프리즘 '사냥 <20% + 보스 합연산' 재구성
- **요청**: 프리즘 후 최고점 고정, 프리즘 전 목표(나로 2.4만 … 팔라딘 1.2만), 프리즘은 사냥 DPS 20% 미만 + 나머지 보스 공격시 데미지 증가(무조건 합연산). 썬콜 예외, 비숍은 데미지 일부를 보스 증가로 변환, 팔라딘 본인 효과 없음(전 = 후), 히어로 공격속도 그대로, 신궁 사냥 약화 감수.
- **변경(코드)**: `RtsJobTableLogic` 레이징 블로우 50→90·강화 +50→+100 / 디바인 차지 200→100·강화 +140→+50 / 스피어 버스터 70→80·강화 +30→+35 / 폭풍의 시 40→50·강화 +15→+17 / 피어싱 30→70·강화 +50→+110 / 도트 퍼니셔 123→628. **변경(문서)**: character.md 설명 12곳 + '동일 직업 중복 영입 불가' 헤더, augmentation.md 프리즘 8종 재작성 + 프리즘 규칙·중복 제외 헤더, damage.md 3단계 예시, balance-detail 전체 표 재생성 + 절 제목·주석 + 증강 절(프리즘 전 목표 열). balcalc/augcalc 갱신, 역산 = prism2.py.
- **결과(50레벨 보스)**: 프리즘 전 최고 나로 24,022 / 히어로 28,471 / 불독 20,001 / 섀도어 11,969 / 신궁 21,759 / 보우 18,010 / DK 20,025 / 팔라딘 11,854 / 비숍 3,770 / 썬콜 6,238. 프리즘 후 나로 124,258 / 히어로 98,405 / 팬텀 93,822 / 불독 88,584 / 섀도어 75,757 / 신궁 62,380 / 보우 54,085 / DK 51,971 / 비숍 46,131 / 썬콜 11,998 / 팔라딘 11,854 (목표 ±0.5%). 프리즘 사냥 배율 1.16~1.18(신궁 0.35·썬콜 2.9 예외).
- **검증**: stop → refresh → save → play, 빌드 로그 Info(타입 추론)만, 런타임 에러 없음(DK 벤치 정상).
- **남은 것**: 프리즘·증강 코드 반영, 영입 중복 금지·프리즘 중복 제외 코드(영입/증강 흐름 구현 시), 도적 3직업 코드 등록. 미커밋.

## Change - 260919-11 · 킷 보스 티어 + 증강 보스 7/15 + 기본 스킬 ×1.3~1.6 + 프리즘 재역산 / 서버 전투 버프 적용(크리 버그)
- **요청**: 증강 보스 사냥꾼·거인 학살자 7/15 너프에 맞춰 프리즘 보스 수치 조정 → 나이트로드 제외 직업 킷에 보스 공격 증가 티어(0/10/15/25/30/40)로 증강 효율 차등, 프리즘 전/후 목표 유지. 별건: DK 샤프아이즈 크확 20%인데 크리 안 뜸.
- **변경(코드)**: `RtsJobTableLogic` 기본 스킬 11직업 값(레블 140/+150, 디바인 120/+70, 스피어 120/+50, 폭풍 70/+23, 피어싱 110/+155, 체라 130/170·블리자드 965, 도퍼 965, 엔젤레이 38) + 50레벨(DK 40) 패시브 bossAdd 티어. `RtsUnitPopupLogic` '보스 데미지 +n%' 행(8행). **크리 버그**: `RtsCombatLogic.DoAttack`이 Calc(기본값)만 써서 서버 크리 0% → `GetStat → _RtsUnitBuffLogic:ApplyToStat(GetBuffsFor) → CalcStat`. `RtsUnitBuffLogic.UnitAt`(서버·클라 공용 조회) 추가, GetBuffsFor ClientOnly 해제.
- **변경(문서)**: character.md(킷 티어 헤더 + 설명 20여 곳, 나로/섀도어/팬텀 포함), augmentation.md(티어 헤더 + 프리즘 8종), damage.md(3단계 예시·티어), balance-detail(모든 표 재생성 — 보스 DPS에 킷 보스 % 포함, 절 제목·주석·헤더, 증강 절). balcalc(stat.boss)·augcalc(7/15, 프리즘) 갱신.
- **결과(50레벨 보스, 브7·실6·골4)**: 프리즘 전 나로 24,293 / 히어로 27,967 / 불독 20,015 / 섀도어 12,070 / 신궁 22,149 / 보우 18,041 / DK 20,092 / 비숍 3,737 / 썬콜 6,340 / 팔라딘 11,895 / 팬텀 93,946. 프리즘 후 나로 123,843 / 히어로 98,402 / 팬텀 93,946 / 불독 87,786 / 섀도어 75,666 / 신궁 62,459 / 보우 53,491 / DK 52,066 / 비숍 46,028 / 썬콜 11,997 / 팔라딘 11,895. 사냥 ×1.15~1.18(신궁 ×0.24·썬콜 ×2.8 예외).
- **검증**: stop → refresh → save → play 2회, 빌드 Info만, 런타임 에러 없음. DK 벤치에서 분홍 크리 스킨(1705) 확인 — 이전엔 서버 크리 확률 0%.
- **남은 것**: 증강·프리즘 코드 반영, 영입 중복 금지·프리즘 중복 제외, 도적 3직업 코드 등록. 미커밋.

## Change - 260920-1 · 나이트로드 등록(쿼드러플 스로우 + 쉐도우 파트너 그림자)
- **요청**: 도적 3직업 스킬 등록 시작 — 나이트로드부터. 진행 중 사용자 지시: 활 자세 → 던지기 모션, 표창 출발 위치 배 앞, 쉐도우 파트너 등 뒤 그림자(원작 4111002 실루엣, 캐릭터가 항상 앞), 표창 = 뇌전수리검, 사거리 2.
- **변경(코드)**: `RtsJobTableLogic` GetSkillsRaw/GetStatRaw("nl") — 쿼드러플 스로우 110%×4·사거리 2·빠름, 자벨린 마스터리 10/40, 크리 마스터리 20, 쉐도우 파트너 30(`halfHits = 4`), 레디 투 다이 50; fx = swingO1 + hideWeapon + 4121013 effect/hit/sound + 뇌전수리검 bullet 4발(projDx/projDy) + projShadow*(그림자 표창). CalcStat `hitsEff = hits + halfHits×0.5`. `RtsCombatLogic.DoAttack` halfHits 추가 타격(½). `RtsSkillFxLogic` SendAction/ShadowSpriteOf/ShadowClip(33종) + projDx. `RtsUnitLogic.EnsureShadow`(자식 "Shadow" 스프라이트, 30레벨~, 레벨업 시 갱신) + 시험대 3번 = 나이트로드 Lv30. `RtsUnitComponent.ApplyShadow`(등 뒤 0.22·방향 뒤집기·재시도).
- **버림**: 아바타 복제 그림자(SetColor) — 본체 옷이 안 입혀지는 사고(`any` 파라미터) + 사용자 "똑같은 실루엣이면 안 될 것 같다".
- **문서**: character.md 나이트로드 자산·규칙, motion.md shootF 실측, balance-detail 사거리 2, 메모리(assets·msw-engine).
- **검증**: 벤치 Lv30 — 던지기 모션(swingO1) 확인(사용자 "지금 좋은데 / 던지기 모션이잖아"), 199×4 + ½ 110×4, 크리 스킨, 그림자 실루엣이 등 뒤에서 같은 동작, 캐릭터 항상 앞.
- **남은 것**: 풍마수리검(프리즘) 자산, 섀도어·팬텀 등록. 미커밋.

## Change - 260920-2 · 인레이지 정의·사운드 추출·업로드, 프리즘 스킬 → character.md 이동, 섀도어 프리즘 2개 분리
- **요청**: 인레이지(히어로 프리즘) 항목 채우기 + 타격 3에 맞춘 밸런스, 원작 녹화에서 인레이지 사운드 추출(BGM 제거·부드럽게), 내 리소스 업로드, 사거리 +1, 나머지 프리즘 스킬을 character.md로 이동하고 augmentation.md는 한 줄로, 섀도어 프리즘을 블레이드 토네이도·카르마 퓨리 2개로 분리(둘 다 = 나로 ×1.10, 비중 55/45).
- **변경**: character.md — 인레이지(타격 3·사거리 +1·보스 +200%·1120017 자산·추출 사운드 RUID e794c138…) + 10개 프리즘 스킬 항목(홀리 유니티 강화·거대화·설치 딸깍·집중·엘릭서·초월·만능·풍마수리검·블레이드 토네이도·카르마 퓨리, 자산 RUID 포함). augmentation.md — 프리즘 줄 `[직업 전용] X 스킬을 획득한다.` + 이동 안내 헤더, 섀도어 2개(각 보스 +575%, 블토 39%×24·카르마 51%×15). balance-detail 증강 절 재생성(프리즘 새 이름, 섀도어 136,606·히어로 98,564). `assets/audio/enrage/enrage_sfx2c.mp3/.ogg`(BGM 게이팅 제거 + 80Hz HPF·2~4kHz −5.5dB·6.8kHz LPF·피크 −7dB, 5회 청취 조정).
- **발견**: msw-mcp 오디오 업로드는 **OGG만** 2단계 통과(wav·mp3 실패) — 메모리. 블레이드 토네이도 = 듀블 하이퍼 4341054 확인, 카르마 퓨리 자산은 미확정(후보 기재), 풍마수리검 bullet 미발견.
- **남은 것**: 카르마 퓨리·풍마수리검 자산 확정, 거대화 연출(스케일 3.0) 확인, 섀도어·팬텀 코드 등록, 프리즘 코드(Phase 6). 미커밋.

## Change - 260920-3 · 섀도어·팬텀 등록, 홀리 유니티 프리즘화, 프리즘 이름 개편, 인레이지 사운드 업로드
- **변경(코드)**: `RtsJobTableLogic` GetSkillsRaw/GetStatRaw("shad") 새비지 17.5%×8·매우빠름·메소 익스플로전(cd 8) + 대거 마스터리/크마/대거 익스퍼트/레디 투 다이(보스 +30); ("phantom") 조커 385%·0.2초·사거리 5 + 문라이트/프레이 오브 아리아/케인 엑스퍼트/블스아이(크확 50·크뎀 30·방무 100·보스 60·최종 20). 팔라딘 홀리 유니티(40) 삭제, `RtsUnitBuffLogic` bond lv 99·fin 100, 시범 팔라딘 BondNo 해제. 시험대 3번 = 팬텀 Lv30.
- **문서**: character.md 섀도어·팬텀 자산, 홀리 유니티 프리즘 항목, 애로우 레인/트루 스나이핑/디바인 퍼니시먼트 이름·설명(기존 스킬 잠금 + 신규 스킬, 데미지 동일), 인레이지 사운드 RUID e794c138…(OGG 업로드) + 사거리 +1; augmentation.md 이름; balance-detail 증강 절; 메모리(assets·balance·msw-engine).
- **검증**: 벤치 섀도어 77×8(크리 108, 붉은 참격 선), 팬텀 1,848(크리 2,842) 0.2초마다. 빌드·런타임 에러 없음.
- **남은 것**: 프리즘 스킬 자산(사용자 제공 대기), 카르마 퓨리·풍마수리검 자산, 프리즘 코드(Phase 6), 로드맵 갱신. 미커밋.

## Change - 260920-4 · 조커 2차(400041010), 유닛 순회 6기 제한 해제, 팬텀 = 영웅
- **변경(코드)**: `RtsUnitLogic.ListZoneUnits(zone)` 신설(맵 루트 자식 스캔) → `RtsUnitBuffLogic.GetBuffsFor/RefreshZone`, `RtsUnitLogic.MyUnitAt`, `RtsUnitPopupLogic.ToggleDropdown`, `RtsUnitSelectLogic.UnitAtScreen`이 1~6 대신 실제 유닛 목록을 돈다. `RtsMonsterComponent.PlayHitFx` `hitClips` 무작위 지원(+Preload). 조커 fx: alert 루프 + 24101000 카드 프레임 투사체(0.3초) + 400041010 hit 3종·타격음. `GetJobGroup("phantom")` = "영웅 · 도적", 기본 스킨 이름 "영웅 팬텀". `PlayProjectile`의 SpawnProjectile 호출에 shadow 인자 명시(빌드 LEA-1121 제거).
- **검증**: BUFFCHECK — units 1~8 열거, 3·7·8번 모두 조커(3)·샤프아이즈(5)·프레이(8) 수신; 화면에서 8기 전부 발 아래 아이콘 3개. 조커 카드가 손 앞에서 대상까지 흐르고 1,934~2,403(프레이 포함). 빌드 Error 0, 런타임 에러 없음.
- **남은 것**: HUD 슬롯 6칸 고정(7번 이상 미표시) — 초과 영입 설계가 정해지면 확장. 미커밋.

## Change - 260920-5 · 조커 3차(원작 400041009 keydown 리본 + 카드 덱 투사체), loopClip을 유닛 자식으로
- **변경(코드)**: `RtsSkillFxLogic` — `projs = {…}` 발마다 무작위 투사체(+Preload), `loopOrder`(루프 클립 OrderInLayer, 190 = 아바타 뒤), **EnsureLoopFx가 루프 클립을 mapRoot가 아니라 유닛 엔티티의 자식으로 스폰**(로컬 값 ½, 방향 바뀌면 FlipX·Position만 갱신) — 사용자 "조커 애니메이션이 캐릭터 위치 이동해도 안 따라간다". `RtsJobTableLogic` 조커 fx: alert 루프 + keydown 01eff730… loopClip(0.9배·+0.55·α0.9·뒤) + projs {screen/3 금 덱 74e2716e…, 분홍 덱 0c3d81a6…} 0.6배·자전 720°·2장/공격·0.35초 + hit 3색.
- **자산**: 내 리소스 업로드 RtsJokerDeckPink `0c3d81a68fe54b20bb1ec72375f0100d`(screen/3 색상환 −60°), 예비 RtsJokerCardGold `d77f86ea…`/RtsJokerCardPink `73d3cffa…`(미사용). 원본 PNG는 `mod-resource.dn.nexoncdn.co.kr/<files.png.path>`의 .mod에서 PNG 구간 추출(메모리 msw-engine).
- **검증**: 서버 스크립트로 3번을 (11,5)로 옮기자 리본 잔상이 같이 이동, 캐릭터가 리본 앞에 보임, 카드가 대상까지 날아가고 1,974~2,388. 빌드 Error 0, 런타임 에러 없음. 미커밋.

## Change - 260920-6 · 조커 카드 포물선 투사체(projArc) + projs 게이트 버그
- **버그**: 3차에서 조커 fx를 `projs`만으로 바꾸자 `PlayCast`의 `if fx.proj ~= nil …` 게이트가 닫혀 투사체가 전혀 안 나갔다(사용자 "카드가 안 날아가잖아") → 게이트를 `proj or projs`로.
- **변경(코드)**: `SpawnProjectile`에 `projArc`(포물선, 발마다 높이 50~100%·위/아래 무작위, 0.03초 타이머) 추가. 조커: 3장/공격(0.06초), 0.4배, 0.4초, projArc 1.0.
- **검증**: 금·분홍 덱이 손 앞에서 위·아래 포물선을 그리며 튀어 대상에 닿고 hit 3색 스파크. 0.6배는 캐릭터만 해서 0.4배로(FxOverrides로 비교 후 표에 반영). 빌드 Error 0, 런타임 에러 없음. 미커밋.

## Change - 260920-7 · 조커 카드 — 머리 위에서 항상 위로 포물선, 갈색 덱 하나, 회전 없음
- **변경(코드)**: `SpawnProjectile` projArc의 수직 벡터를 y≥0으로 정규화(왼쪽 사격 때 아래로 튀던 것) + 기본 항상 위(`projArcRandom=true`일 때만 위/아래 무작위). 조커 fx: `proj` = screen/3 금·갈색 덱만, projDx 0·projDy 1.35(머리), projSpin 제거·projNoRotate, 3장·0.4배·projArc 1.0.
- **근거**: 사용자 "포물선 무조건 캐릭터 머리쪽에서 적으로, 항상 위쪽으로", "카드는 색상 하나로 고정, 갈색", "카드는 회전하지 않고 그대로 날아감".
- **검증**: 아래 스크린샷. 미커밋.

## Change - 260920-8 · 조커 0.1초·192.5%(DPS 동일), 카드 ×1.3
- **변경(코드)**: `RtsJobTableLogic` 팬텀 ratio 385 → 192.5, period 0.2 → 0.1, 설명문 갱신; 조커 fx projCount 3 → 2(0.05초), projScale 0.4 → 0.52.
- **문서**: character.md 조커 설명·자산, balance-detail.md 헤더·요약 표·팬텀 절(표 수치는 DPS 동일이라 그대로), balcalc.py(per 0.1·ratio 1.925), 메모리 balance·assets.
- **근거**: 사용자 "조커를 0.1초당 1회로 변경, 스킬 데미지 반토막", "카드 크기 1.3배". 미커밋.

## Change - 260920-9 · 조커 카드 4종 라운드 로빈
- **변경(코드)**: `SpawnProjectile` `projs`를 무작위 → 라운드 로빈(`ProjIdx[fx.projs]`). 조커 fx `projs` = 사용자 지정 4장(400041015/screen/6·400041011/screen/5·400041013/screen/3·400041011/screen/4), 0.55배(원본 스프라이트의 절반이 투명 잔상 테두리라 0.3배는 너무 작음 — FxOverrides 비교 후 확정).
- **근거**: 사용자 "조커의 투사체를 저 4개 골고루 나가게". 미커밋.

## Change - 260920-10 · 조커 카드 5색(빨강·초록·파랑·검정·노랑) + 포물선 1.4
- **변경(코드)**: 조커 `projs` = 사용자 지정 5장(400041011/screen/6 · 400041012/screen/5 · 400041014/screen/4 · 400041015/screen/4 · 400041013/screen/5) 라운드 로빈, projArc 1.0 → 1.4, 비행 0.4 → 0.65 → 0.55초 → **0.4초로 원복**(사용자 "너무 답답하네")·hitDelay 0.35.
- **버그**: 라운드 로빈 순번을 fx.projs 테이블 자체를 키로 기억했는데 GetSkills가 매번 새 테이블을 만들어 공격마다 1·2번(빨강·초록)만 나옴(사용자 "색상 두 개밖에 없는 것 같은데") → 키를 첫 RUID+개수 문자열로. 미커밋.

## Change - 260920-11 · 조커 포물선 높이를 거리별로(1.0/1.1/1.2/1.3)
- **변경(코드)**: `PlayProjectile`이 대상까지 칸 거리(체비쇼프, 반올림)를 `SpawnProjectile(…, cells)`로 넘기고, `projArcByDist = {…}`가 있으면 그 칸 거리의 높이를 무작위 없이 쓴다. 조커: { 1.0, 1.1, 1.2, 1.3 }.
- **근거**: 사용자 "포물선 높이는 거리에 따라서 1칸 1.0 / 2칸 1.1 / 3칸 1.2 / 4칸 이상 1.3". 미커밋.

## Change - 260920-12 · 조커 모션 순환(swingOF→swingO1→swingO1→stabO1) — 사용자 확정
- **변경(코드)**: `RtsSkillFxLogic` `motionCycle`(CycleTimer, CheckLoops 정리), `motionFrame`/`motionFrameEnd`(SendAction 6인자 — 호출부 전부 nil,nil), 조커 fx `motions = { "swingOF", "swingO1", "swingO1", "stabO1" }, motionCycle = true, motionGap = 0.45`.

## Change - 260920-13 · 모든 유닛 자율 공격 + 메인 대상 고정 + attack.md
- **변경(코드)**: `RtsUnitLogic.SpawnUnit`/`RequestLevelUp` → `StartLoop`; `RtsCombatLogic.Focus` + `PickTargets(…, focus)`; `GetZoneMonsters`가 HP 0 몬스터 제외. 문서 `.info/attack.md`(사용자 파일) 작성 — 루프·스킬 선택·사거리/대상/고정·판정·시험대(개발용, 나중에 삭제).
- **검증**: 재시작 후 사거리 안 유닛들이 각자 허수아비를 침(불독 지대 89/86, 팬텀 1,732 등), 사용자가 유닛 6기를 허수아비 곁으로 옮겨 동시 공격 확인.

## Change - 260920-14 · 그리드 16×13(우측 2열 삭제·아래 1행 추가·위로 당김) + 장식물 여백 재배치
- **변경**: `tools/gen-track-grid.js` COLS 16·ROWS 13 → `assets/textures/track-grid.png` 1280×1040(이전 판 `track-grid-18x12.png`), 업로드 `ZoneTrackGridHenesys16 95b3ec9d377e46ecb9d394467d27dada`; `RtsConfigLogic` GridCols 16·GridRows 13·GridLeft −14.2222·GridTop 11.5556; `RtsThemeLogic` 헤네시스 gridRUID 교체, `GetHenesysDecor` 전부 좌우 여백으로(윗줄 덤불·건초 제거, 오른쪽 큰 건물은 HUD 밑 피해 8행 아래). `RtsZoneLogic` 주석, `assets/textures/README.md` 갱신. 엘나스 프리셋 텍스처는 아직 18×12.
- **검증**: 스크린샷 — 좌우 여백 대칭, 13행 발판 생김, 장식물이 타일과 안 겹침, 유닛 배치·공격 정상. 빌드 Error 0, 런타임 에러 없음. 미커밋.

## Change - 260920-15 · 시험대 = 무적 순회 몬스터 100기
- **변경(코드)**: `RtsCombatLogic.SetupTestBench` — 고정 허수아비 3기(DummyCol/Row·DummyExtra) 삭제 → `BenchMonsters`(100)기를 `SpawnMonster(무적)` + `RtsTrackWalkerComponent`(t = (i−1)/N, Loop)로 트랙에 고르게 세워 순회. attack.md §5 갱신(개발용, 웨이브 오면 삭제).
- **검증**: 100기가 트랙을 따라 돌고 8기 전원이 사거리 안 몬스터를 각자 침(포이즌 리전 틱 8x~9x 전 트랙, 근접 유닛 100~500). 빌드 Error 0, 런타임 에러 없음. 미커밋.

## Change - 260920-16 · 루프 클립이 보는 방향을 따라가게(폭풍의 시 keydown) + 루프 키 구역 분리
- **변경(코드)**: `RtsJobTableLogic` 폭풍의 시 `loopFacesLeft = false → true`(keydown/0~2 원본 PNG 실측: 마법진 왼쪽·날개 오른쪽 = 왼쪽 보기); `RtsSkillFxLogic` `LoopFx[key]` + `RefreshLoopFacing(key)`(반전·위치 재계산) — `EnsureLoopFx`(시전마다)와 `RtsUnitComponent.ApplyFace`(FaceDir 동기화 순간) 양쪽에서 호출; `LoopKey(zone, no)` = 구역×100+번호를 `CastFx`/`PlayBasic`이 PlayCast에 넘김(전 클라 시전 연출이라 유닛 번호만으론 다른 구역과 충돌).
- **원인**: HEAD까진 루프를 첫 시전 때 한 번만 반전하고 갱신하지 않았고(방향 바뀌면 그대로), 09-18에 FaceDir 동기화가 늦어 반대로 보인 걸 플래그 false로 덮어 실제 그림 방향과 반대가 돼 있었다.
- **검증**: 재시작 후 보우마스터 (4,4) — FaceDir +1·loopFlip true(날개 뒤·마법진 앞), 이전 (6,4) 오른쪽 볼 때 flip true / 왼쪽 볼 때 false 확인(FACECHECK3·4). 빌드 Error 0. 미커밋.
- **문서**: character.md 폭풍의 시 루프 항목, 메모리 msw-engine 루프 규칙.

## Change - 260920-17 · 블리자드 타격 클립 + 빙결 결정체 오버레이 + 빙결 이동 50% 감속
- **변경(코드)**: `RtsJobTableLogic` 블리자드 `hitClip = 2221007/hit/0 99a29e16…`(1.6배 — 광역 4종 전부 몬스터 위 타격 클립); `RtsMonsterComponent` `SetFrozenFx`/`ShatterFrozenFx`(2221012/effect 223e1ac7… 자식 오버레이: 0→12 2배속 형성 → EndFrameEvent(12)에서 Start=End=12 유지 → 풀릴 때 13→17 1.5배속 → E17 뒤 Destroy, 상한 0.8초), `IsFrozenNow`, `FreezeSlow 0.5`, `FrozenWorld 1.7`; `RtsTrackWalkerComponent.OnUpdate` 빙결 중 속도 × FreezeSlow.
- **실측(프로브)**: SpriteRUID 대입이 StartFrameIndex/EndFrameIndex를 기본값으로 되돌림 → 구간은 RUID 뒤에 설정. 재생 중 구간 변경은 다음 프레임부터 적용, EndFrameEvent는 구간 끝 프레임에서.
- **검증**: 블리자드 강제 시전 → 15기 빙결 5초 동안 오버레이 st=12/en=12 유지(FRZTICK), 풀린 뒤 잔여 엔티티 0; 서버 FrozenUntil 15/100; 빙결 몬스터 트랙 이동 ≈1.75유닛/초(기준 3.5) = 50%. 스크린샷에 몬스터 위 파란 결정체·눈꽃 확인. 빌드 Error 0. 미커밋.
- **근거**: 사용자 "얼어붙은 유닛은 스킨도 다르면 좋겠다", "블리자드 타격감 문제" → 선택: 타격 순간 몬스터 위 이펙트(광역 전부) + 결정체 오버레이 + 이동 감속.

## Change - 260920-18 · 빙결 표시 = 결정체 아이콘이 눈꽃 아이콘을 대체(머리 위 정중앙, 세계 0.7)
- **변경(코드)**: `RtsMonsterComponent` 눈꽃 `SetFreezeIcon`/FreezeIcon/FreezeIconRUID(21628ca1…) 삭제, `ShowFreeze`는 틴트 + `SetFrozenFx`(결정체)만. 결정체는 x = 피격 박스 중심, y = 체력바 위(BarY + BarH/2 + 0.05 + FrozenWorld/2, 로컬 = ÷부모 스케일), 순서 +8, `FrozenWorld` 1.7 → 0.7. `FreezeSlow`·워커 감속, 블리자드 `hitClip`(2221007/hit/0) 유지.
- **근거**: 사용자 "빙결 결정체가 2종류잖아" → "새로 추가된 아이콘을 기존 것의 대체제로 쓰자, 저게 더 낫다" → "정중앙 머리 위에 나와야 하고 지금보다 작아야 함" → "ㅇㅋ".
- **검증**: 재시작 후 강제 빙결 — 눈꽃 엔티티 0, 결정체 15/15, 스크린샷에서 체력바 위 정중앙에 작은 파란 결정체. 빌드 Error 0. 미커밋.

# Review — main (ship 전 셀프 리뷰, 2026-08-02)

## 대상
직전 커밋(3ba1505, 초기 스냅샷) 이후 워킹트리 전체 — 로드맵 #1 "탑다운 맵·카메라 리그" + 확장분(평지 타일, 개미굴 테마).

## 컨벤션 점검 (CLAUDE.md 기준)
| 항목 | 결과 |
|---|---|
| PascalCase + 역할 접미사 | ✅ `RtsConfigLogic` / `RtsBootstrapLogic` / `RtsCameraAnchorComponent` |
| Component/Logic 분리 | ✅ 튜너블 상수·경계 계산 = Logic, 엔티티 수명주기 = Component |
| @ExecSpace 명시 | ⚠️ 의도적 예외 2종: ① `RtsConfigLogic`의 게터들 — 공용 함수(호출 공간에서 실행)로 서버·클라 양쪽에서 사용, ② `RtsCameraAnchorComponent.OnBeginPlay` — mlua는 동명 메서드 중복 정의 불가라 단일 정의 + `IsServer()` 분기. 근거는 report "플랜 대비 변경점" §2·§3에 기록됨 |
| 권한 민감 로직 Server | ✅ 아바타 숨김·컴포넌트 부착·타일 채움 = ServerOnly. 카메라 이동은 입력/표시 성격이라 Client 적합 |
| 밸런스/수치 테이블 일원화 | ✅ 전부 `RtsConfigLogic` (맵 크기·스크롤·마진) |
| NativeScripts 무수정 | ✅ |
| 맵/설정 JSON 직접 수정분 Maker 로드 확인 | ✅ RtsMap.map·NewTileSet.tileset 모두 refresh+play로 정상 로드 실측 |

## 데이터 접근 스모크
해당 없음 — DataStorage/쿼리 코드 없음.

## 의도 부합 (plan/spec 대비)
- 스펙 요구(탑다운, 카메라 스크롤, 아바타 숨김, 경계, 커서 가두기, 휠줌) 전부 구현·Play Test 실측 통과.
- 플랜 대비 변경점 5건(런타임 부착, OnBeginPlay 분기, 게터 패턴, 커서 가드, 중앙 스폰) + 확장 2건(평지 타일 시스템, 개미굴 테마)은 리포트 Change 라운드에 근거와 함께 기록됨.
- 미해결(리포트 Remaining Issues): 릴리즈용 시작 맵 지정(수동 1클릭), 휠줌·Confined 실마우스 확인, LEA-3035 경고(기능 무관).

## 초안 컨벤션 문서
§4.5 초안 문서 없음(사용자 미승인 — 플랜 문서에만 존재). 마커 정리 대상 없음.

## 결론
차단급 발견 없음 — 커밋 진행 적합.

---
name: lobby-next
description: Phase 8 로비·방 — 2026-09-29 밤에 멈춘 지점과 이어서 할 일(게임 채팅 · 빠른 참가 · 방 게임 다시하기 없음 · 시작 준비 10초 검증)
metadata:
  type: project
---

2026-09-29 사용자 "내일 이어서하자"로 멈춤. 모두 **커밋 전**(제안한 v260929-1도 아직 승인 안 됨). Maker 확인은 사용자가 Stop → Refresh → Play 해 준 뒤에.

**이미 한 것(코드 반영, Maker 미확인)**
- 시작 준비 10초: `RtsStageLogic.BeginStartPrep`(카운트다운 끝 → StageNo 0 · `StartPrep` → 10초 뒤 `BeginStage(1)`), 진행 줄 "시작 준비", 안내 "1라운드 시작까지 n초 — 캐릭터를 영입하고 배치하세요".
- 방 채팅 한 줄기(서버 절반): `RtsRoomNoticeEvent.Text`, `RtsLobbyLogic.NoticeLobby(kind, userId, text)` · `AddChatFrom(room, line, fromGame)`(방이 게임 중이면 `SendToGame(key,"chat",line)`) · 핸들러 인스턴스 쪽 "chat"/"chatlog" → `RtsGameChatLogic.AddLine/SetLog`, 로비 쪽 "chat"(게임에서 온 말)/"chatsync"(기록 요청).
- `RtsGameChatLogic` = 서버 기록만 있는 뼈대(빌드 깨지지 않게).
- 확장 아이콘 업로드: expand RUID `7d1c54b0e5d1416b8d3a0da052f63400`(속성 전부 채움, `tools/gen-lobby-icons.py`에 있음).
- 로비 방 목록 "게임 중" 표시는 이미 있다(`RtsLobbyUiLogic` 상태 칸 — room.state "play"). 사용자가 09-29에 다시 요청했으니 방 게임 중에 목록에 실제로 뜨는지 Maker로 확인만.

**이어서 할 일(순서대로)**
1. 게임 채팅 마무리 — 사용자 결정: 혼자 하기 없음 · 방 게임만 · 왼쪽 고정(A안) · **오른쪽 위 인원 표시 없음** · **[크게] 팝업**.
   - `RtsGameChatLogic` 서버: `OnUserEnter(userId)`(기록 보내기 + 첫 입장 때 한 번 `NoticeLobby("chatsync")`), `@Server RequestSend(text)`(인스턴스 · 방 게임 · 구역 검사, `Clean`, "닉 : 말" → `AddLine` + `NoticeLobby("chat")`), `AddLine`이 구역 유저들에게 `Receive` 보내기.
   - 클라: 왼쪽 상자 340×206(`PlaceMobile(v,0,0,0,184,…)`, 제목 "채팅" + [크게] 아이콘, 기록, 입력 + 보내기) · 팝업 720×420(닫기, 기록, 입력 + 보내기) · 모드 바뀌면 PlaceHolder 색 다시.
   - `RtsBootstrapLogic.HandleUserEnterEvent` 인스턴스 쪽(구역 배정 뒤)에서 `_RtsGameChatLogic:OnUserEnter`. `RtsLobbyUiLogic.ChatRich`는 내 닉 강조 재사용, `IconRUID`에 expand 추가.
2. **방 게임은 다시하기 없음**(2026-09-29 사용자): 방에서 시작한 판(`RtsStageLogic.RoomNo > 0`)은 [다시하기] 숨김(`RtsHudLogic` 1034줄 `RestartBtn` 표시 조건) · 결과 창도 다시하기 대신 방으로 돌아가기 → 방 대기실에서 다시 준비/시작. `RtsPopupLogic` 1282·1348줄에 이미 RoomNo 갈래가 있으니 거기서 확인.
3. **매칭 삭제 → [빠른 참가]**(2026-09-29 사용자 "빈자리가 있는 방에 막 들어가는거임"): 서버 `RequestQuickJoin`(대기 중 · 4명 미만 · 비밀번호 없는 방 중 하나에 기존 입장 처리, 없으면 "들어갈 수 있는 방이 없어요 — 방을 만들어 보세요"), 로비 왼쪽 첫 큰 버튼을 켜진 "빠른 참가"로(점선 · "준비 중" 칩 제거). 문서에서 매칭 흔적 지우기: `.info/lobby.md`(§2 빠른 매칭 · §7 매칭 채팅/다시하기 규칙), `docs/ui-screens.md` 9장, 로드맵 Phase 8 ② 이름.
4. Maker 확인: 시작 준비 10초 · 방 채팅 로비↔게임 · 빠른 참가 · 방 게임 목록 "게임 중" · 방 게임 다시하기 없음.
5. 문서 동기화(.info/lobby.md · mode.md · view.md, docs/ui-screens.md) 후 커밋 승인 요청.

**Why:** 한 세션에서 요청이 연달아 쌓여(채팅 → 매칭 삭제·빠른 참가 → 방 게임 규칙) 중간에 멈췄다.
**How to apply:** 다음 세션 첫 작업으로 이 목록을 사용자에게 짧게 보여 주고 1번부터 잇는다. 끝나면 이 파일을 지우거나 "완료"로 바꾼다. 관련: [[lobby-design-by-claude]] · [[workflow]] · [[msw-engine]]

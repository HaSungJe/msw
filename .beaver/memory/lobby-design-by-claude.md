---
name: lobby-design-by-claude
description: 로비·방 대기실 화면은 Claude가 지금 UI 디자인 기준으로 시안(Design 캔버스)→코드까지 하고, 필요한 그림은 직접 만들어 업로드해도 된다(2026-09-28 사용자)
metadata:
  type: feedback
---

로비·방 대기실(Phase 8) 화면은 Claude가 지금 게임 UI(둥근 패널 · 연보라 강조 · 다크 모드 규칙 — RtsHudLogic·RtsPopupLogic 조각)를 참고해 직접 디자인하고 구현한다. 시안은 Artifact Design 캔버스 "로비 · 방 대기실 시안"(https://claude.ai/artifact/KHFssA8pQLeGQ3qTpvXgYb — 로비 / 방 만들기 창 / 방 대기실, 다크 모드)이고 사용자가 승인했다("시안 괜찮네 코드에 적용해봐").

**Why:** 사용자 "화면 시안 현재 UI디자인 참고해서 만들어줘. ChatGPT보다 너가 디자인 제외 모든 일 잘하니까 너만 믿는다" → "UI를 현재 디자인처럼 만들어줘. 클로드 디자인 없어?" → 시안 승인 → "그림을 너가 리소스 올려서 써도됨. 디자인대로 나오게하자".

**How to apply:** 일반 UI는 여전히 ChatGPT 인계([[workflow]] — docs/design-handoff.md)가 기본이지만, 로비·방·매칭 화면은 Claude가 시안(캔버스) → 코드 → Maker 확인까지 한다. 색은 기존 팔레트를 라이트 값으로 넘겨 다크 변환(`UiModeColor`)이 시안 색을 만들게 하고, 시안 모양을 코드 조각으로 못 내는 부분(선 아이콘·점선)은 그림을 만들어 올린다 — `tools/gen-lobby-icons.py`(시안 SVG 좌표 그대로) → `assets/design/lobby/` → 업로드([[msw-engine]] 업로드 절차). 아이콘 색 역할은 `"icon"`(글자처럼 모드별 짝 색). 화면 명세는 docs/ui-screens.md 9장.

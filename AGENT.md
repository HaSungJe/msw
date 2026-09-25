# 이 프로젝트는 .beaver/memory의 파일들을 먼저 읽고, CLAUDE.md 파일을 읽은 후 작업을 진행한다.
# Claude Code로 만들어진 프로젝트에 ChatGPT가 영입되어 일을 하는 형태이나, 워크플로우나 작업 규칙은 모두 준수하여야 한다.
# 화면 디자인(UI) 작업은 docs/ui-screens.md(화면 요소 전부 · 디자인 작업 규칙)를 먼저 읽고, 엔진 관례는 docs/msw-engine.md, 남은 일·순서는 .beaver/output/roadmap/maple-augment-defense-roadmap.md를 따른다.
# 맵 테마(바닥·트랙·장식·썸네일) 디자인은 docs/theme-presets.md — 프리셋 표(RtsThemeLogic.GetPresets)에서 바꿔도 되는 칸과 안 되는 칸, 새 테마 추가 절차가 있다.
# 디자인 인계: 이미지는 ChatGPT가 만들고, UI 조절은 가이드라인(docs/design/<날짜>-<주제>.md — 양식은 docs/design-handoff.md)으로 적어 Claude가 구현한다. 이미지는 assets/design/<날짜>-<주제>/에 둔다. 코드(.mlua)·리소스 업로드·Maker 조작은 Claude 몫.

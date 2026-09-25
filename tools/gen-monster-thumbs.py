# 몬스터·보스 썸네일 RUID 표 생성기 (2026-09-25)
#   입력: assets/textures/monster-thumbs.tsv  (ID<TAB>RUID<TAB>이름 — 업로드한 256×256 썸네일, 원본 assets/design/monster-thumbnails/)
#   출력: RootDesk/MyDesk/RtsMonsterThumbLogic.mlua 의 "-- BEGIN GENERATED" ~ "-- END GENERATED" 사이(손으로 고치지 않는다)
# 사용: python tools/gen-monster-thumbs.py
import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, "assets", "textures", "monster-thumbs.tsv")
MLUA = os.path.join(ROOT, "RootDesk", "MyDesk", "RtsMonsterThumbLogic.mlua")

rows = []
for line in io.open(TSV, encoding="utf-8"):
    line = line.rstrip("\r\n")
    if not line or line.startswith("#"):
        continue
    f = line.split("\t")
    rows.append((f[0], f[1], f[2] if len(f) > 2 else ""))
rows.sort(key=lambda r: (r[0][0] != "M", r[0]))

body = ["\t\t\t%s = \"%s\",  -- %s" % (i, r, n) for i, r, n in rows]
gen = "\t-- BEGIN GENERATED (tools/gen-monster-thumbs.py — %d종)\n\tmethod table GetTable()\n\t\treturn {\n%s\n\t\t}\n\tend\n\t-- END GENERATED" % (
    len(rows), "\n".join(body))

s = io.open(MLUA, encoding="utf-8").read()
a = s.index("\t-- BEGIN GENERATED")
b = s.index("-- END GENERATED", a) + len("-- END GENERATED")
s = s[:a] + gen + s[b:]
io.open(MLUA, "w", encoding="utf-8", newline="").write(s)
print("RtsMonsterThumbLogic: %d rows" % len(rows))

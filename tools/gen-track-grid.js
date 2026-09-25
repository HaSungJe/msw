// 그리드 트랙 텍스처 — 16×13칸, 칸 80px → 1280×1040, 투명 배경.
//   경로 = 2026-09-25 M2(사용자 "보스 영역을 맵 가운데 2×2로 … 트랙·배치 칸 조정", "매듭 2개는 붙고 1개는 멀리, 난잡한 형태"): 77칸, 교차 4곳, 매듭 3곳
//   배경은 헤네시스 잔디(2026-09-14) — 발판(트랙·보스 영역이 아닌 칸 전부 = 게임 RtsZoneLogic.IsPadCell) = 흰 반투명 채움 + 짙은 초록 테두리, 보스 영역 2×2는 비움(붉은 판은 게임이 그림)
//   트랙 칸 = 헤네시스 포석(2줄 엇갈림) + 바깥 연석, 그 위에 흰 점선 진행선
//   S = 초록 원 + 진행 방향 화살표, E = 짙은 빨강 원 + 되돌리기 화살(2026-09-25 사용자 — 글자 S/E와 E→S 복귀 점선은 삭제)
// 사용: node gen-track-grid.js <out.png>
const zlib = require('zlib');
const fs = require('fs');

const OUT = process.argv[2] || 'track-grid.png';
const COLS = 16, ROWS = 13, CS = 80;
const W = COLS * CS, H = ROWS * CS;

// 경로 꺾임점 (0-기반 [col,row]). RtsZoneLogic.GetTurnPoints(1-기반)와 같은 값.
const SEQ = [[14,8],[11,8],[11,12],[13,12],[13,10],[7,10],[7,8],[9,8],[9,12],[1,12],[1,10],[5,10],[5,1],[3,1],[3,3],[15,3],[15,0],[13,0],[13,5],[10,5]];
// 보스 영역(0-기반 7~8열 × 5~6행 = 게임 8~9열 × 6~7행)
const isBoss = (c, r) => c >= 7 && c <= 8 && r >= 5 && r <= 6;
const PATH = [];
for (let i = 0; i < SEQ.length - 1; i++) {
  const a = SEQ[i], b = SEQ[i + 1];
  const dc = Math.sign(b[0] - a[0]), dr = Math.sign(b[1] - a[1]);
  let c = a[0], r = a[1];
  if (i === 0) PATH.push([c, r]);
  while (c !== b[0] || r !== b[1]) { c += dc; r += dr; PATH.push([c, r]); }
}
const road = new Set(PATH.map(p => p[0] + ',' + p[1]));
const isRoad = (c, r) => road.has(c + ',' + r);
const isPad = (c, r) => c >= 0 && r >= 0 && c < COLS && r < ROWS && !isRoad(c, r) && !isBoss(c, r);

// ── RGBA 캔버스 + 알파 합성 ──────────────────────────────────────
const buf = new Float32Array(W * H * 4); // 0..1
function blend(x, y, r, g, b, a) {
  if (x < 0 || y < 0 || x >= W || y >= H || a <= 0) return;
  const o = (y * W + x) * 4;
  const da = buf[o + 3];
  const oa = a + da * (1 - a);
  if (oa <= 0) return;
  buf[o]     = (r * a + buf[o]     * da * (1 - a)) / oa;
  buf[o + 1] = (g * a + buf[o + 1] * da * (1 - a)) / oa;
  buf[o + 2] = (b * a + buf[o + 2] * da * (1 - a)) / oa;
  buf[o + 3] = oa;
}
function fillRect(x0, y0, w, h, rgb, a) {
  for (let y = Math.floor(y0); y < y0 + h; y++) for (let x = Math.floor(x0); x < x0 + w; x++) blend(x, y, rgb[0], rgb[1], rgb[2], a);
}
function strokeRect(x0, y0, w, h, t, rgb, a) {
  fillRect(x0, y0, w, t, rgb, a); fillRect(x0, y0 + h - t, w, t, rgb, a);
  fillRect(x0, y0, t, h, rgb, a); fillRect(x0 + w - t, y0, t, h, rgb, a);
}
function disc(cx, cy, rad, rgb, a) {
  for (let y = Math.floor(cy - rad - 1); y <= cy + rad + 1; y++) for (let x = Math.floor(cx - rad - 1); x <= cx + rad + 1; x++) {
    const d = Math.hypot(x + 0.5 - cx, y + 0.5 - cy);
    const k = Math.max(0, Math.min(1, rad + 0.5 - d));
    if (k > 0) blend(x, y, rgb[0], rgb[1], rgb[2], a * k);
  }
}
// 굵은 선분(둥근 끝) — 점선은 dash/gap
function line(x0, y0, x1, y1, t, rgb, a, dash, gap) {
  const len = Math.hypot(x1 - x0, y1 - y0);
  const ux = (x1 - x0) / len, uy = (y1 - y0) / len;
  const half = t / 2;
  const minX = Math.floor(Math.min(x0, x1) - half - 1), maxX = Math.ceil(Math.max(x0, x1) + half + 1);
  const minY = Math.floor(Math.min(y0, y1) - half - 1), maxY = Math.ceil(Math.max(y0, y1) + half + 1);
  for (let y = minY; y <= maxY; y++) for (let x = minX; x <= maxX; x++) {
    const px = x + 0.5 - x0, py = y + 0.5 - y0;
    const s = Math.max(0, Math.min(len, px * ux + py * uy));
    const d = Math.hypot(px - s * ux, py - s * uy);
    if (d > half + 0.5) continue;
    if (dash) { const m = s % (dash + gap); if (m > dash) continue; }
    const k = Math.max(0, Math.min(1, half + 0.5 - d));
    blend(x, y, rgb[0], rgb[1], rgb[2], a * k);
  }
}
function tri(p0, p1, p2, rgb, a) {
  const minX = Math.floor(Math.min(p0[0], p1[0], p2[0])), maxX = Math.ceil(Math.max(p0[0], p1[0], p2[0]));
  const minY = Math.floor(Math.min(p0[1], p1[1], p2[1])), maxY = Math.ceil(Math.max(p0[1], p1[1], p2[1]));
  const e = (a, b, x, y) => (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0]);
  for (let y = minY; y <= maxY; y++) for (let x = minX; x <= maxX; x++) {
    const px = x + 0.5, py = y + 0.5;
    const w0 = e(p0, p1, px, py), w1 = e(p1, p2, px, py), w2 = e(p2, p0, px, py);
    if ((w0 >= 0 && w1 >= 0 && w2 >= 0) || (w0 <= 0 && w1 <= 0 && w2 <= 0)) blend(x, y, rgb[0], rgb[1], rgb[2], a);
  }
}
// 굵은 원호(가운데 cx·cy, 반지름 rad, 두께 t, 각도 a0 → a1 라디안 — 화면 좌표라 y는 아래가 +)
function arc(cx, cy, rad, a0, a1, t, rgb, a) {
  const half = t / 2;
  for (let y = Math.floor(cy - rad - half - 1); y <= cy + rad + half + 1; y++) for (let x = Math.floor(cx - rad - half - 1); x <= cx + rad + half + 1; x++) {
    const px = x + 0.5 - cx, py = y + 0.5 - cy;
    const d = Math.abs(Math.hypot(px, py) - rad);
    if (d > half + 0.5) continue;
    let ang = Math.atan2(py, px);
    while (ang < a0) ang += Math.PI * 2;
    if (ang > a1) continue;
    blend(x, y, rgb[0], rgb[1], rgb[2], a * Math.max(0, Math.min(1, half + 0.5 - d)));
  }
}

const hex = h => [parseInt(h.slice(1, 3), 16) / 255, parseInt(h.slice(3, 5), 16) / 255, parseInt(h.slice(5, 7), 16) / 255];
const GRIDC = [30 / 255, 70 / 255, 20 / 255];   // 잔디 위 선색(짙은 초록)
const PADFILL = [1, 1, 1];                       // 발판 채움(흰 반투명)
const cx = c => c * CS + CS / 2, cy = r => r * CS + CS / 2;

// 1) 발판(트랙·보스 영역이 아닌 칸 전부) — 보스 영역 칸은 비운다
for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
  if (!isPad(c, r)) continue;
  fillRect(c * CS, r * CS, CS, CS, PADFILL, 0.18);
  strokeRect(c * CS + 0.5, r * CS + 0.5, CS - 1, CS - 1, 1.5, GRIDC, 0.35);
}

// 2) 트랙 칸 — 헤네시스 포석 (gen-track-stone 톤), 칸 경계는 연석(트랙끼리 맞닿은 면은 생략)
function hash(a, b) {
  let h = (a * 374761393 + b * 668265263) & 0x7fffffff;
  h = (h ^ (h >> 13)) * 1274126177 & 0x7fffffff;
  return ((h ^ (h >> 16)) & 0xffff) / 0xffff;
}
const STONE = [168 / 255, 160 / 255, 146 / 255];
const MORTAR = [92 / 255, 86 / 255, 76 / 255];
const EDGE = hex('#6b645a');
const STONE_H = 20, STONE_L = 40, JOINT = 1.6;
for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
  if (!isRoad(c, r)) continue;
  for (let y = r * CS; y < (r + 1) * CS; y++) for (let x = c * CS; x < (c + 1) * CS; x++) {
    const row = Math.floor(y / STONE_H);
    const sx = x + (row % 2) * STONE_L * 0.5;
    const idx = Math.floor(sx / STONE_L);
    const inStone = sx - idx * STONE_L;
    const dj = Math.min(inStone, STONE_L - inStone);
    const rowEdge = Math.abs((y % STONE_H) - STONE_H / 2);
    let rgb;
    if (dj < JOINT || rowEdge > STONE_H / 2 - JOINT) rgb = MORTAR;
    else {
      const k = (0.88 + hash(idx, row) * 0.24) * (1.06 - (rowEdge / (STONE_H / 2)) * 0.14);
      rgb = STONE.map(v => Math.min(1, v * k));
    }
    blend(x, y, rgb[0], rgb[1], rgb[2], 1);
  }
  const T = 3;
  if (!isRoad(c, r - 1)) fillRect(c * CS, r * CS, CS, T, EDGE, 1);
  if (!isRoad(c, r + 1)) fillRect(c * CS, (r + 1) * CS - T, CS, T, EDGE, 1);
  if (!isRoad(c - 1, r)) fillRect(c * CS, r * CS, T, CS, EDGE, 1);
  if (!isRoad(c + 1, r)) fillRect((c + 1) * CS - T, r * CS, T, CS, EDGE, 1);
}

// 3) 진행 방향 점선 (칸 중심 폴리라인, 14/22)
const LINE = hex('#e9e2d2');
for (let i = 0; i < PATH.length - 1; i++) {
  const a = PATH[i], b = PATH[i + 1];
  line(cx(a[0]), cy(a[1]), cx(b[0]), cy(b[1]), 3, LINE, 0.9, 14, 22);
}

// 4) S = 진행 방향 화살표 / E = 되돌리기(끝에 닿은 몹은 S로 돌아간다 — 복귀 점선 대신 이 아이콘 하나로)
const S = SEQ[0], E = SEQ[SEQ.length - 1];
const S2 = PATH[1];
const WHITE = [1, 1, 1];
{
  const x = cx(S[0]), y = cy(S[1]);
  disc(x, y, 22, hex('#1f6b3f'), 0.95);
  const ux = Math.sign(S2[0] - S[0]), uy = Math.sign(S2[1] - S[1]); // 첫 칸 → 둘째 칸 방향
  const vx = -uy, vy = ux;
  line(x - ux * 11, y - uy * 11, x + ux * 2, y + uy * 2, 5, WHITE, 1);
  tri([x + ux * 13, y + uy * 13], [x + vx * 10, y + vy * 10], [x - vx * 10, y - vy * 10], WHITE, 1);
}
{
  const x = cx(E[0]), y = cy(E[1]);
  disc(x, y, 22, hex('#9a2a1d'), 0.95);
  // 시계 반대 방향 되돌리기: 원호 오른쪽 위(−60°)에서 시작해 한 바퀴 가까이 돌고, 시작점에 화살촉
  const R = 10, A0 = -Math.PI / 3, A1 = A0 + Math.PI * 1.55;
  arc(x, y, R, A0, A1, 4.5, WHITE, 1);
  const hx = x + R * Math.cos(A0), hy = y + R * Math.sin(A0);
  const tx = Math.sin(A0), ty = -Math.cos(A0); // 원호가 시작점에서 나아가는 반대쪽(= 화살 끝이 향하는 쪽)
  const nx = Math.cos(A0), ny = Math.sin(A0);
  tri([hx + tx * 8, hy + ty * 8], [hx + nx * 7 - tx * 2, hy + ny * 7 - ty * 2], [hx - nx * 7 - tx * 2, hy - ny * 7 - ty * 2], WHITE, 1);
}

// ── PNG 쓰기 ─────────────────────────────────────────────────────
const raw = Buffer.alloc((W * 4 + 1) * H);
for (let y = 0; y < H; y++) {
  raw[y * (W * 4 + 1)] = 0;
  for (let x = 0; x < W; x++) {
    const o = y * (W * 4 + 1) + 1 + x * 4, i = (y * W + x) * 4;
    raw[o] = Math.round(buf[i] * 255); raw[o + 1] = Math.round(buf[i + 1] * 255);
    raw[o + 2] = Math.round(buf[i + 2] * 255); raw[o + 3] = Math.round(buf[i + 3] * 255);
  }
}
function crc32(b) {
  let t = crc32.t;
  if (!t) { t = crc32.t = []; for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } }
  let c = 0xffffffff;
  for (let i = 0; i < b.length; i++) c = t[(c ^ b[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
function chunk(type, data) {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
  const tt = Buffer.from(type, 'ascii');
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(Buffer.concat([tt, data])));
  return Buffer.concat([len, tt, data, crc]);
}
const ihdr = Buffer.alloc(13);
ihdr.writeUInt32BE(W, 0); ihdr.writeUInt32BE(H, 4); ihdr[8] = 8; ihdr[9] = 6;
const png = Buffer.concat([
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
  chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw, { level: 9 })), chunk('IEND', Buffer.alloc(0)),
]);
fs.writeFileSync(OUT, png);
let pads = 0; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) if (isPad(c, r)) pads++;
console.log('written', OUT, W + 'x' + H, 'road=' + road.size, 'pads=' + pads, 'steps=' + (PATH.length - 1), png.length, 'bytes');

// 그리드 트랙 텍스처 — 화면 v2(아티팩트 v16). 18×12칸, 칸 80px → 1440×960, 투명 배경.
//   배경은 헤네시스 잔디(2026-09-14) — 빈 칸 = 짙은 초록 얇은 테두리 / 발판(트랙에 4방향으로 면한 칸) = 흰 반투명 채움 + 테두리
//   트랙 칸 = 헤네시스 포석(2줄 엇갈림) + 바깥 연석, 그 위에 흰 점선 진행선
//   S(초록)·E(빨강) 원 + 글자, 3열 왼쪽 여백에 E→S 복귀 점선 화살표
// 사용: node gen-track-grid.js <out.png>
const zlib = require('zlib');
const fs = require('fs');

const OUT = process.argv[2] || 'track-grid.png';
const COLS = 18, ROWS = 12, CS = 80;
const W = COLS * CS, H = ROWS * CS;

// 경로 꺾임점 (0-기반 [col,row], 아티팩트 seq 그대로). RtsZoneLogic의 1-기반 표와 같은 값.
const SEQ = [[2,5],[2,1],[13,1],[13,5],[8,5],[8,7],[13,7],[13,9],[11,9],[11,3],[6,3],[6,7],[2,7],[2,9],[6,9],[6,11],[2,11]];
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
const isPad = (c, r) => !isRoad(c, r) && (isRoad(c + 1, r) || isRoad(c - 1, r) || isRoad(c, r + 1) || isRoad(c, r - 1));

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
const GLYPH = {
  S: ['.###.', '#...#', '#....', '.###.', '....#', '#...#', '.###.'],
  E: ['#####', '#....', '#....', '####.', '#....', '#....', '#####'],
};
function glyph(ch, cx, cy, px, rgb, a) {
  const g = GLYPH[ch];
  const x0 = cx - 2.5 * px, y0 = cy - 3.5 * px;
  for (let r = 0; r < 7; r++) for (let c = 0; c < 5; c++) if (g[r][c] === '#') fillRect(x0 + c * px, y0 + r * px, px, px, rgb, a);
}

const hex = h => [parseInt(h.slice(1, 3), 16) / 255, parseInt(h.slice(3, 5), 16) / 255, parseInt(h.slice(5, 7), 16) / 255];
const GRIDC = [30 / 255, 70 / 255, 20 / 255];   // 잔디 위 선색(짙은 초록)
const PADFILL = [1, 1, 1];                       // 발판 채움(흰 반투명)
const cx = c => c * CS + CS / 2, cy = r => r * CS + CS / 2;

// 1) 빈 칸 / 발판
for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
  if (isRoad(c, r)) continue;
  if (isPad(c, r)) {
    fillRect(c * CS, r * CS, CS, CS, PADFILL, 0.18);
    strokeRect(c * CS + 0.5, r * CS + 0.5, CS - 1, CS - 1, 1.5, GRIDC, 0.35);
  } else {
    strokeRect(c * CS + 0.5, r * CS + 0.5, CS - 1, CS - 1, 1.5, GRIDC, 0.20);
  }
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

// 4) S / E
const S = SEQ[0], E = SEQ[SEQ.length - 1];
disc(cx(S[0]), cy(S[1]), 22, hex('#1f6b3f'), 0.95); glyph('S', cx(S[0]), cy(S[1]), 4, [1, 1, 1], 1);
disc(cx(E[0]), cy(E[1]), 22, hex('#9a2a1d'), 0.95); glyph('E', cx(E[0]), cy(E[1]), 4, [1, 1, 1], 1);

// 5) E→S 복귀 화살표 (3열 왼쪽 여백)
const LX = 2 * CS - 22;
const RET = hex('#c0392b');
line(LX, cy(E[1]), LX, cy(S[1]) + 14, 3, RET, 0.7, 10, 8);
tri([LX - 9, cy(S[1]) + 14], [LX + 9, cy(S[1]) + 14], [LX, cy(S[1]) - 2], RET, 0.7);

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

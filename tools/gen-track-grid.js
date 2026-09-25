// 그리드 트랙 텍스처 — 16×13칸, 칸 80px → 1280×1040, 투명 배경.
//   경로 = 2026-09-25 M2(사용자 "보스 영역을 맵 가운데 2×2로 … 트랙·배치 칸 조정", "매듭 2개는 붙고 1개는 멀리, 난잡한 형태"): 77칸, 교차 4곳, 매듭 3곳
//   배경은 헤네시스 잔디(2026-09-14) — 발판(트랙·보스 영역이 아닌 칸 전부 = 게임 RtsZoneLogic.IsPadCell) = 흰 반투명 채움 + 짙은 초록 테두리, 보스 영역 2×2는 비움(붉은 판은 게임이 그림)
//   트랙 칸 = 헤네시스 포석(2줄 엇갈림) + 바깥 연석, 그 위에 흰 점선 진행선
//   S = 길 위에 새긴 진행 화살표, E = 길 위에 새긴 되돌리기 화살(바깥 원·글자·E→S 복귀 점선 없음)
//   2026-09-25 테마별 트랙 판: 셋째 인자 = 테마 key. 경로·발판·S/E는 같고 길의 재질·가장자리 장식이 다르다.
//     henesys 따뜻한 포석 + 꽃/풀 / ellinia 이끼 둥근돌 + 뿌리/잎 / perion 붉은 사암 + 균열/자갈
//     kerning 청회색 도시 벽돌 + 공사장 안전띠 / lith 목재 부두 + 항구석/로프/물결
// 사용: node gen-track-grid.js <out.png> [theme]
const zlib = require('zlib');
const fs = require('fs');

const OUT = process.argv[2] || 'track-grid.png';
const THEME = process.argv[3] || 'henesys';
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
const cx = c => c * CS + CS / 2, cy = r => r * CS + CS / 2;

// 테마 프리셋: 발판 채움·선(가이드라인 표의 발판 선색·알파), 연석 색, 길 표면 그리기
const TH = {
  henesys: { padFill: [1, 1, 1], padFillA: 0.10, padLine: hex('#56835B'), padLineA: 0.34, edge: hex('#7D6048'), edgeHi: hex('#F5DCB0'), road: 'flag', stone: hex('#D8BA8C'), mortar: hex('#977554') },
  ellinia: { padFill: hex('#C6E8D4'), padFillA: 0.09, padLine: hex('#2F7567'), padLineA: 0.36, edge: hex('#456954'), edgeHi: hex('#B9D7AA'), road: 'cobble', stone: hex('#93B5A3'), mortar: hex('#567B69'), root: hex('#624E38') },
  perion: { padFill: hex('#F6DFBC'), padFillA: 0.10, padLine: hex('#A15D3E'), padLineA: 0.36, edge: hex('#8E4F34'), edgeHi: hex('#F8D29C'), road: 'blocks', stone: hex('#D99A65'), mortar: hex('#9F6342') },
  kerning: { padFill: hex('#D7DEEF'), padFillA: 0.10, padLine: hex('#35425E'), padLineA: 0.40, edge: hex('#434B62'), edgeHi: hex('#C8D0DD'), road: 'bricks', stone: hex('#929BAD'), mortar: hex('#636D82') },
  lith: { padFill: hex('#CDEBEE'), padFillA: 0.09, padLine: hex('#467A88'), padLineA: 0.38, edge: hex('#71533C'), edgeHi: hex('#ECD1A4'), road: 'harbor', stone: hex('#E2D2B3'), wood: hex('#B98557'), mortar: hex('#9F8C72'), seam: hex('#704D35') },
}[THEME];
if (!TH) { console.error('unknown theme ' + THEME); process.exit(1); }

// 1) 발판(트랙·보스 영역이 아닌 칸 전부) — 보스 영역 칸은 비운다
for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
  if (!isPad(c, r)) continue;
  fillRect(c * CS, r * CS, CS, CS, TH.padFill, TH.padFillA);
  strokeRect(c * CS + 0.5, r * CS + 0.5, CS - 1, CS - 1, 1.5, TH.padLine, TH.padLineA);
}

// 2) 트랙 칸 — 테마 길 표면, 칸 경계는 연석(트랙끼리 맞닿은 면은 생략)
function hash(a, b) {
  let h = (a * 374761393 + b * 668265263) & 0x7fffffff;
  h = (h ^ (h >> 13)) * 1274126177 & 0x7fffffff;
  return ((h ^ (h >> 16)) & 0xffff) / 0xffff;
}
const shade = (rgb, k) => rgb.map(v => Math.max(0, Math.min(1, v * k)));
// 둥근돌: 전역 격자(간격 G) 안 흔든 점 → 가장 가까운 두 점 거리 차가 작으면 줄눈, 가장자리일수록 어둡게(둥근 느낌)
function cobble(x, y) {
  const G = 19;
  const gx = Math.floor(x / G), gy = Math.floor(y / G);
  let d1 = 1e9, d2 = 1e9, id = 0;
  for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) {
    const X = gx + i, Y = gy + j;
    const px = (X + 0.2 + hash(X, Y) * 0.6) * G, py = (Y + 0.2 + hash(Y + 71, X + 13) * 0.6) * G;
    const d = Math.hypot(x + 0.5 - px, y + 0.5 - py);
    if (d < d1) { d2 = d1; d1 = d; id = X * 7919 + Y; } else if (d < d2) d2 = d;
  }
  const gap = d2 - d1;
  if (gap < 2.2) return TH.mortar;
  const k = (0.86 + hash(id, 5) * 0.24) * (0.84 + Math.min(1, gap / 9) * 0.2);
  return shade(TH.stone, k);
}
// 블록(사암): 줄 높이 H, 줄마다 길이가 조금씩 다른 블록, 아래·오른쪽 가장자리 그늘
function blocks(x, y, H, L, J) {
  const row = Math.floor(y / H);
  const off = hash(row, 3) * L;
  const sx = x + off;
  const len = L * (0.8 + hash(Math.floor(sx / L), row) * 0.4);
  const idx = Math.floor(sx / L);
  const inS = sx - idx * L;
  const ry = y - row * H;
  if (inS < J || ry < J) return TH.mortar;
  let k = 0.9 + hash(idx, row + 17) * 0.18;
  if (ry > H - 3 || inS > L - 3) k *= 0.9;
  if (ry < J + 2) k *= 1.06;
  return shade(TH.stone, k);
}
// 벽돌(커닝): 줄 H, 길이 L, 반 칸 엇갈림
function bricks(x, y) {
  const H = 13, L = 27, J = 1.6;
  const row = Math.floor(y / H);
  const sx = x + (row % 2) * L * 0.5;
  const idx = Math.floor(sx / L);
  const inS = sx - idx * L, ry = y - row * H;
  if (inS < J || ry < J) return TH.mortar;
  let k = 0.9 + hash(idx, row) * 0.16;
  if (ry > H - 2.5) k *= 0.9;
  return shade(TH.stone, k);
}
// 판자(리스): 가로 판자 14px 줄, 판자 길이 들쭉날쭉, 틈·못
function planks(x, y) {
  const H = 14;
  const row = Math.floor(y / H);
  const L = 58 + Math.floor(hash(row, 9) * 30);
  const sx = x + hash(row, 4) * L;
  const idx = Math.floor(sx / L);
  const inS = sx - idx * L, ry = y - row * H;
  if (ry < 1.6 || inS < 1.4) return TH.seam;
  if ((inS > 4 && inS < 6.2 || inS > L - 6.2 && inS < L - 4) && ry > 5.5 && ry < 8) return shade(TH.seam, 0.9); // 못
  const grain = 0.94 + 0.06 * Math.sin((x * 0.21 + hash(idx, row) * 9) + Math.sin(y * 0.9) * 0.6);
  return shade(TH.wood, (0.88 + hash(idx, row + 3) * 0.2) * grain);
}
// 헤네시스 포석(기존)
function flag(x, y) {
  const STONE_H = 20, STONE_L = 40, JOINT = 1.6;
  const row = Math.floor(y / STONE_H);
  const sx = x + (row % 2) * STONE_L * 0.5;
  const idx = Math.floor(sx / STONE_L);
  const inStone = sx - idx * STONE_L;
  const dj = Math.min(inStone, STONE_L - inStone);
  const rowEdge = Math.abs((y % STONE_H) - STONE_H / 2);
  if (dj < JOINT || rowEdge > STONE_H / 2 - JOINT) return TH.mortar;
  const k = (0.88 + hash(idx, row) * 0.24) * (1.06 - (rowEdge / (STONE_H / 2)) * 0.14);
  return TH.stone.map(v => Math.min(1, v * k));
}
// 리스: 경로 순서로 판자 3칸 · 항구석 2칸 교차(가이드라인 "목재 판자와 항구석의 교차 — 중간색 목재 비중 높게")
const pathIdx = new Map();
PATH.forEach((p, i) => { if (!pathIdx.has(p[0] + ',' + p[1])) pathIdx.set(p[0] + ',' + p[1], i); });
function surface(x, y, c, r) {
  if (TH.road === 'cobble') return cobble(x, y);
  if (TH.road === 'blocks') return blocks(x, y, 26, 48, 2.2);
  if (TH.road === 'bricks') return bricks(x, y);
  if (TH.road === 'harbor') {
    const i = pathIdx.get(c + ',' + r) || 0;
    return (i % 5) < 3 ? planks(x, y) : blocks(x, y, 20, 34, 2);
  }
  return flag(x, y);
}
for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
  if (!isRoad(c, r)) continue;
  const T = 4;
  if (isPad(c, r - 1)) fillRect(c * CS, r * CS - 4, CS, 4, TH.edge, 0.18);
  if (isPad(c, r + 1)) fillRect(c * CS, (r + 1) * CS, CS, 4, TH.edge, 0.18);
  if (isPad(c - 1, r)) fillRect(c * CS - 4, r * CS, 4, CS, TH.edge, 0.18);
  if (isPad(c + 1, r)) fillRect((c + 1) * CS, r * CS, 4, CS, TH.edge, 0.18);
  for (let y = r * CS; y < (r + 1) * CS; y++) for (let x = c * CS; x < (c + 1) * CS; x++) {
    const rgb = surface(x, y, c, r);
    blend(x, y, rgb[0], rgb[1], rgb[2], 1);
  }
  if (!isRoad(c, r - 1)) { fillRect(c * CS, r * CS, CS, T, TH.edge, 1); fillRect(c * CS + 4, r * CS + T, CS - 8, 1.5, TH.edgeHi, 0.72); }
  if (!isRoad(c, r + 1)) { fillRect(c * CS, (r + 1) * CS - T, CS, T, TH.edge, 1); fillRect(c * CS + 4, (r + 1) * CS - T - 1.5, CS - 8, 1.5, TH.edgeHi, 0.72); }
  if (!isRoad(c - 1, r)) { fillRect(c * CS, r * CS, T, CS, TH.edge, 1); fillRect(c * CS + T, r * CS + 4, 1.5, CS - 8, TH.edgeHi, 0.72); }
  if (!isRoad(c + 1, r)) { fillRect((c + 1) * CS - T, r * CS, T, CS, TH.edge, 1); fillRect((c + 1) * CS - T - 1.5, r * CS + 4, 1.5, CS - 8, TH.edgeHi, 0.72); }
}
// 엘리니아: 길 가장자리에 뿌리가 조금 걸친다(연석 밖에서 안으로 짧은 곡선)
if (TH.road === 'cobble') {
  const sides = [[0, -1], [0, 1], [-1, 0], [1, 0]];
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
    if (!isRoad(c, r)) continue;
    sides.forEach(([dx, dy], si) => {
      if (isRoad(c + dx, r + dy)) return;
      if (hash(c * 31 + si, r * 17) > 0.45) return;
      const t = 0.2 + hash(c + si * 5, r + 3) * 0.6;           // 변을 따라 위치
      const len = 10 + hash(r + si, c + 7) * 12;
      // 변의 시작점(연석 바깥 4px)과 안쪽 방향
      let x0, y0, nx = -dx, ny = -dy, tx = dy === 0 ? 0 : 1, ty = dy === 0 ? 1 : 0;
      if (dy === -1) { x0 = c * CS + t * CS; y0 = r * CS - 4; }
      else if (dy === 1) { x0 = c * CS + t * CS; y0 = (r + 1) * CS + 4; }
      else if (dx === -1) { x0 = c * CS - 4; y0 = r * CS + t * CS; }
      else { x0 = (c + 1) * CS + 4; y0 = r * CS + t * CS; }
      const bend = (hash(c, r + si) - 0.5) * 10;
      const xm = x0 + nx * len * 0.55 + tx * bend, ym = y0 + ny * len * 0.55 + ty * bend;
      const x1 = x0 + nx * len + tx * bend * 1.6, y1 = y0 + ny * len + ty * bend * 1.6;
      line(x0, y0, xm, ym, 4, TH.root, 0.95);
      line(xm, ym, x1, y1, 3, TH.root, 0.95);
      line(x0, y0, xm, ym, 1.4, shade(TH.root, 1.35), 0.6);
    });
  }
}

// 2b) 마을마다 길 가장자리의 작은 랜드마크. 길 칸을 가리지 않고 전투 중에도 재질이 읽히는 밀도로 둔다.
const sides = [[0, -1], [0, 1], [-1, 0], [1, 0]];
for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
  if (!isRoad(c, r)) continue;
  const x = cx(c), y = cy(r), h = hash(c * 59 + 11, r * 83 + 7);
  if (THEME === 'ellinia' && h < 0.13) {
    arc(x, y, 11, 0, Math.PI * 2, 2, hex('#B2F3C4'), 0.36);
    disc(x, y, 2.4, hex('#D4FFE4'), 0.55);
  }
  if (THEME === 'perion' && h < 0.27) {
    const px = x - 17 + hash(c, r + 31) * 24, py = y - 19 + hash(r, c + 19) * 23;
    line(px, py, px + 8, py + 3, 1.7, hex('#854F38'), 0.65);
    line(px + 8, py + 3, px + 12, py + 10, 1.3, hex('#854F38'), 0.65);
    line(px + 8, py + 3, px + 15, py + 1, 1.2, hex('#854F38'), 0.55);
  }
  if (THEME === 'kerning' && h < 0.12) {
    disc(x + 18, y - 18, 8, hex('#4E596D'), 0.9);
    arc(x + 18, y - 18, 5.5, 0, Math.PI * 2, 1.4, hex('#B8C3D1'), 0.7);
  }
  sides.forEach(([dx, dy], si) => {
    if (!isPad(c + dx, r + dy)) return;
    const v = hash(c * 37 + si * 11, r * 41 + 3);
    const along = (hash(c + si * 7, r + 29) - 0.5) * 40;
    const x0 = x + dx * (CS / 2 - 1) + (dy !== 0 ? along : 0);
    const y0 = y + dy * (CS / 2 - 1) + (dx !== 0 ? along : 0);
    if (THEME === 'henesys' && v < 0.23) {
      line(x0, y0, x0 + dx * 10, y0 + dy * 10, 2.1, hex('#4B8D53'), 0.82);
      disc(x0 + dx * 10, y0 + dy * 10, 3, hex('#E5F2A3'), 0.92);
      if (v < 0.075) {
        const fx = x0 + dx * 13, fy = y0 + dy * 13;
        disc(fx - 3, fy, 3.8, hex('#FFF5D3'), 0.95);
        disc(fx + 3, fy, 3.8, hex('#FFF5D3'), 0.95);
        disc(fx, fy - 3, 3.8, hex('#FFF5D3'), 0.95);
        disc(fx, fy + 3, 3.8, hex('#FFF5D3'), 0.95);
        disc(fx, fy, 2.7, hex('#E8B94D'), 1);
      }
    } else if (THEME === 'ellinia' && v < 0.23) {
      const fx = x0 + dx * 9, fy = y0 + dy * 9;
      line(x0, y0, fx, fy, 2, hex('#53774F'), 0.8);
      disc(fx - 3, fy - 2, 4.2, hex('#77B779'), 0.9);
      disc(fx + 3, fy + 1, 3.5, hex('#B2D889'), 0.9);
    } else if (THEME === 'perion' && v < 0.22) {
      disc(x0 + dx * 8, y0 + dy * 8, 4.2, hex('#AA6747'), 0.9);
      disc(x0 + dx * 14 + 4, y0 + dy * 14 + 2, 2.3, hex('#E3AB70'), 0.85);
    } else if (THEME === 'kerning' && v < 0.32) {
      const px = x0 - dx * 8, py = y0 - dy * 8;
      for (let k = -1; k <= 1; k++) {
        const sx = px + (dy !== 0 ? k * 10 : 0), sy = py + (dx !== 0 ? k * 10 : 0);
        line(sx - 4, sy - 3, sx + 4, sy + 3, 4, hex('#F4C84E'), 0.88);
      }
    } else if (THEME === 'lith' && v < 0.52) {
      const rope = hex('#F1D9AB');
      if (dy !== 0) line(x0 - 19, y0 - dy * 7, x0 + 19, y0 - dy * 7, 2.8, rope, 0.85, 11, 6);
      else line(x0 - dx * 7, y0 - 19, x0 - dx * 7, y0 + 19, 2.8, rope, 0.85, 11, 6);
      if (v < 0.12) disc(x0 + dx * 10, y0 + dy * 10, 3.5, hex('#9ADAE1'), 0.85);
    }
  });
}

// 3) 진행 방향 점선 (칸 중심 폴리라인, 14/22)
const LINE = THEME === 'kerning' ? hex('#FBE09A') : THEME === 'ellinia' ? hex('#D6F8D6') : hex('#FFF2D6');
for (let i = 0; i < PATH.length - 1; i++) {
  const a = PATH[i], b = PATH[i + 1];
  line(cx(a[0]), cy(a[1]), cx(b[0]), cy(b[1]), 3, LINE, 0.9, 14, 22);
}

// 4) 출발·되돌리기: 원형 배지를 빼고 돌/나무 표면에 새긴 작은 화살표만 둔다.
const S = SEQ[0], E = SEQ[SEQ.length - 1];
const S2 = PATH[1];
const START = THEME === 'kerning' ? hex('#FFE19A') : THEME === 'ellinia' ? hex('#D6F6CB') : hex('#F7E9BC');
const RETURN = THEME === 'lith' ? hex('#FFE0AE') : hex('#F5C9AA');
{
  const x = cx(S[0]), y = cy(S[1]);
  const ux = Math.sign(S2[0] - S[0]), uy = Math.sign(S2[1] - S[1]); // 첫 칸 → 둘째 칸 방향
  const vx = -uy, vy = ux;
  line(x - ux * 12, y - uy * 12, x + ux * 2, y + uy * 2, 7, TH.edge, 0.72);
  line(x - ux * 12, y - uy * 12, x + ux * 2, y + uy * 2, 4, START, 0.94);
  tri([x + ux * 13, y + uy * 13], [x + vx * 8, y + vy * 8], [x - vx * 8, y - vy * 8], START, 0.94);
}
{
  const x = cx(E[0]), y = cy(E[1]);
  // 시계 반대 방향 되돌리기: 원호 오른쪽 위(−60°)에서 시작해 한 바퀴 가까이 돌고, 시작점에 화살촉
  const R = 10, A0 = -Math.PI / 3, A1 = A0 + Math.PI * 1.55;
  arc(x, y, R, A0, A1, 6.5, TH.edge, 0.78);
  arc(x, y, R, A0, A1, 3.8, RETURN, 0.96);
  const hx = x + R * Math.cos(A0), hy = y + R * Math.sin(A0);
  const tx = Math.sin(A0), ty = -Math.cos(A0); // 원호가 시작점에서 나아가는 반대쪽(= 화살 끝이 향하는 쪽)
  const nx = Math.cos(A0), ny = Math.sin(A0);
  tri([hx + tx * 8, hy + ty * 8], [hx + nx * 6 - tx * 2, hy + ny * 6 - ty * 2], [hx - nx * 6 - tx * 2, hy - ny * 6 - ty * 2], RETURN, 0.96);
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

// 스타디움 트랙 — 헤네시스 돌길(포석) 텍스처. 가운데 투명.
//   중심선 라운드 사각형을 촘촘히 샘플링해 각 픽셀의 (호길이 s, 수직거리 d)를 구하고,
//   (s, d) 공간에 포석 격자를 그린다 → 돌이 트랙 진행 방향을 따라 눕는다.
// 사용: node gen-track-stone.js <w> <h> <cornerR> <band> <out.png>
const zlib = require('zlib');
const fs = require('fs');

const W = parseInt(process.argv[2] || '740');
const H = parseInt(process.argv[3] || '270');
const R = parseInt(process.argv[4] || '50');    // 코너 반지름(px)
const BAND = parseInt(process.argv[5] || '32'); // 트랙 폭(px)
const OUT = process.argv[6] || 'track-stone.png';

const CX = W / 2, CY = H / 2;
const INSET = BAND / 2 + 1;
const HW = W / 2 - INSET - R;   // 중심선 직선부 반길이(가로)
const HH = H / 2 - INSET - R;   // 〃 (세로)

// ── 중심선 경로 샘플링 (호길이 포함) ────────────────────────────────
// 경로: 우변 중앙에서 시작해 반시계. 형상만 필요하므로 시작점은 무관.
const path = [];
function pushArc(ccx, ccy, a0, a1) {
  const steps = Math.max(2, Math.ceil((Math.abs(a1 - a0) * R) / 1.5));
  for (let i = 0; i <= steps; i++) {
    const a = a0 + (a1 - a0) * (i / steps);
    path.push([ccx + R * Math.cos(a), ccy + R * Math.sin(a)]);
  }
}
function pushLine(x0, y0, x1, y1) {
  const len = Math.hypot(x1 - x0, y1 - y0);
  const steps = Math.max(2, Math.ceil(len / 1.5));
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    path.push([x0 + (x1 - x0) * t, y0 + (y1 - y0) * t]);
  }
}
const HALF_PI = Math.PI / 2;
pushLine(CX + HW + R, CY - HH, CX + HW + R, CY + HH);                 // 우변
pushArc(CX + HW, CY + HH, 0, HALF_PI);                               // 우하 코너
pushLine(CX + HW, CY + HH + R, CX - HW, CY + HH + R);                // 아랫변
pushArc(CX - HW, CY + HH, HALF_PI, Math.PI);                         // 좌하 코너
pushLine(CX - HW - R, CY + HH, CX - HW - R, CY - HH);                // 좌변
pushArc(CX - HW, CY - HH, Math.PI, Math.PI * 1.5);                   // 좌상 코너
pushLine(CX - HW, CY - HH - R, CX + HW, CY - HH - R);                // 윗변
pushArc(CX + HW, CY - HH, Math.PI * 1.5, Math.PI * 2);               // 우상 코너

// 누적 호길이
const arc = [0];
for (let i = 1; i < path.length; i++) {
  arc[i] = arc[i - 1] + Math.hypot(path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]);
}
const PERIM = arc[arc.length - 1];

// 라운드 사각형 부호 있는 거리 (바깥 > 0)
function sdf(x, y) {
  const dx = Math.abs(x - CX) - HW;
  const dy = Math.abs(y - CY) - HH;
  const qx = Math.max(dx, 0), qy = Math.max(dy, 0);
  return Math.hypot(qx, qy) + Math.min(Math.max(dx, dy), 0) - R;
}

// ── 포석 격자 ────────────────────────────────────────────────────
// 둘레를 정수 개의 돌로 나눠 이음매가 딱 맞물리게
const STONE_LEN = PERIM / Math.round(PERIM / 26);
const ROWS = 2;              // 폭 방향 2줄
const JOINT = 1.6;           // 이음매 반폭(px)

function hash(a, b) {
  let h = (a * 374761393 + b * 668265263) & 0x7fffffff;
  h = (h ^ (h >> 13)) * 1274126177 & 0x7fffffff;
  return ((h ^ (h >> 16)) & 0xffff) / 0xffff;
}

// 헤네시스 돌 톤 — 흰 눈 위에서 뜨도록 중간 회갈색
const STONE = [168, 160, 146];
const MORTAR = [92, 86, 76];
const EDGE = [72, 66, 58];

const raw = Buffer.alloc((W * 4 + 1) * H);
const half = BAND / 2;

for (let y = 0; y < H; y++) {
  raw[y * (W * 4 + 1)] = 0;
  for (let x = 0; x < W; x++) {
    const o = y * (W * 4 + 1) + 1 + x * 4;
    const px = x + 0.5, py = y + 0.5;
    const d = sdf(px, py);
    if (Math.abs(d) > half + 1.5) { raw[o + 3] = 0; continue; }

    // 가장 가까운 경로 샘플 → 호길이 s
    let best = 0, bestD2 = Infinity;
    for (let i = 0; i < path.length; i++) {
      const ddx = px - path[i][0], ddy = py - path[i][1];
      const d2 = ddx * ddx + ddy * ddy;
      if (d2 < bestD2) { bestD2 = d2; best = i; }
    }
    const s = arc[best];

    const ad = Math.abs(d);
    let r, g, b, a = 255;

    if (ad > half) {                         // 바깥 안티에일리어스
      r = EDGE[0]; g = EDGE[1]; b = EDGE[2];
      a = Math.round(255 * Math.max(0, (half + 1.5 - ad) / 1.5));
    } else if (ad > half - 2) {              // 연석(테두리)
      r = EDGE[0]; g = EDGE[1]; b = EDGE[2];
    } else {
      const row = Math.floor((d + half) / (BAND / ROWS));           // 0 또는 1
      const stagger = (row % 2) * STONE_LEN * 0.5;                  // 줄마다 반칸 엇갈리게
      const sp = s + stagger;
      const idx = Math.floor(sp / STONE_LEN);
      const inStone = sp - idx * STONE_LEN;
      const distToJoint = Math.min(inStone, STONE_LEN - inStone);
      const rowEdge = Math.abs(((d + half) % (BAND / ROWS)) - (BAND / ROWS) / 2);

      if (distToJoint < JOINT || rowEdge > BAND / ROWS / 2 - JOINT) {
        r = MORTAR[0]; g = MORTAR[1]; b = MORTAR[2];               // 이음매
      } else {
        const v = hash(idx, row);                                   // 돌마다 톤 편차
        const tone = 0.88 + v * 0.24;
        // 돌 안쪽은 위가 밝고 아래가 어둡게 (얕은 입체감)
        const shade = 1.06 - (rowEdge / (BAND / ROWS / 2)) * 0.14;
        const k = tone * shade;
        r = Math.min(255, Math.round(STONE[0] * k));
        g = Math.min(255, Math.round(STONE[1] * k));
        b = Math.min(255, Math.round(STONE[2] * k));
      }
    }
    raw[o] = r; raw[o + 1] = g; raw[o + 2] = b; raw[o + 3] = a;
  }
}

function crc32(buf) {
  let t = crc32.t;
  if (!t) { t = crc32.t = []; for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } }
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = t[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
function chunk(type, data) {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
  const tt = Buffer.from(type, 'ascii');
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(Buffer.concat([tt, data])));
  return Buffer.concat([len, tt, data, crc]);
}
const ihdr = Buffer.alloc(13);
ihdr.writeUInt32BE(W, 0); ihdr.writeUInt32BE(H, 4);
ihdr[8] = 8; ihdr[9] = 6;
const png = Buffer.concat([
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
  chunk('IHDR', ihdr),
  chunk('IDAT', zlib.deflateSync(raw, { level: 9 })),
  chunk('IEND', Buffer.alloc(0)),
]);
fs.writeFileSync(OUT, png);
console.log('written', OUT, W + 'x' + H, 'perim=' + PERIM.toFixed(1), 'stone=' + STONE_LEN.toFixed(1), png.length, 'bytes');

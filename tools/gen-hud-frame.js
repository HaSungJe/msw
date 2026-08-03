// HUD 장식 프레임 생성기 — 어두운 청동 베벨 + 코너 플레이트/리벳 (중앙 투명 오버레이)
// 사용: node gen-hud-frame.js <width> <height> <out.png>
const zlib = require('zlib');
const fs = require('fs');

const W = parseInt(process.argv[2] || '340');
const H = parseInt(process.argv[3] || '340');
const OUT = process.argv[4] || 'frame.png';

const T = 10;        // 테두리 두께
const CORNER = 26;   // 코너 플레이트 크기

function px(x, y) {
  // 프레임 밴드 밖(중앙)은 투명
  const inBand = x < T || y < T || x >= W - T || y >= H - T;
  const inCorner =
    (x < CORNER && y < CORNER) || (x >= W - CORNER && y < CORNER) ||
    (x < CORNER && y >= H - CORNER) || (x >= W - CORNER && y >= H - CORNER);
  if (!inBand && !inCorner) return [0, 0, 0, 0];

  // 밴드 내 깊이(0=바깥, 1=안쪽)
  const d = Math.min(x, y, W - 1 - x, H - 1 - y);
  let r, g, b;
  if (d === 0 || d === 1) { r = 12; g = 10; b = 8; }              // 최외곽 검정 라인
  else if (d < 4) { r = 122; g = 96; b = 58; }                     // 밝은 베벨(상단광)
  else if (d < T - 2) {                                            // 본체 청동 그라데이션
    const t = (d - 4) / (T - 6);
    r = Math.round(88 - t * 30); g = Math.round(68 - t * 24); b = Math.round(42 - t * 16);
  }
  else if (inBand) { r = 30; g = 24; b = 16; }                     // 안쪽 어두운 라인
  else { r = 58; g = 46; b = 30; }                                 // 코너 플레이트 안쪽 채움

  // 코너 플레이트: 약간 어둡게 + 사선 컷 느낌
  if (inCorner) {
    const cx = x < CORNER ? x : W - 1 - x;
    const cy = y < CORNER ? y : H - 1 - y;
    if (cx + cy > CORNER + 6 && !inBand) return [0, 0, 0, 0];      // 사선 컷(안쪽 투명)
    r = Math.round(r * 0.92); g = Math.round(g * 0.92); b = Math.round(b * 0.92);
    // 리벳 (플레이트 대각선상 2개)
    const rivets = [[8, 8], [17, 17]];
    for (const [rx, ry] of rivets) {
      const dd = Math.hypot(cx - rx, cy - ry);
      if (dd < 3.2) { r = 140; g = 116; b = 76; }
      else if (dd < 4.2) { r = 20; g = 16; b = 12; }
    }
  }
  return [r, g, b, 255];
}

const raw = Buffer.alloc((W * 4 + 1) * H);
for (let y = 0; y < H; y++) {
  raw[y * (W * 4 + 1)] = 0;
  for (let x = 0; x < W; x++) {
    const [r, g, b, a] = px(x, y);
    const o = y * (W * 4 + 1) + 1 + x * 4;
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
console.log('written', OUT, W + 'x' + H, png.length, 'bytes');

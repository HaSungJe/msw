// 스타디움(라운드 사각형) 트랙 외곽선 텍스처 생성 — 가운데 투명
// 사용: node gen-track-texture.js <w> <h> <cornerR> <band> <out.png>
const zlib = require('zlib');
const fs = require('fs');

const W = parseInt(process.argv[2] || '740');
const H = parseInt(process.argv[3] || '270');
const R = parseInt(process.argv[4] || '50');   // 코너 반지름(px)
const BAND = parseInt(process.argv[5] || '32'); // 트랙 폭(px)
const OUT = process.argv[6] || 'track.png';

// 중심선 라운드 사각형까지의 부호 없는 거리
function distToPath(x, y) {
  const cx = W / 2, cy = H / 2;
  const inset = BAND / 2 + 1;
  const halfW = W / 2 - inset - R;
  const halfH = H / 2 - inset - R;
  const dx = Math.abs(x - cx) - halfW;
  const dy = Math.abs(y - cy) - halfH;
  const qx = Math.max(dx, 0), qy = Math.max(dy, 0);
  const outside = Math.sqrt(qx * qx + qy * qy);
  const inside = Math.min(Math.max(dx, dy), 0);
  return Math.abs(outside + inside - R);
}

const raw = Buffer.alloc((W * 4 + 1) * H);
for (let y = 0; y < H; y++) {
  raw[y * (W * 4 + 1)] = 0;
  for (let x = 0; x < W; x++) {
    const d = distToPath(x + 0.5, y + 0.5);
    const half = BAND / 2;
    let a = 0, r = 0, g = 0, b = 0;
    if (d <= half) {
      // 트랙 노면: 가장자리로 갈수록 밝은 테두리
      const edge = 1 - d / half;          // 0(가장자리) ~ 1(중심선)
      if (d > half - 3) { r = 232; g = 206; b = 140; a = 255; }   // 바깥 라인
      else {
        const t = edge;
        r = Math.round(96 + t * 40);
        g = Math.round(80 + t * 34);
        b = Math.round(58 + t * 24);
        a = 235;
      }
    } else if (d <= half + 1.2) {
      r = 232; g = 206; b = 140;
      a = Math.round(255 * (half + 1.2 - d) / 1.2);
    }
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

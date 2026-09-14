// 헤네시스 풀밭 바닥 — 256px 무이음새, 연두 램프 (gen-snow-floor.js 노이즈 구조 재사용)
//   2026-09-14 사용자 지시: 트랙/타일 배경을 헤네시스로. 밝은 연두 잔디 + 미세 풀결 + 옅은 명암 덩어리
// 사용: node gen-henesys-floor.js <out.png>
const zlib = require('zlib');
const fs = require('fs');

const W = 256, H = 256;

function makeLattice(n, seed) {
  let s = seed;
  const rnd = () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; };
  const g = [];
  for (let y = 0; y < n; y++) { g[y] = []; for (let x = 0; x < n; x++) g[y][x] = rnd(); }
  return g;
}
const smooth = t => t * t * (3 - 2 * t);
function sampleWrapped(g, n, fx, fy) {
  const x0 = Math.floor(fx) % n, y0 = Math.floor(fy) % n;
  const x1 = (x0 + 1) % n, y1 = (y0 + 1) % n;
  const tx = smooth(fx - Math.floor(fx)), ty = smooth(fy - Math.floor(fy));
  const a = g[y0][x0] * (1 - tx) + g[y0][x1] * tx;
  const b = g[y1][x0] * (1 - tx) + g[y1][x1] * tx;
  return a * (1 - ty) + b * ty;
}

const l1 = makeLattice(4, 137);    // 큰 명암 덩어리
const l2 = makeLattice(8, 2029);   // 중간
const l3 = makeLattice(64, 7717);  // 미세 풀결
const l4 = makeLattice(128, 991);  // 아주 미세한 점

// 헤네시스 잔디 램프 — 그늘 초록 → 볕 받은 연두
const stops = [
  [112, 168, 70],
  [134, 190, 84],
  [154, 206, 96],
  [176, 220, 112],
];
function rampColor(t) {
  const f = Math.max(0, Math.min(0.9999, t)) * (stops.length - 1);
  const i = Math.floor(f), u = f - i;
  const a = stops[i], b = stops[i + 1];
  return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u];
}

const raw = Buffer.alloc((W * 3 + 1) * H);
for (let y = 0; y < H; y++) {
  raw[y * (W * 3 + 1)] = 0;
  for (let x = 0; x < W; x++) {
    const n1 = sampleWrapped(l1, 4, x / W * 4, y / H * 4);
    const n2 = sampleWrapped(l2, 8, x / W * 8, y / H * 8);
    // 풀결: 세로로 살짝 늘어진 미세 노이즈
    const n3 = sampleWrapped(l3, 64, x / W * 64, y / H * 64 * 0.6);
    const n4 = sampleWrapped(l4, 128, x / W * 128, y / H * 128);
    let v = n1 * 0.40 + n2 * 0.25 + n3 * 0.25 + n4 * 0.10;
    v = Math.pow(v, 0.95);
    const [r, g, b] = rampColor(v);
    const o = y * (W * 3 + 1) + 1 + x * 3;
    raw[o] = Math.round(r);
    raw[o + 1] = Math.round(g);
    raw[o + 2] = Math.round(b);
  }
}

function crc32(buf) {
  let table = crc32.table;
  if (!table) {
    table = crc32.table = [];
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      table[n] = c >>> 0;
    }
  }
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = table[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
function chunk(type, data) {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
  const t = Buffer.from(type, 'ascii');
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(Buffer.concat([t, data])));
  return Buffer.concat([len, t, data, crc]);
}
const ihdr = Buffer.alloc(13);
ihdr.writeUInt32BE(W, 0); ihdr.writeUInt32BE(H, 4);
ihdr[8] = 8; ihdr[9] = 2;
const png = Buffer.concat([
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
  chunk('IHDR', ihdr),
  chunk('IDAT', zlib.deflateSync(raw, { level: 9 })),
  chunk('IEND', Buffer.alloc(0)),
]);
const out = process.argv[2] || 'henesys-grass.png';
fs.writeFileSync(out, png);
console.log('written', out, W + 'x' + H, png.length, 'bytes');

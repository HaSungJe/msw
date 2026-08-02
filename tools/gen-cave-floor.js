// v2: smooth dark cave floor — no crack lines, soft large forms, painterly
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

const l1 = makeLattice(4, 91);    // 큰 명암 덩어리
const l2 = makeLattice(8, 517);   // 중간
const l3 = makeLattice(64, 3301); // 미세 그레인

// 어두운 청회색 램프 (동굴 바닥): 부드러운 연속 보간
// 갈색(개미굴 흙) 톤 — 2026-08-02 사용자 확정
const stops = [
  [40, 30, 22],   // 어두운 부분
  [58, 44, 32],
  [78, 60, 44],
  [98, 78, 58],   // 밝은 부분(은은하게)
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
    const n3 = sampleWrapped(l3, 64, x / W * 64, y / H * 64);
    // 큰 덩어리 위주 + 미세 그레인 약간
    let v = n1 * 0.62 + n2 * 0.28 + n3 * 0.10;
    v = Math.pow(v, 1.15); // 살짝 어두운 쪽으로
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
const out = process.argv[2] || 'cave2.png';
fs.writeFileSync(out, png);
console.log('written', out, png.length, 'bytes');

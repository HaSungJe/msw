// Shared vector-derived UI assets. Run with the bundled Node/sharp runtime.
const fs = require('fs');
const path = require('path');
const sharp = require(process.env.SHARP_PATH || 'sharp');
const out = path.resolve(__dirname, '../assets/design/ui');
fs.mkdirSync(out, { recursive: true });
const paths = {
  atk: '<path d="M18 44 42 12l10-2-2 10-28 28M14 34l16 16M12 52l8-8"/>',
  pct: '<path d="m15 28 13-17 7 1-2 8-15 17M11 25l13 13M9 41l7-7M37 48l17-19"/><circle cx="39" cy="32" r="3"/><circle cx="52" cy="46" r="3"/>',
  fin: '<path d="m35 8-19 27h13l-2 21 23-30H36l4-18z"/>',
  boss: '<path d="m10 20 10 9 12-17 12 17 10-9-5 27H15zM17 53h30"/><path d="m26 36 6-6 6 6-6 6z"/>',
  crit: '<circle cx="32" cy="32" r="17"/><circle cx="32" cy="32" r="6"/><path d="M32 8v10m0 28v10M8 32h10m28 0h10"/>',
  critDmg: '<path d="m32 8 5 15 14-8-7 15 12 8-17 2-1 16-10-14-14 8 6-17-13-7 17-2z"/>',
  skill: '<path d="m32 9 19 22-19 24-19-24zM13 31h38M32 9l-8 22 8 24 8-24z"/>'
};
const colors = {atk:'#3878aa',pct:'#338eaf',fin:'#9063b1',boss:'#d17b55',crit:'#409d8e',critDmg:'#c15b84',skill:'#8672bd'};
async function png(name, svg) { await sharp(Buffer.from(svg)).png().toFile(path.join(out,name+'.png')); }
(async()=>{
 for (const [key,p] of Object.entries(paths)) await png('stat-'+key, `<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><rect x="1" y="1" width="62" height="62" rx="18" fill="${colors[key]}" fill-opacity=".12"/><g fill="none" stroke="${colors[key]}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">${p}</g></svg>`);
 const grades = {
 bronze: {a:'#fff4e7',b:'#c5916c',c:'#9f6748',shape:'<circle cx="64" cy="64" r="45"/><circle cx="64" cy="64" r="38" fill="none"/><path d="M24 111C1 91 1 58 15 35M104 111c23-20 23-53 9-76M10 61l-7-8m5 26L0 72m14 23-11-5m115-29 7-8m-5 26 8-7m-14 23 11-5" fill="none"/>'},
 silver: {a:'#ffffff',b:'#bec8d7',c:'#7c8da6',shape:'<path d="M31 75 5 37l4 32 22 28M97 75l26-38-4 32-22 28"/><path d="m64 8 51 56-51 56L13 64z"/><path d="m64 19 40 45-40 45-40-45z" fill="none"/>'},
 gold: {a:'#fffae5',b:'#e7bc65',c:'#ac802e',shape:'<path d="m64 1 10 25 22-15-2 29 31-1-19 23 20 19-30 4 2 28-25-14-9 28-10-26-23 15 2-30-30-4 19-20L3 39l29 1-2-27 24 14z"/><circle cx="64" cy="64" r="38"/><circle cx="64" cy="64" r="32" fill="none"/>'},
 prism: {a:'#f5fcff',b:'#c8b9ef',c:'#a18acf',shape:'<path d="m64 2 48 28 8 64-56 31L8 94l8-64z"/><path d="m64 10 37 26 10 52-47 29-47-29 10-52z" fill="none"/><path d="m64 2 13 30 35-2-18 34 26 30-42-3-14 34-15-33-41 2 27-30-19-34 35 2z" fill="none"/>'}
 };
 for(const [key,g] of Object.entries(grades)) await png('grade-'+key,`<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128"><defs><linearGradient id="metal" x2=".8" y2="1"><stop stop-color="${g.b}"/><stop offset=".28" stop-color="${g.a}"/><stop offset=".52" stop-color="${g.b}"/><stop offset=".76" stop-color="${g.a}"/><stop offset="1" stop-color="${g.b}"/></linearGradient></defs><g fill="url(#metal)" stroke="${g.c}" stroke-width="2" stroke-linejoin="round">${g.shape}</g><circle cx="64" cy="64" r="26" fill="${g.a}" fill-opacity=".94"/></svg>`);
 await png('rounded-outline','<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><rect x="1" y="1" width="62" height="62" rx="12" fill="none" stroke="white" stroke-width="2"/></svg>');
 await png('water-flow',`<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="512" viewBox="0 0 1024 512"><defs><linearGradient id="silk" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff" stop-opacity=".85"/><stop offset=".25" stop-color="#ffffff" stop-opacity=".5"/><stop offset=".55" stop-color="#c1c0d5" stop-opacity=".17"/><stop offset=".75" stop-color="#ffffff" stop-opacity=".85"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient><filter id="soft"><feGaussianBlur stdDeviation="3"/></filter></defs><g fill="url(#silk)"><path d="M-80 160C190-90 475 390 800 95S1000 35 1120 10L1120 50C920 75 1040 100 810 150S460 435 160 240-10 260-80 230Z"/><path d="M-80 360C280 190 480 650 850 280S1100 260 1160 250V330C960 255 825 565 550 495S85 325-80 440Z"/></g><g fill="none" stroke="white" stroke-opacity=".8"><path d="M-40 186C230-45 440 450 800 115S1040 45 1100 20" stroke-width="4" filter="url(#soft)"/><path d="M-40 195C230-30 440 460 810 130S1040 55 1100 30" stroke-width="1.8"/><path d="M-50 400C290 230 465 630 850 310S1100 290 1140 280" stroke-width="3"/></g></svg>`);
 console.log('Generated 7 stat icons, 4 rarity emblems, outline and white water-flow.');
})().catch(e=>{console.error(e);process.exit(1)});

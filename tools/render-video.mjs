/**
 * Ghi hình một file HTML animation thành MP4, ghép sẵn voice-over.
 *
 * Dùng chromium + ffmpeg đã cài sẵn cho html-video.
 *
 *   node tools/render-video.mjs <frame.html> <out.mp4> <giay> [audio.mp3]
 *
 * Cách làm: đóng băng mọi animation CSS ngay khi trang bắt đầu parse, chờ font
 * nạp xong, rồi mới thả cho chạy — nếu không, animation đã chạy mất mấy giây
 * trong lúc trình duyệt còn đang dựng font, và đoạn đó lọt vào bản ghi.
 */
import { spawn } from 'node:child_process';
import { mkdtemp, readdir, rm, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';

// Tìm playwright theo thứ tự: bản cài kèm html-video (máy gốc), rồi
// tools/node_modules (máy mới: cd tools && npm install playwright).
const HERE = dirname(fileURLToPath(import.meta.url));
const PW_CHON = [
  join(HERE, 'html-video', 'packages', 'adapter-hyperframes',
       'node_modules', 'playwright', 'index.mjs'),
  join(HERE, 'node_modules', 'playwright', 'index.mjs'),
];
const PW = PW_CHON.find(existsSync);
if (!PW) {
  console.error('Khong thay playwright. Chay:\n' +
    '  cd tools && npm install playwright && npx playwright install chromium');
  process.exit(1);
}
const { chromium } = await import(pathToFileURL(PW).href);

const [, , htmlArg, outArg, durArg, audioArg, leadArg] = process.argv;
if (!htmlArg || !outArg || !durArg) {
  console.error('Dung: node render-video.mjs <frame.html> <out.mp4> <giay> [audio.mp3] [lead-in giay]');
  process.exit(1);
}

const htmlPath = resolve(htmlArg);
const outPath = resolve(outArg);
const duration = Number(durArg);
const audioPath = audioArg && audioArg !== '-' ? resolve(audioArg) : null;
const leadInSec = leadArg !== undefined ? Number(leadArg) : 1.0;  // trễ giọng so với hình
const W = 1080, H = 1920, FPS = 30;

// Chế độ nháp: make-video.py đặt các biến này để mã hoá nhanh, hình xấu hơn.
// Ghi hình bằng Chromium luôn chạy theo thời gian thật, không rút ngắn được —
// chỗ tiết kiệm được duy nhất là khâu mã hoá và độ phân giải xuất ra.
const PRESET = process.env.RBW_PRESET || 'slow';
const CRF = process.env.RBW_CRF || '20';
const OUT_W = Number(process.env.RBW_W || W);
const OUT_H = Number(process.env.RBW_H || H);

const run = (cmd, args) =>
  new Promise((res, rej) => {
    const p = spawn(cmd, args, { stdio: ['ignore', 'ignore', 'pipe'] });
    let err = '';
    p.stderr.on('data', (d) => (err += d));
    p.on('close', (c) => (c === 0 ? res() : rej(new Error(`${cmd} thoát ${c}:\n${err.slice(-1500)}`))));
  });

const recDir = await mkdtemp(join(tmpdir(), 'rbw-rec-'));
await mkdir(dirname(outPath), { recursive: true });

console.log(`  Ghi hinh ${W}x${H} @${FPS}fps, ${duration}s ...`);
const browser = await chromium.launch({
  headless: true,
  args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'],
});
const ctx = await browser.newContext({
  viewport: { width: W, height: H },
  deviceScaleFactor: 1,
  recordVideo: { dir: recDir, size: { width: W, height: H } },
});
const page = await ctx.newPage();

// Đóng băng animation TRƯỚC khi CSS kịp chạy.
await page.addInitScript(() => {
  const s = document.createElement('style');
  s.id = '__freeze';
  s.textContent =
    '*,*::before,*::after{animation-play-state:paused !important;' +
    '-webkit-animation-play-state:paused !important}';
  const put = () => (document.head || document.documentElement).appendChild(s);
  if (document.head || document.documentElement) put();
  else document.addEventListener('DOMContentLoaded', put, { once: true });
  window.__unfreeze = () => {
    document.getElementById('__freeze')?.remove();
    // phát mọi video nền từ đầu, đồng bộ với lúc thả animation
    document.querySelectorAll('video').forEach((v) => {
      try { v.currentTime = 0; v.play(); } catch (e) {}
    });
  };
});

await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'domcontentloaded' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(600);          // font vẽ xong hẳn

const tStart = Date.now();
await page.evaluate(() => window.__unfreeze());
await page.waitForTimeout(duration * 1000 + 400);
const wall = (Date.now() - tStart) / 1000;

await ctx.close();
await browser.close();

const webm = (await readdir(recDir)).filter((f) => f.endsWith('.webm')).sort().pop();
if (!webm) throw new Error('Chromium khong tao ra file webm');
const webmPath = join(recDir, webm);
console.log(`  Ghi xong (${wall.toFixed(1)}s thuc te) -> ma hoa MP4 ...`);

const args = ['-y', '-v', 'error', '-i', webmPath];
if (audioPath && existsSync(audioPath)) args.push('-i', audioPath);

args.push(
  '-t', String(duration),
  '-r', String(FPS),
  '-vf', `scale=${OUT_W}:${OUT_H}:flags=lanczos,format=yuv420p`,
  '-c:v', 'libx264', '-preset', PRESET, '-crf', CRF,
  '-profile:v', 'high', '-level', '4.0',
  '-movflags', '+faststart',
);
if (audioPath && existsSync(audioPath)) {
  // giọng bắt đầu sau lead-in, đệm im lặng ở cuối cho khớp độ dài video
  const delayMs = Math.round(leadInSec * 1000);
  args.push(
    '-filter_complex', `[1:a]adelay=${delayMs}|${delayMs},apad[a]`,
    '-map', '0:v', '-map', '[a]',
    '-c:a', 'aac', '-b:a', '160k', '-ar', '44100',
  );
} else {
  args.push('-an');
}
args.push(outPath);

await run('ffmpeg', args);
await rm(recDir, { recursive: true, force: true });
console.log(`  XONG: ${outPath}`);

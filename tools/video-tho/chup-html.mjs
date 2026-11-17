// Chụp một file HTML thành ảnh 1080×1920 (ảnh bìa khi KHÔNG dùng Remotion — kênh công ty).
//   node tools/video-tho/chup-html.mjs <vao.html> <ra.png>
// Mượn Playwright/Chromium của tools/html-video như tools/render-video.mjs. Font: nhúng @font-face trỏ tới
// tools/video-tho/fonts/*.woff2 (bản đã bỏ hint — TTF gốc vẽ "c" thành "o").
import {existsSync} from 'node:fs';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const PW = join(HERE, '..', 'html-video', 'packages', 'adapter-hyperframes', 'node_modules', 'playwright', 'index.mjs');
if (!existsSync(PW)) {
  console.error(`Khong thay playwright tai ${PW}`);
  process.exit(1);
}
const [vao, ra] = process.argv.slice(2);
if (!vao || !ra) {
  console.error('dung: node chup-html.mjs <vao.html> <ra.png>');
  process.exit(1);
}
const {chromium} = await import(pathToFileURL(PW).href);
const b = await chromium.launch();
const p = await b.newPage({viewport: {width: 1080, height: 1920}});
await p.goto(pathToFileURL(resolve(vao)).href);
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(300);
await p.screenshot({path: resolve(ra), clip: {x: 0, y: 0, width: 1080, height: 1920}});
await b.close();
console.log(`chup xong: ${resolve(ra)}`);

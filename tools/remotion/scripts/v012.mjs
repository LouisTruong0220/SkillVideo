// Dựng 4 cảnh Remotion của video 012 thẳng vào assets/ của dự án.  Chạy: node scripts/v012.mjs [ten...]
import {execFileSync} from 'node:child_process';
import path from 'node:path';

const RA = path.resolve('../../04-video-projects/012-robot-le-tan/assets');
const TAT_CA = ['dien-thoai', 'hom-nay', 'ba-the', 'tich-hop'];
const chon = process.argv.slice(2).length ? process.argv.slice(2) : TAT_CA;
for (const x of chon) {
  console.log(`→ rm-${x}.mp4`);
  execFileSync('npx', ['remotion', 'render', 'src/index.ts', `v012-${x}`, path.join(RA, `rm-${x}.mp4`), '--codec=h264', '--crf=16'], {
    stdio: 'inherit',
    shell: true,
  });
}

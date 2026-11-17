// Dựng 4 cảnh Remotion của video 011 thẳng vào assets/ của dự án.  Chạy: npm run v011
import {execFileSync} from 'node:child_process';
import path from 'node:path';

const RA = path.resolve('../../04-video-projects/011-robot-cong-nghiep-vs-dich-vu-v2/assets');
for (const x of ['so-gia', 'tay-may', 'day-chuyen', 'ket']) {
  console.log(`→ rm-${x}.mp4`);
  execFileSync('npx', ['remotion', 'render', 'src/index.ts', `v011-${x}`, path.join(RA, `rm-${x}.mp4`), '--codec=h264', '--crf=16'], {
    stdio: 'inherit',
    shell: true,
  });
}

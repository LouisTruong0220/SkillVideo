import {Composition, Folder, Still} from 'remotion';
import {MauDoc} from './MauDoc';
import {SoGia} from './v011/SoGia';
import {TayMay} from './v011/TayMay';
import {DayChuyen} from './v011/DayChuyen';
import {Ket} from './v011/Ket';
import {Thumbnail} from './v011/Thumbnail';
import {DienThoai} from './v012/DienThoai';
import {HomNay} from './v012/HomNay';
import {BaThe} from './v012/BaThe';
import {TichHop} from './v012/TichHop';
import {AnhBia} from './v012/AnhBia';

// Khung dọc 1080×1920, 30 khung/giây. Thêm video mới = thêm một <Composition>.
// Cảnh "nửa trên" (1080×960) dựng ở đây rồi ghép vào HyperFrames (tools/video-tho) như một canh-phu.
const NUA = {fps: 30, width: 1080, height: 960};

export const RemotionRoot = () => (
  <>
    <Composition
      id="MauDoc"
      component={MauDoc}
      durationInFrames={90}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{dong1: 'Xin chào', dong2: 'Video mẫu Remotion'}}
    />
    <Folder name="v011-robot-cong-nghiep-vs-dich-vu">
      <Composition id="v011-so-gia" component={SoGia} durationInFrames={255} {...NUA} />
      <Composition id="v011-tay-may" component={TayMay} durationInFrames={207} {...NUA} />
      <Composition id="v011-day-chuyen" component={DayChuyen} durationInFrames={333} {...NUA} />
      <Composition id="v011-ket" component={Ket} durationInFrames={304} {...NUA} />
      <Still id="v011-thumbnail" component={Thumbnail} width={1080} height={1920} />
    </Folder>
    <Folder name="v012-robot-le-tan">
      <Composition id="v012-dien-thoai" component={DienThoai} durationInFrames={375} {...NUA} />
      <Composition id="v012-hom-nay" component={HomNay} durationInFrames={297} {...NUA} />
      <Composition id="v012-ba-the" component={BaThe} durationInFrames={156} {...NUA} />
      <Composition id="v012-tich-hop" component={TichHop} durationInFrames={252} {...NUA} />
      <Still id="v012-anh-bia" component={AnhBia} width={1080} height={1920} />
    </Folder>
  </>
);

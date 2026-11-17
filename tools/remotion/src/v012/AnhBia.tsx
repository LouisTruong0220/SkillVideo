// Ảnh bìa video 012 robot lễ tân — 1080×1920.
// Xuất: npx remotion still src/index.ts v012-anh-bia ../../04-video-projects/012-robot-le-tan/anh-bia.png
// Lưới hồ sơ TikTok cắt giữa 3:4 (y 240–1680) → tiêu đề + hai thẻ + mặt người nói nằm trong dải đó.
// Chữ chỉ trong x 140–940 (cột nút phải), y ≥ 250. Không logo, không số điện thoại (logo ROBOWORLD trên thân máy là cảnh thật).
// Tiêu đề bám phép so sánh trong video: "điện thoại xịn chỉ nghe gọi — có mua không?" → robot lễ tân chỉ để chào khách?
// Ảnh: public/v012/mat.jpg (nguon/c01 11,0 s — câu "Chắc chắn là không rồi") · nova-mat.jpg (nguon/c02 10,6 s — Nova nhìn thẳng, màn mặt cười)
//      · ung-dung.jpg (assets/canh-01 1,0 s).
import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {DO, Nhan, tieuDe, VANG, vien} from '../v011/chung';

const THE_TOP = 712;
const THE_H = 450;
const THE_W = 370;

// hop = khung đặt ảnh [trái, trên, rộng] (px trong thẻ) — phóng to để đưa robot / màn hình vào giữa thẻ
const The: React.FC<{left: number; nhan: string; duoi: string; src: string; hop: [number, number, number]; mau: string}> = ({left, nhan, duoi, src, hop, mau}) => (
  <div
    style={{
      position: 'absolute', left, top: THE_TOP, width: THE_W, height: THE_H, borderRadius: 34, overflow: 'hidden',
      border: `6px solid ${mau}`, boxShadow: `0 0 50px ${mau === VANG ? 'rgba(255,212,59,.45)' : 'rgba(232,54,54,.55)'}`, background: '#1a0f0e',
    }}
  >
    <Img src={staticFile(src)} style={{position: 'absolute', left: hop[0], top: hop[1], width: hop[2], height: 'auto'}} />
    <div style={{position: 'absolute', left: 0, right: 0, top: 0, padding: '20px 0 46px', background: 'linear-gradient(rgba(0,0,0,.8), transparent)', textAlign: 'center'}}>
      <span style={{display: 'inline-block', padding: '10px 26px', borderRadius: 999, background: mau, color: mau === VANG ? '#110909' : '#fff', ...tieuDe(44), lineHeight: 1}}>
        {nhan}
      </span>
    </div>
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, padding: '60px 0 22px', background: 'linear-gradient(transparent, rgba(0,0,0,.88))', textAlign: 'center', fontWeight: 700, fontSize: 40, ...vien(6)}}>
      <Nhan chu={duoi} />
    </div>
  </div>
);

export const AnhBia: React.FC = () => (
  <AbsoluteFill style={{background: '#110909', fontFamily: 'Britti', color: '#fff', overflow: 'hidden'}}>
    {/* người nói — nửa dưới, mờ dần lên trên */}
    {/* mắt ~y 1400, miệng ~y 1620: trong dải lưới 3:4 (≤ 1680) */}
    <Img src={staticFile('v012/mat.jpg')} style={{position: 'absolute', left: 0, top: 1130, width: 1080, height: 790, objectFit: 'cover', objectPosition: '50% 33%'}} />
    <div style={{position: 'absolute', left: 0, right: 0, top: 1120, height: 260, background: 'linear-gradient(#110909 0%, rgba(17,9,9,.85) 40%, transparent 100%)'}} />
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 40%, rgba(232,54,54,.32), transparent 55%)'}} />

    {/* tiêu đề */}
    <div style={{position: 'absolute', left: 140, right: 140, top: 268, textAlign: 'center'}}>
      <div style={{fontWeight: 700, fontSize: 58, letterSpacing: 1, ...vien(8)}}>
        <Nhan chu="Robot lễ tân AI…" />
      </div>
      <div style={{...tieuDe(112), marginTop: 12, ...vien(16), filter: 'drop-shadow(0 6px 24px rgba(0,0,0,.6))'}}>
        <Nhan chu="Chỉ để" />
        <br />
        <Nhan chu="*chào khách?*" />
      </div>
    </div>

    <The left={140} nhan="Hôm nay" duoi="Chào · *đón khách*" src="v012/nova-mat.jpg" hop={[-6, -1135, 1210]} mau={DO} />
    <The left={570} nhan="Tương lai" duoi="+ *nhiều ứng dụng*" src="v012/ung-dung.jpg" hop={[-100, -250, 640]} mau={VANG} />

    {/* mũi tên giữa hai thẻ */}
    <div
      style={{
        position: 'absolute', left: 540 - 62, top: THE_TOP + THE_H / 2 - 62, width: 124, height: 124, borderRadius: '50%',
        background: DO, border: '8px solid #fff', boxShadow: '0 0 50px rgba(232,54,54,.9)', boxSizing: 'border-box',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}
    >
      <svg width={64} height={64} viewBox="0 0 64 64">
        <path d="M12 32 H50 M34 16 L50 32 L34 48" stroke="#fff" strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" fill="none" />
      </svg>
    </div>
  </AbsoluteFill>
);

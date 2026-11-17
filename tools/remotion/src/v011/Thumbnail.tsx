// Ảnh bìa video 011 — 1080×1920. Xuất: npx remotion still src/index.ts v011-thumbnail <ra.png>
// Lưới hồ sơ TikTok cắt giữa 3:4 (y 240–1680) → nội dung chính nằm trong dải đó.
// Bên "nhà máy" là HÌNH VẼ tay máy, không dùng ảnh T300: cạnh chữ "hàng tỷ" người xem sẽ tưởng T300 giá hàng tỷ (T300 = 320 triệu).
// Không logo, không số điện thoại. Hai con số là lời anh Trường nói trong video.
import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {DO, NAU, Nhan, TayMayNho, tieuDe, VANG, vien} from './chung';

const THE_TOP = 640;
const THE_H = 560;

const The: React.FC<{left: number; ten: string; gia: string; children: React.ReactNode}> = ({left, ten, gia, children}) => (
  <div
    style={{
      position: 'absolute',
      left,
      top: THE_TOP,
      width: 470,
      height: THE_H,
      borderRadius: 36,
      overflow: 'hidden',
      border: `6px solid ${DO}`,
      boxShadow: '0 0 60px rgba(232,54,54,.55)',
      background: '#1a0f0e',
    }}
  >
    {children}
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        top: 0,
        padding: '22px 0 40px',
        background: 'linear-gradient(rgba(0,0,0,.75), transparent)',
        ...tieuDe(58),
        color: '#fff',
        ...vien(8),
      }}
    >
      {ten}
    </div>
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
        padding: '60px 0 22px',
        background: 'linear-gradient(transparent, rgba(0,0,0,.85))',
        ...tieuDe(78),
        color: VANG,
        ...vien(12),
      }}
    >
      {gia}
    </div>
  </div>
);

export const Thumbnail: React.FC = () => (
  <AbsoluteFill style={{background: '#110909', fontFamily: 'Britti', color: '#fff', overflow: 'hidden'}}>
    {/* mặt anh Trường — nửa dưới, mờ dần lên trên */}
    <Img
      src={staticFile('v011/mat.jpg')}
      style={{position: 'absolute', left: 0, top: 990, width: 1080, height: 930, objectFit: 'cover', objectPosition: '50% 26%'}}
    />
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        top: 980,
        height: 330,
        background: 'linear-gradient(#110909 0%, rgba(17,9,9,.85) 35%, transparent 100%)',
      }}
    />
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 42%, rgba(232,54,54,.35), transparent 55%)'}} />

    {/* tiêu đề */}
    <div style={{position: 'absolute', left: 50, right: 50, top: 268, textAlign: 'center'}}>
      <div style={{fontWeight: 700, fontSize: 60, letterSpacing: 1, ...vien(8)}}>Cùng là robot…</div>
      <div style={{...tieuDe(138), marginTop: 10, ...vien(16), filter: 'drop-shadow(0 6px 24px rgba(0,0,0,.6))'}}>
        <Nhan chu="Vì sao" />
        <br />
        <Nhan chu="*giá chênh?*" />
      </div>
    </div>

    <The left={40} ten="Nhà máy" gia="Hàng tỷ">
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(ellipse at 50% 70%, rgba(232,54,54,.35), transparent 70%), #1a0f0e',
        }}
      />
      <svg viewBox="0 0 470 560" width={470} height={560} style={{position: 'absolute', inset: 0}}>
        <rect x={0} y={380} width={470} height={18} fill="#3a2a28" />
        {Array.from({length: 13}, (_, i) => (
          <path key={i} d={`M${i * 40},398 l20,0 l-14,26 h-20z`} fill={VANG} opacity={0.55} />
        ))}
        <rect x={280} y={292} width={120} height={88} rx={10} fill="#c98a3c" stroke={NAU} strokeWidth={4} />
        <rect x={280} y={292} width={120} height={18} fill={VANG} />
        <TayMayNho cx={130} cy={330} s={1.75} a1={22} a2={118} />
      </svg>
    </The>

    <The left={570} ten="Nhà hàng" gia="Hơn 100 triệu">
      <Img
        src={staticFile('v011/nha-hang.jpg')}
        style={{position: 'absolute', inset: 0, width: 470, height: THE_H, objectFit: 'cover', objectPosition: '62% 40%'}}
      />
    </The>

    <div
      style={{
        position: 'absolute',
        left: 470,
        top: THE_TOP + THE_H / 2 - 70,
        width: 140,
        height: 140,
        borderRadius: '50%',
        background: DO,
        border: '8px solid #fff',
        ...tieuDe(64),
        lineHeight: '124px',
        boxShadow: '0 0 60px rgba(232,54,54,.9)',
      }}
    >
      VS
    </div>
  </AbsoluteFill>
);

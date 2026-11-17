// Mở bài 0,0–8,5 s: "Tại sao cùng là robot, robot nhà máy hàng tỷ đồng, robot nhà hàng hơn 100 triệu".
// Chỉ có hai con số anh Trường nói: "hàng tỷ đồng", "hơn 100 triệu".
import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {bat, dap, DO, Nen, Nhan, NAU, pha, RobotPhucVu, TayMayNho, tieuDe, VANG, vien} from './chung';

const MOC = {tieuDe: 0.12, nhaMay: 1.95, hangTy: 3.5, nhaHang: 4.9, tram: 6.95};

const The: React.FC<{left: number; ten: string; hien: number; children: React.ReactNode; gia: React.ReactNode}> = ({
  left,
  ten,
  hien,
  children,
  gia,
}) => (
  <div
    style={{
      position: 'absolute',
      left,
      top: 345,
      width: 466,
      height: 592,
      borderRadius: 34,
      background: 'rgba(255,255,255,.045)',
      border: `4px solid ${NAU}`,
      textAlign: 'center',
      transform: `scale(${0.6 + 0.4 * hien})`,
      opacity: Math.min(1, hien * 1.5),
    }}
  >
    <div style={{...tieuDe(60), marginTop: 26}}>{ten}</div>
    <svg viewBox="0 0 466 330" width={466} height={300}>
      {children}
    </svg>
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 28}}>{gia}</div>
  </div>
);

export const SoGia: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;

  const hTd = bat(f, fps, MOC.tieuDe);
  const h1 = bat(f, fps, MOC.nhaMay, 13);
  const h2 = bat(f, fps, MOC.nhaHang, 13);
  const vs = bat(f, fps, MOC.nhaHang + 0.1, 9);

  // tay máy lắc qua lại, robot phục vụ nhún nhẹ + chớp mắt
  const lac = Math.sin((t - MOC.nhaMay) * 3.4);
  const a1 = -3 + 22 * lac;
  const a2 = 2 - 32 * lac;
  const nhun = -10 * Math.abs(Math.sin((t - MOC.nhaHang) * 3.2));
  const chop = t > 6.0 && t < 6.16 ? 0.12 : 1;

  // "hàng tỷ": đập + rung
  const rung = t > MOC.hangTy && t < MOC.hangTy + 0.45 ? Math.sin(t * 90) * 7 * (1 - (t - MOC.hangTy) / 0.45) : 0;
  // "hơn 100 triệu": số chạy 0 → 100
  const so = Math.round(pha(t, MOC.tram, MOC.tram + 0.55, 0, 100, Easing.out(Easing.quad)));
  const giaChu: React.CSSProperties = {...tieuDe(76), color: VANG, ...vien(10)};

  return (
    <Nen>
      <div
        style={{
          position: 'absolute',
          left: 40,
          right: 40,
          top: 246,
          ...tieuDe(74),
          transform: `scale(${hTd})`,
        }}
      >
        <Nhan chu="Vì sao *giá chênh*?" />
      </div>

      <The left={44} ten="Nhà máy" hien={h1} gia={<div style={{...giaChu, ...dap(t, MOC.hangTy), translate: `${rung}px 0`}}>Hàng tỷ<br />đồng</div>}>
        <rect x={40} y={292} width={386} height={16} rx={8} fill="#3a2a28" />
        <rect x={300} y={232} width={90} height={60} rx={8} fill="#c98a3c" stroke={VANG} strokeWidth={3} />
        <TayMayNho cx={180} cy={262} s={1.15} a1={a1} a2={a2} />
      </The>

      <The
        left={570}
        ten="Nhà hàng"
        hien={h2}
        gia={
          <div style={{...giaChu, opacity: t >= MOC.tram ? 1 : 0, transform: `scale(${t >= MOC.tram + 0.55 ? 1 + 0.08 * Math.sin(Math.min(Math.PI, (t - MOC.tram - 0.55) * 10)) : 1})`}}>
            Hơn {so}
            <br />
            triệu
          </div>
        }
      >
        <RobotPhucVu cx={233} cy={262} s={0.95} dy={nhun} nhay={chop} />
      </The>

      <div
        style={{
          position: 'absolute',
          left: 480,
          top: 560,
          width: 120,
          height: 120,
          borderRadius: '50%',
          background: DO,
          border: '6px solid #fff',
          ...tieuDe(54),
          lineHeight: '108px',
          boxShadow: '0 0 50px rgba(232,54,54,.8)',
          transform: `scale(${vs}) rotate(${(1 - Math.min(1, vs)) * -90}deg)`,
        }}
      >
        VS
      </div>
    </Nen>
  );
};

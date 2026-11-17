// 105,45 s → hết: "Tại Roboworld, chúng em đã cung cấp nhiều giải pháp robot từ nhà hàng, dịch vụ cho tới công nghiệp.
// Anh chị đang quan tâm chuyển đổi sang mô hình robot, vui lòng đến với em Trường để nhận tư vấn, thông tin và báo giá chi tiết ạ."
// Không logo, không số điện thoại (hotline chỉ ở caption).
import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {bat, DauTich, DO, NAU, Nen, Nhan, pha, RobotPhucVu, TayMayNho, tieuDe, VANG} from './chung';

const MOC = {giaiPhap: 0.9, o: [2.3, 2.8, 3.3], cauHoi: 3.85, nhan: 6.85, muc: [7.6, 8.35, 9.05]};

const RobotLeTan: React.FC = () => (
  <g>
    <ellipse cx={130} cy={70} rx={62} ry={50} fill="#f4f1ee" />
    <rect x={88} y={48} width={84} height={42} rx={14} fill="#111" />
    <circle cx={112} cy={69} r={8} fill="#5ef" />
    <circle cx={148} cy={69} r={8} fill="#5ef" />
    <rect x={92} y={122} width={76} height={110} rx={10} fill="#222" stroke="#f4f1ee" strokeWidth={6} />
    <rect x={102} y={134} width={56} height={86} rx={4} fill={DO} opacity={0.75} />
    <path d="M70,250 q60,-40 120,0 v10 h-120z" fill="#f4f1ee" />
  </g>
);

const O: React.FC<{left: number; ten: string; hien: number; mo: number; children: React.ReactNode}> = ({left, ten, hien, mo, children}) => (
  <div
    style={{
      position: 'absolute',
      left,
      top: 380,
      width: 300,
      height: 420,
      borderRadius: 30,
      background: 'rgba(255,255,255,.05)',
      border: `4px solid ${NAU}`,
      textAlign: 'center',
      transform: `scale(${(0.5 + 0.5 * hien) * (1 - 0.15 * (1 - mo))}) translateY(${(1 - mo) * -60}px)`,
      opacity: Math.min(1, hien * 1.5) * mo,
    }}
  >
    <svg viewBox="0 0 260 270" width={260} height={270} style={{marginTop: 30}}>
      {children}
    </svg>
    <div style={{...tieuDe(44), marginTop: 18}}>{ten}</div>
  </div>
);

export const Ket: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;

  const mo1 = pha(t, MOC.cauHoi - 0.2, MOC.cauHoi + 0.1, 1, 0, Easing.in(Easing.quad));
  const hGp = bat(f, fps, MOC.giaiPhap) * mo1;
  const hCh = bat(f, fps, MOC.cauHoi + 0.12, 12);
  const mo2 = pha(t, MOC.nhan - 0.3, MOC.nhan - 0.05, 1, 0);
  const hNh = bat(f, fps, MOC.nhan, 12);
  const lac = Math.sin(t * 3);

  return (
    <Nen>
      <div style={{position: 'absolute', left: 40, right: 40, top: 250, ...tieuDe(70), transform: `scale(${hGp})`}}>
        <Nhan chu="Giải pháp *robot*" />
      </div>
      <O left={45} ten="Nhà hàng" hien={bat(f, fps, MOC.o[0], 12)} mo={mo1}>
        <RobotPhucVu cx={130} cy={215} s={0.82} dy={-6 * Math.abs(lac)} />
      </O>
      <O left={390} ten="Dịch vụ" hien={bat(f, fps, MOC.o[1], 12)} mo={mo1}>
        <RobotLeTan />
      </O>
      <O left={735} ten="Công nghiệp" hien={bat(f, fps, MOC.o[2], 12)} mo={mo1}>
        <rect x={150} y={218} width={80} height={52} rx={8} fill="#c98a3c" stroke={VANG} strokeWidth={3} />
        <TayMayNho cx={95} cy={236} s={1} a1={8 + 18 * lac} a2={-4 - 26 * lac} />
      </O>

      {/* Anh chị đang quan tâm chuyển đổi sang mô hình robot? */}
      <div
        style={{
          position: 'absolute',
          left: 60,
          right: 60,
          top: 420,
          ...tieuDe(92),
          opacity: Math.min(1, hCh * 1.4) * mo2,
          transform: `scale(${0.6 + 0.4 * hCh})`,
        }}
      >
        <Nhan chu="Chuyển đổi sang *mô hình robot*?" />
      </div>

      {/* đến với em Trường để nhận: tư vấn · thông tin · báo giá chi tiết */}
      <div
        style={{
          position: 'absolute',
          left: 60,
          right: 60,
          top: 262,
          textAlign: 'center',
          fontWeight: 700,
          fontSize: 54,
          opacity: Math.min(1, hNh * 1.4),
          transform: `translateY(${(1 - hNh) * -40}px)`,
        }}
      >
        <Nhan chu="Đến với *em Trường* để nhận" />
      </div>
      <div style={{position: 'absolute', left: 230, top: 400}}>
        {['Tư vấn', 'Thông tin', 'Báo giá chi tiết'].map((chu, i) => {
          const b = bat(f, fps, MOC.muc[i], 10);
          return (
            <div
              key={chu}
              style={{
                display: 'flex',
                alignItems: 'center',
                marginBottom: 44,
                fontFamily: 'Neusharp',
                fontSize: 70,
                textTransform: 'uppercase',
                opacity: Math.min(1, b * 1.4),
                transform: `translateX(${(1 - b) * 90}px)`,
              }}
            >
              <DauTich co={78} ve={pha(t, MOC.muc[i] + 0.1, MOC.muc[i] + 0.4)} />
              <span style={{marginLeft: 28}}>{chu}</span>
            </div>
          );
        })}
      </div>
    </Nen>
  );
};

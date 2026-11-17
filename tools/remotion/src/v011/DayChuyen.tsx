// 50,5–61,6 s: "ứng dụng một chuỗi robot làm việc liên tục, tạo thành hệ thống tự động hoá,
// có thể cắt giảm hàng chục, hàng trăm nhân công, tạo nên một giá trị cực kỳ lớn cho nhà máy".
import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {bat, dap, DO, Nen, Nhan, pha, tieuDe, VANG, vien} from './chung';

const MOC = {tay: 2.4, heThong: 5.1, catGiam: 6.95, hangChuc: 7.6, hangTram: 8.3, mo: 9.2, giaTri: 9.6};
const BANG_Y = 500;
const TAY_X = [200, 420, 640, 860];
const NGUOI = Array.from({length: 45}, (_, i) => [90 + 64 * (i % 15), 640 + 62 * Math.floor(i / 15)]);

export const DayChuyen: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const conLai = t - MOC.giaTri;

  return (
    <Nen>
      <svg viewBox="0 0 1080 960" width={1080} height={960} style={{position: 'absolute', left: 0, top: 0}}>
        <rect x={0} y={BANG_Y} width={1080} height={34} fill="#2b2b2b" stroke="#6b5a55" strokeWidth={3} />
        {Array.from({length: 18}, (_, i) => {
          const x = 30 + 60 * i;
          const y = BANG_Y + 17;
          const quay = t * 360;
          return (
            <g key={i} transform={`rotate(${quay} ${x} ${y})`}>
              <circle cx={x} cy={y} r={11} fill="#6b5a55" />
              <rect x={x - 1.5} y={y - 11} width={3} height={22} fill="#2b2b2b" />
            </g>
          );
        })}
        {/* hộp chạy trên băng chuyền: cứ 0,75 s một hộp, mỗi hộp đi hết băng trong 4,2 s */}
        {Array.from({length: 16}, (_, k) => {
          const u = (t - 0.3 - k * 0.75) / 4.2;
          if (u < 0 || u > 1) return null;
          return (
            <g key={k} transform={`translate(${-100 + u * 1280} ${BANG_Y - 60})`}>
              <rect width={76} height={60} rx={6} fill="#c98a3c" stroke="#5E0F18" strokeWidth={3} />
              <rect width={76} height={12} fill={VANG} />
            </g>
          );
        })}
        {TAY_X.map((x, i) => {
          const vao = bat(f, fps, MOC.tay + i * 0.3, 12);
          const bd = MOC.tay + 0.8 + i * 0.22;
          const ep = t > bd ? 34 * (0.5 - 0.5 * Math.cos(((t - bd) / 0.7) * 2 * Math.PI)) : 0;
          return (
            <g key={i} transform={`translate(0 ${(1 - vao) * -200})`} opacity={Math.min(1, vao * 1.5)}>
              <rect x={x - 40} y={330} width={80} height={24} rx={8} fill="#3a2a28" stroke={DO} strokeWidth={3} />
              <g transform={`translate(0 ${ep})`}>
                <rect x={x - 12} y={350} width={24} height={90} rx={10} fill={DO} />
                <path d={`M${x - 16},440 l-8,22 M${x + 16},440 l8,22`} stroke={VANG} strokeWidth={8} strokeLinecap="round" />
              </g>
              <circle cx={x} cy={352} r={13} fill="#5E0F18" stroke="#fff" strokeWidth={3} />
            </g>
          );
        })}
        {NGUOI.map(([x, y], i) => {
          const luc = i < 15 ? MOC.hangChuc + i * 0.03 : MOC.hangTram + (i - 15) * 0.02;
          const v = bat(f, fps, luc, 12);
          const mo = pha(t, MOC.mo + i * 0.006, MOC.mo + 0.5 + i * 0.006, 1, 0.16);
          return (
            <g key={i} transform={`translate(${x} ${y}) scale(${v})`} opacity={Math.min(1, v) * mo}>
              <circle cy={-14} r={11} fill="#FAB29A" />
              <path d="M-17,18 q0,-22 17,-22 q17,0 17,22z" fill="#FAB29A" />
            </g>
          );
        })}
      </svg>

      <div style={{position: 'absolute', left: 30, right: 30, top: 246, ...tieuDe(66), ...dap(t, MOC.heThong, 1.8)}}>
        <Nhan chu="Dây chuyền *tự động hoá*" />
      </div>

      <div
        style={{
          position: 'absolute',
          left: 40,
          right: 40,
          top: 850,
          textAlign: 'center',
          fontWeight: 700,
          fontSize: 46,
          lineHeight: 1.1,
          opacity: pha(t, MOC.catGiam, MOC.catGiam + 0.3) * pha(t, MOC.giaTri - 0.25, MOC.giaTri - 0.05, 1, 0),
          transform: `translateY(${pha(t, MOC.catGiam, MOC.catGiam + 0.3, 30, 0)}px)`,
        }}
      >
        <Nhan chu="Cắt giảm *hàng chục, hàng trăm* nhân công" />
      </div>

      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: 640,
          ...tieuDe(86),
          color: VANG,
          ...vien(12),
          filter: 'drop-shadow(0 0 30px rgba(232,54,54,.9))',
          opacity: pha(t, MOC.giaTri, MOC.giaTri + 0.18),
          transform: `scale(${conLai < 0.3 ? pha(t, MOC.giaTri, MOC.giaTri + 0.3, 2.2, 1, Easing.out(Easing.poly(4))) : 1 + (conLai - 0.3) * 0.04})`,
        }}
      >
        Giá trị cực kỳ lớn
      </div>
    </Nen>
  );
};

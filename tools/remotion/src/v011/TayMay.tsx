// 43,6–50,5 s: "robot trong nhà máy thay thế những công việc mang tính chính xác cao, nặng nhọc, nguy hiểm".
// Tay máy 2 khâu gắp – nhấc – đặt hộp, góc khớp tính bằng động học ngược (IK).
import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {bat, DO, NAU, Nen, Nhan, pha, tieuDe, VANG} from './chung';

const L1 = 240;
const L2 = 210;
const G = 46;
const VAI: [number, number] = [150, 800];
const SAN = 880;
const HOP_W = 120;
const HOP_H = 96;

const rad = (d: number) => (d * 180) / Math.PI;

/** Góc (độ, thuận chiều kim đồng hồ từ hướng lên) của vai a1 và khuỷu a2 để cổ tay tới (wx, wy). Chọn khuỷu cao hơn. */
const ik = (wx: number, wy: number): [number, number] => {
  const dx = wx - VAI[0];
  const dy = wy - VAI[1];
  const d = Math.hypot(dx, dy);
  const q2 = Math.acos(Math.max(-1, Math.min(1, (d * d - L1 * L1 - L2 * L2) / (2 * L1 * L2))));
  const phi = Math.atan2(dx, -dy);
  const k = Math.atan2(L2 * Math.sin(q2), L1 + L2 * Math.cos(q2));
  const nghiem: [number, number][] = [
    [phi + k, -q2],
    [phi - k, q2],
  ];
  nghiem.sort((a, b) => -Math.cos(a[0]) + Math.cos(b[0]));
  return [rad(nghiem[0][0]), rad(nghiem[0][1])];
};

const TU_THE = {
  gap: ik(330, SAN - HOP_H - G),
  dat: ik(545, SAN - HOP_H - G),
  nhac: ik(420, 470),
};
type TuThe = keyof typeof TU_THE;

// [giây, tư thế] — giữa hai mốc chạy mượt (power2.inOut)
const KHUNG: [number, TuThe][] = [
  [0, 'nhac'], [0.35, 'nhac'], [1.1, 'gap'], [1.3, 'gap'], [2.1, 'nhac'], [2.9, 'dat'], [3.1, 'dat'],
  [3.7, 'nhac'], [3.75, 'nhac'], [4.5, 'gap'], [4.7, 'gap'], [5.5, 'nhac'], [6.3, 'dat'], [99, 'dat'],
];
const muot = Easing.inOut(Easing.quad);

const goc = (t: number): [number, number] => {
  for (let i = 0; i < KHUNG.length - 1; i++) {
    const [ta, a] = KHUNG[i];
    const [tb, b] = KHUNG[i + 1];
    if (t <= tb) {
      const p = muot(Math.max(0, Math.min(1, (t - ta) / (tb - ta))));
      return [TU_THE[a][0] + (TU_THE[b][0] - TU_THE[a][0]) * p, TU_THE[a][1] + (TU_THE[b][1] - TU_THE[a][1]) * p];
    }
  }
  return TU_THE.dat;
};

const Hop: React.FC<{x: number; y: number; dx?: number; op?: number}> = ({x, y, dx = 0, op = 1}) => (
  <g transform={`translate(${dx} 0)`} opacity={op}>
    <rect x={x - HOP_W / 2} y={y} width={HOP_W} height={HOP_H} rx={8} fill="#c98a3c" stroke={NAU} strokeWidth={4} />
    <rect x={x - HOP_W / 2} y={y} width={HOP_W} height={18} fill={VANG} />
    {[0, 1, 2, 3, 4].map((i) => (
      <path key={i} d={`M${x - HOP_W / 2 + 6 + 22 * i},${y + 18} l14,-18 h8 l-14,18z`} fill="#111" />
    ))}
  </g>
);

const Y_LIST: [number, string][] = [
  [2.1, 'Thay *con người*'],
  [3.2, 'Độ *chính xác cao*'],
  [4.2, 'Việc *nặng nhọc*'],
  [5.9, 'Việc *nguy hiểm*'],
];

export const TayMay: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const [a1, a2] = goc(t);
  const [cx, cy] = VAI;
  const wx0 = cx;
  const wy0 = cy - L1 - L2;

  const dong = (t >= 1.12 && t < 2.95) || (t >= 4.52 && t < 6.35);
  const ngon = dong ? 10 : 0;
  const trongKep = (t >= 1.25 && t < 3.0) || (t >= 4.65 && t < 6.4);
  // hộp ở chỗ gắp
  const hA = t < 1.25 ? 1 : t >= 3.1 && t < 4.65 ? 1 : 0;
  const hAdx = t >= 3.1 ? pha(t, 3.1, 3.7, -220, 0, Easing.out(Easing.quad)) : 0;
  // hộp ở chỗ đặt
  const hB = t >= 3.0 && t < 4.6 ? pha(t, 4.0, 4.6, 1, 0, Easing.in(Easing.quad)) : t >= 6.4 ? 1 : 0;
  const hBdx = t >= 3.0 && t < 4.6 ? pha(t, 4.0, 4.6, 0, 220, Easing.in(Easing.quad)) : 0;

  return (
    <Nen>
      <svg viewBox="0 0 640 960" width={640} height={960} style={{position: 'absolute', left: 0, top: 0}}>
        <rect x={20} y={SAN} width={600} height={14} fill="#3a2a28" />
        {Array.from({length: 15}, (_, i) => (
          <path key={i} d={`M${20 + 40 * i},${SAN + 14} l20,0 l-14,26 h-20z`} fill={VANG} opacity={0.55} />
        ))}
        <Hop x={330} y={SAN - HOP_H} dx={hAdx} op={hA} />
        <Hop x={545} y={SAN - HOP_H} dx={hBdx} op={hB} />
        <rect x={cx - 70} y={cy} width={140} height={80} rx={12} fill="#3a2a28" stroke={DO} strokeWidth={4} />
        <g transform={`rotate(${a1} ${cx} ${cy})`}>
          <rect x={cx - 26} y={cy - L1} width={52} height={L1} rx={24} fill={DO} />
          <g transform={`rotate(${a2} ${cx} ${cy - L1})`}>
            <rect x={cx - 20} y={wy0} width={40} height={L2} rx={20} fill="#f4f1ee" />
            <g transform={`rotate(${-(a1 + a2)} ${wx0} ${wy0})`}>
              <Hop x={wx0} y={wy0 + G} op={trongKep ? 1 : 0} />
              <rect x={wx0 - 40} y={wy0} width={80} height={22} rx={8} fill={NAU} />
              <rect x={wx0 - 46 + ngon} y={wy0 + 12} width={14} height={G + 20} rx={6} fill={VANG} />
              <rect x={wx0 + 32 - ngon} y={wy0 + 12} width={14} height={G + 20} rx={6} fill={VANG} />
            </g>
            <circle cx={cx} cy={wy0} r={18} fill={NAU} stroke="#fff" strokeWidth={4} />
          </g>
          <circle cx={cx} cy={cy - L1} r={26} fill={NAU} stroke="#fff" strokeWidth={4} />
        </g>
        <circle cx={cx} cy={cy} r={34} fill={NAU} stroke="#fff" strokeWidth={5} />
      </svg>

      <div
        style={{
          position: 'absolute',
          left: 0,
          width: 640,
          top: 250,
          ...tieuDe(58),
          opacity: pha(t, 0.15, 0.45),
          transform: `translateY(${pha(t, 0.15, 0.45, -30, 0)}px)`,
        }}
      >
        Robot nhà máy
      </div>

      <div style={{position: 'absolute', left: 640, right: 34, top: 360}}>
        {Y_LIST.map(([luc, chu]) => {
          const b = bat(f, fps, luc, 10);
          return (
            <div
              key={chu}
              style={{
                marginBottom: 34,
                padding: '16px 20px',
                borderRadius: 20,
                background: 'rgba(255,255,255,.06)',
                borderLeft: `10px solid ${DO}`,
                fontWeight: 700,
                fontSize: 42,
                lineHeight: 1.1,
                opacity: Math.min(1, b * 1.4),
                transform: `translateX(${(1 - b) * 80}px)`,
              }}
            >
              <Nhan chu={chu} />
            </div>
          );
        })}
      </div>
    </Nen>
  );
};

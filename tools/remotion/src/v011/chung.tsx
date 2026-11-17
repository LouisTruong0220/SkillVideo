// Dùng chung cho các cảnh Remotion của video 011 (bảng nửa trên 1080×960, ghép vào HyperFrames dưới dạng canh-phu).
import React from 'react';
import {AbsoluteFill, continueRender, delayRender, Easing, interpolate, spring, staticFile} from 'remotion';

// Font thương hiệu bản WOFF2 đã bỏ hint (TTF gốc làm Chromium vẽ "c" thành "o" ở cỡ ≥20px).
const FONTS: [string, string, string][] = [
  ['Neusharp', '1FTV-VIP-NEUSHARP-BOLD.woff2', '700'],
  ['Britti', 'DFVN-BrittiSans-Bold.woff2', '700'],
  ['Britti', 'DFVN-BrittiSans-SemiBold.woff2', '600'],
  ['Britti', 'DFVN-BrittiSans-Regular.woff2', '400'],
];
const cho = delayRender('nạp font');
Promise.all(
  FONTS.map(([ten, file, w]) =>
    new FontFace(ten, `url(${staticFile('fonts/' + file)}) format('woff2')`, {weight: w}).load().then((f) => {
      document.fonts.add(f);
    }),
  ),
).then(() => continueRender(cho));

export const DO = '#E83636';
export const DO_DAM = '#C13F28';
export const NAU = '#5E0F18';
export const VANG = '#FFD43B';
export const W = 1080;
export const H = 960;

const kep = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** Giá trị chạy từ `tu` tới `den` trong khoảng giây [a, b]. */
export const pha = (t: number, a: number, b: number, tu = 0, den = 1, e = Easing.out(Easing.cubic)) =>
  interpolate(t, [a, b], [tu, den], {...kep, easing: e});

/** Lò xo bật 0 → 1 (có vọt) bắt đầu ở giây `luc`. */
export const bat = (f: number, fps: number, luc: number, damping = 11) =>
  spring({frame: Math.max(0, f - luc * fps), fps, config: {damping, stiffness: 190, mass: 0.8}}) * (f >= luc * fps ? 1 : 0);

/** Đập mạnh: từ `to` (vd 2.2) về 1 nhanh, kèm hiện dần. */
export const dap = (t: number, luc: number, to = 2.2, dai = 0.28) => ({
  transform: `scale(${pha(t, luc, luc + dai, to, 1, Easing.out(Easing.poly(4)))})`,
  opacity: pha(t, luc, luc + dai * 0.6),
});

/** Chuỗi có *từ* → tô vàng. */
export const Nhan: React.FC<{chu: string; mau?: string}> = ({chu, mau = VANG}) => (
  <>
    {chu.split('*').map((x, i) =>
      i % 2 ? (
        <span key={i} style={{color: mau}}>
          {x}
        </span>
      ) : (
        <React.Fragment key={i}>{x}</React.Fragment>
      ),
    )}
  </>
);

/** Nền bảng chuẩn: tối gần đen + vệt sáng đỏ tụ giữa-dưới + viền đỏ đáy. */
export const Nen: React.FC<{children: React.ReactNode}> = ({children}) => (
  <AbsoluteFill
    style={{
      background: 'radial-gradient(ellipse at 50% 118%, rgba(232,54,54,.42), transparent 62%), #110909',
      borderBottom: `8px solid ${DO}`,
      overflow: 'hidden',
      fontFamily: 'Britti',
      color: '#fff',
    }}
  >
    {children}
  </AbsoluteFill>
);

export const tieuDe = (co: number): React.CSSProperties => ({
  fontFamily: 'Neusharp',
  fontWeight: 700,
  fontSize: co,
  lineHeight: 1.04,
  textTransform: 'uppercase',
  textAlign: 'center',
});

export const vien = (px: number, mau = '#000'): React.CSSProperties => ({
  WebkitTextStroke: `${px}px ${mau}`,
  paintOrder: 'stroke fill',
});

/** Robot phục vụ cách điệu (đầu màn hình mắt mèo, 3 khay). Gốc (cx, cy) = giữa thân dưới. */
export const RobotPhucVu: React.FC<{cx: number; cy: number; s?: number; nhay?: number; dy?: number}> = ({
  cx,
  cy,
  s = 1,
  nhay = 1,
  dy = 0,
}) => {
  const w = 150 * s;
  return (
    <g transform={`translate(0 ${dy})`}>
      <rect x={cx - w / 2} y={cy - 260 * s} width={w} height={300 * s} rx={40 * s} fill="#f4f1ee" />
      <rect x={cx - 62 * s} y={cy - 245 * s} width={124 * s} height={82 * s} rx={22 * s} fill="#111" />
      {[-26, 26].map((d) => (
        <ellipse key={d} cx={cx + d * s} cy={cy - 204 * s} rx={14 * s} ry={17 * s * nhay} fill="#5ef" />
      ))}
      {[0, 1, 2].map((i) => (
        <rect key={i} x={cx - 90 * s} y={cy + (-140 + 55 * i) * s} width={180 * s} height={14 * s} rx={7 * s} fill="#2b2b2b" />
      ))}
      <ellipse cx={cx} cy={cy + 48 * s} rx={88 * s} ry={18 * s} fill={DO} opacity={0.85} />
    </g>
  );
};

/** Cánh tay công nghiệp nhỏ nhìn ngang; a1/a2 là góc (độ) của hai khâu. */
export const TayMayNho: React.FC<{cx: number; cy: number; s?: number; a1: number; a2: number}> = ({cx, cy, s = 1, a1, a2}) => {
  const L1 = 110 * s;
  const L2 = 90 * s;
  return (
    <g>
      <rect x={cx - 50 * s} y={cy} width={100 * s} height={30 * s} rx={8 * s} fill="#3a2a28" stroke={DO} strokeWidth={3} />
      <g transform={`rotate(${a1} ${cx} ${cy})`}>
        <rect x={cx - 13 * s} y={cy - L1} width={26 * s} height={L1} rx={12 * s} fill={DO} />
        <circle cx={cx} cy={cy} r={20 * s} fill={NAU} stroke="#fff" strokeWidth={3} />
        <g transform={`rotate(${a2} ${cx} ${cy - L1})`}>
          <rect x={cx - 10 * s} y={cy - L1 - L2} width={20 * s} height={L2} rx={10 * s} fill="#fff" />
          <circle cx={cx} cy={cy - L1} r={15 * s} fill={NAU} stroke="#fff" strokeWidth={3} />
          <path
            d={`M${cx - 18 * s},${cy - L1 - L2} l-8,-26 M${cx + 18 * s},${cy - L1 - L2} l8,-26`}
            stroke={VANG}
            strokeWidth={8 * s}
            strokeLinecap="round"
          />
        </g>
      </g>
    </g>
  );
};

/** Dấu tích vẽ bằng SVG (font Britti không có ký tự ✔). */
export const DauTich: React.FC<{co?: number; ve?: number}> = ({co = 64, ve = 1}) => (
  <svg width={co} height={co} viewBox="0 0 64 64" style={{flex: 'none'}}>
    <circle cx={32} cy={32} r={30} fill={DO} />
    <path
      d="M17 33 l10 10 l20 -22"
      fill="none"
      stroke="#fff"
      strokeWidth={7}
      strokeLinecap="round"
      strokeLinejoin="round"
      pathLength={1}
      strokeDasharray="1 1"
      strokeDashoffset={1 - ve}
    />
  </svg>
);

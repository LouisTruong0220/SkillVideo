// Video 012 · 2,6 s → 15,1 s trên bản cắt (cảnh dài 12,5 s). Mốc = giây tính từ đầu cảnh (mốc bản cắt − 2,6).
// Lời: "điện thoại rất là xịn, thậm chí đắt tiền, nhưng chỉ được sử dụng tính năng nghe và gọi … có muốn mua không?
//       Chắc chắn là không rồi. Vẫn một chiếc điện thoại đấy, nhưng bên trong được cập nhật nhiều phần mềm hơn
//       thì các anh chị sẽ có nhiều cơ hội và ứng dụng được nhiều hơn trong cuộc sống."
import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {bat, DO, DO_DAM, NAU, Nen, Nhan, pha, tieuDe, VANG} from '../v011/chung';

const MOC = {
  vao: 0, sang: 0.3, man: 1.05, ngheGoi: 2.15, // "nghe và gọi" 4,74
  khong: 5.0, // "Chắc chắn là không rồi" 7,61
  van: 5.9, // "Vẫn một chiếc điện thoại đấy" 8,47
  capNhat: 7.85, // "cập nhật nhiều" 10,47
  phanMem: 8.6, // "phần mềm hơn" 11,20
  coHoi: 10.0, // "có nhiều cơ hội" 12,64
  ungDung: 11.05, // "ứng dụng được nhiều" 13,67
};

// Thân máy: x 400–680, y 350–870
const X0 = 400, Y0 = 350, PW = 280, PH = 520;
const MX0 = X0 + 16, MY0 = Y0 + 30, MW = PW - 32, MH = PH - 60;
const COT = [MX0 + 52, MX0 + MW / 2, MX0 + MW - 52];
const HANG = [MY0 + 80, MY0 + 172, MY0 + 264, MY0 + 356];
const MAU = [DO, VANG, '#FAB29A', '#fff', DO_DAM, VANG, '#FAB29A', DO, '#fff', VANG, DO, '#FAB29A'];

const OngNghe: React.FC<{x: number; y: number; s: number}> = ({x, y, s}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <circle r={44} fill={DO} />
    <path d="M-20,-14 q4,-10 12,-6 l6,10 q2,5 -3,8 l-4,3 q6,12 18,18 l3,-4 q3,-5 8,-3 l10,6 q4,8 -6,12 q-26,4 -44,-44z" fill="#fff" />
  </g>
);
const Loa: React.FC<{x: number; y: number; s: number}> = ({x, y, s}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <circle r={44} fill={VANG} />
    <path d="M-20,-8 h10 l14,-12 v40 l-14,-12 h-10z" fill="#110909" />
    <path d="M10,-10 q8,10 0,20 M17,-17 q15,17 0,34" stroke="#110909" strokeWidth={5} fill="none" strokeLinecap="round" />
  </g>
);

export const DienThoai: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;

  const vao = bat(f, fps, MOC.vao, 13);
  const man = pha(t, MOC.man, MOC.man + 0.3);
  const ng = bat(f, fps, MOC.ngheGoi, 10);
  const x = bat(f, fps, MOC.khong, 9) * pha(t, MOC.van - 0.15, MOC.van + 0.15, 1, 0);
  const mo = pha(t, MOC.khong, MOC.khong + 0.2, 1, 0.35) * 1 + pha(t, MOC.van, MOC.van + 0.25, 0, 0.65);
  const van = bat(f, fps, MOC.van, 9);
  const tienDo = pha(t, MOC.capNhat + 0.1, MOC.phanMem, 0, 1, Easing.inOut(Easing.quad));
  const thanhCN = pha(t, MOC.capNhat, MOC.capNhat + 0.2) * pha(t, MOC.phanMem + 0.1, MOC.phanMem + 0.35, 1, 0);
  const anNgheGoi = pha(t, MOC.phanMem - 0.1, MOC.phanMem + 0.15, 1, 0);
  const sang = pha(t, MOC.ungDung, MOC.ungDung + 0.3) * (0.6 + 0.4 * Math.sin((t - MOC.ungDung) * 6));
  const phong = 1 + 0.05 * bat(f, fps, MOC.ungDung, 12) - 0.05 * pha(t, MOC.ungDung + 0.4, MOC.ungDung + 0.9);
  const lacVan = van > 0 && t < MOC.van + 0.6 ? Math.sin((t - MOC.van) * 30) * 4 * (1 - (t - MOC.van) / 0.6) : 0;

  const nhan1 = bat(f, fps, MOC.ngheGoi, 12) * pha(t, MOC.khong - 0.25, MOC.khong, 1, 0);
  const nhan2 = bat(f, fps, MOC.phanMem, 12);

  return (
    <Nen>
      {/* nhãn trên — chữ ở top ≥ 250 */}
      <div style={{position: 'absolute', left: 60, right: 140, top: 254, ...tieuDe(62), opacity: Math.min(1, nhan1 * 1.4), transform: `scale(${0.6 + 0.4 * nhan1})`}}>
        <Nhan chu="Chỉ *nghe và gọi*?" />
      </div>
      <div style={{position: 'absolute', left: 60, right: 140, top: 254, ...tieuDe(62), opacity: Math.min(1, nhan2 * 1.4), transform: `scale(${0.6 + 0.4 * nhan2})`}}>
        <Nhan chu="+ *Nhiều phần mềm*" />
      </div>

      <svg viewBox="0 0 1080 960" width={1080} height={960} style={{position: 'absolute', left: 0, top: 0}}>
        <defs>
          <clipPath id="v012-may">
            <rect x={X0} y={Y0} width={PW} height={PH} rx={46} />
          </clipPath>
          <linearGradient id="v012-man" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#3a1714" />
            <stop offset="1" stopColor="#120808" />
          </linearGradient>
        </defs>
        <g
          transform={`translate(${540 + lacVan} ${Y0 + PH / 2}) scale(${(0.55 + 0.45 * vao) * phong}) translate(-540 ${-(Y0 + PH / 2)})`}
          opacity={Math.min(1, vao * 1.5) * (x > 0.01 ? 1 - 0.55 * x : 1)}
        >
          {/* viền sáng khi "ứng dụng được nhiều hơn" */}
          <rect x={X0 - 14} y={Y0 - 14} width={PW + 28} height={PH + 28} rx={58} fill="none" stroke={VANG} strokeWidth={8} opacity={sang} />
          <rect x={X0} y={Y0} width={PW} height={PH} rx={46} fill="#1d1515" stroke="#e9e3df" strokeWidth={7} />
          <rect x={MX0} y={MY0} width={MW} height={MH} rx={22} fill="#060303" />
          <rect x={MX0} y={MY0} width={MW} height={MH} rx={22} fill="url(#v012-man)" opacity={man} />
          <rect x={540 - 40} y={Y0 + 12} width={80} height={10} rx={5} fill="#0b0707" />

          {/* ô trống — máy "chỉ nghe gọi" */}
          {HANG.map((y, r) =>
            COT.map((cx, c) => {
              const i = r * 3 + c;
              const app = bat(f, fps, MOC.phanMem + i * 0.07, 11);
              return (
                <g key={i}>
                  <rect x={cx - 34} y={y - 34} width={68} height={68} rx={18} fill="none" stroke="rgba(255,255,255,.18)" strokeWidth={3} strokeDasharray="8 8" opacity={man * (1 - app)} />
                  <g transform={`translate(${cx} ${y}) scale(${app}) translate(${-cx} ${-y})`}>
                    <rect x={cx - 34} y={y - 34} width={68} height={68} rx={18} fill={MAU[i]} />
                    <circle cx={cx} cy={y} r={13} fill={MAU[i] === '#fff' || MAU[i] === VANG || MAU[i] === '#FAB29A' ? NAU : '#fff'} opacity={0.85} />
                  </g>
                </g>
              );
            }),
          )}

          {/* hai chức năng duy nhất: Gọi · Nghe */}
          <g opacity={anNgheGoi}>
            <OngNghe x={COT[0] + 18} y={HANG[1] + 46} s={ng} />
            <Loa x={COT[2] - 18} y={HANG[1] + 46} s={ng} />
          </g>

          {/* thanh cập nhật */}
          <g opacity={thanhCN}>
            <rect x={MX0 + 30} y={MY0 + MH - 70} width={MW - 60} height={18} rx={9} fill="rgba(255,255,255,.15)" />
            <rect x={MX0 + 30} y={MY0 + MH - 70} width={(MW - 60) * tienDo} height={18} rx={9} fill={VANG} />
          </g>

          {/* lớp sáng lướt qua: "rất là xịn" */}
          <g clipPath="url(#v012-may)">
            <rect x={pha(t, MOC.sang, MOC.sang + 0.8, 200, 820)} y={Y0 - 100} width={70} height={PH + 200} fill="#fff" opacity={0.18} transform={`rotate(18 540 ${Y0 + PH / 2})`} />
          </g>
        </g>

        {/* nhãn chữ dưới hai biểu tượng — đặt ngoài nhóm co giãn để không nhoè */}
        <g opacity={Math.min(1, ng * 1.3) * anNgheGoi * (1 - 0.55 * x)} fontFamily="Britti" fontWeight={700} fontSize={30} fill="#fff" textAnchor="middle">
          <text x={COT[0] + 18} y={HANG[1] + 124}>Gọi</text>
          <text x={COT[2] - 18} y={HANG[1] + 124}>Nghe</text>
        </g>

        {/* lấp lánh "đắt tiền" */}
        {[
          [330, 420, 0.35],
          [760, 470, 0.5],
          [720, 800, 0.65],
        ].map(([cx, cy, d], i) => {
          const s = bat(f, fps, MOC.sang + d, 9) * pha(t, MOC.sang + d + 0.7, MOC.sang + d + 1.1, 1, 0);
          return (
            <path key={i} d={`M${cx},${cy - 30} Q${cx + 5},${cy - 5} ${cx + 30},${cy} Q${cx + 5},${cy + 5} ${cx},${cy + 30} Q${cx - 5},${cy + 5} ${cx - 30},${cy} Q${cx - 5},${cy - 5} ${cx},${cy - 30}Z`} fill={VANG} transform={`translate(${cx} ${cy}) scale(${s}) translate(${-cx} ${-cy})`} />
          );
        })}

        {/* dấu X: "Chắc chắn là không rồi" */}
        <g transform={`translate(540 610) scale(${0.4 + 0.6 * x}) rotate(${(1 - x) * -20})`} opacity={Math.min(1, x * 1.5)}>
          <path d="M-150,-150 L150,150 M150,-150 L-150,150" stroke={DO} strokeWidth={44} strokeLinecap="round" />
        </g>
      </svg>
    </Nen>
  );
};

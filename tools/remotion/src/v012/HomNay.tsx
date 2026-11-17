// Video 012 · 19,6 s → 29,5 s (9,9 s). Mốc = giây từ đầu cảnh (bản cắt − 19,6).
// Lời: "…đáp ứng được những nhu cầu như là giao tiếp AI bằng tiếng Việt hay là đi lại đón khách. Tuy nhiên đó chỉ là
//       những nhu cầu ở thời điểm hiện tại, trong tương lai công nghệ sẽ phát triển rất là nhanh anh chị ạ."
import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {bat, DO, Nen, Nhan, pha, VANG} from '../v011/chung';

const MOC = {nhan: 0.2, the1: 1.0, the2: 3.2, hienTai: 6.3, tuongLai: 6.7, ve: 7.0, nhanh: 8.6};

const Tich: React.FC<{ve: number}> = ({ve}) => (
  <svg width={86} height={86} viewBox="0 0 86 86" style={{flex: 'none'}}>
    <circle cx={43} cy={43} r={40} fill={VANG} />
    <path d="M24 44 L38 58 L63 30" fill="none" stroke="#110909" strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - ve} />
  </svg>
);

const The: React.FC<{top: number; hien: number; ve: number; chu: string}> = ({top, hien, ve, chu}) => (
  <div
    style={{
      position: 'absolute', left: 90, top, width: 830, height: 150, borderRadius: 30, boxSizing: 'border-box',
      border: '4px solid rgba(255,255,255,.22)', background: 'rgba(255,255,255,.06)',
      display: 'flex', alignItems: 'center', gap: 34, padding: '0 36px',
      opacity: Math.min(1, hien * 1.4), transform: `translateX(${(1 - hien) * -140}px)`,
    }}
  >
    <Tich ve={ve} />
    <div style={{fontWeight: 700, fontSize: 56, whiteSpace: 'nowrap'}}>
      <Nhan chu={chu} />
    </div>
  </div>
);

// Đường cong tăng tốc: hàm mũ, vẽ bằng điểm để biết điểm đầu bút (chấm sáng chạy theo)
const DIEM = Array.from({length: 61}, (_, i) => {
  const u = i / 60;
  return [110 + u * 790, 820 - 370 * (Math.exp(3.2 * u) - 1) / (Math.exp(3.2) - 1)] as const;
});

export const HomNay: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;

  const di = pha(t, MOC.tuongLai, MOC.tuongLai + 0.35, 0, 1, Easing.in(Easing.quad));
  const nhanNay = bat(f, fps, MOC.nhan, 12);
  const nhay = 1 + 0.12 * Math.sin(Math.PI * pha(t, MOC.hienTai, MOC.hienTai + 0.3, 0, 1, Easing.linear));
  const tl = bat(f, fps, MOC.tuongLai + 0.15, 11);
  // vẽ tới 55% rồi vút nốt khi nói "rất là nhanh"
  const ve = pha(t, MOC.ve, MOC.ve + 1.2, 0, 0.55) + pha(t, MOC.nhanh, MOC.nhanh + 0.45, 0, 0.45, Easing.in(Easing.quad));
  const n = Math.max(1, Math.round(ve * 60));
  const d = DIEM.slice(0, n + 1).map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`).join(' ');
  const [bx, by] = DIEM[n];
  const ghi = bat(f, fps, MOC.nhanh, 12);
  const muiTen = pha(t, MOC.nhanh + 0.4, MOC.nhanh + 0.5);

  return (
    <Nen>
      {/* nhóm HÔM NAY */}
      <div style={{position: 'absolute', inset: 0, opacity: 1 - di, transform: `translateX(${-260 * di}px)`}}>
        <div
          style={{
            position: 'absolute', left: 90, top: 250, padding: '14px 34px', borderRadius: 999, background: DO,
            fontFamily: 'Neusharp', fontSize: 58, lineHeight: 1, letterSpacing: 2,
            transform: `scale(${nhanNay * nhay})`, transformOrigin: '0% 50%',
          }}
        >
          HÔM NAY
        </div>
        <The top={420} hien={bat(f, fps, MOC.the1, 12)} ve={pha(t, MOC.the1 + 0.25, MOC.the1 + 0.55)} chu="Giao tiếp AI *tiếng Việt*" />
        <The top={610} hien={bat(f, fps, MOC.the2, 12)} ve={pha(t, MOC.the2 + 0.25, MOC.the2 + 0.55)} chu="Đi lại · *đón khách*" />
      </div>

      {/* nhóm TƯƠNG LAI */}
      <div style={{position: 'absolute', inset: 0, opacity: tl > 0 ? 1 : 0}}>
        <div
          style={{
            position: 'absolute', right: 160, top: 250, padding: '14px 34px', borderRadius: 999, border: `5px solid ${VANG}`,
            color: VANG, fontFamily: 'Neusharp', fontSize: 58, lineHeight: 1, letterSpacing: 2,
            transform: `scale(${tl})`, transformOrigin: '100% 50%',
          }}
        >
          TƯƠNG LAI
        </div>
        <svg viewBox="0 0 1080 960" width={1080} height={960} style={{position: 'absolute', left: 0, top: 0}}>
          <path d="M90 840 H930 M90 840 V440" stroke="rgba(255,255,255,.25)" strokeWidth={4} fill="none" opacity={tl} />
          <path d={d} stroke={VANG} strokeWidth={14} fill="none" strokeLinecap="round" strokeLinejoin="round" opacity={tl > 0 ? 1 : 0} />
          <circle cx={110} cy={820} r={16} fill={DO} opacity={tl} />
          {ve > 0.01 && ve < 0.995 ? <circle cx={bx} cy={by} r={14} fill="#fff" /> : null}
          <path d="M858 452 L902 450 L898 494" stroke={VANG} strokeWidth={14} fill="none" strokeLinecap="round" strokeLinejoin="round" opacity={muiTen} />
        </svg>
        <div
          style={{
            position: 'absolute', left: 130, top: 370, fontWeight: 600, fontSize: 48, color: 'rgba(255,255,255,.85)',
            opacity: Math.min(1, ghi * 1.4), transform: `translateY(${(1 - ghi) * 30}px)`,
          }}
        >
          <Nhan chu="Công nghệ phát triển *rất nhanh*" />
        </div>
      </div>
    </Nen>
  );
};

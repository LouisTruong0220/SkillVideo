// Video 012 · 49,0 s → hết (57,17 s; cảnh dài 8,4 s cho dư). Mốc = giây từ đầu cảnh.
// Lời: "Khi đó anh chị không phải chỉ là mua một con robot độc lập nữa, mà anh chị có thể sở hữu một con robot có thể
//       tích hợp cùng với nền tảng hệ sinh thái công nghệ đã có sẵn của đơn vị."
import React from 'react';
import {Easing, useCurrentFrame, useVideoConfig} from 'remotion';
import {bat, DO, Nen, Nhan, pha, tieuDe, VANG} from '../v011/chung';

const MOC = {robot: 0.2, gach: 1.0, soHuu: 2.7, tichHop: 3.85, noi: 4.25, xung: 4.6, heSinhThai: 5.9, chot: 6.3};

/** Robot lễ tân chung chung (màn hình đầu nghiêng + thân thuôn), khung 260×400. */
const RobotLeTan: React.FC<{chop: number}> = ({chop}) => (
  <svg viewBox="0 0 260 400" width={260} height={400}>
    <rect x={38} y={8} width={184} height={124} rx={22} fill="#1d1414" stroke="#fff" strokeWidth={7} transform="rotate(-6 130 70)" />
    <ellipse cx={98} cy={72} rx={17} ry={22 * chop} fill="#fff" />
    <ellipse cx={160} cy={66} rx={17} ry={22 * chop} fill="#fff" />
    <rect x={112} y={136} width={36} height={34} rx={8} fill="#fff" />
    <path d="M74 172 H186 Q206 172 210 196 L232 372 Q234 392 214 392 H46 Q26 392 28 372 L50 196 Q54 172 74 172 Z" fill="#2a1e1c" stroke="#fff" strokeWidth={7} />
    <path d="M78 236 H182" stroke={DO} strokeWidth={10} strokeLinecap="round" />
  </svg>
);

const O = [
  [52, 140], [186, 140], [320, 140],
  [52, 268], [186, 268], [320, 268],
];

export const TichHop: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;

  const rb = bat(f, fps, MOC.robot, 11);
  const chop = 1 - 0.9 * Math.sin(Math.PI * pha(t, 0.9, 1.05, 0, 1, Easing.linear));
  const gach = pha(t, MOC.gach, MOC.gach + 0.3);
  const mo = pha(t, MOC.gach + 0.15, MOC.gach + 0.35, 1, 0.45) + pha(t, MOC.soHuu, MOC.soHuu + 0.3, 0, 0.55);
  const sang = pha(t, MOC.soHuu, MOC.soHuu + 0.45, 0, -340, Easing.inOut(Easing.cubic));
  const nhanDi = pha(t, MOC.soHuu - 0.1, MOC.soHuu + 0.15, 1, 0);
  const nen = bat(f, fps, MOC.tichHop, 11);
  const dau = bat(f, fps, MOC.tichHop + 0.05, 10);
  const noi = pha(t, MOC.noi, MOC.noi + 0.35);
  const chot = bat(f, fps, MOC.chot, 12);
  // xung dữ liệu chạy dọc dây, lặp mỗi 0,6 s (hàm của t — không ngẫu nhiên)
  const pk = t >= MOC.xung ? ((t - MOC.xung) % 0.6) / 0.45 : -1;

  return (
    <Nen>
      {/* nhãn trên — top ≥ 250 */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 250, textAlign: 'center', opacity: Math.min(1, dau * 1.4)}}>
        <span style={{display: 'inline-block', padding: '14px 36px', borderRadius: 999, background: DO, fontFamily: 'Neusharp', fontSize: 56, lineHeight: 1, letterSpacing: 2, transform: `scale(${dau})`}}>
          TÍCH HỢP
        </span>
      </div>

      {/* dây nối robot → nền tảng */}
      <svg viewBox="0 0 1080 960" width={1080} height={960} style={{position: 'absolute', left: 0, top: 0}}>
        <path d="M340 570 H440" stroke={VANG} strokeWidth={10} strokeLinecap="round" fill="none" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - noi} />
        {pk >= 0 && pk <= 1 ? <circle cx={340 + 100 * pk} cy={570} r={11} fill="#fff" /> : null}
      </svg>

      <div
        style={{
          position: 'absolute', left: 410, top: 350, width: 260, height: 400,
          transform: `translateX(${sang}px) scale(${0.4 + 0.6 * rb})`, transformOrigin: '50% 100%', opacity: Math.min(1, rb * 1.5) * Math.min(1, mo),
        }}
      >
        <RobotLeTan chop={chop} />
      </div>

      {/* ROBOT ĐỘC LẬP — bị gạch */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 770, ...tieuDe(64), letterSpacing: 2, opacity: pha(t, 0.35, 0.6) * nhanDi}}>ROBOT ĐỘC LẬP</div>
      <div style={{position: 'absolute', left: 270, top: 796, width: 540, height: 12, borderRadius: 6, background: DO, transform: `scaleX(${gach})`, transformOrigin: '0 50%', opacity: nhanDi}} />

      {/* NỀN TẢNG CỦA ĐƠN VỊ */}
      <div
        style={{
          position: 'absolute', left: 440, top: 350, width: 490, height: 410, borderRadius: 36, boxSizing: 'border-box',
          border: `6px solid ${VANG}`, background: 'rgba(255,212,59,.07)', transform: `scale(${0.5 + 0.5 * nen})`, opacity: Math.min(1, nen * 1.5),
        }}
      >
        <div style={{position: 'absolute', left: 0, right: 0, top: 30, ...tieuDe(44), color: VANG, lineHeight: 1.08}}>
          NỀN TẢNG
          <br />
          CỦA ĐƠN VỊ
        </div>
        {O.map(([l, tp], i) => {
          const s = pha(t, MOC.heSinhThai + i * 0.14, MOC.heSinhThai + i * 0.14 + 0.18);
          return (
            <div
              key={i}
              style={{
                position: 'absolute', left: l, top: tp, width: 118, height: 118, borderRadius: 24, boxSizing: 'border-box',
                border: `4px solid ${s > 0.5 ? VANG : 'rgba(255,255,255,.35)'}`,
                background: `rgba(255,212,59,${0.05 + 0.3 * s})`, transform: `scale(${1 + 0.12 * Math.sin(Math.PI * s)})`,
              }}
            />
          );
        })}
      </div>

      {/* câu chốt */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 800, textAlign: 'center', fontWeight: 700, fontSize: 62, opacity: Math.min(1, chot * 1.4), transform: `translateY(${(1 - chot) * 30}px)`}}>
        <Nhan chu="Không chỉ là *một con robot*" />
      </div>
    </Nen>
  );
};

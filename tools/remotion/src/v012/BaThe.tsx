// Video 012 · 43,8 s → 49,0 s (5,2 s). Mốc = giây từ đầu cảnh.
// Lời: "…mà có thể là có nhiều phần mềm, nhiều công nghệ và nhiều chức năng có thể phát triển ở tương lai."
import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {bat, DO, Nen, pha, VANG} from '../v011/chung';

const MOC = {the: [0.12, 1.0, 2.0], phatTrien: 2.6};
const CHU = ['Phần mềm', 'Công nghệ', 'Chức năng'];

export const BaThe: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const len = pha(t, MOC.phatTrien, MOC.phatTrien + 0.5);
  const dau = pha(t, MOC.phatTrien + 0.4, MOC.phatTrien + 0.5);

  return (
    <Nen>
      {CHU.map((chu, i) => {
        const b = bat(f, fps, MOC.the[i], 11);
        const vang = pha(t, MOC.phatTrien + i * 0.1, MOC.phatTrien + i * 0.1 + 0.15);
        // sau "phát triển": cả cột thẻ nhích lên theo mũi tên
        const nhich = -18 * pha(t, MOC.phatTrien + 0.1, MOC.phatTrien + 0.6);
        return (
          <div
            key={chu}
            style={{
              position: 'absolute', left: 110, top: 250 + 180 * i, width: 660, height: 150, borderRadius: 30, boxSizing: 'border-box',
              border: `5px solid ${vang > 0.5 ? VANG : DO}`, background: 'rgba(255,255,255,.06)',
              display: 'flex', alignItems: 'center', gap: 30, padding: '0 40px',
              opacity: Math.min(1, b * 1.4), transform: `translate(${(1 - b) * -160}px, ${nhich}px)`,
            }}
          >
            <svg width={78} height={78} viewBox="0 0 78 78" style={{flex: 'none'}}>
              <circle cx={39} cy={39} r={39} fill={vang > 0.5 ? VANG : DO} />
              <path d="M19 39 H59 M39 19 V59" stroke={vang > 0.5 ? '#110909' : '#fff'} strokeWidth={9} strokeLinecap="round" />
            </svg>
            <div style={{fontWeight: 700, fontSize: 62, whiteSpace: 'nowrap'}}>{chu}</div>
          </div>
        );
      })}
      <svg viewBox="0 0 1080 960" width={1080} height={960} style={{position: 'absolute', left: 0, top: 0}}>
        <path d="M880 760 V270" stroke={VANG} strokeWidth={16} strokeLinecap="round" fill="none" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - len} />
        <path d="M832 310 L880 256 L928 310" stroke={VANG} strokeWidth={16} strokeLinecap="round" strokeLinejoin="round" fill="none" opacity={dau} />
      </svg>
    </Nen>
  );
};

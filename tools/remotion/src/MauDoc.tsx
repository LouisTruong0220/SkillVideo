import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export const MauDoc = ({dong1, dong2}: {dong1: string; dong2: string}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const bat = spring({frame: f, fps, config: {damping: 12}});
  const hien2 = interpolate(f, [15, 30], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#110909', justifyContent: 'center', alignItems: 'center',
      fontFamily: 'Arial, sans-serif', color: 'white', textAlign: 'center'}}>
      <div style={{fontSize: 130, fontWeight: 800, transform: `scale(${bat})`}}>{dong1}</div>
      <div style={{fontSize: 60, marginTop: 40, opacity: hien2, color: '#E83636'}}>{dong2}</div>
    </AbsoluteFill>
  );
};

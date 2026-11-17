# -*- coding: utf-8 -*-
"""Đo cao độ (F0) + nhịp nói của file audio, để đối chiếu bản gốc với bản clone."""
import subprocess
import sys

import numpy as np

SR = 16000
FMIN, FMAX = 80, 400          # dải cao độ giọng người
WIN = int(0.040 * SR)         # cửa sổ 40 ms
HOP = int(0.010 * SR)         # bước nhảy 10 ms


def doc_pcm(path):
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "s16le",
         "-acodec", "pcm_s16le", "-ar", str(SR), "-ac", "1", "-"],
        capture_output=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr.decode()[-500:])
    return np.frombuffer(r.stdout, dtype=np.int16).astype(np.float64) / 32768.0


def f0_khung(x):
    """Ước lượng F0 một khung bằng tự tương quan. Trả None nếu không phải tiếng hữu thanh."""
    x = x - x.mean()
    nang_luong = np.sqrt((x ** 2).mean())
    if nang_luong < 0.01:                     # quá nhỏ -> im lặng
        return None, nang_luong
    ac = np.correlate(x, x, mode="full")[len(x) - 1:]
    if ac[0] <= 0:
        return None, nang_luong
    ac = ac / ac[0]
    lo, hi = SR // FMAX, SR // FMIN
    vung = ac[lo:hi]
    if len(vung) == 0:
        return None, nang_luong
    i = int(np.argmax(vung))
    dinh = vung[i]
    if dinh < 0.30:                           # tương quan yếu -> vô thanh / nhiễu
        return None, nang_luong
    return SR / (lo + i), nang_luong


def phan_tich(path):
    x = doc_pcm(path)
    f0s, huu_thanh, tong = [], 0, 0
    for s in range(0, len(x) - WIN, HOP):
        f, e = f0_khung(x[s:s + WIN])
        if e >= 0.01:
            tong += 1
            if f:
                f0s.append(f)
                huu_thanh += 1
    if not f0s:
        return None
    a = np.array(f0s)
    return {
        "n": len(a),
        "median": float(np.median(a)),
        "p10": float(np.percentile(a, 10)),
        "p90": float(np.percentile(a, 90)),
        "dai": float(np.percentile(a, 90) - np.percentile(a, 10)),
        "ty_le_huu_thanh": huu_thanh / max(tong, 1),
        "giay": len(x) / SR,
    }


if __name__ == "__main__":
    print(f"{'file':<42} {'F0 giua':>8} {'p10':>7} {'p90':>7} {'dai':>7} {'huu thanh':>10} {'giay':>7}")
    print("-" * 92)
    for p in sys.argv[1:]:
        r = phan_tich(p)
        ten = p.replace("\\", "/").split("/")[-1]
        if not r:
            print(f"{ten:<42} {'(khong do duoc)':>8}")
            continue
        print(f"{ten:<42} {r['median']:8.1f} {r['p10']:7.1f} {r['p90']:7.1f} "
              f"{r['dai']:7.1f} {r['ty_le_huu_thanh']:9.0%} {r['giay']:7.1f}")

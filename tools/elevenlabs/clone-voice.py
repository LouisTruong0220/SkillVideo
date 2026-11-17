# -*- coding: utf-8 -*-
"""
Nhân bản giọng anh Trường từ mẫu audio đã trích sẵn.

CẦN GÓI TRẢ PHÍ (Starter trở lên) — gói Free không nhân bản giọng được.

Chạy:  python clone-voice.py
       python clone-voice.py --mau 02 03 07      (chọn mẫu khác)
"""
import argparse
import glob
import os

import rbw_voice as rv

SAMPLES = os.path.join(rv.ROOT, "02-media", "voice-samples")
MAC_DINH = os.path.join(SAMPLES, "_GHEP-3-mau-tot-nhat.mp3")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ten", default="Duy Truong",
                    help="Tên giọng hiển thị trên ElevenLabs")
    ap.add_argument("--mau", nargs="*",
                    help="Số thứ tự mẫu, vd: --mau 02 03 07. Bỏ trống = dùng file ghép sẵn")
    a = ap.parse_args()

    if a.mau:
        files = []
        for so in a.mau:
            hit = glob.glob(os.path.join(SAMPLES, f"{so}-*.mp3"))
            if not hit:
                raise SystemExit(f"Khong thay mau so {so} trong {SAMPLES}")
            files.extend(hit)
    else:
        files = [MAC_DINH]

    print("  Mau giong dung de nhan ban:")
    tong = 0
    for f in files:
        mb = os.path.getsize(f) / 1024 / 1024
        tong += mb
        print(f"    - {os.path.basename(f)}  ({mb:.1f} MB)")
    print(f"    Tong: {tong:.1f} MB\n")

    env = rv.load_env()
    print("  Dang gui len ElevenLabs ...")
    kq = rv.clone(
        env, a.ten, files,
        description="Giong Phan Duy Truong - Duy Truong Robot, Roboworld. "
                    "Trich tu video gioi thieu robot phuc vu nha hang.",
    )

    vid = kq.get("voice_id", "")
    print(f"\n  XONG. voice_id = {vid}")
    print(f"\n  Dan dong nay vao tools/elevenlabs/.env:")
    print(f"     ELEVENLABS_VOICE_ID={vid}")
    print(f"\n  Roi thu ngay:")
    print(f'     python doc-kich-ban.py "Xin chao, toi la Duy Truong Robot." thu-giong')


if __name__ == "__main__":
    main()

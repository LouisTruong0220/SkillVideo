# -*- coding: utf-8 -*-
"""
Nhân bản giọng Bella (BellaBot Pro tiếng Việt) lên ElevenLabs.

Chạy dung-mau-bella.py TRƯỚC để có file mẫu ghép.

CẦN GÓI TRẢ PHÍ (Starter trở lên). Tài khoản dùng chung của công ty —
đừng xoá giọng của đồng nghiệp ("Q Huy MKT RBW", "Phương Uyên RBW").

Chạy:  python clone-bella.py
       python clone-bella.py --ten "Bella BellaBot"
"""
import argparse
import os
import sys

import rbw_voice as rv

sys.stdout.reconfigure(encoding="utf-8")

MAU = os.path.join(rv.ROOT, "02-media", "giong-noi", "bellabot-pro-tieng-viet",
                   "_mau-clone", "bella-mau-clone.mp3")

# Mô tả gửi kèm. ElevenLabs dùng nó làm gợi ý phong cách, nên nêu rõ chất
# "mèo máy": có tiếng meo, có tiếng cười, nói nhấn nhá chứ không đọc đều.
MO_TA = (
    "Giong robot phuc vu nha hang BellaBot Pro ban tieng Viet. "
    "Nu, tre, tuoi tan, noi nhan nha nhu nhan vat hoat hinh mèo may. "
    "Hay keu 'meo' o cuoi cau va co tieng cuoi khuc khich."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ten", default="Bella BellaBot VI",
                    help="Ten giong hien thi tren ElevenLabs")
    ap.add_argument("--mau", default=MAU, help="Duong dan file mau")
    a = ap.parse_args()

    if not os.path.exists(a.mau):
        raise SystemExit(
            f"Chua co file mau: {a.mau}\n"
            "  Chay truoc:  python dung-mau-bella.py"
        )

    mb = os.path.getsize(a.mau) / 1024 / 1024
    print(f"  Mau: {os.path.basename(a.mau)}  ({mb:.1f} MB)")

    env = rv.load_env()

    # Canh bao neu trung ten giong da co -> tranh tao ban sao thu 2, thu 3.
    try:
        for v in rv.list_voices(env):
            if v.get("name", "").strip().lower() == a.ten.strip().lower():
                print(f"\n  DA CO giong ten '{a.ten}' (voice_id={v.get('voice_id')}).")
                print("  Dat ten khac bang --ten, hoac xoa giong cu tren web truoc.")
                return
    except SystemExit:
        raise
    except Exception:
        pass  # khong liet ke duoc thi cu tao, khong chan viec chinh

    print("  Dang gui len ElevenLabs ...")
    kq = rv.clone(env, a.ten, [a.mau], description=MO_TA)

    vid = kq.get("voice_id", "")
    print(f"\n  XONG. voice_id = {vid}")
    print("\n  Thu ngay:")
    print(f'     python doc-kich-ban.py "Xin chao, toi la Bella. Meo!" thu-bella --giong {vid}')


if __name__ == "__main__":
    main()

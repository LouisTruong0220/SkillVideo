# -*- coding: utf-8 -*-
"""Xem da tieu bao nhieu credit ElevenLabs, va con sinh duoc bao nhieu thu tuc nua.

⚠⚠ ĐỌC KỸ TRƯỚC KHI TIN CON SỐ CỦA CÔNG CỤ NÀY.

Key cua cong ty KHONG co quyen `user_read`: /v1/user va /v1/user/subscription deu
tra 401, nen API khong cho biet HAN MUC cua goi. Chi /v1/usage/character-stats la mo.

VA CHINH NO DEM THIEU. Doi chieu 18/08/2026 voi trang Subscription tren web:

    API /usage/character-stats  ->  23.369 credit trong ky
    Trang web (so that)         ->  34.973 / 38.093 credit

Lech ~11.600. character-stats hinh nhu chi dem phan Text-to-Speech, khong dem
Studio / Music / Sound Effects / nhan ban giong — ma tai khoan nay dung chung ca
phong, dong nghiep tieu o cac muc do.

  → SO TREN WEB MOI LA SO THAT.
  → Cong cu nay chi de xem XU HUONG dung theo ngay, va de do TY LE credit/ky tu.
  → TRUOC KHI SINH LO LON: mo elevenlabs.io -> Subscription xem con bao nhieu.

  python tools\\elevenlabs\\xem-su-dung.py
  python tools\\elevenlabs\\xem-su-dung.py --han-muc 38093
"""
import argparse
import collections
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import requests
import rbw_voice as rv

API = "https://api.elevenlabs.io/v1"

# Do tren tai khoan cong ty 18/08/2026: gui 17.382 ky tu bang eleven_v3, API bao
# tru 8.680 credit — dung MOT NUA. Nen credit = so ky tu x 0,5.
# ⚠ Ty le nay la CUA GOI DANG DUNG, khong phai hang so cua ElevenLabs. Model khac
#   hoac goi khac co the tinh 1:1. Do lai: ghi so ky tu vua gui, chay lai lenh nay,
#   lay chenh lech credit chia cho so ky tu.
CREDIT_MOI_KY_TU = 0.5

# Doc tren web 18/08/2026.
GOI_DANG_DUNG = "Starter — gia han ngay 22 hang thang, ky nay 38.093 credit"

# Han muc thang cua cac goi, de doi chieu nhanh (theo trang gia 18/08/2026).
GOI = [("Free", 10_000), ("Starter", 30_000), ("Creator", 121_000),
       ("Pro", 600_000), ("Scale", 1_800_000)]


def lay_theo_ngay(env, so_ngay):
    now = datetime.datetime.now(datetime.timezone.utc)
    start = now - datetime.timedelta(days=so_ngay)
    r = requests.get(
        API + "/usage/character-stats",
        headers={"xi-api-key": env["ELEVENLABS_API_KEY"]},
        params={"start_unix": int(start.timestamp() * 1000),
                "end_unix": int(now.timestamp() * 1000)},
        timeout=60,
    )
    r.raise_for_status()
    d = r.json()
    return ([(datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc), v or 0)
             for ms, v in zip(d["time"], d["usage"]["All"])], now)


def so(n):
    return "{:,}".format(int(n)).replace(",", ".")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--han-muc", type=int, default=0,
                    help="han muc credit cua ky (doc tren trang Subscription)")
    ap.add_argument("--so-ngay", type=int, default=400)
    a = ap.parse_args()

    env = rv.load_env()
    ngay, now = lay_theo_ngay(env, a.so_ngay)

    thang = collections.OrderedDict()
    for dt, v in ngay:
        k = "%04d-%02d" % (dt.year, dt.month)
        thang[k] = thang.get(k, 0) + v

    print("API BÁO ĐÃ DÙNG (chỉ Text-to-Speech — xem cảnh báo bên dưới)")
    print("  %-9s %12s" % ("tháng", "credit"))
    for k in sorted(thang):
        if thang[k]:
            print("  %-9s %12s" % (k, so(thang[k])))

    da_dung = int(thang.get("%04d-%02d" % (now.year, now.month), 0))
    print("\n  Tháng này: %s credit (theo API)" % so(da_dung))

    print("\n  ⚠ CON SỐ TRÊN ĐÂY ĐẾM THIẾU. Đối chiếu 18/08/2026: API báo 23.369")
    print("    credit trong kỳ, trang web báo 34.973/38.093 — lệch ~11.600.")
    print("    character-stats chỉ đếm Text-to-Speech, không đếm Studio / Music /")
    print("    Sound Effects / nhân bản giọng, mà tài khoản này dùng chung cả phòng.")
    print("    → Mở elevenlabs.io → Subscription xem số thật.")
    print("    Gói: %s" % GOI_DANG_DUNG)
    print("    (API không tự đọc được: key thiếu quyền user_read, /v1/user trả 401)")

    if not a.han_muc:
        print("\n  Hạn mức các gói để đối chiếu:")
        for ten, h in GOI:
            print("    %-9s %12s credit/tháng" % (ten, so(h)))
        print("\n  Chạy lại với --han-muc <số đọc trên web> để tính còn bao nhiêu.")
        return 0

    con = a.han_muc - da_dung
    print("\n  ⚠ Phép tính dưới đây dùng số ĐÃ DÙNG của API nên LẠC QUAN HƠN THỰC TẾ.")
    print("    Muốn đúng: lấy thẳng 'Credits used X / Y' trên web, còn lại = Y − X.")
    print("  Hạn mức %s − API báo dùng %s = %s credit" % (so(a.han_muc), so(da_dung), so(con)))
    print("  ≈ %s ký tự (1 ký tự = %s credit)" % (so(con / CREDIT_MOI_KY_TU), CREDIT_MOI_KY_TU))
    return 0


if __name__ == "__main__":
    sys.exit(main())

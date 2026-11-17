# -*- coding: utf-8 -*-
"""
Chuẩn hoá ảnh về đúng khổ dọc 1080×1920 để chèn vào scene video.

Vì sao cần: LESSONS.md ghi lại ba lần cùng một nhóm lỗi — ảnh 800×449 phóng lên
bị vỡ, ảnh studio dính logo PUDU ở góc trên, ảnh triển khai có dải watermark
"ROBOWORLD". Cả ba đều máy kiểm được, nên để máy làm thay vì nhắc bằng lời.

Dùng:
  python tools/prep-assets.py <anh.jpg> --ra <thu-muc>
  python tools/prep-assets.py <thu-muc-anh> --ra <thu-muc>          # cả thư mục
  python tools/prep-assets.py <anh.jpg> --ra <thu-muc> --cat-tren 13
  python tools/prep-assets.py <anh.jpg> --ra <thu-muc> --ten p2-be-khay
  python tools/prep-assets.py <thu-muc> --kiem                      # chỉ báo cáo

Tham số cắt watermark tính theo PHẦN TRĂM chiều cao ảnh gốc, cắt TRƯỚC khi
cover-fit — cắt sau thì phần watermark đã bị kéo giãn, cắt không sạch.
"""
import argparse
import os
import sys

from PIL import Image, ImageEnhance

sys.stdout.reconfigure(encoding="utf-8")

W, H = 1080, 1920
CANH_NGAN_TOI_THIEU = 1080   # dưới mức này phóng lên là vỡ, loại thẳng
DUOI_ANH = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def cover_fit(im, w=W, h=H):
    """Phủ kín khung w×h, cắt phần thừa, không méo tỉ lệ."""
    ti_le = max(w / im.width, h / im.height)
    moi = im.resize((round(im.width * ti_le), round(im.height * ti_le)), Image.LANCZOS)
    trai = (moi.width - w) // 2
    # Cắt lệch lên trên một chút: chủ thể (người, robot) hầu như luôn nằm
    # nửa trên khung, cắt đúng giữa hay bị mất đầu.
    tren = max(0, round((moi.height - h) * 0.4))
    return moi.crop((trai, tren, trai + w, tren + h))


def kiem_anh(duong_dan):
    """Trả (ok, ghi_chu) — ok=False nghĩa là không nên dùng ảnh này."""
    try:
        with Image.open(duong_dan) as im:
            w, h = im.size
    except Exception as e:
        return False, f"không mở được ảnh ({e})"

    canh_ngan = min(w, h)
    if canh_ngan < CANH_NGAN_TOI_THIEU:
        return False, f"{w}×{h} — cạnh ngắn {canh_ngan} < {CANH_NGAN_TOI_THIEU}, phóng lên sẽ vỡ"

    ghi_chu = f"{w}×{h}"
    if (w, h) == (W, H):
        ghi_chu += " — đã đúng khổ"
    elif w > h:
        ghi_chu += " — ảnh ngang, cover-fit sẽ cắt mạnh hai bên, kiểm lại chủ thể còn đủ không"
    return True, ghi_chu


def xu_ly(duong_dan, thu_muc_ra, cat_tren=0.0, cat_duoi=0.0, ten=None,
          sang=1.0, tuong_phan=1.0, cat_trai=0.0, cat_phai=0.0, chat_luong=92):
    ok, ghi_chu = kiem_anh(duong_dan)
    ten_goc = os.path.basename(duong_dan)
    if not ok:
        print(f"  BO   {ten_goc}: {ghi_chu}")
        return None

    with Image.open(duong_dan) as im:
        im = im.convert("RGB")
        w0, h0 = im.size

        # Cắt bỏ vùng vi phạm TRƯỚC khi cover-fit. Cắt sau thì vùng đó đã bị
        # kéo giãn, cắt không sạch. Bốn cạnh vì thứ phải bỏ nằm khắp nơi:
        # watermark ở dải trên, biển hiệu và SỐ ĐIỆN THOẠI ở hai bên khung.
        if cat_tren or cat_duoi or cat_trai or cat_phai:
            x0 = round(w0 * cat_trai / 100)
            x1 = w0 - round(w0 * cat_phai / 100)
            y0 = round(h0 * cat_tren / 100)
            y1 = h0 - round(h0 * cat_duoi / 100)
            if y1 - y0 < 200 or x1 - x0 < 200:
                print(f"  BO   {ten_goc}: cắt quá nhiều, phần còn lại {x1-x0}×{y1-y0}")
                return None
            im = im.crop((x0, y0, x1, y1))

        ra = cover_fit(im)

    # Ảnh thiếu sáng cộng với lớp phủ tối của scene thành một mảng đen, mất
    # luôn nội dung ảnh. Kéo sáng ở đây, đừng hạ shade — hạ shade thì chữ chìm.
    if sang != 1.0:
        ra = ImageEnhance.Brightness(ra).enhance(sang)
    if tuong_phan != 1.0:
        ra = ImageEnhance.Contrast(ra).enhance(tuong_phan)

    os.makedirs(thu_muc_ra, exist_ok=True)
    goc_ten = ten or os.path.splitext(ten_goc)[0]
    dich = os.path.join(thu_muc_ra, goc_ten + ".jpg")
    ra.save(dich, "JPEG", quality=chat_luong, optimize=True)

    canh = [(cat_tren, "↑"), (cat_duoi, "↓"), (cat_trai, "←"), (cat_phai, "→")]
    cat = "".join(f" {v}%{k}" for v, k in canh if v)
    cat = f", cắt{cat}" if cat else ""
    chinh = ""
    if sang != 1.0 or tuong_phan != 1.0:
        chinh = f", sáng ×{sang} tương phản ×{tuong_phan}"
    print(f"  OK   {ten_goc}  {w0}×{h0}{cat}{chinh} -> {W}×{H}  ({dich})")
    return dich


def liet_ke(nguon):
    if os.path.isdir(nguon):
        return sorted(
            os.path.join(nguon, f)
            for f in os.listdir(nguon)
            if os.path.splitext(f)[1].lower() in DUOI_ANH
        )
    return [nguon]


def main():
    p = argparse.ArgumentParser(description="Chuẩn hoá ảnh về 1080×1920 cho video dọc")
    p.add_argument("nguon", help="file ảnh hoặc thư mục ảnh")
    p.add_argument("--ra", help="thư mục xuất (bắt buộc trừ khi --kiem)")
    p.add_argument("--cat-tren", type=float, default=0.0,
                   help="cắt %% chiều cao phía trên (bỏ logo/watermark), vd 13")
    p.add_argument("--cat-duoi", type=float, default=0.0, help="cắt %% chiều cao phía dưới")
    p.add_argument("--cat-trai", type=float, default=0.0,
                   help="cắt %% chiều rộng bên trái (bỏ biển hiệu, số điện thoại)")
    p.add_argument("--cat-phai", type=float, default=0.0, help="cắt %% chiều rộng bên phải")
    p.add_argument("--ten", help="đổi tên file ra (chỉ khi nguồn là 1 ảnh)")
    p.add_argument("--sang", type=float, default=1.0,
                   help="hệ số độ sáng, 1.0 = giữ nguyên. Ảnh tối dùng 1.3–1.6")
    p.add_argument("--tuong-phan", type=float, default=1.0,
                   help="hệ số tương phản, 1.0 = giữ nguyên")
    p.add_argument("--kiem", action="store_true", help="chỉ báo cáo kích thước, không xuất file")
    a = p.parse_args()

    anh = liet_ke(a.nguon)
    if not anh:
        print("Không tìm thấy ảnh nào.")
        return 1

    if a.kiem:
        print(f"Kiểm {len(anh)} ảnh:")
        loai = 0
        for d in anh:
            ok, ghi_chu = kiem_anh(d)
            print(f"  {'OK ' if ok else 'BO '} {os.path.basename(d)}: {ghi_chu}")
            loai += (not ok)
        print(f"\n{len(anh) - loai} dùng được, {loai} phải loại.")
        return 0

    if not a.ra:
        print("Thiếu --ra <thu-muc-xuat>")
        return 1
    if a.ten and len(anh) > 1:
        print("--ten chỉ dùng khi nguồn là một ảnh.")
        return 1

    print(f"Chuẩn hoá {len(anh)} ảnh -> {W}×{H}:")
    xong = sum(
        1 for d in anh
        if xu_ly(d, a.ra, a.cat_tren, a.cat_duoi, a.ten, a.sang, a.tuong_phan,
                 a.cat_trai, a.cat_phai)
    )
    print(f"\nXong {xong}/{len(anh)} ảnh.")
    return 0 if xong else 1


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Soát ảnh bìa 1080×1920: kẻ vạch vùng an toàn + khung lưới hồ sơ 3:4, kèm ô lưới thu nhỏ như trên trang cá nhân.

    tools/video-tho/.venv/Scripts/python.exe tools/video-tho/soat-bia.py <du-an> [anh-bia.png]
    … --html assets/bia.html     # (kênh công ty, không Remotion) chụp file HTML 1080×1920 thành anh-bia.png trước

Ra build/bia/soat.jpg (trái: cả ảnh có vạch xanh = vùng an toàn, khung tím = dải lưới 3:4 y 240–1680;
phải: ô lưới đúng như TikTok cắt). MỞ ra xem:
  • tiêu đề + hình chính + mặt người nằm TRONG khung tím (lưới hồ sơ chỉ hiện dải này)
  • chữ trong x 140–940, y ≥ 250 (khi bìa hiện toàn màn, cột nút và thanh tab đè lên ngoài vùng đó)
  • ô lưới thu nhỏ vẫn đọc được tiêu đề
"""
import argparse, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
from chung import CONG_CU, GOC, doc_json, du_an, gan_bia
from vung import ke_vach

LUOI = (240, 1680)   # TikTok hồ sơ cắt giữa 3:4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("anh", nargs="?", default="anh-bia.png")
    ap.add_argument("--html", help="file HTML 1080×1920 (tương đối dự án) → chụp thành ảnh bìa trước khi soát")
    g = ap.parse_args()
    da = du_an(g.du_an)
    anh = da / g.anh
    if g.html:
        r = subprocess.run(["node", str(CONG_CU / "chup-html.mjs"), str(da / g.html), str(anh)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        print(r.stdout.strip())
        if r.returncode != 0:
            print(r.stderr[-2000:]); sys.exit(1)
    a = Image.open(anh).convert("RGB")
    if a.size != (1080, 1920):
        print(f"⚠ ảnh bìa {a.size[0]}×{a.size[1]} — chuẩn là 1080×1920"); a = a.resize((1080, 1920))
    ve = ke_vach(a, day=4)
    ImageDraw.Draw(ve).rectangle([0, LUOI[0], 1079, LUOI[1]], outline=(255, 0, 255), width=6)
    bang = Image.new("RGB", (900, 960), (17, 17, 17))
    bang.paste(ve.resize((540, 960)), (0, 0))
    bang.paste(a.crop((0, LUOI[0], 1080, LUOI[1])).resize((360, 480)), (540, 240))
    ra = da / "build" / "bia"; ra.mkdir(parents=True, exist_ok=True)
    bang.save(ra / "soat.jpg", quality=90)
    if anh.suffix.lower() == ".png":
        a.save(anh.with_suffix(".jpg"), quality=92)
    print(f"✓ {ra / 'soat.jpg'}  ·  bản tải lên: {anh.with_suffix('.jpg')}")
    cfg = doc_json(da / "dung.json", {})
    video = GOC / "05-output" / f"{cfg.get('ten', da.name)}.mp4"
    if gan_bia(video, anh.with_suffix(".jpg")):
        print(f"  + đã nhúng ảnh bìa vào {video} (dung.py cũng tự nhúng mỗi lần dựng thật)")


if __name__ == "__main__":
    main()

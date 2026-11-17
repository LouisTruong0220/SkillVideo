# -*- coding: utf-8 -*-
"""Soi nhanh vài khoảnh khắc mà KHÔNG dựng video — sửa dung.json / khối html xong là xem ngay.

    tools/video-tho/.venv/Scripts/python.exe tools/video-tho/soi.py <du-an> 15.1 29.8 55.5
    … --nhip            # thêm mỗi nhịp trong dung.json một ảnh (t + 0,4 s)
    … --khong-vach      # không kẻ vạch vùng an toàn

Dựng lại build/hf từ dung.json + phu-de.txt (vài giây) rồi `hyperframes snapshot --at` (~1–2 s/ảnh).
Ra build/soi/*.png (đã kẻ vạch 12% đỉnh · 25% đáy · 140 px phải) + build/soi/bang.jpg. MỞ ra xem.
Ảnh chụp khớp video thật (đã đối chiếu 17/11/2026: người nói đúng giây, cảnh phụ, Remotion, phụ đề).
Cảnh Remotion là video nên hiện đúng khung; muốn xem chuyển động thì `dung.py --doan A-B` (~1,5–2,5 phút).
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from chung import GOC, doc_json, du_an
from dung import dung_hf
from vung import chup, ke_vach


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("giay", nargs="*", type=float)
    ap.add_argument("--nhip", action="store_true", help="thêm một ảnh cho mỗi nhịp (t + 0,4 s)")
    ap.add_argument("--khong-vach", action="store_true")
    g = ap.parse_args()
    da = du_an(g.du_an)
    cfg = doc_json(da / "dung.json")
    moc = set(round(t, 2) for t in g.giay)
    if g.nhip:
        moc |= {round(n["t"] + min(0.4, n.get("dai", 1) / 2), 2) for n in cfg.get("nhip", []) if n["loai"] != "am"}
    if not moc:
        ap.error("cho ít nhất một mốc giây, hoặc --nhip")
    moc = sorted(moc)

    hf = da / "build" / "hf"
    dung_hf(da, cfg, hf)
    ra = da / "build" / "soi"
    anh = chup(hf, moc, ra)

    font = ImageFont.truetype(str(GOC / "00-brand/design-kit/assets/fonts/DFVN-BrittiSans-Bold.ttf"), 26)
    o_w, o_h, cot = 270, 480, 6
    hang = (len(moc) + cot - 1) // cot
    bang = Image.new("RGB", (o_w * cot, (o_h + 40) * hang), "#111")
    d = ImageDraw.Draw(bang)
    for i, t in enumerate(moc):
        p = anh.get(t)
        if not p:
            continue
        a = Image.open(p)
        if not g.khong_vach:
            a = ke_vach(a, day=6)
            a.save(p)
        x, y = (i % cot) * o_w, (i // cot) * (o_h + 40)
        bang.paste(a.resize((o_w, o_h)), (x, y + 40))
        d.text((x + 8, y + 6), f"{t:g}s", fill="#FFD43B", font=font)
    bang.save(ra / "bang.jpg", quality=88)
    print(f"✓ {len(anh)} ảnh → {ra}\n  bảng: {ra / 'bang.jpg'}")


if __name__ == "__main__":
    main()

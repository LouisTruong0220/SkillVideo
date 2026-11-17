# -*- coding: utf-8 -*-
"""B8 — Soát thành phẩm: bảng ảnh trích ở mỗi nhịp + đều đặn, đo độ to, đo độ dài, TỰ DÒ CHỮ LẤN VÙNG AN TOÀN.

    tools/video-tho/.venv/Scripts/python.exe tools/video-tho/kiem.py <du-an> [video.mp4] [--moi 1.5] [--khong-vung]

Ra build/kiem/bang-01.jpg … (mỗi bảng 12 ô có ghi giây, đã kẻ vạch 12% đỉnh · 25% đáy · 140 px phải) + in kết quả đo.
Claude MỞ TỪNG BẢNG ra xem — không xem là chưa soát.
Thang đo: độ to tích phân −14 ±1 LUFS, đỉnh thật ≤ −1 dBTP (chuẩn TikTok/Reels).

Dò vùng an toàn (máy làm, thay việc QC phải đo tay — video 012 trượt QC 2 vòng vì lỗi này):
  • chữ/đồ hoạ HyperFrames: chụp build/hf mỗi 0,5 s với mọi video/ảnh bị giấu → điểm sáng lọt vùng cấm là chữ lấn
  • cảnh nửa trên tự dựng (assets/rm-*.mp4, Remotion): quét điểm sáng thẳng trên file, mỗi 0,2 s
  Vùng cấm: y < 230 · y > 1440 · x > 940 (khung 1080×1920). Ảnh lỗi lưu build/kiem/vung-*.png (khung đỏ = chỗ lấn).
  Lấn chỉ 1 mẫu (≤ 0,5 s) thường là lúc khối đang trượt vào/ra → ghi "thoáng qua", xem ảnh rồi quyết.
"""
import argparse, re, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from chung import GOC, do, doc_json, du_an
from vung import chup, diem_lan, ke_vach, quet_video_nua_tren


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("video", nargs="?")
    ap.add_argument("--moi", type=float, default=1.5)
    ap.add_argument("--khong-vung", action="store_true", help="bỏ bước dò chữ lấn vùng an toàn")
    ap.add_argument("--buoc-vung", type=float, default=0.5)
    g = ap.parse_args()
    da = du_an(g.du_an)
    cfg = doc_json(da / "dung.json", {})
    v = Path(g.video) if g.video else (GOC / "05-output" / f"{cfg.get('ten', da.name)}.mp4")
    if not v.exists():
        v = da / "build" / "nhap.mp4"
    tong = do(v)["giay"]

    moc = {round(x * g.moi, 2): "" for x in range(int(tong / g.moi) + 1)}
    for n in cfg.get("nhip", []):
        if n["loai"] != "am":
            moc[round(n["t"] + min(0.6, n.get("dai", 2) / 2), 2)] = n["loai"]
    moc = dict(sorted((t, l) for t, l in moc.items() if t < tong - 0.05))

    ra = da / "build" / "kiem"; ra.mkdir(parents=True, exist_ok=True)
    for f in ra.glob("bang-*.jpg"):
        f.unlink()
    font = ImageFont.truetype(str(GOC / "00-brand/design-kit/assets/fonts/DFVN-BrittiSans-Bold.ttf"), 26)
    o_w, o_h = 270, 480
    ds = list(moc.items())
    with tempfile.TemporaryDirectory() as td:
        anh = []
        for t, l in ds:
            p = Path(td) / f"{t:08.2f}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(v), "-frames:v", "1",
                            "-vf", f"scale={o_w}:{o_h}", str(p)], check=True)
            anh.append((t, l, p))
        for b in range(0, len(anh), 12):
            bang = Image.new("RGB", (o_w * 6, (o_h + 40) * 2), "#111")
            d = ImageDraw.Draw(bang)
            for i, (t, l, p) in enumerate(anh[b:b + 12]):
                x, y = (i % 6) * o_w, (i // 6) * (o_h + 40)
                bang.paste(ke_vach(Image.open(p), day=2), (x, y + 40))
                d.text((x + 8, y + 6), f"{t:.1f}s {l}", fill="#FFD43B" if l else "#fff", font=font)
            bang.save(ra / f"bang-{b // 12 + 1:02d}.jpg", quality=88)

    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(v), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)
    i_ = float(lufs[-1]) if lufs else None
    p_ = float(tp[-1]) if tp else None
    print(f"video: {v}\n  {tong:.1f}s · {len(ds)} ảnh soát → {ra} ({(len(ds) + 11) // 12} bảng)")
    print(f"  độ to {i_} LUFS {'✓' if i_ is not None and abs(i_ + 14) <= 1 else '✗ lệch chuẩn −14'} · "
          f"đỉnh {p_} dBTP {'✓' if p_ is not None and p_ <= -0.9 else '✗ quá −1'}")
    if not g.khong_vung:
        kiem_vung(da, cfg, tong, ra, g.buoc_vung)


def kiem_vung(da, cfg, tong, ra, buoc):
    for f in ra.glob("vung-*.png"):
        f.unlink()
    loi = []  # (giây, nguồn, vùng, hộp)
    hf = da / "build" / "hf"
    if (hf / "index.html").exists():
        moc = [round(buoc / 2 + i * buoc, 2) for i in range(int((tong - buoc / 2) / buoc) + 1)]
        anh = chup(hf, moc, da / "build" / "kiem-chu", an_hinh=True, timeout_ms=90000)
        for t in moc:
            if t in anh:
                for vung, hop, _ in diem_lan(Image.open(anh[t])):
                    loi.append((t, "chữ/đồ hoạ HyperFrames", vung, hop, anh[t]))
    else:
        print("  ⚠ chưa có build/hf — chạy dung.py trước rồi kiem.py mới dò được chữ HyperFrames")
    for n in cfg.get("nhip", []):
        src = n.get("src", "")
        if n["loai"] in ("canh-phu", "anh") and n.get("kieu") == "nua-tren" and Path(src).name.startswith("rm-"):
            p = (da / src) if (da / src).exists() else (GOC / src)
            for t, vung, hop, _ in quet_video_nua_tren(p, n.get("bat_dau", 0), n.get("dai", 0), n["t"]):
                loi.append((t, Path(src).name, vung, hop, None))

    if not loi:
        print("  vùng an toàn ✓ không chữ nào lấn 12% đỉnh · 25% đáy · 140 px phải")
        return
    # gom các mẫu liền nhau cùng nguồn + vùng thành một khoảng
    loi.sort(key=lambda x: (x[1], x[2], x[0]))
    nhom = []
    for t, ng, vung, hop, p in loi:
        g_ = nhom[-1] if nhom else None
        if g_ and g_["ng"] == ng and g_["vung"] == vung and t - g_["het"] <= buoc * 1.6:
            g_["het"] = t; g_["n"] += 1
            g_["hop"] = [min(g_["hop"][0], hop[0]), min(g_["hop"][1], hop[1]), max(g_["hop"][2], hop[2]), max(g_["hop"][3], hop[3])]
        else:
            nhom.append({"ng": ng, "vung": vung, "dau": t, "het": t, "n": 1, "hop": list(hop), "anh": p})
    that = [x for x in nhom if x["n"] > 1]
    print(f"  vùng an toàn ✗ {len(that)} chỗ lấn kéo dài · {len(nhom) - len(that)} chỗ thoáng qua (≤ 1 mẫu, thường do khối đang trượt):")
    for i, x in enumerate(sorted(nhom, key=lambda x: x["dau"]), 1):
        x0, y0, x1, y1 = x["hop"]
        nhan = "✗" if x["n"] > 1 else "·"
        print(f"    {nhan} {x['dau']:.1f}–{x['het']:.1f}s · {x['vung']} · {x['ng']} · chữ ở x {x0}–{x1}, y {y0}–{y1}")
        if x["anh"]:
            a = ke_vach(Image.open(x["anh"]))
            ImageDraw.Draw(a).rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6], outline=(255, 40, 40), width=8)
            a.resize((540, 960)).save(ra / f"vung-{i:02d}-{x['dau']:.1f}s.png")
    print(f"  ảnh chỗ lấn → {ra}\\vung-*.png")


if __name__ == "__main__":
    main()

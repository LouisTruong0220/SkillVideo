# -*- coding: utf-8 -*-
"""B1 — Chuẩn hoá video thô thành bản làm việc.

    python tools/video-tho/chuan-bi.py <du-an> <video-noi-1> [video-noi-2 ...] [--canh <canh-phu-1> ...]

<du-an>      thư mục dự án, vd 04-video-projects/012-vu-cam-2-tang (tự tạo nếu chưa có)
video-noi    clip anh Trường NÓI trước camera — sẽ được nghe-chép và cắt
--canh       clip/ảnh CẢNH PHỤ (B-roll robot chạy, cận khay, màn hình…) — chỉ chuẩn khổ, không nghe-chép

KHÔNG chép, không sửa file gốc. Ra:
  nguon/c01.mp4 …    1080×1920, 30 khung/giây đều, tiếng đã cân −16 LUFS
  build/c01.a16.wav  16 kHz mono cho VAD + whisper
  assets/canh-01.mp4 cảnh phụ đã chuẩn khổ, bỏ tiếng
  du-an.json         sổ ghi clip nào từ file gốc nào
"""
import argparse, datetime, sys
from pathlib import Path
from chung import FPS, W, H, chay, do, doc_json, du_an, ghi_json

DUOI_ANH = {".jpg", ".jpeg", ".png", ".webp", ".heic"}


def loc_khung(info, nen_mo):
    """Video dọc → phủ kín 1080×1920. Video ngang → đặt giữa trên nền chính nó phóng to làm mờ (không cắt mất người)."""
    if info["w"] >= info["h"] and nen_mo:
        return (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,"
                f"eq=brightness=-0.08[nen];[b]scale={W}:-2[tr];[nen][tr]overlay=0:(H-h)/2,fps={FPS},format=yuv420p")
    return f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p,setsar=1"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("noi", nargs="*", help="clip nói trước camera")
    ap.add_argument("--canh", nargs="*", default=[], help="cảnh phụ (video/ảnh)")
    ap.add_argument("--khong-can-tieng", action="store_true", help="giữ nguyên âm lượng gốc (mặc định cân −16 LUFS)")
    g = ap.parse_args()

    da = du_an(g.du_an)
    for con in ("nguon", "build", "assets"):
        (da / con).mkdir(parents=True, exist_ok=True)
    so = doc_json(da / "du-an.json", {"tao": datetime.date.today().isoformat(), "clip": [], "canh": []})

    for f in g.noi:
        f = Path(f).resolve()
        if any(c["goc"] == str(f) for c in so["clip"]):
            print(f"· đã có {f.name}, bỏ qua"); continue
        info = do(f)
        if not info["co_hinh"] or not info["co_tieng"]:
            print(f"✗ {f.name}: thiếu hình hoặc thiếu tiếng — clip nói phải có cả hai"); sys.exit(1)
        cid = f"c{len(so['clip']) + 1:02d}"
        ra = da / "nguon" / f"{cid}.mp4"
        ngang = info["w"] >= info["h"]
        if ngang:
            print(f"⚠ {f.name} quay NGANG {info['w']}×{info['h']} — đặt giữa trên nền mờ. Lần sau nên quay dọc.")
        tieng = "highpass=f=70" + ("" if g.khong_can_tieng else ",loudnorm=I=-16:TP=-1.5:LRA=11") + ",aresample=48000"
        print(f"→ {cid} ← {f.name}  ({info['giay']:.1f}s, {info['w']}×{info['h']}, {info['fps']} fps)")
        chay(["ffmpeg", "-y", "-v", "error", "-i", f, "-vf", loc_khung(info, True), "-af", tieng,
              "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-g", "15", "-pix_fmt", "yuv420p",
              "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-movflags", "+faststart", ra], "chuẩn hoá " + cid)
        chay(["ffmpeg", "-y", "-v", "error", "-i", ra, "-vn", "-ac", "1", "-ar", "16000", da / "build" / f"{cid}.a16.wav"],
             "tách tiếng 16k")
        so["clip"].append({"id": cid, "goc": str(f), "file": f"nguon/{cid}.mp4", "giay": round(do(ra)["giay"], 3),
                           "goc_khung": f"{info['w']}x{info['h']}@{info['fps']}", "ngang": ngang})

    for f in g.canh:
        f = Path(f).resolve()
        if any(c["goc"] == str(f) for c in so["canh"]):
            print(f"· đã có {f.name}, bỏ qua"); continue
        cid = f"canh-{len(so['canh']) + 1:02d}"
        if f.suffix.lower() in DUOI_ANH:
            ra = da / "assets" / f"{cid}.jpg"
            chay(["ffmpeg", "-y", "-v", "error", "-i", f, "-vf",
                  f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-q:v", "2", ra], "ảnh " + cid)
        else:
            info = do(f)
            ra = da / "assets" / f"{cid}.mp4"
            chay(["ffmpeg", "-y", "-v", "error", "-i", f, "-vf", loc_khung(info, True), "-an",
                  "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-g", "15", "-pix_fmt", "yuv420p", ra], "cảnh " + cid)
        print(f"→ {cid} ← {f.name}")
        so["canh"].append({"id": cid, "goc": str(f), "file": f"assets/{ra.name}",
                           "giay": round(do(ra)["giay"], 2) if ra.suffix == ".mp4" else None, "mo_ta": ""})

    ghi_json(da / "du-an.json", so)
    print(f"\n✓ {len(so['clip'])} clip nói, {len(so['canh'])} cảnh phụ → {da}")
    print("  Bước tiếp: python tools/video-tho/nghe-chep.py", da.name)
    if so["canh"]:
        print("  ⚠ Mở từng cảnh phụ ra XEM rồi điền 'mo_ta' trong du-an.json — tên file không nói ảnh chụp gì.")


if __name__ == "__main__":
    main()

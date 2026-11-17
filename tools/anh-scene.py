# -*- coding: utf-8 -*-
"""
Trích một ảnh đại diện cho mỗi scene từ file MP4 đã render, để kiểm duyệt.

Cố tình trích từ MP4 chứ không chụp từ HTML: cái người xem thấy là MP4. Lỗi
xuất hiện ở khâu ghi hình hay mã hoá (chữ bị mờ, ảnh bị lệch, khung đen xen
giữa) chỉ lộ ra ở thành phẩm.

Điểm trích: 60% quãng scene — lúc đó mọi lớp chữ đã hiện xong nhưng chưa mờ đi.

Dùng:
  python tools/anh-scene.py <thu-muc-du-an>
  python tools/anh-scene.py <thu-muc-du-an> --file scenes-v2.json --video 05-output/001.mp4
"""
import argparse
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    p = argparse.ArgumentParser(description="Trích ảnh từng scene để kiểm duyệt")
    p.add_argument("du_an")
    p.add_argument("--file", help="tên file scenes json (mặc định scenes.json)")
    p.add_argument("--video", help="đường dẫn MP4 (mặc định lấy khoá 'ra' trong json)")
    p.add_argument("--ra", help="thư mục ảnh ra (mặc định <du-an>/_kiem-scene/)")
    a = p.parse_args()

    du_an = a.du_an if os.path.isabs(a.du_an) else os.path.join(GOC, a.du_an)
    if not os.path.isdir(du_an):
        sys.exit(f"Không thấy thư mục dự án: {du_an}")

    ten_json = a.file or ("scenes.json" if os.path.exists(os.path.join(du_an, "scenes.json"))
                          else "scenes-v2.json")
    scenes_json = os.path.join(du_an, ten_json)
    if not os.path.exists(scenes_json):
        sys.exit(f"Không thấy {scenes_json}")
    cfg = json.load(open(scenes_json, encoding="utf-8"))

    video = a.video or cfg.get("ra") or f"05-output/{os.path.basename(du_an.rstrip(chr(92) + '/'))}.mp4"
    video = video if os.path.isabs(video) else os.path.join(GOC, video)
    if not os.path.exists(video):
        sys.exit(f"Không thấy video: {video}\nRender trước bằng tools/make-video.py")

    thu_muc_ra = a.ra or os.path.join(du_an, "_kiem-scene")
    os.makedirs(thu_muc_ra, exist_ok=True)

    tong = float(cfg["duration"])
    print(f"Trích {len(cfg['scenes'])} ảnh từ {os.path.basename(video)} -> {thu_muc_ra}\n")

    for i, sc in enumerate(cfg["scenes"]):
        t0 = float(sc["start"])
        t1 = float(sc.get("end", tong))

        # Chờ dòng chữ CUỐI hiện xong rồi mới chụp. Lấy 60% quãng scene là
        # chưa đủ: dòng có delay dài vẫn đang chạy animation, ảnh ra thiếu chữ
        # và người kiểm tưởng lỗi dựng.
        # Biên 1.4s = 0.75s animation `rise` + ~0.6s lệch giữa mốc thời gian
        # trong MP4 và mốc animation (Chromium mất một nhịp khởi động ghi hình
        # sau khi thả animation). Đo thực tế trên video 002: dòng delay 2.1
        # chỉ hiện đủ ở giây 3.5 của scene, không phải 2.85 như tính lý thuyết.
        tre_nhat = max((float(el.get("delay", 0)) for el in sc.get("lines", [])),
                       default=0.0)
        moc = max(t0 + (t1 - t0) * 0.6, t0 + tre_nhat + 1.4)
        moc = min(moc, t1 - 0.35)          # tránh rơi vào lúc scene đang mờ đi
        moc = max(moc, t0 + 0.3)
        ten = f"{i:02d}_{t0:06.2f}s.png"
        dich = os.path.join(thu_muc_ra, ten)

        kq = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{moc:.3f}", "-i", video,
             "-frames:v", "1", dich],
            capture_output=True, text=True,
        )
        if kq.returncode != 0:
            print(f"  LOI  scene {i}: {kq.stderr.strip()[:200]}")
            continue

        # Chữ hiện trong scene, gộp lại để người kiểm đối chiếu với ảnh
        chu = " | ".join(
            (el.get("text", "") if "donut" not in el else f"[donut {el['donut']}%] {el.get('text','')}")
            .replace("<br>", " ")
            for el in sc.get("lines", [])
        )
        # bỏ thẻ HTML cho dễ đọc
        while "<" in chu and ">" in chu:
            i0, i1 = chu.index("<"), chu.index(">")
            if i0 > i1:
                break
            chu = chu[:i0] + chu[i1 + 1:]

        tu_lieu = sc.get("image") or sc.get("video") or "(không nền)"
        print(f"  {ten}   {t0:.1f}-{t1:.1f}s   nền: {os.path.basename(tu_lieu)}")
        print(f"       chữ: {chu[:150]}")

    print(f"\nXong. Mở từng ảnh trong {thu_muc_ra} để kiểm.")


if __name__ == "__main__":
    main()

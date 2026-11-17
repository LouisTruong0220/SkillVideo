# -*- coding: utf-8 -*-
"""
Dựng một video hoàn chỉnh bằng MỘT lệnh: HTML -> ghi hình -> ghép giọng -> ghép nhạc.

Gộp ba lệnh rời trong README dự án 001 lại. Không có bước này thì quy trình
không tự động được — mỗi lần render vẫn phải gõ tay ba lệnh dài dễ sai.

Dùng:
  python tools/make-video.py <thu-muc-du-an>                 # render thật
  python tools/make-video.py <thu-muc-du-an> --nhap          # render nháp, xem nhịp
  python tools/make-video.py <thu-muc-du-an> --file scenes-v2.json
  python tools/make-video.py <thu-muc-du-an> --chi-nhac      # chỉ ghép lại nhạc

Cấu hình lấy từ chính file scenes json (build-frame.py bỏ qua các khoá lạ nên
thêm vào đây là an toàn):

  {
    "title":    "...",
    "duration": 77.0,
    "giong":    "05-output/voice/002-roi.mp3",   đường dẫn từ GỐC DỰ ÁN
    "nhac":     "assets/nhac-nen.mp3",           đường dẫn từ thư mục dự án
    "nhac_am_luong": 0.16,
    "lead_in":  0.2,
    "ra":       "05-output/002-roi.mp4",
    "scenes":   [ ... ]
  }

Chế độ nháp: 540×960, preset ultrafast, bỏ nhạc nền. Đủ để duyệt thứ tự hình và
nhịp. Ghi hình vẫn chạy theo thời gian thật (Chromium ghi màn hình), nên video
77 giây vẫn mất 77 giây — chỉ khâu mã hoá là nhanh lên.
"""
import argparse
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_FRAME = os.path.join(GOC, "tools", "build-frame.py")
RENDER = os.path.join(GOC, "tools", "render-video.mjs")


def goi_ten(d):
    """Rút gọn đường dẫn cho dễ đọc. relpath ném lỗi khi khác ổ đĩa."""
    if not d:
        return "(không)"
    try:
        return os.path.relpath(d, GOC)
    except ValueError:
        return d


def chay(lenh, moi_truong=None, ten_buoc=""):
    env = dict(os.environ, **(moi_truong or {}))
    kq = subprocess.run(lenh, env=env, cwd=GOC)
    if kq.returncode != 0:
        print(f"\nDUNG LAI: bước '{ten_buoc}' lỗi (mã {kq.returncode}).")
        sys.exit(kq.returncode)


def tim_scenes(du_an, ten_file):
    if ten_file:
        d = os.path.join(du_an, ten_file) if not os.path.isabs(ten_file) else ten_file
        if not os.path.exists(d):
            sys.exit(f"Không thấy {d}")
        return d
    for ten in ("scenes.json", "scenes-v2.json"):
        d = os.path.join(du_an, ten)
        if os.path.exists(d):
            return d
    sys.exit(f"Không thấy scenes.json trong {du_an}")


def duong_dan(goc_tuong_doi, gia_tri):
    """Ghép đường dẫn tương đối, giữ nguyên nếu là đường dẫn tuyệt đối."""
    if not gia_tri:
        return None
    return gia_tri if os.path.isabs(gia_tri) else os.path.join(goc_tuong_doi, gia_tri)


def kiem_tu_lieu(cfg, du_an, giong, nhac):
    """Kiểm mọi file scene cần TRƯỚC khi render.

    build-frame.py nhúng ảnh base64 nên chỉ phát hiện ảnh thiếu ở giữa chừng.
    Với video 15 scene thì đó là vài phút đổ đi vì một dòng đường dẫn sai.
    """
    thieu = []
    for i, sc in enumerate(cfg["scenes"]):
        for khoa in ("image", "video"):
            if sc.get(khoa):
                d = os.path.join(du_an, sc[khoa])
                if not os.path.exists(d):
                    thieu.append(f"  scene {i} ({sc.get('start')}s) -> {khoa}: {sc[khoa]}")
    if giong and not os.path.exists(giong):
        thieu.append(f"  giọng: {goi_ten(giong)}")
    if nhac and not os.path.exists(nhac):
        thieu.append(f"  nhạc: {goi_ten(nhac)}")

    if thieu:
        print("THIEU TU LIEU — chưa render được:\n" + "\n".join(thieu))
        print("\nSửa đường dẫn trong scenes json, hoặc bổ sung file rồi chạy lại.")
        sys.exit(2)


def kiem_muot(video, tong_giay):
    """Bắt lỗi giật hình do ghi hình rớt frame khi máy bận.

    render-video.mjs ghi hình bằng Chromium theo thời gian thực. Máy bận (đang
    chạy render/agent khác) thì Chromium không kịp dựng, lặp lại frame cũ — video
    ra đủ 30fps nhưng nhiều frame trùng nhau, xem thấy giật ở các đoạn chuyển ảnh.
    Đã gặp thật ở video 005: nửa sau chỉ ~10 frame khác nhau mỗi 5 giây.

    Cách đo: mpdecimate bỏ frame gần-trùng, đếm frame CÒN LẠI theo từng vùng 5s.
    Vùng nào (trong thời lượng) < 55/150 là giật. Trả (ok, mô_tả_vùng_xấu).
    """
    try:
        kq = subprocess.run(
            ["ffmpeg", "-hide_banner", "-i", video,
             "-vf", "mpdecimate=hi=200:lo=100:frac=0.33,showinfo", "-f", "null", "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
    except Exception as e:
        print(f"  (bỏ qua kiểm mượt: {e})")
        return True, ""

    moc = [float(m.split(":")[1]) for m in
           __import__("re").findall(r"pts_time:[0-9.]+", kq.stderr)]
    if not moc:
        return True, ""
    vung = {}
    for t in moc:
        if t < tong_giay - 1:                 # bỏ frame giữ cuối cùng
            vung[int(t // 5) * 5] = vung.get(int(t // 5) * 5, 0) + 1
    xau = [(k, n) for k, n in sorted(vung.items()) if n < 55]
    if xau:
        mo_ta = ", ".join(f"{k}-{k+5}s:{n}/150" for k, n in xau)
        return False, mo_ta
    return True, ""


def ghep_nhac(video_vao, nhac, video_ra, tong_giay, am_luong):
    """Ghép nhạc nền dưới giọng, có ducking — nhạc tự nhỏ lại khi có tiếng nói."""
    tat_dan = max(0.0, tong_giay - 3)
    loc = (
        f"[1:a]volume={am_luong},afade=t=in:d=1.5,afade=t=out:st={tat_dan:.2f}:d=3[m];"
        f"[m][0:a]sidechaincompress=threshold=0.02:ratio=8:attack=6:release=350[md];"
        f"[0:a][md]amix=inputs=2:duration=first:normalize=0[a]"
    )
    chay(["ffmpeg", "-y", "-v", "error", "-i", video_vao, "-i", nhac,
          "-filter_complex", loc, "-map", "0:v", "-map", "[a]",
          "-c:v", "copy", "-c:a", "aac", "-b:a", "176k", video_ra],
         ten_buoc="ghép nhạc nền")


def main():
    p = argparse.ArgumentParser(description="Dựng video Roboworld bằng một lệnh")
    p.add_argument("du_an", help="thư mục dự án trong 04-video-projects/")
    p.add_argument("--file", help="tên file scenes json (mặc định scenes.json)")
    p.add_argument("--nhap", action="store_true",
                   help="render nháp: 540×960, mã hoá nhanh, bỏ nhạc nền")
    p.add_argument("--chi-nhac", action="store_true",
                   help="chỉ ghép lại nhạc từ bản đã render, không render lại")
    p.add_argument("--ra", help="đường dẫn MP4 xuất ra (đè giá trị trong json)")
    a = p.parse_args()

    du_an = a.du_an if os.path.isabs(a.du_an) else os.path.join(GOC, a.du_an)
    if not os.path.isdir(du_an):
        sys.exit(f"Không thấy thư mục dự án: {du_an}")

    scenes_json = tim_scenes(du_an, a.file)
    cfg = json.load(open(scenes_json, encoding="utf-8"))
    tong_giay = float(cfg["duration"])
    ten_du_an = os.path.basename(du_an.rstrip("\\/"))

    giong = duong_dan(GOC, cfg.get("giong"))
    nhac = duong_dan(du_an, cfg.get("nhac"))
    am_luong = float(cfg.get("nhac_am_luong", 0.16))
    lead_in = float(cfg.get("lead_in", 0.2))

    # Bản chỉ có giọng giữ lại trong thư mục dự án: đổi nhạc thì không phải
    # render lại từ đầu (mất vài phút), chỉ chạy lại bước ghép.
    goc_ten = os.path.splitext(os.path.basename(scenes_json))[0]
    trung_gian = os.path.join(du_an, f"_{goc_ten}-chi-giong.mp4")

    ra = a.ra or cfg.get("ra") or f"05-output/{ten_du_an}.mp4"
    ra = duong_dan(GOC, ra)
    if a.nhap:
        ra = os.path.join(GOC, "05-output", f"_nhap-{ten_du_an}.mp4")

    print(f"Dự án : {ten_du_an}")
    print(f"Scenes: {os.path.basename(scenes_json)}  ({tong_giay}s, {len(cfg['scenes'])} scene)")
    print(f"Giọng : {goi_ten(giong)}")
    print(f"Nhạc  : {goi_ten(nhac)}"
          + ("  [bỏ qua ở bản nháp]" if a.nhap and nhac else ""))
    print(f"Xuất  : {goi_ten(ra)}"
          + ("   *** BẢN NHÁP 540×960 ***" if a.nhap else ""))
    print()

    kiem_tu_lieu(cfg, du_an, giong, None if a.nhap else nhac)

    t0 = time.time()

    if a.chi_nhac:
        if not (nhac and os.path.exists(trung_gian)):
            sys.exit("--chi-nhac cần sẵn bản chỉ-giọng và khoá 'nhac' trong json.")
        print("[1/1] Ghép lại nhạc nền ...")
        ghep_nhac(trung_gian, nhac, ra, tong_giay, am_luong)
        print(f"\nXONG ({time.time() - t0:.0f}s): {ra}")
        return

    print("[1/3] Dựng HTML tự chứa ...")
    chay([sys.executable, BUILD_FRAME, scenes_json], ten_buoc="build-frame")
    frame_html = os.path.splitext(scenes_json)[0] + ".html"

    env = {}
    if a.nhap:
        env = {"RBW_PRESET": "ultrafast", "RBW_CRF": "30", "RBW_W": "540", "RBW_H": "960"}
    dich_buoc2 = ra if (a.nhap or not nhac) else trung_gian

    # Ghi hình + ghép nhạc, tự kiểm mượt và thử lại tối đa 2 lần.
    # Bản nháp không cần kiểm (giật không quan trọng khi chỉ duyệt nhịp).
    so_lan = 1 if a.nhap else 3
    for lan in range(1, so_lan + 1):
        print(f"[2/3] Ghi hình + ghép giọng ({tong_giay:.0f}s thực tế, chờ chút)"
              + (f" — lần {lan}" if lan > 1 else "") + " ...")
        chay(["node", RENDER, frame_html, dich_buoc2, str(tong_giay),
              giong or "-", str(lead_in)], moi_truong=env, ten_buoc="render-video")

        if a.nhap or not nhac:
            print("[3/3] Bỏ qua nhạc nền.")
        else:
            if not os.path.exists(nhac):
                sys.exit(f"Không thấy file nhạc: {nhac}")
            print("[3/3] Ghép nhạc nền (ducking) ...")
            ghep_nhac(trung_gian, nhac, ra, tong_giay, am_luong)

        if a.nhap:
            break
        muot, xau = kiem_muot(ra, tong_giay)
        if muot:
            if lan > 1:
                print("  Kiểm mượt: ĐẠT (đã render lại).")
            break
        if lan < so_lan:
            print(f"  ⚠ GIẬT HÌNH ở {xau} — máy có thể đang bận. Render lại...")
        else:
            print(f"  ⚠ VẪN GIẬT ở {xau} sau {so_lan} lần. Đóng bớt việc nặng "
                  f"(render/agent khác) rồi chạy lại lệnh này.")

    mb = os.path.getsize(ra) / 1024 / 1024
    print(f"\nXONG ({time.time() - t0:.0f}s): {ra}  ({mb:.1f} MB)")
    if not a.nhap:
        print(f"Kiểm: ffprobe -v error -show_entries stream=width,height,r_frame_rate "
              f"-show_entries format=duration \"{ra}\"")


if __name__ == "__main__":
    main()

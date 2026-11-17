# -*- coding: utf-8 -*-
"""Vùng an toàn TikTok/Reels + chụp ảnh tĩnh composition HyperFrames. Dùng chung cho soi.py và kiem.py.

Chụp bằng `hyperframes snapshot --at` — không trích khung video nguồn, không xử lý âm thanh, nên ~1–2 s/ảnh thay vì
~2–3 phút dựng cả video (đo 17/11/2026: 7 ảnh / 14 s).
"""
import re, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
from chung import AN_TOAN, ENV_HF, HF, H, W

# Vùng cấm cho CHỮ mình thêm (toạ độ khung 1080×1920). Khối tự vẽ phải giữ chữ top ≥ 250, mép phải ≤ 940.
CAM_TREN = AN_TOAN["tren"]          # 230: thanh tab "Đang theo dõi / Dành cho bạn"
CAM_DUOI = AN_TOAN["duoi"]          # 1440: tên kênh + caption
CAM_PHAI = AN_TOAN["phai"]          # 940: cột nút tim / bình luận / chia sẻ


def chup(hf, moc, ra, an_hinh=False, timeout_ms=45000):
    """Chụp composition `hf` ở các mốc giây → {giây: Path png}. an_hinh=True: giấu mọi <video>/<img> (chỉ còn chữ/đồ hoạ)."""
    ra = Path(ra)
    if ra.exists():
        shutil.rmtree(ra)
    goc = hf / "index.html"
    ban_goc = goc.read_text("utf-8")
    try:
        if an_hinh:
            goc.write_text(ban_goc.replace("</head>", "<style>video,img{opacity:0!important}#root{background:#000!important}</style></head>", 1), "utf-8")
        at = ",".join(f"{t:.3f}".rstrip("0").rstrip(".") for t in moc)
        r = subprocess.run([str(HF), "snapshot", str(hf), "--at", at, "--no-end", "-o", str(ra), "--timeout", str(timeout_ms)],
                           env=ENV_HF, capture_output=True, text=True, encoding="utf-8", errors="replace")
    finally:
        goc.write_text(ban_goc, "utf-8")
    if r.returncode != 0:
        print("✗ hyperframes snapshot lỗi:\n", r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
    kq = {}
    for p in ra.glob("frame-*-at-*s.png"):
        m = re.search(r"-at-([\d.]+)s\.png$", p.name)
        if m:
            kq[float(m.group(1))] = p
    # khớp lại mốc đã xin (tên file bỏ số 0 thừa)
    return {t: kq[min(kq, key=lambda x: abs(x - t))] for t in moc if kq}


def ke_vach(anh, day=4):
    """Kẻ vạch vùng cấm lên ảnh PIL (cỡ bất kỳ — tự quy đổi từ 1080×1920)."""
    a = anh.convert("RGB")
    d = ImageDraw.Draw(a)
    sx, sy = a.width / W, a.height / H
    mau = (0, 230, 255)
    d.line([(0, CAM_TREN * sy), (a.width, CAM_TREN * sy)], fill=mau, width=day)
    d.line([(0, CAM_DUOI * sy), (a.width, CAM_DUOI * sy)], fill=mau, width=day)
    d.line([(CAM_PHAI * sx, 0), (CAM_PHAI * sx, a.height)], fill=mau, width=day)
    return a


def diem_lan(anh, nguong=150, it_nhat=40):
    """Ảnh đã giấu video/ảnh (nền đen) → các vùng có điểm sáng (max kênh > nguong) nằm trong vùng cấm.
    Trả [(vùng, (x0, y0, x1, y1), số điểm)]; bỏ qua vùng < it_nhat điểm (nhiễu khử răng cưa)."""
    import numpy as np
    a = np.asarray(anh.convert("RGB").resize((W, H))).astype(np.int16)
    sang = a.max(axis=2) > nguong
    # đỏ thuần (viền bảng nửa trên, dấu X…) không phải chữ — chữ đỏ của mình luôn có viền trắng nên vẫn bị bắt
    sang &= ~((a[..., 0] > 170) & (a[..., 1] < 120) & (a[..., 2] < 120))
    # đường kẻ ngang gần hết bề ngang không phải chữ → bỏ
    sang[sang.sum(axis=1) > 0.8 * W, :] = False
    ra = []
    for ten, o in (("đỉnh 12%", sang[:CAM_TREN, :]), ("đáy 25%", sang[CAM_DUOI:, :]), ("cột phải 140 px", sang[CAM_TREN:CAM_DUOI, CAM_PHAI:])):
        n = int(o.sum())
        if n < it_nhat:
            continue
        ys, xs = np.nonzero(o)
        dy = 0 if ten == "đỉnh 12%" else (CAM_DUOI if ten == "đáy 25%" else CAM_TREN)
        dx = CAM_PHAI if ten.startswith("cột") else 0
        ra.append((ten, (int(xs.min()) + dx, int(ys.min()) + dy, int(xs.max()) + dx, int(ys.max()) + dy), n))
    return ra


def quet_video_nua_tren(video, bat_dau, dai, t0, buoc=0.2, nguong=150, it_nhat=40):
    """Cảnh nửa trên tự dựng (Remotion rm-*.mp4, nền tối, khung 1080×960, đặt ở đỉnh khung dọc) → điểm sáng ở đỉnh 12%
    hoặc cột phải 140 px. Bỏ 20 px đáy (viền đỏ). Trả [(giây trên video thành phẩm, vùng, hộp, số điểm)]."""
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{bat_dau}", "-t", f"{dai}", "-i", str(video),
                        "-vf", f"fps={1 / buoc},scale={W}:960", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True)
    khung = np.frombuffer(r.stdout, np.uint8)
    n = khung.size // (W * 960 * 3)
    ra = []
    for i in range(n):
        f = khung[i * W * 960 * 3:(i + 1) * W * 960 * 3].reshape(960, W, 3).astype(np.int16)
        sang = f.max(axis=2) > nguong
        sang &= ~((f[..., 0] > 170) & (f[..., 1] < 120) & (f[..., 2] < 120))
        sang[940:, :] = False
        sang[sang.sum(axis=1) > 0.8 * W, :] = False
        for ten, o, dx, dy in (("đỉnh 12%", sang[:CAM_TREN, :], 0, 0), ("cột phải 140 px", sang[CAM_TREN:, CAM_PHAI:], CAM_PHAI, CAM_TREN)):
            if int(o.sum()) >= it_nhat:
                ys, xs = np.nonzero(o)
                ra.append((round(t0 + i * buoc, 2), ten, (int(xs.min()) + dx, int(ys.min()) + dy, int(xs.max()) + dx, int(ys.max()) + dy), int(o.sum())))
    return ra

# -*- coding: utf-8 -*-
"""Hàm dùng chung cho bộ dựng video thô. Không chạy trực tiếp."""
import json, os, re, subprocess, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

CONG_CU = Path(__file__).resolve().parent            # tools/video-tho
GOC = CONG_CU.parents[1]                               # D:\RBW_Claude
KHO_AM = GOC / "02-media" / "am-thanh"
FPS = 30
W, H = 1080, 1920
BUOC_RMS = 0.01  # nghe-chep.py ghi năng lượng âm 10 ms một ô

# Vùng an toàn nền tảng (TikTok/Reels/Shorts): đỉnh ~12% có thanh tìm kiếm, đáy ~25% có tên kênh + caption,
# mép phải ~130px có cột nút tim/bình luận. Chữ quan trọng nằm trong khung này.
AN_TOAN = {"tren": int(H * 0.12), "duoi": int(H * 0.75), "trai": 70, "phai": W - 140}


def gan_bia(video, anh):
    """Nhúng ảnh bìa vào MP4 (luồng mjpeg đánh dấu attached_pic) — KHÔNG đụng hình/tiếng (chép nguyên luồng).
    Chỉ trình quản lý file trên máy tính (File Explorer, VLC…) hiện ảnh này. Zalo / Messenger / Telegram / thư viện
    điện thoại / TikTok / Reels lấy KHUNG HÌNH ĐẦU, bỏ qua ảnh nhúng (thấy thật 17/11/2026, video 012):
    khi đăng vẫn phải chọn ảnh bìa thủ công (tải anh-bia.jpg lên ở bước chọn bìa)."""
    video, anh = Path(video), Path(anh)
    if not (video.exists() and anh.exists()):
        return False
    tam = video.with_suffix(".co-bia.tmp.mp4")
    chay(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", anh, "-map", "0:v:0", "-map", "0:a:0?", "-map", "1:0",
          "-c", "copy", "-disposition:v:1", "attached_pic", "-movflags", "+faststart", tam], "gắn ảnh bìa")
    tam.replace(video)
    return True


def chay(lenh, ten="", im=False):
    """Chạy lệnh, dừng hẳn kèm stderr nếu lỗi."""
    r = subprocess.run([str(x) for x in lenh], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"✗ Lỗi ở bước {ten or lenh[0]}:\n{r.stderr[-3000:]}")
        sys.exit(1)
    if not im and r.stdout.strip():
        print(r.stdout.strip()[-2000:])
    return r


def do(file):
    """ffprobe → dict gọn: giay, w, h, fps, xoay, co_tieng."""
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(file)],
                       capture_output=True, text=True, encoding="utf-8")
    j = json.loads(r.stdout or "{}")
    v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), None)
    a = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), None)
    xoay = 0
    if v:
        for sd in v.get("side_data_list", []) or []:
            if "rotation" in sd:
                xoay = int(float(sd["rotation"]))
        xoay = int(v.get("tags", {}).get("rotate", xoay))
    w, h = (v["width"], v["height"]) if v else (0, 0)
    if abs(xoay) in (90, 270):
        w, h = h, w
    fps = 0.0
    if v and v.get("avg_frame_rate", "0/0") != "0/0":
        n, d = v["avg_frame_rate"].split("/")
        fps = float(n) / float(d) if float(d) else 0.0
    return {"giay": float(j.get("format", {}).get("duration", 0) or 0), "w": w, "h": h, "fps": round(fps, 3),
            "xoay": xoay, "co_tieng": a is not None, "co_hinh": v is not None}


def doc_json(p, mac_dinh=None):
    p = Path(p)
    if not p.exists():
        if mac_dinh is not None:
            return mac_dinh
        print(f"✗ Thiếu file {p}")
        sys.exit(1)
    return json.loads(p.read_text("utf-8"))


def ghi_json(p, du_lieu):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(du_lieu, ensure_ascii=False, indent=2), "utf-8")


def du_an(duong_dan):
    """Thư mục dự án (tuyệt đối). Chấp nhận '012-ten' ngắn gọn → 04-video-projects/012-ten."""
    p = Path(duong_dan)
    if not p.is_absolute() and len(p.parts) == 1 and not p.exists():
        p = GOC / "04-video-projects" / duong_dan
    return p.resolve()


def lam_tron_khung(t):
    """Làm tròn về lưới khung hình 1/30 s — hình và tiếng cắt cùng một chỗ thì không lệch tiếng."""
    return round(round(t * FPS) / FPS, 4)


def bo_dau(s):
    """Chữ thường, bỏ dấu câu — để so hai câu có phải nói lại không."""
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def mm_ss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


PY_VENV = CONG_CU / ".venv" / "Scripts" / "python.exe"
HF = CONG_CU / "node_modules" / ".bin" / "hyperframes.cmd"
# Đã thử 16–17/11/2026 để bớt phí cố định ~45–50 s mỗi lần render (extract ~20 s · prehash ~8 s · audio ~14 s ·
# reference_background ~4 s, cộng mỗi khúc chụp thử BeginFrame hỏng rồi chạy lại bằng screenshot):
# PRODUCER_FORCE_SCREENSHOT=true, HYPERFRAMES_EXTRACT_CACHE_MAX_MB=8192, --workers 1/2 — KHÔNG nhanh hơn (cache luôn
# miss vì khoá theo thư mục tạm của mỗi lần render). Đừng thử lại; soi nhanh bằng soi.py (hyperframes snapshot).
ENV_HF = {**os.environ, "HYPERFRAMES_NO_TELEMETRY": "1", "DO_NOT_TRACK": "1", "HYPERFRAMES_NO_UPDATE_CHECK": "1"}

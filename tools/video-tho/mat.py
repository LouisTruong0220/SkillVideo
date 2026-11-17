# -*- coding: utf-8 -*-
"""B5 — Dò khuôn mặt trên bản cắt (YuNet) → build/mat.json. dung.py dùng để:
  - phóng to/khung cận lấy TÂM là mặt (không phóng vào bụng)
  - đặt phụ đề/tiêu đề tránh mặt, chia đôi màn hình mà mặt vẫn nằm trong nửa dưới

    tools/video-tho/.venv/Scripts/python.exe tools/video-tho/mat.py <du-an>
"""
import argparse, shutil
import cv2
import numpy as np
from chung import CONG_CU, GOC, FPS, doc_json, du_an, ghi_json

MO_HINH = CONG_CU / "models" / "face_detection_yunet_2023mar.onnx"
NGUON_MO_HINH = GOC / "11-app-nova" / "nhan-dien-khuon-mat" / "android" / "app" / "src" / "main" / "assets" / "mo-hinh" / MO_HINH.name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("--moi", type=float, default=0.25, help="dò mỗi bao nhiêu giây")
    g = ap.parse_args()
    da = du_an(g.du_an)
    if not MO_HINH.exists():
        MO_HINH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(NGUON_MO_HINH, MO_HINH)

    cap = cv2.VideoCapture(str(da / "build" / "da-cat.mp4"))
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    s = 0.5  # dò trên ảnh thu nhỏ một nửa cho nhanh
    dt = cv2.FaceDetectorYN.create(str(MO_HINH), "", (int(w * s), int(h * s)), 0.7, 0.3, 5000)
    buoc = max(1, round(g.moi * FPS))
    ra, k = [], 0
    while True:
        ok, khung = cap.read()
        if not ok:
            break
        if k % buoc == 0:
            _, mat = dt.detect(cv2.resize(khung, (int(w * s), int(h * s))))
            if mat is not None and len(mat):
                m = max(mat, key=lambda r: r[2] * r[3])       # mặt to nhất = người nói
                x, y, mw, mh = (float(v) / s for v in m[:4])
                ra.append({"t": round(k / FPS, 2), "cx": round(x + mw / 2), "cy": round(y + mh / 2),
                           "w": round(mw), "h": round(mh)})
            else:
                ra.append({"t": round(k / FPS, 2), "cx": None})
        k += 1
    co = [r for r in ra if r["cx"] is not None]
    tom = {"ti_le_thay_mat": round(len(co) / max(1, len(ra)), 2)}
    if co:
        tom.update({k2: int(np.median([r[k2] for r in co])) for k2 in ("cx", "cy", "w", "h")})
    ghi_json(da / "build" / "mat.json", {"tom_tat": tom, "mau": ra})
    print(f"✓ build/mat.json · thấy mặt {tom['ti_le_thay_mat'] * 100:.0f}% khung · tâm mặt trung vị "
          f"({tom.get('cx')}, {tom.get('cy')}) cỡ {tom.get('w')}px")
    if tom["ti_le_thay_mat"] < 0.5:
        print("⚠ dưới nửa số khung thấy mặt — dung.py sẽ dùng tâm mặc định (giữa, 1/3 trên)")


if __name__ == "__main__":
    main()

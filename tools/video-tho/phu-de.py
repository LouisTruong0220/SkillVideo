# -*- coding: utf-8 -*-
"""B6 — Chia chữ thành cụm phụ đề → phu-de.txt (Claude sửa chính tả + đánh dấu từ nhấn rồi mới dựng).

    python tools/video-tho/phu-de.py <du-an> [--toi-da-tu 4] [--toi-da-ky-tu 20]

Mỗi dòng phu-de.txt:   a|b|chữ hiển thị
  - a, b: giây theo bản cắt (giữ nguyên, trừ khi gộp/tách dòng)
  - *từ* = tô màu nhấn (vàng). Mỗi cụm tối đa 1 chỗ nhấn, chỉ nhấn từ khoá thật (con số, lợi ích, tên ý chính).
  - Sửa chữ whisper chép sai: "Delabot" → "BellaBot", "đăng tính" → "đang tính", "lên hãy" → "liên hệ"…
  - Dòng bắt đầu bằng # là ghi chú, bỏ qua.
Phong cách kênh Duy Trường Robot (7 video mẫu): 2–4 chữ một cụm, không dấu câu, chữ trắng viền đen, từ khoá vàng.
"""
import argparse, re
from chung import doc_json, du_an

CUOI_CAU = re.compile(r"[.,!?;:…]$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("--toi-da-tu", type=int, default=4)
    ap.add_argument("--toi-da-ky-tu", type=int, default=20)
    g = ap.parse_args()
    da = du_an(g.du_an)
    tu = doc_json(da / "build" / "tu-moi.json")
    ra = da / "phu-de.txt"
    if ra.exists():
        ra.replace(da / "phu-de.cu.txt")
        print("· phu-de.txt cũ đổi tên thành phu-de.cu.txt (đề phòng đã sửa tay)")

    am_tiet = []
    for x in tu:
        sach = re.sub(r"[.,!?;:…\"“”]", "", x["w"]).strip()
        if sach:
            am_tiet.append({**x, "sach": sach})
    # Whisper trả từng ÂM TIẾT. Gom thành TỪ (pyvi) để không ngắt dòng giữa "nhà | hàng", "phục | vụ".
    don_vi = [[a] for a in am_tiet]
    try:
        from pyvi import ViTokenizer
        to = ViTokenizer.tokenize(" ".join(a["sach"] for a in am_tiet)).split()
        if sum(len(t.split("_")) for t in to) == len(am_tiet):
            don_vi, i = [], 0
            for t in to:
                n = len(t.split("_")); don_vi.append(am_tiet[i:i + n]); i += n
        else:
            print("· pyvi tách lệch số âm tiết — chia theo âm tiết")
    except ImportError:
        print("· thiếu pyvi — chia theo âm tiết (dễ ngắt giữa từ ghép)")

    cum, hien = [], []
    for dv in don_vi:
        x = dv[0]
        if hien:
            dai = len(" ".join(w["sach"] for w in hien + dv))
            ngat = (len(hien) + len(dv) > g.toi_da_tu or dai > g.toi_da_ky_tu or x["s"] - hien[-1]["e"] > 0.3
                    or x["doan"] != hien[-1]["doan"] or CUOI_CAU.search(hien[-1]["w"]))
            if ngat:
                cum.append(hien); hien = []
        hien += dv
    if hien:
        cum.append(hien)
    # cụm 1 chữ lẻ loi dính vào cụm trước nếu cùng đoạn và sát nhau
    gon = []
    for c in cum:
        if gon and len(c) == 1 and c[0]["doan"] == gon[-1][-1]["doan"] and c[0]["s"] - gon[-1][-1]["e"] < 0.2 \
                and len(gon[-1]) < g.toi_da_tu + 1:
            gon[-1] += c
        else:
            gon.append(c)

    dong = ["# a|b|chữ — *từ* = tô vàng. Sửa chính tả + đánh dấu nhấn trước khi chạy dung.py. Không đổi a|b nếu không gộp/tách."]
    for i, c in enumerate(gon):
        a = c[0]["s"]
        b = c[-1]["e"] + 0.2
        if i + 1 < len(gon) and gon[i + 1][0]["s"] - c[-1]["e"] < 0.5:
            b = gon[i + 1][0]["s"]
        dong.append(f"{a:.2f}|{b:.2f}|{' '.join(w['sach'] for w in c)}")
    ra.write_text("\n".join(dong) + "\n", "utf-8")
    print(f"✓ phu-de.txt · {len(gon)} cụm · trung bình {sum(len(c) for c in gon) / max(1, len(gon)):.1f} chữ/cụm")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""B3 — Máy đề xuất danh sách đoạn giữ lại → cat.json. Claude ĐỌC LẠI và sửa tay trước khi cắt.

    python tools/video-tho/de-xuat-cat.py <du-an> [--lang-giu 0.35]

Máy làm:
  - bỏ cả đảo: câu nói hỏng đã được nói lại ở sau (⟲), đảo ảo giác, đảo không có chữ
  - bỏ chữ: ậm ừ, cụm lặp liền, nửa câu đã nói lại
  - khoảng lặng > --lang-giu giây trong câu → cắt bỏ, còn lại ~0,25 s (đệm trước 0,10 + sau 0,15) cho tự nhiên
Máy KHÔNG làm (việc của Claude khi đọc ban-chep.md): chọn bản nói hay hơn khi hai bản cùng trọn vẹn, đảo thứ tự ý,
bỏ câu thừa/lạc đề, giữ một câu "nói lại" vì bản sau kém hơn.
"""
import argparse
import numpy as np
from chung import BUOC_RMS, doc_json, du_an, ghi_json, lam_tron_khung, mm_ss

BO_TU = {"am-u", "lap", "noi-lai-duoi"}
BO_DAO = {"noi-lai", "ao-giac", "khong-chu"}
TRUOC, SAU, SAU_TOI_DA = 0.10, 0.15, 0.35


def keo_duoi(db, nguong, t, gioi_han):
    """Whisper hay chấm hết chữ cuối quá sớm (âm cuối còn ngân). Kéo b theo năng lượng tới khi tắt tiếng."""
    i = int(t / BUOC_RMS)
    j = min(int(gioi_han / BUOC_RMS), len(db))
    while i < j and db[i] > nguong:
        i += 1
    return i * BUOC_RMS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("--lang-giu", type=float, default=0.35, help="khoảng lặng trong câu dài hơn mức này thì cắt")
    g = ap.parse_args()
    da = du_an(g.du_an)
    chep = doc_json(da / "build" / "chep.json")

    doan, bo = [], []
    for c in chep["clip"]:
        db = np.load(da / "build" / f"{c['id']}.rms.npy")
        nguong = c["nguong_db"]
        for o in c["dao"]:
            ly_do = BO_DAO & set(o["co"])
            if ly_do:
                bo.append({"dao": o["id"], "chu": o["chu"], "ly_do": ", ".join(sorted(ly_do))
                           + (f" (bản giữ: {o['noi_lai_boi']})" if "noi_lai_boi" in o else "")})
                continue
            nhom, truoc_bo = [], o["a"] - 0.1
            for i, x in enumerate(o["tu"]):
                if BO_TU & set(x["co"]):
                    bo.append({"dao": o["id"], "chu": x["w"], "t": x["s"], "ly_do": ", ".join(sorted(BO_TU & set(x["co"])))})
                    if nhom:
                        doan.append((c["id"], o["id"], nhom, truoc_bo, x["s"] - 0.03)); nhom = []
                    truoc_bo = x["e"] + 0.02
                    continue
                if nhom and x["s"] - nhom[-1]["e"] > g.lang_giu:
                    doan.append((c["id"], o["id"], nhom, truoc_bo, x["s"] - 0.03))
                    truoc_bo, nhom = nhom[-1]["e"] + 0.02, []
                nhom.append(x)
            if nhom:
                doan.append((c["id"], o["id"], nhom, truoc_bo, o["b"] + 0.25))
            for k in o.get("tieng_khong_chu", []):
                bo.append({"dao": o["id"], "chu": "[tiếng không thành chữ]", "t": k["s"], "ly_do": f"{k['e'] - k['s']:.2f}s"})

    ra = []
    for cid, did, nhom, san, tran in doan:
        c = next(x for x in chep["clip"] if x["id"] == cid)
        db = np.load(da / "build" / f"{cid}.rms.npy")
        a = max(nhom[0]["s"] - TRUOC, san, 0.0)
        b = min(max(nhom[-1]["e"] + SAU, keo_duoi(db, c["nguong_db"], nhom[-1]["e"], nhom[-1]["e"] + SAU_TOI_DA) + 0.05),
                tran, c["giay"])
        a, b = lam_tron_khung(a), lam_tron_khung(b)
        # cách đoạn trước < 0,3 s (nhịp thở giữa hai đảo) → gộp: cắt ở đó là cắt giữa từ ("thậm | chí") và đổi khung vô cớ
        if ra and ra[-1]["clip"] == cid and a <= ra[-1]["b"] + 0.30:
            ra[-1]["b"] = max(ra[-1]["b"], b); ra[-1]["chu"] += " " + " ".join(x["w"] for x in nhom)
            continue
        ra.append({"clip": cid, "dao": did, "a": a, "b": b, "chu": " ".join(x["w"] for x in nhom)})
    for i, x in enumerate(ra, 1):
        x["id"] = f"d{i:02d}"
        x.update({k: x.pop(k) for k in ("clip", "dao", "a", "b", "chu")})

    goc = sum(c["giay"] for c in chep["clip"])
    giu = sum(x["b"] - x["a"] for x in ra)
    ghi_json(da / "cat.json", {
        "_huong_dan": "Claude sửa tay: xoá đoạn thừa, đổi thứ tự (thứ tự trong mảng = thứ tự trong video), chỉnh a/b "
                      "(giây theo clip gốc). Đoạn 'bo' chỉ để tra lại, không ảnh hưởng gì.",
        "doan": [{"id": x["id"], "clip": x["clip"], "a": x["a"], "b": x["b"], "chu": x["chu"]} for x in ra],
        "bo": bo})
    print(f"{len(ra)} đoạn giữ · {giu:.1f}s / {goc:.1f}s gốc (bỏ {goc - giu:.1f}s) · {len(bo)} chỗ bỏ")
    for x in ra:
        print(f"  {x['id']} {x['clip']} {mm_ss(x['a'])}–{mm_ss(x['b'])}  {x['chu'][:90]}")
    print("✓ cat.json — đọc lại cùng build/ban-chep.md rồi mới chạy cat-ghep.py")


if __name__ == "__main__":
    main()

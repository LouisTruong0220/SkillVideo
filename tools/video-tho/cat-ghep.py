# -*- coding: utf-8 -*-
"""B4 — Cắt và ghép theo cat.json → bản cắt thô + bảng chữ theo dòng thời gian MỚI.

    python tools/video-tho/cat-ghep.py <du-an> [--toc-do 1.2]

--toc-do (hoặc "toc_do" trong cat.json): nói nhanh lên bao nhiêu lần. atempo giữ nguyên cao độ giọng —
1,1–1,2 vẫn tự nhiên; > 1,25 bắt đầu nghe "tua". Mọi mốc ra (tu-moi, moc-cat, ban-cat) đã chia theo hệ số.

Ra:
  build/da-cat.mp4     1080×1920 30 fps — nền cho bước dựng (đây cũng là bản cho anh Trường duyệt nhịp cắt)
  build/tu-moi.json    từng chữ với mốc thời gian MỚI (đã bỏ ậm ừ) — nguồn của phụ đề
  build/ban-cat.md     bảng đoạn theo thời gian mới — để lên kế hoạch chữ/cảnh phụ/hiệu ứng
  build/moc-cat.json   mốc các điểm cắt (dựng.py dùng để đổi khung rộng/cận che giật hình)
"""
import argparse
from chung import FPS, chay, do, doc_json, du_an, ghi_json, lam_tron_khung, mm_ss

BO_TU = {"am-u", "lap", "noi-lai-duoi"}
NOI_TIENG = 0.012  # 12 ms tăng/giảm âm ở mỗi mép cắt — không còn tiếng "tạch"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("--chi-chu", action="store_true", help="chỉ dựng lại tu-moi/moc-cat/ban-cat, không cắt lại video")
    ap.add_argument("--toc-do", type=float, help="hệ số nói nhanh (mặc định lấy toc_do trong cat.json, không có = 1)")
    g = ap.parse_args()
    da = du_an(g.du_an)
    so = doc_json(da / "du-an.json")
    cat = doc_json(da / "cat.json")
    chep = doc_json(da / "build" / "chep.json")
    doan = cat["doan"]
    k_td = g.toc_do or cat.get("toc_do", 1.0)
    if not 0.5 <= k_td <= 2.0:
        raise SystemExit("toc_do phải trong 0,5–2,0")
    if not doan:
        raise SystemExit("cat.json không có đoạn nào")

    clip_dung = sorted({d["clip"] for d in doan})
    vao = {cid: i for i, cid in enumerate(clip_dung)}
    lenh = ["ffmpeg", "-y", "-v", "error"]
    for cid in clip_dung:
        lenh += ["-i", da / next(c["file"] for c in so["clip"] if c["id"] == cid)]

    loc, noi = [], ""
    for k, d in enumerate(doan):
        a, b = lam_tron_khung(d["a"]), lam_tron_khung(d["b"])
        dai = b - a
        i = vao[d["clip"]]
        loc.append(f"[{i}:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{k}]")
        loc.append(f"[{i}:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,"
                   f"afade=t=in:d={NOI_TIENG},afade=t=out:st={dai - NOI_TIENG:.4f}:d={NOI_TIENG}[a{k}]")
        noi += f"[v{k}][a{k}]"
    loc.append(f"{noi}concat=n={len(doan)}:v=1:a=1[vg][ag]")
    if abs(k_td - 1) < 1e-6:
        loc.append("[vg]null[v]"); loc.append("[ag]anull[a]")
    else:  # tăng tốc SAU khi ghép: một hệ số cho cả bài → mọi mốc chỉ việc chia k, không trôi theo từng đoạn
        loc.append(f"[vg]setpts=PTS/{k_td},fps={FPS}[v]")
        loc.append(f"[ag]atempo={k_td}[a]")
    ra = da / "build" / "da-cat.mp4"
    if not g.chi_chu:
        print(f"cắt {len(doan)} đoạn · tốc độ ×{k_td} …")
        chay(lenh + ["-filter_complex", ";".join(loc), "-map", "[v]", "-map", "[a]", "-r", str(FPS),
                     "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-g", "15", "-pix_fmt", "yuv420p",
                     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", ra], "cắt ghép")

    # chữ theo dòng thời gian mới
    tu_clip = {c["id"]: [x for o in c["dao"] for x in o["tu"] if not (BO_TU & set(x["co"]))] for c in chep["clip"]}

    def chung(x, d):
        return min(x["e"], lam_tron_khung(d["b"])) - max(x["s"], lam_tron_khung(d["a"]))

    # mỗi chữ chỉ thuộc MỘT đoạn — đoạn chứa nó nhiều nhất (chữ nằm vắt hai đoạn liền nhau không bị in hai lần)
    chu_cua = {}
    for c_id, ds in tu_clip.items():
        for i, x in enumerate(ds):
            ung = [(chung(x, d), k) for k, d in enumerate(doan) if d["clip"] == c_id]
            if ung:
                chu_cua[(c_id, i)] = max(ung)[1]

    tu_moi, moc, bang, t = [], [], [], 0.0
    for k_d, d in enumerate(doan):
        a, b = lam_tron_khung(d["a"]), lam_tron_khung(d["b"])
        for i_x, x in enumerate(tu_clip[d["clip"]]):
            if chu_cua.get((d["clip"], i_x)) != k_d:
                continue
            tam = (x["s"] + x["e"]) / 2
            # chữ kéo dài (⌛) whisper gán khoảng rất rộng → tâm rơi ngoài đoạn dù tiếng vẫn còn ("dịch", "giống")
            if a <= tam <= b or chung(x, d) >= min(0.12, (x["e"] - x["s"]) * 0.5):
                tu_moi.append({"w": x["w"], "s": round((t + max(x["s"], a) - a) / k_td, 3),
                               "e": round((t + min(x["e"], b) - a) / k_td, 3),
                               "p": x["p"], "doan": d["id"]})
        bang.append(f"| {d['id']} | {mm_ss(t / k_td)}–{mm_ss((t + b - a) / k_td)} | {(b - a) / k_td:.1f}s "
                    f"| {d['clip']} {mm_ss(a)} | {d['chu']} |")
        t += b - a
        moc.append(round(t / k_td, 3))
    t /= k_td
    ghi_json(da / "build" / "tu-moi.json", tu_moi)
    ghi_json(da / "build" / "moc-cat.json", {"diem_cat": moc[:-1], "tong": round(t, 3), "toc_do": k_td,
                                             "doan": [{"id": d["id"], "het": m} for d, m in zip(doan, moc)]})
    (da / "build" / "ban-cat.md").write_text(
        f"# Bản cắt — dòng thời gian MỚI (tốc độ ×{k_td})\n\n| Đoạn | Thời gian mới | Dài | Lấy từ | Lời |\n|---|---|---|---|---|\n"
        + "\n".join(bang) + f"\n\nTổng: {t:.1f}s\n", "utf-8")
    thuc = do(ra)["giay"]
    print(f"✓ build/da-cat.mp4 {thuc:.2f}s (tính {t:.2f}s) · {len(tu_moi)} chữ · {len(moc) - 1} điểm cắt")
    if abs(thuc - t) > 0.1:
        print("⚠ độ dài thực lệch tính toán > 0,1 s — kiểm tra lại khớp tiếng/hình")


if __name__ == "__main__":
    main()

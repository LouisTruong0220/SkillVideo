# -*- coding: utf-8 -*-
"""B3b — Làm sạch bản cắt sau khi đã chọn đoạn trong cat.json: bỏ mọi khoảng lặng, chống lẹm chữ đầu đoạn, ghép,
nghe lại cả bản cắt. Chạy SAU khi sửa tay cat.json, TRƯỚC khi đưa anh Trường duyệt. ~1–2 phút cho video 1 phút.

    tools/video-tho/.venv/Scripts/python.exe tools/video-tho/lam-sach.py <du-an> [--toc-do 1.2]

Vì sao (video 012, 16/11/2026): bản cắt đầu bị anh Trường chê "còn ậm ừ, còn đoạn trống" dù bảng chép trông sạch —
  • gộp nhiều đảo thành một đoạn thì cat-ghep.py giữ nguyên lặng bên trong; đầu đoạn đề xuất còn dư 0,3–0,5 s lặng
  • đảo bắt đầu bằng `[…]` có thể là chữ thật (lẹm mất chữ "AI")

Làm gì:
  1. Mỗi đoạn trong cat.json: tìm các khúc có tiếng (RMS 10 ms của nghe-chep.py, làm mượt 50 ms, ngưỡng = nền + 9 dB,
     kẹp −42…−30 dB). Đầu đoạn đang có tiếng → lùi về đầu khúc tiếng (≤ 0,6 s). Khúc cách nhau ≥ --lang (0,28 s)
     → tách đoạn, mép −0,07 / +0,10 s. Đoạn có "giu": true thì để nguyên (mép đã chỉnh tay).
  2. Ghi cat.json (bản cũ: build/cat-truoc-lam-sach.json) → chạy cat-ghep.py. Độ dài thật lệch tính toán > 0,1 s
     (nhiều đoạn làm tròn khung) → nới đuôi đoạn cuối rồi ghép lại, để chữ cuối không bị xén.
  3. Nghe-chép lại cả build/da-cat.mp4 (1 lượt whisper) → build/nghe-lai.md: chữ mất / thừa so với lời các đoạn gốc,
     chữ lặp liền. ĐỌC FILE NÀY trước khi đưa duyệt. Whisper nghe nhầm tên riêng ("Layton" thay "lễ tân") là bình thường.

KHÔNG tự bắt được TIẾNG VẤP nửa chữ ("ư- ứng dụng", "n- nền tảng", "nh-", "m-"). Đã thử 17/11/2026 trên 4 chỗ vấp
thật của video 012: (a) tiếng dư sau chữ cuối của chỗ vấp 0,10–0,24 s — đuôi câu bình thường cũng dư 0,13–0,22 s
(whisper chấm hết chữ sớm), không tách được; (b) whisper nghe riêng đuôi: 9–14 s mỗi lượt trên CPU máy này và bịa
"Cảm ơn các bạn đã theo dõi" trên tiếng nửa chữ. → Chỗ vấp vẫn phải dò bằng tai ở chốt 1; cách đã làm được: chép
riêng hai mẩu hai bên khoảng nghi (luat-cat.md), rồi chỉnh tay mép `b` + đặt "giu": true cho đoạn đó.
"""
import argparse, difflib, shutil, subprocess, sys, time
import numpy as np
from chung import BUOC_RMS, CONG_CU, bo_dau, do, doc_json, du_an, ghi_json

SR = 16000
PA, PB = 0.07, 0.10          # mép đầu / đuôi quanh tiếng
LUI_TOI_DA = 0.6             # đầu đoạn đang có tiếng → lùi tối đa
AO_GIAC = ["cảm ơn các bạn đã theo dõi", "hẹn gặp lại", "subscribe", "đăng ký kênh", "ghiền mì gõ"]


def lam_muot(db):
    return np.convolve(db, np.ones(5) / 5, "same")


def khuc_tieng(db, nguong, a, b):
    """Các khúc có tiếng trong [a, b] (giây theo clip) → [[s, e], …], và số giây đã lùi đầu đoạn."""
    i0, i1 = int(a / BUOC_RMS), int(b / BUOC_RMS)
    co = db > nguong
    lui = 0.0
    if i0 < len(co) and co[i0]:
        j = i0
        while j > 0 and co[j - 1] and (i0 - j) * BUOC_RMS < LUI_TOI_DA:
            j -= 1
        lui = (i0 - j) * BUOC_RMS
        i0 = j
    ra, i = [], i0
    while i < min(i1, len(co)):
        if co[i]:
            j = i
            while j < min(i1, len(co)) and co[j]:
                j += 1
            if (j - i) * BUOC_RMS >= 0.05:
                ra.append([i * BUOC_RMS, j * BUOC_RMS])
            i = j
        else:
            i += 1
    return ra, lui


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("--toc-do", type=float, help="ghi toc_do vào cat.json (vd 1.2 — anh Trường thích nhịp nhanh)")
    ap.add_argument("--lang", type=float, default=0.28, help="khoảng lặng dài hơn mức này thì tách đoạn")
    ap.add_argument("--khong-nghe-lai", action="store_true")
    g = ap.parse_args()
    da = du_an(g.du_an)
    cat = doc_json(da / "cat.json")
    goc = [dict(d) for d in cat["doan"]]
    chep = {c["id"]: c for c in doc_json(da / "build" / "chep.json")["clip"]}
    shutil.copy2(da / "cat.json", da / "build" / "cat-truoc-lam-sach.json")
    db_cache, nhat_ky, moi = {}, [], []

    for d in cat["doan"]:
        c = d["clip"]
        if d.get("giu"):
            moi.append(d); continue
        if c not in db_cache:
            db_cache[c] = lam_muot(np.load(da / "build" / f"{c}.rms.npy"))
        nguong = float(np.clip(chep[c].get("nen_db", -47) + 9, -42, -30))
        runs, lui = khuc_tieng(db_cache[c], nguong, d["a"], d["b"])
        if not runs:
            nhat_ky.append(f"⚠ {d['id']}: không thấy tiếng trong {d['a']:.2f}–{d['b']:.2f}s — giữ nguyên"); moi.append(d); continue
        if lui > 0.02:
            nhat_ky.append(f"↶ {d['id']}: đầu đoạn cắt giữa tiếng → lùi {lui:.2f}s (chống lẹm chữ — nghe lại chỗ này)")
        gop = [runs[0][:]]
        for s, e in runs[1:]:
            if s - gop[-1][1] < g.lang:
                gop[-1][1] = e
            else:
                gop.append([s, e])
        tu = [w for o in chep[c]["dao"] for w in o["tu"]]
        for k, (s, e) in enumerate(gop):
            a2, b2 = max(0.0, s - PA), min(e + PB, d["b"] + 0.05)
            chu = " ".join(w["w"] for w in tu if a2 <= (w["s"] + w["e"]) / 2 <= b2 + 0.1)
            moi.append({"id": f"{d['id']}{chr(97 + k)}" if len(gop) > 1 else d["id"], "clip": c,
                        "a": round(a2, 3), "b": round(b2, 3), "chu": chu})
        if len(gop) > 1:
            nhat_ky.append(f"⧉ {d['id']}: tách {len(gop)} khúc, bỏ {len(gop) - 1} khoảng lặng ≥ {g.lang}s")

    cat["doan"] = moi
    if g.toc_do:
        cat["toc_do"] = g.toc_do
    ghi_json(da / "cat.json", cat)
    ghep(da)

    # độ dài thật lệch tính toán → nới đuôi đoạn cuối (chữ cuối khỏi bị xén)
    tong = doc_json(da / "build" / "moc-cat.json")["tong"]
    that = do(da / "build" / "da-cat.mp4")["giay"]
    if that - tong > 0.1:
        cuoi = cat["doan"][-1]
        cuoi["b"] = round(cuoi["b"] + (that - tong) * cat.get("toc_do", 1.0) + 0.02, 3)
        nhat_ky.append(f"⇥ {cuoi['id']}: bản ghép dài hơn tính toán {that - tong:.2f}s → nới đuôi đoạn cuối")
        ghi_json(da / "cat.json", cat)
        ghep(da)

    print("\n".join(nhat_ky) or "(không phải sửa gì)")
    print(f"✓ cat.json {len(moi)} đoạn (bản cũ: build/cat-truoc-lam-sach.json)")
    if not g.khong_nghe_lai:
        nghe_lai(da, goc)


def ghep(da):
    r = subprocess.run([sys.executable, str(CONG_CU / "cat-ghep.py"), str(da)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print("\n".join(l for l in r.stdout.splitlines() if l.startswith(("✓", "cắt"))))
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)


def nghe_lai(da, goc):
    from faster_whisper import WhisperModel
    t = time.time()
    mh = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", download_root=str(CONG_CU / "models"), cpu_threads=8)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(da / "build" / "da-cat.mp4"), "-ac", "1", "-ar", str(SR),
                          "-f", "s16le", "-"], capture_output=True).stdout
    am = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    doan, _ = mh.transcribe(am, language="vi", beam_size=5, vad_filter=False, condition_on_previous_text=False)
    cau = [s.text.strip() for s in doan if not any(x in bo_dau(s.text) for x in AO_GIAC)]
    nghe_w = bo_dau(" ".join(cau)).split()
    du_kien = bo_dau(" ".join(d.get("chu", "") for d in goc)).split()
    dong = ["# Nghe lại bản cắt (lam-sach.py)\n",
            "Whisper bỏ qua tiếng vấp nửa chữ — file này KHÔNG thay việc nghe bằng tai ở chốt 1.\n",
            "## Máy nghe được\n", " ".join(cau), "\n## Khác lời các đoạn gốc trong cat.json\n"]
    khac = 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=du_kien, b=nghe_w, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        khac += 1
        ctx = " ".join(du_kien[max(0, i1 - 3):i1])
        if op == "delete":
            dong.append(f"- **mất?** \"{' '.join(du_kien[i1:i2])}\" (sau \"…{ctx}\")")
        elif op == "insert":
            dong.append(f"- **thừa?** \"{' '.join(nghe_w[j1:j2])}\" (sau \"…{ctx}\")")
        else:
            dong.append(f"- **khác:** dự kiến \"{' '.join(du_kien[i1:i2])}\" ↔ nghe \"{' '.join(nghe_w[j1:j2])}\"")
    lap = [f"{nghe_w[i]} {nghe_w[i + 1]}" for i in range(len(nghe_w) - 1)
           if nghe_w[i] == nghe_w[i + 1] and nghe_w[i] not in ("từ", "dần", "rất", "nhiều", "đi")]
    dong.append("\n## Chữ lặp liền (nghi nói vấp còn sót, hoặc whisper nghe nhầm)\n")
    dong += [f"- \"{x}\"" for x in lap] or ["- không có"]
    (da / "build" / "nghe-lai.md").write_text("\n".join(dong) + "\n", "utf-8")
    print(f"nghe lại ({time.time() - t:.0f}s): {len(nghe_w)} chữ · {khac} chỗ khác lời dự kiến · {len(lap)} chỗ lặp liền"
          f" → build/nghe-lai.md (ĐỌC trước khi đưa duyệt)")


if __name__ == "__main__":
    main()

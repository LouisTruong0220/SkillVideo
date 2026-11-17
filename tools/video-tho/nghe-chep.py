# -*- coding: utf-8 -*-
"""B2 — Nghe-chép từng chữ + đánh dấu ậm ừ, câu nói lại, khoảng lặng.

    tools/video-tho/.venv/Scripts/python.exe tools/video-tho/nghe-chep.py <du-an> [--tu-khoa "Vũ Cẩm, Golden Gate"]

Cách làm (học từ ghost-editor, đã chỉnh cho tiếng Việt):
1. Silero VAD chia tiếng thành các "đảo tiếng nói" (ngắt ở khoảng lặng ≥ 0,3 s).
2. Whisper chép TỪNG ĐẢO RIÊNG. Chép cả file một lượt thì whisper gộp câu nói lại thành một câu sạch
   và nuốt mất các câu bỏ dở — đúng thứ mình cần thấy để cắt.
3. Whisper hay BỎ QUA tiếng ậm ừ. Nên ngoài từ điển ậm ừ ("ờ", "ừm"…), chỗ nào CÓ TIẾNG mà KHÔNG CÓ CHỮ
   (đo bằng năng lượng âm 10 ms) cũng bị đánh dấu "tiếng không thành chữ" — thường là ậm ừ, hít thở, chép miệng.
4. So các đảo với nhau để tìm câu nói lại: đảo trước giống đảo sau → đảo trước là bản hỏng, giữ bản sau.

Ra: build/chep.json (máy đọc) · build/ban-chep.md (người + Claude đọc để chọn đoạn) · build/<clip>.rms.npy
"""
import argparse, difflib, time
import numpy as np
import soundfile as sf
from chung import CONG_CU, bo_dau, doc_json, du_an, ghi_json, mm_ss

SR = 16000
BUOC = 0.01  # 10 ms một ô năng lượng

LOI_MOI = ("Ờ, ừm, à, ờm. Anh chị ạ. Robot phục vụ, robot lễ tân, robot vệ sinh, Roboworld, Duy Trường Robot, "
           "em Trường, BellaBot, BellaBot Pro, KettyBot Pro, PuduBot, FlashBot, PUDU, GreetingBot Nova, OrionStar, "
           "Gausium, nhà hàng, demo, AI.")

AM_U = {"ờ", "ơ", "ừ", "ừm", "ưm", "ờm", "ầm", "ừa", "ư", "hmm", "hm", "um", "uh", "ừ ừ", "ờ ờ", "ơ ơ", "ậm", "ơm", "ớ"}
AM_U_NGU_CANH = {"à", "á", "a"}  # chỉ là ậm ừ khi đứng đầu đảo hoặc có khoảng lặng hai bên ("vậy à?" thì không)
# Câu whisper hay "ảo giác" trên tiếng ồn/khoảng lặng tiếng Việt
AO_GIAC = ["subscribe", "ghiền mì gõ", "cảm ơn các bạn đã theo dõi", "hẹn gặp lại các bạn", "đăng ký kênh",
           "like và share", "video tiếp theo", "lalaschool", "chấm com"]


def nang_luong(am):
    n = int(SR * BUOC)
    k = len(am) // n
    o = am[: k * n].reshape(k, n)
    return (20 * np.log10(np.sqrt((o ** 2).mean(axis=1)) + 1e-9)).astype(np.float32)


def ti_le_co_tieng(db, nguong, a, b):
    i, j = int(a / BUOC), max(int(a / BUOC) + 1, int(b / BUOC))
    o = db[i:j]
    return float((o > nguong).mean()) if len(o) else 0.0


def la_am_u(tu, truoc_lang, sau_lang, dau_dao):
    n = bo_dau(tu)
    if n in AM_U:
        return True
    return n in AM_U_NGU_CANH and (dau_dao or (truoc_lang and sau_lang))


def vong_lap(doan):
    """Whisper kẹt vòng: một cụm 1–3 chữ lặp ≥ 4 lần liền."""
    w = bo_dau(" ".join(s.text for s in doan)).split()
    for n in (1, 2, 3):
        for i in range(len(w) - 4 * n + 1):
            if all(w[i:i + n] == w[i + k * n:i + (k + 1) * n] for k in range(1, 4)):
                return True
    return False


def chep_khoi(mh, am, ka, kb, loi_moi):
    """Chép một khối [ka, kb] → danh sách chữ có mốc thời gian theo clip. Kết quả bịa/kẹt vòng → chép lại
    kèm 3 s ngữ cảnh phía trước (rồi bỏ chữ thuộc phần ngữ cảnh), sau cùng thử bỏ lời mồi."""
    tong = len(am) / SR
    lan_thu = [(0.15, loi_moi), (3.0, loi_moi), (3.0, None)]
    for lui, moi in lan_thu:
        pa, pb = max(0.0, ka - lui), min(tong, kb + 0.15)
        # ĐỪNG đặt temperature=0: nó tắt cơ chế tự chép lại khi ra vòng lặp hoặc câu bịa.
        doan = list(mh.transcribe(am[int(pa * SR):int(pb * SR)], language="vi", word_timestamps=True, beam_size=5,
                                  condition_on_previous_text=False, vad_filter=False, initial_prompt=moi)[0])
        chu = bo_dau(" ".join(s.text for s in doan))
        if not (vong_lap(doan) or any(x in chu for x in AO_GIAC)):
            break
    tu = []
    for s in doan:
        for w in s.words or []:
            if w.word.strip() and pa + w.end > ka - 0.1:
                tu.append({"w": w.word.strip(), "s": round(pa + w.start, 3), "e": round(pa + w.end, 3),
                           "p": round(w.probability, 2), "xs_lang": round(s.no_speech_prob, 2),
                           "logp": round(s.avg_logprob, 2)})
    return tu


def tim_lap_lien(chu):
    """Cụm 2–4 chữ lặp ngay sau nó ('cái robot cái robot này') → vị trí bản đầu (bản hỏng)."""
    bo = set()
    for n in (4, 3, 2):
        for i in range(len(chu) - 2 * n + 1):
            if chu[i:i + n] == chu[i + n:i + 2 * n] and not bo.intersection(range(i, i + n)):
                bo.update(range(i, i + n))
    return bo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("--mo-hinh", default="large-v3-turbo")
    ap.add_argument("--tu-khoa", default="", help="tên riêng hay bị chép sai: tên nhà hàng, tên khách…")
    ap.add_argument("--lang-toi-thieu", type=float, default=0.3, help="khoảng lặng ngắt đảo (giây)")
    ap.add_argument("--gop-duoi", type=float, default=0.6, help="đảo cách nhau dưới mức này thì chép chung một khối")
    g = ap.parse_args()
    da = du_an(g.du_an)
    so = doc_json(da / "du-an.json")

    from faster_whisper import WhisperModel
    from faster_whisper.vad import VadOptions, get_speech_timestamps
    t0 = time.time()
    mh = WhisperModel(g.mo_hinh, device="cpu", compute_type="int8", download_root=str(CONG_CU / "models"), cpu_threads=8)
    loi_moi = LOI_MOI + (" " + g.tu_khoa if g.tu_khoa else "")
    print(f"nạp mô hình {g.mo_hinh}: {time.time() - t0:.0f}s")

    ket_qua = {"mo_hinh": g.mo_hinh, "tu_khoa": g.tu_khoa, "clip": []}
    for c in so["clip"]:
        am, sr = sf.read(da / "build" / f"{c['id']}.a16.wav", dtype="float32")
        assert sr == SR
        db = nang_luong(am)
        np.save(da / "build" / f"{c['id']}.rms.npy", db)
        nen = float(np.percentile(db, 10))
        nguong = max(nen + 12, -48.0)

        vung = get_speech_timestamps(am, VadOptions(threshold=0.45, min_silence_duration_ms=int(g.lang_toi_thieu * 1000),
                                                    speech_pad_ms=80, min_speech_duration_ms=120))
        dao_vung = [(v["start"] / SR, v["end"] / SR) for v in vung]
        # Gộp đảo cách nhau < 0,6 s thành KHỐI để chép. Đảo bị VAD cắt giữa câu (ngắt hơi 0,2 s) mà chép riêng
        # thì whisper bịa câu ("subscribe kênh Ghiền Mì Gõ" — dính thật 15/11/2026). Người ta dừng lâu hơn 0,6 s
        # trước khi nói lại một câu, nên khối vẫn tách được bản hỏng với bản nói lại.
        khoi = []
        for a, b in dao_vung:
            if khoi and a - khoi[-1][1] < g.gop_duoi and b - khoi[-1][0] < 28:
                khoi[-1][1] = b
            else:
                khoi.append([a, b])
        t1 = time.time()
        moi_tu = []
        for ka, kb in khoi:
            moi_tu += chep_khoi(mh, am, ka, kb, loi_moi)

        # mỗi chữ về đúng MỘT đảo — đảo gần tâm chữ nhất (khe giữa hai đảo sát nhau không bị đếm đôi)
        thuoc = {}
        for x in moi_tu:
            tam = (x["s"] + x["e"]) / 2
            kc = [max(a - tam, tam - b, 0) for a, b in dao_vung]
            i = int(np.argmin(kc))
            if kc[i] <= 0.5:
                thuoc.setdefault(i, []).append(x)
        dao_list = []
        for k, (a, b) in enumerate(dao_vung, 1):
            tu = [dict(x, co=[]) for x in thuoc.get(k - 1, [])]
            dao = {"id": f"{c['id']}-{k:02d}", "clip": c["id"], "a": round(a, 3), "b": round(b, 3), "tu": tu, "co": [],
                   "lang_xs": max([x["xs_lang"] for x in tu] or [0]), "logp": min([x["logp"] for x in tu] or [0])}
            for x in tu:
                x.pop("xs_lang"); x.pop("logp")
            chu_dao = " ".join(x["w"] for x in tu)
            dao["chu"] = chu_dao
            nd = bo_dau(chu_dao)
            if not tu:
                dao["co"].append("khong-chu")
            if any(x in nd for x in AO_GIAC) or (len(nd) > 20 and nd in bo_dau(loi_moi)):
                dao["co"].append("ao-giac")
            if tu and dao["lang_xs"] > 0.6 and dao["logp"] < -0.9:
                dao["co"].append("nghi-ngo")

            # ậm ừ theo từ điển + chữ kéo dài
            for i, x in enumerate(tu):
                truoc = x["s"] - (tu[i - 1]["e"] if i else a) >= 0.2
                sau = (tu[i + 1]["s"] if i + 1 < len(tu) else b) - x["e"] >= 0.2
                if la_am_u(x["w"], truoc, sau, i == 0):
                    x["co"].append("am-u")
                if x["e"] - x["s"] > 0.9 and i + 1 < len(tu):
                    x["co"].append("keo-dai")
            # lặp liền trong một đảo
            for i in tim_lap_lien([bo_dau(x["w"]) for x in tu]):
                tu[i]["co"].append("lap")
            # tiếng không thành chữ: khe giữa hai chữ (và hai mép đảo) có tiếng mà whisper không chép
            moc = [a] + [m for x in tu for m in (x["s"], x["e"])] + [b]
            khe = []
            for i in range(0, len(moc) - 1, 2):
                ka, kb = moc[i], moc[i + 1]
                if kb - ka >= 0.25 and ti_le_co_tieng(db, nguong, ka + 0.03, kb - 0.03) >= 0.4:
                    khe.append({"s": round(ka, 3), "e": round(kb, 3)})
            dao["tieng_khong_chu"] = khe
            dao_list.append(dao)

        # câu nói lại giữa các đảo: đảo trước giống/đứt giữa chừng so với một đảo ngay sau → bản hỏng
        for i, d in enumerate(dao_list):
            A = [bo_dau(x["w"]) for x in d["tu"] if "am-u" not in x["co"]]
            if len(A) < 2 or "ao-giac" in d["co"]:
                continue
            for j in range(i + 1, min(i + 7, len(dao_list))):
                B = [bo_dau(x["w"]) for x in dao_list[j]["tu"] if "am-u" not in x["co"]]
                if len(B) < 2:
                    continue
                chung_dau = 0
                while chung_dau < min(len(A), len(B)) and A[chung_dau] == B[chung_dau]:
                    chung_dau += 1
                ti_le = difflib.SequenceMatcher(None, A, B[:len(A) + 3]).ratio()
                if chung_dau >= 3 or (chung_dau >= 2 and len(A) <= 4) or ti_le >= 0.6:
                    d["co"].append("noi-lai"); d["noi_lai_boi"] = dao_list[j]["id"]
                    break
                # đuôi đảo trước = đầu đảo sau (nói tiếp rồi vấp, nói lại nửa sau)
                for k in range(1, len(A) - 2):
                    duoi = A[k:]
                    if len(duoi) >= 3 and difflib.SequenceMatcher(None, duoi, B[:len(duoi)]).ratio() >= 0.75:
                        song = [x for x in d["tu"] if "am-u" not in x["co"]]
                        for x in song[k:]:
                            x["co"].append("noi-lai-duoi")
                        d["co"].append("noi-lai-duoi"); d["noi_lai_boi"] = dao_list[j]["id"]
                        break
                if "noi-lai-duoi" in d["co"]:
                    break

        tong_noi = sum(d["b"] - d["a"] for d in dao_list)
        print(f"{c['id']}: {len(dao_list)} đảo, {tong_noi:.1f}s có tiếng / {c['giay']:.1f}s, chép mất {time.time() - t1:.0f}s")
        ket_qua["clip"].append({"id": c["id"], "giay": c["giay"], "nen_db": round(nen, 1), "nguong_db": round(nguong, 1),
                                "dao": dao_list})

    ghi_json(da / "build" / "chep.json", ket_qua)
    viet_ban_chep(da, ket_qua)
    print(f"✓ build/chep.json + build/ban-chep.md\n  Bước tiếp: python tools/video-tho/de-xuat-cat.py {da.name}")


def viet_ban_chep(da, kq):
    d = ["# Bản chép video thô", "",
         "Ký hiệu: ~~gạch~~ = máy đề xuất CẮT (ậm ừ / lặp / nói lại) · `[…]` = có tiếng nhưng không thành chữ "
         "(thường là ậm ừ) · ⟲ = câu này được nói lại ở đảo sau · ⚠ = nghi ảo giác / không chắc · "
         "_nghiêng_ = whisper không chắc chữ này (p<0,5) · ⌛ = chữ kéo dài bất thường", ""]
    for c in kq["clip"]:
        d += [f"## {c['id']} — {c['giay']:.1f}s · nền ồn {c['nen_db']} dB", "",
              "| Đảo | Thời gian (clip) | Dài | Lời nói | Ghi chú |", "|---|---|---|---|---|"]
        for o in c["dao"]:
            khe = list(o["tieng_khong_chu"])
            phan = []
            for x in o["tu"]:
                while khe and khe[0]["e"] <= x["s"] + 0.01:
                    phan.append("`[…]`"); khe.pop(0)
                w = x["w"]
                if x["p"] < 0.5:
                    w = f"_{w}_"
                if "keo-dai" in x["co"]:
                    w += "⌛"
                if {"am-u", "lap", "noi-lai-duoi"} & set(x["co"]):
                    w = f"~~{w}~~"
                phan.append(w)
            phan += ["`[…]`"] * len(khe)
            ghi = []
            if "noi-lai" in o["co"]:
                ghi.append(f"⟲ nói lại ở {o['noi_lai_boi']}")
            if "noi-lai-duoi" in o["co"]:
                ghi.append(f"⟲ nửa sau nói lại ở {o['noi_lai_boi']}")
            if {"ao-giac", "nghi-ngo"} & set(o["co"]):
                ghi.append("⚠ " + ", ".join(sorted({"ao-giac", "nghi-ngo"} & set(o["co"]))))
            if "khong-chu" in o["co"]:
                ghi.append("không chép được chữ nào")
            d.append(f"| {o['id']} | {mm_ss(o['a'])}–{mm_ss(o['b'])} | {o['b'] - o['a']:.1f}s | "
                     f"{' '.join(phan) or '—'} | {'; '.join(ghi)} |")
        d.append("")
    (da / "build" / "ban-chep.md").write_text("\n".join(d), "utf-8")


if __name__ == "__main__":
    main()

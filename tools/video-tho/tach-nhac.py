# -*- coding: utf-8 -*-
"""Tách NHẠC NỀN khỏi video có người nói (Demucs htdemucs, chạy CPU) → kho nhạc nền.

    tools/video-tho/.venv/Scripts/python.exe tools/video-tho/tach-nhac.py <video1> [video2 ...] [--ra <thu-muc>]

Mặc định ghi vào 02-media/am-thanh/nhac-nen-video-mau/<ten-video>.mp3 (+ <ten>.giong.wav là giọng đã tách, để soát).
Anh Trường chốt 15/11/2026: nhạc nền video thô lấy từ các video mẫu của anh, KHÔNG dùng nhạc của video đã dựng.

⚠ Nhạc tách ra còn kèm hiệu ứng âm thanh đã trộn trong video gốc (whoosh, pop…) và vết giọng mờ.
   Đoạn nào nghe rõ hiệu ứng/giọng thì cắt bỏ khi dùng (xem muc-luc.json → "doan_sach").
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
import soundfile as sf
import torch
from chung import KHO_AM, chay

sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", nargs="+")
    ap.add_argument("--ra", default=str(KHO_AM / "nhac-nen-video-mau"))
    g = ap.parse_args()
    ra = Path(g.ra); ra.mkdir(parents=True, exist_ok=True)

    from demucs.pretrained import get_model
    from demucs.apply import apply_model
    mh = get_model("htdemucs"); mh.eval()
    torch.set_num_threads(8)
    ml_p = ra / "muc-luc.json"
    ml = json.loads(ml_p.read_text("utf-8")) if ml_p.exists() else {"nhac": []}

    for v in g.video:
        v = Path(v)
        ten = v.stem
        with tempfile.TemporaryDirectory() as td:
            wav = Path(td) / "a.wav"
            chay(["ffmpeg", "-y", "-v", "error", "-i", v, "-vn", "-ac", "2", "-ar", str(mh.samplerate), wav], "tách tiếng")
            am, sr = sf.read(wav, dtype="float32", always_2d=True)
        x = torch.from_numpy(am.T.copy())
        tb, lc = x.mean(), x.std() + 1e-8
        with torch.no_grad():
            nguon = apply_model(mh, ((x - tb) / lc)[None], device="cpu", split=True, overlap=0.25, progress=False)[0]
        nguon = nguon * lc + tb
        i_giong = mh.sources.index("vocals")
        nhac = sum(nguon[i] for i in range(len(mh.sources)) if i != i_giong).numpy().T
        sf.write(ra / f"{ten}.giong.wav", nguon[i_giong].numpy().T, sr)
        tam = ra / f"{ten}.tam.wav"
        sf.write(tam, nhac, sr)
        chay(["ffmpeg", "-y", "-v", "error", "-i", tam, "-c:a", "libmp3lame", "-b:a", "192k", ra / f"{ten}.mp3"], "mp3")
        tam.unlink()
        # mức nhạc so với giọng trong video gốc — để biết anh Trường hay để nhạc to/nhỏ cỡ nào
        db = lambda a: float(20 * np.log10(np.sqrt((a ** 2).mean()) + 1e-9))
        muc = round(db(nhac) - db(nguon[i_giong].numpy().T), 1)
        ml["nhac"] = [n for n in ml["nhac"] if n["file"] != f"{ten}.mp3"]
        ml["nhac"].append({"file": f"{ten}.mp3", "tu_video": str(v), "giay": round(len(nhac) / sr, 1),
                           "nhac_so_voi_giong_db": muc, "doan_sach": None, "ghi_chu": ""})
        print(f"✓ {ten}.mp3  {len(nhac) / sr:.0f}s · nhạc thấp hơn giọng {-muc:.1f} dB")
    ml["nhac"].sort(key=lambda n: n["file"])
    ml_p.write_text(json.dumps(ml, ensure_ascii=False, indent=2), "utf-8")


if __name__ == "__main__":
    main()

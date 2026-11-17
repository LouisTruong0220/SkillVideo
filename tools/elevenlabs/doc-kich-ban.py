# -*- coding: utf-8 -*-
"""
Sinh giọng đọc tiếng Việt cho video, xuất MP3 vào 05-output/voice/.

Cách dùng:
    python doc-kich-ban.py "Xin chao, day la BellaBot Pro." ten-file
    python doc-kich-ban.py --file kich-ban.txt ten-file
    python doc-kich-ban.py --file kich-ban.txt ten-file --toc-do 1.1

Tuỳ chọn:
    --giong <voice_id>   dùng giọng khác thay vì giọng trong .env
    --toc-do 0.7..1.2    tốc độ đọc (mặc định 1.0)
    --on-dinh 0..1       stability: thấp = biểu cảm hơn, cao = đều hơn (mặc định 0.45)
"""
import argparse
import os
import re
import sys

import rbw_voice as rv

OUT_DIR = os.path.join(rv.ROOT, "05-output", "voice")


def canh_bao_so(text):
    """Model đọc số theo kiểu Anh -> nhắc viết chữ cho đúng tiếng Việt."""
    hits = re.findall(r"\d[\d.,]{2,}", text)
    if hits:
        print("\n  CANH BAO: kich ban co so viet bang chu so:")
        for h in sorted(set(hits))[:6]:
            print(f"     {h}")
        print("  -> Nen viet thanh chu (vd '155.000.000' -> 'mot tram nam muoi lam trieu')")
        print("     de doc dung tieng Viet.\n")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("text", nargs="?", help="Lời thoại (hoặc dùng --file)")
    ap.add_argument("ten_file", help="Tên file xuất, không cần đuôi")
    ap.add_argument("--file", dest="path", help="Đọc lời thoại từ file .txt/.md")
    ap.add_argument("--giong", dest="voice_id")
    ap.add_argument("--model", dest="model",
                    help="eleven_v3 (mặc định) / eleven_turbo_v2_5 / eleven_flash_v2_5")
    ap.add_argument("--toc-do", dest="speed", type=float, default=1.0)
    ap.add_argument("--on-dinh", dest="stability", type=float, default=0.45)
    ap.add_argument("--giong-giong", dest="similarity", type=float, default=0.9,
                    help="similarity_boost 0..1 — cao = bám sát giọng gốc hơn")
    a = ap.parse_args()

    if a.path:
        with open(a.path, encoding="utf-8") as fh:
            text = fh.read().strip()
    elif a.text:
        text = a.text.strip()
    else:
        sys.exit("Can truyen loi thoai hoac --file")

    if not text:
        sys.exit("Loi thoai rong")

    canh_bao_so(text)

    env = rv.load_env()
    out = os.path.join(OUT_DIR, a.ten_file.removesuffix(".mp3") + ".mp3")

    print(f"  Do dai kich ban : {len(text):,} ky tu")
    print(f"  Model           : {a.model or env.get('ELEVENLABS_MODEL', 'eleven_v3')}")
    print(f"  Dang sinh giong ...")
    rv.tts(env, text, out, voice_id=a.voice_id, model=a.model,
           stability=a.stability, similarity=a.similarity, speed=a.speed)

    kb = os.path.getsize(out) / 1024
    print(f"\n  XONG: {out}  ({kb:,.0f} KB)")
    print(f"  Ghep vao video:")
    print(f'     ffmpeg -i video.mp4 -i "{out}" -c:v copy -map 0:v -map 1:a -shortest ket-qua.mp4')


if __name__ == "__main__":
    main()

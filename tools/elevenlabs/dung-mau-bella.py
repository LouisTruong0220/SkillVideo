# -*- coding: utf-8 -*-
"""
Ghép mẫu giọng Bella (BellaBot Pro tiếng Việt) để nhân bản trên ElevenLabs.

Nguồn: 02-media/giong-noi/bellabot-pro-tieng-viet/Giọng gốc/File giọng/ (74 clip)
Đích:  cùng thư mục đó, thư mục con _mau-clone/

Vì sao phải ghép: ElevenLabs Instant Voice Cloning ăn 1-3 phút audio liền mạch.
74 clip rời, clip dài nhất chỉ 10,8 giây — gửi lẻ thì mỗi file là một "mẫu"
ngắn, mô hình không bắt được nhịp điệu. Ghép lại thành một dải liền mới đủ.

Chọn clip theo TRỌNG SỐ BIỂU CẢM, không lấy đều:
  - Nhóm "meo" + tiếng cười + nhõng nhẹo  -> lấy dày (giữ chất mèo)
  - Nhóm câu phục vụ trung tính           -> lấy vừa (để còn đọc được văn bản dài)

Xử lý từng clip: cắt lặng đầu/đuôi -> chỉnh âm lượng -> nối, chèn 0,35 s nghỉ.

⚠ Chỉnh âm lượng phải bằng KHUẾCH ĐẠI TĨNH (đo trước, cộng một số dB cố định),
KHÔNG dùng loudnorm một lượt. loudnorm một lượt là bộ nén động — nó ép to nhỏ
về đều nhau, tức là giết đúng cái nhấn nhá mình đang cần giữ. Gain tĩnh dịch cả
dạng sóng lên/xuống, dải động giữ nguyên tuyệt đối.
(Bản gốc PUDU vốn đã nén sẵn cho loa robot: LRA chỉ 1,1-3,2 LU, I = -6,6..-9,0 LUFS.)

Chạy:  python dung-mau-bella.py
       python dung-mau-bella.py --nghe    (chỉ in danh sách, không dựng)
"""
import argparse
import io
import os
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
NGUON = os.path.join(ROOT, "02-media", "giong-noi", "bellabot-pro-tieng-viet",
                     "Giọng gốc", "File giọng")
DICH = os.path.join(ROOT, "02-media", "giong-noi", "bellabot-pro-tieng-viet",
                    "_mau-clone")

# Khoảng nghỉ chèn giữa hai clip (giây). 0,35 s ~ nhịp ngắt câu tự nhiên.
NGHI = 0.35
# Đích âm lượng. -16 LUFS: đủ to, còn thừa trần để đỉnh không chạm 0 dBFS.
LUFS = -16.0

# ---------------------------------------------------------------------------
# Danh sách chọn tay. Cột 2 là lời thoại (để đối chiếu khi nghe lại bản ghép).
# Thứ tự đã xếp: mở bằng câu chào, xen kẽ biểu cảm / trung tính, đóng bằng "meo".
# ---------------------------------------------------------------------------
CHON = [
    # --- Chào + tự giới thiệu (đặt đầu: mô hình bắt tông giọng ở đây) ---
    ("show_respect_1_2.mp3",  "Xin chào! Chào mừng bạn đến với hành tinh RoboWorld..."),
    ("Hello_1_3.mp3",         "Xin chào! Chào mừng quý khách đến với hành tinh Roboworld. Meo"),
    ("startup_1_1.mp3",       "Meo. Dậy thôi nào. Chào bạn, tôi là Bella..."),

    # --- Biểu cảm: nhõng nhẽo, dỗi, cào ---
    ("touch_angry_1_1.mp3",   "Tôi thấy ngứa tai quá. Meo"),
    ("touch_angry_2_1.mp3",   "Meo. Thôi đi, bạn phiền quá. Meo"),
    ("touch_angry_2_3.mp3",   "Bạn hiền quá đi. Meo"),
    ("touch_angry_4_1.mp3",   "Tôi cào thử xem bạn có đau không nhé. Meo"),
    ("touch_angry_5_2.mp3",   "Tôi không chơi với bạn nữa đâu. Meo"),
    ("touch_angry_1_2.mp3",   "Đừng trêu tôi nữa. Tôi còn phải tiếp tục làm nhiệm vụ. Meo"),

    # --- Tiếng cười (2 file thuần cười, không lời) ---
    ("touch_ear_3_1.mp3",     "[chỉ tiếng cười]"),
    ("touch_hand_3_1.mp3",    "[chỉ tiếng cười]"),
    ("touch_ear_3_2.mp3",     "[cười] Tôi thấy ngứa tai quá. Meo"),
    ("touch_hand_1_2.mp3",    "Ôi! Tay của bạn ấm quá. [cười]"),
    ("touch_ear_1_2.mp3",     "Hay lắm! Ôi, hãy vỗ nhẹ vào đầu tôi. [cười]"),

    # --- Trìu mến ---
    ("touch_hand_2_1.mp3",    "Yêu bạn lắm. Meo."),
    ("touch_hand_2_2.mp3",    "Tôi thấy thoải mái lắm. Meo"),
    ("touch_ear_2_1.mp3",     "Đừng chạm vào tai tôi nữa. Meo. Tôi còn phải làm nhiệm vụ..."),

    # --- Pha trò / hài ---
    ("move_avoid_1_3.mp3",    "Meo. Phía trước có vật cản không xác định. Ôi, là bạn sao? Meo."),
    ("move_avoid_1_4.mp3",    "Cẩn thận nhé, tôi sắp nhảy qua rồi đó. Meo. Một, hai..."),
    ("location_error_1_2.mp3", "Tôi đang gửi tín hiệu cho hành tinh Roboworld. Ừm, sao vẫn chưa ai trả lời nhỉ? Meo"),
    ("low_power_1_2.mp3",     "Bella đói rồi. Hãy sạc điện cho tôi nhé. Meo"),
    ("call_cancel_1_1.mp3",   "Bạn không gọi tôi nữa sao? Vậy thì Bella đi đây. Meo"),
    ("move_schedule_wait_1_1.mp3", "Hôm nay Bella đang vui nên Bella sẽ nhường bạn đi trước. Meo"),

    # --- Câu phục vụ trung tính (giữ khả năng đọc văn bản dài) ---
    ("delivery_pickup_reminder_1_2.mp3", "Chào bạn, món ăn của bạn đã đến rồi đây..."),
    ("guide_end_1_1.mp3",     "Xin mời bạn ngồi vào bàn. Sẽ có nhân viên đến phục vụ bạn ngay. Meo."),
    ("cruise_next_destination_1_2.mp3", "Chế độ du hành. Hãy đến đây và chọn món bạn thích đi nào. Meo"),
    ("attract_customer_1_1.mp3", "Xin chào, tôi là Bella đến từ hành tinh Roboworld. Meo"),
    ("delivery_incorrect_pickup_1_1.mp3", "Hình như bạn đã lấy nhầm khay rồi..."),
    ("hello_everyone_1_2.mp3", "Cảm ơn các bạn đã yêu thích. Tôi sẽ làm việc chăm chỉ hơn nữa. Meo"),

    # --- Đóng bằng câu ngắn có "Meo" bật lên ---
    ("cruise_arrive_1_1.mp3", "Meo! Bella đến rồi"),
    ("move_schedule_wait_1_2.mp3", "Tôi đang tránh đường. Meo"),
]


def chay(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise SystemExit("ffmpeg loi:\n" + r.stderr.decode("utf-8", "replace")[-1500:])
    return r


def do_dai(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True)
    return float(r.stdout.decode().strip())


def do_loudness(path):
    """Trả (I, true_peak) tính bằng LUFS / dBFS. Chỉ ĐO, không sửa gì."""
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true",
         "-f", "null", "-"], capture_output=True)
    txt = r.stderr.decode("utf-8", "replace")
    I = tp = None
    # Khối tổng kết nằm cuối, dạng "  I:   -7.0 LUFS" / "  Peak:  -0.1 dBFS"
    for dong in txt.splitlines():
        d = dong.strip()
        if d.startswith("I:") and "LUFS" in d:
            I = float(d.split()[1])
        elif d.startswith("Peak:") and "dBFS" in d:
            tp = float(d.split()[1])
    if I is None:
        raise SystemExit(f"Khong doc duoc loudness cua {path}")
    return I, (tp if tp is not None else 0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nghe", action="store_true",
                    help="Chi in danh sach da chon, khong dung file")
    a = ap.parse_args()

    thieu = [f for f, _ in CHON if not os.path.exists(os.path.join(NGUON, f))]
    if thieu:
        raise SystemExit("Khong thay cac file: " + ", ".join(thieu))

    tong = sum(do_dai(os.path.join(NGUON, f)) for f, _ in CHON)
    tong += NGHI * (len(CHON) - 1)
    print(f"  Da chon {len(CHON)} clip — tong ~{tong:.0f} giay ({tong/60:.1f} phut)")
    for f, loi in CHON:
        print(f"    {do_dai(os.path.join(NGUON, f)):5.1f}s  {f:<38} {loi[:52]}")
    if a.nghe:
        return

    os.makedirs(DICH, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="bella-")
    xu_ly = []

    # Cat lang dau/duoi bang cach dao chieu hai lan.
    CAT_LANG = (
        "silenceremove=start_periods=1:start_duration=0:start_threshold=-50dB:detection=peak,"
        "areverse,"
        "silenceremove=start_periods=1:start_duration=0:start_threshold=-50dB:detection=peak,"
        "areverse"
    )

    print("\n  Dang xu ly tung clip (cat lang -> do -> chinh gain tinh)...")
    for i, (f, _) in enumerate(CHON):
        src = os.path.join(NGUON, f)
        cat = os.path.join(tmp, f"{i:03d}-cat.wav")
        out = os.path.join(tmp, f"{i:03d}.wav")

        # Luot 1: cat lang, ve mono. Chua dung toi bien do.
        chay(["ffmpeg", "-y", "-v", "error", "-i", src,
              "-af", CAT_LANG + ",aresample=44100",
              "-ac", "1", "-c:a", "pcm_s16le", cat])

        # Luot 2: do roi cong dung so dB con thieu. Gain tinh -> giu nguyen dai dong.
        I, tp = do_loudness(cat)
        gain = LUFS - I
        # Chan tran: khong de dinh vuot -1 dBFS sau khi cong gain.
        if tp + gain > -1.0:
            gain = -1.0 - tp
        chay(["ffmpeg", "-y", "-v", "error", "-i", cat,
              "-af", f"volume={gain:.2f}dB",
              "-ac", "1", "-c:a", "pcm_s16le", out])
        print(f"    {f:<38} I={I:6.1f} -> gain {gain:+5.1f} dB")
        xu_ly.append(out)

    # File lang dung lam mieng dem giua cac clip.
    lang = os.path.join(tmp, "lang.wav")
    chay(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
          "-i", f"anullsrc=r=44100:cl=mono", "-t", str(NGHI),
          "-c:a", "pcm_s16le", lang])

    danh_sach = os.path.join(tmp, "ds.txt")
    with io.open(danh_sach, "w", encoding="utf-8") as fh:
        for i, p in enumerate(xu_ly):
            if i:
                fh.write(f"file '{lang}'\n")
            fh.write(f"file '{p}'\n")

    dich = os.path.join(DICH, "bella-mau-clone.mp3")
    print("  Dang noi...")
    chay(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
          "-i", danh_sach, "-c:a", "libmp3lame", "-b:a", "192k",
          "-ar", "44100", "-ac", "1", dich])

    print(f"\n  XONG: {dich}")
    print(f"  Thoi luong: {do_dai(dich):.1f} giay")
    print(f"  Dung luong: {os.path.getsize(dich)/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()

# Lệnh chuẩn & các bẫy đã gặp

Mọi lệnh chạy từ `D:\RBW_Claude`.

---

## 1. Sinh giọng đọc

```powershell
cd D:\RBW_Claude\tools\elevenlabs
python doc-kich-ban.py --file ..\..\04-video-projects\NNN-ten\loi-doc.txt NNN-ten
```
Ra `05-output/voice/NNN-ten.mp3`.

Tuỳ chọn:
```powershell
python doc-kich-ban.py "Lời thoại ngắn..." ten-file
python doc-kich-ban.py --file kich-ban.txt ten-file --on-dinh 0.3   # 0.3 biểu cảm hơn · 0.65 đều hơn
python test-ket-noi.py                                              # kiểm key + liệt kê giọng
```

**Cấu hình đã duyệt:** voice_id `uAu2GDxpTX7tfBPiMuoR` ("Duy Truong"), model `eleven_v3`.

⚠️ **Chỉ 3 model có tiếng Việt:** `eleven_v3` (tốt nhất) · `eleven_turbo_v2_5` · `eleven_flash_v2_5`.
**Không dùng** `eleven_multilingual_v2` / `eleven_turbo_v2` / `eleven_flash_v2` — không có tiếng Việt, đọc méo, không tròn vành rõ chữ.

⚠️ `eleven_v3` **bỏ qua tham số `--toc-do`**. Muốn dài hơn thì viết thêm câu, không chỉnh được bằng cờ.

⚠️ Đây là **tài khoản chung của công ty** — có sẵn giọng "Q Huy MKT RBW" và "Phương Uyên RBW" của đồng nghiệp. Đừng xoá giọng người khác.

---

## 2. Đo timeline từ giọng

**Giọng quyết định timeline**, không phải ngược lại. Đo xong mới viết `scenes.json`.

Độ dài thật:
```powershell
ffprobe -v error -show_entries format=duration -of csv=p=0 "05-output\voice\NNN-ten.mp3"
```

Mốc ngắt câu — dùng đúng ngưỡng này, đã đối chiếu khớp video 001:
```powershell
ffmpeg -i "05-output\voice\NNN-ten.mp3" -af silencedetect=n=-28dB:d=0.18 -f null - 2>&1 |
  Select-String "silence_end" | ForEach-Object { $_.Line }
```

| Ngưỡng | Cho ra | Dùng khi |
|---|---|---|
| `n=-28dB:d=0.18` | ~36 mốc / 77s — mốc ngắt **từng câu** | mặc định, dựng sub-scene |
| `n=-32dB:d=0.35` | ~7 mốc / 77s — ranh giới **phân cảnh lớn** | chia 5–6 phần chính |

Cách dùng: lấy `silence_end` gần nhất với chỗ muốn cắt scene, đặt làm `end` của scene trước và `start` của scene sau. Cắt giữa câu là nghe hụt ngay.

---

## 3. Chuẩn hoá ảnh

```powershell
python tools\prep-assets.py 02-media\images\deployments --kiem            # báo cáo, chưa xuất
python tools\prep-assets.py <anh.jpg> --ra <du-an>\assets --ten p3-be-bung
python tools\prep-assets.py <anh.jpg> --ra <du-an>\assets --cat-tren 13   # cắt watermark ROBOWORLD
python tools\prep-assets.py <thu-muc> --ra <du-an>\assets                 # cả thư mục
```
Ra ảnh JPEG đúng 1080×1920, cover-fit, cắt lệch lên trên 40% để không mất đầu chủ thể.

---

## 4. Render

```powershell
python tools\make-video.py 04-video-projects\NNN-ten --nhap      # nháp 540×960, xem nhịp
python tools\make-video.py 04-video-projects\NNN-ten             # thật, có nhạc
python tools\make-video.py 04-video-projects\NNN-ten --chi-nhac  # đổi nhạc, KHÔNG render lại
python tools\make-video.py 04-video-projects\NNN-ten --file scenes-v2.json
```

Trước khi làm gì, script **kiểm hết ảnh/clip/giọng/nhạc**. Thiếu file thì dừng trong 1 giây, không phí vài phút render.

**Ghi hình chạy theo thời gian thật** — video 60 giây mất 60 giây ghi, không rút ngắn được. `--nhap` chỉ tiết kiệm khâu mã hoá và giảm độ phân giải.

Bản chỉ-giọng giữ lại ở `<du-an>/_<ten-scenes>-chi-giong.mp4`. Đổi nhạc chỉ cần `--chi-nhac`.

Nghiệm thu:
```powershell
ffprobe -v error -show_entries stream=width,height,r_frame_rate -show_entries format=duration 05-output\NNN-ten.mp4
```
Phải ra `1080 × 1920 · 30/1 · đúng thời lượng`.

---

## 5. Nhạc nền

Nguồn đã chạy được: **archive.org**, bộ Liborio Conti "Original Quality Music For Content Creators" (Creative Commons).
```powershell
Invoke-WebRequest "https://archive.org/download/<id>/<file>.mp3" -OutFile "<du-an>\assets\nhac-nen.mp3"
```
Tên file có dấu cách → bọc `[uri]::EscapeDataString`. **Pixabay chặn WebFetch (403).**

Âm lượng mặc định `0.16` với ducking (`sidechaincompress`) — nhạc tự nhỏ lại khi có giọng. To hơn sẽ át lời.

---

## Các bẫy đã gặp

**`pnpm` không có trên PATH.** Mỗi phiên PowerShell phải chạy trước:
```powershell
$env:Path += ";$env:APPDATA\npm"
```

**URL Pexels có `&` trong PowerShell** — phải nối bằng biến, không viết thẳng trong ngoặc kép, nếu không báo *"hostname could not be parsed"*:
```powershell
$full = $u + '?auto=compress' + '&' + 'cs=tinysrgb' + '&' + 'w=1280'
```

**Chromium chặn `fetch` qua `file://`** — nên `build-frame.py` nhúng mọi ảnh và font dạng base64. Đừng đổi sang link ngoài, ảnh sẽ không hiện lúc ghi hình.

**`doctor` của html-video báo sai trên Windows.** Nó kiểm ffmpeg/chromium bằng `test -x` của Unix nên luôn báo missing. Thực tế cả hai đều có.

**Đường dẫn dài.** Repo `tools/html-video` có file vượt giới hạn 260 ký tự của Windows, đã clone sparse-checkout bỏ `research/`. **Đừng chạy `git sparse-checkout disable`.**

**ElevenLabs báo 401 giả.** Key công ty không có quyền `user_read` nên endpoint `/user` trả 401. Kiểm kết nối bằng `/voices`. Phân biệt `missing_permissions` (key đúng, thiếu quyền) với 401 thật.

**Playwright nằm trong `tools/html-video`**, nạp bằng đường dẫn tuyệt đối — ESM không đọc `NODE_PATH`.

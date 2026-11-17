# tools/video-tho — bộ dựng video quay thô

Quy trình đầy đủ: skill `.claude/skills/dung-video-tho/SKILL.md`. File này chỉ nói **có gì** và **cài lại thế nào**.

## Các bước (chạy từ `D:\RBW_Claude`, `P=tools/video-tho/.venv/Scripts/python.exe`)

| Script | Bước | Ra |
|---|---|---|
| `chuan-bi.py <du-an> <clip...> --canh <...>` | chuẩn hoá 1080×1920/30fps, cân tiếng −16 LUFS | `nguon/`, `assets/canh-*`, `du-an.json` |
| `nghe-chep.py <du-an> --tu-khoa "..."` | VAD + whisper từng khối, đánh dấu ậm ừ / nói lại | `build/chep.json`, `build/ban-chep.md` |
| `de-xuat-cat.py <du-an>` | đề xuất đoạn giữ | `cat.json` (sửa tay) |
| `cat-ghep.py <du-an>` | cắt ghép khớp khung hình | `build/da-cat.mp4`, `tu-moi.json`, `ban-cat.md` |
| `lam-sach.py <du-an> [--toc-do 1.2]` | sau khi sửa tay `cat.json`: tách đoạn tại mọi lặng ≥ 0,28 s, chống lẹm chữ đầu đoạn, ghép, nới đuôi nếu lệch, nghe lại cả bản cắt (~3 phút) | `cat.json`, `build/da-cat.mp4`, `build/nghe-lai.md` |
| `mat.py <du-an>` | dò mặt YuNet | `build/mat.json` |
| `phu-de.py <du-an>` | chia cụm phụ đề theo từ (pyvi) | `phu-de.txt` (sửa tay) |
| `soi.py <du-an> 15.1 29.8 … [--nhip]` | **soi nhanh không dựng video**: `hyperframes snapshot`, kẻ vạch vùng an toàn (~1–2 s/ảnh) | `build/soi/*.png`, `build/soi/bang.jpg` |
| `dung.py <du-an> [--nhap\|--doan A-B\|--chi-nhac]` | dựng HyperFrames + trộn nhạc · `--nhap` 15 khung/giây · `--doan` chỉ một khúc, không nhạc | `05-output/<ten>.mp4` · `build/nhap.mp4` · `build/doan-A-B.mp4` |
| `kiem.py <du-an> [video]` | bảng ảnh soát có vạch vùng an toàn + đo LUFS + **tự dò chữ lấn** 12% đỉnh / 25% đáy / 140 px phải (~2 phút) | `build/kiem/bang-*.jpg`, `build/kiem/vung-*.png` |
| `vung.py` | (thư viện) vùng an toàn, chụp `snapshot`, dò điểm sáng lọt vùng cấm | — |
| `soat-bia.py <du-an> [anh-bia.png] [--html assets/bia.html]` | soát ảnh bìa: vạch vùng an toàn + khung lưới 3:4 + ô lưới thu nhỏ; `--html` chụp HTML thành ảnh bìa trước (kênh công ty); **nhúng ảnh bìa vào video thành phẩm** (`dung.py` bản thật cũng tự nhúng) | `build/bia/soat.jpg`, `anh-bia.jpg`, MP4 có ảnh bìa |
| `chup-html.mjs <vao.html> <ra.png>` | Playwright chụp HTML 1080×1920 (dùng qua `soat-bia.py --html`) | png |
| `am-thanh.py tim\|tai\|liet-ke\|tai-lai` | kho hiệu ứng myinstants.com | `02-media/am-thanh/myinstants/` |
| `tach-nhac.py <video...>` | tách nhạc nền khỏi video có người nói (Demucs) | `02-media/am-thanh/nhac-nen-video-mau/` |

## Thành phần

| Thứ | Bản | Vì sao |
|---|---|---|
| faster-whisper `large-v3-turbo` (int8, CPU) | 1.2.1 | chép tiếng Việt có mốc từng chữ, ~1× thời lượng trên i7-1355U |
| Silero VAD (đi kèm faster-whisper) | — | chia đảo tiếng nói |
| pyvi | 0.1.1 | tách từ tiếng Việt cho phụ đề |
| OpenCV + YuNet | 5.0.0 | dò mặt (mô hình chép từ `11-app-nova/nhan-dien-khuon-mat`) |
| Demucs `htdemucs` + torch CPU | 4.1.0 / 2.15 | tách nhạc nền khỏi giọng |
| HyperFrames (npm, khoá cứng) | 0.9.52 | HTML+GSAP → MP4, tua từng khung nên mọi lần dựng giống hệt nhau |
| GSAP | 3.14.2 | hoạt cảnh, chép sẵn `vendor/gsap.min.js` |
| Font Neusharp + Britti WOFF2 đã bỏ hint | — | `fonts/`, chép từ `cloudflare/robot-phuc-vu-le-tan` |

Telemetry của HyperFrames bị tắt (`HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`) trong `chung.py`.

## Tốc độ (đo 16–17/11/2026, video 012, 57 s)

| Việc | Thời gian | Ghi chú |
|---|---|---|
| `dung.py` bản thật | 2–3,5 phút | ~45–50 s phí cố định mỗi lần render (trích khung video nguồn ~20 s, prehash ~8 s, âm thanh ~14 s) + chụp |
| `dung.py --nhap` (15 khung/giây) | ~2 phút | chỉ bớt phần chụp |
| `dung.py --doan 13-20` (7 s) | ~1,5–2,5 phút | phí cố định vẫn trả đủ — dùng khi cần xem CHUYỂN ĐỘNG |
| `soi.py` 16 ảnh | ~23 s | dùng mặc định để soi bố cục / chữ / vùng an toàn |
| `kiem.py` (bảng + dò vùng) | ~2 phút | |
| `lam-sach.py` | ~3 phút | |

Đã thử mà KHÔNG nhanh hơn (đừng thử lại): `PRODUCER_FORCE_SCREENSHOT=true`, `HYPERFRAMES_EXTRACT_CACHE_MAX_MB=8192`,
`--workers 1/2`. Bộ đệm khung luôn trượt vì khoá theo thư mục tạm của mỗi lần render.

## Cài lại trên máy mới (~3 GB)

```powershell
cd D:\RBW_Claude\tools\video-tho
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install faster-whisper opencv-python numpy pillow soundfile pyvi
.\.venv\Scripts\python.exe -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install demucs
npm install                      # hyperframes 0.9.52 + gsap 3.14.2 theo package.json
python am-thanh.py tai-lai       # tải lại các mp3 hiệu ứng theo muc-luc.json
```
Mô hình whisper (~1,6 GB) tự tải vào `models/` lần chạy đầu.

## Thư mục không vào git
`.venv/` · `models/` · `node_modules/` · `tham-khao/` (bản clone ghost-editor, herk-edit-kit, hyperframes,
iart-ai/motion-skills, iart-ai/tiktok-video-skills — chỉ để đọc học, **không chạy script trong đó**) · `_thu/`.
Tải lại tham khảo: `git clone --depth 1 https://github.com/<kho> tham-khao/<ten>`.

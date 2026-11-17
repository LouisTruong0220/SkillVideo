# SkillVideo — Bộ skill dựng video social Roboworld cho Claude Code

Hai skill Claude Code dựng video dọc 1080×1920 (TikTok / Reels) cho kênh Duy Trường Robot / Roboworld,
kèm toàn bộ công cụ và 2 subagent kiểm duyệt.

| Skill | Dùng khi | Đầu vào → đầu ra |
|---|---|---|
| `video-roboworld` | "Làm video về …" — dựng từ **ảnh + giọng đọc máy** | Đề bài → kịch bản → giọng ElevenLabs → `scenes.json` → MP4 |
| `dung-video-tho` | Gửi một **video tự quay** (nói trước camera) để cắt, thêm phụ đề, hiệu ứng | Clip điện thoại → nghe-chép → cắt ậm ừ → phụ đề + đồ hoạ HyperFrames → MP4, **giữ giọng thật** |

Cả hai đều có 2 chốt duyệt (kịch bản / bản cắt thô, và thành phẩm) và gọi subagent `rbw-qc` soát trước khi giao.

## Cấu trúc

Gói giữ nguyên đường dẫn của workspace gốc — skill và script đều dùng đường dẫn tương đối từ **gốc dự án**,
nên **chép cả thư mục này vào gốc dự án** (không chép riêng `.claude/`).

```
.claude/skills/video-roboworld/     SKILL.md + references/ (luật kịch bản, luật hình, schema scenes.json, lệnh render)
.claude/skills/dung-video-tho/      SKILL.md + references/ (luật cắt, phong cách kênh, schema dung.json, Remotion, bẫy)
.claude/agents/rbw-qc.md            subagent kiểm duyệt video (chỉ đọc)
.claude/agents/rbw-research.md      subagent tìm & chuẩn hoá ảnh 1080×1920
tools/make-video.py · build-frame.py · render-video.mjs · prep-assets.py · anh-scene.py   dây chuyền video-roboworld
tools/elevenlabs/                   sinh giọng đọc (doc-kich-ban.py), nhân bản giọng, hướng dẫn
tools/video-tho/                    dây chuyền dung-video-tho (Python + HyperFrames) — xem README riêng trong đó
tools/remotion/                     dự án Remotion (React) dựng bảng đồ hoạ nửa trên + ảnh bìa — mẫu video 011, 012
00-brand/                           font nhúng base64 + brand-tokens.css (build-frame.py cần)
03-knowledge/                       nguồn số liệu: products.json · pricing.json · proof-points.json · văn mẫu · brand voice
04-video-projects/_template/        khuôn brief / storyboard cho dự án video mới
04-video-projects/LESSONS.md        nhật ký bài học từ các video đã dựng
02-media/am-thanh/                  nhạc nền tách từ video mẫu + mục lục hiệu ứng myinstants
```

## Cài đặt (Windows, PowerShell)

Cần sẵn: **Python 3.11+**, **Node.js 20+**, **ffmpeg** trên PATH (`winget install ffmpeg`), Claude Code.

### 1. Skill `video-roboworld`

```powershell
cd <goc-du-an>\tools\elevenlabs
pip install -r requirements.txt
copy .env.example .env          # rồi điền ELEVENLABS_API_KEY và ELEVENLABS_VOICE_ID
python test-ket-noi.py          # kiểm tra khoá + liệt kê giọng
```

`render-video.mjs` cần Playwright + Chromium. Bản gốc mượn Playwright cài kèm `tools/html-video`;
trên máy mới cài thẳng:

```powershell
cd <goc-du-an>\tools
npm install playwright
npx playwright install chromium
```
`render-video.mjs` tự tìm Playwright ở `tools/node_modules/` khi không có `tools/html-video`.

### 2. Skill `dung-video-tho` (~3 GB sau khi cài)

```powershell
cd <goc-du-an>\tools\video-tho
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install faster-whisper opencv-python numpy pillow soundfile pyvi
.\.venv\Scripts\python.exe -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install demucs
npm install                      # hyperframes 0.9.52 + gsap 3.14.2
python am-thanh.py tai-lai       # tải lại hiệu ứng âm thanh theo muc-luc.json
```
Mô hình whisper `large-v3-turbo` (~1,6 GB) tự tải vào `tools/video-tho/models/` ở lần chạy đầu.
Mô hình dò mặt YuNet đã có sẵn trong `models/`.

### 3. Remotion (tuỳ chọn — chỉ cho video kênh cá nhân)

```powershell
cd <goc-du-an>\tools\remotion
npm install                      # remotion 4.x + react 19
npx remotion studio src/index.ts # xem trước cảnh mẫu v011 / v012
node scripts/v012.mjs            # dựng các cảnh của video 012 (mẫu để chép sang vNNN)
```
Cách dùng trong quy trình: `.claude/skills/dung-video-tho/references/remotion.md`.
⚠ Giấy phép Remotion miễn phí cho cá nhân — video kênh / tài liệu công ty Roboworld phải mua bản quyền.

## Dùng

Mở Claude Code ở gốc dự án rồi nói tự nhiên:

- *"Làm video về chi phí nhân viên chạy bàn so với robot phục vụ"* → `video-roboworld`
- *"Dựng video này thành reel: D:\Downloads\IMG_1234.mp4"* → `dung-video-tho`

## Những thứ KHÔNG có trong gói

| Thứ | Vì sao | Lấy lại |
|---|---|---|
| Khoá ElevenLabs (`.env`) | bí mật | tự tạo tại elevenlabs.io → `.env` |
| `.venv/`, `node_modules/`, mô hình whisper | nặng, cài lại được | các lệnh cài ở trên |
| File mp3 hiệu ứng myinstants | của bên thứ ba | `python tools/video-tho/am-thanh.py tai-lai` |
| Kho ảnh / video robot `02-media/san-pham/` | rất nặng | tự bổ sung ảnh của mình; `rbw-research` sẽ tìm trong đó |
| Các dự án video đã dựng `04-video-projects/0xx-*` | dữ liệu riêng | — (skill có nhắc tới làm ví dụ) |

## Lưu ý

- Luật nội dung (không tự thêm logo / số điện thoại lên hình, chữ ở giữa khung, gọi "robot phục vụ",
  không bịa số) nằm trong mỗi `SKILL.md` — đọc trước khi chỉnh skill.
- Giá trong `03-knowledge/pricing.json` **chưa gồm VAT 8%** và không ghi thời hạn hiệu lực — luôn kiểm lại trước
  khi đưa lên video.
- Remotion (`dung-video-tho/references/remotion.md`) chỉ miễn phí cho cá nhân; video kênh công ty phải mua bản quyền.
- Font Neusharp / Britti Sans là font thương mại của nhận diện Roboworld.

# Bẫy đã dính khi dựng bộ công cụ (15/11/2026)

Mỗi mục: triệu chứng → nguyên nhân → đã chặn ở đâu. Bẫy mới thêm LÊN ĐẦU.

## VT-15 — Phụ đề cụm dài lấn cột nút phải, 3 vòng QC không thấy (video 012, 17/11/2026)
Khung phụ đề `.pd` chạy x 70–1010 (căn giữa) → cụm ~22 ký tự ở 74 px rộng ~830 px, lấn quá x 940. QC đo bằng mắt
trên ảnh nhỏ nên sót. → `.pd` nay 150–930 px + `co_pd()` tự thu cỡ chữ cho vừa MỘT dòng (≈ 0,5 × cỡ chữ mỗi ký tự).
Đừng chỉ thu khung mà không thu chữ — cụm dài xuống dòng mồ côi ("…chúng / em"). `kiem.py` nay tự dò.

## VT-14 — Máy không tự bắt được tiếng vấp nửa chữ (17/11/2026)
Thử trên 4 chỗ vấp thật của video 012 ("nh-", "ư-", "m-", "n-"): tiếng dư sau chữ cuối của chỗ vấp 0,10–0,24 s,
đuôi câu bình thường cũng dư 0,13–0,22 s (whisper chấm hết chữ sớm) → không có ngưỡng tách. Whisper nghe riêng
đuôi: 9–14 s mỗi lượt trên CPU máy này và bịa "Cảm ơn các bạn đã theo dõi" trên tiếng nửa chữ; nghe cả bài thì bỏ
qua tiếng vấp. → `lam-sach.py` chỉ làm phần chắc chắn (lặng, lẹm chữ, lệch độ dài); chỗ vấp dò tay (SKILL.md B3).

## VT-13 — `dung.py --doan` / `--nhap` không nhanh như tưởng (16–17/11/2026)
HyperFrames trả ~45–50 s phí cố định MỖI lần render dù chỉ một khúc 7 s: trích khung mọi video nguồn ~20 s (bộ đệm
khoá theo thư mục tạm nên luôn trượt), prehash ~8 s, âm thanh ~14 s (riêng "guard" ~11 s), nền tham chiếu ~4 s; rồi
mỗi khúc chụp thử BeginFrame hỏng mới chạy lại bằng screenshot. Đã thử `PRODUCER_FORCE_SCREENSHOT=true`,
`HYPERFRAMES_EXTRACT_CACHE_MAX_MB=8192`, `--workers 1/2` — không nhanh hơn. → Soi bố cục bằng `soi.py`
(`hyperframes snapshot --at`, ~1–2 s/ảnh, khớp video thật); chỉ render khi cần xem chuyển động.

## VT-12 — Chữ cuối video bị xén vài chục mili giây (video 012, 16/11/2026)
Bản cắt nhiều đoạn (25 đoạn) dài hơn tính toán 0,17 s — mỗi đoạn làm tròn khung lệch một chút, `cat-ghep.py` báo
"⚠ độ dài thực lệch tính toán". `dung.py` cắt video ở `tong` (tính toán) → đuôi tiếng thật bị xén.
→ Tiếng–hình vẫn khớp nhau (lệch 35 ms). Chữa: nới mép `b` đoạn cuối thêm ≥ độ lệch (vẫn trong khoảng lặng), rồi
nghe-chép 2,5 s cuối của thành phẩm để chắc chữ cuối còn trọn.

## VT-11 — Đường vẽ dở (stroke-dashoffset 0,55) không hiện gì (video 012, 16/11/2026)
GSAP tween `strokeDashoffset` như thuộc tính CSS → đơn vị px → **tự làm tròn về số nguyên** (0,55 → 1). Đường dùng
`pathLength="1"` nên chỉ hiện khi về đúng 0. Dấu tick 1→0 chạy được nên rất khó nhận ra.
→ Trong khối `html` tự viết, tween bằng `attr:{"stroke-dashoffset": x}`. Soi khối riêng không cần dựng lại:
mở `build/hf/index.html` bằng Playwright, `addInitScript(() => window.__timelines = {})`, rồi `__timelines.main.seek(t)`.

## VT-10 — Anh Trường nghe ra "đoạn trống" dù bản chép không còn ậm ừ (video 012, 16/11/2026)
Khi Claude sửa tay `cat.json` và **gộp nhiều đảo thành một đoạn dài**, `cat-ghep.py` giữ nguyên mọi khoảng lặng bên
trong (chỉ `de-xuat-cat.py` mới chia tại lặng). Kèm đó: đầu mỗi đoạn còn 0,3–0,5 s lặng.
→ Xem `luat-cat.md` mục "Sau khi sửa tay cat.json".

## VT-09 — Phụ đề / tiêu đề / thẻ số bị đẩy xuống đáy khung, cửa sổ kéo dài hết màn hình
HyperFrames tự dàn **mọi phần tử con của root có `data-start`** thành toàn khung, đè `top`/`height` mình đặt.
→ `dung.py`: phần tử có thời gian chỉ là lớp `.lop` 1080×1920; nội dung định vị nằm BÊN TRONG lớp. Khối `html`
tự viết cũng phải theo cách này.

## VT-08 — Viền cảnh phụ hiện suốt video
Bọc `<video class="clip">` trong một `div` có viền mà div không có thời gian → video tắt nhưng viền vẫn còn.
→ Viền/khung đặt thẳng lên thẻ `<video>`.

## VT-07 — Render chết: "GSAP was not loaded yet"
HyperFrames KHÔNG tự nạp GSAP. → `dung.py` chép `tools/video-tho/vendor/gsap.min.js` (3.14.2) vào `assets/` và nạp
bằng `<script src>` — không dùng CDN (render không phụ thuộc mạng).

## VT-06 — Whisper bịa "Hãy subscribe cho kênh Ghiền Mì Gõ" trên đoạn có tiếng nói rõ
VAD cắt đảo **giữa câu** (ngắt hơi 0,2 s) → whisper nhận đoạn mở đột ngột → ảo giác kinh điển của tiếng Việt.
→ `nghe-chep.py` gộp đảo cách < 0,6 s thành khối để chép; khối nào vẫn bịa/lặp → chép lại kèm 3 s ngữ cảnh trước,
rồi thử bỏ lời mồi. Danh sách câu ảo giác ở `AO_GIAC` — gặp câu mới thì thêm vào.

## VT-05 — Whisper kẹt vòng "cắt 2, cắt 2, cắt 2…"
Đặt `temperature=0.0` tắt luôn cơ chế tự chép lại khi tỉ lệ nén cao. → để mặc định (dãy nhiệt độ dự phòng).

## VT-04 — `faster_whisper` lỗi `open() got an unexpected keyword argument 'metadata_errors'`
PyAV bản mới đổi giao diện. → tự đọc wav bằng `soundfile` rồi đưa mảng float32 cho whisper.

## VT-03 — Phụ đề ngắt giữa từ ghép ("nhà | hàng", "phục | vụ")
Whisper trả từng ÂM TIẾT. → `phu-de.py` gom âm tiết thành từ bằng `pyvi` trước khi chia cụm.

## VT-02 — Whisper bỏ qua tiếng ậm ừ
Mô hình được huấn luyện để chép "sạch". → (1) lời mồi có sẵn "Ờ, ừm, à" để mô hình chịu chép ậm ừ;
(2) đo năng lượng 10 ms: khe giữa hai chữ ≥ 0,25 s mà ≥ 40% có tiếng → đánh dấu `[…]` và cắt.

## VT-01 — Nhạc tách từ video mẫu còn tiếng vút đoạn logo kết
3,5 s cuối mỗi video mẫu là khung logo có âm hiệu ứng. → `muc-luc.json` ghi `doan_sach` bỏ phần đó; `dung.py` chỉ
lặp trong đoạn sạch.

## Bẫy thừa kế (đã có ở workspace, vẫn áp dụng)
- Font Britti TTF: Chromium vẽ "c" thành "o" ở ≥ 20px → chỉ dùng `tools/video-tho/fonts/*.woff2` (đã bỏ hint).
- `eleven_v3` / ElevenLabs: skill này KHÔNG dùng — giọng là giọng thật trong video. (Khoá ElevenLabs báo 401 ngày 15/11/2026.)
- Không chạy 2 lần dựng song song — HyperFrames dùng hết CPU, lần dựng kia chậm gấp đôi.
- Python in tiếng Việt ra màn hình lỗi `charmap` → `chung.py` đã `reconfigure(encoding="utf-8")`.

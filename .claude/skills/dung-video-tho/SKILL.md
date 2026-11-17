---
name: dung-video-tho
description: Dựng video social dọc 1080×1920 từ VIDEO QUAY THÔ của anh Trường hoặc nhân viên Roboworld (nói trước camera, cạnh robot) — nghe-chép từng chữ, cắt khoảng lặng / ậm ừ / câu nói hỏng, ghép đoạn cho mạch lạc, thêm phụ đề, tiêu đề bật, cảnh phụ, mô phỏng robot, thẻ số, biểu đồ, hiệu ứng âm thanh và nhạc nền, GIỮ NGUYÊN GIỌNG THẬT (không ElevenLabs), chèn video thực tế robot từ kho, ghép bằng HyperFrames (Remotion khi anh Trường yêu cầu cho kênh cá nhân). Dùng skill này MỌI KHI người dùng gửi/đưa đường dẫn một file video tự quay (.mp4/.mov, IMG_xxxx, clip điện thoại) và muốn edit, cắt, dựng, làm thành reel/TikTok, thêm phụ đề hay hiệu ứng cho nó. Video dựng từ ẢNH + giọng đọc máy thì dùng skill video-roboworld, không phải skill này.
---

# Dựng video quay thô

Đầu vào: một hoặc vài clip anh Trường quay bằng điện thoại (nói trước camera) + cảnh phụ nếu có.
Đầu ra: `05-output/<ten>.mp4` 1080×1920, 30 khung/giây, −14 LUFS, giọng thật của anh Trường.

Công cụ ở `tools/video-tho/` (Python chạy bằng `.venv` riêng). Dựng hình bằng **HyperFrames** (HTML → video,
Apache-2.0, dùng miễn phí cho công ty) — đây luôn là bộ GHÉP cuối (người nói, phụ đề, tiêu đề, cảnh phụ, nhạc).

**Remotion — chỉ khi anh Trường yêu cầu VÀ xác nhận video đăng kênh cá nhân của anh.** Giấy phép Remotion miễn phí
cho cá nhân; video kênh / tài liệu công ty Roboworld (40 người) phải mua bản quyền. Remotion dựng **bảng nửa trên
1080×960** thành MP4 rồi HyperFrames ghép như cảnh phụ — xem `references/remotion.md`. Mỗi video phải hỏi lại kênh
đăng; ghi điều kiện giấy phép vào `README.md` + `assets/NGUON.md` của dự án. (Video 012, 16/11/2026: anh xác nhận
kênh cá nhân. QC lưu ý giấy phép có thể xét theo *ai dùng để làm gì* — video có nhân viên chào bán sản phẩm công ty
thì nhắc anh cân nhắc mua bản quyền trước khi đăng lại lên kênh công ty.)

```
P=tools/video-tho/.venv/Scripts/python.exe        # mọi lệnh bên dưới chạy từ D:\RBW_Claude
```

---

## Năm luật tuyệt đối (thừa kế từ video-roboworld + CLAUDE.md)

1. **Không chủ động thêm logo / số điện thoại** lên hình. 7 video mẫu cũ có logo "Duy Trường Robot" ở đỉnh và khung
   logo + liên hệ ở cuối — **đó là kiểu cũ, không làm theo**. Kết thúc bằng câu chốt giá trị/lời mời nhắn tin.
   Logo/số lỡ có sẵn trong cảnh quay thật thì không sao.
2. **Không bịa số mình đưa lên.** Phụ đề chép đúng lời anh Trường nói. Nhưng thẻ số, biểu đồ, tiêu đề có số do
   MÌNH thêm thì số phải có trong `03-knowledge/*.json` hoặc chính anh Trường nói trong video. Biểu đồ ghi `nguon`.
3. **Chữ mình thêm gọi "robot phục vụ"**, không tên model — trừ khi anh Trường đang giới thiệu đúng model đó.
   Phụ đề thì chép đúng lời nói (anh nói "BellaBot" thì phụ đề ghi "BellaBot", sửa chính tả "Delabot").
4. **Chữ ở giữa khung**, tránh 12% đỉnh, 25% đáy, 140px mép phải (cột nút TikTok) — **kể cả chữ ở nửa trên**.
   `kiem.py` tự dò mọi chữ lấn (HyperFrames + cảnh Remotion `rm-*.mp4`).
   `dung.py` chỉ tự giữ cho khối có sẵn: câu móc chừa 140 px hai bên (dòng 1 dài thì hạ `co`), tiêu đề dài thì hạ
   `co` (≤ 80 cho dòng ~15 ký tự in hoa). **Khối tự vẽ (html / Remotion) đi vòng qua nên phải tự giữ: chữ `top ≥ 250 px`,
   mép phải `≤ 940 px`.** Video 012 trượt QC 2 vòng vì đúng lỗi này.
5. **Không đổi ý anh Trường nói.** Được bỏ câu thừa, đảo thứ tự cho mạch lạc, chọn bản nói tốt hơn. Không được
   ghép nửa câu này với nửa câu kia thành ý anh chưa từng nói.

---

## Tám bước

### B0 — Nhận video
Hỏi gọn nếu chưa rõ: video nói về gì / cho ai xem; có cảnh phụ (clip robot chạy, cận khay…) quay kèm không.
Không hỏi lại những gì đã có trong đề bài. Tạo `04-video-projects/NNN-ten-ngan/` (số kế tiếp).

**Mở xem clip trước khi chọn skill** (trích bảng ảnh `fps=1/3,tile`): người nói trước camera → skill này; người
nói có thể là nhân viên chứ không phải anh Trường, quy trình vẫn y nguyên. Thư mục tải về đặt tên ngẫu nhiên
(`1794…5501_….mp4`) — thứ tự số trong tên thường là thứ tự quay; clip ngắn không có người là cảnh phụ.

### B1 — Chuẩn hoá
```
$P tools/video-tho/chuan-bi.py 04-video-projects/NNN-ten <clip-noi...> --canh <canh-phu...>
```
Không sửa/chép file gốc. Clip quay ngang thì tự đặt giữa nền mờ (báo anh lần sau quay dọc).
**Mở xem từng cảnh phụ** (trích 1 khung) rồi điền `mo_ta` trong `du-an.json` — tên file không nói cảnh quay gì.

### B2 — Nghe-chép (≈ 1× thời lượng video trên CPU)
```
$P tools/video-tho/nghe-chep.py NNN-ten --tu-khoa "tên nhà hàng, tên khách, tên riêng trong video"
```
Ra `build/ban-chep.md`. **Đọc hết bảng này.** Ký hiệu: ~~gạch~~ máy định cắt · `[…]` có tiếng không thành chữ
(thường là ậm ừ) · ⟲ câu được nói lại ở đảo sau · ⚠ nghi ảo giác · _nghiêng_ whisper không chắc.

### B3 — Chọn đoạn → cắt thô ═══ CHỐT 1 ═══
```
$P tools/video-tho/de-xuat-cat.py NNN-ten      # máy đề xuất cat.json
```
Đọc `references/luat-cat.md` rồi **sửa tay `cat.json`**: bỏ câu thừa/lạc đề, chọn bản nói hay hơn khi cả hai đều
trọn câu, đổi thứ tự để có móc câu (hook) trong 3 giây đầu và kết bằng lời mời. Rồi:
```
$P tools/video-tho/cat-ghep.py NNN-ten         # → build/da-cat.mp4 + ban-cat.md + tu-moi.json
```
**Ba việc bắt buộc trước khi đưa duyệt** (anh Trường chê "còn ậm ừ, còn đoạn trống" ở video 012 — chi tiết
`references/luat-cat.md` mục "Sau khi sửa tay cat.json"):
```
$P tools/video-tho/lam-sach.py NNN-ten --toc-do 1.2   # ~3 phút: tự làm việc 1 và 3 dưới đây + nới đuôi khi lệch
```
1. Đoạn nào gộp nhiều đảo → **chia lại tại mọi khoảng lặng ≥ 0,28 s**, đầu đoạn sát tiếng, đầu đoạn cắt giữa tiếng
   thì lùi (chống lẹm chữ). `cat-ghep.py` KHÔNG tự bỏ lặng bên trong một đoạn — **`lam-sach.py` làm việc này.**
2. **Tiếng vấp nửa chữ ("ư-", "n-", "m-", "nh-") — máy KHÔNG tự bắt được** (đã thử 17/11, bẫy VT-14). Dò bằng mắt
   trong `ban-chep.md` (chữ kéo dài bất thường, đảo tiếng 0,1–0,2 s trước chữ thật), chép lại riêng hai mẩu hai bên
   chỗ nghi; thấy vấp thì chỉnh tay `b` của đoạn đó trong `cat.json` + `"giu": true` rồi chạy lại `lam-sach.py`.
3. **Nghe-chép lại cả `da-cat.mp4`** — `lam-sach.py` ghi `build/nghe-lai.md` (chữ mất / thừa / lặp). Đọc file đó.

Anh thích nhịp nhanh: `--toc-do 1.2` (ghi `"toc_do"` vào `cat.json`, atempo giữ cao độ).

**Dừng. Đưa anh Trường:** đường dẫn `build/da-cat.mp4`, độ dài trước/sau, và danh sách gọn những câu đã bỏ/đảo
(kèm lý do). Anh duyệt nội dung cắt xong mới làm đồ hoạ — sửa cắt sau khi đã dựng hiệu ứng là làm lại từ đầu.
Anh nói "làm luôn không cần duyệt" thì bỏ qua chốt này.

### B4 — Mặt + phụ đề
```
$P tools/video-tho/mat.py NNN-ten
$P tools/video-tho/phu-de.py NNN-ten
```
**Sửa `phu-de.txt`:** chính tả tên riêng/thuật ngữ, số viết bằng chữ số ("10 suất"), đánh `*từ khoá*` (tối đa
1 chỗ/cụm, khoảng 1/3 số cụm có nhấn — nhấn số liệu, lợi ích, tên ý chính). Không thêm chữ anh không nói.

### B5 — Kế hoạch đồ hoạ `dung.json`
Đọc `references/phong-cach-kenh.md` (nhịp, mật độ, chọn hiệu ứng) và `references/schema-dung.md` (mọi loại nhịp).
Lên kế hoạch từ `build/ban-cat.md` (thời gian MỚI). Chữ mình thêm (câu móc `mo-dau`, tiêu đề, câu chốt, tiêu đề ảnh
bìa, caption) viết bằng giọng anh theo `03-knowledge/van-mau-anh-truong.md` — ưu tiên dùng đúng chữ anh nói trong
video. Nhạc nền: chọn trong
`02-media/am-thanh/nhac-nen-video-mau/muc-luc.json` — **anh Trường chốt 15/11/2026 chỉ dùng nhạc tách từ video mẫu
của anh**, không dùng nhạc các video đã dựng trước. Hiệu ứng âm: `python tools/video-tho/am-thanh.py liet-ke`
(kho myinstants; thiếu thì `am-thanh.py tai <từ khoá> --nhom <nhóm>`).

- **Cắt dày (điểm cắt mỗi 1–2 s)** → `"doi_khung_cach": 2.0` để khung rộng/cận không giật ở mọi điểm cắt.
- **Đổi hình mỗi 5–8 s ngay từ đầu.** Đoạn mở bằng ví dụ so sánh (điện thoại, ô tô…) rất hợp một bảng mô phỏng
  nửa trên — đừng để 20 s đầu chỉ có người nói (QC góp ý video 012).
- **Cảnh thật trước, đồ hoạ sau.** Người nói nhắc robot / ứng dụng → tìm cảnh quay thật và ảnh app thật trong kho
  (danh sách đã soi: `references/phong-cach-kenh.md` mục "Kho cảnh thật"). Mọi đoạn video lấy từ kho phải **soi từng
  0,2 s** — tránh phụ đề cháy sẵn, end card, khúc chỉ thấy lưng người / lia cảnh trống.
- **Khối tự vẽ** cho ý trừu tượng (hôm nay → tương lai, tích hợp…): mặc định `html` trong HyperFrames
  (`schema-dung.md`); dùng Remotion khi anh yêu cầu (`references/remotion.md`). Chữ trên khối lấy từ lời nói.

### B6 — Soi ảnh tĩnh → dựng thật → kiểm
**Mỗi lần dựng HyperFrames tốn 2–3,5 phút, ~50 s trong đó là phí cố định** (bẫy VT-13) — nên soi bằng ảnh tĩnh,
chỉ dựng video khi bố cục đã đạt:
```
$P tools/video-tho/soi.py NNN-ten --nhip          # ~20–30 s: 1 ảnh mỗi nhịp, kẻ vạch vùng an toàn → build/soi/bang.jpg
$P tools/video-tho/soi.py NNN-ten 15.1 29.8       # soi lại đúng mấy giây vừa sửa
```
**Mở `build/soi/bang.jpg` và soi**: chữ đè mặt? chữ lấn vạch? tiêu đề trùng phụ đề? cảnh phụ đúng câu đang nói?
Sửa `dung.json`/`phu-de.txt`/khối html → `soi.py` lại. Cần xem CHUYỂN ĐỘNG một cảnh: `dung.py NNN-ten --doan 28-35`
(~2 phút, không nhạc). Bố cục đạt rồi mới:
```
$P tools/video-tho/dung.py NNN-ten             # chất lượng thật → 05-output/<ten>.mp4
$P tools/video-tho/kiem.py NNN-ten             # ~2 phút: bảng soát có vạch + LUFS + TỰ DÒ chữ lấn vùng an toàn
```
`kiem.py` in "✗" kèm giây + toạ độ cho chỗ lấn kéo dài, "·" cho chỗ thoáng qua (khối đang trượt) — xem
`build/kiem/vung-*.png`. Phải sạch "✗" rồi mới giao QC. Phụ đề cụm dài nay tự thu cỡ chữ cho vừa một dòng trong 150–930 px.
`dung.py --nhap` (15 khung/giây, ~2 phút) chỉ còn dùng khi cần xem nhịp cả bài.
Chỉ đổi nhạc: `dung.py NNN-ten --chi-nhac` (không dựng lại hình). Muốn chỉnh trực quan: `tools/video-tho/node_modules/.bin/hyperframes preview 04-video-projects/NNN-ten/build/hf`.

Khối `html` tự viết không chạy đúng → đừng dựng lại cả video để thử: mở `build/hf/index.html` bằng Playwright,
`addInitScript(() => window.__timelines = {})`, rồi `__timelines.main.seek(t)` và đọc giá trị (bẫy VT-11: tween
`strokeDashoffset` kiểu CSS bị làm tròn số nguyên → dùng `attr:{"stroke-dashoffset":x}`). Ô xem trước trong app
mở trang dạng `data:` nên không nạp được GSAP — dùng Playwright.

### B6b — Ảnh bìa (luôn làm kèm, anh Trường yêu cầu 16/11/2026)
Khung 1080×1920, lưu `04-video-projects/NNN-ten/anh-bia.png` (+ `.jpg` để tải lên). Công thức đã duyệt (video 011, 012):
- **Trên (y 268–700):** dòng nhỏ Britti nói chủ đề ("Robot lễ tân AI…") + tiêu đề Neusharp IN HOA 2–3 dòng, ~110 px,
  từ khoá vàng. Tiêu đề là **câu hỏi / nghịch lý bám đúng ý móc câu của video** (012: phép so sánh "điện thoại chỉ
  nghe gọi" → "CHỈ ĐỂ CHÀO KHÁCH?"). Không bịa ý, số trên bìa phải là số người nói nói trong video.
- **Giữa (y ~700–1160):** 2 thẻ ảnh thật bo góc viền đỏ/vàng + nhãn (HÔM NAY → TƯƠNG LAI, NHÀ MÁY vs NHÀ HÀNG) —
  ảnh lấy từ chính video: khung robot **nhìn thẳng, rõ mặt màn hình** dễ nhận ra hơn robot quay lưng / ở xa.
- **Dưới:** mặt người nói, mờ dần lên trên; mắt + miệng phải nằm trong dải lưới (y ≤ 1680). Chọn khung đang cười / mắt mở.
- Chữ trong x 140–940, y ≥ 250. Không logo, không số điện thoại.

Dựng: Remotion `Still` khi video dùng Remotion (kênh cá nhân — `references/remotion.md`); kênh công ty thì viết
`assets/bia.html` 1080×1920 (font từ `tools/video-tho/fonts/`) và để `soat-bia.py --html` chụp. Rồi **soát**:
```
$P tools/video-tho/soat-bia.py NNN-ten                    # → build/bia/soat.jpg + anh-bia.jpg
$P tools/video-tho/soat-bia.py NNN-ten --html assets/bia.html
```
Mở `build/bia/soat.jpg`: trái là cả ảnh có vạch vùng an toàn + khung tím dải lưới 3:4 (y 240–1680); phải là ô lưới
đúng như TikTok cắt trên trang hồ sơ — tiêu đề, hình chính, mặt người phải đủ trong ô đó.

**Gắn ảnh bìa vào video — tự động** (anh Trường hỏi 17/11/2026 "ảnh bìa chưa gắn vào video à"): `soat-bia.py` nhúng
`anh-bia.jpg` vào `05-output/<ten>.mp4` nếu video đã có, và `dung.py` (bản thật) tự nhúng mỗi lần dựng. Nhúng = thêm
luồng ảnh `attached_pic`, chép nguyên hình/tiếng (đã đối chiếu md5 không đổi).
⚠ **Ảnh nhúng chỉ hiện ở trình quản lý file trên máy tính (File Explorer, VLC…).** Zalo, Messenger, Telegram, thư viện
ảnh điện thoại, TikTok/Reels **tự lấy khung hình ĐẦU TIÊN của video**, bỏ qua ảnh nhúng — 17/11/2026 anh Trường gửi
video 012 lên vẫn thấy mặt người nói ở giây 0 thay vì ảnh bìa (đã kiểm tra: file vẫn có `covr`). Vì vậy:
- Đăng TikTok/Reels → tải `anh-bia.jpg` lên ở bước "Chọn ảnh bìa" — dặn anh câu này khi giao video.
- Gửi qua Zalo/Messenger mà muốn hiện bìa → phải **ghép ảnh bìa thành khung hình đầu** (đổi nội dung video,
  hỏi anh Trường trước). Anh Trường gửi Zalo thật (17/11) → làm **bản riêng** `05-output/<ten>-zalo.mp4`, giữ bản gốc:
  chèn `anh-bia.jpg` 0,1 s (3 khung @30fps) bằng `concat`, tiếng `adelay=100|100`, x264 crf 16, nhúng lại `covr`.
  Kiểm: khung 0 = bìa, khung ở 0,1 s = cảnh gốc, `silencedetect` thấy đúng 0,1 s lặng ở đầu.

### B7 — Soát → ═══ CHỐT 2 ═══
Giao subagent `rbw-qc` (chỉ đọc) soi `05-output/<ten>.mp4` theo luật trên + `references/phong-cach-kenh.md`.
FAIL → sửa đúng danh sách, tối đa 2 vòng. PASS → đưa anh Trường: đường dẫn file bấm được (video + **ảnh bìa**),
độ dài, nhạc đã dùng, 1 câu caption gợi ý (hotline `0866 153 946` chỉ ở caption). Giao QC soát cả `anh-bia.png`.

- Giao QC SAU khi `kiem.py` sạch "✗" vùng an toàn — để QC lo nội dung, không tốn vòng vì lỗi máy đo được.
  (Video 012: 3 vòng QC vẫn sót 3 cụm phụ đề lấn cột phải; `kiem.py` bắt được ngay lần chạy đầu.)
- Dặn QC **đo ở độ phân giải đầy đủ** (1080×1920), không đo trên bảng ảnh thu nhỏ — video 012 vòng 1 sót lỗi lấn
  mép phải vì đo trên ảnh nhỏ.
- Vòng sau phải soát lại **đủ mọi mục**, không chỉ chỗ vừa sửa. Gửi QC danh sách thay đổi nhưng dặn "đối chiếu file thật".
- Anh Trường thêm yêu cầu mới giữa chừng (vd thêm Remotion, thêm cảnh thật) → đếm lại vòng QC từ đầu cho bản mới.
- Cùng một subagent QC (gửi tiếp bằng `SendMessage`) nhớ lỗi vòng trước → bắt được lỗi "sửa chưa hết".

### B8 — Ghi bài học
Anh nhận xét xong: thêm mục mới lên đầu `04-video-projects/LESSONS.md`; luật lặp lại được → ghi vào `references/`
của skill này. Bẫy kỹ thuật mới → `references/bay.md`.

**Bổ sung văn mẫu** (anh Trường yêu cầu 17/11/2026): video anh tự nói được duyệt → thêm lời thoại vào
`03-knowledge/van-mau-anh-truong.md` theo mục 6 của file đó (lời từ `phu-de.txt`, chia nhịp móc · thân · kết, câu bị
cắt kèm lý do, cập nhật mục 1/4 nếu có nét văn phong mới). Anh đăng xong và gửi caption thật → chép vào mục 5.

---

## Tham chiếu

| File | Đọc khi |
|---|---|
| `references/luat-cat.md` | B3 — chọn đoạn, ậm ừ tiếng Việt, câu nói lại, mép cắt |
| `references/phong-cach-kenh.md` | B4–B5 — phong cách 7 video mẫu, nhịp đồ hoạ, mức nhạc |
| `references/schema-dung.md` | B5 — mọi trường `dung.json`, ví dụ đầy đủ |
| `references/remotion.md` | B5 — khi anh yêu cầu dựng bằng Remotion (giấy phép, cách ghép, mẫu video 011/012) |
| `references/bay.md` | gặp lỗi lạ — các bẫy đã dính khi dựng bộ công cụ |
| `04-video-projects/012-robot-le-tan/README.md` | ví dụ đầy đủ gần nhất: cắt dày ×1,2, Remotion + video Nova thật, 3 vòng QC |
| `tools/video-tho/README.md` | cài lại trên máy mới, danh sách công cụ |
| `tools/video-tho/tham-khao/` | mã nguồn ghost-editor, HyperFrames, motion-skills… để học thêm hiệu ứng |

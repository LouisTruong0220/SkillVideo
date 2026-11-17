---
name: video-roboworld
description: Dựng video social dọc 1080×1920 cho Duy Trường Robot / Roboworld (robot phục vụ nhà hàng) — từ đề bài đến file MP4 có giọng anh Trường và nhạc nền. Dùng skill này MỌI KHI người dùng yêu cầu làm video, dựng video, làm clip TikTok/Reels, viết kịch bản video, sửa lại một video đã dựng, hoặc thêm/đổi giọng đọc và nhạc nền cho video. KHÔNG dùng khi người dùng gửi một VIDEO TỰ QUAY (nói trước camera) để cắt/edit — việc đó thuộc skill dung-video-tho.
---

# Dây chuyền video Roboworld

Quy trình 7 bước, chạy **tuần tự**, dừng ở đúng **2 chốt duyệt**. Đọc hết mục "Ba luật tuyệt đối" trước khi làm bất cứ bước nào.

---

## Năm luật tuyệt đối

**1. KHÔNG chủ động thêm logo / số điện thoại vào thứ mình dựng.**
Không tự đặt logo Roboworld / DTR / PUDU dạng đồ hoạ, không tự gõ số điện thoại thành chữ, không đọc số điện thoại trong lời thoại. Liên hệ nằm ở **caption**. Frame cuối là câu chốt giá trị / lời mời nhắn tin.
→ **Nới 25/07/2026:** logo, watermark, hotline **lỡ có sẵn trong ảnh chụp thật thì không sao** — mọi ảnh workspace đều dùng được, không cần crop, không loại ảnh. Luật chỉ áp cho thứ mình chủ động thêm vào.

**2. Không bịa số MÌNH ĐƯA LÊN.**
Mọi con số mình gõ lên hình hoặc đọc trong lời thoại phải có sẵn trong `03-knowledge/products.json` · `pricing.json` · `proof-points.json`. Không có → bổ sung vào knowledge base trước. Không tự suy ra, không làm tròn cho đẹp. (Số/giá nằm sẵn trong ảnh chụp là cảnh thật, không tính.)

**3. Gọi "robot phục vụ", không nói tên model.**
Người xem chưa biết "BellaBot", "KettyBot"… Trên hình và trong lời đọc luôn dùng tên chung **"robot phục vụ"** / **"robot phục vụ nhà hàng"**. Chỉ nói tên model khi được yêu cầu làm video giới thiệu đúng sản phẩm đó.

**4. Chữ ở GIỮA khung, không ở đáy.**
Nền tảng phủ UI lên ~1/4 đáy + ~12% đỉnh màn hình. Dùng `"align": "center"` hoặc `"safe"` trong `scenes.json` cho chữ quan trọng, tránh `"bottom"`.

**5. Tôn trọng chuyên môn người xem.**
Chủ nhà hàng rất giỏi bài toán đầu tư. Đi theo **phân tích logic**, khơi gợi mong muốn đầu tư khéo léo, không dạy đời, không bán hàng lộ liễu. Chi tiết + hai chủ thể khai thác (nhân viên, quản lý) trong `references/luat-kich-ban.md`.

**Hotline duy nhất khi cần (chỉ ở caption): `0866 153 946`.**

---

## Chuẩn kỹ thuật

| | |
|---|---|
| Khổ hình | 1080×1920 dọc, 30fps, H.264 |
| Thời lượng | 20–75 giây |
| Nền mặc định | tối gần đen `#0b0605` + vệt sáng đỏ tụ giữa-dưới (đã có sẵn trong `build-frame.py`) |
| Font | tiêu đề **Neusharp IN HOA**, còn lại **Britti Sans**. Không dùng font thứ ba. |
| Đỏ nhấn | `#E83636` |

---

## Bảy bước

### B1 — Brief

Tạo thư mục `04-video-projects/NNN-ten-video/` (số thứ tự tiếp theo). Điền `brief.md` theo `04-video-projects/_template/brief.md`.

**Làm trước tiên, trước cả khi viết chữ nào:**

- Video có nêu **giá** không? Nếu có → mở `03-knowledge/pricing.json`, đọc khoá `_meta.canh_bao`. Báo giá có hạn hiệu lực. **Nếu đã quá hạn, hỏi người dùng xác nhận giá mới trước khi viết kịch bản** — không phải trước khi render. Sai giá thì cả kịch bản phải viết lại.
- Giá thuê: `pricing.json` tự ghi cảnh báo ánh xạ giá ↔ dòng robot **chưa xác nhận**. Không đưa lên hình cho tới khi người dùng xác nhận.
- **Video nói về một model cụ thể? Kiểm ảnh model đó CÓ DÙNG ĐƯỢC KHÔNG, ngay bây giờ:**
  ```powershell
  python tools\prep-assets.py 02-media\images\products --kiem
  ```
  Ảnh cạnh ngắn <1080px là loại. Đã mất một vòng viết kịch bản + sinh giọng vì viết cho KettyBot Pro rồi mới phát hiện ảnh duy nhất chỉ 400×400 (LESSONS 24/07). **Không có ảnh đúng model thì đổi model theo ảnh, đừng chiếu hình máy khác** — đọc thông số máy này mà hiện hình máy kia là sai lệch, dù không con số nào bịa.

Chốt trong brief: **một câu duy nhất** người xem phải nhớ. Chưa chốt được câu đó thì chưa viết kịch bản.

### B2 — Kịch bản → ═══ CHỐT 1 ═══

Đọc `references/luat-kich-ban.md` **và `03-knowledge/van-mau-anh-truong.md`** (văn phong thật của anh) **trước khi viết**. Đây là chỗ sai đắt nhất và cũng rẻ nhất để sửa.

Xuất **hai file**:
- `kich-ban.txt` — bản đầy đủ, có tên phân cảnh, ghi chú `[trong ngoặc vuông]`, số viết bằng chữ số ("80%")
- `loi-doc.txt` — **chỉ lời thoại**, bỏ hết tiêu đề phân cảnh và ghi chú, **số viết bằng chữ** ("tám mươi phần trăm")

**Dừng lại. Đưa kịch bản cho người dùng duyệt.** Không tự đi làm bước 3.

### B3 — Giọng đọc + mốc timeline

```powershell
cd D:\RBW_Claude\tools\elevenlabs
python doc-kich-ban.py --file ..\..\04-video-projects\NNN-ten\loi-doc.txt NNN-ten
```
File ra: `05-output/voice/NNN-ten.mp3`. Model mặc định `eleven_v3` — **không đổi sang** `eleven_multilingual_v2` / `eleven_turbo_v2` / `eleven_flash_v2`, ba model đó không có tiếng Việt.

Đo độ dài thật và lấy mốc ngắt câu — xem `references/lenh-render.md`. **Giọng quyết định timeline**, không phải ngược lại: viết `scenes.json` theo mốc đo được từ mp3.

### B4 — Ảnh (chạy song song với B3)

Giao cho subagent **`rbw-research`**. Đưa nó: đường dẫn dự án, `kich-ban.txt`, và danh sách cảnh cần ảnh kèm mô tả cụ thể từng cảnh.

Nó trả về `assets/*.jpg` đã đúng 1080×1920 + `assets/NGUON.md`. Đọc `references/luat-hinh-anh.md` để biết cần bao nhiêu ảnh và loại nào.

### B5 — scenes.json

Đọc `references/schema-scenes.md` (schema + danh mục class) và `references/luat-hinh-anh.md` (luật bố cục).

Ghi `scenes.json` trong thư mục dự án. Bốn luật bố cục quan trọng nhất:
1. **Không để chữ đứng một mình** — scene chỉ có chữ thì scene ngay sau phải là hình hoặc biểu đồ
2. **Hình là chủ đạo** — dùng liên tiếp 2–3 scene hình, không chỉ một scene lẻ
3. **Số liệu quan trọng → biểu đồ**, không chỉ chữ to
4. **Không lặp ảnh ở hai scene liền kề**

### B6 — Render nháp → render thật

```powershell
cd D:\RBW_Claude
python tools\make-video.py 04-video-projects\NNN-ten --nhap
```
Bản nháp 540×960 để duyệt **thứ tự hình và nhịp**. Xem lại, sửa `scenes.json` nếu lệch — sai ở bước này vứt đi không tiếc.

Nhịp đạt rồi mới render thật:
```powershell
python tools\make-video.py 04-video-projects\NNN-ten
```

### B7 — QC → ═══ CHỐT 2 ═══

Giao cho subagent **`rbw-qc`**. Nó chỉ đọc, không sửa — đó là chủ ý, để nó không tự đi vá rồi báo PASS.

- **PASS** → đưa video + caption cho người dùng duyệt
- **FAIL** → sửa `scenes.json` theo đúng danh sách lỗi nó trả về, render lại, gọi QC lần nữa. **Tối đa 2 vòng.** Vòng thứ 3 vẫn FAIL thì dừng, báo người dùng — lúc đó là vấn đề tư liệu hoặc kịch bản, không phải vấn đề dựng.

⚠️ **Vòng QC thứ hai phải kiểm lại ĐỦ 8 mục, không chỉ 6 chỗ vừa sửa.** Sửa chỗ này làm lộ chỗ khác: ở video 003, việc đổi chỗ hai ảnh đã đẩy một ảnh có thương hiệu bên thứ ba vào scene dễ thấy hơn, và lỗi đó chỉ bị bắt ở vòng 2.

**Nhớ cập nhật `assets/NGUON.md`** khi thay ảnh — đó là hồ sơ truy vết bản quyền và cách xử lý từng ảnh, QC sẽ đối chiếu.

Viết `README.md` cho dự án theo khuôn của `001-noi-dau-be-bung/README.md`: thành phẩm, bảng phân cảnh, nguồn ảnh, lệnh dựng lại, caption.

**Caption** — viết bằng giọng anh Trường theo `03-knowledge/van-mau-anh-truong.md` (xưng em, gọi anh chị; mục 5
có caption anh tự viết khi đã được bổ sung — bám theo đó trước). Chủ nhà hàng chỉ cần **1 câu punch** đủ dừng ngón tay. Bản dài (hook + proof + CTA + hashtag) là tuỳ chọn, hỏi người dùng muốn bản nào. Hotline chỉ ở đây.

### B8 — Ghi nhận sau khi người dùng nhận xét

Người dùng nhận xét xong → **cập nhật ngay**, đừng để lần sau nhớ lại:
- `04-video-projects/LESSONS.md` — thêm mục mới **lên đầu**, ghi ngày, việc, kết quả, cách khắc phục
- Nếu là luật mới lặp lại được → thêm thẳng vào `references/luat-kich-ban.md` hoặc `references/luat-hinh-anh.md` của skill này

Đây là cơ chế cải tiến: video sau chạy trên bộ luật dày hơn video trước.

---

## Tham chiếu

| File | Nội dung |
|---|---|
| `references/luat-kich-ban.md` | Cách viết lời thoại. Đọc TRƯỚC B2. |
| `references/luat-hinh-anh.md` | Luật bố cục hình + checklist kiểm scene. Đọc TRƯỚC B5. |
| `references/schema-scenes.md` | Schema `scenes.json` + danh mục class + ví dụ đã duyệt. |
| `references/lenh-render.md` | Lệnh chuẩn, cách đo timeline, các bẫy đã gặp. |
| `04-video-projects/LESSONS.md` | Nhật ký đầy đủ. Đọc khi gặp lỗi lạ. |
| `03-knowledge/brand-voice.md` | Giọng điệu thương hiệu. |

## Khi người dùng chỉ muốn sửa một phần

| Yêu cầu | Làm gì |
|---|---|
| Đổi nhạc nền | Thay `nhac` trong `scenes.json` → `python tools\make-video.py <du-an> --chi-nhac` (không render lại) |
| Sửa một câu chữ | Sửa `scenes.json` → render lại. Giọng không đổi thì **không** sinh giọng lại. |
| Sửa lời thoại | Sửa `loi-doc.txt` → sinh giọng lại → **đo lại mốc timeline** → sửa `scenes.json` cho khớp → render |
| Đổi một ảnh | `python tools\prep-assets.py <anh> --ra <du-an>\assets --ten <ten>` → sửa `scenes.json` → render |

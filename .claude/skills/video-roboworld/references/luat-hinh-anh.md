# Luật hình ảnh & bố cục scene

> Mục tiêu duy nhất: **người xem thấy cảnh thật để liên tưởng vào quán của mình.**
> Video không được là "chữ chạy trên nền đen".

## Bốn luật bố cục

**1. Không để chữ đứng một mình.**
Một scene chỉ có chữ thì scene **ngay sau** phải là ảnh minh hoạ hoặc biểu đồ/số liệu. Không bao giờ hai scene chữ-trơn liền nhau.

**2. Hình là chủ đạo.**
Scene dùng hình phải để hình chiếm phần lớn khung. Dùng **liên tiếp 2–3 scene** hình, không rải một scene hình lẻ giữa toàn chữ.

**3. Số liệu quan trọng → biểu đồ.**
Con số then chốt (phần trăm, ROI, so sánh trước/sau) dựng thành đồ hoạ dữ liệu, không chỉ chữ to. `build-frame.py` có sẵn `donut`. Cần dạng khác (cột, thanh so sánh) thì dựng bằng div/SVG trong `lines[].text`.

**4. Không lặp ảnh — và kiểm bằng MẮT, không bằng tên file.**
Video 001 dùng 17 ảnh cho 15 scene, không ảnh nào lặp liền nhau.
⚠️ Khi tái dùng ảnh từ dự án cũ, **`Read` từng ảnh trước khi copy**. Ở video 007, `002/p6-team-robot-that.jpg` và `003/p6-robot-that-01.jpg` hoá ra là ảnh đã có sẵn trong `02-media/personal/` dưới tên khác — cùng một ảnh Gogi House suýt lên hình 3 lần. Tên file khác nhau không có nghĩa ảnh khác nhau.

---

## Nguồn ảnh, theo thứ tự ưu tiên

**1. `02-media/` — ảnh thật của công ty.** Xem `03-knowledge/media-index.md` để biết ảnh nào chụp gì.
- `images/products/` — studio, key visual, sơ đồ kỹ thuật
- `images/deployments/` — triển khai thật tại khách hàng ⚠️ nhiều ảnh có dải watermark "ROBOWORLD" phía trên
- `images/personal/` — ảnh anh Trường, dùng cho frame "người bán"

Ảnh **người Việt + robot thật** luôn mạnh hơn ảnh stock. Video 001 dùng ảnh team Roboworld ở Hội An cho phần Golden Gate, hiệu quả hơn hẳn ảnh stock.

**2. Ảnh stock miễn phí thương mại** khi workspace không có: Pexels, Pixabay, Unsplash. Không cần ghi nguồn, nhưng vẫn lưu link vào `assets/NGUON.md`.

Cách tải Pexels đã chạy được:
```
WebFetch trang tìm kiếm Pexels → lấy URL trực tiếp https://images.pexels.com/photos/<id>/....jpeg
→ Invoke-WebRequest, thêm ?auto=compress&cs=tinysrgb&w=1280
```
⚠️ Trong PowerShell, URL có `&` **phải nối bằng biến**, không viết thẳng trong ngoặc kép:
```powershell
$full = $u + '?auto=compress' + '&' + 'cs=tinysrgb' + '&' + 'w=1280'
```
Không làm vậy sẽ báo *"hostname could not be parsed"*.

---

## Hai thứ phải kiểm ở MỌI ảnh trước khi dùng

**1. Đúng khổ 1080×1920 chưa?** Mọi ảnh phải qua:
```powershell
python tools\prep-assets.py <anh> --ra <du-an>\assets --ten <ten-scene>
python tools\prep-assets.py <thu-muc> --kiem      # chỉ báo cáo, chưa xuất
```

**2. Đủ lớn không?** Cạnh ngắn phải ≥ 1080. `prep-assets.py` tự loại ảnh nhỏ hơn — đừng phóng lên, sẽ vỡ.

## Logo & watermark trong ảnh — KHÔNG còn phải né (cập nhật 25/07/2026)

Anh Trường đã chốt: **mọi ảnh trong workspace đều dùng được.** Logo trên thân robot, watermark "ROBOWORLD", logo bên thứ ba, hotline lỡ chụp vào ảnh — **tất cả đều không sao**, không cần crop, không cần loại ảnh.

Hai điều CẤM giờ chỉ áp cho thứ **mình chủ động thêm vào**: không tự đặt logo dạng đồ hoạ, không tự gõ số điện thoại thành chữ, không đọc số điện thoại trong lời thoại.

Vẫn nên crop khi ảnh xấu vì lý do **thẩm mỹ** (watermark dày che chủ thể, thương hiệu bên thứ ba to lấn át robot làm loãng thông điệp) — nhưng đó là lựa chọn chất lượng, không phải luật bắt buộc. `prep-assets.py` vẫn có `--cat-tren/duoi/trai/phai` khi cần.

---

## Video nền

`scenes.json` hỗ trợ field `video` thay cho `image`. Nhưng:

⚠️ **Tính đến 24/07/2026, mọi clip robot trong `02-media/san-pham/<model>/video/` đều dính logo hoặc text overlay** — PUDU góc trên-trái, watermark "Duy Trường Robot" ở `02-media/video-mau-social/`. Chưa dùng làm nền được.

Thay thế đang dùng: **ảnh + zoom chậm (Ken Burns)** qua field `zoom`. Hiệu quả gần bằng, sạch logo.

Muốn nền động thật → xin anh Trường quay clip không có overlay.

---

## Vị trí chữ — GIỮA khung, không ở đáy (quan trọng)

Đăng lên TikTok/Reels/Shorts, nền tảng phủ UI của nó lên **~1/4 đáy màn hình** (caption, tên kênh, nút tim/bình luận/chia sẻ) và **~12% đỉnh**. Chữ đặt ở đáy bị che mất — đã gặp thật ở video 001.

- Dùng **`"align": "center"`** cho hầu hết scene — an toàn cả trên lẫn dưới.
- Dùng **`"align": "safe"`** khi muốn chữ hơi thấp mà vẫn tránh vùng bị che (chừa đáy 430px, đỉnh 240px).
- **Tránh `"align": "bottom"`** cho chữ quan trọng.

## Chữ trên nền ảnh

Chữ đỏ `#E83636` đặt trên vùng ảnh sáng **bị chìm**. Cách xử lý:
- Tăng `shade` (lớp phủ tối) ở scene đó — dải 0.55–0.85. Ảnh càng sáng, `shade` càng cao.
- `.shade` trong `build-frame.py` đã phủ đậm hơn ở giữa khung, nơi chữ nằm.
- Mọi cấp chữ đã có sẵn `text-shadow`.

---

## Checklist bắt buộc — kiểm sau MỖI scene

Render bản nháp xong, **screenshot từng scene và tự kiểm** trước khi sang scene sau:

- [ ] Chữ khớp với giọng đọc và nội dung scene
- [ ] Hình cân đối trong khung, không méo, chủ thể không bị chữ che
- [ ] Nếu ảnh có **robot**: đủ bối cảnh, thấy rõ con robot — không cắt cụt, không quá nhỏ
- [ ] Nếu ảnh **minh hoạ**: đúng với nội dung câu đang nói
- [ ] Chữ đọc được — tương phản đủ trên nền ảnh
- [ ] **Không logo, không số điện thoại** trên frame

Chưa đạt thì sửa ngay, chưa sang scene sau.

---

## Chuyển cảnh

`build-frame.py` đã xử lý sẵn **cross-fade**: mỗi scene bắt đầu hiện sớm 0,4s, đè lên scene trước. Không còn nháy đen ở điểm đổi ảnh. Đừng sửa lại phần này trừ khi có lý do rõ.

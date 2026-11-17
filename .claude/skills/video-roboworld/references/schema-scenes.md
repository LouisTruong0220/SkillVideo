# Schema `scenes.json`

File này là **bản thiết kế toàn bộ video**. `tools/build-frame.py` đọc nó, sinh ra HTML tự chứa (font + ảnh nhúng base64), rồi `tools/render-video.mjs` ghi hình thành MP4.

## Khung ngoài cùng

```json
{
  "title": "Tên video (chỉ để đọc)",
  "duration": 60.0,

  "giong": "05-output/voice/002-roi.mp3",
  "nhac": "assets/nhac-nen.mp3",
  "nhac_am_luong": 0.16,
  "lead_in": 0.2,
  "ra": "05-output/002-roi.mp4",

  "scenes": [ ... ]
}
```

| Khoá | Bắt buộc | Ý nghĩa |
|---|---|---|
| `duration` | ✔ | Tổng giây. Phải khớp độ dài file giọng (±0,5s). |
| `giong` | | Đường dẫn **từ gốc dự án** `D:\RBW_Claude`. |
| `nhac` | | Đường dẫn **từ thư mục dự án**. |
| `nhac_am_luong` | | Mặc định `0.16`. Nhạc to hơn sẽ át giọng. |
| `lead_in` | | Giọng vào chậm hơn hình bao nhiêu giây. Video 001 dùng `0.2`. |
| `ra` | | Đường dẫn MP4 xuất, từ gốc dự án. Bỏ trống thì mặc định `05-output/<tên-thư-mục>.mp4`. |

`build-frame.py` chỉ đọc `title` / `duration` / `scenes`, bỏ qua các khoá còn lại — nên thêm khoá mới vào đây là an toàn.

## Một scene

```json
{
  "start": 8.5,
  "end": 14.3,
  "align": "bottom",
  "image": "assets/p2-nhan-vien-phuc-vu.jpg",
  "shade": 0.62,
  "zoom": 1.1,
  "lines": [
    { "class": "kicker", "text": "Cho em hỏi thật", "delay": 0.3 },
    { "class": "mid", "text": "Nhân viên của anh chị<br>đang dành sức<br><span class=\"hl\">cho việc gì?</span>", "delay": 0.9 }
  ]
}
```

| Khoá | Mặc định | Ý nghĩa |
|---|---|---|
| `start` / `end` | — | Giây. **Phải liền mạch, không hở, không chồng.** `end` scene này = `start` scene sau. |
| `align` | `center` | `center` chữ giữa khung · `bottom` chữ dưới đáy (dùng khi có ảnh) |
| `image` | — | Ảnh nền, đường dẫn **từ thư mục dự án**. |
| `video` | — | Clip nền thay cho ảnh. ⚠️ Xem cảnh báo logo trong `luat-hinh-anh.md`. |
| `loop` | `true` | Chỉ áp cho `video`. |
| `shade` | `0.62` | Độ phủ tối lên ảnh, 0–1. Ảnh sáng thì tăng lên 0.8+, không thì chữ chìm. |
| `zoom` | `1.10` | Ken Burns: ảnh phóng dần từ 1 đến giá trị này trong suốt scene. |
| `lines` | `[]` | Các lớp chữ, hiện lần lượt. |

## Một dòng chữ trong `lines`

```json
{ "class": "mid", "text": "...", "delay": 0.9, "style": "text-align:center" }
```

- `delay` — giây tính **từ `start` của scene**, không phải từ đầu video
- `text` — cho phép HTML: `<br>` xuống dòng, `<span class="hl">…</span>` tô đỏ
- `style` — CSS inline, dùng khi cần căn giữa riêng một dòng

### Danh mục class có sẵn

| Class | Font | Cỡ | Dùng cho |
|---|---|---|---|
| `kicker` | Britti Bold | 34px | Nhãn nhỏ IN HOA đỏ, mở đầu scene |
| `big` | Neusharp | 136px | Tiêu đề lớn nhất, IN HOA |
| `mid` | Neusharp | 92px | Tiêu đề vừa — **dùng nhiều nhất** |
| `body` | Britti | 46px | Câu văn thường |
| `small` | Britti Light | 34px | Chú thích, nguồn |
| `num` | Neusharp | 230px | Con số khổng lồ, màu đỏ |
| `rule` | — | — | Gạch ngang đỏ 132×8px, ngăn khối |

Class phụ dùng trong `text`:
- `hl` — tô đỏ `#E83636` một cụm từ

### Biểu đồ vòng (donut)

Thay `class` bằng `donut`:

```json
{ "donut": 80, "text": "80%", "delay": 0.2 }
```

`donut` là phần trăm 0–100 (vòng đỏ chạy tới đó), `text` là chữ hiện giữa vòng. Vòng tự vẽ bằng SVG, có hiệu ứng chạy 1,1 giây.

---

## Hai ví dụ đã duyệt (chép từ video 001)

**Scene ảnh + chữ dưới đáy:**
```json
{ "start": 0.0, "end": 5.0, "align": "bottom",
  "image": "assets/p1-mon-an-1.jpg", "shade": 0.55, "zoom": 1.1,
  "lines": [
    { "class": "kicker", "text": "Gửi các chủ nhà hàng", "delay": 0.3 },
    { "class": "mid", "text": "Menu hấp dẫn.<br>Quảng cáo.<br>Giảm giá.", "delay": 0.8 }
  ] }
```

**Scene biểu đồ, không ảnh nền:**
```json
{ "start": 25.4, "end": 31.0, "align": "center",
  "lines": [
    { "donut": 80, "text": "80%", "delay": 0.2 },
    { "class": "mid", "text": "thời gian một ca", "delay": 1.6, "style": "text-align:center" },
    { "class": "body", "text": "chỉ để <span class=\"hl\">đi lại, bưng bê</span> từ bàn này sang bàn kia.", "delay": 2.2, "style": "text-align:center" }
  ] }
```

---

## Bảy lỗi hay gặp

1. **`end` scene này ≠ `start` scene sau** → hở khung đen, hoặc scene chồng nhau
2. **`duration` không khớp độ dài mp3** → giọng bị cắt cụt, hoặc video im lặng ở cuối
3. **`delay` tính từ đầu video** thay vì từ `start` scene → chữ hiện sai lúc
4. **Đường dẫn ảnh tính từ gốc dự án** thay vì từ thư mục dự án → `make-video.py` báo thiếu tư liệu
5. **`shade` quá thấp trên ảnh sáng** → chữ đỏ chìm, không đọc được
6. **Nháy chữ:** đặt quá nhiều `lines` trong scene ngắn — mỗi dòng cần ≥0,4s để hiện xong
7. **Quên escape dấu ngoặc kép** trong `text` khi dùng `<span class=\"hl\">`
8. **Rớt âm tiết lẻ** — dòng `mid` dài quá tự xuống dòng, để lại một chữ đứng trơ ("TÍP", "THỨ", "MÌNH"). Xem mục dưới.

## Ngưỡng ký tự mỗi dòng (đo ở video 008)

`mid` (Neusharp 92px, khung 1080) chứa được **tối đa ~15 ký tự/dòng**. Quá là tự wrap và rớt chữ lẻ.

| Vừa | Tràn |
|---|---|
| `HỎI Ý NHÂN VIÊN` (15) | `Bạn ấy thấy mình` (16) → rớt "MÌNH" |
| `TRƯỚC, HAY CHO` (14) | `Nỗi lo của các bạn` (18) → rớt "BẠN" |
| `CHÍNH BẠN CHÊ` (13) | `Anh chủ đứng nhìn,` (18) → rớt "NHÌN," |

⚠️ **Đếm ký tự thôi chưa đủ — phải tính bề rộng.** Dấu gạch ngang dài `—` rộng hơn dấu phẩy đáng kể: `trước — hay cho` (15) vẫn tràn, đổi thành `trước, hay cho` (14) mới vừa.

**Cách làm:** chủ động đặt `<br>` chia dòng ≤14 ký tự ngay từ đầu, đừng để trình duyệt tự wrap. Sau bản nháp, trích `tools/anh-scene.py` và soi **từng scene có chữ `mid`** — lỗi này chỉ thấy bằng mắt, không script nào bắt được.

# Brief — <TÊN VIDEO>

> Copy cả thư mục `_template/` thành `NNN-ten-video/` rồi điền vào đây.
> Chưa điền xong brief thì chưa viết storyboard.

## 1. Mục tiêu

- **Video này để làm gì?** (kéo inbox / hâm nóng khách cũ / gửi kèm báo giá / chạy quảng cáo)
- **Người xem là ai?** (chủ chuỗi lẩu nướng 5–20 chi nhánh / quản lý vận hành / chủ quán cà phê mới mở)
- **Xem xong họ làm gì?** (nhắn fanpage / gọi hotline / đồng ý cho khảo sát)

## 2. Thông số kỹ thuật

| | |
|---|---|
| Khổ hình | `9:16` dọc / `16:9` ngang / `1:1` |
| Độ phân giải | 1080×1920 / 1920×1080 |
| Thời lượng mục tiêu | ... giây |
| Nơi đăng | TikTok / Reels / YouTube / gửi Zalo cho khách |
| Có tiếng nói? | Không / Voice-over / Phụ đề cứng |

## 3. Sản phẩm nói tới

- Dòng chính: `bellabot-pro` / `bellabot` / `pudubot-2` / `kettybot-pro` / `greetingbot-nova`
- Có nêu giá không? → nếu **có**, kiểm tra hiệu lực trong `03-knowledge/pricing.json` **trước khi dựng**

## 4. Thông điệp

- **Một câu duy nhất** người xem phải nhớ:
- Nỗi đau mở đầu:
- Bằng chứng dùng (chép từ `03-knowledge/proof-points.json`, ghi rõ con số + nguồn):
  - [ ] ...
  - [ ] ...

## 5. Tư liệu sử dụng

Chọn từ `03-knowledge/media-index.md`, ghi đường dẫn đầy đủ:

- Ảnh: `02-media/san-pham/<model>/anh-studio|anh-thuc-te/...`
- Video: `02-media/san-pham/<model>/video/...`
- Ảnh cá nhân (nếu cần mặt người bán): `02-media/cong-ty/duy-truong/...`

## 6. Template html-video dự kiến

Chạy `node tools/html-video/packages/cli/dist/bin.js search-templates --intent "..." --top 5` rồi ghi id vào đây:

- Template:
- Lý do chọn:

## 7. Voice-over

- [ ] Có voice-over không? Nếu có, viết kịch bản vào `kich-ban.txt` cùng thư mục
- [ ] Số đã viết bằng chữ chưa? (`155.000.000` → "một trăm năm mươi lăm triệu")
- [ ] Sinh giọng: `python tools/elevenlabs/doc-kich-ban.py --file kich-ban.txt <ten-file>`

## 8. Checklist trước khi render

**Hai điều CẤM — kiểm tra đầu tiên:**
- [ ] **KHÔNG có logo nào** trên bất kỳ frame nào (Roboworld / Duy Trường Robot / PUDU)
- [ ] **KHÔNG có số điện thoại** trên hình

Còn lại:
- [ ] Mọi con số trên hình đều có trong `products.json` hoặc `proof-points.json`
- [ ] Giá (nếu có) còn hiệu lực
- [ ] Màu dùng đúng token trong `00-brand/brand-tokens.css`
- [ ] Tiêu đề dùng font Neusharp IN HOA, phần còn lại dùng Britti Sans
- [ ] Frame cuối là **câu chốt giá trị / lời mời nhắn tin**, không phải frame liên hệ
- [ ] Chữ đủ to để đọc trên màn hình điện thoại
- [ ] Không dùng ảnh/logo khách hàng ngoài danh sách trong `02-media/san-pham/<model>/anh-thuc-te/`

## 9. Caption đăng bài

Thông tin liên hệ nằm ở đây, không lên hình:

```
<nội dung caption>

📞 0866 153 946
Duy Trường Robot — Robot phục vụ nhà hàng
```

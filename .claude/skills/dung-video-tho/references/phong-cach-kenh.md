# Phong cách kênh Duy Trường Robot (B4–B5)

Rút từ 7 video mẫu `01-source-data/_ban-goc-anh-Truong/video/video-mau-social/` (soi 15/11/2026), lọc qua luật
thương hiệu hiện hành. Video mẫu được dựng bằng CapCut; bộ công cụ này tái tạo cùng ngôn ngữ hình ảnh.

## Những gì video mẫu làm — và mình làm theo

| Video mẫu | Trong `dung.json` |
|---|---|
| Anh Trường đứng cạnh robot, quay toàn thân / nửa người, nói thẳng vào máy | nền: bản cắt `da-cat.mp4` |
| Phụ đề 2–4 chữ, chữ trắng viền đen đậm, 1 từ khoá vàng (đôi khi đỏ), đặt ngang ngực | `phu-de.txt` + `*từ*` (mặc định) |
| Chữ to bật lên ở ý chính: "2 mặt sàn", "MỖI TẦNG 1 ROBOT", "LÍ DO THỨ 2", "10 suất demo miễn phí" | `tieu-de` |
| Tiêu đề hook đầu video đỏ + trắng: "ROBOT LỄ TÂN AI / Trong Hành Chính Công" | `mo-dau` |
| Cắt sang cận robot / khay đồ ăn / màn hình khi anh nhắc tới | `canh-phu` `toan-man` |
| Nửa trên clip hãng, nửa dưới anh Trường nói | `canh-phu` `nua-tren` |
| Khung giao diện bật lên (hộp thoại Windows) khi kể quy trình | `cua-so` |
| Logo nhà hàng khách (Vũ Cẩm) bật lên cạnh người nói | `dan` |
| Tách người đặt lên nền bản vẽ mặt bằng "từ 150–200 m²" | chưa có khối tách người → dùng `mo-phong` / `bieu-do` nửa trên |

## Những gì video mẫu làm — mà KHÔNG làm nữa

- Logo "DUY TRƯỜNG ROBOT" cố định ở đỉnh khung suốt video → bỏ (luật 1).
- Khung kết logo + điện thoại + email → bỏ. Kết bằng câu chốt / lời mời của chính anh Trường.
- Tiêu đề tên model ("BELLABOT" to giữa khung) → đổi thành "ROBOT PHỤC VỤ", trừ video giới thiệu đúng model đó.

## Mật độ và nhịp (video 45–75 s)

| Thứ | Bao nhiêu | Ghi chú |
|---|---|---|
| Phụ đề | suốt video | ~1/3 số cụm có từ nhấn; nhấn số, lợi ích, tên ý — không nhấn hư từ |
| Móc câu | 1 `mo-dau` 2–3 s đầu | ≤ 6 chữ dòng 1; dòng 2 nói rõ cho ai / ở đâu |
| Tiêu đề bật | 1 mỗi 6–10 s | 2–5 chữ, đúng lúc anh nói chữ đó (đặt `t` = mốc chữ trong `tu-moi.json`) |
| Đổi hình (cảnh phụ, mô phỏng, biểu đồ, cửa sổ) | 1 mỗi 5–8 s | mặt anh Trường vẫn trên hình ≥ 60% thời lượng — kênh cá nhân, khách theo dõi NGƯỜI |
| Phóng to | 1–2 mỗi 15 s | ở câu chốt / con số, 1,25–1,35× |
| Hiệu ứng âm | mỗi lần hình mới xuất hiện | KHÔNG gắn âm vào phụ đề; tối đa ~1 âm / 2 s |

Luật cũ của `04-video-projects/LESSONS.md` vẫn đúng: **số liệu quan trọng → biểu đồ / thẻ số**, không chỉ chữ to;
**cảnh phụ phải khớp đúng câu đang nói** (nói "khay" thì hiện khay); **mở cảnh ra xem trước khi dùng**.

## Chọn khối theo điều anh Trường đang nói

| Anh đang nói | Khối |
|---|---|
| Con số: "lên tới 98%", "400 câu mỗi ngày", "10 suất" | `the-so` |
| So sánh hai thứ: nhân viên vs robot, trước vs sau | `bieu-do` (số phải có nguồn) |
| Robot đi thế nào, phục vụ mấy bàn, mấy tầng, lối đi | `mo-phong` |
| Thao tác trên màn hình / app / thủ tục / lời mời đăng ký | `cua-so` |
| Tên nhà hàng / khách hàng | `dan` (logo khách — chỉ khi có ảnh logo thật trong workspace) |
| Ý chính một câu | `tieu-de` |
| Thứ nhìn thấy được: robot chạy, khay, màn hình, khách | `canh-phu` |

## Kho cảnh thật đã soi (cập nhật 16/11/2026)

Cảnh quay thật luôn hơn đồ hoạ khi người nói nhắc tới robot / ứng dụng. Mọi đoạn mới lấy từ kho: soi từng 0,2 s.

| Cảnh | File · đoạn dùng được | Ghi chú |
|---|---|---|
| **Nova dẫn người đi qua văn phòng Roboworld** | `02-media/video-mau-social/05-robot-le-tan-hanh-chinh-cong-79s.mp4` · **46,6–50,1 s** + **51,35–52,35 s** | Roboworld tự quay. 44–46,5 s và từ 53 s có phụ đề cháy sẵn; 50,1–51,3 s chỉ thấy lưng người rồi lia bàn ghế trống. Dùng ở video 012 (toàn màn) |
| Nova — màn hình ứng dụng, tay bấm | clip quay kèm video 012 (`04-video-projects/012-robot-le-tan/assets/canh-01.mp4`) | lộ tên app dự án khách (Vinpearl, Mường Thanh…) — cảnh thật, báo anh biết |
| Ảnh app Roboworld tự làm | `11-app-nova/<app>/demo/anh-soi/*.png` (vd `nhan-dien-khuon-mat/…/02-m1-quen.png`, `hcc-van-phong/…/02g-so-da-in.png`) | 1920×1080 ngang → cắt vùng nội dung, đặt vào 1080×960, giữ chữ trong x ≤ 900. Ảnh lỗi (02e "chưa nối máy in") đừng dùng |
| Nova ở ngân hàng MSB | `02-media/san-pham/greetingbot-nova/video/greetingbot-nova-ngan-hang-msb-126s-doc.mp4` | **chưa dùng**: clip TikTok của người khác (watermark), logo MSB, kho không ghi là dự án Roboworld — hỏi anh trước |
| Nova ở bệnh viện (phóng sự THVL1) | `…/greetingbot-nova-benh-vien-gia-dinh-thvl1.mp4` | khung ngang 848×480, logo đài — kém, hỏi anh trước |
| Phim hãng OrionStar | `…/greetingbot-nova-office-reception.mp4`, `…shopping-guide-thailand.mp4` | phụ đề Anh + watermark ORIONSTAR — không gọi là "thực tế" |

Thêm bản ghi mới vào bảng này mỗi khi soi được cảnh thật dùng tốt.

## Màu chữ

Trắng + viền đen (mặc định), vàng `#FFD43B` nhấn, đỏ `#E83636` thương hiệu. Font: **Neusharp IN HOA** cho tiêu đề,
**Britti** cho phụ đề/chữ thường. Không font thứ ba.

## Nhạc nền

Chỉ dùng `02-media/am-thanh/nhac-nen-video-mau/` (tách bằng Demucs từ 7 video mẫu). Đọc `muc-luc.json`:
`doan_sach` đã bỏ 3,5 s cuối (tiếng vút đoạn logo kết). Gợi ý: **01** và **03** nhịp đều, sạch nhất; **06** dài 99 s
cho video > 60 s; tránh **04** (có đoạn chói). Mức mặc định thấp hơn giọng 11 dB (`duoi_giong_db`) — đúng mức
trung vị đo trong video mẫu; nhạc tự nhỏ thêm khi anh nói (ducking).
⚠ Nhạc tách vẫn lẫn chút tiếng ồn hiện trường của video gốc — nghe thấy rõ thì đổi bản.

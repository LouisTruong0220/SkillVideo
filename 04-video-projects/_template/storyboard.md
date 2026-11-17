# Storyboard — <TÊN VIDEO>

Mỗi frame = một file HTML trong `frames/`. Render xong ghép lại thành MP4.

| # | File | Giây | Nội dung trên hình | Tư liệu | Ghi chú động |
|---|---|---|---|---|---|
| 1 | `frames/01-hook.html` | 0–3 | Câu hook | | fade in, chữ trượt lên |
| 2 | `frames/02-noi-dau.html` | 3–8 | Con số nỗi đau | | số đếm tăng dần |
| 3 | `frames/03-giai-phap.html` | 8–14 | Robot chạy thật | video ... | cắt cảnh |
| 4 | `frames/04-so-sanh.html` | 14–22 | Bảng trước/sau | proof-points | cột trượt vào |
| 5 | `frames/05-bang-chung.html` | 22–27 | 200+ nhà hàng Golden Gate | ảnh ... | |
| 6 | `frames/06-chot.html` | 27–30 | Câu chốt / lời mời nhắn tin — **KHÔNG logo, KHÔNG số điện thoại** | | |

## Lời thoại / phụ đề

```
Frame 1:
Frame 2:
...
```

## Quy tắc dựng frame

**Nền tối (mặc định thương hiệu)** — dùng class `.rbw-stage`, chữ trắng, nhấn `--rbw-signal-red`.
**Nền sáng** — dùng `.rbw-stage-light` cho frame bảng số liệu / so sánh cho dễ đọc.

Cấu trúc chữ chuẩn một frame:
```
KICKER nhỏ IN HOA đỏ      ← .rbw-kicker
TIÊU ĐỀ LỚN NEUSHARP      ← .rbw-title
tagline đỏ nghiêng         ← .rbw-tagline
body Britti Sans           ← mặc định
```

**Thời lượng:** mỗi frame tối thiểu 2.5s để người xem kịp đọc. Frame có bảng số cần 5–8s.

**Chuyển cảnh:** html-video ghi từng frame riêng rồi ghép — chuyển cảnh mượt phải làm bằng fade in/out ở đầu và cuối mỗi frame HTML (GSAP hoặc CSS animation).

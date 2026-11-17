# Remotion — dùng cho video quảng cáo CÁ NHÂN của anh Trường

Cài 16/11/2026: remotion 4.0.543 + React 19, Chrome Headless Shell tải sẵn trong `node_modules/.remotion/`.
Chiếm ~790 MB (`node_modules/`, đã gitignore).

**Giấy phép:** cá nhân dùng miễn phí. Video đăng kênh / tài liệu của Roboworld (công ty 40 người) thì phải mua
bản quyền Remotion — video công ty tiếp tục dựng bằng HyperFrames (`tools/video-tho/`, Apache-2.0).

```
cd D:\RBW_Claude\tools\remotion
npm run studio      # mở trình chỉnh trực quan trên trình duyệt
npm run render      # dựng MauDoc → out/mau-doc.mp4 (1080×1920, 30 fps)
npx remotion render src/index.ts <Id> out/<ten>.mp4
```

## Kết hợp với HyperFrames (cách đã chạy ở video 011)

Remotion dựng **bảng đồ hoạ nửa trên 1080×960** thành MP4 → bỏ vào `04-video-projects/<du-an>/assets/rm-*.mp4` →
`dung.json` gọi như cảnh phụ `{"loai":"canh-phu","src":"assets/rm-x.mp4","kieu":"nua-tren"}`. HyperFrames vẫn lo
mặt, phụ đề bám chữ, tiêu đề, nhạc, hiệu ứng âm. Mốc thời gian trong cảnh Remotion = giây tính từ đầu cảnh,
đặt theo `phu-de.txt` của bản cắt.

- `src/v012/` — 4 cảnh video 012 robot lễ tân (điện thoại · hôm nay→tương lai · ba thẻ · tích hợp), dùng lại `v011/chung.tsx`.
  `node scripts/v012.mjs [dien-thoai hom-nay …]` dựng thẳng vào `04-video-projects/012-robot-le-tan/assets/`.
- `src/v011/` — 4 cảnh video 011 (so giá · tay máy IK · dây chuyền · lời kết) + `chung.tsx` (font, màu, hình vẽ dùng chung).
  `npm run v011` dựng lại cả 4 thẳng vào assets dự án.
- Font: `public/fonts/*.woff2` là bản ĐÃ BỎ HINT (chép từ `tools/video-tho/fonts`). Đừng thay bằng TTF gốc — Chromium
  vẽ "c" thành "o".
- Soi nhanh không cần dựng cả cảnh: `npx remotion still src/index.ts <Id> out/x.jpg --frame=120`.
- Không có `typescript` cài riêng → `npx tsc` sẽ kéo nhầm gói "tsc" giả. Soi bằng ảnh tĩnh là đủ.

## Tệp

- `src/Root.tsx` — khai báo các Composition (mỗi video một cái).
- `src/MauDoc.tsx` — mẫu 3 giây: chữ bật lò xo + dòng phụ hiện dần.
- File media đặt trong `public/`, gọi bằng `staticFile('ten.mp4')`.

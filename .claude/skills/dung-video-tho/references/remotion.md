# Remotion trong video quay thô (B5)

Rút từ video 011 (máy công nghiệp vs dịch vụ) và 012 (robot lễ tân, 16/11/2026).

## Khi nào dùng

- **Chỉ khi anh Trường yêu cầu** ("thêm dựng bằng Remotion") **và xác nhận video đăng kênh cá nhân của anh.**
  Remotion miễn phí cho cá nhân; kênh / tài liệu công ty Roboworld (40 người) phải mua bản quyền
  (`tools/remotion/README.md`). Hỏi bằng câu hỏi có lựa chọn: kênh cá nhân · công ty đã/sẽ mua · kênh công ty chưa mua
  (→ giữ HyperFrames).
- Ghi điều kiện giấy phép vào `README.md` + `assets/NGUON.md` của dự án và vào `_ghi_chu` của `dung.json`.
- Nếu video có nhân viên chào bán sản phẩm công ty: nhắc anh rằng giấy phép có thể xét theo *ai dùng để làm gì*,
  đăng lại kênh công ty thì mua bản quyền trước.

## Phân vai — Remotion KHÔNG thay HyperFrames

| Remotion (`tools/remotion/`) | HyperFrames (`dung.py`) |
|---|---|
| Bảng đồ hoạ **nửa trên 1080×960**, xuất MP4 `assets/rm-*.mp4` | Ghép tất cả: người nói, khung rộng/cận, phụ đề, câu móc, tiêu đề, cảnh phụ, nhạc, hiệu ứng âm |
| Chuyển động lò xo, đường vẽ theo hàm, đồ hoạ dữ liệu | Gọi MP4 như cảnh phụ: `{"loai":"canh-phu","src":"assets/rm-x.mp4","kieu":"nua-tren"}` |

## Làm một cảnh

1. Thư mục `tools/remotion/src/vNNN/`, một file `.tsx` mỗi cảnh. Dùng lại `src/v011/chung.tsx`:
   `Nen` (nền tối + vệt đỏ + viền đáy), `bat` (lò xo), `pha` (nội suy có kẹp), `Nhan` (`*từ*` tô vàng), `tieuDe`,
   `DauTich` (dấu tích SVG — font Britti không có ✔), màu `DO`/`VANG`/`NAU`.
2. **Mốc thời gian = giây tính từ đầu cảnh** = mốc trong `phu-de.txt` của bản cắt trừ `t` của cảnh. Ghi bảng `MOC`
   ở đầu file kèm câu nói tương ứng trong chú thích.
3. Đăng ký trong `src/Root.tsx`: `<Folder name="vNNN-…">` + `<Composition id="vNNN-ten" … durationInFrames={giây×30} {...NUA}/>`.
   Độ dài cảnh ≥ `dai` trong `dung.json` (cảnh cuối cho dư 0,2–0,3 s).
4. Script dựng: `tools/remotion/scripts/vNNN.mjs` (chép từ `v012.mjs`) → `node scripts/vNNN.mjs [ten…]`.
5. **Soi ảnh tĩnh trước khi render**: `npx remotion still src/index.ts vNNN-ten out/vNNN/x.jpg --frame=N` ở mỗi mốc
   chính, ghép bảng bằng ffmpeg `xstack` rồi xem. Render cả 4 cảnh video 012 mất ~1 phút.
6. Vùng an toàn trong khung 1080×960: **chữ `top ≥ 250`, mép phải `≤ 940`**. Viền đồ hoạ lố tạm thời khi lò xo
   vọt quá thì chấp nhận được, chữ thì không.
7. Hiệu ứng âm đặt bằng nhịp `am` trong `dung.json` theo đúng mốc của cảnh — Remotion không mang tiếng.

## Cảnh đã có để học / dùng lại

| Cảnh | File | Ý |
|---|---|---|
| So sánh điện thoại | `v012/DienThoai.tsx` | máy xịn lấp lánh → chỉ 2 chức năng → dấu X → thanh cập nhật → nở lưới ứng dụng |
| Hôm nay → tương lai | `v012/HomNay.tsx` | thẻ tích ✓ trượt vào → đổi nhóm → đường cong hàm mũ vẽ dần có chấm đầu bút |
| Ba thẻ + mũi tên | `v012/BaThe.tsx` | thẻ trượt theo từng chữ, mũi tên đi lên khi nói "phát triển" |
| Tích hợp | `v012/TichHop.tsx` | robot độc lập bị gạch → dịch trái → nối dây vào khối nền tảng, xung chạy dọc dây |
| So giá · tay máy · dây chuyền · lời kết | `v011/*.tsx` | robot phục vụ / tay máy cách điệu trong `chung.tsx` |

## Ảnh bìa bằng Remotion (`Still`)

- Mẫu: `v011/Thumbnail.tsx` (2 thẻ + VS), `v012/AnhBia.tsx` (2 thẻ + mũi tên, thẻ có `hop=[trái, trên, rộng]` để phóng
  và đặt ảnh — đưa robot / màn hình vào giữa thẻ thay vì `objectFit` cắt mù).
- Ảnh đặt `public/vNNN/*.jpg`, trích full-res từ `nguon/` hoặc `assets/` của dự án:
  `ffmpeg -ss <giây> -i nguon/c01.mp4 -frames:v 1 -vf scale=1080:1920:flags=lanczos -q:v 2 public/vNNN/mat.jpg`.
- Đăng ký `<Still id="vNNN-anh-bia" component={…} width={1080} height={1920} />` trong `Root.tsx`, xuất:
  `npx remotion still src/index.ts vNNN-anh-bia ../../04-video-projects/NNN-ten/anh-bia.png` (~10 s), rồi
  `tools/video-tho/soat-bia.py NNN-ten`. Thường mất 3–4 vòng chỉnh vị trí ảnh — soát mỗi vòng, đừng đoán.

## Bẫy

- Font: chỉ dùng `public/fonts/*.woff2` đã bỏ hint (TTF gốc vẽ "c" thành "o").
- Không có `typescript` riêng → đừng `npx tsc` (kéo nhầm gói giả). Soi bằng ảnh tĩnh.
- Mọi chuyển động là hàm của `useCurrentFrame()` — không `Math.random`, không `Date.now`.

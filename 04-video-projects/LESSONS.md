# Nhật ký làm video — thất bại & thành công

> Ghi lại mọi bài học khi dựng video, để lần sau không lặp lỗi cũ.
> Mục mới thêm lên ĐẦU. Ghi ngày, việc, kết quả, cách khắc phục.

---

## 16/11/2026 — Video 012 (57,2s): video tự quay robot lễ tân — "còn ậm ừ, còn đoạn trống"

**1. Bản cắt đầu (77 s) bị chê vì còn khoảng trống và ậm ừ, dù bảng chép trông sạch.**
Tôi gộp nhiều đảo nói thành đoạn dài trong `cat.json` → mọi khoảng lặng 0,3–0,5 s bên trong và ở đầu đoạn còn nguyên;
whisper lại nuốt các tiếng vấp ("ư- ứng dụng", "n- nền tảng") vào chữ liền sau nên bảng chép không lộ.
→ Chia đoạn tại mọi khoảng lặng ≥ 0,28 s, chép lại riêng từng mẩu nghi vấp, nghe-chép lại cả bản cắt trước khi đưa duyệt.
Luật ghi ở `dung-video-tho/references/luat-cat.md`.

**2. Anh Trường muốn nhịp nhanh hơn: ×1,2** — và bỏ câu kết bán hàng ("Vậy nên robot Nova chính là giải pháp…").
Video kết bằng ý của người nói ("tích hợp với nền tảng sẵn có của đơn vị") + câu chốt trên hình, không cần câu chào hàng.

**3. Cắt dày (24 điểm cắt) thì đừng đổi khung rộng/cận ở mọi điểm** — `doi_khung_cach: 2.0` trong `dung.json`.

**4. Ảnh màn hình app thật Roboworld đã làm (nhận diện khuôn mặt, lấy số) là cảnh phụ rất khớp** khi người nói kể
"robot có thể có nhiều ứng dụng" — lấy ở `11-app-nova/<app>/demo/anh-soi/`.

**5. Anh Trường muốn thêm Remotion + video Nova thật.** 4 bảng nửa trên dựng bằng Remotion (`tools/remotion/src/v012`),
HyperFrames vẫn ghép tất cả. Anh xác nhận video đăng **kênh cá nhân** → giấy phép Remotion miễn phí; kênh công ty phải mua.
Video Nova thật lấy từ chính video mẫu của anh (`video-mau-social/05`, giây 46,6–52,35) — **soi từng 0,2 s**: đoạn 50–51,3 s
chỉ thấy lưng người rồi lia qua bàn ghế trống, QC bắt được → ghép hai khúc thấy rõ robot.

**6. Vùng an toàn phải tính cả cột 140 px bên phải cho chữ ở NỬA TRÊN.** Hộp câu móc của `dung.py` từng chạy x 50–1030;
nay chừa 140 px hai bên + trường `co`. Khối html/Remotion tự vẽ: chữ top ≥ 250 px, mép phải ≤ 940 px.

---

## 21/08/2026 — Video 009 (72,9s): video MỜI, không phải video social

**1. Có loại video thứ hai trong workspace: video GỬI RIÊNG cho khách, không đăng nền tảng.**
Video 009 gửi Zalo/email cho doanh nghiệp Tây Ninh dự Triển lãm Kết nối Chuỗi cung ứng hàng hoá
quốc tế 2026. Anh Trường chốt phong cách **kể chuyện, thân thiện, liền mạch**: mở bằng **cơ hội**
chứ không bằng nỗi đau, kết bằng **lời chúc** chứ không bằng câu hỏi mở.
→ Khuôn 6 nhịp của video 001 (hook nỗi đau → bằng chứng → cái giá → câu hỏi) **không dùng cho
loại này**. Người xem là khách mời, không phải người cần thuyết phục rằng họ đang thiếu sót.
→ Bản kịch bản đầu tôi viết theo khuôn cũ (mở bằng "khách đi ngang, liếc một cái, rồi đi tiếp")
đã bị đổi hướng. **Hỏi phong cách trước khi viết, đừng mặc định khuôn social.**

**2. Luật "không gọi tên model" có ngoại lệ: khi người xem SẮP GẶP đúng con máy đó.**
Anh Trường yêu cầu gọi thẳng "BellaBot". Khách sẽ gặp chính con máy này ở hội chợ và Trung tâm
đã đặt tên nó trong thư mời → tên riêng biến robot thành **một nhân vật**, không làm người xem
khựng lại. Luật vẫn đúng cho video social bán hàng cho người lạ.
→ ⚠ Viết **"Bella Bốt"** trong `loi-doc.txt` để máy đọc đúng, **"BellaBot"** trên hình.
`loi-doc.txt` không bao giờ hiện ra cho người đọc — đó đúng là chỗ để viết phiên âm.

**3. Chữ Neusharp 92px (`class: mid`) chỉ chứa ~13–14 ký tự một dòng, KHÔNG phải 16.**
Chữ hoa tiếng Việt rộng hẹp rất khác nhau: `NHÌN TẬN NƠI,` (13) vừa khít, `VỊ TRÍ GIAN HÀNG` (16)
cũng vừa vì nhiều chữ mảnh, nhưng `BELLA DẪN KHÁCH` (15) thì tràn.
→ **Tràn thì `<span class="hl">` bị đứt đôi qua hai dòng, nhìn như lỗi font.** Mất 2 lần render lại.
→ Cách chắc ăn: tự đặt `<br>` và giữ mỗi dòng **≤ 13 ký tự** nếu có chữ hoa rộng (B, D, K, M, N, Ơ).

**4. `--cat-trai` / `--cat-phai` là BẮT BUỘC với ảnh ngang 6016×4016.**
Cover-fit về 9:16 chỉ giữ 2.259 px giữa ảnh. Ba ảnh sự kiện có robot nằm lệch mép → khung cắt
mặc định **mất sạch robot**, ảnh ra chỉ còn cái quầy. Không có cảnh báo nào.
→ Chuẩn hoá ảnh xong **phải `Read` từng ảnh**, không tin dòng "OK ... -> 1080×1920".

**5. ⚠ `make-video.py` bước ghép nhạc HỎNG — bản chỉ-giọng vẫn tốt, đừng vứt đi.**
`ghep_nhac()` đọc lại luồng **AAC do chính pipeline vừa tạo**; bộ giải mã báo bậy
*"Rematrix is needed between stereo and 21 channels"* rồi cả filter graph chết (exit −22),
kèm hàng nghìn dòng `Invalid NAL unit size`. Lặp lại y hệt 3 lần → không phải sự cố nhất thời.
→ **Hình ảnh KHÔNG hỏng.** Đã kiểm: trích khung ở giây 45 sắc nét đủ 1080×1920, `ffprobe` đọc
đủ 2.186 khung, đúng 72,88 s. Chỉ luồng AAC trung gian là đọc lại không được.
→ **Cách vòng:** trộn nhạc với **file MP3 giọng gốc** thay vì giải mã lại AAC — vừa hết lỗi,
vừa bớt một đời nén mất chất. Lệnh đầy đủ trong `009-robot-gian-hang-tay-ninh/README.md`.
→ Chưa sửa vào `make-video.py` vì 8 video trước chạy đường cũ vẫn tốt; sửa công cụ dùng chung
cần thử lại cả 8 dự án. **Việc còn treo.**

**6. Kiểm hạn mức ElevenLabs TRƯỚC khi sinh giọng.** Gói Starter gia hạn **ngày 22 hàng tháng**,
nên ngày 20–21 là đáy kỳ. Kịch bản 1.377 ký tự tốn ~690 credit; sinh lại vì sửa lời là mất
chừng đó lần nữa. Đó là lý do phải chốt kịch bản trước, không phải thủ tục cho vui.

---

## 26/07/2026 — Video 008 (115,9s): kho ảnh robot nhà hàng THẬT SỰ chỉ có 7 cảnh

**1. `media-index.md` có mô tả SAI và ảnh không tồn tại — đừng tin, phải mở ra xem.**
- `duy-truong-doi-robot-nha-hang-den-long.jpg` được liệt kê nhưng **không có file** trong `02-media/images/personal/`.
- `duy-truong-trung-tam-thuong-mai-2-robot.jpg` ghi là "đứng giữa 2 robot tại trung tâm thương mại", thực tế là **ảnh nhận cúp Sao Khuê 2025** tại Trung tâm Hội nghị Quốc gia, đứng trước dàn **robot lễ tân đỏ** — không liên quan robot phục vụ nhà hàng.
→ Quy tắc 007 ("tên file không cho biết ảnh chụp gì") mở rộng: **mô tả trong media-index cũng không đáng tin**. Chỉ `Read` ảnh mới biết.

**2. Kho ảnh robot-trong-nhà-hàng chỉ có 7 cảnh riêng biệt, không phải 30+.** Đếm file thì nhiều, nhưng phần lớn là **crop khác nhau của cùng một khoảnh khắc**:
- Sàn caro đỏ-trắng → 007 dùng dưới **ba** tên (`s10`, `s13`, `s20`), gốc là 2 file gần trùng.
- Nhà hàng gỗ khách gia đình → `007/s08` + `003/p6-robot-khach-vui` + `002/p6-nha-hang-robot-khach` = **một** cảnh.
→ **`Get-FileHash` KHÔNG bắt được** loại trùng này (crop khác nhau ⇒ hash khác). Hash chỉ lọc trùng tuyệt đối; trùng bối cảnh phải soi mắt. Chạy hash trước cho nhanh, rồi soi phần còn lại.
→ **Hệ quả cho video sau: lập bản đồ cảnh robot TRƯỚC khi chia scene.** Kịch bản cần >7 scene có robot thì phải chấp nhận tái dùng hoặc bổ sung ảnh chụp mới.

**3. Trích frame từ `02-media/videos/` để bù ảnh: KHÔNG dùng được.** Đã thử 4 frame:
- `bellabot-gourmet-market-thailand.mp4` → siêu thị Thái Lan + **logo PUDU overlay** góc trên.
- `phong-van-khach-hang-theone-tai-vec.mp4` → triển lãm nội thất + **phụ đề cứng tiếng Việt** của video gốc nằm giữa khung.
→ Video tư liệu hầu hết đã đóng overlay/phụ đề. Coi như **không phải nguồn ảnh nền**, trừ khi tìm được đoạn sạch.

**4. Ngưỡng chữ `mid` (92px) là ~15 ký tự/dòng.** Ba scene rớt âm tiết lẻ ở bản nháp: "TÍP", "THỨ", "CHO" đứng một mình. Sửa bằng `<br>` chủ động.
→ Dấu gạch ngang dài `—` **rộng hơn dấu phẩy đáng kể**: `"trước — hay cho"` (15 ký tự) vẫn tràn dòng, đổi thành `"trước, hay cho"` mới vừa. Đếm ký tự thôi chưa đủ, phải tính cả bề rộng ký tự.

**5. Ước lượng 18,4 ký tự/giây (bài học 007) chính xác.** Ước 114s từ 2.102 ký tự, mp3 thật ra **115,68s** — lệch 1,5%. Công thức dùng được để hứa thời lượng với anh Trường ngay từ bước kịch bản.

**Về nội dung:** anh Trường cung cấp câu chuyện triển khai có thật (chủ mê / nhân viên chê / thử một tối / bạn chê nhiều nhất được khách tip). Kịch bản thêm **một nhịp riêng công nhận nỗi lo của nhân viên là hợp lý** trước khi kể diễn biến — theo luật "đứng cùng phía, không công kích". Câu chốt đổi từ khẳng định sang **câu hỏi mở gắn với hành động cụ thể** ("hỏi ý trước, hay cho thử một tối?") vì đó chính là điều anh chủ trong chuyện đã làm.

## 26/07/2026 — Video 007 (123s, dài nhất từ trước tới nay): 5 bài học

**1. Tên file ảnh KHÔNG cho biết ảnh chụp gì — phải mở ra xem.**
Tái dùng ảnh từ 002/003 theo tên file, kết quả: `p6-team-robot-that.jpg` hoá ra chính là `duy-truong-bellabot-nha-hang-sang-trong.jpg`, và `p6-robot-that-01.jpg` chính là ảnh Gogi House đã dùng ở scene khác. Ảnh Gogi suýt xuất hiện **3 lần** trong một video. Phải render 3 vòng mới sạch.
→ **Quy tắc: trước khi copy ảnh từ dự án cũ, `Read` từng ảnh một.** Luật "không lặp ảnh ở hai scene liền kề" không đủ — phải là "không lặp ảnh trong cả video", và phải kiểm bằng mắt chứ không bằng tên.
→ `003/p6-ky-thuat-robot.jpg` và `006/q11-ky-thuat.jpg` cũng là **một ảnh** (phòng mô phỏng bay VR), không liên quan robot phục vụ. Đừng dùng cho video robot nhà hàng.

**2. Ước lượng thời lượng giọng: `eleven_v3` đọc ~18,4 ký tự/giây.**
2.266 ký tự → 123,2 giây. Tôi ước 85s, sai 45%. Muốn video 70s thì kịch bản khoảng **1.300 ký tự**. Đo trước khi hứa thời lượng với anh Trường.

**3. `silencedetect` im lặng nếu chạy kèm `-v error`.**
`silencedetect` và `volumedetect` in ra ở mức log *info*, `-v error` nuốt mất → tưởng file hỏng. Chạy `ffmpeg -i <mp3> -af silencedetect=... -f null -` **không có `-v error`**, rồi grep.

**4. Ảnh Pexels ngang phải tải `w=2400`, không phải `w=1600`.**
`w=1600` với ảnh 3:2 cho cạnh ngắn 1067px — dưới ngưỡng 1080 của `prep-assets.py`, bị loại. Ảnh dọc thì `w=1600` vẫn đủ.

**5. `kiem_muot` trong `make-video.py` chạy đúng như thiết kế.**
Bắt giật ở vùng 120–125s (51/150 frame), tự render lại, lần hai ĐẠT. Không cần can thiệp tay. Khi kiểm tay, nhớ mpdecimate mặc định đếm "frame khác nhau" nên **scene tĩnh có ít frame khác là bình thường** — muốn phân biệt giật thật với cảnh tĩnh, chạy lại với ngưỡng nhạy `mpdecimate=hi=192:lo=64:frac=0.02`; rớt frame thật sẽ tụt xuống dưới 30%, cảnh tĩnh vẫn ~80%.

**Về nội dung:** đây là video đầu tiên **khai thác chính người bán** thay vì nỗi đau nhà hàng. Anh Trường yêu cầu **viết đầy đủ ý, không rút gọn** — các câu chốt kiểu ẩn dụ ("ai sẽ ở đó cùng mình khi máy cần chỉnh?") bị coi là **thiếu ý, không thoát ý**; phải nói thẳng lợi ích cụ thể ("khách cần tùy chỉnh, dù là sales cũng xử lý ngay lập tức"). Dùng **"người kinh doanh"**, không dùng "người bán hàng".

## 25/07/2026 — Video 005 GIẬT HÌNH từ giây 30: ghi hình rớt frame khi máy bận
- **Hiện tượng:** anh Trường báo 005 chuyển ảnh rất lag từ ~giây 30. Container vẫn đủ 2052 frame @30fps, không thiếu.
- **Chẩn đoán bằng `mpdecimate`:** đếm frame KHÁC NHAU theo vùng 5s. Nửa đầu ~110–130/150 (mượt), từ 30s rớt còn **10–43/150** → Chromium **lặp frame cũ** vì không kịp dựng.
- **Nguyên nhân gốc:** `render-video.mjs` ghi hình bằng Chromium **theo thời gian thực**. Lúc render bản thật 005, máy đang chạy song song một agent QC cho 006 → Chromium đói CPU, rớt frame, càng về sau càng nặng do bộ nhớ dồn ứ 14 ảnh base64 lớn.
- **Khắc phục ngay:** render lại 005 khi máy rảnh → 80% frame khác nhau, mượt đều. Thay file.
- **Chống tái diễn (không bắt người dùng nhớ):** thêm `kiem_muot()` vào `make-video.py` — sau mỗi lần render thật, tự đo mpdecimate; vùng nào <55/150 coi là giật → **tự render lại, tối đa 3 lần**. Bản nháp không kiểm.
- **Quy tắc rút ra:** ghi hình thời gian thực nhạy với tải máy. **Không chạy 2 render song song, không render trong khi agent nặng đang chạy.** Nếu buộc phải, `kiem_muot` sẽ bắt và thử lại. Ngưỡng phát hiện: <55 frame khác nhau/5s.
- **Cách kiểm tay:** `ffmpeg -i <mp4> -vf mpdecimate,showinfo -f null -` rồi đếm `pts_time` theo vùng.

## 25/07/2026 — Hai video theo bộ luật mới (005 Nhân viên, 006 Quản lý): cả hai PASS
- **005 Nhân viên** (68s, 19 scene): QC **PASS ngay vòng 1, 0 lỗi**. Chữ căn giữa/safe hoạt động tốt, giọng phân tích logic + tái định khung vai trò nhân viên. Chốt "trả lương để bê đồ hay bán hàng?".
- **006 Quản lý** (70s, 19 scene): QC **PASS, 2 lỗi polish** — kicker scene 0 chìm trên tạp dề sáng (tăng shade 0.62→0.74), và nhiều dòng `mid` rớt âm tiết lẻ ("HỢP/LÝ", "VẬN/HÀNH"). Sửa: rút gọn chữ trên hình + `<br>` chủ động.
- **`align:safe` xác nhận đúng ý anh Trường:** chữ nằm dải 60–78%, không tụt góc đáy. Scene `center` cho chữ-trơn nằm ~45–58%.
- **Bẫy đã gặp khi sửa hàng loạt bằng script:** off-by-one khi sửa `lines` theo index — clobber nhầm kicker scene kế bên. **Luôn in lại 2 scene quanh chỗ sửa để xác nhận** trước khi render. (Và: script Python trên Windows in ra ký tự Việt lỗi `charmap` — ghi file thì OK vì dùng `io.open(encoding=utf-8)`, chỉ `print` ra stdout mới lỗi; đọc lại bằng tool Read/ffprobe an toàn hơn.)
- **Tái dùng ảnh giữa các dự án chạy tốt** — 005 dùng lại 14 ảnh của 002/003, 006 dùng 12 + 3 ảnh quản lý mới. Copy (không move) sang `assets/` từng dự án.
- **Kho ảnh "quản lý" mỏng** (chỉ 2 ảnh gốc) — phải tải thêm 3 ảnh Pexels. Cần bổ sung ảnh quản lý/chủ nhà hàng Việt thật vào `02-media/` cho các video sau.

## Nhận xét của anh Trường sau 3 video draft đầu (chốt 25/07/2026) — QUAN TRỌNG

1. **Chữ phải ở GIỮA khung, không ở đáy.** Đăng lên TikTok/Reels, UI nền tảng (caption, nút tim/bình luận, tên kênh) phủ lên ~1/4 đáy màn hình và ~12% đỉnh, che mất chữ đặt ở đáy. → dùng `"align": "center"` hoặc `"align": "safe"`, bỏ `"align": "bottom"` cho chữ quan trọng. Đã thêm `.align-safe` (chừa đáy 430px, đỉnh 240px) vào `build-frame.py`.
2. **Không nói tên model robot.** Người xem chưa biết "BellaBot", "KettyBot". Luôn gọi chung **"robot phục vụ"** trên hình và trong lời đọc. (Việc đổi 004 sang BellaBot Pro giờ không còn quan trọng — chỉ cần gọi "robot phục vụ".)
3. **Nới quy định logo & số điện thoại.** Mọi ảnh trong workspace đều dùng được; hotline/logo/watermark lỡ có trong ảnh chụp **không sao cả**. Hai điều CẤM giờ chỉ áp cho thứ **mình chủ động thêm vào** (chữ, đồ hoạ, lời đọc). → **Không còn phải crop watermark, không loại ảnh vì có số/logo nền.** Điều này gỡ bỏ phần lớn công việc crop ở `prep-assets.py` và các lỗi QC "thương hiệu bên thứ ba".
4. **Tôn trọng chuyên môn người xem.** Chủ nhà hàng rất giỏi bài toán đầu tư, thậm chí chuyên sâu. Nội dung đi theo **phân tích logic**, tôn trọng kiến thức của họ, **khơi gợi mong muốn đầu tư khéo léo** — không dạy đời, không bán hàng lộ liễu. Xem thêm hai chủ thể khai thác trong `references/luat-kich-ban.md`.
5. **Ưu tiên giọng như video 002** (giọng anh Trường `eleven_v3`, on-dinh mặc định 0.5).

---

## Quy tắc dựng video (chốt 24/07/2026)

### Về hình ảnh — QUAN TRỌNG NHẤT
Mục tiêu: **người xem muốn thấy hình ảnh/video thật để liên tưởng thực tế.** Video không được là "chữ chạy trên nền đen".

1. **Không để chữ đứng một mình.** Một scene chỉ có chữ thì scene ngay sau **phải** là hình ảnh minh họa, hoặc biểu đồ/số liệu chứng minh.
2. **Hình ảnh là chủ đạo.** Scene dùng hình phải để hình chiếm phần lớn khung, dùng **liên tiếp 2–3 scene** hình, không chỉ 1 scene lẻ.
3. **Nguồn ảnh:**
   - Ưu tiên ảnh/video thật trong `02-media/`
   - Thiếu thì **chủ động tìm trên web và tải về** (ảnh stock miễn phí thương mại: Pexels, Pixabay, Unsplash)
   - Ảnh chèn vào scene **phải đúng kích thước scene** (video dọc = 1080×1920, cover-fit, không méo)
4. **Số liệu → biểu đồ.** Con số quan trọng (70–80%, ROI, so sánh) nên dựng thành biểu đồ/đồ họa dữ liệu, không chỉ chữ to.

### Kiểm tra bắt buộc sau MỖI scene
Render xong một scene → **tự screenshot lại và tự kiểm** trước khi sang scene sau:
- [ ] Chữ khớp với giọng đọc và nội dung scene
- [ ] Hình ảnh cân đối trong khung, không méo, không bị chữ che mất chủ thể
- [ ] Nếu ảnh có **Robot**: đủ bối cảnh, thấy rõ con robot (không bị cắt cụt, không quá nhỏ)
- [ ] Nếu ảnh **minh họa**: đúng với nội dung câu đang nói
- [ ] Chữ đọc được (tương phản đủ trên nền ảnh)

### Quy tắc thương hiệu (nhắc lại)
- **Video social: KHÔNG logo, KHÔNG số điện thoại** trên hình. Liên hệ để ở caption.
- Hotline duy nhất: **0866 153 946**.
- Số liệu chỉ lấy từ `03-knowledge/`. Không bịa.
- Ảnh có watermark của bên khác (đài TV, agency) hoặc watermark "ROBOWORLD" dạng overlay → **cắt bỏ** trước khi dùng.

---

## Quy tắc viết lời thoại / kịch bản (chốt 24/07/2026) — QUAN TRỌNG

Người xem mục tiêu là **chủ nhà hàng — họ cũng là chủ doanh nghiệp, cũng đã tính toán, cân nhắc rất nhiều phương án.** Lời thoại phải tôn trọng điều đó.

1. **Không công kích người xem.** Tuyệt đối tránh giọng "anh chị đang làm sai", "anh chị chưa nghĩ tới", "sao chưa có kế hoạch nào" — nghe như dạy đời, chê chủ quán kém. Họ tự ái ngay.
2. **Đồng cảm + kể chuyện, không phán xét.** Nêu vấn đề như một câu chuyện chung của cả ngành mà "ai cũng gặp", đứng cùng phía người xem, không đứng trên.
3. **Dồn nỗi đau vào NHÂN VIÊN, không vào chủ.** Cách chạm mạnh nhất: nhân viên tiềm năng, có tâm, **bị kiệt sức vì việc lặp lại vô nghĩa** — đáng lẽ sức đó để chăm khách, tư vấn thì hiệu quả hơn và khách hài lòng hơn. Chủ quán thấy tiếc người, thấy mất mát, chứ không thấy bị chê.
4. **Nối nỗi đau → hệ quả kinh doanh:** nhân viên kiệt sức → khách không được chăm → khách bỏ đi → tuyển & đào tạo lại → "một vòng lặp ai cũng mất". Chủ tự thấy cái giá, mình không cần chỉ trích.
5. **Dùng từ thông dụng, đời thường.** Ví dụ ghi số theo cách người ta hay nói: **"80 phần trăm"** chứ không phải "tám phần mười"; câu ngắn, dễ nghe khi lướt điện thoại.
6. **Chốt bằng câu hỏi mở, không ép mua.** "Bắt đầu trước, hay chạy theo sau?" — để người xem tự quyết, không hối thúc.

### Caption
- Chủ quán chỉ cần **1 câu punch** đủ dừng ngón tay. Bản dài (hook + proof + CTA + hashtag) chỉ là tùy chọn — hỏi Sếp muốn bản ngắn hay đầy đủ.
- Câu chốt đã duyệt cho video 001: *"Nhân viên giỏi nhất của bạn đang dành 80% thời gian chỉ để làm công việc không tạo ra giá trị thật sự."*
- Hotline + lời mời nhắn tin **chỉ ở caption/bio**, không lên hình.

### Lưu ý khi đưa lời thoại vào máy đọc (ElevenLabs)
- Kịch bản có **2 phiên bản chữ**: bản hiển thị/caption dùng "80%", nhưng **file đưa vào máy đọc phải viết số bằng chữ** — "tám mươi phần trăm", "hơn hai trăm nhà hàng". `doc-kich-ban.py` cảnh báo nếu còn chữ số.
- Tách riêng phần LỜI ĐỌC ra file `loi-doc.txt`, **bỏ hết tiêu đề phân cảnh và ghi chú [trong ngoặc vuông]** trước khi sinh giọng.
- Bỏ dấu gạch ngang giữa câu ("có tâm, họ đang…" thay vì "có tâm — họ đang…") để máy đọc không ngắt lỗi.

---

## Lịch sử

### 24/07/2026 — Dựng dây chuyền tự động: skill `video-roboworld` + 3 script + 2 subagent
- **Việc:** anh Trường muốn tự động hoá việc dựng video nhưng giữ chất lượng, có cơ chế cải tiến sau mỗi lần duyệt. Đề xuất ban đầu là 5 agent (kịch bản · research · dựng · ghi lỗi · master).
- **Đã sửa 3 điểm trong thiết kế:**
  1. **Agent master dạng subagent là ngõ cụt** — subagent trong Claude Code không spawn được subagent khác. Cuộc hội thoại chính làm master.
  2. **"Agent ghi nhận lỗi cho agent khác" không có kênh quan sát lúc chạy.** Tự-sửa-lỗi thật đến từ: luật viết thành văn bản cố định (`references/`) + một con mắt độc lập (`rbw-qc`, chỉ đọc, không có quyền Write) + nhật ký này.
  3. **Thiếu mắt xích giọng đọc** — giọng quyết định timeline, không phải ngược lại. Không có mp3 thì không viết được `scenes.json`.
- **Chốt kiến trúc:** 7 bước, 2 chốt duyệt (kịch bản · video nháp). Chi tiết ở `.claude/skills/video-roboworld/SKILL.md`.
- **Ba script mới:** `make-video.py` (một lệnh thay 3 lệnh PowerShell, có `--nhap` render nháp 540×960) · `prep-assets.py` (ảnh → 1080×1920, cắt watermark) · `anh-scene.py` (trích 1 ảnh/scene từ MP4 cho QC soi).
- **Ngưỡng `silencedetect` chuẩn — đã đối chiếu khớp video 001:** `n=-28dB:d=0.18` cho mốc ngắt **từng câu** (~36 mốc/77s), `n=-32dB:d=0.35` cho ranh giới **phân cảnh lớn** (~7 mốc/77s). Cách dùng: chia lời đọc theo đoạn, tính vị trí theo **tỷ lệ số ký tự**, rồi **snap về mốc gần nhất**. Sai số thực đo trên 3 video: 0,3–1,4 giây.
- **`CLAUDE.md` từng mô tả sai pipeline** — ghi quy trình qua 23 template của `tools/html-video`, nhưng chưa video nào dựng bằng đường đó. Đã sửa lại theo pipeline thật.

### 24/07/2026 — Kết quả 3 video draft: QC bắt 16 lỗi, 1 nặng lọt tới vòng 2
- **Vòng QC thực tế trên 3 video:**

  | Video | Vòng 1 | Vòng 2 | Lỗi nặng |
  |---|---|---|---|
  | 002 Bài toán chi phí | FAIL 5 thường | — | 0 |
  | 003 Golden Gate 120 | FAIL 1 nặng + 5 thường | FAIL 1 nặng (mới lộ) | 2 |
  | 004 BellaBot Pro 65cm | FAIL 5 thường | — | 0 |

- **Bài học lớn nhất: sửa chỗ này làm lộ chỗ khác.** Ở 003, việc đổi chỗ ảnh scene 11↔12 làm ảnh gian hàng Cake by VPBank rơi vào scene dễ thấy hơn, và QC vòng 2 bắt được lỗi mà vòng 1 bỏ qua. **Vòng QC thứ hai phải kiểm lại ĐỦ 8 mục, không chỉ kiểm 6 chỗ vừa sửa.**
- **Ba ảnh của 003 bị loại, cả ba cùng một nguyên nhân:** ảnh chụp tại nơi khách hàng mang theo **thương hiệu, giá và số điện thoại của họ** — thư pháp Hán cạnh chữ "400 NHÀ HÀNG", menu in "XÈO XÈO 499.000" + biển GoGi House, chữ CAKE + poster VPBank. Ưu tiên ảnh nền trung tính.
- **Nhóm lỗi hay gặp nhất, theo thứ tự:** (1) ảnh lệch nội dung câu đang nói — 4 lần · (2) chữ chìm vì `shade` thấp trên ảnh sáng — 3 lần · (3) thương hiệu bên thứ ba trong ảnh nền — 3 lần · (4) số liệu chỉ là chữ to, chưa dựng đồ hoạ — 2 lần · (5) chữ quá nhiều so với thời lượng scene — 2 lần.
- **Ngưỡng `shade` rút ra:** ảnh nền tối 0,6–0,7 · ảnh có vùng sáng hoặc thân robot trắng **0,8–0,86** · ảnh rất tối thì đừng hạ `shade`, hãy kéo sáng ảnh bằng `prep-assets.py --sang` (hạ `shade` là chữ chìm ngay).

### 24/07/2026 — QC bắt được GIÁ nằm trong ảnh nền, và tên khách hàng bị lộ
- **Lỗi nặng ở video 003:** ảnh nền scene 25,2s chụp tại nhà hàng GoGi House có nhân sự cầm quyển menu in **"XÈO XÈO 499.000"**. Video này cố ý không đưa giá nào lên hình (báo giá đã hết hiệu lực), vậy mà một con số giá lọt vào qua ảnh chụp. Ở tốc độ xem thường nó chỉ là vệt đỏ mờ — nhưng ai chụp màn hình phóng to là đọc ra.
- **Cùng ảnh đó lộ rõ biển "GoGi House"** trong khi kịch bản cố tình chỉ nói "một chuỗi hơn 400 nhà hàng". Nêu đích danh khách hàng mà chưa xin phép là rủi ro quan hệ, không phải rủi ro thương hiệu.
- **Khắc phục:** thay hẳn ảnh, không cắt vá.
- **Quy tắc rút ra — mở rộng luật "không bịa số":** ảnh nền có thể mang theo **giá của người khác** (menu, poster khuyến mãi, bảng giá treo tường) và **tên thương hiệu khách hàng**. Cả hai đều phải soi, không chỉ soi số điện thoại. Đã bổ sung vào `rbw-qc.md`.

### 24/07/2026 — Đổi sản phẩm video 004 vì không có ảnh: KettyBot Pro → BellaBot Pro
- **Việc:** kịch bản 004 viết cho KettyBot Pro (lối đi 52 cm, 3 khay, 9 giờ). Nhưng ảnh KettyBot Pro duy nhất trong kho — `02-media/san-pham/kettybot-pro/anh-studio/kettybot-pro-2-mau-vang-trang-studio.png` — chỉ **400×400 px**. `prep-assets.py` loại thẳng, đúng luật cạnh ngắn ≥1080.
- **Vấn đề thật:** mọi ảnh dùng được đều là BellaBot / BellaBot Pro. Đọc thông số máy này mà chiếu hình máy khác là **sai lệch**, dù không con số nào bịa.
- **Cách xử lý đã chốt:** đổi nội dung theo ảnh, không đổi ảnh theo nội dung — sang BellaBot Pro (lối đi 65 cm, 4 khay, 40 kg/chuyến, màn 18.5", ~11 giờ). Sinh lại giọng. Kịch bản KettyBot Pro cũ giữ nguyên ở cuối `kich-ban.txt` chờ ảnh thật.
- **Quy tắc rút ra:** **kiểm ảnh sản phẩm TRƯỚC khi viết kịch bản sản phẩm**, không phải sau. Một dòng lệnh `prep-assets.py <thư-mục> --kiem` ở bước brief đã tránh được cả vòng viết kịch bản + sinh giọng bỏ đi.

### 24/07/2026 — `anh-scene.py` chụp quá sớm → QC báo "thiếu chữ" oan
- **Lỗi:** bản đầu trích ảnh kiểm ở **60% quãng scene**. Scene 2 của video 002 có dòng cuối `delay: 1.3` → ở mốc 60% (1,77s vào scene) dòng "TRIỆU / THÁNG" vẫn đang chạy animation, ảnh ra chỉ thấy "8–12". Người kiểm tưởng dựng thiếu chữ.
- **Khắc phục:** mốc chụp = `max(60% quãng scene, delay lớn nhất + 0.85s)`, kẹp trong `[t0+0.3, t1-0.35]`. `rise` chạy 0,75s nên +0,85s là chắc chắn hiện xong.
- **Quy tắc rút ra:** công cụ kiểm cũng phải được kiểm. Một QC báo lỗi giả còn tệ hơn không có QC — nó làm người dựng mất niềm tin rồi bỏ qua cả lỗi thật.

### 24/07/2026 — `rbw-research` bắt được 4 ảnh có SỐ ĐIỆN THOẠI trong nền
- **Việc:** agent tìm ảnh cho video 002 tự loại 4 ảnh vì phát hiện số điện thoại **nằm trong ảnh nền**, không phải chữ mình thêm vào: hotline `0975 032 288` trên cửa kính, `1900 25 88` trên thân taxi, `1900 6622` trên poster GoGi, `090 44 88 290` trên biển Coca-Cola trong quán phở.
- **Bài học:** luật "không số điện thoại trên hình" **không chỉ áp cho chữ mình đặt vào** — số nằm sẵn trong ảnh chụp cũng vi phạm. Đây là loại lỗi rất dễ lọt vì mắt người dựng chỉ nhìn chủ thể, không đọc biển hiệu ở hậu cảnh.
- Đã bổ sung ý này vào `rbw-research.md` và `rbw-qc.md`.
- **Tìm ra luôn ảnh mất tích của video 001:** `robot-nha-hang-doc.jpg` vẫn còn trong `02-media/images/products/`, và bản đó **không có watermark**. Muốn dựng lại 001 thì copy từ đó về `assets/`.

### 24/07/2026 — `scenes-v2.json` của video 001 trỏ vào 2 ảnh không còn tồn tại
- **Việc:** chạy lại video 001 để kiểm `make-video.py`, `build-frame.py` báo `FileNotFoundError` ở `assets/robot-nha-hang-doc.jpg` và `assets/p6-robot-no.jpg`. Hai file này biến mất khỏi `assets/` sau khi bản MP4 đã render xong.
- **Hệ quả:** bản MP4 đã duyệt vẫn còn nguyên, nhưng **không dựng lại được** từ nguồn.
- **Khắc phục ngay:** thêm bước **kiểm tư liệu trước khi render** vào `make-video.py` — quét toàn bộ `image`/`video`/`giong`/`nhac` trước khi làm gì. Thiếu file thì dừng trong 1 giây kèm danh sách, thay vì hỏng giữa chừng sau vài phút ghi hình.
- **Quy tắc rút ra:** ảnh trong `assets/` là **nguồn**, không phải file tạm. Đừng dọn `assets/` sau khi render — MP4 xong không có nghĩa dự án dựng lại được.

### 24/07/2026 — Giọng `eleven_v3` đọc nhanh hơn ước lượng ~30%
- Ước theo video 001: 1.426 ký tự → 76,5 giây ≈ **18,6 ký tự/giây**. Ba video mới: 1.069c → 63,6s · 748c → 39,0s · 335c → 18,2s ≈ **16,8–19,2 ký tự/giây**, khớp.
- **Nhưng** kịch bản 003 viết cho mục tiêu 55 giây lại ra 39 giây — vì ước theo *số câu* chứ không theo *số ký tự*. **Luôn đếm ký tự để ước thời lượng**, đừng đếm câu.
- Không chỉnh được bằng cờ (`eleven_v3` bỏ qua `--toc-do`). Muốn dài hơn thì viết thêm chữ.

### 24/07/2026 — Viết lại lời thoại theo hướng đồng cảm + giọng v2: BÀI HỌC COPYWRITING
- **Vấn đề Sếp chỉ ra:** bản kịch bản cũ (đoạn 6–46s) có phần **công kích người xem** — hỏi kiểu "có kế hoạch nâng cấp nhân viên chưa?" nghe như chê chủ quán chưa nghĩ tới. Mà chủ quán cũng là chủ doanh nghiệp, họ đã tính toán nhiều rồi.
- **Cách sửa:** chuyển sang **kể chuyện + đồng cảm**, dồn nỗi đau vào **nhân viên bị kiệt sức** (người tiềm năng, có tâm, đáng lẽ để sức chăm khách/tư vấn thì hiệu quả hơn) → nối sang hệ quả kinh doanh (khách bỏ đi, tuyển lại từ đầu, "vòng lặp ai cũng mất"). Chủ thấy tiếc, không thấy bị chê. Chi tiết → xem block "Quy tắc viết lời thoại".
- **Từ ngữ:** đổi "tám phần mười" → **"80 phần trăm"** (từ thông dụng). Nhưng file đưa máy đọc vẫn viết "tám mươi phần trăm".
- **Giọng v2:** tách `loi-doc.txt` (chỉ phần thoại, bỏ ghi chú phân cảnh) → `doc-kich-ban.py --file` → `001-noi-dau-be-bung-v2.mp3` (76.5s, on-dinh mặc định 0.5). Kịch bản dài 1.426 ký tự.
- **Caption:** Sếp chốt bản 1 câu duy nhất, không cần bản dài.

### 24/07/2026 — Bản 3 (v2): thêm nhạc nền + giọng v2 + 15 sub-scene
- **Giọng:** dùng file Sếp tự tạo `001-noi-dau-be-bung-v2.mp3` (76.5s). Canh timeline bằng `silencedetect` — mốc ngắt câu khớp ranh giới 6 phân cảnh rất tốt khi ánh xạ theo tỷ lệ số ký tự mỗi phân cảnh.
- **Nhạc nền:** tải 3 track CC từ **archive.org** (Liborio Conti — "Original Quality Music For Content Creators"). URL trực tiếp `https://archive.org/download/<id>/<file>.mp3`, tải qua `Invoke-WebRequest` (tên file có dấu cách → `[uri]::EscapeDataString`). Pixabay chặn WebFetch (403).
- **Ghép nhạc + ducking:** `sidechaincompress` cho nhạc tự giảm khi có giọng, nhạc `volume=0.16` + fade in/out. Lệnh: `[1:a]volume=0.16,afade...[m];[m][0:a]sidechaincompress=threshold=0.02:ratio=8[md];[0:a][md]amix=inputs=2:duration=first:normalize=0`.
- **Ảnh:** 17 ảnh 1080×1920, không ảnh nào lặp liền kề. Robot dùng ảnh thật team Roboworld ở Hội An (người Việt + robot thật) cho phần 200+ Golden Gate — mạnh hơn ảnh stock.
- **Bẫy đã gặp:** ảnh Sếp thêm có kích thước lẻ (800×449, 1024×683, 1920×2560) → phải crop lại 1080×1920. Ảnh `robot-studio` có **logo PUDU overlay góc trên** → crop bỏ 18% trên. Ảnh 800×449 quá nhỏ → loại (phóng lên vỡ).
- **Quy tắc rút ra:** khi Sếp bỏ ảnh vào `assets/`, luôn kiểm 3 thứ: (1) đúng 9:16 chưa, (2) có logo overlay không, (3) độ phân giải đủ lớn không (cạnh ngắn ≥ 1080).

### 24/07/2026 — Bản 2 video "Nỗi đau bê bưng": THÀNH CÔNG (hình làm chủ đạo)
- **Làm lại theo quy tắc mới:** mỗi phân cảnh có ảnh/biểu đồ làm nền chủ đạo, không còn chữ trên nền đen trơn.
- **Nguồn hình:** ảnh robot workspace (P6) + ảnh stock Pexels cho cảnh nỗi đau (nhân viên bê bưng, kiệt sức, nhà hàng đông) — crop cover-fit 1080×1920.
- **Biểu đồ:** thêm donut SVG tự vẽ (vòng đỏ chạy theo %) cho số liệu 70–80% → "dữ liệu chứng minh" đúng ý.
- **Khử nháy đen ở điểm chuyển ảnh:** cross-fade overlap — mỗi scene bắt đầu hiện sớm 0.4s, đè lên scene trước (sửa 1 chỗ trong `build-frame.py`). Trước đó đổi ảnh giữa 2 sub-scene bị nháy đen 0.4s.
- **Quy trình kiểm tra từng scene chạy tốt:** render 6 scene rời → screenshot từng scene → phát hiện lỗi nháy P2 → sửa → render lại → ghép. Ghép bằng concat demuxer `-c copy` (cùng codec/res/fps) nên không giảm chất lượng.
- Kết quả: 65s, 22.5 MB, 1080×1920. Mọi scene: hình chủ đạo, robot rõ đủ bối cảnh, ảnh khớp nội dung, không logo/không số.

### 24/07/2026 — Clip robot đều dính logo → chưa dùng làm video nền
- **Việc:** muốn dùng video robot thật làm nền (Sếp yêu cầu "video minh họa thật").
- **Vấn đề:** cả 3 clip serving-robots (gourmet-market, cake, kettybot) đều có **logo PUDU góc trên-trái + text overlay** → vi phạm "không logo". Video cá nhân duy-truong-social thì có watermark "Duy Trường Robot".
- **Xử lý tạm:** dùng ảnh robot workspace (sạch logo) + hiệu ứng zoom chậm (Ken Burns) để tạo chuyển động. Pipeline đã hỗ trợ video nền (`video` field trong scenes.json) — sẵn sàng khi có clip sạch.
- **Cần Sếp:** nếu muốn video nền động thật, quay/gửi clip robot **không có logo overlay** (logo in trên thân máy thì OK, ở khổ dọc rất nhỏ).

### 24/07/2026 — Tải ảnh stock từ Pexels: THÀNH CÔNG
- **Việc:** cần ảnh "nhân viên nhà hàng bê bưng", "khách chờ" — không có trong workspace.
- **Cách chạy được:** `WebFetch` trang tìm kiếm Pexels → lấy URL trực tiếp `https://images.pexels.com/photos/<id>/...jpeg` → tải bằng `Invoke-WebRequest`, thêm `?auto=compress&cs=tinysrgb&w=1280`.
- **Bẫy:** trong PowerShell, URL có `&` phải nối chuỗi bằng biến, không viết thẳng trong ngoặc kép — nếu không báo "hostname could not be parsed". Cách né: `$full = $u + '?auto=compress' + '&' + 'cs=tinysrgb'`.
- Pexels/Pixabay/Unsplash: miễn phí cho mục đích thương mại, không cần ghi nguồn (nên vẫn nên lưu link nguồn vào README dự án).

### 24/07/2026 — Model tiếng Việt: BÀI HỌC LỚN
- **Lỗi:** đặt mặc định `eleven_multilingual_v2` — model này **KHÔNG có tiếng Việt**, đọc méo, không tròn vành rõ chữ. Sếp phát hiện ngay.
- **Khắc phục:** chỉ 3 model có tiếng Việt: `eleven_v3` (tốt nhất), `eleven_turbo_v2_5`, `eleven_flash_v2_5`. Đã đặt mặc định `eleven_v3`, thêm cảnh báo tự động trong `rbw_voice.py`.
- **Cấu hình giọng anh Trường được duyệt:** voice_id `uAu2GDxpTX7tfBPiMuoR`, model `eleven_v3`, similarity 1.0 (bản `vi-v3-bamsat`).

### 24/07/2026 — ElevenLabs 401 giả: BÀI HỌC
- **Lỗi:** script test kết nối gọi endpoint `/user`, nhưng key của công ty không có quyền `user_read` → trả 401, tưởng nhầm "key sai".
- **Khắc phục:** kiểm tra kết nối bằng `/voices` (endpoint luôn có quyền). Phân biệt `missing_permissions` (key đúng, thiếu quyền) với 401 thật.

### 24/07/2026 — Voice v3 không nghe lời tham số speed
- Model `eleven_v3` bỏ qua `--toc-do`. Giọng ra ~21s cho kịch bản 30s. Cách xử lý: viết thêm câu cho đủ độ dài, hoặc chấp nhận video ngắn hơn (video ngắn xem hết = tốt cho thuật toán).

### 24/07/2026 — Chữ đỏ chìm trên ảnh sáng: BÀI HỌC
- **Lỗi:** chữ đỏ `#E83636` đặt trên vùng ảnh sáng bị chìm, khó đọc.
- **Khắc phục:** tăng lớp phủ tối (`shade`) ở giữa khung nơi có chữ; thêm `text-shadow` cho mọi cấp chữ; chữ trên ảnh luôn cần nền tối đệm.

### 24/07/2026 — Watermark trong ảnh triển khai
- Ảnh trong `02-media/images/deployments/` có dải watermark "ROBOWORLD" ở trên. Cắt bỏ ~11–13% chiều cao phía trên trước khi dùng (script crop trong scratchpad, kết quả lưu vào `assets/` của dự án).

### 24/07/2026 — Pipeline render tự dựng: THÀNH CÔNG
- `tools/build-frame.py` (HTML tự chứa font+ảnh base64) + `tools/render-video.mjs` (Chromium ghi hình → ffmpeg → MP4 ghép voice-over). Render 1080×1920 H.264 chạy ổn.
- Playwright nằm trong `tools/html-video`, nạp bằng đường dẫn tuyệt đối (ESM không đọc NODE_PATH).
- Dựng từng scene rời rồi ghép: mỗi scene 1 file json → render riêng → concat. Lead-in 0.3s/scene tạo nhịp thở tự nhiên khi ghép.

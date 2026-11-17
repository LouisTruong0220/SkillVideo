# Hướng dẫn lấy API key ElevenLabs

Mục tiêu: có một chuỗi key dạng `sk_xxxxxxxx...` để máy tự sinh giọng đọc tiếng Việt cho video.

---

## Phần 1 — Tạo tài khoản & lấy key (5 phút)

### Bước 1. Đăng ký

Mở **https://elevenlabs.io** → bấm **Sign up** (góc trên phải).

Đăng ký bằng Google cho nhanh, hoặc bằng email + mật khẩu. Nếu dùng email thì phải vào hộp thư bấm link xác nhận.

### Bước 2. Vào trang API Keys

Sau khi đăng nhập, bấm vào **ảnh đại diện góc trên bên phải** → chọn **API Keys**.

Hoặc vào thẳng: **https://elevenlabs.io/app/settings/api-keys**

### Bước 3. Tạo key mới

- Bấm **Create API Key**
- Đặt tên gợi nhớ, ví dụ: `duy-truong-video`
- Phần quyền (Permissions): chọn **Full Access**, hoặc tối thiểu bật `Text to Speech` và `Voices`
- Bấm **Create**

### Bước 4. Sao chép key NGAY

Chuỗi key hiện ra dạng:

```
sk_1a2b3c4d5e6f7g8h9i0j...
```

> **Key chỉ hiện MỘT LẦN.** Đóng cửa sổ là không xem lại được, phải tạo key khác. Copy ngay.

### Bước 5. Đưa key vào máy

Mở thư mục `D:\RBW_Claude\tools\elevenlabs\`, copy file `.env.example` thành `.env`, mở bằng Notepad và dán key vào:

```
ELEVENLABS_API_KEY=sk_1a2b3c4d5e6f7g8h9i0j...
```

Lưu lại. Xong.

> **Bảo mật:** file `.env` đã được đưa vào `.gitignore`, không bị đẩy lên GitHub. Đừng dán key vào chat, đừng gửi qua Zalo, đừng lưu lên Drive. Ai có key là dùng được hạn mức trả phí của Sếp. Lỡ lộ thì vào trang API Keys bấm **Delete** rồi tạo key mới.

Xong bước này, Sếp nhắn tôi **"đã có key ElevenLabs"** là tôi chạy kiểm tra kết nối ngay.

---

## Phần 2 — Chọn gói (đọc kỹ phần này trước khi trả tiền)

| Gói | Giá | Ký tự/tháng | Nhân bản giọng (Voice Cloning) |
|---|---|---|---|
| **Free** | 0 đ | ~10.000 | ❌ **KHÔNG có** |
| **Starter** | ~5 USD/tháng | ~30.000 | ✅ Instant Voice Cloning |
| **Creator** | ~22 USD/tháng | ~100.000 | ✅ + Professional Voice Cloning |

**Điểm quan trọng nhất:** muốn dùng **giọng của Sếp** thì **bắt buộc phải có gói trả phí từ Starter trở lên**. Gói Free chỉ dùng được giọng có sẵn của ElevenLabs — nghe vẫn ổn nhưng không phải giọng Sếp.

**Ước lượng thực tế:** một video 30 giây cần khoảng 400–600 ký tự lời thoại. Gói Starter 30.000 ký tự ≈ **50–70 video ngắn/tháng**. Thừa sức cho nhu cầu hiện tại.

**Đề xuất:** đăng ký Free trước, để tôi test kết nối và thử giọng có sẵn. Thấy chất lượng ổn thì mới nâng lên Starter để nhân bản giọng Sếp. Không cần trả tiền ngay từ đầu.

---

## Phần 3 — Nhân bản giọng của Sếp (sau khi có gói trả phí)

Tôi đã chuẩn bị sẵn mẫu giọng từ 7 video TikTok của Sếp:

```
02-media/giong-noi/mau-giong-duy-truong/_GHEP-3-mau-tot-nhat.mp3    ← 2 phút 21 giây, dùng file này
```

File này ghép từ 3 video có nhiều khoảng nghỉ tự nhiên nhất (ít nhạc nền chèn lên giọng nói):
- `02-bellabot-gioi-thieu-kha-nang-51s`
- `03-bellabot-quan-thit-nuong-han-quoc-58s`
- `07-duy-truong-nha-hang-lau-31s`

**Sếp nghe thử file ghép này trước.** Nếu nhạc nền to át giọng thì báo tôi, tôi cắt lại đoạn khác — có 7 file gốc trong cùng thư mục để chọn.

### Cách nhân bản

**Cách 1 — trên web (dễ hơn, khuyên dùng lần đầu):**
1. Vào **https://elevenlabs.io/app/voice-lab**
2. Bấm **Add Voice** → **Instant Voice Cloning**
3. Đặt tên: `Duy Truong`
4. Kéo file `_GHEP-3-mau-tot-nhat.mp3` vào
5. Tick ô xác nhận đây là giọng của mình (bắt buộc — ElevenLabs yêu cầu)
6. Bấm **Add Voice**

**Cách 2 — bằng lệnh:**
```powershell
cd D:\RBW_Claude\tools\elevenlabs
python clone-voice.py
```

Xong, Sếp báo tôi để tôi lấy `voice_id` ghi vào `.env`, sau đó mọi video đều đọc bằng giọng Sếp.

### Lưu ý về chất lượng

Mẫu lấy từ TikTok nên đã bị nén và chuẩn hóa âm lượng (tôi đo được đỉnh 0.0 dB = có nén giới hạn). Giọng nhân bản sẽ giống nhưng không hoàn hảo.

**Muốn giọng chuẩn hơn:** Sếp thu 2–3 phút bằng điện thoại trong phòng yên tĩnh — đọc bình thường, không nhạc nền, không tiếng ồn — rồi đưa tôi file đó. Chất lượng sẽ hơn hẳn.

---

## Phần 4 — Dùng hằng ngày

Sau khi xong, chỉ cần nhắn tôi:

> *"Đọc kịch bản này bằng giọng tôi"* → tôi sinh file WAV/MP3 vào `05-output/voice/`

> *"Dựng video 30 giây về BellaBot Pro, có voice-over"* → tôi viết kịch bản, sinh giọng, ghép vào video

---

## Xử lý sự cố

| Hiện tượng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `401 Unauthorized` | Key sai hoặc đã bị xóa | Tạo key mới, dán lại vào `.env` |
| `Voice cloning not available` | Đang dùng gói Free | Nâng lên gói Starter |
| `quota_exceeded` | Hết ký tự trong tháng | Chờ sang tháng hoặc nâng gói |
| Giọng đọc sai tiếng Việt | Dùng sai model | Phải là `eleven_multilingual_v2` — script đã đặt sẵn |
| Đọc số sai ("155.000.000") | Model đọc số theo kiểu Anh | Viết chữ trong kịch bản: "một trăm năm mươi lăm triệu" |

## ⚠️ Chọn model — quyết định chất lượng phát âm tiếng Việt

**Chỉ 3 model hỗ trợ tiếng Việt chính thức:**

| Model | Đặc điểm |
|---|---|
| `eleven_v3` | Mới nhất, phát âm tiếng Việt tốt nhất — **mặc định** |
| `eleven_turbo_v2_5` | Nhanh hơn, rẻ hơn |
| `eleven_flash_v2_5` | Nhanh nhất, rẻ nhất |

**KHÔNG dùng** `eleven_multilingual_v2`, `eleven_turbo_v2`, `eleven_flash_v2` — chúng không có tiếng Việt trong danh sách ngôn ngữ, sẽ đọc méo và không tròn vành rõ chữ.

Đổi model tạm thời cho một lần chạy:
```powershell
python doc-kich-ban.py "..." ten-file --model eleven_turbo_v2_5
```

## Tinh chỉnh khi giọng chưa ưng

| Tham số | Ý nghĩa | Thử |
|---|---|---|
| `--giong-giong` | Bám sát giọng gốc (similarity). Cao = giống Sếp hơn | `1.0` |
| `--on-dinh` | Thấp = biểu cảm hơn · Cao = đều, chắc hơn | `0.3` hoặc `0.65` |
| `--toc-do` | Tốc độ đọc | `0.95` chậm lại cho rõ chữ |

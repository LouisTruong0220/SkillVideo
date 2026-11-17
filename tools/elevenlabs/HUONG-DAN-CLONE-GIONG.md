# Hướng dẫn nhân bản giọng trên ElevenLabs

> Quy trình đã chạy thật, kiểm chứng bằng máy. Viết cho session sau khỏi dò lại từ đầu.
> Lần chạy gần nhất: giọng Bella (BellaBot Pro tiếng Việt) — 14/08/2026.
> Cần API key trong `.env` — xem [HUONG-DAN-LAY-API-KEY.md](HUONG-DAN-LAY-API-KEY.md).

Nhân bản giọng cần **gói trả phí (Starter trở lên)**. Tài khoản là **của chung công ty** —
có giọng của đồng nghiệp ("Q Huy MKT RBW", "Phương Uyên RBW"). **Đừng xoá giọng người khác.**

---

## Bản đồ 4 bước

```
Nhiều clip rời  →  [1] chọn clip  →  [2] ghép 1 file 1-3 phút  →  [3] gọi API clone
                                                                        ↓
                     [4] sinh file thử + trang nghe A/B  →  Sếp duyệt
```

| Bước | Script | Ra cái gì |
|---|---|---|
| 1–2 | `dung-mau-bella.py` | file mẫu ghép `.mp3` |
| 3 | `clone-bella.py` | `voice_id` |
| 4 | `doc-kich-ban.py` + `dung-trang-nghe-bella.py` | file thử + `nghe-doi-chieu.html` |

Ba script trên **viết riêng cho giọng Bella**. Làm giọng khác thì copy ra, sửa đường dẫn
nguồn và danh sách `CHON`. Phần lõi gọi API nằm ở `rbw_voice.py` (hàm `clone`), dùng lại được nguyên.

> ⚠️ `clone-voice.py` (bản cũ, cho giọng anh Trường) **trỏ vào `02-media/voice-samples/` đã không còn** —
> kho media dọn lại rồi. Muốn nhân bản lại giọng anh Trường thì sửa đường dẫn thành
> `02-media/giong-noi/mau-giong-duy-truong/` trước.

---

## Bước 1 — Chọn clip

**Đích: 1–3 phút.** Nhiều hơn KHÔNG tốt hơn — Instant Voice Cloning bão hoà ở đó.
Lần làm Bella: 31 clip / 2 phút 42 giây, chọn từ kho 74 clip.

**Chọn theo trọng số biểu cảm, đừng lấy đều:**

| Lấy dày | Lấy vừa | Bỏ |
|---|---|---|
| Clip có nhấn nhá, cảm xúc, tiếng cười, tiếng đặc trưng | Câu trung tính, đọc trơn | Clip dính nhạc nền, clip < 1 giây rời rạc |
| Giữ "chất" của giọng | Giữ khả năng đọc văn bản dài | |

Chỉ lấy trung tính thì giọng ra đọc đều đều như máy đọc tin. Chỉ lấy biểu cảm thì
đọc câu dài bị ngoa. Phải pha.

**Nếu có bảng lời thoại đi kèm — đọc trước.** Với Bella, bảng `.xlsx` cho biết "Meo" là
**một từ diễn viên đọc thành lời** ở cuối 45/74 câu, chứ không phải hiệu ứng ghép thêm.
Biết vậy mới chọn đúng clip, và mới biết cách dùng: chỉ cần viết `Meo.` vào kịch bản.

---

## Bước 2 — Ghép file mẫu

Từng clip: **cắt lặng đầu/đuôi → đo → cộng gain tĩnh**, rồi nối, chèn 0,35 giây nghỉ.
Xuất mono 44,1 kHz 192 kbps, đích khoảng **-16 LUFS**, đỉnh không chạm -1 dBFS.

```powershell
python dung-mau-bella.py --nghe   # in danh sách đã chọn, chưa dựng
python dung-mau-bella.py          # dựng thật
```

### ⚠️ Bẫy 1 — `loudnorm` một lượt giết nhấn nhá

`loudnorm` **là bộ nén động**, không phải chỉnh âm lượng. Nó ép chỗ to chỗ nhỏ về đều
nhau — đúng thứ mình đang cần giữ.

```
SAI :  -af "loudnorm=I=-16:TP=-1.5:LRA=11"
ĐÚNG:  đo trước  →  -af "volume=-6.4dB"
```

Gain tĩnh dịch cả dạng sóng lên/xuống, dải động **giữ nguyên tuyệt đối**. Đo bằng
`ffmpeg -i x.mp3 -af ebur128=peak=true -f null -` rồi lấy `I` và `Peak`, cộng đúng
số dB còn thiếu, chặn trần để đỉnh không vượt -1 dBFS.

### ⚠️ Bẫy 2 — "Noise floor" của `astats` KHÔNG đáng tin

Nó báo 42/74 file Bella có nền -31…-50 dB → tưởng dính nhạc nền, suýt loại sạch nhóm
biểu cảm (tức là loại đúng phần hay nhất).

**Muốn biết có nhạc nền hay không thì quét RMS theo cửa sổ**, đừng tin một con số tổng:

```bash
ffmpeg -i x.mp3 -af "aresample=8000,asetnsamples=2000,astats=metadata=1:reset=1,\
ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null -
```

Đọc dãy số: khoảng nghỉ giữa câu **tụt sâu rồi bật lại** = tiếng sạch.
Nếu có một **mức sàn giữ nguyên suốt cả file** = có nhạc nền thật.
Với Bella: nghỉ xuống -34…-47 dB, đuôi file -97…-112 dB → sạch, chỉ là nhiễu nén MP3.

### ⚠️ Bẫy 3 — Nguồn thường đã bị nén sẵn

Giọng nhà máy robot được master cho loa nhỏ: Bella có LRA chỉ **1,1–3,2 LU**,
I = -6,6…-9,0 LUFS. Thấy LRA thấp ở bản ghép **đừng hoảng** — đó là trung thực với nguồn,
không phải mình làm hỏng. So với bản gốc trước khi kết luận.

---

## Bước 3 — Gọi API

```powershell
python clone-bella.py                      # tên mặc định
python clone-bella.py --ten "Ten Giong"    # đặt tên khác
```

Script tự kiểm tên trùng trước khi tạo, tránh đẻ ra bản sao thứ 2, thứ 3 trên tài khoản chung.

**Không bật `remove_background_noise`** nếu tiếng đã sạch — nó ăn mất tiếng cười và các
âm đặc trưng (với Bella là tiếng "meo").

Có `voice_id` rồi thì **lưu vào `.env` dưới tên riêng**, đừng đè `ELEVENLABS_VOICE_ID`
(dòng đó là giọng anh Trường, pipeline video đang dùng):

```
ELEVENLABS_VOICE_ID_BELLA=50SWaRvGlWK9PFx8N9Al
```

---

## Bước 4 — Thử và duyệt

```powershell
python doc-kich-ban.py "Lời thoại. Meo!" ten-file --giong <voice_id> --on-dinh 0.5
python dung-trang-nghe-bella.py     # dựng trang nghe A/B gốc ↔ clone
```

Trang HTML nhúng audio base64 nên **tự đứng một mình** — gửi Zalo/mail mở được ngay,
không cần kèm mp3. (Chromium chặn `fetch` qua `file://`, nhúng base64 là cách duy nhất.)

### Chọn stability — đã thử thật, có kết luận

`eleven_v3` **chỉ nhận 0,0 / 0,5 / 1,0**. Anh Trường nghe 6 mẫu Bella, chấm:

| stability | Có thẻ biểu cảm | Kết quả | Dùng khi nào |
|---|---|---|---|
| **0,5** | không | ✅ **đạt** | **Mặc định. Cứ bắt đầu từ đây.** |
| **1,0** | không | ✅ đạt | Đọc hàng loạt câu cần đồng đều |
| **0,0** | **có** `[giggles]` | ✅ đạt | Cần cảm xúc mạnh — **phải có thẻ dẫn** |
| 0,0 | không | ❌ trượt | — |

> **Quy luật rút ra: stability 0,0 chỉ dùng được khi có thẻ biểu cảm dẫn đường.**
> Thả trôi ở 0,0 thì giọng trôi theo, mỗi lần sinh một kiểu.
> Thẻ `[giggles]`, `[laughs]`, `[excited]`, `[whispers]` **chỉ chạy trên `eleven_v3`**.

### Kiểm bằng máy trước khi bắt Sếp nghe

Đo cao độ (F0) bằng tự tương quan — chỉ cần numpy, không cần librosa (máy này chưa cài).

```powershell
python do-cao-do.py <file-goc.mp3> <file-clone.mp3> ...
```

So bản clone với bản gốc:

| Nguồn | F0 giữa | p10 | p90 | Dải nhấn nhá |
|---|---:|---:|---:|---:|
| Bella gốc (5 clip) | 250–308 Hz | 213–231 | 340–390 | 127–174 |
| Bella clone (7 clip) | 246–314 Hz | 208–225 | 369–400 | 150–192 |

Cùng quãng giọng, dải p10→p90 không hẹp lại → biểu cảm không bị san phẳng. **Đạt.**
Nếu dải clone **hẹp hơn hẳn** bản gốc → nhiều khả năng đã lỡ nén động ở bước 2, quay lại sửa.

Cách `do-cao-do.py` làm: giải mã PCM 16 kHz mono → cắt khung 40 ms, bước 10 ms →
tự tương quan trong dải 80–400 Hz → lấy trung vị và bách phân vị 10/90.
Khung nào năng lượng thấp hoặc tương quan đỉnh < 0,30 thì bỏ (im lặng / phụ âm vô thanh).

**Đo bằng máy không thay được tai người.** Nó chỉ bắt lỗi thô. Vẫn phải để Sếp nghe duyệt.

---

## Nhớ hỏi trước khi đưa ra ngoài

Giọng nhà máy (PUDU, Gausium, OrionStar) là **của diễn viên lồng tiếng hãng thuê**,
không phải tài sản Roboworld. Nhân bản dùng nội bộ cho chính dòng máy mình phân phối
thì hợp lý; **đưa lên video/tài liệu công khai thì hỏi anh Trường trước.**

Ghi nguồn vào `NGUON.md` cạnh file mẫu — nêu rõ giọng gốc của ai, lấy từ đâu.

---

## Đã làm rồi

| Giọng | voice_id | Mẫu & ghi chú |
|---|---|---|
| Duy Trường | `uAu2GDxpTX7tfBPiMuoR` | `02-media/giong-noi/mau-giong-duy-truong/` |
| Bella (BellaBot Pro VI) | `50SWaRvGlWK9PFx8N9Al` | `02-media/giong-noi/bellabot-pro-tieng-viet/_mau-clone/NGUON.md` |

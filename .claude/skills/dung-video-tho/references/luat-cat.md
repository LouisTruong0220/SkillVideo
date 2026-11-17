# Luật chọn đoạn và cắt (B3)

Phỏng theo `ghost-editor/references/take-selection.md` (MIT), chỉnh cho tiếng Việt và cách anh Trường quay.

## Người ta quay thế nào

Nói một câu, không ưng, nói lại; trôi thì nói tiếp; đôi khi làm lại cả bài sau khi "nóng máy". Nên video thô là
kịch bản đọc 2–3 lần chồng lên nhau, bản trôi chảy thường nằm **phía sau**. Bảng `ban-chep.md` là bản đồ của nó.

## Quy trình

1. Dựng lại "kịch bản anh muốn nói" từ bản đầy đủ nhất. Đánh số các ý.
2. Gắn mỗi đảo trong `ban-chep.md` với số ý của nó, hoặc `x` cho câu bỏ dở, lẩm bẩm ("thôi làm lại"), mở đầu hỏng.
3. Mỗi ý chọn MỘT bản:
   - đúng ý (không cần đúng chữ — lời nói tự nhiên thường hay hơn);
   - trôi, không vấp giữa câu, không ậm ừ;
   - bằng nhau thì chọn **bản sau** (người nói đã nóng máy);
   - một mạch nhiều ý liền hơi → giữ cả mạch làm một đoạn, ít điểm cắt hơn, giọng liền hơn.
4. Bỏ hẳn: câu thừa, lặp ý, câu "để em nói lại", lời chào dài dòng, đoạn nói với người quay.
5. **Móc câu 3 giây đầu.** Câu đầu video phải khiến chủ nhà hàng dừng ngón tay: con số, nghịch lý, kết quả.
   Câu đó nằm giữa video thô thì được phép đưa lên đầu, miễn ý không bị đổi.
6. Kết bằng lời mời (nhắn tin / demo) hoặc câu chốt giá trị. Không kết lửng.

## Ậm ừ tiếng Việt

| Loại | Ví dụ | Máy xử lý |
|---|---|---|
| Ậm ừ thuần | ờ, ơ, ừ, ừm, ưm, ờm, ầm | tự cắt |
| "à / á / a" | "À, hôm nay…" | tự cắt khi đứng đầu đảo hoặc lặng hai bên. "vậy à?" giữ |
| Lặp liền 2–4 chữ | "cái robot cái robot này" | tự cắt bản đầu. Láy 1 chữ ("từ từ", "dần dần") KHÔNG đụng |
| Tiếng không thành chữ `[…]` | ậm ừ whisper bỏ qua, hít thở, chép miệng | tự cắt (nằm ngoài mọi chữ) |
| Từ đệm | "thì là", "kiểu như", "nói chung là", "thực ra thì" | **không tự cắt** — Claude quyết. Anh Trường hay nói "anh chị ạ" — là chất giọng, giữ |
| "ạ" cuối câu | "anh chị ạ" | không bao giờ là ậm ừ |

## Câu nói lại

- ⟲ trên một đảo = đảo sau giống nó (≥ 3 chữ đầu trùng hoặc giống ≥ 60%). Máy bỏ đảo trước. **Kiểm lại**: nếu bản
  trước trọn câu và hay hơn, sửa `cat.json` lấy bản trước.
- "nửa sau nói lại" = anh nói tiếp được một đoạn rồi vấp, quay lại nói nửa sau. Máy cắt nửa vấp.
- Whisper chép cả file sẽ GỘP hai lần nói thành một câu sạch — vì vậy `nghe-chep.py` chép theo khối ngắn.

## Mép cắt (máy đã làm, chỉ sửa khi soi thấy lỗi)

- Đầu đoạn: chữ đầu − 0,10 s. Cuối đoạn: chữ cuối + 0,15 s, kéo thêm tới khi tắt tiếng (tối đa +0,35 s) vì
  whisper hay chấm hết chữ cuối quá sớm.
- Khoảng lặng trong câu > 0,35 s → cắt, còn ~0,25 s. Dưới mức đó là nhịp thở của người nói, giữ.
- Mọi mép làm tròn về lưới 1/30 s và có 12 ms tăng/giảm âm → không lệch tiếng, không "tạch".
- Mỗi điểm cắt, `dung.py` đổi khung rộng ↔ cận (1,14×) quanh mặt → che giật hình (jump cut thành "đổi góc máy").

## Sau khi sửa tay `cat.json` — bắt buộc (anh Trường nhận xét 16/11/2026, video 012)

Anh Trường nghe ra "ậm ừ và đoạn trống" ở bản cắt mà bảng chép trông sạch. Ba nguyên nhân, ba việc phải làm.
**Việc 1 và 3 nay do `tools/video-tho/lam-sach.py` làm tự động** (17/11/2026); việc 2 vẫn làm tay (bẫy VT-14).
1. **Không để đoạn dài chứa khoảng lặng.** Đo RMS (−38 dB, làm mượt 50 ms) trong từng đoạn; khoảng lặng ≥ 0,28 s →
   tách đoạn, mép −0,07 / +0,10 s. Đầu đoạn cũng phải sát tiếng (đề xuất máy thường dư 0,3–0,5 s).
2. **Nói vấp không hiện trong bảng chép.** Whisper nuốt "ư-", "n-", "m-" vào chữ liền sau (chữ kéo dài bất thường,
   hoặc một đảo tiếng ngắn 0,1–0,2 s ngay trước chữ thật). Chép lại riêng từng mẩu nghi ngờ (kèm 0,5 s lặng hai đầu)
   để biết mẩu đó là chữ gì, rồi cắt mẩu thừa.
3. **Nghe-chép lại cả `da-cat.mp4`** trước khi đưa duyệt: phải đọc liền mạch, không chữ lặp, không mất chữ
   (v1 của 012 lẹm chữ "AI" vì đảo bắt đầu bằng `[…]` mà thật ra là chữ).

Anh Trường thích **nhịp nhanh**: mặc định thử `toc_do` 1,2 cho video nói.

## Sửa `cat.json`

```json
{"doan": [
  {"id": "d03", "clip": "c01", "a": 41.20, "b": 47.93, "chu": "…"},
  {"id": "d01", "clip": "c01", "a": 3.10,  "b": 9.87,  "chu": "…"}
]}
```
Thứ tự trong mảng = thứ tự trong video. `a`/`b` là giây theo clip đã chuẩn hoá (`nguon/c01.mp4`).
Cần mốc chính xác của một chữ → tra `build/chep.json` (mỗi chữ có `s`/`e`).

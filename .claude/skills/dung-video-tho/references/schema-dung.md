# Schema `dung.json` (B5)

Mọi mốc `t` / `dai` tính bằng giây trên **bản cắt** (`build/ban-cat.md`, `build/tu-moi.json`), không phải video thô.
Đường dẫn file: tương đối thư mục dự án (`assets/canh-01.mp4`) hoặc gốc workspace (`02-media/...`).

```json
{
  "ten": "010-vu-cam-2-tang",
  "nhac": {"file": "02-media/am-thanh/nhac-nen-video-mau/01-bellabot-nha-hang-starbucks-63s.mp3"},
  "phu_de": {"y": 0.60, "co": 74, "nhan": "#FFD43B"},
  "can": 1.14,
  "cat_doi_khung": true,
  "nhip": [ { "loai": "...", "t": 0, "dai": 2.5, ... } ]
}
```

| Trường gốc | Mặc định | Ý nghĩa |
|---|---|---|
| `ten` | tên thư mục | file ra `05-output/<ten>.mp4` |
| `nhac.file` | — (không nhạc) | bản nhạc trong `nhac-nen-video-mau/` |
| `nhac.bat_dau` / `het` | `doan_sach` trong muc-luc | đoạn nhạc dùng (lặp nếu video dài hơn) |
| `nhac.duoi_giong_db` | −11 | nhạc thấp hơn giọng bao nhiêu dB (tự đo) |
| `nhac.am_luong` | — | hệ số cứng, ghi đè cách tự đo |
| `phu_de.y` | 0.60 | tâm phụ đề theo chiều cao (tự né mặt khi cận, tự về 980px khi chia đôi) |
| `phu_de.co` / `nhan` | 74 / `#FFD43B` | cỡ chữ px, màu từ nhấn |
| `can` | 1.14 | mức "khung cận" xen kẽ ở điểm cắt |
| `cat_doi_khung` | true | false = không đổi khung ở điểm cắt |
| `doi_khung_cach` | 0 | chỉ đổi rộng↔cận khi lần đổi trước đã cách ≥ X giây. Bản cắt dày (bỏ từng khoảng lặng, điểm cắt mỗi 1–2 s) dùng 2.0 để khung không giật liên tục |

## Trường chung của mọi nhịp

| Trường | Ý nghĩa |
|---|---|
| `loai` | xem bảng dưới |
| `t`, `dai` | bắt đầu, độ dài |
| `am` | file hiệu ứng (tương đối `02-media/am-thanh/myinstants/`, vd `bat-chu/pop_7e9Is8L.mp3`); `false` = im. Bỏ trống = âm mặc định của loại |
| `am_luong_am` | 0.55 — âm lượng hiệu ứng (1 = nguyên bản) |

Chữ trong mọi trường văn bản nhận `*từ*` để tô vàng.

## Các loại nhịp

| `loai` | Trường riêng | Hiển thị |
|---|---|---|
| `mo-dau` | `dong1`, `dong2`, `co` (96) | Hook đầu video: dòng 1 Neusharp đỏ viền trắng, dòng 2 Britti trắng. Đặt ở ~y 300px, khung chữ chừa 140 px hai bên (16/11/2026) — dòng 1 quá ~13 ký tự in hoa thì hạ `co` (80) kẻo xuống hàng đè mặt |
| `tieu-de` | `chu` (`\n` xuống dòng), `mau` = `trang-do` · `vang` · `trang` · `do`, `y` (0.27), `co` | Chữ to IN HOA bật từ 2× về 1×, phóng nhẹ, mờ đi |
| `phong-to` | `muc` (1.3) | Phóng vào mặt trong `dai` giây rồi về |
| `canh-phu` | `src` (video/ảnh), `kieu` = `toan-man` · `nua-tren` · `khung`, `bat_dau` (giây trong clip) | Cảnh phụ. Giọng anh Trường vẫn chạy. Ảnh tự Ken Burns |
| `anh` | như `canh-phu` | bí danh của `canh-phu` |
| `dan` | `src`, `x` (0.72 tâm ngang), `y` (0.2 đỉnh), `rong` (300px) | Ảnh dán viền trắng bật lên, lắc nhẹ (logo nhà hàng khách) |
| `the-so` | `so`, `don_vi`, `truoc`, `nhan`, `y` (0.24), `thap_phan` | Thẻ tối viền đỏ, số vàng đếm từ 0 |
| `bieu-do` | `tieu_de`, `don_vi`, `cot`: [{`nhan`, `gia_tri`, `hien`?, `mau` = `do`·`xam`·`vang`}], `nguon` | Cột ngang mọc dần ở nửa trên, người nói xuống nửa dưới |
| `mo-phong` | `so_ban` (6), `ban_den` ([3, 6]), `chu` | Mặt bằng nhìn từ trên: BẾP + các bàn, robot phục vụ chạy bếp → các bàn → về bếp, để lại vệt vàng. Nửa trên |
| `cua-so` | `tieu_de`, `noi_dung`, `nut` (["OK"]), `y` (0.2) | Hộp thoại bật lên, nút chính "bấm" trước khi tắt |
| `html` | `file` (tương đối dự án), `ten` | Khối tự viết riêng cho video — xem dưới |
| `am` | `file`, `am_luong` (0.6) | Chỉ phát hiệu ứng âm |

`kieu: nua-tren` (và `bieu-do`, `mo-phong`): `dung.py` tự dời người nói xuống nửa dưới cho mặt ở ~y 1250px và đưa
phụ đề lên đường ranh giữa.

## Khối tự viết (`html`) — cho mô phỏng riêng từng video

File HTML chứa markup + một `<script>` đăng ký hàm dựng hoạt cảnh. Khung là 1080×1920; phần tử gốc là `goc`.

```html
<div class="lop-rieng" style="position:absolute;inset:0">
  <svg id="mp-x" viewBox="0 0 1080 960" width="1080" height="960"> … </svg>
</div>
<script>
window.__khoi = window.__khoi || {};
window.__khoi["ten-khoi"] = function (tl, t0, dai, goc) {
  // CHỈ dùng tl.fromTo / tl.to / tl.set với mốc tuyệt đối t0 + x. Không Date.now, không Math.random,
  // không setTimeout, không repeat:-1 — mọi thứ phải là hàm của thời gian timeline.
  tl.fromTo(goc.querySelector("#mp-x"), {opacity: 0}, {opacity: 1, duration: .3}, t0);
};
</script>
```
`"ten"` trong `dung.json` phải khớp khoá `window.__khoi[...]`. Id trong khối phải là duy nhất (đặt tiền tố).

## Ví dụ đã chạy thật (dự án thử 15/11/2026)

```json
{"ten": "thu-video-tho",
 "nhac": {"file": "02-media/am-thanh/nhac-nen-video-mau/01-bellabot-nha-hang-starbucks-63s.mp3"},
 "nhip": [
  {"loai": "mo-dau", "t": 0, "dai": 2.6, "dong1": "Robot phục vụ", "dong2": "rất có duyên với *nhà hàng cuốn*"},
  {"loai": "canh-phu", "t": 3.0, "dai": 2.8, "src": "assets/canh-01.mp4", "kieu": "nua-tren", "bat_dau": 2},
  {"loai": "tieu-de", "t": 10.3, "dai": 1.8, "chu": "2 mặt sàn", "mau": "vang"},
  {"loai": "phong-to", "t": 12.2, "dai": 1.2, "muc": 1.3},
  {"loai": "mo-phong", "t": 13.6, "dai": 4.0, "so_ban": 6, "ban_den": [3, 5], "chu": "Mỗi tầng *1 robot* phục vụ"},
  {"loai": "the-so", "t": 18.2, "dai": 2.4, "so": 10, "truoc": "Còn", "nhan": "suất *demo miễn phí*"},
  {"loai": "canh-phu", "t": 20.8, "dai": 1.4, "src": "assets/canh-01.mp4", "kieu": "khung", "bat_dau": 8},
  {"loai": "cua-so", "t": 22.3, "dai": 2.5, "tieu_de": "Đăng ký demo",
   "noi_dung": "Nhắn tin cho *em Trường* để nhận lịch demo", "nut": ["Nhắn ngay", "Để sau"]}
 ]}
```

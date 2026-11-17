# -*- coding: utf-8 -*-
"""
Dựng trang HTML nghe đối chiếu: bản gốc BellaBot Pro <-> bản clone ElevenLabs.

Audio nhúng base64 nên trang tự đứng một mình, gửi qua Zalo/mail mở được ngay.
(Chromium chặn fetch qua file:// — nhúng base64 là cách duy nhất chạy offline.)

Chạy:  python dung-trang-nghe-bella.py
Mở:    02-media/giong-noi/bellabot-pro-tieng-viet/_mau-clone/nghe-doi-chieu.html
"""
import base64
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
GOC = os.path.join(ROOT, "02-media", "giong-noi", "bellabot-pro-tieng-viet",
                   "Giọng gốc", "File giọng")
OUT = os.path.join(ROOT, "05-output", "voice")
DICH = os.path.join(ROOT, "02-media", "giong-noi", "bellabot-pro-tieng-viet",
                    "_mau-clone")

VOICE_ID = "50SWaRvGlWK9PFx8N9Al"

# (tieu_de, duong_dan_goc, duong_dan_clone, loi_thoai, ghi_chu)
CAP = [
    ("Câu chào thương hiệu",
     os.path.join(GOC, "Hello_1_3.mp3"),
     os.path.join(OUT, "thu-bella-A-st05.mp3"),
     "Xin chào! Chào mừng quý khách đến với hành tinh Roboworld. Meo",
     "Cùng một câu — nghe thẳng xem tiếng “Meo” cuối câu có giống không."),

    ("Cùng câu, mức biểu cảm CAO (stability 0.0)",
     os.path.join(GOC, "Hello_1_3.mp3"),
     os.path.join(OUT, "thu-bella-A-st00.mp3"),
     "Xin chào! Chào mừng quý khách đến với hành tinh Roboworld. Meo",
     "Nhấn nhá mạnh hơn, nhưng mỗi lần sinh lại hơi khác nhau."),

    ("Cùng câu, mức ĐỀU (stability 1.0)",
     os.path.join(GOC, "Hello_1_3.mp3"),
     os.path.join(OUT, "thu-bella-A-st10.mp3"),
     "Xin chào! Chào mừng quý khách đến với hành tinh Roboworld. Meo",
     "Ổn định nhất, hợp khi cần đọc hàng loạt câu cho đồng bộ."),

    ("Tiếng cười + meo",
     os.path.join(GOC, "touch_hand_1_2.mp3"),
     os.path.join(OUT, "thu-bella-B-cuoi.mp3"),
     "[giggles] Ôi! Tay của bạn ấm quá. Meo. [giggles] Đừng trêu tôi nữa nhé.",
     "Thẻ [giggles] chỉ chạy trên model eleven_v3."),

    ("Giọng dỗi",
     os.path.join(GOC, "touch_angry_2_1.mp3"),
     os.path.join(OUT, "thu-bella-D-doi.mp3"),
     "Meo. Thôi đi, bạn phiền quá đi. Meo. Tôi không chơi với bạn nữa đâu.",
     "Kiểm chất “nhõng nhẽo” — chỗ khó nhất của giọng này."),

    ("CÂU MỚI (không có trong mẫu)",
     os.path.join(GOC, "delivery_arrive_1_1.mp3"),
     os.path.join(OUT, "thu-bella-C-cau-moi.mp3"),
     "Xin chào quý khách. Bella xin phép dọn bàn giúp bạn nhé. Meo!",
     "Phép thử thật sự: câu robot chưa từng đọc bao giờ."),
]


def nhung(path):
    with open(path, "rb") as fh:
        return "data:audio/mpeg;base64," + base64.b64encode(fh.read()).decode()


CSS = """
:root{--do:#C13F28;--do-tuoi:#E83636;--nen:#110909;--chu:#f5ebe8;--mo:#b09a94;
      --vien:#3a2320;--the:#1c1010}
*{box-sizing:border-box}
body{margin:0;padding:32px 20px 64px;background:var(--nen);color:var(--chu);
     font:16px/1.6 "Segoe UI",system-ui,sans-serif}
.bo{max-width:920px;margin:0 auto}
h1{font-size:30px;margin:0 0 6px;color:#fff;letter-spacing:.3px;text-transform:uppercase}
.phu{color:var(--mo);margin:0 0 28px;font-size:15px}
.tt{background:var(--the);border:1px solid var(--vien);border-left:3px solid var(--do-tuoi);
    border-radius:8px;padding:14px 18px;margin:0 0 28px;font-size:14.5px}
.tt code{background:#000;padding:2px 7px;border-radius:4px;color:#ffb3a5;font-size:13.5px}
.cap{background:var(--the);border:1px solid var(--vien);border-radius:10px;
     padding:18px 20px;margin-bottom:18px}
.cap h2{font-size:17px;margin:0 0 4px;color:#fff}
.loi{color:#ffd9cf;font-style:italic;margin:0 0 4px;font-size:15px}
.ghi{color:var(--mo);font-size:13.5px;margin:0 0 14px}
.hang{display:flex;gap:14px;flex-wrap:wrap}
.o{flex:1 1 300px;min-width:280px;background:#000;border:1px solid var(--vien);
   border-radius:8px;padding:12px 14px}
.nhan{font-size:12px;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:8px;
      font-weight:700}
.goc .nhan{color:#8fbf9f}
.clone .nhan{color:var(--do-tuoi)}
audio{width:100%;height:36px}
table{width:100%;border-collapse:collapse;margin-top:10px;font-size:14px}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--vien)}
th{color:var(--mo);font-weight:600;font-size:12.5px;text-transform:uppercase;
   letter-spacing:.6px}
td.s{text-align:right;font-variant-numeric:tabular-nums}
"""

HTML = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nghe đối chiếu — giọng Bella</title>
<style>{css}</style></head><body><div class="bo">
<h1>Giọng Bella — gốc so với bản nhân bản</h1>
<p class="phu">BellaBot Pro tiếng Việt · nhân bản trên ElevenLabs {ngay}</p>

<div class="tt">
<b>Cách nghe:</b> mỗi mục có hai ô — <b>bên trái là file gốc của máy</b>,
<b>bên phải là bản ElevenLabs sinh ra</b>. Nghe kỹ tiếng “Meo” cuối câu và
chỗ lên giọng giữa câu.<br><br>
<code>voice_id = {vid}</code> &nbsp; <code>model = eleven_v3</code>
</div>

{caps}

<div class="cap">
<h2>Đo cao độ — bằng máy, không cảm tính</h2>
<p class="ghi">F0 là cao độ giọng. Dải p10→p90 càng rộng thì nói càng có nhấn nhá.</p>
<table>
<tr><th>Nguồn</th><th class="s">F0 giữa</th><th class="s">p10</th>
    <th class="s">p90</th><th class="s">Dải nhấn nhá</th></tr>
<tr><td>Gốc (5 clip)</td><td class="s">250–308 Hz</td><td class="s">213–231</td>
    <td class="s">340–390</td><td class="s">127–174</td></tr>
<tr><td>Clone (7 clip)</td><td class="s">246–314 Hz</td><td class="s">208–225</td>
    <td class="s">369–400</td><td class="s">150–192</td></tr>
</table>
<p class="ghi" style="margin-top:12px">Cùng quãng giọng. Dải nhấn nhá của bản clone
rộng hơn gốc một chút — biểu cảm không bị san phẳng.</p>
</div>

</div></body></html>
"""

CAP_HTML = """<div class="cap">
<h2>{i}. {tieu_de}</h2>
<p class="loi">“{loi}”</p>
<p class="ghi">{ghi}</p>
<div class="hang">
  <div class="o goc"><div class="nhan">Gốc — máy BellaBot</div>
    <audio controls preload="none" src="{a_goc}"></audio></div>
  <div class="o clone"><div class="nhan">Clone — ElevenLabs</div>
    <audio controls preload="none" src="{a_clone}"></audio></div>
</div></div>
"""


def main():
    thieu = [p for _, g, c, _, _ in CAP for p in (g, c) if not os.path.exists(p)]
    if thieu:
        raise SystemExit("Thieu file:\n  " + "\n  ".join(thieu))

    caps = "".join(
        CAP_HTML.format(i=i + 1, tieu_de=t, loi=loi, ghi=ghi,
                        a_goc=nhung(g), a_clone=nhung(c))
        for i, (t, g, c, loi, ghi) in enumerate(CAP)
    )

    from datetime import date
    html = HTML.format(css=CSS, caps=caps, vid=VOICE_ID,
                       ngay=date.today().strftime("%d/%m/%Y"))

    os.makedirs(DICH, exist_ok=True)
    dich = os.path.join(DICH, "nghe-doi-chieu.html")
    with io.open(dich, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(f"  XONG: {dich}")
    print(f"  Dung luong: {os.path.getsize(dich)/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()

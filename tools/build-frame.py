# -*- coding: utf-8 -*-
"""
Dựng file HTML tự chứa (font + ảnh nhúng base64) cho một video dọc 1080×1920.

Vì sao nhúng base64: headless Chromium chặn fetch qua file://, nên mọi tài
nguyên phải nằm ngay trong file HTML thì mới hiện lúc ghi hình.

Dùng:  python tools/build-frame.py <thu-muc-du-an>
Đọc:   <thu-muc>/scenes.json
Ghi:   <thu-muc>/frame.html
"""
import base64
import json
import mimetypes
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_CSS = os.path.join(ROOT, "00-brand", "brand-fonts-embedded.css")

W, H = 1080, 1920


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode("ascii")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build(target):
    # target có thể là thư mục (chứa scenes.json) hoặc thẳng 1 file .json
    if os.path.isdir(target):
        json_path = os.path.join(target, "scenes.json")
        proj_dir = target
        out = os.path.join(proj_dir, "frame.html")
    else:
        json_path = target
        proj_dir = os.path.dirname(target)
        out = os.path.splitext(target)[0] + ".html"

    cfg = json.load(open(json_path, encoding="utf-8"))
    total = float(cfg["duration"])
    scenes = cfg["scenes"]

    fonts = open(FONT_CSS, encoding="utf-8").read()

    parts_css, parts_html = [], []

    for i, sc in enumerate(scenes):
        t0 = float(sc["start"])
        t1 = float(sc.get("end", total))
        dur = t1 - t0
        fade = min(0.45, dur / 4)

        # Cross-fade: scene sau BẮT ĐẦU hiện sớm 0.4s so với start, đè lên scene
        # trước (nền opaque che scene cũ) -> không còn nháy đen ở điểm chuyển ảnh.
        lead = min(0.4, t0)
        p_in0 = (t0 - lead) / total * 100
        p_in1 = (t0 + fade) / total * 100
        p_out0 = (t1 - fade) / total * 100
        p_out1 = t1 / total * 100

        parts_css.append(f"""
@keyframes sc{i}{{
  0%,{p_in0:.4f}%{{opacity:0;visibility:hidden}}
  {p_in1:.4f}%{{opacity:1;visibility:visible}}
  {p_out0:.4f}%{{opacity:1;visibility:visible}}
  {p_out1:.4f}%,100%{{opacity:0;visibility:hidden}}
}}
#s{i}{{animation:sc{i} {total}s linear forwards}}""")

        # chuyển động riêng của các lớp bên trong scene
        inner = []
        for j, el in enumerate(sc.get("lines", [])):
            delay = t0 + float(el.get("delay", 0))
            cls = el.get("class", "line")
            style = el.get("style", "")
            parts_css.append(
                f"#s{i} .e{j}{{animation:rise .75s cubic-bezier(.2,.7,.3,1) both;"
                f"animation-delay:{delay:.3f}s}}"
            )
            if "donut" in el:
                # Biểu đồ vòng chứng minh dữ liệu — vòng đỏ tự vẽ theo %
                pct = float(el["donut"])
                C = 534.0
                off = C * (1 - pct / 100.0)
                parts_css.append(
                    f"#s{i} .e{j} .dfg{{stroke-dasharray:{C:.0f};"
                    f"animation:draw{i}_{j} 1.1s ease-out both;"
                    f"animation-delay:{delay + 0.25:.3f}s}}"
                    f"@keyframes draw{i}_{j}{{from{{stroke-dashoffset:{C:.0f}}}"
                    f"to{{stroke-dashoffset:{off:.0f}}}}}"
                )
                inner.append(
                    f'<div class="donutwrap e{j}" style="{style}">'
                    f'<svg viewBox="0 0 200 200">'
                    f'<circle class="dbg" cx="100" cy="100" r="85"/>'
                    f'<circle class="dfg" cx="100" cy="100" r="85" '
                    f'transform="rotate(-90 100 100)"/></svg>'
                    f'<div class="dnum">{el["text"]}</div></div>'
                )
            else:
                inner.append(f'<div class="{cls} e{j}" style="{style}">{el["text"]}</div>')

        bg = ""
        if sc.get("video"):
            # Video nền thật — nhúng base64, phát khi unfreeze (xem render-video.mjs)
            uri = data_uri(os.path.join(proj_dir, sc["video"]))
            shade = sc.get("shade", 0.55)
            bg = (f'<video class="bgv" muted playsinline preload="auto" '
                  f'{"loop" if sc.get("loop", True) else ""}>'
                  f'<source src="{uri}" type="video/mp4"></video>'
                  f'<div class="shade" style="--a:{shade}"></div>')
        elif sc.get("image"):
            uri = data_uri(os.path.join(proj_dir, sc["image"]))
            zoom = sc.get("zoom", 1.10)
            parts_css.append(
                f"#s{i} .bg{{animation:ken{i} {dur + fade:.2f}s linear both;"
                f"animation-delay:{t0:.3f}s}}"
                f"@keyframes ken{i}{{from{{transform:scale(1)}}to{{transform:scale({zoom})}}}}"
            )
            shade = sc.get("shade", 0.62)
            bg = (f'<div class="bg" style="background-image:url({uri})"></div>'
                  f'<div class="shade" style="--a:{shade}"></div>')

        align = sc.get("align", "center")
        parts_html.append(
            f'<section id="s{i}" class="scene align-{align}">{bg}'
            f'<div class="stack">{"".join(inner)}</div></section>'
        )

    html = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<title>{esc(cfg.get("title", "video"))}</title>
<style>
{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#0b0605}}
body{{font-family:'Britti Sans',system-ui,sans-serif;color:#fff;
  -webkit-font-smoothing:antialiased}}

.scene{{position:absolute;inset:0;display:flex;flex-direction:column;
  padding:110px 88px;opacity:0;visibility:hidden;
  background:#0b0605 radial-gradient(ellipse 78% 42% at 50% 74%,
    rgba(232,54,54,.42) 0%, rgba(232,54,54,.13) 44%, rgba(11,6,5,0) 74%)}}
.align-center{{justify-content:center}}
.align-bottom{{justify-content:flex-end}}
/* Vùng an toàn: TikTok/Reels/Shorts phủ UI (caption, nút tim/bình luận, tên
   kênh) lên khoảng 22-26% đáy màn hình và ~12% đỉnh. Chữ đặt ở đáy bị che mất.
   align-safe giữ chữ trong dải giữa — đáy chừa 430px, đỉnh chừa 240px. */
.align-safe{{justify-content:flex-end;padding-bottom:430px;padding-top:240px}}
.stack{{position:relative;z-index:3;display:flex;flex-direction:column;gap:30px}}

.bg{{position:absolute;inset:0;background-size:cover;background-position:center;
  transform-origin:center;z-index:1}}
.bgv{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1}}
/* Lớp phủ tối để chữ luôn đọc được trên ảnh. Giữa khung phủ đậm hơn hai
   đầu vì chữ nằm ở đó — chữ đỏ trên vùng ảnh sáng là chìm ngay. */
.shade{{position:absolute;inset:0;z-index:2;
  background:linear-gradient(180deg,
    rgba(11,6,5,calc(var(--a)*.92)) 0%,
    rgba(11,6,5,calc(var(--a)*.78)) 30%,
    rgba(11,6,5,calc(var(--a)*.88)) 55%,
    rgba(11,6,5,calc(var(--a)*.96)) 80%,
    rgba(11,6,5,.99) 100%)}}

.kicker{{font-weight:700;text-transform:uppercase;letter-spacing:.2em;
  font-size:34px;color:#E83636}}
.big{{font-family:'Neusharp','Arial Black',sans-serif;text-transform:uppercase;
  font-size:136px;line-height:1.02;letter-spacing:.01em;
  text-shadow:0 6px 34px rgba(0,0,0,.75)}}
.mid{{font-family:'Neusharp','Arial Black',sans-serif;text-transform:uppercase;
  font-size:92px;line-height:1.06;text-shadow:0 5px 28px rgba(0,0,0,.75)}}
.body{{font-size:46px;line-height:1.42;font-weight:400;color:#efe7e5;
  text-shadow:0 3px 18px rgba(0,0,0,.8)}}
.small{{font-size:34px;line-height:1.4;font-weight:300;color:#c9bdba}}
.num{{font-family:'Neusharp','Arial Black',sans-serif;font-size:230px;
  line-height:.9;color:#E83636}}
.hl{{color:#E83636}}
.rule{{width:132px;height:8px;background:#E83636;border-radius:4px}}

/* Biểu đồ vòng (donut) chứng minh dữ liệu */
.donutwrap{{position:relative;width:440px;height:440px;align-self:center}}
.donutwrap svg{{width:100%;height:100%}}
.dbg{{fill:none;stroke:rgba(255,255,255,.14);stroke-width:22}}
.dfg{{fill:none;stroke:#E83636;stroke-width:22;stroke-linecap:round;
  filter:drop-shadow(0 0 16px rgba(232,54,54,.55))}}
.dnum{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  font-family:'Neusharp','Arial Black',sans-serif;font-size:96px;color:#fff}}

@keyframes rise{{from{{opacity:0;transform:translateY(46px)}}
  to{{opacity:1;transform:translateY(0)}}}}
{"".join(parts_css)}
</style></head>
<body>{"".join(parts_html)}</body></html>"""

    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"  {out}  ({os.path.getsize(out)/1024/1024:.1f} MB, {total}s, {len(scenes)} scene)")
    return out


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ".")

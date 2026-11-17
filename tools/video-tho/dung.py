# -*- coding: utf-8 -*-
"""B7 — Dựng thành phẩm: bản cắt + phụ đề + nhịp (chữ, cảnh phụ, mô phỏng, hiệu ứng, âm thanh) + nhạc nền.

    python tools/video-tho/dung.py <du-an> [--nhap]        # --nhap: 15 khung/giây, nén nháp, ra build/nhap.mp4
    python tools/video-tho/dung.py <du-an> --doan 28-35    # chỉ dựng giây 28–35 (30 khung/giây, có tiếng nói, không nhạc)
                                                           #   → build/doan-28-35.mp4 — xem nhanh một cảnh vừa sửa
    python tools/video-tho/dung.py <du-an> --chi-nhac      # chỉ trộn lại nhạc (không dựng lại hình)
Soi ảnh tĩnh không cần dựng: tools/video-tho/soi.py <du-an> 15.1 29.8 …

Đọc: dung.json (kế hoạch) · phu-de.txt · build/da-cat.mp4 · build/moc-cat.json · build/mat.json
Ghi: build/hf/ (dự án HyperFrames, mở được bằng `hyperframes preview`) · build/hf-ra.mp4 · 05-output/<ten>.mp4
Schema dung.json: .claude/skills/dung-video-tho/references/schema-dung.md
"""
import argparse, html, json, re, shutil, subprocess, sys
from pathlib import Path
from chung import (AN_TOAN, CONG_CU, ENV_HF, GOC, H, HF, KHO_AM, W, chay, do, doc_json, du_an, gan_bia)

VANG, DO, DO_SAM = "#FFD43B", "#E83636", "#C13F28"
AM_MAC_DINH = {  # hiệu ứng âm mặc định theo loại nhịp; nhịp nào ghi "am": false thì im
    "mo-dau": "chuyen-canh/transition-whoosh.mp3", "tieu-de": "bat-chu/pop_7e9Is8L.mp3",
    "canh-phu": "chuyen-canh/fast-whoosh.mp3", "anh": "chuyen-canh/fast-whoosh.mp3",
    "the-so": "nhan-manh/proper-ding_IbfMQYw.mp3", "bieu-do": "chuyen-canh/whoosh-sfx.mp3",
    "mo-phong": "chuyen-canh/whoosh-sfx.mp3", "cua-so": "giao-dien/discord-notification.mp3",
    "dan": "bat-chu/bubble-pop.mp3",
}
NUA_TREN = {"nua-tren"}


def e(s):
    return html.escape(str(s), quote=True)


class Mat:
    """Vị trí mặt theo thời gian (toạ độ khung 1080×1920 của bản cắt)."""
    def __init__(self, p):
        j = doc_json(p, {"tom_tat": {}, "mau": []})
        self.mau = [m for m in j["mau"] if m.get("cx") is not None]
        t = j["tom_tat"]
        self.mac_dinh = {"cx": t.get("cx", W // 2), "cy": t.get("cy", int(H * 0.33)), "w": t.get("w", 200), "h": t.get("h", 240)}

    def luc(self, t):
        if not self.mau:
            return self.mac_dinh
        m = min(self.mau, key=lambda x: abs(x["t"] - t))
        return m if abs(m["t"] - t) < 1.0 else self.mac_dinh

    def trung_vi(self, a, b):
        o = [m for m in self.mau if a <= m["t"] < b]
        if not o:
            return self.luc((a + b) / 2)
        o.sort(key=lambda m: m["cx"]); cx = o[len(o) // 2]["cx"]
        o.sort(key=lambda m: m["cy"]); cy = o[len(o) // 2]["cy"]
        return {"cx": cx, "cy": cy, "w": o[0]["w"], "h": o[0]["h"]}


def doc_phu_de(p):
    ra = []
    for d in Path(p).read_text("utf-8").splitlines():
        d = d.strip()
        if not d or d.startswith("#"):
            continue
        a, b, chu = d.split("|", 2)
        ra.append((float(a), float(b), chu.strip()))
    return ra


def chu_nhan(chu):
    """*từ* → <b>từ</b> (màu nhấn)."""
    return re.sub(r"\*([^*]+)\*", lambda m: f"<b>{e(m.group(1))}</b>", e(chu).replace("&#x27;", "'"))


def co_pd(chu, co):
    """Cụm phụ đề dài → thu cỡ chữ cho vừa MỘT dòng trong khung 150–930 px (không xuống dòng mồ côi, không lấn cột nút
    phải). Britti Bold + viền 11 px ≈ 0,5 × cỡ chữ mỗi ký tự (đo video 012: 23 ký tự ở 74 px rộng ~830 px)."""
    n = len(chu.replace("*", ""))
    vua = int(760 / (0.5 * max(n, 1)))
    return f' style="font-size:{vua}px;white-space:nowrap"' if vua < co else ""


def chuan_bi_am(src, dich):
    """Cắt khoảng lặng đầu file hiệu ứng (nhiều file myinstants trễ 0,1–0,4 s) để tiếng đập đúng nhịp."""
    if dich.exists():
        return
    dich.parent.mkdir(parents=True, exist_ok=True)
    chay(["ffmpeg", "-y", "-v", "error", "-i", src, "-af",
          "silenceremove=start_periods=1:start_threshold=-45dB,aresample=48000", "-ac", "2", dich], "chuẩn bị âm " + src.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("du_an")
    ap.add_argument("--nhap", action="store_true", help="nháp 15 khung/giây (nhanh ~2×) → build/nhap.mp4")
    ap.add_argument("--doan", help="chỉ dựng một đoạn, vd 28-35 (giây trên bản cắt) → build/doan-28-35.mp4")
    ap.add_argument("--chi-nhac", action="store_true")
    g = ap.parse_args()
    da = du_an(g.du_an)
    cfg = doc_json(da / "dung.json")
    hf = da / "build" / "hf"
    ra_hinh = da / "build" / "hf-ra.mp4"
    ra = da / "build" / "nhap.mp4" if g.nhap else GOC / "05-output" / f"{cfg.get('ten', da.name)}.mp4"

    if g.doan:  # dựng một khúc để soi nhanh — không đụng thành phẩm, không trộn nhạc
        try:
            a, b = (float(x.replace(",", ".")) for x in g.doan.split("-"))
            assert 0 <= a < b
        except Exception:
            print("✗ --doan phải dạng A-B, vd 28-35"); sys.exit(1)
        dung_hf(da, cfg, hf)
        ra_doan = da / "build" / f"doan-{g.doan}.mp4"
        print(f"dựng đoạn {a:g}–{b:g}s (HyperFrames) …")
        hf_render(hf, ra_doan, ["--quality", "draft", "--start", f"{a}", "--end", f"{b}"])
        print(f"✓ {ra_doan}  {do(ra_doan)['giay']:.1f}s (tiếng nói gốc, chưa có nhạc)")
        return

    if not g.chi_nhac:
        dung_hf(da, cfg, hf)
        print("dựng hình (HyperFrames) …")
        hf_render(hf, ra_hinh, ["--quality", "draft", "--fps", "15"] if g.nhap else ["--quality", "delivery"])
    tron_nhac(cfg, ra_hinh, ra)
    i = do(ra)
    print(f"✓ {ra}  {i['w']}×{i['h']} · {i['giay']:.1f}s")
    if not g.nhap and gan_bia(ra, da / "anh-bia.jpg"):
        print(f"  + đã nhúng ảnh bìa {da / 'anh-bia.jpg'}")


def hf_render(hf, ra, them):
    r = subprocess.run([str(HF), "render", str(hf), "-o", str(ra)] + them,
                       env=ENV_HF, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("\n".join(l for l in r.stdout.splitlines() if "rendered in" in l or "✗" in l or "Failed" in l)[-800:])
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-2000:]); sys.exit(1)


def muc_db(f):
    """Mức trung bình (dB) của phần CÓ TIẾNG — bỏ khoảng lặng để video nhiều lặng không bị đo thấp."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-af",
                        "silenceremove=stop_periods=-1:stop_threshold=-45dB,volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r)
    return float(m.group(1)) if m else -20.0


def tron_nhac(cfg, vao, ra):
    nhac = cfg.get("nhac")
    ra.parent.mkdir(parents=True, exist_ok=True)
    tong = do(vao)["giay"]
    if not nhac:
        loc = "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]"
        lenh = ["ffmpeg", "-y", "-v", "error", "-i", vao]
    else:
        f = GOC / nhac["file"]
        # đoạn sạch của bản nhạc (bỏ tiếng vút logo kết ở cuối video mẫu) — lấy từ muc-luc.json nếu không ghi
        ml = doc_json(f.parent / "muc-luc.json", {"nhac": []})
        sach = next((n.get("doan_sach") for n in ml["nhac"] if n["file"] == f.name), None) or [0, do(f)["giay"]]
        a0 = float(nhac.get("bat_dau", sach[0]))
        a1 = float(nhac.get("het", sach[1]))
        doan_nhac = vao.parent / "nhac-doan.wav"
        chay(["ffmpeg", "-y", "-v", "error", "-i", f, "-ss", str(a0), "-to", str(a1), "-ar", "48000", "-ac", "2", doan_nhac],
             "cắt đoạn nhạc")
        # mức nhạc: mặc định thấp hơn giọng 11 dB — trung vị đo ở 7 video mẫu của anh Trường (−7…−12 dB)
        if "am_luong" in nhac:
            am = float(nhac["am_luong"])
        else:
            lech = muc_db(doan_nhac) - muc_db(vao)
            am = round(10 ** ((float(nhac.get("duoi_giong_db", -11)) - lech) / 20), 3)
            print(f"nhạc: {f.name} [{a0:.1f}–{a1:.1f}s] · hệ số {am} (nhạc thấp hơn giọng {-float(nhac.get('duoi_giong_db', -11))} dB)")
        loc = (f"[1:a]volume={am},afade=t=in:d=0.6,afade=t=out:st={max(0, tong - 1.8):.2f}:d=1.8[m];"
               f"[m][0:a]sidechaincompress=threshold=0.05:ratio=3:attack=10:release=350[md];"
               f"[0:a][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
        lenh = ["ffmpeg", "-y", "-v", "error", "-i", vao, "-stream_loop", "-1", "-i", doan_nhac]
    chay(lenh + ["-filter_complex", loc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                 "-ar", "48000", "-t", f"{tong:.3f}", "-movflags", "+faststart", ra], "trộn nhạc")


# ───────────────────────────────────────────── dựng composition ─────────────────────────────────────────────

def dung_hf(da, cfg, hf):
    (hf / "assets" / "sfx").mkdir(parents=True, exist_ok=True)
    (hf / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
    shutil.copy2(da / "build" / "da-cat.mp4", hf / "assets" / "talk.mp4")
    shutil.copy2(CONG_CU / "vendor" / "gsap.min.js", hf / "assets" / "gsap.min.js")
    for f in (CONG_CU / "fonts").glob("*.woff2"):
        shutil.copy2(f, hf / "assets" / "fonts" / f.name)

    moc = doc_json(da / "build" / "moc-cat.json")
    tong = moc["tong"]
    mat = Mat(da / "build" / "mat.json")
    pd = doc_phu_de(da / "phu-de.txt")
    nhip = sorted(cfg.get("nhip", []), key=lambda n: n["t"])
    can = float(cfg.get("can", 1.14))
    doi_khung = cfg.get("cat_doi_khung", True)
    pd_cfg = {"y": 0.60, "co": 74, "nhan": VANG, **cfg.get("phu_de", {})}

    # ── khung nói: rộng/cận xen kẽ ở mỗi điểm cắt, tâm phóng = mặt ──
    doan_t = [0.0] + moc["diem_cat"] + [tong]
    # doi_khung_cach: chỉ đổi rộng↔cận khi lần đổi trước đã cách ≥ X giây — bản cắt dày (bỏ từng khoảng lặng)
    # có điểm cắt mỗi 1–2 s, đổi ở mọi điểm thì khung giật liên tục. 0 = đổi ở mọi điểm cắt (như cũ).
    cach = float(cfg.get("doi_khung_cach", 0))
    khung = []  # (a, b, scale, ox, oy)
    cap, lan_doi = 0, 0.0
    for i in range(len(doan_t) - 1):
        a, b = doan_t[i], doan_t[i + 1]
        if i > 0 and a - lan_doi >= cach - 1e-6:
            cap, lan_doi = cap ^ 1, a
        m = mat.trung_vi(a, b)
        s = can if (doi_khung and cap == 1) else 1.0
        khung.append((a, b, s, m["cx"], m["cy"]))

    def scale_luc(t):
        for a, b, s, ox, oy in khung:
            if a <= t < b:
                return s, ox, oy
        return khung[-1][2:]

    def chia_doi_luc(t):
        return any(n["t"] <= t < n["t"] + n.get("dai", 0) and n.get("kieu", mac_kieu(n)) in NUA_TREN for n in nhip)

    def y_mat_sau_phong(t):
        s, ox, oy = scale_luc(t)
        m = mat.luc(t)
        tren = oy + (m["cy"] - m["h"] * 0.6 - oy) * s
        duoi = oy + (m["cy"] + m["h"] * 0.75 - oy) * s
        return tren, duoi

    js, the, am_list = [], [], []
    z = 10

    # phụ đề
    for k, (a, b, chu) in enumerate(pd):
        if chia_doi_luc(a):
            y = 980
        else:
            y = int(H * pd_cfg["y"])
            tren, duoi = y_mat_sau_phong(a)
            if duoi + 30 > y - 60:              # mặt (cận) chạm vùng chữ → đẩy xuống dưới cằm
                y = int(duoi + 100)
            if y > AN_TOAN["duoi"] - 80:        # xuống quá vùng UI đáy → đặt trên đầu
                y = max(int(tren - 110), AN_TOAN["tren"] + 80)
                # …nhưng trên đầu đang có tiêu đề / hook → về ngang cổ (che cằm còn hơn đè chữ lên chữ)
                if any(n["loai"] in ("tieu-de", "mo-dau") and n["t"] - 0.1 <= a < n["t"] + n.get("dai", 0)
                       for n in nhip):
                    y = AN_TOAN["duoi"] - 100
        the.append(f'<div id="pd{k}" class="clip lop" data-start="{a:.3f}" data-duration="{max(0.1, b - a):.3f}" '
                   f'data-track-index="20" style="z-index:50"><div class="pd" style="top:{y}px"><span{co_pd(chu, pd_cfg["co"])}>'
                   f'{chu_nhan(chu)}</span></div></div>')
        js.append(f'tl.fromTo("#pd{k} span",{{scale:.72,opacity:0}},{{scale:1,opacity:1,duration:.13,ease:"back.out(2.6)"}},{a:.3f});')

    # nhịp
    for k, n in enumerate(nhip):
        loai, t, dai = n["loai"], float(n["t"]), float(n.get("dai", 2.0))
        nid = f"n{k}"
        if loai == "am":
            am_list.append((n["file"], t, n.get("am_luong", 0.6)))
            continue
        am = n.get("am", AM_MAC_DINH.get(loai))
        if am:
            am_list.append((am, t, n.get("am_luong_am", 0.55)))
        z += 1
        fn = KHOI.get(loai)
        if fn is None:
            print(f"✗ loại nhịp lạ: {loai}"); sys.exit(1)
        h_, j_ = fn(nid, n, t, dai, z, da, hf, mat)
        the.append(h_); js.append(j_)
        if n.get("kieu", mac_kieu(n)) in NUA_TREN:        # chia đôi: dời người xuống nửa dưới
            m = mat.trung_vi(t, t + dai)
            dy = max(0, min(900, 1250 - m["cy"]))
            # hai nhịp chia đôi nối liền (cách < 0,3 s) → người nói ĐỨNG YÊN ở nửa dưới, không nhảy lên rồi xuống
            ke_truoc = any(x is not n and x.get("kieu", mac_kieu(x)) in NUA_TREN
                           and 0 <= t - (x["t"] + x.get("dai", 2.0)) < 0.3 for x in nhip)
            ke_sau = any(x is not n and x.get("kieu", mac_kieu(x)) in NUA_TREN
                         and 0 <= x["t"] - (t + dai) < 0.3 for x in nhip)
            js.append(f'tl.to("#khung-noi",{{y:{dy},duration:{0.12 if ke_truoc else 0.28},ease:"power3.inOut"}},{t:.3f});')
            if not ke_sau:
                js.append(f'tl.to("#khung-noi",{{y:0,duration:.25,ease:"power3.inOut"}},{t + dai - 0.25:.3f});')
        if loai == "phong-to":
            s0, _, _ = scale_luc(t)
            js.append(f'tl.to("#khung-noi",{{scale:{n.get("muc", 1.3)},duration:.16,ease:"power3.out"}},{t:.3f});'
                      f'tl.to("#khung-noi",{{scale:{scale_luc(t + dai)[0]},duration:.14,ease:"power2.inOut"}},{t + dai:.3f});')

    # khung rộng/cận (đặt SAU phong-to để mốc cắt thắng nếu trùng)
    js_khung = [f'tl.set("#khung-noi",{{scale:{s},transformOrigin:"{ox}px {oy}px"}},{a:.3f});' for a, b, s, ox, oy in khung]

    # âm thanh hiệu ứng
    for i, (f, t, vol) in enumerate(am_list):
        src = KHO_AM / "myinstants" / f if not Path(f).is_absolute() and not (GOC / f).exists() else (GOC / f)
        if not src.exists():
            print(f"✗ không có file âm {f}"); sys.exit(1)
        dich = hf / "assets" / "sfx" / (src.stem + ".wav")
        chuan_bi_am(src, dich)
        dai_am = min(do(dich)["giay"], tong - t)
        if dai_am <= 0.05:
            continue
        the.append(f'<audio id="am{i}" class="clip" src="assets/sfx/{dich.name}" data-start="{t:.3f}" '
                   f'data-duration="{dai_am:.3f}" data-track-index="40" data-volume="{vol}"></audio>')

    trang = MAU_HTML.replace("{{TONG}}", f"{tong:.3f}").replace("{{THE}}", "\n  ".join(the)) \
        .replace("{{JS}}", "\n".join(js_khung + js)).replace("{{PD_CO}}", str(pd_cfg["co"])) \
        .replace("{{PD_NHAN}}", pd_cfg["nhan"])
    (hf / "index.html").write_text(trang, "utf-8")
    print(f"composition: {len(pd)} cụm phụ đề · {len(nhip)} nhịp · {len(am_list)} hiệu ứng âm · {len(khung)} đoạn khung")


def mac_kieu(n):
    return {"mo-phong": "nua-tren", "bieu-do": "nua-tren"}.get(n["loai"], "toan-man" if n["loai"] in ("canh-phu", "anh") else "")


def tieu_de_html(chu, co=None):
    dong = str(chu).split("\n")
    dai = max(len(d) for d in dong)
    co = co or (150 if dai <= 9 else 124 if dai <= 13 else 100)
    return "".join(f'<div class="td-dong" style="font-size:{co}px">{chu_nhan(d)}</div>' for d in dong)


# ── các khối nhịp: mỗi hàm trả (html, js) ──

def k_mo_dau(nid, n, t, dai, z, *_):
    # khung chữ chừa 140 px hai bên (cột nút TikTok) → dòng 1 dài thì hạ "co" (mặc định 96 px) để khỏi xuống hàng
    co1 = f' style="font-size:{int(n["co"])}px"' if n.get("co") else ""
    h_ = (f'<div id="{nid}" class="clip lop" data-start="{t}" data-duration="{dai}" style="z-index:{z}"><div class="mo-dau">'
          f'<div class="md1"{co1}>{chu_nhan(n["dong1"])}</div>' + (f'<div class="md2">{chu_nhan(n["dong2"])}</div>' if n.get("dong2") else "")
          + '</div></div>')
    j_ = (f'tl.fromTo("#{nid} .md1",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"power3.out"}},{t});'
          f'tl.fromTo("#{nid} .md2",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"power3.out"}},{t + .15});'
          f'tl.to("#{nid} .mo-dau > div",{{opacity:0,duration:.2}},{t + dai - .25});')
    return h_, j_


def k_tieu_de(nid, n, t, dai, z, *_):
    mau = n.get("mau", "trang-do")
    y = int(H * n.get("y", 0.27))
    h_ = (f'<div id="{nid}" class="clip lop td-{mau}" data-start="{t}" data-duration="{dai}" style="z-index:{z}">'
          f'<div class="td" style="top:{y}px"><div class="td-in">{tieu_de_html(n["chu"], n.get("co"))}</div></div></div>')
    j_ = (f'tl.fromTo("#{nid} .td-in",{{scale:2.1,opacity:0,rotation:-5}},{{scale:1,opacity:1,rotation:0,duration:.26,ease:"power4.out"}},{t});'
          f'tl.to("#{nid} .td-in",{{scale:1.04,duration:{max(.2, dai - .6):.2f},ease:"none"}},{t + .26});'
          f'tl.to("#{nid} .td-in",{{opacity:0,scale:.9,duration:.16}},{t + dai - .2});')
    return h_, j_


def copy_asset(da, hf, src):
    p = (da / src) if (da / src).exists() else (GOC / src)
    if not p.exists():
        print(f"✗ không có file {src}"); sys.exit(1)
    (hf / "assets" / "phu").mkdir(parents=True, exist_ok=True)
    dich = hf / "assets" / "phu" / p.name
    if not dich.exists() or dich.stat().st_mtime < p.stat().st_mtime:
        shutil.copy2(p, dich)
    return f"assets/phu/{p.name}"


def k_canh(nid, n, t, dai, z, da, hf, mat):
    src = copy_asset(da, hf, n["src"])
    kieu = n.get("kieu", "toan-man")
    extra = f'data-media-start="{n.get("bat_dau", 0)}"'
    la_video = Path(src).suffix.lower() in (".mp4", ".mov", ".webm")
    if la_video:
        # video là clip trực tiếp, mang luôn khung/viền — bọc trong div không có thời gian thì viền hiện suốt video
        h_ = (f'<video id="{nid}-v" class="clip phu phu-{kieu} phu-vid" src="{src}" data-start="{t}" data-duration="{dai}" '
              f'{extra} data-track-index="{z}" muted playsinline style="z-index:{z}"></video>')
    else:
        h_ = (f'<div class="clip lop" data-start="{t}" data-duration="{dai}" style="z-index:{z}">'
              f'<div id="{nid}" class="phu phu-{kieu}"><img id="{nid}-v" class="phu-media" src="{src}" alt=""></div></div>')
    sel = f"#{nid}-v"
    vao = {"toan-man": "{opacity:0,scale:1.12},{opacity:1,scale:1,duration:.22,ease:\"power2.out\"}",
           "nua-tren": "{yPercent:-100},{yPercent:0,duration:.28,ease:\"power3.out\"}",
           "khung": "{scale:.6,opacity:0,rotation:-3},{scale:1,opacity:1,rotation:0,duration:.3,ease:\"back.out(1.8)\"}"}[kieu]
    if not la_video and kieu != "toan-man":
        sel = f"#{nid}"           # ảnh trong khung: động cả khung, ảnh bên trong chạy Ken Burns
    j_ = f'tl.fromTo("{sel}",{vao},{t});'
    if not la_video:
        j_ += f'tl.fromTo("#{nid}-v",{{scale:1}},{{scale:1.08,duration:{dai:.2f},ease:"none"}},{t});'   # Ken Burns
    if kieu == "nua-tren":
        j_ += f'tl.to("{sel}",{{yPercent:-100,duration:.25,ease:"power3.in"}},{t + dai - .25});'
    elif kieu == "khung":
        j_ += f'tl.to("{sel}",{{scale:.8,opacity:0,duration:.18}},{t + dai - .2});'
    return h_, j_


def k_dan(nid, n, t, dai, z, da, hf, mat):
    src = copy_asset(da, hf, n["src"])
    x, y, rong = n.get("x", 0.72), n.get("y", 0.2), n.get("rong", 300)
    h_ = (f'<div id="{nid}" class="clip lop" data-start="{t}" data-duration="{dai}" style="z-index:{z}">'
          f'<div class="dan" style="left:{int(W * x - rong / 2)}px;top:{int(H * y)}px;width:{rong}px">'
          f'<img src="{src}" alt="" style="width:100%"></div></div>')
    j_ = (f'tl.fromTo("#{nid} img",{{scale:0,rotation:-12}},{{scale:1,rotation:4,duration:.32,ease:"back.out(2.2)"}},{t});'
          f'tl.to("#{nid} img",{{rotation:-2,duration:{max(.3, dai - .6):.2f},ease:"sine.inOut"}},{t + .32});'
          f'tl.to("#{nid} img",{{scale:0,duration:.16}},{t + dai - .2});')
    return h_, j_


def k_the_so(nid, n, t, dai, z, *_):
    y = int(H * n.get("y", 0.24))
    so = float(n["so"])
    thap_phan = int(n.get("thap_phan", 0 if so == int(so) else 1))
    h_ = (f'<div id="{nid}" class="clip lop" data-start="{t}" data-duration="{dai}" style="z-index:{z}">'
          f'<div class="the-so" style="top:{y}px"><div class="ts-in">' + (f'<div class="ts-truoc">{chu_nhan(n["truoc"])}</div>' if n.get("truoc") else "")
          + f'<div class="ts-so"><span class="ts-gt">0</span><span class="ts-dv">{e(n.get("don_vi", ""))}</span></div>'
          + (f'<div class="ts-nhan">{chu_nhan(n["nhan"])}</div>' if n.get("nhan") else "") + '</div></div></div>')
    j_ = (f'tl.fromTo("#{nid} .ts-in",{{scale:.5,opacity:0}},{{scale:1,opacity:1,duration:.28,ease:"back.out(2)"}},{t});'
          f'(function(){{const el=document.querySelector("#{nid} .ts-gt"),o={{v:0}};'
          f'tl.fromTo(o,{{v:0}},{{v:{so},duration:{min(1.2, dai * .5):.2f},ease:"power2.out",onUpdate:()=>{{'
          f'el.textContent=o.v.toLocaleString("vi-VN",{{minimumFractionDigits:{thap_phan},maximumFractionDigits:{thap_phan}}})}}}},{t + .1});}})();'
          f'tl.to("#{nid} .ts-in",{{opacity:0,y:-30,duration:.18}},{t + dai - .22});')
    return h_, j_


def k_bieu_do(nid, n, t, dai, z, *_):
    cot = n["cot"]
    lon = max(c["gia_tri"] for c in cot)
    hang = "".join(
        f'<div class="bd-hang"><div class="bd-nhan">{e(c["nhan"])}</div><div class="bd-ray">'
        f'<div class="bd-cot bd-{c.get("mau", "do")}" style="width:{max(4, 100 * c["gia_tri"] / lon):.1f}%"></div>'
        f'<div class="bd-gt">{e(c.get("hien", c["gia_tri"]))} {e(n.get("don_vi", ""))}</div></div></div>' for c in cot)
    h_ = (f'<div id="{nid}" class="clip lop" data-start="{t}" data-duration="{dai}" style="z-index:{z}"><div class="bd">'
          f'<div class="bd-in"><div class="bd-td">{chu_nhan(n.get("tieu_de", ""))}</div>{hang}'
          + (f'<div class="bd-nguon">{e(n["nguon"])}</div>' if n.get("nguon") else "") + '</div></div></div>')
    j_ = (f'tl.fromTo("#{nid} .bd-in",{{yPercent:-100}},{{yPercent:0,duration:.3,ease:"power3.out"}},{t});'
          f'tl.fromTo("#{nid} .bd-cot",{{scaleX:0}},{{scaleX:1,duration:.7,ease:"power3.out",stagger:.18}},{t + .3});'
          f'tl.fromTo("#{nid} .bd-gt",{{opacity:0}},{{opacity:1,duration:.2,stagger:.18}},{t + .7});'
          f'tl.to("#{nid} .bd-in",{{yPercent:-100,duration:.25,ease:"power3.in"}},{t + dai - .25});')
    return h_, j_


def k_cua_so(nid, n, t, dai, z, *_):
    y = int(H * n.get("y", 0.2))
    nut = "".join(f'<span class="cs-nut{" cs-chinh" if i == 0 else ""}">{e(b)}</span>' for i, b in enumerate(n.get("nut", ["OK"])))
    h_ = (f'<div id="{nid}" class="clip lop" data-start="{t}" data-duration="{dai}" style="z-index:{z}">'
          f'<div class="cs" style="top:{y}px"><div class="cs-in"><div class="cs-thanh"><span></span><span></span><span></span>'
          f'<b>{e(n.get("tieu_de", ""))}</b></div><div class="cs-than">{chu_nhan(n.get("noi_dung", ""))}</div>'
          f'<div class="cs-nuts">{nut}</div></div></div></div>')
    j_ = (f'tl.fromTo("#{nid} .cs-in",{{scale:.4,opacity:0}},{{scale:1,opacity:1,duration:.3,ease:"back.out(2)"}},{t});'
          f'tl.fromTo("#{nid} .cs-chinh",{{scale:1}},{{scale:.92,duration:.08,yoyo:true,repeat:1}},{t + dai - .55});'
          f'tl.to("#{nid} .cs-in",{{scale:.6,opacity:0,duration:.16}},{t + dai - .2});')
    return h_, j_


def k_mo_phong(nid, n, t, dai, z, *_):
    """Mô phỏng nhìn từ trên xuống: bếp → robot phục vụ chạy tới các bàn → về bếp (nửa trên màn hình)."""
    so_ban = int(n.get("so_ban", 6))
    cot_ = 3
    ban = []
    for i in range(so_ban):
        r, c = divmod(i, cot_)
        ban.append((180 + c * 360, 330 + r * 230))
    den = n.get("ban_den", [min(3, so_ban), so_ban])
    bep = (540, 150)
    duong = [bep] + [(ban[b - 1][0], ban[b - 1][1] - 95) for b in den] + [bep]
    svg_ban = "".join(f'<g><rect x="{x - 80}" y="{y - 55}" width="160" height="110" rx="18" class="mp-ban"/>'
                      f'<text x="{x}" y="{y + 16}" class="mp-so">{i + 1}</text></g>' for i, (x, y) in enumerate(ban))
    pts = " ".join(f"{x},{y}" for x, y in duong)
    chieu_cao = 330 + ((so_ban - 1) // cot_) * 230 + 110
    h_ = (f'<div id="{nid}" class="clip lop" data-start="{t}" data-duration="{dai}" style="z-index:{z}"><div class="mp">'
          f'<div class="mp-in"><svg viewBox="0 0 1080 {chieu_cao}" width="1080" height="{min(900, chieu_cao)}">'
          f'<rect x="300" y="40" width="480" height="110" rx="16" class="mp-bep"/><text x="540" y="112" class="mp-chu-bep">BẾP</text>'
          f'{svg_ban}<polyline points="{pts}" class="mp-vet" pathLength="1"/>'
          f'<g class="mp-robot"><circle r="46" class="mp-than"/><rect x="-26" y="-18" width="52" height="30" rx="10" fill="#111"/>'
          f'<circle cx="-11" cy="-3" r="6" fill="#5ef"/><circle cx="11" cy="-3" r="6" fill="#5ef"/></g></svg>'
          + (f'<div class="mp-nhan">{chu_nhan(n["chu"])}</div>' if n.get("chu") else "") + '</div></div></div>')
    buoc = (dai - 0.9) / max(1, len(duong) - 1)
    j_ = [f'tl.fromTo("#{nid} .mp-in",{{yPercent:-100}},{{yPercent:0,duration:.3,ease:"power3.out"}},{t});',
          f'tl.set("#{nid} .mp-robot",{{x:{bep[0]},y:{bep[1]}}},{t});',
          f'tl.fromTo("#{nid} .mp-vet",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dai - 0.9:.2f},ease:"none"}},{t + .35});']
    for i, (x, y) in enumerate(duong[1:]):
        j_.append(f'tl.to("#{nid} .mp-robot",{{x:{x},y:{y},duration:{buoc * 0.8:.2f},ease:"power1.inOut"}},{t + .35 + i * buoc:.2f});')
    j_.append(f'tl.to("#{nid} .mp-in",{{yPercent:-100,duration:.25,ease:"power3.in"}},{t + dai - .25});')
    return h_, "".join(j_)


def k_html(nid, n, t, dai, z, da, hf, mat):
    """Khối tự viết cho từng video: file HTML chứa markup + <script> định nghĩa window.khoi(tl, t0, dai, goc)."""
    noi = (da / n["file"]).read_text("utf-8")
    h_ = (f'<div id="{nid}" class="clip khoi-rieng" data-start="{t}" data-duration="{dai}" style="z-index:{z}">'
          f'{noi}</div>')
    j_ = f'window.__khoi && window.__khoi["{n.get("ten", Path(n["file"]).stem)}"](tl,{t},{dai},document.getElementById("{nid}"));'
    return h_, j_


def k_trong(nid, n, t, dai, z, *_):
    return "", ""


KHOI = {"mo-dau": k_mo_dau, "tieu-de": k_tieu_de, "canh-phu": k_canh, "anh": k_canh, "dan": k_dan,
        "the-so": k_the_so, "bieu-do": k_bieu_do, "cua-so": k_cua_so, "mo-phong": k_mo_phong, "html": k_html,
        "phong-to": k_trong}

MAU_HTML = r"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{font-family:"Britti";src:url("assets/fonts/DFVN-BrittiSans-Bold.woff2") format("woff2");font-weight:700}
@font-face{font-family:"Britti";src:url("assets/fonts/DFVN-BrittiSans-SemiBold.woff2") format("woff2");font-weight:600}
@font-face{font-family:"Britti";src:url("assets/fonts/DFVN-BrittiSans-Regular.woff2") format("woff2");font-weight:400}
@font-face{font-family:"Neusharp";src:url("assets/fonts/1FTV-VIP-NEUSHARP-BOLD.woff2") format("woff2");font-weight:700}
#root{position:absolute;inset:0;background:#000;overflow:hidden;font-family:"Britti"}
#khung-noi{position:absolute;left:0;top:0;width:1080px;height:1920px}
#talk{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
/* phụ đề: trắng viền đen, từ nhấn vàng — đúng phong cách 7 video mẫu */
.pd{position:absolute;left:150px;right:150px;height:0;display:flex;align-items:center;justify-content:center;text-align:center}
.pd span{display:inline-block;font:700 {{PD_CO}}px/1.12 "Britti";color:#fff;-webkit-text-stroke:11px #000;paint-order:stroke fill;
  text-shadow:0 6px 16px rgba(0,0,0,.5);max-width:900px}
.pd b{color:{{PD_NHAN}}}
/* tiêu đề lớn bật lên */
.td{position:absolute;left:40px;right:40px;height:0;display:flex;align-items:center;justify-content:center;text-align:center}
.td-in{display:inline-block}
.td-dong{font-family:"Neusharp";font-weight:700;line-height:1.02;text-transform:uppercase;paint-order:stroke fill;
  -webkit-text-stroke:14px #000;filter:drop-shadow(0 10px 0 rgba(0,0,0,.35))}
.td-trang-do .td-dong{color:#fff;-webkit-text-stroke-color:#E83636}
.td-vang .td-dong{color:#FFD43B}
.td-trang .td-dong{color:#fff}
.td-do .td-dong{color:#E83636;-webkit-text-stroke-color:#fff}
.td-dong b{color:#FFD43B}
/* tiêu đề mở đầu (hook) */
.mo-dau{position:absolute;left:140px;right:140px;top:300px;text-align:center}
.md1{font:700 96px/1.05 "Neusharp";text-transform:uppercase;color:#E83636;-webkit-text-stroke:12px #fff;paint-order:stroke fill;
  filter:drop-shadow(0 8px 0 rgba(0,0,0,.35))}
.md2{margin-top:14px;font:700 62px/1.1 "Britti";color:#fff;-webkit-text-stroke:9px #000;paint-order:stroke fill}
.md1 b,.md2 b{color:#FFD43B}
/* cảnh phụ */
.phu{position:absolute;overflow:hidden}
.phu-toan-man{left:0;top:0;width:1080px;height:1920px}
.phu-nua-tren{left:0;top:0;width:1080px;height:960px;border-bottom:8px solid #E83636}
.phu-khung{left:90px;top:250px;width:900px;height:660px;border-radius:36px;border:8px solid #fff;box-shadow:0 30px 60px rgba(0,0,0,.5)}
.phu-media{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover}
.phu-vid{object-fit:cover}
.dan{position:absolute}
.dan img{border:10px solid #fff;border-radius:28px;box-shadow:0 20px 40px rgba(0,0,0,.45)}
/* thẻ số */
.the-so{position:absolute;left:0;right:0;height:0;display:flex;align-items:center;justify-content:center;text-align:center}
.ts-in{display:inline-block;padding:34px 60px 38px;border-radius:40px;background:rgba(17,9,9,.86);border:5px solid #E83636;
  box-shadow:0 0 80px rgba(232,54,54,.45)}
.ts-truoc{font:600 52px/1.1 "Britti";color:#fff}
.ts-so{font:700 210px/1 "Neusharp";color:#FFD43B;margin:6px 0}
.ts-dv{font-size:120px;margin-left:8px;color:#fff}
.ts-nhan{font:700 54px/1.15 "Britti";color:#fff;max-width:820px}
.ts-truoc b,.ts-nhan b{color:#FFD43B}
/* biểu đồ (nửa trên) */
.bd{position:absolute;left:0;top:0;width:1080px;height:960px;overflow:hidden}
.bd-in{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 120%,rgba(232,54,54,.45),transparent 60%),#110909;
  padding:230px 70px 0;border-bottom:8px solid #E83636}
.bd-td{font:700 60px/1.1 "Britti";color:#fff;margin-bottom:50px}
.bd-td b{color:#FFD43B}
.bd-hang{margin-bottom:38px}
.bd-nhan{font:600 44px/1 "Britti";color:#ddd;margin-bottom:14px}
.bd-ray{display:flex;align-items:center;gap:22px}
.bd-cot{height:86px;border-radius:14px;transform-origin:left center}
.bd-do{background:linear-gradient(90deg,#C13F28,#E83636)}
.bd-xam{background:#6b6461}
.bd-vang{background:#FFD43B}
.bd-gt{font:700 60px/1 "Neusharp";color:#fff;white-space:nowrap}
.bd-nguon{position:absolute;left:70px;bottom:24px;font:400 26px "Britti";color:#998}
/* cửa sổ giao diện bật lên */
.cs{position:absolute;left:0;right:0;display:flex;justify-content:center}
.cs-in{width:820px;border-radius:30px;background:#fff;box-shadow:0 30px 80px rgba(0,0,0,.55);overflow:hidden}
.cs-thanh{display:flex;align-items:center;gap:12px;padding:22px 30px;background:#5E0F18;color:#fff;font:700 38px "Britti"}
.cs-thanh span{width:20px;height:20px;border-radius:50%;background:#FAB29A}
.cs-thanh span:first-child{background:#E83636}
.cs-thanh b{margin-left:14px}
.cs-than{padding:40px 44px 20px;font:600 50px/1.25 "Britti";color:#1a1010}
.cs-than b{color:#C13F28}
.cs-nuts{display:flex;justify-content:flex-end;gap:20px;padding:10px 44px 36px}
.cs-nut{padding:16px 42px;border-radius:18px;background:#eee;font:700 40px "Britti";color:#333}
.cs-chinh{background:#E83636;color:#fff}
/* mô phỏng robot phục vụ */
.mp{position:absolute;left:0;top:0;width:1080px;height:960px;overflow:hidden}
.mp-in{position:absolute;inset:0;background:#110909;border-bottom:8px solid #E83636;padding-top:40px}
.mp-in svg{display:block;margin:0 auto}
.mp-bep{fill:#5E0F18;stroke:#E83636;stroke-width:4}
.mp-chu-bep{font:700 54px "Neusharp";fill:#fff;text-anchor:middle}
.mp-ban{fill:#2a1e1c;stroke:#6b5a55;stroke-width:3}
.mp-so{font:700 50px "Neusharp";fill:#bba;text-anchor:middle}
.mp-vet{fill:none;stroke:#FFD43B;stroke-width:8;stroke-dasharray:1 1;stroke-linecap:round;opacity:.85}
.mp-than{fill:#fff;stroke:#E83636;stroke-width:8}
.mp-nhan{position:absolute;left:60px;right:60px;bottom:30px;text-align:center;font:700 50px/1.15 "Britti";color:#fff}
.mp-nhan b{color:#FFD43B}
.khoi-rieng{position:absolute;inset:0}
.lop{position:absolute;left:0;top:0;width:1080px;height:1920px}
</style></head>
<body>
<script src="assets/gsap.min.js"></script>
<div id="root" data-composition-id="main" data-start="0" data-duration="{{TONG}}" data-width="1080" data-height="1920">
  <div id="khung-noi">
    <video id="talk" class="clip" src="assets/talk.mp4" data-start="0" data-duration="{{TONG}}" data-track-index="1"
      playsinline data-has-audio="true"></video>
  </div>
  {{THE}}
</div>
<script>
window.__khoi = window.__khoi || {};
const tl = gsap.timeline({paused:true});
{{JS}}
window.__timelines["main"] = tl;
</script>
</body></html>
"""

if __name__ == "__main__":
    main()

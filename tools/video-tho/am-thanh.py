# -*- coding: utf-8 -*-
"""Kho hiệu ứng âm thanh lấy từ myinstants.com (anh Trường chọn nguồn này 15/11/2026).

    python am-thanh.py tim whoosh                 # xem kết quả tìm, chưa tải
    python am-thanh.py tai whoosh --so 4 --nhom chuyen-canh
    python am-thanh.py bo-khoi-dau                # tải bộ cơ bản cho video nói-trước-camera
    python am-thanh.py liet-ke                    # mọi âm thanh đã có + độ dài

Kho: 02-media/am-thanh/myinstants/<nhom>/<ten>.mp3, mục lục ở muc-luc.json cùng thư mục.
File mp3 không đưa vào git (tải lại được bằng `python am-thanh.py tai-lai`), mục lục thì có.

⚠ Âm thanh trên myinstants do người dùng tải lên, nhiều cái trích từ phim/game/meme có bản quyền.
Video đăng kênh công ty → ưu tiên nhóm "hiệu ứng" thuần (whoosh, pop, ding…), tránh đoạn trích lời thoại/nhạc phim.
"""
import argparse, html, json, re, subprocess, sys, time, urllib.parse, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
GOC = "https://www.myinstants.com"
KHO = Path(__file__).resolve().parents[2] / "02-media" / "am-thanh" / "myinstants"
MUC_LUC = KHO / "muc-luc.json"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Bộ cơ bản: (nhóm, từ khoá tìm, số lấy). Dùng cho phong cách CapCut của kênh Duy Trường Robot.
BO_KHOI_DAU = [
    ("chuyen-canh", "whoosh", 4),
    ("chuyen-canh", "swoosh", 3),
    ("bat-chu", "pop", 4),
    ("bat-chu", "bubble pop", 2),
    ("nhan-manh", "ding", 3),
    ("nhan-manh", "vine boom", 1),
    ("nhan-manh", "impact", 2),
    ("giao-dien", "mouse click", 2),
    ("giao-dien", "keyboard typing", 2),
    ("giao-dien", "notification", 3),
    ("giao-dien", "windows error", 1),
    ("tien-so", "cash register", 2),
    ("tien-so", "coin", 2),
    ("cong-nghe", "robot beep", 3),
    ("cong-nghe", "scanner", 2),
    ("cam-xuc", "wow", 2),
    ("cam-xuc", "applause", 2),
    ("cam-xuc", "correct answer", 2),
    ("cam-xuc", "wrong answer", 2),
    ("may-anh", "camera shutter", 2),
]


def lay(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def tim(tu_khoa, trang=1):
    """Trả về [(ten, duong_dan_mp3, trang_chi_tiet)] theo thứ tự trang web xếp."""
    q = urllib.parse.urlencode({"name": tu_khoa, "page": trang})
    trang_html = lay(f"{GOC}/en/search/?{q}").decode("utf-8", "replace")
    kq = []
    # Mỗi nút: <div class="instant"> ... play('/media/sounds/x.mp3', ...) ... <a href="/en/instant/slug/" class="instant-link ...">Tên</a>
    for khoi in trang_html.split('class="instant"')[1:]:
        mp3 = re.search(r"play\('([^']+\.mp3)'", khoi)
        ten = re.search(r'href="(/en/instant/[^"]+)"[^>]*class="instant-link[^>]*>([^<]+)<', khoi)
        if mp3 and ten:
            kq.append((html.unescape(ten.group(2)).strip(), mp3.group(1), GOC + ten.group(1)))
    return kq


def doc_muc_luc():
    return json.loads(MUC_LUC.read_text("utf-8")) if MUC_LUC.exists() else {"nguon": GOC, "am_thanh": []}


def ghi_muc_luc(ml):
    KHO.mkdir(parents=True, exist_ok=True)
    ml["am_thanh"].sort(key=lambda a: (a["nhom"], a["file"]))
    MUC_LUC.write_text(json.dumps(ml, ensure_ascii=False, indent=2), "utf-8")


def do_dai(p):
    try:
        return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout), 2)
    except ValueError:
        return None


def tai(tu_khoa, so, nhom, toi_da_giay=8.0):
    ml = doc_muc_luc()
    da_co = {a["url"] for a in ml["am_thanh"]}
    lay_duoc = 0
    for ten, mp3, chi_tiet in tim(tu_khoa):
        if lay_duoc >= so:
            break
        url = GOC + mp3
        if url in da_co:
            continue
        dich = KHO / nhom / Path(mp3).name
        dich.parent.mkdir(parents=True, exist_ok=True)
        dich.write_bytes(lay(url))
        dai = do_dai(dich)
        if dai is None or dai > toi_da_giay:  # hiệu ứng phải ngắn; đoạn dài thường là bài hát/clip
            print(f"  bỏ  {ten} ({dai}s — quá dài cho hiệu ứng)")
            dich.unlink()
            continue
        ml["am_thanh"].append({"nhom": nhom, "file": f"{nhom}/{dich.name}", "ten": ten, "tu_khoa": tu_khoa,
                               "giay": dai, "url": url, "trang": chi_tiet})
        lay_duoc += 1
        print(f"  tải {nhom}/{dich.name}  {dai}s  «{ten}»")
        time.sleep(0.8)
    ghi_muc_luc(ml)
    return lay_duoc


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="lenh", required=True)
    a = sub.add_parser("tim"); a.add_argument("tu_khoa"); a.add_argument("--trang", type=int, default=1)
    b = sub.add_parser("tai"); b.add_argument("tu_khoa"); b.add_argument("--so", type=int, default=3)
    b.add_argument("--nhom", default="khac"); b.add_argument("--toi-da-giay", type=float, default=8.0)
    sub.add_parser("bo-khoi-dau"); sub.add_parser("liet-ke"); sub.add_parser("tai-lai")
    g = ap.parse_args()

    if g.lenh == "tim":
        for i, (ten, mp3, ct) in enumerate(tim(g.tu_khoa, g.trang), 1):
            print(f"{i:2}. {ten}  —  {GOC}{mp3}")
    elif g.lenh == "tai":
        tai(g.tu_khoa, g.so, g.nhom, g.toi_da_giay)
    elif g.lenh == "bo-khoi-dau":
        for nhom, kw, so in BO_KHOI_DAU:
            print(f"[{nhom}] {kw}")
            tai(kw, so, nhom)
    elif g.lenh == "liet-ke":
        for x in doc_muc_luc()["am_thanh"]:
            print(f"{x['file']:<45} {x['giay']:>5}s  {x['ten']}")
    elif g.lenh == "tai-lai":  # máy mới / sau khi clone: tải lại mp3 theo mục lục
        for x in doc_muc_luc()["am_thanh"]:
            p = KHO / x["file"]
            if not p.exists():
                p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(lay(x["url"])); print("tải lại", x["file"])


if __name__ == "__main__":
    main()

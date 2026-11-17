# -*- coding: utf-8 -*-
"""
Kiểm tra kết nối ElevenLabs: key có dùng được không, gói nào, còn bao nhiêu ký tự,
có những giọng nào.

Chạy:  python test-ket-noi.py
"""
import rbw_voice as rv

env = rv.load_env()

print("=" * 64)
print("KIEM TRA KET NOI ELEVENLABS")
print("=" * 64)

# /voices là phép thử thật sự: gọi được = key hop le va du quyen lam viec.
voices = rv.list_voices(env)
print("\n  KET NOI THANH CONG - key hop le")

sub = rv.get_subscription(env)
if sub:
    tier = sub.get("tier", "?")
    used = sub.get("character_count", 0)
    limit = sub.get("character_limit", 0)
    con_lai = limit - used
    print(f"  Goi           : {tier}")
    print(f"  Da dung       : {used:,} / {limit:,} ky tu")
    print(f"  Con lai       : {con_lai:,} ky tu  (~{con_lai // 500} video 30 giay)")
    co_clone = tier.lower() not in ("free", "starter_free", "")
    print(f"  Nhan ban giong: {'CO' if co_clone else 'KHONG - can nang len goi Starter'}")
else:
    print("  Goi / han muc : khong doc duoc (key chua bat quyen 'User' > Read)")
    print("                  -> Khong sao, sinh giong van chay binh thuong.")
    print("                  -> Muon xem han muc: API Keys > sua key > bat User Read.")

tu_tao = [v for v in voices if v.get("category") == "cloned"]
co_san = [v for v in voices if v.get("category") != "cloned"]

vid = env.get("ELEVENLABS_VOICE_ID", "")

print(f"\n  GIONG DA NHAN BAN ({len(tu_tao)}):")
if tu_tao:
    for v in tu_tao:
        dau = " <-- dang dung" if v["voice_id"] == vid else ""
        print(f"    - {v['name']:<26} voice_id = {v['voice_id']}{dau}")
    if not vid:
        # uu tien giong anh Truong, khong lay bua phan tu dau danh sach
        goi_y = next((v for v in tu_tao if "duy" in v["name"].lower()
                      or "truong" in v["name"].lower()), tu_tao[0])
        print(f"\n  -> Chua dat giong. Dan dong nay vao .env:")
        print(f"     ELEVENLABS_VOICE_ID={goi_y['voice_id']}   # {goi_y['name']}")
else:
    print("    (chua co) -> chay `python clone-voice.py` (can goi Starter tro len)")

print(f"\n  GIONG CO SAN ({len(co_san)}) - dung thu ngay khi chua nhan ban:")
for v in co_san[:10]:
    print(f"    - {v['name'][:38]:<40} {v['voice_id']}")

ten_dang_dung = next((v["name"] for v in voices if v["voice_id"] == vid), "")
print(f"\n  ELEVENLABS_VOICE_ID hien tai : {vid or '(chua dat)'}"
      + (f"  ({ten_dang_dung})" if ten_dang_dung else ""))
print(f"  Model                        : {env.get('ELEVENLABS_MODEL', 'eleven_multilingual_v2')}")
print()

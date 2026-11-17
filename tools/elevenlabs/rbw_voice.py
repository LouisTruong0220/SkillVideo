# -*- coding: utf-8 -*-
"""
Lõi dùng chung cho các script ElevenLabs của Duy Trường Robot.
Đọc .env, gọi API, không phụ thuộc SDK (chỉ cần `requests`).
"""
import os
import sys
import json

import requests

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
API = "https://api.elevenlabs.io/v1"


def load_env():
    """Đọc .env cạnh file này. Trả về dict."""
    path = os.path.join(HERE, ".env")
    if not os.path.exists(path):
        raise SystemExit(
            "Chua co file .env.\n"
            "  1. Copy .env.example thanh .env\n"
            "  2. Dan API key vao\n"
            "  Xem HUONG-DAN-LAY-API-KEY.md"
        )
    env = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")

    key = env.get("ELEVENLABS_API_KEY", "")
    if not key or key.startswith("sk_dan_key"):
        raise SystemExit("Chua dien ELEVENLABS_API_KEY thuc trong .env")
    return env


def headers(env, accept=None):
    h = {"xi-api-key": env["ELEVENLABS_API_KEY"]}
    if accept:
        h["Accept"] = accept
    return h


class ThieuQuyen(Exception):
    """Key hợp lệ nhưng không được cấp quyền cho endpoint này."""


def check(resp):
    """Dịch lỗi API sang tiếng Việt dễ hiểu."""
    if resp.ok:
        return resp
    body = resp.text[:400]
    low = body.lower()

    # 401 có HAI nghĩa khác nhau — phải phân biệt:
    #   missing_permissions = key ĐÚNG, chỉ chưa bật quyền cho endpoint này
    #   còn lại             = key sai/đã xoá
    if resp.status_code == 401 and "missing_permissions" in low:
        raise ThieuQuyen(body)

    msg = f"HTTP {resp.status_code}: {body}"
    if resp.status_code == 401:
        msg = "401 - API key sai hoac da bi xoa. Tao key moi tai elevenlabs.io/app/settings/api-keys"
    elif resp.status_code == 402 or "quota" in low:
        msg = "402 - Het han muc ky tu thang nay, hoac tinh nang can goi tra phi (Starter tro len)"
    elif resp.status_code == 403:
        msg = f"403 - Key thieu quyen cho thao tac nay. Vao API Keys > sua key > bat quyen con thieu.\n     {body}"
    elif resp.status_code == 422:
        msg = f"422 - Tham so khong hop le: {body}"
    raise SystemExit("LOI: " + msg)


def get_user(env):
    """None nếu key không có quyền user_read (không sao, chỉ mất thông tin hiển thị)."""
    try:
        return check(requests.get(f"{API}/user", headers=headers(env), timeout=30)).json()
    except ThieuQuyen:
        return None


def get_subscription(env):
    """None nếu key không có quyền user_read."""
    try:
        r = check(requests.get(f"{API}/user/subscription", headers=headers(env), timeout=30))
        return r.json()
    except ThieuQuyen:
        return None


def list_voices(env):
    r = check(requests.get(f"{API}/voices", headers=headers(env), timeout=30))
    return r.json().get("voices", [])


# CHỈ 3 model này có tiếng Việt. Dùng model khác sẽ đọc méo tiếng.
MODEL_CO_TIENG_VIET = ("eleven_v3", "eleven_turbo_v2_5", "eleven_flash_v2_5")


def tts(env, text, out_path, voice_id=None, model=None,
        stability=0.45, similarity=0.9, style=0.0, speed=1.0):
    """Sinh giọng đọc -> ghi ra file MP3. Trả về đường dẫn."""
    vid = voice_id or env.get("ELEVENLABS_VOICE_ID", "")
    if not vid:
        raise SystemExit(
            "Chua co ELEVENLABS_VOICE_ID trong .env.\n"
            "  Chay `python test-ket-noi.py` de xem danh sach giong co san,\n"
            "  hoac `python clone-voice.py` de nhan ban giong anh Truong."
        )
    mdl = model or env.get("ELEVENLABS_MODEL", "eleven_v3")
    if mdl not in MODEL_CO_TIENG_VIET:
        print(f"  CANH BAO: model '{mdl}' KHONG ho tro tieng Viet -> doc se meo tieng.")
        print(f"            Nen dung: {' / '.join(MODEL_CO_TIENG_VIET)}")

    payload = {
        "text": text,
        "model_id": mdl,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": True,
            "speed": speed,
        },
    }
    r = check(requests.post(
        f"{API}/text-to-speech/{vid}",
        headers={**headers(env, "audio/mpeg"), "Content-Type": "application/json"},
        params={"output_format": "mp3_44100_128"},
        data=json.dumps(payload).encode("utf-8"),
        timeout=180,
    ))

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(r.content)
    return out_path


def clone(env, name, audio_files, description=""):
    """Instant Voice Cloning. CAN GOI TRA PHI (Starter tro len)."""
    files = []
    opened = []
    for p in audio_files:
        if not os.path.exists(p):
            raise SystemExit(f"Khong thay file mau giong: {p}")
        fh = open(p, "rb")
        opened.append(fh)
        files.append(("files", (os.path.basename(p), fh, "audio/mpeg")))
    try:
        r = check(requests.post(
            f"{API}/voices/add",
            headers=headers(env),
            data={"name": name, "description": description},
            files=files,
            timeout=300,
        ))
    finally:
        for fh in opened:
            fh.close()
    return r.json()

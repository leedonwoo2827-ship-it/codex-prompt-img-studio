"""codex(OpenAI Codex CLI) 인증 상태 헬퍼.

Codex 는 "Sign in with ChatGPT"(OAuth) 로 로그인하면 API 키 없이 ChatGPT 구독 할당량으로
모델을 쓴다. 로그인 `codex login`, 로그아웃 `codex logout`, 자격증명은 ~/.codex/auth.json.

(260606-googleOuth-aim-od/services/codex/auth.py 패턴 차용·축약.)
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

CODEX_BIN = os.environ.get("CODEX_BIN", "codex")
AUTH_PATH = os.environ.get("CODEX_AUTH_PATH", str(Path.home() / ".codex" / "auth.json"))

_FALLBACK_CODEX_PATHS = [
    os.path.expanduser("~/.local/bin/codex"),
    os.path.expandvars(r"%APPDATA%\npm\codex.cmd"),
    os.path.expandvars(r"%APPDATA%\npm\codex"),
]


def codex_path() -> Optional[str]:
    if os.path.sep in CODEX_BIN or (os.path.altsep and os.path.altsep in CODEX_BIN):
        return CODEX_BIN if os.path.isfile(CODEX_BIN) else None
    found = shutil.which(CODEX_BIN)
    if found:
        return found
    for p in _FALLBACK_CODEX_PATHS:
        if p and os.path.isfile(p):
            return p
    return None


def is_installed() -> bool:
    return codex_path() is not None


def _read_auth() -> Optional[dict]:
    try:
        if os.path.isfile(AUTH_PATH):
            with open(AUTH_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return None


def has_token() -> bool:
    """~/.codex/auth.json 에 사용 가능한 ChatGPT OAuth access_token 이 있으면 True."""
    auth = _read_auth()
    if not isinstance(auth, dict):
        return False
    tokens = auth.get("tokens")
    return isinstance(tokens, dict) and isinstance(tokens.get("access_token"), str)


def _decode_jwt_email(token: str) -> Optional[str]:
    try:
        payload_b64 = token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode("utf-8"))
        for k in ("email", "preferred_username"):
            v = payload.get(k)
            if isinstance(v, str) and "@" in v:
                return v.strip().lower()
        prof = payload.get("https://api.openai.com/auth") or payload.get(
            "https://api.openai.com/profile"
        )
        if isinstance(prof, dict) and isinstance(prof.get("email"), str):
            return prof["email"].strip().lower()
    except Exception:
        pass
    return None


def _deep_find(obj, keys) -> Optional[str]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and isinstance(v, str) and v.strip():
                return v.strip()
        for v in obj.values():
            r = _deep_find(v, keys)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = _deep_find(v, keys)
            if r:
                return r
    return None


def get_account_email() -> Optional[str]:
    auth = _read_auth()
    if not isinstance(auth, dict):
        return None
    email = _deep_find(auth, {"email", "account_email", "preferred_username"})
    if email and "@" in email:
        return email.strip().lower()
    idt = _deep_find(auth, {"id_token", "access_token"})
    if idt and idt.count(".") >= 2:
        return _decode_jwt_email(idt)
    return None


def login_terminal_cmd() -> List[str]:
    return [codex_path() or CODEX_BIN, "login"]


def status() -> dict:
    installed = is_installed()
    authed = has_token()
    return {
        "provider": "codex",
        "label": "OpenAI (ChatGPT)",
        "installed": installed,
        "authenticated": authed,
        "email": (get_account_email() if authed else None),
        "login_hint": "터미널에서 `codex login` 을 실행해 ChatGPT 계정으로 로그인하세요.",
    }

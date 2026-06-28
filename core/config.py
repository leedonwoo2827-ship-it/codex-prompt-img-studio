"""앱 설정 — data/settings.json 에 저장/로드.

이미지 엔진 선택과 기본 생성 옵션을 담는다. codex(키리스) 가 기본이고, gemini(API 키)는
선택적 대체 엔진이다. 키는 코드에 하드코딩하지 않고 사용자가 설정 화면/환경변수로 넣는다.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict

from core.atomic_io import atomic_write_json
from core.constants import SETTINGS_PATH

_DEFAULTS: Dict[str, Any] = {
    "engine": "codex",          # "codex" (키리스) | "gemini" (API 키)
    "default_size": "auto",     # auto | 1024x1024 | 1536x1024 | 1024x1536
    "default_format": "png",    # png | jpeg | webp
    "gemini_api_key": "",       # gemini 엔진을 쓸 때만
    "gemini_model": "gemini-2.5-flash-image",
}


def load_settings() -> Dict[str, Any]:
    data = dict(_DEFAULTS)
    try:
        if os.path.isfile(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                stored = json.load(f)
            if isinstance(stored, dict):
                data.update({k: v for k, v in stored.items() if k in _DEFAULTS})
    except Exception:
        pass
    # 환경변수 우선(있을 때만)
    if os.environ.get("GEMINI_API_KEY"):
        data["gemini_api_key"] = os.environ["GEMINI_API_KEY"].strip()
    return data


def save_settings(patch: Dict[str, Any]) -> Dict[str, Any]:
    data = load_settings()
    for k, v in (patch or {}).items():
        if k in _DEFAULTS:
            data[k] = v
    atomic_write_json(str(SETTINGS_PATH), data)
    return data


def get_setting(key: str, default: Any = None) -> Any:
    return load_settings().get(key, default)

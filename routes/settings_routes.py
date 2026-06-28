"""설정 라우트 — 엔진/기본옵션/Gemini 키 (gemini 키는 응답에서 마스킹)."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from core.config import load_settings, save_settings
from core.constants import SIZE_CHOICES

router = APIRouter(prefix="/api/settings", tags=["settings"])


def _public(s: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(s)
    key = out.get("gemini_api_key") or ""
    out["gemini_api_key_set"] = bool(key)
    out["gemini_api_key"] = (key[:4] + "…" + key[-4:]) if len(key) > 8 else ("설정됨" if key else "")
    out["size_choices"] = SIZE_CHOICES
    return out


class SettingsPatch(BaseModel):
    engine: str | None = None
    default_size: str | None = None
    default_format: str | None = None
    gemini_api_key: str | None = None
    gemini_model: str | None = None


@router.get("")
async def get_settings():
    return _public(load_settings())


@router.post("")
async def update_settings(patch: SettingsPatch):
    data = {k: v for k, v in patch.model_dump().items() if v is not None}
    # 빈 문자열로 키를 지우는 것은 허용하되, 마스킹된 값(…)이 그대로 오면 무시
    if "gemini_api_key" in data and "…" in data["gemini_api_key"]:
        data.pop("gemini_api_key")
    return _public(save_settings(data))

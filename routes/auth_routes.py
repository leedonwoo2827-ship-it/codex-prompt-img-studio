"""인증/상태 라우트 — codex(ChatGPT) 로그인 상태 + 현재 엔진."""
from __future__ import annotations

from fastapi import APIRouter

from core.config import load_settings
from services import codex_auth

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/status")
async def auth_status():
    st = codex_auth.status()
    settings = load_settings()
    st["engine"] = settings.get("engine", "codex")
    # codex 엔진인데 미로그인이면 차단 사유 안내
    st["ready"] = (
        True if settings.get("engine") == "gemini" and settings.get("gemini_api_key")
        else st["authenticated"]
    )
    return st

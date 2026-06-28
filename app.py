# app.py — Codex Studio 오케스트레이터 (프롬프트 빌더 + 이미지 스튜디오 통합)
#
# 두 로컬 앱을 하나의 FastAPI 앱으로 합쳤다.
#   · 앞 워크스페이스 = 프롬프트 빌더  (/api/builder/*)
#   · 뒤 워크스페이스 = 이미지 스튜디오 (/api/auth · /api/settings · /api/projects · /api/images)
# 로그인은 codex-image-studio 방식(ChatGPT OAuth, ~/.codex/auth.json) 하나로 통일했고,
# 빌더의 텍스트/비전 생성도 같은 Codex 백엔드를 쓴다(별도 API 키 불필요).
import mimetypes
import os
import threading
import webbrowser

# Windows 일부 환경에서 .js MIME 매핑이 깨져 ES 모듈 로드가 실패하는 것을 방지
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("application/javascript", ".mjs")

from dotenv import load_dotenv  # noqa: E402

# utf-8-sig: Notepad 로 저장한 .env 의 BOM 을 허용
load_dotenv(encoding="utf-8-sig")

from contextlib import asynccontextmanager  # noqa: E402

import uvicorn  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.responses import FileResponse, Response  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

from core.constants import APP_TITLE, HOST, PORT, PRESETS_DIR, STATIC_DIR  # noqa: E402
from core.database import init_db  # noqa: E402

# 이미지 스튜디오 라우터
from routes.auth_routes import router as auth_router  # noqa: E402
from routes.image_routes import router as image_router  # noqa: E402
from routes.project_routes import router as project_router  # noqa: E402
from routes.settings_routes import router as settings_router  # noqa: E402

# 프롬프트 빌더 라우터 (/api/builder/*)
from routes.builder_archive_routes import router as builder_archive_router  # noqa: E402
from routes.builder_chat_routes import router as builder_chat_router  # noqa: E402
from routes.builder_manuscript_routes import router as builder_manuscript_router  # noqa: E402
from routes.builder_preset_routes import router as builder_preset_router  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=APP_TITLE, lifespan=lifespan)

# 이미지 스튜디오
app.include_router(auth_router)
app.include_router(settings_router)
app.include_router(project_router)
app.include_router(image_router)

# 프롬프트 빌더
app.include_router(builder_chat_router)
app.include_router(builder_preset_router)
app.include_router(builder_archive_router)
app.include_router(builder_manuscript_router)


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


# 프리셋 커버 이미지 서빙 (빌더) — 정적 마운트보다 먼저 등록
app.mount("/presets", StaticFiles(directory=str(PRESETS_DIR)), name="presets")

# 정적 자산 (css/js 등) — 마지막에 마운트 (API·전용 경로와 충돌 방지)
app.mount("/", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _open_browser():
    try:
        webbrowser.open(f"http://{HOST}:{PORT}/")
    except Exception:
        pass


def _port_in_use(host: str, port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


if __name__ == "__main__":
    # 이미 다른 인스턴스가 떠 있으면(포트 사용중) 그냥 브라우저만 열고 종료(더블클릭 친화).
    if _port_in_use(HOST, PORT):
        print(f"\n  이미 실행 중입니다 → 브라우저를 엽니다: http://{HOST}:{PORT}/\n")
        _open_browser()
        raise SystemExit(0)

    threading.Timer(1.2, _open_browser).start()
    print(f"\n  Codex Studio → http://{HOST}:{PORT}/\n")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")

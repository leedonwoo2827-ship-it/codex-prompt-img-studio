# 시스템 구조 & API

통합 앱(프롬프트 빌더 + 이미지 스튜디오)의 내부 구조 메모.

## 디렉터리 구조

```
app.py                       # 통합 FastAPI 진입점 (단일 포트 8765, 단일 정적 마운트)
core/                        # 경로/설정/DB (이미지 스튜디오 + 빌더 경로 통합)
  constants.py               # 경로·포트·이미지 사이즈 + 빌더 자산 경로(PROMPTS/PRESETS/ARCHIVES)
  config.py                  # 엔진/기본옵션/Gemini 키 (data/settings.json)
  database.py                # SQLite (Project / Image / EditEvent)
  atomic_io.py               # 원자적 JSON 저장
services/
  codex_auth.py              # ChatGPT OAuth 상태 + 로그인/로그아웃 콘솔 실행
  codex_image.py             # 이미지 생성/수정/병합 (Codex Responses API · SSE)
  codex_text.py              # 빌더 텍스트·비전 (codex_image 의 토큰/스트림 재사용) ← 신규
  prompt_spec.py             # 빌더 시스템 프롬프트 조립
  presets.py / archive.py / manuscript.py   # 프리셋 / 보관함 / 원고 추출
routes/
  auth · settings · project · image_routes.py        # /api/*        (스튜디오)
  builder_chat · preset · archive · manuscript_routes.py   # /api/builder/* (빌더)
static/
  index.html                 # 워크스페이스 전환 셸 + 두 UI
  css/tokens.css · app.css   # Miro 디자인 토큰 + 통합 스타일
  js/shell.js · app.js · builder.js · api.js
  manual.html                # 앱 내 프롬프트 매뉴얼
prompts/ · presets/          # 빌더 자산 (브랜드 가이드 · 스타일 카탈로그 · 프리셋)
data/                        # 런타임 (app.db · images/ · settings.json · archives.json) — git 제외
```

## 워크스페이스 & API 네임스페이스

| 워크스페이스 | UI | API |
|---|---|---|
| ✍️ 프롬프트 빌더 (앞) | 자유 빌더(채팅) · 프롬프트 생성기 · 보관함 | `/api/builder/*` |
| 🎨 이미지 스튜디오 (뒤) | 갤러리 · 뷰어/편집 · 병합 · 큐 | `/api/auth` · `/api/settings` · `/api/projects` · `/api/images` |

- 빌더 API는 모두 `/api/builder/*` 로 묶어 스튜디오 `/api/*` 와 충돌을 피했습니다.
- 정적 자산은 `/` 단일 마운트, 프리셋 커버는 `/presets` 마운트.

## 로그인(인증) — 하나로 통일

- **ChatGPT OAuth** (`~/.codex/auth.json`) 하나로 빌더의 텍스트·비전과 스튜디오의 이미지 생성이 모두 동작.
- 핵심: `services/codex_text.py` 가 `services/codex_image.py` 의 토큰 로드·401 자동 갱신·SSE 스트림 파싱을
  **재사용**해, 텍스트/비전도 같은 Codex Responses 엔드포인트로 호출합니다. (LiteLLM/별도 API 키 불필요)
- `codex_image.py` 의 엔드포인트는 Codex CLI 가 쓰는 **비공식 내부 엔드포인트**라 OpenAI 측 변경 시 영향받을 수 있습니다.

## 엔진

- 기본: **ChatGPT (gpt-image-2 이미지 / Codex 텍스트)** — 키리스
- 대체: **Gemini** (`gemini-2.5-flash-image`) — 설정에서 API 키 입력 시 이미지 생성 대체. 할당량 절약·비교용.

## 프롬프트 큐 (보관함 → 스튜디오)

- 빌더 「📌 보관」 → `data/archives.json`
- 스튜디오 `📋` → 보관 프롬프트 선택 → (옵션) 코드블록(컷) 단위로 분리해 큐 적재
- 한 장씩 자동 입력 → 생성 성공 시 다음 프롬프트 자동 입력 (일괄 동시 생성 아님)

## 데이터/프라이버시

- 이미지·기록·설정·토큰은 전부 **로컬**(`data/`, `~/.codex/`)에만 저장. `data/` 와 `.env` 는 git 에서 제외.

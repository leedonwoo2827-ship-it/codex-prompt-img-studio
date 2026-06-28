# Codex Studio — 프롬프트 빌더 & 이미지 스튜디오 (통합 로컬 앱)

두 개의 로컬 앱을 하나로 합친 단일 FastAPI 앱입니다.

- **앞 워크스페이스 · 프롬프트 빌더** — 원고/레퍼런스를 바탕으로 이미지 생성용 프롬프트를 자동으로 만들어 줍니다. (자유 빌더 채팅 / 프롬프트 생성기 / 보관함)
- **뒤 워크스페이스 · 이미지 스튜디오** — 만든 프롬프트로 이미지를 생성·수정·병합합니다.

상단바의 탭으로 두 워크스페이스를 오갑니다.

## 로그인 (codex-image-studio 방식 · 하나로 통일)

API 키가 필요 없습니다. **ChatGPT 구독 계정으로 로그인**하면 빌더의 텍스트·비전 생성과
스튜디오의 이미지 생성이 모두 같은 로그인으로 동작합니다.

```
codex login
```

자격증명은 `~/.codex/auth.json` 에 저장되며, 토큰이 만료되면 자동 갱신됩니다.

## 설치 & 실행

**Windows**
1. `setup.bat` 더블클릭 — 가상환경 생성, 의존성 설치, `codex login` 안내
2. `run.bat` 더블클릭 — 브라우저에서 `http://127.0.0.1:8765/` 자동 열림

**macOS (Apple) — 더블클릭**
1. 먼저 준비물 설치: [Python 3](https://www.python.org/downloads/macos/) 와 [Node.js](https://nodejs.org/) (각 설치 파일 더블클릭)
2. 이 저장소를 내려받아 압축을 풉니다. (초록색 **Code → Download ZIP**)
3. **최초 1회만** 터미널에서 아래를 복사해 실행 — ZIP 다운로드는 실행권한·보안격리가 걸려 있어 풀어줘야 합니다:
   ```bash
   cd ~/Downloads/codex-prompt-img-studio-master   # 압축 푼 폴더 경로
   xattr -dr com.apple.quarantine .                # 보안 격리 해제
   chmod +x setup.command run.command setup.sh run.sh
   ```
   > 폴더를 터미널로 끌어다 놓으면 경로가 자동 입력됩니다. (`cd ` 입력 후 폴더 드래그)
4. **`setup.command` 더블클릭** — 환경 설치 + ChatGPT 로그인 (브라우저 자동 열림)
5. 이후엔 **`run.command` 더블클릭** — 서버 실행 + 브라우저 자동 열림 (`http://127.0.0.1:8765/`)
   - 종료: 열린 터미널 창에서 `Control+C` 또는 창 닫기

> 처음 더블클릭 시 "확인되지 않은 개발자" 경고가 뜨면, 파일을 **우클릭 → 열기**를 선택하세요.

**Linux**
```bash
chmod +x setup.sh run.sh   # 최초 1회 (git clone 시엔 보통 불필요)
./setup.sh                 # 가상환경 + 의존성 + codex login
./run.sh                   # 서버 실행 → http://127.0.0.1:8765/
```

> iOS/iPadOS 등 모바일은 로컬 Python 서버 실행이 불가하여 지원하지 않습니다(데스크톱 전용).

## 구조

```
app.py                       # 통합 FastAPI 진입점 (단일 포트 8765, 단일 정적 마운트)
core/                        # 경로/설정/DB (이미지 스튜디오 + 빌더 경로 통합)
services/
  codex_auth.py              # ChatGPT OAuth 상태
  codex_image.py             # 이미지 생성/수정/병합 (Codex Responses API)
  codex_text.py              # 빌더 텍스트·비전 (같은 Codex 백엔드 재사용) ← 신규
  prompt_spec / presets / archive / manuscript.py   # 빌더 서비스
routes/
  auth · settings · project · image_routes.py        # /api/* (스튜디오)
  builder_*_routes.py                                # /api/builder/* (빌더)
static/
  index.html                 # 워크스페이스 전환 셸 + 두 UI
  css/tokens.css · app.css   # Miro 디자인 토큰 + 통합 스타일
  js/shell.js · app.js · builder.js · api.js
prompts/ · presets/          # 빌더 자산
data/                        # 런타임 (app.db · images/ · settings.json · archives.json)
```

## 디자인

UI 는 **Miro 스타일**의 디자인 토큰(색 팔레트, 타이포, 필(pill) 버튼, 카드, 라운드, 엘리베이션)을
작업 도구 화면에 적용해 SaaS 등급으로 마감했습니다. (디자인 스펙 원본은 저장소에 포함하지 않습니다.)
Roobert PRO 는 비공개 폰트라 한글 지원이 우수한 Pretendard 로 대체했습니다.

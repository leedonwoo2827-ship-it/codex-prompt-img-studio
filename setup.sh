#!/usr/bin/env bash
# Codex Studio - 최초 설정 (Linux / macOS)
set -e
cd "$(dirname "$0")"

echo
echo "============================================"
echo "  Codex Studio - First-time Setup (Linux/macOS)"
echo "============================================"
echo

# -- Python 3.10+ 찾기 --
PY=""
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
fi
if [ -z "$PY" ]; then
  echo "[ERROR] Python 3 가 필요합니다. python.org 또는 패키지 매니저(brew/apt)로 설치 후 다시 실행하세요."
  exit 1
fi

# -- 가상환경 --
if [ ! -x "venv/bin/python" ]; then
  echo "[1/3] 가상환경 생성..."
  "$PY" -m venv venv
fi

echo "[2/3] 의존성 설치..."
# shellcheck disable=SC1091
. venv/bin/activate
python -m pip install --upgrade pip >/dev/null
pip install -r requirements.txt

# -- codex CLI + ChatGPT 로그인 --
echo "[3/3] ChatGPT(codex) 로그인 확인..."
if ! command -v codex >/dev/null 2>&1; then
  echo "  codex CLI 가 없습니다. 설치를 시도합니다... (npm 필요)"
  if command -v npm >/dev/null 2>&1; then npm i -g @openai/codex || true; fi
fi
if [ -f "$HOME/.codex/auth.json" ]; then
  echo "  이미 로그인되어 있습니다."
elif command -v codex >/dev/null 2>&1; then
  echo "  브라우저로 ChatGPT 로그인을 진행합니다..."
  codex login || true
else
  echo "  [안내] codex 설치 후 터미널에서 'codex login' 을 직접 실행하세요."
fi

echo
echo "설정 완료! ./run.sh 로 실행하세요."
echo

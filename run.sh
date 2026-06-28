#!/usr/bin/env bash
# Codex Studio - 실행 (Linux / macOS)
set -e
cd "$(dirname "$0")"

if [ ! -x "venv/bin/python" ]; then
  echo "최초 설정이 필요합니다. setup.sh 를 실행합니다..."
  bash ./setup.sh
fi

# shellcheck disable=SC1091
. venv/bin/activate
echo "Codex Studio 시작... → http://127.0.0.1:8765"
python app.py

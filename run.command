#!/usr/bin/env bash
# Codex Studio - macOS 더블클릭 실행
# Finder 에서 더블클릭하면 터미널이 열리며 서버가 시작되고 브라우저가 열립니다.
# 종료하려면 이 터미널 창에서 Control+C 를 누르거나 창을 닫으세요.
cd "$(dirname "$0")"
bash ./run.sh

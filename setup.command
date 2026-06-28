#!/usr/bin/env bash
# Codex Studio - macOS 더블클릭 설치
# Finder 에서 더블클릭하면 터미널이 열리며 실행됩니다.
cd "$(dirname "$0")"

bash ./setup.sh
status=$?

echo
if [ $status -eq 0 ]; then
  echo "✅ 설치가 끝났습니다. 이제 run.command 를 더블클릭해 실행하세요."
else
  echo "⚠️ 설치 중 문제가 있었습니다. 위 메시지를 확인하세요."
fi
echo
read -n 1 -s -r -p "아무 키나 누르면 이 창이 닫힙니다..."
echo

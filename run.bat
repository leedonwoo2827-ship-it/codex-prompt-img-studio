@echo off
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
  echo First-time setup required. Running setup.bat...
  call setup.bat
)

call venv\Scripts\activate.bat
echo Starting Codex Studio...
python app.py
pause

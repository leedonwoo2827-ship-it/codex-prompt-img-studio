@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================
echo   Codex Studio - First-time Setup
echo ============================================
echo.

REM -- Find Python 3.10+ --
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY ( where python >nul 2>nul && set "PY=python" )
if not defined PY (
  echo [ERROR] Python not found. Install from https://www.python.org/downloads/ then run again.
  pause & exit /b 1
)

REM -- Create virtual environment --
if not exist "venv\Scripts\python.exe" (
  echo [1/3] Creating virtual environment...
  %PY% -m venv venv || ( echo [ERROR] venv creation failed & pause & exit /b 1 )
)

echo [2/3] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
pip install -r requirements.txt || ( echo [ERROR] dependency install failed & pause & exit /b 1 )

REM -- codex CLI + ChatGPT login --
echo [3/3] Checking ChatGPT (codex) login...
where codex >nul 2>nul
if errorlevel 1 (
  echo   codex CLI not found. Trying to install via npm...
  where npm >nul 2>nul && npm i -g @openai/codex
)
if exist "%USERPROFILE%\.codex\auth.json" (
  echo   Already logged in.
) else (
  echo   Opening browser for ChatGPT login...
  codex login
)

echo.
echo Setup complete. Double-click run.bat to start.
echo.
pause

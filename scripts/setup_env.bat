@echo off
REM Create & activate venv with supported Python (3.12 / 3.11 / 3.10). Avoid pre-release 3.14 builds (pygame wheel missing).
REM Usage: setup_env.bat [/help]
if /I "%1"=="/help" (
  echo Usage: setup_env.bat
  echo   Creates .venv using Python 3.12 or 3.11 (falls back to 3.10 if logic updated) and installs requirements.
  echo   Automatically upgrades pip/setuptools/wheel and installs requirements/dev if files present.
  exit /b 0
)

set "PY_CMD="
for %%P in (python3.12.exe python312.exe py -3.12 python3.11.exe python311.exe py -3.11 python3.10.exe python310.exe py -3.10) do (
  %%P -c "import sys; sys.exit(0 if (3,10) <= sys.version_info < (3,14) else 1)" 2>nul
  if not errorlevel 1 (
    set "PY_CMD=%%P"
    goto :found
  )
)

echo ERROR: Supported Python (3.10 - 3.13 exclusive) not found. Install Python 3.12 or 3.11 from https://www.python.org/downloads/
exit /b 1

:found
for /f "tokens=2 delims= " %%v in ('%PY_CMD% --version') do set "FOUND_VER=%%v"
echo Using %PY_CMD% (version %FOUND_VER%)
if exist .venv (
  echo .venv already exists. Skipping creation.
) else (
  %PY_CMD% -m venv .venv || exit /b 1
)
set "VENV_PY=.venv\Scripts\python.exe"
if not exist %VENV_PY% (
  echo ERROR: Virtual environment python not found.
  exit /b 1
)

rem Use venv python explicitly (no reliance on activation side-effects)
%VENV_PY% -m pip install --upgrade pip setuptools wheel
if exist requirements.txt %VENV_PY% -m pip install -r requirements.txt
if exist requirements-dev.txt %VENV_PY% -m pip install -r requirements-dev.txt
echo Environment ready. To use manually: .venv\Scripts\activate.bat

@echo off
REM Auto-start script: ensure venv, upgrade (once per day), then leave environment ready for PyCharm terminal.
REM Usage: auto_start_env.bat [/force] [/noupgrade] [/quiet] [/pause] [/help] [/diag]
REM Exit codes: 0=OK,1=Failure,2=Critical packages missing

setlocal ENABLEDELAYEDEXPANSION
set "FORCE=0"
set "NOUPGRADE=0"
set "QUIET=0"
set "HELP=0"
set "DIAG=0"
set "CRITICAL_PKGS=pygame"
for %%A in (%*) do if /I "%%~A"=="/force" set "FORCE=1"
for %%A in (%*) do if /I "%%~A"=="/noupgrade" set "NOUPGRADE=1"
for %%A in (%*) do if /I "%%~A"=="/quiet" set "QUIET=1"
for %%A in (%*) do if /I "%%~A"=="/help" set "HELP=1"
for %%A in (%*) do if /I "%%~A"=="/diag" set "DIAG=1"
if "%HELP%"=="1" (
  echo Usage: auto_start_env.bat [/force] [/noupgrade] [/quiet] [/pause] [/help] [/diag]
  echo.
  echo   /force      Force dependency upgrade even if already done today.
  echo   /noupgrade  Skip dependency upgrade (still reports outdated pkgs).
  echo   /quiet      Suppress informational output.
  echo   /pause      Pause before closing (handy in double-click).
  echo   /diag       Print diagnostic info about environment and exit.
  echo   /help       Show this help and exit.
  echo.
  echo Exit codes: 0=Success, 1=Script failure, 2=Critical package(s) missing.
  endlocal & exit /b 0
)

REM If venv Python exists, use it; otherwise attempt creation via setup_env.bat
set "VENV_PY=.venv\Scripts\python.exe"
if not exist %VENV_PY% (
  call "%~dp0setup_env.bat" || goto :fail
)
if not exist %VENV_PY% (
  echo ERROR: Virtual environment python not found after setup. Aborting.
  goto :fail
)

if "%DIAG%"=="1" (
  echo === Environment Diagnostics ===
  %VENV_PY% - <<EOF 2>nul
import sys, os, platform, site, importlib
print('Python Executable :', sys.executable)
print('Version           :', sys.version.replace('\n',' '))
print('Platform          :', platform.platform())
print('sys.prefix        :', sys.prefix)
print('sys.base_prefix   :', getattr(sys,'base_prefix','?'))
print('In venv           :', sys.prefix != getattr(sys,'base_prefix',''))
print('Site-Pkgs         :', site.getsitepackages())
print('PATH first entry  :', os.environ.get('PATH','').split(os.pathsep)[0])
for name in '%CRITICAL_PKGS%'.split():
    try:
        importlib.import_module(name)
        print(f'Import {name:12}: OK')
    except Exception as e:
        print(f'Import {name:12}: FAIL - {e}')
EOF
  endlocal & exit /b 0
)

REM Daily upgrade guard
set "MARKER=.venv\last_upgrade.txt"
for /f "usebackq tokens=*" %%D in (`powershell -NoLogo -NoProfile -Command "Get-Date -Format yyyy-MM-dd"`) do set "TODAY=%%D"
if exist "%MARKER%" (
  set /p LAST=<"%MARKER%"
) else (
  set "LAST=NEVER"
)
if "%FORCE%"=="0" if /I "%LAST%"=="%TODAY%" (
  echo (Skip) Dependencies already upgraded today (%TODAY%). Use /force to override.
  goto :report
)

if "%QUIET%"=="0" echo Upgrading core tooling...
if "%NOUPGRADE%"=="0" (
  %VENV_PY% -m pip install --upgrade pip setuptools wheel >nul 2>&1
  if "%QUIET%"=="0" echo Upgrading project dependencies (requirements)...
  if exist requirements.txt if "%QUIET%"=="0" (
    %VENV_PY% -m pip install -r requirements.txt --upgrade
  ) else if exist requirements.txt (
    %VENV_PY% -m pip install -r requirements.txt --upgrade >nul 2>&1
  )
  if exist requirements-dev.txt if "%QUIET%"=="0" (
    %VENV_PY% -m pip install -r requirements-dev.txt --upgrade
  ) else if exist requirements-dev.txt (
    %VENV_PY% -m pip install -r requirements-dev.txt --upgrade >nul 2>&1
  )
  >"%MARKER%" echo %TODAY%
) else (
  if "%QUIET%"=="0" echo (Skip) Upgrade skipped due to /noupgrade flag.
)

:report
if "%QUIET%"=="0" echo Outdated package report (informational):
set "TMP_REPORT=%TEMP%\_pip_outdated_report_%RANDOM%.py"
(
  echo import json, subprocess, sys
  echo try:
  echo ^    r = subprocess.check_output([sys.executable,'-m','pip','list','--outdated','--format','json'], text=True)
  echo ^    data = json.loads(r)
  echo except Exception as e:
  echo ^    print('  (Could not generate report)', e)
  echo ^    data = []
  echo if not data:
  echo ^    print('  All up to date.')
  echo else:
  echo ^    for p in data:
  echo ^        print(f"  {p['name']}: {p['version']} -> {p['latest_version']}")
) > "%TMP_REPORT%"
if "%QUIET%"=="0" (
  "%VENV_PY%" "%TMP_REPORT%" 2>nul
) else (
  "%VENV_PY%" "%TMP_REPORT%" >nul 2>&1
)
if exist "%TMP_REPORT%" del /f /q "%TMP_REPORT%" >nul 2>&1

REM Critical package presence check
set "TMP_CHECK=%TEMP%\_pip_check_%RANDOM%.py"
(
  echo import sys
  echo pkgs = "%CRITICAL_PKGS%".split()
  echo missing=[]
  echo for n in pkgs:
  echo ^    try: __import__(n)
  echo ^    except Exception: missing.append(n)
  echo if missing: print('MISSING:'+' '.join(missing))
) >"%TMP_CHECK%"
for /f "usebackq tokens=* delims=" %%L in (`"%VENV_PY%" "%TMP_CHECK%" 2^>nul`) do set "CHECK_OUT=%%L"
if exist "%TMP_CHECK%" del /f /q "%TMP_CHECK%" >nul 2>&1
if defined CHECK_OUT (
  echo ERROR: Critical packages not importable: !CHECK_OUT:~8!
  endlocal & exit /b 2
)

if "%QUIET%"=="0" echo Virtual environment ready. (Python:)
if "%QUIET%"=="0" %VENV_PY% --version

for %%A in (%*) do if /I "%%~A"=="/pause" (if "%QUIET%"=="0" echo Press any key to continue . . . & pause >nul)
endlocal
exit /b 0

:fail
echo Auto-start script failed.
endlocal
exit /b 1

<#!
.SYNOPSIS
  Ensure virtual env exists, activate it for current session, and (optionally) upgrade dependencies once per day.
.DESCRIPTION
  Use this script in PyCharm (Settings > Tools > Terminal) by setting the shell path to:
    powershell -NoLogo -NoExit -ExecutionPolicy Bypass -File scripts/auto_start_env.ps1
.PARAMETER Force
  Force dependency upgrade even if already upgraded today.
.PARAMETER Quiet
  Suppress some informational output.
.PARAMETER NoUpgrade
  Suppress upgrade of dependencies.
.PARAMETER Critical
  Specify critical packages to check for import errors (default: pygame).
.EXAMPLE
  ./scripts/auto_start_env.ps1 -Force
#>
[CmdletBinding()]
param(
  [switch]$Force,
  [switch]$Quiet,
  [switch]$NoUpgrade,
  [string[]]$Critical = @('pygame'),
  [switch]$Help
)
$ErrorActionPreference = 'Stop'

function Write-Info($msg){ if(-not $Quiet){ Write-Host $msg -ForegroundColor Cyan } }

if($Help){
  Write-Host "Usage: auto_start_env.ps1 [-Force] [-NoUpgrade] [-Quiet] [-Critical name1,name2] [-Help]" -ForegroundColor Yellow
  Write-Host ""; Write-Host "  -Force       Force dependency upgrade even if already done today.";
  Write-Host "  -NoUpgrade   Skip dependency upgrade (still shows outdated report).";
  Write-Host "  -Quiet       Suppress informational output.";
  Write-Host "  -Critical    One or more critical packages to verify (default: pygame).";
  Write-Host "  -Help        Show this help and exit.";
  Write-Host ""; Write-Host "Exit codes: 0=Success, 1=Script failure, 2=Critical package(s) missing.";
  exit 0
}

# Move to repo root (script is in scripts/)
Set-Location -Path (Join-Path $PSScriptRoot '..')

# Re-use existing batch setup (handles creation & base install)
Write-Info "Ensuring virtual environment (.venv) exists..."
& "$PSScriptRoot/setup_env.bat" | Out-Null
if(-not (Test-Path .venv)) { throw 'Virtual environment creation failed.' }

# Activate for current PowerShell session
$activate = Join-Path .venv 'Scripts' 'Activate.ps1'
. $activate

# Daily upgrade marker logic
$marker = '.venv/last_upgrade.txt'
$today  = Get-Date -Format 'yyyy-MM-dd'
$doUpgrade = $true
if($NoUpgrade){ $doUpgrade = $false }
if(-not $Force -and -not $NoUpgrade -and (Test-Path $marker)){
  $last = Get-Content $marker -ErrorAction SilentlyContinue | Select-Object -First 1
  if($last -eq $today){
    if(-not $Quiet){ Write-Host "(Skip) Dependencies already upgraded today ($today). Use -Force to override." -ForegroundColor DarkGray }
    $doUpgrade = $false
  }
}

if($doUpgrade){
  Write-Info 'Upgrading pip tooling...'
  python -m pip install --upgrade pip setuptools wheel | Out-Null
  if(Test-Path requirements.txt){ Write-Info 'Upgrading runtime dependencies...'; pip install --upgrade -r requirements.txt }
  if(Test-Path requirements-dev.txt){ Write-Info 'Upgrading dev dependencies...'; pip install --upgrade -r requirements-dev.txt }
  Set-Content -Path $marker -Value $today -NoNewline
} elseif($NoUpgrade) {
  Write-Info '(Skip) Upgrade suppressed by -NoUpgrade.'
}

# Outdated report always (informational)
if(-not $Quiet){ Write-Info 'Outdated package report:' }
$reportScript = Join-Path $env:TEMP ("_pip_outdated_report_{0}.py" -f ([guid]::NewGuid().ToString('N')))
$reportPy = @'
import json, subprocess, sys
try:
    raw = subprocess.check_output([sys.executable,'-m','pip','list','--outdated','--format','json'], text=True)
    data = json.loads(raw)
except Exception as e:
    print('  (Could not retrieve report)', e)
    data = []
if not data:
    print('  All up to date within constraints.')
else:
    for pkg in data:
        print(f"  {pkg['name']}: {pkg['version']} -> {pkg['latest_version']}")
'@
Set-Content -Path $reportScript -Value $reportPy -NoNewline
try {
  $report = & python $reportScript 2>$null
  if(-not $Quiet){ $report | ForEach-Object { Write-Info $_ } }
} catch { if(-not $Quiet){ Write-Info '  (Report failed)'} }
Remove-Item $reportScript -Force -ErrorAction SilentlyContinue

# Critical package import check
if($Critical -and $Critical.Count -gt 0){
  $critScript = Join-Path $env:TEMP ("_pip_crit_check_{0}.py" -f ([guid]::NewGuid().ToString('N')))
  $critList = ($Critical | ForEach-Object { "'$_'" }) -join ', '
  $critPy = @"
import sys
missing=[]
for name in [$critList]:
    try: __import__(name)
    except Exception: missing.append(name)
if missing:
    print('MISSING:'+' '.join(missing))
"@
  Set-Content -Path $critScript -Value $critPy -NoNewline
  try {
    $critOut = & python $critScript 2>$null
  } catch { $critOut = '' }
  Remove-Item $critScript -Force -ErrorAction SilentlyContinue
  if($critOut -and $critOut.StartsWith('MISSING:')){
    $miss = $critOut.Substring(8)
    Write-Host "ERROR: Critical packages not importable: $miss" -ForegroundColor Red
    exit 2
  }
}

Write-Info 'Virtual environment ready.'
